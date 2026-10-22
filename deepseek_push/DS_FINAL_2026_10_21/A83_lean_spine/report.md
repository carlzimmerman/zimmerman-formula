# A83 — LEAN 4 FORMALIZATION OF THE ALGEBRAIC SPINE

**Lane:** A83_lean_spine · **Date:** 2026-10-22 · **Status:** CERTIFIED (47 theorems, zero sorry,
standard axioms only)
**Modules:** `fable_independent_2026/lean_2026/A83/{BlockA,BlockB,BlockC,BlockD}.lean`, umbrella
`fable_independent_2026/lean_2026/A83.lean`, audit `fable_independent_2026/lean_2026/A83_Axioms.lean`
**Script:** `a83_checks.py` — **all checks PASS, exit 0** · **Output:** `a83.out` ·
**Data:** `a83_results.json`, `a8_baseline.json`, `a83_mutations.json`, `a83_mutations_inplace.json` ·
**Mutations:** `MUTATE.md` (5 dials, each killed in isolation and each forcing the full verification to
exit 1 when applied in place).

---

## 0. The answer in one paragraph

**Forty-seven theorems, no `sorry`, no `axiom`, no `native_decide`, standard axioms only, in the
existing `lean_2026` project — and not one of them is the kind of tautology that disqualified the
external package.** The Lean tree formalizes the A68 quadratic form (the 2×2 longitudinal/conformal
kinetic matrix, its degeneracy at `β = −2/3`, the `α = γ` single-stiffness condition, `Z, Q₀ > 0`, and
`ω² = αp⁴/Z` vanishing to order exactly four), the A63/A54/A75 saturating law (`g_N < g`, both slopes,
`dg/dg_N = 1 + a₀²/(g²+2a₀g) > 1`, the rectification obstruction `odd ⟹ f''(0) = 0` against
`θ''(0) = −2`, and the mass cancellation `a_sat = k_BTc/ħ`), the A72 coefficient **with its Friedmann
premise** (`√(Gρ_Λ) = 2H_Λ/Z`, `a₀/(cH_Λ) = 2κ/Z`, `κ_DE = Z/4π = √(2/3π)`, `8π/κ² = 12π²`, and the
unreduced branch `48π⁴`), and the A78 β-relation **with matter** (`β = (2/3)Ω_L(r_Λ − 1)`,
`β > 0 ⟺ r_Λ > 1`, the BBN window, and its sharpness). The theorem delta over A8_lean is **+47 new
names, 0 overlap, 0 deleted, 0 weakened** — the last by byte-identical source hashes, not by
assertion. The one item the task asked for that cannot be proved is "second-class ⟺ α = γ": A68's
second-class matrix carries no α or γ at all (§3.3 below), so I prove the true statements (single
stiffness ⟺ α = γ; the kinetic degeneracy ⟺ β = −2/3; the stiffness block non-degenerate ⟺ α γ p ≠ 0)
and do not manufacture the false equivalence.

---

## 1. Where the Lean lives — extending the real project, not a stub

The task forbade a disconnected toolchain, so the modules sit inside the warm project
`fable_independent_2026/lean_2026/` (toolchain `leanprover/lean4:v4.34.0-rc2`, Mathlib at
`v4.34.0-rc2`) and are a first-class Lake target:

```toml
[[lean_lib]]
name = "A83"            # root A83.lean, modules A83.BlockA … A83.BlockD
```

* `lakefile.toml` is the **only** project file touched. `defaultTargets` is unchanged
  (`["Mondlean", "ChainCert"]`), and `lake build` (default targets) still completes: 8785 jobs, exit 0.
* `lake build A83` — **exit 0 from a cold start** (A83 artefacts deleted; the elapsed time is
  recorded in `a83.out`; it varies with cache state, 11–40 s across runs).
* The lane ships byte-identical copies of the five built modules and the audit file under
  `A83_lean_spine/lean/`; check L8 re-hashes them against the built sources so the archive cannot
  drift.
* `lake env lean A83_Axioms.lean` — exit 0, 47 axiom footprints.
* `grep -r A79` over the modules and the checker: **0 hits**. The refuted external package is not
  imported, cited or depended on.
