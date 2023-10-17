import os 
import sys
sys.path.insert(0, "D:\Thyroid_Disease_Detection\src")
import pandas as pd 

from src.logger import logging
from src.exception import CustomException
from src.constant import *
from src.components.data_ingestion import DataIngestion
from src.utils import MainUtils
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from dataclasses import dataclass


@dataclass
class DataTransformationConfig:
     clean_data=os.path.join(artifact,'clean_data.csv')
     train_data=os.path.join(artifact,'train_data.csv')
     test_data=os.path.join(artifact,'test_data.csv')
     save_model=os.path.join(artifact,'scale.pkl')


class DataTransformation:
     def __init__(self):
          self.datatransformationconfig=DataTransformationConfig()
          self.utils=MainUtils()


     def read_data(self,file_path):
          try: 
               logging.info("Enter into read data of data transformation")
               df=pd.read_csv(file_path)
               logging.info("Successfully read the data artifact\hypothyroid.csv")
               return df
          except Exception as e:
               logging.error(e)
               raise CustomException(e,sys) from e
          

     def preprocessing_data(self,file_path):
          try:
              logging.info("Cleaning process of data is start ...")
              df=self.read_data(file_path=file_path)
              df['binaryClass']=df['binaryClass'].map({'P':'1','N':'0'})
              df=df.replace({'t':'1','f':'0'})
              df.drop(columns=['referral source'],inplace=True)
              del df['TBG']
              df['sex']=df['sex'].map({'M':'1','F':'0'})
              cols=df.columns[df.dtypes.eq('object')]
              df[cols]=df[cols].apply(pd.to_numeric,errors='coerce')
              logging.info("After some clean the data now start the fill the missing value")
              df['sex'].fillna(df['sex'].mean(),inplace=True)
              df['age'].fillna(df['age'].mean(),inplace=True)
              df['T4U measured'].fillna(df['T4U measured'].mean(),inplace=True)
              cols=['TSH','T3','TT4','T4U','FTI']
              S=SimpleImputer(strategy='mean')
              for i in cols:
                   df[i]=S.fit_transform(df[[i]])
              logging.info("We get the clean data and save into artifact ")
              clean_data=df
              clean_data.to_csv(self.datatransformationconfig.clean_data,index=False)
              logging.info("Save the clean the data")
          #     return clean_data
          except Exception as e:
               logging.error(e)
               raise CustomException(e,sys) from e
          
              