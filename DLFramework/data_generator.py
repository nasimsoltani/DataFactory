import keras
from tqdm import tqdm
from scipy.io import loadmat
import pickle as pkl
import numpy as np
import random
from multiprocessing import Pool, cpu_count
import os
import math
import collections

class IQDataGenerator(keras.utils.Sequence):

    def __init__(self, ex_list, args):

        self.args = args
        self.ex_list = ex_list
        self.data_cache = {}

        # load all data to cache:
        print('Adding all files to cache')
        for ex in tqdm(self.ex_list):
            this_ex = loadmat(ex)['f_sig']
           
            if this_ex.shape[1] >= self.args.slice_size:
                data = np.zeros((this_ex.shape[1],2),dtype=self.args.dtype)
                data[:,0] = np.real(this_ex[0,:])
                data[:,1] = np.imag(this_ex[0,:])
                self.__add_to_cache(ex, data)
        
        # update ex_list to contain only examples with length >= slice_size
        print 'length of ex_list before and after:'
        print len(self.ex_list)
        self.ex_list = self.data_cache.keys()
        print len(self.ex_list)
     
    def __len__(self):
        # calculate total number of batches:
        total_slice_cnt = len(self.ex_list)*(self.args.stats['avg_samples']-self.args.slice_size+1)
        batch_cnt = (math.ceil(total_slice_cnt/self.args.batch_size))/float(self.args.slice_size)
        print 'total number of batches are: '+str(int(batch_cnt))
        return int(batch_cnt)

    def __add_to_cache(self, ex, data):
        
        if self.args.normalize:
            data = (data - self.args.stats['mean']) / self.args.stats['std']

        device_id = self.args.device_ids[self.args.labels[ex]]
        self.data_cache[ex] = (data,device_id)
   
    def __getitem__(self, index):
        #Generate one batch of data 

        ex_indices = np.random.randint(len(self.ex_list), size=self.args.batch_size)
         
        X = np.zeros((self.args.batch_size, self.args.slice_size, 2), dtype=self.args.dtype)
        y = np.zeros((self.args.batch_size, self.args.num_classes), dtype=int)

        cnt = 0
        for ex_index in ex_indices:
            
            this_ex = self.data_cache[self.ex_list[ex_index]][0]
            this_class_index = self.data_cache[self.ex_list[ex_index]][1]

            # slicing:
            slice_index = random.randint(0, this_ex.shape[0] - self.args.slice_size)
            X[cnt,:,:] = this_ex[slice_index:slice_index+self.args.slice_size, :]
            
            # create y vector:
            y[cnt,this_class_index] = 1
           
            cnt += 1
        
        return X, y

if __name__ == "__main__":
    base_path = '/home/nasim/UWBDataSet/PklFiles/NewDeviceDetection/Day11_2m_new_device/' 
    stats_path = base_path
    class Employee:
        pass
    args = Employee()

    with open (base_path + 'partition.pkl','rb') as handle:
        partition = pkl.load(handle)
    ex_list = partition['train']
    with open (base_path + 'stats.pkl','rb') as handle:
        stats = pkl.load(handle)
    with open (base_path + 'label.pkl','rb') as handle:
        labels = pkl.load(handle)
    with open (base_path + 'device_ids.pkl','rb') as handle:
        device_ids = pkl.load(handle)


    args.normalize = True
    args.batch_size = 256
    args.slice_size = 32
    args. num_classes = 4
    args.device_ids = device_ids
    args.labels= labels
    args.stats = stats

    DG = IQDataGenerator(ex_list, args)

    print DG.__getitem__(0)
