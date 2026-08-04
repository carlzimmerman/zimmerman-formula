#!/usr/bin/env python3
r"""mi_crossover_master_formula_2026.py -- REFUTES the "rigidity theorem" of mi_orbital_q_selfaudit_2026.py.

WHAT I CLAIMED, AND WHY IT WAS WRONG. In mi_orbital_q_selfaudit_2026.py (published same day inside DOI
10.5281/zenodo.21782600 v2) I asserted that for an inertia functional I(a) = f(T(a)) - f(T_GH), with
T = sqrt(a^2+H^2)/(2 pi), requiring BOTH the Newtonian limit (I ~ a for a >> H) and the deep-MOND limit
(I ~ a^2 for a << H) FORCES f linear and therefore forces q = 2. My argument was: "requiring I ~ a at large a,
where T -> a/2pi, forces f to be asymptotically linear -- after which the deep limit has no remaining freedom."

The first clause is true. The second is a NON-SEQUITUR. Asymptotic linearity constrains f as T -> infinity; the
deep limit reads f' AT T_GH. Those are different points and nothing connects them. The five candidates I tested
(T, T^2, T^4, sqrt T, log T) are all SCALE-FREE, so for them the asymptotic slope and the local slope coincide up
to a power -- which is why they all gave r = 1 or failed outright. Five examples, not a theorem.

WHAT IS ACTUALLY TRUE:

    q  =  2 * c1p / f'(T_GH)        with c1p = lim_{T->inf} f(T)/T          [ C1 ]

so the temperature class is a ONE-PARAMETER family in r = f'(T_GH)/c1p, with q = 2/r. Milgrom 1999's f = T is
the r = 1 member. And:

    r = 1                    ->  q = 2            Milgrom 1999 (hyperbolic dS-Unruh balance)
    r = 4 pi     EXACTLY     ->  q = 1/(2 pi)     Milgrom 2020
    r = 2 Z = 8 sqrt(6 pi)/3 ->  q = 1/Z          this framework, kappa = 1/2

CREDIT. The kernel nu = sqrt(1+1/y) and the balance I = sqrt(a^2+H^2) - H are Milgrom 1999 PLA 253:273 eqs 6-9,
who fixes the coefficient at a0_hat = 2 c H_Lambda. Milgrom 1994 Ann.Phys. 229:384 sec II eq 3 writes
a_lambda = c^2 sqrt(Lambda/3). The five-acceleration construction is Deser & Levin 1997 CQG 14:L163. Milgrom 2020
proposes kappa = 1/2pi. The framework's distinctive content is the COEFFICIENT plus the MI completion.

AND THE COST, WHICH IS THE POINT OF CHECK C5. r is a FREE dimensionless number. If the only thing that fixes
r = 2Z is wanting kappa = 1/2, then this trades one fitted number for another and is a REPARAMETRISATION, NOT a
derivation. kappa = 1/2 remains FITTED, NOT DERIVED. What the refutation buys is narrower and honest: the door
is not shut by theorem, so the question "why is the floor a0/2 rather than c H_Lambda" is a live physical
question rather than a closed one.

Exit 0 = every check held. No check(True); every condition below can fail.
"""
from __future__ import annotations

import math
import sys

import sympy as sp

ok: list[tuple[bool, str]] = []


def check(c, m):
    c = bool(c)
    ok.append((c, m))
    print(f"  [{'OK' if c else 'FAIL'}] {m}")
    return c


def banner(t):
    print("\n" + "=" * 104)
    print(f"  {t}")
    print("=" * 104)


a, T, bet = sp.symbols("a T beta", positive=True)
Z = 2 * sp.sqrt(8 * sp.pi / 3)                  # 5.7888100...
Tf = sp.sqrt(a**2 + 1) / (2 * sp.pi)            # H = 1
TG = sp.Integer(1) / (2 * sp.pi)


def crossover(fexpr):
    """(c1, c2, q) for I(a) = f(T(a)) - f(T_GH), H = 1. q = c1/c2 = a0/H."""
    I = fexpr.subs(T, Tf) - fexpr.subs(T, TG)
    c1 = sp.limit(I / a, a, sp.oo)
    c2 = sp.limit(I / a**2, a, 0)
    return c1, c2, sp.simplify(c1 / c2)


banner("C1  THE MASTER FORMULA  q = 2 c1p / f'(T_GH)")

