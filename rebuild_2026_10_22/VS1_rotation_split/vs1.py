# VS1: law offset against rotation class at fixed mass. MUTATE=1 shuffles labels within mass terciles. One thread, seconds.
import glob, json, os, re
import numpy as np

MUT = os.environ.get("MUTATE") == "1"
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
rng = np.random.default_rng(20261102)
cfg = json.load(open(f"{REPO}/campaign_fresh_gravity/CFG323_sluggs_measured_tracers/cfg323_measured_tracers_results.json"))
mass = json.load(open(f"{REPO}/campaign_fresh_gravity/CFG330_sluggs_icgc_clip/cfg330_icgc_K0_results.json"))["per_galaxy"]
exact, oldmap = {}, {}
for ln in open(f"{REPO}/_external_data/atlas3d_emsellem11/tableb1.tsv"):
    p = ln.rstrip("\n").split("\t")
    if len(p) > 11 and p[1].strip().startswith("NGC"):
        exact[p[1].strip()] = (p[10].strip(), float(p[8])); oldmap[re.sub(r"\D", "", p[1])] = p[10].strip()
out = {"mode": "MUTATE" if MUT else "normal"}

def stats(off, M, S):
    D = off[S].mean() - off[~S].mean()
    perm = np.array([(lambda s: off[s].mean() - off[~s].mean())(rng.permutation(S)) for _ in range(100000)])
    X = np.c_[np.ones_like(M), M - M.mean(), S.astype(float)]
    b = np.linalg.lstsq(X, off, rcond=None)[0]; r = off - X @ b
    se = np.sqrt(np.diag(r @ r / (len(off) - 3) * np.linalg.inv(X.T @ X)))
    mm = [off[i] - off[np.abs(M - M[i]) < 0.25][~S[np.abs(M - M[i]) < 0.25]].mean() for i in np.where(S)[0]
          if (~S[np.abs(M - M[i]) < 0.25]).any()]
    return dict(D=D, p=float((perm >= D).mean()), coef=b[2], se=se[2], Z=b[2] / se[2], slope=b[1], slope_se=se[1], mass_matched=float(np.mean(mm)) if mm else None,
                n_matched=len(mm), mean_slow=off[S].mean(), mean_fast=off[~S].mean(), logM_slow=M[S].mean(), logM_fast=M[~S].mean(), n_slow=int(S.sum()), n_fast=int((~S).sum()))

def spear(a, b):
    ra = np.argsort(np.argsort(a)).astype(float); rb = np.argsort(np.argsort(b)).astype(float)
    return float(np.corrcoef(ra, rb)[0, 1])

verdict = {}
for foot, key in (("canonical", "nu_mono|canonical"), ("alt", "nu_mono|alt")):
    g = cfg["per_galaxy"][foot]; names = sorted(g, key=int)
    off = np.array([g[n]["primary"] for n in names]); M = np.array([mass[key][n]["lMjamlaw"] for n in names])
    S = np.array([exact[f"NGC{n}"][0] == "S" for n in names]); lam = np.array([exact[f"NGC{n}"][1] for n in names])
    if MUT:
        o = np.argsort(M)
        for c in np.array_split(o, 3): S[c] = rng.permutation(S[c])
    row = stats(off, M, S)
    row["per_galaxy"] = {n: [round(float(a), 3), round(float(b), 2), bool(s), float(l)] for n, a, b, s, l in zip(names, off, M, S, lam)}
    row["spearman_lam"] = spear(off, -lam)
    res = off - np.polyval(np.polyfit(M, off, 1), M); row["spearman_lam_mass_removed"] = spear(res, -lam)
    row["spearman_M"] = spear(off, M)
    C = np.array([int(n) in cfg["centrals"] for n in names]); row["centrals"] = [n for n, c in zip(names, C) if c]
    row["no_centrals"] = stats(off[~C], M[~C], S[~C]) if S[~C].sum() >= 2 else {"n_slow": int(S[~C].sum())}
    O = np.array([oldmap[n] == "S" for n in names]); row["old_label_map"] = stats(off, M, O)
    ok = row["D"] >= 0.15 and row["p"] < 0.05 and row["coef"] >= 0.10 and row["Z"] > 2
    kill = row["D"] <= 0.05 or abs(row["Z"]) < 1
    row["cell"] = "PASS" if ok else "KILL" if kill else "NOT SEPARATED"
    verdict[foot] = row["cell"]; out[foot] = row
out["label"] = "ROTATION SPLIT PASSES" if all(v == "PASS" for v in verdict.values()) else "KILLED" if "KILL" in verdict.values() else "NOT SEPARATED"

# SPARC disc arm
T = {}
for ln in open(f"{REPO}/real_research/data/SPARC_Lelli2016c.mrt"):
    p = ln.split()
    if len(p) >= 18 and p[1].isdigit() and not ln.startswith(("Title", "Note", "Byte")):
        try: T[p[0]] = dict(inc=float(p[5]), L=float(p[7]), MHI=float(p[13]), Q=int(p[17]))
        except ValueError: pass
for foot, a0 in (("canonical", 9.3603e-11), ("alt", 1.1312e-10)):
    rows = []
    for f in glob.glob(f"{REPO}/real_research/data/sparc_data/*_rotmod.dat"):
        n = os.path.basename(f).replace("_rotmod.dat", ""); t = T.get(n)
        if t is None or t["Q"] >= 3 or t["inc"] < 30: continue
        lM = np.log10(0.5e9 * t["L"] + 1.33e9 * t["MHI"])
        if lM < 10.7: continue
        d = np.loadtxt(f, comments="#"); d = d[d[:, 0] > 0]; d = d[len(d) // 2:]
        k = 1e6 / 3.0857e19  # (km/s)^2/kpc to m/s^2
        go = d[:, 1]**2 / d[:, 0] * k
        gn = (np.sign(d[:, 3]) * d[:, 3]**2 + 0.5 * d[:, 4]**2 + 0.7 * d[:, 5]**2) / d[:, 0] * k
        gn = np.clip(gn, 1e-14, None); gl = gn / 2 + np.sqrt(gn**2 / 4 + gn * a0)
        rows.append((n, lM, float(np.mean(np.log10(go / gl)))))
    v = np.array([r[2] for r in rows]); lm = np.array([r[1] for r in rows])
    out[foot]["discs"] = dict(n=len(v), mean=float(v.mean()), sd=float(v.std(ddof=1)), sem=float(v.std(ddof=1) / np.sqrt(len(v))), logMb_mean=float(lm.mean()),
                              minus_slow=float(v.mean() - out[foot]["mean_slow"]), minus_fast=float(v.mean() - out[foot]["mean_fast"]))
json.dump(out, open(f"{HERE}/vs1{'_MUTATE' if MUT else ''}.json", "w"), indent=1, default=float)
for foot in ("canonical", "alt"):
    r = out[foot]; print(foot, r["cell"], {k: (round(v, 3) if isinstance(v, float) else v) for k, v in r.items() if k not in ("per_galaxy", "no_centrals", "old_label_map", "discs", "cell")})
    for s in ("no_centrals", "old_label_map", "discs"):
        print(" ", s, {k: (round(v, 3) if isinstance(v, float) else v) for k, v in r[s].items()})
    if foot == "canonical": print(" per_galaxy off,logM,slow,lam", r["per_galaxy"])
print("LABEL", out["label"])
