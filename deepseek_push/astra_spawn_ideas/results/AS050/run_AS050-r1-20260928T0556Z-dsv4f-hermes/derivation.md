# AS050 — Stable evaluation of the RAR deep x

**Run:** `run_AS050-r1-20260928T0556Z-dsv4f-hermes` · **Worker:** Hermes subagent (deepseek/deepseek-v4-flash-0731 via openrouter) · **Task SHA-256:** `03ac57f374e3c5b8bda9b455d64d668435e39334d098c013c99924266fdf4578`

> **Spec provenance (important).** The dispatched file path `deepseek_push/astra_spawn_ideas/AS050_stable_evaluation_of_the_rar_deep_x.md` does **not** exist in the repository; the catalog AS050 (`AS050_a_branch_specific_primitive_cannot_fix_its_zero.md`, `db6efad6…`) is a different, undispatched topic. `claims/AS050.json` records AS050 as reserved/dispatched by the orchestrator at 2026-09-28T05:42:53Z with result base `results/AS050/`, matching this dispatch. The executed specification is therefore the dispatch text itself, captured verbatim in `reference/AS050_dispatch_spec.md` (hashed as `03ac57f3…`). Its closest catalog sibling is AS028 (`AS028_rar_deep_expansion_with_stable_evaluation.md`), whose run `results/AS028/run_AS028-r1-20260928T0010Z-dsv4f-hermes` is cited ("cf. AS028") and cross-checked here.

Source hashes verified against `deepseek_push/astra_spawn_ideas/SOURCE_MANIFEST.json` (all match the pinned manifest): README.md `91a5fac4…`, FRIED_CHICKEN_SPEC.md `98d9149f…`, peer_review_2026_09_26/README.md `521d9ac3…`. Git HEAD `bfa3207e13140faee237e1f0e339cad8b6293f62`. Framework base per FRAMEWORK_CONTRACT.md: `a0 = kappa·c·sqrt(G·rho_Lambda)`, **kappa = 1/2 ADOPTED input**, `G = 6.67430e-11 m³ kg⁻¹ s⁻²` (= G_N; G_bare, G_cosmo kept separate), `c = 299792458 m/s`.

---

## 1. Precise claim, symbols, assumptions

**Symbols.** `B = g_bar = g_N > 0`, `y = B/a0` (dimensionless), `s = sqrt(y)` (deep variable), `x = g/a0 = y·nu_RAR(y)` with `nu_RAR(y) = 1/(1 − exp(−sqrt(y)))` — i.e. the RAR deep-branch total acceleration **x = y/(1 − exp(−√y))**, the object of this task. `h_RAR(y) = y·(nu_RAR − 1)` (phantom boost). `Q(s) = s/(1 − e^{−s}) = Σ q_k s^k` (Bernoulli generating function) so that `x/s = Q(s)`.

