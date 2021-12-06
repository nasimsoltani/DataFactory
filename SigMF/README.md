## SigMF
Signal Metadata Format is a way to form and share datasets in the wireless communications community. https://www.gnuradio.org/grcon/grcon17/presentations/sigmf/Ben-Hilburn-SigMF.pdf

In SigMF, each recorded signal is stored in the form of interleaved IQ values with desired data type and length in .bin files. Each .bin file is accompanied by a .json file, containing meta-data about the recorded signal. The meta-data include information about the waveform, data collection environment and tools, etc.,

## Description:

This code implements:

1. Converting from .mat files to the SigMF for sharing purposes.
2. Converting from .bin files (SigMF) to .mat files for (neural network) processing purposes.

### Running the code:

The code is run through the `run.sh` script that sends 3 input arguments to `sigmf_converter.py`: 

    --sigmf_path      # Path to the directory that contains or will contain binary (SigMF) files.
    --mat_path        # Path to the directory that contains or will contain .mat files.
    --conversion      # A switch that indicates we would want to run SigMF to mat conversion (sigmf2mat) or vice-versa (mat2sigmf). 

### Requirements
For the code to run as it is, all the source files need to be uniquely named and be located flat in a directory without sub-directories.
The convert_bin_to_mat() function converts all the binary files in the source directory to complex sequences of values with size (1,L), which will later be read by the neural network.
