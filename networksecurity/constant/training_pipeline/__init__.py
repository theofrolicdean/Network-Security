import os
import sys
import numpy as np
import pandas as pd

"""
Defining common constant variable for training pipeline
"""
RANDOM_SEED = 42
REQUIREMENT_FILE_NAME: str = "requirements.txt"
HYPEN_DOT: str = "-e ."
TARGET_COLUMN: str = "Result"
ARTIFACT_DIR: str = "artifacts"
FILE_NAME: str = "Dataset Phising Website.csv"
DATASET_FILE_PATH: str = f"Network_Data/{FILE_NAME}"
TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"
PIPELINE_NAME: str = "NetworkSecurity"
"""
Data Ingestion related constant
"""
DATA_INGESTION_FEATURE_STORE_DIR = "feature_store"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2
