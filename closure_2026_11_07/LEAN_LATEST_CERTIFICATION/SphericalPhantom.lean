import Mathlib
open Real
namespace SphericalPhantom

/-- Simple-mu spherical phantom mass, outside any central point singularity. -/
noncomputable def phantomMass (a G : ℝ) (M : ℝ → ℝ) (r : ℝ) : ℝ :=
  M r * (Real.sqrt (1/4 + a*r^2/(G*M r)) - 1/2)

/-- A radial derivative identity converts the apparently signed density into
one nonnegative term plus one strictly positive term. -/
theorem derivative_normal_form {a G m dm r s : ℝ}
    (hG : 0 < G) (hm : 0 < m) (hs : 0 < s)
    (hsq : s^2 = 1/4 + a*r^2/(G*m)) :
    dm*(s-1/2) + m*((1/(2*s))*((a*(2*r))*(G*m)-(a*r^2)*(G*dm))/(G*m)^2)
      = dm*(s-1/2)^2/(2*s) + a*r/(G*s) := by
  have hG0 := hG.ne'; have hm0 := hm.ne'; have hs0 := hs.ne'
  have hrel : G*m*s^2 = G*m/4 + a*r^2 := by
    have := (eq_div_iff (mul_ne_zero hG0 hm0)).mp
      (by linarith : s^2-1/4 = a*r^2/(G*m))
    nlinarith
  field_simp
  linear_combination 4*dm*hrel

theorem phantomMass_hasDerivAt {a G r dm : ℝ} {M : ℝ → ℝ}
    (ha : 0 < a) (hG : 0 < G) (hm : 0 < M r) (hr : 0 < r)
    (hM : HasDerivAt M dm r) :
    HasDerivAt (phantomMass a G M)
      (dm*(Real.sqrt (1/4+a*r^2/(G*M r))-1/2)^2 /
        (2*Real.sqrt (1/4+a*r^2/(G*M r))) +
        a*r/(G*Real.sqrt (1/4+a*r^2/(G*M r)))) r := by
  have hp : 0 < 1/4 + a*r^2/(G*M r) := by positivity
  have hs : 0 < Real.sqrt (1/4 + a*r^2/(G*M r)) := Real.sqrt_pos.mpr hp
  have hq := (((hasDerivAt_id r).pow 2).const_mul a).div (hM.const_mul G)
    (mul_ne_zero hG.ne' hm.ne')
  have hroot := (Real.hasDerivAt_sqrt hp.ne').comp r ((hasDerivAt_const r (1/4 : ℝ)).add hq)
  have hf := hM.mul (hroot.sub_const (1/2))
  have hraw : HasDerivAt (phantomMass a G M)
      (dm*(Real.sqrt (1/4+a*r^2/(G*M r))-1/2) +
       M r*((1/(2*Real.sqrt (1/4+a*r^2/(G*M r))))*
        ((a*(2*r))*(G*M r)-(a*r^2)*(G*dm))/(G*M r)^2)) r := by
    convert! hf using 1 <;>
      (try simp only [Pi.add_apply, Pi.div_apply, Pi.pow_apply,
        Function.comp_apply, id_eq, mul_one, zero_add]) <;> ring
  rw [derivative_normal_form (a := a) (G := G) (m := M r) (dm := dm) (r := r)
    hG hm hs (Real.sq_sqrt hp.le)] at hraw
  exact hraw

/-- Universal positivity for differentiable nondecreasing enclosed mass,
not a finite census of four profiles. Spherical isolation and simple-mu remain
model assumptions. No statement about nonspherical or transient fields. -/
theorem phantomMass_deriv_pos {a G r dm : ℝ} {M : ℝ → ℝ}
    (ha : 0 < a) (hG : 0 < G) (hm : 0 < M r) (hr : 0 < r)
    (hM : HasDerivAt M dm r) (hdm : 0 ≤ dm) :
    0 < deriv (phantomMass a G M) r := by
  rw [(phantomMass_hasDerivAt ha hG hm hr hM).deriv]
  have hs : 0 < Real.sqrt (1/4+a*r^2/(G*M r)) := by positivity
  have h1 : 0 ≤ dm*(Real.sqrt (1/4+a*r^2/(G*M r))-1/2)^2 /
      (2*Real.sqrt (1/4+a*r^2/(G*M r))) := by positivity
  have h2 : 0 < a*r/(G*Real.sqrt (1/4+a*r^2/(G*M r))) := by positivity
  linarith

theorem spherical_density_pos {a G r dm : ℝ} {M : ℝ → ℝ}
    (ha : 0 < a) (hG : 0 < G) (hm : 0 < M r) (hr : 0 < r)
    (hM : HasDerivAt M dm r) (hdm : 0 ≤ dm) :
    0 < deriv (phantomMass a G M) r / (4*Real.pi*r^2) := by
  exact div_pos (phantomMass_deriv_pos ha hG hm hr hM hdm) (by positivity)

theorem static_switch_on {rho rhoDE : ℝ} (hrho : 0 < rho) (hDE : 0 < rhoDE) :
    0 < rho/rhoDE ∧ 0 < 2+rho/rhoDE := by
  have h := div_pos hrho hDE
  exact ⟨h, by linarith⟩

end SphericalPhantom
#print axioms SphericalPhantom.derivative_normal_form
#print axioms SphericalPhantom.phantomMass_hasDerivAt
#print axioms SphericalPhantom.phantomMass_deriv_pos
#print axioms SphericalPhantom.spherical_density_pos
#print axioms SphericalPhantom.static_switch_on
