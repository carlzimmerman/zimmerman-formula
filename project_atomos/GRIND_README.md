# GRIND — resumable depth-escalation grinder (40 GB cap)

Continues the committed depth-6/7 CLEAN NULLS past the old depth-8 memory wall, under the
owner-authorized **40 GB** cap (2026-07-21; machine 64 GB, >= 24 GB headroom, never swap).
RULE 3 held: `gate/ engine/ exhaust.py exhaust_parallel.py exhaust_depth4_forced.py
exhaust_depth5_forced.py exhaust_depthN_forced.py` have **zero diff** — `grind.py` imports them
verbatim and overrides the imported 6 GB watchdog attribute **at runtime only**.

## Start / stop / status

```
./grind.sh                          # start (or resume) the escalation from the first depth >= 8
Ctrl-C  (or kill <pid>)             # safe ANY time: state is boundary-atomic, ledger append-only
kill -9                             # also safe: loses at most the in-flight phase/target
python3 grind.py --status           # ledger + in-flight state + honest ETA notes
python3 grind.py --replay 6         # replay gate (must PASS before trusting the streamed build)
python3 grind.py --replay 7
python3 grind.py --deep-sample --depth 12 --trials 2000000 [--seed 1]
```

## What gets recorded where (all under `results_grind/`)

| path | contents |
|---|---|
| `LEDGER.jsonl` | one append-only line per finished depth (verdict, counts, walls, **mem_cap_gb**) |
| `state.json` | atomic (tmp+rename) checkpoint: depth / phase / in-flight target, sample trial counter |
| `depth_D/VERDICT.json` | raw, distinct, hits, per-target rows, CERT/RELAB, tightest hit + formula, walls, peak RSS, validation heads |
| `depth_D/completeness.json`, `a0.json` | the per-depth validation heads (verbatim committed checks) |
| `depth_D/values.f64`, `records.sqlite`, `build_meta.json` | streamed build: distinct values, in-window formula records, completion marker |
| `depth_D/targets/<key>.json` | per-target sweep reports (resume granularity) |
| `SAMPLE_LEDGER.jsonl`, `sample_dD_sS/hits.jsonl` | deep-sample runs and their hits |
| `grind.log` | tee'd console output |

Every entry records `mem_cap_gb` actually in force. The committed depth-6/7 nulls
(`results_exhaust_depthN/`, 6-GB-era) are ground truth and are **never conflated** with
40-GB-era results.

## Per depth (never skipped, in order)

1. **Completeness self-check** — verbatim `constructive_completeness_selfcheck` (memory-light).
   If it cannot run, the depth is recorded **UNVALIDATED** and escalation **stops** (an
   unvalidated null is never reported).
2. **a0-validity** — verbatim `a0_validity_depthN`.
3. **Streamed build + 21-target sweep** — single process, build once, targets sequential;
   every in-window hit goes through the **real committed gates** (rebuilt ExprNode ->
   `gate_candidate_for` -> `gate.validate`), never a reimplementation.

## Honest expectations under the 40 GB cap (ranges, not precision)

| depth | expectation |
|---|---|
| D8 | ~10-25 min total; first depth past the old wall. Unstreamed build measured 5.77 GB (fits); the streamed build stays well under 1 GB |
| D9 | first genuinely NEW ground. Build+sweep ~1-2 h by the ~4.7x raw growth; **but** the b_s=5 completeness brute is ~30^5-sized (~1-2 h more) — budget ~2-4 h. ~27 GB only if the unstreamed path were used; streamed stays low |
| D10 | ~a day-class, **REQUIRES the streamed path** (unstreamed projects ~127 GB). Caveat: the b_s=6 completeness brute is ~30^6-sized and projects to **days** single-threaded — the validation, not the sweep, is the binding cost |
| D11+ | days-to-weeks EACH (raw ~4-5x/depth, completeness brute ~30x/depth) |
| D14 | exhaustive run **not realistic** — that is what `--deep-sample` is for |

Each further depth is ~4-5x slower on build/sweep alone; no false precision is printed —
`--status` shows measured walls from the ledger and scales from those.

## The both-ways rule (non-negotiable)

- **NULL (0 certified) is the expected/valid outcome** and is reported as **CLEAN NULL** —
  never dressed up, never dismissed.
- Any all-gates survivor is **CANDIDATE-NEEDING-SCRUTINY** (escalation stops for human
  review) — **never a discovery claim**.
- `--deep-sample` is non-exhaustive: it can **never claim a null**, and every sampled hit is
  labeled **CANDIDATE (sampled, non-exhaustive)** with the sampled-trials multiplicity recorded
  for conservative E_chance accounting. The sampler is a fixed, seeded, documented distribution
  (uniform over valid generator tuples — see the `grind.py` docstring), not uniform over
  distinct values.
- The replay gate (`--replay 6` / `--replay 7`) must reproduce the committed numbers exactly
  (distinct 107,719 / 498,848; hits 259 / 1,248; tightest `koide_Q_lep` rel 9.23e-06) or it
  exits nonzero — do not trust new-depth results if replay fails.
