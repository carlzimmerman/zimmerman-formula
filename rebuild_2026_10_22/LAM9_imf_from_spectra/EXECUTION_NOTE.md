# LAM9 execution note (not a method change)

κ = ½ FITTED; not theory closed. The criteria (9c1f411110) and amendment A1 (66fb0bbf80) are unedited.

## Sharding
- The fits run as four independent single-thread processes. Shard k takes the jobs whose list index mod 4 equals k, so
  every sum is fitted by exactly one process.
- Each shard writes its own JSONL file outside the repo (`_external_data/lam9_work_2026_11_04/fits/`). Each line is flushed
  and fsync'd.
- `--merge` checks that no sum has two lines for the same variant. It then writes `lam9_fit_*.jsonl` here, sorted by plateifu.
- The K synthetics are split the same way by synthetic index. Every synthetic's donor, Γb_in and noise seed come from one
  plan drawn in index order, so the split does not change any input.

## A restart, disclosed
- The first launch, at 13:08 on 2026-11-04, imported numpy before the single-thread variables were set. Each process
  therefore held BLAS thread pools (16 threads), though each ran at about 100 % of one core.
- That launch was stopped with SIGTERM after five sums. Every shard exited 75 at a sum boundary.
- The variables were then moved before the numpy import, and the shards resumed with `--resume`, each with one thread.
- The five sums fitted before the restart were kept, not refitted.

## The queue
- `compute_queue/heavyq.py` was blocked at its head of line (A1 item 7), so the shards run directly with `nice -n 10`.
- They follow the job contract: SIGTERM or `compute_queue/YIELD` gives exit 75 at a sum boundary, and `--resume` continues.

## Order of the run (A1 item 3)
- The 330 donor sums (the first 110 of each third) were fitted from 13:08 to 13:43. There were no fit errors.
- The 300 K synthetics ran from 13:44 to 14:49 as four shards split by synthetic index. All 300 succeeded.
- K1 failed on both variants, so the remaining 1256 sums were not fitted and nothing was graded.

## Resources
- Each shard's physical footprint peaked at 0.82-0.91 GB during loading and sat near 0.13-0.15 GB while fitting.
- Variant A takes a median 10.5 s per sum, and A plus B about 20 s.
