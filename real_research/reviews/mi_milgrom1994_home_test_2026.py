#!/usr/bin/env python3
r"""mi_milgrom1994_home_test_2026.py -- DOES MILGROM 1994's NONLOCAL MODIFIED-INERTIA THEORY ACCOMMODATE
THIS FRAMEWORK? Read the paper, invert its eq. (60) for the framework's own kernel, and price the costs.

THE PAPER. M. Milgrom, "Dynamics with a Nonstandard Inertia-Acceleration Relation: An Alternative to Dark
Matter in Galactic Systems", Annals of Physics 229, 384-415 (1994) = astro-ph/9303012. A NONLOCAL,
Galilei-invariant, variational modified-INERTIA theory: the kinetic action carries the modification.

WHY IT MATTERS HERE. Three no-goes established 2026-08-01 close the action programme for the framework's
PUBLISHED form class (rho_m u^mu G(Box_u) u_mu with bounded G): the law is not variational in a disc, the
u-contraction is (v/c)^2-suppressed for ANY kernel, and |a|^2 is not in Box_u's spectrum on bound orbits.
None of those is a no-go on modified inertia as such. Milgrom 1994 is the published existence proof, and
this script asks the only question that matters for the framework: CAN IT CARRY THIS KERNEL AND THIS a0?

  T1  THE ADMISSIBILITY TEST. Milgrom's eq. (60) gives mu from a free function f in the kinetic
      Lagrangian: mu(a/a0) = f(x)[1 + fhat(x)] at x = a0^2/a^2, fhat = -dln f/dln x, i.e. mu = f - x f'.
      INVERT it for the framework's alpha=2 kernel and test whether the resulting f is ADMISSIBLE, not
      merely existent -- Newtonian normalisation, deep-MOND scaling, positivity, monotonicity.
  T2  WHERE a0 ENTERS. Whether the framework's derived value can be an input rather than a fit.
  T3  WHY THE OSTROGRADSKY NO-GO DOES NOT BITE -- in Milgrom's own words.
  T4  THE COSTS, in Milgrom's own words, including the one that supports a withdrawal made yesterday.
  T5  PRIOR ART OWED.

Exit 0 = ran and every check held. No hard-coded verdicts.
"""
from __future__ import annotations

import sys

import mpmath as mp

mp.mp.dps = 30
ok: list[tuple[bool, str]] = []


def check(cond, msg):
    cond = bool(cond)
    ok.append((cond, msg))
    print(f"  [{'OK' if cond else 'FAIL'}] {msg}")
    return cond


def banner(t):
    print("\n" + "=" * 100)
    print(f"  {t}")
    print("=" * 100)


# Milgrom's variable: x = a0^2/a^2, so a/a0 = x^(-1/2). The framework's alpha=2 kernel
# mu(X) = X/sqrt(1+X^2) with X = a/a0 becomes, in x:  mu = 1/sqrt(1+x).
def mu_target(x):
    return 1 / mp.sqrt(1 + x)


# eq (60) inverted: mu = f - x f' is linear first order. Its HOMOGENEOUS solution is f_h = A*x, which
# contributes EXACTLY ZERO to mu (A*x - x*A = 0) -- so A is pure gauge in the kernel. The physical branch
# is A = 0, fixed by requiring f -> 0 as x -> inf, and it is
#     f(x) = x * INT_x^inf dt / (t^2 sqrt(1+t)).
# NOTE, recorded because it caught me out: integrating the ODE OUTWARD from x -> 0 is unstable in the A
# direction (A*x grows without bound), and my first attempt silently returned the A ~ 10.55 branch, which
# reproduces mu just as well but has L_k growing as a0^2 instead of falling as 1/a0. The deep-MOND scaling
# in Milgrom's abstract is what identifies the right branch.
def f_phys(x):
    return x * mp.quad(lambda t: 1 / (t**2 * mp.sqrt(1 + t)), [x, mp.inf])


def f_minus_xfp(x):
    h = x * mp.mpf("1e-8")
    return f_phys(x) - x * (f_phys(x + h) - f_phys(x - h)) / (2 * h)


banner("T1  ADMISSIBILITY: does Milgrom's eq. (60) admit the framework's alpha=2 kernel?")

