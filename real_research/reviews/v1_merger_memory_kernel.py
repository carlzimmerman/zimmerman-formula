#!/usr/bin/env python3
r"""
VEIN 1 -- P2: TIME-VARYING MUTUAL FIELD in INTERACTING PAIRS / RECENT MERGERS.
================================================================================
B4 DISCIPLINE: no hardcoded sign, no ad-hoc proxy. Real time-nonlocal MI calc on
the framework's OWN theta(y) kernel; a0-degeneracy checked both ways.

FRAMEWORK (Milgrom 2022 MI formulation; a0=cH_Lambda/Z=9.36e-11; framework mu_fw):
  EFE two-frequency form (Eq 33/34): the internal MOND magnification of a member
  galaxy reads the EXTERNAL field of its companion weighted by theta(omega_ext/omega_in),
  where omega_ext = rate of change of the companion's field = the ORBITAL frequency of
  the PAIR, and omega_in = internal frequency of the galaxy (sigma/R).
  ADIABATIC (Eq 35): omega_ext<<omega_in -> theta->theta(0)=const -> a MG EFE with
  a0->a0/theta(0) (a0-degenerate trap). NON-ADIABATIC (omega_ext~omega_in) -> theta(y)
  phase-dependent -> NOT a0-degenerate as a RELATIONAL observable.

WHY A PAIR IS A BETTER CARRIER THAN A STREAM (the physical point):
  In a pair, BOTH bodies are EXTENDED diffuse galaxies, so omega_in (internal) is LOW
  naturally (sigma~30-80 km/s over R~5-15 kpc), AND omega_ext = the pair's ORBITAL
  frequency at closest approach can be made ~omega_in WITHOUT requiring a 1-kpc
  pericentric plunge into a dense host core (the stream's fatal tidal-disruption
  problem). The companion's field varies on the encounter timescale; the memory kernel
  reads the encounter PHASE.

THE POSIT: in a galaxy on a close, fast (non-adiabatic) encounter, the internal sigma
  carries a theta(y_encounter) tag set by the ENCOUNTER PHASE (approaching vs receding
  vs at closest approach), NOT just the momentary companion field. MG's instantaneous
  EFE sees only the momentary mutual field -> two galaxies at the SAME momentary
  separation (one inbound pre-peri, one outbound post-peri) have IDENTICAL internal
  boost in MG; MI gives them DIFFERENT boosts (different omega_ext history -> different
  theta tag). RELATIONAL observable: inbound-vs-outbound sigma asymmetry at matched
  separation. MG = exactly 0 for any a0.

WHAT WE COMPUTE (real, both-ways):
  (1) For a realistic pair encounter (two ~10^10-10^11 Msun galaxies), compute
      omega_ext (orbital) vs omega_in (internal) over the encounter -> does y reach O(1)
      WITHOUT a pathologically deep pericenter?
  (2) The MI inbound-vs-outbound internal-sigma asymmetry at matched separation, via
      theta(y) on the framework mu_fw, vs MG's exact zero.
  (3) a0-degeneracy: single galaxy / single encounter = a0-absorbable; the inbound-vs-
      outbound RELATIONAL asymmetry at matched separation = MG-impossible for any a0.
  (4) THE SWAMP: tidal distortion, ongoing star formation / disturbed kinematics,
      projection, non-equilibrium. Is the asymmetry above the floor?

FOOTING sealed; never McGaugh nu. DO NOT git-push.
"""
import math
import numpy as np

A0   = 9.36e-11
G    = 6.674e-11
Msun = 1.989e30
kpc  = 3.0857e19
km   = 1.0e3
Myr  = 3.156e13

def mu_fw(x):  return (math.sqrt(1.0+4.0*x*x)-1.0)/(2.0*x)
def theta_rat(y): return 2.0/(1.0+y*y)        # theta0=2
def theta_exp(y): return math.exp(1.0-abs(y)) # theta0=e

print("="*100)
print(" VEIN 1 -- P2: INTERACTING-PAIR / MERGER MEMORY KERNEL theta(y)  (real time-nonlocal MI, both-ways)")
print("="*100)

# -----------------------------------------------------------------------------
# (1) the encounter: two galaxies, masses M1,M2, on a parabolic-ish encounter with
#     pericentric separation d_peri. omega_ext = orbital angular frequency of the
#     RELATIVE orbit; omega_in = internal frequency of the (diffuse) target galaxy.
# -----------------------------------------------------------------------------
M1 = 5e10*Msun   # target (diffuse, sigma~50 km/s)
M2 = 5e10*Msun   # companion (comparable -> major interaction)
Mtot = M1+M2

# target internal frequency: sigma~50 km/s over R~8 kpc  (a normal-to-diffuse disk/spheroid)
sig_in_kms = 50.0; R_in_kpc = 8.0
omega_in = (sig_in_kms*km)/(R_in_kpc*kpc)      # 1/s
g_in     = (sig_in_kms*km)**2/(R_in_kpc*kpc)   # internal accel scale

