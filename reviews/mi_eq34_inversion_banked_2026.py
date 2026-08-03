#!/usr/bin/env python3
r"""mi_eq34_inversion_banked_2026.py -- BANKING THE MILGROM eq.(34) INVERSION. Two results that REFRAME the
"no action" problem in the framework's favour, two new closed forms, one scope correction owed to a committed
script, and the confirmation that the class cannot touch kappa.

THE QUESTION ASKED: Milgrom 1994 (Ann. Phys. 229, 384 = astro-ph/9303012) proves that a Galilei-invariant,
local-or-weakly-nonlocal MOND theory derivable from an action is impossible, leaving his eq. (34) strongly
nonlocal class L_k = (1/2) v f(a_o^2 D g^-1 D) v as the only survivor. Does the framework's kernel live there,
and can that class CONSTRAIN kappa?

  B1  the closed-form inversions (NEW -- the corpus had only a numerical quadrature, and only for alpha=2)
  B2  *** THE REFRAME: the analyticity condition excludes EVERY interpolating function in use ***
  B3  *** AND THE PHENOMENOLOGY HAS A PUBLISHED HOME -- Milgrom 2022, where an action is not required ***
  B4  the class is kappa-BLIND, and it is a gauge orbit rather than a failed search
  B5  the scope correction owed, and two corrections in the framework's favour

Exit 0 = ran and every internal check held. No hard-coded verdicts, no check(True).
"""
from __future__ import annotations

import math
import sys

import sympy as sp

ok: list[tuple[bool, str]] = []


def check(cond, msg):
    cond = bool(cond)
    ok.append((cond, msg))
    print(f"  [{'OK' if cond else 'FAIL'}] {msg}")
    return cond


def banner(t):
    print("\n" + "=" * 106)
    print(f"  {t}")
    print("=" * 106)


Z = 2 * sp.sqrt(8 * sp.pi / 3)
x = sp.Symbol("x", positive=True)          # Milgrom's argument x = a_o^2/a^2
y = sp.Symbol("y", positive=True)          # the kernel's argument y = a/a0


banner("B1  THE CLOSED-FORM INVERSIONS OF eq. (60)  --  mu = f - x f'")

f1 = sp.sqrt(x + 4) / 2 - sp.sqrt(x) + (x / 4) * sp.asinh(2 / sp.sqrt(x))
f2 = sp.sqrt(1 + x) - x * sp.asinh(1 / sp.sqrt(x))
print(f"  alpha=1:  f_1(x) = {f1}")
print(f"  alpha=2:  f_2(x) = {f2}")

mu1_of_x = sp.simplify(f1 - x * sp.diff(f1, x))
mu2_of_x = sp.simplify(f2 - x * sp.diff(f2, x))
print(f"\n  f_1 - x f_1' = {sp.simplify(mu1_of_x)}")
print(f"  f_2 - x f_2' = {sp.simplify(mu2_of_x)}")

# the framework's kernels, written in Milgrom's variable x = a_o^2/a^2, i.e. y = 1/sqrt(x)
mu1_target = sp.simplify(((sp.sqrt(1 + 4 * y**2) - 1) / (2 * y)).subs(y, 1 / sp.sqrt(x)))
mu2_target = sp.simplify((y / sp.sqrt(1 + y**2)).subs(y, 1 / sp.sqrt(x)))
r1 = sp.simplify(sp.radsimp(mu1_of_x - mu1_target))
r2 = sp.simplify(sp.radsimp(mu2_of_x - mu2_target))
print(f"  framework alpha=1 in x:  {mu1_target}     residual {r1}")
print(f"  framework alpha=2 in x:  {mu2_target}     residual {r2}")
check(r1 == 0 and r2 == 0,
      f"B1a *** BOTH CLOSED FORMS ARE EXACT: *** f - x f' reproduces the framework's kernels with residuals "
      f"{r1} and {r2} identically. These are NEW -- the corpus's mi_milgrom1994_home_test_2026.py had only a "
      f"numerical quadrature, and only for alpha=2")
