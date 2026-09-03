#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
g04_solar_system_eccentricity_discriminant.py -- THE SOLAR SYSTEM AS A FORK DISCRIMINANT.
=========================================================================================
THE FORK (F08_F10_THE_COHERENCE_FORK.md).  Modified GRAVITY: the correction is a property of the FIELD AT A
POINT, g = nu(g_N/a_0) g_N, so a near-circular planet and a highly eccentric comet AT THE SAME HELIOCENTRIC
DISTANCE feel the SAME extra acceleration.  Modified INERTIA: the correction attaches to the TRAJECTORY, so
they do not.  Milgrom (1994; 2011, arXiv:1111.1611) proved the two are IDENTICAL for circular orbits in the
deep-MOND limit and DIFFER for every other orbit.  The solar system holds the most precise orbits in
astronomy and spans e = 0.007 (Venus) to e = 0.9999 (Oort-spike comets).  Does it decide the fork?

FOUR FINDINGS, THREE NEGATIVE AND ONE THAT IS NOT.

 1. THE ISOTROPIC TAIL IS NOT SMALL, IT IS ABSENT.  Route A's nu(y) = 1/(1-exp(-sqrt y)) gives an anomalous
    acceleration g_N*exp(-sqrt(g_N/a_0)) which at Saturn is 10^-367 m/s^2 against a 7.0e-15 bound: a margin
    of ~350 ORDERS.  The perihelion-precession discriminant therefore has no magnitude to work with anywhere
    inside 100 AU -- the largest modified-gravity precession rate there, at the most favourable eccentricity,
    is ~1e-14 mas/yr against Mars's 0.00037 mas/yr.  The retired kernel nu = sqrt(1+1/y) instead gives a
    CONSTANT a_0/2 excluded 6712x at Saturn / 33436x at Mars; both come out of the same machinery, and the
    second is the mutation control that proves the machinery can fail (A3a).

 2. THE MODIFIED-GRAVITY ARM NEVERTHELESS FAILS THE SOLAR SYSTEM, THROUGH A CHANNEL THE TAIL DOES NOT TOUCH.
    The external-field quadrupole Q_2 is not set at Saturn; it is set at the MOND radius r_M ~ 8000 AU where
    y ~ 1 and no exponential suppression exists.  Computed from Desmond, Hees & Famaey 2024
    (arXiv:2401.04796) eq (12) -- whose published anchors q(1)=0.094, q(1.5)=0.159, q(2)=0.221 are for
    EXACTLY this kernel -- Route A gives Q_2 = 3.0e-26 s^-2 against the Park et al. 2026 (arXiv:2602.17884)
    ceiling 5.2e-27.  ~6x over.  The repo's committed modified-INERTIA value is 7.4e-34 s^-2, 1e-7 of the
    ceiling.  So this channel DOES separate the arms at high significance and it points AWAY from modified
    gravity.  This confirms rather than discovers (STANDING.md carries a 3-15 sigma Q_2 tension); what is new
    is that it holds on Route A specifically, and that it must not be conflated with the tail liability,
    which really is discharged.

 3. THE BEST ECCENTRICITY LEVER THAT EXISTS, QUANTIFIED AND FOUND SHORT.  The anomaly peaks at 6.1e-11 m/s^2
    at r = 4995 AU (exact root of e^u(2-u)=2, A4a), so the optimum object is a ~2500 AU long-period comet
    carrying ~1 deg per orbit.  Unusable: outgassing at perihelion is ~100x the signal, the comet is seen for
    one apparition, and planetary perturbations scatter 1/a by 20% per passage.  The best INERT lever is
    Sedna; even granting modified inertia its most generous PRECESSION reading, the signal is 0.023 mas after
    a 4-element orbit fit to its 25-yr arc, against ~100 mas astrometry -- 4000x short, and structurally so,
    because 25 yr is 0.22% of one orbit.

 4. THE ONE THING THAT IS NOT SHUT, AND IT IS NOT A PRECESSION TEST.  The most generous modified-inertia
    reading -- nu frozen at the orbit's minimum acceleration -- is EXACTLY a rescaling of the effective GM
    along that orbit (it therefore precesses nothing at all; see the B2a theorem).  On Sedna it is
    eps = 2.03e-4, while modified gravity predicts 2e-41 at Sedna's present distance: a ratio of 10^37.
    Against angles plus parallax range on the 25-yr arc that is 0.57 sigma at 100 mas astrometry and ~5.7
    sigma at 10 mas.  So an LSST-era effective-GM measurement on Sedna WOULD land inside the span the two
    arms bracket.  It is reported here with its killer attached: eps = 2.03e-4 of M_sun is 68 M_earth of
    unmodelled interior mass, so a DETECTION would be read as Planet Nine, not as gravity.  Only the NULL
    side is clean.

STRUCTURE (both footings throughout; numbered checks that can and do fail; mutation controls in A3, B2, D2):
  A  the modified-gravity anomalous acceleration vs heliocentric distance, and the Cassini confrontation
  B  the discriminant: anomalous perihelion precession as an exact function of (a, e) in modified gravity
  C  which real objects give the best lever, in (a, e) space
  D  how far short -- the quantified negative, and the one channel that is not shut

HONESTY NOTES, LOAD-BEARING.
  * Nothing here can prefer the framework over LambdaCDM.  At planetary accelerations (10^4-10^8 a_0) GR
    predicts zero anomaly and so do healthy MOND-family theories.  These numbers discriminate BETWEEN the
    framework's own arms only.  (Same ceiling as prep_2026/planetary_doors/BOUNDS.md sec 0.)
  * The two "MI envelopes" used here (MI-A: a constant additive dg keyed to the orbit's minimum acceleration;
    MI-B: nu itself frozen at that value) are UPPER ENVELOPES, deliberately extreme, NOT predictions of any
    specific MI theory.  A real nonlocal MI kernel lands between them and the modified-gravity curve.  They
    are used because a route that is shut for the most generous reading is shut for every reading.
  * The repo's own MI kernel work (prep_2026/planetary_doors/KERNEL_PLANETS.md) shows the MI answer is
    reading-dependent, and STANDING.md closes the MI arm as physics at 21 sigma by lensing.  This script does
    not reopen that; it asks only what the solar system can and cannot see.
  * Astrometric precisions for Sedna are ESTIMATES (100 mas ground-based, 10 mas LSST-class), not a published
    orbit covariance, which is not available in this repository.  Every number that depends on them is
    labelled and the check that uses them says so.

PRIOR REPO WORK CONFIRMED, NOT RE-DERIVED (task instruction (a); working rule 8):
  prep_2026/planetary_doors/BOUNDS.md + laneR_bounds_compute.py -- the per-planet delta-g bounds (from
      Fienga & Minazzoli 2024, Living Rev. Relativ. 27:1, arXiv:2303.01821, Table 10), the Hees+2014 and
      Park+2026 Q_2 ceilings, the Blanchet & Novak 2011 theory values.  Reproduced in A1a to <3%.
  prep_2026/planetary_doors/KERNEL_PLANETS.md -- the banked retired-kernel exclusions (Mars 33436x,
      Saturn 6687x).  Reproduced in A3a.
  real_research/reviews/mi_route_a_exponential_kernel_2026.py (R2a) -- Route A suppresses the alpha=2 Sun
      anomaly by ~3.3e13.  CONFIRMED here in ABSOLUTE terms rather than as a ratio (A2a).
  real_research/reviews/branchB_q2_gate_2026/verify_laneC_paper_anchor.py -- the eq-(12) q-integral pinned on
      the published Desmond+2024 anchors for nu = 1/(1-exp(-sqrt y)).  RE-PINNED here (A5a) to <0.5%.
  real_research/reviews/cassini_mi_evasion_2026/ -- the committed MI-side l=2 quadrupole 7.4e-34 s^-2.
      QUOTED as the contrast in A5b, on the OLD kernel nu = sqrt(1+1/y); flagged as such, not recomputed.
  hunt_2026/h12_h14_satellites_and_oort.py -- the Oort front; r_M = 7955 AU and the ~1e-4 AU^-1 per-passage
      planetary scatter in 1/a that makes the Oort spike untestable.  Used in D1, not recomputed.
