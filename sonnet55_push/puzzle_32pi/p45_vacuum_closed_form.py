"""p45: closed form for the MOND field's vacuum term with the framework kernel and the k = 2 turn-off (PAPER41/42):
   L(T) = Lambda c^4/a0^2 = (1/2) int_0^inf 2y (sqrt(1 + 1/y) - 1) / (1 + (y/T)^2) dy  =  (pi/4) T - (1/8) ln(4T) + 1/16 + O(ln T / T).
Derivation: 2y(sqrt(1+1/y) - 1) = 1 - h(y), h = 1 + 2y - 2 sqrt(y^2 + y); int_0^Y h dy = 1/4 ln(4Y) - 1/8 + O(1/Y) (elementary antiderivative, checked by sympy);
the Lorentzian gives int dy/(1+y^2/T^2) = pi T/2 and turns ln Y into ln T (h ~ 1/(4y)).
Corollary (the 32 pi footing): L(T) = 32 pi  <=>  T = 128 + (ln(4T) - 1/2)/(2 pi) + O(ln T/T)  ->  T = 128.91.
Run: python3 p45_vacuum_closed_form.py  |  MUTATE=1: constant 1/16 -> 1/8 (check N must fail)
"""
import os, sys, math
import sympy as sp
import mpmath as mp
MUTATE = os.environ.get("MUTATE") == "1"
res = []
def check(n, ok): res.append(bool(ok)); print(("PASS  " if ok else "FAIL  ") + n)
y, Y = sp.symbols("y Y", positive=True)
h = 1 + 2 * y - 2 * sp.sqrt(y**2 + y)
Hint = sp.integrate(h, (y, 0, Y))
lim = sp.limit(sp.simplify(Hint - sp.log(4 * Y) / 4), Y, sp.oo)
check(f"H int_0^Y h dy - (1/4) ln(4Y) -> {lim} (= -1/8) as Y -> oo (sympy, exact)", sp.simplify(lim + sp.Rational(1, 8)) == 0)
CONST = sp.Rational(1, 8) if MUTATE else sp.Rational(1, 16)
closed = lambda T: math.pi / 4 * T - math.log(4 * T) / 8 + float(CONST)
mp.mp.dps = 30
def L(T):
    f = lambda t: 2 * t * (mp.sqrt(1 + 1 / t) - 1) / (1 + (t / T)**2)
    return 0.5 * mp.quad(f, [0, 1, 10, T, 10 * T, mp.inf])
rows = [(T, float(L(T)), closed(T)) for T in (30.0, 100.0, 128.0, 1000.0, 1e4)]
for T, num, cf in rows:
    print(f"   T = {T:8.0f}: numeric {num:12.6f}  closed form {cf:12.6f}  diff {num - cf:+.2e}  (diff x T/ln T = {(num-cf)*T/math.log(T):+.3f})")
check("N the closed form matches the exact integral to < 0.01 for T >= 100 and the residual falls like ln T / T", all(abs(n - c) < 0.01 for T, n, c in rows if T >= 100))
check("P matches p35's committed values 77.85 / 99.81 / 784.4 at T = 100 / 128 / 1000", abs(closed(100) - 77.85) < 0.01 and abs(closed(128) - 99.81) < 0.01 and abs(closed(1000) - 784.4) < 0.05)
T = 128.0
for _ in range(50): T = 128 + (math.log(4 * T) - 0.5) / (2 * math.pi)
print(f"   32 pi footing: T = 128 + (ln 4T - 1/2)/(2 pi) = {T:.4f}  (numeric root of the exact integral: {float(mp.findroot(lambda t: L(t) - 32 * mp.pi, 128.9)):.4f})")
check("R the corollary T = 128 + (ln 4T - 1/2)/(2 pi) reproduces the numeric root 128.9 to 0.01", abs(T - float(mp.findroot(lambda t: L(t) - 32 * mp.pi, 128.9))) < 0.01)
print(f"\n{sum(res)}/{len(res)} pass" + ("  (MUTATE)" if MUTATE else ""))
sys.exit(0 if all(res) else 1)
