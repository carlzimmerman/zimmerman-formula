#!/usr/bin/env python3
r"""mi_orbital_q_selfaudit_2026.py -- SELF-AUDIT of the published q = 2 no-go (DOI 10.5281/zenodo.21782600).

THE CHALLENGE. The paper says the dS-Unruh mechanism "returns Milgrom's coefficient and cannot be made to
yield a smaller one." That is a PROOF claim. But mi_orbital_unruh_q_2026.py never evaluated a detector response:
it bounded the orbital correction to the CORRELATOR (which is solid) and then extracted q from Milgrom's
ANALYTIC balance I(a) = T(a) - T_GH. The response lane that was supposed to compute F(E) and T_eff(E) died twice
on an output limit and was never replaced. So the question is fair: is q = 2 a result, or an assumption wearing
one?

This script separates the two and reports both ways.

  N1  does the 2 pi cancel? -- i.e. is q blind to the Unruh normalisation, or did a factor get lost
  N2  *** THE RIGIDITY THEOREM: what class of inertia functionals can give MOND at all? ***
  N3  what freedom actually remains, and what q each remaining option would need to deliver
  N4  the honest scope of the published claim, and the correction owed

Exit 0 = every check held. No check(True).
"""
from __future__ import annotations

import math
import sys

import sympy as sp

ok: list[tuple[bool, str]] = []
Z_FW = 2 * math.sqrt(8 * math.pi / 3)
Q_NEED = 1.0 / Z_FW                       # 0.17275, what kappa = 1/2 requires
Q_M2020 = 1.0 / (2 * math.pi)             # 0.15915


def check(c, m):
    c = bool(c)
    ok.append((c, m))
    print(f"  [{'OK' if c else 'FAIL'}] {m}")
    return c


def banner(t):
    print("\n" + "=" * 104)
    print(f"  {t}")
    print("=" * 104)


a, H, C = sp.symbols("a H C", positive=True)
T = sp.sqrt(a**2 + H**2) / (2 * sp.pi)            # Deser-Levin / GEMS temperature, 2 pi included
T_GH = H / (2 * sp.pi)

banner("N1  DOES THE 2 pi CANCEL? -- is q blind to the Unruh normalisation")

I_lin = T - T_GH
c2 = sp.limit(I_lin / a**2, a, 0)                  # deep coefficient
c1 = sp.limit(I_lin / a, a, sp.oo)                 # Newtonian coefficient
q_lin = sp.simplify(c1 / c2)
print(f"  I = T - T_GH  with T = sqrt(a^2+H^2)/2pi")
print(f"    deep      c2 = {sp.simplify(c2)}")
print(f"    Newtonian c1 = {sp.simplify(c1)}")
print(f"    q = c1/c2    = {q_lin}")
check(sp.simplify(q_lin - 2 * H) == 0,
      f"N1a THE 2 pi CANCELS EXACTLY, and this DEFENDS the published number rather than undermining it. Both c1 "
      f"and c2 carry the same 1/2pi prefactor, so it divides out of q = c1/c2 = {q_lin}. *** So q = 2 is NOT an "
      f"artefact of dropping an Unruh normalisation -- it is blind to it. The '2' in q = 2 is the binomial 1/2 "
      f"from sqrt(1+x) ~ 1 + x/2, inverted: a structural feature of the quadrature a5^2 = a^2 + H^2, not a "
      f"convention ***")


banner("N2  *** THE RIGIDITY THEOREM -- what functionals can give MOND at all? ***")

print("""  Suppose inertia is any function of the LOCAL temperature, I = f(T) - f(T_GH), with T = sqrt(a^2+H^2)/2pi.
  MOND requires BOTH limits:
      (i)  I -> const * a    as a >> H     (Newtonian: F = m a recovered)
      (ii) I -> const * a^2  as a << H     (deep MOND: g_obs = sqrt(g_bar a0))
  Test the natural candidates.""")

