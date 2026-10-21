module

public import Mathlib.Algebra.Order.Field.Basic
public import Mathlib.Algebra.Order.BigOperators.Group.Finset
public import Mathlib.Algebra.BigOperators.Ring.Finset
meta import Mathlib.Tactic.Linarith.Frontend
meta import Mathlib.Tactic.Ring.Basic

public section

/-!
Exact stress obstruction for PROOF.md, section B, over an ordered field.
The radius r is represented by its defining nonnegative-root conditions
r >= 0 and r^2 = 1 + d^2. Their uniqueness is proved below; no new physics
assumption is hidden in this representation. The physical-cutoff energy and
directional null-stress expressions are explicit inputs. No implication from
dynamical health to the null energy condition is used. These results do not
derive the why-4 target or a complete microscopic theory.
-/

namespace Why4.PairedBandStress

variable {K : Type*} [Field K] [LinearOrder K] [IsStrictOrderedRing K]

def shape (d r : K) : K := r ^ 3 - 1 - d ^ 3

def energy (A L d r : K) : K := A * L ^ 3 * shape d r

def nullStress (A L _d r : K) : K := (3 / 2 : K) * A * L ^ 3 * (r - 1)

def pressure (A L d r : K) : K := nullStress A L d r - energy A L d r

theorem nonnegative_root_unique {d r t : K}
    (hr : 0 ≤ r) (ht : 0 ≤ t) (hrsq : r ^ 2 = 1 + d ^ 2)
    (htsq : t ^ 2 = 1 + d ^ 2) : r = t := by
  nlinarith

theorem root_gt_one {d r : K} (hd : 0 < d)
    (hr : 0 ≤ r) (hrsq : r ^ 2 = 1 + d ^ 2) : 1 < r := by
  nlinarith [sq_pos_of_pos hd]

theorem root_gt_gap {d r : K} (hd : 0 < d)
    (hr : 0 ≤ r) (hrsq : r ^ 2 = 1 + d ^ 2) : d < r := by
  nlinarith

theorem shape_factorization {d r : K} (hrsq : r ^ 2 = 1 + d ^ 2) :
    shape d r * (r + d) = (r - 1) * (2 * r + d + 1) := by
  have hfactor :
      shape d r * (r + d) - (r - 1) * (2 * r + d + 1) =
        (r ^ 2 - 1 - d ^ 2) * (r ^ 2 + d ^ 2 + d * r - 1) := by
    dsimp [shape]
    ring1
  rw [hrsq] at hfactor
  have hzero : (1 + d ^ 2 : K) - 1 - d ^ 2 = 0 := by ring1
  rw [hzero, zero_mul] at hfactor
  exact sub_eq_zero.mp hfactor

theorem shape_strict_bounds {d r : K} (hd : 0 < d)
    (hr : 0 ≤ r) (hrsq : r ^ 2 = 1 + d ^ 2) :
    (3 / 2 : K) * (r - 1) < shape d r ∧ shape d r < 3 * (r - 1) := by
  have h1 := root_gt_one hd hr hrsq
  have hdlt := root_gt_gap hd hr hrsq
  have hs : 0 < r + d := by linarith
  have hf := shape_factorization hrsq
  have hloeq : (2 * shape d r - 3 * (r - 1)) * (r + d) =
      (r - 1) * (r - d + 2) := by
    calc
      _ = 2 * (shape d r * (r + d)) - 3 * (r - 1) * (r + d) := by ring1
      _ = _ := by rw [hf]; ring1
  have hhieq : (3 * (r - 1) - shape d r) * (r + d) =
      (r - 1) * (r + 2 * d - 1) := by
    calc
      _ = 3 * (r - 1) * (r + d) - shape d r * (r + d) := by ring1
      _ = _ := by rw [hf]; ring1
  have hlo : 0 < 2 * shape d r - 3 * (r - 1) := by
    apply (mul_pos_iff_of_pos_right hs).mp
    rw [hloeq]
    exact mul_pos (by linarith) (by linarith)
  have hhi : 0 < 3 * (r - 1) - shape d r := by
    apply (mul_pos_iff_of_pos_right hs).mp
    rw [hhieq]
    exact mul_pos (by linarith) (by linarith)
  constructor <;> linarith