**Claim (supported by this run, on the RAR branch, spherical unfiltered algebraic response).**
1. The two evaluation forms are algebraically identical, `x = y/(1 − e^{−s}) = y·e^s/(e^s − 1)` (multiply numerator and denominator by `e^s`, `e^{−s}·e^s = 1`; Lean-certified), and `x = −y/expm1(−s)` by the defining `expm1(x) = e^x − 1`.
2. **In fp64 the "multiply by exp(+√y)" form is *not* stable** — it fails the 1e-14 relative bar at 118/121 grid points on the mandated deep range `y ∈ [1e-16, 1e-4]` (max rel err 1.11e-08, worse than naive at the deep end), because `e^s − 1` is again a cancellation of a quantity ~1 against 1, with absolute rounding error ~ulp(1) amplified by 1/s. The genuinely stable forms are `−y/expm1(−s)` (max rel err 2.43e-16, 0 failures) and the **expm1-free rearrangement**, the deep series route `x/s = 1 + s/2 + s²/12 − s⁴/720 + …` (max rel err 2.45e-16, 0 failures on the mandated range).
3. Naive form: max rel err **3.57e-09**, fails the 1e-14 bar at **105/121** mandated points (first failure at y = 7.94e-06). Guaranteed accuracy gain of expm1/series over naive: median 3.3e4×, max 5.1e8× (y = 1e-16); the exp-multiplied form gives **no** gain (median gain 0.46×: naive is sometimes more accurate than it).
4. Deep series route (cf. AS028): `x/sqrt(y) = 1 + s/2 + s²/12 − s⁴/720 + s⁶/30240 − …` with exact rational coefficients `q_k = B_k/k!` (Bernoulli family, `B_1 = +1/2` convention, odd `k ≥ 3` vanish: `{1, 1/2, 1/12, 0, −1/720, 0, 1/30240, 0, −1/1209600, 0, 1/47900160, …}`), radius of convergence `|s| < 2π ⇔ y < 4π² = 39.4784176…` (pole of `s/(1−e^{−s})` at `s = 2πi`). 120-term evaluation matches the 70-digit reference to 1.93e-16 for `y ≤ 10`; degrades toward the radius exactly as predicted (err 0.159 at y = 4π², |term₁₂₀| → 2; diverges beyond, |term₁₂₀| = 2.87e6 at y = 50).
5. Operative branch: the framework's operative target is filtered MONO; RAR is the comparison branch on which this derivation is certified. **MONO deep inherits via the splice**: the contract continuation has `h_mono(y) = h_RAR(y)` on `(0, y*]`, so `nu_mono ≡ nu_RAR` and the deep-x evaluation/series are operative for MONO on the whole deep domain `(0, y*]` — the mandated `[1e-16, 1e-4]` sits 4.37 decades below the splice point `y* = 2.337412405` (re-derived, dev 4.1e-7 from the quoted landmark; splice residual 6.1e-18). Measured with independent stable routes: max |nu_mono − nu_RAR| rel = 3.3e-16.

**Assumptions / framework inputs.** kappa = 1/2 adopted (not derived); G_N, c measured; RAR declared branch for conclusions; MONO enters only via the mandated inheritance statement (contract formula + quoted landmarks, re-derived); Q, MU2, EXP are distinct branches (criterion B), not used. Both a0 footings separate, kappa held fixed → rho_Lambda changes (§7).

---

## 2. Derivation (every intermediate factor, sign, unit)

**Step 1 — the expansion.** `x = y/(1 − e^{−s})` with `y = s²`. Multiply numerator and denominator by `e^s`:
`x = y·e^s/(e^s − 1)` (uses only `e^{−s}·e^s = 1`, valid for all real s ≠ 0). Equivalently `x = −y/(e^{−s} − 1) = −y/expm1(−s)`. Define `P(s) = (1 − e^{−s})/s = Σ_{k≥0} (−1)^k s^k/(k+1)!`; then `x/s = s·nu = s/(1 − e^{−s}) = 1/P(s) =: Q(s)`. Formal reciprocal (Fraction-exact recursion `q_0 = 1`, `q_n = −Σ_{k=1..n} p_k q_{n−k}`, 130 terms):
`Q(s) = 1 + s/2 + s²/12 + 0·s³ − s⁴/720 + 0·s⁵ + s⁶/30240 + 0·s⁷ − s⁸/1209600 + 0·s⁹ + s¹⁰/47900160 + …` — hence the dispatch's claimed route `x/sqrt(y) = 1 + s/2 + s²/12 − s⁴/720 + …` with `q_k = B_k/k!` (Bernoulli, `B_1 = +1/2` "second-Bernoulli" convention: `s/(1−e^{−s}) = Σ B_k s^k/k!`; the raw recurrence `Σ_k C(m+1,k) B_k = 0` produces `B_1 = −1/2` — the `x/(e^x − 1)` convention — and the sign flip at k = 1 is exactly the adopted generating-function convention; all other orders agree. Verified: all 130 coefficients match an independent Bernoulli route `q_k = (−1)^k·B⁻_k/k!`, verify C1.) The x-series in s is `x(s) = s·Q(s) = s + s²/2 + s³/12 − s⁵/720 + s⁷/30240 + …` (odd powers ≥ 5 absent; in y: `x = y^{1/2} + y/2 + y^{3/2}/12 − y^{5/2}/720 + y^{7/2}/30240 + …`).

