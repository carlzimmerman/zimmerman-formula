# Depth-5 Constructive Forced-Interlock Search — Both-Ways Verdict

**Date:** 2026-07-06
**Script:** `exhaust_depth5_forced.py` (new; `gate/`, `engine/`, `exhaust.py`, `exhaust_parallel.py`,
`exhaust_depth4_forced.py` imported VERBATIM — RULE 3, zero git diff to any of them; HEAD still ee44122)
**Machine:** 16-core M4 Max, 64 GB.
**Predecessor:** depth-4 CLEAN NULL (commit ee44122; `notes/DEPTH4_FORCED_INTERLOCK_VERDICT.md`).
**Status:** **CLEAN NULL.** 0 CERTIFIED, 0 REAL-PUZZLE-RE-LABELED, 0 candidates-needing-scrutiny across
all 21 SM constants — and, unlike depth-4, the gates A/B/C **actually fired** on real dimensionless
candidates.

Both-ways working rule: certify ONLY if all 3 gates pass + cross-sector; report a NULL honestly as the
expected/valid outcome; any all-3-gates survivor is a CANDIDATE-NEEDING-SCRUTINY, not a TOE. No win and
no dismissal is manufactured. Every number below is from the runnable script (exit 0), independently
re-run for this verdict.

---

## 0. Reconciliation of the adversarial review (done before writing)

Two adversarial verifiers were run (`fdr-smuggle`, `fidelity`); both returned `verdict_holds=true`,
`numbers_reproduced=true`, `overclaim_found=false`, `underclaim_found=false`, `required_correction=None`.
I did **not** take that on trust. I re-ran every load-bearing check myself:

| check | my independent re-run | matches record? |
|---|---|---|
| RULE 3 zero-diff (`gate/ engine/ exhaust.py exhaust_parallel.py exhaust_depth4_forced.py`) | empty diff; HEAD `ee44122` | ✅ |
| constructive space size | 918,528 raw/tgt · 13 skeletons · 70,656 recipes; shrink 33,512.87× | ✅ |
| completeness anchor (depth-≤4 dimensionless Gate-B) | brute 0, constructive 0 → MISSED=0 EXTRA=0 | ✅ |
| completeness teeth (constructive 1-scale vs brute depth-4 ALL Gate-B) | 11,209 = 11,209 → MISSED=0 EXTRA=0 | ✅ |
| soundness (real `gate.forced_kernel` on depth-5 sample) | keep 400/400, kernel.passed 400/400 | ✅ |
| a0 re-derivation (LEG 1, dimensional filter @ depth 4) | `(c/Z)·H_L = 9.36018e-11`, rel_err 1.97e-05, FDR-DEAD | ✅ |
| a0 depth-5 identity (LEG 2, `((((c*H_L)/Z)*3)/3)`) | 9.36018e-11, dims L/T² True, ==a0 True, FDR-DEAD | ✅ |
| full 21-target sweep | 0 CERTIFIED, 0 RELABELED, 49 in-window hits, 48/48 displayed kernel.passed=True | ✅ |
| FDR library | 25 germs, mult=21 on all 21 targets | ✅ |
| single-process wall / RSS | 26.4 s, 300 MB max RSS, **0 swaps** (`/usr/bin/time -l`) | ✅ |

**One residual gap I closed independently** (the fidelity verifier's strongest objection): the
brute-≤4 cross-check only exercises the **1-scale** shape; the depth-5-*novel* **2-scale dimensionless
skeleton** layer is not covered by it (an end-to-end brute-depth-5 is infeasible, ~3×10¹⁰ trees). I ran
my own brute over all 11×11×2 leaf pairs and confirmed it yields **exactly the 13** dimensionless
skeletons the constructive scheme uses (0 missed / 0 extra), and that the **1-scale dimensionless set is
empty**. The 13 = `c/c` (=1) plus the 12 distinct energy-scale ratios (`E_H/E_dS`, `E_H/Lam_QCD`,
`E_H/v_EW`, …). The skeleton layer is now brute-confirmed complete, not merely theorem-asserted.

**Result of reconciliation: nothing to correct.** Every load-bearing number reproduced exit-0 on my own
runs. The CLEAN NULL is honest and stands. The verifiers' single disclosed caveat (the a0 LEG-2 tree
multiplies then divides by the same forced germ `3`, so a0 presents only ONE forced provenance → it is
correctly FDR-DEAD / not overdetermined, i.e. the depth-5 a0 reach is a degenerate `a0 × cancelling
identity`, not a novel depth-5 structure) is real, consistent with the depth-3 theorem, and does not
change the null.