* No `THEORY.md`, `README.md`, `STATUS_BOARD.html` or other lane directory was modified; nothing is
  committed.

The four block files are independent (each imports only Mathlib), so every block can be compiled and
mutated on its own; `A83.lean` imports all four.

---

## 2. The theorem delta over A8_lean

The A8_lean "40 theorems" needs one sentence of reconciliation, because the count is 40 *certified
declarations*, not 40 names:

| object | count |
|---|---|
| `theorem` declarations in the four A8 files | **43** |
| unique fully-qualified names among them | **42** (`A8.gCanon_form` is declared in both `A8_C3` and `A8_C4`) |
| declarations with a `#print axioms` footprint in `LEAN_VERIFICATION.log` — the lane's "40" | **40** |
| unique names among those 40 | **39** |
| the three A8 declarations without an axiom print | `A8.deriv_inner_quad`, `A8.deriv_inner_canon`, `A8.deriv_half` |

Against that frozen baseline (`a8_baseline.json`, written before A83 existed):

| delta | value |
|---|---|
| new named theorems in A83 | **47** |
| new names not in the A8 set | **47** |
| overlap with A8 names | **0** |
| A8 names missing after the run | **0** (42/42 unique names still parse) |
| A8 sources changed | **0** — all four files byte-identical (sha256 checked) |
| net certified declarations after A83 | **87** = 40 (A8) + 47 (A83); under the 43-declaration reading of A8, 90 |

**Why "no theorem deleted or weakened" is proved, not asserted.** The checker re-hashes the four
A8 source files and compares them with the frozen baseline. Byte-identical sources cannot contain a
deleted theorem, a strengthened hypothesis, or a weakened conclusion; there is no room for a silent
edit. The 47 new names live in `A83.*` and cannot shadow `A8.*`.

A54's 13 standalone theorems are **not** part of the 40 (different directory, no `A8` namespace, not
in the A8 verification log). One of the new theorems overlaps A54 in *content*:
`deriv_gOfgN_gt_one` is A54's gate (iv) (`dg_dgN_ge_one` in `A54_coefficients.lean`). It is a new
name, proved here through the inverse-function theorem rather than by importing A54's file (which has
no lakefile of its own). The θ-derivative theorems are A63's content, not A54's.

Of the 47 theorems, **46 are non-definitional**; the single definitional one is
`theta_temperature_blind` (`rfl`, §4.4), which is counted in the 47 but excluded from any
"substantive" claim.

---

## 3. Block A — the A68 quadratic form

### 3.1 The matrices, quoted

A68 §3.1 gives the scalar-sector quadratic Lagrangian with `A ≡ 2+3β`:

```
L/a³ = [−3A(ζ̇ − Hn)² + 2A(ζ̇ − Hn)Y − βY² + 2p²ζ² + 4p²nζ] / (4K)
       + p² n σ + (ηp²/2) σ̇² − ((Kp² + αp⁴)/2) σ² .
```

The longitudinal/conformal kinetic block is therefore

```lean
def Kmat (β η K p : ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  !![-(3 * (2 + 3 * β)) / (4 * K), 0; 0, η * p ^ 2 / 2]
```

(`−3Aζ̇²/(4K)` is A68 D1; `(ηp²/2)σ̇²` is the P kinetic term in the same line.)

The P-sector **gradient** block comes from `−(α/2)(D_iP^i)² − (γ/4)F_ijF^ij` with
`(D·P)² ↦ p⁴σ²` and `F² ↦ 2p²|P_T|²` (A68 D16, D17):

```lean
def Gmat (α γ p : ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  !![α * p ^ 4, 0; 0, γ * p ^ 2]
```

### 3.2 What is proved

| theorem | statement |
|---|---|
| `Kmat_det` | `det Kmat = −3(2+3β)ηp²/(8K)` |
| `Kmat_det_eq_zero_iff` | `det = 0 ↔ 2+3β = 0 ∨ η = 0 ∨ p = 0` (K ≠ 0) |
| `Kmat_degenerate_iff_beta` | with `η, p, K ≠ 0`: `det = 0 ↔ β = −2/3` — A54 L8 / A68 §3.4 |
| `Gmat_det` | `det Gmat = αγp⁶` |
| `Gmat_det_ne_zero_iff` | `det ≠ 0 ↔ α ≠ 0 ∧ γ ≠ 0 ∧ p ≠ 0` |
| `Gmat_single_stiffness_iff` | `p ≠ 0`: `Gmat α γ p = γ • Gmat 1 1 p ↔ α = γ` (A68 D16) |

