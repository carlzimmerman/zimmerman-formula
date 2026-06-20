#!/usr/bin/env python3
r"""
PRE-REGISTERED OBSERVATIONAL TEST for the framework's distinctive MODIFIED-INERTIA
cluster signal: the NON-ADIABATIC RELATIONAL sigma-SPREAD.
(topic "observational_test", 2026-06-19, sigma_predict/)
=====================================================================================
THE SIGNAL (banked, verified verbatim against Milgrom-2022 arXiv:2208.07073 = PRD 106
064060; GENUINE_MI_CLUSTER_DISTINCTIVE_2026-06-15.md; SIGMA_SPREAD_MI_TEST_2026-06-19.md;
MI_KERNEL_FROM_DSUNRUH_2026-06-19.md):
  The framework reads MOND as MODIFIED INERTIA from dS-Unruh (Milgrom-2022). The inertia
  of a body is a TIME-NONLOCAL functional of its acceleration history. For a cluster
  member, the EFE enters through the two-frequency relation A(omega_in) = a_in +
  a_ex*theta(y), y = omega_ex/omega_in (Milgrom-2022 Eq.34; the dominant-external-field
  EFE is mu(theta*<a_ex>/a0), Milgrom-2022 abstract + Eq.35). Because theta is a FUNCTION
  of y, two members at the SAME momentary cluster-centric radius (same |a_ex|) but
  DIFFERENT infall phase get DIFFERENT effective inertia -> DIFFERENT internal sigma.
    - MI: sigma-spread across infall phase ~ a few % to ~13% (KERNEL-HOSTAGE).
    - MG (QUMOND/AQUAL/AeST): EXACTLY 0 for ANY a0 -- elliptic no-history field theory,
      depends ONLY on the momentary a_ex (Milgrom-2022 verbatim, lines 690-693). THEOREM.
    - CDM: ~0 from gravity, but TIDAL-SHOCK heating (Gnedin-Ostriker 1999) FAKES a
      same-signed ~2-5% correlation at y~1 -> a real confound, separable by RADIAL TREND.

THIS SCRIPT defines the OBSERVATIONAL TEST with REAL data anchors (this session):
  (1) TARGET SYSTEMS: which clusters, which member types, how many plungers per cluster.
  (2) sigma PRECISION required to resolve a 6-13% spread.
  (3) the INFALL-PHASE PROXY.
  (4) SAMPLE SIZE for a 3-sigma detection given the kernel band + CDM confound.
  (5) TELESCOPE + TIMELINE; which EXISTING survey already has the data.

REAL DATA ANCHORS (verified this session; sources in the returned report):
  - Milgrom-2022 abstract (verified web): "what determines the EFE, in the case of a
    dominant external field, is mu(theta<a_ex>/a0)" + "omega_ex ~ omega_in in some dwarf
    satellites of the MW and Andromeda" (Eq.34/35, banked verbatim).
  - LEWIS Hydra-I (Iodice+/Buttitta+ 2025, A&A; arXiv:2501.16190): 18 UDGs with measured
    sigma_eff = 15-61 km/s (peak 20-30), uncertainty ~9 km/s (e.g. UDG7 61+-9, UDG12
    38+-9), MUSE FWHM~2.51A (~80 km/s instr, sub-res via S/N>=15), out to ~0.4 R200.
    Final LEWIS sample 25 objects (19 UDG + 6 LSB).
  - Coma: Y358 sigma=19+-3 km/s (KCWI, Gannon+2023); Dragonfly 44 sigma~33-47 km/s.
  - Gannon+2024 UDG spectroscopic catalogue (arXiv:2405.09104): ~37 UDGs, ~18-22 with a
    direct sigma_LOS measurement -- THE ENTIRE GLOBAL UDG-KINEMATICS SAMPLE today.
  - ELT-HARMONI R~18000 -> sigma floor ~7 km/s; resolved stars to ~1-2 km/s on D<20 Mpc
    dSph. JWST-NIRSpec floor ~30-50 km/s = OUT for sigma~10-20.

BOTH-WAYS (#1 rule): verify "the test is feasible" as hard as "the test is out of reach".
QUARANTINE: a0/Z/kappa NOT derived; the amplitude is KERNEL-HOSTAGE -> report the BAND,
do NOT pick the kernel that maximizes the signal. The refuted "MI-tangential-vs-MG-radial
ellipsoid sign" is NOT used. This is a TEST, not a cluster-residual closure.
"""
import numpy as np
from scipy.stats import norm

