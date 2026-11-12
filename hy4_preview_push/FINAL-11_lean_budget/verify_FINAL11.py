#!/usr/bin/env python3
"""FINAL-11 (LEAN-BUDGET) -- independent sympy audit of every bracket shipped in
Final11Budget.lean.  Run BEFORE the Lean file was typed; re-run here as evidence.

For each theorem we (a) evaluate the quantity to 25 significant digits and
(b) check the shipped rational bracket contains it.  Exit code 0 iff all pass.
"""
import sympy as sp

PREC = 25
fails = []


def check(name, true_val, lo, hi):
    ok = sp.Rational(lo) < true_val < sp.Rational(hi)
    print(f"{'PASS' if ok else 'FAIL'}  {name}")
    print(f"        true = {sp.N(true_val, PREC)}   bracket = ({lo}, {hi})")
    if not ok:
        fails.append(name)


def check_eq(name, true_val, claimed):
    ok = sp.simplify(true_val - claimed) == 0
    print(f"{'PASS' if ok else 'FAIL'}  {name}")
    print(f"        true = {sp.simplify(true_val)}   claimed = {claimed}")
    if not ok:
        fails.append(name)


x, R = sp.symbols('x R', real=True)
X = (sp.sqrt(1 + 4 * x ** 2) - 1) / 2
xb = sp.sqrt(R * (1 + R))

# ---- (1) -------------------------------------------------------------------
check_eq("(1b) X x * (1 + X x) - x^2 = 0", sp.simplify(X * (1 + X) - x ** 2), 0)
# numeric spot-check of positivity at the four radii used later
for xv in ['21.45', '41.98', '60.00', '98.32']:
    v = X.subs(x, sp.Rational(xv))
    print(f"        X({xv}) = {sp.N(v, PREC)} > 0 : {v > 0}")
    if not v > 0:
        fails.append("(1a) X_pos")

# ---- (2) -------------------------------------------------------------------
Rb = sp.Rational(541, 100)
check_eq("(2) X(x_b(541/100)) = 541/100", X.subs(x, xb.subs(R, Rb)), Rb)
check("(2) x_b(541/100) bracket", xb.subs(R, Rb),
      sp.Rational('5.8887').p / sp.Rational('5.8887').q, None) if False else None
check("(2) window 5.8887 < x_break < 5.8889", xb.subs(R, Rb),
      sp.Rational(58887, 10000), sp.Rational(58889, 10000))
# the evenness that makes the one-sided "iff" false off x >= 0
print(f"        evenness check: X(-x_b) - X(x_b) = "
      f"{sp.simplify(X.subs(x, -xb.subs(R, Rb)) - X.subs(x, xb.subs(R, Rb)))}")

# ---- (3) -------------------------------------------------------------------
# NB: sympy will NOT simplify sqrt(4R(R+1)+1) to 2R+1 for a merely real R, because
# the branch requires 2R+1 >= 0.  The Lean proof supplies that via the hypothesis `0 < R`
# (lemma `X_x_b`, step `Real.sqrt_sq hpos`).  Audit numerically over positive R instead.
for Rv in ['1/1000', '1/7', '1', '541/100', '10', '12345/10']:
    v = (X.subs(x, xb) / R).subs(R, sp.Rational(Rv))
    check_eq(f"(3) X(x_b R)/R = 1 at R = {Rv}", sp.simplify(v), 1)

# ---- (4) -------------------------------------------------------------------
for xv, lo, hi, expect in [('21.45', '3.87', '3.88', '3.87'),
                           ('41.98', '7.66', '7.67', '7.67'),
                           ('60.00', '10.99', '11.00', '11.00'),
                           ('98.32', '18.08', '18.09', '18.08')]:
    v = X.subs(x, sp.Rational(xv)) / Rb
    check(f"(4) X({xv})/R_b  [expect ~{expect}]", v, lo, hi)

# ---- (5) -------------------------------------------------------------------
Xs, Dlow, Dhigh = sp.Rational(119, 2), sp.Rational(911, 1000), sp.Rational(7, 5)
check("(5) X_s/D_low bracket", Xs / Dlow, sp.Rational(653, 10), sp.Rational(654, 10))
check_eq("(5) X_s/D_high = 425/10", Xs / Dhigh, sp.Rational(425, 10))
check("(5) X_s/D_high bracket", Xs / Dhigh, sp.Rational(4249, 100), sp.Rational(4251, 100))

# ---- (6) -------------------------------------------------------------------
GN = sp.Rational(66743, 10 ** 15)
Sig = lambda a0: a0 / (sp.pi * GN * (xb.subs(R, Rb)) ** 2)
check("(6) Sigma canonical bracket", Sig(sp.Rational(93603, 10 ** 15)),
      sp.Rational(12872, 10 ** 6), sp.Rational(12874, 10 ** 6))
check("(6) Sigma alternative bracket", Sig(sp.Rational(11312, 10 ** 14)),
      sp.Rational(15557, 10 ** 6), sp.Rational(15558, 10 ** 6))

print()
print("ALL PASS" if not fails else f"FAILURES: {fails}")
raise SystemExit(0 if not fails else 1)
