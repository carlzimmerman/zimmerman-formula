import Mathlib

/-!
Conditional mathematical certificates for the gravity architecture, 2026-10-12.
All variables are real unless otherwise specified. Physical laws are explicit
hypotheses or definitions, never extra axioms. This file does not formalize GR,
the empirical likelihoods, microscopic field theory, or a halo-selection mechanism.
The deep law is exact only within the idealized deep-regime model defined here.
-/

noncomputable section
namespace GravityArchitecture

/-- Proposed scale, with mass-equivalent dark-energy density. -/
def accelerationScale (κ c G ρ : ℝ) : ℝ := κ * c * Real.sqrt (G * ρ)

theorem scale_squared (κ c G ρ : ℝ) (h : 0 ≤ G * ρ) :
    accelerationScale κ c G ρ ^ 2 = κ ^ 2 * c ^ 2 * G * ρ := by
  unfold accelerationScale
  rw [mul_pow, mul_pow, Real.sq_sqrt h]
  ring

/-- The coefficient is conditional on the chosen κ and vacuum relation. -/
theorem vacuum_coefficient (κ c G ρ Λ : ℝ) (hc : c ≠ 0)
    (hρ : 0 ≤ G * ρ) (hΛ : Λ = 8 * Real.pi * G * ρ / c ^ 2) :
    accelerationScale κ c G ρ ^ 2 = κ ^ 2 * Λ * c ^ 4 / (8 * Real.pi) := by
  rw [scale_squared κ c G ρ hρ, hΛ]
  field_simp [hc, Real.pi_ne_zero]

theorem half_kappa_32pi (c G ρ Λ : ℝ) (hc : c ≠ 0)
    (hρ : 0 ≤ G * ρ) (hΛ : Λ = 8 * Real.pi * G * ρ / c ^ 2) :
    accelerationScale (1 / 2) c G ρ ^ 2 = Λ * c ^ 4 / (16 * Real.pi) := by
  rw [vacuum_coefficient (1 / 2) c G ρ Λ hc hρ hΛ]
  ring

/-- The scale definition alone admits every real κ, including positive alternatives. -/
theorem coefficient_family (κ c G ρ : ℝ) (h : 0 ≤ G * ρ) :
    ∃ a₀ : ℝ, a₀ = accelerationScale κ c G ρ ∧
      a₀ ^ 2 = κ ^ 2 * c ^ 2 * G * ρ := by
  exact ⟨accelerationScale κ c G ρ, rfl, scale_squared κ c G ρ h⟩

def baryonAcceleration (G M r : ℝ) : ℝ := G * M / r ^ 2
def deepAcceleration (G M a₀ r : ℝ) : ℝ :=
  Real.sqrt (a₀ * baryonAcceleration G M r)

/-- Circular orbit equation plus the deep law implies the quartic relation. -/
theorem baryonic_quartic (G M a₀ r V : ℝ)
    (hG : 0 < G) (hM : 0 ≤ M) (ha : 0 ≤ a₀) (hr : 0 < r)
    (horbit : V ^ 2 / r = deepAcceleration G M a₀ r) :
    V ^ 4 = G * M * a₀ := by
  have hnonneg : 0 ≤ a₀ * baryonAcceleration G M r := by
    unfold baryonAcceleration
    positivity
  have hs := Real.sq_sqrt hnonneg
  have hv : V ^ 2 = deepAcceleration G M a₀ r * r :=
    (div_eq_iff (ne_of_gt hr)).mp horbit
  unfold deepAcceleration at hv
  calc
    V ^ 4 = (Real.sqrt (a₀ * baryonAcceleration G M r)) ^ 2 * r ^ 2 := by
      nlinarith [sq_nonneg (V ^ 2 - Real.sqrt (a₀ * baryonAcceleration G M r) * r),
        congrArg (fun x : ℝ => x ^ 2) hv]
    _ = a₀ * baryonAcceleration G M r * r ^ 2 := by rw [hs]
    _ = G * M * a₀ := by
      unfold baryonAcceleration
      field_simp [ne_of_gt hr]

/-- At each radius, a real-mass realization fixes the required extra enclosed mass. -/
theorem target_mass_unique (G Mb Mc r ν : ℝ) (hG : G ≠ 0) (hr : r ≠ 0)
    (hforce : G * (Mb + Mc) / r ^ 2 = ν * (G * Mb / r ^ 2)) :
    Mc = (ν - 1) * Mb := by
  have h := hforce
  field_simp [hr, hG] at h
  nlinarith [h]

theorem target_mass_sufficient (G Mb r ν : ℝ) :
    G * (Mb + (ν - 1) * Mb) / r ^ 2 = ν * (G * Mb / r ^ 2) := by
  ring

/-- Negative targets cannot be interpreted as nonnegative real enclosed cold mass. -/
theorem target_mass_nonnegative_iff (Mb ν : ℝ) (hM : 0 < Mb) :
    0 ≤ (ν - 1) * Mb ↔ 1 ≤ ν := by
  constructor
  · intro h
    nlinarith
  · intro h
    exact mul_nonneg (sub_nonneg.mpr h) (le_of_lt hM)

/-- A compact source's ideal deep-law tail: Mc(r) = A r - Mb. -/
def tailColdMass (A Mb r : ℝ) : ℝ := A * r - Mb

theorem tail_mass_derivative (A Mb r : ℝ) :
    HasDerivAt (tailColdMass A Mb) A r := by
  change HasDerivAt (fun x : ℝ => A * x - Mb) A r
  have hid : HasDerivAt (fun x : ℝ => x) 1 r := hasDerivAt_id r
  have hmul : HasDerivAt (fun x : ℝ => A * x) A r := by
    simpa only [mul_one] using hid.const_mul A
  exact hmul.sub_const Mb