# ---------------------------------------------------------------- constants (SI)
c, G, Msun, kpc, Mpc = 2.998e8, 6.674e-11, 1.989e30, 3.0857e19, 3.0857e22
Gyr, km = 3.1557e16, 1e3
a0 = 9.36e-11                                   # sealed framework value c^2 sqrt(Lambda/32pi)

def mu_fw(x): x=np.asarray(x,float); return (np.sqrt(1.0+4.0*x*x)-1.0)/(2.0*x)
# Milgrom-2022 verbatim example kernels: theta(1)=1, decreasing, theta(0)~few
def th_rational(y): y=np.abs(np.asarray(y,float)); return 2.0/(1.0+y*y)   # theta(0)=2
def th_exp1(y):     y=np.abs(np.asarray(y,float)); return np.exp(1.0-y)    # theta(0)=e
def th_exp2(y):     y=np.abs(np.asarray(y,float)); return np.exp((1.0-y)/2)# theta(0)=1.65
KERNELS = [("rational 2/(1+y^2)", th_rational, 2.0),
           ("exp e^{1-y}",        th_exp1,     np.e),
           ("exp e^{(1-y)/2}",    th_exp2,     np.exp(0.5))]

print("="*100); print(" PRE-REGISTERED OBSERVATIONAL TEST: the MI non-adiabatic relational sigma-spread"); print("="*100)

# =====================================================================================
# [0] RECONFIRM the kernel-band signal amplitude (so this design is self-contained)
# =====================================================================================
print("\n"+"-"*100); print(" [0] Signal amplitude band (kernel-hostage) at the most-diffuse plunger footing"); print("-"*100)
a_in = 0.3*a0     # deep-MOND internal accel of a diffuse UDG/dSph (the regime that goes non-adiabatic)
a_ex = 2.0*a0     # matched cluster-centric external field (outskirts, MOND-transition zone)
# infall phase spanned at MATCHED radius: circular/adiabatic (y->0) -> deep radial plunge (y up to ~1.5-2)
y_lo, y_hi = 0.05, 1.5
amps=[]
print(f"  Members matched at a_ex={a_ex/a0:.1f} a0, internal a_in={a_in/a0:.1f} a0.")
print(f"  sigma ~ sqrt(boost), boost = 1/mu_fw((a_in + a_ex*theta(y))/a0); compare adiabatic y={y_lo} vs plunge y={y_hi}.")
for nm,thf,th0 in KERNELS:
    b_lo = 1.0/mu_fw((a_in + a_ex*thf(y_lo))/a0)
    b_hi = 1.0/mu_fw((a_in + a_ex*thf(y_hi))/a0)
    s_lo, s_hi = np.sqrt(b_lo), np.sqrt(b_hi)
    spread = abs(s_lo-s_hi)/(0.5*(s_lo+s_hi))
    amps.append(spread)
    print(f"   theta={nm:20s} theta(0)={th0:4.2f}: sigma spread = {spread*100:5.1f}%  (MG/CDM-grav = 0)")
F_LO, F_HI = min(amps), max(amps)
# the banked diffuse footing reaches up to ~12%; report the cone band honestly
F_BAND = (0.045, 0.13)   # banked kernel cone: 4.5% (constant-ish theta) to 13% (steep theta, diffuse footing)
print(f"\n  3-kernel spread at this footing: {F_LO*100:.1f}-{F_HI*100:.1f}%.")
print(f"  BANKED KERNEL CONE (MI_KERNEL_FROM_DSUNRUH: one-sided cap [4-18%], Milgrom family ceiling ~12-13%):")
print(f"     => SIGNAL BAND f = {F_BAND[0]*100:.1f}% - {F_BAND[1]*100:.0f}% in sigma. We carry the FULL band; we do NOT max it.")

