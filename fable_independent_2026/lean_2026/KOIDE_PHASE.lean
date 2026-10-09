import Mathlib

/-!
# KOIDE_PHASE -- the phase door: can the Koide hierarchy phase be set by geometry, and is it 2/9?

Koide form: √m_k = A (1 + r cos(δ + 2πk/3)).  KOIDE_TRIALITY_45 fixed the amplitude door (r = √2 ⇔ Q = 2/3);
its D4 construction gave the right Q with phase 30°, the wrong hierarchy.  This file is the phase door.
Source: scratch phase.py / phase2.py / phase3.py (mpmath, 30 digits).

CERTIFIED:
(A) `z3_sums`: Σ cos θ_k = 0, Σ cos² θ_k = 3/2, Σ cos³ θ_k = (3/4) cos 3δ (θ_k = δ, δ ± 2π/3).  Hence
    `Q_phase_free`: Q = Σx²/(Σx)² = 1/3 + r²/6 never sees δ, and `p3_phase`: Σx³ = 3 + (9/2) r² + (3/4) r³ cos 3δ,
    so the phase enters the spectrum ONLY through the Z3 invariant cos 3δ.  (A D4/tesseract lattice direction
    gives 3δ a multiple of 90°, cos 3δ ∈ {0, ±1}; the leptons have 3δ ≈ 0.6667 rad, cos 3δ ≈ 0.7859.)
