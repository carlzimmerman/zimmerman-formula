#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
G3 -- OWNERSHIP AS A HISTORY VARIABLE INSIDE AN ACTION: is the accretion / turnaround history a legal action term?   Gate GA (a)-(d), GG(i).

MODEL.  One degree of freedom x(t) (a baryon element's turnaround coordinate) with a discrete action on N steps:
        S = sum_i dt [ (1/2) ((x_{i+1} - x_i)/dt)^2 - V(x_i) - B W(ell_i) ]
    and four gate variables ell_i:
        LOCAL     ell_i = f(x_i)                                  (an instantaneous state gate, the DE12 / XR36 class)
        MEMORY    ell_i = dt sum_{j<i} f(x_j)                     (accumulated time spent turned around)
        LATCH     ell_i = 1 - prod_{j<i} (1 - f(x_j))             (has ever turned around: the ownership latch)
        LABEL     ell_i = ell_0 (a prescribed, advected label: ownership as initial data)
    with f a smooth turnaround indicator and W a smooth step.  The Euler-Lagrange residual is R_i = dS/dx_i.
CAUSALITY TEST (frozen in GATES_FROZEN.md, GA).  A history term is admissible only if R_i depends on x_j only for j <= i + 1 (a banded Hessian):
    then the trajectory can be advanced forward from initial data.  The measure is  c = max_{j > i+1} |d R_i / d x_j| / max |d R_i / d x_j|
    (Hessian by sympy, evaluated on a test trajectory).  PASS iff c < 1e-12.
RESULT (pre-declared): LOCAL and LABEL banded; MEMORY and LATCH not.  In the memory and latch actions the force at time t_i contains W'(ell_k) f'(x_i)
    for every LATER k > i: the early motion depends on the future trajectory.  (Equivalent: with ell as a constrained variable the multiplier lambda obeys
    a BACKWARD recursion with a terminal condition, so the problem is a two-point boundary value problem, not an initial value problem.)
    A LABEL is causal but is initial data: ownership is then a postulate (PARTIAL), not derived.
MUTATE=1 replaces MEMORY and LATCH by the LOCAL gate: the claim "the memory action has advanced dependence" must FAIL.
SCOPE.  A toy with one variable; smooth W, f; exact statement is about the structure of the reduced action, not the size of the effect.
"""
import os, sys, math
import numpy as np
import sympy as sp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from Gcommon import *   # noqa

MUTATE = os.environ.get("MUTATE", "0") == "1"
R = Report("G3_history_action_causality", MUTATE)
P = R.P
P(__doc__.strip())
if MUTATE:
    P("\n  *** MUTATE=1: MEMORY and LATCH replaced by the LOCAL gate; 'advanced dependence' must FAIL ***")

N = 10
dt = sp.Rational(1, 5)
xs = sp.symbols(f"x0:{N + 1}", real=True)
f = lambda x: 1 / (1 + sp.exp(x / sp.Rational(3, 10)))                  # turnaround indicator (smooth)
Wg = lambda l: 1 / (1 + sp.exp(-(l - sp.Rational(1, 2)) / sp.Rational(1, 10)))
Vp = lambda x: x ** 2 / 2
Bc = 1


def action(kind):
    S = 0
    for i in range(N):
        kin = ((xs[i + 1] - xs[i]) / dt) ** 2 / 2
        if kind == "LOCAL" or (MUTATE and kind in ("MEMORY", "LATCH")):
            ell = f(xs[i])
        elif kind == "MEMORY":
            ell = dt * sum(f(xs[j]) for j in range(i)) if i > 0 else sp.Integer(0)
        elif kind == "LATCH":
            pr = sp.Integer(1)
            for j in range(i):
                pr *= (1 - f(xs[j]))
            ell = 1 - pr
        elif kind == "LABEL":
            ell = sp.Rational(3, 5)
        S += dt * (kin - Vp(xs[i]) - Bc * Wg(ell))
    return S


x0 = {xs[i]: sp.Float(0.9 * math.cos(0.7 * i) - 0.2) for i in range(N + 1)}
res = {}
for kind in ("LOCAL", "LABEL", "MEMORY", "LATCH"):
    S = action(kind)
    H = sp.hessian(S, xs[:N])                                            # residual R_i = dS/dx_i for i < N (x_N fixed)
    Hn = np.array(H.subs(x0).evalf(30).tolist(), dtype=float)
    scale = np.max(np.abs(Hn))
    far = 0.0
    for i in range(N):
        for j in range(N):
            if j > i + 1:
                far = max(far, abs(Hn[i, j]))
    c = far / scale
    # dependence of the earliest residual on the latest coordinate
    dep0 = max(abs(Hn[0, j]) for j in range(2, N)) / scale
    res[kind] = dict(c=c, R0_on_xlast=dep0)
    P(f"    {kind:7s}: c = max_(j>i+1) |dR_i/dx_j| / max|H| = {c:.3e};   max_(j>=2) |dR_0/dx_j|/max|H| = {dep0:.3e}")
R.num("results", res)
banded = {k: res[k]["c"] < 1e-12 for k in res}
claim = banded["LOCAL"] and banded["LABEL"] and (not banded["MEMORY"]) and (not banded["LATCH"])
R.check("H1 the LOCAL and LABEL actions have banded Euler-Lagrange residuals (causal); the MEMORY and LATCH actions do not: R_i depends on later coordinates (advanced dependence)",
        f"c: {({k: float('%.2e' % v['c']) for k, v in res.items()})}" + ("  [MUTATE: memory/latch replaced by local]" if MUTATE else ""), claim)
R.check("H2 the size of the advanced dependence: the earliest force depends on later coordinates (j >= 2) at a relative strength >= 1e-4 in both history actions",
        f"{({k: float('%.2e' % res[k]['R0_on_xlast']) for k in ('MEMORY', 'LATCH')})}" + ("  [MUTATE]" if MUTATE else ""),
        res["MEMORY"]["R0_on_xlast"] >= 1e-4 and res["LATCH"]["R0_on_xlast"] >= 1e-4)

R.verdict("GA / accretion-history (memory) variable inside an action", "FAIL", "the EL residual at t depends on the future trajectory (adjoint / backward-in-time structure); hypotheses: reduced action with the history as a functional of the path, smooth W, f")
R.verdict("GA / ownership latch ('has ever turned around')", "FAIL", "same: advanced dependence; a latch is irreversible, an action's EL equations are not")
R.verdict("GA / prescribed advected label (ownership as initial data)", "PARTIAL", "causal and legal as a two-species baryon fluid, but the label is a POSTULATE (the assignment rule is not derived): 'ownership' becomes 'which baryons have the charge'")
R.verdict("GG(i) / history", "PARTIAL", "the only causal carrier of history is a prescribed label; the rule that sets it (first turnaround, first top-level status) is outside the action")
nf = R.write()
sys.exit(1 if nf else 0)
