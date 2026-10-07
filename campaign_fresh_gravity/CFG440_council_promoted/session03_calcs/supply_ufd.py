#!/usr/bin/env python3
"""Session 3, Addendum B: can (Omega_c/Omega_b) x original baryons pay for the UFDs' missing mass? Run: python3 supply_ufd.py [--mutate]"""
import os, sys, json, math, io, contextlib, runpy
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
MUT = "--mutate" in sys.argv; TAG = "_MUTATE" if MUT else ""
with contextlib.redirect_stdout(io.StringIO()):
    g = runpy.run_path(os.path.join(HERE, "..", "session02_calcs", "fossil_switch.py"))
RES, j317 = g["RES"], g["j317"]
OUT = []
def P(s=""): print(s); OUT.append(str(s))
G, MSUN, PC = 6.674e-11, 1.989e30, 3.0857e16
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}; COSMIC = 0.1200 / 0.02237
def nu_exp(y): y = max(y, 1e-12); return 1 / (1 - math.exp(-math.sqrt(y)))
res = {}
for yv in ("-0.2", "-0.5", "0.1"):
    R = {nm: (10 ** e["lR"] if e and e.get("lR") is not None else 1.0) for nm, e in zip(j317["NAMES"]["ufd"], j317["EST"][yv + "|ufd"])}
    for foot, a0 in A0.items():
        fs, rows = [], []
        for d in RES:
            Mb = 2 * d["LV"] + 1.33 * d["MHI"]; r = 4 / 3 * d["rh"] * PC
            gN = G * 0.5 * Mb * MSUN / r ** 2
            Mlaw = 0.0 if MUT else nu_exp(gN / a0) * gN * r ** 2 / G / MSUN
            Mdyn = 3 * (d["sig"] * 1e3) ** 2 * r / G / MSUN
            f = (Mdyn - Mlaw) / (COSMIC * R[d["name"]] * Mb)
            fs.append(f); rows.append((d["name"], Mb, R[d["name"]], Mdyn, Mlaw, f))
        fs = np.array(fs); med = float(np.median(fs))
        v = "VIABLE" if med <= 0.13 else "STRAINED" if med <= 0.6 else "OVER-CLUSTER" if med <= 1 else "EXCLUDED"
        res[f"{yv}|{foot}"] = dict(median=med, p16=float(np.percentile(fs, 16)), p84=float(np.percentile(fs, 84)), frac_gt1=float((fs > 1).mean()), verdict=v)
        P(f"yield {yv:>4s} {foot:9s}: median f_min {med:.2f} (16-84% {np.percentile(fs,16):.2f}..{np.percentile(fs,84):.2f}); f_min > 1 in {(fs>1).sum()}/{len(fs)} -> {v}")
        if yv == "-0.2" and foot == "canonical":
            P("   name | M_b now | R_ind | M_dyn(<r1/2) | M_law(<r1/2) | f_min")
            for nm, Mb, Ri, Md, Ml, f in sorted(rows, key=lambda x: -x[5]):
                P(f"   {nm:20s} {Mb:9.2e} {Ri:7.1f} {Md:9.2e} {Ml:9.2e} {f:7.2f}")
json.dump(res, open(os.path.join(HERE, f"supply_ufd{TAG}_results.json"), "w"), indent=1)
open(os.path.join(HERE, f"supply_ufd{TAG}.out"), "w").write("\n".join(OUT) + "\n")
rc = 0
if MUT:
    main = json.load(open(os.path.join(HERE, "supply_ufd_results.json")))
    rose = res["-0.2|canonical"]["median"] - main["-0.2|canonical"]["median"]
    P(f"MUTATE: median rose by {rose:+.3f}"); rc = 1 if rose > 0 else 0
sys.exit(rc)
