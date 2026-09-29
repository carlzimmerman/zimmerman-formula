import Mathlib
open Real Filter Topology intervalIntegral MeasureTheory

/- LR7: Lean certificates of the W1 exact moments (Z9 door).
  W1_tau0_cumulant.py (committed) banked N_num(tau0,q) = (3/4+5q/12) - B(q) tau0 + O(tau0^2)
  with -B(q) = Var(S_q)/2 exactly, resting on the (u,v) disk moments
  E[c^2] = 4/5, E[cT] = 2/5, E[T^2] = 208/945 (E[c] = 3/4, E[T] = 5/12 already
  certified by LR3/LR4c).  Here those three NEW moments' 1D cores are certified.
  Reduction provenance: after the (u,v) disk reduction (density (3/2)u, c = s - v,
  s = sqrt(1-u^2), T = (u^2+v^2)c + v c^2 + c^3/3; even-v projection), each moment
  is the following 1D integral (mechanical sympy, LR7_moments_lean.py; independently
  audited by LR7_r0_audit.py: dblquad + Gauss-Legendre/analytic-v, both rel <= 4e-13,
  and the exact coefficient identities b0 = (E[c^2]-E[c]^2)/2 = 19/160,
  b1 = E[cT]-E[c]E[T] = 7/80, b2 = (E[T^2]-E[T]^2)/2 = 703/30240 checked exactly):
    E[c^2]  = 4 * A,          A := int_0^1 u (1-u^2) sqrt(1-u^2)          = 1/5
    E[cT]   = (6/5) * C + 4 * B,   C := int u (1-u^2)^2 sqrt(1-u^2)       = 1/7
                                   B := int u^3 (1-u^2) sqrt(1-u^2)       = 2/35
    E[T^2]  = (8/21) * E + (12/5) * D + 4 * G,
              E := int u (1-u^2)^3 sqrt(1-u^2)                          = 1/9
              D := int u^3 (1-u^2)^2 sqrt(1-u^2)                        = 2/63
              G := int u^5 (1-u^2) sqrt(1-u^2)                          = 8/315
  Antiderivative primitive: T_k(u) = (1-u^2)^(k+1) * sqrt(1-u^2),
  T_k' = -(2k+3) * u * (1-u^2)^k * sqrt(1-u^2)  (0 < u < 1).
  HONEST SCOPE (LR3b precedent): the 1D values below are certified zero-sorry;
  the (u,v)-reduction leg (1D integral <- disk measure) is NUMERICALLY audited
  (LR7_r0_audit.py, two independent quadratures) but NOT Lean-certified here --
  the even-v projection is the same mechanism class as LR3b/LR4c's cov_generic,
  whose zero-sorry certificate covers the c/T engine definition used by W1. -/

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

/- The six base integrals. -/

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

theorem base_E : ∫ u in (0:ℝ)..1, u * (1 - u ^ 2) ^ 3 * Real.sqrt (1 - u ^ 2) = ((1:ℚ)/9 : ℝ) := by
  have hderiv : ∀ x ∈ Set.Ioo (0:ℝ) 1, HasDerivAt
      (fun w : ℝ => -((1:ℝ)/9) * ((1 - w ^ 2) ^ (3 + 1) * Real.sqrt (1 - w ^ 2)))
      (x * (1 - x ^ 2) ^ 3 * Real.sqrt (1 - x ^ 2)) x := by
    intro x hx
    have hx1 : 0 < 1 - x ^ 2 := by nlinarith [hx.1, hx.2]
    have t1 := (T_deriv x 3 hx1).const_mul (-((1:ℝ)/9))
    refine t1.congr_deriv ?_
    ring
  have hcont : ContinuousOn (fun w : ℝ => -((1:ℝ)/9) * ((1 - w ^ 2) ^ (3 + 1) * Real.sqrt (1 - w ^ 2)))
      (Set.Icc (0:ℝ) 1) := by fun_prop
  have hint : IntervalIntegrable (fun u : ℝ => u * (1 - u ^ 2) ^ 3 * Real.sqrt (1 - u ^ 2)) volume 0 1 := by
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

