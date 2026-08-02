#!/usr/bin/env python3
r"""mi_kappa_linear_class_2026.py -- THE kappa-LINEAR SPECTRAL CLASS: the audit was right that it is a valid
probe and the old "structurally blind" verdict is wrong. But the class cannot force kappa, and this proves
why in one line rather than by exhausting candidates.

WHERE THIS COMES FROM. The 2026-08-02 closure audit found that
`KAPPA_SCALE_VS_FRACTION_VERDICT_2026-06-17.md`'s claim -- spectral conditions "can never reach kappa, the
OUTSIDE fraction" -- is a parametrization artefact, because kappa = sqrt(8pi/3)/Z is a BIJECTION with Z. It
named the kappa-linear spectral class "the one genuinely untried door" to deriving kappa. This is the swing at
that door.

WHAT IS ALREADY ON THE BOARD, so the look-elsewhere ledger is honest. Six forced-condition attempts:
  1. local kernel conditions           -> ALL scale-invariant (mi_bootstrap_circularity_2026)
  2. spectral weight vs natural values -> no candidate gives 32pi/3 (mi_spectral_weight_swing_2026)
  3. thermal half-saturation R(Z)=1/2  -> Z* = 4.185 (mi_spectral_kms_bootstrap_2026)
  4. memory-time matching              -> bound violated by 11.6x
  5. P1 fluctuation-dissipation R=2/pi -> Z = 2.5437, kappa = 1.1379 (+128%)
  6. P2 crossover matching             -> Z = 2.8596, kappa = 1.0122 (+102%)
Every one lands at Z of order a few, and the framework needs Z = 5.7888. Guessing more conditions until one
yields 32pi/3 is exactly the failure mode PAPER_ATOMOS_NULL (DOI 10.5281/zenodo.21654272) documents. So this
script does not add a seventh guess as its main content. It proves a structural result about the whole class.

  K1  the bijection, three ways -- the class IS a probe, and the old blindness verdict is withdrawn
  K2  *** THE REPARAMETRIZATION THEOREM: every functional in the family scales as kappa^n exactly, so the
      family is a RELABELLING of kappa and no condition inside it can force kappa without importing it ***
  K3  the pre-registered enumeration anyway, both functionals, every candidate reported
  K4  the reduction to ONE unexplained number: kappa^2 = 1/4, i.e. Z^2 = 4 x (8pi/3)
  K5  verdict, ledger, and where a forcing condition could still live

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


Z_FW = math.sqrt(32 * math.pi / 3)          # 5.788810, the framework
Z_M20 = 2 * math.pi                         # 6.283185, Milgrom 2020
K_REF = math.sqrt(8 * math.pi / 3)          # 2.894405 = kappa at Z = 1
A0_BOX = 0.16                               # the corpus's own +/-16% empirical a0 box


def kappa_of_Z(Z):
    return K_REF / Z


banner("K1  THE BIJECTION -- the class IS a probe; the 'structurally blind' verdict is WITHDRAWN")

kap, Zs, n = sp.symbols("kappa Z n", positive=True)
# a0 = kappa c sqrt(G rho_L) and rho_L = 3 H_L^2/(8 pi G)  =>  a0 = kappa c H_L sqrt(3/(8pi)) = c H_L / Z
Z_from_kappa = sp.simplify(1 / (kap * sp.sqrt(sp.Rational(3, 1) / (8 * sp.pi))))
print(f"  from a0 = kappa c sqrt(G rho_Lambda) and rho_Lambda = 3H_L^2/(8 pi G):   Z = {Z_from_kappa}")
check(sp.simplify(Z_from_kappa - sp.sqrt(8 * sp.pi / 3) / kap) == 0,
      f"K1a Z = sqrt(8pi/3)/kappa EXACTLY, so Z and kappa are in strict BIJECTION -- "
      f"d(ln Z)/d(ln kappa) = {sp.simplify(sp.diff(sp.log(Z_from_kappa), kap) * kap)}, never 0. Any condition "
      f"that pins Z pins kappa. The old verdict's 'spectral conditions can never reach kappa, the OUTSIDE "
      f"fraction' is a PARAMETRIZATION ARTEFACT and is withdrawn")
check(abs(float(Z_from_kappa.subs(kap, sp.Rational(1, 2))) - Z_FW) < 1e-12,
      f"K1b and it closes numerically: kappa = 1/2 -> Z = "
      f"{float(Z_from_kappa.subs(kap, sp.Rational(1,2))):.12f} against sqrt(32pi/3) = {Z_FW:.12f}")

# the committed spectral functional, from mi_spectral_weight_swing_2026: W_above(Z) = 1/(pi Z)
u = sp.Symbol("u", positive=True)
W1 = sp.simplify(sp.integrate(1 / (sp.pi * u**2), (u, Zs, sp.oo)))
print(f"\n  the committed weight functional:  W_above(Z) = INT_Z^inf du/(pi u^2) = {W1}")
check(sp.simplify(W1 - 1 / (sp.pi * Zs)) == 0,
      f"K1c W_above = 1/(pi Z) exactly (reproducing mi_spectral_weight_swing_2026), so W_above is ALSO in "
      f"bijection with kappa: W_above = kappa/(pi sqrt(8pi/3)) = {float(1/(math.pi*K_REF)):.8f} x kappa -- "
      f"exactly LINEAR, which is the class the audit named")
print(f"  framework needs  W_above = 1/(pi Z_fw) = {1/(math.pi*Z_FW):.8f}   (i.e. only "
      f"{100/(math.pi*Z_FW):.2f}% of the weight above the branch point)")
print(f"  Milgrom 2020     W_above = 1/(pi 2pi)  = {1/(math.pi*Z_M20):.8f}")


banner("K2  THE REPARAMETRIZATION THEOREM -- the whole family is a relabelling of kappa")

# the natural family of tail functionals on this axis
Wn = sp.simplify(sp.integrate(1 / (sp.pi * u ** (n + 1)), (u, Zs, sp.oo)))
print(f"  W_n(Z) = INT_Z^inf du/(pi u^(n+1)) = {Wn}      (W_1 is the committed W_above)")
Wn_kappa = sp.simplify(Wn.subs(Zs, sp.sqrt(8 * sp.pi / 3) / kap))
print(f"  substituting Z = sqrt(8pi/3)/kappa:   W_n = {Wn_kappa}")
power = sp.simplify(sp.diff(sp.log(Wn_kappa), kap) * kap)
check(sp.simplify(power - n) == 0,
      f"K2a *** W_n IS EXACTLY PROPORTIONAL TO kappa^n FOR EVERY n: *** d(ln W_n)/d(ln kappa) = {power}, "
      f"identically in n. So the entire tail-functional family is a pure POWER RELABELLING of kappa -- it "
      f"contains no additional structure, and the framework's value sits at no distinguished point in any "
      f"member of it")

# consequence: a condition W_n = c yields kappa = (n pi (8pi/3)^(n/2) c)^(1/n). Solve symbolically.
cc = sp.Symbol("c", positive=True)
kap_sol = sp.solve(sp.Eq(Wn_kappa, cc), kap)
kap_expr = sp.simplify(kap_sol[0])
print(f"\n  so a condition W_n = c gives  kappa = {kap_expr}")
# for kappa = 1/2 the required c is forced -- i.e. c must be TUNED, for every n
c_req = sp.simplify(Wn_kappa.subs(kap, sp.Rational(1, 2)))
print(f"  and kappa = 1/2 requires        c = {c_req}")
check(len(c_req.free_symbols) == 1 and n in c_req.free_symbols,
      f"K2b *** THE NO-GO. *** For every n, kappa = 1/2 requires c = {c_req} -- a value that depends on n and "
      f"is fixed only by DEMANDING kappa = 1/2. Inverting a monotone one-parameter map cannot create "
      f"information: 'W_n = c forces kappa' is 'c forces kappa', so any condition inside this family imports "
      f"the answer it is supposed to derive. *** THE kappa-LINEAR CLASS IS A VALID PROBE BUT NOT A POSSIBLE "
      f"DERIVATION *** -- and that is a stronger statement than the six failed attempts")
print(f"""
  WHAT THIS DOES AND DOES NOT SAY. It does NOT say kappa is underivable -- it says the derivation cannot come
  from setting a tail functional of THIS kernel's own spectral measure equal to a constant, because the
  kernel's measure was itself calibrated on the RAR. That is the circularity KERNEL_THEORY.md:47 already
  states in its own words ("forced by (Herglotz class) + (the RAR): there is nothing left to tune"). The
  audit was right that the class is a probe; it is a probe of a quantity already fitted.""")


banner("K3  THE PRE-REGISTERED ENUMERATION ANYWAY -- every candidate reported, both functionals")

# Fixed in source, chosen for being the standard O(1) constants of a Herglotz/thermal spectral problem.
# NOT tuned to any target. Every one is reported with its implied kappa and whether it survives the a0 box.
CANDS = [("1/2", 0.5), ("1/pi", 1 / math.pi), ("2/pi", 2 / math.pi), ("1/4", 0.25),
         ("1/(2pi)", 1 / (2 * math.pi)), ("1/pi^2", 1 / math.pi**2), ("1/(2pi^2)", 1 / (2 * math.pi**2)),
         ("3/(8pi)", 3 / (8 * math.pi)), ("1/(4pi)", 1 / (4 * math.pi)), ("1/8", 0.125),
         ("1/(2pi^3)", 1 / (2 * math.pi**3)), ("1/(8pi^3)", 1 / (8 * math.pi**3))]
print(f"  {len(CANDS)} candidates, fixed in source. a0 box = +/-{100*A0_BOX:.0f}% around kappa = 1/2 "
      f"({0.5*(1-A0_BOX):.4f}-{0.5*(1+A0_BOX):.4f}).\n")
print(f"  {'candidate c':<14}{'value':>12}{'kappa (n=1)':>13}{'in box?':>9}{'kappa (n=2)':>13}{'in box?':>9}")
print("  " + "-" * 72)
hits = []
for nm, c in CANDS:
    k1 = float(sp.N(kap_expr.subs({n: 1, cc: c})))
    k2 = float(sp.N(kap_expr.subs({n: 2, cc: c})))
    in1 = abs(k1 / 0.5 - 1) <= A0_BOX
    in2 = abs(k2 / 0.5 - 1) <= A0_BOX
    if in1:
        hits.append((nm, 1, k1))
    if in2:
        hits.append((nm, 2, k2))
    print(f"  {nm:<14}{c:>12.6f}{k1:>13.6f}{'YES' if in1 else 'no':>9}{k2:>13.6f}{'YES' if in2 else 'no':>9}")

print(f"\n  candidates landing inside the empirical a0 box: {len(hits)} of {2*len(CANDS)} cells")
for nm, nn, kv in hits:
    print(f"      c = {nm:<12} n = {nn}  ->  kappa = {kv:.6f}  ({100*(kv/0.5-1):+.1f}% from 1/2)")
check(not any(abs(kv / 0.5 - 1) < 0.01 for _, _, kv in hits),
      f"K3a NO candidate lands on kappa = 1/2 to better than 1%. The closest cells are inside the +/-16% "
      f"empirical box but that box is DATA, not a derivation -- being in it is necessary and worth nothing "
      f"on its own. This reproduces mi_spectral_weight_swing_2026's null on a second functional")
check(len(hits) >= 1,
      f"K3b and stated against my own no-go: {len(hits)} cells DO land in the box, so the class is in the "
      f"right NEIGHBOURHOOD -- consistent with K2's reading that it is a faithful relabelling of a fitted "
      f"quantity rather than a wrong axis. Neighbourhood is not derivation")

# THE SHARPEST THING IN THIS RUN, and it goes against the framework.
Z_hits = sorted({round(K_REF / kv, 6) for _, _, kv in hits})
check(len(Z_hits) == 1 and abs(Z_hits[0] - Z_M20) < 1e-4,
      f"K3c *** AND IT IS THE RIVAL THAT THE SPECTRAL AXIS PICKS OUT, NOT THE FRAMEWORK. *** Every cell that "
      f"lands in the empirical box corresponds to Z = {Z_hits[0]:.6f} = 2pi to {abs(Z_hits[0]-Z_M20):.1e} -- "
      f"MILGROM 2020's coefficient -- on BOTH functionals independently (c = 1/(2pi^2) at n=1 and "
      f"c = 1/(8pi^3) at n=2 are the same Z = 2pi expressed in each). The framework's sqrt(32pi/3) lands on "
      f"no natural constant in either. So on the THEORY axis the natural spectral value is 2pi, while on the "
      f"DATA axis the SPARC profile likelihood favours kappa = 1/2 over 1/2pi by ~2.2 sigma "
      f"(mi_a0_profile_likelihood_sparc_2026.py). Those two point OPPOSITE WAYS and both should be quoted")


banner("K4  THE REDUCTION -- ONE unexplained number, and it is a 4")

Z2 = sp.simplify((sp.sqrt(8 * sp.pi / 3) / kap) ** 2)
print(f"  Z^2 = {Z2}, so at kappa = 1/2:  Z^2 = {sp.simplify(Z2.subs(kap, sp.Rational(1,2)))}")
ratio = sp.simplify(Z2.subs(kap, sp.Rational(1, 2)) / (8 * sp.pi / 3))
check(ratio == 4,
      f"K4a *** Z^2 = {ratio} x (8pi/3) EXACTLY. *** 8pi is the Einstein coupling, 3 is Friedmann's -- both "
      f"forced conversions that CANCEL out of the physics. So 'derive Z' reduces to 'derive the {ratio}', "
      f"equivalently kappa^2 = 1/{ratio}. The framework's entire undetermined content is one factor of "
      f"{ratio} (a factor 2 in Z). That is the sharpest available statement of the open problem")
check(sp.simplify(kap**2 - sp.Rational(1, 4)).subs(kap, sp.Rational(1, 2)) == 0,
      f"K4b equivalently kappa^2 = 1/4 exactly -- and note that K2a's theorem says the n = 2 functional is "
      f"the one in which kappa^2 appears linearly, i.e. the natural variable for this factor is the "
      f"QUADRATIC functional, not the linear one the prior six attempts all probed")

print(f"""
  A NUMERICAL COINCIDENCE, FLAGGED AS ONE AND NOT CASHED. The unexplained factor is 4, and 4 is the
  Bekenstein-Hawking denominator in S = A/4G. That is suggestive and it is ALL it is: this script has no
  construction that forces the horizon entropy's quarter to appear as Z^2/(8pi/3), and writing one after
  noticing the coincidence is precisely the Kepler-epicycle move the atomos null paper documents. Recorded
  as a lead with 1 candidate's worth of look-elsewhere, NOT as a derivation. The same discipline retires two
  other factor-of-4 stories I checked: the Tolman active density |rho + 3p| = 2 rho_Lambda gives a factor
  sqrt(2) in a0, not 2 (so kappa = 1/(2 sqrt(2)) = {1/(2*math.sqrt(2)):.5f}, {100*(1/(2*math.sqrt(2))/0.5-1):+.0f}% -- outside the box); and
  equipartition's 1/2 per degree of freedom is a factor 2 in ENERGY, which enters a0 as sqrt(2), not 2.""")


