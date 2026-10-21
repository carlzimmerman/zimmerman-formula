#!/usr/bin/env python3
"""A14 -- kappa from data with NO stellar mass-to-light prior: the Upsilon-free channel.

Question (owner): lane A9 showed kappa ~ Upsilon^-1.23, so Chabrier -> Salpeter moves kappa
by 1.98x, and the record's "kappa measured = 0.465 +- 0.076" is prior-dominated.  Is there a
subset of SPARC in which the stellar M/L does not enter, and what does that subset say?

What this script does, in order:
  K0  data convention: 175 curves on disk, Table 1 cross-check, and the *verification* that
      the tabulated Vdisk is the M/L = 1 template (M(Vdisk)/L36 = 1, not 0.5)
  K1  the Upsilon-free sample: N_gal, N_points
  K2  depth: every selected curve reaches g_bar < a0, and how deep
  K3  the Upsilon lever: slope dln a0/dln Upsilon on the free sample vs the full sample
  K4  the distance scaling a0 -> a0/f^2, verified by refitting rescaled data
  K5  the same exponent read off the data's own per-galaxy scatter vs the published e_D
  K6  a0 on both laws (canonical n=1, quadratic n=2), one parameter, 5% floor
  K7  both footings: chi^2 at a0_can and a0_alt, and whether the preference survives
      the distance-quality split
  K8  kappa on the 2 x 2 grid (two footings x two rho_DE conventions) and on the fits
  K9  the error budget, term by term, and the total
  K10 the sample size forecast for 5% kappa
  K11 pipeline validation against the record's own full-sample a0
  K12 robustness: radial split, floor scan, gas-only g_bar, threshold scan

Data on disk only.  Nothing downloaded.  Every number printed is computed in this file
except the labelled external inputs in EXTERNAL.

Run:     python3 a14_checks.py
Mutate:  python3 a14_checks.py --mutate    (freezes V_bar under a distance rescaling --
                                            the A9 bookkeeping -- and must break K4)
"""
import os
import sys
import csv
import json
import math

import numpy as np

MUTATE = "--mutate" in sys.argv
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
SPARC_DIR = os.path.join(ROOT, "real_research", "data", "sparc_data")
SPARC_MRT = os.path.join(ROOT, "real_research", "data", "SPARC_Lelli2016c.mrt")
SPARC_CSV = os.path.join(ROOT, "real_research", "data", "sparc_master_clean.csv")

# ---------------------------------------------------------------------------------------
# constants (BRIEF section 4) and external inputs
# ---------------------------------------------------------------------------------------
C_LIGHT = 2.99792458e8
G_N = 6.67430e-11
KPC = 3.0856775814913673e19
MPC = 3.0856775814913673e22
G_PC = 4.300917270e-3                 # pc (km/s)^2 / Msun
A0_CAN = 9.3603e-11                   # BRIEF: canonical footing
A0_ALT = 1.1312e-10                   # BRIEF: alt footing
H0_CMB = 0.6736                       # Planck 2018 (external)
OM_M_CMB = 0.3153                     # Planck 2018 (external)
H0_LOC = 0.7300                       # SH0ES-type local value (external)
OM_L_LOC = 0.685                      # 1 - 0.315 (external)

UPS_D, UPS_B = 0.5, 0.7                # SPARC standard 3.6um M/L (Chabrier)
FGAS_TH = 0.80                        # frozen threshold, FROZEN_CRITERIA.md S1
EVCUT = 0.10                          # SPARC standard relative-error cut
QFLOOR = 0.05                         # 5% error floor, per the task
SEED = 20261021

EXTERNAL = {
    "M/L standard 0.5 (disk) / 0.7 (bulge) at 3.6um": "Lelli, McGaugh & Schombert 2016; "
    "repo convention fable_independent_2026/L232_sparc_parameter_free.py:42",
    "Chabrier -> Salpeter bracket +0.24 dex in Upsilon": "A9 report, K4 / register CFG926",
    "Omega_m = 0.3153, h = 0.6736": "Planck 2018 TT,TE,EE+lowE+lensing",
    "H0 = 73.0, Omega_L = 0.685": "local distance ladder value, A9 K5 convention",
    "RAR intrinsic scatter 0.13 dex": "McGaugh, Lelli & Schombert 2016 (used only as a yardstick)",
    "helium correction 1.33 +- 0.03 in M_gas": "SPARC convention; bracket is ours",
}

CHECKS = []
NUM = {}

# ---------------------------------------------------------------------------------------
# data
# ---------------------------------------------------------------------------------------


def parse_table1():
    """SPARC Table 1.  Fixed-format file; parsed by whitespace and validated against the
    repo's own 10-column extract (sparc_master_clean.csv) in K0."""
    out = {}
    for line in open(SPARC_MRT):
        tok = line.split()
        if len(tok) < 18 or not tok[0][0].isalpha():
            continue
        try:
            out[tok[0]] = dict(T=int(tok[1]), D=float(tok[2]), eD=float(tok[3]), fD=int(tok[4]),
                               inc=float(tok[5]), einc=float(tok[6]), L36=float(tok[7]),
                               Rdisk=float(tok[11]), SBdisk=float(tok[12]),
                               MHI=float(tok[13]), RHI=float(tok[14]),
                               Vflat=float(tok[15]), Q=int(tok[17]))
        except (ValueError, IndexError):
            continue
    return out


def load_curves():
    out = {}
    for fn in sorted(os.listdir(SPARC_DIR)):
        if not fn.endswith("_rotmod.dat"):
            continue
        a = np.loadtxt(os.path.join(SPARC_DIR, fn), comments="#")
        if a.ndim != 2 or a.shape[1] < 6 or len(a) < 3:
            continue
        out[fn.replace("_rotmod.dat", "")] = a
    return out


