"""LAM2 stage 0 (criteria fa14da563a, amendment A1): F1 size and F2 power on the gas-poor quality sample; gas-bearing as rows.
Run: python3 -I lam2_stage0.py. Single thread, seconds. kappa = 1/2 FITTED; not theory closed."""
import os, glob, json, math, numpy as np
from astropy.io import fits
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE)); EXT = os.path.join(ROOT, "_external_data")
LD = os.path.join(EXT, "lam2_sdss_lines_2026_11_03"); OUT = []; RES = {"lane": "LAM2", "stage": 0}
def P(s=""): print(s, flush=True); OUT.append(s)

dp = fits.open(os.path.join(EXT, "lam1_dynpop_2026_11_03", "SDSSDR17_MaNGA_JAM_v2.fits"))[1].data
m = np.loadtxt(os.path.join(LD, "dynpop_match.csv"), delimiter=",", skiprows=1, dtype=np.int64)
# A1: one row per mangaid, highest Qual then first in file order
o = np.lexsort((m[:, 0], -dp["Qual"][m[:, 0]])); seen = set(); keep = []
for k in o:
    g = dp["mangaid"][m[k, 0]]
    if g not in seen: seen.add(g); keep.append(k)
m = m[np.sort(keep)]; P(f"matched rows 5811 -> {len(m)} galaxies after one row per mangaid")

L = np.concatenate([np.atleast_1d(np.genfromtxt(fn, delimiter=",", skip_header=1, names=True, dtype=None, encoding=None,
                    missing_values="", filling_values=np.nan)) for fn in sorted(glob.glob(os.path.join(LD, "lines_*.csv")))])
SID = np.concatenate([np.loadtxt(fn, delimiter=",", skiprows=2, usecols=0, dtype=str, ndmin=1) for fn in sorted(glob.glob(os.path.join(LD, "lines_*.csv")))])
pos = {int(s): i for i, s in enumerate(SID)}; li = np.array([pos[int(np.int64(s).view(np.uint64))] for s in m[:, 1]])  # ids are uint64
row = m[:, 0]; lam = dp["Lambda_Re"][row].astype(float); eps = dp["Eps_MGE"][row].astype(float)
slow = lam < 0.31 * np.sqrt(np.clip(eps, 0, None))
sn, vd, vde = (L[c][li].astype(float) for c in ("snMedian", "velDisp", "velDispErr"))
ew = -L["h_alpha_eqw"][li].astype(float)  # A1: emission EW, positive = emission
hasline = np.isfinite(ew)
qual = (sn >= 20) & (vd >= 100) & (vde / vd < 0.10)
poor, rich = qual & hasline & (ew < 3), qual & hasline & (ew >= 3)
P(f"no galSpecLine row {int((~hasline).sum())}; quality cut passes {int(qual.sum())} (S/N>=20 {int((sn >= 20).sum())}, velDisp>=100 {int((vd >= 100).sum())})")
P(f"slow overall {int(slow.sum())}; slow in quality {int((slow & qual).sum())}")

def hm(A, n1, n2):
    q1, q2 = A / (2 - A), 2 * A * A / (1 + A)
    return math.sqrt((A * (1 - A) + (n1 - 1) * (q1 - A * A) + (n2 - 1) * (q2 - A * A)) / (n1 * n2))
for name, s in (("gas-poor (GRADED)", poor), ("gas-bearing (row)", rich)):
    n, ns = int(s.sum()), int((s & slow).sum()); nf = n - ns
    f1 = n >= 1000 and ns >= 100; sa = hm(0.75, ns, nf) if ns and nf else float("inf"); f2 = sa <= 0.05 / 3
    P(f"{name}: N {n}, slow {ns} ({ns / max(n, 1):.3f}), fast {nf}; F1 {'PASS' if f1 else 'FAIL'}; "
      f"F2 sigma(AUC) {sa:.4f} vs 0.0167: {'PASS' if f2 else 'FAIL'}")
    RES[name.split()[0]] = dict(n=n, n_slow=ns, n_fast=nf, F1=bool(f1), sigma_auc=sa, F2=bool(f2))
gp = RES["gas-poor"]
P(f"slow fraction: gas-poor {gp['n_slow'] / max(gp['n'], 1):.3f}, gas-bearing {RES['gas-bearing']['n_slow'] / max(RES['gas-bearing']['n'], 1):.3f}; "
  f"slow rotators in quality cut that are gas-poor {gp['n_slow'] / max(int((slow & qual & hasline).sum()), 1):.3f}")
for lo, hi in ((-99, 1), (1, 2), (2, 3)):
    s = poor & (ew >= lo) & (ew < hi); P(f"  gas-poor EW bin [{max(lo, -99)}, {hi}): N {int(s.sum())}, slow {int((s & slow).sum())}")
v = "PASS" if gp["F1"] and gp["F2"] else ("STOP: NOT FEASIBLE" if not gp["F1"] else "STOP: NOT POWERED")
P(f"STAGE 0: {v}. F3 (compute) is a scheduling gate, read by hand."); RES["verdict"] = v
open(os.path.join(HERE, "lam2_stage0.out"), "w").write("\n".join(OUT) + "\n")
json.dump(RES, open(os.path.join(HERE, "lam2_stage0.json"), "w"), indent=1, default=float)