**Step 2 — radius.** `Q(s) = s/(1 − e^{−s})` extends meromorphically; zeros of `e^{−s} − 1` at `s = 2πik`, k ∈ ℤ⧹{0} ⇒ nearest singularities at `±2πi` ⇒ radius `|s| < 2π` ⇒ **`y < 4π² = 39.4784176…`**. Asymptotic corroboration: `|q_{2n}|·(2π)^{2n} → 2` (measured n = 31..60 tail mean 1.999999999999993; sample n = 1..8: 3.290, 2.165, 2.035, 2.008, 2.002, 2.0005, 2.0001, 2.0000) — `|q_{2n}| ≈ 2(2π)^{−2n}`, so terms decay only for `s < 2π`.

**Step 3 — fp64 error analysis of the three forms.** Let `δ` be the absolute rounding error of the library `exp` at arguments near 1, `|δ| ≤ ½·ulp(1) = 5.55e-17`.
- Naive: `1 − e^{−s} = s·(1 − δ/s + …)` ⇒ relative error `≈ δ/s` — catastrophic as `s → 0`.
- "Multiply by e^s": `e^s − 1 = s·(1 − δ/s + …)` — the SAME conditioning `≈ δ/s`. The algebraic identity is exact; the fp64 evaluation of `e^s − 1` by subtraction re-introduces the cancellation (only `expm1` avoids it). Hence the dispatch's prescribed candidate form must be *verified*, and it verifies as **not stable in fp64** (measured below). Worst-case guarantee bar: `δ/s ≤ 1e-14` requires `s ≥ 5.55e-3`, i.e. cancellation forms cannot be *guaranteed* against the bar for `y < 3.08e-5`.
- `−y/expm1(−s)`: `expm1(−s)` is relatively accurate by construction ⇒ relative error ~ulp, forever ≤ ~2.4e-16 measured over the whole grid.
- Series: no exponential evaluation at all; truncation-controlled (exact rational coefficients). On `y ≤ 1e-4` (s ≤ 1e-2), 8 terms suffice: first neglected term `|q₈|·s⁸ = (1/1209600)·10⁻¹⁶ ≈ 8.3e-23`.

Units: everything dimensionless in y, s, x; the only dimensional maps are `B = a0·y` (m/s²) and `g = a0·x` (m/s²) with the footings of §7. No hidden coefficients: the 1/2 is `B₁ = +1/2`; signs alternate every fourth power of s (`−s⁴/720, +s⁶/30240`).

---

## 3. Controls and numerical validation (actual outputs; 70-digit Decimal reference)

**Grid.** Mandated deep range `y = 10^k`, k ∈ [−16, −4] step 0.1 → **121 points**; extended k ∈ [−16, 8] step 0.1 → 241 points; boundary probes y ∈ {1e-18, 1e-20, 1e-30, 1e-31, 1e-32, 1e-33, 1e8, 1e10, 1e-34}. Reference: 70-digit `Decimal(y)/(1 − exp(−√y))` (self-convergence to the 50-digit reference ≤ 2.8e-43 — deep-end floor ~1e-50/s, 26 orders below the fp64 statistics; verify C2).

**C1 — negative control (naive fails, stable passes), on the mandated range, bar 1e-14:**

| form | max rel err | fails 1e-14 | first (largest-y) failure |
|---|---|---|---|
| naive `y/(1−e^{−s})` | **3.571e-09** | **105/121** | y = 7.94e-6 |
| exp-multiplied `y·e^s/(e^s−1)` | **1.108e-08** | **118/121** | y = 1e-4 (top of range) |
| expm1 `−y/expm1(−s)` | 2.431e-16 | 0 | — |
| series, 8 terms | 2.454e-16 | 0 | — |
| series, 30 terms | 2.454e-16 | 0 | — |

