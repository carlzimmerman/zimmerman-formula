import Mathlib

/-!
# AS070 — constraint-coupling algebra certificates

Certifies the algebraic core of the AS070 analysis (run_20260928T115333_06b0):

  F = 4*a0^2 - G*c^2*rho_L  (constraint candidate, units m^2 s^-4)
  lambda = rho_L / rho_Lambda,  rho_Lambda = 4*a0^2/(G*c^2)   (adopted framework footing)
  kappa = a0 / (c * sqrt(G*rho_L))                            (candidate coefficient reading)

  T1  F = 0  <->  lambda = 1   (the constraint IS the adopted kappa=1/2 normalization)
  T1' F = 0  <->  rho_L = 4*a0^2/(G*c^2)
  T1''F = 4*a0^2*(1 - lambda)  (exact factor form used by all diagnostics)
  T2  s = c*sqrt(G*rho_L) = 2*a0*sqrt(lambda)                  (MU_n scale identity)
  T3  kappa^2 = 1/(4*lambda);  F=0 (rho_L>0,a0>0,c>0,G>0) -> kappa = 1/2
  T4  mu2(rational form): (1+Y)^2 * (1 - (1+Y)^(-2)) = Y*(Y+2)
  T5  MU2 cell mapping: the Y = g/(2a0) form equals the (g/a0)/2 form (framework cell at lambda=1)

Zero sorry. Axioms of each declared theorem are printed at the bottom (expect
{propext, Classical.choice, Quot.sound}).
-/

noncomputable section

namespace AS070

open Real

variable (a0 G c rho_L g Y : ℝ)

def lambdaOf (a0 G c rho_L : ℝ) : ℝ := G * c ^ 2 * rho_L / (4 * a0 ^ 2)

def kappaOf (a0 G c rho_L : ℝ) : ℝ := a0 / (c * Real.sqrt (G * rho_L))

def mu2 (Y : ℝ) : ℝ := 1 - ((1 + Y) ^ 2)⁻¹

-- T1'':  F = 4*a0^2*(1 - lambda)  (exact factor identity)
theorem f_eq_four_a0sq_one_sub_lambda (ha : a0 ≠ 0) :
    4 * a0 ^ 2 - G * c ^ 2 * rho_L = 4 * a0 ^ 2 * (1 - lambdaOf a0 G c rho_L) := by
  unfold lambdaOf
  field_simp [ha]

