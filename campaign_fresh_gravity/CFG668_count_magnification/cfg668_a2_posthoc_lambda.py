"""CFG668 A2 POST-HOC (not frozen): Quaia steepest bin (G 17-19), 0-4', split by richness. Lensing must grow with lambda."""
import numpy as np, os, json, importlib.util
from scipy.spatial import cKDTree
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("a2", os.path.join(HERE, "cfg668_a2_quasars.py"))
src = open(os.path.join(HERE, "cfg668_a2_quasars.py")).read().split("res = {")[0]   # reuse setup (clusters, blanks, helpers) only
g = {"__file__": os.path.join(HERE, "cfg668_a2_quasars.py")}; exec(src, g)
q = g["readtsv"](os.path.join(HERE, "quaia_g20_ra_dec_z_g.tsv.gz"), gz=True); q = q[np.isfinite(q).all(1)]
tq = cKDTree(g["xyz"](q[:, 0], q[:, 1])); cl = g["cl"]; Xc = g["xyz"](cl[:, 0], cl[:, 1]); B = g["B"]; Xb = g["Xb"]
nb = np.array([len(x) for x in tq.query_ball_point(Xb, g["chord"](30))]); med = np.median(nb)
nc = np.array([len(x) for x in tq.query_ball_point(Xc, g["chord"](30))])
mags = [(17, 19.0)]
Cn = g["counts"](Xc, cl[:, 2], q, tq, mags).sum(1)[:, 0]; Bn = g["counts"](Xb[nb >= 0.5*med], B[nb >= 0.5*med, 2], q, tq, mags).sum(1)[:, 0]
okc = nc >= 0.5*med; r = np.random.default_rng(1); out = {}
for lo, hi in [(20, 30), (30, 50), (50, 1e9)]:
    m = okc & (cl[:, 3] >= lo) & (cl[:, 3] < hi); c = Cn[m]
    R = c.mean()/Bn.mean(); s = np.std([c[r.integers(0, len(c), len(c))].mean()/Bn[r.integers(0, len(Bn), len(Bn))].mean() for _ in range(2000)])
    out[f"{lo}-{hi}"] = [float(R), float(s), int(m.sum())]; print(f"lambda {lo}-{hi:g}: n={m.sum():5d}  R={R:.3f}±{s:.3f} ({(R-1)/s:+.1f}σ)")
json.dump(out, open(os.path.join(HERE, "cfg668_a2_posthoc_lambda.json"), "w"), indent=1)
