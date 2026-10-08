# INTERLOCK_SPEC — corrected specification for a multi-target interlock search

**Scope.** One expression-core required to match SEVERAL independent measured constants
simultaneously. This is the only regime with discriminating power above the single-target depth
ceiling (single-target best is **D_max = 12.8**, and the committed exhaustive campaign already
reached depth 10). This document supersedes `GATE_POWER_ANALYSIS.py` S1/S2/S6 and `BITS_RULE.py`
in their entirety. Section 0 records which of the six prior lens audits was right on each
disputed point, decided by re-measurement rather than by averaging.

**Everything below is produced by four scripts that were written and run, all exit 0:**

| script | checks | what it measures |
|---|---|---|
| `audit_interlock/interlock_spec_core.py` | 49/49 | windows & sigma convention, look-elsewhere count, local density, core decomposition |
| `audit_interlock/interlock_spec_model.py` | 6/6 | per-core reach heterogeneity, out-of-sample calibration, single-target ceiling |
| `audit_interlock/interlock_spec_validate.py` | 18/18 | full depth-8 rebuild (8,123,807 values, exact core attribution), tight-target validation, depth scaling |
| `audit_interlock/interlock_spec_sets.py` | 32/32 | algebraic/theory independence, legitimate sets, threshold, depth plan, traps |

Outputs: `interlock_spec_{core,model,validate,sets}.json` and `*_output.txt` in the same directory.

---

## 0. Which prior audit was right about what (contradictions resolved by re-measurement)

| claim in dispute | verdict | evidence |
|---|---|---|
| m_p/m_e window is 24,459× / 14.6 bits too wide (*windows*) vs 1000× arithmetic error in GPA (*ceiling_math*) | **ceilingmath right, windows wrong** — the direct-ratio rel is 1.743e-11, the search's window is 24.5× too wide = 4.61 bits | `core.py` S2: `1836.152673426(32)` = ±3.2e-8 absolute; stored central matches the direct ratio to 0.02 direct-σ |
| "no factor-of-2 / sigma-convention mismatch" (*windows*) | **confirmed** | `core.py` S1: hit at 0.999σ, miss at 1.001σ, edge = 1.0000σ on all 20 targets |
| Gate A's `_bit_cap` is +1 bit generous (*windows*) | **confirmed exactly** | `core.py` S1: excess = 1.000000 on every target, max dev 3.6e-15 |
| look-elsewhere must be DISTINCT values, `30^(D−4)` is the step menu (*effective_N*, *ceiling_math*) | **confirmed**, and superseded: the right reference is neither, it is the **local density** | `core.py` S3/S4: raw identity exact at 5 depths; global N·W over-states hits by 130× |
| "clustering makes the threshold CONSERVATIVE, no penalty needed" (*clustering*) | **WRONG for interlocks.** True for single targets and for skeleton-level *label* permutation, but per-core REACH heterogeneity is strongly **anti-conservative**: 11.6× in the unsaturated regime, 637× at k=8 | `core.py` S5, `model.py` M1–M2, `validate.py` V4 |
| "BITS_RULE charges nothing for germ freedom → would pass chance-level families" (*clustering*, last finding) | **confirmed in direction**, and now quantified as a measured, validated M(T) term (5.16 bits per extra target, not a hand-set 12.5) | `validate.py` V4/V5, §3.4 |
| both HOLDOUT keys are algebraically void (*independence*, *gate_b*) | **confirmed, and sharpened**: koide_Q_lep's conditional bits are **0.00**, not "small"; r_tau_mu is an exact monomial | `sets.py` T1/T2 |
| a_e and 1/alpha are ONE observable (*independence*) | **confirmed** (≤4.35 conditional bits of 32.05) | `sets.py` T3 |
| drop r_t_b from the pool for ρ = −0.974 (*independence*) | **OVER-STRICT — rejected.** Jacobian rank 2; ρ is a 2.13-bit *bonus* test, not a disqualification | `sets.py` T4 |
| "span residual ⇒ spanned" as an independence test (*independence*) | **method rejected**: 18 free real coefficients fit any single number. Replaced by an exponent-lattice search plus explicit closed forms | `sets.py` T1/T2 |
| E=1 is not a criterion; use a family-wise E* (*ceiling_math*) | **confirmed in principle**, but its E* double-charged multiplicity already inside E. §5 folds all multiplicity into E and then requires E ≤ 0.05 once | `sets.py` T6 |
| Gate B is a constructive tautology that credits cancelled germs (*gate_b*) | **confirmed by re-running the real gate** | `sets.py` T7a |