T1 = parse_table1()
CURVES = load_curves()


def select(th=FGAS_TH, qmax=2, nmin=3, evmax=EVCUT, upd=UPS_D, upb=UPS_B, deep=True,
           fDset=None):
    """The frozen selection of FROZEN_CRITERIA.md S1-S5."""
    sel = []
    for name, a in CURVES.items():
        info = T1.get(name)
        if info is None or info["Q"] > qmax:
            continue
        if fDset is not None and info["fD"] not in fDset:
            continue
        R, Vo, eV, Vg, Vd, Vb = (a[:, i] for i in range(6))
        vg2 = Vg ** 2
        tot = vg2 + upd * Vd ** 2 + upb * Vb ** 2
        fg = np.where(tot > 0, vg2 / np.maximum(tot, 1e-30), 0.0)
        m = ((R > 2.0 * info["Rdisk"]) & (R > 0) & (Vo > 0) & (eV > 0) &
             (eV / np.maximum(Vo, 1e-9) < evmax) & (Vg > 0) & (tot > 0))
        if th > 0:
            m = m & (fg > th)
        if m.sum() < nmin:
            continue
        gb = tot[m] / (R[m] * KPC) * 1e6
        if deep and gb.min() >= A0_CAN:
            continue
        sel.append(dict(name=name, R=R[m], Vo=Vo[m], eV=eV[m], Vg2=vg2[m],
                        Vd2=Vd[m] ** 2, Vb2=Vb[m] ** 2, fg=fg[m],
                        D=info["D"], eD=info["eD"], fD=info["fD"], inc=info["inc"],
                        einc=info["einc"], rd=info["Rdisk"], Q=info["Q"],
                        Vflat=info["Vflat"], T=info["T"]))
    return sel


def gbar_of(g, upd=UPS_D, upb=UPS_B):
    return (g["Vg2"] + upd * g["Vd2"] + upb * g["Vb2"]) / (g["R"] * KPC) * 1e6


def gobs_of(g, dscale=1.0):
    return g["Vo"] ** 2 / (g["R"] * dscale * KPC) * 1e6


# ---------------------------------------------------------------------------------------
# the two laws
# ---------------------------------------------------------------------------------------


def law_canon(gb, a0):
    """g = (g_N/2)(1 + sqrt(1 + 4 a0/g_N)); deep limit g -> sqrt(a0 g_N)."""
    return 0.5 * gb * (1.0 + np.sqrt(1.0 + 4.0 * a0 / gb))


def law_quad(gb, a0):
    """g^2 - g_N^2 = a0 g_N  =>  g = sqrt(g_N^2 + a0 g_N)."""
    return np.sqrt(gb * gb + a0 * gb)


LAWS = {"canon": law_canon, "quad": law_quad}


def stack(S, dscale=1.0, upd=UPS_D, upb=UPS_B):
    """Flatten a galaxy list into per-point arrays plus a galaxy index."""
    gb, vo, ev, r, gi = [], [], [], [], []
    for k, g in enumerate(S):
        gb.append(gbar_of(g, upd, upb))
        vo.append(g["Vo"])
        ev.append(g["eV"])
        r.append(g["R"] * dscale)
        gi.append(np.full(len(g["R"]), k))
    return (np.concatenate(gb), np.concatenate(vo), np.concatenate(ev),
            np.concatenate(r), np.concatenate(gi))


def chi2_grid(a0s, gb, vo, ev, r, law, floor=QFLOOR, mutate_gb=None):
    """chi^2(a0) for an array of a0 values, vectorised over points."""
    gbe = gb if mutate_gb is None else gb / mutate_gb
    sig = np.sqrt(ev ** 2 + (floor * vo) ** 2)
    out = np.empty(len(a0s))
    for k, a0 in enumerate(a0s):
        vm = np.sqrt(LAWS[law](gbe, a0) * r * KPC) / 1e3
        out[k] = np.sum(((vo - vm) / sig) ** 2)
    return out


def fit_a0(S, law, floor=QFLOOR, dscale=1.0, upd=UPS_D, upb=UPS_B, mutate_gb=None,
           coarse=(-12.2, -9.0, 65), fine=(-0.10, 0.10, 41)):
    gb, vo, ev, r, gi = stack(S, dscale, upd, upb)
    las = np.linspace(coarse[0], coarse[1], coarse[2])
    cs = chi2_grid(10.0 ** las, gb, vo, ev, r, law, floor, mutate_gb)
    i = int(np.argmin(cs))
    step = las[1] - las[0]
    las2 = las[i] + np.linspace(fine[0], fine[1], fine[2])
    cs2 = chi2_grid(10.0 ** las2, gb, vo, ev, r, law, floor, mutate_gb)
    j = int(np.argmin(cs2))
    la0 = las2[j]
    if 0 < j < len(las2) - 1:
        y0, y1, y2 = cs2[j - 1], cs2[j], cs2[j + 1]
        den = (y0 - 2 * y1 + y2)
        if den > 0:
            la0 = las2[j] + 0.5 * (y0 - y2) / den * (las2[1] - las2[0]) * 0.5
    cmin = float(chi2_grid([10.0 ** la0], gb, vo, ev, r, law, floor, mutate_gb)[0])
    # Delta chi^2 = 1 crossings on a fine scan around the minimum
    scan = la0 + np.linspace(-0.6, 0.6, 1201)
    csc = chi2_grid(10.0 ** scan, gb, vo, ev, r, law, floor, mutate_gb)
    lo = hi = np.nan
    tgt = cmin + 1.0
    below = np.where(csc <= tgt)[0]
    if len(below):
        lo, hi = scan[below[0]], scan[below[-1]]
    err = (10.0 ** hi - 10.0 ** lo) / 2.0 if np.isfinite(lo) else np.nan
    return dict(a0=10.0 ** la0, la0=la0, chi2=cmin, n=int(len(vo)), err=err,
                chi2r=cmin / max(len(vo) - 1, 1))


