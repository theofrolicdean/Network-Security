from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.exception.exception import NetworkException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import *
from networksecurity.entity.artifact_entity import *
from networksecurity.constant import training_pipeline
import sys

if __name__ == "__main__":
    try:
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config=training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
        logging.info("Initiate the data ingestion") 
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        logging.info("Data initiation Completed")
        print(data_ingestion_artifact)
    except Exception as err:
        raise NetworkException(error_message=str(err), error_detail=sys)