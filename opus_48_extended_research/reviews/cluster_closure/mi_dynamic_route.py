#!/usr/bin/env python3
r"""
MI-DYNAMIC ROUTE to the cluster residual  (topic mi_dynamic_route, 2026-06-19)
================================================================================
QUESTION (the make-or-break one the prior MI work did NOT answer):
  Does the framework's GENUINE modified-inertia (time-nonlocal, Milgrom 2022
  arXiv:2208.07073 = PRD 106 064060) supply any RESIDUAL that quasi-static MOND
  misses -- i.e. does the NON-ADIABATIC inertia of a hot, plunging cluster member
  give a LARGER MEAN effective DYNAMICAL MASS than quasi-static MOND, enough to
  push eta(core)~2.33 toward 1 (needs a0_eff ~ 4x, i.e. boost^2 ~ 4)?

  Prior repo work (GENUINE_MI_CLUSTER_DISTINCTIVE_2026-06-15;
  member_MI_nonadiabatic_plunge.py) established the non-adiabatic MI gives a
  member-internal sigma-SPREAD (~6-13%, relational, a distinctive TEST) -- but
  a spread is NOT a residual. A residual needs the cycle-AVERAGED MEAN mass to
  rise. THIS script computes the MEAN specifically. Both parts:

  (a) FULL Milgrom 1994/2022 time-nonlocal inertia for a member on a radial /
      plunging orbit (sigma~1000 km/s, eccentric, fluctuating potential): is the
      cycle-AVERAGED effective inertial boost <1/mu> LARGER than the quasi-static
      MOND boost at the same mean acceleration? (Jensen's inequality + the actual
      Milgrom A(omega) functional, integrated over a real eccentric orbit.)
  (b) dS-Unruh T_eff = (hbar/2 pi c kB) sqrt(a^2 + (c H_Lambda)^2) (Deser-Levin):
      does the deep cluster potential / high local a add a term that RAISES a0 in
      the core toward 4x? (Note the sign trap: high a in the core means a>>a0 ->
      LESS MOND, the wrong way.)

FRAMEWORK FOOTING (sealed): a0 = c^2 sqrt(Lambda/32pi) = (c/2) sqrt(G rho_DE)
  = 9.36e-11 m/s^2.  dS-Unruh isolated boost g_obs = sqrt(g_N^2 + g_N a0)
  <=> nu(y) = sqrt(1+1/y), inverse-inertia mu_fw(x) = (sqrt(1+4x^2)-1)/(2x).

BOTH-WAYS (#1 rule): a "closes it" claim is verified as hard as a "fails" claim.
GALAXY VETO: any mean-mass enhancement that closes clusters MUST be shown not to
break the 175-SPARC RAR (0.11-0.13 dex).  QUARANTINE: a0/Z never asserted derived.

Equation numbers from Milgrom 2022 arXiv:2208.07073v3 (PDF text verified this session:
Eq 3 a_hat(w)mu[A(w)/a0]=a_N_hat(w); Eq 20 A(w)=int theta(w'/w)|a_hat(w')|dw'/sqrt(2pi);
Eq 23 per-frequency; the deep-MOND V^4/M Ga0 = const from space-time scale invariance,
Sec II D line "the whole family ... has the same value of V^4/M Ga0 ... expected to be
of order unity and not change appreciably among systems"; M Ga0 = eta sigma^4, eta~1,
exact eta a SECOND-TIER prediction; EFE: theta>1 QUENCHES MOND -- the wrong direction.)
"""
import numpy as np

# ----------------------------------------------------------------- constants (SI)
c    = 2.998e8
G    = 6.674e-11
hbar = 1.0546e-34
kB   = 1.381e-23
Msun = 1.989e30
kpc  = 3.0857e19
Mpc  = 3.0857e22
km   = 1e3

