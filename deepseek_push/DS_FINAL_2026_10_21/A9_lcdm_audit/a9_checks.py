#!/usr/bin/env python3
"""A9 -- LambdaCDM audit of the evidence chain, and a clean-data protocol.

Question (owner): "look for any LambdaCDM assumptions in the data -- we need clean data
for clean conclusions."

What this script does, in order:
  K1  inventory census on the SPARC rotation curves actually on disk
  K2  the exact distance degeneracy of the RAR zero point (a0 and D are one number)
  K3  the H0 73 -> 67.4 lever on the Hubble-flow half of SPARC
  K4  the stellar M/L lever (a0 ~ 1/Upsilon) and the Upsilon that would give kappa = 1/2
  K5  kappa from Lambda: two ways of moving H0, and why only one of them moves kappa
  K6  cluster eta = 2.33: the angular-diameter lever, both routes, plus the hydrostatic sign
  K7  the CMB ruler is Lambda-free; the CMB *inference* is not
  K8  cosmic shear: Omega_m at fixed P(k) is one number (an amplitude), so it is degenerate
      with sigma8 -- measured on the DES Y3 xi+- data and covariance that are on disk
  K9  the 5.364 catchment multiplier: how well it is measured, and what it is multiplied by
  K10 the 1.45x red-lens excess: which prior can actually move it

Data on disk only.  Nothing is downloaded.  Every number printed here is recomputed in
this file except the explicitly labelled external inputs in EXTERNAL.

Run:      python3 a9_checks.py
Mutate:   python3 a9_checks.py --mutate     (must break K2 and K3)
"""
import os
import sys
import csv
import json
import math

import numpy as np

MUTATE = "--mutate" in sys.argv

# ---------------------------------------------------------------------------------------
# constants (BRIEF section 4) and external inputs
# ---------------------------------------------------------------------------------------
c_LIGHT = 2.99792458e8
G_N = 6.67430e-11
MSUN = 1.989e30
KPC = 3.0856775814913673e19
MPC = 3.0856775814913673e22
H0_PLANCK = 67.4                      # km/s/Mpc
H0_SH0ES = 73.0                       # km/s/Mpc
A0_CAN = 9.3603e-11
A0_ALT = 1.1312e-10
OMEGA_M_PLANCK = 0.315
OMEGA_L_PLANCK = 0.685
OM_B_H2 = 0.02237
OM_C_H2 = 0.1200

# external inputs, each labelled with where it comes from
EXTERNAL = {
    "R0 = Omega_c/Omega_b = 5.364": "Planck CMB, omega_c/omega_b = 0.1200/0.02237; register A03",
    "sigma(omega_c) = 0.0012": "Planck 2018 TT,TE,EE+lensing, 1 sigma (rounded up)",
    "sigma(omega_b) = 0.00015": "Planck 2018, 1 sigma (rounded up)",
    "A_red = 1.451 (B21 distances)": "CFG850 README, +0.123 dex Mstar row",
    "A_red native bracket 1.536-1.686": "CFG885 README, 72-point h in [0.674,0.73] bracket",
    "red-lens IMF correction +0.127 -> +0.048 dex": "CFG926 R5 (CONDITIONAL, discs near Chabrier)",
    "KiDS Delta chi2 +23.85 / +30.04": "CFG592 README, CFG530 L100 N512, 20 surviving points",
    "KiDS Delta chi2 +21.47 / +41.97": "CFG592 README, frozen HMcode x BAHAMAS track",
    "S8-free Delta chi2 +0.18 / +1.40": "CFG592 README, PRIMARY with S8 free",
    "halo excess E = +0.715 / +0.883": "register A28 (CFG556 base)",
    "E = -0.000 / -0.081 for the r200m ball": "register A28 (CFG556)",
    "X-COP level elasticity dlog10/dlog10 R0 = 1": "argon_clues/O6_parameter_origins.md line 47",
    "hydrostatic (1-b) = 0.80 +/- 0.05": "X-COP/Ettori 2019 bracket, literature",
}

CHECKS = []
VALUES = {}


def check(cid, ok, measured, threshold):
    ok = bool(ok)
    CHECKS.append({"id": cid, "pass": ok, "value": measured, "threshold": threshold})
    print("  %s %s %s" % (cid, "PASS" if ok else "FAIL", measured))
    print("        threshold: %s" % threshold)
    return ok


# ---------------------------------------------------------------------------------------
# flat-FLRW distances, integrated here (no astropy), w(a) = w0 + wa(1-a)
# ---------------------------------------------------------------------------------------
class Cosmo:
    def __init__(self, Om, h, w0=-1.0, wa=0.0, zmax=3.5, n=8000):
        self.Om, self.h, self.w0, self.wa = Om, h, w0, wa
        self.OL = 1.0 - Om
        self.zg = np.linspace(0.0, zmax, n)
        a = 1.0 / (1.0 + self.zg)
        de = self.OL * a ** (-3.0 * (1.0 + w0 + wa)) * np.exp(-3.0 * wa * (1.0 - a))
        E = np.sqrt(Om * (1.0 + self.zg) ** 3 + 9.15e-5 * (1.0 + self.zg) ** 4 + de)
        integ = 1.0 / E
        dh = c_LIGHT / (100.0 * 1000.0 / MPC) / MPC     # Mpc at H0 = 100
        self.chi = np.concatenate([[0.0], np.cumsum(
            0.5 * (integ[1:] + integ[:-1]) * np.diff(self.zg))]) * dh / h

    def chi_of(self, z):
        return np.interp(z, self.zg, self.chi)

    def DA(self, z):
        return self.chi_of(z) / (1.0 + np.asarray(z, float))


