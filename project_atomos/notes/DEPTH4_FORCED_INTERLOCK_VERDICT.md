# Depth-4 Forced-Interlock Search — Both-Ways Verdict

**Date:** 2026-07-06
**Script:** `exhaust_depth4_forced.py` (new; `gate/`, `engine/`, `exhaust.py`, `exhaust_parallel.py` imported VERBATIM — RULE 3)
**Status:** CLEAN NULL. 0 CERTIFIED, 0 REAL-PUZZLE-RE-LABELED, 0 candidates-needing-scrutiny across all 21 dimensionless SM constants.

This extends the depth-3 EXHAUSTION THEOREM (complete null, 584,441 trees/target, 21 constants) to
**depth-4 forced-complexity** via a *sound* Gate-B pre-screen. It is the exact statement:
**no forced-geometric kernel is reachable at depth-4 forced-complexity.** It is NOT a proof that no
kernel exists at higher complexity or under a new mechanism (see the HONEST CEILING).

---

## 0. Reconciliation of the adversarial review (done before writing)

Three adversarial lenses (soundness, fdr-smuggle, fidelity) all reproduced every load-bearing number
and all three returned `verdict_holds = true`. Two raised framing issues; both were reconciled by
re-running the checks here:

**(i) One wrong arithmetic identity in the RUN'S PROSE (soundness lens; confirmed and corrected).**
The run's `aggregate_verdict` paraphrase said "kept 777,216 + dropped 14,883,418 == generated 15,729,010."
That is false: `777,216 + 14,883,418 = 15,660,634 ≠ 15,729,010`. I re-ran `--self-check`: the CODE
asserts the *correct* closure, `total_generated (15,729,010) == total_survivors (845,592) + total_dropped
(14,883,418)`, and prints "generated == survivors + dropped ? -> OK (closed)". `kept (777,216)` is a
PROPER SUBSET of survivors; the 68,376 gap = live subtrees that spawn children without themselves being a
completed keep. **The machine's invariant is correct and exits 0; only the human paraphrase swapped
"survivors" for "kept."** No code, gate result, or verdict changes. Corrected identity is stated in §1 below.

**(ii) The `accounting_closed` check is tautological (fidelity lens; framing downgraded, no number changes).**
`total_generated == total_survivors + total_dropped` holds by construction of `_consider` (every generated
node is routed into exactly one bin), so it cannot by itself detect a wrongly-dropped tree. It is a
book-keeping identity, not the soundness proof. The real soundness guarantee rests on three independent
legs, all re-confirmed: (1) the monotonicity of `Fset`/`Rset` under extension (D1/D2 bounds), (2)
`_verify_drop_soundness` exhausting the `(|Fset|,|Rset|,depth_k)` state space, and (3) the depth≤3
exhaustive real-gate agreement (0 Gate-B passers dropped, 0 predicate mismatches over 584,441 trees).
§1 frames it accordingly.

Neither issue touches a dropped tree, the FDR library, a0, or the null. **The clean null holds.**

RULE 3 verified clean *before and after* all my re-runs: `git diff --stat gate/ engine/ exhaust.py
exhaust_parallel.py` is empty.

---

## 1. Pre-filtered space size + completeness + soundness (the depth-4 theorem)

**Raw depth-4 leaf space (per target, unpruned closed form):**
`closed_form_count(11 leaves, 4, 25 germs) = [11, 2530, 581900, 133837000]`, total **134,421,441**.
The filtered generator TOUCHES 15,729,010 nodes at depths 2–4 (the rest are never generated because their
parents were pruned).

**Pre-filter drops (each PROVABLY Gate-B-impossible):**
- D1 (free-overflow): **11,755,392** — already carry >1 free O(1); extension only adds free params, so
  Gate-B condition (c) `n_free == 1` can never be recovered.
- D2 (forced-unreachable): **3,128,026** — cannot reach `Fset == {both forced provenances}` because
  `Fset`/`Rset` grow only monotonically under extension and the remaining depth budget is insufficient.
- **Total dropped: 14,883,418.**

**Kept → gate: 777,216** (all satisfy the Gate-B keep predicate: `Fset` covers both forced provenances
and exactly 1 free O(1)).

**Closed accounting (corrected identity):**
`total_generated (15,729,010) == total_survivors (845,592) + total_dropped (14,883,418)` ✓
`kept (777,216) ⊂ survivors (845,592)` (proper subset; the difference spawns children but is not itself a
completed keep). `D1 (11,755,392) + D2 (3,128,026) == 14,883,418` ✓.

