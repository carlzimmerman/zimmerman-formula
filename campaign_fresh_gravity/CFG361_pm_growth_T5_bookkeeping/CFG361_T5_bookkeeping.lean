import Mathlib
/-! CFG361: B's max bookkeeping (CFG4 T5) vs additive gravity on the PM mesh.  Criteria 6373544c3.
Pointwise lemmas only; the sigma8 interval certificates are appended from cfg361_pm_growth_T5_results.json. -/

/-- T5 identity: the dark density max(phantom, cold) never exceeds the additive sum when both are non-negative. -/
theorem max_le_sum (p c : ℝ) (hp : 0 ≤ p) (hc : 0 ≤ c) : max p c ≤ p + c :=
  max_le (by linarith) (by linarith)

/-- T5-local extra source f·max(s_ph − s_c, 0) ≤ additive f·s_ph where the phantom density is non-negative. -/
theorem t5_le_add (f p c : ℝ) (hf0 : 0 ≤ f) (hp : 0 ≤ p) (hc : 0 ≤ c) :
    f * max (p - c) 0 ≤ f * p :=
  mul_le_mul_of_nonneg_left (max_le (by linarith) hp) hf0

/-- Where the phantom density is negative, T5 adds nothing while additive subtracts: T5 ≥ additive there. -/
theorem t5_ge_add_neg (f p c : ℝ) (hf0 : 0 ≤ f) (hp : p < 0) (_hc : 0 ≤ c) :
    f * p ≤ f * max (p - c) 0 :=
  mul_le_mul_of_nonneg_left (le_trans (le_of_lt hp) (le_max_right _ _)) hf0

/-- In an ON cell (f = 1) the T5 total source equals baryons + max(phantom, cold). -/
theorem t5_on_cell (b p c : ℝ) : b + c + max (p - c) 0 = b + max p c := by
  rcases le_total c p with h | h
  · rw [max_eq_left (by linarith), max_eq_left h]; ring
  · rw [max_eq_right (by linarith), max_eq_right h]; ring

/-- Force analogue: f_b·max(ν − 1/f_b, 0) ≤ f_b·(ν − 1) for ν ≥ 1 and 0 < f_b ≤ 1. -/
theorem t5f_le_add (fb nu : ℝ) (h0 : 0 < fb) (h1 : fb ≤ 1) (hnu : 1 ≤ nu) :
    fb * max (nu - 1 / fb) 0 ≤ fb * (nu - 1) := by
  have h : 1 ≤ 1 / fb := by rw [le_div_iff₀ h0]; linarith
  exact mul_le_mul_of_nonneg_left (max_le (by linarith) (by linarith)) h0.le

/-! sigma8 ratio certificates (z = 0, T5-local, A0-FLAT; cfg361_pm_growth_T5_results.json).  The FAIL cut is
|ratio - 1| > 1/5.  Canonical: 1.2049 in [1.2045, 1.2055]; alt: 1.2573 in [1.2570, 1.2580]. -/
theorem t5_flat_canonical_fail (r : ℝ) (h1 : (12045:ℝ)/10000 ≤ r) (_h2 : r ≤ (12055:ℝ)/10000) : 1/5 < |r - 1| := by
  rw [abs_of_pos (by linarith)]; linarith
theorem t5_flat_alt_fail (r : ℝ) (h1 : (12570:ℝ)/10000 ≤ r) (_h2 : r ≤ (12580:ℝ)/10000) : 1/5 < |r - 1| := by
  rw [abs_of_pos (by linarith)]; linarith
/-- T5 sits strictly below additive on both footings (measured): canonical 1.2049 < 1.5815, alt 1.2573 < 1.6452. -/
theorem t5_below_add : (12055:ℝ)/10000 < 15815/10000 ∧ (12580:ℝ)/10000 < 16452/10000 := by norm_num

/-! Final certificates (all 21 runs; cfg361_pm_growth_T5_results.json).  FAIL cut |ratio - 1| > 1/5.
T5 CRIT 1.5025 / 1.5929; S FLAT 1.1938 / 1.2489 (S canonical alone is TENSION side: certified below 1/5);
S CRIT 1.4905 / 1.5834.  K4: T5 FLAT canonical 128^3 = 1.1510 (TENSION side), 256^3 = 1.2049 (FAIL side). -/
theorem t5_crit_canonical_fail (r : ℝ) (h1 : (15020:ℝ)/10000 ≤ r) (_h2 : r ≤ (15030:ℝ)/10000) : 1/5 < |r - 1| := by
  rw [abs_of_pos (by linarith)]; linarith
theorem t5_crit_alt_fail (r : ℝ) (h1 : (15925:ℝ)/10000 ≤ r) (_h2 : r ≤ (15935:ℝ)/10000) : 1/5 < |r - 1| := by
  rw [abs_of_pos (by linarith)]; linarith
theorem s_flat_canonical_tension_side (r : ℝ) (_h1 : (11935:ℝ)/10000 ≤ r) (h2 : r ≤ (11945:ℝ)/10000) (h3 : 1 ≤ r) : |r - 1| ≤ 1/5 := by
  rw [abs_of_nonneg (by linarith)]; linarith
theorem s_flat_alt_fail (r : ℝ) (h1 : (12485:ℝ)/10000 ≤ r) (_h2 : r ≤ (12495:ℝ)/10000) : 1/5 < |r - 1| := by
  rw [abs_of_pos (by linarith)]; linarith
theorem s_crit_canonical_fail (r : ℝ) (h1 : (14900:ℝ)/10000 ≤ r) (_h2 : r ≤ (14910:ℝ)/10000) : 1/5 < |r - 1| := by
  rw [abs_of_pos (by linarith)]; linarith
theorem s_crit_alt_fail (r : ℝ) (h1 : (15830:ℝ)/10000 ≤ r) (_h2 : r ≤ (15840:ℝ)/10000) : 1/5 < |r - 1| := by
  rw [abs_of_pos (by linarith)]; linarith
/-- K4: the 128^3 ratio is on the TENSION side, the 256^3 on the FAIL side; higher resolution gives MORE excess. -/
theorem k4_resolution_trend (r128 r256 : ℝ) (h1 : r128 ≤ (11515:ℝ)/10000) (h2 : (12045:ℝ)/10000 ≤ r256) (h0 : 1 ≤ r128) :
    |r128 - 1| ≤ 1/5 ∧ 1/5 < |r256 - 1| ∧ r128 < r256 := by
  refine ⟨?_, ?_, by linarith⟩
  · rw [abs_of_nonneg (by linarith)]; linarith
  · rw [abs_of_pos (by linarith)]; linarith
