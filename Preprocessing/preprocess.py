from tqdm import tqdm
import os
import glob
from scipy.io import loadmat,savemat
import random
import pickle
from collections import defaultdict
from multiprocessing import Pool, cpu_count
import numpy as np
import json
import argparse

""" This script takes the mat path and generates 4 dataset pickle files that are inputs to the MLFramework""" 


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
    cnt = total_ex_len  
    Imean = Itotal / cnt
    above = Itotal_square - 2 * Imean * Itotal + cnt * (Imean**2)
    Istd = np.sqrt(above / cnt)
    Qmean = Qtotal / cnt
    above = Qtotal_square - 2 * Qmean * Qtotal + cnt * (Qmean**2)
    Qstd = np.sqrt(above / cnt)
    return Imean, Istd, Qmean, Qstd, total_ex_len

def create_dataset(mat_address, pkl_path, sigmf_address, distance_list, device_list, symbolic_transmitter_key):
    
    if not os.path.isdir(pkl_path):
        os.mkdir(pkl_path)

    train_list = []
    val_list = []
    label_list = defaultdict(dict)
    test_list = []

    print("Creating train/val/test partitions:")
        
    # Form the train, validation, and test sets     
    
    # if your mat files are following the format of Device_Distance_anything_else.mat then use these two nested for loop
    # these for loops partition each Device and distance into 70%, 10%, and 20% for training, validation, and test
    for device in tqdm(device_list):
        for distance in tqdm(distance_list):
            all_files = glob.glob(mat_address + device+'_'+distance+'_'+'*')
            random.shuffle(all_files)
            train_list += all_files[:int(0.7*len(all_files))]
            val_list += all_files[int(0.7*len(all_files)):int(0.8*len(all_files))]
            test_list += all_files[int(0.8*len(all_files)):]

    # if the Device (transmitter) and Distance are not mentioned in the file name, uncomment and use this part:
    # This part shuffles all mat files and randomly partitions them into 70%, 10%, and 20% for training, validation, and test
    """all_files = glob.glob(mat_address + '*')
    random.shuffle(all_files)
    train_list += all_files[:int(0.7*len(all_files))]
    val_list += all_files[int(0.7*len(all_files)):int(0.8*len(all_files))]
    test_list += all_files[int(0.8*len(all_files)):]"""

    # create labels:
    print("Creating label pickle file:")
    all_mat_list = train_list + val_list + test_list
    for file in tqdm(all_mat_list):

        # read the label from the file name:
        #label_list[file]= file.split('/')[-1].split('_')[0]
        
        # read the label from the corresponding meta-data file (slower than file name)
        json_name = file.split('/')[-1].split('.')[0]+'.json'
        json_path = os.path.join(sigmf_address, json_name)
        with open (json_path, 'r') as handle:
            meta = json.load(handle)
        label[file] = device_list.index(meta['annotations']['transmitter']['core:'+symbolic_transmitter_key])


    with open (pkl_path+'label.pkl','wb') as handle:
        pickle.dump(label_list,handle)

    # partition 
    print("Creating partition pickle file:")
    partition = {}
    partition['train']= train_list
    partition['test']= test_list    
    partition['val']= val_list
    print("lengths of partitions are:")
    print len(train_list),len(val_list),len(test_list)
    with open (pkl_path+'partition.pkl','wb') as handle:
        pickle.dump(partition,handle)

    # device_ids
    print("Creating device ids pickle file:")
    device_ids={}
    for element in tqdm(device_list):
        device_ids[element] = device_list.index(element)
    with open (pkl_path+'device_ids.pkl','wb') as handle:
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
    with open (pkl_path+'stats.pkl','wb') as handle:
        pickle.dump(stats_dict,handle)
    print("Dataset successfully generated in: ")
    print(pkl_path)

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description = 'Preprocessing script',formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--sigmf_address', default='', type=str, help='Please enter the path to the directory containing Signal meta-data files. This path will be used to pick proper label (transmitter ID) for each transmission.')
    parser.add_argument('--mat_address', default='', type=str, help='The path where you keep the .mat files (dataset)')
    parser.add_argument('--pkl_path', default='', type=str, help='The path where the pkl files will be generated.')
    parser.add_argument('--symbolic_class_name', default='', type=str, help='Symbolic class name, for example Tx, or uav.')
    parser.add_argument('--num_classes', default=7, type=int, help='Number of classes (transmitters).')
    parser.add_argument('--distance_list', default='6ft,9ft,12ft,15ft', type=str, help='List of distances.')
    parser.add_argument('--symbolic_transmitter_sigmf_key', default='UAV', type=str, help='The key in Sigmf meta-data, in transmitter key whose value is symbolic transmitter')

    args = parser.parse_args()
    
    # create the device list: (transmitter list)
    device_list = []
    for i in range(1 , args.num_classes+1):
        device_list.append(args.symbolic_class_name+str(i))

    # create distance list:
    distance_list = args.distance_list.split(',')

    create_dataset(args.mat_address, args.pkl_path, args.sigmf_address, distance_list, device_list, args.symbolic_transmitter_sigmf_key)

