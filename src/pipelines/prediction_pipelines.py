import os
import sys
from flask import Flask, request
from src.logger import logging
from src.exception import CustomException
from src.constant import *
from utils import MainUtils
from dataclasses import dataclass

@dataclass
class PredictionConfig:
    read_file_path = os.path.join(artifact, MODEL)
    scale_path = os.path.join(artifact, 'scale.pkl')

class PredictionPipeline:
    def __init__(self):
        self.prediction = PredictionConfig()
        self.utils = MainUtils()

    def read_file(self):
        try:
            if request.method == 'POST':
                model = self.utils.load_model(file_path=self.prediction.read_file_path)
                age= float(request.form.get('age'))
                sex = 1 if request.form.get('sex') == 'M' else 0
                on_thyroxine = request.form.get('on_thyroxine')
                query_on_thyroxine = request.form.get('query_on_thyroxine')
                on_antithyroid_medication = request.form.get('on_antithyroid_medication')
                sick = request.form.get('sick')
                pregnant = request.form.get('pregnant')
                thyroid_surgery = request.form.get('thyroid_surgery')
                I131_treatment = request.form.get('I131_treatment')
                query_hypothyroid = request.form.get('query_hypothyroid')
                query_hyperthyroid = request.form.get('query_hyperthyroid')
                lithium = request.form.get('lithium')
                goitre = request.form.get('goitre')
                tumor = request.form.get('tumor')
                hypopituitary = request.form.get('hypopituitary')
                psych = request.form.get('psych')
                TSH_measured = request.form.get('TSH_measured')
                TSH = float(request.form.get('TSH'))
                T3_measured = request.form.get('T3_measured')
                T3 = float(request.form.get('T3'))
                TT4_measured = request.form.get('TT4_measured')
                TT4 = float(request.form.get('TT4'))
                T4U_measured = request.form.get('T4U_measured')
                T4U = float(request.form.get('T4U'))
                FTI_measured = request.form.get('FTI_measured')
                FTI = float(request.form.get('FTI'))
                TBG_measured = request.form.get('TBG_measured')

#             input_data = {
#     'age': 35,
#     'sex': 'M',
#     'on_thyroxine': 'f',
#     'query_on_thyroxine': 'f',
#     'on_antithyroid_medication': 'f',
#     'sick': 'f',
#     'pregnant': 'f',
#     'thyroid_surgery': 'f',
#     'I131_treatment': 'f',
#     'query_hypothyroid': 'f',
#     'query_hyperthyroid': 'f',
#     'lithium': 'f',
#     'goitre': 'f',
#     'tumor': 'f',
#     'hypopituitary': 'f',
#     'psych': 'f',
#     'TSH_measured': 't',
#     'TSH': 1.5,
#     'T3_measured': 't',
#     'T3': 2.0,
#     'TT4_measured': 't',
#     'TT4': 100,
#     'T4U_measured': 't',
#     'T4U': 0.8,
#     'FTI_measured': 't',
#     'FTI': 120,
#     'TBG_measured': 't'
# }

                

                numerical_cols = ['age', 'TSH', 'T3', 'TT4', 'T4U', 'FTI']
                scale = self.utils.load_pickle(self.prediction.scale_path)
                y_pred=model.predict(scale.transform([[age, sex, on_thyroxine, query_on_thyroxine,
       on_antithyroid_medication, sick, pregnant, thyroid_surgery,
       I131_treatment, query_hypothyroid, query_hyperthyroid, lithium,
       goitre, tumor, hypopituitary, psych, TSH_measured, TSH,
       T3_measured, T3, TT4_measured, TT4, T4U_measured, T4U,
       FTI_measured, FTI, TBG_measured]]))

                

                if y_pred[0][0] == 1:
                    return "Positive"
                else:
                    return  "Negative"
        except Exception as e:
            logging.error(e)
            raise CustomException(e, sys) from e

    def run_pipeline(self):
        try:
            logging.info("Enter into the Prediction now Prediction is too bee start.... ")
            result=self.read_file()
            logging.info("Prediction is now Complete ",result)
            return result
        except Exception as e:
            logging.error(e)
            raise CustomException(e,sys) from e
        