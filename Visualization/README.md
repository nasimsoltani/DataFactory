This code implements conversion from `.mat` files to `SigMF`, and conversion from `SigMF` to `.mat` files.

## SigMF
Signal Metadata Format is a way to form and share datasets in the wireless communications community. https://www.gnuradio.org/grcon/grcon17/presentations/sigmf/Ben-Hilburn-SigMF.pdf

In SigMF, each recorded signal is stored in the form of interleaved IQ values with desired data type and length in .bin files. Each .bin file is accompanied by a .json file, containing meta-data about the recorded signal. The meta-data include information about the waveform, data collection environment and tools, etc.,

## Code description:

This code implements two functions:

1. convert_mat_to_sigmf() to convert .mat files to the SigMF for sharing purposes.
2. convert_bin_to_mat() to convert .bin files (SigMF) to .mat files with size (1,L), where L is the length of each complex signal.

### Running the code:

The code is run through the `run.sh` script that sends 3 input arguments to `sigmf_converter.py`: 

    --sigmf_path      # Path to the directory that contains or will contain binary (SigMF) files.
    --mat_path        # Path to the directory that contains or will contain .mat files.
    --conversion      # A switch that indicates we would want to run SigMF to mat conversion (sigmf2mat) or vice-versa (mat2sigmf). 

### Example
The code can be run as it is to convert dataset shared in the sigmf format here: https://genesys-lab.org/hovering-uavs to .mat files.
To run the code, the dataset should be download and the appropriate path to the dataset folder should be provided in the `run.sh` script.
After editing the paths in the `run.sh` script, run `sigmf_converter.py` as:
        
        ./run.sh
