#!/usr/bin/env python3
"""FRZ3 layout module. The halo layout of rule 5 at redshift z is COPIED from FRZ1R's frz1r_hm.py (its CFG556 numerics:
EH no-wiggle at sigma8 0.811, Tinker 2008 with z-scaling, Tinker 2010 bias, Duffy c(M, z), Moster stars, beta gas,
Delta_ta(z) interpolation, PD1 share at z 1), with FRZ1's conventions restored where the two lanes differ:
  - primary galaxy remainder laid out isothermally (rem * r / r_ta), FRZ1's convention ("L");
  - FRZ1R's remainder convention (remainder in the reference NFW shape) is the bracket "remnfw";
  - FRZ1's reading V (virial scope, gal_scope = "vir", its own Rb) is the bracket "V".
This module only builds profiles; the point of FRZ3 is the flux step. kappa = 1/2 FITTED; not theory closed. Adopts nothing."""
import math
import numpy as np
from scipy.optimize import brentq
from scipy.integrate import quad

h = 0.6736; ob, oc = 0.02237, 0.1200; Om = (ob + oc) / h ** 2; OL = 1 - Om; FB = ob / (ob + oc)
G = 4.30091e-9; RHO = Om * 2.77536627e11
A0SI = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
A0 = {f: A0SI[f] * 3.0856775814913673e22 / 1e6 for f in A0SI}          # (km/s)^2 / Mpc
VST = {"canonical": 265.8, "alt": 288.1}
X0 = {"canonical": 59.486, "alt": 59.503}; X1 = {"canonical": 55.716, "alt": 55.731}

def tf_eh(k):  # Eisenstein & Hu 1998 zero-baryon-wiggle fit, k in 1/Mpc
    obh = ob; omh = Om * h * h; fb = obh / omh
    s = 44.5 * math.log(9.83 / omh) / math.sqrt(1 + 10 * obh ** 0.75)
    ag = 1 - 0.328 * math.log(431 * omh) * fb + 0.38 * math.log(22.3 * omh) * fb ** 2
    gam = Om * h * (ag + (1 - ag) / (1 + (0.43 * k * s) ** 4))
    q = k * (2.7255 / 2.7) ** 2 / (gam * h)
    L = np.log(2 * math.e + 1.8 * q); C = 14.2 + 731 / (1 + 62.5 * q)
    return L / (L + C * q * q)
KL = np.geomspace(1e-5, 300, 40000)
def wth(x): return 3 * (np.sin(x) - x * np.cos(x)) / x ** 3
PK0 = KL ** 0.965 * tf_eh(KL * h) ** 2
PK0 *= 0.811 ** 2 / (np.trapz(PK0 * wth(KL * 8) ** 2 * KL ** 2, KL) / (2 * math.pi ** 2))
def plin(k, z): return np.interp(np.log(k), np.log(KL), PK0) * growth(z) ** 2
_GC = {}
def growth(z):
    if z in _GC: return _GC[z]
    E = lambda a: math.sqrt(Om / a ** 3 + OL)
    g = lambda a: E(a) * quad(lambda b: 1 / (b * E(b)) ** 3, 0, a, epsabs=0, epsrel=1e-10)[0]
    _GC[z] = g(1 / (1 + z)) / g(1.0); return _GC[z]
def Ez(z): return math.sqrt(Om * (1 + z) ** 3 + OL)
LM = np.linspace(8, 16, 321); MM = 10 ** LM; DLN = (LM[1] - LM[0]) * math.log(10)
RL = (3 * MM / (4 * math.pi * RHO)) ** (1 / 3)
SIG0 = np.array([math.sqrt(np.trapz(PK0 * wth(KL * R) ** 2 * KL ** 2, KL) / (2 * math.pi ** 2)) for R in RL])
mn = lambda x: np.log1p(x) - x / (1 + x)
def j0sum(r, M, k):
    dM = np.diff(M); rm = 0.5 * (r[1:] + r[:-1]); x = np.outer(k, rm)
    return M[0] + (np.sinc(x / math.pi)) @ dM

