#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
g04_verify_cassini_q2_adversarial.py -- ADVERSARIAL RE-VERIFICATION of g04's A5b Cassini Q_2 claim.
====================================================================================================
THE CLAIM UNDER ATTACK (g04_solar_system_eccentricity_discriminant.py, check A5b):
  "The modified-GRAVITY arm fails the Cassini external-field quadrupole on Route A's own kernel, on
   both footings.  The exponential tail does not help because Q_2 is set at the MOND-transition
   radius (thousands of AU) where y ~ 1, not at Saturn."

This script does NOT re-run g04.  It attacks the claim four independent ways, three of which g04
does not do at all.  Checks are written so they FAIL if the claim is wrong.

 V1  INDEPENDENT QUADRATURE.  g04 evaluates Desmond, Hees & Famaey 2024 (arXiv:2401.04796) eq (12)
     with scipy.integrate.dblquad.  Here the same integral is done with tensor-product Gauss-Legendre
     on geometric panels -- a different algorithm, different error mode -- and pinned on the SAME
     published anchors, which were read VERBATIM from the paper's Fig. 1 caption:
       "q(1) = 0.094, q(1.5) = 0.159 and q(2) = 0.221"   for   nu_RAR(y) = [1 - exp(-y^1/2)]^-1  (their eq 6)
     Their eq (10):  Q_2 = -(3 a_0^{3/2} / (2 sqrt(GM))) q(etilde);  their eq (11):  etilde = g_ext/a_0.

 V2  WHERE THE INTEGRAL ACTUALLY LIVES.  g04 ASSERTS "Q_2 is set at r_M ~ 8000 AU", it does not show
     it.  In eq (12) the radial variable enters as v^2 = g_N,Sun/a_0 = (r_M/r)^2, so r = r_M/v and the
     panelled quadrature yields the accumulation of q with radius directly.  This is the load-bearing
     physics of the whole claim -- if q accumulated near Saturn, Route A's exp(-sqrt y) would kill it.
     Desmond+2024's own Fig. 1 caption states the same conclusion independently:
       "The plot shows that the value of q(etilde) mainly probes the behaviour of the IF around e_N."

 V3  HOW MUCH WOULD HAVE TO MOVE.  The stated weakest link is a single g_ext with no error bar.  So:
     solve for the g_ext, and separately the a_0, at which Route A would CLEAR the ceiling.

 V4  A CLEANER, MODEL-INDEPENDENT RESTATEMENT, cross-validated against a published number g04 never
     used.  Park et al. 2026 (arXiv:2602.17884) abstract: "the Q2 constraint imposes an upper bound of
     only 2% (at 95% confidence) on the MOND boost to the galactic radial acceleration (i.e., the
     ratio of the observed over baryonic Newtonian acceleration) at the position of the Sun".  That
     boost is nu(e_N), a pure kernel quantity with no quadrupole machinery in it.  Reconstructing
     Park's 2% from the Q_2 ceiling through THIS script's machinery is an end-to-end validation of the
     transcription, the etilde<->e_N inversion, the prefactor and the a_0 scaling all at once.

MUTATION CONTROL (V1c): the RETIRED kernel nu = sqrt(1+1/y) must give a DIFFERENT q that misses the
published RAR anchors badly -- otherwise the anchors would not be pinning the kernel at all and the
"published pin on Route A's own kernel" language would be empty.

LITERATURE, ALL READ FROM THE PRIMARY SOURCE, NOT FROM THIS REPOSITORY:
  Desmond, Hees & Famaey 2024, MNRAS, arXiv:2401.04796, "On the tension between the Radial
      Acceleration Relation and Solar System quadrupole in modified gravity MOND" -- eq (6), (10),
      (11), (12); Fig. 1 caption; eq (2) quotes Hees et al. 2014 as Q_2 = (3 +- 3)e-27 s^-2;
      abstract quotes 8.7 sigma fiducial, reduced "to 1.9 sigma by removing galaxies with bulges".
  Park, Hees, Famaey, Desmond & Durakovic 2026, arXiv:2602.17884, "Improved constraints on modified
      Newtonian gravity from Cassini radio tracking data" -- Q_2 = (1.6 +- 1.8)e-27 s^-2 (1 sigma,
      DE440); tensions "at the 3-15 sigma level depending on the detailed mass modeling or the subset
      of galaxies considered"; the 2%-at-95%-confidence boost bound used in V4; and the explicit
      statement that Jupiter contributes 0.05% to the MOND Q_2, validating the Sun-only calculation.
  Milgrom 2009, MNRAS 399, 474 -- the origin of the Q_2 = -(3 a_0^{3/2}/2 sqrt(GM)) q formula.

