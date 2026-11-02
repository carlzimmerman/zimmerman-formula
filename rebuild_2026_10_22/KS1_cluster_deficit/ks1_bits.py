#!/usr/bin/env python3
"""KS1: BK1's alphabet A against the best windows, BK1 engine read only. Reports raw hits, control, ceiling, bits. python3 ks1_bits.py. kappa = 1/2 FITTED; not theory closed."""
import json, math, os, sys
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); BK = os.path.join(os.path.dirname(HERE), "BK1_forced_kernel_scales"); sys.path.insert(0, BK)
import numpy as np, resource
from bk1_engine import *
R = json.load(open(os.path.join(HERE, "ks1_results.json"))); A0 = dict(canonical=9.360324825027975e-11, alt=1.1312e-10); CC = 2.99792458e8; GG = 6.6743e-11; FB = .15747293971651993; O = {}
for ft in ("canonical", "alt"):
    B = R["bits"][ft]["rows"]; W = []
    for x, tag in (("0.6", "x06"), ("1.0", "x1")):
        r = B[x]; W += [Window(f"HSE_{tag}", *r["hse"]), Window(f"KiDS_{tag}", *r["kids"]), Window(f"HSC_{tag}", *r["hsc"]), Window(f"total_{tag}", r["mid"], r["tot"])]
    kt = R["kterm"][ft]["one"]; W.append(Window("kterm_KiDS", float(kt["k"][0]), float(kt["s"][0])))
    T = Tree(dict(c=CC, G=GG, rho=(2 * A0[ft] / CC) ** 2 / GG, a0=A0[ft], f_b=FB))
    for d in (2, 3): T.layer(d)
    H, HG, rows, zh, st = search(T, TARGET_DIMS["none"], W, G2=False); cum = cumulative(H); O[ft] = {}
    for w in W:
        g = grade(cum, w); O[ft][w.name] = dict(value=w.value, sigma=w.sigma, ceiling=g["ceiling_bits"], dstar=g["dstar"], P=g.get("P"), bits=g.get("bits"), real5=g["depth"][5]["real"], ctrl5=g["depth"][5]["ctrl_mean"]); print(ft, w.name, f"{w.value:.2f} +- {w.sigma:.2f}", f"ceiling {g['ceiling_bits']:.2f}", f"d* {g['dstar']} P {g.get('P')} bits {g.get('bits')}", f"hits {g['depth'][5]['real']:.3e} vs control {g['depth'][5]['ctrl_mean']:.3e}", flush=True)
O["rss_GB"] = None; json.dump({k: v for k, v in O.items() if k != "rss_GB"}, open(os.path.join(HERE, "ks1_bits.json"), "w"), indent=0, sort_keys=True); print("peak GB", resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9)