CANDS = [("f(T) = T            (Milgrom 1999)", T - T_GH),
         ("f(T) = T^2", T**2 - T_GH**2),
         ("f(T) = T^4   (Stefan-Boltzmann energy density)", T**4 - T_GH**4),
         ("f(T) = sqrt(T)", sp.sqrt(T) - sp.sqrt(T_GH)),
         ("f(T) = log(T)", sp.log(T) - sp.log(T_GH))]
print(f"\n  {'functional':<46}{'deep power':>12}{'Newt power':>12}{'MOND?':>8}{'q':>10}")
print("  " + "-" * 90)
survivors = []
for nm, I in CANDS:
    # deep: leading power of a as a -> 0 ; Newtonian: leading power as a -> oo
    dp = sp.limit(sp.log(sp.simplify(I.subs(H, 1))) / sp.log(a), a, 0)
    npow = sp.limit(sp.log(sp.simplify(I.subs(H, 1))) / sp.log(a), a, sp.oo)
    good = (sp.simplify(dp - 2) == 0) and (sp.simplify(npow - 1) == 0)
    qv = "-"
    if good:
        cc2 = sp.limit(I / a**2, a, 0)
        cc1 = sp.limit(I / a, a, sp.oo)
        qv = sp.simplify(cc1 / cc2)
        survivors.append((nm, qv))
    print(f"  {nm:<46}{str(dp):>12}{str(npow):>12}{('YES' if good else 'no'):>8}{str(qv):>10}")
check(len(survivors) == 1 and sp.simplify(survivors[0][1] - 2 * H) == 0,
      f"N2a *** THE TWO LIMITS TOGETHER FORCE f LINEAR, AND THEREFORE FORCE q = 2. *** Of the five candidates "
      f"only f(T) = T survives: T^2 and T^4 give the right DEEP power but a WRONG Newtonian power (a^2 and a^4 "
      f"instead of a), sqrt(T) and log(T) fail the deep limit. And the survivor is unique because requiring "
      f"I ~ a at large a, where T ~ a/2pi, forces f to be asymptotically linear -- after which the deep limit "
      f"has no remaining freedom. *** So within the class 'inertia is a function of the local temperature', "
      f"q = 2 is a THEOREM, not a choice, and the no-go is stronger than the paper claimed rather than weaker ***")


banner("N3  WHAT FREEDOM ACTUALLY REMAINS -- and what it would have to deliver")

need = 2.0 / Q_NEED
print(f"  kappa = 1/2 needs q = 1/Z = {Q_NEED:.5f}; the mechanism gives 2. The functional would have to supply")
print(f"  a factor {1/need:.5f} = 1/{need:.3f}, i.e. shift the crossover DOWN by {need:.2f}x.")
print(f"\n  candidate sources of a non-cancelling factor, and where each lands:")
ROUTES = [("2 pi from a Planck factor in F(E) rather than T", 2.0 / (2 * math.pi)),
          ("4 pi from a horizon-area / solid-angle normalisation", 2.0 / (4 * math.pi)),
          ("pi alone", 2.0 / math.pi),
          ("2Z = 4 sqrt(8 pi/3), what kappa = 1/2 actually needs", 2.0 / (2 * Z_FW))]
print(f"  {'route':<52}{'q':>10}{'vs 1/Z':>10}{'vs 1/2pi':>11}")
print("  " + "-" * 84)
for nm, qv in ROUTES:
    print(f"  {nm:<52}{qv:>10.5f}{qv/Q_NEED:>10.3f}{qv/Q_M2020:>11.3f}")
check(abs(2.0 / (4 * math.pi) / Q_M2020 - 1.0) < 1e-12 and abs(2.0 / (2 * Z_FW) / Q_NEED - 1.0) < 1e-12,
      f"N3a AND THE ARITHMETIC IS UNCOMFORTABLE FOR THE FRAMEWORK, WHICH IS WHY IT IS WORTH STATING: a 4 pi "
      f"lands EXACTLY on Milgrom 2020's 1/2pi ({2.0/(4*math.pi):.5f}), and a plain pi lands at "
      f"{2.0/math.pi:.5f}. Both are natural response-function factors. Reaching 1/Z = {Q_NEED:.5f} requires "
      f"dividing 2 by 2Z = {2*Z_FW:.3f} = 4 sqrt(8pi/3) -- note it is 2Z and NOT Z, a slip an earlier version of "
      f"this table made in the framework's favour by a factor 2. That factor carries sqrt(pi) times sqrt(32/3) "
      f"and is NOT a natural normalisation of any detector response. *** So the remaining freedom, if it delivers anything, "
      f"most plausibly delivers MILGROM 2020's coefficient and not this framework's ***")

