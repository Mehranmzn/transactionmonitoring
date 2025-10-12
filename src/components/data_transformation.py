import sys
import os
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline

from src.constant.training_pipeline import TARGET_COLUMN
from src.constant.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS

from src.typing.artifact_types import (
    DataTransformationArtifact,
    DataValidationArtifact
)

from src.typing.config_types import DataTransformationConfig
from src.exception.exception import SrcException 
from src.logging.logger import logging
from src.utils.main_utils.utils import save_numpy_array_data,save_object

class DataTransformation:
    def __init__(self,data_validation_artifact:DataValidationArtifact,
                 data_transformation_config:DataTransformationConfig):
        try:
            self.data_validation_artifact:DataValidationArtifact=data_validation_artifact
            self.data_transformation_config:DataTransformationConfig=data_transformation_config
        except Exception as e:
            raise SrcException(e,sys)
        
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise SrcException(e, sys)
        
    def get_data_transformer_object(cls) -> Pipeline:
        """
        Initialize the data transformer pipeline with KNNImputer and OneHotEncoder for categorical columns.
        """
        logging.info(
            "Entered get_data_transformer_object method of Transformation class"
        )
        try:
            # Initialize the KNNImputer
            imputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logging.info(
                f"Initialized KNNImputer with {DATA_TRANSFORMATION_IMPUTER_PARAMS}"
            )

            # OneHotEncoder for categorical columns
            categorical_columns = ['Sender_bank_location',
                                   'Receiver_bank_location', 'Payment_type', "Payment_currency", "Received_currency"]
            numerical_columns = ['Amount', 'hour', 'minute', 'second', 'year', 'month', 'day', 'day_of_week', 'is_weekend',
                                 'Sender_account', 'Receiver_account']
            categorical_transformer = OneHotEncoder(handle_unknown='ignore', sparse_output=False)

            # Combine the transformations using ColumnTransformer
            preprocessor = ColumnTransformer(
                transformers=[
                    ("onehot", categorical_transformer, categorical_columns),  # Apply OneHotEncoder to the specified columns

                    ("imputer", imputer, numerical_columns),  # Apply imputer to all numeric columns
                ],
                remainder="passthrough"  # Keep the remaining columns as they are
            )

            # Create the pipeline
            processor = Pipeline([("preprocessor", preprocessor)])
            return processor

        except Exception as e:
            raise SrcException(e, sys)

        
    def initiate_data_transformation(self)->DataTransformationArtifact:
        logging.info("Entered initiate_data_transformation method of DataTransformation class")
        try:
            logging.info("Starting data transformation")
            train_df=DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df=DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)

            
            ## training dataframe
            input_feature_train_df=train_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]
            #target_feature_train_df = target_feature_train_df.replace(-1, 0)

            #testing dataframe
            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN]

            input_feature_train_df = input_feature_train_df.drop(columns=['Laundering_type'])
            input_feature_test_df = input_feature_test_df.drop(columns=['Laundering_type'])


            # Convert to datetime
            input_feature_train_df['Time'] = pd.to_datetime(input_feature_train_df['Time'], format='%H:%M:%S')
            input_feature_test_df['Time'] = pd.to_datetime(input_feature_test_df['Time'], format='%H:%M:%S')
            input_feature_train_df['Date'] = pd.to_datetime(input_feature_train_df['Date'], errors='coerce')
            input_feature_test_df['Date'] = pd.to_datetime(input_feature_test_df['Date'], errors='coerce')


            # Extract numeric features
            input_feature_train_df['hour'] = input_feature_train_df['Time'].dt.hour
            input_feature_train_df['minute'] = input_feature_train_df['Time'].dt.minute
            input_feature_train_df['second'] = input_feature_train_df['Time'].dt.second
            input_feature_train_df = input_feature_train_df.drop(columns=['Time' ])

            input_feature_test_df['hour'] = input_feature_test_df['Time'].dt.hour
            input_feature_test_df['minute'] = input_feature_test_df['Time'].dt.minute
            input_feature_test_df['second'] = input_feature_test_df['Time'].dt.second
            input_feature_test_df = input_feature_test_df.drop(columns=['Time'])


            # Extract numeric features from Date
            input_feature_train_df['year'] = input_feature_train_df['Date'].dt.year
            input_feature_train_df['month'] = input_feature_train_df['Date'].dt.month
            input_feature_train_df['day'] = input_feature_train_df['Date'].dt.day
            input_feature_train_df['day_of_week'] = input_feature_train_df['Date'].dt.dayofweek  # Monday=0, Sunday=6
            input_feature_train_df['is_weekend'] = input_feature_train_df['day_of_week'].apply(lambda x: 1 if x >= 5 else 0)
            input_feature_train_df = input_feature_train_df.drop(columns=['Date'])

            input_feature_test_df['year'] = input_feature_test_df['Date'].dt.year
            input_feature_test_df['month'] = input_feature_test_df['Date'].dt.month
            input_feature_test_df['day'] = input_feature_test_df['Date'].dt.day
            input_feature_test_df['day_of_week'] = input_feature_test_df['Date'].dt.dayofweek  # Monday=0, Sunday=6
            input_feature_test_df['is_weekend'] = input_feature_test_df['day_of_week'].apply(lambda x: 1 if x >= 5 else 0)
            input_feature_test_df = input_feature_test_df.drop(columns=['Date'])
            
            input_feature_test_df = input_feature_test_df.astype({col: 'string' for col in input_feature_test_df.select_dtypes(include='object').columns})
            input_feature_train_df = input_feature_train_df.astype({col: 'string' for col in input_feature_train_df.select_dtypes(include='object').columns})

            preprocessor=self.get_data_transformer_object()

            preprocessor_object=preprocessor.fit(input_feature_train_df)
            transformed_input_train_feature=preprocessor_object.transform(input_feature_train_df)
            transformed_input_test_feature =preprocessor_object.transform(input_feature_test_df)
             

            train_arr = np.c_[transformed_input_train_feature, np.array(target_feature_train_df) ]
            test_arr = np.c_[ transformed_input_test_feature, np.array(target_feature_test_df) ]

            #save numpy array data
            save_numpy_array_data( self.data_transformation_config.transformed_train_file_path, array=train_arr, )
            save_numpy_array_data( self.data_transformation_config.transformed_test_file_path,array=test_arr,)
            save_object( self.data_transformation_config.transformed_object_file_path, preprocessor_object,)

            save_object( "final_model/preprocessor.pkl", preprocessor_object,)


            #preparing artifacts

            data_transformation_artifact=DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )
            return data_transformation_artifact


            
        except Exception as e:
            raise SrcException(e,sys)
