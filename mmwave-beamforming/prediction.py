import argparse
import pickle
import numpy as np
import sys
import csv
import os
import glob

import keras
from keras.models import Sequential
from keras.layers import Input, Conv2D, MaxPooling2D, Dropout, Flatten, Dense, Activation
from keras import backend as K
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.layers.normalization import BatchNormalization
from keras.optimizers import Adam
from keras.models import Model
from keras.callbacks import ModelCheckpoint
from keras.models import model_from_json


from sklearn.preprocessing import MultiLabelBinarizer

from PIL import Image
from  more_itertools import unique_everseen
from random import randrange
from time import time


def labels_to_categorical(labels):
    """
    Convert nominal labels to categorical
    This function assigns labels to each beam vector tuple, [(0, (14, 14)), (1, (16, 14)), (2, (18, 16)),..., (15, (12, 24)), (16, (12, 0)), (17, (8, 10))]
    The mapping is then used to labelize the dataset, and the mapped values(integers) are fed to to_catogerical function
    """
    dis=list(unique_everseen(labels))
    mapping=[(dis.index(element),element) for element in dis]

    indexing=[]
    for l in labels:
      for m in mapping:
        if m[1]==l:
          indexing.append((m[0],l))

    mapped=[c[0] for c in indexing]

    categorical_labels = keras.utils.to_categorical(mapped)
    return categorical_labels,mapping


################################################################
def get_2d_models(height, width, classes=2, lr=0.001):
    """
    Create original classification model
    """

    model = Sequential()
    inputShape = (height, width, 1)
    # first set of CONV => RELU => POOL layers
    model.add(Conv2D(10, (10,10), padding="same", input_shape=inputShape))
    model.add(Activation("relu"))
    model.add(MaxPooling2D(pool_size=(3, 3),strides=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(128))
    model.add(Activation("relu"))
    model.add(Dropout(0.5))

    model.add(Dense(classes))
    model.add(Activation("softmax"))

    # return the constructed network architecture
    model.compile(loss=keras.losses.categorical_crossentropy,
                  optimizer=keras.optimizers.adam(lr=lr),
                  metrics=['accuracy'])

    return model
################################################################




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'mmwave framework',formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--id_gpu', default=0, type=int, help='which gpu to use.')

    parser.add_argument('-bs', '--batch_size', type=int, default=10,help='Batch size')
    parser.add_argument('--epochs', type=int, default=5,help='Number of epochs')
    parser.add_argument('--lr', type=float, default=1e-4,help='Number of epochs')

    args = parser.parse_args()

    if args.id_gpu >= 0:
        os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
        # The GPU id to use
        os.environ["CUDA_VISIBLE_DEVICES"] = str(args.id_gpu)

##################################################################Binary Classifier of Wall
    with open('npy_label.pkl','rb') as handle:
        data = pickle.load(handle)

    all_label = [ytrain[1] for ytrain in data]
    categorical_labels, mapping_scheme = labels_to_categorical(all_label)
    x = np.asarray([np.load(x[0]) for x in data])

    print("There are total {} samples and {} labels".format(x.shape,categorical_labels.shape))
##################################################################split to train test
    x_train = x[:int(0.8*x.shape[0])]
    y_train = categorical_labels[:int(0.8*x.shape[0])]


    x_test = x[int(0.8*x.shape[0]):]
    y_test = categorical_labels[int(0.8*x.shape[0]):]

    print("Training set:{},{} Testing set : {},{}".format(x_train.shape,y_train.shape,x_test.shape,y_test.shape))


    model  = get_2d_models(x_train.shape[1], x_train.shape[2], classes=18, lr=args.lr)
    model.summary()

    x_train = x_train.reshape((x_train.shape[0], x_train.shape[1], x_train.shape[2], 1))
    x_test = x_test.reshape((x_test.shape[0], x_test.shape[1], x_test.shape[2], 1))

    history = model.fit(x_train,
              y_train,
              batch_size=args.batch_size,
              epochs=args.epochs,
              verbose=1)

    print(history.history.keys())
    print(history.history['acc'])
    print(history.history['loss'])

    start = time()
    testing_accuracy = model.evaluate(x_test,y_test,verbose=0)
    print("test{}".format(testing_accuracy))
    end = time()
    time_per = (end-start)/len(x_test)
    print("Evaluation time is:",time_per)

