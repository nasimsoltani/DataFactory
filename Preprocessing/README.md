### Preprocessing

Preprocessing is preparing the already collected dataset for being fed to the neural network. 

Preprocessing consists of a series of steps such as:

1. Partitioning the dataset to training, validation, and test sets. 
2. Calculating mean and standard deviation of the training set, which is later used for z-score standardization.
3. Creating training and test true labels for each signal.

Before running the preprocessing script, the dataset must be saved in the form of `.mat` files in one folder on the hard storage. For the `.mat` files to be readable by the DLFramework, each signal (transmission) must be resized to (1,L) as a vector of L complex values. Each transmission should be named as devicename_A_B_etc.mat. During preprocessing device labels are infered from the first element before '_'.

The preprocessing step generates 4 pickle files:

1. `Partition.pkl`: Contains train/val/test partitions which are lists of paths to the corresponding `.mat` files.
2. `stats.pkl`: Contains information about the dataset including mean and standard deviation of the training set.
3. `label.pkl`: Contains a dictionary that associates each mat file with a device name (class name).
4. `device_ids.pkl`: Contains a dictionary that associates each device name with a class index.