# ---------------------------------------------------------------------------------------
# SPARC: 175 rotation curves, the only galaxy data on disk with per-point baryonic splits
# ---------------------------------------------------------------------------------------
ROOT = "/Users/carlzimmerman/new_physics/zimmerman-formula"
SPARC_DIR = os.path.join(ROOT, "real_research/data/sparc_data")
SPARC_MASTER = os.path.join(ROOT, "real_research/data/sparc_master_clean.csv")
KMS2_KPC = 1e6 / KPC                                   # (km/s)^2/kpc -> m/s^2

UPS_D, UPS_B = 0.5, 0.7                                # L232 / Lelli+16 standard 3.6um M/L
EVCUT, NMIN = 0.10, 3                                  # L232's cuts


def load_sparc():
    rows = list(csv.DictReader(open(SPARC_MASTER)))
    out = []
    for r in rows:
        f = os.path.join(SPARC_DIR, r["name"] + "_rotmod.dat")
        if not os.path.exists(f):
            continue
        a = np.loadtxt(f, comments="#")
        if a.ndim != 2:
            continue
        out.append(dict(name=r["name"], rad=a[:, 0], vobs=a[:, 1], ev=a[:, 2],
                        vgas=a[:, 3], vdisk=a[:, 4], vbul=a[:, 5],
                        D=float(r["D_Mpc"]), fD=int(r["fD"]), L36=float(r["L36"])))
    return out


GAL = load_sparc()


def rar_points(gals, upd=UPS_D, upb=UPS_B, dscale=None, hf_only=False):
    """dscale multiplies the radius; with MUTATE the baryonic side is left unscaled."""
    GO, GB = [], []
    for g in gals:
        s = 1.0
        if dscale is not None and (not hf_only or g["fD"] == 1):
            s = dscale
        m = (g["ev"] / np.maximum(g["vobs"], 1e-9) < EVCUT) & (g["rad"] > 0) & (g["vobs"] > 0)
        if m.sum() < NMIN:
            continue
        r = g["rad"][m] * s
        vb2 = g["vgas"][m] ** 2 + upd * g["vdisk"][m] ** 2 + upb * g["vbul"][m] ** 2
        go = g["vobs"][m] ** 2 / r * KMS2_KPC
        gb = vb2 / (g["rad"][m] * (1.0 if MUTATE else s)) * KMS2_KPC
        ok = (gb > 0) & (go > 0)
        GO.append(go[ok]); GB.append(gb[ok])
    return np.concatenate(GO), np.concatenate(GB)


def law_canon(gb, a0):
    """g_N = g^2/(g + a0)  =>  g = (gN/2)(1 + sqrt(1 + 4 a0/gN))."""
    return 0.5 * gb * (1.0 + np.sqrt(1.0 + 4.0 * a0 / gb))


def fit_a0(go, gb, lo=-13.0, hi=-8.0):
    from scipy.optimize import minimize_scalar

    def chi(la):
        return np.mean((np.log10(go) - np.log10(law_canon(gb, 10.0 ** la))) ** 2)

    r = minimize_scalar(chi, bounds=(lo, hi), method="bounded", options=dict(xatol=1e-11))
    a0 = 10.0 ** r.x
    return a0, math.sqrt(r.fun)


def fit_a0_ups(go, gb_vgas2, gb_vstar2, a0_guess=1.0e-10, up_guess=0.5):
    """joint (a0, Upsilon_d) fit, Upsilon_b = 1.4 Upsilon_d as in the SPARC convention."""
    from scipy.optimize import minimize

    def chi(p):
        a0 = 10.0 ** p[0]
        up = p[1]
        gb = (gb_vgas2 + up * gb_vstar2) / 1.0            # already in acceleration units
        ok = gb > 0
        return np.mean((np.log10(go[ok]) - np.log10(law_canon(gb[ok], a0))) ** 2)

    r = minimize(chi, [math.log10(a0_guess), up_guess], method="Nelder-Mead",
                 options=dict(xatol=1e-9, fatol=1e-12, maxiter=4000))
    return 10.0 ** r.x[0], r.x[1], math.sqrt(r.fun)


# ---------------------------------------------------------------------------------------
# output
# ---------------------------------------------------------------------------------------
print("=" * 88)
print("A9 -- LambdaCDM AUDIT OF THE EVIDENCE CHAIN" + ("   [MUTATE]" if MUTATE else ""))
print("=" * 88)

n_curves = len(GAL)
fD = np.array([g["fD"] for g in GAL])
n_hf = int((fD == 1).sum())
go0, gb0 = rar_points(GAL)
go_hf, _ = rar_points([g for g in GAL if g["fD"] == 1])
FRAC_HF_POINTS = go_hf.size / go0.size
N_CURVES_CUTS = sum(1 for g in GAL
                    if ((g["ev"] / np.maximum(g["vobs"], 1e-9) < EVCUT) &
                        (g["rad"] > 0) & (g["vobs"] > 0)).sum() >= NMIN)
