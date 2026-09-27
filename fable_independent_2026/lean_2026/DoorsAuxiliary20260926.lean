import Mathlib

/-!
Exact finite spectral/real inequalities underlying the lapse-weighted auxiliary
repair. Analytic identification of the continuum heat operator, its spectrum,
and a complete gravity action remains outside these declarations.
-/
namespace DoorsAuxiliary20260926

theorem weighted_transfer_bound (X Y r d H : ℝ)
    (hd : 0 ≤ d) (hY : Y ≤ r * X) (hH : 4 * (X - d * Y) ≤ H) :
    4 * (1 - d * r) * X ≤ H := by
  have hm := mul_le_mul_of_nonneg_left hY hd
  nlinarith

theorem original_filter_positive_bound (X Y r H : ℝ)
    (hX : 0 < X) (hr : r < 8) (hY : Y ≤ r * X)
    (hH : 4 * (X - Y / 8) ≤ H) : 0 < H := by
  have hb : 4 * (1 - (1 / 8 : ℝ) * r) * X ≤ H :=
    weighted_transfer_bound X Y r (1 / 8) H (by norm_num) hY (by linarith)
  have hp : 0 < 4 * (1 - (1 / 8 : ℝ) * r) := by linarith
  exact lt_of_lt_of_le (mul_pos hp hX) hb

theorem adapted_filter_uniform_bound (X Y H : ℝ)
    (hY : Y ≤ X) (hH : 4 * (X - Y / 8) ≤ H) :
    (7 / 2 : ℝ) * X ≤ H := by linarith

theorem finite_spectral_contraction {ι : Type*} (s : Finset ι)
    (weight gain amplitude : ι → ℝ)
    (hw : ∀ i ∈ s, 0 ≤ weight i)
    (hg : ∀ i ∈ s, 0 ≤ gain i ∧ gain i ≤ 1) :
    ∑ i ∈ s, weight i * (gain i * amplitude i)^2 ≤
      ∑ i ∈ s, weight i * amplitude i^2 := by
  apply Finset.sum_le_sum
  intro i hi
  have hgi := hg i hi
  have hg2 : (gain i)^2 ≤ 1 := by nlinarith
  have hm := mul_le_mul_of_nonneg_right hg2 (sq_nonneg (amplitude i))
  have hwg := mul_le_mul_of_nonneg_left hm (hw i hi)
  nlinarith

noncomputable def weightedEnergy (t : ℝ) : ℝ :=
  Real.exp (-2*t) + (1/25:ℝ)*Real.exp (-200*t) - (4/25:ℝ)*Real.exp (-101*t)

theorem weighted_energy_at_zero : weightedEnergy 0 = 22/25 := by
  norm_num [weightedEnergy]

theorem weighted_energy_initial_derivative :
    HasDerivAt weightedEnergy (154/25) 0 := by
  have he (a : ℝ) : HasDerivAt (fun t : ℝ => Real.exp (a*t)) a 0 := by
    convert! (Real.hasDerivAt_exp (a*0)).comp 0 ((hasDerivAt_id (0:ℝ)).const_mul a) using 1 <;> simp
  unfold weightedEnergy
  convert! ((he (-2)).add ((he (-200)).const_mul (1/25))).sub
    ((he (-101)).const_mul (4/25)) using 1 <;> norm_num

theorem positive_initial_derivative : (0:ℝ) < 154/25 := by norm_num

#print axioms weighted_transfer_bound
#print axioms original_filter_positive_bound
#print axioms adapted_filter_uniform_bound
#print axioms finite_spectral_contraction
#print axioms weighted_energy_at_zero
#print axioms weighted_energy_initial_derivative
#print axioms positive_initial_derivative

end DoorsAuxiliary20260926