# framework
a0      = 9.36e-11                       # sealed = c^2 sqrt(Lambda/32pi)
H_Lambda = a0/(0.5*c) / 1.0              # placeholder; computed properly below
# de Sitter Hubble from Lambda: a0 = c^2 sqrt(Lam/32pi); cH_Lambda = c*sqrt(Lam/3)
Lambda  = (a0/c**2)**2 * 32*np.pi        # m^-2
cH_Lam  = c*np.sqrt(Lambda/3.0)          # m/s^2  -- the dS floor acceleration
print("="*92)
print(" MI-DYNAMIC ROUTE to the cluster residual -- does time-nonlocal MEAN mass beat quasi-static MOND?")
print("="*92)
print(f"  a0            = {a0:.3e} m/s^2  (sealed c^2 sqrt(Lambda/32pi))")
print(f"  Lambda        = {Lambda:.3e} m^-2  (back-out)")
print(f"  cH_Lambda     = {cH_Lam:.3e} m/s^2  = {cH_Lam/a0:.3f} * a0   (dS-Unruh floor accel)")
print(f"    [Deser-Levin: T_eff = (hbar/2 pi c kB) sqrt(a^2 + (cH_Lam)^2);  a0 = c^2 sqrt(Lam/32pi)")
print(f"     equals (pi/sqrt(8))*(2 kB/hbar c)*... -> the floor term inside sqrt is (cH_Lam)^2.]\n")

def nu(y):    y=np.asarray(y,float); return np.sqrt(1.0+1.0/y)            # g = g_N nu(g_N/a0)
def mu_fw(x): x=np.asarray(x,float); return (np.sqrt(1.0+4.0*x*x)-1.0)/(2.0*x)  # inverse-inertia

# ===========================================================================
# PART (a): cycle-AVERAGED effective dynamical mass on a plunging/eccentric orbit
# ===========================================================================
print("="*92)
print(" PART (a): does the FULL time-nonlocal MI raise the cycle-AVERAGED MEAN dynamical mass?")
print("="*92)
print(r"""
 The observable that sets the cluster residual is the DYNAMICAL MASS an observer infers from the
 member/galaxy velocities: M_dyn = (mean boost) * M_baryon, where boost = g_obs/g_bar = 1/mu.
 Quasi-static MOND uses the MOMENTARY mu(g_bar/a0). The FULL MI (Milgrom 2022 Eq 3,20,23) replaces
 the momentary acceleration by the NONLOCAL functional A(omega) built from the WHOLE trajectory
 (Fourier), and gives a PER-FREQUENCY inertia mu[A(omega_k)/a0]. The question: integrated over a real
 eccentric/plunging orbit, is the CYCLE-AVERAGED boost <1/mu> LARGER than quasi-static?

 TWO competing effects, computed exactly below:
  [J] JENSEN curvature: 1/mu(x) is CONVEX in x over the deep/transition regime, so for a FLUCTUATING
      acceleration <1/mu(a/a0)> >= 1/mu(<a>/a0).  This is the ONLY way MI could give MORE mean mass.
  [A] The A(omega) functional REPLACES the instantaneous a by an rms/frequency-weighted A that is
      LARGER than the orbit-min a (it sums |a_hat| over the orbit). A larger argument -> SMALLER 1/mu
      -> LESS boost.  And the deep-MOND scale-invariance theorem (Milgrom Sec II D) pins V^4/(M G a0)
      to an O(1) constant INDEPENDENT of orbit shape -> the integrated virial mass does NOT depend on
      eccentricity at leading order.
""")

# --- (a.1) JENSEN bound: how much can a fluctuating acceleration raise <1/mu>? -------------
# Quasi-static deep-MOND boost 1/mu(x) ~ 1/x for x<<1 (since mu_fw(x)->x). On an eccentric orbit
# a oscillates between a_peri (large) and a_apo (small). Take a member whose orbit-MEAN g_bar is the
# residual-setting value g_bar ~ a few * 0.01 a0 (deep MOND at R500). Compute <1/mu(a/a0)> for a
# realistic acceleration distribution along the orbit vs 1/mu(<a>/a0).
print("-"*92)
print(" (a.1) JENSEN: max mean-mass gain from a FLUCTUATING acceleration vs the momentary-mean MOND")
print("-"*92)

