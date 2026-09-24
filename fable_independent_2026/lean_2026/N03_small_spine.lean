import Mathlib

/-!
# N03 — The small algebraic spine, machine-checked

Scope (per lean-math-certification / deepseek-lean-certificates, lane
`deepseek_push/L01* / L02* / M05* / J11*`): the SURVIVING small algebra of the
volume/central window-ratio family — no transport machinery, only the real
arithmetic these claims sit on:

* **The Thomson-kernel moments (L01, central-source N=1 sector).**
  `thomsonKernel μ = (3/8)(1+μ²)` is the normalized Thomson scattering kernel on
  μ ∈ [−1,1] (∫ p dμ = 1, CERTIFIED as `n03KernelNormalized`).  The L01 anchor
  E[(1−μ)²] = 7/5 is CERTIFIED as the exact one-dimensional polynomial integral
  `n03SecondMoment`; the companions E[1−μ] = 1 (`n03FirstMoment`, base of the
  L02 fact E[ang] = E[N]) and E[μ] = 0 (`n03MeanMu`, base of the L02 fact
  E[d_j] = 0 for j < N) are certified.  The task's literal phrasing "½ × the
  integral" is CHECKED and REFUTED: `n03SecondMomentHalf` shows the ½-sealed
  value is 7/10, and `n03SecondMomentHalfNotSevenFifths` certifies it ≠ 7/5 —
  the ½ does not belong, since (3/8)(1+μ²) is already normalized.  The L01
  leading algebra R−1 = (7/5)/(τ₀(1+q/3)) − 1 is CERTIFIED as
  `n03L01RatioLead` (exact field identity on the assembled E[D], E[ang],
  E[D·ang] formulas).

* **The M05 first-flight moment sequence (volume source).**
  ⟨chord⟩ = 3/4, E[∫r²ds] = 5/12, E[∫r⁴ds] = 1/4 (quadrature ladder ng=1024 →
  0.7500000000003 / 0.41666666667 / 0.25000000000; M05_FIRST_FLIGHT_MOMENTS.md).
  The FULL 2D statements stay CONJECTURED (formally stated as Props, zero
  axioms): the analytic reduction passes through the change of variables
  (r,μ) ↦ (u,w) = (rμ, r√(1−μ²)) on the quarter unit disk, and **no 2D
  change-of-variables theorem exists for mathlib's interval integrals in this
  toolchain** (checked: this build's interval-integral cache has no
  `integral_pow`/`integral_id` value lemmas either — the FTC route used
  below is `intervalIntegral.integral_deriv_eq_sub'`).  What **IS** certified
  is the entire one-dimensional polynomial tail of the reduction: after
  integrating out the u-direction (the μ-odd parts vanish — certified
  piecewise by `n03ChordMuLinearVanishes`), the three moments reduce to
  ∫₀¹ w(1−w²)dw = 1/4, ∫₀¹ w(1−w²)(1+2w²)dw = 5/12 and
  ∫₀¹ w(1−w²)(1−2w²+4w⁴)dw = 1/4 — ALL THREE as `n03M05ChordCore`,
  `n03M05R2Core`, `n03M05R4Core` (plus the rescaled `n03M05ChordTimesThree`),
  exact one-dimensional polynomial integrals.  The chord moment 3/4 =
  3·∫₀¹w(1−w²)dw is thereby certified exactly up to the single 2D change of
  variables.

* **The L02 Q-decomposition (N = 1 sector).**  Q(N) = Σ_{j=0}^{N} ℓ_j (u_j·u_N);
  the split Q = ℓ_N·(u_N·u_N) + Σ_{j<N} ℓ_j (u_j·u_N) is CERTIFIED as `qSplit`,
  the unit-final-direction fact ⟪u,u⟫ = 1 is CERTIFIED as `dotSelfUnit`
  (Euclidean inner product), the headline decomposition Q = ℓ_N + Σ_{j<N}
  ℓ_j(u_j·u_N) as `qDecomp`, and the N=1 two-line case
  Q = ℓ₀·(u₀·u₁) + ℓ₁ as `qN1` / `qN1Unit`.  (L02's E[Q] itself is a measured
  functional with no closed form — out of scope here.)

