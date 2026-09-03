#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
g04v_adversarial_eccentricity_vacuity_refutation.py -- ADVERSARIAL AUDIT OF g04's B3b CLAIM.
=============================================================================================
THE CLAIM UNDER ATTACK (g04_solar_system_eccentricity_discriminant.py, check B3b, and the headline
sentence carried out of it):

  "The eccentricity discriminant is vacuous inside 100 AU: the modified-gravity precession has no
   magnitude to work with, so the fork cannot be decided by orbit shape in the inner solar system.
   Largest modified-gravity precession rate inside 100 AU at e=0.9: 1.9e-14 mas/yr (a=100 AU),
   against Mars's 0.00037 mas/yr -- shortfall 10^10."

TWO SEPARABLE ASSERTIONS.  They do not stand or fall together, and the audit finds them on opposite
sides of the line:

  (i)  ARITHMETIC.  Route A's ISOLATED-SUN central tail dg = (nu(g_N/a_0)-1) g_N gives an orbit-averaged
       perihelion precession below 2e-14 mas/yr anywhere inside 100 AU at any eccentricity.
       ---> INDEPENDENTLY CONFIRMED HERE (V1), with a different quadrature, a different integration
       variable, and a Gauss equation carrying BOTH radial and transverse components rather than the
       radial-only form g04 uses.

  (ii) INFERENCE.  "...so the fork cannot be decided by orbit shape in the inner solar system."
       ---> REFUTED HERE (V2, V3).  The isolated-Sun tail is NOT the modified-gravity arm's
       solar-system precession signal.  The Sun sits in the Galactic field g_ext = 2.146e-10 m/s^2
       > a_0, and the nonlinear MOND boundary condition imprints a CONSTANT anomalous quadrupole Q_2
       on the whole interior (Milgrom 2009; Blanchet & Novak 2011; Hees+2014; Desmond+2024).  That
       term is NOT exponentially suppressed -- it is set at r_M ~ 8000 AU where y ~ 1 -- it grows as
       Q_2 * r, it is anisotropic, and it precesses perihelia.  g04's OWN Part A computes it: Q_2 =
       3.00e-26 s^-2 for Route A, 5.8x OVER the Park+2026 ceiling.  Fed through the same precession
       machinery, that is ~0.03 mas/yr at Saturn -- SIX TIMES the sharpest Saturn bound, and 1e12
       times the 1.9e-14 mas/yr the B3b sentence calls "the largest modified-gravity precession rate
       anywhere inside 100 AU".

  So the modified-gravity arm has ample precession magnitude inside 100 AU; it is already excluded
  there; and the fork IS decided there, because g04's own committed contrast puts the modified-inertia
  arm at 7.4e-34 s^-2, 1e-7 of the same ceiling.  The B3b arithmetic is sound.  The sentence built on
  it is a statement about ONE term of the modified-gravity solution, promoted to a statement about the
  arm and then about the fork.

