#creats crops of sizw window, column wise

from PIL import Image
import glob
import numpy as np
import heapq
from matplotlib import cm
import random
import os
from tqdm import tqdm
import sys

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

main_directory = sys.argv[1]   #For example "/home/batool/mmwave-beamforming"
save_path = main_directory+'/data/'
imag_path = main_directory+'/Wall/Images/'
[check_and_create(save_path+sets+'/'+classes) for classes in ['Background','Antenna1','Antenna2'] for sets in ['train','validation','test']]


for flag in ['Background',"Antenna1","Antenna2"]:
  input_path = imag_path+flag

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
  crops_per_Image = int(number_of_shrinked_crops/number_of_files_in_directory)
  print('Generate {} crops per Image'.format(crops_per_Image))

  count=1

  for experiment in tqdm(show_all_files_in_directory(input_path)):
      img=Image.open(experiment)

      row_step = int((img.size[1]-window)/stride+1)
      col_step = int((img.size[0]-window)/stride+1)

      all_strides = [(j*stride,k*stride) for j in range(col_step) for k in range(row_step)]
      index = np.random.permutation(len(all_strides))[:crops_per_Image]
      strides = [all_strides[m] for m in index]

      for counter_per_Image, strides_to_genearte in enumerate(strides):

          area = (strides_to_genearte[0], strides_to_genearte[1], strides_to_genearte[0]+window, strides_to_genearte[1]+window)
          crop = img.crop(area)
          name = str(count)+'.JPG'

          random_number = random.uniform(0, 1)

          if random_number<0.7:
              crop.save(save_path+'train/'+flag+'/'+name)
          elif 0.7<random_number<0.85:
              crop.save(save_path+'validation/'+flag+'/'+name)
          elif 0.85<random_number:
              crop.save(save_path+'test/'+flag+'/'+name)

          count +=1
  print('{} crops has been created'.format(count))
