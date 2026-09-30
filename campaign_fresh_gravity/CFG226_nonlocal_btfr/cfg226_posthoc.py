#!/usr/bin/env python3
"""CFG226 POST HOC diagnostics (written after the main run, whose C1 slope control failed narrowly at 3.597 against the frozen window [3.6, 4.2]; reported only, not frozen):
where does the shallow plain-BTFR slope come from, and does the beta > 0 preference track it?  The plain power-law slope (same effective-variance likelihood) for the sample, its subsamples and an
inverse regression; the F1 beta_hat and the improvement over beta = 0 restricted to galaxies above a mass cut.  kappa = 1/2 FITTED; no law verdict."""
import os, sys, io, contextlib
sys.dont_write_bytecode = True
import numpy as np
from scipy.optimize import minimize
LANE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(LANE, "cfg226_nonlocal_btfr.py")).read()
stop = src.index('# ---- controls (algebra first)')
ns = {"__file__": os.path.join(LANE, "cfg226_nonlocal_btfr.py"), "__name__": "cfg226_lib"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[:stop], "cfg226_nonlocal_btfr.py", "exec"), ns)
sample, fit, m2nll = ns["sample"], ns["fit"], ns["m2nll"]
OUT = [__doc__.strip(), ""]


def P(s):
    print(s); OUT.append(s)


def slope_fit(d):
    def m2(t):
        s_, c, si = t
        var = d["sM"] ** 2 + (s_ * d["ev"]) ** 2 + si ** 2
        return float(np.sum((d["logM"] - (s_ * np.log10(d["v"]) + c)) ** 2 / var + np.log(var)))
    r = min((minimize(m2, [s0, 1.0, 0.1], method="L-BFGS-B", bounds=[(2, 6), (-5, 5), (1e-3, 1)]) for s0 in (3.5, 3.9, 4.3)), key=lambda r: r.fun)
    return r.x[0], r.x[2]


def inv_slope(d):
    """log v on log M with the same errors propagated the other way (v dependent)."""
    def m2(t):
        s_, c, si = t                           # log v = s_ log M + c  (s_ ~ 1/slope)
        ev2 = d["ev"] ** 2 + (s_ * d["sM"]) ** 2 + si ** 2
        return float(np.sum((np.log10(d["v"]) - (s_ * d["logM"] + c)) ** 2 / ev2 + np.log(ev2)))
    r = min((minimize(m2, [s0, -1.0, 0.03], method="L-BFGS-B", bounds=[(0.1, 0.6), (-5, 5), (1e-4, 1)]) for s0 in (0.25, 0.27)), key=lambda r: r.fun)
    return 1 / r.x[0]


P("plain BTFR slope (effective-variance fit of log M on log v, sigma_int free); inverse-regression slope beside it")
for tag, d in (("Upsilon 0.5, all", sample(0.5)), ("Upsilon 0.35", sample(0.35)), ("Upsilon 0.70", sample(0.70)), ("gas-dominated", sample(0.5, True))):
    s_, si = slope_fit(d)
    P(f"  {tag:18s} N = {len(d['v']):3d}: slope {s_:.3f} (sigma_int {si:.3f}); inverse-regression slope {inv_slope(d):.3f}")
P("\nrestricting to galaxies above a baryonic mass cut (Upsilon 0.5): plain slope, F1 beta_hat (kpc) and the improvement in -2 lnL over beta = 0")
d0 = sample(0.5)
for cut in (0.0, 8.5, 9.0, 9.5, 10.0):
    m = d0["logM"] >= cut
    d = {k: (v[m] if k != "name" else [n for n, mm in zip(v, m) if mm]) for k, v in d0.items()}
    if len(d["v"]) < 20:
        continue
    s_, si = slope_fit(d); f1 = fit(d); f4 = fit(d, None, 0.0)
    P(f"  log10 M_bar >= {cut:4.1f}: N = {len(d['v']):3d}, slope {s_:.3f}, beta_hat {f1['beta']:.3f} kpc, a0 {f1['a0']:.3e}, improvement {f4['m2'] - f1['m2']:.2f}")
P("\nReading: the fitted beta tracks the plain slope; a slope below 4 has other causes (Upsilon, distances, inclination, pressure support in dwarfs), so a beta > 0 preference does not single out this model.")
open(os.path.join(LANE, "cfg226_posthoc.out"), "w").write("\n".join(OUT) + "\n")
