#!/usr/bin/env python3
"""CFG949 POST-HOC diagnostic PH1 (amendment A1, 2026-10-20; written after the main run; NO class weight).

How much of the S-cen baryon budget (and therefore of H-UT's cold supply) is the CFG687 pipeline's beta-model gas EXTRAPOLATED beyond
R500 (eROSITA measures Mgas500 only)? Same gas construction as CFG687 law() (RGRID 1e-3..30 Mpc x 3000, cut at 3 Mpc, normalised to
Mgas500 at R500), for beta 2/3 (primary) and the 0.6 / 0.8 brackets.
Run: OMP_NUM_THREADS=1 nice -n 10 python3 cfg949_posthoc.py  -> cfg949_posthoc.out, cfg949_posthoc.json  (seconds, < 100 MB)
kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import os, json
os.environ["OMP_NUM_THREADS"] = "1"
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE)
PC7 = np.load(os.path.join(LANES, "CFG687_erass1_shear_stack", "cfg687_percluster.npz"))
MG, R500 = np.asarray(PC7["mg"], float), np.asarray(PC7["R500"], float)
R = np.logspace(-3, np.log10(30), 3000)
out = {"lane": "CFG949", "amendment": "A1 post hoc 2026-10-20, no class weight", "rows": {}}
lines = []
for beta in (2 / 3, 0.6, 0.8):
    ratio = np.empty(len(MG))
    for i in range(len(MG)):
        rc = 0.15 * R500[i]; shape = (1 + (R / rc) ** 2) ** (-1.5 * beta); shape[R > 3.0] = 0
        dm = 4 * np.pi * R ** 2 * shape; M = np.r_[0, np.cumsum(0.5 * (dm[1:] + dm[:-1]) * np.diff(R))]
        ratio[i] = M[-1] / np.interp(R500[i], R, M)
    q = np.percentile(ratio, [16, 50, 84]); share = 1 - 1 / ratio
    out["rows"][f"beta{beta:.2f}"] = dict(Mgas3_over_Mgas500_p16_50_84=q.tolist(), share_beyond_R500_median=float(np.median(share)))
    lines.append(f"beta {beta:.2f}: M_gas(<3 Mpc)/Mgas500 median {q[1]:.2f} (16-84% {q[0]:.2f}-{q[2]:.2f}); share of the gas budget beyond R500 "
                 f"(extrapolated, unmeasured) median {np.median(share):.2f}")
lines.append("Reading: the S-cen cold supply (5.364 x catchment) inherits this share; the S-R500 corner (measured gas only) is the bound "
             "without it (main run: B0 FAILS there, lambda_OUT 2.87).")
with open(os.path.join(HERE, "cfg949_posthoc.out"), "w") as f:
    for s in lines:
        print(s); f.write(s + "\n")
json.dump(out, open(os.path.join(HERE, "cfg949_posthoc.json"), "w"), indent=1)
