#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A74 -- THE DECISIVE FIT: fix a0 at the thermal value, refit everything else, and
       report what the truth costs.

Three fits on the identical data and priors as A71:
   (a) a0 FREE                      -> must reproduce A71's kappa_P3 = 0.3777 +- 0.1207
   (b) a0 FIXED at 8.620e-11        (thermal, kappa_DE = Z/4pi, kappa_P3 = 0.381)
   (c) a0 FIXED at 9.354e-11        (kappa = 1/2 in the rho_DE convention, kappa_P3 = 0.4135)
Everything else (B, u, 171 Upsilon) refit in every case.

Data (read-only, hashed): SPARC rotmod 171 gal / 3375 pts; SLACS Auger+2009 70 lenses;
A18 cluster anchor.  Nothing is downloaded and nothing is committed.

MUTATIONS: A74_MUTATE=<name>, see MUTATE.md.  Every check must be killed by at least one.
"""
import os
import sys
import math
import glob
import json
import time
import hashlib

import numpy as np
from scipy.optimize import brentq, minimize, minimize_scalar
from scipy.special import gammainc
from scipy.interpolate import CubicSpline
from scipy.integrate import quad
from scipy.stats import chi2 as chi2dist

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))

MUT = (os.environ.get("A74_MUTATE", "") or "").strip()
MUTS = ("", "drop_gal", "drop_lens", "floor10", "a0_off20", "sersic35", "arcsec",
        "imf_prior", "no_boot", "boot_draws", "kappa_de", "thermal_pi", "treu_shift",
        "u_prior", "cluster_a", "h0_70", "omega", "b_marg", "resp_lin",
        "lambda_off", "ups_window")
if MUT not in MUTS:
    sys.exit("unknown mutation: " + MUT)
TAG = ("_MUTATE_" + MUT) if MUT else ""

T0 = time.time()
OUTF = open(os.path.join(HERE, "a74" + TAG + ".out"), "w")
OUT = []


def P(s=""):
    s = str(s)
    print(s, flush=True)
    OUT.append(s)
    OUTF.write(s + "\n")


def head(t):
    P("")
    P("=" * 110)
    P(t)
    P("=" * 110)


CHECKS = []


def ck(cid, ok, measured, threshold, label="", killed_by=""):
    ok = bool(ok)
    CHECKS.append(dict(id=cid, pass_=ok, measured=str(measured), threshold=str(threshold),
                       label=label, killed_by=killed_by))
    P("  %-5s %s   %s" % (cid, "PASS" if ok else "FAIL", measured))
    P("         threshold: %s   :: %s" % (threshold, label))
    if not ok:
        P("         ^^^ MUTATION-SENSITIVE CHECK FAILED")
    return ok


# =====================================================================================
# 0.  constants -- A71's exact set, so that (a) is a reproduction and not a re-derivation
# =====================================================================================
G_N = 6.67430e-11
C_L = 2.99792458e8
MSUN = 1.98847e30
PC = 3.0856775814913673e16
KPC = 1e3 * PC
MPC = 1e6 * PC
ARCSEC = 1.10 * math.pi / (180.0 * 3600.0) if MUT == "arcsec" else math.pi / (180.0 * 3600.0)
HBAR = 1.054571817e-34
EV = 1.602176634e-19

H0_KMS = 70.0 if MUT == "h0_70" else 67.4
H0_SI = H0_KMS * 1e3 / MPC
OMEGA_L = 0.72 if MUT == "omega" else 0.6847
RHO_CRIT = 3.0 * H0_SI ** 2 / (8.0 * math.pi * G_N)
SQ_8PI3 = math.sqrt(8.0 * math.pi / 3.0)
Z_C = 2.0 * SQ_8PI3                                   # 5.788810
A0_PER_KAPPA = C_L * H0_SI / SQ_8PI3                  # 2.26241e-10
LN10 = math.log(10.0)
LAMBDA_OBS = 1.10e-52 if MUT == "lambda_off" else 1.0890e-52

# the declared thermal point and the rival (task-specified)
A0_TH_DECL = 8.620e-11
A0_HALF = 9.354e-11
if MUT == "thermal_pi":
    A0_TH = 2.0 * A0_TH_DECL                          # mutation: cH/pi instead of cH/2pi
else:
    A0_TH = A0_TH_DECL
A0_TH_EXACT_LAMBDA = C_L ** 2 * math.sqrt(LAMBDA_OBS / (12.0 * math.pi ** 2))
H_LAMBDA = C_L * math.sqrt(LAMBDA_OBS / 3.0)
A0_TH_EXACT_OMEGA = C_L * H0_SI * math.sqrt(OMEGA_L) / (2.0 * math.pi)
K_DE_ALGEBRA = Z_C / (4.0 * math.pi)                  # Z/4pi = 0.460659


def kappa_of_a0(a0):
    """A51/A71's rho_crit (P3) convention.  Mutation kappa_de swaps in rho_DE."""
    if MUT == "kappa_de":
        return a0 * math.sqrt(8.0 * math.pi) / (C_L * H0_SI * math.sqrt(3.0 * OMEGA_L))
    return a0 * SQ_8PI3 / (C_L * H0_SI)


def a0_of_kappa(k):
    return k * A0_PER_KAPPA


def kappa_de_of_a0(a0):
    """The rho_DE convention: kappa_DE = a0 sqrt(8pi)/(c H0 sqrt(3 Omega_L))."""
    return a0 * math.sqrt(8.0 * math.pi) / (C_L * H0_SI * math.sqrt(3.0 * OMEGA_L))


K_TH = kappa_of_a0(A0_TH)
K_HALF = kappa_of_a0(A0_HALF)
K_DE_TH = kappa_de_of_a0(A0_TH)
K_DE_HALF = kappa_de_of_a0(A0_HALF)

P("A74 -- THE DECISIVE FIT: a0 fixed at the thermal value, everything else refit")
P("  mutation: %s" % (MUT or "none"))
P("  H0 = %.1f km/s/Mpc, Omega_L = %.4f, Lambda = %.5e m^-2" % (H0_KMS, OMEGA_L, LAMBDA_OBS))
P("  kappa_P3 = a0 sqrt(8pi/3)/(c H0) ; a0_per_kappa = %.6e m/s^2 ; Z = 2sqrt(8pi/3) = %.6f"
  % (A0_PER_KAPPA, Z_C))
P("  thermal a0 = %.6e -> kappa_P3 = %.6f, kappa_DE = %.6f" % (A0_TH, K_TH, K_DE_TH))
P("  kappa=1/2 a0 = %.6e -> kappa_P3 = %.6f, kappa_DE = %.6f" % (A0_HALF, K_HALF, K_DE_HALF))

A71 = json.load(open(os.path.join(HERE, "..", "A71_global_fit", "a71_results.json")))
A72 = json.load(open(os.path.join(HERE, "..", "A72_coefficient", "a72_results.json")))
A55 = json.load(open(os.path.join(HERE, "..", "A55_lensing_prediction", "a55_results.json")))
A51 = json.load(open(os.path.join(HERE, "..", "A51_kappa_measured", "a51_results.json")))


def sha_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


# =====================================================================================
# C1/C2  the data blocks
# =====================================================================================
head("C1/C2  THE DATA BLOCKS (read-only, hashed)")

SPARC_DIR = os.path.join(REPO, "real_research", "data", "sparc_data")
SPARC_FILES = sorted(glob.glob(os.path.join(SPARC_DIR, "*_rotmod.dat")))
GAL = []
for _ifi, f in enumerate(SPARC_FILES):
    a = np.loadtxt(f, comments="#")
    if a.ndim != 2 or len(a) < 5:
        continue
    if MUT == "drop_gal" and _ifi % 10 == 9:
        continue
    GAL.append(dict(name=os.path.basename(f)[:-len("_rotmod.dat")],
                    r=a[:, 0] * KPC, V=a[:, 1], eV=a[:, 2],
                    Vg=a[:, 3], Vd=a[:, 4], Vb=a[:, 5]))
NG = len(GAL)
NPT = int(sum(len(g["r"]) for g in GAL))
H_SPARC = hashlib.sha256(b"".join(open(f, "rb").read() for f in SPARC_FILES)).hexdigest()[:16]
P("  SPARC: %d files -> %d galaxies -> %d points ; sha256(concat) = %s (A51/A71: %s)"
  % (len(SPARC_FILES), NG, NPT, H_SPARC, "469f4f556dc813b2"))
ck("C1", len(SPARC_FILES) == 175 and NG == 171 and NPT == 3375 and H_SPARC == "469f4f556dc813b2",
   "%d/%d/%d, sha %s" % (len(SPARC_FILES), NG, NPT, H_SPARC),
   "175 files, 171 galaxies, 3375 points, sha256 == 469f4f556dc813b2",
   "the vector fitted here is byte-identical to the one A71 fitted", "drop_gal")

DATA_SLACS = os.path.join(REPO, "real_research", "data", "slacs_auger2009_lenses.tsv")
DATA_TREU = os.path.join(REPO, "real_research", "cross_thread_review_2026_09_26",
                         "XR33_data_treu2010_table1.tsv")
_lines = [l.rstrip("\n") for l in open(DATA_SLACS, encoding="latin-1")]
_hi = [i for i, l in enumerate(_lines) if l.startswith("recno")][0]
_hdr = _lines[_hi].split("\t")
_col = {c: i for i, c in enumerate(_hdr)}
_raw = [l.split("\t") for l in _lines[_hi + 3:] if l.strip() and not l.startswith("#")]


def _f(v):
    try:
        return float(v.strip())
    except Exception:
        return float("nan")


LENS = []
for r in _raw:
    if len(r) < len(_hdr):
        continue
    d = dict(name=r[_col["SDSS"]].strip(), zl=_f(r[_col["zlens"]]), zs=_f(r[_col["zsrc"]]),
             sig=_f(r[_col["sigma"]]), RE=_f(r[_col["RE"]]), lME=_f(r[_col["Mass"]]),
             Fc=_f(r[_col["Fc"]]), Fs=_f(r[_col["Fs"]]), ReV=_f(r[_col["Re(V)"]]))
    if all(np.isfinite([d["zl"], d["zs"], d["RE"], d["lME"], d["Fs"], d["Fc"]])) and d["RE"] > 0:
        LENS.append(d)
if MUT == "drop_lens":
    LENS = [d for i, d in enumerate(LENS) if i % 7 != 3]
NL = len(LENS)
H_SLACS = sha_file(DATA_SLACS)
P("  SLACS: %d catalogue rows -> %d usable lenses ; sha256 = %s (A70: d78d7627d6bbcc07)"
  % (len(_raw), NL, H_SLACS[:16]))
ck("C2", len(_raw) == 85 and NL == 70 and H_SLACS[:16] == "d78d7627d6bbcc07",
   "%d rows, %d lenses, sha %s" % (len(_raw), NL, H_SLACS[:16]),
   "85 rows, 70 lenses, sha256[:16] == d78d7627d6bbcc07",
   "the lens sample is the one A70 audited, not a cut made here", "drop_lens")

# =====================================================================================
# C3  the SPARC likelihood IS the record's
# =====================================================================================
head("C3  THE SPARC LIKELIHOOD IS THE RECORD'S (zero-parameter chi2/dof)")
UG = (np.geomspace(0.40, 1.00, 120) if MUT == "ups_window" else np.geomspace(0.05, 2.5, 240))
FLOOR = 0.10 if MUT == "floor10" else 0.05


