import h5py
import numpy as np
from PIL import Image
import os
from tqdm import tqdm
import sys

from numpy import expand_dims
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import ImageDataGenerator


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


def create_effected_samples_entire_image(Input_path,repeat):
    all_JPGS = show_all_files_in_directory(Input_path)
    print("number of images:",len(all_JPGS))

    for i in all_JPGS:
        img = load_img(i)
        data = img_to_array(img)
        samples = expand_dims(data, 0)
        datagen = ImageDataGenerator(brightness_range=[0.5,1.5])
        it = datagen.flow(samples, batch_size=1)

        # folder name
        folder = i.split('/')[-2]
        name = i.split('/')[-1].split('.')[0]

        count=0
        for i in tqdm(range(repeat)):
            batch = it.next()
            image = batch[0].astype('uint8')
            img = Image.fromarray(image,mode='RGB')
            img.save(Input_path+folder+'/'+name+'-'+str(count)+'.JPG')
            count +=1

#####Inputs
hdf5_path = sys.argv[1]           #For example'/home/batool/mmwave-beamforming/Wood/Wood_zip/Wood_angle1.hdf5'
main_directory = sys.argv[2]      #For example "/home/batool/mmwave-beamforming"

f = h5py.File(hdf5_path, 'r')
Angle1 = f.get('Angle1')

print('**********Generating Entire Images**********')
Entire_Image_original_angle_1 = Angle1.get('Entire_Image_original_angle_1')
pairing = [("Image-case-"+str(i)+"-"+str(j),"label-case-"+str(i)+"-"+str(j)) for i in range(1,6) for j in range(1,6)]

for k in pairing:
    img = Entire_Image_original_angle_1[k[0]]
    label = Entire_Image_original_angle_1[k[1]]
    ######## Save image to JPG
    Image_save = Image.fromarray(np.array(img))
    folder_name = k[0][-3:]+'-'+str(np.array(label)[0])+'-'+str(np.array(label)[1])
    check_and_create(main_directory+'/Entire_Image_original/'+folder_name)
    Image_save.save(main_directory+'/Entire_Image_original/'+folder_name+"/"+str(k[0][-3:]+'.JPG'))

create_effected_samples_entire_image(main_directory+'/Entire_Image_original/',50)

print('**********Generating Class samples**********')
class_samples = Angle1.get('Cropped_Samples_per_class')
print('class_samples',class_samples.keys())
Antenna1_samples = class_samples.get('Antenna1')
Antenna2_samples = class_samples.get('Antenna2')
Background_samples = class_samples.get('Background')


print('**********Generating Background samples**********')
for b in tqdm(Background_samples.keys()):
    name = b.split('_')[-1]
    img = Image.fromarray(np.array(Background_samples[b]))
    check_and_create(main_directory+'/Wall/Images/'+"Background"+"/")
    img.save(main_directory+'/Wall/Images/'+"Background"+"/"+str(name)+'.JPG')

print('**********Generating Antenna1 samples**********')
for a1 in tqdm(Antenna1_samples.keys()):
    name = a1.split('_')[-1]
    img = Image.fromarray(np.array(Antenna1_samples[a1]))
    check_and_create(main_directory+'/Wall/Images/'+"Antenna1"+"/")
    img.save(main_directory+'/Wall/Images/'+"Antenna1"+"/"+str(name)+'.JPG')

print('**********Generating Antenna2 samples**********')
for a2 in tqdm(Antenna2_samples.keys()):
    name = a2.split('_')[-1]
    img = Image.fromarray(np.array(Antenna2_samples[a2]))
    check_and_create(main_directory+'/Wall/Images/'+"Antenna2"+"/")
    img.save(main_directory+'/Wall/Images/'+"Antenna2"+"/"+str(name)+'.JPG')
