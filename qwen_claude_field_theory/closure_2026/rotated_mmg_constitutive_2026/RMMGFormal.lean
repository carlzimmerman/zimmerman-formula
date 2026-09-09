import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic

open Matrix

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