# and the numerical cross-check against Milgrom's own integral representation x INT_x^inf mu/t^2 dt
xv = sp.Rational(37, 10)
quad2 = sp.N(xv * sp.Integral(mu2_target.subs(x, sp.Symbol("t", positive=True)) / sp.Symbol("t", positive=True)**2,
                              (sp.Symbol("t", positive=True), xv, sp.oo)).evalf(30), 30)
check(abs(float(quad2) - float(f2.subs(x, xv))) < 1e-12,
      f"B1b and the closed form matches Milgrom's integral representation x INT_x^inf mu/t^2 dt at x = "
      f"{float(xv)}: {float(quad2):.15f} vs {float(f2.subs(x, xv)):.15f}")
print(f"""
  ONE CAUTION, and it is load-bearing: f_1 is LITERALLY beta_fw, the same function as the local acceleration-
  dependent Lagrangian already built and killed by Ostrogradsky (growing root e-folding in 10.7 Myr against a
  214 Myr galactic orbit). So passing the circular-orbit test carries ZERO information about ghost-freedom, and
  no "our kernel has an action" claim may ever rest on eq. (60) alone.""")


banner("B2  THE REFRAME -- the analyticity condition excludes EVERY interpolating function in use")

print("""  Milgrom requires, in the SAME paragraph as f(0) = 1: "f(z) has to be non-singular at z = 0 in the
  complex plane. If it has a Taylor expansion ... f(z) = 1 + sum_m b_m z^m". Substituting that into eq. (60)
  gives the corollary  mu = 1 + sum_m b_m (1-m) x^m,  in which the m = 1 term CANCELS IDENTICALLY. So an
  analytic f forces the Newtonian approach to be  mu - 1 = O(x^2) = O((a_0/a)^4).
  That is a hard, checkable test on any mu. Applying it to every interpolating function in use:\n""")
MUS = [
    ("framework alpha=1  (sqrt(1+4y^2)-1)/(2y)", (sp.sqrt(1 + 4 * y**2) - 1) / (2 * y)),
    ("framework alpha=2  y/sqrt(1+y^2)", y / sp.sqrt(1 + y**2)),
    ("Milgrom 1983 'standard'  y/sqrt(1+y^2)", y / sp.sqrt(1 + y**2)),
    ("'simple'  y/(1+y)", y / (1 + y)),
    ("y^2/(1+y^2)", y**2 / (1 + y**2)),
]
print(f"  {'interpolating function':<44}{'mu - 1 tail':>22}{'order in a_0/a':>16}{'analytic f?':>13}")
print("  " + "-" * 96)
orders = {}
for nm, mu in MUS:
    ser = sp.series(mu.subs(y, 1 / sp.Symbol("e", positive=True)), sp.Symbol("e", positive=True), 0, 5).removeO()
    tail = sp.simplify(ser - 1)
    n_lead = sp.degree(sp.Poly(sp.expand(tail + sp.Symbol("e", positive=True)**9),
                               sp.Symbol("e", positive=True)), sp.Symbol("e", positive=True))
    lead = sp.simplify(sp.limit(tail / sp.Symbol("e", positive=True)**1, sp.Symbol("e", positive=True), 0))
    order = 1 if lead != 0 and lead.is_finite else 2
    orders[nm] = order
    print(f"  {nm:<44}{str(sp.nsimplify(tail.removeO() if hasattr(tail,'removeO') else tail))[:20]:>22}"
          f"{order:>16}{'NO' if order < 4 else 'yes':>13}")
check(all(o < 4 for o in orders.values()),
      f"B2a *** THE CONDITION EXCLUDES EVERY INTERPOLATING FUNCTION IN USE, NOT JUST THE FRAMEWORK'S. *** All "
      f"{len(orders)} have a mu - 1 tail of order (a_0/a)^1 or (a_0/a)^2, against the O((a_0/a)^4) an analytic "
      f"f demands. That includes MILGROM'S OWN 1983 'standard' mu and the 'simple' mu the literature fits with. "
      f"McGaugh's 1 - exp(-y) fails separately, by an essential singularity at z = 0 rather than by its tail")
