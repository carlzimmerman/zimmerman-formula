import Mathlib.Data.Real.Basic
import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic
import Mathlib.Topology.Algebra.Ring.Real
import Mathlib.Topology.Order.IntermediateValue
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring

open Matrix

noncomputable section

def bracketWitness : Matrix (Fin 4) (Fin 4) ℤ :=
  !![0, 0, 1, 0;
     0, 0, 0, 1;
    -1, 0, 0, 0;
     0,-1, 0, 0]

def bracketZero : Matrix (Fin 4) (Fin 4) ℤ :=
  !![0, 0, 0, 0;
     0, 0, 0, 0;
     0, 0, 0, 0;
     0, 0, 0, 0]

theorem bracket_witness_det : Matrix.det bracketWitness = 1 := by
  native_decide

theorem bracket_witness_nonzero : Matrix.det bracketWitness ≠ 0 := by
  rw [bracket_witness_det]
  decide

theorem bracket_zero_det : Matrix.det bracketZero = 0 := by
  native_decide

theorem rank_jump_witness : Matrix.det bracketZero ≠ Matrix.det bracketWitness := by
  rw [bracket_zero_det, bracket_witness_det]
  decide

/-!
  Exact algebraic witnesses for the evolving homogeneous DBI clock branch.
  The executable gate supplies the variational derivation and the numerical
  branch construction; these lemmas kernel-check the finite identities used
  there without treating them as a proof of the full covariant theory.
-/

def dbiRho (A z s : ℝ) : ℝ := A * (1 + z ^ 2) / s

def dbiPressure (A s : ℝ) : ℝ := -A * s

def dbiSoundSpeedSquared (z : ℝ) : ℝ := (1 - z ^ 2) / (3 - z ^ 2)

theorem dbi_rho_plus_pressure
    (A z s : ℝ) (hs : s ≠ 0) (hsq : s ^ 2 = 1 - z ^ 2) :
    dbiRho A z s + dbiPressure A s = 2 * A * z ^ 2 / s := by
  unfold dbiRho dbiPressure
  field_simp [hs]
  rw [hsq]
  ring

theorem dbi_sound_speed_positive_subluminal
    (z : ℝ) (hz0 : 0 < z) (hz1 : z < 1) :
    0 < dbiSoundSpeedSquared z ∧ dbiSoundSpeedSquared z < 1 := by
  unfold dbiSoundSpeedSquared
  have hleft : 0 < 1 - z := sub_pos.mpr hz1
  have hright : 0 < 1 + z := by nlinarith
  have hprod : 0 < (1 - z) * (1 + z) := mul_pos hleft hright
  have hnum : 0 < 1 - z ^ 2 := by nlinarith [hprod]
  have hden : 0 < 3 - z ^ 2 := by nlinarith [hnum]
  constructor
  · exact div_pos hnum hden
  · apply (div_lt_one hden).2
    nlinarith [hnum]

theorem expanding_shift_symmetric_forces_zero_gradient
    (H KX : ℝ) (hH : H ≠ 0) (hEq : 3 * H * KX = 0) : KX = 0 := by
  have hprod : H * KX = 0 := by nlinarith [hEq]
  exact (mul_eq_zero.mp hprod).resolve_left hH

def affineLapseResidual (k e : ℝ) : ℝ := -k ^ 2 * (1 + (k - 1) * e)

theorem affine_lapse_residual_unit_slope (e : ℝ) :
    affineLapseResidual 1 e = -1 := by
  unfold affineLapseResidual
  ring

theorem affine_lapse_residual_unit_slope_nonzero (e : ℝ) :
    affineLapseResidual 1 e ≠ 0 := by
  rw [affine_lapse_residual_unit_slope]
  norm_num

/-!
  The numerical evolving-clock scan can be upgraded to an all-a>0 theorem.
  The current map is strictly increasing on (0,1), and its cubic numerator
  changes sign across the interval; no root count is inserted as a constant.
-/

def chargeShape (z : ℝ) : ℝ := z ^ 3 / (1 - z ^ 2)

def chargePoly (q z : ℝ) : ℝ := z ^ 3 + q * z ^ 2 - q

