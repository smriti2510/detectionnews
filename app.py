import pickle
import pandas as pd
from flask import Flask
from flask import request, jsonify, Flask,render_template
import random as r
import sqlite3
# Include Libraries
# make necessary imports
from sklearn.model_selection import train_test_split
import sklearn
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
from sklearn.pipeline import Pipeline
from sklearn.metrics import confusion_matrix
from matplotlib import pyplot as plt
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.model_selection import KFold
import itertools
import numpy as np

app = Flask(__name__)
conn = sqlite3.connect("static/test.db",check_same_thread = False)
app.config['CORS_HEADERS'] = 'Content-Type'
load_model = pickle.load(open('final_model.sav', 'rb'))
var1= False

@app.route("/")
def home():
  #text =  request.args['news'];
  return render_template("index.html")

@app.route("/prediction")
def prediction():
    return render_template("prediction.html")

@app.route("/predict",methods=['GET','POST'])
def detecting_fake_news():
    text = request.args.get('news')
    prediction = load_model.predict([text])
    return(prediction[0])
    #return render_template("prediction.html",prediction_text=prediction[0])

@app.route("/contact",methods=['GET','POST'])
def contact():
    return render_template("contact.html")

@app.route("/sign",methods=['GET','POST'])
def sign():
    return render_template("signup.html")

@app.route("/reg",methods=['GET','POST'])
def reg():
    return render_template("register.html")

# function to run for prediction
@app.route("/register",methods=['GET','POST'])
def register():
  fullname =  request.args['name'];
  age =  request.args['age'];
  Gender =  request.args['gender'];
  Username =  request.args['username'];
  Password =  request.args['password'];
  email =  request.args['email'];
  try:
    result = conn.execute("INSERT INTO REGISTER VALUES('"+fullname+"',"+age+",'"+Gender+"','"+Username+"','"+Password+"','"+email+"');")
    print(result);
    return ("Registered Succesfully");
  except :
    return ("Username already exists");

@app.route("/signup",methods=['GET','POST'])
def signup():
  Username = request.args['username'];
  Password = request.args['password'];
  cursor = conn.execute("SELECT * from REGISTER where Username ='"+Username+"'and Password ='"+Password+"';");
  for row in cursor:
    print(row);
    return ("Successfully logged in")
  else:
    return("Invalid Username or Password")
 

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')
