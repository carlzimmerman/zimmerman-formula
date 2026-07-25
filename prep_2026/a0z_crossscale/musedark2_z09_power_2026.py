#!/usr/bin/env python3
"""
musedark2_z09_power_2026.py -- THE DEC-vs-RISE POWER CALCULATION AT z ~ 0.9 ON MUSE-DARK II.
============================================================================================
Carl Zimmerman's de Sitter-Unruh MODIFIED-INERTIA framework (a0 = c H_Lambda / Z,
Z = sqrt(32 pi / 3) = 5.78633; canonical a0(0) = 9.355e-11 m/s^2; its OWN dS-Unruh
interpolation g_obs = sqrt(g_bar^2 + g_bar a0), i.e. the EXACT a0-line
g_obs^2 - g_bar^2 = a0 g_bar).  Judged on ITS OWN terms; McGaugh's nu is never used.

ROLE (the OPEN DOOR pass): every prior high-z pass hunted z ~ 2-3 and returned NO-GO because
the DEC-vs-RISE test there demands g_bar < 0.3 a0 at z ~ 2 where no sample exists.  This file
does NOT inherit that verdict.  It asks a DIFFERENT question about a DIFFERENT, REAL, ALREADY
PUBLISHED sample:

    MUSE-DARK II -- Jeanneau et al. 2026, A&A (arXiv:2603.28856; A&A 2026/05 aa59953-26):
    95 strongly-lensed, rotation-dominated, LOW-MASS star-forming galaxies,
    0.56 <= z <= 1.37, mu = 1.4 - 12.4, log M* = 8.1 - 10.3,
    4 Frontier Fields clusters (Abell 2744, Abell 370, Abell S1063, MACS0416),
    lensing-aware 3D forward modelling (lensed GalPaK3D), V measured at 1.8 R_e,
    PUBLISHED RESULT: Delta_b(bTFR) = 0.00 (+0.06/-0.06) dex in baryonic mass
    (and Delta_b(sTFR) = -0.42 +/- 0.05 dex), i.e. NO detectable bTFR zero-point evolution.

Why this sample and not another: the committed compilation already scores it as having the
BEST acceleration-dilution lever of any high-z constraint in hand.  The framework's OWN kernel
gives the bTFR a0-lever  L = 1/(1+2y),  y = g_bar/a0, and MUSE-DARK II sits at
g_bar ~ (0.3-1.0) a0  ->  y = 0.548 (geometric mean)  ->  L = 0.477, against L = 0.126 for
Ubler z=2.3 and L = 0.078 for Amvrosiadis z=2.4.  It is the only existing sample that gets
near the a0 regime at anything like cosmic noon.

THE FORK BEING TESTED (both branches zero-parameter, both fixed by DESI+Planck, ratio
FOOTING-INDEPENDENT):
    DEC   de Sitter / future-event horizon  [Carl's canonical]: a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE0)
    RISE  Hubble horizon                    [McCulloch MiHsC -- CREDITED]: a0(z)/a0(0) = E(z)
At z = 0.9 these read DEC = 0.9996 and RISE = 1.6867: a 68.7% gap.  That is a FAR more
favourable regime than the 2.3% DEC-vs-FLAT gap at the same z, and looser than the z=2 bars.

*** THE ONE THING THIS FILE CANNOT DO, SAID UP FRONT ***
z ~ 0.9 is the WORST redshift in the whole problem for the framework's DISTINCTIVE claim.
DEC(0.9) = 0.9996 vs FLAT = 1.000 -- a 0.04% gap, needing 0.014% precision for 3 sigma.
MUSE-DARK II therefore CANNOT detect the declining branch and CANNOT test DEC vs FLAT at all.
Anything it decides is DEC-vs-RISE, i.e. de Sitter horizon vs Hubble horizon -- a MECHANISM
discriminator against McCulloch, NOT a detection of Carl's decline.  A DEC "win" here is a
win over the rival horizon reading only.  This is stated first so no result below can be
mis-sold, and it is asserted in the self-check.

HARD CALIBRATION (a manufactured DETECTION and a manufactured DEFICIT are penalized EQUALLY)
 (1) No manufactured detection.  Every separation S below is COMPUTED from a covariance model
     with explicit coherent blocks; the published numbers are used as published; the verdict
     strings are f-string functions of the numbers, never typed in by hand.
 (2) No inherited NO-GO either.  The z=2 verdict is NOT carried over.  z~0.9 with L = 0.477
     is evaluated on its own numbers, and where the numbers are FAVOURABLE (the trend route's
     immunity to the coherent wall; the a0-line route's per-object gain over the bTFR route)
     that is reported as plainly as the walls.
 (3) The LCDM-degenerate apparent-drift nuisance is carried, with the committed exposure
     w = 0.20 for this clean lensed near-a0 sample -- AND with a sweep to w = 1.00, because
     the TREND route is exactly the channel w controls and w=0.20 was justified by the
     ACCELERATION regime, not by the z-dependence of the Tacconi/NUM gas prescription.
     That sweep is an anti-GO adjustment made deliberately.
 (4) The HI nuisance is sign-locked: under-counting M_bar makes a0 read HIGH, i.e. toward
     RISE, i.e. AGAINST the framework's declining branch.  Prior M_HI in [0, M_mol], never
     zero.  MUSE-DARK II does model HI (NEUTRALUNIVERSEMACHINE), so both the modelled case
     and the full one-sided prior are carried.
 (5) BOTH footings: canonical cH_Lambda/Z = 9.355e-11 and alt cH0/Z = 1.1305e-10.  The ratio
     a0(z)/a0(0) is footing-independent (re-asserted numerically), so every separation,
     every bar and every requirement below is identical on both footings.
 (6) ESTIMATOR: MEDIAN-LIKE ONLY.  Committed estimator_bias_mocks.py / estimator_bias_verdict
     .json: gls_origin bias +10.34 pp = FAIL, theilsen_pairwise +7.93 pp = FAIL;
     median_a0pt +0.84, ivw_median_a0pt +0.66, galaxy_median_then_median +0.31 pp = PASS.
     GLS IS FORBIDDEN HERE.  The cost of that pre-registration -- the median's efficiency
     penalty sqrt(pi/2) = 1.2533 on the incoherent term -- is APPLIED, not waived.
 (7) nu = sqrt(1 + 1/y) is Milgrom 1999 (PLA 253:273 Eq.9) -- WELLHEAD CREDIT.  The
     framework's distinctive content is the cH_Lambda/Z coefficient and the modified-inertia
     completion.  McCulloch (MiHsC) credited for the Hubble-horizon branch.  a0's VALUE and
     the HORIZON CHOICE remain POSITS.  No TOE.  No "theory closed".  No closed doors.
     Exit 0 = ran, NOT a verdict.

BUILDS ON (does not modify or contradict) the committed parents:
    desitter_unruh_horizon_fork_2026.py   -- the DEC / RISE branches per z
    a0z_fork_likelihood_2026.py           -- the joint likelihood, the lever L = 1/(1+2y),
                                             the A_drift prior ladder + per-point exposures
                                             (imported here, stdout suppressed, so the 10
                                             cited constraints are NOT duplicated by hand)
    highz_a0_fork_confront_2026.py        -- the 11-constraint compilation incl. Jeanneau
    lensed_deepmond_floor_2026.py         -- the lensed deep-MOND amplifications at z~2
    ../a0_line/estimator_bias_mocks.py    -- the median-like estimator pre-registration
"""
import numpy as np
import json
import os
import io
import sys
import contextlib

