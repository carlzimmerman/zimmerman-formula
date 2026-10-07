#!/usr/bin/env python3
"""CFG474: cold-mass window from UFD cold-dominance + the UFD heating bound + superradiance (FROZEN_CRITERIA.md). Run: python3 cfg474_window.py [--mutate]"""
import os, sys, json, math, io, contextlib
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE)
MUT = "--mutate" in sys.argv; TAG = "_MUTATE" if MUT else ""
OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))
src = os.path.join(LANES, "CFG440_council_promoted", "session02_calcs", "fossil_switch.py")
g = {"__file__": src, "__name__": "fs"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open(src).read().split("j317 = json.load")[0], g)       # data loader + estimator only
RES, UL, sig_pred = g["RES"], g["UL"], g["sig_pred"]
G, MSUN, PC = 6.674e-11, 1.989e30, 3.0857e16
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}
def nu(y): y = max(y, 1e-12); return 1 / (1 - math.exp(-math.sqrt(y)))
res = {}; dom = {}
for foot, a0 in A0.items():
    fc = []; seg = None
    for d in RES:
        Mb = 2 * d["LV"] + 1.33 * d["MHI"]; r = 4 / 3 * d["rh"] * PC
        gN = G * 0.5 * Mb * MSUN / r ** 2
        Mlaw = nu(gN / a0) * gN * r ** 2 / G / MSUN * (20 if MUT else 1)
        Mdyn = 3 * (d["sig"] * 1e3) ** 2 * r / G / MSUN
        f = (Mdyn - Mlaw) / Mdyn; fc.append(f)
        if d["name"] == "Segue 1": seg = dict(Mdyn=Mdyn, Mlaw=Mlaw, f=f)
    fc = np.array(fc); med = float(np.median(fc)); frac = float((fc >= 0.5).mean())
    ok = med >= 0.6 and seg["f"] >= 0.8
    dom[foot] = ok
    res[foot] = dict(median_f_cold=med, frac_ge_half=frac, segue1=seg, cold_dominated=ok)
    P(f"{foot:9s}: median f_cold {med:.3f}; f_cold >= 0.5 in {frac:.2f} of {len(fc)}; Segue 1: M_dyn {seg['Mdyn']:.3e}, M_law {seg['Mlaw']:.3e}, f_cold {seg['f']:.3f} -> {'COLD-DOMINATED' if ok else 'NOT COLD-DOMINATED'}")
k1 = abs(res["canonical"]["segue1"]["Mdyn"] / 2.86e5 - 1) < 0.01 and (MUT or abs(res["canonical"]["segue1"]["Mlaw"] / 1.15e4 - 1) < 0.01)
P(f"K1 Segue 1 vs CFG440 s03 (2.86e5 / 1.15e4): {'PASS' if k1 else 'FAIL'}")
P("Segue 2 (in the heating bound's sample): LVD gives only an upper-limit sigma -> " + ", ".join(f"{d['name']} sigma_ul {d['sig_ul']}" for d in UL if d["name"] == "Segue 2"))
c367 = json.load(open(os.path.join(LANES, "CFG367_superradiance_window", [f for f in os.listdir(os.path.join(LANES, "CFG367_superradiance_window")) if f.endswith("results.json") and "MUTATE" not in f][0])))
surv = c367["primary"]["surviving"]
k2 = abs(surv[0][0] / 2.0e-20 - 1) < 0.01 and abs(surv[0][1] / 4.4e-20 - 1) < 0.02
P(f"K2 CFG367 light end {surv[0][0]:.3e}-{surv[0][1]:.3e} eV -> {'PASS' if k2 else 'FAIL'}")
HC = 1.97327e-7; CK = 2.99792e5
lam_pc = lambda m, v: 2 * math.pi * HC / m * CK / v / 3.0857e16          # de Broglie length, pc
cold_all = all(dom.values())
MBOUND = 3e-19
new = []
for lo, hi in surv:
    if hi < MBOUND and cold_all: continue
    lo2 = max(lo, MBOUND) if cold_all else lo
    if lo2 <= hi: new.append([lo2, hi])
P(f"surviving windows {'after m > 3e-19 eV (conditional on c1-c3)' if cold_all else '(bound NOT applied: UFDs not cold-dominated)'}:")
for lo, hi in new:
    P(f"   {lo:.3e} - {hi:.3e} eV | lambda_dB at 10 km/s: {lam_pc(lo,10):.3g}-{lam_pc(hi,10):.3g} pc; at 200 km/s: {lam_pc(lo,200):.3g}-{lam_pc(hi,200):.3g} pc")
json.dump(dict(step1=res, K1=bool(k1), K2=bool(k2), surviving_before=surv, surviving_after=new, bound_applied=cold_all), open(os.path.join(HERE, f"cfg474_window{TAG}_results.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg474_window{TAG}.out"), "w").write("\n".join(OUT) + "\n")
if MUT:
    ok = not any(dom.values()); P(f"MUTATE: NOT COLD-DOMINATED -> {'detected (exit 1)' if ok else 'NOT detected'}"); sys.exit(1 if ok else 0)
sys.exit(0 if (k1 and k2) else 1)