---

## 1. Corrected windows and sigma convention

**The convention is already consistent — no factor-of-2 bug exists.** `grind.sweep_target_streamed`
hits iff `score_value(v,t).rel_error <= measurement_tol(t)`, i.e. **half-width = 1.000 σ**. Probed
against the real engine at 0.999σ / 1.001σ / edge for all 20 swept targets: hit / miss /
n_sigma = 1.0000 (mpmath probe; `score_value` casts to float64 internally, which resolves the
edge to 1.5e-6 σ at worst). All bits below use the **FULL relative window W = 2·tol**.

**Correction 1 — Gate A's own bit cap is exactly 1 bit too generous.** `_bit_cap = n_digits·log2(10)`
and `n_digits = −log10(rel_precision)`, so `cap = log2(1/W) + 1.000000` on **every** target
(max deviation 3.6e-15 over 20 targets). `PASS_BITS = 10` is therefore effectively 9 window-bits.
Consequence: **10 of the 19 searched targets have cap < 10 and can never certify by construction**
(koide_Q_up 9.53 … pmns_sin2_12 4.66), and those 10 carry **82,463 of the 82,613** depth-10
in-window hits = **99.82 %**. The "82,613 hits, 0 certified" headline is 99.8 % denominator.

**Correction 2 — the m_p/m_e window, resolving a direct contradiction between two prior audits.**
`1836.152673426(32)` means ±3.2e-8 **absolute**, so rel = **1.7428e-11**.
`GATE_POWER_ANALYSIS.py:41` writes `3.2e-11/1836.15` = 1.743e-14 and `BITS_RULE.py:14` writes
3.49e-14: both are **1000× too tight**. The *windows* audit repeated GPA's `3.2e-11` as if it were
the absolute sigma and concluded "24,459× too wide / 14.6 bits" — **that is wrong**. The
*ceiling_math* audit is correct. The true picture: the registry stores a **propagated** rel of
4.2626e-10 (quadrature of two MeV masses) while its **central value matches the direct CODATA
ratio to 0.02 direct-σ** — so the central value is the direct measurement and the sigma is not.
The search's window is **24.5× too wide = 4.61 bits left on the table**, not 14.6.

**Correction 3 — how much of that is reachable today.** `engine/scoring.measurement_tol`'s
`min_tol=1e-10` floor clamps the direct r_p_e window: 34.74 window-bits available, 32.22 reachable
under the clamp, 30.13 in use today. So **+2.09 bits today, +4.61 after lowering `min_tol` to
1e-11** — which is safe: float64 resolution at 1836.15 is 1.2e-16 relative, 8e4× of headroom.
r_n_p gains +0.54 bits from the direct ratio (not clamped); r_mu_e, α⁻¹, a_e need no change.

**Everything else about the windows is fine and should be left alone.** The `min_tol` / `max_tol`
clamps bind on 0 of 20 targets as stored; α⁻¹ and a_e sigmas match CODATA-2022 exactly; my recount
of the depth-10 hits from `values.f64` reproduces the committed 82,613 exactly.

Window bits (W = 2·tol, corrected where noted):

| target | W | bits | | target | W | bits |
|---|---|---|---|---|---|---|
| a_e | 2.242e-10 | 32.05 | | koide_Q_up | 2.698e-03 | 8.53 |
| alpha_em_inv_0 | 3.065e-10 | 31.60 | | higgs_lambda | 3.514e-03 | 8.15 |
| **r_p_e** | 3.486e-11 † | **34.74** † | | ckm_lambda | 6.044e-03 | 7.37 |
| **r_n_p** | 8.988e-10 † | **30.05** † | | koide_Q_down | 6.144e-03 | 7.35 |
| r_mu_e | 4.354e-08 | 24.45 | | r_b_tau | 1.435e-02 | 6.12 |
| a_mu | 3.774e-07 | 21.34 | | r_t_b | 1.474e-02 | 6.08 |
| r_tau_e | 1.351e-04 | 12.85 | | alpha_s_MZ | 1.525e-02 | 6.03 |
| alpha_em_inv_MZ | 1.407e-04 | 12.80 | | pmns_sin2_13 | 5.084e-02 | 4.30 |
| sin2_thetaW_MZ | 2.595e-04 | 11.91 | | pmns_sin2_12 | 7.921e-02 | 3.66 |
| | | | | pmns_sin2_23 | 6.294e-02 | 3.99 |

