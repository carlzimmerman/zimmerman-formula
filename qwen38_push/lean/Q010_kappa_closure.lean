import Mathlib

/-!
# Q010: the kappa = 1/2 closure chain — certified algebra (referee spine)

SCOPE (read this). Complements Q001 (constitutive σ_Z² = c_s²) and Q007 (the ½ amplitude
identity) — it does NOT restate them. This file certifies the algebraic spine the Q010
referee re-derives independently (q010_referee.py, frozen criteria 0eb0b4d078):

  * the static log branch Φ = C ln r has Φ' = C/r and Φ'' = −C/r² (L1, L2 — the analytic
    derivative facts GF2 labels "textbook"), and its radial Laplacian is Φ''+2Φ'/r = C/r²
    (L3) — the P2 step: Poisson then FORCES ρ = C/(4πG) r⁻², i.e. γ = 2 (L4);
  * hydrostatics of the forced profile forces σ² = C/2 (L5) — the rung-4 temperature,
    no data;
  * γ = 2 is the UNIQUE self-sourced power-law exponent: the two-point Poisson argument
    (hydrostatic Φ' = γσ²/r sampled at r = 1, 2) gives 2^(−γ) = 1/4, whose unique real
    solution is γ = 2 (L6, via log-injectivity);
  * the germ identity κ = a₀/s = 1/n on the committed tie scale s = n·a₀ (L7);
  * the capacity–dark-energy relation (AG4 T5 + S1 tie): Σ_max = a₀/(πG) with
    a₀ = κc√(Gρ_DE) gives (πGΣ_max)² = (κc)²Gρ_DE — the medium's maximum sheet strength
    is set by the dark-energy density (L8, cleared form);
  * the zero-mode shift invariance (G002 V16): deriv (f + c) = deriv f — slope-based
    quantities (κ, a₀, the RAR shape) are invariant under the constant shift that moves
    the vacuum offset one-for-one (L9);
  * the mutation backbone κ = 1/γ (L10): σ² = C/γ, v_flat² = C ⇒ κ_dyn = 1/γ, reproducing
    GF2's declared γ=2.1 ⇒ κ=0.476 as exact algebra.

PHYSICAL PREMISES NOT CERTIFIED HERE (declared): that the log branch is the committed
static configuration (P1; G081 V1, survives AG1); stationarity + barotropy (P3); the
rung-5 equilibrium identification bridging κ_dyn to κ_germ (carried postulate — the Q010
junction audit records it, this file does not prove it); the empirical tie ρ_DE c² = 4a₀²/G.

Every statement was hand-derived and sympy-prechecked in the same session (J5-pre,
q010_referee.out) before typing; lemma names grep-verified against the cached Mathlib.
-/

noncomputable section

namespace Q010

/-- L1: the log branch derivative — d/dr (C ln r) = C/r for r > 0. -/
theorem L1_log_branch_deriv (C r : ℝ) (hr : 0 < r) :
    HasDerivAt (fun x => C * Real.log x) (C / r) r := by
  have h := (Real.hasDerivAt_log (ne_of_gt hr)).const_mul C
  have hval : C * r⁻¹ = C / r := by field_simp
  rw [← hval]
  exact h

/-- L2: d/dr (C/r) = −C/r² for r > 0 (second derivative of the log branch). -/
theorem L2_inv_deriv (C r : ℝ) (hr : 0 < r) :
    HasDerivAt (fun x => C / x) (-C / r ^ 2) r := by
  have h := (hasDerivAt_const (x := r) C).div (hasDerivAt_id (x := r)) (ne_of_gt hr)
  simp only [id_eq, zero_mul, mul_one, zero_sub] at h
  exact h

/-- L3: the radial Laplacian of the log branch: with Φ' = C/r and Φ'' = −C/r²,
Φ'' + 2Φ'/r = C/r². (P2's algebra step; the derivative facts are L1/L2.) -/
theorem L3_laplacian_log (C r ph1 ph2 : ℝ) (hr : r ≠ 0) (h1 : ph1 = C / r)
    (h2 : ph2 = -C / r ^ 2) : ph2 + 2 * ph1 / r = C / r ^ 2 := by
  rw [h1, h2]
  field_simp
  ring

/-- L4: Poisson coefficient identity — 4πG·A = C iff A = C/(4πG) (γ = 2 case of
∇²Φ = 4πGρ with ρ = A/r²: the log branch sources EXACTLY the r⁻² profile). -/
theorem L4_poisson_coefficient (C A G4 : ℝ) (hG : G4 ≠ 0) : G4 * A = C ↔ A = C / G4 := by
  constructor
  · intro h
    field_simp [hG]
    ring_nf at h ⊢
    linarith
  · intro h
    rw [h]
    field_simp [hG]

/-- L5: hydrostatic forcing — the isothermal hydrostatic balance of the r⁻² profile,
σ²·(2A) = A·C (i.e. σ²ρ'/ρ = −Φ' cleared), forces σ² = C/2. The rung-4 temperature,
no data input. -/
theorem L5_hydrostatic_forcing (σ2 C A : ℝ) (hA : A ≠ 0) (h : σ2 * (2 * A) = A * C) :
    σ2 = C / 2 := by
  have h' : 2 * σ2 = C := by
    apply mul_right_cancel₀ hA
    ring_nf at h ⊢
    linarith
  field_simp
  linarith

