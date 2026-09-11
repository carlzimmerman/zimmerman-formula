import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Linarith

/- Exact real-algebra leaf for spline_obstruction.py.
   The differentiation and spline-to-jets bridge are checked symbolically,
   not formalized here. This is not a no-go for approximation or physics. -/
namespace SplineJetObstruction
noncomputable section

/-- For D=G+2zG', its second z derivative is 5G''+2zG'''.
At a positive knot, continuity of G'' and D'' forces continuity of G'''. -/
theorem third_jet_continuity (z left2 right2 left3 right3 : ℝ)
    (hz : 0 < z) (h2 : left2 = right2)
    (hd2 : 5*left2+2*z*left3 = 5*right2+2*z*right3) :
    left3 = right3 := by
  have hp : 2*z*(left3-right3) = 0 := by nlinarith only [h2,hd2]
  have hn : 2*z ≠ 0 := ne_of_gt (by linarith only [hz])
  exact sub_eq_zero.mp ((mul_eq_zero.mp hp).resolve_left hn)

/-- No nonzero coefficient jump survives all four derived join conditions
at a positive knot. Coefficients use powers of z minus the knot. -/
theorem cubic_join_unique (z a0 a1 a2 a3 : ℝ)
    (hz : 0 < z) (h0 : a0=0) (h1 : a1=0) (h2 : 2*a2=0)
    (hd2 : 10*a2+12*z*a3=0) :
    a0=0 ∧ a1=0 ∧ a2=0 ∧ a3=0 := by
  have ha2 : a2=0 := by linarith only [h2]
  have hp : (12*z)*a3=0 := by nlinarith only [ha2,hd2]
  have hn : 12*z ≠ 0 := ne_of_gt (by linarith only [hz])
  exact ⟨h0,h1,ha2,(mul_eq_zero.mp hp).resolve_left hn⟩

#print axioms third_jet_continuity
#print axioms cubic_join_unique
end
end SplineJetObstruction
