#!/usr/bin/env python3
"""FRZ1R: own halo-model implementation of form B's redistribution R_cold(k, z) (READING.md, 5daab3b12c).
Written independently; CFG556's numerical settings (EH no-wiggle shape, Tinker 08/10, Moster stars, beta gas, turnaround,
spectrum formulas) re-implemented from its definitions, nothing imported. Usage: nice -n 19 python3 frz1r_hm.py <foot>
kappa = 1/2 FITTED; not theory closed. Adopts nothing."""
import os, sys, json, math
import numpy as np
from scipy.optimize import brentq
from scipy.integrate import quad
HERE = os.path.dirname(os.path.abspath(__file__))
FOOT = sys.argv[1]; assert FOOT in ("canonical", "alt")
h = 0.6736; ob, oc = 0.02237, 0.1200; Om = (ob + oc) / h ** 2; OL = 1 - Om; FB = ob / (ob + oc)
G = 4.30091e-9; RHO = Om * 2.77536627e11
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}[FOOT] * 3.0856775814913673e22 / 1e6   # (km/s)^2 / Mpc
VST = {"canonical": 265.8, "alt": 288.1}[FOOT]
X0 = {"canonical": 59.486, "alt": 59.503}[FOOT]; X1 = {"canonical": 55.716, "alt": 55.731}[FOOT]

def tf_eh(k):  # Eisenstein & Hu 1998 zero-baryon-wiggle fit, k in 1/Mpc
    obh = ob; omh = Om * h * h; fb = obh / omh
    s = 44.5 * math.log(9.83 / omh) / math.sqrt(1 + 10 * obh ** 0.75)
    ag = 1 - 0.328 * math.log(431 * omh) * fb + 0.38 * math.log(22.3 * omh) * fb ** 2
    gam = Om * h * (ag + (1 - ag) / (1 + (0.43 * k * s) ** 4))
    q = k * (2.7255 / 2.7) ** 2 / (gam * h)
    L = np.log(2 * math.e + 1.8 * q); C = 14.2 + 731 / (1 + 62.5 * q)
    return L / (L + C * q * q)
KL = np.geomspace(1e-5, 100, 40000)
def wth(x): return 3 * (np.sin(x) - x * np.cos(x)) / x ** 3
PK0 = KL ** 0.965 * tf_eh(KL * h) ** 2
PK0 *= 0.811 ** 2 / (np.trapz(PK0 * wth(KL * 8) ** 2 * KL ** 2, KL) / (2 * math.pi ** 2))
def growth(z):
    E = lambda a: math.sqrt(Om / a ** 3 + OL)
    g = lambda a: E(a) * quad(lambda b: 1 / (b * E(b)) ** 3, 0, a, epsabs=0, epsrel=1e-10)[0]
    return g(1 / (1 + z)) / g(1.0)
LM = np.linspace(8, 16, 321); MM = 10 ** LM; DLN = (LM[1] - LM[0]) * math.log(10)
RL = (3 * MM / (4 * math.pi * RHO)) ** (1 / 3)
SIG0 = np.array([math.sqrt(np.trapz(PK0 * wth(KL * R) ** 2 * KL ** 2, KL) / (2 * math.pi ** 2)) for R in RL])
KK = np.geomspace(1e-3, 10.0, 260)
mn = lambda x: np.log1p(x) - x / (1 + x)
def j0sum(r, M, k):
    dM = np.diff(M); rm = 0.5 * (r[1:] + r[:-1]); x = np.outer(k, rm)
    return M[0] + (np.sinc(x / math.pi)) @ dM

