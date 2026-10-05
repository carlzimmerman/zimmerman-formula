"""p23: horizons of BIMOND's auxiliary metric g-hat (the a0 sector's own metric). Milgrom 2009 (arXiv:0912.0790v2) eq (24) at kappa = 1, f(1) = 1:
   Lambda   = -(1/2)(1 + f'(1)) a0^2 M(0)      (our metric g)
   Lambdahat = -(1/2)(f'(1) - 1) a0^2 M(0)      (g-hat; [kappa^-1 f]' = -1 + f'(1) at kappa = 1; the kappa^3 prefactor is 1)
Vacuum horizons of g-hat are SdS-type in Lambdahat: 1 - 2 kappa r = Lambdahat r^2 (B3), so Lambdahat r^2 <= 3 (cosmological), <= 1 (black hole).
Target: a g-hat horizon with kappa r = 1/2 and Lambda r^2 = 8 pi (Lambda of OUR metric).  G = c = 1.
Run: python3 p23_bimond_aux_metric_horizon.py  |  MUTATE=1: Lambdahat with (f'(1) + 1) (no sign difference between sectors); check A must fail
"""
import os, sys
import sympy as sp
MUTATE = os.environ.get("MUTATE") == "1"
fp, M0, a0, r = sp.symbols("fp M0 a0 r", real=True)
res = []
def check(n, ok): res.append(bool(ok)); print(("PASS  " if ok else "FAIL  ") + n)
Lam = -sp.Rational(1, 2) * (1 + fp) * a0**2 * M0
Lamh = -sp.Rational(1, 2) * ((fp + 1) if MUTATE else (fp - 1)) * a0**2 * M0
# kappa r = 1/2 on an SdS-type horizon of g-hat:  1 - 2 (1/2) = Lamh r^2  ->  Lamh r^2 = 0  ->  Lamh = 0
need = sp.solve(sp.Eq(Lamh, 0), fp)
print(f"   kappa r = 1/2 on a g-hat horizon needs Lambdahat = 0, i.e. f'(1) = {need}; then Lambda = {sp.simplify(Lam.subs(fp, need[0]))}")
check("A kappa r = 1/2 forces Lambdahat = 0, i.e. the free slope f'(1) = 1 (a choice, not fixed by the theory)", need == [1])
# with Lambdahat = 0, g-hat admits plain Schwarzschild holes of ANY mass; Lambda r^2 = 8 pi picks one mass
m = sp.symbols("m", positive=True); L = sp.symbols("Lambda", positive=True)
msol = sp.solve(sp.Eq(L * (2 * m)**2, 8 * sp.pi), m)
print(f"   then Lambda r_s^2 = 8 pi selects the hole of mass m = {msol} (r_s = 2m); kappa = a0 selects m = 1/(4 a0)")
both = sp.solve(sp.Eq(sp.Rational(1, 4) / a0, msol[0]), L)
print(f"   requiring both on one hole gives Lambda = {both}, i.e. Lambda = 32 pi a0^2 -- the puzzle itself, assumed, not derived")
check("B on that hole the two conditions together ARE Lambda = 32 pi a0^2 (restatement): the mass is chosen, nothing selects it",
      len(both) == 1 and sp.simplify(both[0] - 32 * sp.pi * a0**2) == 0)
# and Lambda itself is then a0^2 M(0): with f'(1) = 1, Lambda = -a0^2 M(0) -> 32 pi needs M(0) = -32 pi (the tail integral I_nu = 32 pi, p21/p22)
check("C with f'(1) = 1, Lambda = -a0^2 M(0), so 32 pi still needs I_nu = 32 pi: the p22 tail tuning again", sp.simplify(Lam.subs(fp, 1) + a0**2 * M0) == 0)
print(f"\n{sum(res)}/{len(res)} pass" + ("  (MUTATE)" if MUTATE else ""))
sys.exit(0 if all(res) else 1)
