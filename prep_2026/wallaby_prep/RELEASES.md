# WALLABY public releases — what exists NOW for per-side work (2026-07-16)

Door 5 prep (directional-EFE scale-up). Every count below is recomputable by
`wallaby_census.py` (live CADC TAP, anonymous); gate + pilot by
`perside_extractor.py`. Banked requirement: N ~ 1,157 signed per-side
asymmetries (canonical a0 = 9.36e-11, max-clustering e_N, AQUAL-vs-BranchB
w = 0.304; alt footing 1.13e-10 → N ~ 1,424) — source:
`zimmerman-formula/real_research/reviews/directional_efe_2026/confrontation.out`;
AQUAL-amplitude band N ~ 192–3,057 (`laneB_FEASIBILITY.md`). In hand before
this door: 16 signed per-side galaxies (van Eymeren+2011 × Chae+2021).

## 1. Releases and access points

| Release | Date | Contents | Kinematic models |
|---|---|---|---|
| Pilot DR1 | 2022-11-15 | ~600 HI sources; Hydra, Norma, NGC 4636 fields (Westmeier+2022, PASA 39 e058) | WKAPP flat-disk tilted-ring models for 109/592 detections (Deg+2022, PASA 39 e059, arXiv:2211.07333) |
| Pilot DR2 | 2024-09-23 | ~1800 HI sources at 30″; NGC 4808, NGC 5044, Vela; +80 galaxies at 12″ high-res (Murugeshan+2024, arXiv:2409.13130) | WKAPP models for >120 spatially resolved detections |
| 3KIDNAS (announced) | 2025 newsletter 21 | successor pipeline applied to all PDR1+PDR2 | ~400 models generated; CADC/CASDA upload pending release paper — **not yet public** (absent from the CAOM2 census below) |
| Full survey | — | ~210,000 detections expected to z~0.1 | Deg+22 projection: ~40,000 models (20% success), floor "likely higher than 10%" (~21,000) |

Access (all anonymous/public):
- CADC direct file service (used by the pipeline):
  `https://ws.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/raven/files/cadc:WALLABY/<filename>`
- CADC TAP (CAOM2): `https://ws.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/argus/sync`
  (collection = 'WALLABY'; productIDs `source_data_*` and `kinematic_model_*`)
- CASDA: https://data.csiro.au (WALLABY collections, DOI-linked)
- Survey data page: https://wallaby-survey.org/data/

## 2. Per-side vs azimuthally-averaged — the decisive fact

- **WKAPP rotation curves are azimuthally-averaged flat-disk ONLY.**
  Deg+2022 Table 3 products: `_AvgMod.txt` (geometry + single `VROT_model`
  column), `_ModRotCurve.fits` (same, FITS), `_ModSurfDens`, `_ModGeometry`,
  cubelets (`_ProcData`, `_ModCube`, `_DiffCube`, `_FullRes*`),
  `_DiagnosticPlot.png`. **No approaching/receding split is released anywhere.**
- **2D moment-1 velocity fields ARE downloadable per source** (SoFiA
  `_mom1.fits`, barycentric frequency in Hz, 20–400 KB each; verified by
  download for 3 galaxies). Plus `_mom0`, `_mom2`, `_cube`, `_mask`, `_spec`.
- Therefore per-side curves must be **re-derived**: mom1 field + WKAPP
  geometry → per-side outer rotation curves → signed asymmetry. That is
  exactly what `perside_extractor.py` does.

## 3. Measured census (live CADC TAP, 2026-07-16)

| Quantity | N (distinct J-name galaxies) |
|---|---|
| Sources with a mom1 velocity field | **2,426** |
| Galaxies with released WKAPP geometry (`_AvgMod.txt`) | **238** |
| **Per-side-capable NOW (both products)** | **237** |

(Cross-check: WALLABY newsletter 21 quotes "236 different galaxies" modelled
across PDR1+PDR2 — consistent.)

## 4. Honest capacity statement

- **NOW: 237** per-side-capable galaxies = **20%** of the canonical-footing
  N~1,157 target (17% of alt-footing 1,424; 8% of the 1%-AQUAL ceiling 3,057;
  **123%** of the most favorable 4%-AQUAL floor N~192).
  → The current public release CANNOT decide AQUAL-vs-BranchB at 3σ on either
  a0 footing; it CAN begin to probe the most favorable AQUAL-floor corner —
  a ~15x improvement over the 16 galaxies now in hand.
- **+3KIDNAS** (when public): ~400 models → capable count rises to ~400
  (still short of 1,157).
- **Full survey**: Deg+22's own projection ~40,000 models (floor ~21,000)
  exceeds every banked N target by >6x. The scale-up path is real but
  years-scale (full-survey observing + pipeline releases), not months.
- Independent missing ingredient (unchanged by WALLABY): the per-galaxy
  **g_ext DIRECTION**, reconstructable from public 2M++/MCXC/NSA per
  Chae+2021 sec. 3 — still must be built (banked in laneB_FEASIBILITY.md).
- Noise reality (from the synthetic gate, honest): single-galaxy
  σ(A) ≈ 0.013–0.030 at WALLABY pilot resolution (6-beam → 3.5-beam), i.e.
  a 2% aligned signal is an ENSEMBLE measurement; intrinsic lopsidedness
  scatter 0.092 (van Eymeren) remains the dominant noise, exactly as the
  banked power analysis assumes.

## 5. Files here

- `perside_extractor.py` — extractor + synthetic gate + 3-galaxy real PILOT
  (exit 0; gate PASS: injected +2% recovered as +0.0187±0.0024 at 6-beam,
  +0.0140±0.0039 at 3.5-beam marginal, null recovers 0.0018±0.0024, bootstrap
  pulls 0.75–0.88). Output: `run_perside.out`, `perside_results.json`.
- `wallaby_census.py` — live TAP census + capacity statement (exit 0; caches
  to `census_cache.json`). Output: `run_census.out`.
- `pilot_data/` — the 15 downloaded WALLABY files (3 galaxies × mom0/mom1/
  AvgMod/ModRotCurve/ModGeometry), CADC raven, fetched 2026-07-16.

PILOT results (proof-of-life ONLY, no physics claim; sanity vs WKAPP
azimuthal curve = 0.93–0.98):
- J125548+041805 (12″ high-res): A = −0.085 ± 0.008
- J165901−601241 (Norma 30″): A = −0.019 ± 0.007
- J100426−282638 (Hydra 30″, Deg+22 showcase, inc 75°): A = +0.225 ± 0.012
  (high inclination — thick-wedge projection systematics likely inflate this;
  a real campaign needs an inclination cut ~<70° and a warp/flat-disk budget).

These A values sit within/around the 0.092 lopsidedness rms measured on WHISP —
consistent with expectation, and a reminder that the directional test is a
stacked-ensemble statistic, not a per-galaxy one.
