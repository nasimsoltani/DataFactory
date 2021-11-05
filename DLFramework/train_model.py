import pickle as pkl
import data_generator as DG
import os
from CustomModelCheckpoint import CustomModelCheckpoint
from keras.callbacks import EarlyStopping
import glob

def train_model(args, model):

    # initialize function:
    
    
    # load training data
    with open(os.path.join(args.partition_path,'partition.pkl'),'rb') as handle:
        partition = pkl.load(handle)
    train_list = partition['train']
    val_list = partition['val']

    
    # create train and validation generators    
    train_generator = DG.IQDataGenerator(train_list, args)
    val_generator = DG.IQDataGenerator(val_list, args)

    call_backs = []

    checkpoint = CustomModelCheckpoint(os.path.join(args.save_path, "weights.{epoch:02d}-{val_loss:.2f}.hdf5"), monitor='val_acc', verbose=2, save_best_only=True)
    call_backs.append(checkpoint)

    if args.early_stopping:
        earlystop_callback = EarlyStopping(monitor='val_acc', min_delta=0, patience=args.patience, verbose=2, mode='auto')
        call_backs.append(earlystop_callback)
            
        model.fit_generator(generator=train_generator, validation_data=val_generator, use_multiprocessing=False, 
                max_queue_size=100, shuffle=False, epochs=args.epochs, callbacks=call_backs, initial_epoch=0, verbose = 2)

    # save the final model right before exiting
    model.save(os.path.join(args.save_path,"model.hdf5"))
    # Now that training has ended, remove all intermediate weights to save space
    weight_list = glob.glob(os.path.join(args.save_path,'weights.')+'*')
    for w in weight_list:
        os.remove(w)
    
    # load the last weights and exit
    model.load_weights(os.path.join(args.save_path,'model.hdf5'), by_name=True)

    return model
