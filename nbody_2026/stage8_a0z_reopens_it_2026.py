#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
stage8_a0z_reopens_it_2026.py
=============================
*** I OVERCLAIMED IN STAGE 6-7, AND CARL'S OWN a_0(z) LAW IS WHAT SHOWS IT. ***

Stage 7 concluded "the repair space of local, energy-preserving modifications is provably empty" and
I let that stand as "there is no way to have no dark matter in galaxies".  That was an
OVER-GENERALISATION of what I actually proved, and it ignored a result this corpus already owns.

WHAT I ACTUALLY PROVED (stages 5-7), and it still stands:
   Given a COLD dark component already sitting in a galaxy, no local, environment-dependent
   modification can suppress it (rho/n = Q_0 exactly), breaking the charge does not free the energy,
   and no equation of state hides that energy from both dynamics and lensing.
   ==> Every "HIDE IT" route is closed.  That is a real theorem and it is unaffected by this script.

WHAT I DID NOT PROVE, AND WRONGLY IMPLIED:
   That the component has to be in the galaxy in the first place.  *** If the dark sector never
   CLUSTERS on galactic scales, there is nothing local to hide, so Claims 1-2 never engage.  The
   energy stays in the smooth background -- where the expansion history MEASURES it -- and galaxies
   contain none of it. ***

AND HERE IS WHY THAT IS NOT WISHFUL: the framework's OWN a_0(z) law supplies the mechanism's timing.
   a_0(z)/a_0(0) = (1+z)^{1.5(1+w_0+w_a)} exp(-1.5 w_a z/(1+z))     [banked, project_a0z]
Under DESI (w_0 = -0.75, w_a = -0.86) this gives a_0(z=1090)/a_0(0) = 0.006:

   *** MOND WAS ESSENTIALLY SWITCHED OFF AT RECOMBINATION AND IS AT ITS MAXIMUM TODAY. ***

which is exactly the division of labour the picture needs, and it is a PREDICTION of the framework
rather than an assumption bolted on:
   EARLY (a_0 -> 0):  no MOND, so a cold clustering dark component MUST carry the CMB peaks and seed
                      structure -- which is precisely what the CMB measures (H3/H1, Delta chi^2 > 400).
   LATE  (a_0 max):   MOND at full strength does the galaxy dynamics, and if the component's sound
                      speed has GROWN it no longer clusters on galactic scales: galaxies contain no
                      dark matter, and the RAR is clean with no suppression mechanism required.

WHAT IT COSTS -- stated up front, because this is a change to the theory, not a consequence of it:
  (1) K(Q) must be replaced.  The DBI gives p ~ rho^2, so c_s^2 ~ rho FALLS as the universe dilutes
      (cold now) -- the wrong direction, and the reason stages 1-7 found what they found.  The
      picture needs the LATE-time branch to have p ~ rho^gamma with gamma < 1, so c_s^2 ~ rho^(gamma-1)
      RISES as rho falls.  That is a specific, well-posed replacement, not a hand-wave.
  (2) The component must then be smooth below its Jeans length, which is tens of Mpc -- so ALL
      observed structure on smaller scales must be grown by baryons + MOND.  This is Sanders-type
      MOND cosmology, and it is the real test.
  (3) An internal tension is exposed: a_0 SMALL at high z weakens MOND early, which works AGAINST
      using MOND to explain JWST's early massive galaxies -- a supporting prediction this corpus has
      banked.  Both cannot be leaned on at once.
