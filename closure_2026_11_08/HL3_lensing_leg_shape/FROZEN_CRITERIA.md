# HL3 frozen criteria: the law's cluster residual per bin on the LENSING leg against the HYDROSTATIC leg

Frozen before any script producing a graded number exists and before any new file is downloaded. Kappa = 1/2
FITTED; not theory closed. Adopts nothing; the owner adopts. No dark-matter particle. Both footings graded
separately (canonical a0 1.2e-10, alt 1.1e-10), never pooled. Follows HL1 (e9212275db) and HL2 (da7b5808f7),
which compared lensing and hydrostatic MASSES at R500 on published pairs and read NO GAP (+0.031 +- 0.020 dex,
81 clusters). HL3 asks the per-bin SHAPE question those lanes did not: does the law's cluster residual have
the same radial shape on a lensing-only mass profile as on the hydrostatic one?

## Why

The record's hot-leg need (X-COP x4.2 canonical / x3.8 alt at R500) and its radial clue ("too little in the
centre, too much outside"; NA2 (d): stars-traced bins -0.068 / +0.089 / +0.070 dex at 0-0.25 / 0.25-0.5 /
0.5-0.75 R500, canonical) rest on hydrostatic masses (X-COP, 12 clusters, `real_research/data/xcop/*/`
`_hydro_mass.fits` M_FORW, `_fgas_profile.fits`, `_mstar.fits`, R500 from `xcop_r500_ettori2019.json`). A
hydrostatic mass can carry non-thermal pressure and core systematics that a lensing mass does not. The record
holds a lensing-only leg on disk and never graded it per bin: Tian+2020 (ApJ 896, 70; VizieR J/ApJ/896/70/fig2,
`real_research/data/clash_rar_tian2020_fig2.tsv`, 84 (g_bar, g_tot) points in 20 CLASH clusters at 14.3-600
kpc; g_tot from the Umetsu+2016 joint strong+weak lensing profiles, g_bar from Donahue+2014 gas + the BCG).
The frozen kill test "lensing = dynamics" (PREDICTIONS_2026_11_07.md section 3) was graded on galaxy-scale
lenses with weak power; a cluster-scale per-bin reading is the missing rung. Owner's go for downloads
(2026-11-08, verbatim): "Yes, download them".

## Data

On disk, read only (never edited): the two sets named above, the QX7 iter_5/iter_7 and NA2 loaders
(`closure_2026_11_06/QX7_unified_cold_switch/iter_7_collisionless_remnant/qx7_iter7.py`,
`closure_2026_11_07/NA2_compact_baryon_remnant/na2.py`), `hunt_2026/h56_clash_eta_collapse.py` and its `.out`.

