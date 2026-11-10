#!/usr/bin/env python3
"""GRW1 observables: CMB-lensing Limber ratio with a k- and z-dependent ratio (GAL1's kernel), the PR4 amplitude and shape
rules, sigma8 / S8, f sigma8 (baryon velocity), the L346 forest band. Criteria 11c19a2c5f section 2.
Read-only reuse: QX3 iter2 (run_class, X_of; PR4 via cfg917_lib), SV5 sv5_t0.json, QX3 iter2.json. Adopts nothing.
kappa = 1/2 FITTED; not theory closed.
"""
import os, sys, io, json, math, contextlib
import numpy as np
from scipy.interpolate import RegularGridInterpolator
import grw1_lib as GL

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
I2D = os.path.join(REPO, "closure_2026_11_06", "QX3_cmb_growth", "iter2_kq_dust")
sys.path.insert(0, I2D)
with contextlib.redirect_stdout(io.StringIO()):
    import iter2 as I2                                   # loads PR4 (cfg917_lib) at import
LIB, DPR4 = I2.LIB, I2.D
h = GL.h
ML = I2.run_class(GL.OB, GL.OD, GL.H0, GL.NS, pk=True)   # the reference with lensing (GAL1's M)
X0 = I2.X_of(ML)

def amp_fit(X):
    """GAL1's PR4 best amplitude rule (QX3 iter2 best_amp_chi2), with its error and the refitted chi^2."""
    u = LIB.wsum(DPR4["W"], X) + LIB.wsum(DPR4["M"], X)
    a = LIB.qform(u, DPR4["Cinv"], DPR4["d"] + DPR4["F"]); b = LIB.qform(u, DPR4["Cinv"]); A = a / b
    r = A * u - DPR4["F"] - DPR4["d"]
    return dict(A=A, sig_abs=1.0 / math.sqrt(b), chi2_refit=LIB.qform(r, DPR4["Cinv"]), u=u)
FX0 = amp_fit(X0); AX0 = FX0["A"]; SIGREL = FX0["sig_abs"] / AX0; CHI2_X0 = FX0["chi2_refit"]
SV5 = json.load(open(os.path.join(REPO, "closure_2026_11_06", "SV5_growth_mechanism", "sv5_t0.json")))
IT2 = json.load(open(os.path.join(I2D, "iter2.json")))
CHI2_REC = max(IT2["G1"], key=lambda r: r["chi2_min"])["chi2_min"]
LINE_L1 = 2 * SIGREL
DESI = [("BGS", 0.295, 0.80, 0.20, 0.20, 0.84, 0.19, 0.19), ("LRG1", 0.510, 1.09, 0.12, 0.14, 1.16, 0.13, 0.13),
        ("LRG2", 0.706, 1.05, 0.12, 0.12, 1.04, 0.11, 0.092), ("LRG3", 0.919, 0.96, 0.11, 0.10, 0.997, 0.10, 0.084)]  # GAL1 / CE2
S8LINE = 2 * 0.0225 / 0.759
KFOREST = np.geomspace(1.10, 3.56, 6) * h                 # L346's band, h/Mpc -> 1/Mpc
ZFOREST = (2.0, 3.0); ZFOREST_REP = (4.0,)

# ------------------------------------------------------------------ Limber (GAL1's standard kernel)
ZSTAR = 1089.0; CHIS = ML.angular_distance(ZSTAR) * (1 + ZSTAR)
zg = np.concatenate([np.linspace(1e-4, 6.5, 3251), np.geomspace(6.5, ZSTAR, 801)[1:-1], [ZSTAR * (1 - 1e-9)]])
chi = np.array([ML.angular_distance(z) * (1 + z) for z in zg])
LG = np.unique(np.concatenate([np.round(np.geomspace(2, 2500, 400)).astype(int), [100, 200, 300, 400]])).astype(float)
KT = np.geomspace(1e-5, 10.0, 320); ZT = np.unique(np.concatenate([np.linspace(0, 7, 141), np.linspace(7, 20, 53)]))
LPT = np.log(np.array([[ML.pk_lin(k, z) for z in ZT] for k in KT]))
PINT = RegularGridInterpolator((np.log(KT), ZT), LPT, bounds_error=False, fill_value=None)
D20 = ML.scale_independent_growth_factor(20.0)
def Pk(k, z):
    k = np.asarray(k, float); out = np.zeros_like(k); m = (k >= KT[0]) & (k <= KT[-1])
    if m.any():
        zz = min(z, 20.0); out[m] = np.exp(PINT(np.column_stack([np.log(k[m]), np.full(m.sum(), zz)])))
        if z > 20.0: out[m] *= (ML.scale_independent_growth_factor(z) / D20) ** 2
    return out
