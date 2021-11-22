## SigMF
Signal Metadata Format is a way to form and share datasets in the wireless communications community. https://www.gnuradio.org/grcon/grcon17/presentations/sigmf/Ben-Hilburn-SigMF.pdf

In SigMF, each recorded signal is stored in the form of interleaved IQ values with desired data type and length in .bin files. Each .bin file is accompanied by a .json file, containing meta-data about the recorded signal. The meta-data include information about the waveform, data collection environment and tools, etc.,

## Running the code:

This code implements:

1. Converting from .mat files to the SigMF for sharing purposes.
2. Converting from .bin files (SigMF) to .mat files for (neural network) processing purposes.

### Inputs

The code takes 3 inputs: 

1. 
