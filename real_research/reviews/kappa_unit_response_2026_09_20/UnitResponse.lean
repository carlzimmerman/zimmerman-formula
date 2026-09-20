import Mathlib

/-! Exact algebraic elimination of two nondynamical response variables.
The action-to-stationarity calculation is independently symbolic in verify.py.
The relative action coefficient is retained as lambda; it is not derived from
covariance, the channel count, or a cosmological measurement in this file. -/
namespace UnitResponse
noncomputable section
set_option backward.isDefEq.respectTransparency false

def engagement (lam y : ℝ) : ℝ := lam*y/(1+lam*y)
def response (lam y : ℝ) : ℝ := 1-(1-engagement lam y)^2

/-- The exchange-symmetric auxiliary equations force equal channel states. -/
theorem equal_auxiliaries {lam y q₁ q₂ : ℝ}
    (hq₁ : q₁ ≤ 1) (hq₂ : q₂ ≤ 1)
    (h₁ : (1-q₁)^2 = (lam*y)^2*q₁*q₂)
    (h₂ : (1-q₂)^2 = (lam*y)^2*q₁*q₂) : q₁=q₂ := by
  nlinarith [sq_nonneg (q₁-q₂)]

/-- For positive lambda and nonnegative acceleration, stationary auxiliary
states in 0<q<=1 are uniquely q=1/(1+lambda*y). -/
theorem stationary_auxiliary {lam y q₁ q₂ : ℝ}
    (hlam : 0 < lam) (hy : 0 ≤ y)
    (hpos₁ : 0 < q₁) (hupper₁ : q₁ ≤ 1) (hupper₂ : q₂ ≤ 1)
    (h₁ : (1-q₁)^2 = (lam*y)^2*q₁*q₂)
    (h₂ : (1-q₂)^2 = (lam*y)^2*q₁*q₂) :
    q₁=1/(1+lam*y) ∧ q₂=1/(1+lam*y) := by
  have he := equal_auxiliaries hupper₁ hupper₂ h₁ h₂
  have hnon : 0 ≤ lam*y := mul_nonneg hlam.le hy
  have hp : 0 ≤ lam*y*q₁ := mul_nonneg hnon hpos₁.le
  have heq : 1-q₁=lam*y*q₁ := by
    rw [← he] at h₁
    nlinarith [sq_nonneg (1-q₁-lam*y*q₁)]
  have hd : 1+lam*y ≠ 0 := by linarith
  have hq : q₁=1/(1+lam*y) := by
    apply (eq_div_iff hd).mpr
    nlinarith [heq]
  exact ⟨hq, he.symm.trans hq⟩

theorem auxiliary_exists {lam y : ℝ} (hlam : 0 < lam) (hy : 0 ≤ y) :
    let q := 1/(1+lam*y)
    0 < q ∧ q ≤ 1 ∧ (1-q)^2=(lam*y)^2*q*q := by
  dsimp
  have hnon : 0 ≤ lam*y := mul_nonneg hlam.le hy
  have hd : 0 < 1+lam*y := by linarith
  refine ⟨by positivity, (div_le_one hd).mpr (by linarith), ?_⟩
  field_simp
  ring

theorem stationary_engagement {lam y q : ℝ} (h : q=1/(1+lam*y))
    (hd : 1+lam*y ≠ 0) : 1-q=engagement lam y := by
  rw [h]
  unfold engagement
  field_simp
  ring

theorem engagement_zero (lam : ℝ) : engagement lam 0=0 := by
  simp [engagement]

/-- The derivative is derived from the stationary solution, not inserted as
a premise; its value records the relative action coefficient. -/
theorem engagement_derivative (lam : ℝ) :
    HasDerivAt (engagement lam) lam 0 := by
  have hnum : HasDerivAt (fun y : ℝ => lam*y) lam 0 := by
    simpa using (hasDerivAt_id (0 : ℝ)).const_mul lam
  have hden : HasDerivAt (fun y : ℝ => 1+lam*y) lam 0 := by
    simpa using hnum.const_add 1
  convert! hnum.div hden (by norm_num : (1 : ℝ)+lam*0 ≠ 0) using 1
  simp

theorem response_derivative (lam : ℝ) :
    HasDerivAt (response lam) (2*lam) 0 := by
  have he := engagement_derivative lam
  have h := (he.const_sub 1).pow 2 |>.const_sub 1
  convert! h using 1
  simp [engagement_zero]

/-- In the action with equal relative weights, unit response follows. -/
theorem equal_weight_unit_response :
    engagement 1 0=0 ∧ HasDerivAt (engagement 1) 1 0 ∧
    HasDerivAt (response 1) 2 0 := by
  exact ⟨engagement_zero 1, engagement_derivative 1, by simpa using response_derivative 1⟩

/-- Matching the derived deep flux to a MOND scale leaves lambda explicit. -/
theorem deep_matching {lam s a0 : ℝ} (hlam : lam ≠ 0) (hs : s ≠ 0)
    (hmatch : (2*lam/s)*a0=1) : a0/s=1/(2*lam) := by
  field_simp at hmatch ⊢
  nlinarith [hmatch]

/-- This is the target for the equal-weight action, conditional on the
physical deep-limit matching, not conditional on assuming kappa=1/2. -/
theorem equal_weight_kappa_half {s a0 : ℝ} (hs : s ≠ 0)
    (hmatch : (2/s)*a0=1) : a0/s=1/2 := by
  simpa using deep_matching (lam := 1) (by norm_num) hs (by simpa using hmatch)

/-- Unit response is precisely the remaining coefficient selection. -/
theorem half_iff_unit_weight {lam s a0 : ℝ} (hlam : lam ≠ 0) (hs : s ≠ 0)
    (hmatch : (2*lam/s)*a0=1) : a0/s=1/2 ↔ lam=1 := by
  rw [deep_matching hlam hs hmatch]
  constructor
  · intro h
    field_simp at h
    linarith
  · intro h
    rw [h]
    norm_num

/-- Canonical field normalization cannot fix a relative coupling ratio. -/
theorem canonical_ratio_invariant {Z beta a : ℝ} (ha : a ≠ 0) :
    (Z/a^2)/(beta/a)^2=Z/beta^2 := by
  field_simp

/-- A variation of response couplings can leave the entire quadratic
vacuum functional fixed, not just its value at one background. -/
theorem fixed_vacuum_coefficient (D b beta : ℝ) :
    (2*D-2*b*beta^2)/2+b*beta^2=D := by ring

/-- Two positive-coupling examples share D=4 but have different kappa². -/
theorem fixed_vacuum_distinct_response {b : ℝ} (_hb0 : 0 ≤ b) (hb1 : b < 1) :
    0 < 8-2*b ∧ 0 < 8-8*b ∧
    (8-2*b)/2+b*1^2=4 ∧ (8-8*b)/2+b*2^2=4 ∧
    (1 : ℝ)^2/4 ≠ (2 : ℝ)^2/4 := by
  constructor
  · linarith
  constructor
  · linarith
  constructor
  · ring
  constructor
  · ring
  · norm_num

#print axioms equal_auxiliaries
#print axioms stationary_auxiliary
#print axioms auxiliary_exists
#print axioms stationary_engagement
#print axioms engagement_zero
#print axioms engagement_derivative
#print axioms response_derivative
#print axioms equal_weight_unit_response
#print axioms deep_matching
#print axioms equal_weight_kappa_half
#print axioms half_iff_unit_weight
#print axioms canonical_ratio_invariant
#print axioms fixed_vacuum_coefficient
#print axioms fixed_vacuum_distinct_response
end
end UnitResponse
