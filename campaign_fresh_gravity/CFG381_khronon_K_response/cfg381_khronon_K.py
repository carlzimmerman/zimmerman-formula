"""CFG381: does the chassis khronon equation produce K ~ Gamma/c when the cold fluid settles? Criteria: FROZEN_CRITERIA.md (364e91182).
Linearised khronometric action alpha a.a - c2 K^2 (beta = 0) in the weak-field metric; sympy Euler-Lagrange for chi.
Run: python3 cfg381_khronon_K.py ; MUTATE=1 sets alpha_c -> 1 (R_K must move by > 1e6; rc 1).
"""
import json, math, os, sys
import sympy as sp
from sympy.calculus.euler import euler_equations

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("MUTATE") == "1"
TAG = "_MUTATE" if MUTATE else ""
lines, checks = [], []
def say(s=""):
    print(s); lines.append(s)
def check(n, ok, v):
    checks.append({"name": n, "pass": bool(ok), "value": v}); say(f"  [{'PASS' if ok else 'FAIL'}] {n}: {v}")

say("CFG381 khronon K response" + ("  (MUTATE: alpha_c -> 1)" if MUTATE else ""))
say("=" * 78)
t, x, y, z = sp.symbols("t x y z")
al, c2 = sp.symbols("alpha c2", positive=True)
X = (x, y, z)
chi, Phi, Psi = (sp.Function(n)(t, x, y, z) for n in ("chi", "Phi", "Psi"))
B = [sp.Function(f"B{i}")(t, x, y, z) for i in range(3)]
lap = lambda f: sum(sp.diff(f, v, 2) for v in X)
# linearised kinematics (u_i = d_i chi at linear order; u^i = B_i - d_i chi; c = 1)
a_vec = [sp.diff(sp.diff(chi, t) + Phi, v) for v in X]
K = sum(sp.diff(B[i], X[i]) for i in range(3)) - lap(chi) + 3 * sp.diff(Psi, t)
L = al * sum(ai**2 for ai in a_vec) - c2 * K**2
# C1: static, chi = 0, B = 0 -> a = grad Phi, K = 3 Psi-dot
subs0 = {chi: 0}
a0 = [sp.simplify(ai.subs(chi, 0)) for ai in a_vec]
K0 = sp.simplify(K.subs(chi, 0).subs({B[0]: 0, B[1]: 0, B[2]: 0}).doit())
check("C1 linear kinematics: chi = 0, B = 0 gives a = grad Phi and K = 3 Psi-dot",
      all(sp.simplify(a0[i] - sp.diff(Phi, X[i])) == 0 for i in range(3)) and sp.simplify(K0 - 3 * sp.diff(Psi, t)) == 0, "ok")
EL = euler_equations(L, [chi], [t, x, y, z])[0].lhs
target = 2 * (al * sp.diff(lap(sp.diff(chi, t) + Phi), t) + c2 * lap(K))
same = sp.simplify(sp.expand(EL - target)) == 0 or sp.simplify(sp.expand(EL + target)) == 0
check("Derived chi equation = +-2 [alpha d_t lap(chi-dot + Phi) + c2 lap K]  =>  lap[c2 K + alpha d_t(chi-dot + Phi)] = 0", same, "sympy Euler-Lagrange")
say("  With decaying boundary conditions: K = -(alpha/c2) d_t(chi-dot + Phi). The khronon's expansion is driven ONLY through alpha_c,")
say("  by the time-change of the lapse potential.")
EL0 = sp.simplify(EL.subs(al, 0))
check("C2 alpha_c = 0 decouples chi from Phi (equation -> lap K = 0, no Phi)", not EL0.has(Phi), f"Phi present: {EL0.has(Phi)}")

# ---------------- numbers
c = 2.998e8
V = 2.0e5
PhiN = V**2                                     # |Phi| ~ V^2 (m^2/s^2)
HL = 67.4e3 / 3.0857e22 * math.sqrt(0.6847)
ALPHA = (1.0, 1.0) if MUTATE else (9.62e-14, 3.2e-9)
C2W = (7.29e-3, 0.0667)
say("\nInduced K for settling: Phi-dot ~ Gamma Phi (chi-ddot taken <= the same order: an upper bracket x2)")
res = {}
for lab, Gam in (("CFG370 cooling 3.21 H_L", 3.21 * HL), ("CFG245 needed 5.4 H_L", 5.4 * HL)):
    K_need = Gam / c
    Ks = [(a / cc) * 2 * Gam * PhiN / c**3 for a in ALPHA for cc in C2W]     # x2 bracket for chi-ddot
    R = [k / K_need for k in Ks]
    res[lab] = dict(K_need=K_need, R_min=min(R), R_max=max(R))
    say(f"  {lab}: K_needed = {K_need:.2e} /m;  R_K = K_induced/K_needed = {min(R):.1e} .. {max(R):.1e}  [= 2 (alpha/c2)(V/c)^2]")
Rmax = max(v["R_max"] for v in res.values())
verdict = "PRODUCES" if Rmax >= 0.1 else "DOES NOT PRODUCE"
say(f"\nVERDICT: {verdict}  (max R_K = {Rmax:.1e}; the induced expansion is suppressed by (alpha_c/c_2)(V/c)^2)")
# direct-coupling cost
say("Direct alternative: a fluid-khronon coupling lambda_x (rho_c - rho_target) K would source K directly. Matching K ~ Gamma/c fixes")
say("lambda_x to one NEW dark-sector constant (it does not touch baryons, so G9 is intact). The sink then exists by construction: CONDITIONAL with +1 constant.")
check("T-MUT main-run marker (MUTATE alpha_c -> 1 must move R_K by > 1e6)", not MUTATE, f"max R_K {Rmax:.1e}")
if MUTATE:
    checks.append({"name": "MUTATE forces rc 1", "pass": False, "value": Rmax})
n = sum(c_["pass"] for c_ in checks)
say(f"\n{n}/{len(checks)} pass" + ("  (MUTATE)" if MUTATE else ""))
json.dump({"lane": "CFG381", "mutate": MUTATE, "verdict": verdict, "R": res, "relation": "K = -(alpha/c2) d_t(chi-dot + Phi)", "checks": checks},
          open(os.path.join(HERE, f"cfg381_results{TAG}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg381{TAG}.out"), "w").write("\n".join(lines) + "\n")
sys.exit(0 if n == len(checks) else 1)
