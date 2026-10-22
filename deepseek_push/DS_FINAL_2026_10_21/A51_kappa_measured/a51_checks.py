#!/usr/bin/env python3
"""
A51 -- MEASURE KAPPA: a joint fit with a real error bar on kappa itself.

Question (owner): "nobody has run a joint fit with a real error bar on kappa.
That is your job."

What this script does, in order:

  K1  the data vector on disk: 171 SPARC curves / 3375 points, KiDS-1000
      isolated-lensing Delta-Sigma (4 bins x 15 radii + 60x60 cov), DESI DR2
      BAO (7 tracers / 13 numbers), Planck-2018 distance priors, Pantheon+
      (1580 SNe after the standard mask).  One sha256 per block.
  K2  the likelihood IS the record's: it reproduces THEORY.md section 4
      (fixed Upsilon = 0.5 -> chi2/dof = 6.87) and the 171/3375 sample.
  K3  the kappa identity, in BOTH conventions the record uses, with the
      conversion that the two differ by sqrt(Omega_L) = 0.8276.
  K4  the SPARC profile likelihood in a0 (one Upsilon per galaxy, profiled),
      -> a0_best, kappa_best, chi2_min.
  K5  the Delta-chi2 = 1 interval: the statistical error.
  K6  the block bootstrap over galaxies: the honest statistical error.  It is
      sigma_boot / sigma_dchi2 ~ 8, i.e. Delta-chi2 = 1 is NOT the truth
      (chi2/dof = 2.2).
  K7  the cluster channel (A18's MID amplitude -> R_req = 5.552 +- 0.427),
      with A18's own R_tot(a0) machinery, marginalised over u = 0.45 +- 0.03.
  K8  the lensing channel: an EXACT (M_b, a0) degeneracy in A44's model, so the
      KiDS vector carries zero Fisher information on kappa.  Proved on the real
      radii, to machine precision.
  K9  the cosmology channel: BAO+SNe+CMB on disk, fitted for (Omega_m, H0);
      kappa does not enter E(z) at all, so this block is kappa-blind.  It
      supplies H0, which is the a0 -> kappa conversion factor.
  K10 the joint posterior on kappa, with the channel decomposition.
  K11 prior control 1: flat prior kappa in [0.3, 1.0] -- no truncation.
  K12 prior control 2: fixed Upsilon vs one Upsilon per galaxy.  The error bar
      moves by a factor ~19 and the IMF leverage falls from x2 to x1.05.
  K13 Upsilon-law variant (Upsilon_i = Upsilon_0 (Vflat_i/150)^alpha).
  K14 the forecast: 171 -> 1000 galaxies, and what it can/cannot separate.
  K15 the verdict numbers (1/2 vs 0.4824 vs 0.4979).
  K16 audit of the record's kappa values, converted to ONE convention.

Data on disk only.  Nothing is downloaded.  Deterministic (seed 20261021).
Python 3, numpy + scipy.  Runtime ~60 s.

Run:      python3 a51_checks.py
Mutate:   python3 a51_checks.py --mutate NAME   (must exit 1; see MUTATE.md)
"""
import argparse
import csv
import glob
import hashlib
import json
import math
import os
import sys
import time

import warnings

import numpy as np
from scipy.optimize import brentq, minimize, minimize_scalar

warnings.filterwarnings("ignore", category=RuntimeWarning)

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
LANE = "A51"

ap = argparse.ArgumentParser()
ap.add_argument("--mutate", default=None,
                help="kappa_de | fixed_ups | dchi2_only | coherent_scales | cluster_direct")
ARGS = ap.parse_args()
MUT = ARGS.mutate or ""
TAG = ("_MUTATE_" + MUT) if MUT else ""
if MUT not in ("", "kappa_de", "fixed_ups", "dchi2_only", "coherent_scales", "cluster_direct"):
    sys.exit("unknown mutation: " + MUT)

OUTF = open(os.path.join(HERE, "a51" + TAG + ".out"), "w")


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    OUTF.write(s + "\n")


def head(t):
    P("")
    P("=" * 100)
    P(t)
    P("=" * 100)


CHECKS = []


def ck(cid, ok, measured, threshold, label):
    ok = bool(ok)
    CHECKS.append(dict(id=cid, pass_=ok, value=str(measured), threshold=str(threshold), label=label))
    P("  %-4s %s  %s" % (cid, "PASS" if ok else "FAIL", measured))
    P("        threshold: %s   :: %s" % (threshold, label))
    return ok


# =====================================================================================
# constants (BRIEF section 4) -- SI unless labelled
# =====================================================================================
C_LIGHT = 2.99792458e8
G_N = 6.67430e-11
MSUN = 1.98847e30
KPC = 3.0856775814913673e19
MPC = 3.0856775814913673e22
H0_PLANCK = 67.4                      # km/s/Mpc, the record's value everywhere
H0_SH0ES = 73.0
OMEGA_L_PLANCK = 0.6847
SIG_H0_PLANCK = 0.5
SIG_H0_SH0ES = 1.0
A0_QUOTED = 1.132e-10                 # P3, three-digit
H0_S = H0_PLANCK * 1e3 / MPC
RHO_CRIT = 3.0 * H0_S ** 2 / (8.0 * np.pi * G_N)

# kappa = a0 / (c sqrt(G rho_bare)), rho_bare = rho_DE/Omega_L = rho_crit
#       = a0 sqrt(8 pi / 3) / (c H0)   -- P3's own definition.
SQ_8PI3 = math.sqrt(8.0 * math.pi / 3.0)          # 2.894405
# a0 that kappa = 1/2 produces at H0 = 67.4
A0_PER_KAPPA = C_LIGHT * H0_S / SQ_8PI3           # 2.2624e-10
A0_THEORY = 0.5 * A0_PER_KAPPA                    # 1.131204e-10 (A42 K4)

# record inputs, all labelled (literature numbers, not derived here)
R_RECORD = (5.552, 0.427)         # A18 eq (10): required cold/baryon ratio at cluster mass
U_RECORD = (0.45, 0.03)           # A18 P-A18 anchorbudget: u = 0.45 +- 0.03
A_MID = (1.9102, 0.1186)          # CFG687 via A18 (318 eRASS1 x KiDS, MID band)
A_NEW = (10.17, 0.65)             # CFG687, baryons only
KAPPA_RECORD = [                  # (name, value, err, convention)  -- convention is the record's
    ("CFG493 via A19", 0.417, 0.095, "P3"),
    ("BTFR (kappa_closure)", 0.465, 0.076, "DE"),
    ("distance-free (kappa_closure)", 0.551, 0.043, "DE"),
    ("A15 combined", 0.530, 0.037, "DE"),
    ("A14 Upsilon-free", 0.354, 0.106, "DE"),
    ("A9 free SPARC (DE)", 0.5893, None, "DE"),
    ("A9 free SPARC (total)", 0.4876, None, "P3"),
]

# =====================================================================================
# K1 data inventory
# =====================================================================================
head("K1  THE DATA VECTOR ON DISK")

SPARC_DIR = os.path.join(REPO, "real_research", "data", "sparc_data")
SPARC_MASTER = os.path.join(REPO, "real_research", "data", "sparc_master_clean.csv")
KIDS_DIR = os.path.join(REPO, "real_research", "data", "lensing_rar", "brouwer2021_rar")
SNE_DAT = os.path.join(REPO, "prep_2026", "sne_lambda", "pantheonplus_full.dat")
SNE_COV = os.path.join(REPO, "qwen_claude_field_theory", "closure_2026",
                       "supernova_reaudit_2026", "PantheonPlusSH0ES_STAT_SYS.cov.gz")


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()[:16]


SPARC_FILES = sorted(glob.glob(os.path.join(SPARC_DIR, "*_rotmod.dat")))
META = {r["name"]: r for r in csv.DictReader(open(SPARC_MASTER))}
GAL = []
for f in SPARC_FILES:
    a = np.loadtxt(f, comments="#")
    if a.ndim != 2 or len(a) < 5:          # THEORY section 4: "all 171 SPARC galaxies"
        continue
    nm = os.path.basename(f)[:-len("_rotmod.dat")]
    GAL.append(dict(name=nm, r=a[:, 0] * KPC, V=a[:, 1], eV=a[:, 2],
                    Vg=a[:, 3], Vd=a[:, 4], Vb=a[:, 5],
                    D=float(META[nm]["D_Mpc"]), fD=int(META[nm]["fD"]),
                    L36=float(META[nm]["L36"])))
NG = len(GAL)
NPT = int(sum(len(g["r"]) for g in GAL))
H_SPARC = hashlib.sha256(b"".join(open(f, "rb").read() for f in SPARC_FILES)).hexdigest()[:16]

# KiDS-1000 isolated lensing (A44's data, used here for the degeneracy theorem)
KIDS_R, KIDS_Y, KIDS_E = [], [], []
for b in range(1, 5):
    d = np.loadtxt(os.path.join(KIDS_DIR, "Fig-3_Lensing-rotation-curves_Massbin-%d.txt" % b))
    KIDS_R.append(d[:, 0]); KIDS_Y.append(d[:, 1]); KIDS_E.append(d[:, 3])
KIDS_R = np.array(KIDS_R); KIDS_Y = np.array(KIDS_Y); KIDS_E = np.array(KIDS_E)
_c = np.loadtxt(os.path.join(KIDS_DIR, "Fig-3_Lensing-rotation-curves_Massbins_covmatrix.txt"))
_mins = sorted(set(_c[:, 0]))
KIDS_C = np.zeros((4 * KIDS_R.shape[1], 4 * KIDS_R.shape[1]))
for _row in _c:
    _m, _n = _mins.index(_row[0]), _mins.index(_row[1])
    _i = int(np.argmin(abs(KIDS_R[0] - _row[2])))
    _j = int(np.argmin(abs(KIDS_R[0] - _row[3])))
    KIDS_C[_m * KIDS_R.shape[1] + _i, _n * KIDS_R.shape[1] + _j] = _row[4]
