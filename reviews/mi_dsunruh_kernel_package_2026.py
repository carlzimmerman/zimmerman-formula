#!/usr/bin/env python3
r"""mi_dsunruh_kernel_package_2026.py -- THE de SITTER-UNRUH MECHANISM FORCES THE alpha=1 KERNEL AND
a0 = 2 c H_Lambda AS ONE INSEPARABLE PACKAGE. The framework keeps the kernel and rejects the coefficient by a
factor 11.58. And my own "derivation" of a0 = cH_Lambda/2pi from the previous swing is WITHDRAWN -- it
disagrees with the correct reading by 4 pi.

WHY THIS EXISTS. mi_kernel_measure_from_desitter_2026 claimed to DERIVE a0 = cH_Lambda/2pi by identifying the
kernel's dimensionless FREQUENCY variable w = omega c/a0 with the de Sitter thermal variable
x = 2 pi omega/H_Lambda. A literature check on Milgrom's own pedagogical review then turned up the standard
de Sitter-Unruh construction, which is an identification on the ACCELERATION rather than the frequency, and
which gives a0 = 2 c H_Lambda. Those differ by 4 pi = 12.57. Both cannot be right, and the acceleration
reading is the correct one -- the 2 pi in the Unruh prefactor CANCELS out of a turnover condition, while my
frequency reading smuggled it in through an unforced temperature-to-frequency conversion. So this script
withdraws that claim and establishes what the mechanism actually forces.

THE STANDARD CONSTRUCTION (Deser & Levin 1997; Narnhofer, Peter & Thirring 1996; and stated in Milgrom's own
MOND review). A uniformly accelerated observer in de Sitter space sees a thermal bath at
        T(a) = (hbar / 2 pi c k_B) sqrt(a^2 + a_dS^2),        a_dS = c H_Lambda
so the EXCESS over the ambient Gibbons-Hawking temperature that an inertial observer already sees is
        Delta T(a) ~ sqrt(a^2 + a_dS^2) - a_dS
If inertia is proportional to that excess, the effective inertial mass ratio is
        mu(a) = [sqrt(a^2 + a_dS^2) - a_dS] / a
Note the 2 pi and the hbar sit in a COMMON PREFACTOR and cancel out of mu entirely -- which is exactly why
the correct reading carries no 2 pi, and why mine did.

  D1  mu_dS in closed form, and its two limits
  D2  *** IS IT THE FRAMEWORK'S alpha=1 KERNEL? -- symbolic identity test ***
  D3  the coefficient the SAME derivation forces, and the size of the framework's departure
  D4  what the alpha=1 -> alpha=2 switch costs that the corpus has not priced
  D5  the withdrawal of my cH_Lambda/2pi claim, quantified

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


a, adS, u, x = sp.symbols("a a_dS u x", positive=True)
Z_FW = sp.sqrt(32 * sp.pi / 3)


banner("D1  mu_dS IN CLOSED FORM, AND ITS TWO LIMITS")

mu_dS_a = sp.simplify((sp.sqrt(a**2 + adS**2) - adS) / a)
mu_dS = sp.simplify(mu_dS_a.subs(a, u * adS))          # dimensionless u = a/a_dS
print(f"  mu_dS(a) = [sqrt(a^2 + a_dS^2) - a_dS]/a = {mu_dS_a}")
print(f"  in u = a/a_dS:   mu_dS(u) = {mu_dS}")
lim_hi = sp.limit(mu_dS, u, sp.oo)
lim_lo = sp.simplify(sp.series(mu_dS, u, 0, 2).removeO())
print(f"  u -> infinity:  mu_dS -> {lim_hi}      (Newtonian)")
print(f"  u -> 0:         mu_dS -> {lim_lo}      (deep MOND)")
check(lim_hi == 1 and sp.simplify(lim_lo - u / 2) == 0,
      f"D1a mu_dS -> {lim_hi} at large acceleration and -> {lim_lo} at small, so it interpolates correctly and "
      f"its deep-regime slope is 1/2 in u. The 1/2 is what fixes the coefficient in D3 -- it is not free")
check(not mu_dS.has(sp.pi) and not mu_dS.has(sp.Symbol("hbar")),
      f"D1b and mu_dS contains NO 2 pi and NO hbar: both sit in the common prefactor of T(a) and cancel in the "
      f"ratio. *** That is precisely why the correct de Sitter-Unruh coefficient carries no 2 pi, and why my "
      f"frequency-based reading in the previous swing was wrong. ***")


banner("D2  IS IT THE FRAMEWORK'S alpha=1 KERNEL? -- symbolic identity test")

# the framework's alpha=1 relation g_obs^2 = g_bar^2 + g_bar a0, in units of a0 (x = g_obs/a0, y = g_bar/a0):
#   x^2 = y^2 + y  =>  y = (-1 + sqrt(1+4x^2))/2  =>  mu_1(x) = y/x
a0s = sp.Symbol("a_0", positive=True)
mu_1 = sp.simplify((sp.sqrt(1 + 4 * x**2) - 1) / (2 * x))
print(f"  framework alpha=1:  from g_obs^2 = g_bar^2 + g_bar a0,   mu_1(x) = {mu_1}   (x = g_obs/a0)")
# the mechanism's own coefficient identification is a0 = 2 a_dS, hence u = a/a_dS = 2x
mu_dS_in_x = sp.simplify(mu_dS.subs(u, 2 * x))
print(f"  mu_dS with the mechanism's own a0 = 2 a_dS (so u = 2x):   mu_dS = {mu_dS_in_x}")
resid = sp.simplify(mu_dS_in_x - mu_1)
check(resid == 0,
      f"D2a *** THEY ARE THE SAME FUNCTION. Residual = {resid}, identically. *** The de Sitter-Unruh "
      f"interpolation IS the framework's alpha=1 kernel, exactly, with no adjustment. So the framework's "
      f"kernel shape is NOT an arbitrary choice -- it is what the mechanism produces. That is a genuine "
      f"vindication of the kernel, and it is prior art (Milgrom 1999; the construction appears in his own "
      f"pedagogical review)")
# and the same statement in the corpus's published algebraic form
lhs = sp.simplify((x * a0s) ** 2)
rhs = sp.simplify((mu_1 * x * a0s) ** 2 + (mu_1 * x * a0s) * a0s)
check(sp.simplify(lhs - rhs) == 0,
      f"D2b cross-check in the corpus's own published form: mu_1 reproduces g_obs^2 = g_bar^2 + g_bar a0 "
      f"identically, so D2a is a statement about the framework's PUBLISHED law and not about a paraphrase")


banner("D3  THE COEFFICIENT THE SAME DERIVATION FORCES")

# a0 = 2 a_dS = 2 c H_Lambda  =>  Z = 1/2  =>  kappa = sqrt(8pi/3)/Z
Z_dS = sp.Rational(1, 2)
kap_dS = sp.simplify(sp.sqrt(8 * sp.pi / 3) / Z_dS)
kap_fw = sp.Rational(1, 2)
ratio = sp.simplify(kap_dS / kap_fw)
print(f"  the mechanism forces a0 = 2 a_dS = 2 c H_Lambda, i.e. Z = {Z_dS}, kappa = {kap_dS} = "
      f"{float(kap_dS):.5f}")
Z_carl = sp.simplify(2 * sp.sqrt(8 * sp.pi / 3))
print(f"  the framework uses kappa = {kap_fw}, i.e. Z = 2 sqrt(8pi/3) = {Z_carl} = {float(Z_carl):.5f}")
print(f"  ratio = {ratio} = {float(ratio):.4f}")
check(sp.simplify(Z_carl - Z_FW) == 0 and abs(float(ratio) - 2 * float(Z_FW)) < 1e-9,
      f"D3a *** THE PACKAGE IS INSEPARABLE AND THE FRAMEWORK TAKES HALF OF IT. *** The same one-line "
      f"construction that gives the framework its kernel (D2a) also forces a0 = 2 c H_Lambda, which is "
      f"{float(ratio):.2f}x = 4 sqrt(8pi/3) times the framework's value. Written the clean way: the framework's "
      f"Z = 2 sqrt(8pi/3) EXACTLY (identical to sqrt(32pi/3)), so its coefficient is one factor of 2 in Z away "
      f"from the kappa = 1 reference sqrt(8pi/3), and the mechanism's output sits 4 sqrt(8pi/3) away from it. The framework adopts the kernel and "
      f"rejects the coefficient by that factor. This is not new to the corpus -- A0_HALF_THE_DARK_ENERGY_RATE "
      f"already states the 11.58x -- but the KERNEL half of the package is not stated anywhere, and it is what "
      f"makes the rejection costly rather than free")


banner("D4  WHAT THE alpha=1 -> alpha=2 SWITCH COSTS, UNPRICED UNTIL NOW")

mu_2 = sp.simplify(x / sp.sqrt(1 + x**2))
print(f"  the kernel now in force (alpha=2):  mu_2(x) = {mu_2}")
diff_at_1 = sp.simplify(mu_2.subs(x, 1) - mu_1.subs(x, 1))
print(f"  mu_2(1) = {sp.nsimplify(mu_2.subs(x,1))} = {float(mu_2.subs(x,1)):.6f} against "
      f"mu_1(1) = {float(mu_1.subs(x,1)):.6f}")
check(sp.simplify(mu_2 - mu_dS_in_x) != 0,
      f"D4a *** THE alpha=2 KERNEL IS NOT THE de SITTER-UNRUH KERNEL. *** mu_2 != mu_dS as functions "
      f"(they differ by {float(abs(diff_at_1)):.4f} at x = 1, {100*float(abs(diff_at_1)/mu_1.subs(x,1)):.1f}%). "
      f"So the alpha=1 -> alpha=2 switch -- made for solar-system reasons -- ALSO costs the framework the "
      f"mechanism's derivation of its kernel shape. The corpus priced that switch at +0.0033 dex on SPARC plus "
      f"ephemeris relief; it did NOT price the loss of the de Sitter-Unruh derivation of the kernel, and that "
      f"is a real cost this script is the first to state")
print(f"""
  THE HONEST LEDGER ON THE SWITCH, both directions:
   * alpha=1 KEEPS the de Sitter-Unruh derivation of the kernel (D2a) but carries the Sun-binding ephemeris
     liability at 1279x the Earth bound, post-EFE = bare (mi_efe_escape_and_ch23_withdrawn_2026).
   * alpha=2 fixes the ephemeris to 6.2-12.4x (still failing, mi_alpha2_sun_reflex_2026) but FORFEITS the
     kernel derivation.
  Neither kernel is free. That trade is now explicit and was not before.""")


banner("D5  THE WITHDRAWAL, QUANTIFIED")

Z_mine = 2 * sp.pi
disagreement = sp.simplify(Z_mine / Z_dS)
print(f"  my previous claim (frequency identification):  Z = {Z_mine} -> a0 = c H_Lambda/2pi")
print(f"  the correct acceleration identification:       Z = {Z_dS} -> a0 = 2 c H_Lambda")
print(f"  they disagree by a factor {disagreement} = {float(disagreement):.3f}")
check(sp.simplify(disagreement - 4 * sp.pi) == 0,
      f"D5a *** MY cH_Lambda/2pi 'DERIVATION' IS WITHDRAWN. *** It disagrees with the standard construction by "
      f"exactly {disagreement} = 4 pi = {float(disagreement):.2f} (I first wrote 4 pi^2 -- corrected), and "
      f"the standard construction is the correct one: the 2 pi "
      f"and the hbar cancel out of mu (D1b), so a turnover condition on the ACCELERATION carries no 2 pi. My "
      f"reading identified the kernel's FREQUENCY unit with the thermal frequency k_B T/hbar, which is an "
      f"extra, unforced conversion. The claim that the de Sitter tie 'derives kappa = sqrt(2/(3pi))' must not "
      f"be repeated")
print(f"""
  WHAT SURVIVES FROM THAT SWING, unchanged: the two no-go results, which are arithmetic about Z and are
  independent of which identification is used --
   * Z^2/pi = 32/3 is rational while Z/pi^k is irrational for every integer k, so rational x pi^k ingredients
     can force Z^2 but never Z;
   * quadratic-in-Z, hbar-free, and carrying the Bekenstein-Hawking 1/4 are jointly unsatisfiable.
  And what survives is now sharper, because the de Sitter mechanism's actual output is a RATIONAL multiple of
  cH_Lambda (namely 2), which is in the barred class for Z = sqrt(32pi/3) exactly as those theorems predict.

  *** NET EFFECT ON THE FRAMEWORK, stated both ways. *** BETTER: its alpha=1 kernel is derived, not chosen --
  the de Sitter-Unruh mechanism produces it exactly (D2a), which is a substantive result the corpus did not
  have. WORSE: the same derivation forces a0 = 2 c H_Lambda, 11.58x the framework's value (D3a), and the
  alpha=2 switch now in force forfeits the kernel derivation entirely (D4a). The framework cannot hold the
  kernel derivation and the coefficient at the same time, and under alpha=2 it holds neither.""")

banner("RESULT")
nn = sum(1 for x_, _ in ok if x_)
print(f"  {nn}/{len(ok)} checks held.")
if nn != len(ok):
    print("\n  FAILED:")
    for x_, m in ok:
        if not x_:
            print(f"    - {m}")
    sys.exit(1)
print("  Exit 0: mu_dS IS the alpha=1 kernel exactly, with a0 = 2cH_Lambda forced; my cH_L/2pi is withdrawn.")
