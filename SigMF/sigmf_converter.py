from scipy.io import loadmat, savemat
import glob
import numpy as np
import os
import json
from tqdm import tqdm
import argparse


device_list = ['m1001','m1005','m1007','m1008','m1009','m10010','m10011']
distance_list = ['6ft','9ft','12ft','15ft']
uav_list = []
for i in range(len(device_list)):
    uav_list.append('uav'+str(i+1))
print uav_list


cf_dict = {'m1008_6ft':'2476500000', 'm1008_9ft':'2406500000', 'm1008_12ft':'2406500000', 'm1008_15ft':'2406500000', 'm1009_6ft':'2426500000', 'm1009_9ft':'2426500000', 'm1009_12ft':'2426500000', 'm1009_15ft':'2436500000', 'm1007_6ft':'2476500000', 'm1007_9ft':'2476500000', 'm1007_12ft':'2476500000', 'm1007_15ft':'2476500000', 'm1005_6ft':'2406500000', 'm1005_9ft':'2406500000', 'm1005_12ft':'2406500000', 'm1005_15ft':'2406500000', 'm10011_6ft':'2416500000', 'm10011_9ft':'2416500000', 'm10011_12ft':'2416500000', 'm10011_15ft':'2416500000', 'm1001_6ft':'2406500000', 'm1001_9ft':'2406500000', 'm1001_12ft':'2406500000', 'm1001_15ft':'2406500000', 'm10010_6ft':'2406500000', 'm10010_9ft':'2406500000', 'm10010_12ft':'2406500000', 'm10010_15ft':'2416500000'}

def convert_mat_to_sigmf(sigmf_path, mat_path):
    
    # if destinaiton path does not exist, create it
    if not os.path.isdir(sigmf_path):
        os.mkdir(sigmf_path)

    # get full list of .mat files in the mat_path directory
    
    all_mat_list = glob.glob(mat_path+'*')
    
    for mat_file in tqdm(all_mat_list):
       
        #print mat_file
        mat_filename = mat_file.split('/')[-1].strip('.mat')
        uav = mat_filename.split('_')[0]
        distance = mat_filename.split('_')[1]
        burst = mat_filename.split('_')[2]  
        file_cntr = mat_filename.split('_')[3]
        
        # load the mat file and convert to bin format:
        mat_file_content = loadmat(mat_file)
        seq = mat_file_content['f_sig']
        len_seq=seq.shape[1]
        binary_array = np.zeros((2*len_seq),dtype=np.float16)
        current_bin_index = 0
        print seq
        #print seq.shape
                        
        #----------------------------------------------------------------------- 
                        
        # convert to bin
        for i in range(len_seq):
      
            real_part = np.real(seq[0,i])
            imag_part = np.imag(seq[0,i])
            #print seq[0,i]
            #print real_part,imag_part
            
            binary_array[current_bin_index] = real_part
            binary_array[current_bin_index+1] = imag_part
            
            #print binary_array[current_bin_index]
            #print binary_array[current_bin_index+1]
            #if real_part != binary_array[current_bin_index]:
                #print 'differeeeeent'

            current_bin_index += 2
        binary_format = bytearray(binary_array)

        #binary array is ready now dump it into a file
        bin_filename = mat_filename+'.bin'
        
        with open(os.path.join(sigmf_path,bin_filename), 'wb') as handle:
            handle.write(binary_format)
        
        #--------------------------------------------------------------------
        device = device_list[uav_list.index(uav)]
        this_cf = int(cf_dict[device+'_'+distance])
        
        #create meta data
        my_meta = {
            'global': {
                'core:datatype': 'cf16_le',         
                'core:sample_rate': 10000000,       
                'core:version': '0.0.1',            
                'core:total_transmissions': 13893,
                'core:record_date': 'March 11, 2020',
                'core:description': 'This is the meta file for a specific transmission in the UAV dataset'
                },
            'captures': {
                 'core:sample_start': 0,
                 'core:center_frequency' : this_cf,
                 'core:transmission_number': file_cntr
                },
            'annotations':{
                'core:sample_start': 0,
                'core:sample_count':len_seq,
                'core:environment':'RF anechoic chamber',
                'core:distance':distance,
                'core:protocol':'Lightbridge',
                'transmitter': {
                    'core:make_and_model': 'DJI M100',
                    'core:UAV':uav,
                    'core:device_id_genesys_lab':device,
                    'core:antenna': 'M100 proprietary'
                    },
                'receiver': {
                    'core:radio':'Ettus USRP X310',
                    'core:daughter_board':'UBX 160 USRP',
                    'core:antenna_make':'ETS-Lindgren',
                    'core:antenna_model':'3181 Broadband Mini-Bicon'
                    }
                }
            }

        json_filename = mat_filename+'.json'

        with open(os.path.join(sigmf_path,json_filename),'wb') as json_file:
            json.dump(my_meta, json_file)
       
       


def convert_bin_to_mat(sigmf_path, mat_path):

    # if destination directory does not exist, create it
    if not os.path.isdir(mat_path):
        os.mkdir(mat_path)
    
    bin_json_list = glob.glob(sigmf_path+'*')

    for filepath in tqdm(bin_json_list):
        # do this only if you have a .bin file not a .json file
        if filepath.endswith('.bin'):
            # read the .bin file
            with open (filepath,'rb') as handle:
                iq_seq = np.fromfile(handle, dtype='<f2')    # (f2 => float16)
            n_samples = iq_seq.shape[0]/2
            # separate I and Q
            IQ_data = np.zeros((n_samples,2),dtype=np.float16)
            IQ_data[:,0] = iq_seq[range(0, iq_seq.shape[0]-1, 2)]    # load all I-values in dimension 0
            IQ_data[:,1] = iq_seq[range(1, iq_seq.shape[0], 2)]      # ...and Q-values in dimension 1
            # convert to Complex I/Q
            Complex_IQ = IQ_data[:,0] + 1j*IQ_data[:,1]

            # reshape the complex sequence to (1,L)
            Complex_IQ = np.expand_dims(Complex_IQ, axis=0)

            # dump the complex sequence into a .mat file
            filename = filepath.split('/')[-1].strip('.bin')
            this_mat_file_path = os.path.join(mat_path, filename)

            savemat(this_mat_file_path, {'f_sig':Complex_IQ}) 


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description = 'Converting mat to sigmf and vice-versa',formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--sigmf_path', default='', type=str, help='Directory path that contains or will contain SigMF data.')
    parser.add_argument('--mat_path', default='', type=str, help='Directory path that contains or will contain mat (MATLAB) format.')
    parser.add_argument('--conversion', default='', type=str, help='set to either "sigmf2mat" or "mat2sigmf"')

    args = parser.parse_args() 
    
    sigmf_path = args.sigmf_path
    mat_path = args.mat_path
    conversion = args.conversion

    if conversion == 'sigmf2mat':
        convert_bin_to_mat(sigmf_path, mat_path)
    elif conversion == 'mat2sigmf':
        convert_mat_to_sigmf(sigmf_path, mat_path)
    else:
        'Please set conversion argument to either "sigmf2mat" or "mat2sigmf"'
