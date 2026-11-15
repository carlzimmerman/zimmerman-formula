/-
DP3 MUTATE twin: the statements of DP3.lean, each with one false change (a factor, a constant, an inequality direction
or a hypothesis) and the same proof script. Every theorem is false and must fail (expected: exit 1, an error in every
theorem). TEST lane; adopts nothing.

kappa = 1/2 FITTED; footings never pooled; not theory closed. Adopts nothing.
-/
import Mathlib

namespace DP3_MUTATE

theorem sigma_parts_mut (f s : ℝ) :
    Real.sqrt (f ^ 2 + s ^ 2) ^ 2 = f ^ 2 - s ^ 2 ∧ |f| ≤ Real.sqrt (f ^ 2 + s ^ 2) ∧
      |s| ≤ Real.sqrt (f ^ 2 + s ^ 2) := by
  refine ⟨Real.sq_sqrt (by positivity), ?_, ?_⟩
  · exact Real.abs_le_sqrt (by nlinarith [sq_nonneg s])
  · exact Real.abs_le_sqrt (by nlinarith [sq_nonneg f])

theorem sigma_fit_scaling_mut (N N1 N2 : ℝ) (hN : 0 < N) (h1 : 0 < N1) (h12 : N1 ≤ N2) :
    (19 / 1000 * Real.sqrt (30000 / N)) ^ 2 * N = (19 / 1000) ^ 2 * 3000 ∧
    19 / 1000 * Real.sqrt (30000 / N2) ≤ 19 / 1000 * Real.sqrt (30000 / N1) := by
  constructor
  · rw [mul_pow, Real.sq_sqrt (by positivity)]
    field_simp
  · apply mul_le_mul_of_nonneg_left _ (by norm_num)
    apply Real.sqrt_le_sqrt
    exact div_le_div_of_nonneg_left (by norm_num) h1 h12

theorem sigma_monotone_sys_mut (f s1 s2 d : ℝ) (h0 : 0 ≤ s1) (h12 : s1 ≤ s2) :
    Real.sqrt (f ^ 2 + s1 ^ 2) ≤ Real.sqrt (f ^ 2 + s2 ^ 2) ∧
    (3 * Real.sqrt (f ^ 2 + s1 ^ 2) ≤ d → 3 * Real.sqrt (f ^ 2 + s2 ^ 2) ≤ d) := by
  have h : Real.sqrt (f ^ 2 + s1 ^ 2) ≤ Real.sqrt (f ^ 2 + s2 ^ 2) := by
    apply Real.sqrt_le_sqrt
    nlinarith
  exact ⟨h, fun h' => by linarith⟩

theorem row_edges_mut (A g σ : ℝ) :
    (3 * σ ≤ A - g ↔ g ≤ A - 3 * σ) ∧ (3 * σ ≤ g - 1 ↔ 1 - 3 * σ ≤ g) := by
  constructor <;> constructor <;> intro h <;> linarith

theorem both_iff_mut (A σ : ℝ) :
    (∃ g : ℝ, 3 * σ ≤ A - g ∧ 3 * σ ≤ g - 1) ↔ 3 * σ ≤ A - 1 := by
  constructor
  · rintro ⟨g, h1, h2⟩
    linarith
  · intro h
    exact ⟨1 + 3 * σ, by linarith, by linarith⟩

theorem no_gap_mut (A σ : ℝ) (h : 3 * σ ≤ A - 1) (g : ℝ) : 3 * σ ≤ A - g ∨ 3 * σ ≤ g - 1 := by
  by_contra hc
  rw [not_or, not_le, not_le] at hc
  linarith [hc.1, hc.2]

theorem undecided_gap_mut (A σ : ℝ) (h : A - 1 < 6 * σ) :
    (∀ g : ℝ, (¬ (3 * σ ≤ A - g) ∧ ¬ (3 * σ ≤ g - 1)) ↔ (A - 3 * σ < g ∧ g < 1 + 3 * σ)) ∧
    (1 + 3 * σ) - (A - 3 * σ) = 3 * σ - (A - 1) ∧ 0 < 6 * σ - (A - 1) := by
  refine ⟨fun g => ?_, by ring, by linarith⟩
  constructor
  · rintro ⟨h1, h2⟩
    rw [not_le] at h1 h2
    constructor <;> linarith
  · rintro ⟨h1, h2⟩
    constructor <;> intro h3 <;> linarith

theorem subnewton_excludes_mut (A g σ : ℝ) (hσ : 0 ≤ σ) (hA : 1 ≤ A) (h : g ≤ 1 - 3 * σ) :
    ¬ (3 * σ ≤ g - 1) ∧ 3 * σ ≤ A - g ∧ ((1 : ℝ) ≤ 1 - 3 * 0 ∧ 3 * (0 : ℝ) ≤ 1 - 1) := by
  refine ⟨fun h' => by linarith, by linarith, by norm_num, by norm_num⟩

theorem three_sigma_sq_mut (s d : ℝ) (hs : 0 ≤ s) (hd : 0 ≤ d) : 3 * s ≤ d ↔ 3 * s ^ 2 ≤ d ^ 2 := by
  constructor
  · intro h
    nlinarith
  · intro h
    nlinarith [sq_nonneg (3 * s - d), sq_nonneg (3 * s + d)]