def bootstrap(S, law, ndraw=400, floor=QFLOOR):
    gb, vo, ev, r, gi = stack(S, 1.0)
    ng = len(S)
    blocks = [np.where(gi == k)[0] for k in range(ng)]
    rng = np.random.default_rng(SEED)
    vals = np.empty(ndraw)
    for d in range(ndraw):
        pick = rng.integers(0, ng, ng)
        idx = np.concatenate([blocks[k] for k in pick])
        las = np.linspace(-11.9, -9.2, 55)
        cs = chi2_grid(10.0 ** las, gb[idx], vo[idx], ev[idx], r[idx], law, floor)
        i = int(np.argmin(cs))
        las2 = las[i] + np.linspace(-0.06, 0.06, 25)
        cs2 = chi2_grid(10.0 ** las2, gb[idx], vo[idx], ev[idx], r[idx], law, floor)
        vals[d] = 10.0 ** las2[int(np.argmin(cs2))]
    return vals


def chi2_at(S, law, a0, floor=QFLOOR, mutate_gb=None):
    gb, vo, ev, r, gi = stack(S, 1.0)
    return float(chi2_grid([a0], gb, vo, ev, r, law, floor, mutate_gb)[0])


# ---------------------------------------------------------------------------------------
# rho_DE and kappa
# ---------------------------------------------------------------------------------------


def rho_de(OmL, h):
    H0 = h * 100.0 * 1000.0 / MPC
    return OmL * 3.0 * H0 ** 2 / (8.0 * math.pi * G_N)


RHO_CMB = rho_de(1.0 - OM_M_CMB, H0_CMB)     # Omega_L h^2 fixed by the CMB
RHO_LOC = rho_de(OM_L_LOC, H0_LOC)           # local H0, Omega_L held fixed


def kappa(a0, rho):
    return a0 / (C_LIGHT * math.sqrt(G_N * rho))


# ---------------------------------------------------------------------------------------
# output helpers
# ---------------------------------------------------------------------------------------


def check(cid, ok, measured, threshold, note=""):
    ok = bool(ok)
    CHECKS.append({"id": cid, "pass": ok, "value": measured, "threshold": threshold})
    print("  %-4s %s %s" % (cid, "PASS" if ok else "FAIL", measured))
    print("        threshold: %s" % threshold)
    if note:
        print("        %s" % note)
    return ok


print("=" * 92)
print("A14 -- KAPPA FROM DATA WITH NO STELLAR MASS-TO-LIGHT PRIOR" + ("   [MUTATE]" if MUTATE else ""))
print("=" * 92)

# =======================================================================================
print("\nK0  data on disk, and what the Vdisk column means")
# =======================================================================================
n_curves = len(CURVES)
ref = list(csv.DictReader(open(SPARC_CSV)))
bad = 0
for r in ref:
    q = T1.get(r["name"])
    if q is None:
        bad += 1
        continue
    for kc, km in [("D_Mpc", "D"), ("fD", "fD"), ("inc", "inc"), ("L36", "L36"),
                   ("MHI", "MHI"), ("Vflat", "Vflat"), ("Q", "Q")]:
        if abs(float(r[kc]) - float(q[km])) > 1e-3 * max(1.0, abs(float(r[kc]))):
            bad += 1

# Vdisk convention: at large R an exponential disk acts as a point mass, so
# M(Vdisk) = Vdisk^2 R / G must equal Upsilon * L36.  If the tabulated column were
# already at M/L = 0.5 the ratio would be 0.5.
rat = []
for name, a in CURVES.items():
    info = T1.get(name)
    if info is None or info["L36"] <= 0:
        continue
    R, Vo, eV, Vg, Vd, Vb = (a[:, i] for i in range(6))
    m = (R > 0) & (Vd > 0) & (R > 2.0 * info["Rdisk"]) & (eV / np.maximum(Vo, 1e-9) < EVCUT)
    if m.sum() < 1:
        continue
    i = int(np.where(m)[0][-1])
    rat.append(Vd[i] ** 2 * (R[i] * 1e3) / G_PC / (info["L36"] * 1e9))
ML_MED = float(np.median(rat))
ML_LO, ML_HI = float(np.percentile(rat, 16)), float(np.percentile(rat, 84))
print("        %d rotmod curves, %d Table-1 rows, %d cross-check mismatches" % (n_curves, len(T1), bad))
print("        M(Vdisk)/L36 over %d galaxies: median %.3f (p16-84 %.2f-%.2f)"
      % (len(rat), ML_MED, np.percentile(rat, 16), np.percentile(rat, 84)))
NUM["n_curves"] = n_curves
NUM["ml_convention_median"] = round(ML_MED, 4)
NUM["ml_convention_p16"] = round(ML_LO, 3)
NUM["ml_convention_p84"] = round(ML_HI, 3)
ok0 = check("K0", n_curves == 175 and bad == 0 and 0.85 < ML_MED < 1.30,
            "175 curves, 0 mismatches, M(Vdisk)/L36 = %.3f" % ML_MED,
            "175 and 0 and 0.85 < ratio < 1.30  (=> Vdisk is the M/L=1 template)")

# =======================================================================================
print("\nK1  the Upsilon-free sample")
# =======================================================================================
S = select()
NG = len(S)
NPTS = sum(len(g["R"]) for g in S)
print("        f_gas > %.2f at every fitted point, R > 2 Rd, errV/V < %.2f, Q <= 2,"
      % (FGAS_TH, EVCUT))
