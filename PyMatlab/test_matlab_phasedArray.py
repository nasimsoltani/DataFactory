import matutils
import numpy as np
import pickle
import matplotlib.pyplot as plt

path_list = [
    r'/home/mauro/Documents/MATLAB/Examples/R2020a/phased/HybridPrecodingExample'
]

eng = matutils.initMatlabEngine(path_list)

# setup simulation parameters

Nt = 8          # N. of TX antennas
NtRF = 1        # N. of TX RF-chains

Nr = 4          # N. of RX antennas
NrRF = 1        # N. of RX RF-chains

c = 3e8         # speed of light
fc = 28e9       # central frequency (in Hz)
lam = c/fc      # lambda (i.e. wavelength)

Ncl = 6                 # num. of ray clusters
Nray = 8                # num. of rays per cluster
Nscatter = Nray*Ncl     # num. of scattering objects
angspread = 5           # angle spread

Ns=1

TX_cb = eng.dftmtx(Nt)
RX_cb = eng.dftmtx(Nr)

txarray = eng.phased.PartitionedArray(
    'Array', eng.phased.ULA('NumElements', eng.double(Nt), 'ElementSpacing', lam/2),
    'SubarraySelection', eng.ones(NtRF, Nt),
    'SubarraySteering', 'Custom'
)
rxarray = eng.phased.PartitionedArray(
    'Array', eng.phased.ULA('NumElements', eng.double(Nr), 'ElementSpacing', lam/2),
    'SubarraySelection', eng.ones(NrRF, Nr),
    'SubarraySteering', 'Custom'
)

txpos = eng.rdivide(eng.getElementPosition(txarray), lam)
rxpos = eng.rdivide(eng.getElementPosition(rxarray), lam)

n_channels = 100

cb_angle_TX = eng.findCBAngles(TX_cb, eng.double(fc), eng.double(c), True)
cb_angle_RX = eng.findCBAngles(RX_cb, eng.double(fc), eng.double(c), True)
N_angles_TX = 60  # (-30, 30)
N_angles_RX = 180  # (-90, 90)



#coords_H = pickle.load(open('H_samples.pkl','rb'))


#coords_H = [[0]*(N_angles_RX+1)]*(N_angles_TX+1)    # 2D list, dims -> (N_angles_TX, N_angles_RX)
coords_H = [[{'H': []} for rx in range(N_angles_RX+1)] for tx in range(N_angles_TX+1)]

for h in range(n_channels):
    if (h % 10 ) == 0:
        print('generating chan', h)
    H, Hmat, txang, rxang = matutils.genScatMIMOChannel(eng, txarray, rxarray, Nscatter, lam)

    snr_dB = -5
    snr = 10**(snr_dB/10)
    Fopt, Wopt = eng.helperOptimalHybridWeights(Hmat, eng.double(NrRF), eng.double(1/snr), nargout=2)


    Frf2, Fbb2, Wrf2, Wbb2, best_prec_ix, best_comb_ix = eng.bestHybridCodes(Hmat, eng.double(NrRF), TX_cb, RX_cb, eng.double(NtRF), eng.double(NrRF), eng.double(snr), nargout=6)

    At = eng.steervec(txpos, txang)
    Ar = eng.steervec(rxpos, rxang)
    Fbb, Frf, Wbb, Wrf = eng.omphybweights(Hmat, eng.double(Ns), eng.double(NtRF),
                                                   At, eng.double(NrRF), Ar, eng.double(1 / snr),
                                                   nargout=4)

    OMP_TX_bestangle = eng.findCBAngles(eng.transpose(Frf), eng.double(fc), eng.double(c), True)
    OMP_RX_bestangle = eng.findCBAngles(Wrf, eng.double(fc), eng.double(c), True)


    # insert matrix H in matrix lists
    coords_H[int(OMP_TX_bestangle - 60)][int(OMP_RX_bestangle)]['H'].append(H)

pickle.dump(coords_H, open('H_samples.pkl', 'wb'))