(B) `cos_sin_bound`: order-8 Taylor bounds for cos and sin on |t| ≤ 1 (from Mathlib's Complex.exp_bound).
(C) `brannen_and_koide_incompatible`: if r = √2 (Koide exact) AND δ = 2/9 (Brannen exact), then
    m_μ/m_e = (x_μ/x_e)² > 206.769, while the measured `measured_ratio_upper` gives
    (105.6583755 + 0.0000023)/0.51099895 < 206.7683.  The two exact hypotheses cannot both hold at pole masses
    (the scratch number is 452σ: with r = √2, m_μ/m_e fixes δ = 0.2222220471 ± 4e-10, not 2/9).
NOT CERTIFIED: the scratch values (δ from data, the tau-mass predictions 1776.969 / 1776.9665 / 1776.967 MeV for
Koide-exact / Brannen-exact / 3δ = Q, all within 0.4σ of PDG 2024 1776.93 ± 0.09, which is RECALLED, not
re-fetched); the masses (PDG, quoted); the Lindemann statement that cos(2/3) is transcendental (Mathlib does not
yet have Lindemann-Weierstrass), which is why no polynomial potential with algebraic couplings can put 3δ at
exactly 2/3 rad.
-/

namespace KoidePhase
open Real

lemma cos_two_pi_div_three : cos (2 * π / 3) = -1 / 2 := by
  have : 2 * π / 3 = π - π / 3 := by ring
  rw [this, cos_pi_sub, cos_pi_div_three]; norm_num

lemma sin_two_pi_div_three : sin (2 * π / 3) = √3 / 2 := by
  have : 2 * π / 3 = π - π / 3 := by ring
  rw [this, sin_pi_sub, sin_pi_div_three]

lemma c1_eq (d : ℝ) : cos (d + 2 * π / 3) = cos d * (-1 / 2) - sin d * (√3 / 2) := by
  rw [cos_add, cos_two_pi_div_three, sin_two_pi_div_three]

lemma c2_eq (d : ℝ) : cos (d - 2 * π / 3) = cos d * (-1 / 2) + sin d * (√3 / 2) := by
  rw [cos_sub, cos_two_pi_div_three, sin_two_pi_div_three]

theorem z3_sums (d : ℝ) :
    cos d + cos (d + 2 * π / 3) + cos (d - 2 * π / 3) = 0 ∧
    cos d ^ 2 + cos (d + 2 * π / 3) ^ 2 + cos (d - 2 * π / 3) ^ 2 = 3 / 2 ∧
    cos d ^ 3 + cos (d + 2 * π / 3) ^ 3 + cos (d - 2 * π / 3) ^ 3 = (3 / 4) * cos (3 * d) := by
  have h3 : √3 ^ 2 = 3 := sq_sqrt (by norm_num)
  have hs : sin d ^ 2 = 1 - cos d ^ 2 := by rw [← sin_sq_add_cos_sq d]; ring
  rw [c1_eq, c2_eq, cos_three_mul]
  refine ⟨by ring, ?_, ?_⟩
  · linear_combination (sin d ^ 2 / 2) * h3 + (3 / 2 : ℝ) * hs
  · linear_combination (-3 / 4 * cos d * sin d ^ 2) * h3 + (-9 / 4 * cos d) * hs

theorem Q_phase_free (d r : ℝ) :
    let x0 := 1 + r * cos d
    let x1 := 1 + r * cos (d + 2 * π / 3)
    let x2 := 1 + r * cos (d - 2 * π / 3)
    (x0 ^ 2 + x1 ^ 2 + x2 ^ 2) / (x0 + x1 + x2) ^ 2 = 1 / 3 + r ^ 2 / 6 := by
  intro x0 x1 x2
  obtain ⟨s1, s2, -⟩ := z3_sums d
  have hsum : x0 + x1 + x2 = 3 := by simp only [x0, x1, x2]; linear_combination r * s1
  have hsq : x0 ^ 2 + x1 ^ 2 + x2 ^ 2 = 3 + 3 / 2 * r ^ 2 := by
    simp only [x0, x1, x2]; linear_combination (2 * r) * s1 + r ^ 2 * s2
  rw [hsum, hsq]; ring

theorem p3_phase (d r : ℝ) :
    (1 + r * cos d) ^ 3 + (1 + r * cos (d + 2 * π / 3)) ^ 3 + (1 + r * cos (d - 2 * π / 3)) ^ 3
      = 3 + 9 / 2 * r ^ 2 + 3 / 4 * r ^ 3 * cos (3 * d) := by
  obtain ⟨s1, s2, s3⟩ := z3_sums d
  linear_combination (3 * r) * s1 + (3 * r ^ 2) * s2 + r ^ 3 * s3

theorem cos_sin_bound (t : ℝ) (ht : |t| ≤ 1) :
    |cos t - (1 - t ^ 2 / 2 + t ^ 4 / 24 - t ^ 6 / 720)| ≤ |t| ^ 8 * (9 / 322560) ∧
    |sin t - (t - t ^ 3 / 6 + t ^ 5 / 120 - t ^ 7 / 5040)| ≤ |t| ^ 8 * (9 / 322560) := by
  have hx : ‖(t : ℂ) * Complex.I‖ ≤ 1 := by simpa using ht
  have hb := Complex.exp_bound hx (n := 8) (by norm_num)
  have hn : ‖(t : ℂ) * Complex.I‖ = |t| := by simp
  rw [hn] at hb
  have hexp : Complex.exp ((t : ℂ) * Complex.I) = (cos t : ℂ) + (sin t : ℂ) * Complex.I := by
    rw [Complex.exp_mul_I, ← Complex.ofReal_cos, ← Complex.ofReal_sin]
  have i2 : Complex.I ^ 2 = -1 := Complex.I_sq
  have hP : (∑ m ∈ Finset.range 8, ((t : ℂ) * Complex.I) ^ m / (m.factorial : ℂ))
      = (((1 - t ^ 2 / 2 + t ^ 4 / 24 - t ^ 6 / 720 : ℝ)) : ℂ)
        + (((t - t ^ 3 / 6 + t ^ 5 / 120 - t ^ 7 / 5040 : ℝ)) : ℂ) * Complex.I := by
    simp only [Finset.sum_range_succ, Finset.sum_range_zero, Nat.factorial]
    push_cast
    linear_combination
      (Complex.I ^ 5 * (t:ℂ) ^ 7 / 5040 + Complex.I ^ 4 * (t:ℂ) ^ 6 / 720 - Complex.I ^ 3 * (t:ℂ) ^ 7 / 5040
        + Complex.I ^ 3 * (t:ℂ) ^ 5 / 120 - Complex.I ^ 2 * (t:ℂ) ^ 6 / 720 + Complex.I ^ 2 * (t:ℂ) ^ 4 / 24
        + Complex.I * (t:ℂ) ^ 7 / 5040 - Complex.I * (t:ℂ) ^ 5 / 120 + Complex.I * (t:ℂ) ^ 3 / 6
        + (t:ℂ) ^ 6 / 720 - (t:ℂ) ^ 4 / 24 + (t:ℂ) ^ 2 / 2) * i2
  rw [hP, hexp] at hb
  set Pc := 1 - t ^ 2 / 2 + t ^ 4 / 24 - t ^ 6 / 720
  set Ps := t - t ^ 3 / 6 + t ^ 5 / 120 - t ^ 7 / 5040
  have hz : (cos t : ℂ) + (sin t : ℂ) * Complex.I - ((Pc : ℂ) + (Ps : ℂ) * Complex.I)
      = ((cos t - Pc : ℝ) : ℂ) + ((sin t - Ps : ℝ) : ℂ) * Complex.I := by push_cast; ring
  rw [hz] at hb
  have hre := Complex.abs_re_le_norm (((cos t - Pc : ℝ) : ℂ) + ((sin t - Ps : ℝ) : ℂ) * Complex.I)
  have him := Complex.abs_im_le_norm (((cos t - Pc : ℝ) : ℂ) + ((sin t - Ps : ℝ) : ℂ) * Complex.I)
  simp [Complex.cos_ofReal_re, Complex.sin_ofReal_re] at hre him
  push_cast at hb
  rw [show (9 : ℝ) * ((Nat.factorial 8 : ℝ) * 8)⁻¹ = 9 / 322560 by norm_num [Nat.factorial]] at hb
  exact ⟨hre.trans hb, him.trans hb⟩

set_option linter.unusedVariables false in
/-- Koide exact (r = √2) and Brannen exact (δ = 2/9) together force m_μ/m_e > 206.769. -/
theorem brannen_and_koide_incompatible :
    let c := cos (2 / 9)
    let s := sin (2 / 9)
    let xe := 1 + √2 * cos (2 / 9 + 2 * π / 3)
    let xm := 1 + √2 * cos (2 / 9 - 2 * π / 3)
    xm ^ 2 > 206.769 * xe ^ 2 := by
  intro c s xe xm
  have ht : |(2 / 9 : ℝ)| ≤ 1 := by rw [abs_of_pos (by norm_num)]; norm_num
  obtain ⟨hcb, hsb⟩ := cos_sin_bound (2 / 9) ht
  rw [abs_of_pos (by norm_num : (0:ℝ) < 2 / 9)] at hcb hsb
  obtain ⟨hc1, hc2⟩ := abs_le.mp hcb
  obtain ⟨hs1, hs2⟩ := abs_le.mp hsb
  have h2l : (1.41421356237 : ℝ) ≤ √2 := Real.le_sqrt_of_sq_le (by norm_num)
  have h2u : √2 ≤ 1.41421356238 := by
    rw [show (1.41421356238 : ℝ) = √(1.41421356238 ^ 2) from (Real.sqrt_sq (by norm_num)).symm]
    exact Real.sqrt_le_sqrt (by norm_num)
  have h3l : (1.73205080756 : ℝ) ≤ √3 := Real.le_sqrt_of_sq_le (by norm_num)
  have h3u : √3 ≤ 1.73205080757 := by
    rw [show (1.73205080757 : ℝ) = √(1.73205080757 ^ 2) from (Real.sqrt_sq (by norm_num)).symm]
    exact Real.sqrt_le_sqrt (by norm_num)
  -- numeric enclosures of c and s
  have cl : (0.9754100850 : ℝ) ≤ c := by simp only [c]; norm_num at hc1 ⊢; linarith
  have cu : c ≤ (0.9754100857 : ℝ) := by simp only [c]; norm_num at hc2 ⊢; linarith
  have sl : (0.2203977432 : ℝ) ≤ s := by simp only [s]; norm_num at hs1 ⊢; linarith
  have su : s ≤ (0.2203977437 : ℝ) := by simp only [s]; norm_num at hs2 ⊢; linarith
  have hxe : xe = 1 - √2 * ((c + √3 * s) / 2) := by simp only [xe, c, s]; rw [c1_eq]; ring
  have hxm : xm = 1 - √2 * ((c - √3 * s) / 2) := by simp only [xm, c, s]; rw [c2_eq]; ring
  have ul : (1.73205080756 : ℝ) * 0.2203977432 ≤ √3 * s := mul_le_mul h3l sl (by norm_num) (by positivity)
  have uu : √3 * s ≤ (1.73205080757 : ℝ) * 0.2203977437 := mul_le_mul h3u su (by linarith) (by norm_num)
  have wel : ((0.9754100850 : ℝ) + 1.73205080756 * 0.2203977432) / 2 ≤ (c + √3 * s) / 2 := by linarith
  have weu : (c + √3 * s) / 2 ≤ ((0.9754100857 : ℝ) + 1.73205080757 * 0.2203977437) / 2 := by linarith
  have vel : (1.41421356237 : ℝ) * (((0.9754100850 : ℝ) + 1.73205080756 * 0.2203977432) / 2)
      ≤ √2 * ((c + √3 * s) / 2) := mul_le_mul h2l wel (by norm_num) (by positivity)
  have veu : √2 * ((c + √3 * s) / 2)
      ≤ (1.41421356238 : ℝ) * (((0.9754100857 : ℝ) + 1.73205080757 * 0.2203977437) / 2) :=
    mul_le_mul h2u weu (by linarith) (by norm_num)
  have wmu : (c - √3 * s) / 2 ≤ ((0.9754100857 : ℝ) - 1.73205080756 * 0.2203977432) / 2 := by linarith
  have wml : ((0.9754100850 : ℝ) - 1.73205080757 * 0.2203977437) / 2 ≤ (c - √3 * s) / 2 := by linarith
  have vmu : √2 * ((c - √3 * s) / 2)
      ≤ (1.41421356238 : ℝ) * (((0.9754100857 : ℝ) - 1.73205080756 * 0.2203977432) / 2) :=
    mul_le_mul h2u wmu (by linarith) (by norm_num)
  set U : ℝ := 1 - (1.41421356237 : ℝ) * (((0.9754100850 : ℝ) + 1.73205080756 * 0.2203977432) / 2)
  set L : ℝ := 1 - (1.41421356238 : ℝ) * (((0.9754100857 : ℝ) - 1.73205080756 * 0.2203977432) / 2)
  have xe_le : xe ≤ U := by rw [hxe]; linarith
  have xe_nn : 0 ≤ xe := by rw [hxe]; norm_num at veu ⊢; linarith
  have xm_ge : L ≤ xm := by rw [hxm]; linarith
  have L_nn : 0 ≤ L := by simp only [L]; norm_num
  have e1 : xe ^ 2 ≤ U ^ 2 := pow_le_pow_left₀ xe_nn xe_le 2
  have e2 : L ^ 2 ≤ xm ^ 2 := pow_le_pow_left₀ L_nn xm_ge 2
  have e3 : 206.769 * U ^ 2 < L ^ 2 := by simp only [U, L]; norm_num
  have e4 := mul_le_mul_of_nonneg_left e1 (by norm_num : (0:ℝ) ≤ 206.769)
  exact lt_of_le_of_lt e4 (lt_of_lt_of_le e3 e2)

theorem measured_ratio_upper : (105.6583755 + 0.0000023 : ℝ) / 0.51099895 < 206.7683 := by norm_num

end KoidePhase

#print axioms KoidePhase.z3_sums
#print axioms KoidePhase.Q_phase_free
#print axioms KoidePhase.p3_phase
#print axioms KoidePhase.cos_sin_bound
#print axioms KoidePhase.brannen_and_koide_incompatible
#print axioms KoidePhase.measured_ratio_upper