/-- Spherical density reconstruction, with its geometric relation explicit. -/
theorem tail_density (A Mb r ρ : ℝ) (hr : r ≠ 0)
    (hmass : 4 * Real.pi * r ^ 2 * ρ = deriv (tailColdMass A Mb) r) :
    ρ = A / (4 * Real.pi * r ^ 2) := by
  rw [(tail_mass_derivative A Mb r).deriv] at hmass
  apply (eq_div_iff (by positivity : (4 : ℝ) * Real.pi * r ^ 2 ≠ 0)).mpr
  nlinarith [hmass]

/-- Supply bounds the radius of the idealized tail; no infinite halo is permitted. -/
theorem supply_radius_bound (A Mb S r : ℝ) (hA : 0 < A)
    (hsupply : tailColdMass A Mb r ≤ S) :
    r ≤ (S + Mb) / A := by
  apply (le_div_iff₀ hA).mpr
  unfold tailColdMass at hsupply
  nlinarith

theorem no_finite_supply_for_infinite_tail (A Mb S : ℝ) (hA : 0 < A) :
    ¬ (∀ r : ℝ, 0 < r → tailColdMass A Mb r ≤ S) := by
  intro h
  let r := max ((S + Mb) / A) 0 + 1
  have hr : 0 < r := by dsimp [r]; have := le_max_right ((S + Mb) / A) 0; linarith
  have hu := supply_radius_bound A Mb S r hA (h r hr)
  have hl := le_max_left ((S + Mb) / A) 0
  dsimp [r] at hu
  linarith

/-- Algebra for the tested non-lensing additive-force prescription, not a data verdict. -/
theorem nonlensing_residual (gb gc gs gd gl : ℝ)
    (hd : gd = gb + gc + gs) (hl : gl = gb + gc) :
    gd - gl = gs := by linarith

theorem matched_lensing_forces_zero_extra (gb gc gs gd gl : ℝ)
    (hd : gd = gb + gc + gs) (hl : gl = gb + gc) (hm : gd = gl) :
    gs = 0 := by linarith

/-- Componentwise exchange cancellation; no tensor calculus is asserted here. -/
theorem exchange_conserves_total {ι : Type*} (Dc Dr Q : ι → ℝ)
    (hc : ∀ i, Dc i = Q i) (hr : ∀ i, Dr i = -Q i) :
    ∀ i, Dc i + Dr i = 0 := by
  intro i
  rw [hc i, hr i]
  ring

/-- Once zero vacuum divergence is supplied, a constant vacuum cannot receive nonzero Q. -/
theorem passive_vacuum_no_exchange {ι : Type*} (Dv Q : ι → ℝ)
    (hzero : ∀ i, Dv i = 0) (hexchange : ∀ i, Dv i = -Q i) :
    ∀ i, Q i = 0 := by
  intro i
  have hz := hzero i
  have he := hexchange i
  linarith

/-- An idealized response energy is nonnegative; not a full gravitational stability proof. -/
theorem response_energy_nonnegative (C β mismatchSq p : ℝ)
    (hC : 0 ≤ C) (hβ : 0 ≤ β) (hm : 0 ≤ mismatchSq) (hp : 0 ≤ p) :
    0 ≤ C / 2 * mismatchSq + β / 3 * p ^ 3 := by positivity

/-- A universal quadratic-in-mass law cannot equal a positive linear-in-mass law
at two distinct positive masses. This tests the two asymptotic models only. -/
theorem distinct_mass_scalings (K L M₁ M₂ : ℝ) (hK : 0 < K)
    (hM₁ : 0 < M₁) (hM₂ : 0 < M₂) (hne : M₁ ≠ M₂)
    (h₁ : K * M₁ = L * M₁ ^ 2) :
    K * M₂ ≠ L * M₂ ^ 2 := by
  intro h₂
  have hf₁ : M₁ * (K - L * M₁) = 0 := by nlinarith [h₁]
  have hf₂ : M₂ * (K - L * M₂) = 0 := by nlinarith [h₂]
  have he₁ := (mul_eq_zero.mp hf₁).resolve_left (ne_of_gt hM₁)
  have he₂ := (mul_eq_zero.mp hf₂).resolve_left (ne_of_gt hM₂)
  have hL : L ≠ 0 := by intro hz; rw [hz] at he₁; nlinarith
  have hf : L * (M₁ - M₂) = 0 := by nlinarith
  have he := (mul_eq_zero.mp hf).resolve_left hL
  exact hne (by linarith)

end GravityArchitecture

#print axioms GravityArchitecture.scale_squared
#print axioms GravityArchitecture.vacuum_coefficient
#print axioms GravityArchitecture.half_kappa_32pi
#print axioms GravityArchitecture.coefficient_family
#print axioms GravityArchitecture.baryonic_quartic
#print axioms GravityArchitecture.target_mass_unique
#print axioms GravityArchitecture.target_mass_sufficient
#print axioms GravityArchitecture.target_mass_nonnegative_iff
#print axioms GravityArchitecture.tail_mass_derivative
#print axioms GravityArchitecture.tail_density
#print axioms GravityArchitecture.supply_radius_bound
#print axioms GravityArchitecture.no_finite_supply_for_infinite_tail
#print axioms GravityArchitecture.nonlensing_residual
#print axioms GravityArchitecture.matched_lensing_forces_zero_extra
#print axioms GravityArchitecture.exchange_conserves_total
#print axioms GravityArchitecture.passive_vacuum_no_exchange
#print axioms GravityArchitecture.response_energy_nonnegative
#print axioms GravityArchitecture.distinct_mass_scalings
