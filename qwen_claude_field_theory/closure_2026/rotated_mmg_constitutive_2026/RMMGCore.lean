import Init.Omega

/-!
  Small kernel-checked companion for the rotated-MMG constitutive gate.

  The Python program computes the Poisson-bracket matrix.  This file records
  its determinant factor for the four scalar constraints, and kernel-checks
  the nonzero-mode and homogeneous-mode witnesses without importing Mathlib.
  It is intentionally a witness, not a formal proof of the full field theory.
-/

namespace RMMGConstitutive

def diracDet (d k : Int) : Int := d * d * k * k * k * k

theorem local_witness_det : diracDet 1 1 = 1 := by
  decide

theorem local_witness_nonzero : diracDet 1 1 ≠ 0 := by
  decide

theorem homogeneous_witness_det : diracDet 0 0 = 0 := by
  decide

theorem homogeneous_rank_witness_is_not_local :
    diracDet 0 0 ≠ diracDet 1 1 := by
  decide

def admDof (secondClassScalar : Nat) : Nat :=
  (20 - 2 * 6 - secondClassScalar) / 2

theorem local_adm_count : admDof 4 = 2 := by
  decide

theorem homogeneous_adm_count : admDof 0 = 4 := by
  decide

/- On an expanding FLRW branch, the shift-symmetric clock equation reduces
   (up to a nonzero factor) to H * K_X = 0.  This tiny theorem kernel-checks
   the algebraic implication used by the executable FLRW gate. -/
theorem flrw_expanding_forces_clock_gradient_zero
    (H KX : Int) (hH : H ≠ 0) (hEq : H * KX = 0) : KX = 0 := by
  exact (Int.mul_eq_zero.mp hEq).resolve_left hH

end RMMGConstitutive