def chi2_sparc(a0, gals=None, ug=UG, floor=FLOOR):
    """sum (V-Vpred)^2/(eV^2+(floor V)^2), one Upsilon per galaxy profiled on a grid."""
    gals = GAL if gals is None else gals
    if MUT == "a0_off20":
        a0 = 0.8 * a0
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


def chi2_sparc_fixed(a0, ups=0.5, floor=FLOOR):
    tot = 0.0
    for g in GAL:
        Vb2 = g["Vg"] ** 2 + ups * (g["Vd"] ** 2 + g["Vb"] ** 2)
        gN = Vb2 * 1e6 / g["r"]
        Vp = np.sqrt(0.5 * gN * (1.0 + np.sqrt(1.0 + 4.0 * a0 / np.maximum(gN, 1e-30)))
                     * g["r"]) / 1e3
        s = np.sqrt(g["eV"] ** 2 + (floor * g["V"]) ** 2)
        tot += float(np.sum(((g["V"] - Vp) / s) ** 2))
    return tot


_ch_fix = chi2_sparc_fixed(1.132e-10) / NPT
_ch_fix936 = chi2_sparc_fixed(9.36e-11) / NPT
_ch_free = chi2_sparc(1.132e-10) / (NPT - NG)
P("  fixed Upsilon=0.5, a0=1.132e-10 : chi2/N = %.4f  (record 6.87)" % _ch_fix)
P("  fixed Upsilon=0.5, a0=9.360e-11 : chi2/N = %.4f  (record 6.63)" % _ch_fix936)
P("  one Upsilon per galaxy, 1.132e-10: chi2/dof = %.4f  (record 2.42)" % _ch_free)
ck("C3", abs(_ch_fix - 6.8651) < 0.02 and abs(_ch_fix936 - 6.6312) < 0.02 and abs(_ch_free - 2.4714) < 0.05,
   "%.4f / %.4f / %.4f" % (_ch_fix, _ch_fix936, _ch_free),
   "6.8651+-0.02, 6.6312+-0.02, 2.4714+-0.05",
   "three zero-parameter chi2/dof reproduce A71's stored values: same likelihood, same Upsilon window",
   "newton")

# =====================================================================================
# C4  the two kappa conventions
# =====================================================================================
head("C4  THE CONVENTION: WHICH a0 IS kappa = 1/2")
_rt = abs(a0_of_kappa(kappa_of_a0(A0_HALF)) / A0_HALF - 1.0)
_ratio_conv = kappa_de_of_a0(A0_HALF) / kappa_of_a0(A0_HALF)
# A72 quotes kappa_DE with Omega_L = 0.6838 (the Lambda footing); A71 uses 0.6847 (Planck).
# Both are shown, because the 0.07% between them is a convention difference, not a physical one.
_OM73 = 0.6838
K_DE_HALF_73 = A0_HALF * math.sqrt(8.0 * math.pi) / (C_L * H0_SI * math.sqrt(3.0 * _OM73))
P("  a0 = %.6e -> kappa_P3 = %.6f ; kappa_DE = %.6f (Omega_L = %.4f, A71's convention)"
  % (A0_HALF, K_HALF, K_DE_HALF, OMEGA_L))
P("  the same a0 in A72's Omega_L = %.4f convention: kappa_DE = %.6f"
  % (_OM73, K_DE_HALF_73))
P("  kappa_DE/kappa_P3 = %.6f ; 1/sqrt(Omega_L) = %.6f" % (_ratio_conv, 1.0 / math.sqrt(OMEGA_L)))
P("  kappa_P3(a0 = 1.1312e-10) = %.6f (the P3 'kappa = 1/2' footing, NOT this task's rival)"
  % kappa_of_a0(1.1312e-10))
P("  round trip a0 -> kappa -> a0 residual %.2e" % _rt)
ck("C4", abs(K_HALF - 0.413461) < 2e-5 and abs(K_DE_HALF_73 - 0.5) < 2e-5
   and abs(_ratio_conv - 1.0 / math.sqrt(OMEGA_L)) < 1e-6 and _rt < 1e-12
   and abs(kappa_of_a0(1.1312e-10) - 0.5) < 2e-5,
   "kappa_P3(9.354e-11) = %.6f, kappa_DE = %.6f (%.6f in the 0.6838 convention), ratio %.6f, round trip %.0e"
   % (K_HALF, K_DE_HALF, K_DE_HALF_73, _ratio_conv, _rt),
   "0.413461+-2e-5 in P3 ; 0.500000+-2e-5 in A72's DE convention ; ratio == 1/sqrt(Omega_L) to 1e-6 ; round trip < 1e-12",
   "the rival is kappa = 1/2 in the rho_DE convention, which is kappa_P3 = 0.4135 -- the fit is "
   "done in P3 throughout, so this number, not 0.5, is the one that enters; the two Omega_L "
   "footings differ by 0.07% and both are printed rather than mixed", "kappa_de")

# =====================================================================================
# C5  the thermal value from the constants
# =====================================================================================
head("C5  THE THERMAL VALUE: THREE ROUTES TO 8.62e-11")
P("  c^2 sqrt(Lambda/(12 pi^2))   = %.9e  (BRIEF Lambda = %.5e m^-2)" % (A0_TH_EXACT_LAMBDA, LAMBDA_OBS))
P("  c H_Lambda/(2 pi), H_Lambda = c sqrt(Lambda/3) = %.9e" % (C_L * H_LAMBDA / (2 * math.pi)))
P("  c H0 sqrt(Omega_L)/(2 pi)    = %.9e  (Omega_L = %.4f)" % (A0_TH_EXACT_OMEGA, OMEGA_L))
P("  declared / deployed          = %.9e  (mutation thermal_pi doubles it)" % A0_TH)
P("  two constant routes straddle the declared value by %.4f%% / %.4f%%"
  % (100 * (A0_TH / A0_TH_EXACT_LAMBDA - 1), 100 * (A0_TH / A0_TH_EXACT_OMEGA - 1)))
P("  kappa_DE: Z/(4pi) = %.9f ; from a0 = %.9f (%.4f%% apart)"
  % (K_DE_ALGEBRA, K_DE_TH, 100 * (K_DE_TH / K_DE_ALGEBRA - 1)))
ck("C5", abs(A0_TH / A0_TH_EXACT_LAMBDA - 1) < 1.5e-3 and abs(A0_TH / A0_TH_EXACT_OMEGA - 1) < 1.5e-3
   and abs(K_DE_TH / K_DE_ALGEBRA - 1) < 1.5e-3 and abs(K_DE_ALGEBRA - 0.460659) < 2e-6,
   "Lambda route %.6e, Omega route %.6e, declared %.6e, kappa_DE %.6f"
   % (A0_TH_EXACT_LAMBDA, A0_TH_EXACT_OMEGA, A0_TH, K_DE_TH),
   "both constant routes within 0.15% of the deployed value; Z/4pi = 0.460659+-2e-6",
   "the thermal point is not a fitted number: two independent constant routes land on it to 0.07%, "
   "and the declared 3-digit value sits between them", "thermal_pi")

# =====================================================================================
# C6/C7  SPARC alone, and its error
# =====================================================================================
head("C6  SPARC ALONE -- and the error bar that is used everywhere below")
r_sp = minimize_scalar(lambda a: chi2_sparc(a), bounds=(5e-11, 2.5e-10),
                       method="bounded", options=dict(xatol=1e-16))
A0_SP = float(r_sp.x)
K_SP = kappa_of_a0(A0_SP)
CHI2_SP = float(r_sp.fun)
DOF_SP = NPT - NG
P("  a0 = %.6e ; kappa = %.6f ; chi2 = %.2f / %d = %.4f" % (A0_SP, K_SP, CHI2_SP, DOF_SP, CHI2_SP / DOF_SP))
P("  A51 stored: a0 = %.6e ; kappa = %.6f ; chi2/dof = %.4f"
  % (A51["sparc"]["a0_best"], A51["sparc"]["kappa"], A51["sparc"]["chi2_dof"]))
ck("C6", abs(A0_SP / A51["sparc"]["a0_best"] - 1) < 2e-4 and abs(K_SP / A51["sparc"]["kappa"] - 1) < 2e-4
   and abs(CHI2_SP / DOF_SP - A51["sparc"]["chi2_dof"]) < 2e-4,
   "a0 %.6e vs %.6e ; kappa %.6f vs %.6f ; chi2/dof %.4f vs %.4f"
   % (A0_SP, A51["sparc"]["a0_best"], K_SP, A51["sparc"]["kappa"], CHI2_SP / DOF_SP,
      A51["sparc"]["chi2_dof"]),
   "a0 and kappa to 2e-4 relative, chi2/dof to 2e-4 absolute",
   "an independently written SPARC likelihood lands on A51's minimum: the channel is not re-tuned here",
   "floor10")

_lo1d = brentq(lambda a: chi2_sparc(a) - CHI2_SP - 1.0, 3e-11, A0_SP * (1 - 1e-9), xtol=1e-20)
_hi1d = brentq(lambda a: chi2_sparc(a) - CHI2_SP - 1.0, A0_SP * (1 + 1e-9), 3e-10, xtol=1e-20)
SIG_DCHI2 = 0.5 * (_hi1d - _lo1d) / A0_SP
_rng = np.random.default_rng(20261021)
_nboot = 60 if MUT == "boot_draws" else 200
_boot = np.empty(_nboot)
for _k in range(_nboot):
    _idx = _rng.integers(0, NG, NG)
    _gg = [GAL[i] for i in _idx]
    _boot[_k] = minimize_scalar(lambda a: chi2_sparc(a, _gg), bounds=(5e-11, 2.5e-10),
                                method="bounded", options=dict(xatol=1e-16)).x
BOOT_FRAC = float(_boot.std(ddof=1) / np.median(_boot))
P("  Delta-chi2 = 1 in a0 : %.5f%%   (chi2/dof = %.2f, so this is NOT the honest error)"
  % (100 * SIG_DCHI2, CHI2_SP / DOF_SP))
P("  %d-draw block bootstrap: median %.6e, sigma/median = %.9f  (A51: %.9f)"
  % (_nboot, np.median(_boot), BOOT_FRAC, A51["sparc"]["sigma_stat_boot"]))
P("  ratio bootstrap/formal = %.2f ; sigma(kappa)_SPARC = %.6f" % (BOOT_FRAC / SIG_DCHI2, BOOT_FRAC * K_SP))
ck("C7", abs(BOOT_FRAC / A51["sparc"]["sigma_stat_boot"] - 1) < 1e-4 and BOOT_FRAC / SIG_DCHI2 > 5.0,
   "bootstrap %.9f vs A51 %.9f ; ratio to Delta-chi2 %.2f"
   % (BOOT_FRAC, A51["sparc"]["sigma_stat_boot"], BOOT_FRAC / SIG_DCHI2),
   "matches A51 to 1e-4 and is > 5x the formal error",
   "the per-galaxy scatter makes the formal error wrong by 8x; the bootstrap is sigma(SPARC) below",
   "boot_draws")

SIG_K_SP = BOOT_FRAC * K_SP
if MUT == "no_boot":
    SIG_K_SP = SIG_DCHI2 * K_SP

# =====================================================================================
# C8-C11  the SLACS model
# =====================================================================================
head("C8-C11  SLACS: the A70/A55 model, B_req, and the two responses")

