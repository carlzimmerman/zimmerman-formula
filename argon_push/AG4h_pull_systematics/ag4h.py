#!/usr/bin/env python3
"""AG4h: can distance or inclination errors explain AG4g's 13 large pulls?  Per galaxy: A_ML (Upsilon and a coherent log-g offset c
both free, no priors) vs B (Upsilon at the stellar-population value, c free); dchi2 <= 4 -> COHERENT-ABSORBABLE (then the distance or
inclination change needed, in quoted sigmas), else SHAPE-DRIVEN.  CF4 TRGB cross-check for the pulled TRGB galaxies.
Criteria: FROZEN_CRITERIA.md (committed alone, before this script).  AG4g's frozen definitions are executed read-only.
Run: OMP_NUM_THREADS=1 nice -n 10 python3 ag4h.py      AG4H_MUTATE=1: inner-half Upsilon x3 mocks must read SHAPE-DRIVEN (exit 1).
kappa = 1/2 fitted; not theory closed."""
import csv, json, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
G4G = os.path.join(REPO, "argon_push", "AG4g_galaxy_pull_census"); EXT = os.path.join(os.path.dirname(REPO), "_external_data")
MUT = os.environ.get("AG4H_MUTATE") == "1"; TAG = "_MUTATE" if MUT else ""
OUT = open(os.path.join(HERE, f"ag4h{TAG}.out"), "w")
def P(*a):
    s = " ".join(str(x) for x in a); print(s); OUT.write(s + "\n"); OUT.flush()
src = open(os.path.join(G4G, "ag4g.py")).read()
ns = {"__file__": os.path.join(G4G, "ag4g.py"), "__name__": "ag4g_frozen", "P": P, "MUT": False, "FAILS": [], "check": None}
exec(compile(src[:src.index("MUT = os.environ.get")], "ag4g_head", "exec"), ns); ns["P"] = P; ns["MUT"] = False
exec(compile(src[src.index("LN10 = math.log(10.0)"):src.index("PR = props(D_)")], "ag4g_body", "exec"), ns)
D_, fit, NU1, A0C, LU0, S0, LN10 = ns["D_"], ns["fit"], ns["NU1"], ns["A0C"], ns["LU0"], ns["S0"], ns["LN10"]
P("AG4h: distance/inclination error-budget inversion for AG4g's large pulls (n=1, canonical a0)" + ("   *** MUTATE ***" if MUT else ""))
P("kappa = 1/2 fitted; not theory closed.")

res4g = json.load(open(os.path.join(G4G, "ag4g_results.json")))
pulls = np.array(res4g["stage1"]["n=1 canonical (PRIMARY)"]["pulls"]); names = res4g["names"]
assert names == [d["name"] for d in D_]
IDX = [k for k in range(len(D_)) if abs(pulls[k]) >= 3 - 1e-9]
P(f"{len(IDX)} large-pull galaxies: {', '.join(D_[k]['name'] for k in IDX)}")
pk = fit(D_, NU1, A0C)
k1 = all(abs(pk[k] - pulls[k]) < 1e-12 for k in IDX)
P(f"  [{'PASS' if k1 else 'FAIL'}] K1 AG4g MAP pulls reproduced for the {len(IDX)} galaxies")

LUW = LU0 + np.linspace(-1.5, 1.5, 1201)                              # wide grid for the prior-free A_ML


def chi_data(d, lu, go=None):
    """data-part chi2 with the coherent offset c profiled (no prior) at each log Upsilon in lu; returns chi2 array and c array."""
    go = d["go"] if go is None else go
    gb = d["gas"][:, None] + d["star"][:, None] * (10 ** np.atleast_1d(lu))[None, :]
    bad = np.any(gb <= 0, axis=0); gb = np.where(gb > 0, gb, 1.0)
    r = np.log10(go)[:, None] - np.log10(NU1(gb / A0C) * gb)
    w = (1.0 / (d["sv"] ** 2 + S0 ** 2))[:, None]
    c = (w * r).sum(0) / w.sum(0); chi = (w * (r - c) ** 2).sum(0)
    return np.where(bad, np.inf, chi), c


