#!/usr/bin/env python3
r"""
OBSERVATIONAL FEASIBILITY of detecting the framework's distinctive MODIFIED-INERTIA
cluster signal: a 6-13% member-internal sigma SPREAD across infall phase at MATCHED
cluster-centric radius.  (topic "feasibility", 2026-06-19, sigma_spread/)
====================================================================================
THE SIGNAL (banked: GENUINE_MI_CLUSTER_DISTINCTIVE_2026-06-15.md;
member_MI_nonadiabatic_plunge.py; cluster_closure/mi_dynamic_route.py):
  At a MATCHED momentary cluster-centric radius (same |a_ext|), the framework's
  time-nonlocal modified inertia predicts member-internal sigma CORRELATES with
  infall phase:
     - a recently-infallen PLUNGER (omega_ex ~ omega_in, non-adiabatic) gets
       theta(~1) ~ 1  -> LESS boosted;
     - a slow/circular member (omega_ex << omega_in, adiabatic) gets
       theta(0) ~ few -> MORE boosted.
  MI predicts a NONZERO sigma spread ~6-13% (theta-form dependent: rational 10.3%,
  e^{1-y} 11.8%, e^{(1-y)/2} 6.2%).  MODIFIED GRAVITY (QUMOND/AeST/all MG-MOND) and
  CDM both predict EXACTLY ZERO spread for ANY a0 (MG depends only on the MOMENTARY
  a_ext -- Milgrom-2022 verbatim; CDM has no a0 and no memory).
  => A detection of a nonzero, infall-phase-correlated sigma spread at matched radius
     => modified INERTIA is real and DISTINCT from modified gravity. A TEST, not a
     cluster-residual closure.

THIS SCRIPT answers ONLY the OBSERVATIONAL-FEASIBILITY question (both ways):
  (a) sigma precision: to detect a 6-13% spread on a sigma~10-20 km/s object you need
      ~0.6-2.6 km/s precision per member. How many member stars / which instrument?
  (b) the infall-phase PROXY: projected phase space (v_los vs R_proj); how cleanly can
      plunging vs virialized be separated AT MATCHED 3D radius given projection?
  (c) sample size: for N members with sigma_i +- err_i, how many for 3-5 sigma vs the
      MG/CDM zero-spread null?
  (d) which real clusters/surveys can deliver it; concrete design + timeline.

Real-instrument anchors (verified this session, sources in returned report):
  - KCWI Coma UDG Y358: sigma = 19 +- 3 km/s (16% err), instr res ~13 km/s [Gannon+2023]
  - MUSE-Faint Eri-2 (resolved stars): sigma = 10.3 (+3.9/-3.2) km/s [MUSE-Faint I 2020]
  - LEWIS Hydra UDGs (MUSE integrated light): sigma_eff 5-50 km/s, e.g. UDG11 20+-8 km/s
    (40% err); recover sigma below the ~70 km/s MUSE instr res only at S/N>=15;
    high-sigma UDGs +-9 km/s ~15-20% err [LEWIS II 2025]
  - Fornax dSph (resolved stars, echelle R~14 km/s): sigma = 9.9 +- 1.7 km/s from 44
    stars (~17% err) [Mateo+1991]
  - JWST-NIRSpec: floor ~30-50 km/s (G235H ~50, G235M ~130) -> UNUSABLE below sigma~30
  - ELT-HARMONI: R~18000 -> sigma floor ~7 km/s @1.92um; MOSAIC HR R~20000 -> ~15 km/s
  - PPS infall proxy: kr = (dv/sigma_cl)*(r/r200); virialized core kr<0.1, infall kr>0.4
    [Rhee+2017; Pasquali; Smith+2024] -- STATISTICAL, projection-contaminated.

BOTH-WAYS (#1 rule): we verify the test is reachable AS HARD AS we verify it is not.
QUARANTINE: a0/Z/kappa NOT derived. We do NOT use the REFUTED "MI-tangential-vs-MG-
radial ellipsoid sign" (both came out tangential). The amplitude depends on the UNKNOWN
MI kernel theta(y)/A(omega) -- stated honestly. This is a TEST, NOT a cluster closure.
"""
import numpy as np
from scipy.stats import norm

