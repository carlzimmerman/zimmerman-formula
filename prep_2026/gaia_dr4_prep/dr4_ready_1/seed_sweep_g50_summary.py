#!/usr/bin/env python3
"""DR4-READY-1: the summary of Q-G50 (SEED_SWEEP_G50_FROZEN.md, 62b165001): reads the manifest of `seed_sweep.py --K 50 --mode g-only --fit --jobs 4 --tag g50` and reports, per footing, SD(gamma-hat) over the 51 builds,
SD/mean sigma_fit with a 2,000-resample bootstrap (16th-84th percentile) interval, the mean one-way flips, the fit-only SD and the kappa range, next to the ten-build values of a51d6f8f2.  DR3 code-path numbers (Amendment 7(e));
no verdict word.  Run: python3 prep_2026/gaia_dr4_prep/dr4_ready_1/seed_sweep_g50_summary.py"""
import sys
sys.dont_write_bytecode = True
import json
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
M = json.load(open(REPO / "real_research" / "data" / "widebinaries" / "dr3_extract" / "seed_sweep" / "seed_sweep_manifest_g50.json"))
TEN = json.load(open(HERE / "seed_sweep_streams_dr3.json"))["QS"]
rng = np.random.default_rng(50)
out = ["Q-G50: stage-G-only spread on %d builds (DR3 PRIMARY base, registered fit path; DR3 numbers are code-path tests, never results)" % len(M["builds"])]
res = {}
for f in ("canonical", "alt"):
    g = np.array([b["fit"][f]["g"] for b in M["builds"]])
    s = np.array([b["fit"][f]["s"] for b in M["builds"]])
    ratio = g.std(ddof=1) / s.mean()
    bs = []
    for _ in range(2000):
        i = rng.integers(0, len(g), len(g))
        bs.append(g[i].std(ddof=1) / s[i].mean())
    lo, hi = np.percentile(bs, [16, 84])
    fo = np.array(M["sigma_build"][f]["fit_only_gammas"])
    kap = [b["fit"][f]["kappa"] for b in M["builds"]]
    res[f] = dict(n=len(g), sd=float(g.std(ddof=1)), mean_sigma_fit=float(s.mean()), ratio=float(ratio), ratio_16_84=[float(lo), float(hi)], fit_only_sd=float(fo.std(ddof=1)), fit_only_ratio=float(fo.std(ddof=1) / s.mean()), kappa_range=[min(kap), max(kap)],
                  gamma_mean=float(g.mean()))
    out.append(f"  {f:9s}: SD(gamma-hat) over {len(g)} builds {g.std(ddof=1):.4f}; mean sigma_fit {s.mean():.4f}; SD/sigma_fit {ratio:.3f} (bootstrap 16-84%: {lo:.3f} to {hi:.3f}); fit-only SD over {len(fo)} fits {fo.std(ddof=1):.4f} ({fo.std(ddof=1) / s.mean():.3f}); "
               f"kappa {min(kap):.4f}-{max(kap):.4f}; mean gamma-hat {g.mean():.4f}")
    out.append(f"             ten-build values quoted from a51d6f8f2: ALL {TEN['ALL']['per_footing'][f]['sd_over_sigma_fit']:.3f}; G-only {TEN['G-only']['per_footing'][f]['sd_over_sigma_fit']:.3f}; EF-only {TEN['EF-only']['per_footing'][f]['sd_over_sigma_fit']:.3f}")
fl = M["flips_vs_k0"]
res["flips_mean_one_way"] = float(np.mean([(a + b) / 2 for a, b in fl]))
out.append(f"  one-way pair flips against k = 0: mean {res['flips_mean_one_way']:.1f} over k = 1..{len(fl)} (ten-build G-only 142.3, ALL 157.8); final pairs mean {np.mean([b['n_pairs'] for b in M['builds']]):.1f} (SD {np.std([b['n_pairs'] for b in M['builds']], ddof=1):.1f})")
(HERE / "seed_sweep_g50_summary.out").write_text("\n".join(out) + "\n")
json.dump(res, open(HERE / "seed_sweep_g50_summary.json", "w"), indent=1)
print("\n".join(out))