def classify(d, go=None):
    chA, _ = chi_data(d, LUW, go); iA = int(np.argmin(chA))
    chB, cB = chi_data(d, np.array([LU0]), go)
    dchi = float(chB[0] - chA[iA]); c = float(cB[0]); m = d["meta"] or {}
    out = dict(dchi2=dchi, c_req=c, U_ML=float(10 ** LUW[iA]), f_dist=float(10 ** (-c)))   # f as frozen: 10^(-c) = D_SPARC/D_true
    eDD = m.get("eD", 0) / m.get("D", 1) if m else 0.0
    out["n_D"] = abs(c) / (eDD / LN10) if eDD > 0 else float("inf")
    inc = math.radians(m.get("Inc", 90.0)); s = math.sin(inc) * 10 ** (c / 2)
    if s <= 1.0:
        inew = math.degrees(math.asin(s)); out["i_new"] = inew; out["n_i"] = abs(inew - m.get("Inc", 90.0)) / max(m.get("eInc", 1e-9), 1e-9)
    else:
        out["i_new"] = None; out["n_i"] = float("inf")
    if dchi > 4:
        out["cls"] = "SHAPE-DRIVEN"
    elif out["n_D"] <= 2 or out["n_i"] <= 2:
        out["cls"] = "COHERENT-ABSORBABLE: " + " + ".join(x for x, ok in (("DISTANCE-PLAUSIBLE", out["n_D"] <= 2), ("INCLINATION-PLAUSIBLE", out["n_i"] <= 2)) if ok)
    else:
        out["cls"] = "COHERENT-ABSORBABLE: NEEDS > 2 sigma ERRORS"
    return out


