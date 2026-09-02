# The graviton-bath CTP nonlinear drift — VERDICT (2026-09-01): the last κ lane is closed

**Asked:** evaluate the cubic-order graviton-bath influence functional in de Sitter with the nonlinear worldline coupling
— the one lane the corpus had identified where a rational κ = ½ was even the right kind of number
(`real_research/reviews/mi_cubic_noise_ctp_2026.py`, `mi_ctp_variational_2026.py`).
**Script:** `graviton_bath_ctp_drift_2026.py` (rc=0, 21 checks; `MUTATE=1` makes T_GH ħ-free and breaks B2/B3/B5 → rc=1).

## Setup
Worldline S_pp = −mc²∫dτ√(1−h_uu), h_uu = h_μν u^μu^ν, expanded: g₁ = mc²/2, g₂ = mc²/8, g₃ = mc²/16 (exact). Graviton bath in
Bunch–Davies, seen by the static-patch worldline as thermal at k_BT(a) = (ħ/2πc)√(a²+c²H²) (Deser–Levin). CTP mean EOM:
dissipation kernel from the commutator (state-independent, ρ(ω)=ω/π²), noise kernel from the anticommutator; the noise reaches
the mean trajectory only through g₂h_uu² (the rectified drift ⟨g₂h²⟩ = g₂c₂). Universality screen passes: every gₙ ∝ m.

## Result — the drift exists, is computable, and cannot be a₀
⟨h_uu²⟩_th = (2n/3π)·ℓ_P²·(a² + c²H²), n ≤ O(1) the polarisation × tensor/kinematic factor.

| | finding | number |
|---|---|---|
| **B ħ-counting theorem** | the dissipation kernel D = g₁²⟨[h,h]⟩/ħ is ħ-free and H-free (Λ-blind); the Bose factor ħω/2k_BT = πω/√(a²+H²) is ħ-free because T_GH ∝ ħ; so the noise, and every Λ-dependent term at every order (k insertions ⇒ (32πGħ)^{k/2}), is O(ħ^{≥1}) | lim_{ħ→0}(Λ-dependent EOM) = 0 |
| **C magnitude** | drift/(H²r) = (n/6π)(ℓ_P H_Λ/c)² = n/(6 S_dS); the missing factor is exactly the de Sitter entropy (1/(ℓ_P H/c)² = S_dS/π) | 5.0e−124·n; at 1 kpc the drift is 5e−140 m/s², a₀/drift = 10^129 |
| **C shape in r** | ∝ r: a renormalisation δΛ/Λ = n/6S_dS, not a constant acceleration | — |
| **D shape in a** | the bath gives f(T) = T² (the variance): I(a) = f(T(a)) − f(T_GH) is purely quadratic, c1p = ∞, so the crossover master formula gives q = 0: no Newtonian limit, no interpolation function; the H² piece is a constant in L (no force), the a² piece a higher-derivative term of weight (n/6π)(ℓ_Pω/c)² | 1.4e−118 |
| **D location** | even the T(a) crossover a = cH_Λ would be κ = √(8π/3) = 2.894 | EXCLUDED (a₀ = 5.4e−10) |

## Rescues, priced
- **E1 induced inertia** (f = T, Milgrom 1999): a₀ = 2cH_Λ, κ = 5.79, excluded; and MI-as-fundamental is out at 21σ (lensing).
- **E2 holographic/coherent response**: needs an enhancement of 6S_dS/n ≈ 2e123, i.e. all horizon degrees of freedom acting
  coherently — a new postulate (category III medium; Verlinde-class), amplitude and relaxation time free inputs.
- **E3 dS IR secular growth** of ⟨h²⟩: O(1) only after ~1e122 e-folds; today Ht ~ 1.
- **E4 primordial tensor background**: capped at ⟨h²⟩ ≤ rA_s = 7.6e−11 and an initial condition, not Λ.

## Standing
**Every named derivation lane for κ = ½ is now closed by a committed script**: the action (modulus theorem,
`A0_PROMOTION_VERDICT.md`), the in-action postulates (excluded or empty), and the graviton-bath CTP drift (ħ-suppressed by 1/S_dS,
shapeless). κ is a **measured constitutive number**, 0.465±0.076 (BTFR) / 0.551±0.043 (distance-free). This is not "theory closed":
the kernel, the a₀(z) ∝ √ρ_DE(z) prediction, the dark-field theorem and the cluster |Φ|-lever are untouched. Layer A untouched.
Cite: "a₀ = κc√(Gρ_Λ) with κ fitted; a₀ = c²√(Λ/32π) is the κ = ½ member."
