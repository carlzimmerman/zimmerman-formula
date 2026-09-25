import Mathlib

/-!
# I21 — D-YM1, second independent route: the space-time polymer-expansion threshold

SCOPE. Lean certifies the SCALAR CHAIN of
`real_research/reviews/ym_door_swings_2026_09_22/ym1_hamiltonian/PROOF.md` (§§5–7):
every inequality that turns the analytic lemmas into the explicit thresholds. The analytic
lemmas themselves (Dyson expansion, polymer factorisation Lemma 4.1, the tree bounds of §5,
Ueltschi 2004 Theorem 1, the boundary-component argument of §7) are proved in prose there,
independently refereed twice (`REVIEW.md`), and are NOT formalized here. Energies are in units
of C_F, and the certified parameter choice is G = 7/100, b = C_F/2.

* `c_identity` — c + a₂ + b = C_F (§6 parameter choice).
* `kappa_le_Kstar` — κ = G/(1+G)⁷ ≤ K* = 6⁶/7⁷ (tree criticality, §5).
* `tree_supersolution` — for 0 ≤ g ≤ G: κ(1+g)⁷ ≤ G, so the monotone branching iteration
  started at 0 never leaves [0, G] (the bound behind Lemmas 5.1–5.2).
* `KP_a2_identity` — 2(d−1)·R = a₂ exactly, with R = 16λe^{a₁}(1+G)⁸ at λ = λ_*(d)
  (the event-contact half of the Kotecký–Preiss condition (6.2); a₁ = 4G² = 4A is the other).
* `kappaB_lt` — the boundary-sum condition of §7: κ_B = κ e^{2a₁}/(1−2G−2G²) ≤ 0.95 K*.
* `boundary_supersolution`, `path_ratio` — g = 3/25 is a supersolution for κ_B and the marked
  path step 7g/(1+g) = 3/4 < 1 (the Γ₀ₜ sum is bounded uniformly in t).
* `exp_neg_a1_lower` — e^{−a₁} ≥ 1/(1 + a₁ + a₁²/2 + 2a₁³/9) (Mathlib `Real.exp_bound'`, n = 3).
* `eps_uniform` — λ/C_F = 2b_N/(x²C_F) ≤ 32/(3x²) for every N ≥ 2 and 0 ≤ b_N ≤ 2N.
* `X2`, `X3`, `X4` — for x ≥ 131.1 / 185.3 / 227.0 the coupling is ≤ λ_*(d): the table of
  Theorem 1's Corollary, uniform in N.
* `gap_conversion` — (x/2)(C_F/2) ≥ 3x/16 for C_F ≥ 3/4.

Zero `sorry`; axioms ⊆ {propext, Classical.choice, Quot.sound}.
-/

noncomputable section

namespace I21

open Real

/-- The certified parameters (PROOF.md §6), energies in units of C_F. -/
def G : ℝ := 7 / 100
def b : ℝ := 1 / 2
def a1 : ℝ := 4 * G ^ 2
def c : ℝ := (1 - b) / (1 + G + G ^ 2)
def a2 : ℝ := c * G * (1 + G)
def κ : ℝ := G / (1 + G) ^ 7
def Kstar : ℝ := 6 ^ 6 / 7 ^ 7
/-- λ_*(d)/C_F = G c e^{−a₁} / (32 (d−1) (1+G)⁷). -/
def lamStar (d : ℝ) : ℝ := G * c * exp (-a1) / (32 * (d - 1) * (1 + G) ^ 7)

theorem c_identity : c + a2 + b = 1 := by
  norm_num [c, a2, b, G]

theorem kappa_le_Kstar : κ ≤ Kstar := by
  unfold κ Kstar G; norm_num

theorem tree_supersolution (g : ℝ) (h0 : 0 ≤ g) (hg : g ≤ G) : κ * (1 + g) ^ 7 ≤ G := by
  have hκ : 0 ≤ κ := by unfold κ G; positivity
  have hpow : (1 + g) ^ 7 ≤ (1 + G) ^ 7 := by gcongr
  have hG : (1 + G) ^ 7 ≠ 0 := by norm_num [G]
  calc κ * (1 + g) ^ 7 ≤ κ * (1 + G) ^ 7 := mul_le_mul_of_nonneg_left hpow hκ
    _ = G := by unfold κ; exact div_mul_cancel₀ G hG

