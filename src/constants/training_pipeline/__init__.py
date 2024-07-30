import os


"""
    Data Ingestion constants

""" 

# folder to store artifacts
ARTIFACT_DIR:str = 'artifacts'
DATA_INGESTION_DIR_NAME :str = "Data_Ingestion"

ORIGINAL_DATA_FILENAME:str = "insurance.csv"
TRAIN_FILE_NAME:str = "train.csv"
TEST_FILE_NAME:str = "test.csv"

TRAIN_TEST_SPLIT_RATIO:float = 0.25
RANDOM_STATE:int = 0


"""
    Data Transformation constants

"""

DATA_TRANSFORMATION_DIR_NAME:str = "Data_Transformation"
TRAIN_DIR_NAME:str = "Train"
TEST_DIR_NAME:str = "Test"

X_TRAIN_FILE_PATH:str = "x_train.npy"
Y_TRAIN_FILE_PATH:str = "y_train.npy"
X_TEST_FILE_PATH:str = "x_test.npy"
Y_TEST_FILE_PATH:str = "y_test.npy"

PREPROCESSOR_FILE_PATH:str = "preprocessor.pkl"
TARGET:str = 'expenses'

"""
    Model training constants

"""

MODEL_TRAINING_DIR_NAME:str = "Model_training"
MODEL_FILE_PATH:str = "model.pkl"

CRITERION = 'squared_error'
LEARNING_RATE = 0.05
MAX_DEPTH = 3
N_ESTIMATORS = 100

"""
    Model Evaluation constants

"""

MODEL_EVALUATION_DIR_NAME:str = "Model_Evaluation"
MODEL_EVALUATION_REPORT_FILEPATH:str = "evaluation_report.json"