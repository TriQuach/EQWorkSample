from Label.label import *
from math import radians, cos, sin, asin, sqrt
import matplotlib.pyplot as plt
from os import listdir
from keras.preprocessing import sequence
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense,Flatten
from keras.layers import LSTM

from keras.optimizers import Adam
from keras.models import load_model
from keras.callbacks import ModelCheckpoint

import numpy as np

def single_pt_haversine(lat, lng, degrees=True):
    """
    'Single-point' Haversine: Calculates the great circle distance
    between a point on Earth and the (0, 0) lat-long coordinate
    """
    r = 6371 # Earth's radius (km). Have r = 3956 if you want miles

    # Convert decimal degrees to radians
    if degrees:
        lat, lng = map(radians, [lat, lng])

    # 'Single-point' Haversine formula
    a = sin(lat/2)**2 + cos(lat) * sin(lng/2)**2
    d = 2 * r * asin(sqrt(a))

    return d


def getHashMapTimeSeries():
    hashMapTimeSeries = {}
    df = labelWithDataFrameForModel()
    df.POI = pd.factorize(df.POI)[0]
    for index, row in df.iterrows():
        value = single_pt_haversine(row['Latitude'], row['Longitude'])
        label = row.POI
        if row['City'] not in hashMapTimeSeries:
            tempObj = {'vals':[value],'label':[label]}
            hashMapTimeSeries[row['City']] = tempObj
        else:
            tempArrVal = hashMapTimeSeries[row['City']]['vals']
            tempArrLabel = hashMapTimeSeries[row['City']]['label']
            tempArrVal.append(value)
            tempArrLabel.append(label)

            hashMapTimeSeries[row['City']]['vals'] = tempArrVal
            hashMapTimeSeries[row['City']]['label'] = tempArrLabel

    return hashMapTimeSeries

def splitDataSet():
    hashMapTimeSeries = getHashMapTimeSeries()
    X = []
    y = []
    for city in hashMapTimeSeries:
        X.append(hashMapTimeSeries[city]['vals'])
        y.append(hashMapTimeSeries[city]['label'])
    return X,y

def create_dataset(dataset, look_back=1):
  dataX, dataY = [], []
  for i in range(len(dataset)-look_back+1):
    a = dataset[i:(i+look_back), :]
    dataX.append(a)
    dataY.append(dataset[i + look_back - 1, :])
  return np.array(dataX), np.array(dataY)


X, y = splitDataSet()


X = np.asarray(X)
X = X.reshape((X.shape[0], 1, 1))
y = np.asarray(y)
y = y.reshape((y.shape[0], 1, 1))

# X = np.ndarray(X)
#
# max_review_length = 500
#
#
# # X = create_dataset(X, look_back = 1)
# # y = create_dataset(y, look_back = 1)
# #
seq_len = 1

model = Sequential()
model.add(LSTM(256, input_shape=(1,1)))

model.add(Dense(1, activation='sigmoid'))

model.summary()

adam = Adam(lr=0.001)
chk = ModelCheckpoint('best_model.pkl', monitor='val_acc', save_best_only=True, mode='max', verbose=1)
model.compile(loss='binary_crossentropy', optimizer=adam, metrics=['accuracy'])
model.fit(X, y, epochs=20, batch_size=128, callbacks=[chk])