import Mathlib
import Mathlib.Tactic

/-
  C01 -- Lean certificate for the cluster mass-scaling fork (opus_48 cluster_massindep_2026/C01).

  Observed: the dark-component scale radius r_s(M) = k * M^(1/3) (self-similarity, k>0) is STRICTLY
  INCREASING in halo mass M.  Candidate: the dark-source peak radius is a UNIVERSAL constant H (fixed by a
  universal coupling |K2|).  Two load-bearing facts, certified here:

    (1) r_s is strictly increasing in M  ==>  a single universal H can equal r_s(M) for AT MOST ONE mass
        (rs_strictMono, universal_H_at_most_one_mass);
    (2) to place the peak at r_s(M) for every system, the required coupling K2(M) = A / r_s(M) (A>0) is
        STRICTLY DECREASING in M -- i.e. K2 ~ M^(-1/3), NOT a universal constant
        (K2_required_strictAnti).

  These certify the qualitative content of C01 (a mass-independent radius cannot track a mass-scaling one);
  the magnitude (x7.4 over 1e13-1e15 Msun) is the empirical statement in the Python lane.
-/

noncomputable section
open Real

/-- The observed dark scale radius as a function of halo mass (self-similar, k>0). -/
def rs (k M : ℝ) : ℝ := k * M ^ ((1:ℝ)/3)

/-- (1) r_s is strictly increasing in M on [0,∞) for k>0. -/
theorem rs_strictMono {k : ℝ} (hk : 0 < k) {M₁ M₂ : ℝ} (h1 : 0 ≤ M₁) (h12 : M₁ < M₂) :
    rs k M₁ < rs k M₂ := by
  have hpow : M₁ ^ ((1:ℝ)/3) < M₂ ^ ((1:ℝ)/3) :=
    Real.rpow_lt_rpow h1 h12 (by norm_num)
  unfold rs
  exact mul_lt_mul_of_pos_left hpow hk

/-- (1') A universal constant H equals r_s(M) for at most one mass: if r_s hits H at M₁ and M₂, then M₁=M₂. -/
theorem universal_H_at_most_one_mass {k H : ℝ} (hk : 0 < k) {M₁ M₂ : ℝ}
    (h1 : 0 ≤ M₁) (h2 : 0 ≤ M₂) (e1 : rs k M₁ = H) (e2 : rs k M₂ = H) : M₁ = M₂ := by
  rcases lt_trichotomy M₁ M₂ with h | h | h
  · exact absurd (e1 ▸ e2 ▸ rs_strictMono hk h1 h) (by simp)
  · exact h
  · exact absurd (e2 ▸ e1 ▸ rs_strictMono hk h2 h) (by simp)

/-- The required coupling to place the peak at r_s(M): K2(M) = A / r_s(M). -/
def K2req (A k M : ℝ) : ℝ := A / rs k M

/-- (2) The required coupling is strictly DECREASING in M (so it cannot be a universal constant). -/
theorem K2_required_strictAnti {A k : ℝ} (hA : 0 < A) (hk : 0 < k) {M₁ M₂ : ℝ}
    (h1 : 0 < M₁) (h12 : M₁ < M₂) : K2req A k M₂ < K2req A k M₁ := by
  have hr1 : 0 < rs k M₁ := by
    unfold rs; exact mul_pos hk (Real.rpow_pos_of_pos h1 _)
  have hr12 : rs k M₁ < rs k M₂ := rs_strictMono hk (le_of_lt h1) h12
  have hr2 : 0 < rs k M₂ := lt_trans hr1 hr12
  unfold K2req
  exact div_lt_div_of_pos_left hA hr1 hr12

end
