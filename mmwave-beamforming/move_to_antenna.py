import os 
from PIL import Image
from tqdm import tqdm

def show_all_files_in_directory(input_path):
    'This function reads the path of all files in directory input_path'
    files_list=[]
    for path, subdirs, files in os.walk(input_path):
        for file in files:
            if file.endswith(".JPG"):
               files_list.append(os.path.join(path, file))
    return files_list





folder1 = '/home/batool/Directroy/data/validation/Antenna1/'
folder2 = '/home/batool/Directroy/data/validation/Antenna2/'
save_path = '/home/batool/Directroy/data/validation/Antenna/'

all_Image = show_all_files_in_directory(folder1)+show_all_files_in_directory(folder2)
print(all_Image)


count = 0 
for move in tqdm(all_Image):
    im = Image.open(move)
    new_name = str(count)+'.JPG'
    im.save(save_path+new_name)
    count +=1