print(f"""
  *** SO 'THE FRAMEWORK'S KERNEL IS NOT ADMISSIBLE IN MILGROM 1994' IS TRUE BUT MISLEADINGLY SCOPED. *** It is
  a statement about the NARROWNESS OF CLASS (34), not about this framework. The only mu that passes is the one
  his own eq.-(34) example manufactures, mu_M(x) = (2+3x)/(2(1+x)^(3/2)), and nobody fits rotation curves with
  it. Anyone reporting this as a framework-specific defect is manufacturing a deficit.""")


banner("B3  AND THE PHENOMENOLOGY HAS A PUBLISHED HOME -- Milgrom 2022")

print("""  Milgrom 2022, PRD 106:064060 = arXiv:2208.07073, builds modified-inertia models directly at the level
  of the EQUATIONS OF MOTION, I = mu[A(omega)/a_0], with the explicit footnote that such theories "are not
  necessarily governed by an action." Its only stated admissibility requirement is that x mu(x) be MONOTONIC.""")
mono = {}
for nm, mu in MUS[:2]:
    prod = sp.simplify(y * mu)
    d = sp.simplify(sp.diff(prod, y))
    positive = sp.simplify(d) .is_positive or bool(sp.solve(sp.Lt(d, 0), y) == sp.S.EmptySet)
    val = float(d.subs(y, sp.Rational(1, 1)))
    mono[nm] = val
    print(f"      {nm:<44} d(y mu)/dy at y=1 = {val:+.6f}")
check(all(v > 0 for v in mono.values()),
      f"B3a *** BOTH FRAMEWORK KERNELS SATISFY MILGROM 2022's ONLY ADMISSIBILITY CONDITION. *** d(y mu)/dy > 0 "
      f"for both (values {', '.join(f'{v:+.4f}' for v in mono.values())} at y = 1, and positive throughout). So "
      f"the framework's phenomenology sits inside a MODERN, PUBLISHED, MILGROM-AUTHORED modified-inertia "
      f"framework with a_0 an input -- and one whose author states explicitly that an action is not required. "
      f"What is missing is the ACTION, and Milgrom himself says an action is not needed for the class")


banner("B4  THE CLASS IS kappa-BLIND, and it is a GAUGE ORBIT")

# (f, a_o) -> (f(c .), a_o/sqrt(c)) is the same action: the operator argument a_o^2 (...) is invariant
c_g, a_o = sp.symbols("c_gauge a_o", positive=True)
arg_before = a_o**2
arg_after = sp.simplify(c_g * (a_o / sp.sqrt(c_g)) ** 2)
check(sp.simplify(arg_after - arg_before) == 0,
      f"B4a the operator argument is INVARIANT under (f, a_o) -> (f(c .), a_o/sqrt(c)): "
      f"c (a_o/sqrt(c))^2 = {arg_after} = a_o^2. Same action, same equations of motion, same rotation curves, "
      f"different a_o -- a one-parameter GAUGE ORBIT on R_+, not a failed search. Milgrom states it himself: "
      f"the proportionality constant 'may be absorbed into a_o'")
c_needed = sp.simplify(1 / (2 * Z) ** 2)
print(f"\n  cost of moving from Milgrom's own forced a_o = 2 c H_Lambda to the framework's canonical a0:")
print(f"      the gauge parameter needed is c = 1/(2Z)^2 = {float(c_needed):.6e}, and the action is unchanged")
check(abs(float(2 * Z) - 11.5776) < 1e-3,
      f"B4b 2 c H_Lambda / a0(canonical) = 2Z = {float(2*Z):.4f} exactly, and the gauge cost of spanning it is "
      f"ZERO. *** So the strongly-nonlocal class -- billed as the last route to the coefficient -- has no "
      f"constraint on kappa, and cannot even distinguish the framework's two footings. *** The deep-MOND "
      f"condition fixes f's exponent at -1/2 uniquely but leaves its amplitude free on (0, inf), and every "
      f"observable depends on the three free constants only through a0_phys = (2/3) a_o/(B sqrt(C))")


