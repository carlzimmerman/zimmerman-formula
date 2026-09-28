import Mathlib
import Mathlib.Tactic
noncomputable section
open Real

-- P1: is pointwise pow reducible?
example (f : ℝ → ℝ) (x : ℝ) : (f ^ 2) x = f x ^ 2 := by rfl
example (f : ℝ → ℝ) : (f ^ 2) = fun x => f x ^ 2 := by rfl

-- P2: full mu2c derivative proof
example (x : ℝ) (hx : 1 + x / 2 ≠ 0) :
    HasDerivAt (fun z : ℝ => 1 - 1 / (1 + z / 2) ^ 2) (1 / (1 + x / 2) ^ 3) x := by
  have hlin : HasDerivAt (fun z : ℝ => 1 + z / 2) (1 / 2) x := by
    simpa [add_comm] using ((hasDerivAt_id x).div_const 2).const_add 1
  have hp := hlin.pow 2
  have h2v : (↑(2 : ℕ) : ℝ) * (1 + x / 2) ^ (2 - 1) * (1 / 2) = 1 + x / 2 := by
    norm_num [pow_one]
    ring_nf
  have hg2 : HasDerivAt ((fun z : ℝ => 1 + z / 2) ^ 2) (1 + x / 2) x := by
    rw [h2v] at hp
    exact hp
  have hg2ne : (1 + x / 2) ^ 2 ≠ 0 := pow_ne_zero 2 hx
  have hinv : HasDerivAt (fun z : ℝ => ((1 + z / 2) ^ 2)⁻¹)
      (-(1 + x / 2) / ((1 + x / 2) ^ 2) ^ 2) x := by
    simpa using hg2.inv hg2ne
  have hpre : HasDerivAt (fun z : ℝ => 1 - ((1 + z / 2) ^ 2)⁻¹)
      ((1 + x / 2) / ((1 + x / 2) ^ 2) ^ 2) x := by
    simpa using hinv.const_sub 1
  have hval : (1 + x / 2) / ((1 + x / 2) ^ 2) ^ 2 = 1 / (1 + x / 2) ^ 3 := by
    field_simp [hx]
  rw [hval] at hpre
  rw [inv_eq_one_div] at hpre
  simpa using hpre

-- P3: kappa identities with ring after field_simp
example (y : ℝ) (hy : 2 * y + 1 ≠ 0) :
    2 * (y + 1) / (2 * y + 1) = 1 + 1 / (2 * y + 1) := by
  field_simp [hy]
  ring

example (y : ℝ) (hy : 2 * y + 1 ≠ 0) :
    2 * (y + 1) / (2 * y + 1) = 2 - 2 * y / (2 * y + 1) := by
  field_simp [hy]
  ring

-- P4: scale-invariant did NOT hold; check the reciprocal identity instead
example (x y dxdy : ℝ) (hx : x ≠ 0) (hy : y ≠ 0) (hd : dxdy ≠ 0) :
    (x / (y * dxdy)) * (dxdy * y / x) = 1 := by
  field_simp [hx, hy, hd]
  ring

-- P5: hsl2 for muQ derivative
example : ((2 * 1 / Real.sqrt 5) * 1 - ((Real.sqrt 5 - 1) / 2) * 1) / 1 ^ 2
    = (Real.sqrt 5 - 1) / (2 * Real.sqrt 5) := by
  have hsq5 : (Real.sqrt 5) ^ 2 = (5 : ℝ) := by
    rw [Real.sq_sqrt]
    norm_num
  have hne5 : Real.sqrt 5 ≠ 0 := ne_of_gt (Real.sqrt_pos.2 (by norm_num : (0 : ℝ) < 5))
  field_simp [hne5]
  rw [mul_sub, mul_one]
  rw [← pow_two, hsq5]
  ring

-- P6: muS derivative at one rpow with base normalization
example : HasDerivAt (fun z : ℝ => z / Real.sqrt (1 + z ^ 2)) ((2 : ℝ) ^ (-(3 / 2) : ℝ)) 1 := by
  have harg : 0 < 1 + 1 ^ 2 := by norm_num
  have hne : Real.sqrt (1 + 1 ^ 2) ≠ 0 := ne_of_gt (Real.sqrt_pos.2 harg)
  have hs2 : (Real.sqrt (1 + 1 ^ 2)) ^ 2 = 1 + 1 ^ 2 := by
    rw [Real.sq_sqrt]
    exact le_of_lt harg
  have hd : HasDerivAt (fun z : ℝ => 1 + z ^ 2) (2 * 1) 1 := by
    simpa using ((hasDerivAt_id 1).pow (2 : ℕ)).const_add 1
  have hds : HasDerivAt (fun z : ℝ => Real.sqrt (1 + z ^ 2))
      ((2 * 1) / (2 * Real.sqrt (1 + 1 ^ 2))) 1 :=
    hd.sqrt harg.ne'
  have hdiv : HasDerivAt (fun z : ℝ => z / Real.sqrt (1 + z ^ 2))
      ((1 * Real.sqrt (1 + 1 ^ 2) - 1 * ((2 * 1) / (2 * Real.sqrt (1 + 1 ^ 2))))
        / (Real.sqrt (1 + 1 ^ 2)) ^ 2) 1 :=
    (hasDerivAt_id 1).div hds hne
  have hx2 : (2 * 1) / (2 * Real.sqrt (1 + 1 ^ 2)) = 1 / Real.sqrt (1 + 1 ^ 2) := by
    field_simp [hne]
  have hnum : 1 * Real.sqrt (1 + 1 ^ 2) - 1 * (1 / Real.sqrt (1 + 1 ^ 2))
      = 1 / Real.sqrt (1 + 1 ^ 2) := by
    field_simp [hne]
    rw [hs2]
    ring
  have hsl : (1 / Real.sqrt (1 + 1 ^ 2)) / (Real.sqrt (1 + 1 ^ 2)) ^ 2
      = 1 / ((1 + 1 ^ 2) * Real.sqrt (1 + 1 ^ 2)) := by
    field_simp [hne]
    rw [hs2]
  rw [hx2, hnum, hsl] at hdiv
  have hr : (1 + 1 ^ 2) ^ (-(3 / 2) : ℝ) = 1 / ((1 + 1 ^ 2) * Real.sqrt (1 + 1 ^ 2)) := by
    have hpos : 0 < 1 + 1 ^ 2 := by norm_num
    have hle : 0 ≤ 1 + 1 ^ 2 := le_of_lt hpos
    have h32 : (1 + 1 ^ 2) ^ ((3 / 2 : ℝ))
        = (1 + 1 ^ 2) * Real.sqrt (1 + 1 ^ 2) := by
      have hsplit : (3 / 2 : ℝ) = 1 + 1 / 2 := by norm_num
      rw [hsplit, Real.rpow_add hpos, Real.rpow_one]
      rw [← Real.sqrt_eq_rpow]
    rw [Real.rpow_neg hle]
    rw [h32]
    rw [one_div]
  have hb : (1 + 1 ^ 2) = (2 : ℝ) := by norm_num
  rw [← hr] at hdiv
  rwa [hb] at hdiv
end