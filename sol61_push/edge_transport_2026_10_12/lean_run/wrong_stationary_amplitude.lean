import Mathlib

/-! Exact algebra for the conditional edge-transport model. This file does not
formalize stochastic calculus, Fourier analysis, the heat kernel, or astrophysical
applicability. The derivative factors and diffusion convention are specified in
the accompanying analytical report. -/
noncomputable section
namespace EdgeTransport

/-- A scalar boundary shift changes only the zero harmonic in this representation. -/
def shifted (h : ℕ → ℝ) (b : ℝ) (n : ℕ) : ℝ :=
  if n = 0 then h n - b else h n

theorem nonzero_harmonic_unchanged (h : ℕ → ℝ) (b : ℝ) (n : ℕ) (hn : n ≠ 0) :
    shifted h b n = h n := by simp [shifted, hn]

theorem nonzero_spectral_sum_unchanged (s : Finset ℕ) (w h : ℕ → ℝ) (b : ℝ)
    (hs : ∀ n ∈ s, n ≠ 0) :
    ∑ n ∈ s, w n * (shifted h b n) ^ 2 = ∑ n ∈ s, w n * (h n) ^ 2 := by
  apply Finset.sum_congr rfl
  intro n hn
  rw [nonzero_harmonic_unchanged h b n (hs n hn)]

theorem spectral_power_positive (s : Finset ℕ) (w h : ℕ → ℝ)
    (hw : ∀ n ∈ s, 0 ≤ w n)
    (hex : ∃ n ∈ s, 0 < w n ∧ h n ≠ 0) :
    0 < ∑ n ∈ s, w n * (h n) ^ 2 := by
  apply Finset.sum_pos'
  · intro n hn
    exact mul_nonneg (hw n hn) (sq_nonneg (h n))
  · obtain ⟨n, hn, hwp, hhp⟩ := hex
    exact ⟨n, hn, mul_pos hwp (sq_pos_of_ne_zero hhp)⟩

/-- J = (A-D') n - D n'; x = sqrt(q+q0), A=d/2, D=d*x². -/
def current (d x n nprime : ℝ) : ℝ := (d / 2 - d) * n - d * x ^ 2 * nprime

theorem reflecting_profile_zero_current (d x : ℝ) (hx : x ≠ 0) :
    current d x (1 / x) (-1 / (2 * x ^ 3)) = 0 := by
  unfold current
  field_simp [hx]
  ring

/-- General stationary-current family n = B/x - 2J/d. -/
theorem stationary_family_current (d x B J : ℝ) (hd : d ≠ 0) (hx : x ≠ 0) :
    current d x (B / x - 2 * J / d) (-B / (2 * x ^ 3)) = 2 * J := by
  unfold current
  field_simp [hd, hx]
  ring

/-- Within that family, zero flux and an absorbing boundary at s>0 force zero amplitude. -/
theorem absorbing_zero_flux_trivial (B s : ℝ) (hs : s ≠ 0)
    (hboundary : B / s = 0) : B = 0 := by
  exact (div_eq_zero_iff).mp hboundary |>.resolve_right hs

theorem replenished_profile_current (d x C s : ℝ) (hx : x ≠ 0) :
    current d x (C * (1 - s / x)) (C * s / (2 * x ^ 3)) = -d * C / 2 := by
  unfold current
  field_simp [hx]
  ring

theorem replenished_profile_absorbs (C s : ℝ) (hs : s ≠ 0) :
    C * (1 - s / s) = 0 := by rw [div_self hs]; ring

theorem replenished_profile_positive (C s x : ℝ)
    (hC : 0 < C) (hs : 0 < s) (hx : s < x) :
    0 < C * (1 - s / x) := by
  have hxpos : 0 < x := lt_trans hs hx
  exact mul_pos hC (sub_pos.mpr ((div_lt_one hxpos).mpr hx))

theorem replenished_flux_outward (d C : ℝ) (hd : 0 < d) (hC : 0 < C) :
    -d * C / 2 < 0 := by nlinarith [mul_pos hd hC]

/-- Ito drift of x=sqrt(q+q0), conditional on the stated transformation rule. -/
theorem transformed_drift_zero (d x : ℝ) (hx : x ≠ 0) :
    (d / 2) / (2 * x) - (d * x ^ 2) / (4 * x ^ 3) = 0 := by
  field_simp [hx]
  ring

/-- Fokker-Planck diffusion coefficient of x is d/4 (variance rate d/2). -/
theorem transformed_diffusion (d x : ℝ) (hx : x ≠ 0) :
    d * x ^ 2 * (1 / (2 * x)) ^ 2 = d / 4 := by
  field_simp [hx]
  ring

theorem rationalized_distance (q x s : ℝ) (h : x ^ 2 - s ^ 2 = q)
    (hden : x + s ≠ 0) : x - s = q / (x + s) := by
  apply (eq_div_iff hden).mpr
  nlinarith [h]

end EdgeTransport

#print axioms EdgeTransport.nonzero_harmonic_unchanged
#print axioms EdgeTransport.nonzero_spectral_sum_unchanged
#print axioms EdgeTransport.spectral_power_positive
#print axioms EdgeTransport.reflecting_profile_zero_current
#print axioms EdgeTransport.stationary_family_current
#print axioms EdgeTransport.absorbing_zero_flux_trivial
#print axioms EdgeTransport.replenished_profile_current
#print axioms EdgeTransport.replenished_profile_absorbs
#print axioms EdgeTransport.replenished_profile_positive
#print axioms EdgeTransport.replenished_flux_outward
#print axioms EdgeTransport.transformed_drift_zero
#print axioms EdgeTransport.transformed_diffusion
#print axioms EdgeTransport.rationalized_distance
