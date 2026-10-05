import Mathlib

/-!
# PUZZLE_32pi_chain_2026_10_05_MUTATE (three false variants; this file MUST fail) -- the 2026-10-04/05 reductions of "A Lambda = 32 pi^2" (c = G = 1), certified

Sources: sonnet55_push/puzzle_32pi/p17-p25 (sympy). Premises are named hypotheses; no `axiom` declarations.

* `sds_horizon_identity`   : at a root of f = 1 - 2M/r - Lambda r^2/3 with kappa = f'(r)/2:  1 - 2 kappa r = Lambda r^2   (p12, B3, p20).
* `no_sds_horizon_is_puzzle` : hence no such horizon has kappa r = 1/2 and Lambda r^2 = 8 pi.
* `escape_condition_value` : the 'vacuum ball is its own black hole' condition gives rho r^2 = 3/(8 pi), which is < 1 (p17: seven conditions agree on it).
* `heaviside_form`         : with G_H = 4 pi G, G rho r^2 = 1 <-> G_H rho r^2 = 4 pi (p18).
* `flux_form`              : Lambda (4 pi r^2) = 32 pi^2 <-> (Lambda/(8 pi)) (4 pi r^2) = 4 pi, the Gauss-Bonnet total of the horizon sphere (p19).
* `acoustic_ds_superluminal` : the cosmological sound horizon r = c_s/H with Lambda = 3H^2 meets Lambda r^2 = 8 pi only if c_s^2 = 8 pi/3 > 1 (p20a).
* `bimond_vacuum_condition` : Lambda = (1/2)(1 + f'(1)) a0^2 I  (Milgrom eq 24 with M(0) = -I)  ->  Lambda = 32 pi a0^2 <-> (1 + f'(1)) I = 64 pi (p21).
* `exchange_symmetry_pins_fprime` : f differentiable at 1 with f(k) = f(1/k) near 1  ->  f'(1) = 0 (p24).
* `symmetric_map` : (1 - m)/(1 - 2m) = nu <-> m = (nu - 1)/(2 nu - 1) (p25).
* `class_identity_integrand` : the alpha = beta vacuum integrand minus the alpha + beta = 0 integrand is d/dy[2 y^2 (nu - 1)^2] (p25).
NOT certified: any physical reason for kappa = 1/2, the numerical integrals, or the BIMOND field equations themselves (taken from the paper).
-/

open Real

/-- At a horizon of the SdS-type function f(r) = 1 - 2M/r - Lambda r^2/3, with kappa = f'(r)/2. -/
theorem sds_horizon_identity {M Λ r κ : ℝ} (hr : 0 < r)
    (hf : 1 - 2 * M / r - Λ * r ^ 2 / 3 = 0)
    (hk : κ = (2 * M / r ^ 2 - 2 * Λ * r / 3) / 2) :
    1 - 2 * κ * r = Λ * r ^ 2 := by
  have hr0 : r ≠ 0 := hr.ne'
  have hM : 2 * M = r * (1 - Λ * r ^ 2 / 3) := by
    field_simp at hf; nlinarith [hf]
  subst hk
  field_simp
  nlinarith [hM]

theorem no_sds_horizon_is_puzzle {M Λ r κ : ℝ} (hr : 0 < r)
    (hf : 1 - 2 * M / r - Λ * r ^ 2 / 3 = 0)
    (hk : κ = (2 * M / r ^ 2 - 2 * Λ * r / 3) / 2) :
    ¬ (κ * r = 1 / 2 ∧ Λ * r ^ 2 = 0) := by
  rintro ⟨h1, h2⟩
  have hid := sds_horizon_identity hr hf hk
  have hp := Real.pi_pos
  nlinarith [hid, h1, h2]