theorem base_D : ∫ u in (0:ℝ)..1, u ^ 3 * (1 - u ^ 2) ^ 2 * Real.sqrt (1 - u ^ 2) = ((2:ℚ)/63 : ℝ) := by
  have hderiv : ∀ x ∈ Set.Ioo (0:ℝ) 1, HasDerivAt
      ((fun w : ℝ => (-((1:ℝ)/7)) * ((1 - w ^ 2) ^ (2 + 1) * Real.sqrt (1 - w ^ 2)))
      + fun w : ℝ => (((1:ℝ)/9)) * ((1 - w ^ 2) ^ (3 + 1) * Real.sqrt (1 - w ^ 2)))
      (x ^ 3 * (1 - x ^ 2) ^ 2 * Real.sqrt (1 - x ^ 2)) x := by
    intro x hx
    have hx1 : 0 < 1 - x ^ 2 := by nlinarith [hx.1, hx.2]
    have t1 := (T_deriv x 2 hx1).const_mul (-((1:ℝ)/7))
    have t2 := (T_deriv x 3 hx1).const_mul (((1:ℝ)/9))
    exact (t1.add t2).congr_deriv (by ring)
  have hcont : ContinuousOn ((fun w : ℝ => (-((1:ℝ)/7)) * ((1 - w ^ 2) ^ (2 + 1) * Real.sqrt (1 - w ^ 2)))
      + fun w : ℝ => (((1:ℝ)/9)) * ((1 - w ^ 2) ^ (3 + 1) * Real.sqrt (1 - w ^ 2)))
      (Set.Icc (0:ℝ) 1) := by fun_prop
  have hint : IntervalIntegrable (fun u : ℝ => u ^ 3 * (1 - u ^ 2) ^ 2 * Real.sqrt (1 - u ^ 2)) volume 0 1 := by
    apply Continuous.intervalIntegrable
    fun_prop
  rw [integral_eq_sub_of_hasDerivAt_of_le (by norm_num) hcont hderiv hint]
  norm_num [Pi.add_apply]

theorem base_G : ∫ u in (0:ℝ)..1, u ^ 5 * (1 - u ^ 2) * Real.sqrt (1 - u ^ 2) = ((8:ℚ)/315 : ℝ) := by
  have hderiv : ∀ x ∈ Set.Ioo (0:ℝ) 1, HasDerivAt
      (((fun w : ℝ => (-((1:ℝ)/5)) * ((1 - w ^ 2) ^ (1 + 1) * Real.sqrt (1 - w ^ 2)))
      + fun w : ℝ => (((2:ℝ)/7)) * ((1 - w ^ 2) ^ (2 + 1) * Real.sqrt (1 - w ^ 2)))
      + fun w : ℝ => (-((1:ℝ)/9)) * ((1 - w ^ 2) ^ (3 + 1) * Real.sqrt (1 - w ^ 2)))
      (x ^ 5 * (1 - x ^ 2) * Real.sqrt (1 - x ^ 2)) x := by
    intro x hx
    have hx1 : 0 < 1 - x ^ 2 := by nlinarith [hx.1, hx.2]
    have t1 := (T_deriv x 1 hx1).const_mul (-((1:ℝ)/5))
    have t2 := (T_deriv x 2 hx1).const_mul (((2:ℝ)/7))
    have t3 := (T_deriv x 3 hx1).const_mul (-((1:ℝ)/9))
    exact ((t1.add t2).add t3).congr_deriv (by ring)
  have hcont : ContinuousOn (((fun w : ℝ => (-((1:ℝ)/5)) * ((1 - w ^ 2) ^ (1 + 1) * Real.sqrt (1 - w ^ 2)))
      + fun w : ℝ => (((2:ℝ)/7)) * ((1 - w ^ 2) ^ (2 + 1) * Real.sqrt (1 - w ^ 2)))
      + fun w : ℝ => (-((1:ℝ)/9)) * ((1 - w ^ 2) ^ (3 + 1) * Real.sqrt (1 - w ^ 2)))
      (Set.Icc (0:ℝ) 1) := by fun_prop
  have hint : IntervalIntegrable (fun u : ℝ => u ^ 5 * (1 - u ^ 2) * Real.sqrt (1 - u ^ 2)) volume 0 1 := by
    apply Continuous.intervalIntegrable
    fun_prop
  rw [integral_eq_sub_of_hasDerivAt_of_le (by norm_num) hcont hderiv hint]
  norm_num [Pi.add_apply]