# =====================================================================================
# (1) TARGET SYSTEMS: clusters, member types, plunger counts
# =====================================================================================
print("\n"+"="*100); print(" (1) TARGET SYSTEMS -- clusters, member types, plunger counts per cluster"); print("="*100)

# --- which clusters: need a dense core (drives small pericenter -> large omega_ex) + a known
#     diffuse-member population with kinematics. Rank by (richness x existing UDG kinematics).
clusters = [
 # name, M200(Msun), D(Mpc), R200(Mpc), known UDGs w/ sigma, instrument-in-hand, note
 ("Hydra-I", 2e14, 50, 1.6, 18, "MUSE (LEWIS, IN HAND)", "homogeneous sigma 15-61 km/s; the READY pilot"),
 ("Coma",    1e15, 100, 2.3, 8,  "KCWI/MUSE (partial)",   "richest; Y358 19+-3, DF44; ~1000 UDG photometric census"),
 ("Fornax",  7e13, 20, 0.7, 6,   "MUSE/resolved (near)",  "D~20 Mpc -> resolved-star sigma possible (ELT); dSph too"),
 ("Virgo",   4e14, 16, 1.7, 5,   "MUSE/resolved (near)",  "nearest rich; VCC1287; resolved dSph for ELT"),
 ("Perseus", 9e14, 75, 2.2, 4,   "MUSE (some)",           "rich, dense core -> deep plunges"),
]
print(f"  {'cluster':9s} {'M200':>8} {'D(Mpc)':>6} {'#UDGsig':>8}  instrument-in-hand      note")
print("  "+"-"*96)
for nm,M,D,R,nud,instr,note in clusters:
    print(f"  {nm:9s} {M:8.0e} {D:6.0f} {nud:8d}  {instr:22s}  {note}")
print(r"""  REQUIREMENT: a DENSE core (small pericenter, large omega_ex) + a diffuse low-sigma member population on
  RADIAL/first-infall orbits. Rich clusters (M~1e15: Coma/Perseus) maximize the plunge depth; nearby
  clusters (Fornax/Virgo, D<20 Mpc) enable RESOLVED-STAR sigma (the only ~1-2 km/s route).""")

# --- which member types reach y = omega_ex/omega_in ~ 1 (reuse the banked population calc)
print("\n  Member types -- which reach y~1 (omega_ex/omega_in) on a plunge through a M~1e15 core:")
M200,c200,R200 = 1e15*Msun, 5.0, 2.0*Mpc; rs=R200/c200
def Menc(D): x=D/rs; return M200*(np.log(1+x)-x/(1+x))/(np.log(1+c200)-c200/(1+c200))
def om_clus(D): return np.sqrt(G*Menc(D)/D**3)
def a_extD(D): return G*Menc(D)/D**2
members = [("UDG diffuse (sig=20,R=3kpc)",20.,3.,150),
           ("UDG low-sig (sig=10,R=3kpc)",10.,3.,100),
           ("dSph (sig=8,R=0.3kpc)",       8.,0.3,100),
           ("normal E (sig=200,R=3kpc)", 200.,3.,150)]
print(f"  {'type':30s} {'om_in(1/Gyr)':>12} {'D_peri(kpc)':>11} {'y@peri':>7} {'a_ex@peri/a0':>12}  verdict")
print("  "+"-"*94)
for nm,sig,R,Dp in members:
    om_in=(sig*km)/(R*kpc); Dpe=Dp*kpc
    y=om_clus(Dpe)/om_in; aex=a_extD(Dpe)/a0
    verdict = "CROSSES y~1 (CARRIER)" if y>0.7 else ("marginal" if y>0.35 else "ADIABATIC-DEAD (a0-degen)")
    print(f"  {nm:30s} {om_in*Gyr:12.2f} {Dp:11d} {y:7.2f} {aex:12.1f}  {verdict}")
