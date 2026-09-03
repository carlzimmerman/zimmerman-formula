#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""g04v_adversarial_tail_margin_audit.py -- ADVERSARIAL AUDIT of g04's A1a/A2a isotropic-tail claim.

THE CLAIM UNDER ATTACK (g04_solar_system_eccentricity_discriminant.py, checks A1a + A2a):
  "Route A's exponential kernel discharges the isotropic solar-system tail liability absolutely, not
   marginally: the anomalous acceleration is below every per-planet ephemeris bound by 320 to 8900 orders
   of magnitude on both footings.  Smallest margin 10^320 (Saturn, alt).  The delta-g bound machinery is
   validated to <1% against the repo's own committed conversion (A1a, worst |log10 ratio| 0.0087)."

WHAT THIS SCRIPT DOES.  It re-derives the central numbers with an INDEPENDENT implementation (mpmath at 60
digits, no log-space float tricks, no reuse of g04's helpers) and then applies the one attack the lens
demands: g04's A2 table compares an r-DEPENDENT anomaly EVALUATED AT A SINGLE POINT (r = a) against a bound
that was DERIVED FOR A CONSTANT radial perturbation.  Those are not the same estimator.  Route A's dg varies
by tens to thousands of decades along a single planetary orbit and the orbit average is dominated by
APHELION, not by r = a.  The self-consistent comparison is: push Route A's actual dg(r) through the SAME
Gauss secular integral that produced the bound, and compare the resulting precession rate directly against
the published sigma(omega-dot).  V3 does exactly that.  V4 re-checks the "<1%" validation figure.  V5 asks
whether the SCOPE word "isotropic" is doing load-bearing work by pricing the arm's OTHER solar-system
anomaly (the EFE quadrupole) in the same delta-g currency at the same planet.

Sources for every measured number (no invented data):
  sigma(supplementary perihelion advance), mas/yr -- Fienga & Minazzoli 2024, Living Rev. Relativ. 27:1
      (arXiv:2303.01821) Table 10, tighter of Pitjeva & Pitjev 2013 (EPM) / Fienga+ 2011b (INPOP10a).
      FM24 sec 5 itself calls reading un-refit supplementary precessions as theory bounds "strongly
      discouraged"; carried as a caveat, not used to move any verdict.
  committed per-planet delta-g bounds -- prep_2026/planetary_doors/BOUNDS.md sec 1.2.
  Q_2 2-sigma ceiling 5.2e-27 s^-2 -- Park, Hees, Famaey, Desmond, Durakovic 2026 (arXiv:2602.17884).
  planetary elements -- Standish & Williams, JPL approximate positions, J2000.
"""
import sys, math
import numpy as np
import mpmath as mp
from hunt_lib import Check, P, info, A0

mp.mp.dps = 60
ck = Check()

GM   = mp.mpf("1.32712440018e20")
AU   = mp.mpf("1.495978707e11")
YR   = mp.mpf("3.155760000e7")
RAD2MAS = mp.mpf(180)/mp.pi*3600*1000

# name, a[AU], e, sigma(wdot)[mas/yr], BOUNDS.md committed delta-g [m/s^2]
PLANETS = [
    ("Mercury", "0.38709927", "0.20563593", "0.006",   4.6e-14),
    ("Venus",   "0.72333566", "0.00677672", "0.015",   8.0e-14),
    ("Earth",   "1.00000261", "0.01671123", "0.0019",  8.7e-15),
    ("Mars",    "1.52371034", "0.09339410", "0.00037", 1.4e-15),
    ("Jupiter", "5.20288700", "0.04838624", "0.28",    5.6e-13),
    ("Saturn",  "9.53667594", "0.05386179", "0.0047",  7.0e-15),
]

def dg_routeA(r, a0):
    """(nu-1)*g_N with nu = 1/(1-exp(-sqrt(y))), exact in mpmath.  nu-1 = 1/(exp(u)-1), u = sqrt(g_N/a0)."""
    gN = GM/r**2
    u  = mp.sqrt(gN/a0)
    return gN/mp.expm1(u)

def period_yr(a):
    return 2*mp.pi*mp.sqrt(a**3/GM)/YR

def dg_bound(a, e, sig_mas_yr):
    """Invert |Delta omega|_per_orbit = 2 pi dg a^2 sqrt(1-e^2)/GM  (constant sunward dg).
    Independently derived here: for delta-Phi = dg*r the time-average is dg*a(1+e^2/2); Lagrange's
    d(omega)/dt = sqrt(1-e^2)/(n a^2 e) * d<R>/de with R = -delta-Phi gives -dg sqrt(1-e^2)/(n a);
    times 2 pi/n gives -2 pi dg a^2 sqrt(1-e^2)/GM.  (Same closed form g04's B1b validates numerically.)"""
    return (mp.mpf(sig_mas_yr)/RAD2MAS)*period_yr(a)*GM/(2*mp.pi*a**2*mp.sqrt(1-e**2))

def dperi_per_orbit(a, e, a0, n=40001):
    """Delta(omega) per orbit for the ACTUAL r-dependent Route A dg, via the same Gauss integral g04 Part B
    uses:  Delta(omega) = (1/(GM e)) Int_0^{2pi} dg(r(f)) r(f)^2 cos f df,  r = a(1-e^2)/(1+e cos f).
    Done in mpmath so nothing underflows and no log-space bookkeeping can hide a factor.  Symmetric about
    f = pi, so integrate 0..pi and double.  The integrand is a sharp peak at aphelion of angular width
    ~sqrt(2(1-e)/(e*sqrt(y_apo))); the grid below resolves it by >1e3 points for every planet here."""
    p = a*(1-e**2)
    f = [mp.pi*mp.mpf(i)/(n-1) for i in range(n)]
    vals = []
    for ff in f:
        r = p/(1+e*mp.cos(ff))
        vals.append(dg_routeA(r, a0)*r**2*mp.cos(ff))
    # Simpson on 0..pi (n odd), doubled by symmetry
    h = mp.pi/(n-1)
    s = vals[0] + vals[-1] + 4*sum(vals[1:-1:2]) + 2*sum(vals[2:-1:2])
    return 2*(h/3)*s/(GM*e)

P("="*118)
P("g04v -- ADVERSARIAL AUDIT of the g04 isotropic-tail margin claim (A1a / A2a)")
P("="*118)

# ---------------------------------------------------------------------------------------------------- V1
P(""); info("V1 -- independent re-derivation of g04's A1 delta-g bound table (mpmath, own closed form)")
P(f"  {'planet':<10}{'a [AU]':>10}{'P [yr]':>10}{'dg bound here':>16}{'g04 / BOUNDS.md':>18}{'ratio':>9}")
v1 = []
for nm, aS, eS, sw, dgrepo in PLANETS:
    a = mp.mpf(aS)*AU; e = mp.mpf(eS)
    b = dg_bound(a, e, sw)
    v1.append(float(b)/dgrepo)
    P(f"  {nm:<10}{float(a/AU):>10.5f}{float(period_yr(a)):>10.4f}{float(b):>16.4e}{dgrepo:>18.1e}"
      f"{float(b)/dgrepo:>9.4f}")
worst_v1 = max(abs(math.log10(x)) for x in v1)
ck("V1a  the bound machinery reproduces independently -- g04's A1a is arithmetically sound",
   worst_v1 < 0.03,
   f"worst |log10 ratio| vs the committed BOUNDS.md numbers is {worst_v1:.4f}, from a completely separate "
   f"mpmath implementation with the closed form re-derived from Lagrange's equations rather than copied.  "
   f"g04's A1a number 0.0087 is CONFIRMED")

P(""); info("V2 -- but the '<1%' description of that validation is WRONG, and it is a log/percent conflation")
frac = [abs(x-1.0) for x in v1]
P(f"  worst |log10 ratio| = {worst_v1:.4f}   ->   as a FRACTIONAL error that is 10^0.0087 - 1 = "
  f"{100*(10**worst_v1 - 1):.2f}%")
P(f"  worst actual fractional deviation over the six planets = {100*max(frac):.2f}%  (Mercury, "
  f"{float(v1[0]):.4f} of BOUNDS.md)")
ck("V2a  the claim's stated validation precision '<1%' is correct",
   max(frac) < 0.01,
   f"IT IS NOT.  The worst per-planet deviation is {100*max(frac):.2f}% (Mercury), not <1%.  The '<1%' comes "
   f"from reading the log10 residual 0.0087 as if it were a fraction; 10^0.0087 - 1 = "
   f"{100*(10**worst_v1-1):.2f}%.  g04's own A1a text says 'all within 3%', which is right -- the ERROR IS IN "
   f"THE CLAIM SUMMARY, not in the script.  Immaterial to the verdict at a 10^320 margin, flagged because it "
   f"is exactly the kind of number that gets quoted downstream")

# ---------------------------------------------------------------------------------------------------- V3
P(""); info("V3 -- THE ESTIMATOR ATTACK: g04's A2 margin uses dg AT r = a against a CONSTANT-dg bound")
P("  Route A's dg(r) = g_N/(exp(sqrt(g_N/a0)) - 1) falls off super-exponentially inward, so along ONE orbit")
P("  it spans many decades and its orbit average is set at APHELION.  Evaluating it at r = a therefore")
P("  UNDERSTATES the observable.  The self-consistent comparison is to push the true dg(r) through the same")
P("  Gauss integral that defined the bound, and compare the precession RATE to sigma(omega-dot) directly.")
P("")
P(f"  {'planet':<10}{'foot':>10}{'log10 dg(a)':>13}{'log10 dg(Q)':>13}{'A2 margin':>11}"
  f"{'log10|rate| mas/yr':>20}{'sigma mas/yr':>14}{'TRUE margin':>13}{'A2 optimism':>13}")
opt_bias = []; true_margins = []; a2_margins = []
for fn, a0f in A0.items():
    a0 = mp.mpf(repr(a0f))
    for nm, aS, eS, sw, dgrepo in PLANETS:
        a = mp.mpf(aS)*AU; e = mp.mpf(eS); Q = a*(1+e)
        Lg_a = float(mp.log10(dg_routeA(a, a0)))
        Lg_Q = float(mp.log10(dg_routeA(Q, a0)))
        m_a2 = float(mp.log10(dg_bound(a, e, sw))) - Lg_a
        dw   = dperi_per_orbit(a, e, a0)
        Lrate = float(mp.log10(abs(dw)*RAD2MAS/period_yr(a)))
        m_true = math.log10(float(sw)) - Lrate
        opt_bias.append(m_a2 - m_true); true_margins.append(m_true); a2_margins.append(m_a2)
        P(f"  {nm:<10}{fn:>10}{Lg_a:>13.1f}{Lg_Q:>13.1f}{m_a2:>11.1f}{Lrate:>20.1f}{float(sw):>14.5f}"
          f"{m_true:>13.1f}{m_a2-m_true:>13.1f}")
P("    'A2 margin'   = log10(bound) - log10(dg at r=a)                       <- what g04's A2a reports")
P("    'TRUE margin' = log10(sigma_wdot) - log10(|orbit-averaged rate|)      <- apples to apples")
P("    'A2 optimism' = how many decades the point estimate is too generous by")
ck("V3a  g04's A2 margins are the right estimator -- the point value at r = a is not systematically low",
   max(opt_bias) < 1.0,
   f"THEY ARE NOT the right estimator.  Comparing dg at r = a against a bound built for a CONSTANT dg is a "
   f"mismatch, and it runs in the ANTI-CONSERVATIVE direction on every planet and both footings: the "
   f"optimism ranges from {min(opt_bias):.0f} to {max(opt_bias):.0f} decades, worst on Mercury (highest e "
   f"times highest sqrt(y), so the aphelion/mean contrast is largest).  Every A2a margin is overstated")
ck("V3b  the claim's quoted margin range '10^320 to 10^8900' is the correct range",
   abs(min(a2_margins) - min(true_margins)) < 1.0 and abs(max(a2_margins) - max(true_margins)) < 1.0,
   f"IT IS NOT.  Done self-consistently the range is 10^{min(true_margins):.0f} to "
   f"10^{max(true_margins):.0f}, against the claimed 10^{min(a2_margins):.0f} to 10^{max(a2_margins):.0f}.  "
   f"The smallest margin (Saturn, alt footing) is 10^{min(true_margins):.0f}, not 10^320.  THE NUMBERS IN "
   f"THE CLAIM ARE WRONG; the CONCLUSION they support is not, and the next check says so")
ck("V3c  the qualitative conclusion nevertheless survives the correction: absolute, not marginal, discharge",
   min(true_margins) > 100.0,
   f"the smallest self-consistent margin over six planets and both footings is still "
   f"10^{min(true_margins):.0f}.  A ~{max(opt_bias):.0f}-decade correction to a ~{min(true_margins):.0f}-decade "
   f"margin changes nothing about whether the isotropic tail is discharged.  The claim's ADJECTIVE "
   f"('absolutely, not marginally') is right; its DIGITS are not")

# ---------------------------------------------------------------------------------------------------- V4
P(""); info("V4 -- sanity: does the mutation control still fire on the retired kernel, in MY implementation?")
P("  nu = sqrt(1+1/y) has nu-1 -> 1/(2y), i.e. a CONSTANT a_0/2 sunward.  Constant is exactly the estimator")
P("  the bound was built for, so here the point comparison IS self-consistent and no correction applies.")
P(f"  {'planet':<10}{'foot':>10}{'a0/2':>12}{'bound':>11}{'excluded by':>13}{'KERNEL_PLANETS':>16}")
BANKED = {"Mercury": 1018, "Earth": 5380, "Mars": 33436, "Saturn": 6687}
mut = []; rep_err = {}
for fn, a0f in A0.items():
    for nm, aS, eS, sw, dgrepo in PLANETS:
        a = mp.mpf(aS)*AU; e = mp.mpf(eS)
        gN = GM/a**2; y = gN/mp.mpf(repr(a0f))
        dg = (mp.sqrt(1+1/y)-1)*gN
        x = float(dg/dg_bound(a, e, sw)); mut.append(x)
        ref = BANKED.get(nm) if fn == "canonical" else None
        if ref: rep_err[nm] = abs(x/ref - 1.0)
        P(f"  {nm:<10}{fn:>10}{float(dg):>12.3e}{float(dg_bound(a,e,sw)):>11.2e}{x:>13.0f}"
          f"{(str(ref) if ref else '--'):>16}")
ck("V4a  MUTATION CONTROL reproduces independently: the retired kernel is excluded by the banked factors",
   max(mut) > 1e3 and rep_err["Mars"] < 0.05 and rep_err["Saturn"] < 0.05,
   f"max exclusion {max(mut):.0f}x; Mars reproduces the banked 33436x to {100*rep_err['Mars']:.1f}% and "
   f"Saturn its 6687x to {100*rep_err['Saturn']:.1f}%, from an independent implementation.  So the machinery "
   f"CAN fail and g04's A3a is confirmed.  Note this control does NOT exercise the r-dependence that V3a "
   f"exposes -- a constant perturbation is precisely the case where the point estimate is exact, which is "
   f"why the control passed while the estimator mismatch went unflagged")

# ---------------------------------------------------------------------------------------------------- V5
P(""); info("V5 -- SCOPE: is the word 'isotropic' load-bearing?  Price the OTHER anomaly in the same currency")
P("  g04's own A5b FAILS: the EFE quadrupole is Q_2 = 3.0e-26 / 3.3e-26 s^-2 against Park+2026's 5.2e-27")
P("  2-sigma ceiling.  Q_2 has units s^-2 and produces a tidal acceleration of order Q_2 * r at radius r.")
P("  Evaluated at Saturn that is a DIRECT competitor to the same per-planet delta-g bound.")
Q2 = {"canonical": 3.002e-26, "alt": 3.269e-26}      # g04 A5, on the Desmond+2024 eq-(12) published anchors
r_sat = mp.mpf("9.53667594")*AU
b_sat = dg_bound(r_sat, mp.mpf("0.05386179"), "0.0047")
P(f"  {'footing':>10}{'Q2 [s^-2]':>13}{'Q2*r_Saturn':>14}{'Saturn dg bound':>17}{'ratio':>9}")
q2_over = []
for fn, q in Q2.items():
    dgq = mp.mpf(repr(q))*r_sat
    q2_over.append(float(dgq/b_sat))
    P(f"  {fn:>10}{q:>13.3e}{float(dgq):>14.3e}{float(b_sat):>17.3e}{float(dgq/b_sat):>9.2f}")
ck("V5a  the framework's modified-gravity arm predicts a Saturn anomaly under the ephemeris bound",
   max(q2_over) < 1.0,
   f"IT DOES NOT.  The EFE quadrupole alone gives Q_2*r = {float(mp.mpf(repr(Q2['canonical']))*r_sat):.2e} "
   f"m/s^2 at Saturn, {min(q2_over):.1f}x-{max(q2_over):.1f}x the same {float(b_sat):.1e} m/s^2 bound that "
   f"the tail clears by 10^{min(true_margins):.0f}.  So 'the anomalous acceleration is below every "
   f"per-planet ephemeris bound' is TRUE ONLY of the isotropic piece and FALSE of the arm's total predicted "
   f"anomaly.  The word 'isotropic' in the claim is not decoration -- it is the entire content, and g04 "
   f"itself says so ('the two must never be conflated').  This check exists so that the claim cannot be "
   f"quoted with that word dropped")

P(""); P("="*118)
P("VERDICT OF THE AUDIT")
P("="*118)
P(f"""
 CONFIRMED.  The kernel algebra, the bound machinery, and the mutation control all reproduce from an
 independent 60-digit implementation (V1a, V4a).  Route A's isotropic tail really is discharged absolutely:
 the smallest self-consistent margin over six planets and both footings is 10^{min(true_margins):.0f} (V3c).  No
 measurement now or conceivable touches it.

 REFUTED AS STATED, IN THREE PLACES, NONE OF WHICH FLIPS THE CONCLUSION.
  1. The margin RANGE is wrong.  g04's A2 (and the claim) compares dg evaluated at r = a against a bound
     derived for a CONSTANT radial dg.  Route A's dg is dominated by aphelion, so the point estimate is
     anti-conservative by {min(opt_bias):.0f}-{max(opt_bias):.0f} decades.  Self-consistently the range is
     10^{min(true_margins):.0f} to 10^{max(true_margins):.0f}, not 10^320 to 10^8900 (V3a, V3b).
  2. '<1%' for the A1a validation is a log/percent conflation; the worst deviation is {100*max(frac):.2f}% (V2a).
     g04's own text says 'within 3%' and is correct.
  3. 'below every per-planet ephemeris bound' is true only with the word 'isotropic' attached.  The same
     arm's EFE quadrupole is {min(q2_over):.1f}x-{max(q2_over):.1f}x OVER that very bound at Saturn (V5a).

 WHAT A REFEREE WOULD DO WITH THIS: accept the physics, strike the digits, and insist on the scope word.
""")
sys.exit(ck.done())
