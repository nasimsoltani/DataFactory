#creats crops of sizw window, column wise

from PIL import Image
import glob
import numpy as np
import heapq
from matplotlib import cm
import random
import os
from tqdm import tqdm

def check_and_create(dir_path):
    if os.path.exists(dir_path):
        return True
    else:
        os.makedirs(dir_path)
        return False



def show_all_files_in_directory(input_path):
    'This function reads the path of all files in directory input_path'
    files_list=[]
    for path, subdirs, files in os.walk(input_path):
        for file in files:
            if file.endswith(".JPG"):
               files_list.append(os.path.join(path, file))
    return files_list


flag = 'Antenna1'


input_path = '/home/batool/Directroy/Wall/Images/'+flag
save_path = '/home/batool/Directroy/data/'
window=50
stride=20


number_of_files_in_directory = len(show_all_files_in_directory(input_path))
print('There are {} files in directory'.format(number_of_files_in_directory))


if flag == 'Background':
   input_size = (3000,4000,3)
   shrink = 1

elif flag == 'Antenna1':
   input_size = (70,70,3)
   shrink = 1

elif flag == 'Antenna2':
   input_size = (170,170,3)
   shrink = 1

number_of_possible_crops = int((input_size[0]-window)/stride+1)*int((input_size[1]-window)/stride+1)*number_of_files_in_directory
print('There are {} possible crops for all Images'.format(number_of_possible_crops))
number_of_shrinked_crops = int(number_of_possible_crops*shrink)
print('We are considering {} crops for all Images'.format(number_of_shrinked_crops))
crops_per_Image = number_of_shrinked_crops/number_of_files_in_directory
print('Generate {} crops per Image'.format(crops_per_Image))


count=1

for experiment in tqdm(show_all_files_in_directory(input_path)):
    img=Image.open(experiment)

    row_step = int((img.size[1]-window)/stride+1)
    col_step = int((img.size[0]-window)/stride+1)

    # If we choose not very large window and stride, it will be equal to stride
    #row_jump = img.size[1]/row_step
    #col_jump = img.size[0]/col_step

    all_strides = [(j*stride,k*stride) for j in range(col_step) for k in range(row_step)]
    print(all_strides)
    index = np.random.permutation(len(all_strides))[:crops_per_Image]
    strides = [all_strides[m] for m in index]
