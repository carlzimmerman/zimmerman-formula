# DP6: wire the filed Amendment 17 cut 12 (NSS screen) into the DR4 build: FROZEN CRITERIA

Committed alone, before any code. New code only; no frozen file is edited. DR3 numbers here are code-path tests, never
results. NON-SCORING. κ = ½ FITTED; not theory closed.

## Why (DP3 open issue O8, 27cfb3ea4e)
- The frozen `catalog_builder/build_catalog.py` `frozen_cuts` computes the NSS screen from a per-star column (line 328):
  `nss = (S["non_single_star"][a] > 0) | (S["non_single_star"][b] > 0)`.
- DR4's `gaia_source` has no such column (DP5 drops it from the stage-A SELECT; the frozen SELECT would fail instead).
- `dr4_ready_1/dry_run_driver.py` imports `cut12_nss_union` but never calls it.

So every DR4 build raises KeyError at its first `frozen_cuts` call: G6 candidates, G8 primary, G10 seed sweep, G11 NSS-off
rung. The G5 id files are read by nothing.

Amendment 17 (filed, ab9557d58) fixes cut 12 for DR4 as **`cut12_nss_union.run_a17` with reading `A17_primary`**, a
pair-level rule. It is not a per-star flag: an `nss_resolved_pair` own-pair row of type ResolvedPairFixed/Linear exempts
that pair only.

## Design (fixed now)
1. `a17_cut12.py` builds a patched `frozen_cuts` from the frozen function's source text. This is the same mechanism as
   CFG816's `build_variant_catalogue.patched_frozen_cuts`. Exactly one line is replaced: the `nss = ...` line at line 328
   becomes a call `nss = _DP6_NSS(S, a, b)`. It refuses if that line is not found exactly once.
   - `_DP6_NSS` maps the pairs (S["source_id"][a], S["source_id"][b]) to `run_a17(manifest, ids_a, ids_b)[reading]`.
   - The reading is `A17_primary` by default. It is never chosen from the data.
   - The result is cached by the sha256 of the two id arrays.
   - Every other line, and the cut order, is unchanged.
   - The patched source is registered in `linecache`, so `inspect.getsource` works on it, and CFG816's `drop_nss` / `smax`
     patch composes on top (DP1's rung).
   - `install(manifest_path, reading)` puts the patched function into the builder module, and therefore the driver.
     `uninstall()` restores the original.
2. `dp6_with_a17.py --a17-manifest M [--reading R] -- <script.py> <args...>` installs the patch, then runs the target script
   in-process as `__main__` (runpy) with its own argv. This covers the CLI steps (`dry_run_driver.py`, `seed_sweep.py`,
   `nss_off_rung.py`) without editing them.
3. `--write-per-star OUT.npz --stage-a stage_A.npz` writes stage A plus `non_single_star = 0` for every star. This is the
   R-input per-star file for `make_pair_table.py --declare-neutral non_single_star` (D7 N5; the registered catalogue is
   already NSS-screened).

## Checks (`test_dp6.py`, socket guard on, no network)
- **T0** sha256 of the frozen files is unchanged before and after the run: build_catalog.py, dry_run_driver.py,
  cut12_nss_union.py, cut12_stub.py, build_variant_catalogue.py, seed_sweep.py, wide_binary_pipeline.py, nss_off_rung.py.
- **T1 patch mechanics.**
  - The patched source differs from the frozen source in exactly one line.
  - The `"NSS screen": ~nss,` line is present once.
  - `inspect.getsource` works on the patched function.
  - `uninstall()` restores the identical original object.
- **T2 synthetic known answer** (small fake S and F, fake id files).
  - The fake cases are:
    - a one-source solution on a component;
    - an own-pair resolved-pair row of an exempt type (ResolvedPairFixed);
    - an own-pair row of a non-exempt type;
    - a third-source row;
    - a pair that nothing touches.
  - The patched `frozen_cuts` "NSS screen" keep-mask must equal both `run_a17(...)['A17_primary']` and a hand-written truth
    (exempt pair kept; the others rejected; the untouched pair kept).
- **T3 DR3 equivalence.**
  - Setup:
    - A manifest declares one one-source table, `dr3_nss_proxy`: the source_ids of DR3 stage-A stars with
      non_single_star > 0, written as an id file.
    - Reading `A17_primary` counts only that table, with no exemptions.
    - The `non_single_star` column is **removed from S** before the build (a test-only wrapper around the driver's
      `apply_manifest_columns`), so any read of it would raise.
  - `dry_run_driver.run("dr3", "primary", "extract-builder", ...)` must reproduce the registered catalogue: 6,210 pairs,
    sha256 prefix 6fff64d964ebaa72.
- **T4 composition with DP1's rung.** With the patch installed and the column removed, `nss_off_rung.rung_build(True, 30)`
  must reproduce DP1's DR3 rung CSV: 6,282 pairs, sha256 prefix 1dbdf21a.
- **T5 launcher.** `dp6_with_a17.py --a17-manifest <T3 manifest> -- dry_run_driver.py --release dr3 --cut13 extract-builder
  --out-csv X`, run as a subprocess, must write a CSV with the T3 sha.
  - With no patch, the same command on a stage-A copy without the column is not run: it would need a second copy of the
    4.6 M-row extract.
  - Instead, T5b: calling the unpatched frozen `frozen_cuts` on the T2 fake S without the column must raise KeyError.
    This shows O8 is real.
- **T6 refusals.**
  - A missing reading name refuses.
  - A manifest with no `readings` refuses, by run_a17's own rule.
  - Install twice is idempotent.
- **T7 per-star file.** `--write-per-star` on the T2 fake: every stage-A column is preserved byte for byte; `non_single_star`
  is all 0; `make_pair_table.build(..., declare_neutral=("non_single_star",))` accepts it.

**MUTATE controls** (each must make its target check FAIL):
- MUTATE=1: `_DP6_NSS` returns all False (the screen off). **T3 fails.**
- MUTATE=2: `cut12_nss_union._MUTATE_A17 = "exempt_all"` (every own-pair row exempt). **T2 fails.**

## Verdict rule
- **BUILT:** T0–T7 all pass and both MUTATEs bite. DP3 O8 is then closed by routing G6, G8, G10 and G11 through
  `dp6_with_a17.py`, and the R-input per-star file is made by `--write-per-star`.
- **NOT BUILT:** any check fails. O8 stays blocking. Nothing is tuned to pass; a failing check is reported as is.

## Not covered
- Real DR4 table names, column names and solution_type strings (A17 (d): recorded on release day before opening).
- The cones-literal cut 13 (T3 uses extract-builder; the NSS screen line is independent of cut 13).
- `seed_sweep.py` passes `manifest=None` to `D.run`, so the manifest's column joins (ruwe, ipd, RV) do not apply in the sweep.
  This is reported, not fixed here. It matters only if DR4 moves those columns out of `gaia_source`.
- Memory: each DR3 build is about 1 GB, a few minutes; run alone, single-threaded.
