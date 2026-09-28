import Mathlib
import Mathlib.Tactic

/-
  AS038 -- Recover an AQUAL energy primitive (Lean 4 certificate).

  Framework:  AQUAL-type action  L = (a0^2/8 pi G) F(X) + rho_b Phi,
              X = |grad Phi|^2/a0^2,  F'(X) = mu(sqrt X),
              so that variation gives  div(mu(|grad Phi|/a0) grad Phi) = 4 pi G rho_b
              (historical EXP equation; the branch kernels below are the declared
              Separate Q, RAR, MU2, historical EXP and operative MONO laws).

  The audited cell (task step 2) is MU2:  mu2(x) = 1 - (1 + x/2)^(-2),
  whose primitive is F_2(X) = X - 8 ln(1 + sqrt X / 2) - 16/(sqrt X + 2) + 8,
  i.e. in x = sqrt X variables  P2(x) = x^2 - 8 log(1 + x/2) - 16/(x + 2) + 8,
  with the additive constant pinned by P2(0) = 0 (no field -> no energy).

  Formalized content:
    A  Q-branch algebraic response identity:  yQ(x)^2 + yQ(x) = x^2  for all real x,
       with yQ(x) = (sqrt(1 + 4 x^2) - 1)/2  (the exact inverse of the Q line
       g^2 = B^2 + a0 B, x = g/a0, y = B/a0).
    B  Q-branch boundary: yQ(0) = 0 (physical root; B = 0 at g = 0).
    C  MU2 response relation in algebraic form:  (x - x*mu2(x)) (x + 2)^2 = 4 x
       (i.e. y = x*mu2(x) satisfies  (x - y)(x + 2)^2 = 4 x  -- the implicit
       algebraic response identity of the audited branch, restated exactly).
    D  Euler chain for the recovered MU2 primitive:  deriv P2 x = 2 * x * mu2(x)
       for all x > 0.  Restated exactly:  2x * P2'(x) = 4x^2 * mu2(x) = 4 x y(x);
       equivalently F'(X) = mu(sqrt X) with X = x^2, the AQUAL energy chain
       the task requires the recovered f to satisfy.
    E  Additive constant: P2(0) = 0.
-/

noncomputable section
open Real

/-- Exact inverse of the algebraic a0 line, dimensionless: y = B/a0 as function of x = g/a0. -/
def yQ (x : ℝ) : ℝ := (Real.sqrt (1 + 4 * x ^ 2) - 1) / 2

/-- MU2 constitutive kernel: mu2(x) = 1 - (1 + x/2)^(-2). -/
def mu2 (x : ℝ) : ℝ := 1 - 4 / (x + 2) ^ 2

/-- MU2 energy primitive in x = sqrt X variables, F(0) = 0 additive constant pinned. -/
def P2 (x : ℝ) : ℝ := x ^ 2 - 8 * Real.log (1 + x / 2) - 16 / (x + 2) + 8

theorem sqrt_one_add_four_sq_sq (x : ℝ) : (Real.sqrt (1 + 4 * x ^ 2)) ^ 2 = 1 + 4 * x ^ 2 := by
  rw [Real.sq_sqrt]
  nlinarith [sq_nonneg x]

/- A: Q-branch algebraic response identity (the task's named algebraic response
   identity, restated exactly: y^2 + y = x^2 with y = yQ(x)). -/
theorem qbranch_response_identity (x : ℝ) : yQ x ^ 2 + yQ x = x ^ 2 := by
  unfold yQ
  have ht2 := sqrt_one_add_four_sq_sq x
  have hfac : ((Real.sqrt (1 + 4 * x ^ 2) - 1) / 2) ^ 2 + (Real.sqrt (1 + 4 * x ^ 2) - 1) / 2
      = (Real.sqrt (1 + 4 * x ^ 2) ^ 2 - 1) / 4 := by
    ring
  rw [hfac, ht2]
  ring

/- B: Q-branch boundary: no field, no response. -/
theorem qbranch_yQ_at_zero : yQ 0 = 0 := by
  unfold yQ
  norm_num [Real.sqrt_one]

