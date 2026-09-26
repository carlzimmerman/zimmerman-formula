import Mathlib

/-!
# XC1 — G8, the strong-coupling gate on C-H/K: algebraic certificates

SCOPE. Lean certifies the algebra behind `real_research/extra_crispy_2026/XC1_strong_coupling_chk.py`. The vertex
expansion (A1), the power counting of each class (A2), the window numbers (A4–A6) and the filter maximum's numerical
value (A8) are computed in that lane; here the identities they rest on are proved.

* `u_elimination_square`: eliminating the auxiliary U from the C-H block 2k²(u+v)² + 2Ck²u² leaves the clock inertia
  2Ck²v²/(1+C) plus a non-negative square — so 2C/(1+C) is the minimum, attained at u = −v/(1+C) (XC1 A3).
* `ch_inertia_bounds`: for C ≥ 0 the C-H inertia 2C/(1+C) lies in [0, 2C] and below 2; hence α_eff ≥ α_c
  (`alpha_eff_ge`), and with α_c = 0 the kinetic coefficient is below any ε once C < ε/2 (`uv_kinetic_small`,
  the MUTATE failure: the filter drives C to zero at every Solar-System momentum).
* `perfect_square_vanishes`: if a symmetric form h annihilates n (h^{μν} n_μ = 0), then h(t n, t n) = 0 — so with
  U = ln N, where D U − a = −n (n·∂ ln N), the C-H term is identically zero (XC1 A3).
* `branch_min_iff`: for c > 0, c^{3/2} ≤ c^{−1/2} ↔ c ≤ 1 — the two literature branches of the strong-coupling scale
  (Gümrükçüoğlu, Saravani & Sotiriou 2018 eq. 15) exchange exactly at c_s = 1 (XC1 A2).
* `msc_fourth_power`: with c₂ = α c_s², the superluminal-branch scale k = √α M/√c_s obeys k⁴ c₂ = M⁴ α³
  (i.e. k = M α^{3/4} c₂^{−1/4}) (XC1 A4).
* `de_scale_identity`: with a₀ = κ √(ρ/8π)/M (natural units, M reduced), (M a₀)² = κ² ρ/(8π): the MOND sector's
  scale √(M a₀) is (κ²/8π)^{1/4} ρ^{1/4} (XC1 A7).
* `filter_max`: for every real x, x e^{−3x/2} ≤ 2/(3e) — the largest MOND coupling under the heat filter (XC1 A8).
* `mond_cubic_coefficient`: 2[2 q″ s + (4/3) q‴ s³] with q″ = T′/(2s), q‴ = (s T″ − T′)/(4s³) equals
  (2/3)(2T′ + s T″) = (2/3) C_L′ (XC1 A6).
-/

theorem u_elimination_square (C k u v : ℝ) (hC : 0 ≤ C) :
    2 * k ^ 2 * (u + v) ^ 2 + 2 * C * k ^ 2 * u ^ 2
      = 2 * C * k ^ 2 * v ^ 2 / (1 + C) + 2 * k ^ 2 * (1 + C) * (u + v / (1 + C)) ^ 2 := by
  have h1 : (1 + C) ≠ 0 := by linarith
  field_simp
  ring

theorem u_elimination_min (C k u v : ℝ) (hC : 0 ≤ C) :
    2 * C * k ^ 2 * v ^ 2 / (1 + C) ≤ 2 * k ^ 2 * (u + v) ^ 2 + 2 * C * k ^ 2 * u ^ 2 := by
  rw [u_elimination_square C k u v hC]
  have h1 : 0 ≤ 2 * k ^ 2 * (1 + C) * (u + v / (1 + C)) ^ 2 := by positivity
  linarith

theorem ch_inertia_bounds (C : ℝ) (hC : 0 ≤ C) :
    0 ≤ 2 * C / (1 + C) ∧ 2 * C / (1 + C) ≤ 2 * C ∧ 2 * C / (1 + C) < 2 := by
  have h1 : 0 < 1 + C := by linarith
  refine ⟨by positivity, ?_, ?_⟩
  · rw [div_le_iff₀ h1]; nlinarith
  · rw [div_lt_iff₀ h1]; linarith

theorem alpha_eff_ge (αc C : ℝ) (hC : 0 ≤ C) : αc ≤ αc + 2 * C / (1 + C) := by
  have := (ch_inertia_bounds C hC).1
  linarith