Per-decade (k = −4 … −16), naive / exp-form / expm1 (+series) relative errors:
`1e-4: 5.47e-15 / 1.05e-14 / 1.0e-16 · 1e-5: 1.47e-15 / 1.65e-14 / 9.6e-18 · 1e-6: 3.03e-14 / 4.29e-14 / 2.2e-17 · 1e-7: 3.87e-14 / 4.58e-14 / 1.7e-16 · 1e-8: 1.35e-14 / 4.33e-13 / 4.4e-17 · 1e-9: 1.30e-12 / 2.20e-12 / 5.3e-17 · 1e-10: 5.73e-13 / 9.70e-12 / 4.8e-17 · 1e-11: 1.37e-13 / 1.24e-13 / 7.3e-17 · 1e-12: 1.59e-11 / 3.80e-11 / 2.3e-17 · 1e-13: 1.24e-11 / 2.65e-10 / 8.5e-17 · 1e-14: 4.86e-10 / 5.66e-10 / 6.7e-17 · 1e-15: 1.18e-09 / 1.20e-09 / 8.9e-17 · 1e-16: 1.08e-09 / 1.11e-08 / 2.1e-18`.

**Accuracy gain over naive (mandated range):** vs expm1: median 3.34e4×, max 5.09e8× (at y = 1e-16), min 1.52× (top of range, where naive is borderline); vs 30-term series: median 3.14e4×, max 1.63e9×. **vs the exp-multiplied form: median 0.46×, max 13.3×** — the candidate "stable" form of the dispatch yields *no* accuracy gain in fp64 (it is algebraically exact but numerically as ill-conditioned as the naive form; at the deep end it is up to ~10× worse). This is the central verification result of the task.

**C2 — boundary cases (capable-of-failing edge, fp64):** for `s < 2^-53 ≈ 1.1e-16` (y ≲ 1.2e-32), `exp(±s)` rounds to 1.0 exactly, so both cancellation forms divide by zero: measured `x_exp → inf` at y = 1e-32, `x_naive → inf` at y = 1e-33, both `inf` at y = 1e-34; `−y/expm1(−s)` and the series stay accurate (≤ 1.3e-16; e.g. y = 1e-34: 3.1e-17 / 6.9e-17). Probes inside the range (y = 1e-18, 1e-20, 1e-30, 1e-31): naive 2.8e-8, 8.3e-8, 8.0e-4, 5.1e-2; exp 8.2e-8, 8.3e-8, 9.9e-2, 0.42; expm1/series ≤ 1.6e-16 — error grows like δ/s exactly as derived. Large-y: at y = 1e8 all three closed forms give exactly y (e^{−1e4} < 1e-4300; both fp64 and reference truncate to y — degenerate consistency, not a precision statement); the 8-term series there is 3.3e15 off — outside its radius, as required by the domain statement.

**C3 — series route verification (cf. AS028).** (i) Exact coefficients, two independent routes (formal reciprocal; Bernoulli B⁻ + sign map): all 130 match (verify C1); odd-k ≥ 3 coefficients vanish; first-term signature `{1, 1/2, 1/12, −1/720, 1/30240, −1/1209600, 1/47900160}` exact. (ii) 120-term `x/s` vs 70-digit reference on y ≤ 10: **max rel err 1.93e-16** (Horner; direct-sum agrees); substitution `(1 − e^{−s})·(x_ser/s) − s`: max |resid| 4.44e-16 (2 ulp). (iii) Radius boundary probes (y, 120-term rel err, |term₁₂₀|): 19.7392 → 0.0 (=1e-19 level), 1.7e-18; 30 → 1.4e-8, 1.4e-7; 39 → 7.7e-2, 0.96; 39.4 → 0.141, 1.78; **4π² = 39.4784176 → 0.159, term 2.000** (no decay at the radius); 40 → 0.345, 4.40; 50 → 1.8e5, 2.87e6 (divergent). Exactly the analytic statement; in full agreement with the AS028 run's probes (their y = 39.4: 0.141; 39.478: 0.159; y = 50 term 2.87e6). (iv) Independent representation at arbitrary non-decade points y ≤ 10: max rel err 1.70e-16 (verify C6).

