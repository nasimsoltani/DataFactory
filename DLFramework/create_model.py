import keras
import keras.models as models
from keras.layers.convolutional import Conv2D, MaxPooling2D, ZeroPadding2D, Conv1D, MaxPooling1D
from keras.layers.core import Flatten, Dense, Dropout, Activation, Reshape
from keras.models import model_from_json#, load_weights
import os

def create_model(args):
    """ creates a new model, or loads a model structure and inserts weights 
    and returns either and empty model or a pre-trained model"""


    if args.contin:
        
        # reading model from json file
        json_file = open(args.json_path, 'r')
        model = model_from_json(json_file.read(), custom_objects=None)
        json_file.close()
        model.load_weights(args.hdf5_path, by_name=True)
    
    else:
        if args.model_flag == 'alexnet':
            from NNs.AlexNet1D import AlexNet1D
            model = AlexNet1D(args.slice_size, args.num_classes)
        elif args.model_flag == 'resnet':
            from NNs.ResNet1D import ResNet1D
            model = ResNet1D(args.slice_size, args.num_classes)
        else:
            print('Error: Model Flag not recognized! Please choose alexnet or resnet.')

        # save the newly created model
        model_json = model.to_json()
        with open(os.path.join(args.save_path,'model_file.json'), "w") as json_file:
            json_file.write(model_json)
    
    return model


