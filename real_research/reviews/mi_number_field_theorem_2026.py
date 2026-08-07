#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
AMENDMENT 2026-08-07 (see `mi_number_field_local_presentation_2026.py`, 29/29)
-----------------------------------------------------------------------------
THEOREM 3's against-interest reading below -- "the existence of a clean EVEN-weight competitor at
8% is the strongest number-theoretic argument that the framework's sqrt(pi) is an artefact of its
own construction" -- is PRESENTATION-DEPENDENT and is WITHDRAWN AS STATED.

The pi-weights are computed against c H_Lambda.  Computed instead against the LOCAL scale
c sqrt(G rho_Lambda), the parities SWAP: the framework's coefficient is kappa = 1/2, weight 0
(ALGEBRAIC), while Milgrom 2020's is sqrt(2/3 pi), weight -1/2 (transcendental) -- as this file's
own check w(kappa_Milgrom) = -1/2 already records.  So neither coefficient is intrinsically the
"clean" one; the parity is a property of which scale you divide by.

WHAT SURVIVES UNCHANGED: Theorem 1, Theorem 2, Corollary 2a, Corollary 2b as arithmetic statements
about the HORIZON presentation; the rigidity of the 8% gap (the two coefficients sit in different
weight classes in BOTH presentations, so no rational re-choice of kappa closes it); and escapes
E1-E5.  The mirror-image PRO-framework argument is equally void: the pi-arithmetic favours NEITHER
coefficient.  kappa = 1/2 remains FITTED, NOT DERIVED.
"""

r"""
LANE G4 -- THE NUMBER-FIELD OBSTRUCTION, PROMOTED FROM COMPUTATION TO THEOREM
============================================================================

