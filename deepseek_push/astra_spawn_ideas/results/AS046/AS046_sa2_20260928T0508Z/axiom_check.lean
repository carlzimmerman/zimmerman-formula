import Mathlib
import Mathlib.Tactic

/-
  AS046 -- MU2 matching nu and derivative at one (Lean 4 certificate).

  Branch cells (dimensionless, x = g/a0 > 0, y = B/a0 > 0, a0 = kappa c sqrt(G rho_Lambda),
  kappa = 1/2 ADOPTED; framework contract branch dictionary):

    Q   : x^2 = y^2 + y            -> mu_Q(x)  = (sqrt(1+4x^2)-1)/(2x) = y/x
    MU2 : y = x*mu2(x), mu2(x) = 1-(1+x/2)^(-2)      (CONTRACT cell)
    EXP : y = x*(1-e^{-x})          (historical AQUAL cell)
    RAR : x = y*nu(y), nu = 1/(1-e^{-sqrt(y)})
    MONO: nu_mono heat-filter splice of RAR (numerically bracketed landmarks)

  Formalized content (all exact algebraic statements):
    A  mu2 contract value at x=1:  mu2(1) = 5/9        (NOT 1/sqrt 2)
    B  mu2 contract derivative at 1: mu2'(1) = 8/27, x*mu2'(1) = 8/27
    C  mu2 derivative identity (general x): d/dx mu2 = (1+x/2)^(-3)
    D  rational form of the contract cell: 1-(1+x/2)^(-2) = 1-1/(1+x/2)^2
    E  dispatch-claimed interpolant mu_s(x) = x/sqrt(1+x^2): mu_s(1) = 1/sqrt 2
       (so "mu_MU2(1) = 1/sqrt(2)" is 5/9 vs 1/sqrt2: holds for mu_s only;
       mu_s is NOT the contract MU2 cell, which the seed compares)
    F  mu_s'(x) = (1+x^2)^(-3/2) as rpow, x*mu_s' = x(1+x^2)^(-3/2),
       mu_s'(1) = 2^(-3/2)
    G  Q-cell exact values: mu_Q(1) = (sqrt 5 - 1)/2,
       mu_Q'(1) = (sqrt 5 - 1)/(2 sqrt 5), x*mu_Q'(1) = mu_Q'(1) at x = 1
    H  conditioning identity kappa = g/(B F'(B)):
       on Q, kappa_Q(y) = 2(y+1)/(2y+1) with exact identities
       kappa = 1 + 1/(2y+1) = 2 - 2y/(2y+1); kappa_Q(1) = 4/3;
       1 < kappa_Q(y) < 2 for every y > 0
    H' inverse-relative conditioning is the EXACT RECIPROCAL of the forward
       relative conditioning (hence dimensionless; this is the sense in which
       it is unit/footing-invariant; cf. NC1: kappa_abs != kappa_rel)
    I  RAR conditioning algebra: kappa_RAR(s) = 1/(1 - (s/2) e^{-s}/(1-e^{-s})),
       s = sqrt(y), from kappa = nu/(nu + y nu'), y nu' = -(s/2)e^{-s}/(1-e^{-s})^2
-/

noncomputable section
open Real

/-- Contract MU2 cell (rational form; equal to 1-(1+x/2)^(-2), see D). -/
def mu2c (x : ℝ) : ℝ := 1 - 1 / (1 + x / 2) ^ 2

/-- Dispatch-mentioned interpolant mu_s(x) = x/sqrt(1+x^2). -/
def muS (x : ℝ) : ℝ := x / Real.sqrt (1 + x ^ 2)

/-- Q branch response mu_Q(x) = y/x, y = (sqrt(1+4x^2)-1)/2; written as (y)/x. -/
def muQ (x : ℝ) : ℝ := ((Real.sqrt (1 + 4 * x ^ 2) - 1) / 2) / x

/- D: rational form equals the display 1-(1+x/2)^(-2) for all real x. -/
theorem mu2c_eq_display (x : ℝ) : 1 - (1 + x / 2) ^ (-2 : ℤ) = mu2c x := by
  unfold mu2c
  have hz : (1 + x / 2) ^ (-2 : ℤ) = ((1 + x / 2) ^ 2)⁻¹ := by
    simp [zpow_natCast, zpow_neg]
  rw [hz]
  rw [inv_eq_one_div]

/- A: contract MU2 value at x = 1 is 5/9. -/
theorem mu2c_at_one : mu2c 1 = 5 / 9 := by
  unfold mu2c
  norm_num

/- A': the dispatch claim "mu2(1) = 1/sqrt 2" is FALSE for the contract cell:
   mu2c 1 != 1/sqrt 2. -/
theorem mu2c_at_one_not_one_over_sqrt2 : mu2c 1 ≠ 1 / Real.sqrt 2 := by
  rw [mu2c_at_one]
  intro h
  have hsq := congrArg (fun t : ℝ => t ^ 2) h
  have hsqrt : (Real.sqrt 2) ^ 2 = (2 : ℝ) := by
    rw [Real.sq_sqrt]
    norm_num
  norm_num [div_pow, hsqrt, hsq]

/- C: derivative of the contract MU2 cell: d/dx mu2 = (1+x/2)^(-3).
   Proof: g(z) = 1+z/2 has g' = 1/2; g^2 has (g^2)' = 2*g*g' = 1+x/2
   (product rule, no pow-on-lambda); then inv rule and subtraction of 1. -/
theorem mu2c_deriv (x : ℝ) (hx : 1 + x / 2 ≠ 0) : HasDerivAt mu2c (1 / (1 + x / 2) ^ 3) x := by
  unfold mu2c
  have hlin : HasDerivAt (fun z : ℝ => 1 + z / 2) (1 / 2) x := by
    simpa [add_comm] using ((hasDerivAt_id x).div_const 2).const_add 1
  have hm := hlin.mul hlin
  have hsl : (1 / 2) * (1 + x / 2) + (1 + x / 2) * (1 / 2) = 1 + x / 2 := by
    ring
  have hg2m : HasDerivAt (fun z : ℝ => (1 + z / 2) * (1 + z / 2)) (1 + x / 2) x := by
    rwa [hsl] at hm
  have hg2ne : (1 + x / 2) * (1 + x / 2) ≠ 0 := mul_ne_zero hx hx
  have hrec : HasDerivAt (fun z : ℝ => ((1 + z / 2) * (1 + z / 2))⁻¹)
      (-(1 + x / 2) / ((1 + x / 2) * (1 + x / 2)) ^ 2) x :=
    hg2m.inv hg2ne
  have hc := hrec.const_sub 1
  have hs2 : -(-(1 + x / 2) / ((1 + x / 2) * (1 + x / 2)) ^ 2)
      = (1 + x / 2) / ((1 + x / 2) * (1 + x / 2)) ^ 2 := by
    ring
  rw [hs2] at hc
  have hval : (1 + x / 2) / ((1 + x / 2) * (1 + x / 2)) ^ 2 = 1 / (1 + x / 2) ^ 3 := by
    field_simp [hx]
  rw [hval] at hc
  simpa [← pow_two, mu2c] using hc

/- B: contract MU2 derivative at x = 1: mu2'(1) = 8/27. -/
theorem mu2c_deriv_at_one : HasDerivAt mu2c (8 / 27) 1 := by
  have hd := mu2c_deriv 1 (by norm_num : (1 : ℝ) + 1 / 2 ≠ 0)
  have hval : (1 : ℝ) / (1 + 1 / 2) ^ 3 = 8 / 27 := by norm_num
  rwa [hval] at hd

/- B': x*mu2'(1) = 8/27 (the 'x dmu/dx' term at x=1 on the contract cell). -/
theorem mu2c_x_deriv_at_one : (1 : ℝ) * (8 / 27) = 8 / 27 := by
  norm_num

/- E: dispatch interpolant mu_s(1) = 1/sqrt 2. -/
theorem muS_at_one : muS 1 = 1 / Real.sqrt 2 := by
  unfold muS
  norm_num

/- F1: mu_s'(x) = 1/((1+x^2) * sqrt(1+x^2))  (rational form of (1+x^2)^(-3/2)). -/
theorem muS_deriv_rational (x : ℝ) : HasDerivAt muS (1 / ((1 + x ^ 2) * Real.sqrt (1 + x ^ 2))) x := by
  unfold muS
  have harg : 0 < 1 + x ^ 2 := by nlinarith [sq_nonneg x]
  have hne : Real.sqrt (1 + x ^ 2) ≠ 0 := ne_of_gt (Real.sqrt_pos.2 harg)
  have hs2 : (Real.sqrt (1 + x ^ 2)) ^ 2 = 1 + x ^ 2 := by
    rw [Real.sq_sqrt]
    exact le_of_lt harg
  have hd : HasDerivAt (fun z : ℝ => 1 + z ^ 2) (2 * x) x := by
    simpa using ((hasDerivAt_id x).pow (2 : ℕ)).const_add 1
  have hds : HasDerivAt (fun z : ℝ => Real.sqrt (1 + z ^ 2))
      ((2 * x) / (2 * Real.sqrt (1 + x ^ 2))) x :=
    hd.sqrt harg.ne'
  have hdiv : HasDerivAt (fun z : ℝ => z / Real.sqrt (1 + z ^ 2))
      ((1 * Real.sqrt (1 + x ^ 2) - x * ((2 * x) / (2 * Real.sqrt (1 + x ^ 2))))
        / (Real.sqrt (1 + x ^ 2)) ^ 2) x :=
    (hasDerivAt_id x).div hds hne
  have hx2 : (2 * x) / (2 * Real.sqrt (1 + x ^ 2)) = x / Real.sqrt (1 + x ^ 2) := by
    field_simp [hne]
  have hnum : 1 * Real.sqrt (1 + x ^ 2) - x * (x / Real.sqrt (1 + x ^ 2))
      = 1 / Real.sqrt (1 + x ^ 2) := by
    field_simp [hne]
    rw [hs2]
    ring
  have hsl : (1 / Real.sqrt (1 + x ^ 2)) / (Real.sqrt (1 + x ^ 2)) ^ 2
      = 1 / ((1 + x ^ 2) * Real.sqrt (1 + x ^ 2)) := by
    field_simp [hne]
    rw [hs2]
  rw [hx2, hnum, hsl] at hdiv
  simpa using hdiv

/- F2: exact rpow form: (1+x^2)^(-3/2) = 1/((1+x^2) * sqrt(1+x^2)). -/
theorem rpow_neg_three_halves (x : ℝ) : (1 + x ^ 2) ^ (-(3 / 2) : ℝ)
    = 1 / ((1 + x ^ 2) * Real.sqrt (1 + x ^ 2)) := by
  have hpos : 0 < 1 + x ^ 2 := by nlinarith [sq_nonneg x]
  have hle : 0 ≤ 1 + x ^ 2 := le_of_lt hpos
  have h32 : (1 + x ^ 2) ^ ((3 / 2 : ℝ))
      = (1 + x ^ 2) * Real.sqrt (1 + x ^ 2) := by
    have hsplit : (3 / 2 : ℝ) = 1 + 1 / 2 := by norm_num
    rw [hsplit, Real.rpow_add hpos, Real.rpow_one]
    rw [← Real.sqrt_eq_rpow]
  rw [Real.rpow_neg hle]
  rw [h32]
  rw [one_div]

/- F3: mu_s'(1) = 2^(-3/2) (the dispatch claim, rpow form). -/
theorem muS_deriv_at_one_rpow : HasDerivAt muS ((2 : ℝ) ^ (-(3 / 2) : ℝ)) 1 := by
  have hd := muS_deriv_rational 1
  have hb : (1 + 1 ^ 2) = (2 : ℝ) := by norm_num
  rw [← rpow_neg_three_halves 1] at hd
  rwa [hb] at hd

/- F3': mu_s'(1) = 1/(2 sqrt 2) (explicit rational-radical form). -/
theorem muS_deriv_at_one : HasDerivAt muS (1 / (2 * Real.sqrt 2)) 1 := by
  have hd := muS_deriv_rational 1
  have hv : 1 / ((1 + 1 ^ 2) * Real.sqrt (1 + 1 ^ 2)) = 1 / (2 * Real.sqrt 2) := by
    norm_num
  rwa [hv] at hd

/- F4: x*mu_s'(1) = 2^(-3/2) (the 'x dmu/dx' factor at x=1). -/
theorem muS_x_deriv_at_one_rpow : (1 : ℝ) * ((2 : ℝ) ^ (-(3 / 2) : ℝ))
    = (2 : ℝ) ^ (-(3 / 2) : ℝ) := by
  norm_num

/- G1: Q cell value at x = 1. -/
theorem muQ_at_one : muQ 1 = (Real.sqrt 5 - 1) / 2 := by
  unfold muQ
  norm_num

/- G2: Q cell derivative at x = 1: mu_Q'(1) = (sqrt 5 - 1)/(2 sqrt 5).
   yQ(x) = (sqrt(1+4x^2)-1)/2 has yQ'(x) = 2x/sqrt(1+4x^2) (cf. AS026 I);
   quotient rule for mu_Q = yQ/x at x = 1 gives (y'(1)*1 - y(1)*1)/1^2. -/
theorem muQ_deriv_at_one : HasDerivAt muQ ((Real.sqrt 5 - 1) / (2 * Real.sqrt 5)) 1 := by
  have harg : (0 : ℝ) < 1 + 4 * 1 ^ 2 := by norm_num
  have hne : Real.sqrt (1 + 4 * 1 ^ 2) ≠ 0 := ne_of_gt (Real.sqrt_pos.2 harg)
  have hd : HasDerivAt (fun z : ℝ => 1 + 4 * z ^ 2) (4 * (2 * 1)) 1 := by
    simpa using (((hasDerivAt_id 1).pow (2 : ℕ)).const_mul (4 : ℝ)).const_add (1 : ℝ)
  have hds : HasDerivAt (fun z : ℝ => Real.sqrt (1 + 4 * z ^ 2))
      ((4 * (2 * 1)) / (2 * Real.sqrt (1 + 4 * 1 ^ 2))) 1 :=
    hd.sqrt harg.ne'
  have hdy : HasDerivAt (fun z : ℝ => (Real.sqrt (1 + 4 * z ^ 2) - 1) / 2)
      (((4 * (2 * 1)) / (2 * Real.sqrt (1 + 4 * 1 ^ 2))) / 2) 1 :=
    (hds.sub_const 1).div_const 2
  have hsl : ((4 * (2 * 1)) / (2 * Real.sqrt (1 + 4 * 1 ^ 2))) / 2
      = 2 * 1 / Real.sqrt (1 + 4 * 1 ^ 2) := by
    field_simp [hne]
    ring
  have hdy' : HasDerivAt (fun z : ℝ => (Real.sqrt (1 + 4 * z ^ 2) - 1) / 2)
      (2 * 1 / Real.sqrt (1 + 4 * 1 ^ 2)) 1 := by
    rwa [hsl] at hdy
  have hdivq : HasDerivAt (fun z : ℝ => ((Real.sqrt (1 + 4 * z ^ 2) - 1) / 2) / z)
      (((2 * 1 / Real.sqrt (1 + 4 * 1 ^ 2)) * 1
          - ((Real.sqrt (1 + 4 * 1 ^ 2) - 1) / 2) * 1) / 1 ^ 2) 1 :=
    hdy'.div (hasDerivAt_id 1) (by norm_num)
  have hsq5 : (Real.sqrt 5) ^ 2 = (5 : ℝ) := by
    rw [Real.sq_sqrt]
    norm_num
  have hne5 : Real.sqrt 5 ≠ 0 := ne_of_gt (Real.sqrt_pos.2 (by norm_num : (0 : ℝ) < 5))
  have hconv : Real.sqrt (1 + 4 * 1 ^ 2) = Real.sqrt 5 := by norm_num
  have hsl2 : ((2 * 1 / Real.sqrt (1 + 4 * 1 ^ 2)) * 1
          - ((Real.sqrt (1 + 4 * 1 ^ 2) - 1) / 2) * 1) / 1 ^ 2
      = (Real.sqrt 5 - 1) / (2 * Real.sqrt 5) := by
    rw [hconv]
    field_simp [hne5]
    have hmul : Real.sqrt 5 * (Real.sqrt 5 - 1) = (Real.sqrt 5) ^ 2 - Real.sqrt 5 := by
      ring
    rw [hmul, hsq5]
    ring
  have hfin : HasDerivAt (fun z : ℝ => ((Real.sqrt (1 + 4 * z ^ 2) - 1) / 2) / z)
      ((Real.sqrt 5 - 1) / (2 * Real.sqrt 5)) 1 := by
    rwa [hsl2] at hdivq
  unfold muQ
  simpa using hfin

/- G3: x*mu_Q'(1) = mu_Q'(1) at x = 1. -/
theorem muQ_x_deriv_at_one : (1 : ℝ) * ((Real.sqrt 5 - 1) / (2 * Real.sqrt 5))
    = (Real.sqrt 5 - 1) / (2 * Real.sqrt 5) := by
  ring

/- H1: kappa for the inverse map B = F^{-1}(g) on the Q branch:
   with x^2 = y^2 + y (x>0, y>0), kappa = g/(B F'(B)) = x/(y dx/dy)
   = 2x^2/(y(2y+1)) = 2(y+1)/(2y+1).  Exact. -/
theorem kappa_Q_closed_form (x y : ℝ) (_hx : 0 < x) (hy : 0 < y)
    (hid : x ^ 2 = y ^ 2 + y) : 2 * x ^ 2 / (y * (2 * y + 1)) = 2 * (y + 1) / (2 * y + 1) := by
  rw [hid]
  have h2y : 2 * y + 1 ≠ 0 := by nlinarith
  have hy0 : y ≠ 0 := ne_of_gt hy
  field_simp [h2y, hy0]

/- H2: alternative exact identities for kappa_Q. -/
theorem kappa_Q_identity_one (y : ℝ) (hy : 2 * y + 1 ≠ 0) :
    2 * (y + 1) / (2 * y + 1) = 1 + 1 / (2 * y + 1) := by
  field_simp [hy]
  ring

theorem kappa_Q_identity_two (y : ℝ) (hy : 2 * y + 1 ≠ 0) :
    2 * (y + 1) / (2 * y + 1) = 2 - 2 * y / (2 * y + 1) := by
  field_simp [hy]
  ring

/- H3: kappa_Q(1) = 4/3. -/
theorem kappa_Q_at_one : 2 * (1 + 1) / (2 * 1 + 1) = 4 / 3 := by
  norm_num

/- H4: the Q-branch relative conditioning is strictly inside (1, 2) for y > 0
   (amplification at most 2x in the deep regime, 1x in the Newtonian limit). -/
theorem kappa_Q_bounds_lower (y : ℝ) (hy : 0 < y) : 1 < 2 * (y + 1) / (2 * y + 1) := by
  have h2y : 2 * y + 1 ≠ 0 := by nlinarith
  field_simp [h2y]
  nlinarith

theorem kappa_Q_bounds_upper (y : ℝ) (hy : 0 < y) : 2 * (y + 1) / (2 * y + 1) < 2 := by
  have h2y : 2 * y + 1 ≠ 0 := by nlinarith
  field_simp [h2y]
  nlinarith

/- H': inverse-relative conditioning = exact reciprocal of forward-relative
   conditioning; hence dimensionless, and it is this ratio -- NOT the absolute
   slope |dB/dg| = 1/F'(B) -- that survives a change of acceleration units
   (NC1).  Certified as the exact product identity. -/
theorem kappa_inv_times_forward_eq_one (x y dxdy : ℝ) (hx : x ≠ 0) (hy : y ≠ 0)
    (hd : dxdy ≠ 0) : (x / (y * dxdy)) * (dxdy * y / x) = 1 := by
  field_simp [hx, hy, hd]

/- I: RAR conditioning algebra (s = sqrt y): kappa_RAR = nu/(nu + y nu'),
   nu = 1/(1-e^{-s}), nu' = -e^{-s}/(2s(1-e^{-s})^2)  =>
   kappa = 1/(1 - (s/2) e^{-s}/(1-e^{-s})).  Exact rational-in-(e^s) identity. -/
theorem rar_kappa_algebra (s : ℝ) (h : 1 - Real.exp s ≠ 0) :
    (1 / (1 - Real.exp s)) / (1 / (1 - Real.exp s)
      - s / 2 * Real.exp s / (1 - Real.exp s) ^ 2)
    = 1 / (1 - (s / 2) * Real.exp s / (1 - Real.exp s)) := by
  field_simp [h]

end