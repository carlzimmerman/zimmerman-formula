#!/usr/bin/env python3
"""
fire_common.py -- shared real-SPARC machinery for the fire_* deliverable scripts.
Lifted verbatim (same cuts, same fiducials, same estimator) from estimator_theory.py so
every fire script reproduces the banked derivation numbers from the raw data, not from a
cached json. READ-ONLY on the frozen repo.

Sample: SPARC Q<=2, inc>=30 deg, point cut eV/Vobs < 10% (Lelli+2017 standard).
Gas-dominated cut (POINT level, stated): Vgas^2 > Ud*Vdisk^2 + Ub*Vbul^2, Ub = 1.4*Ud.
Fiducial systematics (stated, not hidden):
  sigma_lnD by SPARC fD flag {1 Hubble-flow 25%, 2 TRGB 5%, 3 Cepheid 5%, 4 UMa 10%,
  5 SNIa 8%}; sigma_i = 3 deg; sigma_lnUpsilon = 0.23 (0.1 dex, GLOBAL); sigma_ln(gascal)
  = 0.10 (GLOBAL); per-point g_bar shape scatter 10%; intrinsic floor f_int*g_obs,model^2
  iterated to chi2/N = 1; estimator-choice spread |GLS - median|/2 as an extra line.
"""
import numpy as np, glob, os, csv, json

REPO = "/Users/carlzimmerman/new_physics/zimmerman-formula/real_research"
HERE = os.path.dirname(os.path.abspath(__file__))
LEDGER = "/Users/carlzimmerman/new_physics/prep_2026/concordance_ledger"
ANCHOR = json.load(open(os.path.join(LEDGER, "anchor_values.json")))
A0C, A0A = ANCHOR["a0_canon"], ANCHOR["a0_alt"]     # canonical 9.355e-11 / ALT 1.1305e-10
SC, SA = ANCHOR["sig_canon"], ANCHOR["sig_alt"]     # Planck anchor widths
ZVAL, HL = ANCHOR["Z"], ANCHOR["HL"]
A0_RARFIT = 1.2e-10                                  # McGaugh+2016 g_dagger, for comparison
CLIGHT = 2.99792458e8
kpc = 3.0857e19

SIG_LND = {1: 0.25, 2: 0.05, 3: 0.05, 4: 0.10, 5: 0.08}
SIG_INC = np.deg2rad(3.0)
SIG_LNU, SIG_LNG, SLNB = 0.23, 0.10, 0.10
FVCUT = 0.10

_meta = {}
with open(os.path.join(REPO, "data", "sparc_master_clean.csv")) as fh:
    for r_ in csv.DictReader(fh):
        _meta[r_["name"]] = dict(Q=int(r_["Q"]), inc=float(r_["inc"]),
                                 D=float(r_["D_Mpc"]), fD=int(r_["fD"]))
_cache = {}


def load(Ud):
    """Per-galaxy dicts at disk M/L Ud (bulge 1.4*Ud), SPARC-standard cuts applied."""
    key = round(float(Ud), 3)
    if key in _cache:
        return _cache[key]
    Ub = 1.4 * Ud
    gals = []
    for f in sorted(glob.glob(os.path.join(REPO, "data", "sparc_data", "*_rotmod.dat"))):
        name = os.path.basename(f).replace("_rotmod.dat", "")
        m = _meta.get(name)
        if m is None or m["Q"] > 2 or m["inc"] < 30:
            continue
        d = np.genfromtxt(f, comments="#")
        if d.ndim != 2 or d.shape[1] < 6:
            continue
        R, Vo, eV, Vg, Vd, Vb = (d[:, i] for i in range(6))
        gstar = (Ud * Vd**2 + Ub * Vb**2) * 1e6 / (R * kpc)
        ggas = np.sign(Vg) * Vg**2 * 1e6 / (R * kpc)
        gb, go = ggas + gstar, (Vo * 1e3) ** 2 / (R * kpc)
        fv = np.clip(eV, 1.0, None) / np.clip(Vo, 1, None)
        ok = (gb > 0) & (Vo > 0) & np.isfinite(gb) & np.isfinite(go) & (fv < FVCUT)
        if ok.sum() == 0:
            continue
        gals.append(dict(name=name, inc=np.deg2rad(m["inc"]), sig_lnD=SIG_LND[m["fD"]],
                         fD=m["fD"], R=R[ok], gb=gb[ok], go=go[ok], fv=fv[ok],
                         phi=(gstar / gb)[ok], gasdom=(ggas > gstar)[ok]))
    _cache[key] = gals
    return gals


