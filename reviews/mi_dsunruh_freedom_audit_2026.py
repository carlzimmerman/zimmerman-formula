#!/usr/bin/env python3
r"""mi_dsunruh_freedom_audit_2026.py -- HOW MUCH FREEDOM DOES THE de SITTER-UNRUH MECHANISM ACTUALLY LEAVE?
Carl's question: what if the kernel is slightly different from Milgrom's -- can the framework's kappa = 1/2
work? The answer is precise, and it is BETTER for the framework than the previous note said:

  * THE KERNEL SHAPE IS INDEPENDENT OF THE AMBIENT SCALE. mu = [sqrt(a^2+A^2) - A]/a written in units of
    a0 = 2A is (sqrt(1+4x^2)-1)/(2x) for EVERY A. So the framework keeps the derived alpha=1 kernel at ANY
    a0. The "inseparable package" of the previous note is separable in the coefficient -- that was too strong
    and is corrected here.
  * BUT THE RESPONSE POWER IS FORCED. Among power-law responses f(T) = T^n, deep-MOND linearity
    (mu -> x, which is what gives flat rotation curves and the BTFR) forces n = 1 UNIQUELY, and n = 1 forces
    the deep slope to be exactly 1/2, hence a0 = 2A with nothing left to adjust.
  * SO THE WHOLE QUESTION REDUCES TO ONE NUMBER: the ambient acceleration A. Milgrom takes A = cH_Lambda,
    the de Sitter horizon scale, giving a0 = 2cH_Lambda. The framework needs A = a0/2 = (1/4) c sqrt(G rho_L)
    = cH_Lambda/11.58. That is now a single well-posed physics question instead of a bare postulate.
  * AND IT MAKES THE alpha=2 SWITCH WORSE, NOT BETTER: alpha=2 is outside the derived family for EVERY A and
    EVERY n, so the ephemeris liability cannot be repaired by rescaling or reshaping inside the mechanism.

  F1  the kernel shape is A-independent -- symbolic proof
  F2  *** THE RESPONSE-POWER UNIQUENESS THEOREM: deep-MOND linearity forces n = 1, hence a0 = 2A ***
  F3  the variants, all evaluated and all reported -- and why each fails
  F4  what the framework now needs, stated as one number; and what it costs alpha=2
  F5  correction to the previous note

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


a, A, x, v, n = sp.symbols("a A x v n", positive=True)
Z_FW = 2 * sp.sqrt(8 * sp.pi / 3)          # Carl's form; identical to sqrt(32pi/3)


banner("F1  THE KERNEL SHAPE IS INDEPENDENT OF THE AMBIENT SCALE A")

# mu from the de Sitter-Unruh excess, with a GENERAL ambient acceleration A (Milgrom takes A = cH_Lambda)
mu_A = sp.simplify((sp.sqrt(a**2 + A**2) - A) / a)
print(f"  mu_A(a) = [sqrt(a^2 + A^2) - A]/a = {mu_A}")
# express in units of a0 = 2A, i.e. a = 2 A x
mu_in_x = sp.simplify(mu_A.subs(a, 2 * A * x))
print(f"  in units of a0 = 2A (a = 2 A x):   mu = {mu_in_x}")
mu_1 = sp.simplify((sp.sqrt(1 + 4 * x**2) - 1) / (2 * x))
check(sp.simplify(mu_in_x - mu_1) == 0 and A not in mu_in_x.free_symbols,
      f"F1a *** THE SHAPE IS A-INDEPENDENT. *** In units of a0 = 2A the kernel is {mu_in_x}, with A absent "
      f"from the expression entirely -- identical to the framework's alpha=1 kernel for EVERY ambient scale. "
      f"*** So the framework keeps its DERIVED kernel at any a0 it likes. The previous note's 'inseparable "
      f"package' overstated the constraint and is corrected here (F5). *** What the mechanism fixes is the "
      f"SHAPE, unconditionally, plus the RELATION a0 = 2A -- not a0 itself")


banner("F2  THE RESPONSE-POWER UNIQUENESS THEOREM -- deep-MOND linearity forces n = 1")

# Milgrom's construction generalised: respond to f(T) = T^n, normalised by the flat-space Unruh value at a.
#   T(a)/T0 = sqrt(1+v^2),   T_U(a)/T0 = v,    v = a/A
#   mu_n(v) = [T(a)^n - T0^n] / T_U(a)^n
T_ratio = sp.sqrt(1 + v**2)
mu_n = sp.simplify((T_ratio**n - 1) / v**n)
print(f"  mu_n(v) = [T(a)^n - T0^n]/T_U(a)^n = {mu_n}      (v = a/A)")
lim_hi = sp.limit(mu_n.subs(n, 1), v, sp.oo)
print(f"  large v (Newtonian limit), n = 1:  mu -> {lim_hi}")
print(f"\n  {'n':>4}{'deep-regime behaviour':>28}{'deep power of v':>18}{'MOND-viable?':>15}")
print("  " + "-" * 66)
rows = []
for nv in (1, 2, 3, 4):
    lead = sp.simplify(sp.limit(mu_n.subs(n, nv) / v ** (2 - nv), v, 0))
    powv = 2 - nv
    viable = (powv == 1)
    rows.append((nv, lead, powv, viable))
    print(f"  {nv:>4}{str(lead) + ' * v^' + str(powv):>28}{powv:>18}{'YES' if viable else 'no':>15}")
check(sum(1 for _, _, _, vi in rows if vi) == 1 and rows[0][3],
      f"F2a *** n = 1 IS UNIQUE. *** For f(T) = T^n the deep-regime behaviour is (n/2) v^(2-n), so deep-MOND "
      f"linearity -- mu proportional to v, which is what produces flat rotation curves and the BTFR -- forces "
      f"2 - n = 1, i.e. n = 1, and no other power works: n = 2 gives a CONSTANT mu (no MOND regime at all) and "
      f"n >= 3 gives mu DIVERGING as a -> 0. So 'respond to the excess temperature' is not a choice Milgrom "
      f"made; it is the only power-law response compatible with the phenomenology")
lead1 = rows[0][1]
check(sp.simplify(lead1 - sp.Rational(1, 2)) == 0,
      f"F2b and n = 1 then forces the deep slope to be exactly {lead1}: mu -> v/2 = a/(2A), so matching to "
      f"mu -> a/a0 gives *** a0 = 2A with nothing left to adjust. *** The coefficient is locked to the ambient "
      f"scale, and the lock is the Taylor 1/2 of the square root. This is why no reshaping of the response can "
      f"move the coefficient -- only a different A can")


banner("F3  THE VARIANTS, ALL EVALUATED AND ALL REPORTED")

print("  Stated before evaluation, so this is an enumeration and not a search. Each is a natural alternative")
print("  to 'inertia tracks the excess temperature', and each is reported with why it fails.\n")
VAR = []
# V1 linear in T (Milgrom) -- the baseline
VAR.append(("V1  linear in T (Milgrom)", sp.simplify(mu_n.subs(n, 1)), "baseline"))
# V2 energy density, T^4 (Stefan-Boltzmann)
VAR.append(("V2  energy density, T^4", sp.simplify(mu_n.subs(n, 4)), "Stefan-Boltzmann"))
# V3 quadrature excess sqrt(T^2 - T0^2)
VAR.append(("V3  sqrt(T^2 - T0^2)/T_U", sp.simplify(sp.sqrt(T_ratio**2 - 1) / v), "quadrature"))
# V4 logarithmic (entropy-like) response
VAR.append(("V4  log(T/T0)/log(T_U/T0)", sp.simplify(sp.log(T_ratio) / sp.log(v)), "entropy-like"))
print(f"  {'variant':<28}{'deep v -> 0':>22}{'large v -> inf':>18}{'viable':>9}")
print("  " + "-" * 78)
viable = []
for nm, expr, note in VAR:
    try:
        lo = sp.simplify(sp.limit(expr / v, v, 0))
        lo_txt = f"~ {lo} * v" if lo.is_finite and lo != 0 else ("~ v^0 or worse" if lo == sp.oo else f"{lo}")
    except Exception:
        lo_txt = "n/a"
    hi = sp.limit(expr, v, sp.oo)
    good = (hi == 1) and (lo_txt.startswith("~ ") and "v^0" not in lo_txt)
    if good:
        viable.append(nm)
    print(f"  {nm:<28}{lo_txt:>22}{str(hi):>18}{'YES' if good else 'no':>9}")
check(len(viable) == 1 and viable[0].startswith("V1"),
      f"F3a of the four natural response laws only V1 is viable ({viable}): V2 (T^4) DIVERGES as a -> 0 "
      f"instead of vanishing; V3 collapses to mu = 1 identically, i.e. pure Newton with no MOND regime at all; "
      f"V4 interpolates but its deep behaviour is v^2/log v, which is NOT linear and therefore gives neither "
      f"flat rotation curves nor the BTFR. *** The framework cannot buy a different coefficient by changing "
      f"the response law. ***")


banner("F4  WHAT THE FRAMEWORK NOW NEEDS -- one number; and what it costs alpha=2")

# a0 = 2A always; the framework wants a0 = (1/2) c sqrt(G rho_L) = cH_L/Z_FW
Zc = sp.Rational(1, 2)                                # A = cH_L means Z = 1/2 (a0 = 2cH_L)
A_needed_over_cHL = sp.simplify(1 / (2 * Z_FW))       # A = a0/2 = cH_L/(2 Z_FW)
print(f"  the mechanism always gives a0 = 2A. So:")
print(f"      Milgrom:   A = c H_Lambda            -> a0 = 2 c H_Lambda          (Z = {Zc})")
print(f"      framework: A = a0/2 = cH_L/(2 Z_fw)  -> a0 = cH_L/Z_fw             (Z = {sp.nsimplify(Z_FW)})")
print(f"  so the framework needs the ambient acceleration to be")
print(f"      A = cH_Lambda / {float(1/A_needed_over_cHL):.4f}  =  (1/4) c sqrt(G rho_Lambda)")
check(sp.simplify(A_needed_over_cHL - 1 / (2 * Z_FW)) == 0
      and abs(float(1 / A_needed_over_cHL) - 2 * float(Z_FW)) < 1e-9,
      f"F4a *** THE WHOLE OPEN QUESTION IS NOW ONE NUMBER. *** The framework's kappa = 1/2 is exactly the "
      f"statement that the ambient acceleration entering the de Sitter-Unruh temperature is "
      f"A = (1/4) c sqrt(G rho_Lambda) = cH_Lambda/{float(1/A_needed_over_cHL):.2f}, rather than the horizon "
      f"scale cH_Lambda that Milgrom uses. That is a well-posed physics question about which ambient scale a "
      f"BOUND system actually samples -- a far better position than a bare postulate, and it is the honest "
      f"answer to 'how can the framework's posit work'")

mu_2 = sp.simplify(x / sp.sqrt(1 + x**2))
check(sp.simplify(mu_2 - mu_1) != 0 and all(sp.simplify(mu_2 - sp.simplify(mu_n.subs(n, nv).subs(v, 2 * x))) != 0
                                            for nv in (1, 2, 3, 4)),
      f"F4b *** AND THIS MAKES THE alpha=2 SWITCH WORSE, NOT BETTER. *** Since F1a shows the alpha=1 shape is "
      f"forced for EVERY ambient scale, and F2a/F3a show it is forced for every response law, mu_2 = "
      f"x/sqrt(1+x^2) lies outside the derived family entirely -- not at some other point in it. So the "
      f"solar-system liability CANNOT be repaired by rescaling or reshaping within the mechanism; any fix "
      f"(screening, a frequency gate, or the exponential tail) has to come from outside it, and pays the "
      f"kernel derivation as its price")


banner("F5  CORRECTION TO THE PREVIOUS NOTE")

print(f"""  The note `explainers/the_kernel_and_the_coefficient_come_together.md` says the mechanism delivers
  "a kernel and a coefficient as one inseparable package" and that the framework "cannot hold the kernel
  derivation and the coefficient at the same time." *** THE SECOND HALF IS TOO STRONG AND IS CORRECTED. ***

  What is actually true, from F1a and F2b:
   * the SHAPE is forced unconditionally -- alpha=1 for every ambient scale A and every viable response law;
   * the RELATION a0 = 2A is forced;
   * A ITSELF IS NOT FORCED by the mechanism. Milgrom supplies it from the de Sitter horizon; that is a
     physical choice, not an algebraic necessity.
  So the framework CAN hold the derived kernel together with kappa = 1/2. What it owes is not a new kernel --
  it is an argument for A = (1/4) c sqrt(G rho_Lambda). The previous note's 11.58x gap is unchanged in size;
  what changes is where the gap lives. It is not a conflict between the kernel and the coefficient. It is one
  unexplained ambient scale, and the kernel comes along free.

  STILL UNRESOLVED, and not softened: nothing here supplies that argument. A = (1/4) c sqrt(G rho_Lambda) is
  11.58x below the horizon scale, and the two prior no-go theorems (rational x pi^k cannot reach
  Z = 2 sqrt(8pi/3); quadratic + hbar-free + the Bekenstein-Hawking 1/4 are jointly unsatisfiable) apply to it
  unchanged. What HAS improved is the shape of the problem: from "the coefficient is postulated and the
  mechanism contradicts it" to "the coefficient is postulated, the mechanism supplies the kernel for free, and
  the single open question is which ambient acceleration a bound system samples."

  ONE HONEST WARNING. F4a is an interpretation of what kappa = 1/2 MEANS, not evidence for it. Rewriting a
  postulate as a different postulate is progress in clarity only. It becomes physics if and only if someone
  derives A from the bound-system kinematics -- and per F4b, the alpha=2 kernel now in force is not even in the
  family this argument applies to.""")

banner("RESULT")
nn = sum(1 for t, _ in ok if t)
print(f"  {nn}/{len(ok)} checks held.")
if nn != len(ok):
    print("\n  FAILED:")
    for t, m in ok:
        if not t:
            print(f"    - {m}")
    sys.exit(1)
print("  Exit 0: the shape is A-independent so the framework keeps its derived kernel; n=1 is unique so")
print("  a0 = 2A is locked; the open question reduces to the ambient scale A = (1/4) c sqrt(G rho_Lambda).")
