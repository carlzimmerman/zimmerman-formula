/-
DP3: Lean statements for the algebra of the Gaia DR4 scoring rows that lane DP3_release_day applies
(dr4_push_2026_11_05/DP3_release_day: dr4_outcome_map.py, RELEASE_DAY_RUNBOOK_DR4.md section 2), taken from
prep_2026/gaia_dr4_prep/NOTE_2026-10-22_FORK_SCORING_PRE_DR4.md (the D2 rows, A1-A3),
prep_2026/gaia_dr4_prep/OWNER_DECISION_2026-11-05_DR4_FORKS.md (sections 2 and 3) and the R rule of
campaign_fresh_gravity/CFG816_dr4_r_statistic_scoring/cfg816_r.py (classify). They certify the algebra, not the physics,
and no number or label of the lane; the constants are the frozen ones the files give. TEST lane; adopts nothing.

Notation: sigma = sqrt(sigma_fit^2 + sigma_sys^2); law-first excluded: anchor - g >= 3 sigma; screened excluded:
g - 1 >= 3 sigma; sub-Newton: g <= 1 - 3 sigma (D4); R KILLED: R - 1 >= 0.01 and R - 1 >= 3 sigma_R; R CONSISTENT:
|R - 1| < 0.01 and 2 sigma_R <= 0.01.

  sigma_parts             : sigma^2 = sigma_fit^2 + sigma_sys^2 and sigma >= |sigma_fit|, sigma >= |sigma_sys|.
  sigma_fit_scaling       : sigma_fit = 0.019 sqrt(30000/N): sigma_fit^2 N = 0.019^2 x 30000, and sigma_fit does not
                            increase with N.
  sigma_monotone_sys      : sigma does not decrease when sigma_sys grows, so a verdict row that holds at the larger
                            sigma holds at the smaller (a larger sigma_sys only moves outcomes toward UNDECIDED, A1).
  row_edges               : the two exclusion rows are exactly g <= anchor - 3 sigma and g >= 1 + 3 sigma.
  both_iff                : some g satisfies both rows (BOTH EXCLUDED, D5) iff anchor - 1 >= 6 sigma.
  no_gap                  : if anchor - 1 >= 6 sigma, every g satisfies at least one row (no UNDECIDED band).
  undecided_gap           : neither row holds iff anchor - 3 sigma < g < 1 + 3 sigma; when anchor - 1 < 6 sigma that
                            band has width 6 sigma - (anchor - 1) > 0.
  subnewton_excludes      : for sigma > 0 the sub-Newton row excludes the screened row, and (anchor >= 1) it lies inside
                            the law-first row, which is why it is evaluated first; at sigma = 0, g = 1 meets both
                            the sub-Newton and the screened conditions (sigma > 0 is needed).
  three_sigma_sq          : for d, s >= 0: 3 s <= d iff 9 s^2 <= d^2 (the edges below are proved on squares).
  registered_sigma        : sigma^2 = 0.019^2 + 0.020^2 gives 0.02758 <= sigma <= 0.02759 and 0.0827 <= 3 sigma <= 0.0828.
  registered_edges        : at that sigma: canonical law-first edge 1.1614 - 3 sigma in [1.0786, 1.0787], screened edge
                            1 + 3 sigma in [1.0827, 1.0828], sub-Newton edge in [0.9172, 0.9173], alt law-first edge
                            1.1917 - 3 sigma in [1.1089, 1.1090]; canonical leaves an UNDECIDED band, alt overlaps.
  small_N_newton_undecided : N = 6210, sigma_sys = 0.0375: a Newtonian g = 1 meets no row (UNDECIDED).
  r_kill_iff_max          : KILLED iff R - 1 >= max(0.01, 3 sigma_R).
  r_consistent_unreachable : CONSISTENT is impossible when sigma_R > 0.005, hence when sigma_R >= 0.02.
  r_kill_cons_exclusive   : KILLED and CONSISTENT never hold together.
  r_kill_needs            : at sigma_R = 0.075 a kill needs R - 1 >= 0.225.
  gate_constants          : sigma_sys < 0.048 implies < 0.058; 3 x 0.048 < 0.1614 and 3 x 0.058 < 0.1917 (under the gate
                            3 sigma_sys stays below the Arm A distances); 3 x 0.048 <= 1.145 - 1; 1.173 - 1 < 3 x 0.058.
  sigma_sys_unreachable   : if 3 sigma_sys > anchor - 1 then anchor - 1 < 3 sigma for every sigma_fit.

kappa = 1/2 FITTED; footings never pooled; not theory closed. Adopts nothing.
-/
import Mathlib

namespace DP3

