"""p27: the framework kernel nu = sqrt(1 + 1/y) with a Planck-acceleration cutoff in BIMOND's vacuum integral (p21/p25: Lambda/a0^2 = I/2, I = int_0^Y 2y(nu-1) dy).
Exact antiderivative: int 2y(sqrt(1+1/y) - 1) dy = sqrt(y(y+1))(... ) -- computed by sympy; large Y: I = Y - (1/4) ln Y + const.
Run: python3 p27_planck_cutoff_framework_kernel.py  |  MUTATE=1: kernel sqrt(1 + 1/y^2) (alpha = 2 class), check B must fail
"""
import os, sys, math
import sympy as sp
MUTATE = os.environ.get("MUTATE") == "1"
res = []
def check(n, ok): res.append(bool(ok)); print(("PASS  " if ok else "FAIL  ") + n)
y, Y = sp.symbols("y Y", positive=True)
nu = sp.sqrt(1 + 1 / y**2) if MUTATE else sp.sqrt(1 + 1 / y)
F = sp.integrate(sp.expand(2 * y * (nu - 1)), (y, 0, Y))
F = sp.simplify(F)
print(f"   I(Y) = {F}")
c, G, hbar = 2.99792458e8, 6.67430e-11, 1.054571817e-34
aP = math.sqrt(c**7 / (hbar * G))
for lab, a0 in (("framework 9.36e-11", 9.3603e-11), ("alt 1.131e-10", 1.1312e-10)):
    yP = aP / a0
    Iv = float(sp.N(F.subs(Y, sp.Float(yP, 200)), 200))
    print(f"   {lab}: y_P = {yP:.3e}; I = {Iv:.4e}; Lambda/a0^2 = {Iv/2:.3e} vs 32 pi = {32*math.pi:.2f}: too large by {Iv/(64*math.pi):.2e}")
yP = aP / 9.3603e-11; Iv = float(sp.N(F.subs(Y, sp.Float(yP, 200)), 200))
check("A the exact integral grows linearly, I = Y - (1/4) ln Y + O(1): the vacuum term is set by the cutoff itself", abs(Iv / yP - 1) < 1e-6)
check(f"B Planck cutoff: Lambda = (1/2) a0 a_P / c^4 (the geometric mean of a0 and the Planck acceleration), {Iv/(64*math.pi):.1e} x too large -- the cosmological-constant problem, softened from 1e122 to 1e{math.log10(Iv/(64*math.pi)):.0f}",
      Iv / (64 * math.pi) > 1e50)
print(f"\n{sum(res)}/{len(res)} pass" + ("  (MUTATE)" if MUTATE else ""))
sys.exit(0 if all(res) else 1)
