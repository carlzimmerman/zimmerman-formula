#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG54 -- A PRE-REGISTERED a0(z) CHECK ON THE PHIBSS z ~ 1-2 SAMPLE (Tacconi+2013 joined table): flat a0 (the framework's branch A) against a0 * E(z) (the H(z)-tracking rival).

WHY.  CFG52 found that no clean object on disk has g_bar < 0.3 a0 at z >= 1.5, and that the deepest sample (MUSE-DARK II, z ~ 1.2) is gas-dominated.  The data-assembly
thread (commit fa93fe736, data_assembly/kmos3d_phibss/) joined Tacconi+2013's tables 1 and 2 (73 galaxies at z ~ 1.2 and 2.2, direct CO gas masses, Vrot for 65) and found
KMOS3D and PHIBSS do not overlap.  This lane runs the one check that sample allows, with every criterion FROZEN BEFORE THE FIRST RUN.  An empty or non-diagnostic
result is a valid result.

FROZEN CRITERIA (declared before this script's first run; nothing below is tuned afterwards).
  Sample S0: rows of data_assembly/kmos3d_phibss/phibss13_joined.csv with a rotation velocity, a half-light radius (rh_opt_kpc, else rh_co_kpc), a redshift z_co, mbar_is_upper_limit
      = 0, co_upper_limit = 0 and fgas_inconsistent_in_source = 0.  (Six gas masses are 3-sigma upper limits and three rows quote an fgas their masses do not reproduce: excluded.)
  Baryons: an exact Freeman exponential disc of mass M_bar = M_* + M_mol (the table's mbar_msun) with R_d = r_h / 1.68 (as CFG52).
  Velocity radius (declared assumption; the table does not tabulate it): r_v = 2.2 R_d = 1.31 r_h, the ledger's convention (v at 2.2 R_d).  Brackets, used only for the floor: r_v = 1.0 r_h
      and 2.0 r_h.  MISMATCH stated: Tacconi+2013's own velocities are CO or H-alpha rotation velocities with the inclination and pressure corrections they applied (a sigma0 term
      is not applied here); the ledger's convention is not identical to theirs.
  Selection S1: g_bar(r_v) < a0 (canonical, disc model).  Selection is on the baryonic acceleration, which does not use the velocity.
  Predictions: g_flat = nu_mono(g_bar/a0) g_bar (canonical a0 = 9.3603e-11 m/s^2); g_rival = nu_mono(g_bar/(a0 E(z))) g_bar with E(z) = sqrt(0.3138 (1+z)^3 + 0.6862) at the galaxy's z_co.
  Observed: g_obs = v^2/r_v.  Offset Delta = log10(g_obs/g_pred) for each law.
  Errors: velocity 25% (the table quotes 20-30%) -> 2 x 0.25/ln 10 = 0.217 dex per galaxy in g_obs; mass 0.20 dex, CORRELATED across the sample (Mmol 50% and M* 30% systematics),
      propagated through the slope d log g_pred / d log g_bar; the sample mean's error = the quadrature of (velocity scatter / sqrt N) and (the correlated mass term) and (half the
      spread of the mean over the three velocity radii).  The mean's significance is against this total.
  H0  [FEASIBILITY GATE] the selected sample has N >= 5.  If not, the lane is declared NON-DIAGNOSTIC (reported plainly, no hypothesis is scored).
  H1  flat a0 fits: |mean Delta_flat| < 2 sigma_tot.        H2  the rival fits: |mean Delta_rival| < 2 sigma_tot.
  H3  [HEADLINE; MUTATE must fail] the sample can DISCRIMINATE the two laws: |mean Delta_flat - mean Delta_rival| > 2 sigma_tot.
  R1-R3 (reported): the selection-bias mock (mass noise 0.20 dex, reselect on the noisy g_bar, truth = flat law); the discs-only subsample; N and the g_bar / a0 range; the
      z ~ 1.2 and z ~ 2.2 halves.
  READING (declared): H0 FAIL -> non-diagnostic.  H0 PASS, H3 FAIL -> the sample is too small or too uncertain to discriminate (CFG52's forecast: the calibration systematic caps
      the significance near 2.3 sigma).  H3 PASS -> the sample discriminates, and whichever of H1 / H2 holds is the verdict; a verdict is subject to the selection-bias mock.
MUTATE=1: the observed velocities are multiplied by 0.5 -- H1 and H2 must FAIL (rc = 1).  NOTE (disclosed after the run): the selection precedes the velocities, so if H0 fails
  H1/H2 are never scored and the control is vacuous; the mutated run then fails H0 exactly as the main run does.