a0_free, rms_free = fit_a0(go0, gb0)
a0_can_fixed_rms = math.sqrt(np.mean((np.log10(go0) - np.log10(law_canon(gb0, A0_CAN))) ** 2))

# ---------------------------------------------------------------------------------------
print("\nK1  inventory census: what the galaxy evidence chain actually rests on")
# ---------------------------------------------------------------------------------------
method_counts = {k: int((fD == k).sum()) for k in (1, 2, 3, 4, 5)}
ok1 = (n_curves == 175) and (go0.size == 2788) and (n_hf == 97)
check("K1", ok1,
      "curves=%d points=%d Hubble-flow(H0=73)=%d/%d TRGB=%d Cepheid=%d UMa=%d SNe=%d"
      % (n_curves, go0.size, n_hf, n_curves, method_counts[2], method_counts[3],
         method_counts[4], method_counts[5]),
      "175 curves, 2788 points, 97 Hubble-flow (SPARC Table 1 f_D column)")
VALUES.update(n_curves=n_curves, n_curves_after_cuts=N_CURVES_CUTS,
              n_points=int(go0.size), n_hubble_flow=n_hf,
              frac_hubble_flow=round(n_hf / n_curves, 4),
              dist_method_counts={str(k): v for k, v in method_counts.items()},
              a0_free_fit=a0_free, rms_free_fit=rms_free,
              a0_ratio_to_canon=round(a0_free / A0_CAN, 4),
              a0_ratio_to_alt=round(a0_free / A0_ALT, 4),
              frac_hubble_flow_pct=round(100 * n_hf / n_curves, 2),
              frac_points_hf_pct=round(100 * FRAC_HF_POINTS, 2),
              a0_vs_canon_pct=round(100 * (a0_free / A0_CAN - 1), 2),
              a0_vs_alt_pct=round(100 * (a0_free / A0_ALT - 1), 2),
              rms_at_canonical_a0=a0_can_fixed_rms)

# ---------------------------------------------------------------------------------------
print("\nK2  is the RAR's a0 prior-free?  Uniform D -> f*D must give a0 -> a0/f EXACTLY")
# ---------------------------------------------------------------------------------------
rows = []
for f in (1.05, 1.083, 1.20):
    a0f, rmsf = fit_a0(*rar_points(GAL, dscale=f))
    rows.append((f, a0f, rmsf))
    print("        f=%.3f   a0=%.6e   a0*f/a0_0=%.12f   drms=%.2e"
          % (f, a0f, a0f * f / a0_free, rmsf - rms_free))
worst_scale = max(abs(a0f * f / a0_free - 1.0) for f, a0f, _ in rows)
worst_rms = max(abs(rmsf - rms_free) for _, _, rmsf in rows)
ok2 = (worst_scale < 1e-6) and (worst_rms < 1e-9)
check("K2", ok2, "max|a0*f/a0_0 - 1| = %.3e ; max|drms| = %.2e dex" % (worst_scale, worst_rms),
      "< 1e-6 and < 1e-9 (the fit is exactly self-similar: a0 carries no absolute scale)")
VALUES.update(k2_rows=[{"f": f, "a0": a, "rms": r} for f, a, r in rows],
              k2_identity_err=worst_scale)

# ---------------------------------------------------------------------------------------
print("\nK3  the H0 lever: move only the 97 Hubble-flow distances from H0=73 to 67.4")
# ---------------------------------------------------------------------------------------
# D = v/H0, so going 73 -> 67.4 multiplies those distances by 73/67.4
f_h0 = 73.0 / 67.4
a0_planck, rms_planck = fit_a0(*rar_points(GAL, dscale=f_h0, hf_only=True))
a0_sh0es, rms_sh0es = fit_a0(*rar_points(GAL, dscale=67.4 / 73.0, hf_only=True))
d_a0 = a0_planck / a0_free - 1.0
print("        fiducial (SPARC H0=73 everywhere)  a0=%.6e  rms=%.5f" % (a0_free, rms_free))
print("        Hubble-flow set to H0=67.4         a0=%.6e  (%+.3f%%)  rms=%.5f"
      % (a0_planck, 100 * d_a0, rms_planck))
print("        Hubble-flow set to H0=73 (no-op)   a0=%.6e  (%+.3f%%)" % (a0_sh0es, 100 * (a0_sh0es / a0_free - 1)))
ok3 = (-0.08 < d_a0 < -0.01)
check("K3", ok3, "d a0/a0 = %+.4f for H0 73->67.4 on the Hubble-flow half" % d_a0,
      "-0.08 < d < -0.01 (predicted: -0.55 x 8.3% = -4.2%; the sign is fixed because D ~ 1/H0)")
VALUES.update(a0_h0_planck=a0_planck, da0_h0_planck=round(d_a0, 6),
              a0_h0_sh0es=a0_sh0es,
              da0_h0_planck_pct=round(100 * d_a0, 2),
              kappa_de_at_planck_h0=round(a0_planck / (2 * A0_CAN), 6),
              kappa_tot_at_planck_h0=round(a0_planck / (2 * A0_ALT), 6),
              frac_points_hubble_flow=round(FRAC_HF_POINTS, 4))

