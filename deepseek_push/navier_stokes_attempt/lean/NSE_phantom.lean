import Mathlib

/-!
# NSE phantom-cusp rungs (N07_ACTION_DOOR.md): the D1 chain, certified algebra

Certifies the algebraic rungs of the action door's D1 (phantom) chain with
σ² = √(G·M_b·a0)/2, r_M = √(G·M_b/a0), M_ph(r) = 2σ²·r/G:
- `phantom_mass`: the phantom density field collapses to 2σ²/r
  (g_ph = G·M_ph/r² = 2σ²/r);
- `phantom_ratio`: g_ph/g_N = r/r_M (the phantom/Newtonian field ratio);
- `phantom_crossing`: at r = r_M the phantom field EQUALS the Newtonian
  field AND both equal a0 exactly;
- `phantom_cap`: the phantom's extra pull on baryons is bounded by a0/2
  (Lean-side restatement of `a0cap_bound` — proved directly here, same
  square-route);
- `phantom_subdominant`: inside r_M the phantom force is subdominant,
  g_ph/g_N ≤ 1.

Algebra only — physics scope: the a0-line is a MEASURED empirical law; Lean
certifies the mathematics of the law's consequences, not that nature obeys
it.  Zero `sorry`; Mathlib 4.34.0-rc2.
-/

noncomputable section

open Real

/-- The phantom product identity: √(x·a0) · √(x/a0) = x for x > 0, a0 > 0
(proved by the square-then-sqrt route with `sq_eq_sq₀`).  Used by
`phantom_ratio` and `phantom_crossing`. -/
theorem phantom_sqrt_product (Mb G a0 : ℝ) (hpos : 0 < G * Mb) (ha0 : 0 < a0) :
    Real.sqrt (G * Mb * a0) * Real.sqrt (G * Mb / a0) = G * Mb := by
  have hxa0 : 0 ≤ G * Mb * a0 := (mul_pos hpos ha0).le
  have hxda0 : 0 ≤ G * Mb / a0 := div_nonneg (le_of_lt hpos) (le_of_lt ha0)
  have hsq : (Real.sqrt (G * Mb * a0) * Real.sqrt (G * Mb / a0)) ^ 2 = (G * Mb) ^ 2 := by
    rw [mul_pow, Real.sq_sqrt hxa0, Real.sq_sqrt hxda0]
    field_simp [hpos.ne', ha0.ne']
  have hnn : 0 ≤ Real.sqrt (G * Mb * a0) * Real.sqrt (G * Mb / a0) :=
    mul_nonneg (Real.sqrt_nonneg _) (Real.sqrt_nonneg _)
  exact (sq_eq_sq₀ hnn hpos.le).mp hsq

/-- `phantom_mass`: with M_ph(r) = 2σ²·r/G the phantom density field
g_ph = G·M_ph/r² is exactly 2σ²/r.  Pure field algebra. -/
theorem phantom_mass (sigma2 r G : ℝ) (hr : r ≠ 0) (hG : G ≠ 0) :
    G * (2 * sigma2 * r / G) / r ^ 2 = 2 * sigma2 / r := by
  field_simp [hr, hG]

