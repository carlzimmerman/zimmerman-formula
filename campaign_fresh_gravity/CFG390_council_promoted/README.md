# CFG390: promoted dwarf/cluster calculations (exploratory runs of 10-06, now committed)

These calculations were first run in a git-ignored exploratory folder on 2026-10-06. Each `FROZEN_CRITERIA.md` section there was written before its script. The scripts are copied here unchanged, apart from attribution labels removed from the criteria headings and one disclosed bug fix (session05). Rerun from this location, all 26 outputs are **byte-identical** to the exploratory runs. Caveat: the freeze-before-run order was kept in the git-ignored folder, so git cannot prove it for these lanes. Commit timestamps prove it only for CFG391–CFG399.

κ = ½ fitted; both footings (9.36e-11 / 1.13e-10). No dark-matter particle; the cold mass is still required. Nothing here says the theory is closed or that the data favour the framework over ΛCDM.

| folder | test | verdict |
|---|---|---|
| session02 | light-end (2–4.4e-20 eV) soliton explanation of the MW ultra-faints | **DEAD**: soliton scaling rejected (Mahalanobis 6.23); implied m 3.9e-21 eV, outside the CFG367 window; Dalal & Kravtsov 2022 (arXiv 2203.05750) bound m > 3e-19 eV for a granular halo |
| session02 | fossil-phantom switch (λ_dB > r_½ keeps the target of the original baryons) | **FAIL**; scatter 0.20 → 0.33–0.39 dex |
| session02 | SPARC a₀ by distance method | not significant: flow − ladder +0.151 ± 0.084 (Υ 0.5), +0.113 ± 0.093 (Υ 0.7); estimator distance response ~D^−2.7 |
| session02 | super spirals vs the cm08 retention levels | all 23 at f = 0.16 (galaxy level); nine fastest 0.49 ± 0.24 (between); f–V correlation is a shared-variable artifact |
| session03 | UFD offsets vs tidal susceptibility at law-MW pericentres | **NOT TIDAL**: the tidally safest half sits at +0.36 dex (K2 control mis-specified, K2b hand check post-run) |
| session03 | the supply rule (cosmic share of ORIGINAL baryons, CFG317 R_ind) | **VIABLE** budget: median f_min 0.10 (yield bracket 0.05–0.21) |
| session03 | zero-parameter σ prediction with f_gal = 0.13 | level fixed (−0.05), but **NOT SUPPORTED**: scatter 0.204 vs the same-sample law's 0.193 |
| session04 | the same rule on the 12 MW classicals | median consistent (−0.16 ± 0.09; broken at yield +0.1); the single-rule check **FAILS** (UFD q 0.76 vs classical q 0.18) |
| session04 | SPARC residual skew (a binding supply limit) | **NO SUPPLY SIGNAL** |
| session04 | one universal cold density | vacuous PASS; the two populations need densities ×21 apart |
| session05 | shape of the X-COP missing mass | **NEITHER** target- nor baryon-shaped: more concentrated than both (log-slopes of ratios −0.46 ± 0.07, −0.33 ± 0.07); post-hoc NFW-like (r^1.39). Correction: the frozen MUTATE does not fire (see session05/RESULTS.md) |
| session06 | VPOS members vs non-members | **DISFAVOURED** TDG origin under the settling model (Δ +0.03 ± 0.10); VPOS normal recalled; rechecked with published values in CFG391 |
| session06 | fossil a₀ by Hubble type | **NOT POSSIBLE** on SPARC (0 early types with gas-dominated deep points); pursued in CFG395 |

Run any script from its own folder: `python3 <script>.py [--mutate]`. session03 `supply_ufd.py` / `predict_ufd.py` import session02's `fossil_switch.py` by relative path.
