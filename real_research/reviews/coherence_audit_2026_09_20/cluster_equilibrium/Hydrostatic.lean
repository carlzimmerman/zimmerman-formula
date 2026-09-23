import Mathlib

/-! Algebraic implications of P=rho*C and P'=-rho*v²/r.
The action-to-fluid dictionary, derivative product rule and explicit integral
solution are separate obligations. No full halo or stability theorem here. -/
namespace HydrostaticAudit

theorem logarithmic_slope (r rho C rhoPrime CPrime v2 : ℝ)
    (hr : r ≠ 0) (hd : rho ≠ 0) (hc : C ≠ 0)
    (balance : rhoPrime*C+rho*CPrime = -rho*v2/r) :
    r*rhoPrime/rho = -v2/C-r*CPrime/C := by
  field_simp at balance ⊢
  nlinarith [balance]

theorem sign_error (r C CPrime v2 : ℝ) :
    (-v2/C+r*CPrime/C)-(-v2/C-r*CPrime/C) = 2*r*CPrime/C := by ring

/-- Mass is linear in an independently chosen density amplitude; shape alone
does not select that amplitude. I is the already-integrated unit profile. -/
theorem amplitude_matching (I M : ℝ) (hI : 0<I) (hM : 0<M) :
    ∃ amplitude : ℝ, 0<amplitude ∧ amplitude*I=M := by
  refine ⟨M/I, by positivity, ?_⟩
  field_simp

/-- Declared affine EOS has positive density and zero pressure at its anchor;
it cannot simultaneously equal p=w*rho there when w and rho0 are positive. -/
theorem affine_is_not_isothermal (w rho0 : ℝ) (hw : 0<w) (hr : 0<rho0) :
    w*(rho0-rho0) ≠ w*rho0 := by
  have h : 0<w*rho0 := mul_pos hw hr
  simp only [sub_self,mul_zero]
  exact ne_of_lt h

#print axioms logarithmic_slope
#print axioms sign_error
#print axioms amplitude_matching
#print axioms affine_is_not_isothermal
end HydrostaticAudit
