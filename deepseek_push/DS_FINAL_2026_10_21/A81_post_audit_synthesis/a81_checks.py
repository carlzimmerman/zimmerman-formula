#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
A81 -- POST-AUDIT GLOBAL SYNTHESIS

The final joint likelihood with every parameter profiled at every grid point,
the exact parameter ledger, and the cross-lane identity audit.

CHANNELS (every parameter is profiled at every kappa):
  1. SPARC RAR        171 galaxies / 3375 points, one Upsilon per galaxy profiled
                      inside chi2_SPARC; compressed to a Gaussian in kappa with the
                      200-draw block-bootstrap width (A51/A71's declared error model).
  2. SLACS 70 lenses  the A70 Sersic-n=4 model, ONE shared B, profiled EXACTLY at
                      every kappa through the per-lens response: the full 70-term
                      quadratic in ln B is minimised, not a mean/SD compression.
  3. clusters         A18's R_req = 5.552 +- 0.427 with the sourcing fraction u
                      profiled at every kappa.
  4. sigma_ap (opt.)  A85's SDSS aperture dispersions, imported as the Gaussian
                      constraint B = B_sigma(kappa) +- s_cond; both the formal width
                      and A85's sqrt(chi2/dof)-inflated width are run.
  + the IMF prior B = 1.00 +- 0.036 dex (Treu+2010) on the shared B.

NOT in the likelihood, with the reason computed here:
  closure I(y_t) = 8 pi/kappa^2   -- an identity (C19)
  BAO/SNe/CMB                     -- kappa-blind, an exact LCDM relabelling (A71 K17)
  wide binaries                   -- a prediction, no data on disk
  Sersic n                        -- no per-lens n on disk (A80); A80's n-curve is
                                     imported as a declared systematic, not fitted.

TASK 2 is the ledger (nine symbols, five classes) and TASK 3 the identity audit.
Every number in report.md is printed here.

MUTATIONS.  A81_MUTATE=<name> changes ONE input and must break a named check.
  unprofile_B | no_boot | thermal_off | imf_prior | drop_sigma_ap | sersic_default
  | vacuum_beta | drop_lens | sd_at_b1 | floor10
  sd_at_b1 computes A80's "B profiled" column at boost = 1 -- exactly A71's SD_TAB defect.
  floor10 widens the SPARC per-point floor from 5% to 10%.
  thermal_off replaces the 1/(2 pi) by 1/pi (the factor-2 slip of the kind A79 found).
Exit 0 iff every check passes.

Run:     python3 a81_checks.py
Mutate:  A81_MUTATE=unprofile_B python3 a81_checks.py     (must exit 1)
"""
import os
import sys
import json
import math
import time
import glob
import hashlib

import numpy as np
from scipy.optimize import brentq, minimize, minimize_scalar
from scipy.special import gammainc
from scipy.interpolate import CubicSpline
from scipy.integrate import quad
from scipy.stats import chi2 as chi2dist

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.abspath(os.path.join(HERE, ".."))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))

MUT = (os.environ.get("A81_MUTATE", "") or "").strip()
MUTS = ("", "unprofile_B", "no_boot", "thermal_off", "imf_prior",
        "drop_sigma_ap", "sersic_default", "vacuum_beta", "drop_lens", "sd_at_b1", "floor10")
if MUT not in MUTS:
    sys.exit("unknown mutation: " + MUT)
TAG = ("_MUTATE_" + MUT) if MUT else ""

T0 = time.time()
OUTF = open(os.path.join(HERE, "a81" + TAG + ".out"), "w")
OUT = []


def P(s=""):
    s = str(s)
    print(s, flush=True)
    OUT.append(s)
    OUTF.write(s + "\n")


def head(t):
    P("")
    P("=" * 112)
    P(t)
    P("=" * 112)


CHECKS = []


def ck(cid, ok, measured, threshold, label=""):
    ok = bool(ok)
    CHECKS.append(dict(id=cid, pass_=ok, measured=str(measured),
                       threshold=str(threshold), label=label))
    P("  %-5s %s   %s" % (cid, "PASS" if ok else "FAIL", measured))
    P("         threshold: %s   :: %s" % (threshold, label))
    return ok


# =====================================================================================
# constants, conventions, and the two fixed points of the theory
# =====================================================================================
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
A0_PER_KAPPA = C_L * H0_SI / SQ_8PI3            # 2.262407e-10 m/s^2, A51's P3 convention
LAMBDA_OBS = 1.0890e-52                          # A28/A72's footing, m^-2
LN10 = math.log(10.0)
B4 = 7.669249934

# the algebraic thermal coefficient: a0 = c H_Lambda/(2 pi), H_Lambda = c sqrt(Lambda/3)
Z_COEF = 2.0 * math.sqrt(8.0 * math.pi / 3.0)
KAPPA_DE_ALG = Z_COEF / (4.0 * math.pi)          # = sqrt(2/(3 pi))
A0_THERM_LAMBDA = C_L * C_L * math.sqrt(LAMBDA_OBS / 3.0) / (2.0 * math.pi)
A0_THERM_H0 = C_L * H0_SI * math.sqrt(OMEGA_L) / (2.0 * math.pi)
A0_THERM_DEPLOYED = 8.6257e-11                   # deployed in A80/A85 and this session
if MUT == "thermal_off":                          # mutation: the temperature is divided by pi, not 2 pi
    A0_THERM_DEPLOYED = C_L * C_L * math.sqrt(LAMBDA_OBS / 3.0) / math.pi
A0_HALF = 9.354e-11                              # A74's declared kappa = 1/2 footing (= cH0/7 to 8e-5)
A0_P3_HALF = 1.1312e-10                           # the OTHER "1/2": kappa_P3 = 0.5 (A71's old target)


def kappa_p3(a0):
    """A51/A71's rho_crit convention: kappa = a0 sqrt(8 pi/3)/(c H0)."""
    return a0 * SQ_8PI3 / (C_L * H0_SI)


def a0_p3(k):
    return k * A0_PER_KAPPA


def kappa_de(a0):
    """The rho_DE convention: kappa_DE = a0 sqrt(8 pi)/(c H0 sqrt(3 Omega_L)) = kappa_P3/sqrt(Omega_L)."""
    return a0 * math.sqrt(8.0 * math.pi) / (C_L * H0_SI * math.sqrt(3.0 * OMEGA_L))


def sha_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


K_TH = kappa_p3(A0_THERM_DEPLOYED)
K_HF = kappa_p3(A0_HALF)
K_P3H = kappa_p3(A0_P3_HALF)

P("A81 -- POST-AUDIT GLOBAL SYNTHESIS      (mutation: %s)" % (MUT or "none"))
P("  lane dir %s" % HERE)
P("  generated %s   python %s" % (time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                                  sys.version.split()[0]))
P("  H0 = %.1f km/s/Mpc ; Omega_L = %.4f ; a0_per_kappa = %.9e m/s^2 (A51 P3 convention)"
  % (H0_KMS, OMEGA_L, A0_PER_KAPPA))
P("  thermal: cH_Lambda/2pi = %.9e (Lambda_obs route) / %.9e (H0 sqrt(Omega_L) route)"
  % (A0_THERM_LAMBDA, A0_THERM_H0))
P("  deployed a0_therm = %.6e ; kappa=1/2 footing a0 = %.6e (cH0/7 = %.9e) ; kappa_P3=1/2 at %.4e"
  % (A0_THERM_DEPLOYED, A0_HALF, C_L * H0_SI / 7.0, A0_P3_HALF))
P("  kappa_DE(algebraic) = Z/4pi = %.9f ; kappa_P3(thermal) = %.6f ; kappa_P3(1/2) = %.6f ; kappa_P3(0.5) = %.6f"
  % (KAPPA_DE_ALG, K_TH, K_HF, K_P3H))

# =====================================================================================
# C1  the data blocks
# =====================================================================================
head("C1  THE DATA BLOCKS: SPARC 171/3375, SLACS 70, Treu 56 -- read-only, hashed")

SPARC_DIR = os.path.join(REPO, "real_research", "data", "sparc_data")
SPARC_FILES = sorted(glob.glob(os.path.join(SPARC_DIR, "*_rotmod.dat")))
GAL = []
for _ifi, f in enumerate(SPARC_FILES):
    a = np.loadtxt(f, comments="#")
    if a.ndim != 2 or len(a) < 5:
        continue
    GAL.append(dict(name=os.path.basename(f)[:-len("_rotmod.dat")],
                    r=a[:, 0] * KPC, V=a[:, 1], eV=a[:, 2],
                    Vg=a[:, 3], Vd=a[:, 4], Vb=a[:, 5]))
NG = len(GAL)
NPT = int(sum(len(g["r"]) for g in GAL))
H_SPARC = hashlib.sha256(b"".join(open(f, "rb").read() for f in SPARC_FILES)).hexdigest()[:16]
H_SPARC_A51 = "469f4f556dc813b2"

DATA_SLACS = os.path.join(REPO, "real_research", "data", "slacs_auger2009_lenses.tsv")
DATA_TREU = os.path.join(REPO, "real_research", "cross_thread_review_2026_09_26",
                         "XR33_data_treu2010_table1.tsv")
A55JSON = os.path.join(LANE, "A55_lensing_prediction", "a55_results.json")

_lines = [ln.rstrip("\n") for ln in open(DATA_SLACS, encoding="latin-1")]
_hi = [i for i, ln in enumerate(_lines) if ln.startswith("recno")][0]
_hdr = _lines[_hi].split("\t")
_col = {c: i for i, c in enumerate(_hdr)}
_raw = [ln.split("\t") for ln in _lines[_hi + 3:] if ln.strip() and not ln.startswith("#")]


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
    if all(np.isfinite([d["zl"], d["zs"], d["RE"], d["lME"], d["Fs"], d["Fc"]])) and float(d["RE"]) > 0:
        LENS.append(d)
if MUT == "drop_lens":                      # mutation: a corrupted lens census (every 7th lens lost)
    LENS = [d for i, d in enumerate(LENS) if i % 7 != 3]
NL = len(LENS)
H_SLACS = sha_file(DATA_SLACS)

_tl = [ln.rstrip("\n") for ln in open(DATA_TREU, encoding="latin-1")]
_ti = [i for i, ln in enumerate(_tl) if ln.startswith("name")][0]
_th = _tl[_ti].split("\t")
_ic = {c: i for i, c in enumerate(_th)}
_tr = [ln.split("\t") for ln in _tl[_ti + 1:] if ln.strip() and not ln.startswith("#")]
ALPHA_TREU = np.array([float(r[_ic["log_alpha"]]) for r in _tr if len(r) == len(_th)])
TREU_MEAN = float(ALPHA_TREU.mean())
TREU_SEM = float(ALPHA_TREU.std(ddof=1) / math.sqrt(len(ALPHA_TREU)))
TREU_95HI = 10 ** (1.96 * math.sqrt(0.03 ** 2 + 0.02 ** 2))

P("  SPARC: %d files, %d galaxies, %d points, sha256(concat) = %s (A51 recorded %s)"
  % (len(SPARC_FILES), NG, NPT, H_SPARC, H_SPARC_A51))
P("  SLACS: %d catalogue rows, %d usable lenses, sha256 = %s" % (len(_raw), NL, H_SLACS[:16]))
P("  Treu+2010: %d lenses, <log10 alpha_Salp> = %+.4f +- %.4f (sem), 95%% upper = %.4f"
  % (len(ALPHA_TREU), TREU_MEAN, TREU_SEM, TREU_95HI))
ck("C1", len(SPARC_FILES) == 175 and NG == 171 and NPT == 3375 and H_SPARC == H_SPARC_A51
   and len(_raw) == 85 and NL == 70 and len(ALPHA_TREU) == 56,
   "SPARC %d/%d/%d sha %s ; SLACS %d/%d sha %s ; Treu %d"
   % (len(SPARC_FILES), NG, NPT, H_SPARC, len(_raw), NL, H_SLACS[:16], len(ALPHA_TREU)),
   "175 files, 171 fitted, 3375 points, sha == A51's ; 85 rows, 70 lenses ; 56 Treu lenses",
   "the three channels are the record's own data, byte-identical where A51 recorded a hash")

# =====================================================================================
# C2/C3/C4  SPARC: the likelihood, the fit, the error bar
# =====================================================================================
head("C2  SPARC: THE LIKELIHOOD IS THE RECORD'S (zero-parameter chi2/dof)")

UG = np.geomspace(0.05, 2.5, 240)
FLOOR = 0.10 if MUT == "floor10" else 0.05


def chi2_sparc(a0, gals=None, ug=UG, floor=FLOOR):
    gals = GAL if gals is None else gals
    tot = 0.0
    for g in gals:
        s2 = g["eV"] ** 2 + (floor * g["V"]) ** 2
        Vb2 = (g["Vg"] ** 2)[None, :] + ug[:, None] * (g["Vd"] ** 2 + g["Vb"] ** 2)[None, :]
        gN = Vb2 * 1e6 / g["r"][None, :]
        Vp = np.sqrt(0.5 * gN * (1.0 + np.sqrt(1.0 + 4.0 * a0 / np.maximum(gN, 1e-30)))
                     * g["r"][None, :]) / 1e3
        tot += float(np.sum((g["V"][None, :] - Vp) ** 2 / s2[None, :], axis=1).min())
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
P("  fixed Upsilon = 0.5, a0 = 1.132e-10 : chi2/dof = %.4f   (record 6.87)" % _ch_fix)
P("  fixed Upsilon = 0.5, a0 = 9.36e-11  : chi2/dof = %.4f   (record 6.63)" % _ch_fix936)
P("  one Upsilon per galaxy, 1.132e-10   : chi2/dof = %.4f   (record 2.42)" % _ch_free)
ck("C2", abs(_ch_fix - 6.87) < 0.02 and abs(_ch_fix936 - 6.63) < 0.02 and abs(_ch_free - 2.42) < 0.10,
   "%.4f / %.4f / %.4f" % (_ch_fix, _ch_fix936, _ch_free),
   "6.87 +- 0.02, 6.63 +- 0.02, 2.42 +- 0.10",
   "the zero-parameter chi2/dof reproduces the record to four digits: same likelihood")

head("C3  SPARC ALONE: a0, kappa, and A51's stored values")

r_sp = minimize_scalar(lambda a: chi2_sparc(a), bounds=(5e-11, 2.5e-10),
                       method="bounded", options=dict(xatol=1e-16))
A0_SP = float(r_sp.x)
K_SP = kappa_p3(A0_SP)
CHI2_SP = float(r_sp.fun)
DOF_SP = NPT - NG
A51 = json.load(open(os.path.join(LANE, "A51_kappa_measured", "a51_results.json")))
P("  a0 = %.6e m/s^2   kappa_P3 = %.6f   chi2 = %.2f / %d = %.4f"
  % (A0_SP, K_SP, CHI2_SP, DOF_SP, CHI2_SP / DOF_SP))
P("  A51 stored: a0 = %.6e  kappa = %.6f  chi2/dof = %.4f"
  % (A51["sparc"]["a0_best"], A51["sparc"]["kappa"], A51["sparc"]["chi2_dof"]))
P("  SPARC's own best fit is %.2f%% below the thermal point, %.2f%% below the kappa=1/2 point"
  % (100 * (1 - K_SP / K_TH), 100 * (1 - K_SP / K_HF)))
ck("C3", abs(A0_SP / A51["sparc"]["a0_best"] - 1) < 2e-4 and abs(K_SP / A51["sparc"]["kappa"] - 1) < 2e-4
   and abs(CHI2_SP / DOF_SP - A51["sparc"]["chi2_dof"]) < 1e-3,
   "a0 %.6e vs %.6e ; kappa %.6f vs %.6f ; chi2/dof %.4f vs %.4f"
   % (A0_SP, A51["sparc"]["a0_best"], K_SP, A51["sparc"]["kappa"], CHI2_SP / DOF_SP,
      A51["sparc"]["chi2_dof"]),
   "2e-4 relative on a0 and kappa, 1e-3 on chi2/dof",
   "an independently written likelihood lands on A51's minimum; SPARC peaks well below both theory points")

head("C4  THE SPARC ERROR BAR: formal Delta-chi2=1 vs the 200-draw block bootstrap")

_lo1d = brentq(lambda a: chi2_sparc(a) - CHI2_SP - 1.0, 3e-11, A0_SP * (1 - 1e-9), xtol=1e-20)
_hi1d = brentq(lambda a: chi2_sparc(a) - CHI2_SP - 1.0, A0_SP * (1 + 1e-9), 3e-10, xtol=1e-20)
SIG_DCHI2 = 0.5 * (_hi1d - _lo1d) / A0_SP
rng = np.random.default_rng(20261021)
boot = np.empty(200)
for _k in range(200):
    idx = rng.integers(0, NG, NG)
    gg = [GAL[i] for i in idx]
    boot[_k] = minimize_scalar(lambda a: chi2_sparc(a, gg), bounds=(5e-11, 2.5e-10),
                               method="bounded", options=dict(xatol=1e-16)).x
BOOT_FRAC = float(boot.std(ddof=1) / np.median(boot))
P("  Delta-chi2 = 1 in a0: %.5f%%  (chi2/dof = %.2f, so the formal error is not the truth)"
  % (100 * SIG_DCHI2, CHI2_SP / DOF_SP))
P("  200-draw block bootstrap: median %.6e, sigma/median = %.9f  (A51: %.9f)"
  % (np.median(boot), BOOT_FRAC, A51["sparc"]["sigma_stat_boot"]))
P("  ratio bootstrap/formal = %.2f" % (BOOT_FRAC / SIG_DCHI2))
ck("C4", abs(BOOT_FRAC / A51["sparc"]["sigma_stat_boot"] - 1) < 1e-4 and BOOT_FRAC / SIG_DCHI2 > 5.0,
   "bootstrap %.9f vs A51 %.9f ; ratio to formal %.2f"
   % (BOOT_FRAC, A51["sparc"]["sigma_stat_boot"], BOOT_FRAC / SIG_DCHI2),
   "bootstrap matches A51 to 1e-4 and is >5x the formal error",
   "the 3375 points are not independent; the bootstrap is the declared honest error and it is used below")

SIG_K_SP = BOOT_FRAC * K_SP
if MUT == "no_boot":
    SIG_K_SP = SIG_DCHI2 * K_SP
EST_HALF_SPAN = 0.20838642838788285

# =====================================================================================
# C5  the two fixed points and the kappa identities
# =====================================================================================
head("C5  THE TWO FIXED POINTS: kappa_DE = Z/4pi AND THE CONVENTION MAP")

_kde_alg = math.sqrt(2.0 / (3.0 * math.pi))
_rt = abs(a0_p3(kappa_p3(A0_THERM_DEPLOYED)) / A0_THERM_DEPLOYED - 1.0)
P("  Z = 2 sqrt(8 pi/3) = %.9f ; Z/4pi = %.12f ; sqrt(2/(3 pi)) = %.12f (difference %.1e)"
  % (Z_COEF, KAPPA_DE_ALG, _kde_alg, abs(KAPPA_DE_ALG - _kde_alg)))
P("  a0_therm = %.6e -> kappa_P3 = %.6f, kappa_DE = %.6f" % (A0_THERM_DEPLOYED, K_TH, kappa_de(A0_THERM_DEPLOYED)))
P("  a0_half  = %.6e -> kappa_P3 = %.6f, kappa_DE = %.6f" % (A0_HALF, K_HF, kappa_de(A0_HALF)))
P("  a0_therm/a0_half = %.6f ; separation in kappa_P3 = %.6f (%.2f%% of a0_half)"
  % (A0_THERM_DEPLOYED / A0_HALF, K_HF - K_TH, 100 * (K_HF - K_TH) / K_HF))
P("  round trip a0 -> kappa -> a0 residual %.2e ; kappa_DE/kappa_P3 = 1/sqrt(Omega_L) = %.6f"
  % (_rt, 1 / math.sqrt(OMEGA_L)))
P("  kappa_DE(a0_half) = %.9f (1/2 exactly iff Omega_L = 32pi/147 = %.9f)"
  % (kappa_de(A0_HALF), 32 * math.pi / 147))
P("  the OTHER '1/2': kappa_P3 = 0.5 is a0 = %.4e, %.2f%% above the thermal point"
  % (A0_P3_HALF, 100 * (A0_P3_HALF / A0_THERM_DEPLOYED - 1)))
ck("C5", abs(KAPPA_DE_ALG - _kde_alg) < 1e-12 and abs(kappa_de(A0_HALF) - 0.5) < 2e-3
   and _rt < 1e-12 and 0.37 < K_TH < 0.39 and 0.405 < K_HF < 0.42,
   "Z/4pi %.12f ; kappa_DE(a0_half) %.9f ; kappa_P3 %.6f/%.6f ; round trip %.1e"
   % (KAPPA_DE_ALG, kappa_de(A0_HALF), K_TH, K_HF, _rt),
   "identity to 1e-12 ; kappa_DE(a0_half) = 1/2 to 2e-3 ; round trip < 1e-12",
   "the thermal point is kappa_P3 = 0.381 / kappa_DE = 0.4607; kappa = 1/2 is a different a0, 8.5% higher")

# =====================================================================================
# the SLACS model (A70's, as in A71)
# =====================================================================================
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


def M2D_star(R, Re, n=4.0):
    b = B4 if n == 4.0 else 2.0 * n - 1.0 / 3.0 + 4.0 / (405.0 * n) + 46.0 / (25515.0 * n * n)
    return gammainc(2.0 * n, b * (np.asarray(R) / Re) ** (1.0 / n))


def M3D_star(r, Re, n=4.0):
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
    """Einstein radius (kpc): the law + a Sersic n=4 stellar profile + one shared IMF boost."""
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


_DB = 0.10
_t0 = time.time()
RESP_I = np.array([math.log(predict(d, 1.132e-10, boost=1.0 + _DB) / predict(d, 1.132e-10))
                   for d in LENS]) / math.log(1.0 + _DB)
RESP = float(np.median(RESP_I))
RESP_MEAN = float(RESP_I.mean())
RESP_SCAT = float(RESP_I.std(ddof=1))
P("")
P("  per-lens response dlnR_E/dlnB: median %.5f, mean %.5f, scatter %.5f  (%.1f s)"
  % (RESP, RESP_MEAN, RESP_SCAT, time.time() - _t0))
S_LN = math.sqrt(0.045 ** 2 + 0.09 ** 2) * LN10      # A70/A71's per-lens sigma, 0.1006 dex
SIG_B_MEAS_DEX = 0.0143
SIG_B_PRIOR_DEX = 0.100 if MUT == "imf_prior" else 0.036
SIG_B_MEAS = SIG_B_MEAS_DEX * LN10
SIG_B_PRIOR = SIG_B_PRIOR_DEX * LN10
SIG_B_PULL_DEX = math.sqrt(SIG_B_PRIOR_DEX ** 2 + SIG_B_MEAS_DEX ** 2)

# =====================================================================================
# C6/C7  the SLACS model is A70's, and the two responses
# =====================================================================================
head("C6  SLACS: THE A70 MODEL REPRODUCES A55's 70 PER-LENS RATIOS AND B_req")

SHIFT_N4 = 0.0
if MUT == "sersic_default":
    # mutation: the SLACS baseline is Sersic n = 6 (A80's slope-zeroing index), not n = 4
    SHIFT_N4 = RESP * math.log(1.22798616285 / 1.09854135156)

RATIOS_A70 = np.array([predict(d, 1.132e-10) / d["RE"] for d in LENS])
MED50 = float(np.median(RATIOS_A70))
MEANLN50 = float(np.log(RATIOS_A70).mean())
SD50 = float(np.log(RATIOS_A70).std(ddof=1))
A55 = json.load(open(A55JSON))
_r55 = {x["name"]: x["ratio"] for x in A55["slacs"]["per_lens_salpeter"]}
_dev = float(np.max(np.abs(np.array([RATIOS_A70[i] / _r55[d["name"]] - 1.0
                                     for i, d in enumerate(LENS)]))))
P("  median R_E,pred/R_E,obs = %.6f (A55 0.885232) ; <ln> = %+.6f (A55 -0.124539) ; sd = %.6f ln"
  % (MED50, MEANLN50, SD50))
P("  max per-lens deviation from A55's stored ratios: %.2e" % _dev)


def med_at_B(B, a0=1.132e-10):
    return float(np.median([predict(d, a0, boost=B) / d["RE"] for d in LENS]))


B_REQ_HALF = brentq(lambda B: med_at_B(B) - 1.0, 1.02, 5.0, xtol=1e-6)
P("  root-found B (median ratio = 1) at kappa = 1/2 : %.4f   (A70/A71: 1.1738)" % B_REQ_HALF)
P("  1/median = %.4f ; 1/median^2 = %.4f (A55's erroneous 1.283) ; B_req/(1/median) = %.4f"
  % (1 / MED50, 1 / MED50 ** 2, B_REQ_HALF / (1 / MED50)))
ck("C6", abs(MED50 / 0.8852 - 1) < 1e-4 and _dev < 1e-9 and abs(B_REQ_HALF - 1.1738) < 2e-3,
   "median %.6f, max dev %.1e, B_req(1/2) %.4f" % (MED50, _dev, B_REQ_HALF),
   "median 0.8852 +- 1e-4 ; per-lens < 1e-9 ; B_req 1.1738 +- 2e-3",
   "the lensing model here IS A55's/A70's, not a re-implementation, and the required boost is 1.174")

head("C7  THE TWO RESPONSES: B AND kappa")

_kk = (0.35, 0.5, 0.7)
_med_k = [float(np.median([predict(d, a0_p3(k)) / d["RE"] for d in LENS])) for k in _kk]
_h = 1e-3
_dlnR_dlnk = (math.log(float(np.median([predict(d, a0_p3(0.5 * math.exp(_h))) / d["RE"] for d in LENS])))
              - math.log(float(np.median([predict(d, a0_p3(0.5 * math.exp(-_h))) / d["RE"] for d in LENS])))) / (2 * _h)
B_FROM_RESP = math.exp(-MEANLN50 / RESP)
P("  median ratio at kappa = 0.35/0.50/0.70 : %.4f / %.4f / %.4f" % tuple(_med_k))
P("  dlnR/dlnB = %.4f (per-lens median; scatter %.4f) ; response-route B(1/2) = %.4f vs root %.4f"
  % (RESP, RESP_SCAT, B_FROM_RESP, B_REQ_HALF))
P("  dlnR/dlnkappa = %.4f ; ratio dlnR/dlnB : dlnR/dlnkappa = %.2f : 1"
  % (_dlnR_dlnk, RESP / abs(_dlnR_dlnk)))
ck("C7", abs(RESP - 0.7775) < 6e-3 and abs(B_FROM_RESP / B_REQ_HALF - 1) < 3e-3
   and abs(_dlnR_dlnk - 0.1205) < 6e-3 and 5.8 < RESP / abs(_dlnR_dlnk) < 7.2,
   "dlnR/dlnB %.4f ; B_resp %.4f vs B_root %.4f ; dlnR/dlnkappa %.4f ; ratio %.2f"
   % (RESP, B_FROM_RESP, B_REQ_HALF, _dlnR_dlnk, RESP / abs(_dlnR_dlnk)),
   "0.7775 +- 0.006 ; B_resp == B_root to 3e-3 ; 0.1205 +- 0.006 ; ratio in [5.8, 7.2]",
   "lensing is 6.5x more sensitive to the IMF than to a0: it is a mass-normalisation measurement")

# =====================================================================================
# the SLACS 70-lens quadratic in ln B, at every kappa
# =====================================================================================
# chi2_SLACS(kappa,B) = sum_i (ln r_i + r_i lnB + SHIFT_N4)^2 / S_LN^2
#                     = A(kappa) + 2 Bc(kappa) lnB + C lnB^2
_KGF = np.array([0.16, 0.18, 0.20, 0.225, 0.25, 0.28, 0.30, 0.33, 0.36,
                 0.44, 0.47, 0.50, 0.55, 0.60, 0.66, 0.72, 0.80,
                 0.90, 1.00, 1.20, 1.45, 1.70, 2.00])
KG = np.sort(np.concatenate([_KGF, [K_TH, K_HF]]))
LNR_TAB = np.zeros((len(KG), NL))
for _i, _k in enumerate(KG):
    LNR_TAB[_i, :] = np.log(np.array([predict(d, a0_p3(_k)) / d["RE"] for d in LENS])) + SHIFT_N4
_A = np.array([float(np.sum(LNR_TAB[i] ** 2)) / S_LN ** 2 for i in range(len(KG))])
_Bc = np.array([float(np.sum(RESP_I * LNR_TAB[i])) / S_LN ** 2 for i in range(len(KG))])
C_TOT = float(np.sum(RESP_I ** 2)) / S_LN ** 2
SPL_A = CubicSpline(np.log(KG), _A)
SPL_B = CubicSpline(np.log(KG), _Bc)

_i_th = int(np.argmin(np.abs(KG - K_TH)))
M_TH = float(LNR_TAB[_i_th].mean())
SD_TH = float(LNR_TAB[_i_th].std(ddof=1))
B_ML_TH = math.exp(-_Bc[_i_th] / C_TOT)
B_REQ_TH = math.exp(-M_TH / RESP)
P("  SLACS at the thermal point: <ln r> = %+.6f, sd = %.6f ln ; B_ML = %.5f (70-term profile), B_req = %.5f"
  % (M_TH, SD_TH, B_ML_TH, B_REQ_TH))

KG8 = np.array([0.20, 0.30, 0.40, 0.4607, 0.50, 0.60, 0.70, 0.80])
CHI2_B1, CHI2_BPROF = [], []
for _k in KG8:
    _lnr = np.array([math.log(predict(d, a0_p3(_k)) / d["RE"]) for d in LENS])
    _Breq = math.exp(-_lnr.mean() / RESP)
    if MUT == "sd_at_b1":
        _lnrB = _lnr                      # mutation: the "profiled" column is computed at B = 1
    else:
        _lnrB = np.array([math.log(predict(d, a0_p3(_k), boost=_Breq) / d["RE"]) for d in LENS])
    CHI2_B1.append(NL * _lnr.std(ddof=1) ** 2 / S_LN ** 2)
    CHI2_BPROF.append(NL * _lnrB.std(ddof=1) ** 2 / S_LN ** 2)
CHI2_B1 = np.array(CHI2_B1)
CHI2_BPROF = np.array(CHI2_BPROF)
D_B1 = float(CHI2_B1[0] - CHI2_B1[-1])
D_BPROF = float(np.max(CHI2_BPROF) - np.min(CHI2_BPROF))

head("C8  A80's 6.35 IS AN UNPROFILED-B ARTEFACT -- RECOMPUTED HERE, BOTH WAYS")
P("  the A80/A71 scatter statistic N sd(ln r)^2/s^2, s = %.4f ln (0.1006 dex):" % S_LN)
P("    kappa      0.20     0.30     0.40    0.4607   0.50     0.60     0.70     0.80")
P("    B = 1    " + "".join("%9.2f" % x for x in CHI2_B1))
P("    B profiled" + "".join("%9.2f" % x for x in CHI2_BPROF))
P("  Delta over kappa in [0.20,0.80]: B = 1 -> %.4f ; B profiled -> %.4f  (ratio %.1f)"
  % (D_B1, D_BPROF, D_B1 / max(D_BPROF, 1e-12)))
P("  the profiled column re-solves the Einstein radius at boost = B_req(kappa), so the per-lens")
P("  response scatter (%.1f%%) is what moves the SD; a constant boost shift cannot." % (100 * RESP_SCAT))
ck("C8", D_B1 > 4.0 and D_BPROF < 0.5 and D_B1 / D_BPROF > 8.0,
   "Delta(B=1) = %.4f ; Delta(B profiled) = %.4f" % (D_B1, D_BPROF),
   "Delta(B=1) > 4 ; Delta(profiled) < 0.5 ; ratio > 8",
   "A71's 6.35 is real at B = 1 but 20x smaller at the B the lane says it profiled -- A80 confirmed")

# =====================================================================================
# C9  the cluster channel
# =====================================================================================
head("C9  CLUSTERS: A18's ANCHOR AND THE CLUSTER-ONLY kappa")


def F_ph(y):
    return 0.5 * (math.sqrt(1.0 + 4.0 / y) - 1.0)


CL_MB, CL_A = 1.4e14 * MSUN, 250.0 * KPC


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


R_CAN, RV_CAN, F_CAN = R_tot(9.36e-11)
_hh = 1e-3
DLNR = (math.log(R_tot(9.36e-11 * (1 + _hh))[0]) - math.log(R_tot(9.36e-11 * (1 - _hh))[0])) / (2 * _hh)
R_REQ, SIG_R = 5.552, 0.427
U0, SIG_U = 0.45, 0.03
SIG_CL = (math.sqrt((SIG_R / R_REQ) ** 2 + (SIG_U / U0) ** 2)) / abs(DLNR)
K_CL = kappa_p3(9.36e-11) * (U0 * R_REQ / R_CAN) ** (1.0 / DLNR)


def chi2_cluster(k, u):
    Rt = R_tot(a0_p3(k))[0]
    return ((Rt / u - R_REQ) / SIG_R) ** 2 + ((u - U0) / SIG_U) ** 2


def u_best(k):
    return minimize_scalar(lambda u: chi2_cluster(k, u), bounds=(0.30, 0.70), method="bounded",
                           options=dict(xatol=1e-10)).x


P("  r_v = %.4f Mpc ; F(y_v) = %.4f ; R_tot = %.4f   (A18: 1.6863 / 3.7702 / 2.6179)"
  % (RV_CAN / MPC, F_CAN, R_CAN))
P("  dlnR_tot/dlna0 = %+.4f ; cluster-only kappa = %.4f +- %.4f (%.1f%%)   (A51: 0.3934 +- 0.0432)"
  % (DLNR, K_CL, K_CL * SIG_CL, 100 * SIG_CL))
P("  the channel's inputs: R_req = %.3f +- %.3f (A18), u = %.2f +- %.2f (A18, circular)"
  % (R_REQ, SIG_R, U0, SIG_U))
ck("C9", abs(RV_CAN / MPC - 1.6863) < 1e-3 and abs(F_CAN - 3.7702) < 1e-3 and abs(R_CAN - 2.6179) < 1e-3
   and abs(K_CL - 0.3934) < 2e-3 and abs(SIG_CL - 0.1097) < 3e-3,
   "%.4f Mpc / %.4f / %.4f ; kappa %.4f +- %.4f" % (RV_CAN / MPC, F_CAN, R_CAN, K_CL, K_CL * SIG_CL),
   "1.6863/3.7702/2.6179 +- 1e-3 ; 0.3934 +- 0.002, 10.97% +- 0.3%",
   "A18's anchor is reproduced before it is used; u and R_req come from the same amplitudes (circular, stated)")

# =====================================================================================
# C10  the sigma_ap channel, imported from A85 and audited here
# =====================================================================================
head("C10  THE A85 sigma_ap CHANNEL: FISHER AUDIT AND THE 3.08 deg DEGENERACY")

A85 = json.load(open(os.path.join(LANE, "A85_slacs_jeans_joint", "a85_results.json")))
A80 = json.load(open(os.path.join(LANE, "A80_slacs_sersic", "a80_results.json")))
_F = np.array([[10235.6, 949.3], [949.3, 102.0]])
DET_F = float(np.linalg.det(_F))
COND_F = float(np.linalg.cond(_F))
SK_JOINT_F = float(math.sqrt(np.linalg.inv(_F)[1, 1]))
SK_RE = float(A85["fisher"]["sk_re"])
SINF = float(A85["sinf"])
# A85's own derivative pairs: lensing (dlnR/dlnB, dlnR/dlnkappa) and sigma (dlnsig/dlnB, dlnsig/dlnkappa)
JB85, JK85 = 0.7865, 0.1003          # A85 section 2 (its own exact-deprojection solver, per-lens medians)
JBS, JKS = 0.470585, 0.034456        # A85 section 2 (median lens)
ANGLE = abs(math.degrees(math.atan2(JK85, JB85)) - math.degrees(math.atan2(JKS, JBS)))
# the same angle with A70/A71's lensing response, for the model-dependence
ANGLE_A70 = abs(math.degrees(math.atan2(0.1205, 0.7775)) - math.degrees(math.atan2(JKS, JBS)))
P("  A85's 2x2 Fisher (70 lenses, R_E + sigma_ap): F = [[%.1f, %.1f], [%.1f, %.1f]]" % tuple(_F.flatten()))
P("  det = %.4e (A85 %.4e) ; condition number = %.2f (A85 %.2f)"
  % (DET_F, A85["fisher"]["det"], COND_F, A85["fisher"]["cond"]))
P("  sigma(kappa) from F alone = sqrt(inv(F)_kk) = %.5f (A85 %.5f) ; R_E alone %.5f ; improvement %.3f"
  % (SK_JOINT_F, A85["fisher"]["sk_joint"], SK_RE, SK_RE / SK_JOINT_F))
P("  angle between the constraints, with A85's own derivatives (%.4f, %.4f) vs (%.6f, %.6f): %.4f deg (A85 %.4f)"
  % (JB85, JK85, JBS, JKS, ANGLE, A85["fisher"]["angle"]))
P("  the same angle with A70/A71's lensing response (0.7775, 0.1205): %.4f deg -- both say 'nearly parallel'" % ANGLE_A70)
P("  A85's error inflation sqrt(chi2/dof) = %.4f ; B = %.5f +- %.5f (formal) +- %.5f (scaled)"
  % (SINF, A85["route2"]["thermal"]["beta0"]["B"], A85["route2"]["thermal"]["beta0"]["sB_hi"],
     A85["route2"]["thermal"]["beta0"]["sB_hi"] * SINF))
ck("C10", abs(DET_F / A85["fisher"]["det"] - 1) < 1e-3 and abs(COND_F / A85["fisher"]["cond"] - 1) < 1e-2
   and abs(SK_JOINT_F / A85["fisher"]["sk_joint"] - 1) < 1e-3 and abs(ANGLE - A85["fisher"]["angle"]) < 0.05
   and abs(SK_RE / SK_JOINT_F - A85["fisher"]["improvement"]) < 0.02,
   "det %.4e ; cond %.2f ; sigma(kappa) %.5f ; angle %.4f deg ; improvement %.3f"
   % (DET_F, COND_F, SK_JOINT_F, ANGLE, SK_RE / SK_JOINT_F),
   "1e-3 on det, 1e-2 on cond, 1e-3 on sigma, 0.05 deg on the angle, 0.02 on the improvement (F's entries are published to 1 decimal)",
   "A85's Fisher is internally consistent: the two constraints are 3.08 deg apart and sigma(kappa) improves only 2.35x")

_k85 = np.array([x["kappa"] for x in A85["kappa_sweep"]])
_a85 = np.array([x["a0"] for x in A85["kappa_sweep"]])
_bsig = np.array([x["B_sig"] for x in A85["kappa_sweep"]])
_kp85 = np.array([kappa_p3(a) for a in _a85])
_ord = np.argsort(_kp85)
SPL_BSIG = CubicSpline(np.log(_kp85[_ord]), np.log(_bsig[_ord]))


def _bsig_of(k):
    return math.exp(float(SPL_BSIG(math.log(k))))


_hh = 1e-3
_bs = _bsig_of(K_TH)
BSLOPE = math.log(_bsig_of(K_TH * (1 + _hh)) / _bsig_of(K_TH * (1 - _hh))) / (math.log(1 + _hh) - math.log(1 - _hh))
SIGMA_K_SIG = 0.7318                 # A85's sigma_ap-alone marginalised sigma(kappa), its section 2
S_COND = SIGMA_K_SIG * abs(BSLOPE)
P("  B_sigma(kappa) at the thermal point = %.5f (A85's table at kappa = 0.4607: %.5f)"
  % (_bs, A85["kappa_sweep"][4]["B_sig"]))
P("  dlnB_sigma/dlnkappa = %+.5f -> conditional sigma(lnB|kappa) = %.5f (formal), %.5f (A85-inflated)"
  % (BSLOPE, S_COND, S_COND * SINF))
P("  the anchor: A85's sigma_ap-alone sigma(kappa) = %.4f ; this line's slope gives back %.5f"
  % (SIGMA_K_SIG, S_COND / abs(BSLOPE)))
ck("C10b", abs(_bs / A85["kappa_sweep"][4]["B_sig"] - 1) < 5e-3 and abs(S_COND / abs(BSLOPE) / SIGMA_K_SIG - 1) < 0.02
   and S_COND > 0 and abs(BSLOPE) < 0.2,
   "B_sigma(thermal) %.5f ; s_cond %.5f -> sigma(kappa)_sigma %.5f"
   % (_bs, S_COND, S_COND / abs(BSLOPE)),
   "B_sigma to 5e-3 of A85's table ; sigma(kappa)_sigma 0.7318 +- 2% ; |slope| < 0.2",
   "the imported sigma_ap channel reproduces A85's own marginalised kappa error by construction")

# =====================================================================================
# C11  the A80 / A85 agreement on B(n = 4)
# =====================================================================================
head("C11  A80 vs A85 vs THIS LANE ON B(n=4): THREE SOLVERS, THE SAME NUMBER")

B80_N4 = float(A80["models"]["thermal"]["a_renorm"]["B"])
B80_N6 = float(A80["n_profile"][4]["B"])
N_ZERO = float(A80["n_zero"])
B85 = float(A85["route2"]["thermal"]["beta0"]["B"])
B85_S = float(A85["route2"]["thermal"]["beta0"]["sB_hi"])
B85_RE = float(A85["kappa_sweep"][4]["B_RE"])      # A85's R_E-only fit at kappa = 0.4607
SIG_B_CMP = SIG_B_PULL_DEX * LN10                  # the 0.0387 dex IMF/measurement quadrature, in ln B
P("  A80 (A70 kernel, profiled scatter, thermal a0 = %.4e): B(n=4) = %.5f, B(n=6.0) = %.5f"
  % (A80["models"]["thermal"]["a_renorm"]["a0"], B80_N4, B80_N6))
P("  A80: the shape residual vanishes at n = %.4f ; B there = %.5f (shift %+.4f dex)"
  % (N_ZERO, B80_N6, math.log10(B80_N6 / B80_N4)))
P("  A85 (exact deprojection + Jeans, thermal a0): B(R_E + sigma_ap) = %.5f +- %.5f (formal) ; B(R_E only) = %.5f"
  % (B85, B85_S, B85_RE))
P("  A81 (this lane, 70-term profile, R_E): B_ML = %.5f, B_req = %.5f" % (B_ML_TH, B_REQ_TH))
P("  like-for-like (R_E only): A81 vs A85 = %+.5f (%+.2f%%, %.2f sigma of the 0.0387 dex quadrature)"
  % (B_ML_TH - B85_RE, 100 * (B_ML_TH / B85_RE - 1), (B_ML_TH - B85_RE) / SIG_B_CMP))
P("  the task's comparison: A80 B(n=4) vs A85's headline B = %+.5f (%+.2f%%, %.2f sigma)"
  % (B80_N4 - B85, 100 * (B80_N4 / B85 - 1), (B80_N4 - B85) / SIG_B_CMP))
P("  A85 vs Treu = %.2f sigma (its own 2.27, reproduced)" % (math.log10(B85) / SIG_B_PULL_DEX))
P("  the n-band in IMF units: at n = 4 the pull is %.2f sigma, at n = 6.0 it would be %.2f sigma (A80: 1.05)"
  % (math.log10(B80_N4) / SIG_B_PULL_DEX, math.log10(B80_N6) / SIG_B_PULL_DEX))
ck("C11", abs(B80_N4 / B85 - 1) < 0.01 and abs((B80_N4 - B85) / SIG_B_CMP) < 1.0
   and abs(B_ML_TH / B85_RE - 1) < 0.01 and abs(B80_N6 - 1.0985) < 1e-3,
   "A80 %.5f vs A85 %.5f (%+.2f%%, %.2f sigma) ; A81 vs A85(R_E) %+.2f%% ; B(n=6) %.5f"
   % (B80_N4, B85, 100 * (B80_N4 / B85 - 1), (B80_N4 - B85) / SIG_B_CMP,
      100 * (B_ML_TH / B85_RE - 1), B80_N6),
   "A80/A85 within 1% and 1 sigma ; A81/A85(R_E) within 1% ; B(n=6) 1.0985 +- 1e-3",
   "three independent lensing solvers agree on the shared IMF normalisation to ~1%: B is not solver-dependent")

# =====================================================================================
# the joint likelihood
# =====================================================================================
S_COND_USE = S_COND


def slacs_at(k, prior=True, sigma=False, B_fixed=None):
    """The 70-term SLACS chi2 at kappa with lnB profiled (or fixed), + optional prior and sigma_ap."""
    lnk = math.log(k)
    A = float(SPL_A(lnk))
    Bc = float(SPL_B(lnk))
    C = C_TOT
    if MUT == "drop_sigma_ap":
        sigma = False                   # mutation: the sigma_ap channel is dropped from the likelihood
    lbs = math.log(_bsig_of(k)) if sigma else 0.0
    Csum = C + ((1.0 / SIG_B_PRIOR ** 2) if prior else 0.0) + ((1.0 / S_COND_USE ** 2) if sigma else 0.0)
    Lsum = Bc - ((lbs / S_COND_USE ** 2) if sigma else 0.0)
    if B_fixed is not None:
        lb = math.log(B_fixed)
    elif MUT == "unprofile_B" and prior and not sigma:
        lb = -Bc / C                       # the lensing value: the prior is NOT marginalised
    else:
        lb = -Lsum / Csum
    val = A + 2.0 * Bc * lb + C * lb * lb
    if prior:
        val += lb * lb / SIG_B_PRIOR ** 2
    if sigma:
        val += (lb - lbs) ** 2 / S_COND_USE ** 2
    return val, lb


def chi2_joint(k, use_slacs=True, use_sigma=False, use_cluster=True, use_prior=True,
               B_fixed=None, sparc_sigma=None):
    s = SIG_K_SP if sparc_sigma is None else sparc_sigma
    c = ((k - K_SP) / s) ** 2
    lnB = 0.0
    if use_slacs:
        v, lnB = slacs_at(k, prior=use_prior, sigma=use_sigma, B_fixed=B_fixed)
        c += v
    if use_cluster:
        c += chi2_cluster(k, u_best(k))
    return c, lnB


def profile_fit(use_slacs=True, use_sigma=False, use_cluster=True, use_prior=True, lo=0.16, hi=1.20):
    r = minimize_scalar(lambda lk: chi2_joint(math.exp(lk), use_slacs=use_slacs, use_sigma=use_sigma,
                                              use_cluster=use_cluster, use_prior=use_prior)[0],
                        bounds=(math.log(lo), math.log(hi)), method="bounded", options=dict(xatol=1e-13))
    k = float(math.exp(r.x))
    c = float(r.fun)
    _, lb = chi2_joint(k, use_slacs=use_slacs, use_sigma=use_sigma, use_cluster=use_cluster, use_prior=use_prior)
    try:
        klo = brentq(lambda x: chi2_joint(x, use_slacs=use_slacs, use_sigma=use_sigma, use_cluster=use_cluster,
                                          use_prior=use_prior)[0] - c - 1.0, lo, k, xtol=1e-12)
        khi = brentq(lambda x: chi2_joint(x, use_slacs=use_slacs, use_sigma=use_sigma, use_cluster=use_cluster,
                                          use_prior=use_prior)[0] - c - 1.0, k, hi, xtol=1e-12)
        sig = 0.5 * (khi - klo)
    except ValueError:
        klo = khi = sig = float("nan")
    return dict(kappa=k, chi2=c, lnB=lb, B=math.exp(lb), u=u_best(k), sigma_kappa=sig,
                klo=klo, khi=khi)


head("C12  THE JOINT FIT: (kappa, B, u) WITH B AND u PROFILED AT EVERY GRID POINT")

FIT = profile_fit()
K_JOINT = FIT["kappa"]
CHI2_JOINT = FIT["chi2"]
B_JOINT = FIT["B"]
LNB_JOINT = FIT["lnB"]
U_JOINT = FIT["u"]
SIG_K_JOINT = FIT["sigma_kappa"]
A0_JOINT = a0_p3(K_JOINT)
_AJ = float(SPL_A(math.log(K_JOINT)))
_BJ = float(SPL_B(math.log(K_JOINT)))
CHI2_SP_JOINT = ((K_JOINT - K_SP) / SIG_K_SP) ** 2
CHI2_SL_DATA = _AJ + 2 * _BJ * LNB_JOINT + C_TOT * LNB_JOINT ** 2
CHI2_PR = LNB_JOINT ** 2 / SIG_B_PRIOR ** 2
CHI2_CL_JOINT = chi2_cluster(K_JOINT, U_JOINT)
CHI2_TOT = CHI2_SP_JOINT + CHI2_SL_DATA + CHI2_CL_JOINT + CHI2_PR
B_REQ_JOINT = math.exp(-_BJ / C_TOT)
P("  kappa_P3 = %.6f +- %.6f (stat, Delta-chi2=1) ; a0 = %.6e m/s^2" % (K_JOINT, SIG_K_JOINT, A0_JOINT))
P("  a0 is %.2f%% below the thermal point and %.2f%% below the kappa=1/2 point"
  % (100 * (1 - K_JOINT / K_TH), 100 * (1 - K_JOINT / K_HF)))
P("  in the rho_DE convention: kappa_DE(joint) = %.6f ; kappa_DE(thermal) = %.6f ; distance %.2f sigma"
  % (kappa_de(A0_JOINT), KAPPA_DE_ALG, (K_TH - K_JOINT) / SIG_K_JOINT))
P("  B = %.6f (log10 B = %+.5f dex), B_req(kappa) = %.6f, prior mean 1.0 ; u = %.6f"
  % (B_JOINT, math.log10(B_JOINT), B_REQ_JOINT, U_JOINT))
P("  chi2 = %.5f = SPARC %.4f + SLACS %.4f + clusters %.4f + IMF prior %.4f"
  % (CHI2_TOT, CHI2_SP_JOINT, CHI2_SL_DATA, CHI2_CL_JOINT, CHI2_PR))
P("  Delta-chi2=1 range in kappa: [%.5f, %.5f]" % (FIT["klo"], FIT["khi"]))
SIG_LNB_COND = 1.0 / math.sqrt(C_TOT + 1.0 / SIG_B_PRIOR ** 2)
SIG_B_COND = B_JOINT * SIG_LNB_COND
_du = 1e-4
_c_u = (chi2_cluster(K_JOINT, U_JOINT + _du) - 2 * chi2_cluster(K_JOINT, U_JOINT)
        + chi2_cluster(K_JOINT, U_JOINT - _du)) / _du ** 2
SIG_U_COND = math.sqrt(2.0 / _c_u)
P("  conditional errors at the joint: sigma(lnB) = %.5f -> sigma(B) = %.5f (%.1f%%) ; sigma(u) = %.5f"
  % (SIG_LNB_COND, SIG_B_COND, 100 * SIG_LNB_COND, SIG_U_COND))
P("  the IMF prior: B = 1.00 +- 0.036 dex (Treu+2010, 56 lenses, mean %+.4f +- %.4f sem)"
  % (TREU_MEAN, TREU_SEM))
P("  the two B estimators at the thermal point: profile B_ML = %.5f vs mean-zero B_req = %.5f (%.2f%%)"
  % (B_ML_TH, B_REQ_TH, 100 * (B_ML_TH / B_REQ_TH - 1)))
P("  Sersic n is NOT a parameter of this likelihood: no per-lens n exists on disk (A80 K2).")
P("  A80's n-curve instead: n_zero = %.4f (slope zero), n_ML = %.4f, B(n=4) = %.5f, B(n=6.0) = %.5f"
  % (N_ZERO, float(A80["models"]["thermal"]["b_renorm"]["n"]), B80_N4, B80_N6))

def _obj3(p):
    # the SAME surface, with A(kappa) and Bc(kappa) re-evaluated at every kappa (no frozen coefficients)
    _k = math.exp(p[0])
    _a = float(SPL_A(p[0]))
    _b = float(SPL_B(p[0]))
    return (((_k - K_SP) / SIG_K_SP) ** 2
            + (_a + 2.0 * _b * p[1] + C_TOT * p[1] ** 2)
            + p[1] ** 2 / SIG_B_PRIOR ** 2
            + chi2_cluster(_k, p[2]))


_r2 = minimize(_obj3, [math.log(K_JOINT) + 0.01, LNB_JOINT + 0.01, 0.5], method="Nelder-Mead",
               options=dict(xatol=1e-13, fatol=1e-13, maxiter=40000))
K_NM, B_NM, U_NM = math.exp(_r2.x[0]), math.exp(_r2.x[1]), float(_r2.x[2])
_kt = 0.31
_direct = np.array([math.log(predict(d, a0_p3(_kt)) / d["RE"]) for d in LENS]) + SHIFT_N4
_dA = float(np.sum(_direct ** 2)) / S_LN ** 2
_dBc = float(np.sum(RESP_I * _direct)) / S_LN ** 2
_lnB_d = -_dBc / (C_TOT + 1.0 / SIG_B_PRIOR ** 2)
_ch_direct = _dA + 2 * _dBc * _lnB_d + C_TOT * _lnB_d ** 2 + _lnB_d ** 2 / SIG_B_PRIOR ** 2
_ch_spline = slacs_at(_kt, prior=True)[0]
P("  independent Nelder-Mead on (ln kappa, ln B, u): kappa %.6f, B %.6f, u %.6f, chi2 %.5f"
  % (K_NM, B_NM, U_NM, _r2.fun))
P("  spline compression at kappa = %.2f: direct 70-lens %.5f vs spline %.5f (diff %.1e)"
  % (_kt, _ch_direct, _ch_spline, abs(_ch_direct - _ch_spline)))
P("  B is between the prior mean and B_req: %.5f < %.5f < %.5f"
  % (min(1.0, B_REQ_JOINT), B_JOINT, max(1.0, B_REQ_JOINT)))
ck("C12", abs(K_NM / K_JOINT - 1) < 1e-4 and abs(B_NM / B_JOINT - 1) < 1e-4 and abs(_r2.fun - CHI2_TOT) < 1e-3
   and abs(_ch_direct - _ch_spline) < 1e-3 and min(1.0, B_REQ_JOINT) < B_JOINT < max(1.0, B_REQ_JOINT)
   and abs(B_JOINT - B_REQ_JOINT) > 0.01 and 0.3 < K_JOINT < 0.45,
   "profile %.6f/%.5f/%.5f vs NM %.6f/%.5f/%.5f ; B %.4f in (1, %.4f) ; chi2 diff %.1e"
   % (K_JOINT, B_JOINT, U_JOINT, K_NM, B_NM, U_NM, B_JOINT, B_REQ_JOINT, abs(_ch_direct - _ch_spline)),
   "two minimisers agree to 1e-4 ; spline == direct to 1e-3 ; 1 < B < B_req and |B - B_req| > 0.01",
   "the joint optimum is not a minimiser artefact, and B is the prior-weighted compromise, not B_req")

# =====================================================================================
# C13  per-channel chi2/dof and the pulls
# =====================================================================================
head("C13  PER-CHANNEL chi2/dof AT THE JOINT POINT, AND THE PULLS")

CHI2_SP_RAW = float(chi2_sparc(A0_JOINT))
CHI2_SL_RAW = _AJ + 2 * _BJ * LNB_JOINT + C_TOT * LNB_JOINT ** 2
CHI2_CL_RAW = CHI2_CL_JOINT - (U_JOINT - U0) ** 2 / SIG_U ** 2
P("  SPARC   raw chi2 %.2f / %d dof = %.4f   (compressed %.4f / 1 dof)"
  % (CHI2_SP_RAW, DOF_SP, CHI2_SP_RAW / DOF_SP, CHI2_SP_JOINT))
P("  SLACS   raw chi2 %.2f / %d dof = %.4f   (compressed %.4f / 1 dof)"
  % (CHI2_SL_RAW, NL - 2, CHI2_SL_RAW / (NL - 2), CHI2_SL_DATA))
P("  cluster raw chi2 %.4f / 1 dof              (compressed %.4f, u profiled)" % (CHI2_CL_RAW, CHI2_CL_JOINT))
P("  IMF prior (lnB)^2/sigma_p^2 = %.4f / 1 dof" % CHI2_PR)

r_cl = minimize_scalar(lambda lk: chi2_cluster(math.exp(lk), u_best(math.exp(lk))),
                       bounds=(math.log(0.16), math.log(0.9)), method="bounded")
K_CL_ONLY = float(math.exp(r_cl.x))
SIG_CL_ONLY = 0.5 * (brentq(lambda k: chi2_cluster(k, u_best(k)) - r_cl.fun - 1.0, K_CL_ONLY, 0.9) -
                     brentq(lambda k: chi2_cluster(k, u_best(k)) - r_cl.fun - 1.0, 0.16, K_CL_ONLY))
_G = np.linspace(0.16, 2.0, 500)
_CH_SL_ONLY = np.array([slacs_at(k, prior=True)[0] for k in _G])
_i = int(np.argmin(_CH_SL_ONLY))
K_SL_ONLY = float(_G[_i])
_chi_sl_min = float(_CH_SL_ONLY[_i])
try:
    _lo_sl = brentq(lambda k: slacs_at(k, prior=True)[0] - _chi_sl_min - 1.0, 0.16, K_SL_ONLY, xtol=1e-10)
    _hi_sl = brentq(lambda k: slacs_at(k, prior=True)[0] - _chi_sl_min - 1.0, K_SL_ONLY, 2.0, xtol=1e-10)
    SIG_SL_ONLY = 0.5 * (_hi_sl - _lo_sl)
except ValueError:
    _lo_sl = _hi_sl = SIG_SL_ONLY = float("nan")
PULL_SP = (K_SP - K_JOINT) / SIG_K_SP
PULL_CL = (K_CL_ONLY - K_JOINT) / SIG_CL_ONLY
PULL_SLK = (K_SL_ONLY - K_JOINT) / SIG_SL_ONLY if np.isfinite(SIG_SL_ONLY) else float("nan")
PULL_B = math.log10(B_JOINT) / SIG_B_PULL_DEX
P("  SPARC    kappa %.5f +- %.5f  -> pull %+.2f sigma" % (K_SP, SIG_K_SP, PULL_SP))
P("  clusters kappa %.5f +- %.5f  -> pull %+.2f sigma" % (K_CL_ONLY, SIG_CL_ONLY, PULL_CL))
P("  SLACS    kappa %.4f +- %.4f  -> pull %+.2f sigma  (Delta-chi2=1 range [%.3f, %.3f])"
  % (K_SL_ONLY, SIG_SL_ONLY, PULL_SLK, _lo_sl, _hi_sl))
P("  IMF      log10(B_joint) = %+.5f dex, sigma = %.5f dex -> pull %+.2f sigma ; 95%% upper %.4f -> %s"
  % (math.log10(B_JOINT), SIG_B_PULL_DEX, PULL_B, TREU_95HI, "OUTSIDE" if B_JOINT > TREU_95HI else "inside"))
ck("C13", abs(PULL_SP) < 2.0 and abs(PULL_CL) < 2.0 and 1.5 < abs(PULL_B) < 3.5
   and abs(CHI2_SP_RAW / DOF_SP - 2.22) < 0.05 and 0.4 < CHI2_SL_RAW / (NL - 2) < 1.6,
   "SPARC %+.2f, clusters %+.2f, SLACS(kappa) %+.2f, IMF %+.2f ; chi2/dof %.4f / %.4f"
   % (PULL_SP, PULL_CL, PULL_SLK, PULL_B, CHI2_SP_RAW / DOF_SP, CHI2_SL_RAW / (NL - 2)),
   "kappa pulls within 2 sigma ; IMF pull in [1.5,3.5] ; SPARC chi2/dof 2.22 +- 0.05 ; SLACS 0.4-1.6",
   "no channel is pulled in kappa; the one >2 sigma statement is the IMF normalisation")

# =====================================================================================
# C14  the global tension and its decomposition
# =====================================================================================
head("C14  THE GLOBAL TENSION T AND ITS DECOMPOSITION: PRIOR vs DATA")

NDOF_SHARED = 2
CHI2_SL_MIN = _chi_sl_min
CHI2_CL_MIN = float(r_cl.fun)
D_SP = CHI2_SP_JOINT
D_SL = (CHI2_SL_DATA + CHI2_PR) - CHI2_SL_MIN
D_CL = CHI2_CL_JOINT - CHI2_CL_MIN
TENSION = D_SP + D_SL + D_CL
P_T = float(chi2dist.sf(TENSION, NDOF_SHARED))
SIG_T = float(np.sqrt(chi2dist.isf(P_T, 1)))
FIT_NP = profile_fit(use_prior=False)
K_NP, CHI2_NP, B_NP = FIT_NP["kappa"], FIT_NP["chi2"], FIT_NP["B"]
CHI2_SL_NP_MIN = float(np.min([slacs_at(k, prior=False)[0] for k in _G]))
T_DATA = CHI2_NP - CHI2_SL_NP_MIN
P_T_D = float(chi2dist.sf(T_DATA, NDOF_SHARED))
SIG_T_D = float(np.sqrt(chi2dist.isf(P_T_D, 1)))
T_PRIOR = TENSION - T_DATA
_k_slmin = float(_G[_i])
_lnB_slmin = -float(SPL_B(math.log(_k_slmin))) / (C_TOT + 1.0 / SIG_B_PRIOR ** 2)
PR_AT_SLMIN = _lnB_slmin ** 2 / SIG_B_PRIOR ** 2
P("  sum of channel minima: SPARC 0, clusters %.4f, SLACS+prior %.4f -> %.4f"
  % (CHI2_CL_MIN, CHI2_SL_MIN, CHI2_CL_MIN + CHI2_SL_MIN))
P("  T = chi2_joint - sum(minima) = %.5f - %.5f = %.4f for %d shared parameters -> p = %.4f (%.2f sigma)"
  % (CHI2_TOT, CHI2_CL_MIN + CHI2_SL_MIN, TENSION, NDOF_SHARED, P_T, SIG_T))
P("  decomposition: SPARC %+.4f + SLACS %+.4f + clusters %+.4f = %.4f" % (D_SP, D_SL, D_CL, D_SP + D_SL + D_CL))
P("  the IMF prior term at the joint is %.4f (%.4f at the SLACS-only minimum)" % (CHI2_PR, PR_AT_SLMIN))
P("  data-only refit (prior dropped): kappa = %.5f, B = %.5f, chi2 = %.5f ; T_data = %.4f (%.2f sigma)"
  % (K_NP, B_NP, CHI2_NP, T_DATA, SIG_T_D))
P("  T_prior = T - T_data = %.4f ; %.1f%% of T is the IMF normalisation" % (T_PRIOR, 100 * T_PRIOR / TENSION))
ck("C14", 1.0 < TENSION < 8.0 and abs((D_SP + D_SL + D_CL) - TENSION) < 1e-6 and 0.0 <= T_DATA < TENSION
   and (TENSION - T_DATA) > 0.5 * TENSION,
   "T = %.3f (%.2f sigma) ; data-only %.3f (%.2f sigma) ; prior %.3f"
   % (TENSION, SIG_T, T_DATA, SIG_T_D, T_PRIOR),
   "1 < T < 8 ; decomposition exact ; 0 <= T_data < T ; more than half of T is the prior",
   "the tension is small and mostly the IMF normalisation, not a kappa disagreement")

# =====================================================================================
# C15  Delta chi2: thermal vs kappa = 1/2, everything profiled
# =====================================================================================
head("C15  DELTA-CHI2(THERMAL vs kappa=1/2) WITH B AND u PROFILED AT EACH POINT")


def at_point(kfix, use_sigma=False, use_prior=True):
    v, lb = slacs_at(kfix, prior=use_prior, sigma=use_sigma)
    return ((kfix - K_SP) / SIG_K_SP) ** 2 + v + chi2_cluster(kfix, u_best(kfix)), lb


C_TH, LNB_TH = at_point(K_TH)
C_HF, LNB_HF = at_point(K_HF)
D_TH_HF = C_HF - C_TH
SIG_D = math.sqrt(abs(D_TH_HF))
LR = math.exp(D_TH_HF / 2.0) if D_TH_HF > 0 else float("nan")
P("  thermal:  kappa_P3 = %.6f (a0 = %.6e) -> B = %.5f, u = %.5f, chi2 = %.5f"
  % (K_TH, A0_THERM_DEPLOYED, math.exp(LNB_TH), u_best(K_TH), C_TH))
P("  kappa=1/2: kappa_P3 = %.6f (a0 = %.6e) -> B = %.5f, u = %.5f, chi2 = %.5f"
  % (K_HF, A0_HALF, math.exp(LNB_HF), u_best(K_HF), C_HF))
P("  Delta-chi2(1/2 - thermal) = %+.6f -> %.4f sigma (1 dof) -> likelihood ratio %.4f : 1"
  % (D_TH_HF, SIG_D, LR))
_dcl = chi2_cluster(K_HF, u_best(K_HF)) - chi2_cluster(K_TH, u_best(K_TH))
_dsp = ((K_HF - K_SP) / SIG_K_SP) ** 2 - ((K_TH - K_SP) / SIG_K_SP) ** 2
_dsl = D_TH_HF - _dsp - _dcl
P("  decomposition: SPARC %+.4f, SLACS+prior %+.4f, clusters %+.4f (sum %+.4f)"
  % (_dsp, _dsl, _dcl, _dsp + _dsl + _dcl))
P("  the free fit sits %.2f sigma (stat) from the thermal point and %.2f sigma from kappa = 1/2"
  % ((K_JOINT - K_TH) / SIG_K_JOINT, (K_HF - K_JOINT) / SIG_K_JOINT))
P("  the thermal point costs Delta = %+.6f against the free fit (chi2 %.5f vs %.5f)"
  % (C_TH - CHI2_JOINT, C_TH, CHI2_JOINT))
A74_D = 1.880786 - 0.016917
P("  against A74's Delta 1.863869: this lane %+.6f (%+.2f%%) ; A74's LR 2.5394 -> this lane %+.4f (%+.2f%%)"
  % (D_TH_HF, 100 * (D_TH_HF / A74_D - 1), LR, 100 * (LR / 2.5394 - 1)))
C_P3H, _ = at_point(K_P3H)
P("  the OTHER '1/2' (kappa_P3 = 0.5, a0 = %.4e): chi2 = %.4f, Delta vs thermal = %+.4f (%.2f sigma)"
  % (A0_P3_HALF, C_P3H, C_P3H - C_TH, math.sqrt(abs(C_P3H - C_TH))))
ck("C15", 1.0 < D_TH_HF < 3.0 and abs((_dsp + _dsl + _dcl) - D_TH_HF) < 1e-6 and 1.5 < LR < 5.0,
   "Delta = %+.4f -> %.3f sigma, LR %.3f ; decomposition closes to %.1e"
   % (D_TH_HF, SIG_D, LR, abs((_dsp + _dsl + _dcl) - D_TH_HF)),
   "1 < Delta < 3 ; decomposition exact ; 1.5 < LR < 5",
   "with everything profiled the thermal point beats kappa = 1/2 by ~1.4 sigma: not a decision")

# =====================================================================================
# C16  is the lensing channel kappa-blind?
# =====================================================================================
head("C16  THE LENSING CHANNEL IS kappa-BLIND: JOINT kappa WITH AND WITHOUT SLACS")

FIT_NS = profile_fit(use_slacs=False)
FIT_NC = profile_fit(use_cluster=False)
K_NOSLAC = FIT_NS["kappa"]
P("  joint WITH SLACS    : kappa = %.5f +- %.5f" % (K_JOINT, SIG_K_JOINT))
P("  joint WITHOUT SLACS : kappa = %.5f +- %.5f" % (K_NOSLAC, FIT_NS["sigma_kappa"]))
P("  joint WITHOUT cluster: kappa = %.5f +- %.5f" % (FIT_NC["kappa"], FIT_NC["sigma_kappa"]))
P("  SPARC alone         : kappa = %.5f +- %.5f" % (K_SP, SIG_K_SP))
P("  SLACS moves kappa by %+.5f (%.2f sigma of the joint error)"
  % (K_JOINT - K_NOSLAC, (K_JOINT - K_NOSLAC) / SIG_K_JOINT))
# the SLACS chi2 split: data (B profiled, no prior) vs the prior-driven part
_sl_data_20 = float(slacs_at(0.20, prior=False)[0])
_sl_data_80 = float(slacs_at(0.80, prior=False)[0])
_sl_20 = float(slacs_at(0.20, prior=True)[0])
_sl_80 = float(slacs_at(0.80, prior=True)[0])
_sl_band = _sl_20 - _sl_80
_sl_data_band = _sl_data_20 - _sl_data_80
_sl_prior_band = _sl_band - _sl_data_band
P("  SLACS DATA alone (B profiled, prior dropped) over kappa in [0.20,0.80]: %.4f -> %.4f, Delta = %+.4f"
  % (_sl_data_20, _sl_data_80, _sl_data_band))
P("  with the IMF prior          : %.4f -> %.4f, Delta = %+.4f, of which the prior supplies %+.4f"
  % (_sl_20, _sl_80, _sl_band, _sl_prior_band))
P("  SLACS-only Delta-chi2=1 width: %.4f (range [%.3f, %.3f]); minimum at kappa = %.4f"
  % (SIG_SL_ONLY, _lo_sl, _hi_sl, K_SL_ONLY))
P("  B_req(kappa) over the same band: %.4f at 0.20 -> %.4f at 0.80 (the prior turns this into the 9 units)"
  % (math.exp(-float(SPL_B(math.log(0.20))) / C_TOT), math.exp(-float(SPL_B(math.log(0.80))) / C_TOT)))
P("  SLACS tightens sigma(kappa) from %.5f (no SLACS) to %.5f: %.2f%%"
  % (FIT_NS["sigma_kappa"], SIG_K_JOINT, 100 * (1 - SIG_K_JOINT / FIT_NS["sigma_kappa"])))
ck("C16", abs(K_JOINT - K_NOSLAC) < 0.02 and abs(_sl_data_band) < 1.0
   and abs(_sl_prior_band) > 5.0 * abs(_sl_data_band)
   and (not np.isfinite(SIG_SL_ONLY) or SIG_SL_ONLY > 0.3),
   "kappa(SLACS) - kappa(no SLACS) = %+.5f ; SLACS data Delta = %+.4f ; prior Delta = %+.4f ; sigma_SLACS = %.3f"
   % (K_JOINT - K_NOSLAC, _sl_data_band, _sl_prior_band, SIG_SL_ONLY),
   "shift < 0.02 ; |data Delta| < 1 over the band ; prior part > 5x the data part ; sigma_SLACS > 0.3",
   "the lensing DATA are kappa-blind (A80); the 9 units of 'preference' are the IMF prior acting through B_req(kappa)")

# =====================================================================================
# C17  the joint fit WITH the A85 sigma_ap term
# =====================================================================================
head("C17  ADDING THE A85 sigma_ap TERM: FORMAL AND HONEST WIDTHS")

RESULTS_SIG = {}
for _tag, _sc in (("formal", S_COND), ("honest", S_COND * SINF)):
    S_COND_USE = _sc
    _f = profile_fit(use_sigma=True)
    _cth, _lth = at_point(K_TH, use_sigma=True)
    _chf, _lhf = at_point(K_HF, use_sigma=True)
    RESULTS_SIG[_tag] = dict(kappa=_f["kappa"], B=_f["B"], chi2=_f["chi2"], dchi2=_chf - _cth,
                             B_th=math.exp(_lth), B_hf=math.exp(_lhf), s_cond=_sc,
                             sigma_kappa=_f["sigma_kappa"])
    P("  sigma_ap %-6s (s_cond = %.5f): kappa = %.5f +- %.5f, B = %.5f, chi2 = %.4f ; Delta(1/2 - thermal) = %+.4f"
      % (_tag, _sc, _f["kappa"], _f["sigma_kappa"], _f["B"], _f["chi2"], _chf - _cth))
    P("    at the thermal point B = %.5f ; at kappa = 1/2 B = %.5f" % (math.exp(_lth), math.exp(_lhf)))
S_COND_USE = S_COND
_dB_formal = RESULTS_SIG["formal"]["B"] / B_JOINT - 1
_dB_honest = RESULTS_SIG["honest"]["B"] / B_JOINT - 1
P("  B shift from sigma_ap: %+.2f%% (formal), %+.2f%% (honest) ; kappa shift %+.5f / %+.5f"
  % (100 * _dB_formal, 100 * _dB_honest, RESULTS_SIG["formal"]["kappa"] - K_JOINT,
     RESULTS_SIG["honest"]["kappa"] - K_JOINT))
P("  B moves toward A85's B = %.5f; the IMF pull becomes %.2f sigma (formal) / %.2f sigma (honest)"
  % (B85, math.log10(RESULTS_SIG["formal"]["B"]) / SIG_B_PULL_DEX,
     math.log10(RESULTS_SIG["honest"]["B"]) / SIG_B_PULL_DEX))
ck("C17", 0.0 < _dB_formal < 0.05 and 0.0 < _dB_honest < 0.02 and _dB_formal > _dB_honest
   and abs(RESULTS_SIG["formal"]["kappa"] - K_JOINT) < 0.02
   and abs(RESULTS_SIG["formal"]["dchi2"] - D_TH_HF) < 1.0,
   "B %+.2f%% formal / %+.2f%% honest ; kappa %+.5f ; Delta %+.4f"
   % (100 * _dB_formal, 100 * _dB_honest, RESULTS_SIG["formal"]["kappa"] - K_JOINT,
      RESULTS_SIG["formal"]["dchi2"]),
   "B rises 0-5% formally, less when inflated ; kappa shifts < 0.02 ; Delta changes < 1",
   "adding sigma_ap raises B (the IMF pull worsens slightly) and leaves kappa where SPARC put it")

# =====================================================================================
# C18  ledger identity 1: a0 = cH_Lambda/(2 pi)
# =====================================================================================
head("C18  LEDGER IDENTITY 1: a0 = c H_Lambda/(2 pi), TWO ROUTES")

_r_lam = abs(A0_THERM_DEPLOYED / A0_THERM_LAMBDA - 1)
_r_h0 = abs(A0_THERM_DEPLOYED / A0_THERM_H0 - 1)
_om_implied = (A0_THERM_DEPLOYED * 2 * math.pi / (C_L * H0_SI)) ** 2
_k_lam = math.sqrt(8 * math.pi / (LAMBDA_OBS * C_L ** 4 / A0_THERM_DEPLOYED ** 2))
P("  from Lambda_obs = %.4e: H_Lambda = c sqrt(Lambda/3) = %.6e 1/s, a0 = %.9e"
  % (LAMBDA_OBS, C_L * math.sqrt(LAMBDA_OBS / 3), A0_THERM_LAMBDA))
P("  from H0 sqrt(Omega_L)  : H_Lambda = %.6e 1/s, a0 = %.9e" % (H0_SI * math.sqrt(OMEGA_L), A0_THERM_H0))
P("  deployed a0 = %.9e -> residuals %.3e (Lambda route), %.3e (H0 route)"
  % (A0_THERM_DEPLOYED, _r_lam, _r_h0))
P("  the deployed value implies Omega_L = %.6f (A71 uses %.4f) and kappa_DE = %.6f (Z/4pi = %.6f)"
  % (_om_implied, OMEGA_L, _k_lam, KAPPA_DE_ALG))
ck("C18", _r_h0 < 1e-3 and _r_lam < 2e-3 and abs(_k_lam / KAPPA_DE_ALG - 1) < 2e-3,
   "residual %.2e (Lambda) / %.2e (H0) ; kappa_DE(implied) %.6f vs %.6f"
   % (_r_lam, _r_h0, _k_lam, KAPPA_DE_ALG),
   "< 2e-3 and < 1e-3 ; kappa_DE within 2e-3",
   "the postulate's identity holds at the 1e-3 level; the residual is the BRIEF's Lambda/H0 rounding, not physics")

# =====================================================================================
# C19  ledger identity 2: y_t from I(y_t) = 8 pi/kappa^2
# =====================================================================================
head("C19  LEDGER IDENTITY 2: I(y_t) = 8 pi/kappa^2, AND THE CLOSURE IS AN IDENTITY")


def hfun(y):
    return 0.5 * (math.sqrt(y * y + 4.0 * y) - y)


def F_closure(Y):
    return quad(lambda th: hfun(Y * math.tan(th)) * Y, 0.0, math.pi / 2.0, limit=400)[0]


def F_closure_exact(Y):
    return quad(lambda v: Y * Y * v * v * (4.0 - v) / (4.0 * Y * Y * (2.0 - v) ** 2 + v ** 4),
                0.0, 2.0, limit=400)[0]


TGT_TH = 8.0 * math.pi / KAPPA_DE_ALG ** 2
YT_TH = brentq(lambda Y: F_closure(Y) - TGT_TH, 10.0, 300.0, xtol=1e-11)
YT_TH_E = brentq(lambda Y: F_closure_exact(Y) - TGT_TH, 10.0, 300.0, xtol=1e-12)
YT_HALF = brentq(lambda Y: F_closure(Y) - 8.0 * math.pi / 0.25, 10.0, 300.0, xtol=1e-11)
_res = [abs(F_closure(YT_TH) - TGT_TH), abs(F_closure_exact(YT_TH_E) - TGT_TH)]
N_LAM = LAMBDA_OBS * C_L ** 4 / A0_THERM_DEPLOYED ** 2
P("  target 8 pi/kappa_DE^2 = %.6f ; y_t = %.6f (tan quadrature) / %.6f (A28 rational form), diff %.1e"
  % (TGT_TH, YT_TH, YT_TH_E, abs(YT_TH - YT_TH_E)))
P("  residual |I(y_t) - 8 pi/kappa^2| = %.1e / %.1e ; N_Lambda = Lambda c^4/a0^2 = %.4f" % (_res[0], _res[1], N_LAM))
P("  y_t at kappa = 1/2: %.6f ; inside A72's pre-registered band [60, 140]: %s / %s"
  % (YT_HALF, 60 <= YT_TH <= 140, 60 <= YT_HALF <= 140))
P("  the closure is an identity: 8 pi/kappa_DE^2 vs Lambda c^4/a0^2 differ by %.3e (%.4f%%)"
  % (abs(TGT_TH - N_LAM), 100 * abs(TGT_TH / N_LAM - 1)))
ck("C19", _res[0] < 1e-8 and _res[1] < 1e-8 and abs(YT_TH - YT_TH_E) < 1e-6 and 60 < YT_TH < 140
   and 60 < YT_HALF < 140 and abs(TGT_TH / N_LAM - 1) < 5e-3,
   "y_t %.5f (band [60,140]) ; residual %.1e ; two quadratures %.1e apart ; closure residual %.2e"
   % (YT_TH, _res[0], abs(YT_TH - YT_TH_E), abs(TGT_TH / N_LAM - 1)),
   "residual < 1e-8 ; quadratures < 1e-6 ; y_t inside [60,140] ; closure within 0.5%",
   "the thermal point's falsifier is satisfied and I(y_t) = 8 pi/kappa^2 is an identity, not data")

# =====================================================================================
# C20  ledger identity 3: L* = sigma_c^2/a0
# =====================================================================================
head("C20  LEDGER IDENTITY 3: L* = sigma_c^2/a0, AND THE 24 pc ANCHOR")

K_B = 1.380649e-23
M_H = 1.6726219e-27          # the proton mass, the value A76 used (0.06% below the H-atom mass)
T_COLD, MU_COLD = 1.0e4, 1.22
SIG_C = math.sqrt(K_B * T_COLD / (MU_COLD * M_H))
LSTAR_TH = (SIG_C ** 2 / A0_THERM_DEPLOYED) / PC
LSTAR_CAN = (SIG_C ** 2 / 9.36e-11) / PC
LSTAR_833 = (8330.0 ** 2 / A0_THERM_DEPLOYED) / PC
LSTAR_MU_LO = (SIG_C ** 2 * (1.22 / 1.40) / A0_THERM_DEPLOYED) / PC
LSTAR_MU_HI = (SIG_C ** 2 * (1.22 / 0.60) / A0_THERM_DEPLOYED) / PC
P("  sigma_c = sqrt(k_B T/mu m_H) at (T = %.0f K, mu = %.2f) = %.5f km/s (A76 K4: 8.22551)"
  % (T_COLD, MU_COLD, SIG_C / 1e3))
P("  L* = sigma_c^2/a0 = %.5f pc (thermal) ; %.5f pc (canonical 9.36e-11) ; %.5f pc with 8.33 km/s"
  % (LSTAR_TH, LSTAR_CAN, LSTAR_833))
P("  mu in [0.60, 1.40] -> L* = %.4f - %.4f pc (factor %.4f) ; the 24.000 pc anchor is %.4f pc away (%.2f%%)"
  % (LSTAR_MU_LO, LSTAR_MU_HI, LSTAR_MU_HI / LSTAR_MU_LO, LSTAR_TH - 24.0, 100 * (LSTAR_TH / 24.0 - 1)))
P("  R_core = (pi/sqrt2) L* = %.4f pc (A20's 200 pc ceiling: inside)" % (LSTAR_TH * math.pi / math.sqrt(2)))
_ident = abs((SIG_C ** 2 / A0_THERM_DEPLOYED) / (LSTAR_TH * PC) - 1)
ck("C20", abs(SIG_C / 1e3 - 8.22551) < 1e-3 and abs(LSTAR_TH - 25.44) < 0.15 and _ident < 1e-12
   and LSTAR_MU_HI / LSTAR_MU_LO > 2.0,
   "sigma_c %.5f km/s ; L* %.4f pc ; mu band %.2f-%.2f pc ; identity residual %.1e"
   % (SIG_C / 1e3, LSTAR_TH, LSTAR_MU_LO, LSTAR_MU_HI, _ident),
   "sigma_c 8.22551 +- 1e-3 ; L* 25.44 +- 0.15 pc ; identity exact ; mu band > factor 2",
   "the identity is exact and the number is ~6% above the 24 pc anchor -- A76's rounded thermal width")

# =====================================================================================
# C21  ledger identity 4: beta from the background, and Delta N_eff
# =====================================================================================
head("C21  LEDGER IDENTITY 4: beta FROM THE BACKGROUND, AND Delta N_eff")

OM_M = 1.0 - OMEGA_L
BETA_MAX = 0.0280
if MUT == "vacuum_beta":
    BETA_MAX = -0.2108          # A33's Omega_L,eff = 1 slice, which A78 corrected
_dne = lambda b: 7.4492 * (2.0 / (2.0 + 3.0 * b) - 1.0)
_beta_of_r = lambda rL: (2.0 / 3.0) * OMEGA_L * (rL - 1.0)
_rL_of_beta = lambda b: 1.0 + 1.5 * b / OMEGA_L
_c05 = abs(_beta_of_r(1.0))
_c29 = _dne(BETA_MAX)
_r_at_beta = _rL_of_beta(BETA_MAX)
_lam0 = _rL_of_beta(0.0)
if MUT == "vacuum_beta":
    _lam0 = 1.0 / (1.0 - OM_M)     # the Omega_L,eff = 1 slice: matter dropped from Friedmann
P("  beta = (2/3) Omega_L (r_Lambda - 1), r_Lambda = Lambda_bare/Lambda_obs ; at beta = 0 -> r_Lambda = %.9f" % _lam0)
P("  inverted: r_Lambda(beta) = 1 + 3 beta/(2 Omega_L) ; at beta = %.4f -> %.6f" % (BETA_MAX, _r_at_beta))
P("  Delta N_eff = 7.4492 (G_eff/G_N - 1) = %.4f beta/(1 + 1.5 beta) ; at beta = %.4f -> %+.5f"
  % (-3.0 * 7.4492 / 2.0, BETA_MAX, _c29))
_b30 = brentq(lambda b: _dne(b) + 0.30, 1e-6, 0.5, xtol=1e-14)
P("  solving Delta N_eff = -0.30: beta = %.5f (A78: 0.0280) ; r_Lambda in (%.6f, %.6f)"
  % (_b30, _rL_of_beta(0.0), _rL_of_beta(_b30)))
P("  beta = 0 sits at Lambda_bare = Lambda_obs (A78's correction of A33's 1.462, the Omega_L,eff = 1 slice)")
ck("C21", _c05 < 1e-12 and abs(_c29 + 0.30) < 2e-3 and abs(_lam0 - 1.0) < 1e-9 and BETA_MAX < 0.03
   and abs(_r_at_beta - 1.0607) < 5e-3 and abs(_b30 - 0.0280) < 5e-4,
   "r_Lambda(0) = %.9f ; Delta N_eff(beta_max) = %+.5f ; r_Lambda(beta_max) = %.5f ; beta(-0.30) = %.5f"
   % (_lam0, _c29, _r_at_beta, _b30),
   "r_Lambda(0) = 1 to 1e-9 ; Delta N_eff = -0.30 +- 2e-3 ; r_Lambda < 1.061 +- 0.005 ; beta 0.0280 +- 5e-4",
   "beta is bounded by BBN, and the bound puts the bare vacuum within 6% of the observed one")

# =====================================================================================
# C22  the ledger count: rank of the constraint system
# =====================================================================================
head("C22  THE LEDGER COUNT: RANK OF THE (K, gamma, L*, sigma_c, a0) CONSTRAINT SYSTEM")

# log-space Jacobian of the two defining relations:
#   ln gamma = ln K + 2 ln L* - ln 2      -> (0, 1, 2, 0, 0)
#   ln sigma_c = (1/2)(ln a0 + ln L*)     -> (0, 0, 0.5, 1, 0.5)
_J = np.array([[0.0, 1.0, 2.0, 0.0, 0.0],
               [0.0, 0.0, 0.5, 1.0, 0.5]])
_sv = np.linalg.svd(_J, compute_uv=False)
RANK = int(np.sum(_sv > 1e-12))
NULL5 = 5 - RANK                      # includes the K and a0 directions, which are fixed EXTERNALLY
# the symbols that the two relations actually leave free: (gamma, L*, sigma_c)
_U, _S, _Vt = np.linalg.svd(np.array([[1.0, 2.0, 0.0], [0.0, 0.5, 1.0]]))
_ns = _Vt[-1]
_ns = _ns / _ns[np.argmax(np.abs(_ns))]
NULL = 3 - int(np.sum(_S > 1e-12))
P("  relations: gamma = K L*^2/2 ; sigma_c^2 = a0 L* ; K forced, a0 fixed by P-therm")
P("  singular values of the 2x5 Jacobian: " + ", ".join("%.4f" % s for s in _sv))
P("  rank = %d of 5 ; but K and a0 are fixed OUTSIDE these relations (K by the action, a0 by P-therm)," % RANK)
P("  so the self-consistent count is over (gamma, L*, sigma_c): rank 2 of 3 -> %d free direction" % NULL)
P("  the null vector (dln gamma, dln L*, dln sigma_c) = (%+.4f, %+.4f, %+.4f)" % tuple(_ns))
P("  i.e. |dln gamma| = 2 |dln L*| and |dln sigma_c| = 0.5 |dln L*|: ONE scale, not three")
P("  with eta (independent: A68 D10 proves the action does not force eta = gamma) the count is %d" % (NULL + 1))
ck("C22", RANK == 2 and NULL == 1 and abs(abs(_ns[0] / _ns[1]) - 2.0) < 0.05
   and abs(abs(_ns[2] / _ns[1]) - 0.5) < 0.02,
   "rank %d/5 ; free block (gamma,L*,sigma_c) nullity %d ; null vector (%+.3f, %+.3f, %+.3f)"
   % (RANK, NULL, _ns[0], _ns[1], _ns[2]),
   "rank 2 ; nullity 1 in the free block ; dln gamma/dln L* = 2, dln sigma_c/dln L* = 0.5",
   "the ledger's three 'free' symbols are one scale; with eta that is two free parameters, not four")

# =====================================================================================
# C23  the systematics and the total error
# =====================================================================================
head("C23  THE SYSTEMATIC FLOOR AND THE TOTAL ERROR ON kappa")

SYS_FRAC = math.sqrt(EST_HALF_SPAN ** 2 + 0.161 ** 2 + 0.125 ** 2 + 0.10 ** 2 + 0.05 ** 2)
SIG_K_TOT = math.sqrt(SIG_K_JOINT ** 2 + (SYS_FRAC * K_JOINT) ** 2)
D_STAT_TH = (K_TH - K_JOINT) / SIG_K_JOINT
D_TOT_TH = (K_TH - K_JOINT) / SIG_K_TOT
D_STAT_HF = (K_HF - K_JOINT) / SIG_K_JOINT
D_TOT_HF = (K_HF - K_JOINT) / SIG_K_TOT
D_STAT_P3H = (K_P3H - K_JOINT) / SIG_K_JOINT
P("  systematic floor: estimator %.6f, distance 0.161, H0 0.125, law 0.100, Upsilon 0.050 -> %.6f"
  % (EST_HALF_SPAN, SYS_FRAC))
BUDGET = [("statistical (joint)", SIG_K_JOINT), ("estimator/error model", EST_HALF_SPAN * K_JOINT),
          ("distance zero point", 0.161 * K_JOINT), ("H0 footing", 0.125 * K_JOINT),
          ("law choice", 0.100 * K_JOINT), ("Upsilon window", 0.050 * K_JOINT)]
P("  error budget (fraction of the total variance of kappa):")
for _nm, _sv in BUDGET:
    P("    %-24s sigma_k = %.5f   share = %5.1f%%" % (_nm, _sv, 100 * _sv ** 2 / SIG_K_TOT ** 2))
P("  sigma(kappa) stat = %.5f ; syst = %.5f ; total = %.5f (%.1f%%)"
  % (SIG_K_JOINT, SYS_FRAC * K_JOINT, SIG_K_TOT, 100 * SIG_K_TOT / K_JOINT))
P("  the coherent floor in percent: %.2f%% of kappa (A51/A71's 31.2%%)" % (100 * SYS_FRAC))
P("  thermal point : %+.2f sigma (stat) / %+.2f sigma (total) from the free fit" % (D_STAT_TH, D_TOT_TH))
P("  kappa_DE = 1/2: %+.2f sigma (stat) / %+.2f sigma (total)" % (D_STAT_HF, D_TOT_HF))
P("  kappa_P3 = 1/2: %+.2f sigma (stat) / %+.2f sigma (total)" % (D_STAT_P3H, (K_P3H - K_JOINT) / SIG_K_TOT))
P("  the two footings are %.2f sigma apart statistically, %.2f in total"
  % ((K_HF - K_TH) / SIG_K_JOINT, (K_HF - K_TH) / SIG_K_TOT))
ck("C23", abs(SYS_FRAC - 0.3122) < 5e-4 and abs(SIG_K_TOT - 0.1207) < 0.008 and D_TOT_TH < 1.0
   and 1.0 < D_STAT_HF < 2.5 and D_STAT_P3H > 4.0,
   "sys %.4f ; sigma_tot %.5f ; thermal %+.2f stat ; 1/2 %+.2f stat ; kappa_P3=1/2 %+.2f stat"
   % (SYS_FRAC, SIG_K_TOT, D_STAT_TH, D_STAT_HF, D_STAT_P3H),
   "sys 0.3122 +- 5e-4 ; sigma_tot 0.1207 +- 0.008 ; thermal inside 1 sigma total ; "
   "1/2 (a0 = 9.354e-11) 1-2.5 sigma ; kappa_P3 = 1/2 > 4 sigma",
   "the thermal point is inside the total error and ~1.4 sigma away statistically; the old kappa_P3 = 1/2 target is ~4.8 sigma")

# =====================================================================================
# C24  the error-model factor: the same two points on the raw SPARC chi2
# =====================================================================================
head("C24  THE ERROR-MODEL FACTOR: THE SAME TWO POINTS ON THE RAW SPARC chi2")

CH_RAW_TH = float(chi2_sparc(A0_THERM_DEPLOYED))
CH_RAW_HF = float(chi2_sparc(A0_HALF))
D_RAW = CH_RAW_HF - CH_RAW_TH
SCALE = CHI2_SP / DOF_SP
P("  raw SPARC chi2 at the thermal point = %.3f ; at kappa = 1/2 = %.3f ; Delta = %.3f" % (CH_RAW_TH, CH_RAW_HF, D_RAW))
P("  rescaled to chi2/dof = 1 (factor %.4f): Delta = %.3f -> %.2f sigma" % (SCALE, D_RAW / SCALE, math.sqrt(D_RAW / SCALE)))
P("  the compressed likelihood gives Delta = %+.4f -> %.3f sigma: a factor %.1f in chi2"
  % (D_TH_HF, SIG_D, (D_RAW / SCALE) / max(D_TH_HF, 1e-12)))
ck("C24", 100 < D_RAW < 140 and (D_RAW / SCALE) / D_TH_HF > 20,
   "Delta(raw) %.2f -> %.2f sigma ; compressed %.3f sigma ; ratio %.1f"
   % (D_RAW, math.sqrt(D_RAW / SCALE), SIG_D, (D_RAW / SCALE) / D_TH_HF),
   "100 < raw Delta < 140 ; ratio > 20",
   "if the per-point errors were right the thermal point would win at 7 sigma; they are not, and the bootstrap is why")

# =====================================================================================
# C25  the ledger itself
# =====================================================================================
head("C25  THE DEFINITIVE PARAMETER LEDGER: NINE SYMBOLS, FIVE CLASSES, ONE COUNT")

K_SI = 4.0 * math.pi * G_N
RHO_C = 2.2565e-27                     # A16/A76's cold-sector density, kg/m^3
_cs_K = math.sqrt(K_SI * RHO_C * (LSTAR_TH * PC) ** 2 / 2.0)
_cs_K8 = math.sqrt(8.0 * math.pi * G_N * RHO_C * (LSTAR_TH * PC) ** 2 / 2.0)
_id_K = abs(2.0 * _cs_K ** 2 / (K_SI * RHO_C) / (LSTAR_TH * PC) ** 2 - 1.0)
_id_K8 = abs(2.0 * _cs_K8 ** 2 / (8.0 * math.pi * G_N * RHO_C) / (LSTAR_TH * PC) ** 2 - 2.0)
P("  K = 4 pi G = %.9e m^3 kg^-1 s^-2 ; c_s = sqrt(K rho_c L*^2/2) = %.5f m/s (A16 0.7204 at L* = 24 pc)"
  % (K_SI, _cs_K))
P("  the identity 2 c_s^2/(K rho_c) = L*^2 holds to %.1e at K = 4 pi G and to %.1e against 2 at K = 8 pi G"
  % (_id_K, _id_K8))
P("  c_s at K = 8 pi G would be %.5f m/s = sqrt(2) x the 4 pi G value (%.5f) -- the Newtonian limit fixes K"
  % (_cs_K8, _cs_K8 / _cs_K))

LEDGER = [
    ("K", "FORCED BY ACTION", "%.6e m^3 kg^-1 s^-2 (4 pi G)" % K_SI,
     "the static Poisson limit G_N = K/4pi; the identity 2c_s^2/(K rho_c) = L*^2 holds at 4 pi G (%.1e) and fails by 2 at 8 pi G (A76 K1, mutated there)" % _id_K),
    ("alpha", "FORCED BY ACTION", "alpha/gamma = 1 exactly",
     "one coefficient in front of both gradient operators: alpha = gamma forced (A68 D10/D12, C23-C24 determinant 4); only the common scale is free"),
    ("gamma", "UNCONSTRAINED FREE SCALE", "%.4e eV^-4 at L* = 25.42 pc, x%.2f over the [24,90] pc window"
     % (5.9371406479e-07 * (LSTAR_TH / 24.0) ** 2, (90.0 / 24.0) ** 2),
     "gamma = K L*^2/2 is a DEFINITION (A76 K1); no observable measures gamma alone (A76 section 4.4: (L*/r)^2, O(1) only inside 24 pc); A33 row 7's 'M' is downgraded by A76"),
    ("eta", "UNCONSTRAINED FREE SCALE", "bounded only by eta >= gamma (luminality)",
     "A77: no Kubo/transport matching exists; gamma/eta free over (0, 1.916e-07] one-sided; the P modes are unpopulated, uncoupled and unsourced (A77 section 3.3)"),
    ("beta", "BOUNDED BY BBN/BACKGROUND", "beta < %.4f ; Lambda_bare/Lambda_obs in (1.000000, %.4f)" % (BETA_MAX, _r_at_beta),
     "Delta N_eff = -11.1738 beta/(1+1.5 beta) > -0.30 -> beta < 0.0280 (A78 C29); beta = 0 at Lambda_bare = Lambda_obs (A78 C05)"),
    ("a0", "FIXED BY THE P-therm POSTULATE", "%.4e m/s^2 ; kappa_DE = Z/4pi = %.9f" % (A0_THERM_DEPLOYED, KAPPA_DE_ALG),
     "A75: the gate is athermal at fixed drive (C_g = 0), the carrier misses the thermal wavelength by 1.989424e+09, and A72's formula is mass-independent; P-therm is a POSTULATE, and it forces R = 3pi/2 = 4.712388980 not-in {1,2,4}"),
    ("L*", "UNCONSTRAINED FREE SCALE", "%.4f pc (if sigma_c = 8.2255 km/s) ; window [24, 90] pc" % LSTAR_TH,
     "A76: L* = sigma_c^2/a0 has coefficient exactly 1 but NO measured sigma_c exists on disk (zero determinations); the 24 pc floor is 23.4289 rounded, so L* is FITTED(sigma_c)"),
    ("sigma_c", "DERIVED FROM ATOMIC INPUT", "%.5f km/s (T = 1e4 K, mu = 1.22) ; L* in %.2f-%.2f pc over mu in [0.60,1.40]"
     % (SIG_C / 1e3, LSTAR_MU_LO, LSTAR_MU_HI),
     "CONDITIONAL: sigma_c = sqrt(k_B T/mu m_H) (A76 K4 = 8.22551); A76 section 3.1 finds zero measured determinations and mu is unmeasured (factor 1.528 in sigma_c, 2.333 in L*), so this is an astrophysical premise, not a derivation in force"),
    ("Lambda_bare", "BOUNDED BY BBN/BACKGROUND", "Lambda_bare/Lambda_obs in (1.000000, %.6f)" % _r_at_beta,
     "A78 C05/C29/C30: 3(2+3beta)H^2 = 2 Lambda_bare c^2 + 4K rho; with beta < 0.0280 the bare vacuum is within 6.13% of the observed one"),
]
CLASSES = ("FORCED BY ACTION", "FIXED BY THE P-therm POSTULATE", "DERIVED FROM ATOMIC INPUT",
           "BOUNDED BY BBN/BACKGROUND", "UNCONSTRAINED FREE SCALE")
P("  %-12s %-32s %s" % ("symbol", "class", "value"))
for _sym, _cls, _val, _ev in LEDGER:
    P("  %-12s %-32s %s" % (_sym, _cls, _val))
P("  evidence per row:")
for _sym, _cls, _val, _ev in LEDGER:
    P("    %-12s %s" % (_sym, _ev))
NFREE_SYM = sum(1 for x in LEDGER if x[1] == "UNCONSTRAINED FREE SCALE")
NBOUND = sum(1 for x in LEDGER if x[1] == "BOUNDED BY BBN/BACKGROUND")
NFORCED = sum(1 for x in LEDGER if x[1] == "FORCED BY ACTION")
NPOST = sum(1 for x in LEDGER if x[1] == "FIXED BY THE P-therm POSTULATE")
NATOM = sum(1 for x in LEDGER if x[1] == "DERIVED FROM ATOMIC INPUT")
NINDEP = NULL + 1
P("  counts: %d forced, %d postulate, %d atomic-conditional, %d bounded, %d free symbols (%d independent)"
  % (NFORCED, NPOST, NATOM, NBOUND, NFREE_SYM, NINDEP))
P("  genuinely free parameters: %d (eta, plus ONE P-sector scale shared by gamma, L*, sigma_c)." % NINDEP)
P("  If the atomic sigma_c were adopted as an input the count would be 1 (eta alone) -- A76 refuses that adoption.")
ck("C25", len(LEDGER) == 9 and all(x[1] in CLASSES for x in LEDGER) and NFREE_SYM == 3
   and NINDEP == 2 and NFORCED + NPOST + NATOM + NBOUND + NFREE_SYM == 9,
   "9 symbols: %d forced, %d postulate, %d atomic, %d bounded, %d free -> %d independent"
   % (NFORCED, NPOST, NATOM, NBOUND, NFREE_SYM, NINDEP),
   "9 symbols, every one in exactly one class, 3 free symbols collapsing to 2 independent",
   "the ledger is complete and its count is the rank computation's: two free parameters, not four")



# =====================================================================================
# C26  the cross-lane anchors this report quotes, verified against their own arithmetic
# =====================================================================================
head("C26  CROSS-LANE ANCHORS QUOTED IN THIS REPORT (each re-derived from its lane's numbers)")

A51_K = float(A51["joint"]["kappa"]); A51_S = float(A51["joint"]["sigma_stat"])
A74_D_FREE = 0.016917; A74_D_HALF = 1.880786
A74_D = A74_D_HALF - A74_D_FREE
A74_SIG = math.sqrt(A74_D); A74_LR = math.exp(A74_D / 2.0)
A80_D1 = float(A80["a71_k25"]["delta_B1"]); A80_DP = float(A80["a71_k25"]["delta_Bprof"])
A85_TEN = math.log10(A85["route2"]["thermal"]["beta0"]["B"]) / math.sqrt(
    A85["route2"]["thermal"]["beta0"]["sB_hi"] ** 2 + 0.0361 ** 2 + 0.0143 ** 2)
A76_L_TH = (8.22551e3) ** 2 / 8.618166e-11 / PC
A75_R = 1.5 * math.pi
A75_LAM_RATIO = 8.0 / (3.0 * math.pi)
A77_GAMMA = 5.9371406479e-07
A77_LAMC = (24.025012 * PC) / (math.sqrt(2.0) * 8325.7 / C_L) / KPC
P("  A51 : joint kappa(sparc+clusters) = %.6f +- %.6f ; SPARC bootstrap %.9f ; systematic floor 0.3122"
  % (A51_K, A51_S, A51["sparc"]["sigma_stat_boot"]))
P("  A71 : kappa = 0.37765 +- 0.02579, B = 1.1916, T = 5.686 (1.89 sigma), B pull 1.97 sigma, Delta(1/2, B profiled) = 20.92")
P("  A72 : kappa_DE = Z/4pi = %.12f ; a0 = cH_Lambda/2pi = %.9e ; 1/7 is Omega_L = 32pi/147 = %.9f"
  % (KAPPA_DE_ALG, 8.618165900e-11, 32 * math.pi / 147))
P("  A74 : a0-implied kappa_DE = 0.460454 (A74's own constants) ; L* = 26.087 pc ; y_t = 77.943961")
P("  A74 : Delta(thermal-free) = %.6f, Delta(1/2-free) = %.6f -> Delta = %.6f, %.4f sigma, LR %.4f"
  % (A74_D_FREE, A74_D_HALF, A74_D, A74_SIG, A74_LR))
P("  A75 : kappa_th = %.9f ; R = 3pi/2 = %.9f not-in {1,2,4} ; Lambda_pred/Lambda_obs = 8/(3pi) = %.9f (15.1%%)"
  % (KAPPA_DE_ALG, A75_R, A75_LAM_RATIO))
P("  A76 : sigma_c = 8.22551 km/s -> L* = %.4f pc at a0 = 8.618166e-11 ; canonical %.4f pc ; the 24 pc floor is 23.4289 pc"
  % (A76_L_TH, 23.4261))
P("  A77 : gamma = %.10e eV^-4 ; lambda_C = 611.0801 kpc ; gamma/eta free over a factor 1.335776e+08" % A77_GAMMA)
P("  A78 : beta < 0.0280 ; Delta N_eff = -0.300 at the bound ; Lambda_bare/Lambda_obs in (1.000, 1.061)")
P("  A80 : Delta(B=1) = %.4f, Delta(B profiled) = %.4f ; B(n=4) = %.5f ; B(n=6) = %.5f ; n_zero = %.4f ; n_ML = %.4f"
  % (A80_D1, A80_DP, B80_N4, B80_N6, N_ZERO, float(A80["models"]["thermal"]["b_renorm"]["n"])))
P("  A85 : B = %.5f +- %.5f +- %.5f -> %.2f sigma vs Treu ; angle %.4f deg ; sigma(kappa) %.4f -> %.4f ; chi2/dof = 8.13 ; inflation %.4f"
  % (B85, B85_S, B85_S * SINF, A85_TEN, A85["fisher"]["angle"], SK_RE, A85["fisher"]["sk_joint"], SINF))
P("  A85's lambda_C check from A77's formula: L*/(sqrt2 sigma_c/c) = %.4f kpc (A77 611.0801, %.3f%%)"
  % (A77_LAMC, 100 * abs(A77_LAMC / 611.0801 - 1)))
P("  this lane against A74's quoted values: y_t 77.943961 -> %.6f (%+.3f%%) ; L* 26.087 pc -> %.5f pc (%+.2f%%)"
  % (YT_TH, 100 * (YT_TH / 77.943961 - 1), LSTAR_833, 100 * (LSTAR_833 / 26.087 - 1)))
P("  against A76's L* at its own a0: 25.4425 pc -> %.5f pc at a0 = 8.6257e-11 (%+.2f%%)"
  % (LSTAR_TH, 100 * (LSTAR_TH / 25.4425 - 1)))
ck("C26", abs(A74_SIG - 1.365236) < 1e-5 and abs(A74_LR - 2.5394) < 1e-3 and abs(A80_D1 - 6.3517) < 1e-3
   and abs(A80_DP - 0.2854) < 1e-3 and abs(A85_TEN - 2.2728) < 2e-3 and abs(A76_L_TH - 25.4425) < 1e-3
   and abs(A75_R - 4.712388980) < 1e-9 and abs(A77_LAMC / 611.0801 - 1) < 5e-3
   and abs(A51_K - 0.37083) < 1e-5,
   "A74 %.6f/%.4f sigma/%.4f ; A80 %.4f/%.4f ; A85 %.4f sigma ; A76 %.4f pc ; A77 %.4f kpc"
   % (A74_D, A74_SIG, A74_LR, A80_D1, A80_DP, A85_TEN, A76_L_TH, A77_LAMC),
   "each anchor reproduces its lane's arithmetic to its quoted precision",
   "the numbers this report imports are re-derived, so a misquote in either direction would show up here")

# =====================================================================================
# summary
# =====================================================================================
head("SUMMARY")
NPASS = sum(1 for c in CHECKS if c["pass_"])
P("  %d/%d checks PASS   (%.1f s)" % (NPASS, len(CHECKS), time.time() - T0))
P("  joint kappa_P3 = %.6f +- %.6f (stat) +- %.6f (syst) = %.6f +- %.6f"
  % (K_JOINT, SIG_K_JOINT, math.sqrt(max(SIG_K_TOT ** 2 - SIG_K_JOINT ** 2, 0)), K_JOINT, SIG_K_TOT))
P("  a0 = %.6e m/s^2 ; B = %.5f ; u = %.5f ; chi2 = %.5f" % (A0_JOINT, B_JOINT, U_JOINT, CHI2_TOT))
P("  T = %.4f (%.2f sigma), of which the IMF prior is %.4f ; data-only T = %.4f (%.2f sigma)"
  % (TENSION, SIG_T, T_PRIOR, T_DATA, SIG_T_D))
P("  Delta-chi2(thermal - 1/2) = %+.4f -> %.4f sigma ; LR = %.4f : 1" % (D_TH_HF, SIG_D, LR))
P("  with sigma_ap: kappa = %.5f, B = %.5f (formal) / kappa = %.5f, B = %.5f (honest)"
  % (RESULTS_SIG["formal"]["kappa"], RESULTS_SIG["formal"]["B"],
     RESULTS_SIG["honest"]["kappa"], RESULTS_SIG["honest"]["B"]))
P("  ledger: 2 independent free parameters (one P-sector scale + eta), 2 BBN-bounded, 1 postulate, 2 forced")
P("  wrote a81_results%s.json ; %d/%d PASS ; exit %d"
  % (TAG, NPASS, len(CHECKS), 0 if NPASS == len(CHECKS) else 1))

RES = dict(lane="A81", generated=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           mutate=MUT or None, n_check=len(CHECKS), n_pass=NPASS, runtime_s=time.time() - T0,
           checks=[{k: (bool(v) if k == "pass_" else v) for k, v in c.items()} for c in CHECKS],
           constants=dict(G=G_N, c=C_L, H0=H0_KMS, Omega_L=OMEGA_L, a0_per_kappa=A0_PER_KAPPA,
                          a0_thermal_deployed=A0_THERM_DEPLOYED, a0_thermal_lambda=A0_THERM_LAMBDA,
                          a0_thermal_h0=A0_THERM_H0, a0_half=A0_HALF, kappa_de_alg=KAPPA_DE_ALG,
                          kappa_p3_thermal=K_TH, kappa_p3_half=K_HF, kappa_p3_05=K_P3H),
           data=dict(n_sparc_files=len(SPARC_FILES), n_galaxies=NG, n_points=NPT,
                     sha256_sparc=H_SPARC, sha256_slacs=H_SLACS, n_lenses=NL, n_treu=len(ALPHA_TREU)),
           sparc=dict(a0=A0_SP, kappa=K_SP, chi2=CHI2_SP, dof=DOF_SP, chi2_dof=CHI2_SP / DOF_SP,
                      sigma_boot_frac=BOOT_FRAC, sigma_formal_frac=SIG_DCHI2, sigma_kappa=SIG_K_SP,
                      chi2_raw_at_joint=CHI2_SP_RAW),
           slacs=dict(B_req_half=B_REQ_HALF, median_ratio=MED50, mean_ln=MEANLN50, sd_ln=SD50,
                      dlnR_dlnB=RESP, dlnR_dlnB_mean=RESP_MEAN, dlnR_dlnB_scatter=RESP_SCAT,
                      dlnR_dlnkappa=_dlnR_dlnk, sigma_logB_dex=SIG_B_MEAS_DEX,
                      chi2_at_B1=CHI2_B1.tolist(), chi2_at_Bprof=CHI2_BPROF.tolist(),
                      kappa_grid=KG8.tolist(), delta_B1=D_B1, delta_Bprof=D_BPROF,
                      B_ml_thermal=B_ML_TH, B_req_thermal=B_REQ_TH,
                      B80_n4=B80_N4, B80_n6=B80_N6, B85=B85, B85_scaled_err=B85_S * SINF),
           cluster=dict(kappa=K_CL, sigma_kappa=K_CL * SIG_CL, R_tot=R_CAN, r_v_Mpc=RV_CAN / MPC,
                        F=F_CAN, dlnR_dlna0=DLNR),
           sigma_ap=dict(angle_deg=ANGLE, det=DET_F, cond=COND_F, sk_re=SK_RE, sk_joint=SK_JOINT_F,
                         B_sigma_thermal=_bs, slope=BSLOPE, s_cond=S_COND, inflation=SINF,
                         formal=RESULTS_SIG["formal"], honest=RESULTS_SIG["honest"]),
           joint=dict(kappa=K_JOINT, a0=A0_JOINT, B=B_JOINT, B_req=B_REQ_JOINT, u=U_JOINT, chi2=CHI2_TOT,
                      sigma_kappa_stat=SIG_K_JOINT, sigma_kappa_syst=SYS_FRAC * K_JOINT,
                      sigma_kappa_tot=SIG_K_TOT, sys_frac=SYS_FRAC,
                      kappa_lo=FIT["klo"], kappa_hi=FIT["khi"],
                      chi2_sparc=CHI2_SP_JOINT, chi2_slacs=CHI2_SL_DATA, chi2_cluster=CHI2_CL_JOINT,
                      chi2_prior=CHI2_PR, chi2_dof_sparc=CHI2_SP_RAW / DOF_SP,
                      chi2_dof_slacs=CHI2_SL_RAW / (NL - 2),
                      pull_sparc=PULL_SP, pull_cluster=PULL_CL, pull_slacs_kappa=PULL_SLK, pull_B=PULL_B,
                      tension=TENSION, tension_sigma=SIG_T, tension_data=T_DATA, tension_data_sigma=SIG_T_D,
                      tension_prior=T_PRIOR,
                      kappa_noslac=K_NOSLAC, kappa_slacs_only=K_SL_ONLY, sigma_kappa_slacs_only=SIG_SL_ONLY,
                      slacs_band_delta=_sl_band,
                      chi2_thermal=C_TH, chi2_half=C_HF, dchi2_thermal_half=D_TH_HF,
                      sigma_thermal_half=SIG_D, LR_thermal_half=LR, chi2_p3half=C_P3H,
                      B_thermal=math.exp(LNB_TH), B_half=math.exp(LNB_HF),
                      d_to_thermal_stat=D_STAT_TH, d_to_thermal_tot=D_TOT_TH,
                      d_to_half_stat=D_STAT_HF, d_to_half_tot=D_TOT_HF, d_to_p3half_stat=D_STAT_P3H),
           ledger=dict(K="FORCED BY ACTION", alpha="FORCED BY ACTION", gamma="UNCONSTRAINED FREE SCALE",
                       eta="UNCONSTRAINED FREE SCALE", beta="BOUNDED BY BBN/BACKGROUND",
                       a0="FIXED BY THE P-therm POSTULATE", Lstar="UNCONSTRAINED FREE SCALE",
                       sigma_c="DERIVED FROM ATOMIC INPUT", Lambda_bare="BOUNDED BY BBN/BACKGROUND",
                       n_independent_free=NULL + 1, rank=RANK, nullity=NULL),
           identities=dict(a0_res_lambda=_r_lam, a0_res_h0=_r_h0, kappa_de_implied=_k_lam,
                           y_t=YT_TH, y_t_half=YT_HALF, y_t_residual=_res[0],
                           closure_residual=abs(TGT_TH / N_LAM - 1),
                           Lstar_pc=LSTAR_TH, Lstar_canon_pc=LSTAR_CAN, sigma_c_kms=SIG_C / 1e3,
                           Lstar_mu_lo=LSTAR_MU_LO, Lstar_mu_hi=LSTAR_MU_HI,
                           beta_max=BETA_MAX, dne_at_max=_c29, r_lambda_max=_r_at_beta,
                           B80_minus_B85=B80_N4 - B85),
           error_model=dict(dchi2_raw=D_RAW, scale=SCALE, sigma_raw=math.sqrt(D_RAW / SCALE),
                            ratio=(D_RAW / SCALE) / D_TH_HF))
json.dump(RES, open(os.path.join(HERE, "a81_results" + TAG + ".json"), "w"), indent=1)
OUTF.close()
sys.exit(0 if NPASS == len(CHECKS) else 1)
