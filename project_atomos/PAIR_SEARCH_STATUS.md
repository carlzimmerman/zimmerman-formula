# GERM-PAIR forced-interlock overnight search — STATUS

**Runner:** `overnight_pair_search.py` (new file; imports gate/ engine/ exhaust*.py +
`overnight_vocab_search.py` + `exhaust_depthN_forced.py` VERBATIM — RULE 3 zero-diff).
**Prior:** STRONGLY NULL. This is honest due diligence after the single-germ vocabulary was
exhausted (clean null, ~80 s, commit b7f1f75). NOT a promise of a hit.

## What it searches
The last untested large compute space: whether any **PAIR** of the 27 candidate forced germs
(a 2-symmetry forced structure, e.g. `A4_irrep3 x S3_order`), BOTH injected into a COPY of
`FORCED_CONSTRAINTS` (each with its law), jointly produces a certified overdetermined interlock a
single germ cannot express.

- **27** candidate germs (`assert len==27`) → **C(27,2) = 351 pairs** → x depths {5,6,7} =
  **1053 configs** x **21** SM targets.
- germ pool stays **25** (`assert len(alpha.germs)==25`); candidates are already in the FDR
  library — injection changes Gate-B CREDIT only, not the density library.

## The #1 anti-fabrication invariant (verified)
```
mult = n_targets x n_PAIRS x sum_depth(n_recipes) = 21 x 351 x 619814 = 4,568,648,994
```
- recipes/depth: d5=13,247  d6=107,719  d7=498,848  (sum 619,814).
- look-elsewhere penalty = **-log2(mult) = 32.1 bits** (+8.5 bits harsher than the single-germ
  mult from the x351 pair factor). A hit must clear PASS_BITS=10 AFTER -32.1 bits.
- Folds into the gate via `gate_candidate_for(..., n_targets_searched=mult)` (exhaust.py:536) →
  `SearchSpace.n_targets_searched` → `gate/fdr.py:150`.
- **`_assert_full_pair_multiplicity`** HALTS the run if the mult ever drops the x n_pairs factor
  (verified: the guard fires on the fabrication-bug mult, passes the correct one).

## Memory discipline (verified)
- The 3 depth reach-lists are built ONCE (pair-independent, same 25-germ pool) and REUSED across
  all 351 pairs; held simultaneously they peak at **1.61 GB** — under the HARD 4 GB cap.
- HARD `_mem_watchdog` (getrusage SELF+CHILDREN) at startup, after each depth build, and every
  config; ABORTS on >4 GB. Across configs only scalars accumulate (counter, certified_cumulative)
  + one transient row + the streaming BestHit inside `score_config`. No per-config reach-list, no
  per-hit list.

## Gate honesty (imported verbatim, no threshold touched)
- Gate B grants forced credit only via a registered law AND overdetermination (>=2 DISTINCT forced
  provenance keys). A pair supplies up to 4 forced appearances (2 injected + base {3,
  sqrt(8pi/3)}); a lone appearance is still "a definition, not a kernel". CERTIFIED iff A & B & C.
- Any CERTIFIED line = **CANDIDATE-NEEDING-SCRUTINY**, logged for human verification, explicitly
  NOT a TOE, NOT auto-trusted. A clean null is the expected, valid outcome.

## Validation (all exit 0)
- **`--injected-positive`** (detector control): an overdetermined synthetic PAIR (2 distinct forced
  provenance keys + 1 free) **CERTIFIES** even under a 5.16e9 mult (A 19.9 bits, B 2 appearances, C
  pass); the SAME structure with ONE forced appearance dies (REAL-PUZZLE-RE-LABELED, B fails) →
  volume/pairs cannot cheat overdetermination.
- **`--dry-run`**: n_pairs=351, mult=4.5686e9 = 21 x 351 x 619814, peak RSS 1.57 GB.
- **`--max-configs 12` smoke**: exit 0, peak RSS **1.62 GB**, 12 configs (depths 5/6/7 x 4 pairs),
  all FDR-DEAD, best near-miss koide_Q_lep rel_err 9.23e-6 (the same Koide 2/3 collapse), **0 real
  certified**. Log lines (jsonl + summary + header) flushed+fsynced each level.

## Per-level logging
`results_overnight_pairs/pair_search_<stamp>.{jsonl,summary.txt,header.json}` — one structured line
per (pair, depth): counter, both germ keys+laws, depth, n_targets, n_pairs, recipes, fdr_mult, best
hit {target, formula, rel_err, status, fdr_bits}, gate_A_surplus_bits (after full pair-mult
look-elsewhere), n_certified this config, certified_cumulative, elapsed, peak RSS. Flushed each line.

## Projected wall-clock & launch
- steady-state ~72 s/pair (3 depths); one-time depth build ~83 s.
- **projected FULL PASS (351 pairs) ≈ 7.0 h.**
- Single genuine forward pass; the deadline stops it mid-pass and finalizes cleanly — NO
  re-confirmation re-loop.

### Overnight launch command
```
cd /Users/carlzimmerman/new_physics/project_atomos
nohup python3 overnight_pair_search.py --hours 8 \
    > results_overnight_pairs/console.out 2>&1 &
```
(`--hours 8` comfortably covers the ~7 h pass; `--hours 13` for extra headroom. The pass stops
itself when complete — it does not burn remaining time.)