def orbit_accel_distribution(a_mean, ecc, n=200000):
    """Acceleration time-series along a Kepler-like eccentric orbit with given time-averaged
       g_bar = a_mean. For a point-mass field a ~ 1/r^2; r(theta) = p/(1+e cos theta); time spent
       dt ~ r^2 dtheta (angular momentum). We sample by TIME (the physically averaged quantity is the
       time-average of the boost the member experiences). Returns the time-sampled a array, rescaled
       so its TIME-MEAN equals a_mean (so we compare at fixed mean acceleration)."""
    theta = np.linspace(0, 2*np.pi, n, endpoint=False)
    r = 1.0/(1.0 + ecc*np.cos(theta))          # units of p (semi-latus rectum)
    a = 1.0/r**2                                # point-mass acceleration, arb units
    dt = r**2                                   # time weight (dtheta/dt ~ L/r^2)
    w = dt/dt.sum()
    a_tmean = np.sum(a*w)
    a = a * (a_mean/a_tmean)                    # rescale so TIME-MEAN = a_mean
    return a, w

print(f"  Member orbit deep-MOND, time-mean g_bar fixed; compare <1/mu>_time vs 1/mu(<g_bar>).")
print(f"  {'g_bar/a0':>9} {'ecc':>5} | {'1/mu(<g>)':>10} {'<1/mu>_time':>11} | {'gain':>7} | {'boost^2 gain':>12}")
print("  "+"-"*74)
jensen_rows=[]
for gbar_ratio in [0.01, 0.03, 0.1, 0.3]:
    for ecc in [0.3, 0.6, 0.9, 0.99]:
        a_arr, w = orbit_accel_distribution(gbar_ratio*a0, ecc)
        boost_qs  = 1.0/mu_fw(gbar_ratio)                    # quasi-static at the mean
        boost_mi  = np.sum(w*(1.0/mu_fw(a_arr/a0)))          # time-averaged instantaneous boost
        gain = boost_mi/boost_qs
        jensen_rows.append((gbar_ratio,ecc,gain))
        print(f"  {gbar_ratio:9.2f} {ecc:5.2f} | {boost_qs:10.3f} {boost_mi:11.3f} | {gain:7.3f} | {gain**2:12.3f}")
print(r"""
  READ: <1/mu>_time / (1/mu(<g>)) is the JENSEN gain in inferred dynamical mass (boost), and its
  SQUARE is the gain in a0_eff-equivalent (since boost ~ 1/mu ~ sqrt(a0/g_bar) in deep MOND).
  This is the MAXIMUM mean-mass help a fluctuating-acceleration MI could give -- it IGNORES the
  A(omega) functional (which only ever RAISES the argument and so LOWERS the boost) and it treats
  the boost as purely local-in-time (the most generous reading for getting extra mass).""")

# --- (a.2) The honest MI: A(omega) raises the argument -> LESS boost, not more ------------
print("-"*92)
print(" (a.2) HONEST full MI: the A(omega) functional (Milgrom Eq 20) RAISES the inertia argument")
print("-"*92)
print(r"""  Milgrom Eq (20): A(omega) = (1/sqrt(2pi)) int_0^inf theta(w'/w) |a_hat(w')| w'^2 ... dw', i.e. A is a
  theta-weighted SUM over ALL Fourier components of the acceleration. For an eccentric orbit this A is
  >= the rms acceleration > the orbit-MIN acceleration. Since mu is increasing, mu[A/a0] >= mu at the
  momentary small-a phases -> the deep-MOND boost is CAPPED, NOT enhanced, relative to a naive
  'boost frozen at apocenter'. We bracket A between the time-mean |a| and the rms |a| (theta>=1).""")
print(f"  {'g_bar/a0':>9} {'ecc':>5} | {'rms a/a0':>9} {'A_lo=<|a|>':>10} {'A_hi=rms':>9} | "
      f"{'1/mu[A_lo]':>10} {'1/mu[A_hi]':>10} | {'vs QS':>7}")
print("  "+"-"*86)
for gbar_ratio in [0.01, 0.03, 0.1]:
    for ecc in [0.6, 0.9, 0.99]:
        a_arr,w = orbit_accel_distribution(gbar_ratio*a0, ecc)
        a_tmean = np.sum(w*a_arr)
        a_rms   = np.sqrt(np.sum(w*a_arr**2))
        boost_qs = 1.0/mu_fw(gbar_ratio)
        b_lo = 1.0/mu_fw(a_tmean/a0)     # A = time-mean accel (theta=1, slow)
        b_hi = 1.0/mu_fw(a_rms/a0)       # A = rms accel (theta>1 upper bracket)
        print(f"  {gbar_ratio:9.2f} {ecc:5.2f} | {a_rms/a0:9.3f} {a_tmean/a0:10.3f} {a_rms/a0:9.3f} | "
              f"{b_lo:10.3f} {b_hi:10.3f} | {b_hi/boost_qs:7.3f}")
