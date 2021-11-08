#!/usr/bin/env python
# coding: utf-8

# In[43]:


import h5py
import os
import numpy as np
import cv2
import open3d as o3d
import re
import argparse


def read_from_hdf5_dataset(hdf5_file_path):
    # to read hdf5 file
    hdf5_dataset_read_obj = h5py.File(hdf5_file_path,'r')

    # Examples of accessing files
    # reading items from hdf5 file
    hdf5_items = list(hdf5_dataset_read_obj.items())
    print("hdf5 items",hdf5_items)

    #reading items from the groups
    sensor_group = hdf5_dataset_read_obj.get('Sensors')
    print("List of subgroups from Sensors group",list(sensor_group.items())) 
    label_group = hdf5_dataset_read_obj.get('Label')
    print("List of subgroups from Label group",list(label_group.items())) 
    
    #reading items from the Sensors/coord subgroups
    sensor_coord_subgroup = sensor_group.get('coord')
    print("Items in coord ",list(sensor_coord_subgroup.items()))
    print("Reading coord file ",np.array(sensor_coord_subgroup.get("Sensors_coord_ds_0")))
    
    #accessing individual list from the Label groups
    for i in list(label_group.get("Label_ds_0")):
        print(i)

    #accessing metadata
    print("Items in metadata",hdf5_dataset_read_obj.attrs.keys())
    print("Accessing attribute",hdf5_dataset_read_obj.attrs['Mobility']) # Can check for any attribute


# In[44]:


if __name__ == '__main__':
    # Parser caller arguments
    argin = argparse.ArgumentParser(description=r"""Reading data from HDF5 dataset...""")
    argin.add_argument('-p', '--hdf5_file_path', dest='hdf5_file_path', type=str, required=True,
                       help='Path of HDF5 dataset file with .hdf5 extension')

    args = argin.parse_args()
    hdf5_file_path = args.hdf5_file_path
    
    # calling function
    read_from_hdf5_dataset(hdf5_file_path)
    