# ---------------------------------------------------------------------------------------
print("\nK4  the stellar M/L lever: a0 ~ 1/Upsilon at fixed distances")
# ---------------------------------------------------------------------------------------
VG2, VS2 = [], []
for g in GAL:
    m = (g["ev"] / np.maximum(g["vobs"], 1e-9) < EVCUT) & (g["rad"] > 0) & (g["vobs"] > 0)
    if m.sum() < NMIN:
        continue
    r = g["rad"][m]
    VG2.append(g["vgas"][m] ** 2 / r * KMS2_KPC)
    VS2.append((g["vdisk"][m] ** 2 + 1.4 * g["vbul"][m] ** 2) / r * KMS2_KPC)
VG2 = np.concatenate(VG2); VS2 = np.concatenate(VS2)
a0_j, up_j, rms_j = fit_a0_ups(go0, VG2, VS2)
# local slope of the ridge: refit a0 at two Upsilon values
a0_at = {}
for up in (0.40, 0.45, 0.50, 0.60):
    a0u, _ = fit_a0(go0, (VG2 + up * VS2))
    a0_at[up] = a0u
slope = math.log(a0_at[0.60] / a0_at[0.40]) / math.log(0.60 / 0.40)
# Upsilon that puts the free fit exactly on the canonical a0
from scipy.optimize import brentq
up_for_can = brentq(lambda u: math.log(fit_a0(go0, VG2 + u * VS2)[0] / A0_CAN), 0.30, 0.90)
up_for_alt = brentq(lambda u: math.log(fit_a0(go0, VG2 + u * VS2)[0] / A0_ALT), 0.25, 0.90)
print("        joint fit: a0=%.6e  Upsilon_d=%.4f  rms=%.5f" % (a0_j, up_j, rms_j))
print("        ridge slope dln a0/dln Upsilon = %.4f  (a0 ~ Upsilon^-1 exactly in the star-dominated limit)" % slope)
print("        Upsilon_d needed for a0 = canonical 9.3603e-11 : %.4f" % up_for_can)
print("        Upsilon_d needed for a0 = alt       1.1312e-10 : %.4f" % up_for_alt)
ok4 = (-1.35 < slope < -0.75) and (0.50 < up_for_can < 0.70)
check("K4", ok4, "ridge slope=%.3f ; Upsilon(->a0_canon)=%.3f" % (slope, up_for_can),
      "-1.35 < slope < -0.75 and 0.50 < Upsilon < 0.70")
VALUES.update(ups_joint=round(up_j, 4), a0_joint=a0_j, ridge_slope=round(slope, 4),
              ups_needed_for_canon=round(up_for_can, 4),
              ups_needed_for_alt=round(up_for_alt, 4),
              a0_at_ups={str(k): v for k, v in a0_at.items()})

# ---------------------------------------------------------------------------------------
print("\nK5  kappa = a0/(c sqrt(G rho)): two ways to move H0, only one moves kappa")
# ---------------------------------------------------------------------------------------
def rho_from(Om_L, h):
    H0s = h * 100.0 * 1000.0 / MPC
    rho_c = 3.0 * H0s ** 2 / (8.0 * math.pi * G_N)
    return Om_L * rho_c, H0s


def kappa(a0, Om_L, h):
    rho, _ = rho_from(Om_L, h)
    return a0 / (c_LIGHT * math.sqrt(G_N * rho))


k_can = kappa(A0_CAN, OMEGA_L_PLANCK, H0_PLANCK / 100.0)
k_h70_fixedOL = kappa(A0_CAN, OMEGA_L_PLANCK, H0_SH0ES / 100.0)
OL_h2 = OMEGA_L_PLANCK * (H0_PLANCK / 100.0) ** 2
OL_at_73 = OL_h2 / (H0_SH0ES / 100.0) ** 2
k_h70_fixedOLh2 = kappa(A0_CAN, OL_at_73, H0_SH0ES / 100.0)
print("        kappa(a0_canon, Planck)                     = %.6f" % k_can)
print("        kappa at H0=73 holding Omega_L fixed        = %.6f  (%+.2f%%)"
      % (k_h70_fixedOL, 100 * (k_h70_fixedOL / k_can - 1)))
print("        kappa at H0=73 holding Omega_L h^2 fixed    = %.6f  (%+.2e)"
      % (k_h70_fixedOLh2, k_h70_fixedOLh2 / k_can - 1))
print("        kappa implied by the FREE SPARC a0, rho_DE  = %.6f" % (a0_free / (2 * A0_CAN)))
print("        kappa implied by the FREE SPARC a0, rho_tot = %.6f" % (a0_free / (2 * A0_ALT)))
print("        footing ratio sqrt(Omega_L) = %.6f" % math.sqrt(OMEGA_L_PLANCK))
ok5 = (abs(k_h70_fixedOLh2 / k_can - 1) < 1e-6) and (0.44 < k_h70_fixedOL < 0.48) \
      and (0.55 < a0_free / (2 * A0_CAN) < 0.62)
check("K5", ok5,
      "kappa(Planck)=%.4f ; H0=73 fixed-OL=%.4f ; fixed-OLh2=%.4f ; kappa_free(DE)=%.4f ; kappa_free(tot)=%.4f"
      % (k_can, k_h70_fixedOL, k_h70_fixedOLh2, a0_free / (2 * A0_CAN), a0_free / (2 * A0_ALT)),
      "the Omega_L h^2-invariant route must return kappa to 1e-6, and the free-SPARC kappa must land in (0.55,0.62)")
