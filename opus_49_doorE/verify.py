#!/usr/bin/env python3
"""
opus_49_doorE / verify.py -- EXPLICIT-X_d hunt arithmetic (2026-09-22).

What this verifies (machine-checked, runnable):
  (1) The exact values of A_d = (32/3)*d*(d-1)/2 used by the parent bridge
      (i15/PROOF.md, Sec. 4: "A_d = (32/3) d(d-1)/2", i.e. (32/3)*C(d,2)).
  (2) The algebraic consolidation of the parent's threshold formula
          X_d = max(1,  sqrt(2*A_d/c1),  sqrt(2*c2*A_d) )
      into the single-parameter family
          X_d = max(1, sqrt(2*A_d/theta)),  theta := min(c1, 1/c2).
      Derivation: the two Yarotsky conditions are
          eta <= A_d/x^2 <= c1/2   (half-margin version of eta < c1)
      and
          c2*eta <= c2*A_d/x^2 <= 1/2,
      i.e. x^2 >= 2*A_d/c1  AND  x^2 >= 2*c2*A_d, so x^2 >= 2*A_d*max(1/c1, c2)
      = 2*A_d/min(c1, 1/c2).  max(sqrt(2A_d/c1), sqrt(2c2 A_d)) = sqrt(2A_d/theta)
      is checked numerically below for many random (c1, c2) pairs.
  (3) HOWEVER: theta = min(c1, 1/c2) is UNKNOWN in every accessible source
      (see REPORT.md).  Nothing numeric is claimed for c1, c2, or X_d.
      The sweep in section (4) uses EXPLICITLY LABELLED hypothetical theta
      values, purely to display the functional shape X_d ~ sqrt(2A_d/theta);
      it is NOT a claim that any of those theta values is the true one.

House rule: no fabricated constants.  This file outputs the parametric
result and the sensitivity SHAPE only.
"""
from fractions import Fraction
import math, random

ok = True

# ---- (1) exact A_d --------------------------------------------------------
print("== (1) exact A_d = (32/3)*d*(d-1)/2 ==")
A = {}
for d in [2, 3, 4, 5, 6, 8]:
    A[d] = Fraction(32, 3) * d * (d - 1) // 2
    # careful: Fraction(32,3) * (d*(d-1)//2) exactly
    A[d] = Fraction(32 * d * (d - 1), 3 * 2)
    print(f"  d={d}: A_d = {A[d]} = {float(A[d]):.6f}")
assert A[2] == Fraction(32, 3), "A_2 must be 32/3 = (32/3)*C(2,2)"
assert A[3] == Fraction(32, 1), "A_3 must be 32"
assert A[4] == Fraction(64, 1), "A_4 must be 64"
assert A[6] == Fraction(160, 1), "A_6 must be 160"
print("  exact values OK")

# ---- (2) consolidation identity ------------------------------------------
print("== (2) consolidation: sqrt(2A_d/c1) vs sqrt(2c2 A_d) -> sqrt(2A_d/theta) ==")
random.seed(49)
for _ in range(200000):
    c1 = 10 ** random.uniform(-6, 2)
    c2 = 10 ** random.uniform(-6, 2)
    theta = min(c1, 1.0 / c2)
    for d in (2, 3, 4):
        ad = float(A[d])
        lhs = max(math.sqrt(2 * ad / c1), math.sqrt(2 * c2 * ad))
        rhs = math.sqrt(2 * ad / theta)
        if abs(lhs - rhs) > 1e-9 * max(1.0, lhs):
            ok = False
            print("  MISMATCH", c1, c2, d, lhs, rhs)
print("  200000 random (c1,c2) pairs: identity holds" if ok else "  FAILED")
assert ok

# also verify the two source conditions directly at x = sqrt(2A_d/theta)
for _ in range(5000):
    c1 = 10 ** random.uniform(-5, 1)
    c2 = 10 ** random.uniform(-5, 1)
    theta = min(c1, 1.0 / c2)
    for d in (2, 3, 4):
        ad = float(A[d])
        x = math.sqrt(2 * ad / theta)
        eta = ad / (x * x)          # eta <= A_d/x^2
        assert eta <= c1 / 2 + 1e-12
        assert c2 * eta <= 0.5 + 1e-12
print("  at x=sqrt(2A_d/theta): eta<=c1/2 and c2*eta<=1/2 hold (machine-checked)")

# ---- (3) what the numeric value would look like: sensitivity SHAPE --------
print("== (3) sensitivity shape (LABELLED HYPOTHETICAL theta; NOT claimed) ==")
print("  X_d(theta) = max(1, sqrt(2A_d/theta)); a 1e4 change in theta moves X_d by 1e2")
hypothetical = [1e-6, 1e-4, 1e-2, 1e0, 1e2]
print("  theta (hypothetical)   X_2        X_3        X_4")
for th in hypothetical:
    row = []
    for d in (2, 3, 4):
        row.append(f"{max(1.0, math.sqrt(2*float(A[d])/th)):9.4f}")
    print(f"  {th:6.0e}              {row[0]}   {row[1]}   {row[2]}")
print("  NOTE: no theta on this table is sourced from Yarotsky or any paper;")
print("  the table exists only to show the sqrt(1/theta) shape (report Sec. 4).")

print("\nALL CHECKS PASSED" if ok else "CHECKS FAILED")