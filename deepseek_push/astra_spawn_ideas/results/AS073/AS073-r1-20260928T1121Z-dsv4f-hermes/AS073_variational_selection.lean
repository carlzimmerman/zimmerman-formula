import Mathlib

/-! AS073 -- Coefficient selection by a variational principle: algebraic certificates.

Part A (L230 matching chain): if a deep response has slope n at the origin (in the
vacuum units Y = g/s, s = c sqrt(G rho_Lambda)), the spherical point-mass deep-MOND
matching gives g^2 = (s/n) g_N, hence a0 = s/n and kappa = a0/s = 1/n.  The slope,
not the action, carries the coefficient: kappa is exactly the reciprocal of the
deep slope.  (This is the algebra that turns the seed's diagnostic counterexamples
with slopes 1/2, 1 and 2 into kappa values 2, 1 and 1/2.)

Part B (diagnostic family): for every lambda > 0 the function
    mu_lam(Y) = 1 - exp(-lambda * log(1+Y))
is admissible for the endpoint-fixed variational problem: mu_lam(0) = 0,
mu_lam(Y) -> 1 as Y -> oo, 0 <= mu_lam <= 1, and its deep slope at Y = 0 is exactly
lambda.  Hence the endpoint data carry NO slope information: slopes 1/2, 1, 2 all
realize the same endpoints, and any endpoint-fixed variational selection that is
scale-covariant (Part A of the derivation) leaves the slope -- and kappa -- free.
-/

noncomputable section
open scoped Real Topology
open Filter

-- ================= Part A: kappa = 1 / (deep slope) =================

/-- The matched deep acceleration g = sqrt((s/n) * g_N) satisfies g^2 = (s/n) * g_N. -/
theorem deep_g_squared (s n gN : ℝ) (hs : 0 < s) (hn : 0 < n) (hgN : 0 < gN) :
    (Real.sqrt ((s / n) * gN)) ^ 2 = (s / n) * gN := by
  rw [pow_two, Real.mul_self_sqrt]
  exact mul_nonneg (le_of_lt (div_pos hs hn)) (le_of_lt hgN)

/-- Physical form: g_N = G M / r^2 with G, M, r > 0. -/
theorem deep_mond_point_mass (s n G M r : ℝ) (hs : 0 < s) (hn : 0 < n) (hG : 0 < G)
    (hM : 0 < M) (hr : 0 < r) :
    let gN := G * M / r ^ 2
    let g := Real.sqrt ((s / n) * gN)
    g ^ 2 = (s / n) * gN := by
  dsimp
  rw [pow_two, Real.mul_self_sqrt]
  exact mul_nonneg (le_of_lt (div_pos hs hn))
    (le_of_lt (div_pos (mul_pos hG hM) (sq_pos_of_pos hr)))

/-- The a0-line matching is unique: if a0 * g_N = (s/n) * g_N then a0 = s/n. -/
theorem a0_unique (s n a0 gN : ℝ) (hgN : gN ≠ 0) (h : a0 * gN = (s / n) * gN) :
    a0 = s / n := by
  exact mul_left_cancel₀ hgN (by simpa [mul_comm] using h)

/-- kappa = a0/s = 1/n: the coefficient is the reciprocal of the deep slope. -/
theorem kappa_eq_one_div_slope (s n : ℝ) (hs : s ≠ 0) (hn : n ≠ 0) :
    (s / n) / s = 1 / n := by
  field_simp [hs, hn]

-- ================= Part B: the diagnostic family =================

/-- mu_lam(Y) = 1 - exp(-lambda * log(1+Y)), the diagnostic member with slope lambda. -/
def muLam (lam Y : ℝ) : ℝ := 1 - Real.exp (-lam * Real.log (1 + Y))

/-- Endpoint at zero: mu_lam(0) = 0 for every lambda. -/
theorem muLam_zero (lam : ℝ) : muLam lam 0 = 0 := by
  unfold muLam
  simp

/-- Range lower bound: 0 <= mu_lam(Y) for Y >= 0 and lambda > 0. -/
theorem muLam_nonneg (lam Y : ℝ) (hlam : 0 < lam) (hY : 0 ≤ Y) : 0 ≤ muLam lam Y := by
  unfold muLam
  have hlog : 0 ≤ Real.log (1 + Y) := by
    exact Real.log_nonneg (by linarith)
  have hle : -lam * Real.log (1 + Y) ≤ 0 := by
    nlinarith [mul_nonneg (le_of_lt hlam) hlog]
  have hexp_le : Real.exp (-lam * Real.log (1 + Y)) ≤ 1 := by
    simpa using (Real.exp_le_exp.mpr hle)
  linarith [hexp_le, le_of_lt (Real.exp_pos (-lam * Real.log (1 + Y)))]

/-- Range upper bound: mu_lam(Y) <= 1 for every lambda and Y. -/
theorem muLam_le_one (lam Y : ℝ) : muLam lam Y ≤ 1 := by
  unfold muLam
  have hp : 0 ≤ Real.exp (-lam * Real.log (1 + Y)) := le_of_lt (Real.exp_pos _)
  linarith