**C4 — MONO splice and deep inheritance (operative-branch statement).** Contract: `h_mono = h_RAR` on `(0, y*]`; `h'_mono = max(h'_RAR, δh_p/(y+y_p))`, δ = 0.05; continuation `h_mono(y) = h_RAR(y*) + δh_p·ln((y+y_p)/(y*+y_p))` for y > y*. Landmarks re-derived (bisection in compute; Newton in verify, exact derivatives): **y\* = 2.3374124053** (|dev| 4.1e-7 vs quoted 2.337412), y_p = 2.5396382822 (1.7e-6), h_p = 0.6476102379 (2.4e-7); splice residual `h'_RAR(y*) − δh_p/(y*+y_p) = 6.1e-18`. Identity check on (0, y*] with independent stable routes (expm1-RAR vs series-MONO): max rel diff 3.3e-16 over all 121 deep points; margins: deep domain sits 4.37 decades below y*. Diagnostic (naive h-form route `y/(e^s−1)`): max rel err vs reference 1.1e-8 — the same cancellation as the naive x-form, i.e. the *evaluation route* degrades, the *function* does not. Statement (criterion B): RAR is the comparison branch of this derivation; the operative MONO branch inherits the deep-x evaluation and the deep series identically on (0, y*] — hence the stable evaluation is operative for the framework's filtered target in the deep-MOND regime; Q, MU2, EXP remain distinct and untouched.

**C5 — footings and dimensional maps (§7).** kappa = 1/2 held fixed ⇒ rho_Lambda changes between footings (ratio (a0_alt/a0_can)² = 1.45149); dimensionless theorem applies identically to both. G_N enters only through B = G_N·M_b/r² and the r_M/v_flat landmarks; G_bare and G_cosmo are separate symbols, not used (no cosmological relation in scope).

**Verify (independent implementation — VERIFY_OK, 6/6):** C1 Bernoulli via B⁻ route (exact match, 130 coeffs); C2 reference self-convergence (≤ 2.8e-43); C3 split-form identity `x = y + h`, `h = −y·e^{−s}/expm1(−s)` vs direct expm1 form over the full 241-point grid (max 3.08e-16); C4 Newton landmarks (identical to bisection); C5 dense rescan k step 0.01, 1201 points, independent 50-digit reference: fails at bar: naive 1066, exp-form 1117, expm1 0, series 0 — confirms the main-grid counts at 10× density (and that the exp-form is the worst offender); C6 series at arbitrary points (1.70e-16).

---

## 4. Step-by-step execution record

1. Read the branch equations (FRAMEWORK_CONTRACT branch dictionary), the AS028 companion results; state/symbols/assumptions (§1); recorded the dispatch-spec provenance above.
2. Derived the algebraic identity chain (§2, Lean-certified), the cancelation analysis with the δ/s bound, and the deep series with exact Bernoulli coefficients.
3. Computed the full fp64 evaluation matrix + 70-digit reference on the mandated grid, extended grid, probes, and boundary (raw_output.json); quantified per-decade errors and accuracy gains.
4. Independent representation: verify script (Bernoulli B⁻ route, 50-digit reference, split form, Newton landmarks, 1201-point dense rescan, arbitrary points); VERIFY_OK.
5. Negative control ran and failed exactly as physics requires (C1), including the unexpected second failure mode of the "stable" exp-multiplied form and the s < 2^-53 division-by-zero edge (C2); surviving statement and transfer implication in §8.

---

## 5. Lean certificate

