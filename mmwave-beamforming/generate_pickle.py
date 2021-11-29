from __future__ import print_function

import argparse
import numpy as np
from PIL import Image
import os
import pickle
import random


def show_all_files_in_directory(input_path):
    'This function reads the path of all files in directory input_path'
    files_list=[]
    for path, subdirs, files in os.walk(input_path):
        for file in files:
            if file.endswith(".npy"):
               files_list.append(os.path.join(path, file))
    return files_list



main_directory = sys.argv[1]     #For example "/home/batool/mmwave-beamforming"

input_path_of_file = main_directory+'/predictions'


print(show_all_files_in_directory(input_path_of_file))


all_np_files = [(i,(i.split('/')[-2].split('-')[2],i.split('/')[-2].split('-')[3])) for i in show_all_files_in_directory(input_path_of_file)]
print(all_np_files)


random.shuffle(all_np_files)

with open('npy_label.pkl', 'wb') as handle:
    pickle.dump(all_np_files, handle, protocol=pickle.HIGHEST_PROTOCOL)

print('pickle succesfully file saved here')