-- T1:  F = 0  <->  lambda = 1
theorem f_iff_lambda_eq_one (hG : G ≠ 0) (hc : c ≠ 0) (ha : a0 ≠ 0) :
    4 * a0 ^ 2 - G * c ^ 2 * rho_L = 0 ↔ lambdaOf a0 G c rho_L = 1 := by
  constructor
  · intro h
    unfold lambdaOf
    have h' : G * c ^ 2 * rho_L = 4 * a0 ^ 2 := by nlinarith
    rw [h']
    have h4 : 4 * a0 ^ 2 ≠ 0 := by positivity
    exact div_self h4
  · intro h
    have h' : G * c ^ 2 * rho_L = 4 * a0 ^ 2 := by
      unfold lambdaOf at h
      have h4 : 4 * a0 ^ 2 ≠ 0 := by positivity
      calc
        G * c ^ 2 * rho_L = 4 * a0 ^ 2 * (G * c ^ 2 * rho_L / (4 * a0 ^ 2)) := by field_simp [h4]
        _ = 4 * a0 ^ 2 * 1 := by rw [h]
        _ = 4 * a0 ^ 2 := by ring
    nlinarith

-- T1':  F = 0  <->  rho_L = 4*a0^2/(G*c^2)
theorem f_iff_rho_framework (hG : G ≠ 0) (hc : c ≠ 0) :
    4 * a0 ^ 2 - G * c ^ 2 * rho_L = 0 ↔ rho_L = 4 * a0 ^ 2 / (G * c ^ 2) := by
  constructor
  · intro h
    have h' : G * c ^ 2 * rho_L = 4 * a0 ^ 2 := by nlinarith
    calc
      rho_L = (G * c ^ 2 * rho_L) / (G * c ^ 2) := by field_simp [hG, hc]
      _ = (4 * a0 ^ 2) / (G * c ^ 2) := by rw [h']
  · intro h
    rw [h]
    field_simp [hG, hc]
    ring

-- T2:  s = c*sqrt(G*rho_L) = 2*a0*sqrt(lambda)
theorem s_two_a0_sqrt_lambda (hG : 0 < G) (hc : 0 < c) (ha : 0 < a0)
    (hr : 0 ≤ rho_L) :
    c * Real.sqrt (G * rho_L) = 2 * a0 * Real.sqrt (lambdaOf a0 G c rho_L) := by
  have hs1 : c * Real.sqrt (G * rho_L) = Real.sqrt (c ^ 2 * (G * rho_L)) := by
    rw [Real.sqrt_mul (sq_nonneg c)]
    rw [Real.sqrt_sq_eq_abs, abs_of_nonneg (le_of_lt hc)]
  have h2 : c ^ 2 * (G * rho_L) = 4 * a0 ^ 2 * lambdaOf a0 G c rho_L := by
    unfold lambdaOf
    have ha' : 4 * a0 ^ 2 ≠ 0 := by positivity
    field_simp [ha']
  have hsq : Real.sqrt ((2 * a0) ^ 2) = 2 * a0 := by
    rw [Real.sqrt_sq_eq_abs]
    rw [abs_of_nonneg]
    positivity
  have hsqmul : Real.sqrt (4 * a0 ^ 2 * lambdaOf a0 G c rho_L) =
      Real.sqrt ((2 * a0) ^ 2) * Real.sqrt (lambdaOf a0 G c rho_L) := by
    rw [show 4 * a0 ^ 2 = (2 * a0) ^ 2 by ring]
    exact Real.sqrt_mul (sq_nonneg (2 * a0)) (lambdaOf a0 G c rho_L)
  calc
    c * Real.sqrt (G * rho_L) = Real.sqrt (c ^ 2 * (G * rho_L)) := hs1
    _ = Real.sqrt (4 * a0 ^ 2 * lambdaOf a0 G c rho_L) := by rw [h2]
    _ = Real.sqrt ((2 * a0) ^ 2) * Real.sqrt (lambdaOf a0 G c rho_L) := hsqmul
    _ = 2 * a0 * Real.sqrt (lambdaOf a0 G c rho_L) := by rw [hsq]

-- T3a:  kappa^2 = 1/(4*lambda)
theorem kappa_sq_inv_four_lambda (hG : 0 < G) (hc : 0 < c) (ha : 0 < a0)
    (hr : 0 ≤ rho_L) (hl : 0 < lambdaOf a0 G c rho_L) :
    (kappaOf a0 G c rho_L) ^ 2 = (1 / 4) / lambdaOf a0 G c rho_L := by
  have hs := s_two_a0_sqrt_lambda a0 G c rho_L hG hc ha hr
  unfold kappaOf
  calc
    (a0 / (c * Real.sqrt (G * rho_L))) ^ 2 = (a0 / (2 * a0 * Real.sqrt (lambdaOf a0 G c rho_L))) ^ 2 := by
      rw [hs]
    _ = (1 / 4) / lambdaOf a0 G c rho_L := by
      field_simp [ne_of_gt ha, ne_of_gt hl]
      nlinarith [Real.sq_sqrt (le_of_lt hl)]

-- T3b:  F = 0 (+ positivity)  ->  kappa = 1/2   (the constraint IS the adopted normalization)
theorem kappa_half_of_constraint (hG : 0 < G) (hc : 0 < c) (ha : 0 < a0)
    (hr : 0 < rho_L) (hF : 4 * a0 ^ 2 - G * c ^ 2 * rho_L = 0) :
    kappaOf a0 G c rho_L = 1 / 2 := by
  have hmain : c * Real.sqrt (G * rho_L) = 2 * a0 := by
    have hG' : G ≠ 0 := ne_of_gt hG
    have hc' : c ≠ 0 := ne_of_gt hc
    have ha' : a0 ≠ 0 := ne_of_gt ha
    have hlam : lambdaOf a0 G c rho_L = 1 := (f_iff_lambda_eq_one a0 G c rho_L hG' hc' ha').1 hF
    have hs := s_two_a0_sqrt_lambda a0 G c rho_L hG hc ha (le_of_lt hr)
    calc
      c * Real.sqrt (G * rho_L) = 2 * a0 * Real.sqrt (lambdaOf a0 G c rho_L) := hs
      _ = 2 * a0 * 1 := by rw [hlam]; simp
      _ = 2 * a0 := by ring
  unfold kappaOf
  rw [hmain]
  field_simp [ne_of_gt ha]

-- T4:  mu2 rational form:  (1+Y)^2 * mu2(Y) = Y*(Y+2)   [1+Y != 0]
theorem mu2_rational_form (Y : ℝ) (hY : 1 + Y ≠ 0) :
    (1 + Y) ^ 2 * mu2 Y = Y * (Y + 2) := by
  unfold mu2
  calc
    (1 + Y) ^ 2 * (1 - ((1 + Y) ^ 2)⁻¹) = (1 + Y) ^ 2 - 1 := by
      field_simp [hY]
    _ = Y * (Y + 2) := by ring

-- T5:  MU2 cell mapping at lambda = 1:  mu2(g/(2a0)) = 1 - (1 + (g/a0)/2)^(-2)
theorem mu2_framework_mapping (ha : a0 ≠ 0) :
    mu2 (g / (2 * a0)) = 1 - ((1 + (g / a0) / 2) ^ 2)⁻¹ := by
  unfold mu2
  congr 1
  congr 1
  field_simp [ha]

-- T5b:  the lambda = 1 argument reduction g/(2*a0*sqrt(1)) = g/(2*a0)
theorem mu2_lambda_one_argument (ha : a0 ≠ 0) :
    mu2 (g / (2 * a0 * Real.sqrt 1)) = mu2 (g / (2 * a0)) := by
  unfold mu2
  congr 1
  congr 1
  rw [Real.sqrt_one]
  field_simp [ha]

end AS070

-- axiom audit (unfiltered)
#print axioms AS070.f_eq_four_a0sq_one_sub_lambda
#print axioms AS070.f_iff_lambda_eq_one
#print axioms AS070.f_iff_rho_framework
#print axioms AS070.s_two_a0_sqrt_lambda
#print axioms AS070.kappa_sq_inv_four_lambda
#print axioms AS070.kappa_half_of_constraint
#print axioms AS070.mu2_rational_form
#print axioms AS070.mu2_framework_mapping
#print axioms AS070.mu2_lambda_one_argument
