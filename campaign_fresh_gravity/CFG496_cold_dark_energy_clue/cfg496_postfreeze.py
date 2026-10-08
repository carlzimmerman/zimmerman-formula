#!/usr/bin/env python3
"""CFG496 post-freeze checks (labelled; written after the main and MUTATE runs; NO verdict weight).
P1  C13 censoring: bounds on the X-COP median log y_mix when clusters that never reach the cosmic mix are treated as
    upper limits (true y_mix lower), for the real R.
P2  MUTATE C13 matches: how many are driven by censored clusters (> half of the sample censored in a cell).
P3  the one MUTATE CLUE (C12 at R' = 4.364, form 4/(3 pi kappa OmL Om)): Omega_L Omega_m is symmetric about the
    rho_m = rho_L epoch, so the z = 1 check is weak there; re-check at z = 2 and z = 0.5.
Output: cfg496_postfreeze.out, cfg496_postfreeze.json"""
import os, sys, json, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
os.environ["CFG496_MUTATE"] = "0"
src = open(os.path.join(HERE, "cfg496_hunt.py")).read().split("# ================================================================== main")[0]
ns = {"__file__": os.path.join(HERE, "cfg496_hunt.py"), "__name__": "cfg496_lib"}
exec(compile(src, "cfg496_hunt.py", "exec"), ns)
cosmo, xcop_test, family_test, family_F1, omega_at = ns["cosmo"], ns["xcop_test"], ns["family_test"], ns["family_F1"], ns["omega_at"]
R_TRUE, KAPPA = ns["R_TRUE"], ns["KAPPA"]
OUT = []
def P(s=""):
    print(s); OUT.append(str(s))
res = {}
P("CFG496 post-freeze checks (no verdict weight).")
cs = cosmo(R_TRUE)
x = xcop_test(cs, nboot=400)
P("P1 C13 censoring bounds (real R): censored clusters set to -inf (lowest possible y_mix) vs their last-radius value")
res["P1"] = {}
for k, v in x["cells"].items():
    ly = np.array(list(v["ymix_per_cluster"].values()))
    # identify censored clusters: recompute crossing flag
    names = list(v["ymix_per_cluster"].keys())
    foot, b = k.split("|"); b = float(b[1:])
    cens = []
    for cl in ns["XC"]:
        ratio = cl["mhse"] / (1 - b) / cl["mb"]
        cens.append(not np.any(ratio <= 1 + cs["R"]))
    cens = np.array(cens)
    lo = ly.copy(); lo[cens] = -np.inf
    med_hi = float(np.median(ly)); med_lo = float(np.median(lo))
    d_hi = med_hi - math.log10(cs["ye"]); d_lo = med_lo - math.log10(cs["ye"])
    res["P1"][k] = dict(n_censored=int(cens.sum()), Delta_upper=d_hi, Delta_lower=d_lo if np.isfinite(d_lo) else None)
    P(f"   {k:14s} censored {int(cens.sum()):2d}/12  Delta in [{d_lo:+.3f}, {d_hi:+.3f}] dex"
      + ("  (b=0: robust miss, > 0.15 dex even at the lower bound)" if np.isfinite(d_lo) and d_lo > 0.15 else
         "  (censoring-dominated: undetermined)"))
P("")
mj = json.load(open(os.path.join(HERE, "cfg496_results_MUTATE.json")))
m13 = [d for d in mj["draws"] if d["C13_match"]]
P(f"P2 MUTATE C13 matches: {len(m13)} of {len(mj['draws'])} draws, R' range "
  f"{min(d['R'] for d in m13) if m13 else float('nan'):.2f}-{max(d['R'] for d in m13) if m13 else float('nan'):.2f}")
cnt = 0
for d in m13:
    c = cosmo(d["R"]); xx = xcop_test(c, nboot=200)
    cnt += any(v["censored"] > 6 for v in xx["cells"].values())
P(f"   of these, {cnt} have > 6/12 clusters censored in at least one cell: the 'match' sits on upper limits, not crossings")
res["P2"] = dict(n_match=len(m13), n_censor_driven=cnt)
P("")
Rq = 4.363888129217914; c = cosmo(Rq)
form = lambda o: (4 / 3) / (math.pi * KAPPA * o["OL"] * o["Om"])
P(f"P3 MUTATE CLUE: R' = {Rq:.4f} vs 4/(3 pi kappa OmL Om) = {form(c):.4f} today")
res["P3"] = {}
for z in (0.5, 1.0, 2.0, 3.0):
    oz = omega_at(c, z); dz = abs(math.log(Rq / form(oz)))
    res["P3"][str(z)] = dz
    P(f"   z = {z}: form {form(oz):.3f}, |dln| {dz:.3f} -> {'PASS' if dz <= 0.03 else 'FAIL'}")
P("   OmL*Om is symmetric about rho_m = rho_L; at R' = 4.36 that epoch is z ~ 0.41, so z = 1 nearly mirrors z = 0.")
P("   A two-epoch second check would have caught it. The frozen rate (0.005) is kept as reported; this hole is disclosed.")
json.dump(res, open(os.path.join(HERE, "cfg496_postfreeze.json"), "w"), indent=1)
open(os.path.join(HERE, "cfg496_postfreeze.out"), "w").write("\n".join(OUT) + "\n")
