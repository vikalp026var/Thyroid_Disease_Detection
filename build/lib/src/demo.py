import os 
import sys 
# import sys
# print(sys.path)
# import sys
sys.path.insert(0, "D:\\Thyroid_Disease_Detection\\src")


# sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# sys.path.insert(0, "D:\Thyroid_Disease_Detection\src")
from dataclasses import dataclass
from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation

obj=DataIngestion()
file_path=obj.data_Ingestion()
obj1=DataTransformation()
obj1.preprocessing_data(file_path)