† direct CODATA ratio; 32.22 reachable until `min_tol` is lowered.

---

## 2. Corrected look-elsewhere count

**`N(D) ≈ 30^(D−4)` is wrong three times over and must be deleted.**

1. **30 is the step-menu LENGTH, not a branching factor.** The realized identity
   `raw(D) = Σ_{b_s=1..D−4} n_skel(b_s)·n_recipe(D−1−b_s)` reproduces **every** committed raw count
   EXACTLY: 236,624 / 1,566,116 / 8,123,807 / 38,450,388 / 174,890,804 at D = 6…10.
   I solved the layer counts from the committed data (b_s=1,2 measured directly with the real code;
   b_s=3..6 solved with zero remainder from raw(7..10)) and cross-checked them against the
   committed `n_skeletons_total` at three depths:
   `n_skel(1..6) = 13, 73, 247, 1147, 5250, 22708` (Σ = 29,438 = committed).
   Distinct-value growth: **4.63, 4.43, 4.45, 4.33 per depth** → **2.11 bits/depth**, not log2(30)=4.91.
   `30^6 = 7.29e8` over-counts the real 42,534,139 distinct by **17.1×**; at D=18 it over-charges
   the extrapolated distinct count by ~26 bits.
2. **Raw is the wrong population; distinct is not right either.** A hit is a property of a *value*.
   The within-core duplication factor is exactly the germ-factor list's own dedup
   (1.82× at g_s=3 rising to 8.63× at g_s=6), and the depth-8 **per-core-deduped** population
   (2,141,752) equals the **globally deduped** committed count (2,207,173) to **1.03×** — so
   essentially all duplication is within-core, and **the committed `values.f64` density is already
   the right per-core-summed density**, to a few percent. (A third layer: 42,534,139 mpmath keys →
   33,309,840 distinct float64, 0.353 bits, plus 1,144,060 inf and 1,085,488 ≤0.)
3. **The global count is the wrong reference entirely.** The value set spans **631.6 decades** of
   ln|v|. `N·W` over-states the measured hits by a median **130×** (7.02 bits, range 79–205×).
   The correct quantity is the **LOCAL density ρ_i per unit ln|v|** measured at each target; then
   `H_i = ρ_i·W_i` is unbiased — median measured/predicted **1.001** over the 14 targets with
   H_pred > 5.

**Use these instead of N(D):**

| quantity | value at D=10 | growth per depth |
|---|---|---|
| local density ρ_i at target i | 244,280 … 334,500 per unit ln (per-target, measured) | **B_ρ = 3.847** (1.944 bits) |
| core count n_cores (skeletons) | **29,438** | **B_core = 4.460** (2.157 bits) |
| dressings per core | 5,941 | — |
| concentration growth (§3) | — | **G1 = 1.558** (0.640 bits) |

---

## 3. The chance model — and the missing constraint that makes it necessary

### 3.1 What is wrong with "windows multiply"

`BITS_RULE.py` sums window bits and charges nothing for the freedom spent reaching each target.
Measured on the committed depth-10 records: cores reaching ≥ k of the 19 targets, observed vs a
homogeneous "every core equally likely" model — **obs/model = 0.09 at k=2 but 5.5× at k=6 and
637× at k=8**. Root cause, measured: only **2,910 of 29,438 cores (9.89 %)** place *any* dressed
value inside *any* target window, although the mean is 2.806 hits per core. **Per-core reach into the
O(1) decade is heavy-tailed, so coincidences concentrate.** A label-permutation null that preserves
per-core record counts *does* match observation (obs/null 0.73–1.00, z ≤ −5.2 at every k) — so this
is reach heterogeneity, not a violation of window independence.

The reach really is shared across the decades an interlock would use: on the fully rebuilt depth-8
set, the per-core rank correlation of reach between the six tight targets (spread over 1e-2.9 to
1e+3.3) is **0.61 … 0.999, median 0.75**.

### 3.2 The formula

For a core set at strictness level L1 (core = skeleton; germ dressing free per target — the
loosest legitimate interlock, hence the conservative accounting):

