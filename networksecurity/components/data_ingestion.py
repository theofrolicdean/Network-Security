from networksecurity.exception.exception import NetworkException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact
from networksecurity.constant import training_pipeline
from typing import List
from sklearn.model_selection import train_test_split
import os
import sys
import numpy as np
import pandas as pd

class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as err:
            raise NetworkException(error_message=str(err), error_detail=sys)
        
    def export_data_as_df(self, path):
        try:
            df = pd.read_csv(path)
            return df
        except Exception as err:
            raise NetworkException(error_message=str(err), error_detail=sys)

    def export_data_into_feature_store(self, df: pd.DataFrame):
        try:
            feature_store_file_path = self.data_ingestion_config.feature_store_path
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)
            df.to_csv(feature_store_file_path, index=False, header=True)
            return df
        except Exception as err:
            raise NetworkException(error_message=str(err), error_detail=sys)
    
    def split_data_as_train_test(self, df: pd.DataFrame):
        try:
            train_df, test_df = train_test_split(
                df, test_size=training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO,
                random_state=training_pipeline.RANDOM_SEED
            )
            logging.info("Performed train test split on the dataframe")
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            print(f"dir Path: {dir_path}")
            os.makedirs(dir_path, exist_ok=True)
            logging.info("Exporting train and test split path")
            train_df.to_csv(
                self.data_ingestion_config.training_file_path, index=False, header=True
            )
            test_df.to_csv(
                self.data_ingestion_config.testing_file_path, index=False, header=True
            )
        except Exception as err:
            raise NetworkException(error_message=str(err), error_detail=sys)

    def initiate_data_ingestion(self):
        try:
            df = self.export_data_as_df(training_pipeline.DATASET_FILE_PATH)
            df = self.export_data_into_feature_store(df)
            self.split_data_as_train_test(df)
            data_ingestion_artifact = DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path
            )
            return data_ingestion_artifact
        except Exception as err:
            raise NetworkException(error_message=str(err), error_detail=sys)
