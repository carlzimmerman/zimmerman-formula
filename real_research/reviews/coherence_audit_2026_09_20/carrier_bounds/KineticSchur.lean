import Mathlib

/-! Universal algebraic Schur certificate for three positive squares.
Mapping an action to this core is an explicit, separately checked hypothesis. -/
namespace CarrierSchur
noncomputable def den (A B E H C : ℝ) := A*H^2+B*C^2+E
noncomputable def k11 (A B E H C : ℝ) := 2*A*(B*C^2+E)/den A B E H C
noncomputable def k12 (A B E H C : ℝ) := 2*A*B*H*C/den A B E H C
noncomputable def k22 (A B E H C : ℝ) := 2*B*(A*H^2+E)/den A B E H C

theorem positive_den (A B E H C : ℝ) (ha : 0<A) (hb : 0<B) (he : 0<E) :
    0<den A B E H C := by unfold den; positivity

theorem determinant (A B E H C : ℝ) :
    k11 A B E H C*k22 A B E H C-(k12 A B E H C)^2 =
      4*A*B*E/den A B E H C := by
  unfold k11 k12 k22
  by_cases hd : den A B E H C = 0
  · simp [hd]
  · field_simp
    unfold den
    ring

theorem positive_minors (A B E H C : ℝ) (ha : 0<A) (hb : 0<B) (he : 0<E) :
    0<k11 A B E H C ∧
    0<k11 A B E H C*k22 A B E H C-(k12 A B E H C)^2 := by
  have hd := positive_den A B E H C ha hb he
  constructor
  · unfold k11; positivity
  · rw [determinant]; positivity

theorem quadratic_positive (A B E H C v u : ℝ)
    (ha : 0<A) (hb : 0<B) (he : 0<E) (huv : v≠0 ∨ u≠0) :
    0<k11 A B E H C*v^2+2*k12 A B E H C*v*u+k22 A B E H C*u^2 := by
  obtain ⟨h11, hdet⟩ := positive_minors A B E H C ha hb he
  by_cases hu : u=0
  · have hv : v≠0 := huv.resolve_right (not_not_intro hu)
    subst u
    simpa using mul_pos h11 (sq_pos_of_ne_zero hv)
  · have hp := mul_pos hdet (sq_pos_of_ne_zero hu)
    have hs := sq_nonneg (k11 A B E H C*v+k12 A B E H C*u)
    have ident : k11 A B E H C *
      (k11 A B E H C*v^2+2*k12 A B E H C*v*u+k22 A B E H C*u^2) =
      (k11 A B E H C*v+k12 A B E H C*u)^2+
      (k11 A B E H C*k22 A B E H C-(k12 A B E H C)^2)*u^2 := by ring
    have hp2 : 0<k11 A B E H C *
      (k11 A B E H C*v^2+2*k12 A B E H C*v*u+k22 A B E H C*u^2) := by nlinarith
    exact (mul_pos_iff_of_pos_left h11).mp hp2

#print axioms positive_den
#print axioms determinant
#print axioms positive_minors
#print axioms quadratic_positive
end CarrierSchur