---

## 1. Why depth 5 is the real frontier (from the committed depth-4 depth-budget theorem)

A Gate-B pass needs the germ triple `{3 (→Ngen_3), sqrt(8pi/3) (→a0_kernel_8pi3), one free O(1)}` — 3
distinct germ leaves, each introduced by exactly one decorate level. With 4 build steps:

- **depth 4:** 3 steps → the germ triple, 1 step → a single scale leaf → a **lone dimensionful scale**,
  never dimensionless → **0 dimensionless survivors**. Every SM target died at the *dimensional filter*
  **before** any gate fired — a weaker null than even depth-3, where the gates fired.
- **depth 5:** 3 steps → the germ triple, the last **1 binary step** appends a 2nd scale leaf → a
  **2-scale monomial that CAN be dimensionless** (the dims cancel). This is the **first depth at which a
  Gate-B-passable *dimensionless* kernel can exist** → the gates A/B/C **actually fire** on real
  dimensionless candidates. A substantive test, not a depth-budget triviality.

### THEOREM (depth-5 shape uniqueness)
Every Gate-B-passable dimensionless depth-5 tree is exactly
`{ 2 dimensionless-cancelling scale leaves via MUL/DIV } decorated by { 3, sqrt(8pi/3), one free germ }`,
each germ via one decorate step (op ∈ {MUL, DIV}, exp ∈ {1, ½, −1, −½} = `_GERM_EXPONENTS`).
Any other allocation of the 4 build steps either (i) overflows depth (a 3-scale skeleton needs 2 binary
steps + 3 germ decorates = depth 6), (ii) adds a 2nd free germ (Rset ≥ 2 → Gate-B-dead / not
overdetermined-with-one-free), or (iii) yields a dimensionful or single-scale tree. None is
Gate-B-passable-and-dimensionless. **⊇** holds by monotone one-germ-per-step introduction; **⊆** holds by
construction → **equality**.

---

## 2. The constructive method + closed-form size

Brute depth-5 = `closed_form_count(11,5,25)[-1]` = **30,782,510,000 trees/target** — infeasible even on
16 cores, and exactly what thrashed 64 GB into swap in the prior (killed) run. The shape-uniqueness
theorem lets us build the Gate-B-passable dimensionless set **constructively** (forced-kernel-coefficient
× dimensionless 2-scale ratio × ≤1 free), STREAMING each `ExprNode` through a generator and holding only
the deduped value-set — never materializing the raw list.

| quantity | value |
|---|---|
| dimensionless 2-scale skeletons (`c/c`=1 + 12 energy-ratio DIVs) | **13** |
| free O(1) germs (25 − 2 forced) | **23** |
| recipes per skeleton = n_free · 3! · (2·\|GERM_EXP\|)³ = 23 · 6 · 8³ | **70,656** |
| **constructive raw / target** = 13 · 70,656 | **918,528** |
| constructive total over 21 targets | 19,289,088 |
| brute depth-5 / target | 30,782,510,000 |
| **shrink factor vs brute (depth-5 layer)** | **33,513×** |
| after canonical-hash + 40-dps value dedup | **13,247 distinct dimensionless values / target** |

The 13,247-value set is target-independent (only the window + gate differ per target), so a worker builds
it once (~24 s) and scores it across all its targets (~0.04 s/target).

### Completeness proof — the load-bearing new risk, proven two ways

**(a) Structural:** the shape-uniqueness theorem above — the constructive cross-product IS exactly the set
of Gate-B-passable dimensionless depth-5 trees.

**(b) Empirical, vs the committed brute depth-4 enumerator (the invalidation trip-wire) + my own
skeleton brute:**
- **Dimensionless anchor:** depth-≤4 Gate-B dimensionless set is **empty on BOTH** constructive and brute
  sides → **MISSED=0, EXTRA=0**.