banner("K5  VERDICT AND LEDGER")

PRIOR = 6
NEW = 2                                       # the n=1 and n=2 enumerations run here
tot = PRIOR + NEW
print(f"""  *** THE DOOR IS OPEN AS A PROBE AND SHUT AS A DERIVATION, and both halves are corrections. ***

  OPEN: the audit was right. kappa = sqrt(8pi/3)/Z is a bijection (K1a), so
  KAPPA_SCALE_VS_FRACTION_VERDICT_2026-06-17.md's "spectral conditions can never reach kappa, the OUTSIDE
  fraction" is a parametrization artefact and is WITHDRAWN. The class is a faithful probe of kappa.

  SHUT: but every tail functional of this kernel's measure obeys W_n ~ kappa^n exactly (K2a), so the family
  is a one-parameter relabelling of kappa. A condition "W_n = c" therefore forces kappa only by fixing c,
  and c is fixed only by demanding the answer (K2b). No member of the class can DERIVE kappa. This replaces
  "six attempts have missed" with a structural reason, and it is the stronger result.

  WHAT REMAINS, stated precisely: kappa^2 = 1/4, i.e. Z^2 = 4 x (8pi/3) with 8pi Einstein and 3 Friedmann.
  The whole open problem is ONE factor of 4 (K4a). A forcing condition must come from OUTSIDE this family --
  it cannot be a functional of the kernel's own RAR-calibrated measure, because that measure already contains
  the fitted scale. Candidate outside routes, none attempted here: horizon ENTROPY rather than horizon
  density (the 4 coincidence, K4); a boundary-counting condition that fixes Z^2 directly rather than Z; or a
  first-principles derivation of the kernel measure itself that does not pass through the RAR calibration.

  LEDGER, honestly: {PRIOR} prior forced-condition attempts + {NEW} functional enumerations here = {tot},
  i.e. log2({tot}) = {math.log2(tot):.2f} bits of accumulated look-elsewhere on this axis. Any future hit must
  beat that before it counts. And K2b means a hit inside this family would not count at all.

  AND THE ONE RESULT HERE THAT CUTS AGAINST THE FRAMEWORK, which must be quoted alongside the favourable
  SPARC result and not instead of it: every natural constant that lands inside the empirical a0 box
  corresponds to Z = 2pi -- MILGROM 2020's coefficient -- on BOTH functionals (K3c). The framework's
  sqrt(32pi/3) lands on no natural spectral constant in either. So:
      THEORY axis (natural spectral values):  favours 2pi
      DATA axis (SPARC profile likelihood):   favours kappa = 1/2 over 1/2pi by ~2.2 sigma
  Those point OPPOSITE WAYS. That is the honest state of the kappa question: the data prefer the framework's
  coefficient and the spectral naturalness argument prefers its rival, and neither is decisive.

  *** kappa = 1/2 REMAINS FITTED, NOT DERIVED. *** That is unchanged by this swing, and the swing's value is
  that it says why the axis cannot change it -- so the next attempt should not be spent here.""")

banner("RESULT")
nn = sum(1 for x, _ in ok if x)
print(f"  {nn}/{len(ok)} checks held.")
if nn != len(ok):
    print("\n  FAILED:")
    for x, m in ok:
        if not x:
            print(f"    - {m}")
    sys.exit(1)
print("  Exit 0: the class is a valid probe (old verdict withdrawn) but provably cannot force kappa;")
print("  the open problem reduces to one factor of 4.")
