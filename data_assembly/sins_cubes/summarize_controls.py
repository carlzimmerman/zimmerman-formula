#!/usr/bin/env python3
"""Controls C1, C3, C4 from the AMEND1 outputs, against the pass lines of FROZEN_CRITERIA_2026-09-30.md (unchanged by ADDENDUM_1). C3 is recomputed here from the profile CSV with bin radii rounded (the run_all value lost most galaxies to float mismatch of bin centres)."""
import pandas as pd, numpy as np, json
g = pd.read_csv("sins_ao_per_galaxy_AMEND1.csv"); p = pd.read_csv("sins_ao_profiles_AMEND1.csv"); p["R"] = p.R_arcsec.round(3)
rms = {}
for n, d in p.groupby("galaxy"):
    a = d[d.variant == "A"].set_index("R").Vlos_kms; b = d[d.variant == "B"].set_index("R").Vlos_kms; c = a.index.intersection(b.index)
    if len(c) >= 2: rms[n] = float(np.sqrt(np.mean((a.loc[c] - b.loc[c]) ** 2)))
g["C3_rms_AB"] = g.galaxy.map(rms); r = g.C1_ratio; n = int(r.notna().sum()); ok = int(((r > 0.75) & (r < 1.25)).sum())
res = dict(C1_within25=ok, C1_n=n, C1_fraction=ok / n, C1_pass=bool(ok / n >= 0.70), C1_median_ratio=float(r.median()), C3_n=len(rms), C3_median_rms=float(np.median(list(rms.values()))), C3_pass=bool(np.median(list(rms.values())) < 20),
           C4_median_dPA=float(g.dPA_best.median()), thin=int(g.thin.sum()), irregular=int(g.irregular.sum()),
           C1_within25_excluding_irregular=[int(((r > .75) & (r < 1.25) & ~g.irregular).sum()), int((r.notna() & ~g.irregular).sum())],
           ratio_gt_2=g[r > 2].galaxy.tolist(), ratio_lt_0p5=g[r < 0.5].galaxy.tolist())
g.to_csv("sins_ao_per_galaxy_AMEND1.csv", index=False); json.dump(res, open("control_results_AMEND1.json", "w"), indent=1); print(json.dumps(res, indent=1))
