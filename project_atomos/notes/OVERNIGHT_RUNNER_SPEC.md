# OVERNIGHT_RUNNER_SPEC — the run-a-day / surface-clues / readjust loop, ported from hali_flow

*Reverse-engineered from the four hali_flow autoresearch loops and distilled into the exact mechanics the Build phase
will implement as `project_atomos/engine/overnight.py`. Read-only sources:*
- `~/new_physics/hali_flow/haliflow_8hr_cosmos.py` — **the primary template** (the cleanest run-N-hours loop:
  `RUN_HOURS`/`CHECKPOINT_INTERVAL`/`STAGNATION_THRESHOLD`, `KnowledgeBase`, `StrategyEvolver`, radical mutation,
  per-checkpoint logging, seeding from prior runs).
- `~/new_physics/hali_flow/autonomous_discovery_engine.py` — the **phase machine** (EXPLORATION→CONVERGENCE→ADVERSARIAL→
  SYNTHESIS→…), `NoveltyTracker.detect_convergence`, `_escape_stuck_state` (shuffle approaches, reset tracker, add new
  approaches), periodic `_save_state`.
- `~/new_physics/hali_flow/autonomous_law_discovery.py` — the **accumulate-knowledge / analyze-failure / improve** spine
  (`MethodologyKnowledge`, best-so-far, "learn from the last N failures", `SUCCESS.json` checkpoint on a hit).
- `~/new_physics/hali_flow/continuous_discovery.py` — the **cycle-through-strategies** wrapper (round-robin engines,
  collect-best, consolidated checkpoint, run-forever-or-N-hours).

