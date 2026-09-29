#!/usr/bin/env python3
"""p04_equivalence_web.py -- the repo states the one open number kappa = 1/2 in many different-looking ways.  Prove they are ONE statement.

Define a0 = kappa c sqrt(G rho_L) with rho_L the vacuum energy density (Lambda = 8 pi G rho_L/c^2).  Each formulation below is turned into an
equation in kappa (or in its own parameters) and solved; every one has the unique positive solution kappa = 1/2.  A derivation of ANY of them
derives all of them; a proof of none of them is a proof that none has been derived.  Sources are the repo documents named in the table.

Part B: the repo's 'Z^2 = 8 x (volume of the unit 3-ball)' reading is tested against the dimension-covariant Friedmann form Z_d^2 = 64 pi/(d(d-1)).
Exit 0 = all equivalences verified and the controls behave.
"""
import math
import sys
import sympy as sp

ok = []
def check(name, cond):
    ok.append(bool(cond)); print(f"  [{'OK' if cond else 'FAIL'}] {name}")

k, G, rho, c = sp.symbols('kappa G rho c', positive=True)
a0 = k * c * sp.sqrt(G * rho)
Lam = 8 * sp.pi * G * rho / c**2
half = sp.Rational(1, 2)

def solves_to_half(eq, var=k):
    sols = [s for s in sp.solve(eq, var) if s.is_positive]
    return len(sols) == 1 and sp.simplify(sols[0] - half) == 0

print("PART A  ten formulations, one statement (each is solved for its own unknown; the unique positive root is kappa = 1/2)")
rows = []
# 1  the puzzle
rows.append(("Lambda = 32 pi a0^2 / c^4", "the puzzle; CFG47/README", solves_to_half(sp.Eq(Lam, 32 * sp.pi * a0**2 / c**4))))
# 2  area x Lambda with the Schwarzschild horizon of surface gravity a0
rsw = c**2 / (2 * a0); Aw = 4 * sp.pi * rsw**2
rows.append(("A Lambda = 32 pi^2, A = 4 pi r_s^2, kappa_S = c^2/(2 r_s) = a0", "the puzzle", solves_to_half(sp.Eq(Aw * Lam, 32 * sp.pi**2))))
# 3  curvature = density
rows.append(("horizon Gauss curvature 1/r_s^2 = G rho_L/c^2", "p01/p02 (this folder)", solves_to_half(sp.Eq(1 / rsw**2, G * rho / c**2))))
# 4  Rindler length = 2 x free-fall length
rows.append(("Rindler length c^2/a0 = 2 R*,  R* = c/sqrt(G rho_L)", "GEOMETRIC_EQUATIONS_SYNTHESIS Part 1 ('free-fall horizon at R*')", solves_to_half(sp.Eq(c**2 / a0, 2 * c / sp.sqrt(G * rho)))))
# 5  unit response  2 p'(0) = 1/kappa
pp = sp.symbols('pprime', positive=True)
rows.append(("unit response p'(0) = 1  with  2 p'(0) = 1/kappa", "real_research/reviews/kappa_unit_response_2026_09_20/ACTION_ROUTE.md", solves_to_half(sp.Eq(1 / (2 * k), 1))))
# 6  memory moment  M1 = 2c/(3 a0) = (4/3) t_L
t = 1 / sp.sqrt(G * rho)
rows.append(("memory first moment M1 = 2c/(3 a0) = (4/3) t_L", "prep_2026 / REV_kappa_memory_moment_dimension (Lean)", solves_to_half(sp.Eq(2 * c / (3 * a0), sp.Rational(4, 3) * t))))
# 7  four-form normalisation: kappa^2 = 2 beta^2/(Z + 2 b beta^2) = 1/4  <=>  Z + 2 b beta^2 = 8 beta^2
beta, Zq, b = sp.symbols('beta Z_q b', positive=True)
kap2 = 2 * beta**2 / (Zq + 2 * b * beta**2)
ok7 = sp.simplify(sp.solve(sp.Eq(kap2, sp.Rational(1, 4)), Zq)[0] - (8 * beta**2 - 2 * b * beta**2)) == 0
rows.append(("four-form: Z_q + 2 b beta^2 = 8 beta^2  (Z_q/beta^2 = 8 - 2b)", "FOURFORM_A0_REPORT; ACTION_ROUTE", ok7))
# 8  Unruh matching with n modes: kappa_match = sqrt(8 pi/3)/n = 1/2  <=>  n = Z = sqrt(32 pi/3)
n = sp.symbols('n', positive=True)
ok8 = sp.simplify(sp.solve(sp.Eq(sp.sqrt(8 * sp.pi / 3) / n, half), n)[0] - sp.sqrt(32 * sp.pi / 3)) == 0
rows.append(("Unruh = de Sitter matching with n modes: n = Z = sqrt(32 pi/3)", "CFG47 (ChainCert/ALPHA_CFG47 Lean)", ok8))
# 9  Z = 2 sqrt(8 pi/3)
Zs = sp.symbols('Z', positive=True)
rows.append(("Z = c H_L / a0 = 2 sqrt(8 pi/3)  (H_L^2 = 8 pi G rho_L/3)", "Z-derivation verdict 2026-06-15; STANDING", solves_to_half(sp.Eq(c * sp.sqrt(8 * sp.pi * G * rho / 3) / a0, 2 * sp.sqrt(8 * sp.pi / 3)))))
# 10 cosmology lock Omega_L = 32 pi a0^2/(3 H0^2 c^2)
H0, OL = sp.symbols('H0 Omega_L', positive=True)
rho_crit = 3 * H0**2 / (8 * sp.pi * G)
a0_lock = k * c * sp.sqrt(G * OL * rho_crit)
rows.append(("Omega_Lambda = 32 pi a0^2/(3 H0^2 c^2)  (a0 and dark energy are one measurement)", "GEOMETRIC_EQUATIONS_SYNTHESIS", solves_to_half(sp.Eq(OL, 32 * sp.pi * a0_lock**2 / (3 * H0**2 * c**2)))))
for i, (name, src, good) in enumerate(rows, 1):
    check(f"{i:>2}  {name}   [{src}]", good)

