import os
import numpy as np
import pickle
import random

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

from PIL import Image
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import ImageDataGenerator
import time
from collections import Counter
from create_crops_of_Entire_Image import create_crops_of_entire_Image


def show_all_files_in_directory(input_path):
    'This function reads the path of all files in directory input_path'
    files_list=[]
    for path, subdirs, files in os.walk(input_path):
        for file in files:
            if file.endswith(".JPG"):
               files_list.append(os.path.join(path, file))
    return files_list



def check_and_create(dir_path):
    if os.path.exists(dir_path):
        return True
    else:
        os.makedirs(dir_path)
        return False




def get_models(model_flag = 'Wall', inputshape=(50,50,3), classes=3, lr=0.001):
    """
    Create original classification model
    """

    model = Sequential()
    # first set of CONV => RELU => POOL layers
    model.add(Conv2D(50, (20,20), padding="same",
        input_shape=inputshape))
    model.add(Activation("relu"))
    model.add(MaxPooling2D(pool_size=(3, 3),strides=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(128))
    model.add(Activation("relu"))
    model.add(Dropout(0.5))

    model.add(Dense(classes))
    model.add(Activation("softmax"))

    return model



def Load_Entire_Image(Entire_Image_path):

    All_jpg = show_all_files_in_directory(Entire_Image_path)
    path_label = []

    for i in All_jpg:
        path = i
        label1 = i.split('/')[-3].split('-')[2]
        label2 = i.split('/')[-3].split('-')[3]
        path_label.append((path,(label1,label2)))

    return path_label



class TrainTest():
    def __init__(self, base_path = '/home/batool/Directroy/', save_path = '/home/batool/Directroy/'):

        self.model = None
        self.base_path = base_path
        self.save_path = save_path

    def add_model(self, classes, model_flag, model, model_path='/home/batool/Directroy/Wall/model/'):

        self.model = model
        self.classes = classes
        model_json = self.model.to_json()
        print('\n*************** Saving New Model Structure ***************')
        with open(os.path.join(model_path, "%s_model.json" % model_flag), "w") as json_file:
            json_file.write(model_json)
            print("json file written")


    # loading the model structure from json file
    def load_model_structure(self, classes, model_path='/home/batool/per_batch/Wall/model/homegrown_model.json'):

        # reading model from json file
        json_file = open(model_path, 'r')
        model = model_from_json(json_file.read())
        json_file.close()

        self.model = model
        self.classes = classes

        return model


    def load_weights(self, weight_path = '/home/batool/per_batch/Wall/model/weights.02-3.05.hdf5'):

        self.model.load_weights(weight_path)



    def train_model(self, batch_size, data_path='/home/batool/Directroy/data' , window=50, lr=0.002, epochs=10, wall_model_path = '/home/batool/Directroy/Wall/model/'):
        # Train
        # Create an Image Datagenerator model, and normalize
        traingen = ImageDataGenerator(rescale=1./255, brightness_range=[0.5,1.5])
        train_generator = traingen.flow_from_directory(data_path+'/train/', target_size=(window, window), color_mode="rgb", batch_size=batch_size, class_mode='categorical', shuffle=True)

        batchX, batchy = train_generator.next()
        print('Batch shape=%s, min=%.3f, max=%.3f' % (batchX.shape, batchX.min(), batchX.max()))


        STEP_SIZE_TRAIN = train_generator.n//train_generator.batch_size

        # Validation
        # Create an Image Datagenerator model, and normalize
        valgen = ImageDataGenerator(rescale=1./255, brightness_range=[0.5,1.5])
        validation_generator = valgen.flow_from_directory(data_path+'/validation/', target_size=(window, window), color_mode="rgb", batch_size=batch_size, class_mode='categorical', shuffle=True)

        STEP_SIZE_Validation = validation_generator.n//validation_generator.batch_size


        self.model.compile(loss=keras.losses.categorical_crossentropy, optimizer=Adam(lr=lr), metrics=['accuracy'])
        print('*******************Saving model weights****************')
        self.model.fit_generator(train_generator, steps_per_epoch=STEP_SIZE_TRAIN, validation_data = validation_generator, validation_steps=STEP_SIZE_Validation, epochs=epochs )

        self.model.save_weights(wall_model_path+"wall_model_weights.hdf5")

    def test_model(self, batch_size, data_path='/home/batool/Directroy/data' , window=50, lr=0.002, epochs=10, wall_model_path = '/home/batool/Directroy/Wall/model/'):

        testgen = ImageDataGenerator(rescale=1./255, brightness_range=[0.5,1.5])
        test_generator = testgen.flow_from_directory(data_path+'/test/', target_size=(window, window), color_mode="rgb", batch_size=batch_size,class_mode='categorical',shuffle=True)

        STEP_SIZE_TEST = test_generator.n//test_generator.batch_size

        self.model.compile(loss=keras.losses.categorical_crossentropy, optimizer=Adam(lr=lr), metrics=['accuracy'])
        score = self.model.evaluate_generator(test_generator, steps=STEP_SIZE_TEST, verbose=1)
        print('Test loss:', score[0])
        print('Test accuracy:', score[1])

        label = (test_generator.class_indices)
        self.labels = dict((v,k) for k,v in label.items())
        print(self.labels)





    def predict_on_crops(self, entire_images_path, window=50, stride=20):

        # For each image predict ton corps
        for count, each_image_path in enumerate(entire_images_path):

            print('**********Create crops and save to swap**************')
            SWAP = create_crops_of_entire_Image(each_image_path, self.base_path+'swap', window, stride)
            print('**********Create crops is done**************')


            predgen = ImageDataGenerator(rescale=1./255)
            preds_generator = predgen.flow_from_directory(SWAP , target_size=(window, window), color_mode="rgb",batch_size=1, shuffle=False)
            STEP_SIZE_PRED = preds_generator.n//preds_generator.batch_size
            preds_generator.reset()
            pred=self.model.predict_generator(preds_generator, steps=STEP_SIZE_PRED, verbose=1)
            print('one image predicted, the pred shape is {}'.format(pred.shape))


            # flow from directory sweeps the Images alphabitcly, we need to map each prediction to the right one
            print('**********Maping to the right index**************')
            feeding_order = [SWAP+'/'+str(i)+'.JPG' for i in range(preds_generator.n)]
            feeding_order = sorted(feeding_order)
            #print(feeding_order)
            pred_correct = np.zeros((preds_generator.n,2),dtype=np.float32)
            for number,value in enumerate(feeding_order):
                #print(value)
                right_index = value.split('/')[-1].split('.')[0]
                pred_correct[int(right_index),:] = pred[number,:]
                #print('the shape of corrected prediction is {}'.format(pred_correct.shape))


            # find top 60 guesses
            maximum_per_pixel = pred_correct[:,0]
            decision = maximum_per_pixel.argsort()[-60:][::-1]
            print('Selected pixels are:',decision)
            vote = np.zeros(pred_correct.shape[0],)
            vote [decision] = 1
            vote_shape = np.transpose(vote.reshape(int((4000-50)/20)+1,-1))
            path_of_npy_save = self.base_path+'/predictions/feature_map_npy/'+each_image_path.split('/')[-2]
            check_and_create(path_of_npy_save)
            print(each_image_path)
            print(path_of_npy_save+'/'+each_image_path.split('/')[-1].split('.')[0]+'.npy')
            np.save(path_of_npy_save+'/'+each_image_path.split('/')[-1].split('.')[0]+'.npy',vote_shape)


            show= (1-vote_shape).astype('uint8')*255
            img = Image.fromarray(show,mode='L')

            path_of_featuremap_save = self.base_path+'/predictions/feature_map/'+each_image_path.split('/')[-2]
            check_and_create(path_of_featuremap_save)
            img.save(path_of_featuremap_save+'/'+each_image_path.split('/')[-1])
            print('done predction for {}',format(count/float(len(entire_images_path))))
            print('**********Prediction is done for this example**************')