`Gmat_single_stiffness_iff` is the precise form of "the frozen action carries one stiffness in front
of both gradient operators iff α = γ": the matrix must be `γ` times the fixed matrix `diag(p⁴, p²)`,
and at `p ≠ 0` that happens exactly when the two diagonal coefficients agree.

### 3.3 The honest note on "second-class ⟺ α = γ"

The task asked to "prove the degeneracy/second-class condition holds iff α = γ". **That equivalence
is not in A68, and I did not formalize it.** A68's second-class object is the Dirac matrix of the pair
`(H_i, π_P^j)`,

```
M_i{}^j(k) = i[π_P^j k_i − δ_i^j(π_P·k)] − δ_i^j (D·π_P) ,
```

which is **linear in the P momentum and contains neither α nor γ**; it vanishes identically on
`π_P = 0` (A68 B3, rank 0 at five configurations), and that is why `SC = 0`. Writing a theorem
"second class ⟺ α = γ" would therefore certify a relation the source explicitly denies. What α = γ
actually is, in A68 D16, is a **single-stiffness** condition on the two gradient operators — and that
is exactly what `Gmat_single_stiffness_iff` proves. The two genuine degeneracies that *do* exist in
the 2×2 blocks are `Kmat_degenerate_iff_beta` (`β = −2/3`, the θ-Legendre singularity) and
`Gmat_det_ne_zero_iff` (a zero stiffness or zero momentum). All three statements are quoted from the
matrices above; none is a tautology, and none re-exports a PDE hypothesis.

### 3.4 `Z`, `Q₀` and the task's transcription slip

A68 §3.2: `Z = Q = B + ηp²`, `B = K(2+3β)/β`. A54 §2: `Q₀ = (2+3β)/(Kβ) + ηk²/K²`. The task's
`Q₀ = K(2+3β)/β + ηp²/K²` is neither of these — it mixes the `Z` normalisation of the first term with
the `Q₀` normalisation of the second. Rather than certify a quantity that appears nowhere in the
record, the module defines both sourced objects and proves the exact bridge:

```lean
def Z  (β η K p : ℝ) : ℝ := K * (2 + 3 * β) / β + η * p ^ 2
def Q0 (β η K p : ℝ) : ℝ := (2 + 3 * β) / (K * β) + η * p ^ 2 / K ^ 2

theorem Q0_eq_Z_div_K_sq : Q0 β η K p = Z β η K p / K ^ 2
theorem Z_pos  : 0 < K → 0 < β → 0 ≤ η → 0 < Z β η K p
theorem Q0_pos : 0 < K → 0 < β → 0 ≤ η → 0 < Q0 β η K p
```

`Z_pos` uses `β > 0` to make `2+3β > 0` and the `ηp²` term non-negative; `Q0_pos` follows from
`Q0 = Z/K²`. **A qualification on A68's phrasing.** A68 §3.2 writes `Z > 0 ⟺ β > 0` on the
`2+3β > 0` branch. The `⟸` direction is what is true for every `p` and is what the module proves. The
converse holds at `p = 0` (where `Z = K(2+3β)/β`) but **not** for all `p` when `η > 0`: on
`β ∈ (−2/3, 0)` the `B` term is negative while `ηp²` can dominate it at large `p`. The Lean statement
is therefore one-directional on purpose; the biconditional would be false as written.

### 3.5 "Vanishes to order 4" — the precise Lean statement

"Order 4 at `p = 0`" is formalized as: the value at zero vanishes **and** the ratio `ω²/p⁴` has a
finite non-zero limit. That is two theorems plus a limit value:

```lean
theorem omegaSq_zero : omegaSq α β η K 0 = 0
theorem omegaSq_div_p4_tendsto (hβ : 0 < β) (hK : 0 < K) :
    Tendsto (fun p : ℝ => omegaSq α β η K p / p ^ 4) (𝓝[≠] 0)
      (𝓝 (α * β / (K * (2 + 3 * β))))
```

