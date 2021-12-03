# Data Factory

## RF fingerprinting example

### Pre-requisites
GPU is required.
The code is tested to work with:
- Python 2.7.16
- Keras 2.2.4
- tensorflow 1.12

### Running
For running an example RF fingerprinting on the UAV dataset 3 steps should be followed:

1. Download the dataset from here: https://genesys-lab.org/hovering-uavs
2. Modify the SigMF script (with paths on your system), as mentioned in the corresponding `readme.md` to generate `.mat` files out of the downloaded dataset. Run the script.
3. Modify the preprocessing script (with paths on your system), as mentioned in the corresponding `readme.md` to generate 4 `.pkl` files, which are the input to the deep learning framework. Run the script.
4. Modify the `run.sh` file inside `DLFramework` (with paths on your system), as mentioned in the corresponding `readme.md`. Run the script.