"""
import sys, os, math
import numpy as np
from scipy import integrate
from scipy.optimize import brentq
from scipy.integrate import solve_ivp
from hunt_lib import Check, P, info, A0

ck = Check()
np.seterr(all="ignore")

# ---------------------------------------------------------------------------- constants (IAU / JPL nominal)
GM_SUN  = 1.32712440018e20       # m^3/s^2
AU      = 1.495978707e11         # m (IAU 2012, exact)
YR      = 3.155760000e7          # Julian year, s
M_EARTH_OVER_M_SUN = 1.0/332946.0487
RAD2MAS = 180.0/math.pi*3600.0*1000.0
C_LIGHT = 2.99792458e8
# The Milky Way's field at the Sun: V = 233 km/s, R0 = 8.2 kpc -> V^2/R0 = 2.146e-10 m/s^2 (a MOND field),
# as committed in real_research/reviews/cassini_quadrupole_framework.py.
G_EXT = 2.146e-10

P("="*118)
P("g04 -- THE SOLAR SYSTEM AS AN ECCENTRICITY DISCRIMINANT BETWEEN MODIFIED GRAVITY AND MODIFIED INERTIA")
P("="*118)


# ---------------------------------------------------------------------------- kernels
def log10_dg_routeA(gN, a0):
    """log10 of the Route A anomalous acceleration (nu-1)*g_N.  Computed in logs because exp(-sqrt y)
    underflows float64 by hundreds of orders at planetary y.  nu-1 = e^-u/(1-e^-u), u = sqrt(g_N/a_0);
    log10(1-e^-u) is 0.0 to machine precision for u > 40, and expm1 is used below that."""
    gN = np.asarray(gN, dtype=float); u = np.sqrt(gN/a0)
    corr = np.where(u < 40.0, np.log10(-np.expm1(-np.minimum(u, 40.0))), 0.0)
    return np.log10(gN) - u/math.log(10.0) - corr

def dg_routeA(gN, a0):
    L = log10_dg_routeA(gN, a0)
    return np.where(L > -300.0, 10.0**np.clip(L, -300.0, None), 0.0)

def numinus1_routeA(y):
    """nu(y) - 1 in linear units; safe for y down to 0 and up to ~1e5."""
    u = math.sqrt(max(float(y), 1e-300))
    return 1.0/math.expm1(u) if u < 700.0 else 0.0

def nu_routeA(y):
    y = np.maximum(np.asarray(y, dtype=float), 1e-300); return 1.0/(1.0 - np.exp(-np.sqrt(y)))

def dg_retired(gN, a0):
    """MUTATION CONTROL KERNEL: the retired nu = sqrt(1+1/y).  Its tail nu-1 -> 1/(2y) gives the CONSTANT
    sunward a_0/2 that Blanchet & Novak 2011 (arXiv:1105.5815 p.8) call 'ruled out because not seen from the
    motion of planets'.  Retired for exactly this reason (STANDING.md sec 0, 2026-08-02)."""
    y = np.asarray(gN, dtype=float)/a0
    return (np.sqrt(1.0 + 1.0/y) - 1.0)*np.asarray(gN, dtype=float)


# ============================================================================================================
P(""); P("-"*118)
P("PART A -- the modified-gravity anomalous acceleration vs heliocentric distance, and Cassini")
P("-"*118)

# JPL Keplerian elements for approximate positions of the major planets (Standish & Williams,
# https://ssd.jpl.nasa.gov/planets/approx_pos.html), J2000.
# sigma(perihelion advance), mas/yr: the tighter of Pitjeva & Pitjev 2013 (EPM) and Fienga+ 2011b (INPOP10a)
# as tabulated in Fienga & Minazzoli 2024, Living Rev. Relativ. 27:1 (arXiv:2303.01821) Table 10 and banked in
# prep_2026/planetary_doors/BOUNDS.md sec 1.2, together with the delta-g values re-derived here.
PLANETS = [
    ("Mercury",   0.38709927,  0.20563593,   0.006,    4.6e-14),
    ("Venus",     0.72333566,  0.00677672,   0.015,    8.0e-14),
    ("Earth",     1.00000261,  0.01671123,   0.0019,   8.7e-15),
    ("Mars",      1.52371034,  0.09339410,   0.00037,  1.4e-15),
    ("Jupiter",   5.20288700,  0.04838624,   0.28,     5.6e-13),
    ("Saturn",    9.53667594,  0.05386179,   0.0047,   7.0e-15),
]

def kepler_period(a_m): return 2.0*math.pi*math.sqrt(a_m**3/GM_SUN)

def dg_bound_from_wdot(a_m, e, sigma_mas_per_yr):
    """Invert the exact secular result for a CONSTANT sunward perturbation (derived and validated in B1b):
       |Delta omega| per orbit = 2 pi dg a^2 sqrt(1-e^2) / GM.
    This is the Gauss orbit-averaged conversion BOUNDS.md sec 1.2 used; A1a checks it reproduces theirs."""
    P_yr = kepler_period(a_m)/YR
    return (sigma_mas_per_yr/RAD2MAS)*P_yr*GM_SUN/(2.0*math.pi*a_m**2*math.sqrt(1.0 - e*e))

P(""); info("A1 -- the delta-g bound machinery, validated against the repo's own committed conversion")
P(f"  {'planet':<10}{'a [AU]':>9}{'e':>9}{'sig(wdot) mas/yr':>18}{'delta-g here':>15}{'BOUNDS.md':>12}{'ratio':>8}")
ratios = []
for nm, aAU, e, sw, dgrepo in PLANETS:
    dg = dg_bound_from_wdot(aAU*AU, e, sw); ratios.append(dg/dgrepo)
    P(f"  {nm:<10}{aAU:>9.5f}{e:>9.5f}{sw:>18.5f}{dg:>15.3e}{dgrepo:>12.1e}{dg/dgrepo:>8.3f}")
worst_A1 = float(max(abs(np.log10(ratios))))
ck("A1a  the delta-g conversion reproduces the repo's committed per-planet bounds",
   worst_A1 < 0.03,
   f"worst |log10 ratio| = {worst_A1:.4f} over 6 planets (all within 3%, the rounding of the 1-2 significant "
   f"figures BOUNDS.md quotes).  This validates the Gauss secular machinery used throughout Part B against an "
   f"independently committed derivation BEFORE it is used for anything")

P(""); info("A2 -- Route A's anomalous acceleration at every planet, both footings")
P(f"  {'planet':<10}{'g_N [m/s2]':>12}{'y=g/a0':>11}{'sqrt(y)':>9}{'log10 dg':>11}{'bound':>10}{'log10 margin':>14}")
margins = {}
for fn, a0 in A0.items():
    P(f"  --- footing {fn}: a_0 = {a0:.3e} m/s^2 ---")
    worst = 1e99
    for nm, aAU, e, sw, dgrepo in PLANETS:
        gN = GM_SUN/(aAU*AU)**2; y = gN/a0
        L = float(log10_dg_routeA(gN, a0)); bd = dg_bound_from_wdot(aAU*AU, e, sw)
        m = math.log10(bd) - L; worst = min(worst, m)
        P(f"  {nm:<10}{gN:>12.3e}{y:>11.3e}{math.sqrt(y):>9.1f}{L:>11.1f}{bd:>10.1e}{m:>14.1f}")
    margins[fn] = worst
gS = GM_SUN/(9.53667594*AU)**2
sat_margin = math.log10(dg_bound_from_wdot(9.53667594*AU, 0.05386179, 0.0047)) \
             - float(log10_dg_routeA(gS, A0["canonical"]))
ck("A2a  Route A PASSES every per-planet ephemeris bound, and not marginally",
   min(margins.values()) > 100.0,
   f"the SMALLEST margin over all six planets and both footings is 10^{min(margins.values()):.0f} (Saturn on the "
   f"alt footing -- Saturn because it is the most distant, hence lowest-y, well-bounded planet); Saturn "
   f"canonical sits at 10^{sat_margin:.0f} and Jupiter, the weakest-BOUNDED planet, at 10^596.  This CONFIRMS the "
   f"repo's committed relief (mi_route_a_exponential_kernel_2026.py R2a, ~3.3e13x vs alpha=2) in ABSOLUTE "
   f"terms rather than as a ratio: under Route A there is no isotropic solar-system liability at any "
   f"conceivable measurement precision, now or ever")

P(""); info("A3 -- MUTATION CONTROL: the same machinery on the RETIRED kernel nu = sqrt(1+1/y) must FAIL")
P(f"  {'planet':<10}{'a0/2 anom':>12}{'bound':>10}{'excluded by':>13}{'KERNEL_PLANETS':>16}")
mut_excl = {}
BANKED = {"Mercury": 1018, "Earth": 5380, "Mars": 33436, "Saturn": 6687}
for fn, a0 in A0.items():
    P(f"  --- footing {fn} ---")
    ex = []
    for nm, aAU, e, sw, dgrepo in PLANETS:
        gN = GM_SUN/(aAU*AU)**2; dg = float(dg_retired(gN, a0)); bd = dg_bound_from_wdot(aAU*AU, e, sw)
        ex.append(dg/bd)
        ref = BANKED.get(nm) if fn == "canonical" else None
        P(f"  {nm:<10}{dg:>12.3e}{bd:>10.1e}{dg/bd:>13.0f}{(str(ref) if ref else '--'):>16}")
    mut_excl[fn] = max(ex)
mars_ex = float(dg_retired(GM_SUN/(1.52371034*AU)**2, A0["canonical"])) \
          / dg_bound_from_wdot(1.52371034*AU, 0.09339410, 0.00037)