The filter is `𝓝[≠] 0`, the **punctured** neighbourhood, not `𝓝 0`. This is not a weakening for
convenience: Lean's division is total, so `ω²(p)/p⁴` is *defined* to be `0` at `p = 0`, while its
punctured limit is `αβ/(K(2+3β)) ≠ 0`; a `𝓝 0` limit with a non-zero value is therefore **false** in
Lean, and the punctured statement is the true one. `omegaSq_pos` gives `ω² > 0` for `p ≠ 0`, so the
mode is a genuine `k⁴` mode: positive frequency, `c_s² = ω²/p² → 0`.

---

## 4. Block B — the saturating law, rectification, mass cancellation

### 4.1 The law and its slopes

| theorem | statement |
|---|---|
| `gN_lt_g` | `g > 0, a₀ > 0 ⟹ g²/(g+a₀) < g` |
| `deriv_gN` | `d/dg [g²/(g+a₀)] = (g² + 2a₀g)/(g+a₀)²` |
| `deriv_gN_pos` | that derivative is `> 0` |
| `gOfgN_eq` | the branch `(g_N + √(g_N²+4a₀g_N))/2` really inverts the law |
| `deriv_gOfgN` | `dg/dg_N = 1 + a₀²/(g² + 2a₀g)` |
| `deriv_gOfgN_gt_one` | `1 < dg/dg_N` |

`deriv_gOfgN` is proved through `HasDerivAt.of_local_left_inverse` — the inverse-function theorem,
with `gOfgN_eq` supplying the local left inverse — not by postulating the reciprocal. That is the
mathematically loaded step: the forward slope `dg_N/dg` is computed by the quotient rule, and the
inverse slope is its reciprocal, then simplified to `1 + a₀²/(g²+2a₀g)` using `g_N(g+a₀) = g²`.

### 4.2 The rectification obstruction (A63)

```lean
theorem deriv_eq_zero_of_even {g : ℝ → ℝ} (heven : ∀ x, g (-x) = g x) : deriv g 0 = 0
theorem deriv_odd_is_even  (hodd : ∀ x, f (-x) = -f x) (hdf : ∀ x, DifferentiableAt ℝ f x) :
    deriv f (-x) = deriv f x
theorem odd_second_deriv_zero (hodd) (hdf) : deriv (deriv f) 0 = 0
```

The first is unconditional: `deriv (g ∘ neg) 0 = −deriv g 0` while `g ∘ neg = g`, so `deriv g 0 = 0`.
The third then applies it to `deriv f`, which is even because `f` is odd. This is the obstruction in
its sharp form: **any** odd (centrosymmetric) isotherm has `f''(0) = 0`, hence no `g²` term, hence
`g_N ∝ g³` — MOND's exponent 2 cannot come from a symmetric medium.

Against it, the Langmuir gate:

```lean
theorem theta_zero              : theta 0 = 0
theorem theta_deriv_zero        : deriv theta 0 = 1
theorem theta_second_deriv_zero : deriv (deriv theta) 0 = -2
```

with `theta x = x/(1+x)`. `θ''(0) = −2` is `c₂ = −1`, the coefficient A63's admissibility theorem
needs (`C = s = −c₂a₀ = a₀`). The second derivative is computed by differentiating
`1/(1+x)²` and transferring along the eventual equality `deriv theta =ᶠ 1/(1+x)²` near `0`; the
punctured/eventual care is explicit in the proof because `theta` has a pole at `x = −1`.

### 4.3 The mass cancellation (A75)

```lean
theorem mass_cancellation (hm : m ≠ 0) (hc : c ≠ 0) (hb : hbar ≠ 0) :
    kB * T / (m * (hbar / (m * c))) = kB * T * c / hbar
```

With `λ_C = ħ/(mc)`, `m·λ_C = ħ/c`, so `a_sat = k_BT/(mλ_C) = k_BTc/ħ` — the mass cancels
identically. This is the real content of A75 §2.5: A72's coefficient cannot test the carrier, because
no carrier mass survives. The numeric check (`N14`) evaluates the two sides at five masses
`1e-30 … 1e-18 kg` and finds a spread of `1.6e-61` (rounding), and `N15` reproduces A72's
`a₀ = 8.618166e-11` from `T_dS` to `1e-9`.

