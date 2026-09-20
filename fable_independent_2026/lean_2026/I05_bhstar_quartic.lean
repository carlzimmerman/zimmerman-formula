import Mathlib

/-!
# I05 — Wave M: the Eddington-quartic beta bound (the certified two-sided band)

SCOPE (per lean-math-certification): Lean certifies the ALGEBRA of the Eddington
standard-model quartic (1−β)/β⁴ = (M/M_E)² — the classical structure law of a
radiation-dominated star (Kippenhahn & Weigert ch. 13) — into a TWO-SIDED exact beta band:

    upper:  β ≤ (M_E/M)^{1/2}                                  (any M, from 1−β ≤ 1)
    lower:  β⁴ ≥ (1/2)·(M_E/M)²  i.e. β ≥ 2^{-1/4}·(M_E/M)^{1/2}  (for M ≥ 4·M_E, where
            the quartic itself forces β ≤ 1/2)

i.e. β ∝ M^{−1/2} with a certified 19% band. This is the thermodynamic correction that
replaces the gas-virial beta (4.6×10⁻⁸ at M = 10⁵ — wrong for a radiation-dominated star,
caught in this session) by β(10⁵) ≈ 0.023 — a ~500× larger Gamma1 gap, changing the
stability ceiling from ~10⁴ to the two-scale statement (global ~6×10⁷ vs pulsational
10⁵-⁶, Python lane `bhstar_m1_quartic_beta.py`). Lean certifies the algebra; the quartic is
a hypothesis (the classical structure law). Zero `sorry`; axioms ⊆ {propext,
Classical.choice, Quot.sound}.
-/

noncomputable section

/-- **M (upper bound, exact).** From the quartic, β ≤ (M_E/M)^{1/2} for every M > M_E. -/
theorem quartic_beta_upper {M ME β : ℝ} (hME : 0 < ME) (hM : 0 < M) (hβ : 0 < β)
    (hquartic : (1 - β) / β ^ 4 = (M / ME) ^ 2) :
    β ≤ Real.sqrt (ME / M) := by
  -- NOTE: the exponent literal `(1 / 2)` elaborates at ℕ in this build (binop%), so the
  -- deliverable statement uses Real.sqrt explicitly.
  have h1 : β ^ 4 * (M / ME) ^ 2 = 1 - β := by
    rw [← hquartic]
    field_simp
  have h2 : β ^ 4 = (1 - β) * (ME / M) ^ 2 := by
    rw [← h1]
    field_simp
  have hβ1 : β ≤ 1 := by
    have h3 : 0 ≤ 1 - β := by rw [← h1]; positivity
    linarith
  have h4 : β ^ 4 ≤ (ME / M) ^ 2 := by
    have h5 : β ^ 4 * (M / ME) ^ 2 ≤ 1 := by
      rw [h1]
      linarith
    rw [h2]
    have hβ1' : (1 : ℝ) - β ≤ 1 := by linarith
    have hXpos : 0 ≤ (ME / M) ^ 2 := by positivity
    nlinarith [hβ1', hXpos]
  have h6 : β ^ 4 = (β ^ 2) ^ 2 := by ring
  have h7 := Real.sqrt_le_sqrt h4
  rw [h6, Real.sqrt_sq (by positivity), Real.sqrt_sq (by positivity)] at h7
  have h8 := Real.sqrt_le_sqrt h7
  rw [Real.sqrt_sq hβ.le] at h8
  exact h8

/-- **M (lower bound, for M ≥ 4·M_E).** The quartic forces β ≤ 1/2 (via the upper bound
and M ≥ 4·M_E), hence 1−β ≥ 1/2 and β⁴ ≥ (1/2)·(M_E/M)² — the lower edge of the band:
β ≥ 2^{-1/4}·(M_E/M)^{1/2}. -/
theorem quartic_beta4_lower {M ME β : ℝ} (hME : 0 < ME) (hM4 : 4 * ME ≤ M) (hβ : 0 < β)
    (hquartic : (1 - β) / β ^ 4 = (M / ME) ^ 2) :
    (1 / 2) * (ME / M) ^ 2 ≤ β ^ 4 := by
  have hMpos : 0 < M := by linarith
  have h1 : β ^ 4 * (M / ME) ^ 2 = 1 - β := by
    rw [← hquartic]
    field_simp
  have h6 : β ^ 4 = (β ^ 2) ^ 2 := by ring
  have hb4 : 0 ≤ β ^ 4 := by rw [h6]; exact sq_nonneg (β ^ 2)
  have hK : (4:ℝ) ≤ M / ME := (le_div_iff₀ hME).mpr hM4
  have hK16 : (16:ℝ) ≤ (M / ME) ^ 2 := by
    have h45 : (4:ℝ) ^ 2 ≤ (M / ME) ^ 2 := pow_le_pow_left₀ (by norm_num) hK 2
    norm_num at h45
    exact h45
  have hK2 : β ^ 4 * 16 ≤ 1 - β := by
    calc β ^ 4 * 16 ≤ β ^ 4 * (M / ME) ^ 2 := mul_le_mul_of_nonneg_left hK16 hb4
    _ = 1 - β := h1
  have hβhalf : β ≤ 1 / 2 := by
    by_contra hcon
    have hcon' : (1:ℝ) / 2 < β := not_le.mp hcon
    have hb41 : (1/2:ℝ) ^ 4 ≤ β ^ 4 := pow_le_pow_left₀ (by norm_num) hcon'.le 4
    have hone : (1:ℝ) ≤ β ^ 4 * 16 := by
      have hv : (1/2:ℝ) ^ 4 * 16 = 1 := by norm_num
      calc (1:ℝ) = (1/2:ℝ) ^ 4 * 16 := hv.symm
        _ ≤ β ^ 4 * 16 := mul_le_mul_of_nonneg_right hb41 (by norm_num)
    linarith
  have h7 : (1/2:ℝ) ≤ 1 - β := by linarith
  have h2 : β ^ 4 = (1 - β) * (ME / M) ^ 2 := by
    rw [← h1]
    field_simp
  rw [h2]
  exact mul_le_mul_of_nonneg_right h7 (by positivity)

end

#print axioms quartic_beta_upper
#print axioms quartic_beta4_lower
