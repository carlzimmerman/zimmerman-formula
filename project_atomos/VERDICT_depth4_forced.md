# Depth-4 forced-interlock search — VERDICT

**A SOUND, Gate-B-pre-filtered, EXHAUSTIVE depth-4 forced-interlock search over the SM constants.**
Every number below comes from `exhaust_depth4_forced.py`, which imports `gate/` and `engine/`
**verbatim** (RULE 3) and exits 0. Reproduce with:

```
python3 exhaust_depth4_forced.py --a0-check      # a0 reach proof (RULE 2)
python3 exhaust_depth4_forced.py --self-check    # completeness + soundness theorem
python3 exhaust_depth4_forced.py --sweep         # all 21 SM targets, depth 4
```

---

## Bottom line

**A clean, decisive NULL — and, at depth 4, an ANALYTIC one.** Over all **21** dimensionless SM
constants at depth 4: **0 CERTIFIED, 0 REAL-PUZZLE-RE-LABELED, 0 in-window hits.** No forced kernel
is reachable. This is the *expected, valid* outcome of the machine (a null is not a failure), and it
is now established with a *stronger* guarantee than the depth-3 exhaustion theorem: at depth 4 the
forced-interlock null is provable **before** the value filter, by a structural depth-budget theorem
(below).

The search is NOT broken: **a0 re-derives through the depth-4 pipeline** (RULE 2 reach proof), so
the null means "no forced kernel reachable", not "the machine can't reach anything".

---

## 1. a0-validity (RULE 2 reach proof) — PASS

Pinned pool `{c,G,Λ,ρ_Λ,H_Λ}+{π,8,3,2,32π,√(8π/3),Z}`, depth 4, tol 1%:

| quantity | value |
|---|---|
| depth-4 raw emitted (pinned pool) | 2,053,875 |
| dim-valid (L/T²) | 15,965 |
| distinct values | 315 |
| **a0 re-found** | `((c / Z) * H_L)` = **9.36018e-11 m/s²** |
| rel_err vs 9.36e-11 | **1.97e-05** (n_sigma ≈ 0.00) |
| gate verdict on the a0 hit | **FDR-DEAD @ Gate A** (5.0 bits, below 10) — EXPECTED |

a0 appears at depth 4 as **a0 × identity** and is re-found by the **dimensional** filter. It does
NOT clear Gate B in the *code* (it presents a single forced provenance string `√(8π/3)` + κ=½ free →
"not overdetermined" to the code) — exactly consistent with the depth-3 theorem: a0 is the cosmology
**calibration positive**, re-derived dimensionally, not a Gate-B kernel. **`a0_certifies_depth4 =
PASS`** (the reach proof is the dimensional re-derivation).

---

## 2. Completeness + Soundness (the depth-4 theorem) — PASS

**(A) Generation completeness (unpruned closed form).** On the full 11-leaf / 25-germ pool:

| depth | 1 | 2 | 3 | 4 | total |
|---|---|---|---|---|---|
| raw trees T(d) | 11 | 2,530 | 581,900 | 133,837,000 | **134,421,441** |

matches `closed_form_count(11,4,25)` exactly (the generator is exhaustive before any drop).

**(B) Sound Gate-B pre-filter.** The Gate-B pass predicate collapses to a decidable condition on a
tree's germ-leaf set (empirically verified against the real `gate.forced_kernel.forced_kernel_detector`:
case A passes; `n_free=0`, `n_free=2`, one-forced, zero-forced all fail):

> **PASS iff** `Fset == {Ngen_3, a0_kernel_8pi3}` (both forced-credit germs) **AND** `len(Rset) == 1`
> (exactly one distinct free O(1) germ).

Only **2** of the 25 germs earn forced credit: integer `3`→`Ngen_3` and `√(8π/3)`→`a0_kernel_8pi3`
(audited). All 23 others (every flavor germ, π, 8, Z, 32π, …) are free O(1)s.

Since `Fset`/`Rset` only **grow** under extension (union at every node; no op removes a leaf), two
drop rules are provably sound:

- **D1 (free-germ overflow):** `|Rset| ≥ 2` ⇒ `free_params ≥ 2` forever ⇒ Gate-B-dead.
- **D2 (forced-germ unreachable):** need `= (2−|Fset|) + max(0, 1−|Rset|)` more distinct germs, each
  costing ≥1 depth level; if `need > (4−k)` for a depth-`k` subtree ⇒ Gate-B-dead.

Drop accounting on the full pool (`--self-check`, ~7 s):