- **Non-vacuous teeth:** the constructive 1-scale-shape family reproduces the committed brute depth-4
  ALL-Gate-B `kept` value-set **EXACTLY — 11,209 = 11,209, MISSED=0, EXTRA=0** (raw 777,216 both sides).
  The constructive builder cannot miss a Gate-B keep.
- **Skeleton layer (the depth-5-novel part, closed in reconciliation §0):** an independent brute over all
  11×11×2 leaf pairs yields **exactly the 13** dimensionless skeletons (0 missed / 0 extra); the 1-scale
  dimensionless set is empty. The 2-scale novelty is brute-confirmed, not just theorem-asserted.

→ **CONSTRUCTIVE_COMPLETE = True** (anchor_ok, teeth_ok). The depth-5 null is VALID — no real kernel is
silently missed.

### Soundness
400/400 sampled depth-5 constructive candidates satisfy the keep predicate (Fset == both forced germs,
exactly 1 free) AND pass the REAL `gate.forced_kernel` (`kernel.passed=True`). Every emitted candidate is
a genuine Gate-B-presentable depth-5 tree — no non-Gate-B candidate is smuggled in.

---

## 3. a0-validity at depth 5 (RULE-2 reach proof, targeted — NOT brute)

a0 = (c/Z)·H_Λ is a **depth-3** quantity; at depth 5 it appears as `a0 × identity`. Two legs, both
through the UNMODIFIED evaluate + dimensional filter + gate:

- **LEG 1 — dimensional-filter re-derivation** (committed `build_reachable_set` @ depth 4 on the pinned
  a0 pool, 2,053,875 raw → 15,965 dim-valid L/T² → 315 distinct, ~34 s):
  **a0 RE-FOUND `((c/Z)*H_L) = 9.36018e-11 m/s²`** (target 9.36e-11; **rel_err 1.97e-05**, n_sigma 0.00).
  Gate verdict **[FDR-DEAD]** (E_chance=0 sparse, surplus 5.0 bits ×21 look-elsewhere → below 10-bit).
- **LEG 2 — explicit depth-5 identity** `((((c*H_L)/Z)*3)/3)` built as a genuine depth-5 `ExprNode`
  (c[1] → c·H_L[2] → /Z[3] → ·3[4] → /3[5]), pushed through the real pipeline:
  **= 9.36018e-11 m/s², dims L/T² True, value==a0 (<1%) True** (rel_err 1.97e-05), gate **[FDR-DEAD]**.

**a0_certifies_depth5 = PASS** (LEG-1 re-finds a0 AND LEG-2 depth-5 tree == a0). FDR-DEAD is **EXPECTED**
and correct: a0 presents ONE forced provenance in the code (the LEG-2 tree cancels `3` against `3`) → not
overdetermined, exactly consistent with the depth-3 theorem. The a0 reach-proof is a degenerate
`a0 × cancelling-identity` embedding, honestly disclosed, not a novel depth-5 structure.

**Honest tractability note (no number weakened):** the FULL depth-5 pinned-a0-pool brute is
`closed_form_count(11,5,7)[-1]` = **149,932,880 raw trees (~43 min at mpmath dps=40)**. Since a0 is
depth-3 and depth-5 only re-emits it as `a0 × identity` (which LEG 2 certifies directly, bit-identical to
the depth-4 value), the 43-min brute adds nothing and is correctly skipped. This is exactly the
brute-enumeration trap that killed the previous run; the targeted proof avoids it.

---

## 4. FDR non-smuggle (actively load-bearing at depth 5, unlike depth 4)

`gate_candidate_for` is called UNMODIFIED; its `SearchSpace.germ_pool` = the FULL **25-germ** library
(built from `build_alphabet(None,None)`, expanded by `build_value_set` into a ~64,881-value realistic
reachable library — the fdr-smuggle verifier hand-recomputed `E_chance=0.0824` for koide_Q_lep over that
library, matching the gate to the digit). `assert len(alpha.germs) == 25` guards every entry point
(`run_target_depth5`, both self-checks, both workers). `mult = n_targets_searched = 21` is folded into
Gate A on every target. The constructive pre-filter shrinks only WHICH candidates are generated
(tractability); it NEVER shrinks the library the surprise is measured against — no sparsification in
either direction. **At depth 5 the gates FIRE, so this constraint is now actively load-bearing** (unlike
depth-4, where every target died at the dimensional filter before Gate A).