dT = sp.simplify(sp.series(Tf - TG, a, 0, 4).removeO())
print(f"  T(a) - T_GH = {dT}   (so c2 = f'(T_GH)/(4 pi) and, since T -> a/2pi, c1 = c1p/(2 pi))")
print(f"  => q = c1/c2 = 2 c1p / f'(T_GH)")
check(sp.simplify(dT - a**2 / (4 * sp.pi)) == 0,
      f"C1a the deep expansion is T - T_GH = a^2/(4 pi H) exactly, which is what puts f'(T_GH) -- the slope AT "
      f"THE FLOOR -- into c2, while c1 reads the slope at infinity. *** These are different points on f, and "
      f"that single fact is the whole refutation ***")

c1m, c2m, qm = crossover(T)                                     # Milgrom 1999
print(f"\n  f = T (Milgrom 1999):  c1 = {c1m}, c2 = {c2m}, q = {qm}")
check(sp.simplify(qm - 2) == 0 and sp.simplify(c1m - 1 / (2 * sp.pi)) == 0
      and sp.simplify(c2m - 1 / (4 * sp.pi)) == 0,
      f"C1b the formula reproduces Milgrom 1999's q = 2 with c1 = 1/2pi and c2 = 1/4pi, so it is anchored on the "
      f"one case whose answer is independently known")

al, be = sp.symbols("alpha b", positive=True)
_, _, qaff = crossover(al * T + be)
check(sp.simplify(qaff - 2) == 0,
      f"C1c q is invariant under f -> alpha f + b: the additive constant cancels in f(T) - f(T_GH) and the "
      f"multiplicative one cancels in c1/c2, so q depends on f ONLY through the ratio r = f'(T_GH)/c1p. This is "
      f"what makes r, not f, the physical content")


banner("C2  THE r TABLE -- and 4 pi is EXACT, not a decimal coincidence")

rows = [("Milgrom 1999, hyperbolic dS-Unruh balance", sp.Integer(2)),
        ("Milgrom 2020, kappa = 1/2pi", 1 / (2 * sp.pi)),
        ("THIS FRAMEWORK, kappa = 1/2", 1 / Z)]
print(f"  {'coefficient proposal':<44}{'q':>13}{'r = 2/q':>13}{'r exact':>26}")
print("  " + "-" * 96)
for nm, qv in rows:
    r = sp.simplify(2 / qv)
    print(f"  {nm:<44}{float(qv):>13.8f}{float(r):>13.6f}{sp.srepr(r)[:0] or str(r):>26}")
check(sp.simplify(2 / (1 / (2 * sp.pi)) - 4 * sp.pi) == 0,
      f"C2a Milgrom 2020's coefficient requires r = 4 pi EXACTLY (symbolic, not numeric) -- a horizon-area or "
      f"solid-angle normalisation is precisely the kind of factor that delivers 4 pi, so of the two live "
      f"proposals HIS is the one with an obvious mechanism for its r. This is against this framework's interest "
      f"and is the reason the check is here")
r_fw = sp.simplify(2 * Z)
check(sp.simplify(r_fw - 8 * sp.sqrt(6 * sp.pi) / 3) == 0,
      f"C2b this framework requires r = 2Z = 8 sqrt(6 pi)/3 = {float(r_fw):.6f}, which is NOT 4 pi -- the two "
      f"differ by {100*(1-float(r_fw)/float(4*sp.pi)):.3f}%, the same 7.87% that separates the two coefficients "
      f"themselves. NOTE, correcting an earlier version of this very check: 2Z = 4 sqrt(8 pi/3) and 8 pi/3 is the "
      f"FRIEDMANN factor, so 2Z is '4 over the square root of the Friedmann factor' and its sqrt(pi) is "
      f"Friedmann's. The objection 'it carries sqrt(pi) that no normalisation supplies' is WITHDRAWN as a bad "
      f"objection -- see mi_2Z_is_the_friedmann_root_2026.py (8/8). What survives is Deser-Levin's: the horizon "
      f"FIXES the floor at H, so H is mechanism-given and sqrt(G rho) is a substitution")
check(abs(float(2 * Z) - 11.577620) < 1e-6 and abs(float(1 / Z) - 0.17274707) < 1e-8,
      f"C2c the numbers are 2Z = {float(2*Z):.6f} and 1/Z = {float(1/Z):.8f}. Recorded to 8 figures because an "
      f"earlier table in this corpus wrote Z where 2Z was meant, in the framework-favouring direction, by a "
      f"factor of exactly 2")


