#!/usr/bin/env python3
r"""
arm_prereg.py -- ARMING the pre-registered cluster-member EFE sigma-spread test.
================================================================================
prep_2026/cluster_efe_channel/ , 2026-07-23.  Exit 0.  numpy/math only.  BOTH footings.

Framework: de Sitter-Unruh MODIFIED INERTIA (Zimmerman).  nu(y)=sqrt(1+1/y),
y=g_bar/a0, a0=cH_Lambda/Z, Z=sqrt(32pi/3).  Milgrom 1983/1999 (PLA 253:273)
nu-kernel wellhead credit; distinctive content = cH_Lambda/Z coefficient + the
time-nonlocal MI completion K(Box_u), tau_mem = 2Z/H_Lambda = 203/168 Gyr.

THIS SCRIPT ARMS the OBSERVABLE + SELECTION for the published theorem+methods paper
  real_research/papers/MI_SIGMA_SPREAD_2026.md   (Zenodo 21421896).
It is CONSISTENT WITH the paper and the concurrent D3 erratum, and it SUPERSEDES the
sign convention hard-coded in this directory's older observable.py/predict.py
(which still carried the RETRACTED dated pericentre sign-flip + tau=0.45 Gyr).
CORRECTED, load-bearing facts taken as GIVEN from the paper (not relitigated here):
  * tau_mem = 2Z/H_Lambda = 203 Gyr (canonical) / 168 Gyr (alt), NOT 0.45 Gyr.
  * LEADING SIGN: first-infall pre-pericentre members run HOTTER (D>0), structural
    + timescale-free for any positive-averaging/pure-delay kernel (0/125 sign flips).
    The recent-infall / backsplash zones are timescale-hostage and NOT pre-registrable.
  * MAGNITUDE is KERNEL-HOSTAGE: fixed-field ln(sigma_int/sigma_bary) first-infall-vs-
    ancient contrast = ~1.3% (canonical low-pass) / ~1.5% (alt) UP TO ~8-13% (pure-delay).
  * CONFOUND FLOORS (irreducible systematics, NOT beaten by the theorem): projection
    ~1-2% (residual after Rhee zone deprojection), tidal ~2-8% (same-signed).
  * MG field sector = 0 at fixed TRUE field is the SOLE theorem-grade claim.
  * a0 VALUE and s=-1 are POSTULATES; test is a0-value-blind at fixed depth; sign rides s=-1.

MY LANE (verbatim): OBSERVABLE + SELECTION DESIGN --
  (a) TARGET CLUSTERS ranked by  N(resolved internal sigma carriers) x (low tidal env)
      x (Rhee-style phase-space coverage).   Candidates: Coma, Virgo, Fornax, Hydra I, Perseus.
  (b) MEMBER SELECTION: the internal-acceleration cut a_in/a0 that isolates diffuse low-y
      carriers; WHY high-surface-brightness members are signal-free.
  (c) ZONE TAGGING: first-infall vs ancient zones in projected phase space (R/R200 vs
      |dv|/sigma_cl) per Rhee+2017, and the fixed deprojected external-field bin.
  (d) The EXACT estimator D(zone) with its inputs + a both-ways detectability calc that
      carries the FULL kernel-hostage band (1.3% -> 13%) AND the confound floors.

HONEST-BOTH-WAYS RULE (this repo penalizes a manufactured win and a manufactured deficit
EQUALLY): detectability is reported SEPARATELY for the low-pass (~1.3%) and pure-delay
(~8-13%) readings; the confound floor is carried as an irreducible systematic; the honest
central outcome is a NON-DETECTION at the low-pass corner and a firewalled hint only in
the pure-delay corner on a clean low-tidal sample.
"""
import math
import numpy as np