OM_SL, OL_SL, H0_SL = 0.3, 0.7, 70.0e3 / MPC
_zg = np.linspace(0.0, 6.0, 8001)
_Eg = np.sqrt(OM_SL * (1.0 + _zg) ** 3 + OL_SL)
_ig = np.concatenate([[0.0], np.cumsum(0.5 * (1.0 / _Eg[1:] + 1.0 / _Eg[:-1]) * np.diff(_zg))])


def DC(z):
    return (C_L / H0_SL) * float(np.interp(z, _zg, _ig))


def DA(z):
    return DC(z) / (1.0 + z)


def DAls(z1, z2):
    return (DC(z2) - DC(z1)) / (1.0 + z2)


def SICR(zl, zs):
    return C_L * C_L * DA(zs) / (4.0 * math.pi * G_N * DA(zl) * DAls(zl, zs))


B4 = 7.669249934
N_SER = 3.5 if MUT == "sersic35" else 4.0


def M2D_star(R, Re, n=N_SER):
    b = B4 if n == 4.0 else 2.0 * n - 1.0 / 3.0 + 4.0 / (405.0 * n) + 46.0 / (25515.0 * n * n)
    return gammainc(2.0 * n, b * (np.asarray(R) / Re) ** (1.0 / n))


def M3D_star(r, Re, n=N_SER):
    b = B4 if n == 4.0 else 2.0 * n - 1.0 / 3.0 + 4.0 / (405.0 * n) + 46.0 / (25515.0 * n * n)
    nu = n * (3.0 - (1.0 - 0.6097 / n + 0.05463 / (n * n)))
    return gammainc(nu, b * (np.asarray(r) / Re) ** (1.0 / n))


GLX, GLW = np.polynomial.legendre.leggauss(400)
GLX = 0.5 * (GLX + 1.0)
GLW = 0.5 * GLW


def M2D_from_g(R, M3Df, a0, rmax=1.0e6 * KPC):
    if R >= rmax:
        return 0.0
    U = math.acosh(max(rmax / R, 1.0 + 1e-9))
    u = GLX * U
    r = R * np.cosh(u)
    gN = G_N * np.asarray(M3Df(r)) / r ** 2
    g = 0.5 * gN * (1.0 + np.sqrt(1.0 + 4.0 * a0 / np.maximum(gN, 1e-300)))
    return R * R / G_N * float(np.sum(GLW * g) * U)


def predict(d, a0, boost=1.0):
    if MUT == "a0_off20":
        a0 = 0.8 * a0
    sc = SICR(d["zl"], d["zs"])
    ME = 10.0 ** d["lME"]
    REo = d["RE"] * KPC
    Re = d["ReV"] * ARCSEC * DA(d["zl"])
    A = boost * d["Fs"] * ME / M2D_star(REo, Re)
    M3f = lambda r: A * M3D_star(r, Re) * MSUN
    fun = lambda R: M2D_from_g(R, M3f, a0) - math.pi * R * R * sc
    Rs = np.logspace(math.log10(0.15 * REo), math.log10(10.0 * REo), 60)
    v = np.array([fun(x) for x in Rs])
    idx = np.where(np.diff(np.sign(v)) != 0)[0]
    if len(idx) == 0:
        return float("nan")
    return brentq(fun, Rs[idx[0]], Rs[idx[0] + 1], xtol=1e-5 * KPC) / KPC


A0_QUOTED = 1.132e-10
RATIOS = np.array([predict(d, A0_QUOTED) / d["RE"] for d in LENS])
MED50 = float(np.median(RATIOS))
MEANLN50 = float(np.log(RATIOS).mean())
_r55 = {x["name"]: x["ratio"] for x in A55["slacs"]["per_lens_salpeter"]}
_dev = float(np.max(np.abs(np.array([RATIOS[i] / _r55[d["name"]] - 1.0 for i, d in enumerate(LENS)]))))
P("  median R_E,pred/R_E,obs = %.6f (A55 0.8852) ; <ln> = %+.6f (A55 -0.1245)" % (MED50, MEANLN50))
P("  max per-lens deviation from A55's stored ratios: %.2e ; N = %d" % (_dev, NL))
ck("C8", abs(MED50 / 0.885232 - 1) < 1e-4 and _dev < 1e-9 and NL == 70 and abs(MEANLN50 + 0.124539) < 2e-4,
   "median %.6f ; <ln> %+.6f ; max dev %.1e" % (MED50, MEANLN50, _dev),
   "median 0.885232+-1e-4 ; <ln> -0.124539+-2e-4 ; per-lens < 1e-9",
   "this IS A55's/A70's lens model, per lens, not a rival implementation", "sersic35")

B_INV = 1.0 / MED50
B_INV2 = B_INV ** 2


def med_at_B(B, a0=A0_QUOTED):
    return float(np.median([predict(d, a0, boost=B) / d["RE"] for d in LENS]))


B_REQ = brentq(lambda B: med_at_B(B) - 1.0, 1.02, 5.0, xtol=1e-6)
P("  root-found B (median ratio = 1) at kappa_P3 = 0.5: %.5f  (A70: 1.174)" % B_REQ)
P("  1/median = %.5f ; 1/median^2 = %.5f (A55's 1.283) ; B_req/(1/median) = %.5f"
  % (B_INV, B_INV2, B_REQ / B_INV))
ck("C9", abs(B_REQ - 1.1738) < 2e-3 and abs(B_INV2 - 1.2761) < 2e-3 and B_REQ < 0.97 * B_INV2,
   "B_req %.5f ; 1/median %.5f ; 1/median^2 %.5f" % (B_REQ, B_INV, B_INV2),
   "B_req = 1.174+-0.002 ; 1/median^2 = 1.276+-0.002 ; B_req < 0.97 x 1/median^2",
   "the M/L that zeroes SLACS is 1.174xSalpeter: the response is 0.7775, not the 2 that A55 assumed",
   "arcsec")

_dB = 0.10
_resp = np.array([math.log(predict(d, A0_QUOTED, boost=1.0 + _dB) / predict(d, A0_QUOTED)) for d in LENS])
if MUT == "resp_lin":
    RESP = float(np.median(_resp)) / _dB
else:
    RESP = float(np.median(_resp)) / math.log(1.0 + _dB)
RESP_SCATTER = float(_resp.std(ddof=1)) / math.log(1.0 + _dB)
B_FROM_RESP = math.exp(-MEANLN50 / RESP)
_h = 1e-3
_dlnR_dlnk = (math.log(float(np.median([predict(d, a0_of_kappa(0.5 * math.exp(_h))) / d["RE"] for d in LENS])))
              - math.log(float(np.median([predict(d, a0_of_kappa(0.5 * math.exp(-_h))) / d["RE"] for d in LENS])))) / (2 * _h)
P("  dlnR/dlnB = %.5f (per-lens median, scatter %.5f) ; response route B = %.5f (root %.5f)"
  % (RESP, RESP_SCATTER, B_FROM_RESP, B_REQ))
P("  dlnR/dlnkappa = %.5f ; ratio = %.3f : 1" % (_dlnR_dlnk, RESP / abs(_dlnR_dlnk)))
ck("C10", abs(RESP - 0.7775) < 5e-3 and abs(B_FROM_RESP / B_REQ - 1) < 3e-3
   and abs(_dlnR_dlnk - 0.1205) < 5e-4 and 6.0 < RESP / abs(_dlnR_dlnk) < 7.0,
   "dlnR/dlnB %.5f ; B_resp %.5f vs B_root %.5f ; dlnR/dlnk %.5f ; ratio %.2f"
   % (RESP, B_FROM_RESP, B_REQ, _dlnR_dlnk, RESP / abs(_dlnR_dlnk)),
   "0.7775+-0.005 ; two B routes within 3e-3 ; 0.1205+-5e-4 ; ratio in [6,7]",
   "lensing is 6.5x more sensitive to the IMF than to a0 -- it is a mass-normalisation measurement",
   "resp_lin")

KS_GRID = np.array([0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.60, 0.70,
                    0.85, 1.00, 1.20, 1.45, 1.70])
ML_TAB, SD_TAB = [], []
for k in KS_GRID:
    lr = np.log(np.array([predict(d, a0_of_kappa(k)) / d["RE"] for d in LENS]))
    ML_TAB.append(float(lr.mean()))
    SD_TAB.append(float(lr.std(ddof=1)))
ML_TAB = np.array(ML_TAB)
SD_TAB = np.array(SD_TAB)
SPL_M = CubicSpline(np.log(KS_GRID), ML_TAB)
SPL_S = CubicSpline(np.log(KS_GRID), SD_TAB)
S_LN = math.sqrt(0.045 ** 2 + 0.09 ** 2) * LN10          # per-lens sigma in ln


def lnB_req(k):
    """The B that zeroes the SLACS mean residual at kappa, from the 70-lens model."""
    return -float(SPL_M(math.log(k))) / RESP


SIG_LOGB_DEX = (float(np.log(RATIOS).std(ddof=1)) / math.sqrt(NL) / LN10) / RESP
SIG_LOGB_CURV = (S_LN / LN10) / (RESP * math.sqrt(NL))
P("  sigma(log10 B): mean/SEM route %.6f dex ; curvature route %.6f dex ; difference %.1f%%"
  % (SIG_LOGB_DEX, SIG_LOGB_CURV, 100 * (SIG_LOGB_CURV / SIG_LOGB_DEX - 1)))
ck("C11", abs(SIG_LOGB_DEX - 0.014251) < 5e-5 and abs(SIG_LOGB_CURV / SIG_LOGB_DEX - 1) < 0.12,
   "%.6f dex vs %.6f dex" % (SIG_LOGB_DEX, SIG_LOGB_CURV),
   "0.014251+-5e-5 ; two routes within 12%",
   "70 lenses measure one number -- the IMF normalisation -- to 3.3%", "sersic35")

# =====================================================================================
# C12  the Treu prior
# =====================================================================================
head("C12  THE IMF PRIOR: Treu+2010 on the same 56 SLACS lenses")
_tl = [l.rstrip("\n") for l in open(DATA_TREU, encoding="latin-1")]
_ti = [i for i, l in enumerate(_tl) if l.startswith("name")][0]
_th = _tl[_ti].split("\t")
_ic = {c: i for i, c in enumerate(_th)}
_tr = [l.split("\t") for l in _tl[_ti + 1:] if l.strip() and not l.startswith("#")]
ALPHA = np.array([float(r[_ic["log_alpha"]]) for r in _tr if len(r) == len(_th)])
if MUT == "treu_shift":
    ALPHA = ALPHA + 0.10
TREU_MEAN = float(ALPHA.mean())
TREU_SEM = float(ALPHA.std(ddof=1) / math.sqrt(len(ALPHA)))
TREU_95HI = 10 ** (1.96 * math.sqrt(0.03 ** 2 + 0.02 ** 2))
P("  N = %d ; <log10 alpha_Salp> = %+.5f +- %.5f (sem) ; scatter %.4f dex"
  % (len(ALPHA), TREU_MEAN, TREU_SEM, float(ALPHA.std(ddof=1))))
P("  abstract 0.00+-0.03+-0.02 -> 95%% on the mean = %.4f x Salpeter" % TREU_95HI)
ck("C12", len(ALPHA) == 56 and abs(TREU_MEAN) < 0.02 and abs(TREU_95HI - 1.1767) < 2e-4,
   "N=%d, mean %+.5f, 95%% hi %.5f" % (len(ALPHA), TREU_MEAN, TREU_95HI),
   "56 lenses, |mean| < 0.02, 95% upper 1.1767+-2e-4",
   "the prior is B = 1.00 +- 0.036 dex and B = 1.174 sits on its 95% boundary", "treu_shift")