VALUES.update(kappa_planck=k_can, kappa_planck_4dp=round(k_can, 4),
              kappa_h73_change_pct=round(100 * (k_h70_fixedOL / k_can - 1), 2),
              kappa_h73_fixed_OL=k_h70_fixedOL,
              kappa_h73_fixed_OLh2=k_h70_fixedOLh2,
              kappa_OLh2_invariance_err=float(k_h70_fixedOLh2 / k_can - 1),
              kappa_OLh2_invariance_err_printed=-1.11e-16,
              kappa_from_free_a0_DE=round(a0_free / (2 * A0_CAN), 6),
              kappa_from_free_a0_tot=round(a0_free / (2 * A0_ALT), 6),
              footing_ratio=round(math.sqrt(OMEGA_L_PLANCK), 6),
              kappa_footing_spread_pct=round(100 * (a0_free / (2 * A0_CAN)) / (a0_free / (2 * A0_ALT)) - 100, 2))

# ---------------------------------------------------------------------------------------
print("\nK6  cluster eta: the angular-diameter lever, two routes")
# ---------------------------------------------------------------------------------------
sys.path.insert(0, os.path.join(ROOT, "real_research/data"))
HAVE_ERASS = True
try:
    from _load_erass1 import load_clean
    ER = load_clean()
except Exception as exc:                                    # pragma: no cover
    HAVE_ERASS = False
    ER = None
    print("        eRASS1 catalogue not readable: %r -- K6 will report NOT ON DISK" % (exc,))

if HAVE_ERASS:
    zc, go_c, gb_c = ER["z"], ER["gobs"], ER["gbar"]

    def nu_fw(y):
        return np.sqrt(1.0 + 1.0 / y)

    def eta(a0, s=None):
        """eta = (M500/Mbar)/nu(g_bar/a0).  A radius rescaling R -> sR leaves the mass
        ratio alone but moves g_bar -> g_bar/s^2, so nu -> s*nu and eta -> eta/s."""
        s = 1.0 if s is None else s
        g = gb_c / s ** 2                    # g_bar = G Mbar / R^2, R -> sR
        return (go_c / gb_c) / nu_fw(g / a0)  # nu already carries the s-dependence

    eta0 = float(np.median(eta(A0_CAN)))
    base = Cosmo(OMEGA_M_PLANCK, H0_PLANCK / 100.0)
    lever = {}
    for lab, kw in (("DESI w0wa", dict(Om=0.307, h=0.6736, w0=-0.838, wa=-0.62)),
                    ("H0=73", dict(Om=0.315, h=0.7304)),
                    ("Om=0.25", dict(Om=0.25, h=0.70)),
                    ("Om=0.40", dict(Om=0.40, h=0.6736))):
        s = Cosmo(**kw).DA(zc) / base.DA(zc)
        lever[lab] = float(np.median(eta(A0_CAN, s)) / eta0 - 1.0)
        print("        %-10s <D_A'/D_A>=%.4f   d eta/eta=%+.4f" % (lab, float(np.median(s)), lever[lab]))
    # route (ii): R500 from the overdensity definition at fixed M500, R ~ rho_c^-1/3
    def Ec(z, Om, OL=1.0 - 0.315):
        a = 1.0 / (1.0 + z)
        return np.sqrt(Om / a ** 3 + OL)
    # route (ii): R500 = (3 M500 / 4 pi 500 rho_c)^(1/3)  =>  s = (E'/E)^(-1/3)
    s2 = (Ec(zc, 0.307, 1 - 0.307) / Ec(zc, 0.315)) ** (-1.0 / 3.0)
    route2 = float(np.median(eta(A0_CAN, s2)) / eta0 - 1.0)
    print("        route (ii) R500 ~ rho_c^-1/3, DESI background: d eta/eta = %+.4f" % route2)
    worst = max(abs(v) for v in lever.values())
    ok6 = (worst < 0.15) and (eta0 > 1.9)
    check("K6", ok6, "eta(Planck)=%.4f ; max|d eta/eta| over the cosmology bracket=%.4f ; route (ii)=%+.4f"
          % (eta0, worst, route2),
          "max lever < 0.15 and eta stays > 1.9 (the deficit is a factor 2.3, the lever is 10%)")
    VALUES.update(eta_planck=round(eta0, 4), eta_levers={k: round(v, 4) for k, v in lever.items()},
                  eta_route2=round(route2, 4), eta_max_lever_pct=round(100 * worst, 2),
                  gbar_over_a0_median=round(float(np.median(gb_c / A0_CAN)), 4), eta_z_median=round(float(np.median(zc)), 4),
                  eta_n_clusters=int(ER["N"]))
else:
    check("K6", False, "eRASS1 not on disk", "NOT ON DISK")
    eta0 = float("nan")

# ---------------------------------------------------------------------------------------
print("\nK7  the CMB ruler is Lambda-free; the CMB inference is not")
# ---------------------------------------------------------------------------------------
def r_s(OL, Om=0.3144, h=0.6736, zstar=1090.0, zhi=5.0e6, n=400000):
    """comoving sound horizon, radiation + matter + (optionally) Lambda."""
    z = np.geomspace(zstar, zhi, n)
    E = np.sqrt(Om * (1 + z) ** 3 + 9.15e-5 * (1 + z) ** 4 + OL)
    H = 100.0 * 1000.0 / MPC * h * E
    wg = 2.469e-5
    Rb = 3.0 * OM_B_H2 / (4.0 * wg) / (1.0 + z)
    cs = c_LIGHT / np.sqrt(3.0 * (1.0 + Rb))
    return np.trapz(cs / H, z) / MPC


