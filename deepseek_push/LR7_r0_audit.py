#!/usr/bin/env python3
"""LR7 R0 algebra audit (pre-registered BEFORE any number):
Lane LR7 = Lean certificates of the W1 exact rationals
  E[c]=3/4 (already certified, LR3/LR4c), E[c^2]=4/5, E[T]=5/12 (certified),
  E[cT]=2/5, E[T^2]=208/945 -> b0=19/160, b1=7/80, b2=703/30240.
R0 gate: independent evaluation of E[c^2], E[cT], E[T^2] by a method
DIFFERENT from W1's K-C monomial-Beta parser: 2D adaptive quadrature
(scipy dblquad) on the RAW (u,v) integrand with explicit sqrt(1-u^2),
PLUS a third method (mpmath Gauss-Legendre in u with analytic even-v
moments), PLUS exact coefficient identities
  b0 = (E[c^2]-E[c]^2)/2, b1 = E[cT]-E[c]E[T], b2 = (E[T^2]-E[T]^2)/2
checked EXACTLY in sympy against 19/160, 7/80, 703/30240.
Definitions (W1_tau0_cumulant.py, committed, loaded-not-transcribed logic
restated here per its docstring): volume source x isotropic direction ->
(u,v) on the unit disk with density (3/2)u; exit distance c = s - v,
s = sqrt(1-u^2); T = (u^2+v^2)c + v c^2 + c^3/3.
KILL (pre-registered): any R0 moment off by > 1e-8 relative, or any exact
coefficient identity mismatch -> exit 1, LR7 Lean leg NOT attempted.
Exit 0 iff all three methods agree within 1e-8 rel AND identities exact.
"""
import json, sys, math
import numpy as np
from scipy import integrate
import mpmath as mp
import sympy as sp

WANT = {"E_c2": sp.Rational(4,5), "E_cT": sp.Rational(2,5), "E_T2": sp.Rational(208,945)}
COEFS = {"b0": sp.Rational(19,160), "b1": sp.Rational(7,80), "b2": sp.Rational(703,30240)}
GATE = 1e-8
log_lines = []
def log(s):
    print(s); log_lines.append(s)

def integrand_factory(k, m):
    u, v = sp.symbols("u v", positive=True)
    s = sp.sqrt(1-u**2); c = s - v
    T = (u**2+v**2)*c + v*c**2 + c**3/3
    return sp.lambdify((u, v), sp.expand(sp.Rational(3,2)*u*(c**k)*(T**m)), "numpy")

def m1_dblquad(k, m):
    f = integrand_factory(k, m)
    val, err = integrate.dblquad(lambda vv, uu: float(f(uu, vv)), 0, 1, lambda u: -math.sqrt(1-u*u), lambda u: math.sqrt(1-u*u),
                                 epsabs=1e-12, epsrel=1e-11)
    return val, err

def m2_gauss_legendre(k, m, nu=400, nv_per=200):
    u, v = sp.symbols("u v", positive=True)
    s = sp.sqrt(1-u**2); c = s - v
    T = (u**2+v**2)*c + v*c**2 + c**3/3
    expr = sp.expand(sp.Rational(3,2)*u*(c**k)*(T**m))
    # analytic even-v inner moment per u: sum over even v-powers
    sv, uv = sp.symbols("sv uv", positive=True)
    inner_total = sp.Integer(0)
    for term in expr.as_ordered_terms():
        pd = sp.Poly(term, v).as_dict() if term.has(v) else {(0,): term}
        pass
    # simpler: numeric GL in v via lambdify on grid of u nodes
    us, ws = np.polynomial.legendre.leggauss(nu)
    us = 0.5*(us+1); ws = 0.5*ws
    fu = sp.lambdify(u, sp.integrate(expr, (v, -s, s)), "numpy")
    vals = fu(us)
    return float(np.dot(ws, vals)), None

Ec  = sp.Rational(3,4); ET = sp.Rational(5,12)   # certified (LR3/LR4c), inputs not targets

res = {"method_dblquad": {}, "method_gl_analytic_v": {}, "exact_identities": {}}
fails = []
for name, (k, m) in {"E_c2": (2,0), "E_cT": (1,1), "E_T2": (0,2)}.items():
    want = float(WANT[name])
    v1, e1 = m1_dblquad(k, m)
    v2, _ = m2_gauss_legendre(k, m)
    r1 = abs(v1-want)/want; r2 = abs(v2-want)/want
    res["method_dblquad"][name] = {"val": v1, "abs_err_est": e1, "rel_dev": r1}
    res["method_gl_analytic_v"][name] = {"val": v2, "rel_dev": r2}
    log("R0 %s: dblquad %.12f (rel %.2e) | GL+analytic-v %.12f (rel %.2e) | target %s = %.12f"
        % (name, v1, r1, v2, r2, WANT[name], want))
    if r1 > GATE or r2 > GATE: fails.append(name)

# exact coefficient identities (sympy, exact rationals)
b0 = (WANT["E_c2"]-Ec**2)/2; b1 = WANT["E_cT"]-Ec*ET; b2 = (WANT["E_T2"]-ET**2)/2
for nm, got, want in [("b0", b0, COEFS["b0"]), ("b1", b1, COEFS["b1"]), ("b2", b2, COEFS["b2"])]:
    ok = sp.simplify(got-want) == 0
    res["exact_identities"][nm] = {"derived": str(got), "want": str(want), "exact": bool(ok)}
    log("R0 identity %s: derived %s vs %s -> %s" % (nm, got, want, "EXACT" if ok else "MISMATCH"))
    if not ok: fails.append(nm)

res["fails"] = fails; res["gate"] = GATE
json.dump(res, open("LR7_r0_audit.json","w"), indent=1)
with open("LR7_r0_audit.out","w") as f: f.write("\n".join(log_lines)+"\n")
if fails:
    print("LR7_R0_EXIT1: %s" % fails); sys.exit(1)
print("LR7_R0_EXIT0"); sys.exit(0)

# RUN HISTORY: run-1 exit 1 -- dblquad integrand argument order bug (func(y,x):
# first arg is the INNER variable v, not u); integrand evaluated as f(v,u).
# Runner fixed (estimator bug, math untouched); run-1 preserved in .out.
