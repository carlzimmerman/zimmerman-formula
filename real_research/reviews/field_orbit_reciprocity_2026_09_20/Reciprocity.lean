import Mathlib

/-! Completion-independent compatibility of spherical orbital slope and
external-field anisotropy in the local AQUAL static action class.
The exterior-flux derivative is formalized; the 3D PDE linearization and
Green function are independently symbolic in verify.py and sourced in README.
No observation, global novelty, or full covariant theory is certified. -/
namespace FieldOrbitReciprocity
noncomputable section
set_option backward.isDefEq.respectTransparency false

theorem flux_derivative {g μ : ℝ → ℝ} {r dg dμ : ℝ}
    (hg : HasDerivAt g dg r) (hμ : HasDerivAt μ dμ (g r)) :
    HasDerivAt (fun t => t^2*g t*μ (g t))
      (2*r*g r*μ (g r)+r^2*dg*(μ (g r)+g r*dμ)) r := by
  convert! (((hasDerivAt_id r).pow 2).mul hg).mul (hμ.comp r hg) using 1
  dsimp
  ring

theorem slope_from_flux {r g dg μ dμ L β : ℝ}
    (hr : r ≠ 0) (hg : g ≠ 0) (hμ : μ ≠ 0)
    (hflux : 2*r*g*μ+r^2*dg*(μ+g*dμ)=0)
    (hL : g*dμ=μ*L) (hβ : 2*β=1+r*dg/g) :
    (1+L)*(1-2*β)=2 := by
  have hb : g*(2*β-1)=r*dg := by
    field_simp at hβ
    nlinarith [hβ]
  have hf : r*g*μ * ((1+L)*(2*β-1)+2)=0 := by
    calc
      r*g*μ * ((1+L)*(2*β-1)+2) =
          2*r*g*μ + r*μ*(1+L)*(g*(2*β-1)) := by ring
      _ = 2*r*g*μ+r^2*dg*(μ+g*dμ) := by rw [hb, hL]; ring
      _ = 0 := hflux
  have hn : r*g*μ ≠ 0 := mul_ne_zero (mul_ne_zero hr hg) hμ
  have := (mul_eq_zero.mp hf).resolve_left hn
  linarith

/-- All dependence on the interpolation function cancels. E is the internal
force magnitude parallel/perpendicular to the uniform external field, at equal
radius, in the linear external-field-dominated point-source Green function. -/
theorem completion_independent_reciprocity {E L β : ℝ}
    (hshape : E^2=1+L) (horbit : (1+L)*(1-2*β)=2) :
    E^2*(1-2*β)=2 := by rw [hshape]; exact horbit

/-- Full calculus-to-reciprocity statement, conditional on the independently
checked external-field Green-function relation at the SAME acceleration. -/
theorem action_class_reciprocity {g μ : ℝ → ℝ} {r dg dμ E β : ℝ}
    (hr : r ≠ 0) (hg0 : g r ≠ 0) (hμ0 : μ (g r) ≠ 0)
    (hg : HasDerivAt g dg r) (hμ : HasDerivAt μ dμ (g r))
    (hconstant : HasDerivAt (fun t => t^2*g t*μ (g t)) 0 r)
    (hβ : 2*β=1+r*dg/g r)
    (hshape : E^2=1+g r*dμ/μ (g r)) : E^2*(1-2*β)=2 := by
  have hf := (flux_derivative hg hμ).unique hconstant
  have he : g r*dμ=μ (g r)*(g r*dμ/μ (g r)) := by field_simp
  exact completion_independent_reciprocity hshape
    (slope_from_flux hr hg0 hμ0 hf he hβ)

/-- No choice of response elasticity can repair incompatible observables
while retaining both physical reductions. This does not exclude other gravity
actions, external-field corrections, or failed observational assumptions. -/
theorem no_response_retuning {E β : ℝ} (hbad : E^2*(1-2*β) ≠ 2) :
    ¬ ∃ L : ℝ, E^2=1+L ∧ (1+L)*(1-2*β)=2 := by
  rintro ⟨L,hshape,horbit⟩
  exact hbad (completion_independent_reciprocity hshape horbit)

theorem deep_anisotropy {E : ℝ} (hE : 0 ≤ E)
    (h : E^2*(1-2*(0:ℝ))=2) : E=Real.sqrt 2 := by
  have hs := Real.sq_sqrt (by norm_num : (0:ℝ) ≤ 2)
  have hn := Real.sqrt_nonneg (2:ℝ)
  nlinarith

/-- Published QUMOND duality: (1+L)(1+K)=1. Unlike AQUAL, its external-field
Green function has E*(1+K/2)=1. The same isolated curve gives a different law. -/
theorem qumond_reciprocity {E L K β : ℝ}
    (hdual : (1+L)*(1+K)=1)
    (horbit : (1+L)*(1-2*β)=2)
    (hshape : E*(1+K/2)=1) : E*(3-2*β)=4 := by
  have hd : 1+L ≠ 0 := by intro h; rw [h] at horbit; norm_num at horbit
  have hk : (1+L)*(2*(1+K)-(1-2*β))=0 := by nlinarith [hdual, horbit]
  have hk' := (mul_eq_zero.mp hk).resolve_left hd
  have he : 3-2*β=4*(1+K/2) := by linarith [hk']
  rw [he]
  nlinarith [hshape]

theorem deep_qumond {E : ℝ} (h : E*(3-2*(0:ℝ))=4) : E=4/3 := by linarith

theorem deep_laws_distinct : (4/3 : ℝ)^2 ≠ 2 := by norm_num

/-- A negative inferred Poisson density is a signed effective source, not
negative baryonic mass: the Green numerator is 2z²-Gamma R². -/
theorem equatorial_effective_density_negative {Γ R : ℝ}
    (hΓ : 1 < Γ) (hR : 0 < R) : (Γ-1)*(2*(0:ℝ)^2-Γ*R^2)<0 := by
  have hp : 0 < Γ*R^2 := mul_pos (by linarith) (sq_pos_of_pos hR)
  have hn : 2*(0:ℝ)^2-Γ*R^2<0 := by nlinarith
  exact mul_neg_of_pos_of_neg (by linarith) hn

/-- The zero-density cone's tan² angle from the external-field axis.
The cone only has a sign-boundary interpretation when Gamma>1. -/
theorem cone_orbit_identity {Γ β t : ℝ}
    (hΓ : Γ ≠ 0) (horbit : Γ*(1-2*β)=2) (hcone : Γ*t=2) :
    t=1-2*β := by
  apply (mul_left_cancel₀ hΓ)
  rw [hcone, horbit]

#print axioms flux_derivative
#print axioms slope_from_flux
#print axioms completion_independent_reciprocity
#print axioms action_class_reciprocity
#print axioms no_response_retuning
#print axioms deep_anisotropy
#print axioms qumond_reciprocity
#print axioms deep_qumond
#print axioms deep_laws_distinct
#print axioms equatorial_effective_density_negative
#print axioms cone_orbit_identity
end
end FieldOrbitReciprocity
