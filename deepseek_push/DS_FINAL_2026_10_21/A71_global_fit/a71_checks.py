#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
A71 -- THE GLOBAL CONSISTENCY TEST

One parameter set (kappa, B, u) against every channel the theory has been compared
to, with a per-channel chi2, the pulls, and the global tension stated honestly.

CHANNELS IN THE LIKELIHOOD (three, and only three):
  1. SPARC RAR          171 galaxies / 3375 points, one Upsilon per galaxy (profiled)
  2. SLACS 70 lenses    the A70 model, response dlnR/dlnB = 0.7775
  3. clusters           A18's R_req = 5.552 +- 0.427 with the sourcing fraction u
NOT in the likelihood, with the reason computed here:
  4. the closure I(y_t) = 8 pi / kappa^2   -- an IDENTITY, not data (K15, K16)
  5. BAO / SNe / CMB                       -- kappa-BLIND (K17)
  6. wide binaries                          -- a prediction with no data yet (K23)
  7. A65's L* = 24 pc                       -- the same SPARC photometry (K24)

Every number printed here is computed here from files on disk.  Nothing is downloaded.
Nothing is written outside this lane's directory.

CONVENTIONS.  SI.  kappa is A51's P3 convention:
      kappa = a0 sqrt(8 pi / 3) / (c H0),  H0 = 67.4 km/s/Mpc,
      a0 = kappa * 2.262407e-10 m/s^2,  kappa = 1/2 at a0 = 1.131204e-10.
Canonical a0 = 9.36e-11 -> kappa = 0.413730.

MUTATIONS.  A71_MUTATE=<name> changes ONE input and must break a named check.
  imf_prior | kappa_de | newton | no_boot | u_prior | closure_4pi | kappa_in_E
Exit 0 iff every check passes.

Run:     python3 a71_checks.py
Mutate:  A71_MUTATE=imf_prior python3 a71_checks.py       (must exit 1)
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
from scipy.linalg import cho_factor, cho_solve

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))

MUT = (os.environ.get("A71_MUTATE", "") or "").strip()
MUTS = ("", "imf_prior", "kappa_de", "newton", "no_boot", "u_prior",
        "closure_4pi", "kappa_in_E", "floor10", "treu", "cluster_a",
        "drop_gal", "drop_lens", "b_marg", "est_span", "closure_kernel", "err045")
if MUT not in MUTS:
    sys.exit("unknown mutation: " + MUT)
TAG = ("_MUTATE_" + MUT) if MUT else ""

T0 = time.time()
OUTF = open(os.path.join(HERE, "a71" + TAG + ".out"), "w")
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


def ck(cid, ok, measured, threshold, label=""):
    ok = bool(ok)
    CHECKS.append(dict(id=cid, pass_=ok, measured=str(measured),
                       threshold=str(threshold), label=label))
    P("  %-5s %s   %s" % (cid, "PASS" if ok else "FAIL", measured))
    P("         threshold: %s   :: %s" % (threshold, label))
    return ok


# =====================================================================================
# constants and the kappa convention
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
A0_PER_KAPPA = C_L * H0_SI / SQ_8PI3            # 2.262407e-10
A0_THEORY = 0.5 * A0_PER_KAPPA                  # 1.131204e-10
A0_CANON = 9.36e-11
A0_QUOTED = 1.132e-10                            # A55/A70's footing (three-digit P3 value)
LN10 = math.log(10.0)
LAMBDA_OBS = 1.0890e-52                          # A28's footing (m^-2)


def kappa_of_a0(a0):
    """A51's P3 convention.  Mutation kappa_de silently swaps in the rho_DE convention."""
    if MUT == "kappa_de":
        return a0 * math.sqrt(8.0 * math.pi) / (C_L * H0_SI * math.sqrt(3.0 * OMEGA_L))
    return a0 * SQ_8PI3 / (C_L * H0_SI)


def a0_of_kappa(k):
    return k * A0_PER_KAPPA


KAPPA_THEORY = kappa_of_a0(A0_THEORY)
KAPPA_CANON = kappa_of_a0(A0_CANON)

P("A71 -- THE GLOBAL CONSISTENCY TEST    (mutation: %s)" % (MUT or "none"))
P("  kappa = a0 sqrt(8 pi/3)/(c H0), H0 = %.1f km/s/Mpc, a0_per_kappa = %.6e m/s^2"
  % (H0_KMS, A0_PER_KAPPA))
P("  kappa = 1/2 at a0 = %.6e ; canonical a0 = %.3e -> kappa = %.6f"
  % (A0_THEORY, A0_CANON, KAPPA_CANON))


def sha_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


# =====================================================================================
# K1  the SPARC block
# =====================================================================================
head("K1  THE SPARC BLOCK: 175 files, 171 galaxies, 3375 points, on disk")

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
H_SPARC_A51 = "469f4f556dc813b2"

P("  files %d ; galaxies with >=5 points %d ; total points %d" % (len(SPARC_FILES), NG, NPT))
P("  sha256(concat) = %s   (A51 recorded %s)" % (H_SPARC, H_SPARC_A51))
ck("K1", len(SPARC_FILES) == 175 and NG == 171 and NPT == 3375 and H_SPARC == H_SPARC_A51,
   "175/171/3375, sha %s" % H_SPARC,
   "175 files, 171 fitted, 3375 points, sha == A51's",
   "the SPARC vector this lane fits is byte-identical to the one A51 fitted")

# =====================================================================================
# K2  the SLACS block
# =====================================================================================
head("K2  THE SLACS BLOCK: 85 catalogue rows -> 70 usable lenses")

DATA_SLACS = os.path.join(REPO, "real_research", "data", "slacs_auger2009_lenses.tsv")
DATA_TREU = os.path.join(REPO, "real_research", "cross_thread_review_2026_09_26",
                         "XR33_data_treu2010_table1.tsv")
A55JSON = os.path.join(REPO, "deepseek_push", "DS_FINAL_2026_10_21",
                       "A55_lensing_prediction", "a55_results.json")

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
P("  catalogue rows %d ; usable lenses %d ; sha256 %s" % (len(_raw), NL, H_SLACS[:16]))
ck("K2", len(_raw) == 85 and NL == 70,
   "raw %d, usable %d, sha %s" % (len(_raw), NL, H_SLACS[:16]),
   "85 rows and 70 with finite z_l, z_s, R_E, f*_c, f*_s, R_E>0",
   "same census as A55/A70; the selection is the file, not a cut made here")

# cosmology used by the SLACS tables themselves (flat LCDM 0.3/0.7/h=0.7)
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


# =====================================================================================
# K3  the SPARC likelihood IS the record's
# =====================================================================================
head("K3  THE LIKELIHOOD IS THE RECORD'S (THEORY sec.4 / A51 K2)")

UG = np.geomspace(0.05, 2.5, 240)          # the record's Upsilon window
FLOOR = 0.10 if MUT == "floor10" else 0.05


def chi2_sparc(a0, gals=None, ug=UG, floor=FLOOR):
    """chi2 = sum (V - Vpred)^2 / (errV^2 + (floor V)^2), one Upsilon per galaxy profiled."""
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
_ch_fix936 = chi2_sparc_fixed(A0_CANON) / NPT
_ch_free = chi2_sparc(1.132e-10) / (NPT - NG)
P("  fixed Upsilon=0.5, a0=1.132e-10 : chi2/dof = %.4f   (record 6.87)" % _ch_fix)
P("  fixed Upsilon=0.5, a0=9.36e-11  : chi2/dof = %.4f   (record 6.63)" % _ch_fix936)
P("  one Upsilon per galaxy, 1.132e-10: chi2/dof = %.4f  (record 2.42)" % _ch_free)
ck("K3", abs(_ch_fix - 6.87) < 0.02 and abs(_ch_fix936 - 6.63) < 0.02 and abs(_ch_free - 2.42) < 0.10,
   "%.4f / %.4f / %.4f" % (_ch_fix, _ch_fix936, _ch_free),
   "6.87+-0.02, 6.63+-0.02, 2.42+-0.10",
   "the zero-parameter chi2/dof reproduces the record to 4 digits, so this is the same likelihood")

# =====================================================================================
# K4  the kappa identity and its two conventions
# =====================================================================================
head("K4  THE KAPPA IDENTITY, IN BOTH CONVENTIONS THE RECORD USES")

k_at_theory = kappa_of_a0(A0_THEORY)
k_de = k_at_theory / math.sqrt(OMEGA_L)
rt = abs(a0_of_kappa(k_at_theory) / A0_THEORY - 1.0)
P("  kappa(1.131204e-10) = %.9f   (target 0.5)" % k_at_theory)
P("  kappa_DE(1.131204e-10) = kappa_P3/sqrt(Omega_L) = %.6f" % k_de)
P("  round trip a0 -> kappa -> a0 residual %.2e" % rt)
P("  kappa(canonical 9.36e-11) = %.6f   <-- the theory's own canonical footing" % KAPPA_CANON)
ck("K4", abs(k_at_theory - 0.5) < 1e-12 and abs(k_de - 0.6043) < 5e-4 and rt < 1e-12,
   "kappa_P3 = %.9f ; kappa_DE = %.6f ; round trip %.1e" % (k_at_theory, k_de, rt),
   "0.5 +- 1e-9 ; 0.6043 +- 5e-4 ; round trip < 1e-12",
   "a0 = kappa c sqrt(G rho_bare); the DE convention is 20.9% larger -- 1/2 in one is 0.604 in the other")

# =====================================================================================
# K5  the SPARC-only fit
# =====================================================================================
head("K5  CHANNEL 1 -- SPARC ALONE: a0, kappa, chi2/dof")

r_sp = minimize_scalar(lambda a: chi2_sparc(a), bounds=(5e-11, 2.5e-10),
                       method="bounded", options=dict(xatol=1e-16))
A0_SP = float(r_sp.x)
K_SP = kappa_of_a0(A0_SP)
CHI2_SP = float(r_sp.fun)
DOF_SP = NPT - NG
A51 = json.load(open(os.path.join(HERE, "..", "A51_kappa_measured", "a51_results.json")))
P("  a0 = %.6e m/s^2   kappa = %.6f   chi2 = %.2f / %d = %.4f"
  % (A0_SP, K_SP, CHI2_SP, DOF_SP, CHI2_SP / DOF_SP))
P("  A51 stored: a0 = %.6e  kappa = %.6f  chi2/dof = %.4f"
  % (A51["sparc"]["a0_best"], A51["sparc"]["kappa"], A51["sparc"]["chi2_dof"]))
ck("K5", abs(A0_SP / A51["sparc"]["a0_best"] - 1) < 2e-4 and abs(K_SP / A51["sparc"]["kappa"] - 1) < 2e-4,
   "a0 %.6e vs %.6e ; kappa %.6f vs %.6f" % (A0_SP, A51["sparc"]["a0_best"], K_SP, A51["sparc"]["kappa"]),
   "agreement to 2e-4 relative on a0 and kappa",
   "two independently written likelihoods land on the same minimum: SPARC peaks 27% below the theory's a0")

# =====================================================================================
# K6  the SPARC error: Delta-chi2=1 is not the truth, the bootstrap is
# =====================================================================================
head("K6  THE SPARC ERROR BAR: formal Delta-chi2=1 vs the block bootstrap")