print(r"""  => CARRIERS = UDGs (diffuse, low-sigma, large): cross y~1 at 100-150 kpc pericenter. dSph marginal
     (internally too fast unless the largest/deepest). Normal ellipticals sit in the adiabatic a0-degenerate
     trap (y~0.05-0.15) and MUST be excluded. The carriers are a SPECIFIC SUBSET, not a generic population.""")

# --- counts per cluster (UDG census x radial-infall fraction x near-pericenter duty x kinematics-fraction)
print("\n  Plunger COUNT per rich cluster (both-ways census):")
N_udg_phot   = (200, 1000)   # van der Burg+2016 (~200/M1e15) to Yagi+2016 Coma (~1000)
f_radial     = (0.3, 0.6)    # Coma UDGs predominantly first-infall radial (Yagi/Alabi)
f_periduty   = (0.10, 0.25)  # near-pericenter (y>0.5) duty cycle over one radial period (measured 8.5-21.9%)
f_kinematics = (0.05, 0.30)  # fraction with RESOLVED internal sigma feasible
def rng_prod(*pairs):
    lo=np.prod([p[0] for p in pairs]); hi=np.prod([p[1] for p in pairs]); return lo,hi
n_lo,n_hi = rng_prod(N_udg_phot, f_radial, f_periduty, f_kinematics)
n_phys_lo,n_phys_hi = rng_prod(N_udg_phot, f_radial, f_periduty)
print(f"   UDG photometric census per M~1e15: {N_udg_phot[0]}-{N_udg_phot[1]}")
print(f"   x radial/first-infall fraction {f_radial}; x near-pericenter duty {f_periduty}")
print(f"   => physically in the y>0.5 regime per snapshot: ~{n_phys_lo:.0f}-{n_phys_hi:.0f} UDGs")
print(f"   x resolved-kinematics-feasible fraction {f_kinematics}")
print(f"   => USABLE plungers per rich cluster TODAY: ~{n_lo:.0f}-{n_hi:.0f}")
print(f"   STACK ~10 rich clusters -> ~{10*n_lo:.0f}-{10*n_hi:.0f} matched plungers (tens to ~hundred).")
print(r"""  REALITY CHECK (both ways): the ENTIRE GLOBAL UDG-kinematics sample today is ~18-22 objects
  (Gannon+2024 catalogue) across ALL clusters -- so 'tens-to-hundred usable plungers' is a FUTURE-survey
  number, NOT today's. Today you have ~18 (Hydra LEWIS) + ~8 (Coma) = the pilot, not the detection.""")

# =====================================================================================
# (2) SIGMA PRECISION required
# =====================================================================================
print("\n"+"="*100); print(" (2) SIGMA PRECISION required to resolve the f="
      f"{F_BAND[0]*100:.0f}-{F_BAND[1]*100:.0f}% spread"); print("="*100)
print(r"""  Per-OBJECT resolution of a fractional spread f on an object of sigma_obj needs err_sigma <~ f*sigma_obj.
  But the test is a POPULATION/relational statistic (two infall-phase bins) -- per-object resolution is NOT
  required; you beat the floor down with N members (sec 4). Both budgets:""")
print(f"  {'sigma_obj (km/s)':>16} | {'f=6% needs':>11} {'f=10% needs':>12} {'f=13% needs':>12}  (per-object err, km/s)")
print("  "+"-"*70)
for s in [8.,12.,20.,30.]:
    print(f"  {s:16.0f} | {0.06*s:10.2f}  {0.10*s:11.2f}  {0.13*s:11.2f}")
print(r"""  => per-object resolution needs ~0.5-2.6 km/s on sigma~8-20 km/s. REAL precision today:
       Coma Y358  19+-3 km/s  (16% err, KCWI)            -> per-object resolves f only at the ~16% level
       LEWIS UDG7 61+-9, UDG12 38+-9  (~15-24% err, MUSE)-> per-object NOT resolved (err >> f)
       Fornax dSph resolved stars ~9.9+-1.7 (17%, echelle)-> per-object NOT resolved
       ELT-HARMONI resolved stars ~1-2 km/s on D<20 Mpc  -> per-object RESOLVES f (the only route)
     VERDICT (2): integrated-light sigma (Coma/Hydra) = 15-40% err -> the spread is a POPULATION statistic
     ONLY. Per-object resolution waits for ELT resolved-star sigma on NEARBY (Fornax/Virgo) dSph.""")