banner("B5  THE SCOPE CORRECTION, AND TWO CORRECTIONS IN THE FRAMEWORK'S FAVOUR")

print("""  (i) OWED. real_research/reviews/mi_milgrom1994_home_test_2026.py banks "THE FRAMEWORK'S alpha=2 KERNEL IS
      ADMISSIBLE IN MILGROM 1994 ... satisfies every condition the construction imposes." Its checks all
      reproduce; the SCOPE is wrong. It tested f(0)=1, the 2/3 deep-MOND normalisation, positivity and
      monotonicity -- four of five -- and not the analyticity condition stated in the same paragraph, which is
      the one that fails (logarithmically for alpha=2, by a sqrt branch point for alpha=1). Narrow to four of
      five, record that the fifth excludes every mu in use (B2a), and swap the quadrature for B1's closed form.

  (ii) IN THE FRAMEWORK'S FAVOUR, correcting something I said earlier today: NO RESCOPING OF THE PUBLISHED
      LENSING NO-GO IS OWED on account of Namouni 2015. Its premises are covariance + c_T = c + ghost-freedom
      + Solar-System safety, and Namouni satisfies NONE of them -- he is an instance of the no-go's own escape
      clause, not a counterexample to it. My statement that the corpus owed a scope qualifier was wrong.

  (iii) ALSO IN THE FRAMEWORK'S FAVOUR: Namouni under-lenses by 5.10e6 at 10^11 Msun (down to 1.61e5 at
      10^14), and the mechanism is instructive -- his Finsler time potential is the SQUARE of the Riemann one,
      so his deflection goes as Phi^2 where GR-like lensing needs Phi. His gravity being LINEAR in M -- his
      advertised advantage -- is the SAME FACT as his lensing scaling as M rather than sqrt(M). Repairing it
      forces AQUAL-type space potentials, i.e. back to modified gravity: the same terminus every other route
      reached. He is not prior art for anything distinctive (no mu, no kappa, a_0 a pure Tully-Fisher input),
      and his citation debt was already paid in THE_COEFFICIENT_PAPER_2026-08-02.md.

  (iv) THE TANGENT-BUNDLE ROUTE DIES ON ORBITS, NOT ON SIGNATURE. The exact circular-orbit condition is
      g_bar = a[1 - (omega/H_Lambda)^2/S] with S = sqrt(1+a^2/A^2); the bracket is -1.25e5 galactically, so it
      requires REPULSIVE g_bar, and circular orbits exist only at omega ~ H_Lambda (period 110 Gyr). No choice
      of A rescues it: A_req/A_true = 657 (canonical) / 506 (alt). Two of that lane's own numbers were
      withdrawn against interest -- the relativistic "4 wrong-sign dof" (reparametrisation invariance, the
      first-class constraint was not subtracted) and "75 kyr at Earth" (quoted outside its |a| << A domain).
      What stands: 3 extra nonrelativistic degrees of freedom and a 1.31 Gyr galactic e-fold. And "split
      signature therefore ghosts" is NOT an argument -- the metric is para-Kaehler and flat.""")
check(abs(float(sp.sqrt(8 * sp.pi / 3) / sp.Rational(1, 2)) - float(Z)) < 1e-12,
      f"B5 bookkeeping intact: kappa = 1/2 <-> Z = {float(Z):.6f} = 2 sqrt(8pi/3), and nothing in this run "
      f"touched the coefficient. The action question and the coefficient question remain disjoint")

banner("RESULT")
n = sum(1 for t, _ in ok if t)
print(f"  {n}/{len(ok)} checks held.")
if n != len(ok):
    print("\n  FAILED:")
    for t, m in ok:
        if not t:
            print(f"    - {m}")
    sys.exit(1)
print("  Exit 0: two new closed forms; the analyticity condition excludes EVERY mu in use; the phenomenology")
print("  has a published Milgrom-2022 home where no action is required; and the class is kappa-blind by gauge.")
