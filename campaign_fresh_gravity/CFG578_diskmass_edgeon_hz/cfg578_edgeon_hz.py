"""CFG578: DiskMass sigma_z with S4G edge-on disc thicknesses. Criteria: FROZEN_CRITERIA.md (3d8a5806f).

Executes CFG577's script head (functions only, unedited) and replaces each galaxy's h_z with the S4G 3.6 micron
relation log10(h_z/kpc) = 0.90 log10(h_R/kpc) - 0.81 (arXiv:2410.09762). MUTATE: CFG578_MUTATE=1 (a0 x10 in RM).
"""
import os, sys, json, math, copy
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SRC577 = os.path.join(HERE, "..", "CFG577_diskmass_grid", "cfg577_diskmass_grid.py")
h577 = open(SRC577).read().split("T0 = time.time()")[0]
n577 = {"__file__": os.path.abspath(SRC577), "__name__": "cfg577_head"}
os.environ.pop("CFG577_MUTATE", None)
exec(compile(h577, "cfg577_head", "exec"), n577)
fit_and_predict, median_ci, gal_dms = n577["fit_and_predict"], n577["median_ci"], n577["gal"]

MUTATE = os.environ.get("CFG578_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUTATE else ""
OUT, CHECKS = [], []


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)


def check(c, m):
    CHECKS.append((bool(c), m)); P(f"  [{'PASS' if c else 'FAIL'}] {m}"); return bool(c)


def hz_s4g(hR, dex=0.0):
    return 10 ** (0.90 * math.log10(hR) - 0.81 + dex)


def with_hz(fun):
    g = copy.deepcopy(gal_dms)
    for u in g:
        g[u]["hz"] = fun(g[u]["hR"])
    return g


def run(gals, foot, rad, mdl, a0m=1.0):
    return {u: fit_and_predict(g, rad, foot, mdl, a0mult_rm=a0m) for u, g in gals.items()}


def summ(per, label):
    rs = [p["r"] for p in per.values() if p]; Ys = [p["Y"] for p in per.values() if p]
    med, lo, hi, n = median_ci(rs); Ym = float(np.median(Ys)) if Ys else float("nan")
    gY = n >= 25 and 0.3 <= Ym <= 1.0; cons = 0.85 <= med <= 1.15 and gY
    P(f"  {label}: median r = {med:.3f} [{lo:.3f}, {hi:.3f}]  n = {n}/30  median Y_K = {Ym:.3f}  G-Y {'pass' if gY else 'FAIL'} -> {'CONSISTENT' if cons else 'not consistent'}")
    return dict(med=med, lo=lo, hi=hi, n=n, Ymed=Ym, gY=gY, consistent=cons)


P("=" * 100)
P(f"CFG578  DiskMass sigma_z with S4G edge-on h_z  {'*** MUTATE: a0 x10 in RM ***' if MUTATE else 'PRIMARY'}")
P("=" * 100)
ratio = [hz_s4g(g["hR"]) / g["hz"] for g in gal_dms.values()]
P(f"S4G h_z / DMS h_z over the sample: median {np.median(ratio):.3f}, range {min(ratio):.3f}-{max(ratio):.3f}")

P("\n--- P1 pipeline control (DMS h_z, canonical, 1.5 h_R) vs CFG577 (RM 1.342, PD 1.551)")
for mdl, ref in (("RM", 1.342), ("PD", 1.551)):
    s = summ(run(gal_dms, "canonical", 1.5, mdl), f"{mdl} DMS h_z")
    check(abs(s["med"] / ref - 1) < 0.005, f"P1 {mdl} reproduces CFG577 {ref} to 0.5% ({s['med']:.3f})")

g4 = with_hz(hz_s4g)
S, res = {}, {}
for foot in ("canonical", "alt"):
    for rad in (1.5, 2.2):
        for mdl in ("RM", "PD"):
            k = f"{mdl}_{foot}_{rad}"
            res[k] = run(g4, foot, rad, mdl, 10.0 if (MUTATE and mdl == "RM") else 1.0)
            S[k] = summ(res[k], f"{mdl:2s} {foot:9s} {rad} h_R  (S4G h_z)")
P("\n--- verdict (primary 1.5 h_R)")
calls = {}
for foot in ("canonical", "alt"):
    rm, pd = S[f"RM_{foot}_1.5"]["consistent"], S[f"PD_{foot}_1.5"]["consistent"]
    calls[foot] = "ROUND FAVOURED" if rm and not pd else "PD FAVOURED" if pd and not rm else "NOT DIAGNOSTIC"
    P(f"  [{foot}] {calls[foot]}")
overall = calls["canonical"] if calls["canonical"] == calls["alt"] else "SPLIT"
P(f"VERDICT: {overall}")
if MUTATE:
    P("MUTATE reading: RM (a0 x10) must NOT be consistent.")
else:
    P("\n--- reported: S4G scatter +-0.11 dex, canonical 1.5 h_R; Newtonian reference")
    for dex in (-0.11, +0.11):
        for mdl in ("RM", "PD"):
            summ(run(with_hz(lambda h, d=dex: hz_s4g(h, d)), "canonical", 1.5, mdl), f"{mdl} h_z x 10^{dex:+.2f}")
    summ(run(g4, "canonical", 1.5, "N"), "Newtonian (S4G h_z)")
P(f"\nchecks: {sum(c for c, _ in CHECKS)}/{len(CHECKS)} pass")
json.dump(dict(verdict=overall, calls=calls, summary=S, checks=CHECKS,
               per_galaxy={k: {str(u): v for u, v in d.items()} for k, d in res.items()}),
          open(os.path.join(HERE, f"cfg578_results{TAG}.json"), "w"), indent=1, default=str)
open(os.path.join(HERE, f"cfg578_edgeon_hz{TAG}.out"), "w").write("\n".join(OUT) + "\n")
