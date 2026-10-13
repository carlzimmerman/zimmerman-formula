import Mathlib

/-! CFG724 MUTATE twin (criteria 7b2193b05): F4 with limit 2√(GMa₀) and F6 with ln(1 + S). Both must FAIL to compile. -/

open Filter Topology Real

namespace CFG724M
/-- the C* field of a point mass at radius r -/
noncomputable def gpm (G M a0 r : ℝ) : ℝ :=
  (G * M / r ^ 2 + √((G * M / r ^ 2) ^ 2 + 4 * a0 * (G * M / r ^ 2))) / 2

/-- r·g(r) written through t = 1/r -/
noncomputable def vsq (G M a0 t : ℝ) : ℝ := G * M * t / 2 + √((G * M * t) ^ 2 + 4 * a0 * G * M) / 2

lemma vsq_eq {G M a0 r : ℝ} (hr : 0 < r) : r * gpm G M a0 r = vsq G M a0 r⁻¹ := by
  unfold gpm vsq
  have hr0 : r ≠ 0 := hr.ne'
  have hsq : r * √((G * M / r ^ 2) ^ 2 + 4 * a0 * (G * M / r ^ 2)) = √((G * M * r⁻¹) ^ 2 + 4 * a0 * G * M) := by
    have hY : (G * M * r⁻¹) ^ 2 + 4 * a0 * G * M = r ^ 2 * ((G * M / r ^ 2) ^ 2 + 4 * a0 * (G * M / r ^ 2)) := by
      field_simp
      try ring
    rw [hY, Real.sqrt_mul (sq_nonneg r), Real.sqrt_sq hr.le]
  have : r * ((G * M / r ^ 2 + √((G * M / r ^ 2) ^ 2 + 4 * a0 * (G * M / r ^ 2))) / 2)
      = (r * (G * M / r ^ 2)) / 2 + (r * √((G * M / r ^ 2) ^ 2 + 4 * a0 * (G * M / r ^ 2))) / 2 := by ring
  rw [this, hsq]
  congr 1
  field_simp
  try ring

/-- F4: the baryonic Tully–Fisher relation as a limit: v² = r g(r) → √(G M a₀). -/
theorem btfr_limit_MUTATE {G M a0 : ℝ} (hG : 0 < G) (hM : 0 < M) (ha : 0 < a0) :
    Tendsto (fun r => r * gpm G M a0 r) atTop (𝓝 (2 * √(G * M * a0))) := by
  have hcont : Continuous (vsq G M a0) := by unfold vsq; fun_prop
  have h0 : vsq G M a0 0 = √(G * M * a0) := by
    unfold vsq
    have : (G * M * 0) ^ 2 + 4 * a0 * G * M = 2 ^ 2 * (G * M * a0) := by ring
    rw [this, Real.sqrt_mul (by norm_num), Real.sqrt_sq (by norm_num)]
    ring
  have hlim : Tendsto (fun r : ℝ => vsq G M a0 r⁻¹) atTop (𝓝 (√(G * M * a0))) := by
    rw [← h0]
    exact (hcont.tendsto 0).comp tendsto_inv_atTop_zero
  refine hlim.congr' ?_
  filter_upwards [eventually_gt_atTop 0] with r hr
  exact (vsq_eq hr).symm

/-- F6: the ν_mono supply edge. -/
theorem supply_edge_MUTATE {S x : ℝ} (hS : 0 < S) : 1 / (Real.exp x - 1) = S ↔ x = Real.log (1 + S) := by
  constructor
  · intro h
    have hne : Real.exp x - 1 ≠ 0 := by
      intro h0; rw [h0, div_zero] at h; linarith
    have he : Real.exp x = 1 + 1 / S := by
      field_simp at h ⊢; linarith
    rw [← he, Real.log_exp]
  · intro h
    have hpos : 0 < 1 + 1 / S := by positivity
    rw [h, Real.exp_log hpos, add_sub_cancel_left, one_div_one_div]

end CFG724M