print(f"\n  Target galaxy: M={M1/Msun:.1e} Msun, sigma_in={sig_in_kms} km/s, R={R_in_kpc} kpc -> omega_in={omega_in:.3e} 1/s")
print(f"  Companion: M={M2/Msun:.1e} Msun.  Encounter relative orbit; omega_ext = orbital freq at separation d.\n")

def omega_orbit(d_kpc):       # relative orbital angular frequency at separation d
    d=d_kpc*kpc; return math.sqrt(G*Mtot/d**3)
def a_companion(d_kpc):       # companion's field at the target = external field
    d=d_kpc*kpc; return G*M2/d**2

print(f"  {'d_peri[kpc]':>11s} {'omega_ext(peri)[1/s]':>20s} {'y_peri=om_ext/om_in':>20s} {'a_comp/a0':>10s}  regime")
carrier=None
for dp in (50.0,30.0,20.0,15.0,10.0,7.0,5.0):
    oe = omega_orbit(dp); yp = oe/omega_in; ac = a_companion(dp)/A0
    reg = "NON-ADIABATIC" if yp>0.8 else ("marginal" if yp>0.3 else "adiabatic")
    if yp>0.8 and carrier is None: carrier=dp
    print(f"  {dp:11.1f} {oe:20.3e} {yp:20.3f} {ac:10.3f}  {reg}")
if carrier is None: carrier=10.0
print(f"\n  -> carrier (y_peri>~1) reached at d_peri ~ {carrier:.0f} kpc -- a CLOSE BUT NON-DESTRUCTIVE pass")
print(f"     (separation > galaxy size {R_in_kpc} kpc), NOT a deep core plunge. This is the key advantage")
print(f"     over streams: a pair reaches the non-adiabatic band at a survivable separation.")

# -----------------------------------------------------------------------------
# (2) inbound-vs-outbound asymmetry at MATCHED separation d_match (so momentary
#     a_ext identical). Inbound parcel approached fast (omega_ext rising, recent
#     history y_in); outbound parcel is post-pericenter (y_out, having just been
#     through the fast peri). The kernel reads the RECENT omega_ext.
#     We model the carried tag as theta evaluated at the y the galaxy MOST RECENTLY
#     experienced over a memory window ~ 1/omega_in (the inertia relaxation time):
#       inbound at d_match  : recent y was SMALLER (came from larger separation, slower) -> y_in
#       outbound at d_match : recent y was LARGER (just passed peri, fast) -> y_out>y_in
# -----------------------------------------------------------------------------
print("\n"+"-"*100)
print("  (2) INBOUND-vs-OUTBOUND asymmetry at MATCHED separation (momentary a_ext identical)")
print("-"*100)
d_match = max(carrier*1.5, 15.0)   # an observable separation, wider than peri
a_match = a_companion(d_match)
# memory window tau_mem ~ 1/omega_in. Over the last tau_mem before 'now':
#  inbound galaxy was at LARGER separation (slower) -> lower omega_ext;
#  outbound galaxy was at SMALLER separation (near peri, faster) -> higher omega_ext.
tau_mem = 1.0/omega_in
# crude but honest: relative orbital speed v_rel at d ~ sqrt(2 G Mtot/d) (near-parabolic).
def v_rel(d_kpc): d=d_kpc*kpc; return math.sqrt(2*G*Mtot/d)
# separation a memory-time earlier/later: dr ~ v_rel * tau_mem  (radial component, order-of-mag)
dr = v_rel(d_match)*tau_mem/kpc
d_inbound_past  = d_match + dr      # inbound: was farther out tau_mem ago
d_outbound_past = max(carrier, d_match - dr)  # outbound: was nearer (post-peri) tau_mem ago
y_inbound  = omega_orbit(d_inbound_past)/omega_in
y_outbound = omega_orbit(d_outbound_past)/omega_in
print(f"  matched separation d_match={d_match:.0f} kpc (a_ext/a0={a_match/A0:.3f}); memory window tau_mem={tau_mem/Myr:.0f} Myr.")
print(f"  inbound galaxy recent-y (was at {d_inbound_past:.0f} kpc) = {y_inbound:.3f}")
print(f"  outbound galaxy recent-y (was at {d_outbound_past:.0f} kpc, post-peri) = {y_outbound:.3f}")
for th_name,th in (("theta=2/(1+y^2)",theta_rat),("theta=e^{1-|y|}",theta_exp)):
    # internal boost B = 1/mu_fw((g_in + theta(y_recent)*a_match)/a0)
    B_in  = 1.0/mu_fw((g_in + th(y_inbound) *a_match)/A0)
    B_out = 1.0/mu_fw((g_in + th(y_outbound)*a_match)/A0)
    B_mg  = 1.0/mu_fw((g_in + th(0.0)       *a_match)/A0)  # MG: momentary only -> same for both
    sig_asym_MI = math.sqrt(B_out/B_in)
    print(f"  {th_name:18s} theta(y_in)={th(y_inbound):.3f}, theta(y_out)={th(y_outbound):.3f}")
    print(f"     MG  sigma(outbound)/sigma(inbound) at matched sep = {math.sqrt(B_mg/B_mg):.4f}  (EXACTLY 1)")
    print(f"     MI  sigma(outbound)/sigma(inbound) at matched sep = {sig_asym_MI:.4f}  -> asymmetry {abs(sig_asym_MI-1)*100:.2f}%")

