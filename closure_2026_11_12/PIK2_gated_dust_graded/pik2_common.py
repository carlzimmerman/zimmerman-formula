#!/usr/bin/env python3
"""PIK2 common definitions (criteria 95edd35e0b): gate family, constants, footings, thresholds.
kappa = 1/2 FITTED; not theory closed. Adopts nothing."""
import os, json, math
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
G = 6.674e-11; C = 2.99792458e8; MS = 1.989e30; KPC = 3.0857e19; MPC = 3.0857e22; C_KMS = 299792.458
FOOT = ("canonical", "alt")
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
LSTAR_PC = {"canonical": 21.7, "alt": 22.9}            # QX17 section 3 (record's Lstar per footing)
H_LIT = 0.674                                          # MK1 / KD1 background h
# KD1 (kd1.json at 7172d3dd4f, read-only copy of the values used): I0 [Mpc^-2], mu_B1a, mu_B1b, Omega_r
KD1 = {"canonical": dict(I0=4.0369171448880406e-08, mu_B1a=198.254232363749, mu_B1b=8890113.53538235, Omega_r=9.19627543683481e-05),
       "alt": dict(I0=4.0365356641010055e-08, mu_B1a=198.24486482353313, mu_B1b=8889273.437013572, Omega_r=9.198461433064905e-05)}
MU_J = 25118.864315095823                              # KD1 G9a / QX3 iter2 Jeans line (MK1 grade json)
XSHARE = {"canonical": 59.486123673272104, "alt": 59.50285020948403}   # ONE1 one1.json X (PD1 share)
MU_SPARC = {"canonical": 7.07945784384142, "alt": 5.623413251903491}    # MK1 row 5 upper bounds (5.62 = 10^0.75)
MU_KIDS = {"canonical": 1.0, "alt": 0.7652}                             # MK1 row 6 upper bounds
MU_LIST = lambda f: {"primary_Jeans": MU_J, "secondary_B1a": KD1[f]["mu_B1a"], "reported_BBN": KD1[f]["mu_B1b"]}
LOGXI = np.round(np.arange(-2.0, 12.0001, 0.05), 2)
NOTE = "kappa = 1/2 FITTED; not theory closed. Adopts nothing."


def rho_d0(f):
    """cosmic mean dust mass density today, rho_d0 = I0 c^2 / (8 pi G) [kg/m^3] (I0 in Mpc^-2)."""
    return KD1[f]["I0"] / MPC ** 2 * C ** 2 / (8 * math.pi * G)


# gate family: S(u), S'(u), S''(u) for u >= 0 (static rows); (s1, s2) at u = 0 (row 2)
def _E1(u): e = np.exp(-u); return e, -e, e
def _P(p):
    def f(u): return (1 + u) ** -p, -p * (1 + u) ** (-p - 1), p * (p + 1) * (1 + u) ** (-p - 2)
    return f
def _F2(u): e = np.exp(-u * u); return e, -2 * u * e, (4 * u * u - 2) * e
def _F3(u): e = np.exp(-u ** 3); return e, -3 * u * u * e, (9 * u ** 4 - 6 * u) * e
def _R3(u):
    d = 1 + u ** 3; return 1 / d, -3 * u * u / d ** 2, (18 * u ** 4 / d ** 3 - 6 * u / d ** 2)
def _ST(u): s = np.where(u < 1.0, 1.0, 0.0); return s, np.zeros_like(s), np.zeros_like(s)
GATES = {"E1": (_E1, (-1, 1)), "P1": (_P(1), (-1, 2)), "P2": (_P(2), (-2, 6)), "P4": (_P(4), (-4, 20)),
         "F2": (_F2, (0, -2)), "F3": (_F3, (0, 0)), "R3": (_R3, (0, 0)), "ST": (_ST, (0, 0))}
GRADED = list(GATES)


def band(b):
    def f(u):
        s = np.where(u < 1, 1.0, np.where(u < 3, 0.0, np.where(u < 30, 10.0 ** -b, 0.0))); z = np.zeros_like(s); return s, z, z
    return f


def S_eval(name, u, mut=None):
    u = np.maximum(np.asarray(u, float), 0.0)
    if mut == "M-S1": o = np.ones_like(u); return o, 0 * o, 0 * o
    if mut == "M-SIGN": e = np.exp(np.minimum(u, 700.0)); return e, e, e
    if name.startswith("BAND"): return band(int(name[4:]))(u)
    with np.errstate(over="ignore", under="ignore", invalid="ignore"):
        return GATES[name][0](u)


def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, np.ndarray): return clean(o.tolist())
    if isinstance(o, (np.floating, float)): return float(o) if np.isfinite(o) else None
    if isinstance(o, np.integer): return int(o)
    if isinstance(o, np.bool_): return bool(o)
    return o
# kappa = 1/2 FITTED; not theory closed. Adopts nothing.