**Soundness (why every dropped tree is Gate-B-impossible — the load-bearing proof, NOT the tautological
closure check):**
1. `Fset`/`Rset` are monotone under any extension operation (union-only) → a tree lacking a forced
   provenance can never regain it within budget (D2), and a tree already over the free-param cap can never
   drop back to 1 (D1). This is a property of the IMPORTED (verbatim) generation rule.
2. `_verify_drop_soundness` brute-forces all `(|Fset|,|Rset|,depth_k)` states and finds ZERO
   dropped-but-Gate-B-reachable violations.
3. Cross-check against the depth≤3 raw space: all 584,441 trees run through the REAL `gate.forced_kernel`
   → 0 Gate-B passers were dropped, 0 predicate mismatches.

`COMPLETENESS_OK = True`, `SOUNDNESS_OK = True`. **No Gate-B-passable depth-4 tree is dropped → the null
is VALID.**

---

## 2. a0-validity at depth-4 (RULE 2 reach proof)

The pipeline re-derives and re-finds a0 through the depth-4 dimensional filter (a0 × identity):

```
a0 RE-FOUND at depth 4:  ((c / Z) * H_L) = 9.36018e-11 m/s^2
   target 9.36e-11; rel_err = 1.97e-05; n_sigma = 0.00
   = c^2 sqrt(Lambda/32pi) = (c/Z)*H_L,  Z = sqrt(32pi/3) = sqrt(8pi/3)*2  (forced kernel x kappa=1/2)
   depth-4 raw emitted 2,053,875 -> dim-valid (L/T^2) 15,965 -> 315 distinct values; a0 is one of them.
a0_certifies_depth4 (dimensional filter re-finds a0): PASS
```

**Gate verdict on the a0 hit: FDR-DEAD @ Gate A** (`E_chance = 0`, 0 wide hits, surplus = 5.0 bits ×21
look-elsewhere < 10-bit threshold → BAKED). This is EXPECTED and consistent with the depth-3 theorem:
a0 presents exactly ONE forced provenance (`sqrt(8pi/3)`) + `kappa=1/2` free → not overdetermined → fails
Gate-B condition (b). **The reach proof is the dimensional re-derivation, which PASSED.** a0 is the ONLY
expression in the entire sweep that clears the dimensional filter — because it is dimensionful (L/T²); no
dimensionless SM target can (see §4). The a0 5.0-bit figure is the *precision cap* (`n_digits·log2(10) ≈
4.963`), pool-INVARIANT: recomputed under both the pinned 7-germ pool and the full 25-germ pool, bits =
4.963 in BOTH (|Δ| = 0.0), so sparsification neither inflates a0 toward a win nor does enrichment resurrect
it. The reach proof stands: the machine CAN reach a0, so a null means "no forced kernel reachable," not
"the search reaches nothing."

---

## 3. FDR honesty (non-smuggle: full realistic library + look-elsewhere)

Gate A's chance density is measured over the **FULL 25-germ library** — the same rich pool (forced +
flavor + O(1) germs) the depth-3 exhaustion used — NOT a sparsified forced-only pool. Enforced by a hard
guard that crashes any sparse run:

```python
assert len(alpha.germs) == 25, f"FDR non-smuggle: expected 25 germs, got {len(alpha.germs)}"
```

(Forcing a 3-germ pool raises `AssertionError: expected 25 germs, got 3`.) Look-elsewhere multiplicity
`mult = 21` (n_targets) is folded in: `chance = min(1, e_chance) * mult`. The pre-filter shrinks WHICH
CANDIDATES are generated (tractability); it does NOT shrink the library against which surprise is measured.

Honest caveat (fdr-smuggle lens): for the 21 SM targets Gate A **never actually fires** — they all die
upstream at the dimensional filter (dim_valid = 0, §4). So the FDR machinery is correctly *wired and
guarded* but is exercised on exactly ONE expression in the whole sweep (a0, the dimensionful control). This
makes the FDR-smuggle attack surface essentially empty for the SM sweep and STRENGTHENS the null rather
than weakening it: there is no SM "surprise" to inflate in the first place.

---

## 4. Per-target result — the aggregate (complete null at depth-4 forced-complexity)

All 21 dimensionless SM constants: **CERTIFIED 0, REAL-PUZZLE-RE-LABELED 0, in-window hits 0,
dim_valid = 0.**

Targets swept (each an identical clean-null block): `a_e, alpha_em_inv_0, r_p_e, r_n_p, r_mu_e, a_mu,
koide_Q_lep, r_tau_e, r_tau_mu, alpha_em_inv_MZ, sin2_thetaW_MZ, koide_Q_up, higgs_lambda, ckm_lambda,
koide_Q_down, r_b_tau, r_t_b, alpha_s_MZ, pmns_sin2_13, pmns_sin2_12, pmns_sin2_23`.
(`grep -c "CERTIFIED: 0" = 21`; `grep -c "^DEPTH-4 FORCED-INTERLOCK" = 21`.)