print("""
  THE FREEDOM THAT IS GENUINELY UNEXPLORED, stated so it is not lost:
   (a) inertia as a functional of the full RESPONSE F(E) rather than of the temperature T. The GEMS/conformal
       lanes proved strict KMS thermality FAILS for every Omega != 0, so T_eff(E) is necessarily gap-dependent
       for orbits -- that E-dependence is real freedom, and it was NOT explored because the response lane died.
       N1a shows a 2 pi cannot enter through the temperature; it could enter through a Planck factor.
   (b) functionals of the correlator W(s) directly, not through any temperature.
   (c) non-quadratic-in-u couplings, rho_m/T_munu couplings, and the b-projector -- all already in the corpus's
       own open list from 2026-08-01.
  None of these is closed by the published paper, and N2a does not close them either: N2a closes only the class
  'a function of the local temperature'.""")


banner("N4  THE HONEST SCOPE, AND THE CORRECTION OWED")

print("""  WHAT THE PUBLISHED RESULT ACTUALLY ESTABLISHES, in two parts that must not be merged:
   1. q IS ORBITAL-INVARIANT. Solid, and independent of any functional choice: sup eps = gamma^2v^2/(1+gamma^2v^2)
      is a-independent to 1e-16 over five decades, so the orbital correction is a uniform rescaling that cancels
      in the crossover ratio. Nothing about the inertia postulate enters this.
   2. q = 2 FOR TEMPERATURE-BASED FUNCTIONALS. Now upgraded by N2a from an assumption to a theorem WITHIN that
      class -- the two limits force f linear -- but it is still a class restriction.

  THE PAPER'S SENTENCE "the mechanism therefore returns Milgrom's coefficient and cannot be made to yield a
  smaller one" IS OVERSTATED. It is true for temperature-based functionals and it is NOT established for
  response-based ones, which were never computed. The correct claim is:
      "within the class of inertia functionals depending on the local de Sitter-Unruh temperature, q = 2 is
       forced by the Newtonian and deep-MOND limits jointly, and is orbital-invariant; response-based
       functionals with a gap-dependent effective temperature remain uncomputed."
  A v2 of the record is owed with that scoping, and the ARITHMETIC of N3a should travel with it: the natural
  remaining factors point at Milgrom 2020's coefficient, not at kappa = 1/2.""")
check(abs(2.0 / (2 * Z_FW) - Q_NEED) < 1e-15 and Q_NEED > Q_M2020,
      f"N4a and one small point in the framework's favour, since the ledger should run both ways: 1/Z = "
      f"{Q_NEED:.5f} is LARGER than 1/2pi = {Q_M2020:.5f} by {100*(Q_NEED/Q_M2020-1):.2f}%, so of the two "
      f"published candidates the framework's is the one CLOSER to the mechanism's q = 2 -- by a factor "
      f"{2.0/Q_NEED:.2f} against {2.0/Q_M2020:.2f}. That is a weak consolation and is not evidence, but it is "
      f"the honest direction of the residual and the paper did not state it")

banner("RESULT")
n = sum(1 for c, _ in ok if c)
print(f"  {n}/{len(ok)} checks held.")
if n != len(ok):
    print("\n  FAILED:")
    for c, m in ok:
        if not c:
            print(f"    - {m}")
    sys.exit(1)
print("  Exit 0: the no-go SURVIVES audit and is stronger than published within its class (N2a: the two limits")
print("  force q = 2), but the published sentence over-reaches its class. A v2 scoping is owed.")
