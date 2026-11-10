import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Analysis.SpecialFunctions.Log.Deriv
import Mathlib.Tactic

/-!
# MK1: one dust constant μ_K for the CMB, clusters and galaxies (closed forms), 2026-11-10

Lane `fable52_push/MK1_one_dust_constant/` (criteria b1fbded1e2). The quadratic K(Q) = μ_K²(Q − 1)² of action (A).

1. FRW (QX17 K4): w(a) = w0/(w0 + a³), w0 = I0/(4 μ²).
   * `w_turnover`: w = 1/2 exactly where a³ = w0 (the dust turns dust-like there).
   * `w_strictAnti_mu`: at fixed a > 0 and I0 > 0, w strictly decreases as μ grows (so every "cold by z" line is a lower
     bound on μ).
   * `fb1_arith`: FB1's number, I0/4 = 3 (70/299792.458)² 0.26 / 4 lies in (1.0630e-8, 1.0632e-8) Mpc⁻².
2. Static dust in the deep-law field Φ = −(Φc + s ln(rc/r)) (units G = 1 inside the integral):
   * `deep_dust_hasDeriv`: F(r) = Φc r³/3 + s (r³/3 (ln rc − ln r) + r³/9) has derivative r² (Φc + s (ln rc − ln r)),
     i.e. F = ∫₀^r r'² |Φ| dr', the enclosed static dust over μ².
   * `dust_mono_mu`: M_K = μ² I with I ≥ 0 is monotone in μ ≥ 0.
3. The cap (form B):
   * `cap_law_relation`: on the law, ℓ = m_s/2 + √(m_s²/4 + m_s x²) = 1 + X forces m_s = (1 + X)²/(x² + 1 + X).
   * `cap_radius_anti`: in the deep limit ℓ = √(1 + κ) x, the cap radius x_c = (1 + X)/√(1 + κ) strictly decreases as the
     enclosed dust κ grows: dust makes the share end sooner.
4. Solar System (EW2 iter4): `saturn_mono`: dg = μ² (A + B) with A + B > 0 strictly increases in μ ≥ 0.
5. `no_window`: if a lower bound L exceeds an upper bound U, no μ satisfies both. Instances with the lane's numbers:
   `no_window_jeans_saturn` (Jeans line 25118 vs Saturn 6224), `no_window_background_sparc` (KD1 B1a 198 vs SPARC
   7.08), `no_window_background_groups` (198 vs the groups' upper end 1.514), `no_window_background_kids` (198 vs the
   capped KiDS bound).

κ = ½ FITTED; footings never pooled; the cold component is cold dark energy, no particle; not theory closed. Adopts nothing.
-/

open Real

namespace MK1

noncomputable def w0 (I0 μ : ℝ) : ℝ := I0 / (4 * μ ^ 2)
noncomputable def w (I0 μ a : ℝ) : ℝ := w0 I0 μ / (w0 I0 μ + a ^ 3)

theorem w_turnover (I0 μ a : ℝ) (h : a ^ 3 = w0 I0 μ) (hpos : 0 < w0 I0 μ) : w I0 μ a = 1 / 2 := by
  unfold w; rw [h]; field_simp; ring

theorem w0_strictAnti (I0 : ℝ) (hI : 0 < I0) {μ1 μ2 : ℝ} (h1 : 0 < μ1) (h12 : μ1 < μ2) :
    w0 I0 μ2 < w0 I0 μ1 := by
  unfold w0
  have h2 : 0 < μ2 := lt_trans h1 h12
  have hsq : μ1 ^ 2 < μ2 ^ 2 := by nlinarith
  apply div_lt_div_of_pos_left hI (by positivity) (by nlinarith)

theorem w_strictAnti_mu (I0 a : ℝ) (hI : 0 < I0) (ha : 0 < a) {μ1 μ2 : ℝ} (h1 : 0 < μ1) (h12 : μ1 < μ2) :
    w I0 μ2 a < w I0 μ1 a := by
  have h2 : 0 < μ2 := lt_trans h1 h12
  have hw := w0_strictAnti I0 hI h1 h12
  have p1 : 0 < w0 I0 μ1 := by unfold w0; positivity
  have p2 : 0 < w0 I0 μ2 := by unfold w0; positivity
  have ha3 : 0 < a ^ 3 := by positivity
  unfold w
  rw [div_lt_div_iff₀ (by positivity) (by positivity)]
  nlinarith

