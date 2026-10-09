import Mathlib

/-!
# MAGNETIZED_TORUS_3 -- can a magnetized torus FORCE three generations, and what does it do to the masses?

Standard physics (cited, NOT certified here): a chiral fermion on T² with M units of magnetic flux has exactly
|M| zero modes (index theorem / Riemann-Roch, h⁰ of a degree-M line bundle on an elliptic curve), so
N_gen = 3 ⇔ M = 3.  The M zero modes carry the magnetic-translation (Heisenberg) group: a cyclic shift P and a
clock C with P C = ω C P, ω = e^{2πi/M}.  The question is whether anything FORCES M = 3.

CERTIFIED:
(A) `Z2_not_quantised`: Z² = 32π/3 is not a whole number of flux quanta 2πM (it would need M = 16/3).
    The framework's own constant does not fix the flux.
(B) `clock_shift`: for M = 3 (any ω with ω² + ω + 1 = 0), P³ = 1, C³ = 1 and P C = ω • (C P).
(C) `heisenberg_forces_degenerate`: a 3×3 matrix commuting with BOTH P and C is a multiple of the identity.
    Exact flux-3 flavour symmetry forces three EQUAL masses; it must be broken.
(D) `shift_only_is_circulant`: a matrix commuting with P alone is a + bP + cP², the circulant ring of
    KOIDE_HOLONOMY (eigenvalues a + 2t cos(φ + 2πk/3)).  So breaking the clock but keeping the shift gives
    exactly Koide's form, with the amplitude and the flux still free.
NOT CERTIFIED (cited math, from memory): zero-mode count = |M|; a degree-d line bundle on an elliptic curve is
very ample iff d ≥ 3, so M = 3 is the SMALLEST flux whose zero modes embed the torus (the plane cubic).  That
is a genuine mathematical selection rule for 3, but nothing in the framework requires the zero modes to embed
the torus; it is a premise, not a derivation.  Literature on magnetized branes reports Δ(27)-type flavour
groups for M = 3 (recalled, not re-checked).
-/

namespace MagTorus

theorem Z2_not_quantised : ¬ ∃ M : ℤ, (32 * Real.pi / 3 : ℝ) = 2 * Real.pi * M := by
  rintro ⟨M, h⟩
  have hpi : Real.pi ≠ 0 := Real.pi_ne_zero
  have h3 : (3 : ℝ) * M = 16 := by
    have := h; field_simp at this
    nlinarith [Real.pi_pos, this]
  have h3z : (3 : ℤ) * M = 16 := by exact_mod_cast h3
  omega

variable (ω : ℂ)

def P : Matrix (Fin 3) (Fin 3) ℂ := !![0, 1, 0; 0, 0, 1; 1, 0, 0]
def C : Matrix (Fin 3) (Fin 3) ℂ := !![1, 0, 0; 0, ω, 0; 0, 0, ω ^ 2]

lemma cube_one (hω : ω ^ 2 + ω + 1 = 0) : ω ^ 3 = 1 := by
  linear_combination (ω - 1) * hω

theorem clock_shift (hω : ω ^ 2 + ω + 1 = 0) :
    P * P * P = 1 ∧ C ω * C ω * C ω = 1 ∧ P * C ω = ω • (C ω * P) := by
  have h3 := cube_one ω hω
  refine ⟨?_, ?_, ?_⟩
  · ext i j; fin_cases i <;> fin_cases j <;> simp [P, Matrix.mul_apply, Fin.sum_univ_three]
  · ext i j; fin_cases i <;> fin_cases j <;>
      simp [C, Matrix.mul_apply, Fin.sum_univ_three] <;>
      first | linear_combination h3 | linear_combination (ω ^ 3 + 1) * h3
  · ext i j; fin_cases i <;> fin_cases j <;>
      simp [P, C, Matrix.mul_apply, Fin.sum_univ_three] <;> first | linear_combination (-1 : ℂ) * h3 | ring1

