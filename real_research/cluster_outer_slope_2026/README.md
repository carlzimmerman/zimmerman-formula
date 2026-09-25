# COS1 — Cluster Outer-Slope Test (2026-09-25)

The zero-parameter prediction of the two-zone phantom law in the weak-lensing ESD beyond
R500, priced against LambdaCDM NFW and scored against the on-disk archive. Lane COS1 of
the clusters 'named pain' re-audit.

## One-line result
**INCONCLUSIVE (pre-registered, data gate not met):** no on-disk *cluster weak-lensing*
profile reaches 1.4 R500 (CLASH Tian+2020 rows stop at ~0.6 Mpc; the X-COP profiles on
disk are hydrostatic **X-ray**, reaching 2.1–2.9 R500, not shear). The predicted slope
contrast is large and a ~4.3e3-lens stack over [R500, 3 R500] would separate the two
slopes at 3σ — the test is survey-feasible, just not on this disk.

## Numbers (committed script output, M500 = 3e14 Msun, R500 = 1.05 Mpc, f_b = 0.16)
| quantity | value |
|---|---|
| framework window slope d ln ΔΣ/d ln R over [R500, 3 R500] (two-zone law, rho ~ r^-2) | **−0.997** (alt footing −0.998) |
| NFW window slope (anchor-matched 1.65–2.0 × M_b at R500, c = 3–5) | **−1.591 … −1.673** (c=4: −1.639; M500-anchored variant: −1.391) |
| slope contrast (framework − NFW, c=4) | **+0.642** (bracket +0.593…+0.675) |
| ESD amplitude separation ΔΣ_fw/ΔΣ_nfw | 2.03× over [R500, 3 R500] vs only 1.20× over [R500, 1.4 R500] |
| r_M / R500 (canonical a0 = 9.36e-11) | 0.267 Mpc / 3.93 (alt footing 4.31) |
| two-zone law M_tot(<R500) | 3.93 × M_b — **outside** the committed X-COP kernel anchor band [1.65, 2.0] (C5 FAIL, registered tension; the law still covers only 63% of the measured M500 — the cluster residual survives) |
| stack for 3σ slope separation, σ_dex = 0.15/10³-lens stack, K = 6 bins | **4.3e3 lenses** (bracket 1.7e3–2.0e4 for σ_dex = 0.1–0.3, c = 3–5) |
| same stack restricted to the X-COP reach [R500, 1.4 R500] | 4.7e4 lenses (10.8× — the reach is under-powered by **window length**, ΔlnR = 0.336 vs 1.099) |
| with the M500-anchored (cosmologically natural) ΛCDM reading | 1.1e4 lenses |

## Checks (main run: 6/7 PASS; only the C5 anchor-intercept tension fails, as registered)
C1 framework slope band (−1.25, −0.75) · C2 NFW slope band (−2.3, −1.40, c = 3–5) ·
C3 contrast ≥ 0.40 · C4 MUTATE control (label swap flips C1–C3; contrast sign flips) ·
C5 R500 intercept in the committed [1.65, 2.0] × M_b band (**FAIL**, expected) ·
B1 stack requirement ≤ 1e5 · C6 self-audit record.

**MUTATE control** (`MUTATE=1 ...`): the NFW curve is presented as the framework
prediction and vice versa → C1–C4 all flip to FAIL, contrast −0.642 (rc = 1, as intended).

## Data gate inventory (scanned at runtime)
- `real_research/data/xcop/*/A*_hydro_mass.fits` — X-COP hydrostatic **X-ray** mass
  profiles, reach 2.10–2.85 R500 — not weak lensing.
- `real_research/data/clash_rar_tian2020_fig2.tsv` — lensing-based g_tot (Tian+2020,
  CLASH), 19 clusters, max reach 600 kpc (~0.55 R500 typ) — **does not reach 1.4 R500**.
- `real_research/data/lensing_rar/brouwer2021_rar/Fig-3_*.txt` — KiDS-1000 **galaxy-scale**
  stacks (M* ~ 1e11), projected reach 2.60 Mpc with ESD 0.77 ± 0.16 Msun/pc² — galaxy
  halos, not cluster outer slopes (noted per registration).
- `hff_granata_*` (source catalogues), `groener2016` (c200/M200 points),
  `kt2017`/`lovisari2015`/`psz2_union`/`erass1cl` (catalogues) — no radial WL profiles.

## Files
- `COS1_cluster_outer_slope.py` — the lane (run from the repo root; `MUTATE=1` for the control)
- `COS1_cluster_outer_slope.out` / `_results.json` — main run (rc 0)
- `COS1_cluster_outer_slope_MUTATE.out` / `_results_MUTATE.json` — control run (rc 1, intended)