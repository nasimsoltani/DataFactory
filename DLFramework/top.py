import argparse
from keras.callbacks import TensorBoard
from time import time
from keras.utils import plot_model
import os
import pickle
from keras.optimizers import Adam

from create_model import *
from train_model import *
from test_model import *

def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Train and validation pipeline',formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--exp_name', default='exp1', type=str, help='experiment name')
    parser.add_argument('--save_path', default='', type=str, help='The path where you want the results to be saved')
    parser.add_argument('--partition_path', default='', type=str, help='Specify the base path')
    parser.add_argument('--stats_path', default='', type=str, help='Specify the stats path')
    parser.add_argument('--model_flag', default='alexnet', type=str, help='Specify which model to use: alexnet or resnet')

    parser.add_argument('--slice_size', default=1024, type=int, help='Specify the slice size')
    parser.add_argument('--batch_size', default=32, type=int, help='Specify the batch size')
    parser.add_argument('--num_classes', default=100, type=int, help='Specify the number of total classes')
    parser.add_argument('--normalize', default='True', type=str2bool, help='Specify if you want to normalize the data during training and test')
    parser.add_argument('--epochs', default=10, type=int, help='')
    parser.add_argument('--id_gpu', default=0, type=int, help='The id of GPU you like to run the code on.')
    parser.add_argument('--early_stopping', default=False, type=str2bool, help='Specify if you want to use early stopping')
    parser.add_argument('--patience', default=1, type=int, help='patience')
    parser.add_argument('--train', default=False, type=str2bool, help='Specify doing training or not')
    parser.add_argument('--test', default=False, type=str2bool, help='Specify doing test or not')
    parser.add_argument('--contin', default=False, type=str2bool, help='If you want to load a pre-trained model')
    parser.add_argument('--hdf5_path', default='', type=str, help='weight path')
    parser.add_argument('--json_path', default='', type=str, help='model path')
    parser.add_argument('--dtype', default='float32', type=str, help='data type')

    # initialize:
    args = parser.parse_args()
    if args.id_gpu >= 0:
        os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
        # The GPU id to use
        os.environ["CUDA_VISIBLE_DEVICES"] = str(args.id_gpu)
    args.save_path = os.path.join(args.save_path , args.exp_name)
    with open(os.path.join(args.stats_path,'stats.pkl'),'rb') as handle:
        args.stats = pkl.load(handle)
    with open(os.path.join(args.partition_path,'label.pkl'),'rb') as handle:
        args.labels = pkl.load(handle)
    with open(os.path.join(args.partition_path,'device_ids.pkl'),'rb') as handle:
        args.device_ids = pkl.load(handle)
    
    with open(os.path.join(args.partition_path,'partition.pkl'),'rb') as handle:
        partitions = pkl.load(handle)
    print('train/val/test partitions have this many examples:')
    print len(partitions['train']), len(partitions['val']), len(partitions['test'])

    # create the model
    model = create_model(args)
    model.summary()

    model.compile(loss='categorical_crossentropy', optimizer=Adam(lr=0.0001), metrics=['accuracy'])
    
    # train the model if train is true
    if args.train:
        print('***** Training the model *****')
        model = train_model(args, model)

    # test the model if test is true
    if args.test:
        print('***** Testing the model *****')
        slice_acc, example_acc = test_model(args, model)

        print('slice accuracy and example accuracy are:')
        print('('+str(slice_acc)+' , '+str(example_acc)+')')