/- The three W1 moment certificates. -/

theorem moment_c2 : ∫ u in (0:ℝ)..1, (4:ℝ) * (u * (1 - u ^ 2) * Real.sqrt (1 - u ^ 2))
    = ((4:ℚ)/5 : ℝ) := by
  rw [intervalIntegral.integral_const_mul, base_A]
  norm_num

theorem moment_cT : ∫ u in (0:ℝ)..1,
    ((6:ℝ)/5) * (u * (1 - u ^ 2) ^ 2 * Real.sqrt (1 - u ^ 2))
    + (4:ℝ) * (u ^ 3 * (1 - u ^ 2) * Real.sqrt (1 - u ^ 2))
    = ((2:ℚ)/5 : ℝ) := by
  rw [intervalIntegral.integral_add
      (f := fun u => ((6:ℝ)/5) * (u * (1 - u ^ 2) ^ 2 * Real.sqrt (1 - u ^ 2)))
      (g := fun u => (4:ℝ) * (u ^ 3 * (1 - u ^ 2) * Real.sqrt (1 - u ^ 2)))
      (Continuous.intervalIntegrable (by fun_prop) _ _)
      (Continuous.intervalIntegrable (by fun_prop) _ _),
      intervalIntegral.integral_const_mul, intervalIntegral.integral_const_mul,
      base_C, base_B]
  norm_num

theorem moment_T2 : ∫ u in (0:ℝ)..1,
    ((8:ℝ)/21) * (u * (1 - u ^ 2) ^ 3 * Real.sqrt (1 - u ^ 2))
    + ((12:ℝ)/5) * (u ^ 3 * (1 - u ^ 2) ^ 2 * Real.sqrt (1 - u ^ 2))
    + (4:ℝ) * (u ^ 5 * (1 - u ^ 2) * Real.sqrt (1 - u ^ 2))
    = ((208:ℚ)/945 : ℝ) := by
  rw [intervalIntegral.integral_add
      (f := fun u => ((8:ℝ)/21) * (u * (1 - u ^ 2) ^ 3 * Real.sqrt (1 - u ^ 2))
        + ((12:ℝ)/5) * (u ^ 3 * (1 - u ^ 2) ^ 2 * Real.sqrt (1 - u ^ 2)))
      (g := fun u => (4:ℝ) * (u ^ 5 * (1 - u ^ 2) * Real.sqrt (1 - u ^ 2)))
      (Continuous.intervalIntegrable (by fun_prop) _ _)
      (Continuous.intervalIntegrable (by fun_prop) _ _),
      intervalIntegral.integral_add
      (f := fun u => ((8:ℝ)/21) * (u * (1 - u ^ 2) ^ 3 * Real.sqrt (1 - u ^ 2)))
      (g := fun u => ((12:ℝ)/5) * (u ^ 3 * (1 - u ^ 2) ^ 2 * Real.sqrt (1 - u ^ 2)))
      (Continuous.intervalIntegrable (by fun_prop) _ _)
      (Continuous.intervalIntegrable (by fun_prop) _ _),
      intervalIntegral.integral_const_mul, intervalIntegral.integral_const_mul,
      intervalIntegral.integral_const_mul, base_E, base_D, base_G]
  norm_num

#print axioms moment_c2
#print axioms moment_cT
#print axioms moment_T2