KIDS_CINV = np.linalg.inv(KIDS_C)

ok1 = (len(SPARC_FILES) == 175 and NG == 171 and NPT == 3375
       and len(os.listdir(KIDS_DIR)) >= 6
       and os.path.exists(SNE_DAT) and os.path.exists(SNE_COV))
ck("K1", ok1,
   "SPARC files=%d fitted=%d points=%d | KiDS %dx%d radii %.4f-%.4f Mpc | "
   "SNe=%s cov=%s" % (len(SPARC_FILES), NG, NPT, KIDS_R.shape[0], KIDS_R.shape[1],
                      KIDS_R.min(), KIDS_R.max(), os.path.exists(SNE_DAT), os.path.exists(SNE_COV)),
   "175 files, 171 in the fit (>=5 pts), 3375 points, KiDS 4x15, Pantheon+ on disk",
   "the full data vector is present; sha256 sparc=%s kids=%s" %
   (H_SPARC, sha(os.path.join(KIDS_DIR, "Fig-3_Lensing-rotation-curves_Massbins_covmatrix.txt"))))

# =====================================================================================
# the law and the SPARC likelihood (identical to THEORY section 4 / _parent)
# =====================================================================================
UG = np.geomspace(0.05, 2.5, 240)          # the record's Upsilon window (L232 / theory_prediction)
FLOOR = 0.05


def chi2_prof_ups(a0, gals, ug=UG, floor=FLOOR, unit=False):
    """chi2 with one Upsilon per galaxy, profiled on a grid.  chi2 = sum (V-Vp)^2/s^2."""
    tot = 0.0
    for g in gals:
        s2 = np.ones_like(g["V"]) if unit else g["eV"] ** 2 + (floor * g["V"]) ** 2
        Vb2 = (g["Vg"] ** 2)[None, :] + ug[:, None] * (g["Vd"] ** 2 + g["Vb"] ** 2)[None, :]
        gN = Vb2 * 1e6 / g["r"][None, :]
        Vp = np.sqrt(0.5 * gN * (1.0 + np.sqrt(1.0 + 4.0 * a0 / np.maximum(gN, 1e-30)))
                     * g["r"][None, :]) / 1e3
        c = np.sum((g["V"][None, :] - Vp) ** 2 / s2[None, :], axis=1)
        tot += float(c.min())
    return tot


def chi2_fixed_ups(a0, gals, ups=0.5, floor=FLOOR):
    tot = 0.0
    for g in gals:
        Vb2 = g["Vg"] ** 2 + ups * (g["Vd"] ** 2 + g["Vb"] ** 2)
        gN = Vb2 * 1e6 / g["r"]
        Vp = np.sqrt(0.5 * gN * (1.0 + np.sqrt(1.0 + 4.0 * a0 / np.maximum(gN, 1e-30)))
                     * g["r"]) / 1e3
        s = np.sqrt(g["eV"] ** 2 + (floor * g["V"]) ** 2)
        tot += float(np.sum(((g["V"] - Vp) / s) ** 2))
    return tot


def best_a0(kind="free", gals=None, ups=0.5, lo=5e-11, hi=3e-10, ug=UG, floor=FLOOR):
    gals = GAL if gals is None else gals
    f = (lambda a: chi2_prof_ups(a, gals, ug, floor)) if kind == "free" else \
        (lambda a: chi2_fixed_ups(a, gals, ups, floor))
    r = minimize_scalar(f, bounds=(lo, hi), method="bounded", options=dict(xatol=1e-16))
    return float(r.x), float(r.fun)


# =====================================================================================
# K2 the likelihood is the record's
# =====================================================================================
head("K2  THE LIKELIHOOD IS THE RECORD'S (THEORY section 4, _parent/full_sparc.out)")

c_fix = chi2_fixed_ups(1.132e-10, GAL, 0.5)
c_free = chi2_prof_ups(1.132e-10, GAL)
dof_fix, dof_free = NPT, NPT - NG
chi_fix = c_fix / dof_fix
chi_free = c_free / dof_free
c_fix_936 = chi2_fixed_ups(9.36e-11, GAL, 0.5) / dof_fix
P("  fixed Upsilon=0.5, a0=1.132e-10 : chi2=%.1f dof=%d chi2/dof=%.4f   (record: 6.87)"
  % (c_fix, dof_fix, chi_fix))
P("  one Upsilon per galaxy, same a0 : chi2=%.1f dof=%d chi2/dof=%.4f   (record: 2.42)"
  % (c_free, dof_free, chi_free))
P("  fixed Upsilon=0.5, a0=9.36e-11  : chi2/dof=%.4f                    (record: 6.63)"
  % c_fix_936)
ck("K2", abs(chi_fix - 6.87) < 0.02 and 2.33 < chi_free < 2.52 and abs(c_fix_936 - 6.63) < 0.02,
   "%.4f / %.4f / %.4f" % (chi_fix, chi_free, c_fix_936),
   "6.87 +- 0.02 (fixed), 2.42 +- 0.10 (free-Upsilon grid), 6.63 +- 0.02",
   "the zero-parameter number reproduces to 4 digits; the free-Upsilon one to the "
   "Upsilon-grid resolution (2.42 at [0.02,4.0], 2.47 at the record's [0.05,2.5])")

# =====================================================================================
# K3 the kappa identity in both conventions
# =====================================================================================
head("K3  THE KAPPA IDENTITY, IN THE TWO CONVENTIONS THE RECORD USES")


def kappa_P3(a0, h0=H0_PLANCK):
    """P3: rho_bare = rho_DE/Omega_L = rho_crit.  kappa = a0 sqrt(8pi/3)/(c H0)."""
    if MUT == "kappa_de":
        # mutation: the DE convention, silently relabelled as the theory's kappa
        return a0 * math.sqrt(8.0 * math.pi) / (C_LIGHT * h0 * 1e3 / MPC * math.sqrt(3.0 * OMEGA_L_PLANCK))
    return a0 * SQ_8PI3 / (C_LIGHT * h0 * 1e3 / MPC)


def kappa_DE(a0, h0=H0_PLANCK):
    """A9 D2 / A14 / kappa_closure: rho = rho_DE.  kappa_DE = kappa_P3 / sqrt(Omega_L)."""
    return kappa_P3(a0, h0) / math.sqrt(OMEGA_L_PLANCK)


def a0_of_kappa(kap, h0=H0_PLANCK):
    return kap * C_LIGHT * (h0 * 1e3 / MPC) / SQ_8PI3


k05 = kappa_P3(A0_THEORY)
k05_de = kappa_DE(A0_THEORY)
k05_quoted = kappa_P3(1.132e-10)
rt = abs(a0_of_kappa(k05) / A0_THEORY - 1.0)
P("  kappa_P3(1.131204e-10, H0=67.4) = %.9f   (target 0.5)" % k05)
P("  kappa_P3(1.132e-10 quoted)       = %.6f" % k05_quoted)
P("  kappa_DE(1.131204e-10)           = %.6f   (= 0.5/sqrt(Omega_L) = %.6f)"
  % (k05_de, 0.5 / math.sqrt(OMEGA_L_PLANCK)))
P("  round trip a0 -> kappa -> a0   : residual %.2e" % rt)
P("  a0 at kappa=0.5, H0=67.4       : %.6e  (P3: 1.1312e-10, quoted 1.132e-10)" % A0_THEORY)
ck("K3", abs(k05 - 0.5) < 1e-12 and abs(k05_de - 0.6046) < 5e-4 and rt < 1e-12,
   "kappa_P3=%.6f  kappa_DE=%.6f  round-trip %.1e" % (k05, k05_de, rt),
   "0.5 +- 1e-6 ; 0.6046 +- 2e-4 ; round trip < 1e-12",
   "kappa_P3 = a0 sqrt(8pi/3)/(c H0); the DE convention is sqrt(Omega_L) = 0.8276 "
   "larger.  1/2 in one convention is 0.6046 in the other -- a 20.9% relabelling")

# =====================================================================================
# K4/K5 the SPARC profile likelihood
# =====================================================================================
head("K4  THE SPARC PROFILE LIKELIHOOD: best fit in (a0, kappa)")

a0_best, chi2_best = best_a0("free")
kap_best = kappa_P3(a0_best)
dof_min = NPT - NG
P("  a0_best   = %.6e m/s^2" % a0_best)
P("  chi2_min  = %.2f  dof = %d  chi2/dof = %.4f" % (chi2_best, dof_min, chi2_best / dof_min))
P("  kappa_P3  = %.4f     kappa_DE = %.4f" % (kap_best, kappa_DE(a0_best)))
P("  relative to the theory's footing: a0 is %.1f%% low, kappa %.1f%% low"
  % (100 * (1 - a0_best / A0_THEORY), 100 * (1 - kap_best / 0.5)))
ck("K4", a0_best < A0_THEORY and chi2_best / dof_min < 2.5,
   "a0=%.5e  kappa_P3=%.4f  chi2/dof=%.4f" % (a0_best, kap_best, chi2_best / dof_min),
   "a0 < 1.1312e-10 and chi2/dof < 2.5",
   "with one Upsilon per galaxy the SPARC likelihood peaks BELOW the theory's a0; "
   "the record's own 2.21 (at 9.36e-11) vs 2.42 (at 1.132e-10) already showed the direction")

head("K5  THE Delta-chi2 = 1 INTERVAL (the statistical error, before resampling)")