THE CONFOUND LENS (the assignment's own question: would ordinary cold dark matter do this?).
  For the B3b null: trivially yes -- GR+CDM predicts zero solar-system anomaly and 1.9e-14 mas/yr is
  zero.  B3b discriminates nothing; it is a consistency statement (V4a, recorded as a FAIL because it
  is a fail).  For the Q_2 channel: NO -- the Newtonian/CDM Galactic tide at the Sun is |dg/dr| ~
  V^2/R_0^2 ~ 9e-32 s^-2, five orders BELOW the Cassini ceiling and 3e5 below the MOND value (V4b).
  So the one inner-solar-system channel that does carry magnitude is also clean of the CDM confound.

STRUCTURE (both footings; numbered checks that can and do fail; two mutation controls):
  V1  independent reimplementation of the isolated-tail precession -> does B3b's number reproduce?
  V2  the omitted term: the external-field quadrupole's perihelion precession, machinery anchored by
      inverting the published Q_2 ceilings out of the measured per-planet sigmas
  V3  the fork inside 100 AU: MG (over the bound) vs MI (1e-7 under it)
  V4  the CDM confound, both ways

MUTATION CONTROLS.
  M1 (in V1): the retired kernel nu = sqrt(1+1/y) through the SAME independent machinery must blow the
     Mars bound by ~3e4 -- if it does not, the machinery cannot detect a solar-system violation at all.
  M2 (in V2): Q_2 = 0 must return exactly zero precession through the quadrupole path.

NOTHING HERE IS NEW PHYSICS AND NOTHING HERE IS A WIN FOR THE FRAMEWORK.  V2 makes the modified-gravity
arm look WORSE, not better.  The purpose is to establish that the B3b sentence's scope is wrong, not to
find a new bound; the Q_2 tension is already carried in STANDING.md sec 4.3 at 3-15 sigma and in g04's
own A5b, which FAILS.  This file only shows that A5b and B3b are statements about the same question and
that B3b's headline sentence contradicts A5b.

LITERATURE INPUTS, CITED, NOT INVENTED.
  Q_2 measured ceiling      : Park et al. 2026, arXiv:2602.17884 (DE440): Q_2 = (1.6 +- 1.8)e-27 s^-2,
                              2-sigma ceiling 5.2e-27 s^-2.   [as transcribed in g04, line 293]
  Q_2 earlier ceiling       : Hees et al. 2014, PRD 89, 102002 (arXiv:1402.6950): ~9e-27 s^-2.
  Q_2 Route A predicted     : 3.00e-26 (canonical) / 3.27e-26 (alt) s^-2 -- computed in g04's A5b from
                              Desmond, Hees & Famaey 2024 (arXiv:2401.04796) eq (12), pinned to <0.8%
                              on that paper's own published anchors for THIS kernel.  QUOTED from
                              g04_solar_system_eccentricity_discriminant.out line 90, not recomputed.
  Q_2 modified-inertia arm  : 7.4e-34 s^-2, committed in
                              real_research/reviews/cassini_mi_evasion_2026/.  QUOTED from g04 line 295.
  sigma(perihelion advance) : Pitjeva & Pitjev 2013 / Fienga+ 2011b as tabulated in Fienga & Minazzoli
                              2024, Living Rev. Relativ. 27:1 (arXiv:2303.01821) Table 10; banked in
                              prep_2026/planetary_doors/BOUNDS.md sec 1.2.  Same six numbers g04 uses.
  Galactic field at the Sun : V = 233 km/s, R_0 = 8.2 kpc -> 2.146e-10 m/s^2, as committed in
                              real_research/reviews/cassini_quadrupole_framework.py.
  Anomalous quadrupole form : Milgrom 2009 (MNRAS 399, 474); Blanchet & Novak 2011 (arXiv:1105.5815);
                              Hees et al. 2014 eq (2): delta-Phi = -(Q_2/2)[(e.x)^2 - x^2/3], giving
                              a_i = Q_2[(e.x)e_i - x_i/3].
"""
import sys, math
import numpy as np
from scipy.optimize import brentq
from hunt_lib import Check, P, info, A0

ck = Check()
np.seterr(all="ignore")

GM_SUN  = 1.32712440018e20
AU      = 1.495978707e11
YR      = 3.155760000e7
RAD2MAS = 180.0/math.pi*3600.0*1000.0
C_LIGHT = 2.99792458e8
G_EXT   = 2.146e-10
V_MW    = 233.0e3
R0_MW   = 8.2*3.0857e19

# Route A predicted Q_2, QUOTED from g04's A5b (not recomputed here -- that integral is g04's job and it
# is pinned on Desmond+2024's published anchors to 0.76%).
Q2_ROUTEA = {"canonical": 3.00e-26, "alt": 3.27e-26}
Q2_CEIL   = 5.2e-27      # Park+2026 2-sigma
Q2_H14    = 9.0e-27      # Hees+2014
Q2_MI     = 7.4e-34      # committed MI arm

PLANETS = [   # name, a[AU], e, sigma(omegadot) [mas/yr]
    ("Mercury", 0.38709927, 0.20563593, 0.006),
    ("Venus",   0.72333566, 0.00677672, 0.015),
    ("Earth",   1.00000261, 0.01671123, 0.0019),
    ("Mars",    1.52371034, 0.09339410, 0.00037),
    ("Jupiter", 5.20288700, 0.04838624, 0.28),
    ("Saturn",  9.53667594, 0.05386179, 0.0047),
]

P("="*118)
P("g04v -- ADVERSARIAL: does 'the eccentricity discriminant is vacuous inside 100 AU' survive?")
P("="*118)


# ============================================================================================ machinery
def period(a_m): return 2.0*math.pi*math.sqrt(a_m**3/GM_SUN)

def dw_per_orbit(a_m, e, Rfun, Sfun, n=40001):
    r"""Orbit-averaged perihelion advance per orbit, from Gauss's form of the Lagrange planetary
    equations with BOTH components (Murray & Dermott eq 2.164; Burns 1976 Am.J.Phys 44, 944):

        dw/dt = (sqrt(1-e^2)/(n a e)) [ -R cos f + S (2 + e cos f)/(1 + e cos f) sin f ]

    with R the RADIAL component positive OUTWARD and S the transverse component positive in the
    direction of motion.  Multiplying by dt = r^2/h df and using h = n a^2 sqrt(1-e^2):

        Delta(w) = (1/(GM e)) Int_0^{2pi} r^2 [ -R cos f + S (2 + e cos f) sin f/(1 + e cos f) ] df

    NOTE this is a DIFFERENT implementation from g04's: g04 drops the S term (valid only for a purely
    central perturbation, which the quadrupole is not) and integrates the trapezoid rule in true
    anomaly.  Here Simpson's rule is used and the S term is carried, so V1 is a genuine cross-check of
    g04's Part B rather than a rerun of it."""
    f = np.linspace(0.0, 2.0*math.pi, n)
    r = a_m*(1.0 - e*e)/(1.0 + e*np.cos(f))
    R = Rfun(r, f); S = Sfun(r, f)
    integ = r*r*(-R*np.cos(f) + S*(2.0 + e*np.cos(f))*np.sin(f)/(1.0 + e*np.cos(f)))
    # Simpson on a uniform grid (n odd)
    h = f[1] - f[0]
    I = h/3.0*(integ[0] + integ[-1] + 4.0*integ[1:-1:2].sum() + 2.0*integ[2:-2:2].sum())
    return I/(GM_SUN*e)

