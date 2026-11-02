# VS3: PN and GC contrasts of slow non-centrals against fast non-centrals, from CFG492's committed offsets. MUTATE=1 reads its shuffled pairing.
import json, os, re
import numpy as np

MUT = os.environ.get("MUTATE") == "1"
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
CF = f"{REPO}/campaign_fresh_gravity/CFG492_multisource_synthesis/cfg492_gc_vs_pn{'_MUTATE' if MUT else ''}_results.json"
PG = json.load(open(CF))["per_galaxy"]

def tsv(f):
    r = [l.rstrip("\n").split("\t") for l in open(f) if not l.startswith("#") and l.strip()]
    return [x.strip() for x in r[0]], r[3:]

_, m = tsv(f"{REPO}/real_research/data/2mrs_huchra2012.tsv")
T = []
for x in m:
    try: T.append([float(x[0]), float(x[1]), float(x[2]), float(x[3])])
    except (ValueError, IndexError): pass
T = np.array(T)
A = {}
for ln in open(f"{REPO}/_external_data/atlas3d_emsellem11/tableb1.tsv"):
    p = ln.rstrip("\n").split("\t")
    if len(p) > 11 and p[1].strip().startswith("NGC"): A[p[1].strip()] = p[10].strip()
h, s = tsv(f"{REPO}/real_research/data/sluggs_forbes2017_galaxies.tsv")
ix = {k: h.index(k) for k in h}

def sex(t, ra):
    a = [float(v) for v in t.replace(":", " ").split()]
    if len(a) == 1: return a[0]
    d = abs(a[0]) + a[1] / 60 + a[2] / 3600
    return d * 15 if ra else (-d if t.strip().startswith("-") else d)

def central(n, Rk, dv):
    r = next(x for x in s if x[ix["NGC"]].strip() == n)
    ra, de = sex(r[ix["RAJ2000"]], 1), sex(r[ix["DEJ2000"]], 0); D = float(r[ix["Dist"]]); v = float(r[ix["Vsys"]])
    dr = np.hypot((T[:, 0] - ra) * np.cos(np.radians(de)), T[:, 1] - de); i = np.argmin(dr)
    sel = (dr < np.degrees(Rk / 1e3 / D)) & (np.abs(T[:, 2] - v) < dv) & (dr > 0.02)
    return not (T[sel, 3] < T[i, 3]).any()

def num(x):
    return x is not None and np.isfinite(x)

def table(foot, tr, Rk, dv):
    g = PG[foot]; rows = {}
    for n, r in g.items():
        O, e = r.get(f"O_{tr}"), r.get(f"e_{tr}")
        if num(O) and num(e):
            rows[n] = dict(O=O, e=e, lM=r["lM"], slow=A[f"NGC{int(n):04d}"] == "S", central=central(n, Rk, dv))
    ref = [v for v in rows.values() if not v["slow"] and not v["central"]]
    if not ref: return rows, None, None
    x = np.array([v["O"] for v in ref]); er = np.array([v["e"] for v in ref])
    e1 = x.std(ddof=1) / np.sqrt(len(x)) if len(x) > 1 else np.inf
    return rows, float(x.mean()), float(max(e1, 1 / np.sqrt((1 / er ** 2).sum())))

out = {"mode": "MUTATE" if MUT else "normal"}; cells = {}
for foot in ("canonical", "alt"):
    res = {}
    for tr in ("PN", "GC"):
        for Rk, dv in ((500, 500), (300, 500), (1000, 1000)):
            rows, ref, eref = table(foot, tr, Rk, dv)
            con = {n: dict(v, contrast=v["O"] - ref, err=float(np.hypot(v["e"], eref))) for n, v in rows.items()} if ref is not None else {}
            res[f"{tr}|{Rk}/{dv}"] = dict(ref=ref, eref=eref, n_ref=sum(not v["slow"] and not v["central"] for v in rows.values()), rows=con)
    p = res["PN|500/500"]; r = p["rows"]; pair = [r.get("3608"), r.get("4374")]
    sn = {n for n, v in r.items() if v["slow"] and not v["central"]}
    lab = "UNDECIDED"
    if p["ref"] is not None and sn >= {"3608", "4374"}:
        c = [q["contrast"] for q in pair]; mean = float(np.mean(c))
        cov = np.array([[pair[0]["e"] ** 2 + p["eref"] ** 2, p["eref"] ** 2], [p["eref"] ** 2, pair[1]["e"] ** 2 + p["eref"] ** 2]])
        em = float(np.sqrt(cov.sum()) / 2); p["pair_mean"] = mean; p["pair_err"] = em
        sc = [v["contrast"] for v in r.values() if v["slow"] and v["central"]]
        if sc:
            p["slow_central_mean"] = float(np.mean(sc)); p["slow_central_err"] = float(np.sqrt(sum(v["err"] ** 2 for v in r.values() if v["slow"] and v["central"])) / len(sc))
        if min(c) >= 0.10 and mean / em > 2: lab = "LEANS ROTATION"
        elif all(abs(q["contrast"]) < q["err"] for q in pair) and sc and p["slow_central_mean"] >= 0.10 and p["slow_central_mean"] / p["slow_central_err"] > 2: lab = "LEANS ENVIRONMENT"
    cells[foot] = lab; out[foot] = res
    M = np.array([v["lM"] for v in r.values()]); O = np.array([v["O"] for v in r.values()])
    out[foot]["slope_O_on_lM"] = float(np.polyfit(M, O, 1)[0])
out["labels"] = cells
out["label"] = cells["canonical"] if cells["canonical"] == cells["alt"] else "FOOTING-DEPENDENT"
if MUT and out["label"] == "LEANS ROTATION": out["label"] = "CONTROL FAILED"
json.dump(out, open(f"{HERE}/vs3{'_MUTATE' if MUT else ''}.json", "w"), indent=1, default=float)
print(out["mode"], cells, "->", out["label"])
for foot in ("canonical", "alt"):
    print(f"\n{foot}: slope of PN offset on log M {out[foot]['slope_O_on_lM']:+.3f}")
    for key, p in out[foot].items():
        if key == "slope_O_on_lM": continue
        print(f" {key}: ref {p['ref'] if p['ref'] is None else round(p['ref'],3)} +- {p['eref'] if p['eref'] is None else round(p['eref'],3)} (n {p['n_ref']})" + (f"; pair {p['pair_mean']:+.3f} +- {p['pair_err']:.3f}" if "pair_mean" in p else "") + (f"; slow central {p['slow_central_mean']:+.3f} +- {p['slow_central_err']:.3f}" if "slow_central_mean" in p else ""))
        for n, v in p["rows"].items():
            print(f"   NGC{n:5s} {'slow' if v['slow'] else 'fast'} {'cen' if v['central'] else 'non'} O {v['O']:+.3f} +- {v['e']:.3f} contrast {v['contrast']:+.3f} +- {v['err']:.3f}")