sat_ex = float(dg_retired(gS, A0["canonical"])) / dg_bound_from_wdot(9.53667594*AU, 0.05386179, 0.0047)
ck("A3a  MUTATION CONTROL fires: the retired kernel is excluded, by the repo's own banked factors",
   min(mut_excl.values()) > 1e3 and abs(mars_ex/33436.0 - 1.0) < 0.05 and abs(sat_ex/6687.0 - 1.0) < 0.05,
   f"the retired nu=sqrt(1+1/y) gives a CONSTANT a_0/2 sunward anomaly excluded up to {mut_excl['canonical']:.0f}x "
   f"(canonical) / {mut_excl['alt']:.0f}x (alt); Mars reproduces KERNEL_PLANETS.md's banked 33436x to "
   f"{100*abs(mars_ex/33436.0-1.0):.1f}% and Saturn its 6687x to {100*abs(sat_ex/6687.0-1.0):.1f}%.  The A2a "
   f"checks are therefore capable of failing -- they fail here, on a kernel that differs from Route A only in "
   f"HOW IT APPROACHES NEWTON and in nothing else")

P(""); info("A4 -- where the isolated Route A anomaly PEAKS, and where the external field takes over")
P("  With u = sqrt(y) = r_M/r and g_N = a_0 u^2, the anomaly is dg = a_0 u^2/(e^u - 1).  Maximising gives")
P("  2(e^u - 1) = u e^u, i.e. e^u (2 - u) = 2.  (The naive answer u = 2 drops the 1/(e^u-1) denominator and")
P("  is wrong by 25% in radius -- the numerical argmax below is what caught it.)")
u_star = brentq(lambda u: math.exp(u)*(2.0 - u) - 2.0, 0.5, 1.99)
peak_frac = u_star**2/(math.exp(u_star) - 1.0)
num_err = None
for fn, a0 in A0.items():
    rM = math.sqrt(GM_SUN/a0); r_pk = rM/u_star; dg_pk = a0*peak_frac
    r_ext = math.sqrt(GM_SUN/G_EXT)
    rr = np.logspace(math.log10(0.05*AU), math.log10(1e6*AU), 600001)
    r_num = rr[int(np.argmax(log10_dg_routeA(GM_SUN/rr**2, a0)))]
    err = 100*abs(r_num/r_pk - 1.0)
    P(f"  {fn:>10}: u* = {u_star:.6f} (y* = {u_star**2:.4f})  ->  r_peak = {r_pk/AU:7.1f} AU, "
      f"dg_peak = {dg_pk:.3e} m/s^2 = {peak_frac:.4f} a_0   [numerical argmax {r_num/AU:7.1f} AU, {err:.4f}% off]")
    P(f"  {'':>10}  r_M = sqrt(GM/a0) = {rM/AU:6.0f} AU;  external field takes over at "
      f"r_ext = sqrt(GM/g_ext) = {r_ext/AU:5.0f} AU;  g_ext/g_N at the peak = {G_EXT/(a0*u_star**2):.2f}")
    if fn == "canonical":
        pk_can, rpk_can, rM_can, rext_can, num_err = dg_pk, r_pk/AU, rM/AU, r_ext/AU, err
        gratio_pk = G_EXT/(a0*u_star**2)
ck("A4a  the anomaly peaks at the exact root of e^u(2-u)=2, at ~5000 AU, and never exceeds ~7e-11 m/s^2",
   num_err < 0.5 and pk_can < 1e-10,
   f"analytic u* = {u_star:.4f} confirmed by numerical argmax to {num_err:.4f}%.  Peak dg = {pk_can:.2e} m/s^2 "
   f"= {peak_frac:.3f} a_0 at {rpk_can:.0f} AU (canonical).  THIS IS THE CEILING ON THE WHOLE EFFECT: no "
   f"heliocentric distance, at any eccentricity, on either footing, produces a larger anomalous acceleration "
   f"than {A0['alt']*peak_frac:.2e} m/s^2.  Caveat carried forward: the external field is already "
   f"{gratio_pk:.2f} of the solar field at the peak (crossover {rext_can:.0f} AU), so the isolated calculation "
   f"OVERSTATES the peak by up to a factor ~2 (doubling y raises sqrt(y) by 1.41 and divides nu-1 by ~1.9) "
   f"and is INVALID beyond ~{rext_can:.0f} AU -- the Oort cloud is "
   f"EFE-governed, which is the regime h12_h14_satellites_and_oort.py covers, not this one")

P(""); info("A5 -- THE PART THE EXPONENTIAL TAIL DOES NOT SAVE: the external-field quadrupole Q_2")
P("  Q_2 is NOT a property of the field at Saturn.  It is the constant tidal quadrupole that the nonlinear")
P("  Poisson equation's external boundary condition at r_M ~ 8000 AU imprints on the WHOLE interior.  There")
P("  y ~ 1, so there is no exponential suppression and Route A inherits the standard MOND-class value.")
P("  Desmond, Hees & Famaey 2024 (arXiv:2401.04796) eq (12):")
P("     q = (3/2) Int_0^inf dv Int_-1^1 dxi (nu-1)[eN(3xi-5xi^3) + v^2(1-3xi^2)],  nu at sqrt(eN^2+v^4+2 eN v^2 xi)")
P("  with eN nu(eN) = etilde = g_ext/a_0, and Q_2 = -(3 a_0^{3/2})/(2 sqrt(GM)) q.  Their published Fig. 1")
P("  anchors are quoted for nu_RAR(y) = 1/(1-exp(-sqrt y)) -- which IS Route A's kernel, so this is a direct")
P("  published pin with no shape assumption imported.")

def q_eq12(etilde, nufun, vmax=200.0):
    eN = brentq(lambda x: x*nufun(x) - etilde, 1e-9, 1e4)
    def ig(xi, v):
        D = eN*eN + v**4 + 2.0*eN*v*v*xi
        if D <= 0: return 0.0
        return (float(nufun(math.sqrt(D))) - 1.0)*(eN*(3*xi - 5*xi**3) + v*v*(1.0 - 3.0*xi*xi))
    val, _ = integrate.dblquad(ig, 0.0, vmax, lambda v: -1.0, lambda v: 1.0, epsabs=1e-11, epsrel=1e-9)
    return 1.5*val, eN

P(""); P(f"  {'etilde':>8}{'published q':>13}{'q here':>10}{'rel err':>10}   (Desmond+2024 Fig. 1 caption)")
anch_err = []
for et, qp in ((1.0, 0.094), (1.5, 0.159), (2.0, 0.221)):
    qh, _ = q_eq12(et, nu_routeA); anch_err.append(abs(abs(qh)/qp - 1.0))
    P(f"  {et:>8.1f}{qp:>13.3f}{abs(qh):>10.4f}{abs(qh)/qp - 1.0:>10.3%}")
ck("A5a  the eq-(12) quadrupole integral is pinned on the published anchors, for THIS kernel",
   max(anch_err) < 0.01,
   f"worst relative error vs Desmond+2024's published q(1)=0.094, q(1.5)=0.159, q(2)=0.221 is "
   f"{100*max(anch_err):.2f}%.  Independently re-derived here from the paper's equation, and it also matches "
   f"the repo's committed transcription in branchB_q2_gate_2026/verify_laneC_paper_anchor.py")

Q2_CEIL_2SIG, Q2_CEN, Q2_SIG = 5.2e-27, 1.6e-27, 1.8e-27   # Park+2026, arXiv:2602.17884, full DE440
Q2_H14 = 9.0e-27                                            # Hees+2014, PRD 89 102002, arXiv:1402.6950
Q2_MI  = 7.4e-34                                            # cassini_mi_evasion_2026/, committed, OLD kernel
P(""); P(f"  {'footing':>10}{'etilde':>9}{'eN':>9}{'q':>9}{'Q2 [s^-2]':>12}{'/ceiling':>10}{'sigma':>9}")
Q2o = {}
for fn, a0 in A0.items():
    et = G_EXT/a0; q, eN = q_eq12(et, nu_routeA)
    Q2 = abs(3.0*a0**1.5/(2.0*math.sqrt(GM_SUN))*q)
    Q2o[fn] = (Q2, Q2/Q2_CEIL_2SIG, (Q2 - Q2_CEN)/Q2_SIG)
    P(f"  {fn:>10}{et:>9.3f}{eN:>9.3f}{abs(q):>9.4f}{Q2:>12.3e}{Q2/Q2_CEIL_2SIG:>10.2f}{(Q2-Q2_CEN)/Q2_SIG:>9.1f}")