theorem fb1_arith :
    (10630 / 1000000000000 : ℝ) < 3 * (70 / 299792.458) ^ 2 * 0.26 / 4 ∧
    3 * (70 / 299792.458 : ℝ) ^ 2 * 0.26 / 4 < 10632 / 1000000000000 := by
  constructor <;> norm_num

/-- The enclosed static dust (over μ²) in the deep-law field: F' = r² (Φc + s (ln rc − ln r)). -/
noncomputable def F (Pc s rc r : ℝ) : ℝ := Pc * r ^ 3 / 3 + s * (r ^ 3 / 3 * (Real.log rc - Real.log r) + r ^ 3 / 9)

theorem deep_dust_hasDeriv (Pc s rc r : ℝ) (hr : 0 < r) :
    HasDerivAt (F Pc s rc) (r ^ 2 * (Pc + s * (Real.log rc - Real.log r))) r := by
  have hl : HasDerivAt Real.log r⁻¹ r := Real.hasDerivAt_log (ne_of_gt hr)
  have h3 : HasDerivAt (fun x : ℝ => x ^ 3) (3 * r ^ 2) r := by
    simpa using hasDerivAt_pow 3 r
  have hA : HasDerivAt (fun x : ℝ => Pc * x ^ 3 / 3) (Pc * (3 * r ^ 2) / 3) r := (h3.const_mul Pc).div_const 3
  have hB1 : HasDerivAt (fun x : ℝ => x ^ 3 / 3) (3 * r ^ 2 / 3) r := h3.div_const 3
  have hB2 : HasDerivAt (fun x : ℝ => Real.log rc - Real.log x) (0 - r⁻¹) r := (hasDerivAt_const r (Real.log rc)).sub hl
  have hB : HasDerivAt (fun x : ℝ => x ^ 3 / 3 * (Real.log rc - Real.log x))
      (3 * r ^ 2 / 3 * (Real.log rc - Real.log r) + r ^ 3 / 3 * (0 - r⁻¹)) r := hB1.mul hB2
  have hC : HasDerivAt (fun x : ℝ => x ^ 3 / 9) (3 * r ^ 2 / 9) r := h3.div_const 9
  have key : HasDerivAt (fun x : ℝ => Pc * x ^ 3 / 3 + s * (x ^ 3 / 3 * (Real.log rc - Real.log x) + x ^ 3 / 9))
      (Pc * (3 * r ^ 2) / 3 + s * (3 * r ^ 2 / 3 * (Real.log rc - Real.log r) + r ^ 3 / 3 * (0 - r⁻¹) + 3 * r ^ 2 / 9)) r :=
    hA.add ((hB.add hC).const_mul s)
  have hF : (F Pc s rc) = fun x => Pc * x ^ 3 / 3 + s * (x ^ 3 / 3 * (Real.log rc - Real.log x) + x ^ 3 / 9) := by
    funext x; rfl
  rw [hF]
  convert key using 1
  have hr0 : r ≠ 0 := hr.ne'
  field_simp
  ring

theorem dust_mono_mu {I μ1 μ2 : ℝ} (hI : 0 ≤ I) (h1 : 0 ≤ μ1) (h12 : μ1 ≤ μ2) : μ1 ^ 2 * I ≤ μ2 ^ 2 * I := by
  have : μ1 ^ 2 ≤ μ2 ^ 2 := by nlinarith
  exact mul_le_mul_of_nonneg_right this hI

