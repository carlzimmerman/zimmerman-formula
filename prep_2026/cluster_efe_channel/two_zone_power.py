#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
two_zone_power.py -- DEDICATED statistical power calc for the cluster-member EFE
relational sigma-spread discriminator (MI history-dependent inertia vs MG field-sector
zero), as a PROPER TWO-ZONE comparison:  D = <ln(sigma_int/sigma_bary)>_first-infall
                                             - <ln(sigma_int/sigma_bary)>_ancient
at a fixed deprojected caustic external-field bin (Rhee+2017 phase-space zones).  2026-07-23.

ARMS (does NOT relitigate) the published theorem+methods paper
  real_research/papers/MI_SIGMA_SPREAD_2026.md  (Zenodo 21421896).

HARD CALIBRATION RULES (this repo penalizes a manufactured WIN and a manufactured DEFICIT
EQUALLY).  Enforced here:
  (1) CARRY THE FULL KERNEL-HOSTAGE RANGE.  The MG-impossible fixed-field history contrast is
      kernel-hostage at the framework-committed memory tau_mem=2Z/H_Lambda~203 Gyr:
        * LOW-PASS reading   S ~ 1.3% (canonical) / 1.5% (alt)   [decaying-memory corner]
        * PURE-DELAY reading S ~ 8-13% (fiducial 10.5%)          [|K|=1 group-delay corner]
      Detectability is reported SEPARATELY for the two readings; they are NEVER averaged.
  (2) The confound floor is an IRREDUCIBLE, N-INDEPENDENT systematic on the contrast:
        projection alias ~1-2% (which ALREADY encodes finite Rhee zone-tag purity, Sec 4.4)
        (+) tidal/environmental residual ~2-8% (after the F3 radial-profile separator)
        -> quadrature.  Detection requires the signal to beat BOTH the statistical error AND the
      floor.  The floor does not average down, so it sets a HARD CEILING z_max = S/floor that no N
      can exceed; if S < z_target*floor, detection is IMPOSSIBLE at any N.
      NOTE (no double-count): the paper's quoted 1.3% / 8-13% are the MEASURED post-tagging
      contrast (Sec 4.2), so the signal is used at FACE VALUE and the tagging/purity limitation
      lives ONLY in the projection floor -- diluting the signal by purity AND charging a projection
      floor would manufacture a deficit.
  (3) The discriminating POWER is theorem-grade vs the ENTIRE MG class; a DETECTION additionally
      requires beating same-signed dynamical confounds by DESIGN (F3 radial profile + F2 sign),
      not by the theorem.  The tidal term of the floor IS that residual, carried as a systematic.
  (4) Both a0 footings carried; a0 cancels at fixed dimensionless depth (signal footing-invariant
      to <=~15%).  No "theory closed".
  (5) tau_mem=2Z/H_Lambda~203 Gyr >> orbital/crossing times -> pure-phase branch SATURATES; the
      spread is the residual (hence the kernel-hostage smallness).  No invented resonance.

SCOPE (from the paper, restated, not weakened):  MI-CLASS-GENERIC (separates history-dependent
inertia from MG; does NOT separate this framework from Milgrom 2503.07106).  Does NOT test a0's
value or the sign s=-1.  MG field-sector zero at fixed true field is the sole theorem-grade claim.

