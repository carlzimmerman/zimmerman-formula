#!/usr/bin/env python3
"""AH5 -- dimensional obstruction to deriving alpha from (c, G, Lambda [, hbar]).  Pre-registered in AH5_DIMENSIONAL_OBSTRUCTION.md.

Buckingham pi with exact rational arithmetic: dimensionless groups = nullspace of the dimension matrix over (M, L, T).
Run: python3 ah5_dimensional_obstruction.py
"""
import math
import sympy as sp

CHECKS = []


def check(tag, ok, detail=""):
    CHECKS.append((tag, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {tag} {detail}")


# dimension exponents (M, L, T)
DIM = {
    "c": (0, 1, -1),          # length / time
    "G": (-1, 3, -2),         # length^3 / (mass time^2)
    "Lambda": (0, -2, 0),     # length^-2
    "hbar": (1, 2, -1),       # mass length^2 / time
    "e2": (1, 3, -2),         # Gaussian e^2: energy x length
}


def nullspace(names):
    A = sp.Matrix([[DIM[n][i] for n in names] for i in range(3)])
    return A.nullspace()


def integerize(v):
    den = sp.ilcm(*[sp.fraction(x)[1] for x in v])
    w = [x * den for x in v]
    g = sp.igcd(*[int(x) for x in w])
    return [int(x) // g for x in w]


print("=" * 100)
print("AH5 dimensional obstruction (exact rational Buckingham pi)")
print("=" * 100)

print("\nD1  {c, G, Lambda}")
ns1 = nullspace(["c", "G", "Lambda"])
print(f"    dimensionless groups: {len(ns1)}")
check("D1 no dimensionless number from (c, G, Lambda)", len(ns1) == 0)

print("\nD2  {c, G, Lambda, hbar}")
names2 = ["c", "G", "Lambda", "hbar"]
ns2 = nullspace(names2)
grp = integerize(ns2[0]) if ns2 else None
print(f"    dimensionless groups: {len(ns2)};  exponent vector on {names2}: {grp}")
expected = {"c": -3, "G": 1, "Lambda": 1, "hbar": 1}         # Lambda G hbar / c^3
ok2 = len(ns2) == 1 and all(abs(grp[i]) == abs(expected[n]) and (grp[i] * expected[n] > 0) == (grp[0] * expected["c"] > 0)
                            for i, n in enumerate(names2))
check("D2 exactly one group, x = Lambda G hbar / c^3 = Lambda l_P^2", ok2)

print("\nD3  {c, G, Lambda, hbar, e^2}")
names3 = ["c", "G", "Lambda", "hbar", "e2"]
ns3 = nullspace(names3)
print(f"    dimensionless groups: {len(ns3)}")
basis = [integerize(v) for v in ns3]
for b in basis:
    print(f"    basis vector on {names3}: {b}")
alpha_vec = [-1, 0, 0, -1, 1]                                  # e^2 / (hbar c): c^-1 hbar^-1 e2^1
alpha_vec = [-1 if n == "c" else (-1 if n == "hbar" else (1 if n == "e2" else 0)) for n in names3]
A3 = sp.Matrix([[DIM[n][i] for n in names3] for i in range(3)])
in_null = (A3 * sp.Matrix(alpha_vec)).is_zero_matrix
print(f"    alpha = e^2/(hbar c): exponent vector {alpha_vec}; dimensionless: {in_null}")
x_vec = [-3, 1, 1, 1, 0]
# is alpha a rational multiple of any monomial in the gravity groups?  test whether alpha_vec lies in span{x_vec} (it cannot: e^2 exponent)
span_test = sp.Matrix.hstack(sp.Matrix(x_vec), sp.Matrix(alpha_vec)).rank()
check("D3 two groups; alpha is dimensionless and is NOT a power of x (rank of {x, alpha} = 2)",
      len(ns3) == 2 and in_null and span_test == 2, f"(rank {span_test})")

print("\nD4  numbers (report only)")
c = 299792458.0
G = 6.67430e-11
hbar = 1.054571817e-34
H0 = 67.4e3 / 3.0856775814913673e22
OmL = 0.6847
Lam = 3 * OmL * H0 ** 2 / c ** 2
lP2 = G * hbar / c ** 3
x = Lam * lP2
alpha = 1 / 137.035999177
print(f"    Lambda = {Lam:.4e} m^-2;  l_P^2 = {lP2:.4e} m^2;  x = Lambda l_P^2 = {x:.4e};  ln(1/x) = {math.log(1 / x):.4f}")
print("    parameter each family would need to hit alpha = 1/137.035999177 (REPORT ONLY, none scored):")
print(f"      alpha = x^p:              p = ln(alpha)/ln(x) = {math.log(alpha) / math.log(x):.6f}")
print(f"      1/alpha = a ln(1/x):      a = {(1 / alpha) / math.log(1 / x):.6f}")
print(f"      1/alpha = b ln(1/sqrt x): b = {(1 / alpha) / math.log(1 / math.sqrt(x)):.6f}")
print("    (a one-parameter family can always hit one number; a hit is evidence only if the family has no free parameter and is forced)")
check("D4 x is a single number ~ 3e-122 (the only gravity-cosmology dimensionless group)", 1e-123 < x < 1e-121, f"(x = {x:.3e})")

print("\n" + "=" * 100)
passed = sum(1 for _, ok in CHECKS if ok)
print(f"CHECKS: {passed}/{len(CHECKS)} passed")
print("CONCLUSION: within (c, G, Lambda, hbar) the ONLY dimensionless number is x = Lambda l_P^2 ~ 3e-122; alpha is an independent second group once a charge is")
print("  present. So the a0 chain (no hbar, no charge) cannot output alpha, and any derivation from these inputs is an explicit function f with f(x) = 1/137.036.")
print("  A derivation therefore needs a NEW charge-quantization principle (e no longer independent) or a forced f. Structural statement, not a no-go on all physics.")
raise SystemExit(0 if passed == len(CHECKS) else 1)