_lo1d = brentq(lambda a: chi2_sparc(a) - CHI2_SP - 1.0, 3e-11, A0_SP * (1 - 1e-9), xtol=1e-20)
_hi1d = brentq(lambda a: chi2_sparc(a) - CHI2_SP - 1.0, A0_SP * (1 + 1e-9), 3e-10, xtol=1e-20)
SIG_DCHI2 = 0.5 * (_hi1d - _lo1d) / A0_SP   # fractional, Delta-chi2 = 1
rng = np.random.default_rng(20261021)
boot = np.empty(200)
for _k in range(200):
    idx = rng.integers(0, NG, NG)
    gg = [GAL[i] for i in idx]
    boot[_k] = minimize_scalar(lambda a: chi2_sparc(a, gg), bounds=(5e-11, 2.5e-10),
                               method="bounded", options=dict(xatol=1e-16)).x
BOOT_FRAC = float(boot.std(ddof=1) / np.median(boot))
P("  Delta-chi2 = 1 in a0 : %.5f%%   (chi2/dof = %.2f, so this is NOT the truth)" % (100 * SIG_DCHI2, CHI2_SP / DOF_SP))
P("  200-draw block bootstrap: median %.6e, sigma/median = %.6f  (A51: %.6f)"
  % (np.median(boot), BOOT_FRAC, A51["sparc"]["sigma_stat_boot"]))
P("  ratio bootstrap / formal = %.2f" % (BOOT_FRAC / SIG_DCHI2))
ck("K6", abs(BOOT_FRAC / A51["sparc"]["sigma_stat_boot"] - 1) < 1e-4 and BOOT_FRAC / SIG_DCHI2 > 5.0,
   "bootstrap %.6f vs A51 %.6f ; ratio to Delta-chi2 %.1f"
   % (BOOT_FRAC, A51["sparc"]["sigma_stat_boot"], BOOT_FRAC / SIG_DCHI2),
   "bootstrap matches A51 to 1e-4 and is >5x the formal error",
   "the per-galaxy scatter (0.455 dex) makes the formal error wrong by ~8x; the bootstrap is used as sigma(SPARC)")

SIG_K_SP = BOOT_FRAC * K_SP
if MUT == "no_boot":
    SIG_K_SP = SIG_DCHI2 * K_SP          # mutation: use the formal Delta-chi2 = 1 error
# A51's estimator-ensemble half-span, verified at its two chi2 endpoints below
EST_HALF_SPAN = 0.05 if MUT == "est_span" else 0.20838642838788285

# =====================================================================================
# K7  the SLACS model reproduces A55 per lens
# =====================================================================================
head("K7  CHANNEL 2 -- SLACS: the A70 model reproduces A55's 70 per-lens ratios")

B4 = 7.669249934
NU_PS4 = 4.0 * (3.0 - (1.0 - 0.6097 / 4.0 + 0.05463 / 16.0))


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
    """Projected mass inside R for the spherical law g = (gN/2)(1+sqrt(1+4a0/gN))."""
    if R >= rmax:
        return 0.0
    U = math.acosh(max(rmax / R, 1.0 + 1e-9))
    u = GLX * U
    r = R * np.cosh(u)
    gN = G_N * np.asarray(M3Df(r)) / r ** 2
    g = 0.5 * gN * (1.0 + np.sqrt(1.0 + 4.0 * a0 / np.maximum(gN, 1e-300)))
    return R * R / G_N * float(np.sum(GLW * g) * U)


def predict(d, a0, boost=1.0):
    """Einstein radius (kpc) predicted by the law + the P-scalar phantom + a Sersic n=4 stars."""
    if MUT == "newton":
        a0 = 1e-30
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


RATIOS_A70 = np.array([predict(d, A0_QUOTED) / d["RE"] for d in LENS])
MED50 = float(np.median(RATIOS_A70))
MEANLN50 = float(np.log(RATIOS_A70).mean())
A55 = json.load(open(A55JSON))
_r55 = {x["name"]: x["ratio"] for x in A55["slacs"]["per_lens_salpeter"]}
_names70 = [d["name"] for d in LENS]
_dev = float(np.max(np.abs(np.array([RATIOS_A70[i] / _r55[n] - 1.0 for i, n in enumerate(_names70)]))))
P("  median R_E,pred/R_E,obs = %.6f  (A55 0.8852) ; <ln> = %+.6f (A55 -0.1245)" % (MED50, MEANLN50))
P("  max per-lens deviation from A55's stored ratios: %.2e" % _dev)
ck("K7", abs(MED50 / 0.8852 - 1) < 1e-4 and _dev < 1e-9,
   "median %.6f, max per-lens deviation %.2e" % (MED50, _dev),
   "median 0.8852 +- 1e-4 ; per-lens < 1e-9",
   "the SLACS model here IS A55's/A70's, not a rival re-implementation")

# =====================================================================================
# K8  the required IMF normalisation B, and why A55's 1.283 is wrong
# =====================================================================================
head("K8  THE REQUIRED IMF NORMALISATION B(0.5) AND A55's ARITHMETIC ERROR")

B_INV = 1.0 / MED50
B_INV2 = B_INV ** 2


def med_at_B(B, a0=A0_QUOTED):
    return float(np.median([predict(d, a0, boost=B) / d["RE"] for d in LENS]))


B_REQ = brentq(lambda B: med_at_B(B) - 1.0, 1.02, 5.0, xtol=1e-6)
P("  root-found B (median ratio = 1) at kappa = 0.5 : %.4f" % B_REQ)
P("  1/median = %.4f ; 1/median^2 = %.4f (A55's 1.283) ; B_req/(1/median) = %.4f"
  % (B_INV, B_INV2, B_REQ / B_INV))
ck("K8", abs(B_REQ - 1.1738) < 2e-3 and abs(B_INV2 - 1.2761) < 2e-3 and B_REQ < 0.97 * B_INV2,
   "B_req %.4f ; 1/median %.4f ; 1/median^2 %.4f" % (B_REQ, B_INV, B_INV2),
   "B_req = 1.174 +- 0.002 ; 1/median^2 = 1.276 +- 0.002 ; B_req < 0.97 x 1/median^2",
   "the M/L that zeroes SLACS is 1.174xSalpeter, not A55's 1.283: M2D does not scale as R^2")

# =====================================================================================
# K9  the two responses: B and kappa
# =====================================================================================
head("K9  THE TWO RESPONSES: dlnR/dlnB = 0.7775 vs dlnR/dlnkappa = 0.1205")

_dB = 0.10
_resp = np.array([math.log(predict(d, A0_QUOTED, boost=1.0 + _dB) / predict(d, A0_QUOTED))
                  for d in LENS])
RESP = float(np.median(_resp)) / math.log(1.0 + _dB)
RESP_SCATTER = float(_resp.std(ddof=1)) / math.log(1.0 + _dB)
B_FROM_RESP = math.exp(-MEANLN50 / RESP)
P("  dlnR/dlnB = %.4f (per-lens median, scatter %.4f) ; response route B = exp(%.4f/%.4f) = %.4f"
  % (RESP, RESP_SCATTER, -MEANLN50, RESP, B_FROM_RESP))
_kk = [0.35, 0.5, 0.7]
_med_k = [float(np.median([predict(d, a0_of_kappa(k)) / d["RE"] for d in LENS])) for k in _kk]
_h = 1e-3
_dlnR_dlnk = (math.log(float(np.median([predict(d, a0_of_kappa(0.5 * math.exp(_h))) / d["RE"] for d in LENS])))
              - math.log(float(np.median([predict(d, a0_of_kappa(0.5 * math.exp(-_h))) / d["RE"] for d in LENS])))) / (2 * _h)
P("  median ratio at kappa = 0.35 / 0.50 / 0.70 : %.4f / %.4f / %.4f"
  % tuple(_med_k))
P("  dlnR/dlnkappa = %.4f ; response ratio dlnR/dlnB : dlnR/dlnkappa = %.2f : 1"
  % (_dlnR_dlnk, RESP / max(abs(_dlnR_dlnk), 1e-12)))
ck("K9", abs(RESP - 0.7775) < 5e-3 and abs(B_FROM_RESP / B_REQ - 1) < 2e-3
   and abs(_dlnR_dlnk - 0.1205) < 5e-3 and 6.0 < RESP / max(abs(_dlnR_dlnk), 1e-12) < 7.0,
   "dlnR/dlnB %.4f ; B_response %.4f vs B_root %.4f ; dlnR/dlnkappa %.4f ; ratio %.2f"
   % (RESP, B_FROM_RESP, B_REQ, _dlnR_dlnk, RESP / max(abs(_dlnR_dlnk), 1e-12)),
   "0.7775 +- 0.005 ; B_response == B_root to 2e-3 ; 0.1205 +- 0.005 ; ratio in [6,7]",
   "lensing is 6.5x more sensitive to the IMF than to a0: it is a mass-normalisation measurement")

# =====================================================================================
# K10  kappa with Salpeter fixed, and the sigma that comes with it
# =====================================================================================
head("K10  WITH SALPETER FIXED, LENSING 'PREFERS' kappa* = 1.03 -- AND WHY THAT IS NOT A kappa MEASUREMENT")

try:
    KSTAR = brentq(lambda k: float(np.median([predict(d, a0_of_kappa(k)) / d["RE"] for d in LENS])) - 1.0,
                   0.6, 3.0, xtol=1e-6)
except ValueError:
    KSTAR = float("nan")      # the model has no kappa dependence at all: report nan, let the check fail
_s_tot = math.sqrt(0.045 ** 2 + 0.09 ** 2)
_ks = np.linspace(0.75, 1.25, 6) * KSTAR
try:
    _c2 = np.array([float(np.sum((np.log(np.array([predict(d, a0_of_kappa(k)) / d["RE"] for d in LENS]))
                                  / LN10 / _s_tot) ** 2)) for k in _ks])
    _cf = np.polyfit(_ks, _c2, 2)
    SIG_K_SALP = math.sqrt(1.0 / _cf[0])
except Exception:
    SIG_K_SALP = float("nan")
P("  kappa* (median ratio = 1, B = 1) = %.4f   (A70: 1.0279)" % KSTAR)
P("  Delta-chi2 = 1 width from the full per-lens likelihood: %.4f ; (kappa*-%.4f)/sigma = %.2f"
  % (SIG_K_SALP, K_SP, (KSTAR - K_SP) / SIG_K_SALP))
ck("K10", abs(KSTAR - 1.0279) < 0.01 and 0.09 < SIG_K_SALP < 0.17,
   "kappa* %.4f, sigma %.4f, apparent tension %.1f sigma"
   % (KSTAR, SIG_K_SALP, (KSTAR - K_SP) / SIG_K_SALP),
   "kappa* = 1.0279 +- 0.01 ; 0.09 < sigma < 0.17",
   "the 6-sigma 'lensing failure' exists ONLY with Salpeter pinned; dlnR/dlnkappa = 0.12 makes it an M/L statement")

# =====================================================================================
# K11  sigma(log B) two routes, and the free-IMF flatness
# =====================================================================================
head("K11  sigma(log10 B) FROM TWO ROUTES, AND THE FREE-IMF FLATNESS")

SIG_LOGB_DEX = (float(np.log(RATIOS_A70).std(ddof=1)) / math.sqrt(NL) / LN10) / RESP
SIG_LOGB_CURV = ((0.045 if MUT == "err045" else _s_tot) / (RESP * math.sqrt(NL)))
P("  mean/SEM route  : scatter %.4f dex / sqrt(%d) / %.4f = %.4f dex"
  % (float(np.log(RATIOS_A70).std(ddof=1)) / LN10, NL, RESP, SIG_LOGB_DEX))