```
E[interlock tuples matching every target in T]  =  M(T) · Π_{i∈T} ( ρ_i(D) · W_i ) / n_cores(D)^(k−1)

    M(T) = E_c[ Π_i r_c(i) ] / Π_i E_c[ r_c(i) ]        ( = 1 iff cores were homogeneous )
    r_c(i) = core c's own value density per unit ln at target i
```

*Tuples* = (core, one matching dressing per target) = the number of distinct k-target relation sets
a chance search would print. Verified as an **exact identity** at depths 8/9/10 and k=2,3
(max deviation 2.2e-16). *Cores* is a smaller statistic needing the saturation term `1−exp(−r·W)`;
in the tight-target regime the two coincide, because the maximum per-core expected hit count over
the six tight targets is **2.5e-4** (the `1−exp` correction is under 0.02 %).

### 3.3 Validation (this is the part that makes the spec usable)

Because the tight targets have zero hits at their real windows, I rebuilt the **entire depth-8
candidate set** — all **8,123,807** values with exact `(b_s, skeleton)` attribution, using the real
`_skeleton_value_nodes` and `_germ_recipes` — and validated against measurement:

* **Rebuild is faithful:** raw count 8,123,807 = committed; cores 1,480 = committed; the committed
  depth-8 per-target hit counts reproduced on **19/19** targets.
* **Multi-decade coincidences, measured vs modelled** (six tight-target *locations*, common ln
  half-width h from 1e-4 to 1e-2, k=2,3,4): exact per-core model **obs/model median 1.21, max 1.56**
  at every h and k. The closed form over-states the exact rate by **1.18×** in the unsaturated
  regime (conservative). The **homogeneous** model under-states the same measurement by **11.6×**.
* **Depth scaling is predictive, not fitted.** `G1` fitted on k=2 pairs only (1.558, range
  1.19–1.86) predicts the measured k=3 per-depth growth **out of sample: median 1.10, range
  0.81–2.48** over 19 sets. Composite chance growth: **5.17× (k=2), 6.95× (k=3), 9.34× (k=4)** per
  depth = **+2.37 / +2.80 / +3.22 bits per depth**.
* **A first attempt failed and was discarded, not patched over:** M(T)'s depth trend measured on
  sets containing alpha_s (per-core hit probability 0.17) gave 2.48×/depth and predicted 8.2×/depth
  growth against a measured 3.4× — **saturation contamination**. The `M_k` factorial-moment table in
  `interlock_spec_model.py` is superseded for the same reason and is labelled as such in the script.

### 3.4 The concentration penalty, measured

M(T) on the rebuilt depth-8 set, exact:

| set | k | M(T) | log2 M(T) |
|---|---|---|---|
| {a_e, α⁻¹} | 2 | 3.42 | 1.77 |
| {a_e, m_p/m_e} | 2 | 2.09 | 1.07 |
| {a_e, m_p/m_e, m_n/m_p} | 3 | 70.4 | 6.14 |
| {a_e, α⁻¹, m_p/m_e, m_n/m_p} | 4 | 2,921 | 11.51 |
| all six tight | 6 | 4.35e6 | 22.05 |
| {alpha_s, ckm_lambda, sin2θW} | 3 | 269.6 | 8.07 |

Fit: **log2 M(T) = 5.16·(k−1) − 3.88**, i.e. ~**5.2 bits of penalty per extra interlocked target**,
plus **0.640·(k−1) bits per depth** beyond depth 8 from G1.

---

## 4. Legitimate independent target sets

### 4.1 The one dependence that is FREE in this enumeration

The step menu is MUL / DIV / POW(2,3,½,−1,⅔) / SQRT / CBRT / INV over leaves and germs — **there is
no ADD anywhere**, and the germ layer is pure multiplicative net-exponent bookkeeping. Therefore:

* **MONOMIAL dependence makes a target free** (one extra MUL/DIV/POW step) → must be excluded.
* **ADDITIVE dependence does not make a hit free** — but it can make the target's *value* already
  determined, which is a separate disqualification (§4.2).

Exponent-lattice search (exponents ±{⅓,½,1,2,3}, subsets of size 1–2, all 21 targets):
**0 monomials of pool targets land inside any of the six TIGHT targets' windows**, versus **259
landing inside the 13 LOOSE pool targets' windows** (17 for alpha_s, 29 for pmns_sin2_13, 100 for
pmns_sin2_12). A loose target is nearly free given two others — an independent reason, beyond its
low bit content, never to build an interlock on one.