`AS050_stable_evaluation_certificates.lean`, compiled with `lake env lean` (mathlib v4.34.0-rc2, project `fable_independent_2026/lean_2026`), **exit 0, zero `sorry`, axioms = {propext, Classical.choice, Quot.sound} on all 9 theorems**: `nu_stable_rearrangement`, `x_stable_form_exp` (`y/(1−e^{−s}) = y·e^s/(e^s−1)` — the dispatch's multiply-by-exp identity), `x_stable_form_exp_neg` (`= −y/(e^{−s}−1)`, i.e. −y/expm1(−s) by definition), `x_deep_rearrangement` (`= y + y/(e^s−1)`), `deep_x_series_terms` (s·Q₆ = x-series through s⁷: `s + s²/2 + s³/12 − s⁵/720 + s⁷/30240`), `deep_x_over_s_terms`/`_in_y` (the claimed route `x/√y = 1 + s/2 + s²/12 − s⁴/720 + s⁶/30240` as an exact truncated identity), `deep_x_series_in_y`, and `series_core_algebraic_core` (P₆·Q₆ = 1 + s⁷·(1/40320 + 19/1814400·s + 1/1814400·s² − 1/21772800·s⁴ + 1/152409600·s⁵) — exact coefficient inversion through order 6; residual computed independently in Python before transcription). Mathlib v4.34 has no `Real.expm1`, so the expm1 form is anchored definitionally to `e^{−s} − 1`; everything transcendental (Taylor series, radius, Bernoulli identification, truncation estimates) is analytic input validated numerically, deliberately not a Lean statement.

---

## 6. Both footings and dimensional examples (SI; kappa = 1/2 held fixed → rho_Lambda changes)

| quantity | canonical | alternative |
|---|---|---|
| a0 (m/s²) | 9.3619e-11 | 1.1279e-10 |
| rho_Lambda = 4a0²/(G·c²) (kg/m³) | 5.8444e-27 | 8.4831e-27 |
| eps_Lambda = rho_Lambda·c² (J/m³) | 5.2527e-10 | 7.6242e-10 |
| Λ = 32πa0²/c⁴ (m⁻², Einstein G = scale G) | 1.0908e-52 | 1.5833e-52 |
| r_M(1e11 M_sun) (kpc) | 12.202 | 11.117 |
| v_flat(1e11 M_sun) (km/s) | 187.75 | 196.70 |
| g = a0·x at y = 1e-16 (m/s²) | 9.3619e-19 | 1.1279e-18 |
| g at y = 1e-10 (m/s²) | 9.3619e-16 | 1.1279e-15 |
| g at y = 1e-4 (m/s²) | 9.4088e-13 | 1.1335e-12 |
| g at y = 1 (m/s²) | 1.4810e-10 | 1.7843e-10 |
| g at y = 1e2 (m/s²) | 9.3623e-09 | 1.1280e-08 |

(The landmarks replicate the framework's published values at 1e11 M_sun, e.g. AS019/AS028's 12.202/11.117 kpc and 187.75/196.70 km/s.)

---

## 7. Failed attempts (preserved honestly)

1. **`x_exp` overflow at y = 1e8** (math.exp(1e4)) → guarded: for s > 700 return the limit y (e^s/(e^s−1) = 1 − e^{−s}, error < e^{-700}); noted in code.
2. **ZeroDivisionError at boundary probes** (y = 1e-34: `e^s − 1 == 0` in fp64) → caught and recorded as inf; became the C2 boundary finding (cancellation forms divide by zero below s ≈ 2^-53).
3. **Lean v1: exponent transposition in the x-series statement** — wrote `−s⁷/720 + s¹¹/30240` for the RHS of `s·Q₆(s)`; `ring` failed showing the correct normal form `−s⁵/720 + s⁷/30240`; fixed (x = s·Q(s), so x⁵ and x⁷ terms), plus a trailing `ring` after `field_simp` had closed the goal ("No goals to be solved") and an unused `hy` hypothesis — removed.
4. **Bernoulli convention mismatch**: the raw recurrence `Σ_k C(m+1,k)B_k = 0` yields B₁ = −1/2 (x/(e^x − 1) convention); the series carries B₁ = +1/2 (s/(1−e^{−s})). Initial cross-check "failed"; corrected to the second-Bernoulli convention and documented; verification then exact on all 130 orders, independently re-derived through the sign map `q_k = (−1)^k B⁻_k/k!`.
5. **Verify C2 tolerance miscalibrated**: required 1e-47 but the 50-digit reference's own deep-end floor is ~1e-50/s ≈ 1e-42; observed 2.8e-43 is genuine convergence; tolerance re-set to 1e-40 with explanation (fp64 claims need only ≪ 1e-16).

---

## 8. Strongest surviving statement, closure implication, next step

**Strongest statement.** On the RAR branch, for y ∈ (0, 4π²): `x/√y = 1 + s/2 + s²/12 − s⁴/720 + s⁶/30240 − ⋯` with exact Bernoulli coefficients (radius |s| < 2π ⇔ y < 4π²), and on y ∈ [1e-16, 1e8] the stable evaluations `x = −y/expm1(−√y)` (fp64: max rel err 2.43e-16) and the expm1-free deep series (max rel err 2.45e-16 on the mandated range) reproduce the RAR deep-x to full double precision, while the naive form `y/(1−e^{−√y})` maxes out at 3.6e-9 (105/121 failures at the 1e-14 bar) **and the dispatch's candidate form `y·e^s/(e^s−1)` fails equally (118/121, max 1.1e-8)** — multiplying by e^s is algebraically exact but numerically still a cancellation; only expm1 or the series is stable. MONO (operative filtered target) inherits this identically on (0, y*] = (0, 2.337412] (deep domain 4.37 decades below the splice; measured residual 3.3e-16).

**Closure implication (gate A02, criterion B branch fidelity).** The framework's RAR/MONO deep-MOND evaluation layer now has: an exact-identity + exact-coefficient deep series with radius and measured truncation behavior, a certified stable evaluation, the measured failure envelope of every cancellation form (including the exp-multiplied candidate), and the operative-branch inheritance statement. This is the numerical prerequisite for any downstream use of RAR/MONO deep-x in the campaign's fitting/evaluation pipelines; no transfer to the filtered field equation is made.

**Next unresolved implication.** The evaluation lives on the spherical unfiltered algebraic response `g = a0·x(y)`; the operative target is `Δu = 4πGρ_b` with `S = exp[(ξ²/2)Δ]` and `div[nu_mono(|∇Su|/a0)·∇Su]`. The missing bridge is (a) the metric/measure/domain specification of S (open dependency, as in AS028.C01), and (b) a repository-level audit of evaluation sites: any campaign code evaluating the kernel via `1/(1−exp(−√y))` or `e^s/(e^s−1)` in the deep regime inherits the measured 1e-9…1e-8 error envelope; the audit target and replacement spec are the suggested follow-up.

**Suggested follow-up.** `AS050.C01` (spec, not dispatched — no runner in this session): *kernel evaluation audit + crossover spec* — scan the campaign's RAR/MONO evaluation sites (SPARC fit kernels, EFE pipelines, deep-MOND landscape code) for the naive and exp-multiplied patterns; replace with `−y/expm1(−√y)` for all y and the certified series for y ≤ 10 (or y < 4π² with N-term remainder bound); regression test at y = 1e-16 against the 70-digit reference; new claim: "no evaluation site in the audited set exceeds 3e-16 relative error in the deep regime after the replacement." Existing coverage check: AS028 covers the nu-form stability/series (same coefficient family, radius), AS028.C01 covers the filtered transfer bound — neither claims the exp-form failure measurement or the evaluation audit; no manifest/claims entry found for either (AS050 catalog file is a different topic; claims/AS050.json is the orchestrator's reservation record, untouched).