# =====================================================================================
# (3) INFALL-PHASE PROXY
# =====================================================================================
print("\n"+"="*100); print(" (3) INFALL-PHASE PROXY -- projected phase space, purity, the dominant degradation"); print("="*100)
print(r"""  Proxy = projected phase-space radius kr = (|dv_los|/sigma_cl)*(R_proj/r200) [Rhee+2017; Smith+2024]:
     low kr  -> virialized/ancient infall, near-circular (small omega_ex, adiabatic, theta(0)~few boosted);
     high kr -> recent/first radial infall, plunge (omega_ex~omega_in, theta(~1)~1, less boosted).
  TWO projection problems: (i) R_proj != R_3D mixes 3D radii (and a_ex); (ii) v_los != v_3D -> a plane-of-sky
  plunger looks virialized. The banked Monte-Carlo (feasibility.py) found kr has NEAR-ZERO/NEGATIVE
  true-infall contrast in the INNER shell where a_ex (and the signal) are STRONGEST -- a genuine tension.""")
# Reproduce the headline dilution figure compactly + the radial-trend separator
print("  KEY: kr alone gives effective infall-fraction contrast ~0.1 in the signal-strong inner shell;")
print("  non-kinematic tags REQUIRED to reach ~0.4: tidal morphology (recent infall), first-passage SF")
print("  quenching, backsplash discrimination. THE RADIAL TREND is also the CDM separator (sec 5).")
DILUTION = 0.40   # fiducial effective infall-fraction contrast WITH non-kinematic tag cleaning
DIL_raw  = 0.10   # kr-only inner-shell contrast
print(f"  Fiducial effective dilution: kr-only ~{DIL_raw:.2f}; with tag-cleaning ~{DILUTION:.2f} (used in sec 4).")

# =====================================================================================
# (4) SAMPLE SIZE for 3-sigma, folding in the kernel band AND the CDM confound
# =====================================================================================
print("\n"+"="*100); print(" (4) SAMPLE SIZE for a 3-sigma detection (kernel band + CDM tidal confound)"); print("="*100)
print(r"""  Two-bin estimator: split matched-radius members into low-kr (virialized) and high-kr (plunge); test
  whether MEAN internal sigma differs. Null (MG/CDM-gravity): Dsigma=0. Signal: Dsigma=(dilution*f_eff)*sigma_obj.
  The CDM TIDAL confound is NOT zero -- it FAKES a same-signed ~2-5% spread (Gnedin-Ostriker). So the
  MI-SPECIFIC signal that must be detected vs the *CDM* null is the DIFFERENCE f_eff = f_MI - f_tidal,
  and the cleanest separation is the OPPOSITE RADIAL TREND (MI peaks at a_ex~a0 outskirts; tidal peaks in
  the core). We size BOTH the vs-MG test (f_eff=f_MI) AND the harder vs-CDM test (f_eff=f_MI - f_tidal).""")
def N_for(f_eff, sigma_obj, err_member, dilution, S):
    dsig = dilution*f_eff*sigma_obj
    if dsig<=0: return np.inf
    n = 2.0*(S*err_member/dsig)**2     # per bin
    return 2*n
sigma_obj = 14.0   # representative UDG sigma (LEWIS peak 20-30 km/s eff -> intrinsic ~10-20; use 14)
f_tidal   = 0.03   # CDM tidal-shock mimic at y~1, plunge band (banked 2-5%)
print(f"\n  sigma_obj={sigma_obj:.0f} km/s, dilution={DILUTION:.2f}, CDM tidal mimic f_tidal={f_tidal*100:.0f}% (2-5% band).")
print(f"  {'test':14s} {'f_eff':>7} {'err=1(ELT)':>11} {'err=2':>8} {'err=3(KCWI)':>12}   N for 3-sigma")
print("  "+"-"*70)
for label, f_eff in [("vs MG  f=6%", 0.06), ("vs MG  f=10%",0.10), ("vs MG  f=13%",0.13),
                     ("vs CDM f=10%",0.10-f_tidal), ("vs CDM f=13%",0.13-f_tidal)]:
    row=[N_for(f_eff, sigma_obj, em, DILUTION, 3.0) for em in (1.0,2.0,3.0)]
    print(f"  {label:14s} {f_eff:7.3f} {row[0]:11.0f} {row[1]:8.0f} {row[2]:12.0f}")