theorem energy_pos {A L d r : K} (hA : 0 < A) (hL : 0 < L) (hd : 0 < d)
    (hr : 0 ≤ r) (hrsq : r ^ 2 = 1 + d ^ 2) : 0 < energy A L d r := by
  have hb := (shape_strict_bounds hd hr hrsq).1
  have h1 := root_gt_one hd hr hrsq
  have hf : 0 < shape d r := by linarith
  exact mul_pos (mul_pos hA (pow_pos hL 3)) hf

theorem band_strict_bounds {A L d r : K}
    (hA : 0 < A) (hL : 0 < L) (hd : 0 < d)
    (hr : 0 ≤ r) (hrsq : r ^ 2 = 1 + d ^ 2) :
    energy A L d r / 2 < nullStress A L d r ∧
      nullStress A L d r < energy A L d r := by
  have hb := shape_strict_bounds hd hr hrsq
  have hw : 0 < A * L ^ 3 := mul_pos hA (pow_pos hL 3)
  have hlo := mul_lt_mul_of_pos_left hb.1 hw
  have hhi := mul_lt_mul_of_pos_left hb.2 hw
  have hnull : (A * L ^ 3) * ((3 / 2 : K) * (r - 1)) =
      nullStress A L d r := by dsimp [nullStress]; ring1
  have htwice : (A * L ^ 3) * (3 * (r - 1)) =
      2 * nullStress A L d r := by dsimp [nullStress]; ring1
  rw [hnull] at hlo
  change nullStress A L d r < energy A L d r at hlo
  change energy A L d r < (A * L ^ 3) * (3 * (r - 1)) at hhi
  rw [htwice] at hhi
  exact ⟨by linarith only [hhi], hlo⟩

theorem pressure_strict_bounds {A L d r : K}
    (hA : 0 < A) (hL : 0 < L) (hd : 0 < d)
    (hr : 0 ≤ r) (hrsq : r ^ 2 = 1 + d ^ 2) :
    -(energy A L d r) / 2 < pressure A L d r ∧ pressure A L d r < 0 := by
  have hb := band_strict_bounds hA hL hd hr hrsq
  dsimp [pressure]
  constructor <;> linarith

theorem energy_add_pressure (A L d r : K) :
    energy A L d r + pressure A L d r = nullStress A L d r := by
  dsimp [pressure]
  ring1

section FiniteFamily

variable {ι : Type*} (s : Finset ι) (A L d r : ι → K)

theorem finite_band_strict_bounds (hs : s.Nonempty)
    (hA : ∀ i ∈ s, 0 < A i) (hL : ∀ i ∈ s, 0 < L i)
    (hd : ∀ i ∈ s, 0 < d i) (hr : ∀ i ∈ s, 0 ≤ r i)
    (hrsq : ∀ i ∈ s, r i ^ 2 = 1 + d i ^ 2) :
    (∑ i ∈ s, energy (A i) (L i) (d i) (r i)) / 2 <
        ∑ i ∈ s, nullStress (A i) (L i) (d i) (r i) ∧
      (∑ i ∈ s, nullStress (A i) (L i) (d i) (r i)) <
        ∑ i ∈ s, energy (A i) (L i) (d i) (r i) := by
  constructor
  · have h := Finset.sum_lt_sum_of_nonempty hs (fun i hi =>
      (band_strict_bounds (hA i hi) (hL i hi) (hd i hi) (hr i hi) (hrsq i hi)).1)
    simpa only [div_eq_mul_inv, Finset.sum_mul] using h
  · exact Finset.sum_lt_sum_of_nonempty hs (fun i hi =>
      (band_strict_bounds (hA i hi) (hL i hi) (hd i hi) (hr i hi) (hrsq i hi)).2)

