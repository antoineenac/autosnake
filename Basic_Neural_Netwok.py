import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix,accuracy_score
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout


#Opening of the database
Xs = np.load("X_nn.npy", allow_pickle = True)
Ys = np.load("Y.npy", allow_pickle = True)


#Creation of the database we are going to use
X,Y = [],[]
for k in range(len(Xs)):
	X = X+Xs[k]
	Y = Y+Ys[k]
	
Y_ovh = []
for y in Y:
	if y=="z":
		Y_ovh.append([1,0,0,0])
	if y=="s":
		Y_ovh.append([0,1,0,0])
	if y=="q":
		Y_ovh.append([0,0,1,0])
	if y=="d":
		Y_ovh.append([0,0,0,1])
		

#Train/test split
X_train, X_test, y_train, y_test = train_test_split(X,Y,test_size=0.2)


Y_train_ovh = []
for y in y_train:
	if y=="z":
		Y_train_ovh.append([1,0,0,0])
	if y=="s":
		Y_train_ovh.append([0,1,0,0])
	if y=="q":
		Y_train_ovh.append([0,0,1,0])
	if y=="d":
		Y_train_ovh.append([0,0,0,1])
		
Y_test_ovh = []
for y in y_test:
	if y=="z":
		Y_test_ovh.append([1,0,0,0])
	if y=="s":
		Y_test_ovh.append([0,1,0,0])
	if y=="q":
		Y_test_ovh.append([0,0,1,0])
	if y=="d":
		Y_test_ovh.append([0,0,0,1])

X_train, X_test, Y_train_ovh, Y_test_ovh = np.array(X_train), np.array(X_test), np.array(Y_train_ovh), np.array(Y_test_ovh)
#Model definition
def model():
    model = Sequential()
    model.add(Dense(12, activation='relu'))
    model.add(Dense(6, activation = 'sigmoid'))
    model.add(Dense(4, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

model = model()
model.fit(X_train,Y_train_ovh, epochs = 20, batch_size = 32, validation_split=0.2)

print(model.summary())

preds = model.predict(X_test)

classes_pred = []
for p in preds:
	p = list(p)
	m = p.index(max(p))
	if m==0:
		classes_pred.append("z")
	if m==1:
		classes_pred.append("s")
	if m==2:
		classes_pred.append("q")
	if m==3:
		classes_pred.append("d")
		
a = accuracy_score(classes_pred,y_test)
print('Accuracy is:', a*100)

from sklearn.metrics import multilabel_confusion_matrix
print(confusion_matrix(y_test, classes_pred))
		
