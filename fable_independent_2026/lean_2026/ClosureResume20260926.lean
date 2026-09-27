import Mathlib

/-!
# Closure-resume certificates, 2026-09-26

Scope: exact real algebra for the local linear gate and for simultaneous scalar
threshold constraints. These theorems do not derive a gate from an action,
identify a physical curvature/expansion solution, validate observational bounds,
or certify the full gravity theory.

The local gate is the c = 1, p = 1 expression used in the clean-path note:
  (9 R / (4 K^2)) (3 Λ / K^2) = 27 Λ R / (4 K^4).
Here R denotes the combined curvature/shear scalar in that note. The omitted
normalization by today's vacuum fraction can be absorbed into a positive cut.
The positivity and nonzero-expansion conditions below are explicit; K = 0 is
outside the asserted physical regime.

`vacuum_only_obstruction` excludes only a response that is a function of the
same vacuum input alone when incompatible response bounds are required. It
places no obstruction on the curvature/expansion-dependent gate. Its premise
that the two physical systems require incompatible responses is NOT derived.
The local gate's separate environment dependence is demonstrated by strict
monotonicity, scaling, and explicit on/off witnesses with fixed Λ and K.

`four_epoch_window_iff` is an abstract four-constraint feasibility theorem.
Treating an empirical pass set as one scalar floor/cap remains an input. The
fourth floor is optional for applications; it does not formalize the numerical
forest monotonicity/dominance assumption used by DE2. The rational example is a
nonvacuity test, not a fit to data.

The final group differentiates the exact exponential constitutive law on its
branch x > 1. With t(x) = x (1 - exp(-x)) and h(x) = x exp(-x), any
differentiable response reproducing h along t locally must have negative
derivative. This conflicts with a strictly positive constitutive-derivative
requirement. It is not a no-go theorem for other kernels or other health
conditions, and does not derive the C-H/K scalar block from an action.
-/

namespace ClosureResume20260926

noncomputable def localGate (R K Λ : ℝ) : ℝ := 27 * Λ * R / (4 * K ^ 4)

theorem local_gate_product (R K Λ : ℝ) (hK : K ≠ 0) :
    (9 * R / (4 * K ^ 2)) * (3 * Λ / K ^ 2) = localGate R K Λ := by
  unfold localGate
  field_simp
  ring

theorem vacuum_only_obstruction {V : Type*} (response : V → ℝ) (v : V)
    (lower upper : ℝ) (hgap : upper < lower) :
    ¬ (lower ≤ response v ∧ response v ≤ upper) := by
  rintro ⟨hlower, hupper⟩
  linarith

theorem local_gate_curvature_strict (R₁ R₂ K Λ : ℝ)
    (hΛ : 0 < Λ) (hK : K ≠ 0) (hR : R₁ < R₂) :
    localGate R₁ K Λ < localGate R₂ K Λ := by
  unfold localGate
  apply (div_lt_div_iff_of_pos_right (by positivity : 0 < 4 * K ^ 4)).2
  exact mul_lt_mul_of_pos_left hR (by positivity)

theorem local_gate_expansion_scaling (R K Λ t : ℝ) (hK : K ≠ 0) (ht : t ≠ 0) :
    localGate R (t * K) Λ = localGate R K Λ / t ^ 4 := by
  unfold localGate
  field_simp

theorem local_gate_environment_witnesses (K Λ cut : ℝ)
    (hK : K ≠ 0) (hΛ : 0 < Λ) (hcut : 0 < cut) :
    ∃ Roff Ron : ℝ, 0 ≤ Roff ∧ 0 ≤ Ron ∧
      localGate Roff K Λ < cut ∧ cut ≤ localGate Ron K Λ := by
  refine ⟨0, cut * (4 * K ^ 4) / (27 * Λ), le_rfl, by positivity, ?_, ?_⟩
  · simpa [localGate] using hcut
  · have hvalue : localGate (cut * (4 * K ^ 4) / (27 * Λ)) K Λ = cut := by
      unfold localGate
      field_simp
    exact hvalue.ge

