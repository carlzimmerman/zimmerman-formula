import Mathlib

/-!
# KOIDE_TRIALITY_45 -- can cube x sphere / the tesseract / Spin(8) triality force Koide's 45 degrees?

Koide: Q = (Σ m)/(Σ √m)^2 = 2/3  ⇔  the √m vector sits at exactly 45° to the democratic axis (1,1,1).
Source: scratch exploration (cube, tesseract, D4 triality), this file is the certificate.

CERTIFIED:
(A) `koide_cone_no_integer`: no nonzero integer (hence, by homogeneity, no rational) 3-vector lies on the
    Koide cone 2(x+y+z)^2 = 3(x^2+y^2+z^2).  So no polytope / lattice / counting construction whose output
    √-mass ratios are rational can give Q = 2/3.  (Descent on 2s^2 = 3u^2 + w^2, mod 3.)
(B) Spin(8) triality on the D4 Cartan: `T_cube` (T^3 = 1), `T_orth` (T^T T = 1), `T_a1`..`T_a2`
    (T: α1 → α3 → α4 → α1, α2 fixed); `P_eq` (the triality-fixed projector (1+T+T^2)/3 = Pm, the G2 Cartan).
    `triality_no_integer_45`: reading the generation singlet from the G2 (fixed) part and the doublet from the
    triality-rotated part, NO nonzero integer 4-vector (so no D4 root or weight, all of which are in ½ℤ^4)
    sits at 45°.  (Descent on a^2 + c^2 = 3(b^2 + d^2), mod 3.)
(C) The GO (conditional): `go_split`: X = (unit G2-fixed root -(1,1,0,0)/√2) + (unit rotated weight (0,0,0,1))
    has |PX|^2 = |(1-P)X|^2, i.e. it is at exactly 45°; the √2 enters through the unit normalisation of the
    root.  `go_Q`: the √-mass vector it yields, (√3/3 + √2/2, √3/3, √3/3 - √2/2), has Q = 2/3 exactly.
    `go_masses`: its masses are in the ratio (5+2√6) : 2 : (5-2√6).
    `go_fails_electron`: the predicted lightest/heaviest ratio 49 - 20√6 exceeds 1/100, while the measured
    m_e/m_τ = 0.51099895/1776.86 is below 1/1000 (`lepton_ratio_small`).  So the construction reproduces
    Koide's NUMBER and gets the HIERARCHY wrong (its Brannen phase is 30°, the leptons' is 12.735°).
NOT CERTIFIED: that unit-normalising the root is forced (it is a choice; with D4's own lengths the same
vector gives Q = 1/2); the scratch searches; the phase values; the lepton masses (data, quoted).
-/

namespace KoideTriality

/-! ## (A) the 3D Koide cone has no rational points -/

theorem zmod3_two_sq : ∀ s w : ZMod 3, 2 * s ^ 2 = w ^ 2 → s = 0 ∧ w = 0 := by decide

theorem zmod3_sum_sq : ∀ a c : ZMod 3, a ^ 2 + c ^ 2 = 0 → a = 0 ∧ c = 0 := by decide

lemma three_dvd_of_sq {u : ℤ} (h : (3 : ℤ) ∣ u ^ 2) : (3 : ℤ) ∣ u :=
  Int.prime_three.dvd_of_dvd_pow h

lemma cast3 {x : ℤ} (h : ((x : ZMod 3)) = 0) : (3 : ℤ) ∣ x :=
  (ZMod.intCast_zmod_eq_zero_iff_dvd x 3).mp h