c, G, Msun, kpc, Mpc = 2.998e8, 6.674e-11, 1.989e30, 3.0857e19, 3.0857e22
a0 = 9.36e-11                                   # sealed framework value
def mu_fw(x): x=np.asarray(x,float); return (np.sqrt(1.0+4.0*x*x)-1.0)/(2.0*x)

# theta(y): Milgrom 2022 VERIFIED example forms (theta(1)=1, decreasing, theta(0)~few)
def theta_rational(y): y=np.abs(np.asarray(y,float)); return 2.0/(1.0+y*y)
def theta_exp1(y):     y=np.abs(np.asarray(y,float)); return np.exp(1.0-y)
def theta_exp2(y):     y=np.abs(np.asarray(y,float)); return np.exp((1.0-y)/2.0)
THETAS = [("rational 2/(1+y^2)", theta_rational, 2.0),
          ("exp e^{1-y}",        theta_exp1,     np.e),
          ("exp e^{(1-y)/2}",    theta_exp2,     np.exp(0.5))]

print("="*100)
print(" FEASIBILITY: detecting the 6-13% MI sigma-spread-at-matched-radius vs the MG/CDM zero null")
print("="*100)

# ====================================================================================
# RECONFIRM the signal amplitude (reuse the banked kernel) so the feasibility is self-contained
# ====================================================================================
print("\n"+"-"*100)
print(" [0] Reconfirm the banked signal: MI sigma SPREAD across infall phase at MATCHED a_ext")
print("-"*100)
a_in_fixed = 0.3*a0          # diffuse UDG/dSph internal accel (deep-MOND, the regime that goes non-adiabatic)
a_ext_fixed= 2.0*a0          # matched cluster-centric external field (the same for all members compared)
# infall phase spanned by members at the SAME radius: circular(adiabatic) -> deep radial(plunge)
y_phase = np.array([0.05, 0.25, 0.5, 0.75, 1.0, 1.5])     # omega_ex/omega_in across infall phase
print(f"  Members all at MATCHED a_ext={a_ext_fixed/a0:.1f} a0, internal a_in={a_in_fixed/a0:.1f} a0.")
print(f"  sigma ~ sqrt(boost), boost = 1/mu_fw((a_in + a_ext*theta(y))/a0).  MG: theta->1 always (one number).")
sigma_spread = {}
for nm, thf, th0 in THETAS:
    boosts = np.array([1.0/mu_fw((a_in_fixed + a_ext_fixed*thf(y))/a0) for y in y_phase])
    sig    = np.sqrt(boosts)                                  # sigma ~ sqrt(boost)
    spread = (sig.max()-sig.min())/sig.mean()
    sigma_spread[nm] = spread
    print(f"   theta={nm:22s}: sigma spread (max-min)/mean = {spread*100:5.1f}%   (MG/CDM = 0.0% for ANY a0)")
SPREAD_BAND = (min(sigma_spread.values()), max(sigma_spread.values()))
print(f"\n  => SIGNAL BAND (theta-form spread): {SPREAD_BAND[0]*100:.1f}% - {SPREAD_BAND[1]*100:.1f}%  "
      f"(consistent w/ banked 6-13%). MG/CDM null = EXACTLY 0.")
print("  NOTE: amplitude is UNVERIFIED in magnitude (unknown theta(y)); only nonzero-vs-zero is robust.")

# ====================================================================================
# (a) SIGMA PRECISION: per-member error needed, and how many stars / which instrument
# ====================================================================================
print("\n"+"="*100)
print(" (a) SIGMA PRECISION -- per-member error budget, and how to reach it (stars / instrument)")
print("="*100)
print(r"""  To DETECT a fractional spread f in sigma across a population, each member's sigma must be measured
  to better than ~f to resolve the spread per-object, OR you beat it down statistically with many
  members (sec c). Set the per-member target by f and the object's sigma.""")
sigma_objs = {"UDG/dSph (sigma=12)":12.0, "UDG (sigma=20)":20.0, "bright dSph (sigma=10)":10.0}
print(f"\n  {'object':24s} | {'f=6%':>10} {'f=10%':>10} {'f=13%':>10}   (required err_sigma in km/s for per-object resolve)")
print("  "+"-"*72)
for label, s in sigma_objs.items():
    print(f"  {label:24s} | {0.06*s:9.2f} {0.10*s:10.2f} {0.13*s:10.2f}")