---

## 5. The full 21-target result — the complete null (gates FIRED)

Single-process AND 12-worker parallel both give **0 CERTIFIED, 0 RE-LABELED across all 21 targets**. 49
expressions land in-window (almost all in the wide-tolerance PMNS mixing angles); **every one PASSES
Gate B** (`B=True` — it genuinely presents the forced kernel `{3, sqrt(8pi/3)}` + one free O(1)) and then
**DIES FDR-DEAD at Gate A**: the 25-germ library densely covers those regions, so a hit is unsurprising.
Every hit also fails Gate C (`C=False`, single sector). This is the gates ACTUALLY FIRING on real
dimensionless candidates — not the depth-4 dimensional-filter triviality.

| target | in-window hits | tightest rel_err | CERTIFIED | RE-LABELED |
|---|---|---|---|---|
| pmns_sin2_23 | 21 | 4.18e-03 | 0 | 0 |
| pmns_sin2_12 | 10 | 5.33e-03 | 0 | 0 |
| pmns_sin2_13 | 7 | 5.83e-03 | 0 | 0 |
| koide_Q_down | 3 | 1.23e-03 | 0 | 0 |
| r_b_tau | 3 | 5.59e-04 | 0 | 0 |
| alpha_s_MZ | 3 | 3.75e-03 | 0 | 0 |
| koide_Q_lep | 1 | **9.23e-06** | 0 | 0 |
| ckm_lambda | 1 | 2.69e-03 | 0 | 0 |
| the other 13 targets | 0 | — | 0 | 0 |
| **TOTAL (21 targets)** | **49** | — | **0** | **0** |

Status distribution over recorded hits: **48/48 FDR-DEAD** with `kernel_passed(Gate B)=True` (47 dense,
E_chance ≫ 1; 1 sparse-below-10-bit). The "48 vs 49" is only the `hits[:20]` display cap on the 21-hit
pmns_sin2_23 target — NOT a streaming/parallel candidate drop (single-process totals equal the 12-worker
totals; the constructive build is deterministic → identical 13,247-value set on every worker).

**The tightest hit of the whole sweep** — and the one worth naming — is `koide_Q_lep`:
`((((c/c)*(3)^-1/2)*sqrt(8pi/3))*(2pi)^-1/2) = 0.66666667`, i.e. **Q = 2/3** at **rel_err 9.2e-06**,
Gate B = True. It dies **FDR-DEAD sparse-below-threshold**: E_chance = 0.082 (< 1) but 190 hits
contribute surplus = −0.0 bits, below the 10-bit Gate-A threshold. The Koide 2/3 is *reproducible* by the
forced kernel but carries **no surprise** — the forced pool bakes it in. Honestly FDR-DEAD, not a survivor.

### Performance + the mandatory memory watchdog (the #1 fix)

| metric | value |
|---|---|
| constructive build (once/worker) | ~24 s |
| per-target scoring after build | ~0.04 s/target |
| **single-process 21-target sweep wall-clock** | **26.4 s** (`/usr/bin/time -l`) |
| **single-process peak RSS** | **300 MB** (0 swaps) |
| 12-worker parallel sweep wall-clock | ~28 s (max across shards) |
| 12-worker peak RSS | ~288 MB/worker |
| self-check peak RSS | 0.42 GB |

`_mem_watchdog()` samples total RSS (`RUSAGE_SELF + RUSAGE_CHILDREN`, so the launcher counts detached
workers) at every phase boundary and **ABORTS the instant total RSS exceeds the HARD 6 GB cap** — a
breach is treated as a BUG (leak / non-streaming path), never a reason to raise the cap. Observed peak
0.28–0.42 GB, ~14× under the cap, 0 swaps. `--workers` capped at 12 (headroom on the 16-core box).
Streaming confirmed: candidates are yielded one `ExprNode` at a time; only the two dedup `set()`s + the
deduped 13,247-entry `Reachable` list are ever held — the 918,528 raw list is never materialized.

---

## 6. VERDICT (both-ways)

