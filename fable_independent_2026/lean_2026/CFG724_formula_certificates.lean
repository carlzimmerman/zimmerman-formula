import Mathlib

/-!
# CFG724: Lean certificates for the cold-energy formula itself

Criteria: campaign_fresh_gravity/CFG724_lean_formula_certificates/FROZEN_CRITERIA.md (7b2193b05), committed before this file.
The formula (COLD_ENERGY_FULL_FORMULA_2026-10-13.md): M_total = ν(g_N/a₀)·M_b + k·M_hot, with the other chat's C* static law
g_N = g²/(g + a₀), saturating polarization u = a₀g/(a₀ + g) and vacuum potential W(u) = −(a₀/K)[u + a₀ ln(1 − u/a₀)], K = 4πG.

CERTIFIED (mathematics from stated premises):
* `law_inversion`: g > 0 ∧ g_N = g²/(g + a₀) ⇔ g = (g_N + √(g_N² + 4a₀g_N))/2 (g_N, a₀ > 0).
* `saturation_bounds`, `saturation_mono`: 0 < a₀g/(a₀ + g) < a₀ and strictly increasing in g > 0.
* `W_deriv`, `static_law_from_W`, `W_strictly_convex`: W′(u) = u a₀/(K(a₀ − u)) on (0, a₀); K·W′(u) = g ⇔ u = a₀g/(a₀ + g); W′ strictly
  increasing on (0, a₀) (positive second variation).
* `btfr_limit`: r·g(r) → √(G M a₀) as r → ∞ for a point mass (the flat rotation curve / baryonic Tully–Fisher relation as a limit).
* `settled_mass_linear`: M_c(<r)/r → √(M a₀/G) for M_c(<r) = r²g(r)/G − M.
* `supply_edge`: 1/(eˣ − 1) = S ⇔ x = ln(1 + 1/S) for S > 0 (ν_mono supply edge, r_edge = r_M / ln(1 + f_ret f_b/(1 − f_b))).
* `sis_hydrostatic`, `sis_btfr`: ρ = σ²/(2πGr²) with M = 2σ²r/G is in hydrostatic balance; V² = 2σ², V⁴ = GMa₀ ⇒ σ⁴ = GMa₀/4.
* `clock_family_closed`: for 1 < R ≤ 3.15, −ln(1 − 1/√R)·17.528 ≥ 13.8 (CFG666, canonical: the cosmic clock needs longer than 13.8 Gyr).

NOT certified: that the law, k, κ or the C* action are physically correct; the hot-gas selector; any data verdict. κ = ½ is FITTED; nothing
here says the theory is closed.
-/

open Filter Topology Real

namespace CFG724