/-- Deep slope at the origin is exactly lambda for every lambda > 0. -/
theorem muLam_hasDerivAt_zero (lam : ℝ) :
    HasDerivAt (fun Y : ℝ => muLam lam Y) lam 0 := by
  unfold muLam
  have hc : HasDerivAt (fun Y : ℝ => 1 + Y) 1 0 := by
    exact (hasDerivAt_id (0 : ℝ)).const_add (1 : ℝ)
  have hlogd : HasDerivAt (fun Y : ℝ => Real.log (1 + Y)) 1 0 := by
    simpa [one_div] using hc.log (by norm_num : (1 + (0 : ℝ)) ≠ 0)
  have hinner : HasDerivAt (fun Y : ℝ => -lam * Real.log (1 + Y)) (-lam) 0 := by
    simpa using hlogd.const_mul (-lam)
  have hexp : HasDerivAt (fun Y : ℝ => Real.exp (-lam * Real.log (1 + Y))) (-lam) 0 := by
    simpa using hinner.exp
  have hmain : HasDerivAt (fun Y : ℝ => 1 - Real.exp (-lam * Real.log (1 + Y))) (0 - (-lam)) 0 := by
    exact (hasDerivAt_const (x := (0 : ℝ)) (c := (1 : ℝ))).sub hexp
  simpa [muLam] using hmain

/-- Diagnostic members: slopes 1/2, 1 and 2 (the seed's lambda = 1/2, 1, 2). -/
theorem muLam_slope_half : HasDerivAt (fun Y : ℝ => muLam (1 / 2) Y) (1 / 2) 0 := by
  simpa using muLam_hasDerivAt_zero (1 / 2)

theorem muLam_slope_one : HasDerivAt (fun Y : ℝ => muLam 1 Y) 1 0 := by
  simpa using muLam_hasDerivAt_zero 1

theorem muLam_slope_two : HasDerivAt (fun Y : ℝ => muLam 2 Y) 2 0 := by
  simpa using muLam_hasDerivAt_zero 2

/-- The three diagnostic slopes are pairwise distinct: the endpoints do not pin
    the slope, so they cannot pin kappa = 1/slope. -/
theorem slopes_distinct : (1 / 2 : ℝ) ≠ 1 ∧ (1 : ℝ) ≠ 2 ∧ (1 / 2 : ℝ) ≠ 2 := by
  norm_num

/-- Newtonian endpoint: mu_lam(Y) -> 1 as Y -> +infinity for lambda > 0. -/
theorem muLam_tendsto_atTop (lam : ℝ) (hlam : 0 < lam) :
    Tendsto (fun Y : ℝ => muLam lam Y) atTop (𝓝 1) := by
  unfold muLam
  have hplus : Tendsto (fun Y : ℝ => 1 + Y) atTop atTop := by
    rw [tendsto_atTop]
    intro B
    exact (eventually_ge_atTop (B - 1)).mono (fun y hy => by linarith)
  have hlog : Tendsto (fun Y : ℝ => Real.log (1 + Y)) atTop atTop :=
    Real.tendsto_log_atTop.comp hplus
  have hlog' : ∀ b : ℝ, ∀ᶠ Y in atTop, b ≤ Real.log (1 + Y) := by
    rw [tendsto_atTop] at hlog
    exact hlog
  have hlin : Tendsto (fun Y : ℝ => lam * Real.log (1 + Y)) atTop atTop := by
    rw [tendsto_atTop]
    intro B
    exact (hlog' (B / lam)).mono (fun y hy => by
      have hmul : (B / lam) * lam ≤ Real.log (1 + y) * lam :=
        mul_le_mul_of_nonneg_right hy (le_of_lt hlam)
      calc
        B = (B / lam) * lam := by rw [div_mul_cancel₀ B (ne_of_gt hlam)]
        _ ≤ Real.log (1 + y) * lam := hmul
        _ = lam * Real.log (1 + y) := by rw [mul_comm])
  have hlin' : ∀ b : ℝ, ∀ᶠ Y in atTop, b ≤ lam * Real.log (1 + Y) := by
    rw [tendsto_atTop] at hlin
    exact hlin
  have hneg : Tendsto (fun Y : ℝ => -(lam * Real.log (1 + Y))) atTop atBot := by
    rw [tendsto_atBot]
    intro B
    exact (hlin' (-B)).mono (fun y hy => by linarith)
  have hexp : Tendsto (fun Y : ℝ => Real.exp (-(lam * Real.log (1 + Y)))) atTop (𝓝 0) :=
    Real.tendsto_exp_atBot.comp hneg
  have hmain : Tendsto (fun Y : ℝ => 1 - Real.exp (-(lam * Real.log (1 + Y)))) atTop (𝓝 (1 - 0)) :=
    tendsto_const_nhds.sub hexp
  simpa [neg_mul] using hmain

-- ================= axiom ledger (unfiltered) =================
#print axioms deep_g_squared
#print axioms deep_mond_point_mass
#print axioms a0_unique
#print axioms kappa_eq_one_div_slope
#print axioms muLam_zero
#print axioms muLam_nonneg
#print axioms muLam_le_one
#print axioms muLam_hasDerivAt_zero
#print axioms muLam_slope_half
#print axioms muLam_slope_one
#print axioms muLam_slope_two
#print axioms slopes_distinct
#print axioms muLam_tendsto_atTop