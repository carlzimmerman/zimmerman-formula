/-
SMF1 (criteria 9586b716e6): Lean statements for the algebraic cores of the graded structure items.
They certify the algebra, not the physics. TEST lane; adopts nothing. kappa = 1/2 FITTED; not theory closed.

  gauss_telescope   : S0b, sum over shells of the polarization charge (Y_{i+1} - Y_i) = Y_n - Y_0.
  gauss_zero        : S0b, regular centre (Y_0 = 0) and a free-falling boundary (Y_n = 0): net polarization charge 0.
  exchange_net_zero : S0b, the change of the net polarization charge between two times, both with Y_0 = Y_n = 0, is 0,
                      whatever the per-shell exchange did: the exchange cannot fill the halo in net.
  starvation        : S0c, S = g_x rho s vanishes where rho_Psi = 0.
  jeans_empty_core  : S0e, isotropic support outward from an empty core: p_{i+1} = p_i - rho_i g_i dr_i, p_0 = 0,
                      rho, g, dr >= 0 gives p_n <= 0 (no positive pressure can hold a hollow shell).
  jeans_root        : S1, the k -> 0 dispersion (mu^2/K^2) w^2 - ((G' rho - mu^2 (n + rho))/K) w - G' rho (n + rho) = 0
                      has the root w = -K (n + rho): Psi grows like dust with the total cold density.
  c1_split          : S1, the k^2 coefficient of the growing root equals -lambda_s + K hb^2 n^2/D (the stiffness enters
                      with a negative sign).
  lock_band_94      : S0d, g_x/depth at g_x = 9.199^2 and depth = 119.9^2 (km/s)^2 is below 0.006.
  constants_count   : section 1.2, 4 new constants >= the spec's 3.
-/
import Mathlib.Tactic

namespace SMF1

theorem gauss_telescope (Y : ℕ → ℝ) (n : ℕ) :
    (Finset.range n).sum (fun i => Y (i + 1) - Y i) = Y n - Y 0 := by
  exact Finset.sum_range_sub Y n

theorem gauss_zero (Y : ℕ → ℝ) (n : ℕ) (h0 : Y 0 = 0) (hn : Y n = 0) :
    (Finset.range n).sum (fun i => Y (i + 1) - Y i) = 0 := by
  rw [Finset.sum_range_sub Y n, h0, hn]; ring

theorem exchange_net_zero (Y Y' : ℕ → ℝ) (n : ℕ) (h0 : Y 0 = 0) (hn : Y n = 0) (h0' : Y' 0 = 0) (hn' : Y' n = 0) :
    (Finset.range n).sum (fun i => Y' (i + 1) - Y' i) - (Finset.range n).sum (fun i => Y (i + 1) - Y i) = 0 := by
  rw [gauss_zero Y n h0 hn, gauss_zero Y' n h0' hn']; ring

theorem starvation (g rho s : ℝ) (h : rho = 0) : g * rho * s = 0 := by
  rw [h]; ring

theorem jeans_empty_core (rho g dr : ℕ → ℝ) (p : ℕ → ℝ) (hp0 : p 0 = 0)
    (hstep : ∀ i, p (i + 1) = p i - rho i * g i * dr i)
    (hr : ∀ i, 0 ≤ rho i) (hg : ∀ i, 0 ≤ g i) (hd : ∀ i, 0 ≤ dr i) : ∀ n, p n ≤ 0 := by
  intro n
  induction n with
  | zero => rw [hp0]
  | succ k ih =>
    rw [hstep k]
    have : 0 ≤ rho k * g k * dr k := mul_nonneg (mul_nonneg (hr k) (hg k)) (hd k)
    linarith

theorem jeans_root (K mu G' rho n : ℝ) (hK : K ≠ 0) :
    (mu ^ 2 / K ^ 2) * (-K * (n + rho)) ^ 2 - ((G' * rho - mu ^ 2 * (n + rho)) / K) * (-K * (n + rho))
      - G' * rho * (n + rho) = 0 := by
  field_simp; ring

theorem c1_split (K hb n g lam m rho mu : ℝ) (hD : 2 * g * m ^ 2 * rho + hb ^ 2 * mu ^ 2 * n + hb ^ 2 * mu ^ 2 * rho ≠ 0) :
    -(-K * hb ^ 2 * n ^ 2 + 2 * g * lam * m ^ 2 * rho + hb ^ 2 * lam * mu ^ 2 * n + hb ^ 2 * lam * mu ^ 2 * rho)
        / (2 * g * m ^ 2 * rho + hb ^ 2 * mu ^ 2 * n + hb ^ 2 * mu ^ 2 * rho)
      = -lam + K * hb ^ 2 * n ^ 2 / (2 * g * m ^ 2 * rho + hb ^ 2 * mu ^ 2 * n + hb ^ 2 * mu ^ 2 * rho) := by
  have hD2 : hb ^ 2 * n * mu ^ 2 + hb ^ 2 * rho * mu ^ 2 + g * m ^ 2 * rho * 2 ≠ 0 := by
    intro h; apply hD; linarith
  rw [div_eq_iff hD, add_mul, div_mul_cancel₀ _ hD]; ring

theorem lock_band_94 : (9.199 : ℝ) ^ 2 / (119.9 : ℝ) ^ 2 < 0.006 := by norm_num

theorem constants_count : (3 : ℕ) ≤ 4 := by norm_num

end SMF1

#print axioms SMF1.gauss_telescope
#print axioms SMF1.gauss_zero
#print axioms SMF1.exchange_net_zero
#print axioms SMF1.starvation
#print axioms SMF1.jeans_empty_core
#print axioms SMF1.jeans_root
#print axioms SMF1.c1_split
#print axioms SMF1.lock_band_94
#print axioms SMF1.constants_count

-- Adopts nothing. kappa = 1/2 FITTED; not theory closed.
