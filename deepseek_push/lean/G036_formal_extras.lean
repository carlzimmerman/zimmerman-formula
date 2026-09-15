/-
  G036/G037 -- THE SLAB COLUMN-CANCELLATION CHAIN (G024) and the
  NOETHER-CHARGE w-WINDOW COLDNESS BOUND (G028) -- the Lean certificates.

  PART 1 (G036, from G024_slab_limit.py V7/V4b).  The phantom slab density
  rho_ph(z) = A*z^(-1/2) - rho_b with A^2 = rb^2*z_c (equivalently
  A^2 = a0*rb/(16*pi*G) and z_c = a0/(16*pi*G*rb), so that z* = 4*z_c,
  proved here as slab_zstar_eq_four_zc).  Four theorems close the
  certified-but-unformalized chain:

    (a) box_nu_extends: at z = z* = 4*z_c the two formulas for the
        box-averaged vertical boost AGREE -- 2*sqrt(z_c/z*) = 1 exactly.
        Continuity of the nu_box curve at the saturation point: inside the
        slab the curve is 2*sqrt(z_c/z), beyond it the certified constant 1,
        and the two branches meet at z*.
    (b) rho_ph_at_saturation: the local density at z* is exactly -rho_b/2
        (the negative outer layer's endpoint value, zero-parameter).
    (c) slab_column_zero: the TWO-SIDED net dark column over the whole slab,
        integral_0^z* 2*(A z^(-1/2) - rho_b) dz, is EXACTLY ZERO -- the
        negative outer layer cancels the positive core.  Closed with
        Mathlib's `integral_rpow` (r = -1/2, valid on [0, z*]); the
        cancellation reduces to 4*A*sqrt(z_c) = 4*rho_b*z_c, i.e.
        A*sqrt(z_c) = rho_b*z_c, which is A*sqrt(z_c) = sqrt(A^2 z_c)
        = sqrt(rb^2 z_c^2) = rb*z_c.
    (d) peak_column: the one-sided column integral over [0, z_c] equals
        a0/(16*pi*G) exactly (given A^2 = a0*rb/(16*pi*G)), so the
        two-sided PEAK column is a0/(8*pi*G) -- the registered
        26.7 M_sun/pc^2 number.  Stated symbolically and anchored
        numerically (num_peak_column_msun): with the certified
        a0 = 9.3619e-11 m/s^2 and G = 6.674e-11 SI, the peak column lies
        strictly between 26 and 27 M_sun/pc^2.

  PART 2 (G037, from G028_noether_dark_sector.py V1).  The Noether charge
  dust equation of state w satisfies 0 < w <= 5.7e-7; its density scales as
  a^(-3(1+w)).  Three theorems, stated HONESTLY at the exponent level and
  at a = 1 (the G028 claim "the exponent differs from cold dust by < 2e-6"
  is an EXPONENT statement; the relative DENSITY difference at a = 1/1101
  is ~ 3*w*ln(1101) ~ 8.4e-5, NOT 2e-6, and is deliberately NOT claimed):

    - w_window_exponent: |(-3)*(1+w) - (-3)| = 3*w <= 1.71e-6 < 2e-6 --
      the cold-dust exponent a^-3 is recovered to within 2 parts per
      million across the whole window.
    - w_window_cold: the window is inside the acoustic reach,
      w <= 5.7e-7 < 1e-4.
    - rho_vs_dust_a1: at a = 1 the densities agree EXACTLY
      (1^(-3(1+w)) = 1^(-3) = 1); the window bound bites only away from
      a = 1, at the exponent level.
-/
import Mathlib

open MeasureTheory intervalIntegral

noncomputable section

/-! ## PART 1 -- G024: the slab saturation and column cancellation. -/

/-- **slab_zstar_eq_four_zc.** The branch-crossing height z* = a0/(4*pi*G*rb)
is exactly FOUR times the layer half-width z_c = a0/(16*pi*G*rb): z* = 4*z_c. -/
theorem slab_zstar_eq_four_zc (a0 G rb : ℝ) (ha0 : 0 < a0) (hG : 0 < G) (hrb : 0 < rb) :
    a0 / (4 * Real.pi * G * rb) = 4 * (a0 / (16 * Real.pi * G * rb)) := by
  field_simp [hG, hrb, Real.pi_pos]
  ring

/-- **box_nu_extends (saturation continuity).** At z = z* = 4*z_c the
box-averaged vertical boost  nu_box(z) = 2*sqrt(z_c/z)  (the in-slab branch)
equals EXACTLY 1, the certified constant value beyond z*: the two branches
of the box-nu curve AGREE at the saturation point. -/
theorem box_nu_extends (zc : ℝ) (hzc : 0 < zc) :
    2 * Real.sqrt (zc / (4 * zc)) = 1 := by
  have h1 : zc / (4 * zc) = 1 / 4 := by field_simp
  have h2 : Real.sqrt (1 / 4) = 1 / 2 := by
    have hp : (0:ℝ) ≤ Real.sqrt (1 / 4) := Real.sqrt_nonneg _
    have hsq : (Real.sqrt (1 / 4 : ℝ)) ^ 2 = (1 / 2) ^ 2 := by
      rw [Real.sq_sqrt (by norm_num : (0:ℝ) ≤ 1 / 4)]
      norm_num
    calc Real.sqrt (1 / 4 : ℝ) = Real.sqrt ((Real.sqrt (1 / 4 : ℝ)) ^ 2) := (Real.sqrt_sq hp).symm
      _ = Real.sqrt ((1 / 2 : ℝ) ^ 2) := by rw [hsq]
      _ = 1 / 2 := Real.sqrt_sq (by norm_num)
  rw [h1, h2]
  ring

/-- **rho_ph_at_saturation.** The local phantom density at the saturation
height: A/sqrt(z*) - rho_b = -rho_b/2 exactly, where A^2 = rb^2*z_c and
z* = 4*z_c.  The negative outer layer ends AT -rho_b/2 -- a direct,
zero-parameter falsifiable prediction for the local vertical mass profile. -/
theorem rho_ph_at_saturation (A rb zc : ℝ) (hA : 0 < A) (hrb : 0 < rb)
    (hzc : 0 < zc) (hAsq : A ^ 2 = rb ^ 2 * zc) :
    A * (4 * zc) ^ (-1 / (2:ℝ)) - rb = -rb / 2 := by
  have hz4 : (0:ℝ) < 4 * zc := by positivity
  have hAeq : A = rb * Real.sqrt zc := by
    have h3 : (0:ℝ) ≤ rb * Real.sqrt zc := by positivity
    have hsq : A ^ 2 = (rb * Real.sqrt zc) ^ 2 := by
      calc A ^ 2 = rb ^ 2 * zc := hAsq
        _ = rb ^ 2 * (Real.sqrt zc) ^ 2 := by rw [Real.sq_sqrt hzc.le]
        _ = (rb * Real.sqrt zc) ^ 2 := by ring
    calc A = Real.sqrt (A ^ 2) := (Real.sqrt_sq hA.le).symm
      _ = Real.sqrt ((rb * Real.sqrt zc) ^ 2) := by rw [hsq]
      _ = rb * Real.sqrt zc := Real.sqrt_sq h3
  have hsqzne : Real.sqrt zc ≠ 0 := by
    intro h
    rw [← Real.sq_sqrt hzc.le, h] at hzc
    exact absurd hzc (by norm_num)
  have hsqrt4 : Real.sqrt (4 * zc) = 2 * Real.sqrt zc := by
    rw [Real.sqrt_mul (by norm_num : (0:ℝ) ≤ 4) zc, show Real.sqrt (4:ℝ) = 2 from by norm_num]
  have hinv : (4 * zc) ^ (-1 / (2:ℝ)) = (2 * Real.sqrt zc)⁻¹ := by
    rw [show (-1 / (2:ℝ)) = (-(1 / (2:ℝ))) from by norm_num, Real.rpow_neg hz4.le,
      ← Real.sqrt_eq_rpow, hsqrt4]
  rw [hinv, hAeq]
  field_simp [hsqzne]
  ring_nf

/-- **slab_column_zero (the exact zero at z* = 4*z_c).** The two-sided net
dark column over the whole slab is EXACTLY zero:
  ∫_0^z* 2*(A z^(-1/2) - rho_b) dz = 4*A*sqrt(z*) - 2*rho_b*z* = 0.
The positive core (0 < z < z_c) and the negative outer layer
(z_c < z < z*) cancel exactly: the slab's dark matter is a FINITE,
self-cancelling structure, not an ever-growing halo. -/
theorem slab_column_zero (A rb zc : ℝ) (hA : 0 < A) (hrb : 0 < rb)
    (hzc : 0 < zc) (hAsq : A ^ 2 = rb ^ 2 * zc) :
    ∫ (z : ℝ) in 0..4 * zc, 2 * (A * z ^ (-1 / (2:ℝ)) - rb) = 0 := by
  have hz4 : (0:ℝ) < 4 * zc := by positivity
  have key : ∫ (z : ℝ) in 0..4 * zc, (2 * A) * z ^ (-1 / (2:ℝ))
      = (2 * A) * (4 * zc) ^ (1 / (2:ℝ)) / (1 / (2:ℝ)) := by
    rw [intervalIntegral.integral_const_mul, integral_rpow (Or.inl (by norm_num : (-1:ℝ) < -1/2))]
    norm_num
    ring
  have h2 : ∫ (z : ℝ) in 0..4 * zc, (2:ℝ) * rb = 2 * rb * (4 * zc) := by
    rw [intervalIntegral.integral_const_mul, intervalIntegral.integral_const, smul_eq_mul]
    ring
  have hsplit : ∫ (z : ℝ) in 0..4 * zc, 2 * (A * z ^ (-1 / (2:ℝ)) - rb)
      = ∫ (z : ℝ) in 0..4 * zc, (2 * A) * z ^ (-1 / (2:ℝ)) - (2 * rb) := by
    congr 1
    exact funext fun z => by ring
  have hAsqrt : A * Real.sqrt zc = rb * zc := by
    have h3 : (0:ℝ) ≤ rb * zc := by positivity
    have hsq : (A * Real.sqrt zc) ^ 2 = (rb * zc) ^ 2 := by
      calc (A * Real.sqrt zc) ^ 2 = A ^ 2 * (Real.sqrt zc) ^ 2 := by ring
        _ = A ^ 2 * zc := by rw [Real.sq_sqrt hzc.le]
        _ = (rb * zc) ^ 2 := by rw [hAsq]; ring
    calc A * Real.sqrt zc = Real.sqrt ((A * Real.sqrt zc) ^ 2) :=
          (Real.sqrt_sq (by positivity)).symm
      _ = Real.sqrt ((rb * zc) ^ 2) := by rw [hsq]
      _ = rb * zc := Real.sqrt_sq h3
  have hsqrt42 : (4 * zc) ^ (1 / (2:ℝ)) = 2 * Real.sqrt zc := by
    rw [← Real.sqrt_eq_rpow, Real.sqrt_mul (by norm_num : (0:ℝ) ≤ 4) zc,
      show Real.sqrt (4:ℝ) = 2 from by norm_num]
  have hpow : (2:ℝ) * A * (2 * Real.sqrt zc) / (1 / (2:ℝ)) = 8 * (A * Real.sqrt zc) := by
    ring
  rw [hsplit, intervalIntegral.integral_sub
      (IntervalIntegrable.const_mul
        (intervalIntegrable_rpow' (by norm_num : (-1:ℝ) < -1 / (2:ℝ))) (2 * A))
      intervalIntegrable_const, key, h2, hsqrt42, hpow, hAsqrt]
  ring

/-- **peak_column.** The one-sided column integral over the positive core
[0, z_c] (z_c = (A/rho_b)^2) equals a0/(16*pi*G) exactly, given
A^2 = a0*rho_b/(16*pi*G), so the two-sided PEAK column is a0/(8*pi*G) -- the
registered 26.7 M_sun/pc^2.  The column rises from 0 to this max at z_c,
then falls and crosses zero at z* = 4*z_c (slab_column_zero). -/
theorem peak_column (A a0 G rb : ℝ) (hA : 0 < A) (ha0 : 0 < a0) (hG : 0 < G)
    (hrb : 0 < rb) (hAsq : A ^ 2 = a0 * rb / (16 * Real.pi * G)) :
    ∫ (z : ℝ) in 0..(A / rb) ^ 2, (A * z ^ (-1 / (2:ℝ)) - rb)
      = a0 / (16 * Real.pi * G) := by
  have hkey : ∫ (z : ℝ) in 0..(A / rb) ^ 2, A * z ^ (-1 / (2:ℝ))
      = A * ((A / rb) ^ 2) ^ (1 / (2:ℝ)) / (1 / (2:ℝ)) := by
    rw [intervalIntegral.integral_const_mul, integral_rpow (Or.inl (by norm_num : (-1:ℝ) < -1/2))]
    norm_num
    ring
  have h2 : ∫ (z : ℝ) in 0..(A / rb) ^ 2, rb = rb * (A / rb) ^ 2 := by
    rw [intervalIntegral.integral_const, smul_eq_mul]
    ring
  have hsplit : ∫ (z : ℝ) in 0..(A / rb) ^ 2, (A * z ^ (-1 / (2:ℝ)) - rb)
      = ∫ (z : ℝ) in 0..(A / rb) ^ 2, A * z ^ (-1 / (2:ℝ)) - rb := by
    congr 1
  have hsqrt : ((A / rb) ^ 2) ^ (1 / (2:ℝ)) = A / rb := by
    rw [← Real.sqrt_eq_rpow, Real.sqrt_sq_eq_abs, abs_of_pos (by positivity : (0:ℝ) < A / rb)]
  have hfin : (2:ℝ) * A * (A / rb) - rb * (A / rb) ^ 2 = a0 / (16 * Real.pi * G) := by
    have h1 : (2:ℝ) * A * (A / rb) - rb * (A / rb) ^ 2 = A ^ 2 / rb := by
      field_simp
      ring
    rw [h1, hAsq]
    field_simp [hrb.ne']
  rw [hsplit, intervalIntegral.integral_sub
      (IntervalIntegrable.const_mul
        (intervalIntegrable_rpow' (by norm_num : (-1:ℝ) < -1 / (2:ℝ))) A)
      intervalIntegrable_const, hkey, h2, hsqrt]
  rw [show A * (A / rb) / (1 / (2:ℝ)) = (2:ℝ) * A * (A / rb) from by ring]
  exact hfin

/-- **num_peak_column_msun (numeric anchor).** With the certified SI
constants a0 = 9.3619e-11 m/s^2 and G = 6.674e-11 m^3 kg^-1 s^-2, the peak
column a0/(8*pi*G) lies strictly between 26 and 27 solar masses per square
parsec (M_sun = 1.989e30 kg, pc = 3.0857e16 m): the registered 26.7
M_sun/pc^2. -/
theorem num_peak_column_msun :
    (26:ℝ) * 1.989e30 / (3.0857e16) ^ 2 < 9.3619e-11 / (8 * Real.pi * 6.674e-11) ∧
    9.3619e-11 / (8 * Real.pi * 6.674e-11) < 27 * 1.989e30 / (3.0857e16) ^ 2 := by
  have hden : (0:ℝ) < 8 * Real.pi * 6.674e-11 := by positivity
  have hkey : (0.0557:ℝ) < 9.3619e-11 / (8 * Real.pi * 6.674e-11) := by
    rw [lt_div_iff₀ hden]
    calc (0.0557:ℝ) * (8 * Real.pi * 6.674e-11)
        = (0.0557:ℝ) * (8 * 6.674e-11) * Real.pi := by ring
      _ ≤ (0.0557:ℝ) * (8 * 6.674e-11) * 3.1416 :=
          mul_le_mul_of_nonneg_left Real.pi_lt_d4.le
            (by norm_num : (0:ℝ) ≤ (0.0557:ℝ) * (8 * 6.674e-11))
      _ < 9.3619e-11 := by norm_num
  have hkey2 : 9.3619e-11 / (8 * Real.pi * 6.674e-11) < (0.0559:ℝ) := by
    rw [div_lt_iff₀ hden]
    calc (9.3619e-11:ℝ) < (0.0559:ℝ) * (8 * 6.674e-11) * 3.141592 := by norm_num
      _ ≤ (0.0559:ℝ) * (8 * 6.674e-11) * Real.pi :=
          mul_le_mul_of_nonneg_left (le_of_lt Real.pi_gt_d6)
            (by norm_num : (0:ℝ) ≤ (0.0559:ℝ) * (8 * 6.674e-11))
      _ = (0.0559:ℝ) * (8 * Real.pi * 6.674e-11) := by ring
  constructor
  · calc (26:ℝ) * 1.989e30 / (3.0857e16) ^ 2 < 0.0557 := by norm_num
      _ < 9.3619e-11 / (8 * Real.pi * 6.674e-11) := hkey
  · calc 9.3619e-11 / (8 * Real.pi * 6.674e-11) < 0.0559 := hkey2
      _ < 27 * 1.989e30 / (3.0857e16) ^ 2 := by norm_num

/-! ## PART 2 -- G028: the Noether-charge w-window coldness bound. -/

/-- **w_window_exponent (the coldness bound, EXPONENT level).** For the
charge dust equation of state w with 0 < w <= 5.7e-7, the density exponent
-3(1+w) differs from the cold-dust exponent -3 by exactly 3*w <= 1.71e-6,
strictly below 2e-6: the cold-dust exponent a^-3 is recovered to within
2 parts per million across the whole window. -/
theorem w_window_exponent (w : ℝ) (hw : 0 < w ∧ w ≤ 5.7e-7) :
    |(-3 : ℝ) * (1 + w) - (-3)| = 3 * w ∧ 3 * w ≤ 1.71e-6 ∧ 3 * w < 2e-6 := by
  have hx : (-3:ℝ) * (1 + w) - (-3) = -3 * w := by ring
  have h1 : |(-3 : ℝ) * (1 + w) - (-3)| = 3 * w := by
    rw [hx, abs_of_nonpos (by nlinarith : (-3:ℝ) * w ≤ 0)]
    ring
  refine ⟨h1, ?_, ?_⟩
  · nlinarith [hw.2, hw.1]
  · nlinarith [hw.1, hw.2]

/-- **w_window_cold.** The window's ceiling is deep inside the acoustic
reach: w <= 5.7e-7 < 1e-4 -- the acoustic band is reachable in existing
data; the ceiling is a theory bound. -/
theorem w_window_cold (w : ℝ) (hw : 0 < w ∧ w ≤ 5.7e-7) : w < 1e-4 := by
  nlinarith [hw.2, hw.1]

/-- **rho_vs_dust_a1 (the density comparison AT a = 1).** At the scale
factor a = 1 the charge dust density a^(-3(1+w)) agrees with cold dust
a^(-3) EXACTLY (both are 1).  HONEST SCOPE: the exponent-level bound
(w_window_exponent) is the certified G028 claim; the relative density
difference away from a = 1 grows like 3*w*|ln a| and is deliberately NOT
claimed to stay under 2e-6 at recombination. -/
theorem rho_vs_dust_a1 (w : ℝ) (_hw : 0 < w ∧ w ≤ 5.7e-7) :
    |(1 : ℝ) ^ (-3 * (1 + w)) - (1 : ℝ) ^ (-3 : ℝ)| = 0 := by
  have h1 : (1 : ℝ) ^ (-3 * (1 + w)) = 1 := Real.one_rpow _
  have h2 : (1 : ℝ) ^ (-3 : ℝ) = 1 := Real.one_rpow _
  rw [h1, h2]
  norm_num

#print axioms slab_zstar_eq_four_zc
#print axioms box_nu_extends
#print axioms rho_ph_at_saturation
#print axioms slab_column_zero
#print axioms peak_column
#print axioms num_peak_column_msun
#print axioms w_window_exponent
#print axioms w_window_cold
#print axioms rho_vs_dust_a1
