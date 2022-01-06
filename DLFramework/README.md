
### DLFramework 
(To be run after Pre-processing API)

The DLFramework takes the path to the 4 .pkl files generated from the preprocessing step and trains and tests the neural network with the parameters that the user specifies. The toppest file in the framework is `top.py` which calls training and test functions.

	top.py			# calls data loaders, training, and test functions.
	data_generator.py	# contains a version of Keras DataGenerator class, edited for our need. This file returns the training batches along with the corresponding labels.
	create_model.py		# creates the empty template of the neural network architecture and saves it in a model_file.json file.
	train_model.py 		# trains the model.
	test_model.py		# tests the trained model and saves the predictions in a preds.pkl file.
	NNs 			# a folder containing different neural network architectures.

The user arguments are given to the top.py using a bash script. The bash script is run as:

	./run.sh exp1 0

where **exp1** is variable **$1** in the bash file and represents an optional experiment name, and **0** is variable **$2** in the bash file and represents the GPU ID.

	python -u /home/nasim/UAVFramework/DLFramework/top.py \
	--exp_name $1 \
	--partition_path /home/nasim/UAV-TVT/PklFiles/cnn1/ \
	--stats_path /home/nasim/UAV-TVT/PklFiles/cnn1/ \
	--save_path /home/nasim/UAV-TVT/results/ \
	--model_flag alexnet \
	--contin false \
	--json_path /home/nasim/UAV-TVT/results/cnn1/model_file.json \
	--hdf5_path /home/nasim/UAV-TVT/results/cnn1/model.hdf5 \
	--slice_size 200 \
	--num_classes 7 \
	--batch_size 256 \
	--id_gpu $2 \
	--normalize true \
	--train true \
	--test true \
	--epochs 100 \
	--early_stopping true \
	--patience 5 \
	> /home/nasim/UAV-TVT/results/$1/log.out \
	2> /home/nasim/UAV-TVT/results/$1/log.err
	
- python -u path_to_top.py
- **exp_name**: An optional name for this experiment. This name will also be the name of the folder your results will be saved to.
- **partition_path**: Path to the `partition.pkl` file generated from pre-processing step.
- **stats_path**: Path to the stats.pkl file generated from pre-processing step. (if you are training, this will be the same as your partition_path)
- **save_path**: Path to the result folder on your system.
- **model_flag**: A switch to use either of the models in the paper, alexnet or resnet. Please note that our alexnet is a modified version of the famous AlexNet, and is not exactly the same.
- **contin**: Set to true if you want to load a pre-trained model and continue training/testing from there.
- **json_path**: If conin is set to true, this argument represents the structure file path for the pre-trained model.
- **hdf5_path**: If conin is set to true, this argument represents the weight file path for the pre-trained model.
- **slice_size**: Input size of the NN also known as slice size in the paper.
- **num_classes**: Number of UAVs you want to fingerprint. This argument determines the output size of the NN.
- **batch_size**: Your desired batch size for training.
- **id_gpu**: The GPU ID you like to use for training/test.
- **normalize**: Set to true if you wish to normalize data for training/test.
- **train**: Set to true if you want to train a network.
- **test**: Set to true if you want to test a nework.
- **epochs**: The number of epochs you wish to run training for.
- **early_stopping**: Set to true if you wish to stop earlier than the number of epochs determined above.
- **patience**: If early stopping is set to true, the training stops after the validation accuracy does not improve for this many consecutive epochs.
- The last two lines specify where you want to write the output log and error log in the result folder.

The `DLFramework` generates the outputs in a folder named as the variable `exp_name` in the path specified in `save_path'. The output files are as the following:
- `model_file.json` containing the structure of the neural network.
- `model.hdf5` containing the trained weights.
- `log.out` containing the recorded outputs.
- `log.err` containing the recorded errors.
- `preds.pkl` containing the neural network predictions for each test transmission.
