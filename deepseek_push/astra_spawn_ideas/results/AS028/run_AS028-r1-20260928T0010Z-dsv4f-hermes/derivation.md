# AS028 — RAR deep expansion with stable evaluation

**Run:** `run_AS028-r1-20260928T0010Z-dsv4f-hermes` · **Worker:** Hermes subagent (deepseek/deepseek-v4-flash-0731 via openrouter) · **Task SHA-256:** `e6411e3f77a13a78d22ce328acbcb07184bee40b672896b7cb266aab32a9025b`

Source hashes verified against `deepseek_push/astra_spawn_ideas/SOURCE_MANIFEST.json` before computing:
README.md `91a5fac4…`, FRIED_CHICKEN_SPEC.md `98d9149f…`, peer_review_2026_09_26/README.md `521d9ac3…` — all match the pinned manifest. Framework base taken from FRAMEWORK_CONTRACT.md: `a0 = kappa·c·sqrt(G·rho_Lambda)` with **kappa = 1/2 ADOPTED input**, `r_M = sqrt(G·M_b/a0)`, `v_flat⁴ = G·M_b·a0`, `G = 6.67430e-11 m³ kg⁻¹ s⁻²`, `c = 299792458 m/s`.

---

## 1. Precise claim, symbols, assumptions

**Symbols.** `B = g_bar = g_N > 0` (baryonic/Newtonian acceleration), `y = B/a0` (dimensionless), `s = sqrt(y)` (used throughout; the deep variable), `g = a0·x`, `x = g/a0 = y·nu_RAR(y)` (total acceleration in a0 units), `h_RAR(y) = y·(nu_RAR(y) − 1)` (phantom-boost fraction).

**Claim (probably true, supported by this run).** On the RAR branch, `nu_RAR(y) = 1/(1−exp(−sqrt(y)))` admits the deep expansion

```
nu_RAR(y) = 1/sqrt(y) + 1/2 + sqrt(y)/12 − y^(3/2)/720 + y^(5/2)/30240 + O(y^(7/2)),   y → 0⁺,
```

with exact coefficients `{1/2, 1/12, −1/720, 1/30240, …}` (Bernoulli family, `s/(1−e^{−s}) = Σ B_k s^k/k!`, `B_1 = +1/2`), convergence radius `|s| < 2π` ⇔ `y < 4π² = 39.4784…`, leading neglected term (after the `y^(5/2)` term) `−s⁷/1209600 = −y^(7/2)/1209600` absolute (relative to the leading term `1/s`: `−s⁸/1209600 = −y⁴/1209600`). The **numerically stable evaluation** over the full positive domain

```
nu_stable(y) = −1/expm1(−sqrt(y))        (identity: −(e^{−s} − 1)⁻¹ = (1 − e^{−s})⁻¹)
            = e^s/(e^s − 1)               (certified algebraic rearrangement)
```

agrees with a 70-digit reference to ≤ 2.04e-16 relative error on the full grid `y ∈ [10⁻¹⁶, 10⁸]` (241 points), whereas the naive form `1/(1 − exp(−sqrt(y)))` loses accuracy by catastrophic cancellation in the deep regime: max relative error 3.57e-9, violating a 1e-14 bar at **105 of 241** grid points (`y ≲ 10⁻⁸` region and below).

**Assumptions / framework inputs.** kappa = 1/2 adopted (not derived here); G, c measured constants; RAR is the declared branch for conclusions; MONO (operative filtered continuation) enters only as comparison; Q, MU2, EXP are distinct branches and are *not* used in any conclusion. Both a0 footings (canonical 9.3619e-11, alternative 1.1279e-10 m/s²) carried separately — see §7.

---

## 2. Derivation

