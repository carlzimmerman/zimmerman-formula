/-
CLOSE-1 / DT2 MUTATE: false statements that MUST NOT compile.  Each is a one-token
alteration of a load-bearing DT2 theorem; the lane's algebra is only certified if every
one of these is rejected.
-/
import Mathlib

namespace DT2Mutate

-- M1: the in-band derivative is ABOVE the cold slope (false: it is strictly below)
theorem m1_nprime_in_band_wrong (n0 M A Bp : ℝ) (hn0 : 0 < n0) (hM : 0 < M)
    (hA : 0 < A) (hB : 0 < Bp) :
    M < n0 / (n0 / M + A * Bp) := by
  have hden : 0 < n0 / M + A * Bp := by
    have h1 : 0 < n0 / M := div_pos hn0 hM
    have h2 : 0 < A * Bp := mul_pos hA hB
    linarith
  rw [lt_div_iff₀ hden]
  have : 0 < A * Bp * M := mul_pos (mul_pos hA hB) hM
  nlinarith [show n0 / M * M = n0 by field_simp]

-- M2: the halo is M_b X with the wrong square-root identity S^2 = 1 + 3 x^2 (false)
theorem m2_polar_is_formB_wrongS (Mb x S : ℝ) (hS : S ^ 2 = 1 + 3 * x ^ 2)
    (hden : 2 * x ^ 2 + 1 + S ≠ 0) :
    Mb * x ^ 2 * (1 + S) / (2 * x ^ 2 + 1 + S) = Mb * (S - 1) / 2 := by
  have hkey : 2 * x ^ 2 * (1 + S) = (S - 1) * (2 * x ^ 2 + 1 + S) := by
    nlinarith
  calc
    Mb * x ^ 2 * (1 + S) / (2 * x ^ 2 + 1 + S)
        = (Mb * (2 * x ^ 2 * (1 + S)) / 2) / (2 * x ^ 2 + 1 + S) := by ring
    _ = (Mb * ((S - 1) * (2 * x ^ 2 + 1 + S)) / 2) / (2 * x ^ 2 + 1 + S) := by rw [hkey]
    _ = Mb * (S - 1) / 2 := by field_simp [hden]

-- M3: the law-on force balance with the pressure term sign flipped (false)
theorem m3_force_balance_wrong (K dN dn k dh : ℝ) (hk : k ≠ 0)
    (h : K * dN = dn + k ^ 2 * dh) :
    K * dN / k + k * dh = dn / k := by
  rw [h]
  field_simp
  ring

-- M4: the band is reachable from z = 10 (false: 11^3 = 1331 > 26)
theorem m4_z10_below_band : (11 : ℝ) ^ 3 < 26 := by norm_num

-- M5: the universal column with 2 pi -> pi (false)
theorem m5_column_wrong (a0 G r : ℝ) (hG : G ≠ 0) (hr : r ≠ 0) :
    (1 / (4 * Real.pi * r ^ 2)) * (2 * a0 * r / G) = a0 / (Real.pi * G * r) := by
  field_simp
  ring

-- M6: the audit's offset width with the wrong coefficient (false)
theorem m6_audit_delta_wrong (n0 M : ℝ) (hM : M ≠ 0) :
    (n0 / M * (216 - 1)) - (n0 / M * (27 - 1)) = 190 * n0 / M := by
  ring

-- M7: the general-K dispersion without the law's k^2 term (the isolated-fluid form)
theorem m7_dispersion_isolated (n np k : ℝ) (hd : np + k ^ 2 ≠ 0) :
    -n * np / (np + k ^ 2) = -n + n * k ^ 2 / np := by
  field_simp
  ring

end DT2Mutate
