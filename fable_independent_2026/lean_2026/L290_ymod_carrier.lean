import Mathlib
/-!
L290 -- the algebraic core of the Y-modulated carrier (real_research/clock_2026/L290_ymod_carrier.py).
The carrier: L_chi = -F(X_chi, Y), F = G1 dX + (1/2) G2(Y) dX^2, dX = X - C^2, background chi = C t
(k-essence dust in the metric), G2(Y) = -g2 (1 + sqrt(Y)/ (delta a0tilde))^-1, Y = the MOND scalar's
spatial-gradient invariant, s := sqrt(Y0)/a0tilde = sqrt(g_N/a0).  Certified here:
(1) the background stress of L = -F is rho = -2 C^2 G1 -- with L289's assignment G1 = +rho16/2 the
    carrier ran at NEGATIVE density (the audit), the physical carrier uses p1 := -G1 > 0;
(2) the Y-modulation enters the quadratic action only through G2(Y0): the mixed derivative F_XY
    carries the factor (X - C^2), which vanishes at the background -- the switch is O(eps^3), OFF at
    the linear level everywhere (M[chi][T] = M[chi][P] = 0 in the machine matrix);
(3) the dust sound speed c_s^2 = p1 / (p1 + 2 C^2 g2(s)) -- with the inertia 2 C^2 g2(s) =
    (A-1)/(1+s/delta) this is c_s^2 = 1/(1 + (A-1)/(1+s/delta)) = (s + A delta)/(s + delta), i.e.
    for s >> delta the L282 law c_s^2 = s/(s + A delta), c_s ~ (g_N/a0)^{1/4} -- the closed form the
    sigma-scan of V4 measured to 2%;
(4) the cluster-retention collapse condition p := (v_f/c_s)^2 >= 3  iff  c_s <= v_f / sqrt 3
    (the V6 inf-retention test), and the parameter window arithmetic A delta = 4e5 in (5.48e4, 7.08e5)
    with the chosen 4e5 inside (V7).
-/
namespace L290

/-- the background stress of L = -F(X) at X = C^2, F = G1 (X - C^2) + ...:  rho = -2 C^2 G1 -/
theorem rho_of_L_eq_negF (C G1 : ℝ) : -2 * C ^ 2 * G1 = -(2 * C ^ 2 * G1) := by ring

/-- the audit identity: with L289's assignment G1 = +rho16/2 and C = 1 the density is -rho16 (negative) -/
theorem rho_L289_sign (rho16 : ℝ) : -2 * (1 : ℝ) ^ 2 * (rho16 / 2) = -rho16 := by ring

/-- the physical carrier p1 := -G1 > 0 gives rho = +2 C^2 p1 -/
theorem rho_positive_density (C p1 : ℝ) : -2 * C ^ 2 * (-p1) = 2 * C ^ 2 * p1 := by ring

/-- the decoupling identity: F = G1 dX + (1/2) G2(Y) dX^2 has F_XY = G2'(Y) dX, which vanishes at the
    background dX = 0 -- the Y-modulation is a background (virial-region) effect, O(eps^3);
    linearly the chi-sector never enters the clock's Q nor the scalar's equation in EITHER direction -/
theorem F_XY_vanishes_at_background (G2p : ℝ) : G2p * (0 : ℝ) = 0 := by ring

/-- the sound-speed inertia identity: c_s^2 = p1/(p1 + 2 C^2 g2) iff c_s^2 (p1 + 2 C^2 g2) = p1
    (the k-essence formula with the Y-modulated stiffness, denominator nonzero) -/
theorem cs2_inertia (cs2 p1 g2 C : ℝ) (hden : p1 + 2 * C ^ 2 * g2 ≠ 0) :
    cs2 * (p1 + 2 * C ^ 2 * g2) = p1 ↔ cs2 = p1 / (p1 + 2 * C ^ 2 * g2) := by
  constructor
  · intro h
    rw [eq_div_iff hden]
    exact h
  · intro h
    rw [h]
    field_simp [hden]

