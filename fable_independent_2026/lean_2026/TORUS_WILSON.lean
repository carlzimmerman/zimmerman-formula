import Mathlib

/-!
# TORUS_WILSON -- discrete Z3 Wilson lines on the flux-3 torus (criteria TORUS_WILSON_CRITERIA.md, 8ea12cecf): KILL

Numeric (TORUS_WILSON.py / .out): single-valuedness gate 3e-14; across all 1134 configurations (81 Wilson-line
pairs × τ ∈ {i, e^{2πi/3}} × 7 Higgs choices) only TWO spectra occur per τ, (ε, 1, 1) and (δ, δ, 1): every one
has a degenerate pair, so the Koide band is unreachable.

CERTIFIED (the mechanism): a Z3 Wilson line on an M = 3 torus is a magnetic translation, acting on the three
generations by the clock and shift matrices, which are unitary (`shift_unitary`, `clock_unitary` for |ω| = 1).
A mass matrix changed by unitaries on both sides, m ↦ U m V, has m'†m' = V†(m†m)V (`two_sided`) and the same
characteristic polynomial (`same_charpoly`), hence the same masses.  Discrete Wilson lines therefore cannot
lift the degeneracy proved in TORUS_YUKAWA; only continuous Wilson lines (free moduli, a fit) can.
-/

namespace TorusWilson

def P : Matrix (Fin 3) (Fin 3) ℂ := !![0, 1, 0; 0, 0, 1; 1, 0, 0]
def C (ω : ℂ) : Matrix (Fin 3) (Fin 3) ℂ := !![1, 0, 0; 0, ω, 0; 0, 0, ω ^ 2]

theorem shift_unitary : P.conjTranspose * P = 1 := by
  ext i j; fin_cases i <;> fin_cases j <;> simp [P, Matrix.mul_apply, Fin.sum_univ_three]

theorem clock_unitary (ω : ℂ) (h : star ω * ω = 1) : (C ω).conjTranspose * C ω = 1 := by
  have h' : (starRingEnd ℂ) ω * ω = 1 := h
  ext i j; fin_cases i <;> fin_cases j <;> simp [C, Matrix.mul_apply, Fin.sum_univ_three]
  all_goals first
    | exact h'
    | (rw [show (starRingEnd ℂ) ω ^ 2 * ω ^ 2 = ((starRingEnd ℂ) ω * ω) ^ 2 by ring, h']; norm_num)

theorem two_sided (m U V : Matrix (Fin 3) (Fin 3) ℂ) (hU : U.conjTranspose * U = 1) :
    (U * m * V).conjTranspose * (U * m * V) = V.conjTranspose * (m.conjTranspose * m) * V := by
  simp only [Matrix.conjTranspose_mul]
  calc V.conjTranspose * (m.conjTranspose * U.conjTranspose) * (U * m * V)
      = V.conjTranspose * m.conjTranspose * (U.conjTranspose * U) * m * V := by
        simp only [Matrix.mul_assoc]
    _ = V.conjTranspose * (m.conjTranspose * m) * V := by rw [hU]; simp [Matrix.mul_assoc]

theorem same_charpoly (A : Matrix (Fin 3) (Fin 3) ℂ) (V : (Matrix (Fin 3) (Fin 3) ℂ)ˣ) :
    (V⁻¹.val * A * V.val).charpoly = A.charpoly := by
  simp

end TorusWilson

#print axioms TorusWilson.shift_unitary
#print axioms TorusWilson.clock_unitary
#print axioms TorusWilson.two_sided
#print axioms TorusWilson.same_charpoly