theorem four_epoch_window_iff (aK aS aF aL XK XS XF XL : ℝ)
    (hK : 0 < aK) (hS : 0 < aS) (hF : 0 < aF) (hL : 0 < aL)
    (hXS : 0 < XS) :
    (∃ x : ℝ, 0 < x ∧ x * aK ≤ XK ∧ XS ≤ x * aS ∧
      x * aF ≤ XF ∧ XL ≤ x * aL) ↔
    max (XS / aS) (XL / aL) ≤ min (XK / aK) (XF / aF) := by
  constructor
  · rintro ⟨x, _hx, hupperK, hlowerS, hupperF, hlowerL⟩
    have hmax : max (XS / aS) (XL / aL) ≤ x := by
      apply max_le
      · exact (div_le_iff₀ hS).2 hlowerS
      · exact (div_le_iff₀ hL).2 hlowerL
    have hmin : x ≤ min (XK / aK) (XF / aF) := by
      apply le_min
      · exact (le_div_iff₀ hK).2 hupperK
      · exact (le_div_iff₀ hF).2 hupperF
    exact hmax.trans hmin
  · intro hwindow
    refine ⟨max (XS / aS) (XL / aL), ?_, ?_, ?_, ?_, ?_⟩
    · exact lt_of_lt_of_le (div_pos hXS hS) (le_max_left _ _)
    · exact (le_div_iff₀ hK).1 (hwindow.trans (min_le_left _ _))
    · exact (div_le_iff₀ hS).1 (le_max_left _ _)
    · exact (le_div_iff₀ hF).1 (hwindow.trans (min_le_right _ _))
    · exact (div_le_iff₀ hL).1 (le_max_right _ _)

theorem four_epoch_window_nonvacuous :
    ∃ x : ℝ, 0 < x ∧ x * 1 ≤ 3 ∧ 4 ≤ x * 2 ∧
      x * 4 ≤ 9 ∧ 3 ≤ x * 2 := by
  refine ⟨2, ?_⟩
  norm_num

theorem four_epoch_window_empty_example :
    ¬ ∃ x : ℝ, 0 < x ∧ x * 1 ≤ 3 ∧ 4 ≤ x * 1 ∧
      x * 4 ≤ 9 ∧ 3 ≤ x * 2 := by
  rintro ⟨x, _hx, hK, hS, _hF, _hL⟩
  linarith

noncomputable def sourceParam (x : ℝ) : ℝ := x * (1 - Real.exp (-x))
noncomputable def phantomParam (x : ℝ) : ℝ := x * Real.exp (-x)

theorem phantom_param_hasDerivAt (x : ℝ) :
    HasDerivAt phantomParam ((1 - x) * Real.exp (-x)) x := by
  have he : HasDerivAt (fun y : ℝ => Real.exp (-y)) (-Real.exp (-x)) x := by
    simpa using ((hasDerivAt_id x).neg.exp)
  have hm : HasDerivAt (fun y : ℝ => y * Real.exp (-y))
      (Real.exp (-x) + x * (-Real.exp (-x))) x := by
    convert! (hasDerivAt_id x).mul he using 1 <;> simp
  have heq : Real.exp (-x) + x * (-Real.exp (-x)) = (1 - x) * Real.exp (-x) := by ring
  rw [heq] at hm
  exact hm

theorem source_param_hasDerivAt (x : ℝ) :
    HasDerivAt sourceParam (1 + (x - 1) * Real.exp (-x)) x := by
  have hf : sourceParam = fun y : ℝ => y - phantomParam y := by
    funext y
    simp [sourceParam, phantomParam]
    ring
  rw [hf]
  have heq : 1 - ((1 - x) * Real.exp (-x)) = 1 + (x - 1) * Real.exp (-x) := by ring
  rw [← heq]
  exact (hasDerivAt_id x).sub (phantom_param_hasDerivAt x)