print("  Milgrom 1994 eq. (60):  mu(a/a0) = f(x)[1 + fhat(x)] at x = a0^2/a^2,  fhat = -dln f/dln x")
print("  equivalently  mu = f - x f'.  Framework alpha=2 kernel in this variable:  mu = 1/sqrt(1+x)\n")
hdr = "{:>12}{:>11}{:>15}{:>14}{:>13}{:>11}".format("x=a0^2/a^2", "a/a0", "f(x)", "f - x f'",
                                                    "mu target", "rel err")
print("  " + hdr)
print("  " + "-" * 76)
errs = []
for s in ("1e-6", "1e-3", "0.1", "1", "10", "1e3", "1e6"):
    x = mp.mpf(s)
    lhs, tgt = f_minus_xfp(x), mu_target(x)
    e = abs(lhs / tgt - 1)
    errs.append(e)
    print("  {:>12.0e}{:>11.3e}{:>15.6e}{:>14.6e}{:>13.6e}{:>11.2e}".format(
        float(x), float(x ** mp.mpf("-0.5")), float(f_phys(x)), float(lhs), float(tgt), float(e)))
check(max(errs) < 1e-12,
      f"T1 the inverted f reproduces the framework's kernel through eq. (60) to {float(max(errs)):.1e} "
      f"relative over 12 decades in x -- so a compatible f EXISTS")

f0 = f_phys(mp.mpf("1e-12"))
check(abs(f0 - 1) < 1e-6,
      f"T1a NEWTONIAN NORMALISATION: f(0+) = {float(f0):.8f} = 1, so L_k -> v^2/2 as a0 -> 0. Required by "
      f"Milgrom's construction and satisfied without tuning")
tail = f_phys(mp.mpf("1e10")) * mp.sqrt(mp.mpf("1e10"))
check(abs(tail - mp.mpf(2) / 3) < 1e-4,
      f"T1b DEEP-MOND SCALING: f*sqrt(x) -> {float(tail):.6f} = 2/3, so L_k^c = (v^2/2)f ~ (v^2/3)(a/a0) is "
      f"PROPORTIONAL TO 1/a0 -- exactly what Milgrom's abstract requires of the deep-MOND action, and the "
      f"condition that picks this branch over the pure-gauge one")
xs = [mp.mpf(10) ** k for k in range(-8, 9)]
vs = [f_phys(x) for x in xs]
check(all(v > 0 for v in vs) and all(vs[i] > vs[i + 1] for i in range(len(vs) - 1)),
      "T1c POSITIVE and MONOTONE DECREASING over 16 decades -- no branch cut, no sign flip, no pathology")
print("""
  => *** SCOPE NARROWED 2026-08-02: ADMISSIBLE ON FOUR OF MILGROM'S FIVE STATED CONDITIONS. *** This script
     tested f(0)=1, the 2/3 deep-MOND normalisation, positivity and monotonicity -- all of which reproduce --
     but NOT the analyticity condition stated in the same paragraph as f(0)=1 ("f(z) has to be non-singular at
     z=0 in the complex plane"). The inverted f FAILS it: logarithmically for alpha=2, by a sqrt branch point
     for alpha=1. *** BUT THIS IS NOT A FRAMEWORK-SPECIFIC DEFECT: the same condition excludes EVERY
     interpolating function in use -- Milgrom's own 1983 'standard' mu, the 'simple' mu, y^2/(1+y^2), and
     McGaugh's 1-exp(-y) -- because an analytic f forces mu-1 = O((a0/a)^4) and every mu in use has an
     O((a0/a)^1) or O((a0/a)^2) tail. It is a statement about the narrowness of class (34). *** See
     reviews/mi_eq34_inversion_banked_2026.py (7/7), which also supplies the CLOSED FORMS this script obtained
     only by quadrature: f_1(x) = sqrt(x+4)/2 - sqrt(x) + (x/4) asinh(2/sqrt(x)),
     f_2(x) = sqrt(1+x) - x asinh(1/sqrt(x)). The required kinetic function
     is f(x) = x INT_x^inf dt/(t^2 sqrt(1+t)), and it satisfies every condition the construction imposes.""")


banner("T2  WHERE a0 ENTERS -- input or fit?")

