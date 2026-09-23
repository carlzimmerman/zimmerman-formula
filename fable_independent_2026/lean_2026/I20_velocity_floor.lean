import Mathlib

/-!
# I20 — The velocity floor: around an isolated point mass the framework's circular speed never
# drops below v_flat = (G M a0)^{1/4}

SCOPE (per lean-math-certification): Lean certifies the MATHEMATICS. Physics inputs (an isolated point mass,
no external field; circular orbits; the kernel) are hypotheses. Companion lane:
`real_research/bhstar_audit_2026/L327_qso1_cube_refit.py`.

* `one_sub_exp_neg_le` — 1 − e^{−t} ≤ t for all t (the only analytic input).
* `nuRAR_ge_inv_sqrt` — the framework's RAR kernel satisfies ν(y) ≥ 1/√y for y > 0.
* `velocity_floor_rar` — hence, for every r > 0, v_c(r)² = (GM/r)·ν(GM/(r²a0)) ≥ √(G M a0) = v_flat²:
  **no circular orbit around an isolated point mass is slower than (G M a0)^{1/4}**. Newton has no floor
  (GM/r → 0), so a resolved circular speed below v_flat at any radius falsifies the framework (given M, no EFE).
* `velocity_floor_mu` — the same floor for ANY interpolating function with μ(x) ≤ x (simple, exp-μ, …):
  if x·μ(x) = y (x = g/a0, y = g_N/a0) and μ(x) ≤ x then x ≥ √y, i.e. g ≥ √(g_N a0).
* `floor_value_qso1` — for A2744-QSO1 (M = 5.01e7 Msun, canonical a0) the floor exceeds 27.9 km/s.

Zero `sorry`; axioms ⊆ {propext, Classical.choice, Quot.sound}.
-/

noncomputable section

open Real

noncomputable def nuRAR (y : ℝ) : ℝ := 1 / (1 - Real.exp (-Real.sqrt y))

theorem one_sub_exp_neg_le (t : ℝ) : 1 - Real.exp (-t) ≤ t := by
  have := Real.add_one_le_exp (-t)
  linarith

theorem nuRAR_ge_inv_sqrt {y : ℝ} (hy : 0 < y) : 1 / Real.sqrt y ≤ nuRAR y := by
  have hs : 0 < Real.sqrt y := Real.sqrt_pos.mpr hy
  have hd : 0 < 1 - Real.exp (-Real.sqrt y) := by
    have : Real.exp (-Real.sqrt y) < 1 := by
      have := Real.exp_lt_exp.mpr (show -Real.sqrt y < 0 by linarith)
      rwa [Real.exp_zero] at this
    linarith
  unfold nuRAR
  exact one_div_le_one_div_of_le hd (one_sub_exp_neg_le _)

/-- The floor: (GM/r)·ν(GM/(r² a0)) ≥ √(G M a0) for every r > 0. -/
theorem velocity_floor_rar {G M a0 r : ℝ} (hG : 0 < G) (hM : 0 < M) (ha : 0 < a0) (hr : 0 < r) :
    Real.sqrt (G * M * a0) ≤ G * M / r * nuRAR (G * M / (r ^ 2 * a0)) := by
  have hy : 0 < G * M / (r ^ 2 * a0) := by positivity
  have h1 := nuRAR_ge_inv_sqrt hy
  have hsq : Real.sqrt (G * M / (r ^ 2 * a0)) = Real.sqrt (G * M / a0) / r := by
    have h : G * M / (r ^ 2 * a0) = (G * M / a0) / r ^ 2 := by field_simp
    rw [h, Real.sqrt_div (by positivity), Real.sqrt_sq hr.le]
  have hGMr : 0 < G * M / r := by positivity
  have key : G * M / r * (1 / Real.sqrt (G * M / (r ^ 2 * a0))) = Real.sqrt (G * M * a0) := by
    rw [hsq]
    have hs : 0 < Real.sqrt (G * M / a0) := Real.sqrt_pos.mpr (by positivity)
    have hprod : Real.sqrt (G * M / a0) * Real.sqrt (G * M * a0) = G * M := by
      rw [← Real.sqrt_mul (by positivity)]
      have : G * M / a0 * (G * M * a0) = (G * M) ^ 2 := by field_simp
      rw [this, Real.sqrt_sq (by positivity)]
    field_simp
    nlinarith [hprod]
  calc Real.sqrt (G * M * a0) = G * M / r * (1 / Real.sqrt (G * M / (r ^ 2 * a0))) := key.symm
    _ ≤ G * M / r * nuRAR (G * M / (r ^ 2 * a0)) := mul_le_mul_of_nonneg_left h1 hGMr.le

/-- Any kernel with μ(x) ≤ x: from x·μ(x) = y and μ(x) ≤ x (x ≥ 0) follows x ≥ √y. -/
theorem velocity_floor_mu {x y mu : ℝ} (hx : 0 ≤ x) (hy : 0 ≤ y) (hdef : x * mu = y) (hmu : mu ≤ x) :
    Real.sqrt y ≤ x := by
  have : y ≤ x ^ 2 := by nlinarith
  calc Real.sqrt y ≤ Real.sqrt (x ^ 2) := Real.sqrt_le_sqrt this
    _ = x := Real.sqrt_sq hx

/-- QSO1: v_flat⁴ = G M a0 at M = 5.01e7 Msun, canonical a0 — the floor exceeds 27.9 km/s. -/
theorem floor_value_qso1 :
    (27.9e3 : ℝ) ^ 4 < 6.6743e-11 * (5.01e7 * 1.98892e30) * 9.3619e-11 := by
  norm_num

end

#print axioms one_sub_exp_neg_le
#print axioms nuRAR_ge_inv_sqrt
#print axioms velocity_floor_rar
#print axioms velocity_floor_mu
#print axioms floor_value_qso1
