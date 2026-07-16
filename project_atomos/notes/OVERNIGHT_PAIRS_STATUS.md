# Overnight GERM-PAIR Forced-Interlock Search — STATUS

**Launched:** 2026-07-07 02:37 (run stamp `20260707T023702`)
**Runner:** `overnight_pair_search.py --hours 8`  (detached, `nohup`)
**Python PID:** 22785
**Result dir:** `results_overnight_pairs/`

## What it searches
The last genuinely-untested large compute space after tonight's committed single-germ
nulls (depths 3–7 all null; 27 single germs all null; commit `b7f1f75`). Tests whether
any **PAIR** of the 27 pre-registered candidate forced germs — two symmetry invariants
BOTH injected into a COPY of `FORCED_CONSTRAINTS` (each with its registered law) —
jointly produces a **certified overdetermined interlock** that singles cannot express.

- **351 pairs** = C(27,2)
- **× depths {5, 6, 7}**  →  **1053 configs / full pass**
- **× 21 targets** per config
- Recipes/depth: 5→13,247 · 6→107,719 · 7→498,848  (sum 619,814)

## Anti-fabrication guard (THE #1 invariant)
FDR look-elsewhere multiplicity folds the ENTIRE search:
```
mult = n_targets × n_PAIRS × Σ_depth(n_recipes) = 21 × 351 × 619,814 = 4,568,648,994  (32.09 bits)
```
The **×351 pair factor is load-bearing** — trying more pairs RAISES the bar. This exact
`mult` threads into the gate's `n_targets_searched` (→ `gate/fdr.py:150`) on every route.
`_assert_full_pair_multiplicity` HALTS the run if `n_pairs != 351` or if `mult` omits the
pair factor (that omission would be the fabrication bug). Gate imported VERBATIM (zero-diff
vs HEAD in `gate/ engine/ exhaust_depth5_forced.py overnight_vocab_search.py`); germ_pool
stays 25 (FDR library is the full realistic pool, NOT inflated by forced-credit injection —
injection changes only Gate-B credit). A hit must clear ~10 surplus bits AFTER dividing by
ALL 4.57e9 trials.

## Memory guard
- Reach-lists built ONCE into `reach_by_depth` and REUSED across all 351 pairs; only Gate-B
  credit changes per pair. NOT accumulated across configs.
- Per-config loop mutates only scalars (counters) + one transient row + streaming BestHit.
- Mandatory 4 GB RSS watchdog (`getrusage` SELF+CHILDREN) at startup, each build-depth, and
  each config; SystemExit if breached.
- **Measured peak: ~1.61 GB, FLAT** (2.5× under cap; no per-config growth).

## Log path + how to tail
```
results_overnight_pairs/pair_search_20260707T023702.summary.txt   # human-tailable
results_overnight_pairs/pair_search_20260707T023702.jsonl         # structured, one line/level
results_overnight_pairs/pair_search_20260707T023702.header.json   # run params
results_overnight_pairs/run_launch.log                            # stdout (buffered)

tail -f results_overnight_pairs/pair_search_20260707T023702.summary.txt
```
Each level-line (per pair, per depth) is flushed+fsynced, so a crash leaves a readable
partial. Fields: counter, germ1+germ2, depth, n_targets, recipes, best hit (target/expr/
rel_err), gate verdict + Gate-A surplus bits (AFTER full pair-multiplicity look-elsewhere),
cumulative CERTIFIED, elapsed, peak RSS.

## Prior + interpretation
**STRONGLY NULL.** Everything collapses to the same FDR-DEAD Koide 2/3 near-miss
(rel_err 9.23e-06, but Gate-A surplus = −0.0 bits after the 32-bit look-elsewhere → killed).
Pairs face a ×351-higher FDR bar. A clean null is the EXPECTED and VALID outcome — this is
honest due diligence, not a promise of a hit.

**Any CERTIFIED line is a CANDIDATE-NEEDING-HUMAN-SCRUTINY** logged for verification —
explicitly NOT a TOE, NOT auto-trusted. The gate is never weakened to produce a hit.

## What a hit vs the null looks like
- **Expected null row:** `best=koide_Q_lep:FDR-DEAD ... FDRbits=-0.0 gateAsurplus=-0.0 CERTcum=0`
- **A genuine hit row would read:** `best=<target>:CERTIFIED ... gateAsurplus>=+10bits CERTcum>=1`
  — a positive Gate-A surplus surviving the full 4.57e9-trial look-elsewhere, with Gate B
  overdetermination (≥2 independent forced appearances) and Gate C. That line would be flagged
  for human verification, never trusted on its own.