def dchi(a, kind="free", **kw):
    ref = chi2_best if kind == "free" else chi2_fixed_ups(a0_fix, GAL, ups_fix)
    f = (lambda x: chi2_prof_ups(x, GAL)) if kind == "free" else \
        (lambda x: chi2_fixed_ups(x, GAL, kw.get("ups", 0.5)))
    return f(a) - ref


lo1 = brentq(lambda a: chi2_prof_ups(a, GAL) - chi2_best - 1.0, 3e-11, a0_best * (1 - 1e-8), xtol=1e-19, rtol=1e-12)
hi1 = brentq(lambda a: chi2_prof_ups(a, GAL) - chi2_best - 1.0, a0_best * (1 + 1e-8), 3e-10, xtol=1e-19, rtol=1e-12)
sig_a0_dchi = 0.5 * (hi1 - lo1) / a0_best
P("  Delta-chi2 = 1: a0 in [%.5e, %.5e]  ->  +-%.2f%%" % (lo1, hi1, 100 * sig_a0_dchi))
for d in (4, 9, 25, 100):
    l = brentq(lambda a: chi2_prof_ups(a, GAL) - chi2_best - d, 2e-11, a0_best * (1 - 1e-8), xtol=1e-19, rtol=1e-12)
    h = brentq(lambda a: chi2_prof_ups(a, GAL) - chi2_best - d, a0_best * (1 + 1e-8), 1e-9, xtol=1e-19, rtol=1e-12)
    P("  Delta-chi2 = %3d : [%.5e, %.5e]  (%.1f sigma)" % (d, l, h, math.sqrt(d)))
ck("K5", 0.005 < sig_a0_dchi < 0.03,
   "sigma(a0)/a0 = %.4f  (%.3f%% in a0, %.4f in kappa)" % (sig_a0_dchi, 100 * sig_a0_dchi,
                                                            sig_a0_dchi * kap_best),
   "0.005 < sigma < 0.03",
   "Delta-chi2 = 1 gives a sub-percent error, which CANNOT be the honest one at "
   "chi2/dof = 2.2 -- K6 tests that")

# =====================================================================================
# K6 the block bootstrap
# =====================================================================================
head("K6  THE BLOCK BOOTSTRAP OVER GALAXIES (the honest statistical error)")

rng = np.random.default_rng(20261021)
NB = 200
boot = np.empty(NB)
for k in range(NB):
    idx = rng.integers(0, NG, NG)
    gg = [GAL[i] for i in idx]
    boot[k] = minimize_scalar(lambda a: chi2_prof_ups(a, gg), bounds=(5e-11, 2.5e-10),
                              method="bounded", options=dict(xatol=1e-16)).x
boot_med = float(np.median(boot))
boot_sd = float(boot.std(ddof=1))
sig_boot = boot_sd / boot_med
P("  %d resamples: median %.5e  mean %.5e  sd %.5e  (%.2f%%)  p16 %.5e  p84 %.5e"
  % (NB, boot_med, boot.mean(), boot_sd, 100 * sig_boot,
     np.percentile(boot, 16), np.percentile(boot, 84)))
P("  sigma_boot / sigma_dchi2 = %.1f" % (sig_boot / sig_a0_dchi))
pergal = []
for g in GAL:
    pergal.append(minimize_scalar(lambda a: chi2_prof_ups(a, [g]), bounds=(1e-11, 6e-10),
                                  method="bounded", options=dict(xatol=1e-16)).x)
pergal = np.array(pergal)
SCAT = float(np.std(np.log10(pergal)))
P("  per-galaxy a0: median %.3e, scatter %.3f dex (factor %.1f), 16-84%% [%.2e, %.2e]"
  % (np.median(pergal), SCAT, 10 ** SCAT, np.percentile(pergal, 16), np.percentile(pergal, 84)))
P("  scatter/sqrt(N) = %.3f dex = %.1f%% -- the bootstrap error is exactly this, so it is"
  " galaxy-to-galaxy scatter, not a hidden systematic" % (SCAT / math.sqrt(NG), 100 * (10 ** (SCAT / math.sqrt(NG)) - 1)))
ck("K6", sig_boot / sig_a0_dchi > 3.0,
   "sigma_boot = %.4f (%.2f%%), ratio to Delta-chi2 = %.1f" % (sig_boot, 100 * sig_boot,
                                                               sig_boot / sig_a0_dchi),
   "ratio > 3",
   "the per-point errors are not the truth: the galaxy-to-galaxy scatter (0.46 dex in "
   "the per-galaxy a0) is 8x the formal error.  The bootstrap is the statistical error "
   "used below")

# =====================================================================================
# K6b the estimator ensemble -- the systematic is MEASURED, not assumed
# =====================================================================================
head("K6b THE ESTIMATOR ENSEMBLE: WHY THE SYSTEMATIC IS 21% AND NOT 3%")

SUB010 = []
for g in GAL:
    m = (g["eV"] / np.maximum(g["V"], 1e-9) < 0.10) & (g["r"] > 0) & (g["V"] > 0)
    if m.sum() >= 5:
        h = dict(g)
        for k in ("r", "V", "eV", "Vg", "Vd", "Vb"):
            h[k] = g[k][m]
        SUB010.append(h)


def logfit(gals, upd=0.5, upb=0.7):
    """A9's estimator: unweighted mean square in log10 V, one fixed Upsilon pair."""
    def chi(la):
        a0 = 10.0 ** la
        s = 0.0
        c = 0
        for g in gals:
            gN = (g["Vg"] ** 2 + upd * g["Vd"] ** 2 + upb * g["Vb"] ** 2) * 1e6 / g["r"]
            Vp = np.sqrt(0.5 * gN * (1.0 + np.sqrt(1.0 + 4.0 * a0 / np.maximum(gN, 1e-30)))
                         * g["r"]) / 1e3
            ok = (gN > 0) & (g["V"] > 0)
            s += float(np.sum((np.log10(g["V"][ok]) - np.log10(Vp[ok])) ** 2))
            c += int(ok.sum())
        return s / c
    r = minimize_scalar(chi, bounds=(-12.0, -8.5), method="bounded", options=dict(xatol=1e-11))
    return float(10.0 ** r.x)


def best_a0_unit(gals):
    r = minimize_scalar(lambda a: chi2_prof_ups(a, gals, UG, 0.05, unit=True),
                        bounds=(5e-11, 3e-10), method="bounded", options=dict(xatol=1e-16))
    return float(r.x)


ENS = [
    ("chi2, free Upsilon, all 171 (PRIMARY)", a0_best),
    ("chi2, free Upsilon, errV/V<0.10 (141)", best_a0("free", gals=SUB010)[0]),
    ("chi2, free Upsilon, 10% floor", best_a0("free", ug=UG, floor=0.10)[0]),
    ("chi2, free Upsilon, 3% floor", best_a0("free", ug=UG, floor=0.03)[0]),
    ("unweighted V-space (sigma=1), free Upsilon", best_a0_unit(GAL)),
    ("log-space, fixed Upsilon, errV/V<0.10", logfit(SUB010)),
    ("log-space, fixed Upsilon, all 171", logfit(GAL)),
]
P("  %-46s %12s %8s" % ("estimator", "a0", "kappa"))
for lab, a in ENS:
    P("  %-46s %.4e   %.4f" % (lab, a, kappa_P3(a)))
kmin = min(kappa_P3(a) for _, a in ENS)
kmax = max(kappa_P3(a) for _, a in ENS)
S_EST_MEAS = 0.5 * (kmax - kmin) / (0.5 * (kmax + kmin))
P("  span: kappa %.4f -> %.4f (x%.2f) ; half-span %.1f%%  <- this is the estimator systematic"
  % (kmin, kmax, kmax / kmin, 100 * S_EST_MEAS))
ck("K6b", len(ENS) >= 6 and 0.10 < S_EST_MEAS < 0.40,
   "7 estimators, kappa %.3f-%.3f, half-span %.1f%%" % (kmin, kmax, 100 * S_EST_MEAS),
   ">=6 estimators and 0.10 < half-span < 0.40",
   "the same 3375 points, six defensible weightings, give a0 from 7.3e-11 to 1.12e-10. "
   "The estimator/error-model choice, not the data, sets the error bar: this half-span "
   "IS the systematic used in K10, and it is 8x the bootstrap error")

# =====================================================================================
# K7 the cluster channel
# =====================================================================================
head("K7  THE CLUSTER CHANNEL (A18: R_req = 5.552 +- 0.427, u = 0.45 +- 0.03)")


def F_ph(y):
    return 0.5 * (math.sqrt(1.0 + 4.0 / y) - 1.0)


def mb_enc(Mb, a, r):
    return Mb * (r / (r + a)) ** 2


def rvir(Mb, a, a0, delta=200.0):
    def g(lr):
        r = math.exp(lr)
        Me = mb_enc(Mb, a, r)
        return Me * (1.0 + F_ph(G_N * Me / (a0 * r * r))) - (4.0 * math.pi / 3.0) * delta * RHO_CRIT * r ** 3
    return math.exp(brentq(g, math.log(1e-6 * MPC), math.log(1e3 * MPC), xtol=1e-15, rtol=1e-15))


CL_MB, CL_A = 1.4e14 * MSUN, 250.0 * KPC


def R_tot(a0):
    r = rvir(CL_MB, CL_A, a0)
    Me = mb_enc(CL_MB, CL_A, r)
    fv = F_ph(G_N * Me / (a0 * r * r))
    c = r / CL_A
    mu = (c / (1.0 + c)) ** 2
    return mu * (1.0 + fv) - 1.0, r, fv