print("\n  classification (what kind of statement each one is):")
kinds = {1: "dimensionless relation between two scales", 2: "same, via a horizon area", 3: "curvature of a horizon = an energy density", 4: "two lengths: Rindler vs free-fall",
         5: "a response coefficient of the interpolation function", 6: "a moment of the memory kernel", 7: "a ratio of two normalisations of one field",
         8: "an integer-like mode count that is not an integer", 9: "a coefficient in front of the Friedmann number", 10: "the same, on the cosmological measurement"}
for i in range(1, 11):
    print(f"      {i:>2}  {kinds[i]}")

# control: a wrong value must be rejected by the same solver
ok_ctl = not solves_to_half(sp.Eq(Lam, 16 * sp.pi * a0**2 / c**4))
check("C1  control: Lambda = 16 pi a0^2/c^4 (a wrong coefficient) does NOT give kappa = 1/2 (it gives kappa = 1/sqrt 2)", ok_ctl)

# ----------------------------------------------------------------------------- Part B
print("\nPART B  is 'Z^2 = 8 x Vol(B^3)' structural, or a d = 3 coincidence?  (dimension-covariant Friedmann form: H^2 = 16 pi G rho/(d(d-1)))")
print(f"  {'d':>3}{'Z_d^2 = 64 pi/(d(d-1))':>26}{'= 32 pi/dim SO(d)':>20}{'8 Vol(B^d)':>14}{'equal?':>9}")
hits = []
for d in range(2, 8):
    zd2 = 64 * math.pi / (d * (d - 1))
    vb = math.pi**(d / 2) / math.gamma(d / 2 + 1)
    eq = abs(zd2 - 8 * vb) < 1e-9
    hits.append(eq)
    print(f"  {d:>3}{zd2:>26.4f}{32 * math.pi / (d * (d - 1) / 2):>20.4f}{8 * vb:>14.4f}{'yes' if eq else 'no':>9}")
check("B1  Z_d^2 = 64 pi/(d(d-1)) equals 8 Vol(B^d) ONLY at d = 3: the 'ball volume' reading is a d = 3 coincidence, the Friedmann form is the structural one", hits == [d == 3 for d in range(2, 8)])
check("B2  Z_d^2 = 32 pi/dim SO(d) identically (dim SO(d) = d(d-1)/2): the '3' is the number of independent 2-planes of the spatial slice", all(abs(64 * math.pi / (d * (d - 1)) - 32 * math.pi / (d * (d - 1) / 2)) < 1e-12 for d in range(2, 8)))
print(f"\n  {sum(ok)}/{len(ok)} checks held.")
sys.exit(0 if all(ok) else 1)
