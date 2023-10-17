import os 
import sys 
sys.path.insert(0, "D:\Thyroid_Disease_Detection\src")
import pandas as pd 
from src.logger import logging
from src.exception import CustomException
from src.constant import * 
from src.utils import MainUtils
import pymongo
from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
     artifact=os.path.join(artifact)
     data=os.path.join(DATASET)

class DataIngestion:
     def __init__(self):
          self.utils=MainUtils()
          self.dataingestionconfig=DataIngestionConfig()

     def collections(self):
          try:
               logging.info("Enter into the collections")
               client=pymongo.MongoClient(MONGODB_URL)
               db=client[MONGODB_DB_NAME]
               collections=db[MONGODB_COLLECTION_NAME]
               logging.info(f"Collections name is {collections} we are at exit point of collections")
               return collections
          except Exception as e:
               logging.error(e)
               raise CustomException(e,sys) from e
     def dataset_read(self):
          try:
               logging.info("Enter into the dataset read")
               collections=self.collections()
               data=collections.find({})
               df=pd.DataFrame(data)
               df.drop(columns=['_id'],axis=1,inplace=True)
               logging.info("Exit from datasetread from MongoDB ")
               return df
          except Exception as e:
               logging.error(e)
               raise CustomException(e,sys) from e
     
     def save_dataset(self):
          try:
               logging.info("Enter into the save dataset ")
               df=self.dataset_read()
               os.makedirs(self.dataingestionconfig.artifact,exist_ok=True)
               raw_path=os.path.join(self.dataingestionconfig.artifact,self.dataingestionconfig.data)
               df.to_csv(raw_path,index=False)
               logging.info(f"Successfuly save into the artifact folder into {raw_path}")
               return raw_path
          except Exception as e:
               logging.error(e)
               raise CustomException(e,sys) from e
          
     def data_Ingestion(self):
          try:
               logging.info("Enter into the data ingestion method")
               file_path=self.save_dataset()
               logging.info("Exit from the data ingestion method of Data Ingestion ")
               return file_path
          except Exception as e:
               logging.error(e)
               raise CustomException(e,sys) from e
          

     


