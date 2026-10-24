#!/usr/bin/env python3
"""TM1 SSb (AMENDMENT A1): re-solve D6's self-similar collisionless infall at 2x tau_max, memory-light.

D6's selfsim() is exec'd from its source text with ONE change: solve_ivp(..., dense_output=True) + sol.sol(t) is replaced by
solve_ivp(..., t_eval=t) + sol.y (the same sampled trajectory; no stored interpolants). The frozen 3x run exceeded 9 GB RSS
through dense_output and was killed before any row-3 number.  Writes tm1_selfsim_resolve_2x.npz (mode-independent).
Run: OMP_NUM_THREADS=1 nice -n 15 python3 tm1_selfsim_resolve.py
"""
import os, sys, math, time, resource
import numpy as np
from scipy.integrate import solve_ivp
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
T = open(os.path.join(REPO, "doors_push_2026_10_22", "D6_u_mechanism", "d6_u_mechanism.py")).read()
src = T[T.index("def selfsim("):T.index("key = hashlib")]
a = 'sol = solve_ivp(f, (1.0, p["tau_max"]), [1.0, 0.0], method="DOP853", rtol=p["rtol"], atol=p["atol"],\n                        dense_output=True)'
b = '        lt = np.linspace(0, math.log(p["tau_max"]), p["nsamp"]); t = np.exp(lt)\n        L, V = sol.sol(t)'
assert a in src and b in src
src = src.replace(a, 'lt = np.linspace(0, math.log(p["tau_max"]), p["nsamp"]); t = np.minimum(np.exp(lt), p["tau_max"])\n'
                     '        sol = solve_ivp(f, (1.0, p["tau_max"]), [1.0, 0.0], method="DOP853", rtol=p["rtol"], atol=p["atol"], t_eval=t)')
src = src.replace(b, '        L, V = sol.y')
ns = {"np": np, "math": math, "solve_ivp": solve_ivp, "XB": np.logspace(-2.5, 0.0, 51)}
exec(src, ns)
PAR = dict(tau_max_eps1=600.0, n_iter=40, nlam=400, soft=1e-4, nsamp=600000, rtol=1e-8, atol=1e-11, tol=1e-2)
SS = {}
for eps in (1.0, 0.5, 1.0 / 3.0):
    t0 = time.time(); SS[f"{eps:.4f}"] = ns["selfsim"](eps, PAR)
    s = SS[f"{eps:.4f}"]
    print(f"eps {eps:.4f}: {time.time() - t0:.0f} s, iterations {s['iters']}, last max|dlnM| {s['last_err']:.4f}, lambda_sp {s['lsp']:.4f}, "
          f"slope(0.01-0.03) {s['slope_in']:.3f}, RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9:.2f} GB", flush=True)
np.savez(os.path.join(HERE, "tm1_selfsim_resolve_2x.npz"), SS=np.array(SS, dtype=object), PAR=np.array(PAR, dtype=object))
