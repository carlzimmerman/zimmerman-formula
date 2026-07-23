#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
sigma_spread_prereg_2026.py -- THE FROZEN PRE-REGISTRATION for the cluster-member
=================================================================================
external-field-effect (EFE) relational velocity-dispersion-spread test: the ONE
genuinely MODIFIED-GRAVITY-IMPOSSIBLE discriminator of the de Sitter-Unruh MODIFIED-
INERTIA framework (Zimmerman).  numpy-only, exit 0.  BOTH coefficient footings.
2026-07-23.

This file FREEZES the pre-registered analysis of the published theorem+methods paper
  real_research/papers/MI_SIGMA_SPREAD_2026.md   (Zenodo 21421896)
and is consistent with its D3 erratum.  It does NOT re-derive or relitigate the paper.
It ARMS the paper by pinning, before any data touch:
   (i)   the exact D(zone) estimator + the member-selection cuts + the target-cluster ranking;
   (ii)  the required-N vs per-galaxy-precision power curves for 3sigma AND 5sigma, computed
         SEPARATELY for the low-pass (~1.3%) and pure-delay (~8-13%) kernel readings, with the
         projection (1-2%) + tidal (2-8%) confound floors added IN QUADRATURE as irreducible,
         N-independent systematics;
   (iii) the best real existing dataset's (N, precision) plugged in -> does it reach 3sigma?;
   (iv)  the frozen GO/NO-GO per (target sample x kernel reading x floor corner);
   (v)   the PRE-REGISTRATION block: exact prediction, decision thresholds, honesty caveats.

The power engine (z_at_total, N_req_*, z_ceiling) is IDENTICAL to the committed
prep_2026/cluster_efe_channel/two_zone_power.py so every number reconciles; the target
ranking + selection cuts mirror prep_2026/cluster_efe_channel/arm_prereg.py.

SUPERSEDES the stale prep_2026/cluster_efe_channel/observable.py, which still carried the
RETRACTED dated pericentre sign-flip (deficit->excess, tau=0.45 Gyr).  CORRECTED, load-
bearing facts taken as GIVEN (paper Secs 2-5, not relitigated here):
  * tau_mem = 2c/a0 = 2Z/H_Lambda = 203 Gyr (canonical) / 168 Gyr (alt); 2Z=11.58 footing-free.
    tau_mem >> orbital/crossing times -> the pure-phase branch SATURATES (NO resonance); the
    spread is the small residual (hence the kernel-hostage smallness).
  * LEADING SIGN: first-infall pre-pericentre members run HOTTER (D>0), structural + timescale-
    free for any positive-averaging / pure-delay causal kernel (0/125 orbit-scan sign flips).
    Recent-infall / backsplash zones are timescale-hostage and NOT pre-registrable.
  * MAGNITUDE is KERNEL-HOSTAGE: the fixed-field ln(sigma_int/sigma_bary) first-infall-vs-ancient
    contrast = ~1.3% (canonical low-pass) / ~1.5% (alt) UP TO ~8-13% (pure-delay |K|=1 corner).
  * CONFOUND FLOORS (irreducible, NOT beaten by the theorem): projection ~1-2%, tidal ~2-8%
    (same-signed).  MG field sector = 0 at fixed TRUE field is the SOLE theorem-grade claim.
  * The signature is MI-CLASS-GENERIC (separates history-dependent inertia from MG; does NOT
    separate this framework from Milgrom 2503.07106).  Does NOT test a0's VALUE or the sign s=-1.

HONEST-BOTH-WAYS RULE (this repo penalizes a manufactured WIN and a manufactured DEFICIT
EQUALLY): every power number carries BOTH kernel readings; the low-pass corner is reported as
the honest central expectation (a NON-DETECTION); the pure-delay corner is firewalled as a
conditional hint that lives or dies on the confound floor.  UNDERPOWERED is a valid verdict.