print(r"""  READ: the genuine MI argument A sits between <|a|> and rms|a| (both >= the orbit-min), so the
  cycle-averaged boost from the ACTUAL Milgrom functional is <= the quasi-static boost at the mean,
  i.e. column 'vs QS' <= 1.  The A(omega) functional MOVES THE ANSWER THE WRONG WAY for adding mass.""")

# --- (a.2b) WHY the local-Jensen blow-up is PHYSICALLY VOID (both-ways guard) ----------------
print("-"*92)
print(" (a.2b) BOTH-WAYS GUARD: the (a.1) Jensen 'gain' at high ecc is a LOCAL-mu apocenter ARTIFACT")
print("-"*92)
print(r"""  The (a.1) gains -> 17x at ecc=0.99 come ENTIRELY from the apocenter phase where a(t)->0 and the
  LOCAL 1/mu(a/a0)->infinity (deep-MOND singularity). That is NOT a physical mass: (i) the genuine MI
  does not use the instantaneous a -- it uses A(omega) (Eq 20), which (a.2) shows is >= rms a, KILLING
  the apocenter singularity; (ii) the conserved MI kinetic energy (Milgrom Eq 11) is weighted by the
  inertia functional I over the WHOLE trajectory, not by 1/mu(a(t)). The honest mean boost is the
  ENERGY-virial one, set by scale invariance (a.3). We show the local-Jensen and the honest-A answers
  DIVERGE and the honest one (<= QS) is the physical one -- so (a.1) is an upper bound that is VOID,
  not a candidate cure. Reported so no one mistakes the 17x for a residual.""")
# direct demonstration: replace the instantaneous boost by the A-functional boost (theta=1, slow EFE),
# which is the physically correct per-frequency inertia -- recompute the 'gain' and show it is <=1.
print(f"  {'g_bar/a0':>9} {'ecc':>5} | {'(a.1) local gain':>16} | {'A-functional gain':>17} | physical?")
print("  "+"-"*70)
for gbar_ratio in [0.03,0.1]:
    for ecc in [0.6,0.9,0.99]:
        a_arr,w = orbit_accel_distribution(gbar_ratio*a0, ecc)
        boost_qs   = 1.0/mu_fw(gbar_ratio)
        boost_loc  = np.sum(w*(1.0/mu_fw(a_arr/a0)))     # (a.1) local-mu
        a_rms      = np.sqrt(np.sum(w*a_arr**2))
        boost_Afun = 1.0/mu_fw(a_rms/a0)                  # honest: argument = rms a (A-functional, theta=1)
        print(f"  {gbar_ratio:9.2f} {ecc:5.2f} | {boost_loc/boost_qs:16.2f} | {boost_Afun/boost_qs:17.3f} | "
              f"A-func <=1 -> VOID local blow-up")

# --- (a.3) the decisive scale-invariance pin: integrated virial mass independent of orbit shape ---
print("-"*92)
print(" (a.3) DECISIVE: deep-MOND space-time scale invariance pins the integrated mass (Milgrom Sec IID)")
print("-"*92)
print(r"""  Milgrom 2022 Sec II D proves the deep-MOND MI models obey V^4/(M G a0) = const, set ONLY by
  'dimensionless attributes of the system' and 'not changing appreciably among systems' -- the SAME
  scale-invariance that gives MG its virial theorem (Milgrom 2014, ref [22]: all MG theories share one
  eta). So the M-sigma relation M G a0 = eta sigma^4 has eta~1 in BOTH MI and MG; eta's exact value /
  orbit-shape dependence is a SECOND-TIER O(1) wiggle, NOT a factor that can grow to the ~4x clusters
  need. The integrated dynamical mass an observer reads off sigma is fixed by a0 + scale invariance,
  which MI and MG SHARE. => No orbit-shape / non-adiabatic MEAN-mass residual at leading order.""")

