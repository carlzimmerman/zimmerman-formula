import Mathlib

/-!
# MineM5-C: the alpha = 2 cancellation of the memory-force residual, its scale-invariance, and the lambda^4 scaling arithmetic

Source lane: real_research/reviews/mi_N_count_and_kappa_iff_2026.py, Part A (lines ~108-134: checks A1 "1 - mu_eff = Theta^(-alpha)(2-alpha)/(4 alpha)", A2 "vanishes at alpha = 2",
  A3 "mu + (arg/2) d mu/d(arg) is the SAME functional whether Theta ~ |a| or ~ v", NC1 "no cancellation at alpha = 3/2") and Part B line ~150 (B1, the lambda^4 scaling of Delta).

CERTIFIED (premises => conclusions; calculus over the reals with rpow):
* `hasDerivAt_mu`: for alpha > 0, Theta > 0 the model kernel mu(Theta) = 1 - Theta^(-alpha)/(2 alpha) has derivative Theta^(-alpha-1)/2.
* `residual_formula`: with mu_eff := mu + (Theta/2) mu', 1 - mu_eff = Theta^(-alpha) (2 - alpha)/(4 alpha).
* `residual_zero_at_two`: the residual vanishes at alpha = 2; `residual_ne_zero_of_ne_two`: it is nonzero for every alpha != 2 (in particular alpha = 3/2, the lane's control NC1).
* `mueff_scale_invariant`: for any function m with derivative m' at k Y (any real k), the operator m + (Y/2) d/dY[m(k Y)] equals the operator m(Theta) + (Theta/2) m'(Theta) evaluated at Theta = k Y,
  so mu_eff is the same functional whether the argument is proportional to |a| (short memory) or v (long memory), for ANY kernel m (chain rule cancels k).
* `delta_lambda4`: with Theta = (8/3) v/(pi a0 lambda), g/(32 Theta^4) = g (3 pi a0 lambda)^4/(32 * 8^4 v^4), i.e. the residual anomaly scales as lambda^4.

NOT certified: that mu = 1 - Theta^(-alpha)/(2 alpha) is the framework's kernel (it is the lane's large-Theta model; the actual kernel and its exact next-order coefficient are NOT computed here:
the lane's "1 - mu_eff = 1/(32 Theta^4)" is asserted in its text, not checked symbolically, so it is not certified); the ephemeris bound BOUND = 3.66e-14 and the resulting lambda_max, N >= 2.1e6
(empirical/numeric); the physical memory-force renormalisation mu_eff = mu + (Theta/2) dmu/dTheta (the lane's definition, derived elsewhere); any planetary-anomaly statement.
kappa = 1/2 is FITTED; nothing here says the theory is closed.
-/

open Real

namespace MineM5C

/-- the lane's model kernel -/
noncomputable def mu (α Θ : ℝ) : ℝ := 1 - Θ ^ (-α) / (2 * α)

/-- derivative of the model kernel: Theta^(-alpha-1)/2 -/
theorem hasDerivAt_mu {α Θ : ℝ} (hα : 0 < α) (hΘ : 0 < Θ) :
    HasDerivAt (mu α) (Θ ^ (-α - 1) / 2) Θ := by
  have h := Real.hasDerivAt_rpow_const (x := Θ) (p := -α) (Or.inl hΘ.ne')
  have h2 := (h.div_const (2 * α)).const_sub 1
  have hne : α ≠ 0 := hα.ne'
  have e : -((-α) * Θ ^ (-α - 1) / (2 * α)) = Θ ^ (-α - 1) / 2 := by
    field_simp
  rw [e] at h2
  exact h2

/-- 1 - mu_eff = Theta^(-alpha)(2 - alpha)/(4 alpha), mu_eff := mu + (Theta/2) mu' -/
theorem residual_formula {α Θ : ℝ} (hα : 0 < α) (hΘ : 0 < Θ) :
    1 - (mu α Θ + Θ / 2 * (Θ ^ (-α - 1) / 2)) = Θ ^ (-α) * (2 - α) / (4 * α) := by
  have hne : α ≠ 0 := hα.ne'
  have hp : Θ * Θ ^ (-α - 1) = Θ ^ (-α) := by
    have := Real.rpow_add hΘ 1 (-α - 1)
    rw [Real.rpow_one] at this
    rw [← this]; congr 1; ring
  unfold mu
  have : Θ / 2 * (Θ ^ (-α - 1) / 2) = Θ ^ (-α) / 4 := by
    rw [← hp]; ring
  rw [this]
  field_simp
  ring

/-- the cancellation: at alpha = 2 the residual vanishes identically -/
theorem residual_zero_at_two {Θ : ℝ} (hΘ : 0 < Θ) :
    1 - (mu 2 Θ + Θ / 2 * (Θ ^ (-(2 : ℝ) - 1) / 2)) = 0 := by
  rw [residual_formula (by norm_num) hΘ]
  norm_num

/-- and it is nonzero for every alpha != 2 (control: alpha = 3/2) -/
theorem residual_ne_zero_of_ne_two {α Θ : ℝ} (hα : 0 < α) (hΘ : 0 < Θ) (h2 : α ≠ 2) :
    1 - (mu α Θ + Θ / 2 * (Θ ^ (-α - 1) / 2)) ≠ 0 := by
  rw [residual_formula hα hΘ]
  have h1 : 0 < Θ ^ (-α) := Real.rpow_pos_of_pos hΘ _
  have h3 : (2 - α) ≠ 0 := sub_ne_zero.mpr (Ne.symm h2)
  positivity

/-- the operator m + (arg/2) m' is the same functional whether the argument is k*Y or the bare argument: chain rule cancels k -/
theorem mueff_scale_invariant {m : ℝ → ℝ} {m' k Y : ℝ}
    (h : HasDerivAt m m' (k * Y)) :
    ∃ d : ℝ, HasDerivAt (fun y => m (k * y)) d Y ∧
      m (k * Y) + Y / 2 * d = m (k * Y) + (k * Y) / 2 * m' := by
  refine ⟨m' * k, ?_, by ring⟩
  have h1 : HasDerivAt (fun y : ℝ => k * y) k Y := by
    simpa using (hasDerivAt_id Y).const_mul k
  exact HasDerivAt.scomp Y h h1 |>.congr_deriv (by simp [smul_eq_mul, mul_comm])

/-- lambda^4 scaling arithmetic: g/(32 Theta^4) with Theta = (8/3) v/(pi a0 lambda) -/
theorem delta_lambda4 {g v a0 lam : ℝ} (hv : v ≠ 0) (ha : a0 ≠ 0) (hl : lam ≠ 0) :
    g / (32 * ((8 / 3) * v / (π * a0 * lam)) ^ 4) = g * (3 * π * a0 * lam) ^ 4 / (32 * 8 ^ 4 * v ^ 4) := by
  have hp : π ≠ 0 := Real.pi_ne_zero
  field_simp

end MineM5C

#print axioms MineM5C.hasDerivAt_mu
#print axioms MineM5C.residual_formula
#print axioms MineM5C.residual_zero_at_two
#print axioms MineM5C.residual_ne_zero_of_ne_two
#print axioms MineM5C.mueff_scale_invariant
#print axioms MineM5C.delta_lambda4
