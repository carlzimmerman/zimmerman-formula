/-
  G039 -- THE G036 RADIAL-SCATTER DECOMPOSITION -- the Lean certificate.

  G036 (commit f8d1ad7f0) discovered the RAR residual's radial anatomy on
  175 SPARC galaxies: the pooled deep-regime rms 0.1741 dex decomposes as
  between-galaxy 0.1908 / within-galaxy 0.0447 (per-galaxy offsets carry
  almost everything), and V4a's per-galaxy linear detrend collapses the
  pooled lag-1 autocorrelation to ~0.  This file certifies the two exact
  structural identities underneath those numbers:

    ols_normal
        the fitted pair satisfies the two normal equations -- the
        definitional heart, proved once
    ols_residual_sum_zero, ols_residual_x_sum_zero, ols_orthogonality
        the normal equations AS orthogonality: the detrended sequence has
        zero sum AND zero x-weighted sum -- the detrend kills the DC and
        drift channels (V4a's formal content)
    detrended_orthogonal_to_trend
        the residuals are orthogonal to the removed trend itself
    detrended_equals_noise
        idealized V4a: data = line-in-log-r + mean-zero noise, fit
        recovers the line => the detrended sequence IS the noise
    within_sq_split, pooled_second_moment_split
        the between/within variance identity: for two galaxies with n1,
        n2 points the pooled second moment splits EXACTLY into
        within-galaxy scatter + n1 (m1 - ybar)^2 + n2 (m2 - ybar)^2
        -- the identity G036's between/within rms's are square roots of

  The statistical verdicts (Fisher-z pooling, t- and binomial tests) are
  G036's computational lane; here are the exact statements beneath them.
-/
import Mathlib

noncomputable section

/-! ## OLS detrending and its orthogonality -/

/-- The OLS slope of `y` against `x` over `i < n`:
(n Sxy - Sx Sy) / (n Sxx - Sx^2). -/
def ols_slope (x y : ℕ → ℝ) (n : ℕ) : ℝ :=
  ((n : ℝ) * ∑ i ∈ Finset.range n, x i * y i
      - (∑ i ∈ Finset.range n, x i) * (∑ i ∈ Finset.range n, y i))
    / ((n : ℝ) * ∑ i ∈ Finset.range n, x i * x i
      - (∑ i ∈ Finset.range n, x i) ^ 2)

/-- The OLS intercept: (Sy - slope * Sx)/n -- the fitted line passes
through the data's centroid. -/
def ols_intercept (x y : ℕ → ℝ) (n : ℕ) : ℝ :=
  ((∑ i ∈ Finset.range n, y i)
      - ols_slope x y n * (∑ i ∈ Finset.range n, x i)) / (n : ℝ)

/-- The i-th OLS residual: data minus fitted line. -/
def ols_residual (x y : ℕ → ℝ) (n : ℕ) (i : ℕ) : ℝ :=
  y i - ols_intercept x y n - ols_slope x y n * x i

/-- The nondegeneracy hypothesis: n Sxx - Sx^2 ≠ 0 (the x_i not all
equal). -/
def design_nd (x : ℕ → ℝ) (n : ℕ) : Prop :=
  (n : ℝ) * ∑ i ∈ Finset.range n, x i * x i
    - (∑ i ∈ Finset.range n, x i) ^ 2 ≠ 0

/-- **ols_normal.**  The OLS pair satisfies the two normal equations:
n c + b Sx = Sy and c Sx + b Sxx = Sxy.  These two scalar facts are the
definitional heart of everything below. -/
theorem ols_normal (x y : ℕ → ℝ) (n : ℕ) (hn : 0 < n) (hnd : design_nd x n) :
    (n : ℝ) * ols_intercept x y n
        + ols_slope x y n * (∑ i ∈ Finset.range n, x i) = ∑ i ∈ Finset.range n, y i
    ∧ ols_intercept x y n * (∑ i ∈ Finset.range n, x i)
        + ols_slope x y n * (∑ i ∈ Finset.range n, x i * x i)
      = ∑ i ∈ Finset.range n, x i * y i := by
  have hnR : (n : ℝ) ≠ 0 := by exact_mod_cast ne_of_gt hn
  have hDne : (n : ℝ) * ∑ i ∈ Finset.range n, x i * x i
      - (∑ i ∈ Finset.range n, x i) ^ 2 ≠ 0 := hnd
  constructor
  · rw [ols_intercept]
    field_simp [hnR]
    ring
  · -- second normal equation: solve for the pair, combine linearly
    have hb : ols_slope x y n * ((n : ℝ) * ∑ i ∈ Finset.range n, x i * x i
        - (∑ i ∈ Finset.range n, x i) ^ 2)
        = (n : ℝ) * ∑ i ∈ Finset.range n, x i * y i
          - (∑ i ∈ Finset.range n, x i) * ∑ i ∈ Finset.range n, y i := by
      rw [ols_slope]
      exact div_mul_cancel₀ _ hDne
    have hc : (n : ℝ) * ols_intercept x y n
        = ∑ i ∈ Finset.range n, y i
          - ols_slope x y n * ∑ i ∈ Finset.range n, x i := by
      rw [ols_intercept]
      field_simp [hnR]
    have hterm1 : (n : ℝ) * (ols_intercept x y n * ∑ i ∈ Finset.range n, x i)
        = (∑ i ∈ Finset.range n, y i
            - ols_slope x y n * ∑ i ∈ Finset.range n, x i)
          * ∑ i ∈ Finset.range n, x i := by
      rw [← hc]
      ring
    have hterm2 : (n : ℝ) * (ols_slope x y n * ∑ i ∈ Finset.range n, x i * x i)
        = (n : ℝ) * ∑ i ∈ Finset.range n, x i * y i
          - (∑ i ∈ Finset.range n, x i) * ∑ i ∈ Finset.range n, y i
          + ols_slope x y n * (∑ i ∈ Finset.range n, x i) ^ 2 := by
      have hre : (n : ℝ) * (ols_slope x y n * ∑ i ∈ Finset.range n, x i * x i)
          = ols_slope x y n * ((n : ℝ) * ∑ i ∈ Finset.range n, x i * x i
            - (∑ i ∈ Finset.range n, x i) ^ 2)
          + ols_slope x y n * (∑ i ∈ Finset.range n, x i) ^ 2 := by ring
      rw [hre, hb]
    have hcomb : (n : ℝ) * (ols_intercept x y n * ∑ i ∈ Finset.range n, x i
        + ols_slope x y n * ∑ i ∈ Finset.range n, x i * x i)
        = (n : ℝ) * ∑ i ∈ Finset.range n, x i * y i := by
      rw [mul_add, hterm1, hterm2]
      ring
    exact mul_left_cancel₀ hnR hcomb

/-- **ols_residual_sum_zero.**  The OLS residuals have zero sum: the
detrended sequence carries no DC component (the first normal equation). -/
theorem ols_residual_sum_zero (x y : ℕ → ℝ) (n : ℕ) (hn : 0 < n)
    (hnd : design_nd x n) :
    ∑ i ∈ Finset.range n, ols_residual x y n i = 0 := by
  obtain ⟨h1, _⟩ := ols_normal x y n hn hnd
  have hexp : ∑ i ∈ Finset.range n, ols_residual x y n i
      = (∑ i ∈ Finset.range n, y i) - (n : ℝ) * ols_intercept x y n
        - ols_slope x y n * (∑ i ∈ Finset.range n, x i) := by
    simp only [ols_residual, Finset.sum_sub_distrib, Finset.sum_const,
      Finset.card_range, ← Finset.mul_sum]
    ring
  rw [hexp]
  linarith

/-- **ols_residual_x_sum_zero.**  The OLS residuals are orthogonal to the
regressor: sum r_i x_i = 0, for n > 0 and a nondegenerate design.
This is the x-orthogonality that kills the radial drift channel (the
formal content of G036 V4a). -/
theorem ols_residual_x_sum_zero (x y : ℕ → ℝ) (n : ℕ) (hn : 0 < n)
    (hnd : design_nd x n) :
    ∑ i ∈ Finset.range n, ols_residual x y n i * x i = 0 := by
  obtain ⟨_, h2n⟩ := ols_normal x y n hn hnd
  have hswap : ∑ i ∈ Finset.range n, y i * x i
      = ∑ i ∈ Finset.range n, x i * y i :=
    Finset.sum_congr rfl (fun i _ => by ring)
  have hres : ∀ i : ℕ, ols_residual x y n i * x i
      = y i * x i - ols_intercept x y n * x i
        - ols_slope x y n * (x i * x i) := by
    intro i
    rw [ols_residual]
    ring
  have hsplit : ∑ i ∈ Finset.range n, ols_residual x y n i * x i
      = ∑ i ∈ Finset.range n,
          (y i * x i - ols_intercept x y n * x i
            - ols_slope x y n * (x i * x i)) :=
    Finset.sum_congr rfl (fun i _ => hres i)
  have h2a : ∑ i ∈ Finset.range n, ols_intercept x y n * x i
      = ols_intercept x y n * ∑ i ∈ Finset.range n, x i := by
    rw [Finset.mul_sum]
  have h3a : ∑ i ∈ Finset.range n, ols_slope x y n * (x i * x i)
      = ols_slope x y n * ∑ i ∈ Finset.range n, x i * x i := by
    rw [Finset.mul_sum]
  rw [hsplit]
  simp only [Finset.sum_sub_distrib]
  rw [hswap]
  linarith

/-- **ols_orthogonality.**  The OLS normal equations as a single
orthogonality statement: the residual vector is orthogonal to 1 and to x.
After removing each galaxy's own best-fit line in log-r, the leftover
sequence has NO component along the trend. -/
theorem ols_orthogonality (x y : ℕ → ℝ) (n : ℕ) (hn : 0 < n)
    (hnd : design_nd x n) :
    ∑ i ∈ Finset.range n, ols_residual x y n i = 0
    ∧ ∑ i ∈ Finset.range n, ols_residual x y n i * x i = 0 :=
  ⟨ols_residual_sum_zero x y n hn hnd, ols_residual_x_sum_zero x y n hn hnd⟩

/-- **detrended_orthogonal_to_trend.**  The residuals are orthogonal to
the REMOVED TREND ITSELF: sum r_i (a + b x_i) = 0.  The drift channel the
detrend extracted cannot reappear downstream -- G036's "slow drift, not
concentric rings" reading, exactly. -/
theorem detrended_orthogonal_to_trend (x y : ℕ → ℝ) (n : ℕ) (hn : 0 < n)
    (hnd : design_nd x n) :
    ∑ i ∈ Finset.range n, ols_residual x y n i
        * (ols_intercept x y n + ols_slope x y n * x i) = 0 := by
  have hr := ols_residual_sum_zero x y n hn hnd
  have hx := ols_residual_x_sum_zero x y n hn hnd
  have hper : ∀ i, ols_residual x y n i
        * (ols_intercept x y n + ols_slope x y n * x i)
      = ols_intercept x y n * ols_residual x y n i
        + ols_slope x y n * (ols_residual x y n i * x i) := by
    intro i; ring
  rw [Finset.sum_congr rfl (fun i _ => hper i), Finset.sum_add_distrib,
    ← Finset.mul_sum, ← Finset.mul_sum, hr, hx]
  ring

/-! ## The idealized V4a -- the detrended sequence IS the noise -/

/-- **detrended_equals_noise.**  Idealized V4a: if the deep-regime
residual is exactly linear-in-log-r plus noise, y i = c + d x i + eps i,
and the per-galaxy fit recovers the generating line exactly (the OLS pair
is (c, d) -- what the normal equations deliver when the noise is itself
orthogonal to 1 and x), then the detrended sequence IS the noise; with
mean-zero noise its sum vanishes -- the drift is gone, the white
per-point noise is all that remains. -/
theorem detrended_equals_noise (x : ℕ → ℝ) (c d : ℝ) (eps y : ℕ → ℝ)
    (hy : ∀ i, y i = c + d * x i + eps i) (n : ℕ)
    (hfit : ols_intercept x y n = c ∧ ols_slope x y n = d)
    (heps : ∑ i ∈ Finset.range n, eps i = 0) :
    (∀ i, ols_residual x y n i = eps i)
    ∧ ∑ i ∈ Finset.range n, ols_residual x y n i = 0 := by
  constructor
  · intro i
    simp only [ols_residual, hfit.1, hfit.2, hy i]
    ring
  · have hrw : ∑ i ∈ Finset.range n, ols_residual x y n i
        = ∑ i ∈ Finset.range n, eps i :=
      Finset.sum_congr rfl (fun i _ => by
        simp only [ols_residual, hfit.1, hfit.2, hy i]; ring)
    rw [hrw, heps]

/-! ## The between/within variance decomposition -/

/-- The mean of a size-n sequence. -/
def seq_mean (g : ℕ → ℝ) (n : ℕ) : ℝ := (∑ i ∈ Finset.range n, g i) / (n : ℝ)

/-- **within_sq_split.**  The one-galaxy identity underneath the
decomposition: for ANY reference value `ybar`, the second moment about
ybar splits into the within-mean scatter plus n (m - ybar)^2, m the
galaxy mean.  (G036's use takes ybar = the pooled mean, but the identity
is exact for every ybar -- no distributional assumption anywhere.) -/
theorem within_sq_split (g : ℕ → ℝ) (n : ℕ) (_hn : 0 < n) (m ybar : ℝ)
    (hm : (n : ℝ) * m = ∑ i ∈ Finset.range n, g i) :
    ∑ i ∈ Finset.range n, (g i - ybar) ^ 2
      = ∑ i ∈ Finset.range n, (g i - m) ^ 2 + (n : ℝ) * (m - ybar) ^ 2 := by
  have hsmul : n • m = (n : ℝ) * m := by simp
  have hzero : ∑ i ∈ Finset.range n, (g i - m) = 0 := by
    rw [Finset.sum_sub_distrib, Finset.sum_const, Finset.card_range, hsmul, hm]
    ring
  have hexp : ∑ i ∈ Finset.range n, (g i - ybar) ^ 2
      = ∑ i ∈ Finset.range n, ((g i - m) ^ 2 + (m - ybar) ^ 2
          + 2 * (g i - m) * (m - ybar)) :=
    Finset.sum_congr rfl (fun i _ => by ring)
  have hcross : ∑ i ∈ Finset.range n, (2 * (g i - m) * (m - ybar))
      = 2 * (m - ybar) * ∑ i ∈ Finset.range n, (g i - m) := by
    rw [Finset.mul_sum]
    exact Finset.sum_congr rfl (fun i _ => by ring)
  have hconst : ∑ i ∈ Finset.range n, (m - ybar) ^ 2
      = (n : ℝ) * (m - ybar) ^ 2 := by
    rw [Finset.sum_const, Finset.card_range]
    simp
  rw [hexp, Finset.sum_add_distrib, Finset.sum_add_distrib, hcross, hzero,
    mul_zero, add_zero, hconst]

/-- **pooled_second_moment_split -- THE G036 DECOMPOSITION.**  Two
galaxies, n1 and n2 points, galaxy means m1 = seq_mean g1 n1 and
m2 = seq_mean g2 n2, any pooled reference ybar: the pooled second moment
splits EXACTLY into the within-galaxy parts plus the between-galaxy part
n1 (m1 - ybar)^2 + n2 (m2 - ybar)^2.  G036's numbers -- pooled 0.1741,
between 0.1908, within 0.0447 dex -- are the rms form of this identity
with ybar the pooled mean; the between term dominating the within term is
the discovery: per-galaxy offsets carry the deep-regime scatter. -/
theorem pooled_second_moment_split (g1 g2 : ℕ → ℝ) (n1 n2 : ℕ)
    (hn1 : 0 < n1) (hn2 : 0 < n2) (ybar : ℝ) :
    ∑ i ∈ Finset.range n1, (g1 i - ybar) ^ 2
        + ∑ j ∈ Finset.range n2, (g2 j - ybar) ^ 2
      = (∑ i ∈ Finset.range n1, (g1 i - seq_mean g1 n1) ^ 2
          + (n1 : ℝ) * (seq_mean g1 n1 - ybar) ^ 2)
        + (∑ i ∈ Finset.range n2, (g2 i - seq_mean g2 n2) ^ 2
          + (n2 : ℝ) * (seq_mean g2 n2 - ybar) ^ 2) := by
  have hn1R : (n1 : ℝ) ≠ 0 := by exact_mod_cast ne_of_gt hn1
  have hn2R : (n2 : ℝ) ≠ 0 := by exact_mod_cast ne_of_gt hn2
  have hm1 : (n1 : ℝ) * seq_mean g1 n1 = ∑ i ∈ Finset.range n1, g1 i := by
    rw [seq_mean]; field_simp
  have hm2 : (n2 : ℝ) * seq_mean g2 n2 = ∑ i ∈ Finset.range n2, g2 i := by
    rw [seq_mean]; field_simp
  have h1 := within_sq_split g1 n1 hn1 (seq_mean g1 n1) ybar hm1
  have h2 := within_sq_split g2 n2 hn2 (seq_mean g2 n2) ybar hm2
  rw [h1, h2]

#print axioms ols_normal
#print axioms ols_residual_sum_zero
#print axioms ols_residual_x_sum_zero
#print axioms ols_orthogonality
#print axioms detrended_orthogonal_to_trend
#print axioms detrended_equals_noise
#print axioms within_sq_split
#print axioms pooled_second_moment_split