theorem escape_condition_value {ρ r : ℝ} (hr : 0 < r)
    (h : 2 * ((4 * π / 3) * ρ * r ^ 3) / r = 1) : ρ * r ^ 2 = 3 / (8 * π) ∧ ρ * r ^ 2 < 1 := by
  have hp := Real.pi_gt_three
  have hr0 : r ≠ 0 := hr.ne'
  have e : ρ * r ^ 2 = 3 / (8 * π) := by
    field_simp at h ⊢; nlinarith [h]
  refine ⟨e, ?_⟩
  rw [e, div_lt_one (by positivity)]; linarith

theorem heaviside_form {G ρ r : ℝ} : G * ρ * r ^ 2 = 1 ↔ (4 * π * G) * ρ * r ^ 2 = 4 * π := by
  have hp := Real.pi_pos
  constructor
  · intro h; calc (4 * π * G) * ρ * r ^ 2 = 4 * π * (G * ρ * r ^ 2) := by ring
      _ = 4 * π := by rw [h]; ring
  · intro h
    have : 4 * π * (G * ρ * r ^ 2) = 4 * π * 1 := by linarith [h]
    exact mul_left_cancel₀ (by positivity) this

theorem flux_form {Λ r : ℝ} : Λ * (4 * π * r ^ 2) = 32 * π ^ 2 ↔ (Λ / (8 * π)) * (4 * π * r ^ 2) = 4 * π := by
  have hp := Real.pi_pos
  have h8 : (8 * π) ≠ 0 := by positivity
  constructor
  · intro h; field_simp; nlinarith [h]
  · intro h; field_simp at h; nlinarith [h]

theorem acoustic_ds_superluminal {H cs Λ : ℝ} (hH : 0 < H) (hΛ : Λ = 3 * H ^ 2)
    (h : Λ * (cs / H) ^ 2 = 8 * π) : cs ^ 2 = 8 * π / 3 ∧ 1 < cs ^ 2 := by
  have hp := Real.pi_gt_three
  have hH0 : H ≠ 0 := hH.ne'
  have e : cs ^ 2 = 8 * π / 3 := by
    rw [hΛ] at h; field_simp at h; nlinarith [h]
  exact ⟨e, by rw [e]; linarith⟩

theorem bimond_vacuum_condition {a0 fp I Λ : ℝ} (ha : 0 < a0)
    (hΛ : Λ = (1 / 2) * (1 + fp) * a0 ^ 2 * I) :
    Λ = 32 * π * a0 ^ 2 ↔ (1 + fp) * I = 32 * π := by
  have h2 : a0 ^ 2 ≠ 0 := by positivity
  rw [hΛ]
  constructor
  · intro h
    have : a0 ^ 2 * ((1 + fp) * I) = a0 ^ 2 * (64 * π) := by linarith [h]
    exact mul_left_cancel₀ h2 this
  · intro h
    calc (1 / 2) * (1 + fp) * a0 ^ 2 * I = (1 / 2) * a0 ^ 2 * ((1 + fp) * I) := by ring
      _ = 32 * π * a0 ^ 2 := by rw [h]; ring

theorem exchange_symmetry_pins_fprime {f : ℝ → ℝ} {d : ℝ} (hd : HasDerivAt f d 1)
    (hsym : ∀ k : ℝ, 0 < k → f k = f k⁻¹) : d = 0 := by
  -- g(k) = f(1/k) has derivative d * (-1) at 1, and g = f on a neighbourhood of 1
  have hinv : HasDerivAt (fun k : ℝ => k⁻¹) (-(1 : ℝ) ^ 2)⁻¹ 1 := by
    have := hasDerivAt_inv (x := (1 : ℝ)) one_ne_zero
    simpa using this
  have hcomp : HasDerivAt (fun k : ℝ => f k⁻¹) (d * (-(1 : ℝ) ^ 2)⁻¹) 1 := by
    have hd' : HasDerivAt f d ((fun k : ℝ => k⁻¹) 1) := by simpa using hd
    exact hd'.comp 1 hinv
  have heq : (fun k : ℝ => f k⁻¹) =ᶠ[nhds 1] f := by
    filter_upwards [lt_mem_nhds (show (0 : ℝ) < 1 by norm_num)] with k hk
    exact (hsym k hk).symm
  have h2 : HasDerivAt f (d * (-(1 : ℝ) ^ 2)⁻¹) 1 := hcomp.congr_of_eventuallyEq heq.symm
  have := hd.unique h2
  norm_num at this
  linarith

