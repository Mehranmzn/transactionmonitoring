from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.data_validation import DataValidation
from src.exception.exception import SrcException
from src.logging.logger import logging
from src.typing.config_types import DataIngestionConfig, TrainingPipelineConfig, DataValidationConfig
from src.typing.config_types import DataTransformationConfig, ModelTrainerConfig
from src.components.model_trainer import ModelTrainer

if __name__=='__main__':
    try:
        trainingpuipeline_config=TrainingPipelineConfig()
        data_ingestion_config=DataIngestionConfig(trainingpuipeline_config)
        data_ingestion_obj=DataIngestion(data_ingestion_config)
        logging.info("Exporting collection as dataframe")
        dataingestionartifact = data_ingestion_obj.initiate_data_ingestion()
        logging.info("Data ingestion completed")
        print(dataingestionartifact)

        data_validation_config=DataValidationConfig(trainingpuipeline_config)
        data_validation = DataValidation(dataingestionartifact,data_validation_config)
        logging.info("Initiating data validation")
        data_validation_artifact = data_validation.initiate_data_validation()
        logging.info("Data validation completed")
        print(data_validation_artifact)

        data_transformation_config = DataTransformationConfig(trainingpuipeline_config)
        logging.info("Initiating data transformation")
        data_transformation = DataTransformation(data_validation_artifact, data_transformation_config)
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        print(data_transformation_artifact)
        logging.info("Data transformation completed")

        logging.info("Initiating model training")
        model_trainer_config = ModelTrainerConfig(trainingpuipeline_config)
        model_trainer = ModelTrainer(model_trainer_config = model_trainer_config, data_transformation_artifact = data_transformation_artifact)
        model_trainer_artifact = model_trainer.initiate_model_trainer()
        logging.info("Model training completed")


    except SrcException as e:
        logging.error(e)
    except Exception as e:
        logging.error(e)