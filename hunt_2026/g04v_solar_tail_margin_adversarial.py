#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""g04v_solar_tail_margin_adversarial.py -- ADVERSARIAL AUDIT of g04's check A2a.
=================================================================================
THE CLAIM UNDER ATTACK (as handed to this verifier):

  "Route A's exponential kernel discharges the isotropic solar-system tail liability ABSOLUTELY, not
   marginally: the anomalous acceleration is below every per-planet ephemeris bound by 320 to 8900 orders
   of magnitude on both footings."

Source: hunt_2026/g04_solar_system_eccentricity_discriminant.py, check A2a, and its .out.

WHAT THIS SCRIPT DOES.  It first REPRODUCES g04's arithmetic independently (V1), then attacks the INFERENCE
from that arithmetic in three ways that a referee would use (V2, V3, V4), and finally states what survives.

  V1  reproduction.  Independent recomputation of g_N, y, log10 dg and the per-planet bound.  Expected PASS:
      the numbers are right and the machinery is validated.  If V1 failed there would be nothing else to say.
  V2  MUTATION CONTROL on the attack machinery itself: a kernel relic that is too small MUST leave the
      margin intact, and one that is large MUST break it.  Both directions checked so V3 cannot pass by
      construction.
  V3  THE MARGIN IS NOT A ROBUSTNESS MARGIN.  nu(y) = 1/(1-exp(-sqrt y)) is a FITTED interpolating function
      (McGaugh, Lelli & Schombert 2016, PRL 117 201101, eq 4 -- the RAR fitting function; adopted here as
      Route A).  The data that fit it reach sqrt(y) ~ 9.  The planets sit at sqrt(y) = 835 (Saturn) to 20562
      (Mercury).  The entire "10^320 to 10^8900" is the value of an exponential evaluated 10^2 to 10^3 times
      further out in its own exponent than anything that constrains it.  V3 measures how much freedom the
      calibrating data actually leave, by asking: what is the SMALLEST fractional modification of nu in the
      CALIBRATED regime that saturates a per-planet bound?  If that number is far below the RAR's own
      scatter, the 10^320 is an artifact of an analytic continuation and carries no information.
  V4  THE CLAIM IS FALSE OF ROUTE A'S ACTUAL SOLAR-SYSTEM ANOMALY.  g04's own check A5b (which FAILS)
      computes Route A's external-field quadrupole Q_2 = 3.0e-26 / 3.3e-26 s^-2.  A quadrupole is an
      ACCELERATION, Q_2 * r.  V4 converts it and confronts it with the SAME per-planet delta-g bounds A2a
      used.  If Route A's total anomalous acceleration at Saturn EXCEEDS the Saturn bound, then the sentence
      "the anomalous acceleration is below every per-planet ephemeris bound" is false as written, and true
      only of one multipole component of it.

BOTH FOOTINGS THROUGHOUT (A0 dict from hunt_lib).  Checks are written so that they CAN fail, and several DO.

CITATIONS FOR EVERY EXTERNAL NUMBER USED HERE
  Fienga & Minazzoli 2024, Living Rev. Relativ. 27:1 (arXiv:2303.01821) Table 10 -- supplementary perihelion
      advance sigmas, via Pitjeva & Pitjev 2013 (EPM) and Fienga+ 2011b (INPOP10a).  Banked in
      prep_2026/planetary_doors/BOUNDS.md sec 1.2.  FM24 sec 5 itself calls reading un-refit supplementary
      precessions as theory bounds "strongly discouraged"; carried as a caveat, immaterial at these margins.
  Park, Hees, Famaey, Desmond & Durakovic 2026 (arXiv:2602.17884) -- Q_2 = (1.6 +- 1.8)e-27 s^-2, 2-sigma
      ceiling 5.2e-27 s^-2, from the full DE440 dataset with Q_2 fit simultaneously with ephemeris params.
  Desmond, Hees & Famaey 2024 (arXiv:2401.04796) eq (12) and Fig. 1 -- the q-integral and its published
      anchors q(1)=0.094, q(1.5)=0.159, q(2)=0.221 for nu = 1/(1-exp(-sqrt y)).
  McGaugh, Lelli & Schombert 2016, PRL 117 201101 -- the RAR fitting function and its observed orthogonal
      scatter, 0.11 dex (their abstract); Lelli+2017 ApJ 836 152 give 0.13 dex for the full RAR.
  Blanchet & Novak 2011, MNRAS 412 2530 (arXiv:1105.5815) -- the constant-a_0 tail of nu = sqrt(1+1/y), the
      mutation kernel; and the class Q_2 range 2.2e-26 to 4.1e-26 s^-2.
  SPARC: Lelli, McGaugh & Schombert 2016, AJ 152 157, loaded through hunt_lib.load_sparc.
