import os
import sys
# sys.path.append("C:\Thyroid Disease_detection")
sys.path.insert(0, "D:\Thyroid_Disease_Detection\src")
from src.logger import logging
from src.exception import CustomException
from tensorflow.keras.models import load_model as tf_load_model
import pickle
from src.constant import *


class MainUtilsConfig:

    artifact = os.path.join(artifact)


class MainUtils:
    def __init__(self):
        self.mainutils = MainUtilsConfig()

    @staticmethod
    def save_model(file_path, model):
        try:
            logging.info("Enter into the save model method")
            model.save(file_path) 
            logging.info("Model has been saved successfully")
        except Exception as e:
            logging.error(e)
            raise CustomException(e, sys) from e

    @staticmethod
    def load_model(file_path):
        try:
            logging.info("Enter into the load model method of utils")
            model = tf_load_model(file_path)  
            logging.info("Exit from the load model method of utils")
            return model
        except Exception as e:
            logging.error(e)
            raise CustomException(e, sys) from e
    
    @staticmethod
    def save_pickle(file_path,object):
        try:
            logging.info("Enter into the save pickle file ")
            with open(file_path,'wb') as file:
                pickle.dump(object,file)
            logging.info("Save the object")
        except Exception as e:
            logging.error(e)
            raise CustomException(e,sys) from e
        
    @staticmethod
    def load_pickle(file_path):
        try:
            logging.info("Enter into the load pickle method")
            with open(file_path,'rb') as file:
                model=pickle.load(file)
            logging.info("Successfully load the model ")
            return model
        except Exception as e:
            logging.error(e)
            raise CustomException(e,sys) from e
        