**Step 1 — series coefficients (exact rationals).** Let `P(s) = (1 − e^{−s})/s = Σ_{k≥0} (−1)^k s^k/(k+1)!`. Then `nu = 1/(1−e^{−s}) = s⁻¹·Q(s)` with `Q = 1/P` as a formal power series, computed exactly by the recursion `Q[0]=1`, `Q[n] = −Σ_{k=1..n} P[k]·Q[n−k]` (Fraction arithmetic, 121 coefficients):

```
Q = 1 + s/2 + s²/12 + 0·s³ − s⁴/720 + 0·s⁵ + s⁶/30240 + 0·s⁷ − s⁸/1209600 + 0·s⁹ + s¹⁰/47900160 + …
```

Independently reproduced via the standard Bernoulli recurrence `Σ_{k=0}^{m} C(m+1,k) B_k = 0` with `B_1 = +1/2` and `Q_k = B_k/k!` — exact agreement on all checked orders (verify log). The first three nonzero terms beyond the leading `1/s`: `1/2`, `s/12`, `−s³/720` (then `+s⁵/30240`), satisfying the task's "at least three nonzero deep terms".

*Scale/sign/units check.* Everything dimensionless in `y`, `s`; the only dimensional maps are `B = a0·y` and `g = a0·y·nu` (m/s²), applied per footing in §7. No hidden coefficients: the 1/2 in front of the constant term is the `B_1 = +1/2` Bernoulli convention, the same convention that makes `x/(1−e^{−x}) = 1 + x/2 + …`; the signs alternate every even power as fixed by `Q[4] = −1/720`, `Q[6] = +1/30240`, `Q[8] = −1/1209600`.

**Step 2 — convergence domain.** `s/(1−e^{−s}) = Σ Q_k s^k` is the generating function `Σ B_k s^k/k!`, which extends meromorphically to ℂ with poles exactly at `s = 2πik`, `k ∈ ℤ\{0}` (zeros of `e^{−s} − 1`); hence radius of convergence `|s| < 2π`, i.e. **`y < 4π² = 39.4784176…`**. Within `0 < y` the series is absolutely convergent (at `y = 4π²·(1−ε)` convergence is arbitrarily slow — the honest domain statement, verified numerically below).

**Step 3 — stable evaluation.** The naive form evaluates `1 − exp(−s)`: for `s → 0` the subtraction loses about `eps/s` relative digits (`exp(−s)` rounding error ~1.1e-16 absolute is amplified by `1/s`). The stable forms

```
−1/expm1(−s)   and   e^s/(e^s − 1)
```

have no cancellation: `expm1(−s)` is relatively accurate for tiny arguments by definition, and `e^s − 1 ≈ s + s²/2` near 0. The identity `−1/expm1(−s) = 1/(1−e^{−s}) = e^s/(e^s−1)` (with the defining `expm1(x) = e^x − 1`; the exp-only equality is Lean-certified, §6) is exact; the series is then an additional, independent representation on `0 < y < 4π²`.

---

## 3. Controls and numerical validation (actual outputs)

**Grid.** `y = 10^k`, `k = −16 … 8` step 0.1 → **241 points** (the mandated diagnostic grid `k = −10 … 8` is a subset) + an extra deep tail `y ∈ [10⁻¹⁶, 10⁻¹⁰]`. Reference: 70-digit Decimal `1/(1−e^{−s})` (Decimal.exp is accurate for tiny arguments; subtraction at 70 digits is loss-free).

**C1 — negative control (naive cancellation), PASSES-DESIGN (naive fails, stable passes):**

| y | naive rel err | stable rel err |
|---|---|---|
| 1e-16 | 1.077e-09 | 1.678e-16 |
| 1e-14 | 4.864e-10 | 9.740e-17 |
| 1e-12 | 1.586e-11 | 9.980e-18 |
| 1e-10 | 5.731e-13 | 1.534e-17 |
| 1e-08 | 1.353e-14 | 7.108e-17 |

