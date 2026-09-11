import Mathlib.Analysis.Complex.Exponential
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Positivity

/-! Conditional finite-time MOND susceptibility obstruction.
The hypothesis bounding force by C * exp(L*t) * ε is NOT derived here from
the gravity PDE. The theorem gives a necessary formation-time inequality
if that estimate holds and the exact exponential MOND relation is attained.
No existence, Dirac closure, observational validity, or uniqueness is assumed
to have been proved by compiling this file.
-/

namespace FiniteTimeMOND
noncomputable section

def force (a g : ℝ) : ℝ := (1 - Real.exp (-(g/a))) * g

theorem force_upper (a g : ℝ) (hg : 0 ≤ g) :
    force a g ≤ g^2/a := by
  have ht : 1 - Real.exp (-(g/a)) ≤ g/a := by
    have := Real.add_one_le_exp (-(g/a))
    linarith
  calc
    force a g ≤ (g/a)*g := mul_le_mul_of_nonneg_right ht hg
    _ = g^2/a := by ring

/-- Exact MOND requires a gain that diverges as the source amplitude vanishes. -/
theorem necessary_gain (a n ε g gain : ℝ)
    (ha : 0 < a) (he : 0 < ε) (hg : 0 ≤ g)
    (hb : g ≤ gain*ε) (hm : force a g = ε*n) :
    a*n ≤ gain^2*ε := by
  have hf : ε*n ≤ g^2/a := hm ▸ force_upper a g hg
  have hf' := (le_div_iff₀ ha).mp hf
  have hs : g^2 ≤ (gain*ε)^2 := by
    simpa only [pow_two] using mul_self_le_mul_self hg hb
  have hmul : (a*n)*ε ≤ (gain^2*ε)*ε := by nlinarith only [hf',hs]
  nlinarith only [hmul,he]

theorem necessary_exponential_gain (a n ε g C L t : ℝ)
    (ha : 0 < a) (he : 0 < ε) (hg : 0 ≤ g)
    (hb : g ≤ (C*Real.exp (L*t))*ε) (hm : force a g = ε*n) :
    a*n ≤ C^2*Real.exp (2*(L*t))*ε := by
  have h := necessary_gain a n ε g (C*Real.exp (L*t)) ha he hg hb hm
  have hx : Real.exp (2*(L*t)) = (Real.exp (L*t))^2 := by
    rw [two_mul,Real.exp_add,pow_two]
  rw [hx]
  nlinarith only [h]

/-- An exact threshold formulation, avoiding any assumption of a PDE estimate. -/
theorem formation_after_threshold (a n ε g C L t t0 : ℝ)
    (ha : 0 < a) (he : 0 < ε) (hL : 0 ≤ L)
    (hg : 0 ≤ g) (hb : g ≤ (C*Real.exp (L*t))*ε)
    (hm : force a g = ε*n)
    (hthreshold : C^2*Real.exp (2*(L*t0))*ε < a*n) : t0 < t := by
  have h := necessary_exponential_gain a n ε g C L t ha he hg hb hm
  by_contra ht
  have htime : t ≤ t0 := le_of_not_gt ht
  have harg : 2*(L*t) ≤ 2*(L*t0) := by nlinarith only [hL,htime]
  have hexp := Real.exp_le_exp.mpr harg
  have hcoef : 0 ≤ C^2*ε := mul_nonneg (sq_nonneg C) he.le
  have hproduct := mul_le_mul_of_nonneg_left hexp hcoef
  nlinarith only [h,hproduct,hthreshold]

/-- A source below the finite-gain threshold cannot satisfy exact MOND. -/
theorem exclusion_below_gain_threshold (a n ε g gain : ℝ)
    (ha : 0 < a) (he : 0 < ε) (hg : 0 ≤ g)
    (hb : g ≤ gain*ε) (hsmall : gain^2*ε < a*n) :
    force a g ≠ ε*n := by
  intro hm
  exact (not_lt_of_ge (necessary_gain a n ε g gain ha he hg hb hm)) hsmall

#print axioms necessary_gain
#print axioms necessary_exponential_gain
#print axioms formation_after_threshold
#print axioms exclusion_below_gain_threshold
end
end FiniteTimeMOND