def build(z, foot, KU, mmin_bracket=1e10, a0scale=True):
    """Per-halo-mass profiles U(k) (Fourier transform of the cumulative mass, U(0) = M_ta) on KU for:
    R (reference Rb, Lagrangian scope), L (rule 5, primary), remnfw (FRZ1R remainder), RV / V (FRZ1 virial scope)."""
    D = growth(z); sig = SIG0 * D; zp = 1 + z
    Omz = Om * zp ** 3 / (Om * zp ** 3 + OL); OLz = 1 - Omz
    alpha = 10 ** (-(0.75 / math.log(200 / 75)) ** 1.2)
    A, a, b, c = 0.186 * zp ** -0.14, 1.47 * zp ** -0.06, 2.57 * zp ** -alpha, 1.19
    fsig = A * ((sig / b) ** -a + 1) * np.exp(-c / sig ** 2)
    dls = np.gradient(np.log(sig), LM * math.log(10))
    W = fsig * RHO / MM * (-dls) * DLN                     # number density per bin, (Mpc/h)^-3
    y = math.log10(200); nu = 1.686 / sig
    A10 = 1 + 0.24 * y * math.exp(-(4 / y) ** 4); a10 = 0.44 * y - 0.88; C10 = 0.019 + 0.107 * y + 0.19 * math.exp(-(4 / y) ** 4)
    bias = 1 - A10 * nu ** a10 / (nu ** a10 + 1.686 ** a10) + 0.183 * nu ** 1.5 + C10 * nu ** 2.4
    dta = 5.55 + (11.81 - 5.55) * OLz / OL
    a0c = A0[foot] / zp ** 2 if a0scale else A0[foot]
    XX = X0[foot] if z < 1 else X1[foot]
    out = {v: np.empty((len(MM), len(KU))) for v in ("R", "L", "remnfw", "RV", "V", "std", "Lta")}
    Mta_all = np.empty(len(MM)); rta_all = np.empty(len(MM)); regime = []; chk = []
    for i, M in enumerate(MM):
        cc = 10.14 * (M / 2e12) ** -0.081 * zp ** -1.01; r200 = (3 * M / (4 * math.pi * 200 * RHO)) ** (1 / 3); rs = r200 / cc; mc = mn(cc)
        ML = lambda r: M * mn(np.asarray(r) / rs) / mc
        xta = brentq(lambda x: mn(cc * x) / mc / x ** 3 - dta / 200, 1.0, 50.0, xtol=1e-13); rta = xta * r200; Mta = float(ML(rta))
        xc = brentq(lambda x: mn(cc * x) / mc / x ** 3 - 1 / Omz, 0.05, 1.0, xtol=1e-13); R2c = xc * r200; M2c = float(ML(R2c))
        Mta_all[i] = Mta; rta_all[i] = rta
        rr = np.concatenate([[0.0], np.geomspace(1e-4 * r200, r200, 1600)]); out["std"][i] = j0sum(rr, ML(rr), KU)
        rl = np.concatenate([[0.0], np.geomspace(1e-4 * r200, rta, 2000)]); out["Lta"][i] = j0sum(rl, ML(rl), KU)
        vv = math.sqrt(zp * G * M2c / R2c)
        prof = {}
        if vv <= VST[foot]:
            regime.append("galaxy")
            for scope in ("lag", "vir"):
                Rs, Ms = (rta, Mta) if scope == "lag" else (r200, M)
                Mcold = (1 - FB) * Ms; Mb = Mcold / XX; rM = math.sqrt(G * Mb * h / a0c); rt = rM * math.sqrt(XX * (XX + 1))
                r = np.unique(np.concatenate([[0.0], np.geomspace(1e-4 * r200, rta, 2000), [min(rt, Rs), Rs]])); r = r[r <= rta * (1 + 1e-14)]
                rin = np.minimum(r, Rs); shape = ML(rin) / Ms; outside = np.where(r > Rs, ML(r) - Ms, 0.0)
                unc = (FB * Ms - Mb) * shape
                ph = np.minimum(Mb * (np.sqrt(0.25 + (rin / rM) ** 2) - 0.5), Mcold); ph[0] = 0.0
                rem = max(Mcold - float(np.interp(Rs, r, ph)), 0.0)
                if scope == "lag":
                    prof["R"] = (r, Mb + Mcold * shape + unc + outside)
                    prof["L"] = (r, Mb + ph + rem * rin / Rs + unc + outside)
                    prof["remnfw"] = (r, Mb + ph + rem * shape + unc + outside)
                else:
                    prof["RV"] = (r, Mb + Mcold * shape + unc + outside)
                    prof["V"] = (r, Mb + ph + rem * rin / Rs + unc + outside)
        else:
            regime.append("cluster")
            r = np.unique(np.concatenate([[0.0], np.geomspace(1e-4 * r200, rta, 2000), [R2c]]))
            Mbs = FB * M2c; share = (1 - FB) * M2c
            ms = min(M2c / h * 2 * 0.0351 / ((M2c / h / 10 ** 11.59) ** -1.376 + (M2c / h / 10 ** 11.59) ** 0.608) * h, Mbs); mg = Mbs - ms
            ah = 0.015 * R2c / (1 + math.sqrt(2)); rcg = 0.1 * R2c; ru = np.minimum(r, R2c)
            hs = lambda q: q ** 2 / (q + ah) ** 2; gb = lambda q: q / rcg - np.arctan(q / rcg)
            mb = ms * hs(ru) / hs(R2c) + mg * gb(ru) / gb(R2c)
            fcore = min(max(0.5 * (1 - (VST[foot] / vv) ** 2), 0.0), 1.0); E = (1 - fcore) * share
            Wv = 1.5 * vv ** 2 / (1.5 * vv ** 2 + 15.0 ** 2)
            with np.errstate(divide="ignore", invalid="ignore"):
                ph = np.where(r > 0, Wv * (np.sqrt(0.25 * mb ** 2 + mb * r ** 2 * a0c / (G * h)) - 0.5 * mb), 0.0)
            ph = np.minimum(np.maximum.accumulate(np.nan_to_num(ph)), E)
            iso = max(E - ph[-1], 0.0) * r / rta
            outer = np.maximum(ML(r) - M2c, 0.0)
            MB = mb + fcore * share * ML(ru) / M2c + ph + iso + outer
            MR = mb + (1 - FB) * ML(ru) + outer
            prof = dict(R=(r, MR), L=(r, MB), remnfw=(r, MB), RV=(r, MR), V=(r, MB))
        for v, (r, Mc) in prof.items():
            chk.append(max(abs(Mc[-1] / Mta - 1), float(max(0.0, -np.diff(Mc).min()) / Mta)))
            out[v][i] = j0sum(r, Mc, KU)
    return dict(z=z, D=D, W=W, bias=bias, Mta=Mta_all, rta=rta_all, regime=regime, U=out, conserve_max=float(max(chk)),
                amiss=1 - float(np.sum(W * bias * MM)) / RHO, norm=float(np.sum(W * bias * Mta_all)) / RHO, mmin=mmin_bracket)

def halo_model_Rcold(B, KU, var="L", ref="R"):
    """FRZ1R's halo-model ratio R_cold = R_tot / R_bar (its formula, copied), for check b0 against FRZ1's stored R_cold."""
    W, bias, U = B["W"], B["bias"], B["U"]; PL = plin(KU, B["z"])
    def Pstd(Uu): return np.sum(W[:, None] * (Uu / RHO) ** 2, 0) + PL * (np.sum(W[:, None] * bias[:, None] * Uu / RHO, 0) + B["amiss"]) ** 2
    def Pta(Uu): return np.sum(W[:, None] * (Uu / RHO) ** 2, 0) + PL * (np.sum(W[:, None] * bias[:, None] * Uu / RHO, 0) / B["norm"]) ** 2
    ps, pl = Pstd(U["std"]), Pta(U["Lta"])
    return (1 + (Pta(U[var]) - pl) / ps) / (1 + (Pta(U[ref]) - pl) / ps)
