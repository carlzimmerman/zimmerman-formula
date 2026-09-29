import Mathlib

/-!
# M6-C -- FP22 check B1: the zero-field runaway with gas pressure -- one growing root at every k, rate saturating

Source: `real_research/derivation_chain_2026/FP22_who_feels_mond.py`, part B1 (lines 596-609 sympy block; the check
at 640-644).  The baryon-phi block, gravity terms dropped, has the dispersion
        s^2 + c_s^2 K^2 s - K^2 c^2 Gamma_b/lambda = 0,        s = Gamma^2,
and the script reports (sympy): the product of the roots is -K^2 c^2 Gamma_b/lambda < 0 (one growing mode at every
K), and the positive root tends, as K -> infinity, to  c^2 Gamma_b/(lambda c_s^2)  ("pressure saturates the rate
at Gamma_inf = (c/c_s) sqrt(Gamma_b/lambda_eff) instead of stopping it").  The script proves neither the
boundedness nor the monotonicity of the root: it prints the limit.

Corpus check (2026-09-29): `git grep -n -i -e runaway -e saturat -- '*.lean'` finds no lean file on this
quadratic (only unrelated `saturates` hits and an I13 pulsation file).  New.

Write  a := c_s^2 K^2  and  B := beta K^2  with  beta := c^2 Gamma_b/lambda > 0  (c_s, K, c, Gamma_b, lambda > 0).
CERTIFIED:
  * `splus_root`       : s+ = (-a + sqrt(a^2 + 4B))/2 solves s^2 + a s - B = 0;  `sminus_root` likewise for s-;
  * `roots_product`    : s+ * s- = -B < 0, `splus_pos`, `sminus_neg`: exactly one positive root;
  * `only_positive_root` : any real root s > 0 of the quadratic equals s+;
  * `splus_lt_cap`     : s+(K) < beta/c_s^2 for every K > 0  (the pressure cap: Gamma^2 never exceeds
                         c^2 Gamma_b/(lambda c_s^2));
  * `splus_strictMono` : K -> s+(K) is strictly increasing on K > 0;
  * `splus_tendsto`    : s+(K) -> beta/c_s^2 as K -> infinity  (the script's `lim`).
NOT CERTIFIED: that this 2x2 block is the right truncation of the full 3x3 (baryons, dark, phi, gravity); the
identification of c_s, Gamma_b = 4 pi G rho_b, lambda_eff (FP14/XR26 readings) or any number (3 H ... thousands of H);
that the runaway is physical or absent in the true theory.  It is a statement about a stated quadratic only.
No empirical premise; kappa = 1/2 is unrelated.
-/

noncomputable section
namespace M6C

open Real Filter Topology

/-- the positive root of s^2 + a s - B = 0 -/
def splus (a B : ℝ) : ℝ := (-a + Real.sqrt (a ^ 2 + 4 * B)) / 2
/-- the negative root -/
def sminus (a B : ℝ) : ℝ := (-a - Real.sqrt (a ^ 2 + 4 * B)) / 2

theorem splus_root (a B : ℝ) (hB : 0 ≤ B) : splus a B ^ 2 + a * splus a B - B = 0 := by
  have h := Real.sq_sqrt (show (0:ℝ) ≤ a ^ 2 + 4 * B by positivity)
  unfold splus
  nlinarith [h]

theorem sminus_root (a B : ℝ) (hB : 0 ≤ B) : sminus a B ^ 2 + a * sminus a B - B = 0 := by
  have h := Real.sq_sqrt (show (0:ℝ) ≤ a ^ 2 + 4 * B by positivity)
  unfold sminus
  nlinarith [h]

theorem roots_product (a B : ℝ) (hB : 0 ≤ B) : splus a B * sminus a B = B := by
  have h := Real.sq_sqrt (show (0:ℝ) ≤ a ^ 2 + 4 * B by positivity)
  unfold splus sminus
  nlinarith [h]

theorem sqrt_gt (a B : ℝ) (_ha : 0 ≤ a) (hB : 0 < B) : a < Real.sqrt (a ^ 2 + 4 * B) := by
  apply Real.lt_sqrt_of_sq_lt
  linarith

theorem splus_pos (a B : ℝ) (ha : 0 ≤ a) (hB : 0 < B) : 0 < splus a B := by
  unfold splus
  have := sqrt_gt a B ha hB
  linarith

theorem sminus_neg (a B : ℝ) (ha : 0 ≤ a) (hB : 0 < B) : sminus a B < 0 := by
  unfold sminus
  have := Real.sqrt_nonneg (a ^ 2 + 4 * B)
  have := sqrt_gt a B ha hB
  linarith

theorem only_positive_root (a B s : ℝ) (ha : 0 ≤ a) (hB : 0 < B) (hs : 0 < s)
    (h : s ^ 2 + a * s - B = 0) : s = splus a B := by
  have hp := roots_product a B hB.le
  have hm := sminus_neg a B ha hB
  have h1 := splus_root a B hB.le
  have h2 := sminus_root a B hB.le
  have hfac : (s - splus a B) * (s - sminus a B) = 0 := by
    have hsum : splus a B + sminus a B = -a := by unfold splus sminus; ring
    nlinarith [hsum, hp]
  rcases mul_eq_zero.1 hfac with h0 | h0
  · linarith
  · exfalso; linarith

/-- s+ = 2B/(a + sqrt(a^2+4B)) -/
theorem splus_eq (a B : ℝ) (ha : 0 ≤ a) (hB : 0 < B) :
    splus a B = 2 * B / (a + Real.sqrt (a ^ 2 + 4 * B)) := by
  have h := Real.sq_sqrt (show (0:ℝ) ≤ a ^ 2 + 4 * B by positivity)
  have hs := Real.sqrt_nonneg (a ^ 2 + 4 * B)
  have hpos : 0 < a + Real.sqrt (a ^ 2 + 4 * B) := by
    have := sqrt_gt a B ha hB; linarith
  rw [eq_div_iff hpos.ne']
  unfold splus
  nlinarith [h]

theorem splus_lt_cap (cs2 beta K : ℝ) (hcs : 0 < cs2) (hb : 0 < beta) (hK : 0 < K) :
    splus (cs2 * K ^ 2) (beta * K ^ 2) < beta / cs2 := by
  have ha : 0 ≤ cs2 * K ^ 2 := by positivity
  have hB : 0 < beta * K ^ 2 := by positivity
  rw [splus_eq _ _ ha hB]
  have hsq := sqrt_gt _ _ ha hB
  have hpos : 0 < cs2 * K ^ 2 + Real.sqrt ((cs2 * K ^ 2) ^ 2 + 4 * (beta * K ^ 2)) := by linarith
  rw [div_lt_div_iff₀ hpos hcs]
  have hK2 : 0 < K ^ 2 := by positivity
  nlinarith [mul_pos hb hK2, mul_pos hcs hK2, mul_lt_mul_of_pos_left hsq (mul_pos hb hcs)]

/-- the closed form used for monotonicity and the limit -/
theorem splus_scaled (cs2 beta K : ℝ) (hcs : 0 < cs2) (hb : 0 < beta) (hK : 0 < K) :
    splus (cs2 * K ^ 2) (beta * K ^ 2) =
      2 * beta / (cs2 + Real.sqrt (cs2 ^ 2 + 4 * beta * (K ^ 2)⁻¹)) := by
  have ha : 0 ≤ cs2 * K ^ 2 := by positivity
  have hB : 0 < beta * K ^ 2 := by positivity
  rw [splus_eq _ _ ha hB]
  have hK2 : 0 < K ^ 2 := by positivity
  have hs : Real.sqrt ((cs2 * K ^ 2) ^ 2 + 4 * (beta * K ^ 2)) =
      K ^ 2 * Real.sqrt (cs2 ^ 2 + 4 * beta * (K ^ 2)⁻¹) := by
    have h1 : (cs2 * K ^ 2) ^ 2 + 4 * (beta * K ^ 2) = (K ^ 2) ^ 2 * (cs2 ^ 2 + 4 * beta * (K ^ 2)⁻¹) := by
      field_simp
    rw [h1, Real.sqrt_mul (by positivity), Real.sqrt_sq hK2.le]
  rw [hs]
  have hpos : 0 < cs2 + Real.sqrt (cs2 ^ 2 + 4 * beta * (K ^ 2)⁻¹) := by
    have := Real.sqrt_nonneg (cs2 ^ 2 + 4 * beta * (K ^ 2)⁻¹); linarith
  field_simp

theorem splus_strictMono (cs2 beta : ℝ) (hcs : 0 < cs2) (hb : 0 < beta) {K L : ℝ} (hK : 0 < K) (hKL : K < L) :
    splus (cs2 * K ^ 2) (beta * K ^ 2) < splus (cs2 * L ^ 2) (beta * L ^ 2) := by
  have hL : 0 < L := hK.trans hKL
  rw [splus_scaled cs2 beta K hcs hb hK, splus_scaled cs2 beta L hcs hb hL]
  have hi : (L ^ 2)⁻¹ < (K ^ 2)⁻¹ := by
    apply inv_strictAnti₀ (by positivity)
    exact pow_lt_pow_left₀ hKL hK.le (by norm_num)
  have hs : Real.sqrt (cs2 ^ 2 + 4 * beta * (L ^ 2)⁻¹) < Real.sqrt (cs2 ^ 2 + 4 * beta * (K ^ 2)⁻¹) := by
    apply Real.sqrt_lt_sqrt (by positivity)
    nlinarith [mul_pos hb (sub_pos.2 hi)]
  have hpos : 0 < cs2 + Real.sqrt (cs2 ^ 2 + 4 * beta * (L ^ 2)⁻¹) := by
    have := Real.sqrt_nonneg (cs2 ^ 2 + 4 * beta * (L ^ 2)⁻¹); linarith
  apply div_lt_div_of_pos_left (by positivity) hpos
  linarith

theorem splus_tendsto (cs2 beta : ℝ) (hcs : 0 < cs2) (hb : 0 < beta) :
    Tendsto (fun K : ℝ => splus (cs2 * K ^ 2) (beta * K ^ 2)) atTop (𝓝 (beta / cs2)) := by
  have h0 : Tendsto (fun K : ℝ => (K ^ 2)⁻¹) atTop (𝓝 0) :=
    tendsto_inv_atTop_zero.comp (tendsto_pow_atTop (by norm_num))
  have h1 : Tendsto (fun K : ℝ => cs2 + Real.sqrt (cs2 ^ 2 + 4 * beta * (K ^ 2)⁻¹)) atTop
      (𝓝 (cs2 + Real.sqrt (cs2 ^ 2 + 4 * beta * 0))) := by
    apply Tendsto.const_add
    apply (Real.continuous_sqrt.tendsto _).comp
    exact Tendsto.const_add _ (Tendsto.const_mul _ h0)
  have hlim : cs2 + Real.sqrt (cs2 ^ 2 + 4 * beta * 0) = 2 * cs2 := by
    have : Real.sqrt (cs2 ^ 2 + 4 * beta * 0) = cs2 := by
      rw [show cs2 ^ 2 + 4 * beta * 0 = cs2 ^ 2 by ring, Real.sqrt_sq hcs.le]
    linarith
  rw [hlim] at h1
  have h2 := (tendsto_const_nhds (x := 2 * beta)).div h1 (by positivity)
  have h3 : 2 * beta / (2 * cs2) = beta / cs2 := by field_simp
  rw [h3] at h2
  refine h2.congr' ?_
  filter_upwards [eventually_gt_atTop 0] with K hK
  exact (splus_scaled cs2 beta K hcs hb hK).symm

end M6C

end

#print axioms M6C.splus_root
#print axioms M6C.roots_product
#print axioms M6C.only_positive_root
#print axioms M6C.splus_lt_cap
#print axioms M6C.splus_strictMono
#print axioms M6C.splus_tendsto
