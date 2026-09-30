#!/usr/bin/env python3
"""CFG226 POST HOC 2 (written after the MUTATE control failed and the plain slope depended on the regression direction; reported only, NOT frozen, no substitution for the frozen fit).
The frozen likelihood lets the effective variance depend on the model's own slope, which biases a noise-free fit (the MUTATE failure).  Here the variances use a FIXED slope S0 = 3.7 (between the two plain-slope
estimates), in two directions: M given v (residual in log M) and v given M (residual in log v, v_model = sqrt(A(M))).  Each variant: a0 free and beta >= 0 free, sigma_int free; beta = 0 beside; and a noise-free MUTATE
(beta = 0.50 kpc) per variant.  kappa = 1/2 FITTED; no law verdict."""
import os, sys, io, contextlib, math
sys.dont_write_bytecode = True
import numpy as np
from scipy.optimize import minimize
LANE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(LANE, "cfg226_nonlocal_btfr.py")).read()
stop = src.index('# ---- controls (algebra first)')
ns = {"__file__": os.path.join(LANE, "cfg226_nonlocal_btfr.py"), "__name__": "cfg226_lib"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[:stop], "cfg226_nonlocal_btfr.py", "exec"), ns)
sample, M_model, A_of, KPC, G, MSUN = ns["sample"], ns["M_model"], ns["A_of"], ns["KPC"], ns["G"], ns["MSUN"]
OUT = [__doc__.strip(), ""]


def P(s):
    print(s); OUT.append(s)


S0 = 3.7


def logv_model(M_msun, a0, b):
    return np.array([0.5 * math.log10(A_of(M, a0, b)) - 3.0 for M in M_msun])          # log10 of v in km/s: v = sqrt(A) / 1e3 (A in (m/s)^2)


def m2(theta, d, direction, a0fix=None):
    la0, b, si = (theta if a0fix is None else (math.log10(a0fix), theta[0], theta[1]))
    a0 = 10 ** la0
    if direction == "M":
        r = d["logM"] - np.log10(M_model(d["v"], a0, b))
        var = d["sM"] ** 2 + (S0 * d["ev"]) ** 2 + si ** 2
    else:
        r = np.log10(d["v"]) - logv_model(10 ** d["logM"], a0, b)
        var = d["ev"] ** 2 + (d["sM"] / S0) ** 2 + si ** 2
    return float(np.sum(r ** 2 / var + np.log(var)))


def fit(d, direction, beta_fix=None):
    best = None
    for s0 in ((-9.92, 0.0, 0.1), (-10.1, 0.1, 0.1), (-10.3, 0.5, 0.15), (-9.8, 0.01, 0.08), (-10.0, 1.0, 0.12)):
        if beta_fix is None:
            r = minimize(lambda t: m2(t, d, direction), list(s0), method="L-BFGS-B", bounds=[(-11.5, -9.0), (0.0, 50.0), (1e-4, 1.0)])
        else:
            r = minimize(lambda t: m2([t[0], beta_fix, t[1]], d, direction), [s0[0], s0[2]], method="L-BFGS-B", bounds=[(-11.5, -9.0), (1e-4, 1.0)])
        if best is None or r.fun < best.fun:
            best = r
    return best


def prof_up(d, direction, m0):
    grid = np.concatenate([[0.0], np.logspace(-3, 1.3, 31)])
    p = np.array([fit(d, direction, b).fun for b in grid]) - m0
    i0 = int(np.argmin(p)); up = float("inf")
    for i in range(i0, len(grid)):
        if p[i] - p[i0] >= 2.71:
            b0, b1 = grid[i - 1], grid[i]
            up = b0 + (b1 - b0) * (2.71 - (p[i - 1] - p[i0])) / (p[i] - p[i - 1]) if b0 <= 0 else math.exp(math.log(b0) + (math.log(b1) - math.log(b0)) * (2.71 - (p[i - 1] - p[i0])) / (p[i] - p[i - 1]))
            break
    return grid[i0], up


P("variant: a0 free and beta >= 0 free; beta = 0 beside; improvement = -2lnL(beta = 0) - -2lnL(best); profile one-sided 95% upper limit on beta")
for tag, d in (("Upsilon 0.5, all", sample(0.5)), ("Upsilon 0.35", sample(0.35)), ("Upsilon 0.70", sample(0.70)), ("gas-dominated", sample(0.5, True))):
    for direction in ("M", "v"):
        f1 = fit(d, direction); f0 = fit(d, direction, 0.0)
        bh, up = prof_up(d, direction, f1.fun)
        P(f"  {tag:18s} [{direction} given {'v' if direction == 'M' else 'M'}, fixed-slope variance] N = {len(d['v']):3d}: beta_hat {f1.x[1]:.4f} kpc (profile minimum {bh:.4f}; 95% upper {up:.4f}), a0 {10 ** f1.x[0]:.3e}, sigma_int {f1.x[2]:.3f}; beta = 0: a0 {10 ** f0.x[0]:.3e}, improvement {f0.fun - f1.fun:.2f}")
P("\nnoise-free MUTATE per variant (M_i = M_model(v_i; 1.2e-10, 0.50 kpc) on the real v and errors)")
d = dict(sample(0.5)); d["logM"] = np.log10(M_model(d["v"], 1.2e-10, 0.50))
for direction in ("M", "v"):
    f1 = fit(d, direction); f0 = fit(d, direction, 0.0)
    P(f"  {direction} direction: beta_hat {f1.x[1]:.5f} kpc, a0 {10 ** f1.x[0]:.4e}; plain BTFR worse by {f0.fun - f1.fun:.1f}")
open(os.path.join(LANE, "cfg226_posthoc2.out"), "w").write("\n".join(OUT) + "\n")
