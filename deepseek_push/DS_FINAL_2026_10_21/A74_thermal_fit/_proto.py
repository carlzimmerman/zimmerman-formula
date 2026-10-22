import os, sys, math, glob, json, time
import numpy as np
from scipy.optimize import brentq, minimize, minimize_scalar
from scipy.special import gammainc
from scipy.interpolate import CubicSpline

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))

G_N = 6.67430e-11
C_L = 2.99792458e8
MSUN = 1.98847e30
PC = 3.0856775814913673e16
KPC = 1e3 * PC
MPC = 1e6 * PC
ARCSEC = math.pi / (180.0 * 3600.0)
H0_KMS = 67.4
H0_SI = H0_KMS * 1e3 / MPC
OMEGA_L = 0.6847
RHO_CRIT = 3.0 * H0_SI ** 2 / (8.0 * math.pi * G_N)
SQ_8PI3 = math.sqrt(8.0 * math.pi / 3.0)
A0_PER_KAPPA = C_L * H0_SI / SQ_8PI3
LN10 = math.log(10.0)
LAMBDA_OBS = 1.0890e-52

SPARC_DIR = os.path.join(REPO, "real_research", "data", "sparc_data")
SPARC_FILES = sorted(glob.glob(os.path.join(SPARC_DIR, "*_rotmod.dat")))
GAL = []
for f in SPARC_FILES:
    a = np.loadtxt(f, comments="#")
    if a.ndim != 2 or len(a) < 5:
        continue
    GAL.append(dict(name=os.path.basename(f)[:-len("_rotmod.dat")],
                    r=a[:, 0] * KPC, V=a[:, 1], eV=a[:, 2],
                    Vg=a[:, 3], Vd=a[:, 4], Vb=a[:, 5]))
NG = len(GAL)
NPT = int(sum(len(g["r"]) for g in GAL))
print("SPARC", len(SPARC_FILES), NG, NPT)

UG = np.geomspace(0.05, 2.5, 240)
FLOOR = 0.05


def chi2_sparc(a0, gals=None, ug=UG, floor=FLOOR):
    gals = GAL if gals is None else gals
    tot = 0.0
    for g in gals:
        s2 = g["eV"] ** 2 + (floor * g["V"]) ** 2
        Vb2 = (g["Vg"] ** 2)[None, :] + ug[:, None] * (g["Vd"] ** 2 + g["Vb"] ** 2)[None, :]
        gN = Vb2 * 1e6 / g["r"][None, :]
        Vp = np.sqrt(0.5 * gN * (1.0 + np.sqrt(1.0 + 4.0 * a0 / np.maximum(gN, 1e-30)))
                     * g["r"][None, :]) / 1e3
        c = np.sum((g["V"][None, :] - Vp) ** 2 / s2[None, :], axis=1)
        tot += float(c.min())
    return tot


t0 = time.time()
for _ in range(3):
    chi2_sparc(1.132e-10)
print("3 chi2_sparc calls: %.2f s" % (time.time() - t0))