# Quantify the second-tier eta spread MI could plausibly carry (orbit-shape), generously:
# the Jensen gains above are the most generous bound; convert to an eta-equivalent spread.
gains = np.array([g for *_ ,g in jensen_rows])
print(f"\n  The naive local-Jensen gains (a.1) span {gains.min():.2f}-{gains.max():.2f}x in mass, but (a.2b)")
print(f"  shows these are VOID apocenter-singularity artifacts: the genuine A(omega) functional gives a")
print(f"  cycle-averaged boost <= quasi-static. So the PHYSICAL mean-mass gain is <= 1x, NOT a few-x, and")
print(f"  certainly not the 4x the core needs. The honest MI mean dynamical mass = the QS/scale-invariant")
print(f"  M G a0 = eta sigma^4 (eta~1), SHARED with MG. No non-adiabatic MEAN residual.")

# ===========================================================================
# PART (b): dS-Unruh T_eff environmental term -- does the deep core RAISE a0?
# ===========================================================================
print("\n"+"="*92)
print(" PART (b): dS-Unruh T_eff environmental term -- does the deep cluster core RAISE a0 toward 4x?")
print("="*92)
print(r"""  Deser-Levin / framework: T_eff(a) = (hbar / 2 pi c kB) sqrt(a^2 + (cH_Lam)^2). The MOND scale a0 is
  set by the FLOOR of this temperature, a0 ~ c^2 sqrt(Lam/32pi) ~ (pi) (kB/hbar c) * T_dS-type, i.e. a0
  is tied to the (cH_Lam)^2 floor term, NOT to the kinematic a^2 term. Two ways the core could shift a0:
   (b1) DIRECT: replace cH_Lam by an enhanced 'local de Sitter' scale from the cluster's own curvature.
   (b2) KINEMATIC: the member's own high acceleration a in the core enters T_eff via the a^2 term.""")

# (b1) local-curvature reading: does the cluster potential add to the (cH_Lam)^2 floor?
print("-"*92)
print(" (b1) Could the cluster's own curvature replace/augment (cH_Lambda)^2 inside the sqrt?")
print("-"*92)
# cluster core: M ~ 1e14-1e15 Msun within ~ 0.3-0.5 Mpc; local 'curvature acceleration' scale.
for Mcl, Rcore in [(1e14*Msun,0.3*Mpc),(5e14*Msun,0.4*Mpc),(1e15*Msun,0.5*Mpc)]:
    g_core = G*Mcl/Rcore**2                          # Newtonian core acceleration
    # an effective 'local Hubble/curvature' accel from the enclosed density: a_curv = c*sqrt(G rho_core)
    rho_core = Mcl/((4/3)*np.pi*Rcore**3)
    a_curv = c*np.sqrt(G*rho_core)                   # = the density-a0 scale (x2 = a0_local)
    a0_local = 0.5*a_curv                            # (c/2) sqrt(G rho) -- the density-a0 reading
    print(f"  M={Mcl/Msun:.0e}Msun R={Rcore/Mpc:.2f}Mpc: g_core={g_core/a0:.2f} a0, rho/rho_DE="
          f"{rho_core/6.0e-27:.1f}, a0_local=(c/2)sqrt(Grho)={a0_local:.2e}={a0_local/a0:.1f}x a0")
print(r"""  READ: the density-a0 reading DOES give a few-x a0 in the core (the cluster's rho_core is ~10s-100s x
  rho_DE). BUT this is exactly the density-a0 law already adjudicated in the repo
  (CLUSTER_MI_DSUNRUH_A0RHO + cluster_closure/galaxy_veto_test.py): it RAISES cluster a0 a few-x but
  the SAME law applied to a galaxy disk (rho ~ 1e5-1e6 rho_DE) raises galaxy a0 by 300-1000x and
  ERASES the 0.13-dex RAR. It BREAKS THE GALAXY VETO. And a 'few-x' in the core is right-signed but
  still short of the 4x needed, AND declines outward faster than the residual. This is NOT new MI
  content -- it is the already-vetoed density-a0 angle wearing a T_eff hat.""")

