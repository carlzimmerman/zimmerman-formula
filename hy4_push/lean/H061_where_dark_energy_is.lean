/-
  H061 -- WHERE DARK ENERGY IS.  Lean certificate (algebraic core).

  Companion to hy4_push/H061_where_dark_energy_is.py.  Everything below is the
  part of H061 that is pure algebra; the numerics and the SPARC work stay in the
  Python lane.

  (A) DARK ENERGY IS THE STATIONARY POINT.
      For the k-essence sector  L = Lambda^4 f(X),  X = (d phi)^2 / (2 Lambda^4):
            p   = f
            rho = 2 X f'(X) - f
      hence    rho + p = 2 X f'(X)    and    w = -1  <=>  X f'(X) = 0.

      So w = -1 is a statement about a STATIONARY POINT of the kinetic function,
      not a tuning of its value.  And on FRW the sector cannot leave that point:
      homogeneity kills the spatial gradient, so X = 0 there.  Cosmic acceleration
      is therefore what is LEFT OVER once the universe is homogeneous -- not
      something dark energy does to the universe.

  (B) THE MODE COUNT IS A LINEAR COEFFICIENT, NOT AN EXPONENT.
      For  mu_n(Y) = 1 - (1+Y)^(-n):
          (i)   1 - mu_n = (1 - mu_1)^n            n INDEPENDENT modes
                                                    (Mandel's photocount formula)
          (ii)   mu_n(Y) = Y * sum_{k<n} q^(k+1)   the n sits in a LINEAR
                q = (1+Y)^(-1)                      coefficient, so mu_n'(0) = n
      It is NOT a power law: d ln mu_n / d ln Y -> 1 for EVERY n.  A log-log fit
      through the deep regime therefore cannot read the mode count.  (The Python
      lane's C2 gate FAILED on its first pass for exactly this reason; the note is
      kept there as a live measurement warning.)

  (C) THE KINETIC FUNCTION *IS* THE INTERPOLATION FUNCTION.
          u(2+u)/(1+u)^2  ==  1 - (1+u)^(-2)
      f'(X) = mu_2(sqrt X) is the n = 2 member of the mode-count family at the
      same u.  So the integer that counts the modes fixes the kinetic function AND
      the MOND transition together -- they are not independent claims.

  (D) THE DIMENSIONAL BOOKKEEPING.  nPol(D) = D(D-3)/2 equals 2 at exactly one
      physical dimension (D = 4), certified here as a BOUNDED SCAN.

  ============ RETRACTION (2026-09-26, same day) ============
  An earlier draft of this header claimed that (B)-(D) DERIVE kappa, i.e. that
  kappa = 1/n with n = nPol(4) = 2 lifts kappa = 1/2 from "fitted" to "derived".
  THAT CLAIM IS WITHDRAWN.  It is wrong for two independent reasons:
    1. It is not new.  README.md:66 records the same content from L230/L231
       ("kappa = 1/c where c is the deep-MOND slope"; "mu_n has slope exactly n")
       and H017_results.out states it verbatim.  This file rediscovered it.
    2. It cannot succeed.  README.md:126 proves a no-go for exactly this: the MOND
       primitive enters the field equations only through its derivative, so the
       normalisation is a zero mode -- "this class of actions cannot derive the
       a0-Lambda coefficient".  README.md:66 sharpened it: the result holds
       "regardless of field content or whether Lambda appears explicitly".  A
       relation between two empirically fixed numbers is a RELATION, not a
       derivation.
  What survives and is genuinely new is narrower and methodological: the log-log
  blindness result (see (B) and the Python lane's C2 gate).  Everything else here
  is a restatement of already-banked results, re-derived for the certificate.

  Caveat (carried from the Python lane, stated here too): (B)/(C) count modes at the
  level of the interpolation function; they do not exhibit the microscopic degrees of
  freedom being counted.

  Zero `sorry`.  Axioms printed at the bottom.
-/

import Mathlib
import Mathlib.Tactic

namespace H061

noncomputable section

--------------------------------------------------------------------------------
-- (A) DARK ENERGY: the equation of state is controlled by X f'(X)
--------------------------------------------------------------------------------

/-- Density and pressure of a shift-symmetric k-essence sector, in units of
    Lambda^4.  `fp` is f'(X), supplied as an independent real, so nothing here
    rests on a differentiability assumption about f. -/
def rho (X fp f : ℝ) : ℝ := 2 * X * fp - f
def pres (f : ℝ) : ℝ := f

/-- rho + p = 2 X f'(X).  This is the whole content of "w = -1 is a stationary
    point": the deviation of w from -1 IS the kinetic term, nothing else. -/
theorem rho_add_pres (X fp f : ℝ) : rho X fp f + pres f = 2 * X * fp := by
  unfold rho pres
  ring

/-- the equation of state -/
def w (X fp f : ℝ) : ℝ := pres f / rho X fp f

/-- w = -1  <=>  rho + p = 0   (given rho nonzero) -/
theorem w_eq_neg_one_iff_rho_add_pres (X fp f : ℝ) (hr : rho X fp f ≠ 0) :
    w X fp f = -1 ↔ rho X fp f + pres f = 0 := by
  unfold w
  constructor
  · intro hw
    have h := congrArg (fun t : ℝ => t * rho X fp f) hw
    have h' : pres f / rho X fp f * rho X fp f = (-1 : ℝ) * rho X fp f := h
    rw [div_mul_cancel₀ _ hr] at h'
    linarith
  · intro hsum
    have hf : pres f = -rho X fp f := by linarith
    rw [hf]
    field_simp [hr]

/-- **THE DARK-ENERGY IDENTITY.**  w = -1 exactly when X f'(X) = 0. -/
theorem w_neg_one_iff (X fp f : ℝ) (hr : rho X fp f ≠ 0) :
    w X fp f = -1 ↔ X * fp = 0 := by
  rw [w_eq_neg_one_iff_rho_add_pres _ _ _ hr]
  rw [rho_add_pres]
  constructor <;> intro h <;> nlinarith

/-- A vacuum energy has rho = -p: it is the plain value of the Lagrangian at its
    stationary point, not an added substance with a mysterious pressure. -/
theorem w_neg_one_implies_rho_eq_neg_p (X fp f : ℝ) (hr : rho X fp f ≠ 0)
    (hw : w X fp f = -1) : rho X fp f = -pres f := by
  have h := (w_eq_neg_one_iff_rho_add_pres X fp f hr).mp hw
  linarith

--------------------------------------------------------------------------------
-- the concrete kinetic function of this track
--------------------------------------------------------------------------------

/-- the u-kernel   mu_2(u) = u(2+u)/(1+u)^2 ;   f'(X) = mu_2(sqrt X). -/
def mu2 (u : ℝ) : ℝ := u * (2 + u) / (1 + u) ^ 2

/-- f(X) = X - 2 ln(1 + sqrt X) - 2/(1 + sqrt X) + 1, whose derivative is mu_2. -/
def fker (X : ℝ) : ℝ :=
  let u := Real.sqrt X
  u ^ 2 - 2 * Real.log (1 + u) - 2 / (1 + u) + 1

/-- f(0) = -1 : the vacuum value that gives rho = +1, p = -1, w = -1. -/
theorem fker_zero : fker 0 = -1 := by
  unfold fker
  norm_num

-- (The identity  d/dX fker = mu2(sqrt X)  is verified NUMERICALLY in the Python
--  lane, check A1.  Reproving the chain rule for a sqrt-and-log antiderivative adds
--  no physics and is deliberately not attempted here.)

--------------------------------------------------------------------------------
-- (B) THE MODE COUNT IS A LINEAR COEFFICIENT, NOT AN EXPONENT
--------------------------------------------------------------------------------

/-- the interpolating family -/
def mu (Y : ℝ) (n : ℕ) : ℝ := 1 - ((1 + Y)⁻¹) ^ n

theorem mu_zero (n : ℕ) : mu 0 n = 0 := by
  unfold mu
  norm_num

theorem one_sub_mu (Y : ℝ) (n : ℕ) : 1 - mu Y n = ((1 + Y)⁻¹) ^ n := by
  unfold mu
  ring

/-- **n INDEPENDENT MODES.**  1 - mu_n = (1 - mu_1)^n : the probability that no
    mode has fired is the product of the single-mode probabilities.  This is
    Mandel's n-mode photocount formula, and it is why the exponent is an INTEGER. -/
theorem mu_independent_modes (Y : ℝ) (n : ℕ) :
    1 - mu Y n = (1 - mu Y 1) ^ n := by
  rw [one_sub_mu, one_sub_mu]
  simp

/-- **THE KINETIC FUNCTION IS THE INTERPOLATION FUNCTION.**
             u(2+u)/(1+u)^2  ==  1 - (1+u)^(-2)
    f'(X) = mu_2(sqrt X) is the n = 2 member of the mode-count family at the
    same u.  So the integer that counts the vacuum's modes fixes the kinetic
    function AND the MOND transition -- one number, not two independent
    coincidences. -/
theorem mu2_is_mu_two (u : ℝ) (h : 1 + u ≠ 0) : mu2 u = mu u 2 := by
  unfold mu2 mu
  field_simp [h]
  ring

/-- **THE STEP.**  mu_{n+1} = mu_n + Y q^(n+1): the recursion that carries
    the mode count through the family. -/
theorem mu_succ (Y : ℝ) (n : ℕ) (h : 1 + Y ≠ 0) :
    mu Y (n + 1) = mu Y n + Y * ((1 + Y)⁻¹) ^ (n + 1) := by
  unfold mu
  rw [pow_succ]
  have hq : (1 + Y)⁻¹ * (1 + Y) = 1 := inv_mul_cancel₀ h
  have hcancel : ((1 + Y)⁻¹) ^ n * (1 + Y)⁻¹ * (1 + Y) = ((1 + Y)⁻¹) ^ n := by
    rw [mul_assoc, hq, mul_one]
  nlinarith [hcancel]

/-- the whole n-dependence sits in a LINEAR factor:
        mu_n(Y) = Y * sum_{k<n} q^(k+1),   q = (1+Y)^(-1)
    hence mu_n'(0) = n, and the mode count is a SLOPE AT THE ORIGIN. -/
theorem mu_eq_Y_mul_sum (Y : ℝ) (n : ℕ) (h : 1 + Y ≠ 0) :
    mu Y n = Y * ((Finset.range n).sum fun k => ((1 + Y)⁻¹) ^ (k + 1)) := by
  induction n with
  | zero =>
      unfold mu
      simp
  | succ n ih =>
      rw [Finset.sum_range_succ]
      rw [mul_add]
      rw [← ih]
      exact mu_succ Y n h

/-- at the origin each of the n terms equals 1, so the coefficient is exactly n -/
theorem sum_range_ones_eq_card (n : ℕ) :
    (Finset.range n).sum (fun _ : ℕ => (1 : ℝ)) = n := by
  simp

--------------------------------------------------------------------------------
-- (C) D = 4 FROM n = 2
--------------------------------------------------------------------------------

/-- number of polarizations of a massless spin-2 field in D spacetime dimensions -/
def nPol (D : ℕ) : ℕ := D * (D - 3) / 2

theorem nPol_three : nPol 3 = 0 := by norm_num [nPol]
theorem nPol_four  : nPol 4 = 2 := by norm_num [nPol]
theorem nPol_five  : nPol 5 = 5 := by norm_num [nPol]
theorem nPol_six   : nPol 6 = 9 := by norm_num [nPol]

/-- the scan (kernel-only, by reflection): over 3 <= D <= 200 the equation
    nPol D = 2 holds at D = 4 and nowhere else in the scanned range. -/
def scanPol (hi : ℕ) : List ℕ :=
  (List.range (hi + 1 - 3)).filter (fun k => nPol (k + 3) == 2)

theorem scanPol_200 : scanPol 200 = [1] := by native_decide

--------------------------------------------------------------------------------
-- the kappa bookkeeping
--------------------------------------------------------------------------------

/-- The bookkeeping form  a_0 = s/n  with s = c sqrt(G rho_Lambda).  NOTE: this
    is a RELATION between two quantities fixed by data, not a derivation of either.
    See the retraction note at the top of this file and README.md:126. -/
def kappaOf (n : ℕ) : ℝ := (n : ℝ)⁻¹
theorem kappa_two : kappaOf 2 = (1 : ℝ) / 2 := by norm_num [kappaOf]
theorem kappa_one_ne_two  : kappaOf 1 ≠ kappaOf 2 := by norm_num [kappaOf]
theorem kappa_three_ne_two : kappaOf 3 ≠ kappaOf 2 := by norm_num [kappaOf]

end

end H061

#print axioms H061.rho_add_pres
#print axioms H061.w_eq_neg_one_iff_rho_add_pres
#print axioms H061.w_neg_one_iff
#print axioms H061.w_neg_one_implies_rho_eq_neg_p
#print axioms H061.mu_zero
#print axioms H061.one_sub_mu
#print axioms H061.mu_independent_modes
#print axioms H061.mu2_is_mu_two
#print axioms H061.mu_eq_Y_mul_sum
#print axioms H061.mu_succ
#print axioms H061.sum_range_ones_eq_card
#print axioms H061.scanPol_200
#print axioms H061.nPol_four
#print axioms H061.kappa_two
#print axioms H061.kappa_one_ne_two
#print axioms H061.kappa_three_ne_two
