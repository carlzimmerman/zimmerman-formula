/-
CFG355 certificates: tidal rule T1 (middle eigenvalue >= tau) with a cold-rank veto (rank sigma_c = 2 -> OFF).
-/
import Mathlib

open Real

namespace CFG355

/-- middle of three numbers (T1 reads the middle tidal eigenvalue). -/
noncomputable def med3 (a b c : ℝ) : ℝ := max (min a b) (min (max a b) c)

/-- T1 and the combined rule f = T1 AND NOT (rank = 2); MUTATE vetoes rank 3. -/
def T1on (l2 tau : ℝ) : Prop := tau ≤ l2
def fOn (l2 tau : ℝ) (rank : ℕ) : Prop := tau ≤ l2 ∧ rank ≠ 2
def fMut (l2 tau : ℝ) (rank : ℕ) : Prop := tau ≤ l2 ∧ rank ≠ 3

/-- sphere triple (lt, lt, lr) with lr <= lt: the middle eigenvalue is lt. -/
theorem sphere_med (lt lr : ℝ) (h : lr ≤ lt) : med3 lt lt lr = lt := by
  unfold med3; simp [min_self, max_self, h]

/-- cylinder core (c, c, 0), c >= 0: middle eigenvalue c. -/
theorem cyl_med (c : ℝ) (h : 0 ≤ c) : med3 c c 0 = c := by
  unfold med3; simp [h]

/-- plane (d, 0, 0), d >= 0: middle eigenvalue 0. -/
theorem plane_med (d : ℝ) (h : 0 ≤ d) : med3 d 0 0 = 0 := by
  unfold med3; simp [h]

/-- host interior: sphere at or inside turnaround, rank 3 -> ON. -/
theorem sphere_rank3_on (lt lr tau : ℝ) (h : lr ≤ lt) (ht : tau ≤ lt) : fOn (med3 lt lt lr) tau 3 := by
  rw [sphere_med lt lr h]; exact ⟨ht, by decide⟩

/-- halo infall zone: single stream (rank 0) inside turnaround -> ON. -/
theorem sphere_rank0_on (lt lr tau : ℝ) (h : lr ≤ lt) (ht : tau ≤ lt) : fOn (med3 lt lt lr) tau 0 := by
  rw [sphere_med lt lr h]; exact ⟨ht, by decide⟩

/-- ideal filament core (rank 2) is vetoed, whatever T1 says. -/
theorem cyl_rank2_off (c tau : ℝ) : ¬ fOn (med3 c c 0) tau 2 := by
  intro h; exact h.2 rfl

/-- a plane is OFF at any rank when tau > 0. -/
theorem plane_off (d tau : ℝ) (r : ℕ) (hd : 0 ≤ d) (ht : 0 < tau) : ¬ fOn (med3 d 0 0) tau r := by
  rw [plane_med d hd]; intro h; unfold fOn at h; linarith [h.1]

/-- the generic 3-stream shell of a host (rank 2) is vetoed even inside turnaround. -/
theorem shell_vetoed (lt lr tau : ℝ) : ¬ fOn (med3 lt lt lr) tau 2 := by
  intro h; exact h.2 rfl

/-- false-positive bound: ON(f) is a subset of ON(T1). -/
theorem f_subset_T1 (l tau : ℝ) (r : ℕ) (h : fOn l tau r) : T1on l tau := h.1

theorem indicator_le (l tau : ℝ) (r : ℕ) [Decidable (fOn l tau r)] [Decidable (T1on l tau)] :
    (if fOn l tau r then (1 : ℝ) else 0) ≤ (if T1on l tau then 1 else 0) := by
  by_cases h : fOn l tau r
  · simp [h, f_subset_T1 l tau r h]
  · by_cases h' : T1on l tau <;> simp [h, h']

/-- MUTATE: the rank-3 veto switches OFF the host interior. -/
theorem mutate_interior_off (lt lr tau : ℝ) : ¬ fMut (med3 lt lt lr) tau 3 := by
  intro h; exact h.2 rfl