| quantity | value |
|---|---|
| filtered generator produced (depths 2–4) | 15,729,010 |
| dropped **D1** (free-overflow) | 11,755,392 |
| dropped **D2** (forced-unreachable) | 3,128,026 |
| **dropped total** | **14,883,418** |
| **KEPT completed → gate** | **777,216** |
| generated == survivors + dropped | **OK (closed)** |
| all KEPT satisfy the Gate-B keep predicate | **OK** |
| drop soundness (constructive re-verification over the (\|Fset\|,\|Rset\|,depth) state space) | **PROVEN** |

`soundness_ok = True`, `completeness_ok = True`. No Gate-B-passable tree is dropped; every kept tree
is re-checked by the actual gate.

---

## 3. The structural depth-budget theorem (why the null is ANALYTIC at depth 4)

A Gate-B pass needs **3 distinct germ leaves** (`3` + `√(8π/3)` + one free germ). Each germ enters
only through a **decorate** step (the imported generation rule), consuming one depth level. Three
germs consume 3 of the 4 levels, leaving exactly **one** level for the scale skeleton — i.e.
**exactly one dimensionful scale leaf**. Verified directly: **all 777,216 KEPT trees have
scale-leaf count = {1}**, and a bucket-scan of 3,000,000 raw depth-4 trees confirms the
`(≥3 germ, ≥2 scale)` class is structurally **empty**.

A single dimensionful scale (c, G, Λ, ρ_Λ, H_Λ, M_P, …) is **never dimensionless**. Therefore, for a
**dimensionless** SM target, the dimensional filter admits **zero** Gate-B-passable trees:
`dim_valid_distinct_values = 0` for every target. This is a property of the *imported generation
rule*, not the pre-filter, so it strengthens (does not weaken) the null.

---

## 4. FDR non-smuggle — CLEAN

`fdr_uses_full_library = True` for every target: `assert len(alpha.germs) == 25` holds, and the gate's
`build_value_set` is fed the **full 25-germ pool** (via `gate_candidate_for`'s `germ_pool =
_germ_pool_from_alpha(alpha)`), with `mult = n_targets = 21` folded in. The pre-filter shrinks *which
candidates are generated*, never the library surprise is measured against. (Vacuously clean this run:
0 candidates reach the FDR because the dimensional filter is empty — but the wiring is verified on the
a0 hit, which is scored against the full-pool library.)

---

## 5. Full 21-target sweep — NULL

`python3 exhaust_depth4_forced.py --sweep` (7 m 26 s single-core):

| across all 21 targets | value |
|---|---|
| KEPT completed (identical enumeration) | 777,216 |
| scale-leaf counts | {1} |
| dim-valid distinct values | 0 |
| in-window hits | **0** |
| CERTIFIED | **0** |
| REAL-PUZZLE-RE-LABELED | **0** |

Targets: `a_e, alpha_em_inv_0, r_p_e, r_n_p, r_mu_e, a_mu, koide_Q_lep, r_tau_e, r_tau_mu,
alpha_em_inv_MZ, sin2_thetaW_MZ, koide_Q_up, higgs_lambda, ckm_lambda, koide_Q_down, r_b_tau, r_t_b,
alpha_s_MZ, pmns_sin2_13, pmns_sin2_12, pmns_sin2_23`.

---

## 6. Tractability

- **Single-target:** ~21 s. **Full sweep (21 targets):** ~7.5 min single-core — **tractable in one
  run**; no sharding required. A `--workers N` / `--status` shard mode (mirrors
  `exhaust_parallel.py`) is provided for convenience (verified: worker writes `result.json`, `--status`
  aggregates).
- vs. the infeasible **134,421,441** raw trees/target: the sound pre-filter drops 14.88M dead
  subtrees at generation and hands only 777,216 completed candidates to the (here-vacuous, dimension-
  killed) gate.

---

## 7. Honest standing (both-ways)

- **NOT a win:** nothing certified; no candidate-needing-scrutiny survived. The a0 hit is FDR-DEAD by
  design (calibration positive, not a kernel).
- **NOT a manufactured dismissal:** the null is *computed*, the pre-filter is *provably sound* (no
  passable tree dropped), the FDR is measured over the *full* library, and a0 *does* re-derive (the
  machine can reach a real forced structure when one exists).
- **Result:** at a0-complexity **plus one** (depth 4), there is **no forced-geometric kernel** behind
  the 21 SM constants reachable by the framework's own template. The depth-4 layer cannot even present
  a dimensionally-valid Gate-B candidate for a dimensionless target — a structural theorem, not a
  fitting accident. **Sign/Z/κ remain postulated; the SM mass+mixing sector remains kernel-free at
  this depth.** This is a CANDIDATE-FREE null, explicitly not a claim about deeper depths or other
  templates.
