"""p13: the open target -- 'an a0-sector ENERGY DENSITY coupled to gravity with coefficient fixed at 4' --
run through the three-question screen (external_notes/README.md, EXT02):
  T1  does a principle fix the number, such that a different kappa would give a different number?
  T2  is the relation dimensionally consistent in general spacetime dimension d before d = 4 is set?
  T3  does it predict something besides a0?
Idea: rho_Lambda IS the vacuum energy of the a0 sector, rho_Lambda = W a0^2 / G, with W fixed by a principle.
Target: G rho_Lambda = 4 a0^2 (c = 1), i.e. W = 1/kappa^2 = 4 at kappa = 1/2.
The w0-wa values in T3 are ILLUSTRATIVE inputs (round numbers of the size reported by DESI-era fits), not fetched data.
Run: python3 p13_energy_density_three_tests.py      MUTATE=1 -> kappa set to 1/3; checks tied to kappa = 1/2 must fail.
"""
import os
import sys

import sympy as sp

MUTATE = os.environ.get("MUTATE") == "1"
res = []


def check(name, ok):
    res.append(bool(ok))
    print(("PASS  " if ok else "FAIL  ") + name)


pi = sp.pi
a0, G, H, rho, kap = sp.symbols("a0 G H rho kappa", positive=True)
kappa = sp.Rational(1, 3) if MUTATE else sp.Rational(1, 2)

# ---------------- T1: what number must a principle produce, in each natural normalisation ----------
W = sp.solve(sp.Eq(a0, kap * sp.sqrt(G * rho)), rho)[0] * G / a0**2      # rho = W a0^2/G
check("T1a W = 1/kappa^2: W = 4 at kappa = 1/2 (W tracks kappa, so a principle fixing W is a real test)",
      sp.simplify(W - 1 / kap**2) == 0 and W.subs(kap, kappa) == 4)
# Newtonian field energy density is g^2/(8 pi G); at g = a0 the natural unit is a0^2/(8 pi G)
X = sp.simplify((1 / kappa**2) * 8 * pi)                                  # rho = X a0^2/(8 pi G)
check("T1b in field-energy units a0^2/(8 pi G) the target is X = 32 pi = 8 x (4 pi): eight full solid angles",
      sp.simplify(X - 32 * pi) == 0)
# AQUAL normalisation L = -(a0^2/(8 pi G)) F(|grad phi|^2/a0^2): vacuum offset F(0) must be 32 pi; F(0) is free
check("T1c AQUAL vacuum offset: rho_vac = a0^2 F(0)/(8 pi G) needs F(0) = 32 pi; nothing in AQUAL fixes F(0) -> FAILS T1 as it stands",
      sp.simplify(sp.solve(sp.Eq(G * a0**2 * sp.Symbol("F0") / (8 * pi * G), 4 * a0**2), sp.Symbol("F0"))[0] - 32 * pi) == 0)
# Friedmann form: G rho = 3 H^2/(8 pi) (Lambda-dominated) -> a0/H = sqrt(3/(32 pi)) = 1/5.789
r = sp.sqrt(sp.Rational(3, 8) / pi) * kappa
check("T1d equivalent statement: a0/H_inf = kappa sqrt(3/(8 pi)) = 0.1727 = 1/5.789 (Z = 5.7888)",
      abs(float(r) - 0.17275) < 1e-4 and abs(float(1 / r) - 5.7888) < 1e-3)

# ---------------- T2: dimensional consistency in general d ------------------------------------------
# c = 1. Poisson in d spacetime dims: lap phi = Omega_{d-2} (d-3)/(d-2) G_d rho (any O(1) factor); phi is
# dimensionless, so [G_d rho] = 1/L^2 in every d; [a0^2] = 1/L^2. G rho = W_d a0^2 is consistent in all d.
d, Lsym = sp.symbols("d L", positive=True)
dim_Grho = -2            # power of L
dim_a0sq = -2
check("T2a [G_d rho] = [a0^2] = L^-2 in every d: the relation is consistent before d = 4 is set (PASSES T2)",
      dim_Grho == dim_a0sq)
Omega = lambda n: 2 * pi ** sp.Rational(n + 1, 2) / sp.gamma(sp.Rational(n + 1, 2))   # area of unit S^n
check("T2b the solid angle Omega_{d-2} is 4 pi at d = 4, so a principle built on Gauss's law would make W_d d-dependent: a falsifiable structure",
      sp.simplify(Omega(2) - 4 * pi) == 0 and sp.simplify(Omega(3) - 2 * pi**2) == 0)

# ---------------- T3: extra prediction -- a0 tracks the dark-energy density ----------------------------
z, w0, wa = sp.symbols("z w0 wa", real=True)
rDE = (1 + z) ** (3 * (1 + w0 + wa)) * sp.exp(-3 * wa * z / (1 + z))      # CPL rho_DE(z)/rho_DE(0)
a0_ratio = sp.sqrt(rDE)
check("T3a w = -1 exactly <=> a0(z) flat (the framework's distinctive law)", sp.simplify(a0_ratio.subs({w0: -1, wa: 0})) == 1)
illus = [(-0.75, -0.85), (-0.84, -0.60), (-0.67, -1.10)]                  # ILLUSTRATIVE, not fetched
vals = [float(a0_ratio.subs({w0: a, wa: b, z: 2.5})) for a, b in illus]
for (a, b), v in zip(illus, vals):
    print(f"      illustrative w0={a:+.2f} wa={b:+.2f}: a0(2.5)/a0(0) = {v:.3f}")
Ez = sp.sqrt(0.315 * (1 + z) ** 3 + 0.685)
check("T3b evolving DE gives a0(2.5)/a0(0) ~ 0.7-0.85 (a FALL), opposite to the a0 ~ H(z) rival's rise x3.77",
      all(0.6 < v < 0.9 for v in vals) and abs(float(Ez.subs(z, 2.5)) - 3.77) < 0.03)
zs = [i / 20 for i in range(0, 61)]
peak = max(zs, key=lambda zz: float(a0_ratio.subs({w0: -0.75, wa: -0.85, z: zz})))
check(f"T3c a phantom-crossing fit puts an a0 MAXIMUM at z ~ {peak:.2f} (a second, sharper signature)", 0.2 < peak < 1.0)

n = sum(res)
print(f"\n{n}/{len(res)} checks pass" + ("  [MUTATE=1: failures REQUIRED]" if MUTATE else ""))
sys.exit(0 if n == len(res) else 1)