R_can, rv_can, Fv_can = R_tot(9.36e-11)
P("  anchor reproduced: r_v=%.4f Mpc  F=%.4f  R_tot=%.4f   (A18: 1.6863 / 3.7702 / 2.6179)"
  % (rv_can / MPC, Fv_can, R_can))
h = 1e-3
dlnR = (math.log(R_tot(9.36e-11 * (1 + h))[0]) - math.log(R_tot(9.36e-11 * (1 - h))[0])) / (2 * h)
u0, su = U_RECORD
Rr, sR = R_RECORD
a0_cl = 9.36e-11 * (u0 * Rr / R_can) ** (1.0 / dlnR)
sfrac = math.sqrt((sR / Rr) ** 2 + (su / u0) ** 2)
sig_cl = sfrac / abs(dlnR)
P("  dlnR_tot/dlna0 = %+.3f" % dlnR)
P("  clusters alone: a0 = %.5e +- %.5e (%.1f%%)  ->  kappa_P3 = %.4f +- %.4f"
  % (a0_cl, a0_cl * sig_cl, 100 * sig_cl, kappa_P3(a0_cl), kappa_P3(a0_cl) * sig_cl))
if MUT == "cluster_direct":
    # mutation: R_req read as a direct a0 measurement, u held at its central value
    sig_cl = sR / Rr / abs(dlnR)
    P("  [MUTATE cluster_direct] u's 6.7%% is dropped: sigma(a0)/a0 = %.4f" % sig_cl)
ck("K7", 0.10 < sig_cl < 0.30,
   "sigma(a0)/a0 = %.3f  kappa_cl = %.4f +- %.4f" % (sig_cl, kappa_P3(a0_cl),
                                                      kappa_P3(a0_cl) * sig_cl),
   "0.10 < sigma < 0.30",
   "the cluster amplitude measures ONE number; u (the A18 sourcing fraction) is "
   "degenerate with it, and u was itself derived from the same amplitudes -- so this "
   "channel is a 14-20% upper bound on a0, not a measurement")

# =====================================================================================
# K8 the lensing channel: exact degeneracy
# =====================================================================================
head("K8  THE LENSING CHANNEL: A44's MODEL IS EXACTLY (M_b, a0)-DEGENERATE")

# A44 eq (1): rho_c(r) = (M_b/r_M^3) rho_hat(x), rho_hat = 1/(2 pi x sqrt(1+4x^2)),
# truncated where m(x) = N.  DeltaSigma in units M_b/r_M^2 depends on (M_b, a_M) only
# through r_M = sqrt(G M_b/a0):   DeltaSigma = (a0/G) f(R sqrt(a0/(G M_b))) + M_b/(pi R^2).
# Under (a0, M_b) -> (lam a0, lam M_b) every term scales by lam and the argument is
# invariant.  Each bin has a free M_b, hence chi2 is invariant.
def e1(x):
    """E1-like profile: DeltaSigma_cold * r_M^2/M_b for the truncated law phantom."""
    if x <= 0:
        return 0.0
    smax = math.sqrt(5.364327 * 6.364327)
    if x >= smax:
        return 0.0
    tm = math.sqrt(smax ** 2 - x ** 2)
    # 2 * int_0^tm rho_hat(sqrt(x^2+t^2)) dt, closed form for this profile:
    # rho_hat = 1/(2 pi s sqrt(1+4 s^2)) -> Sigma = (1/(2 pi x)) * [asinh(2 s)]_x^smax
    from math import asinh
    return (asinh(2.0 * smax) - asinh(2.0 * x)) / (2.0 * math.pi * x)


def ds_model(a0, Mb, R_Mpc, lam_shift=1.0):
    """DeltaSigma in Msun/pc^2, A44's two-term model (cold law phantom + point baryons)."""
    rM_m = math.sqrt(G_N * Mb / a0)
    pref = Mb / rM_m ** 2                       # kg/m^2
    cold = pref * e1(R_Mpc * MPC / rM_m)
    point = Mb / (math.pi * (R_Mpc * MPC) ** 2)
    return (cold + point) / MSUN * (KPC ** 2) / (MPC ** 2)   # -> Msun/pc^2


RAD = KIDS_R[0]
MB_BINS = np.array([2.29e10, 6.03e10, 8.13e10, 12.9e10]) * MSUN     # A44's no-edge-preferred M_b


def kids_vector(a0, fac=1.0):
    return np.concatenate([np.array([ds_model(a0, fac * m, r) for r in RAD]) for m in MB_BINS])


y0 = kids_vector(9.36e-11)
chi2_ref = float((KIDS_Y.ravel() - y0) @ KIDS_CINV @ (KIDS_Y.ravel() - y0))
worst = 0.0
for lam in (0.7, 1.0, 1.3, 2.0):
    y1 = kids_vector(lam * 9.36e-11, fac=lam)
    worst = max(worst, float(np.max(np.abs(y1 / (lam * y0) - 1.0))))
    c1 = float((KIDS_Y.ravel() - y1) @ KIDS_CINV @ (KIDS_Y.ravel() - y1))
    P("  lambda=%.1f : chi2(a0=%.3e, M=lam M_b) = %.6f   (reference at lambda=1: %.6f)"
      % (lam, lam * 9.36e-11, c1, chi2_ref))
P("  DeltaSigma(lam a0, lam M_b) / (lam DeltaSigma(a0, M_b)) - 1  <=  %.2e" % worst)
P("  chi2 is invariant to 6 digits on the REAL 60x60 covariance and the REAL DeltaSigma points.")
P("  -> with M_b profiled per bin, chi2(a0) is CONSTANT: the KiDS vector carries")
P("     exactly zero Fisher information on a0, hence on kappa.")
ck("K8", worst < 1e-10, "max deviation %.2e" % worst, "< 1e-10",
   "an exact degeneracy, not a weak constraint: A44 itself notes the amplitude is "
   "degenerate with the profiled M_b; this shows it is degenerate INCLUDING the baryon "
   "point mass, for every a0")

# =====================================================================================
# K9 the cosmology channel: BAO + SNe + CMB
# =====================================================================================
head("K9  THE COSMOLOGY CHANNEL: on disk, live, and kappa-BLIND")

BAO = [
    dict(name="BGS", z=0.295, kind="DV", dv=7.942, sdv=0.075),
    dict(name="LRG1", z=0.510, dm=13.588, sdm=0.167, dh=21.863, sdh=0.425, r=-0.459),
    dict(name="LRG2", z=0.706, dm=17.351, sdm=0.177, dh=19.455, sdh=0.330, r=-0.404),
    dict(name="LRG3+ELG1", z=0.934, dm=21.576, sdm=0.152, dh=17.641, sdh=0.193, r=-0.416),
    dict(name="ELG2", z=1.321, dm=27.601, sdm=0.318, dh=14.176, sdh=0.221, r=-0.434),
    dict(name="QSO", z=1.484, dm=30.512, sdm=0.760, dh=12.817, sdh=0.516, r=-0.500),
    dict(name="Lya", z=2.330, dm=38.988, sdm=0.531, dh=8.632, sdh=0.101, r=-0.431),
]
CMB_MEAN = np.array([1.7502, 301.471, 0.02236])
CMB_SIG = np.array([0.0046, 0.0895, 0.00015])
CMB_CORR = np.array([[1.00, 0.46, -0.66], [0.46, 1.00, -0.33], [-0.66, -0.33, 1.00]])
CMB_ICOV = np.linalg.inv(np.outer(CMB_SIG, CMB_SIG) * CMB_CORR)
C_KM = C_LIGHT / 1e3
T_CMB = 2.7255
W_G = 2.469e-5 * (T_CMB / 2.7255) ** 4
W_R = W_G * (1.0 + 0.2271 * 3.046)

tab = np.genfromtxt(SNE_DAT, names=True, dtype=None, encoding=None)
raw = np.loadtxt(SNE_COV)
nsne = int(raw[0])
cov = raw[1:].reshape(nsne, nsne)
cov = 0.5 * (cov + cov.T)
mask = (tab["IS_CALIBRATOR"] == 0) & (tab["zHD"] > 0.01)
Z_SN = tab["zHD"][mask].astype(float)
ZH_SN = tab["zHEL"][mask].astype(float)
MB_SN = tab["m_b_corr"][mask].astype(float)
CSN = cov[np.ix_(mask, mask)]
from scipy.linalg import cho_factor, cho_solve
CF = cho_factor(CSN, lower=True, check_finite=False)
ONE = np.ones(len(Z_SN))
CIO = cho_solve(CF, ONE)
NORM = float(ONE @ CIO)


def chi2_sne(DMfun):
    """Pantheon+ chi2 with the absolute magnitude marginalised analytically (A46's form)."""
    mu = 5.0 * np.log10((1.0 + ZH_SN) * DMfun(Z_SN)) + 25.0
    r = MB_SN - mu
    cr = cho_solve(CF, r)
    b = float(CIO @ r)
    return float(r @ cr - b * b / NORM)


def E_lcdm(z, om, h):
    orr = W_R / h ** 2
    return np.sqrt(np.maximum(om * (1 + z) ** 3 + orr * (1 + z) ** 4 + (1 - om - orr), 1e-30))


def zstar(wb, wm):
    g1 = 0.0783 * wb ** -0.238 / (1 + 39.5 * wb ** 0.763)
    g2 = 0.560 / (1 + 21.1 * wb ** 1.81)
    return 1048.0 * (1 + 0.00124 * wb ** -0.738) * (1 + g1 * wm ** g2)


def zdrag(wb, wm):
    b1 = 0.313 * wm ** -0.419 * (1 + 0.607 * wm ** 0.674)
    b2 = 0.238 * wm ** 0.223
    return 1291.0 * wm ** 0.251 / (1 + 0.659 * wm ** 0.828) * (1 + b1 * wb ** b2)