theorem KP_a2_identity (d : ℝ) (hd : 1 < d) :
    2 * (d - 1) * (16 * lamStar d * exp a1 * (1 + G) ^ 8) = a2 := by
  have hd1 : (d - 1) ≠ 0 := by linarith
  have hG : (1 + G) ≠ 0 := by unfold G; norm_num
  unfold lamStar a2
  rw [show exp (-a1) = (exp a1)⁻¹ from exp_neg a1]
  have he : exp a1 ≠ 0 := (exp_pos a1).ne'
  field_simp
  ring

/-- e^{2a₁} ≤ 1/(1 − 2a₁) (Mathlib `Real.exp_bound_div_one_sub_of_interval`). -/
theorem exp_2a1_upper : exp (2 * a1) ≤ 1 / (1 - 2 * a1) := by
  apply exp_bound_div_one_sub_of_interval
  · unfold a1 G; norm_num
  · unfold a1 G; norm_num

/-- κ_B := κ e^{2a₁}/(1 − 2G − 2G²) is at most 0.95 K*. -/
theorem kappaB_lt : κ * exp (2 * a1) / (1 - 2 * G - 2 * G ^ 2) ≤ 95 / 100 * Kstar := by
  have hden : 0 < 1 - 2 * G - 2 * G ^ 2 := by unfold G; norm_num
  have hκ : 0 ≤ κ := by unfold κ G; positivity
  have h1 := exp_2a1_upper
  calc κ * exp (2 * a1) / (1 - 2 * G - 2 * G ^ 2)
      ≤ κ * (1 / (1 - 2 * a1)) / (1 - 2 * G - 2 * G ^ 2) := by
        gcongr
    _ ≤ 95 / 100 * Kstar := by unfold κ a1 Kstar G; norm_num

theorem boundary_supersolution :
    κ * exp (2 * a1) / (1 - 2 * G - 2 * G ^ 2) * (1 + 3 / 25) ^ 7 ≤ 3 / 25 := by
  have hden : 0 < 1 - 2 * G - 2 * G ^ 2 := by unfold G; norm_num
  have hκ : 0 ≤ κ := by unfold κ G; positivity
  have h1 := exp_2a1_upper
  calc κ * exp (2 * a1) / (1 - 2 * G - 2 * G ^ 2) * (1 + 3 / 25) ^ 7
      ≤ κ * (1 / (1 - 2 * a1)) / (1 - 2 * G - 2 * G ^ 2) * (1 + 3 / 25) ^ 7 := by
        gcongr
    _ ≤ 3 / 25 := by unfold κ a1 G; norm_num

theorem path_ratio : 7 * (3 / 25 : ℝ) / (1 + 3 / 25) < 1 := by norm_num

/-- e^{−a₁} ≥ 1/(1 + a₁ + a₁²/2 + 2a₁³/9), from `Real.exp_bound'` with n = 3. -/
theorem exp_neg_a1_lower : 1 / (1 + a1 + a1 ^ 2 / 2 + 2 * a1 ^ 3 / 9) ≤ exp (-a1) := by
  have h0 : 0 ≤ a1 := by unfold a1 G; norm_num
  have h1 : a1 ≤ 1 := by unfold a1 G; norm_num
  have hb := exp_bound' h0 h1 (n := 3) (by norm_num)
  have hsum : (∑ m ∈ Finset.range 3, a1 ^ m / (m.factorial : ℝ)) + a1 ^ 3 * (3 + 1) /
      ((Nat.factorial 3 : ℝ) * 3) = 1 + a1 + a1 ^ 2 / 2 + 2 * a1 ^ 3 / 9 := by
    simp [Finset.sum_range_succ, Nat.factorial]
    ring
  have hup : exp a1 ≤ 1 + a1 + a1 ^ 2 / 2 + 2 * a1 ^ 3 / 9 := by
    have := hb
    push_cast at this
    linarith [this, hsum.le, hsum.ge]
  rw [exp_neg, one_div]
  exact inv_anti₀ (exp_pos a1) hup