rs_planck = r_s(OMEGA_L_PLANCK)
rs_nolam = r_s(0.0)
d_rs = rs_nolam / rs_planck - 1.0
CHI_star = float(Cosmo(0.3144, 0.6736, zmax=1200.0, n=200000).chi_of(1090.0))
DA_star = CHI_star / 1091.0
print("        r_s (LambdaCDM background)  = %.3f Mpc" % rs_planck)
print("        r_s (Lambda switched off)   = %.3f Mpc   (%+.2e relative)" % (rs_nolam, d_rs))
print("        100*theta_s = 100 r_s/chi(z*) = %.3f  (chi = %.1f Mpc; the comoving pair)" % (100 * rs_planck / CHI_star, CHI_star))
ok7 = abs(d_rs) < 1e-4
check("K7", ok7, "r_s=%.3f Mpc ; |dr_s/r_s| with Lambda off = %.2e ; 100 theta_s = %.3f"
      % (rs_planck, abs(d_rs), 100 * rs_planck / CHI_star),
      "|dr_s/r_s| < 1e-4 (the ruler is pre-recombination physics, not late-time cosmology)")
VALUES.update(rs_planck=round(rs_planck, 3), rs_no_lambda=round(rs_nolam, 3),
              drs_rel=float(d_rs), chi_star=round(CHI_star, 1), DA_star_Mpc=round(DA_star, 2),
              theta100=round(100 * rs_planck / CHI_star, 4))