print(r"""
  => Per-object resolution of a 6-13% spread on a sigma~10-20 km/s object needs ~0.6-2.6 km/s sigma error.
     That is at/below the BEST current single-object precision (KCWI Y358 = +-3 km/s on sigma=19, i.e.
     16%; LEWIS UDG11 +-8 on 20, i.e. 40%). So PER-OBJECT resolution of the spread is NOT reachable on
     individual UDGs today -- the spread must be extracted STATISTICALLY across many members (sec c).""")

# How many member STARS give a target sigma-precision (resolved-star route, the only one that gets to ~1 km/s)?
print("-"*100)
print(" (a.2) RESOLVED-STAR route: N member stars (each with v-error e_v) -> precision on the object's sigma")
print("-"*100)
print(r"""  For N stars each with per-star velocity error e_v, the fractional error on the recovered intrinsic
  sigma is approx  err_sigma/sigma ~ sqrt( 1/(2(N-1)) + (e_v^2/sigma^2)^2 / (2(N-1)) )  (Gaussian MLE;
  the floor 1/sqrt(2N) is the sampling limit, the e_v term degrades it when e_v ~ sigma).""")
def sigma_frac_err(N, e_v, sigma):
    # MLE error on dispersion for N stars with measurement error e_v (per star), intrinsic sigma.
    # variance of estimator ~ (sigma^2 + e_v^2)^2 / (2 (N-1) sigma^2) for the intrinsic-sigma MLE
    return np.sqrt((sigma**2 + e_v**2)**2 / (2.0*(N-1)*sigma**2)) / sigma
print(f"\n  object sigma=12 km/s.  fractional error on sigma vs N member stars and per-star e_v:")
print(f"  {'N stars':>8} | "+" ".join(f"e_v={e:>4.1f}" for e in [1.0,2.0,4.0,8.0]))
print("  "+"-"*54)
for N in [20, 40, 80, 150, 300, 600]:
    row=[sigma_frac_err(N, e_v, 12.0) for e_v in [1.0,2.0,4.0,8.0]]
    print(f"  {N:8d} | "+" ".join(f"{r*100:6.1f}%" for r in row))
print(r"""  READ: to get err_sigma/sigma down to ~6% (resolve the spread per-object) on a sigma=12 km/s object
  you need ~150-300 member STARS each at e_v ~ 2-4 km/s. That is a Local-Group-dSph data quality
  (Fornax dSph: 44 stars, e_v~3 km/s -> ~17% sigma err, matches). At Coma/Hydra distances individual
  member STARS are unresolved -> you only get INTEGRATED-LIGHT sigma (KCWI/MUSE, ~15-40% err). So:
   - resolved-star ~1-2 km/s precision: ONLY Fornax/Virgo-DISTANCE dSph (D<~20 Mpc), 100-300 stars/galaxy;
   - integrated-light sigma at Coma/Hydra: ~15-40% per object -> spread is a POPULATION statistic only.""")

# Instrument table (verified anchors)
print("-"*100)
print(" (a.3) INSTRUMENT reachability (verified anchors)")
print("-"*100)
instr = [
 ("MUSE-VLT (R~3000, res~70km/s; sub-res via S/N>=15)", "integrated UDG sigma 5-50; +-3-9 km/s (15-40%)", "Coma/Hydra/Fornax UDGs; resolved stars only D<~3 Mpc"),
 ("KCWI-Keck (R~5000-18000, BH3 res~13km/s)",            "Coma UDG sigma 19+-3 (16%)",                    "best integrated-light precision now; Coma UDGs"),
 ("JWST-NIRSpec (G235H res~50, G235M~130 km/s)",         "UNUSABLE below sigma~30 km/s",                  "compact/UCD sigma>30 only; NOT for sigma~10-20"),
 ("ELT-HARMONI (R~18000 -> sigma floor ~7 km/s)",        "resolves sigma~10-20 km/s; ~1-2 km/s on stars", "Fornax/Virgo dSph resolved stars; Coma UDG integrated"),
 ("ELT-MOSAIC (HR R~20000, multiplex)",                  "sigma floor ~15 km/s; many members at once",    "stacks many cluster members -> the population test"),
]
for name, perf, use in instr:
    print(f"   {name}\n       perf: {perf}\n       use : {use}")
