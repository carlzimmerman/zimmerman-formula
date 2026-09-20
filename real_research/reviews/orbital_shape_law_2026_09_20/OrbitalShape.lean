import Mathlib

/-! Conditional orbital-shape results for the specified rational constitutive
law. Physical hypotheses: isolated spherical modified gravity, ordinary test
body inertia, circular orbits, constant positive acceleration normalization.
This does not certify observations, novelty, or a covariant completion. -/
namespace OrbitalShape
noncomputable section
set_option backward.isDefEq.respectTransparency false

def mu (x : ℝ) : ℝ := 1 - 1 / (1+x)^2
def alpha (q : ℝ) : ℝ := 2*q^2/(1+q)
def slope (q : ℝ) : ℝ := 1/2 - (1+q)/(1+q+2*q^2)

theorem mu_derivative {x : ℝ} (hx : 1+x ≠ 0) :
    HasDerivAt mu (2/(1+x)^3) x := by
  have h := ((hasDerivAt_const x (1 : ℝ)).div
    (((hasDerivAt_id x).const_add 1).pow 2) (pow_ne_zero 2 hx)).const_sub 1
  convert! h using 1
  dsimp
  field_simp
  ring

theorem response_elasticity {x : ℝ} (hx : 0 < x) :
    x * (2/(1+x)^3) / mu x = alpha (1/(1+x)) := by
  have h1 : 1+x ≠ 0 := by positivity
  have h2 : 2+x ≠ 0 := by positivity
  have hm : (1+x)^2-1 ≠ 0 := by nlinarith
  unfold mu alpha
  field_simp
  ring

theorem observable_root {x : ℝ} (hx : 0 ≤ x) :
    Real.sqrt (1-mu x) = 1/(1+x) := by
  have hn : 0 ≤ 1/(1+x) := by positivity
  have he : 1-mu x = (1/(1+x))^2 := by
    unfold mu
    field_simp
    ring
  rw [he, Real.sqrt_sq hn]

/-- The radial derivative of spherical flux, proved by calculus. -/
theorem flux_derivative {g μ : ℝ → ℝ} {r dg dμ : ℝ}
    (hg : HasDerivAt g dg r) (hμ : HasDerivAt μ dμ (g r)) :
    HasDerivAt (fun t => t^2*g t*μ (g t))
      (2*r*g r*μ (g r)+r^2*dg*(μ (g r)+g r*dμ)) r := by
  convert! (((hasDerivAt_id r).pow 2).mul hg).mul (hμ.comp r hg) using 1
  dsimp
  ring

/-- Constant exterior flux fixes the local derivative; no fit is used. -/
theorem exterior_flux_constraint {g μ : ℝ → ℝ} {r dg dμ : ℝ}
    (hg : HasDerivAt g dg r) (hμ : HasDerivAt μ dμ (g r))
    (hconstant : HasDerivAt (fun t => t^2*g t*μ (g t)) 0 r) :
    2*r*g r*μ (g r)+r^2*dg*(μ (g r)+g r*dμ)=0 :=
  (flux_derivative hg hμ).unique hconstant

