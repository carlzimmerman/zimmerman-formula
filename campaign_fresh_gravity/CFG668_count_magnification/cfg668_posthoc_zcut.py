"""CFG668 POST-HOC (not frozen): does the inner-annulus excess shrink as the photo-z gap above the cluster grows?
Member leakage shrinks with the gap; lensing does not. Faint bin r 20.5-21.5, 0-2' and 4-6'."""
import json, os, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
raw = [o for o in json.load(open(os.path.join(HERE, "cfg668_counts_raw.json"))) if o["gals"]]
allc = np.loadtxt(os.path.join(HERE, "redmapper_all_positions.tsv"))
def clean(o):
    d = np.degrees(np.arccos(np.clip(np.sin(np.radians(o["dec"]))*np.sin(np.radians(allc[:,1])) + np.cos(np.radians(o["dec"]))*np.cos(np.radians(allc[:,1]))*np.cos(np.radians(o["ra"]-allc[:,0])), -1, 1)))
    return not (d < 0.25).any() and len(o["gals"]) > 50
cl = [o for o in raw if o["kind"] == "cl"]; rn = [o for o in raw if o["kind"] == "rnd" and clean(o)]
def n(o, gap, a, b):
    g = np.array(o["gals"]); return ((g[:,2] > o["z"]+gap) & (g[:,0]>=a) & (g[:,0]<b) & (g[:,1]>=20.5) & (g[:,1]<21.5)).sum()
rng = np.random.default_rng(2); out = {}
for gap in [0.1, 0.2, 0.3, 0.4, 0.5]:
    for a, b in [(0, 2), (4, 6)]:
        C = np.array([n(o, gap, a, b) for o in cl], float); R = np.array([n(o, gap, a, b) for o in rn], float)
        r = C.mean()/R.mean(); s = np.std([C[rng.integers(0,len(C),len(C))].mean()/R[rng.integers(0,len(R),len(R))].mean() for _ in range(1000)])
        out[f"gap{gap}_{a}-{b}"] = [r, s, C.mean(), R.mean()]
        print(f"photo-z gap > {gap}: annulus {a}-{b}'  N_cl={C.mean():5.2f} N_blank={R.mean():5.2f}  R={r:.3f}±{s:.3f}")
json.dump(out, open(os.path.join(HERE, "cfg668_posthoc_zcut.json"), "w"), indent=1)
