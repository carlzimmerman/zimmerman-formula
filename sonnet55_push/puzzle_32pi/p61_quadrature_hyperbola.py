"""p61: the quadrature law is a unit hyperbola (rapidity form) -- the inverse relationship behind it, and what it says about kappa.
x = g/a0, y = g_N/a0, x^2 = y^2 + y  <=>  (2y+1)^2 - (2x)^2 = 1  <=>  2y + 1 = cosh(theta), 2x = sinh(theta).
  => g_N = a0 sinh^2(theta/2), g = (a0/2) sinh(theta), nu = g/g_N = coth(theta/2), phantom p = x - y = (1 - e^-theta)/2  (plateau 1/2 = 1 - e^-inf over 2).
  Inverse: e^theta = 2y + 1 + 2x (a 'Doppler factor'); theta -> -theta flips the sign of g only (the repulsive branch).
Equivalently g_N = sqrt(g^2 + a_L^2) - a_L with a_L = a0/2: EXACTLY Milgrom's 1999 de Sitter-Unruh form (inertia ~ T_Unruh-dS(g) - T_dS), with the dS acceleration a_L = a0/2.
So kappa = 1/2 <=> the MOND sector's de Sitter rate is H_M = a_L/c = (1/4) sqrt(G rho_Lambda), i.e. H_M^2 = G rho_Lambda/16, versus Friedmann's H^2 = (8 pi/3) G rho_Lambda.
Checks: Y the parametrisation satisfies x^2 = y^2 + y identically; M Milgrom-99 form with a_L = a0/2 equals the quadrature law; P phantom = (1 - e^-theta)/2;
  F the implied Friedmann coefficient is 1/16 (pi-free) and its ratio to 8 pi/3 is 3/(128 pi).
Run: python3 p61_quadrature_hyperbola.py | MUTATE=1 uses a_L = a0 (Milgrom's own normalisation) -> M fails
"""
import os, sys, sympy as sp
MUTATE = os.environ.get("MUTATE") == "1"
res = []
def check(n, ok): res.append(bool(ok)); print(("PASS  " if ok else "FAIL  ") + n)
th, g, a0, G, rho, c = sp.symbols("theta g a0 G rho c", positive=True)
x = sp.sinh(th) / 2; y = sp.sinh(th / 2)**2
check("Y x = sinh(theta)/2, y = sinh^2(theta/2) satisfies x^2 = y^2 + y", sp.simplify((x**2 - y**2 - y).rewrite(sp.exp)) == 0)
aL = a0 if MUTATE else a0 / 2
gN = sp.sqrt(g**2 + aL**2) - aL
check("M Milgrom-99 g_N = sqrt(g^2 + a_L^2) - a_L with a_L = a0/2 reproduces g^2 = g_N^2 + a0 g_N", sp.simplify(sp.expand(gN**2 + a0 * gN - g**2)) == 0)
check("P phantom p = x - y = (1 - e^-theta)/2", sp.simplify((x - y - (1 - sp.exp(-th)) / 2).rewrite(sp.exp)) == 0)
kap = sp.Rational(1, 2)
HM2 = sp.simplify((kap * c * sp.sqrt(G * rho) / 2 / c)**2)
coef = sp.simplify(HM2 / (G * rho)); ratio = sp.simplify(coef / (sp.Rational(8, 3) * sp.pi))
print(f"   H_M^2 = {HM2}  -> Friedmann-type coefficient {coef} vs 8 pi/3; ratio {ratio}")
check("F kappa = 1/2 means H_M^2 = G rho/16 (pi-free), ratio to Friedmann = 3/(128 pi)", coef == sp.Rational(1, 16) and sp.simplify(ratio - 3 / (128 * sp.pi)) == 0)
print(f"\n{sum(res)}/{len(res)} pass" + ("  (MUTATE)" if MUTATE else ""))
sys.exit(0 if all(res) else 1)
