import Mathlib
open Real Filter Topology intervalIntegral MeasureTheory

/- LR8 -- Lean certificates of the W2 thin-window rationals A0 = 2/5, A1 = 8/35
   (Z12 door; W2 banked c00(q) = 2/5 + (8/35) q, commit 446286a06).

   Honest scope (LR3b/LR4c/LR7 mechanism-class precedent): the outer 1D cores
   base_A (int_0^1 u(1-u^2)^(3/2) = 1/5), base_B (int u^3(1-u^2)^(3/2) = 2/35)
   and base_C (int u(1-u^2)^(5/2) = 1/7) are UNCONDITIONAL zero-sorry
   certificates, copied verbatim from LR7_w1_moments.lean (commit 400e7919a);
   the rational assembly w2_A0_law / w2_A1_law is certified HERE. The
   geometric leg (p uniform in the unit ball x u isotropic -> cylindrical
   (rho,z) density (3/2) rho, z-substitution z = s w, dz = s dw, inner
   w-polynomial integrals 8/3, 16/15, -12/5, 32/5 with exact cancellation of
   the odd-in-w terms) is NOT probability-space-certified: it is
   numeric-audited (LR8 R0: sympy-Beta exact + mpmath/GL quadrature + MC of
   the full geometric reduction, n = 2e7; W2 K1/K2) -- the same mechanism
   class as LR4c's cov_generic and LR7's moments.

   Chain (W2_c00_tau0_expansion.py, conductor hand-derivation): after the
   reduction, with s = Real.sqrt (1 - rho^2),
     A0 = (3/2) * int_0^1 rho * (4/3) * s^3 drho                        = 2 * base_A,
     A1 = (3/2) * ( (4/3) * int rho^3 * s^3 drho
                  + (8/15) * int rho * s^5 drho ) = (3/2)*((4/3)*base_B + (8/15)*base_C),
   the 2*z*W^3/3 term and part of W^4/4 cancelling exactly
   (int w(1-w)^3 = -12/5, int (1-w)^4 = 32/5 over [-1,1], sum 0). -/

theorem hb_pow2 (u : ℝ) : HasDerivAt (fun w : ℝ => 1 - w ^ 2) (-2 * u) u := by
  have h1 : HasDerivAt (fun _ : ℝ => (1:ℝ)) 0 u := hasDerivAt_const u (1:ℝ)
  have h2 : HasDerivAt (fun w : ℝ => w ^ 2) (2 * u) u := by
    refine (hasDerivAt_pow 2 u).congr_deriv ?_
    norm_num
  have h3 : HasDerivAt (fun w : ℝ => 1 - w ^ 2) (-2 * u) u := by
    refine h1.sub h2 |>.congr_deriv ?_
    ring
  exact h3

theorem T_deriv (u : ℝ) (k : ℕ) (hu : 0 < 1 - u ^ 2) :
    HasDerivAt (fun w : ℝ => (1 - w ^ 2) ^ (k + 1) * Real.sqrt (1 - w ^ 2))
      (-(2 * (k : ℝ) + 3) * u * (1 - u ^ 2) ^ k * Real.sqrt (1 - u ^ 2)) u := by
  have hb := hb_pow2 u
  have hp := hb.pow (k + 1)
  have hsqr : HasDerivAt Real.sqrt (1 / (2 * Real.sqrt (1 - u ^ 2))) (1 - u ^ 2) :=
    Real.hasDerivAt_sqrt (ne_of_gt hu)
  have h3 : HasDerivAt (fun w : ℝ => Real.sqrt (1 - w ^ 2))
      ((1 / (2 * Real.sqrt (1 - u ^ 2))) * (-2 * u)) u := hsqr.comp u hb
  have h := hp.mul h3
  refine h.congr_deriv ?_
  have hs : (Real.sqrt (1 - u ^ 2)) ^ 2 = 1 - u ^ 2 := Real.sq_sqrt hu.le
  have hpos : Real.sqrt (1 - u ^ 2) ≠ 0 := (Real.sqrt_pos.mpr hu).ne'
  simp only [Pi.pow_apply, pow_succ, Nat.succ_sub_one]
  field_simp [hs]
  rw [hs]
  simp only [Nat.cast_add]
  ring

theorem base_A : ∫ u in (0:ℝ)..1, u * (1 - u ^ 2) * Real.sqrt (1 - u ^ 2) = ((1:ℚ)/5 : ℝ) := by
  have hderiv : ∀ x ∈ Set.Ioo (0:ℝ) 1, HasDerivAt
      (fun w : ℝ => (-((1:ℝ)/5)) * ((1 - w ^ 2) ^ (1 + 1) * Real.sqrt (1 - w ^ 2)))
      (x * (1 - x ^ 2) * Real.sqrt (1 - x ^ 2)) x := by
    intro x hx
    have hx1 : 0 < 1 - x ^ 2 := by nlinarith [hx.1, hx.2]
    have t1 := (T_deriv x 1 hx1).const_mul (-((1:ℝ)/5))
    refine t1.congr_deriv ?_
    ring
  have hcont : ContinuousOn (fun w : ℝ => (-((1:ℝ)/5)) * ((1 - w ^ 2) ^ (1 + 1) * Real.sqrt (1 - w ^ 2)))
      (Set.Icc (0:ℝ) 1) := by fun_prop
  have hint : IntervalIntegrable (fun u : ℝ => u * (1 - u ^ 2) * Real.sqrt (1 - u ^ 2)) volume 0 1 := by
    apply Continuous.intervalIntegrable
    fun_prop
  rw [integral_eq_sub_of_hasDerivAt_of_le (by norm_num) hcont hderiv hint]
  norm_num [Pi.add_apply]