**Depth-5 constructive forced-interlock: CLEAN NULL across all 21 SM targets.** Zero Gate-B-passable,
dimensionless depth-5 expression clears the full 3-part gate for any SM constant. 49 expressions land
in-window; **every one passes Gate B (the real forced kernel `{3, sqrt(8pi/3)}` + one free O(1))** and
then **dies FDR-DEAD at Gate A** (the germ library densely covers the region) — **the gates FIRE**, so
this is a substantive null. **0 CERTIFIED, 0 RE-LABELED, 0 candidates-needing-scrutiny.** The
constructive enumerator is **provably complete** (shape-uniqueness theorem + brute-≤4 cross-check
11,209 = 11,209 MISSED=0/EXTRA=0 + independent skeleton brute 13 = 13) and **sound** (400/400 real-gate
keep-predicate), so the null is VALID — no real kernel is silently missed. a0 re-derives (9.36018e-11,
rel_err 1.97e-05) and certifies through the depth-5 pipeline (FDR-DEAD, as expected for a depth-3 quantity
with one forced provenance). FDR density is measured over the full 25-germ library with mult=21
(non-smuggle held). A mandatory 6 GB memory watchdog guards every phase; observed peak 0.28 GB, 0 swaps.

**Both-ways honesty:** the tightest hit (Koide Q = 2/3, rel_err 9.2e-06) is reported plainly as
reproducible-by-the-forced-kernel-but-FDR-dead-sparse — **not** dressed as a win; and the null is reported
as the expected/valid **strengthening** of the depth-4 result (the gates fired here on real dimensionless
kernels, whereas at depth-4 every target died at the dimensional filter before any gate fired) — **not**
dressed as a failure.

---

## 7. THE HONEST CEILING — what a depth-5 forced null does and does NOT prove

**Does prove:** at **depth-5 forced-complexity**, over the forced vocabulary `{3, sqrt(8pi/3)}` + one
free O(1), **no forced-geometric kernel is reachable that clears the full gate for any of the 21 SM
constants** — and this is the **first depth where the gates genuinely fire on dimensionless kernels**
(depth-4's null was a dimensional-filter triviality), so it is a **real strengthening** over depth-4, with
the constructive scheme proven complete (no silent miss).

**Does NOT prove:**
- No kernel at **depth ≥ 6** (a 3-scale skeleton, or a 2nd free germ under a different overdetermination
  rule, opens at depth 6 — untested here).
- No kernel under a **richer forced vocabulary** — the null is conditional on the audited two-germ forced
  set `{3, sqrt(8pi/3)}`; a new forced germ / a new forced gauge-or-Yukawa kernel would reopen the search.
- Nothing about a **new mechanism** outside the germ-decorate build model.
- The a0 depth-5 reach is a degenerate `a0 × identity` embedding (one forced provenance) — a0's *value*
  is not derived here; that quarantine is unchanged.

---

## 8. Reproduction commands

```bash
cd /Users/carlzimmerman/new_physics/project_atomos

# constructive space size (closed-form)
python3 exhaust_depth5_forced.py --space

# constructive COMPLETENESS (brute-≤4 cross-check) + SOUNDNESS — the load-bearing trip-wires
python3 exhaust_depth5_forced.py --self-check

# a0-validity through depth-5 (2-leg reach proof; ~35 s)
python3 exhaust_depth5_forced.py --a0-check

# full 21-target sweep, single process (~26 s, 300 MB)
/usr/bin/time -l python3 exhaust_depth5_forced.py --sweep

# full 21-target sweep, 12-worker parallel (detached), then aggregate
python3 exhaust_depth5_forced.py --workers 16     # capped to 12
python3 exhaust_depth5_forced.py --status

# one target
python3 exhaust_depth5_forced.py --target koide_Q_lep
```

All exit 0. RULE 3: `git diff --stat` on `gate/ engine/ exhaust.py exhaust_parallel.py
exhaust_depth4_forced.py` is EMPTY; HEAD still `ee44122`; only `exhaust_depth5_forced.py`,
`VERDICT_depth5_forced.md`, `notes/DEPTH5_FORCED_INTERLOCK_VERDICT.md`, and `results_exhaust_depth5/` are
new/untracked. No commit made.
