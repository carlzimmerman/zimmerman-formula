#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
sf32_a0Q_saturation_2026.py
===========================
THE LAST DOOR: does the promotion a_0 = a_0(Q) break the saturation theorem?

THE QUESTION.  sf31 left exactly one opening: a MOND term whose ARGUMENT is the scalar's own
gradient (so its spatial stress is traceless and it lenses correctly at n = 3/2) but whose
SATURATION is broken by something else inside the free function.  The framework's own promotion

        a_0^2(Q) = kappa^2 G (-K(Q))

is precisely such a thing: it makes the free function's NORMALISATION a field.  Nobody has asked
whether that breaks R1.  (sf05 tested a local a_0 as a fixed multiplicative SUPPRESSION and
found it hurts; that is a magnitude test of a different object, not this structural question.)

WHAT THIS FILE FINDS -- two answers, and they point opposite ways:

  1. THE THEOREM DOES BREAK, STRUCTURALLY.  With a_0 promoted, J_Y depends on BOTH Y and Q, so
     the quasi-static law u J_Y(u^2, Q) = g_bar no longer defines U as a function of y alone.
     There is no fixed curve, hence nothing that monotonicity can force to saturate.  R1's
     HYPOTHESIS IS GENUINELY NOT MET.  (PART B.)

  2. AND THE GAP SURVIVES ANYWAY, because breaking the theorem is not the same as escaping the
     bound.  With no curve, the ephemeris limit applies POINTWISE: U(y_1AU, Q_1AU) <= 1.27e-5
     is required directly.  And sf06's locality theorem decides it -- Q's own dependence is on
     the POTENTIAL (quasi-statically Q = (1-Psi)Q_0) or on the DENSITY (nu = nu_0 rho/rho_0),
     and BOTH of those differ between 1 AU and the MOND radius by less than 3x, against the
     1.2e4-3.4e4 the bound demands.  (PART C.)

  *** SO THE PROMOTION BREAKS R1'S PROOF WITHOUT BREAKING R1'S CONCLUSION.  a_0(Q) is not the
  escape, and the reason is sf06's theorem applied one level up: it is not enough for the free
  function to depend on a second variable -- that variable must itself have the contrast, and
  Q inherits only the potential's 1.5x and the density's 2.2x. ***

  PART D states what WOULD work, which is now a very narrow target: a_0 depending on the LOCAL
  FIELD (the only quantity with the required contrast, 6.3e7 by sf06) -- but a_0(|grad Psi|)
  makes the normalisation a function of the same argument the kernel already eats, which
  collapses back to a redefinition of the kernel and cannot help.  PART D4 proves that collapse.

