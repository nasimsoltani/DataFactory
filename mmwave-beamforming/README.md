Please use below the link to download the datasets: 
Dataset#1 (Wood): https://repository.library.northeastern.edu/files/neu:gm80mq018
Dataset#2 (Card box): https://repository.library.northeastern.edu/files/neu:gm80mp942


Extracting the data from hdf5 files:

One can use “Extract_from_hdf5.py” to extract the images and labels from hdf5 files.
Run: python Extract_from_hdf5.py “path_to_hdf5_file”  “path_to_cloned_directory”


Running the framework: One can use our framework by running a sequence of 5 Python files.

Detection stage:
1. Run: python stride.py “path_to_cloned_directory”
2. Run: python move_to_antenna.py “path_to_cloned_directory”
3. Run the main script as follows (this step takes time, we recommend running it in a bash script): python main.py --base_path “path_to_cloned_directory“ train True --test True  --restore_models False --wall_model_path “the_path_to_save_model” --wall_model_json “the_path_to_model_json_file” --wall_model_weight “the_path_to_restore_model_weights” --path_of_entire_image “path_to_images_folder_for_prediction” --epochs 4

Prediction stage:
1. Run: generate_pickle.py  “path_to_cloned_directory” to generate the pickle file of bit maps and their labels:
2. Run: prediction.py