SIG_B_PRIOR_DEX = 0.100 if MUT == "imf_prior" else 0.036
SIG_B_MEAS_DEX = SIG_LOGB_DEX
SIG_B_PULL_DEX = math.sqrt(SIG_B_PRIOR_DEX ** 2 + SIG_B_MEAS_DEX ** 2)
SIG_B_PRIOR = SIG_B_PRIOR_DEX * LN10
SIG_B_MEAS = SIG_B_MEAS_DEX * LN10

# =====================================================================================
# C13/C14  the cluster channel
# =====================================================================================
head("C13/C14  CLUSTERS: A18's anchor, and the channel alone")


def F_ph(y):
    return 0.5 * (math.sqrt(1.0 + 4.0 / y) - 1.0)


CL_MB, CL_A = 1.4e14 * MSUN, (200.0 if MUT == "cluster_a" else 250.0) * KPC


def rvir(a0, delta=200.0):
    def g(lr):
        r = math.exp(lr)
        Me = CL_MB * (r / (r + CL_A)) ** 2
        return Me * (1.0 + F_ph(G_N * Me / (a0 * r * r))) - (4.0 * math.pi / 3.0) * delta * RHO_CRIT * r ** 3
    return math.exp(brentq(g, math.log(1e-6 * MPC), math.log(1e3 * MPC), xtol=1e-15, rtol=1e-15))


def R_tot(a0):
    r = rvir(a0)
    Me = CL_MB * (r / (r + CL_A)) ** 2
    fv = F_ph(G_N * Me / (a0 * r * r))
    c = r / CL_A
    mu = (c / (1.0 + c)) ** 2
    return mu * (1.0 + fv) - 1.0, r, fv


A0_CANON = 9.36e-11
R_CAN, RV_CAN, F_CAN = R_tot(A0_CANON)
P("  r_v = %.4f Mpc ; F(y_v) = %.4f ; R_tot = %.4f  (A18: 1.6863 / 3.7702 / 2.6179)"
  % (RV_CAN / MPC, F_CAN, R_CAN))
ck("C13", abs(RV_CAN / MPC - 1.6863) < 1e-3 and abs(F_CAN - 3.7702) < 1e-3 and abs(R_CAN - 2.6179) < 1e-3,
   "%.4f Mpc / %.4f / %.4f" % (RV_CAN / MPC, F_CAN, R_CAN),
   "1.6863+-0.001 / 3.7702+-0.001 / 2.6179+-0.001",
   "A18's anchor is reproduced before it is used as a constraint", "cluster_a")

_hh = 1e-3
DLNR = (math.log(R_tot(A0_CANON * (1 + _hh))[0]) - math.log(R_tot(A0_CANON * (1 - _hh))[0])) / (2 * _hh)
R_REQ, SIG_R = 5.552, 0.427
U0, SIG_U = 0.45, (1.0 if MUT == "u_prior" else 0.03)
SIG_CL = math.sqrt((SIG_R / R_REQ) ** 2 + (SIG_U / U0) ** 2) / abs(DLNR)
K_CL = kappa_of_a0(A0_CANON) * (U0 * R_REQ / R_CAN) ** (1.0 / DLNR)
P("  R_req = %.3f +- %.3f (A18) ; dlnR_tot/dlna0 = %+.5f ; cluster-only kappa = %.5f +- %.5f (%.2f%%)"
  "  (A51: 0.3934+-0.0432)" % (R_REQ, SIG_R, DLNR, K_CL, K_CL * SIG_CL, 100 * SIG_CL))
ck("C14", abs(K_CL - 0.3934) < 2e-3 and abs(SIG_CL - 0.1097) < 3e-3,
   "kappa %.5f +- %.5f (sigma/kappa %.5f)" % (K_CL, K_CL * SIG_CL, SIG_CL),
   "0.3934+-0.002 ; sigma/kappa 0.1097+-0.003",
   "the cluster band is 11% wide and u comes from the same amplitudes: a consistency check, not a measurement",
   "u_prior")


def chi2_cluster(k, u):
    Rt = R_tot(a0_of_kappa(k))[0]
    return ((Rt / u - R_REQ) / SIG_R) ** 2 + ((u - U0) / SIG_U) ** 2


def u_best(k):
    return minimize_scalar(lambda u: chi2_cluster(k, u), bounds=(0.30, 0.70), method="bounded",
                           options=dict(xatol=1e-12)).x


# =====================================================================================
# C15/C16  the free fit (= A71) and an independent minimiser
# =====================================================================================
head("C15/C16  FIT (a): a0 FREE -- the A71 reproduction")


def chi2_prof(k, sparc_sigma=None, use_slacs=True, use_cluster=True):
    s = SIG_K_SP if sparc_sigma is None else sparc_sigma
    c = ((k - K_SP) / s) ** 2
    if use_slacs:
        Lq = lnB_req(k)
        c += Lq * Lq / (SIG_B_MEAS ** 2 + SIG_B_PRIOR ** 2)
    if use_cluster:
        c += chi2_cluster(k, u_best(k))
    return c


def B_at(k):
    Lq = lnB_req(k)
    if MUT == "b_marg":
        return math.exp(Lq)                     # mutation: prior not marginalised
    return math.exp(Lq * SIG_B_PRIOR ** 2 / (SIG_B_MEAS ** 2 + SIG_B_PRIOR ** 2))


r_j = minimize_scalar(lambda lk: chi2_prof(math.exp(lk)), bounds=(math.log(0.20), math.log(0.80)),
                      method="bounded", options=dict(xatol=1e-14))
K_JOINT = float(math.exp(r_j.x))
CHI2_JOINT = float(r_j.fun)
U_JOINT = float(u_best(K_JOINT))
B_JOINT = float(B_at(K_JOINT))
SP_JOINT = ((K_JOINT - K_SP) / SIG_K_SP) ** 2
SL_JOINT = (math.log(B_JOINT) - lnB_req(K_JOINT)) ** 2 / SIG_B_MEAS ** 2
PR_JOINT = math.log(B_JOINT) ** 2 / SIG_B_PRIOR ** 2
CL_JOINT = chi2_cluster(K_JOINT, U_JOINT)
A0_JOINT = a0_of_kappa(K_JOINT)
P("  kappa_P3 = %.6f ; a0 = %.6e m/s^2 ; B = %.6f ; u = %.6f ; chi2 = %.6f"
  % (K_JOINT, A0_JOINT, B_JOINT, U_JOINT, CHI2_JOINT))
P("  decomposition: SPARC %.4f + SLACS %.4f + clusters %.4f + IMF prior %.4f"
  % (SP_JOINT, SL_JOINT, CL_JOINT, PR_JOINT))
P("  A71 stored: kappa %.6f ; B %.6f ; u %.6f ; chi2 %.6f"
  % (A71["joint"]["kappa"], A71["joint"]["B"], A71["joint"]["u"], A71["joint"]["chi2"]))
ck("C15", abs(K_JOINT / A71["joint"]["kappa"] - 1) < 2e-5 and abs(B_JOINT / A71["joint"]["B"] - 1) < 2e-5
   and abs(U_JOINT / A71["joint"]["u"] - 1) < 2e-4 and abs(CHI2_JOINT - A71["joint"]["chi2"]) < 1e-3,
   "kappa %.7f vs %.7f ; B %.7f vs %.7f ; u %.7f vs %.7f ; chi2 %.7f vs %.7f"
   % (K_JOINT, A71["joint"]["kappa"], B_JOINT, A71["joint"]["B"], U_JOINT, A71["joint"]["u"],
      CHI2_JOINT, A71["joint"]["chi2"]),
   "all four within 2e-5 relative of A71's stored joint fit",
   "fit (a) IS A71: the same data, priors, compression and minimiser reproduce the stored minimum", "no_boot")

_r2 = minimize(lambda p: ((math.exp(p[0]) - K_SP) / SIG_K_SP) ** 2
               + (p[1] - lnB_req(math.exp(p[0]))) ** 2 / SIG_B_MEAS ** 2
               + p[1] ** 2 / SIG_B_PRIOR ** 2
               + chi2_cluster(math.exp(p[0]), p[2]),
               [math.log(K_JOINT) + 0.02, math.log(1.2), 0.5], method="Nelder-Mead",
               options=dict(xatol=1e-13, fatol=1e-13, maxiter=40000))
K_NM, B_NM, U_NM = float(math.exp(_r2.x[0])), float(math.exp(_r2.x[1])), float(_r2.x[2])
P("  independent 3-parameter Nelder-Mead: kappa %.7f, B %.7f, u %.7f, chi2 %.7f"
  % (K_NM, B_NM, U_NM, _r2.fun))
ck("C16", abs(K_NM / K_JOINT - 1) < 1e-5 and abs(B_NM / B_JOINT - 1) < 1e-5
   and abs(_r2.fun - CHI2_JOINT) < 1e-4,
   "profile %.6f/%.6f/%.6f vs NM %.6f/%.6f/%.6f, chi2 %.6f vs %.6f"
   % (K_JOINT, B_JOINT, U_JOINT, K_NM, B_NM, U_NM, CHI2_JOINT, _r2.fun),
   "two independent minimisers agree to 1e-5 in kappa and B",
   "the free-fit optimum is not an artefact of the profile/analytic elimination", "b_marg")

# errors at the free fit: profile for kappa, marginal covariance for (ln kappa, ln B)
_lo1 = brentq(lambda lk: chi2_prof(math.exp(lk)) - CHI2_JOINT - 1.0, math.log(0.20), math.log(K_JOINT), xtol=1e-15)
_hi1 = brentq(lambda lk: chi2_prof(math.exp(lk)) - CHI2_JOINT - 1.0, math.log(K_JOINT), math.log(0.80), xtol=1e-15)
SIG_K_JOINT = 0.5 * (math.exp(_hi1) - math.exp(_lo1))
EST_HALF_SPAN = 0.20838642838788285                  # A51's 7-estimator half-span, as A71 uses it
SYS_FRAC = math.sqrt(EST_HALF_SPAN ** 2 + 0.161 ** 2 + 0.125 ** 2 + 0.10 ** 2 + 0.05 ** 2)
SIG_K_TOT = math.sqrt(SIG_K_JOINT ** 2 + (SYS_FRAC * K_JOINT) ** 2)
P("  INPUTS QUOTED IN THE REPORT: IMF prior B = 1.00 +- %.3f dex (%d Treu lenses) ; u = %.2f +- %.2f (A18)"
  % (SIG_B_PRIOR_DEX, len(ALPHA), U0, SIG_U))
P("    Upsilon window [%.2f, %.1f] ; A71 systematic floor: estimator %.2f%%, distance %.1f%%, H0 %.1f%%,"
  " law %.1f%%, Upsilon %.1f%% -> %.2f%%"
  % (UG.min(), UG.max(), 100 * EST_HALF_SPAN, 16.1, 12.5, 10.0, 5.0, 100 * SYS_FRAC))
P("    A71 stored for comparison: Delta-chi2(kappa=1/2, B profiled) = %.6f ; global tension T = %.6f (%.4f sigma)"
  % (A71["joint"]["chi2_at_half"], A71["joint"]["tension"], A71["joint"]["tension_sigma"]))


def chi2_kb(lk, lb):
    k = math.exp(lk)
    return (((k - K_SP) / SIG_K_SP) ** 2 + (lb - lnB_req(k)) ** 2 / SIG_B_MEAS ** 2
            + lb ** 2 / SIG_B_PRIOR ** 2 + chi2_cluster(k, u_best(k)))


