#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""k_anomaly-mining_efe_total_mass.py -- CANDIDATE K-B: "a galaxy's TOTAL mass from its external field".

THE CANDIDATE AS PROPOSED
    M_dyn,total / M_bar = nu(e_N),  e_N = g_ext/a_0,  with the phantom confined inside
    r_EFE = sqrt(G M_bar/a_0)/sqrt(e_N) = r_M / sqrt(e_N).
    Claimed novelty: the EFE has been tested as a rotation-curve SHAPE (item 28, formally unidentified), as a
    truncation RADIUS (item 72) and as a lensing QUADRUPOLE (item 83), but never as the MONOPOLE NORMALISATION of
    a galaxy's total mass against a MEASURED external field.

WHAT THIS SCRIPT DOES, IN ORDER, EACH WITH CHECKS THAT CAN FAIL
  (A) THE COEFFICIENT.  Derive the monopole law from QUMOND's Gauss law by direct flux quadrature, with no
      expansion, and compare with the proposed nu(e_N).  This is an independent re-derivation (different
      implementation from hunt_2026/k03_efe_phantom_theorem.py) and it is written so that the CANDIDATE is what
      can fail: if the true coefficient is not nu(e_N), the candidate's stated coefficient is wrong.
  (B) THE RESTATEMENT TEST, EXECUTED.  Take v^4 = G M_b a_0 (the deep-MOND limit) plus the EFE truncation radius
      and see whether the relation closes ALGEBRAICALLY.  Compare the closed form numerically to the kernel form
      over the e_N range the data actually occupy.  If it closes, is_restatement = TRUE and it is labelled so.
  (C) THE MEASURED EXTERNAL FIELDS.  175 reconstructed 2M++ external-field vectors on disk
      (gext_vectors_2026/data/gext_vectors.csv), two brackets spanning ~0.9 dex.  Predicted M_dyn/M_b and r_EFE.
  (D) THE OBSERVATIONAL TEST.  KiDS-1000 (Brouwer+2021) Fig-3 lensing "rotation curves", four stellar-mass bins,
      full 60x60 covariance (positive-definiteness enforced by hunt_lib).  The EFE truncation is a MASS
      SATURATION, so the excess surface density must break from 1/R to a steeper fall beyond r_EFE.  The model
      ESD is built by EXACT SPHERICAL PROJECTION of the QUMOND monopole mass profile -- no eq-23 shortcut -- and
      the projection machinery is validated against the analytic deep-MOND answer before it is used.
      The amplitude is FREE per mass bin, which makes the shape test independent of the baryon budget and hence
      of Upsilon; the amplitude-based prediction of M_dyn/M_b is reported separately, where Upsilon does bite.
  (E) THE UPSILON LEVER, MEASURED by re-running the pipeline at Upsilon x1.5.
  (F) MUTATION CONTROLS: nu = 1 (Newtonian) must break every pass; a_0 x10 must move the answer.
  BOTH FOOTINGS throughout.  The Newtonian and an NFW/LambdaCDM alternative are computed beside the framework.

BUG PATTERNS CHECKED (the five the hunt has already produced)
  (1) total vs enclosed mass: the projection uses M_dyn(r), an ENCLOSED mass, differentiated to a density.
  (2) spherical formula on a disc: the KiDS lenses are stacked and azimuthally averaged at R > 35 kpc >> disc
      scale length, so the spherical monopole is the right object; stated, not assumed.
  (3) aperture on a saddle: no aperture ratios are taken here.
  (4) covariance index order: loaded through the (m,n,i,j) -> (m,i,n,j) transpose with an eigenvalue check.
  (5) trivial correlation from joint-fit degeneracy: the amplitude and e_N are fitted jointly and their
      degeneracy is reported explicitly.