Max over all 241 points: naive **3.57e-09** (fails the 1e-14 bar at 105 points), stable **2.04e-16** (passes everywhere, incl. the whole deep regime ≤ 1e-4 where naive is 3.57e-9). The control is genuinely capable of failing and **did fail spuriously on the first attempt** when the grid builder (`range(-16, 81)` instead of `range(-160, 81)`) produced only `y ≥ 10⁻¹·⁶` — the naive form "passed" because the deep points were missing; fixing the grid made the control trip exactly as physics requires. This is the strongest evidence the control is wired correctly.

**C2 — series accuracy on its practical domain, PASS:** 120-term series (exact rational coefficients) vs reference: max relative error **1.04e-16** for `y ≤ 10`; on `y < 0.97·4π²` the error grows (max 2.6e-7, near-boundary diagnostic).

**C3 — radius boundary probe, PASS:** at `y = 39.0 / 39.4 / 39.478` the 120-term series errors are 7.6e-2 / 0.141 / 0.159 (degradation inside the radius, convergence too slow to use), `|Q₁₂₀|·s¹²⁰` at the radius = **1.999** (no decay of the 120th term), and beyond the radius (`y = 50`) the term magnitude is 2.87e6 — divergence. Expressed in s: terms only decay when `s < 2π`.

**C4 — limiting regimes, PASS:** `nu(10⁴) − 1 = 3.72e-44` (≈ `e^{−100}`; Newtonian `g → B` on RAR) — relative residual to 1: 3.72e-44 < 1e-30. Deep: at `y = 10⁻¹⁶`, `sqrt(y)·nu(y) = 1 + 5.0000e-9·(1 ± 1e-9)` with residual to `1 + s/2` of 1.88e-17 — the first two deep terms `1/s + 1/2` reproduce the reference to 1e-17 (next correction scale `s²/12 ≈ 8.3e-18`). These are consistency checks at the level of exact identities plus finite numerical agreement — the *infinite* limits `y→∞: nu→1`, `y→0⁺: sqrt(y)·nu→1` follow from `1/(1−e^{−s})` continuity in s at 0/∞; stated as standard calculus, not overclaimed.

**C5 — independent representation (substitution into the defining relation), PASS:** `(1 − e^{−s})·nu_series − 1` ≤ 1e-37 for `y ≤ 10` (e.g. −2.02e-37 at `y = 10`, 1e-69 at `y = 1`, 2.06e-63 at `y = 10⁻¹⁶`); at `y = 30, 39` the residual degrades to −1.1e-8, −7.6e-2 exactly as the radius analysis predicts. Secondary independent check (verify script): the rearranged evaluation `nu = 1 + 1/(e^s − 1)` satisfies the defining relation to 4.1e-62 over 35 strided points.

**C6/C7 — MONO splice landmarks and branch distinction, PASS:** see §5.

All seven checks pass; bounds enforced in-script: wall 0.062 s (budget 120 s), RSS 13.9 MB (budget 512 MB), 1 thread by construction.

---

## 4. Step-by-step execution record

1. Read the branch equations from FRAMEWORK_CONTRACT.md; wrote the claim/dictionary/assumptions (§1).
2. Derived ≥ 3 nonzero deep terms with exact rational coefficients, implemented `expm1`-based evaluation; the cancellation-error bound (naive vs 70-digit reference) computed over the grid (C1).
3. All scale factors/signs/units shown (§2,7); leading neglected term and its domain stated (`−y^{7/2}/1209600` on `y < 4π²`).
4. Independent check via a different representation: substitution `(1−e^{−s})·nu_series = 1` (C5) plus a fully separate verify script (Bernoulli-recurrence coefficients, `1 + 1/(e^s−1)` rearrangement, Newton landmarks, dense max scan — AS028_verify.py, VERIFY_OK).
5. Negative control runs and fails as designed (C1, including its first spurious pass before the grid fix, preserved as a failed attempt, §8); the surviving statement and the first transfer implication are §9.

---

## 5. MONO splice comparison (operative branch, comparison only)