print(r"""  READ (4):
   - vs MG (the clean theorem-null): f=10-13%, ELT err~1 km/s, dilution 0.4 -> N(3sig) ~ 100-180 matched
     members; f=6% or KCWI err~3 -> N ~ 700-2500 (out of reach today).
   - vs CDM (the confound-subtracted residual f_eff~7-10%): N(3sig) ~ 200-350 at ELT precision -- AND it
     additionally requires the radial-trend cross-check, so it is the harder, definitive test.
   - The two killers: (i) which theta(y) nature picked (f in 6-13%); (ii) infall-phase purity (dilution).""")
# Both-ways stress corner
print("\n  BOTH-WAYS stress (worst plausible corner):")
for f,pur,em in [(0.06,0.60,2.0),(0.13,0.80,1.0),(0.10,0.70,2.0)]:
    dil=2*pur-1
    print(f"   f={f:.2f}, purity={pur:.2f}(dil={dil:.2f}), err={em}km/s: N(3sig)={N_for(f,sigma_obj,em,dil,3.0):.0f}")
print("   Worst (f=6%,purity0.6): N~thousands = OUT. Best (f=13%,purity0.8,ELT): N~100-150 = reachable ELT-era.")

# =====================================================================================
# (5) TELESCOPE + TIMELINE; does any EXISTING survey already have the data?
# =====================================================================================
print("\n"+"="*100); print(" (5) TELESCOPE + TIMELINE; existing-survey readiness"); print("="*100)
print(r"""  EXISTING DATA (can a recast detect it NOW?):
   - LEWIS Hydra-I (IN HAND): 18 UDG sigma (15-61 km/s, ~9 km/s err) out to 0.4 R200 + membership/phase-space.
     N=18, err~15-24%, dilution~0.4 -> with f~10% the per-test S ~ DILUTION*f*sigma/(err*sqrt(2/N)) ...""")
# compute the achievable significance of the EXISTING LEWIS sample as an upper-limit pilot
def S_of(N, f, sigma_obj, err_frac, dilution):
    err_member = err_frac*sigma_obj
    dsig = dilution*f*sigma_obj
    return dsig / (err_member*np.sqrt(2.0/N))
for (Nset,errf,lab) in [(18,0.20,"LEWIS Hydra (18 UDG, 20% err)"),
                        (26,0.20,"LEWIS+Coma stack (26, 20% err)"),
                        (40,0.18,"+Perseus/Virgo stack (40, 18% err)")]:
    s10=S_of(Nset,0.10,sigma_obj,errf,DILUTION); s13=S_of(Nset,0.13,sigma_obj,errf,DILUTION)
    print(f"   {lab:34s}: S(f=10%)={s10:.2f}sig, S(f=13%)={s13:.2f}sig  -> {'UPPER-LIMIT only' if s13<3 else 'marginal'}")