### 4.4 The definitional lemma — labelled, not dressed as physics

```lean
def thetaOf (g a0 : ℝ) : ℝ := g / (g + a0)
def thetaAtTemperature (_T g a0 : ℝ) : ℝ := thetaOf g a0
theorem theta_temperature_blind (T g a0 : ℝ) : thetaAtTemperature T g a0 = thetaOf g a0 := rfl
```

**This is a definitional fact, not a physics theorem.** `thetaOf` has no temperature argument, so
"the gate is temperature-blind at fixed drive" is true by construction (`rfl`). It is included because
the task asked for it and because it makes the logical status explicit, and it is **excluded from the
substantive count** below. The physics — that the drive is an activity `z = g/a₀`, that the free
energy is `F = U − TS` with `S = −k_B[θlnθ + (1−θ)ln(1−θ)]`, and that `a₀` must therefore be
postulated as a function of `T_dS` — is A75 §1 and is **not formalized**. The algebraic trace of the
activity structure that *is* formalized is

```lean
theorem thetaOf_eq_activity (ha0 : a0 ≠ 0) : thetaOf g a0 = (g / a0) / (1 + g / a0)
```

which is an identity, not a thermodynamic statement.

---

## 5. Block C — the A72 coefficient, with its Friedmann premise

The task's premise `8πGρ_DE = 3H_Λ²` is not decoration: it is the hypothesis that turns
`a₀ = κc√(Gρ_Λ)` into `a₀/(cH_Λ) = 2κ/Z`, and it is the hypothesis of the derivation:

```lean
theorem sqrt_Grho_eq (hH : 0 < H) (hFried : 8*π*G*ρ = 3*H^2)
    (hZ : Z^2 = 32*π/3) (hZ0 : 0 < Z) : Real.sqrt (G*ρ) = 2*H/Z

theorem kappa_of_a0_from_friedmann (hH : 0 < H) (hc : c ≠ 0)
    (hFried : 8*π*G*ρ = 3*H^2) (hZ : Z^2 = 32*π/3) (hZ0 : 0 < Z)
    (ha0 : a0 = κ*c*Real.sqrt (G*ρ)) : a0/(c*H) = 2*κ/Z
```

That is A72 eq. (0.1): with the Friedmann normalisation, `√(Gρ_Λ) = 2H_Λ/Z`, so
`a₀/(cH_Λ) = 2κ/Z`, i.e. `κ = Za₀/(2cH_Λ)`. Then:

| theorem | statement |
|---|---|
| `Zcanon_sq` | `(2√(8π/3))² = 32π/3` |
| `kappaDE_eq_sqrt` | `Z² = 32π/3, Z > 0 ⟹ Z/(4π) = √(2/(3π))` |
| `a0_eq_iff_kappa_eq` | `a₀ = cH/(2π) ↔ Za₀/(2cH) = Z/(4π)` — the "algebraic equivalence" |
| `two_cH_over_a0` | `2cH/a₀ = 4π` for `a₀ = cH/(2π)` |
| `eight_pi_over_kappa_sq` | `8π/κ_DE² = 12π²` |
| `a0_reduced` | `a0OfWavelength c (c/H) = cH/(2π)` |
| `a0_full` | `a0OfWavelength c (2π c/H) = (cH/(2π))/(2π)` |
| `kappa_full` | `κ_DE/(2π) = Z/(8π²)` |
| `eight_pi_over_kappa_full_sq` | `8π/κ_full² = 48π⁴` |

The unreduced branch is the 2π slip that got the external package refuted: using
`λ_full = 2πλ_reduced` divides `a₀` and `κ` by `2π`, and `8π/κ_full² = 4π² · 12π² = 48π⁴`, not
`12π²`. Both branches are exact.

