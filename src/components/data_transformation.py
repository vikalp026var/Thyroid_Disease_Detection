import os 
import sys
sys.path.insert(0, "D:\Thyroid_Disease_Detection\src")
import pandas as pd 

from src.logger import logging
from src.exception import CustomException
from constant import *
from components.data_ingestion import DataIngestion
from utils import MainUtils
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
              new_columns = { 
    'on thyroxine':'on_thyroxine',
    'query on thyroxine':'query_on_thyroxine',
    'on antithyroid medication':'on_antithyroid_medication',
    'thyroid surgery':'thyroid_surgery',
    'I131 treatment':'I131_treatment',
    'query hypothyroid':'query_hypothyroid',
    'query hyperthyroid':'query_hyperthyroid',
    'TSH measured':'TSH_measured',
    'T3 measured':'T3_measured',
    'TT4 measured':'TT4_measured',
    'T4U measured':'T4U_measured',
    'FTI measured':'FTI_measured',
    'TBG measured':'TBG_measured', 
}

# Rename the columns directly
              df.columns = [new_columns.get(col, col) for col in df.columns]
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
              df['T4U_measured'].fillna(df['T4U_measured'].mean(),inplace=True)
              cols=['TSH','T3','TT4','T4U','FTI']
              S=SimpleImputer(strategy='mean')
              for i in cols:
                   df[i]=S.fit_transform(df[[i]])
              logging.info("We get the clean data and save into artifact ")
              clean_data=df
              clean_data.to_csv(self.datatransformationconfig.clean_data,index=False)
              logging.info("Save the clean the data")
              return clean_data
          except Exception as e:
               logging.error(e)
               raise CustomException(e,sys) from e
     


     def train_test_split(self,file_path):
          try:
               logging.info("Enter into the train test split ")
               df=self.preprocessing_data(file_path)
               X=df.iloc[:,:-1]
               y=df.iloc[:,-1]
               X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.33,random_state=42)
               logging.info("Exit from the train test split ")
               return X_train,X_test,y_train,y_test,X
          except Exception as e:
               logging.error(e)
               raise CustomException(e,sys) from e



     def standard_scale(self,file_path):
          try:
               logging.info("Enter into the scale the data ")
               X_train,X_test,y_train,y_test,X=self.train_test_split(file_path)
               scale=StandardScaler()
               X_train_scaled=scale.fit_transform(X_train)
               X_test_scaled=scale.transform(X_test)
               self.utils.save_pickle(self.datatransformationconfig.save_model,scale)
               logging.info('Exit from the scale method and the save the scale into artifact')
               return X_train_scaled,X_test_scaled,y_train,y_test,X
          except Exception as e:
               logging.error(e)
               raise CustomException(e,sys) from e
          



     def data_transformation(self,file_path):
          try:
               logging.info("Enter into the data transformation")
               X_train_scaled,X_test_scaled,y_train,y_test,X=self.standard_scale(file_path)
               logging.info("Successfully run the data transformation file")
               return X_train_scaled,X_test_scaled,y_train,y_test,X
          except Exception as e:
               logging.error(e)
               raise CustomException(e,sys) from e
          

               
              