WHAT THIS SCRIPT DOES NOT DO.  It does not verify the modified-INERTIA contrast value 7.4e-34 s^-2
(cassini_mi_evasion_2026/), which is one model on the retired kernel.  It only records that the
CLASS-level direction is the published authors' own reading: Desmond+2024 sec 5 state that "a Solar
System quadrupole is not generically predicted by modified inertia ..., potentially allowing the
Cassini constraint to be completely circumvented", and their sec 2 that in MI formulations the EFE
"may be very different ... or effectively absent".  Direction supported; magnitude not verified here.
"""
import math, sys
import numpy as np
from scipy.optimize import brentq
from numpy.polynomial.legendre import leggauss
from hunt_lib import Check, P, info, A0

ck = Check()
np.seterr(all="ignore")

GM_SUN = 1.32712440018e20
AU     = 1.495978707e11
G_EXT  = 2.146e-10          # V^2/R0 with V = 233 km/s, R0 = 8.2 kpc (as in g04 and the repo baseline)

# Park+2026, arXiv:2602.17884 (1 sigma, DE440); 2-sigma ceiling = 1.6 + 2*1.8
Q2_CEN, Q2_SIG = 1.6e-27, 1.8e-27
Q2_CEIL_2SIG   = Q2_CEN + 2.0*Q2_SIG
PARK_BOOST_95  = 0.02       # Park+2026 abstract: <2% boost at the Sun, 95% confidence

def nu_routeA(y):  return 1.0/(1.0 - np.exp(-np.sqrt(y)))          # Desmond+2024 eq (6) == Route A
def nu_retired(y): return np.sqrt(1.0 + 1.0/y)                     # mutation-control kernel

def q_gl(etilde, nufun, nx=200, vmax=200.0, npan=80, want_profile=False):
    """Desmond+2024 eq (12) by tensor-product Gauss-Legendre on geometric panels.
       q = (3/2) Int_0^inf dv Int_-1^1 dxi (nu-1)[eN(3xi-5xi^3) + v^2(1-3xi^2)], nu at sqrt(eN^2+v^4+2 eN v^2 xi).
       v^2 is the Sun's NEWTONIAN field in units of a_0, so v = r_M/r and r = r_M/v."""
    eN = brentq(lambda x: x*nufun(x) - etilde, 1e-12, 1e6)          # eq (11) + algebraic MOND relation
    xg, xw = leggauss(nx); vg, vw = leggauss(12)
    knee = max(4.0, 2.0*math.sqrt(etilde))
    edges = np.concatenate([np.linspace(0.0, knee, npan//2 + 1)[:-1],
                            np.geomspace(knee, vmax, npan//2 + 1)])
    tot = 0.0; prof = []
    for i in range(len(edges) - 1):
        a, b = edges[i], edges[i+1]
        vv = 0.5*(b-a)*vg + 0.5*(a+b); ww = 0.5*(b-a)*vw
        V, X = np.meshgrid(vv, xg, indexing="ij")
        D = eN*eN + V**4 + 2.0*eN*V*V*X
        f = (nufun(np.sqrt(D)) - 1.0)*(eN*(3*X - 5*X**3) + V*V*(1.0 - 3.0*X*X))
        seg = float(np.sum(ww[:, None]*xw[None, :]*f))
        tot += seg; prof.append((a, b, 1.5*seg))
    return (1.5*tot, eN, prof) if want_profile else (1.5*tot, eN)

def Q2_of(a0, q): return abs(3.0*a0**1.5/(2.0*math.sqrt(GM_SUN))*q)   # Desmond+2024 eq (10)

P("="*118)
P("g04 ADVERSARIAL RE-VERIFICATION -- the Cassini external-field quadrupole Q_2 on Route A's kernel")
P("="*118)

# ------------------------------------------------------------------------------------------ V1
P(""); info("V1 -- eq (12) by an INDEPENDENT quadrature, pinned on the paper's own Fig. 1 anchors")
P(f"  {'etilde':>8}{'published q':>13}{'q (Gauss-Legendre)':>21}{'rel err':>10}")
errs = []
for et, qp in ((1.0, 0.094), (1.5, 0.159), (2.0, 0.221)):
    q, _ = q_gl(et, nu_routeA); errs.append(abs(abs(q)/qp - 1.0))
    P(f"  {et:>8.1f}{qp:>13.3f}{abs(q):>21.5f}{abs(q)/qp - 1.0:>10.3%}")
ck("V1a  a DIFFERENT quadrature reproduces Desmond+2024's published q anchors for nu_RAR",
   max(errs) < 0.01,
   f"worst relative error {100*max(errs):.2f}% against q(1)=0.094, q(1.5)=0.159, q(2)=0.221, read verbatim "
   f"from the Fig. 1 caption of arXiv:2401.04796.  g04 used scipy dblquad; this uses tensor Gauss-Legendre on "
   f"geometric panels.  Agreement to 0.8% (and the 0.8% is the paper's own 2-significant-figure rounding at "
   f"etilde=1, since the etilde=2 anchor matches to 1e-5) rules out a quadrature artefact in g04")

P(""); P(f"  {'footing':>10}{'a_0':>11}{'etilde':>9}{'e_N':>9}{'|q|':>9}{'Q_2 [s^-2]':>13}"
        f"{'/ceiling':>10}{'sigma':>8}")
res = {}
for fn, a0 in A0.items():
    et = G_EXT/a0; q, eN = q_gl(et, nu_routeA); Q2 = Q2_of(a0, q)
    res[fn] = dict(a0=a0, et=et, eN=eN, q=abs(q), Q2=Q2, ratio=Q2/Q2_CEIL_2SIG,
                   sig=(Q2 - Q2_CEN)/Q2_SIG, boost=float(nu_routeA(eN)) - 1.0)
    P(f"  {fn:>10}{a0:>11.3e}{et:>9.4f}{eN:>9.4f}{abs(q):>9.5f}{Q2:>13.4e}"
      f"{Q2/Q2_CEIL_2SIG:>10.3f}{(Q2 - Q2_CEN)/Q2_SIG:>8.2f}")
P(f"  Park+2026: Q_2 = ({Q2_CEN:.1e} +- {Q2_SIG:.1e}) s^-2 (1 sigma, DE440); 2-sigma ceiling {Q2_CEIL_2SIG:.1e}.")
ck("V1b  g04's central numbers survive: Q_2 = 3.00e-26 / 3.27e-26 s^-2, both footings over the ceiling",
   abs(res["canonical"]["Q2"]/3.00e-26 - 1.0) < 0.02 and abs(res["alt"]["Q2"]/3.27e-26 - 1.0) < 0.02
   and min(v["ratio"] for v in res.values()) > 1.0,
   f"reproduced to {100*abs(res['canonical']['Q2']/3.00e-26 - 1.0):.2f}% (canonical) and "
   f"{100*abs(res['alt']['Q2']/3.27e-26 - 1.0):.2f}% (alt).  BOTH FOOTINGS GENUINELY ENTER AND THEY ARE NOT "
   f"DECORATIVE: they give different etilde ({res['canonical']['et']:.3f} vs {res['alt']['et']:.3f}), different "
   f"e_N ({res['canonical']['eN']:.3f} vs {res['alt']['eN']:.3f}), different q "
   f"({res['canonical']['q']:.4f} vs {res['alt']['q']:.4f}) and a different a_0^{{3/2}} prefactor -- and the two "
   f"effects PARTIALLY CANCEL (the smaller a_0 raises etilde hence q while lowering the prefactor), which is "
   f"why the two footings land within 9% of each other rather than 32% apart.  Both are over the ceiling")

P(""); info("V1c -- MUTATION CONTROL: the retired kernel must MISS the published RAR anchors")
mut = []
for et, qp in ((1.0, 0.094), (1.5, 0.159), (2.0, 0.221)):
    q, _ = q_gl(et, nu_retired); mut.append(abs(q)/qp)
    P(f"  etilde={et:.1f}: retired nu=sqrt(1+1/y) gives |q|={abs(q):.4f} against the RAR-anchored {qp:.3f} "
      f"-- factor {abs(q)/qp:.2f}")
ck("V1d  MUTATION CONTROL fires: a different kernel gives different q, so the anchors really pin the kernel",
   max(abs(math.log10(m)) for m in mut) > 0.05,
   f"the retired nu=sqrt(1+1/y) misses the published anchors by factors {mut[0]:.2f}/{mut[1]:.2f}/{mut[2]:.2f}.  "
   f"If it had matched, V1a would have been pinning nothing and 'the published anchors are for Route A's own "
   f"kernel' would have been an empty sentence.  It is not empty: q is kernel-discriminating at this level")

# ------------------------------------------------------------------------------------------ V2
P(""); info("V2 -- WHERE the q integral accumulates: the load-bearing physics g04 asserts but never shows")
P("  In eq (12), v^2 = g_N,Sun/a_0 = (r_M/r)^2, so each quadrature panel in v is a shell in radius r = r_M/v.")
P("  If q were built up near Saturn (r ~ 10 AU, v ~ 800) Route A's exp(-sqrt y) WOULD suppress it and g04's")
P("  claim would collapse.  Accumulating panel by panel, from large r inward (canonical footing):")
a0c = A0["canonical"]; rM = math.sqrt(GM_SUN/a0c)/AU
r_ext = math.sqrt(GM_SUN/G_EXT)/AU
qtot, eNc, prof = q_gl(G_EXT/a0c, nu_routeA, want_profile=True)
P(f"  r_M = sqrt(GM/a_0) = {rM:.0f} AU;  g_N,Sun = g_ext at r_ext = {r_ext:.0f} AU;  e_N = {eNc:.3f}")
P(f"  {'quantile of q':>16}{'v':>10}{'r [AU]':>12}")
for frac in (0.10, 0.25, 0.50, 0.75, 0.90, 0.99):
    c = 0.0
    for a, b, seg in prof:
        c += seg
        if abs(c/qtot) >= frac:
            P(f"  {100*frac:>15.0f}%{b:>10.3f}{rM/b:>12.0f}"); break
P(f"  {'fraction of q from INSIDE r':>34}")
inside = {}
for rcut in (10.0, 100.0, 1000.0, 3000.0, 5000.0, 8000.0):
    vcut = rM/rcut
    s = sum(seg for a, b, seg in prof if a >= vcut)
    inside[rcut] = abs(s/qtot)
    P(f"  r < {rcut:>8.0f} AU (v > {vcut:>9.3f}):  {abs(s/qtot):>12.4e}")
ck("V2a  q is built at the MOND-transition radius, NOT at Saturn -- the exponential tail cannot touch it",
   inside[100.0] < 1e-6 and inside[1000.0] < 1e-2 and inside[5000.0] > 0.3,
   f"the fraction of q coming from inside Saturn's neighbourhood is {inside[10.0]:.1e}, from inside 100 AU "
   f"{inside[100.0]:.1e}, and from inside 1000 AU only {inside[1000.0]:.1e}.  Half of q comes from OUTSIDE "
   f"~4300 AU and 99% from outside ~1500 AU.  So g04's A5b sentence is right in substance.  ONE CORRECTION TO "
   f"ITS WORDING: the weighting is centred nearer r_ext = {r_ext:.0f} AU (where the Sun's field equals the "
   f"galactic one, i.e. y ~ e_N = {eNc:.2f}) than at r_M = {rM:.0f} AU (where y = 1), so 'set at r_M ~ 8000 AU' "
   f"overstates the radius by ~2x.  The conclusion is unaffected -- both radii are thousands of AU -- and "
   f"Desmond+2024's Fig. 1 caption says the same thing independently: q 'mainly probes the behaviour of the "
   f"IF around e_N'")

# ------------------------------------------------------------------------------------------ V3
P(""); info("V3 -- the stated weakest link: how far would g_ext (or a_0) have to move to clear the ceiling?")
for fn, a0 in A0.items():
    g_ok = brentq(lambda g: Q2_of(a0, q_gl(g/a0, nu_routeA)[0]) - Q2_CEIL_2SIG, 1e-12, G_EXT, xtol=1e-14)
    P(f"  {fn:>10}: Route A clears {Q2_CEIL_2SIG:.1e} only if g_ext < {g_ok:.3e} m/s^2 = "
      f"{100*g_ok/G_EXT:.1f}% of V^2/R0, i.e. V_circ < {233*math.sqrt(g_ok/G_EXT):.0f} km/s at R0 = 8.2 kpc")
g_ok_can = brentq(lambda g: Q2_of(a0c, q_gl(g/a0c, nu_routeA)[0]) - Q2_CEIL_2SIG, 1e-12, G_EXT, xtol=1e-14)
a0_ok = brentq(lambda la: Q2_of(10**la, q_gl(G_EXT/10**la, nu_routeA)[0]) - Q2_CEIL_2SIG, -13.0, -10.3, xtol=1e-8)
P(f"  and at fixed g_ext, Route A clears the ceiling only if a_0 < {10**a0_ok:.3e} m/s^2 -- a factor "
  f"{a0c/10**a0_ok:.1f} below the canonical footing and {A0['alt']/10**a0_ok:.1f} below the alt one")
ck("V3a  a plausible error in the Milky Way external field could rescue Route A",
   g_ok_can/G_EXT > 0.75,
   f"IT COULD NOT.  g_ext would have to be {100*g_ok_can/G_EXT:.0f}% of V^2/R0 -- a Milky Way circular speed of "
   f"{233*math.sqrt(g_ok_can/G_EXT):.0f} km/s instead of 233 -- to bring Q_2 under the ceiling.  So the "
   f"stated weakest link (a single g_ext with no error bar) sets the SIGMA VALUE but cannot flip the SIGN of "
   f"the verdict: the 5.8x-6.3x ratio to the ceiling is robust to any defensible Milky Way model, and a_0 "
   f"itself is not a free knob here -- it is fixed by the framework's own two footings")

# ------------------------------------------------------------------------------------------ V4
P(""); info("V4 -- END-TO-END validation against a PUBLISHED number g04 never used: Park's 2% boost bound")
P("  Park+2026 abstract: the Q_2 constraint 'imposes an upper bound of only 2% (at 95% confidence) on the")
P("  MOND boost to the galactic radial acceleration ... at the position of the Sun'.  That boost is nu(e_N):")
P("  a pure kernel quantity with no quadrupole machinery in it.  Push the Q_2 ceiling back through THIS")
P("  script's chain and see whether 2% comes out.  If the transcription, the etilde<->e_N inversion, the")
P("  eq-(10) prefactor or the a_0 scaling were wrong, this reconstruction would miss.")
a0_at_ceil = 10**a0_ok
q_c, eN_c = q_gl(G_EXT/a0_at_ceil, nu_routeA)
boost_at_ceil = float(nu_routeA(eN_c)) - 1.0
P(f"  Q_2 = {Q2_CEIL_2SIG:.1e} s^-2 is reached at a_0 = {a0_at_ceil:.3e}, where e_N = {eN_c:.2f} and the boost")
P(f"  nu(e_N) - 1 = {100*boost_at_ceil:.2f}%   <-->   Park+2026's published 2% at 95% confidence.")
ck("V4a  reconstructing Park+2026's published 2% boost bound from the Q_2 ceiling through this chain",
   abs(boost_at_ceil - PARK_BOOST_95) < 0.015,
   f"{100*boost_at_ceil:.2f}% reconstructed against {100*PARK_BOOST_95:.0f}% published -- agreement to "
   f"{100*abs(boost_at_ceil - PARK_BOOST_95):.2f} percentage points, which is the expected size of the gap "
   f"between a 2-sigma ceiling on a Gaussian Q_2 posterior and a proper 95%-confidence bound on a nonlinearly "
   f"derived quantity.  This validates eq (12), the etilde<->e_N inversion, the eq-(10) prefactor and the "
   f"a_0^{{3/2}} scaling SIMULTANEOUSLY, against a published quantity that appears nowhere in g04")

P("")
P(f"  {'footing':>10}{'MOND boost at the Sun':>25}{'Park+2026 ceiling':>20}{'over by':>10}")
for fn in A0:
    P(f"  {fn:>10}{100*res[fn]['boost']:>24.1f}%{100*PARK_BOOST_95:>19.0f}%"
      f"{res[fn]['boost']/PARK_BOOST_95:>9.0f}x")
ck("V4b  Route A's own MOND boost at the Sun respects the published 2% bound",
   max(v["boost"] for v in res.values()) < PARK_BOOST_95,
   f"IT DOES NOT, and this is the cleanest statement of the failure available -- cleaner than any sigma.  "
   f"Route A boosts the galactic radial acceleration at the Sun by {100*res['canonical']['boost']:.1f}% "
   f"(canonical) / {100*res['alt']['boost']:.1f}% (alt) against a published ceiling of 2% at 95% confidence: "
   f"over by {res['canonical']['boost']/PARK_BOOST_95:.0f}x / {res['alt']['boost']/PARK_BOOST_95:.0f}x.  It "
   f"involves NO quadrupole integral, NO error bar of ours and NO sigma arithmetic -- just nu(e_N) with "
   f"e_N nu(e_N) = g_ext/a_0.  Quote THIS, not the 16 sigma")

# ------------------------------------------------------------------------------------------ V5
P(""); info("V5 -- is the formally-quoted significance inside the published band?")
P(f"  Park+2026 abstract: tensions 'at the 3-15 sigma level depending on the detailed mass modeling or the")
P(f"  subset of galaxies considered'.  Desmond+2024 abstract: 8.7 sigma fiducial, reduced 'to 1.9 sigma by")
P(f"  removing galaxies with bulges'.  g04's A5b prints +{res['canonical']['sig']:.1f} / +{res['alt']['sig']:.1f} sigma.")
ck("V5a  g04's formal sigma sits INSIDE the published 3-15 sigma band without needing a caveat",
   max(v["sig"] for v in res.values()) <= 15.0,
   f"IT DOES NOT -- +{res['canonical']['sig']:.1f} / +{res['alt']['sig']:.1f} sigma sits just ABOVE Park+2026's "
   f"own published 3-15 sigma range, because g04 fixes g_ext, a_0 and the IF exactly and so carries no model "
   f"variance at all.  This is NOT an error in g04 -- it already forbids quoting 16 alone -- but the honest "
   f"bound is the PUBLISHED band.  RECOMMENDED WORDING: 'several sigma; Park+2026's own published range for "
   f"this tension is 3-15 sigma, and a zero-variance evaluation on Route A's exact footings lands at the top "
   f"of it.'  The robust statements remain the two ratios: {res['canonical']['ratio']:.1f}x-{res['alt']['ratio']:.1f}x "
   f"the Q_2 ceiling, and {res['canonical']['boost']/PARK_BOOST_95:.0f}x-{res['alt']['boost']/PARK_BOOST_95:.0f}x "
   f"the published 2% boost bound")

P(""); P("="*118); P("VERDICT OF THE ADVERSARIAL PASS"); P("="*118)
P(f"""
 THE CLAIM SURVIVES.  Route A's modified-gravity arm gives Q_2 = {res['canonical']['Q2']:.2e} (canonical) /
 {res['alt']['Q2']:.2e} (alt) s^-2 against Park+2026's 2-sigma ceiling {Q2_CEIL_2SIG:.1e}: over by
 {res['canonical']['ratio']:.1f}x / {res['alt']['ratio']:.1f}x.  Reproduced here by a different quadrature, pinned on anchors read
 verbatim from the primary source, on the kernel the anchors are published for (their eq 6 IS Route A).
 Both footings genuinely enter the etilde -> e_N -> q -> Q_2 chain and both fail.

 THE ONE PIECE OF PHYSICS THE CLAIM RESTS ON IS VERIFIED, NOT JUST ASSERTED.  99% of q is built outside
 ~1500 AU and the contribution from inside 100 AU is {inside[100.0]:.0e}.  Route A's exp(-sqrt y) tail lives at
 y ~ 1e8 and is irrelevant to Q_2.  The isotropic-tail discharge and the Q_2 failure are genuinely
 different channels and g04 is right to insist they never be conflated.

 CORRECTION TO g04's WORDING, not to its result: the q weighting is centred nearer r_ext = {r_ext:.0f} AU
 (y ~ e_N = {eNc:.2f}) than r_M = {rM:.0f} AU (y = 1).  A factor ~2 in the quoted radius; nothing else moves.

 THE CLEANEST RESTATEMENT, AND IT IS STRONGER THAN THE SIGMA.  Route A boosts the galactic radial
 acceleration at the Sun by {100*res['canonical']['boost']:.0f}% / {100*res['alt']['boost']:.0f}% against Park+2026's published 2% at 95%
 confidence.  No integral, no sigma, no error bar of ours.  Recommended as the headline.

 WHAT THIS PASS DID NOT VERIFY.  The modified-inertia contrast 7.4e-34 s^-2 is one model on the retired
 kernel; it was not recomputed.  The CLASS-level direction is however the published authors' own reading:
 Desmond+2024 state that a Solar System quadrupole is not generically predicted by modified inertia and
 that the Cassini constraint may be circumvented entirely in such formulations.  So "this observable
 separates the arms" is literature-supported as a direction, while the factor 1e-7 is not independently
 established and must not be quoted as a prediction of the MI class.
""")
sys.exit(ck.done())