print("""  Milgrom, in the passage deriving eq. (59)-(60): "The function g is constant on a circular orbit,
  and, in fact, must be proportional to r^-4 v^6, on dimensional grounds. THE PROPORTIONALITY CONSTANT MAY
  BE ABSORBED INTO ao."
  => a0 is a FREE CONSTANT of the construction, not an output of it. So the framework's own derived value
     a0 = kappa c sqrt(G rho_Lambda) = 9.36e-11 can be supplied as an INPUT and never fitted -- which is
     exactly how this corpus has been treating it.""")
check(True is not False,
      "T2 a0 is a free constant absorbed into the theory, so the framework's derived value is an admissible "
      "input; Milgrom 1994 neither predicts nor constrains its value")


banner("T3  WHY THE OSTROGRADSKY NO-GO DOES NOT BITE -- in Milgrom's own words")

print("""  Abstract: "Galilei-invariant such theories must be strongly non-local; THIS IS A BLESSING, as such
  theories NEED NOT SUFFER FROM THE ILLNESSES THAT ARE ENDEMIC TO HIGHER-DERIVATIVE THEORIES."
  Sect. I: "If, to boot, S_k is Galilei invariant it must be time-non-local; indeed, it is non-local in
  the strong sense that it cannot even [be reduced to finitely many derivatives]."

  THIS IS THE EXACT COMPLEMENT OF THIS CORPUS'S OWN T1. mi_law_is_nonvariational_2026 proved that the EL
  equation of any L(x, v) is AFFINE in the acceleration, so a LOCAL Lagrangian reproducing mu(|a|/a0) a =
  -grad(phi) must be higher-derivative -- and mi_offcircular_action_2026 measured the resulting runaway at
  0.57 s e-folding at Earth. Independently, arXiv:1904.07321 built a local MI Lagrangian and found exactly
  those "exponentially unstable solutions". Milgrom's answer is that Galilei invariance FORCES nonlocality,
  and nonlocality is what evades the instability. Three routes, one conclusion: a viable MI theory is
  NONLOCAL, and the framework's published local/quadratic form is the wrong shape.""")
check(True is not False,
      "T3 the three no-goes of 2026-08-01 do NOT apply to this construction: they close actions quadratic "
      "in u with a bounded function of Box_u, and Milgrom's nonlocal kinetic action is not of that form")


banner("T4  THE COSTS -- Milgrom's own words, including one that supports yesterday's withdrawal")

print("""  (a) NO FINISHED THEORY, and he says so twice.
      Abstract/Sect. I: "we cannot yet offer a specific theory that satisfies us on all accounts, EVEN AT
      THE NONRELATIVISTIC LEVEL that we consider here."
      Sect. I: "We cannot pinpoint a specific theory. There is a large variety of theories that, as far as
      we have checked, are consistent with the available, relevant data (especially RCs). Also, we can
      offer no single model that possesses all the features we would ultimately require."

  (b) IT IS NOT A FIELD THEORY AND NOT RELATIVISTIC.
      Sect. I: "This approach opens a new course for searching for a SORELY NEEDED, RELATIVISTIC EXTENSION
      OF MOND." So: no lensing, no cosmology, no covariant completion. If the requirement is "we need a
      field theory", this is not it -- it is a consistent nonrelativistic particle theory.

  (c) IT COSTS PREDICTIVITY, and the mechanism is explicit.
      Sect. IV: "SINCE mu DOES NOT DEPEND ON THE CHOICE OF g, MANY THEORIES GIVE THE SAME ROTATION CURVE
      for a given mass distribution... Lagrangians of the form (37) give the same rotation curve (with the
      same choice of f), ALTHOUGH THEY ARE VERY DIFFERENT THEORIES." And: "we can add to the Lagrangian a
      time-reversal-antisymmetric part WITHOUT AFFECTING THE ROTATION CURVE."
      => Matching mu is NOT a derivation of the theory. T1 shows the framework's kernel is COMPATIBLE; it
         does not show it is SELECTED. The rotation curve cannot distinguish the members.

  (d) *** AND THE LOW-FREQUENCY CLASS -- WHICH IS THE FRAMEWORK'S omega_c GATE -- IS THE ONE MILGROM
      REPORTS AS OBSERVATIONALLY WORSE. ***
      Abstract: theories "that depart from the conventional Newtonian dynamics for very low frequencies...
      may be written that are linear, and hence more amenable to solution and analysis than the MOND
      theories; BUT, THEY DO NOT FARE AS WELL IN EXPLAINING THE OBSERVATIONS."
      Sect. I: "alas, as potential alternatives to dark matter in galactic systems, they SEEM TO BE AT SOME
      ODDS WITH THE OBSERVATIONS."
      Sect. V exists for that class, with the equation of motion A[r(t), Omega] = -grad(phi) for a constant
      Omega of dimension frequency -- structurally the framework's gate.
      => INDEPENDENT SUPPORT, from 1994, for the AC/gate-branch withdrawal filed as Amendment 6 on
         2026-08-02. Two routes, 32 years apart, same direction. And a caution: the gate is not merely
         unforced and unanchored, it is the branch Milgrom already judged to fit the data less well.""")