theorem symmetric_map {m ν : ℝ} (hm : 1 - 2 * m ≠ 0) (hν : 2 * ν - 1 ≠ 0) :
    (1 - m) / (1 - 2 * m) = ν ↔ m = (ν - 1) / (2 * ν) := by
  constructor
  · intro h
    rw [div_eq_iff hm] at h
    rw [eq_div_iff hν]
    linarith
  · intro h
    rw [div_eq_iff hm, h]
    have k : (ν - 1) / (2 * ν - 1) * (2 * ν - 1) = ν - 1 := div_mul_cancel₀ _ hν
    have e1 : 1 - (ν - 1) / (2 * ν - 1) = ν * (1 - 2 * ((ν - 1) / (2 * ν - 1))) ↔
        (1 - (ν - 1) / (2 * ν - 1)) * (2 * ν - 1) = ν * (1 - 2 * ((ν - 1) / (2 * ν - 1))) * (2 * ν - 1) := by
      constructor
      · intro hh; rw [hh]
      · intro hh; exact mul_right_cancel₀ hν hh
    rw [e1]
    have l : (1 - (ν - 1) / (2 * ν - 1)) * (2 * ν - 1) = (2 * ν - 1) - (ν - 1) / (2 * ν - 1) * (2 * ν - 1) := by ring
    have r : ν * (1 - 2 * ((ν - 1) / (2 * ν - 1))) * (2 * ν - 1) = ν * ((2 * ν - 1) - 2 * ((ν - 1) / (2 * ν - 1) * (2 * ν - 1))) := by ring
    rw [l, r, k]; ring

/-- Integrand identity (nu' = derivative of nu at y): m dz/dy - (nu - 1) d(y^2)/dy = d/dy [2 y^2 (nu - 1)^2], with m = (nu-1)/(2nu-1), z = y^2 (2nu-1)^2. -/
theorem class_identity_integrand {y ν ν' : ℝ} (hw : 2 * ν - 1 ≠ 0) :
    (ν - 1) / (2 * ν - 1) * (2 * y * (2 * ν - 1) ^ 2 + y ^ 2 * (2 * (2 * ν - 1) * (2 * ν'))) - (ν - 1) * (2 * y)
      = 4 * y * (ν - 1) ^ 2 + 2 * y ^ 2 * (2 * (ν - 1) * ν') := by
  have k : (ν - 1) / (2 * ν - 1) * (2 * ν - 1) = ν - 1 := div_mul_cancel₀ _ hw
  calc (ν - 1) / (2 * ν - 1) * (2 * y * (2 * ν - 1) ^ 2 + y ^ 2 * (2 * (2 * ν - 1) * (2 * ν'))) - (ν - 1) * (2 * y)
      = ((ν - 1) / (2 * ν - 1) * (2 * ν - 1)) * (2 * y * (2 * ν - 1) + 4 * y ^ 2 * ν') - (ν - 1) * (2 * y) := by ring
    _ = (ν - 1) * (2 * y * (2 * ν - 1) + 4 * y ^ 2 * ν') - (ν - 1) * (2 * y) := by rw [k]
    _ = 4 * y * (ν - 1) ^ 2 + 2 * y ^ 2 * (2 * (ν - 1) * ν') := by ring

-- axiom audit (must list only propext, Classical.choice, Quot.sound)
#print axioms no_sds_horizon_is_puzzle
#print axioms escape_condition_value
#print axioms heaviside_form
#print axioms flux_form
#print axioms acoustic_ds_superluminal
#print axioms bimond_vacuum_condition
#print axioms exchange_symmetry_pins_fprime
#print axioms symmetric_map
#print axioms class_identity_integrand
