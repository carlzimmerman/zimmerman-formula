import Mathlib

/-!
# XC3 — the filter's own foliation vertices: certificates for the inequalities

SCOPE. Lean certifies the inequalities behind `real_research/extra_crispy_2026/XC3_filter_foliation_vertices.py`. The
jet expansions of the leaf Laplacian and the leaf-metric argument (C1, C2), the finite-difference check of the
heat-kernel derivative (C3) and the numbers (C4–C6) are computed in that lane.

* `heat_factor_le_b`, `heat_factor_le_inv`: the high-momentum factor of the heat-kernel derivative obeys
  (1 − e^{−bK²})/K² ≤ b and ≤ 1/K² (XC3 C3).
* `ratio_bound_at_lowest_k`: for k ≥ 1/L the induced-to-khronon ratio 6Cg²/(c₂k²) is at most 6C(gL)²/c₂ — its value
  is set by the background's depth gL (XC3 C4).
* `unstable_band`: if the gradient coefficient c₂k² − 2Cg²cos²θ is negative (cos²θ ≤ 1), then k² < 2Cg²/c₂ (XC3 C5).
* `band_outside_wkb`: if gL√(2C/c₂) < 1, no wavenumber is both local (kL ≥ 1) and inside the band (k < g√(2C/c₂)) —
  the destabilising sign never reaches a mode the local analysis describes (XC3 C5).
-/

theorem heat_factor_le_b (b K : ℝ) (hK : K ≠ 0) :
    (1 - Real.exp (-(b * K ^ 2))) / K ^ 2 ≤ b := by
  have hK2 : 0 < K ^ 2 := by positivity
  have h := Real.add_one_le_exp (-(b * K ^ 2))
  rw [div_le_iff₀ hK2]
  linarith

theorem heat_factor_le_inv (b K : ℝ) (hK : K ≠ 0) :
    (1 - Real.exp (-(b * K ^ 2))) / K ^ 2 ≤ 1 / K ^ 2 := by
  have hK2 : 0 < K ^ 2 := by positivity
  have hpos : 0 < Real.exp (-(b * K ^ 2)) := Real.exp_pos _
  apply div_le_div_of_nonneg_right _ hK2.le
  linarith

theorem ratio_bound_at_lowest_k (C g c2 k L : ℝ) (hC : 0 ≤ C) (hc2 : 0 < c2) (hL : 0 < L) (hk : 1 / L ≤ k) :
    6 * C * g ^ 2 / (c2 * k ^ 2) ≤ 6 * C * (g * L) ^ 2 / c2 := by
  have hk0 : 0 < k := lt_of_lt_of_le (by positivity) hk
  have hkL : 1 ≤ k * L := by
    have := (div_le_iff₀ hL).mp hk
    linarith
  have hk2L2 : 1 ≤ (k * L) ^ 2 := by nlinarith
  rw [div_le_div_iff₀ (by positivity) hc2]
  have hnum : 0 ≤ 6 * C * g ^ 2 := by positivity
  have : 6 * C * g ^ 2 * c2 * 1 ≤ 6 * C * g ^ 2 * c2 * (k * L) ^ 2 :=
    mul_le_mul_of_nonneg_left hk2L2 (by positivity)
  nlinarith

theorem unstable_band (C g c2 k cs2 : ℝ) (hC : 0 ≤ C) (hc2 : 0 < c2) (hcs1 : cs2 ≤ 1)
    (hneg : c2 * k ^ 2 - 2 * C * g ^ 2 * cs2 < 0) : k ^ 2 < 2 * C * g ^ 2 / c2 := by
  rw [lt_div_iff₀ hc2]
  have : 2 * C * g ^ 2 * cs2 ≤ 2 * C * g ^ 2 := by
    have h0 : 0 ≤ 2 * C * g ^ 2 := by positivity
    calc 2 * C * g ^ 2 * cs2 ≤ 2 * C * g ^ 2 * 1 := mul_le_mul_of_nonneg_left hcs1 h0
      _ = 2 * C * g ^ 2 := by ring
  nlinarith

theorem band_outside_wkb (g L s k : ℝ) (hL : 0 < L) (hsmall : g * L * s < 1) :
    ¬ (1 ≤ k * L ∧ k < g * s) := by
  rintro ⟨hloc, hband⟩
  have : k * L < g * s * L := by nlinarith
  nlinarith

#print axioms heat_factor_le_b
#print axioms heat_factor_le_inv
#print axioms ratio_bound_at_lowest_k
#print axioms unstable_band
#print axioms band_outside_wkb