def log10_dg_routeA(gN, a0):
    gN = np.asarray(gN, dtype=float); u = np.sqrt(gN/a0)
    corr = np.where(u < 40.0, np.log10(-np.expm1(-np.minimum(u, 40.0))), 0.0)
    return np.log10(gN) - u/math.log(10.0) - corr

def dw_log_routeA(a_m, e, a0, n=40001):
    """log10|Delta w| per orbit for the isolated Route A tail, done in logs (the integrand spans
    hundreds of decades).  Radial-only, inward-positive convention -> R_out = -dg."""
    f = np.linspace(0.0, 2.0*math.pi, n)
    r = a_m*(1.0 - e*e)/(1.0 + e*np.cos(f))
    L = log10_dg_routeA(GM_SUN/r**2, a0); Lm = float(np.max(L))
    w = 10.0**(L - Lm)*r*r*np.cos(f)
    h = f[1] - f[0]
    I = h/3.0*(w[0] + w[-1] + 4.0*w[1:-1:2].sum() + 2.0*w[2:-2:2].sum())
    return Lm + math.log10(abs(I)) - math.log10(GM_SUN*e)


# ============================================================================================
P(""); P("-"*118)
P("PART V1 -- can g04's B3b arithmetic be reproduced by an independent implementation?")
P("-"*118)

P(""); info("V1.0 -- validate the independent Gauss integrator on two closed forms with opposite signs")
errs = []
for aAU, e in ((0.38709927, 0.20563593), (9.53667594, 0.05386179), (100.0, 0.90)):
    a_m = aAU*AU; p = a_m*(1 - e*e)
    ana_gr = 6.0*math.pi*GM_SUN/(C_LIGHT**2*p)
    num_gr = dw_per_orbit(a_m, e,
                          lambda r, f: -3.0*GM_SUN*(GM_SUN*p)/(C_LIGHT**2*r**4),
                          lambda r, f: np.zeros_like(r))
    dg0 = 1e-13
    ana_c = -2.0*math.pi*dg0*a_m**2*math.sqrt(1 - e*e)/GM_SUN
    num_c = dw_per_orbit(a_m, e, lambda r, f: np.full_like(r, -dg0), lambda r, f: np.zeros_like(r))
    errs += [abs(num_gr/ana_gr - 1.0), abs(num_c/ana_c - 1.0)]
    P(f"  a={aAU:8.4f} e={e:.4f}   GR  ana {ana_gr:+.6e} num {num_gr:+.6e} rel {num_gr/ana_gr-1:+.1e}"
      f"   |  const  ana {ana_c:+.6e} num {num_c:+.6e} rel {num_c/ana_c-1:+.1e}")
ck("V1a  the independent Gauss integrator reproduces both closed forms",
   max(errs) < 1e-8,
   f"worst relative error {max(errs):.2e} over the GR 1/r^4 prograde form and the constant-inward "
   f"retrograde form.  Different quadrature (Simpson) and a transverse term g04 does not carry; both "
   f"closed forms recovered, so this is an independent check of g04's Part B machinery, not a rerun")

P(""); info("V1.1 -- reproduce g04's B3 table: log10|dw| per orbit and the rate at e=0.01 vs e=0.90")
P(f"  {'a [AU]':>9}{'L(e=.01)':>12}{'L(e=.9)':>11}{'log10 ratio':>13}{'rate(e=.9) mas/yr':>20}"
  f"{'g04 rate':>12}")