KER = ((1 + zg) * (CHIS - chi) / CHIS) ** 2
KLZ = (LG[:, None] + 0.5) / chi[None, :]                 # (nL, nz)
PM = np.array([Pk(KLZ[:, j], z) for j, z in enumerate(zg)]).T
TW = np.zeros_like(chi); dchi = np.diff(chi); TW[:-1] += 0.5 * dchi; TW[1:] += 0.5 * dchi
KMAT = PM * (KER * TW)[None, :]
DEN = KMAT.sum(axis=1)

def _expand(s):
    Lall = np.arange(LIB.LMAX + 1.0); S = np.ones(LIB.LMAX + 1)
    S[2:] = np.interp(np.log(Lall[2:]), np.log(LG), s); return S
def S_of_z(Rz):
    """z-only ratio R(z) on zg (GAL1's S_of), S = C_L[R]/C_L[1]."""
    return _expand((KMAT * (Rz ** 2)[None, :]).sum(axis=1) / DEN)
def ratio_interp(ratio, zgrid, kgrid=GL.KGRID):
    """ratio(k, z) table on (kgrid, zgrid ascending) -> function of (k array, z array); clamped at the edges (criteria 1.5)."""
    zi = np.asarray(zgrid); o = np.argsort(zi)
    F = RegularGridInterpolator((np.log(kgrid), zi[o]), ratio[:, o], bounds_error=False, fill_value=None)
    def f(k, z):
        lk = np.clip(np.log(k), math.log(kgrid[0]), math.log(kgrid[-1])); zz = np.clip(z, zi.min(), zi.max())
        return F(np.column_stack([lk.ravel(), zz.ravel()])).reshape(np.shape(k))
    return f
def S_of_kz(rfun):
    """S(L) for a power ratio R_P(k, z) (already squared), applied inside the Limber integral."""
    R = rfun(KLZ, np.broadcast_to(zg[None, :], KLZ.shape))
    return _expand((KMAT * R).sum(axis=1) / DEN)
def X_abs():
    H0c = ML.Hubble(0.0); OMCL = (GL.OB + GL.OD) / h ** 2
    C = 4.0 / (LG + 0.5) ** 4 * (1.5 * OMCL * H0c ** 2) ** 2 * DEN
    return dict(zip(LG.astype(int), (LG * (LG + 1)) ** 2 * C / (2 * math.pi)))
def lensing(S):
    fit = amp_fit(S * X0)
    return dict(r_eff=float(AX0 / fit["A"]), dchi2=float(fit["chi2_refit"] - CHI2_X0), chi2_abs=float(fit["chi2_refit"]),
                S_L={str(L): float(S[L]) for L in (100, 200, 400)},
                bins=[float(x) for x in (fit["u"] / FX0["u"])])

# ------------------------------------------------------------------ sigma8, f sigma8, forest
KS = np.geomspace(1e-4, 10.0, 1200); R8 = 8.0 / h
def W2(k, R): x = k * R; return (3 * (np.sin(x) - x * np.cos(x)) / x ** 3) ** 2
_LKS = np.log(KS); _WKS = np.gradient(_LKS)
def sigma2(P, R=R8):
    return float(np.sum(_WKS * KS ** 3 * P * W2(KS, R)) / (2 * math.pi ** 2))
PREF = {z: Pk(KS, z) for z in [0.0] + [d[1] for d in DESI]}
def interp_k(ratio_k):
    return np.interp(np.log(np.clip(KS, GL.KGRID[0], GL.KGRID[-1])), np.log(GL.KGRID), ratio_k)
def zindex(zarr, z):
    j = int(np.argmin(np.abs(zarr - z))); assert abs(zarr[j] - z) < 1e-6, (z, zarr[j]); return j

kappa_note = "kappa = 1/2 FITTED; not theory closed. Adopts nothing."
