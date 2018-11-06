from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.models import Model
from keras.layers import Input,Flatten, Dropout
from sklearn.model_selection import train_test_split
import numpy
from random import randint

# fix random seed for reproducibility
numpy.random.seed(7)
# load pima indians dataset
import csv
def processRaw(csvnam,cursmall):
    with open(csvnam, 'r') as f:
        reader = csv.reader(f)
        your_list = list(reader)
    
    mylist = []
    for x in your_list:
        tlist = []
        count = 1
        for y in x:
            if count == 1:
                y = y[-3:]
                tlist.append(float(y)%100)
                count +=1
            else:
                tlist.append(float(y))
        mylist.append(tlist)
    
    smallcount = 10000
    test = []
    for x in mylist:
        test.append(x[0])
    count = 0
    prevnum = mylist[0][0];
    for num in test:
        if num == prevnum:
            count+= 1
        
        else:
            if count < smallcount:
                smallcount = count
        prevnum = num
    xlist = []
    count = 0
    if cursmall < smallcount:
        smallcount = cursmall
    currnum = mylist[0][0]
    for arr in mylist:
        if arr[0] == currnum and count < smallcount:
            xlist.append(arr[1:])
            count +=1
        elif count == smallcount:
            count +=1
        elif count > smallcount and currnum != arr[0]:
            count = 1
            currnum = arr[0]
            xlist.append(arr[1:])
    #print(xlist)
    X = numpy.asarray(xlist)
    return (X, smallcount)


X_san, sanlowct = processRaw('sanjana_data.csv', 1000000)
X_sar, sarlowct = processRaw('sarah_data.csv', sanlowct)


X = numpy.concatenate((X_san, X_sar), axis = 0)

Y= []
for num in range(1204):
    temp = num%5
    if temp == 0:
        Y.append(numpy.array([1,0,0,0,0]))
    elif temp == 1:
        Y.append(numpy.array([0,1,0,0,0]))
    elif temp == 2:
        Y.append(numpy.array([0,0,1,0,0]))
    elif temp == 3:
        Y.append(numpy.array([0,0,0,1,0]))
    elif temp == 4:
        Y.append(numpy.array([0,0,0,0,1]))


Y=numpy.asarray(Y)
print(Y)
X = X.reshape(1204,32,4)
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.1, random_state=42)
# split into input (X) and output (Y) variables

# create model
model = Sequential()
model.add(LSTM(32, activation='sigmoid', input_shape=(32,4)))

#model.add(LSTM(32, activation = 'relu'))

model.add(Dense(12, activation='relu'))

model.add(Dense(8, activation='relu'))
model.add(Dense(5, activation='softmax'))
# Compile model
model.compile(loss='categorical_crossentropy', optimizer='sgd', metrics=['accuracy'])
# Fit the model
model.summary()
model.fit(X_train, Y_train, epochs=25, batch_size=10, validation_data=(X_test,Y_test))
# evaluate the model
results = model.predict(X_test)
for arr in results:
    idxLarge = 0
    curval = 0
    for val in range(len(arr)):
        if arr[val] >curval:
            idxLarge = val
            curval = arr[val]
    print("The predicted number is: " + str(idxLarge+1) )
scores = model.evaluate(X_test, Y_test)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

