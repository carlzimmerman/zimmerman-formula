import Mathlib
import Mathlib.Tactic

/-
  AS057 -- Dimension dependence of static-channel rank (Lean 4 certificate).

  Derivation (run AS057-r1-20260928T080406Z-dsv4f-hermes, verified symbolically
  and by an independent Christoffel-route check at d = 1..5): for the static
  diagonal perturbation h = diag(-2 Phi, -2 Psi, ...) of (d+1)-dimensional
  Minkowski space, the two linearized Einstein channels are

      G_00 = (d-1) Delta Psi
      G_kk = (d-1) Delta(Phi-Psi) + (d-1)(3-d) Delta Psi      (the seed's claim)
           = (d-1) Delta Phi       - (d-1)(d-2) Delta Psi     (direct form)

  so the 2x2 coefficient matrix in the basis (Delta Psi, Delta(Phi-Psi)) has
  determinant (d-1)^2.  Rank 2 for every d >= 2; rank collapse exactly at
  d = 1 (2D Einstein tensor identically zero); the d = 3 special is the
  DECOUPLING ((d-1)(3-d) = 0, diagonal map) -- a diagonalization, not a rank
  change.  Decoupling and rank are separated.

  Formalized content (field arithmetic over Q; d stands for a positive real
  spatial dimension, delta = d - 1):
    det2_main      : determinant of the coefficient matrix = (d-1)^2
    inv_iff        : invertible iff d != 1     (rank-2 statement, d >= 2 case)
    decouples_iff  : off-diagonal coefficient = 0 iff d = 1 or d = 3
    coeff_identity : the claim-form Delta Psi coefficient (after expanding
                     Delta(Phi-Psi)) equals the direct-form coefficient
    rank_stable    : d >= 2 -> d - 1 != 0      (dimension-stability of rank 2)
    det_integers   : det N = 1, 4, 9 at d = 2, 3, 4; det N(1) = 0
-/

noncomputable section

namespace AS057

open scoped Matrix
open BigOperators

-- determinant of the 2x2 channel-coefficient matrix, laid out explicitly
-- (position (0,0)=d-1, (0,1)=0, (1,0)=(d-1)(3-d), (1,1)=d-1)
theorem det2 (d : ℚ) :
    (d - 1) * (d - 1) - 0 * ((d - 1) * (3 - d)) = (d - 1) ^ 2 := by
  ring

-- rank collapse happens iff d = 1 (the square vanishes iff its base does)
theorem det_sq_zero_iff (d : ℚ) : (d - 1) ^ 2 = 0 ↔ d = 1 := by
  constructor
  · intro h
    exact sub_eq_zero.mp (sq_eq_zero_iff.mp h)
  · intro h
    subst d
    norm_num

-- invertibility of the channel map iff d != 1
theorem inv_iff (d : ℚ) : (d - 1) ^ 2 ≠ 0 ↔ d ≠ 1 := by
  constructor
  · intro h z
    apply h
    rw [z]
    norm_num
  · intro h z
    apply h
    exact sub_eq_zero.mp (sq_eq_zero_iff.mp z)

-- rank 2 for every d >= 2 (dimension-stability of the static channel count)
theorem rank_stable (d : ℚ) (hd : 2 ≤ d) : d - 1 ≠ 0 := by
  intro h
  linarith

-- the d=3 special is a DECOUPLING, not a rank change:
-- the off-diagonal coefficient vanishes exactly at d = 1 and d = 3
theorem decouples_iff (d : ℚ) : (d - 1) * (3 - d) = 0 ↔ d = 1 ∨ d = 3 := by
  constructor
  · intro h
    rcases mul_eq_zero.mp h with h1 | h2
    · left
      linarith
    · right
      linarith
  · rintro (rfl | rfl) <;> norm_num

-- coefficient identity: the claim form's Delta Psi coefficient equals the
-- direct form's (expansion of Delta(Phi-Psi) included)
--   (d-1)(3-d) - (d-1) = -(d-1)(d-2)
theorem coeff_identity (d : ℚ) :
    (d - 1) * (3 - d) - (d - 1) = -((d - 1) * (d - 2)) := by
  ring

-- determinant values at the integer test points, and the d=1 exception
theorem det_integers :
    (1 - 1) ^ 2 = 0 ∧ (2 - 1) ^ 2 = 1 ∧ (3 - 1) ^ 2 = 4 ∧ (4 - 1) ^ 2 = 9 := by
  norm_num

-- d=3 diagonal map (decoupling): both off-diagonal = 0, determinant 4
theorem d3_diagonal :
    (3 - 1) * (3 - 3) = 0 ∧ (3 - 1) * (3 - 1) = 4 := by
  norm_num

end AS057

/- Axiom audit (unfiltered): every certified theorem, zero sorry.
   Allowed axioms: {propext, Classical.choice, Quot.sound}. -/
#print axioms AS057.det2
#print axioms AS057.det_sq_zero_iff
#print axioms AS057.inv_iff
#print axioms AS057.rank_stable
#print axioms AS057.decouples_iff
#print axioms AS057.coeff_identity
#print axioms AS057.det_integers
#print axioms AS057.d3_diagonal