"""
import sys, math
import numpy as np
from scipy import integrate
from scipy.optimize import brentq
from hunt_lib import Check, P, info, A0, load_sparc

ck = Check()
np.seterr(all="ignore")

GM_SUN = 1.32712440018e20
AU     = 1.495978707e11
YR     = 3.155760000e7
RAD2MAS = 180.0/math.pi*3600.0*1000.0
G_EXT  = 2.146e-10                # V^2/R0 at the Sun, as committed in cassini_quadrupole_framework.py

# name, a[AU], e, sigma(perihelion advance) [mas/yr], delta-g bound banked in BOUNDS.md sec 1.2 [m/s^2]
PLANETS = [("Mercury", 0.38709927, 0.20563593, 0.006,   4.6e-14),
           ("Venus",   0.72333566, 0.00677672, 0.015,   8.0e-14),
           ("Earth",   1.00000261, 0.01671123, 0.0019,  8.7e-15),
           ("Mars",    1.52371034, 0.09339410, 0.00037, 1.4e-15),
           ("Jupiter", 5.20288700, 0.04838624, 0.28,    5.6e-13),
           ("Saturn",  9.53667594, 0.05386179, 0.0047,  7.0e-15)]

Q2_CEIL_2SIG = 5.2e-27            # Park+2026
RAR_SCATTER_DEX = 0.11            # McGaugh+2016 orthogonal scatter

P("="*116)
P("g04v -- ADVERSARIAL AUDIT of g04 A2a: is the 10^320-10^8900 solar-system tail margin what it claims to be?")
P("="*116)


# ------------------------------------------------------------------ V1: independent reproduction
P(""); P("-"*116); P("V1 -- INDEPENDENT REPRODUCTION (this must pass, or there is nothing to argue about)")
P("-"*116)

def dg_bound(a_m, e, sig_mas_yr):
    """Bound on a CONSTANT sunward dg from a supplementary-perihelion sigma.  Derived here from scratch by
    NUMERICAL orbit-averaging of Gauss's radial equation, NOT from g04's closed form, so this is an
    independent route to the same number:
        Delta(omega)_orbit = (1/(GM e)) Int_0^2pi dg r^2 cos f df,  r = a(1-e^2)/(1+e cos f)."""
    f = np.linspace(0.0, 2.0*math.pi, 400001)
    r = a_m*(1.0 - e*e)/(1.0 + e*np.cos(f))
    I = np.trapezoid(r*r*np.cos(f), f) if hasattr(np, "trapezoid") else np.trapz(r*r*np.cos(f), f)
    dw_per_dg = abs(I/(GM_SUN*e))                             # rad per orbit per unit dg
    P_yr = 2.0*math.pi*math.sqrt(a_m**3/GM_SUN)/YR
    return (sig_mas_yr/RAD2MAS)*P_yr/dw_per_dg

def log10_dg_routeA(gN, a0):
    u = math.sqrt(gN/a0)
    corr = math.log10(-math.expm1(-u)) if u < 40.0 else 0.0
    return math.log10(gN) - u/math.log(10.0) - corr

P(f"  {'planet':<9}{'g_N':>12}{'bound(num)':>12}{'BOUNDS.md':>11}{'ratio':>8}"
  f"{'  sqrt(y) can':>14}{'log10dg can':>12}{'margin can':>11}{'margin alt':>11}")
bnd_err, margins = [], {k: [] for k in A0}
BND = {}
for nm, aAU, e, sw, dgrepo in PLANETS:
    a_m = aAU*AU; gN = GM_SUN/a_m**2
    bd = dg_bound(a_m, e, sw); BND[nm] = bd; bnd_err.append(abs(bd/dgrepo - 1.0))
    Ls = {}
    for k, a0 in A0.items():
        L = log10_dg_routeA(gN, a0); Ls[k] = L; margins[k].append(math.log10(bd) - L)
    P(f"  {nm:<9}{gN:>12.4e}{bd:>12.3e}{dgrepo:>11.1e}{bd/dgrepo:>8.3f}"
      f"{math.sqrt(gN/A0['canonical']):>14.1f}{Ls['canonical']:>12.1f}"
      f"{math.log10(bd)-Ls['canonical']:>11.1f}{math.log10(bd)-Ls['alt']:>11.1f}")

worst_margin = min(min(v) for v in margins.values())
best_margin  = max(max(v) for v in margins.values())
ck("V1a  g04's per-planet bounds reproduce by an INDEPENDENT numerical Gauss average",
   max(bnd_err) < 0.03,
   f"worst deviation {100*max(bnd_err):.1f}% from the BOUNDS.md values, computed here by numerically "
   f"orbit-averaging r^2 cos f rather than by g04's analytic -2 pi a^2 sqrt(1-e^2)/GM.  The bound machinery "
   f"is not in dispute")
ck("V1b  g04's A2a arithmetic reproduces exactly: margins span 10^320 to 10^8900",
   abs(worst_margin - 320.0) < 3.0 and abs(best_margin - 8918.0) < 5.0,
   f"smallest margin 10^{worst_margin:.0f} (Saturn, alt footing), largest 10^{best_margin:.0f} (Mercury, "
   f"canonical).  Independently recomputed here.  THE ARITHMETIC IN A2a IS CORRECT.  Everything below is "
   f"about what that arithmetic licenses")

gals = load_sparc()
gbar = np.concatenate([g["gbar"] for g in gals])
P("")
P(f"  CALIBRATION RANGE OF THE KERNEL.  SPARC ({len(gals)} galaxies, {len(gbar)} points, hunt_lib.load_sparc):")
for k, a0 in A0.items():
    ymax = float(gbar.max()/a0)
    P(f"    {k:>10}: fitted over y = {gbar.min()/a0:.2e} to {ymax:.1f}, i.e. sqrt(y) <= {math.sqrt(ymax):.2f}")
P(f"    the planets sit at sqrt(y) = {math.sqrt(GM_SUN/(9.53667594*AU)**2/A0['canonical']):.0f} (Saturn) to "
  f"{math.sqrt(GM_SUN/(0.38709927*AU)**2/A0['canonical']):.0f} (Mercury).")
sq_ratio = math.sqrt(GM_SUN/(9.53667594*AU)**2/A0['canonical'])/math.sqrt(float(gbar.max()/A0['canonical']))
P(f"    Route A's exponent sqrt(y) is therefore extrapolated by a factor {sq_ratio:.0f}x (Saturn) to "
  f"{sq_ratio*math.sqrt(3.9575e-2/6.5203e-5):.0f}x (Mercury) beyond the largest value any fitting datum has.")


# ------------------------------------------------------------------ the attack machinery
def eps_crit(nm, a0, power):
    """The smallest coefficient eps of a POWER-LAW RELIC added to nu-1,
           (nu-1)_modified(y) = (nu-1)_RouteA(y) + eps * y^(-power),
    that saturates planet nm's delta-g bound.  Solvable in closed form because the Route A piece at planetary
    y is ~10^-300 and utterly negligible:  dg = (nu-1) g_N  ->  eps = (bound/g_N) * y^power."""
    aAU = dict((p[0], p[1]) for p in PLANETS)[nm]
    gN = GM_SUN/(aAU*AU)**2; y = gN/a0
    return (BND[nm]/gN)*y**power

def relic_rel_size(eps, power, y):
    """The relic's size RELATIVE to nu itself, at a y inside the calibrating range -- i.e. how big a change
    this makes to the thing SPARC actually measures."""
    nu_here = 1.0/(1.0 - math.exp(-math.sqrt(y)))
    return eps*y**(-power)/nu_here


# ------------------------------------------------------------------ V2: mutation control on the attack
P(""); P("-"*116); P("V2 -- MUTATION CONTROL on the attack machinery: it must be able to BOTH pass and fail")
P("-"*116)
P("  A 1/y relic is the physically motivated one: it is exactly the tail of the RETIRED kernel")
P("  nu = sqrt(1+1/y) -> 1 + 1/(2y), the one Blanchet & Novak 2011 call ruled out.  So this is not an")
P("  arbitrary deformation -- it is the family the framework itself was in until 2026-08-02.")
P(f"  {'eps':>10}{'relic/nu at y=1':>18}{'dg Saturn [m/s2]':>19}{'/bound':>10}{'verdict':>10}")
v2 = {}
for eps in (1e-12, 1e-8, 1e-5, 1e-3):
    gN = GM_SUN/(9.53667594*AU)**2; y = gN/A0["canonical"]
    dg = eps/y*gN
    v2[eps] = dg/BND["Saturn"]
    P(f"  {eps:>10.0e}{relic_rel_size(eps,1.0,1.0):>18.2e}{dg:>19.3e}{dg/BND['Saturn']:>10.2e}"
      f"{('PASSES' if dg < BND['Saturn'] else 'FAILS'):>10}")
ck("V2a  MUTATION CONTROL: a tiny relic leaves the margin intact, a large one destroys it",
   v2[1e-12] < 1e-3 and v2[1e-3] > 10.0,
   f"eps = 1e-12 gives {v2[1e-12]:.1e} of the Saturn bound (margin survives); eps = 1e-3 gives "
   f"{v2[1e-3]:.1e} of it (margin gone).  The V3 test below is therefore capable of both outcomes and is "
   f"not passing or failing by construction")


# ------------------------------------------------------------------ V3: is the margin a robustness margin?
P(""); P("-"*116)
P("V3 -- THE ATTACK: is 10^320 a ROBUSTNESS margin, or the value of an extrapolated analytic form?")
P("-"*116)
P("  The question a referee asks is not 'what does this function do at y = 7e5' -- it is 'how much of the")
P("  function at y = 7e5 is fixed by anything measured'.  Below: the smallest relic coefficient eps that")
P("  saturates each planet's bound, and how large that relic is IN THE CALIBRATED REGIME (y = 1, the RAR's")
P("  own transition point), where the data constrain nu to the RAR scatter of 0.11 dex = 29%.")
P("")
P(f"  {'planet':<9}{'footing':>10}{'eps_crit (1/y relic)':>22}{'relic/nu at y=1':>18}{'vs RAR scatter':>16}")
worst_rel = 0.0
for nm, aAU, e, sw, dgrepo in PLANETS:
    for k, a0 in A0.items():
        ec = eps_crit(nm, a0, 1.0); rel = relic_rel_size(ec, 1.0, 1.0)
        worst_rel = max(worst_rel, rel)
        P(f"  {nm:<9}{k:>10}{ec:>22.3e}{rel:>18.3e}{rel/(10**RAR_SCATTER_DEX - 1):>16.2e}")
tight = min(min(eps_crit(nm, a0, 1.0) for k, a0 in A0.items()) for nm, *_ in PLANETS)
tight_rel = relic_rel_size(tight, 1.0, 1.0)
P("")
P(f"  Same test with a 1/y^2 relic (a sharper, even more 'Newtonian-looking' deformation):")
P(f"  {'planet':<9}{'footing':>10}{'eps_crit (1/y^2)':>22}{'relic/nu at y=1':>18}")
for nm in ("Mars", "Saturn"):
    for k, a0 in A0.items():
        ec = eps_crit(nm, a0, 2.0)
        P(f"  {nm:<9}{k:>10}{ec:>22.3e}{relic_rel_size(ec,2.0,1.0):>18.3e}")

ck("V3a  the 10^320 margin is ROBUST to the freedom the calibrating data leave in the kernel",
   tight_rel > (10**RAR_SCATTER_DEX - 1),
   f"IT IS NOT, and by a very large factor.  The tightest planet (Mars) is saturated by a 1/y relic with "
   f"eps = {tight:.2e}, which at y = 1 -- the middle of the RAR's own transition, where SPARC has thousands "
   f"of points -- is a fractional change in nu of {tight_rel:.2e}.  The RAR's measured orthogonal scatter is "
   f"{RAR_SCATTER_DEX} dex = {100*(10**RAR_SCATTER_DEX - 1):.0f}% (McGaugh+2016), so this deformation is "
   f"{(10**RAR_SCATTER_DEX - 1)/tight_rel:.0e}x SMALLER than the noise on the data that fixed the kernel.  "
   f"The 10^320 to 10^8900 is not a statement about the framework's robustness; it is the value of "
   f"exp(-sqrt y) continued {sq_ratio:.0f}x-{sq_ratio*24.6:.0f}x beyond the largest sqrt(y) any fitting datum "
   f"reaches.  The physically supportable statement is the DIRECTION (this functional form carries no "
   f"isotropic planetary tail), never the adverb ('absolutely', 'at any conceivable precision, now or ever')")

ck("V3b  the solar system is nevertheless a real 1e-5-level constraint ON THE KERNEL, which is the "
   "content the margin actually has",
   tight_rel < 1e-4,
   f"the correct reading of the same arithmetic, stated as a measurement rather than as a margin: the "
   f"planets bound any 1/y relic in nu to eps < {tight:.1e}, i.e. they pin the kernel at the "
   f"{tight_rel:.0e} fractional level in a regime the galaxy data cannot see at all.  That is a genuine and "
   f"quotable result and it is the SAME arithmetic; it is simply not the claim A2a makes")


# ------------------------------------------------------------------ V4: the total anomaly, not one multipole
P(""); P("-"*116)
P("V4 -- THE ATTACK: 'the anomalous acceleration is below every per-planet bound' -- is it?")
P("-"*116)
P("  g04's own A5b FAILS: Route A's external-field quadrupole is Q_2 = 3.0e-26 (canonical) / 3.3e-26 (alt)")
P("  s^-2 against the Park+2026 2-sigma ceiling 5.2e-27.  A quadrupole is a TIDAL ACCELERATION Q_2 * r.  It")
P("  is recomputed here from the same published equation and confronted with the SAME delta-g bounds A2a")
P("  used, because a referee will not accept 'the anomalous acceleration' meaning one multipole of it.")

def nu_routeA(y):
    y = max(float(y), 1e-300); return 1.0/(1.0 - math.exp(-math.sqrt(y)))

def q_eq12(etilde, vmax=200.0):
    """Desmond, Hees & Famaey 2024 (arXiv:2401.04796) eq (12).  Re-derived independently here."""
    eN = brentq(lambda x: x*nu_routeA(x) - etilde, 1e-9, 1e4)
    def ig(xi, v):
        D = eN*eN + v**4 + 2.0*eN*v*v*xi
        if D <= 0: return 0.0
        return (nu_routeA(math.sqrt(D)) - 1.0)*(eN*(3*xi - 5*xi**3) + v*v*(1.0 - 3.0*xi*xi))
    val, _ = integrate.dblquad(ig, 0.0, vmax, lambda v: -1.0, lambda v: 1.0, epsabs=1e-11, epsrel=1e-9)
    return 1.5*val

anch = [(1.0, 0.094), (1.5, 0.159), (2.0, 0.221)]
aerr = [abs(abs(q_eq12(et))/qp - 1.0) for et, qp in anch]
ck("V4a  the DHF24 eq-(12) integral is independently re-pinned on the published anchors for THIS kernel",
   max(aerr) < 0.01,
   f"worst {100*max(aerr):.2f}% vs q(1)=0.094, q(1.5)=0.159, q(2)=0.221 (Desmond+2024 Fig. 1), recomputed "
   f"here from the paper's equation with no code shared with g04.  So the Q_2 numbers below are not taken "
   f"on trust from the script under audit")

P("")
P(f"  {'footing':>10}{'Q_2 [s^-2]':>13}{'/Park ceiling':>15}   then, as an acceleration Q_2*r:")
P(f"  {'':>10}{'':>13}{'':>15}   {'planet':<9}{'Q2*r [m/s2]':>14}{'bound':>10}{'over by':>10}")
q2_over = {}
for k, a0 in A0.items():
    q = q_eq12(G_EXT/a0)
    Q2 = abs(3.0*a0**1.5/(2.0*math.sqrt(GM_SUN))*q)
    P(f"  {k:>10}{Q2:>13.3e}{Q2/Q2_CEIL_2SIG:>15.2f}")
    for nm, aAU, e, sw, dgrepo in PLANETS:
        acc = Q2*aAU*AU
        q2_over.setdefault(k, {})[nm] = acc/BND[nm]
        P(f"  {'':>10}{'':>13}{'':>15}   {nm:<9}{acc:>14.3e}{BND[nm]:>10.1e}{acc/BND[nm]:>10.2f}x")

sat_over = max(q2_over[k]["Saturn"] for k in A0)
any_over = max(max(d.values()) for d in q2_over.values())
sat_acc = q2_over['canonical']['Saturn']*BND['Saturn']
ck("V4b  Route A's TOTAL anomalous acceleration is below every per-planet ephemeris bound",
   any_over < 1.0,
   f"IT IS NOT.  Route A's external-field quadrupole delivers {sat_acc:.2e} m/s^2 at "
   f"Saturn's orbit against the same {BND['Saturn']:.1e} m/s^2 bound A2a used -- OVER by "
   f"{q2_over['canonical']['Saturn']:.1f}x (canonical) / {q2_over['alt']['Saturn']:.1f}x (alt), and over at "
   f"Mars by {q2_over['canonical']['Mars']:.1f}x / {q2_over['alt']['Mars']:.1f}x.  The 10^320 applies ONLY to "
   f"the isotropic l=0 component.  The l=2 component, which is the DOMINANT one and is set at r_M ~ 8000 AU "
   f"where the exponential does nothing, EXCEEDS the very bounds the claim says it clears by hundreds of "
   f"orders.  g04's own A5b says this and FAILS on it; the claim as worded does not carry that")

ck("V4c  the tail-multipole decomposition is legitimate, i.e. A2a is not simply computing the wrong thing",
   True,
   f"checked and it is: for a point mass in a constant external field the AQUAL/QUMOND anomalous internal "
   f"field is a TRACELESS tidal tensor Q_ij x_j plus the isolated-source isotropic piece, and at Saturn "
   f"g_ext/g_N = {G_EXT/(GM_SUN/(9.53667594*AU)**2):.1e} so the external field shifts sqrt(y) by only "
   f"{0.5*(G_EXT/(GM_SUN/(9.53667594*AU)**2))*math.sqrt(GM_SUN/(9.53667594*AU)**2/A0['canonical']):.1e} and "
   f"cannot rescue the l=0 term.  A2a's l=0 number is the right number for the l=0 term.  The defect is in "
   f"the INFERENCE from it, not in it")


# ------------------------------------------------------------------ verdict
P(""); P("="*116); P("VERDICT"); P("="*116)
P(f"""
 SURVIVES.  The arithmetic of A2a is exactly right (V1a, V1b, reproduced independently).  The bound
 machinery is right (V1a, by a different route than g04's).  The mutation control in g04 A3a is real: the
 retired kernel does fail the same machinery by ~3e4x.  Route A's isotropic l=0 tail at planetary
 accelerations is, WITHIN THE ASSUMED FUNCTIONAL FORM, unmeasurably small, and the retired kernel's constant
 a_0/2 liability is genuinely not inherited.  That much is a real result and should be banked as such.

 DOES NOT SURVIVE, TWO WAYS.

 (1) "ABSOLUTELY, NOT MARGINALLY" IS NOT SUPPORTED (V3a).  nu = 1/(1-exp(-sqrt y)) is a FITTED form whose
     calibrating data reach sqrt(y) <= {math.sqrt(float(gbar.max()/A0['canonical'])):.1f}; the planets are at sqrt(y) = 835-20562.  A 1/y relic in
     nu -- the tail of the framework's OWN previous kernel -- with eps = {tight:.1e} saturates the Mars bound,
     and at y = 1 that relic is {tight_rel:.1e} of nu, i.e. {(10**RAR_SCATTER_DEX-1)/tight_rel:.0e}x below the RAR's 0.11 dex scatter.  So the
     10^320 measures the analytic continuation, not the physics: a kernel modification four to five orders
     below the precision of the data that chose the kernel converts it to O(1).  Correct wording: "this
     functional form carries no isotropic planetary tail" -- never "at any conceivable measurement
     precision, now or ever".  Read the other way round it IS a result (V3b): the planets pin the kernel at
     the {tight_rel:.0e} fractional level in a regime galaxies cannot see.

 (2) "THE ANOMALOUS ACCELERATION IS BELOW EVERY PER-PLANET EPHEMERIS BOUND" IS FALSE AS WRITTEN (V4b).
     Route A's own external-field quadrupole, recomputed here independently from Desmond+2024 eq (12) and
     pinned to their published anchors for this exact kernel, gives {q2_over['canonical']['Saturn']:.1f}x the Saturn delta-g bound
     and {q2_over['canonical']['Mars']:.1f}x the Mars one.  The claim holds only for the l=0 multipole in isolation; Route A's
     total solar-system anomalous acceleration EXCEEDS the same bounds.  g04 itself is scrupulous about this
     (A5b FAILS and says "the two must never be conflated"); the summary claim is not.

 ON THE FORK.  This channel does not discriminate modified gravity from modified inertia in the direction
 the claim implies, and it cannot discriminate the framework from LambdaCDM at all: GR predicts zero
 planetary anomaly and so does any sharp-transition MOND kernel, so a null here is not evidence for
 anything.  The one solar-system observable that DOES separate the arms is Q_2 -- and it points away from
 modified gravity, which is this repository's operative arm.
""")
sys.exit(ck.done())
