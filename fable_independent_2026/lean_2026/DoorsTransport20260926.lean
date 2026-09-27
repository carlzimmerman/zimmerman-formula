import Mathlib

/-!
# Same-clock transport: exact scoped certificates (2026-09-26)

This file certifies real moment algebra and the explicit one-dimensional
Chaplygin-limit solution X(m,t)=m-M sin(m) sin(t), with mass-coordinate
Jacobian tau=1-M cos(m) sin(t). Positive tau is an INPUT to the fluid
interpretation rho=1/tau; after tau reaches zero the continued wave map is
not a positive-density single-valued fluid solution.

The accompanying transport computation derives this limit and the finite-eta
bounded-DBI equation from the single canonical clock pair (Theta,rho). Lean
does not certify that action reduction, numerical trajectories, a covariant
completion, or a universal obstruction to gradient-dependent/dispersive fields.
The moment obstruction concerns a LOCAL barotropic stress determined only by
density/current. It does not exclude spatially oscillatory weak limits.
-/

namespace DoorsTransport20260926

theorem two_stream_moment_identity (a b va vb : ℝ) :
    (a + b) * (a * va ^ 2 + b * vb ^ 2) - (a * va + b * vb) ^ 2 =
      a * b * (va - vb) ^ 2 := by ring

theorem distinct_streams_have_positive_variance (a b va vb : ℝ)
    (ha : 0 < a) (hb : 0 < b) (hv : va ≠ vb) :
    0 < (a + b) * (a * va ^ 2 + b * vb ^ 2) - (a * va + b * vb) ^ 2 := by
  rw [two_stream_moment_identity]
  exact mul_pos (mul_pos ha hb) (sq_pos_of_ne_zero (sub_ne_zero.mpr hv))

theorem counterstreams_share_density_current (V : ℝ) :
    (1 / 2 : ℝ) + 1 / 2 = 1 ∧
      (1 / 2 : ℝ) * V + (1 / 2 : ℝ) * (-V) = 0 ∧
      (1 / 2 : ℝ) * V ^ 2 + (1 / 2 : ℝ) * (-V) ^ 2 = V ^ 2 := by
  constructor
  · norm_num
  constructor <;> ring

theorem no_density_only_pressure_matches_both (P : ℝ → ℝ) :
    ¬ (P 1 = (1 : ℝ) ^ 2 ∧ P 1 = (2 : ℝ) ^ 2) := by
  rintro ⟨h1, h2⟩
  norm_num at h1 h2
  linarith

noncomputable def position (M m t : ℝ) : ℝ := m - M * Real.sin m * Real.sin t
noncomputable def velocity (M m t : ℝ) : ℝ := -M * Real.sin m * Real.cos t
noncomputable def jacobian (M m t : ℝ) : ℝ := 1 - M * Real.cos m * Real.sin t

theorem position_time_derivative (M m t : ℝ) :
    HasDerivAt (fun t => position M m t) (velocity M m t) t := by
  have h := ((Real.hasDerivAt_sin t).const_mul (M * Real.sin m)).const_sub m
  convert! h using 1
  simp [velocity]

theorem position_mass_derivative (M m t : ℝ) :
    HasDerivAt (fun m => position M m t) (jacobian M m t) m := by
  have h := (hasDerivAt_id m).sub ((Real.hasDerivAt_sin m).const_mul (M * Real.sin t))
  have hf : (fun m => position M m t) = (fun m : ℝ => m - (M * Real.sin t) * Real.sin m) := by
    funext m
    simp [position]
    ring
  rw [hf]
  convert! h using 1
  simp [jacobian]
  ring

theorem velocity_time_derivative (M m t : ℝ) :
    HasDerivAt (fun t => velocity M m t) (M * Real.sin m * Real.sin t) t := by
  convert! (Real.hasDerivAt_cos t).const_mul (-M * Real.sin m) using 1
  simp

theorem jacobian_mass_derivative (M m t : ℝ) :
    HasDerivAt (fun m => jacobian M m t) (M * Real.sin m * Real.sin t) m := by
  have h := ((Real.hasDerivAt_cos m).const_mul (M * Real.sin t)).const_sub 1
  have hf : (fun m => jacobian M m t) = (fun m : ℝ => 1 - (M * Real.sin t) * Real.cos m) := by
    funext m
    simp [jacobian]
    ring
  rw [hf]
  convert! h using 1
  ring

