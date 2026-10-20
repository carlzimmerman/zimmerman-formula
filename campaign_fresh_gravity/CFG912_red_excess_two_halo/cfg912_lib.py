"""CFG912 shared definitions (criteria FROZEN_CRITERIA.md, 96de8091f).  kappa = 1/2 FITTED; not theory closed.

Imports CFG903's cfg903_lib read-only (paths, distances, catchment fixed point, d/M_b cells, watchdog) and defines this lane's
x = d / rho_l binning, lens-mass cells, colour/isolation classes and the jackknife coarse cells.
"""
import math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
D903 = os.path.abspath(os.path.join(HERE, "..", "CFG903_framework_two_halo_kids"))
sys.path.insert(0, D903)
import cfg903_lib as L                                   # read-only import (never edited)

L.LIM_RSS, L.LIM_T = 1.2e9, 19.5 * 60                    # criteria: < 1.2 GB current RSS, < 20 min per process
WORK = os.path.join(L.EXT, "cfg912_work")
WORK903 = L.WORK

# ------------------------------------------------------------------ B21 RAR g_bar bins (criteria: g_k = 10^(-15 + 0.246606 k))
DLG = 0.246606
GK = 10.0 ** (-15.0 + DLG * np.arange(16))               # 16 edges, 15 bins
G_REF = float(GK[10])                                    # rho_l = sqrt(G M_l / g_10)
KB = np.arange(5, 14)                                    # bins computed (k = 5..13)
G_SI, MSUN, MPC = 6.674e-11, 1.989e30, L.Mpc_m
PC_M = 3.0857e16
ESD_UNIT = MSUN / PC_M ** 2                              # kg/m^2 per Msun/pc^2

def rho_Mpc(Mgal):                                       # physical Mpc (h70^-1), the radius where g_bar = g_10
    return np.sqrt(G_SI * np.asarray(Mgal, float) * MSUN / G_REF) / MPC

# ------------------------------------------------------------------ x bins: log, 0.0246606 dex, annulus edges on bin edges
DX = DLG / 10.0
I_LO, I_HI = -101, 88                                    # fine log edges x_i = 10^(DX i), i = I_LO..I_HI; bin 0 = [0, x_{I_LO})
NX = 1 + (I_HI - I_LO)                                   # 190
X_EDGES = np.concatenate([[0.0], 10.0 ** (DX * np.arange(I_LO, I_HI + 1))])   # len NX + 1
def xbin_of(x):
    x = np.asarray(x, float)
    i = np.floor(np.log10(np.maximum(x, 1e-300)) / DX + 1e-9).astype(np.int64)
    return np.where(x < X_EDGES[1], 0, np.clip(i - I_LO + 1, 1, NX - 1))
def X_of_k(k):                                           # X edge of g_k: sqrt(g_10 / g_k) = 10^(-5 DX (k - 10))
    return 10.0 ** (-5 * DX * (np.asarray(k) - 10))
def i_of_k(k):                                           # fine-edge index of X_k
    return -5 * (np.asarray(k) - 10)
for _k in range(5, 15):
    assert abs(X_EDGES[i_of_k(_k) - I_LO + 1] / X_of_k(_k) - 1) < 1e-12

# coarse x bins for the jackknife: 5 fine bins each, coarse edges on the annulus edges (fine index multiple of 5)
NXC = 39
def xc_of_xb(xb):
    xb = np.asarray(xb)
    i = I_LO + xb - 1                                    # lower fine-edge index of fine bin xb (xb >= 1)
    return np.where(xb == 0, 0, (i + 105) // 5)
XC_EDGES = np.concatenate([[0.0], 10.0 ** (DX * (5 * np.arange(1, NXC + 1) - 105))])   # coarse c covers [XC_EDGES[c], XC_EDGES[c+1])

# ------------------------------------------------------------------ lens-mass cells (0.1 dex in log M_gal) and neighbour cells
LM_LO, LM_DL, NLM = 9.3, 0.1, 18
LM_CEN = LM_LO + LM_DL * (np.arange(NLM) + 0.5)
def lm_of(logMgal):
    return np.clip(np.floor((np.asarray(logMgal) - LM_LO) / LM_DL).astype(np.int64), 0, NLM - 1)
NM_OFF, NNM = 30, 90                                     # main cells = CFG903 mbin_of - 30 (log M_b 8.5 .. 13.0)
NM_CEN = L.M_CEN[NM_OFF:NM_OFF + NNM]
NNMC = 23                                                # jackknife: 0.2 dex (4 main cells)
NWB = 3                                                  # |dchi| bins [0,300) [300,500) [500,1000)
WB_EDGES = np.array([300.0, 500.0])

# ------------------------------------------------------------------ classes: iso3 (I1 | I0 - I1 | I5 - I0) x colour3 (<=2.0 | 2.0-2.5 | >2.5)
NCLS = 9
def colour3(ur):
    ur = np.asarray(ur, float)
    return np.where(ur > 2.5, 2, np.where(ur > 2.0, 1, 0))
def iso3(I0, I1, I5):
    assert not np.any(I1 & ~I0) and not np.any(I0 & ~I5)
    return np.where(I1, 0, np.where(I0, 1, 2))

SHAPE_MAIN = (NCLS, NLM, NX, NNM, 2, NWB)
SHAPE_JK = (L.NPATCH, 3, NLM, NXC, NNMC, 2)

# ------------------------------------------------------------------ MUTATE injection (criteria; MUTATE-B per AMENDMENT_A1.md)
_MM = os.environ.get("CFG912_MUTATE", "")
MUT_MODE = "B" if _MM == "B" else ("A" if _MM == "1" else "")          # A = frozen MUTATE (d 0.4 Mpc), B = A1 (d 0.01 Mpc)
MUT_SFX = {"": "", "A": "_MUTATE", "B": "_MUTATE_B"}[MUT_MODE]
INJ_LOGMB, INJ_EVERY, INJ_LOGMS = 11.325, 10, 7.5
INJ_D = 0.01 if MUT_MODE == "B" else 0.4
