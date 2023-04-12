import tensorflow as tf
from sklearn.model_selection import train_test_split

import numpy as np


X = np.load("X2.npy")
Y = np.load("Y2.npy")

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2)
y_train, y_test = tf.one_hot(y_train,2),tf.one_hot(y_test,2)


taille = len(X_train[0][0])

from keras.models import Sequential
from keras.layers import Dense, Conv2D, Flatten
#create model
model = Sequential()
#add model layers
model.add(Conv2D(64, kernel_size=3, activation="relu", input_shape=(taille,taille,1)))
model.add(Conv2D(32, kernel_size=3, activation="relu"))
model.add(Flatten())
model.add(Dense(4, activation="softmax"))


model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=3)