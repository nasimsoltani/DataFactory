import os
from PIL import Image
from tqdm import tqdm
import shutil
import sys


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


main_directory = sys.argv[1]     #For example "/home/batool/mmwave-beamforming"

for sets in ["train","validation","test"]:

    folder1 = main_directory+'/data/'+sets+'/Antenna1/'
    folder2 = main_directory+'/data/'+sets+'/Antenna2/'
    save_path = main_directory+'/data/'+sets+'/Antenna/'
    check_and_create(main_directory+'/data/'+sets+'/Antenna/')

    all_Image = show_all_files_in_directory(folder1)+show_all_files_in_directory(folder2)
    print("# of found images",len(all_Image))

    count = 0
    for move in tqdm(all_Image):
        im = Image.open(move)
        new_name = str(count)+'.JPG'
        im.save(save_path+new_name)
        count +=1

    shutil.rmtree(folder1)
    shutil.rmtree(folder2)