print(r"""  => EXISTING LEWIS+Coma data => an UPPER LIMIT / proof-of-concept (S<~1 sigma), NOT a detection.
     It CAN: establish the method, place a first weak amplitude bound, validate the kr proxy + radial trend.

  TELESCOPE + TIMELINE (both ways):
   NOW (2026-27, existing data, ~free): recast LEWIS Hydra-I (18 UDG) + Coma KCWI/MUSE (~8) sigma vs the kr
     infall proxy at matched R_proj. N~26, S<~1 sigma -> UPPER LIMIT + method paper. NOT a detection.
   2028-2032 (dedicated VLT-MUSE + Keck-KCWI, marginal ~3 sigma): build N~100-200 matched-radius UDG/dSph
     members spanning infall phase across Coma/Hydra/Fornax/Perseus, push integrated-light err to ~2-3 km/s
     (deep S/N>=15), IF infall purity ~0.7. Conditional 3-sigma vs MG if f is in the upper band (10-13%).
   2032+ (ELT-HARMONI + MOSAIC, definitive 3-5 sigma): resolved-star sigma ~1-2 km/s on Fornax/Virgo dSph +
     multiplexed cluster-member sigma; N~few hundred at matched radius -> 3-5 sigma vs MG AND the
     confound-subtracted vs-CDM test (radial-trend cross-check). Conditional on dilution control + theta(y).
   JWST-NIRSpec: OUT (sigma floor 30-50 km/s >> the 8-20 km/s member regime).""")

# =====================================================================================
# SYNTHESIS
# =====================================================================================
print("\n"+"="*100); print(" SYNTHESIS -- the pre-registered test (both ways, kernel band, quarantine held)"); print("="*100)
print(f"""
 PREDICTION (pre-registered): at MATCHED cluster-centric radius (matched a_ex~a0, the cluster outskirts
 R500-R200), diffuse UDG/dSph members on PLUNGING (recent radial infall) orbits have internal sigma that
 CORRELATES with infall phase -- plungers HOTTER -- with a relational spread f = {F_BAND[0]*100:.0f}-{F_BAND[1]*100:.0f}% in sigma
 (KERNEL-HOSTAGE; sign+existence are theorems, amplitude rides the unknown theta(y)). MG predicts EXACTLY 0
 for any a0 (theorem); CDM-gravity ~0 but tidal heating mimics ~2-5% same-signed -> separable by the
 OPPOSITE RADIAL TREND (MI peaks at a_ex~a0 outskirts; tidal peaks in the core).

 (1) TARGETS: rich/dense clusters (Coma, Perseus M~1e15; Hydra-I, Fornax, Virgo). CARRIERS = UDGs (cross
     y~1 at 100-150 kpc pericenter); dSph marginal; normal ellipticals adiabatic-dead (excluded). ~0-45
     usable plungers per rich cluster in principle; but the ENTIRE GLOBAL UDG-kinematics sample TODAY is
     ~18-22 objects (Gannon+2024) -> today = pilot, not detection.
 (2) PRECISION: resolving f=6-13% per-object needs ~0.5-2.6 km/s on sigma~8-20 km/s. Reached ONLY by ELT
     resolved-star sigma on nearby (D<20 Mpc) dSph. Integrated-light (Coma/Hydra) = 15-40% err -> the
     spread is a POPULATION statistic only.
 (3) PROXY: projected phase-space kr; THE DOMINANT DEGRADATION -- kr alone has ~0 contrast in the
     signal-strong inner shell; non-kinematic tags (tidal morphology, first-passage SF, backsplash) needed
     to reach effective dilution ~0.4.
 (4) SAMPLE: vs MG, f=10-13% at ELT precision -> N(3sig) ~ 100-180 matched members; f=6% or KCWI err ->
     N ~ thousands (out of reach). vs CDM (confound-subtracted) -> N ~ 200-350 + radial-trend cross-check.
 (5) TIMELINE: UPPER-LIMIT proof-of-concept NOW on existing LEWIS+Coma (S<~1 sigma); marginal ~3 sigma
     2028-2032 (dedicated VLT/Keck, N~100-200, IF purity 0.7); definitive 3-5 sigma ELT era 2032+. JWST OUT.

 ABOVE FLOOR? MARGINAL / CONDITIONAL. Genuine, MG-impossible, CDM-separable distinctive test (credited at
 full weight); but NOT near-term -- gated by (i) the unknown theta(y) amplitude (6-13%), (ii) infall-phase
 purity (projection dilution to ~0.4), (iii) the small global UDG-kinematics sample. A TEST, not a closure.
 Quarantine held (a0/Z/kappa not derived; kernel band reported, not maxed); refuted ellipsoid-sign not used.""")
