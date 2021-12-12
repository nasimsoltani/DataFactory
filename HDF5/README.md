This code implements conversion from multimodal data folder to a single file as portable `HDF5` format.

## HDF5
Hierarchical Data Format is a way to form and share different types of data. In this particular repository we concentrate on generating and reading HDF5 files from a folder which contains data from different modalities of the same scenario (or environment).

In this specific example, each folder contains 2 LiDAR, 2 camera image and 1 GPS sensor information with RF ground truth data.

## Code description:

This repository have two code stucture:

1. `Generate_HDF5_Dataset.py`: to generate the hdf5 files from the folder containing multimodal data samples.
2. `Read_HDF5_Dataset.py`: to read the generated hdf5 files.


## Multimodal input folder structure
Sample_folder
	|
	|---Sensors
	|---Label
	|---Metadata.txt

The metadata file can be in a separate folder location as well, the absolute path of the metadata file is given in the hdf5 generation code. A sample folder is uploaded in the repository as `Multimodal_dataset_samples`.


### Running the code:

The hdf5 generation code is run through the `run_generate.sh` script that sends 4 input arguments to `Generate_HDF5_Dataset.py`: 

    --destination_dir      # Path to the directory that contains or will contain the hdf5 files.
    --source_dir	           # Path to the directory that contains the multimodal input folder.
    --metadata_file_path       # Path to the directory that contains the metadata file name.
    --hdf5_file_name      # The file name of generated HDF5 file.

The code to read the generated hdf5 file is run through the `run_read.sh` script that sends 1 input arguments to `Read_HDF5_Dataset.py`: 

    --hdf5_file_path       # Path to the hdf5 file.


### Example
The code can be run as it is to generate multimodal dataset shared in the hdf5 format here: https://genesys-lab.org/hovering-uavs to .hdf files.
To run the code, the dataset should be download and the appropriate path to the dataset folder should be provided in the `run_generate.sh` and `run_read.sh` script.
After editing the paths in the `run.sh` script, run appropriate scripts for hdf5 generation or reading as:
	./run_generate.sh
	./run_read.sh