banner("C3  *** THE COUNTEREXAMPLE -- my rigidity theorem is REFUTED ***")

print("""  Take f(T) = T + lam beta T_GH (1 - exp(-(T - T_GH)/(beta T_GH))), with lam = 2Z - 1.
  It is smooth, strictly increasing, and ASYMPTOTICALLY LINEAR with slope 1 (the exponential saturates), so it
  satisfies the Newtonian limit that my argument said was the binding one. Its slope at the floor is 2Z.""")

lam = r_fw - 1
fe = T + lam * bet * TG * (1 - sp.exp(-(T - TG) / (bet * TG)))
slope_inf = sp.limit(fe / T, T, sp.oo)
slope_TG = sp.simplify(sp.diff(fe, T).subs(T, TG))
_, _, qe = crossover(fe)
qe = sp.simplify(qe)
print(f"\n  lim f/T as T -> inf   = {slope_inf}")
print(f"  f'(T_GH)              = {slope_TG} = {float(slope_TG):.6f}")
print(f"  q                     = {qe} = {float(qe):.14f}")
print(f"  target 1/Z            = {float(1/Z):.14f}")
check(sp.simplify(slope_inf - 1) == 0,
      f"C3a the counterexample IS asymptotically linear (slope exactly 1), so it satisfies the Newtonian limit -- "
      f"it is not a cheat that evades the constraint my argument actually used")
check(sp.simplify(slope_TG - r_fw) == 0,
      f"C3b and its slope at the Gibbons-Hawking floor is exactly 2Z = {float(r_fw):.6f}, i.e. r = 2Z while the "
      f"asymptotic slope is 1 -- the two slopes are DIFFERENT, which is exactly what I asserted was impossible")
check(sp.simplify(qe - 1 / Z) == 0,
      f"C3c *** IT DELIVERS q = 1/Z EXACTLY (symbolically, sqrt(6)/(8 sqrt(pi))), i.e. a0 = 1/2 c sqrt(G rho_L). "
      f"SO THE RIGIDITY THEOREM OF mi_orbital_q_selfaudit_2026.py IS REFUTED: the two MOND limits do NOT force "
      f"q = 2 within the temperature class. WITHDRAWN ***")
check(sp.simplify(sp.diff(qe, bet)) == 0,
      f"C3d and q is independent of beta, so beta is free SHAPE freedom that does not disturb the coefficient: "
      f"one knob sets q, the rest of the family is available for the interpolation shape. The family is genuinely "
      f"two-dimensional, not a single tuned point")

# numerical confirmation, independent of sympy's limit machinery, with float64 hygiene
rf, TGf = float(r_fw), float(TG)


def I_num(av):
    # T - T_GH = (sqrt(a^2+1) - 1)/2pi, written as a^2/(2pi(sqrt(a^2+1)+1)): the literal difference loses ALL
    # significance for a < 1e-4 (sqrt(1+1e-14) - 1 is known to only ~2% in float64), which is what made the
    # first version of this check fail by 2.3%.
    dTv = av * av / (2.0 * math.pi * (math.sqrt(av * av + 1.0) + 1.0))
    d = dTv / TGf                              # beta = 1
    # -expm1(-d) is exact where (1 - exp(-d)) loses digits for small d
    return dTv + (rf - 1.0) * TGf * (-math.expm1(-d))


c1n = I_num(1e9) / 1e9
c2n = I_num(1e-6) / 1e-12
print(f"\n  numeric (float64, expm1-guarded): c1 = {c1n:.12e}, c2 = {c2n:.12e}, q = {c1n/c2n:.12f}")
check(abs(c1n / c2n / float(1 / Z) - 1.0) < 1e-6,
      f"C3e independently confirmed in float64 at a/H = 1e9 and 1e-6: q = {c1n/c2n:.10f} against 1/Z = "
      f"{float(1/Z):.10f}. TWO guards were needed and the first version of this check FAILED by 2.3% without the "
      f"second: -expm1(-d) for the exponential, and the algebraic rewrite of sqrt(a^2+1) - 1 to kill the "
      f"catastrophic cancellation. A deep-limit check that reads a difference of two nearly-equal float64 "
      f"quantities measures rounding, not physics")


banner("C4  THE SAME FACTOR, SEEN AS A FLOOR -- so this is ONE door, not two")