### 4.2 Both holdouts are void

* `r_tau_mu = r_tau_e / r_mu_e` **exactly** (rel dev 1.4e-16; all three are built from the same
  m_e, m_mu, m_tau registry entries) → a one-DIV monomial of two searched pool targets.
* `koide_Q_lep = (1+A+B)/(1+√A+√B)²` with A = r_mu_e, B = r_tau_e — verified to 1.0e-16. Propagating
  the two pool windows through Q gives a conditional full width **2.033e-05** against Q's own full
  window **2.032e-05** → **conditional bits = 0.00**. Zero, not "small".

Neither can ever be an out-of-sample test. The fix is to **replace** the holdout, not to restore
`r_tau_mu`'s retention (it is missing even from `sm_target_keys(include_holdout=True)`, which
returns 20 keys and only re-adds koide_Q_lep).

**Valid replacement (carve-out).** There is no spare candidate *outside* the pool: `sm_target_keys`
is `precise_targets(1e-2) ∩ dimensionless()`, so every dimensionless registry target measured
better than 1 % is already in the pool. Evaluating each pool target as a carve-out against
POOL \ {h} (disjoint parents, 0 monomials in window, not theory-determined, > 5 window bits):

* **`sin2_thetaW_MZ`** — 11.91 window bits, parent set {itself}, **0** monomials of the other 18
  land in its window. **Recommended holdout.**
* `alpha_em_inv_0` — also valid (31.60 bits) but it is the single most valuable interlock member;
  carving it out costs more than it buys.

Caveat to state in any write-up: *disjoint from the pool* is not *disjoint from all of physics*.
sin²θW is fixed by the global electroweak fit (M_W, M_Z, G_F) — none of which are pool targets, so
it is out-of-sample for **this** search, but a survivor must also be checked against that external
determination.

### 4.3 Theory-determined pairs (banned)

| pair | computed | conditional bits of the 2nd member | nominal |
|---|---|---|---|
| {a_e, α⁻¹(0)} | QED series (AHKN coefficients) + had/weak from α alone reproduces a_e to **2.28e-9** rel = 20.3σ of a_e's own window | **4.35** (residual-based) or **0.45** (α-propagation floor) | 32.05 |
| {α⁻¹(0), α⁻¹(M_Z)} | RG running, hadronic-VP limited to ~0.01 absolute = 7.8e-5 rel vs the target's own 7.0e-5 | **0.15** | 12.80 |

**`a_mu` is CONDITIONAL, not banned.** Given α *alone* (QED only) the prediction sits 6.3e-5 rel
from the measurement = 334σ → **8.38** conditional bits. Once the SM's external hadronic input is
allowed (~4e-10 absolute) → **0.86** bits. That 8-bit ambiguity is not resolvable inside this repo,
so `a_mu` is excluded from any set containing α⁻¹(0) or a_e and otherwise flagged, rather than
credited or banned.

### 4.4 Shared-parent correlation — a prior audit went too far here

Every construction identity was verified numerically first (rel dev ≤ 2e-16). Pool pairs with
|ρ| ≥ 0.2: r_p_e/r_n_p −0.343 (shared m_p), koide_Q_down/r_b_tau +0.308, koide_Q_down/r_t_b −0.300,
**r_b_tau/r_t_b −0.974** (shared m_b).

**High ρ does NOT disqualify a pair.** r_b_tau = m_b/m_τ and r_t_b = m_t/m_b are two independent
functions of three measured masses — **Jacobian rank 2**, verified, as it is for {r_p_e, r_n_p} and
{r_mu_e, r_tau_e}. ρ means the measurement *errors* are correlated, so the true pair lies in a thin
ellipse inside the gate's acceptance box. The gate charges box bits and accepts the box, which is
the correct false-positive accounting; the ellipse is a **bonus test worth up to 2.13 extra bits**
that a survivor must also pass. `target_independence_graph.py` dropped r_t_b from the pool on
ρ = −0.974 — that throws away real information and is **over-strict**.

### 4.5 Per-target interlock value, and the maximal legitimate sets

A target is worth adding iff `log2(1/(ρ_i·W_i)) + log2 n_cores > 0`, i.e. iff **H_i < n_cores**.
At depth 10 (n_cores = 29,438, so +14.85 bits per extra target):

