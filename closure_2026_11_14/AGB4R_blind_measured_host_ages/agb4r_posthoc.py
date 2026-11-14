"""AGB4R POST HOC (written after the words were read; changes no word).
(a) KR diagnosis: the file's own hr column against mu minus a flat Hubble line.
(b) Low-stretch share by age bin with the Sako table's x1 beside Pantheon+'s.
(c) Effect of rescaling the formula error by chi2/dof on the primary and fork fits.
Usage: python3 -I agb4r_posthoc.py > agb4r_posthoc.out"""
import os
import sys
import json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import agb4r_data as D  # noqa: E402
import numpy as np  # noqa: E402
from scipy.optimize import minimize_scalar  # noqa: E402

t = D.load_tsv("campbell_local.tsv"); RS = D.load_rose_summary()
snid = t["SNID"].astype(int); z = t["redshift"]; mu = t["mu"]; hr = t["hr"]
loc = np.array([RS[s]["local"] for s in snid])
d = hr - (mu - D.mu_flat(z, z, 0.3))
print(f"(a) hr - (mu - line Om 0.3): mean {d.mean():+.4f}, per-object scatter {d.std():.4f} mag")
r = minimize_scalar(lambda om: np.std(hr - (mu - D.mu_flat(z, z, om))), bounds=(0.01, 1.0), method="bounded")
print(f"(a) Om that makes hr closest to a constant shift of mu - line: {r.x:.3f} (scatter left {r.fun:.4f} mag)")
for cut in (6, 7, 8, 9):
    res = mu - D.mu_flat(z, z, 0.3); yy = loc < cut
    print(f"(a) split at {cut} Gyr: n young {yy.sum()}, unweighted step from mu {res[yy].mean() - res[~yy].mean():+.4f},"
          f" from own hr {hr[yy].mean() - hr[~yy].mean():+.4f}")

X = D.build_samples(); pp = X["pp"]
for lab, x1 in (("Pantheon+ x1", pp["x1"]), ("Sako table x1", pp["x1_tab"])):
    out = []
    for lo, hi in ((0, 2), (2, 4), (4, 6), (6, 8), (8, 14), (0, 4)):
        m = (pp["age"] >= lo) & (pp["age"] < hi)
        out.append(f"{lo}-{hi}: {np.mean(x1[m] < -1):.3f} (n {m.sum()}, low {np.sum(x1[m] < -1)})")
    print(f"(b) {lab}: " + "; ".join(out))

F = json.load(open(os.path.join(HERE, "agb4r_fits.json")))
for model in ("M0", "M1"):
    for k, f in F[model].items():
        s = f["chi2"] / f["dof"]
        print(f"(c) {model} {k:36s} chi2/dof {s:.3f}: dchi2(A=0) {f['dchi2_A0'] / s:.2f}, dchi2(A=1) {f['dchi2_A1'] / s:.2f}"
              " after rescaling")