theorem finite_energy_pos (hs : s.Nonempty)
    (hA : ∀ i ∈ s, 0 < A i) (hL : ∀ i ∈ s, 0 < L i)
    (hd : ∀ i ∈ s, 0 < d i) (hr : ∀ i ∈ s, 0 ≤ r i)
    (hrsq : ∀ i ∈ s, r i ^ 2 = 1 + d i ^ 2) :
    0 < ∑ i ∈ s, energy (A i) (L i) (d i) (r i) := by
  exact Finset.sum_pos (fun i hi =>
    energy_pos (hA i hi) (hL i hi) (hd i hi) (hr i hi) (hrsq i hi)) hs

/- The offset contributes +offset to energy and -offset to pressure. -/
theorem finite_nec_obstruction (hs : s.Nonempty)
    (hA : ∀ i ∈ s, 0 < A i) (hL : ∀ i ∈ s, 0 < L i)
    (hd : ∀ i ∈ s, 0 < d i) (hr : ∀ i ∈ s, 0 ≤ r i)
    (hrsq : ∀ i ∈ s, r i ^ 2 = 1 + d i ^ 2)
    (offset extraEnergy extraPressure : K) (hnec : 0 ≤ extraEnergy + extraPressure) :
    0 < (offset + (∑ i ∈ s, energy (A i) (L i) (d i) (r i)) + extraEnergy) +
      (-offset + (∑ i ∈ s, pressure (A i) (L i) (d i) (r i)) + extraPressure) := by
  have hb := (finite_band_strict_bounds s A L d r hs hA hL hd hr hrsq).1
  have he := finite_energy_pos s A L d r hs hA hL hd hr hrsq
  simp only [pressure, Finset.sum_sub_distrib]
  linarith

theorem finite_no_vacuum (hs : s.Nonempty)
    (hA : ∀ i ∈ s, 0 < A i) (hL : ∀ i ∈ s, 0 < L i)
    (hd : ∀ i ∈ s, 0 < d i) (hr : ∀ i ∈ s, 0 ≤ r i)
    (hrsq : ∀ i ∈ s, r i ^ 2 = 1 + d i ^ 2)
    (offset extraEnergy extraPressure : K) (hnec : 0 ≤ extraEnergy + extraPressure) :
    (offset + (∑ i ∈ s, energy (A i) (L i) (d i) (r i)) + extraEnergy) +
      (-offset + (∑ i ∈ s, pressure (A i) (L i) (d i) (r i)) + extraPressure) ≠ 0 := by
  exact ne_of_gt (finite_nec_obstruction s A L d r hs hA hL hd hr hrsq
    offset extraEnergy extraPressure hnec)

theorem required_negative_extra_null_stress (hs : s.Nonempty)
    (hA : ∀ i ∈ s, 0 < A i) (hL : ∀ i ∈ s, 0 < L i)
    (hd : ∀ i ∈ s, 0 < d i) (hr : ∀ i ∈ s, 0 ≤ r i)
    (hrsq : ∀ i ∈ s, r i ^ 2 = 1 + d i ^ 2) (offset extraEnergy extraPressure : K)
    (hvac : (offset + (∑ i ∈ s, energy (A i) (L i) (d i) (r i)) + extraEnergy) +
      (-offset + (∑ i ∈ s, pressure (A i) (L i) (d i) (r i)) + extraPressure) = 0) :
    (∑ i ∈ s, energy (A i) (L i) (d i) (r i)) / 2 < -(extraEnergy + extraPressure) ∧
      extraEnergy + extraPressure < 0 := by
  have hb := (finite_band_strict_bounds s A L d r hs hA hL hd hr hrsq).1
  have he := finite_energy_pos s A L d r hs hA hL hd hr hrsq
  simp only [pressure, Finset.sum_sub_distrib] at hvac
  constructor <;> linarith

end FiniteFamily

#check @nonnegative_root_unique
#check @band_strict_bounds
#check @pressure_strict_bounds
#check @finite_band_strict_bounds
#check @finite_nec_obstruction
#check @finite_no_vacuum
#check @required_negative_extra_null_stress
#print axioms nonnegative_root_unique
#print axioms band_strict_bounds
#print axioms pressure_strict_bounds
#print axioms finite_band_strict_bounds
#print axioms finite_nec_obstruction
#print axioms finite_no_vacuum
#print axioms required_negative_extra_null_stress

end Why4.PairedBandStress
