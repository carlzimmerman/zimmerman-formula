#!/usr/bin/env python3
"""CFG539 post-hoc diagnostic (not a verdict input; added after the first 256^3 results, 2026-10-10): the bookkeeping engines' T4 numbers
(CFG527/530) are P(k) of the PARTICLES, while their gravitating density is particles + (e - comp).  In the CFG539 two-species engine the settled
cold energy IS particles.  Like-for-like: P(k) of CFG530's bookkeeping GRAVITATING density (CFG530 profile caches rho_g at z = 0) vs S0."""
import os, sys, json, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import cfg539_profiles as PR
out = {}
for L in (100, 200):
    for N in (128, 256):
        mod = PR.load_engine(f"Acan_L{L}_N{N}"); mesh = mod.Mesh(N)
        d = os.path.join(PR.W530, "profiles", f"N{N}")
        s0 = np.load(os.path.join(d, f"cfg526_S0_L{L}_rhop.npy")).astype(np.float32) - 1
        k, p0, s80 = mod.measure_pk(mesh, s0, N ** 3)
        for run in ("LRcan", "LRalt"):
            f = os.path.join(d, f"cfg526_{run}_L{L}_rhog.npy")
            if not os.path.exists(f): continue
            g = np.load(f).astype(np.float32) - 1
            _, pg, s8 = mod.measure_pk(mesh, g, N ** 3)
            k_ = np.array(k); r = np.array(pg) / np.array(p0); m = k_ <= min(1.0, math.pi * N / L / 4)
            at = lambda kk: float(r[int(np.argmin(np.abs(k_ - kk)))]) if kk <= math.pi * N / L / 2 else None
            out[f"{run}_L{L}_N{N}"] = {"sigma8_ratio_grav": s8 / s80, "max_abs_r_minus_1_grav": float(np.max(np.abs(r[m] - 1))),
                                      "r_grav": {str(kk): at(kk) for kk in (0.5, 1.0, 2.0, 4.0)}}
            print(f"{run}_L{L}_N{N}", json.dumps(out[f"{run}_L{L}_N{N}"]))
json.dump(out, open(os.path.join(HERE, "cfg539_posthoc_grav_pk.json"), "w"), indent=1)