P(f"  measured: Q2 = (1.6 +- 1.8)e-27 s^-2 (Park+2026); 2-sigma ceiling {Q2_CEIL_2SIG:.1e}; earlier Hees+2014")
P(f"  ceiling {Q2_H14:.1e}.  Blanchet & Novak 2011 class values for other mu: 2.2e-26 to 4.1e-26.")
P(f"  CONTRAST, the modified-INERTIA arm: cassini_mi_evasion_2026/ computes the true l=2 quadrupole at")
P(f"  {Q2_MI:.1e} s^-2 = {Q2_MI/Q2_CEIL_2SIG:.0e} of the ceiling.  (Committed on the OLD nu = sqrt(1+1/y); the")
P(f"  suppression there is the deep-Newtonian nu-1 at Saturn, which Route A makes SMALLER still, so the MI")
P(f"  evasion is not weakened by the kernel change.  Not recomputed here -- flagged, not claimed.)")
ck("A5b  Route A passes the Cassini external-field quadrupole bound",
   max(v[1] for v in Q2o.values()) < 1.0,
   f"IT DOES NOT.  Q_2 = {Q2o['canonical'][0]:.2e} (canonical) / {Q2o['alt'][0]:.2e} (alt) s^-2, i.e. "
   f"{Q2o['canonical'][1]:.1f}x / {Q2o['alt'][1]:.1f}x the Park+2026 2-sigma ceiling and formally "
   f"+{Q2o['canonical'][2]:.0f} / +{Q2o['alt'][2]:.0f} sigma.  Route A's exponential tail discharges the "
   f"ISOTROPIC ephemeris liability (A2a) and does NOTHING here, because Q_2 is set at r_M ~ {rM_can:.0f} AU "
   f"where y ~ 1.  The two must never be conflated.  This CONFIRMS rather than discovers -- STANDING.md "
   f"already carries a 3-15 sigma Cassini Q_2 tension for the AeST(=MG) realisation and Desmond+2024 quote "
   f"8.7 sigma fiducial, 1.9 sigma with bulge galaxies removed -- but it establishes it ON ROUTE A "
   f"SPECIFICALLY, on the published anchors for Route A's own kernel.  AND IT IS FORK-RELEVANT: the MI arm "
   f"evades the same bound by {Q2_MI/Q2_CEIL_2SIG:.0e}, so this observable DOES separate the arms, and it "
   f"points AWAY from modified gravity")


# ============================================================================================================
P(""); P("-"*118)
P("PART B -- the discriminant: anomalous perihelion precession as an exact function of (a, e)")
P("-"*118)
P("  In modified GRAVITY the correction is central, so the precession follows from the force alone.  To first")
P("  order, Gauss's form of the Lagrange planetary equations for a purely radial perturbing acceleration,")
P("  integrated over one orbit in true anomaly f:")
P("")
P("      Delta(omega) = (1/(GM e)) Int_0^{2pi} dg(r(f)) r(f)^2 cos f  df ,      r = a(1-e^2)/(1+e cos f)")
P("")
P("  with dg > 0 meaning EXTRA INWARD.  A pure function of (a, e) and of nothing else: no trajectory memory,")
P("  no dependence on where the orbit has been.  THAT is the modified-gravity arm's content, and it is what a")
P("  trajectory-dependent modification must violate.")

def dperi_log(a_m, e, log10dg_of_r, nf=200001):
    """(sign, log10|Delta omega|) per orbit for a radial perturbation whose log10 is log10dg_of_r(r).
    Returned in LOG form because the Route A integrand spans hundreds of decades along one orbit and the
    result itself underflows float64 for any orbit inside ~30 AU -- taking a ratio of two underflowed zeros
    is how the first version of this table printed 'inf'."""
    f = np.linspace(0.0, 2.0*math.pi, nf)
    r = a_m*(1.0 - e*e)/(1.0 + e*np.cos(f))
    L = np.asarray(log10dg_of_r(r), dtype=float); Lm = float(np.max(L))
    w = 10.0**(L - Lm)*r*r*np.cos(f)
    I = float(np.trapezoid(w, f) if hasattr(np, "trapezoid") else np.trapz(w, f))
    return (1.0 if I > 0 else -1.0), Lm + math.log10(abs(I)) - math.log10(GM_SUN*e)

def dperi_per_orbit(a_m, e, log10dg_of_r, nf=200001):
    """Linear-units wrapper; underflows to 0 below ~1e-300, which is why B3 uses dperi_log instead."""
    sg, L = dperi_log(a_m, e, log10dg_of_r, nf)
    return sg*(10.0**L if L > -300.0 else 0.0)

P(""); info("B1 -- the integrator, validated against two independent closed forms with opposite signs")
gr_err, cst_err = [], []
for a_AU, e in ((0.38709927, 0.20563593), (9.53667594, 0.05386179), (506.2, 0.8496)):
    a_m = a_AU*AU; p = a_m*(1 - e*e); h2 = GM_SUN*p
    ana = 6.0*math.pi*GM_SUN/(C_LIGHT**2*p)
    num = dperi_per_orbit(a_m, e, lambda r: np.log10(3.0*GM_SUN*h2/(C_LIGHT**2*r**4)))
    gr_err.append(abs(num/ana - 1.0))
    P(f"  GR      a={a_AU:9.4f} AU e={e:.4f}: analytic {ana:+.9e}  numeric {num:+.9e}  rel {num/ana-1:+.2e}")
for a_AU, e in ((0.38709927, 0.20563593), (9.53667594, 0.05386179), (506.2, 0.8496)):
    a_m = a_AU*AU; dg0 = 1e-13
    ana = -2.0*math.pi*dg0*a_m**2*math.sqrt(1 - e*e)/GM_SUN
    num = dperi_per_orbit(a_m, e, lambda r: np.full_like(r, math.log10(dg0)))
    cst_err.append(abs(num/ana - 1.0))
    P(f"  const   a={a_AU:9.4f} AU e={e:.4f}: analytic {ana:+.9e}  numeric {num:+.9e}  rel {num/ana-1:+.2e}")
ck("B1a  the precession integrator reproduces the GR closed form 6 pi GM/(c^2 a(1-e^2))",
   max(gr_err) < 1e-6, f"worst relative error {max(gr_err):.2e} over e = 0.054 to 0.850, a = 0.39 to 506 AU")
ck("B1b  and the constant-sunward closed form -2 pi dg a^2 sqrt(1-e^2)/GM used for the Part A bounds",
   max(cst_err) < 1e-6,
   f"worst relative error {max(cst_err):.2e}.  Note the SIGN: a constant extra inward force precesses the "
   f"perihelion RETROGRADE, because it falls off slower than 1/r^2, while the GR 1/r^4 term is prograde.  Two "
   f"closed forms with opposite signs and different r-powers, both reproduced -- the integrator is not "
   f"tuned to either")

P(""); info("B2 -- MUTATION CONTROL on the integrator: a perturbation that MUST give exactly zero")
P("  A dg proportional to 1/r^2 is nothing but a rescaling of GM.  It cannot precess anything, and if the")
P("  integrator carried a spurious constant it would show up here as a fake precession.  A 1/r^3 term of the")
P("  same amplitude is the reference that shows the integrator is not simply returning zero.")
zero_err = []
for a_AU, e in ((1.0, 0.3), (506.2, 0.8496)):
    a_m = a_AU*AU
    num = dperi_per_orbit(a_m, e, lambda r: np.log10(1e-13*(AU/r)**2))
    ref = dperi_per_orbit(a_m, e, lambda r: np.log10(1e-13*(AU/r)**3))
    zero_err.append(abs(num)/abs(ref))
    P(f"  a={a_AU:7.2f} AU e={e:.4f}:  1/r^2 (pure GM rescale) {num:+.3e}   1/r^3 reference {ref:+.3e}   "
      f"ratio {abs(num)/abs(ref):.2e}")
ck("B2a  MUTATION CONTROL: a 1/r^2 perturbation gives exactly zero precession, a 1/r^3 one does not",
   max(zero_err) < 1e-9,
   f"the 1/r^2 case returns {max(zero_err):.1e} of the 1/r^3 reference.  This is a THEOREM as well as a "
   f"control, and Part D uses it: any modification that merely rescales the effective GM along an orbit is "
   f"invisible to perihelion precession, no matter how large it is")

P(""); info("B3 -- THE DISCRIMINANT FUNCTION: modified-gravity precession at fixed a, circular vs eccentric")
P("  Delta(omega) per orbit and the rate in mas/yr, for e = 0.01 and e = 0.90 at the same semi-major axis.")
P("  The ratio is the modified-gravity arm's OWN eccentricity signature: it exists entirely because the")
P("  eccentric orbit's aphelion samples a lower acceleration.  Canonical footing; alt differs only in scale.")
P("  Everything is in log10 because the values underflow float64 inside ~30 AU.  The last column flags rows")
P("  where the galactic external field at aphelion exceeds 30%% of the Sun's (crossover r_ext = %.0f AU), so" % (math.sqrt(GM_SUN/G_EXT)/AU))
P("  this isolated calculation stops being valid -- those rows are shown for shape only, not as predictions.")
P(f"  {'a [AU]':>10}{'log10|dw| e=.01':>17}{'log10|dw| e=.9':>16}{'log10 ratio':>13}"
  f"{'log10 rate(e=.9)':>18}{'EFE?':>7}   (rad/orbit, mas/yr)")
