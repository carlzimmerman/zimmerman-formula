import Mathlib
import Mathlib.Tactic

/-!
# AS069 -- Dimensionless kernel parameter versus vacuum energy (Lean 4 certificate)

Framework (dimensionless; s = c*sqrt(G*rho_L), Y = g/s, a0 = kappa*s, kappa = 1/2 ADOPTED):
    MU_lambda response family:  mu_lam(Y) = 1 - (1+Y)^(-lambda),
    force law (branch MU_n at lambda = n):  mu_lam(g/s)*g = B,
    vacuum observable from the additive shift C (units a0^2, J(0)=0 convention):
        rho_vac / rho_L = alpha*C_a02/(64*pi),        alpha = 2 - K_B.

Certified content (exact algebraic/analytic identities; physical reading in
derivation.md):

  A  block_det       : det [[a, 0]; [c, d]] = a*d  (block-triangular Jacobian of
                       the observables (force, vacuum) wrt (lambda, C); d = dV/dC
                       = alpha/(64 pi) != 0 is the lower-right corner).
     col_indep      : the two columns (d/dlambda, d/dC) are linearly independent
                       iff a != 0 and d != 0 -- i.e. rank 2 exactly when the force
                       responds to lambda (dF/dlambda = a != 0); dF/dlambda = 0
                       degrades the Jacobian to rank 1 (lambda a pure label).
  B  calibr_ratio    : alpha*(64*pi/alpha)/(64*pi) = 1 : the shift that reproduces
                       rho_L is lambda-independent (pure bookkeeping/calibration).
     calibr_dimens  : with C = 64*pi*a0^2/alpha and rho_L = 4*a0^2/(G*c^2):
                       rho_vac/rho_L = 1 exactly, for ANY lambda.
  C  force_law2      : y*mu2(y) = y^2*(y+2)/(1+y)^2  (MU_2 force law in closed form)
     cubic_form     : y^2*(y+2) - q*(1+y)^2 = y^3 + (2-q)y^2 - 2*q*y - q
                       (the exact cubic inverse used as independent representation
                       of the lambda = 2 force law: mu2(g/s)*g/s = q).
  D  J2_zero, J2_deriv : primitive J2(Y) = Y - Y/(1+Y): J2(0) = 0 and
                       d/dY J2 = mu2(Y) = 1 - 1/(1+Y)^2  (the derivative fixes
                       forces; the integration constant is the free C(lambda)).
  E  kappa_of_deep   : a0 = s/lambda  =>  kappa = a0/s = 1/lambda  (deep-slope
                       identification; kappa = 1/2 <=> lambda = 2, adopted).