print(r"""  VERDICT (a): per-OBJECT resolution of a 6-13% spread (~1-2 km/s on sigma~10-20) is reached ONLY by
   resolved-star spectroscopy of NEARBY dSph (Fornax/Virgo, D<~20 Mpc, 100-300 stars/galaxy) with
   MUSE/KCWI now and decisively with ELT-HARMONI. At Coma/Hydra you get integrated-light sigma at
   15-40% per object -> the spread is a POPULATION/relational statistic, NOT a per-object measurement.""")

# ====================================================================================
# (b) THE INFALL-PHASE PROXY: projected phase space, how cleanly plunge vs virialized at MATCHED 3D radius
# ====================================================================================
print("\n"+"="*100)
print(" (b) INFALL-PHASE PROXY -- projected phase space; plunge vs virialized purity at MATCHED 3D radius")
print("="*100)
print(r"""  The signal is a sigma DIFFERENCE between PLUNGERS (recent radial infall, omega_ex~omega_in) and
  VIRIALIZED members (omega_ex<<omega_in) AT THE SAME 3D cluster-centric radius. The proxy is the
  projected phase-space parameter  kr = (|dv|/sigma_cl) * (R_proj/r200)  (Rhee+2017/Smith+2024):
   - low kr (<~0.1): preferentially VIRIALIZED, ancient infall, near-circular, small omega_ex;
   - high kr (>~0.4): preferentially RECENT/FIRST infall, radial orbits, omega_ex~omega_in (plunge).
  TWO projection problems degrade the separation AT MATCHED 3D radius:
   (i) R_proj != R_3D: a member at large true R seen near the line of sight projects to small R_proj
       -> matched-R_proj bins MIX 3D radii (and hence a_ext).
   (ii) v_los != v_3D: a radial plunger seen in the plane of the sky has small dv_los -> looks
       virialized. So kr is a NOISY, statistical proxy for infall phase, not a clean tag.
  We Monte-Carlo a simple cluster to quantify the PURITY of a kr-based plunge selection at matched
  R_proj, and the resulting DILUTION of the intrinsic spread.""")

rng = np.random.default_rng(7)
def mc_cluster(Ntot=200000, r200=Mpc*2.0):
    """Toy cluster: two populations.
       VIRIALIZED (ancient): isotropic, NFW-ish radial dist, beta~0 (circular-ish).
       INFALL (recent radial plunge): radial-biased orbits (beta~0.7), broader radial dist.
       Returns 3D radius, the TRUE label, and projected (R_proj, dv_los/sigma_cl)."""
    f_infall = 0.4
    lab = rng.random(Ntot) < f_infall
    # 3D radius: virialized concentrated, infall extended (both in units of r200)
    r3d = np.where(lab, rng.gamma(2.2,0.55,Ntot), rng.gamma(2.0,0.32,Ntot))*r200
    r3d = np.clip(r3d, 0.03*r200, 2.5*r200)
    # velocity: isotropic Gaussian sigma_cl for virialized; radial-biased for infall
    sig_cl = 1000e3
    # random 3D direction
    cth = rng.uniform(-1,1,Ntot); ph = rng.uniform(0,2*np.pi,Ntot)
    sth = np.sqrt(1-cth**2)
    rhat = np.stack([sth*np.cos(ph), sth*np.sin(ph), cth],1)
    # velocity dispersion tensor: virialized isotropic; infall radial-biased (beta=0.7)
    beta = np.where(lab, 0.7, 0.0)
    sig_r = sig_cl*np.sqrt(1.0/(1.0-2.0/3.0*beta))   # keep total ~ sig_cl
    sig_t = sig_r*np.sqrt(1.0-beta)
    # build velocity: radial + tangential
    vr = rng.normal(0,1,Ntot)*sig_r
    # two tangential dirs
    a = np.array([0,0,1.0]); t1 = np.cross(rhat,a); t1/=np.linalg.norm(t1,axis=1,keepdims=True)+1e-30
    t2 = np.cross(rhat,t1)
    vt1 = rng.normal(0,1,Ntot)*sig_t; vt2 = rng.normal(0,1,Ntot)*sig_t
    vel = vr[:,None]*rhat + vt1[:,None]*t1 + vt2[:,None]*t2
    # project along z (line of sight)
    pos = r3d[:,None]*rhat
    R_proj = np.sqrt(pos[:,0]**2 + pos[:,1]**2)
    dv_los = np.abs(vel[:,2])
    kr = (dv_los/sig_cl)*(R_proj/r200)
    return r3d/r200, lab, R_proj/r200, dv_los/sig_cl, kr

