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
2. Run the code in SigMF folder with instructions in the corresponding `README.md` to generate `.mat` files out of the downloaded dataset. 
3. Run the code in the preprocessing folder with instructions in the corresponding `README.md` to generate 4 `.pkl` files, which are the input to the deep learning framework. 
4. Run the code in the DLFramework folder with instructions in the corresponding `README.md`.
