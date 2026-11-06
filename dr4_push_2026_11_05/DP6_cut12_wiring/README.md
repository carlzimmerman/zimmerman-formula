# DP6: the filed A17 cut 12 (NSS screen) wired into the DR4 build: BUILT, 8/8 CHECKS PASS, BOTH MUTATES BITE

Criteria `FROZEN_CRITERIA.md` (ee74edfda2), committed alone before the code. New code only; no frozen file edited (T0).
DR3 numbers are code-path tests, never results. NON-SCORING. κ = ½ FITTED; not theory closed.

## Why (DP3 open issue O8)
- The frozen builder's `frozen_cuts` reads the NSS flag `S["non_single_star"]` from stage A (build_catalog.py:328).
- DR4's `gaia_source` has no such column.
- `dry_run_driver.py` imports `cut12_nss_union` but never calls it.
- So every DR4 build (G6, G8, G10, G11) would have raised KeyError, and the G5 NSS id files would have been read by nothing.
- T5b confirms the crash on a fake stage A without the column.

## What it does
- **`a17_cut12.py`**
  - Rebuilds `frozen_cuts` from its own source with one line changed:
    `nss = _DP6_NSS(S, a, b)` = `cut12_nss_union.run_a17(manifest, ids_a, ids_b)['A17_primary']`.
  - This is the filed Amendment 17 reading (ab9557d58). It is applied pair by pair, so the own-pair exemption for
    ResolvedPairFixed/Linear exempts only that pair.
  - It uses the same source-patch mechanism as CFG816's variant builder.
  - DP1's NSS-off patch composes on top of it.
- **`dp6_with_a17.py --a17-manifest M -- <script> <args>`**
  - Installs the patch, then runs a frozen CLI script in the same process (dry_run_driver.py, seed_sweep.py, nss_off_rung.py).
  - `--report-json` saves run_a17's per-table report for the manifest.
- **`dp6_with_a17.py --write-per-star OUT --stage-a stage_A.npz`**
  - Writes stage A plus `non_single_star = 0`.
  - This is the R input for `make_pair_table.py --declare-neutral non_single_star` (D7 N5).

## Result (`test_dp6.out`; MUTATE runs `test_dp6_MUTATE1.out`, `test_dp6_MUTATE2.out`)
| check | result |
|---|---|
| T1 patched source differs in exactly one line; getsource works; uninstall restores the original | PASS |
| T2 synthetic: exempt own pair kept; non-exempt own pair, third-source row and solution-on-star rejected; untouched kept; = run_a17 = hand truth | PASS |
| T3 DR3, per-star column REMOVED, cut 12 from a one-table A17 manifest (84,906 NSS ids): **6,210 pairs, sha 6fff64d964ebaa72** = registered | PASS |
| T4 DP1 rung on the patched builder: **6,282 pairs, sha 1dbdf21a** = DP1 | PASS |
| T5 launcher subprocess writes the T3 CSV with the screen active (5,555 of 213,097 stage-F pairs rejected); T5b unpatched code raises KeyError | PASS |
| T6 refusals (undeclared reading; no readings); install idempotent | PASS |
| T7 per-star file accepted by make_pair_table | PASS (run 2) |
| T0 frozen files unchanged | PASS |
| MUTATE=1 (screen off) | T3 FAILED as designed |
| MUTATE=2 (every own-pair row exempt) | T2 FAILED as designed |

**Run 1 failed T7 because of a fixture flaw, disclosed:**
- The fake stars all had parallax 10.0, and make_pair_table correctly refuses a constant column.
- Run 2 varies parallax by pair. No tool code changed.
- The run-1 output is kept as `test_dp6_run1_T7_FIXTURE_FAILED.out/.json`.

Peak RSS 1.3 GB, about 12 s per run.

## Release day (wired into DP3's `dr4_release_day.sh`)
- G6, G8, G10 and G11 run through `dp6_with_a17.py --a17-manifest "$M" --report-json <step>_a17.json --`.
- O12 builds `stage_A_nss0.npz` with `--write-per-star`.
- G5 now requires `cut12_nss.readings.A17_primary.counted_tables`, `id_files` and `solution_types_recorded` (A17 (d)) to be
  filled before the builds.

## Not covered
- Real DR4 table names, column names and solution_type strings (recorded on release day before opening).
- cones-literal cut 13 was not exercised here; T3 uses extract-builder, and the NSS line is independent of cut 13.
- `seed_sweep.py` passes manifest None to the driver, so manifest column joins do not apply in G10. This matters only if DR4
  moves ruwe, ipd or RV out of `gaia_source`.
- Departure from the criteria: none in the tool. T7's fixture was corrected between runs, as disclosed above.
