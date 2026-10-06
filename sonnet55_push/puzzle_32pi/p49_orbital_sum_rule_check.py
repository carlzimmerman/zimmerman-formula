"""p49: independent check of Sol's orbital sum rule (sol61_push/cold_component|puzzle_32pi breakthrough_2026_10_05, read-only):
   Lambda c^4/a0^2 = (1/4) int_0^inf y nu(y) [kappa^2/Omega^2 - 1] dy,   for an isolated point mass with g = g_N nu(y), y = g_N/a0 ~ r^-2.
Own derivation: Omega^2 = g/r, kappa^2/Omega^2 = 3 + dln g/dln r = 1 - 2 y nu'/nu, so the RHS = -(1/2) int y^2 nu' dy = int y (nu - 1) dy - (1/2)[y^2 (nu - 1)]_0^inf,
which equals our vacuum integral (1/2) int (nu - 1) d(y^2) (p21/p25) iff the boundary term vanishes.
Checks: (S) sympy, kappa^2/Omega^2 from a general g(r); (N) numerically for nu_fix (y_t = 128, PAPER41) and RAR: both sides agree; (B) for the exact framework kernel the
boundary term y^2(nu - 1) -> y/2 does NOT vanish (the a0/2 tail): the identity needs the turn-off.
Run: python3 p49_orbital_sum_rule_check.py  |  MUTATE=1: kappa^2/Omega^2 taken as 4 + dln g/dln r (wrong; check S and N must fail)
"""
import os, sys, math
import sympy as sp
import mpmath as mp
MUTATE = os.environ.get("MUTATE") == "1"
res = []
def check(n, ok): res.append(bool(ok)); print(("PASS  " if ok else "FAIL  ") + n)
r = sp.symbols("r", positive=True); g = sp.Function("g")(r)
Om2 = g / r
kap2 = sp.diff(r**4 * Om2, r) / r**3                      # kappa^2 = r^-3 d(r^4 Omega^2)/dr
ratio = sp.simplify(kap2 / Om2)
target = 3 + r * sp.diff(g, r) / g
claim = (4 if MUTATE else 3) + r * sp.diff(g, r) / g
check("S kappa^2/Omega^2 = 3 + dln g/dln r (sympy from the definition)", sp.simplify(ratio - claim) == 0)
mp.mp.dps = 25
def nu_fix(y, T=128): return 1 + (mp.sqrt(1 + 1 / y) - 1) / (1 + (y / T)**2)
def nu_rar(y): return 1 / (1 - mp.e**(-mp.sqrt(y)))
def both(nu):
    lhs = mp.quad(lambda y: y * (nu(y) - 1), [0, 1, 10, 100, 1000, mp.inf])
    dnu = lambda y: mp.diff(nu, y)
    off = 1 if MUTATE else 0                              # MUTATE: ratio - 1 gets an extra +1
    rhs = 0.25 * mp.quad(lambda y: y * nu(y) * ((1 - 2 * y * dnu(y) / nu(y) + off) - 1), [0, 1, 10, 100, 1000, mp.inf])
    return float(lhs), float(rhs)
for nm, f in (("nu_fix y_t=128", nu_fix), ("RAR", nu_rar)):
    l, rr = both(f)
    print(f"   {nm:16s}: vacuum integral int y(nu-1) dy = {l:.6f};  orbital sum rule = {rr:.6f}")
    if nm.startswith("nu_fix"): okfix = abs(l - rr) < 1e-4 * abs(l)
    else: okrar = abs(l - rr) < 1e-4 * abs(l)
check("N both sides agree (rel 1e-4) for the turn-off kernel and RAR", okfix and okrar)
yb = sp.symbols("y", positive=True)
bt = sp.limit(yb**2 * (sp.sqrt(1 + 1 / yb) - 1) / yb, yb, sp.oo)
check(f"B exact framework kernel: y^2(nu - 1)/y -> {bt} (boundary term grows like y/2): the sum rule needs the turn-off", bt == sp.Rational(1, 2))
print(f"\n{sum(res)}/{len(res)} pass" + ("  (MUTATE)" if MUTATE else ""))
sys.exit(0 if all(res) else 1)