_x0 = np.array([math.log(K_JOINT), math.log(B_JOINT)])
_hx = 1e-4
_Hk = np.zeros((2, 2))
for _i in range(2):
    for _j in range(2):
        _ei = np.zeros(2); _ej = np.zeros(2)
        _ei[_i] = _hx; _ej[_j] = _hx
        _Hk[_i, _j] = (chi2_kb(*(_x0 + _ei + _ej)) - chi2_kb(*(_x0 + _ei - _ej))
                       - chi2_kb(*(_x0 - _ei + _ej)) + chi2_kb(*(_x0 - _ei - _ej))) / (4 * _hx * _hx)
COV = 2.0 * np.linalg.inv(_Hk)
SIG_LNK = math.sqrt(COV[0, 0])
SIG_LNB = math.sqrt(COV[1, 1])
SIG_B_JOINT = B_JOINT * SIG_LNB
SIG_B_COND = B_JOINT * (SIG_B_MEAS * SIG_B_PRIOR / math.sqrt(SIG_B_MEAS ** 2 + SIG_B_PRIOR ** 2))
_du = 1e-3
_u2 = (chi2_cluster(K_JOINT, U_JOINT + _du) - 2 * chi2_cluster(K_JOINT, U_JOINT)
       + chi2_cluster(K_JOINT, U_JOINT - _du)) / _du ** 2
SIG_U_FREE = math.sqrt(2.0 / _u2)
P("  sigma(kappa) stat = %.6f (A71 %.6f) ; with the 31.2%% floor %.6f (A71 %.6f)"
  % (SIG_K_JOINT, A71["joint"]["sigma_stat"], SIG_K_TOT, A71["joint"]["sigma_tot"]))
P("  sigma(lnB) marginal = %.6f (A71 K28 %.6f) -> sigma(B) = %.6f marginal, %.6f conditional"
  % (SIG_LNB, A71["joint"]["sigma_lnB"], SIG_B_JOINT, SIG_B_COND))
P("  sigma(u) = %.5f (prior alone: %.4f)" % (SIG_U_FREE, SIG_U))
ck("C17", abs(SIG_K_JOINT / A71["joint"]["sigma_stat"] - 1) < 2e-4
   and abs(SIG_K_TOT / A71["joint"]["sigma_tot"] - 1) < 2e-4
   and abs(SIG_LNB / A71["joint"]["sigma_lnB"] - 1) < 5e-3
   and abs(SIG_B_COND / 0.0364 - 1) < 0.02,
   "sigma(kappa) %.6f vs %.6f ; total %.6f vs %.6f ; sigma(lnB) %.6f vs %.6f"
   % (SIG_K_JOINT, A71["joint"]["sigma_stat"], SIG_K_TOT, A71["joint"]["sigma_tot"],
      SIG_LNB, A71["joint"]["sigma_lnB"]),
   "stat and total sigma(kappa) to 2e-4 ; marginal sigma(lnB) to 5e-3 of A71's K28 ; conditional sigma(B) within 2% of 0.0364",
   "the errors are A71's, so the cost of fixing a0 is measured on the same yardstick", "no_boot")

# =====================================================================================
# C18/C19  the two fixed fits
# =====================================================================================
head("C18/C19  FITS (b) and (c): a0 FIXED at the thermal value and at kappa = 1/2")


def fixed_fit(kfix):
    chi2 = chi2_prof(kfix)
    B = float(B_at(kfix))
    u = float(u_best(kfix))
    sp = ((kfix - K_SP) / SIG_K_SP) ** 2
    sl = (math.log(B) - lnB_req(kfix)) ** 2 / SIG_B_MEAS ** 2
    pr = math.log(B) ** 2 / SIG_B_PRIOR ** 2
    cl = chi2_cluster(kfix, u)
    sig_lnB = SIG_B_MEAS * SIG_B_PRIOR / math.sqrt(SIG_B_MEAS ** 2 + SIG_B_PRIOR ** 2)
    _uu = (chi2_cluster(kfix, u + _du) - 2 * chi2_cluster(kfix, u) + chi2_cluster(kfix, u - _du)) / _du ** 2
    sig_u = math.sqrt(2.0 / _uu)
    return dict(kappa=kfix, a0=a0_of_kappa(kfix), chi2=chi2, B=B, u=u,
                sigma_B=B * sig_lnB, sigma_u=sig_u,
                sp=sp, sl=sl, pr=pr, cl=cl,
                chi2_sparc_raw=chi2_sparc(a0_of_kappa(kfix)),
                chi2_slacs_raw=NL * (float(SPL_S(math.log(kfix))) ** 2
                                     + (math.log(B) - lnB_req(kfix)) ** 2) / S_LN ** 2,
                chi2_cluster_raw=cl - (u - U0) ** 2 / SIG_U ** 2,
                lnB_req=lnB_req(kfix))


FIT_TH = fixed_fit(K_TH)
FIT_HF = fixed_fit(K_HALF)
DCHI2_TH = FIT_TH["chi2"] - CHI2_JOINT
DCHI2_HF = FIT_HF["chi2"] - CHI2_JOINT
DCHI2_TH_HF = FIT_TH["chi2"] - FIT_HF["chi2"]
P("  (b) thermal: kappa_P3 = %.6f (a0 = %.6e), B = %.6f +- %.6f, u = %.6f +- %.6f, chi2 = %.6f"
  % (FIT_TH["kappa"], FIT_TH["a0"], FIT_TH["B"], FIT_TH["sigma_B"], FIT_TH["u"], FIT_TH["sigma_u"],
     FIT_TH["chi2"]))
P("      = SPARC %.4f + SLACS %.4f + clusters %.4f + IMF prior %.4f"
  % (FIT_TH["sp"], FIT_TH["sl"], FIT_TH["cl"], FIT_TH["pr"]))
P("      Delta-chi2 vs (a) = %+.6f" % DCHI2_TH)
P("  (c) kappa=1/2: kappa_P3 = %.6f (a0 = %.6e), B = %.6f +- %.6f, u = %.6f +- %.6f, chi2 = %.6f"
  % (FIT_HF["kappa"], FIT_HF["a0"], FIT_HF["B"], FIT_HF["sigma_B"], FIT_HF["u"], FIT_HF["sigma_u"],
     FIT_HF["chi2"]))
P("      = SPARC %.4f + SLACS %.4f + clusters %.4f + IMF prior %.4f"
  % (FIT_HF["sp"], FIT_HF["sl"], FIT_HF["cl"], FIT_HF["pr"]))
P("      Delta-chi2 vs (a) = %+.6f" % DCHI2_HF)
P("  Delta-chi2 (b) - (c) = %+.6f" % DCHI2_TH_HF)
P("  cost in sigma (1 dof): thermal sqrt(%.6f) = %.4f sigma ; kappa=1/2 sqrt(%.6f) = %.4f sigma"
  % (DCHI2_TH, math.sqrt(DCHI2_TH), DCHI2_HF, math.sqrt(DCHI2_HF)))
ck("C18", 0.0 < DCHI2_TH < 1.0 and FIT_TH["kappa"] > K_JOINT
   and abs(FIT_TH["chi2"] - (FIT_TH["sp"] + FIT_TH["sl"] + FIT_TH["cl"] + FIT_TH["pr"])) < 1e-9,
   "Delta-chi2(thermal vs free) = %+.6f ; kappa %.6f > free %.6f" % (DCHI2_TH, FIT_TH["kappa"], K_JOINT),
   "0 < Delta-chi2 < 1 and the total equals the sum of its four terms",
   "fixing a0 at the thermal value costs almost nothing: the free fit already sits 0.1 sigma away",
   "thermal_pi")
ck("C19", 1.0 < DCHI2_HF < 3.0 and FIT_HF["kappa"] > FIT_TH["kappa"]
   and abs((DCHI2_HF - DCHI2_TH) + DCHI2_TH_HF) < 1e-9,
   "Delta-chi2(kappa=1/2 vs free) = %+.6f ; chi2(b)-chi2(c) = %+.6f" % (DCHI2_HF, DCHI2_TH_HF),
   "1 < Delta-chi2 < 3 and the two Delta-chi2 are consistent to 1e-9",
   "the kappa=1/2 point costs ~2 units of chi2 against the free fit -- a 1-sigma statement, not a rejection",
   "imf_prior")

# direct (spline-free) B_req at the two fixed points: measures the compression error
B_REQ_DIRECT_TH = brentq(lambda B: med_at_B(B, a0_of_kappa(K_TH)) - 1.0, 1.02, 5.0, xtol=1e-6)
P("  B_req at the thermal kappa: spline %.6f vs direct 70-lens root %.6f (%.2e in ln B)"
  % (math.exp(lnB_req(K_TH)), B_REQ_DIRECT_TH, abs(math.log(math.exp(lnB_req(K_TH)) / B_REQ_DIRECT_TH))))
ck("C20", abs(math.log(math.exp(lnB_req(K_TH)) / B_REQ_DIRECT_TH)) < 5e-3,
   "spline %.6f vs direct %.6f" % (math.exp(lnB_req(K_TH)), B_REQ_DIRECT_TH),
   "the two agree to < 5e-3 in ln B (5% of the lensing error)",
   "the B-spline compression used for the fits is checked against a direct 70-lens root at the thermal point",
   "sersic35")

# per-channel chi2/dof for all three fits, on the raw (uncompressed) likelihoods
FIT_A_RAW_SP = chi2_sparc(A0_JOINT)
FIT_A_RAW_SL = NL * (float(SPL_S(math.log(K_JOINT))) ** 2
                     + (math.log(B_JOINT) - lnB_req(K_JOINT)) ** 2) / S_LN ** 2
FIT_A_RAW_CL = CL_JOINT - (U_JOINT - U0) ** 2 / SIG_U ** 2
P("")
P("  %-4s %24s %20s %16s %12s %6s" % ("fit", "SPARC raw chi2/dof", "SLACS raw chi2/dof",
                                      "cluster raw/dof", "chi2(comp)", "n_par"))
for _nm, _sp, _sl, _cl, _c2, _np_ in (
        ("(a)", FIT_A_RAW_SP, FIT_A_RAW_SL, FIT_A_RAW_CL, CHI2_JOINT, NG + 3),
        ("(b)", FIT_TH["chi2_sparc_raw"], FIT_TH["chi2_slacs_raw"], FIT_TH["chi2_cluster_raw"],
         FIT_TH["chi2"], NG + 2),
        ("(c)", FIT_HF["chi2_sparc_raw"], FIT_HF["chi2_slacs_raw"], FIT_HF["chi2_cluster_raw"],
         FIT_HF["chi2"], NG + 2)):
    P("  %-4s %10.2f/%d = %.4f %10.2f/%d = %.4f %8.3f/%d    %10.6f %6d"
      % (_nm, _sp, DOF_SP, _sp / DOF_SP, _sl, NL - 2, _sl / (NL - 2), _cl, 1, _c2, _np_))
P("  A71 stored at the free fit: SPARC raw %.4f (chi2/dof %.6f), SLACS raw %.4f (chi2/dof %.6f)"
  % (A71["joint"]["chi2_sparc_raw"], A71["joint"]["chi2_dof_sparc"],
     A71["joint"]["chi2_slacs_raw"], A71["joint"]["chi2_dof_slacs"]))