/-- Uniform in N: 2 b_N/(x² C_F) ≤ 32/(3x²) for N ≥ 2, 0 ≤ b_N ≤ 2N, C_F = (N²−1)/(2N). -/
theorem eps_uniform (N bN x : ℝ) (hN : 2 ≤ N) (_hb0 : 0 ≤ bN) (hb : bN ≤ 2 * N) (hx : 0 < x) :
    2 * bN / (x ^ 2 * ((N ^ 2 - 1) / (2 * N))) ≤ 32 / (3 * x ^ 2) := by
  have hN0 : 0 < N := by linarith
  have hCF : 0 < (N ^ 2 - 1) / (2 * N) := by
    apply div_pos <;> nlinarith
  rw [div_le_div_iff₀ (by positivity) (by positivity)]
  have hx2 : 0 < x ^ 2 := by positivity
  have key : 2 * bN * (2 * N) * 3 ≤ 32 * (N ^ 2 - 1) := by nlinarith
  field_simp
  nlinarith [key, hx2]

/-- λ_*(d) ≥ its rational lower bound. -/
theorem lamStar_lower (d : ℝ) (hd : 1 < d) :
    G * c * (1 / (1 + a1 + a1 ^ 2 / 2 + 2 * a1 ^ 3 / 9)) / (32 * (d - 1) * (1 + G) ^ 7)
      ≤ lamStar d := by
  unfold lamStar
  have hpos : 0 < 32 * (d - 1) * (1 + G) ^ 7 := by unfold G; positivity
  have hGc : 0 ≤ G * c := by norm_num [G, c, b]
  gcongr
  exact exp_neg_a1_lower

theorem X3 (x : ℝ) (hx : 1853 / 10 ≤ x) : 32 / (3 * x ^ 2) ≤ lamStar 3 := by
  refine le_trans ?_ (lamStar_lower 3 (by norm_num))
  have hx0 : 0 < x := by linarith
  have hx2 : (1853 / 10 : ℝ) ^ 2 ≤ x ^ 2 := by gcongr
  calc 32 / (3 * x ^ 2) ≤ 32 / (3 * (1853 / 10) ^ 2) := by gcongr
    _ ≤ _ := by norm_num [G, c, a1, b]

theorem X2 (x : ℝ) (hx : 1311 / 10 ≤ x) : 32 / (3 * x ^ 2) ≤ lamStar 2 := by
  refine le_trans ?_ (lamStar_lower 2 (by norm_num))
  have hx0 : 0 < x := by linarith
  have hx2 : (1311 / 10 : ℝ) ^ 2 ≤ x ^ 2 := by gcongr
  calc 32 / (3 * x ^ 2) ≤ 32 / (3 * (1311 / 10) ^ 2) := by gcongr
    _ ≤ _ := by norm_num [G, c, a1, b]

theorem X4 (x : ℝ) (hx : 227 ≤ x) : 32 / (3 * x ^ 2) ≤ lamStar 4 := by
  refine le_trans ?_ (lamStar_lower 4 (by norm_num))
  have hx0 : 0 < x := by linarith
  have hx2 : (227 : ℝ) ^ 2 ≤ x ^ 2 := by gcongr
  calc 32 / (3 * x ^ 2) ≤ 32 / (3 * (227 : ℝ) ^ 2) := by gcongr
    _ ≤ _ := by norm_num [G, c, a1, b]

theorem gap_conversion (x CF : ℝ) (hx : 0 ≤ x) (hC : 3 / 4 ≤ CF) : 3 * x / 16 ≤ x / 2 * (CF / 2) := by
  nlinarith

end I21

end

#print axioms I21.c_identity
#print axioms I21.kappa_le_Kstar
#print axioms I21.tree_supersolution
#print axioms I21.KP_a2_identity
#print axioms I21.kappaB_lt
#print axioms I21.boundary_supersolution
#print axioms I21.path_ratio
#print axioms I21.exp_neg_a1_lower
#print axioms I21.eps_uniform
#print axioms I21.X2
#print axioms I21.X3
#print axioms I21.X4
#print axioms I21.gap_conversion