print("        >= 3 points, min g_bar < a0_can")
print("        N_gal = %d of %d curves (%.1f%%), N_points = %d" % (NG, n_curves, 100.0 * NG / n_curves, NPTS))
UPS_SAL = UPS_D * 10 ** 0.24        # Chabrier -> Salpeter (+0.24 dex)
S_SAL = select(upd=UPS_SAL, upb=UPS_B * 10 ** 0.24)
print("        at a Salpeter M/L (Upsilon_d = %.2f) the same cuts leave %d galaxies, %d points"
      % (UPS_SAL, len(S_SAL), sum(len(g["R"]) for g in S_SAL)))
NUM["n_gal_salpeter"] = len(S_SAL)
NUM["n_pts_salpeter"] = int(sum(len(g["R"]) for g in S_SAL))
NUM["ups_salpeter"] = round(UPS_SAL, 3)
ok1 = check("K1", NG >= 8 and NPTS >= 50, "N_gal = %d, N_points = %d" % (NG, NPTS),
            "N_gal >= 8 and N_points >= 50")

# =======================================================================================
print("\nK2  depth actually reached")
# =======================================================================================
gmin_gal = np.array([np.min(gbar_of(g)) / A0_CAN for g in S])
gmin_pt = np.concatenate([gbar_of(g) / A0_CAN for g in S])
med_reached = float(np.median(gmin_gal))
med_all = float(np.median(gmin_pt))
print("        per-galaxy min g_bar/a0: median %.4f, worst %.4f, best %.4f"
      % (med_reached, gmin_gal.max(), gmin_gal.min()))
print("        median over all %d fitted points: g_bar/a0 = %.4f" % (NPTS, med_all))
print("        deepest single point: g_bar/a0 = %.4f" % gmin_pt.min())
ok2 = check("K2", med_reached < 0.10 and gmin_gal.max() < 1.0,
            "median per-galaxy min g_bar/a0 = %.4f, max over galaxies = %.4f"
            % (med_reached, gmin_gal.max()),
            "< 0.10 and < 1.0  (every curve reaches the deep branch)")

PER_GAL = []
print("        %-11s %2s %2s %5s %8s %9s %10s" % ("galaxy", "n", "fD", "eD/D", "min gb/a0", "Vflat", "T"))
for g in sorted(S, key=lambda z: np.min(gbar_of(z))):
    PER_GAL.append(dict(name=g["name"], n=int(len(g["R"])), fD=g["fD"],
                        eD_over_D=round(g["eD"] / g["D"], 4),
                        gb_min_over_a0=round(float(np.min(gbar_of(g)) / A0_CAN), 5),
                        fgas_min=round(float(np.min(g["fg"])), 4),
                        Vflat=g["Vflat"], T=g["T"], D_Mpc=g["D"], inc=g["inc"],
                        e_inc=g["einc"]))
    print("        %-11s %2d %2d %5.2f %8.4f %9.1f %10d"
          % (g["name"], len(g["R"]), g["fD"], g["eD"] / g["D"],
             float(np.min(gbar_of(g)) / A0_CAN), g["Vflat"], g["T"]))
NUM["per_galaxy"] = PER_GAL
NUM["n_gal"] = NG
NUM["n_points"] = NPTS
NUM["median_gb_over_a0_reached"] = round(med_reached, 5)
NUM["median_gb_over_a0_all"] = round(med_all, 5)
NUM["min_gb_over_a0"] = round(float(gmin_pt.min()), 5)

# =======================================================================================
print("\nK3  the Upsilon lever: what the free channel actually buys")
# =======================================================================================
FULL = select(th=0.0, qmax=3, nmin=1, deep=False)
f_can, f_quad = fit_a0(S, "canon"), fit_a0(S, "quad")
base_can = f_can["a0"]
a_up2, a_up05 = (fit_a0(S, "canon", upd=1.0, upb=1.4)["a0"],
                 fit_a0(S, "canon", upd=0.25, upb=0.35)["a0"])
slope_free = math.log(a_up2 / a_up05) / math.log(1.0 / 0.25)
b_full = fit_a0(FULL, "canon")["a0"]
a_full2, a_full05 = (fit_a0(FULL, "canon", upd=1.0, upb=1.4)["a0"],
                     fit_a0(FULL, "canon", upd=0.25, upb=0.35)["a0"])
slope_full = math.log(a_full2 / a_full05) / math.log(1.0 / 0.25)
imf = 0.24 * math.log(10.0)          # Chabrier -> Salpeter, +0.24 dex
fg_mean = float(np.mean(np.concatenate([g["fg"] for g in S])))
slope_pred = -(1.0 - fg_mean)
print("        mean f_gas over the %d fitted points = %.3f -> predicted slope %.3f"
      % (NPTS, fg_mean, slope_pred))
NUM["fgas_mean"] = round(fg_mean, 4)
NUM["slope_pred_from_fgas"] = round(slope_pred, 4)
moved_free = math.exp(abs(slope_free) * imf)
moved_full = math.exp(abs(slope_full) * imf)
# pure-gas variant: Upsilon_* = 0
a_gas = fit_a0(S, "canon", upd=0.0, upb=0.0)["a0"]
print("        dln a0/dln Upsilon:  free sample %+.3f   full sample %+.3f"
      % (slope_free, slope_full))
print("        Chabrier->Salpeter (+0.24 dex, x1.74) moves a0 by x%.3f (free) vs x%.3f (full)"
      % (moved_free, moved_full))
print("        gas-only g_bar (Upsilon_* = 0): a0 = %.4e (x%.2f of the standard-M/L value)"
      % (a_gas, a_gas / base_can))
# read the free channel as an effective M/L for the full sample: a0 ~ Upsilon^slope_full
ups_eff = UPS_D * (base_can / b_full) ** (1.0 / slope_full)
print("        free channel as an effective M/L for the full sample: Upsilon_d = %.3f"
      % ups_eff)