numpy-only, exit 0.  Read-only w.r.t. the rest of the repo.  Every headline number is a guarded
assert.  Credit: Milgrom 1983 / 1999 PLA 253:273 (nu-kernel wellhead) / 2022 PRD 106:064060 (MI
two-frequency EFE) / 2503.07106 (linear MI, also spreads).  Scaffolding: Rhee+2017 ApJ 843:128,
Wolf+2010 MNRAS 406:1220, Abdullah+2020, Owers+2017, Law+2021.
"""
import numpy as np

LINE = "=" * 100
def h(t):
    print(); print(LINE); print(t); print(LINE)

# ---------------------------------------------------------------------------------------------
# 0.  INPUTS -- all traceable to the paper / cited literature.  ln = natural log; a fractional
#     spread S maps to a log-contrast ln(1+S).  (dex = log10; ln = 2.3026*dex.)
# ---------------------------------------------------------------------------------------------
Z          = np.sqrt(32*np.pi/3)          # 5.789
TAU_MEM_HL = 2*Z                          # tau_mem*H_Lambda = 11.58 (exact, footing-free)
A0_CAN, A0_ALT = 9.36e-11, 1.13e-10

# --- kernel-hostage SIGNAL readings (fixed-field first-infall - ancient MEASURED contrast),
#     BOTH footings.  Paper Sec 4.2, 5.4.  a0 cancels at fixed depth (canonical/alt = member remap).
SIG = {
    "LOW-PASS":   {"can": 0.013, "alt": 0.015, "band": (0.013, 0.015),
                   "note": "decaying-memory corner; residence-time-limited"},
    "PURE-DELAY": {"can": 0.105, "alt": 0.105, "band": (0.080, 0.130),
                   "note": "|K|=1 group-delay corner; bounded transient survives"},
}

# --- per-galaxy scatter of ln(sigma_int/sigma_bary) at fixed field, decomposed:
#     s_FJ : intrinsic astrophysical scatter of the Wolf-normalized relation, IRREDUCIBLE per
#            galaxy even at perfect measurement.  0.05-0.08 dex -> 0.115-0.184 ln; fiducial 0.065 dex.
#     e_sig: per-galaxy internal-sigma MEASUREMENT precision (fractional); resolved-IFU dE/dSph
#            delivers ~3-8% -> adds ~0.03-0.08 in ln(sigma_int).  The lever the task probes.
S_FJ_LN   = {"opt": 0.115, "fid": 0.150, "pes": 0.184}   # 0.05 / 0.065 / 0.08 dex
E_SIG_IFU = {"opt": 0.03,  "fid": 0.05,  "pes": 0.08}    # IFU fractional sigma precision
def s_ln(s_fj, e_sig):
    return float(np.hypot(s_fj, e_sig))

# --- IRREDUCIBLE systematic floor on the CONTRAST (quadrature of projection + tidal residual).
#     projection alias ~1-2% (Sec 4.4; ENCODES finite zone-tag purity p=0.5-0.9);
#     tidal/environmental same-signed ~2-8%, "opt" = F3 outward-profile separator working well.
PROJ  = {"opt": 0.010, "fid": 0.015, "pes": 0.020}
TIDAL = {"opt": 0.020, "fid": 0.050, "pes": 0.080}
FLOOR = {k: float(np.hypot(PROJ[k], TIDAL[k])) for k in PROJ}   # 0.0224 / 0.0522 / 0.0825

# --- Rhee+2017 zone fractions of the tagged carrier pool (first-infall zone A, ancient zone E).
F_FIRST, F_ANC = 0.33, 0.50

print(f"tau_mem*H_Lambda = 2Z = {TAU_MEM_HL:.3f}  ->  tau_mem = 203 Gyr (can) / 168 Gyr (alt), footing-free")
print(f"per-galaxy ln-scatter s_ln = hypot(s_FJ, e_sig).  Systematic floor on the contrast "
      f"(quadrature proj(+)tidal): opt {FLOOR['opt']*100:.1f}%  fid {FLOOR['fid']*100:.1f}%  pes {FLOOR['pes']*100:.1f}%")

# ---------------------------------------------------------------------------------------------
# helper estimators (two-zone contrast; balanced 'per zone' N and realistic Rhee split)
# ---------------------------------------------------------------------------------------------
def z_ceiling(S, fl):                       # N -> infinity structural ceiling
    return np.log1p(S) / fl

def N_req_balanced(S, sln, fl, ztar):       # N PER ZONE (N1=N2=Nz) to reach ztar; None if ceiling fails
    lead = np.log1p(S)
    if lead <= ztar*fl:
        return None
    se_max = np.sqrt((lead/ztar)**2 - fl**2)
    return 2.0*sln**2 / se_max**2

def N_req_rhee(S, sln, fl, ztar):           # TOTAL tagged N with Rhee split; None if ceiling fails
    lead = np.log1p(S)
    if lead <= ztar*fl:
        return None
    se_max = np.sqrt((lead/ztar)**2 - fl**2)
    return (1.0/F_FIRST + 1.0/F_ANC) * sln**2 / se_max**2

def z_at_total(Ntot, S, sln, fl):           # achieved z at a real Rhee-split carrier count
    N1, N2 = Ntot*F_FIRST, Ntot*F_ANC
    se_stat = sln*np.sqrt(1.0/N1 + 1.0/N2)
    return np.log1p(S) / np.hypot(se_stat, fl)

def fmt(x):
    return "  NO N" if x is None else f"{x:8.0f}"

# ---------------------------------------------------------------------------------------------
# 1.  THE STRUCTURAL CEILING  z_max = S/floor  (N -> infinity).  Load-bearing, PER READING.
# ---------------------------------------------------------------------------------------------
h(" (1) SYSTEMATIC CEILING  z_max = S/floor  (the N->infinity limit; the floor never averages down)")
print("   If z_max < 3 the reading CANNOT reach 3sigma at ANY N; if z_max < 5, no 5sigma at any N.")
print("   Signal at FACE VALUE (measured post-tagging contrast); purity lives in the projection floor.\n")
print(f"   {'reading':11s} {'S(can)':>7s} | {'zmax@2.2%':>10s} {'zmax@5.2%':>10s} {'zmax@8.2%':>10s}   floor menu")
for rd in ("LOW-PASS", "PURE-DELAY"):
    S = SIG[rd]["can"]
    zc = {fl: z_ceiling(S, FLOOR[fl]) for fl in FLOOR}
    print(f"   {rd:11s} {S*100:6.1f}% | {zc['opt']:10.2f} {zc['fid']:10.2f} {zc['pes']:10.2f}   "
          f"proj 1-2% (+) tidal 2-8%")

zmax_lp_best = z_ceiling(SIG["LOW-PASS"]["can"],   FLOOR["opt"])
zmax_pd_best = z_ceiling(SIG["PURE-DELAY"]["can"], FLOOR["opt"])
zmax_pd_fid  = z_ceiling(SIG["PURE-DELAY"]["can"], FLOOR["fid"])
zmax_pd_lo_best = z_ceiling(SIG["PURE-DELAY"]["band"][0], FLOOR["opt"])   # bottom of band, best floor
zmax_pd_hi_best = z_ceiling(SIG["PURE-DELAY"]["band"][1], FLOOR["opt"])   # top of band, best floor
print(f"\n   LOW-PASS,   even best (F3-cleaned ~2.2%) floor:  z_max = {zmax_lp_best:.2f}  "
      f"-> {'BELOW 1: undetectable at ANY N' if zmax_lp_best < 1 else '??'}")
print(f"   PURE-DELAY, fiducial (~5.2%) floor:              z_max = {zmax_pd_fid:.2f}  "
      f"-> {'CANNOT reach 3sigma at any N' if zmax_pd_fid < 3 else 'clears 3sigma'}")
print(f"   PURE-DELAY, F3-cleaned (~2.2%) floor:            z_max = {zmax_pd_best:.2f}  "
      f"(band {zmax_pd_lo_best:.2f} @8% .. {zmax_pd_hi_best:.2f} @13%)")
assert zmax_lp_best < 1.0,  "low-pass must sit below the most optimistic floor (undetectable at any N)"
assert zmax_pd_fid  < 3.0,  "pure-delay at the fiducial ~5% floor must FAIL the 3sigma ceiling"
assert zmax_pd_best > 3.0,  "pure-delay at the F3-cleaned ~2.2% floor must CLEAR the 3sigma ceiling"
assert zmax_pd_hi_best > 5.0 and zmax_pd_lo_best < 5.0, \
    "5sigma pure-delay ceiling should clear only near the TOP of the 8-13% band at the best floor"

# ---------------------------------------------------------------------------------------------
# 2.  BREAK-EVEN FLOOR  floor_max = S/z_target  (the floor you must beat for ANY N to work).
# ---------------------------------------------------------------------------------------------
h(" (2) BREAK-EVEN FLOOR  floor_max = S/z_target  (max systematic that still ADMITS a detection)")
print(f"   Stated floor menu: projection alone ~1-2%; tidal residual ~2-8%; quadrature ~2.2-8.3%.\n")
print(f"   {'reading':11s} {'S(can)':>7s} | {'floor<= 3s':>11s} {'floor<= 5s':>11s}   feasibility")
for rd in ("LOW-PASS", "PURE-DELAY"):
    S = SIG[rd]["can"]
    be3, be5 = np.log1p(S)/3.0, np.log1p(S)/5.0
    if be3 < PROJ["opt"]:
        feas = "3s IMPOSSIBLE: break-even below projection floor alone"
    elif be3 < FLOOR["opt"]:
        feas = "3s needs floor below best quadrature (tidal->~0)"
    else:
        feas = "3s feasible iff F3 drives floor to ~2%"
    print(f"   {rd:11s} {S*100:6.1f}% | {be3*100:10.2f}% {be5*100:10.2f}%   {feas}")
be3_lp = np.log1p(SIG["LOW-PASS"]["can"])/3.0
assert be3_lp < PROJ["opt"], "low-pass 3s break-even floor must sit below the projection floor alone (=> impossible)"

# ---------------------------------------------------------------------------------------------
# 3.  REQUIRED N -- per zone (balanced) AND total (Rhee split), for combos that clear the ceiling.
# ---------------------------------------------------------------------------------------------
h(" (3) REQUIRED N  (per zone balanced | total Rhee-split);  'NO N' = ceiling fails, no count works")
sln_fid = s_ln(S_FJ_LN["fid"], E_SIG_IFU["fid"])
print(f"   fiducial per-galaxy s_ln = hypot(s_FJ 0.150, e_sig 0.050) = {sln_fid:.3f}\n")
print(f"   {'reading':11s} {'floor':>6s} | {'Nz(3s)':>9s} {'Nz(5s)':>9s} | {'Ntot(3s)':>9s} {'Ntot(5s)':>9s}")
for rd in ("LOW-PASS", "PURE-DELAY"):
    S = SIG[rd]["can"]
    for flab in ("opt", "fid", "pes"):
        fl = FLOOR[flab]
        row = (N_req_balanced(S, sln_fid, fl, 3.0), N_req_balanced(S, sln_fid, fl, 5.0),
               N_req_rhee(S, sln_fid, fl, 3.0),     N_req_rhee(S, sln_fid, fl, 5.0))
        print(f"   {rd:11s} {fl*100:5.1f}% | {fmt(row[0]):>9s} {fmt(row[1]):>9s} | {fmt(row[2]):>9s} {fmt(row[3]):>9s}")

Nz3_pd = N_req_balanced(SIG["PURE-DELAY"]["can"], sln_fid, FLOOR["opt"], 3.0)
Nt3_pd = N_req_rhee(SIG["PURE-DELAY"]["can"], sln_fid, FLOOR["opt"], 3.0)
# 5sigma pure-delay needs best-case everything (top of band, best precision, best floor):
Nz5_pd = N_req_balanced(SIG["PURE-DELAY"]["band"][1], s_ln(S_FJ_LN["opt"], E_SIG_IFU["opt"]), FLOOR["opt"], 5.0)
print(f"\n   PURE-DELAY 3sigma @ F3-cleaned 2.2% floor: ~{Nz3_pd:.0f} per zone  (~{Nt3_pd:.0f} total tagged, Rhee split).")
print(f"   PURE-DELAY 5sigma needs best-case (S~13%, e_sig 3%, s_FJ 0.05dex, floor 2.2%): ~{Nz5_pd:.0f} per zone.")
assert N_req_balanced(SIG["LOW-PASS"]["can"], sln_fid, FLOOR["opt"], 3.0) is None, \
    "low-pass must return NO N at 3sigma even at the best floor"
assert 40 < Nz3_pd < 200, "pure-delay 3s per-zone N should land in the tens-to-~150 exploratory range"

# ---------------------------------------------------------------------------------------------
# 4.  REQUIRED-N vs PER-GALAXY PRECISION CURVE (pure-delay, F3-cleaned floor).
# ---------------------------------------------------------------------------------------------
h(" (4) REQUIRED-N vs PER-GALAXY sigma PRECISION  (pure-delay S=10.5%, floor 2.2%)")
print("   Even PERFECT sigma (e_sig->0) cannot beat the intrinsic s_FJ; precision is a WEAK lever.\n")
print(f"   {'e_sig (IFU %)':>13s} {'s_ln':>7s} {'Nz(3s)':>9s} {'Nz(5s)':>9s}")
S_pd = SIG["PURE-DELAY"]["can"]
curve = []
for e in (0.0, 0.03, 0.05, 0.08, 0.12):
    sln = s_ln(S_FJ_LN["fid"], e)
    nz3 = N_req_balanced(S_pd, sln, FLOOR["opt"], 3.0)
    nz5 = N_req_balanced(S_pd, sln, FLOOR["opt"], 5.0)
    curve.append((e, sln, nz3, nz5))
    print(f"   {e*100:11.0f}%  {sln:7.3f} {fmt(nz3):>9s} {fmt(nz5):>9s}")
n_perfect, n_8pct = curve[0][2], curve[3][2]
print(f"\n   e_sig 8% -> 0%: Nz(3s) moves {n_8pct:.0f} -> {n_perfect:.0f}  (only x{n_8pct/n_perfect:.2f}).")
print("   BINDING levers: (i) the systematic floor (ceiling), (ii) carrier COUNT, (iii) intrinsic s_FJ.")
assert n_8pct/n_perfect < 1.6, "per-galaxy precision must be a weak lever (intrinsic scatter dominates)"

# ---------------------------------------------------------------------------------------------
# 5.  ACHIEVED z ON REAL CARRIER SAMPLES  (data_scout counts; per reading; both floors).
# ---------------------------------------------------------------------------------------------
h(" (5) ACHIEVED z ON REAL CARRIER SAMPLES  (Rhee split; fiducial s_ln; PER READING, no averaging)")
print("   carrier pools (data_scout/overlap_power.py): MMU-MaNGA ~40-77 ; +SAMI stack ~135-237 ;")
print("   clean-exploratory target 300-500 ; dedicated wide dwarf-IFU / ELT ~10^3-10^4.")
samples = [("MMU-MaNGA", 77), ("MaNGA+SAMI stack", 237), ("clean target", 400), ("dedicated survey", 2000)]
achieved = {}
for flab, fl in (("F3-cleaned 2.2%", FLOOR["opt"]), ("fiducial 5.2%", FLOOR["fid"])):
    print(f"\n   --- floor = {flab} ---")
    print(f"   {'sample':20s} {'N':>6s} | {'z LOW-PASS(1.3%)':>17s} {'z PURE-DELAY(10.5%)':>20s}")
    for nm, N in samples:
        zlp = z_at_total(N, SIG["LOW-PASS"]["can"],   sln_fid, fl)
        zpd = z_at_total(N, SIG["PURE-DELAY"]["can"], sln_fid, fl)
        achieved[(flab, nm)] = (zlp, zpd)
        print(f"   {nm:20s} {N:6d} | {zlp:17.2f} {zpd:20.2f}")
# low-pass must be sub-3sigma everywhere; pure-delay must be a HINT (<3) on public data at best floor
assert all(achieved[("F3-cleaned 2.2%", nm)][0] < 1.5 for nm, _ in samples), "low-pass must stay <1.5s on all real samples"
assert achieved[("F3-cleaned 2.2%", "MaNGA+SAMI stack")][1] < 3.5, "public-stack pure-delay must be exploratory, not a clean kill"
# reconciliation with the committed overlap_power.py (data_scout): that lane ALSO applied an explicit
# zone-tag purity retention (~0.65) on top of the floor.  Here purity lives in the projection floor
# (no double-count), so the FACE-VALUE stack z~3.1 is the optimistic corner; charging purity a second
# time (overlap_power convention) drops it to ~2.0 -- the two bracket the honest ~2-3sigma stack range.
_z_stack_purity = np.log1p(SIG["PURE-DELAY"]["can"]) * 0.65 / np.hypot(
    sln_fid*np.sqrt(1/(237*F_FIRST)+1/(237*F_ANC)), FLOOR["opt"])
print(f"\n   RECONCILE w/ overlap_power.py: MaNGA+SAMI(237) pure-delay = {achieved[('F3-cleaned 2.2%','MaNGA+SAMI stack')][1]:.2f} "
      f"(face) .. {_z_stack_purity:.2f} (if purity charged again) -> honest stack range ~2-3sigma, NOT a clean detection.")
assert 1.8 < _z_stack_purity < 2.6, "purity-charged stack must reproduce the committed ~2-2.5sigma exploratory hint"

# ---------------------------------------------------------------------------------------------
# 6.  BOTH FOOTINGS -- signal footing-invariance at fixed dimensionless depth.
# ---------------------------------------------------------------------------------------------
h(" (6) BOTH FOOTINGS -- signal footing-invariance at fixed dimensionless depth (a0 cancels)")
for rd in ("LOW-PASS", "PURE-DELAY"):
    dc = abs(SIG[rd]["alt"]-SIG[rd]["can"])/SIG[rd]["can"]
    print(f"   {rd:11s}: S_can={SIG[rd]['can']*100:.1f}%  S_alt={SIG[rd]['alt']*100:.1f}%  "
          f"footing spread {dc*100:.0f}%  (tau_mem*H_Lambda=2Z footing-free)")
    assert dc <= 0.16, "footing spread must be within ~15% (a0 cancels at fixed depth)"

# ---------------------------------------------------------------------------------------------
# 7.  VERDICT
# ---------------------------------------------------------------------------------------------
h(" (7) VERDICT -- per kernel reading, both ways, no averaging")
z_stack_pd_best = achieved[("F3-cleaned 2.2%", "MaNGA+SAMI stack")][1]
z_manga_pd_best = achieved[("F3-cleaned 2.2%", "MMU-MaNGA")][1]
z_target_pd_best= achieved[("F3-cleaned 2.2%", "clean target")][1]
print(f"""
  LOW-PASS reading (S ~ 1.3% canonical / 1.5% alt):  UNDETECTABLE AT ANY N.
    The signal sits BELOW even the most optimistic combined confound floor (~2.2%; the projection
    alias ALONE is ~1-2%).  Structural ceiling z_max = {zmax_lp_best:.2f} < 1 at the best floor: no galaxy
    count closes it.  A 3sigma detection would need the total floor beaten to <= {be3_lp*100:.2f}% --
    below the projection floor by itself.  On every real sample z_LP < {max(achieved[('F3-cleaned 2.2%', nm)][0] for nm,_ in samples):.2f}.  This is a
    genuine NO, not a shortfall of N.

  PURE-DELAY reading (S ~ 8-13%, fiducial 10.5%):  CONDITIONALLY DETECTABLE, floor-hostage.
    * At the FIDUCIAL ~5% floor (tidal residual not aggressively cleaned): ceiling z_max = {zmax_pd_fid:.2f}
      < 3 -> NO 3sigma at any N.  The tidal floor, not statistics, is the wall.
    * ONLY if the F3 outward-rising radial-profile separator drives the combined floor to ~2.2%
      does the ceiling clear 3sigma (z_max = {zmax_pd_best:.2f}).  Then 3sigma needs ~{Nz3_pd:.0f} diffuse tagged
      carriers PER ZONE (~{Nt3_pd:.0f} total, Rhee split).
    * 5sigma needs the TOP of the band (S~13%) + best precision + floor ~2.2%: ~{Nz5_pd:.0f} per zone,
      and collapses if the floor rises above ~2.5% or S sits mid-band.

  BREAK-EVEN (the whole detection lives or dies on the confound floor):
    floor must be <= S/3.  Low-pass: <= {be3_lp*100:.2f}% (impossible, below projection).
    Pure-delay: <= {np.log1p(SIG['PURE-DELAY']['can'])/3.0*100:.2f}% for 3sigma, <= {np.log1p(SIG['PURE-DELAY']['can'])/5.0*100:.2f}% for 5sigma.
    The per-galaxy sigma precision (3-8% IFU) is a WEAK lever: intrinsic relational scatter
    s_FJ~0.065 dex dominates, so tightening sigma 8%->0% cuts required N by <x1.6.  Buying
    precision does NOT rescue the low-pass reading.

  REAL-DATA MAP (best F3-cleaned 2.2% floor, pure-delay):
    MMU-MaNGA (77): z~{z_manga_pd_best:.1f}   MaNGA+SAMI (237): z~{z_stack_pd_best:.1f}   target (400): z~{z_target_pd_best:.1f}.
    All public samples are UNDERPOWERED for a clean pure-delay detection, and DEAD for low-pass
    at every sample.  A clean >=3sigma pure-delay probe needs BOTH (i) ~300-500 diffuse tagged
    carriers from a dedicated wide nearby-cluster dwarf-IFU survey (or ELT/HARMONI, ~2032) AND
    (ii) the tidal floor demonstrably beaten to ~2% by the F3 radial-profile separator on real data.

  HONEST HEADLINE:  UNDERPOWERED, and MORE than a count problem.  The discriminating POWER is
    theorem-grade vs the whole MG class; a DETECTION is possible only in the pure-delay (high)
    kernel reading AND a specifically clean, low-tidal sample with F3 working.  In the committed
    low-pass corner the signal is below the irreducible floor and no instrument detects it.
    MI-class-generic; does NOT test a0's value or s=-1; both footings identical at fixed depth.
""")
print(LINE)
print("two_zone_power.py complete -- exit 0")
print(LINE)