def flat(gals, gas_only):
    GB, GO, FV, PHI, GAL, SLD, CTI = [], [], [], [], [], [], []
    for k, g in enumerate(gals):
        m = g["gasdom"] if gas_only else np.ones(len(g["gb"]), bool)
        n = int(m.sum())
        GB += list(g["gb"][m]); GO += list(g["go"][m]); FV += list(g["fv"][m])
        PHI += list(g["phi"][m]); GAL += [k] * n
        SLD += [g["sig_lnD"]] * n; CTI += [1 / np.tan(g["inc"])] * n
    return list(map(np.array, (GB, GO, FV, PHI, GAL, SLD, CTI)))


def sig2_model(GB, GOm2, FV, fint):
    """Model-based per-point variance of E = g_obs^2 - g_bar^2 (the honest weights)."""
    return (4 * GOm2 * FV) ** 2 + (2 * GB**2 * SLNB) ** 2 + (fint * GOm2) ** 2


def gls(GB, GO, FV, biased=False):
    """Iterated GLS through origin; biased=True reproduces the observed-weight trap."""
    E = GO**2 - GB**2
    a0, fint = 1e-10, 0.2
    c2n = np.inf
    for _ in range(300):
        GOm2 = (GO**2 if biased else GB**2 + a0 * GB)
        s2 = sig2_model(GB, GOm2, FV, fint)
        w = 1 / s2
        a0n = np.sum(w * E * GB) / np.sum(w * GB**2)
        c2n = float(np.mean((E - a0n * GB) ** 2 / s2))
        fint = max(0.01, fint * c2n**0.25)
        if abs(a0n - a0) < 1e-17 and abs(c2n - 1) < 1e-3:
            a0 = a0n; break
        a0 = a0n
    return a0, fint, c2n, w


def budget(gals, gas_only):
    """a0_hat + full systematic budget (per-galaxy D and i, global Upsilon/gascal,
    estimator-choice spread). Same algebra as estimator_theory.py S4."""
    GB, GO, FV, PHI, GAL, SLD, CTI = flat(gals, gas_only)
    if len(GB) < 10:
        return None
    a0, fint, c2n, w = gls(GB, GO, FV)
    med = float(np.median((GO**2 - GB**2) / GB))
    S = np.sum(w * GB**2)
    sig_stat = np.sqrt(1 / S)
    yq = GB / a0
    varD = varI = 0.0
    for k in set(GAL.tolist()):
        m = GAL == k
        cD = a0 * np.sum(w[m] * GB[m] ** 2 * 2 * (yq[m] + 1)) / S
        cI = a0 * np.sum(w[m] * GB[m] ** 2 * 4 * (yq[m] + 1) * CTI[m]) / S
        varD += (cD * SLD[m][0]) ** 2
        varI += (cI * SIG_INC) ** 2
    KU = np.sum(w * GB**2 * PHI * (2 * yq + 1)) / S
    KG = np.sum(w * GB**2 * (1 - PHI) * (2 * yq + 1)) / S
    sU, sG = KU * a0 * SIG_LNU, KG * a0 * SIG_LNG
    sEst = abs(a0 - med) / 2.0
    tot = np.sqrt(sig_stat**2 + varD + varI + sU**2 + sG**2 + sEst**2)
    return dict(N=int(len(GB)), Ngal=len(set(GAL.tolist())), a0hat=float(a0),
                a0med=med, fint=float(fint), stat=float(sig_stat),
                sysD=float(np.sqrt(varD)), sysI=float(np.sqrt(varI)),
                sysU=float(sU), sysG=float(sG), sysEst=float(sEst), tot=float(tot),
                phibar=float(np.sum(w * GB**2 * PHI) / S),
                ybar=float(np.sum(w * GB**2 * yq) / S))


def excess_model(gbv, s, kind):
    """Model excess E(g_bar) for each nu family, each in ITS OWN convention with its
    own scale s (the anti-conflation rule: rivals are always shown at their own best fit)."""
    yv = gbv / s
    if kind == "fw":                       # framework: nu = sqrt(1+1/y) -> E = s*g exactly
        return s * gbv
    if kind == "mcg":                      # McGaugh/RAR-fit: nu = 1/(1-exp(-sqrt(y)))
        return gbv**2 * (1.0 / (1.0 - np.exp(-np.sqrt(yv))) ** 2 - 1.0)
    if kind == "simple":                   # simple nu = 1/2 + sqrt(1/4+1/y)
        nu = 0.5 + np.sqrt(0.25 + 1.0 / yv)
        return gbv**2 * (nu**2 - 1.0)
    raise ValueError(kind)


MODEL_LABEL = {"fw": "framework  sqrt(1+1/y)", "mcg": "McGaugh/RAR-fit exp",
               "simple": "simple nu"}
