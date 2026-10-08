import Mathlib

/-!
# ChainCert.Certificates -- five certificates for links of the program's chain

Each theorem states premises => conclusion; the premises are the program's own inputs, written as binders, never
proved from data.  What each one certifies, and what it does NOT:

* C1  dimensional uniqueness of a0 in the (c, G, rho) monomial family (exponent matrix det = -2).  It does not
      say a0 must be a monomial in these three constants -- that restriction is the premise.
* C2  kernel deep limit => v^4 -> G M a0 (point mass), composed with a0 = kappa c sqrt(G rho_Lambda) and the nu_beta family.
      The deep-limit premise `nu y * sqrt y -> 1` is a hypothesis of the general theorem and is verified for nu_beta here
      and for nu_mono in `ChainCert.Kernel`.
* C3  the cold-mass bookkeeping: f_ex = max(0, 1 - M_ph/M_c) gives M_ph + f_ex M_c = max(M_ph, M_c).  This is the algebra of
      the rule AS STATED (the max rule is a declared law of candidate B); it does not derive the rule.
* C4  the flat-a0 law and its rival: with Omega_m > 0, E(z) > 1 for z > 0 and E is strictly increasing; constant a0(z) holds
      iff rho_Lambda(z) is constant -- the premise is thereby explicit.
* C5  kappa is a free ratio of the four-form closure: every kappa with 0 < kappa^2 b < 1 is realised for some Z_q > 0.
      So kappa = 1/2 is a tuned value, NOT a derived one.

Nothing here certifies an empirical premise.  kappa = 1/2 is FITTED; Omega_c is FITTED; rho_Lambda constant is a premise.
-/

open Filter Topology

/-! ## C1 -- link (a): the dimensional form of a0 is unique (|det| = 2) -/

/-- exponent matrix of (c, G, rho) over (m, s, kg): c = m s^-1, G = m^3 kg^-1 s^-2, rho = kg m^-3 -/
theorem C1_exponent_matrix_det : Matrix.det !![(1:ℚ), 3, -3; -1, -2, 0; 0, -1, 1] = -2 := by
  simp [Matrix.det_fin_three]

/-- if a0 = xi * c^alpha * G^beta * rho^gamma has the units of an acceleration (m s^-2) then
    (alpha, beta, gamma) = (1, 1/2, 1/2): a0 = xi c sqrt(G rho). The converse is in `C1_a0_form_iff`. -/
theorem C1_a0_form_unique (α β γ : ℚ)
    (hkg : -β + γ = 0) (hm : α + 3 * β - 3 * γ = 1) (hs : -α - 2 * β = -2) :
    α = 1 ∧ β = 1 / 2 ∧ γ = 1 / 2 := by
  refine ⟨?_, ?_, ?_⟩ <;> linarith

/-- the converse: (1, 1/2, 1/2) does satisfy the three unit equations, so the units of an acceleration hold iff (alpha, beta, gamma) = (1, 1/2, 1/2) -/
theorem C1_a0_form_iff (α β γ : ℚ) :
    (-β + γ = 0 ∧ α + 3 * β - 3 * γ = 1 ∧ -α - 2 * β = -2) ↔ (α = 1 ∧ β = 1 / 2 ∧ γ = 1 / 2) := by
  constructor
  · rintro ⟨h1, h2, h3⟩
    exact C1_a0_form_unique α β γ h1 h2 h3
  · rintro ⟨rfl, rfl, rfl⟩
    norm_num

/-! ## C2 -- links (b)+(c): kernel family => deep-MOND flat speed => BTFR zero point, composed with a0(Lambda) -/

/-- the transition family nu_beta(y) = (1 + y^-beta)^(1/(2 beta)); beta = 1 is P2 = sqrt(1 + 1/y) -/
noncomputable def nuBeta (β y : ℝ) : ℝ := (1 + y ^ (-β)) ^ (1 / (2 * β))

theorem C2_nuBeta_one (y : ℝ) (hy : 0 < y) : nuBeta 1 y = Real.sqrt (1 + 1 / y) := by
  unfold nuBeta
  rw [Real.sqrt_eq_rpow, Real.rpow_neg_one]
  norm_num [one_div]