/-- three streams: the weighted deviations sum to zero, so the third lies in the span of the other two (rank <= 2). -/
theorem three_streams_dependent (w1 w2 w3 x1 x2 x3 : ℝ) (h : w1 * x1 + w2 * x2 + w3 * x3 = 0) (hw : w3 ≠ 0) :
    x3 = -(w1 / w3) * x1 - (w2 / w3) * x2 := by
  field_simp; linarith

/-- conservation, rank part: on rank-1 sigma = s n n^T, (tr sigma) sigma - sigma^2 = 0 entrywise. -/
theorem rank1_stress_entry (s a b c ni nj : ℝ) :
    (s * a * a + s * b * b + s * c * c) * (s * ni * nj)
      - (s * ni * a * (s * a * nj) + s * ni * b * (s * b * nj) + s * ni * c * (s * c * nj)) = 0 := by
  ring

/-- e2 (principal 2x2 minor) vanishes on rank 1. -/
theorem rank1_minor (s a b : ℝ) : (s * a * a) * (s * b * b) - (s * a * b) * (s * a * b) = 0 := by ring

/-- sigma adj(sigma) = det I for a symmetric 3x3: diagonal entry equals the determinant, off-diagonal vanishes. -/
theorem adj_diag (p q r u v w : ℝ) :
    p * (q * r - w * w) + u * (w * v - u * r) + v * (u * w - q * v)
      = p * q * r + 2 * u * v * w - p * w ^ 2 - q * v ^ 2 - r * u ^ 2 := by ring

theorem adj_offdiag (_p q r u v w : ℝ) :
    u * (q * r - w * w) + q * (w * v - u * r) + w * (u * w - q * v) = 0 := by ring

/-- width: eps >= c_d Delta / 6 and (g_ph/g)^2 <= 1 give V_b/V_c^2 = c_d Delta/(6 eps) (g_ph/g)^2 <= 1. -/
theorem width_bound (cd D eps g : ℝ) (hcd : 0 ≤ cd) (hD : 0 < D) (he : 0 < eps) (hw : cd * D / 6 ≤ eps)
    (hg : g ^ 2 ≤ 1) : cd * D / (6 * eps) * g ^ 2 ≤ 1 := by
  have h1 : cd * D / (6 * eps) ≤ 1 := by
    rw [div_le_one (by positivity)]; linarith
  have h0 : 0 ≤ cd * D / (6 * eps) := by positivity
  calc cd * D / (6 * eps) * g ^ 2 ≤ 1 * 1 := mul_le_mul h1 hg (sq_nonneg g) zero_le_one
    _ = 1 := by ring

theorem eps_min_pos (cd D : ℝ) (hcd : 0 < cd) (hD : 1 < D) : 0 < cd * D / 6 := by positivity

/-- the generic shell between the caustics holds > 3% of the r_ta volume and > 12% of an isothermal phantom. -/
theorem shell_share : (0.3588 : ℝ) ^ 3 - 0.2321 ^ 3 > 0.03 ∧ (0.3588 : ℝ) - 0.2321 > 0.12 := by
  constructor <;> norm_num

end CFG355

#print axioms CFG355.sphere_med
#print axioms CFG355.cyl_med
#print axioms CFG355.plane_med
#print axioms CFG355.sphere_rank3_on
#print axioms CFG355.sphere_rank0_on
#print axioms CFG355.cyl_rank2_off
#print axioms CFG355.plane_off
#print axioms CFG355.shell_vetoed
#print axioms CFG355.f_subset_T1
#print axioms CFG355.indicator_le
#print axioms CFG355.mutate_interior_off
#print axioms CFG355.three_streams_dependent
#print axioms CFG355.rank1_stress_entry
#print axioms CFG355.rank1_minor
#print axioms CFG355.adj_diag
#print axioms CFG355.adj_offdiag
#print axioms CFG355.width_bound
#print axioms CFG355.eps_min_pos
#print axioms CFG355.shell_share