G04_RATE_LOG = {1.0: -1812.91, 5.0: -358.10, 10.0: -176.47, 30.0: -55.65, 100.0: -13.72}
G04_RATIO    = {1.0: 1599.93, 5.0: 317.36, 10.0: 157.05, 30.0: 50.23, 100.0: 13.10}
a0c = A0["canonical"]
rate_err, ratio_err, inner_rates = [], [], []
for aAU in (1.0, 5.0, 10.0, 30.0, 100.0):
    a_m = aAU*AU; Pyr = period(a_m)/YR
    L1 = dw_log_routeA(a_m, 0.01, a0c); L9 = dw_log_routeA(a_m, 0.90, a0c)
    Lrate = L9 - math.log10(Pyr) + math.log10(RAD2MAS)
    rate_err.append(abs(Lrate - G04_RATE_LOG[aAU])); ratio_err.append(abs((L9 - L1) - G04_RATIO[aAU]))
    inner_rates.append(10.0**Lrate)
    P(f"  {aAU:>9.0f}{L1:>12.2f}{L9:>11.2f}{L9-L1:>13.2f}{Lrate:>20.2f}{G04_RATE_LOG[aAU]:>12.2f}")
max_inner = max(inner_rates)
MARS_SIG = 0.00037
ck("V1b  g04's B3 table reproduces independently, to better than 0.02 dex everywhere",
   max(rate_err) < 0.02 and max(ratio_err) < 0.02,
   f"worst |delta log10 rate| = {max(rate_err):.4f} dex and worst |delta log10 ratio| = "
   f"{max(ratio_err):.4f} dex across a = 1-100 AU.  The 10^157 ratio at 10 AU and the "
   f"log10 rate = {math.log10(max_inner):.2f} at 100 AU are both confirmed")
ck("V1c  the B3b HEADLINE NUMBER is confirmed: 1.9e-14 mas/yr, shortfall 10^10 vs Mars",
   abs(math.log10(max_inner/1.9e-14)) < 0.05 and abs(math.log10(MARS_SIG/max_inner) - 10.0) < 0.5,
   f"independently {max_inner:.2e} mas/yr (g04 says 1.9e-14), shortfall "
   f"10^{math.log10(MARS_SIG/max_inner):.1f} against Mars's {MARS_SIG} mas/yr.  THE ARITHMETIC OF THE "
   f"CLAIM IS CORRECT AND IS NOT WHAT THIS AUDIT DISPUTES")

P(""); info("V1.2 -- MUTATION CONTROL M1: the retired kernel nu = sqrt(1+1/y) through the SAME machinery")
mut = {}
for fn, a0 in A0.items():
    ex = []
    for nm, aAU, e, sw in PLANETS:
        a_m = aAU*AU
        dg = (math.sqrt(1.0 + a0/(GM_SUN/a_m**2)) - 1.0)*(GM_SUN/a_m**2)   # -> a_0/2 in the deep-Newtonian tail
        dw = dw_per_orbit(a_m, e, lambda r, f: np.full_like(r, -(np.sqrt(1.0 + a0*r**2/GM_SUN) - 1.0)*GM_SUN/r**2),
                          lambda r, f: np.zeros_like(r))
        rate = abs(dw)/(period(a_m)/YR)*RAD2MAS
        ex.append(rate/sw)
        if fn == "canonical":
            P(f"  {nm:<9} rate {rate:.3e} mas/yr   sigma {sw:.5f}   excluded by {rate/sw:8.0f}x")
    mut[fn] = max(ex)
ck("V1d  MUTATION CONTROL M1 fires: the retired kernel is blown out by ~3e4 through this machinery",
   min(mut.values()) > 1e3,
   f"max exclusion {mut['canonical']:.0f}x (canonical) / {mut['alt']:.0f}x (alt), driven by Mars -- "
   f"matching KERNEL_PLANETS.md's banked 33436x.  So the V1 machinery CAN report a solar-system "
   f"violation; the 10^10 shortfall in V1c is a property of Route A's kernel, not of a dead integrator")


# ============================================================================================
P(""); P("-"*118)
P("PART V2 -- THE ATTACK: the term B3b omits, and it is the one that is measured")
P("-"*118)
P("  The Sun is not isolated.  g_ext = 2.146e-10 m/s^2 > a_0, so the nonlinear MOND field equation's")
P("  exterior boundary condition imprints a CONSTANT anomalous quadrupole on the whole interior:")
P("      delta-Phi = -(Q_2/2)[(e.x)^2 - x^2/3]   ->   a_i = Q_2[(e.x) e_i - x_i/3]")
P("  (Milgrom 2009 MNRAS 399 474; Blanchet & Novak 2011 arXiv:1105.5815; Hees+2014 PRD 89 102002.)")
P("  Q_2 is set at r_M ~ 8000 AU where y ~ 1.  Route A's exponential does NOTHING to it -- that is")
P("  g04's own A5b finding, which FAILS at 5.8x over the Park+2026 ceiling.  The anomalous acceleration")
P("  it carries is Q_2 * r, GROWING outward, ANISOTROPIC, and it precesses perihelia.")