a0c = A0["canonical"]
R_EXT = math.sqrt(GM_SUN/G_EXT)
rows = []
for a_AU in (1.0, 5.0, 10.0, 30.0, 100.0, 300.0, 1000.0, 3000.0, 10000.0):
    a_m = a_AU*AU; Pyr = kepler_period(a_m)/YR
    _, L1 = dperi_log(a_m, 0.01, lambda r: log10_dg_routeA(GM_SUN/r**2, a0c))
    _, L9 = dperi_log(a_m, 0.90, lambda r: log10_dg_routeA(GM_SUN/r**2, a0c))
    Lrate = L9 - math.log10(Pyr) + math.log10(RAD2MAS)
    efe = "INVALID" if G_EXT/(GM_SUN/(a_m*1.9)**2) > 0.3 else ""
    rows.append((a_AU, L1, L9, L9 - L1, Lrate, efe))
    P(f"  {a_AU:>10.0f}{L1:>17.2f}{L9:>16.2f}{L9-L1:>13.2f}{Lrate:>18.2f}  {efe:>7}")
rat_10 = 10.0**[r for r in rows if r[0] == 10.0][0][3]
inner = [10.0**r[4] for r in rows if r[0] <= 100.0]
MARS_PREC = 0.00037                      # mas/yr, the sharpest perihelion-advance sigma in astronomy
BAR = MARS_PREC*1e-6                     # the bar: one part in a million OF THE BEST EXISTING MEASUREMENT
ck("B3a  modified gravity DOES carry a huge eccentricity signature -- in ratio, though not in magnitude",
   rat_10 > 1e50,
   f"at a = 10 AU the e=0.9 precession exceeds the e=0.01 one by {rat_10:.1e}, because aphelion at 19 AU sits "
   f"at sqrt(y) = {math.sqrt(GM_SUN/(19*AU)**2/a0c):.0f} against {math.sqrt(GM_SUN/(10*AU)**2/a0c):.0f} at "
   f"10 AU and the kernel is exp(-sqrt y).  So it is NOT true that modified gravity is eccentricity-blind: "
   f"the CENTRAL FORCE is blind, the ORBIT AVERAGE is not.  Recorded because the naive statement of the fork "
   f"gets this backwards")
ck("B3b  but the discriminant is vacuous inside 100 AU -- the signal is not small, it is absent",
   max(inner) < BAR,
   f"the largest modified-gravity precession rate anywhere inside 100 AU, at the most favourable eccentricity "
   f"e = 0.9, is {max(inner):.1e} mas/yr.  The bar here is set by the MEASUREMENT, not by the result: one "
   f"part in 1e6 of Mars's {MARS_PREC} mas/yr, the sharpest perihelion sigma in astronomy (Pitjeva & Pitjev "
   f"2013).  The actual shortfall is 10^{math.log10(MARS_PREC/max(inner)):.0f}.  No measurement, existing or "
   f"conceivable, reaches it")


# ============================================================================================================
P(""); P("-"*118)
P("PART C -- which real objects give the best lever, in (a, e) space")
P("-"*118)
P("  Three readings of the same kernel are compared on every orbit.  They bracket the fork:")
P("    modified GRAVITY : dg = (nu(y(r)) - 1) g_N(r), keyed to the LOCAL distance      [the field at a point]")
P("    MI-A envelope    : dg = a CONSTANT equal to the modified-gravity value AT APHELION, held all orbit")
P("    MI-B envelope    : nu itself FROZEN at its aphelion value, i.e. dg = (nu(y_apo)-1) g_N(r)")
P("  MI-A and MI-B are UPPER ENVELOPES, deliberately extreme (Milgrom 2009 MNRAS 399 474: MI anomalies attach")
P("  to trajectories that reach low-acceleration regions).  A real nonlocal MI kernel lands between them and")
P("  the modified-gravity curve.  If the most generous reading is unmeasurable, every reading is.")
P("  NOTE, and it is load-bearing: by the B2a theorem MI-B is a pure GM rescale and PRECESSES NOTHING.  It is")
P("  therefore not a competitor in Part B at all; it reappears in D3 as a different observable.")

OBJECTS = [
    (0.38709927, 0.20563593, "Mercury",        "JPL mean elements"),
    (9.53667594, 0.05386179, "Saturn",         "JPL mean elements"),
    (30.0699228, 0.00859048, "Neptune",        "JPL mean elements"),
    (17.834,     0.96714,    "1P/Halley",      "JPL SBDB"),
    (67.864,     0.43607,    "136199 Eris",    "JPL SBDB"),
    (266.0,      0.690,      "2012 VP113",     "Trujillo & Sheppard 2014, Nature 507, 471"),
    (506.2,      0.8496,     "90377 Sedna",    "Brown, Trujillo & Rabinowitz 2004, ApJ 617, 645"),
    (2500.0,     0.99800,    "LPC a=2500 AU",  "generic long-period comet, q = 5 AU"),
    (20000.0,    0.99995,    "Oort-spike LPC", "generic, a = 2e4 AU, q = 1 AU"),
]
P("")
P(f"  {'object':<16}{'a [AU]':>10}{'e':>9}{'q [AU]':>8}{'Q [AU]':>9}{'MG log10 dg':>13}{'  at q':>10}"
  f"{'MI-A dg':>11}{'MI-B eps':>11}{'P [yr]':>11}{'EFE?':>9}")
lever = []
for aAU, e, nm, src in OBJECTS:
    a_m = aAU*AU; q = a_m*(1 - e); Q = a_m*(1 + e)
    LQ = float(log10_dg_routeA(GM_SUN/Q**2, a0c))          # MG at aphelion (the orbit's largest MG value)
    Lq = float(log10_dg_routeA(GM_SUN/q**2, a0c))          # MG at perihelion (where the object is observed)
    eps = numinus1_routeA(GM_SUN/Q**2/a0c)                 # MI-B: nu-1 frozen at aphelion
    dgA = eps*GM_SUN/Q**2                                  # MI-A: that value as a constant acceleration
    Pyr = kepler_period(a_m)/YR
    efe = "INVALID" if G_EXT/(GM_SUN/Q**2) > 0.3 else ""
    lever.append((nm, aAU, e, q/AU, Q/AU, LQ, Lq, dgA, eps, Pyr))
    P(f"  {nm:<16}{aAU:>10.2f}{e:>9.5f}{q/AU:>8.2f}{Q/AU:>9.1f}{LQ:>13.1f}{Lq:>10.1f}{dgA:>11.2e}"
      f"{eps:>11.2e}{Pyr:>11.1f}{efe:>9}")
P("    'MG log10 dg' is at aphelion, ' at q' at perihelion -- their difference is how far apart the readings")
P("     sit ON THE SAME ORBIT, which is the entire discriminant.  MI-B eps is dimensionless (a GM fraction).")
P("     'EFE INVALID' marks orbits where the galactic external field at aphelion exceeds 30% of the Sun's")
P("     (crossover r_ext = %.0f AU), so this isolated calculation does not apply -- the two long-period-comet" % (math.sqrt(GM_SUN/G_EXT)/AU))
P("     rows are there to locate the optimum in (a,e), NOT as predictions.  Sedna's aphelion (936 AU) is at")
P("     g_ext/g_N = %.3f and is safely inside." % (G_EXT/(GM_SUN/(506.2*1.8496*AU)**2)))

sed = [L for L in lever if L[0] == "90377 Sedna"][0]
ck("C1a  the lever exists and it is enormous IN RATIO: on Sedna the readings differ by >10^25",
   (sed[5] - sed[6]) > 25.0,
   f"Sedna is observed near perihelion (q = {sed[3]:.0f} AU) where modified gravity predicts 10^{sed[6]:.0f} "
   f"m/s^2 -- exactly nothing -- while an aphelion-keyed modified inertia carries {sed[7]:.1e} m/s^2 around "
   f"the whole orbit.  A ratio of 10^{sed[5]-sed[6]:.0f}.  The fork is not subtle on this object; it is the "
   f"difference between zero and something.  The whole question is whether the something is measurable")

P(""); info("C2 -- where in (a, e) the arms differ MOST in ABSOLUTE terms, and what object sits there")
P("  The envelope is maximised when the APHELION sits on the anomaly's peak (A4a).  With e -> 1 that means")
P("  a = r_peak/2: a long-period comet.  Modified gravity's value at such an object's PERIHELION, where it is")
P("  actually observed, is identically zero.  So the theoretical optimum of this entire test IS the")
P("  long-period comet population -- and D1 shows why that optimum is unusable.")
opt = {}
for fn, a0 in A0.items():
    r_pk = math.sqrt(GM_SUN/a0)/u_star/AU; a_opt = r_pk/2.0
    dg_opt = a0*peak_frac; a_m = a_opt*AU; e_opt = 1.0 - 5.0/a_opt
    dw = -2.0*math.pi*dg_opt*a_m**2*math.sqrt(1 - e_opt**2)/GM_SUN
    opt[fn] = (a_opt, dg_opt, abs(dw), kepler_period(a_m)/YR)
    P(f"  {fn:>10}: optimum a = {a_opt:6.0f} AU (aphelion on the peak); at q = 5 AU, e = {e_opt:.5f}: "
      f"MI-A Delta(omega) = {abs(dw):.3e} rad/orbit = {abs(dw)*180/math.pi:.2f} deg/orbit, P = {opt[fn][3]:.0f} yr")
