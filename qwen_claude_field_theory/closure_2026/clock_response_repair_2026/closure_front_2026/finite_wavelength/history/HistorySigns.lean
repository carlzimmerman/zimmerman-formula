import Mathlib.Data.Real.Basic
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity

namespace FixedHistorySigns

/- Pointwise real-algebra certificate. The ODE invariant region, action-to-G
map, and normalization are proved in the report and checked symbolically;
they are not formalized as differential equations in this file. -/

noncomputable def lowerU (m : ℝ) : ℝ := 3*m/(2*(m+2))
noncomputable def upperBeta (m : ℝ) : ℝ := 3*m^4/(20*(m+1)^3)
noncomputable def normalized (m u beta eps : ℝ) : ℝ :=
  2*u-1+u/(m^2+beta*u)-eps
noncomputable def positiveNumerator (m : ℝ) : ℝ :=
  3*(2533320*m^6+10303237*m^5+9473074*m^4+1333000*m^3+2533120*m^2+8133280*m+4000000)
noncomputable def positiveDenominator (m : ℝ) : ℝ :=
  100000*m*(m+2)*(40*m^4+209*m^3+360*m^2+280*m+80)

theorem lower_identity (m : ℝ) (hm : 0 < m) :
    normalized m (lowerU m) (upperBeta m) (1/100000) - 1/10 =
      positiveNumerator m / positiveDenominator m := by
  have h1 : m+1 ≠ 0 := ne_of_gt (by positivity)
  have h2 : m+2 ≠ 0 := ne_of_gt (by positivity)
  have hpoly : 40*m^4+209*m^3+360*m^2+280*m+80 ≠ 0 :=
    ne_of_gt (by positivity)
  have hc : m^2+3*m^4/(20*(m+1)^3)*(3*m/(2*(m+2))) ≠ 0 :=
    ne_of_gt (by positivity)
  unfold normalized lowerU upperBeta positiveNumerator positiveDenominator
  field_simp
  <;> ring

theorem lower_exceeds_tenth (m : ℝ) (hm : 0 < m) :
    1/10 < normalized m (lowerU m) (upperBeta m) (1/100000) := by
  have hn : 0 < positiveNumerator m := by unfold positiveNumerator; positivity
  have hd : 0 < positiveDenominator m := by unfold positiveDenominator; positivity
  have hp := div_pos hn hd
  rw [← lower_identity m hm] at hp
  linarith

theorem fraction_monotone (a u0 u beta upper : ℝ)
    (ha : 0 < a) (hu0 : 0 ≤ u0) (hu : u0 ≤ u)
    (hb : 0 ≤ beta) (hub : beta ≤ upper) :
    u0/(a+upper*u0) ≤ u/(a+beta*u) := by
  have hu' : 0 ≤ u := le_trans hu0 hu
  have hup : 0 ≤ upper := le_trans hb hub
  have hd0 : 0 < a+upper*u0 := by positivity
  have hd : 0 < a+beta*u := by positivity
  apply (div_le_div_iff₀ hd0 hd).2
  have hp1 := mul_nonneg (le_of_lt ha) (sub_nonneg.mpr hu)
  have hp2 := mul_nonneg (mul_nonneg hu0 hu') (sub_nonneg.mpr hub)
  nlinarith

theorem full_bound (m u beta eps : ℝ) (hm : 0 < m)
    (hu : lowerU m ≤ u) (hb : 0 ≤ beta) (hub : beta ≤ upperBeta m)
    (he : eps ≤ 1/100000) :
    1/10 < normalized m u beta eps := by
  have hu0 : 0 ≤ lowerU m := by unfold lowerU; positivity
  have hfrac := fraction_monotone (m^2) (lowerU m) u beta (upperBeta m)
    (sq_pos_of_pos hm) hu0 hu hb hub
  have hlo := lower_exceeds_tenth m hm
  unfold normalized at *
  linarith

#print axioms lower_identity
#print axioms lower_exceeds_tenth
#print axioms fraction_monotone
#print axioms full_bound

end FixedHistorySigns
