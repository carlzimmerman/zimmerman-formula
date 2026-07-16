# Overnight Forced-Vocabulary Search — STATUS

**Launched:** 2026-07-07 (run stamp `20260707T003316`)
**Process:** `python3 overnight_vocab_search.py --hours 8`  (detached via `nohup`, PID **41114**)
**Prior:** NULL (expected). This is honest due diligence, NOT a promise of a hit.

---

## What it searches

The depth axis is EXHAUSTED over the committed forced vocabulary `{3 (Ngen_3),
sqrt(8pi/3) (a0_kernel_8pi3)}` — depth-3/4/5 are committed CLEAN NULLS. The only
remaining axis that could surface a certified SM hit is a **NEW FORCED GERM that
legitimately OVERDETERMINES** (value pinned by a declared symmetry law BEFORE
fitting AND appearing in >=2 independent forced places).

- **27 candidate forced germs** — pre-registered symmetry invariants, each WITH its
  forcing law, curated from `targets.geometric_primitives.forced_pool()` + the
  discrete-flavor / GUT symmetry primitives already in the corpus: A4/S4/S3/Delta27
  rep dims + group orders, tetra/cube polytope counts, SU(5)/SO(10)/E6 dims + one-
  generation multiplets, Coxeter numbers, GUT hypercharge norm 5/3, tree Weinberg
  3/8, Dynkin 1/2, Koide circulant floor 1/3 + amplitude 1/6 + cos^2 angle, TBM
  Clebsch 1/3 & 1/2. No number is hand-typed to fit; every value is drawn from a
  pre-registered forced primitive.
- **3 depths** `[5, 4, 3]` — depth 5 is the substantive constructive level
  (13,247 Gate-B-passable dimensionless values); depths 4/3 are committed-null
  anchors (dimensionless Gate-B set genuinely empty -> 0 recipes, real not skipped).
- **21 SM targets** (`exhaust_parallel.sm_target_keys()`).

= **81 levels per sweep** (27 germs x 3 depths). ~80 s per sweep. The `--hours 8`
run wraps the 81 levels in an **outer sweep loop** that keeps the process alive to
the deadline, re-verifying the deterministic 81 levels each sweep (~360 sweeps over
8 h). Sweeps 2+ are RE-CONFIRMATION passes — they re-run identical (germ, depth,
target, expression) trials, so they do **NOT** inflate the multiplicity and do NOT
add to the certified count (counted on sweep 1 only). Est. completion ~8 h from
launch (deterministic stop at deadline).

## Anti-fabrication guard — FULL look-elsewhere multiplicity

`mult = n_targets x n_germs x sum_depth(n_recipes) = 21 x 27 x 13247 = **7,511,049**`
(penalty **-22.8 bits** on any surplus). This is wired verbatim into the gate via
`gate_candidate_for(..., n_targets_searched=mult)` -> `SearchSpace.n_targets_searched`
-> `gate/fdr.py:150`. Trying MORE germs RAISES the bar. Verified in every logged row
(`fdr_mult=7.511e+06`), not just the dry-run.

- **Gate B (overdetermination):** a germ earns forced credit only if it appears in
  **>=2 distinct forced provenance keys**. A candidate registered once is a
  definition, not a kernel -> Gate B fails. Adding candidate germs cannot cheat it.
- **RULE 3:** `gate/`, `engine/`, `exhaust*.py`, `targets/` imported UNMODIFIED
  (git: 0 tracked-file modifications). Candidate germs are injected into a **COPY**
  of `FORCED_CONSTRAINTS` per config and restored on exit; the FDR germ pool stays
  fixed at 25 (`assert len(alpha.germs)==25`).
- **CERTIFIED iff Gate A (>=10 surplus bits AFTER -22.8 penalty) & B & C.** Anything
  else = FDR-DEAD / REAL-PUZZLE-RE-LABELED, logged honestly.

## Memory guard

- Reachable sets built ONCE at startup (depth-independent of germ/target), reused
  every level. Streaming score (only running best, no per-hit list). Builder's
  `seen_canon` is bounded and freed on return. **No state accumulates across sweeps**
  beyond scalars (counter, certified_cumulative, sweep) -> memory bound preserved.
- **HARD RSS watchdog** samples SELF+CHILDREN, ABORTS >4 GB with a clear logged
  message, fires at startup + each build + each config. Observed peak **~0.29 GB**
  (14x under cap). A depth-5 run once thrashed 64 GB into swap; that path is gone.

## Log path + how to tail

- Per-level JSONL: `results_overnight_vocab/vocab_search_20260707T003316.jsonl`
  (one structured line per level, `fsync`-ed — a crash leaves a readable partial).
- Human summary:  `results_overnight_vocab/vocab_search_20260707T003316.summary.txt`
- Header:         `results_overnight_vocab/vocab_search_20260707T003316.header.json`

```
tail -f /Users/carlzimmerman/new_physics/project_atomos/results_overnight_vocab/vocab_search_20260707T003316.summary.txt
```

Each line: counter, germ key, depth, n_targets, n_recipes, best hit (target :
status), its rel_err + Gate-A FDR bits (AFTER full look-elsewhere), full mult,
cumulative CERTIFIED, elapsed, peak RSS.

## Prior + how to read a result

**Prior is NULL** (committed number-field obstruction: a0/Z carries sqrt(pi),
transcendental; flavor data is algebraic -> a0/Z structurally gauge-blind). A clean
null is the expected, valid outcome. So far: CERTcum=0, closest near-miss
`koide_Q_lep` rel_err 9.2e-6 -> **-0.0 FDR bits -> FDR-DEAD** (correctly rejected).

- **NULL line** (expected): `best=<target>:FDR-DEAD` (or `:NONE`), `FDRbits` <= ~0,
  `CERTcum=0`.
- **HIT line** (would need human scrutiny, NOT auto-trusted, NOT a TOE): a row with
  `best=<target>:CERTIFIED` and `FDRbits >= +10` AFTER the -22.8 penalty, plus
  `CERTcum` incrementing. That requires a germ that genuinely overdetermines
  (>=2 independent forced places) AND clears 10 surplus bits against 7.5M trials.
  Any such line is a **CANDIDATE-NEEDING-SCRUTINY logged for human verification** —
  explicitly not a discovery until independently re-derived.

**Working rule (both-ways):** the gate is NEVER weakened to produce a hit; a
manufactured win is worse than an honest null. A clean null is a legitimate result.