Angle brackets denote expectation over the kernel/geometry in question.  Lean
certifies the mathematics, not that the formulas model radiation transfer;
everything above is the algebraic spine the physics lane sits on.

Zero `sorry`; axioms ⊆ {propext, Classical.choice, Quot.sound} (verified by
`#print axioms` at the end of the file).
-/

namespace N03

noncomputable section

open scoped intervalIntegral
open scoped RealInnerProductSpace

/-! ## 1&2. FTC engine: exact polynomial integrals on [−1,1] and [0,1].
The one-dimensional integrals are evaluated by the fundamental theorem
(`intervalIntegral.integral_deriv_eq_sub'`) with the antiderivatives written as
function-level sums of monomial terms; `deriv` is computed termwise from the
`_field` lemmas (no instance gymnastics). -/

/-- Antiderivative of the quartic polynomial (function-level sum). -/
def quadAnti (c0 c1 c2 c3 c4 : ℝ) : ℝ → ℝ :=
  (fun y : ℝ => c0 * y) + (fun y : ℝ => (c1 / 2) * y ^ 2) +
    (fun y : ℝ => (c2 / 3) * y ^ 3) + (fun y : ℝ => (c3 / 4) * y ^ 4) +
    (fun y : ℝ => (c4 / 5) * y ^ 5)

/-- The quartic polynomial itself. -/
def quadPolyF (c0 c1 c2 c3 c4 : ℝ) : ℝ → ℝ :=
  fun x : ℝ => c0 + c1 * x + c2 * x ^ 2 + c3 * x ^ 3 + c4 * x ^ 4

/-- deriv (quadAnti) = quadPolyF, termwise. -/
lemma n03_deriv_quadAnti (c0 c1 c2 c3 c4 : ℝ) : deriv (quadAnti c0 c1 c2 c3 c4) = quadPolyF c0 c1 c2 c3 c4 := by
  funext x
  unfold quadAnti quadPolyF
  rw [deriv_add (by fun_prop : DifferentiableAt ℝ ((fun y : ℝ => c0 * y) + (fun y : ℝ => (c1 / 2) * y ^ 2) + (fun y : ℝ => (c2 / 3) * y ^ 3) + (fun y : ℝ => (c3 / 4) * y ^ 4)) x)
                (by fun_prop : DifferentiableAt ℝ (fun y : ℝ => (c4 / 5) * y ^ 5) x)]
  rw [deriv_add (by fun_prop : DifferentiableAt ℝ ((fun y : ℝ => c0 * y) + (fun y : ℝ => (c1 / 2) * y ^ 2) + (fun y : ℝ => (c2 / 3) * y ^ 3)) x)
                (by fun_prop : DifferentiableAt ℝ (fun y : ℝ => (c3 / 4) * y ^ 4) x)]
  rw [deriv_add (by fun_prop : DifferentiableAt ℝ ((fun y : ℝ => c0 * y) + (fun y : ℝ => (c1 / 2) * y ^ 2)) x)
                (by fun_prop : DifferentiableAt ℝ (fun y : ℝ => (c2 / 3) * y ^ 3) x)]
  rw [deriv_add (by fun_prop : DifferentiableAt ℝ (fun y : ℝ => c0 * y) x)
                (by fun_prop : DifferentiableAt ℝ (fun y : ℝ => (c1 / 2) * y ^ 2) x)]
  change deriv (fun y : ℝ => c0 * id y) x + deriv (fun y : ℝ => (c1 / 2) * y ^ 2) x +
      deriv (fun y : ℝ => (c2 / 3) * y ^ 3) x + deriv (fun y : ℝ => (c3 / 4) * y ^ 4) x +
      deriv (fun y : ℝ => (c4 / 5) * y ^ 5) x
      = c0 + c1 * x + c2 * x ^ 2 + c3 * x ^ 3 + c4 * x ^ 4
  simp_rw [deriv_const_mul_field, deriv_pow_field, deriv_id]
  simp
  ring_nf