/-- F1: inversion of the C* static law. -/
theorem law_inversion {gN a0 g : ℝ} (hgN : 0 < gN) (ha : 0 < a0) :
    (0 < g ∧ gN = g ^ 2 / (g + a0)) ↔ g = (gN + √(gN ^ 2 + 4 * a0 * gN)) / 2 := by
  have hD : 0 ≤ gN ^ 2 + 4 * a0 * gN := by positivity
  have hs2 : (√(gN ^ 2 + 4 * a0 * gN)) ^ 2 = gN ^ 2 + 4 * a0 * gN := Real.sq_sqrt hD
  have hs0 : 0 ≤ √(gN ^ 2 + 4 * a0 * gN) := Real.sqrt_nonneg _
  have hsgt : gN < √(gN ^ 2 + 4 * a0 * gN) := by nlinarith
  constructor
  · rintro ⟨hg, h⟩
    have hga : g + a0 ≠ 0 := by linarith
    have hq : g ^ 2 = gN * (g + a0) := by field_simp at h; linarith
    set s := √(gN ^ 2 + 4 * a0 * gN)
    have hprod : (2 * g - gN - s) * (2 * g - gN + s) = 0 := by nlinarith
    rcases mul_eq_zero.mp hprod with h1 | h1
    · linarith
    · nlinarith
  · intro h
    set s := √(gN ^ 2 + 4 * a0 * gN)
    have hg : 0 < g := by rw [h]; linarith
    refine ⟨hg, ?_⟩
    have hga : 0 < g + a0 := by linarith
    rw [eq_div_iff hga.ne']
    rw [h]; nlinarith

/-- F2: the polarization saturates below a₀. -/
theorem saturation_bounds {a0 g : ℝ} (ha : 0 < a0) (hg : 0 < g) :
    0 < a0 * g / (a0 + g) ∧ a0 * g / (a0 + g) < a0 := by
  have h : 0 < a0 + g := by linarith
  refine ⟨by positivity, ?_⟩
  rw [div_lt_iff₀ h]; nlinarith

/-- F2: and it increases with the field. -/
theorem saturation_mono {a0 g1 g2 : ℝ} (ha : 0 < a0) (h1 : 0 < g1) (h12 : g1 < g2) :
    a0 * g1 / (a0 + g1) < a0 * g2 / (a0 + g2) := by
  have hp1 : 0 < a0 + g1 := by linarith
  have hp2 : 0 < a0 + g2 := by linarith
  have hk := mul_lt_mul_of_pos_left h12 (mul_pos ha ha)
  rw [div_lt_div_iff₀ hp1 hp2]; nlinarith [hk]

/-- the vacuum potential of C* -/
noncomputable def W (K a0 u : ℝ) : ℝ := -(a0 / K) * (u + a0 * Real.log (1 - u / a0))

/-- F3: its derivative on (0, a₀). -/
theorem W_deriv {K a0 u : ℝ} (hK : K ≠ 0) (ha : 0 < a0) (hu0 : 0 < u) (hu1 : u < a0) :
    HasDerivAt (W K a0) (u * a0 / (K * (a0 - u))) u := by
  have hpos : 0 < 1 - u / a0 := by rw [sub_pos, div_lt_one ha]; exact hu1
  have h1 : HasDerivAt (fun x => 1 - x / a0) (-(1 / a0)) u := by
    simpa using ((hasDerivAt_id' u).div_const a0).const_sub 1
  have h2 := h1.log hpos.ne'
  have h3 := ((hasDerivAt_id' u).add (h2.const_mul a0)).const_mul (-(a0 / K))
  have hne : a0 - u ≠ 0 := by linarith
  have hne2 : a0 ≠ 0 := ha.ne'
  refine (h3.congr_deriv ?_)
  field_simp
  ring

/-- F3b: the static field equation of C* is the law's saturating relation. -/
theorem static_law_from_W {K a0 u g : ℝ} (hK : K ≠ 0) (ha : 0 < a0) (hu0 : 0 < u) (hu1 : u < a0) (hg : 0 < g) :
    K * (u * a0 / (K * (a0 - u))) = g ↔ u = a0 * g / (a0 + g) := by
  have hne : a0 - u ≠ 0 := by linarith
  have hag : a0 + g ≠ 0 := by linarith
  have hs : K * (u * a0 / (K * (a0 - u))) = u * a0 / (a0 - u) := by field_simp
  rw [hs, div_eq_iff hne, eq_div_iff hag]
  constructor <;> intro h <;> linear_combination h

/-- F3c: W′ strictly increasing on (0, a₀): the vacuum is stable there. -/
theorem W_strictly_convex {K a0 : ℝ} (hK : 0 < K) (ha : 0 < a0) :
    StrictMonoOn (fun u => u * a0 / (K * (a0 - u))) (Set.Ioo 0 a0) := by
  intro u1 hu1 u2 hu2 h12
  simp only
  have d1 : 0 < K * (a0 - u1) := mul_pos hK (by linarith [hu1.2])
  have d2 : 0 < K * (a0 - u2) := mul_pos hK (by linarith [hu2.2])
  have hk := mul_lt_mul_of_pos_left h12 (mul_pos (mul_pos hK ha) ha)
  rw [div_lt_div_iff₀ d1 d2]
  nlinarith [hk]

/-- the C* field of a point mass at radius r -/
noncomputable def gpm (G M a0 r : ℝ) : ℝ :=
  (G * M / r ^ 2 + √((G * M / r ^ 2) ^ 2 + 4 * a0 * (G * M / r ^ 2))) / 2

/-- r·g(r) written through t = 1/r -/
noncomputable def vsq (G M a0 t : ℝ) : ℝ := G * M * t / 2 + √((G * M * t) ^ 2 + 4 * a0 * G * M) / 2

lemma vsq_eq {G M a0 r : ℝ} (hr : 0 < r) : r * gpm G M a0 r = vsq G M a0 r⁻¹ := by
  unfold gpm vsq
  have hr0 : r ≠ 0 := hr.ne'
  have hsq : r * √((G * M / r ^ 2) ^ 2 + 4 * a0 * (G * M / r ^ 2)) = √((G * M * r⁻¹) ^ 2 + 4 * a0 * G * M) := by
    have hY : (G * M * r⁻¹) ^ 2 + 4 * a0 * G * M = r ^ 2 * ((G * M / r ^ 2) ^ 2 + 4 * a0 * (G * M / r ^ 2)) := by
      field_simp
      try ring
    rw [hY, Real.sqrt_mul (sq_nonneg r), Real.sqrt_sq hr.le]
  have : r * ((G * M / r ^ 2 + √((G * M / r ^ 2) ^ 2 + 4 * a0 * (G * M / r ^ 2))) / 2)
      = (r * (G * M / r ^ 2)) / 2 + (r * √((G * M / r ^ 2) ^ 2 + 4 * a0 * (G * M / r ^ 2))) / 2 := by ring
  rw [this, hsq]
  congr 1
  field_simp
  try ring

/-- F4: the baryonic Tully–Fisher relation as a limit: v² = r g(r) → √(G M a₀). -/
theorem btfr_limit {G M a0 : ℝ} (hG : 0 < G) (hM : 0 < M) (ha : 0 < a0) :
    Tendsto (fun r => r * gpm G M a0 r) atTop (𝓝 (√(G * M * a0))) := by
  have hcont : Continuous (vsq G M a0) := by unfold vsq; fun_prop
  have h0 : vsq G M a0 0 = √(G * M * a0) := by
    unfold vsq
    have : (G * M * 0) ^ 2 + 4 * a0 * G * M = 2 ^ 2 * (G * M * a0) := by ring
    rw [this, Real.sqrt_mul (by norm_num), Real.sqrt_sq (by norm_num)]
    ring
  have hlim : Tendsto (fun r : ℝ => vsq G M a0 r⁻¹) atTop (𝓝 (√(G * M * a0))) := by
    rw [← h0]
    exact (hcont.tendsto 0).comp tendsto_inv_atTop_zero
  refine hlim.congr' ?_
  filter_upwards [eventually_gt_atTop 0] with r hr
  exact (vsq_eq hr).symm

/-- F5: the settled cold mass grows linearly, M_c(<r)/r → √(M a₀/G). -/
theorem settled_mass_linear {G M a0 : ℝ} (hG : 0 < G) (hM : 0 < M) (ha : 0 < a0) :
    Tendsto (fun r => (r ^ 2 * gpm G M a0 r / G - M) / r) atTop (𝓝 (√(M * a0 / G))) := by
  have hval : √(M * a0 / G) = √(G * M * a0) / G - 0 := by
    have : M * a0 / G = (G * M * a0) / G ^ 2 := by field_simp; try ring
    rw [this, Real.sqrt_div' _ (sq_nonneg G), Real.sqrt_sq hG.le, sub_zero]
  rw [hval]
  have h1 := (btfr_limit hG hM ha).div_const G
  have h2 : Tendsto (fun r : ℝ => M / r) atTop (𝓝 0) := tendsto_const_nhds.div_atTop tendsto_id
  refine (h1.sub h2).congr' ?_
  filter_upwards [eventually_gt_atTop 0] with r hr
  field_simp
  try ring

/-- F6: the ν_mono supply edge. -/
theorem supply_edge {S x : ℝ} (hS : 0 < S) : 1 / (Real.exp x - 1) = S ↔ x = Real.log (1 + 1 / S) := by
  constructor
  · intro h
    have hne : Real.exp x - 1 ≠ 0 := by
      intro h0; rw [h0, div_zero] at h; linarith
    have he : Real.exp x = 1 + 1 / S := by
      field_simp at h ⊢; linarith
    rw [← he, Real.log_exp]
  · intro h
    have hpos : 0 < 1 + 1 / S := by positivity
    rw [h, Real.exp_log hpos, add_sub_cancel_left, one_div_one_div]

/-- F7: the singular isothermal sphere is in hydrostatic balance. -/
theorem sis_hydrostatic {σ G r : ℝ} (hG : G ≠ 0) (hr : r ≠ 0) :
    HasDerivAt (fun x => σ ^ 2 / (2 * π * G * x ^ 2) * σ ^ 2)
      (-(σ ^ 2 / (2 * π * G * r ^ 2)) * G * (2 * σ ^ 2 * r / G) / r ^ 2) r := by
  have hπ : π ≠ 0 := Real.pi_ne_zero
  have hden : HasDerivAt (fun x => 2 * π * G * x ^ 2) (2 * π * G * (2 * r)) r := by
    simpa using (hasDerivAt_pow 2 r).const_mul (2 * π * G)
  have hne : 2 * π * G * r ^ 2 ≠ 0 := by positivity
  have h := ((hden.inv hne).const_mul (σ ^ 2)).mul_const (σ ^ 2)
  refine (h.congr_of_eventuallyEq (Filter.Eventually.of_forall fun y => by simp [div_eq_mul_inv])).congr_deriv ?_
  field_simp
  try ring

/-- F7b: with V² = 2σ², the Tully–Fisher law fixes the halo temperature. -/
theorem sis_btfr {V2 σ2 G M a0 : ℝ} (hV : V2 = 2 * σ2) (hT : V2 ^ 2 = G * M * a0) : σ2 ^ 2 = G * M * a0 / 4 := by
  subst hV; nlinarith

/-- exp y ≤ 1/(1 − y) on [0, 1) -/
lemma exp_le_inv_one_sub {y : ℝ} (hy1 : y < 1) : Real.exp y ≤ 1 / (1 - y) := by
  have h := Real.add_one_le_exp (-y)
  rw [Real.exp_neg] at h
  have hp : 0 < 1 - y := by linarith
  rw [le_div_iff₀ hp]
  have he : 0 < Real.exp y := Real.exp_pos y
  have : (1 - y) * Real.exp y ≤ 1 := by
    have := mul_le_mul_of_nonneg_right h he.le
    rw [inv_mul_cancel₀ he.ne'] at this
    linarith
  linarith

/-- F8: CFG666 canonical — a shape-allowed true scale (R ≤ 3.15) needs a settling time beyond 13.8 Gyr at the rate H_Λ. -/
theorem clock_family_closed {R : ℝ} (h1 : 1 < R) (h2 : R ≤ 3.15) :
    13.8 ≤ -Real.log (1 - 1 / √R) * 17.528 := by
  have hsR1 : 1 < √R := by rw [Real.lt_sqrt (by norm_num)]; linarith
  have hs : √R ≤ 1.77483 := by
    have : R ≤ (1.77483 : ℝ) ^ 2 := by norm_num; linarith
    calc √R ≤ √((1.77483 : ℝ) ^ 2) := Real.sqrt_le_sqrt this
      _ = 1.77483 := Real.sqrt_sq (by norm_num)
  have hspos : 0 < √R := by linarith
  have hf : 1 / 1.77483 ≤ 1 / √R := one_div_le_one_div_of_le hspos hs
  have hflt : 1 / √R < 1 := by rw [div_lt_one hspos]; exact hsR1
  have hpos : 0 < 1 - 1 / √R := by linarith
  set c : ℝ := 13.8 / 17.528 with hc
  have hexp : Real.exp c ≤ 2.243 := by
    have hc16 : Real.exp c = Real.exp (c / 16) ^ 16 := by
      rw [← Real.exp_nat_mul]; congr 1; push_cast; ring
    have hb : Real.exp (c / 16) ≤ 1 / (1 - c / 16) := exp_le_inv_one_sub (by rw [hc]; norm_num)
    have hb16 : Real.exp (c / 16) ^ 16 ≤ (1 / (1 - c / 16)) ^ 16 :=
      pow_le_pow_left₀ (Real.exp_pos _).le hb 16
    rw [hc16]
    refine le_trans hb16 ?_
    rw [hc]; norm_num
  have hlow : 1 / 2.243 ≤ Real.exp (-c) := by
    rw [Real.exp_neg]
    exact one_div_le_one_div_of_le (Real.exp_pos c) hexp |>.trans_eq (one_div _)
  have hle : 1 - 1 / √R ≤ Real.exp (-c) := by
    have : 1 - 1 / √R ≤ 1 - 1 / 1.77483 := by linarith
    refine le_trans this (le_trans ?_ hlow)
    norm_num
  have hlog : Real.log (1 - 1 / √R) ≤ -c := (Real.log_le_iff_le_exp hpos).mpr hle
  rw [hc] at hlog
  nlinarith

end CFG724

open CFG724 in
#print axioms law_inversion
open CFG724 in
#print axioms saturation_bounds
open CFG724 in
#print axioms saturation_mono
open CFG724 in
#print axioms W_deriv
open CFG724 in
#print axioms static_law_from_W
open CFG724 in
#print axioms W_strictly_convex
open CFG724 in
#print axioms btfr_limit
open CFG724 in
#print axioms settled_mass_linear
open CFG724 in
#print axioms supply_edge
open CFG724 in
#print axioms sis_hydrostatic
open CFG724 in
#print axioms sis_btfr
open CFG724 in
#print axioms clock_family_closed