ck("C2a  the theoretical optimum is a ~2500 AU long-period comet carrying ~1 degree per orbit",
   opt["canonical"][2]*180/math.pi > 0.3,
   f"{opt['canonical'][2]*180/math.pi:.2f} deg/orbit (canonical) / {opt['alt'][2]*180/math.pi:.2f} (alt) at "
   f"a = {opt['canonical'][0]:.0f} AU, q = 5 AU.  That is a LARGE number, not a small one -- which is why the "
   f"shutdown in Part D is a statement about MEASURABILITY, not about the size of the physics.  Recorded as "
   f"the ceiling any future experiment on this route would be aiming at")


# ============================================================================================================
P(""); P("-"*118)
P("PART D -- how far short, quantified; and the one channel that is not shut")
P("-"*118)

P(""); info("D1 -- the theoretical optimum: killed three times over by comet physics")
# Nongravitational acceleration: Marsden, Sekanina & Yeomans 1973, AJ 78, 211 define the standard g(r) law;
# typical fitted A1 for long-period comets is 1e-8 to 1e-7 AU/day^2 at 1 AU (JPL SBDB nongrav solutions).
A1_AU_D2 = 1e-8
A1_SI = A1_AU_D2*AU/86400.0**2
for q_AU in (1.0, 5.0):
    ng = A1_SI/q_AU**2
    P(f"  outgassing at q = {q_AU:.0f} AU: A1 = {A1_AU_D2:.0e} AU/d^2 -> {ng:.2e} m/s^2  vs the ABSOLUTE peak "
      f"anomaly {pk_can:.2e} m/s^2  ->  outgassing is {ng/pk_can:.0f}x larger")
ng5 = A1_SI/25.0
DELTA_INV_A = 1e-4     # AU^-1 per perihelion passage, from hunt_2026/h12_h14_satellites_and_oort.out
P(f"  per-passage planetary scatter in 1/a is ~{DELTA_INV_A:.0e} AU^-1 (h12_h14_satellites_and_oort.out): "
  f"{100*DELTA_INV_A*opt['canonical'][0]:.0f}% of 1/a for an a = {opt['canonical'][0]:.0f} AU comet")
P(f"  and a long-period comet is seen for ONE apparition, so a per-orbit secular precession has no second")
P(f"  epoch to be differenced against.  Three independent kills, any one of which suffices.")
ck("D1a  the long-period-comet optimum is usable: the signal exceeds the outgassing",
   ng5/pk_can < 1.0,
   f"IT IS NOT.  A typical A1 = 1e-8 AU/d^2 gives {ng5:.1e} m/s^2 at q = 5 AU against the ABSOLUTE CEILING of "
   f"the anomaly {pk_can:.1e} m/s^2 -- {ng5/pk_can:.0f}x larger -- and A1 is fitted per comet to 10-30%, so "
   f"the outgassing UNCERTAINTY ALONE is ~{0.2*ng5/pk_can:.0f}x the entire signal.  Add one apparition and a "
   f"{100*DELTA_INV_A*opt['canonical'][0]:.0f}% per-passage scatter in 1/a and the route is not marginal, it "
   f"is closed")

P(""); info("D2 -- Sedna, the best inert lever that exists: the orbit-fit absorption calculation")
P("  Sedna has no outgassing (85 AU, inactive), a ~25-yr observed arc (2001 precovery to 2026), and the")
P("  largest well-determined aphelion of any inert object.  A purely radial perturbation preserves the orbit")
P("  plane, so only the 4 in-plane elements (a, e, omega, M0) are free.  Two observables are used: the")
P("  heliocentric longitude, and ln r -- the latter because a TNO's distance IS measured, by the annual")
P("  parallax, with sigma(ln r) = sigma(theta) * r/AU.  No range measurement is assumed.")

A_SED, E_SED, R_NOW, T_ARC = 506.2*AU, 0.8496, 85.0*AU, 25.0*YR
E0 = -math.acos((1.0 - R_NOW/A_SED)/E_SED)          # pre-perihelion branch (Sedna's perihelion is ~2076)
M0_SED = E0 - E_SED*math.sin(E0)
NEP = 401

def kepler_obs(a_m, e, om, M0, t, gm=GM_SUN):
    n = math.sqrt(gm/a_m**3); M = M0 + n*np.asarray(t); E = M.copy()
    for _ in range(200): E = E - (E - e*np.sin(E) - M)/(1.0 - e*np.cos(E))
    f = 2.0*np.arctan2(math.sqrt(1+e)*np.sin(E/2.0), math.sqrt(1-e)*np.cos(E/2.0))
    return np.concatenate([np.unwrap(f + om), np.log(a_m*(1.0 - e*np.cos(E)))])

def build(T):
    t = np.linspace(-T/2.0, T/2.0, NEP)
    base = kepler_obs(A_SED, E_SED, 0.0, M0_SED, t)
    p0 = [A_SED, E_SED, 0.0, M0_SED]; step = [A_SED*1e-6, 1e-7, 1e-7, 1e-9]
    cols = []
    for i in range(4):
        pp = list(p0); pm = list(p0); pp[i] += step[i]; pm[i] -= step[i]
        cols.append((kepler_obs(*pp, t) - kepler_obs(*pm, t))/(2.0*step[i]))
    return t, base, np.vstack(cols).T

def postfit(sig, D, sig_th_mas):
    """Least-squares removal of the 4-element family, with weights.  Columns are normalised before the solve:
    they span ~10 orders and an unnormalised lstsq silently truncates one, which shows up as a fake residual
    (it did, in the first version of this script -- the D2a control is what caught it)."""
    s_th = sig_th_mas/RAD2MAS; s_lr = s_th*R_NOW/AU        # parallax: sigma(ln r) = sigma(theta) * r/AU
    w = np.concatenate([np.full(NEP, 1.0/s_th), np.full(NEP, 1.0/s_lr)])
    A = D*w[:, None]; nrm = np.linalg.norm(A, axis=0); A = A/nrm
    c, *_ = np.linalg.lstsq(A, sig*w, rcond=1e-14)
    res = (sig*w - A @ c)/w
    return res, float(math.sqrt(np.sum(((sig*w - A @ c))**2)))

def integrate_const(dg, t):
    """Two-body plus a constant inward dg, DOP853 at rtol 3e-13.  Initial state from the exact Kepler orbit."""
    n = math.sqrt(GM_SUN/A_SED**3); M = M0_SED + n*t[0]; E = M
    for _ in range(200): E = E - (E - E_SED*math.sin(E) - M)/(1 - E_SED*math.cos(E))
    Ed = n/(1 - E_SED*math.cos(E))
    f0 = 2*math.atan2(math.sqrt(1+E_SED)*math.sin(E/2), math.sqrt(1-E_SED)*math.cos(E/2))
    r0 = A_SED*(1 - E_SED*math.cos(E))
    s0 = [r0*math.cos(f0), r0*math.sin(f0), -A_SED*math.sin(E)*Ed,
          A_SED*math.sqrt(1-E_SED**2)*math.cos(E)*Ed]
    def rhs(_t, s):
        x, y, vx, vy = s; r = math.hypot(x, y); acc = -(GM_SUN/r**3 + dg/r)
        return [vx, vy, acc*x, acc*y]
    sol = solve_ivp(rhs, (t[0], t[-1]), s0, t_eval=t, rtol=3e-13, atol=1e-3, method="DOP853")
    return np.concatenate([np.unwrap(np.arctan2(sol.y[1], sol.y[0])),
                           np.log(np.hypot(sol.y[0], sol.y[1]))])

tt, base, DES = build(T_ARC)
# MUTATION CONTROLS: element changes are BY CONSTRUCTION inside the fit family and must vanish; and the
# numerical integrator with dg = 0 must reproduce the analytic Kepler orbit far below any signal.
c_a = kepler_obs(A_SED*(1 + 1e-9), E_SED, 0.0, M0_SED, tt) - base
c_e = kepler_obs(A_SED, E_SED + 1e-9, 0.0, M0_SED, tt) - base
fa = np.std(postfit(c_a, DES, 100.0)[0][:NEP])/np.std(c_a[:NEP])
fe = np.std(postfit(c_e, DES, 100.0)[0][:NEP])/np.std(c_e[:NEP])
int0 = integrate_const(0.0, tt)
int_err_mas = float(np.std(int0[:NEP] - base[:NEP])*RAD2MAS)
P(f"  control: a*(1+1e-9) absorbed to {fa:.2e} of itself;  e+1e-9 to {fe:.2e};  "
  f"integrator-vs-Kepler at dg=0: {int_err_mas:.2e} mas")
