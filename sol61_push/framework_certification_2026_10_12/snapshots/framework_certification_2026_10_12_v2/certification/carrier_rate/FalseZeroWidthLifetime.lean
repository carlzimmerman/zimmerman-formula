import Mathlib

/-! FRAMEWORK-CERT-TRANSPORT-2026-10-12: conditional carrier rate bound.
Natural units hbar=c=1. The width formula is an EXPLICIT hypothesis requiring
canonical perturbative quantization, Bose asymptotic daughter states, tree
amplitude 2g, identical-state factor 1/2, invariant phase space/Golden Rule,
and weak dilute vacuum use excluding medium/coherent/loop corrections.
Lean certifies only consequences, not these quantum assumptions or microphysics.
-/
noncomputable section
namespace FrameworkCarrierRate

def speed (M Δ : ℝ) : ℝ := Real.sqrt Δ / M

theorem speed_positive (M Δ : ℝ) (hM : 0 < M) (hΔ : 0 < Δ) : 0 < speed M Δ := by
  unfold speed
  positivity

theorem speed_kinematic (M Δ : ℝ) (hM : M ≠ 0) (hΔ : 0 ≤ Δ) :
    M ^ 2 * speed M Δ ^ 2 = Δ := by
  unfold speed
  rw [div_pow, Real.sq_sqrt hΔ]
  field_simp

/-- Δ=M²−4m² with positive daughter mass guarantees subluminal speed. -/
theorem speed_less_than_one (M Δ m : ℝ) (hM : 0 < M) (hm : 0 < m)
    (hΔ : 0 < Δ) (hgap : Δ = M ^ 2 - 4 * m ^ 2) : speed M Δ < 1 := by
  have hs := speed_positive M Δ hM hΔ
  have hk := speed_kinematic M Δ hM.ne' hΔ.le
  nlinarith [sq_nonneg (speed M Δ - 1), mul_pos hm hm]

/-- Exact residual from the declared stable-action coefficient relation and
stipulated perturbative width, with no restriction on the sign of g. -/
theorem rate_margin (M Δ g rep lam Γ : ℝ) (hM : 0 < M) (hΔ : 0 < Δ)
    (hlam : lam = rep + g ^ 2 / Δ)
    (hΓ : Γ = g ^ 2 * speed M Δ / (8 * Real.pi * M)) :
    lam * speed M Δ ^ 3 / (8 * Real.pi) - Γ / M =
      rep * speed M Δ ^ 3 / (8 * Real.pi) := by
  have hs := speed_positive M Δ hM hΔ
  have hk := speed_kinematic M Δ hM.ne' hΔ.le
  have hlam' : lam = rep + g ^ 2 / (M ^ 2 * speed M Δ ^ 2) := by rw [hk]; exact hlam
  rw [hlam', hΓ]
  field_simp [hM.ne', hs.ne', Real.pi_ne_zero]
  ring

theorem coldness_rate_bound (M Δ g rep lam Γ : ℝ) (hM : 0 < M) (hΔ : 0 < Δ)
    (hrep : 0 ≤ rep) (hlam : lam = rep + g ^ 2 / Δ)
    (hΓ : Γ = g ^ 2 * speed M Δ / (8 * Real.pi * M)) :
    Γ / M ≤ lam * speed M Δ ^ 3 / (8 * Real.pi) := by
  have hm := rate_margin M Δ g rep lam Γ hM hΔ hlam hΓ
  have hs := speed_positive M Δ hM hΔ
  have hr : 0 ≤ rep * speed M Δ ^ 3 / (8 * Real.pi) := by positivity
  linarith

/-- For a nonzero rate, inverse width is the declared natural-unit lifetime. -/
theorem lifetime_floor (M Δ g rep lam Γ : ℝ) (hM : 0 < M) (hΔ : 0 < Δ)
    (hrep : 0 ≤ rep) (hlam : lam = rep + g ^ 2 / Δ)
    (hΓ : Γ = g ^ 2 * speed M Δ / (8 * Real.pi * M)) (hΓpos : 0 < Γ) :
    8 * Real.pi / (lam * speed M Δ ^ 3) ≤ M / Γ := by
  have hb := coldness_rate_bound M Δ g rep lam Γ hM hΔ hrep hlam hΓ
  have hs := speed_positive M Δ hM hΔ
  have hlampos : 0 < lam := by
    by_contra hn
    have hlamneg : lam ≤ 0 := le_of_not_gt hn
    have hzero : lam * speed M Δ ^ 3 / (8 * Real.pi) ≤ 0 :=
      div_nonpos_of_nonpos_of_nonneg (mul_nonpos_of_nonpos_of_nonneg hlamneg (by positivity)) (by positivity)
    have hp : 0 < Γ / M := div_pos hΓpos hM
    linarith
  apply (div_le_div_iff₀ (by positivity : 0 < lam * speed M Δ ^ 3) hΓpos).mpr
  have hx := (div_le_div_iff₀ hM (by positivity : 0 < 8 * Real.pi)).mp hb
  nlinarith [hx]

/-- The rate bound is strict for strictly positive repulsion. -/
theorem positive_repulsion_strict (M Δ g rep lam Γ : ℝ) (hM : 0 < M) (hΔ : 0 < Δ)
    (hrep : 0 < rep) (hlam : lam = rep + g ^ 2 / Δ)
    (hΓ : Γ = g ^ 2 * speed M Δ / (8 * Real.pi * M)) :
    Γ / M < lam * speed M Δ ^ 3 / (8 * Real.pi) := by
  have hm := rate_margin M Δ g rep lam Γ hM hΔ hlam hΓ
  have hs := speed_positive M Δ hM hΔ
  have hr : 0 < rep * speed M Δ ^ 3 / (8 * Real.pi) := by positivity
  linarith

/-- Repulsion-free limit saturates; positive strict margins cannot be asserted there. -/
theorem zero_repulsion_saturates (M Δ g lam Γ : ℝ) (hM : 0 < M) (hΔ : 0 < Δ)
    (hlam : lam = g ^ 2 / Δ)
    (hΓ : Γ = g ^ 2 * speed M Δ / (8 * Real.pi * M)) :
    Γ / M = lam * speed M Δ ^ 3 / (8 * Real.pi) := by
  have hm := rate_margin M Δ g 0 lam Γ hM hΔ (by simpa using hlam) hΓ
  simp at hm
  linarith

end FrameworkCarrierRate
#print axioms FrameworkCarrierRate.speed_positive
#print axioms FrameworkCarrierRate.speed_kinematic
#print axioms FrameworkCarrierRate.speed_less_than_one
#print axioms FrameworkCarrierRate.rate_margin
#print axioms FrameworkCarrierRate.coldness_rate_bound
#print axioms FrameworkCarrierRate.lifetime_floor
#print axioms FrameworkCarrierRate.positive_repulsion_strict
#print axioms FrameworkCarrierRate.zero_repulsion_saturates

/- EXPECTED FAILURE: dropping Gamma>0 admits g=Gamma=0; totalized M/0 is 0. -/
example : 8 * Real.pi / (1 * FrameworkCarrierRate.speed 2 1 ^ 3) ≤ (2 : ℝ) / 0 := by
  norm_num [FrameworkCarrierRate.speed]
  have hp := Real.pi_pos
  nlinarith