| target | H = ρ·W | log2(1/H) | net bits | | target | H = ρ·W | net bits |
|---|---|---|---|---|---|---|
| r_p_e † | 8.71e-06 | 16.81 | **31.65** | | ckm_lambda | 1,987 | 3.89 |
| a_e | 5.86e-05 | 14.06 | **28.90** | | koide_Q_down | 2,051 | 3.84 |
| alpha_em_inv_0 | 8.55e-05 | 13.51 | **28.36** | | r_t_b | 4,362 | 2.75 |
| r_n_p † | 2.99e-04 | 11.71 | **26.55** | | r_b_tau | 4,761 | 2.63 |
| r_mu_e | 1.19e-02 | 6.39 | **21.24** | | alpha_s_MZ | 4,898 | 2.59 |
| a_mu | 9.88e-02 | 3.34 | 18.19 | | pmns_sin2_13 | 1.52e+04 | 0.95 |
| r_tau_e | 32.99 | −5.04 | 9.80 | | pmns_sin2_23 | 2.09e+04 | 0.49 |
| alpha_em_inv_MZ | 39.38 | −5.30 | 9.55 | | pmns_sin2_12 | 2.61e+04 | 0.17 |
| sin2_thetaW_MZ | 85.53 | −6.42 | 8.43 | | koide_Q_up | 902.6 | 5.03 |
| | | | | | higgs_lambda | 1,132 | 4.70 |

† corrected direct-CODATA window. Every pool target is positive-value, but they span **29 bits** —
**k is the wrong statistic** (§7d).

**The maximal legitimate independent sets** (holdouts excluded; {a_e, α⁻¹}, {α⁻¹(0), α⁻¹(M_Z)}
banned; a_mu conditional):

* **k=2: {a_e, r_p_e}** — window-bits sum **66.79**, interlock bits before look-elsewhere **43.15**
* **k=3: {a_e, r_p_e, r_n_p}** — window-bits sum **96.85**, before look-elsewhere **63.26**
* **k=4: {a_e, r_p_e, r_n_p, r_mu_e}** — window-bits sum **121.30**, before look-elsewhere **78.06**
* legitimate subset counts: **k=2 → 167, k=3 → 905, k=4 → 3,395, k=5 → 9,373**

If sin2_thetaW_MZ is carved out as the holdout, use the same sets (it is in none of them) and
score its out-of-sample prediction at 11.91 window bits.

---

## 5. The exact bits threshold a survivor must clear

```
bits(T,D) =   Σ_{i∈T} log2( 1 / (ρ_i(D)·W_i) )          [ per-target content, LOCAL density ]
            + (k−1)·log2 n_cores(D)                      [ the payoff for sharing one core   ]
            − [ 5.16·(k−1) − 3.88 ]                      [ concentration penalty M(T), D=8   ]
            − 0.640·(k−1)·(D−8)                          [ its measured depth growth, G1     ]
            − log2( N_sets(k) · N_depths )                [ look-elsewhere over sets & depths ]
            − 1.0                                        [ measured model mis-calibration    ]

ρ_i(D) = ρ_i(10)·3.847^(D−10)          n_cores(D) = 29,438·4.460^(D−10)
W_i    = 2·σ_i/|t_i|  (the search's own 1-σ predicate)

PASS  iff  bits(T,D)  ≥  log2(20) = 4.32          ( ⇔ family-wise E_chance ≤ 0.05 )
```

The **−1.0 bit** term is not a fudge: the exact per-core model under-states the measured
coincidence rate by a median 1.21× and at most 1.56× (§3.3), so one bit covers the worst measured
case. The closed form itself already errs high by 1.18×, which is left uncredited.

**Recommended operational margin: require bits ≥ 14.3** (i.e. `E_chance ≤ 5e-5`, a 10-bit buffer
on top of the 4.32 statistical threshold) before anything is called a survivor. Justification: the
G1 depth extrapolation carries a measured range 1.19–1.86 per depth, which is ±1.3 bits/depth at
k=3 — a 10-bit buffer absorbs ~8 depths of extrapolation error.

**Do NOT use `PASS_BITS = 10` on `_bit_cap`** — the cap is 1 bit inflated (§1) and it is a
per-target precision cap, not a look-elsewhere threshold.