def dw_quadrupole(a_m, e, Q2, beta):
    """Perihelion advance per orbit from the anomalous quadrupole, with the symmetry axis e-hat at
    angle beta from the perihelion direction and lying IN the orbit plane (the maximal-coupling
    geometry; an out-of-plane tilt reduces the in-plane components by <=1).  theta = f + omega with
    omega = 0.  R_out = Q2 r [cos^2(theta-beta) - 1/3];  S = -Q2 r cos(theta-beta) sin(theta-beta)."""
    return dw_per_orbit(a_m, e,
                        lambda r, f: Q2*r*(np.cos(f - beta)**2 - 1.0/3.0),
                        lambda r, f: -Q2*r*np.cos(f - beta)*np.sin(f - beta))

P(""); info("V2.0 -- MUTATION CONTROL M2: Q_2 = 0 must give exactly zero through the quadrupole path")
z = max(abs(dw_quadrupole(aAU*AU, e, 0.0, b)) for nm, aAU, e, sw in PLANETS for b in (0.0, 1.0, 2.0))
ref = abs(dw_quadrupole(9.53667594*AU, 0.05386179, 1e-26, 0.7))
ck("V2a  MUTATION CONTROL M2: the quadrupole path returns identically zero at Q_2 = 0",
   z == 0.0 and ref > 0.0,
   f"max |dw| over 6 planets x 3 orientations at Q_2 = 0 is {z:.1e}; the Q_2 = 1e-26 reference at "
   f"Saturn is {ref:.3e} rad/orbit.  No spurious constant is leaking into the quadrupole branch")

P(""); info("V2.1 -- ANCHOR: invert the measured sigmas to a Q_2 ceiling; must land on the PUBLISHED one")
P("  If this machinery is right, feeding each planet's measured sigma(omegadot) back through it must")
P("  reproduce the Q_2 ceilings the literature actually quotes (Park+2026 5.2e-27, Hees+2014 9e-27).")
P("  Nothing is tuned: the geometry is scanned over the full range of orientations and the resulting")
P("  per-planet ceiling BAND is compared to the published number.")
betas = np.linspace(0.0, 2.0*math.pi, 73)[:-1]
P(f"  {'planet':<9}{'P [yr]':>9}{'|dw/dt| per Q2 [mas/yr / (1e-26 s^-2)]':>40}{'Q2 ceiling from sigma [s^-2]':>32}")
ceilings = {}
for nm, aAU, e, sw in PLANETS:
    a_m = aAU*AU; Pyr = period(a_m)/YR
    resp = np.array([abs(dw_quadrupole(a_m, e, 1e-26, b))/Pyr*RAD2MAS for b in betas])
    lo, hi = resp[resp > 0].min(), resp.max()
    c_lo, c_hi = sw/hi*1e-26, sw/lo*1e-26     # tightest / loosest ceiling over orientation
    ceilings[nm] = (c_lo, c_hi)
    P(f"  {nm:<9}{Pyr:>9.2f}{('%.3e - %.3e' % (lo, hi)):>40}{('%.2e - %.2e' % (c_lo, c_hi)):>32}")
sat_lo, sat_hi = ceilings["Saturn"]
anchor_ok = (sat_lo <= Q2_CEIL <= sat_hi) or (sat_lo <= Q2_H14 <= sat_hi)
ck("V2b  ANCHOR: the published Q_2 ceiling falls inside the band this machinery derives from Saturn",
   anchor_ok,
   f"Saturn's measured sigma = 0.0047 mas/yr maps to Q_2 <= {sat_lo:.2e} - {sat_hi:.2e} s^-2 across "
   f"orbit orientations, and the published ceilings -- Park+2026 {Q2_CEIL:.1e} and Hees+2014 "
   f"{Q2_H14:.1e} -- sit inside that band.  Saturn is exactly the planet those analyses are driven by "
   f"(Cassini ranging).  The quadrupole precession machinery is therefore validated against published "
   f"numbers it was not fitted to, which is what licenses the next check")