theorem cone_descent : ∀ (n : ℕ) (s u w : ℤ), s.natAbs = n →
    2 * s ^ 2 = 3 * u ^ 2 + w ^ 2 → s = 0 ∧ u = 0 ∧ w = 0 := by
  intro n
  induction n using Nat.strong_induction_on with
  | _ n ih =>
    intro s u w hn h
    by_cases hs : s = 0
    · subst hs
      have hu : u ^ 2 = 0 := by nlinarith [sq_nonneg u, sq_nonneg w]
      have hw : w ^ 2 = 0 := by nlinarith [sq_nonneg u, sq_nonneg w]
      exact ⟨rfl, pow_eq_zero_iff (two_ne_zero) |>.mp hu, pow_eq_zero_iff (two_ne_zero) |>.mp hw⟩
    · have hz : 2 * ((s : ZMod 3)) ^ 2 = ((w : ZMod 3)) ^ 2 := by
        have := congrArg (fun x : ℤ => (x : ZMod 3)) h
        have h3 : (3 : ZMod 3) = 0 := by decide
        push_cast at this
        simpa [h3] using this
      obtain ⟨hs3, hw3⟩ := zmod3_two_sq _ _ hz
      obtain ⟨s', rfl⟩ := cast3 hs3
      obtain ⟨w', rfl⟩ := cast3 hw3
      have hu3 : (3 : ℤ) ∣ u ^ 2 := ⟨2 * s' ^ 2 - w' ^ 2, by nlinarith⟩
      obtain ⟨u', rfl⟩ := three_dvd_of_sq hu3
      have h9 : (9 : ℤ) * (2 * s' ^ 2) = 9 * (3 * u' ^ 2 + w' ^ 2) := by linear_combination h
      have h' : 2 * s' ^ 2 = 3 * u' ^ 2 + w' ^ 2 := mul_left_cancel₀ (by norm_num) h9
      have hs' : s' ≠ 0 := by rintro rfl; simp at hs
      have hlt : s'.natAbs < n := by
        rw [← hn, Int.natAbs_mul]; have := Int.natAbs_pos.mpr hs'; simp; omega
      obtain ⟨h1, h2, h3⟩ := ih _ hlt s' u' w' rfl h'
      exact absurd h1 hs'

theorem koide_cone_no_integer (x y z : ℤ)
    (h : 2 * (x + y + z) ^ 2 = 3 * (x ^ 2 + y ^ 2 + z ^ 2)) : x = 0 ∧ y = 0 ∧ z = 0 := by
  have key : 2 * (x + y + z) ^ 2 = 3 * (x - y) ^ 2 + (x + y - 2 * z) ^ 2 := by
    linear_combination (2 : ℤ) * h
  obtain ⟨h1, h2, h3⟩ := cone_descent _ _ _ _ rfl key
  omega

/-! ## (B) Spin(8) triality on the D4 Cartan -/

def T : Matrix (Fin 4) (Fin 4) ℚ :=
  !![1/2, 1/2, 1/2, 1/2; 1/2, 1/2, -1/2, -1/2; 1/2, -1/2, 1/2, -1/2; -1/2, 1/2, 1/2, -1/2]

def Pm : Matrix (Fin 4) (Fin 4) ℚ :=
  !![2/3, 1/3, 1/3, 0; 1/3, 2/3, -1/3, 0; 1/3, -1/3, 2/3, 0; 0, 0, 0, 0]

def a1 : Fin 4 → ℚ := ![1, -1, 0, 0]
def a2 : Fin 4 → ℚ := ![0, 1, -1, 0]
def a3 : Fin 4 → ℚ := ![0, 0, 1, -1]
def a4 : Fin 4 → ℚ := ![0, 0, 1, 1]

theorem T_cube : T * T * T = 1 := by
  ext i j; fin_cases i <;> fin_cases j <;>
    simp [T, Matrix.mul_apply, Fin.sum_univ_four] <;> norm_num

theorem T_orth : T.transpose * T = 1 := by
  ext i j; fin_cases i <;> fin_cases j <;>
    simp [T, Matrix.mul_apply, Fin.sum_univ_four] <;> norm_num

theorem T_a1 : T.mulVec a1 = a3 := by
  ext i; fin_cases i <;> simp [T, a1, a3, Matrix.mulVec, dotProduct, Fin.sum_univ_four] <;> norm_num
theorem T_a3 : T.mulVec a3 = a4 := by
  ext i; fin_cases i <;> simp [T, a3, a4, Matrix.mulVec, dotProduct, Fin.sum_univ_four] <;> norm_num
theorem T_a4 : T.mulVec a4 = a1 := by
  ext i; fin_cases i <;> simp [T, a4, a1, Matrix.mulVec, dotProduct, Fin.sum_univ_four] <;> norm_num
theorem T_a2 : T.mulVec a2 = a2 := by
  ext i; fin_cases i <;> simp [T, a2, Matrix.mulVec, dotProduct, Fin.sum_univ_four] <;> norm_num

theorem P_eq : (1/3 : ℚ) • (1 + T + T * T) = Pm := by
  ext i j; fin_cases i <;> fin_cases j <;>
    simp [T, Pm] <;> norm_num

theorem sumsq_descent : ∀ (n : ℕ) (a b c d : ℤ), b.natAbs + d.natAbs = n →
    a ^ 2 + c ^ 2 = 3 * (b ^ 2 + d ^ 2) → a = 0 ∧ b = 0 ∧ c = 0 ∧ d = 0 := by
  intro n
  induction n using Nat.strong_induction_on with
  | _ n ih =>
    intro a b c d hn h
    have h3 : (3 : ZMod 3) = 0 := by decide
    have hz : ((a : ZMod 3)) ^ 2 + ((c : ZMod 3)) ^ 2 = 0 := by
      have := congrArg (fun x : ℤ => (x : ZMod 3)) h
      push_cast at this; simpa [h3] using this
    obtain ⟨ha3, hc3⟩ := zmod3_sum_sq _ _ hz
    obtain ⟨a', rfl⟩ := cast3 ha3
    obtain ⟨c', rfl⟩ := cast3 hc3
    have hbd : b ^ 2 + d ^ 2 = 3 * (a' ^ 2 + c' ^ 2) := by linarith
    have hz2 : ((b : ZMod 3)) ^ 2 + ((d : ZMod 3)) ^ 2 = 0 := by
      have := congrArg (fun x : ℤ => (x : ZMod 3)) hbd
      push_cast at this; simpa [h3] using this
    obtain ⟨hb3, hd3⟩ := zmod3_sum_sq _ _ hz2
    obtain ⟨b', rfl⟩ := cast3 hb3
    obtain ⟨d', rfl⟩ := cast3 hd3
    by_cases hzero : b' = 0 ∧ d' = 0
    · obtain ⟨rfl, rfl⟩ := hzero
      have ha : a' ^ 2 = 0 := by nlinarith [sq_nonneg a', sq_nonneg c']
      have hc : c' ^ 2 = 0 := by nlinarith [sq_nonneg a', sq_nonneg c']
      simp [pow_eq_zero_iff (two_ne_zero) |>.mp ha, pow_eq_zero_iff (two_ne_zero) |>.mp hc]
    · have h' : a' ^ 2 + c' ^ 2 = 3 * (b' ^ 2 + d' ^ 2) := by nlinarith
      have hlt : b'.natAbs + d'.natAbs < n := by
        rw [← hn, Int.natAbs_mul, Int.natAbs_mul]
        have : 0 < b'.natAbs + d'.natAbs := by
          rcases not_and_or.mp hzero with hb | hd
          · have := Int.natAbs_pos.mpr hb; omega
          · have := Int.natAbs_pos.mpr hd; omega
        simp; omega
      obtain ⟨h1, h2, h3', h4⟩ := ih _ hlt a' b' c' d' rfl h'
      subst h1 h2 h3' h4; simp

/-- |PY|^2 = ½|Y|^2 (45° between the G2-fixed and triality-rotated parts) has no nonzero integer solution. -/
theorem triality_no_integer_45 (y : Fin 4 → ℤ)
    (h : 2 * dotProduct (fun i => (y i : ℚ)) (Pm.mulVec (fun i => (y i : ℚ)))
          = dotProduct (fun i => (y i : ℚ)) (fun i => (y i : ℚ))) : y = 0 := by
  simp [Pm, Matrix.mulVec, dotProduct, Fin.sum_univ_four] at h
  have key : (((y 0 + 2 * y 1 + 2 * y 2 : ℤ)) : ℚ) ^ 2 + (((3 * y 2 : ℤ)) : ℚ) ^ 2
      = 3 * ((((y 1 + 2 * y 2 : ℤ)) : ℚ) ^ 2 + (((y 3 : ℤ)) : ℚ) ^ 2) := by
    push_cast; linear_combination (3 : ℚ) * h
  have keyZ : (y 0 + 2 * y 1 + 2 * y 2) ^ 2 + (3 * y 2) ^ 2 = 3 * ((y 1 + 2 * y 2) ^ 2 + (y 3) ^ 2) := by
    exact_mod_cast key
  obtain ⟨h1, h2, h3, h4⟩ := sumsq_descent _ _ _ _ _ rfl keyZ
  funext i; fin_cases i <;> simp <;> omega

/-! ## (C) the conditional GO, and its prediction -/

/-- unit G2-fixed root plus unit rotated weight: fixed part and rotated part have equal norm (45°). -/
theorem go_split :
    let r := Real.sqrt 2
    let X : Fin 4 → ℝ := ![-1 / r, -1 / r, 0, 1]
    let PX : Fin 4 → ℝ := ![-1 / r, -1 / r, 0, 0]
    (∀ i, PX i + (X i - PX i) = X i) ∧
    dotProduct PX PX = dotProduct (X - PX) (X - PX) := by
  intro r X PX
  have hr : r ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  have hr0 : r ≠ 0 := by positivity
  refine ⟨fun i => by ring, ?_⟩
  simp [X, PX, dotProduct, Fin.sum_univ_four]
  field_simp
  linarith

/-- the Koide frame image of X: √m ∝ (√3/3 + √2/2, √3/3, √3/3 - √2/2); Q = 2/3 exactly. -/
theorem go_Q :
    let a := Real.sqrt 3 / 3
    let b := Real.sqrt 2 / 2
    ((a + b) ^ 2 + a ^ 2 + (a - b) ^ 2) / ((a + b) + a + (a - b)) ^ 2 = 2 / 3 := by
  intro a b
  have h3 : Real.sqrt 3 ^ 2 = 3 := Real.sq_sqrt (by norm_num)
  have h2 : Real.sqrt 2 ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  have hnum : (a + b) ^ 2 + a ^ 2 + (a - b) ^ 2 = 2 := by
    simp only [a, b]; linear_combination (1 / 3 : ℝ) * h3 + (1 / 2 : ℝ) * h2
  have hden : ((a + b) + a + (a - b)) ^ 2 = 3 := by
    simp only [a]; linear_combination h3
  rw [hnum, hden]

theorem go_masses :
    let a := Real.sqrt 3 / 3
    let b := Real.sqrt 2 / 2
    (a + b) ^ 2 = (5 + 2 * Real.sqrt 6) / 6 ∧ a ^ 2 = 2 / 6 ∧ (a - b) ^ 2 = (5 - 2 * Real.sqrt 6) / 6 := by
  intro a b
  have h3 : Real.sqrt 3 ^ 2 = 3 := Real.sq_sqrt (by norm_num)
  have h2 : Real.sqrt 2 ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  have h6 : Real.sqrt 3 * Real.sqrt 2 = Real.sqrt 6 := by
    rw [← Real.sqrt_mul (by norm_num)]; norm_num
  refine ⟨?_, ?_, ?_⟩ <;> simp only [a, b]
  · linear_combination (1 / 9 : ℝ) * h3 + (1 / 4 : ℝ) * h2 + (1 / 3 : ℝ) * h6
  · linear_combination (1 / 9 : ℝ) * h3
  · linear_combination (1 / 9 : ℝ) * h3 + (1 / 4 : ℝ) * h2 - (1 / 3 : ℝ) * h6

/-- predicted lightest/heaviest = (5-2√6)/(5+2√6) = 49 - 20√6 > 1/100. -/
theorem go_fails_electron :
    (5 - 2 * Real.sqrt 6) / (5 + 2 * Real.sqrt 6) = 49 - 20 * Real.sqrt 6 ∧
    (1 : ℝ) / 100 < 49 - 20 * Real.sqrt 6 := by
  have h6 : Real.sqrt 6 ^ 2 = 6 := Real.sq_sqrt (by norm_num)
  have hpos : 0 ≤ Real.sqrt 6 := Real.sqrt_nonneg 6
  have hden : (5 + 2 * Real.sqrt 6) ≠ 0 := by positivity
  refine ⟨?_, ?_⟩
  · rw [div_eq_iff hden]; linear_combination (40 : ℝ) * h6
  · nlinarith [h6, hpos]

theorem lepton_ratio_small : (0.51099895 : ℝ) / 1776.86 < 1 / 1000 := by norm_num

end KoideTriality

#print axioms KoideTriality.koide_cone_no_integer
#print axioms KoideTriality.T_cube
#print axioms KoideTriality.T_orth
#print axioms KoideTriality.T_a1
#print axioms KoideTriality.T_a3
#print axioms KoideTriality.T_a4
#print axioms KoideTriality.T_a2
#print axioms KoideTriality.P_eq
#print axioms KoideTriality.triality_no_integer_45
#print axioms KoideTriality.go_split
#print axioms KoideTriality.go_Q
#print axioms KoideTriality.go_masses
#print axioms KoideTriality.go_fails_electron
#print axioms KoideTriality.lepton_ratio_small
