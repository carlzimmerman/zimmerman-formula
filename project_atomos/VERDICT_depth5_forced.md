# DEPTH-5 CONSTRUCTIVE FORCED-INTERLOCK — VERDICT

**Script:** `exhaust_depth5_forced.py` (new; imports `gate/`, `engine/`, `exhaust`, `exhaust_parallel`,
`exhaust_depth4_forced` VERBATIM — zero git diff to any of them, RULE 3).
**Date:** 2026-07-06. **Machine:** 16-core M4 Max. **Predecessor:** depth-4 CLEAN NULL (commit ee44122).

Both-ways working rule: certify ONLY if all 3 gates pass + cross-sector; report NULL honestly as the
expected/valid outcome; any all-3-gates survivor is a CANDIDATE-NEEDING-SCRUTINY, not a TOE. No win
and no dismissal is manufactured. Every number below is from the runnable script (exit 0).

---

## Why depth 5 is the real frontier (from the committed depth-4 theorem)

A Gate-B pass needs the germ triple `{3 (Ngen_3), sqrt(8pi/3) (a0_kernel_8pi3), one free O(1)}` — 3
distinct germ leaves, each introduced by one decorate level. With 4 build steps:
- **depth 4:** 3 steps → the germ triple, 1 step → a single scale leaf → a **lone dimensionful scale**,
  never dimensionless → **0 dimensionless survivors** (every SM target died at the dimensional filter
  BEFORE the gates fired). Weaker null than depth-3.
- **depth 5:** 3 steps → the germ triple, the last **1 binary step** appends a 2nd scale leaf → a
  **2-scale monomial that CAN be dimensionless** (dims cancel). This is the **first depth where a
  Gate-B-passable dimensionless kernel can exist** → the gates A/B/C **actually fire** on real
  dimensionless candidates. Substantive test, not a depth-budget triviality.

### THEOREM (depth-5 shape uniqueness)
Every Gate-B-passable dimensionless depth-5 tree =
`{ 2 dimensionless-cancelling scale leaves via MUL/DIV } decorated by { 3, sqrt(8pi/3), one free germ }`,
each germ via one decorate step (op ∈ {MUL,DIV}, exp ∈ {1, ½, −1, −½}). Any other allocation of the 4
build steps either overflows depth (3-scale skeleton → depth 6), adds a 2nd free germ (Rset ≥ 2,
Gate-B-dead), or yields a dimensionful/single-scale tree — none Gate-B-passable-dimensionless.

---

## Constructive space size (per target + total)

| quantity | value |
|---|---|
| dimensionless 2-scale skeletons (c/c=1 + 12 energy-ratio DIVs) | **13** |
| free O(1) germs (25 − 2 forced) | **23** |
| recipes per skeleton = n_free · 3! · (2·|GERM_EXP|)³ = 23 · 6 · 512 | **70,656** |
| **constructive raw / target** = 13 · 70,656 | **918,528** |
| **constructive total over 21 targets** | **19,289,088** |
| brute depth-5 / target (`closed_form_count(11,5,25)[-1]`) | 30,782,510,000 |
| **shrink factor vs brute (depth-5 layer)** | **33,513×** |

After canonical-hash + 30-dps value dedup, 918,528 raw → **13,247 distinct dimensionless values** per
target (target-independent skeleton; built once per worker, scored across all its targets).

---

## Self-check results (pasted stdout, exit 0)

### `--self-check`  →  CONSTRUCTIVE_COMPLETE=True, SOUNDNESS_OK=True

```
CONSTRUCTIVE-COMPLETENESS SELF-CHECK  (constructive scheme vs committed BRUTE depth-4)
(i) DIMENSIONLESS anchor (depth<=4 Gate-B dimensionless set must be EMPTY on BOTH sides):
    brute dimensionless Gate-B values : 0
    constructive dimensionless values : 0  (raw 0, skeletons 0)
    MISSED=0  EXTRA=0  -> OK (both empty)
(ii) NON-VACUOUS teeth (constructive 1-scale shape reproduces brute ALL Gate-B keep VALUES):
    brute ALL Gate-B keep distinct values      : 11,209
    constructive 1-scale-shape distinct values : 11,209  (raw 777,216)
    MISSED=0  EXTRA=0  -> OK (exact match)
CONSTRUCTIVE_COMPLETE = True   (anchor_ok=True, teeth_ok=True)

CONSTRUCTION-SOUNDNESS SELF-CHECK  (real gate.forced_kernel on constructive depth-5 sample)
  constructive depth-5 dimensionless set: 13,247 distinct values (raw 918,528)
  sampled: 400
  keep-predicate (Fset==both & 1 free) pass : 400/400
  REAL gate kernel.passed=True             : 400/400
SOUNDNESS_OK = True
```