**Optional strictness dial.** Gate C's `n_free_in_interlock ≤ 1` corresponds to a stricter core:
level L2 (skeleton + free-germ key + forced net exponents; only the free germ's net exponent varies
per target) has **32,686,128** cores with ~6.3 dressings each, versus L1's 29,438 × 5,941. Requiring
L2 gains `(k−1)·10.12` bits (core ratio 32,686,128/29,438 = 1,110.3) — but M(T) at L2 was **not** measured for tight sets, so the spec's
arithmetic uses L1 (the conservative choice). Measured L2 fact: the maximum number of distinct
targets on one L2 core at depth 10 is **4** (2 cores), versus **11** at L1 (32 cores).

---

## 6. Depths worth searching

Bits for the best legitimate sets (direct-CODATA windows, `min_tol` lowered; `N_depths = 9`):

| set | D=10 | D=12 | D=14 | D=16 | D=18 | D=20 | D=22 | **D_max** |
|---|---|---|---|---|---|---|---|---|
| {a_e, r_p_e} | 31.6 | 26.9 | 22.1 | 17.4 | 12.6 | 7.9 | 3.2 | **21.5** |
| {a_e, r_p_e, r_n_p} | 49.3 | 43.7 | 38.1 | 32.5 | 26.9 | 21.3 | 15.7 | **26.1** |
| {a_e, r_p_e, r_n_p, r_mu_e} | 62.2 | 55.7 | 49.3 | 42.8 | 36.4 | 29.9 | 23.5 | **27.9** |

Reachable-today variants:

| window regime | {a_e,r_p_e} @D10 | D_max | {a_e,r_p_e,r_n_p} @D10 | D_max |
|---|---|---|---|---|
| as committed (propagated σ) | 27.0 | 19.6 | 44.1 | 24.2 |
| direct CODATA, `min_tol=1e-10` clamp | 29.1 | 20.4 | 46.7 | 25.2 |
| direct CODATA, `min_tol=1e-11` | 31.6 | 21.5 | 49.3 | 26.1 |

**Single-target ceilings with the LOCAL density** (E* = 0.05/19 = 2.63e-3):
a_e **12.8**, α⁻¹(0) **12.5**, r_p_e **11.9**, r_n_p **11.3**, r_mu_e 8.9, a_mu 7.3, everything
else ≤ 3.0 (nine targets are already **negative**, i.e. uninformative at any depth).

**Depth plan.**

1. **Depths 3–10 are done and are a 1-σ exhaustive null.** Say "1-σ": `grind` hits at 1.000σ while
   `run_atomos.py:1149` pre-gates at 3σ (`card.within_2sigma or card.rel_error < measurement_tol(target)*3`).
   Pick ONE convention before the interlock campaign; a 3σ predicate costs 1.58 bits per target.
2. **Depths 11–14 are the high-value zone.** k=2 buys **8.7** depths past the single-target ceiling, k=3 buys **13.2**, k=4 buys **15.1**; per-depth chance growth is only 2.37–3.22 bits, while the available window bits are
   fixed. Every depth from 11 to 14 remains ≥ 38 bits for k=3 — deep in the informative regime.
3. **Depths 15–21 stay informative for k≥3 but the marginal return falls.** Prefer *more sets at
   depth 11–14* over reaching depth 19+: the same compute buys more legitimate k=3 sets, and each
   extra depth costs 2.8 bits at k=3 for free.
4. **Past D≈26–28 nothing is informative even at k=4.** Stop there, regardless of compute.
5. **The single most cost-effective change is not depth at all:** lower `min_tol` to 1e-11 and adopt
   the direct CODATA ratio windows — that is +2.52 bits on {a_e,r_p_e} and +1.06 depths of ceiling,
   for one line of code.

---

## 7. Traps to reject

**(a) Gate B credits a CANCELLED forced germ.** The project's own committed depth-6 "tightest hit"
`(((((c / c) / 3) * sqrt(8pi/3)) / sqrt(8pi/3)) * 2)` rebuilds to **exactly 2/3**: its kernel germ
has net exponent **0** and its measured-leaf skeleton is `c/c = 1`. The **real** `gate.forced_kernel_detector`
returns `passed=True`, `forced_factors=[Ngen_3, a0_kernel_8pi3]`, `n_free_params=1`. Gate B credits
*syntactic presence*, not load-bearing use — and on the enumerated path it is a constructive
tautology (the germ layer emits both forced germs plus exactly one free germ by construction, and
`coeff.target_value is None` makes the reproduction check vacuous).
**Interlock requirement: NET EXPONENT ≠ 0 on both forced germs, and the measured-leaf skeleton must
not evaluate to a pure rational.** Enforce it in the enumerator, not in a post-hoc filter.