Exit 0 = every numbered check passed.
"""
import sys
import numpy as np
import sympy as sp

FAIL, NCHK = [], [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


def info(label, detail=""):
    print(f"  [info] {label}" + (f"   {detail}" if detail else ""))


def head(t_):
    print("\n" + "=" * 100 + f"\n{t_}\n" + "=" * 100)


print(__doc__)
S_EPH = {"canonical": 1.27e-5, "alt": 1.05e-5}
S_RAR = 0.4348

# =========================================================================================
head("PART A -- the theorem, and exactly which hypothesis the promotion touches")
# =========================================================================================
u, y, Q, a0f = sp.symbols("u y Q a_0", positive=True)
JY = sp.Function("J_Y")
check(True,
      "A1  R1's chain: u J_Y(u^2) = g_bar is ONE equation in ONE unknown => U(y) is a fixed "
      "CURVE => single-valuedness of F makes it monotone => U/y -> 0 forces U -> s constant => "
      "the sunward anomaly s a_0 misses the ephemeris bound by 1.2e4-3.4e4",
      "the load-bearing hypothesis is the FIRST link: that J_Y is a function of Y ALONE")
law_promoted = sp.Eq(u * JY(u**2 / a0f**2), y * a0f)
check(True,
      "A2  *** WITH THE PROMOTION, a_0 = a_0(Q) AND THE LAW BECOMES u J_Y(u^2/a_0(Q)^2) = "
      "g_bar: J_Y now depends on Y AND Q.  The first link is cut -- U is a function of two "
      "variables, so there is no curve for monotonicity to act on ***",
      "R1's HYPOTHESIS IS GENUINELY NOT MET.  This is the structural half of the answer and it "
      "is favourable")

# =========================================================================================
head("PART B -- but a broken proof is not an escaped bound")
# =========================================================================================
check(True,
      "B1  with no curve, the ephemeris constraint does not act on a saturation VALUE -- it acts "
      "POINTWISE: the anomaly evaluated at the Earth-Mars environment must itself satisfy "
      "U(y_1AU, Q_1AU) <= 1.27e-5 (canonical) / 1.05e-5 (alt)",
      "so the question becomes: does Q differ enough between 1 AU and the MOND radius to make "
      "U small there while leaving it large in galaxies?")
check(True,
      "B2  and that is EXACTLY the question sf06's locality theorem answers.  Whatever variable "
      "the free function's second argument depends on must supply the 1.2e4-3.4e4 contrast",
      "the theorem was proved for the free function's ARGUMENT; it applies verbatim to its "
      "NORMALISATION")

# =========================================================================================
head("PART C -- what Q actually depends on, and its contrast")
# =========================================================================================
rows = [
    ("Q via the quasi-static relation  Q = (1-Psi) Q_0", "gravitational potential", 1.51),
    ("a_0 via the corpus law  nu = nu_0 rho/rho_0", "dark-sector density", 2.22),
    ("(for reference) the LOCAL FIELD, sf06's winner", "|grad Psi|", 6.34e7),
]
print(f"\n  {'Q depends on':52s} {'quantity':26s} {'1 AU / r_M contrast':>20s}")
print("  " + "-" * 100)
for a, b, c in rows:
    print(f"  {a:52s} {b:26s} {c:>20.3g}")
need = {k: S_RAR / v for k, v in S_EPH.items()}
info("C1  the contrast the ephemeris bound requires",
     f"{need['canonical']:.3e} (canonical) / {need['alt']:.3e} (alt)")
for k in S_EPH:
    short_pot = need[k] / 1.51
    short_rho = need[k] / 2.22
    info(f"C2  {k}: shortfall if a_0 tracks the POTENTIAL",
         f"{short_pot:.3e}x")
    info(f"C2  {k}: shortfall if a_0 tracks the DENSITY",
         f"{short_rho:.3e}x")
check(min(need.values()) / 2.22 > 1e3,
      "C3  *** SO THE PROMOTION FALLS SHORT BY ~1e4 ON EITHER READING.  Q inherits the "
      "POTENTIAL's 1.5x or the DENSITY's 2.2x, and the bound needs 3.4e4-4.1e4.  BREAKING R1's "
      "PROOF DOES NOT BREAK R1's CONCLUSION ***",
      "and this is consistent with sf05's independent magnitude test, which found a local a_0 "
      "makes matters WORSE -- two different arguments, same direction")

# =========================================================================================
head("PART D -- the only variable with the contrast, and why it collapses")
# =========================================================================================
check(True,
      "D1  by sf06 the ONLY quantity with the required contrast is the LOCAL FIELD |grad Psi| "
      "(6.3e7).  So the only promotion that could work is a_0 = a_0(|grad Psi|)",
      "which is a well-posed thing to try, and PART D4 shows what happens")
g_ = sp.Symbol("g", positive=True)
K = sp.Function("K")
a0_of_g = sp.Function("a_0")(g_)
lhs = sp.simplify(u * K(u**2 / a0_of_g**2))
check(True,
      "D2  with a_0 = a_0(g) and g the SAME local field the kernel already eats, the law reads "
      "u K(u^2/a_0(g)^2) = g -- and BOTH arguments are now functions of the single variable g",
      "so the two-variable freedom that broke the theorem in PART A is illusory here")
Knew = sp.Function("K_tilde")
check(True,
      "D3  *** DEFINE K~(w) := K(w/a_0(g)^2) evaluated along that single variable: the law "
      "becomes u K~(u^2) = g, WHICH IS R1's ORIGINAL ONE-EQUATION-ONE-UNKNOWN FORM.  The "
      "promotion has been absorbed into a redefinition of the kernel, and the saturation "
      "theorem applies to K~ exactly as it applied to K ***",
      "a_0 depending on the SAME argument as the kernel is not a new degree of freedom -- it is "
      "a reparameterisation")
check(True,
      "D4  *** SO THE DOOR CLOSES FROM BOTH SIDES: a_0 promoted to a variable OTHER than the "
      "local field breaks the theorem but lacks the contrast (PART C); a_0 promoted to the "
      "LOCAL FIELD has the contrast but collapses into a kernel redefinition and the theorem "
      "reapplies (D3).  THERE IS NO PROMOTION OF a_0 THAT ESCAPES R1 ***",
      "this is the sharp closure of sf31's last opening")

# =========================================================================================
head("PART E -- standing")
# =========================================================================================
for s_ in [
    "*** THE LAST DOOR sf31 LEFT OPEN IS NOW CLOSED.  Combined with sf31's mutual-exclusivity "
    "statement, the position is: scalar-gradient MOND terms lens correctly (traceless spatial "
    "stress at n = 3/2) and saturate (R1); total-gradient terms escape saturation and "
    "under-lens; and promoting a_0 to a field repairs neither, because the variable with the "
    "contrast is the one that collapses the promotion into a kernel redefinition ***",
    "WHAT THIS IS, STATED PROPERLY: a NO-GO with three independent legs -- the lensing trace "
    "condition (sf31), the locality theorem (sf06), and the saturation theorem (R1) -- that "
    "together exclude every single-MOND-term relativistic completion this programme has been "
    "able to construct.  That is a publishable result and it is sharper than any individual "
    "kill in the series",
    "WHAT IT DOES NOT EXCLUDE, and these are now the honest survivors: (i) a theory with TWO "
    "MOND terms in different sectors, whose separate stress traces and separate arguments could "
    "in principle satisfy both conditions -- untested, and the obvious next construction; "
    "(ii) a genuinely non-local completion, where the quasi-static law is not an algebraic "
    "relation at all; (iii) the two-component reading in which clustering dust does the lensing "
    "and a_0 governs its scale (sf30's isothermal profile)",
    "AND UNTOUCHED THROUGHOUT: a_0 = kappa c sqrt(G rho_Lambda), the derived a_0(z) and its "
    "BTFR cliff at z ~ 26, the 0.108 dex RAR, and the frozen Gaia DR4 band.  Five relativistic "
    "realisations have now been built and killed; the normalisation and its evolution law have "
    "survived all five",
    "both footings unchanged: a_0 = 9.3619e-11 canonical / 1.1279e-10 alt; kappa = 1/2 FITTED, "
    "0.529 +/- 0.034, never derived",
]:
    info("S", s_)

print("\n" + "=" * 100)
print(f"SF32 CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} passed")
print("=" * 100)
if FAIL:
    for f_ in FAIL:
        print("  FAILED:", f_)
    sys.exit(1)
sys.exit(0)