P("  chi2 curvature  : s/(dlnR/dlnB sqrt(N)) = %.4f/(%.4f*%.3f) = %.4f dex"
  % (_s_tot, RESP, math.sqrt(NL), SIG_LOGB_CURV))
P("  two routes agree to %.1f%%" % (100 * (SIG_LOGB_CURV / SIG_LOGB_DEX - 1)))
# the mean-only and scatter-only chi2 profiles
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
S_LN = (0.045 if MUT == "err045" else _s_tot) * LN10   # per-lens sigma in ln
CHI2_SHAPE = NL * (SD_TAB ** 2) / S_LN ** 2
_kb = np.linspace(math.log(0.20), math.log(0.80), 61)
_cb = NL * (SPL_S(_kb) ** 2) / S_LN ** 2
D_SHAPE = float(_cb.max() - _cb.min())                                  # over kappa in [0.20,0.80]
D_SHAPE_FULL = float(CHI2_SHAPE.max() - CHI2_SHAPE.min())               # over the whole grid
D_MEAN = 0.0                              # zero by construction: B is profiled per kappa
P("  mean-only chi2 over kappa in [0.2,0.8]: Delta-chi2 = %.2e (B profiled -> exactly flat)" % D_MEAN)
P("  scatter term NL*sd^2/s^2 over the same band: %.2f -> %.2f, Delta-chi2 = %.2f"
  % (_cb.max(), _cb.min(), D_SHAPE))
P("  (over the whole grid kappa in [0.2,1.7] the scatter term runs %.2f -> %.2f, Delta-chi2 = %.2f)"
  % (CHI2_SHAPE.max(), CHI2_SHAPE.min(), D_SHAPE_FULL))
ck("K11", abs(SIG_LOGB_DEX - 0.0143) < 5e-4 and abs(SIG_LOGB_CURV / SIG_LOGB_DEX - 1) < 0.12,
   "%.4f dex (mean/SEM) vs %.4f dex (curvature)" % (SIG_LOGB_DEX, SIG_LOGB_CURV),
   "0.0143 +- 0.0005 ; two routes within 12%",
   "70 SLACS lenses measure the IMF normalisation to 3.3% -- the sharpest number in the lensing channel")

# =====================================================================================
# K12  the Treu+2010 prior
# =====================================================================================
head("K12  THE IMF PRIOR: Treu+2010's dynamical calibration of the same lenses")

_tl = [l.rstrip("\n") for l in open(DATA_TREU, encoding="latin-1")]
_ti = [i for i, l in enumerate(_tl) if l.startswith("name")][0]
_th = _tl[_ti].split("\t")
_ic = {c: i for i, c in enumerate(_th)}
_tr = [l.split("\t") for l in _tl[_ti + 1:] if l.strip() and not l.startswith("#")]
ALPHA = np.array([float(r[_ic["log_alpha"]]) for r in _tr if len(r) == len(_th)])
if MUT == "treu":
    ALPHA = ALPHA + 0.10
TREU_MEAN = float(ALPHA.mean())
TREU_SEM = float(ALPHA.std(ddof=1) / math.sqrt(len(ALPHA)))
TREU_95HI = 10 ** (1.96 * math.sqrt(0.03 ** 2 + 0.02 ** 2))
TREU_95LO = 10 ** (-1.96 * math.sqrt(0.03 ** 2 + 0.02 ** 2))
P("  N = %d lenses, <log10 alpha_Salp> = %+.4f +- %.4f (sem), scatter %.4f dex"
  % (len(ALPHA), TREU_MEAN, TREU_SEM, float(ALPHA.std(ddof=1))))
P("  abstract: 0.00 +- 0.03 (stat) +- 0.02 (sys) -> 95%% on the mean = [%.3f, %.3f] x Salpeter"
  % (TREU_95LO, TREU_95HI))
ck("K12", len(ALPHA) == 56 and abs(TREU_MEAN) < 0.02 and abs(TREU_95HI - 1.177) < 2e-3,
   "N=%d, mean %+.4f, 95%% hi %.4f" % (len(ALPHA), TREU_MEAN, TREU_95HI),
   "56 lenses, |mean| < 0.02, 95% upper = 1.177 +- 0.002",
   "the prior is B = 1.00 with sigma = 0.036 dex, and 95% = [0.850, 1.177] -- B=1.174 sits ON the boundary")

SIG_B_PRIOR_DEX = 0.036
SIG_B_MEAS_DEX = SIG_LOGB_DEX                 # 0.0143
if MUT == "imf_prior":
    SIG_B_PRIOR_DEX = 0.100                    # mutation: use the cross-method spread
SIG_B_PULL_DEX = math.sqrt(SIG_B_PRIOR_DEX ** 2 + SIG_B_MEAS_DEX ** 2)
SIG_B_PRIOR = SIG_B_PRIOR_DEX * LN10
SIG_B_MEAS = SIG_B_MEAS_DEX * LN10

# =====================================================================================
# K13  the cluster anchor
# =====================================================================================
head("K13  CHANNEL 3 -- CLUSTERS: A18's machinery and anchor")


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


R_CAN, RV_CAN, F_CAN = R_tot(A0_CANON)
P("  r_v = %.4f Mpc ; F(y_v) = %.4f ; R_tot = %.4f   (A18: 1.6863 / 3.7702 / 2.6179)"
  % (RV_CAN / MPC, F_CAN, R_CAN))
ck("K13", abs(RV_CAN / MPC - 1.6863) < 1e-3 and abs(F_CAN - 3.7702) < 1e-3 and abs(R_CAN - 2.6179) < 1e-3,
   "%.4f Mpc / %.4f / %.4f" % (RV_CAN / MPC, F_CAN, R_CAN),
   "1.6863 +- 0.001 / 3.7702 +- 0.001 / 2.6179 +- 0.001",
   "A18's anchor is reproduced by this implementation before it is used as a constraint")

# =====================================================================================
# K14  the cluster channel alone
# =====================================================================================
head("K14  THE CLUSTER CHANNEL ALONE: kappa = 0.393 +- 0.043, circular in u")

_hh = 1e-3
DLNR = (math.log(R_tot(A0_CANON * (1 + _hh))[0]) - math.log(R_tot(A0_CANON * (1 - _hh))[0])) / (2 * _hh)
R_REQ, SIG_R = 5.552, 0.427
U0, SIG_U = 0.45, 0.03
if MUT == "u_prior":
    SIG_U = 1.0                                # mutation: drop the sourcing-fraction prior
SIG_CL = (math.sqrt((SIG_R / R_REQ) ** 2 + (SIG_U / U0) ** 2)) / abs(DLNR)
K_CL = KAPPA_CANON * (U0 * R_REQ / R_CAN) ** (1.0 / DLNR)
P("  dlnR_tot/dlna0 = %+.4f" % DLNR)
P("  cluster-only kappa = %.4f +- %.4f (%.1f%%)   (A51: 0.3934 +- 0.0432)"
  % (K_CL, K_CL * SIG_CL, 100 * SIG_CL))
ck("K14", abs(K_CL - 0.3934) < 2e-3 and abs(SIG_CL - 0.1097) < 3e-3,
   "kappa %.4f +- %.4f (sigma/kappa %.4f)" % (K_CL, K_CL * SIG_CL, SIG_CL),
   "0.3934 +- 0.002, sigma/kappa 0.1097 +- 0.003",
   "u was fitted by A18 to the same amplitudes, so this is an 11% consistency band, not an independent measurement")

SIG_K_CL = K_CL * SIG_CL

# =====================================================================================
# K15/K16  the closure is an identity
# =====================================================================================
head("K15  THE CLOSURE I(y_t) = 8 pi / kappa^2 -- AN IDENTITY, NOT A CONSTRAINT")


def hfun(y):
    return 0.5 * (math.sqrt(y * y + 4.0 * y) - y)


def F_closure(Y):
    """F(Y) = int_0^inf h(y)/(1+(y/Y)^2) dy,  y = Y tan(theta)."""
    g = lambda th: hfun(Y * math.tan(th)) * Y * (1.001 if MUT == "closure_kernel" else 1.0)
    val, _ = quad(g, 0.0, math.pi / 2.0, limit=400)
    return val


N_LAMBDA = LAMBDA_OBS * C_L ** 4 / A0_CANON ** 2
KAPPA_LAMBDA = math.sqrt((8.0 * math.pi if MUT != "closure_4pi" else 4.0 * math.pi) / N_LAMBDA)
YT_OBS = brentq(lambda Y: F_closure(Y) - N_LAMBDA, 10.0, 200.0, xtol=1e-10)
YT_HALF = brentq(lambda Y: F_closure(Y) - 8.0 * math.pi / 0.25, 10.0, 200.0, xtol=1e-10)
P("  N_Lambda = Lambda c^4 / a0^2 = %.6f   (Lambda = %.4e m^-2, a0 = %.3e)"
  % (N_LAMBDA, LAMBDA_OBS, A0_CANON))
P("  root of F(y_t) = N_Lambda : y_t = %.6f   (A28: 66.299937)" % YT_OBS)
P("  root of F(y_t) = 8 pi/(1/2)^2 = 32 pi = %.6f : y_t = %.6f   (A28: 66.380331)"
  % (32 * math.pi, YT_HALF))
P("  kappa implied by (Lambda, a0): %.6f   (A28: 0.500311)" % KAPPA_LAMBDA)
ck("K15", abs(YT_OBS - 66.29994) < 2e-3 and abs(YT_HALF - 66.38033) < 2e-3 and abs(KAPPA_LAMBDA - 0.500311) < 1e-4,
   "y_t %.5f (obs) / %.5f (1/2) / kappa %.6f" % (YT_OBS, YT_HALF, KAPPA_LAMBDA),
   "66.29994 +- 0.002 ; 66.38033 +- 0.002 ; 0.500311 +- 1e-4",
   "the closure reproduces A28's numbers to 1e-4 -- and it is the definition of kappa rewritten")

head("K16  WHY THE CLOSURE CANNOT BE COUNTED AS DATA")


def F_closure_exact(Y):
    """A28 eq. (5): F(Y) = Y^2 int_0^2 v^2(4-v)/[4Y^2(2-v)^2+v^4] dv,  v = sqrt(y^2+4y)-y."""
    g = lambda v: Y * Y * v * v * (4.0 - v) / (4.0 * Y * Y * (2.0 - v) ** 2 + v ** 4)
    val, _ = quad(g, 0.0, 2.0, limit=400)
    return val


_yt_q = brentq(lambda Y: F_closure(Y) - 8.0 * math.pi / 0.25, 10.0, 200.0, xtol=1e-12)
_yt_e = brentq(lambda Y: F_closure_exact(Y) - 8.0 * math.pi / 0.25, 10.0, 200.0, xtol=1e-12)
P("  two independent formulations of the same integral at kappa = 1/2:")
P("    tan-substitution quadrature : y_t = %.9f" % _yt_q)
P("    A28 eq.(5) rational integral: y_t = %.9f   (difference %.2e)" % (_yt_e, abs(_yt_q - _yt_e)))
_agree = abs(_yt_q - _yt_e) / _yt_q
COEF_CLOSURE = 8.0 * math.pi if MUT != "closure_4pi" else 4.0 * math.pi
_res = []
for k in (0.25, 0.3415, 0.371, 0.5, 0.5265, 0.8):
    target = COEF_CLOSURE / k ** 2
    Y = brentq(lambda Y: F_closure(Y) - target, 10.0, 300.0, xtol=1e-10)
    _res.append((k, Y, F_closure(Y) - target))
