from __future__ import print_function

import numpy as np
import sys
import os
import glob


from PIL import Image
from random import randrange
from tqdm import tqdm

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



mode = 2
input_path='/home/batool/Directroy/Wall/Images/Antenna'+str(mode)+'/'
save_path = '/home/batool/Directroy/Wall/Images/Antenna'+str(mode)+'/rotated_add_by_me/'
window = 50
stride = 20

# We have more samples for background(3000,4000,3), we shrink that with rate 0.7
shrink = 0.7

background_shape = (3000,4000,3)
Antenna1_shape = (70,70,3)
Antenna2_shape = (170,170,3)

num_backround = int((((3000-window)/stride)+1)*(((4000-window)/stride)+1)*shrink)
num_antenna1 = (((70-window)/stride)+1)*(((70-window)/stride)+1)
num_antenna2 = (((170-window)/stride)+1)*(((170-window)/stride)+1)
print(num_backround,num_antenna1,num_antenna2)

antenna_array_paths = show_all_files_in_directory(input_path)
print('There are {0} files in folder'.format(len(antenna_array_paths)))
check_and_create(save_path)

if mode == 1:
   rate = int(num_backround/num_antenna1)
   width = 70
   height = 70

elif mode==2:
   rate = int(num_backround/num_antenna2)   
   width = 170
   height = 170 

print(rate)

count=1

for i in tqdm(antenna_array_paths):
    I=Image.open(i)

    for r in range(rate):
        deg = randrange(-90,90)
        rotated = I.rotate(deg)
        rotated.save(save_path+str(count)+'.JPG')
        count+=1
        
print(count)