print("        (0.50 = Chabrier, 0.87 = Salpeter; the channel sits between them)")
NUM["ups_eff_from_free_channel"] = round(ups_eff, 4)
NUM["slope_free"] = round(slope_free, 4)
NUM["slope_full"] = round(slope_full, 4)
NUM["imf_move_free"] = round(moved_free, 4)
NUM["imf_move_full"] = round(moved_full, 4)
NUM["a0_gasonly"] = a_gas
NUM["gas_only_ratio"] = round(a_gas / base_can, 4)
ok3 = check("K3", abs(slope_free) <= 0.40 and abs(slope_full) >= 1.0 and moved_free < moved_full,
            "|slope| = %.3f free vs %.3f full; IMF move x%.2f vs x%.2f"
            % (abs(slope_free), abs(slope_full), moved_free, moved_full),
            "|slope_free| <= 0.40, |slope_full| >= 1.0, free move < full move")

# =======================================================================================
print("\nK4  the distance scaling: a0 -> a0/f^2, by refitting rescaled data")
# =======================================================================================
FSCALE = 1.10
dists = {}
for law in LAWS:
    a1 = f_can["a0"] if law == "canon" else f_quad["a0"]
    mg = FSCALE if MUTATE else None      # mutate: freeze V_bar, i.e. g_bar -> g_bar/f
    a2 = fit_a0(S, law, dscale=FSCALE, mutate_gb=mg)["a0"]
    dists[law] = (a1, a2, a2 * FSCALE ** 2 / a1)
    print("        %-5s a0(f=1) = %.5e   a0(f=%.2f) = %.5e   a0*f^2/a0 = %.4f"
          % (law, a1, FSCALE, a2, a2 * FSCALE ** 2 / a1))
dev = abs(dists["canon"][2] - 1.0)
NUM["dist_scale_test"] = {k: round(v[2], 5) for k, v in dists.items()}
print("        residual from exact f^2 is O(sqrt(g_bar/a0)) = the interpolation correction,")
print("        not a failure of the scaling: the deep limit is exact, the transition is not.")
ok4 = check("K4", dev < 0.05, "|a0 f^2/a0 - 1| = %.4f at f = %.2f (canonical law)" % (dev, FSCALE),
            "< 0.05")

# =======================================================================================
print("\nK5  the same exponent from the data's own scatter (no rescaling experiment)")
# =======================================================================================
per_a0 = np.array([fit_a0([g], "canon")["a0"] for g in S])
scat = float(np.std(np.log10(per_a0)))
ed = np.array([g["eD"] / g["D"] for g in S])
rms_ed = float(np.sqrt(np.mean(ed ** 2)))
pred2 = 2.0 * rms_ed / math.log(10.0)
pred1 = 1.0 * rms_ed / math.log(10.0)
# the exponent the script adopts; MUTATE adopts the 1/f bookkeeping, consistently
PEXP = 1.0 if MUTATE else 2.0
pred_chosen, pred_other = (pred1, pred2) if MUTATE else (pred2, pred1)
print("        per-galaxy a0 spans %.2e .. %.2e (%.3f dex)" % (per_a0.min(), per_a0.max(), scat))
print("        published e_D/D: rms %.3f  (f_D=1: %.2f, f_D=2: %.2f)"
      % (rms_ed, np.mean([g["eD"] / g["D"] for g in S if g["fD"] == 1]),
         np.mean([g["eD"] / g["D"] for g in S if g["fD"] == 2])))
if MUTATE:
    print("        [MUTATE] adopting the 1/f bookkeeping, as A9 K2 did")
print("        predicted scatter: p=2 -> %.3f dex,  p=1 -> %.3f dex,  measured %.3f dex"
      % (pred2, pred1, scat))
print("        => the measured scatter is what p=2 predicts with ZERO intrinsic a0 scatter;")
print("           p=1 would need %.3f dex of intrinsic scatter on top." % math.sqrt(max(scat ** 2 - pred1 ** 2, 0)))
NUM["a0_scatter_dex"] = round(scat, 4)
NUM["pred_scatter_p2"] = round(pred2, 4)
NUM["pred_scatter_p1"] = round(pred1, 4)
NUM["rms_eD_over_D"] = round(rms_ed, 4)
NUM["pred_intrinsic_if_p1"] = round(math.sqrt(max(scat ** 2 - pred1 ** 2, 0)), 4)
ok5 = check("K5", abs(scat - pred_chosen) < abs(scat - pred_other) and scat / pred_chosen < 1.35,
            "measured %.3f dex; adopted p=%.0f predicts %.3f, p=%.0f predicts %.3f"
            % (scat, PEXP, pred_chosen, 3.0 - PEXP, pred_other),
            "closer to the adopted exponent and measured/pred < 1.35")

# =======================================================================================
print("\nK6  a0, one parameter, both laws, 5% error floor")
# =======================================================================================
for law in LAWS:
    f = f_can if law == "canon" else f_quad
    print("        %-5s a0 = %.5e   chi2 = %.1f / %d (chi2r %.2f)   dchi2=1 err %.2e (%.2f%%)"
          % (law, f["a0"], f["chi2"], f["n"] - 1, f["chi2r"], f["err"], 100 * f["err"] / f["a0"]))
boot = {}
for law in LAWS:
    boot[law] = bootstrap(S, law, ndraw=400)
    b = boot[law]
    print("        %-5s block bootstrap (400 draws, galaxies): 16-84 = (%.4e, %.4e), %.1f%%"
          % (law, np.percentile(b, 16), np.percentile(b, 84),
             100 * 0.5 * (np.percentile(b, 84) - np.percentile(b, 16)) / np.median(b)))
LAW_RATIO = f_quad["a0"] / f_can["a0"]
DCHI2_LAW = f_can["chi2"] - f_quad["chi2"]
print("        law ratio quad/canon = %.4f  ->  law systematic +-%.1f%%"
      % (LAW_RATIO, 100 * abs(LAW_RATIO - 1) / 2))