P("  kappa    y_t        residual F(y_t) - 8pi/kappa^2")
for k, Y, rr in _res:
    P("  %.4f  %9.5f   %+.3e" % (k, Y, rr))
_maxres = max(abs(r[2]) for r in _res)
_hE = 1e-4
_yt_hi = brentq(lambda Y: F_closure(Y) - COEF_CLOSURE / (0.5 * (1 + _hE)) ** 2, 10.0, 200.0, xtol=1e-12)
_yt_lo = brentq(lambda Y: F_closure(Y) - COEF_CLOSURE / (0.5 * (1 - _hE)) ** 2, 10.0, 200.0, xtol=1e-12)
_elast = (math.log(_yt_hi) - math.log(_yt_lo)) / (math.log(1 + _hE) - math.log(1 - _hE))
P("  max |residual| over six kappa: %.2e  -> the closure is satisfied identically, for every kappa" % _maxres)
P("  dln y_t/dln kappa = %+.4f (A28: -1.946912): y_t is a FUNCTION of kappa, not a measurement of it" % _elast)
ck("K16", _maxres < 1e-8 and abs(_elast + 1.9469) < 5e-3 and _agree < 1e-9,
   "max residual %.1e ; dln y_t/dln kappa %.4f ; two formulations agree to %.1e" % (_maxres, _elast, _agree),
   "residual < 1e-8 for every kappa ; elasticity -1.9469 +- 0.005 ; formulations agree to 1e-9",
   "counting it as data would add a zero-variance constraint on a derived quantity: it is EXCLUDED")

# =====================================================================================
# K17  BAO/SNe/CMB are kappa-blind
# =====================================================================================
head("K17  BAO + SNe + CMB: VERIFIED kappa-BLIND, THEN EXCLUDED")

OM_FW = 0.4376                                  # any Omega_m; the identity is what is tested
_r = 0.0001


def E_fw(z, om=OM_FW, k=None):
    k = KAPPA_CANON if k is None else k
    e = math.sqrt((1.0 + om * (1.0 + z) ** 3) / (1.0 + om))
    if MUT == "kappa_in_E":                     # mutation: put a kappa factor in the background
        e *= (1.0 + 0.1 * k)
    return e


def E_lcdm(z, om):
    return math.sqrt(om * (1.0 + z) ** 3 + (1.0 - om))


_zs = np.linspace(0.05, 2.5, 40)
_dk = max(abs(E_fw(z, k=0.20) / E_fw(z, k=1.00) - 1.0) for z in _zs)
_om_eff = OM_FW / (1.0 + OM_FW)
_rep = max(abs(E_fw(z) / E_lcdm(z, _om_eff) - 1.0) for z in _zs)
P("  max |E(z; kappa=0.20)/E(z; kappa=1.00) - 1| over z in [0.05, 2.5] : %.2e" % _dk)
P("  max |E_fw(z; Om) / E_LCDM(z; Om/(1+Om)) - 1|                       : %.2e" % _rep)
ck("K17", _dk < 1e-14 and _rep < 1e-12,
   "kappa-blind to %.1e ; reparametrisation exact to %.1e" % (_dk, _rep),
   "< 1e-14 and < 1e-12",
   "a0 does not enter E(z) at all; the framework background IS flat LCDM relabelled, so the "
   "distance vector supplies neither kappa nor an independent H0 -> EXCLUDED (both directions)")

# =====================================================================================
# K18  THE JOINT FIT
# =====================================================================================
head("K18  THE JOINT FIT: (kappa, B, u) AGAINST SPARC + SLACS + CLUSTERS")

KSPP = np.linspace(0.20, 0.80, 31)
CHI2_SP_TAB = np.array([chi2_sparc(a0_of_kappa(k)) for k in KSPP])
SPL_CHI2_SP = CubicSpline(np.log(KSPP), CHI2_SP_TAB)
_chi_at_min = float(SPL_CHI2_SP(math.log(K_SP)))
P("  SPARC chi2 grid: minimum %.3f at the grid point kappa %.4f ; direct fit %.3f at kappa %.4f"
  % (float(CHI2_SP_TAB.min()), KSPP[int(np.argmin(CHI2_SP_TAB))], CHI2_SP, K_SP))
P("  spline at the direct minimum: %.3f (grid resolution %.3f)" % (_chi_at_min, _chi_at_min - CHI2_SP))


def lnB_req(k):
    """The B that zeroes the SLACS mean residual at kappa, from the 70-lens model."""
    return -float(SPL_M(math.log(k))) / RESP


def chi2_cluster(k, u):
    Rt = R_tot(a0_of_kappa(k))[0]
    return ((Rt / u - R_REQ) / SIG_R) ** 2 + ((u - U0) / SIG_U) ** 2


def u_best(k):
    return minimize_scalar(lambda u: chi2_cluster(k, u), bounds=(0.30, 0.70), method="bounded",
                           options=dict(xatol=1e-10)).x


def chi2_profile_k(k, sparc_sigma=None, use_slacs=True, use_cluster=True):
    """chi2 minimised over B analytically and over u numerically, as a function of kappa."""
    s = SIG_K_SP if sparc_sigma is None else sparc_sigma
    c = ((k - K_SP) / s) ** 2
    if use_slacs:
        L = lnB_req(k)
        c += L * L / (SIG_B_MEAS ** 2 + SIG_B_PRIOR ** 2)
    if use_cluster:
        c += chi2_cluster(k, u_best(k))
    return c


def B_at(k):
    L = lnB_req(k)
    if MUT == "b_marg":
        return math.exp(L)                   # mutation: B at the lensing value, prior not marginalised
    return math.exp(L * SIG_B_PRIOR ** 2 / (SIG_B_MEAS ** 2 + SIG_B_PRIOR ** 2))


r_j = minimize_scalar(lambda lk: chi2_profile_k(math.exp(lk)), bounds=(math.log(0.20), math.log(0.80)),
                      method="bounded", options=dict(xatol=1e-12))
K_JOINT = float(math.exp(r_j.x))
CHI2_JOINT_PROF = float(r_j.fun)
U_JOINT = u_best(K_JOINT)
B_JOINT = B_at(K_JOINT)
CHI2_SP_JOINT = ((K_JOINT - K_SP) / SIG_K_SP) ** 2
CHI2_SL_JOINT = (math.log(B_JOINT) - lnB_req(K_JOINT)) ** 2 / SIG_B_MEAS ** 2
CHI2_PR_JOINT = math.log(B_JOINT) ** 2 / SIG_B_PRIOR ** 2
CHI2_CL_JOINT = chi2_cluster(K_JOINT, U_JOINT)
CHI2_TOT = CHI2_SP_JOINT + CHI2_SL_JOINT + CHI2_CL_JOINT + CHI2_PR_JOINT
P("  kappa   = %.5f   a0 = %.5e m/s^2  (%.1f%% below canonical, %.1f%% below the kappa=1/2 footing)"
  % (K_JOINT, a0_of_kappa(K_JOINT), 100 * (1 - K_JOINT / KAPPA_CANON), 100 * (1 - K_JOINT / 0.5)))
P("  B       = %.5f  (log10 B = %+.5f dex)" % (B_JOINT, math.log10(B_JOINT)))
P("  u       = %.5f" % U_JOINT)
P("  chi2 = %.4f = SPARC %.3f + SLACS %.3f + cluster %.3f + IMF prior %.3f"
  % (CHI2_TOT, CHI2_SP_JOINT, CHI2_SL_JOINT, CHI2_CL_JOINT, CHI2_PR_JOINT))
P("  B_req(kappa_joint) = %.4f ; B_joint is the prior-weighted mean of that and 1.00"
  % math.exp(lnB_req(K_JOINT)))
# independent cross-check: brute-force 2D Nelder-Mead on (lnk, lnB, u)
_r2 = minimize(lambda p: ((math.exp(p[0]) - K_SP) / SIG_K_SP) ** 2
               + (p[1] - lnB_req(math.exp(p[0]))) ** 2 / SIG_B_MEAS ** 2
               + p[1] ** 2 / SIG_B_PRIOR ** 2
               + chi2_cluster(math.exp(p[0]), p[2]),
               [math.log(K_JOINT) + 0.02, math.log(1.2), 0.5], method="Nelder-Mead",
               options=dict(xatol=1e-12, fatol=1e-12, maxiter=20000))
K_NM = float(math.exp(_r2.x[0]))
B_NM = float(math.exp(_r2.x[1]))
U_NM = float(_r2.x[2])
# per-channel chi2/dof at the joint best fit (raw likelihoods, not the compressed forms)
_m_joint = math.log(B_JOINT) - lnB_req(K_JOINT)
_sd_joint = float(SPL_S(math.log(K_JOINT)))
CHI2_SL_RAW = NL * (_sd_joint ** 2 + _m_joint ** 2) / S_LN ** 2
CHI2_SP_RAW = float(SPL_CHI2_SP(math.log(K_JOINT)))
P("  per-channel chi2/dof AT THE JOINT BEST FIT:")
P("    SPARC   raw chi2 %.2f / %d dof = %.4f   (compressed %.3f / 1 dof)"
  % (CHI2_SP_RAW, DOF_SP, CHI2_SP_RAW / DOF_SP, CHI2_SP_JOINT))
P("    SLACS   raw chi2 %.2f / %d dof = %.4f   (compressed %.3f / 1 dof)"
  % (CHI2_SL_RAW, NL - 2, CHI2_SL_RAW / (NL - 2), CHI2_SL_JOINT))
P("    cluster raw chi2 %.3f / 1 dof            (compressed %.3f / 1 dof)"
  % (CHI2_CL_JOINT - (U_JOINT - U0) ** 2 / SIG_U ** 2, CHI2_CL_JOINT))
P("    SLACS residual at the joint: ln B - ln B_req = %+.4f (%.2f sigma of the lensing error)"
  % (_m_joint, _m_joint / SIG_B_MEAS))
P("  independent 3-parameter Nelder-Mead: kappa %.6f  B %.6f  u %.6f  chi2 %.5f"
  % (K_NM, B_NM, U_NM, _r2.fun))
ck("K18", abs(K_NM / K_JOINT - 1) < 1e-5 and abs(B_NM / B_JOINT - 1) < 1e-5 and abs(_r2.fun - CHI2_TOT) < 1e-4,
   "profile %.6f/%.5f/%.5f vs NM %.6f/%.6f/%.6f" % (K_JOINT, B_JOINT, U_JOINT, K_NM, B_NM, U_NM),
   "two independent minimisers agree to 1e-5 in kappa and B",
   "the joint optimum is not an artefact of one minimiser: analytic-profiled and 3-D routes agree")

# =====================================================================================
# K19  the joint kappa vs A51
# =====================================================================================
head("K19  THE JOINT kappa AGAINST A51's 0.3708 +- 0.0265")

_lo1 = brentq(lambda lk: chi2_profile_k(math.exp(lk)) - CHI2_JOINT_PROF - 1.0,
              math.log(0.20), math.log(K_JOINT), xtol=1e-14)
