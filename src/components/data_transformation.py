# importing libraries
import numpy as np
import sys
from sklearn.preprocessing import(StandardScaler)
from sklearn.pipeline import Pipeline
from src.logger import logging
from src.exception import CustomException
from src.utils import(save_object,
                      save_numpy_array_data)
from src.entity.artifact_entity import(DataIngestionArtifact,
                                       DataTransformationArtifact)
from src.entity.config_entity import DataTransformationConfig
from src.components.data_ingestion import DataIngestion
from src.constants.training_pipeline import *

"""
creating data_transformation component by using data_ingestion_artifact and
as inputs and model_transformation_artifacts as output
    
"""

class DataTransformation:
    def __init__(self,
                 data_ingestion_artifact:DataIngestionArtifact,
                 data_transformation_config:DataTransformationConfig):
        
        self.data_ingestion_artifact = data_ingestion_artifact
        self.data_transformation_config = data_transformation_config
  
    def get_data_transformation_object(self):        
         try:
            logging.info('Pipeline Initiated')
            # applying standard scaler in a pipeline to scale the values 
            pipeline = Pipeline(
                steps = [
                    ('standard_scaler',StandardScaler())
                ]
            )
            logging.info('Pipeline Completed')
            return pipeline

         except Exception as e:
            logging.info("Error in get_data_transformation_object pipeline creation")
            raise CustomException(e,sys)
         
    @staticmethod
    def converting_variables(data):
        try:
            logging.info("applying square root to bmi and label encoding to some features")
            data['bmi'] = np.sqrt(data['bmi'])

            # label encoding categorical columns(sex,smoker, region)
            data['sex'] = data['sex'].map({'female':0, 'male':1})
            data['smoker'] = data['smoker'].map({'no':0, 'yes':1})
            data['region'] = data['region'].map({'southwest':0,
                                                 'southeast':1,
                                                 'northwest':2,
                                                 'northeast':3 })
            logging.info("converted successfully")
            return data

        except Exception as e:
            logging.info("Error in converting_variables module")
            raise CustomException(e,sys)


    def initiate_data_transformation(self):
        try:
           # Reading train and test data
            train_df = DataIngestion.read_data(self.data_ingestion_artifact.train_filepath)
            test_df = DataIngestion.read_data(self.data_ingestion_artifact.test_filepath)

            logging.info('imported train and test data')
            logging.info(f'Train Dataframe Head : \n{train_df.head().to_string()}')
            logging.info(f'Test Dataframe Head  : \n{test_df.head().to_string()}')

            # applying label encoding and square root transformations
            train_df = DataTransformation.converting_variables(train_df)
            test_df = DataTransformation.converting_variables(test_df)

            ## independent and dependent features
            x_train_df = train_df.drop(TARGET,axis=1)
            y_train_df=train_df[TARGET]
            x_test_df=test_df.drop(TARGET,axis=1)
            y_test_df=test_df[TARGET]
            logging.info('seperated independent and dependent features')

            # preprocessing object
            preprocessing_obj = self.get_data_transformation_object()

            ## apply the transformation for x_train and x_test
            input_feature_train_arr = preprocessing_obj.fit_transform(x_train_df)
            logging.info(f'preprocessing of x_train completed {input_feature_train_arr[1:5,:]}')

            input_feature_test_arr = preprocessing_obj.transform(x_test_df)
            logging.info(f'preprocessing of x_test completed {input_feature_test_arr[1:5,:]}')
            
            # saving numpy array of x_train
            save_numpy_array_data(
                file_path = self.data_transformation_config.x_train_filepath,
                array = input_feature_train_arr
            )

            # saving numpy array of x_test
            save_numpy_array_data(
                file_path = self.data_transformation_config.x_test_filepath,
                array = input_feature_test_arr
            )

            # saving numpy array of y_train
            save_numpy_array_data(
                file_path = self.data_transformation_config.y_train_filepath,
                array = y_train_df
            )

            # saving numpy array of y_test
            save_numpy_array_data(
                file_path = self.data_transformation_config.y_test_filepath,
                array = y_test_df
            )
            logging.info('saved all the numpy array files')

            # saving preprocessor pickle file
            save_object(
                file_path = self.data_transformation_config.preprocessor_filepath,
                obj = preprocessing_obj
            )
            logging.info('saved preprocessor pickle file')

            # saving the artifacts
            data_transformation_artifacts = DataTransformationArtifact(
                x_train_filepath = self.data_transformation_config.x_train_filepath,
                y_train_filepath = self.data_transformation_config.y_train_filepath,
                x_test_filepath = self.data_transformation_config.x_test_filepath,
                y_test_filepath = self.data_transformation_config.y_test_filepath,
                preprocessor_filepath = self.data_transformation_config.preprocessor_filepath
            )

            logging.info('data transformation artifacts created')
            return data_transformation_artifacts
        
        except Exception as e:
            logging.info('error occured in inititate_data_transformation module')
            raise CustomException(e,sys)