import Mathlib

/-!
# I16 -- THE VOLUME-DEPENDENT STRONG-COUPLING WINDOW (doorG's partial theorem, certified rung)

**Scope statement:** the operator premise -- for the SU(N) lattice-gauge
Hamiltonian on an open finite graph, the min-max + magnetic-trace bounds give
gap(H_Lambda) >= (x/2) C_F - 3 b_N P(Lambda)/x with C_F = (N^2-1)/(2N) the
electric Casimir, x = g^2, 0 <= b_N <= 2N the magnetic normalization, P(Lambda)
the plaquette count -- is door G's proven statement
(opus_49_doorG/Xd_CLUSTER_ATTEMPT.md). This file certifies the ALGEBRA of the
reduction: given that premise, the gap is at least 3x/16 whenever the
strong-coupling window x >= 4 sqrt(b_N P) holds. Nothing here claims the
many-plaquette x>=2 window, a continuum limit, or the Clay problem.

Compiled against the repo's Mathlib build (Lean 4.34.0-rc2).
-/
noncomputable section
open scoped Real

/-- the volume-dependent gap lower bound of door G -/
def gapVol (x C_F b_N P : ℝ) : ℝ := (x / 2) * C_F - 3 * b_N * P / x

/-- the electric floor: (x/2) C_F >= 3x/8 from C_F >= 3/4, x >= 0 -/
theorem electric_floor (x C_F : ℝ) (hx : 0 ≤ x) (hcf : 3 / 4 ≤ C_F) :
    (x / 2) * C_F ≥ 3 * x / 8 := by
  have hpos : 0 ≤ x / 2 := by positivity
  calc
    (x / 2) * C_F ≥ (x / 2) * (3 / 4) := mul_le_mul_of_nonneg_left hcf hpos
    _ = 3 * x / 8 := by ring

/-- the magnetic floor: 3 b_N P / x <= 3x/16 from 16 b_N P <= x^2, x > 0 -/
theorem magnetic_floor (x b_N P : ℝ) (hx : 0 < x) (hx2 : 16 * b_N * P ≤ x^2) :
    3 * b_N * P / x ≤ 3 * x / 16 := by
  have hx' : x ≠ 0 := ne_of_gt hx
  have hdiv : (16 * b_N * P) / x ≤ x^2 / x := by
    have hmul : ((16 * b_N * P) / x) * x ≤ (x^2 / x) * x := by
      rw [div_mul_cancel₀ (16 * b_N * P) hx', div_mul_cancel₀ (x^2) hx']
      exact hx2
    exact le_of_mul_le_mul_right hmul hx
  calc
    3 * b_N * P / x = (3 / 16) * ((16 * b_N * P) / x) := by
      field_simp [hx']
    _ ≤ (3 / 16) * (x^2 / x) := mul_le_mul_of_nonneg_left hdiv (by norm_num)
    _ = 3 * x / 16 := by
      field_simp [hx']

/-- THE VOLUME WINDOW, certified: C_F >= 3/4 and 16 b_N P <= x^2 force
    gap >= 3x/16 -- door G's reduction, the algebraic rung -/
theorem volume_gap_reduction (x C_F b_N P : ℝ) (hx : 0 < x) (hcf : 3 / 4 ≤ C_F)
    (hx2 : 16 * b_N * P ≤ x^2) :
    gapVol x C_F b_N P ≥ 3 * x / 16 := by
  have h1 : (x / 2) * C_F ≥ 3 * x / 8 := electric_floor x C_F (le_of_lt hx) hcf
  have h2 : 3 * b_N * P / x ≤ 3 * x / 16 := magnetic_floor x b_N P hx hx2
  unfold gapVol
  nlinarith [h1, h2]

/-- the strong-coupling window in the sqrt form: x >= 4 sqrt(b_N P) with
    b_N P >= 0 implies the squared condition -/
theorem threshold_sq (x b_N P : ℝ) (hx : 0 ≤ x) (hbNP : 0 ≤ b_N * P)
    (hxbig : 4 * Real.sqrt (b_N * P) ≤ x) : 16 * b_N * P ≤ x^2 := by
  have hn : 0 ≤ 4 * Real.sqrt (b_N * P) := by
    exact mul_nonneg (by norm_num) (Real.sqrt_nonneg (b_N * P))
  have hsq : (4 * Real.sqrt (b_N * P))^2 ≤ x^2 := by
    calc
      (4 * Real.sqrt (b_N * P))^2 = (4 * Real.sqrt (b_N * P)) * (4 * Real.sqrt (b_N * P)) := by
        rw [pow_two]
      _ ≤ x * x := mul_le_mul hxbig hxbig hn hx
      _ = x^2 := by ring
  have hide : (4 * Real.sqrt (b_N * P))^2 = 16 * (b_N * P) := by
    calc
      (4 * Real.sqrt (b_N * P))^2 = 16 * (Real.sqrt (b_N * P))^2 := by
        rw [pow_two]
        ring
      _ = 16 * (b_N * P) := by
        rw [pow_two, Real.mul_self_sqrt hbNP]
  have hsq' : 16 * b_N * P ≤ x^2 := by nlinarith [hsq]
  exact hsq'

/-- THE WINDOW THEOREM: for C_F >= 3/4 and x >= 4 sqrt(b_N P) >= 0,
    gapVol >= 3x/16 -/
theorem strong_coupling_window (x C_F b_N P : ℝ) (hx : 0 ≤ x) (hcf : 3 / 4 ≤ C_F)
    (hbNP : 0 ≤ b_N * P) (hxbig : 4 * Real.sqrt (b_N * P) ≤ x)
    (hxpos : 0 < x) :
    gapVol x C_F b_N P ≥ 3 * x / 16 := by
  have hsq : 16 * b_N * P ≤ x^2 := threshold_sq x b_N P hx hbNP hxbig
  exact volume_gap_reduction x C_F b_N P hxpos hcf hsq

/-! ## the certificate record -/

#print axioms electric_floor
#print axioms magnetic_floor
#print axioms volume_gap_reduction
#print axioms threshold_sq
#print axioms strong_coupling_window