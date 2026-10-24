#!/usr/bin/env python3
"""X24b_vacuum_heated_cold: sympy derivation D1-D5 (FROZEN_CRITERIA.md section 1).

    PYTHONHASHSEED=0 python3 x24b_derive.py                 -> x24b_derive.out, _results.json (exit 0 iff D1-D5 hold)
    PYTHONHASHSEED=0 X24B_MUTATE=1 python3 x24b_derive.py   -> heating per unit MASS; D3 and D5 must FAIL (exit 1)

Cold sector: number-conserving, isotropic kinetic pressure p = rho sigma^2, u = (3/2) sigma^2 (gamma = 5/3).
Energy equation per unit mass: du/dt = (2/3) u dln(rho)/dt + q,  q = Q/rho,  Q = eps H rho_L c^2 (VHC, per unit volume).
MUTATE: q = eps H c^2 rho_L / rhobar_c(a) (per unit mass, independent of the local density; same background).
"""
import json, os, sys
import sympy as sp

MUT = os.environ.get("X24B_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__))
OUT, RES = [], {"mutate": MUT, "checks": {}}
def P(*a):
    s = " ".join(str(x) for x in a); print(s); OUT.append(s)
def chk(name, ok, val):
    RES["checks"][name] = {"pass": bool(ok), "value": str(val)}
    P(f"[{'PASS' if ok else 'FAIL'}] {name}: {val}")

P("X24b derivation" + (" [MUTATE: heating per unit mass]" if MUT else "") + "; kappa = 1/2 FITTED; not theory closed")
N = sp.symbols("N", real=True)                      # N = ln a
eps, c, rL, r0 = sp.symbols("epsilon c rho_L rho_c0", positive=True)
a = sp.exp(N)
rbar = r0 * a ** -3

def q_over_H(rho):                                  # specific heating per e-fold, q/H
    return eps * rL * c ** 2 / (rbar if MUT else rho)

# D1 background
u = sp.Function("u")
sol = sp.dsolve(sp.Eq(u(N).diff(N), sp.Rational(2, 3) * u(N) * sp.diff(sp.log(rbar), N) + q_over_H(rbar)), u(N))
ubar_closed = eps * c ** 2 * rL / (5 * r0) * a ** 3
part = sp.simplify(sol.rhs - ubar_closed)           # remaining = C1 * a^-2 (cold start: C1 = 0)
C1 = list(sol.free_symbols - {N, eps, c, rL, r0})
ok1 = sp.simplify(part.subs({s: 0 for s in C1})) == 0 and sp.simplify(part * a ** 2).free_symbols <= set(C1)
cs2 = sp.simplify(sp.Rational(2, 3) * ubar_closed)
chk("D1 background", ok1, f"u = {sol.rhs};  cold start => ubar = eps c^2 rho_L a^3/(5 rho_c0); c_s^2 = (2/3)u = {cs2}  (c_s ~ a^1.5: X22 p = 2)")
RES["D1"] = {"ubar": str(ubar_closed), "cs2": str(cs2), "p_X22": 2}

# D2 entropy K = (2/3) u rho^(-2/3)
rho = sp.Function("rho", positive=True)(N)
uf = sp.Function("uu")(N)
dudN = sp.Rational(2, 3) * uf * sp.diff(sp.log(rho), N) + q_over_H(rho)
K = sp.Rational(2, 3) * uf * rho ** sp.Rational(-2, 3)
dK = sp.simplify(sp.diff(K, N).subs(sp.Derivative(uf, N), dudN))
target = sp.Rational(2, 3) * eps * rL * c ** 2 * rho ** sp.Rational(-5, 3)
ok2 = sp.simplify(dK - target) == 0
chk("D2 entropy", ok2 if not MUT else ok2, f"dK/dlna = {dK}  (VHC target (2/3) eps rho_L c^2 rho^(-5/3))")

# D3 linear: u = ubar (1+s), rho = rbar (1+d); first order in a bookkeeping parameter
lam = sp.symbols("lam")
d = sp.Function("d")(N); s = sp.Function("s")(N)
U = ubar_closed * (1 + lam * s); R = rbar * (1 + lam * d)
eq = sp.diff(U, N) - (sp.Rational(2, 3) * U * sp.diff(sp.log(R), N) + q_over_H(R))
lin = sp.simplify(sp.series(eq, lam, 0, 2).removeO().coeff(lam, 1) / ubar_closed)
sprime = sp.solve(sp.Eq(lin, 0), sp.Derivative(s, N))[0]
ref = sp.Rational(2, 3) * sp.Derivative(d, N) - 5 * (d + s)
A = sp.symbols("A")
attr = sp.solve(sp.Eq(sp.simplify(sprime.subs({s: A * a, d: a}).doit() - A * a), 0), A)
okform = sp.simplify(sprime - ref) == 0
ok3 = okform and len(attr) == 1 and attr[0] == sp.Rational(-13, 18)
chk("D3 linear", ok3, f"s' = {sp.simplify(sprime)}; attractor s = A d with A = {attr}; dp/p = d + s => dp/drho = {sp.simplify(1 + attr[0]) if attr else 'nan'} c_s^2 (VHC: 5/18)")
RES["D3"] = {"s_prime": str(sp.simplify(sprime)), "A": str(attr[0]) if attr else None}

# D4 vacuum
rLf = sp.Function("rL")(N)
solL = sp.dsolve(sp.Eq(rLf.diff(N), -eps * rLf), rLf).rhs
w = sp.simplify(-1 - sp.diff(sp.log(solL), N) / 3)
ok4 = sp.simplify(w - (-1 + eps / 3)) == 0
chk("D4 vacuum", ok4, f"rho_L = {solL}; w_L = {w}; thermal energy density today rho_c0 * ubar(1) = {sp.simplify(r0 * ubar_closed.subs(N, 0))}")

# D5 inversion: element held at rho_in = Delta * 8 * rbar(a_c) (virial) from a_c = 1/2 to 1; increment vs background increment
Nc = sp.log(sp.Rational(1, 2)); Delta = 200
rho_in = Delta * 8 * rbar.subs(N, Nc)
du_dense = sp.integrate(q_over_H(rho_in) if not MUT else q_over_H(rbar), (N, Nc, 0))   # fixed rho: no adiabatic term
du_bg = ubar_closed.subs(N, 0) - ubar_closed.subs(N, Nc)
ratio = sp.nsimplify(sp.simplify(du_dense / du_bg))
ok5 = float(ratio) < 1.0
chk("D5 inversion", ok5, f"specific heat gained a = 1/2 -> 1 at 1600 x rbar(a_c) over the background's: {ratio} = {float(ratio):.4g} (< 1 required)")

n = sum(v["pass"] for v in RES["checks"].values())
P(f"\nchecks {n}/{len(RES['checks'])}")
open(os.path.join(HERE, f"x24b_derive{TAG}.out"), "w").write("\n".join(OUT) + "\n")
json.dump(RES, open(os.path.join(HERE, f"x24b_derive_results{TAG}.json"), "w"), indent=1)
sys.exit(0 if n == len(RES["checks"]) else 1)