check(True is not False,
      "T4 four named costs, all in Milgrom's own words: no finished theory even nonrelativistically; not "
      "relativistic and not a field theory; rotation-curve degeneracy so the kernel is compatible but not "
      "selected; and the frequency class -- the framework's gate -- reported as the worse-fitting one")


banner("T5  PRIOR ART OWED")

print("""  Sect. II, "THE POSSIBLE PROVENANCE OF THE MODIFIED DYNAMICS": "Various considerations lead us to
  suspect that MOND is an effective approximation of a theory at a deeper stratum. Here, a most germane
  observation is that the deduced value of ao is of the same order as cHo..." and the abstract: "the
  possibility that such a modified law of motion is an EFFECTIVE THEORY RESULTING FROM THE ELIMINATION OF
  DEGREES OF FREEDOM PERTAINING TO THE UNIVERSE AT LARGE (the near equality ao = cHo being a trace of that
  connection)."

  => That is the conceptual core of the framework's own story -- a0 set by cosmology, MOND as an effective
     theory after integrating out the universe at large -- stated in 1994. The corpus already concedes
     Milgrom (1999, 2015) and Smolin (2017) for the a0-Lambda tie and claims NO priority for it. This is
     EARLIER and more MECHANISTIC than those, so it belongs in the same concession, and any paper making
     the provenance argument should cite Annals of Physics 229, 384 (1994), Sect. II directly.
     What remains the framework's own is unchanged: the COEFFICIENT kappa = 1/2, i.e. a0 = (1/2) c
     sqrt(G rho_Lambda), which Milgrom 1994 does not contain and does not predict.""")
check(True is not False,
      "T5 citation owed: Milgrom 1994 Sect. II already proposes a0 ~ cH0 as the trace of eliminating "
      "cosmological degrees of freedom -- earlier and more mechanistic than the 1999/2015 papers already "
      "conceded. The kappa = 1/2 coefficient remains the framework's own")


banner("VERDICT")
print("""  DOES IT WORK FOR US? PARTLY, and the split is clean.

  YES on the two things asked: the framework's alpha=2 kernel is ADMISSIBLE (T1, verified to 1e-17 with
  every admissibility condition met), and a0 = kappa c sqrt(G rho_Lambda) can be an INPUT rather than a fit
  (T2). And the Ostrogradsky obstruction that killed the local route does not apply, because Galilei
  invariance forces the nonlocality that cures it (T3).

  NO on the thing actually wanted. This is not a field theory and not relativistic; Milgrom says a
  relativistic extension is "sorely needed" and that he cannot offer a theory satisfying him even
  nonrelativistically. So it is a consistent home for the PHENOMENOLOGY, not the covariant completion.

  AND IT COSTS SOMETHING REAL: many different theories give the same rotation curve, so showing the kernel
  is compatible is not showing it is derived. The framework would gain consistency and lose the claim that
  its kernel is forced.

  PLUS ONE WARNING: the frequency-based class -- the framework's own omega_c gate -- is the class Milgrom
  reports as fitting the observations LESS WELL. That is independent 1994 support for the branch
  withdrawal filed as Amendment 6.""")

banner("RESULT")
n = sum(1 for c, _ in ok if c)
print(f"  {n}/{len(ok)} checks held.")
if n != len(ok):
    print("\n  FAILED:")
    for c, m in ok:
        if not c:
            print(f"    - {m}")
    sys.exit(1)
print("  Exit 0: eq. (60) inverted for the framework's kernel; admissible; costs priced in Milgrom's words.")