theorem uv_kinetic_small (C ε : ℝ) (hC : 0 ≤ C) (hsmall : C < ε / 2) :
    (0 : ℝ) + 2 * C / (1 + C) < ε := by
  have h := (ch_inertia_bounds C hC).2.1
  linarith

theorem perfect_square_vanishes {n : ℕ} (h : Fin n → Fin n → ℝ) (v : Fin n → ℝ) (t : ℝ)
    (hn : ∀ j, ∑ i, h i j * v i = 0) :
    ∑ i, ∑ j, h i j * (t * v i) * (t * v j) = 0 := by
  have : ∀ i j, h i j * (t * v i) * (t * v j) = (t * t * v j) * (h i j * v i) := by
    intro i j; ring
  simp_rw [this]
  rw [Finset.sum_comm]
  simp_rw [← Finset.mul_sum]
  simp [hn]

theorem branch_min_iff (c : ℝ) (hc : 0 < c) :
    c ^ ((3 : ℝ) / 2) ≤ c ^ ((-1 : ℝ) / 2) ↔ c ≤ 1 := by
  have hsplit : c ^ ((3 : ℝ) / 2) = c ^ ((-1 : ℝ) / 2) * c ^ (2 : ℝ) := by
    rw [← Real.rpow_add hc]; norm_num
  have hpos : 0 < c ^ ((-1 : ℝ) / 2) := Real.rpow_pos_of_pos hc _
  rw [hsplit]
  constructor
  · intro h
    have h2 : c ^ (2 : ℝ) ≤ 1 := by
      have := (mul_le_iff_le_one_right hpos).mp h
      exact this
    have h3 : c ^ (2 : ℝ) = c ^ 2 := by
      rw [show (2 : ℝ) = ((2 : ℕ) : ℝ) by norm_num, Real.rpow_natCast]
    rw [h3] at h2
    nlinarith
  · intro h
    have h3 : c ^ (2 : ℝ) = c ^ 2 := by
      rw [show (2 : ℝ) = ((2 : ℕ) : ℝ) by norm_num, Real.rpow_natCast]
    have h2 : c ^ (2 : ℝ) ≤ 1 := by rw [h3]; nlinarith
    calc c ^ ((-1 : ℝ) / 2) * c ^ (2 : ℝ) ≤ c ^ ((-1 : ℝ) / 2) * 1 :=
          mul_le_mul_of_nonneg_left h2 hpos.le
      _ = c ^ ((-1 : ℝ) / 2) := by ring

theorem msc_fourth_power (α M cs c2 : ℝ) (hα : 0 < α) (hcs : 0 < cs) (hc2 : c2 = α * cs ^ 2) :
    (Real.sqrt α * M / Real.sqrt cs) ^ 4 * c2 = M ^ 4 * α ^ 3 := by
  have hsa : Real.sqrt α ^ 2 = α := Real.sq_sqrt hα.le
  have hsc : Real.sqrt cs ^ 2 = cs := Real.sq_sqrt hcs.le
  have hscpos : 0 < Real.sqrt cs := Real.sqrt_pos.mpr hcs
  have h4a : Real.sqrt α ^ 4 = α ^ 2 := by rw [show (4 : ℕ) = 2 * 2 by rfl, pow_mul, hsa]
  have h4c : Real.sqrt cs ^ 4 = cs ^ 2 := by rw [show (4 : ℕ) = 2 * 2 by rfl, pow_mul, hsc]
  rw [div_pow, mul_pow, h4a, h4c, hc2]
  field_simp

theorem de_scale_identity (M κ ρ : ℝ) (hM : 0 < M) (hρ : 0 ≤ ρ) :
    (M * (κ * Real.sqrt (ρ / (8 * Real.pi)) / M)) ^ 2 = κ ^ 2 * ρ / (8 * Real.pi) := by
  have hM' : M ≠ 0 := ne_of_gt hM
  have hq : 0 ≤ ρ / (8 * Real.pi) := by positivity
  have hs : Real.sqrt (ρ / (8 * Real.pi)) ^ 2 = ρ / (8 * Real.pi) := Real.sq_sqrt hq
  rw [show M * (κ * Real.sqrt (ρ / (8 * Real.pi)) / M) = κ * Real.sqrt (ρ / (8 * Real.pi)) by field_simp]
  rw [mul_pow, hs]
  ring