_hi1 = brentq(lambda lk: chi2_profile_k(math.exp(lk)) - CHI2_JOINT_PROF - 1.0,
              math.log(K_JOINT), math.log(0.80), xtol=1e-14)
_lo95 = brentq(lambda lk: chi2_profile_k(math.exp(lk)) - CHI2_JOINT_PROF - 3.8415,
               math.log(0.20), math.log(K_JOINT), xtol=1e-14)
_hi95 = brentq(lambda lk: chi2_profile_k(math.exp(lk)) - CHI2_JOINT_PROF - 3.8415,
               math.log(K_JOINT), math.log(0.80), xtol=1e-14)
SIG_K_JOINT = 0.5 * (math.exp(_hi1) - math.exp(_lo1))
P("  joint kappa = %.5f +- %.5f (stat, Delta-chi2=1)" % (K_JOINT, SIG_K_JOINT))
P("  95%% statistical: [%.5f, %.5f]" % (math.exp(_lo95), math.exp(_hi95)))
P("  A51 (SPARC + clusters, no SLACS): %.5f +- %.5f" % (A51["joint"]["kappa"], A51["joint"]["sigma_stat"]))
P("  shift from adding SLACS: %+.5f (%.2f sigma of the joint)" % (K_JOINT - A51["joint"]["kappa"],
                                                                 (K_JOINT - A51["joint"]["kappa"]) / SIG_K_JOINT))
_chi_noslac = minimize_scalar(lambda lk: chi2_profile_k(math.exp(lk), use_slacs=False),
                              bounds=(math.log(0.2), math.log(0.8)), method="bounded").x
K_NOSLAC = float(math.exp(_chi_noslac))
P("  joint WITHOUT the SLACS channel: kappa = %.5f  (SLACS moves kappa by %.5f)" % (K_NOSLAC, K_JOINT - K_NOSLAC))
ck("K19", abs(K_JOINT / A51["joint"]["kappa"] - 1) < 0.02 and abs(SIG_K_JOINT / A51["joint"]["sigma_stat"] - 1) < 0.05,
   "kappa %.5f +- %.5f vs A51 %.5f +- %.5f" % (K_JOINT, SIG_K_JOINT, A51["joint"]["kappa"], A51["joint"]["sigma_stat"]),
   "agreement to 2% in the mean and 5% in sigma",
   "adding the corrected SLACS likelihood to A51's three channels moves kappa by <1%: SLACS carries no kappa weight")

# =====================================================================================
# K20  the pulls
# =====================================================================================
head("K20  THE PULLS: (channel best fit - joint) / channel sigma")

# each channel's own best fit
K_SP_CH = K_SP
SIG_SP_CH = SIG_K_SP
r_cl = minimize_scalar(lambda lk: chi2_cluster(math.exp(lk), u_best(math.exp(lk))),
                       bounds=(math.log(0.2), math.log(0.8)), method="bounded")
K_CL_ONLY = float(math.exp(r_cl.x))
SIG_CL_ONLY = 0.5 * (brentq(lambda k: chi2_cluster(k, u_best(k)) - r_cl.fun - 1.0, K_CL_ONLY, 0.8) -
                     brentq(lambda k: chi2_cluster(k, u_best(k)) - r_cl.fun - 1.0, 0.2, K_CL_ONLY))
r_sl = minimize(lambda p: (p[1] - lnB_req(math.exp(p[0]))) ** 2 / SIG_B_MEAS ** 2 + p[1] ** 2 / SIG_B_PRIOR ** 2,
                [math.log(1.2), math.log(1.0)], method="Nelder-Mead", options=dict(xatol=1e-12, fatol=1e-12))
K_SL_ONLY = float(math.exp(r_sl.x[0]))
B_SL_ONLY = float(math.exp(r_sl.x[1]))
_chi_sl_min = float(r_sl.fun)
# sigma(kappa) from the SLACS channel alone (B profiled): the ridge width at Delta-chi2 = 1
def _chi_sl(k):
    return (lnB_req(k) ** 2) / (SIG_B_MEAS ** 2 + SIG_B_PRIOR ** 2)
try:
    _lo_sl = brentq(lambda k: _chi_sl(k) - _chi_sl_min - 1.0, 0.20, K_SL_ONLY, xtol=1e-12)
    _hi_sl = brentq(lambda k: _chi_sl(k) - _chi_sl_min - 1.0, K_SL_ONLY, 3.0, xtol=1e-12)
except ValueError:
    _lo_sl, _hi_sl = float("nan"), float("nan")
SIG_SL_ONLY = 0.5 * (_hi_sl - _lo_sl)
P("  SPARC   : kappa %.5f +- %.5f   pull %+.2f sigma" % (K_SP_CH, SIG_SP_CH, (K_SP_CH - K_JOINT) / SIG_SP_CH))
P("  clusters: kappa %.5f +- %.5f   pull %+.2f sigma" % (K_CL_ONLY, SIG_CL_ONLY, (K_CL_ONLY - K_JOINT) / SIG_CL_ONLY))
P("  SLACS   : kappa %.4f +- %.4f    pull %+.2f sigma  (kappa direction)"
  % (K_SL_ONLY, SIG_SL_ONLY, (K_SL_ONLY - K_JOINT) / SIG_SL_ONLY))
P("  SLACS   : the ridge runs kappa in [%.2f, %.2f] at Delta-chi2 = 1 -> dlnR/dlnkappa = %.3f makes" % (_lo_sl, _hi_sl, _dlnR_dlnk))
P("            it a 1/%.1f measurement of what it measures directly (B)" % (RESP / max(abs(_dlnR_dlnk), 1e-12)))
P("  SLACS   : B %.4f  ->  in the joint B = %.4f" % (B_SL_ONLY, B_JOINT))
PULL_B = math.log10(B_JOINT) / SIG_B_PULL_DEX
P("  IMF     : log10(B_joint) = %+.5f dex ; sigma(pull) = sqrt(%.3f^2 + %.4f^2) = %.4f dex"
  % (math.log10(B_JOINT), SIG_B_PRIOR_DEX, SIG_B_MEAS_DEX, SIG_B_PULL_DEX))
P("            pull on the IMF normalisation = %+.2f sigma ; 95%% upper bound 1.177 -> B_joint %s"
  % (PULL_B, "OUTSIDE" if B_JOINT > TREU_95HI else "inside"))
ck("K20", abs((K_SP_CH - K_JOINT) / SIG_SP_CH) < 2.0 and abs((K_CL_ONLY - K_JOINT) / SIG_CL_ONLY) < 2.0
   and abs((K_SL_ONLY - K_JOINT) / SIG_SL_ONLY) < 2.5 and 1.5 < abs(PULL_B) < 2.5,
   "SPARC %+.2f, clusters %+.2f, SLACS(kappa) %+.2f, IMF %+.2f sigma"
   % ((K_SP_CH - K_JOINT) / SIG_SP_CH, (K_CL_ONLY - K_JOINT) / SIG_CL_ONLY,
      (K_SL_ONLY - K_JOINT) / SIG_SL_ONLY, PULL_B),
   "kappa channels within 2.5 sigma; |IMF pull| in [1.5, 2.5]",
   "no channel is pulled in kappa; the pull is in the mass normalisation B")

# =====================================================================================
# K21  the global tension
# =====================================================================================
head("K21  THE GLOBAL TENSION: chi2_joint - sum of the individual best fits")

CHI2_SUM_MIN = 0.0 + _chi_sl_min + 0.0
TENSION = CHI2_TOT - CHI2_SUM_MIN
NDOF_SHARED = 2
from scipy.stats import chi2 as chi2dist
P_TENSION = float(chi2dist.sf(TENSION, NDOF_SHARED))
SIG_TENSION = float(np.sqrt(chi2dist.isf(P_TENSION, 1)))
P("  chi2_joint            = %.4f" % CHI2_TOT)
P("  sum of channel minima = %.4f  (SPARC 0 + SLACS+prior %.4f + clusters 0)" % (CHI2_SUM_MIN, _chi_sl_min))
P("  T = %.4f for %d shared parameters -> p = %.4f (%.2f sigma)" % (TENSION, NDOF_SHARED, P_TENSION, SIG_TENSION))
P("  decomposition: SPARC %.3f, SLACS %.3f, clusters %.3f, IMF prior %.3f"
  % (CHI2_SP_JOINT, CHI2_SL_JOINT, CHI2_CL_JOINT, CHI2_PR_JOINT))
TENSION_NO_PRIOR = CHI2_TOT - CHI2_PR_JOINT - CHI2_SUM_MIN
P("  without the IMF-prior term (i.e. using only the three data channels): T = %.4f" % TENSION_NO_PRIOR)
ck("K21", 3.0 < TENSION < 8.0 and (CHI2_SL_JOINT + CHI2_PR_JOINT) / TENSION > 0.80,
   "T = %.3f (%.2f sigma) ; %.3f of it is the IMF-prior term" % (TENSION, SIG_TENSION, CHI2_PR_JOINT),
   "3 < T < 8 and >80% of it is the SLACS + IMF-prior terms",
   "the global tension is real but small, and it is entirely the mass normalisation, not kappa")

# =====================================================================================
# K22  is kappa = 1/2 inside the joint 95% region?
# =====================================================================================
head("K22  IS THE THEORY'S OWN kappa = 1/2 INSIDE THE JOINT 95% REGION?")

SYS_FRAC = math.sqrt(EST_HALF_SPAN ** 2 + 0.161 ** 2 + 0.125 ** 2 + 0.10 ** 2 + 0.05 ** 2)
SIG_K_TOT = math.sqrt(SIG_K_JOINT ** 2 + (SYS_FRAC * K_JOINT) ** 2)
D_STAT = (0.5 - K_JOINT) / SIG_K_JOINT
D_TOT = (0.5 - K_JOINT) / SIG_K_TOT
LO95_TOT = K_JOINT - 1.96 * SIG_K_TOT
HI95_TOT = K_JOINT + 1.96 * SIG_K_TOT
CHI2_AT_HALF = chi2_profile_k(0.5) - CHI2_JOINT_PROF
CHI2_AT_THEORY = (((0.5 - K_SP) / SIG_K_SP) ** 2 + (0.0 - lnB_req(0.5)) ** 2 / SIG_B_MEAS ** 2
                  + chi2_cluster(0.5, u_best(0.5)))
CHI2_AT_THEORY_SYS = (((0.5 - K_SP) / SIG_K_TOT) ** 2 + (0.0 - lnB_req(0.5)) ** 2 / SIG_B_MEAS ** 2
                      + chi2_cluster(0.5, u_best(0.5)))
P("  systematic floor: estimator %.4f, distance 0.161, H0 0.125, law 0.100, Upsilon 0.050 -> %.4f"
  % (EST_HALF_SPAN, SYS_FRAC))
P("  sigma(kappa) stat = %.5f ; total = %.5f (%.1f%%)" % (SIG_K_JOINT, SIG_K_TOT, 100 * SIG_K_TOT / K_JOINT))
P("  1/2 is %.2f sigma away on the statistical error, %.2f sigma on the total error" % (D_STAT, D_TOT))
P("  joint 95%%: statistical [%.5f, %.5f] ; with the declared floor [%.5f, %.5f]"
  % (math.exp(_lo95), math.exp(_hi95), LO95_TOT, HI95_TOT))
