#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""g03l -- the candidate's kernel (exponential below y_tot = 1, monotone scalar force above; g03j) against SPARC, on f25's design:
equal-galaxy log-residual MSE with a_0 AND the disc M/L profiled jointly on a grid, paired multinomial galaxy resampling (999 replicates).
The kernel as nu(y) = g_obs/g_N with y = g_N/a0: nu = nu_muexp(y) for y <= 1 - 1/e, and 1 + (1/e)(y/0.632)^p / y above (continuous), p = 0, 0.1, 0.25.
Question: can SPARC see the +0.02-0.05 dex bump at 2-10 a0?  Checks can fail."""
import os, sys, math, io, contextlib, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); src = open(os.path.join(HERE, "f25_profiled_kernel_comparison_mu10.py")).read()
head = src[:src.index("CUBE = {k: loss_cube(k, UPS) for k in KERN}")]
g = {"__file__": os.path.join(HERE, "f25_profiled_kernel_comparison_mu10.py"), "__name__": "f25head"}
buf = io.StringIO()
with contextlib.redirect_stdout(buf): exec(compile(head, "f25head", "exec"), g)
KERN, loss_cube, profiled, UPS, LOGA, NG, rng, info, P, ck = [g[k] for k in ("KERN", "loss_cube", "profiled", "UPS", "LOGA", "NG", "rng", "info", "P", "ck")]
print("=" * 100); print("g03l -- SPARC vs the candidate's monotone-completed kernel (f25 design: a_0 and Upsilon profiled, paired galaxy resampling)"); print("=" * 100)
print("  " + [l for l in buf.getvalue().splitlines() if "SPARC:" in l][0].strip())
Y1 = 1 - 1/math.e; nu_exp = KERN["mu_exp"]
def make_cand(p):
    def nu(y):
        y = np.asarray(y, float); hi = 1 + (1/math.e)*(y/Y1)**p/np.maximum(y, 1e-300)
        return np.where(y <= Y1, nu_exp(y), hi)
    return nu
for p in (0.0, 0.1, 0.25): KERN[f"cand_p{p}"] = make_cand(p)
g["KERN"] = KERN
yy = np.array([0.3, 0.632, 0.7, 1, 2, 3, 5, 10, 30, 100])
print("  kernels nu(y) at y = " + " ".join(f"{v:g}" for v in yy)); 
for k in ("nu_rar", "mu_exp", "cand_p0.0", "cand_p0.1", "cand_p0.25"): print(f"    {k:11s}: " + " ".join(f"{float(KERN[k](v)):.4f}" for v in yy))
cont = abs(float(KERN["cand_p0.0"](Y1*1.0001)) - float(KERN["mu_exp"](Y1*0.9999)))
ck("C1 the candidate kernel is continuous at y = 1 - 1/e and equals the exponential kernel below it", cont < 2e-3, f"jump {cont:.1e}")
CUBE = {k: loss_cube(k, UPS) for k in KERN}
W0 = np.full((1, NG), 1.0/NG); REPS = 999; W = rng.multinomial(NG, np.full(NG, 1.0/NG), size=REPS)/NG
res = {}
for k in KERN:
    full, (iu, ia) = profiled(CUBE[k], W0); boot, _ = profiled(CUBE[k], W)
    res[k] = dict(full=float(full[0]), ups=float(UPS[iu[0]]), a0=10**float(LOGA[ia[0]]), boot=boot)
    print(f"  {k:11s}: profiled MSE = {res[k]['full']:.5f} dex^2 at Upsilon = {res[k]['ups']:.2f}, a_0 = {res[k]['a0']:.3e}")
def pair(a, b):
    d = res[a]["boot"] - res[b]["boot"]; pc = np.percentile(d, [2.5, 50, 97.5]); return pc, float(np.mean(d > 0))
pc0, f0 = pair("mu_exp", "nu_rar")
print(f"  paired MSE(mu_exp) - MSE(nu_rar): [{pc0[0]:+.5f}, {pc0[1]:+.5f}, {pc0[2]:+.5f}] dex^2, fraction > 0: {f0:.3f}   (f25: interval contains zero)")
ck("R1 f25's result reproduces: the exp-vs-RAR paired difference's 95% interval contains zero", pc0[0] < 0 < pc0[2])
verdicts = {}
for p in (0.0, 0.1, 0.25):
    k = f"cand_p{p}"; pcE, fE = pair(k, "mu_exp"); pcR, fR = pair(k, "nu_rar"); verdicts[p] = (pcE, fE, pcR, fR)
    print(f"  paired MSE({k}) - MSE(mu_exp): [{pcE[0]:+.5f}, {pcE[1]:+.5f}, {pcE[2]:+.5f}] (frac > 0 {fE:.3f});  - MSE(nu_rar): [{pcR[0]:+.5f}, {pcR[1]:+.5f}, {pcR[2]:+.5f}] (frac > 0 {fR:.3f})")
undecided = [p for p in verdicts if verdicts[p][0][0] < 0 < verdicts[p][0][2]]
worse = [p for p in verdicts if verdicts[p][0][0] > 0]; better = [p for p in verdicts if verdicts[p][0][2] < 0]
print(f"  verdict vs the exponential kernel with a_0 and Upsilon profiled: undecided for p = {undecided}; disfavoured (95%) for p = {worse}; favoured (95%) for p = {better}")
ck("S1 the SPARC verdict on the monotone completion is REPORTED, not manufactured: for each p the paired difference vs the exponential kernel is classified as undecided / disfavoured / favoured by its 95% interval, and at least the saturated case p = 0 is not favoured at 95%", 0.0 not in better)
print(f"\nRESULT: {len(ck.fails)} FAIL -> {ck.fails}" if hasattr(ck, "fails") else "")
