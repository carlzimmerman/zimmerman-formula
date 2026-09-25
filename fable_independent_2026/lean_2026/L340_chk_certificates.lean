import Mathlib

/-!
# L340 — C-H/K, the filtered-khronon completion: algebraic certificates

SCOPE. Lean certifies the algebra `real_research/g03_audit_2026/L340_filtered_khronon_completion.py` rests on:
the static (omega -> 0) solution of the scalar block, the sign structure of the khronon mode, the negative-lobe
inertia bound and the alpha_2 bound.  It does not certify the reduction of the action to the block, the Krein
(energy-sign) computation, the SPARC or Solar-System numerics, or any nonlinear statement.

* `static_tracking`: at omega = 0 with c_2 != 0 the shift vanishes, psi = phi, (1 + C) U = phi and
  phi (2 alpha_c (1 + C) - 4) k^2 = R (1 + C): the MOND solution, G renormalised by alpha_c.
* `mode_sign`: the khronon root C (2 + 3 c_2) omega^2 = c_2 k^2 has omega^2 > 0 iff C > 0 (for c_2 > 0, k != 0):
  the constitutive coefficient C is the mode's inertia; a direction with C < 0 cannot be healthy.
* `inertia_pos`: 2k^2 C E/(1 + C) + alpha k^2 + lambda0 (1/2 - e) > 0 whenever C >= 0, 0 <= E, 0 <= e <= 1 and
  alpha k^2 > |lambda0|/2 -- the alpha_c a^2 term removes the negative-lobe pole.
* `alpha2_bound`: for 0 < c14 <= c2 <= 1/2 the khronometric alpha_2 = c14 (c14 - c2 + 2 c14 c2)/(c2 (2 - c14))
  (Yagi-Blas-Barausse-Yunes 2014, beta = 0; reproduced by L333) satisfies |alpha_2| <= c14.
-/

theorem static_tracking {k C c2 ac R psi phi beta U : ℝ} (hk : k ≠ 0) (hc2 : c2 ≠ 0)
    (hbeta : 2 * c2 * k ^ 4 * beta = 0)                                   -- beta equation at omega = 0
    (hpsi : 4 * k ^ 2 * psi - 4 * k ^ 2 * phi - 4 * k ^ 2 * 0 = 0)          -- psi equation at omega = 0
    (hU : 4 * k ^ 2 * (U - phi) + 4 * k ^ 2 * C * U = 0)
    (hphi : -4 * k ^ 2 * psi - 4 * k ^ 2 * (U - phi) + 2 * ac * k ^ 2 * phi - R = 0) :
    beta = 0 ∧ psi = phi ∧ (1 + C) * U = phi ∧ phi * ((2 * ac * (1 + C) - 4) * k ^ 2) = R * (1 + C) := by
  have hk2 : (k ^ 2 : ℝ) ≠ 0 := pow_ne_zero 2 hk
  have hk4 : (4 * k ^ 2 : ℝ) ≠ 0 := mul_ne_zero (by norm_num) hk2
  have hb : beta = 0 := by
    have : (2 * c2 * k ^ 4) ≠ 0 := mul_ne_zero (mul_ne_zero (by norm_num) hc2) (pow_ne_zero 4 hk)
    rcases mul_eq_zero.mp hbeta with h | h
    · exact absurd h this
    · exact h
  have hp : psi = phi := by
    have h : (4 * k ^ 2) * (psi - phi) = 0 := by linear_combination hpsi
    rcases mul_eq_zero.mp h with h | h
    · exact absurd h hk4
    · linarith
  have hu : (1 + C) * U = phi := by
    have h : (4 * k ^ 2) * ((1 + C) * U - phi) = 0 := by linear_combination hU
    rcases mul_eq_zero.mp h with h | h
    · exact absurd h hk4
    · linarith
  refine ⟨hb, hp, hu, ?_⟩
  rw [hp] at hphi
  linear_combination (1 + C) * hphi + 4 * k ^ 2 * hu

theorem mode_sign {C c2 k w2 : ℝ} (hc2 : 0 < c2) (hk : k ≠ 0)
    (hroot : C * (2 + 3 * c2) * w2 = c2 * k ^ 2) :
    0 < w2 ↔ 0 < C := by
  have hk2 : 0 < k ^ 2 := by positivity
  have hrhs : 0 < c2 * k ^ 2 := mul_pos hc2 hk2
  have h23 : 0 < 2 + 3 * c2 := by linarith
  constructor
  · intro hw
    rcases le_or_gt C 0 with hC | hC
    · have : C * (2 + 3 * c2) * w2 ≤ 0 :=
        mul_nonpos_of_nonpos_of_nonneg (mul_nonpos_of_nonpos_of_nonneg hC h23.le) hw.le
      linarith
    · exact hC
  · intro hC
    rcases le_or_gt w2 0 with hw | hw
    · have : C * (2 + 3 * c2) * w2 ≤ 0 :=
        mul_nonpos_of_nonneg_of_nonpos (mul_pos hC h23).le hw
      linarith
    · exact hw

theorem inertia_pos {k C E e al lam0 : ℝ} (hC : 0 ≤ C) (hE : 0 ≤ E) (he0 : 0 ≤ e) (he1 : e ≤ 1)
    (hal : |lam0| / 2 < al * k ^ 2) :
    0 < 2 * k ^ 2 * C * E / (1 + C) + al * k ^ 2 + lam0 * (1 / 2 - e) := by
  have h1 : 0 ≤ 2 * k ^ 2 * C * E / (1 + C) := by positivity
  have h2 : -(|lam0| / 2) ≤ lam0 * (1 / 2 - e) := by
    have hb : |1 / 2 - e| ≤ 1 / 2 := by rw [abs_le]; constructor <;> linarith
    have := abs_mul lam0 (1 / 2 - e)
    have h3 : |lam0 * (1 / 2 - e)| ≤ |lam0| / 2 := by
      rw [this]; nlinarith [abs_nonneg lam0, abs_nonneg (1 / 2 - e)]
    linarith [neg_abs_le (lam0 * (1 / 2 - e))]
  linarith

theorem alpha2_bound {c14 c2 : ℝ} (h14 : 0 < c14) (h142 : c14 ≤ c2) (hc2 : c2 ≤ 1 / 2) :
    |c14 * (c14 - c2 + 2 * c14 * c2) / (c2 * (2 - c14))| ≤ c14 := by
  have hc2p : 0 < c2 := lt_of_lt_of_le h14 h142
  have hden : 0 < c2 * (2 - c14) := mul_pos hc2p (by linarith)
  rw [abs_div, abs_of_pos hden, div_le_iff₀ hden, abs_mul, abs_of_pos h14]
  have hn : |c14 - c2 + 2 * c14 * c2| ≤ c2 := by
    rw [abs_le]; constructor <;> nlinarith
  have h3 : c2 ≤ c2 * (2 - c14) := by nlinarith
  have h4 : c14 * |c14 - c2 + 2 * c14 * c2| ≤ c14 * c2 := mul_le_mul_of_nonneg_left hn h14.le
  have h5 : c14 * c2 ≤ c14 * (c2 * (2 - c14)) := mul_le_mul_of_nonneg_left h3 h14.le
  linarith

#print axioms static_tracking
#print axioms mode_sign
#print axioms inertia_pos
#print axioms alpha2_bound