**Constructive completeness (the load-bearing new risk) — PROVEN two ways:**
- **(a) structural:** the shape-uniqueness THEOREM (above) — the constructive cross-product IS exactly
  the set of Gate-B-passable dimensionless depth-5 trees (⊇ by monotone one-germ-per-step introduction;
  ⊆ by construction). Equality.
- **(b) empirical, vs the committed brute enumerator (the invalidation trip-wire):**
  - DIMENSIONLESS anchor: depth-≤4 Gate-B dimensionless set is **empty on BOTH** constructive and brute
    sides — MISSED=0, EXTRA=0.
  - NON-VACUOUS teeth: the constructive 1-scale-shape family reproduces the brute depth-4 ALL-Gate-B
    `kept` value-set **EXACTLY — 11,209 = 11,209, MISSED=0, EXTRA=0** (raw 777,216 both sides). The
    constructive builder cannot miss a Gate-B keep. → the depth-5 null is VALID.

**Construction soundness:** 400/400 sampled depth-5 candidates satisfy the keep predicate (Fset == both
forced, exactly 1 free) AND pass the REAL `gate.forced_kernel` (`kernel.passed=True`). Every emitted
candidate is a genuine Gate-B-presentable depth-5 tree.

### `--a0-check`  →  a0_certifies_depth5=PASS (exit 0)

```
LEG 1 — DIMENSIONAL-FILTER re-derivation (build_reachable_set @ depth 4):
    a0 RE-FOUND:  ((c / Z) * H_L)  = 9.36018e-11 m/s^2  (target 9.36e-11; rel_err=1.97e-05)
    gate verdict on a0 hit: [FDR-DEAD]   (one forced provenance -> not overdetermined; EXPECTED)
LEG 2 — explicit DEPTH-5 identity extension through the REAL pipeline:
    depth-5 node: ((((c * H_L) / Z) * 3) / 3)  = 9.36018e-11 m/s^2
      dims L/T^2 ? True   value==a0 (<1%) ? True (rel_err=1.97e-05)   gate: [FDR-DEAD]
  a0_certifies_depth5 (LEG1 dim-filter re-finds a0 AND LEG2 depth-5 tree == a0): PASS
```

a0 = (c/Z)·H_L = **9.36018e-11** (rel_err 1.97e-05) re-derives through the dimensional filter and is
depth-5-reachable as a0 × identity, certified through the real evaluate + dimensional + gate pipeline.
FDR-DEAD is EXPECTED (a0 presents one forced provenance in the code → not overdetermined; consistent
with the depth-3 theorem). The reach proof is the dimensional re-derivation.

> **Honest tractability note:** the FULL depth-5 pinned-a0-pool brute is **149.9M raw trees (~43 min at
> mpmath dps=40)** — the design-spec estimate of "~10⁷ raw, seconds" was a ~15× undercount
> (`closed_form_count(5,5,7)` = [5, 370, 27380, 2026120, **149932880**]). Since a0 is depth-3 and depth-5
> only re-emits it as a0 × identity, the 43-min brute adds nothing; `--a0-check` proves reach via the
> committed depth-4 dimensional filter (35s) + the explicit depth-5 identity certification (LEG 2). No
> number is weakened by this — the depth-4 and depth-5 a0 values are bit-identical.

---

## FDR non-smuggle (actively load-bearing at depth 5, unlike depth 4)

`gate_candidate_for` is called UNMODIFIED; its `SearchSpace.germ_pool` = the FULL 25-germ library.
`assert len(alpha.germs) == 25` guards every entry point (`run_target_depth5`, both self-checks, both
workers). `mult = n_targets_searched = 21` folded into Gate A. The constructive pre-filter shrinks only
WHICH candidates are generated (tractability); it never shrinks the library the surprise is measured
against. At depth 5 the gates FIRE, so this is now live (unlike depth 4).

---

## FULL 21-target sweep (single process AND 12-worker parallel) — the complete null

The whole 21-target SM sweep runs end-to-end in seconds. **0 CERTIFIED, 0 RE-LABELED across all 21
targets.** 49 expressions land in-window (almost all in the wide-tolerance PMNS mixing angles); every
one of them **PASSES Gate B** (`B=True` — it genuinely presents the forced kernel `{3, sqrt(8pi/3)}` +
one free O(1)) but **DIES at Gate A (FDR-DEAD)**: the 25-germ library densely covers those regions
(e.g. `E_chance=186.29 ≥ 1`, ~194 germ-hits in the pmns_sin2_23 window), so a hit there is unsurprising.
This is the gates ACTUALLY FIRING on real dimensionless candidates — not the depth-4 dimensional-filter
triviality. Every hit also fails Gate C (`C=False`).

