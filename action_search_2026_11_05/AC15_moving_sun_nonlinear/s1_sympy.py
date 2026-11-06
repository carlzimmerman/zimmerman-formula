#!/usr/bin/env python3
"""AC15 S1: global Bernoulli from the P equation; Euler form; static limit (KA1); Bernoulli-off = AC12 (KA2).

Criteria: FROZEN_CRITERIA.md (b089f97024). Run from the repo root:
  PYTHONHASHSEED=0 OMP_NUM_THREADS=1 python3 action_search_2026_11_05/AC15_moving_sun_nonlinear/s1_sympy.py
kappa = 1/2 FITTED; footings never pooled; not theory closed.
"""
import os, sys, json, math
sys.dont_write_bytecode = True
import sympy as sp
from sympy.calculus.euler import euler_equations

HERE = os.path.dirname(os.path.abspath(__file__))
OUT, RES = [], {"lane": "AC15_moving_sun_nonlinear", "criteria": "b089f97024", "checks": {}}


def P(s=""):
    print(s, flush=True); OUT.append(str(s))


def check(name, ok, detail):
    RES["checks"][name] = dict(ok=bool(ok), detail=str(detail)); P(f"{name} {'PASS' if ok else 'FAIL'} {detail}")


t, x, y, z = Xs = sp.symbols("t x y z", real=True)
xs3 = (x, y, z)
gam, KM = sp.symbols("gamma KM", positive=True)
sig = sp.Function("sigma")(*Xs); phi = sp.Function("phi")(*Xs)
Pf = [sp.Function(f"P{i}")(*Xs) for i in range(3)]
Xi = phi - sp.diff(sig, t) + sum(sp.diff(sig, v) ** 2 for v in xs3) / 2
q = sum(sp.diff(Pf[i], xs3[i]) for i in range(3))
L = sum(Pf[i] * sp.diff(Xi, xs3[i]) for i in range(3)) - gam / 2 * q ** 2 - KM / 2 * sum(p_ ** 2 for p_ in Pf)

# S1a: P equations  ->  grad(Xi + gamma q) = KM P   (EL: dL/dP - div(dL/d grad P) = 0)
els = euler_equations(L, Pf, Xs)
res = [sp.simplify(sp.expand(els[i].lhs) - (sp.diff(Xi + gam * q, xs3[i]) - KM * Pf[i])) for i in range(3)]
res2 = [sp.simplify(sp.expand(els[i].lhs) + (sp.diff(Xi + gam * q, xs3[i]) - KM * Pf[i])) for i in range(3)]
check("S1a", all(r == 0 for r in res) or all(r == 0 for r in res2),
      f"P-EL = +/-[grad(Xi + gamma q) - K M_theta P]: residuals {res if all(r == 0 for r in res) else res2}")

# screening-term size at 10 AU: 2 M_theta (r/Lstar)^2, M_theta = (1 + x_e)^2
PC = 3.0856775814913673e16; AU = 1.495978707e11
scr = {f: 2 * (1 + xe) ** 2 * (10 * AU / (Lmin * PC)) ** 2 for f, xe, Lmin in (("canonical", 1.15, 21.68), ("alt", 2.6, 22.85))}
check("S1a_size", max(scr.values()) <= 1e-9, f"2 M_theta (10 AU/Lstar)^2 = {scr} (line 1e-9): screening term dropped")
RES["screening_10AU"] = scr

# S1b: stationary pattern sigma(x - V t) along z: Xi = phi + (w^2 - V^2)/2, w = v - V
V = sp.Symbol("V", real=True)
s0 = sp.Function("s0")
sig_st = s0(x, y, z - V * t)
Xi_st = phi - sp.diff(sig_st, t) + sum(sp.diff(sig_st, v) ** 2 for v in xs3) / 2
vv = [-sp.diff(sig_st, v) for v in xs3]
w = [vv[0], vv[1], vv[2] - V]
r1b = sp.simplify(Xi_st - (phi + (sum(c ** 2 for c in w) - V ** 2) / 2))
check("S1b", r1b == 0, f"Xi - [phi + (w^2 - V^2)/2] = {r1b}  ->  gamma q = c_gal^2 + Phi_N + (V^2 - w^2)/2 (global, one constant)")

# S1c: gradient of Hamilton-Jacobi (sigma_t = phi + |grad sigma|^2/2 + h - C, h = gamma q) is Euler, v = -grad sigma
h = sp.Function("h")(*Xs)
HJ = sp.diff(sig, t) - (phi + sum(sp.diff(sig, v) ** 2 for v in xs3) / 2 + h)
v_ = [-sp.diff(sig, c) for c in xs3]
euler = [sp.diff(v_[i], t) + sum(v_[j] * sp.diff(v_[i], xs3[j]) for j in range(3)) + sp.diff(phi, xs3[i]) + sp.diff(h, xs3[i]) for i in range(3)]
r1c = [sp.simplify(euler[i] + sp.diff(HJ, xs3[i])) for i in range(3)]
check("S1c", all(r == 0 for r in r1c), f"-grad(HJ) = Euler(dv/dt + v.grad v = -grad phi - grad h): residuals {r1c}")

# KA1: V = 0, w = 0  ->  gamma q = c^2 + Phi_N; enclosed hedgehog charge M r^2 / Lstar^2 (gamma = 2 pi Lstar^2, geometric)
r, M, Ls, cg = sp.symbols("r M Lstar c_gal", positive=True)
qh = (cg ** 2 + M / r) / (2 * sp.pi * Ls ** 2) - cg ** 2 / (2 * sp.pi * Ls ** 2)       # minus Galactic background
Menc = sp.integrate(4 * sp.pi * r ** 2 * qh, (r, 0, r))
check("KA1", sp.simplify(Menc - M * r ** 2 / Ls ** 2) == 0 and sp.simplify(Menc / r ** 2 - M / Ls ** 2) == 0,
      f"V = w = 0: hedgehog enclosed charge {Menc} -> anomaly GM/Lstar^2 (C6P)")

# KA2: Bernoulli off (q fixed): stationary continuity d_t q + div(q v) = 0 with q(x - V t) is div(q w) = 0 (AC12)
q0 = sp.Function("q0")
qst = q0(x, y, z - V * t)
cont = sp.diff(qst, t) + sum(sp.diff(qst * vv[i], xs3[i]) for i in range(3))
divqw = sum(sp.diff(qst * w[i], xs3[i]) for i in range(3))
check("KA2", sp.simplify(cont - divqw) == 0, "d_t q + div(q v) = div(q w) for a stationary pattern: AC12's operator")

ok = all(c["ok"] for c in RES["checks"].values())
P(f"S1 overall {'PASS' if ok else 'FAIL'}  kappa = 1/2 FITTED; not theory closed")
json.dump(RES, open(os.path.join(HERE, "s1.json"), "w"), indent=1)
open(os.path.join(HERE, "s1.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if ok else 1)
