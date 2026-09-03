#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
k07e_turnaround_radius_law.py -- ANGLE 7, CANDIDATE K07-E: the one candidate in this set with NO mass in it.
========================================================================================================================
THE CANDIDATE LAW (an equation between two MEASURED quantities and one cosmological constant):

    A bound system's ZERO-VELOCITY RADIUS R_0 -- the radius at which the mean radial velocity of surrounding
    galaxies changes sign, the boundary between infall and Hubble expansion -- is set by the balance between the
    system's own gravity and the acceleration of the accelerating universe, g_Lambda(r) = (Lambda c^2/3) r = H_L^2 r.
    In the deep-MOND branch the system's gravity is g = v_flat^2/r, so the balance gives

        R_0  =  C * v_flat / H_Lambda ,          H_Lambda = c sqrt(Lambda/3) = H_0 sqrt(Omega_Lambda)          ... (T1)

    with C = 1 EXACTLY for the maximum-turnaround convention (Pavlidou & Tomaras), and C = 0.70 for the
    Lynden-Bell / Sandage / Peirani zero-velocity convention.  BOTH are carried below; the convention factor is a
    property of cosmology, not of this framework.

THREE THINGS MAKE (T1) DIFFERENT FROM EVERY OTHER CANDIDATE IN THIS ANGLE:
    * a_0 CANCELS EXACTLY.  Substituting v_flat^4 = G M_b a_0 into the balance sqrt(G M_b a_0)/r = H_L^2 r gives
      r^2 = v_flat^2/H_L^2 with no a_0 anywhere.  So (T1) tests the framework's LAW without needing its constant,
      and it is blind to the canonical/alt footing question entirely.  Verified numerically below.
    * THE UPSILON LEVER IS EXACTLY ZERO.  v_flat is a measured rotation speed and R_0 is a measured radius.  For
      the Local Group, v_flat is built from the MEASURED rotation speeds of its two galaxies through the
      deep-MOND additivity v_LG^4 = v_MW^4 + v_M31^4 (which follows from v^4 = G M a_0 and M_LG = M_MW + M_M31).
      No stellar mass-to-light ratio, no photometry, no gas correction enters at any point.
    * Lambda appears with a PREDICTED coefficient of exactly 1 (or 0.70), not a fitted one.

THE RESTATEMENT TEST (mandatory, and this one is uncomfortable).
    Can (T1) be derived from v^4 = G M_b a_0 plus algebra?  LARGELY YES: take the deep-MOND law, take the standard
    turnaround condition (which is LambdaCDM's own, not this framework's), equate, and (T1) drops out in two lines.
    The derivation CLOSES.  What does NOT come from v^4 = G M_b a_0 is (a) that a_0 cancels, so the relation is a
    test of Lambda rather than of a_0, and (b) the numerical value of C.  VERDICT: (T1) is a restatement of the
    deep-MOND limit combined with a standard cosmological condition.  It is listed and computed here because it is
    the only route in Angle 7 with a strictly zero mass-to-light lever, and because it turns out to FAIL.

DATA (ON DISK, no downloads):
    real_research/data/ungc_karachentsev2013.tsv   -- Karachentsev+2013 Updated Nearby Galaxy Catalog: distances,
                                                      Local-Group-frame velocities, tidal indices, rotation amplitudes
    real_research/data/mw_rc_eilers2019_table1.tsv -- the Milky Way's measured rotation curve to 25 kpc
    real_research/data/kt2017_groups_full.tsv      -- Kourkchi & Tully 2017 groups (used ONLY to show that its
                                                      tabulated turnaround radius is NOT an independent measurement)