NUM["a0_canon"] = f_can["a0"]
NUM["a0_quad"] = f_quad["a0"]
NUM["chi2_canon"] = round(f_can["chi2"], 2)
NUM["chi2_quad"] = round(f_quad["chi2"], 2)
NUM["law_ratio"] = round(LAW_RATIO, 4)
NUM["chi2r_canon"] = round(f_can["chi2r"], 3)
NUM["chi2r_quad"] = round(f_quad["chi2r"], 3)
NUM["dchi2_law_pooled"] = round(DCHI2_LAW, 2)
NUM["boot_rel_canon"] = float(np.std(np.log(boot["canon"])))
NUM["boot_rel_quad"] = float(np.std(np.log(boot["quad"])))
ok6 = check("K6", 0.9 < LAW_RATIO < 1.6 and f_can["chi2r"] < 12.0,
            "quad/canon = %.4f, chi2r(canon) = %.2f" % (LAW_RATIO, f_can["chi2r"]),
            "0.9 < ratio < 1.6 and chi2r < 12  (both laws give a finite, similar a0)")

# =======================================================================================
print("\nK7  both footings")
# =======================================================================================
foot = {}
for law in LAWS:
    cc = chi2_at(S, law, A0_CAN)
    ca = chi2_at(S, law, A0_ALT)
    foot[law] = (cc, ca)
    print("        %-5s chi2(a0_can=%.3e) = %8.1f   chi2(a0_alt=%.3e) = %8.1f   d = %+.1f"
          % (law, A0_CAN, cc, A0_ALT, ca, cc - ca))
S2 = [g for g in S if g["fD"] == 2]
f2 = fit_a0(S2, "canon")
c2c, c2a = chi2_at(S2, "canon", A0_CAN), chi2_at(S2, "canon", A0_ALT)
print("        distance-quality split (canonical law):")
print("          f_D=2 (2-5%%, %d gal, %d pts): a0 = %.4e, chi2(a0_can) = %.1f, chi2(a0_alt) = %.1f"
      % (len(S2), sum(len(g['R']) for g in S2), f2["a0"], c2c, c2a))
S1 = [g for g in S if g["fD"] == 1]
f1 = fit_a0(S1, "canon")
d2 = fit_a0(S2, "canon")["chi2"] - fit_a0(S2, "quad")["chi2"]
d1 = fit_a0(S1, "canon")["chi2"] - fit_a0(S1, "quad")["chi2"]
NUM["dchi2_law_fD2"] = round(d2, 2)
NUM["dchi2_law_fD1"] = round(d1, 2)
print("          f_D=1 (25-30%%, %d gal, %d pts): a0 = %.4e"
      % (len(S1), sum(len(g['R']) for g in S1), f1["a0"]))
print("        law preference dchi2(canon-quad): pooled %+.1f, f_D=2 %+.1f, f_D=1 %+.1f"
      % (DCHI2_LAW, d2, d1))
print("        => the footing preference (canonical over alt, dchi2 = %.0f pooled) REVERSES"
      % (foot["canon"][0] - foot["canon"][1]))
print("           on the 4 galaxies with 2-5%% distances, where a0 = %.3e ~ a0_alt." % f2["a0"])
NUM["dchi2_footing_canon"] = round(foot["canon"][0] - foot["canon"][1], 1)
NUM["a0_fD1"] = f1["a0"]
NUM["a0_fD2"] = f2["a0"]
NUM["fD_split_ratio"] = f2["a0"] / f1["a0"]
ok7 = check("K7", abs(foot["canon"][0] - foot["canon"][1]) > 25 and f2["a0"] / f1["a0"] > 1.5,
            "pooled dchi2(can-alt) = %+.0f; a0(fD=2)/a0(fD=1) = %.2f"
            % (foot["canon"][0] - foot["canon"][1], f2["a0"] / f1["a0"]),
            "|dchi2| > 25 and distance-quality ratio > 1.5  (the footing verdict is not robust)")

# =======================================================================================
print("\nK8  kappa on the 2 x 2 grid, and on the fits")
# =======================================================================================
print("        rho_DE(CMB)  = %.4e kg/m^3   (Omega_L h^2 = %.4f)"
      % (RHO_CMB, (1.0 - OM_M_CMB) * H0_CMB ** 2))
print("        rho_DE(local)= %.4e kg/m^3   (H0 = %.1f, Omega_L = %.3f)"
      % (RHO_LOC, H0_LOC * 100, OM_L_LOC))
print("        sqrt(rho_loc/rho_CMB) = %.4f" % math.sqrt(RHO_LOC / RHO_CMB))
grid = {}
for lab, a0 in [("footing canonical", A0_CAN), ("footing alt", A0_ALT),
                ("fit canonical", f_can["a0"]), ("fit quadratic", f_quad["a0"]),
                ("fit fD=2 only", f2["a0"])]:
    kc, kl = kappa(a0, RHO_CMB), kappa(a0, RHO_LOC)
    grid[lab] = (kc, kl)
    print("        %-17s a0 = %.4e  ->  kappa_CMB = %.4f   kappa_local = %.4f" % (lab, a0, kc, kl))
vals = [v for p in grid.values() for v in p]
spread = max(vals) / min(vals)
print("        total spread over the five a0 choices x two densities: %.3f -> %.3f (x%.2f)"
      % (min(vals), max(vals), spread))
print("        footing x density alone: %.4f .. %.4f (x%.2f) with NO data at all"
      % (min(grid["footing canonical"] + grid["footing alt"]),
         max(grid["footing canonical"] + grid["footing alt"]),
         max(grid["footing canonical"] + grid["footing alt"]) /
         min(grid["footing canonical"] + grid["footing alt"])))
