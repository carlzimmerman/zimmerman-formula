import Mathlib
import Mathlib.Tactic

/-
  M01 -- Lean certificate for the asymmetric-drift a0-bias DIRECTION (opus_48 muse_a0z_2026/M01).

  The MUSE-DARK III a0(z) puzzle: the pressure-support (asymmetric-drift) correction injects a bias into
  the fitted a0 of the form  b(σ) = 2 · eps · eta · σ² / v_c²   (eps = net over-correction fraction,
  eta = profile factor, σ = intrinsic velocity dispersion, v_c = circular velocity), with eps,eta,v_c > 0.

  Two load-bearing STRUCTURAL claims of the calculation, certified here:
    (1) b(0) = 0            -- no bias without pressure support;
    (2) 0 ≤ σ₁ < σ₂  ⟹  b(σ₁) < b(σ₂)   -- the bias is STRICTLY INCREASING in σ, hence (since the
        measured σ₀(z) rises with z) the bias grows with redshift and lifts the fitted a0 UPWARD --
        exactly the sign of MUSE's apparent a0(z) rise.

  This certifies the qualitative content of M01 (the a0-rising direction and σ-growth); the magnitude is a
  numerical/empirical statement handled in the Python lane, not here.
-/

noncomputable section

/-- The AD-correction bias on the fitted `a0` as a function of the velocity dispersion `σ`. -/
def adBias (eps eta vc σ : ℝ) : ℝ := 2 * eps * eta * σ ^ 2 / vc ^ 2

/-- (1) No pressure support (σ = 0) ⇒ no bias. -/
theorem adBias_zero (eps eta vc : ℝ) : adBias eps eta vc 0 = 0 := by
  simp [adBias]

/-- The bias coefficient `2·eps·eta/vc²` is strictly positive when eps, eta, vc are. -/
theorem adBias_coeff_pos {eps eta vc : ℝ} (he : 0 < eps) (ht : 0 < eta) (hv : 0 < vc) :
    0 < 2 * eps * eta / vc ^ 2 := by
  have hnum : 0 < 2 * eps * eta := by positivity
  have hden : 0 < vc ^ 2 := by positivity
  positivity

/-- (2) The bias is STRICTLY INCREASING in σ on `[0, ∞)`: a rising σ(z) drives the fitted a0 upward. -/
theorem adBias_strictMono {eps eta vc : ℝ} (he : 0 < eps) (ht : 0 < eta) (hv : 0 < vc)
    {σ₁ σ₂ : ℝ} (h1 : 0 ≤ σ₁) (h12 : σ₁ < σ₂) :
    adBias eps eta vc σ₁ < adBias eps eta vc σ₂ := by
  have hsq : σ₁ ^ 2 < σ₂ ^ 2 := by
    have h2 : (0:ℝ) ≤ σ₂ := le_of_lt (lt_of_le_of_lt h1 h12)
    nlinarith [sq_nonneg (σ₂ - σ₁), sq_nonneg (σ₂ + σ₁)]
  have hcoeff : 0 < 2 * eps * eta / vc ^ 2 := adBias_coeff_pos he ht hv
  -- rewrite adBias as coeff * σ²
  have e1 : adBias eps eta vc σ₁ = (2 * eps * eta / vc ^ 2) * σ₁ ^ 2 := by
    simp only [adBias]; ring
  have e2 : adBias eps eta vc σ₂ = (2 * eps * eta / vc ^ 2) * σ₂ ^ 2 := by
    simp only [adBias]; ring
  rw [e1, e2]
  exact mul_lt_mul_of_pos_left hsq hcoeff

/-- Corollary: the bias is nonnegative for every σ (an apparent-a0 rise, never a spurious decline). -/
theorem adBias_nonneg {eps eta vc : ℝ} (he : 0 < eps) (ht : 0 < eta) (hv : 0 < vc)
    (σ : ℝ) : 0 ≤ adBias eps eta vc σ := by
  unfold adBias
  have : (0:ℝ) < vc ^ 2 := by positivity
  positivity

end
