import os
import sys
from src.logger import logging
import pandas as pd
from src.exception import CustomException
from src.utils import MainUtils
from src.constant import *
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.models import Sequential
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from dataclasses import dataclass

@dataclass
class ModelTrainConfig:
    model_path = os.path.join(artifact, MODEL)

class ModelTrainer:
    def __init__(self):
        self.modeltrainconfig = ModelTrainConfig()
        self.utils = MainUtils()

    def model_architecture(self,X):
        try:
            logging.info("Model architecture is defined")
            model = Sequential()
            model.add(Dense(256, input_shape=[X.shape[1]], activation='relu'))
            model.add(Dropout(0.4))
            model.add(Dense(128, activation='relu'))
            model.add(Dropout(0.3))
            model.add(Dense(63, activation='relu'))
            model.add(Dropout(0.2))
            model.add(Dense(1,activation='sigmoid'))
            model.summary()
            logging.info("Architecture has been successfully defined")
            LOSS='binary_crossentropy'
            OPTIMIZER='Adam'
            METRICS=['accuracy']

            model.compile(loss=LOSS, optimizer=OPTIMIZER, metrics=METRICS)
            self.utils.save_model(self.modeltrainconfig.model_path, model)
            return self.modeltrainconfig.model_path
        except Exception as e:
            logging.error(e)
            raise CustomException(str(e)) from e  # Modified this line for CustomException

    def fit_model(self, X_train, y_train,X):
        try:
            logging.info("Enter into the fit of model")
            model_path = self.model_architecture(X)
            logging.info("Safely load the model")
            model = self.utils.load_model(model_path)
            history = model.fit(X_train, y_train, epochs=100, 
                                callbacks=[EarlyStopping(verbose=1, patience=50), ModelCheckpoint('Thyroid.h5')],
                                batch_size=64, validation_split=0.1)
            info = pd.DataFrame(history.history)
            path = os.path.join(artifact, 'model_history.csv')
            info.to_csv(path, index=False)
            self.utils.save_model(model_path,model)
        except Exception as e:
            logging.error(e)
            raise CustomException(str(e)) from e

    def model_train(self, X_train, y_train,X):
        try:
            logging.info("Enter into the model train")
            self.fit_model(X_train=X_train, y_train=y_train,X=X)
            logging.info("Exit from model train")
        except Exception as e:
            logging.error(e)
            raise CustomException(str(e)) from e
