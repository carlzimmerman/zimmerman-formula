#!/usr/bin/env python3
"""L266 -- THE TIGHTNESS GATE of the emergent reading: can LCDM halo scatters reproduce the BTFR's intrinsic scatter?

At fixed V_flat the BTFR residual in log M_b equals (minus) the residual of log a0_eff = log(V_max^4/(G M_b)), so the emergent
reading predicts sigma_int(log M_b | V) = sigma(log a0_eff) from the population scatters at fixed halo mass:
    d log a0_eff = A d log c - d log M_b,      A = 4 d log(V_max/V_200)/d log c   (NFW: V_max/V_200 = sqrt(0.216 c/f(c)))
    d log M_b    = k d log c + eps,             k = rho sigma_b/sigma_c (assembly bias: concentration-stellar-mass correlation), eps independent
so  sigma^2(log a0_eff) = (A - k)^2 sigma_c^2 + (1 - rho^2) sigma_b^2.
Literature inputs (ranges carried): sigma_c = 0.11 dex (Dutton & Maccio 2014; Diemer & Kravtsov 0.10-0.13); sigma_* at fixed M_h =
0.15-0.20 dex (Wechsler & Tinker 2018; Behroozi+19); gas-fraction scatter 0.25-0.35 dex at fixed M_* (Bradford+15), entering M_b with
weight f_g/(1+f_g); rho(M_* residual, c) = 0.5-0.7 (Matthee+17 EAGLE, Zehavi+18); observed BTFR intrinsic scatter sigma_obs = 0.10 +- 0.02 dex
in log M_b at fixed V_flat (Lelli+16, McGaugh 2012 <= 0.11).  Gates fixed first:
  T1  without assembly bias (rho = 0) the predicted scatter exceeds the observed by > 1.5x (the Desmond 2017 tension reproduced);
  T2  with rho = 0.5-0.7 the predicted scatter is within 1.3x of the observed for the stellar-dominated (MW-mass) population;
  T3  the same for the gas-dominated dwarf population (f_g ~ 3), where the gas scatter enters and the SMHM is steepest.
Both a0 footings do not enter (a ratio of scatters).  A FAIL is a finding."""
import os, json, math
import numpy as np
CH, OUT = [], {}
def check(n, ok, d=""):
    CH.append(bool(ok)); print(f"  [{'PASS' if ok else 'FAIL'}] {n}" + (f"\n           ({d})" if d else ""), flush=True)
print("L266 -- the tightness gate of the emergent reading\n")
def A_of(c):
    f = lambda cc: math.log(1 + cc) - cc / (1 + cc)
    g = lambda cc: 0.5 * math.log10(0.216 * cc / f(cc))
    return 4 * (g(c * 1.01) - g(c * 0.99)) / (math.log10(1.01) - math.log10(0.99))
SIG_OBS = (0.10, 0.02)
pops = {"MW-mass, stellar-dominated (c ~ 8.5, f_g ~ 0.15)": dict(c=8.5, fg=0.15), "dwarf, gas-dominated (c ~ 12, f_g ~ 3)": dict(c=12.0, fg=3.0)}
grid = dict(sigma_c=(0.10, 0.11, 0.13), sigma_star=(0.15, 0.175, 0.20), sigma_gas=(0.25, 0.30, 0.35), rho=(0.0, 0.5, 0.6, 0.7))
for name, p in pops.items():
    A = A_of(p["c"]); w = p["fg"] / (1 + p["fg"])
    print("=" * 100); print(f"{name}: A = 4 d log(V_max/V_200)/d log c = {A:.3f}; gas weight in M_b = {w:.2f}"); print("=" * 100)
    res = {}
    for rho in grid["rho"]:
        vals = []
        for sc in grid["sigma_c"]:
            for ss in grid["sigma_star"]:
                for sg in grid["sigma_gas"]:
                    sb = math.sqrt(ss ** 2 + (w * sg) ** 2)   # log M_b = log M_* + log(1+f_g): d log M_b = d log M_* + w d log f_g
                    k = rho * sb / sc
                    s = math.sqrt((A - k) ** 2 * sc ** 2 + (1 - rho ** 2) * sb ** 2)
                    vals.append(s)
        res[rho] = (min(vals), float(np.median(vals)), max(vals))
        print(f"    rho = {rho:.1f}: predicted sigma(log M_b | V) = {res[rho][1]:.3f} dex  [range {res[rho][0]:.3f}-{res[rho][2]:.3f}]  = {res[rho][1]/SIG_OBS[0]:.2f}x observed {SIG_OBS[0]} +- {SIG_OBS[1]}")
    OUT[name] = {str(k_): v for k_, v in res.items()}
    if "MW" in name:
        check("T1 without assembly bias the emergent scatter exceeds the observed by > 1.5x (the Desmond 2017 tension)", res[0.0][1] / SIG_OBS[0] > 1.5, f"{res[0.0][1]/SIG_OBS[0]:.2f}x")
        check("T2 with rho = 0.5-0.7 the MW-mass emergent scatter is within 1.3x of the observed (median over the input ranges, best rho)",
              min(res[r][1] for r in (0.5, 0.6, 0.7)) / SIG_OBS[0] <= 1.3, f"best {min(res[r][1] for r in (0.5, 0.6, 0.7))/SIG_OBS[0]:.2f}x at rho = 0.7; rho = 0.5: {res[0.5][1]/SIG_OBS[0]:.2f}x")
    else:
        check("T3 with rho = 0.5-0.7 the gas-dominated dwarf emergent scatter is within 1.3x of the observed",
              min(res[r][1] for r in (0.5, 0.6, 0.7)) / SIG_OBS[0] <= 1.3, f"best {min(res[r][1] for r in (0.5, 0.6, 0.7))/SIG_OBS[0]:.2f}x; the gas scatter (0.25-0.35 dex, uncorrelated with c) dominates and does not cancel")
n, n_pass = len(CH), sum(CH)
print(f"\nL266 COMPLETE: {n_pass}/{n} checks PASS.")
print("READING: assembly bias narrows the Desmond gap for stellar-dominated galaxies (2.0x -> 1.3-1.55x, marginal), but for gas-dominated dwarfs the")
print("gas-fraction scatter, which no halo property correlates with, leaves the emergent scatter 2.2-2.4x the observed unless the observed dwarf")
print("scatter is itself larger (Lelli+16 report the gas-rich BTFR scatter is NOT larger).  This is the sharpest live tension for the emergent")
print("reading and the sharpest live support for a universal scale: the gas-rich dwarfs are where the two readings differ, and the record's G114")
print("(55 gas-dominated dwarfs, 0.150 dex rms about g^2 = a0 g_N, zero bias) is the number to beat with a full LCDM population model.")
json.dump(dict(pass_=n_pass, n=n, parts=OUT), open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "L266_results.json"), "w"), indent=1, default=str)
