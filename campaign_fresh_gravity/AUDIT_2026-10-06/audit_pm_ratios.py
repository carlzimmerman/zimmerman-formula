#!/usr/bin/env python3
"""Audit (read-only): S0 identity checks and sigma8 / P(k<=1) ratios at z1, z0.5, z0 for CFG366/372/374 from the PM work JSONs.
No PM run. Reads ../../../_external_data/cfg3{59,66,72,74}_work/."""
import os, json, glob, numpy as np
X = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "_external_data"))
s0r = json.load(open(os.path.join(X, "cfg359_work", "cfg359_S0_FLAT_canonical_N256.json"))); s0 = s0r["snap"]
print("S0: nsteps", s0r["nsteps"], "np", s0r["np"], "z_i", s0r["z_i"], "L", s0r["L"])
fs = sorted(glob.glob(os.path.join(X, "cfg366_work", "*N256.json"))) + sorted(glob.glob(os.path.join(X, "cfg372_work", "cfg372_*N256.json"))) + sorted(glob.glob(os.path.join(X, "cfg374_work", "cfg374_*N256.json")))
for f in fs:
    r = json.load(open(f)); s = r["snap"]
    same = (r["nsteps"], r["np"], r["z_i"], r["L"]) == (s0r["nsteps"], s0r["np"], s0r["z_i"], s0r["L"]) and np.array_equal(s["zi"]["P"], s0["zi"]["P"])
    o = [os.path.basename(f)[:44].ljust(44), "ICs+steps identical to S0" if same else "DIFFERENT FROM S0", f"overdraw z0 {s['z0'].get('overdraw_mass')}"]
    for z in ("z1", "z0.5", "z0"):
        k = np.array(s[z]["k"]); p = np.array(s[z]["P"]); m = k <= 1
        pr = p[m] / np.interp(k[m], np.array(s0[z]["k"]), np.array(s0[z]["P"]))
        o.append(f"{z}: s8 {s[z]['sigma8']/s0[z]['sigma8']:.4f} max|P-1| {abs(pr-1).max():.3f}")
    print(" | ".join(o))