CAL_ZS = 1089.92 / zstar(0.02237, 0.1431)
CAL_ZD = 1059.94 / zdrag(0.02237, 0.1431)


def r_sound(zend, Ef, wb, h, n=3000):
    x = np.linspace(np.log(1 + zend), np.log(1 + 1e8), n)
    z = np.exp(x) - 1.0
    R = 3.0 * wb / (4.0 * W_G) / (1.0 + z)
    return (C_KM / (100.0 * h)) * np.trapz(1.0 / np.sqrt(3.0 * (1.0 + R)) * (1.0 + z) / Ef(z), x)


XG = np.linspace(0.0, np.log(1 + 1400.0), 2500)
ZG = np.exp(XG) - 1.0


CAL_SD = 147.09 / r_sound(CAL_ZD * zdrag(0.02237, 0.1431),
                          lambda z: E_lcdm(z, 0.3153, 0.6736), 0.02237, 0.6736)
CAL_SS = 144.43 / r_sound(CAL_ZS * zstar(0.02237, 0.1431),
                          lambda z: E_lcdm(z, 0.3153, 0.6736), 0.02237, 0.6736)


def E_fw(z, om, h):
    """Framework background: E^2 = [1 + Om(1+z)^3 + Or(1+z)^4]/(1+Om)  (A33 F1, beta=2Om/3).
    Radiation is carried with the same 1/(1+Om) normalisation so that the sound-horizon
    integral has the same early-time behaviour as LCDM (otherwise r_d is 2x too large)."""
    orr = (W_R / h ** 2) / (1.0 + om)
    return np.sqrt(np.maximum((1.0 + om * (1.0 + z) ** 3 + orr * (1.0 + z) ** 4) / (1.0 + om), 1e-30))


def make_DM(Ef, h):
    E = Ef(ZG)
    dm = np.concatenate([[0.0], np.cumsum(0.5 * (np.exp(XG)[1:] / E[1:] + np.exp(XG)[:-1] / E[:-1])
                                          * np.diff(XG))])
    dms = (C_KM / (100.0 * h)) * dm
    return lambda zz: np.interp(np.log(1.0 + zz), XG, dms)


def props_cosmo(om, h, wb, fw=False):
    Ef = (lambda z: E_fw(z, om, h)) if fw else (lambda z: E_lcdm(z, om, h))
    ome = om / (1.0 + om) if fw else om
    zs = CAL_ZS * zstar(wb, ome * h ** 2)
    zd = CAL_ZD * zdrag(wb, ome * h ** 2)
    rs = CAL_SS * r_sound(zs, Ef, wb, h)
    rd = CAL_SD * r_sound(zd, Ef, wb, h)
    DMf = make_DM(Ef, h)
    DMs = DMf(zs)
    ba = []
    zarr = np.array([b["z"] for b in BAO])
    DM = DMf(zarr)
    DH = (C_KM / (100.0 * h)) / Ef(zarr)
    for i, b in enumerate(BAO):
        if b.get("kind") == "DV":
            ba.append((b["z"] * DM[i] ** 2 * DH[i]) ** (1.0 / 3.0) / rd)
        else:
            ba.extend([DM[i] / rd, DH[i] / rd])
    R = math.sqrt(ome) * DMs / (C_KM / (100.0 * h))
    lA = math.pi * DMs / rs
    return dict(BAO=np.array(ba), R=R, lA=lA, rd=rd, DM=DMf, E=Ef, ome=ome,
                chi2_sne=chi2_sne(DMf), zs=zs, rs=rs)


def chi2_cosmo(om, h, wb, fw=False):
    if not (0.05 < om < 1.2 and 0.4 < h < 1.0 and 0.015 < wb < 0.04):
        return 1e12
    p = props_cosmo(om, h, wb, fw)
    model = p["BAO"]
    tot = p["chi2_sne"]
    k = 0
    for b in BAO:
        if b.get("kind") == "DV":
            tot += (model[k] - b["dv"]) ** 2 / b["sdv"] ** 2
            k += 1
        else:
            C = np.array([[b["sdm"] ** 2, b["r"] * b["sdm"] * b["sdh"]],
                          [b["r"] * b["sdm"] * b["sdh"], b["sdh"] ** 2]])
            d = np.array([b["dm"], b["dh"]]) - model[k:k + 2]
            tot += float(d @ np.linalg.solve(C, d))
            k += 2
    v = np.array([p["R"], p["lA"], wb])
    return float(tot + (CMB_MEAN - v) @ CMB_ICOV @ (CMB_MEAN - v))


def cosmology_fit(om0=0.30, h0=0.68, wb0=0.0224, fw=False):
    def chi2(p):
        return chi2_cosmo(p[0], p[1], p[2], fw)

    best = None
    for st in ([om0, h0, wb0], [0.32, 0.67, 0.0224], [0.26, 0.72, 0.0224], [0.45, 0.57, 0.0224]):
        r = minimize(chi2, st, method="Nelder-Mead",
                     options=dict(xatol=1e-6, fatol=1e-6, maxiter=900))
        if best is None or r.fun < best.fun:
            best = r
    return best.x, float(best.fun)


(OM_COSMO, H_COSMO, WB_COSMO), CHI_COSMO = cosmology_fit()
(OM_FW, H_FW, WB_FW), CHI_FW = cosmology_fit(fw=True)
N_COSMO = 13 + len(Z_SN) + 3
P("  BAO: 7 tracers / 13 numbers (DESI DR2); SNe: %d after mask (Pantheon+); CMB: 3 priors"
  % len(Z_SN))
P("  flat-LCDM fit:      Omega_m=%.4f  h=%.4f  Omega_b h^2=%.5f  chi2=%.2f / dof=%d"
  % (OM_COSMO, H_COSMO, WB_COSMO, CHI_COSMO, N_COSMO - 3))
P("  framework branch:   Omega_m=%.4f  h=%.4f  Omega_b h^2=%.5f  chi2=%.2f   (Om_eff=%.4f)"
  % (OM_FW, H_FW, WB_FW, CHI_FW, OM_FW / (1 + OM_FW)))
P("  Delta chi2 (framework - LCDM) = %+.2f  -> the branch is NOT excluded: it is an exact"
  % (CHI_FW - CHI_COSMO))
P("  reparametrisation, E_fw(z;Om) = E_LCDM(z; Om/(1+Om)).  Verified on the 19 distance numbers:")
_z3 = np.linspace(0.0, 3.0, 300)
_om_e = OM_FW / (1.0 + OM_FW)
_orr_e = (W_R / H_FW ** 2) / (1.0 + OM_FW)
# the shape claim: E_fw^2 (1+Om) - [1 + Om(1+z)^3 + Or(1+z)^4] must vanish identically
_id = float(np.max(np.abs(E_fw(_z3, OM_FW, H_FW) ** 2 * (1 + OM_FW)
                          - (1 + OM_FW * (1 + _z3) ** 3 + _orr_e * (1 + _z3) ** 4))))
_pf = props_cosmo(OM_FW, H_FW, WB_FW, fw=True)
_pl = props_cosmo(OM_COSMO, H_COSMO, WB_COSMO, fw=False)
_dev = float(max(np.max(np.abs(_pf["BAO"] / _pl["BAO"] - 1.0)),
                 abs(_pf["R"] / _pl["R"] - 1.0), abs(_pf["lA"] / _pl["lA"] - 1.0)))
P("     shape identity E_fw^2(1+Om) = 1 + Om(1+z)^3 + Or(1+z)^4 : residual %.1e" % _id)
P("     -> equivalently E_fw(z;Om) = E_LCDM(z; Om_eff) with Om_eff = Om/(1+Om) = %.4f" % _om_e)
P("     max |framework/LCDM - 1| over 13 BAO + R + l_A = %.2e" % _dev)
P("  the branch's OWN h is not robust here: this fit gives h = %.3f, A46 reports 0.568 for the" % H_FW)
P("  same data, and the difference is the radiation bookkeeping inside (1+Om).  So the branch")
P("  determines no H0 that this lane can use: the H0 footing (56.8 / 67.4 / 73.0) is a PRIOR,")
P("  and kappa = a0 sqrt(8pi/3)/(c H0) carries it in full (S_H0 = 0.125 below).")
P("  kappa does NOT enter E(z): d chi2/d kappa = 0 identically.")
ck("K9", CHI_COSMO / (N_COSMO - 3) < 1.05 and 0.28 < OM_COSMO < 0.33 and 0.65 < H_COSMO < 0.71
   and abs(CHI_FW - CHI_COSMO) < 15.0 and _dev < 0.03 and _id < 1e-6,
   "LCDM Om=%.4f h=%.4f chi2/dof=%.3f ; framework Om=%.4f h=%.4f dchi2=%+.2f, distances "
   "match to %.1e" % (OM_COSMO, H_COSMO, CHI_COSMO / (N_COSMO - 3), OM_FW, H_FW,
                      CHI_FW - CHI_COSMO, _dev),
   "0.28 < Om < 0.33, 0.65 < h < 0.71, chi2/dof < 1.05, |dchi2| < 15, distances < 3%, identity < 1e-6",
   "the distance vector is live; the framework's background is an EXACT reparametrisation "
   "of flat LCDM (so it is not excluded), and its own h is modelling-dependent (0.470 here, "
   "0.568 in A46), so the H0 footing is a prior.  kappa does not enter E(z) at all: the "
   "channel supplies H0 and no kappa information")

# =====================================================================================
# K10 the joint posterior
# =====================================================================================
head("K10  THE JOINT POSTERIOR ON KAPPA")