P(""); info("V2.2 -- THE REFUTATION: Route A's OWN Q_2 through the SAME machinery, inside 100 AU")
P(f"  Route A's Q_2 = {Q2_ROUTEA['canonical']:.2e} (canonical) / {Q2_ROUTEA['alt']:.2e} (alt) s^-2, taken")
P(f"  from g04's own A5b (Desmond+2024 eq 12, pinned to 0.76% on that paper's anchors for THIS kernel).")
P(f"  {'planet':<9}{'MG quadrupole rate [mas/yr]':>30}{'sigma [mas/yr]':>17}{'over by':>10}"
  f"{'B3b isolated tail':>20}{'omitted factor':>17}")
over = {}
for fn, a0 in A0.items():
    Q2 = Q2_ROUTEA[fn]; worst = 0.0
    for nm, aAU, e, sw in PLANETS:
        a_m = aAU*AU; Pyr = period(a_m)/YR
        resp = np.array([abs(dw_quadrupole(a_m, e, Q2, b))/Pyr*RAD2MAS for b in betas])
        rmax = resp.max(); worst = max(worst, rmax/sw)
        if fn == "canonical":
            Ltail = dw_log_routeA(a_m, e, a0) - math.log10(Pyr) + math.log10(RAD2MAS)
            P(f"  {nm:<9}{rmax:>30.4e}{sw:>17.5f}{rmax/sw:>10.1f}{('1e%.0f' % Ltail):>20}"
              f"{('1e%.0f' % (math.log10(rmax) - Ltail)):>17}")
    over[fn] = worst
# and at a = 100 AU, e = 0.9 -- the exact configuration B3b calls "the largest inside 100 AU"
a100 = 100.0*AU; P100 = period(a100)/YR
q100 = max(abs(dw_quadrupole(a100, 0.90, Q2_ROUTEA["canonical"], b)) for b in betas)/P100*RAD2MAS
ck("V2c  B3b's 'largest modified-gravity precession rate anywhere inside 100 AU' is the largest",
   q100 <= max_inner,
   f"IT IS NOT, BY TWELVE TO FOURTEEN ORDERS.  At the very configuration B3b names -- a = 100 AU, "
   f"e = 0.9 -- the external-field quadrupole gives {q100:.2e} mas/yr against B3b's {max_inner:.2e} "
   f"mas/yr for the isolated tail: a factor 10^{math.log10(q100/max_inner):.0f}.  At Saturn the "
   f"quadrupole gives up to {over['canonical']*0 + max(abs(dw_quadrupole(9.53667594*AU, 0.05386179, Q2_ROUTEA['canonical'], b)) for b in betas)/(period(9.53667594*AU)/YR)*RAD2MAS:.4f} "
   f"mas/yr against sigma = 0.0047.  B3b computed ONE TERM of the modified-gravity solution -- the "
   f"isolated-Sun central tail -- and its sentence promotes that to 'the modified-gravity precession'")
ck("V2d  the modified-gravity arm's inner-solar-system precession is below the measured bounds",
   max(over.values()) < 1.0,
   f"IT IS NOT.  Route A's Q_2 exceeds the sharpest per-planet perihelion sigma by up to "
   f"{over['canonical']:.1f}x (canonical) / {over['alt']:.1f}x (alt) at the maximal-coupling "
   f"orientation.  That is the SAME 5.8x/6.3x g04's A5b reports against the Park+2026 ceiling, "
   f"recovered here through perihelion precession rather than through the Cassini Q_2 fit -- so the "
   f"modified-gravity arm does not merely have magnitude to work with inside 100 AU, it has too much, "
   f"and the inner solar system already excludes it.  (Reading caveat carried from g04: the true "
   f"orientation is fixed by the Galactic-centre direction, not scanned, and the significance is set "
   f"by the Milky Way mass model -- Desmond+2024 quote 8.7 sigma fiducial, 1.9 sigma with bulge "
   f"galaxies cut.  The ROBUST statement is 'of order the bound, not 1e-10 of it')")


