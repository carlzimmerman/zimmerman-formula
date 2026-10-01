/-
AS233 Lean 4 certificate -- Tier-0b preferred-frame vector response.
Certified identities:

  (1) Clock-normal unit consistency to second order:
        X_tau = 1 + t  (t = X_tau - 1),  sqrt-series  q(t) = 1 - t/2 + 3 t^2/8.
        Claim:  (1 + t) * q(t)^2 - 1 = (5/8) t^3 - (15/64) t^4 + (9/64) t^5,
        i.e. the truncated unit normal n = -tau/sqrt(X_tau) satisfies
        n . n = -1 through terms of degree two in the perturbation
        (matches the script's 'unit check (trunc) = 0').

  (2) Closed-form preferred-frame response of CA5-GNC-R in the
      high-acceleration window (S_k -> 0, gate inactive):
        alpha_1(alpha, c2) = 4 (alpha + 2 c2) / (2 - c2)
      certified at the exact rational reference cell
      (alpha, ell, c2) = (3/10, 1/25, 1/2), where the ladder reads
      alpha_1 = 52/15 (Will dictionary alpha_1 = 2 coeff(g_02, w_2)/U_amp,
      U_amp = -Psi_k/R_k), and the pure-clock limit 2 alpha at c2 = 0.

All statements are elementary real arithmetic: proven by norm_num/ring_nf.
-/
import Mathlib

open Real

-- (1) unit-normal consistency of the sqrt series
theorem sqrt_series_unit_identity (t : ℝ) :
    (1 + t) * (1 - t / 2 + 3 * t ^ 2 / 8) ^ 2 - 1
      = (5 / 8) * t ^ 3 - (15 / 64) * t ^ 4 + (9 / 64) * t ^ 5 := by
  ring_nf

theorem sqrt_series_unit_mod_cube (t : ℝ) :
    (1 + t) * (1 - t / 2 + 3 * t ^ 2 / 8) ^ 2 - 1
      = t ^ 3 * ((5:ℝ) / 8 - (15:ℝ) / 64 * t + (9:ℝ) / 64 * t ^ 2) := by
  ring_nf

-- second-order terms vanish identically (the truncation is unit-consistent):
theorem sqrt_series_low_order (t : ℝ) :
    (1 + t) * (1 - t / 2 + 3 * t ^ 2 / 8) ^ 2 = 1 + t ^ 3 * ((5:ℝ) / 8
      - (15:ℝ) / 64 * t + (9:ℝ) / 64 * t ^ 2) := by
  ring_nf

-- (2) closed form at the C1 reference cell:  alpha_1 = 52/15
theorem alpha1_closed_form_cell :
    4 * ((3:ℝ) / 10 + 2 * (1 / 2 : ℝ)) / (2 - (1 / 2 : ℝ)) = 52 / 15 := by
  norm_num

-- dictionary consistency: 2 * c2t_v / U_amp = 52/15  with the ACTUAL ladder
-- amplitudes (extracted from the run, cell C1):
--   c2t  = coeff(d1_B2k, w_2)/R_k = 416 pi / 51
--   U_amp = -Psi_k/R_k           = 80 pi / 17
theorem alpha1_dictionary_cell (c2t U : ℝ) (hc2 : c2t = (416:ℝ) * Real.pi / 51)
    (hU : U = 80 * Real.pi / 17) :
    2 * c2t / U = 52 / 15 := by
  rw [hc2, hU]
  field_simp [Real.pi_ne_zero]
  norm_num

-- pure-clock limit:  c2 -> 0  gives  alpha_1 = 2 alpha
theorem alpha1_clock_limit (α : ℝ) : 4 * (α + 2 * 0) / (2 - 0) = 2 * α := by
  ring

-- trace-mixing-only limit:  alpha -> 0  gives  alpha_1 = 8 c2 / (2 - c2)
theorem alpha1_trace_limit (c2 : ℝ) (hc : c2 ≠ 2) : 4 * (0 + 2 * c2) / (2 - c2) = 8 * c2 / (2 - c2) := by
  field_simp [hc]
  ring

-- Einstein limit:  alpha = c2 = 0  =>  alpha_1 = 0
theorem alpha1_einstein_limit : 4 * (0 + 2 * 0) / (2 - 0) = 0 := by
  norm_num

-- the trace-mixing branch value -4E cannot equal the cell value for any E > 0:
theorem negative_control_residual (E : ℝ) (hE : 0 < E) :
    4 * ((3:ℝ) / 10 + 2 * (1 / 2 : ℝ)) / (2 - (1 / 2 : ℝ)) + 4 * E ≠ 0 := by
  rw [alpha1_closed_form_cell]
  norm_num
  linarith [hE]

#check sqrt_series_unit_identity
#check alpha1_closed_form_cell
#check alpha1_dictionary_cell
#check negative_control_residual