/-- exact deep-limit identity: nu_beta(y) * sqrt(y) = (1 + y^beta)^(1/(2 beta)) -/
theorem C2_nuBeta_mul_sqrt (β y : ℝ) (hβ : 0 < β) (hy : 0 < y) :
    nuBeta β y * Real.sqrt y = (1 + y ^ β) ^ (1 / (2 * β)) := by
  unfold nuBeta
  have hyb : 0 < y ^ β := Real.rpow_pos_of_pos hy β
  have h1 : Real.sqrt y = (y ^ β) ^ (1 / (2 * β)) := by
    rw [Real.sqrt_eq_rpow, ← Real.rpow_mul hy.le]
    congr 1
    field_simp
  rw [h1, ← Real.mul_rpow (by positivity) hyb.le]
  congr 1
  rw [add_mul, one_mul, ← Real.rpow_add hy]
  simp
  ring

theorem C2_nuBeta_deep (β : ℝ) (hβ : 0 < β) :
    Tendsto (fun y => nuBeta β y * Real.sqrt y) (𝓝[>] 0) (𝓝 1) := by
  have hcont : ContinuousAt (fun y : ℝ => (1 + y ^ β) ^ (1 / (2 * β))) 0 := by
    have h1 : ContinuousAt (fun y : ℝ => y ^ β) 0 := (Real.continuousAt_rpow_const 0 β (Or.inr hβ.le))
    have h2 : ContinuousAt (fun y : ℝ => 1 + y ^ β) 0 := continuousAt_const.add h1
    exact h2.rpow_const (Or.inr (by positivity))
  have key : Tendsto (fun y : ℝ => (1 + y ^ β) ^ (1 / (2 * β))) (𝓝 0) (𝓝 1) := by
    have := hcont.tendsto
    simpa [Real.zero_rpow hβ.ne'] using this
  have ht : Tendsto (fun y : ℝ => (1 + y ^ β) ^ (1 / (2 * β))) (𝓝[>] 0) (𝓝 1) :=
    key.mono_left nhdsWithin_le_nhds
  refine ht.congr' ?_
  filter_upwards [self_mem_nhdsWithin] with y hy
  exact (C2_nuBeta_mul_sqrt β y hβ hy).symm

/-- deep-MOND flat speed for ANY kernel whose deep limit is nu(y) sqrt(y) -> 1:
    v_c^4 -> G M a0 as r -> infinity (point mass, g = nu(g_N/a0) g_N). -/
theorem C2_deep_mond_flat_speed {G M a0 : ℝ} (hG : 0 < G) (hM : 0 < M) (ha : 0 < a0)
    (ν : ℝ → ℝ) (hν : Tendsto (fun y => ν y * Real.sqrt y) (𝓝[>] 0) (𝓝 1)) :
    Tendsto (fun r : ℝ => ((G * M / r) * ν (G * M / (r ^ 2 * a0))) ^ 2) atTop (𝓝 (G * M * a0)) := by
  have hy : Tendsto (fun r : ℝ => G * M / (r ^ 2 * a0)) atTop (𝓝[>] 0) := by
    refine tendsto_nhdsWithin_iff.mpr ⟨?_, ?_⟩
    · have h1 : Tendsto (fun r : ℝ => r ^ 2 * a0) atTop atTop :=
        (tendsto_pow_atTop (by norm_num : (2:ℕ) ≠ 0)).atTop_mul_const ha
      exact tendsto_const_nhds.div_atTop h1
    · filter_upwards [eventually_gt_atTop 0] with r hr
      exact Set.mem_Ioi.mpr (by positivity)
  have hcomp := hν.comp hy
  have hsq := (hcomp.pow 2).mul_const (G * M * a0)
  have hlim : (1 : ℝ) ^ 2 * (G * M * a0) = G * M * a0 := by ring
  rw [hlim] at hsq
  refine hsq.congr' ?_
  filter_upwards [eventually_gt_atTop 0] with r hr
  simp only [Function.comp]
  have hy0 : 0 < G * M / (r ^ 2 * a0) := by positivity
  have hs : Real.sqrt (G * M / (r ^ 2 * a0)) * Real.sqrt (G * M * a0) = G * M / r := by
    rw [← Real.sqrt_mul hy0.le]
    have : G * M / (r ^ 2 * a0) * (G * M * a0) = (G * M / r) ^ 2 := by field_simp
    rw [this, Real.sqrt_sq (by positivity)]
  have hsa : Real.sqrt (G * M * a0) ^ 2 = G * M * a0 := Real.sq_sqrt (by positivity)
  have hx : ∀ x : ℝ, x ^ 2 * (G * M * a0) = (x * Real.sqrt (G * M * a0)) ^ 2 := fun x => by
    rw [mul_pow, hsa]
  rw [hx]
  have : ν (G * M / (r ^ 2 * a0)) * Real.sqrt (G * M / (r ^ 2 * a0)) * Real.sqrt (G * M * a0)
      = G * M / r * ν (G * M / (r ^ 2 * a0)) := by
    rw [mul_assoc, hs]; ring
  rw [this]

/-- composition (a)+(b)+(c): with a0 = kappa c sqrt(G rho_Lambda) and the nu_beta family (beta > 0, contains P2),
    the asymptotic v^4 of a point mass is G M kappa c sqrt(G rho_Lambda). -/
theorem C2_btfr_from_vacuum {G M κ c ρΛ β : ℝ} (hG : 0 < G) (hM : 0 < M) (hκ : 0 < κ) (hc : 0 < c)
    (hρ : 0 < ρΛ) (hβ : 0 < β) :
    Tendsto (fun r : ℝ => ((G * M / r) * nuBeta β (G * M / (r ^ 2 * (κ * c * Real.sqrt (G * ρΛ)))))^2)
      atTop (𝓝 (G * M * (κ * c * Real.sqrt (G * ρΛ)))) :=
  C2_deep_mond_flat_speed hG hM (by positivity) (nuBeta β) (C2_nuBeta_deep β hβ)

/-! ## C3 -- link (d): cold-mass conservation, the max rule (no double counting of the phantom) -/

/-- leftover fraction: f_ex = max(0, 1 - M_ph,edge / [(1-f_b) M_coll]); Mc := (1-f_b) M_coll -/
noncomputable def fex (Mph Mc : ℝ) : ℝ := max 0 (1 - Mph / Mc)

theorem C3_conservation (Mph Mc : ℝ) (hMph : 0 ≤ Mph) (hMc : 0 < Mc) :
    0 ≤ fex Mph Mc ∧ fex Mph Mc ≤ 1 ∧ Mph + fex Mph Mc * Mc = max Mph Mc := by
  unfold fex
  refine ⟨le_max_left _ _, ?_, ?_⟩
  · refine max_le (by norm_num) ?_
    have : 0 ≤ Mph / Mc := by positivity
    linarith
  · rcases le_total Mph Mc with h | h
    · have h1 : 0 ≤ 1 - Mph / Mc := by rw [sub_nonneg, div_le_one hMc]; exact h
      rw [max_eq_right h1, max_eq_right h]; field_simp; ring
    · have h1 : 1 - Mph / Mc ≤ 0 := by
        rw [sub_nonpos, one_le_div hMc]; exact h
      rw [max_eq_left h1, max_eq_left h]; ring

/-- the total dark mass at the edge is the LARGER of the phantom's use and the conserved cold budget;
    it never falls below either, and is monotone in the collapse mass. -/
theorem C3_max_rule_monotone (Mph Mc Mc' : ℝ) (hMph : 0 ≤ Mph) (hMc : 0 < Mc) (hle : Mc ≤ Mc') :
    Mph + fex Mph Mc * Mc ≤ Mph + fex Mph Mc' * Mc' := by
  have hMc' : 0 < Mc' := lt_of_lt_of_le hMc hle
  rw [(C3_conservation Mph Mc hMph hMc).2.2, (C3_conservation Mph Mc' hMph hMc').2.2]
  exact max_le_max le_rfl hle

/-! ## C4 -- link (h): flat a0(z) versus the H-scaling rival are separated by E(z) > 1 at every z > 0 -/

noncomputable def Efun (Ωm ΩΛ z : ℝ) : ℝ := Real.sqrt (Ωm * (1 + z) ^ 3 + ΩΛ)

theorem C4_rival_exceeds_flat (Ωm ΩΛ z : ℝ) (hm : 0 < Ωm) (hΛ : 0 ≤ ΩΛ) (hsum : Ωm + ΩΛ = 1)
    (hz : 0 < z) : 1 < Efun Ωm ΩΛ z := by
  unfold Efun
  rw [Real.lt_sqrt (by norm_num)]
  have h1 : 1 < (1 + z) ^ 3 := by
    have : (1:ℝ) < 1 + z := by linarith
    exact one_lt_pow₀ this (by norm_num)
  nlinarith

theorem C4_rival_strictMono (Ωm ΩΛ : ℝ) (hm : 0 < Ωm) (hΛ : 0 ≤ ΩΛ) :
    StrictMonoOn (Efun Ωm ΩΛ) (Set.Ici 0) := by
  intro a ha b hb hab
  unfold Efun
  apply Real.sqrt_lt_sqrt
  · have : 0 ≤ (1 + a) ^ 3 := pow_nonneg (by simp at ha; linarith) 3
    positivity
  · have ha' : 0 < 1 + a := by simp at ha; linarith
    have : (1 + a) ^ 3 < (1 + b) ^ 3 := pow_lt_pow_left₀ (by linarith) ha'.le (by norm_num)
    nlinarith

/-- the numeric edge used by the chain: E(2.5) for Omega_m = 0.3138 lies in (3.76, 3.761) -/
theorem C4_E_at_two_point_five : 3.76 < Efun 0.3138 0.6862 2.5 ∧ Efun 0.3138 0.6862 2.5 < 3.761 := by
  unfold Efun
  constructor
  · rw [Real.lt_sqrt (by norm_num)]; norm_num
  · rw [Real.sqrt_lt' (by norm_num)]; norm_num

/-- flat law: if rho_Lambda does not evolve (w = -1) then a0(z) = a0(0) for every z (definitional) --
    stated so the PREMISE (constant rho_Lambda) is explicit in any chain that uses it -/
theorem C4_flat_iff_rho_const (κ c G : ℝ) (ρ : ℝ → ℝ) (hk : 0 < κ) (hc : 0 < c) (hG : 0 < G)
    (hρ : ∀ z, 0 < ρ z) :
    (∀ z, κ * c * Real.sqrt (G * ρ z) = κ * c * Real.sqrt (G * ρ 0)) ↔ (∀ z, ρ z = ρ 0) := by
  constructor
  · intro h z
    have h1 := h z
    have h2 : Real.sqrt (G * ρ z) = Real.sqrt (G * ρ 0) := by
      have hk' : κ * c ≠ 0 := by positivity
      exact mul_left_cancel₀ hk' h1
    have h3 : G * ρ z = G * ρ 0 := by
      have := congrArg (fun t => t ^ 2) h2
      simpa [Real.sq_sqrt (mul_pos hG (hρ z)).le, Real.sq_sqrt (mul_pos hG (hρ 0)).le] using this
    exact mul_left_cancel₀ hG.ne' h3
  · intro h z; rw [h z]

/-! ## C5 -- kappa is a FREE parameter of the four-form closure: every kappa in (0, 1/sqrt b) is realised -/

theorem C5_kappa_free (b β κ : ℝ) (hb : 0 < b) (hβ : 0 < β) (hκ : 0 < κ) (hκb : κ ^ 2 * b < 1) :
    ∃ Zq : ℝ, 0 < Zq ∧ κ ^ 2 = 2 * β ^ 2 / (Zq + 2 * b * β ^ 2) := by
  refine ⟨2 * β ^ 2 / κ ^ 2 - 2 * b * β ^ 2, ?_, ?_⟩
  · have hk2 : 0 < κ ^ 2 := by positivity
    have : 2 * b * β ^ 2 < 2 * β ^ 2 / κ ^ 2 := by
      rw [lt_div_iff₀ hk2]; nlinarith [sq_pos_of_pos hβ]
    linarith
  · have hk2 : 0 < κ ^ 2 := by positivity
    have : (2 * β ^ 2 / κ ^ 2 - 2 * b * β ^ 2) + 2 * b * β ^ 2 = 2 * β ^ 2 / κ ^ 2 := by ring
    rw [this]; field_simp