/-- L6: two-point uniqueness of the self-sourced exponent. Hydrostatics gives Φ' = γσ²/r;
Poisson (r²Φ')' = 4πGAr^(−γ) evaluated at r = 1 and r = 2 (D := 4πGA) gives
γσ² = D and γσ²/4 = D·2^(−γ), hence 2^(−γ) = 1/4, whose unique real solution is γ = 2
(base-2 exponential injective via log). -/
theorem L6_two_point_uniqueness (γ σ2 D : ℝ) (hD : D ≠ 0) (hσ : 0 < σ2)
    (h1 : γ * σ2 = D) (h2 : γ * σ2 / 4 = D * (2:ℝ) ^ (-γ)) : γ = 2 := by
  have hγ : γ ≠ 0 := by
    intro hg
    rw [hg, zero_mul] at h1
    exact hD h1.symm
  have hne : γ * σ2 ≠ 0 := mul_ne_zero hγ (ne_of_gt hσ)
  have h2' : γ * σ2 / 4 = γ * σ2 * (2:ℝ) ^ (-γ) := by
    rw [← h1] at h2
    exact h2
  have h3 : (2:ℝ) ^ (-γ) = 1 / 4 := by
    apply (mul_right_inj' hne).1
    have hq : γ * σ2 * (1 / 4) = γ * σ2 / 4 := by ring
    linarith
  have hpos2 : (0:ℝ) < 2 := by norm_num
  have h4 : -γ * Real.log 2 = Real.log ((1:ℝ) / 4) := by
    have hl := congrArg Real.log h3
    rwa [Real.log_rpow hpos2] at hl
  have hlog4 : Real.log ((1:ℝ) / 4) = -(2 * Real.log 2) := by
    have hn1 : (1:ℝ) ≠ 0 := by norm_num
    have hn4 : (4:ℝ) ≠ 0 := by norm_num
    have hn2 : (2:ℝ) ≠ 0 := by norm_num
    rw [Real.log_div hn1 hn4, Real.log_one, zero_sub]
    have h44 : (4:ℝ) = 2 * 2 := by norm_num
    rw [h44, Real.log_mul hn2 hn2]
    ring
  rw [hlog4] at h4
  have h5 : γ * Real.log 2 - 2 * Real.log 2 = 0 := by linarith
  have hL : Real.log 2 ≠ 0 := ne_of_gt (Real.log_pos (by norm_num : (1:ℝ) < 2))
  have h6 : (γ - 2) * Real.log 2 = 0 := by
    have hf : (γ - 2) * Real.log 2 = γ * Real.log 2 - 2 * Real.log 2 := by ring
    linarith [hf, h5]
  rcases mul_eq_zero.mp h6 with hz | hz
  · exact sub_eq_zero.mp hz
  · exact absurd hz hL

/-- L7: germ identity — on the committed tie scale s = n·a₀, κ_germ = a₀/s = 1/n. -/
theorem L7_germ_identity (a0 s n : ℝ) (hn : n ≠ 0) (ha : a0 ≠ 0) (hs : s = n * a0) :
    a0 / s = 1 / n := by
  rw [hs]
  field_simp

/-- L8: capacity–dark-energy relation (cleared form). With the S1 tie a₀ = κc√(Gρ_DE)
and the AG4 capacity sheet πGΣ_max = a₀: (πGΣ_max)² = (κc)²·Gρ_DE. The medium's maximum
sheet strength is set by the dark-energy density. -/
theorem L8_capacity_DE (a0 κ c G ρ Smax : ℝ) (hpos : 0 ≤ G * ρ)
    (htie : a0 = κ * c * Real.sqrt (G * ρ)) (hcap : Real.pi * G * Smax = a0) :
    (Real.pi * G * Smax) ^ 2 = (κ * c) ^ 2 * (G * ρ) := by
  rw [hcap, htie]
  have hs : Real.sqrt (G * ρ) ^ 2 = G * ρ := Real.sq_sqrt hpos
  ring_nf
  rw [hs]
  ring

/-- L9: zero-mode shift invariance (G002 V16 algebra): deriv (f + c) = deriv f — every
slope-based quantity (κ = 1/slope, a₀ = s/n, the RAR shape) is invariant under the
constant shift that moves the vacuum offset one-for-one. -/
theorem L9_shift_invariance (f : ℝ → ℝ) (c x : ℝ) :
    deriv (fun y => f y + c) x = deriv f x := by
  rw [deriv_add_const']

/-- L10: the mutation backbone κ = 1/γ: with σ² = C/γ and v_flat² = C (any self-similar
power-law attempt), κ_dyn = σ²/v_flat² = 1/γ — at γ = 2 this is ½; at γ = 2.1 it is
GF2's registered MUTATE value 0.476 (2.38% off ½). -/
theorem L10_kappa_of_gamma (σ2 C γ v2 : ℝ) (hC : C ≠ 0) (hγ : γ ≠ 0)
    (hσ : σ2 = C / γ) (hv : v2 = C) : σ2 / v2 = 1 / γ := by
  rw [hσ, hv]
  field_simp

end Q010

end noncomputable section

#print axioms Q010.L1_log_branch_deriv
#print axioms Q010.L2_inv_deriv
#print axioms Q010.L3_laplacian_log
#print axioms Q010.L4_poisson_coefficient
#print axioms Q010.L5_hydrostatic_forcing
#print axioms Q010.L6_two_point_uniqueness
#print axioms Q010.L7_germ_identity
#print axioms Q010.L8_capacity_DE
#print axioms Q010.L9_shift_invariance
#print axioms Q010.L10_kappa_of_gamma