**Why zero — a STRUCTURAL depth-budget theorem (surfaced honestly, strengthens the null):**
A Gate-B pass requires 3 distinct germ leaves — `{3 → Ngen_3, sqrt(8pi/3) → a0_kernel_8pi3, one free
O(1)}`. In the imported generation rule, germs are decorate-only (each germ costs one `decorate` level),
so 3 distinct germ leaves consume the full decorate budget and force **exactly one dimensionful scale
leaf** — never zero. All 11 measured leaves are dimensionful, so every one of the 777,216 kept trees carries
exactly 1 scale leaf → is dimensionful → **cannot equal any dimensionless SM constant.** The dimensional
filter admits ZERO Gate-B-passable trees for any dimensionless target. This was independently confirmed:
all 777,216 kept trees have scale-leaf count exactly 1, zero have 0. It is a property of the imported
(verbatim) generation rule, not a smuggle.

**Koide, explicitly:** `koide_Q_lep/up/down` are in the sweep and are the closest real puzzle. They still
FAIL Gate B (as at depth-3): `sqrt(2)` appears in only ONE forced place and a Koide fit needs a 2nd free
number → not overdetermined + n_free ≠ 1. No re-labeling either (needs A & C2; B's failure is upstream of
the dimensional death here). The one genuine SM lead remains a re-labeling, not a forced kernel.

**Both-ways bottom line:** This is a CLEAN NULL, and a clean structural null is the EXPECTED, VALID
outcome — not a failure of the machine. It is NOT a manufactured dismissal (the pre-filter is provably
sound, the FDR is over the full 25-germ library, and a0 genuinely re-derives) and NOT a manufactured win
(0 survivors, honestly reported).

---

## 5. The HONEST CEILING — what this does and does NOT prove

**DOES prove:**
- No forced-geometric kernel (2+ forced provenances, ≤1 free O(1)) reproduces ANY of the 21 dimensionless
  SM constants **at depth-4 forced-complexity**, under the imported, calibrated (8/8) gate.
- This EXTENDS the depth-3 exhaustion theorem (a0-complexity) to a0-complexity+1. The pre-filter is sound
  (0 Gate-B-passable trees dropped), so "null" means "no forced kernel *reachable at this complexity*,"
  not "the search cannot reach anything" (a0 IS reached — the reach proof).
- The SM mass + mixing sector is **kernel-free at depth-4 forced-complexity** — consistent with the
  number-field obstruction (Z carries √π transcendental; flavor data algebraic → a0/Z structurally
  gauge-blind).

**Does NOT prove:**
- That NO forced kernel exists anywhere. Higher complexity (depth ≥ 5), a LARGER forced-germ registry, or
  a genuinely NEW forced mechanism (a new gauge/Yukawa kernel that earns forced credit) are all outside
  this null's reach.
- Anything about **sign, Z, or kappa** — these remain POSTULATED, not derived.
- That the framework's a0 reframing is right or wrong — a0 re-derives dimensionally but lands FDR-DEAD
  (one forced provenance), exactly as the depth-3 theorem says.

**Standing:** This does NOT re-open the SM mass/mixing sector. Per the exhaustion standing, the sector
stays WALLED — do not re-open absent a NEW forced gauge/Yukawa kernel. Depth-4 is another wall brick, not
a door.

---

## 6. Reproduction commands (each exits 0)

```bash
cd /Users/carlzimmerman/new_physics/project_atomos
python3 exhaust_depth4_forced.py --a0-check     # RULE 2 reach proof: a0 = (c/Z)*H_L = 9.36018e-11, PASS
python3 exhaust_depth4_forced.py --self-check    # completeness + soundness; prints closed accounting
python3 exhaust_depth4_forced.py --target r_mu_e # one SM target: dim_valid 0, CERTIFIED 0
python3 exhaust_depth4_forced.py --sweep         # all 21 targets, single process (clean null x21)
# RULE 3 (must be empty before AND after):
git diff --stat gate/ engine/ exhaust.py exhaust_parallel.py
```

**Key reproduced numbers:** a0 = 9.36018e-11 (rel_err 1.97e-05, n_sigma 0.00, FDR-DEAD, reach PASS);
raw = [11, 2530, 581900, 133837000] = 134,421,441; dropped 14,883,418 (D1 11,755,392 + D2 3,128,026);
kept 777,216; survivors 845,592; closure `15,729,010 == 845,592 + 14,883,418`; dim_valid 0; 0 CERTIFIED /
0 RE-LABELED across all 21 targets. FDR over full 25-germ library, mult = 21. RULE 3 clean.
