#!/usr/bin/env python3
"""Addendum F (FROZEN_CRITERIA.md): fossil-phantom switch keyed on de Broglie length vs r_1/2. Reuses AUDIT_UFD's estimator
and CFG317's R_ind exactly as AUDIT_UFD section 7 does. Run: python3 fossil_switch.py -> fossil_switch.out/_results.json."""
import os, sys, json, math, csv
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
OUT = []
def P(s=""): print(s); OUT.append(str(s))
G, MSUN, PC = 6.674e-11, 1.989e30, 3.0857e16
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}; ERR = 0.086
HOM = lambda m: 1.97327e-7 / m * 2.99792e5 / PC          # hbar/m in pc km/s
def fnum(v):
    try: x = float(v); return x if np.isfinite(x) else None
    except (TypeError, ValueError): return None
def nu_exp(y): y = max(y, 1e-12); return 1 / (1 - math.exp(-math.sqrt(y)))
rows = list(csv.DictReader(open(os.path.join(REPO, "real_research/data/dsph/lvd_dwarf_mw.csv"))))
RES, UL, CL = [], [], []
for r in rows:
    MV = fnum(r["M_V"]); sig = fnum(r["vlos_sigma"]); ul = fnum(r["vlos_sigma_ul"])
    rh = fnum(r["rhalf_sph_physical"]) or fnum(r["rhalf_physical"]); Dh = fnum(r["distance_host"]) or fnum(r["distance_gc"])
    if MV is None or rh is None: continue
    d = dict(name=r["name"], LV=10 ** (0.4 * (4.83 - MV)), rh=rh, MHI=(10 ** fnum(r["mass_HI"]) if fnum(r["mass_HI"]) is not None else 0.0))
    if MV <= -7.7:
        if sig: d["sig"] = sig; CL.append(d)
        continue
    if Dh is None: continue
    if sig is not None and ul is None and sig > 0: d["sig"] = sig; RES.append(d)
    elif ul is not None: d["sig_ul"] = ul; UL.append(d)
def sig_pred(d, a0, fac):
    Mb = (2 * d["LV"] + 1.33 * d["MHI"]) * fac; r = 4 / 3 * d["rh"] * PC
    gN = G * 0.5 * Mb * MSUN / r ** 2; return math.sqrt(gN * nu_exp(gN / a0) * r / 3) / 1e3
def km_median(x, xu):
    y = np.concatenate([-np.asarray(x), -np.asarray(xu)]); ev = np.concatenate([np.ones(len(x), bool), np.zeros(len(xu), bool)])
    o = np.lexsort((~ev, y)); y, ev = y[o], ev[o]; S, n, i = 1.0, len(y), 0
    while i < len(y):
        t = y[i]; j = i; dd = 0; cc = 0
        while j < len(y) and y[j] == t: dd += ev[j]; cc += (not ev[j]); j += 1
        if dd: S *= 1 - dd / n
        if S <= 0.5: return -t
        n -= dd + cc; i = j
    return -y[-1]
j317 = json.load(open(os.path.join(REPO, "campaign_fresh_gravity/CFG317_baryon_loss_cold_mass/cfg317_baryon_loss_results.json")))["numbers"]
res = {}
P(f"Addendum F: fossil-phantom switch | sample {len(RES)}+{len(UL)} UFDs, {len(CL)} classicals with sigma")
for m in (2.0e-20, 4.4e-20):
    lam = lambda d: 2 * math.pi * HOM(m) / d.get("sig", d.get("sig_ul"))
    cl_switch = [d["name"] for d in CL if lam(d) > 4 / 3 * d["rh"]]
    for yv in ("-0.2", "-0.5", "0.1"):
        Rres = {nm: (10 ** e["lR"] if e and e.get("lR") is not None else 1.0) for nm, e in zip(j317["NAMES"]["ufd"], j317["EST"][yv + "|ufd"])}
        Rul = [(10 ** e["lR"] if e and e.get("lR") is not None else 1.0) for e in j317["EST"][yv + "|ul"]]
        sw = sum(lam(d) > 4 / 3 * d["rh"] for d in RES + UL)
        for foot, a0 in A0.items():
            fr = lambda d, R: R if lam(d) > 4 / 3 * d["rh"] else 1.0
            x = [math.log10(d["sig"] / sig_pred(d, a0, fr(d, Rres[d["name"]]))) for d in RES]
            xu = [math.log10(d["sig_ul"] / sig_pred(d, a0, fr(d, R))) for d, R in zip(UL, Rul)]
            med = km_median(x, xu); res[f"{m}|{yv}|{foot}"] = dict(median=med, z=med / ERR, switched=int(sw), classicals_switched=cl_switch)
            P(f"  m {m:.1e} yield {yv:>4s} {foot:9s}: switched {sw}/40 UFDs, classicals switched {len(cl_switch)}; KM median {med:+.3f} dex ({med/ERR:+.2f} sigma)")
nom = [res[f"{m}|-0.2|{f}"]["median"] for m in (2.0e-20, 4.4e-20) for f in A0]
v = "PASS" if all(abs(x) < 2 * ERR for x in nom) else "FAIL"
P(f"VERDICT (nominal yield, both footings, both m): {v}")
json.dump(dict(results=res, verdict=v), open(os.path.join(HERE, "fossil_switch_results.json"), "w"), indent=1)
open(os.path.join(HERE, "fossil_switch.out"), "w").write("\n".join(OUT) + "\n")