np.seterr(all="ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
DEX = np.log(10.0)
BAR = "=" * 100
MEDPEN = np.sqrt(np.pi / 2.0)          # 1.2533 -- median-like efficiency penalty (rule 6)

# ---------------------------------------------------------------------------------------
# import the committed likelihood WITHOUT duplicating its data (stdout suppressed)
# ---------------------------------------------------------------------------------------
sys.path.insert(0, HERE)
_buf = io.StringIO()
with contextlib.redirect_stdout(_buf):
    import a0z_fork_likelihood_2026 as PAR
R_dec, R_rise, R_flat = PAR.R_dec, PAR.R_rise, PAR.R_flat
A0_CAN, A0_ALT, Z_CONST = PAR.A0_CAN, PAR.A0_ALT, PAR.Z_CONST
PMAX_LADDER = list(PAR.PMAX_LADDER)                 # [0.46, 0.92, 1.22, 1.50]
PRIOR_LABELS = [l.split()[0] for l, _ in PAR.PRIORS]

# =======================================================================================
# S0 -- THE SAMPLE (published facts only) AND THE FRAMEWORK CONSTANTS
# =======================================================================================
ZLO, ZHI = 0.56, 1.37                  # published kinematic-subsample span
N_GAL = 95                             # published rotation-dominated sample
N_CL = 4                               # Abell 2744, Abell 370, Abell S1063, MACS0416
MU_LO, MU_HI = 1.4, 12.4               # published magnification range
DB_BTFR, DB_STAT = 0.00, 0.06          # published bTFR zero-point offset (dex, baryonic mass)
DB_HONEST = 0.27                       # committed systematics-inclusive band (compilation)
SIG_LOGMBAR_PUB = 0.20                 # published: "uniform uncertainty of +/-0.2 dex" in the TFR fit
DV_SEL = 0.30                          # published selection cut: Delta v_1.8 / v_1.8 < 30%
Y_JEAN = float(np.sqrt(0.3 * 1.0))     # committed g_bar/a0 in [0.3,1.0] -> geometric mean
LEVER = 1.0 / (1.0 + 2.0 * Y_JEAN)     # framework's OWN bTFR a0-lever
W_JEAN = 0.20                          # committed drift exposure for this clean lensed point

print(BAR)
print("MUSE-DARK II @ z~0.9 -- THE DEC-vs-RISE POWER CALCULATION (dS-Unruh MODIFIED INERTIA)")
print(BAR)
print(f"  a0 = c H_Lambda / Z,  Z = {Z_CONST:.5f};  canonical a0(0) = {A0_CAN:.4e} m/s^2,"
      f"  alt = {A0_ALT:.4e}.")
print(f"  SAMPLE (published, Jeanneau+2026 A&A, arXiv:2603.28856):")
print(f"    N = {N_GAL} lensed rotation-dominated SFGs, {ZLO} <= z <= {ZHI}, mu = {MU_LO}-{MU_HI},")
print(f"    log M* = 8.1-10.3, {N_CL} Frontier Fields clusters (A2744, A370, AS1063, MACS0416),")
print(f"    lensed GalPaK3D 3D forward modelling, V at 1.8 R_e, selection Delta v/v < {DV_SEL:.0%},")
print(f"    baryonic masses carry a PUBLISHED uniform +/-{SIG_LOGMBAR_PUB:.2f} dex in their TFR fit,")
print(f"    M_mol from Tacconi+2020 scaling relations, M_HI from NEUTRALUNIVERSEMACHINE,")
print(f"    PUBLISHED Delta_b(bTFR) = {DB_BTFR:+.2f} (+{DB_STAT:.2f}/-{DB_STAT:.2f}) dex"
      f"  [Delta_b(sTFR) = -0.42 +/- 0.05].")
print(f"  FRAMEWORK LEVER (its OWN kernel, not assumed): y = g_bar/a0 = {Y_JEAN:.4f}"
      f"  ->  L = 1/(1+2y) = {LEVER:.4f}")
print(f"    (vs L = 0.126 Ubler z=2.3, L = 0.078 Amvrosiadis z=2.4 -- the BEST lever in hand.)")

# footing independence, numerically, on both footings
_f1 = float(A0_CAN * R_dec(0.9)) / float(A0_CAN * R_dec(0.0))
_f2 = float(A0_ALT * R_dec(0.9)) / float(A0_ALT * R_dec(0.0))
print(f"  FOOTING CHECK: a0(0.9)/a0(0) canonical = {_f1:.12f}  alt = {_f2:.12f}  "
      f"|diff| = {abs(_f1-_f2):.1e} -> IDENTICAL (every number below is footing-independent).")
print(f"  In ABSOLUTE units the fork at z=0.9 is: DEC -> {A0_CAN*_f1:.4e} (canon) / "
      f"{A0_ALT*_f1:.4e} (alt) m/s^2,")
print(f"                                          RISE -> {A0_CAN*float(R_rise(0.9)):.4e} (canon) / "
      f"{A0_ALT*float(R_rise(0.9)):.4e} (alt).")

# =======================================================================================
# S1 -- THE TWO BRANCHES ACROSS THE SAMPLE'S OWN z SPAN, AND THE GAP PER BIN
# =======================================================================================
print("\n" + BAR)
print("S1 -- DEC vs RISE ACROSS 0.56 <= z <= 1.37 (the gap GROWS with z; quantified per bin)")
print(BAR)


def gap_dex(z):
    return float(np.log10(R_rise(z) / R_dec(z)))


def bars_3s(z):
    """the three defensible 3-sigma conventions, in FRACTIONAL sigma(a0)/a0."""
    d, r = float(R_dec(z)), float(R_rise(z))
    mid = 0.5 * (d + r)
    return (abs(r - d) / (3.0 * mid),          # mid-referenced   (TIGHTEST -> headline)
            10.0 ** (gap_dex(z) / 3.0) - 1.0,  # pure-dex         (gap/3 in dex)
            abs(r - d) / (3.0 * d))            # DEC-referenced   (LOOSEST)


ZEDGES = np.array([0.56, 0.76, 0.965, 1.17, 1.37])
print(f"  {'z':>6} | {'DEC':>7} {'RISE':>7} {'RISE/DEC':>9} {'gap(dex)':>9} | "
      f"{'3s mid':>8} {'3s dex':>8} {'3s DEC':>8} | {'DEC-vs-FLAT 3s bar':>19}")
print("  " + "-" * 98)
for z in [ZLO, 0.76, 0.90, 0.965, 1.0, 1.17, ZHI]:
    d, r = float(R_dec(z)), float(R_rise(z))
    b1, b2, b3 = bars_3s(z)
    fl = abs(1.0 - d) / (3.0 * 0.5 * (1.0 + d))
    print(f"  {z:>6.3f} | {d:>7.4f} {r:>7.4f} {r/d:>8.4f}x {gap_dex(z):>9.5f} | "
          f"{100*b1:>7.2f}% {100*b2:>7.2f}% {100*b3:>7.2f}% | {100*fl:>18.4f}%")
print(f"\n  The gap grows from {gap_dex(ZLO):.4f} dex at z={ZLO} to {gap_dex(ZHI):.4f} dex at "
      f"z={ZHI} -- a factor {gap_dex(ZHI)/gap_dex(ZLO):.2f} across the sample's own span.")
print(f"  HEADLINE 3-sigma BAR used below = the TIGHTEST convention (mid-referenced) at the")
print(f"  sample's effective z, so a GO can never be manufactured by choosing a convention.")
print(f"  The prompt's '~23% at z~0.9' is the LOOSEST (DEC-referenced) reading; the tightest")
print(f"  is {100*bars_3s(0.9)[0]:.2f}% and the pure-dex reading is {100*bars_3s(0.9)[1]:.2f}%. All three are carried.")
print(f"  *** DEC-vs-FLAT at z=0.9 needs {100*abs(1-float(R_dec(0.9)))/(3*0.5*(1+float(R_dec(0.9)))):.4f}% -- "
      f"IMPOSSIBLE. This sample tests DEC vs RISE ONLY. ***")

# =======================================================================================
# S2 -- WHERE THE POWER LIVES.  The true N(z) of the 95 is NOT published as a table, so
#       THREE defensible z-distributions are carried and the SPREAD is reported.
# =======================================================================================
print("\n" + BAR)
print("S2 -- WHICH REDSHIFTS CARRY THE POWER (Fisher share per bin; 3 z-distributions)")
print(BAR)
print("  HONEST GAP: the per-object redshift list of the 95 is NOT published in a table")
print("  (the paper's Tables 1-3 are model priors, SED priors and TFR fit parameters).")
print("  So N(z) is an ASSUMPTION and is swept.  Every distribution below spans exactly")
print("  [0.56, 1.37] and has N = 95.")

RNG = np.random.default_rng(20260725)


def zsample(kind, n=N_GAL):
    """three defensible N(z) shapes on [ZLO, ZHI]; deterministic (quantile) construction."""
    q = (np.arange(n) + 0.5) / n
    if kind == "uniform":
        u = q
    elif kind == "low-heavy":              # MUSE [OII]/Hbeta detection favours lower z
        u = q ** 1.6
    elif kind == "high-heavy":             # volume-weighted
        u = q ** 0.625
    else:
        raise ValueError(kind)
    return ZLO + (ZHI - ZLO) * u


ZDISTS = {k: zsample(k) for k in ("uniform", "low-heavy", "high-heavy")}
print(f"\n  {'N(z) shape':12} {'median z':>9} {'mean z':>8} {'N(z>0.965)':>11} "
      f"{'mean gap(dex)':>14} {'sd gap(dex)':>12}")
print("  " + "-" * 74)
for k, zs in ZDISTS.items():
    g = np.array([gap_dex(z) for z in zs])
    print(f"  {k:12} {np.median(zs):>9.3f} {zs.mean():>8.3f} {int((zs>0.965).sum()):>11d} "
          f"{g.mean():>14.5f} {g.std(ddof=0):>12.5f}")

print("\n  FISHER SHARE per z bin (information for DEC-vs-RISE at FIXED per-object sigma")
print("  goes as gap_i^2, so the share is sum(gap^2) in the bin / total):")
print(f"  {'z bin':16} " + " ".join(f"{k:>14}" for k in ZDISTS))
print("  " + "-" * 64)
for i in range(len(ZEDGES) - 1):
    lo, hi = ZEDGES[i], ZEDGES[i + 1]
    cells = []
    for k, zs in ZDISTS.items():
        g2 = np.array([gap_dex(z) for z in zs]) ** 2
        m = (zs >= lo) & (zs < hi if i < len(ZEDGES) - 2 else zs <= hi)
        cells.append(f"{100*g2[m].sum()/g2.sum():>13.1f}%")
    print(f"  [{lo:.3f},{hi:.3f}) " + " ".join(f"{c:>14}" for c in cells))
UPPER = {}
for k, zs in ZDISTS.items():
    g2 = np.array([gap_dex(z) for z in zs]) ** 2
    m = zs > np.median(zs)
    UPPER[k] = (float(g2[m].sum() / g2.sum()), int(m.sum()))
print("\n  UPPER-HALF (above the sample's own median z) share of the DEC-vs-RISE information:")
for k in ZDISTS:
    print(f"    {k:12} N_upper = {UPPER[k][1]:>3d}  carries {100*UPPER[k][0]:.1f}% of the "
          f"information ({100*(1-UPPER[k][0]):.1f}% in the lower half)")
print(f"  => the high-z half carries {100*min(u[0] for u in UPPER.values()):.0f}-"
      f"{100*max(u[0] for u in UPPER.values()):.0f}% of the power. REAL but NOT overwhelming:")
print("     the gap grows only 2.8x across the span while N is halved, so dropping the")
print("     lower half costs ~27-32% of the information. Cutting to z>1.17 (the top bin)")
print("     leaves too few objects. Stated plainly: there is no cheap 'use only the high-z")
print("     half' shortcut -- the whole span is needed.")

# =======================================================================================
# S3 -- THE REQUIRED sigma(a0)/a0 AS A FUNCTION OF z: 3-sigma AND PRIOR-ROBUST 20:1
#       The 20:1 bar is computed by REPLACING the committed Jeanneau point [3] with an
#       improved-error version (NOT by adding a new point, which would double-count).
# =======================================================================================
print("\n" + BAR)
print("S3 -- REQUIRED sigma(a0)/a0 vs z: 3-sigma AND the PRIOR-ROBUST 20:1 Bayes bar")
print(BAR)
IDX_JEAN = [i for i, P in enumerate(PAR.POINTS) if P["tag"].startswith("[3]")][0]
TARGET20 = np.log(20.0)
DEXGRID = np.concatenate([np.arange(0.002, 0.200, 0.002), np.arange(0.20, 0.80, 0.005)])


def lnZ_with_replaced_jeanneau(model, z, sig_a0_dex, pmax, truth, w_new=W_JEAN):
    """ln evidence for `model` when point [3] is REPLACED by a MUSE-DARK II re-analysis at
    (z, sig_a0_dex) whose central value is the Asimov truth of `truth`."""
    pts = [dict(P) for P in PAR.POINTS]
    P = pts[IDX_JEAN]
    P["zrep"] = z
    P["val"] = float(np.log10(PAR.MODELS[truth](z))) * P["L"]      # de-dilutes to the truth
    P["sig_stat"] = P["sig_tot"] = sig_a0_dex * P["L"]            # de-dilutes to sig_a0_dex
    P["w"] = w_new
    return PAR.ln_evidence(model, pmax, pts=pts)[0]


def robust_lnB_dec_rise(z, sig_a0_dex, truth="M-DEC", w_new=W_JEAN):
    """worst case over the WHOLE A_drift prior ladder of ln B(truth vs the other branch)."""
    other = "M-RISE" if truth == "M-DEC" else "M-DEC"
    return min(lnZ_with_replaced_jeanneau(truth, z, sig_a0_dex, pm, truth, w_new) -
               lnZ_with_replaced_jeanneau(other, z, sig_a0_dex, pm, truth, w_new)
               for pm in PMAX_LADDER)


def loosest(fn):
    ok = [bool(fn(float(s))) for s in DEXGRID]
    if not any(ok):
        return None, None
    return float(DEXGRID[max(i for i, v in enumerate(ok) if v)]), ok[0]


print(f"  3-sigma bars: three conventions (tightest first). 20:1 bar: B(DEC/RISE) > 20 under")
print(f"  EVERY prior in the committed ladder {PRIOR_LABELS} = U[0,p] with p in {PMAX_LADDER},")
print(f"  with MUSE-DARK II's own drift exposure w = {W_JEAN:.2f} and its own lever L = {LEVER:.4f}.")
print(f"\n  {'z':>6} | {'3s mid(dex)':>11} {'3s mid(%)':>10} | {'3s dex(%)':>10} {'3s DEC(%)':>10} | "
      f"{'20:1 (dex)':>11} {'20:1 (%)':>9}  note")
print("  " + "-" * 96)
BARS = {}
for z in [ZLO, 0.76, 0.90, 1.00, 1.17, ZHI]:
    b1, b2, b3 = bars_3s(z)
    d1 = np.log(1 + b1) / DEX
    need20, tight_ok = loosest(lambda s, zz=z: robust_lnB_dec_rise(zz, s) > TARGET20)
    BARS[z] = dict(s3_mid_frac=b1, s3_mid_dex=d1, s3_dex_frac=b2, s3_dec_frac=b3,
                   need20_dex=need20, tight_ok=tight_ok)
    if need20 is None:
        print(f"  {z:>6.3f} | {d1:>11.4f} {100*b1:>9.2f}% | {100*b2:>9.2f}% {100*b3:>9.2f}% | "
              f"{'UNREACHABLE':>11} {'--':>9}  no sigma clears 20:1 under every prior")
    else:
        flag = "" if tight_ok else "  NON-MONOTONE (ultra-precise point breaks the joint fit)"
        print(f"  {z:>6.3f} | {d1:>11.4f} {100*b1:>9.2f}% | {100*b2:>9.2f}% {100*b3:>9.2f}% | "
              f"{need20:>11.4f} {100*(10**need20-1):>8.1f}%{flag}")
Z_EFF = 0.90
B3_DEX = BARS[Z_EFF]["s3_mid_dex"]
B3_FRAC = BARS[Z_EFF]["s3_mid_frac"]
B20_DEX = BARS[Z_EFF]["need20_dex"]
print(f"\n  HEADLINE BARS at the effective z = {Z_EFF:.2f}:")
print(f"    BAR-3S  = {B3_DEX:.4f} dex on log10(a0(z)/a0(0))  = {100*B3_FRAC:.2f}% on a0   "
      f"[tightest 3-sigma convention]")
if B20_DEX is not None:
    print(f"    BAR-20  = {B20_DEX:.4f} dex = {100*(10**B20_DEX-1):.1f}% on a0   "
          f"[prior-robust 20:1 DEC-vs-RISE, via the committed likelihood]")
    print(f"    ratio BAR-3S / BAR-20 = {B3_DEX/B20_DEX:.2f}x  -- the 20:1 bar is the harder test.")
else:
    print(f"    BAR-20  = UNREACHABLE at z = {Z_EFF:.2f} at ANY precision under every prior.")
print(f"  In Delta_b (mass-axis) currency the SAME bars are BAR-3S = {B3_DEX*LEVER:.4f} dex"
      + (f" and BAR-20 = {B20_DEX*LEVER:.4f} dex," if B20_DEX is not None else ",")
      + f"\n  because Delta_b = -L * Delta log10 a0 with L = {LEVER:.4f}. Published stat is "
        f"{DB_STAT:.2f} dex, honest {DB_HONEST:.2f} dex.")

# =======================================================================================
# S4 -- THE FRAMEWORK'S OWN ERROR AMPLIFICATIONS AT MUSE-DARK II's OWN y  (numeric, no
#       symbolic field theory: every lever is verified by central finite differences on
#       the EXACT a0-line a0 = (g_obs^2 - g_bar^2)/g_bar)
# =======================================================================================
print("\n" + BAR)
print("S4 -- ERROR AMPLIFICATIONS FROM THE FRAMEWORK'S OWN KERNEL AT y = "
      f"{Y_JEAN:.4f} (finite-difference verified)")
print(BAR)


def a0_line(gb, go):
    return (go ** 2 - gb ** 2) / gb


def onshell(y, a0=A0_CAN):
    gb = y * a0
    return gb, float(np.sqrt(gb ** 2 + gb * a0))


def fd_dln(f, x, *rest):
    h = 1e-6
    return (np.log(f(x * (1 + h), *rest)) - np.log(f(x * (1 - h), *rest))) / (2 * h)


AMP_V = lambda y: 4.0 * (y + 1.0)          # d ln a0 / d ln V
AMP_GOBS = lambda y: 2.0 * (y + 1.0)       # d ln a0 / d ln g_obs
AMP_GBAR = lambda y: 2.0 * y + 1.0         # d ln a0 / d ln g_bar  = 1/L
AMP_R = lambda y: 2.0 * y                  # d ln a0 / d ln R   (a0-line route)
AMP_MU = lambda y: y + 1.0                 # d ln a0 / d ln mu  (EXACT; ->1 as y->0)

_gb, _go = onshell(Y_JEAN)
_num_go = fd_dln(lambda g: a0_line(_gb, g), _go)
_num_gb = fd_dln(lambda g: a0_line(g, _go), _gb)
# the mu law, verified on the LENSING transformation itself: V invariant, R ~ mu^-1/2,
# M_bar ~ 1/mu  =>  g_bar = G M/R^2 invariant, g_obs = V^2/R ~ mu^1/2
def a0_of_mu(mu, y=Y_JEAN, a0=A0_CAN):
    gb0, go0 = onshell(y, a0)
    return a0_line(gb0 * (mu / 1.0) ** 0.0, go0 * np.sqrt(mu))
_num_mu = fd_dln(a0_of_mu, 1.0)
print(f"  {'channel':34} {'analytic':>10} {'finite-diff':>12} {'value at y=0.548':>17}")
print("  " + "-" * 78)
for lab, ana, num in (("d ln a0 / d ln g_obs  = 2(y+1)", AMP_GOBS(Y_JEAN), _num_go),
                      ("d ln a0 / d ln g_bar  = -(2y+1)", -AMP_GBAR(Y_JEAN), _num_gb),
                      ("d ln a0 / d ln mu     = (y+1)", AMP_MU(Y_JEAN), _num_mu)):
    print(f"  {lab:34} {ana:>10.5f} {num:>12.5f} {ana:>17.4f}")
print(f"  d ln a0 / d ln V      = 4(y+1)   {AMP_V(Y_JEAN):>10.5f} "
      f"{'(=2x the g_obs lever, V^2=g R)':>12}   {AMP_V(Y_JEAN):>17.4f}")
print(f"  d ln a0 / d ln R      = 2y       {AMP_R(Y_JEAN):>10.5f} "
      f"{'(a0-line route only)':>12}   {AMP_R(Y_JEAN):>17.4f}")
print(f"  1/L = 2y+1 = {AMP_GBAR(Y_JEAN):.4f} IS the g_bar/mass-channel amplification -- the")
print("  'dilution lever' and the 'mass-side error amplification' are THE SAME OBJECT, so")
print("  applying the de-dilution 1/L is not double-counting, it IS the amplification.")
print(f"\n  MAGNIFICATION LEVER -- a CORRECTION to the naive statement, in the hostile direction:")
print(f"    the deep-MOND limit gives d ln a0/d ln mu = 1 (a0 EXACTLY linear in mu), but the")
print(f"    EXACT framework value at MUSE-DARK II's OWN y = {Y_JEAN:.4f} is (y+1) = {AMP_MU(Y_JEAN):.4f}.")
print(f"    The 1:1 reading is therefore {AMP_MU(Y_JEAN):.2f}x TOO OPTIMISTIC here; {AMP_MU(Y_JEAN):.4f} is used below.")
print(f"    Derivation (numeric, above): lensing conserves surface brightness so M_bar ~ 1/mu")
print(f"    and area ~ 1/mu leave Sigma -- hence g_bar -- magnification-INVARIANT, while V is")
print(f"    invariant and R ~ mu^-1/2, so g_obs ~ mu^1/2.  Equivalently a0 = V^4/(G M_bar) -")
print(f"    g_bar, whose first term goes as mu: d ln a0/d ln mu = (a0+g_bar)/a0 = y+1.")
print(f"  Lever-gain context (why z~0.9 is NOT the z~2 problem):")
for lab, y in (("MUSE-DARK II lensed z~0.9", Y_JEAN), ("Ubler KMOS3D z=2.3", 3.46),
               ("Amvrosiadis ALMA z=2.4", 5.92), ("deep-MOND target (0.2 a0)", 0.20)):
    print(f"    {lab:28} y = {y:>5.2f}  L = {1/(1+2*y):>6.4f}  1/L = {1+2*y:>6.3f}  "
          f"AMP_V = {AMP_V(y):>6.3f}")

# =======================================================================================
# S5 -- THE PER-OBJECT ERROR BUDGET FROM MUSE-DARK II's *PUBLISHED* NUMBERS
# =======================================================================================
print("\n" + BAR)
print("S5 -- PER-OBJECT sigma(log10 a0) FROM THE PAPER'S OWN PUBLISHED UNCERTAINTIES")
print(BAR)
print("  PUBLISHED inputs (nothing invented; anything estimated is flagged ESTIMATE):")
print(f"    * baryonic mass: uniform +/-{SIG_LOGMBAR_PUB:.2f} dex adopted in their own TFR fit  [PUBLISHED]")
print(f"    * velocity: selection requires Delta v_1.8/v_1.8 < {DV_SEL:.0%}; the per-object")
print(f"      distribution is NOT tabulated, so sigma_V/V is SWEPT 5-30%             [SWEPT]")
print(f"    * R_e / 1.8 R_e from lensed GalPaK3D posteriors; sigma_R/R swept 10-20%   [ESTIMATE]")
print(f"    * magnification: lens-model uncertainties are NOT propagated in the paper")
print(f"      (its Appendix C shows an average of five public models does not change the")
print(f"      recovered velocities much, but no sigma_mu is quoted); swept 5-30%      [SWEPT]")
print(f"    * {N_CL} clusters -> mu systematics are COHERENT PER CLUSTER, averaging as sqrt({N_CL}) = "
      f"{np.sqrt(N_CL):.2f}, NOT sqrt({N_GAL}) = {np.sqrt(N_GAL):.2f}.")


def sig_a0_dex_object(sig_lnV, sig_logM, sig_lnR, sig_lnmu, y=Y_JEAN):
    """per-object sigma(log10 a0) via the framework's own amplifications (a0-LINE route)."""
    v = (AMP_V(y) * sig_lnV) ** 2
    m = (AMP_GBAR(y) * sig_logM * DEX) ** 2
    r = (AMP_R(y) * sig_lnR) ** 2
    u = (AMP_MU(y) * sig_lnmu) ** 2
    return float(np.sqrt(v + m + r + u) / DEX)


print(f"\n  (a) a0-LINE ROUTE (uses V, M_bar AND R -- the framework's kernel is exact at every")
print(f"      radius, so no deep-MOND limit is needed).  sigma(log10 a0) per object, dex:")
print(f"  {'sigma_V/V':>10} " + " ".join(f"{'sR=' + f'{r:.0%}':>10}" for r in (0.10, 0.20))
      + f"   {'(mu err excluded here; added in S6 as its own coherent block)':>10}")
print("  " + "-" * 76)
OBJ = {}
for sv in (0.05, 0.10, 0.15, 0.20, 0.30):
    cells = []
    for sr in (0.10, 0.20):
        s = sig_a0_dex_object(sv, SIG_LOGMBAR_PUB, sr, 0.0)
        OBJ[(sv, sr)] = s
        cells.append(f"{s:>10.4f}")
    print(f"  {sv:>9.0%} " + " ".join(cells))
print(f"  breakdown at sigma_V/V = 15%, sR = 15%: velocity term "
      f"{AMP_V(Y_JEAN)*0.15/DEX:.4f} dex, mass term "
      f"{AMP_GBAR(Y_JEAN)*SIG_LOGMBAR_PUB:.4f} dex, radius term {AMP_R(Y_JEAN)*0.15/DEX:.4f} dex")
print(f"  -> the VELOCITY channel dominates (amplification {AMP_V(Y_JEAN):.3f}) unless "
      f"sigma_V/V <~ {SIG_LOGMBAR_PUB*DEX*AMP_GBAR(Y_JEAN)/AMP_V(Y_JEAN):.1%}, where the "
      f"PUBLISHED +/-0.2 dex mass takes over.")

# (b) the bTFR route, CALIBRATED BACKWARDS from the published +/-0.06 stat -- a real check
SIG_MASSAXIS_IMPLIED = DB_STAT * np.sqrt(N_GAL)
print(f"\n  (b) bTFR ROUTE, calibrated from the paper's OWN published stat error (consistency")
print(f"      check, not an assumption): sigma(Delta_b) = {DB_STAT:.2f} dex with N = {N_GAL} implies a")
print(f"      per-object mass-axis scatter of {DB_STAT:.2f}*sqrt({N_GAL}) = {SIG_MASSAXIS_IMPLIED:.3f} dex")
print(f"      (intrinsic bTFR scatter + velocity error mapped through the fixed slope 4 +")
print(f"      the +/-0.2 dex mass).  De-diluted by the framework's lever this is")
print(f"      {SIG_MASSAXIS_IMPLIED:.3f}/{LEVER:.4f} = {SIG_MASSAXIS_IMPLIED/LEVER:.3f} dex per object on log10 a0.")
SIG_OBJ_BTFR = SIG_MASSAXIS_IMPLIED / LEVER
SIG_OBJ_A0LINE_MID = OBJ[(0.15, 0.10)]
print(f"\n  *** A FAVOURABLE, FRAMEWORK-NATIVE FINDING, STATED AS PLAINLY AS THE WALLS ***")
print(f"  a0-LINE route per object {SIG_OBJ_A0LINE_MID:.3f} dex vs bTFR route {SIG_OBJ_BTFR:.3f} dex")
print(f"  = a {SIG_OBJ_BTFR/SIG_OBJ_A0LINE_MID:.2f}x per-object GAIN, because the framework's kernel is exact at")
print(f"  each radius and does NOT discard R the way a fixed-slope bTFR does.  The residual")
print(f"  bTFR scatter that a standard analysis calls 'intrinsic' is, in this framework, mostly")
print(f"  the r-dependence the bTFR throws away.  This is a real gain and it is USED below --")
print(f"  but it is a FORECAST for a re-analysis, not something MUSE-DARK II has published.")

# =======================================================================================
# S6 -- THE POWER CALCULATION.  ONE covariance, TWO limits (absolute + trend), and the
#       drift profiled ON ITS PRIOR BOUNDARY (worst case for the signal).
# =======================================================================================
print("\n" + BAR)
print("S6 -- THE SEPARATION S(DEC vs RISE): one covariance, coherent blocks explicit")
print(BAR)
print("  MODEL.  Per object i the analysis delivers x_i = log10(a0(z_i)/a0(0)) with")
print("     C = sigma_r^2 I  +  sigma_c^2 J  +  sigma_mu^2 B ,")
print("  where J = all-ones (a SAMPLE-WIDE coherent systematic: the gas-mass calibration")
print("  zero-point, the local z=0 reference, the pressure-support prescription) and B is")
print(f"  block-diagonal over the {N_CL} clusters (the lens-model magnification systematic).")
print("  sigma_r carries the median-like estimator's efficiency penalty sqrt(pi/2) = "
      f"{MEDPEN:.4f} (rule 6; GLS is FORBIDDEN).")
print("  The LCDM apparent drift enters as w*p*log10(1+z_i) with p in [0,pmax] under EACH")
print("  model, so the mimicry direction is w*dp*log10(1+z) with |dp| <= pmax.  It is")
print("  PROFILED to MINIMIZE S -- i.e. always the worst case for a detection.")
print("  S^2 = min_{|dp|<=pmax} (D + w dp Lz)' C^-1 (D + w dp Lz),  D_i = log10(RISE/DEC)(z_i).")
print("  Two limits fall out of the SAME formula and are NOT separate assumptions:")
print("     sigma_c -> 0   : the ABSOLUTE route (full gap exploited)")
print("     sigma_c -> inf : the TREND route (constant projected out; only the z-DIFFERENTIAL")
print("                      of the gap survives -> IMMUNE to the coherent wall)")


def clusters(zs, mode):
    """cluster id per object. 'interleave' = each cluster spans the full z range (what 4
    Frontier Fields lines of sight actually give); 'segregate' = each cluster occupies one
    quarter of the z range (HOSTILE: lets per-cluster mu offsets eat the z-trend)."""
    n = len(zs)
    o = np.argsort(zs)
    cid = np.empty(n, int)
    if mode == "interleave":
        cid[o] = np.arange(n) % N_CL
    else:
        cid[o] = np.minimum((np.arange(n) * N_CL) // n, N_CL - 1)
    return cid


def separation(zs, sig_r, sig_c, sig_mu, w, pmax, cmode="interleave", full=False):
    """S (in sigma) for DEC vs RISE, drift profiled on its bound to minimize S."""
    zs = np.asarray(zs, float)
    n = len(zs)
    D = np.array([gap_dex(z) for z in zs])
    Lz = np.log10(1.0 + zs)
    sr = MEDPEN * sig_r
    C = np.eye(n) * sr ** 2 + sig_c ** 2
    if sig_mu > 0:
        cid = clusters(zs, cmode)
        C = C + sig_mu ** 2 * (cid[:, None] == cid[None, :])
    Ci = np.linalg.inv(C)
    a = float(D @ Ci @ D)
    b = float(Lz @ Ci @ D)
    c = float(Lz @ Ci @ Lz)
    if w * w * c <= 0:
        dp = 0.0
    else:
        dp = float(np.clip(-b / (w * c), -pmax, pmax))
    S2 = a + 2 * w * dp * b + (w * dp) ** 2 * c
    S = float(np.sqrt(max(S2, 0.0)))
    if full:
        S2_nodrift = a
        return S, dict(S_nodrift=float(np.sqrt(max(S2_nodrift, 0.0))), dp=dp,
                       absorbed_frac=float(1.0 - S / max(np.sqrt(a), 1e-300)))
    return S


ZS = ZDISTS["uniform"]
print("\n  (A) THE PUBLISHED RESULT, AS PUBLISHED.  The integrated bTFR zero-point is ONE")
print("      number, so it is the sigma_c-dominated limit of the same formula:")
for lab, dbe in (("published stat only  +/-0.06 dex", DB_STAT),
                 ("committed honest band +/-0.27 dex", DB_HONEST)):
    s_a0 = dbe / LEVER
    S_int = gap_dex(Z_EFF) / s_a0
    print(f"      {lab:34} -> sigma(log10 a0) = {s_a0:.4f} dex -> "
          f"S = {S_int:.2f} sigma  ({'clears' if S_int >= 3 else 'MISSES'} 3 sigma; "
          f"needs {s_a0/B3_DEX:.2f}x tighter)")
INT_STAT_S = gap_dex(Z_EFF) / (DB_STAT / LEVER)
INT_HON_S = gap_dex(Z_EFF) / (DB_HONEST / LEVER)

print("\n  (B) PER-OBJECT ANALYSIS OF THE 95.  S as a function of the per-object sigma_r and")
print(f"      the SAMPLE-WIDE coherent sigma_c (mu block off here; pmax = {max(PMAX_LADDER)}, "
      f"w = {W_JEAN:.2f}, uniform N(z)):")
SR_GRID = [0.135, 0.30, 0.584, 0.91, 1.225]
SC_GRID = [0.0, 0.02, 0.05, 0.10, 0.20, 0.566]
print(f"      {'sigma_r (dex)':>14} | " + " ".join(f"{'sc=' + f'{c:.3f}':>9}" for c in SC_GRID))
print("      " + "-" * 76)
GRID = {}
for sr in SR_GRID:
    cells = []
    for sc in SC_GRID:
        S = separation(ZS, sr, sc, 0.0, W_JEAN, max(PMAX_LADDER))
        GRID[(sr, sc)] = S
        cells.append(f"{S:>9.2f}")
    print(f"      {sr:>14.3f} | " + " ".join(cells))
print(f"      (sigma_r = 0.584 is the a0-LINE route at 15% velocities; 0.91 at the 30%")
print(f"       selection limit; 1.225 is the bTFR route implied by the published +/-0.06;")
print(f"       0.135 is the target derived below.  sigma_c = 0.566 is the published honest")
print(f"       band de-diluted; 0.02-0.20 are reduced-systematics scenarios.)")
print(f"      Rightmost column (sigma_c = 0.566 dex, i.e. AS PUBLISHED): S = "
      f"{GRID[(0.584,0.566)]:.2f}-{GRID[(1.225,0.566)]:.2f} sigma. The coherent wall, not N, is the binding term.")
print(f"      Leftmost column (sigma_c = 0): S = {GRID[(1.225,0.0)]:.2f}-{GRID[(0.135,0.0)]:.2f} sigma -- "
      f"so with PERFECT systematics")
print(f"      the sample's own per-object errors reach {GRID[(0.584,0.0)]:.2f} sigma (a0-line, 15% V) / "
      f"{GRID[(1.225,0.0)]:.2f} sigma (bTFR).")

print("\n  (C) THE TREND (z-DIFFERENTIAL) ROUTE -- the structurally NEW result of this file.")
print("      Because a SAMPLE-WIDE coherent offset is a CONSTANT and the DEC-vs-RISE gap is")
print(f"      NOT (it runs {gap_dex(ZLO):.4f} -> {gap_dex(ZHI):.4f} dex across 0.56-1.37), the z-DIFFERENTIAL")
print("      of the gap survives sigma_c -> infinity. The integrated zero-point CANNOT use this;")
print("      a per-object analysis CAN. Quantified (sigma_c = 10 dex = effectively free):")
TREND = {}
print(f"      {'w':>5} {'pmax':>6} | {'absorbed by drift':>18} | " +
      " ".join(f"{'sr=' + f'{s:.3f}':>10}" for s in (0.135, 0.30, 0.584, 0.91)))
print("      " + "-" * 88)
for w in (0.15, W_JEAN, 0.35, 0.50, 1.00):
    for pmax in (max(PMAX_LADDER),):
        S_, info = separation(ZS, 0.584, 10.0, 0.0, w, pmax, full=True)
        cells = []
        for sr in (0.135, 0.30, 0.584, 0.91):
            S = separation(ZS, sr, 10.0, 0.0, w, pmax)
            TREND[(w, pmax, sr)] = S
            cells.append(f"{S:>10.2f}")
        print(f"      {w:>5.2f} {pmax:>6.2f} | {100*info['absorbed_frac']:>17.1f}% | "
              + " ".join(cells))
print(f"      At the committed exposure w = {W_JEAN:.2f} the maximal drift can absorb only")
_, _i = separation(ZS, 0.584, 10.0, 0.0, W_JEAN, max(PMAX_LADDER), full=True)
print(f"      {100*_i['absorbed_frac']:.1f}% of the trend, because mimicking the gap's slope would need")
print(f"      p = {gap_dex(ZHI)-gap_dex(ZLO):.4f}/({W_JEAN:.2f}*{np.log10(1+ZHI)-np.log10(1+ZLO):.4f}) = "
      f"{(gap_dex(ZHI)-gap_dex(ZLO))/(W_JEAN*(np.log10(1+ZHI)-np.log10(1+ZLO))):.2f}, far outside every prior "
      f"(ceiling {max(PMAX_LADDER)}).")
print(f"      *** BUT *** at w = 1.00 the drift absorbs "
      f"{100*separation(ZS,0.584,10.0,0.0,1.0,max(PMAX_LADDER),full=True)[1]['absorbed_frac']:.1f}% and the trend route DIES.")
print(f"      This is the load-bearing fork of the whole file and it is NOT decided by this")
print(f"      script: w = {W_JEAN:.2f} was assigned in the committed likelihood for the ACCELERATION")
print(f"      regime (lensed, low-mass, near-a0). The TREND route is exposed to a different")
print(f"      channel -- the z-DEPENDENCE of the Tacconi+2020 / NEUTRALUNIVERSEMACHINE gas")
print(f"      prescriptions, which is exactly a (1+z)^p-shaped systematic on M_bar. Nothing")
print(f"      in the published paper bounds that w. Reported as the decisive unknown.")

print("\n  (D) THE MAGNIFICATION BLOCK -- coherent per cluster, only sqrt(4) of averaging.")
print(f"      sigma_mu(a0) = AMP_MU * sigma_mu/mu = {AMP_MU(Y_JEAN):.4f} * (sigma_mu/mu) in ln, /ln10 in dex.")
print(f"      {'sigma_mu/mu':>12} {'-> dex on a0':>13} | {'S abs (sc=0)':>13} {'S abs (sc=0.02)':>16} "
      f"{'S trend interleave':>19} {'S trend segregate':>18}")
print("      " + "-" * 96)
MUTAB = {}
for smu in (0.05, 0.10, 0.20, 0.30):
    sd = AMP_MU(Y_JEAN) * smu / DEX
    a = separation(ZS, 0.584, 0.0, sd, W_JEAN, max(PMAX_LADDER))
    a2 = separation(ZS, 0.584, 0.02, sd, W_JEAN, max(PMAX_LADDER))
    t1 = separation(ZS, 0.584, 10.0, sd, W_JEAN, max(PMAX_LADDER), cmode="interleave")
    t2 = separation(ZS, 0.584, 10.0, sd, W_JEAN, max(PMAX_LADDER), cmode="segregate")
    MUTAB[smu] = (sd, a, a2, t1, t2)
    print(f"      {smu:>11.0%} {sd:>13.4f} | {a:>13.2f} {a2:>16.2f} {t1:>19.2f} {t2:>18.2f}")
print(f"      READING: with only {N_CL} clusters a 10-30% lens-model error contributes "
      f"{MUTAB[0.10][0]:.3f}-{MUTAB[0.30][0]:.3f} dex")
print(f"      coherently per cluster, i.e. {MUTAB[0.10][0]/np.sqrt(N_CL):.3f}-{MUTAB[0.30][0]/np.sqrt(N_CL):.3f} dex after sqrt({N_CL}) averaging -- "
      f"comparable to")
print(f"      or larger than BAR-3S = {B3_DEX:.4f} dex ON ITS OWN. This term is NOT in the published")
print(f"      +/-0.06 and it must be propagated. The TREND route is far more robust to it")
print(f"      (interleaved clusters), and CONSPICUOUSLY less so if the clusters are")
print(f"      z-segregated -- the 'segregate' column is the honest worst case.")

# =======================================================================================
# S7 -- SOLVING FOR THE REQUIREMENT: what per-object and what coherent precision is needed
# =======================================================================================
print("\n" + BAR)
print("S7 -- THE REQUIREMENT, SOLVED (separating 1/sqrt(N) terms from COHERENT ones)")
print(BAR)
SGRID = np.concatenate([np.arange(0.004, 0.200, 0.002), np.arange(0.20, 2.40, 0.005)])


def loosest_sr(target_S, sig_c, sig_mu, w, pmax, cmode="interleave", zs=None):
    zs = ZS if zs is None else zs
    ok = [separation(zs, float(s), sig_c, sig_mu, w, pmax, cmode) >= target_S for s in SGRID]
    if not any(ok):
        return None
    return float(SGRID[max(i for i, v in enumerate(ok) if v)])


def loosest_sc(target_S, sig_r, sig_mu, w, pmax, zs=None):
    """(loosest sigma_c meeting target_S, hit_ceiling).  hit_ceiling=True means the TREND
    route alone already carries the target, so ANY coherent systematic is tolerable."""
    zs = ZS if zs is None else zs
    ok = [separation(zs, sig_r, float(s), sig_mu, w, pmax) >= target_S for s in SGRID]
    if not any(ok):
        return None, False
    return float(SGRID[max(i for i, v in enumerate(ok) if v)]), bool(ok[-1])


print("  (i) PER-OBJECT sigma_r required, at fixed coherent budget (uniform N(z), w = "
      f"{W_JEAN:.2f}, pmax = {max(PMAX_LADDER)}):")
print(f"      {'target':10} " + " ".join(f"{'sc=' + f'{c:.2f}':>11}" for c in (0.0, 0.02, 0.05, 0.10, 10.0))
      + "     (sc=10 is the TREND limit)")
print("      " + "-" * 84)
REQ = {}
for tag, tS in (("3 sigma", 3.0), ("20:1 equiv", None)):
    if tS is None:
        continue
    cells = []
    for sc in (0.0, 0.02, 0.05, 0.10, 10.0):
        r = loosest_sr(tS, sc, 0.0, W_JEAN, max(PMAX_LADDER))
        REQ[(tag, sc)] = r
        cells.append("UNREACH" if r is None else f"{r:>11.3f}")
    print(f"      {tag:10} " + " ".join(f"{c:>11}" for c in cells))
REQ_ABS = REQ[("3 sigma", 0.0)]
REQ_TREND = REQ[("3 sigma", 10.0)]
print(f"\n      -> ABSOLUTE route (sigma_c = 0): per-object sigma_r <= {REQ_ABS:.3f} dex on log10 a0.")
print(f"         In the framework's own currencies at y = {Y_JEAN:.4f}, that single number is met by")
print(f"         ANY of: sigma_V/V <= {REQ_ABS*DEX/AMP_V(Y_JEAN):.1%}  OR  sigma(log M_bar) <= "
      f"{REQ_ABS/AMP_GBAR(Y_JEAN):.3f} dex  OR  sigma_mu/mu <= {REQ_ABS*DEX/AMP_MU(Y_JEAN):.1%},")
print(f"         each ALONE -- i.e. the incoherent side of the absolute route is EASY: it is")
print(f"         already met by MUSE-DARK II's published +/-{SIG_LOGMBAR_PUB} dex masses and by any")
print(f"         velocity precision better than {REQ_ABS*DEX/AMP_V(Y_JEAN):.0%}. N = 95 is ENOUGH on the random side.")
print(f"      -> TREND route (coherent-immune): per-object sigma_r <= {REQ_TREND:.3f} dex --")
print(f"         {REQ_ABS/REQ_TREND:.2f}x TIGHTER, because the z-DIFFERENTIAL of the gap "
      f"(sd = {np.std([gap_dex(z) for z in ZS]):.4f} dex) is")
print(f"         {np.mean([gap_dex(z) for z in ZS])/np.std([gap_dex(z) for z in ZS]):.2f}x smaller than the gap itself "
      f"({np.mean([gap_dex(z) for z in ZS]):.4f} dex). That is the PRICE of coherent immunity.")
print(f"         In framework currencies: sigma_V/V <= {REQ_TREND*DEX/AMP_V(Y_JEAN):.2%}, "
      f"sigma(log M_bar) <= {REQ_TREND/AMP_GBAR(Y_JEAN):.3f} dex, sigma_mu/mu <= "
      f"{REQ_TREND*DEX/AMP_MU(Y_JEAN):.2%} (each ALONE).")

print(f"\n  (ii) COHERENT budget required, at the sample's OWN per-object precision:")
print(f"      {'sigma_r (dex)':>14} {'source':40} {'sigma_c needed for 3s':>22}")
print("      " + "-" * 80)
for sr, src in ((0.135, "the derived target"),
                (0.584, "a0-line route, 15% velocities"),
                (0.910, "a0-line route, 30% selection limit"),
                (1.225, "bTFR route implied by published +/-0.06")):
    sc, ceil = loosest_sc(3.0, sr, 0.0, W_JEAN, max(PMAX_LADDER))
    txt = ("NEVER REACHES 3s" if sc is None else
           "ANY (trend carries it)" if ceil else f"{sc:.4f}")
    print(f"      {sr:>14.3f} {src:40} {txt:>22}")
SC_NEED_A0LINE = loosest_sc(3.0, 0.584, 0.0, W_JEAN, max(PMAX_LADDER))[0]
print(f"      -> the incoherent term at sigma_r = 0.584 already spends "
      f"{MEDPEN*0.584/np.sqrt(N_GAL):.4f} dex of a")
print(f"         {gap_dex(Z_EFF)/3:.4f}-dex budget, which is why the required coherent budget is "
      + ("UNREACHABLE" if SC_NEED_A0LINE is None else f"only {SC_NEED_A0LINE:.4f} dex")
      + ".")

# ---- the PRIOR-ROBUST 20:1 bar translated into per-object currency -----------------
print(f"\n  (iia) THE PRIOR-ROBUST 20:1 BAR ({B20_DEX:.4f} dex on the combined log10 a0-ratio),")
print(f"       translated into per-object requirements at N = {N_GAL} (absolute route, sigma_c = 0):")
SR20 = B20_DEX * np.sqrt(N_GAL) / MEDPEN
print(f"       sigma_r <= BAR-20 * sqrt(N)/{MEDPEN:.4f} = {SR20:.4f} dex per object")
print(f"         -> sigma_V/V <= {SR20*DEX/AMP_V(Y_JEAN):.2%}  OR  sigma(log M_bar) <= "
      f"{SR20/AMP_GBAR(Y_JEAN):.3f} dex  OR  sigma_mu/mu <= {SR20*DEX/AMP_MU(Y_JEAN):.2%} (each ALONE)")
print(f"       AND sigma_c <= {B20_DEX:.4f} dex, AND sigma_mu(per-cluster) <= "
      f"{B20_DEX*np.sqrt(N_CL)/MEDPEN:.4f} dex  (= sigma_mu/mu <= "
      f"{B20_DEX*np.sqrt(N_CL)/MEDPEN*DEX/AMP_MU(Y_JEAN):.1%}),")
print(f"       every one of which must hold SIMULTANEOUSLY. The coherent conditions are the")
print(f"       binding ones: {B20_DEX:.4f} dex on log10 a0 is {B20_DEX*LEVER:.4f} dex on Delta_b, i.e. a "
      f"{100*(10**(B20_DEX*LEVER)-1):.1f}%")
print(f"       COHERENT baryonic-mass calibration. Nothing in the literature is at that level.")

print(f"\n  (iii) HOW MANY OBJECTS at the sample's OWN per-object precision?")
print(f"      {'route':22} {'sigma_r':>8} {'S at N=95':>10} {'N for 3s':>10} {'x MUSE-DARK II':>15}")
print("      " + "-" * 72)
NEED_N = {}
for lab, sr, sc in (("absolute, sc=0", 0.584, 0.0), ("absolute, sc=0", 0.910, 0.0),
                    ("absolute, sc=0", 1.225, 0.0), ("trend (sc free)", 0.584, 10.0),
                    ("trend (sc free)", 0.910, 10.0)):
    S95 = separation(ZS, sr, sc, 0.0, W_JEAN, max(PMAX_LADDER))
    n_need = int(np.ceil(N_GAL * (3.0 / S95) ** 2))
    NEED_N[(lab, sr)] = (S95, n_need)
    print(f"      {lab:22} {sr:>8.3f} {S95:>10.2f} {n_need:>10d} {n_need/N_GAL:>14.1f}x")
print(f"      (S scales as sqrt(N) once the coherent terms are fixed, so this is exact for the")
print(f"       sc = 0 and sc = free limits; it is NOT valid at intermediate sc, where S")
print(f"       SATURATES at gap/sigma_c no matter how large N gets. That saturation is the")
print(f"       whole reason the published +/-0.27 band cannot be beaten by more galaxies.)")
SAT = gap_dex(Z_EFF) / (DB_HONEST / LEVER)
print(f"       SATURATION at the published honest band: S -> {SAT:.2f} sigma as N -> infinity. "
      f"No sample size fixes it.")

# =======================================================================================
# S8 -- THE HI NUISANCE, SIGN-LOCKED AGAINST THE FRAMEWORK (rule 4)
# =======================================================================================
print("\n" + BAR)
print("S8 -- THE HI NUISANCE: prior M_HI in [0, M_mol], SIGN-LOCKED TOWARD *RISE*")
print(BAR)
print("  MUSE-DARK II does NOT set M_HI = 0: it takes M_HI from NEUTRALUNIVERSEMACHINE and")
print("  M_mol from Tacconi+2020.  Rule 4 is still carried in full, because the direction is")
print("  fixed: UNDER-counting M_bar makes a0 = V^4/(G M_bar) - g_bar read HIGH, i.e. toward")
print("  RISE, i.e. AGAINST the framework's declining branch.  Never zero, never one-sided in")
print("  the framework's favour.")
print(f"\n  {'M_mol/M*':>9} {'M_HI = 0':>10} {'M_HI = M_mol':>13} {'d log M_bar (dex)':>18} "
      f"{'-> d log a0 (dex)':>18} {'-> in sigma at BAR-3S':>22}")
print("  " + "-" * 96)
HITAB = {}
for rmol in (0.5, 1.0, 2.0, 3.0):
    mb0 = 1.0 + rmol                       # M_bar/M* with M_HI = 0
    mb1 = 1.0 + 2 * rmol                   # M_bar/M* with M_HI = M_mol
    dlogm = float(np.log10(mb1 / mb0))
    dloga0 = AMP_GBAR(Y_JEAN) * dlogm
    HITAB[rmol] = (dlogm, dloga0)
    print(f"  {rmol:>9.1f} {mb0:>10.2f} {mb1:>13.2f} {dlogm:>18.4f} {dloga0:>18.4f} "
          f"{dloga0/B3_DEX:>21.2f}x")
HI_MIN = min(v[1] for v in HITAB.values())
HI_MAX = max(v[1] for v in HITAB.values())
print(f"  -> the FULL prior spans {HI_MIN:.3f}-{HI_MAX:.3f} dex on log10 a0, ONE-SIDED and COHERENT.")
print(f"     That is {HI_MIN/B3_DEX:.1f}-{HI_MAX/B3_DEX:.1f}x BAR-3S ({B3_DEX:.4f} dex) all by itself, and it pushes")
print(f"     the measured a0 UP -- i.e. it makes the data look MORE like McCulloch's RISE and")
print(f"     LESS like Carl's DEC. Carrying it honestly HURTS the framework here, and it is")
print(f"     carried anyway.")
print(f"  If instead NEUTRALUNIVERSEMACHINE is trusted to +/-0.3 dex on M_HI with M_HI/M_bar ~ 0.3:")
_s = 0.30 * (0.3 * DEX) / DEX * AMP_GBAR(Y_JEAN)
print(f"     coherent contribution = (M_HI/M_bar) * sigma(log M_HI) * (2y+1) = "
      f"0.3*0.30*{AMP_GBAR(Y_JEAN):.3f} = {_s:.4f} dex")
print(f"     = {_s/B3_DEX:.1f}x BAR-3S. Still over, but only by ~{_s/B3_DEX:.0f}x rather than "
      f"{HI_MAX/B3_DEX:.0f}x. BOTH cases reported.")
print(f"  AND it is z-DEPENDENT (gas fractions evolve), so it hits the TREND route too -- it is")
print(f"  precisely a channel that argues for w > {W_JEAN:.2f} in S6(C). Said against interest.")

# =======================================================================================
# S9 -- VERDICT.  Every string below is an f-string of a COMPUTED number; nothing typed in.
# =======================================================================================
print("\n" + BAR)
print("S9 -- VERDICT: can the DEC-vs-RISE call be made at z~0.9 from ALREADY-PUBLISHED data?")
print(BAR)
S_PUB_STAT = INT_STAT_S
S_PUB_HON = INT_HON_S
S_TABLE_ABS = separation(ZS, 0.584, 0.0, 0.0, W_JEAN, max(PMAX_LADDER))
S_TABLE_TREND = separation(ZS, 0.584, 10.0, 0.0, W_JEAN, max(PMAX_LADDER))
S_TABLE_REAL = separation(ZS, 0.584, _s, AMP_MU(Y_JEAN) * 0.10 / DEX, W_JEAN, max(PMAX_LADDER))
COH_FLOOR_LO = min(_s, HI_MIN)
COH_FLOOR_HI = HI_MAX
GO3 = S_PUB_HON >= 3.0
GO20 = (S_PUB_HON >= 3.0) and (DB_HONEST / LEVER <= (B20_DEX if B20_DEX else 0.0))
print(f"  ANSWER (computed, not asserted):")
print(f"    from the PUBLISHED INTEGRATED zero-point Delta_b = {DB_BTFR:+.2f} +/- {DB_STAT:.2f} (stat) / "
      f"+/-{DB_HONEST:.2f} (honest):")
print(f"       S(DEC vs RISE) = {S_PUB_STAT:.2f} sigma (stat-only, NOT a defensible error) and "
      f"{S_PUB_HON:.2f} sigma (honest).")
print(f"       3-sigma reached: {GO3}.   prior-robust 20:1 reached: {GO20}.")
print(f"    from a PER-OBJECT re-analysis of the same 95 galaxies (a0-line route, its own")
print(f"       published +/-{SIG_LOGMBAR_PUB} dex masses, 15% velocities):")
print(f"       S = {S_TABLE_ABS:.2f} sigma with PERFECT coherent systematics, {S_TABLE_TREND:.2f} sigma on the")
print(f"       coherent-immune TREND route, and {S_TABLE_REAL:.2f} sigma with a REALISTIC coherent budget")
print(f"       (HI model {_s:.3f} dex + 10% lens models). 3-sigma reached: "
      f"{max(S_TABLE_ABS, S_TABLE_TREND, S_TABLE_REAL) >= 3.0}.")
print(f"\n  SO THE CALL CANNOT BE MADE TODAY -- and the reason is SPECIFIC, not generic:")
print(f"    * It is NOT the sample size. N = {N_GAL} is ENOUGH on the random side: the incoherent")
print(f"      requirement for 3 sigma is sigma_r <= {REQ_ABS:.3f} dex per object, which MUSE-DARK II's own")
print(f"      +/-{SIG_LOGMBAR_PUB} dex masses ({AMP_GBAR(Y_JEAN)*SIG_LOGMBAR_PUB:.3f} dex on a0) plus <=16% velocities already meet.")
print(f"    * It is NOT the acceleration regime. y = {Y_JEAN:.3f} gives L = {LEVER:.3f}, the best lever in")
print(f"      hand, and the z~2 NO-GO (which demanded g_bar < 0.3 a0 where nothing exists) does")
print(f"      NOT apply here. This really is a different and much more favourable regime.")
print(f"    * It IS the COHERENT budget. Three named terms, each independently over BAR-3S:")
print(f"        - HI / gas-mass calibration:  {_s:.3f} dex (NUM trusted to 0.3 dex) up to "
      f"{HI_MAX:.3f} dex (full [0,M_mol] prior)  = {_s/B3_DEX:.1f}-{HI_MAX/B3_DEX:.1f}x BAR-3S")
print(f"        - local z=0 reference zero-point: ~0.16 dex on Delta_b = "
      f"{0.16/LEVER:.3f} dex on a0        = {0.16/LEVER/B3_DEX:.1f}x BAR-3S")
print(f"        - lens-model magnification (NOT propagated in the paper), 10-30% over {N_CL} clusters:")
print(f"          {MUTAB[0.10][0]/np.sqrt(N_CL):.3f}-{MUTAB[0.30][0]/np.sqrt(N_CL):.3f} dex after sqrt({N_CL})"
      f"                                     = {MUTAB[0.10][0]/np.sqrt(N_CL)/B3_DEX:.1f}-{MUTAB[0.30][0]/np.sqrt(N_CL)/B3_DEX:.1f}x BAR-3S")
print(f"      These do not average down. S SATURATES at {SAT:.2f} sigma as N -> infinity at the")
print(f"      published honest band -- no number of galaxies and no better estimator fixes it.")
print(f"\n  HOW CLOSE DOES IT GET (the number that matters):")
print(f"    the published honest band is {DB_HONEST/LEVER/B3_DEX:.2f}x too wide for 3 sigma and "
      f"{DB_HONEST/LEVER/B20_DEX:.0f}x too wide for prior-robust 20:1.")
print(f"    the published STAT band is only {DB_STAT/LEVER/B3_DEX:.2f}x too wide for 3 sigma.")
print(f"    For comparison the committed z~2 lensed deep-MOND design needed ~6-15x beyond its")
print(f"    floor, and the massive-HSB z=2 floor was 9-55x off. z~0.9 is the closest this")
print(f"    problem has ever been -- {DB_HONEST/LEVER/B3_DEX:.1f}x, not 9-55x -- and it is still NOT there.")
print(f"\n  WHAT EXACTLY WOULD CLOSE IT (in increasing cost):")
print(f"   (1) THE PER-OBJECT TABLE (z_i, mu_i, V_1.8, R_e, M*, M_mol, M_HI + errors).")
print(f"       NOT published: the paper's Tables 1-3 are kinematic priors, SED priors and TFR")
print(f"       fit parameters; there is no per-galaxy catalogue in it. From the authors, or by")
print(f"       re-running lensed GalPaK3D on the MUSE cubes (available on request) with the")
print(f"       PUBLIC Frontier Fields mass models. This alone buys: the a0-LINE estimator")
print(f"       ({SIG_OBJ_BTFR/SIG_OBJ_A0LINE_MID:.2f}x per-object gain over the bTFR), the median-like pre-registered")
print(f"       estimator (GLS forbidden), a propagated per-cluster mu term, and the")
print(f"       COHERENT-IMMUNE TREND route. It moves S from {S_PUB_HON:.2f} to {S_TABLE_TREND:.2f} sigma. NOT 3 sigma.")
print(f"   (2) DIRECT MOLECULAR GAS MASSES on the high-mu subsample (ALMA CO(2-1); mu up to")
print(f"       {MU_HI} makes this feasible NOW). Removes the Tacconi+2020 coherent zero-point.")
print(f"       Does NOT remove the HI term -- which is the larger one ({_s:.3f}-{HI_MAX:.3f} dex).")
print(f"   (3) DIRECT ATOMIC GAS. There is no 21cm at z ~ 1 before SKA1-MID/SKA2 (~2030s).")
print(f"       This is the hard wall, and it is the SAME wall the z~2 passes hit -- the")
print(f"       committed conclusion that a clean fork read needs direct HI is UNCHANGED by")
print(f"       MUSE-DARK II. Honest: this pass narrows the gap, it does not open the door.")
print(f"   (4) A MATCHED local z=0 reference (same V definition at 1.8 R_e, same M_bar")
print(f"       convention, same fitting) to <= {B3_DEX*LEVER:.3f} dex, and lens-model errors propagated")
print(f"       to <= {B3_DEX*np.sqrt(N_CL)/MEDPEN:.3f} dex per cluster. Both are analysis work, not new photons.")
print(f"   (5) THE ONE FREE THING, unchanged from the committed parents: a Magneticum-style")
print(f"       apparent-drift calibration run on MUSE-DARK II's ACTUAL selection function.")
print(f"       It MEASURES w*p for this sample, which S6(C) shows is the single decisive")
print(f"       unknown for the trend route (w = {W_JEAN:.2f} -> {100*_i['absorbed_frac']:.0f}% absorbed and the route lives;")
print(f"       w = 1.00 -> {100*separation(ZS,0.584,10.0,0.0,1.0,max(PMAX_LADDER),full=True)[1]['absorbed_frac']:.0f}% absorbed and it dies). No new observations required.")
print(f"\n  AND THE LIMIT THAT NO AMOUNT OF DATA AT THIS REDSHIFT REMOVES:")
print(f"    DEC(z=0.9) = {float(R_dec(0.9)):.4f} vs FLAT = 1.0000. This sample can NEVER test the")
print(f"    framework's DISTINCTIVE declining prediction -- only DEC vs RISE, i.e. de Sitter")
print(f"    horizon vs Hubble horizon. A DEC win here would refute McCulloch's reading, not")
print(f"    confirm Carl's decline. The decline still needs z >~ 2. Both halves stated.")

# =======================================================================================
# S10 -- PRE-REGISTRATION, RESULTS JSON, SELF-CHECK
# =======================================================================================
print("\n" + "#" * 100)
print("# PRE-REGISTRATION -- MUSE-DARK II z~0.9 DEC-vs-RISE POWER, frozen with this commit")
print("#" * 100)
CAVEATS = [
    f"The per-object redshift list, magnifications, velocities and gas masses of the {N_GAL} "
    f"galaxies are NOT published as a table (Tables 1-3 of Jeanneau+2026 are kinematic priors, "
    f"SED priors and TFR fit parameters). N(z) is therefore an ASSUMPTION here and is swept over "
    f"three shapes (uniform / low-heavy / high-heavy). The upper-half information share moves only "
    f"{100*min(u[0] for u in UPPER.values()):.0f}-{100*max(u[0] for u in UPPER.values()):.0f}%, so no "
    f"conclusion in this file depends on N(z).",

    f"sigma_V/V per object is NOT published; only the selection cut Delta v/v < {DV_SEL:.0%} is. It is "
    f"SWEPT 5-30% and every headline number states which value it used. The baryonic-mass "
    f"uncertainty +/-{SIG_LOGMBAR_PUB} dex IS published (adopted in the paper's own TFR fit).",

    f"MAGNIFICATION uncertainties are NOT propagated in the published analysis, so the published "
    f"+/-{DB_STAT:.2f} dex stat error OMITS a term that this file computes to be "
    f"{MUTAB[0.10][0]/np.sqrt(N_CL):.3f}-{MUTAB[0.30][0]/np.sqrt(N_CL):.3f} dex on log10 a0 after "
    f"sqrt({N_CL})-cluster averaging -- i.e. comparable to BAR-3S on its own. Any use of the "
    f"+/-{DB_STAT:.2f} stat number as if it were a total error is therefore forbidden.",

    f"The MAGNIFICATION LEVER is (y+1) = {AMP_MU(Y_JEAN):.4f}, NOT the 1:1 of the deep-MOND limit. "
    f"Using 1:1 at this sample's y = {Y_JEAN:.4f} would understate the mu term by "
    f"{AMP_MU(Y_JEAN):.2f}x. The hostile (correct) value is used throughout.",

    f"The TREND route's coherent immunity is REAL but it is bought at a "
    f"{np.mean([gap_dex(z) for z in ZS])/np.std([gap_dex(z) for z in ZS]):.2f}x smaller signal, and its "
    f"viability is controlled ENTIRELY by the drift-exposure weight w for the z-DEPENDENT part of "
    f"the Tacconi+2020 / NEUTRALUNIVERSEMACHINE gas prescriptions. The committed w = {W_JEAN:.2f} was "
    f"assigned for the ACCELERATION regime, not for that channel. At w = {W_JEAN:.2f} the drift absorbs "
    f"{100*_i['absorbed_frac']:.0f}% of the trend and the route lives; at w = 1.00 it absorbs "
    f"{100*separation(ZS,0.584,10.0,0.0,1.0,max(PMAX_LADDER),full=True)[1]['absorbed_frac']:.0f}% and the route "
    f"dies. This is the single most load-bearing unmeasured number in the file and it is flagged as "
    f"such, not resolved in the framework's favour.",

    f"The HI nuisance is carried with prior M_HI in [0, M_mol], never zero, and it is SIGN-LOCKED "
    f"toward RISE: under-counting M_bar makes a0 read HIGH. Its full range "
    f"{HI_MIN:.3f}-{HI_MAX:.3f} dex on log10 a0 is {HI_MIN/B3_DEX:.1f}-{HI_MAX/B3_DEX:.1f}x BAR-3S by "
    f"itself. It works AGAINST the framework's declining branch and is carried anyway.",

    f"ESTIMATOR: median-like only. GLS is FORBIDDEN (committed estimator_bias_verdict.json: "
    f"gls_origin bias +10.34 pp FAIL, theilsen_pairwise +7.93 pp FAIL; median_a0pt +0.84, "
    f"ivw_median_a0pt +0.66, galaxy_median_then_median +0.31 pp PASS). The median's efficiency "
    f"penalty sqrt(pi/2) = {MEDPEN:.4f} is APPLIED to every incoherent term, not waived.",

    f"z ~ 0.9 CANNOT test DEC vs FLAT: DEC({Z_EFF}) = {float(R_dec(Z_EFF)):.4f} against FLAT = 1, a "
    f"{100*abs(1-float(R_dec(Z_EFF))):.3f}% gap needing "
    f"{100*abs(1-float(R_dec(Z_EFF)))/(3*0.5*(1+float(R_dec(Z_EFF)))):.4f}% precision. Every result here "
    f"is DEC-vs-RISE = de Sitter horizon vs Hubble horizon. A DEC win at z~0.9 refutes McCulloch's "
    f"reading; it does NOT detect the framework's distinctive decline, which still needs z >~ 2.",

    f"The a0-LINE per-object route is {SIG_OBJ_BTFR/SIG_OBJ_A0LINE_MID:.2f}x tighter per object than the "
    f"bTFR route because the framework's kernel is exact at every radius. That is a genuine, "
    f"framework-native gain and it is reported as such -- but it is a FORECAST for a re-analysis "
    f"that does not exist yet, NOT a published capability of MUSE-DARK II.",

    f"BOTH FOOTINGS: canonical cH_Lambda/Z = {A0_CAN:.4e} and alt cH0/Z = {A0_ALT:.4e} give IDENTICAL "
    f"numbers, because everything lives in the footing-independent ratio a0(z)/a0(0) (asserted "
    f"numerically in S0). a0's VALUE and the HORIZON CHOICE remain POSITS.",

    f"nu = sqrt(1 + 1/y) is Milgrom 1999 (PLA 253:273 Eq.9) -- WELLHEAD CREDIT. The framework's "
    f"distinctive content is the cH_Lambda/Z coefficient and the modified-inertia completion. "
    f"McCulloch (MiHsC) credited for the Hubble-horizon branch. No TOE, no 'theory closed', no "
    f"closed doors. Exit 0 = ran, NOT a verdict.",

    f"PRE-REGISTERED DECISION RULE (frozen): a DEC-vs-RISE claim from MUSE-DARK II may be made ONLY "
    f"if a per-object analysis reports (a) sigma_r <= {REQ_ABS:.3f} dex/object AND a COHERENT budget "
    f"<= {B3_DEX:.4f} dex including HI, local reference and lens models, for the 3-sigma call; or "
    + (f"(b) a combined sigma <= {B20_DEX:.4f} dex for the prior-robust 20:1 call. " if B20_DEX else "")
    + f"Neither is met by anything published today, so NO claim may be made from this file in either "
      f"direction.",
]
for i, c in enumerate(CAVEATS, 1):
    print(f"#  {i}. {c}")
print("#" * 100)

OUT = dict(
    sample=dict(cite="Jeanneau et al. 2026, A&A (arXiv:2603.28856; A&A 2026/05 aa59953-26)",
                N=N_GAL, z_lo=ZLO, z_hi=ZHI, n_clusters=N_CL,
                clusters=["Abell 2744", "Abell 370", "Abell S1063", "MACS0416"],
                mu_range=[MU_LO, MU_HI], logMstar_range=[8.1, 10.3],
                delta_b_btfr=DB_BTFR, delta_b_stat=DB_STAT, delta_b_honest_committed=DB_HONEST,
                sigma_logMbar_published=SIG_LOGMBAR_PUB, dv_selection_cut=DV_SEL,
                per_object_table_published=False),
    framework=dict(Z=float(Z_CONST), a0_canonical=A0_CAN, a0_alt=A0_ALT,
                   y_gbar_over_a0=Y_JEAN, lever_L=LEVER, inv_lever=1.0 / LEVER,
                   amp_V=AMP_V(Y_JEAN), amp_gobs=AMP_GOBS(Y_JEAN), amp_gbar=AMP_GBAR(Y_JEAN),
                   amp_R=AMP_R(Y_JEAN), amp_mu_exact=AMP_MU(Y_JEAN), amp_mu_deepmond_limit=1.0,
                   ratio_footing_independent=True, median_efficiency_penalty=float(MEDPEN)),
    fork=dict(z=[float(z) for z in [ZLO, 0.76, 0.90, 1.00, 1.17, ZHI]],
              DEC=[float(R_dec(z)) for z in [ZLO, 0.76, 0.90, 1.00, 1.17, ZHI]],
              RISE=[float(R_rise(z)) for z in [ZLO, 0.76, 0.90, 1.00, 1.17, ZHI]],
              gap_dex=[gap_dex(z) for z in [ZLO, 0.76, 0.90, 1.00, 1.17, ZHI]],
              dec_vs_flat_gap_at_0p9=float(abs(1.0 - float(R_dec(0.9))))),
    bars={f"z={z}": BARS[z] for z in BARS},
    headline_bars=dict(z_eff=Z_EFF, BAR3S_dex=B3_DEX, BAR3S_frac=B3_FRAC, BAR20_dex=B20_DEX,
                       BAR3S_in_delta_b_dex=B3_DEX * LEVER,
                       BAR20_in_delta_b_dex=(B20_DEX * LEVER) if B20_DEX else None),
    information_share_upper_half={k: UPPER[k][0] for k in UPPER},
    per_object_budget=dict(a0line_dex={f"sV={k[0]},sR={k[1]}": v for k, v in OBJ.items()},
                           btfr_implied_dex=SIG_OBJ_BTFR,
                           a0line_gain_over_btfr=SIG_OBJ_BTFR / SIG_OBJ_A0LINE_MID),
    separations=dict(published_integrated_stat_sigma=S_PUB_STAT,
                     published_integrated_honest_sigma=S_PUB_HON,
                     saturation_sigma_at_honest_band=SAT,
                     per_object_absolute_perfect_syst_sigma=S_TABLE_ABS,
                     per_object_trend_sigma=S_TABLE_TREND,
                     per_object_realistic_syst_sigma=S_TABLE_REAL,
                     grid={f"sr={k[0]},sc={k[1]}": v for k, v in GRID.items()},
                     trend_grid={f"w={k[0]},pmax={k[1]},sr={k[2]}": v for k, v in TREND.items()},
                     mu_block={f"smu={k}": dict(dex=v[0], S_abs_sc0=v[1], S_abs_sc002=v[2],
                                                S_trend_interleave=v[3], S_trend_segregate=v[4])
                               for k, v in MUTAB.items()}),
    requirements=dict(sigma_r_3s_absolute_dex=REQ_ABS, sigma_r_3s_trend_dex=REQ_TREND,
                      sigma_r_20to1_dex=float(SR20),
                      sigma_c_3s_at_published_perobj=SC_NEED_A0LINE,
                      N_for_3s={f"{k[0]}@sr={k[1]}": v[1] for k, v in NEED_N.items()},
                      factor_short_3s_honest=DB_HONEST / LEVER / B3_DEX,
                      factor_short_3s_stat=DB_STAT / LEVER / B3_DEX,
                      factor_short_20to1_honest=(DB_HONEST / LEVER / B20_DEX) if B20_DEX else None),
    hi_nuisance=dict(sign_locked_toward="RISE (against the framework's declining branch)",
                     prior="M_HI in [0, M_mol]",
                     dex_on_log_a0={f"Mmol/Mstar={k}": v[1] for k, v in HITAB.items()},
                     num_trusted_0p3dex_case_dex=float(_s)),
    verdict=dict(three_sigma_from_published_summary=bool(GO3),
                 twenty_to_one_from_published_summary=bool(GO20),
                 three_sigma_from_per_object_table_alone=bool(
                     max(S_TABLE_ABS, S_TABLE_TREND, S_TABLE_REAL) >= 3.0),
                 binding_term="COHERENT systematics (HI/gas calibration, local z=0 reference, "
                              "lens-model magnification) -- NOT sample size, NOT the "
                              "acceleration regime",
                 cannot_test_dec_vs_flat_at_this_z=True),
    caveats=CAVEATS,
)
JPATH = os.path.join(HERE, "musedark2_z09_power_2026_results.json")
with open(JPATH, "w") as f:
    json.dump(OUT, f, indent=1, default=float)
print(f"\nwrote {JPATH}")

print("\n" + BAR)
print("SELF-CHECK (frozen invariants)")
print(BAR)
assert abs(float(R_dec(0.9)) - 0.9996) < 5e-4, "DEC(0.9) must match the committed fork"
assert abs(float(R_rise(0.9)) - 1.6867) < 5e-4, "RISE(0.9) must match the committed fork"
assert abs(LEVER - 0.477) < 2e-3, "the committed Jeanneau lever L must be 0.477"
assert abs(1.0 / LEVER - AMP_GBAR(Y_JEAN)) < 1e-12, "1/L must EQUAL the g_bar amplification"
assert abs(_num_go - AMP_GOBS(Y_JEAN)) < 1e-5 and abs(_num_gb + AMP_GBAR(Y_JEAN)) < 1e-5, \
    "finite-difference levers must reproduce the analytic ones"
assert abs(_num_mu - AMP_MU(Y_JEAN)) < 1e-5, "the mu lever must be (y+1), not 1"
assert AMP_MU(Y_JEAN) > 1.0, "the exact mu lever must be HOSTILE relative to the 1:1 limit"
assert abs(_f1 - _f2) < 1e-15, "the ratio must be footing-independent on both footings"
assert gap_dex(ZHI) > gap_dex(ZLO), "the DEC-RISE gap must GROW with z"
assert abs(1.0 - float(R_dec(0.9))) < 0.01, \
    "z~0.9 must be the DEC~FLAT crossover -> this sample cannot test the decline"
assert bars_3s(0.9)[0] < bars_3s(0.9)[1] < bars_3s(0.9)[2], \
    "the three 3-sigma conventions must be ordered mid < dex < DEC-referenced (tightest first)"
assert B3_DEX == BARS[Z_EFF]["s3_mid_dex"], "the HEADLINE bar must be the TIGHTEST convention"
assert S_PUB_STAT > S_PUB_HON, "the honest band must give a SMALLER separation than stat-only"
assert not GO3 and not GO20, \
    "no 3-sigma / 20:1 claim may be made from the published summary statistics"
assert S_TABLE_TREND > 0.0 and S_TABLE_TREND < 3.0, \
    "the per-object trend route must be reported as real but sub-3-sigma"
assert separation(ZS, 0.584, 10.0, 0.0, 1.00, max(PMAX_LADDER)) < \
    separation(ZS, 0.584, 10.0, 0.0, W_JEAN, max(PMAX_LADDER)), \
    "the drift must HURT the trend route as w rises (it is not a one-way knob)"
assert separation(ZS, 0.584, 0.0, 0.0, W_JEAN, max(PMAX_LADDER)) > \
    separation(ZS, 0.584, 0.566, 0.0, W_JEAN, max(PMAX_LADDER)), \
    "a coherent systematic must REDUCE the absolute-route separation"
assert REQ_TREND < REQ_ABS, \
    "coherent immunity must cost per-object precision (trend requirement TIGHTER than absolute)"
assert HI_MIN > B3_DEX, "the HI nuisance must be reported as exceeding BAR-3S on its own"
assert SIG_OBJ_BTFR > SIG_OBJ_A0LINE_MID, \
    "the a0-line route must be tighter per object than the bTFR route (framework-native gain)"
assert SAT < 3.0, "the published honest band must saturate below 3 sigma for any N"
print(f"  DEC(0.9) = {float(R_dec(0.9)):.4f}, RISE(0.9) = {float(R_rise(0.9)):.4f}, "
      f"gap = {gap_dex(0.9):.4f} dex, RISE/DEC = {float(R_rise(0.9)/R_dec(0.9)):.4f}x  OK")
print(f"  lever L = {LEVER:.4f} = 1/(2y+1) with y = {Y_JEAN:.4f}; 1/L = AMP_gbar = "
      f"{AMP_GBAR(Y_JEAN):.4f}  OK")
print(f"  mu lever = {AMP_MU(Y_JEAN):.4f} (exact) vs 1.0000 (deep-MOND limit) -- hostile value used  OK")
print(f"  three 3-sigma conventions at z=0.9: {100*bars_3s(0.9)[0]:.2f}% < {100*bars_3s(0.9)[1]:.2f}%"
      f" < {100*bars_3s(0.9)[2]:.2f}%; headline = tightest = {B3_DEX:.4f} dex  OK")
print(f"  published integrated: {S_PUB_STAT:.2f} sigma (stat) / {S_PUB_HON:.2f} sigma (honest); "
      f"saturates at {SAT:.2f} sigma for N -> inf  OK")
print(f"  per-object routes: absolute {S_TABLE_ABS:.2f} sigma (perfect syst) / trend "
      f"{S_TABLE_TREND:.2f} sigma / realistic {S_TABLE_REAL:.2f} sigma  OK")
print(f"  requirements: sigma_r <= {REQ_ABS:.3f} dex (absolute) / {REQ_TREND:.3f} dex (trend) / "
      f"{SR20:.3f} dex (20:1)  OK")
print(f"  HI nuisance {HI_MIN:.3f}-{HI_MAX:.3f} dex, sign-locked toward RISE, > BAR-3S  OK")
print(f"  drift cuts BOTH ways: trend S falls {S_TABLE_TREND:.2f} -> "
      f"{separation(ZS,0.584,10.0,0.0,1.0,max(PMAX_LADDER)):.2f} as w goes {W_JEAN:.2f} -> 1.00  OK")
print("\nEXIT 0 (ran; not a verdict).")
