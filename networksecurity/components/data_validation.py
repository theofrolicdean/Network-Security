from networksecurity.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.exception.exception import NetworkException
from networksecurity.logging.logger import logging
from networksecurity.utils.main_utils.utils import read_yaml_file, write_yaml_file
from networksecurity.constant.training_pipeline import SCHEMA_FILE_PATH
from scipy.stats import ks_2samp
import sys
import pandas as pd
import os   

class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact,
                 data_validation_config: DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as err:
            raise NetworkException(error_message=str(err), error_detail=sys)
        
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            df = pd.read_csv(file_path)
            return df
        except Exception as err:
            raise NetworkException(error_message=str(err), error_detail=sys)
    
    def detect_dataset_drift(self, base_df: pd.DataFrame, current_df: pd.DataFrame,
                             threshold: float = 0.05) -> dict:
        try: 
            report = {}

            for column in base_df.columns:
                df_1 = base_df[column]
                df_2 = current_df[column]
                is_same_dist = ks_2samp(df_1, df_2)
                is_found = is_same_dist.pvalue > threshold
                status = not is_found
                report.update({
                    "p_value": float(is_same_dist.pvalue),
                    "drift_status": status   
                })

            drift_report_file_path = self.data_validation_config.drift_report_path
            dir_path = os.path.dirname(drift_report_file_path)
            print(f"Directory drift report path: {dir_path}")
            os.makedirs(dir_path, exist_ok=True)
            print("drift_report_file_path: ", drift_report_file_path)
            write_yaml_file(file_path=drift_report_file_path, content=report)
            
        except Exception as err:    
            raise NetworkException(error_message=str(err), error_detail=sys)

    def validate_number_of_cols(self, df: pd.DataFrame) -> bool:
        try:
            print(f"Schema config: {self._schema_config}")
            number_of_cols = len(self._schema_config)
            logging.info(f"Total number of columns is {number_of_cols}")
            logging.info(f"Data frame has {len(df.columns)} columns")
            return len(df.columns) == number_of_cols
        except Exception as err:
            raise NetworkException(error_message=str(err), error_detail=sys)

    def initiate_data_validation(self):
        try:
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path
            train_df = DataValidation.read_data(train_file_path)
            test_df = DataValidation.read_data(test_file_path)
            train_df.name = "Train Dataframe"
            test_df.name = "Test Dataframe"
            
            # Validate number of columns
            for df in [train_df, test_df]:
                status = self.validate_number_of_cols(train_df)
                if not status:
                    print(f"{df.name} doesn't contain all columns")
            
            # Check data drift
            status = self.detect_dataset_drift(base_df=train_df, current_df=test_df)
            dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path, exist_ok=True)

            train_df.to_csv(
                self.data_validation_config.valid_train_file_path, index=False, 
                header=True
            )
            test_df.to_csv(
                self.data_validation_config.valid_test_file_path, index=False,
                header=True
            )

            data_validaton_artifact =DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_ingestion_artifact.trained_file_path,
                valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_path,
            )

            return data_validaton_artifact

        except Exception as err:
            raise NetworkException(error_message=str(err), error_detail=sys)

