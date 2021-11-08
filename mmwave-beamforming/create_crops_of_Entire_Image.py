import numpy as np
from tqdm import tqdm
import os
from PIL import Image


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




def create_crops_of_entire_Image(input_image_path,save_path,window,stride):
    # without final slash

    count = 1
    img=Image.open(input_image_path)

    row_step = int((img.size[1]-window)/stride+1)
    col_step = int((img.size[0]-window)/stride+1)

    # If we choose not very large window and stride, it will be equal to stride
    row_jump = img.size[1]/row_step
    col_jump = img.size[0]/col_step
    all_strides = [(j*col_jump,k*row_jump) for j in range(col_step) for k in range(row_step)]

    for strides_to_genearte in tqdm(all_strides):

        area = (strides_to_genearte[0], strides_to_genearte[1], strides_to_genearte[0]+window, strides_to_genearte[1]+window)
        crop = img.crop(area)
        crop.save(save_path+'/Test_folder/'+str(count)+'.JPG')
        count +=1
    print('{} crops has been created'.format(count))
    return save_path