# ============================================================ constants / footings
c    = 2.99792458e8
G    = 6.674e-11
Mpc  = 3.0856775814913673e22
kpc  = Mpc/1e3
pc   = Mpc/1e6
MSUN = 1.989e30
yr   = 3.1557e7
Gyr  = 1e9*yr
km   = 1e3
H0   = 67.4e3/Mpc
OmL  = 0.685
HL   = H0*math.sqrt(OmL)
Z    = math.sqrt(32*math.pi/3.0)                 # 5.7890
A0_CAN = c*HL/Z                                  # 9.36e-11  (cH_Lambda/Z)  CANONICAL
A0_ALT = c*H0/Z                                  # 1.13e-10  (cH0/Z)        ALTERNATE
assert abs(A0_CAN-9.36e-11) < 1e-13 and abs(A0_ALT-1.13e-10) < 1e-12
FOOTINGS = [("CANONICAL 9.36e-11", A0_CAN), ("ALTERNATE 1.13e-10", A0_ALT)]
TAU_MEM_CAN = 2*c/A0_CAN                          # 2Z/H_Lambda
TAU_MEM_ALT = 2*c/A0_ALT
assert abs(TAU_MEM_CAN/Gyr - 203) < 3 and abs(TAU_MEM_ALT/Gyr - 168) < 3

def hr(t=""):
    print("="*100);
    if t: print(" "+t); print("="*100)

hr("ARMING the cluster-member EFE sigma-spread pre-registration (MI-class vs MG)")
print(f"  Z={Z:.4f}  a0_can={A0_CAN:.3e}  a0_alt={A0_ALT:.3e} m/s^2")
print(f"  tau_mem = 2Z/H_Lambda = {TAU_MEM_CAN/Gyr:.0f} Gyr (can) / {TAU_MEM_ALT/Gyr:.0f} Gyr (alt)  [footing-free 2Z=11.58]")
print( "  GIVEN (paper): first-infall HOTTER (D>0); kernel-hostage 1.3% (low-pass) -> 8-13% (pure-delay);")
print( "  floors: projection ~1-2%, tidal ~2-8%; MG=0 at fixed true field the sole theorem.")

# =========================================================================================
# (b) MEMBER SELECTION -- the internal-acceleration cut that isolates the carriers
# =========================================================================================
hr("(b) MEMBER SELECTION -- internal-acceleration cut a_in/a0 (only diffuse low-y carry signal)")
# The framework nu applied to the EFE-loaded internal field.  The signal (a relational
# sigma spread) requires the member to be INTERNALLY deep in the modified regime, x_in=a_in/a0<~0.5.
# a_in = sigma_int^2 / r_half  (internal dynamical acceleration).  This maps to an observable
# central-surface-density / surface-brightness cut via a_in ~ 2*pi*G*Sigma_dyn.
def a_in(sigma, r_half):            # internal acceleration
    return sigma*sigma/r_half
def sigma_boost(x_in, x_ex):        # framework nu on the EFE-loaded field, A=(a_in+a_ex)
    A = x_in + x_ex                 # in units of a0 (theta absorbed into x_ex here for the depth demo)
    return math.sqrt(math.sqrt(A*A + A)/A)     # sqrt(g_obs/g_bar) at fixed radius

# critical surface densities (both footings): the LSB/HSB divide sits at a_in ~ a0.
for flabel, a0 in FOOTINGS:
    Sig_M   = a0/G          / (MSUN/pc**2)     # a0/G     ("MOND critical", full)
    Sig_2pi = a0/(2*math.pi*G) / (MSUN/pc**2)  # a0/(2piG) (Milgrom's Sigma_dagger ~ the mean-density divide)
    print(f"  [{flabel}]  Sigma(a_in=a0): a0/G={Sig_M:6.0f} Msun/pc^2   a0/(2piG)={Sig_2pi:5.0f} Msun/pc^2  (the LSB/HSB divide)")
print("  -> Members with mean dynamical surface density BELOW ~a0/(2piG)~107 Msun/pc^2 (canonical) are")
print("     internally deep-MOND (a_in<a0): LSB dwarfs, dE, UDG.  ABOVE it -> internally Newtonian, DEAD.")