Notes: All statements are dimensionless; both a0 footings (9.3619e-11 and
1.1279e-10 m/s^2) apply unchanged.  The deep/Newtonian limiting statements and
the leading-correction coefficients are verified numerically (as069_audit.py,
checks E1/E2) and symbolically (sympy).  lambda = 1/2 is an algebraic probe, not
a channel count; channel counts are the integers n >= 1.
No `sorry`; axioms restricted to {propext, Classical.choice, Quot.sound}
(verified via #print axioms at the end).
-/

noncomputable section
open Real

/- A: the block-triangular Jacobian determinant (rows: F1 deep, F2 transition, V;
      cols: d/dlambda, d/dC).  The force corner dF/dC = 0 and dV/dC != 0 put the
      matrix in the form [[a, 0]; [c, d]]. -/
theorem block_det (a c d : ℝ) :
    (!![a, 0; c, d] : Matrix (Fin 2) (Fin 2) ℝ).det = a * d := by
  simp [Matrix.det_fin_two]

def col0 (a c : ℝ) : Fin 2 → ℝ := ![a, c]
def col1 (d : ℝ) : Fin 2 → ℝ := ![0, d]

theorem col_indep (a c d : ℝ) (ha : a ≠ 0) (hd : d ≠ 0) :
    LinearIndependent ℝ ![col0 a c, col1 d] := by
  rw [Fintype.linearIndependent_iff]
  intro l hl
  rw [Fin.sum_univ_two] at hl
  have hz0 : l 0 * a = 0 := by
    have hv0 := congrFun hl 0
    simpa [col0, col1, smul_eq_mul, Pi.add_apply, Pi.smul_apply] using hv0
  have hz1 : l 0 * c + l 1 * d = 0 := by
    have hv1 := congrFun hl 1
    simpa [col0, col1, smul_eq_mul, Pi.add_apply, Pi.smul_apply] using hv1
  have h0 : l 0 = 0 := (mul_eq_zero.mp hz0).resolve_right ha
  have h1 : l 1 = 0 := by
    rw [h0, zero_mul, zero_add] at hz1
    exact (mul_eq_zero.mp hz1).resolve_right hd
  intro i
  fin_cases i <;> simp [h0, h1]

theorem col_dep (a c d : ℝ) (ha : a = 0) (hd : d ≠ 0) :
    ¬ LinearIndependent ℝ ![col0 a c, col1 d] := by
  rw [Fintype.linearIndependent_iff]
  intro h
  let g : Fin 2 → ℝ := ![d, -c]
  have hsum : (∑ i, g i • ![col0 a c, col1 d] i) = 0 := by
    rw [Fin.sum_univ_two]
    ext j
    fin_cases j
    · simp [g, col0, col1, ha, smul_eq_mul, Pi.add_apply]
    · simp [g, col0, col1, ha, smul_eq_mul, Pi.add_apply]
      ring
  have hg : ∀ i : Fin 2, g i = 0 := h g hsum
  have hg0 : g 0 = 0 := hg 0
  have : d = 0 := by simpa [g] using hg0
  exact hd this

/- B: calibration algebra -- the shift that reproduces rho_L is lambda-independent
      by construction: identifying rho_vac with rho_L is bookkeeping, not a
      derivation of kappa.  (Dimensionless ratio; alpha = 2 - K_B nonzero.) -/
theorem calibr_ratio (alpha : ℝ) (ha : alpha ≠ 0) :
    (alpha * (64 * Real.pi / alpha)) / (64 * Real.pi) = 1 := by
  field_simp [ha, Real.pi_ne_zero]

theorem calibr_dimens (alpha a0 G c : ℝ) (ha : alpha ≠ 0) (ha0 : a0 ≠ 0)
    (hG : G ≠ 0) (hc : c ≠ 0) :
    (alpha * (64 * Real.pi * a0 ^ 2 / alpha)) / (16 * Real.pi * G * c ^ 2)
      / ((4 * a0 ^ 2) / (G * c ^ 2)) = 1 := by
  field_simp [ha, ha0, hG, hc, Real.pi_ne_zero]
  norm_num

/- C: the MU_2 force law -- closed algebraic form and the exact cubic inverse
      representation used as the independent numerical check. -/
def mu2 (Y : ℝ) : ℝ := 1 - 1 / (1 + Y) ^ 2

theorem force_law2 (y : ℝ) (hy : 1 + y ≠ 0) :
    y * mu2 y = y ^ 2 * (y + 2) / (1 + y) ^ 2 := by
  unfold mu2
  field_simp [hy]
  ring

theorem cubic_form (y q : ℝ) :
    y ^ 2 * (y + 2) - q * (1 + y) ^ 2 = y ^ 3 + (2 - q) * y ^ 2 - 2 * q * y - q := by
  ring

/- D: the lambda = 2 primitive of the family (J(0) = 0 convention shown; the
      nonzero integration constants of other antiderivatives are absorbed into
      the free C(lambda)). -/
def J2 (Y : ℝ) : ℝ := Y - Y / (1 + Y)

theorem J2_zero : J2 0 = 0 := by
  simp [J2]

theorem J2_deriv (Y : ℝ) (hY : 1 + Y ≠ 0) :
    deriv J2 Y = mu2 Y := by
  unfold J2 mu2
  have hdiv : deriv (fun t : ℝ => t / (1 + t)) Y = 1 / (1 + Y) ^ 2 := by
    have hd1 : DifferentiableAt ℝ (fun t : ℝ => t) Y := by fun_prop
    have hd2 : DifferentiableAt ℝ (fun t : ℝ => 1 + t) Y := by fun_prop
    change deriv ((fun t : ℝ => t) / (fun t : ℝ => 1 + t)) Y = 1 / (1 + Y) ^ 2
    rw [deriv_div hd1 hd2 (by simpa using hY)]
    rw [deriv_id'']
    rw [deriv_const_add_id 1]
    ring
  calc
    deriv (fun t : ℝ => t - t / (1 + t)) Y
        = deriv (fun t : ℝ => t) Y - deriv (fun t : ℝ => t / (1 + t)) Y := by
          exact deriv_sub (by fun_prop) (by fun_prop)
    _ = 1 - 1 / (1 + Y) ^ 2 := by
          change deriv id Y - deriv (fun t : ℝ => t / (1 + t)) Y = 1 - 1 / (1 + Y) ^ 2
          rw [deriv_id, hdiv]

/- E: the deep-slope identification: mu ~ lambda*Y with mu*g = B gives g^2 =
      (s/lambda)*B, i.e. a0 = s/lambda and kappa = a0/s = 1/lambda. -/
theorem kappa_of_deep (a0 s lam : ℝ) (hlam : lam ≠ 0) (hs : s ≠ 0)
    (h : a0 = s / lam) : a0 / s = 1 / lam := by
  rw [h]
  field_simp [hlam, hs]

end

-- Print axioms (unfiltered) -- the certificate is clean iff every listed name
-- depends only on the allowed set {propext, Classical.choice, Quot.sound}.
#print axioms block_det
#print axioms col_indep
#print axioms col_dep
#print axioms calibr_ratio
#print axioms calibr_dimens
#print axioms force_law2
#print axioms cubic_form
#print axioms J2_zero
#print axioms J2_deriv
#print axioms kappa_of_deep
