import math
import numpy as np
from scipy.integrate import quad
from scipy.interpolate import RegularGridInterpolator
from scipy.ndimage import gaussian_filter

C_LIGHT = 2.99792458e8; G = 6.67430e-11; MSUN = 1.98847e30
PC = 3.0856775814913673e16; MPC = 1.0e6 * PC
SIG_UNIT = MSUN / PC ** 2
A0 = 9.36e-11
Rc = np.load("Rc_fine.npy"); zc = np.load("zc_fine.npy"); Rf = np.load("Rf_fine.npy")
Cq = np.load("Cq_fine.npy"); Ca = np.load("Ca_fine.npy")
S_Q = -0.280594; S_A = -0.229815

LRG = dict(M=10 ** 11.3 * MSUN, d=8.23 / 0.7 * MPC, z=0.42, sigma_crit=1640.0, n_src=11.0,
           n_pairs=23000, area=154.0)
SIGMA_E = 0.26


def abel(x, col, Rc):
    if x < 1e-9:
        return 2.0 * np.sum(col * np.diff(np.concatenate([[0.0], Rc])))
    umax = math.acosh(max(Rc[-1] / x, 1.0001))
    us = np.linspace(0.0, umax, 2001)
    Rs = x * np.cosh(us)
    fs = np.interp(Rs, Rc, col, left=col[0], right=0.0)
    return 2.0 * x * np.sum(fs * np.cosh(us)) * (us[1] - us[0])


def forecast(C, S_inf, smooth=0.0):
    if smooth > 0:
        C = gaussian_filter(C, smooth / (Rc[1] - Rc[0]))
    xs = np.concatenate([[0.0], np.geomspace(0.01, 1.4, 53)])
    zrows = [j for j in range(len(zc)) if zc[j] < 0.16]
    D = np.zeros((len(zrows), len(xs)))
    for a, j in enumerate(zrows):
        col = np.minimum(C[:, j], 0.0)
        D[a, :] = [-abel(x, col, Rc) for x in xs]
    D0 = D[0, 0]
    A_eff = 4.0 * float(np.trapz(np.trapz((D / D0) ** 2, xs, axis=1), zc[zrows]))
    d = LRG["d"]
    unit_col = math.sqrt(G * LRG["M"] * A0) / (G * d)
    dsig = abs(S_inf) * unit_col / SIG_UNIT
    def DA(z, Om=0.3, h=0.7):
        dc = (C_LIGHT / 1000.0) / (100.0 * h) * quad(lambda x: 1 / math.sqrt(Om * (1 + x) ** 3 + 1 - Om), 0, z)[0]
        return dc / (1 + z)
    DA_ = DA(LRG["z"]); amp = 60.0 * (180.0 / math.pi) / DA_
    A_arcmin2 = A_eff * (d / MPC) ** 2 * amp ** 2
    S1 = dsig * math.sqrt(LRG["n_src"] * A_arcmin2) / (SIGMA_E * LRG["sigma_crit"])
    return dict(A_eff=A_eff, A_arcmin2=A_arcmin2, dsig=dsig, S1=S1, N3=(3 / S1) ** 2,
                N5=(5 / S1) ** 2, deg2_3=(3 / S1) ** 2 / (LRG["n_pairs"] / LRG["area"]),
                D0=D0, prof=[(x, float(np.interp(x, xs, D[0]) / D0)) for x in (0.0, 0.02, 0.05, 0.1, 0.2, 0.3, 0.5)])


print("QUMOND", forecast(Cq, S_Q))
print("QUMOND sm", forecast(Cq, S_Q, 0.01))
print("AQUAL", forecast(Ca, S_A))
print("AQUAL sm", forecast(Ca, S_A, 0.01))