theorem charge_shape_strictMono_on :
    StrictMonoOn chargeShape (Set.Ioo (0 : ℝ) 1) := by
  intro x hx y hy hxy
  have hx0 : 0 < x := hx.1
  have hx1 : x < 1 := hx.2
  have hy0 : 0 < y := hy.1
  have hy1 : y < 1 := hy.2
  have hdx : 0 < 1 - x ^ 2 := by
    nlinarith [mul_pos (sub_pos.mpr hx1) (by nlinarith : 0 < 1 + x)]
  have hdy : 0 < 1 - y ^ 2 := by
    nlinarith [mul_pos (sub_pos.mpr hy1) (by nlinarith : 0 < 1 + y)]
  have hfac : 0 < x ^ 2 + x * y + y ^ 2 - x ^ 2 * y ^ 2 := by
    have hxx : 0 < x ^ 2 * (1 - y ^ 2) := mul_pos (sq_pos_of_pos hx0) hdy
    have hxypos : 0 < x * y := mul_pos hx0 hy0
    have hyy : 0 < y ^ 2 := sq_pos_of_pos hy0
    nlinarith
  have hid : y ^ 3 * (1 - x ^ 2) - x ^ 3 * (1 - y ^ 2) =
      (y - x) * (x ^ 2 + x * y + y ^ 2 - x ^ 2 * y ^ 2) := by ring
  have hprod : 0 < (y - x) * (x ^ 2 + x * y + y ^ 2 - x ^ 2 * y ^ 2) :=
    mul_pos (sub_pos.mpr hxy) hfac
  unfold chargeShape
  apply (div_lt_div_iff₀ hdx hdy).2
  nlinarith [hprod]

theorem charge_shape_exists (q : ℝ) (hq : 0 < q) :
    ∃ z, z ∈ Set.Ioo (0 : ℝ) 1 ∧ chargeShape z = q := by
  have hcont : ContinuousOn (chargePoly q) (Set.Icc (0 : ℝ) 1) := by
    unfold chargePoly
    fun_prop
  have hsubset : Set.Icc (chargePoly q 0) (chargePoly q 1) ⊆
      chargePoly q '' Set.Icc (0 : ℝ) 1 :=
    intermediate_value_Icc (show (0 : ℝ) ≤ 1 by norm_num) hcont
  have hzero : (0 : ℝ) ∈ Set.Icc (chargePoly q 0) (chargePoly q 1) := by
    constructor <;> dsimp [chargePoly] <;> nlinarith
  obtain ⟨z, hz, hp⟩ := hsubset hzero
  have hz0 : 0 < z := by
    have hzle : 0 ≤ z := hz.1
    by_contra hn
    have hzeq : z = 0 := le_antisymm (le_of_not_gt hn) hzle
    subst z
    dsimp [chargePoly] at hp
    nlinarith
  have hz1 : z < 1 := by
    have hzl : z ≤ 1 := hz.2
    by_contra hn
    have hzeq : z = 1 := le_antisymm hzl (le_of_not_gt hn)
    subst z
    dsimp [chargePoly] at hp
    nlinarith
  have hden : 1 - z ^ 2 ≠ 0 := by
    have hdenpos : 0 < 1 - z ^ 2 := by
      nlinarith [mul_pos (sub_pos.mpr hz1) (by nlinarith : 0 < 1 + z)]
    exact ne_of_gt hdenpos
  refine ⟨z, ⟨hz0, hz1⟩, ?_⟩
  unfold chargeShape
  field_simp [hden]
  dsimp [chargePoly] at hp
  nlinarith [hp]

theorem charge_shape_unique_positive_root (q : ℝ) (hq : 0 < q) :
    ∃! z, z ∈ Set.Ioo (0 : ℝ) 1 ∧ chargeShape z = q := by
  obtain ⟨z, hz, hqz⟩ := charge_shape_exists q hq
  refine ⟨z, ⟨hz, hqz⟩, ?_⟩
  intro y hy
  exact charge_shape_strictMono_on.injOn hy.1 hz (by simp [hy.2, hqz])

theorem dbi_clock_unique_speed
    (A L C a : ℝ) (hA : 0 < A) (hL : 0 < L) (hC : 0 < C) (ha : 0 < a) :
    ∃! z, z ∈ Set.Ioo (0 : ℝ) 1 ∧
      chargeShape z = L * (C / (A * a ^ 3)) ^ 2 := by
  have hAa : 0 < A * a ^ 3 := mul_pos hA (pow_pos ha 3)
  have hfrac : 0 < C / (A * a ^ 3) := div_pos hC hAa
  have hq : 0 < L * (C / (A * a ^ 3)) ^ 2 :=
    mul_pos hL (sq_pos_of_pos hfrac)
  exact charge_shape_unique_positive_root _ hq
