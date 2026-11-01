#!/usr/bin/env python3
"""MH1 T1, post-result, no label: why K-T1 failed. Shell N halo against LC1's NFW c 12.95, and Blumenthal on the shell halo's own profile. kappa = 1/2 FITTED, unused; not theory closed."""
import json, math, os, re, numpy as np
H = os.path.dirname(os.path.abspath(__file__)); s = open(os.path.join(H, "mh1_t1.py")).read().replace("main()\n", "", 1) if False else open(os.path.join(H, "mh1_t1.py")).read(); s = s[:s.rindex("main()")]; ns = {"__file__": os.path.join(H, "mh1_t1.py")}; exec(s, ns)
ns["SR"] = tuple(np.geomspace(0.1, 150, 60)); run = ns["run"]; Rd = 3.565; Md = 6.7187942657e10; rg = np.array(ns["SR"]) * Rd
out = {}
for p in (.2, .05):
    N0 = np.array(run(1e12, 0, Rd, "N", p)); L = np.array(run(1e12, Md, Rd, "L", p)); Mb = Md * (1 - (1 + rg / Rd) * np.exp(-rg / Rd)); F = Md / 1e12; ri = rg.copy(); rf = ri.copy(); M0c = N0 * (1 - F)
    for _ in range(100): rf = .5 * rf + .5 * ri * N0 / (np.interp(np.log(rf), np.log(rg), Mb) + M0c)
    Bl = np.interp(np.log(rg), np.log(np.maximum.accumulate(rf)), M0c); c = 12.95; R200 = 213.0; mu = lambda x: math.log(1 + x) - x / (1 + x); nfw = lambda r: 1e12 * mu(c * r / R200) / mu(c); i3 = int(np.argmin(abs(rg - 3 * Rd))); out[str(p)] = dict(N_3Rd=float(N0[i3]), nfw_3Rd=nfw(3 * Rd), Q_live=float(L[i3] / N0[i3]), Q_blum=float(Bl[i3] / N0[i3])); print(p, out[str(p)], flush=True)
json.dump(out, open(os.path.join(H, "mh1_t1_post.json"), "w"), indent=1)
