import Mathlib.Data.Real.Basic
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Positivity

namespace EntropyClockProfile
noncomputable def v (a R L : ℝ) := (1+4*R*a^3)/(1+(4*R+L)*a^3)

theorem profile_interval (a R L : ℝ) (ha : 0<a) (hR : 0≤R) (hL : 0<L) :
    0<v a R L ∧ v a R L<1 := by
  have hp : 0<a^3 := pow_pos ha 3
  have hn : 0<1+4*R*a^3 := by positivity
  have hd : 0<1+(4*R+L)*a^3 := by positivity
  unfold v
  constructor
  · exact div_pos hn hd
  · apply (div_lt_one hd).2
    nlinarith [mul_pos hL hp]

/- The derivative on the left is computed in SymPy. This theorem certifies
the rational flow identity, not a HasDerivAt assertion. The installed calculus
imports currently conflict; no formal derivative certificate is claimed. -/
theorem profile_flow (a R L : ℝ) (ha : 0<a) (hR : 0≤R) (hL : 0<L) :
    a*(-3*L*a^2/(1+(4*R+L)*a^3)^2) =
      3/(1+4*R*a^3)*(v a R L)*(v a R L-1) := by
  have hn : 1+4*R*a^3 ≠ 0 := ne_of_gt (by positivity)
  have hd : 1+(4*R+L)*a^3 ≠ 0 := ne_of_gt (by positivity)
  unfold v
  field_simp
  ring

theorem kinetic_domain (A e w : ℝ) (hA : 0<A) (he : e<0) (hw : 0<w) (hu : w<1) :
    0<(-3*A*w/e) ∧ 0<(-3*A*w/e)*e+3*A := by
  have hne : e≠0 := ne_of_lt he
  constructor
  · apply div_pos_of_neg_of_neg <;> nlinarith
  · have hi : (-3*A*w/e)*e+3*A=3*A*(1-w) := by field_simp; ring
    rw [hi]
    have hw1 : 0<1-w := by linarith
    positivity

#print axioms profile_interval
#print axioms profile_flow
#print axioms kinetic_domain
end EntropyClockProfile
