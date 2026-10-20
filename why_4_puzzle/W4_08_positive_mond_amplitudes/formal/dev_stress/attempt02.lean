import Mathlib.Data.Real.Sqrt
import Mathlib.Algebra.Order.BigOperators.Group.Finset
import Mathlib.Tactic.LinearCombination
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Ring

/-!
Exact stress obstruction for the positive paired spectrum in PROOF.md, section B.
The physical-cutoff expressions for energy and directional null stress are explicit
inputs. No implication from dynamical health to the null energy condition is used.
These results do not derive the why-4 target or a complete microscopic theory.
-/

namespace Why4.PairedBandStress

noncomputable def radius (d : ℝ) : ℝ := Real.sqrt (1 + d ^ 2)

noncomputable def shape (d : ℝ) : ℝ := radius d ^ 3 - 1 - d ^ 3

noncomputable def energy (A L d : ℝ) : ℝ := A * L ^ 3 * shape d

noncomputable def nullStress (A L d : ℝ) : ℝ :=
  (3 / 2 : ℝ) * A * L ^ 3 * (radius d - 1)

noncomputable def pressure (A L d : ℝ) : ℝ :=
  nullStress A L d - energy A L d

theorem radius_sq (d : ℝ) : radius d ^ 2 = 1 + d ^ 2 := by
  exact Real.sq_sqrt (by positivity)

theorem radius_gt_one {d : ℝ} (hd : 0 < d) : 1 < radius d := by
  have hr := radius_sq d
  have hn : 0 ≤ radius d := Real.sqrt_nonneg _
  nlinarith [sq_pos_of_pos hd]

theorem radius_gt_gap {d : ℝ} (hd : 0 < d) : d < radius d := by
  have hr := radius_sq d
  have hn : 0 ≤ radius d := Real.sqrt_nonneg _
  nlinarith

theorem shape_factorization (d : ℝ) :
    shape d * (radius d + d) = (radius d - 1) * (2 * radius d + d + 1) := by
  have hr := radius_sq d
  dsimp [shape]
  linear_combination (radius d ^ 2 + d ^ 2 + d * radius d - 1) * hr

theorem shape_strict_bounds {d : ℝ} (hd : 0 < d) :
    (3 / 2 : ℝ) * (radius d - 1) < shape d ∧
      shape d < 3 * (radius d - 1) := by
  have h1 := radius_gt_one hd
  have hdlt := radius_gt_gap hd
  have hs : 0 < radius d + d := by linarith
  have hf := shape_factorization d
  have hloeq :
      (2 * shape d - 3 * (radius d - 1)) * (radius d + d) =
        (radius d - 1) * (radius d - d + 2) := by
    calc
      _ = 2 * (shape d * (radius d + d)) -
          3 * (radius d - 1) * (radius d + d) := by ring
      _ = _ := by rw [hf]; ring
  have hhieq :
      (3 * (radius d - 1) - shape d) * (radius d + d) =
        (radius d - 1) * (radius d + 2 * d - 1) := by
    calc
      _ = 3 * (radius d - 1) * (radius d + d) -
          shape d * (radius d + d) := by ring
      _ = _ := by rw [hf]; ring
  have hlo : 0 < 2 * shape d - 3 * (radius d - 1) := by
    apply (mul_pos_iff_of_pos_right hs).mp
    rw [hloeq]
    exact mul_pos (by linarith) (by linarith)
  have hhi : 0 < 3 * (radius d - 1) - shape d := by
    apply (mul_pos_iff_of_pos_right hs).mp
    rw [hhieq]
    exact mul_pos (by linarith) (by linarith)
  constructor <;> linarith

theorem energy_pos {A L d : ℝ} (hA : 0 < A) (hL : 0 < L) (hd : 0 < d) :
    0 < energy A L d := by
  have hb := (shape_strict_bounds hd).1
  have h1 := radius_gt_one hd
  have hf : 0 < shape d := by linarith
  exact mul_pos (mul_pos hA (pow_pos hL 3)) hf

theorem band_strict_bounds {A L d : ℝ}
    (hA : 0 < A) (hL : 0 < L) (hd : 0 < d) :
    energy A L d / 2 < nullStress A L d ∧
      nullStress A L d < energy A L d := by
  have hb := shape_strict_bounds hd
  have hw : 0 < A * L ^ 3 := mul_pos hA (pow_pos hL 3)
  have hlo := mul_lt_mul_of_pos_left hb.1 hw
  have hhi := mul_lt_mul_of_pos_left hb.2 hw
  have hnull : (A * L ^ 3) * ((3 / 2 : ℝ) * (radius d - 1)) =
      nullStress A L d := by dsimp [nullStress]; ring
  have htwice : (A * L ^ 3) * (3 * (radius d - 1)) =
      2 * nullStress A L d := by dsimp [nullStress]; ring
  rw [hnull] at hlo
  change nullStress A L d < energy A L d at hlo
  change energy A L d < (A * L ^ 3) * (3 * (radius d - 1)) at hhi
  rw [htwice] at hhi
  exact ⟨by linarith only [hhi], hlo⟩

