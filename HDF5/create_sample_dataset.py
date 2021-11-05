#!/usr/bin/env python
# coding: utf-8

# In[1]:


import h5py
import os
import numpy as np
import cv2
import open3d as o3d
import re


# In[ ]:





# In[2]:


# flash_dataset_hf = h5py.File("path/Flash_sample_dataset.hdf5",'w')
hdf5_file_name = os.path.join(os.getcwd(), "Flash_sample_dataset.hdf5")
if not os.path.isfile(hdf5_file_name):
    flash_dataset_hf = h5py.File(hdf5_file_name,'w')

# Group 1- Sensors
Sensors = flash_dataset_hf.create_group('Sensors')
# Group 1- subfolders
coord = Sensors.create_group('coord')
hero4 = Sensors.create_group('hero4')
hero9 = Sensors.create_group('hero9')
vlp = Sensors.create_group('vlp')
ost = Sensors.create_group('ost')

# Group 2- Label
Label = flash_dataset_hf.create_group('Label')

# metadata file for dataset
flash_dataset_hf.attrs['Category'] = 'Cat3'
flash_dataset_hf.attrs['NLOS Object'] = 'Car'
flash_dataset_hf.attrs['Mobility'] = 'Static'
flash_dataset_hf.attrs['Position'] = 'Front'
flash_dataset_hf.attrs['Speed'] = '15mph'
flash_dataset_hf.attrs['Direction'] = 'LR'
flash_dataset_hf.attrs['Lane'] = 'Opposite'





# In[3]:


# to read data from local folder and creating dataset in hdf5 groups/subgroups
sensors_path = os.path.join(os.getcwd(),'FLASH_dataset_samples/Sensors')
label_path = os.path.join(os.getcwd(),'FLASH_dataset_samples/Label')


#creating dataset for sensors
subgroup_names = ['coord', 'hero4','hero9','vlp','ost']
for subgroup in subgroup_names:
    subgroup_path = os.path.join(sensors_path, subgroup)
    files_list = os.listdir(subgroup_path) 
    
    if (subgroup ==  "coord"):
        for count, file_name in enumerate (files_list):
            if file_name.endswith('.txt'):
                value = np.loadtxt(os.path.join(subgroup_path,file_name))
                name = "Sensors_"+str(subgroup)+"_ds_"+str(count)
                if name not in Sensors[subgroup].keys():
                    IQ = coord.create_dataset(name=name,data = value)

    if (subgroup ==  "hero4"):
            for count, file_name in enumerate (files_list):
                if file_name.endswith('.jpg'):
                    value = cv2.imread(os.path.join(subgroup_path,file_name)) # reads image in BGR format
                    name = "Sensors_"+str(subgroup)+"_ds_"+str(count)
                    if name not in Sensors[subgroup].keys():
                        IQ = hero4.create_dataset(name=name,data = value)
                        
                        
    if (subgroup ==  "hero9"):
            for count, file_name in enumerate (files_list):
                if file_name.endswith('.jpg'):
                    value = cv2.imread(os.path.join(subgroup_path,file_name)) # reads image in BGR format
                    name = "Sensors_"+str(subgroup)+"_ds_"+str(count)
                    if name not in Sensors[subgroup].keys():
                        IQ = hero9.create_dataset(name=name,data = value)
                 

    if (subgroup ==  "vlp"):
            for count, file_name in enumerate (files_list):
                if file_name.endswith('.pcd'):
                    pcd = o3d.io.read_point_cloud(os.path.join(subgroup_path,file_name))
                    value = np.asarray(pcd.points)  
                    name = "Sensors_"+str(subgroup)+"_ds_"+str(count)
                    if name not in Sensors[subgroup].keys():
                        print("Hello")
                        IQ = vlp.create_dataset(name=name,data = value)
 

    if (subgroup ==  "ost"):
            for count, file_name in enumerate (files_list):
                if file_name.endswith('.pcd'):
                    pcd = o3d.io.read_point_cloud(os.path.join(subgroup_path,file_name))
                    value = np.asarray(pcd.points)  
                    name = "Sensors_"+str(subgroup)+"_ds_"+str(count)
                    if name not in Sensors[subgroup].keys():
                        IQ = ost.create_dataset(name=name,data = value)
         
        

# # creating dataset for label
# files_list = os.listdir(label_path)
# for count, file_name in enumerate (files_list):
#     with open(os.path.join(label_path,file_name),'r') as f:
#         txt = f.read()
#         print(txt)
#     nums = re.findall(r'\[([^][]+)\]', txt)
#     print(nums)
#     value = np.loadtxt(nums)
#     #value = np.loadtxt(os.path.join(label_path,file_name), delimiter=',')
#     print(value)
#     name = "Label"+"_ds_"+str(count)
#     if name not in flash_dataset_hf.keys():    
#         IQ = Label.create_dataset(name=name,data = value)




# In[4]:


# to read the files from hdf5
hdf5_dataset_path = os.path.join(os.getcwd(), "Flash_sample_dataset.hdf5")
reading_hdf5_dataset = h5py.File(hdf5_dataset_path,'r')


# In[7]:


# reading items from the hdf5 file
hdf5_items = list(reading_hdf5_dataset.items())
print("hdf5_items",hdf5_items)


#reading items from the coord subgroup
reading_group = reading_hdf5_dataset.get('Sensors')
print("reading_sensors",list(reading_group.items())) 
reading_subgroup = reading_group.get('coord')
# print("coord_items",list(reading_subgroup.items()))
print("coord_items",np.array(reading_subgroup.get("Sensors_coord_ds_0")))



reading_subgroup = reading_group.get('ost')
print("ost",np.array(reading_subgroup.get("Sensors_ost_ds_0")))


# In[ ]:





# In[ ]:




