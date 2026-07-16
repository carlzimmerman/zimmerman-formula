# project_atomos — STATUS: overnight FORCED-VOCABULARY search

*As of 2026-07-07. The honest continuation past the committed depth-3/4/5 forced-vocabulary NULLS.
Depth is EXHAUSTED over {3 (Ngen_3), sqrt(8pi/3) (a0_kernel_8pi3)}. The ONLY remaining axis to a
certified SM hit is a NEW FORCED GERM that legitimately OVERDETERMINES. This runner tests candidate
new forced germs (pre-registered symmetry invariants, each WITH a forcing law) across depths and all
21 SM targets, all night, gate-honest. The prior is NULL; a clean null is the expected outcome.*

## Files
- `overnight_vocab_search.py` — the runner (new; RULE-3 clean: gate/engine/exhaust* imported verbatim).
- `results_overnight_vocab/` — the log dir (jsonl per level + human-readable `.summary.txt` + header).
- Reuses `exhaust_depth5_forced.py`'s constructive, streaming, Gate-B-passable enumerator verbatim.

## What it does (verified this session)
- **27 candidate forced germs**, each `(key, value, law)` drawn from `geometric_primitives.forced_pool()`
  + `gate.registry`: A4/S4/S3/Delta27 orders + irrep dims + polytope counts; GUT dims (24/45/78,
  15/16/27), Weyl/Coxeter (5/12), 5/3 GUT norm, 3/8 tree-Weinberg, Dynkin 1/2; Koide circulant
  rationals (1/3, 1/6, 1/2); TBM Clebsch (1/3, 1/2). NO number hand-typed to fit — `--list-germs`.
- Each candidate is registered in a **COPY** of `FORCED_CONSTRAINTS` with its law (context manager,
  restores the real registry on exit). `_germ_provenance` then grants it forced credit — WITHOUT
  weakening any gate threshold (RULE 3).
- Per `(germ, depth)` level it scores the constructive depth-5 dimensionless Gate-B-passable set
  (13,247 distinct values) against all 21 targets through the **real 3-part gate**.

## The #1 anti-fabrication invariant — WIRED and verified
- **`mult = n_targets x n_germs x n_depths(recipes) = 21 x 27 x 13247 = 7.51e6`**, a **-22.8-bit**
  look-elsewhere penalty (vs the naive n_targets-only -4.4 bits). Threaded through
  `exhaust.gate_candidate_for(..., n_targets_searched=mult)` -> `SearchSpace.n_targets_searched` ->
  `gate/fdr.py:150 mult = max(1, s.n_targets_searched)`, which divides the chance probability.
  Trying MORE germs RAISES the certification bar. `--dry-run` prints it.

## Why candidate germs CANNOT cheat the gate (the honest core)
- **Gate B needs OVERDETERMINATION**: `_keep_completed` requires `len(Fset)==2` DISTINCT forced
  provenance keys in the tree. A germ registered ONCE supplies at most ONE forced key -> a definition,
  not a kernel. Adding candidates does not relax this.
- **Provenance collisions are the mechanism, not a bug**: several candidates share a VALUE with an
  already-forced germ (`A4_irrep3=3.0 -> Ngen_3`), so `_germ_provenance` returns the EXISTING key and
  the candidate adds NO new independent forced place. Confirmed live: `A4_irrep3` probes to `Ngen_3`.
- **FDR non-smuggle**: the germ POOL stays FIXED at 25 (`assert len(alpha.germs)==25`); the candidate
  enters as a per-config REGISTRY law, not a new pool member, so the FDR library is unchanged.

## Memory discipline (the depth-5 64-GB-thrash fix)
- **Streaming only**: the constructive enumerator holds bounded value-dedup sets; the runner keeps
  only a running BestHit per config (no materialized hit lists). The known `run_atomos.py`
  unbounded `seen_canonical` bug is AVOIDED by not using that scaffold — the lean path reuses the
  already-streamed depth-5 machinery.
- **HARD RSS watchdog < 4 GB** (`_mem_watchdog`, SELF+CHILDREN), called at startup, each depth build,
  and each config. Peak observed: **0.28 GB**. A breach aborts with a clear message (it is a bug, not
  a reason to raise the cap).

## Self-checks passing (this session)
- `exhaust_depth5_forced.py --self-check`: constructive completeness (MISSED=0 EXTRA=0 vs committed
  brute depth-4, 11,209 values) + soundness (400/400 real-gate keep) — peak 0.42 GB.
- Live single-config: gate fires (13,247 scored/target), **CERT=0 / clean null**, best hit
  `koide_Q_lep` rel_err 9.2e-6 scores **-0.0 FDR bits** after the -22.8-bit penalty. ~2.1s/config.

## Honest standing
- Prior NULL (number-field obstruction: a0/Z carries sqrt(pi) transcendental, flavor data algebraic
  -> a0/Z gauge-blind). Any CERTIFIED result is logged as a CANDIDATE-NEEDING-HUMAN-SCRUTINY,
  explicitly NOT a TOE. The gate is NEVER weakened to produce a hit; a fake hit is worse than a null.

## Launch
    python3 overnight_vocab_search.py --list-germs   # the 27 candidate germs + laws
    python3 overnight_vocab_search.py --dry-run      # print the FULL FDR multiplicity
    python3 overnight_vocab_search.py --hours 10     # the overnight run (logs per level to results_overnight_vocab/)