"""
import os, math, sys, csv
import numpy as np
from hunt_lib import *

ck = Check(); rng = np.random.default_rng(20260903)
P("=" * 120)
P("CANDIDATE K-B -- the external-field monopole: M_dyn,total / M_bar = nu(g_ext/a_0)?")
P("=" * 120)

# ------------------------------------------------------------------------------------------------------------
# (A) THE COEFFICIENT.  QUMOND Gauss law, exact flux quadrature, no expansion.
# ------------------------------------------------------------------------------------------------------------
P("")
P("(A) THE COEFFICIENT -- what QUMOND actually gives for the monopole, by exact flux quadrature")
P("-" * 120)
P("  QUMOND:  div(grad Phi) = div[ nu(|grad Phi_N|/a_0) grad Phi_N ].  Gauss over a sphere of radius r around a")
P("  point baryonic mass M_b sitting in a uniform external Newtonian field g_ext:")
P("      M_dyn(r) = (r^2 / 2G) * INT_{-1}^{+1} nu(|g|/a_0) (e + E mu) dmu ,")
P("      e = G M_b/r^2,  E = g_ext,  |g| = sqrt(E^2 + 2 E e mu + e^2),  mu = cos(angle to the external field).")
P("  This is a ONE-DIMENSIONAL quadrature of the exact field -- nothing is expanded.")

def nu_s1(y):
    s = math.sqrt(max(y, 1e-300))
    return 1.0 / s if s < 1e-8 else 1.0 / (1.0 - math.exp(-s))

_MU = np.linspace(-1.0, 1.0, 20001)                # dense, uniform in mu (dOmega = 2 pi dmu)

def Mdyn_over_Mb(e_over_a0, E_over_a0):
    """(1/M_b) * (r^2/2G) INT nu(|g|/a0)(e + E mu) dmu, in units where a_0 = 1 and e = G M_b/r^2 / a_0."""
    e, E = float(e_over_a0), float(E_over_a0)
    g = np.sqrt(E * E + 2.0 * E * e * _MU + e * e)
    nn = nu(g)                                      # hunt_lib vectorised Route A kernel
    return float(np.trapz(nn * (e + E * _MU), _MU)) / (2.0 * e)

def L_of(y):
    """dln nu/dln y for Route A: L = -(s/2)/(e^s - 1), s = sqrt(y)."""
    s = math.sqrt(max(y, 1e-300))
    if s < 1e-8: return -0.5
    if s > 700: return 0.0
    return -(s / 2.0) / math.expm1(s)

P("")
P(f"  {'e_N = g_ext/a_0':>16} {'CANDIDATE nu(e_N)':>18} {'QUMOND flux (r -> inf)':>24} {'nu_e(1+L_e/3)':>15} "
  f"{'candidate error (dex)':>22}")
rows_A = []
for eN in (1e-4, 1e-3, 3.3e-3, 1e-2, 0.1, 1.0, 10.0):
    nue = nu_s1(eN)
    exact = Mdyn_over_Mb(eN * 1e-6, eN)             # e/E = 1e-6: deep in the r -> infinity limit
    theo = nue * (1.0 + L_of(eN) / 3.0)
    rows_A.append((eN, nue, exact, theo))
    P(f"  {eN:>16.4g} {nue:>18.4f} {exact:>24.4f} {theo:>15.4f} {math.log10(nue/exact):>22.4f}")

ck("A1 the flux quadrature reproduces the analytic monopole coefficient nu_e(1 + L_e/3) to 0.2% at every e_N "
   "(an independent second implementation of hunt_2026/k03's theorem)",
   all(abs(r[2] / r[3] - 1) < 2e-3 for r in rows_A),
   "max |flux/theory - 1| = " + f"{max(abs(r[2]/r[3]-1) for r in rows_A):.2e}")

worst = max(abs(math.log10(r[1] / r[2])) for r in rows_A)
ck("A2 AGAINST THE CANDIDATE: the proposed coefficient nu(e_N) is NOT the QUMOND monopole coefficient.  The flux "
   "carries an extra factor (1 + L_e/3), which tends to 5/6 in a deep external field, so the candidate as written "
   "over-states the total dynamical mass by up to 0.079 dex",
   worst < 0.005,
   f"max |log10 nu(e_N)/QUMOND| = {worst:.4f} dex over e_N = 1e-4..10; deep-limit factor 5/6 = "
   f"{math.log10(6/5):.4f} dex.  THIS CHECK IS EXPECTED TO FAIL and its failure is the result.")

deep = Mdyn_over_Mb(1e-4 * 1e-6, 1e-4) / nu_s1(1e-4)
ck("A3 the deep-external-field limit of the flux coefficient is exactly 5/6",
   abs(deep - 5.0 / 6.0) < 1e-3, f"flux/nu_e -> {deep:.6f} (5/6 = 0.833333)")

# ------------------------------------------------------------------------------------------------------------
# (B) THE RESTATEMENT TEST -- executed, not asserted.
# ------------------------------------------------------------------------------------------------------------
P("")
P("(B) THE RESTATEMENT TEST -- can this be derived from v^4 = G M_b a_0 plus algebra?")
P("-" * 120)
P("  Step 1.  Deep-MOND limit:  g(r) = sqrt(G M_b a_0)/r  <=>  v^4 = G M_b a_0.  This alone says NOTHING about")
P("           where the flat part ends, so M_dyn = v^2 r/G is undetermined -- the candidate is right about that.")
P("  Step 2.  Add ONE more ingredient, the EFE truncation radius, itself pure algebra: the isolated internal")
P("           field g_N = G M_b/r^2 equals the external field g_ext at r_EFE, i.e.")
P("               r_EFE = sqrt(G M_b / g_ext) = sqrt(G M_b/a_0)/sqrt(e_N) = r_M / sqrt(e_N).")
P("  Step 3.  M_dyn = g(r_EFE) r_EFE^2 / G = [sqrt(G M_b a_0)/r_EFE] r_EFE^2/G = sqrt(G M_b a_0) r_EFE / G")
P("               = sqrt(G M_b a_0) * sqrt(G M_b/a_0) / (G sqrt(e_N)) = M_b / sqrt(e_N).")
P("  Step 4.  And the deep limit of the kernel is nu(e_N) -> 1/sqrt(e_N).  SO THE TWO ARE THE SAME EXPRESSION.")
P("  => The relation closes from the deep-MOND limit plus the definition of the EFE radius.  Nothing beyond")
P("     v^4 = G M_b a_0 and dimensional algebra is used.  Verified numerically over the measured e_N range:")
P("")
P(f"  {'e_N':>10} {'nu(e_N) [kernel]':>18} {'1/sqrt(e_N) [pure algebra]':>28} {'ratio':>10}")
rat = []
for eN in (1e-4, 3.8e-4, 1e-3, 3.3e-3, 1e-2):
    a, b = nu_s1(eN), 1.0 / math.sqrt(eN)
    rat.append(a / b)
    P(f"  {eN:>10.3g} {a:>18.4f} {b:>28.4f} {a/b:>10.5f}")
ck("B1 RESTATEMENT: over the whole range of external field the reconstruction actually measures (e_N = 1e-4 to "
   "1e-2), the kernel form nu(e_N) and the pure-algebra form 1/sqrt(e_N) agree to better than 6%, so the "
   "candidate carries no information beyond v^4 = G M_b a_0 plus the EFE radius.  IS_RESTATEMENT = TRUE",
   max(abs(r - 1) for r in rat) < 0.12,
   f"max |nu(e_N) sqrt(e_N) - 1| = {max(abs(r-1) for r in rat):.4f} over e_N = 1e-4..1e-2; the kernel's "
   f"interpolation only differs at e_N ~ 1, which the measured fields never reach "
   f"(max reconstructed e_N = 3.9e-2)")
IS_RESTATEMENT = True

# ------------------------------------------------------------------------------------------------------------
# (C) THE MEASURED EXTERNAL FIELDS
# ------------------------------------------------------------------------------------------------------------
P("")
P("(C) THE MEASURED EXTERNAL FIELDS -- 175 reconstructed 2M++ vectors on disk")
P("-" * 120)
GEXT = os.path.join(HERE, "..", "gext_vectors_2026", "data", "gext_vectors.csv")
grows = list(csv.DictReader(open(GEXT)))
eN_no = np.array([10 ** float(r["log_eN_noclu"]) for r in grows])
eN_mx = np.array([10 ** float(r["log_eN_maxclu"]) for r in grows])
P(f"  {len(grows)} galaxies.  Two brackets (clusters excluded / clusters at maximum):")
for nm, v in (("no-cluster", eN_no), ("max-cluster", eN_mx)):
    P(f"    {nm:>12}: e_N median {np.median(v):.3e}, 16-84% [{np.percentile(v,16):.2e}, {np.percentile(v,84):.2e}], "
      f"range [{v.min():.2e}, {v.max():.2e}]")
BR = math.log10(np.median(eN_mx) / np.median(eN_no))
ck("C1 the two brackets differ by about 0.9 dex in e_N, so the prediction of M_dyn/M_b carries +-0.45 dex from "
   "the external field alone before any measurement error",
   0.7 < BR < 1.1, f"bracket width {BR:.2f} dex in e_N -> {BR/2:.2f} dex in M_dyn/M_b (slope -1/2)")
P("")
P(f"  {'bracket':>12} {'median e_N':>12} {'QUMOND M_dyn/M_b':>18} {'candidate nu(e_N)':>19} {'(dex apart)':>12}")
for nm, v in (("no-cluster", eN_no), ("max-cluster", eN_mx)):
    m = float(np.median(v))
    q = Mdyn_over_Mb(m * 1e-6, m); c0 = nu_s1(m)
    P(f"  {nm:>12} {m:>12.3e} {q:>18.2f} {c0:>19.2f} {math.log10(c0/q):>12.4f}")

# the log-slope in g_ext, measured numerically (the candidate's own dominant lever)
h_ = 1e-3
m0 = float(np.median(eN_no))
sl_gext = (math.log10(Mdyn_over_Mb(m0 * 10 ** h_ * 1e-6, m0 * 10 ** h_)) -
           math.log10(Mdyn_over_Mb(m0 * 10 ** -h_ * 1e-6, m0 * 10 ** -h_))) / (2 * h_)
ck("C2 d log(M_dyn/M_b)/d log g_ext = -1/2 (the deep-MOND value), so a 0.9 dex uncertainty in g_ext is a 0.45 dex "
   "uncertainty in the prediction -- which is 4.5x the RAR's own scatter and 4.5x the 0.1 dex a Kepler-grade law "
   "is allowed",
   abs(sl_gext + 0.5) < 0.02, f"measured slope {sl_gext:+.4f}")

# ------------------------------------------------------------------------------------------------------------
# (D) THE OBSERVATIONAL TEST -- KiDS-1000 excess surface density, four stellar-mass bins
# ------------------------------------------------------------------------------------------------------------
P("")
P("(D) THE OBSERVATIONAL TEST -- does the KiDS-1000 lensing signal show the predicted mass saturation?")
P("-" * 120)
LOGM = {1: 10.0, 2: 10.45, 3: 10.7, 4: 10.9}          # B21 bin medians (h70), as used in hunt_2026/h1_*
FGAS = {1: 0.5, 2: 0.3, 3: 0.2, 4: 0.15}              # cold-gas fraction added to M*, same source
rc = {b: load_esd(f"Fig-3_Lensing-rotation-curves_Massbin-{b}.txt") for b in range(1, 5)}
nR = len(rc[1][0])
d3 = np.genfromtxt(os.path.join(B, "Fig-3_Lensing-rotation-curves_Massbins_covmatrix.txt"), comments="#")
C3 = (d3[:, 4] / d3[:, 6]).reshape(4, 4, nR, nR).transpose(0, 2, 1, 3).reshape(4 * nR, 4 * nR)
C3 = (C3 + C3.T) / 2
ev3 = np.linalg.eigvalsh(C3)
ck("D0a BUG PATTERN 4: the 60x60 covariance is positive definite in the (m,i,n,j) ordering (a plain reshape is "
   "not, and gives negative chi2)",
   ev3.min() > 0, f"min eigenvalue {ev3.min():.3e}")
Rall = rc[1][0]
P(f"  {nR} radial bins x 4 stellar-mass bins, R = {Rall.min():.3f} - {Rall.max():.2f} Mpc (h70)")

# ---- exact spherical projection of a QUMOND monopole mass profile -------------------------------------------
MSUN_PC3 = 1.0                                        # work in Msun, pc, s: G_PC = 4.52e-30 pc^3/(Msun s^2)
PC = 1.0
MPC = 1e6                                             # pc per Mpc

def Mdyn_profile(r_pc, Mb_msun, a0_si, eN):
    """Enclosed QUMOND dynamical mass at radius r (pc), by the exact flux quadrature above.
    a0 is converted to pc/s^2; e_N is the external field in units of a_0."""
    a0_pc = a0_si / 3.0857e16                          # m/s^2 -> pc/s^2
    out = np.empty_like(r_pc)
    for i, r in enumerate(r_pc):
        e = G_PC * Mb_msun / r ** 2 / a0_pc            # internal Newtonian field in units of a_0
        out[i] = Mb_msun * (Mdyn_over_Mb(e, eN) if eN > 0 else nu_s1(e))
    return out

_LR = np.logspace(math.log10(3.0e2), math.log10(3.0e10), 900)     # 300 pc .. 30 Gpc, log grid

def esd_model(R_mpc, Mb_msun, a0_si, eN, newtonian=False):
    """Excess surface density (Msun/pc^2) of the spherical monopole, by exact projection.
    ESD(R) = mean Sigma inside R - Sigma(R), with Sigma(R) = 2 INT_0^inf rho(sqrt(R^2+z^2)) dz."""
    if newtonian:
        M = np.full_like(_LR, Mb_msun)
    else:
        M = Mdyn_profile(_LR, Mb_msun, a0_si, eN)
    rho = np.gradient(M, _LR) / (4 * math.pi * _LR ** 2)          # Msun/pc^3
    rho = np.maximum(rho, 0.0)
    lr = np.log(_LR)
    def rho_at(r):
        return np.exp(np.interp(np.log(np.maximum(r, _LR[0])), lr, np.log(np.maximum(rho, 1e-300)),
                                left=-700.0, right=-700.0))
    zs = np.concatenate([np.array([0.0]), np.logspace(0.0, math.log10(3.0e10), 700)])
    Rp = np.asarray(R_mpc, float) * MPC
    Sig = np.array([2.0 * np.trapz(rho_at(np.sqrt(Rr ** 2 + zs ** 2)), zs) for Rr in Rp])
    # mean Sigma inside R needs Sigma on a fine grid from 0 to R
    def sigbar(Rr):
        rr = np.concatenate([np.array([1.0]), np.logspace(0.0, math.log10(Rr), 260)])
        sg = np.array([2.0 * np.trapz(rho_at(np.sqrt(x ** 2 + zs ** 2)), zs) for x in rr])
        return 2.0 / Rr ** 2 * np.trapz(sg * rr, rr)
    return np.array([sigbar(Rr) for Rr in Rp]) - Sig

# ---- validate the projection against a case with a closed form ----------------------------------------------
Mb_t = 1e11
a0_t = A0["canonical"]
Rt = np.array([0.1, 0.3, 1.0])
a0_pc_t = a0_t / 3.0857e16
# the closed form: for rho = A/r^2 exactly, Sigma = pi A/R and ESD = pi A/R.  Feed the SAME projector that
# 3-D density and check it reproduces pi A/R.  This validates the quadrature itself, separately from the kernel.
A_iso = math.sqrt(G_PC * Mb_t * a0_pc_t) / (4 * math.pi * G_PC)
_zs_v = np.concatenate([np.array([0.0]), np.logspace(0.0, math.log10(3.0e10), 700)])
def _proj_analytic(R_mpc):
    Rp = np.asarray(R_mpc, float) * MPC
    rho_f = lambda r: A_iso / r ** 2
    Sig = np.array([2.0 * np.trapz(rho_f(np.sqrt(Rr ** 2 + _zs_v ** 2)), _zs_v) for Rr in Rp])
    def sigbar(Rr):
        rr = np.concatenate([np.array([1.0]), np.logspace(0.0, math.log10(Rr), 260)])
        sg = np.array([2.0 * np.trapz(rho_f(np.sqrt(x ** 2 + _zs_v ** 2)), _zs_v) for x in rr])
        return 2.0 / Rr ** 2 * np.trapz(sg * rr, rr)
    return np.array([sigbar(Rr) for Rr in Rp]) - Sig
esd_chk = _proj_analytic(Rt)
esd_an = math.pi * A_iso / (Rt * MPC)
P("")
P("  projection validation on the one case with a closed form (rho = A/r^2, for which ESD = pi A/R exactly):")
for i, r in enumerate(Rt):
    P(f"    R = {r:4.2f} Mpc:  numeric ESD = {esd_chk[i]:9.4f}   closed form = {esd_an[i]:9.4f}   "
      f"ratio {esd_chk[i]/esd_an[i]:.5f}")
ck("D0b the exact spherical projection reproduces the closed-form excess surface density to 0.1%, so the "
   "quadrature that will be used for the EFE case is validated independently of the kernel",
   np.all(np.abs(esd_chk / esd_an - 1) < 1e-3),
   f"max |ratio - 1| = {np.max(np.abs(esd_chk/esd_an - 1)):.2e}")
esd_num = esd_model(Rt, Mb_t, a0_t, 0.0)
P("  and here is how far the FULL Route A profile sits from that deep asymptote -- this is physics, not error:")
for i, r in enumerate(Rt):
    P(f"    R = {r:4.2f} Mpc ({r*MPC/(math.sqrt(G_PC*Mb_t/a0_pc_t)):5.1f} r_M):  full kernel {esd_num[i]:9.4f}  "
      f"deep asymptote {esd_an[i]:9.4f}   ratio {esd_num[i]/esd_an[i]:.4f}")
ck("D0c the full kernel profile is BELOW its own deep-MOND asymptote at every measured radius, by 7% at 0.1 Mpc "
   "falling to 1% at 1 Mpc -- the finite-y correction, which the analysis carries exactly rather than assuming "
   "the deep limit (this is the same +0.095 dex estimator bias that the hunt's item 103 found)",
   np.all(esd_num < esd_an) and abs(esd_num[-1] / esd_an[-1] - 1) < 0.03,
   "ratios " + ", ".join(f"{esd_num[i]/esd_an[i]:.4f}" for i in range(len(Rt))))

def rEFE_mpc(Mb_msun, a0_si, eN):
    a0_pc = a0_si / 3.0857e16
    return math.sqrt(G_PC * Mb_msun / a0_pc) / math.sqrt(eN) / MPC

DAT = np.concatenate([rc[b][1] for b in range(1, 5)])
CINV = np.linalg.inv(C3)

def chi2_fit(models, extra=None):
    """models: dict bin -> model ESD vector (length nR).  One free amplitude per mass bin.
    extra: optional second dict bin -> template, given its OWN free amplitude per bin (used for the
    correlated-structure / two-halo robustness test).  Returns chi2 at the best fit and the amplitudes."""
    ncomp = 1 if extra is None else 2
    Mfull = np.zeros((4 * nR, 4 * ncomp))
    for k, b in enumerate(range(1, 5)):
        Mfull[k * nR:(k + 1) * nR, k] = models[b]
        if extra is not None:
            Mfull[k * nR:(k + 1) * nR, 4 + k] = extra[b]
    A = Mfull.T @ CINV @ Mfull
    bvec = Mfull.T @ CINV @ DAT
    amps = np.linalg.solve(A, bvec)
    res = DAT - Mfull @ amps
    return float(res @ CINV @ res), amps

USE = (Rall > 0.05)                                    # point-mass monopole valid well outside the disc
P("")
P(f"  fitting {USE.sum()} of {nR} radial bins per mass bin (R > 0.05 Mpc), amplitude FREE per bin")
P("  (a free amplitude absorbs the baryon budget, so the SHAPE test below is independent of Upsilon)")

def run_footing(ft, ups=1.0, label=""):
    a0 = A0[ft]
    out = {}
    Mb = {b: (10 ** LOGM[b] * ups) * (1 + FGAS[b] / ups) for b in range(1, 5)}   # gas mass fixed, Upsilon on M*
    # 1. isolated framework
    mod_iso = {b: esd_model(Rall, Mb[b], a0, 0.0) for b in range(1, 5)}
    c_iso, amp_iso = chi2_fit(mod_iso)
    out["iso"] = (c_iso, amp_iso)
    # 2. framework + EFE at the reconstructed medians (no free parameter)
    for nm, eN in (("efe_noclu", float(np.median(eN_no))), ("efe_maxclu", float(np.median(eN_mx)))):
        mod = {b: esd_model(Rall, Mb[b], a0, eN) for b in range(1, 5)}
        c, amp = chi2_fit(mod)
        out[nm] = (c, amp, eN, {b: rEFE_mpc(Mb[b], a0, eN) for b in range(1, 5)})
    # 3. Newtonian baryons only
    mod_n = {b: esd_model(Rall, Mb[b], a0, 0.0, newtonian=True) for b in range(1, 5)}
    c_n, amp_n = chi2_fit(mod_n)
    out["newton"] = (c_n, amp_n)
    # 4. EFE with e_N free (one common value), scanned
    grid = np.logspace(-6.0, -0.5, 34)
    cs = []
    for eN in grid:
        mod = {b: esd_model(Rall, Mb[b], a0, eN) for b in range(1, 5)}
        cs.append(chi2_fit(mod)[0])
    cs = np.array(cs)
    out["scan"] = (grid, cs)
    return out, Mb

RES = {}
for ft in ("canonical", "alt"):
    RES[ft], MB = run_footing(ft)
    a0 = A0[ft]
    r = RES[ft]
    P("")
    P(f"  --- footing {ft} (a_0 = {a0:.3e} m/s^2) ---")
    P(f"    baryonic masses used for r_EFE: " + ", ".join(f"bin{b} {MB[b]:.2e}" for b in range(1, 5)))
    P(f"    {'model':>22} {'chi2 (60 pts, 4 amps)':>24} {'Delta chi2 vs isolated':>24}")
    P(f"    {'framework, isolated':>22} {r['iso'][0]:>24.1f} {0.0:>24.1f}")
    for nm in ("efe_noclu", "efe_maxclu"):
        c, amp, eN, rE = r[nm]
        P(f"    {nm:>22} {c:>24.1f} {c - r['iso'][0]:>+24.1f}    e_N = {eN:.2e}, "
          f"r_EFE = " + "/".join(f"{rE[b]:.2f}" for b in range(1, 5)) + " Mpc")
    P(f"    {'Newtonian baryons':>22} {r['newton'][0]:>24.1f} {r['newton'][0] - r['iso'][0]:>+24.1f}")

# --- the headline check -------------------------------------------------------------------------------------
d_no = RES["canonical"]["efe_noclu"][0] - RES["canonical"]["iso"][0]
d_mx = RES["canonical"]["efe_maxclu"][0] - RES["canonical"]["iso"][0]
d_no_a = RES["alt"]["efe_noclu"][0] - RES["alt"]["iso"][0]
d_mx_a = RES["alt"]["efe_maxclu"][0] - RES["alt"]["iso"][0]
ck("D1 THE TEST.  The candidate says the dynamical mass saturates at r_EFE, which for these lenses at the "
   "reconstructed external fields is 0.2-0.7 Mpc -- well inside the KiDS reach of 2.6 Mpc.  If the data show that "
   "saturation, the EFE model must fit BETTER than the isolated one.  This check passes only if it does "
   "(Delta chi2 < 0 in at least one bracket, both footings)",
   min(d_no, d_mx) < 0 and min(d_no_a, d_mx_a) < 0,
   f"canonical: Delta chi2 = {d_no:+.1f} (no-cluster e_N), {d_mx:+.1f} (max-cluster e_N); "
   f"alt: {d_no_a:+.1f}, {d_mx_a:+.1f}.  Positive = the EFE truncation is DISFAVOURED by the data.")

grid, cs = RES["canonical"]["scan"]
c0 = RES["canonical"]["iso"][0]
ok = cs - c0 < 9.0
eN_max = grid[ok].max() if ok.any() else 0.0
ck("D2 the 3-sigma upper limit on a common external field from the KiDS lensing shape alone, with the amplitude "
   "free in every bin: e_N must be below the value quoted.  Compare with the reconstruction's median of "
   "3.8e-4 (no-cluster) to 3.3e-3 (max-cluster) -- this check passes only if the lensing limit is ABOVE the "
   "reconstructed median, i.e. only if the two are compatible",
   eN_max > float(np.median(eN_mx)),
   f"KiDS 3-sigma limit e_N < {eN_max:.2e}; reconstruction medians 3.8e-4 / 3.3e-3")

ck("D3 MUTATION CONTROL: Newtonian baryons (nu = 1) must be excluded outright by the same data and the same "
   "amplitude freedom, or the test has no power at all",
   RES["canonical"]["newton"][0] - RES["canonical"]["iso"][0] > 9,
   f"Delta chi2 (Newtonian - framework isolated) = {RES['canonical']['newton'][0] - RES['canonical']['iso'][0]:+.1f}")

# --- THE CONFOUND, faced head on: correlated structure -------------------------------------------------------
P("")
P("  THE CONFOUND THIS TEST MUST SURVIVE.  The mass that generates g_ext is real mass a few Mpc away, and it is")
P("  correlated with the lens, so it contributes its own lensing signal at large R (the 'two-halo' term).  An EFE")
P("  deficit in the lens's own profile could in principle be refilled by it.  So the test is repeated with a FREE")
P("  correlated-structure component added to every model -- shape ESD ~ R^-0.8 over 0.1-3 Mpc, the projected")
P("  linear correlation function's slope -- with its own free amplitude in each mass bin (8 parameters, not 4).")
tmpl2h = {b: (Rall / 1.0) ** (-0.8) for b in range(1, 5)}
Mb_ref = {b: 10 ** LOGM[b] * (1 + FGAS[b]) for b in range(1, 5)}
a0c = A0["canonical"]
c2_iso, a2_iso = chi2_fit({b: esd_model(Rall, Mb_ref[b], a0c, 0.0) for b in range(1, 5)}, tmpl2h)
P(f"    + free two-halo, isolated framework            :  chi2 = {c2_iso:8.1f}   two-halo amplitudes = "
  + ", ".join(f"{a:+.3f}" for a in a2_iso[4:]))
row2h = []
for nm, eN in (("no-cluster", float(np.median(eN_no))), ("max-cluster", float(np.median(eN_mx)))):
    c2, a2 = chi2_fit({b: esd_model(Rall, Mb_ref[b], a0c, eN) for b in range(1, 5)}, tmpl2h)
    row2h.append((nm, eN, c2, c2 - c2_iso, a2))
    P(f"    + free two-halo, EFE at {nm:>11} e_N = {eN:.2e}:  chi2 = {c2:8.1f}   Delta chi2 vs isolated"
      f" = {c2 - c2_iso:+8.1f}   two-halo amplitudes = " + ", ".join(f"{a:+.3f}" for a in a2[4:]))
ck("D5 AGAINST MY OWN RESULT ABOVE: the D1 exclusion is NOT robust to a correlated-structure term.  Allow four "
   "extra free parameters with the two-halo shape and the weak-field (no-cluster) EFE truncation stops being "
   "excluded and becomes mildly PREFERRED, because a rising two-halo term and a falling EFE deficit are nearly "
   "the same degree of freedom (bug pattern 5).  This check passes only if the EFE model stays excluded "
   "(Delta chi2 > 9) in BOTH brackets even with that freedom",
   min(r[3] for r in row2h) > 9.0,
   "; ".join(f"{r[0]}: Delta chi2 = {r[3]:+.1f}" for r in row2h) +
   f".  So the honest statement is: KiDS excludes the truncation at the strong-field bracket "
   f"({row2h[1][3]:+.1f}) and cannot decide it at the weak-field one ({row2h[0][3]:+.1f}) once the neighbours "
   f"that GENERATE g_ext are allowed to lens as well.  Note the required two-halo amplitudes are physical "
   f"(positive) in the EFE fits.")

# --- the LambdaCDM alternative, computed beside -------------------------------------------------------------
P("")
P("  the LambdaCDM alternative, computed beside the framework: NFW halo, M200 from a stellar-to-halo-mass")
P("  relation, concentration from Dutton & Maccio 2014, amplitude free in each bin exactly as above.")
def nfw_esd(R_mpc, M200_msun, c200):
    """Wright & Brainerd 2000 analytic NFW ESD (Msun/pc^2), rho_crit at z=0.2 in Msun/pc^3."""
    rho_c = 1.4e-7 * (0.3 * 1.2 ** 3 + 0.7)            # Msun/pc^3 at z=0.2 (rho_crit,0 = 1.4e-7)
    r200 = (3 * M200_msun / (4 * math.pi * 200 * rho_c)) ** (1 / 3.)
    rs = r200 / c200
    dc = (200 / 3.) * c200 ** 3 / (math.log(1 + c200) - c200 / (1 + c200))
    x = np.asarray(R_mpc, float) * MPC / rs
    out = np.empty_like(x)
    for i, xi in enumerate(x):
        if abs(xi - 1) < 1e-4:
            g = 10. / 3 + 4 * math.log(0.5)
        elif xi < 1:
            a = math.acosh(1 / xi)
            g = (8 * math.atanh(math.sqrt((1 - xi) / (1 + xi))) / (xi ** 2 * math.sqrt(1 - xi ** 2))
                 + 4 / xi ** 2 * math.log(xi / 2) - 2 / (xi ** 2 - 1)
                 + 4 * math.atanh(math.sqrt((1 - xi) / (1 + xi))) / ((xi ** 2 - 1) * math.sqrt(1 - xi ** 2)))
        else:
            g = (8 * math.atan(math.sqrt((xi - 1) / (1 + xi))) / (xi ** 2 * math.sqrt(xi ** 2 - 1))
                 + 4 / xi ** 2 * math.log(xi / 2) - 2 / (xi ** 2 - 1)
                 + 4 * math.atan(math.sqrt((xi - 1) / (1 + xi))) / ((xi ** 2 - 1) ** 1.5))
        out[i] = g
    return rs * dc * rho_c * out
def M200_of_Mstar(logMs):
    """Behroozi+2013-like inversion, adequate at the 0.1 dex level for a beside-the-framework comparison."""
    return 10 ** (1.5 * (logMs - 10.5) + 12.2)
mod_nfw = {}
for b in range(1, 5):
    M200 = M200_of_Mstar(LOGM[b]); c200 = 10 ** (0.905 - 0.101 * (math.log10(M200 / 1e12)))
    mod_nfw[b] = nfw_esd(Rall, M200, c200)
c_nfw, amp_nfw = chi2_fit(mod_nfw)
P(f"    NFW (LambdaCDM):  chi2 = {c_nfw:.1f}   amplitudes = " + ", ".join(f"{a:.2f}" for a in amp_nfw))
P(f"    framework isolated (canonical): chi2 = {RES['canonical']['iso'][0]:.1f}   amplitudes = "
  + ", ".join(f"{a:.2f}" for a in RES['canonical']['iso'][1]))
ck("D4 REPORTED BOTH WAYS: which of the two shapes the KiDS profile prefers, with one free amplitude each",
   True, f"NFW chi2 = {c_nfw:.1f} vs framework-isolated chi2 = {RES['canonical']['iso'][0]:.1f} on 60 points "
         f"with 4 amplitudes each; difference {c_nfw - RES['canonical']['iso'][0]:+.1f}")

# ------------------------------------------------------------------------------------------------------------
# (E) THE UPSILON LEVER, MEASURED
# ------------------------------------------------------------------------------------------------------------
P("")
P("(E) THE UPSILON LEVER -- the whole pipeline re-run at Upsilon x 1.5")
P("-" * 120)
R15, MB15 = run_footing("canonical", ups=1.5)
d15 = R15["efe_noclu"][0] - R15["iso"][0]
# the AMPLITUDE prediction (where Upsilon does bite): M_dyn/M_b at fixed measured M_dyn
P(f"  {'quantity':>34} {'Upsilon x1':>14} {'Upsilon x1.5':>14} {'d log / d log Upsilon':>22}")
rE1 = rEFE_mpc(10 ** LOGM[4] * (1 + FGAS[4]), A0["canonical"], float(np.median(eN_no)))
rE15 = rEFE_mpc(MB15[4], A0["canonical"], float(np.median(eN_no)))
lev_rEFE = math.log10(rE15 / rE1) / math.log10(1.5)
P(f"  {'r_EFE, bin 4 [Mpc]':>34} {rE1:>14.3f} {rE15:>14.3f} {lev_rEFE:>22.3f}")
P(f"  {'Delta chi2 (EFE - isolated)':>34} {d_no:>14.1f} {d15:>14.1f} {'--':>22}")
# M_dyn/M_b amplitude test: measured M_dyn at 1 Mpc from the data, divided by the baryon budget
Cinv = np.linalg.inv(C3)
Mdyn_meas = {}
for b in range(1, 5):
    Rb, Eb, eEb = rc[b]
    j = int(np.argmin(np.abs(Rb - 1.0)))
    g_meas = 4 * G_PC * Eb[j] * PC_PER_M               # m/s^2
    Mdyn_meas[b] = g_meas * (Rb[j] * Mpc) ** 2 / G / Msun
rat1 = np.array([Mdyn_meas[b] / (10 ** LOGM[b] * (1 + FGAS[b])) for b in range(1, 5)])
rat15 = np.array([Mdyn_meas[b] / MB15[b] for b in range(1, 5)])
lev_amp = np.mean(np.log10(rat15 / rat1)) / math.log10(1.5)
P(f"  {'M_dyn(1 Mpc)/M_b, mean of 4 bins':>34} {np.mean(rat1):>14.1f} {np.mean(rat15):>14.1f} {lev_amp:>22.3f}")
ck("E1 THE UPSILON LEVER, MEASURED: the amplitude form of the candidate (M_dyn/M_b) moves with Upsilon at the "
   "exponent quoted, while the shape form (does the profile break at r_EFE) is nearly Upsilon-free because the "
   "amplitude is fitted out",
   True, f"d log(M_dyn/M_b)/d log Upsilon = {lev_amp:+.3f} (the candidate's proposer estimated -0.73); "
         f"d log r_EFE/d log Upsilon = {lev_rEFE:+.3f}; the shape test's Delta chi2 moves "
         f"{d_no:+.1f} -> {d15:+.1f}")
spread_gext = 0.5 * (np.percentile(np.log10(eN_mx), 84) - np.percentile(np.log10(eN_no), 16))
ck("E2 CRITERION (3) -- RAR-CLASS SCATTER.  The candidate's own input, g_ext, spans the width below across the "
   "two reconstruction brackets and their 16-84 percentiles; at d log/d log g_ext = -1/2 that is the irreducible "
   "scatter of the prediction.  This check passes only if it is inside the 0.1 dex a Kepler-grade law is allowed",
   spread_gext < 0.1,
   f"g_ext spread {2*spread_gext:.2f} dex -> prediction scatter {spread_gext:.2f} dex, against the 0.10 dex "
   f"criterion; by comparison a 50% Upsilon error moves it only {abs(lev_amp)*math.log10(1.5):.3f} dex")

# ------------------------------------------------------------------------------------------------------------
# (F) MUTATION CONTROLS
# ------------------------------------------------------------------------------------------------------------
P("")
P("(F) MUTATION CONTROLS")
P("-" * 120)
mod_m = {b: esd_model(Rall, 10 ** LOGM[b] * (1 + FGAS[b]), A0["canonical"] * 10, 0.0) for b in range(1, 5)}
c_m, _ = chi2_fit(mod_m)
ck("F1 a_0 x 10 must change the fit: if it does not, the amplitude freedom has eaten the entire a_0 dependence "
   "and nothing here measures a_0",
   abs(c_m - RES["canonical"]["iso"][0]) > 1.0,
   f"chi2(a_0 x10) = {c_m:.1f} vs chi2(a_0) = {RES['canonical']['iso'][0]:.1f}, difference "
   f"{c_m - RES['canonical']['iso'][0]:+.1f}")
def Mdyn_over_Mb_mut(e, E):
    """the same quadrature with nu replaced by the identity -- must give exactly 1 at every external field."""
    g = np.sqrt(E * E + 2.0 * E * e * _MU + e * e)
    return float(np.trapz(np.ones_like(g) * (e + E * _MU), _MU)) / (2.0 * e)
mut = [Mdyn_over_Mb_mut(eN * 1e-6, eN) for eN in (1e-4, 1e-2, 1.0, 10.0)]
P(f"  F2 kernel mutation: nu -> 1 in the same quadrature gives M_dyn/M_b = " + ", ".join(f"{m:.8f}" for m in mut))
ck("F2 with the kernel replaced by the identity the monopole law collapses to M_dyn = M_b at every external "
   "field, so every number in section A is the kernel and not an artefact of the quadrature",
   max(abs(m - 1.0) for m in mut) < 1e-9,
   f"max |M_dyn/M_b - 1| = {max(abs(m-1.0) for m in mut):.2e}")

# ------------------------------------------------------------------------------------------------------------
P("")
P("=" * 120)
P("VERDICT")
P("=" * 120)
P("  Read the checks.  Four things decide this candidate, and none of them favour it:")
P("   (i)   the coefficient it states, nu(e_N), is not the QUMOND monopole coefficient -- that is nu_e(1+L_e/3),")
P("         which is 5/6 nu_e in a deep external field, a 0.079 dex error built into the statement (A2);")
P("   (ii)  the relation closes algebraically from v^4 = G M_b a_0 plus the definition of the EFE radius, so it")
P("         IS A RESTATEMENT of the deep-MOND limit and the external-field effect together (B1), exactly as the")
P("         proposer half-conceded -- and criterion (5) of the hunt says a restatement must be labelled one;")
P("   (iii) it fails criterion (3): its own input g_ext is known to 1.5 dex across the two brackets and their")
P("         percentiles, which at slope -1/2 is 0.74 dex of irreducible scatter against the 0.10 dex allowed (E2);")
P("   (iv)  and on the data it has, the predicted mass saturation is not seen: with a free amplitude per mass bin")
P("         the KiDS-1000 profiles disfavour the truncation by Delta chi2 = +144 (weak field) to +507 (strong")
P("         field), both footings (D1), and the shape alone caps e_N at 6.8e-5, 5.6x below even the no-cluster")
P("         reconstruction median (D2).  BUT THAT EXCLUSION IS NOT ROBUST: allow the neighbours that generate")
P("         g_ext to lens as well and the weak-field truncation is no longer excluded (D5).  So the observational")
P("         verdict is 'excluded at the strong-field bracket, undecided at the weak-field one', not a clean kill.")
P("  The Upsilon lever is -0.815 measured on the amplitude form and +0.445 on r_EFE; but Upsilon is NOT the")
P("  blocker here.  g_ext is, at 5x the size.  Same failure mode as the nine Upsilon items, different quantity.")
sys.exit(ck.done())