MONO construction (contract): `h_RAR(y) = y·(nu−1)`, `h'_mono = max(h'_RAR, δ·h_p/(y+y_p))` with δ = 0.05, continuous splice at `y*`, `h_mono(y) = h_RAR(y*) + δ·h_p·ln((y+y_p)/(y*+y_p))` for `y > y*`, `nu_mono = 1 + h_mono/y`.

Landmarks quoted in the task (`y* = 2.337412, y_p = 2.53964, h_p = 0.647610`) **independently re-derived** by bisection (main run) and by Newton on the closed-form derivative `h'(y) = (e^s(2−s) − 2)/(2(e^s−1)²)` (verify run) — agreeing to ≤ 4.1e-7 (y*), 1.7e-6 (y_p), 2.4e-7 (h_p); the splice condition `h'_RAR(y*) = δ·h_p/(y*+y_p)` holds to −4.3e-17, and `h_mono(y*) = h_RAR(y*)` exactly (log term = 0, residual 0.0).

| y | nu_RAR | nu_MONO | Δnu abs | Δg/a0 = h_MONO−h_RAR |
|---|---|---|---|---|
| 1.1687 (y*/2) | 1.51339356695… | identical | 0 | 0 |
| 2.337412 (y*) | 1.27678490854… | identical | 0 | 0 |
| 2.53964 (y_p) | 1.25500080243… | 1.25526292718… | 2.62e-4 | 6.66e-4 |
| 4.0 | 1.15651764275… | 1.16411472517… | 7.60e-3 | 3.04e-2 |
| 10.0 | 1.04420017869… | 1.06775390177… | 2.36e-2 | 2.36e-1 |
| 100.0 | 1.00004540199… | 1.00745581931… | 7.41e-3 | 7.41e-1 |
| 1e4 | 1.00000000000… | 1.00008938958… | 8.94e-5 | 0.894 |

Max |Δnu| on the splice neighbourhood `[y*, y*+3.9] ⊇ [y*, 2y_p]`: **0.01706**; global max on `(y*, 10⁴]`: **0.02475 at y ≈ 13.7** (dense 20k-point log scan).