def model(z, X=None, a0scale=True, variant="L"):
    D = growth(z); sig = SIG0 * D; zp = 1 + z
    Omz = Om * zp ** 3 / (Om * zp ** 3 + OL); OLz = 1 - Omz
    alpha = 10 ** (-(0.75 / math.log(200 / 75)) ** 1.2)
    A, a, b, c = 0.186 * zp ** -0.14, 1.47 * zp ** -0.06, 2.57 * zp ** -alpha, 1.19
    fsig = A * ((sig / b) ** -a + 1) * np.exp(-c / sig ** 2)
    dls = np.gradient(np.log(sig), LM * math.log(10))
    W = fsig * RHO / MM * (-dls) * DLN
    y = math.log10(200); nu = 1.686 / sig
    A10 = 1 + 0.24 * y * math.exp(-(4 / y) ** 4); a10 = 0.44 * y - 0.88; C10 = 0.019 + 0.107 * y + 0.19 * math.exp(-(4 / y) ** 4)
    bias = 1 - A10 * nu ** a10 / (nu ** a10 + 1.686 ** a10) + 0.183 * nu ** 1.5 + C10 * nu ** 2.4
    amiss = 1 - np.sum(W * bias * MM) / RHO
    dta = 5.55 + (11.81 - 5.55) * OLz / OL
    a0c = A0 / zp ** 2 if a0scale else A0
    XX = X if X is not None else (X0 if z < 1 else X1)
    Ustd = np.empty((len(MM), len(KK))); ULta = np.empty_like(Ustd); UB = np.empty_like(Ustd); URb = np.empty_like(Ustd)
    Mta_all = np.empty(len(MM)); chk = []
    for i, M in enumerate(MM):
        cc = 10.14 * (M / 2e12) ** -0.081 * zp ** -1.01; r200 = (3 * M / (4 * math.pi * 200 * RHO)) ** (1 / 3); rs = r200 / cc; mc = mn(cc)
        ML = lambda r: M * mn(np.asarray(r) / rs) / mc
        xta = brentq(lambda x: mn(cc * x) / mc / x ** 3 - dta / 200, 1.0, 50.0, xtol=1e-13); rta = xta * r200; Mta = float(ML(rta))
        xc = brentq(lambda x: mn(cc * x) / mc / x ** 3 - 1 / Omz, 0.05, 1.0, xtol=1e-13); R2c = xc * r200; M2c = float(ML(R2c))
        Mta_all[i] = Mta
        rr = np.concatenate([[0.0], np.geomspace(1e-4 * r200, r200, 1600)]); Ustd[i] = j0sum(rr, ML(rr), KK)
        vv = math.sqrt(zp * G * M2c / R2c)
        if vv <= VST:   # galaxy regime, Lagrangian scope (variant V: virial scope)
            cold = (1 - FB) * (Mta if variant != "V" else M)
            Mb = cold / XX; rM = math.sqrt(G * Mb * h / a0c); rt = rM * math.sqrt(XX * (XX + 1))
            r = np.unique(np.concatenate([[0.0], np.geomspace(1e-4 * r200, rta, 2000), [min(rt, rta)]]))
            x = r / rM; ph = np.where(r <= rt, Mb * (0.5 + np.sqrt(0.25 + x * x) - 1), cold)
            ph[0] = 0.0; rem = cold - ph[-1]
            refsh = ML(r) / Mta
            if variant == "shell":
                MB = Mb + ph + (Mta - Mb - cold) * refsh; MB[-1] += rem
            else:
                MB = Mb + ph + (Mta - Mb - cold + rem) * refsh
            MR = Mb + (Mta - Mb) * refsh
        else:           # group / cluster regime, R200c scope
            r = np.unique(np.concatenate([[0.0], np.geomspace(1e-4 * r200, rta, 2000), [R2c]]))
            Mbs = FB * M2c; share = (1 - FB) * M2c
            ms = min(M2c / h * 2 * 0.0351 / ((M2c / h / 10 ** 11.59) ** -1.376 + (M2c / h / 10 ** 11.59) ** 0.608) * h, Mbs); mg = Mbs - ms
            ah = 0.015 * R2c / (1 + math.sqrt(2)); rcg = 0.1 * R2c; ru = np.minimum(r, R2c)
            hs = lambda q: q ** 2 / (q + ah) ** 2; gb = lambda q: q / rcg - np.arctan(q / rcg)
            mb = ms * hs(ru) / hs(R2c) + mg * gb(ru) / gb(R2c)
            fcore = 0.5 * (1 - (VST / vv) ** 2); E = (1 - fcore) * share
            Wv = 1.5 * vv ** 2 / (1.5 * vv ** 2 + 15.0 ** 2)
            with np.errstate(divide="ignore", invalid="ignore"):
                yy = G * mb * h / (r ** 2 * a0c); nuy = 0.5 + np.sqrt(0.25 + 1 / yy)
                ph = np.where(r > 0, Wv * mb * (nuy - 1), 0.0)
            ph = np.minimum(np.maximum.accumulate(np.nan_to_num(ph)), E)
            iso = (E - ph[-1]) * r / rta
            outer = np.maximum(ML(r) - M2c, 0.0)
            MB = mb + fcore * share * ML(ru) / M2c + ph + iso + outer
            MR = mb + (1 - FB) * ML(ru) + outer
        for Mc in (MB, MR):
            chk.append(max(abs(Mc[-1] / Mta - 1), float(max(0.0, -np.diff(Mc).min()) / Mta)))
        UB[i] = j0sum(r, MB, KK); URb[i] = j0sum(r, MR, KK)
        rl = np.concatenate([[0.0], np.geomspace(1e-4 * r200, rta, 2000)]); ULta[i] = j0sum(rl, ML(rl), KK)
    PL = np.interp(np.log(KK), np.log(KL), PK0) * D ** 2
    norm = np.sum(W * bias * Mta_all) / RHO
    def Pstd(U):
        return np.sum(W[:, None] * (U / RHO) ** 2, 0) + PL * (np.sum(W[:, None] * bias[:, None] * U / RHO, 0) + amiss) ** 2
    def Pta(U):
        return np.sum(W[:, None] * (U / RHO) ** 2, 0) + PL * (np.sum(W[:, None] * bias[:, None] * U / RHO, 0) / norm) ** 2
    ps, pl = Pstd(Ustd), Pta(ULta)
    Rt = 1 + (Pta(UB) - pl) / ps; Rb = 1 + (Pta(URb) - pl) / ps
    return dict(z=z, D=D, R_cold=(Rt / Rb).tolist(), R_tot=Rt.tolist(), R_bar=Rb.tolist(), conserve_max=float(max(chk)))