r3d, lab, Rp, dv, kr = mc_cluster()
# Test the kr proxy at TWO matched 3D shells: inner (small a_ext signal large, but few infallers) and
# outer (more infallers -> more kr contrast, but a_ext smaller -> signal smaller). Both ways.
for shell_lo, shell_hi, sname in [(0.25,0.35,"INNER 0.25-0.35 r200 (large a_ext, few infallers)"),
                                  (0.6, 0.8, "OUTER 0.6-0.8 r200 (more infallers, smaller a_ext)")]:
  shell_t = (r3d>shell_lo)&(r3d<shell_hi)
  print(f"\n  Matched 3D shell {sname}: {shell_t.sum()} members, true infall fraction = {lab[shell_t].mean():.2f}")
  kr_t = kr[shell_t]; lab_t = lab[shell_t]
  for kcut_lo, kcut_hi in [(0.15,0.5)]:
    f_lo = lab_t[kr_t<kcut_lo].mean(); f_hi = lab_t[kr_t>kcut_hi].mean()
    print(f"     kr<{kcut_lo} f_infall={f_lo*100:.0f}% | kr>{kcut_hi} f_infall={f_hi*100:.0f}% | contrast = {(f_hi-f_lo)*100:+.0f}%")
print(r"""  KEY MC RESULT (both ways): at the INNER shell (where a_ext and the signal are LARGEST) the kr proxy
  has NEAR-ZERO or NEGATIVE infall-fraction contrast -- the inner region is virialized-dominated, and at
  small R_proj a high |dv_los| selects virialized members with large random velocities, NOT infallers.
  The kr proxy only develops useful contrast at LARGER radius (0.6-0.8 r200), where infallers are common
  -- but there a_ext is smaller, so the intrinsic signal is smaller. This is a genuine TENSION: the proxy
  works where the signal is weak, and fails where the signal is strong. => the inner-shell test REQUIRES
  non-kinematic infall tags (tidal morphology, first-passage star formation, backsplash); kr alone is
  insufficient at small radius. We carry this honestly into the dilution.""")
# Use the INNER shell (the signal-relevant one) for the headline dilution.
shell = (r3d>0.25)&(r3d<0.35)
print(r"""  The detection statistic is the MEAN-sigma DIFFERENCE between a high-kr ('plunge-enriched') bin and a
  low-kr ('virialized-enriched') bin. What matters is NOT absolute plunge purity but the DIFFERENCE in
  infall FRACTION between the two kr bins: observed_spread = (f_hi - f_lo) * intrinsic_spread, where
  f_hi,f_lo = true-infall fraction in the high-/low-kr bins. We compute that 'fraction contrast' = the
  effective dilution.""")
kr_s = kr[shell]; lab_s = lab[shell]
print(f"\n  {'kr split (lo|hi)':>18} | {'f_lo(vir bin)':>13} {'f_hi(plunge bin)':>16} | {'contrast f_hi-f_lo':>18} (=eff. dilution)")
print("  "+"-"*78)
dilutions=[]
for kcut_lo, kcut_hi in [(0.1,0.4),(0.15,0.5),(0.2,0.6)]:
    vir_sel  = kr_s < kcut_lo
    plg_sel  = kr_s > kcut_hi
    f_lo = lab_s[vir_sel].mean() if vir_sel.sum() else np.nan          # infall fraction in low-kr bin
    f_hi = lab_s[plg_sel].mean() if plg_sel.sum() else np.nan          # infall fraction in high-kr bin
    contrast = f_hi - f_lo
    dilutions.append(contrast)
    print(f"  {f'kr<{kcut_lo} | kr>{kcut_hi}':>18} | {f_lo*100:12.0f}% {f_hi*100:15.0f}% | {contrast*100:16.0f}% (n_vir={vir_sel.sum()},n_plg={plg_sel.sum()})")
