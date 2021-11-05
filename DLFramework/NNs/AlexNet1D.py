import keras
import keras.models as models
from keras.layers.convolutional import Conv2D, MaxPooling2D, ZeroPadding2D, Conv1D, MaxPooling1D
from keras.layers.core import Flatten, Dense, Dropout, Activation, Reshape

def AlexNet1D(slice_size=64, num_classes=100):
    
    model = models.Sequential()
    model.add(Conv1D(128,7, activation='relu', padding='same', input_shape=(slice_size, 2)))
    model.add(Conv1D(128,5, activation='relu', padding='same'))
    model.add(MaxPooling1D())
    for i in range(1, 5):
        model.add(Conv1D(128,7, activation='relu', padding='same'))
        model.add(Conv1D(128,5, activation='relu', padding='same'))
        model.add(MaxPooling1D())
    model.add(Flatten())
    model.add(Dense(256, activation='relu'))
    model.add(Dense(128, activation='relu'))
    model.add(Dense(num_classes, activation='softmax'))

    return model