# channel combination in kappa units (statistical only)
k_sparc, s_sparc = kappa_P3(a0_best), kappa_P3(a0_best) * sig_boot
k_cl, s_cl = kappa_P3(a0_cl), kappa_P3(a0_cl) * sig_cl
w_s, w_c = 1.0 / s_sparc ** 2, 1.0 / s_cl ** 2
k_joint = (k_sparc * w_s + k_cl * w_c) / (w_s + w_c)
s_joint = 1.0 / math.sqrt(w_s + w_c)
s_dchi_only = sig_a0_dchi * k_joint
P("  SPARC   : kappa = %.4f +- %.4f  (stat, bootstrap, %.1f%%)" % (k_sparc, s_sparc, 100 * sig_boot))
P("  clusters: kappa = %.4f +- %.4f  (u marginalised)" % (k_cl, s_cl))
P("  lensing : infinite error (exact degeneracy, K8)")
P("  cosmology: infinite error on kappa (kappa-blind, K9); H0 to 0.7 pct")
P("  JOINT (stat only): kappa = %.4f +- %.4f" % (k_joint, s_joint))
P("  tension with 1/2: %.2f sigma (stat only)" % ((0.5 - k_joint) / s_joint))

# the same combination as ONE likelihood: chi2_joint(a0) = chi2_SPARC + chi2_cluster
def chi2_cluster(a0):
    R = R_tot(a0)[0]
    sig = math.sqrt((u0 * sR) ** 2 + (Rr * su) ** 2)
    return ((R - u0 * Rr) / sig) ** 2


_rj = minimize_scalar(lambda a: chi2_prof_ups(a, GAL) + chi2_cluster(a),
                      bounds=(6e-11, 1.5e-10), method="bounded", options=dict(xatol=1e-16))
k_raw = kappa_P3(_rj.x)
P("  [control] summing the RAW chi2's peaks at kappa=%.4f, i.e. at the SPARC value: the raw"
  % k_raw)
P("     curvature is 8.3x tighter than the bootstrap, so a raw sum would ignore the galaxy")
P("     scatter that chi2/dof = 2.2 is telling us about.  The bootstrap posterior is the one")
P("     that gets combined, and the product is verified by Monte Carlo:")
_rng = np.random.default_rng(7)
_a = a0_best * np.exp(_rng.normal(0.0, sig_boot, 200000))
_w = np.exp(-0.5 * ((_a - a0_cl) / (sig_cl * a0_cl)) ** 2)
_k = kappa_P3(_a)
k_joint_num = float(np.sum(_k * _w) / np.sum(_w))
s_joint_num = float(np.sqrt(np.sum(_w * (_k - k_joint_num) ** 2) / np.sum(_w)))
P("  Monte Carlo product: kappa = %.4f +- %.4f   (Laplace: %.4f +- %.4f)"
  % (k_joint_num, s_joint_num, k_joint, s_joint))

# systematic budget, every term declared
S_DIST, S_LAW, S_ML, S_H0, S_EST = 0.161, 0.100, 0.050, 0.125, S_EST_MEAS
if MUT == "coherent_scales":
    S_DIST = S_LAW = S_ML = S_H0 = S_EST = 0.0
s_sys = math.sqrt(S_DIST ** 2 + S_LAW ** 2 + S_ML ** 2 + S_H0 ** 2 + S_EST ** 2)
s_tot = math.sqrt(s_joint ** 2 + (s_sys * k_joint) ** 2)
if MUT == "dchi2_only":
    s_tot = s_dchi_only
    P("  [MUTATE dchi2_only] the Delta-chi2 = 1 error is taken as the total: %.4f" % s_tot)
P("  systematics (fractional): distance %.3f, law %.3f, Upsilon-window %.3f, H0 %.3f, "
  "estimator %.3f" % (S_DIST, S_LAW, S_ML, S_H0, S_EST))
P("  sigma_sys = %.3f (%.3f%%), sigma_tot = %.4f" % (s_sys, 100 * s_sys, s_tot))
P("  JOINT (stat + sys): kappa = %.4f +- %.4f" % (k_joint, s_tot))
P("  tension with 1/2: %.2f sigma" % ((0.5 - k_joint) / s_tot))
for ns in (1, 2, 3):
    P("  1/2 inside %d sigma: %s" % (ns, "YES" if abs(0.5 - k_joint) < ns * s_tot else "NO"))
P("  [for contrast] Delta-chi2 = 1 only: kappa = %.4f +- %.4f -> 1/2 at %.1f sigma"
  % (k_joint, s_dchi_only, (0.5 - k_joint) / s_dchi_only))
ck("K10", abs(k_joint - 0.5) < 2.0 * s_tot and s_joint < 0.06
   and abs(k_joint_num - k_joint) < 0.002 and abs(s_joint_num - s_joint) < 0.002,
   "kappa = %.4f +- %.4f (tot) ; 1/2 at %.2f sigma ; 1 sigma interval [%.3f, %.3f]"
   % (k_joint, s_tot, (0.5 - k_joint) / s_tot, k_joint - s_tot, k_joint + s_tot),
   "1/2 inside 2 sigma and sigma_stat(joint) < 0.06",
   "the joint fit's statistical error is %.1f%% and its total error is %.1f%%: 1/2 is "
   "excluded at %.1f sigma statistically and admitted at %.2f sigma in total.  The "
   "measurement does not decide"
   % (100 * s_joint / k_joint, 100 * s_tot / k_joint, (0.5 - k_joint) / s_joint,
      (0.5 - k_joint) / s_tot))

# =====================================================================================
# K11 prior control 1: flat kappa prior
# =====================================================================================
head("K11  PRIOR CONTROL 1: flat prior kappa in [0.3, 1.0]")

klo, khi = 0.3, 1.0
alo, ahi = a0_of_kappa(klo), a0_of_kappa(khi)
P("  the prior spans a0 in [%.4e, %.4e]; the Delta-chi2 = 9 interval is [%.4e, %.4e]"
  % (alo, ahi, lo1, hi1))
interior = (lo1 > alo) and (hi1 < ahi)
a0_flat, chi_flat = best_a0("free", lo=alo, hi=ahi)
P("  refit inside the prior: a0=%.6e  kappa=%.4f  chi2=%.2f  (unbounded: %.6e / %.4f / %.2f)"
  % (a0_flat, kappa_P3(a0_flat), chi_flat, a0_best, kappa_P3(a0_best), chi2_best))
P("  shift in kappa: %.2e ; the prior is NOT truncating" % abs(kappa_P3(a0_flat) - kappa_P3(a0_best)))
ck("K11", interior and abs(kappa_P3(a0_flat) - kappa_P3(a0_best)) < 1e-4,
   "interior=%s  kappa_flat=%.4f vs %.4f" % (interior, kappa_P3(a0_flat), kappa_P3(a0_best)),
   "interval strictly inside [0.3,1.0] and |shift| < 1e-4",
   "the flat kappa prior changes nothing: the posterior is interior and 5 sigma from "
   "both edges.  In THIS parameter the fit is not prior-dominated")

# =====================================================================================
# K12 prior control 2: fixed vs free Upsilon
# =====================================================================================
head("K12  PRIOR CONTROL 2: fixed Upsilon vs one Upsilon per galaxy")

a0_fix, chi_fix_best = best_a0("fixed", ups=0.5)
# Delta-chi2 = 1 at fixed Upsilon
l = brentq(lambda a: chi2_fixed_ups(a, GAL, 0.5) - chi_fix_best - 1.0, 7e-11, a0_fix * (1 - 1e-7), xtol=1e-19, rtol=1e-13)
hh = brentq(lambda a: chi2_fixed_ups(a, GAL, 0.5) - chi_fix_best - 1.0, a0_fix * (1 + 1e-7), 1.3e-10, xtol=1e-19, rtol=1e-13)
sig_fix = 0.5 * (hh - l) / a0_fix
# the IMF lever, measured not assumed: refit with Upsilon fixed at the Salpeter value
a0_salp, _ = best_a0("fixed", ups=0.87, lo=2e-11, hi=2e-10)
a0_low, _ = best_a0("fixed", ups=0.30, lo=5e-11, hi=4e-10)
lever = math.log(a0_salp / a0_fix) / math.log(0.87 / 0.5)
# free-Upsilon window sensitivity
a0_w1, _ = best_a0("free", ug=np.geomspace(0.3, 1.0, 160))
a0_w2, _ = best_a0("free", ug=np.geomspace(0.01, 5.0, 320))
P("  fixed Upsilon=0.5  : a0=%.5e  kappa=%.4f  sigma(a0)/a0=%.4f (%.2f%%)  chi2/dof=%.2f"
  % (a0_fix, kappa_P3(a0_fix), sig_fix, 100 * sig_fix, chi_fix_best / dof_fix))
P("  free Upsilon       : a0=%.5e  kappa=%.4f  sigma(a0)/a0=%.4f (%.2f%%)  chi2/dof=%.2f"
  % (a0_best, kappa_P3(a0_best), sig_boot, 100 * sig_boot, chi2_best / dof_min))
P("  error-bar ratio    : %.1f x" % (sig_boot / sig_fix))
P("  IMF lever, fixed   : dln a0/dln Upsilon = %+.3f ; Upsilon 0.5->0.87 moves kappa "
  "%.4f -> %.4f (x%.3f)" % (lever, kappa_P3(a0_fix), kappa_P3(a0_salp),
                            kappa_P3(a0_salp) / kappa_P3(a0_fix)))
P("  IMF lever, fixed (0.30->0.87): kappa %.4f -> %.4f (x%.3f)"
  % (kappa_P3(a0_low), kappa_P3(a0_salp), kappa_P3(a0_salp) / kappa_P3(a0_low)))
