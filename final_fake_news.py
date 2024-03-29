# -*- coding: utf-8 -*-
"""Final fake news.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/18-OzZAwNGyKS-hlAL0nu1_0ro5t9Pep5
"""

# Include Libraries
# make necessary imports

import pandas as pd
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
import pickle
import sqlite3

# Importing dataset using pandas dataframe
# read the data
# reading data files 

df = pd.read_csv("fake_or_real_news.csv")

df.shape
df.shape

# Print first 10 lines of 'df' 

df.head(10)

# distribution of classes for prediction

def create_distribution(dataFile):
    return sb.countplot(x='label', data=dataFile, palette='hls')

# by calling below we can see that training, test and valid data seems to be failry evenly distributed between the classes
create_distribution(df)

# data integrity check (missing label values)
# the dataset does not contains missing values therefore no cleaning required

def data_qualityCheck():
    print("Checking data qualitites...")
    df.isnull().sum()
    df.info()  
    print("check finished.")
data_qualityCheck()

# Separate the labels and set up training and test datasets

# Get the labels
y = df.label
y.head()

# Drop the 'label' column

df.drop("label", axis=1)

# Make training and test sets

#Split the dataset
X_train, X_test, y_train, y_test = train_test_split(df['text'], y, test_size=0.33, random_state=53)

X_train.head(10)

X_test.head(10)

# before we can train an algorithm to classify fake news labels, we need to extract features from it. It means reducing the mass
# of unstructured data into some uniform set of attributes that an algorithm can understand. For fake news detection, it could 
# be word counts (bag of words). 

# we will start with simple bag of words technique 
# Building the Count and Tfidf Vectors

# creating feature vector - document term matrix
# Initialize the 'count_vectorizer'

count_vectorizer = CountVectorizer(stop_words='english')

# Fit and transform the training data 
# Learn the vocabulary dictionary and return term-document matrix

count_train = count_vectorizer.fit_transform(X_train)

print(count_vectorizer)

print(count_train)

# print training doc term matrix
# we have matrix of size of (4244, 56922) by calling below

def get_countVectorizer_stats():
    
    #vocab size
    print(count_train.shape)

    #check vocabulary using below command
    print(count_vectorizer.vocabulary_)

get_countVectorizer_stats()

# Transform the test set

count_test = count_vectorizer.transform(X_test)

# create tf-df frequency features
# tf-idf 
# Initialize a TfidfVectorizer
# Initialize the 'tfidf_vectorizer'
# This removes words which appear in more than 70% of the articles

tfidf_vectorizer = TfidfVectorizer(stop_words='english', max_df=0.7)

# Fit and transform train set, transform test set

# Fit and transform the training data 
tfidf_train = tfidf_vectorizer.fit_transform(X_train)

def get_tfidf_stats():
    tfidf_train.shape
    #get train data feature names 
    print(tfidf_train.A[:10])

get_tfidf_stats()

# Transform the test set 

tfidf_test = tfidf_vectorizer.transform(X_test)

X_test

# get feature names

# Get the feature names of 'tfidf_vectorizer'

print(tfidf_vectorizer.get_feature_names()[-10:])

# Get the feature names of 'count_vectorizer'

print(count_vectorizer.get_feature_names()[:10])

count_df = pd.DataFrame(count_train.A, columns=count_vectorizer.get_feature_names())
tfidf_df = pd.DataFrame(tfidf_train.A, columns=tfidf_vectorizer.get_feature_names())
difference = set(count_df.columns) - set(tfidf_df.columns)
print(difference)

print(count_df.equals(tfidf_df))

print(count_df.head())

print(tfidf_df.head())

# Function to plot the confusion matrix 
# This function prints and plots the confusion matrix
# Normalization can be applied by setting 'normalize=True'

def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j],
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

# building classifier using naive bayes 
# Naive Bayes classifier for Multinomial model

nb_pipeline = Pipeline([
        ('NBTV',tfidf_vectorizer),
        ('nb_clf',MultinomialNB())])

# Fit Naive Bayes classifier according to X, y

nb_pipeline.fit(X_train,y_train)

# Perform classification on an array of test vectors X

predicted_nbt = nb_pipeline.predict(X_test)

score = metrics.accuracy_score(y_test, predicted_nbt)
print(f'Accuracy: {round(score*100,2)}%')

cm = metrics.confusion_matrix(y_test, predicted_nbt, labels=['FAKE', 'REAL'])
plot_confusion_matrix(cm, classes=['FAKE', 'REAL'])

print(cm)

nbc_pipeline = Pipeline([
        ('NBCV',count_vectorizer),
        ('nb_clf',MultinomialNB())])
nbc_pipeline.fit(X_train,y_train)

predicted_nbc = nbc_pipeline.predict(X_test)
score = metrics.accuracy_score(y_test, predicted_nbc)
print(f'Accuracy: {round(score*100,2)}%')

cm1 = metrics.confusion_matrix(y_test, predicted_nbc, labels=['FAKE', 'REAL'])
plot_confusion_matrix(cm1, classes=['FAKE', 'REAL'])

print(cm1)

print(metrics.classification_report(y_test, predicted_nbt))

print(metrics.classification_report(y_test, predicted_nbc))

# building Passive Aggressive Classifier 
# Applying Passive Aggressive Classifier

# Initialize a PassiveAggressiveClassifier
linear_clf = Pipeline([
        ('linear',tfidf_vectorizer),
        ('pa_clf',PassiveAggressiveClassifier(max_iter=50))])
linear_clf.fit(X_train,y_train)

#Predict on the test set and calculate accuracy

pred = linear_clf.predict(X_test)
score = metrics.accuracy_score(y_test, pred)
print(f'Accuracy: {round(score*100,2)}%')

#Build confusion matrix

cm = metrics.confusion_matrix(y_test, pred, labels=['FAKE', 'REAL'])
plot_confusion_matrix(cm, classes=['FAKE', 'REAL'])

print(cm)

print(metrics.classification_report(y_test, pred))

# saving best model to the disk

model_file = 'final_model.sav'
pickle.dump(linear_clf,open(model_file,'wb'))

import sqlite3
conn = sqlite3.connect('test.db',check_same_thread=False)
conn.execute('CREATE TABLE REGISTER (fullname  TEXT,age   INT,Gender  CHAR(50), Username  CHAR(50) Primary Key,Password CHAR(50) NOT NULL,email   TEXT);')
print("table created")

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
conn = sqlite3.connect("C:\Users\dell\OneDrive\Desktop\Final Year Project Code\static\test.db",check_same_thread = False)
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
    app.run()

res = conn.execute("Select * from  REGISTER;");
for row in res:
  print(row);