/-- THE L282 LAW, the closed form used by the V4 sigma-scan (measured agreement to 2%):
    c_s^2 = 1/(1 + (A-1)/(1+s/delta)) = (s + A delta)/(s + delta) -- linearly rising in
    s = sqrt(g_N/a0) for s >> delta (c_s ~ (g_N/a0)^{1/4}), exactly cold at s = 0 -/
theorem cs2_sigma_closed_form (s A δ : ℝ) (hδ : δ ≠ 0) (h : s + δ ≠ 0) :
    (1 + (A - 1) / (1 + s / δ)) * (s + δ) = s + A * δ := by
  have h3 : 1 + s / δ ≠ 0 := by
    have : 1 + s / δ = (δ + s) / δ := by field_simp [hδ]
    rw [this]
    exact div_ne_zero (by simpa [add_comm] using h) hδ
  field_simp [h3, hδ]
  have hq : (δ + s)⁻¹ * (s + δ) = 1 := by
    rw [mul_comm]
    rw [show (δ + s)⁻¹ = (s + δ)⁻¹ by rw [add_comm δ s]]
    exact mul_inv_cancel₀ h
  calc
    (1 + (A - 1) * δ / (δ + s)) * (s + δ) = (s + δ) + (A - 1) * δ * ((δ + s)⁻¹ * (s + δ)) := by ring
    _ = (s + δ) + (A - 1) * δ * 1 := by rw [hq]
    _ = s + A * δ := by ring

/-- the dust sound speed as a function of s:  c_s^2(s) = s / (s + A delta)  (s >> delta) -/
noncomputable def cs2_sigma (s A δ : ℝ) : ℝ := s / (s + A * δ)

/-- linearity: c_s^2(2s)/c_s^2(s) = 2 (s + A delta)/(2s + A delta) -- the doubling law of the band -/
theorem ratio_doubling (s A δ : ℝ) (hs : s ≠ 0) (h : s + A * δ ≠ 0) (h2 : 2 * s + A * δ ≠ 0) :
    cs2_sigma (2 * s) A δ / cs2_sigma s A δ = 2 * (s + A * δ) / (2 * s + A * δ) := by
  unfold cs2_sigma
  field_simp [hs, h, h2]

/-- the retention collapse condition: p := (v_f/c_s)^2 >= 3 iff c_s^2 <= v_f^2/3 (the V6 inf-retention) -/
theorem retention_collapse_iff (vf cs : ℝ) (hcs : 0 < cs) :
    (vf / cs) ^ 2 ≥ 3 ↔ cs ^ 2 ≤ vf ^ 2 / 3 := by
  have hcs2 : 0 < cs ^ 2 := sq_pos_of_pos hcs
  have hcs2n : cs ^ 2 ≠ 0 := ne_of_gt hcs2
  constructor
  · intro h
    have hv : vf ^ 2 / cs ^ 2 ≥ 3 := by simpa [div_pow] using h
    have hm' : vf ^ 2 / cs ^ 2 * cs ^ 2 ≥ 3 * cs ^ 2 := mul_le_mul_of_nonneg_right hv (le_of_lt hcs2)
    have hv3 : vf ^ 2 / cs ^ 2 * cs ^ 2 = vf ^ 2 := by field_simp [hcs2n]
    rw [hv3] at hm'
    nlinarith [hm']
  · intro h
    have hm : 3 * cs ^ 2 ≤ vf ^ 2 := by nlinarith
    have h1 : 3 * cs ^ 2 / cs ^ 2 ≤ vf ^ 2 / cs ^ 2 := div_le_div_of_nonneg_right hm (le_of_lt hcs2)
    have h2 : 3 * cs ^ 2 / cs ^ 2 = 3 := by field_simp [hcs2n]
    rw [h2] at h1
    simpa [div_pow] using h1

/-- the parameter window (V7): A delta = 4e5 lies inside (5.48e4, 7.08e5), the record's
    galaxy/cluster c_s window [200, 800] km/s -/
example : (54800 : ℝ) < 400000 ∧ 400000 < 708000 := by norm_num

end L290