Credit: Milgrom 1983 ApJ 270:365 (MG-virial universality) / 1999 PLA 253:273 Eq.9 (nu-kernel
wellhead, nu=sqrt(1+1/y)) / 2022 PRD 106:064060 (two-frequency MI EFE) / 2503.07106 (linear MI).
Scaffolding: Rhee+2017 ApJ 843:128 (PPS zones); Wolf+2010 MNRAS 406:1220 (beta-immune mass);
Abdullah+2020 ApJS 246:2 (GalWCat19); Rines+2013/2016 (HeCS); Owers+2017 MNRAS 468:1824 (SAMI);
Toloba+2014 (SMAKCED); Kourkchi+2012 (Coma dEs); Gannon+2022 (Perseus UDGs).
"""
import math
import numpy as np

LINE = "=" * 100
def h(t):
    print(); print(LINE); print(t); print(LINE)

# =====================================================================================
# 0.  FROZEN CONSTANTS / FOOTINGS / INPUTS  (all traceable to the paper or cited lit.)
# =====================================================================================
c    = 2.99792458e8
G    = 6.674e-11
Mpc  = 3.0856775814913673e22
kpc  = Mpc / 1e3
pc   = Mpc / 1e6
MSUN = 1.989e30
yr   = 3.1557e7
Gyr  = 1e9 * yr
km   = 1e3
H0   = 67.4e3 / Mpc
OmL  = 0.685
HL   = H0 * math.sqrt(OmL)
Z    = math.sqrt(32 * math.pi / 3.0)                 # 5.7890
A0_CAN = c * HL / Z                                  # 9.36e-11  (cH_Lambda/Z)  CANONICAL
A0_ALT = c * H0 / Z                                  # 1.13e-10  (cH0/Z)        ALTERNATE
assert abs(A0_CAN - 9.36e-11) < 1e-13 and abs(A0_ALT - 1.13e-10) < 1e-12
TAU_MEM_CAN = 2 * c / A0_CAN                         # 2Z/H_Lambda
TAU_MEM_ALT = 2 * c / A0_ALT
assert abs(TAU_MEM_CAN / Gyr - 203) < 3 and abs(TAU_MEM_ALT / Gyr - 168) < 3

# --- KERNEL-HOSTAGE SIGNAL (fixed-field first-infall - ancient MEASURED ln-contrast), BOTH
#     footings.  Paper Secs 4.2, 5.4.  a0 cancels at fixed dimensionless depth (can/alt = remap).
SIG = {
    "LOW-PASS":   {"can": 0.013, "alt": 0.015, "band": (0.013, 0.015),
                   "note": "decaying-memory corner; residence-time-limited; the honest baseline"},
    "PURE-DELAY": {"can": 0.105, "alt": 0.105, "band": (0.080, 0.130),
                   "note": "|K|=1 group-delay corner; bounded transient survives; firewalled hint"},
}

# --- per-galaxy ln(sigma_int/sigma_bary) scatter = hypot(intrinsic, measurement).
#     s_FJ : IRREDUCIBLE astrophysical scatter of the Wolf-normalized relation, 0.05-0.08 dex.
#     e_sig: per-galaxy internal-sigma IFU precision (fractional); the lever the power curve probes.
S_FJ_LN   = {"opt": 0.115, "fid": 0.150, "pes": 0.184}   # 0.050 / 0.065 / 0.080 dex -> ln
E_SIG_IFU = {"opt": 0.03,  "fid": 0.05,  "pes": 0.08}
def s_ln(s_fj, e_sig):
    return float(np.hypot(s_fj, e_sig))
SLN_FID = s_ln(S_FJ_LN["fid"], E_SIG_IFU["fid"])         # 0.158

# --- IRREDUCIBLE, N-INDEPENDENT systematic FLOOR on the contrast (quadrature proj + tidal).
#     projection alias ~1-2% (Sec 4.4; ALREADY encodes finite Rhee zone-tag purity p=0.5-0.9);
#     tidal/environmental same-signed ~2-8% ("opt" = F3 outward-profile separator working well).
PROJ  = {"opt": 0.010, "fid": 0.015, "pes": 0.020}
TIDAL = {"opt": 0.020, "fid": 0.050, "pes": 0.080}
FLOOR = {k: float(np.hypot(PROJ[k], TIDAL[k])) for k in PROJ}   # 0.0224 / 0.0522 / 0.0825

# --- Rhee+2017 zone fractions of the tagged carrier pool (first-infall A, ancient E); the
#     residual ~0.17 (recent-infall/backsplash) is DROPPED (timescale-hostage, not pre-registrable).
F_FIRST, F_ANC = 0.33, 0.50

# --- member-selection carrier cut: a_in = sigma_int^2 / r_half < 0.5 a0.  Fraction of an existing
#     resolved-sigma dwarf sample that survives it (diffuse deep-MOND carriers):
CARRIER_FRAC = 0.60

h(" FROZEN PRE-REGISTRATION -- MI cluster-member EFE sigma-spread discriminator (MI-class vs MG)")
print(f"  Z = {Z:.4f}   a0(can) = {A0_CAN:.3e}   a0(alt) = {A0_ALT:.3e}  m/s^2")
print(f"  tau_mem = 2Z/H_Lambda = {TAU_MEM_CAN/Gyr:.0f} Gyr (can) / {TAU_MEM_ALT/Gyr:.0f} Gyr (alt)   [2Z = {2*Z:.2f}, footing-free]")
print(f"  per-galaxy s_ln = hypot(s_FJ, e_sig); fiducial = hypot({S_FJ_LN['fid']}, {E_SIG_IFU['fid']}) = {SLN_FID:.3f}")
print(f"  systematic floor (quadrature proj+tidal): opt {FLOOR['opt']*100:.1f}%  fid {FLOOR['fid']*100:.1f}%  pes {FLOOR['pes']*100:.1f}%")
print( "  GIVEN (paper): first-infall HOTTER (D>0); S = 1.3% (low-pass) -> 8-13% (pure-delay); MG=0 sole theorem.")

# =====================================================================================
# 1.  THE ESTIMATOR + SELECTION CUTS + ZONE TAGGING  (frozen definitions)
# =====================================================================================
h(" (1) THE FROZEN OBSERVABLE  D(zone)  --  estimator, selection cuts, zone tagging")
print(r"""  ESTIMATOR (per deprojected external-field bin b; width <= 0.3 dex; inverse-variance weighted):
      L_i        = ln( sigma_int,i / sigma_bary,i )                       (the log EFE boost per member)
      sigma_bary = sqrt( G * M_bary / (3 * r_half) )                      (beta-IMMUNE Wolf+2010)
      w_i        = 1 / Var[L_i],  Var[L_i] ~ (e_i/sigma_int,i)^2 + (0.5 dln M_bary,i)^2
      D_hat(b)   = <L>_{first-infall, b}  -  <L>_{ancient, b}             (difference ALONG history axis)
      sig_D(b)^2 = sig_stat(b)^2  (+)  s_sys^2  ,   s_sys^2 = s_proj^2 + s_tidal^2   (quadrature)

  SELECTION CUT (frozen; only diffuse deep-MOND members carry the signal):
      a_in = sigma_int^2 / r_half  <  0.5 * a0    (equivalently mean dynamical Sigma < ~a0/(2piG),
      mu_0 >~ 24 mag/arcsec^2).  Carriers: UDG (sigma~15-25), dSph/LSB dE (sigma~20-45 km/s).
      HSB / L* members have nu -> 1 (a_in/a0 >~ 3): NO boost to memory-modulate -> SIGNAL-FREE.
      (The survey-BRIGHT members are exactly the adiabatically DEAD ones -- the power wall, Sec 6.)

  ZONE TAGGING (frozen; Rhee+2017 projected phase space X=R_proj/R200, Y=|v_los-v_cl|/sigma_cl):
      ANCIENT (reference)  : X < 0.5  & Y < 1.5    (virialized core)
      FIRST-INFALL (signal): X in 1.0-2.0 & Y < 2.0 (pre-first-pericentre outskirts)
      Recent-infall / backsplash: DROPPED (timescale-hostage at tau_mem=203 Gyr; not pre-registrable).

  THE FIXED-FIELD TRICK (why D is a common-mode difference, not a radial trend):
      D is NOT computed zone-vs-zone across radius -- that radial EFE gradient is the SHARED (MG=MI)
      killer common mode.  Instead: deproject each member to a_ext = G*M(<r)/r^2 from the CAUSTIC mass
      profile (GalWCat19 / HeCS), BIN by a_ext (<=0.3 dex), and difference first-infall vs ancient
      WITHIN each bin (both histories coexist at a fixed true radius).  Signal peaks at the transition
      shell a_ext ~ 0.3-1 a0 (~R500-R200): the F3 outward-rising radial-profile separator.""")

# a_in carrier locus + the LSB/HSB critical surface density, both footings (design feasibility)
print("\n  Critical surface density (LSB/HSB divide, a_in ~ a0):")
for flab, a0 in (("CANONICAL", A0_CAN), ("ALTERNATE", A0_ALT)):
    Sig_2pi = a0 / (2 * math.pi * G) / (MSUN / pc**2)
    Sig_G   = a0 / G / (MSUN / pc**2)
    print(f"    [{flab}]  a0/(2piG) = {Sig_2pi:5.0f} Msun/pc^2    a0/G = {Sig_G:5.0f} Msun/pc^2")
print("  Carrier locus (a_in = 0.3 a0, canonical): sigma ~ 29 km/s at r_half=1 kpc, ~51 km/s at 3 kpc.")
# transition shell per cluster mass
print("  Transition shell R(a_ex=a0)=sqrt(GM/a0) [F3 peak]:", end=" ")
print(", ".join(f"{M:.0e}->{math.sqrt(G*M*MSUN/A0_CAN)/Mpc:.2f}Mpc" for M in (7e13, 2e14, 4e14, 1.3e15)))

# =====================================================================================
# 2.  TARGET-CLUSTER RANKING  (carrier reach x low-tidal x phase-space coverage)
# =====================================================================================
h(" (2) TARGET-CLUSTER RANKING  --  score = carrier_reach x low-tidal x phase-space coverage")
# name       dist_Mpc  M200     N_car  tidal  PPS   anchor(cited)
CLUSTERS = [
  ("Virgo",   16.5, 3.0e14, 39, 0.35, 0.85, "SMAKCED 39 dEs (Toloba+2014); nearest rich cluster -> only place sigma~20-30 dwarfs resolve; NGVS PPS"),
  ("Fornax",  20.0, 7.0e13, 33, 0.90, 0.60, "SAMI-Fornax + Fornax3D 33; relaxed cool-core -> LOWEST tidal floor; FDS ~600 membership"),
  ("Coma",   100.0, 1.3e15, 41, 0.60, 1.00, "Kourkchi+2012 41 dEs (Keck/DEIMOS); richest caustic/Rhee scaffolding + MaNGA-served"),
  ("Hydra I", 50.0, 2.0e14, 15, 0.85, 0.55, "LEWIS MUSE UDG/LSB ~15; relaxed; resolved-sigma dwarf sample thin"),
  ("Perseus", 75.0, 8.0e14,  5, 0.55, 0.70, "Gannon+2022 5 UDGs (KCWI); rich but distance-walled; sloshing cool-core"),
]
def score_cluster(d, Ncar, tidal, ps):
    prox = min(1.0, 20.0 / d)                # carrier reachability (line resolved above LSF floor), cap 1
    car  = (Ncar / 45.0) ** 0.7 * prox       # 45 ~ richest existing resolved-sigma dwarf sample scale
    return car * tidal * ps, prox, car
print(f"  {'cluster':9s} {'d(Mpc)':>6s} {'M200':>8s} {'N_car':>6s} {'prox':>5s} {'tidal':>6s} {'PPS':>5s} {'SCORE':>7s}")
scored = []
for name, d, M, Ncar, tidal, ps, anch in CLUSTERS:
    sc, prox, car = score_cluster(d, Ncar, tidal, ps)
    scored.append((sc, name, anch))
    print(f"  {name:9s} {d:6.1f} {M:8.1e} {Ncar:6d} {prox:5.2f} {tidal:6.2f} {ps:5.2f} {sc:7.3f}")
scored.sort(reverse=True)
print("\n  RANKING (frozen):")
for rank, (sc, name, anch) in enumerate(scored, 1):
    print(f"   {rank}. {name:9s} score={sc:.3f}   [{anch}]")
# assert the frozen ordering
assert [s[1] for s in scored] == ["Fornax", "Virgo", "Coma", "Hydra I", "Perseus"], "frozen cluster ranking changed"
assert abs(scored[0][0] - 0.435) < 0.01 and abs(scored[1][0] - 0.269) < 0.01, "top-two scores drifted"
print("""
  READ (honest, both-ways -- the top two are a TENSION, not a clean winner):
    * FORNAX tops the composite score: relaxed cool-core = LOWEST tidal floor + a dedicated resolved-
      dwarf-sigma survey -- the clean LOW-TIDAL control (best place to let F3 breathe).
    * VIRGO is the CARRIER reservoir: nearest rich cluster, the only place sigma~20-30 dwarfs resolve.
      Penalty = dynamically young -> high tidal floor + biased spherical caustic.
    * The ordering flips Fornax<->Virgo depending on how heavily the tidal floor is weighted vs count.
  FROZEN PRIMARY SAMPLE = the VIRGO (carriers+signal) + FORNAX (low-tidal control) PAIR;
  COMA for caustic/PPS scaffolding + a MaNGA cross-check; Hydra I + Perseus as stack fodder.""")

# =====================================================================================
# 3.  POWER ENGINE  (identical to two_zone_power.py so numbers reconcile)
# =====================================================================================
def z_ceiling(S, fl):                          # N -> infinity structural ceiling  z_max = ln(1+S)/floor
    return math.log1p(S) / fl
def N_req_total(S, sln, fl, ztar):             # TOTAL tagged N (Rhee split) for ztar; None if ceiling fails
    lead = math.log1p(S)
    if lead <= ztar * fl:
        return None
    se_max = math.sqrt((lead / ztar) ** 2 - fl ** 2)
    return (1.0 / F_FIRST + 1.0 / F_ANC) * sln ** 2 / se_max ** 2
def z_at_total(Ntot, S, sln, fl):              # achieved z at a real Rhee-split carrier count
    N1, N2 = Ntot * F_FIRST, Ntot * F_ANC
    se_stat = sln * math.sqrt(1.0 / N1 + 1.0 / N2)
    return math.log1p(S) / math.hypot(se_stat, fl)
def fmtN(x):
    return "   NO N" if x is None else f"{x:7.0f}"

# =====================================================================================
# 3a.  REQUIRED-N vs PER-GALAXY-PRECISION POWER CURVES  (3sigma AND 5sigma, per reading)
# =====================================================================================
h(" (3) REQUIRED-N vs PER-GALAXY sigma PRECISION  --  3sigma AND 5sigma, per kernel reading")
print("   TOTAL tagged carriers (Rhee split) needed at the F3-cleaned floor (2.2%); 'NO N' = ceiling")
print("   fails, no count works.  Signal at FACE VALUE (measured post-tag contrast); purity in the floor.\n")
for rd in ("LOW-PASS", "PURE-DELAY"):
    S_can = SIG[rd]["can"]; S_top = SIG[rd]["band"][1]
    print(f"   --- {rd} reading (S = {S_can*100:.1f}% canonical; band top {S_top*100:.0f}%) ---")
    print(f"   {'e_sig(IFU)':>10s} {'s_ln':>7s} | {'N(3s|S_can)':>12s} {'N(5s|S_can)':>12s} {'N(5s|S_top)':>12s}")
    for e in (0.0, 0.03, 0.05, 0.08, 0.12):
        sln = s_ln(S_FJ_LN["fid"], e)
        n3  = N_req_total(S_can, sln, FLOOR["opt"], 3.0)
        n5  = N_req_total(S_can, sln, FLOOR["opt"], 5.0)
        n5t = N_req_total(S_top, s_ln(S_FJ_LN["opt"], e), FLOOR["opt"], 5.0)
        print(f"   {e*100:8.0f}%  {sln:7.3f} | {fmtN(n3):>12s} {fmtN(n5):>12s} {fmtN(n5t):>12s}")
    print()
# structural ceilings, load-bearing
zmax_lp_best = z_ceiling(SIG["LOW-PASS"]["can"],   FLOOR["opt"])
zmax_pd_fid  = z_ceiling(SIG["PURE-DELAY"]["can"], FLOOR["fid"])
zmax_pd_best = z_ceiling(SIG["PURE-DELAY"]["can"], FLOOR["opt"])
be3_lp       = math.log1p(SIG["LOW-PASS"]["can"]) / 3.0
n3_pd_fid_e5 = N_req_total(SIG["PURE-DELAY"]["can"], SLN_FID, FLOOR["opt"], 3.0)
print(f"   CEILINGS (z_max = S/floor, N->inf):  LOW-PASS best-floor = {zmax_lp_best:.2f}  (< 1: undetectable at ANY N)")
print(f"                                        PURE-DELAY fid-floor = {zmax_pd_fid:.2f}  (< 3: no 3sigma at any N)")
print(f"                                        PURE-DELAY best-floor= {zmax_pd_best:.2f}  (clears 3sigma; 5sigma only at band top)")
print(f"   PURE-DELAY 3sigma @ best floor, fiducial precision: ~{n3_pd_fid_e5:.0f} total tagged carriers (Rhee split).")
print(f"   Precision is a WEAK lever: intrinsic s_FJ dominates; e_sig 8%->0% cuts N by < x1.6.")

# --- SELF-CHECK ASSERTS (frozen honesty gates) ---
assert zmax_lp_best < 1.0, "LOW-PASS 1.3% must sit below the most optimistic floor => undetectable at any N"
assert be3_lp < PROJ["opt"], "LOW-PASS 3sigma break-even floor must be below the projection floor alone => impossible"
assert N_req_total(SIG["LOW-PASS"]["can"], SLN_FID, FLOOR["opt"], 3.0) is None, "LOW-PASS must return NO N at 3sigma"
assert zmax_pd_fid < 3.0, "PURE-DELAY at the fiducial floor must FAIL the 3sigma ceiling"
assert zmax_pd_best > 3.0, "PURE-DELAY at the F3-cleaned floor must CLEAR the 3sigma ceiling"
assert N_req_total(SIG["PURE-DELAY"]["can"], SLN_FID, FLOOR["opt"], 5.0) is None, \
    "PURE-DELAY 5sigma at S=10.5% must be impossible at any N (ceiling 4.46 < 5)"
assert n3_pd_fid_e5 is not None and 150 < n3_pd_fid_e5 < 300, "PURE-DELAY 3sigma N should land in the exploratory 150-300 range"

# =====================================================================================
# 4.  BEST REAL EXISTING DATASET plugged in -- does it reach 3sigma?
# =====================================================================================
h(" (4) BEST REAL EXISTING DATASET  --  public MaNGA+SAMI overlap stack, N~237, e_sig~5%")
N_REAL, E_REAL = 237, 0.05          # data_scout/overlap_power.py carrier census; fiducial IFU precision
sln_real = s_ln(S_FJ_LN["fid"], E_REAL)
print(f"   (data_scout: MMU-MaNGA alone ~40-77 carriers; +SAMI stack ~135-237; clean target 300-500.)")
print(f"   {'reading':11s} {'floor':>14s} | {'achieved z':>11s}   call")
real = {}
for rd in ("LOW-PASS", "PURE-DELAY"):
    for flab, fl in (("F3-cleaned 2.2%", FLOOR["opt"]), ("fiducial 5.2%", FLOOR["fid"])):
        z = z_at_total(N_REAL, SIG[rd]["can"], sln_real, fl)
        real[(rd, flab)] = z
        call = "GO (>=3s)" if z >= 3.0 else ("hint" if z >= 2.0 else "NO-GO (<2s)")
        print(f"   {rd:11s} {flab:>14s} | {z:11.2f}   {call}")
# RECONCILE with the paper's Sec 6.2 table (~2.0sigma optimistic): that lane / the committed
# data_scout overlap_power.py charge zone-tag purity (~0.65) a SECOND time on top of the floor.
# Here purity lives in the projection floor (no double-count), so the FACE-VALUE stack z~3.1 is the
# optimistic bracket; charging purity again drops it to ~2.0 -- the two bracket the honest ~2-3sigma
# stack range.  The MaNGA+SAMI "GO" cell is therefore a FIREWALLED ~2-3sigma HINT, not a clean detection.
z_stack_purity = math.log1p(SIG["PURE-DELAY"]["can"]) * 0.65 / math.hypot(
    sln_real * math.sqrt(1.0 / (N_REAL * F_FIRST) + 1.0 / (N_REAL * F_ANC)), FLOOR["opt"])
print(f"""
   READ: the ONLY cell that reaches 3sigma is PURE-DELAY x F3-cleaned-floor, face-value z ~ {real[('PURE-DELAY','F3-cleaned 2.2%')]:.1f} --
   a DOUBLY-optimistic corner (the kernel must sit at |K|=1 AND the F3 separator must drive the tidal
   floor to ~2%).  RECONCILE w/ paper Sec 6.2 (~2.0sigma): charging zone-tag purity a 2nd time drops
   this to z ~ {z_stack_purity:.1f}, so the honest MaNGA+SAMI range is ~2-3sigma -- a FIREWALLED HINT, not a clean
   detection.  In the honest LOW-PASS central reading the best real dataset gives z ~ {real[('LOW-PASS','F3-cleaned 2.2%')]:.2f} (dead), and
   PURE-DELAY at the un-cleaned fiducial floor gives z ~ {real[('PURE-DELAY','fiducial 5.2%')]:.2f} (dead).  Best existing data does NOT
   reach a CLEAN 3sigma in any reading.""")
assert real[("LOW-PASS", "F3-cleaned 2.2%")] < 1.0, "best real dataset must be dead in the low-pass reading"
assert real[("PURE-DELAY", "fiducial 5.2%")] < 3.0, "best real dataset must miss 3sigma at the un-cleaned floor"
assert 1.8 < z_stack_purity < 2.6, "purity-charged stack must reproduce the paper's ~2-2.5sigma firewalled hint"

# =====================================================================================
# 5.  FROZEN GO/NO-GO  per (target sample x kernel reading x floor corner)
# =====================================================================================
h(" (5) FROZEN GO / NO-GO  --  per (target sample x kernel reading x floor corner)")
print("   GO := achieved z >= 3.0.  Samples tie to clusters/surveys via the data_scout carrier census.\n")
SAMPLES = [
    ("MMU-MaNGA (public)",        77,  "Coma/other MaNGA-served clusters"),
    ("MaNGA + SAMI stack",       237,  "SAMI clusters + MaNGA overlap"),
    ("Virgo+Fornax pilot",        43,  "primary pair, best low-tidal control"),
    ("clean-exploratory target", 400,  "dedicated pointing, 4-5 nearby clusters"),
    ("dedicated dwarf-IFU / ELT",2000, "wide nearby-cluster survey or ELT/HARMONI ~2032"),
]
corners = [("LOW-PASS", FLOOR["opt"], "S=1.3%, floor 2.2%"),
           ("PURE-DELAY", FLOOR["fid"], "S=10.5%, floor 5.2% (un-cleaned)"),
           ("PURE-DELAY", FLOOR["opt"], "S=10.5%, floor 2.2% (F3-cleaned)")]
print(f"   {'sample':26s} {'N':>5s} | " + " ".join(f"{c[2]:>28s}" for c in corners))
go_matrix = {}
for sname, N, note in SAMPLES:
    cells = []
    for rd, fl, _ in corners:
        z = z_at_total(N, SIG[rd]["can"], SLN_FID, fl)
        go = z >= 3.0
        go_matrix[(sname, rd, fl)] = (z, go)
        cells.append(f"{'GO ' if go else 'no '}z={z:4.2f}")
    print(f"   {sname:26s} {N:5d} | " + " ".join(f"{cc:>28s}" for cc in cells))
print("""
   Every LOW-PASS cell is NO-GO at any N (ceiling < 1).  Every PURE-DELAY cell at the un-cleaned
   fiducial floor is NO-GO at any N (ceiling < 3).  GO appears ONLY in the PURE-DELAY x F3-cleaned
   column, and only for N >~ 200 (MaNGA+SAMI and above) -- the conditioned, firewalled corner.""")
# frozen GO/NO-GO asserts
assert all(not go_matrix[(s, "LOW-PASS", FLOOR["opt"])][1] for s, *_ in SAMPLES), "LOW-PASS must be NO-GO for every sample"
assert all(not go_matrix[(s, "PURE-DELAY", FLOOR["fid"])][1] for s, *_ in SAMPLES), "PURE-DELAY fid-floor must be NO-GO for every sample"
assert not go_matrix[("MMU-MaNGA (public)", "PURE-DELAY", FLOOR["opt"])][1], "public MMU-MaNGA must be NO-GO even pure-delay/F3-cleaned"
assert go_matrix[("MaNGA + SAMI stack", "PURE-DELAY", FLOOR["opt"])][1], "MaNGA+SAMI stack must be GO in the pure-delay/F3-cleaned corner"
# the threshold-N property: pure-delay F3-cleaned crosses z=3 between N=150 and N=300
assert z_at_total(150, SIG["PURE-DELAY"]["can"], SLN_FID, FLOOR["opt"]) < 3.0 \
    < z_at_total(300, SIG["PURE-DELAY"]["can"], SLN_FID, FLOOR["opt"]), \
    "pure-delay F3-cleaned must clear 3sigma only above the printed threshold N (~200)"

# =====================================================================================
# 6.  BOTH FOOTINGS -- signal footing-invariance at fixed dimensionless depth
# =====================================================================================
h(" (6) BOTH FOOTINGS  --  signal footing-invariance at fixed dimensionless depth (a0 cancels)")
for rd in ("LOW-PASS", "PURE-DELAY"):
    dc = abs(SIG[rd]["alt"] - SIG[rd]["can"]) / SIG[rd]["can"]
    print(f"   {rd:11s}: S_can={SIG[rd]['can']*100:.1f}%  S_alt={SIG[rd]['alt']*100:.1f}%  footing spread {dc*100:.0f}%")
    assert dc <= 0.16, "footing spread must be within ~15% (a0 cancels at fixed depth; 2Z footing-free)"

# =====================================================================================
# 7.  THE PRE-REGISTRATION BLOCK  (frozen prediction + thresholds + caveats)
# =====================================================================================
h(" (7) PRE-REGISTRATION  --  frozen prediction, decision thresholds, honesty caveats")
z_stack_pd = go_matrix[("MaNGA + SAMI stack", "PURE-DELAY", FLOOR["opt"])][0]
z_manga_pd = go_matrix[("MMU-MaNGA (public)", "PURE-DELAY", FLOOR["opt"])][0]
print(f"""
  PREDICTION (frozen, framework-specific numbers; the discriminating power is MI-class-generic):
    * TIER (i) EXISTENCE -- at fixed cluster-centric TRUE external field, a modified-inertia universe
      shows a NONZERO internal-sigma spread correlated with infall history.  In the FIELD SECTOR of
      any sourced-field-WEP gravity (QUMOND/AQUAL/AeST/TeVeS/f(R)/local-mod-g) this fixed-field
      history spread is EXACTLY ZERO -- theorem-grade, MG-impossible.
    * TIER (ii) LEADING SIGN -- FIRST-INFALL pre-pericentre members run HOTTER (larger internal sigma)
      than matched long-resident members:  D(first-infall) > 0.  Structural + timescale-free for any
      positive-averaging / pure-delay causal kernel (0/125 orbit-scan sign flips).
    * MAGNITUDE (kernel-hostage band, both footings ~identical at fixed depth):
        D(first-infall) = +1.3% (canonical low-pass) / +1.5% (alt)   ... up to  +8..13% (pure-delay |K|=1).
      The instantaneous 6-13% EFE boost is a current-configuration quantity MG PARTLY SHARES -- NOT the
      discriminant; the discriminant is the fixed-field history RESIDUAL D(zone) above.

  DECISION THRESHOLDS (frozen, pre-data):
    * SUPPORT   := D_hat > 0 (first-infall hotter) AND the F3 profile RISES outward peaking at the
                   transition shell a_ext~0.3-1 a0 AND baryon-blind (F4) -- jointly, at adequate power.
    * FALSIFY   := D_hat < 0 at >= 3sigma (first-infall COOLER) OR a null at adequate power (falsifies
                   Tier ii).  A coherent pre-pericentre DEFICIT is the FALSIFIER (inverts retracted D3).
    * MG-IMPOSSIBLE content := any nonzero fixed-TRUE-field history contrast (theorem d/dy=0 for the whole
                   MG class).  The OBSERVABLE existence claim is confound-contingent on F3 holding.
    * GO := achieved z >= 3sigma.  Per (5): GO ONLY in PURE-DELAY x F3-cleaned-floor x N >~ 200.

  HONEST VERDICT (both-ways, no averaging):
    * LOW-PASS reading (S~1.3-1.5%, the committed baseline): UNDETECTABLE AT ANY N.  z_max = {zmax_lp_best:.2f} < 1
      at the best floor; the signal sits BELOW even the projection alias (~1-2%).  A genuine NO, not a
      shortfall of N.  This is the HONEST CENTRAL EXPECTATION: a NON-DETECTION.
    * PURE-DELAY reading (S~8-13%): CONDITIONALLY detectable, floor-hostage.  At the fiducial ~5% floor
      z_max = {zmax_pd_fid:.2f} < 3 (NO 3sigma at any N).  ONLY if F3 drives the floor to ~2.2% does 3sigma open,
      needing ~{n3_pd_fid_e5:.0f} tagged carriers; 5sigma needs the TOP of the band (S~13%) + best everything.
      Best real data (MaNGA+SAMI, N=237): face z ~ {z_stack_pd:.1f}, purity-charged ~ {z_stack_purity:.1f} -> honest ~2-3sigma
      FIREWALLED HINT, not a clean detection; public MMU-MaNGA (77): z ~ {z_manga_pd:.1f} (NO-GO).

  SINGLE MOST-REALISTIC TARGET:  underpowered on existing data.  A clean >= 3sigma probe needs a
    DEDICATED wide nearby-cluster dwarf-IFU survey (M* floor to logM~8, reliable stellar sigma well
    below 45 km/s, ~300-500 diffuse tagged carriers) OR ELT/HARMONI (~2032) reaching sigma~20 km/s --
    AND the tidal floor demonstrably beaten to ~2% by the F3 radial-profile separator on real data.

  HONESTY CAVEATS (frozen, load-bearing):
    * KERNEL-HOSTAGE: the magnitude is a band (1.3% low-pass -> 8-13% pure-delay), genuinely uncomputed
      WITHIN the committed E10 memory; the low-pass corner is NOT presented as 'the answer'.
    * CONFOUND-CONTINGENT: MG=0 is a theorem only in the field sector at fixed TRUE field; same-signed
      non-equilibrium dynamics / tidal shocking / projection produce fixed-field spreads in Newton+DM
      and MG alike, separated by DESIGN (F3 outward profile + F2 sign), not by the theorem.
    * MI-CLASS-GENERIC: separates history-dependent inertia from MG; does NOT separate this framework
      from Milgrom's linear no-EFE MI (2503.07106), which also spreads.
    * DOES NOT TEST a0's VALUE (the spread is a0-value-blind at fixed depth) NOR the sign s=-1 (both
      postulates; the leading sign RIDES on s=-1; s=+1 reverses it).
    * BOTH FOOTINGS carried; a0 cancels at fixed dimensionless depth; tau_mem*H_Lambda = 2Z = 11.58
      footing-free.  No claim of proof for the framework; no 'theory closed'.
""")
print(LINE)
print("sigma_spread_prereg_2026.py -- FROZEN pre-registration ARMED.  Exit 0.")
print("Honest verdict: UNDERPOWERED.  Low-pass corner = non-detection at any N; pure-delay corner a")
print("firewalled hint only with F3-cleaned floor + N>~200; clean detection gated on a dedicated")
print("dwarf-IFU survey or ELT/HARMONI (~2032).  Design/feasibility, not a confrontation.")
print(LINE)