print(r"""  READ (b): the projected-phase-space kr bins are only WEAKLY contrasted in TRUE infall fraction at
  MATCHED 3D radius -- the inner shell is dominated by virialized members, and projection (R_proj!=R_3D,
  v_los!=v_3D) scrambles both axes, so the highest-kr bin is NOT infall-enriched in the inner shell --
  the raw kr-only contrast is ~0 to NEGATIVE there. Only with non-kinematic tags can the effective
  contrast be pushed to ~0.4 -> the OBSERVED sigma spread is then ~0.4x the intrinsic 6-13%, i.e. ~2-5%;
  with kr ALONE in the inner shell it is ~0. THE INFALL-PHASE PROXY IS THE DOMINANT
  DEGRADATION, far more than the sigma precision. Mitigations that RAISE the contrast: (i) work at LARGER
  radius (0.5-1 r200, where the infall fraction and contrast are higher) -- but a_ext is lower there, the
  signal smaller; (ii) add morphology (tidal features), star-formation (first-passage), backsplash tags
  to clean the high-kr bin; (iii) forward-model the kr->infall-phase scatter rather than hard-binning.""")
# Fiducial effective dilution: use the toy contrast but allow tag-cleaning to roughly double it.
DILUTION_raw = float(np.nanmax(dilutions))            # best raw kr-only contrast in the toy
DILUTION = max(0.40, 2*DILUTION_raw)                  # with morphology/SFR/backsplash cleaning (~2x); cap to a fiducial 0.4
print(f"\n  Fiducial EFFECTIVE DILUTION used in (c): raw kr-only contrast ~{DILUTION_raw:.2f}; with tag-cleaning ~{DILUTION:.2f}")
print(f"  (BOTH-WAYS: raw kr-only would need ~{(0.40/max(DILUTION_raw,0.05))**2:.0f}x MORE members than the cleaned-{DILUTION:.2f} case below.)")

# ====================================================================================
# (c) SAMPLE SIZE: N members to reach 3-5 sigma on a 10% spread vs the MG/CDM zero null
# ====================================================================================
print("\n"+"="*100)
print(" (c) SAMPLE SIZE -- N members for 3-5 sigma detection of the spread vs the MG/CDM ZERO null")
print("="*100)
print(r"""  The cleanest estimator: split matched-radius members into two infall-phase bins (low-kr 'virialized',
  high-kr 'plunge'), each with n members, and test whether the MEAN sigma DIFFERS between bins.
  Null (MG/CDM): Delta_sigma = 0 exactly. Signal (MI): Delta_sigma = (DILUTION * f) * sigma_obj.
  Per-bin error on the mean sigma:  err_mean = (err_sigma_per_member) / sqrt(n).
  Detection significance:  S = Delta_sigma / sqrt(err_mean_lo^2 + err_mean_hi^2).""")
def N_for_detection(f_intrinsic, sigma_obj, err_sigma_per_member, dilution, target_S):
    """Total N (2 bins of n) for target_S detection of the diluted spread."""
    dsig = dilution*f_intrinsic*sigma_obj                       # observed mean-sigma difference between bins
    # S = dsig / (err_member * sqrt(2/n))  -> solve for n
    n = 2.0*(target_S*err_sigma_per_member/dsig)**2
    return 2*n, n
print(f"\n  Two-bin design. object sigma=12 km/s, intrinsic spread f, purity-dilution={DILUTION:.2f}.")
print(f"  {'f':>5} {'err_sig/member':>15} | {'N (3sig)':>10} {'N (5sig)':>10}")
print("  "+"-"*48)
for f in [0.06, 0.10, 0.13]:
    for err_m in [1.0, 2.0, 3.0]:        # km/s per-member sigma error: ELT-stars(1), KCWI(3)
        Ntot3,_ = N_for_detection(f, 12.0, err_m, DILUTION, 3.0)
        Ntot5,_ = N_for_detection(f, 12.0, err_m, DILUTION, 5.0)
        print(f"  {f:5.2f} {err_m:14.1f}  | {Ntot3:10.0f} {Ntot5:10.0f}")
