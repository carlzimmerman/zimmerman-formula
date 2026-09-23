import Mathlib

/-! Positive kinetic matrix of the independently reduced flat-FRW quadratic
action. The action-to-matrix derivation is symbolic, not formalized here.
Variables: a>0, alpha=c14>0, b=c2>0, eps>0, t=-F_Q>0, k>0;
H and Q are arbitrary real numbers. This proves absence of scalar kinetic
ghosts at quadratic order under those assumptions, not gradient stability.
-/
namespace RepairedClock
noncomputable def den (a α b e t k H Q : ℝ) : ℝ :=
  4*H^2*a^2*e*(3*b+2)+a^2*b*t*Q^2+2*α*b*e*k^2
noncomputable def k11 (a α b e t k H Q : ℝ) : ℝ :=
  4*a^3*(3*b+2)*(a^2*t*Q^2+2*α*e*k^2)/den a α b e t k H Q
noncomputable def k12 (a α b e t k H Q : ℝ) : ℝ :=
  4*H*a^5*t*Q*(3*b+2)/den a α b e t k H Q
noncomputable def k22 (a α b e t k H Q : ℝ) : ℝ :=
  2*a^3*t*(2*H^2*a^2*(3*b+2)+α*b*k^2)/den a α b e t k H Q

theorem denominator_positive (a α b e t k H Q : ℝ)
    (ha : 0<a) (hα : 0<α) (hb : 0<b) (he : 0<e) (ht : 0<t) (hk : 0<k) :
    0 < den a α b e t k H Q := by unfold den; positivity

theorem determinant_identity (a α b e t k H Q : ℝ)
    (hd : den a α b e t k H Q ≠ 0) :
    k11 a α b e t k H Q * k22 a α b e t k H Q - (k12 a α b e t k H Q)^2
      = 8*a^6*α*t*k^2*(3*b+2)/den a α b e t k H Q := by
  unfold k11 k12 k22
  field_simp
  unfold den
  ring

theorem principal_minors_positive (a α b e t k H Q : ℝ)
    (ha : 0<a) (hα : 0<α) (hb : 0<b) (he : 0<e) (ht : 0<t) (hk : 0<k) :
    0 < k11 a α b e t k H Q ∧
    0 < k11 a α b e t k H Q * k22 a α b e t k H Q - (k12 a α b e t k H Q)^2 := by
  have hd := denominator_positive a α b e t k H Q ha hα hb he ht hk
  constructor
  · unfold k11; positivity
  · rw [determinant_identity a α b e t k H Q (ne_of_gt hd)]
    positivity

theorem sylvester_two (A B C x y : ℝ) (hA : 0<A) (hD : 0<A*C-B^2)
    (hxy : x≠0 ∨ y≠0) : 0 < A*x^2+2*B*x*y+C*y^2 := by
  by_cases hy : y=0
  · have hx : x≠0 := hxy.resolve_right (not_not_intro hy)
    subst y
    simpa using mul_pos hA (sq_pos_of_ne_zero hx)
  · have hp := mul_pos hD (sq_pos_of_ne_zero hy)
    have hs := sq_nonneg (A*x+B*y)
    have identity : A*(A*x^2+2*B*x*y+C*y^2) =
        (A*x+B*y)^2+(A*C-B^2)*y^2 := by ring
    have hab : 0 < A*(A*x^2+2*B*x*y+C*y^2) := by nlinarith
    exact (mul_pos_iff_of_pos_left hA).mp hab

theorem repaired_scalar_kinetic_positive (a α b e t k H Q x y : ℝ)
    (ha : 0<a) (hα : 0<α) (hb : 0<b) (he : 0<e) (ht : 0<t) (hk : 0<k)
    (hxy : x≠0 ∨ y≠0) :
    0 < k11 a α b e t k H Q*x^2 + 2*k12 a α b e t k H Q*x*y
      + k22 a α b e t k H Q*y^2 := by
  obtain ⟨h1,h2⟩ := principal_minors_positive a α b e t k H Q ha hα hb he ht hk
  exact sylvester_two _ _ _ x y h1 h2 hxy

#print axioms denominator_positive
#print axioms determinant_identity
#print axioms principal_minors_positive
#print axioms sylvester_two
#print axioms repaired_scalar_kinetic_positive
end RepairedClock
