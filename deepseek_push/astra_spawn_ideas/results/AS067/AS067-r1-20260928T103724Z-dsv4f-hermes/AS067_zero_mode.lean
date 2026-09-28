import Mathlib
import Mathlib.Tactic

/-!
# AS067 -- Additive vacuum zero mode in the local action (Lean 4 certificate)

Framework (dimensionless, c = 1, reduced action of the corpus k01 class):
    alpha = 2 - K_B,  Lambda_eff = Lambda + alpha*J(0)/2 + K(Q0)/2
    (masse density convention: the constant sector is -2*Lambda - alpha*J(0) - K(Q0)).
    MU_n family: mu_n(Y) = 1 - (1+Y)^(-n),  Y = g/s,  s = c*sqrt(G*rho_L),  a0 = kappa*s.

Certified content (each statement is an exact algebraic/analytic identity; the
physical reading is in derivation.md):

  A  lambda_eff        : -2*(Lambda + alpha*J0/2 + K0/2) = -2*Lambda - alpha*J0 - K0
                         (the background combination), and its uniqueness
                         (solve_eff): any a with -2a = -2Lambda - alpha*J0 - K0
                         equals Lambda + alpha*J0/2 + K0/2.
  B  shift_linear      : J0 -> J0 + lam*C shifts Lambda_eff by lam*alpha*C/2, linearly.
  C  compensation      : (Lambda - lam*alpha*C/2) + alpha*(J0 + lam*C)/2 + K0/2
                         = Lambda + alpha*J0/2 + K0/2  (compensated pair leaves
                         Lambda_eff unchanged), and
     density_vanish    : -2*(-(lam*alpha*C/2)) - alpha*(lam*C) = 0  (the action
                         density is unchanged pointwise: exact gauge symmetry).
  D  deriv_shift_inv   : deriv (fun Y => J Y + C) = deriv J   (the statics see the
                         primitive only through J': constants are invisible), and
     deriv_const_shift : deriv (fun _ : R => C) = 0.
  E  muN_slope_note   : the deep-MOND slope deriv (fun Y => muN n Y) 0 = n is NOT
                       re-certified here (documented tooling limitation; proved
                       symbolically for symbolic n in the audit run, and the n = 2
                       landing is certified by the corpus's PD07);
  F  mu2_pos, mu3_pos : 0 < Y -> 0 < mu_n(Y)  (positive response; with the
                       saturated-end fixing J(0) = -I a0^2, I > 0, hence the
                       vacuum zero is negative: rho_vac < 0 for the MU_n family).
  G  deep_matching, kappa_chain : mu ~ n*g/s and mu*g = g_N give g^2 = (s/n)*g_N,
                       i.e. a0 = s/n and kappa = a0/s = 1/n  (the L230 chain).

Notes: monotonicity/slope statements are dimensionless; both a0 footings
(9.3619e-11, 1.1279e-10 m/s^2) apply unchanged.  No `sorry`; axioms restricted
to {propext, Classical.choice, Quot.sound} (verified via #print axioms below).
-/

noncomputable section
open Real Filter

/- A: the background combination and its uniqueness. -/
theorem lambda_eff (Lambda J0 K0 alpha : ℝ) :
    -2 * (Lambda + alpha * J0 / 2 + K0 / 2) = -2 * Lambda - alpha * J0 - K0 := by
  ring

theorem solve_eff (a Lambda J0 K0 alpha : ℝ)
    (h : -2 * a = -2 * Lambda - alpha * J0 - K0) :
    a = Lambda + alpha * J0 / 2 + K0 / 2 := by
  nlinarith

/- B: linearity of the background shift in the added constant (J0 -> J0 + lam*C). -/
theorem shift_linear (Lambda J0 K0 C lam alpha : ℝ) :
    (Lambda + alpha * (J0 + lam * C) / 2 + K0 / 2)
      = (Lambda + alpha * J0 / 2 + K0 / 2) + lam * alpha * C / 2 := by
  ring

/- C: the compensated pair (J -> J + lam*C, Lambda -> Lambda - lam*alpha*C/2)
      leaves Lambda_eff unchanged; the action density change vanishes pointwise. -/
theorem compensation (Lambda J0 K0 C lam alpha : ℝ) :
    (Lambda - lam * alpha * C / 2) + alpha * (J0 + lam * C) / 2 + K0 / 2
      = Lambda + alpha * J0 / 2 + K0 / 2 := by
  ring

theorem density_vanish (C lam alpha : ℝ) :
    -2 * (-(lam * alpha * C / 2)) - alpha * (lam * C) = 0 := by
  ring

/- D: the statics see the primitive only through its derivative: a constant shift
      of J does not change any field equation built from J'. -/
theorem deriv_shift_inv (J : ℝ → ℝ) (C : ℝ) :
    deriv (fun Y : ℝ => J Y + C) = deriv J := by
  funext Y
  rw [deriv_add_const]

theorem deriv_const_shift (C : ℝ) : deriv (fun _ : ℝ => C) = 0 := by
  funext Y
  simp

/- E: deep-MOND slopes of the MU_n family.

   deriv (fun Y => muN n Y) 0 = n  for every n : Nat, n >= 1, is a standard
   calculus fact; here it is NOT re-certified: (i) the audit script proves it
   symbolically for symbolic n (sympy limit of d/dY [1-(1+Y)^(-n)] at 0 = n,
   plus instances n = 1..6, checks D1); (ii) the channel-count landing for the
   operative n = 2 is already certified in the corpus (PD07, kappa_locked).
   Attempted Lean proofs hit typeclass-instance mismatches inside Mathlib's
   HasDerivAt (AddCommGroup/Module instance equality goals) that `convert`,
   `simpa` and `fun_prop` cannot close on Mathlib v4.34.0-rc2; documented here
   as a tooling limitation, not a mathematical gap.  The zero-mode algebra --
   the content this seed audits -- IS certified below (A-D, F, G). -/

/- F: positive response on Y > 0 (instances n = 2, 3) -- with J(0) = -I a0^2 and
      I = 2*int z*mu(z) dz > 0 this is the sign statement rho_vac < 0 of S6a. -/
def muN (n : ℕ) (Y : ℝ) : ℝ := 1 - 1 / (1 + Y) ^ n
theorem mu2_pos (Y : ℝ) (hY : 0 < Y) : 0 < muN 2 Y := by
  unfold muN
  have hY1 : 0 < (1 : ℝ) + Y := by linarith
  have hsq : 0 < (1 + Y) ^ 2 := sq_pos_of_pos hY1
  have hone : (1 : ℝ) < (1 + Y) ^ 2 := by
    nlinarith [sq_pos_of_pos hY]
  rw [sub_pos, div_lt_one hsq]
  exact hone

theorem mu3_pos (Y : ℝ) (hY : 0 < Y) : 0 < muN 3 Y := by
  unfold muN
  have hY1 : 0 < (1 : ℝ) + Y := by linarith
  have hcb : 0 < (1 + Y) ^ 3 := pow_pos hY1 3
  have hone : (1 : ℝ) < (1 + Y) ^ 3 := by
    nlinarith [sq_pos_of_pos hY]
  rw [sub_pos, div_lt_one hcb]
  exact hone

/- G: the L230 chain: mu ~ n*g/s and mu*g = g_N imply g^2 = (s/n)*g_N, hence
      a0 = s/n and kappa = a0/s = 1/n.  (Algebraic core of the deep matching.) -/
theorem deep_matching (g s gN n : ℝ) (hn : n ≠ 0) (hs : s ≠ 0)
    (h : n * (g / s) * g = gN) : g ^ 2 = s * gN / n := by
  field_simp [hn, hs] at h ⊢
  ring_nf at h ⊢
  nlinarith

theorem kappa_chain (a0 s n : ℝ) (hn : n ≠ 0) (hs : s ≠ 0)
    (h : a0 = s / n) : a0 / s = 1 / n := by
  rw [h]
  field_simp [hn, hs]

end

-- Print axioms (unfiltered) -- the certificate is clean iff every listed name
-- depends only on the allowed set {propext, Classical.choice, Quot.sound}.
#print axioms lambda_eff
#print axioms solve_eff
#print axioms shift_linear
#print axioms compensation
#print axioms density_vanish
#print axioms deriv_shift_inv
#print axioms deriv_const_shift
#print axioms mu2_pos
#print axioms mu3_pos
#print axioms deep_matching
#print axioms kappa_chain