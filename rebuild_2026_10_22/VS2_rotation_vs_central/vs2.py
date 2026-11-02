# VS2: law offset on mass, slow and central together. MUTATE=1 shuffles central labels within mass terciles. One thread, seconds.
import json, os
import numpy as np

MUT = os.environ.get("MUTATE") == "1"
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
rng = np.random.default_rng(20261102)

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

def fit(off, M, S, C):
    X = np.c_[np.ones_like(M), M - M.mean(), S.astype(float), C.astype(float)]
    b = np.linalg.lstsq(X, off, rcond=None)[0]; r = off - X @ b
    se = np.sqrt(np.diag(r @ r / (len(off) - 4) * np.linalg.inv(X.T @ X)))
    return dict(mass=b[1], mass_se=se[1], slow=b[2], slow_se=se[2], central=b[3], central_se=se[3], n=len(off), corr_slow_central=float(np.corrcoef(S, C)[0, 1]))

cfg = json.load(open(f"{REPO}/campaign_fresh_gravity/CFG323_sluggs_measured_tracers/cfg323_measured_tracers_results.json"))
mass = json.load(open(f"{REPO}/campaign_fresh_gravity/CFG330_sluggs_icgc_clip/cfg330_icgc_K0_results.json"))["per_galaxy"]
out = {"mode": "MUTATE" if MUT else "normal"}; cells = {}
for foot, key in (("canonical", "nu_mono|canonical"), ("alt", "nu_mono|alt")):
    g = cfg["per_galaxy"][foot]; names = sorted(g, key=int)
    off = np.array([g[n]["primary"] for n in names]); M = np.array([mass[key][n]["lMjamlaw"] for n in names])
    S = np.array([A[f"NGC{n}"] == "S" for n in names])
    row = {}
    for R, dv in ((500, 500), (300, 500), (1000, 1000)):
        C = np.array([central(n, R, dv) for n in names])
        if MUT:
            for c in np.array_split(np.argsort(M), 3): C[c] = rng.permutation(C[c])
        f = fit(off, M, S, C)
        f["quadrants"] = {lab: dict(n=int(q.sum()), mean=float(off[q].mean()) if q.any() else None, names=[n for n, k in zip(names, q) if k])
                          for lab, q in (("slow_central", S & C), ("slow_non", S & ~C), ("fast_central", ~S & C), ("fast_non", ~S & ~C))}
        row[f"{R}/{dv}"] = f
    p = row["500/500"]
    rot = p["slow"] >= 0.10 and p["slow"] / p["slow_se"] > 2 and abs(p["central"]) < p["central_se"]
    env = p["central"] >= 0.10 and p["central"] / p["central_se"] > 2 and abs(p["slow"]) < p["slow_se"]
    cells[foot] = "ROTATION" if rot else "ENVIRONMENT" if env else "UNDECIDED"
    row["off_sl_3608"] = None
    out[foot] = row
out["label"] = cells["canonical"] if cells["canonical"] == cells["alt"] else "UNDECIDED"
json.dump(out, open(f"{HERE}/vs2{'_MUTATE' if MUT else ''}.json", "w"), indent=1, default=float)
for foot in ("canonical", "alt"):
    print(foot, cells[foot])
    for k, v in out[foot].items():
        if v: print(" ", k, {a: (round(b, 3) if isinstance(b, float) else b) for a, b in v.items() if a != "quadrants"})
        if v:
            for q, d in v["quadrants"].items(): print("     ", q, d["n"], None if d["mean"] is None else round(d["mean"], 3), d["names"])
print("LABEL", out["label"])