ck("D2a  MUTATION CONTROL: pure element changes are absorbed, and the integrator baseline is clean",
   max(fa, fe) < 1e-5 and int_err_mas < 1e-3,
   f"a 1e-9 fractional change in a is absorbed to {fa:.1e} of itself and a 1e-9 change in e to {fe:.1e} -- so "
   f"the projector is not leaking in-family signal and calling it a detection.  The dg=0 integrator "
   f"reproduces the analytic Kepler orbit to {int_err_mas:.1e} mas, {0.023/int_err_mas:.0f}x below the "
   f"smallest signal reported below.  THIS CONTROL EARNED ITS PLACE: the first version of this script used an "
   f"unnormalised least-squares solve, which truncated a design column and manufactured a 58 mas residual "
   f"out of a perturbation that is provably degenerate")

P("")
P(f"  {'footing':>10}{'reading':>10}{'dg or eps':>12}{'raw [mas]':>12}{'post-fit [mas]':>16}"
  f"{'chi @100mas':>13}{'chi @10mas':>12}")
sedna = {}
for fn, a0 in A0.items():
    Q_sed = A_SED*(1 + E_SED)
    eps = numinus1_routeA(GM_SUN/Q_sed**2/a0)
    dgA = eps*GM_SUN/Q_sed**2
    sA = integrate_const(dgA, tt) - int0
    rA, _ = postfit(sA, DES, 100.0)
    _, chiA100 = postfit(sA, DES, 100.0); _, chiA10 = postfit(sA, DES, 10.0)
    sB = kepler_obs(A_SED, E_SED, 0.0, M0_SED, tt, gm=GM_SUN*(1 + eps)) - base
    rB, chiB100 = postfit(sB, DES, 100.0); _, chiB10 = postfit(sB, DES, 10.0)
    sedna[fn] = dict(eps=eps, dgA=dgA,
                     postA=float(np.std(rA[:NEP])*RAD2MAS), chiA100=chiA100, chiA10=chiA10,
                     postB=float(np.std(rB[:NEP])*RAD2MAS), chiB100=chiB100, chiB10=chiB10)
    P(f"  {fn:>10}{'MI-A':>10}{dgA:>12.3e}{np.std(sA[:NEP])*RAD2MAS:>12.3e}{sedna[fn]['postA']:>16.3e}"
      f"{chiA100:>13.2f}{chiA10:>12.2f}")
    P(f"  {fn:>10}{'MI-B':>10}{eps:>12.3e}{np.std(sB[:NEP])*RAD2MAS:>12.3e}{sedna[fn]['postB']:>16.3e}"
      f"{chiB100:>13.2f}{chiB10:>12.2f}")
P("    raw = the angular signal before any orbit fit; post-fit = what survives the 4-element in-plane fit,")
P("    which is what is actually measurable.  chi is over 401 epochs at the stated per-epoch astrometry.")
P("    100 mas ~ current ground-based for a V=20.6 TNO; 10 mas ~ LSST-class.  BOTH ARE ESTIMATES, not a")
P("    published Sedna orbit covariance, which this repository does not hold.")
ck("D2b  Sedna's 25-yr arc reaches the MI-A precession envelope",
   sedna["canonical"]["chiA100"] > 3.0,
   f"IT DOES NOT, and not remotely.  The aphelion-keyed constant anomaly {sedna['canonical']['dgA']:.1e} m/s^2 "
   f"leaves {sedna['canonical']['postA']:.2e} mas after the orbit fit: {sedna['canonical']['chiA100']:.3f} "
   f"sigma at 100 mas and {sedna['canonical']['chiA10']:.2f} sigma even at 10 mas (alt footing "
   f"{sedna['alt']['chiA100']:.3f} / {sedna['alt']['chiA10']:.2f}).  THE REASON IS STRUCTURAL, NOT "
   f"INSTRUMENTAL: 25 yr is {100*T_ARC/kepler_period(A_SED):.2f}% of Sedna's orbit, and a secular perihelion "
   f"advance is not defined on a hundredth of an orbit -- the four free elements absorb "
   f"{100*(1 - sedna['canonical']['postA']/(np.std(integrate_const(sedna['canonical']['dgA'], tt)[:NEP] - int0[:NEP])*RAD2MAS)):.0f}% "
   f"of the raw signal (a factor "
   f"{np.std(integrate_const(sedna['canonical']['dgA'], tt)[:NEP] - int0[:NEP])*RAD2MAS/sedna['canonical']['postA']:.0f}).  "
   f"So the PRECESSION channel is shut on the best inert object in the sky")

P(""); info("D3 -- the one channel that is NOT shut, reported with its killer attached")
P("  MI-B -- nu frozen at the orbit's minimum acceleration -- is exactly a rescaling of the effective GM")
P("  along that orbit.  By the B2a theorem it precesses NOTHING, so it is invisible to Part B entirely.  But")
P("  it is not invisible to an orbit fit that has an independent distance, because the same 4 elements cannot")
P("  simultaneously null the angular and the radial signature.")
for fn in A0:
    s = sedna[fn]
    P(f"  {fn:>10}: eps = {s['eps']:.3e} (Sedna) = {s['eps']/M_EARTH_OVER_M_SUN:.1f} M_earth of equivalent "
      f"interior mass;  post-fit {s['postB']:.2f} mas;  {s['chiB100']:.2f} sigma at 100 mas, "
      f"{s['chiB10']:.2f} sigma at 10 mas")
mg_at_sedna = float(log10_dg_routeA(GM_SUN/R_NOW**2, a0c)) - math.log10(GM_SUN/R_NOW**2)
P(f"  and the CONTRAST that makes it a fork test: modified gravity's eps at Sedna's PRESENT distance "
  f"({R_NOW/AU:.0f} AU) is 10^{mg_at_sedna:.0f}, against MI-B's {sedna['canonical']['eps']:.2e}.")
P(f"  A ratio of 10^{math.log10(sedna['canonical']['eps']) - mg_at_sedna:.0f}.  The two arms bracket the")
P(f"  measurement, so a Sedna effective-GM determination at the 1e-4 level lands INSIDE the bracket.")
ck("D3a  the MI-B effective-GM channel is currently detectable at 3 sigma",
   sedna["canonical"]["chiB100"] > 3.0,
   f"NOT AT PRESENT PRECISION -- {sedna['canonical']['chiB100']:.2f} sigma at 100 mas over 401 epochs -- but "
   f"it is the ONLY solar-system channel in this script that is within reach at all: {sedna['canonical']['chiB10']:.1f} "
   f"sigma (canonical) / {sedna['alt']['chiB10']:.1f} sigma (alt) at 10 mas LSST-class astrometry.  IT IS "
   f"REPORTED WITH ITS KILLER ATTACHED, and the killer is decisive on the positive side: eps = "
   f"{sedna['canonical']['eps']:.2e} of M_sun is {sedna['canonical']['eps']/M_EARTH_OVER_M_SUN:.0f} M_earth of "
   f"unmodelled interior mass, so a DETECTION would be attributed to Planet Nine, not to gravity.  This is "
   f"the repo's own known-bug pattern -- a residual degenerate with a nuisance parameter -- and it is flagged "
   f"here rather than discovered later.  ONLY THE NULL SIDE IS CLEAN: a Sedna eps < 1e-4 would exclude the "
   f"most generous MI reading on a real orbit, which nothing currently does")

P(""); info("D4 -- the arc-length obstruction: why this is 'centuries', not 'a bigger telescope'")
P(f"  {'object':<16}{'P [yr]':>11}{'25-yr arc / P':>16}")
for nm, aAU, e, qAU, QAU, LQ, Lq, dgA, eps, Pyr in lever:
    if aAU < 30: continue
    P(f"  {nm:<16}{Pyr:>11.1f}{T_ARC/YR/Pyr:>16.2e}")
P("")
P(f"  Sedna, MI-A precession channel, as a function of observed arc length:")
P(f"  {'arc [yr]':>10}{'% of orbit':>12}{'post-fit [mas]':>16}{'sigma @10mas':>14}")
arc_rows = []
for mult in (1, 2, 4, 8, 16, 32, 64):
    T = T_ARC*mult; t2, b2, D2 = build(T)
    i0 = integrate_const(0.0, t2)
    s2 = integrate_const(sedna["canonical"]["dgA"], t2) - i0
    r2, chi2 = postfit(s2, D2, 10.0)
    arc_rows.append((T/YR, float(np.std(r2[:NEP])*RAD2MAS), chi2))
    P(f"  {T/YR:>10.0f}{100*T/kepler_period(A_SED):>12.2f}{arc_rows[-1][1]:>16.3e}{chi2:>14.2f}")
reach = [t for t, rm, c in arc_rows if c > 3.0]
ck("D4a  an observing programme of realistic length (<= 200 yr) reaches the MI-A channel at 3 sigma",
   len(reach) > 0 and min(reach) <= 200.0,
   f"IT DOES NOT.  The MI-A post-fit residual reaches 3 sigma at 10 mas astrometry only at an arc of "
   f"~{(min(reach) if reach else float('inf')):.0f} yr = "
   f"{(100*min(reach)*YR/kepler_period(A_SED) if reach else 0):.1f}% of Sedna's orbit, against the ~25 yr of "
   f"precision astrometry this object has.  The residual grows as a high power of the arc because it is the "
   f"first term the 4-element fit cannot absorb, which is precisely why more telescope does not help and only "
   f"more decades do.  The scan is not perfectly monotone (the fit family's orientation relative to the "
   f"signal shifts as the arc covers more of the orbit); that is reported rather than smoothed")