theorem sigma_parts (f s : ℝ) :
    Real.sqrt (f ^ 2 + s ^ 2) ^ 2 = f ^ 2 + s ^ 2 ∧ |f| ≤ Real.sqrt (f ^ 2 + s ^ 2) ∧
      |s| ≤ Real.sqrt (f ^ 2 + s ^ 2) := by
  refine ⟨Real.sq_sqrt (by positivity), ?_, ?_⟩
  · exact Real.abs_le_sqrt (by nlinarith [sq_nonneg s])
  · exact Real.abs_le_sqrt (by nlinarith [sq_nonneg f])

theorem sigma_fit_scaling (N N1 N2 : ℝ) (hN : 0 < N) (h1 : 0 < N1) (h12 : N1 ≤ N2) :
    (19 / 1000 * Real.sqrt (30000 / N)) ^ 2 * N = (19 / 1000) ^ 2 * 30000 ∧
    19 / 1000 * Real.sqrt (30000 / N2) ≤ 19 / 1000 * Real.sqrt (30000 / N1) := by
  constructor
  · rw [mul_pow, Real.sq_sqrt (by positivity)]
    field_simp
  · apply mul_le_mul_of_nonneg_left _ (by norm_num)
    apply Real.sqrt_le_sqrt
    exact div_le_div_of_nonneg_left (by norm_num) h1 h12

theorem sigma_monotone_sys (f s1 s2 d : ℝ) (h0 : 0 ≤ s1) (h12 : s1 ≤ s2) :
    Real.sqrt (f ^ 2 + s1 ^ 2) ≤ Real.sqrt (f ^ 2 + s2 ^ 2) ∧
    (3 * Real.sqrt (f ^ 2 + s2 ^ 2) ≤ d → 3 * Real.sqrt (f ^ 2 + s1 ^ 2) ≤ d) := by
  have h : Real.sqrt (f ^ 2 + s1 ^ 2) ≤ Real.sqrt (f ^ 2 + s2 ^ 2) := by
    apply Real.sqrt_le_sqrt
    nlinarith
  exact ⟨h, fun h' => by linarith⟩

theorem row_edges (A g σ : ℝ) :
    (3 * σ ≤ A - g ↔ g ≤ A - 3 * σ) ∧ (3 * σ ≤ g - 1 ↔ 1 + 3 * σ ≤ g) := by
  constructor <;> constructor <;> intro h <;> linarith

theorem both_iff (A σ : ℝ) :
    (∃ g : ℝ, 3 * σ ≤ A - g ∧ 3 * σ ≤ g - 1) ↔ 6 * σ ≤ A - 1 := by
  constructor
  · rintro ⟨g, h1, h2⟩
    linarith
  · intro h
    exact ⟨1 + 3 * σ, by linarith, by linarith⟩

theorem no_gap (A σ : ℝ) (h : 6 * σ ≤ A - 1) (g : ℝ) : 3 * σ ≤ A - g ∨ 3 * σ ≤ g - 1 := by
  by_contra hc
  rw [not_or, not_le, not_le] at hc
  linarith [hc.1, hc.2]

theorem undecided_gap (A σ : ℝ) (h : A - 1 < 6 * σ) :
    (∀ g : ℝ, (¬ (3 * σ ≤ A - g) ∧ ¬ (3 * σ ≤ g - 1)) ↔ (A - 3 * σ < g ∧ g < 1 + 3 * σ)) ∧
    (1 + 3 * σ) - (A - 3 * σ) = 6 * σ - (A - 1) ∧ 0 < 6 * σ - (A - 1) := by
  refine ⟨fun g => ?_, by ring, by linarith⟩
  constructor
  · rintro ⟨h1, h2⟩
    rw [not_le] at h1 h2
    constructor <;> linarith
  · rintro ⟨h1, h2⟩
    constructor <;> intro h3 <;> linarith

theorem subnewton_excludes (A g σ : ℝ) (hσ : 0 < σ) (hA : 1 ≤ A) (h : g ≤ 1 - 3 * σ) :
    ¬ (3 * σ ≤ g - 1) ∧ 3 * σ ≤ A - g ∧ ((1 : ℝ) ≤ 1 - 3 * 0 ∧ 3 * (0 : ℝ) ≤ 1 - 1) := by
  refine ⟨fun h' => by linarith, by linarith, by norm_num, by norm_num⟩

theorem three_sigma_sq (s d : ℝ) (hs : 0 ≤ s) (hd : 0 ≤ d) : 3 * s ≤ d ↔ 9 * s ^ 2 ≤ d ^ 2 := by
  constructor
  · intro h
    nlinarith
  · intro h
    nlinarith [sq_nonneg (3 * s - d), sq_nonneg (3 * s + d)]

