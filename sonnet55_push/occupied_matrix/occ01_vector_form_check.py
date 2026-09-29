#!/usr/bin/env python3
"""occ01_vector_form_check.py -- is the N-carrier VECTOR form of the CA5-GNC-R occupied reduced action right?

real_research/breakthrough_review_2026_09_26/occupied/check.py verifies the reduced scalar action for ONE carrier
field (chi, v, Vp, Vpp scalars). RESULT.md then states the boxed VECTOR form (J, F_d, G) for N fields. The
five-field action has N = 5, so the vector form is what a finite-k matrix needs. This script rebuilds the reduced
action for N = 2 carriers straight from the same primitive pieces (shift block, U/Z auxiliary block, projected
matter jets, spatial term), eliminating beta, U, Z, then phi, and compares with the boxed vector formula
symbolically. Same primitives, generalised dot products; nothing else is assumed.

Exit 0 = every exact identity held.
"""
import sys
import sympy as s

ok = []
def check(name, expr):
    z = s.simplify(s.expand(expr))
    good = (z == 0)
    ok.append(good)
    print(f"  [{'OK' if good else 'FAIL'}] {name}" + ("" if good else f"   residual = {z}"))

M, H, c2, x, alpha, r, V0 = s.symbols('M H c2 x alpha r V0', positive=True)
psi, pd, phi, beta, Z, U = s.symbols('psi pd phi beta Z U', real=True)
V = s.Symbol('V', nonnegative=True)
v = s.Matrix(s.symbols('v1 v2', real=True))
chi = s.Matrix(s.symbols('chi1 chi2', real=True))
cd = s.Matrix(s.symbols('cd1 cd2', real=True))
Vp = s.Matrix(s.symbols('Vp1 Vp2', real=True))
a_, b_, c_ = s.symbols('Vpp_a Vpp_b Vpp_c', real=True)
Vpp = s.Matrix([[a_, b_], [b_, c_]])
dot = lambda p, q: (p.T * q)[0, 0]

T = dot(v, v) / 2
Q = 1 - r
cN = 1 - alpha / 2
K = 2 * (2 + 3 * c2) / c2
ae = 2 - (2 - alpha) * Q**2
f1 = f2 = 0                                          # CA5-GNC-R: reciprocal barrier, both jets zero

ss = pd + H * phi
shiftblock = M / 2 * (-6 * ss**2 + 4 * x * beta * ss - c2 * (3 * ss - x * beta)**2) - x * beta * dot(v, chi)
aux = M * x / 2 * (alpha * (phi - Z)**2 + 4 * phi * Z - 2 * Z * Z - 4 * cN * Z * U + 4 * cN * r * phi * U)
rest = (dot(cd, cd) / 2 + dot(v, cd) * (Z - phi) + 3 * dot(v, chi) * pd + T * phi**2
        + (V - T - V0 * f1) * phi * Z - (V + V0 * f2 / 2) * Z * Z
        + dot(Vp, chi) * (Z - phi) - dot(chi, (x * s.eye(2) + Vpp) * chi) / 2)
spatial = M * x * psi**2 - 2 * M * x * phi * psi
full = shiftblock + aux + rest + spatial

betastar = ((3 + 2 / c2) * ss - dot(v, chi) / (M * c2)) / x
check("beta stationarity (vector)", s.diff(full, beta).subs(beta, betastar))
check("U constraint gives Z = r phi (vector)", s.diff(full, U).subs(Z, r * phi))
red = full.subs(beta, betastar).subs(Z, r * phi)

Delta = ae * x + 2 * (T + (V - T - V0 * f1) * r - (V + V0 * f2 / 2) * r * r) / M
Fd = K * H * H + Delta
source = (M * K * H * pd - Q * dot(v, cd) - 2 * M * x * psi
          - H * (3 + 2 / c2) * dot(v, chi) - Q * dot(Vp, chi))
base = (M * K * pd**2 / 2 + dot(cd, cd) / 2 - 2 * pd * dot(v, chi) / c2 + dot(v, chi)**2 / (2 * M * c2)
        - dot(chi, (x * s.eye(2) + Vpp) * chi) / 2 + M * x * psi**2)

check("reduced action = base + phi*source + M*F_d*phi^2/2 (vector)",
      red - (base + phi * source + M * Fd * phi**2 / 2))
phistar = -source / (M * Fd)
final = base - source**2 / (2 * M * Fd)
check("lapse elimination gives the boxed L_red (vector)",
      (base + phi * source + M * Fd * phi**2 / 2).subs(phi, phistar) - final)

# the positive-definiteness relation D = Delta - 2 T Q^2 / M (vector T)
Dkin = ae * x + 2 * r * (Q * (T + V) - V0 * (f1 + f2 * r / 2)) / M
check("D identity: Delta - Q^2 v.v/M = D (vector)", Delta - Q**2 * dot(v, v) / M - Dkin)

print(f"\n  {sum(ok)}/{len(ok)} identities held")
sys.exit(0 if all(ok) else 1)