P("  Delta-chi2 of kappa = 1/2 (B profiled, others at their joint values) = %.3f" % CHI2_AT_HALF)
_th_sp = ((0.5 - K_SP) / SIG_K_SP) ** 2
_th_sl = (0.0 - lnB_req(0.5)) ** 2 / SIG_B_MEAS ** 2
_th_cl = chi2_cluster(0.5, u_best(0.5))
P("  the theory's OWN point (kappa, B, u) = (0.5, 1.00, 0.45): Delta-chi2 = %.2f (stat errors)" % CHI2_AT_THEORY)
P("    decomposition: SPARC %.2f + SLACS %.2f + clusters %.2f" % (_th_sp, _th_sl, _th_cl))
P("  the same point with the systematic floor on kappa            : Delta-chi2 = %.2f" % CHI2_AT_THEORY_SYS)
P("  B_joint = %.4f vs the 95%% upper bound %.4f -> %s"
  % (B_JOINT, TREU_95HI, "OUTSIDE" if B_JOINT > TREU_95HI else "inside"))
INSIDE_STAT = (0.5 >= math.exp(_lo95)) and (0.5 <= math.exp(_hi95))
INSIDE_TOT = (0.5 >= LO95_TOT) and (0.5 <= HI95_TOT)
P("  kappa = 1/2 inside the statistical 95%% region: %s ; with the declared floor: %s"
  % (INSIDE_STAT, INSIDE_TOT))
ck("K22", (not INSIDE_STAT) and INSIDE_TOT and D_STAT > 3.5,
   "stat %.2f sigma (inside=%s) ; total %.2f sigma (inside=%s) ; Delta-chi2(1/2) = %.2f"
   % (D_STAT, INSIDE_STAT, D_TOT, INSIDE_TOT, CHI2_AT_HALF),
   "outside the statistical 95% at >3.5 sigma, inside the total 95% at <2 sigma",
   "the answer to 'is 1/2 excluded?' depends entirely on the error model -- exactly A51's lesson, now with SLACS in")

# =====================================================================================
# K26  task 3(a): do SPARC and SLACS agree once the IMF prior is applied?
# =====================================================================================
head("K26  TASK 3(a): SPARC's kappa AND SLACS's B, ONCE THE IMF PRIOR IS APPLIED")

B_AT_SPARC = math.exp(lnB_req(K_SP))
PULL_B_SPARC = math.log10(B_AT_SPARC) / SIG_B_PULL_DEX
try:
    K_FOR_95 = brentq(lambda k: math.exp(lnB_req(k)) - TREU_95HI, 0.30, 3.0, xtol=1e-8)
except ValueError:
    K_FOR_95 = float("nan")
P("  at kappa = 0.5 (P3, a0 = 1.1312e-10): B_req = %.4f = %+.4f dex = %.2f sigma  <- A70's headline, reproduced"
  % (B_REQ, math.log10(B_REQ), math.log10(B_REQ) / SIG_B_PULL_DEX))
P("  at SPARC's kappa = %.4f the SLACS model demands B = %.4f" % (K_SP, B_AT_SPARC))
P("    = %+.4f dex above 1.00 -> %.2f sigma of the combined prior+measurement error (%.4f dex)"
  % (math.log10(B_AT_SPARC), PULL_B_SPARC, SIG_B_PULL_DEX))
P("    and %s Treu's 95%% upper bound 1.177" % ("ABOVE" if B_AT_SPARC > TREU_95HI else "below"))
P("  to bring the required B down to 1.177 the joint fit would need kappa = %.4f," % K_FOR_95)
P("    i.e. %+.1f sigma from the joint kappa %.4f" % ((K_FOR_95 - K_JOINT) / SIG_K_JOINT, K_JOINT))
P("  the kappa channels themselves: SPARC %.4f, clusters %.4f, SLACS ridge %.4f -- all within 2 sigma"
  % (K_SP, K_CL_ONLY, K_SL_ONLY))
ck("K26", 1.8 < PULL_B_SPARC < 3.0 and K_FOR_95 > 0.45 and abs((K_SL_ONLY - K_JOINT) / SIG_SL_ONLY) < 2.5,
   "B_req(kappa_SPARC) = %.4f (%.2f sigma) ; kappa needed for B=1.177: %.3f (+%.1f sigma)"
   % (B_AT_SPARC, PULL_B_SPARC, K_FOR_95, (K_FOR_95 - K_JOINT) / SIG_K_JOINT),
   "1.8 < pull < 3.0 ; kappa needed > 0.45 ; SLACS ridge within 2.5 sigma of the joint",
   "SPARC and SLACS agree in kappa and disagree in B: the residual is an IMF-normalisation statement")

# =====================================================================================
# K28  the joint posterior in the (kappa, B) plane: covariance, correlation, 1 and 2 sigma
# =====================================================================================
head("K28  THE JOINT (kappa, B) POSTERIOR: covariance, correlation, 1-sigma and 2-sigma")


def chi2_kb(lk, lb):
    k = math.exp(lk)
    return (((k - K_SP) / SIG_K_SP) ** 2 + (lb - lnB_req(k)) ** 2 / SIG_B_MEAS ** 2
            + lb ** 2 / SIG_B_PRIOR ** 2 + chi2_cluster(k, u_best(k)))


_x0 = np.array([math.log(K_JOINT), math.log(B_JOINT)])
_hh = 1e-4
_H = np.zeros((2, 2))
for _i in range(2):
    for _j in range(2):
        _ei = np.zeros(2); _ej = np.zeros(2)
        _ei[_i] = _hh; _ej[_j] = _hh
        _H[_i, _j] = (chi2_kb(*(_x0 + _ei + _ej)) - chi2_kb(*(_x0 + _ei - _ej))
                      - chi2_kb(*(_x0 - _ei + _ej)) + chi2_kb(*(_x0 - _ei - _ej))) / (4 * _hh * _hh)
COV = 2.0 * np.linalg.inv(_H)
SIG_LNK = math.sqrt(COV[0, 0])
SIG_LNB = math.sqrt(COV[1, 1])
CORR = COV[0, 1] / math.sqrt(COV[0, 0] * COV[1, 1])
P("  curvature matrix at the joint minimum, in (ln kappa, ln B):")
P("    sigma(ln kappa) = %.5f -> sigma(kappa) = %.5f (profile gave %.5f)"
  % (SIG_LNK, SIG_LNK * K_JOINT, SIG_K_JOINT))
P("    sigma(ln B)     = %.5f -> sigma(B)     = %.5f (%.1f%%)" % (SIG_LNB, SIG_LNB * B_JOINT, 100 * SIG_LNB))
P("    correlation(ln kappa, ln B) = %+.4f" % CORR)
P("  1 sigma (Delta-chi2 = 2.30) ellipse: kappa %.4f-%.4f, B %.4f-%.4f"
  % (K_JOINT * math.exp(-math.sqrt(2.30 * COV[0, 0])), K_JOINT * math.exp(math.sqrt(2.30 * COV[0, 0])),
     B_JOINT * math.exp(-math.sqrt(2.30 * COV[1, 1])), B_JOINT * math.exp(math.sqrt(2.30 * COV[1, 1]))))
P("  2 sigma (Delta-chi2 = 6.17) ellipse: kappa %.4f-%.4f, B %.4f-%.4f"
  % (K_JOINT * math.exp(-math.sqrt(6.17 * COV[0, 0])), K_JOINT * math.exp(math.sqrt(6.17 * COV[0, 0])),
     B_JOINT * math.exp(-math.sqrt(6.17 * COV[1, 1])), B_JOINT * math.exp(math.sqrt(6.17 * COV[1, 1]))))
ck("K28", abs(SIG_LNK * K_JOINT / SIG_K_JOINT - 1) < 0.10 and 0.02 < SIG_LNB < 0.05
   and -0.5 < CORR < -0.05,
   "sigma(kappa) %.5f vs profile %.5f ; sigma(lnB) %.5f ; corr %+.3f"
   % (SIG_LNK * K_JOINT, SIG_K_JOINT, SIG_LNB, CORR),
   "marginal and profile sigma(kappa) agree to 10%; 0.02 < sigma(lnB) < 0.05; corr in [-0.5,-0.05]",
   "the (kappa, B) posterior is a mildly correlated Gaussian; B is the better-measured direction")

# =====================================================================================
# K27  the two kappa conventions: which "1/2" is which a0
# =====================================================================================
head("K27  THE CONVENTION TRAP: kappa = 1/2 IS A DIFFERENT a0 IN THE TWO CONVENTIONS")


def kappa_de_of_a0(a0):
    """kappa with rho_bare = rho_DE (the closure / A28 convention)."""
    return a0 * math.sqrt(8.0 * math.pi) / (C_L * H0_SI * math.sqrt(3.0 * OMEGA_L))


K_DE_CANON = kappa_de_of_a0(A0_CANON)              # should be ~0.5
K_DE_THEORY = kappa_de_of_a0(A0_THEORY)            # 0.6043
K_P3_FROM_LAMBDA = math.sqrt(8.0 * math.pi / N_LAMBDA)   # from the closure normalisation
K_JOINT_DE = K_JOINT / math.sqrt(OMEGA_L)
SIG_K_JOINT_DE = SIG_K_JOINT / math.sqrt(OMEGA_L)
P("  kappa_DE(a0 = 9.36e-11)  = %.6f   (from the definition; the closure gives %.6f)"
  % (K_DE_CANON, K_P3_FROM_LAMBDA))
P("  kappa_P3(a0 = 9.36e-11)  = %.6f   <- the same a0 in A51's convention" % (kappa_of_a0(A0_CANON)))
P("  kappa_DE(a0 = 1.1312e-10) = %.6f ; kappa_P3 = 0.500000" % K_DE_THEORY)
P("  ratio kappa_DE/kappa_P3 = %.4f (= 1/sqrt(Omega_L) = %.4f)" % (K_DE_CANON / kappa_of_a0(A0_CANON), 1 / math.sqrt(OMEGA_L)))
P("")
P("  the joint fit, in both conventions: kappa_P3 = %.4f +- %.4f ; kappa_DE = %.4f +- %.4f"
  % (K_JOINT, SIG_K_JOINT, K_JOINT_DE, SIG_K_JOINT_DE))
P("  distance to a0 = 9.36e-11   : %.2f sigma (stat) in P3, %.2f sigma in DE  <- identical"
  % ((kappa_of_a0(A0_CANON) - K_JOINT) / SIG_K_JOINT, (0.5 - K_JOINT_DE) / SIG_K_JOINT_DE))
P("  distance to a0 = 1.1312e-10 : %.2f sigma (stat) in P3, %.2f sigma in DE  <- identical"
  % ((0.5 - K_JOINT) / SIG_K_JOINT, (K_DE_THEORY - K_JOINT_DE) / SIG_K_JOINT_DE))
P("  -> the task's pairing 'kappa = 1/2 <-> a0 = 9.36e-11' is the rho_DE convention; in A51's")
P("     rho_crit convention that a0 is kappa = %.4f and kappa = 1/2 is a0 = 1.1312e-10." % kappa_of_a0(A0_CANON))
_kde60 = math.sqrt(8.0 * math.pi / F_closure(60.0))
_kde140 = math.sqrt(8.0 * math.pi / F_closure(140.0))
P("  falsifier band y_t in [60,140] -> kappa_DE in [%.4f, %.4f] -> kappa_P3 in [%.4f, %.4f]"
  % (_kde140, _kde60, _kde140 * math.sqrt(OMEGA_L), _kde60 * math.sqrt(OMEGA_L)))