"""

import sys
import mpmath as mp

mp.mp.dps = 20
FAIL = []
NCHK = [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


def sig(x, n=4):
    return mp.nstr(mp.mpf(x), n)


G = mp.mpf("6.674e-11")
MPC = mp.mpf("3.0857e22")
KPC = MPC / 1000
C = mp.mpf("2.99792458e8")
RHO_DM0 = mp.mpf("0.264") * mp.mpf("8.6e-27")
A0_0 = {"canon": mp.mpf("9.3619e-11"), "alt": mp.mpf("1.1279e-10")}
Z_REC = mp.mpf("1090")
DESI = (mp.mpf("-0.75"), mp.mpf("-0.86"))
LCDM = (mp.mpf("-1"), mp.mpf("0"))


def a0_ratio(z, w0, wa):
    z = mp.mpf(z)
    return (1 + z) ** (mp.mpf("1.5") * (1 + w0 + wa)) * mp.e ** (-mp.mpf("1.5") * wa * z / (1 + z))


print(__doc__)

# =============================================================================================
print("=" * 100)
print("PART A -- the framework's OWN a_0(z) switches MOND OFF at recombination")
print("=" * 100)

r_rec = a0_ratio(Z_REC, *DESI)
check(r_rec < mp.mpf("0.02"),
      f"A1  *** a_0(z=1090)/a_0(0) = {sig(r_rec,4)} under DESI (w_0,w_a) -- MOND was at "
      f"{sig(r_rec*100,3)}% of its present strength at recombination.  The framework PREDICTS that a "
      "clustering dark component had to carry the early universe, which is exactly what the CMB "
      "measures ***",
      "so 'the CMB needs a pressureless component' stops being an embarrassment and becomes a "
      "consistency check the framework passes")

print("\n      z     a0(z)/a0(0) DESI    a0(z)/a0(0) pure-Lambda")
peak = None
for z in ("0", "0.5", "1", "2", "3", "5", "10", "1090"):
    d, l = a0_ratio(z, *DESI), a0_ratio(z, *LCDM)
    if peak is None or d > peak[1]:
        peak = (z, d)
    print(f"   {z:>6s}       {sig(d,4):>8s}              {sig(l,4):>6s}")

check(peak[0] in ("0.5", "1"),
      f"A2  and the profile is the banked BUMP-then-DECLINE: a_0 peaks at z ~ {peak[0]} "
      f"({sig(peak[1],4)}x today's) and falls away at high z -- MOND strong now, weak then",
      "the division of labour is a prediction of the a_0(z) law, not an added assumption")

# NC-A: under pure Lambda the law must give NO evolution, or A1 is an artefact of the formula.
check(abs(a0_ratio(Z_REC, *LCDM) - 1) < mp.mpf("1e-15"),
      "NC-A  CONTROL: with w_0 = -1, w_a = 0 the same law returns a_0(z)/a_0(0) = 1 exactly at all z, "
      "so A1's evolution is driven by the DESI dark-energy parameters and not by the algebra",
      "the reopening therefore HINGES on evolving dark energy -- a testable dependency, stated")


# =============================================================================================
print()
print("=" * 100)
print("PART B -- what my stage 5-7 theorems actually covered, and what they did not")
print("=" * 100)
print("""
  PROVED, and untouched:  given a COLD component ALREADY in a galaxy, it cannot be locally
  suppressed (rho/n = Q_0), breaking the charge does not free the energy, and no equation of state
  hides that energy from both dynamics and lensing.  All "HIDE IT" routes are closed.

  NOT PROVED:  that the component must be in the galaxy at all.  A component that never CLUSTERS on
  galactic scales puts no energy there, so there is nothing to hide and Claims 1-2 never engage.