**Branch-distinctness statement (criterion B, the task's own principle).** Both branches share the Newtonian asymptote `nu → 1` (so `g → B`), but not the approach: on RAR, `h_RAR(y) = y/(e^s−1) ≈ y·e^{−√y} → 0` exponentially (3.7e-40 at y = 10⁴); on MONO, `h_mono(y) ≈ h_RAR(y*) + δ·h_p·ln y → ∞` logarithmically, so `nu_mono − 1 = O(ln y / y)` and at `y = 10⁴` the two kernels differ by `Δg ≈ 0.894·a0` (~9.4e-11 m/s² canonical). **Matching one asymptote does not make the kernels equivalent** — here they are different functions on `(y*, ∞)` with different approach rates and an a0-scale accumulated difference. This is a property of the contract's continuation formula (log tail), reported as measured comparison; the RAR task's conclusions use only the RAR branch.

---

## 6. Lean certificate

File: `AS028_rar_deep_expansion_certificates.lean` — compiled with `lake env lean` (mathlib v4.34.0-rc2, project `fable_independent_2026/lean_2026`), **exit 0, zero `sorry`, axioms = {propext, Classical.choice, Quot.sound}** on all theorems. Mathlib v4.34 has no `Real.expm1`, so the certified "equivalence of the two stable forms" is the exp-only rearrangement (the defining expm1 identity `expm1(x) = e^x − 1` makes `−1/expm1(−s)` literally equal to them):

1. `nu_stable_rearrangement`: `1/(1 − e^{−s}) = e^s/(e^s − 1)` for `s ≠ 0`.
2. `inv_stable_rearrangement`, `h_RAR_rearrangement`: `y·(1/(1−e^{−s}) − 1) = y/(e^s − 1)`.
3. `deep_series_expansion_terms` (+ `…_in_y` with `s = sqrt y, y > 0`): the five-term deep form `(1/s)(1 + s/2 + s²/12 − s⁴/720 + s⁶/30240) = 1/s + 1/2 + s/12 − s³/720 + s⁵/30240` is an exact algebraic identity.
4. `series_core_algebraic_core`: `P₈(s)·Q₇(s) = 1 + s⁸·(−1/518400 − 11/7257600·s − 1/87091200·s³ + 1/152409600·s⁴ − 1/1219276800·s⁵)` where `P₈ = Σ₀⁷(−1)^k s^k/(k+1)!` is the 8th-order Taylor polynomial of `(1−e^{−s})/s` — i.e. the first eight Taylor coefficients and the seven deep-series coefficients are mutual inverses through order 7 (the exact algebraic core of the inversion step; the exponential's Taylor coefficients and all convergence/truncation estimates are analytic inputs, numerically validated, not Lean statements).

The transcendental identities (`1 − e^{−s} ~ s`, radius 2π, full Bernoulli series) are deliberately NOT claimed as Lean theorems — per task, only exact algebraic statements are certified.

---

## 7. Both footings and dimensional examples (SI)

Dimensionless claim applies identically to both footings (same `nu(y)` curve); dimensional map `g = a0·y·nu(y)`, `a0 = kappa·c·sqrt(G·rho_Lambda)`, kappa = 1/2 **held fixed → rho_Lambda changes** with the footing (ratio = (a0_alt/a0_can)² = 1.45149…):

| quantity | canonical | alternative |
|---|---|---|
| a0 (m/s²) | 9.3619e-11 | 1.1279e-10 |
| rho_Lambda = 4a0²/(Gc²) (kg/m³) | 5.8444e-27 | 8.4831e-27 |
| eps_Lambda = rho_Lambda·c² (J/m³) | 5.2527e-10 | 7.6242e-10 |
| Λ = 32π a0²/c⁴ (m⁻², Einstein G = scale G) | 1.0908e-52 | 1.5833e-52 |
| r_M(10¹¹ M_sun) (kpc) | 12.202 | 11.117 |
| v_flat(10¹¹ M_sun) (km/s) | 187.75 | 196.70 |
| g at y=1e-6 (m/s²) | 9.3666e-14 | 1.1285e-13 |
| g at y=1 (m/s²) | 1.4810e-10 | 1.7843e-10 |
| g at y=1e2 (m/s²) | 9.3623e-09 | 1.1280e-08 |
| g at y=1e4 (m/s²) | 9.3619e-07 | 1.1279e-06 |

(The `r_M`, `v_flat` values replicate the framework's published landmarks at 1e11 M_sun, e.g. AS019's 12.202/11.117 kpc and 187.75/196.70 km/s — same-adopted-inputs consistency.)

---

## 8. Failed attempts (preserved honestly)

1. **Grid bug (numerical, caught by the negative control).** `ks = [k/10 for k in range(-16, 81)]` yields k/10 ∈ [−1.6, 8.0], so the "deep" grid ended at y = 10⁻¹·⁶: the naive form then showed max error 3.2e-16 and the control did NOT trip. The detail rows (computed on the intended powers of ten) disagreed with the loop maxima, exposing the bug. Fixed to `range(-160, 81)` → 241 points down to y = 1e-16; after the fix the control trips at 105 points as physics requires. (First run.log overwritten by the final run; the diagnosis is preserved here and in run history.)
2. **Decimal ⊗ float TypeError** in the splice-table rows (`y * (m − r)` with float·Decimal); fixed by explicit `Decimal(y)` conversion (in-session edit, not preserved as a file).
3. **60-term series check overclaimed** at `y ≤ 0.97·4π²` (observed 2.0e-4 max error near the boundary — the series genuinely degrades toward the radius; a 60-term cutoff was only ~1e-10 at y = 19.7, consistent with the term-decay analysis `|Q_{2n}| ≈ 2(2π)^{−2n}`). Re-scoped: accuracy claim on `y ≤ 10` with 120 terms (1.04e-16), near-radius degradation reported as the C3 boundary probe.
4. **Lean v1:** `Real.exp_eq_one_iff.mp` dot-notation resolution failed (unknown constant) → replaced by `rw [Real.exp_eq_one_iff] at h`; `sub_ne_zero.mpr` direction, `exp ≠ 0` vs `≠ 1`, commuted multiplication order, and a stray trailing `ring` — all fixed in the final file (lean_check.out, exit 0).

---

## 9. Strongest surviving statement, closure implication, next step

**Strongest statement.** For all `y ∈ (0, 4π²)`: `nu_RAR(y) = Σ_{k≥0} Q_k y^{k/2}` with the exact Bernoulli coefficients `{Q₀=1, Q₁=1/2, Q₂=1/12, Q₄=−1/720, Q₆=1/30240, Q₈=−1/1209600, …}`, and the numerically stable evaluation `−1/expm1(−√y)` (= `e^s/(e^s−1)`) reproduces `1/(1−e^{−√y})` to ≤ 2e-16 relative accuracy over `y ∈ [10⁻¹⁶, 10⁸]` (241-point grid; naive form fails a 1e-14 bar at 105 points). Branch comparison on the MONO splice: `nu_RAR ≠ nu_mono` on `(y*, ∞)` with `max|Δnu| = 0.0248` (at y ≈ 13.7) and `Δg/a0 = 0.894` at y = 10⁴, despite both approaching the Newtonian asymptote — matching one asymptote does not identify the kernel. (RAR is the declared branch; the MONO numbers are comparison evidence for criterion-B branch distinctness only.)

**Closure implication.** This seed feeds the operative gate "constitutive kernels and branch fidelity" (group A02): exact, stable evaluation of the RAR response on `(0, ∞)` and explicit quantification of the RAR-vs-MONO difference on the splice neighbourhood is the missing *numerical prerequisite* for any transfer of RAR kernel statements to the filtered MONO target — per the contract, that transfer is NOT made here (no filter, no field equation, no action).

**Next unresolved implication (first bridge needed before transfer).** The RAR deep series and its stable evaluation live on the *unfiltered, spherical, algebraic* response `g = B·nu(B/a0)`; the operative target is `Δu = 4πGρ_b` with `S = exp[(ξ²/2)Δ]` and `div[ nu_mono(|∇Su|/a0)·∇Su ]`. The missing bridge: **derive how the deep series truncation error and the RAR-vs-MONO difference (≤ 0.025 in nu, ≤ 0.9 a0 in g at large y) propagate through the heat filter S and the divergence equation — i.e., bound ‖(nu_RAR − nu_mono)(|∇Su|/a0)·∇Su‖ in the filtered field equation**, which requires the filtered MONO's metric/measure/domain specification (an open dependency, not supplied by this task).

**Suggested follow-up (child candidate, not dispatched — no runner spawn used).** `AS028.C01 — filtered-transfer error bound`: with the same action source, kernel pair {RAR, MONO}, gate A02/CORE, assume the filter S as an L²-smoothing operator with known kernel bounds, prove/certify an a priori bound on `‖(nu_RAR(y) − nu_mono(y))·y‖` over the deep+turning region using the exact series remainder `−y^{7/2}/1209600` and the log-tail bound `δ·h_p·ln((y+y_p)/(y*+y_p))`, and quantify the resulting difference in the spherical filtered field equation. Duplicate scan: no manifest/claims entry covers filtered RAR-vs-MONO error transfer (FGF queue and AS manifests checked: none).

---

*Proof-only exception honored: no fabricated numbers; every figure above is from `raw_output.json`, `run.log`, `verify.log`, or `lean_check.out` in this directory.*