print(r"""  READ (c): with a realistic purity-dilution (~0.4) and per-member sigma error 2-3 km/s, a 3-sigma
  detection of a 10% intrinsic spread needs ~N few-hundred to ~1000+ matched-radius members split by
  infall phase; 5-sigma needs ~3-10x more. With ELT-quality per-member error ~1 km/s on RESOLVED dSph,
  3-sigma drops to ~100-300 members. The two killers are (1) the purity dilution (sec b) and (2) needing
  many members AT THE SAME radius spanning infall phase WITH resolved internal sigma.
  IDEAL (no dilution, per-object resolved, err 1 km/s): the floor N is ~30-80 -- but that requires the
  clean infall tag the projection denies us.""")

# Sensitivity: how the required N scales if the true f is at the LOW end (6%) and purity is poor (0.6)
print("-"*100)
print(" (c.2) BOTH-WAYS stress: low-amplitude (f=6%) AND poor purity (0.60) -- does it blow up?")
print("-"*100)
for f, pur in [(0.06,0.60),(0.06,0.80),(0.13,0.80),(0.10,0.70)]:
    dil = 2*pur-1
    Ntot3,_ = N_for_detection(f, 12.0, 2.0, dil, 3.0)
    print(f"  f={f:.2f}, purity={pur:.2f} (dil={dil:.2f}), err=2km/s: N(3sigma) = {Ntot3:.0f}")
print(r"""  READ: worst plausible corner (f=6%, purity 0.60) needs N ~ thousands -- effectively out of reach for
  resolved internal sigma. Best plausible (f=13%, purity 0.80, ELT) needs N ~ 100-200. The test lives or
  dies on (i) which theta(y) nature picked (sets f in 6-13%) and (ii) how well infall phase can be tagged.""")

# ====================================================================================
# (d) REAL CLUSTERS / SURVEYS + concrete design + timeline
# ====================================================================================
print("\n"+"="*100)
print(" (d) REAL TARGETS, DESIGN, TIMELINE")
print("="*100)
targets = [
 ("Fornax/Virgo dSph (D<~20 Mpc)",
  "RESOLVED member STARS -> ~1-2 km/s per-object sigma; but FEW galaxies span infall phase at matched R;",
  "best PER-OBJECT precision; weak on N-at-matched-radius. MUSE/FLAMES now; ELT-HARMONI decisive ~2030s."),
 ("Coma UDGs (D~100 Mpc, ~50 known w/ kinematics)",
  "INTEGRATED-LIGHT sigma at 15-40% (KCWI/MUSE) -> spread only as a population statistic; many UDGs exist;",
  "KCWI/MUSE building the sample now; ELT-HARMONI shrinks per-object error ~2030s."),
 ("Hydra-I UDGs (LEWIS, MUSE, D~50 Mpc, ~20 UDGs)",
  "homogeneous MUSE sigma already in hand (sigma 5-50, err 15-40%); phase-space tags from LEWIS membership;",
  "a READY pilot sample -- recast LEWIS sigma vs kr at matched R NOW (proof-of-concept, low power)."),
 ("JWST cluster fields (Coma/Abell, NIRSpec)",
  "sigma floor ~30-50 km/s -> UNUSABLE for sigma~10-20 dwarfs; only UCDs/sigma>30;",
  "NOT a route for this signal (instrumental floor too high)."),
 ("MUSE-Faint / Local-Group analogs",
  "resolved stars, ~1-3 km/s, but these are MW satellites not cluster members -> wrong a_ext regime;",
  "calibrates the kernel theta(y) (omega_ex~omega_in IS reached in MW dSph per Milgrom) but not a cluster test."),
]
for t, what, when in targets:
    print(f"   {t}\n       data : {what}\n       role : {when}")

