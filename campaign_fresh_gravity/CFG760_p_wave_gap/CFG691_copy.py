"""Copy of CFG691's SPARC statistic (cfg691.py G-GAL block, read-only data via CFG4_common). Used by CFG760 G3; checked by K5."""
import os, sys, math

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import CFG4_common as C4  # noqa: E402

G, KPC_S = 6.6743e-11, 3.0857e19
GAL = C4.load_sparc()
NG = len(GAL)
UPS = np.round(np.arange(0.30, 1.2001, 0.01), 2)
Rm = np.concatenate([g["R"] for g in GAL]) * KPC_S
Vo = np.concatenate([g["Vobs"] for g in GAL]); eV = np.concatenate([g["eV"] for g in GAL])
Vg = np.concatenate([g["Vgas"] for g in GAL]); Vd = np.concatenate([g["Vdisk"] for g in GAL]); Vb = np.concatenate([g["Vbul"] for g in GAL])
GI = np.concatenate([np.full(len(g["R"]), i) for i, g in enumerate(GAL)])
VB2 = np.sign(Vg)[:, None] * Vg[:, None] ** 2 + UPS[None, :] * Vd[:, None] ** 2 + 1.4 * UPS[None, :] * Vb[:, None] ** 2
GB = VB2 * 1e6 / Rm[:, None]
GO = ((Vo * 1e3) ** 2 / Rm)[:, None] * np.ones_like(GB)
OK = (GB > 0) & (GO > 0) & np.isfinite(GB) & np.isfinite(GO) & (Vo > 0)[:, None]
WPT = 1.0 / (np.clip(eV, 1, None) / np.clip(Vo, 1, None)) ** 2
WW = np.where(OK, WPT[:, None], 0.0)
last = np.array([np.where(GI == i)[0][-1] for i in range(NG)])
MB = np.clip(VB2[last] * 1e6 * Rm[last, None] / G, 1e30, None)
RM_G = np.sqrt(G * MB / 1.0)


def _S_of(s, sol):
    s = np.asarray(s, float)
    out = np.empty_like(s)
    lo, hi = s < 1e-4, s > 1e4
    mid = ~(lo | hi)
    out[lo] = s[lo] * 0.5
    out[hi] = 1 - 1 / s[hi]
    out[mid] = s[mid] * sol.sol(np.log(s[mid]))[0]
    return out


def sparc_fit(a0, Lstar, sol):
    with np.errstate(all="ignore"):
        gb = np.where(OK, GB, 1.0)
        boost = np.sqrt(a0 / gb)
        if Lstar > 0:
            ell = Lstar ** 2 / (2 * RM_G[GI] / math.sqrt(a0))
            boost = boost * _S_of((Rm[:, None] / ell).ravel(), sol).reshape(ell.shape)
        r_ = np.log10(np.where(OK, GO, 1.0)) - np.log10(np.where(OK, (1 + boost) * gb, 1.0))
    mse = (WW * r_ ** 2).sum(0) / WW.sum(0)
    i = int(np.argmin(mse))
    return math.sqrt(mse[i]), float(UPS[i])