To download (owner's go), into `_external_data/hl3/<source>/` at the repo root (untracked), each logged in
`closure_2026_11_08/HL3_lensing_leg_shape/FETCH_LOG.md` with URL, byte size, sha256 and use, no absolute
home paths, nothing downloaded executed, data files only:
- D1 Umetsu+2016 (ApJ 821, 116; VizieR J/ApJ/821/116): the per-cluster CLASH lensing mass or convergence
  profiles, to extend the lensing leg from 600 kpc to R500 and beyond. If the per-radius profiles are not in
  the VizieR tables, the arXiv source (1507.04385) tables are the fallback; if neither carries per-radius
  values, the extension is NOT RUN and the lane grades the on-disk 14.3-600 kpc leg only.
- D2 Donahue+2014 (ApJ 794, 136; VizieR J/ApJ/794/136 or arXiv 1405.7876 source): gas density profile
  parameters and BCG stellar masses for the same clusters, for g_bar beyond 600 kpc. If absent, g_bar beyond
  600 kpc is extrapolated from the on-disk points with the extrapolation flagged per bin.
- D3 (secondary, conditional) LoCuSS Okabe & Smith 2016 (MNRAS 461, 3794; arXiv 1507.04493, already fetched by
  HL2 as `okabe16`) per-cluster shear profiles and Martino+2014 gas; graded only if per-radius shear profiles
  are machine readable in the source. Otherwise D3 is NOT RUN, stated.
Budget: under 200 MB total; VizieR CfA mirror first, CDS second; a source that times out twice is logged and
skipped.

## Statistic

For every cluster and radius, the plain-law residual rho = log10(g_obs / g_law) with g_law = g_bar nu(g_bar/a0)
and nu the adopted law (g_N = g^2/(g + a0) inverted: g = (g_N + sqrt(g_N^2 + 4 a0 g_N))/2), per footing.
Radii in r/R500 with R500 per cluster: X-COP from the Ettori 2019 json; CLASH from the Umetsu+2016 lensing M500
(primary) and the Donahue X-ray M500 (bracket). Bins: edges 0, 0.25, 0.5, 0.75, 1.0, 2.0 (NA2's). Per bin and
per leg the cluster median of rho with a bootstrap 95 % interval over clusters (B 10,000, seed 1103), one value
per cluster per bin (that cluster's median within the bin) so no cluster is weighted by its point count.

- S1 (shape difference). Per bin: Delta_b = median_lensing - median_hydrostatic, with the bootstrap interval of
  the difference (independent resampling of the two samples).
- S2 (lensing-leg need at R500). The lensing-leg median rho in the 0.75-1.0 bin as 10^rho, against X-COP's
  hydrostatic need (NA2's F table, baryon-traced 4.206 / 3.811 at the captured amount; the plain-law X-COP
  rho in the same bin is recomputed here, not quoted).
- S3 (per-cluster scatter). Per leg, the scatter of rho at fixed r/R500 across clusters, to be set beside h56's
  0.176 dex per-cluster a0 scatter.

Samples: CLASH relaxed X-ray-selected 16 as primary, all 20 as bracket (the four high-magnification clusters
are mergers). X-COP all 12 (A2319 flagged for its 44 % non-thermal pressure claim, reported with and without).

## Decision rule (per footing)

- SAME SHAPE: every bin shared by the two legs has |Delta_b| <= 0.10 dex and its 95 % interval includes 0, on the
  primary sample. Reading: the hot-leg residual shape is NOT a hydrostatic artefact; the lensing = dynamics
  statement holds at cluster scale for the law's residual.
- HYDROSTATIC-SPECIFIC: the innermost shared bin has Delta_b <= -0.15 dex with its 95 % interval excluding 0
  (lensing shows less missing mass in the core than hydrostatics do), on the primary sample and the bracket.
  Reading: part of the core clue is non-thermal pressure or core systematics; the amount is Delta_b.
- LENSING-SPECIFIC: Delta_b >= +0.15 dex in any shared bin with the interval excluding 0 on both samples.
- UNDECIDED: anything else, with the bins printed.
A bin is "shared" when both legs have at least 6 clusters in it. Bins with fewer are reported, not graded.
S2 is reported with its interval, never graded as PASS/FAIL: the need on the lensing leg at R500 is a number
the record did not have, and it is written into RESULT.md as such (if the 0.75-1.0 bin has fewer than 6 lensing
clusters, S2 is reported at the outermost shared bin and says so).

## Known answers (must pass before the grade is read)

- KA1: h56's one-a0 fit on the 84 on-disk CLASH points reproduces chi2 136.1 (1 parameter) and the per-cluster
  a0 scatter 0.176 dex within 1 % (`hunt_2026/h56_clash_eta_collapse.out`).
- KA2: Tian+2020's slope-fixed g_ddagger 2.02e-9 m/s^2 is recovered from the same points within 10 % by the
  paper's fit (slope 1/2 fixed; a check that the leg is read in the paper's units and convention).
- KA3: the X-COP hydrostatic plain-law rho per bin, computed through NA2/QX7's loaders executed from source,
  reproduces NA2's baryon-traced F bracket when NA2's fit is rerun (4.206 / 3.811 within 1 %), and NA2's
  stars-traced bins -0.068 / +0.089 / +0.070 (canonical) within 0.005 dex.
- KA4: at R500 the two legs' masses on HL2's published pairs read NO GAP (+0.031 +- 0.020 from
  `rebuild_2026_10_22/HL2_combined_mass_pairs/hl2_results.json`, replayed); HL3's S1 in the 0.75-1.0 bin must be
  consistent with it (|Delta_b - 0.031| within the combined 95 % interval) when that bin is shared, else noted.
- KA5: the law inversion reproduces g = g_N at g_N >> a0 to 1e-9 and g = sqrt(a0 g_N) to 1 % at g_N <= 1e-3 a0.

## MUTATE (must bite)

- M1: legs swapped: every Delta_b flips sign (identity check on the grader).
- M2: plant +0.30 dex on the lensing leg's innermost bin: the label must read LENSING-SPECIFIC; plant -0.30 dex:
  HYDROSTATIC-SPECIFIC. If either fails to flip, the innermost bin has no power and the label is UNDECIDED (NO
  POWER) regardless of S1.
- M3: a0 -> 10 a0 on one leg only: Delta_b must move by more than its interval in every shared bin (the
  statistic sees the law, not only the data).

## Hand estimates (frozen, HIT/MISS in RESULT.md)

HE-a: the 0-0.25 bin reads Delta_b between -0.10 and 0 (lensing a little less missing mass in the core, within
the SAME SHAPE band). HE-b: S2's lensing-leg need at the outermost shared bin is within x1.3 of X-COP's. HE-c:
D1 extends the lensing leg to at least the 0.75-1.0 bin for >= 10 clusters. HE-d: S3's lensing scatter exceeds the
hydrostatic scatter by >= 0.05 dex.

Outputs: hl3_fetch.py (logs only), hl3.py, hl3_grade.py, hl3.json, hl3.out, hl3_MUTATE.out, FETCH_LOG.md,
RESULT.md. Commit with explicit paths; push via a temp detached worktree of origin/main. Downloads untracked.
Budget: compute minutes; RSS < 1 GB.
