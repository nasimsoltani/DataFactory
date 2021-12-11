# Matlab interface for Python
MATLAB Engine API for Python starts a MATLAB session out-of-process, which executes MATLAB as a separate process. You can use MATLAB Engine API for Python to call built-in or user-written MATLAB functions.
The API provided simplifies the setup and launch of Matlab engine package in a Python script. The purpose of this API is to provide a powerful interface between Matlab, often used to simulate wireless standards, transmissions through wireless channel models, generate standard compliant waveforms etc. and easily pass data between Matlab and Python, a more popular tool in for the Machine Learning and Deep Learning research community. For more insights on the functionalities of Matlab engine package for Python, please refer to the official Mathworks documentation available here: https://www.mathworks.com/help/matlab/matlab-engine-for-python.html
## Setup
First, we need to compile and install the Matlab engine Python package in the desired Python environment. Run these commands in a Linux/MacOS shell:
```
$MATROOT = /usr/local/MATLAB/R2021b   # Matlab root folder. Change accordingly if a different version is installed or root directory is different
$PYENV = ~/anaconda3/envs/py3         # Python environment where you want to install the package.

cd $MATROOT/extern/engines/python
python setup.py install --prefix=$PYENV
```
This should compile and setup the Matlab engine package for Python. Note that if you want to install Python package in the default system environment, you can install without the `--prefix` argument. For other OSs and additional instructions, please refer to the official guide at https://www.mathworks.com/help/matlab/matlab_external/install-the-matlab-engine-for-python.html

## Usage of `matutils` package
After Matlab package is compiled, we can start the Matlab engine within a Python script with the following command:
```
import matutils

path_list = [
    r'~/Documents/MATLAB/Examples/R2021b/phased/HybridPrecodingExample'
]

eng = matutils.initMatlabEngine(paths=path_list)

```
Note that the `paths` argument is needed if we want to add user-defined functions or include helpers from Matlab's Examples, like in this case.

Once the engine is started, it is possible to launch any Matlab function within Python with the following syntax:
```
out1, ..., outN = eng.<matlab_function_name>(<arg1>,<arg2>, nargout=N)
```
Note that the number of output arguments must be known in advance to avoid errors when using the Matlab engine. Moreover, the argument passed as input to a Matlab function must be cast to a Matlab compatible type through the dedicated cast functions. Finally, the matrix operators are not automatically overloaded in Python as in Matlab, so to perform a specific operation we need to refer to the full function name of the desired operation. For more info, refer to the official documentation https://www.mathworks.com/help/matlab/matlab_oop/implementing-operators-for-your-class.html#br02znk-6 

## Example: scattering MIMO channel matrix generation

We provide a Python [example script](matutils.py) that showcases the use of Matlab engine to generate scattering MIMO channel matrices for mmWave bands. This example can be useful to understand the mechanics of the input/output arguments casting from Matlab to Python and vice-versa.