/-- Logarithmic circular-speed slope beta=(1+r*g'/g)/2 follows from v²=rg.
The response elasticity A=g*μ'/μ fixes beta. -/
theorem slope_from_flux {r g dg μ dμ A β : ℝ}
    (hr : r ≠ 0) (hg : g ≠ 0) (hμ : μ ≠ 0)
    (hflux : 2*r*g*μ+r^2*dg*(μ+g*dμ)=0)
    (hA : g*dμ=μ*A) (hβ : 2*β=1+r*dg/g) :
    (1+A)*(2*β-1) = -2 := by
  have hb : g*(2*β-1)=r*dg := by
    field_simp at hβ
    nlinarith [hβ]
  have hf : r*g*μ * ((1+A)*(2*β-1)+2)=0 := by
    calc
      r*g*μ * ((1+A)*(2*β-1)+2) =
          2*r*g*μ + r*μ*(1+A)*(g*(2*β-1)) := by ring
      _ = 2*r*g*μ+r^2*dg*(μ+g*dμ) := by rw [hb, hA]; ring
      _ = 0 := hflux
  have hn : r*g*μ ≠ 0 := mul_ne_zero (mul_ne_zero hr hg) hμ
  have := (mul_eq_zero.mp hf).resolve_left hn
  linarith

theorem slope_elimination {q β : ℝ} (hq : 0 ≤ q)
    (h : (1+alpha q)*(2*β-1) = -2) : β=slope q := by
  have h1 : 1+q ≠ 0 := by positivity
  have h2 : 1+q+2*q^2 ≠ 0 := by positivity
  unfold alpha at h
  unfold slope
  field_simp at h ⊢
  nlinarith [h]

/-- Observable form: q=sqrt(1-f), f=Mb/Mdyn; no acceleration scale remains. -/
theorem observable_shape {q f β : ℝ} (hq : 0 ≤ q)
    (hf : f=1-q^2) (h : (1+alpha q)*(2*β-1) = -2) :
    β = 1/2 - (1+Real.sqrt (1-f))/(3-2*f+Real.sqrt (1-f)) := by
  have hs : Real.sqrt (1-f)=q := by
    rw [hf]
    convert Real.sqrt_sq hq using 1
    ring
  rw [hs, hf, slope_elimination hq h]
  unfold slope
  congr 2
  ring

/-- Assembled calculus-to-observable theorem. The physical input is locally
constant spherical flux; beta denotes the logarithmic circular-speed slope.
c=lambda/s is arbitrary positive and disappears from the observable law. -/
theorem rational_exterior_shape {g : ℝ → ℝ} {r dg c β : ℝ}
    (hr : 0 < r) (hc : 0 < c) (hg0 : 0 < g r)
    (hg : HasDerivAt g dg r)
    (hconstant : HasDerivAt (fun t => t^2*g t*mu (c*g t)) 0 r)
    (hβ : 2*β=1+r*dg/g r) :
    let f := mu (c*g r)
    β=1/2-(1+Real.sqrt (1-f))/(3-2*f+Real.sqrt (1-f)) := by
  dsimp only
  have hx : 0 < c*g r := mul_pos hc hg0
  have hd : 1+c*g r ≠ 0 := by positivity
  have hm : 0 < mu (c*g r) := by
    unfold mu
    have hp : 0 < (1+c*g r)^2 := by positivity
    apply sub_pos.mpr
    apply (div_lt_one hp).mpr
    nlinarith
  have hμ : HasDerivAt (fun z : ℝ => mu (c*z))
      ((2/(1+c*g r)^3)*c) (g r) := by
    convert! (mu_derivative hd).comp (g r)
      ((hasDerivAt_id (g r)).const_mul c) using 1
    ring
  have hf := exterior_flux_constraint hg hμ hconstant
  have he := response_elasticity hx
  have hA : g r*((2/(1+c*g r)^3)*c) =
      mu (c*g r)*alpha (1/(1+c*g r)) := by
    have hh := (div_eq_iff (ne_of_gt hm)).mp he
    nlinarith [hh]
  have hs := slope_from_flux (ne_of_gt hr) (ne_of_gt hg0) (ne_of_gt hm) hf hA hβ
  apply observable_shape (q := 1/(1+c*g r)) (by positivity) ?_ hs
  unfold mu
  field_simp

/-- The quarter-slope point is unique on the physical branch. -/
theorem quarter_slope_iff {q : ℝ} (hq : 0 ≤ q) :
    slope q = -(1/4) ↔ q=1/2 := by
  have hd : 1+q+2*q^2 ≠ 0 := by positivity
  constructor
  · intro h
    unfold slope at h
    field_simp at h
    have hp : (2*q-1)*(3*q+1)=0 := by nlinarith [h]
    have hpos : 3*q+1 ≠ 0 := by positivity
    have := (mul_eq_zero.mp hp).resolve_right hpos
    linarith
  · intro h
    subst q
    norm_num [slope]

theorem quarter_mass_ratio {q : ℝ} (hq : 0 ≤ q)
    (h : slope q = -(1/4)) : 1/(1-q^2)=(4:ℝ)/3 := by
  rw [(quarter_slope_iff hq).mp h]
  norm_num

/-- Standard epicyclic identity ωr²/Ω²=2+2 beta gives this conditional value. -/
theorem quarter_epicycle : 2+2*(-(1/4 : ℝ))=3/2 := by norm_num

/-- The point-mass circular-orbit law after clearing denominators.
Here b=s/lambda=2a0, w=v². -/
theorem circular_orbit_polynomial {r w b K : ℝ}
    (hr : r ≠ 0) (hd : w+b*r ≠ 0)
    (h : w/r*(1-(b*r/(w+b*r))^2)=K/r^2) :
    r*w^2*(w+2*b*r)=K*(w+b*r)^2 := by
  have hd' : w+r*b ≠ 0 := by simpa [mul_comm] using hd
  field_simp [hr, hd, hd'] at h
  nlinarith [h]

#print axioms mu_derivative
#print axioms response_elasticity
#print axioms observable_root
#print axioms flux_derivative
#print axioms exterior_flux_constraint
#print axioms slope_from_flux
#print axioms slope_elimination
#print axioms observable_shape
#print axioms rational_exterior_shape
#print axioms quarter_slope_iff
#print axioms quarter_mass_ratio
#print axioms quarter_epicycle
#print axioms circular_orbit_polynomial
end
end OrbitalShape