/- C: MU2 implicit response relation in algebraic form, on the physical domain
   x + 2 != 0 (x = g/a0 > 0 everywhere on the branch):
   y(x) := x*mu2(x) satisfies (x - y)(x + 2)^2 = 4 x. -/
theorem mu2_response_algebraic (x : ℝ) (hx2 : x + 2 ≠ 0) :
    (x - x * mu2 x) * (x + 2) ^ 2 = 4 * x := by
  have hmain : x - x * mu2 x = 4 * x / (x + 2) ^ 2 := by
    unfold mu2
    field_simp [hx2]
    ring
  rw [hmain]
  field_simp [hx2, pow_ne_zero 2 hx2]

/- D: Euler chain of the recovered MU2 primitive:
   deriv P2 x = 2 x mu2(x)  for all x > 0  (F'(X) = mu(sqrt X) with X = x^2).
   This is the AQUAL identity 2x f'(x) = 2 x^2 mu2(x) = 2 x y(x) restated
   exactly for the audited cell. -/
theorem mu2_euler_chain (x : ℝ) (hx : 0 < x) : deriv P2 x = 2 * x * mu2 x := by
  have hx2p : 0 < x + 2 := by positivity
  have hx2 : x + 2 ≠ 0 := ne_of_gt hx2p
  have hx2sq : (x + 2) ^ 2 ≠ 0 := pow_ne_zero 2 hx2
  have harg : 0 < 1 + x / 2 := by positivity
  have hlin : HasDerivAt (fun y : ℝ => 1 + y / 2) (1 / 2) x := by
    simpa using ((hasDerivAt_id x).div_const 2).const_add (1 : ℝ)
  have hlog : HasDerivAt (fun y : ℝ => Real.log (1 + y / 2)) ((1 / 2) / (1 + x / 2)) x :=
    hlin.log (ne_of_gt harg)
  have hsq : HasDerivAt (fun y : ℝ => y ^ 2) (2 * x) x := by
    simpa using (hasDerivAt_pow 2 x)
  have hlin2 : HasDerivAt (fun y : ℝ => y + 2) 1 x := by
    simpa [add_comm] using (hasDerivAt_id x).const_add 2
  have hinv : HasDerivAt (fun y : ℝ => (y + 2)⁻¹) (-1 / (x + 2) ^ 2) x :=
    hlin2.inv hx2
  have hm1 : HasDerivAt (fun y : ℝ => y ^ 2 + -8 * Real.log (1 + y / 2))
      (2 * x + -8 * ((1 / 2) / (1 + x / 2))) x :=
    hsq.add (hlog.const_mul (-8))
  have hm2 : HasDerivAt (fun y : ℝ => y ^ 2 + -8 * Real.log (1 + y / 2) + -16 * (y + 2)⁻¹)
      (2 * x + -8 * ((1 / 2) / (1 + x / 2)) + -16 * (-1 / (x + 2) ^ 2)) x :=
    hm1.add (hinv.const_mul (-16))
  have hm3 : HasDerivAt (fun y : ℝ => y ^ 2 + -8 * Real.log (1 + y / 2) + -16 * (y + 2)⁻¹ + 8)
      ((2 * x + -8 * ((1 / 2) / (1 + x / 2)) + -16 * (-1 / (x + 2) ^ 2)) + 0) x :=
    hm2.add (hasDerivAt_const (x := x) 8)
  have hd : HasDerivAt P2
      ((2 * x + -8 * ((1 / 2) / (1 + x / 2)) + -16 * (-1 / (x + 2) ^ 2)) + 0) x := by
    unfold P2
    convert hm3 using 2
    · ring_nf
  have hd' : HasDerivAt P2 (2 * x * mu2 x) x := by
    convert hd
    unfold mu2
    field_simp [hx2, hx2sq, ne_of_gt harg]
    ring
  exact hd'.deriv

/- E: additive constant pinned: F(0) = 0 (no field -> no energy density). -/
theorem P2_at_zero : P2 0 = 0 := by
  unfold P2
  norm_num

/- Axiom audit: every theorem below must print an axiom list subseteq {propext, Classical.choice, Quot.sound}. -/
#print axioms qbranch_response_identity
#print axioms qbranch_yQ_at_zero
#print axioms mu2_response_algebraic
#print axioms mu2_euler_chain
#print axioms P2_at_zero
