import Mathlib

/-! Scoped inverse bridges. The source-to-FLRW and action-to-stress
interpretations are hypotheses documented in RESULT.md, not Lean field theory. -/
namespace InversePressure20260926

theorem continuity_integrating_factor
    (e : ℝ → ℝ) (a edot tension : ℝ)
    (he : HasDerivAt e edot a)
    (hcont : a*edot+3*(e a-tension)=0) :
    HasDerivAt (fun x => x^3*e x) (3*a^2*tension) a := by
  have hh := ((hasDerivAt_pow 3 a).mul he)
  convert hh using 1 <;> simp only [Nat.cast_ofNat]
  have hmul := congrArg (fun z : ℝ => a^2*z) hcont
  nlinarith [hmul]

theorem constant_pressure_has_dust_family (a tension D : ℝ) (ha : a ≠ 0) :
    a*(-3*D/a^4)+3*((tension+D/a^3)-tension)=0 := by
  field_simp
  <;> ring

theorem one_density_boundary_fixes_dust (a tension D1 D2 : ℝ)
    (ha : a ≠ 0)
    (he : tension+D1/a^3=tension+D2/a^3) : D1=D2 := by
  have h : D1/a^3=D2/a^3 := by linarith
  exact (div_left_inj' (pow_ne_zero 3 ha)).mp h

theorem pressure_density_identification_cost (epsilon tension w : ℝ)
    (he : 0 < epsilon) (hp : tension = -w*epsilon) :
    tension=epsilon ↔ w = -1 := by
  constructor
  · intro h
    nlinarith
  · intro h
    rw [h] at hp
    linarith

theorem dust_shift_cancels_pressure (a F Fprime D : ℝ) (ha : a ≠ 0) :
    a*(Fprime-3*D/a^4)+3*(F+D/a^3)=a*Fprime+3*F := by
  field_simp
  <;> ring

theorem normalized_pressure_null (a0 a00 Q Q0 K : ℝ)
    (h0 : a00 ≠ 0) (hq : Q ≠ 0) (hk : K ≠ 0)
    (h : a0^2=K*Q) (hbase : a00^2=K*Q0) :
    (a0/a00)^2*(Q0/Q)=1 := by
  have hprod : a0^2*Q0=a00^2*Q := by rw [h,hbase];ring
  field_simp
  nlinarith [hprod]

#print axioms continuity_integrating_factor
#print axioms constant_pressure_has_dust_family
#print axioms one_density_boundary_fixes_dust
#print axioms pressure_density_identification_cost
#print axioms dust_shift_cancels_pressure
#print axioms normalized_pressure_null
end InversePressure20260926