/-- `phantom_ratio`: g_ph/g_N = r/r_M.  From σ² = √(G·M_b·a0)/2 and
r_M = √(G·M_b/a0) the ratio (2σ²·r/(G·M_b)) / (G·M_b/r²) collapses to
2σ²·r/(G·M_b) = r·√(G·M_b·a0)/(G·M_b) = r/r_M.  The identity is
sign-agnostic in r (squares kill signs) — NO `0 ≤ r` hypothesis needed:
the r-free ratio identity √(x·a0)/x = 1/√(x/a0) holds for all a0 (for
a0 ≤ 0 both sides vanish, since Lean's real √ of a nonpositive number is 0
and division by zero is total). -/
theorem phantom_ratio (sigma2 Mb G a0 : ℝ) (r rM : ℝ) (hsigma : sigma2 = Real.sqrt (G * Mb * a0) / 2)
    (hrM : rM = Real.sqrt (G * Mb / a0)) (hpos : 0 < G * Mb) (hr : r ≠ 0) :
    (2 * sigma2 * r / (G * Mb)) = r / rM := by
  have _ := hr
  rw [hsigma, hrM]
  have h2 : 2 * (Real.sqrt (G * Mb * a0) / 2) = Real.sqrt (G * Mb * a0) := by ring
  rw [h2]
  by_cases ha0 : 0 < a0
  · have hC : Real.sqrt (G * Mb * a0) / (G * Mb) = 1 / Real.sqrt (G * Mb / a0) := by
      have hM : Real.sqrt (G * Mb * a0) * Real.sqrt (G * Mb / a0) = G * Mb :=
        phantom_sqrt_product Mb G a0 hpos ha0
      have htpos : 0 < Real.sqrt (G * Mb / a0) := Real.sqrt_pos.mpr (div_pos hpos ha0)
      field_simp [hpos.ne', ne_of_gt htpos]
      rw [div_eq_mul_inv, hM]
      exact mul_inv_cancel₀ hpos.ne'
    calc
      Real.sqrt (G * Mb * a0) * r / (G * Mb) = r * (Real.sqrt (G * Mb * a0) / (G * Mb)) := by ring
      _ = r * (1 / Real.sqrt (G * Mb / a0)) := by rw [hC]
      _ = r / Real.sqrt (G * Mb / a0) := by ring
  · have ha0le : a0 ≤ 0 := le_of_not_gt ha0
    have hs : Real.sqrt (G * Mb * a0) = 0 :=
      Real.sqrt_eq_zero_of_nonpos (mul_nonpos_of_nonneg_of_nonpos (le_of_lt hpos) ha0le)
    have htd : Real.sqrt (G * Mb / a0) = 0 :=
      Real.sqrt_eq_zero_of_nonpos (div_nonpos_of_nonneg_of_nonpos (le_of_lt hpos) ha0le)
    simp [hs, htd]

/-- `phantom_crossing`: at r = r_M the phantom field equals the Newtonian
field AND both equal a0 exactly.  EXTRA hypotheses vs. the door draft:
`hpos : 0 < G·M_b` and `ha0 : 0 < a0` were added as explicit arguments —
the statement is FALSE without them: if a0 < 0 or G·M_b ≤ 0 then
√(G·M_b/a0) = 0, so r = r_M = 0 and 2σ²/r = 0 ≠ a0 (Lean's √ of a
nonpositive number is 0 and division by zero is total). -/
theorem phantom_crossing (sigma2 Mb G a0 : ℝ) (r rM : ℝ) (hsigma : sigma2 = Real.sqrt (G * Mb * a0) / 2)
    (hrM : rM = Real.sqrt (G * Mb / a0)) (hr : r = rM) (hpos : 0 < G * Mb) (ha0 : 0 < a0) :
    2 * sigma2 / r = G * Mb / r ^ 2 ∧ 2 * sigma2 / r = a0 := by
  rw [hsigma, hr, hrM]
  have h1 : 2 * (Real.sqrt (G * Mb * a0) / 2) = Real.sqrt (G * Mb * a0) := by ring
  rw [h1]
  have hxa0 : 0 ≤ G * Mb * a0 := (mul_pos hpos ha0).le
  have hxda0 : 0 ≤ G * Mb / a0 := div_nonneg (le_of_lt hpos) (le_of_lt ha0)
  have hM : Real.sqrt (G * Mb * a0) * Real.sqrt (G * Mb / a0) = G * Mb :=
    phantom_sqrt_product Mb G a0 hpos ha0
  have htpos : 0 < Real.sqrt (G * Mb / a0) := Real.sqrt_pos.mpr (div_pos hpos ha0)
  have htnz : Real.sqrt (G * Mb / a0) ≠ 0 := ne_of_gt htpos
  constructor
  · field_simp [htnz, pow_ne_zero 2 htnz]
    exact hM
  · have hsq2 : (Real.sqrt (G * Mb * a0) / Real.sqrt (G * Mb / a0)) ^ 2 = a0 ^ 2 := by
      rw [div_pow, Real.sq_sqrt hxa0, Real.sq_sqrt hxda0]
      field_simp [hpos.ne', ha0.ne']
      rw [div_eq_mul_inv]
      exact mul_inv_cancel₀ hpos.ne'
    have hsn0 : 0 ≤ Real.sqrt (G * Mb * a0) / Real.sqrt (G * Mb / a0) :=
      div_nonneg (Real.sqrt_nonneg _) (le_of_lt htpos)
    exact (sq_eq_sq₀ hsn0 ha0.le).mp hsq2

/-- `phantom_cap`: the phantom's extra force on baryons is capped at a0/2,
√(g_N² + a0·g_N) − g_N ≤ a0/2 (the Lean-side restatement of `a0cap_bound`,
proved directly here by the same square-route). -/
theorem phantom_cap (gN a0 : ℝ) (hg : 0 ≤ gN) (ha : 0 ≤ a0) :
    Real.sqrt (gN ^ 2 + a0 * gN) - gN ≤ a0 / 2 := by
  have hrad : 0 ≤ gN ^ 2 + a0 * gN := by nlinarith [sq_nonneg gN, mul_nonneg ha hg]
  have hrel : (gN + a0 / 2) ^ 2 = gN ^ 2 + a0 * gN + a0 ^ 2 / 4 := by ring
  have ha24 : 0 ≤ a0 ^ 2 / 4 := by positivity
  have hsq : (Real.sqrt (gN ^ 2 + a0 * gN)) ^ 2 ≤ (gN + a0 / 2) ^ 2 := by
    rw [Real.sq_sqrt hrad, hrel]
    nlinarith [ha24]
  have hs0 : 0 ≤ Real.sqrt (gN ^ 2 + a0 * gN) := Real.sqrt_nonneg _
  have ht0 : 0 ≤ gN + a0 / 2 := by positivity
  have hle : Real.sqrt (gN ^ 2 + a0 * gN) ≤ gN + a0 / 2 := by
    simpa [abs_of_nonneg hs0, abs_of_nonneg ht0] using sq_le_sq.mp hsq
  linarith

/-- `phantom_subdominant`: inside r_M the phantom force on baryons is
subdominant: g_ph/g_N = 2σ²·r/(G·M_b) ≤ 1.  From `phantom_ratio` the ratio
is r/r_M ≤ 1; the closed branch (a0 ≤ 0) forces r = 0 via total division.
The `0 ≤ r` hypothesis is used exactly here (to pin r through r/r_M). -/
theorem phantom_subdominant (sigma2 Mb G a0 : ℝ) (r rM : ℝ) (hsigma : sigma2 = Real.sqrt (G * Mb * a0) / 2)
    (hrM : rM = Real.sqrt (G * Mb / a0)) (hr : 0 ≤ r) (hrrM : r ≤ rM) (hpos : 0 < G * Mb) :
    2 * sigma2 * r / (G * Mb) ≤ 1 := by
  by_cases ha0 : 0 < a0
  · have hrMpos : 0 < rM := by
      rw [hrM]
      exact Real.sqrt_pos.mpr (div_pos hpos ha0)
    by_cases hr0 : r = 0
    · simp [hr0]
    · have hratio := phantom_ratio sigma2 Mb G a0 r rM hsigma hrM hpos hr0
      rw [hratio]
      rw [div_le_iff₀ hrMpos]
      simpa using hrrM
  · have ha0le : a0 ≤ 0 := le_of_not_gt ha0
    have hrMz : rM = 0 := by
      rw [hrM]
      exact Real.sqrt_eq_zero_of_nonpos (div_nonpos_of_nonneg_of_nonpos (le_of_lt hpos) ha0le)
    have hr0 : r = 0 := by nlinarith [hr, hrrM, hrMz]
    simp [hr0]

end

#print axioms phantom_sqrt_product
#print axioms phantom_mass
#print axioms phantom_ratio
#print axioms phantom_crossing
#print axioms phantom_cap
#print axioms phantom_subdominant