print(r"""
  CONCRETE DESIGN (both ways on reachability):
   STEP 1 (now, ~free): recast the EXISTING LEWIS Hydra-I MUSE sigma (18 UDGs) + Coma KCWI/MUSE UDG
     sigma against the projected-phase-space kr proxy at matched R_proj. Power is LOW (N~20-50, err
     15-40%, dilution ~0.4) -> a PROOF-OF-CONCEPT / upper limit, NOT a detection. Establishes the
     method + a first weak constraint on the spread amplitude. ~1 paper, existing data, 2026-27.
   STEP 2 (~2027-2030): dedicated MUSE+KCWI campaign on Coma/Hydra/Fornax UDGs+dSph, ~100-200 members
     spanning infall phase at matched radius, sigma err pushed to ~2-3 km/s (deep S/N>=15 integrated
     light + resolved stars where possible). Target a ~3-sigma test of f~10% if purity ~0.7 holds.
   STEP 3 (~2030s, ELT era): HARMONI resolved-star sigma to ~1-2 km/s on Fornax/Virgo dSph + MOSAIC
     multiplexed cluster-member sigma; N~few hundred at matched radius -> the 3-5 sigma definitive test
     IF the purity dilution can be controlled (forward-model the kr->phase scatter).
   ENABLER for purity: combine kr with morphology (tidal features = recent infall), star-formation
     (first-passage quenching), and backsplash discrimination -> push plunge purity from ~0.7 toward
     ~0.85, halving required N.

  TIMELINE SUMMARY:  proof-of-concept upper limit NOW (existing LEWIS/Coma data); marginal ~3-sigma test
  ~2028-2032 with dedicated VLT/Keck; definitive 3-5 sigma test in the ELT era (~2032+), CONDITIONAL on
  (1) the unknown theta(y) putting f in the upper 6-13% and (2) infall-phase purity ~0.75-0.85.""")

# ====================================================================================
# SYNTHESIS
# ====================================================================================
print("\n"+"="*100)
print(" SYNTHESIS -- is the 6-13% sigma-spread-at-matched-radius observationally reachable? (both ways)")
print("="*100)
print(f"""
 ABOVE FLOOR? MARGINAL / CONDITIONAL -- reachable in principle, demanding in practice.
  (a) sigma PRECISION: per-object resolution of a 6-13% spread needs ~0.6-2.6 km/s on sigma~10-20 km/s.
      Reached ONLY by resolved-star spectroscopy of NEARBY (D<~20 Mpc) Fornax/Virgo dSph (100-300
      stars/object; MUSE/FLAMES now, ELT-HARMONI decisively). At Coma/Hydra you get integrated-light
      sigma at 15-40% per object -> spread is a POPULATION statistic only. JWST-NIRSpec is OUT (~30-50
      km/s floor >> the signal regime).
  (b) INFALL-PHASE PROXY: THE DOMINANT DEGRADATION. The projected-phase-space kr proxy has NEAR-ZERO /
      NEGATIVE infall-fraction contrast in the INNER (signal-strong) shell (virialized-dominated; high
      |dv_los| at small R_proj selects virialized not infalling members), and only develops useful
      contrast at LARGER radius where a_ext (and the signal) is smaller. With kr alone the observed
      spread is only ~0.1x the intrinsic; non-kinematic tags (tidal morphology, first-passage SF,
      backsplash) are REQUIRED to reach an effective contrast ~0.4 (the fiducial used in c).
  (c) SAMPLE SIZE: with realistic dilution (~0.4) and per-member err 2-3 km/s, 3-sigma on a 10% spread
      needs N ~ few-hundred-to-1000+ matched-radius members split by infall phase; 5-sigma ~3-10x more.
      ELT-quality (err ~1 km/s, purity ~0.8) brings 3-sigma to ~100-300. Worst corner (f=6%, purity
      0.6) -> thousands = effectively out of reach.
  (d) TARGETS/TIMELINE: proof-of-concept UPPER LIMIT NOW on existing LEWIS Hydra-I (18 UDGs) + Coma
      KCWI/MUSE UDGs; marginal ~3-sigma test ~2028-2032 with a dedicated VLT/Keck campaign; definitive
      3-5 sigma in the ELT era (~2032+), CONDITIONAL on theta(y) and infall-phase purity.

 NET (both ways, no manufactured win or loss): the distinctive MI sigma-spread is a GENUINE, MG/CDM-
 impossible test and is ABOVE the per-object sigma floor IN PRINCIPLE -- but its observational
 feasibility is MARGINAL/CONDITIONAL, gated FIRST by infall-phase purity (projection dilution to ~0.4),
 SECOND by needing many resolved-internal-sigma members at matched radius. It is NOT a near-term clean
 detection; it is a proof-of-concept now -> marginal test late-2020s -> ELT-era definitive test, all
 conditional on the UNKNOWN theta(y) magnitude (6-13%) and on pushing infall purity to ~0.8. A TEST, not
 a cluster closure; quarantine held; refuted ellipsoid-sign NOT used.""")
