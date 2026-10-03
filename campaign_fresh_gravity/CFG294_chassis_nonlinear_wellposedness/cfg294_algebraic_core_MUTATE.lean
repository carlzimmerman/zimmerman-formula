import Mathlib

/-!
# CFG294 MUTATE — the gap theorem on a window that contains the crossing c_S = 1 must NOT compile

The window is moved so that alpha reaches c₂/(1 + 2c₂) at c₂ = 1/15 (alpha = 1/17), i.e. the crossing of the families
{±1} and {±c_S}. The same statement and the same proof as `cs2_gap_window` must fail: the claim is false at
(α, c₂) = (1/17, 1/15), where c_S² = 1. A successful compile of this file would mean the certificate does not bite.
-/

theorem cs2_gap_window_MUTATE (α c : ℝ) (ha : 0 < α) (ham : α ≤ 1 / 17) (hc : 1 / 15 ≤ c) :
    c * (2 - α) > 443 ^ 2 * (α * (2 + 3 * c)) := by
  have hD : 0 ≤ 2 - α * (1 + 3 * 443 ^ 2) := by nlinarith
  have h1 : 0 ≤ (c - 1 / 15) * (2 - α * (1 + 3 * 443 ^ 2)) := mul_nonneg (by linarith) hD
  have h2 : 0 ≤ (1 / 15 : ℝ) * (1 + 3 * 443 ^ 2) * (1 / 17 - α) := by
    apply mul_nonneg; · norm_num
    · linarith
  nlinarith [h1, h2]