theorem pressure_strict_bounds {A L d : ℝ}
    (hA : 0 < A) (hL : 0 < L) (hd : 0 < d) :
    -(energy A L d) / 2 < pressure A L d ∧ pressure A L d < 0 := by
  have hb := band_strict_bounds hA hL hd
  dsimp [pressure]
  constructor <;> linarith

theorem energy_add_pressure (A L d : ℝ) :
    energy A L d + pressure A L d = nullStress A L d := by
  dsimp [pressure]
  ring

section FiniteFamily

variable {ι : Type*} (s : Finset ι) (A L d : ι → ℝ)

theorem finite_band_strict_bounds (hs : s.Nonempty)
    (hA : ∀ i ∈ s, 0 < A i) (hL : ∀ i ∈ s, 0 < L i)
    (hd : ∀ i ∈ s, 0 < d i) :
    (∑ i ∈ s, energy (A i) (L i) (d i)) / 2 <
        ∑ i ∈ s, nullStress (A i) (L i) (d i) ∧
      (∑ i ∈ s, nullStress (A i) (L i) (d i)) <
        ∑ i ∈ s, energy (A i) (L i) (d i) := by
  constructor
  · have h := Finset.sum_lt_sum_of_nonempty hs (fun i hi =>
      (band_strict_bounds (hA i hi) (hL i hi) (hd i hi)).1)
    simpa only [Finset.sum_div] using h
  · exact Finset.sum_lt_sum_of_nonempty hs (fun i hi =>
      (band_strict_bounds (hA i hi) (hL i hi) (hd i hi)).2)

theorem finite_energy_pos (hs : s.Nonempty)
    (hA : ∀ i ∈ s, 0 < A i) (hL : ∀ i ∈ s, 0 < L i)
    (hd : ∀ i ∈ s, 0 < d i) :
    0 < ∑ i ∈ s, energy (A i) (L i) (d i) := by
  exact Finset.sum_pos (fun i hi => energy_pos (hA i hi) (hL i hi) (hd i hi)) hs

/- The offset contributes +offset to energy and -offset to pressure. -/
theorem finite_nec_obstruction (hs : s.Nonempty)
    (hA : ∀ i ∈ s, 0 < A i) (hL : ∀ i ∈ s, 0 < L i)
    (hd : ∀ i ∈ s, 0 < d i) (offset extraEnergy extraPressure : ℝ)
    (hnec : 0 ≤ extraEnergy + extraPressure) :
    0 < (offset + (∑ i ∈ s, energy (A i) (L i) (d i)) + extraEnergy) +
      (-offset + (∑ i ∈ s, pressure (A i) (L i) (d i)) + extraPressure) := by
  have hb := (finite_band_strict_bounds s A L d hs hA hL hd).1
  have he := finite_energy_pos s A L d hs hA hL hd
  simp only [pressure, Finset.sum_sub_distrib]
  linarith

theorem finite_no_vacuum (hs : s.Nonempty)
    (hA : ∀ i ∈ s, 0 < A i) (hL : ∀ i ∈ s, 0 < L i)
    (hd : ∀ i ∈ s, 0 < d i) (offset extraEnergy extraPressure : ℝ)
    (hnec : 0 ≤ extraEnergy + extraPressure) :
    (offset + (∑ i ∈ s, energy (A i) (L i) (d i)) + extraEnergy) +
      (-offset + (∑ i ∈ s, pressure (A i) (L i) (d i)) + extraPressure) ≠ 0 := by
  exact ne_of_gt
    (finite_nec_obstruction s A L d hs hA hL hd offset extraEnergy extraPressure hnec)

theorem required_negative_extra_null_stress (hs : s.Nonempty)
    (hA : ∀ i ∈ s, 0 < A i) (hL : ∀ i ∈ s, 0 < L i)
    (hd : ∀ i ∈ s, 0 < d i) (offset extraEnergy extraPressure : ℝ)
    (hvac : (offset + (∑ i ∈ s, energy (A i) (L i) (d i)) + extraEnergy) +
      (-offset + (∑ i ∈ s, pressure (A i) (L i) (d i)) + extraPressure) = 0) :
    (∑ i ∈ s, energy (A i) (L i) (d i)) / 2 < -(extraEnergy + extraPressure) ∧
      extraEnergy + extraPressure < 0 := by
  have hb := (finite_band_strict_bounds s A L d hs hA hL hd).1
  have he := finite_energy_pos s A L d hs hA hL hd
  simp only [pressure, Finset.sum_sub_distrib] at hvac
  constructor <;> linarith

end FiniteFamily

#check @band_strict_bounds
#check @pressure_strict_bounds
#check @finite_band_strict_bounds
#check @finite_nec_obstruction
#check @finite_no_vacuum
#check @required_negative_extra_null_stress
#print axioms band_strict_bounds
#print axioms pressure_strict_bounds
#print axioms finite_band_strict_bounds
#print axioms finite_nec_obstruction
#print axioms finite_no_vacuum
#print axioms required_negative_extra_null_stress

end Why4.PairedBandStress
