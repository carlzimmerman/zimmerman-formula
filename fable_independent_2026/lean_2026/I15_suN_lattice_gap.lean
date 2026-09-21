import Mathlib

/-!
# I15 -- THE SU(N) STRONG-COUPLING GAP, UNIFORM IN N

**Scope statement (as every certificate in this repo reads):** Lean certifies
the MATHEMATICS. The physical premises -- the electric Casimir
C_F = (N^2-1)/(2N) of SU(N), its Gauss-law minimal excitation the 4-link
plaquette loop E_loop = g^2 (N^2-1)/N, and the magnetic shift capped by the
unitary-trace bound |tr U| <= N at 2N/g^2 -- are the deepseek campaign's
committed values (deepseek_push/yang_mills_gap/YM05_lattice_gap, certified
for N = 2, 3). This file certifies the SYMBOLIC completion: the
strong-coupling lattice mass gap for EVERY SU(N), N >= 2:

    gap_N(x) = x (N^2-1)/N - 2N/x,   x = g^2 (lattice units),

with gap_N(2) = (N^2-2)/N -- reproducing the certified corner values
SU(2): 1 and SU(3): 7/3 -- and gap_N(x) > 0 for all x >= 2, all N >= 2:
a strictly positive spectral gap in the strong-coupling corner of the
scaling plane, UNIFORM in the gauge group. This is the general-N face of
the campaign's rung R4. The scaling window and the continuum limit
(YM_ROADMAP R5/R6) remain untouched and named: nothing here claims the
Clay SU(3) continuum gap.

Compiled against the repo's Mathlib build (Lean 4.34.0-rc2).
-/
noncomputable section
open scoped Real

/-- the electric Casimir of SU(N), dimensionless -/
def Cc (N : ℝ) : ℝ := (N^2 - 1) / (2 * N)

/-- the strong-coupling lattice gap bound (lattice units) -/
def gapN (N x : ℝ) : ℝ := x * (N^2 - 1) / N - 2 * N / x

/-- the loop energy is twice the Casimir times x: E_loop = 2 x C_F -/
theorem loop_energy (N x : ℝ) (hN : N ≠ 0) : x * (N^2 - 1) / N = 2 * x * Cc N := by
  unfold Cc
  field_simp [hN]

/-- the certified corner values: gap_N(2) = (N^2 - 2)/N -- SU(2) gives 1,
    SU(3) gives 7/3, reproducing the certified table -/
theorem gap_at_two (N : ℝ) (hN : N ≠ 0) : gapN N 2 = (N^2 - 2) / N := by
  unfold gapN
  field_simp [hN, (by norm_num : (2 : ℝ) ≠ 0)]
  ring

/-- the Casimir is positive -/
theorem casimir_pos (N : ℝ) (hN2 : 2 ≤ N) : 0 < Cc N := by
  have hN : 0 < N := by linarith
  unfold Cc
  exact div_pos (by nlinarith [hN2]) (by linarith)

/-- THE GAP, UNIFORM IN N: for every SU(N), N >= 2, at every strong coupling
    x >= 2 the spectral gap bound is strictly positive -/
theorem gap_at_strong (N x : ℝ) (hN2 : 2 ≤ N) (hx2 : 2 ≤ x) : 0 < gapN N x := by
  have hN : 0 < N := by linarith
  have hNn : N ≠ 0 := ne_of_gt hN
  have hq : 0 ≤ (N^2 - 1) / N := by
    exact le_of_lt (div_pos (by nlinarith [hN2]) hN)
  have h1 : (2 : ℝ) * (N^2 - 1) / N ≤ x * (N^2 - 1) / N := by
    calc
      (2 : ℝ) * (N^2 - 1) / N = 2 * ((N^2 - 1) / N) := by ring
      _ ≤ x * ((N^2 - 1) / N) := mul_le_mul_of_nonneg_right hx2 hq
      _ = x * (N^2 - 1) / N := by ring
  have hx1 : 1 / x ≤ 1 / 2 := by
    exact one_div_le_one_div_of_le (by norm_num : (0 : ℝ) < 2) hx2
  have h2 : 2 * N / x ≤ N := by
    calc
      2 * N / x = (2 * N) * (1 / x) := by ring
      _ ≤ (2 * N) * (1 / 2) := mul_le_mul_of_nonneg_left hx1 (by linarith : 0 ≤ 2 * N)
      _ = N := by
        field_simp [(by norm_num : (2 : ℝ) ≠ 0)]
  have hmain : (N^2 - 2) / N ≤ gapN N x := by
    unfold gapN
    calc
      (N^2 - 2) / N = (2 : ℝ) * (N^2 - 1) / N - N := by
        field_simp [hNn]
        ring
      _ ≤ x * (N^2 - 1) / N - 2 * N / x := by
        nlinarith [h1, h2]
  have hpos : 0 < (N^2 - 2) / N := by
    exact div_pos (by nlinarith [hN2]) hN
  exact lt_of_lt_of_le hpos hmain

/-! ## the certificate record -/

#print axioms loop_energy
#print axioms gap_at_two
#print axioms casimir_pos
#print axioms gap_at_strong