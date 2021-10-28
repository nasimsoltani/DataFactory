import numpy as np
import matlab.engine

def initMatlabEngine(paths=[]):
    """
    This method initialize Matlab engine and add the corresponding list of paths to the Matlab environment
    :param paths: a list of paths pointing to directories with Matlab code
    :return: the engine object
    """
    eng = matlab.engine.start_matlab()
    for p in paths:
        eng.addpath(p, nargout=0)
    return eng

def genScatMIMOChannel(eng, txarray, rxarray, Nscatter, lam):
    """
    This method generates a scattering channel matrix using Matlab's Phased Array Toolbox functions.

    :param eng: Matlab engine object. Needs to be initialized externally to this function
    :param txarray: Transmitter array object, generated through Phased Array Toolbox
    :param rxarray: Receiver array object, generated through Phased Array Toolbox
    :param Nscatter: Num. of scatterers to be considered in the scattering MIMO channel generation
    :param lam: lambda, i.e. wavelength
    :return: The channel matrix H converted in Numpy ndarray format
    """

    # set the tx and rx individual antennas positions
    txpos = eng.rdivide(  # basically a./b
        eng.getElementPosition(txarray),
        lam
    )
    rxpos = eng.rdivide(
        eng.getElementPosition(rxarray),
        lam
    )

    # generate transmission angles
    txang = eng.minus(
        eng.times(
            eng.rand(1, Nscatter),
            eng.double(60)
        ),
        eng.double(30)
    )  # txang = [rand(1,Nscatter)*60-30];

    rxang = eng.minus(
        eng.times(
            eng.rand(1, Nscatter),
            eng.double(180)
        ),
        eng.double(90)
    )  # rxang = [rand(1,Nscatter)*180-90];

    # generate the random channel gains for each scatterer
    g = eng.rdivide(
        eng.complex(
            eng.randn(1, Nscatter),
            eng.randn(1, Nscatter)
        ),
        eng.sqrt(eng.double(Nscatter))
    )

    H = eng.scatteringchanmtx(txpos, rxpos, txang, rxang, g)

    return np.array(H), H, txang, rxang