P("  A28's quoted falsifier band [0.3415, 0.5265] is the DE convention: reproduced to %.1e"
  % max(abs(_kde140 / 0.3415 - 1), abs(_kde60 / 0.5265 - 1)))
_d_canon = (kappa_of_a0(A0_CANON) - K_JOINT) / SIG_K_JOINT
SEP_FOOTINGS = (0.5 - kappa_of_a0(A0_CANON)) / SIG_K_JOINT
P("  the two theory footings (a0 = 9.36e-11 and 1.1312e-10) are %.4f apart in kappa_P3,"
  % (0.5 - kappa_of_a0(A0_CANON)))
P("    i.e. %.2f sigma at the joint statistical precision -- the fit separates them" % SEP_FOOTINGS)
ck("K27", abs(K_DE_CANON - 0.5) < 2e-3 and abs(K_P3_FROM_LAMBDA - K_DE_CANON) < 2e-3
   and abs(_d_canon - (0.5 - K_JOINT_DE) / SIG_K_JOINT_DE) < 1e-3 and SEP_FOOTINGS > 3.0,
   "kappa_DE(9.36e-11) = %.5f ; kappa_P3(9.36e-11) = %.5f ; distance %.2f sigma in both" %
   (K_DE_CANON, kappa_of_a0(A0_CANON), _d_canon),
   "the two conventions give 0.500 and 0.414 for the same a0, the same distance to it, and the "
   "footings are >3 sigma apart",
   "a0 = 9.36e-11 is kappa=1/2 in one convention and 0.4137 in the other; every comparison here is "
   "made inside one convention")

# =====================================================================================
# K23  the wide-binary prediction (no data -> not in the likelihood)
# =====================================================================================
head("K23  WIDE BINARIES: A PREDICTION WITH NO DATA -- EXCLUDED FROM THE LIKELIHOOD")

M_WB = 2.0 * MSUN
S_WB = 20.0 * 1000.0 * 1.495978707e11     # 20 kAU in metres


def gamma_wb(k, efe=False):
    y = G_N * M_WB / (S_WB ** 2 * a0_of_kappa(k))
    nu = 0.5 * (1.0 + math.sqrt(1.0 + 4.0 / y))
    if not efe:
        return math.sqrt(nu)
    x_ext = 1.8 * (KAPPA_CANON / k)
    y_ext = x_ext * x_ext / (x_ext + 1.0)
    nu_e = 0.5 * (1.0 + math.sqrt(1.0 + 4.0 / y_ext))
    return 0.947 * math.sqrt(nu_e)     # A24's exact 1.1811 / sqrt(nu(y_ext)) at canonical


G_WB_CANON = gamma_wb(KAPPA_CANON)
G_WB_EFE_CANON = gamma_wb(KAPPA_CANON, efe=True)
_hh = 1e-3
DG_WB = (gamma_wb(KAPPA_CANON * (1 + _hh)) - gamma_wb(KAPPA_CANON * (1 - _hh))) / (2 * _hh * KAPPA_CANON)
DG_WB_EFE = (gamma_wb(KAPPA_CANON * (1 + _hh), True) - gamma_wb(KAPPA_CANON * (1 - _hh), True)) / (2 * _hh * KAPPA_CANON)
P("  EFE-blind, total-mass composition: gamma_v(20 kAU, canonical) = %.4f   (A24: 1.5315)" % G_WB_CANON)
P("  EFE-present (A24's exact 1.1811 rescaled by sqrt(nu(y_ext(kappa)))): %.4f" % G_WB_EFE_CANON)
P("  dgamma_v/dkappa = %+.4f (EFE-blind) / %+.4f (EFE-present)" % (DG_WB, DG_WB_EFE))
P("  A24's frozen resolution sigma_tot = 0.0276 -> a 20 kAU measurement alone gives")
P("    sigma(kappa) = %.3f (EFE-blind) / %.3f (EFE-present)" % (0.0276 / abs(DG_WB), 0.0276 / abs(DG_WB_EFE)))
P("  NO DATA on disk: this is a prediction, so it is NOT in the likelihood.")
ck("K23", abs(G_WB_CANON - 1.5315) < 1e-3 and abs(G_WB_EFE_CANON - 1.1811) < 5e-3 and abs(DG_WB) > 0.1,
   "gamma_v %.4f / %.4f ; dgamma/dkappa %.3f / %.3f" % (G_WB_CANON, G_WB_EFE_CANON, DG_WB, DG_WB_EFE),
   "1.5315 +- 0.001 ; 1.1811 +- 0.005 ; |dgamma/dkappa| > 0.1",
   "the EFE-blind value reproduces A24 exactly; the EFE-present one is a declared rescaling of A24's number")

# =====================================================================================
# K24  the error budget and what the joint fit cannot say
# =====================================================================================
head("K24  THE ERROR BUDGET, THE DEGENERACIES, AND THE ONE MEASUREMENT THAT WOULD TIGHTEN IT")

# verify the estimator-ensemble endpoints from A51 with two independent weightings
_a10 = minimize_scalar(lambda a: chi2_sparc(a, floor=0.10), bounds=(5e-11, 2.5e-10),
                       method="bounded", options=dict(xatol=1e-16)).x
_a03 = minimize_scalar(lambda a: chi2_sparc(a, floor=0.03), bounds=(5e-11, 2.5e-10),
                       method="bounded", options=dict(xatol=1e-16)).x
P("  estimator check: 10%% floor -> a0 %.5e (kappa %.4f) ; 3%% floor -> a0 %.5e (kappa %.4f)"
  % (_a10, kappa_of_a0(_a10), _a03, kappa_of_a0(_a03)))
P("  A51's ensemble at those two settings: 7.3417e-11 / 8.5464e-11")
BUDGET = [("statistical (joint)", SIG_K_JOINT),
          ("estimator/error model", EST_HALF_SPAN * K_JOINT),
          ("distance zero point", 0.161 * K_JOINT),
          ("H0 footing", 0.125 * K_JOINT),
          ("law choice", 0.100 * K_JOINT),
          ("Upsilon window", 0.050 * K_JOINT)]
P("  %-24s %9s %9s" % ("term", "sigma_k", "share"))
for nm, s in BUDGET:
    P("  %-24s %9.5f %9.1f%%" % (nm, s, 100 * s ** 2 / SIG_K_TOT ** 2))
REMOVED = []
for nm, s in BUDGET:
    if nm.startswith("stat"):
        continue
    REMOVED.append((nm, math.sqrt(max(SIG_K_TOT ** 2 - s ** 2, 1e-12))))
REMOVED.sort(key=lambda x: x[1])
P("  removing each term in turn (total sigma_kappa, current %.4f):" % SIG_K_TOT)
for nm, s in REMOVED:
    P("    %-24s -> %.4f  (%.1f%% tighter)" % (nm, s, 100 * (1 - s / SIG_K_TOT)))
BEST_REMOVE, BEST_SIG = REMOVED[0]
# --- what each candidate next measurement would do to sigma(kappa)
# A24: 2,223 pairs in the 18-22 kAU bin give sigma_fit = 0.0699, sigma_tot = 0.0726;
# sigma_sys = 0.020 is irreducible.  sigma_fit scales as 1/sqrt(N).
SIG_FIT_2223, SIG_SYS_WB, SIG_TOT_2223 = 0.0699, 0.020, 0.0726
P("  A24 inputs used below: sigma_fit(2,223 pairs) = %.4f, sigma_sys = %.3f, sigma_tot = %.4f"
  % (SIG_FIT_2223, SIG_SYS_WB, SIG_TOT_2223))
SIG_WB = SIG_TOT_2223 / abs(DG_WB_EFE)                 # one 18-22 kAU bin
SIG_WB_BLIND = SIG_TOT_2223 / abs(DG_WB)
# full 30,000-pair catalogue: sigma_fit(N) = 0.0699 sqrt(2223/N); 7 bins combined
SIG_BIN = math.sqrt((SIG_FIT_2223 * math.sqrt(2223.0 / (30000.0 / 7.0))) ** 2 + SIG_SYS_WB ** 2)
SIG_ALL = SIG_BIN / math.sqrt(7.0)
SIG_WB_FULL = SIG_ALL / abs(DG_WB_EFE)
SIG_1000 = SIG_K_JOINT * math.sqrt(171.0 / 1000.0)
# combine a new independent channel with the joint, keeping the SHARED H0 term
SIG_NOH0 = math.sqrt(max(SIG_K_TOT ** 2 - (0.125 * K_JOINT) ** 2, 0.0))
def after(sig_new):
    return math.sqrt(1.0 / (1.0 / SIG_NOH0 ** 2 + 1.0 / sig_new ** 2) + (0.125 * K_JOINT) ** 2)
SIG_C = 8.33e3                                    # A65's cold-phase width, m/s
LSTAR_CANON = SIG_C ** 2 / A0_CANON / PC
LSTAR_JOINT = SIG_C ** 2 / a0_of_kappa(K_JOINT) / PC
P("  A65 cross-check (not an independent channel -- same SPARC photometry):")
P("    L* = sigma_c^2/a0 = %.3f pc at canonical a0, %.3f pc at the joint a0 (anchor 24.0 pc)"
  % (LSTAR_CANON, LSTAR_JOINT))
P("    the anchor a0 implied by L* = 24.0 pc is %.4e -> kappa = %.4f"
  % (SIG_C ** 2 / (24.0 * PC), kappa_of_a0(SIG_C ** 2 / (24.0 * PC))))
P("  candidates for the next measurement (sigma_kappa, and the joint error afterwards):")
P("    wide binary, one 18-22 kAU bin (2,223 pairs)      %.3f  ->  joint %.4f" % (SIG_WB, after(SIG_WB)))
P("    wide binary, full 30,000-pair catalogue (7 bins)  %.3f  ->  joint %.4f" % (SIG_WB_FULL, after(SIG_WB_FULL)))
SIG_WB_BLIND_FULL = SIG_ALL / abs(DG_WB)
SIG_SPARC1000 = math.sqrt(SIG_1000 ** 2 + (SIG_K_TOT ** 2 - SIG_K_JOINT ** 2))
P("    wide binary, EFE-blind reading, full catalogue    %.3f  ->  joint %.4f"
  % (SIG_WB_BLIND_FULL, after(SIG_WB_BLIND_FULL)))
P("    SPARC at N=1000, same systematics (REPLACES it)   %.3f  ->  joint %.4f"
  % (SIG_SPARC1000, SIG_SPARC1000))
P("    distance zero point fixed to 2.5%%                 -     ->  joint %.4f"
  % math.sqrt(SIG_K_TOT ** 2 - (0.161 * K_JOINT) ** 2))
P("    estimator half-span eliminated (analysis, not data) -  ->  joint %.4f" % BEST_SIG)
ck("K24", abs(_a10 - 7.3417e-11) / 7.3417e-11 < 3e-3 and abs(_a03 - 8.5464e-11) / 8.5464e-11 < 3e-3
   and BEST_REMOVE.startswith("estimator") and 15.0 < 100 * (1 - BEST_SIG / SIG_K_TOT) < 35.0,
   "10%%/3%% floor: %.4e/%.4e ; largest removable term '%s' -> %.4f (%.1f%% tighter)"
   % (_a10, _a03, BEST_REMOVE, BEST_SIG, 100 * (1 - BEST_SIG / SIG_K_TOT)),
   "endpoints reproduce A51 to 3e-3 ; the estimator term is the largest and worth 15-35%",
   "the estimator/error-model term dominates the budget, and the distance zero point is the largest term "
   "that a new OBSERVATION could remove")