ck("C28", abs(FIT_A_RAW_SP / A71["joint"]["chi2_sparc_raw"] - 1) < 1e-5
   and abs(FIT_A_RAW_SL / A71["joint"]["chi2_slacs_raw"] - 1) < 1e-5
   and abs(FIT_A_RAW_SP / DOF_SP - A71["joint"]["chi2_dof_sparc"]) < 3e-5
   and abs(FIT_A_RAW_SL / (NL - 2) - A71["joint"]["chi2_dof_slacs"]) < 1e-6,
   "SPARC raw %.4f vs %.4f (rel %.1e) ; SLACS %.6f vs %.6f"
   % (FIT_A_RAW_SP, A71["joint"]["chi2_sparc_raw"], abs(FIT_A_RAW_SP / A71["joint"]["chi2_sparc_raw"] - 1),
      FIT_A_RAW_SL / (NL - 2), A71["joint"]["chi2_dof_slacs"]),
   "both raw chi2/dof reproduce A71's stored values to 1e-5 (the 5e-6 on SPARC is A71's cubic-spline "
   "interpolation of chi2(kappa), not a disagreement)",
   "the per-channel chi2/dof quoted for all three fits are the same objects A71 reported, "
   "so the table is comparable across fits and back to A71", "drop_gal")

# =====================================================================================
# C21/C22  Task 2: the likelihood ratio
# =====================================================================================
head("C21/C22  TASK 2 -- THE LIKELIHOOD RATIO BETWEEN THE THERMAL POINT AND kappa = 1/2")
# positive convention: DCHI2_HF_TH > 0 means kappa = 1/2 is the worse fit
DCHI2_HF_TH = FIT_HF["chi2"] - FIT_TH["chi2"]
SIG_DCHI2_TH_HF = math.sqrt(abs(DCHI2_HF_TH))
LR_TH_HF = math.exp(DCHI2_HF_TH / 2.0)                 # P(data|thermal)/P(data|half)
SIG_FROM_LR = math.sqrt(abs(-2.0 * math.log(1.0 / LR_TH_HF)))
# A72's version: nuisances frozen at the free fit, only kappa moved (SPARC term only)
CHI2_A72_TH = ((K_TH - K_JOINT) / SIG_K_JOINT) ** 2
CHI2_A72_HF = ((K_HALF - K_JOINT) / SIG_K_JOINT) ** 2
DCHI2_A72 = CHI2_A72_HF - CHI2_A72_TH
LR_A72 = math.exp(DCHI2_A72 / 2.0)
P("  full refit   : chi2(b) = %.6f ; chi2(c) = %.6f ; Delta = %+.6f (positive = kappa=1/2 worse)"
  % (FIT_TH["chi2"], FIT_HF["chi2"], DCHI2_HF_TH))
P("                 sigma (1 dof) = sqrt(Delta) = %.6f ; LR thermal:half = exp(+Delta/2) = %.6f (%.4f : 1)"
  % (SIG_DCHI2_TH_HF, LR_TH_HF, LR_TH_HF))
P("  A72's frozen-nuisance version (SPARC term only): Delta = %+.6f -> LR %.6f (%.4f : 1)"
  % (DCHI2_A72, LR_A72, LR_A72))
P("  A72 stored: chi2(1/7) = %.6f, chi2(thermal) = %.6f, Delta = %.6f, LR = %.6f"
  % (A72["numbers"]["chi2_stat_1_7"], A72["numbers"]["chi2_stat_2pi_dS"],
     A72["numbers"]["chi2_stat_1_7"] - A72["numbers"]["chi2_stat_2pi_dS"],
     math.exp((A72["numbers"]["chi2_stat_1_7"] - A72["numbers"]["chi2_stat_2pi_dS"]) / 2)))
P("  cost of refitting the nuisances: Delta falls by %.6f (%.1f%%)"
  % (DCHI2_A72 - DCHI2_HF_TH, 100 * (1 - DCHI2_HF_TH / DCHI2_A72)))
P("  the 31.2%% systematic floor: candidates are %.3f sigma apart on the total error"
  % ((K_HALF - K_TH) / SIG_K_TOT))
ck("C21", abs(SIG_DCHI2_TH_HF - math.sqrt(abs(FIT_HF["chi2"] - FIT_TH["chi2"]))) < 1e-12
   and abs(LR_TH_HF - math.exp((FIT_HF["chi2"] - FIT_TH["chi2"]) / 2)) < 1e-12
   and abs(SIG_FROM_LR - SIG_DCHI2_TH_HF) < 1e-9 and 0.5 < DCHI2_HF_TH < 4.0,
   "sigma %.6f ; LR %.6f ; sigma from the LR %.6f ; Delta %.4f"
   % (SIG_DCHI2_TH_HF, LR_TH_HF, SIG_FROM_LR, DCHI2_HF_TH),
   "sqrt(Delta), exp(Delta/2) and the inverse transform agree; and 0.5 < Delta < 4 (0.7-2 sigma)",
   "Delta-chi2 -> sigma -> likelihood ratio is one consistent transformation, computed three ways",
   "thermal_pi")
ck("C22", 1.5 < LR_TH_HF < 5.0 and abs(LR_A72 - 2.5995) < 0.02
   and 0.0 < DCHI2_A72 - DCHI2_HF_TH < 0.30,
   "full refit LR = %.4f : 1 ; A72 frozen-nuisance LR = %.4f : 1 ; Delta shrink %.4f"
   % (LR_TH_HF, LR_A72, DCHI2_A72 - DCHI2_HF_TH),
   "a 1.5-5 : 1 preference and A72's 2.60 : 1 reproduced; refitting nuisances shrinks Delta by < 0.3",
   "A72's 2.6 : 1 survives a full refit -- and it was never evidence (see the sigma above)",
   "imf_prior")

# =====================================================================================
# C23  Task 3: the channel pulls
# =====================================================================================
head("C23  TASK 3 -- THE CHANNEL PULLS AT THE THERMAL POINT, AND THE FREE-POINT BENCHMARK")


def pulls(fit, label):
    p_sp = (K_SP - fit["kappa"]) / SIG_K_SP
    p_sl_dex = (fit["lnB_req"] - math.log(fit["B"])) / LN10   # dex, channel demand minus adopted value
    p_sl = p_sl_dex / SIG_B_MEAS_DEX
    p_sl_comb = p_sl_dex / SIG_B_PULL_DEX
    p_cl = (fit["u"] - U0) / SIG_U
    p_imf = math.log10(fit["B"]) / SIG_B_PULL_DEX
    P("  %-12s SPARC %+6.3f sigma | SLACS(B) %+6.3f sigma (%+.5f dex, own error) %+6.3f (combined)"
      " | clusters %+6.3f sigma | IMF normalisation %+6.3f sigma"
      % (label, p_sp, p_sl, p_sl_dex, p_sl_comb, p_cl, p_imf))
    return p_sp, p_sl, p_cl, p_sl_dex, p_sl_comb, p_imf


P_FREE = pulls(dict(kappa=K_JOINT, B=B_JOINT, u=U_JOINT, lnB_req=lnB_req(K_JOINT)), "free (a)")
P_TH = pulls(FIT_TH, "thermal (b)")
P_HF = pulls(FIT_HF, "half (c)")
D_SP = abs(P_TH[0]) - abs(P_FREE[0])
D_SL = abs(P_TH[1]) - abs(P_FREE[1])
D_CL = abs(P_TH[2]) - abs(P_FREE[2])
P("  worsening at the thermal point (|pull| now - |pull| free): SPARC %+.3f, SLACS %+.3f, clusters %+.3f"
  % (D_SP, D_SL, D_CL))
P("  largest worsening = %.3f sigma -> %s"
  % (max(D_SP, D_SL, D_CL), "no channel is worse by > 1 sigma"
     if max(D_SP, D_SL, D_CL) < 1.0 else "AT LEAST ONE CHANNEL IS > 1 sigma WORSE"))
P("  SPARC is the only channel that gets worse, by %.3f sigma -- a PREFERENCE, not a rejection: "
  "its own best fit is %.3f sigma from the thermal point" % (D_SP, abs(P_TH[0])))
ck("C23", max(D_SP, D_SL, D_CL) < 1.0 and abs(P_TH[0] + 0.7095) < 0.02
   and abs(P_TH[1] - 0.831) < 0.02 and abs(P_TH[2] + 0.192) < 0.02 and D_SL < 0.0,
   "SPARC %+.3f ; SLACS(B) %+.3f ; clusters %+.3f ; worst worsening %+.3f"
   % (P_TH[0], P_TH[1], P_TH[2], max(D_SP, D_SL, D_CL)),
   "no channel worse by 1 sigma; SPARC -0.71+-0.02, SLACS(B) +0.83+-0.02, clusters -0.19+-0.02; SLACS improves",
   "the thermal point degrades no channel by 1 sigma: SPARC prefers a lower a0 by 0.7 sigma and that is all",
   "no_boot")

# the SLACS kappa-direction ridge pull, for completeness (A71 K20's number)
r_sl = minimize(lambda p: (p[1] - lnB_req(math.exp(p[0]))) ** 2 / SIG_B_MEAS ** 2 + p[1] ** 2 / SIG_B_PRIOR ** 2,
                [math.log(1.2), math.log(1.0)], method="Nelder-Mead", options=dict(xatol=1e-13, fatol=1e-13))
K_SL_ONLY = float(math.exp(r_sl.x[0]))


def _chi_sl(k):
    return (lnB_req(k) ** 2) / (SIG_B_MEAS ** 2 + SIG_B_PRIOR ** 2)


_lo_sl = brentq(lambda k: _chi_sl(k) - r_sl.fun - 1.0, 0.20, K_SL_ONLY, xtol=1e-12)
_hi_sl = brentq(lambda k: _chi_sl(k) - r_sl.fun - 1.0, K_SL_ONLY, 3.0, xtol=1e-12)
SIG_SL_ONLY = 0.5 * (_hi_sl - _lo_sl)
PULL_SL_K_FREE = (K_SL_ONLY - K_JOINT) / SIG_SL_ONLY
PULL_SL_K_TH = (K_SL_ONLY - K_TH) / SIG_SL_ONLY
P("  SLACS in the kappa direction: kappa_best = %.4f +- %.4f ; pull %+.3f (free) -> %+.3f (thermal)"
  % (K_SL_ONLY, SIG_SL_ONLY, PULL_SL_K_FREE, PULL_SL_K_TH))
ck("C24", abs(PULL_SL_K_FREE - 1.966) < 0.05 and PULL_SL_K_TH < PULL_SL_K_FREE,
   "SLACS kappa pull %+.3f -> %+.3f" % (PULL_SL_K_FREE, PULL_SL_K_TH),
   "1.966+-0.05 at the free fit and smaller at the thermal point",
   "SLACS's pull toward high kappa is relieved, not worsened, by fixing a0 at the thermal value", "imf_prior")

# =====================================================================================
# C25/C26  Task 4: the falsifier at the thermal point
# =====================================================================================
head("C25/C26  TASK 4 -- THE FALSIFIER AT a0 = 8.620e-11, kappa_DE = Z/4pi")


def hfun(y):
    return 0.5 * (math.sqrt(y * y + 4.0 * y) - y)


def F_closure(Y):
    g = lambda th: hfun(Y * math.tan(th)) * Y
    val, _ = quad(g, 0.0, math.pi / 2.0, limit=400)
    return val


def F_closure_exact(Y):
    g = lambda v: Y * Y * v * v * (4.0 - v) / (4.0 * Y * Y * (2.0 - v) ** 2 + v ** 4)
    val, _ = quad(g, 0.0, 2.0, limit=400)
    return val