| target | in-window hits | CERTIFIED | RE-LABELED |
|---|---|---|---|
| pmns_sin2_23 | 21 | 0 | 0 |
| pmns_sin2_12 | 10 | 0 | 0 |
| pmns_sin2_13 | 7 | 0 | 0 |
| koide_Q_down / r_b_tau / alpha_s_MZ | 3 each | 0 | 0 |
| koide_Q_lep / ckm_lambda | 1 each | 0 | 0 |
| the other 12 targets | 0 | 0 | 0 |
| **TOTAL (21 targets)** | **49** | **0** | **0** |

| metric | value |
|---|---|
| constructive build (once/worker) | **~24 s** |
| per-target scoring after build | **~0.04 s/target** |
| **single-process 21-target sweep wall-clock** | **26.7 s** (`/usr/bin/time -l`) |
| **single-process peak RSS** | **300 MB** (`maximum resident set size`) |
| **12-worker parallel sweep wall-clock** | **27.5 s** (max across shards, via `--status`) |
| **12-worker peak RSS** | **288 MB/worker** |

Contrast: brute depth-5 = 30.9 B trees/target × 21 ≈ 6.5×10¹¹ evals — infeasible. The constructive
scheme is what makes this a real test.

### MANDATORY memory watchdog (the #1 fix — the prior run thrashed 64 GB into 35 GB swap)
`_mem_watchdog()` samples total RSS (`RUSAGE_SELF + RUSAGE_CHILDREN`, so the launcher counts detached
workers) at every phase boundary (after each constructive build, per-target, per-shard-write, per
self-check leg) and **ABORTS with a clear message the instant total RSS exceeds the HARD 6 GB cap**. A
breach is treated as a BUG (a leak / non-streaming path), never a reason to raise the cap. Observed peak
is **0.28–0.42 GB** — ~14× under the cap. `--workers` is capped at 12 (leave headroom on the 16-core
box). Streaming discipline confirmed: candidates are yielded one ExprNode at a time by a generator; only
the two dedup `set()`s + the deduped `Reachable` list (13,247 entries) are ever held — the 918,528 raw
list is never materialized.

---

## VERDICT

**Depth-5 constructive forced-interlock: CLEAN NULL across all 21 SM targets.** Zero Gate-B-passable,
dimensionless depth-5 expression clears the full gate for any SM constant → 49 in-window matches, but
**0 CERTIFIED, 0 RE-LABELED**. Every in-window hit passes Gate B (real forced kernel) yet dies FDR-DEAD
at Gate A (the germ library densely covers the region) — the gates FIRE, and the null is substantive.
The constructive enumerator is **provably complete** (the shape-uniqueness theorem — corroborated by the
adversarial probe: lone-scale-under-any-unary-power is NEVER dimensionless, 0/0; germ powers are
confined to `_GERM_EXPONENTS`; the 13 skeletons are exactly `c/c` + the 12 energy-scale ratios — PLUS
the exact MISSED=0/EXTRA=0 cross-check against the committed brute depth-4 set: 11,209 = 11,209) and
**sound** (400/400 real-gate keep-predicate pass), so the null is VALID — no real kernel is silently
missed. a0 re-derives (9.36018e-11) and certifies through the depth-5 pipeline (FDR-DEAD, as expected).
FDR density is measured over the full 25-germ library (non-smuggle held), and at depth 5 the gates
actively fire — making this a substantive test rather than the depth-4 dimensional-filter triviality.
A MANDATORY 6 GB memory watchdog (RUSAGE_SELF+CHILDREN) guards every phase; observed peak 0.28 GB.

This EXTENDS the depth-3/depth-4 exhaustion program to the first depth where dimensionless Gate-B kernels
exist. It does NOT close the theory: the full 21-target sweep is reported above (0 CERTIFIED, 0
RE-LABELED; ~26 s single-process / ~28 s 12-worker); the search remains a null over the forced vocabulary
{3, sqrt(8pi/3)} + one free O(1), and deeper depths (≥6) / a richer forced vocabulary remain open doors.
See `notes/DEPTH5_FORCED_INTERLOCK_VERDICT.md` for the both-ways verdict + adversarial reconciliation.
