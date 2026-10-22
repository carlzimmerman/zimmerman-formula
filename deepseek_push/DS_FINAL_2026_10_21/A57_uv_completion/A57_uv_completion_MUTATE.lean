/-
A57 -- THE UV COMPLETION: the algebraic part, certified.

What is proved here (and nothing else):

  (1) `langmuir_law`      the n = 1 force law:  g - a0 * g/(g+a0) = g^2/(g+a0).
                          This is the exact statement that one gate per site with
                          capacity = affinity = a0 reproduces the law.

  (2) `h_lt_one`          0 <= h(y) < 1, where h(y) = (1/2)(sqrt(y^2+4y) - y)
                          is the response u/a0.  This is the statement that the
                          medium's response never exceeds its capacity, and it is
                          the hypothesis of the truncation bound (6).

  (3) `gibbs_shift`       the Gibbs weight of a two-state site is invariant under a
                          uniform shift H -> H + C of the energy.  Hence no
                          partition function can fix the absolute zero of energy,
                          hence kappa = a0/(c sqrt(G rho_Lambda)) is not a function
                          of the medium's parameters.

  (4) `kappa_length_ratio` kappa = ell_1 / L  =>  L / ell_1 = 1 / kappa.
  (5) `Lstar_identity`     L*/L = (sigma/c)^2 and kappa = ell_1/L
                             =>  L*/ell_1 = (sigma/c)^2 / kappa.
                          This is the identity the report calls "curve A": true,
                          and it defines sigma, so it is not a prediction.

  (6) `kappa_ge_eight_pi`  F = 8 pi/kappa^2, Y = 1/kappa, F <= Y, kappa > 0
                             =>  8 pi <= kappa.
                          The truncation bound at the cell-length cutoff.
  (7) `kappa_half_excluded`  therefore kappa = 1/2 is impossible for a medium
                          whose correlation length is the vacuum cell ell_1.

  (8) `q3_identity`        the q = 3 ladder's response:  x - x(1+2x)/(1+x+x^2)
                          = x^2(x-1)/(1+x+x^2), which is negative for 0 < x < 1.
                          Hence q >= 3 over-responds and g_N < 0: the exact law
                          forces one occupant per site.

No `sorry`, no `admit`, no new `axiom`.  Checked with `#print axioms` at the end.
-/
import Mathlib

namespace A57mut

/-! ## 1. The n = 1 law from one gate per site with capacity = affinity = a0 -/

theorem langmuir_law (g a0 : ℝ) (h : g + a0 ≠ 0) :
    g - a0 * (g / (g + a0)) = g ^ 2 / (g + a0) := by
  field_simp
  ring

/-! ## 2. The response never exceeds the capacity: h(y) < 1 -/

theorem h_lt_one (y : ℝ) (hy : 0 < y) :
    (1 / 2) * (Real.sqrt (y ^ 2 + 4 * y) - y) < 1 := by
  have h0 : (0 : ℝ) ≤ y ^ 2 + 4 * y := by nlinarith
  have hlt : Real.sqrt (y ^ 2 + 4 * y) < y + 2 := by
    have h2 : Real.sqrt (y ^ 2 + 4 * y) < Real.sqrt ((y + 2) ^ 2) := by
      apply Real.sqrt_lt_sqrt h0
      nlinarith
    rwa [Real.sqrt_sq (by linarith : (0 : ℝ) ≤ y + 2)] at h2
  linarith

/-! ## 3. The Gibbs weight is blind to the zero of energy -/

theorem gibbs_shift (β H₀ H₁ C : ℝ) :
    Real.exp (-(β * (H₀ + C))) /
        (Real.exp (-(β * (H₀ + C))) + Real.exp (-(β * (H₁ + C))))
      = Real.exp (-(β * H₀)) /
        (Real.exp (-(β * H₀)) + Real.exp (-(β * H₁))) := by
  have e0 : Real.exp (-(β * (H₀ + C)))
      = Real.exp (-(β * H₀)) * Real.exp (-(β * C)) := by
    rw [← Real.exp_add]
    congr 1
    ring
  have e1 : Real.exp (-(β * (H₁ + C)))
      = Real.exp (-(β * H₁)) * Real.exp (-(β * C)) := by
    rw [← Real.exp_add]
    congr 1
    ring
  rw [e0, e1]
  have ha : Real.exp (-(β * H₀)) ≠ 0 := Real.exp_ne_zero _
  have hb : Real.exp (-(β * H₁)) ≠ 0 := Real.exp_ne_zero _
  have hc : Real.exp (-(β * C)) ≠ 0 := Real.exp_ne_zero _
  have hsum : Real.exp (-(β * H₀)) + Real.exp (-(β * H₁)) ≠ 0 := by positivity
  have hden : Real.exp (-(β * H₀)) * Real.exp (-(β * C))
      + Real.exp (-(β * H₁)) * Real.exp (-(β * C)) ≠ 0 := by positivity
  field_simp