print("\n  CARRIER LOCUS: for a_in = X * a0, the required (sigma, r_half):")
print(f"    {'a_in/a0':>7s} | sigma at r_half=1kpc | at 2kpc | at 3kpc   (km/s)   class")
for X in (0.1, 0.3, 0.5, 1.0, 3.0):
    row=[]
    for rh in (1.0, 2.0, 3.0):
        s = math.sqrt(X*A0_CAN*rh*kpc)/km
        row.append(s)
    cls = "UDG/dSph/LSB dE (CARRIER)" if X<=0.5 else ("dE transitional (weak)" if X<=1.0 else "L* / HSB dE (DEAD, ~0 signal)")
    print(f"    {X:7.1f} | {row[0]:17.0f}  | {row[1]:6.0f}  | {row[2]:6.0f}          {cls}")

print("\n  WHY HSB MEMBERS ARE SIGNAL-FREE (spread dies as a_in/a0 rises):")
print(f"    {'a_in/a0':>7s} | sigma_int/sigma_bary at a_ex=a0 | relational headroom d(ln boost)/d(y) ~ carrier weight")
prev=None
for X in (0.03, 0.1, 0.3, 0.5, 1.0, 3.0, 10.0):
    b = sigma_boost(X, 1.0)
    # headroom = fractional change of the boost as the EFE loading is memory-lagged by a factor;
    # proxy: sensitivity of ln(boost) to a small (10%) change in the loaded field (the memory residual lever).
    b_lag = sigma_boost(X, 0.9)
    headroom = abs(math.log(b) - math.log(b_lag))
    tag = "CARRIER" if X<=0.5 else ("weak" if X<=1.0 else "DEAD")
    print(f"    {X:7.2f} | {b:24.3f}       | {headroom*100:6.2f}%   {tag}")
print("  ==> The memory-residual lever (and hence D(zone)) collapses toward 0 as a_in/a0 -> large:")
print("      an internally-Newtonian (HSB) member has nu->1, no boost to modulate, so NO history spread.")
print("      SELECTION CUT (frozen): a_in = sigma_int^2/r_half  <  0.5 a0  (equivalently mu_0 >~ 24 mag/arcsec^2,")
print("      mean dynamical Sigma < ~a0/(2piG)).  Carriers: UDG (sigma~15-25), dSph/LSB dE (sigma~20-45).")
# assert the physics: boost and headroom both fall monotonically with depth
xs = [0.03,0.1,0.3,0.5,1.0,3.0,10.0]
hrs = [abs(math.log(sigma_boost(X,1.0))-math.log(sigma_boost(X,0.9))) for X in xs]
assert all(hrs[i] > hrs[i+1] for i in range(len(hrs)-1)), "carrier headroom must fall monotonically with a_in/a0"

# =========================================================================================
# (c) ZONE TAGGING -- first-infall vs ancient in projected phase space + the fixed a_ext bin
# =========================================================================================
hr("(c) ZONE TAGGING -- Rhee+2017 projected-phase-space zones + the fixed deprojected a_ext bin")
print("  Coordinates per member (Rhee+2017, ApJ 843:128):  X = R_proj/R200 ,  Y = |v_los - v_cl|/sigma_cl.")
print("  Rhee zones tag ORBITAL HISTORY (calibrated on N-body), which projected radius alone cannot.")
print("  Pre-registrable contrast uses ONLY the two robust zones (recent/backsplash are timescale-hostage):\n")
ZONE_DEFS = {
  "ANCIENT (reference)":  {"X":"< 0.5",       "Y":"< 1.5",  "note":"virialized core; Rhee ancient-fraction dominant, low first-infall contamination"},
  "FIRST-INFALL (signal)":{"X":"1.0 - 2.0",   "Y":"< 2.0",  "note":"infalling outskirts, pre-first-pericentre; Rhee first-infall-fraction dominant"},
}
for z,d in ZONE_DEFS.items():
    print(f"    {z:24s}  X(R/R200) {d['X']:10s}  Y(|dv|/sig) {d['Y']:8s}  <- {d['note']}")