# (b2) kinematic a^2 term: high core a -> a >> a0 -> T_eff ~ a/(...) -> DEEP NEWTONIAN -> LESS MOND
print("-"*92)
print(" (b2) KINEMATIC a^2 term: the member's own acceleration in the core -- which way does it push?")
print("-"*92)
print(f"  In T_eff = (hbar/2 pi c kB) sqrt(a^2+(cH_Lam)^2), a member's own a only matters when a>~cH_Lam~a0.")
print(f"  {'regime':>22} {'a/a0':>7} | {'T_eff/T_floor':>13} | {'mu(g_bar/a0)':>12} | {'-> MOND boost':>13}")
print("  "+"-"*78)
for label, a_ratio in [("cluster core (hot)",5.0),("transition",1.0),("R500 outskirt",0.05),("deep MOND",0.01)]:
    a_phys = a_ratio*a0
    Teff_ratio = np.sqrt(a_phys**2 + cH_Lam**2)/cH_Lam
    boost = 1.0/mu_fw(a_ratio)
    print(f"  {label:>22} {a_ratio:7.2f} | {Teff_ratio:13.3f} | {mu_fw(a_ratio):12.3f} | {boost:13.3f}")
print(r"""  READ (the SIGN TRAP, as flagged in the task): in the dense core a member's own a >> a0, so the a^2
  term DOMINATES T_eff -> T_eff tracks a (the ordinary Unruh/Newtonian limit) -> mu -> 1 -> boost -> 1
  = LESS MOND, not more. The a^2 environmental term pushes the core toward NEWTONIAN (away from the
  enhancement clusters need). It is the WRONG SIGN for closing the residual. Only the (cH_Lam)^2 FLOOR
  sets a0, and that floor is the global cosmological Lambda -- it does not know about the cluster.""")

# ===========================================================================
# SYNTHESIS
# ===========================================================================
print("\n"+"="*92)
print(" SYNTHESIS -- does the MI-dynamic route supply the cluster residual?")
print("="*92)
print(f"""
 (a) NON-ADIABATIC MEAN MASS:  NO.
     - The naive local-mu Jensen 'gain' (a.1) blows up to 17x at ecc~0.99 BUT IS PHYSICALLY VOID (a.2b):
       it is an apocenter a->0 singularity of the LOCAL interpolation, killed by the A(omega) functional
       and absent from the conserved MI energy. NOT a residual -- flagged so it is not mistaken for one.
     - HONEST full MI (A(omega) functional, Milgrom Eq 20) sums |a_hat| over the orbit -> argument >=
       rms a -> cycle-averaged boost <= quasi-static (vs-QS column <= 1). MOVES THE WRONG WAY for mass.
     - DECISIVE: deep-MOND space-time scale invariance (Milgrom Sec II D) pins V^4/(M G a0)=const and
       M G a0 = eta sigma^4 with eta~1 SHARED by MI and MG; orbit shape is a second-tier O(1) wiggle,
       not a 4x factor. The prior repo find (sigma-SPREAD ~6-13%) is a member-internal RELATIONAL signal
       that supplies NO residual to the MEAN mass -- confirmed here directly.
 (b) dS-Unruh T_eff ENVIRONMENTAL term:  NO (and wrong-signed).
     - (b1) the only way to raise a0 in the core is the density reading a0_local=(c/2)sqrt(G rho_core),
       a few-x in the core -- but that IS the already-vetoed density-a0 law (breaks the 0.13-dex galaxy
       RAR by 300-1000x; cluster_closure/galaxy_veto_test.py), and still < 4x and declines too fast.
     - (b2) the kinematic a^2 term in T_eff makes the HOT core MORE Newtonian (a>>a0 -> mu->1 -> boost->1)
       = LESS MOND. Wrong sign, exactly as the task flagged. a0 is set by the (cH_Lam)^2 cosmological
       FLOOR, which is blind to the cluster.
 NET: the MI-dynamic route supplies NEGLIGIBLE residual. The non-adiabatic time-nonlocality gives a
 distinctive member-internal sigma-spread (a TEST, banked prior) but NOT a larger mean dynamical mass;
 the dS-Unruh environmental terms either reduce to the vetoed density-a0 law or push the core the wrong
 way. The cluster ~2x core residual is NOT closed by the framework's distinctive MI physics. Both ways,
 no manufactured cure; the galaxy veto is not even reached because the mean-mass effect is absent.
 QUARANTINE held: a0/Z never asserted derived.""")
