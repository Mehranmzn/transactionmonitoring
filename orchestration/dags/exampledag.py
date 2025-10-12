from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from src.typing.config_types import ModelTrainerConfig
from src.typing.artifact_types import DataTransformationArtifact
from src.exception.exception import SrcException
from src.components.model_trainer import ModelTrainer
from src.utils.main_utils.utils import load_numpy_array_data

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
with DAG(
    dag_id='transaction_monitoring_ml_pipeline',
    default_args=default_args,
    description='Transaction Monitoring ML Pipeline',
    schedule_interval='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False,
) as dag:

    # Task 1: Load data
    def load_data(**kwargs):
        try:
            logging.info("Loading training and testing data...")
            data_transformation_artifact = kwargs['data_transformation_artifact']
            train_file_path = data_transformation_artifact.transformed_train_file_path
            test_file_path = data_transformation_artifact.transformed_test_file_path

            # Load numpy arrays
            train_arr = load_numpy_array_data(train_file_path)
            test_arr = load_numpy_array_data(test_file_path)
            
            x_train, y_train, x_test, y_test = (
                train_arr[:, :-1],
                train_arr[:, -1],
                test_arr[:, :-1],
                test_arr[:, -1],
            )
            
            return {
                "x_train": x_train,
                "y_train": y_train,
                "x_test": x_test,
                "y_test": y_test,
            }
        except Exception as e:
            raise SrcException(e, sys)

    task_load_data = PythonOperator(
        task_id='load_data',
        python_callable=load_data,
        provide_context=True,
        dag=dag,
    )

    # Task 2: Train model
    def train_model(**kwargs):
        try:
            logging.info("Training the model...")
            model_trainer_config = kwargs['model_trainer_config']
            data_transformation_artifact = kwargs['data_transformation_artifact']

            xcom_data = kwargs['ti'].xcom_pull(task_ids='load_data')
            x_train, y_train, x_test, y_test = (
                xcom_data['x_train'],
                xcom_data['y_train'],
                xcom_data['x_test'],
                xcom_data['y_test'],
            )

            model_trainer = ModelTrainer(
                model_trainer_config=model_trainer_config,
                data_transformation_artifact=data_transformation_artifact,
            )
            model_trainer_artifact = model_trainer.train_model(
                x_train, y_train, x_test, y_test
            )
            
            return model_trainer_artifact
        except Exception as e:
            raise SrcException(e, sys)

    task_train_model = PythonOperator(
        task_id='train_model',
        python_callable=train_model,
        provide_context=True,
        dag=dag,
    )

    # Task 3: Track experiments with MLflow
    def track_experiments(**kwargs):
        try:
            logging.info("Tracking experiments with MLflow...")
            ti = kwargs['ti']
            model_trainer_artifact = ti.xcom_pull(task_ids='train_model')
            model_trainer = ModelTrainer(
                model_trainer_config=None,  # Assuming the config is embedded in the artifact
                data_transformation_artifact=None,
            )
            
            # Log metrics and model
            model_trainer.track_mlflow(
                best_model=model_trainer_artifact.best_model,
                classificationmetric=model_trainer_artifact.test_metric_artifact,
            )
        except Exception as e:
            raise SrcException(e, sys)

    task_track_experiments = PythonOperator(
        task_id='track_experiments',
        python_callable=track_experiments,
        provide_context=True,
        dag=dag,
    )

    # Task 4: Save final model
    def save_final_model(**kwargs):
        try:
            logging.info("Saving the final model...")
            ti = kwargs['ti']
            model_trainer_artifact = ti.xcom_pull(task_ids='train_model')

            # Save the trained model to a defined path
            save_object("final_model/final_model.pkl", model_trainer_artifact.trained_model_file_path)
        except Exception as e:
            raise SrcException(e, sys)

    task_save_final_model = PythonOperator(
        task_id='save_final_model',
        python_callable=save_final_model,
        provide_context=True,
        dag=dag,
    )

    # Define task dependencies
    task_load_data >> task_train_model >> task_track_experiments >> task_save_final_model
