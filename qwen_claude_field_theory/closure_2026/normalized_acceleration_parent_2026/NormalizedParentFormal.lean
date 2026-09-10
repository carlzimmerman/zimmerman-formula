import Mathlib.Data.Real.Basic
import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic
import Mathlib.Tactic.Ring

open Matrix

noncomputable section

namespace NormalizedAccelerationParent

def G (y : ℝ) : ℝ := y ^ 2 + 2 * (1 + y) * Real.exp (-y) - 2

def H (y : ℝ) : ℝ := 2 * (1 + y) * Real.exp (-y) - 2

theorem parent_recombines_to_exponential_primitive (y : ℝ) :
    H y + y ^ 2 = G y := by
  unfold H G
  ring

/- If the lapse-neutral scalar stress is isotropic, its constitutive derivative
   must vanish.  The exact MOND flux has positive derivative data at every
   positive acceleration, so the two requirements cannot hold simultaneously.
   This is an abstract arithmetic core; the Python gate supplies the metric
   variation and identifies the hypotheses for the covariant parent. -/
theorem isotropic_flux_incompatibility
    (y mu : ℝ) (hy : 0 < y) (hmu : 0 < mu)
    (hisotropy : y * mu = 0) : False := by
  have hprod : 0 < y * mu := mul_pos hy hmu
  nlinarith

theorem algebraic_envelope_chain_rule_jet
    (Fy Fq qstarPrime : ℝ) :
    (Fy + Fq * qstarPrime) - Fy - Fq * qstarPrime = 0 := by
  ring

def localLapseBracket : Matrix (Fin 2) (Fin 2) ℤ :=
  !![0, -1;
     1,  0]

def homogeneousLapseBracket : Matrix (Fin 2) (Fin 2) ℤ :=
  !![0, 0;
     0, 0]

theorem local_lapse_bracket_det : Matrix.det localLapseBracket = 1 := by
  native_decide

theorem homogeneous_lapse_bracket_det : Matrix.det homogeneousLapseBracket = 0 := by
  native_decide

theorem normalized_parent_rank_jump_witness :
    Matrix.det homogeneousLapseBracket ≠ Matrix.det localLapseBracket := by
  rw [homogeneous_lapse_bracket_det, local_lapse_bracket_det]
  decide

end NormalizedAccelerationParent