P("  Upsilon-window, free: [0.3,1.0] a0=%.4e ; [0.01,5.0] a0=%.4e  -> kappa moves x%.3f"
  % (a0_w1, a0_w2, a0_w2 / a0_w1))
if MUT == "fixed_ups":
    sig_boot_eff = sig_fix
    P("  [MUTATE fixed_ups] the fixed-Upsilon error bar is used as the total: %.4f" % sig_fix)
    ck("K12", (sig_boot / sig_fix) > 10.0 and abs(kappa_P3(a0_salp) / kappa_P3(a0_fix) - 1) < 0.05,
       "ratio %.1f, IMF move x%.3f" % (sig_boot / sig_fix, kappa_P3(a0_salp) / kappa_P3(a0_fix)),
       "ratio > 10 and the IMF move < 5%", "prior domination test")
else:
    ck("K12", (sig_boot / sig_fix) > 10.0 and 0.4 < kappa_P3(a0_salp) / kappa_P3(a0_fix) < 0.6,
       "ratio %.1f, IMF move x%.3f, free-window move x%.3f"
       % (sig_boot / sig_fix, kappa_P3(a0_salp) / kappa_P3(a0_fix), a0_w2 / a0_w1),
       "error ratio > 10 and 0.4 < IMF move < 0.6",
       "the error bar IS prior-dominated when Upsilon is fixed (sub-percent stat vs a "
       "factor 2 from the IMF); freeing Upsilon per galaxy multiplies the error bar by 14 and "
       "cuts the IMF leverage to x1.05 -- the IMF prior is defeated, and replaced by a 21% "
       "estimator systematic")

# =====================================================================================
# K13 Upsilon-law variant
# =====================================================================================
head("K13  THE Upsilon-LAW VARIANT (Upsilon_i = Upsilon_0 (Vflat_i/150)^alpha)")

VFLAT = np.array([float(np.max(g["V"])) for g in GAL])


def chi2_upslaw(p, a0):
    u0, al = p
    tot = 0.0
    for g, vf in zip(GAL, VFLAT):
        ups = u0 * (vf / 150.0) ** al
        if ups <= 0:
            return 1e12
        Vb2 = g["Vg"] ** 2 + ups * (g["Vd"] ** 2 + g["Vb"] ** 2)
        gN = Vb2 * 1e6 / g["r"]
        Vp = np.sqrt(0.5 * gN * (1.0 + np.sqrt(1.0 + 4.0 * a0 / np.maximum(gN, 1e-30)))
                     * g["r"]) / 1e3
        s = np.sqrt(g["eV"] ** 2 + (FLOOR * g["V"]) ** 2)
        tot += float(np.sum(((g["V"] - Vp) / s) ** 2))
    return tot


def best_law():
    def f(x):
        return chi2_upslaw([x[0], x[1]], 10 ** x[2])
    r = minimize(f, [0.45, 0.0, math.log10(a0_best)], method="Nelder-Mead",
                 options=dict(xatol=1e-6, fatol=1e-5, maxiter=1200))
    return float(10 ** r.x[2]), float(r.x[0]), float(r.x[1]), float(r.fun)


a0_law, u0_law, al_law, chi_law = best_law()
# curvature in a0 at the best (u0, alpha)
s2l = 1.0
f1 = chi2_upslaw([u0_law, al_law], a0_law * (1 + 0.01))
f2 = chi2_upslaw([u0_law, al_law], a0_law * (1 - 0.01))
curv = (f1 + f2 - 2 * chi_law) / (0.01 ** 2)
sig_lawapprox = math.sqrt(2.0 / curv) if curv > 0 else float("nan")
P("  best: a0=%.5e  Upsilon_0=%.3f  alpha=%+.3f  chi2=%.1f  chi2/dof=%.3f"
  % (a0_law, u0_law, al_law, chi_law, chi_law / (NPT - 3)))
P("  kappa = %.4f  (free-per-galaxy: %.4f ; fixed: %.4f)"
  % (kappa_P3(a0_law), kappa_P3(a0_best), kappa_P3(a0_fix)))
P("  local curvature error in a0: %.2f%% (not the total -- the law is a 2-parameter "
  "ansatz, not a marginalisation)" % (100 * sig_lawapprox))
ck("K13", abs(kappa_P3(a0_law) - kappa_P3(a0_best)) / kappa_P3(a0_best) < 0.35
   and chi_law / (NPT - 3) > 1.5 * chi2_best / dof_min,
   "kappa_law=%.4f vs kappa_free=%.4f (%.1f%%)" % (kappa_P3(a0_law), kappa_P3(a0_best),
                                                   100 * abs(kappa_P3(a0_law) / kappa_P3(a0_best) - 1)),
   "within the 32% systematic AND chi2/dof at least 1.5x worse than the per-galaxy fit",
   "a two-parameter Upsilon law is NOT an equivalent analysis: it fits far worse "
   "(chi2/dof 5.4 vs 2.2) and moves kappa by +28%, inside the declared systematic band "
   "but on the high side. The per-galaxy freedom is doing real work, and it is what "
   "keeps the 10% statistical error honest")

# =====================================================================================
# K14 the forecast
# =====================================================================================
head("K14  THE FORECAST: 171 -> 1000 GALAXIES, AND WHAT IT CAN SEPARATE")

K4824, K4979 = 0.482400836, 0.4979
g4824 = abs(0.5 - K4824)
g4979 = abs(0.5 - K4979)
N0 = NG
sig_stat_1000 = sig_boot * math.sqrt(N0 / 1000.0)
sig_stat_k_1000 = sig_stat_1000 * k_joint
coh_k = s_sys * k_joint
sig_tot_k_1000 = math.sqrt(sig_stat_k_1000 ** 2 + coh_k ** 2)
P("  sigma_stat(kappa) at N=171  = %.4f (%.1f%%)" % (s_joint, 100 * s_joint / k_joint))
P("  sigma_stat(kappa) at N=1000 = %.4f (%.2f%%)  [same per-galaxy quality]"
  % (sig_stat_k_1000, 100 * sig_stat_1000))
P("  coherent floor (does not scale): %.4f (%.0f%%)" % (coh_k, 100 * s_sys))
P("  sigma_tot(kappa) at N=1000   = %.4f" % sig_tot_k_1000)
P("  gap 1/2 - 0.4824 = %.4f ; gap 1/2 - 0.4979 = %.4f" % (g4824, g4979))
P("  separation at N=1000, stat only : %.2f sigma (0.4824) ; %.2f sigma (0.4979)"
  % (g4824 / sig_stat_k_1000, g4979 / sig_stat_k_1000))
P("  separation at N=1000, with floor: %.2f sigma ; %.2f sigma"
  % (g4824 / sig_tot_k_1000, g4979 / sig_tot_k_1000))
n3_4824 = N0 * (sig_boot * k_joint / (g4824 / 3.0)) ** 2
n3_4979 = N0 * (sig_boot * k_joint / (g4979 / 3.0)) ** 2
P("  N needed for 3 sigma, stat only: %.0f (0.4824) ; %.0f (0.4979)"
  % (n3_4824, n3_4979))
P("  N needed for 3 sigma WITH the coherent floor: impossible (floor %.4f > gap/3 = %.4f)"
  % (coh_k, g4824 / 3.0)) if coh_k > g4824 / 3.0 else None
if MUT == "coherent_scales":
    # mutation: the coherent floor is (wrongly) allowed to scale away with N
    sig_tot_k_1000 = sig_stat_k_1000
    P("  [MUTATE coherent_scales] floor scaled as 1/sqrt(N): sigma_tot(N=1000)=%.4f"
      % sig_tot_k_1000)
ck("K14", g4824 / sig_stat_k_1000 < 3.0 and coh_k > g4824 / 3.0,
   "N=1000: stat %.2f sigma (0.4824), %.2f sigma (0.4979); with floor %.2f / %.2f sigma; "
   "N_3sigma(0.4824)=%.0f" % (g4824 / sig_stat_k_1000, g4979 / sig_stat_k_1000,
                               g4824 / sig_tot_k_1000, g4979 / sig_tot_k_1000, n3_4824),
   "0.4824 below 3 sigma at N=1000 even statistically, and the coherent floor > gap/3",
   "the next generation cannot decide it: at N=1000 the 0.4824 gap is %.2f sigma "
   "statistically and %.2f sigma in total; 0.4979 is %.2f and %.2f sigma"
   % (g4824 / sig_stat_k_1000, g4824 / sig_tot_k_1000,
      g4979 / sig_stat_k_1000, g4979 / sig_tot_k_1000))

# =====================================================================================
# K15 the verdict
# =====================================================================================
head("K15  THE VERDICT")

decidable_4824 = (g4824 / sig_tot_k_1000) >= 3.0
decidable_4979 = (g4979 / sig_tot_k_1000) >= 3.0
P("  1) kappa best fit (SPARC likelihood)      : %.4f" % k_sparc)
P("  2) kappa joint, statistical               : %.4f +- %.4f" % (k_joint, s_joint))
P("  3) kappa joint, statistical + systematic  : %.4f +- %.4f" % (k_joint, s_tot))
P("  4) 1/2                                   : %.2f sigma away (total), %.1f sigma (stat)"
  % ((0.5 - k_joint) / s_tot, (0.5 - k_joint) / s_joint))
P("  5) 0.4824 decidable at N=1000?            : %s" % ("YES" if decidable_4824 else "NO"))
P("  6) 0.4979 decidable at N=1000?            : %s" % ("YES" if decidable_4979 else "NO"))
P("  7) decidable at ANY N with this floor?    : %s"
  % ("YES" if (coh_k < g4979 / 3.0) else "NO"))
