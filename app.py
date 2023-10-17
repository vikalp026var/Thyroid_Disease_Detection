from flask import Flask, jsonify,request,app,render_template
import pickle
from src.pipelines.training_pipelines import Training
from src.pipelines.prediction_pipelines import PredictionPipeline
import sys 


app=Flask(__name__)

@app.route('/')
def welcome():
     return render_template('index.html')

@app.route('/train')
def train():
     try:
          obj=Training()
          obj.run_pipelines()
          return render_template('index.html')
     except Exception as e:
          raise e
     
@app.route('/predict',methods=['GET','POST'])
def predict():
     try:
          obj1=PredictionPipeline()
          result=obj1.run_pipeline()
          return render_template('result.html',result=result)
     except Exception as e:
          raise e
     



if __name__=='__main__':
     app.run(debug=True,port=8080)
