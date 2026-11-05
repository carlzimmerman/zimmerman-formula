# DP4: sharded (parallel) Q1 cone fetch for cut 13: EQUIVALENT ON DR3, BYTE FOR BYTE

Criteria `FROZEN_CRITERIA.md` (43d86506d1), committed alone before the code. OFFLINE, new code only; no frozen file
edited; nothing fetched. DR3 numbers are code-path tests, never results; NON-SCORING. κ = ½ FITTED; not theory closed.

## Result
- **S1 PASS.** Splitting the 10,231 DR3 candidates into K sky-contiguous shards (contiguous source_id1 = nested
  HEALPix order), each with only its own cone rows, gives the driver's final catalogue **byte-identical** to the
  unsharded run:
  - cones-literal: 6,180 pairs, sha256 c5cb89e8f95bfe3d, at K = 2, 4 (written to FITS and read back through
    `ConeTable.from_files`) and 8;
  - cones-orbit: 6,190 pairs, sha256 31b1c8b99a594b6e, at K = 4.
- **S2 PASS.** Every candidate is in exactly one shard.
- **S5 PASS.** The subset check (the two WP1 literal hits plus 100 seeded pairs) flags exactly the two hits.
- **S4 PASS.** The printed per-shard commands keep the frozen `--spec`, have distinct tags and manifests, and their
  caps sum to the given cap.
- **S3 (information).** Planned units total 170,091 against 170,064 unsharded (ratio 1.000 at K = 2, 4 and 8).
  The largest shard holds 0.504 / 0.257 / 0.131 of the serial units at K = 2 / 4 / 8.
  - Sharding does not inflate the query count.
  - Wall time scales about as 1/K, *if* the archive serves K concurrent sync requests at the single-request pace.
  - The central 47 h estimate becomes **about 12 h at K = 4 and about 6 h at K = 8**, an untested assumption about
    the archive.
- **MUTATE=1** (one shard left out): S1 FAILED as designed (ConeCoverageError: no pair is treated as "no third star").
- **MUTATE=2** (one shard's pair ids shifted): S5 FAILED as designed.

## Disclosures
- **Run 1, S4 FAILED, a test-parser fault.** The placeholder output directory `<data dir>` contains a space, so the
  test's split cut every manifest path to the same token. The tool's commands were correct. The placeholder was changed
  to `<data_dir>`. Run 1 is kept as `test_dp4_shards_dr3_run1_S4_PARSER_FAILED.out`, with its scratch path redacted.
- A run before run 1 stopped on a `load_spec` return-type error in the information step S3, after S1, S2 and S5 had
  already passed. It was fixed in both files, and no output from it was kept.
- **Peak RSS about 5.3 GB** (peak footprint 2.5 GB), above the 4 GB the criteria stated. The run took 30 s and no
  1024³ job was live.

## Release day
1. `dry_run_driver.py --dump-candidates` gives the DR4 candidates.
2. `python3 -B dr4_push_2026_11_05/DP4_parallel_q1/dr4_shard_q1.py --pairs-csv <candidates.csv> --k <K> --out-dir <data_dir>
   --spec dr4_all_source --stage-a <dr4_extract>/stage_A.npz --cap-accepted-mb <A> --cap-received-mb <R> --max-queries <Q> --plan`
   prints the K fetch commands and a driver manifest.
3. Run the K commands concurrently, each with the owner's go recorded. The owner chooses K together with the caps.
4. The driver runs with `--cut13 cones-literal --neighbours-manifest <manifest>`.

What the test does not cover: how the archive behaves under K concurrent requests (it may throttle), and whether a
registered account changes the rate. Start with K = 4 and read the first progress lines for the real rate.
