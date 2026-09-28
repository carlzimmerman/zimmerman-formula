import Mathlib

/-!
AS229 Lean certificate — exact closed forms of the CA5-GNC-R reciprocal
vacuum barrier  F(t) = 1 + (t + 1/t - 2)^2  about t_c = 1.

Certified here:
  (a) F(1+z) - 1 = z^4 / (1+z)^2        (exact closed form, for all z ≠ -1)
  (d) (F(1+z) - 1) / z^4 = 1 / (1+z)^2  (quartic order of the barrier)
  (r) deriv (fun s => s⁻¹) t = -(t^2)⁻¹ for t ≠ 0  (derivative fact used by the
      perturbation series)

These are the algebraic identities that carry the seed's flatness statement
(F'(1)=F''(1)=F'''(1)=0, F''''(1)=24, series F(1+z)-1 = z^4 - 2 z^5 + ...,
F'(1+z) = 4 z^3 - 10 z^4 + ...).  The full derivative-chain certificate for the
closed derivative form was attempted; this host's HasDerivAt typeclass
elaboration and the inability of rw to descend into function lambdas made the
chain unmaintainable within the run budget, so the derivative content is
certified here only at the first-derivative fact (r) and verified symbolically
(sympy exact series) and numerically (CK2-CK4) in the run's main evidence.
-/

noncomputable section
open Filter
open scoped Topology

/-- F(t) = 1 + (t + 1/t - 2)^2 -/
def F (t : ℝ) : ℝ := 1 + (t + t⁻¹ - 2)^2

/-- (a) exact closed form for the barrier increment -/
theorem F_sub_one_closed (z : ℝ) (hz : z ≠ -1) :
    F (1 + z) - 1 = z^4 / (1 + z)^2 := by
  unfold F
  have hz1 : 1 + z ≠ 0 := by
    intro h
    apply hz
    linarith
  have hz1sq : (1 + z)^2 ≠ 0 := pow_ne_zero 2 hz1
  field_simp [hz1, hz1sq]
  ring

/-- (d) quartic order: the barrier increment divided by z^4 has the exact limit shape -/
theorem barrier_quartic_order (z : ℝ) (hz : z ≠ -1) (hz0 : z ≠ 0) :
    (F (1 + z) - 1) / z^4 = 1 / (1 + z)^2 := by
  rw [F_sub_one_closed z hz]
  have hz1 : 1 + z ≠ 0 := by
    intro h
    apply hz
    linarith
  field_simp [hz0, hz1]

/-- (r) derivative of the reciprocal at a nonzero point -/
theorem deriv_inv_at (t : ℝ) (ht : t ≠ 0) :
    deriv (fun s : ℝ => s⁻¹) t = -(t ^ 2)⁻¹ :=
  (hasDerivAt_inv ht).deriv

end

#print axioms F_sub_one_closed
#print axioms barrier_quartic_order
#print axioms deriv_inv_at