import os 
import sys 
import time 
from src.logger import logging
from src.exception import CustomException
from src.components.data_ingestion import DataIngestion
from components.data_transformation import DataTransformation
from components.model_trainer import ModelTrainer
from src.constant import *
from dataclasses import dataclass


@dataclass
class ModelTrainingConfig:
     model_read=os.path.join(artifact,MODEL)


class Training:
     def __init__(self):
          self.modeltrainconfig=ModelTrainingConfig()
          self.data_ingestion=DataIngestion()
          self.data_transformation=DataTransformation()
          self.modeltrain=ModelTrainer()

     def run_pipelines(self):
          try:
               start=time.perf_counter()
               logging.info(f"Model is start at time {start}")
               logging.info("Data Ingestion is start from mongodb")
               file_path=self.data_ingestion.data_Ingestion()
               logging.info("Data is successfully saved into the artifact folder")
               logging.info("Data Transformation is start ")
               X_train_scaled,X_test_scaled,y_train,y_test,X=self.data_transformation.data_transformation(file_path)
               logging.info("Data cleaning is successfully and saved into the artifact ")
               logging.info("Model train is start")
               self.modeltrain.model_train(X_train_scaled,y_train,X=X)
               logging.info("---------Model is train Successfully and lets do predtiction---------")
               end=time.perf_counter()
               logging.info(f"Model is end at {end}")
          except Exception as e:
               logging.error(e)
               raise CustomException(e,sys) from e


