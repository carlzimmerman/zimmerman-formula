import Mathlib.Data.Real.Basic
import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith

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