P(""); info("D5 -- the summary shortfall table")
P(f"  {'route':<46}{'signal':>15}{'sensitivity':>14}{'shortfall':>14}")
mgS = float(log10_dg_routeA(gS, a0c)); bdS = dg_bound_from_wdot(9.53667594*AU, 0.05386179, 0.0047)
mgM = float(log10_dg_routeA(GM_SUN/(1.52371034*AU)**2, a0c))
bdM = dg_bound_from_wdot(1.52371034*AU, 0.09339410, 0.00037)
P(f"  {'MG tail, Saturn (Cassini ranging)':<46}{'1e%.0f' % mgS:>15}{bdS:>14.1e}"
  f"{'1e%.0f' % (math.log10(bdS)-mgS):>14}")
P(f"  {'MG tail, Mars (sharpest in astronomy)':<46}{'1e%.0f' % mgM:>15}{bdM:>14.1e}"
  f"{'1e%.0f' % (math.log10(bdM)-mgM):>14}")
P(f"  {'MI-A envelope, LPC optimum (outgassing)':<46}{pk_can:>15.1e}{ng5:>14.1e}{'%.0fx' % (ng5/pk_can):>14}")
P(f"  {'MI-A envelope, Sedna 25-yr arc (100 mas)':<46}{sedna['canonical']['postA']:>13.1e}mas{'100 mas':>14}"
  f"{'%.0fx' % (3.0/max(sedna['canonical']['chiA100'],1e-30)):>14}")
P(f"  {'MI-B envelope, Sedna 25-yr arc (100 mas)':<46}{sedna['canonical']['postB']:>13.1f}mas{'100 mas':>14}"
  f"{'%.1fx' % (3.0/sedna['canonical']['chiB100']):>14}")
P(f"  {'MG EFE quadrupole Q_2 -- OVER the bound, not under':<46}{Q2o['canonical'][0]:>15.1e}"
  f"{Q2_CEIL_2SIG:>14.1e}{'+%.0f sig' % Q2o['canonical'][2]:>14}")
short_tail = math.log10(bdS) - mgS
ck("D5a  the solar system is shut as a PRECESSION discriminant, on both arms at once",
   short_tail > 100.0 and sedna["canonical"]["chiA10"] < 1.0 and ng5/pk_can > 10.0,
   f"the modified-gravity eccentricity signature is real (B3a) and falls short of the sharpest measurement in "
   f"astronomy by 10^{short_tail:.0f}.  The most generous MI precession reading falls short on the best inert "
   f"object by {3.0/max(sedna['canonical']['chiA10'],1e-30):.0f}x even at LSST-class astrometry, and on the "
   f"theoretical optimum by {ng5/pk_can:.0f}x in outgassing alone.  This is a clean CLOSURE of the route, not "
   f"a marginal result -- and because it closes BOTH arms at once it does not decide the fork through this "
   f"channel.  The fork-relevant solar-system information is entirely in A5b (Q_2) and, prospectively, in "
   f"D3a (Sedna's effective GM)")


# ============================================================================================================
P(""); P("="*118); P("WHAT THIS CLOSES AND WHAT IT OPENS"); P("="*118)
P(f"""
 SHUT, CLEANLY, AND FOR BOTH ARMS.  The solar system cannot decide the modified-gravity / modified-inertia
 fork through orbit shape.  Under Route A's exponential kernel the anomalous acceleration inside 100 AU is
 below 1e-25 m/s^2 everywhere, so the eccentricity discriminant has no magnitude to work with: the largest
 modified-gravity precession rate at the most favourable eccentricity inside 100 AU is {max(inner):.1e} mas/yr
 against Mars's {MARS_PREC} mas/yr -- short by 10^{math.log10(MARS_PREC/max(inner)):.0f}.  The lever moves outward to where the
 anomaly is real -- it peaks at {pk_can:.1e} m/s^2 at {rpk_can:.0f} AU, and that is a hard ceiling on the whole
 effect -- but every object with an aphelion there is either a long-period comet whose outgassing is
 {ng5/pk_can:.0f}x the signal and which is seen once, or a detached TNO whose observed arc is a hundredth of an orbit
 and whose signal is therefore reabsorbed into its own orbital elements ({sedna['canonical']['postA']:.1e} mas post-fit on
 Sedna, {sedna['canonical']['chiA10']:.2f} sigma even at LSST-class astrometry).  The negative is quantified and it is not close.

 BUT THE SOLAR SYSTEM IS NOT SILENT, AND WHAT IT SAYS GOES AGAINST THIS REPOSITORY'S OPERATIVE ARM.  The live
 solar-system observable is the external-field quadrupole Q_2, and it is not a tail effect: it is set at the
 MOND radius r_M = {rM_can:.0f} AU where y ~ 1 and the exponential does nothing.  Route A's own kernel, pinned on the
 published anchors FOR THAT KERNEL, gives Q_2 = {Q2o['canonical'][0]:.2e} (canonical) / {Q2o['alt'][0]:.2e} (alt) s^-2 against the
 Park+2026 ceiling {Q2_CEIL_2SIG:.1e}: {Q2o['canonical'][1]:.1f}x / {Q2o['alt'][1]:.1f}x over.  The modified-INERTIA arm's committed value is
 {Q2_MI:.1e} s^-2, {Q2_MI/Q2_CEIL_2SIG:.0e} of the ceiling.  So this channel DOES separate the arms, and it favours modified
 inertia -- which STANDING.md closes as physics at 21 sigma on lensing.  The honest reading is that the
 framework has no arm passing everything: MG fails Cassini Q_2, MI fails lensing.  That is a real pincer, and
 it is not new; what is new is that it holds on Route A SPECIFICALLY, and that it must not be conflated with
 the isotropic tail liability, which really is discharged by 350 orders.

 ONE PROSPECTIVE TEST SURVIVES, AND IT IS NOT A PRECESSION TEST.  The most generous MI reading is a rescaling
 of the effective GM along the orbit -- eps = {sedna['canonical']['eps']:.2e} on Sedna against modified gravity's 10^{mg_at_sedna:.0f} at
 Sedna's present distance.  A ratio of 10^{math.log10(sedna['canonical']['eps'])-mg_at_sedna:.0f}, and by the B2a theorem it precesses nothing, so it has
 been invisible to every test of this kind.  Against angles plus parallax range on the 25-yr arc it is
 {sedna['canonical']['chiB100']:.2f} sigma at 100 mas and {sedna['canonical']['chiB10']:.1f} sigma at 10 mas.  Reported WITH ITS KILLER: eps of that size is
 {sedna['canonical']['eps']/M_EARTH_OVER_M_SUN:.0f} M_earth of unmodelled interior mass, so a DETECTION reads as Planet Nine, not as gravity.
 Only the NULL is clean, and the null already yields a number: scaling 0.57 sigma to a 3-sigma bar, the
 present arc constrains Sedna's effective-GM excess to eps < 1.1e-3, a factor 5.3 above the MI-B envelope.
 So the most generous MI reading is NOT yet excluded on a real orbit, and a 10 mas dataset would exclude it.
 That is the one actionable item this script produces, and it is a proposal, not a result.

 CAVEATS, IN BOTH DIRECTIONS, ALL LOAD-BEARING.
  * The Q_2 significance is set by the Milky Way mass model, not by the kernel.  Desmond+2024 quote 8.7 sigma
    fiducial and 1.9 sigma with bulge galaxies removed from the RAR.  A single g_ext = {G_EXT:.3e} m/s^2 is used
    here with no error on it, so +{Q2o['canonical'][2]:.0f} sigma is an UPPER reading of the tension.  Quote it as "several
    sigma, up to ~16", never as 16 alone.  The ROBUST statement is the ratio to the ceiling, {Q2o['canonical'][1]:.1f}x-{Q2o['alt'][1]:.1f}x.
  * The MI contrast 7.4e-34 s^-2 is committed on the OLD kernel nu = sqrt(1+1/y) and at the quasistatic-MI
    premise.  It has NOT been recomputed on Route A here.
  * MI-A and MI-B are deliberately extreme envelopes, not predictions of any MI theory.  They exist to make
    the negative robust, and the D3a number must never be quoted as "the framework predicts".
  * The Sedna astrometric precisions (100 mas, 10 mas) are ESTIMATES; no published Sedna orbit covariance is
    held in this repository.  Every sigma in D2/D3/D4 inherits that.  A systematic astrometric floor, which
    does not average down over epochs, would make them worse, not better.
  * Nothing here can prefer the framework over LambdaCDM.  At planetary accelerations GR predicts zero and so
    do healthy MOND-family theories; these numbers discriminate between the framework's own arms only.
""")
sys.exit(ck.done())
