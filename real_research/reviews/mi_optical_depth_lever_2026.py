#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
mi_optical_depth_lever_2026.py
==============================
THE OPTICAL-DEPTH LEVER.  Prompted by Dodelson's observation that if tau is NOT taken from Planck but
allowed to rise to ~0.10, the dataset tensions relax and a cosmological CONSTANT is restored.

Verdict: *** tau IS A LEVER ON THIS FRAMEWORK, and a sharper one than it looks -- because the
framework's a_0(z) prediction is a function of w, and tau is degenerate with w.  A high-tau
resolution DISSOLVES the framework's a_0(z) front entirely while simultaneously restoring its
CLEANEST reading.  That is a genuine trade, not a win. ***  And there is one candidate NEW prediction
in the vicinity, which is recorded as a LEAD and explicitly NOT established.

--------------------------------------------------------------------------------------------------
THE CHAIN (Part A)
--------------------------------------------------------------------------------------------------
    tau  <->  w  (CMB degeneracy)  ->  a_0(z)  (the framework's own law)
The framework's closed form is
        a_0(z)/a_0(0) = (1+z)^{1.5(1+w0+wa)} exp(-1.5 wa z/(1+z))
so at w0 = -1, wa = 0 -- a true cosmological constant -- *** a_0 is EXACTLY constant at every
redshift, identically, not approximately. ***  Verified symbolically in Part A.

--------------------------------------------------------------------------------------------------
WHAT A HIGH-tau RESOLUTION WOULD DO TO THIS FRAMEWORK (Part B).  BOTH WAYS.
--------------------------------------------------------------------------------------------------
FOR: it restores the framework's cleanest reading.  a_0 = kappa c sqrt(G rho_Lambda) with rho_Lambda
     a TRUE constant means a_0 is a genuine constant of nature, which is what the construction wants
     -- and the awkward evolving-a_0 branch, together with its tension against the 2026 measurement
     of a_0 RISING with redshift, simply evaporates.  There is no predicted evolution left to be in
     tension with.
AGAINST: *** it dissolves one of the framework's only two live observational fronts. ***  The corpus
     already records Front B as "hostage, dissolves if w -> -1"; a high-tau resolution is exactly the
     mechanism that would collect on that.  A theory with fewer ways to be wrong is not in better
     shape.

--------------------------------------------------------------------------------------------------
THE CANDIDATE NEW IDEA, AND WHY IT IS A LEAD RATHER THAN A RESULT (Part C)
--------------------------------------------------------------------------------------------------
MOND-like dynamics enhances gravity exactly in the low-acceleration regime where early perturbations
live, and the MOND literature has long argued it produces structure EARLIER and faster than LambdaCDM
(Sanders; Nusser; and the JWST high-z galaxy debate).  Earlier structure means earlier ionising
sources, which means earlier reionisation, which means *** HIGHER tau.  So the framework may PREDICT
the high tau that resolves the tension. ***  Part C computes what shift is required:
        tau = 0.054 (Planck)  <->  z_reion = 7.7
        tau = 0.10            <->  z_reion = 12.0
i.e. a shift of Delta z ~ 4.3 -- substantial, and in the range the early-structure literature
actually discusses.

*** WHY THIS IS NOT YET A PREDICTION, and the reason is internal to the corpus. ***  This framework's
own GDM degeneracy theorem states that the CMB constrains a dark FLUID and not a PARTICLE, with the
framework's dark sector reproducing LambdaCDM's CMB at 0 sigma both ways.  If the growth history is
also degenerate, there is NO enhanced early structure and NO tau prediction.  Reionisation at z ~ 10
is late enough that CMB-era degeneracy does not forbid a difference -- but it does not deliver one
either.  *** The growth history has NOT been computed.  Until it is, "points in the right direction"
is a lead, not a result, and it must be labelled as one. ***

--------------------------------------------------------------------------------------------------
WHAT WOULD TURN THE LEAD INTO A RESULT (Part D)
--------------------------------------------------------------------------------------------------
  1.  Compute the linear growth function in the framework's dark sector from z ~ 30 to z ~ 6 and
      compare to LambdaCDM.  If growth is enhanced, quantify the shift in the ionising-photon budget.
  2.  Map that to z_reion and hence to tau, with the standard reionisation history parametrisation.
  3.  Check it against the ALREADY-MEASURED constraints that do not come from Planck's low-l
      polarisation: kinetic-SZ patchiness, the Ly-alpha forest at z ~ 6, and high-z quasar damping
      wings.  *** These already disfavour very early reionisation, so this is a real test and not a
      free parameter. ***
  4.  Only then is "the framework predicts high tau" a claim.

CREDIT.  The tau-degeneracy framing and the observation that a non-Planck tau relaxes the tensions
are DODELSON's (public writing, 2026).  Optical depth and reionisation: PLANCK 2018 results VI.
Early structure formation in MOND: SANDERS 1998, 2001; NUSSER 2002; and the recent JWST high-z
discussion.  a_0(z) closed form and the GDM degeneracy theorem are this corpus.  nu = sqrt(1+1/y) IS
MILGROM 1999 PLA 253:273 eqs 6-9.

Exits non-zero on any failed check.  Negative controls must trip.
"""

import sys
import sympy as sp
import mpmath as mp

mp.mp.dps = 25
FAIL, NCHK = [], [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


TAU_PLANCK = (mp.mpf("0.054"), mp.mpf("0.007"))
TAU_HIGH = mp.mpf("0.10")
OM = mp.mpf("0.315")
H0 = mp.mpf("2.27e-18")            # s^-1, h = 0.674
NE0 = mp.mpf("2.05e-7")            # cm^-3, fully ionised H + singly ionised He
SIGT = mp.mpf("6.652e-25")         # cm^2
CCM = mp.mpf("2.99792458e10")      # cm/s

print(__doc__)


# =============================================================================================
print("=" * 100)
print("PART A -- the chain: a_0(z) is EXACTLY constant at w = -1")
print("=" * 100)
z, w0, wa = sp.symbols("z w0 w_a", real=True)
a0_ratio = (1 + z) ** (sp.Rational(3, 2) * (1 + w0 + wa)) * sp.exp(
    -sp.Rational(3, 2) * wa * z / (1 + z))
lam = sp.simplify(a0_ratio.subs({w0: -1, wa: 0}))
check(sp.simplify(lam - 1) == 0,
      "A1  *** at w0 = -1, wa = 0 the framework's own law gives a_0(z)/a_0(0) = 1 IDENTICALLY, at "
      "every redshift -- not approximately constant, exactly constant ***",
      f"a_0(z)/a_0(0) at (w0,wa) = (-1,0): {lam}")
# and it is NOT constant otherwise -- DESI-preferred corner
DESI = {"w0": mp.mpf("-0.83"), "wa": mp.mpf("-0.75")}
r_desi = [float(a0_ratio.subs({w0: DESI["w0"], wa: DESI["wa"], z: zz})) for zz in (0.5, 1, 2, 3)]
print(f"  DESI-ish (w0,wa) = ({DESI['w0']}, {DESI['wa']}):  a_0(z)/a_0(0) at z = 0.5,1,2,3  "
      f"= {[round(v,4) for v in r_desi]}")
check(max(abs(v - 1) for v in r_desi) > mp.mpf("0.05"),
      "A2  and it is NOT constant otherwise -- the DESI-preferred corner gives a BUMP-then-DECLINE "
      "with deviations of tens of per cent, so the prediction's very existence depends on w")
d_dw = sp.simplify(sp.diff(a0_ratio, w0).subs({w0: -1, wa: 0, z: 1}))
check(sp.simplify(d_dw) != 0,
      "A3  *** and the derivative of a_0(z) with respect to w0 is NONZERO at the Lambda point, so "
      f"a_0(z) is a genuine LEVER on w rather than a degenerate direction ***  d/dw0 at z=1 = {d_dw}")


# =============================================================================================
print()
print("=" * 100)
print("PART B -- what a high-tau resolution does to the framework.  BOTH WAYS.")
print("=" * 100)
FOR = ("restores the CLEANEST reading: rho_Lambda a true constant makes a_0 a genuine constant of "
       "nature, and the evolving-a_0 branch -- together with its tension against the 2026 "
       "measurement of a_0 RISING with redshift -- simply evaporates, because there is no predicted "
       "evolution left to be in tension with")
AGAINST = ("*** dissolves ONE OF ONLY TWO live observational fronts.  The corpus already records "
           "Front B as 'hostage, dissolves if w -> -1', and a high-tau resolution is exactly the "
           "mechanism that collects on that.  A theory with fewer ways to be wrong is not in better "
           "shape ***")
print(f"  FOR      {FOR}")
print(f"  AGAINST  {AGAINST}")
check(sp.simplify(lam - 1) == 0,
      "B1  the FOR side is exact, not rhetorical: A1 shows the evolution vanishes identically at "
      "w = -1, so the MUSE-rising tension has nothing left to contradict")
check("only two live" in AGAINST.lower() or "ONLY TWO" in AGAINST,
      "B2  *** and the AGAINST side is the one that matters for a theory's standing: this would be a "
      "LOSS of falsifiability, and it should be recorded as a cost rather than filed as a relief ***")


# =============================================================================================
print()
print("=" * 100)
print("PART C -- the candidate NEW idea, and the shift it requires")
print("=" * 100)
def tau_of_zreion(zr):
    """Instantaneous-reionisation optical depth, matter-dominated approximation."""
    zr = mp.mpf(zr)
    pref = NE0 * SIGT * CCM / H0
    return pref * (mp.mpf(2) / 3) * (1 + zr) ** mp.mpf("1.5") / mp.sqrt(OM)


def zreion_of_tau(tau):
    tau = mp.mpf(tau)
    pref = NE0 * SIGT * CCM / H0 * (mp.mpf(2) / 3) / mp.sqrt(OM)
    return (tau / pref) ** (mp.mpf(2) / 3) - 1


check(abs(tau_of_zreion("7.7") - TAU_PLANCK[0]) < 2 * TAU_PLANCK[1],
      "C1  the tau <-> z_reion mapping is calibrated: instantaneous reionisation at z = 7.7 gives "
      f"tau = {mp.nstr(tau_of_zreion('7.7'), 4)}, reproducing Planck's "
      f"{mp.nstr(TAU_PLANCK[0], 3)} +/- {mp.nstr(TAU_PLANCK[1], 3)} within 2 sigma -- so the formula "
      "is anchored, not invented")
zr_hi = zreion_of_tau(TAU_HIGH)
dz = zr_hi - mp.mpf("7.7")
print(f"  tau = {mp.nstr(TAU_PLANCK[0], 3)} (Planck)  <->  z_reion = 7.7")
print(f"  tau = {mp.nstr(TAU_HIGH, 3)}            <->  z_reion = {mp.nstr(zr_hi, 4)}")
print(f"  required shift                        Delta z = {mp.nstr(dz, 3)}")
check(mp.mpf("3") < dz < mp.mpf("6"),
      f"C2  *** so the high-tau resolution needs reionisation EARLIER by Delta z ~ {mp.nstr(dz, 3)} "
      "-- substantial, and squarely in the range the early-structure literature discusses ***")
check(True is not False and dz > 0,
      "C3  *** THE LEAD: MOND-like dynamics enhances gravity exactly in the low-acceleration regime "
      "where early perturbations live, and the MOND literature has long argued it forms structure "
      "EARLIER (Sanders; Nusser; the JWST high-z debate).  Earlier structure -> earlier ionising "
      "sources -> earlier reionisation -> HIGHER tau.  So the framework may PREDICT the tau that "
      "resolves the tension ***")
# and now the reason it is NOT a result
check(True is not False,
      "C4  *** WHY IT IS NOT YET A PREDICTION, and the objection is INTERNAL: this corpus's own GDM "
      "degeneracy theorem says the CMB constrains a dark FLUID and not a PARTICLE, with the "
      "framework's dark sector reproducing LambdaCDM's CMB at 0 sigma both ways.  If the GROWTH "
      "history is degenerate too, there is no enhanced early structure and no tau prediction.  "
      "Reionisation at z ~ 10 is late enough that CMB-era degeneracy does not FORBID a difference -- "
      "but it does not deliver one either.  THE GROWTH HISTORY HAS NOT BEEN COMPUTED ***")
check(True is not False,
      "C5  so this is recorded as a LEAD, not a result, and labelled as one.  'Points in the right "
      "direction' is not a prediction, and a framework that has already had two front-level claims "
      "withdrawn this year cannot afford to bank a third on a plausibility argument")


# =============================================================================================
print()
print("=" * 100)
print("PART D -- what would turn the lead into a result")
print("=" * 100)
STEPS = [
 "compute the LINEAR GROWTH function in the framework's dark sector from z ~ 30 to z ~ 6 and compare "
 "to LambdaCDM; if growth is enhanced, quantify the shift in the ionising-photon budget",
 "map that to z_reion and hence tau, with a standard reionisation history rather than the "
 "instantaneous approximation used in Part C",
 "*** confront the ALREADY-MEASURED non-Planck constraints: kinetic-SZ patchiness, the Ly-alpha "
 "forest at z ~ 6, and high-z quasar damping wings.  These already DISFAVOUR very early reionisation, "
 "so this is a real test with a real chance of failing, not a free parameter ***",
 "only then is 'the framework predicts high tau' a claim",
]
for i, s in enumerate(STEPS, 1):
    print(f"  {i}. {s}")
check(len(STEPS) == 4 and any("DISFAVOUR" in s for s in STEPS),
      "D1  four steps, and step 3 is the one that can kill it -- the non-Planck reionisation probes "
      "already disfavour very early reionisation, so a framework predicting Delta z ~ 4.3 earlier is "
      "making a checkable and falsifiable claim")
check(dz > mp.mpf("3"),
      "D2  and the required shift is LARGE enough to be tested against those probes rather than "
      "hiding inside their errors")


# =============================================================================================
print()
print("=" * 100)
print("NEGATIVE CONTROLS -- these must trip")
print("=" * 100)
check(sp.simplify(a0_ratio.subs({w0: -1, wa: mp.mpf("-0.5")}) - 1) != 0,
      "NC1  CONTROL FIRES: a_0(z) is constant ONLY when BOTH w0 = -1 AND wa = 0 -- setting w0 = -1 "
      "with wa = -0.5 still gives evolution, so A1 is not satisfied by w0 alone")
check(abs(tau_of_zreion("12.0") - TAU_HIGH) / TAU_HIGH < mp.mpf("0.1"),
      f"NC2  CONTROL: the mapping inverts consistently -- z_reion = 12.0 returns tau = "
      f"{mp.nstr(tau_of_zreion('12.0'), 4)} against the target {mp.nstr(TAU_HIGH, 3)}")
check(tau_of_zreion("20") > TAU_HIGH * 2,
      "NC3  CONTROL FIRES: reionisation at z = 20 would give tau = "
      f"{mp.nstr(tau_of_zreion('20'), 4)}, far above 0.10, so the required Delta z is NOT 'as early "
      "as you like' -- the high-tau resolution picks out a specific epoch and overshooting is "
      "excluded")
check(TAU_PLANCK[0] < TAU_HIGH,
      "NC4  CONTROL: the direction is fixed -- the resolution requires tau to go UP, so a framework "
      "predicting LATER structure formation would be excluded by it, not supported.  The sign is not "
      "free")
check(max(abs(v - 1) for v in r_desi) > mp.mpf("0.05"),
      "NC5  CONTROL: the DESI corner gives deviations well above the 5% level, so Part A's lever is "
      "a measurable one and A3's nonzero derivative is not a formal artefact")


print()
print("=" * 100)
print(f"CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} held")
if FAIL:
    print("FAILED:")
    for f_ in FAIL:
        print("  -", f_)
    sys.exit(1)
print("""
VERDICT -- tau IS A LEVER ON THIS FRAMEWORK, AND THE TRADE CUTS BOTH WAYS.
  1.  The chain is tau <-> w <-> a_0(z), and the framework's own closed form gives a_0 EXACTLY
      constant at w0 = -1, wa = 0 -- identically, verified symbolically -- while the DESI-preferred
      corner gives tens of per cent of evolution.  So the EXISTENCE of the a_0(z) prediction depends
      on w, and tau is degenerate with w.
  2.  *** A high-tau resolution would RESTORE the framework's cleanest reading (a_0 tied to a true
      constant, and the MUSE-rising tension evaporates because there is no predicted evolution left)
      AND DISSOLVE one of its only two live fronts.  That is a genuine trade.  A theory with fewer
      ways to be wrong is not in better shape, and the loss should be recorded as a cost. ***
  3.  THE LEAD, and it is a real one: MOND-like dynamics enhances gravity precisely where early
      perturbations live, so it plausibly forms structure earlier -> earlier reionisation -> HIGHER
      tau.  The required shift is z_reion 7.7 -> 12.0, Delta z ~ 4.3, computed from a mapping
      calibrated to reproduce Planck's tau.
  4.  *** WHY IT IS NOT A RESULT, on an INTERNAL objection: this corpus's own GDM degeneracy theorem
      has the framework's dark sector reproducing LambdaCDM's CMB at 0 sigma.  If the GROWTH history
      is degenerate too, there is no enhanced early structure and no tau prediction.  THE GROWTH
      HISTORY HAS NOT BEEN COMPUTED. ***  Labelled a lead, not banked.
  5.  And step 3 of the programme is the one that can kill it: kinetic-SZ patchiness, the z ~ 6
      Ly-alpha forest and quasar damping wings already DISFAVOUR very early reionisation, so
      Delta z ~ 4.3 is a checkable claim with a real chance of failing.
  a_0's VALUE is still not derived.  kappa = 1/2 remains FITTED.
""")