# ============================================================================================
P(""); P("-"*118)
P("PART V3 -- does the inner solar system decide the fork, or not?")
P("-"*118)
P(f"  modified GRAVITY  arm : Q_2 = {Q2_ROUTEA['canonical']:.2e} s^-2  ->  {Q2_ROUTEA['canonical']/Q2_CEIL:.1f}x the Park+2026 ceiling")
P(f"  modified INERTIA  arm : Q_2 = {Q2_MI:.2e} s^-2  ->  {Q2_MI/Q2_CEIL:.1e} of the same ceiling")
P(f"                          (committed in cassini_mi_evasion_2026/, on the OLD kernel; quoted, not")
P(f"                           recomputed, exactly as g04 flags it)")
sep = Q2_ROUTEA["canonical"]/Q2_MI
ck("V3a  the fork CANNOT be decided by orbital dynamics in the inner solar system",
   sep < 10.0,
   f"IT CAN, AND g04's OWN PART A DECIDES IT.  The two arms differ by a factor {sep:.1e} in the one "
   f"inner-solar-system observable that carries magnitude, and the measurement sits BETWEEN them: the "
   f"modified-gravity arm is {Q2_ROUTEA['canonical']/Q2_CEIL:.1f}x OVER the 2-sigma ceiling and the "
   f"modified-inertia arm is {Q2_MI/Q2_CEIL:.0e} UNDER it.  A bracketed measurement is the definition "
   f"of a decided fork.  g04's own conclusion says so -- 'the fork-relevant solar-system information "
   f"is entirely in A5b (Q_2)' -- which is precisely what the B3b headline sentence denies")
# Is the quadrupole precession actually a function of orbit SHAPE, or only of size?  Two independent
# probes at fixed a: (1) spread over the symmetry-axis orientation beta; (2) ratio between e = 0.01 and
# e = 0.90 at fixed beta.  "Orbit-shape-blind" would mean BOTH ratios sit at 1.
sat_resp = np.array([abs(dw_quadrupole(9.53667594*AU, 0.05386179, 1e-26, b)) for b in betas])
orient_spread = float(sat_resp.max()/sat_resp[sat_resp > 0].min())
ecc_ratio = float(abs(dw_quadrupole(100*AU, 0.90, 1e-26, 0.0))/abs(dw_quadrupole(100*AU, 0.01, 1e-26, 0.0)))
P(f"  orbit-shape dependence of the quadrupole precession: orientation spread at fixed (a,e) = "
  f"{orient_spread:.1f}x;  e=0.90 / e=0.01 at fixed beta, a = 100 AU = {ecc_ratio:.2f}x")
ck("V3b  the Q_2 channel is orbit-shape-blind, so 'cannot be decided by ORBIT SHAPE' still stands",
   abs(orient_spread - 1.0) < 0.05 and abs(ecc_ratio - 1.0) < 0.05,
   f"IT IS NOT ORBIT-SHAPE-BLIND.  The quadrupole force is anisotropic, so its perihelion advance "
   f"depends on the perihelion's orientation relative to the symmetry axis (Saturn response varies "
   f"{orient_spread:.1f}x over the orientation scan at fixed a and e) and on eccentricity "
   f"({ecc_ratio:.2f}x between e = 0.01 and e = 0.90 at a = 100 AU, fixed beta).  Both are far from 1, "
   f"which is what 'blind' would require.  Orbit shape is exactly the handle the published Q_2 "
   f"constraints use -- they are fits to SUPPLEMENTARY PERIHELION ADVANCES, per planet, per geometry.  "
   f"The eccentricity lever here is modest (0.44x, not 1e157) but it is not zero, and it sits on a "
   f"signal that is of order the measurement rather than 1e-10 of it, which is the whole point")


# ============================================================================================
P(""); P("-"*118)
P("PART V4 -- the confound lens: would ordinary cold dark matter give the same signature?")
P("-"*118)
Q2_CDM = V_MW**2/R0_MW**2
P(f"  For the B3b NULL: GR + CDM predicts identically zero solar-system anomaly.  1.9e-14 mas/yr is")
P(f"  observationally indistinguishable from zero, so B3b separates the framework from nothing.")
P(f"  For the Q_2 CHANNEL: the Newtonian/CDM Galactic tide at the Sun is of order V^2/R_0^2 =")
P(f"  {Q2_CDM:.2e} s^-2 (V = 233 km/s, R_0 = 8.2 kpc), against the Park+2026 ceiling {Q2_CEIL:.1e} and")
P(f"  Route A's {Q2_ROUTEA['canonical']:.2e}.  The CDM tide is {Q2_CEIL/Q2_CDM:.0f}x BELOW the ceiling")
P(f"  and {Q2_ROUTEA['canonical']/Q2_CDM:.1e}x below the MOND value.")
ck("V4a  the B3b null discriminates the framework from GR + cold dark matter",
   max_inner > MARS_SIG,
   f"IT DOES NOT, and cannot: {max_inner:.1e} mas/yr is zero to any instrument.  B3b is a CONSISTENCY "
   f"statement, not a discriminant.  This is not a criticism of the arithmetic -- g04's own honesty "
   f"note says the same -- but it does mean B3b carries no fork information in EITHER direction, so "
   f"nothing about the fork can be concluded from it")
