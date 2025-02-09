# -*- coding: utf-8 -*-
"""TweetSentiment.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1tp0kk66FVHX_Rwrz1c23d5Ft6mDhigvx
"""

#INSTALL KAGGLE
!pip install kaggle

#importing the dependencies
import numpy as np
import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

import nltk
nltk.download('stopwords')

#print the stopwrds in eng
print(stopwords.words('english'))

"""data processing"""

#data loading csv-->pandas data frame

twitter_data=pd.read_csv('training.1600000.processed.noemoticon.csv',encoding='ISO-8859-1')

twitter_data

twitter_data.shape

twitter_data.info()

twitter_data.head()

#column naming

column_names=['target','ids','date','flag','user','text']
twitter_data=pd.read_csv('training.1600000.processed.noemoticon.csv',names=column_names,encoding='ISO-8859-1')

twitter_data.shape

twitter_data.head()

#countingmisssingval in ds
twitter_data.isnull().sum()

"""means no value is missing....no need to processing any more"""

#checking the distribution of target column
twitter_data['target'].value_counts()

#convert.target2one
twitter_data.replace({'target':{4:1}}, inplace=True)

twitter_data['target'].value_counts()



"""0----> negative tweet
1----> positive tweet

**stemming**;process of reducing a word to its root word
ex. actor,actress,actig==act
"""

port_stem = PorterStemmer()

def stemming(content):
    stemmed_content = re.sub('[^a-zA-Z]',' ',content)
    stemmed_content = stemmed_content.lower()
    stemmed_content = stemmed_content.split()
    stemmed_content = [port_stem.stem(word) for word in stemmed_content if not word in stopwords.words('english')]
    stemmed_content = ' '.join(stemmed_content)
    return stemmed_content

twitter_data['stemmed_content']=twitter_data['text'].apply(stemming)

twitter_data.head()

print(twitter_data['stemmed_content'])

print(twitter_data['target'])

#separating the data & label
x=twitter_data['stemmed_content'].values
y=twitter_data['target'].values

print(x)

print(y)

"""splitting the data to training data and test data"""

x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,stratify=y,random_state=2)

print(x.shape,x_train.shape,x_test.shape)

print(x_train)

print(x_test)

#CONVERTING THE TEXTUAL DATA TO NUMERICAL DATA

vectorizer = TfidfVectorizer()

x_train = vectorizer.fit_transform(x_train)
x_test = vectorizer.transform(x_test)

print (x_train)

print (x_test)

#Training ML model

model = LogisticRegression(max_iter=1000)

model.fit(x_train,y_train)

"""model Evaluation

accuracy score
"""

#accuracy score on the training data
x_train_prediction = model.predict(x_train)
training_data_accuracy = accuracy_score(y_train,x_train_prediction)

print('Accuracy score of the training data : ', training_data_accuracy)

#accuracy score on the test data
x_test_prediction = model.predict(x_test)
test_data_accuracy = accuracy_score(y_test,x_test_prediction)

print('Accuracy score of the testing data : ', test_data_accuracy)

"""Model accuracy is more than 77 percentage

saving the trained model
"""

import pickle

filename = 'trained_model.sav'
pickle.dump(model,open(filename,'wb'))

#using saved model for future pred
#loading saved model
loaded_model = pickle.load(open('trained_model.sav','rb'))

x_new = x_test[200]
print (y_test[200])

prediction = loaded_model.predict(x_new)
print(prediction)

if prediction[0]==0:
  print('its a negative tweet')
else:
  print('its a positive tweet')

x_new = x_test[3]
print (y_test[3])

prediction = loaded_model.predict(x_new)
print(prediction)

if prediction[0]==0:
  print('its a negative tweet')
else:
  print('its a positive tweet')