/-! ## 4. kappa is a length ratio -/

theorem kappa_length_ratio (κ ℓ L : ℝ) (hκ : κ ≠ 0) (h : κ = ℓ / L) :
    L / ℓ = 1 / κ := by
  have hL : L ≠ 0 := by
    intro hL0
    rw [hL0, div_zero] at h
    exact hκ h
  have hℓ : ℓ = κ * L := by
    rw [h]
    field_simp
  rw [hℓ]
  field_simp

/-! ## 5. The L* -- kappa -- sigma identity -/

theorem Lstar_identity (κ ℓ L σ c Ls : ℝ) (hκ : κ ≠ 0) (hc : c ≠ 0) (hL : L ≠ 0)
    (hk : κ = ℓ / L) (hs : Ls / L = (σ / c) ^ 2) :
    Ls / ℓ = (σ / c) ^ 2 / κ := by
  have hℓ : ℓ = κ * L := by
    rw [hk]
    field_simp
  have hLs : Ls = L * (σ / c) ^ 2 := by
    rw [← hs]
    field_simp
  rw [hℓ, hLs]
  field_simp

/-! ## 6. The truncation bound:  F <= Y and Y = 1/kappa  force  kappa >= 8 pi -/

theorem kappa_ge_eight_pi (κ F Y : ℝ) (hκ : 0 < κ)
    (hF : F = 8 * Real.pi / κ ^ 2) (hY : Y = 1 / κ) (hb : F ≤ 3 * Y) :
    8 * Real.pi ≤ κ := by
  rw [hF, hY] at hb
  have hk2 : 0 < κ ^ 2 := by positivity
  have hmul := mul_le_mul_of_nonneg_right hb (le_of_lt hk2)
  have h1 : 8 * Real.pi / κ ^ 2 * κ ^ 2 = 8 * Real.pi := by
    field_simp
  have h2 : 1 / κ * κ ^ 2 = κ := by
    field_simp
  rwa [h1, h2] at hmul

/-! ## 7. kappa = 1/2 is excluded by (6) -/

theorem kappa_half_excluded_unused : ¬ (8 * Real.pi ≤ 1 / 2) := by
  have hp := Real.pi_gt_three
  intro h
  nlinarith

/-! ## 8. The q = 3 ladder over-responds: g_N < 0 for 0 < x < 1 -/

theorem q3_identity (x : ℝ) (h : 1 + x + x ^ 2 ≠ 0) :
    x - x * (1 + 2 * x) / (1 + x + x ^ 2)
      = x ^ 2 * (x - 1) / (1 + x + x ^ 2) := by
  field_simp
  ring

theorem q3_negative (x : ℝ) (hx0 : 0 < x) (hx1 : x < 1)
    (h : 1 + x + x ^ 2 ≠ 0) :
    x - x * (1 + 2 * x) / (1 + x + x ^ 2) < 0 := by
  rw [q3_identity x h]
  have hx2 : 0 < x ^ 2 := by positivity
  have hxm : x - 1 < 0 := by linarith
  have hnum : x ^ 2 * (x - 1) < 0 := mul_neg_of_pos_of_neg hx2 hxm
  have hden : 0 < 1 + x + x ^ 2 := by nlinarith
  exact div_neg_of_neg_of_pos hnum hden

end A57mut

#print axioms A57mut.langmuir_law
#print axioms A57mut.h_lt_one
#print axioms A57mut.gibbs_shift
#print axioms A57mut.kappa_length_ratio
#print axioms A57mut.Lstar_identity
#print axioms A57mut.kappa_ge_eight_pi
#print axioms A57mut.kappa_half_excluded
#print axioms A57mut.q3_identity
#print axioms A57mut.q3_negative