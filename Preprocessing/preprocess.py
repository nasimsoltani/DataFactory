from tqdm import tqdm
import os
import glob
from scipy.io import loadmat,savemat
import random
import pickle
from collections import defaultdict
from multiprocessing import Pool, cpu_count
import numpy as np

""" This script takes the mat path and generates 4 dataset pickle files that are inputs to the ML_code 
    Please note that this script contains an example script for generating Set1 training/val/test sets
    for CNN1 and needs adjustment in the commented parts for other CNNs in the paper."""

""" Create a pkl_files folder in your UAV-TVT folder and adjust the paths below before running this script """

mat_address = '/home/nasim/UAV-TVT/mat_files/'
dataset_address = '/home/nasim/UAV-TVT/pkl_files/cnn1/'  # adjust this to your desired CNN (optional name)

def helper(file):
    data = loadmat(file,struct_as_record=True)
    sequence = data['f_sig']
    Idata = sequence.real 
    Qdata = sequence.imag
    return np.sum(Idata), np.sum(np.square(Idata)), np.sum(Qdata), np.sum(np.square(Qdata)), sequence.shape[1]
    
def stats(file_list):
    n = len(file_list)
    pool = Pool(cpu_count())
    Itotal = Itotal_square = Qtotal = Qtotal_square = total_ex_len = 0
    for I_tmp, I_tmp_square, Q_tmp, Q_tmp_square, ex_len in tqdm(pool.map(helper, file_list)):
        Itotal += I_tmp
        Itotal_square += I_tmp_square
        Qtotal += Q_tmp
        Qtotal_square += Q_tmp_square
        total_ex_len += ex_len
    cnt = n * total_ex_len * 1 
    Imean = Itotal / cnt
    above = Itotal_square - 2 * Imean * Itotal + Imean ** 2
    Istd = np.sqrt(above / cnt)
    Qmean = Qtotal / cnt
    above = Qtotal_square - 2 * Qmean * Qtotal + Qmean ** 2
    Qstd = np.sqrt(above / cnt)
    return Imean, Istd, Qmean, Qstd, total_ex_len

def create_dataset(mat_address,dataset_address):
    if not os.path.isdir(dataset_address):
        os.mkdir(dataset_address)

    device_list = ['uav1','uav2','uav3','uav4','uav5','uav6','uav7']
    distance_list = ['6ft','9ft','12ft','15ft']

    train_val_list = []
    label_list = defaultdict(dict)
    test_list = []

    print("Creating train/val/test partitions:")
    # adjust this according to the CNN number ( burst1 for CNN1, CNN2, CNN3, CNN4, 
    #                                           burst2 for CNN5, CNN6, CNN7, CNN8, 
    #                                           burst3 for CNN9, CNN10, CNN11, CNN12)
    # Visualization available in the paper Figure 6
    
    # Form the train and validation sets
    desired_training_burst = 'burst1'      
    
    for device in tqdm(device_list):
        for distance in tqdm(distance_list):
            train_val_files = glob.glob(mat_address + device+'_'+distance+'_'+desired_training_burst+'_'+'*')
            # sort the train_val_files 
            sorted_list = []
            for i in range(1,len(train_val_files)/10+1):
                for j in range(10):
                    this_sub_ex = mat_address + device+'_'+distance+'_'+desired_training_burst+'_'+str(i)+'_'+str(j)+'.mat'
                    #if this_sub_ex in train_val_files:
                    sorted_list.append(this_sub_ex)

            # now the sorted list is ready
            # adjust the limit based on the CNN you want to create the training set for:
            train_val_list += sorted_list[:int(0.25*len(sorted_list))]
            
            # add to the test set
            # Form the test list from only burst4
            test_list += glob.glob(mat_address + device+'_'+distance+'_'+'burst4'+'_'+'*')


    # Now train_val_list is ready, shuffle and separate training and validation sets
    random.shuffle(train_val_list)
    train_list = train_val_list[:int(0.9*len(train_val_list))]
    val_list = train_val_list[int(0.9*len(train_val_list)):]

    # create labels:
    print("Creating label pickle file:")
    all_mat_list = train_list + val_list + test_list
    for file in tqdm(all_mat_list):
        label_list[file]= file.split('/')[-1].split('_')[0]
    with open (dataset_address+'label.pkl','wb') as handle:
        pickle.dump(label_list,handle)

    # partition 
    print("Creating partition pickle file:")
    partition = {}
    partition['train']= train_list
    partition['test']= test_list    
    partition['val']= val_list
    print("lengths of partitions are:")
    print len(train_list),len(val_list),len(test_list)
    with open (dataset_address+'partition.pkl','wb') as handle:
        pickle.dump(partition,handle)

    # device_ids
    print("Creating device ids pickle file:")
    device_ids={}
    for element in tqdm(device_list):
        device_ids[element] = device_list.index(element)
    with open (dataset_address+'device_ids.pkl','wb') as handle:
        pickle.dump(device_ids,handle)

    # stats
    print("Creating stats file")
    Imean, Istd, Qmean, Qstd, total_ex_len= stats(train_list)
    avg_sam = int((total_ex_len)*1.0/len(train_list)) if len(train_list)!=0 else 0

    stats_dict={'total_samples':total_ex_len,
    'avg_samples':avg_sam,
    'total_examples':len(train_list),
    'skipped':0,
    'avg_example_per_device':len(train_list)/len(device_list),
    'mean':np.array([Imean,Qmean]),
    'std':np.array([Istd,Qstd])
    }
    with open (dataset_address+'stats.pkl','wb') as handle:
        pickle.dump(stats_dict,handle)
    print("Dataset successfully generated in: ")
    print(dataset_address)

if __name__ == "__main__": 
    create_dataset(mat_address,dataset_address)
