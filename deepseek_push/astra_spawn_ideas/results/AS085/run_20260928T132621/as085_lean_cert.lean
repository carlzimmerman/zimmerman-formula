/-
AS085 Lean certificate -- External Newtonian baryon virial term.

SCOPE (read before over-reading this file): Lean certifies the MATHEMATICS
below, not that the framework describes nature.  The physical premises are
stated as hypotheses: the external Newtonian point-mass well
Phi_b(r) = -G*M_b/r on r > 0, the equilibrium phantom density rho = A/r^2, the
equipartition normalization A = C/(4*pi*G) with C = sqrt(G*M_b*a0) (this file
carries the two combinations 4*pi*G*A = C and G*M_b/r_M = C as hypotheses; the
sqrt deductions from r_M = sqrt(G*M_b/a0), C = sqrt(G*M_b*a0) are verified in
the Python lane as_single.py and are one-line algebraic consequences), and the
G091 closed virial chain 2T + W_self + W_bar = 3*P_s*V with the isothermal
fluid closure.

Certified theorems:
 1) vthm_phi_deriv          d/dr [-G*M/r] = G*M/r^2 pointwise (r != 0)
 2) vthm_r_phi'_eq_neg_phi  r * Phi_b' = -Phi_b  (the work form and the
                            potential form of W_bar are the same integrand:
                            -int rho r Phi_b' dV = int rho Phi_b dV)
 3) vthm_log_shell_integral int_{rb}^{R} dx/x = ln R - ln rb  (FTC, log
                            antiderivative; 0 < rb <= R)
 4) vthm_wbar_shell_integral the assembled shell integral equals
                            -(M_b*C)*L with L = ln R - ln rb, given
                            A = C/(4*pi*G)  (scale factors and sign bookkeeping)
 5) vthm_wbar_coefficient   -(4*pi*G*M_b*A)*L = -(M_b*C)*L from A = C/(4*pi*G)
 6) vthm_log_per_decade     ln(R/(r/10)) - ln(R/r) = ln 10  (NC1/NC2 growth
                            rate: |W_bar| rises by exactly M_b*C*ln(10) per
                            decade as the inner edge drops or the outer edge
                            rises)
 7) vthm_virial_fluid       2T + W_self + W_bar = 3 P_s V with T=(3/2) lam M_b
                            sigma^2, W_self = -lam M_b C, W_bar = -M_b C L,
                            3 P_s V = lam M_b sigma^2  =>  sigma^2 =
                            (C/2)*(1 + L/lam)
 8) vthm_virial_bare        same chain WITHOUT the boundary term  =>
                            sigma^2 = (C/3)*(1 + L/lam)
 9) vthm_virial_triad       L = 0 boundary (r_b = r_break): sigma^2 = C/2
10) vthm_ratio_bare_over_fluid  sigma^2_bare / sigma^2_fluid = 2/3 exactly
                            (NC3: the C/2 triad is NOT a bare-virial answer)
11) vthm_wself_bookkeeping  -G*M_T^2/R = -lam*M_b*C with M_T = lam M_b,
                            R = lam r_M (uses G*M_b = C*r_M)

Hard bar: zero `sorry`, axioms subseteq {propext, Classical.choice,
Quot.sound}; verified via `#print axioms` at the end of this file.
-/
import Mathlib
import Mathlib.Analysis.SpecialFunctions.Log.Deriv
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.MeasureTheory.Integral.IntervalIntegral.FundThmCalculus

open Real
open scoped Topology
noncomputable section

-- 1 ------------------------------------------------------------------
theorem vthm_phi_deriv (G M r : ℝ) (hr : r ≠ 0) :
    deriv (fun x : ℝ => -(G * M) / x) r = (G * M) / r ^ 2 := by
  have hfun : (fun x : ℝ => -(G * M) / x) = fun x : ℝ => -(G * M) * x⁻¹ := by
    funext x
    rw [div_eq_mul_inv]
  rw [hfun]
  rw [deriv_const_mul_field]
  rw [deriv_inv]
  field_simp [hr]

-- 2 ------------------------------------------------------------------
theorem vthm_r_phi'_eq_neg_phi (G M r : ℝ) (hr : r ≠ 0) :
    r * deriv (fun x : ℝ => -(G * M) / x) r = -(-(G * M) / r) := by
  rw [vthm_phi_deriv G M r hr]
  field_simp [hr]

