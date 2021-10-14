# DataFactory

## SigMF
Signal Metadata Format is a way to form and share datasets in the wireless communications community. https://www.gnuradio.org/grcon/grcon17/presentations/sigmf/Ben-Hilburn-SigMF.pdf

In SigMF, each recorded signal is stored in the form of interleaved IQ values with desired data type and length in .bin files. Each .bin file is accompanied by a .json file, containing meta-data about the recorded signal. The meta-data include information about the waveform, data collection environment and tools, etc.,

### Converting complex signal sequences to SigMF

### Converting SigMF .bin files to complex signal sequences

## Deep Learning Framework

### Preprocessing
Preprocessing is preparing the already collected dataset for being fed to the neural network. 
Preprocessing consists of a series of steps such as:
1. Partitioning the dataset to training, validation, and test sets. 
2. Calculating mean and standard deviation of the training set, which is later used for z-score standardization.
3. Creating training and test true labels for each signal.

Before running the preprocessing script, we need to make sure that each signal is stored as a complex sequence with dimensions (1,N) (where N is the number of I/Q samples in the signal, and can be different for different signals) in one single folder. Each example should be named as devicename_A_B_etc.mat. During preprocessing device labels are infered from the first element before '_'.

### Running the framework
The ML framework consists of python code that loads the data and 
