"""CFG230 kernels: P2, simple and a transcription of the CFG44 nu_mono construction (rebuilt from its description, not imported)."""
import math
import numpy as np
from scipy.optimize import brentq

def nu_p2(y): y = np.maximum(np.asarray(y, float), 1e-300); return np.sqrt(1.0 + 1.0 / y)
def nu_simple(y): y = np.maximum(np.asarray(y, float), 1e-300); return 0.5 + np.sqrt(0.25 + 1.0 / y)
def h_rar(y):
    y = np.asarray(y, float)
    with np.errstate(over="ignore"):
        return np.where(y < 1e4, y / np.expm1(np.sqrt(np.minimum(y, 1e4))), 0.0)
def dh_rar(y, e=1e-6): return (h_rar(y * (1 + e)) - h_rar(y * (1 - e))) / (2 * y * e)
Y_P = brentq(lambda y: float(dh_rar(y)), 1.0, 5.0); H_P = float(h_rar(Y_P))
LYG = np.linspace(-14, 14, 280001); YG = 10 ** LYG
DH = np.maximum(dh_rar(YG), 0.05 * H_P / (YG + Y_P))
HM = float(h_rar(YG[0])) + np.concatenate([[0.0], np.cumsum(0.5 * (DH[1:] + DH[:-1]) * np.diff(YG))])
def HMf(y): return np.interp(np.log10(np.maximum(y, 1e-14)), LYG, HM)
def DHf(y): return np.interp(np.log10(np.maximum(y, 1e-14)), LYG, DH)
def nu_mono(y): y = np.maximum(np.asarray(y, float), 1e-14); return 1.0 + HMf(y) / y
KERN = {"P2": nu_p2, "simple": nu_simple, "nu_mono": nu_mono}
