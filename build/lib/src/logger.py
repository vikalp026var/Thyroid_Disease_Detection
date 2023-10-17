import logging
import os
import sys 
from datetime import datetime
sys.path.insert(0, "D:\Thyroid_Disease_Detection\src")
# sys.path.append("C:\Thyroid Disease_detection")


file_name=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
log_path=os.path.join(os.getcwd(),'logs',file_name)
os.makedirs(log_path,exist_ok=True)
LOG_FILE_PATH=os.path.join(log_path,file_name)
logging.basicConfig(filename=LOG_FILE_PATH,
                    format="[%(asctime)s]%(lineno)d %(name)s-%(levelname)s -%(message)s",
                    level=logging.INFO)