Repo : zimmerman-formula   (Carl Zimmerman's modified-inertia framework)
File : real_research/reviews/mi_number_field_theorem_2026.py
Date : 2026-08-07

WHAT THIS IS
------------
The corpus records a "NUMBER-FIELD OBSTRUCTION" (computed 2026-06-27, never proved):

    Z = 2 sqrt(8 pi / 3) carries sqrt(pi), a TRANSCENDENTAL, while all flavour data
    (mass ratios, mixing angles) is ALGEBRAIC.  So a_0/Z is structurally gauge-blind.

This script does four things:

  (A) States and PROVES the obstruction as a theorem, with explicit hypotheses,
      for a class of relations that is named exactly and not one atom wider.
  (B) Names the invariant that does the work: the pi-WEIGHT, and its mod-1 residue
      (PARITY).  The framework's coefficient is HALF-INTEGER weight; every object it
      could ever be equated to on the Standard-Model side is INTEGER weight.
  (C) Gives the CONSTRUCTIVE HALF: five escapes, each with the exact hypothesis it
      breaks and the exact object it would have to supply.  That list is the map of
      where an SM bridge could still live.  Two of the escapes are WIDE, and saying so
      is a CORRECTION to the corpus's own phrasing (see "SCOPE CORRECTION" below).
  (D) Records the honest theory-vs-data tension in arithmetic form: the theoretically
      natural coefficient (Milgrom's 2 pi) and the data-favoured one (kappa = 1/2) sit
      in DIFFERENT pi-weight classes, so the 8.2% gap between them is not closable by
      any rational re-choice of kappa.

THIS IS NOT A UNIFICATION CLAIM.  It is the opposite: a proof of why a whole class of
unification attempts must fail, plus an honest statement of which classes it does NOT
cover.  Nothing here derives Z, Lambda, a_0 or any SM parameter, and nothing here
should ever be cited as doing so.

SCOPE CORRECTION TO THE CORPUS (stated up front, against interest)
------------------------------------------------------------------
The corpus phrase "no algebraic relation can connect them" / "structurally gauge-blind"
is TRUE for finite Q_bar-rational relations (Theorem 1 below) and is FALSE as an
unqualified statement about derivations.  pi is itself the limit of a sequence of
rationals (Wallis), so any construction containing an infinite sum, infinite product,
mode sum or functional determinant can and routinely does manufacture pi -- including a
half-integer power of it -- out of purely algebraic input.  The obstruction bans a
finite algebraic IDENTITY.  It does not ban a DERIVATION.  Check 9 below demonstrates
this with an explicit rational sequence converging to pi/2.  The honest headline is
therefore "no finite algebraic bridge", not "no bridge".

Second honest limit, equally important: a_0 itself is not a pure number.  Its value
involves the measured Lambda (or H_Lambda), an empirical real that is not known to be
algebraic or transcendental.  So NO arithmetic obstruction whatsoever applies to
"a_0 versus a lepton mass".  The theorem constrains only the framework's DIMENSIONLESS
COEFFICIENT a_0/(c H_Lambda) = 2 kappa / Z against DIMENSIONLESS flavour ratios.  That
is the entire arena, and it is narrower than the corpus wording implies.

THE SETUP
---------
Framework constants (canonical footing):
    Z         = 2 sqrt(8 pi / 3)  = 5.78881003647...,   1/Z = 0.172747074736...
    kappa     = 1/2               (FITTED, NOT DERIVED -- the one knob)
    rho_Lam   = Lambda c^2 / (8 pi G),      H_Lam = c sqrt(Lambda / 3)
    a_0       = kappa c sqrt(G rho_Lam)     [exact law: g_obs^2 = g_bar^2 + a_0 g_bar]
  =>  a_0 / (c H_Lam) = 2 kappa / Z = kappa sqrt(3 / (8 pi))      <-- Check 3
    canonical a_0 = 9.36e-11 m/s^2 ; ALT footing = 1.13e-10 (larger by 1/sqrt(Om_Lam))

Let  s := sqrt(pi)  and  Q_bar := the field of algebraic numbers.
Every dimensionless framework constant above lies in Q_bar(s):
    pi = s^2,   Z = 2 sqrt(8/3) * s,   a_0/(c H_Lam) = kappa sqrt(3/8) / s.

THEOREM 1 (NO FINITE ALGEBRAIC BRIDGE).
  Hypotheses:
    (H1) pi is transcendental over Q.                       [Lindemann 1882]
    (H2) the framework's dimensionless content lies in Q_bar(s), s = sqrt(pi).
    (H3) the flavour side of the proposed relation is an algebraic number A in Q_bar
         (this is a MODELLING assertion, see H3 discussion below).
    (H4) the relation is a finite rational function over Q_bar in the framework
         constants.
  Claim:  Let R be in Q_bar(t), defined at t = s, and let A be in Q_bar.  Then
              R(s) = A   <=>   R == A  identically as a rational function.
  Proof:  By (H1), pi is transcendental over Q, hence over Q_bar (Q_bar is algebraic
    over Q).  If s = sqrt(pi) were algebraic then pi = s^2 would be algebraic; so s is
    transcendental over Q_bar.  Since Q_bar is algebraically closed and s is
    transcendental over it, Q_bar[s] is a polynomial ring and the evaluation
    Q_bar[t] -> R, t |-> s, is INJECTIVE.  Write R = P/Q with P, Q in Q_bar[t],
    Q(s) != 0.  Then R(s) = A gives (P - A*Q)(s) = 0, and P - A*Q is in Q_bar[t]
    because A is in Q_bar by (H3); injectivity forces P - A*Q == 0, i.e. R == A.  QED
  Corollary (PREDICTIVE EMPTINESS / "gauge-blindness", now proved for this class):
    such a relation holds for EVERY value of s, hence carries no information about the
    value of pi, hence none about Z, kappa or a_0.  The framework constant drops out.
    An exact bridge in this class is a RELABELLING, not a prediction.

THEOREM 2 (THE INVARIANT: HALF-INTEGER pi-WEIGHT).
  Let G be the multiplicative group Q_bar^* . pi^Q.  By (H1) this is a DIRECT product
  (if pi^r were algebraic for rational r != 0 then pi would be algebraic), so
        w : G -> Q,    w(alpha * pi^r) = r
  is a well-defined homomorphism -- the pi-WEIGHT.  Then:
        w(pi) = 1,   w(Z) = 1/2,   w(a_0/(c H_Lam)) = -1/2   [kappa in Q_bar],
        w(1/(2 pi)) = -1  (Milgrom's coefficient),   w(A) = 0 for A in Q_bar^*.
  Claim:  b in G is algebraic  <=>  w(b) = 0.
  Corollary 2a (ONE-RATIONAL-NUMBER CHANNEL).  In the group <Z, kappa> generated by
  the framework's box, w(Z^m kappa^n) = m/2, which vanishes iff m = 0.  So the
  weight-zero (= algebraic) subgroup is exactly <kappa>.  Hence: the entire algebraic
  content the framework can hand to the SM through a finite multiplicative bridge is
  the single number kappa -- and kappa is FITTED.  A bridge in this class can transmit
  at most the knob, never derive it.
  Corollary 2b (PARITY).  The residue 2*w mod 2 is 1 (ODD) for Z and for
  a_0/(c H_Lam), and 0 (EVEN) for pi, for 1/(2 pi), for every algebraic number, and
  -- Check 10 -- for every sphere volume vol(S^{n-1}) and every even-dimensional loop
  measure (4 pi)^{-d/2}.  The framework's coefficient is the unique ODD-parity object
  in the whole discussion.  That single Z/2 grading is what all 18 routes were hitting.

DISCUSSION OF (H3) -- where the theorem is weakest.
  Flavour observables are MEASUREMENTS with error bars: rationals, not algebraic
  numbers in any intrinsic sense.  (H3) is the assertion a MODEL makes when it says
  "Koide Q = 2/3 exactly" or "the mixing parameter is sqrt(2)".  So Theorem 1 does not
  constrain nature; it constrains the class of exact-algebraic-flavour MODELS.  If the
  true flavour values are transcendental (Escape 2), the theorem says nothing.

THE FIVE ESCAPES (the constructive half -- what a bridge would have to look like)
--------------------------------------------------------------------------------
  E1  BREAKS (H2): a compensating half-weight transcendental on the SM side.
      Requires an object of pi-weight in 1/2 + Z.  Check 10 shows the usual suspects
      do NOT supply one: every vol(S^{n-1}) and every even-d loop measure is
      integer-weight, because Gamma(n/2) at half-integer argument returns exactly the
      compensating sqrt(pi).  Half-integer weight DOES arise from: a single un-squared
      Gaussian / Gamma(1/2); an ODD-dimensional measure (4 pi)^{-d/2}, d odd; a square
      root of a determinant; d = 3 thermal or odd-codimension constructions.  So E1 is
      a real door with a specific address: the SM side must route through an
      odd-dimensional or square-root-of-a-density object.  Note the framework's own
      sqrt(pi) has exactly that provenance (sqrt of a gravitational density).
  E2  BREAKS (H3): the flavour side is only APPROXIMATELY algebraic.  Koide's
      Q = 2/3 holds to O(1e-5), not exactly (Check 11).  Then the exact truth is
      transcendental and the residual carries the sqrt(pi).  Requirement: a bridge must
      PREDICT the residual, not just note that one exists.  Check 11 records the target
      delta = Q - 2/3 and the implied coefficient, so the escape is falsifiable.
  E3  BREAKS (H4): infinite processes.  Limits, infinite products, mode sums,
      functional determinants and zeta-regularised sums all convert algebraic input
      into pi (Check 9: Wallis).  This escape is WIDE OPEN and it is why the theorem
      must be phrased "no finite algebraic identity".  Requirement: an actual mode sum
      or determinant, not a numerology hit.
  E4  IDENTICAL CANCELLATION: relations in which sqrt(pi) cancels.  These exist and are
      exact (Check 12), but by Corollary 2a they are Z-free -- their algebraic content
      is kappa alone.  Requirement: nothing; that is the point.  This escape is
      provably EMPTY of new content, which is what "gauge-blind" should mean.
  E5  A SECOND TRANSCENDENTAL: work in Q_bar(s, T) with T algebraically independent of
      s (T = e, log 2, zeta(3), a Gamma-value...).  Then Theorem 1's injectivity
      argument runs again in the larger polynomial ring and the obstruction RETURNS
      unless T itself carries half-integer pi-weight -- i.e. E5 collapses into E1.
      Requirement: a T with w(T) in 1/2 + Z.  This is the sharpest statement available:
      the ONLY arithmetic route is a half-weight object.

HONEST TENSION (Theorem 3, and it does not favour the framework)
---------------------------------------------------------------
  The two natural coefficients in the a_0 box are arithmetically DISJOINT:
      framework:  a_0/(c H_Lam) = 2 kappa / Z,  weight -1/2  (ODD)   kappa = 1/2 fitted
      Milgrom  :  a_0/(c H_Lam) = 1/(2 pi),     weight -1    (EVEN)
  To land on Milgrom's 2 pi one needs kappa = Z/(4 pi) = sqrt(2/(3 pi)) = 0.4606589...,
  which by Theorem 2 is NOT algebraic.  So:
      * THEORY-natural (2 pi, the coefficient two independent Milgrom-side arguments
        prefer) requires a TRANSCENDENTAL kappa -- the framework then loses its
        "one rational knob" selling point entirely;
      * DATA-favoured kappa = 1/2 is rational (and the corpus's SPARC work favours it
        over 1/2pi by ~2.2 sigma -- QUOTED from project_kappa_discriminability, NOT
        re-derived here);
      * and no rational re-choice of kappa can bridge them, because the weights differ.
  The 8.2% gap between Z and 2 pi (Check 8 reproduces the corpus's 8.20% as the
  mean-relative gap, 8.190%) is therefore ARITHMETICALLY RIGID, not a rounding matter.
  Read against interest: the existence of a clean EVEN-weight competitor at 8% is the
  strongest number-theoretic argument that the framework's sqrt(pi) is an artefact of
  its own construction rather than a fingerprint of nature.

Every algebraic step below is checked with sympy; every "no relation exists" claim is
checked with PSLQ at 60 digits and shipped with a POSITIVE CONTROL that must find a
relation, so that a broken search cannot pass as a proof.

Exit 0 iff all checks hold.
"""

import sys
import sympy as sp
from mpmath import mp, mpf, pslq

mp.dps = 60

CHECKS = []


def check(name, ok, detail=""):
    CHECKS.append((name, bool(ok), detail))
    print(("[OK]   " if ok else "[FAIL] ") + name + (("  | " + detail) if detail else ""))
    return bool(ok)


def hdr(t):
    print()
    print("=" * 78)
    print(t)
    print("=" * 78)


# ----------------------------------------------------------------------------
# helper: pi-weight extractor.  Returns the unique rational k with expr/pi**k
# free of pi, or None if no such half-integer k in [-6, 6] exists.
# ----------------------------------------------------------------------------
PI = sp.pi


def pi_weight(expr):
    expr = sp.simplify(sp.sympify(expr))
    if expr == 0:
        return None
    found = []
    for two_k in range(-12, 13):
        k = sp.Rational(two_k, 2)
        q = sp.simplify(sp.powsimp(sp.expand(expr / PI ** k), force=True))
        q = sp.radsimp(sp.simplify(q))
        if not q.has(PI) and q != 0:
            found.append(k)
    if len(found) == 1:
        return found[0]
    return None


# ============================================================================
hdr("SECTION 0 -- the helper itself: positive and negative controls")
# ============================================================================
# If pi_weight is broken, every weight claim below is vacuous.  Control it.
check("pi_weight control: w(pi) = 1", pi_weight(PI) == 1, "got %s" % pi_weight(PI))
check("pi_weight control: w(7/3) = 0", pi_weight(sp.Rational(7, 3)) == 0)
check("pi_weight control: w(sqrt(pi)) = 1/2",
      pi_weight(sp.sqrt(PI)) == sp.Rational(1, 2))
check("pi_weight control: w(1/(4 pi)^(3/2)) = -3/2",
      pi_weight(1 / (4 * PI) ** sp.Rational(3, 2)) == sp.Rational(-3, 2))
# NEGATIVE control: a mixed-weight sum has NO well-defined weight.  If this
# returned a number the helper would be silently wrong.
check("pi_weight NEGATIVE control: w(1 + sqrt(pi)) undefined",
      pi_weight(1 + sp.sqrt(PI)) is None, "got %s" % pi_weight(1 + sp.sqrt(PI)))


# ============================================================================
hdr("SECTION 1 -- the framework constants, exactly")
# ============================================================================
Z = 2 * sp.sqrt(8 * PI / 3)
kappa = sp.Rational(1, 2)

check("Z^2 = 32 pi / 3 exactly", sp.simplify(Z ** 2 - 32 * PI / 3) == 0)

Z_num = mpf(2) * mp.sqrt(8 * mp.pi / 3)
check("Z = 5.78881003647 (10 dp)", abs(Z_num - mpf("5.7888100365")) < mpf("1e-9"),
      "Z = %s" % mp.nstr(Z_num, 14))
check("1/Z = 0.1727470747 (10 dp)",
      abs(1 / Z_num - mpf("0.1727470747")) < mpf("1e-10"),
      "1/Z = %s" % mp.nstr(1 / Z_num, 13))

# pi lives in Q(Z): this is the one-line reason Theorem 1 bites.
check("pi = 3 Z^2 / 32  ->  pi in Q(Z), so Z algebraic would force pi algebraic",
      sp.simplify(3 * Z ** 2 / 32 - PI) == 0)

# a_0 / (c H_Lambda) = 2 kappa / Z, derived symbolically from the definitions.
Lam, c, G, kap = sp.symbols("Lambda c G kappa", positive=True)
rho_Lam = Lam * c ** 2 / (8 * PI * G)
H_Lam = c * sp.sqrt(Lam / 3)
a0_sym = kap * c * sp.sqrt(G * rho_Lam)
ratio = sp.simplify(a0_sym / (c * H_Lam))
check("a_0/(c H_Lam) = kappa sqrt(3/(8 pi)) from rho_Lam, H_Lam definitions",
      sp.simplify(ratio - kap * sp.sqrt(3 / (8 * PI))) == 0,
      "sympy: %s" % sp.simplify(ratio))
check("kappa sqrt(3/(8 pi)) = 2 kappa / Z  (so a_0 = c H_Lam / Z at kappa = 1/2)",
      sp.simplify(kap * sp.sqrt(3 / (8 * PI)) - 2 * kap / Z) == 0)

# numeric footing, both ways as required
H0 = mpf("67.4") * 1000 / mpf("3.0856775814913673e22")   # Planck-ish, s^-1
Om_Lam = mpf("0.685")
cc = mpf("2.99792458e8")
a0_can = cc * H0 * mp.sqrt(Om_Lam) / Z_num
a0_alt = cc * H0 / Z_num
check("canonical a_0 = 9.36e-11 m/s^2 (within 1%)",
      abs(a0_can - mpf("9.3614e-11")) / mpf("9.3614e-11") < mpf("0.01"),
      "a_0 = %s" % mp.nstr(a0_can, 6))
check("ALT/canonical footing ratio = 1/sqrt(Om_Lam) = 1.2082",
      abs(a0_alt / a0_can - 1 / mp.sqrt(Om_Lam)) < mpf("1e-12")
      and abs(1 / mp.sqrt(Om_Lam) - mpf("1.2082")) < mpf("5e-5"),
      "ALT a_0 = %s ; ratio = %s" % (mp.nstr(a0_alt, 6), mp.nstr(a0_alt / a0_can, 6)))


# ============================================================================
hdr("SECTION 2 -- THEOREM 1: every framework constant lies in Q_bar(s), s=sqrt(pi)")
# ============================================================================
s = sp.symbols("s", positive=True)
subs_s = {s: sp.sqrt(PI)}

check("pi = s^2 with s = sqrt(pi)",
      sp.simplify((s ** 2).subs(subs_s) - PI) == 0)
check("Z = 2 sqrt(8/3) * s   (algebraic coefficient times s)",
      sp.simplify((2 * sp.sqrt(sp.Rational(8, 3)) * s).subs(subs_s) - Z) == 0)
check("a_0/(c H_Lam) = kappa sqrt(3/8) / s   (algebraic coefficient over s)",
      sp.simplify((kap * sp.sqrt(sp.Rational(3, 8)) / s).subs(subs_s)
                  - kap * sp.sqrt(3 / (8 * PI))) == 0)

# The injectivity core of Theorem 1, tested numerically with PSLQ.
#
# PRECISION HAZARD, and it BIT on the first run of this script.  A vector of n
# terms admits SPURIOUS integer relations of height <= H with residual as small as
# ~H^(-(n-1)) by pigeonhole.  For n = 7, H = 1e8 that floor is ~1e-48, BELOW a
# tol of 1e-45 -- so PSLQ dutifully returned a meaningless 8-digit relation and a
# "no relation exists" check would have FAILED for purely numerical reasons.
# A 'no relation' claim is only meaningful when  tol << H^(-(n-1)).
# Below: (a) the hazard is exhibited and the spurious relation is refuted at 400
# digits, (b) the real searches are run in the safe regime.
DPS_HI = 400
TOL_HI = mpf(10) ** -260          # H^(-(n-1)) = 1e-72 at H=1e12, n=7  >>  1e-260
MAXC = 10 ** 12


def sqrt_pi_powers(k, extra=()):
    sv = mp.sqrt(mp.pi)
    return list(extra) + [sv ** j for j in range(0, k + 1)]


# (a) exhibit the hazard.
with mp.workdps(60):
    vec_loose = [mpf(1)] + [mp.sqrt(mp.pi) ** j for j in range(1, 7)]
    rel_loose = pslq(vec_loose, tol=mpf(10) ** -45, maxcoeff=10 ** 8, maxsteps=40000)
resid_loose = None
if rel_loose is not None:
    with mp.workdps(DPS_HI):
        sv_hi = mp.sqrt(mp.pi)
        resid_loose = abs(sum(mpf(int(rel_loose[j])) * sv_hi ** j
                              for j in range(len(rel_loose))))
check("PRECISION HAZARD exhibited: at tol=1e-45 with maxcoeff=1e8 (n=7) PSLQ returns "
      "a SPURIOUS relation, refuted at 400 digits (residual ~1e-46, nowhere near 0)",
      rel_loose is not None and resid_loose is not None
      and resid_loose > mpf(10) ** -100,
      "spurious %s ; |residual| = %s" % (rel_loose, mp.nstr(resid_loose, 4)))

# (b) the real search, in the safe regime.
with mp.workdps(DPS_HI):
    rel_s = pslq(sqrt_pi_powers(6), tol=TOL_HI, maxcoeff=MAXC, maxsteps=200000)
check("PSLQ finds NO integer relation among 1, s, ..., s^6  (s = sqrt(pi)) in the "
      "SAFE regime tol=1e-260 << 1e-72 = spurious floor",
      rel_s is None, "pslq -> %s" % (rel_s,))

# POSITIVE CONTROL for the search itself, same settings: golden ratio must be caught.
with mp.workdps(DPS_HI):
    phi = (1 + mp.sqrt(5)) / 2
    rel_ctl = pslq([mpf(1), phi, phi ** 2], tol=TOL_HI, maxcoeff=MAXC, maxsteps=200000)
check("PSLQ positive control (same tol/maxcoeff): finds phi^2 = phi + 1, so a null "
      "result above is a real null and not a dead search",
      rel_ctl is not None and [int(x) for x in rel_ctl] in ([1, 1, -1], [-1, -1, 1]),
      "pslq -> %s" % (rel_ctl,))

# THEOREM 1 IN ACTION.  Mix algebraic flavour-style data (2/3 Koide, sqrt(2) the
# free Koide parameter r) with powers of s.  A relation DOES exist -- and the
# theorem predicts every coefficient on a power of s, and on the irrational
# algebraic entry, must vanish: the surviving relation is the degenerate,
# framework-free one 3*(2/3) - 2*1 = 0.
with mp.workdps(DPS_HI):
    vec_mix = [mpf(2) / 3, mp.sqrt(2)] + [mp.sqrt(mp.pi) ** j for j in range(0, 4)]
    #          idx 0        idx 1         idx 2 = s^0 = 1, idx 3..5 = s, s^2, s^3
    rel_mix = pslq(vec_mix, tol=TOL_HI, maxcoeff=MAXC, maxsteps=200000)
ok_mix = (rel_mix is not None
          and int(rel_mix[1]) == 0                      # sqrt2 coefficient
          and all(int(rel_mix[i]) == 0 for i in (3, 4, 5)))   # s, s^2, s^3
check("THEOREM 1 in action: the only PSLQ relation among {2/3, sqrt2, 1, s, s^2, s^3} "
      "is Z-FREE -- every sqrt(pi) coefficient and the sqrt2 coefficient vanish, "
      "leaving the degenerate 3*(2/3) - 2*1 = 0",
      ok_mix, "pslq -> %s" % (rel_mix,))

# and a vector with NO rational dependence among its algebraic entries: nothing.
with mp.workdps(DPS_HI):
    rel_none = pslq(sqrt_pi_powers(4, extra=(mp.sqrt(2),)),
                    tol=TOL_HI, maxcoeff=MAXC, maxsteps=200000)
check("PSLQ finds NO relation among {sqrt2, 1, s, s^2, s^3, s^4}",
      rel_none is None, "pslq -> %s" % (rel_none,))


# ============================================================================
hdr("SECTION 3 -- THEOREM 2: pi-weight, and the one-rational-number channel")
# ============================================================================
tbl = [
    ("pi", PI, sp.Integer(1)),
    ("Z = 2 sqrt(8 pi/3)", Z, sp.Rational(1, 2)),
    ("1/Z", 1 / Z, sp.Rational(-1, 2)),
    ("a_0/(c H_Lam) = 2 kappa/Z, kappa=1/2", 2 * kappa / Z, sp.Rational(-1, 2)),
    ("Milgrom 1/(2 pi)", 1 / (2 * PI), sp.Integer(-1)),
    ("kappa = 1/2 (algebraic knob)", kappa, sp.Integer(0)),
    ("8 pi / 3", 8 * PI / 3, sp.Integer(1)),
]
allw = True
for nm, e, want in tbl:
    got = pi_weight(e)
    ok = (got == want)
    allw &= ok
    print("       w(%-38s) = %-6s  expect %-6s  parity %s"
          % (nm, got, want, "ODD" if (got is not None and (2 * got) % 2 == 1) else "EVEN"))
check("pi-weights of the whole a_0 box are as claimed (Z: +1/2, coefficient: -1/2, "
      "Milgrom: -1, algebraic: 0)", allw)

check("PARITY: framework coefficient is ODD, Milgrom's and every algebraic number "
      "are EVEN",
      (2 * pi_weight(2 * kappa / Z)) % 2 == 1
      and (2 * pi_weight(1 / (2 * PI))) % 2 == 0
      and (2 * pi_weight(kappa)) % 2 == 0)

# Corollary 2a: weight-zero subgroup of <Z, kappa> is exactly <kappa>.
bad = []
for m in range(-6, 7):
    for n in range(-6, 7):
        w = sp.Rational(m, 2)                 # w(Z^m kappa^n) = m/2, kappa algebraic
        expr_w = pi_weight(Z ** m * kappa ** n) if abs(m) <= 3 and abs(n) <= 2 else w
        if expr_w != w:
            bad.append((m, n, expr_w, w))
        if (w == 0) != (m == 0):
            bad.append((m, n, "grading", w))
check("COROLLARY 2a: w(Z^m kappa^n) = m/2 (spot-verified symbolically) and vanishes "
      "iff m = 0  ==>  weight-zero subgroup of <Z,kappa> is exactly <kappa>",
      not bad, "violations: %s" % (bad[:3],))
print("       CONSEQUENCE: the only algebraic number a finite multiplicative bridge")
print("       can ever transmit from this framework to the SM is kappa itself -- and")
print("       kappa = 1/2 is FITTED, NOT DERIVED.  A bridge in this class cannot")
print("       derive the knob; at best it relabels it.")


# ============================================================================
hdr("SECTION 4 -- THEOREM 3: the two natural coefficients are arithmetically disjoint")
# ============================================================================
kappa_M = Z / (4 * PI)
check("kappa needed for Milgrom's a_0 = c H_Lam/(2 pi) is Z/(4 pi) = sqrt(2/(3 pi))",
      sp.simplify(kappa_M - sp.sqrt(2 / (3 * PI))) == 0)
check("w(kappa_Milgrom) = -1/2  ==>  kappa_M is NOT algebraic (Theorem 2), so the "
      "2 pi form requires a TRANSCENDENTAL knob",
      pi_weight(kappa_M) == sp.Rational(-1, 2),
      "kappa_M = %s" % mp.nstr(Z_num / (4 * mp.pi), 12))

gap_mean = 100 * (2 * mp.pi - Z_num) / ((2 * mp.pi + Z_num) / 2)
gap_ratio = 2 * mp.pi / Z_num
check("gap Z vs 2 pi reproduces the corpus's 8.20% (mean-relative) to 0.05 pts",
      abs(gap_mean - mpf("8.20")) < mpf("0.05"),
      "mean-relative gap = %s%% ; a_0 ratio 2pi/Z = %s (i.e. +8.54%% in a_0)"
      % (mp.nstr(gap_mean, 5), mp.nstr(gap_ratio, 7)))
check("the two coefficients sit in DIFFERENT weight classes (-1/2 vs -1), so their "
      "ratio is not algebraic and no rational kappa closes the gap",
      pi_weight(2 * kappa / Z) != pi_weight(1 / (2 * PI))
      and pi_weight(sp.simplify((2 * kappa / Z) / (1 / (2 * PI)))) != 0)
print("       TENSION, on the record and against interest: THEORY favours 2 pi (EVEN,")
print("       Milgrom's own coefficient) while DATA favours kappa = 1/2 (~2.2 sigma,")
print("       QUOTED from project_kappa_discriminability, not re-derived here).  If the")
print("       2 pi reading is right, the framework's knob is transcendental and the")
print("       'one rational parameter' economy claim is lost.")


# ============================================================================
hdr("SECTION 5 -- ESCAPE E1/E5: where a half-integer weight could come from")
# ============================================================================
# Claim: the standard geometric / 4d-perturbative factory produces INTEGER weight
# only.  If any of these came out half-integer, E1 would be cheap and the
# obstruction weak -- so this check can genuinely fail.
rows = []
integer_ok = True
for n in range(1, 13):
    vol = sp.simplify(2 * PI ** sp.Rational(n, 2) / sp.gamma(sp.Rational(n, 2)))
    w = pi_weight(vol)
    isint = (w is not None and sp.Rational(w).q == 1)
    integer_ok &= isint
    rows.append(("vol(S^%d) = %s" % (n - 1, vol), w, isint))
for d in (2, 4, 6, 8):
    e = 1 / (4 * PI) ** sp.Rational(d, 2)
    w = pi_weight(e)
    isint = (w is not None and sp.Rational(w).q == 1)
    integer_ok &= isint
    rows.append(("even-d loop measure (4pi)^(-d/2), d=%d" % d, w, isint))
for nm, w, isint in rows:
    print("       %-42s  w = %-6s  %s" % (nm, w, "integer" if isint else "HALF"))
check("E1 mapped: every vol(S^(n-1)) (n<=12) and every EVEN-d loop measure has "
      "INTEGER pi-weight -- Gamma(n/2) supplies the compensating sqrt(pi)",
      integer_ok)

half_rows = []
half_ok = True
for nm, e in [("Gamma(1/2) = sqrt(pi)", sp.gamma(sp.Rational(1, 2))),
              ("odd-d measure (4pi)^(-3/2)", 1 / (4 * PI) ** sp.Rational(3, 2)),
              ("odd-d measure (4pi)^(-5/2)", 1 / (4 * PI) ** sp.Rational(5, 2)),
              ("single Gaussian int_R exp(-x^2)", sp.sqrt(PI))]:
    w = pi_weight(e)
    ishalf = (w is not None and sp.Rational(w).q == 2)
    half_ok &= ishalf
    half_rows.append((nm, w, ishalf))
    print("       %-42s  w = %-6s  %s" % (nm, w, "HALF <- door" if ishalf else "integer"))
check("E1's address is specific: half-integer weight comes from an un-squared "
      "Gamma(1/2) / single Gaussian / ODD-dimensional measure -- and from nothing "
      "else in this list", half_ok)
print("       So E5 (a second transcendental T) collapses into E1: Theorem 1's")
print("       injectivity re-runs in Q_bar(s,T) unless w(T) is in 1/2 + Z.")


# ============================================================================
hdr("SECTION 6 -- ESCAPE E3: infinite processes DEFEAT the theorem (scope correction)")
# ============================================================================
# Wallis: a sequence of RATIONALS converging to pi/2.  This is why the theorem is
# "no finite algebraic identity", not "no derivation".
W = sp.Integer(1)
errs = []
for k in range(1, 2001):
    W *= sp.Rational(4 * k * k, 4 * k * k - 1)
    if k in (10, 100, 1000, 2000):
        errs.append((k, W, float(abs(W - sp.pi / 2))))
all_rational = all(isinstance(w, sp.Rational) for _, w, _ in errs)
monotone = all(errs[i][2] > errs[i + 1][2] for i in range(len(errs) - 1))
check("E3 is REAL: Wallis partial products are exactly RATIONAL at every order",
      all_rational, "e.g. N=10 -> %s" % errs[0][1])
check("E3 is REAL: those rationals converge to pi/2, error strictly decreasing, "
      "|W_2000 - pi/2| < 1e-3",
      monotone and errs[-1][2] < 1e-3,
      "errors: " + ", ".join("N=%d:%.2e" % (k, e) for k, _, e in errs))
check("E3 is REAL: no partial product EQUALS pi/2 (rational vs transcendental)",
      all(sp.simplify(w - sp.pi / 2) != 0 for _, w, _ in errs))
print("       ==> a mode sum, infinite product or functional determinant CAN produce")
print("       pi, and with an odd-dimensional measure a HALF power of it, out of")
print("       algebraic input.  The corpus phrase 'structurally gauge-blind' must be")
print("       read as 'no finite algebraic identity', not 'no derivation'.")


# ============================================================================
hdr("SECTION 7 -- ESCAPE E2: the Koide residual, made into a falsifiable target")
# ============================================================================
# PDG-2024 charged-lepton masses, MeV.
m_e, m_mu, m_tau = mpf("0.51099895000"), mpf("105.6583755"), mpf("1776.86")
Qk = (m_e + m_mu + m_tau) / (mp.sqrt(m_e) + mp.sqrt(m_mu) + mp.sqrt(m_tau)) ** 2
delta = Qk - mpf(2) / 3
check("Koide Q reproduced from PDG masses, Q ~ 2/3 but NOT exactly 2/3",
      abs(delta) > 0 and abs(delta) < mpf("1e-4"),
      "Q = %s ; delta = Q - 2/3 = %s" % (mp.nstr(Qk, 12), mp.nstr(delta, 4)))
# If a framework correction of weight -1/2 carried the residual, its algebraic
# coefficient c would satisfy delta = c / Z.  Record the target.
c_needed = delta * Z_num
check("E2 target recorded: a weight(-1/2) correction delta = c/Z needs an algebraic "
      "coefficient c of size < 1e-3 (i.e. NOT O(1)) -- the escape must PREDICT this "
      "number, not merely allow it",
      abs(c_needed) < mpf("1e-3"),
      "c = delta * Z = %s" % mp.nstr(c_needed, 4))
print("       Honest reading: the residual is far too small to be an O(1) sqrt(pi)")
print("       effect, so E2 is open but requires a tuned, PREDICTED coefficient.")
print("       tau mass dominates the uncertainty; do not over-read the digits.")


# ============================================================================
hdr("SECTION 8 -- ESCAPE E4: exact identities exist, and they are provably empty")
# ============================================================================
check("E4: an exact algebraic identity in the box does exist -- 3 Z^2/(32 pi) = 1",
      sp.simplify(3 * Z ** 2 / (32 * PI) - 1) == 0)
check("E4: and (a_0/(c H_Lam)) * Z / 2 = kappa = 1/2 exactly -- Z cancels, the "
      "surviving content is the FITTED knob and nothing else",
      sp.simplify((2 * kappa / Z) * Z / 2 - sp.Rational(1, 2)) == 0)
check("E4 is empty by Theorem 1's corollary: both identities are independent of the "
      "value of pi (they hold with pi -> any symbol)",
      sp.simplify((3 * (2 * sp.sqrt(8 * s ** 2 / 3)) ** 2 / (32 * s ** 2)) - 1) == 0)
print("       This is the precise, proved meaning of 'gauge-blind': exact bridges are")
print("       available, but every one of them is Z-free after cancellation.")


# ============================================================================
hdr("SECTION 9 -- what this does NOT prove (guard against over-reading)")
# ============================================================================
print("""  1. NOT a derivation of Z, Lambda, a_0 or kappa.  kappa = 1/2 stays FITTED.
  2. NOT a statement about nature.  (H3) is an assumption about MODELS that assert
     exact algebraic flavour values.  If flavour values are transcendental, silence.
  3. NOT applicable to a_0 versus a mass: a_0 carries the measured Lambda, an
     empirical real of unknown arithmetic type.  Only the DIMENSIONLESS coefficient
     is constrained.
  4. NOT a ban on derivations: Escape E3 (limits / mode sums / determinants) is wide
     open and demonstrated real in Section 6.
  5. NOT independent evidence for the framework.  Symmetrically, it means flavour
     data can never REFUTE the framework either -- the SM front is not a test.
  6. The 2.2 sigma kappa=1/2-over-1/2pi preference is QUOTED from the corpus, not
     re-derived here; the arithmetic disjointness in Section 4 is what is new.""")


# ============================================================================
hdr("RESULT")
# ============================================================================
n_ok = sum(1 for _, ok, _ in CHECKS if ok)
n_all = len(CHECKS)
for nm, ok, d in CHECKS:
    if not ok:
        print("FAILED: %s  | %s" % (nm, d))
print()
print("HEADLINE: the number-field obstruction is now a THEOREM for finite "
      "Q_bar-rational relations --")
print("  every exact algebraic bridge between the framework's dimensionless "
      "coefficient and")
print("  algebraic flavour data is forced to be Z-FREE (a relabelling), because "
      "sqrt(pi) gives")
print("  the coefficient HALF-INTEGER pi-weight while every SM-side object it could "
      "meet has")
print("  INTEGER weight.  The only arithmetic door left is a half-weight object "
      "(un-squared")
print("  Gamma(1/2) / odd-dimensional measure / sqrt of a determinant), or an "
      "infinite process.")
print()
print("%d/%d checks held." % (n_ok, n_all))
sys.exit(0 if n_ok == n_all else 1)