g, k, a0 = sp.symbols("g_obs kfloor a_0", positive=True)
gb = sp.sqrt(g**2 + k**2) - k                                   # Milgrom's balance, floor kfloor
line = sp.simplify(sp.expand((gb.subs(k, a0 / 2) + a0 / 2) ** 2 - (g**2 + a0**2 / 4)))
gobs2 = sp.solve(sp.Eq(gb.subs(k, a0 / 2), sp.Symbol("gbar", positive=True)), g)
print(f"  Milgrom's balance with floor kfloor = a0/2 inverts to g_obs^2 = g_bar^2 + a0 g_bar:")
print(f"    residual of the exact algebra = {line}")
check(line == 0,
      f"C4a the framework's a0-line g_obs^2 = g_bar^2 + a0 g_bar is IDENTICALLY Milgrom's five-acceleration "
      f"balance with the floor at a0/2. So the framework's entire distinctive coefficient is the VALUE OF THE "
      f"FLOOR, and 'a nonlinear f at the GH floor' and 'a linear f at a moved floor' are the SAME factor 2Z read "
      f"two ways -- the count of open doors goes 0 -> 1, NOT 0 -> 2")
ratio = sp.simplify(1 / (1 / Z / 2))
check(sp.simplify(ratio - r_fw) == 0,
      f"C4b and the floor ratio c H_Lambda / (a0/2) is the same 2Z = {float(ratio):.6f}. Note what the needed "
      f"floor IS: a0/2 = (1/4) c sqrt(G rho_Lambda), a BARE sqrt(G rho) carrying NO Friedmann 8pi/3, whereas "
      f"c H_Lambda = c sqrt(8 pi G rho_Lambda/3) carries it. A bare sqrt(G rho) is a LOCAL response to the "
      f"vacuum density; sqrt(8 pi G rho/3) is the GLOBAL expansion rate. That is a statable physical difference, "
      f"not merely a relabelled fit -- but it is not a derivation of either")


banner("C5  THE COST, STATED AGAINST INTEREST")

print("""  What the refutation does NOT buy:
   - r is a FREE dimensionless number. Nothing in this script derives r = 2Z; it is imposed to hit kappa = 1/2.
     Trading kappa for r is a REPARAMETRISATION, not a derivation, and must never be presented otherwise.
   - Deser & Levin's construction FIXES the floor at the Gibbons-Hawking value c H_Lambda from the horizon. If
     that fixing is binding then no re-choice of floor is available and the mechanism cannot reach kappa = 1/2
     whatever f is. This script does not defeat that argument; it only shows the two MOND LIMITS do not defeat it
     either, which is a different and much weaker statement than the one I published.
   - Milgrom 2020's r = 4 pi has an obvious candidate mechanism (horizon area / solid angle). 2Z = 8 sqrt(6 pi)/3
     carries sqrt(pi) and has none that I can name. On mechanism the arrow points at HIS coefficient.
   - This says nothing about admissibility: whether an r = 2Z kernel survives the corpus's ephemeris bound and
     the SPARC shape range is UNTESTED here and could kill it independently.""")
check(float(r_fw) < float(4 * sp.pi) and float(1 / Z) > float(1 / (2 * sp.pi)),
      f"C5a the residual's honest direction, both ways in one check: 2Z < 4pi and 1/Z > 1/2pi, so this "
      f"framework's r is the SMALLER departure from Milgrom 1999's r = 1 ({float(r_fw):.4f} against "
      f"{float(4*sp.pi):.4f}) and its q the CLOSER to q = 2. That is the direction of the residual and not "
      f"evidence for it; the mechanism argument above points the other way")


banner("RESULT")
n = sum(1 for c, _ in ok if c)
print(f"  {n}/{len(ok)} checks held.")
if n != len(ok):
    print("\n  FAILED:")
    for c, m in ok:
        if not c:
            print(f"    - {m}")
    sys.exit(1)
print("  Exit 0. The rigidity theorem of mi_orbital_q_selfaudit_2026.py is WITHDRAWN: q = 2/r with r free, and an")
print("  explicit asymptotically-linear f delivers q = 1/Z exactly. The live question is no longer 'can the")
print("  temperature class reach kappa = 1/2' (it can) but 'is the de Sitter floor fixed at c H_Lambda by the")
print("  horizon, or is it (1/4) c sqrt(G rho_Lambda)'. kappa = 1/2 remains FITTED, NOT DERIVED.")
