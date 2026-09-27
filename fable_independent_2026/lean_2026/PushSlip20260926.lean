import Mathlib

/-!
Scoped CD26-2 certificates for IC27/IC28 algebra. These statements do not
formalize the field-action variation, a PDE support theorem, the numerical
witness, or the full gravity theory. `p` below denotes spatial wave number
squared. The companion report supplies the bridge from the action.
-/
namespace PushSlip20260926

theorem two_curvatures_obstruct (F z R₁ R₂ : ℝ)
    (h₁ : F - 2 * z * R₁ = 0) (h₂ : F - 2 * z * R₂ = 0)
    (hz : z ≠ 0) : R₁ = R₂ := by
  have h : z * (R₁ - R₂) = 0 := by nlinarith
  have hR := (mul_eq_zero.mp h).resolve_left hz
  linarith

theorem retained_auxiliary_positive (A D E z : ℝ) (hA : A ≠ 0)
    (hD : 0 < D) (hE : 0 ≤ E) : 0 < A ^ 2 / (4 * D + 24 * E * z ^ 2) := by
  apply div_pos (sq_pos_of_ne_zero hA)
  positivity

theorem static_gap_identity (t D A : ℝ) (ht : t ≠ 0) (hD : D ≠ 0) :
    2 * D - 3 * A ^ 2 / t = 12 * D * (t / 6 - A ^ 2 / (4 * D)) / t := by
  field_simp
  ring

theorem static_gap_positive (t D A : ℝ) (ht : 0 < t) (hD : 0 < D)
    (hL : 0 < t / 6 - A ^ 2 / (4 * D)) : 0 < 2 * D - 3 * A ^ 2 / t := by
  rw [static_gap_identity t D A (ne_of_gt ht) (ne_of_gt hD)]
  positivity

theorem oscillator_coefficients_positive (a B C H v m : ℝ)
    (ha : 0 < a) (hB : 0 < B) (hC : 0 < C) (hH : 0 < H)
    (hv : B < v) (hm : 0 < m) (hCH : C < 2 * H)
    (hgap : 2 * a * m < C * (2 * H - C)) :
    0 < (C ^ 2 + 2 * a * m) * (C * (2 * H - C) - 2 * a * m) ∧
    0 < 8 * a * (B * C * (3 * H - C) + C ^ 2 * v + 2 * a * m * (v - B)) ∧
    0 < 16 * B * a ^ 2 * (2 * v - B) := by
  have hvp : 0 < v := lt_trans hB hv
  have hg : 0 < C * (2 * H - C) - 2 * a * m := sub_pos.mpr hgap
  have h3 : 0 < 3 * H - C := by linarith
  have hVB : 0 < v - B := sub_pos.mpr hv
  have h2 : 0 < 2 * v - B := by linarith
  constructor
  · positivity
  constructor <;> positivity

theorem positive_quadratic_every_wave (n₀ n₁ n₂ p : ℝ)
    (h₀ : 0 < n₀) (h₁ : 0 < n₁) (h₂ : 0 < n₂) (hp : 0 ≤ p) :
    0 < n₀ + n₁ * p + n₂ * p ^ 2 := by
  positivity

theorem second_channel_residue (H m a v C B : ℝ) (hB : B ≠ 0) :
    (-H - 4 * a * v * (-m / (2 * B)) / C) *
      (m + 2 * B * (-m / (2 * B))) - 2 * H * m = -2 * H * m := by
  have hz : m + 2 * B * (-m / (2 * B)) = 0 := by field_simp; ring
  rw [hz]
  ring

theorem expanding_regular_residue_nonzero (H m : ℝ) (hH : 0 < H) (hm : 0 < m) :
    -2 * H * m ≠ 0 := by
  have h : -2 * H * m < 0 := by nlinarith [mul_pos hH hm]
  exact ne_of_lt h

theorem physical_metric_tail_positive (H C m B : ℝ)
    (hH : 0 < H) (hCH : C < 2 * H) (hm : 0 < m) (hB : 0 < B) :
    0 < (H - C / 2) * H * m ^ 2 / B := by
  have hc : 0 < H - C / 2 := by linarith
  positivity

theorem exceptional_matter_schur_positive (rho P Psecond : ℝ)
    (hrho : 0 < rho) (hP : P < 0) (hsecond : 0 < Psecond) :
    0 < rho * (-Psecond / P) := by
  exact mul_pos hrho (div_pos_of_neg_of_neg (neg_neg_of_pos hsecond) hP)

theorem positive_schur_spatial_pole (M B : ℝ) (hM : 0 < M) (hB : 0 < B) :
    0 < M / (2 * B) ∧ M - 2 * B * (M / (2 * B)) = 0 := by
  constructor
  · positivity
  · field_simp
    ring

theorem exceptional_matter_low_k_negative (a C M : ℝ)
    (hM : 0 < M) (hsmall : 2 * a * M < C ^ 2) :
    a - C ^ 2 / (2 * M) < 0 := by
  have hd : 0 < 2 * M := by positivity
  have hh : a < C ^ 2 / (2 * M) := (lt_div_iff₀ hd).2 (by nlinarith)
  exact sub_neg.mpr hh

theorem exceptional_metric_local_ode (Psi Q : ℝ → ℝ) (x H a v B p : ℝ)
    (hPsi : HasDerivAt Psi (-H * Psi x - a * Q x) x)
    (hQ : HasDerivAt Q (-2 * H * Q x + 2 * v * (2 * v / B - 1) * p * Psi x) x) :
    HasDerivAt (fun y => -H * Psi y - a * Q y)
      (-3 * H * (-H * Psi x - a * Q x) -
        (2 * H ^ 2 + 2 * a * v * (2 * v / B - 1) * p) * Psi x) x := by
  convert! (hPsi.const_mul (-H)).sub (hQ.const_mul a) using 1
  ring

theorem positive_lapse_jet_identity (y yx yxx : ℝ) (hy : y ≠ 0) :
    (2 * yx / y) ^ 2 + 2 * (2 * yxx / y - 2 * yx ^ 2 / y ^ 2) =
      4 * yxx / y := by
  field_simp
  ring

theorem ground_state_energy_jet_identity (b y yx yxx f fx : ℝ) :
    4 * b * (yx * f + y * fx) ^ 2 + 4 * b * y * yxx * f ^ 2 =
      4 * b * y ^ 2 * fx ^ 2 +
        4 * b * ((yx ^ 2 + y * yxx) * f ^ 2 + 2 * y * yx * f * fx) := by ring

end PushSlip20260926

#print axioms PushSlip20260926.two_curvatures_obstruct
#print axioms PushSlip20260926.retained_auxiliary_positive
#print axioms PushSlip20260926.static_gap_identity
#print axioms PushSlip20260926.static_gap_positive
#print axioms PushSlip20260926.oscillator_coefficients_positive
#print axioms PushSlip20260926.positive_quadratic_every_wave
#print axioms PushSlip20260926.second_channel_residue
#print axioms PushSlip20260926.expanding_regular_residue_nonzero
#print axioms PushSlip20260926.physical_metric_tail_positive
#print axioms PushSlip20260926.exceptional_matter_schur_positive
#print axioms PushSlip20260926.positive_schur_spatial_pole
#print axioms PushSlip20260926.exceptional_matter_low_k_negative
#print axioms PushSlip20260926.exceptional_metric_local_ode
#print axioms PushSlip20260926.positive_lapse_jet_identity
#print axioms PushSlip20260926.ground_state_energy_jet_identity