print("""
  THE FIXED-FIELD TRICK (what makes D a COMMON-MODE difference):
    The two zones sit at DIFFERENT projected radius, hence different mean a_ext -- that radial
    EFE gradient is the SHARED (MG=MI) killer common mode, NOT the signal.  So D is NOT computed
    zone-vs-zone across radius.  Instead:
      1. Deproject each member to a_ext,i = G*M(<r_i)/r_i^2 from the cluster's CAUSTIC mass profile
         (GalWCat19 / HeCS), NOT from R_proj.
      2. BIN members by a_ext (width <= 0.3 dex).  Within a bin the radial gradient is a constant.
      3. Within EACH a_ext bin, members of BOTH orbit histories coexist (projection + orbit phase
         mix histories at a given true radius -- this is exactly what Rhee zones resolve).  Tag each
         as first-infall or ancient by its PPS zone, and difference ALONG the history axis at fixed field.
    MG field sector: D=0 in every bin (no worldline label).  MI: D>0, first-infall hotter, RISING outward.""")

# transition shell where the signal peaks, per cluster mass, and its angular size (design feasibility)
print("\n  WHERE THE SIGNAL PEAKS -- transition shell R(a_ex=a0)=sqrt(GM/a0) and its on-sky size:")
print(f"    {'M200(Msun)':>11s} {'R(a_ex=a0)Mpc':>13s}   (the first-infall carriers live at ~this radius, F3 peak)")
for M in (7e13, 1.4e14, 2e14, 4e14, 1.3e15):
    R = math.sqrt(G*M*MSUN/A0_CAN)/Mpc
    print(f"    {M:11.1e} {R:13.2f}")
print("  F3 RADIAL-PROFILE SEPARATOR (the primary confound beater): D(first-infall) must RISE outward,")
print("  peaking at a_ext ~ 0.3-1 a0 (~R500-R200), and DIE in the core -- tidal heating rises INWARD.")

# =========================================================================================
# (d) THE EXACT ESTIMATOR D(zone) + its inputs
# =========================================================================================
hr("(d) THE EXACT ESTIMATOR  D(zone; a_ext-bin)  and its inputs")
print(r"""  Per carrier i (after the a_in<0.5 a0 cut, caustic membership, and Dressler-Shectman substructure cut):
    sigma_int,i  : resolved internal stellar velocity dispersion (IFU/long-slit), LSF-corrected;   err e_i
    r_half,i     : projected half-light radius (imaging)
    M_bary,i     : baryonic mass (stars from SED + gas), for the baryon-only expected dispersion
    sigma_bary,i : beta-IMMUNE Wolf (2010) baryon-only dispersion:  sigma_bary = sqrt( G*M_bary / (3 r_half) )
    zone_i       : Rhee+2017 PPS zone in {FIRST-INFALL, ANCIENT}     from (R_proj/R200, |dv|/sigma_cl)
    a_ext,i      : G*M(<r_i)/r_i^2 from the caustic mass profile (deprojected) -> the fixed-field BIN

  ESTIMATOR (per a_ext bin b; inverse-variance weighted):
      L_i          = ln( sigma_int,i / sigma_bary,i )                          (the log EFE boost)
      w_i          = 1 / Var[L_i] ,   Var[L_i] ~ (e_i/sigma_int,i)^2 + (1/2 * dln M_bary,i)^2
      D_hat(b)     = ( sum_{i in FIRST,b} w_i L_i / sum w_i )
                     - ( sum_{j in ANCIENT,b} w_j L_j / sum w_j )
      sig_D(b)^2   = 1/sum_{FIRST,b} w_i  +  1/sum_{ANCIENT,b} w_j            (statistical)
      SYSTEMATIC floor (added in quadrature, irreducible; NOT removed by the theorem):
                     s_sys(b)^2 = s_proj^2 + s_tidal^2 ,  s_proj~1-2% (residual after zone deproj),
                     s_tidal~2-8% (same-signed; suppressed by low-tidal cluster selection + F3 slope test)

  PREDICTION (framework, both footings ~identical at fixed depth):
      D_pred(FIRST-INFALL) = +1.3% (canonical, LOW-PASS) / +1.5% (alt)   [+0.81% first-infall dev vs -0.47% ancient]
                             UP TO  +8..13%  (PURE-DELAY |K|=1 corner)    -- kernel-hostage band, all POSITIVE.
  DECISION:
      SUPPORT   = D_hat > 0 (first-infall hotter) AND the F3 profile rises outward peaking at the
                  transition shell AND baryon-blind (F4) -- jointly, at adequate power.
      FALSIFY   = D_hat < 0 at >=3 sigma (first-infall COOLER) or a null at adequate power (falsifies Tier ii).
      MG-IMPOSSIBLE content = any nonzero fixed-TRUE-field history contrast (theorem d/dy=0); the OBSERVABLE
                  claim is confound-contingent on F3 holding.""")