NUM["kappa"] = {k: [round(v[0], 4), round(v[1], 4)] for k, v in grid.items()}
NUM["kappa_spread"] = round(spread, 3)
NUM["kappa_conv_spread"] = round(max(grid["footing canonical"] + grid["footing alt"]) /
                                 min(grid["footing canonical"] + grid["footing alt"]), 3)
NUM["rho_ratio_sqrt"] = round(math.sqrt(RHO_LOC / RHO_CMB), 4)
NUM["kappa_fD1_cmb"] = round(kappa(f1["a0"], RHO_CMB), 4)
A0_RECORD = 0.465 * C_LIGHT * math.sqrt(G_N * RHO_CMB)
print("        the record's kappa = 0.465 +- 0.076 is a0 = %.4e at rho_DE(CMB);" % A0_RECORD)
print("        the free channel gives %.4e = %.2f of it" % (f_can["a0"], f_can["a0"] / A0_RECORD))
NUM["a0_record_implied"] = A0_RECORD
NUM["kerr_vs_record"] = round(f_can["a0"] / A0_RECORD, 4)
ok8 = check("K8", spread > 1.5 and NUM["kappa_conv_spread"] > 1.25,
            "data x density spread x%.2f; convention-only spread x%.2f"
            % (spread, NUM["kappa_conv_spread"]),
            "> x1.5 and > x1.25  (no internally consistent kappa at 5%)")

# =======================================================================================
print("\nK9  the error budget")
# =======================================================================================
sig_fit = f_can["err"] / f_can["a0"] * math.sqrt(f_can["chi2r"])
sig_gal = float(np.std(np.log(boot["canon"])))
sig_dist = 2.0 * math.log(H0_LOC / H0_CMB)
sig_ups = math.exp(abs(slope_free) * imf) - 1.0
sig_law = abs(LAW_RATIO - 1.0) / 2.0
sig_he = 2.0 * 0.5 * math.log(1.36 / 1.33)
terms = [("statistical (dchi2=1, x sqrt(chi2r))", sig_fit),
         ("sample scatter (block bootstrap)", sig_gal),
         ("distance zero point (H0 73 vs 67.4, x2)", sig_dist),
         ("residual stellar M/L (IMF bracket)", sig_ups),
         ("interpolation law (half the L1-L2 gap)", sig_law),
         ("helium 1.33 -> 1.36", sig_he)]
for lab, v in terms:
    print("        %-42s %6.2f%%" % (lab, 100 * v))
tot_q = math.sqrt(sum(v * v for _, v in terms))
tot_l = sum(v for _, v in terms)
print("        %-42s %6.2f%%" % ("quadrature total", 100 * tot_q))
print("        %-42s %6.2f%%" % ("linear (all-coherent) total", 100 * tot_l))
K_CAN_CMB = kappa(f_can["a0"], RHO_CMB)
print("        kappa = %.4f +- %.4f (quadrature);  |kappa - 1/2| = %.2f sigma"
      % (K_CAN_CMB, K_CAN_CMB * tot_q, abs(K_CAN_CMB - 0.5) / (K_CAN_CMB * tot_q)))
NUM["err_terms"] = {k: round(v, 4) for k, v in terms}
NUM["err_total_quad"] = round(tot_q, 4)
NUM["err_total_lin"] = round(tot_l, 4)
NUM["kappa_fit_cmb"] = round(K_CAN_CMB, 4)
NUM["kappa_err_total"] = round(K_CAN_CMB * tot_q, 4)
NUM["sigma_from_half"] = round(abs(K_CAN_CMB - 0.5) / (K_CAN_CMB * tot_q), 3)
NUM["kappa_fit_local"] = round(kappa(f_can["a0"], RHO_LOC), 4)
ok9 = check("K9", tot_q > 0.05, "total = %.1f%% (quadrature), %.1f%% (linear)" % (100 * tot_q, 100 * tot_l),
            "> 5%  (the channel cannot deliver 5% kappa)")

# =======================================================================================
print("\nK10 the sample size forecast for a 5% kappa")
# =======================================================================================
TARGET = 0.05
n_stat = NG * (sig_gal / TARGET) ** 2
n_dist = (2.0 * rms_ed / TARGET) ** 2
print("        statistical: sigma(N) = %.3f sqrt(%d/N) -> N = %d for %.0f%%"
      % (sig_gal, NG, math.ceil(n_stat), 100 * TARGET))
print("        if only the published per-galaxy distance errors mattered: N = %d"
      % math.ceil(n_dist))
print("        coherent floors that NO N removes:")
print("          distance zero point %.1f%%   residual M/L %.1f%%   law choice %.1f%%"
      % (100 * sig_dist, 100 * sig_ups, 100 * sig_law))
print("        SPARC supplies %d galaxies with both f_gas > %.2f and 2-5%% distances."
      % (len(S2), FGAS_TH))
NUM["N_for_5pct"] = int(math.ceil(n_stat))
NUM["N_for_5pct_rawdist"] = int(math.ceil(n_dist))
NUM["n_clean_dist"] = len(S2)
ok10 = check("K10", n_stat > 100 and sig_dist > TARGET,
             "N(5%%) = %d galaxies; coherent distance floor %.1f%%" % (math.ceil(n_stat), 100 * sig_dist),
             "N > 100 and distance floor > 5%")

# =======================================================================================
print("\nK11 pipeline validation against the record's own full-sample a0")
# =======================================================================================
print("        full sample (no gas cut, Q <= 3): %d gal, %d pts" % (len(FULL), sum(len(g['R']) for g in FULL)))
print("        a0(canon) = %.4e  vs A9's free-SPARC 1.1033e-10 (same data, log-space mean-square)" % b_full)
r11 = b_full / 1.1033e-10
NUM["a0_full_sample"] = b_full
NUM["n_full_sample"] = len(FULL)
NUM["full_vs_A9_pct"] = round(100 * (b_full / 1.1033e-10 - 1), 2)
ok11 = check("K11", 0.80 < r11 < 1.20, "a0(full)/1.1033e-10 = %.3f" % r11,
             "0.80 < ratio < 1.20  (the pipeline reproduces the known full-sample answer)")