theorem mass_wave_equation (M m t : ℝ) :
    deriv (fun t => velocity M m t) t = deriv (fun m => jacobian M m t) m := by
  rw [(velocity_time_derivative M m t).deriv, (jacobian_mass_derivative M m t).deriv]

theorem subcritical_jacobian_positive (M m t : ℝ) (hM : 0 ≤ M) (hsub : M < 1) :
    0 < jacobian M m t := by
  have habs : |Real.cos m * Real.sin t| ≤ 1 := by
    rw [abs_mul]
    nlinarith [Real.abs_cos_le_one m, Real.abs_sin_le_one t,
      abs_nonneg (Real.cos m), abs_nonneg (Real.sin t)]
  have hbound : Real.cos m * Real.sin t ≤ 1 := le_trans (le_abs_self _) habs
  have hproduct := mul_le_mul_of_nonneg_left hbound hM
  unfold jacobian
  nlinarith

theorem supercritical_jacobian_zero (M : ℝ) (hM : 1 < M) :
    jacobian M 0 (Real.arcsin (1 / M)) = 0 := by
  have hpos : 0 < M := by linarith
  have hlo : -(1 : ℝ) ≤ 1 / M := by
    have hquot : 0 < 1 / M := one_div_pos.mpr hpos
    linarith
  have hhi : 1 / M ≤ 1 := by rw [div_le_iff₀ hpos]; linarith
  simp only [jacobian, Real.cos_zero, mul_one, Real.sin_arcsin hlo hhi]
  field_simp
  norm_num

theorem positive_initial_jacobian (M m : ℝ) : jacobian M m 0 = 1 := by
  simp [jacobian]

theorem half_period_rebound (M m : ℝ) :
    position M m Real.pi = m ∧ velocity M m Real.pi = M * Real.sin m := by
  simp [position, velocity]

/-- The polar gradient identity is local; it does not extend a phase through a zero. -/
theorem polar_gradient_norm (rp w theta : ℝ) :
    (rp * Real.cos theta - w * Real.sin theta) ^ 2 +
      (rp * Real.sin theta + w * Real.cos theta) ^ 2 = rp ^ 2 + w ^ 2 := by
  calc
    _ = (rp ^ 2 + w ^ 2) * (Real.sin theta ^ 2 + Real.cos theta ^ 2) := by ring
    _ = rp ^ 2 + w ^ 2 := by rw [Real.sin_sq_add_cos_sq, mul_one]

theorem fisher_gradient_energy (r rp vx D : ℝ) (hr : r ≠ 0) (hD : D ≠ 0) :
    D ^ 2 / 2 * (rp ^ 2 + (r * vx / D) ^ 2) =
      r ^ 2 * vx ^ 2 / 2 + D ^ 2 * (2 * r * rp) ^ 2 / (8 * r ^ 2) := by
  field_simp
  ring

theorem polar_canonical_jacobian (r D theta : ℝ) (hr : r ≠ 0) (hD : D ≠ 0) :
    (Real.cos theta / (2 * r)) * (r * Real.cos theta / D) -
      (-r * Real.sin theta / D) * (Real.sin theta / (2 * r)) = 1 / (2 * D) := by
  calc
    _ = (Real.cos theta ^ 2 + Real.sin theta ^ 2) / (2 * D) := by field_simp; ring
    _ = 1 / (2 * D) := by rw [add_comm, Real.sin_sq_add_cos_sq]

theorem counterwave_peak_velocity (A B q : ℝ) (hne : A ≠ B) :
    q * (A ^ 2 - B ^ 2) / (A - B) ^ 2 = q * (A + B) / (A - B) := by
  have hd : A - B ≠ 0 := sub_ne_zero.mpr hne
  field_simp
  ring

theorem balanced_counterwave_node (A : ℝ) : A ^ 2 + A ^ 2 + 2 * A * A * (-1) = 0 := by
  ring

#print axioms two_stream_moment_identity
#print axioms distinct_streams_have_positive_variance
#print axioms counterstreams_share_density_current
#print axioms no_density_only_pressure_matches_both
#print axioms position_time_derivative
#print axioms position_mass_derivative
#print axioms velocity_time_derivative
#print axioms jacobian_mass_derivative
#print axioms mass_wave_equation
#print axioms subcritical_jacobian_positive
#print axioms supercritical_jacobian_zero
#print axioms positive_initial_jacobian
#print axioms half_period_rebound
#print axioms polar_gradient_norm
#print axioms fisher_gradient_energy
#print axioms polar_canonical_jacobian
#print axioms counterwave_peak_velocity
#print axioms balanced_counterwave_node

end DoorsTransport20260926