theorem registered_sigma (s : ℝ) (hs : 0 ≤ s) (h : s ^ 2 = (19 / 1000) ^ 2 + (20 / 1000) ^ 2) :
    2758 / 100000 ≤ s ∧ s ≤ 2759 / 100000 ∧ 827 / 10000 ≤ 3 * s ∧ 3 * s ≤ 828 / 10000 := by
  refine ⟨?_, ?_, ?_, ?_⟩ <;> nlinarith

theorem registered_edges (s : ℝ) (hs : 0 ≤ s) (h : s ^ 2 = (19 / 1000) ^ 2 + (20 / 1000) ^ 2) :
    (10786 / 10000 ≤ 11614 / 10000 - 3 * s ∧ 11614 / 10000 - 3 * s ≤ 10787 / 10000) ∧
    (10827 / 10000 ≤ 1 + 3 * s ∧ 1 + 3 * s ≤ 10828 / 10000) ∧
    (9172 / 10000 ≤ 1 - 3 * s ∧ 1 - 3 * s ≤ 9173 / 10000) ∧
    (11089 / 10000 ≤ 11917 / 10000 - 3 * s ∧ 11917 / 10000 - 3 * s ≤ 11090 / 10000) ∧
    11614 / 10000 - 3 * s < 1 + 3 * s ∧ 1 + 3 * s ≤ 11917 / 10000 - 3 * s := by
  have h3 : 827 / 10000 ≤ 3 * s := by nlinarith
  have h4 : 3 * s ≤ 828 / 10000 := by nlinarith
  refine ⟨⟨?_, ?_⟩, ⟨?_, ?_⟩, ⟨?_, ?_⟩, ⟨?_, ?_⟩, ?_, ?_⟩ <;> linarith

theorem small_N_newton_undecided (s : ℝ) (hs : 0 ≤ s)
    (h : s ^ 2 = (19 / 1000) ^ 2 * (30000 / 6210) + (375 / 10000) ^ 2) :
    ¬ (3 * s ≤ 11614 / 10000 - 1) ∧ ¬ (3 * s ≤ (1 : ℝ) - 1) ∧ ¬ ((1 : ℝ) ≤ 1 - 3 * s) := by
  have hpos : 0 < s := by
    rcases hs.lt_or_eq with h' | h'
    · exact h'
    · rw [← h'] at h; norm_num at h
  refine ⟨fun h' => ?_, fun h' => by linarith, fun h' => by linarith⟩
  nlinarith

theorem r_kill_iff_max (R σ : ℝ) :
    (1 / 100 ≤ R - 1 ∧ 3 * σ ≤ R - 1) ↔ max (1 / 100) (3 * σ) ≤ R - 1 := by
  rw [max_le_iff]

theorem r_consistent_unreachable (R σ : ℝ) :
    (5 / 1000 < σ → ¬ (|R - 1| < 1 / 100 ∧ 2 * σ ≤ 1 / 100)) ∧
    (2 / 100 ≤ σ → ¬ (|R - 1| < 1 / 100 ∧ 2 * σ ≤ 1 / 100)) := by
  constructor
  · rintro hσ ⟨_, h2⟩
    linarith
  · rintro hσ ⟨_, h2⟩
    linarith

theorem r_kill_cons_exclusive (R σ : ℝ) :
    ¬ ((1 / 100 ≤ R - 1 ∧ 3 * σ ≤ R - 1) ∧ (|R - 1| < 1 / 100 ∧ 2 * σ ≤ 1 / 100)) := by
  rintro ⟨⟨h1, _⟩, h3, _⟩
  rw [abs_lt] at h3
  linarith [h3.2]

theorem r_kill_needs : max (1 / 100 : ℝ) (3 * (75 / 1000)) = 225 / 1000 := by
  norm_num

theorem gate_constants (b : ℝ) :
    (b < 48 / 1000 → b < 58 / 1000) ∧ 3 * (48 / 1000 : ℝ) < 11614 / 10000 - 1 ∧
    3 * (58 / 1000 : ℝ) < 11917 / 10000 - 1 ∧ 3 * (48 / 1000 : ℝ) ≤ 1145 / 1000 - 1 ∧
    (1173 / 1000 : ℝ) - 1 < 3 * (58 / 1000) := by
  refine ⟨fun h => by linarith, by norm_num, by norm_num, by norm_num, by norm_num⟩

theorem sigma_sys_unreachable (A f s : ℝ) (hs : 0 ≤ s) (h : A - 1 < 3 * s) :
    A - 1 < 3 * Real.sqrt (f ^ 2 + s ^ 2) := by
  have h1 : |s| ≤ Real.sqrt (f ^ 2 + s ^ 2) := Real.abs_le_sqrt (by nlinarith [sq_nonneg f])
  rw [abs_of_nonneg hs] at h1
  linarith

end DP3

-- kappa = 1/2 FITTED; footings never pooled; not theory closed. Adopts nothing.
