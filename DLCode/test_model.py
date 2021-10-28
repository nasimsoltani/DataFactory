import os
import pickle as pkl
from scipy.io import loadmat
import collections
import numpy as np
from tqdm import tqdm

def test_model(args, model):

    # initialize:

    correct_slice_cntr = 0
    total_slice_cntr = 0
    correct_ex_cntr = 0
    total_ex_cntr = 0

    Preds = {}
    preds_slice = {}
    preds_ex = {}

    # load test set
    with open(os.path.join(args.partition_path,'partition.pkl'),'rb') as handle:
        test_list = pkl.load(handle)['test']
    
    for ex in tqdm(test_list):
        
        # loading mat file
        this_ex = loadmat(ex)['f_sig']
        if this_ex.shape[1] >= args.slice_size:
            data = np.zeros((this_ex.shape[1],2),dtype=args.dtype)
            data[:,0] = np.real(this_ex[0,:])
            data[:,1] = np.imag(this_ex[0,:])
            if args.normalize:
                data = (data - args.stats['mean']) / args.stats['std']
            
            # slice with a stride = 1:
            num_slices = data.shape[0]-args.slice_size+1
            X = np.zeros((num_slices,args.slice_size,2),dtype=args.dtype)
            for i in range(num_slices):
                X[i,:,:] = data[i:i+args.slice_size,:]

            # prepare true index:
            true_index = args.device_ids[args.labels[ex]]

            preds = model.predict(X, batch_size=args.batch_size)

            # calculate slice accuracy:
            slice_pred_index = np.argmax(preds, axis=1)
            counter_dict = collections.Counter(slice_pred_index)
            correct_in_example = counter_dict[true_index]
            correct_slice_cntr += correct_in_example
            total_slice_cntr += preds.shape[0]
            preds_slice[ex] = (preds.shape[0],correct_in_example,counter_dict)

            # calculate example accuracy:
            prob_sum = preds.sum(axis=0)
            example_pred_index = np.argmax(prob_sum)
            if example_pred_index == true_index:
                correct_ex_cntr += 1
            total_ex_cntr +=1
            preds_ex[ex] = prob_sum

    slice_acc = 1.0*correct_slice_cntr/total_slice_cntr
    ex_acc = 1.0*correct_ex_cntr/total_ex_cntr

    # save preds:
    Preds['preds_slice'] = preds_slice
    Preds['preds_ex'] = preds_ex
    with open(os.path.join(args.save_path,'preds.pkl'),'wb') as handle:
        pkl.dump(Preds, handle)
    
    return slice_acc, ex_acc