ck("V4b  the Q_2 channel is confounded by the ordinary Newtonian Galactic tide",
   Q2_CDM > Q2_CEIL,
   f"IT IS NOT.  The CDM/Newtonian tide {Q2_CDM:.2e} s^-2 is {Q2_CEIL/Q2_CDM:.0f}x below the "
   f"measurement ceiling and {Q2_ROUTEA['canonical']/Q2_CDM:.1e}x below Route A's prediction, so the "
   f"Q_2 excess is not something ordinary cold dark matter produces.  The channel that DOES carry "
   f"magnitude inside 100 AU is therefore clean of the confound the audit lens asks about -- which "
   f"makes the refutation of B3b's inference stronger, not weaker")


# ============================================================================================
P(""); P("="*118); P("VERDICT"); P("="*118)
P(f"""
 THE ARITHMETIC SURVIVES.  Route A's isolated-Sun central tail gives {max_inner:.2e} mas/yr at a = 100 AU,
 e = 0.9 -- 10^{math.log10(MARS_SIG/max_inner):.0f} below Mars -- reproduced here to {max(rate_err):.3f} dex with a different quadrature,
 a transverse term g04 does not carry, and a mutation control that fires at {mut['canonical']:.0f}x on the retired
 kernel.  The 10^157 ratio at 10 AU is confirmed to {max(ratio_err):.3f} dex.  V1a-V1d all PASS.

 THE INFERENCE DOES NOT.  "The modified-gravity precession has no magnitude to work with [inside 100 AU],
 so the fork cannot be decided by orbit shape in the inner solar system" is false on both clauses:

  * The isolated-Sun tail is one term of the modified-gravity solution, and not the leading one.  The
    Sun sits in a Galactic field above a_0; the resulting anomalous quadrupole is set at r_M ~ 8000 AU
    where the exponential does nothing, and inside 100 AU it exceeds the isolated tail by
    10^{math.log10(q100/max_inner):.0f}.  Fed through the same Gauss machinery -- anchored by recovering the PUBLISHED Q_2
    ceilings out of the measured per-planet sigmas (V2b) -- Route A's own Q_2 gives up to {over['canonical']:.1f}x the
    sharpest per-planet perihelion sigma.  The modified-gravity arm is not invisible inside 100 AU; it
    is already EXCLUDED there.

  * The fork IS decided there.  The two arms sit at {Q2_ROUTEA['canonical']/Q2_CEIL:.1f}x over and {Q2_MI/Q2_CEIL:.0e} under the same ceiling, a
    separation of {sep:.1e}, and the measurement falls between them.  g04's own A5b FAILS and g04's own
    conclusion says the fork-relevant solar-system information is entirely in that check.  The B3b
    headline sentence contradicts the file it is drawn from.

  * And the quadrupole IS an orbit-shape observable: the published constraints are fits to
    supplementary perihelion advances planet by planet, and the response varies with e and with the
    perihelion's orientation.

 WHAT SHOULD BE CLAIMED INSTEAD.  "Route A's ISOLATED-SUN exponential tail is vacuous as an eccentricity
 discriminant inside 100 AU, by 10^10 -- and this says nothing about the fork, because the inner solar
 system's fork-relevant signal is the external-field quadrupole, which is 5.8x over the bound for
 modified gravity and 1e-7 under it for modified inertia."  That sentence is fully supported by g04.
 The one that was handed out is not.

 DIRECTION OF THE ERROR.  Against the framework's operative arm, not for it.  Every correction here makes
 the modified-gravity arm's solar-system standing WORSE.  Nothing in this file is a win for anything.

 CAVEATS, LOAD-BEARING.
  * Q_2 = 3.00e-26 s^-2 is QUOTED from g04's A5b, not recomputed.  If that integral is wrong, V2c/V2d/V3a
    move with it.  It is pinned to 0.76% on Desmond+2024's own published anchors for this exact kernel.
  * The Q_2 -> precession response is computed with the symmetry axis IN the orbit plane and scanned over
    orientation.  The true Galactic-centre direction is fixed and out of the ecliptic, so the real
    per-planet response is a specific number inside the band, not the maximum.  Every "over by" figure is
    therefore an UPPER reading; the robust statement is "of order the measured bound", which is all the
    refutation needs -- B3b's claim is 1e-10 of the bound.
  * The MI contrast 7.4e-34 s^-2 is committed on the OLD kernel nu = sqrt(1+1/y) and quoted, not
    recomputed, exactly as g04 flags.  The fork separation in V3a inherits that.
  * Nothing here prefers the framework over LambdaCDM.  V4a/V4b establish only that the Q_2 channel is
    not CDM-confounded, i.e. that it is a real discriminant against the framework's modified-gravity arm.
""")
sys.exit(ck.done())