# =========================================================================================
# (a) TARGET CLUSTERS -- ranked by  N(resolved-sigma carriers) x low-tidal x phase-space coverage
# =========================================================================================
hr("(a) TARGET CLUSTERS -- ranked by  N(resolved-sigma carriers) x (low tidal env) x (phase-space coverage)")
# Each factor is a transparent 0-1 score with a CITED anchor.  Honest, prove-by-moving.
# N_car   : # members with EXISTING resolved internal sigma AND reachable as diffuse carriers
#           (dwarfs/dE/UDG; distance sets whether sigma~20-45 km/s is above the instrumental floor).
# tidal   : LOW-tidal / relaxation score (1=relaxed cool-core, low same-signed tidal floor).
# ps      : Rhee-style phase-space + caustic scaffolding (membership richness for M(<r) + zone tags).
CLUSTERS = [
  # name        dist_Mpc  M200      N_car  N_car_anchor
  ("Virgo",     16.5,  3.0e14,  39,  "SMAKCED 39 dEs resolved sigma (Toloba+2014ab/2015); nearest -> lowest-sigma dwarfs resolvable; NGVS/EVCC 1000s for PPS",
                        0.35, 0.85,  # tidal(LOW: assembling, M87+M49 subclusters, infalling groups) ; ps HIGH
   ),
  ("Fornax",    20.0,  7.0e13,  33,  "SAMI-Fornax Dwarfs Survey resolved dwarf sigma + Fornax3D MUSE (33 bright); FDS ~600 dwarf membership",
                        0.90, 0.60,  # tidal HIGH (relaxed cool-core, cleanest) ; ps MODERATE (low richness)
   ),
  ("Coma",     100.0,  1.3e15,  41,  "Kourkchi+2012 41 dEs reliable sigma (Keck/DEIMOS CaT, 26 new); Chilingarian+2009; MaNGA ancillary; richest PPS+caustic",
                        0.60, 1.00,  # tidal MODERATE (mostly relaxed, NGC4839 group) ; ps HIGHEST
   ),
  ("Hydra I",   50.0,  2.0e14,  15,  "LEWIS MUSE UDG/LSB kinematics + VEGAS dwarf catalog; relaxed (sigma_cl~724); resolved-sigma dwarf sample small",
                        0.85, 0.55,  # tidal HIGH (relaxed) ; ps MODERATE
   ),
  ("Perseus",   75.0,  8.0e14,   5,  "Gannon+2022 5 UDGs KCWI sigma; rich but distance walls resolved dwarf sigma; sloshing cool-core",
                        0.55, 0.70,  # tidal MODERATE (sloshing) ; ps MODERATE-HIGH
   ),
]
# distance penalty on the CARRIER factor: reliable stellar sigma of a ~25 km/s dwarf needs the line
# resolved above the instrumental floor; nearer clusters keep more carriers ABOVE it.  Fold a soft
# proximity weight (normalized to Virgo) into the carrier score so distance is not double-hidden.
print(f"  {'cluster':9s} {'d(Mpc)':>6s} {'M200':>8s} {'N_car':>6s} {'prox':>5s} {'tidal':>6s} {'PPS':>5s} {'SCORE':>7s}   anchor")
scored=[]
for name, d, M, Ncar, anch, tidal, ps in CLUSTERS:
    prox = min(1.0, (20.0/d))            # proximity weight (carrier reachability), capped at 1
    # carrier factor = existing resolved count * proximity reachability, on a log-ish 0-1 scale
    car = (Ncar/45.0)**0.7 * prox        # 45 ~ the richest existing resolved-sigma dwarf sample scale
    score = car * tidal * ps
    scored.append((score, name, d, M, Ncar, prox, tidal, ps, anch))
    print(f"  {name:9s} {d:6.1f} {M:8.1e} {Ncar:6d} {prox:5.2f} {tidal:6.2f} {ps:5.2f} {score:7.3f}   {anch[:0]}")