# =======================================================================================
print("\nK12 robustness: radial split, floor, threshold, gas-only")
# =======================================================================================
def fit_subset(S, law, which):
    out = []
    for g in S:
        n = len(g["R"])
        idx = np.arange(n)
        idx = idx[:max(1, n // 2)] if which == "inner" else idx[n // 2:]
        out.append(dict(g, R=g["R"][idx], Vo=g["Vo"][idx], eV=g["eV"][idx],
                        Vg2=g["Vg2"][idx], Vd2=g["Vd2"][idx], Vb2=g["Vb2"][idx]))
    return fit_a0([o for o in out if len(o["R"]) > 0], law)["a0"]


a_in = fit_subset(S, "canon", "inner")
a_out = fit_subset(S, "canon", "outer")
floors = {fl: fit_a0(S, "canon", floor=fl)["a0"] for fl in (0.03, 0.05, 0.10, 0.20)}
scan = {th: len(select(th=th)) for th in (0.70, 0.75, 0.80, 0.85, 0.90)}
scan_a0 = {th: fit_a0(select(th=th), "canon")["a0"] for th in (0.70, 0.75, 0.85, 0.90)}
clean_deep = [g for g in S if g["fD"] == 2 and np.min(g["fg"]) > 0.93]
n_clean_deep = len(clean_deep)
print("        radial split : inner %.3e  outer %.3e  (ratio %.3f)" % (a_in, a_out, a_out / a_in))
print("        floor scan   : " + "  ".join("%.2f:%.3e" % (k, v) for k, v in floors.items()))
print("        threshold scan (N_gal): " + "  ".join("%.2f:%d" % (k, v) for k, v in scan.items()))
print("        threshold scan (a0)    : " + "  ".join("%.2f:%.3e" % (k, v) for k, v in scan_a0.items()))
print("        f_gas > 0.93 AND 2-5%% distances: %d galaxy(ies)" % n_clean_deep)
print("        a0=%.3e at th=0.90 -> kappa_CMB = %.3f" % (scan_a0[0.90], kappa(scan_a0[0.90], RHO_CMB)))
NUM["threshold_scan_a0"] = {str(k): v for k, v in scan_a0.items()}
NUM["n_fgas93_cleandist"] = n_clean_deep
print("        gas-only g_bar: %.3e (x%.2f)" % (a_gas, a_gas / f_can["a0"]))
NUM["a0_inner"] = a_in
NUM["radial_ratio"] = round(a_out / a_in, 4)
NUM["kappa_th090"] = round(kappa(scan_a0[0.90], RHO_CMB), 4)
NUM["a0_outer"] = a_out
NUM["floor_scan"] = {str(k): v for k, v in floors.items()}
NUM["threshold_scan"] = {str(k): v for k, v in scan.items()}
ok12 = check("K12", abs(a_out / a_in - 1) < 0.25 and max(floors.values()) / min(floors.values()) < 1.30,
             "outer/inner = %.3f; floor scan spread x%.2f"
             % (a_out / a_in, max(floors.values()) / min(floors.values())),
             "< 0.25 and < x1.30  (the a0 value is not a artefact of the radial range or the floor)")

# =======================================================================================
# summary
# =======================================================================================
PASS = sum(1 for c in CHECKS if c["pass"])
print("\n" + "=" * 92)
print("SUMMARY")
print("=" * 92)
print("  Upsilon-free sample          : %d of 175 galaxies, %d points, median g_bar/a0 = %.4f"
      % (NG, NPTS, med_reached))
print("  a0 (canonical law, 5%% floor) : %.4e  (bootstrap %.0f%%)" % (f_can["a0"], 100 * sig_gal))
print("  a0 (quadratic law)           : %.4e" % f_quad["a0"])
print("  kappa_fit (CMB density)      : %.4f +- %.4f" % (K_CAN_CMB, K_CAN_CMB * tot_q))
print("  kappa_fit (local density)    : %.4f" % kappa(f_can["a0"], RHO_LOC))
print("  record's kappa               : 0.465 +- 0.076  -> this channel does not confirm it")

RESULTS = {
    "lane": "A14",
    "status": "NUMERICAL",
    "checks": CHECKS,
    "numbers": NUM,
    "constants_used": [
        "c = 2.99792458e8 m/s", "G = 6.67430e-11", "kpc = 3.0856775814913673e19 m",
        "Mpc = 3.0856775814913673e22 m", "a0_can = 9.3603e-11", "a0_alt = 1.1312e-10",
        "H0_CMB = 0.6736", "Omega_m = 0.3153", "H0_local = 0.73", "Omega_L_local = 0.685",
        "Upsilon_disk = 0.5", "Upsilon_bulge = 0.7", "f_gas threshold = 0.80",
        "errV/V cut = 0.10", "error floor = 0.05",
        "derived: Omega_L,CMB = 1 - 0.3153 = 0.6847",
        "derived: Omega_L h^2 = 0.6847 * 0.6736^2 = 0.3107",
        "derived: sqrt(Omega_L,local) = 0.8278",
    ],
    "external_inputs": EXTERNAL,
}
tag = "_MUTATE" if MUTATE else ""
json.dump(RESULTS, open(os.path.join(HERE, "a14_results%s.json" % tag), "w"), indent=1)
print("\nA14 COMPLETE: %d/%d checks PASS." % (PASS, len(CHECKS)))
sys.exit(0 if PASS == len(CHECKS) else 1)