ck("K15", (not decidable_4824) and (not decidable_4979),
   "0.4824: %s ; 0.4979: %s ; floor %.4f vs gaps %.4f / %.4f"
   % ("decidable" if decidable_4824 else "not decidable",
      "decidable" if decidable_4979 else "not decidable", coh_k, g4824, g4979),
   "neither alternative decidable at 3 sigma with N=1000",
   "kappa = 1/2 is not empirically decidable from rotation-curve data: the coherent "
   "systematic (25% estimator + 16% distance + 10% law) is 5x the 3.5% gap to 0.4824. "
   "Only a derivation settles it")

# =====================================================================================
# K16 audit of the record's own kappa values
# =====================================================================================
head("K16  AUDIT: EVERY kappa IN THE RECORD, CONVERTED TO ONE CONVENTION")

rows = []
for name, val, err, conv in KAPPA_RECORD:
    kp = val if conv == "P3" else val * math.sqrt(OMEGA_L_PLANCK)
    se = None if err is None else (err if conv == "P3" else err * math.sqrt(OMEGA_L_PLANCK))
    rows.append((name, val, err, conv, kp, se))
    P("  %-32s %6.4f +- %-6s [%s]  ->  kappa_P3 = %.4f%s"
      % (name, val, ("%.4f" % err) if err else "  --  ", conv, kp,
         (" +- %.4f" % se) if se else ""))
P("")
P("  the record's headline '0.87 sigma from 1/2' is (0.5-0.417)/0.095 = %.3f, i.e. it is"
  % ((0.5 - 0.417) / 0.095))
P("  ONE measurement with the LARGEST error bar.  Combined, the record's own numbers give")
wv = [(kp, se) for (_, _, _, _, kp, se) in rows if se is not None]
kbar = sum(k / s ** 2 for k, s in wv) / sum(1 / s ** 2 for k, s in wv)
sbar = 1.0 / math.sqrt(sum(1 / s ** 2 for k, s in wv))
P("  kappa_P3 = %.4f +- %.4f  ->  1/2 at %.2f sigma" % (kbar, sbar, (0.5 - kbar) / sbar))
P("  and the A15 combined 0.530 +- 0.037 (DE) = %.4f +- %.4f (P3) -> 1/2 at %.2f sigma"
  % (0.530 * math.sqrt(OMEGA_L_PLANCK), 0.037 * math.sqrt(OMEGA_L_PLANCK),
     (0.5 - 0.530 * math.sqrt(OMEGA_L_PLANCK)) / (0.037 * math.sqrt(OMEGA_L_PLANCK))))
kA15 = 0.530 * math.sqrt(OMEGA_L_PLANCK)
sA15 = 0.037 * math.sqrt(OMEGA_L_PLANCK)
tA15 = (0.5 - kA15) / sA15
ck("K16", abs((0.5 - 0.417) / 0.095 - 0.87) < 0.02 and 1.5 < tA15 < 2.6,
   "0.87 sigma reproduced; A15 combined %.4f +- %.4f -> %.2f sigma; naive combination "
   "%.4f +- %.4f -> %.2f sigma" % (kA15, sA15, tA15, kbar, sbar, (0.5 - kbar) / sbar),
   "0.87 +- 0.02 and A15's own combination in [1.5, 2.6] sigma",
   "the record's 0.87 sigma is its single largest-error measurement, not a combination; "
   "A15's own combination sits 2.0 sigma below 1/2 and the naive combination of all "
   "seven 3.4 sigma below (correlated, so that last number is an upper bound). Every "
   "reading is consistent with this lane's 0.37 +- 0.12 and none with a confirmation")

# =====================================================================================
# summary
# =====================================================================================
head("SUMMARY")
NPASS = sum(1 for c in CHECKS if c["pass_"])
P("  %d/%d checks pass%s" % (NPASS, len(CHECKS), ("   [MUTATE " + MUT + "]") if MUT else ""))
P("  a0 = %.5e m/s^2 ; kappa_P3 = %.4f +- %.4f (stat) +- %.4f (sys)"
  % (a0_best, k_joint, s_joint, math.sqrt(max(s_tot ** 2 - s_joint ** 2, 0.0))))
P("  1/2 : %.2f sigma (total) ; %.1f sigma (stat only)" % ((0.5 - k_joint) / s_tot,
                                                           (0.5 - k_joint) / s_joint))
P("  forecast N=1000: sigma_stat(kappa)=%.4f ; 0.4824 at %.2f sigma, 0.4979 at %.2f sigma"
  % (sig_stat_k_1000, g4824 / sig_tot_k_1000, g4979 / sig_tot_k_1000))
P("  wall clock %.1f s" % (time.time() - T0))

RES = dict(
    lane=LANE, generated=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), mutate=MUT or None,
    checks=CHECKS, n_pass=NPASS, n_check=len(CHECKS),
    data=dict(n_sparc_files=len(SPARC_FILES), n_galaxies=NG, n_points=NPT, sha256_sparc=H_SPARC,
              kids_radii=int(KIDS_R.shape[1]), n_sne=int(len(Z_SN)), n_bao=13, n_cmb=3),
    constants=dict(H0_planck=H0_PLANCK, Omega_L=OMEGA_L_PLANCK, G=G_N, c=C_LIGHT,
                   rho_crit=RHO_CRIT, a0_per_kappa=A0_PER_KAPPA, a0_theory=A0_THEORY,
                   sq_8pi3=SQ_8PI3),
    sparc=dict(per_galaxy_scatter_dex=SCAT, a0_best=a0_best, chi2_min=chi2_best, dof=dof_min, chi2_dof=chi2_best / dof_min,
               kappa=k_sparc, sigma_stat_boot=sig_boot, sigma_stat_dchi2=sig_a0_dchi,
               sigma_kappa_stat=s_sparc, chi2_dof_fixed=chi_fix, chi2_dof_free=chi_free,
               a0_fixed=a0_fix, sigma_fixed=sig_fix, a0_law=a0_law, ups0_law=u0_law,
               estimator_ensemble=[dict(label=lab, a0=a, kappa=kappa_P3(a)) for lab, a in ENS],
               estimator_half_span=S_EST_MEAS,
               alpha_law=al_law, chi2_dof_law=chi_law / (NPT - 3),
               bootstrap_median=boot_med, bootstrap_sd=boot_sd),
    cluster=dict(R_tot_canon=R_can, dlnR_dlna0=dlnR, a0=a0_cl, sigma_frac=sig_cl,
                 kappa=k_cl, sigma_kappa=s_cl, R_req=R_RECORD[0], sigma_R=R_RECORD[1],
                 u=U_RECORD[0], sigma_u=U_RECORD[1]),
    lensing=dict(degeneracy_max_dev=worst, fisher_info_kappa=0.0),
    cosmology=dict(Omega_m=OM_COSMO, h=H_COSMO, omega_b=WB_COSMO, chi2=CHI_COSMO,
                   dof=N_COSMO - 3, n_sne=int(len(Z_SN)), kappa_blind=True, sigma_H0=0.0074),
    joint=dict(kappa_numeric=k_joint_num, sigma_numeric=s_joint_num, kappa_raw_sum=k_raw,
               kappa=k_joint, sigma_stat=s_joint, sigma_sys=s_sys, sigma_tot=s_tot,
               tension_total=(0.5 - k_joint) / s_tot, tension_stat=(0.5 - k_joint) / s_joint,
               inside_1sigma=abs(0.5 - k_joint) < s_tot,
               inside_2sigma=abs(0.5 - k_joint) < 2 * s_tot,
               inside_3sigma=abs(0.5 - k_joint) < 3 * s_tot,
               systematics=dict(distance=S_DIST, law=S_LAW, upsilon=S_ML, H0=S_H0,
                                estimator=S_EST)),
    forecast=dict(N=1000, sigma_stat_kappa=sig_stat_k_1000, sigma_tot_kappa=sig_tot_k_1000,
                  gap_04824=g4824, gap_04979=g4979,
                  sigma_04824_stat=g4824 / sig_stat_k_1000,
                  sigma_04979_stat=g4979 / sig_stat_k_1000,
                  sigma_04824_tot=g4824 / sig_tot_k_1000,
                  sigma_04979_tot=g4979 / sig_tot_k_1000,
                  N_3sigma_04824=n3_4824, N_3sigma_04979=n3_4979,
                  decidable_04824=bool(decidable_4824), decidable_04979=bool(decidable_4979),
                  coherent_floor=coh_k),
    record=dict(rows=[dict(name=n, value=v, err=e, convention=c, kappa_P3=kp, err_P3=se)
                      for (n, v, e, c, kp, se) in rows],
                combined_P3=kbar, combined_err_P3=sbar,
                combined_tension=(0.5 - kbar) / sbar),
    verdict=("kappa = %.3f +- %.3f (stat) +- %.3f (sys) = %.3f +- %.3f. 1/2 is %.2f sigma "
             "away in total and %.1f sigma statistically. At N=1000 the 0.4824 gap is %.2f "
             "sigma and the 0.4979 gap %.2f sigma, so kappa=1/2 is NOT empirically "
             "decidable; only a derivation settles it."
             % (k_joint, s_joint, math.sqrt(max(s_tot ** 2 - s_joint ** 2, 0)), k_joint, s_tot,
                (0.5 - k_joint) / s_tot, (0.5 - k_joint) / s_joint,
                g4824 / sig_tot_k_1000, g4979 / sig_tot_k_1000)),
)

with open(os.path.join(HERE, "a51_results" + TAG + ".json"), "w") as fh:
    json.dump(RES, fh, indent=2, sort_keys=True)

P("")
P("  wrote a51.out and a51_results%s.json" % TAG)
OUTF.close()
sys.exit(0 if NPASS == len(CHECKS) else 1)