/-- Differentiability of the quartic antiderivative everywhere. -/
lemma n03_diff_quadAnti (c0 c1 c2 c3 c4 x : ℝ) : DifferentiableAt ℝ (quadAnti c0 c1 c2 c3 c4) x := by
  unfold quadAnti
  fun_prop

/-- Continuity of the quartic polynomial on [−1,1]. -/
lemma n03_cont_quadPoly (c0 c1 c2 c3 c4 : ℝ) :
    ContinuousOn (quadPolyF c0 c1 c2 c3 c4) (Set.uIcc (-1) 1) := by
  unfold quadPolyF
  apply ContinuousOn.mono (by continuity :
    ContinuousOn (fun x : ℝ => c0 + c1 * x + c2 * x ^ 2 + c3 * x ^ 3 + c4 * x ^ 4) Set.univ)
  intro x hx
  simp

/-- Exact quartic integral on [−1,1]: ∫(c0 + c1x + c2x² + c3x³ + c4x⁴) = 2c0 + (2/3)c2 + (2/5)c4.
    The odd powers integrate to zero; the even ones pick up 2, 2/3, 2/5. -/
lemma n03_int_quad_neg11 (c0 c1 c2 c3 c4 : ℝ) :
    (∫ x in (-1 : ℝ)..1, c0 + c1 * x + c2 * x ^ 2 + c3 * x ^ 3 + c4 * x ^ 4)
      = 2 * c0 + (2 : ℝ) / 3 * c2 + (2 : ℝ) / 5 * c4 := by
  rw [intervalIntegral.integral_deriv_eq_sub' (quadAnti c0 c1 c2 c3 c4)]
  · dsimp [quadAnti]
    norm_num <;> ring_nf
  · exact n03_deriv_quadAnti c0 c1 c2 c3 c4
  · intro x hx
    exact n03_diff_quadAnti c0 c1 c2 c3 c4 x
  · exact n03_cont_quadPoly c0 c1 c2 c3 c4

/-- Antiderivative of the odd polynomial (function-level sum). -/
def oddAnti (a1 a3 a5 a7 : ℝ) : ℝ → ℝ :=
  (fun y : ℝ => (a1 / 2) * y ^ 2) + (fun y : ℝ => (a3 / 4) * y ^ 4) +
    (fun y : ℝ => (a5 / 6) * y ^ 6) + (fun y : ℝ => (a7 / 8) * y ^ 8)

/-- The odd polynomial itself. -/
def oddPolyF (a1 a3 a5 a7 : ℝ) : ℝ → ℝ :=
  fun x : ℝ => a1 * x + a3 * x ^ 3 + a5 * x ^ 5 + a7 * x ^ 7

/-- deriv (oddAnti) = oddPolyF, termwise. -/
lemma n03_deriv_oddAnti (a1 a3 a5 a7 : ℝ) : deriv (oddAnti a1 a3 a5 a7) = oddPolyF a1 a3 a5 a7 := by
  funext x
  unfold oddAnti oddPolyF
  rw [deriv_add (by fun_prop : DifferentiableAt ℝ ((fun y : ℝ => (a1 / 2) * y ^ 2) + (fun y : ℝ => (a3 / 4) * y ^ 4) + (fun y : ℝ => (a5 / 6) * y ^ 6)) x)
                (by fun_prop : DifferentiableAt ℝ (fun y : ℝ => (a7 / 8) * y ^ 8) x)]
  rw [deriv_add (by fun_prop : DifferentiableAt ℝ ((fun y : ℝ => (a1 / 2) * y ^ 2) + (fun y : ℝ => (a3 / 4) * y ^ 4)) x)
                (by fun_prop : DifferentiableAt ℝ (fun y : ℝ => (a5 / 6) * y ^ 6) x)]
  rw [deriv_add (by fun_prop : DifferentiableAt ℝ (fun y : ℝ => (a1 / 2) * y ^ 2) x)
                (by fun_prop : DifferentiableAt ℝ (fun y : ℝ => (a3 / 4) * y ^ 4) x)]
  simp_rw [deriv_const_mul_field, deriv_pow_field]
  ring_nf

/-- Differentiability of the odd antiderivative everywhere. -/
lemma n03_diff_oddAnti (a1 a3 a5 a7 x : ℝ) : DifferentiableAt ℝ (oddAnti a1 a3 a5 a7) x := by
  unfold oddAnti
  fun_prop

/-- Continuity of the odd polynomial on [0,1]. -/
lemma n03_cont_oddPoly (a1 a3 a5 a7 : ℝ) :
    ContinuousOn (oddPolyF a1 a3 a5 a7) (Set.uIcc 0 1) := by
  unfold oddPolyF
  apply ContinuousOn.mono (by continuity :
    ContinuousOn (fun x : ℝ => a1 * x + a3 * x ^ 3 + a5 * x ^ 5 + a7 * x ^ 7) Set.univ)
  intro x hx
  simp

/-- Exact odd-polynomial integral on [0,1]: ∫₀¹(a1x + a3x³ + a5x⁵ + a7x⁷) = a1/2 + a3/4 + a5/6 + a7/8. -/
lemma n03_int_odd_01 (a1 a3 a5 a7 : ℝ) :
    (∫ x in (0 : ℝ)..1, a1 * x + a3 * x ^ 3 + a5 * x ^ 5 + a7 * x ^ 7)
      = a1 / 2 + a3 / 4 + a5 / 6 + a7 / 8 := by
  rw [intervalIntegral.integral_deriv_eq_sub' (oddAnti a1 a3 a5 a7)]
  · dsimp [oddAnti]
    norm_num <;> ring_nf
  · exact n03_deriv_oddAnti a1 a3 a5 a7
  · intro x hx
    exact n03_diff_oddAnti a1 a3 a5 a7 x
  · exact n03_cont_oddPoly a1 a3 a5 a7

/-! ## 3. Thomson-kernel moments (L01, N=1 sector; all certified). -/

/-- Thomson scattering kernel on μ ∈ [−1,1], normalized: ∫ p dμ = 1. -/
def thomsonKernel (μ : ℝ) : ℝ := (3 : ℝ) / 8 * (1 + μ ^ 2)

/-- Normalization: ∫_{−1}^{1} (3/8)(1+μ²) dμ = 1. -/
theorem n03KernelNormalized : (∫ μ in (-1 : ℝ)..1, thomsonKernel μ) = 1 := by
  have hp : (∫ μ in (-1 : ℝ)..1, thomsonKernel μ)
      = (∫ μ in (-1 : ℝ)..1, (3 : ℝ) / 8 + (0 : ℝ) * μ + (3 : ℝ) / 8 * μ ^ 2 +
          (0 : ℝ) * μ ^ 3 + (0 : ℝ) * μ ^ 4) := by
    apply intervalIntegral.integral_congr
    intro μ _
    unfold thomsonKernel
    ring
  rw [hp]
  rw [n03_int_quad_neg11]
  norm_num

/-- E[μ] = 0 under the Thomson kernel (mean-zero kick; the base of the L02
    exact fact E[d_j] = 0 for every j < N). -/
theorem n03MeanMu : (∫ μ in (-1 : ℝ)..1, thomsonKernel μ * μ) = 0 := by
  have hp : (∫ μ in (-1 : ℝ)..1, thomsonKernel μ * μ)
      = (∫ μ in (-1 : ℝ)..1, (0 : ℝ) + (3 : ℝ) / 8 * μ + (0 : ℝ) * μ ^ 2 +
          (3 : ℝ) / 8 * μ ^ 3 + (0 : ℝ) * μ ^ 4) := by
    apply intervalIntegral.integral_congr
    intro μ _
    unfold thomsonKernel
    ring
  rw [hp]
  rw [n03_int_quad_neg11]
  norm_num

/-- E[1−μ] = 1 under the Thomson kernel (per-kick aiming loss; base of E[ang] = E[N]). -/
theorem n03FirstMoment : (∫ μ in (-1 : ℝ)..1, thomsonKernel μ * (1 - μ)) = 1 := by
  have hp : (∫ μ in (-1 : ℝ)..1, thomsonKernel μ * (1 - μ))
      = (∫ μ in (-1 : ℝ)..1, (3 : ℝ) / 8 + (-(3 : ℝ) / 8) * μ + (3 : ℝ) / 8 * μ ^ 2 +
          (-(3 : ℝ) / 8) * μ ^ 3 + (0 : ℝ) * μ ^ 4) := by
    apply intervalIntegral.integral_congr
    intro μ _
    unfold thomsonKernel
    ring
  rw [hp]
  rw [n03_int_quad_neg11]
  norm_num

/-- **THE L01 anchor**: E[(1−μ)²] = 7/5 under the Thomson kernel (3/8)(1+μ²).
    The task asked whether ½·∫(3/8)(1+μ²)(1−μ)² dμ = 7/5; what is true is that
    the UNSCALED expectation integral (the kernel is already normalized, so no
    extra ½ belongs) equals 7/5 exactly.  One-dimensional polynomial integral,
    certified by the FTC (integral_deriv_eq_sub'); no calculus-special lemmas. -/
theorem n03SecondMoment : (∫ μ in (-1 : ℝ)..1, thomsonKernel μ * (1 - μ) ^ 2) = (7 : ℝ) / 5 := by
  have hp : (∫ μ in (-1 : ℝ)..1, thomsonKernel μ * (1 - μ) ^ 2)
      = (∫ μ in (-1 : ℝ)..1, (3 : ℝ) / 8 + (-(3 : ℝ) / 4) * μ + (3 : ℝ) / 4 * μ ^ 2 +
          (-(3 : ℝ) / 4) * μ ^ 3 + (3 : ℝ) / 8 * μ ^ 4) := by
    apply intervalIntegral.integral_congr
    intro μ _
    unfold thomsonKernel
    ring
  rw [hp]
  rw [n03_int_quad_neg11]
  norm_num

/-- The literal "½ × the integral" of the task phrase: its true value is 7/10,
    not 7/5 (the ½ is spurious — the kernel (3/8)(1+μ²) already sums to 1). -/
theorem n03SecondMomentHalf : (1 : ℝ) / 2 * (∫ μ in (-1 : ℝ)..1, thomsonKernel μ * (1 - μ) ^ 2) = (7 : ℝ) / 10 := by
  rw [n03SecondMoment]
  norm_num

/-- Certified refutation of the "½ × integral = 7/5" phrasing. -/
theorem n03SecondMomentHalfNotSevenFifths :
    (1 : ℝ) / 2 * (∫ μ in (-1 : ℝ)..1, thomsonKernel μ * (1 - μ) ^ 2) ≠ (7 : ℝ) / 5 := by
  rw [n03SecondMoment]
  norm_num

/-- The μ-linear term of the chord integral integrates to zero (odd on [−1,1]);
    a certified piece of the chord-moment analytic reduction (M01 / J11). -/
theorem n03ChordMuLinearVanishes (r : ℝ) : (∫ μ in (-1 : ℝ)..1, r * μ) = 0 := by
  have hp : (∫ μ in (-1 : ℝ)..1, r * μ)
      = (∫ μ in (-1 : ℝ)..1, (0 : ℝ) + r * μ + (0 : ℝ) * μ ^ 2 + (0 : ℝ) * μ ^ 3 + (0 : ℝ) * μ ^ 4) := by
    apply intervalIntegral.integral_congr
    intro μ _
    ring
  rw [hp]
  rw [n03_int_quad_neg11]
  norm_num

/-- L01 coefficient: r₁(q) = E[(1−μ)²]·(1/2 + q/4) = (7/5)(1/2 + q/4). -/
theorem n03R1q (q : ℝ) :
    (∫ μ in (-1 : ℝ)..1, thomsonKernel μ * (1 - μ) ^ 2) * (1 / 2 + q / 4) = (7 : ℝ) / 5 * (1 / 2 + q / 4) := by
  rw [n03SecondMoment]

/-- L01 leading algebra: with E[D] = τ₀(1/2+q/4), E[ang] = τ₀(1+q/3) and the
    N=1 sector E[D·ang] = τ₀·r₁(q) = τ₀·(7/5)(1/2+q/4), the thin closure ratio
    reads R−1 = (7/5)/(τ₀(1+q/3)) − 1 exactly — the O(1) in the L01 expansion
    R−1 = (7/5)/[(1+q/3)τ₀] − 1 + O(1) is the coefficient of τ₀⁰. -/
theorem n03L01RatioLead (τ₀ q : ℝ) (hτ : τ₀ ≠ 0) (h2 : 1 / 2 + q / 4 ≠ 0) (h3 : 1 + q / 3 ≠ 0) :
    (τ₀ * ((7 : ℝ) / 5 * (1 / 2 + q / 4))) / ((τ₀ * (1 / 2 + q / 4)) * (τ₀ * (1 + q / 3))) - 1
      = ((7 : ℝ) / 5) / (τ₀ * (1 + q / 3)) - 1 := by
  have h4q : 4 + 2 * q ≠ 0 := by
    have h2q : (2 : ℝ) + q ≠ 0 := by
      intro hz
      apply h2
      calc 1 / 2 + q / 4 = (2 + q) / 4 := by ring_nf
        _ = 0 / 4 := by rw [hz]
        _ = 0 := by norm_num
    intro hz
    apply mul_ne_zero (by norm_num : (2 : ℝ) ≠ 0) h2q
    rw [show (4 : ℝ) + 2 * q = 2 * (2 + q) from by ring] at hz
    exact hz
  have h3q : 3 + q ≠ 0 := by
    intro hz
    apply h3
    calc 1 + q / 3 = (3 + q) / 3 := by ring_nf
      _ = 0 / 3 := by rw [hz]
      _ = 0 := by norm_num
  have hcore : (τ₀ * ((7 : ℝ) / 5 * (1 / 2 + q / 4))) / ((τ₀ * (1 / 2 + q / 4)) * (τ₀ * (1 + q / 3)))
        = ((7 : ℝ) / 5) / (τ₀ * (1 + q / 3)) := by
    field_simp [hτ, h2, h3, h4q, h3q]
  rw [hcore]

/-! ## 4. The M05 first-flight moment cores (one-dimensional polynomial tail; certified). -/

/-- The chord-moment core: ∫₀¹ w(1−w²) dw = 1/4.  Both M05 anchors
    E[∫r⁴ds] = 1/4 and (×3) ⟨chord⟩ = 3/4 terminate in this integral once the
    u-direction is integrated out of the quarter-disk (2D change of variables
    not in mathlib's interval-integral toolkit — the exact blocker). -/
theorem n03M05ChordCore : (∫ w in (0 : ℝ)..1, w * (1 - w ^ 2)) = (1 : ℝ) / 4 := by
  have hp : (∫ w in (0 : ℝ)..1, w * (1 - w ^ 2))
      = (∫ w in (0 : ℝ)..1, (1 : ℝ) * w + (-(1 : ℝ)) * w ^ 3 + (0 : ℝ) * w ^ 5 + (0 : ℝ) * w ^ 7) := by
    apply intervalIntegral.integral_congr
    intro w _
    ring
  rw [hp]
  rw [n03_int_odd_01]
  norm_num

/-- ⟨chord⟩_vol = 3·∫₀¹ w(1−w²) dw = 3/4 — the full 1D core of the J11 chord
    anchor 0.750000 (up to the single 2D change of variables, CONJECTURED). -/
theorem n03M05ChordTimesThree : 3 * (∫ w in (0 : ℝ)..1, w * (1 - w ^ 2)) = (3 : ℝ) / 4 := by
  rw [n03M05ChordCore]
  norm_num

/-- E[∫r²ds] core: ∫₀¹ w(1−w²)(1+2w²) dw = 5/12 (M05 anchor 0.41666666667). -/
theorem n03M05R2Core : (∫ w in (0 : ℝ)..1, w * (1 - w ^ 2) * (1 + 2 * w ^ 2)) = (5 : ℝ) / 12 := by
  have hp : (∫ w in (0 : ℝ)..1, w * (1 - w ^ 2) * (1 + 2 * w ^ 2))
      = (∫ w in (0 : ℝ)..1, (1 : ℝ) * w + (1 : ℝ) * w ^ 3 + (-(2 : ℝ)) * w ^ 5 + (0 : ℝ) * w ^ 7) := by
    apply intervalIntegral.integral_congr
    intro w _
    ring
  rw [hp]
  rw [n03_int_odd_01]
  norm_num

/-- E[∫r⁴ds] core: ∫₀¹ w(1−w²)(1−2w²+4w⁴) dw = 1/4 (M05 anchor 0.25000000000). -/
theorem n03M05R4Core : (∫ w in (0 : ℝ)..1, w * (1 - w ^ 2) * (1 - 2 * w ^ 2 + 4 * w ^ 4)) = (1 : ℝ) / 4 := by
  have hp : (∫ w in (0 : ℝ)..1, w * (1 - w ^ 2) * (1 - 2 * w ^ 2 + 4 * w ^ 4))
      = (∫ w in (0 : ℝ)..1, (1 : ℝ) * w + (-(3 : ℝ)) * w ^ 3 + (6 : ℝ) * w ^ 5 + (-(4 : ℝ)) * w ^ 7) := by
    apply intervalIntegral.integral_congr
    intro w _
    ring
  rw [hp]
  rw [n03_int_odd_01]
  norm_num

/-! ## 5. The M05 chord statements — formal, honest (CONJECTURED, zero axioms). -/

/-- chord(r,μ) = −rμ + √(1 − r²(1−μ²)): first-exit path length of a uniform
    interior point of the unit ball, direction with dot μ (sign per J11's
    corrected reading; the rμ-linear part integrates to zero, so the moment is
    sign-insensitive — see n03ChordMuLinearVanishes). -/
def chordVol (r μ : ℝ) : ℝ := -r * μ + Real.sqrt (1 - r ^ 2 * (1 - μ ^ 2))

/-- The volume-source chord moment: 3∫₀¹ r²·½∫₋₁¹ chord(r,μ) dμ dr. -/
def chordMomentVol : ℝ :=
  3 * (∫ r in (0 : ℝ)..1, r ^ 2 * (1 / 2 * (∫ μ in (-1 : ℝ)..1, chordVol r μ)))

/-- J11 anchor: ⟨chord⟩_vol = 3/4.  CONJECTURED-WITH-NUMERIC-EVIDENCE (a
    `def` : Prop — compiling, zero axioms): the 2D change of variables
    (r,μ) ↦ (r√(1−μ²), rμ) is not available for interval integrals in this
    toolchain.  The certified 1D tail is n03M05ChordCore/n03M05ChordTimesThree. -/
def chordMomentConjecture : Prop := chordMomentVol = (3 : ℝ) / 4

/-- ∫r² ds along the first flight: r²L + rμL² + L³/3, L = chord. -/
def intR2s (r μ : ℝ) : ℝ :=
  r ^ 2 * chordVol r μ + r * μ * chordVol r μ ^ 2 + chordVol r μ ^ 3 / 3

/-- E[∫r²ds]_vol = 3∫₀¹ r²·½∫₋₁¹ intR2s dμ dr. -/
def m05R2Mom : ℝ :=
  3 * (∫ r in (0 : ℝ)..1, r ^ 2 * (1 / 2 * (∫ μ in (-1 : ℝ)..1, intR2s r μ)))

/-- M05 anchor: E[∫r²ds] = 5/12.  CONJECTURED (2D change of variables);
    certified 1D tail: n03M05R2Core. -/
def m05R2Conjecture : Prop := m05R2Mom = (5 : ℝ) / 12

/-- ∫r⁴ ds along the first flight. -/
def intR4s (r μ : ℝ) : ℝ :=
  r ^ 4 * chordVol r μ + 2 * r ^ 3 * μ * chordVol r μ ^ 2 +
    (2 * r ^ 2 * μ ^ 2 + r ^ 2) * chordVol r μ ^ 3 / 3 +
    r * μ * chordVol r μ ^ 4 / 2 + chordVol r μ ^ 5 / 5

/-- E[∫r⁴ds]_vol. -/
def m05R4Mom : ℝ :=
  3 * (∫ r in (0 : ℝ)..1, r ^ 2 * (1 / 2 * (∫ μ in (-1 : ℝ)..1, intR4s r μ)))

/-- M05 anchor: E[∫r⁴ds] = 1/4.  CONJECTURED (2D change of variables);
    certified 1D tail: n03M05R4Core (the same polynomial integral as 3/4 core). -/
def m05R4Conjecture : Prop := m05R4Mom = (1 : ℝ) / 4

/-! ## 6. The Q-decomposition (L02), N = 1 sector (all certified). -/

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]

/-- Q(N) = Σ_{j=0}^{N} ℓ_j (u_j · u_N): the directional sum of a photon's
    flight segments against the final (escape) direction (L02 definition). -/
def qFull (N : ℕ) (l : ℕ → ℝ) (u : ℕ → E) : ℝ :=
  ∑ j ∈ Finset.range (N + 1), l j * ⟪u j, u N⟫

/-- Decomposition: Q = ℓ_N·(u_N·u_N) + Σ_{j<N} ℓ_j (u_j·u_N) — split off the
    final segment (j = N); pure finite-sum algebra. -/
theorem qSplit (N : ℕ) (l : ℕ → ℝ) (u : ℕ → E) :
    qFull N l u = l N * ⟪u N, u N⟫ + ∑ j ∈ Finset.range N, l j * ⟪u j, u N⟫ := by
  unfold qFull
  rw [Finset.sum_range_succ]
  ac_rfl

/-- A unit direction dots itself to 1: ⟪u,u⟫ = 1 whenever ‖u‖ = 1. -/
theorem dotSelfUnit {u : E} (hu : ‖u‖ = 1) : ⟪u, u⟫ = 1 := by
  rw [real_inner_self_eq_norm_sq, hu]
  norm_num

/-- **The L02 decomposition**: for a unit final direction, Q = ℓ_N + Σ_{j<N} ℓ_j
    (u_j·u_N) (the j = N term is ℓ_N·1). -/
theorem qDecomp (N : ℕ) (l : ℕ → ℝ) (u : ℕ → E) (hu : ‖u N‖ = 1) :
    qFull N l u = l N + ∑ j ∈ Finset.range N, l j * ⟪u j, u N⟫ := by
  rw [qSplit]
  rw [dotSelfUnit hu]
  ring

/-- N = 1 two-line algebra, general final direction:
    Q = ℓ₀·(u₀·u₁) + ℓ₁·(u₁·u₁). -/
theorem qN1 (l : ℕ → ℝ) (u : ℕ → E) :
    qFull 1 l u = l 0 * ⟪u 0, u 1⟫ + l 1 * ⟪u 1, u 1⟫ := by
  unfold qFull
  rw [Finset.sum_range_succ]
  rw [Finset.sum_range_one]

/-- **The N = 1 headline**: Q = ℓ₀·(u₀·u₁) + ℓ₁ for a unit escape direction
    (u₁·u₁ = 1). -/
theorem qN1Unit (l : ℕ → ℝ) (u : ℕ → E) (hu : ‖u 1‖ = 1) :
    qFull 1 l u = l 0 * ⟪u 0, u 1⟫ + l 1 := by
  unfold qFull
  rw [Finset.sum_range_succ]
  rw [Finset.sum_range_one]
  rw [real_inner_self_eq_norm_sq, hu]
  norm_num

#check chordMomentConjecture
#check m05R2Conjecture
#check m05R4Conjecture

#print axioms n03_deriv_quadAnti
#print axioms n03_diff_quadAnti
#print axioms n03_cont_quadPoly
#print axioms n03_int_quad_neg11
#print axioms n03_deriv_oddAnti
#print axioms n03_diff_oddAnti
#print axioms n03_cont_oddPoly
#print axioms n03_int_odd_01
#print axioms n03KernelNormalized
#print axioms n03MeanMu
#print axioms n03FirstMoment
#print axioms n03SecondMoment
#print axioms n03SecondMomentHalf
#print axioms n03SecondMomentHalfNotSevenFifths
#print axioms n03ChordMuLinearVanishes
#print axioms n03R1q
#print axioms n03L01RatioLead
#print axioms n03M05ChordCore
#print axioms n03M05ChordTimesThree
#print axioms n03M05R2Core
#print axioms n03M05R4Core
#print axioms qSplit
#print axioms dotSelfUnit
#print axioms qDecomp
#print axioms qN1
#print axioms qN1Unit