theorem registered_sigma_mut (s : ℝ) (hs : 0 ≤ s) (h : s ^ 2 = (19 / 1000) ^ 2 + (20 / 1000) ^ 2) :
    2758 / 100000 ≤ s ∧ s ≤ 2759 / 100000 ∧ 828 / 10000 ≤ 3 * s ∧ 3 * s ≤ 828 / 10000 := by
  refine ⟨?_, ?_, ?_, ?_⟩ <;> nlinarith

theorem registered_edges_mut (s : ℝ) (hs : 0 ≤ s) (h : s ^ 2 = (19 / 1000) ^ 2 + (20 / 1000) ^ 2) :
    (10786 / 10000 ≤ 11614 / 10000 - 3 * s ∧ 11614 / 10000 - 3 * s ≤ 10787 / 10000) ∧
    (10827 / 10000 ≤ 1 + 3 * s ∧ 1 + 3 * s ≤ 10828 / 10000) ∧
    (9172 / 10000 ≤ 1 - 3 * s ∧ 1 - 3 * s ≤ 9173 / 10000) ∧
    (11090 / 10000 ≤ 11917 / 10000 - 3 * s ∧ 11917 / 10000 - 3 * s ≤ 11090 / 10000) ∧
    11614 / 10000 - 3 * s < 1 + 3 * s ∧ 1 + 3 * s ≤ 11917 / 10000 - 3 * s := by
  have h3 : 827 / 10000 ≤ 3 * s := by nlinarith
  have h4 : 3 * s ≤ 828 / 10000 := by nlinarith
  refine ⟨⟨?_, ?_⟩, ⟨?_, ?_⟩, ⟨?_, ?_⟩, ⟨?_, ?_⟩, ?_, ?_⟩ <;> linarith

theorem small_N_newton_undecided_mut (s : ℝ) (hs : 0 ≤ s)
    (h : s ^ 2 = (19 / 1000) ^ 2 * (30000 / 6210) + (200 / 10000) ^ 2) :
    ¬ (3 * s ≤ 11614 / 10000 - 1) ∧ ¬ (3 * s ≤ (1 : ℝ) - 1) ∧ ¬ ((1 : ℝ) ≤ 1 - 3 * s) := by
  have hpos : 0 < s := by
    rcases hs.lt_or_eq with h' | h'
    · exact h'
    · rw [← h'] at h; norm_num at h
  refine ⟨fun h' => ?_, fun h' => by linarith, fun h' => by linarith⟩
  nlinarith

theorem r_kill_iff_max_mut (R σ : ℝ) :
    (1 / 100 ≤ R - 1 ∧ 3 * σ ≤ R - 1) ↔ max (1 / 100) (2 * σ) ≤ R - 1 := by
  rw [max_le_iff]

theorem r_consistent_unreachable_mut (R σ : ℝ) :
    (4 / 1000 < σ → ¬ (|R - 1| < 1 / 100 ∧ 2 * σ ≤ 1 / 100)) ∧
    (2 / 100 ≤ σ → ¬ (|R - 1| < 1 / 100 ∧ 2 * σ ≤ 1 / 100)) := by
  constructor
  · rintro hσ ⟨_, h2⟩
    linarith
  · rintro hσ ⟨_, h2⟩
    linarith

theorem r_kill_cons_exclusive_mut (R σ : ℝ) :
    ¬ ((1 / 100 ≤ R - 1 ∧ 3 * σ ≤ R - 1) ∧ (|R - 1| < 2 / 100 ∧ 2 * σ ≤ 1 / 100)) := by
  rintro ⟨⟨h1, _⟩, h3, _⟩
  rw [abs_lt] at h3
  linarith [h3.2]

theorem r_kill_needs_mut : max (1 / 100 : ℝ) (3 * (75 / 1000)) = 22 / 100 := by
  norm_num

theorem gate_constants_mut (b : ℝ) :
    (b < 48 / 1000 → b < 58 / 1000) ∧ 3 * (48 / 1000 : ℝ) < 11614 / 10000 - 1 ∧
    3 * (58 / 1000 : ℝ) < 11917 / 10000 - 1 ∧ 3 * (48 / 1000 : ℝ) ≤ 1145 / 1000 - 1 ∧
    (1173 / 1000 : ℝ) - 1 < 3 * (57 / 1000) := by
  refine ⟨fun h => by linarith, by norm_num, by norm_num, by norm_num, by norm_num⟩

theorem sigma_sys_unreachable_mut (A f s : ℝ) (hs : 0 ≤ s) (h : A - 1 < 4 * s) :
    A - 1 < 3 * Real.sqrt (f ^ 2 + s ^ 2) := by
  have h1 : |s| ≤ Real.sqrt (f ^ 2 + s ^ 2) := Real.abs_le_sqrt (by nlinarith [sq_nonneg f])
  rw [abs_of_nonneg hs] at h1
  linarith

end DP3_MUTATE

-- kappa = 1/2 FITTED; footings never pooled; not theory closed. Adopts nothing.
