#!/usr/bin/env python3
"""cfg157_posthoc_numono -- POST-HOC (written after my main runs were saved and after CFG121's outputs were opened; labelled, not part of the frozen headline).
Question: does the 0.4% difference at 1e12 in T1.5 (mine 0.6253 with my reconstructed nu_mono vs CFG121's 0.623) come from the kernel definition?
Imports CFG44's Bcommon nu_mono READ-ONLY (needs ZF_REPO or the script inside the repo) and re-runs my finite-difference route with it.
Exit 0 (report only)."""
import os, sys, math, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cfg157_common as C
repo = C.find_repo()
if repo is None:
    print("needs ZF_REPO (repo root containing campaign_fresh_gravity/); exit 2"); sys.exit(2)
sys.path.insert(0, os.path.join(repo, "campaign_fresh_gravity", "CFG44_fluid_target"))
sys.dont_write_bytecode = True
import Bcommon as B
C.KERNELS["bcommon"] = (lambda y: np.asarray(B.nu_mono(y), float), None)
out = open(os.path.join(C.HERE, "cfg157_posthoc_numono.out"), "w")
def P(s):
    print(s); out.write(s + "\n")
P("POST-HOC: T1.5 with CFG44 Bcommon.nu_mono (read-only import; path printed as <repo>/campaign_fresh_gravity/CFG44_fluid_target/Bcommon.py) vs my reconstruction, FD route")
x = C.grid_x(121)
res = {}
for fn, a0 in C.A0.items():
    for M in C.MASSES:
        sph = C.ExpSphere(M * C.MSUN, C.h_of_M(M))
        r = x * C.rM(sph.M, a0, C.G_CFG121)
        d_b = C.route_fd(sph, "bcommon", 1.0, a0, C.G_CFG121, r) - 1
        d_m = C.route_fd(sph, "mono", 1.0, a0, C.G_CFG121, r) - 1
        res[f"{fn},{M:g}"] = (float(abs(d_b).max()), float(abs(d_m).max()), float(x[np.argmax(abs(d_b))]))
        P("  %-9s M=%.0e: Bcommon nu_mono max|dev| = %.4f (at x=%.3f)   reconstructed = %.4f" % (fn, M, res[f"{fn},{M:g}"][0], res[f"{fn},{M:g}"][2], res[f"{fn},{M:g}"][1]))
y = np.array([1.0, 2.0, 2.54, 3.0, 10.0, 30.0, 100.0])
P("  kernel values nu-1 at y=%s:  Bcommon %s   reconstructed %s" % (y.tolist(), np.round(B.nu_mono(y) - 1, 5).tolist(), np.round(C.nu_mono(y) - 1, 5).tolist()))
json.dump(res, open(os.path.join(C.HERE, "cfg157_posthoc_numono_results.json"), "w"), indent=1)
out.close()