theorem filter_max (x : ℝ) : x * Real.exp (-(3 / 2) * x) ≤ 2 / (3 * Real.exp 1) := by
  have h := Real.add_one_le_exp ((3 / 2) * x - 1)
  have he : Real.exp ((3 / 2) * x - 1) * Real.exp (-(3 / 2) * x) = Real.exp (-1) := by
    rw [← Real.exp_add]; ring_nf
  have hpos : 0 < Real.exp (-(3 / 2) * x) := Real.exp_pos _
  have key : (3 / 2) * x * Real.exp (-(3 / 2) * x) ≤ Real.exp (-1) := by
    calc (3 / 2) * x * Real.exp (-(3 / 2) * x)
        = ((3 / 2) * x - 1 + 1) * Real.exp (-(3 / 2) * x) := by ring
      _ ≤ Real.exp ((3 / 2) * x - 1) * Real.exp (-(3 / 2) * x) :=
          mul_le_mul_of_nonneg_right h hpos.le
      _ = Real.exp (-1) := he
  have hinv : Real.exp (-1) = 1 / Real.exp 1 := by rw [Real.exp_neg]; ring
  have he1 : 0 < Real.exp 1 := Real.exp_pos 1
  rw [hinv] at key
  have : x * Real.exp (-(3 / 2) * x) = (2 / 3) * ((3 / 2) * x * Real.exp (-(3 / 2) * x)) := by ring
  rw [this]
  calc (2 / 3) * ((3 / 2) * x * Real.exp (-(3 / 2) * x)) ≤ (2 / 3) * (1 / Real.exp 1) := by
        have : (0 : ℝ) ≤ 2 / 3 := by norm_num
        exact mul_le_mul_of_nonneg_left key this
    _ = 2 / (3 * Real.exp 1) := by field_simp

theorem mond_cubic_coefficient (s Tp Tpp : ℝ) (hs : s ≠ 0) :
    2 * (2 * (Tp / (2 * s)) * s + (4 / 3) * ((s * Tpp - Tp) / (4 * s ^ 3)) * s ^ 3)
      = (2 / 3) * (2 * Tp + s * Tpp) := by
  field_simp
  ring

/-- The literature branches in exponent form: a vertex class (coupling index j ∈ {0 (α), 1 (c₂ = α c_s²)},
  fields F, time derivatives n_t, total derivatives N = F + 2) is O(1) at √α M c_s^p with
  p = (2j + n_t − F/2 − 1)/(4 − N).  The eight classes XC1 finds give p ∈ {3/2, 1/2, −1/2}. -/
theorem class_exponents :
    ((2 * 0 + 1 - (3 : ℚ) / 2 - 1) / (4 - 5) = 3 / 2) ∧      -- cubic α, n_t = 1
    ((2 * 0 + 3 - (3 : ℚ) / 2 - 1) / (4 - 5) = -1 / 2) ∧     -- cubic α, n_t = 3
    ((2 * 1 + 1 - (3 : ℚ) / 2 - 1) / (4 - 5) = -1 / 2) ∧     -- cubic c₂, n_t = 1
    ((2 * 0 + 0 - (4 : ℚ) / 2 - 1) / (4 - 6) = 3 / 2) ∧      -- quartic α, n_t = 0
    ((2 * 0 + 2 - (4 : ℚ) / 2 - 1) / (4 - 6) = 1 / 2) ∧      -- quartic α, n_t = 2
    ((2 * 0 + 4 - (4 : ℚ) / 2 - 1) / (4 - 6) = -1 / 2) ∧     -- quartic α, n_t = 4
    ((2 * 1 + 0 - (4 : ℚ) / 2 - 1) / (4 - 6) = 1 / 2) ∧      -- quartic c₂, n_t = 0
    ((2 * 1 + 2 - (4 : ℚ) / 2 - 1) / (4 - 6) = -1 / 2) := by -- quartic c₂, n_t = 2
  norm_num

#print axioms u_elimination_square
#print axioms u_elimination_min
#print axioms ch_inertia_bounds
#print axioms alpha_eff_ge
#print axioms uv_kinetic_small
#print axioms perfect_square_vanishes
#print axioms branch_min_iff
#print axioms msc_fourth_power
#print axioms de_scale_identity
#print axioms filter_max
#print axioms mond_cubic_coefficient
#print axioms class_exponents