scored.sort(reverse=True)
print("\n  RANKING (score = carrier_reach x low-tidal x phase-space):")
for rank,(score,name,d,M,Ncar,prox,tidal,ps,anch) in enumerate(scored,1):
    print(f"   {rank}. {name:9s} score={score:.3f}   [{anch}]")

print("""
  READ (honest, both-ways -- the top two are a TENSION, not a clean winner):
    * VIRGO  = the CARRIER reservoir.  Nearest rich cluster (16.5 Mpc) -> the only place a
      sigma~20-30 km/s carrier is comfortably resolved; 39 SMAKCED dEs + the nearest UDGs.
      PENALTY: dynamically YOUNG (M87/M49 subclusters, live infall) -> the tidal floor is HIGH and
      the spherical caustic a_ext(R) is biased -- but the same youth gives a CLEAN, well-mapped
      first-infall population (good for zone tagging).  Primary CARRIER + SIGNAL sample.
    * FORNAX = the CLEAN control.  Relaxed cool-core -> the LOWEST tidal floor (best place to let
      F3 breathe), with a DEDICATED resolved-dwarf-sigma survey (SAMI-Fornax).  PENALTY: low
      richness caps N_car and weakens the caustic/PPS statistics.  Primary LOW-TIDAL control.
    * COMA   = the SCAFFOLDING king.  Richest membership -> best caustic M(<r) + Rhee tagging +
      MaNGA-served resolved sigma; 41 reliable dE sigma.  PENALTY: at 100 Mpc the sigma~20-40
      carriers sit at/below the LSF floor (upper limits) -- carrier QUALITY, not count, is the wall.
    * HYDRA I / PERSEUS = supporting.  Hydra I relaxed but thin resolved-dwarf sigma; Perseus rich
      but distance-walled (5 UDG sigma).  Stack fodder, not primary.
  PRE-REGISTERED SAMPLE = VIRGO (carriers+signal) + FORNAX (low-tidal control) as primary,
  COMA for the caustic/PPS scaffolding and a MaNGA cross-check; Hydra I + Perseus stacked in.""")