theorem heisenberg_forces_degenerate (hω : ω ^ 2 + ω + 1 = 0) (X : Matrix (Fin 3) (Fin 3) ℂ)
    (hP : X * P = P * X) (hC : X * C ω = C ω * X) : X = X 0 0 • (1 : Matrix (Fin 3) (Fin 3) ℂ) := by
  have h3 := cube_one ω hω
  have hω1 : ω ≠ 1 := by rintro rfl; norm_num at hω
  have hω0 : ω ≠ 0 := by rintro rfl; norm_num at hω
  have hω21 : ω ^ 2 ≠ 1 := by
    intro h
    have hm : ω = -2 := by linear_combination hω - h
    rw [hm] at h; norm_num at h
  have hωω2 : ω ≠ ω ^ 2 := by
    intro h; apply hω1
    have : ω * (ω - 1) = 0 := by linear_combination -h
    rcases mul_eq_zero.mp this with h0 | h1
    · exact absurd h0 hω0
    · linear_combination h1
  have e := fun i j => congrFun (congrFun hC i) j
  have f := fun i j => congrFun (congrFun hP i) j
  simp [C, P, Matrix.mul_apply, Fin.sum_univ_three] at e f
  have x01 : X 0 1 = 0 := by
    have := e 0 1; simp at this
    have : X 0 1 * (ω - 1) = 0 := by linear_combination this
    exact (mul_eq_zero.mp this).resolve_right (sub_ne_zero.mpr hω1)
  have x02 : X 0 2 = 0 := by
    have := e 0 2; simp at this
    have : X 0 2 * (ω ^ 2 - 1) = 0 := by linear_combination this
    exact (mul_eq_zero.mp this).resolve_right (sub_ne_zero.mpr hω21)
  have x10 : X 1 0 = 0 := by
    have := e 1 0; simp at this
    have : X 1 0 * (1 - ω) = 0 := by linear_combination this
    exact (mul_eq_zero.mp this).resolve_right (sub_ne_zero.mpr (Ne.symm hω1))
  have x12 : X 1 2 = 0 := by
    have := e 1 2; simp at this
    have : X 1 2 * (ω ^ 2 - ω) = 0 := by linear_combination this
    exact (mul_eq_zero.mp this).resolve_right (sub_ne_zero.mpr (Ne.symm hωω2))
  have x20 : X 2 0 = 0 := by
    have := e 2 0; simp at this
    have : X 2 0 * (1 - ω ^ 2) = 0 := by linear_combination this
    exact (mul_eq_zero.mp this).resolve_right (sub_ne_zero.mpr (Ne.symm hω21))
  have x21 : X 2 1 = 0 := by
    have := e 2 1; simp at this
    have : X 2 1 * (ω - ω ^ 2) = 0 := by linear_combination this
    exact (mul_eq_zero.mp this).resolve_right (sub_ne_zero.mpr hωω2)
  have d1 : X 1 1 = X 0 0 := by have := f 0 1; simp at this; linear_combination -this
  have d2 : X 2 2 = X 1 1 := by have := f 1 2; simp at this; linear_combination -this
  ext i j; fin_cases i <;> fin_cases j <;> simp [x01, x02, x10, x12, x20, x21, d1, d2]

theorem shift_only_is_circulant (X : Matrix (Fin 3) (Fin 3) ℂ) (hP : X * P = P * X) :
    X = X 0 0 • (1 : Matrix (Fin 3) (Fin 3) ℂ) + X 0 1 • P + X 0 2 • (P * P) := by
  have f := fun i j => congrFun (congrFun hP i) j
  simp [P, Matrix.mul_apply, Fin.sum_univ_three] at f
  have := f 0 0; have := f 0 1; have := f 0 2; have := f 1 0; have := f 1 1; have := f 1 2
  have := f 2 0; have := f 2 1; have := f 2 2
  ext i j; fin_cases i <;> fin_cases j <;>
    simp [P] <;> simp_all

end MagTorus

#print axioms MagTorus.Z2_not_quantised
#print axioms MagTorus.clock_shift
#print axioms MagTorus.heisenberg_forces_degenerate
#print axioms MagTorus.shift_only_is_circulant
