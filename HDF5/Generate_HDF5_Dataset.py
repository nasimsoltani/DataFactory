#!/usr/bin/env python
# coding: utf-8

# In[167]:


import h5py
import os
import numpy as np
import cv2
import open3d as o3d
import re
import argparse

def create_group_subgroup (destination_dir,hdf5_file_name) :
    hdf5_file_name = os.path.join(destination_dir, hdf5_file_name)
    with h5py.File(hdf5_file_name, 'w') as hdf5_dataset:
        # Group 1- Sensors
        Sensors = hdf5_dataset.create_group('Sensors')
        # Group 1- subfolders
        coord = Sensors.create_group('coord')
        hero4 = Sensors.create_group('hero4')
        hero9 = Sensors.create_group('hero9')
        vlp = Sensors.create_group('vlp')
        ost = Sensors.create_group('ost')
        # Group 2- Label
        Label = hdf5_dataset.create_group('Label')


def write_metadata_from_file (destination_dir , meta_file,hdf5_file_name):
    with h5py.File(hdf5_file_name, 'r+') as hdf5_dataset:
        with open(meta_file) as f:
            for line in f:
                (key, val) = line.split(":")
                hdf5_dataset.attrs[key] = val


def store_dataset(destination_dir,hdf5_file_name,group,subgroup,value,count): 
    hdf5_file_name = os.path.join(destination_dir, hdf5_file_name)
    with h5py.File(hdf5_file_name, 'r+') as hdf5_dataset:
        
        Sensors = hdf5_dataset.get('Sensors')
        Label = hdf5_dataset.get('Label')
        
        if (group == 'Sensors'):
            name = "Sensors_"+str(subgroup)+"_ds_"+str(count)
            if name not in Sensors[subgroup].keys():
                subgroup = hdf5_dataset.get("Sensors/"+subgroup)
                subgroup.create_dataset(name=name,data = value)       
        else:
            name = "Label"+"_ds_"+str(count)
            if name not in hdf5_dataset.keys():     
                IQ = Label.create_dataset(name=name,data = value)    
    
                
def create_hdf5_dataset(source_dir, destination_dir,hdf5_file_name):
    # to read files from local folder and creating dataset in hdf5 groups/subgroups
    sensors_path = os.path.join(source_dir,"Sensors")
    label_path = os.path.join(source_dir,"Label")
    
    #creating dataset for sensors
    subgroup_names = ['coord', 'hero4','hero9','vlp','ost']
    for subgroup in subgroup_names:
        subgroup_path = os.path.join(sensors_path, subgroup)
        files_list = os.listdir(subgroup_path) 

        if (subgroup ==  "coord"):
            for count, file_name in enumerate (files_list):
                if file_name.endswith('.txt'):
                    value = np.loadtxt(os.path.join(subgroup_path,file_name))
                    store_dataset(destination_dir,hdf5_file_name,'Sensors',subgroup,value,count)

        if (subgroup ==  "hero4"):
                for count, file_name in enumerate (files_list):
                    if file_name.endswith('.jpg'):
                        value = cv2.imread(os.path.join(subgroup_path,file_name)) # reads image in BGR format
                        store_dataset(destination_dir,hdf5_file_name,'Sensors',subgroup,value,count)

        if (subgroup ==  "hero9"):
                for count, file_name in enumerate (files_list):
                    if file_name.endswith('.jpg'):
                        value = cv2.imread(os.path.join(subgroup_path,file_name)) # reads image in BGR format
                        store_dataset(destination_dir,hdf5_file_name,'Sensors',subgroup,value,count)

        if (subgroup ==  "vlp"):
                for count, file_name in enumerate (files_list):
                    if file_name.endswith('.pcd'):
                        pcd = o3d.io.read_point_cloud(os.path.join(subgroup_path,file_name))
                        value = np.asarray(pcd.points)  
                        store_dataset(destination_dir,hdf5_file_name,'Sensors',subgroup,value,count)

        if (subgroup ==  "ost"):
                for count, file_name in enumerate (files_list):
                    if file_name.endswith('.pcd'):
                        pcd = o3d.io.read_point_cloud(os.path.join(subgroup_path,file_name))
                        value = np.asarray(pcd.points)  
                        store_dataset(destination_dir,hdf5_file_name,'Sensors',subgroup,value,count)

#     creating dataset for label  
    files_list = os.listdir(label_path)
    for count, file_name in enumerate (files_list):
        text_file = os.path.join(label_path,file_name)
        with open(text_file) as f:
            value = []
            for line in f:
                if line.strip():
                    nums = re.findall(r'\[([^][]+)\]', line)
                    val_array = np.loadtxt(nums,delimiter=',',dtype=int)
                    value.append(val_array)
            store_dataset(destination_dir,hdf5_file_name,'Label','',value,count)
        


# In[168]:


if __name__ == '__main__':
    # Parser caller arguments
    argin = argparse.ArgumentParser(description=r"""Generating HDF5 dataset...""")
    argin.add_argument('-p', '--destination_dir', dest='destination_dir', type=str, required=True,
                       help='Directory to store HDF5 dataset file.')
    argin.add_argument('-m', '--metadata_file_path', dest='metadata_file_path', type=str, required=True,
                       help='Path for Metadata .txt file.')
    argin.add_argument('-s', '--source_dir', dest='source_dir', type=str, required=True,
                       help='Directory of raw data.')
    argin.add_argument('-f', '--hdf5_file_name', dest='hdf5_file_name', type=str, required=True,
                       help='File name for HDF5 dataset file with .hdf5 extension')



    args = argin.parse_args()
    destination_dir = args.destination_dir
    metadata_file_path = args.metadata_file_path
    source_dir = args.source_dir
    hdf5_file_name = args.hdf5_file_name
    
    
    # destination_dir   = os.getcwd()
    # meta_file = os.path.join(os.getcwd(),'FLASH_dataset_samples','Metadata.txt')
    # source_dir = os.path.join(os.getcwd(),'FLASH_dataset_samples')
    # hdf5_file_name = "SSSSS.hdf5"


    create_group_subgroup (destination_dir,hdf5_file_name)  
    write_metadata_from_file (destination_dir , metadata_file_path,hdf5_file_name)
    create_hdf5_dataset(source_dir, destination_dir,hdf5_file_name)







