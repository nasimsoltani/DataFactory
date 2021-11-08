from __future__ import print_function

import numpy as np
import sys
import os
import glob


from PIL import Image
from random import randrange
from tqdm import tqdm

from numpy import expand_dims
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import ImageDataGenerator



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



mode = 1
input_path='/home/batool/Directroy/Wall/Images/Antenna'+str(mode)+'/'
save_path = '/home/batool/Directroy/Wall/Images/Antenna'+str(mode)+'/Augmented/'
window = 50
stride = 20

# We have more samples for background(3000,4000,3), we shrink that with rate 0.7

background_shape = (3000,4000,3)
Antenna1_shape = (70,70,3)
Antenna2_shape = (170,170,3)

num_backround = int((((3000-window)/stride)+1)*(((4000-window)/stride)+1))
num_antenna1 = (((70-window)/stride)+1)*(((70-window)/stride)+1)
num_antenna2 = (((170-window)/stride)+1)*(((170-window)/stride)+1)
print(num_backround,num_antenna1,num_antenna2)

antenna_array_paths = show_all_files_in_directory(input_path)
print('There are {0} files in folder'.format(len(antenna_array_paths)))
check_and_create(save_path)

if mode == 1:
   rate = int(num_backround/num_antenna1/2)
   width = 70
   height = 70

elif mode==2:
   rate = int(num_backround/num_antenna2/2)   
   width = 170
   height = 170 

print(rate)

count=1

for i in tqdm(antenna_array_paths):
    img=load_img(i)
    data = img_to_array(img)
    samples = expand_dims(data, 0)
    datagen = ImageDataGenerator(brightness_range=[0.5,1.5])
    it = datagen.flow(samples, batch_size=1)


    for r in range(rate):

        batch = it.next()
        image = batch[0].astype('uint8')
        img = Image.fromarray(image,mode='RGB')
        img.save(save_path+str(count)+'.JPG')
        count+=1
        
print(count)