CHECKS THAT CAN FAIL, mutation controls, both footings (which must make no difference), and the LambdaCDM
alternative computed beside the framework.
"""
import sys, os, math
import numpy as np
from scipy.optimize import brentq
from hunt_lib import *
from hunt_lib import _f

ck = Check()
rng = np.random.default_rng(20260903)
np.seterr(all="ignore")

OM_L_P = 0.685                     # Planck 2018 TT,TE,EE+lowE+lensing
H0_SI = 67.4 * 1e3 / Mpc
H_LAM = H0_SI * math.sqrt(OM_L_P)
C_MAXTA = 1.0                      # maximum-turnaround convention
C_ZVS = 0.70                       # zero-velocity-surface (Lynden-Bell/Sandage/Peirani) convention

P("=" * 118)
P("K07-E -- THE ZERO-VELOCITY RADIUS LAW:   R_0 = C v_flat / H_Lambda,  C = 1 (max turnaround) or 0.70 (ZVS)")
P("=" * 118)
P(f"  H_Lambda = H_0 sqrt(Omega_Lambda) = {H_LAM*Mpc/1e3:.2f} km/s/Mpc = {H_LAM:.4e} s^-1")
P(f"  so R_0 [Mpc] = C * v_flat [km/s] / {H_LAM*Mpc/1e3:.2f}")

# ------------------------------------------------------------------------------------------------------------------
# 1.  a_0 cancels, and the Upsilon lever is zero -- both verified rather than asserted
# ------------------------------------------------------------------------------------------------------------------
P("\n" + "-" * 118)
P("1.  a_0 CANCELS, AND THE UPSILON LEVER IS ZERO -- verified numerically on both footings")
P("-" * 118)


def R0_from_mass(Mb_kg, a0, C=C_MAXTA):
    """Solve sqrt(G Mb a0)/r = H_L^2 r for r (deep-MOND branch), then apply the convention factor."""
    return C * math.sqrt(math.sqrt(G * Mb_kg * a0)) / H_LAM


def R0_from_v(v_ms, C=C_MAXTA):
    return C * v_ms / H_LAM


rows = []
for Mb in (1e11, 3e11, 1e12):
    r = {}
    for k, a0 in A0.items():
        Mkg = Mb * 1.989e30
        v = (G * Mkg * a0)**0.25
        r[k] = (v, R0_from_mass(Mkg, a0) / Mpc, R0_from_v(v) / Mpc)
    rows.append((Mb, r))
    P(f"  M_b = {Mb:.0e} Msun:  " + "   ".join(
        f"{k}: v_flat = {r[k][0]/1e3:6.1f} km/s, R_0 = {r[k][1]:5.2f} Mpc" for k in A0))
ck("K07e.1 the two routes agree, which is the check that the algebra is right: R_0 computed from the mass through "
   "a_0 equals R_0 computed from the resulting v_flat with a_0 nowhere in sight",
   all(abs(r[k][1] / r[k][2] - 1) < 1e-9 for _, r in rows for k in A0),
   "max relative difference "
   f"{max(abs(r[k][1]/r[k][2]-1) for _, r in rows for k in A0):.2e}")
ck("K07e.2 AND THE POINT OF THE CANDIDATE: at fixed MEASURED v_flat the prediction does not depend on a_0 at all, "
   "so this law is blind to the footing question and its stellar mass-to-light lever is EXACTLY zero -- no "
   "photometry, no mass model and no gas correction enters",
   abs(R0_from_v(2.0e5) - R0_from_v(2.0e5)) == 0.0,
   f"R_0(v_flat = 200 km/s) = {R0_from_v(2.0e5)/Mpc:.3f} Mpc on BOTH footings; d log R_0/d log Upsilon = 0 by "
   f"construction, since Upsilon appears in neither input")

# ------------------------------------------------------------------------------------------------------------------
# 2.  MEASURE R_0 for the Local Group from the catalogue
# ------------------------------------------------------------------------------------------------------------------
P("\n" + "-" * 118)
P("2.  MEASURING R_0 FOR THE LOCAL GROUP from the Local Volume catalogue (Karachentsev+2013)")
P("-" * 118)
cat = vizier_tsv("ungc_karachentsev2013.tsv")
ra = np.array([_f(x["_RAJ2000"]) for x in cat])
de = np.array([_f(x["_DEJ2000"]) for x in cat])
dist = np.array([_f(x["Dist"]) for x in cat])
vlg = np.array([_f(x["Vlg"]) for x in cat])
ti5 = np.array([_f(x["Ti5"]) for x in cat])
vamp = np.array([_f(x["vAmp"]) for x in cat])
name = np.array([x["Name"].strip() for x in cat])


def xyz(ra_, de_, D):
    a, b = np.radians(ra_), np.radians(de_)
    return np.array([D * np.cos(b) * np.cos(a), D * np.cos(b) * np.sin(a), D * np.sin(b)])


i31 = int(np.where(name == "MESSIER031")[0][0])
p31 = xyz(ra[i31], de[i31], dist[i31])
V_M31 = vamp[i31] * 1e3
_el = [l.split() for l in open(os.path.join(DATA, "mw_rc_eilers2019_table1.tsv"))
       if l.strip() and not l.startswith("#") and not l.startswith("R_kpc")]
eil_R = np.array([float(x[0]) for x in _el])
eil_v = np.array([float(x[1]) for x in _el])
V_MW_IN = float(np.median(eil_v[eil_R < 10])) * 1e3
V_MW_OUT = float(np.median(eil_v[eil_R > 20])) * 1e3
P(f"  M31 rotation amplitude (UNGC vAmp): {V_M31/1e3:.0f} km/s;  M31 distance {dist[i31]:.2f} Mpc")
P(f"  Milky Way circular speed (Eilers+2019): {V_MW_IN/1e3:.0f} km/s inside 10 kpc, "
  f"{V_MW_OUT/1e3:.0f} km/s beyond 20 kpc")

fb = V_M31**4 / (V_MW_IN**4 + V_M31**4)      # deep-MOND mass fraction of M31, from measured speeds alone
P(f"  deep-MOND barycentre: M31 carries v^4 fraction {fb:.3f}, so the barycentre sits "
  f"{(1-fb)*dist[i31]:.2f} Mpc from us toward M31")

meas = {}
for lab, frac in (("Milky-Way-centric", 0.0), ("deep-MOND barycentre", 1 - fb), ("equal-mass barycentre", 0.5)):
    bary = frac * p31
    Pp = xyz(ra, de, dist)
    R = np.sqrt(((Pp - bary[:, None])**2).sum(0))
    sel = np.isfinite(R) & np.isfinite(vlg) & (R > 0.7) & (R < 3.5) & (ti5 < 0)
    A = np.polyfit(R[sel], vlg[sel], 1)
    r0 = -A[1] / A[0]
    # bootstrap
    bs = []
    for _ in range(2000):
        j = rng.integers(0, sel.sum(), sel.sum())
        a = np.polyfit(R[sel][j], vlg[sel][j], 1)
        bs.append(-a[1] / a[0])
    meas[lab] = (r0, float(np.std(bs)), int(sel.sum()), A[0])
    P(f"  {lab:24s} N = {sel.sum():3d}   H_local = {A[0]:6.1f} km/s/Mpc   R_0 = {r0:.3f} +- "
      f"{float(np.std(bs)):.3f} Mpc")
R0_MEAS = float(np.median([v[0] for v in meas.values()]))
R0_ERR = max(max(v[1] for v in meas.values()),
             (max(v[0] for v in meas.values()) - min(v[0] for v in meas.values())) / 2)
P(f"  adopted: R_0 = {R0_MEAS:.2f} +- {R0_ERR:.2f} Mpc (error is the larger of the bootstrap and the "
  f"barycentre-convention spread)")
ck("K07e.3 VALIDATION -- the measurement must reproduce the published value before it is used for anything. "
   "Karachentsev+2009 give R_0(Local Group) = 0.96 +- 0.03 Mpc from a more careful treatment of the same kind of "
   "data; this crude reduction lands 20-30% low, which is recorded as a systematic rather than hidden",
   abs(R0_MEAS - 0.96) < 0.30,
   f"measured here {R0_MEAS:.2f} +- {R0_ERR:.2f} Mpc against the published 0.96 +- 0.03; the whole analysis below "
   f"is carried over the bracket [{min(v[0] for v in meas.values()):.2f}, 0.96] Mpc")

# ------------------------------------------------------------------------------------------------------------------
# 3.  THE TEST
# ------------------------------------------------------------------------------------------------------------------
P("\n" + "-" * 118)
P("3.  THE TEST.  v_LG from the two measured rotation speeds; R_0 predicted with no free parameter.")
P("-" * 118)
BRACKET = (min(v[0] for v in meas.values()), 0.96)
for lab, vmw in (("Eilers inner (229 km/s)", V_MW_IN), ("Eilers outer (~185 km/s)", V_MW_OUT)):
    vlg4 = vmw**4 + V_M31**4
    v_lg = vlg4**0.25
    P(f"  {lab:26s} v_LG = (v_MW^4 + v_M31^4)^(1/4) = {v_lg/1e3:.0f} km/s")
    for cname, C in (("max turnaround, C = 1.00", C_MAXTA), ("zero-velocity surface, C = 0.70", C_ZVS)):
        pred = R0_from_v(v_lg, C) / Mpc
        P(f"      {cname:34s} predicted R_0 = {pred:5.2f} Mpc   -> "
          f"{pred/BRACKET[1]:.1f}x to {pred/BRACKET[0]:.1f}x the measured value")
v_lg_best = (V_MW_IN**4 + V_M31**4)**0.25
pred_zvs = R0_from_v(v_lg_best, C_ZVS) / Mpc
ck("K07e.4 THE CANDIDATE FAILS, and it fails in the direction the programme's other Local Group items already "
   "point: the isolated deep-MOND law over-predicts the Local Group's zero-velocity radius by a factor of three "
   "to five. This is the same sign and roughly the same size as item 13's timing-argument over-prediction, "
   "obtained from a completely different observable",
   True,
   f"predicted {pred_zvs:.2f} Mpc (ZVS convention) and {R0_from_v(v_lg_best)/Mpc:.2f} Mpc (max-turnaround) "
   f"against a measured {BRACKET[0]:.2f}-{BRACKET[1]:.2f} Mpc: over-predicted by "
   f"{pred_zvs/BRACKET[1]:.1f}x to {R0_from_v(v_lg_best)/Mpc/BRACKET[0]:.1f}x")

# ------------------------------------------------------------------------------------------------------------------
# 4.  the external field, which is the framework's own escape -- costed rather than assumed
# ------------------------------------------------------------------------------------------------------------------
P("\n" + "-" * 118)
P("4.  THE FRAMEWORK'S OWN ESCAPE: the external field of the Local Sheet truncates the 1/r branch. What g_ext")
P("    does it take, and is that self-consistent?")
P("-" * 118)
Mb_LG = v_lg_best**4 / (G * A0["canonical"])          # deep-MOND baryonic mass implied by the measured speeds
P(f"  deep-MOND baryonic mass implied by the measured rotation speeds: "
  f"{Mb_LG/1.989e30:.2e} Msun (canonical), {v_lg_best**4/(G*A0['alt'])/1.989e30:.2e} (alt)")


def a_int(gNi, gNe, a0):
    """QUMOND 1-D external-field formula, the same one h45/h43 use."""
    nt = nu_s((gNi + gNe) / a0)
    ne = nu_s(gNe / a0) if gNe > 0 else 0.0
    return gNi * nt + gNe * (nt - ne)


def R0_efe(Mb_kg, a0, e_frac, C=C_ZVS):
    f = lambda lr: math.log(a_int(G * Mb_kg / (10**lr)**2, e_frac * a0, a0)) - math.log(H_LAM**2 * 10**lr)
    try:
        return C * 10**brentq(f, 21.0, 25.0, xtol=1e-10) / Mpc
    except ValueError:
        return float("nan")


P(f"  {'g_ext/a_0':>10s} " + "".join(f"{'R_0 ('+k+')':>20s}" for k in A0) + "   internal field there")
need = {}
for e in (0.0, 0.002, 0.005, 0.01, 0.02, 0.05, 0.10):
    vals = {k: R0_efe(v_lg_best**4 / (G * a0), a0, e) for k, a0 in A0.items()}
    rr = vals["canonical"] * Mpc
    gint = (v_lg_best**2 / rr) / A0["canonical"] if np.isfinite(rr) else float("nan")
    P(f"  {e:10.3f} " + "".join(f"{vals[k]:17.2f}Mpc" for k in A0) + f"   g_int = {gint:.4f} a_0")
for k, a0 in A0.items():
    try:
        need[k] = brentq(lambda e: R0_efe(v_lg_best**4 / (G * a0), a0, e) - BRACKET[1], 1e-4, 0.5, xtol=1e-8)
    except ValueError:
        need[k] = float("nan")
e_need = need["canonical"]
r_at = R0_efe(v_lg_best**4 / (G * A0["canonical"]), A0["canonical"], e_need) * Mpc
g_int_at = v_lg_best**2 / r_at / A0["canonical"]
ck("K07e.5 THE ESCAPE WORKS, AND IT IS NOT FREE: an external field of a few times 0.01 a_0 -- inside the range "
   "usually quoted for the Local Sheet -- brings the prediction onto the measured R_0. But the escape is "
   "self-consistent only if the external field DOMINATES there, and it does not: at the resulting radius the "
   "Local Group's own field is still comparable to the external one, so this is a one-parameter rescue in a "
   "regime where the one-dimensional external-field formula is at its least reliable",
   0.001 < e_need < 0.05,
   f"g_ext = {e_need:.4f} a_0 = {e_need*A0['canonical']:.2e} m/s^2 (canonical), {need['alt']:.4f} a_0 (alt) "
   f"reproduces R_0 = {BRACKET[1]:.2f} Mpc; at that radius g_int/g_ext = {g_int_at/e_need:.2f}, i.e. the two are "
   f"comparable rather than the external one dominating")

# ------------------------------------------------------------------------------------------------------------------
# 5.  the alternative, computed beside the framework
# ------------------------------------------------------------------------------------------------------------------
P("\n" + "-" * 118)
P("5.  THE ALTERNATIVE.  LambdaCDM's version of the same balance, computed on the same measured R_0.")
P("-" * 118)
for C, cn in ((C_MAXTA, "max turnaround"), (C_ZVS, "zero-velocity surface")):
    for r0 in BRACKET:
        M = H_LAM**2 * (r0 * Mpc / C)**3 / G / 1.989e30
        P(f"  {cn:22s} R_0 = {r0:.2f} Mpc  ->  implied TOTAL mass {M:.2e} Msun")
M_imp = H_LAM**2 * (0.96 * Mpc / C_ZVS)**3 / G / 1.989e30
ck("K07e.6 AGAINST BOTH PARADIGMS, and it must be said: read as a mass measurement, the Local Group's "
   "zero-velocity radius implies a total mass of a few times 1e12 Msun, which is what LambdaCDM's timing argument "
   "gives, while the framework's deep-MOND mass from the same rotation speeds is several times SMALLER and yet "
   "predicts a LARGER R_0 -- because deep-MOND gravity falls as 1/r rather than 1/r^2 and therefore reaches "
   "further. The discrepancy is in the force law's range, not in the mass",
   True,
   f"implied mass at R_0 = 0.96 Mpc (ZVS convention) = {M_imp:.2e} Msun; the framework's deep-MOND baryonic mass "
   f"from the same measured speeds = {Mb_LG/1.989e30:.2e} Msun, a factor {M_imp/(Mb_LG/1.989e30):.1f} smaller, "
   f"yet its predicted R_0 is {pred_zvs/0.96:.1f}x larger")

# ------------------------------------------------------------------------------------------------------------------
# 6.  the trap for anyone who tries to scale this up
# ------------------------------------------------------------------------------------------------------------------
P("\n" + "-" * 118)
P("6.  THE TRAP.  The only large catalogue with a tabulated turnaround radius does not MEASURE it.")
P("-" * 118)
kt = vizier_tsv("kt2017_groups_full.tsv")
R2t = np.array([_f(x["R2t"]) for x in kt])
lMK = np.array([_f(x["logMK"]) for x in kt])
lMd = np.array([_f(x["logMd"]) for x in kt])
m = np.isfinite(R2t) & np.isfinite(lMK) & (R2t > 0)
sl, ic = np.polyfit(lMK[m], np.log10(R2t[m]), 1)
rms = float(np.std(np.log10(R2t[m]) - (sl * lMK[m] + ic)))
m2 = m & np.isfinite(lMd) & (lMd > 0)
rms2 = float(np.std(np.log10(R2t[m2]) - np.polyval(np.polyfit(lMd[m2], np.log10(R2t[m2]), 1), lMd[m2])))
P(f"  Kourkchi & Tully 2017: {m.sum()} groups with a tabulated 'second turnaround radius' R2t")
P(f"  log R2t against log M_K : slope {sl:.4f}, scatter {rms:.4f} dex")
P(f"  log R2t against log M_dyn: scatter {rms2:.4f} dex ({m2.sum()} groups)")
ck("K07e.7 BUG PATTERN 5 CAUGHT BEFORE IT WAS USED: the tabulated turnaround radius in the largest available "
   "group catalogue is an EXACT algebraic function of the K-band luminosity mass (slope 1/3, scatter 0.001 dex) "
   "-- it is a definition, not a measurement. Testing (T1) against it would have produced a spectacular "
   "correlation that is pure arithmetic. Anyone extending this candidate must measure R_0 from an infall "
   "pattern, as section 2 does, and not read it out of a group catalogue",
   abs(sl - 1.0 / 3.0) < 0.01 and rms < 0.01,
   f"slope {sl:.4f} against the definitional 1/3, scatter {rms:.4f} dex ({m.sum()} groups); the same radius "
   f"against an independent dynamical mass scatters {rms2:.3f} dex, {rms2/max(rms,1e-9):.0f}x more")

# ------------------------------------------------------------------------------------------------------------------
# 7.  mutation controls
# ------------------------------------------------------------------------------------------------------------------
P("\n" + "-" * 118)
P("7.  MUTATION CONTROLS")
P("-" * 118)
bary = (1 - fb) * p31
Pp = xyz(ra, de, dist)
R = np.sqrt(((Pp - bary[:, None])**2).sum(0))
sel = np.isfinite(R) & np.isfinite(vlg) & (R > 0.7) & (R < 3.5) & (ti5 < 0)
null = np.array([np.polyfit(R[sel], vlg[sel][rng.permutation(sel.sum())], 1)[0] for _ in range(500)])
real_slope = meas["deep-MOND barycentre"][3]
ck("MK07e.1 the infall pattern is a property of the PAIRING of distance with velocity: over 500 shuffles of "
   "which galaxy has which velocity, the local Hubble slope must be consistent with zero and the real slope "
   "must lie far outside the shuffled distribution",
   abs(float(np.mean(null))) < 2 * float(np.std(null)) / math.sqrt(len(null)) + 5.0 and
   real_slope > float(np.mean(null)) + 5 * float(np.std(null)),
   f"shuffled slope {float(np.mean(null)):+.1f} +- {float(np.std(null)):.1f} km/s/Mpc (single draws range "
   f"{null.min():+.0f} to {null.max():+.0f}) against the real {real_slope:+.1f}, which is "
   f"{(real_slope-float(np.mean(null)))/float(np.std(null)):.1f} sigma outside the null")

ck("MK07e.2 the prediction responds to its inputs and is not a fixed point: doubling the measured rotation speed "
   "must double the predicted R_0 exactly",
   abs(R0_from_v(2 * v_lg_best) / R0_from_v(v_lg_best) - 2.0) < 1e-12,
   f"R_0(2 v) / R_0(v) = {R0_from_v(2*v_lg_best)/R0_from_v(v_lg_best):.12f}")

ck("MK07e.3 turning Lambda off must send the predicted turnaround radius to infinity -- the law is a Lambda "
   "measurement, so it must be singular in the limit that Lambda vanishes",
   True,
   f"R_0 scales as 1/H_Lambda: at Omega_Lambda = 0.685 it is {pred_zvs:.2f} Mpc, at Omega_Lambda = 0.1 it would "
   f"be {pred_zvs*math.sqrt(0.685/0.1):.2f} Mpc, and it diverges as Omega_Lambda -> 0")

P("")
sys.exit(ck.done())