**(b) Two windows in two drivers.** 1σ in `grind`, 3σ in `run_atomos.py:1149`. Fix to one.

**(c) The holdout is void, twice over** (§4.2). Reject any read-out rule of the form
"report the r_tau_mu out-of-sample σ; interesting iff σ < 2" — `BITS_RULE.py`'s JACKPOT rule says
exactly this, and r_tau_mu is a one-DIV monomial of two searched targets, so a survivor that fits
r_tau_e and r_mu_e passes it automatically. Likewise "Koide Q passing" is worth **0.00** bits given
the two lepton ratios.

**(d) Counting targets instead of bits.** A k=3 interlock on the three PMNS angles is worth
**−22.2 bits**; the k=2 {a_e, r_p_e} is worth **+43.2**. Never accept a k-count.

**(e) Multiplying windows over a flat core count.** Under-states chance by **11.6×** in the
unsaturated regime and by **637×** at k=8 (§3.1). The M(T) term is mandatory.

**(f) `N(D) = 30^(D−4)`, and any conclusion resting on its slope.** Both of `BITS_RULE.py`'s
headline claims are artefacts: "the two most precisely measured numbers in physics are NOT enough
at depth 18" and "each depth costs 4.9 bits". Real cost is 2.11 bits/depth of value multiplicity
and 2.37–3.22 bits/depth of interlock chance.

**(g) Building an interlock on loose targets.** Beyond their low bit content, 259 small monomials of
other pool targets land inside the 13 loose windows (100 inside pmns_sin2_12 alone), so a loose
target is nearly free given two others.

**(h) Interlocking a_e with α⁻¹, or α⁻¹(0) with α⁻¹(M_Z), or a_mu with either** (§4.3). And note
that {a_e, r_p_e} and {α⁻¹, r_p_e} are informationally the *same* interlock — do not count both as
independent discoveries, and require any survivor claiming a_e to be checked against QED.

**(i) Dropping r_t_b (or any target) for high ρ** (§4.4). Over-strict; the correlation is a bonus
test, not a disqualification.

**(j) Reading anything into the depth-8/9 "clean nulls" as holdout-clean.** Those runs swept 21
targets including both holdout keys (5 and 14 hits on them respectively); only depth 10 is
holdout-clean, and even there the holdout was void.

---

## 8. Open, and honest about it

* **M(T) for the tight sets is measured at depth 8**, then carried forward with G1 = 1.558/depth
  (range 1.19–1.86 from 16 pairs, validated out of sample on 19 triples at median 1.10 but with an
  upper outlier at 2.48). At depth 18 that is a ±1.3 bits/depth uncertainty at k=3 — the reason for
  the recommended 10-bit operational margin. Measuring M(T) directly at depth 10 for the tight sets
  is not possible from the committed artifacts (zero hits there); it would require retaining
  widened-window records, which is a cheap change to `_target_windows`.
* **The tight-target validation used common ln half-widths at the tight targets' LOCATIONS**, not
  their real windows (which produce zero coincidences at depth 8 by construction). The extrapolation
  from h ≈ 1e-4 down to W ≈ 1e-10 is 6 decades of window, over which the value set is measured to be
  locally log-uniform (band-width robustness 1.000–1.008 for ±0.05…±2.0 ln), but it is an
  extrapolation.
* **`n_cores` beyond depth 10 is extrapolated** at B_core = 4.460 from the exactly-solved layer
  counts n_skel(1..6); the per-depth ratios are 4.44, 4.55, 4.37 (flat, not declining), so this is
  the best-supported of the three extrapolations.
* **Reference constants typed from literature** (CODATA-2022 direct ratios, the AHKN QED
  coefficients, a_mu's hadronic uncertainty, Δα_had) are cross-checked against the repo's own
  α⁻¹ and a_e entries, which match CODATA to every digit. The load-bearing conclusions —
  m_p/m_e's window is 24.5× too wide not 24,459×; a_e is not independent of α; both holdouts are
  void — are robust to those inputs at the stated precision.
