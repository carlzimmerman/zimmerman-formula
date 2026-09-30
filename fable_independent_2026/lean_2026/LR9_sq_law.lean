import Mathlib
open Real Filter Topology intervalIntegral MeasureTheory

/- LR9 -- Lean certificates of the W3 survival law rationals (Z13 door).
   W3 (exit 0, deepseek_push/W3_results.json) banked the survival correction
   S(q) = C00 + q C01 + q^2 C02 = 1/3 + (1/3) q + (46/525) q^2.

   Chain (LR9_sq_law.py R0a, fresh monomial-basis derivation; W3 used
   sp.integrate -- the two paths are independent): after the cylindrical
   reduction (s = sqrt(1-x^2), W = s(1-w), Z = s w, R = 1-s^2+s^2 w^2,
   odd-w monomials vanish on [-1,1]), each C_k is a rational assembly of the
   U-class outer cores int_0^1 x (1-x^2)^j dx = 1/(2j+2):
     C00 = 2       * core(j=2)                          = 1/3
     C01 = 4       * core(j=2) - (8/3)  * core(j=3)     = 1/3
     C02 = 2       * core(j=2) - (8/3)  * core(j=3)
           + (92/105) * core(j=4)                         = 46/525
   (only EVEN-m cores appear -- the odd-m coefficients cancel exactly in the
   fresh derivation; R0b quadrature mp dps=40 GL(300) + float64 GL(600) and
   R0c MC at fresh seed 20260930 confirm the reduction numerically).

   HONEST SCOPE (LR3b/LR4c/LR7/LR8 precedent): the 1D core values and the
   rational assembly are CERTIFIED here, zero-sorry, unconditional; the
   geometric reduction leg (v-integration to the wall W = s(1-w), the
   cylindrical density (3/2) x, the odd-w cancellation) is NUMERICALLY
   audited (LR9_sq_law.py R0a exact-monomial + R0b quadratures + R0c MC),
   not probability-space-certified. -/

theorem hb_pow2 (u : ℝ) : HasDerivAt (fun w : ℝ => 1 - w ^ 2) (-2 * u) u := by
  have h1 : HasDerivAt (fun _ : ℝ => (1:ℝ)) 0 u := hasDerivAt_const u (1:ℝ)
  have h2 : HasDerivAt (fun w : ℝ => w ^ 2) (2 * u) u := by
    refine (hasDerivAt_pow 2 u).congr_deriv ?_
    norm_num
  have h3 : HasDerivAt (fun w : ℝ => 1 - w ^ 2) (-2 * u) u := by
    refine h1.sub h2 |>.congr_deriv ?_
    ring
  exact h3

/-- U-class primitive: (1-u^2)^(j+1) has derivative -2(j+1) u (1-u^2)^j. -/
theorem U_deriv (u : ℝ) (j : ℕ) :
    HasDerivAt (fun w : ℝ => (1 - w ^ 2) ^ (j + 1))
      (-2 * ((j : ℝ) + 1) * u * (1 - u ^ 2) ^ j) u := by
  have hb := hb_pow2 u
  have hp := hb.pow (j + 1)
  refine hp.congr_deriv ?_
  simp only [Nat.add_sub_cancel, Nat.cast_add, Nat.cast_one]
  ring

/-- Generic U-class core: int_0^1 x (1-x^2)^j dx = 1/(2j+2). -/
theorem core_U (j : ℕ) :
    ∫ u in (0:ℝ)..1, u * (1 - u ^ 2) ^ j = 1 / (2 * (j : ℝ) + 2) := by
  have hderiv : ∀ x ∈ Set.Ioo (0:ℝ) 1, HasDerivAt
      (fun w : ℝ => (-1 / (2 * (j : ℝ) + 2)) * (1 - w ^ 2) ^ (j + 1))
      (x * (1 - x ^ 2) ^ j) x := by
    intro x hx
    have t1 := (U_deriv x j).const_mul (-1 / (2 * (j : ℝ) + 2))
    refine t1.congr_deriv ?_
    field_simp
  have hcont : ContinuousOn (fun w : ℝ => (-1 / (2 * (j : ℝ) + 2)) * (1 - w ^ 2) ^ (j + 1))
      (Set.Icc (0:ℝ) 1) := by fun_prop
  have hint : IntervalIntegrable (fun u : ℝ => u * (1 - u ^ 2) ^ j) volume 0 1 := by
    apply Continuous.intervalIntegrable
    fun_prop
  rw [integral_eq_sub_of_hasDerivAt_of_le (by norm_num) hcont hderiv hint]
  have hzero : (0:ℝ) ^ (j + 1) = 0 := zero_pow (by omega : (j:ℕ) + 1 ≠ 0)
  have hA : (1 - (1:ℝ) ^ 2) ^ (j + 1) = 0 := by
    have hb1 : (1 - (1:ℝ) ^ 2) = 0 := by norm_num
    rw [hb1]; exact hzero
  have hB : (1 - (0:ℝ) ^ 2) ^ (j + 1) = 1 := by norm_num
  show (-1 / (2 * (j:ℝ) + 2)) * (1 - (1:ℝ) ^ 2) ^ (j + 1)
      - (-1 / (2 * (j:ℝ) + 2)) * (1 - (0:ℝ) ^ 2) ^ (j + 1) = 1 / (2 * (j:ℝ) + 2)
  rw [hA, hB]
  field_simp
  norm_num

/-- The three assembly laws of the W3 survival correction. -/

theorem s00_law : (2:ℝ) * (∫ u in (0:ℝ)..1, u * (1 - u ^ 2) ^ 2) = (1:ℝ)/3 := by
  rw [core_U 2]
  norm_num

theorem s01_law : (4:ℝ) * (∫ u in (0:ℝ)..1, u * (1 - u ^ 2) ^ 2)
    - (8/3) * (∫ u in (0:ℝ)..1, u * (1 - u ^ 2) ^ 3) = (1:ℝ)/3 := by
  rw [core_U 2, core_U 3]
  norm_num

theorem s02_law : (2:ℝ) * (∫ u in (0:ℝ)..1, u * (1 - u ^ 2) ^ 2)
    - (8/3) * (∫ u in (0:ℝ)..1, u * (1 - u ^ 2) ^ 3)
    + (92/105) * (∫ u in (0:ℝ)..1, u * (1 - u ^ 2) ^ 4) = (46:ℝ)/525 := by
  rw [core_U 2, core_U 3, core_U 4]
  norm_num

#print axioms core_U
#print axioms s00_law
#print axioms s01_law
#print axioms s02_law