theorem cap_law_relation {ms x X : ℝ} (hX : 0 < X) (hx : 0 < x) (hms : 0 < ms)
    (h : ms / 2 + Real.sqrt (ms ^ 2 / 4 + ms * x ^ 2) = 1 + X) :
    ms = (1 + X) ^ 2 / (x ^ 2 + 1 + X) := by
  have hs : Real.sqrt (ms ^ 2 / 4 + ms * x ^ 2) = 1 + X - ms / 2 := by linarith
  have hnn : 0 ≤ ms ^ 2 / 4 + ms * x ^ 2 := by positivity
  have hsq := Real.sq_sqrt hnn
  rw [hs] at hsq
  have hden : 0 < x ^ 2 + 1 + X := by positivity
  rw [eq_div_iff (ne_of_gt hden)]
  nlinarith [hsq]

noncomputable def xcap (X κ : ℝ) : ℝ := (1 + X) / Real.sqrt (1 + κ)

theorem cap_radius_anti {X κ1 κ2 : ℝ} (hX : 0 < X) (h1 : 0 ≤ κ1) (h12 : κ1 < κ2) :
    xcap X κ2 < xcap X κ1 := by
  unfold xcap
  have hs1 : 0 < Real.sqrt (1 + κ1) := Real.sqrt_pos.mpr (by linarith)
  have hs : Real.sqrt (1 + κ1) < Real.sqrt (1 + κ2) := Real.sqrt_lt_sqrt (by linarith) (by linarith)
  exact div_lt_div_of_pos_left (by linarith) hs1 hs

theorem saturn_mono {A B μ1 μ2 : ℝ} (hAB : 0 < A + B) (h1 : 0 ≤ μ1) (h12 : μ1 < μ2) :
    μ1 ^ 2 * (A + B) < μ2 ^ 2 * (A + B) := by
  have : μ1 ^ 2 < μ2 ^ 2 := by nlinarith
  exact mul_lt_mul_of_pos_right this hAB

theorem no_window {L U : ℝ} (h : U < L) : ¬ ∃ μ : ℝ, L ≤ μ ∧ μ ≤ U := by
  rintro ⟨μ, h1, h2⟩; linarith

/-- The record's CMB-lensing Jeans line (KD1 G9a, 25118 per Mpc) against the Saturn line (EW2, at most 6224 per Mpc). -/
theorem no_window_jeans_saturn : ¬ ∃ μ : ℝ, (25118 : ℝ) ≤ μ ∧ μ ≤ 6224 := no_window (by norm_num)

/-- KD1's background line B1a (198.24 per Mpc, both footings) against SPARC's capped upper end (7.08 / 5.62 per Mpc). -/
theorem no_window_background_sparc : ¬ ∃ μ : ℝ, (198 : ℝ) ≤ μ ∧ μ ≤ 7.08 := no_window (by norm_num)

/-- KD1's background line against the groups' window, whose upper end is 1.514 / 1.381 per Mpc. -/
theorem no_window_background_groups : ¬ ∃ μ : ℝ, (198 : ℝ) ≤ μ ∧ μ ≤ 1.514 := no_window (by norm_num)

/-- KD1's background line against the capped KiDS bound (1.00 / 0.765 per Mpc), and the Jeans line against it. -/
theorem no_window_background_kids : ¬ ∃ μ : ℝ, (198 : ℝ) ≤ μ ∧ μ ≤ 1 := no_window (by norm_num)

theorem no_window_jeans_kids : ¬ ∃ μ : ℝ, (25118 : ℝ) ≤ μ ∧ μ ≤ 1 := no_window (by norm_num)

end MK1

#print axioms MK1.w_turnover
#print axioms MK1.w_strictAnti_mu
#print axioms MK1.fb1_arith
#print axioms MK1.deep_dust_hasDeriv
#print axioms MK1.dust_mono_mu
#print axioms MK1.cap_law_relation
#print axioms MK1.cap_radius_anti
#print axioms MK1.saturn_mono
#print axioms MK1.no_window
#print axioms MK1.no_window_jeans_saturn
#print axioms MK1.no_window_background_sparc
#print axioms MK1.no_window_background_groups
#print axioms MK1.no_window_background_kids
#print axioms MK1.no_window_jeans_kids
-- κ = ½ FITTED; not theory closed. Adopts nothing.