# =====================================================================================
# K25  the SLACS shape channel: an honest disagreement with A70's Delta-chi2 = 0.26
# =====================================================================================
head("K25  THE SLACS 'FLATNESS' CLAIM: WHERE IT HOLDS AND WHERE IT DOES NOT")

_prof_mean = []
for k in KS_GRID:
    _prof_mean.append(NL * ((float(SPL_M(math.log(k))) + RESP * lnB_req(k)) ** 2) / S_LN ** 2)
P("  with B profiled, the mean term is EXACTLY zero at every kappa (by construction): max %.1e"
  % max(abs(x) for x in _prof_mean))
P("  the full per-lens chi2 at its own best B, kappa = 0.20 / 0.50 / 0.80: %.2f / %.2f / %.2f"
  % tuple(NL * (float(SPL_S(math.log(k))) ** 2) / S_LN ** 2 for k in (0.20, 0.50, 0.80)))
P("  -> Delta-chi2 = %.2f from the SCATTER term over [0.2,0.8], not the 0.26 A70 reports." % D_SHAPE)
P("  the scatter falls monotonically with kappa (%.4f -> %.4f ln) because a larger a0 raises R_pred"
  % (SD_TAB[0], SD_TAB[-1]))
P("  more for the lenses that are currently under-predicted -- the same R_E/R_e residual A70 measured")
P("  at +0.172 +- 0.060.  It is degenerate with the assumed Sersic n = 4, so it is NOT used as kappa")
P("  information in this lane; the primary likelihood uses the mean term (B at fixed kappa) only.")
ck("K25", D_SHAPE > 4.0 and max(abs(x) for x in _prof_mean) < 1e-9,
   "mean term flat to %.0e ; scatter term Delta-chi2 = %.2f over [0.2,0.8]"
   % (max(abs(x) for x in _prof_mean), D_SHAPE),
   "mean term < 1e-9 ; scatter term > 4",
   "A70's Delta-chi2 = 0.26 is a mean-only statement; the full likelihood is NOT flat, and this lane "
   "reports the difference rather than hiding it")

# =====================================================================================
# summary
# =====================================================================================
head("SUMMARY")
NPASS = sum(1 for c in CHECKS if c["pass_"])
P("  %d/%d checks PASS   (%.1f s)" % (NPASS, len(CHECKS), time.time() - T0))
P("  joint kappa = %.5f +- %.5f (stat) +- %.5f (syst) = %.5f +- %.5f"
  % (K_JOINT, SIG_K_JOINT, math.sqrt(max(SIG_K_TOT ** 2 - SIG_K_JOINT ** 2, 0)), K_JOINT, SIG_K_TOT))
SIG_B_JOINT = math.sqrt(1.0 / (1.0 / SIG_B_MEAS ** 2 + 1.0 / SIG_B_PRIOR ** 2))
P("  joint B     = %.4f +- %.4f  (log10 B = %+.4f dex, %.2f sigma above 1.00)"
  % (B_JOINT, B_JOINT * SIG_B_JOINT, math.log10(B_JOINT), PULL_B))
P("  u           = %.4f" % U_JOINT)
P("  kappa_P3 = 1/2 (a0 = 1.1312e-10): %.2f sigma (stat), %.2f sigma (total); inside the total 95%%: %s"
  % (D_STAT, D_TOT, INSIDE_TOT))
P("  a0 = 9.36e-11 (kappa_DE = 1/2, kappa_P3 = %.4f): %.2f sigma (stat), %.2f sigma (total)"
  % (kappa_of_a0(A0_CANON), _d_canon, (kappa_of_a0(A0_CANON) - K_JOINT) / SIG_K_TOT))
P("  global tension T = %.2f for %d dof (%.2f sigma)" % (TENSION, NDOF_SHARED, SIG_TENSION))
P("  channels in the likelihood: 3 (SPARC, SLACS, clusters).  Excluded with reasons: closure (identity), "
  "BAO/SNe/CMB (kappa-blind), wide binaries (no data), L* (same photometry).")

RES = dict(lane="A71", generated=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           mutate=MUT or None, n_check=len(CHECKS), n_pass=NPASS,
           checks=[{k: (bool(v) if k == "pass_" else v) for k, v in c.items()} for c in CHECKS],
           constants=dict(G=G_N, c=C_L, H0=H0_KMS, Omega_L=OMEGA_L, a0_per_kappa=A0_PER_KAPPA,
                          a0_theory=A0_THEORY, a0_canon=A0_CANON, kappa_theory=KAPPA_THEORY,
                          kappa_canon=KAPPA_CANON, rho_crit=RHO_CRIT),
           data=dict(n_sparc_files=len(SPARC_FILES), n_galaxies=NG, n_points=NPT,
                     sha256_sparc=H_SPARC, sha256_slacs=H_SLACS, n_lenses=NL, n_treu=len(ALPHA)),
           sparc=dict(a0=A0_SP, kappa=K_SP, chi2=CHI2_SP, dof=DOF_SP, chi2_dof=CHI2_SP / DOF_SP,
                      sigma_stat_boot=BOOT_FRAC, sigma_dchi2=SIG_DCHI2, sigma_kappa=SIG_K_SP,
                      estimator_half_span=EST_HALF_SPAN),
           slacs=dict(B_req=B_REQ, median_ratio=MED50, mean_ln=MEANLN50,
                      one_over_median=B_INV, one_over_median_sq=B_INV2,
                      kstar=KSTAR, sigma_kappa_salpeter=SIG_K_SALP,
                      dlnR_dlnB=RESP, dlnR_dlnB_scatter=RESP_SCATTER,
                      dlnR_dlnkappa=_dlnR_dlnk, sigma_logB_dex=SIG_LOGB_DEX,
                      sigma_logB_curvature_dex=SIG_LOGB_CURV,
                      B_from_response=B_FROM_RESP, mean_ln_table=ML_TAB.tolist(),
                      scatter_table=SD_TAB.tolist(), kappa_table=KS_GRID.tolist()),
           cluster=dict(dlnR_dlna0=DLNR, kappa=K_CL, sigma_kappa=SIG_K_CL, R_tot=R_CAN,
                        r_v_Mpc=RV_CAN / MPC, F=F_CAN, R_req=R_REQ, sigma_R=SIG_R, u=U0, sigma_u=SIG_U),
           closure=dict(N_lambda=N_LAMBDA, y_t_obs=YT_OBS, y_t_half=YT_HALF,
                        kappa_from_lambda=KAPPA_LAMBDA, elasticity=_elast, max_residual=_maxres),
           cosmology=dict(max_divergence_two_kappa=_dk, max_reparam_residual=_rep, kappa_blind=True),
           wide_binary=dict(gamma_efe_blind=G_WB_CANON, gamma_efe_present=G_WB_EFE_CANON,
                            dgamma_dkappa=DG_WB, dgamma_dkappa_efe=DG_WB_EFE,
                            sigma_kappa_20kau=SIG_WB),
           joint=dict(kappa=K_JOINT, sigma_stat=SIG_K_JOINT, sigma_tot=SIG_K_TOT,
                      sys_frac=SYS_FRAC, lo95_stat=math.exp(_lo95), hi95_stat=math.exp(_hi95),
                      lo95_tot=LO95_TOT, hi95_tot=HI95_TOT, B=B_JOINT, u=U_JOINT,
                      chi2=CHI2_TOT, chi2_sparc=CHI2_SP_JOINT, chi2_slacs=CHI2_SL_JOINT,
                      chi2_cluster=CHI2_CL_JOINT, chi2_prior_B=CHI2_PR_JOINT,
                      chi2_sparc_raw=CHI2_SP_RAW, chi2_slacs_raw=CHI2_SL_RAW,
                      chi2_dof_sparc=CHI2_SP_RAW / DOF_SP, chi2_dof_slacs=CHI2_SL_RAW / (NL - 2),
                      pull_sparc=(K_SP_CH - K_JOINT) / SIG_SP_CH,
                      pull_cluster=(K_CL_ONLY - K_JOINT) / SIG_CL_ONLY,
                      pull_slacs_kappa=(K_SL_ONLY - K_JOINT) / SIG_SL_ONLY,
                      pull_B=PULL_B, tension=TENSION, tension_dof=NDOF_SHARED,
                      tension_sigma=SIG_TENSION, tension_no_prior=TENSION_NO_PRIOR,
                      sigma_kappa_noslac=K_NOSLAC,
                      dstat_half=D_STAT, dtot_half=D_TOT,
                      inside95_stat=bool(INSIDE_STAT), inside95_tot=bool(INSIDE_TOT),
                      chi2_at_half=CHI2_AT_HALF, chi2_at_theory=CHI2_AT_THEORY,
                      chi2_at_theory_sys=CHI2_AT_THEORY_SYS,
                      lnB_req_at_joint=lnB_req(K_JOINT), B_at_sparc=B_AT_SPARC,
                      pull_B_sparc=PULL_B_SPARC, kappa_for_95bound=K_FOR_95,
                      sigma_for_95bound=(K_FOR_95 - K_JOINT) / SIG_K_JOINT,
                      kappa_de=K_JOINT_DE, sigma_kappa_de=SIG_K_JOINT_DE,
                      kappa_de_at_canon=K_DE_CANON, kappa_p3_at_canon=kappa_of_a0(A0_CANON),
                      d_to_canon_p3=_d_canon, d_to_canon_de=(0.5 - K_JOINT_DE) / SIG_K_JOINT_DE,
                      d_to_theory_p3=(0.5 - K_JOINT) / SIG_K_JOINT,
                      sigma_lnB=SIG_LNB, corr_kB=CORR, Lstar_joint_pc=LSTAR_JOINT,
                      sep_footings_sigma=SEP_FOOTINGS,
                      chi2_theory_split=[_th_sp, _th_sl, _th_cl],
                      dchi2_slacs_scatter_band=D_SHAPE, dchi2_slacs_scatter_full=D_SHAPE_FULL),
           budget=dict(terms={nm: s for nm, s in BUDGET}, remove_one={nm: s for nm, s in REMOVED},
                       best_removable=BEST_REMOVE, sigma_then=BEST_SIG,
                       sigma_wide_binary=SIG_WB, sigma_wide_binary_full=SIG_WB_FULL,
                      sigma_1000=SIG_1000, sigma_sparc1000=SIG_SPARC1000,
                      sigma_wb_blind_full=SIG_WB_BLIND_FULL, joint_after_wb=after(SIG_WB_FULL),
                      joint_after_distance=math.sqrt(SIG_K_TOT ** 2 - (0.161 * K_JOINT) ** 2)),
           a51_cross_check=dict(kappa=A51["joint"]["kappa"], sigma=A51["joint"]["sigma_stat"]))
json.dump(RES, open(os.path.join(HERE, "a71_results" + TAG + ".json"), "w"), indent=1)

P("")
P("  wrote a71_results%s.json ; %d/%d PASS ; exit %d"
  % (TAG, NPASS, len(CHECKS), 0 if NPASS == len(CHECKS) else 1))
OUTF.close()
sys.exit(0 if NPASS == len(CHECKS) else 1)