theorem base_C : ∫ u in (0:ℝ)..1, u * (1 - u ^ 2) ^ 2 * Real.sqrt (1 - u ^ 2) = ((1:ℚ)/7 : ℝ) := by
  have hderiv : ∀ x ∈ Set.Ioo (0:ℝ) 1, HasDerivAt
      (fun w : ℝ => -((1:ℝ)/7) * ((1 - w ^ 2) ^ (2 + 1) * Real.sqrt (1 - w ^ 2)))
      (x * (1 - x ^ 2) ^ 2 * Real.sqrt (1 - x ^ 2)) x := by
    intro x hx
    have hx1 : 0 < 1 - x ^ 2 := by nlinarith [hx.1, hx.2]
    have t1 := (T_deriv x 2 hx1).const_mul (-((1:ℝ)/7))
    refine t1.congr_deriv ?_
    ring
  have hcont : ContinuousOn (fun w : ℝ => -((1:ℝ)/7) * ((1 - w ^ 2) ^ (2 + 1) * Real.sqrt (1 - w ^ 2)))
      (Set.Icc (0:ℝ) 1) := by fun_prop
  have hint : IntervalIntegrable (fun u : ℝ => u * (1 - u ^ 2) ^ 2 * Real.sqrt (1 - u ^ 2)) volume 0 1 := by
    apply Continuous.intervalIntegrable
    fun_prop
  rw [integral_eq_sub_of_hasDerivAt_of_le (by norm_num) hcont hderiv hint]
  norm_num [Pi.add_apply]

theorem base_B : ∫ u in (0:ℝ)..1, u ^ 3 * (1 - u ^ 2) * Real.sqrt (1 - u ^ 2) = ((2:ℚ)/35 : ℝ) := by
  have hderiv : ∀ x ∈ Set.Ioo (0:ℝ) 1, HasDerivAt
      ((fun w : ℝ => (-((1:ℝ)/5)) * ((1 - w ^ 2) ^ (1 + 1) * Real.sqrt (1 - w ^ 2)))
      + fun w : ℝ => (((1:ℝ)/7)) * ((1 - w ^ 2) ^ (2 + 1) * Real.sqrt (1 - w ^ 2)))
      (x ^ 3 * (1 - x ^ 2) * Real.sqrt (1 - x ^ 2)) x := by
    intro x hx
    have hx1 : 0 < 1 - x ^ 2 := by nlinarith [hx.1, hx.2]
    have t1 := (T_deriv x 1 hx1).const_mul (-((1:ℝ)/5))
    have t2 := (T_deriv x 2 hx1).const_mul (((1:ℝ)/7))
    exact (t1.add t2).congr_deriv (by ring)
  have hcont : ContinuousOn ((fun w : ℝ => (-((1:ℝ)/5)) * ((1 - w ^ 2) ^ (1 + 1) * Real.sqrt (1 - w ^ 2)))
      + fun w : ℝ => (((1:ℝ)/7)) * ((1 - w ^ 2) ^ (2 + 1) * Real.sqrt (1 - w ^ 2)))
      (Set.Icc (0:ℝ) 1) := by fun_prop
  have hint : IntervalIntegrable (fun u : ℝ => u ^ 3 * (1 - u ^ 2) * Real.sqrt (1 - u ^ 2)) volume 0 1 := by
    apply Continuous.intervalIntegrable
    fun_prop
  rw [integral_eq_sub_of_hasDerivAt_of_le (by norm_num) hcont hderiv hint]
  norm_num [Pi.add_apply]

/- The W2 assembly. -/
theorem w2_A0_law :
    (2:ℝ) * (∫ u in (0:ℝ)..1, u * (1 - u ^ 2) * Real.sqrt (1 - u ^ 2))
      = ((2:ℚ)/5 : ℝ) := by
  rw [base_A]
  norm_num

theorem w2_A1_law :
    ((3:ℝ)/2) * (((4:ℝ)/3) * (∫ u in (0:ℝ)..1, u ^ 3 * (1 - u ^ 2) * Real.sqrt (1 - u ^ 2))
      + ((8:ℝ)/15) * (∫ u in (0:ℝ)..1, u * (1 - u ^ 2) ^ 2 * Real.sqrt (1 - u ^ 2)))
      = ((8:ℚ)/35 : ℝ) := by
  rw [base_B, base_C]
  norm_num

#print axioms w2_A0_law
#print axioms w2_A1_law
