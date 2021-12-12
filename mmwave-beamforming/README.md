# Dataset:
Please find below the link to download the datasets: 

Dataset#1 (Wood): https://repository.library.northeastern.edu/files/neu:gm80mq018

Dataset#2 (Card box): https://repository.library.northeastern.edu/files/neu:gm80mp942

These datasets were used for the paper "Machine Learning on Camera Images for Fast mmWave Beamforming", IEEE MASS 2020. Any use of this dataset, which results in an academic publication or other publication that includes a bibliography, should contain a citation to our paper. Here is the reference for the work: 

B. Salehi, M. Belgiovine, S. Garcia Sanchez, J. Dy, S. Ioannidis, K. Chowdhury, "Machine Learning on Camera Images for Fast mmWave Beamforming" IEEE MASS, 10-13 December 2020, Delhi NCR, India.

# Pre-requisites

- Python 3.8.3

- Keras 2.4.3 

- tensorflow 2.2.0

# Extracting the data from hdf5 files:

One can use “Extract_from_hdf5.py” to extract the images and labels from hdf5 files.

Run: python Extract_from_hdf5.py “path_to_hdf5_file”  “path_to_cloned_directory”



# Running the framework: 
One can use our framework by running a sequence of 5 Python files. For information about each stage, please refer to the paper. 

## Detection stage:

1. Run: python stride.py “path_to_cloned_directory”
2. Run: python move_to_antenna.py “path_to_cloned_directory”
3. Run the main script as follows (this step takes time, we recommend running it in a bash script):

  python main.py --base_path “path_to_cloned_directory“ --train True --test True  --restore_models False --wall_model_path “the_path_to_save_model” --wall_model_json   “the_path_to_model_json_file” --wall_model_weight “the_path_to_restore_model_weights” --path_of_entire_image ”Entire_Image_original" --epochs 4

## Prediction stage:

1. Run: python generate_pickle.py  “path_to_cloned_directory”
2. Run: python prediction.py