-- 3 ------------------------------------------------------------------
theorem vthm_log_shell_integral (rb R : ℝ) (hrb : 0 < rb) (hle : rb ≤ R) :
    ∫ x in rb..R, (x:ℝ)⁻¹ = Real.log R - Real.log rb := by
  have hderiv : deriv (fun x : ℝ => Real.log x) = fun x : ℝ => x⁻¹ := by
    funext x
    rw [Real.deriv_log]
  have hdiff : ∀ x ∈ Set.uIcc rb R, DifferentiableAt ℝ (fun y : ℝ => Real.log y) x := by
    intro x hx
    rw [Set.uIcc_of_le hle] at hx
    exact Real.differentiableAt_log (ne_of_gt (lt_of_lt_of_le hrb hx.1))
  have hcont : ContinuousOn (fun x : ℝ => x⁻¹) (Set.uIcc rb R) := by
    exact continuousOn_inv₀.mono (by
      intro x hx
      rw [Set.uIcc_of_le hle] at hx
      exact ne_of_gt (lt_of_lt_of_le hrb hx.1))
  simpa using (intervalIntegral.integral_deriv_eq_sub' (f := fun x : ℝ => Real.log x)
    (f' := fun x : ℝ => x⁻¹) hderiv hdiff hcont)

-- 4 ------------------------------------------------------------------
theorem vthm_wbar_shell_integral (G M_b C A R rb L : ℝ)
    (hA : A = C / (4 * Real.pi * G)) (hG : G ≠ 0) (hrb : 0 < rb)
    (hle : rb ≤ R) (hL : L = Real.log R - Real.log rb) :
    -(4 * Real.pi * G * M_b * A) * (∫ x in rb..R, (x:ℝ)⁻¹) = -(M_b * C) * L := by
  rw [vthm_log_shell_integral rb R hrb hle]
  rw [hL]
  rw [hA]
  have hpiG : (4 : ℝ) * Real.pi * G ≠ 0 := by
    exact mul_ne_zero (mul_ne_zero (by norm_num) (ne_of_gt Real.pi_pos)) hG
  field_simp [hpiG]

-- 5 ------------------------------------------------------------------
theorem vthm_wbar_coefficient (G M_b C A L : ℝ)
    (hA : A = C / (4 * Real.pi * G)) (hG : G ≠ 0) :
    -(4 * Real.pi * G * M_b * A) * L = -(M_b * C) * L := by
  rw [hA]
  field_simp [hG]

-- 6 ------------------------------------------------------------------
theorem vthm_log_per_decade (R r : ℝ) (hR : 0 < R) (hr : 0 < r) :
    Real.log (R / (r / 10)) - Real.log (R / r) = Real.log 10 := by
  have hnn : R / (r / 10) ≠ 0 := by positivity
  have hnn2 : R / r ≠ 0 := by positivity
  have hdiv : R / (r / 10) = (R / r) * 10 := by field_simp
  rw [hdiv]
  rw [Real.log_mul hnn2 (by norm_num : (10 : ℝ) ≠ 0)]
  ring

-- 7 ------------------------------------------------------------------
theorem vthm_virial_fluid (M_b C lam L s2 : ℝ)
    (hMb : M_b ≠ 0) (hlam : lam ≠ 0)
    (h : 3 * lam * M_b * s2 - lam * M_b * C - M_b * C * L = lam * M_b * s2) :
    s2 = C / 2 * (1 + L / lam) := by
  field_simp [hMb, hlam] at h
  field_simp [hlam]
  nlinarith [h]

-- 8 ------------------------------------------------------------------
theorem vthm_virial_bare (M_b C lam L s2 : ℝ)
    (hMb : M_b ≠ 0) (hlam : lam ≠ 0)
    (h : 3 * lam * M_b * s2 - lam * M_b * C - M_b * C * L = 0) :
    s2 = C / 3 * (1 + L / lam) := by
  field_simp [hMb, hlam] at h
  have h0 : lam * (3 * s2 - C) - C * L = 0 := by
    exact (mul_eq_zero.mp h).resolve_left hMb
  field_simp [hlam]
  nlinarith [h0]

-- 9 ------------------------------------------------------------------
theorem vthm_virial_triad (M_b C lam s2 : ℝ)
    (hMb : M_b ≠ 0) (hlam : lam ≠ 0)
    (h : 3 * lam * M_b * s2 - lam * M_b * C = lam * M_b * s2) :
    s2 = C / 2 := by
  field_simp [hMb, hlam] at h
  linarith

-- 10 -----------------------------------------------------------------
theorem vthm_ratio_bare_over_fluid (C lam L : ℝ) :
    C / 3 * (1 + L / lam) = (2 / 3) * (C / 2 * (1 + L / lam)) := by
  ring

-- 11 -----------------------------------------------------------------
-- cross-multiplied form (division atoms are opaque to ring; the divided
-- statement -G*M_T^2/R = -lam*M_b*C follows for r_M != 0, lam != 0)
theorem vthm_wself_bookkeeping (G M_b C lam r_M : ℝ)
    (hGM : G * M_b = C * r_M) :
    -G * (lam * M_b) ^ 2 = -(lam * M_b * C) * (lam * r_M) := by
  linear_combination -(lam ^ 2 * M_b) * hGM

end

open scoped Topology

#print axioms vthm_phi_deriv
#print axioms vthm_r_phi'_eq_neg_phi
#print axioms vthm_log_shell_integral
#print axioms vthm_wbar_shell_integral
#print axioms vthm_wbar_coefficient
#print axioms vthm_log_per_decade
#print axioms vthm_virial_fluid
#print axioms vthm_virial_bare
#print axioms vthm_virial_triad
#print axioms vthm_ratio_bare_over_fluid
#print axioms vthm_wself_bookkeeping