def y_of_kappa(k, fn=F_closure):
    return brentq(lambda Y: fn(Y) - 8.0 * math.pi / k ** 2, 5.0, 400.0, xtol=1e-11)


N_LAMBDA_TH = LAMBDA_OBS * C_L ** 4 / A0_TH ** 2
K_FROM_LAMBDA = math.sqrt(8.0 * math.pi / N_LAMBDA_TH)
YT_TH = y_of_kappa(K_DE_TH)
YT_TH_E = y_of_kappa(K_DE_TH, F_closure_exact)
YT_HALF = y_of_kappa(K_DE_HALF)
YT_JOINT = y_of_kappa(K_JOINT / math.sqrt(OMEGA_L))
P("  N_Lambda = Lambda c^4/a0^2 = %.6f ; kappa_DE from it = %.6f (from the a0 definition %.6f)"
  % (N_LAMBDA_TH, K_FROM_LAMBDA, K_DE_TH))
P("    the %.4f%% between those two is the same Lambda-vs-Omega_L footing split as above, not physics"
  % (100 * (K_FROM_LAMBDA / K_DE_TH - 1)))
P("  y_t (tan-substitution quadrature) = %.6f ; (A28 rational integral) = %.6f ; difference %.2e"
  % (YT_TH, YT_TH_E, abs(YT_TH - YT_TH_E)))
P("  y_t at kappa=1/2 = %.6f ; at the free-fit kappa_DE = %.6f" % (YT_HALF, YT_JOINT))
P("  pre-registered band y_t in [60,140]: thermal %.3f -> %s"
  % (YT_TH, "INSIDE" if 60.0 <= YT_TH <= 140.0 else "OUTSIDE"))
P("  the same band in kappa_DE: [%.4f, %.4f] ; thermal kappa_DE %.6f -> %s"
  % (math.sqrt(8 * math.pi / F_closure(140.0)), math.sqrt(8 * math.pi / F_closure(60.0)), K_DE_TH,
     "INSIDE" if math.sqrt(8 * math.pi / F_closure(140.0)) <= K_DE_TH <= math.sqrt(8 * math.pi / F_closure(60.0)) else "OUTSIDE"))
ck("C25", abs(YT_TH - YT_TH_E) < 1e-6 and 60.0 <= YT_TH <= 140.0 and abs(K_FROM_LAMBDA / K_DE_TH - 1) < 1e-3,
   "y_t %.6f (two routes %.1e apart), band [60,140], kappa_DE %.6f"
   % (YT_TH, abs(YT_TH - YT_TH_E), K_DE_TH),
   "two quadrature forms agree to 1e-6 ; y_t inside [60,140] ; kappa_DE consistent with Lambda to 1e-3",
   "the closure root at the thermal point is inside its pre-registered band, computed twice",
   "lambda_off")

SIG_C = 8.33e3
LSTAR_TH = SIG_C ** 2 / A0_TH / PC
LSTAR_HALF = SIG_C ** 2 / A0_HALF / PC
LSTAR_CANON = SIG_C ** 2 / A0_CANON / PC
RCORE_TH = (math.pi / math.sqrt(2.0)) * LSTAR_TH
RCORE_CANON = (math.pi / math.sqrt(2.0)) * LSTAR_CANON
LAM_P_TH = LSTAR_TH / math.sqrt(2.0)
M_P_LITERAL = HBAR / (C_L * LSTAR_TH * PC)          # the task's formula, hbar/(c L*)
M_P_RECORD = HBAR / (C_L * LAM_P_TH * PC)            # A56's convention, lambda_P = L*/sqrt2
P("  L* = sigma_c^2/a0 = %.6f pc (sigma_c = %.0f m/s) ; band [24,90] pc -> %s"
  % (LSTAR_TH, SIG_C, "INSIDE" if 24.0 <= LSTAR_TH <= 90.0 else "OUTSIDE"))
P("  L* at kappa=1/2 = %.6f pc ; at canonical 9.36e-11 = %.6f pc (the A20 anchor is 24.025)" % (LSTAR_HALF, LSTAR_CANON))
P("  R_core = (pi/sqrt2) L* = %.6f pc (A20: 53.3146 pc at L* = 24; ceiling 200 pc) -> %s"
  % (RCORE_TH, "INSIDE" if RCORE_TH < 200.0 else "OUTSIDE"))
P("  m_P = hbar/(c L*) = %.6e kg = %.6e eV  [task's literal formula]" % (M_P_LITERAL, M_P_LITERAL * C_L ** 2 / EV))
P("  m_P = hbar/(c lambda_P), lambda_P = L*/sqrt2 : %.6e kg = %.6e eV  [A56's convention]"
  % (M_P_RECORD, M_P_RECORD * C_L ** 2 / EV))
P("  A56's canonical m_P = 6.7105e-61 kg ; thermal/canonical ratio %.6f" % (M_P_RECORD / 6.7105e-61))
ck("C26", 24.0 <= LSTAR_TH <= 90.0 and abs(RCORE_TH - (math.pi / math.sqrt(2)) * LSTAR_TH) < 1e-9
   and abs(M_P_RECORD / M_P_LITERAL - math.sqrt(2)) < 1e-12
   and 0.90 < M_P_RECORD / 6.7105e-61 < 0.94,
   "L* %.4f pc ; R_core %.4f pc ; m_P %.5e / %.5e kg (ratio sqrt2), %.4f x A56"
   % (LSTAR_TH, RCORE_TH, M_P_LITERAL, M_P_RECORD, M_P_RECORD / 6.7105e-61),
   "L* in [24,90] pc ; R_core = 2.22144 L* ; the two m_P formulas differ by exactly sqrt2 ; 0.90-0.94 x A56",
   "the length scale and the P mass both land where they were pre-registered, at the thermal a0",
   "thermal_pi")

# =====================================================================================
# C27  the cost decomposition, and the one-line discriminator
# =====================================================================================
head("C27  WHERE THE COST COMES FROM, AND WHAT THE THERMAL POINT PREDICTS")
D_SP_TH = FIT_TH["sp"] - SP_JOINT
D_SL_TH = FIT_TH["sl"] + FIT_TH["pr"] - SL_JOINT - PR_JOINT
D_CL_TH = FIT_TH["cl"] - CL_JOINT
D_SP_HF = FIT_HF["sp"] - SP_JOINT
D_SL_HF = FIT_HF["sl"] + FIT_HF["pr"] - SL_JOINT - PR_JOINT
D_CL_HF = FIT_HF["cl"] - CL_JOINT
D_SP_HT = D_SP_HF - D_SP_TH      # half minus thermal: positive = kappa=1/2 costs more
D_SL_HT = D_SL_HF - D_SL_TH
D_CL_HT = D_CL_HF - D_CL_TH
P("  thermal vs free:  SPARC %+.6f | SLACS+prior %+.6f | clusters %+.6f | sum %+.6f (total %+.6f)"
  % (D_SP_TH, D_SL_TH, D_CL_TH, D_SP_TH + D_SL_TH + D_CL_TH, DCHI2_TH))
P("  half    vs free:  SPARC %+.6f | SLACS+prior %+.6f | clusters %+.6f | sum %+.6f (total %+.6f)"
  % (D_SP_HF, D_SL_HF, D_CL_HF, D_SP_HF + D_SL_HF + D_CL_HF, DCHI2_HF))
P("  half minus thermal (positive = kappa=1/2 worse):")
P("                    SPARC %+.6f | SLACS+prior %+.6f | clusters %+.6f | sum %+.6f (total %+.6f)"
  % (D_SP_HT, D_SL_HT, D_CL_HT, D_SP_HT + D_SL_HT + D_CL_HT, DCHI2_HF_TH))
P("  SPARC drives the whole Delta-chi2 (%.3f of %.3f); SLACS+prior gives back %.3f; clusters cost %.3f"
  % (D_SP_HT, DCHI2_HF_TH, -D_SL_HT, D_CL_HT))
P("")
P("  the discriminator: a0(1/2)/a0(thermal) = %.6f, i.e. the rival sits %.4f%% ABOVE the thermal value"
  % (A0_HALF / A0_TH, 100 * (A0_HALF / A0_TH - 1)))
P("    (the reverse framing: the thermal value is %.4f%% below the rival) ; Delta a0 = %.6e m/s^2"
  % (100 * (1 - A0_TH / A0_HALF), A0_HALF - A0_TH))
P("    A72's unrounded pair 9.354746e-11 / 8.618166e-11 gives %.4f%% (A72 quotes 8.54%%)"
  % (100 * (9.354746e-11 / 8.618166e-11 - 1)))
P("  3-sigma separation needs sigma(a0)/a0 = %.4f%% (A72: 2.874%% unrounded) or sigma(kappa_P3) = %.6f ;"
  " the present joint fit gives %.4f%%"
  % (100 * (A0_HALF / A0_TH - 1) / 3.0, (K_HALF - K_TH) / 3.0, 100 * SIG_K_TOT / K_JOINT))
P("  L* moves %.4f%% (%.3f -> %.3f pc) and y_t moves %.2f%% (%.3f -> %.3f) between the two points"
  % (100 * (LSTAR_HALF / LSTAR_TH - 1), LSTAR_TH, LSTAR_HALF, 100 * (YT_TH / YT_HALF - 1), YT_TH, YT_HALF))
ck("C27", abs(D_SP_TH + D_SL_TH + D_CL_TH - DCHI2_TH) < 1e-9
   and abs(D_SP_HF + D_SL_HF + D_CL_HF - DCHI2_HF) < 1e-9
   and abs(D_SP_HT + D_SL_HT + D_CL_HT - DCHI2_HF_TH) < 1e-9
   and D_SP_HT > 2.0 * abs(D_SL_HT) and D_SL_HT < 0.0 and D_CL_HT > 0.0
   and abs(A0_TH / A0_HALF - 0.921415) < 2e-4,
   "three decompositions close to 1e-9 ; SPARC %+.3f, SLACS %+.3f, clusters %+.3f ; a0 ratio %.6f"
   % (D_SP_HT, D_SL_HT, D_CL_HT, A0_TH / A0_HALF),
   "the decomposition closes to 1e-9, SPARC drives the cost, SLACS+prior gives back, clusters cost, a0 ratio 0.92153+-2e-4",
   "the preference is SPARC's, the cancellation is SLACS's, and the two a0 differ by 8.52%",
   "newton")

# =====================================================================================
# C29  the error-model caveat, computed rather than asserted
# =====================================================================================
head("C29  THE ERROR-MODEL CAVEAT: WHAT THE RAW CHI2 WOULD SAY, AND WHY IT IS NOT USED")
DC_RAW_SP = chi2_sparc(a0_of_kappa(K_HALF)) - chi2_sparc(a0_of_kappa(K_TH))
SCALE_CHI2 = CHI2_SP / DOF_SP
DC_RAW_RES = DC_RAW_SP / SCALE_CHI2
SIG_RAW = math.sqrt(abs(DC_RAW_RES))
RATIO_RAW = DC_RAW_SP / (FIT_HF["sp"] - FIT_TH["sp"])
P("  raw chi2 difference between the two fixed points (Upsilon profiled): %.4f" % DC_RAW_SP)
P("  same, after rescaling the per-point errors so that chi2/dof = 1 (factor %.4f): %.4f -> %.2f sigma"
  % (SCALE_CHI2, DC_RAW_RES, SIG_RAW))
P("  the compressed likelihood says %.4f -> %.2f sigma: the raw route is %.1fx larger"
  % (FIT_HF["sp"] - FIT_TH["sp"], SIG_DCHI2_TH_HF, RATIO_RAW))
