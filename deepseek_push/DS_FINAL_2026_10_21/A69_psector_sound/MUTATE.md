# A69 — MUTATIONS

Nine dials. Each changes **one** input, each is run with `python3 a69_checks.py --mutate NAME`,
each is recorded with its exit code and the **named** checks it breaks. The output of each run is
kept as `a69_MUTATE_<name>.out`.

| # | mutation | the one input changed | exit | checks broken |
|---|---|---|---|---|
| 0 | *(none)* | — | **0** | none (56/56 PASS) |
| 1 | `eta_eq_gamma` | the (η,γ) dial pairs are forced onto the diagonal η = γ | **1** | S3 |
| 2 | `no_W` | the saturating potential W(u) is set to 0 | **1** | S4, S5, S6 |
| 3 | `gamma_factor2` | the stiffness is doubled, γ → 2γ (with α = γ, as the action forces) | **1** | O1, O4, O8, G1, G5, G7, C2, C3, C6, C7, C8 |
| 4 | `alpha_zero` | the gradient stiffness α = γ is set to 0 | **1** | C1a, C1, C1b, C2, C3, C4, C5, C6, C7, C8, C9 |
| 5 | `alpha_neq_gamma` | a second stiffness α = 2γ in front of (D·P)² alone | **1** | C1a, C1, C1b, C2, C3, C6, C7, C8 |
| 6 | `wrong_dispersion` | the transverse dispersion is taken as ω² = K/η, dropping γp² | **1** | S10, S11 |
| 7 | `no_pressure` | the c_s²k² term is dropped from the growth equation | **1** | O6, O7, O7b |
| 8 | `weyl_flat` | the clock term is assigned the P-operator weight 2w instead of w+2 | **1** | S7 |
| 9 | `c_s_elastic` | the medium's sound speed is identified with √(γ/η) instead of √(γρ_c) | **1** | O4 |

Reproduce:

```bash
cd deepseek_push/DS_FINAL_2026_10_21/A69_psector_sound
python3 a69_checks.py --json-out a69_results.json > a69.out   # 56/56, exit 0
for M in eta_eq_gamma no_W gamma_factor2 alpha_zero alpha_neq_gamma \
         wrong_dispersion no_pressure weyl_flat c_s_elastic; do
  python3 a69_checks.py --mutate $M > a69_MUTATE_$M.out; echo "$M $?"
done
```

## What each mutation is *for*

* **1 `eta_eq_gamma`** is the hypothesis the lane is testing. Under it the four (η,γ) pairs used by
  the diffeomorphism test collapse to one, so S3 ("four distinct c_T²") fails even though the action
  is still invariant. This is the mutation that shows the symmetry test is not secretly *assuming*
  η = γ: with the dial on the diagonal, the test can no longer distinguish two speeds.
* **2 `no_W`** removes the only object that breaks the constant-shift symmetry. S4 (the shift
  variation equals −a₀|c|), S5 (it is non-zero) and S6 (the |P|² coefficient is K) all fail. This is
  the load-bearing demonstration that the shift-symmetry obstruction is *computed from W*, not declared.
* **3 `gamma_factor2`** is the record's own historical failure mode (A27, "factor two"). It breaks the
  c_T² = m_T²L*²/2 identity (O1), the elastic speed (O4 reports 1.4149 × 0.72 m/s instead of 1.0 × 0.72 m/s), λ_C (O8), the quadrupole ratio (G1), α₁ (G5, G7) and every strong-coupling number
  (C2, C3, C6–C8). One dial, ten named checks.
* **4 `alpha_zero`** deletes the k⁴ mode: with α = 0 the scalar has ω² = 0 and no gradient energy.
  C1a–C1b (the UV limit is α/η) fail, and every p_sc number becomes inf.
* **5 `alpha_neq_gamma`** breaks the one relation the action *does* force (A68 D16: the two gradient
  operators share one stiffness). The UV speed becomes 2γ/η ≠ γ/η, so C1a–C1b fail, and the IR
  strong-coupling formula (which assumes α = γ = KL*²/2) no longer matches its closed form.
* **6 `wrong_dispersion`** uses ω² = K/η in the conservation check. Since the conservation law is
  ∂_tT⁰⁰ + ∂_iT⁰ⁱ = Ṗ·EOM, a wrong dispersion makes both sides non-zero by γp²/K ≈ 0.5 of the
  natural scale: S10 and S11 fail at exactly 2.500e-01, twelve orders above their tolerance.
* **7 `no_pressure`** removes the pressure term from the growth ODE. The suppression S(k) is then 1
  for every c_s², so the bisection cannot land on S = 0.95 and O6/O7/O7b fail.
* **8 `weyl_flat`** assigns the clock term the same weight as the three P operators. S7 (the measured
  exponents) fails by exactly 2, and the "no w is Weyl flat" conclusion would be lost.
* **9 `c_s_elastic`** is the identification the lane exists to adjudicate: is the medium's sound speed
  √(γ/η) or √(γρ_c)? Under it the elastic speed comes out 2.998 × 10⁸ m/s and O4 fails against
  A16/A20's 0.72 m/s.

## Checks that were deleted because they could not be made to fail

Two candidate checks were written and **removed**:

* "w = p/ρ scales as ε" with the *declared* value w = γd/2 — replaced by O3, which computes the
  ratio w(ε)/w(ε/10) = 10 from the potential itself. A declared formula cannot fail.
* "the slip at O(ε) is zero" stated as `got = 0.0` — replaced by G2/G3b, which compute the traceless
  part of the stress tensor for two explicit profiles and for two amplitudes (the quadrupole must
  vanish for P ∝ x, and must scale as ε²). A declared zero cannot fail.

Everything in `a69_checks.py` now evaluates an expression and compares it to a second, independently
obtained number.