**The one porting rule (the whole project's thesis).** hali_flow ranked candidates by **R²/closeness to data**. That is
exactly the move that produces FDR-dead numerology. project_atomos keeps every hali_flow *control* mechanic (timed loop,
knowledge accumulation, stagnation→radical-mutation, checkpointing, clue surfacing) but **replaces the fitness function
with the 3-part gate** (`gate/verdict.py`: FDR-survival ∧ forced-kernel ∧ interlock). Closeness from `engine/search.py`
(`Candidate.score`/`rel_error`) is **advisory ranking only** — it decides *what to hand the gate*, never *what counts as
a discovery*. Same bar both ways: the loop is built so a long night of effort yields **FDR-DEAD, honestly** if the SM
sector is kernel-free, and only promotes a LEAD when all three gates pass.

---

## 1. The run-for-N-hours main loop + checkpoint interval

**Config block** (ported verbatim in spirit from `haliflow_8hr_cosmos.py` lines 37–40):
```
RUN_HOURS            = 18          # default overnight; --hours overrides (continuous_discovery's --hours/--fast)
CHECKPOINT_INTERVAL  = 200         # gate-evaluations between checkpoint writes + strategy-evolve calls
STAGNATION_THRESHOLD = 1500        # gate-evals with no new best-bits before RADICAL MUTATION fires
KNOWLEDGE_DB         = results/knowledge.json          # accumulated tried-set + best-so-far (survives restarts)
LEAD_LEDGER          = results/leads.jsonl             # certified LEADS (all 3 gates pass)  — the "SUCCESS.json" analog
DEAD_LEDGER          = results/fdr_dead.jsonl          # honest FDR-dead ledger with each candidate's TELL
CLUES_FILE           = results/CLUES.md                # human-facing surfaced clues, rewritten each checkpoint
CHECKPOINT_FILE      = results/checkpoint.json         # full resumable state (for kill/restart mid-night)
```

**Loop skeleton** (merges `haliflow_8hr_cosmos.run_discovery` timing + `autonomous_discovery_engine.run` phase dispatch):
```
start = time.time();  end = start + RUN_HOURS*3600
load_checkpoint_if_exists()        # resume tried-set, best-bits, phase, strategy state
seed_from_prior_runs()             # §2: pull prior candidates.jsonl / leads.jsonl as warm-start building blocks
n_eval = 0
while time.time() < end:
    target  = scheduler.next_target()           # which SM constant to attack this step (§3 promising-target weighting)
    cand    = strategy.propose(target)           # an engine.Candidate via the CURRENT strategy (enumerate / mutate / combine)
    verdict = gate.evaluate(cand)                # the 3-part gate — THE fitness function (replaces R²)
    knowledge.record(target, cand, verdict)      # §2 accumulate: tried-set, near-miss, best-bits, per-target stats
    if verdict.is_lead:      ledger_lead(cand, verdict)         # §1 the "SUCCESS" event — but loop CONTINUES (multi-target)
    else:                    ledger_dead(cand, verdict.tell)    # honest dead-ledger with the TELL
    n_eval += 1
    if n_eval % CHECKPOINT_INTERVAL == 0:
        strategy = evolver.evolve(knowledge)     # §3 gradual strategy adaptation
        if knowledge.stagnant(STAGNATION_THRESHOLD):
            evolver.radical_mutation(); knowledge.reset_stagnation()   # §3 dead-end → readjust
        surface_clues(knowledge)                 # §4 rewrite CLUES.md
        save_checkpoint(); gc.collect()          # §1 resumable + memory hygiene (haliflow gc.collect per checkpoint)
finalize_report(knowledge)                       # §4 end-of-run summary: leads, top near-misses, target ledger
```
Key differences from hali_flow worth stating: (a) **the loop does NOT stop on first success** — unlike
`autonomous_law_discovery` (single hidden formula → return on hit), project_atomos has *many* SM targets, so a LEAD is
logged and the run continues to keep probing the rest (the `continuous_discovery` "run all engines, collect best"
posture). (b) **Checkpointing is by gate-eval count, not wall clock**, matching `haliflow`'s `% CHECKPOINT_INTERVAL`.
(c) The loop is **deterministic-seedable** (numpy default_rng with a logged seed) so a surfaced clue can be reproduced.

---

## 2. How it ACCUMULATES knowledge (tried-set / best-so-far / discovery DB)

Ported from `haliflow_8hr_cosmos.KnowledgeBase` + `autonomous_law_discovery.MethodologyKnowledge`, generalized to the
gate. A single `Knowledge` object, persisted to `knowledge.json` every checkpoint:

- **`seen_canonical: set[str]`** — the tried-set. Keyed by `ExprNode.canonical_hash()` (already computed by the engine;
  `G*c` ≡ `c*G`). A candidate whose canonical hash is in the set is **skipped before any gate work** — this is the
  `seen_hashes` dedup from `search.Grammar` lifted to the *cross-checkpoint, cross-strategy* level so the overnight run
  never re-pays for a tree it already judged. This is the literal "accumulate what's tried" Carl asked for.
- **`best_bits_per_target: dict[target → float]`** — best-so-far, but the figure of merit is **gate bits**
  (`fdr_bits` from `gate/fdr.py`), NOT R². Replaces `KnowledgeBase.best_r2_history`. `best_bits` overall drives
  stagnation (§3).
- **`near_misses: list[NearMiss]`** — candidates that *passed Gate A* (survived FDR) but failed B or C, sorted by bits,
  capped at top-100 (the `successful_patterns[:100]` cap in `KnowledgeBase.add_success`). These are the genuinely
  interesting clues — close + statistically surprising but not yet interlocking. Each stores
  `{target, formula, fdr_bits, gate_failed, tell, n_distinct_leaves}`.
- **`building_block_scores: dict[symbol/op → float]`** — `KnowledgeBase.operator_scores` generalized: every time a
  candidate clears Gate A, credit the **leaves, germs, group-invariants, and ops it used** with its `fdr_bits`. This is
  how the loop learns *which constants/structures keep showing up in surprising relations* (e.g. if `kernel=√(8π/3)` or
  the `S4` Casimir keeps appearing in Gate-A survivors, its score climbs and the evolver biases toward it). Recurring
  building blocks = a first-class surfaced clue (§4).
- **`per_target_stats: dict[target → {n_tried, n_passed_A, best_bits, gate_wall}]`** — which targets look promising
  (high best-bits / high Gate-A pass-rate) vs. which are walls (many tried, 0 surprising). Drives the target scheduler
  (§3) and the "promising targets" clue (§4). `gate_wall` records *which gate* most candidates die at per target (the
  honest-prior expectation: most SM mass targets die at Gate B "no forced kernel").
- **`fdr_dead`** is NOT held in memory — it streams straight to `fdr_dead.jsonl` (the dead-ledger), so memory stays
  bounded over an 18-hour run (`haliflow` caps `failed_patterns` at 200 in RAM; we keep 0 and stream).
- **Discovery DB = `leads.jsonl`** — every candidate that passes all three gates, with its full `Verdict`
  (bits, forced-factors, interlock mode, cross-sector result). The `autonomous_law_discovery.SUCCESS.json` analog, but
  append-only because there can be several.

**Seeding / warm-start** (`haliflow_8hr_cosmos` lines 658–674, the "seed with best equations from previous runs"). On
startup the runner reads any prior `candidates.jsonl` / `leads.jsonl` / `near_misses` and loads their formulas as
**combination building blocks** for the `combine`-strategy (§3), so successive nights compound instead of restarting
cold. The tried-set (`seen_canonical`) is also reloaded so a restart never re-judges old trees.

---

## 3. Stagnation detection + RADICAL MUTATION / strategy shift

**Three generation strategies, mixed per-step** (the `haliflow_8hr_cosmos` 50/25/25 split, lines 692–720, retargeted
from curve-fitting templates to gate candidates):
- **`enumerate` (≈50%)** — pull the next dedup'd tree from `engine.Search`/`Grammar` under the current alphabet,
  `max_depth`, and **hard filter** (`dimension|rep|interlock|none`). The systematic exhaustive backbone (this is the
  machine that actually found a₀).
- **`combine` (≈25%)** — take two high-bits survivors from the knowledge DB and combine them
  (`RandomEquationGenerator2Var.combine_successful` analog: product / ratio / quadrature / sum), spending the
  dimensionless freedom on tying *more* measured leaves (pushing toward the interlock filter's Koide signature).
- **`mutate` (≈25%)** — `StrategyEvolver._mutate`: wrap a survivor in a high-scoring op, swap a leaf for a transformed
  leaf, or add/remove a germ factor. Biased by `building_block_scores`.

**`StrategyEvolver` state** (ported from `haliflow`): `complexity_bias`, `mutation_rate`, the per-checkpoint
`evolve(knowledge)` that *gradually* nudges these — raise `mutation_rate` when best-bits flat, lower it when improving,
bias `complexity_bias` toward the depth of recent Gate-A survivors.

**Stagnation detector** (the load-bearing readjust trigger, merging `KnowledgeBase.check_stagnation` +
`NoveltyTracker.detect_convergence`):
- Append current overall `best_bits` to a rolling history each checkpoint. **Stagnant** iff over the last
  `STAGNATION_THRESHOLD` gate-evals (a) `max(best_bits) − min(best_bits) < ε` (no bit improvement, `check_stagnation`),
  **AND** (b) the **novelty rate collapses** — the fraction of newly-enumerated trees whose `canonical_hash` is already
  in `seen_canonical` exceeds ~0.95 (the current alphabet×depth is *exhausted*; `detect_convergence`'s "we keep
  re-seeing the same structures").

**RADICAL MUTATION menu** (fired on stagnation — `_escape_stuck_state` + `_radical_mutation`, generalized to the gate's
real levers; the runner picks the next unused escalation):
1. **Deepen / re-scope the alphabet** — bump `max_depth` (4→5), or swap the active alphabet sub-pool: turn ON a discrete
   flavor group's invariants (`A4 → S4 → Δ(27) → Spin8-triality`), add √-ratios, widen the exponent set. This is the
   single highest-leverage knob — exactly the `symbolic_search → constrained_search` "curate the constants" move that
   unlocked a₀ (ENGINE_RE §1a/§2.2). The alphabet edit *is* the physics input.
2. **Switch the hard filter** — `interlock → rep → dimension` (or relax `min_interlock` 3→2). Changes which structural
   cut spends the dimensionless freedom; e.g. flip to `rep` to chase symmetry-multiplet relations the `interlock` filter
   was hiding.
3. **Re-weight the target scheduler** — abandon a wall target (`gate_wall` dominated, 0 surprising hits after many
   tries) and pour evals into the highest best-bits / highest Gate-A-pass-rate target (`per_target_stats`).
4. **Randomize the strategy mix + mutation params** (`_radical_mutation`: `complexity_bias`, `mutation_rate`,
   `crossover_rate` resampled) and **reset the convergence/novelty tracker** so a fresh sub-region is explored.
The escalations are tried in order; if all are exhausted with no new best-bits, the runner writes a
`STAGNATION: alphabet/filter space exhausted for target T` clue (§4) — the honest "this sector looks kernel-free" signal,
the dead-end report Carl wants surfaced rather than hidden.

---

## 4. How it SURFACES CLUES to a human

Rewritten to `results/CLUES.md` every checkpoint (so it can be read live mid-night), plus a final `finalize_report`.
Sections (this is the "best candidates / near-misses / recurring building blocks / which targets look promising" the
brief enumerates):
- **CERTIFIED LEADS** — anything in `leads.jsonl`: formula, target, n-σ agreement, `fdr_bits`, forced factors with their
  registry provenance, interlock mode + cross-sector result. The headline. (Expected to be empty or Koide-class — that
  is fine and honest.)
- **TOP NEAR-MISSES** — the `near_misses` top-N: Gate-A survivors (statistically surprising, within measurement error)
  that failed B or C, each with the **TELL** (`"factor has no pre-fit provenance"`, `"≥2 free numbers"`,
  `"one-number re-description"`, `"cross-sector kill"`). These are the leads-in-waiting and the most actionable clue.
- **RECURRING BUILDING BLOCKS** — top entries of `building_block_scores`: which constants / germs / group-invariants /
  ops keep appearing in Gate-A survivors (e.g. "S4 Casimir appears in 23 of the top-50 surprising lepton-ratio
  relations"). A recurring forced-coefficient candidate is the strongest hint at where a real kernel might live.
- **PROMISING vs. WALL TARGETS** — `per_target_stats` sorted: best-bits and Gate-A pass-rate per SM target, plus the
  `gate_wall` (which gate kills most candidates) — so a human sees at a glance "PMNS θ₁₂ has 3 Gate-A survivors,
  promising; charged-lepton mass ratios are a Gate-B wall (no forced kernel), as the honest prior predicted."
- **n-σ / SURPLUS-BITS, ALWAYS** (Carl's emphasis (a)). Every surfaced number is reported **relative to the measurement
  uncertainty**: a candidate's headline figure is its **n-σ agreement** with the PDG value and its **surplus bits over
  chance** (`gate/fdr.py`), never a bare digit count. A 6-digit match to a 2-digit-known constant is explicitly demoted
  (the tolerance in `SearchSpace.tol`/`Search.tol` is the measurement error, so "within the error bar" is the bar).
- **STAGNATION / READJUST LOG** — a timestamped trace of every radical-mutation event and what it changed (alphabet
  deepened, filter switched, target abandoned), so the human can see the machine's autonomous course-corrections and the
  honest dead-ends.

Logging cadence and format follow `haliflow.ResultLogger`: a `progress.log` line per checkpoint
(`Gen N | M evaluated | K leads | best_bits=… | near_misses=… | Xh left`) printed and appended, `stats.json` saved each
checkpoint, `CLUES.md` rewritten each checkpoint.

---

## 5. Plausibility / physical-sense checks

Three layers; the engine's cheap structural cut + the gate's statistical-physical bar replace hali_flow's R²/shuffle
sanity tests:
- **Engine-level (free, pre-gate)** — the **hard structural filter** in `Search._passes_filter`
  (`dimension|rep|interlock`) is the analog of `is_acceleration()` and of `PlausibilityChecker.check`
  (finite / bounded / dimensionally-sane): a tree that doesn't match the target dimension, carries a poisoned rep tag,
  or fails to tie `min_interlock` distinct measured leaves is dropped before any gate work. The runner also reuses
  `_finite_pos` (reject non-finite, ≤0) — the `finite`/`bounded` checks from `PlausibilityChecker`.
- **Gate-level (the real plausibility judgment)** — `gate/forced_kernel.py` enforces that each coefficient factor is
  **traceable to a named, pre-registered physical constraint** in `gate/registry.py` (a field-equation normalization, a
  representation dimension, a group Casimir, a root-system angle) **declared before seeing the target**. A factor with no
  registry provenance is a free fit parameter, not forced. This is the principled successor to `HRMValidator`'s
  "does it derive from a fundamental principle?" — but mechanized and anti-circular (the candidate can only *point* at a
  registry key; the gate re-checks it). The `≤1 free O(1)` count is the hard plausibility cut that kills "needs 2 free
  numbers" derivations (the Koide-via-dS-Unruh failure mode).
- **Anti-numerology guardrails (the discipline layer)** — small-denominator-rational targets are flagged
  (`SearchSpace.rational_target`) and routed to the structural-null, because a rational is re-described for free
  (Gate-A-on-value is uninformative for 2/3); the look-elsewhere multiplicity (`n_targets_searched` = number of SM
  targets the night swept) is folded into the bit budget so a hit must beat the *corrected* threshold; and the
  cross-sector falsification (`Interlock.cross_sector`) is mandatory for any relation claimed family-universal. These
  are the ports of hali_flow's shuffle-test / convergence-sanity, upgraded to the FDR discipline that distinguishes a₀
  from the 164 dead re-labelings.

---

## Summary of the loop design the Build phase will implement

`engine/overnight.py` is a timed (`RUN_HOURS`, default 18, `--hours` override), checkpoint-by-gate-eval-count
(`CHECKPOINT_INTERVAL`) loop ported from `haliflow_8hr_cosmos.run_discovery` but with the **3-part gate
(`gate/verdict.py`: FDR-survival ∧ forced-kernel ∧ interlock) as its fitness function in place of R²** — engine
closeness is advisory-only, deciding what to hand the gate, never what counts as a discovery. Each step a target
scheduler picks an SM constant, one of three strategies (≈50% exhaustive `enumerate` from the dedup'd dimensional/rep/
interlock-filtered `Grammar`, ≈25% `combine` two high-bits survivors, ≈25% `mutate`) proposes a `Candidate`, the gate
judges it, and a persistent `Knowledge` object accumulates the cross-checkpoint tried-set (`seen_canonical` hashes),
best-**bits**-per-target, capped top-N near-misses, recurring `building_block_scores`, and per-target gate-wall stats —
streaming all FDR-dead candidates to an honest ledger and all triple-pass LEADS to a discovery DB. A stagnation detector
(no best-bits gain over `STAGNATION_THRESHOLD` evals **and** the novelty rate collapsing as the current alphabet×depth
exhausts) fires an ordered **radical-mutation** escalation — deepen/re-scope the alphabet (toggle A4→S4→Δ(27)→triality
invariants, the highest-leverage "curate the constants" lever that unlocked a₀), switch the hard filter, re-weight the
target scheduler off wall targets, then randomize the strategy mix and reset the novelty tracker — and when those are
exhausted it writes an honest "sector looks kernel-free" stagnation clue. Every checkpoint it rewrites a human-facing
`CLUES.md` surfacing certified leads, top near-misses with their failing-gate TELL, recurring building blocks, and
promising-vs-wall targets, **always scored in n-σ agreement and surplus bits relative to the measurement uncertainty**
(Carl's precision emphasis), and saves a resumable checkpoint so successive nights compound via warm-start seeding. The
whole design is built to report **FDR-DEAD honestly** if the SM sector is kernel-free and to promote a **LEAD** only when
all three gates pass — same bar both ways, never manufacturing a hit.