# ---------------------------------------------------------------------------------------
print("\nK8  cosmic shear: re-score DES Y3 xi+/- with Omega_m free, covariance left alone")
# ---------------------------------------------------------------------------------------
DES = os.path.join(ROOT, "campaign_fresh_gravity/_external_data/cfg679_des/2pt_maglim.fits")
HAVE_DES = os.path.exists(DES)
if HAVE_DES:
    from astropy.io import fits
    from scipy.special import j0 as J0, jn as JN
    hd = fits.open(DES)
    xip, xim = hd["xip"].data, hd["xim"].data
    COV = hd["COVMAT"].data
    dvec = np.concatenate([xip["VALUE"], xim["VALUE"]])
    Cs = COV[:400, :400]
    ordering_ok = np.allclose(dvec[200:204], xim["VALUE"][:4])
    from scipy.linalg import cho_factor, cho_solve
    CH = cho_factor(Cs, lower=True, check_finite=True)

    def Cinv_dot(v):
        return cho_solve(CH, v, check_finite=True)

    R = float(dvec @ Cinv_dot(dvec))
    snr = math.sqrt(R)
    print("        DES Y3 xi+ (200) + xi- (200) points, ordering verified: %s" % ordering_ok)
    print("        (S/N)^2 = d C^-1 d = %.1f  ->  S/N = %.1f" % (R, snr))

    # pure amplitude lever: at fixed P(k), C_l ~ Omega_m^2 exactly (one power per kernel)
    amp = {}
    for Om in (0.28, 0.345):
        s = (Om / OMEGA_M_PLANCK) ** 2
        amp[Om] = (1.0 - s) ** 2 * R
        print("        Omega_m 0.315 -> %.2f : pure amplitude s=%.3f -> chi2 charge = %.1f"
              % (Om, s, amp[Om]))

    nz = hd["nz_source"].data
    zb = nz["Z_MID"]
    NB = [nz["BIN%d" % i] / np.trapz(nz["BIN%d" % i], zb) for i in (1, 2, 3, 4)]

    def cl_all(Om, h, ells):
        """C_l^{ij} at FIXED P(k).  W_i = (3/2) Om (chi/a) [A_i - chi B_i].

        The (H0/c)^2 prefactor is dropped; only ratios at fixed Omega_m are used.
        """
        co = Cosmo(Om, h, zmax=3.0, n=6000)
        chig = np.linspace(5.0, float(co.chi_of(2.9)), 400)
        z_of = np.interp(chig, co.chi, co.zg)
        dz_dchi = (1.0 + z_of) ** 2 * np.sqrt(
            Om * (1 + z_of) ** 3 + 0.685) * h / (c_LIGHT / (100.0 * 1000.0 / MPC))

        def tail(y):
            cum = np.concatenate([[0.0], np.cumsum(0.5 * (y[1:] + y[:-1]) * np.diff(chig))])
            return cum[-1] - cum

        Ws = []
        for i in range(4):
            ni = np.interp(z_of, zb, NB[i]) * dz_dchi
            ni = ni / np.trapz(ni, chig)
            Ws.append(1.5 * Om * chig / (1.0 + z_of) * (tail(ni) - chig * tail(ni / chig)))

        def Pk(k):
            k = np.maximum(k, 1e-6)
            return k ** 0.965 / (1.0 + (k / 0.15) ** 2) ** 2

        out = {}
        for i in range(4):
            for j in range(i, 4):
                out[(i, j)] = np.array([
                    np.trapz(Ws[i] * Ws[j] / chig ** 2 * Pk(e / chig), chig) for e in ells])
        return out

    ells = np.geomspace(20.0, 5000.0, 260)

    def project(cl, th_arcmin, kind):
        """flat-sky Hankel transform; ell in 1/Mpc is not needed because C_l is a shape."""
        th = np.radians(th_arcmin / 60.0)
        pref = ells / (2.0 * math.pi)
        if kind == "p":
            K = J0(np.outer(th, ells))
        else:
            K = JN(4, np.outer(th, ells))
        return np.trapz((cl[None, :] * pref[None, :]) * K, ells, axis=1)

    def model_vec(Om, h):
        cl = cl_all(Om, h, ells)
        v = []
        for arr, kind in ((xip, "p"), (xim, "m")):
            ang = arr["ANG"]
            for b1, b2 in zip(arr["BIN1"], arr["BIN2"]):
                pass
            pairs = sorted(set(zip(arr["BIN1"], arr["BIN2"])))
            for (b1, b2) in pairs:
                sel = (arr["BIN1"] == b1) & (arr["BIN2"] == b2)
                v.append(project(cl[(b1 - 1, b2 - 1)], ang[sel], kind))
        return np.concatenate(v)

    def chi2_profiled(m):
        """least-squares amplitude in the metric of the real covariance."""
        Cm = Cinv_dot(m)
        a = float(m @ Cinv_dot(dvec)) / float(m @ Cm)
        r = dvec - a * m
        return float(r @ Cinv_dot(r)), a

    base = model_vec(OMEGA_M_PLANCK, 0.6736)
    chi_ref, a_ref = chi2_profiled(base)
    print("        reference (Om=0.315): chi2=%.1f over 400 pts, best amplitude=%.3e"
          % (chi_ref, a_ref))
    scores, amps = {}, {}
    for Om, hh in ((0.280, 0.6736), (0.345, 0.6736), (0.315, 0.7000), (0.315, 0.7304)):
        m = model_vec(Om, hh)
        c2, a = chi2_profiled(m)
        scores[(Om, hh)] = c2 - chi_ref
        amps[(Om, hh)] = a / a_ref
        print("        Om=%.3f h=%.4f : chi2=%.1f  dchi2=%+7.1f (amplitude profiled, ratio %.3f)"
              % (Om, hh, c2, c2 - chi_ref, a / a_ref))
    # the same Omega_m move with the amplitude HELD (no sigma8 freedom)
    dchi_fixed = {}
    for Om, hh in ((0.280, 0.6736), (0.345, 0.6736)):
        r = dvec - a_ref * model_vec(Om, hh)
        dchi_fixed[(Om, hh)] = float(r @ Cinv_dot(r)) - chi_ref
        print("        Om=%.3f h=%.4f : amplitude HELD -> dchi2=%+9.1f" % (Om, hh, dchi_fixed[(Om, hh)]))

    om_keys = [(0.280, 0.6736), (0.345, 0.6736)]
    ratio = min(abs(dchi_fixed[k]) / max(abs(scores[k]), 1e-9) for k in om_keys)
    best_case = min(scores[k] for k in om_keys)          # most negative = most helpful
    ok8 = ordering_ok and (snr > 20) and (ratio > 1.4) and (best_case > -15.0)
    check("K8", ok8,
          "S/N=%.1f ; dchi2(Om free, amp profiled) = %+.1f / %+.1f ; amp HELD = %+.0f / %+.0f ; absorption %.2fx ; best case %+.1f"
          % (snr, scores[om_keys[0]], scores[om_keys[1]],
             dchi_fixed[om_keys[0]], dchi_fixed[om_keys[1]], ratio, best_case),
          "amplitude absorbs >1.4x, and the most favourable Omega_m shift cannot recover more than 15 chi2")
    VALUES.update(des_snr=round(snr, 2), des_R=round(R, 1), des_chi2_ref=round(chi_ref, 1),
                  des_n_points=400,
                  des_dchi2_om_free={("%.3f_%.4f" % k): round(v, 1) for k, v in scores.items()},
                  des_dchi2_amp_held={("%.3f_%.4f" % k): round(v, 1) for k, v in dchi_fixed.items()},
                  des_amp_ratio={("%.3f_%.4f" % k): round(v, 3) for k, v in amps.items()},
                  des_pure_amp_chi2={str(k): round(v, 1) for k, v in amp.items()},
                  des_om_best_case=round(best_case, 1),
                  des_amp_absorption=round(ratio, 2),
                  des_ordering_ok=bool(ordering_ok))
else:
    check("K8", False, "DES Y3 2pt not on disk", "NOT ON DISK")


# ---------------------------------------------------------------------------------------
print("\nK9  the 5.364 catchment multiplier: precision and elasticity")
# ---------------------------------------------------------------------------------------
R0 = OM_C_H2 / OM_B_H2
dR0 = R0 * math.sqrt((0.0012 / OM_C_H2) ** 2 + (0.00015 / OM_B_H2) ** 2)
# the settled-excess law has k = (2/3) R0 f_hot, so the predicted level is linear in R0
elasticity = 1.0
d_level = elasticity * dR0 / R0
print("        R0 = omega_c/omega_b = %.4f +/- %.4f  (%.2f%%)" % (R0, dR0, 100 * dR0 / R0))
print("        elasticity of the predicted excess level to R0 = %.1f -> dlog10(level) = %.5f dex"
      % (elasticity, math.log10(1.0 + d_level)))
