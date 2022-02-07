### Preprocessing

Preprocessing is preparing the already collected dataset for being fed to the neural network. 

Preprocessing consists of a series of steps such as:

1. Partitioning the dataset to training, validation, and test sets. 
2. Calculating mean and standard deviation of the training set, which is later used for z-score standardization.
3. Creating training and test true labels for each signal.

Before running the preprocessing script, the dataset must be saved in the form of `.mat` files in one folder on the hard storage. For the `.mat` files to be readable by the DLFramework, each signal (transmission) must be resized to (1,L) as a vector of L complex values. During preprocessing, device labels are read from the meta-data files in the SigMF directory (sigmf_address variable). In this case, the symbolic name of the tranmitter (e.g., Tx3 or uav4) must be recorded under the `annotations` object, `transmitter` key, in a `core:symbolic_transmitter_sigmf_key`, such as `core:UAV` (for the UAV dataset example) or an optional `core:Tx` key for a non-UAV dataset. Your optional symbolic_transmitter_sigmf_key that exists in your meta-data.json file, is given to the script through the input argument `symbolic_transmitter_sigmf_key`.

**Naming format**: It is recommended that the .mat files follow the naming convention of `Device_Distance_anything_else.mat`. In this case, the script can do a balanced partitioning of the collected dataset into training, validation, and test sets. If your .mat files do not follow the naming convention, please comment lines 58 to 64, and uncomment 68 to 72. 

<!--- Each transmission should be named as devicename_A_B_etc.mat. During preprocessing device labels are infered from the first element before '_'. --->

The preprocessing script is run through a bash script with the following arguments.

	python -u ./preprocess.py \
	--sigmf_address /home/nasim/Downloads/neu_m046p309d/UAV-Sigmf-float16/ \
	--mat_address /home/nasim/Downloads/neu_m046p309d/mat_files/ \
 	--pkl_path /home/nasim/Downloads/neu_m046p309d/pkls_new/ \
	--symbolic_class_name 'uav' \
	--num_classes 7 \
  	--distance_list '6ft,9ft,12ft,15ft' \
  	--symbolic_transmitter_sigmf_key 'UAV' \
	
- python -u path_to_preprocess.py
- **sigmf_address**: Path where the meta-data is stored. This path is used in the code to associate the label (transmitter symbolic name) with each transmission.
- **mat_address**: Path where all the .mat files containing transmissions are saved.
- **pkl_path**: Path where the 4 .pkl files that are the output of preprocess.py script, are written.
- **symbolic_class_name**: This is an optional argument. If your .mat files follow the aforementioned naming convention, please provide this input related to the first name part before the first `_`. In the case of UAV dataset, where the a sample file name is uav1_etc.mat, this argument is set as `uav`.
- **num_classes**: Number of transmitters to be fingerprinted.
- **distance_list**: This is an optional argument. If the .mat files follow the aforementioned naming convention, please provide this input.
- **symbolic_transmitter_sigmf_key**: In the meta-data file, this key stores the symbolic transmitter name (e.g., uav7 or uav3).

**Note**: For the labels to be correctly associated, each .mat file and its corresponding meta-data files should have the same name. For example, `uav2_12ft_124.mat` and `uav2_12ft_124.json` are associated with each other.

The preprocessing step generates 4 pickle files:

1. `Partition.pkl`: Contains train/val/test partitions which are lists of paths to the corresponding `.mat` files.
2. `stats.pkl`: Contains information about the dataset including mean and standard deviation of the training set.
3. `label.pkl`: Contains a dictionary that associates each mat file with a device name (class name).
4. `device_ids.pkl`: Contains a dictionary that associates each device name with a class index.

These files should all be located in a folder, whose path is an input to the DLFramework.