def law_mock(d, seed, inner_x=1.0, scale=1.0):
    rng = np.random.default_rng(seed); n = len(d["go"])
    mult = np.where(np.arange(n) < n // 2, inner_x, 1.0)
    gb = d["gas"] + d["star"] * 10 ** LU0 * mult
    return NU1(gb / A0C) * gb * 10 ** (np.sqrt(d["sv"] ** 2 + S0 ** 2) * rng.standard_normal(n)) / scale


if MUT:
    cl = [classify(D_[k], law_mock(D_[k], 500 + k, inner_x=3.0)) for k in IDX]
    nS = sum(c["cls"] == "SHAPE-DRIVEN" for c in cl)
    for k, c in zip(IDX, cl):
        P(f"  {D_[k]['name']:10s} dchi2 {c['dchi2']:7.1f}  {c['cls']}")
    bites = nS >= 7
    P(f"MUTATE (inner-half Upsilon x3 law-true mocks): SHAPE-DRIVEN {nS}/{len(IDX)} -> {'control BITES (exit 1, as designed)' if bites else 'control DID NOT BITE (recorded)'}")
    json.dump(dict(lane="AG4h", mutate=True, n_shape=nS, rows=cl), open(os.path.join(HERE, f"ag4h_results{TAG}.json"), "w"), indent=1, default=float)
    OUT.close(); sys.exit(1 if bites else 0)

# ---- K2: an injected 30% distance overestimate must be recovered as COHERENT-ABSORBABLE with f within 5% of 1.3
k2n = 0
for k in IDX:
    c = classify(D_[k], law_mock(D_[k], 300 + k, scale=1.3))
    k2n += (c["dchi2"] <= 4 and abs(c["f_dist"] / 1.3 - 1) <= 0.05)
P(f"  [{'PASS' if k2n >= 11 else 'FAIL'}] K2 injected 30% distance overestimate recovered in {k2n}/{len(IDX)} (need >= 11)")

# ---- the 13
P(f"\n{'galaxy':10s} {'pull':>5s} {'Q':>2s} {'fD':>2s} {'dchi2':>7s} {'c_req':>7s} {'D_SPARC/D_true':>14s} {'n_D':>6s} {'Inc':>5s} {'i_new':>6s} {'n_i':>6s}  class")
rows = []
for k in IDX:
    d = D_[k]; m = d["meta"] or {}; c = classify(d)
    c.update(name=d["name"], pull=float(pulls[k]), Q=m.get("Q"), fD=m.get("fD"), Inc=m.get("Inc"), eInc=m.get("eInc"), D=m.get("D"), eD=m.get("eD"))
    rows.append(c)
    inew = f"{c['i_new']:.1f}" if c["i_new"] is not None else "  >90"
    P(f"{d['name']:10s} {pulls[k]:+5.2f} {m.get('Q')!s:>2s} {m.get('fD')!s:>2s} {c['dchi2']:7.1f} {c['c_req']:+7.3f} {c['f_dist']:14.3f} {c['n_D']:6.1f} {m.get('Inc', 0):5.1f} {inew:>6s} {c['n_i']:6.1f}  {c['cls']}")
nP = sum(1 for r in rows if "PLAUSIBLE" in r["cls"]); nS = sum(1 for r in rows if r["cls"] == "SHAPE-DRIVEN"); nN = len(rows) - nP - nS
summ = "DISTANCE/INCLINATION EXPLAIN THE EXCESS" if nP >= 10 else "SHAPE DOMINATES" if nS >= 7 else "MIXED"
P(f"\ncounts: plausible distance/inclination {nP}, shape-driven {nS}, coherent but needs > 2 sigma {nN}  ->  {summ}")
P("  (reported, not graded) shape-driven galaxies: " + "; ".join(f"{r['name']} pull {r['pull']:+.1f} Q {r['Q']}" for r in rows if r["cls"] == "SHAPE-DRIVEN"))

# ---- TD: CF4 TRGB cross-check (p50's match: rotation-free method order, 60 arcsec)
fw = lambda l, a, b: (float(l[a - 1:b]) if l[a - 1:b].strip() else float("nan"))
CF = []
for l in open(os.path.join(EXT, "cosmicflows4", "table2.dat")):
    meth = [("TRGB", fw(l, 103, 107)), ("Cepheid", fw(l, 114, 119)), ("SBF", fw(l, 78, 83)), ("SNIa", fw(l, 42, 47)), ("SNII", fw(l, 91, 96))]
    pick = next(((mm, dm) for mm, dm in meth if math.isfinite(dm)), None)
    if pick:
        CF.append((fw(l, 138, 145), fw(l, 147, 154), pick[0], 10 ** (pick[1] / 5 + 1) / 1e6))
A = np.array([(r[0], r[1]) for r in CF])
POS = {r["sparc_name"]: (float(r["ra_deg"]), float(r["dec_deg"])) for r in csv.DictReader(open(os.path.join(EXT, "cosmicflows4", "sesame_sparc.csv"))) if r["ra_deg"]}
td = []
for r in rows:
    if r["fD"] != 2 or r["name"] not in POS:
        continue
    ra, de = POS[r["name"]]; dd = 3600 * np.hypot((A[:, 0] - ra) * math.cos(math.radians(de)), A[:, 1] - de); i = int(np.argmin(dd))
    if dd[i] < 60:
        ratio = CF[i][3] / r["D"]; td.append(dict(name=r["name"], method=CF[i][2], D_CF4=CF[i][3], D_SPARC=r["D"], ratio=ratio, ok=abs(ratio - 1) <= 0.10))
for t in td:
    P(f"  TD {t['name']:10s} CF4 {t['method']} {t['D_CF4']:.2f} Mpc vs SPARC {t['D_SPARC']:.2f}: ratio {t['ratio']:.3f} {'(within 10%)' if t['ok'] else '(DISPUTED)'}")
P(f"\nAG4h: {summ}; TD {sum(t['ok'] for t in td)}/{len(td)} TRGB distances confirmed by CF4")
json.dump(dict(lane="AG4h", mutate=False, K1=k1, K2=k2n, rows=rows, counts=dict(plausible=nP, shape=nS, needs_gt2sigma=nN), summary=summ, TD=td),
          open(os.path.join(HERE, "ag4h_results.json"), "w"), indent=1, default=float)
OUT.close()
sys.exit(0 if (k1 and k2n >= 11) else 1)