ZB = [round(2.2 + 0.2 * i, 1) for i in range(12)]
out = dict(lane="FRZ1R", footing=FOOT, k=KK.tolist(), note="kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
def at(R, k): return float(np.interp(math.log(k), np.log(KK), R))
out["z0"] = model(0.0)
print(FOOT, "z0 R_cold k1/3/5:", [round(at(out["z0"]["R_cold"], k), 4) for k in (1, 3, 5)], "conserve", out["z0"]["conserve_max"], flush=True)
for var in ("L", "V", "shell"):
    out[var] = {}
    for z in ZB:
        m = model(z, variant=var); out[var][f"{z:.1f}"] = m
        print(FOOT, var, z, "D %.4f" % m["D"], "R_cold k1/3/5:", [round(at(m["R_cold"], k), 4) for k in (1, 3, 5)], "cons %.1e" % m["conserve_max"], flush=True)
    if FOOT == "alt" and var == "L": pass
mu = model(3.0, a0scale=False)
out["MUTATE_a0_unscaled_z3"] = mu
d = at(mu["R_cold"], 3) - at(out["L"]["3.0"]["R_cold"], 3)
print(FOOT, "MUTATE a0 unscaled z 3: R_cold k3 %.4f vs %.4f, change %+.4f -> %s" % (at(mu["R_cold"], 3), at(out["L"]["3.0"]["R_cold"], 3), d, "bites" if abs(d) >= 0.005 else "DOES NOT BITE"), flush=True)
out["MUTATE_bites"] = bool(abs(d) >= 0.005); out["MUTATE_change"] = d
json.dump(out, open(os.path.join(HERE, f"frz1r_hm_{FOOT}.json"), "w"))