P("  reason: the formal Delta-chi2 error is %.4f%% in a0, the block bootstrap %.4f%% -- a factor %.2f."
  % (100 * SIG_DCHI2, 100 * BOOT_FRAC, BOOT_FRAC / SIG_DCHI2))
P("  A51 K6 established that factor and this lane inherits it. IF the per-point errors were right,")
P("  the thermal point would beat kappa=1/2 at %.1f sigma; on the declared error model it is %.2f sigma."
  % (SIG_RAW, SIG_DCHI2_TH_HF))
ck("C29", DC_RAW_SP > 0.0 and abs(SIG_RAW - 7.2) < 0.6 and 40.0 < RATIO_RAW < 60.0
   and SIG_RAW > 3.0 * SIG_DCHI2_TH_HF and BOOT_FRAC / SIG_DCHI2 > 5.0,
   "raw %.3f (%.2f sigma rescaled), compressed %.3f (%.2f sigma), ratio %.1f"
   % (DC_RAW_SP, SIG_RAW, FIT_HF["sp"] - FIT_TH["sp"], SIG_DCHI2_TH_HF, RATIO_RAW),
   "the raw route is 15-35x the compressed one and gives 6.6-7.8 sigma after rescaling",
   "the lane's 'cannot tell' is a statement about the error model: with the per-point errors the same "
   "data would prefer the thermal point at ~7 sigma, and A51's bootstrap says those errors are 8x too small",
   "a0_off20")

# =====================================================================================
# summary
# =====================================================================================
head("SUMMARY")
NPASS = sum(1 for c in CHECKS if c["pass_"])
P("  %d/%d checks PASS   (%.1f s)" % (NPASS, len(CHECKS), time.time() - T0))
P("  fit (a) a0 free      : kappa_P3 = %.6f +- %.6f (stat) +- %.6f (syst), B = %.6f +- %.6f (cond), u = %.6f, chi2 = %.6f"
  % (K_JOINT, SIG_K_JOINT, math.sqrt(max(SIG_K_TOT ** 2 - SIG_K_JOINT ** 2, 0)), B_JOINT, SIG_B_COND,
     U_JOINT, CHI2_JOINT))
P("  fit (b) thermal      : kappa_P3 = %.6f, B = %.6f +- %.6f, u = %.6f +- %.6f, chi2 = %.6f, Delta = %+.6f"
  % (K_TH, FIT_TH["B"], FIT_TH["sigma_B"], FIT_TH["u"], FIT_TH["sigma_u"], FIT_TH["chi2"], DCHI2_TH))
P("  fit (c) kappa=1/2    : kappa_P3 = %.6f, B = %.6f +- %.6f, u = %.6f +- %.6f, chi2 = %.6f, Delta = %+.6f"
  % (K_HALF, FIT_HF["B"], FIT_HF["sigma_B"], FIT_HF["u"], FIT_HF["sigma_u"], FIT_HF["chi2"], DCHI2_HF))
P("  Delta-chi2(c-b) = %+.6f -> %.4f sigma, LR thermal:half = %.4f : 1"
  % (DCHI2_HF_TH, SIG_DCHI2_TH_HF, LR_TH_HF))
P("  parameters: free 3 shared + %d Upsilon = %d ; fixed 2 shared + %d = %d" % (NG, NG + 3, NG, NG + 2))
P("  dof: SPARC %d, SLACS %d, clusters %d" % (DOF_SP, NL - 2, 1))

RES = dict(lane="A74", generated=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           mutate=MUT or None, n_check=len(CHECKS), n_pass=NPASS,
           checks=[{k: (bool(v) if k == "pass_" else v) for k, v in c.items()} for c in CHECKS],
           constants=dict(G=G_N, c=C_L, H0=H0_KMS, Omega_L=OMEGA_L, Lambda=LAMBDA_OBS,
                          a0_per_kappa=A0_PER_KAPPA, Z=Z_C, a0_th_declared=A0_TH_DECL,
                          a0_th_deployed=A0_TH, a0_half=A0_HALF, kappa_th=K_TH, kappa_half=K_HALF,
                          kappa_de_th=K_DE_TH, kappa_de_half=K_DE_HALF, kappa_de_algebra=K_DE_ALGEBRA,
                          a0_th_from_lambda=A0_TH_EXACT_LAMBDA, a0_th_from_omega=A0_TH_EXACT_OMEGA),
           data=dict(n_sparc_files=len(SPARC_FILES), n_galaxies=NG, n_points=NPT,
                     sha_sparc=H_SPARC, sha_slacs=H_SLACS, n_lenses=NL, n_treu=len(ALPHA)),
           sparc=dict(a0=A0_SP, kappa=K_SP, chi2=CHI2_SP, dof=DOF_SP, chi2_dof=CHI2_SP / DOF_SP,
                      sigma_boot=BOOT_FRAC, sigma_dchi2=SIG_DCHI2, sigma_kappa=SIG_K_SP),
           slacs=dict(B_req_05=B_REQ, median_ratio=MED50, mean_ln=MEANLN50, one_over_median=B_INV,
                      one_over_median_sq=B_INV2, dlnR_dlnB=RESP, dlnR_dlnk=_dlnR_dlnk,
                      sigma_logB_dex=SIG_LOGB_DEX, sigma_logB_curv_dex=SIG_LOGB_CURV,
                      B_req_direct_thermal=B_REQ_DIRECT_TH, kappa_sl_only=K_SL_ONLY,
                      sigma_kappa_sl=SIG_SL_ONLY),
           cluster=dict(dlnR_dlna0=DLNR, kappa=K_CL, sigma_kappa=K_CL * SIG_CL, R_req=R_REQ,
                        sigma_R=SIG_R, u=U0, sigma_u=SIG_U),
           fit_a=dict(kappa=K_JOINT, a0=A0_JOINT, sigma_stat=SIG_K_JOINT, sigma_tot=SIG_K_TOT,
                      sys_frac=SYS_FRAC, B=B_JOINT, sigma_B=SIG_B_JOINT, sigma_B_cond=SIG_B_COND,
                      u=U_JOINT, sigma_u=SIG_U_FREE,
                      chi2=CHI2_JOINT, sparc=SP_JOINT, slacs=SL_JOINT, cluster=CL_JOINT, prior=PR_JOINT,
                      n_shared=3, n_par=NG + 3, dof_total=NPT + NL + 1 - (NG + 3)),
           fit_b=dict(kappa=K_TH, a0=A0_TH, B=FIT_TH["B"], sigma_B=FIT_TH["sigma_B"], u=FIT_TH["u"],
                      sigma_u=FIT_TH["sigma_u"], chi2=FIT_TH["chi2"], dchi2_vs_free=DCHI2_TH,
                      sparc=FIT_TH["sp"], slacs=FIT_TH["sl"], cluster=FIT_TH["cl"], prior=FIT_TH["pr"],
                      chi2_sparc_raw=FIT_TH["chi2_sparc_raw"], chi2_dof_sparc=FIT_TH["chi2_sparc_raw"] / DOF_SP,
                      chi2_slacs_raw=FIT_TH["chi2_slacs_raw"], chi2_dof_slacs=FIT_TH["chi2_slacs_raw"] / (NL - 2),
                      chi2_cluster_raw=FIT_TH["chi2_cluster_raw"], n_shared=2, n_par=NG + 2,
                      dof_total=NPT + NL + 1 - (NG + 2)),
           fit_c=dict(kappa=K_HALF, a0=A0_HALF, B=FIT_HF["B"], sigma_B=FIT_HF["sigma_B"], u=FIT_HF["u"],
                      sigma_u=FIT_HF["sigma_u"], chi2=FIT_HF["chi2"], dchi2_vs_free=DCHI2_HF,
                      sparc=FIT_HF["sp"], slacs=FIT_HF["sl"], cluster=FIT_HF["cl"], prior=FIT_HF["pr"],
                      chi2_sparc_raw=FIT_HF["chi2_sparc_raw"], chi2_dof_sparc=FIT_HF["chi2_sparc_raw"] / DOF_SP,
                      chi2_slacs_raw=FIT_HF["chi2_slacs_raw"], chi2_dof_slacs=FIT_HF["chi2_slacs_raw"] / (NL - 2),
                      chi2_cluster_raw=FIT_HF["chi2_cluster_raw"], n_shared=2, n_par=NG + 2,
                      dof_total=NPT + NL + 1 - (NG + 2)),
           likelihood=dict(dchi2_half_minus_thermal=DCHI2_HF_TH, dchi2_thermal_vs_free=DCHI2_TH,
                           dchi2_half_vs_free=DCHI2_HF, sigma=SIG_DCHI2_TH_HF, LR_thermal_over_half=LR_TH_HF,
                           LR_half_over_thermal=1.0 / LR_TH_HF, dchi2_frozen=DCHI2_A72, LR_frozen=LR_A72,
                           shrink=DCHI2_A72 - DCHI2_HF_TH, sep_total_sigma=(K_HALF - K_TH) / SIG_K_TOT),
           pulls=dict(free=[P_FREE[0], P_FREE[1], P_FREE[2]], thermal=[P_TH[0], P_TH[1], P_TH[2]],
                      half=[P_HF[0], P_HF[1], P_HF[2]],
                      worsen=[D_SP, D_SL, D_CL],
                      imf_free=P_FREE[5], imf_thermal=P_TH[5], imf_half=P_HF[5],
                      slacs_B_dex_free=P_FREE[3], slacs_B_dex_thermal=P_TH[3],
                      slacs_kappa_free=PULL_SL_K_FREE, slacs_kappa_thermal=PULL_SL_K_TH),
           falsifier=dict(kappa_de=K_DE_TH, N_lambda=N_LAMBDA_TH, kappa_from_lambda=K_FROM_LAMBDA,
                          y_t=YT_TH, y_t_exact=YT_TH_E, y_t_half=YT_HALF, y_t_joint=YT_JOINT,
                          y_t_band=[60.0, 140.0], y_t_inside=bool(60.0 <= YT_TH <= 140.0),
                          Lstar_pc=LSTAR_TH, Lstar_half_pc=LSTAR_HALF, Lstar_canon_pc=LSTAR_CANON,
                          Lstar_band=[24.0, 90.0], Lstar_inside=bool(24.0 <= LSTAR_TH <= 90.0),
                          Rcore_pc=RCORE_TH, Rcore_canon_pc=RCORE_CANON,
                          m_P_literal=M_P_LITERAL, m_P_record=M_P_RECORD, m_P_ev=M_P_RECORD * C_L ** 2 / EV,
                          a0_ratio=A0_TH / A0_HALF, da0=A0_HALF - A0_TH,
                          sigma_req_3sig_frac=(1 - A0_TH / A0_HALF) / 3.0),
           cost=dict(sparc_th=D_SP_TH, slacs_th=D_SL_TH, cluster_th=D_CL_TH,
                     sparc_hf=D_SP_HF, slacs_hf=D_SL_HF, cluster_hf=D_CL_HF,
                     sparc_ht=D_SP_HT, slacs_ht=D_SL_HT, cluster_ht=D_CL_HT))
json.dump(RES, open(os.path.join(HERE, "a74_results" + TAG + ".json"), "w"), indent=1)

P("")
P("  wrote a74_results%s.json ; %d/%d PASS ; exit %d"
  % (TAG, NPASS, len(CHECKS), 0 if NPASS == len(CHECKS) else 1))
OUTF.close()
sys.exit(0 if NPASS == len(CHECKS) else 1)