Run: python3 campaign_fresh_gravity/CFG54_phibss_a0z.py   (MUTATE=1 for the control)
"""
import os, sys, math, csv
import numpy as np
from scipy.special import i0, i1, k0, k1

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import CFG7_common as C
MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C.Report("CFG54_phibss_a0z", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: observed velocities x 0.5 -- H1 and H2 must FAIL ***")
VF = 0.5 if MUTATE else 1.0
G, MSUN, KPC = 6.6743e-11, 1.98847e30, 3.0856775814913673e19
A0 = 9.3603e-11
OM = 0.3138
E = lambda z: math.sqrt(OM * (1 + z) ** 3 + 1 - OM)
nu = lambda y: float(C.nu_mono(np.array([y]))[0])
SIGV = 2 * 0.25 / math.log(10)
SIGM = 0.20


def g_disc(M, r, rh):
    Rd = rh / 1.68; y = r / (2 * Rd)
    v2 = 2 * G * M * MSUN / (Rd * KPC) * y * y * (i0(y) * k0(y) - i1(y) * k1(y))
    return v2 / (r * KPC)


ROWS = list(csv.DictReader(open(os.path.join(C.REPO, "data_assembly", "kmos3d_phibss", "phibss13_joined.csv"))))
f = lambda x: (float(x) if x not in ("", "nan", "NaN") else None)
S0 = []
for r in ROWS:
    v = f(r["vrot_kms"]); rh = f(r["rh_opt_kpc"]) or f(r["rh_co_kpc"]); z = f(r["z_co"]); M = f(r["mbar_msun"])
    if v is None or rh is None or z is None or M is None:
        continue
    if r["mbar_is_upper_limit"] != "0" or r["co_upper_limit"] != "0" or r["fgas_inconsistent_in_source"] != "0":
        continue
    S0.append(dict(name=r["name"], type=r["type"], v=v * VF, rh=rh, z=z, M=M))

R.banner("SAMPLE")
check("C1 CONTROL: the table has 73 rows; S0 keeps only measured, consistent rows with a velocity, radius and redshift",
      f"{len(ROWS)} rows; S0 = {len(S0)} (6 gas upper limits and 3 inconsistent-fgas rows excluded by rule)", len(ROWS) == 73 and 0 < len(S0) <= 65)


def gb(g, fac=1.31):
    r = fac * g["rh"]
    return g_disc(g["M"], r, g["rh"]), r


sel = [g for g in S0 if gb(g)[0] < A0]
P(f"    S0 = {len(S0)}; S1 (g_bar < a0 at r_v = 2.2 R_d) = {len(sel)}; g_bar/a0 of S0: min {min(gb(g)[0] / A0 for g in S0):.2f}, median {np.median([gb(g)[0] / A0 for g in S0]):.2f}, max {max(gb(g)[0] / A0 for g in S0):.2f}")
h0 = len(sel) >= 5
check("H0 [FEASIBILITY GATE] the selected sample (g_bar < a0) has N >= 5", f"N = {len(sel)} of {len(S0)}", h0)
# reported, POST-HOC (added after the main run, disclosed): how far out would the velocity radius have to be for anything to qualify?
sens = {fac: sorted(gb(g, fac)[0] / A0 for g in S0)[:3] for fac in (1.31, 2.0, 3.0, 4.0)}
nsel = {fac: sum(gb(g, fac)[0] < A0 for g in S0) for fac in (1.31, 2.0, 3.0, 4.0)}
check("R0 (reported, POST-HOC: added after the main run) the number of S0 galaxies with g_bar < a0 if the velocity were measured at r = 1.31, 2, 3, 4 r_h, and the three lowest g_bar/a0",
      "; ".join(f"{k} r_h: N = {nsel[k]}, lowest {', '.join(f'{x:.2f}' for x in v)}" for k, v in sens.items()), True, load_bearing=False)


def offsets(sample, fac=1.31, dm=0.0):
    out = []
    for g in sample:
        r = fac * g["rh"]; gbar = g_disc(g["M"] * 10 ** dm, r, g["rh"]); gobs = (g["v"] * 1e3) ** 2 / (r * KPC)
        out.append((math.log10(gobs / (gbar * nu(gbar / A0))), math.log10(gobs / (gbar * nu(gbar / (A0 * E(g["z"]))))), gbar / A0))
    return np.array(out)


if h0:
    o = offsets(sel); mf, mr = o[:, 0].mean(), o[:, 1].mean()
    err_v = SIGV / math.sqrt(len(sel))
    sl = [(offsets(sel, dm=+0.02)[:, k].mean() - offsets(sel, dm=-0.02)[:, k].mean()) / 0.04 for k in (0, 1)]       # d Delta / d log M (negative of the slope of g_pred)
    err_m = SIGM * max(abs(sl[0]), abs(sl[1]))
    fl = [offsets(sel, fac=x) for x in (1.0, 1.31, 2.0)]
    rad = [0.5 * (max(a[:, k].mean() for a in fl) - min(a[:, k].mean() for a in fl)) for k in (0, 1)]
    tot = [math.sqrt(err_v ** 2 + err_m ** 2 + rad[k] ** 2) for k in (0, 1)]
    dsep = abs(mf - mr); tsep = math.sqrt(err_v ** 2 + err_m ** 2 + rad[0] ** 2)
    P(f"    N = {len(sel)}; mean Delta_flat {mf:+.3f} (sigma_tot {tot[0]:.3f}: velocity {err_v:.3f}, mass {err_m:.3f}, radius {rad[0]:.3f}); mean Delta_rival {mr:+.3f} (sigma_tot {tot[1]:.3f}); separation {dsep:.3f}")
    for g, row in zip(sel, o):
        P(f"      {g['name']:12s} {g['type']:9s} z {g['z']:.2f} g_bar/a0 {row[2]:.2f} Delta_flat {row[0]:+.2f} Delta_rival {row[1]:+.2f}")
    h1 = abs(mf) < 2 * tot[0]; h2 = abs(mr) < 2 * tot[1]; h3 = dsep > 2 * tsep
    check("H1 flat a0 fits: |mean Delta_flat| < 2 sigma_tot" + ("  [MUTATE: v x 0.5]" if MUTATE else ""), f"{mf:+.3f} +- {tot[0]:.3f} ({mf / tot[0]:+.2f} sigma)", h1)
    check("H2 the rival fits: |mean Delta_rival| < 2 sigma_tot" + ("  [MUTATE: v x 0.5]" if MUTATE else ""), f"{mr:+.3f} +- {tot[1]:.3f} ({mr / tot[1]:+.2f} sigma)", h2)
    check("H3 [HEADLINE] THE SAMPLE CAN DISCRIMINATE: |mean Delta_flat - mean Delta_rival| > 2 sigma_tot", f"separation {dsep:.3f} against 2 sigma_tot {2 * tsep:.3f} ({dsep / tsep:.2f} sigma)", h3)
    # reported: selection-bias mock (truth = flat law, mass noise 0.20 dex, reselect on the noisy g_bar)
    rng = np.random.default_rng(54); bias = []
    for _ in range(400):
        s_ = []
        for g in S0:
            eps = rng.normal(0, SIGM); g_true = g_disc(g["M"] * 10 ** eps, 1.31 * g["rh"], g["rh"])         # true mass = observed * 10^eps
            if g_disc(g["M"], 1.31 * g["rh"], g["rh"]) < A0:
                gobs = g_true * nu(g_true / A0)
                s_.append(math.log10(gobs / (g_disc(g["M"], 1.31 * g["rh"], g["rh"]) * nu(g_disc(g["M"], 1.31 * g["rh"], g["rh"]) / A0))))
        if s_:
            bias.append(np.mean(s_))
    disc_only = [g for g in sel if g["type"].startswith("Disk")]
    lo = [g for g in sel if g["z"] < 1.6]; hi = [g for g in sel if g["z"] >= 1.6]
    frag = lambda s_: (f"N={len(s_)}: flat {offsets(s_)[:, 0].mean():+.3f}, rival {offsets(s_)[:, 1].mean():+.3f}" if len(s_) else "N=0")
    check("R1 (reported) the selection-bias mock (truth = flat, mass noise 0.20 dex, reselect on the noisy g_bar); R2 discs only; R3 the z ~ 1.2 and z ~ 2.2 halves",
          f"expected bias in mean Delta_flat {np.mean(bias):+.3f} +- {np.std(bias):.3f}; discs only {frag(disc_only)}; z<1.6 {frag(lo)}; z>=1.6 {frag(hi)}", True, load_bearing=False)
    reading = ("the sample discriminates the two laws" if h3 else "the sample is too small or too uncertain to discriminate the two laws (CFG52's forecast: the calibration systematic caps the significance)")
    R.num("stats", dict(N=len(sel), mf=mf, mr=mr, tot=tot, sep=dsep, tsep=tsep, bias=float(np.mean(bias))))
else:
    reading = "NON-DIAGNOSTIC: the frozen selection leaves fewer than five discs"
P(f"\n    READING (declared): {reading}")
R.num("reading", reading); R.num("n", dict(S0=len(S0), sel=len(sel)))
nf = R.write()
sys.exit(1 if nf else 0)
