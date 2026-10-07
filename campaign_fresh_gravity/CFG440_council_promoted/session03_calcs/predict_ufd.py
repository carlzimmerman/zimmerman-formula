#!/usr/bin/env python3
"""Session 3, Addendum B2: zero-parameter UFD sigma from law + 0.13 x cosmic share of ORIGINAL baryons. Run: python3 predict_ufd.py [--mutate]"""
import os, sys, json, math, io, contextlib, runpy
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
MUT = "--mutate" in sys.argv; TAG = "_MUTATE" if MUT else ""
with contextlib.redirect_stdout(io.StringIO()):
    g = runpy.run_path(os.path.join(HERE, "..", "session02_calcs", "fossil_switch.py"))
RES, j317 = g["RES"], g["j317"]
OUT = []
def P(s=""): print(s); OUT.append(str(s))
G, MSUN, PC = 6.674e-11, 1.989e30, 3.0857e16
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}; COSMIC = 0.1200 / 0.02237; FGAL = 0.13
def nu_exp(y): y = max(y, 1e-12); return 1 / (1 - math.exp(-math.sqrt(y)))
res = {}
for yv in ("-0.2", "-0.5", "0.1"):
    Rraw = {nm: (10 ** e["lR"] if e and e.get("lR") is not None else None) for nm, e in zip(j317["NAMES"]["ufd"], j317["EST"][yv + "|ufd"])}
    use = [d for d in RES if Rraw.get(d["name"])]
    Rs = [Rraw[d["name"]] for d in use]
    if MUT: Rs = list(np.random.default_rng(17).permutation(Rs))
    for foot, a0 in A0.items():
        for q in (1.0, 0.5):
            off, base = [], []
            for d, R in zip(use, Rs):
                Mb = 2 * d["LV"] + 1.33 * d["MHI"]; r = 4 / 3 * d["rh"] * PC
                gN = G * 0.5 * Mb * MSUN / r ** 2
                Mlaw = nu_exp(gN / a0) * gN * r ** 2 / G / MSUN
                Mc = q * FGAL * COSMIC * R * Mb
                sp = math.sqrt(G * (Mlaw + Mc) * MSUN / (3 * r)) / 1e3
                spl = math.sqrt(G * Mlaw * MSUN / (3 * r)) / 1e3
                off.append(math.log10(d["sig"] / sp)); base.append(math.log10(d["sig"] / spl))
            off, base = np.array(off), np.array(base)
            med, sc, scb = float(np.median(off)), float(off.std(ddof=1)), float(base.std(ddof=1))
            if sc >= 0.201 or abs(med) > 3 * 0.086: v = "NOT SUPPORTED"
            elif abs(med) < 2 * 0.086: v = "SUPPORTED"
            else: v = "PARTIAL"
            res[f"{yv}|{foot}|q{q}"] = dict(median=med, scatter=sc, law_scatter=scb, n=len(use), verdict=v)
            P(f"yield {yv:>4s} {foot:9s} q {q}: N {len(use)}  median {med:+.3f}  scatter {sc:.3f} (bare law {scb:.3f}) -> {v}")
P(f"excluded (no R_ind): {', '.join(d['name'] for d in RES if not Rraw.get(d['name']))}")
json.dump(res, open(os.path.join(HERE, f"predict_ufd{TAG}_results.json"), "w"), indent=1)
open(os.path.join(HERE, f"predict_ufd{TAG}.out"), "w").write("\n".join(OUT) + "\n")
rc = 0
if MUT:
    main = json.load(open(os.path.join(HERE, "predict_ufd_results.json")))
    d_ = res["-0.2|canonical|q1.0"]["scatter"] - main["-0.2|canonical|q1.0"]["scatter"]
    P(f"MUTATE: scatter changed by {d_:+.3f}"); rc = 1 if d_ > 0.01 else 0
sys.exit(rc)