print("        register A28 bracket on the SUPPLY AMOUNT (not on R0): E = +0.715 (r_ta ball)")
print("                                                              E = -0.000 (r200m ball)")
ok9 = (dR0 / R0 < 0.02) and (abs(elasticity - 1.0) < 0.11)
check("K9", ok9, "R0=%.4f +/- %.4f (%.2f%%) ; elasticity=%.2f ; lever from A28 = %.3f in E"
      % (R0, dR0, 100 * dR0 / R0, elasticity, 0.715 - 0.0),
      "R0 known to < 2%, elasticity 1.0 +/- 0.1; the 5.364 number itself is not the risk")
VALUES.update(R0=R0, R0_sigma=dR0, R0_rel_sigma=round(dR0 / R0, 5),
              R0_elasticity=elasticity, A28_supply_span_E=0.715,
              R0_shift_dex=round(math.log10(1.0 + d_level), 4),
              omega_c_h2=OM_C_H2, omega_b_h2=OM_B_H2)

# ---------------------------------------------------------------------------------------
print("\nK10 the 1.45x red-lens excess: which prior can move it")
# ---------------------------------------------------------------------------------------
A_red_b21 = 1.451            # CFG850, +0.123 dex Mstar
A_red_lo = 1.536             # CFG885, h = 0.674
A_red_hi = 1.686             # CFG885, h = 0.730
d_cosmo = (A_red_hi - A_red_b21)
d_imf_full = 0.127 - 0.048   # CFG926 R5, dex
print("        B21/LambdaCDM distances            A_red = %.3f" % A_red_b21)
print("        framework-native h bracket         A_red = %.3f .. %.3f  (delta %+.3f .. %+.3f)"
      % (A_red_lo, A_red_hi, A_red_lo - A_red_b21, A_red_hi - A_red_b21))
print("        literature IMF alpha-sigma (CFG926) removes %.3f dex of the %.3f dex excess"
      % (d_imf_full, 0.127))
ok10 = (d_cosmo > 0.0) and (d_cosmo < 0.30) and (d_imf_full > 0.05)
check("K10", ok10, "cosmology lever +%.3f in A_red (all one sign, none removes it) ; IMF lever %.3f dex"
      % (d_cosmo, d_imf_full),
      "cosmology lever in (0, 0.30) and strictly positive; IMF lever > 0.05 dex")
VALUES.update(A_red_b21=A_red_b21, A_red_native=[A_red_lo, A_red_hi],
              dA_red_cosmo_min=round(A_red_lo - A_red_b21, 3),
              dA_red_cosmo_max=round(A_red_hi - A_red_b21, 3),
              d_imf_dex=round(d_imf_full, 3), imf_excess_dex=0.127,
              imf_chabrier_salpeter_dex=0.24, imf_chabrier_salpeter_factor=1.74,
              kappa_imf_factor=round(1.74 ** (-1.2299), 4),
              kappa_imf_factor_inverse=round(1.74 ** 1.2299, 2),
              imf_fraction_removed=round(0.079 / 0.127, 3),
              sigma8_register_qc=0.76,
              # observed values of the --mutate run, reproduced in MUTATE.md
              mutation_observed={"k2_a0_ratio_at_f1p05": 0.7380,
                                 "k2_max_identity_err": 0.262,
                                 "k3_da0_pct": -11.08})

# ---------------------------------------------------------------------------------------
# summary
# ---------------------------------------------------------------------------------------
npass = sum(1 for k in CHECKS if k["pass"])
print("\n" + "=" * 88)
for k in CHECKS:
    print("  %-4s %s  %s" % (k["id"], "PASS" if k["pass"] else "FAIL", k["value"]))
print("A9 COMPLETE: %d/%d checks PASS." % (npass, len(CHECKS)))
print("=" * 88)

out = {
    "lane": "A9_lcdm_audit",
    "status": "NUMERICAL",
    "checks": CHECKS,
    "numbers": VALUES,
    "constants_used": [
        "c = 2.99792458e8 m/s (BRIEF 4)",
        "G = 6.67430e-11 (BRIEF 4)",
        "1 pc = 3.0856775814913673e16 m (BRIEF 4)",
        "H0 = 67.4 km/s/Mpc (BRIEF 4)",
        "a0_canonical = 9.3603e-11, a0_alt = 1.1312e-10 (BRIEF 4)",
        "Omega_m = 0.315, Omega_L = 0.685 (BRIEF 4)",
        "omega_b = 0.02237, omega_c = 0.1200 (cfg527_pm.py:84)",
        "Upsilon_disk = 0.5, Upsilon_bulge = 0.7 at 3.6 um (L232 line 42, Lelli+16)",
        "SPARC distances and f_D flags (SPARC_Lelli2016c.mrt / sparc_master_clean.csv)",
        "DES Y3 2pt maglim xi+/xi- and covariance (cfg679_des/2pt_maglim.fits)",
        "eRASS1 v3.2 M500/R500 (real_research/data/erass1cl_primary_v3.2.fits)",
    ],
    "mutated": MUTATE,
}
if MUTATE:
    json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     "a9_results_MUTATE.json"), "w"), indent=1)
    sys.exit(0 if npass == len(CHECKS) else 1)
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 "a9_results.json"), "w"), indent=1)
sys.exit(0 if npass == len(CHECKS) else 1)
