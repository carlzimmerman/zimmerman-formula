#!/usr/bin/env python3
"""Session 4, test C: the Session-3 supply rule on the MW classical dwarfs. Run: python3 classicals_supply.py [--mutate]"""
import os, sys, csv, json, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
MUT = "--mutate" in sys.argv; TAG = "_MUTATE" if MUT else ""
OUT = []
def P(s=""): print(s); OUT.append(str(s))
G, MSUN, PC = 6.674e-11, 1.989e30, 3.0857e16
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}; COSMIC = 0.1200 / 0.02237; FGAL = 0.0 if MUT else 0.13
def nu_exp(y): y = max(y, 1e-12); return 1 / (1 - math.exp(-math.sqrt(y)))
def fnum(v):
    try: x = float(v); return x if np.isfinite(x) else None
    except (TypeError, ValueError): return None
j = json.load(open(os.path.join(REPO, "campaign_fresh_gravity/CFG317_baryon_loss_cold_mass/cfg317_baryon_loss_results.json")))["numbers"]
rows = {r["name"]: r for r in csv.DictReader(open(os.path.join(REPO, "real_research/data/dsph/lvd_dwarf_mw.csv")))}
def obj(r):
    MV = fnum(r["M_V"]); sig = fnum(r["vlos_sigma"]); rh = fnum(r["rhalf_sph_physical"]) or fnum(r["rhalf_physical"])
    if MV is None or sig is None or rh is None: return None
    return dict(name=r["name"], LV=10 ** (0.4 * (4.83 - MV)), rh=rh, sig=sig, MHI=(10 ** fnum(r["mass_HI"]) if fnum(r["mass_HI"]) is not None else 0.0))
def pieces(d, a0):
    Mb = 2 * d["LV"] + 1.33 * d["MHI"]; r = 4 / 3 * d["rh"] * PC
    gN = G * 0.5 * Mb * MSUN / r ** 2
    return Mb, r, nu_exp(gN / a0) * gN * r ** 2 / G / MSUN
def offsets(objs, Rs, a0, q, f=FGAL):
    out = []
    for d, R in zip(objs, Rs):
        Mb, r, Ml = pieces(d, a0)
        sp = math.sqrt(G * (Ml + q * f * COSMIC * R * Mb) * MSUN / (3 * r)) / 1e3
        out.append(math.log10(d["sig"] / sp))
    return np.array(out)
def q_zero(objs, Rs, a0):
    from scipy.optimize import brentq
    g = lambda lq: np.median(offsets(objs, Rs, a0, 10 ** lq, 0.13))
    try: return 10 ** brentq(g, -4, 2)
    except ValueError: return float("nan")
# UFDs, same formula (for the q comparison)
ufd = []; Ru = {}
for nm, e in zip(j["NAMES"]["ufd"], j["EST"]["-0.2|ufd"]):
    if e and e.get("lR") is not None and nm in rows:
        d = obj(rows[nm])
        if d and fnum(rows[nm]["vlos_sigma_ul"]) is None: ufd.append(d); Ru[nm] = 10 ** e["lR"]
res = {}
for yv in ("-0.2", "-0.5", "0.1"):
    cls, Rc, skipped = [], [], []
    for nm, e in zip(j["NAMES"]["cls"], j["EST"][yv + "|cls"]):
        d = obj(rows[nm]) if nm in rows else None
        if d is None or not e or e.get("lR") is None: skipped.append(nm); continue
        cls.append(d); Rc.append(10 ** e["lR"])
    for foot, a0 in A0.items():
        for q in (1.0, 0.5):
            x = offsets(cls, Rc, a0, q); med = float(np.median(x))
            bs = [np.median(x[np.random.default_rng(21 + k).integers(0, len(x), len(x))]) for k in range(2000)]
            err = math.hypot(float(np.std(bs)), 0.077)
            v = "BROKEN" if med < -3 * err else "CONSISTENT" if abs(med) < 2 * err else "STRAINED"
            res[f"{yv}|{foot}|q{q}"] = dict(median=med, err=err, verdict=v, n=len(cls))
            P(f"yield {yv:>4s} {foot:9s} q {q}: classicals N {len(cls)} median {med:+.3f} +- {err:.3f} -> {v}")
        x0 = offsets(cls, Rc, a0, 1.0, 0.0)
        qc = q_zero(cls, Rc, a0); qu = q_zero(ufd, [Ru[d["name"]] for d in ufd], a0) if yv == "-0.2" else float("nan")
        res[f"{yv}|{foot}|qzero"] = dict(law_only=float(np.median(x0)), q_cls=qc, q_ufd=qu)
        P(f"   law only: {np.median(x0):+.3f}; q zeroing classicals {qc:.3g}" + (f"; q zeroing UFDs {qu:.3g}; ratio {qu/qc:.1f}" if yv == "-0.2" else ""))
    if yv == "-0.2":
        P(f"   excluded (no R_ind / data): {', '.join(skipped)}")
        P("   per object (canonical, q=1): name | M_b | R_ind | offset law-only | offset with rule")
        for d, R in zip(cls, Rc):
            P(f"     {d['name']:18s} {pieces(d, A0['canonical'])[0]:9.2e} {R:6.1f} {offsets([d],[R],A0['canonical'],1.0,0.0)[0]:+.3f} {offsets([d],[R],A0['canonical'],1.0,0.13)[0]:+.3f}" + ("  (tidally disrupting)" if d["name"] == "Sagittarius" else ""))
json.dump(res, open(os.path.join(HERE, f"classicals_supply{TAG}_results.json"), "w"), indent=1)
open(os.path.join(HERE, f"classicals_supply{TAG}.out"), "w").write("\n".join(OUT) + "\n")
rc = 0
if MUT:
    m = res["-0.2|canonical|q1.0"]["median"]; P(f"MUTATE: median {m:+.3f} (law-only expected ~+0.10)")
    rc = 1 if abs(m - 0.10) < 0.02 else 0
sys.exit(rc)