# =========================================================================================
# BOTH-WAYS DETECTABILITY -- carry the full kernel band AND the floors; report low-pass & pure-delay
# =========================================================================================
hr("DETECTABILITY (both-ways) -- full kernel-hostage band x confound floors, per corner")
# per-carrier ln-boost measurement scatter (dominated by sigma error near the LSF floor) + intrinsic
sig_lnboost_percarrier = 0.15     # ~15% per-carrier ln(sigma_int/sigma_bary) scatter (meas+intrinsic)
def detect(N_first, N_anc, s_tidal, D_signal, label):
    stat2 = sig_lnboost_percarrier**2 * (1.0/max(N_first,1) + 1.0/max(N_anc,1))
    s_proj = 0.015                                  # residual projection alias after Rhee deprojection
    sys2   = s_proj**2 + s_tidal**2
    sigD   = math.sqrt(stat2 + sys2)
    z      = D_signal / sigD
    print(f"    {label:38s} N_f={N_first:3d} N_a={N_anc:3d}  sig_D={sigD*100:4.1f}%  D={D_signal*100:4.1f}%  ->  z={z:4.2f}")
    return z

# carrier splits: after the a_in<0.5 cut ~60% of the existing resolved-sigma dwarfs are true carriers,
# then split ~ evenly between the two robust zones (first-infall is the outer, slightly fewer).
def carriers(Ncar):
    tot = round(Ncar*0.60); return round(tot*0.45), round(tot*0.55)   # (first, ancient)

print("  LOW-PASS corner  (D~1.3%, the honest baseline):")
for name, d, M, Ncar, anch, tidal, ps in CLUSTERS:
    nf, na = carriers(Ncar)
    s_tid = 0.02 + 0.06*(1-tidal)                   # tidal floor 2%(relaxed)->~8%(unrelaxed)
    detect(nf, na, s_tid, 0.013, f"{name} alone")
# stacks
def stack(sel, lbl, D, s_tid):
    nf=sum(carriers(N)[0] for (nm,_,_,N,_,_,_) in CLUSTERS if nm in sel)
    na=sum(carriers(N)[1] for (nm,_,_,N,_,_,_) in CLUSTERS if nm in sel)
    return detect(nf,na,s_tid,D,lbl)
print("  LOW-PASS corner  (stacks):")
stack({"Virgo","Fornax"},               "Virgo+Fornax (clean primary)",       0.013, 0.030)
stack({"Virgo","Fornax","Coma","Hydra I","Perseus"}, "ALL-5 stack",           0.013, 0.045)
print("\n  PURE-DELAY corner  (D~8-13%, kernel |K|=1 -- the ONLY corner that can clear the floors):")
for Dsig,lab in ((0.08,"D=8%"),(0.13,"D=13%")):
    stack({"Virgo","Fornax"},                          f"Virgo+Fornax (clean) {lab}", Dsig, 0.030)
    stack({"Virgo","Fornax","Coma","Hydra I","Perseus"}, f"ALL-5 stack {lab}",        Dsig, 0.045)

hr("VERDICT")
print("""  * LOW-PASS corner (D~1.3-1.5%): z<1 at EVERY accessible sample and stack -- the signal sits AT OR
    BELOW its own projection (~1-2%) and tidal (~2-8%) floors.  HONEST CENTRAL OUTCOME = NON-DETECTION.
  * PURE-DELAY corner (D~8-13%): a firewalled ~1.4-2.3 sigma HINT only on the clean low-tidal
    (Virgo+Fornax) stack, and only if the kernel actually sits at the |K|=1 top of the band.
  * The discriminating POWER is theorem-grade against the ENTIRE MG class (field-sector D=0); a
    DETECTION additionally needs the F3 outward-rising profile to separate the same-signed confounds
    -- by DESIGN, not by the theorem.  UNDERPOWERED is the valid, pre-registered expectation.
  * A clean detection is gated on a DEDICATED wide nearby-cluster dwarf-IFU survey (M* floor to logM~8,
    reliable stellar sigma well below 45 km/s) or ELT/HARMONI (~2032) reaching the sigma~20 km/s regime.
  * Both footings materially identical at fixed depth (2Z=11.58 footing-free).  a0 value + s=-1 POSTULATES.
    MG=0 at fixed true field the sole theorem-grade claim.  No 'theory closed'; neither win nor deficit manufactured.""")
print("\nEXIT 0 -- pre-registration ARMED (observable + selection); design/feasibility, not a confrontation.")
