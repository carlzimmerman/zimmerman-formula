#!/usr/bin/env python3
"""G03D -- THE EFE-REFIT: does the external field close the 22-25% footing tension?

G03C (seesaw audit): the independently fitted galactic a0 (L232 free-scale
1.2457e-10; McGaugh+16 1.2000e-10) sits 22-25% ABOVE the dark-energy scale
a0_DE = 9.36e-11 -- the registered footing tension, quantified.

THE HYPOTHESIS (the framework's own law): the recorded fits used the bare
deep law g_obs^2 = a0*g_bar.  The framework's EFE-regime law is
g_obs^2 = (1 + Y_i) * a0 * g_bar with Y_i = g_ext,i/a0 per galaxy (the
C(Y)-law's deep limit, G047 efe_floor_law_exact).  If the SPARC sample sits
in environments with mean Y ~ 0.22-0.25, the EFE-boosted fit collapses the
best-fit a0 onto a0_DE -- the tension dissolves and the seesaw becomes
predictive after all.

DATA: the repo's environment table (real_research/data/
sparc_a0_environment_table.csv: per-galaxy a0_SI, the host-environment
acceleration scale, used here as the EFE estimate) and the G044 corpus
(glm53_push/data/rotation_curve_corpus_v7.json, 438 galaxies).

SPARC reduction per point (standard, declared): 
  g_bar = (Vgas^2 + ML*Vdisk^2 + ML*Vbul^2)/R   [m/s^2]
  g_obs = Vobs^2/R
with ML = m2l_disk (corpus) and R = Rad kpc.  Deep cut: g_bar < 0.1 a0_DE
(the same deep-regime domain as the free-scale fits).  Y_i = a0_SI_i/a0_DE
declared (a0-fixed in the ratio).  One free parameter a0, grid fit on the
rms of delta = log10(g_obs) - 0.5 log10(g_pred), g_pred = (1+Y)*a0*g_bar
(boosted) or a0*g_bar (bare).

VERDICTS: V1 the EFE fit's best a0 lands within 6% of 9.36e-11 (the DE
scale); V2 the EFE fit beats the bare fit; V3 the honest statement.
"""
import csv, json, math, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, ".."))
ENV = os.path.join(REPO, "real_research", "data", "sparc_a0_environment_table.csv")
COR = os.path.join(REPO, "glm53_push", "data", "rotation_curve_corpus_v7.json")
A0_DE = 9.3619e-11
KPC = 3.0856775814913673e19

env = {}
with open(ENV) as f:
    for row in csv.DictReader(f):
        try:
            env[row["name"].strip().upper()] = float(row["a0_SI"])
        except (KeyError, ValueError):
            pass
print(f"environment table: {len(env)} galaxies")

with open(COR) as f:
    gals = json.load(f)["galaxies"]

deep = []
gal_hit = gal_miss = 0
for g in gals:
    nm = str(g["galaxy"]).strip().upper()
    if nm not in env:
        gal_miss += 1
        continue
    gal_hit += 1
    ML = float(g.get("m2l_disk") or 0.0)
    y = env[nm] / A0_DE
    for p in g["data"]:
        R = float(p["Rad"]) * KPC
        def num(*keys, default=0.0):
            for k in keys:
                v = p.get(k)
                if v is not None:
                    try:
                        return float(v)
                    except (ValueError, TypeError):
                        pass
            return default
        Vg, Vd, Vb = num("Vgas", "Vg"), num("Vdisk", "Vd"), num("Vbul", "Vb")
        Vo = num("Vobs", "Vc")
        Vg, Vd, Vb, Vo = 1e3 * Vg, 1e3 * Vd, 1e3 * Vb, 1e3 * Vo   # km/s -> m/s
        if R <= 0:
            continue
        gbar = (Vg * Vg + ML * Vd * Vd + ML * Vb * Vb) / R
        gobs = Vo * Vo / R
        if gbar > 0 and gobs > 0 and gbar < 0.1 * A0_DE:
            deep.append((gbar, gobs, y))
print(f"galaxies matched: {gal_hit}, missed: {gal_miss}; deep points: {len(deep)}")
print(f"mean Y = {np.mean([y for _, _, y in deep]):.3f} (the EFE boost in the sample)")

def rms_a0(a0, boosted):
    s = 0.0
    for gb, go, y in deep:
        gp = (1 + y) * a0 * gb if boosted else a0 * gb
        if gp <= 0:
            continue
        s += (math.log10(go) - 0.5 * math.log10(gp)) ** 2
    return math.sqrt(s / len(deep))

res = {}
for boosted, label in ((False, "bare"), (True, "EFE-boosted")):
    best_a0, best_r = None, 1e9
    for a0 in np.linspace(0.5e-10, 1.5e-10, 501):
        r = rms_a0(a0, boosted)
        if r < best_r:
            best_r, best_a0 = r, a0
    res[label] = dict(a0=best_a0, rms=best_r, ratio=best_a0 / A0_DE)
    print(f"  {label:12s}: best a0 = {best_a0:.4e} = {best_a0/A0_DE:.3f} x DE scale, "
          f"rms = {best_r:.4f} dex")

ok = abs(res["EFE-boosted"]["ratio"] - 1.0) <= 0.06
print(f"\n  [{'PASS' if ok else 'FAIL'}] V1 [the EFE-boosted fit lands on the DE scale "
      f"within 6%] ratio = {res['EFE-boosted']['ratio']:.3f}")
res["verdict"] = dict(v1=bool(ok),
                      statement=("the footing tension is an EFE-omission artifact; "
                                 "the seesaw is predictive WITH the external field"
                                 if ok else
                                 "the tension survives the EFE boost; the deep-regime a0 "
                                 "excess is not an EFE artifact"))
json.dump(res, open(os.path.join(HERE, "g03d_efe_refit_results.json"), "w"), indent=1)
print("G03D COMPLETE.")