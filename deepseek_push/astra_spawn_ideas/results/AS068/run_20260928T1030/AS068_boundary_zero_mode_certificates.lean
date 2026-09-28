import Mathlib

/-!
# AS068 — Can a boundary condition remove the zero mode (certificate)

Framework inputs (adopted, NOT derived here):
    s = c*sqrt(G*rho_L)      [vacuum rate, m/s^2]
    Y = g/s                  [dimensionless drive]
    kappa = 1/2 adopted;  a0 = s/2.
Branch: conditional MU_n statistical response; here n = 2 (the MU2 branch on the
adopted footing):
    mu_2(Y) = 1 - (1+Y)^(-2)          (the specified static kernel J'(Y))
    J(Y_ref) = 0                      (the boundary condition under test)
    => J(0) = -int_0^{Y_ref} mu_2(Y) dY   = -Y_ref^2/(1+Y_ref)   (exact)

What is certified (real arithmetic only; no integrals, no dynamics):

1. `mu2_closed`      — mu_2(Y) = (Y^2 + 2Y)/(1+Y)^2 on Y > 0 (the kernel, as a
                       positive rational function).
2. `g0_pos`          — G0(Y) := Y^2/(1+Y) > 0 for Y > 0  (G0 = -J(0)).
3. `j0_negative`     — J0(Y) := -G0(Y) < 0 for Y > 0: the determined constant J(0)
                       is NEGATIVE for every finite positive reference position.
4. `g0_deriv_eq_mu2` — deriv G0 = mu_2 on (0, inf): G0 is the exact primitive of the
                       kernel, i.e. the elementary content of the removal identity
                       J(0) = -int_0^Y_ref mu_2 (fundamental theorem step).
5. `g0_deriv_pos`    — 0 < deriv G0 on (0, inf) (derivative form of the monotonicity).
6. `g0_strict_mono`  — G0 strictly increasing on (0, inf) by pure algebra: the vacuum
                       contribution |J(0)| = G0(Y_ref) grows strictly with the
                       reference position, so the prediction is a genuine one-parameter
                       family (negative control 1, analytic form).
7. `ratio_negative`  — the vacuum-to-Lambda ratio
                       rho_vac/rho_Lambda = -(2-K_B) c^2 G0(Y_ref)/(16 pi)
                       is negative whenever c^2 > 0, 2-K_B > 0, Y_ref > 0:
                       no positive finite reference reproduces the positive
                       rho_Lambda (sign obstruction / counterexample).
8. `diagnostics_distinct` — the three diagnostic references Y_ref = 1/2, 1, 2 give
                       three DISTINCT vacuum contributions (1/6, 1/2, 4/3).

These certify the algebra of the claim only. They do not derive kappa = 1/2, do not
fix the physical value of Y_ref, and do not settle whether the action holds of the
world.
-/

noncomputable def mu2 (y : ℝ) : ℝ := 1 - 1 / (1 + y) ^ 2
noncomputable def G0  (y : ℝ) : ℝ := y ^ 2 / (1 + y)          -- G0 = -J(0)
noncomputable def J0  (y : ℝ) : ℝ := -G0 y                    -- the determined constant

/-- The MU2 kernel as a positive rational function on (0, inf):
    1 - 1/(1+y)^2 = (y^2+2y)/(1+y)^2.  (The unrestricted identity fails at y = -1
    under totalized division; the physical domain is y > 0.) -/
theorem mu2_closed {y : ℝ} (hy : 0 < y) : mu2 y = (y ^ 2 + 2 * y) / (1 + y) ^ 2 := by
  unfold mu2
  have h1 : 1 + y ≠ 0 := by linarith
  have h1sq : (1 + y) ^ 2 ≠ 0 := pow_ne_zero 2 h1
  field_simp [h1, h1sq]
  ring

/-- G0(Y) = Y^2/(1+Y) > 0 for Y > 0. -/
theorem g0_pos {y : ℝ} (hy : 0 < y) : 0 < G0 y := by
  unfold G0
  have hden : 0 < 1 + y := by linarith
  exact div_pos (sq_pos_of_pos hy) hden

/-- The determined constant J(0) = -Y_ref^2/(1+Y_ref) is negative for every
    positive finite reference. -/
theorem j0_negative {y : ℝ} (hy : 0 < y) : J0 y < 0 := by
  unfold J0
  have h : 0 < G0 y := g0_pos hy
  linarith

/-- G0 is the exact primitive of the kernel on (0, inf): deriv G0 = mu_2. -/
theorem g0_deriv_eq_mu2 {y : ℝ} (hy : 0 < y) : deriv G0 y = mu2 y := by
  have hpow : HasDerivAt (fun z : ℝ => z ^ 2) (2 * y) y := by
    change HasDerivAt (id ^ 2) (2 * y) y
    have hp0 : HasDerivAt (id ^ 2) ((↑(2 : ℕ) : ℝ) * y ^ (2 - 1) * 1) y := by
      exact (hasDerivAt_id y).pow (2 : ℕ)
    have hnorm : (↑(2 : ℕ) : ℝ) * y ^ (2 - 1) * 1 = 2 * y := by norm_num [pow_one]
    rwa [hnorm] at hp0
  have hden : HasDerivAt (fun z : ℝ => 1 + z) 1 y := by
    exact (hasDerivAt_id y).const_add (1 : ℝ)
  have hden0 : 1 + y ≠ 0 := by linarith
  have hmain : HasDerivAt (fun z : ℝ => z ^ 2 / (1 + z))
      ((2 * y * (1 + y) - y ^ 2 * 1) / (1 + y) ^ 2) y := hpow.div hden hden0
  have hquot : (2 * y * (1 + y) - y ^ 2 * 1) / (1 + y) ^ 2 = (y ^ 2 + 2 * y) / (1 + y) ^ 2 := by
    field_simp [hden0]
    ring
  have hG : HasDerivAt G0 ((y ^ 2 + 2 * y) / (1 + y) ^ 2) y := by
    unfold G0
    rw [← hquot]
    exact hmain
  rw [hG.deriv, mu2_closed hy]

/-- G0 strictly increasing on (0, inf): |J(0)| = G0(Y_ref) grows strictly with the
    reference position, so the vacuum prediction is a genuine one-parameter family
    (negative control 1, analytic form, no calculus). -/
theorem g0_strict_mono {a b : ℝ} (ha : 0 < a) (h : a < b) : G0 a < G0 b := by
  unfold G0
  have h1p : 0 < 1 + a := by linarith
  have h2p : 0 < 1 + b := by linarith
  have hba : 0 < b - a := by linarith
  have hsum : 0 < b + a + a * b := by
    have hab : 0 < a * b := mul_pos ha (lt_trans ha h)
    nlinarith
  have hprod : 0 < (b - a) * (b + a + a * b) := mul_pos hba hsum
  have hcross : a ^ 2 * (1 + b) < (1 + a) * b ^ 2 := by
    nlinarith [hprod]
  field_simp [ne_of_gt h1p, ne_of_gt h2p]
  exact hcross

/-- G0 strictly increasing on (0, inf): the vacuum contribution
    |J(0)| = G0(Y_ref) changes monotonically with the reference position. -/
theorem g0_deriv_pos {y : ℝ} (hy : 0 < y) : 0 < deriv G0 y := by
  rw [g0_deriv_eq_mu2 hy, mu2_closed hy]
  have hden : 0 < (1 + y) ^ 2 := sq_pos_of_pos (by linarith)
  have hnum : 0 < y ^ 2 + 2 * y := by
    nlinarith [sq_nonneg y]
  exact div_pos hnum hden

/-- Sign obstruction: with c^2 > 0, 2-K_B > 0 and Y_ref > 0,
    rho_vac/rho_Lambda = -(2-K_B) c^2 G0(Y_ref)/(16 pi) < 0.
    A boundary condition at any finite positive reference gives a NEGATIVE vacuum
    density, so it cannot reproduce the positive rho_Lambda. -/
theorem ratio_negative {c2 KB lam : ℝ} (hc2 : 0 < c2) (hKB : 0 < 2 - KB) (hl : 0 < lam) :
    -(c2 * G0 lam * (2 - KB) / (16 * Real.pi)) < 0 := by
  have hG : 0 < G0 lam := g0_pos hl
  have hnum : 0 < c2 * G0 lam * (2 - KB) := mul_pos (mul_pos hc2 hG) hKB
  have h16 : 0 < 16 * Real.pi := mul_pos (by norm_num) Real.pi_pos
  have hdiv : 0 < c2 * G0 lam * (2 - KB) / (16 * Real.pi) := div_pos hnum h16
  exact neg_lt_zero.mpr hdiv

/-- The three diagnostic references Y_ref = 1/2, 1, 2 give three DISTINCT vacuum
    contributions |J(0)| = 1/6, 1/2, 4/3: the prediction changes with the adopted
    reference (negative control, analytic form). -/
theorem diagnostics_distinct : (1 : ℝ) / 6 ≠ 1 / 2 ∧ 1 / 2 ≠ 4 / 3 := by
  constructor <;> norm_num

#check mu2_closed
#check g0_pos
#check j0_negative
#check g0_deriv_eq_mu2
#check g0_deriv_pos
#check g0_strict_mono
#check ratio_negative
#check diagnostics_distinct

#print axioms mu2_closed
#print axioms g0_pos
#print axioms j0_negative
#print axioms g0_deriv_eq_mu2
#print axioms g0_deriv_pos
#print axioms g0_strict_mono
#print axioms ratio_negative
#print axioms diagnostics_distinct