theorem source_param_derivative_positive (x : ℝ) (hx : 1 < x) :
    0 < 1 + (x - 1) * Real.exp (-x) := by
  have hprod : 0 < (x - 1) * Real.exp (-x) := mul_pos (by linarith) (Real.exp_pos _)
  linarith

theorem exponential_slope_formula (x : ℝ) (hx : 1 < x) :
    ((1 - x) * Real.exp (-x)) / (1 + (x - 1) * Real.exp (-x)) =
      (1 - x) / (Real.exp x + x - 1) := by
  have hd : 0 < Real.exp x + x - 1 := by linarith [Real.exp_pos x]
  have he : Real.exp (-x) * Real.exp x = 1 := by
    rw [← Real.exp_add, neg_add_cancel, Real.exp_zero]
  apply (div_eq_div_iff (ne_of_gt (source_param_derivative_positive x hx)) (ne_of_gt hd)).2
  calc
    (1 - x) * Real.exp (-x) * (Real.exp x + x - 1) =
        (1 - x) * (Real.exp (-x) * Real.exp x) + (1 - x) * (x - 1) * Real.exp (-x) := by ring
    _ = (1 - x) * (1 + (x - 1) * Real.exp (-x)) := by rw [he]; ring

theorem exponential_slope_negative (x : ℝ) (hx : 1 < x) :
    (1 - x) / (Real.exp x + x - 1) < 0 := by
  apply div_neg_of_neg_of_pos (by linarith)
  linarith [Real.exp_pos x]

theorem exact_exponential_response_derivative (response : ℝ → ℝ) (x C : ℝ)
    (hx : 1 < x) (hd : HasDerivAt response C (sourceParam x))
    (hmatch : ∀ᶠ y in nhds x, response (sourceParam y) = phantomParam y) :
    C = (1 - x) / (Real.exp x + x - 1) ∧ C < 0 := by
  have hcomp := hd.comp x (source_param_hasDerivAt x)
  have heq : phantomParam =ᶠ[nhds x] (fun y => response (sourceParam y)) := by
    filter_upwards [hmatch] with y hy
    exact hy.symm
  have hsame : HasDerivAt phantomParam (C * (1 + (x - 1) * Real.exp (-x))) x :=
    hcomp.congr_of_eventuallyEq heq
  have hchain := hsame.unique (phantom_param_hasDerivAt x)
  have hdt := source_param_derivative_positive x hx
  have hratio : C = ((1 - x) * Real.exp (-x)) / (1 + (x - 1) * Real.exp (-x)) :=
    (eq_div_iff (ne_of_gt hdt)).2 hchain
  rw [exponential_slope_formula x hx] at hratio
  refine ⟨hratio, ?_⟩
  rw [hratio]
  exact exponential_slope_negative x hx

theorem exact_exponential_incompatible_with_positive_C (response : ℝ → ℝ) (x C : ℝ)
    (hx : 1 < x) (hd : HasDerivAt response C (sourceParam x))
    (hmatch : ∀ᶠ y in nhds x, response (sourceParam y) = phantomParam y) :
    ¬ 0 < C := by
  have hnegative := (exact_exponential_response_derivative response x C hx hd hmatch).2
  linarith

theorem exponential_slope_at_two :
    (1 - (2 : ℝ)) / (Real.exp 2 + 2 - 1) = -1 / (Real.exp 2 + 1) := by
  congr 1 <;> ring

#print axioms local_gate_product
#print axioms vacuum_only_obstruction
#print axioms local_gate_curvature_strict
#print axioms local_gate_expansion_scaling
#print axioms local_gate_environment_witnesses
#print axioms four_epoch_window_iff
#print axioms four_epoch_window_nonvacuous
#print axioms four_epoch_window_empty_example
#print axioms phantom_param_hasDerivAt
#print axioms source_param_hasDerivAt
#print axioms source_param_derivative_positive
#print axioms exponential_slope_formula
#print axioms exponential_slope_negative
#print axioms exact_exponential_response_derivative
#print axioms exact_exponential_incompatible_with_positive_C
#print axioms exponential_slope_at_two

end ClosureResume20260926
