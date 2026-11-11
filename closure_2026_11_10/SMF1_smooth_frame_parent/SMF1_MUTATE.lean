/-
SMF1 MUTATE twin: false versions of SMF1.lean's statements, proved with the same tactics. Every one must fail.
TEST lane; adopts nothing. kappa = 1/2 FITTED; not theory closed.
-/
import Mathlib.Tactic

namespace SMF1_MUTATE

-- boundary not free-falling (Y n unconstrained): the net charge need not vanish
theorem gauss_zero_false (Y : ℕ → ℝ) (n : ℕ) (h0 : Y 0 = 0) :
    (Finset.range n).sum (fun i => Y (i + 1) - Y i) = 0 := by
  rw [Finset.sum_range_sub Y n, h0]; ring

-- exchange without the rho_Psi factor (MU2): not zero at rho = 0
theorem starvation_false (g rho s : ℝ) (h : rho = 0) : g * s = 0 := by
  rw [h]; ring

-- positive pressure outward from an empty core
theorem jeans_empty_core_false (rho g dr : ℕ → ℝ) (p : ℕ → ℝ) (hp0 : p 0 = 0)
    (hstep : ∀ i, p (i + 1) = p i - rho i * g i * dr i)
    (hr : ∀ i, 0 ≤ rho i) (hg : ∀ i, 0 ≤ g i) (hd : ∀ i, 0 ≤ dr i) : ∀ n, 0 < p (n + 1) := by
  intro n
  induction n with
  | zero => rw [hstep 0, hp0]; linarith [mul_nonneg (mul_nonneg (hr 0) (hg 0)) (hd 0)]
  | succ k ih =>
    rw [hstep (k + 1)]
    have : 0 ≤ rho (k + 1) * g (k + 1) * dr (k + 1) := mul_nonneg (mul_nonneg (hr _) (hg _)) (hd _)
    linarith

-- the growing root with the wrong sign
theorem jeans_root_false (K mu G' rho n : ℝ) (hK : K ≠ 0) :
    (mu ^ 2 / K ^ 2) * (K * (n + rho)) ^ 2 - ((G' * rho - mu ^ 2 * (n + rho)) / K) * (K * (n + rho))
      - G' * rho * (n + rho) = 0 := by
  field_simp; ring

-- the stiffness entering with a positive sign
theorem c1_split_false (K hb n g lam m rho mu : ℝ) (hD : 2 * g * m ^ 2 * rho + hb ^ 2 * mu ^ 2 * n + hb ^ 2 * mu ^ 2 * rho ≠ 0) :
    -(-K * hb ^ 2 * n ^ 2 + 2 * g * lam * m ^ 2 * rho + hb ^ 2 * lam * mu ^ 2 * n + hb ^ 2 * lam * mu ^ 2 * rho)
        / (2 * g * m ^ 2 * rho + hb ^ 2 * mu ^ 2 * n + hb ^ 2 * mu ^ 2 * rho)
      = lam + K * hb ^ 2 * n ^ 2 / (2 * g * m ^ 2 * rho + hb ^ 2 * mu ^ 2 * n + hb ^ 2 * mu ^ 2 * rho) := by
  have hD2 : hb ^ 2 * n * mu ^ 2 + hb ^ 2 * rho * mu ^ 2 + g * m ^ 2 * rho * 2 ≠ 0 := by
    intro h; apply hD; linarith
  rw [div_eq_iff hD, add_mul, div_mul_cancel₀ _ hD]; ring

theorem lock_band_94_false : (9.199 : ℝ) ^ 2 / (119.9 : ℝ) ^ 2 < 0.005 := by norm_num

end SMF1_MUTATE

-- Adopts nothing. kappa = 1/2 FITTED; not theory closed.
