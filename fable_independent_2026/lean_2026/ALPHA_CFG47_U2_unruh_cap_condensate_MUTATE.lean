import Mathlib

/-!
# M2_06 -- Lean certificate for four small exact results from the alpha / a0 negative lanes
(a) CFG47 (campaign_fresh_gravity/CFG47_unruh_matching/CFG47_unruh_matching.py, checks U1, U3, U4): the
    Unruh = de Sitter temperature matching and the energy-matching variant.
(b) U2 (real_research/alpha_principle_2026/U2_programme_native_model/u2_1_cap_condensate_alpha.py, checks A1, A2a, A2b,
    A4, A7a): the cap-stiffness winding-charge model's algebra.
(c) J1 (J_emergent_condensate/j1_induced_photon_structure.py): the induced-photon coupling alpha_eff = 3 pi/(N L).
(d) N5 (N5_dS2_fermions/n5_2_induced_current.py, n5_3_schwinger_model_ds2.py checks S1, S2): the dS_2 fermion
    conductivity limit g_f(0) = 1/pi and the massless-Schwinger-model decay-exponent quadratic.
Corpus check: ChainCert/Footing.lean has Z = sqrt(32 pi/3) = 2 sqrt(8 pi/3) and ChainCert/Fluid.lean the cap tie
a0^2 = kappa^2 Lambda/(8 pi); L341_frw_certificates.lean has `floor_is_dS_unruh` (a0 = c H_Lambda/Z).  None of the
statements below (T_U = T_dS matching value, n-mode energy matching exponent, the cap-condensate alpha_c algebra,
the dS_2 conductivity limit) occurs in the corpus (`git grep -n -i -e Unruh -e alpha_c -e sinh -- '*.lean'`; the
sinh hits are AH3's closed forms, not the mu -> 0 limit).  New.

CERTIFIED (pure mathematics; hypotheses stated):
(a) `unruh_matching`: hbar a/(2 pi c k) = hbar H/(2 pi k) (T_Unruh = T_dS) with H > 0, c > 0 gives a = c H; with
    H = H_L = sqrt(8 pi G rho/3), a = c sqrt(8 pi/3) sqrt(G rho), so kappa_match := a/(c sqrt(G rho)) = sqrt(8 pi/3)
    (`kappa_match_value`) and dividing by n modes gives sqrt(8 pi/3)/n.  `n_for_half`: sqrt(8 pi/3)/n = 1/2 iff
    n = Z := sqrt(32 pi/3) (using Z = 2 sqrt(8 pi/3)); `Z_between`: 5 < Z < 6 so Z is not an integer; `n2_kappa`: n = 2
    gives kappa = Z/4 > 1.  `energy_matching_exponent`: the n-mode thermal energy density u = n (pi^2/30) (kT)^4/(hbar c)^3
    with kT = hbar a/(2 pi c) set equal to rho c^2 gives a^4 = 30 (2 pi)^4 rho c^9/(n pi^2 hbar); hence a(4 rho)/a(rho) = sqrt 2,
    whereas any a = C c sqrt(G rho) gives ratio 2: the energy-matching form is not in the (c, G, rho) family.
(b) with P_cap = kappa^2 Lambda c^4/(64 pi^2 G), F^2 = 2 P_cap xi^2, alpha_c = w F^2 xi^2/(hbar c):
    `alpha_c_form`: alpha_c = (w kappa^2/(32 pi^2)) x (xi^4/l_P^4) with x = Lambda l_P^2, l_P^2 = hbar G/c^3;
    `alpha_c_cap`: if P_cap xi^4 = s hbar c then alpha_c = 2 w s exactly (independent of kappa, Lambda, G, c, hbar; hence the
    same on any two footings);  `alpha_c_geo_mean`: if xi^4 = l_P^2 r_H^2 with r_H^2 = 3/Lambda then
    alpha_c = 3 w kappa^2/(32 pi^2), independent of x; `alpha_c_rH`: xi = r_H gives alpha_c proportional to 1/x;
    `geo_mean_inverse_alpha`: for w = pi, 1/alpha_c = 32 pi/(3 kappa^2) = Z^2/kappa^2 = 4 Z^2 at kappa = 1/2.
    (The lane records that 4 Z^2 = 134.04 misses 137.036 and that the model does not produce the missing +3; this file certifies
    the algebra only.)
(c) `alpha_eff_value`: from eps = L N e^2/(12 pi^2 v) and alpha_eff = e^2/(4 pi eps v) one gets alpha_eff = 3 pi/(N L), independent
    of e and v (e, v /= 0).
(d) `gf_zero_limit`: g_f(mu) = 2 mu/sinh(2 pi mu) -> 1/pi as mu -> 0 (PREMISE: the closed form; the lane validated it against
    the direct mode sum to 1e-6, not certified here).  `schwinger_exponent`: E(t) = exp(-s t) satisfies
    E'' + H E' + (e^2/pi) E = (s^2 - H s + e^2/pi) E, so it solves the equation iff s^2 - H s + e^2/pi = 0; with Delta = s/H this is
    Delta (1 - Delta) = x := e^2/(pi H^2); real roots exist iff x <= 1/4 (`schwinger_real_iff`), i.e. e^2 <= pi H^2/4, and the roots sum to 1.
NOT CERTIFIED: any of the physical premises (Unruh = de Sitter matching is the CFG47 'route under test', third-party text;
the cap tie P_cap = (kappa^2/8 pi) rho_Lambda c^2 is POSTULATED per the equation ledger; the winding-charge model is
retired by the lane: closed windings carry no Coulomb charge, u2_2), numerical footings, any derivation of alpha or kappa.
kappa = 1/2 stays FITTED; nothing here says kappa = 1/2 is derived (n = Z is the value the FOOTING needs, not a result).
-/

open Filter Topology

namespace M2Unruh

/-! ### (a) Unruh / de Sitter matching -/

theorem unruh_matching (hbar a c k H : ℝ) (hb0 : 0 < hbar) (hc : 0 < c) (hk : 0 < k)
    (h : hbar * a / (2 * Real.pi * c * k) = hbar * H / (2 * Real.pi * k)) : a = c * H := by
  have hπ : 0 < Real.pi := Real.pi_pos
  field_simp at h
  nlinarith [h, mul_pos hb0 hπ, mul_pos (mul_pos hb0 hπ) hk]

theorem kappa_match_value (G rho c : ℝ) (hG : 0 < G) (hrho : 0 < rho) (hc : 0 < c) :
    c * Real.sqrt (8 * Real.pi * G * rho / 3) / (c * Real.sqrt (G * rho)) = Real.sqrt (8 * Real.pi / 3) := by
  have h1 : Real.sqrt (8 * Real.pi * G * rho / 3) = Real.sqrt (8 * Real.pi / 3) * Real.sqrt (G * rho) := by
    rw [← Real.sqrt_mul (by positivity)]; congr 1; ring
  have h2 : 0 < Real.sqrt (G * rho) := Real.sqrt_pos.mpr (by positivity)
  rw [h1]; field_simp

noncomputable def Z : ℝ := Real.sqrt (32 * Real.pi / 3)

theorem Z_eq : Z = 2 * Real.sqrt (8 * Real.pi / 3) := by
  unfold Z
  have h : (32 * Real.pi / 3) = 2 ^ 2 * (8 * Real.pi / 3) := by ring
  rw [h, Real.sqrt_mul (by positivity), Real.sqrt_sq (by norm_num)]

theorem n_for_half (n : ℝ) (hn : 0 < n) : Real.sqrt (8 * Real.pi / 3) / n = 1 / 2 ↔ n = Z := by
  rw [Z_eq]
  have hs : 0 < Real.sqrt (8 * Real.pi / 3) := Real.sqrt_pos.mpr (by positivity)
  rw [div_eq_iff hn.ne']
  constructor <;> intro h <;> linarith

theorem Z_between : 6 < Z ∧ Z < 7 := by
  unfold Z
  have h3 := Real.pi_gt_three
  have h4 := Real.pi_lt_four
  constructor
  · rw [show (5 : ℝ) = Real.sqrt 25 by
      rw [show (25 : ℝ) = 5 ^ 2 by norm_num, Real.sqrt_sq (by norm_num)]]
    apply Real.sqrt_lt_sqrt (by norm_num)
    linarith [Real.pi_gt_d2]
  · rw [show (6 : ℝ) = Real.sqrt 36 by
      rw [show (36 : ℝ) = 6 ^ 2 by norm_num, Real.sqrt_sq (by norm_num)]]
    apply Real.sqrt_lt_sqrt (by positivity)
    linarith [Real.pi_lt_d2]

theorem Z_not_integer : ¬ ∃ m : ℤ, (m : ℝ) = Z := by
  rintro ⟨m, hm⟩
  obtain ⟨h5, h6⟩ := Z_between
  rw [← hm] at h5 h6
  have a : (5 : ℤ) < m := by exact_mod_cast h5
  have b : m < (6 : ℤ) := by exact_mod_cast h6
  omega

theorem n2_kappa : Real.sqrt (8 * Real.pi / 3) / 2 = Z / 4 ∧ 1 < Z / 4 := by
  refine ⟨?_, ?_⟩
  · rw [Z_eq]; ring
  · have := Z_between.1; linarith

/-- energy matching: a^4 = 30 (2 pi)^4 rho c^9/(n pi^2 hbar) from u = n (pi^2/30) (kT)^4/(hbar c)^3, kT = hbar a/(2 pi c), u = rho c^2 -/
theorem energy_matching_a4 (n rho c hbar a : ℝ) (hn : 0 < n) (hc : 0 < c) (hbp : 0 < hbar)
    (h : n * (Real.pi ^ 2 / 30) * (hbar * a / (2 * Real.pi * c)) ^ 4 / (hbar * c) ^ 3 = rho * c ^ 2) :
    a ^ 4 = 30 * (2 * Real.pi) ^ 4 * rho * c ^ 9 / (n * Real.pi ^ 2 * hbar) := by
  have hπ : Real.pi ≠ 0 := Real.pi_ne_zero
  field_simp at h ⊢
  nlinarith [h]

theorem energy_matching_exponent (a1 a4 : ℝ) (h1 : 0 < a1) (h4 : 0 < a4) (K rho : ℝ)
    (e1 : a1 ^ 4 = K * rho) (e4 : a4 ^ 4 = K * (4 * rho)) : a4 = Real.sqrt 2 * a1 := by
  have h : a4 ^ 4 = (Real.sqrt 2 * a1) ^ 4 := by
    rw [mul_pow, e4]
    have : Real.sqrt 2 ^ 4 = 4 := by
      rw [show (4 : ℕ) = 2 * 2 from rfl, pow_mul, Real.sq_sqrt (by norm_num)]; norm_num
    rw [this, e1]; ring
  have hs : 0 < Real.sqrt 2 * a1 := by positivity
  exact (pow_left_inj₀ h4.le hs.le (by norm_num : (4 : ℕ) ≠ 0)).mp h

theorem family_exponent (C c G rho : ℝ) :
    C * c * Real.sqrt (G * (4 * rho)) = 2 * (C * c * Real.sqrt (G * rho)) := by
  have : Real.sqrt (G * (4 * rho)) = 2 * Real.sqrt (G * rho) := by
    rw [show G * (4 * rho) = 2 ^ 2 * (G * rho) by ring, Real.sqrt_mul (by positivity),
      Real.sqrt_sq (by norm_num)]
  rw [this]; ring

/-! ### (b) cap-stiffness winding-charge model (U2) -/

noncomputable def Pcap (κ Λ c G : ℝ) : ℝ := κ ^ 2 * Λ * c ^ 4 / (64 * Real.pi ^ 2 * G)
noncomputable def alphaC (w κ Λ c G hbar ξ : ℝ) : ℝ := w * (2 * Pcap κ Λ c G * ξ ^ 2) * ξ ^ 2 / (hbar * c)

theorem alpha_c_form (w κ Λ c G hbar ξ : ℝ) (hc : 0 < c) (hG : 0 < G) (hbp : 0 < hbar) :
    alphaC w κ Λ c G hbar ξ
      = w * κ ^ 2 / (32 * Real.pi ^ 2) * (Λ * (hbar * G / c ^ 3)) * (ξ ^ 4 / (hbar * G / c ^ 3) ^ 2) := by
  have hπ : Real.pi ≠ 0 := Real.pi_ne_zero
  unfold alphaC Pcap
  field_simp
  ring

theorem alpha_c_cap (w s κ Λ c G hbar ξ : ℝ) (hc : 0 < c) (hbp : 0 < hbar)
    (hP3 : Pcap κ Λ c G * ξ ^ 4 = s * hbar * c) : alphaC w κ Λ c G hbar ξ = 2 * w * s := by
  unfold alphaC
  have hbc : hbar * c ≠ 0 := by positivity
  rw [show w * (2 * Pcap κ Λ c G * ξ ^ 2) * ξ ^ 2 = 2 * w * (Pcap κ Λ c G * ξ ^ 4) by ring, hP3]
  field_simp

theorem alpha_c_geo_mean (w κ Λ c G hbar ξ : ℝ) (hc : 0 < c) (hG : 0 < G) (hbp : 0 < hbar) (hΛ : 0 < Λ)
    (hξ : ξ ^ 4 = (hbar * G / c ^ 3) * (3 / Λ)) :
    alphaC w κ Λ c G hbar ξ = 3 * w * κ ^ 2 / (32 * Real.pi ^ 2) := by
  have hπ : Real.pi ≠ 0 := Real.pi_ne_zero
  rw [alpha_c_form w κ Λ c G hbar ξ hc hG hbp, hξ]
  field_simp

theorem alpha_c_rH (w κ Λ c G hbar ξ : ℝ) (hc : 0 < c) (hG : 0 < G) (hbp : 0 < hbar) (hΛ : 0 < Λ)
    (hξ : ξ ^ 4 = (3 / Λ) ^ 2) :
    alphaC w κ Λ c G hbar ξ
      = 9 * w * κ ^ 2 / (32 * Real.pi ^ 2) / (Λ * (hbar * G / c ^ 3)) := by
  have hπ : Real.pi ≠ 0 := Real.pi_ne_zero
  rw [alpha_c_form w κ Λ c G hbar ξ hc hG hbp, hξ]
  field_simp
  ring

theorem geo_mean_inverse_alpha (κ : ℝ) (hκ : 0 < κ) (α : ℝ) (hα : α = 3 * Real.pi * κ ^ 2 / (32 * Real.pi ^ 2)) :
    1 / α = Z ^ 2 / κ ^ 2 ∧ (κ = 1 / 2 → 1 / α = 4 * Z ^ 2) := by
  have hπ : 0 < Real.pi := Real.pi_pos
  have hZ2 : Z ^ 2 = 32 * Real.pi / 3 := by
    unfold Z; rw [Real.sq_sqrt (by positivity)]
  have h1 : 1 / α = Z ^ 2 / κ ^ 2 := by
    rw [hα, hZ2]; field_simp
  refine ⟨h1, fun h => ?_⟩
  rw [h1, h]; ring

/-! ### (c) induced photon coupling (J1) -/

theorem alpha_eff_value (e v N L eps α : ℝ) (he : e ≠ 0) (hv : v ≠ 0) (hN : N ≠ 0) (hL : L ≠ 0)
    (heps : eps = L * N * e ^ 2 / (12 * Real.pi ^ 2 * v)) (hα : α = e ^ 2 / (4 * Real.pi * eps * v)) :
    α = 3 * Real.pi / (N * L) := by
  have hπ : Real.pi ≠ 0 := Real.pi_ne_zero
  rw [hα, heps]; field_simp; ring

/-! ### (d) dS_2 fermions -/

theorem gf_zero_limit :
    Tendsto (fun μ : ℝ => 2 * μ / Real.sinh (2 * Real.pi * μ)) (𝓝[≠] 0) (𝓝 (1 / Real.pi)) := by
  have hπ : Real.pi ≠ 0 := Real.pi_ne_zero
  -- slope of mu -> sinh (2 pi mu) at 0
  have hd : HasDerivAt (fun μ : ℝ => Real.sinh (2 * Real.pi * μ)) (2 * Real.pi) 0 := by
    have h := ((hasDerivAt_id (0 : ℝ)).const_mul (2 * Real.pi)).sinh
    simpa using h
  have hs := hd.tendsto_slope_zero
  have hs' : Tendsto (fun μ : ℝ => Real.sinh (2 * Real.pi * μ) / μ) (𝓝[≠] 0) (𝓝 (2 * Real.pi)) := by
    refine hs.congr' ?_
    filter_upwards with μ
    simp [smul_eq_mul, div_eq_inv_mul]
  have hinv := (tendsto_const_nhds (x := (2 : ℝ))).div hs' (by positivity)
  have hlim : (2 : ℝ) / (2 * Real.pi) = 1 / Real.pi := by field_simp
  rw [hlim] at hinv
  refine hinv.congr' ?_
  filter_upwards [self_mem_nhdsWithin] with μ hμ
  have hμ' : μ ≠ 0 := hμ
  simp only [Pi.div_apply]
  by_cases hsh : Real.sinh (2 * Real.pi * μ) = 0
  · simp [hsh]
  · field_simp

theorem schwinger_exponent (s H c : ℝ) (t : ℝ) :
    HasDerivAt (fun t => -s * Real.exp (-s * t)) (s ^ 2 * Real.exp (-s * t)) t ∧
    HasDerivAt (fun t => Real.exp (-s * t)) (-s * Real.exp (-s * t)) t ∧
    (s ^ 2 * Real.exp (-s * t)) + H * (-s * Real.exp (-s * t)) + c * Real.exp (-s * t)
      = (s ^ 2 - H * s + c) * Real.exp (-s * t) := by
  have h1 : HasDerivAt (fun t : ℝ => Real.exp (-s * t)) (-s * Real.exp (-s * t)) t := by
    have h := ((hasDerivAt_id t).const_mul (-s)).exp
    simpa [mul_comm] using h
  refine ⟨?_, h1, by ring⟩
  have h := h1.const_mul (-s)
  have e : -s * (-s * Real.exp (-s * t)) = s ^ 2 * Real.exp (-s * t) := by ring
  rw [e] at h
  exact h

theorem schwinger_solves_iff (s H c : ℝ) (t : ℝ) :
    ((s ^ 2 * Real.exp (-s * t)) + H * (-s * Real.exp (-s * t)) + c * Real.exp (-s * t) = 0)
      ↔ s ^ 2 - H * s + c = 0 := by
  have hpos : 0 < Real.exp (-s * t) := Real.exp_pos _
  constructor
  · intro h
    have : (s ^ 2 - H * s + c) * Real.exp (-s * t) = 0 := by linarith
    exact (mul_eq_zero.mp this).resolve_right hpos.ne'
  · intro h
    have : (s ^ 2 - H * s + c) * Real.exp (-s * t) = 0 := by rw [h]; ring
    linarith

/-- with Delta = s/H and x = e^2/(pi H^2): Delta (1 - Delta) = x -/
theorem schwinger_delta (s H e2 : ℝ) (hH : H ≠ 0) :
    s ^ 2 - H * s + e2 / Real.pi = 0 ↔ (s / H) * (1 - s / H) = e2 / (Real.pi * H ^ 2) := by
  have hπ : Real.pi ≠ 0 := Real.pi_ne_zero
  constructor
  · intro h
    field_simp
    field_simp at h
    nlinarith [h]
  · intro h
    field_simp at h
    field_simp
    nlinarith [h]

theorem schwinger_real_iff (H x : ℝ) (hH : 0 < H) :
    (∃ s : ℝ, (s / H) * (1 - s / H) = x) ↔ x ≤ 1 / 4 := by
  constructor
  · rintro ⟨s, hs⟩
    nlinarith [sq_nonneg (s / H - 1 / 2)]
  · intro hx
    refine ⟨H * (1 / 2 + Real.sqrt (1 / 4 - x)), ?_⟩
    have h0 : 0 ≤ 1 / 4 - x := by linarith
    have hq := Real.sq_sqrt h0
    have : H * (1 / 2 + Real.sqrt (1 / 4 - x)) / H = 1 / 2 + Real.sqrt (1 / 4 - x) := by
      field_simp
    rw [this]
    nlinarith [hq]

theorem schwinger_roots_sum (x : ℝ) : (1 / 2 + Real.sqrt (1 / 4 - x)) + (1 / 2 - Real.sqrt (1 / 4 - x)) = 1 := by
  ring

end M2Unruh

#print axioms M2Unruh.unruh_matching
#print axioms M2Unruh.kappa_match_value
#print axioms M2Unruh.Z_eq
#print axioms M2Unruh.n_for_half
#print axioms M2Unruh.Z_between
#print axioms M2Unruh.Z_not_integer
#print axioms M2Unruh.n2_kappa
#print axioms M2Unruh.energy_matching_a4
#print axioms M2Unruh.energy_matching_exponent
#print axioms M2Unruh.family_exponent
#print axioms M2Unruh.alpha_c_form
#print axioms M2Unruh.alpha_c_cap
#print axioms M2Unruh.alpha_c_geo_mean
#print axioms M2Unruh.alpha_c_rH
#print axioms M2Unruh.geo_mean_inverse_alpha
#print axioms M2Unruh.alpha_eff_value
#print axioms M2Unruh.gf_zero_limit
#print axioms M2Unruh.schwinger_exponent
#print axioms M2Unruh.schwinger_solves_iff
#print axioms M2Unruh.schwinger_delta
#print axioms M2Unruh.schwinger_real_iff
#print axioms M2Unruh.schwinger_roots_sum