**Numbers.** `Z = 5.788810036466141`, `κ_DE = 0.4606588659617806` (A72's
`/numbers/Z_over_4pi` = `0.46065886596178063`, A75's `K20_kappa` = `0.4606588659617806`);
`12π² = 118.4352528130723`; `48π⁴ = 4675.636369632117`.

**One arithmetic slip in the task text, flagged rather than copied:** the task quotes `48π⁴ = 4674.6`.
The exact value is `4675.6364`; `4674.6` is a `2.22e-4` relative error (it looks like π truncated to
four decimals: `48·3.1415⁴ ≈ 4674.3`). The Lean theorem is exact, and the checker records both the
exact identity and the disagreement with the quoted literal (`N6`, `N7`). `12π² = 118.435` is a
correct 3-decimal rounding of `118.43525`.

---

## 6. Block D — A78 with matter, and the BBN window

A33's vacuum-only relation `2 + 3β = 2Ω_L r_Λ` is **not** used anywhere. The module starts from A78
§3's matter-inclusive relation:

```lean
theorem beta_of_r (hrel : 2 + 3*β = 2*(ΩL*r + Ωm)) (hsum : ΩL + Ωm = 1) :
    β = (2/3) * ΩL * (r - 1)

theorem beta_pos_iff_r_gt_one (hβ : β = (2/3)*ΩL*(r-1)) (hΩ : 0 < ΩL) : 0 < β ↔ 1 < r
```

so `β > 0` requires `r_Λ > 1` — not `r_Λ > 1/Ω_L`, which is what the vacuum-only relation would give
and what A78 corrected. The BBN bound comes in two forms, because the data are a non-strict bound and
the open interval needs strictness somewhere:

| theorem | hypothesis | conclusion |
|---|---|---|
| `r_le_bound` | `\|ΔN_eff\| ≤ ε`, `ΔN_eff = −Cβ`, `C > 0` | `r_Λ ≤ 1 + 3ε/(2Ω_L C)` |
| `r_upper_bound` | `\|ΔN_eff\| < ε` | `r_Λ < 1 + 3ε/(2Ω_L C)` |
| `r_window` | `β > 0`, `\|ΔN_eff\| < ε` | `r_Λ ∈ (1, 1 + 3ε/(2Ω_L C))` |
| `bound_sharp` | `β = ε/C` | `r_Λ = 1 + 3ε/(2Ω_L C)` |

`bound_sharp` is the "nothing wider" statement: at `β = ε/C` the endpoint is attained exactly, so the
non-strict bound cannot be improved, and the strict hypothesis in `r_window` is necessary, not
cosmetic.

**Numbers.** With the task's parameters `ε = 0.30`, `C = 11.1738`, `Ω_L = 0.6847`:
`r_Λ < 1.058818141` (`N10`; the task quotes `1.0588`). With A78's own `Ω_L = 0.6838` and its
full-precision `ΔN_eff = −11.173790231394968 β`, the non-linear inversion
`2Cβ/(2+3β) = ε` gives `β_max = 0.02797514` and `r_Λ = 1.06136693`; A78 prints `1.06136690`
(`N13`, residual `3.1e-8`), and `β(r = 1.061) = 0.02780787 < 0.0280` (`N8`, `N9`). The linearised
bound `1.05882` and A78's exact `1.06137` differ by `2.5e-3 = O(β)`, the `3β` in the denominator of
`2Cβ/(2+3β)`; the linearised bound is the tighter of the two at fixed `C`, so both are consistent and
neither is "nothing wider" than the other — they are bounds on two different functions (`N11`).

---

## 7. Checks (`a83_checks.py`, all PASS, exit 0)

```
L1  lake build A83 on lean_2026, cold start                         exit 0 (cold; see a83.out)
L2  lake env lean A83_Axioms.lean                                   exit 0, 47 footprints
L3  sorry / admit / native_decide in the 5 module files              0 / 0 / 0
L4  source-level `axiom` declarations                                0
L5  every axiom set ⊆ {propext, Classical.choice, Quot.sound}        47/47
L6a named theorems in the new modules                                47 (≥ 24)
L6b delta over the A8 set                                            +47, overlap 0
L7a A8 names still present                                           42/42
L7b A8 sources byte-identical to the frozen baseline                 yes (sha256)
N1  Z² = 32π/3                                                       rel 0
N2  κ_DE = Z/(4π) vs A72 JSON                                        0.46065886596178063, rel 0
N3  κ_DE vs A75 JSON                                                 1.2e-16
N4  κ_DE = √(2/3π)                                                   0
N5  8π/κ² = 12π²                                                     rel 0
N6  8π/κ_full² = 48π⁴                                                rel 0
N7  12π² vs the task literal 118.435                                 2.1e-6
N8  β(r=1.061) = (2/3)Ω_L(0.061)                                    0.02780787, rel 0
N9  β(r=1.061) < A78's 0.0280                                        6.9e-3
N10 r bound at ε=0.30, C=11.1738, Ω_L=0.6847                         1.058818141
N11 linearised < exact bound                                         1.058896 < 1.061367
N12 A78's implied ΔN coefficient L                                   7.4492047 vs 7.4492, 6.3e-7
N12b β from L = 7.4492                                               6.5e-7 (report rounding)
N13 1 + 3β_max/(2Ω_L) vs A78's 1.0613669016                          3.1e-8
N14 mass-cancellation spread over 5 masses                           1.6e-61
N15 a_sat = k_BTc/ħ at T_dS                                          8.618166e-11, 0
N16 Z(β=1, η=0, p=0) = 5K = 4.193586e-09                             8.8e-8 (A68 7-digit)
E1  Z² − 32π/3 (50-digit mpmath)                                     8.6e-50
E2  Z/(4π) − √(2/3π)                                                 0
E3  8π/κ² − 12π²                                                     0
E4  8π/κ_full² − 48π⁴                                                2.2e-47
E5  2cH/a₀ − 4π at a₀ = cH/(2π)                                      0
M   5 mutations, each killed in isolation                            5/5
M′  each mutant applied in place makes the full check exit 1         5/5 (files restored)
    vacuum_only_beta / break_alpha_gamma / unreduced_wavelength / drop_Omega_m → L1+L2 fail
    inject_sorry → Lean exits 0, but L3 (token) and L5 (sorryAx) fail
```

The two A78 residuals (`6.3e-7`, `6.5e-7`) and the A68 one (`8.8e-8`) are the rounding of the
*source* values (`7.4492`, `4.193586e-09`), not of the identity: the checker records the implied
full-precision coefficient (`7.449204662`) alongside the printed one, so the discrepancy is
attributed rather than hidden.

---

## 8. What this does not formalize — and will not be quoted as if it did

* **No PDE.** The reduction of the frozen action to the quadratic scalar Lagrangian is A68's symbolic
  computation, not a Lean theorem. The Lean module starts from the quadratic form and quotes it.
* **No gate.** Gate 1 (`Φ = Ψ`) and Gate 3 (`α₁ = α₂ = 0`) are not assumed, imported, or re-exported.
  Nothing here says anything about them.
* **No free-energy derivation.** The `θ` function and its derivatives are formalized; the statistical
  mechanics that produces `θ = g/(g+a₀)` is not.
* **No thermal premise.** A75's conclusion is that `a₀ = cH_Λ/2π` is a *new postulate*, not a
  consequence of the classical action. The Lean module proves the algebraic chain
  `8πGρ = 3H² ⟹ √(Gρ) = 2H/Z ⟹ a₀/(cH) = 2κ/Z`, conditional on `a₀ = κc√(Gρ)`; it does not claim
  that the action supplies that identification.
* **No Dirac count.** `(26 − 16)/2 = 5` is not formalized, and deliberately so — it is exactly the
  kind of arithmetic-theatre theorem the task banned. The 2×2 matrices and their degeneracy
  conditions *are* formalized; the field-content count is not.
* **No numbers for `G`, `H`, `a₀`.** Every theorem is symbolic. The numeric checks live in
  `a83_checks.py` and are labelled as cross-checks of the identities, not as Lean theorems.

---

## 9. Reproduce

```bash
cd deepseek_push/DS_FINAL_2026_10_21/A83_lean_spine
python3 a83_checks.py --cold --json-out a83_results.json | tee a83.out   # all PASS, exit 0
python3 a83_checks.py --mutate all | tee a83_mutations.out               # 5/5 killed, exit 0
python3 a83_checks.py --mutate vacuum_only_beta                          # exit 0 (killed); reverse the
                                                                          # edit by hand and it survives
```

Direct Lean invocations:

```bash
cd fable_independent_2026/lean_2026
lake build A83                     # exit 0
lake env lean A83_Axioms.lean      # 47 × "depends on axioms: [propext, Classical.choice, Quot.sound]"
```

---

## 10. VERDICT

**The algebraic spine is certified: 47 new Lean theorems in the existing `lean_2026` project, zero
`sorry`, zero `axiom`, zero `native_decide`, every theorem's footprint exactly
`[propext, Classical.choice, Quot.sound]`, and `lake build A83` green from a cold start.** The
content is the actual content of the record, not placeholders: the A68 2×2 kinetic matrix with its
`β = −2/3` degeneracy and the `α = γ` single-stiffness condition; `Z, Q₀ > 0` and the order-four
vanishing of `ω² = αp⁴/Z` (stated with the punctured filter Lean requires); the saturating law with
both slopes, the inverse-function proof that `dg/dg_N = 1 + a₀²/(g²+2a₀g) > 1`, the rectification
obstruction `odd ⟹ f''(0) = 0` against `θ''(0) = −2`, and the mass cancellation `a_sat = k_BTc/ħ`;
the A72 coefficient derived **through** its Friedmann premise (`√(Gρ) = 2H/Z`, `κ = Z/4π = √(2/3π)`,
`8π/κ² = 12π²`) with the unreduced branch isolated as `48π⁴`; and A78's matter-inclusive
`β = (2/3)Ω_L(r_Λ − 1)` with `β > 0 ⟺ r_Λ > 1`, the BBN window and its sharpness. The delta over
A8_lean is +47 names with zero overlap, and "no existing theorem deleted or weakened" is proved by
byte-identical source hashes rather than by inspection. Two requested items are honestly *not*
certified as asked: "second-class ⟺ α = γ" is false to A68 (its Dirac matrix carries no α or γ), and
the temperature-blindness of the gate is a definitional `rfl`, labelled as such and excluded from the
substantive count; the task's `Q₀` and `48π⁴ = 4674.6` are transcription slips, corrected and
documented rather than copied. What remains outside Lean is exactly what A75 says remains outside the
action: the thermal identification of `a₀`, the PDE reduction, and the gates — none of which is
assumed anywhere in the 47 theorems.

---

## Appendix A — the exact delta: 47 new names

**Block A (A68 quadratic form) — 13**

`Kmat_det`, `Kmat_det_eq_zero_iff`, `Kmat_degenerate_iff_beta`, `Gmat_det`, `Gmat_det_ne_zero_iff`, `Gmat_single_stiffness_iff`, `Z_pos`, `Q0_eq_Z_div_K_sq`, `Q0_pos`, `omegaSq_pos`, `omegaSq_eq_p4_mul`, `omegaSq_zero`, `omegaSq_div_p4_tendsto`

**Block B (A63/A54/A75) — 16**

`gN_lt_g`, `deriv_gN`, `deriv_gN_pos`, `gOfgN_eq`, `deriv_gOfgN`, `deriv_gOfgN_gt_one`, `theta_zero`, `theta_deriv`, `theta_deriv_zero`, `theta_second_deriv_zero`, `deriv_eq_zero_of_even`, `deriv_odd_is_even`, `odd_second_deriv_zero`, `mass_cancellation`, `theta_temperature_blind`, `thetaOf_eq_activity`

**Block C (A72 coefficient) — 11**

`Zcanon_sq`, `kappaDE_eq_sqrt`, `sqrt_Grho_eq`, `kappa_of_a0_from_friedmann`, `two_cH_over_a0`, `a0_eq_iff_kappa_eq`, `eight_pi_over_kappa_sq`, `a0_reduced`, `a0_full`, `kappa_full`, `eight_pi_over_kappa_full_sq`

**Block D (A78 beta with matter) — 7**

`beta_of_r`, `beta_pos_iff_r_gt_one`, `beta_pos_imp_r_gt_one`, `r_le_bound`, `r_upper_bound`, `r_window`, `bound_sharp`

Total: 47 named theorems, all in namespace `A83`, none present in A8_lean, none shadowing an A8 name.  The full machine-readable list is `a83_results.json` → `theorems.new`.
