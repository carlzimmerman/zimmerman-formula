# DP4 FROZEN CRITERIA: sharded (parallel) Q1 cone fetch for cut 13, proven equivalent on DR3

Written 2026-11-05, committed alone before any code or number. OFFLINE and NEW CODE ONLY: no network, no download, no
frozen file edited (`dry_run_driver.py`, `cones_cut13.py`, `dr4_archive_fetch.py`, `q1_cones_dr4.py`, the pipeline, the
prereg and its amendments, the 2026-11-05 owner decisions). DR3 numbers are code-path tests, never results (Amendment 7(e));
NON-SCORING; no verdict words. κ = ½ FITTED; not theory closed.

## Why
The release-day critical path is the cut-13 Q1 cone fetch: ~39k sync queries, ~47 h serial at the central estimate, up to
189 h if the archive is 4x slower (`dr4_q1_estimate_example_N49000.out`). Server-side upload joins stalled on the anonymous
ESA archive (PLAN.md, 2026-09-29), so a bulk join is not a tested option. The query form that works (literal source_id
ranges, sync) is per-unit independent, and the driver already combines several neighbour files (`--neighbours` /
`--neighbour-pairs`, repeatable; `ConeTable.add` de-duplicates rows). So the fetch can be split by sky region into K
shards run concurrently, with the SAME query form, the SAME rows and the SAME driver path. This lane builds that and
proves it changes nothing.

## What is built (new files in this folder)
- `dr4_shard_q1.py`: splits a candidates CSV (`source_id1,source_id2`) into K shard CSVs in contiguous source_id1 order
  (source_id encodes nested HEALPix, so shards are sky-contiguous); writes a `--neighbours-manifest` JSON listing the K
  (neighbours FITS, pairs CSV) entries; prints the K `q1_cones_dr4.py` commands with each cap = the owner's cap / K
  and its own manifest and tag. Offline `--plan` mode counts, with `dr4_archive_fetch.plan_pairs` (imported read only),
  the units per shard and in total against the unsharded plan.
- `test_dp4_shards_dr3.py`: the DR3 equivalence test below.

## Controls (all reported; failures reported plainly)
- **S1 byte identity.** On the 10,231 DR3 candidates with the real on-disk cones (`q1_full_neighbours.fits` with the
  6,210 final pairs, `q1_delta_neighbours.fits` with the 4,021 delta pairs), re-split into K = 4 shards (each shard's
  FITS rows = the rows whose pair falls in that shard, pair_id re-indexed to the shard CSV), the driver's final CSV for
  `cones-literal` and for `cones-orbit` is BYTE-IDENTICAL (sha256) to the unsharded run. Also K = 2 and K = 8 for
  `cones-literal`.
- **S2 coverage.** Every candidate is in exactly one shard; the union of shard keys equals the candidate set.
- **S3 plan overhead.** For the DR3 candidates, the total planned units over K shards is reported against the unsharded
  plan (K = 2, 4, 8). Information: a ratio above 1.10 at K = 4 is reported as "sharding inflates the query count" and
  the projected wall time is computed with the inflated count. No pass or fail.
- **S4 commands.** The printed per-shard commands use the same `--spec`, the frozen query form, caps summing to the
  given cap, distinct manifests and tags.
- **MUTATE=1** one shard left out: the driver must raise `ConeCoverageError` (missing = error) and S1 must FAIL.
- **MUTATE=2** one shard's pair_ids shifted by one within the shard: the K3b-style subset check (the two literal WP1
  hits plus 100 seeded final pairs, flags on that subset only) must FAIL.

## Limits (stated before the run)
Equivalence is proven for the assembly and the driver path, not for the archive: concurrency on the real archive may be
throttled, and a registered account may change the rate. The concurrency level K on release day is the owner's choice,
given with the caps. Nothing here authorises a query. Memory: ≤ 4 GB RSS, OMP_NUM_THREADS=1, nice -n 10.