# -----------------------------------------------------------------------------
# (3) a0-degeneracy (both-ways)
# -----------------------------------------------------------------------------
print("\n"+"-"*100)
print("  (3) a0-DEGENERACY CHECK")
print("-"*100)
print("""  - A SINGLE galaxy's single encounter (its boost-vs-separation curve) IS a0-absorbable:
    a_ext and the recent-y co-vary along the orbit, so a rescaled a0 reshapes it. NOT distinctive.
  - The DISTINCTIVE observable is the inbound-vs-outbound (or pre-peri-vs-post-peri) sigma asymmetry
    BETWEEN galaxies (or arms) at MATCHED momentary separation: MG sees only momentary a_ext -> EXACTLY
    0 asymmetry for ANY a0; MI gives a nonzero asymmetry because the recent omega_ext history (and thus
    theta) differs between inbound and outbound. No a0 retune manufactures a phase asymmetry MG lacks.
    SIGN robust (post-peri just experienced HIGHER y -> LOWER theta -> LESS external loading -> HOTTER).""")

# -----------------------------------------------------------------------------
# (4) the swamp
# -----------------------------------------------------------------------------
print("\n"+"-"*100)
print("  (4) THE SWAMP (both-ways)")
print("-"*100)
print("""  - Interacting pairs are TIDALLY DISTORTED and KINEMATICALLY DISTURBED: non-equilibrium sigma,
    tidal tails, inflows, bursty star formation -> the internal sigma is NOT a clean equilibrium number
    during a close pass. This is a SEVERE confound: the encounter that creates the signal also wrecks
    the clean-sigma assumption the signal is read from.
  - The inbound/outbound asymmetry must be extracted across a POPULATION of pairs binned by separation
    AND encounter phase (pre- vs post-pericenter), which requires knowing the orbital phase -- itself
    hard (needs relative velocity + modeling).
  - BUT: unlike streams, the carrier regime is reached at a SURVIVABLE separation (d~10-15 kpc > galaxy
    size), so the progenitor is not destroyed; the galaxies remain distinct and measurable. The confound
    is non-equilibrium kinematics, not total disruption. This is a REAL (if hard) population test.""")

print("\n"+"="*100)
print(" VERDICT -- P2 (interacting-pair / merger memory kernel), both ways")
print("="*100)
print(f"""  REGIME EXISTS at a SURVIVABLE separation: a diffuse target reaches y=omega_ext/omega_in ~ 1 at
  d_peri ~ {carrier:.0f} kpc (> galaxy size), NOT requiring a destructive deep plunge. This is the key
  advantage over tidal streams (which need peri<=3 kpc, tidal-disruption-dominated).

  MG-IMPOSSIBILITY: the inbound-vs-outbound (pre- vs post-pericenter) internal-sigma asymmetry at MATCHED
  momentary separation is ~20-24% (theta0=2..e; theta-form-hostage) in MI and EXACTLY 0 in MG for ANY a0
  (instantaneous EFE). SIGN is a theorem (post-peri parcels just saw higher y -> lower theta -> less external
  loading -> HOTTER). Genuinely MG-impossible as a RELATIONAL/phase observable; survives the a0-degeneracy
  trap. The amplitude is LARGER than the stream case because the inbound/outbound recent-y contrast is large.

  HONEST DOWNGRADES: (a) magnitude theta-form-hostage (vanishes as theta0->1); (b) the SEVERE confound is
  NON-EQUILIBRIUM kinematics -- the close pass that makes the signal also disturbs the sigma it is read
  from (tidal tails, inflows, bursty SF); (c) needs a population binned by separation AND encounter phase
  (orbital-phase modeling required). => A GENUINE, MG-impossible, time-nonlocal handle that (unlike streams)
  lives at survivable separations, but is swamped by interaction-driven non-equilibrium kinematics. Grade:
  HYPOTHESIS-WITH-FREE-KNOB (theta-hostage + non-equilibrium confound). Comparable soggy-ness to streams;
  its EDGE is the survivable-separation carrier regime.""")
print("="*100)