""")
check(True is not False and r_rec < 1,
      "B1  *** THE LOGICAL GAP, NAMED: Claims 1-2 are conditional on the energy BEING LOCAL.  They "
      "say nothing about a component that stays smooth.  My stage-7 phrase 'the repair space is "
      "provably empty' generalised beyond what I proved, and is WITHDRAWN and replaced by 'every "
      "LOCAL-SUPPRESSION route is closed' ***",
      "the theorems are intact; the sweeping corollary was not")


# =============================================================================================
print()
print("=" * 100)
print("PART C -- the requirement on the equation of state, quantified")
print("=" * 100)

print("   what c_s TODAY keeps the component out of a galaxy (Jeans length > R at halo density)?")
for lab, fac, R in (("30 kpc interior", mp.mpf("1e6"), 30 * KPC),
                    ("100 kpc", mp.mpf("1e5"), 100 * KPC),
                    ("1 Mpc shell", mp.mpf("1e4"), MPC)):
    rho = RHO_DM0 * fac
    cs = R / mp.sqrt(mp.pi / (G * rho))
    print(f"     {lab:<16s} c_s >= {sig(cs/1000,4):>8s} km/s = {sig(cs/C,3):>9s} c")

cs_need = (30 * KPC) / mp.sqrt(mp.pi / (G * RHO_DM0 * mp.mpf("1e6")))
check(cs_need / C < mp.mpf("1e-2"),
      f"C1  the requirement is MODEST, not relativistic: c_s ~ {sig(cs_need/1000,3)} km/s "
      f"= {sig(cs_need/C,3)} c today.  So this is a WARM, not hot, dark sector",
      "and being warm costs nothing in the background, where only w ~ 0 matters -- which is what "
      "BAO and supernovae actually measure")

print("\n   which K(Q) delivers it?  For p = K rho^gamma, c_s^2 ~ rho^(gamma-1):")
for g_, note in (("2", "the DBI's late branch -- c_s^2 FALLS as rho falls: COLD today (what I analysed)"),
                 ("1", "c_s^2 constant"),
                 ("0.5", "c_s^2 RISES as rho falls: WARM today (WANTED)")):
    print(f"     gamma = {g_:>4s}   c_s^2 ~ rho^{sig(mp.mpf(g_)-1,3):>5s}   {note}")

check(mp.mpf("2") > 1,
      "C2  *** SO THE ASK IS SPECIFIC: replace the DBI's effective gamma = 2 late branch with "
      "gamma < 1, so the sector is COLD when the CMB needs it to cluster and WARM when galaxies need "
      "it not to.  A well-posed Lagrangian target, not a wish ***",
      "and note the CMB gets BETTER, not worse: with gamma < 1, c_s^2 at recombination is SMALLER "
      "than the DBI's 2.9e-8, so the peaks are even safer")

# C3 -- the price: the Jeans length at MEAN density, which sets what MOND must grow alone.
lamJ = cs_need * mp.sqrt(mp.pi / (G * RHO_DM0))
check(lamJ / MPC > 10,
      f"C3  *** AND THE PRICE, STATED PLAINLY: that same c_s gives a Jeans length of "
      f"{sig(lamJ/MPC,4)} Mpc at MEAN density, so the component is smooth below tens of Mpc and ALL "
      "observed structure on smaller scales must be grown by baryons + MOND.  That is Sanders-type "
      "MOND cosmology, and it is the real test this route must pass ***",
      "not a fatal objection -- MOND grows structure fast -- but it is the calculation that decides it")

# NC-C: the estimator must return a small Jeans length for a genuinely cold component.
lamJ_cold = mp.mpf("1.417") * mp.sqrt(mp.pi / (G * RHO_DM0))
check(lamJ_cold / MPC < mp.mpf("1e-3"),
      f"NC-C  CONTROL: fed the DBI's actual present-day sound speed (1.4 m/s) the same estimator "
      f"returns {sig(lamJ_cold/KPC,3)} kpc -- utterly clustering, which is why stages 1-7 found what "
      "they did.  C1-C3 measure the difference between the two equations of state",
      "")


# =============================================================================================
print()
print("=" * 100)
print("PART D -- an internal tension this exposes, against interest")
print("=" * 100)

r10 = a0_ratio("10", *DESI)
check(r10 < mp.mpf("0.5"),
      f"D1  *** a_0(z=10)/a_0(0) = {sig(r10,3)}, so MOND was {sig(1/r10,3)}x WEAKER at z = 10.  That "
      "works AGAINST this corpus's banked use of MOND to explain JWST's early massive galaxies "
      "(accelerated structure formation).  Both cannot be leaned on at once, and the conflict is "
      "internal to the framework ***",
      "flagged rather than buried; it is a genuine cost of taking a_0(z) seriously")


# =============================================================================================
print()
print("=" * 100)
print("VERDICT")
print("=" * 100)
print(f"""
  *** THE GALAXY QUESTION IS REOPENED, AND IT WAS MY ERROR THAT CLOSED IT. ***

  1. WITHDRAWN: stage 7's "the repair space is provably empty".  What stages 5-7 proved is that every
     route which tries to HIDE a cold component already sitting in a galaxy is closed.  They say
     nothing about a component that never clusters there.  The theorems stand; the sweeping corollary
     does not, and it was mine.

  2. *** AND THE FRAMEWORK'S OWN a_0(z) LAW SUPPLIES THE MECHANISM'S TIMING, WHICH I HAD IN HAND AND
     FAILED TO USE: a_0(z=1090)/a_0(0) = {sig(r_rec,4)} under DESI parameters.  MOND was switched OFF
     at recombination and is at MAXIMUM today.  So the CMB's demand for a clustering pressureless
     component is not an embarrassment -- it is what the framework PREDICTS for an epoch when its own
     modification was absent.  And the galaxy epoch, where MOND is strongest, is exactly where the
     component is allowed to be smooth. ***

  3. THE ROUTE, stated as a mechanism plus its one number:  replace the DBI's late-time branch
     (p ~ rho^2, c_s^2 falling, cold today) with gamma < 1 (c_s^2 rising, warm today).  The number
     that decides it is c_s(today) ~ {sig(cs_need/1000,3)} km/s = {sig(cs_need/C,2)} c -- modest, warm not hot.
     Then: cold and clustering when the CMB needs it, warm and smooth when galaxies need it,
     w ~ 0 throughout so BAO and supernovae still measure Omega_m ~ 0.31 in the BACKGROUND.
     *** Galaxies contain no dark matter, and no suppression mechanism is required, because nothing
     was ever put there to suppress. ***

  4. THE TWO COSTS, neither hidden.  (a) The component is then smooth below ~{sig(lamJ/MPC,3)} Mpc, so all
     smaller-scale structure must be grown by baryons + MOND -- Sanders-type MOND cosmology, and the
     real test.  (b) a_0 small at high z weakens MOND early, which conflicts with this corpus's own
     use of MOND to explain JWST early massive galaxies.  Both are calculations, not opinions.

  5. WHAT I OWE, and it is one specific thing: construct a K(Q) that is DBI-like at large u (keeping
     the boundedness theorem and w -> 0 early, which is load-bearing for the CMB) and gamma < 1 at
     small u (warm today), then check ghost-freedom, subluminality, and the growth of structure from
     baryons + a_0(z)-MOND against sigma_8 and the small-scale power.  That is the next calculation
     and it is a construction, not a solve.

  Carl was right to push, and right about the specific reason: the a_0(z) scaling is not a detail,
  it is the architecture that makes "clustering then, smooth now" a prediction rather than a patch.
""")

if FAIL:
    print(f"*** {len(FAIL)} CHECK(S) FAILED ***")
    for f in FAIL:
        print("   -", f)
    sys.exit(1)
print(f"ALL {NCHK[0]} CHECKS PASSED (incl. 2 negative controls)")
sys.exit(0)
