import Mathlib
/-!
# FINAL-12 (LEAN-BACKGROUND) — certificates for the background and conservation statements

SCOPE.  This file certifies ALGEBRA and REAL ANALYSIS: explicit identities, inequalities and one
explicit epsilon-limit, over the hypotheses written at each theorem.  It does **not** certify that
any of these relations is a law of nature, that the khronon/Zimmerman action is the correct
action, or that the numerical values of I0, mu, x_T, R_b are the ones the universe realises.
Every identification of a symbol with a physical quantity (Q, n, p, rho, w, k_J, R_b) is an
assumption imported from the design notes, not a conclusion of this file.

CONVENTIONS (DT1 section 1, DT2 section 2), with kappa = 4 pi G / c^2 > 0.

    Q = sqrt(-g^{mu nu} d_mu tau d_nu tau) > 0,      x = Q - 1,
    V(Q) = kappa L_K(Q)   (up to an additive constant, which cancels from w and c_ad^2),
    n(x) = V_Q(1 + x),                               n'(x) = dn/dx,
    kappa p = V,                                     kappa rho = Q n - V,
    w = p/rho,                                       c_ad^2 = dp/drho = n/(Q n'),  Q = 1 + x.

kappa cancels from w and from c_ad^2, so it is carried only in the comments.  Along the FRW
background (homogeneous, P = 0) the scalar equation gives the conserved charge
a^3 n(xbar(a)) = n0, and I0 := 2 n0.

## What is certified, target by target

1. **FRW equation of state.**  For the quadratic law n = mu^2 x the charge equation gives
   xbar(a) = I0/(2 mu^2 a^3), and the EXACT quadratic equation of state w = x/(2+x) equals
   w0/(w0 + a^3) with w0 = I0/(4 mu^2)  (`frw_eos_quadratic`).  Then `w < 1/2` iff `a^3 > w0`
   (`wFRW_lt_half_iff`), w is strictly decreasing in a (`wFRW_strictly_decreasing`), and
   `w -> 0` as `a -> +infinity` in explicit epsilon form (`wFRW_tendsto_zero`).

2. **Coldness / sound speed.**
   * `cs2_quadratic`: DT1's ratio n/n' for n = mu^2 x equals x (an exact, epoch-independent ratio).
   * `cad2_quadratic`: the EXACT adiabatic speed dp/drho is x/(1+x) = (Qbar - 1)/Qbar; DT1's x is
     its leading order.  The gap is certified in `quad_cs_minus_w`.
   * `cs2_exponential`: for n = n_* exp(x/x_T) the ratio n/n' is x_T exactly, at every epoch.
   * `cad2_exponential`, `eos_exponential`, `exp_w_minus_cs2`: the exact adiabatic speed is x_T/Q and
     the exact equation of state is x_T/(Q - x_T), with gap x_T^2/(Q(Q - x_T)).
   **CORRECTION TO THE LANE TARGET.**  "c_s^2 = x, i.e. w = Qbar - 1" is FALSE: the equation of
   state of the quadratic dust is w = (Qbar-1)/(Qbar+1), and the exact adiabatic speed is
   (Qbar-1)/Qbar.  Likewise the exponential term is NOT exactly isothermal (DT2 section 5).
   Both the DT1 approximation and the exact relation are certified here so that the gap is
   machine-checked rather than silently dropped.  Note the target's own item (1) is consistent with
   the EXACT w, not with `w = Qbar - 1`: `w = w0/(w0 + a^3)` follows from `w = x/(2+x)`, not
   from `w = x` (which would give a pure a-to-the-minus-3 law).

3. **Jeans wavenumber.**  `kJ2_quadratic` / `kJ2_quadratic_value`: the exact value is
   `kappa rho / c_ad^2 = mu^2 (1 + xbar/2)(1 + xbar) = mu^2 + mu^2 xbar (3+xbar)/2`, i.e. mu^2 only
   in the dust limit xbar -> 0 and strictly larger for every xbar > 0 (`kJ2_quadratic_gt_mu2`) — it
   is NOT constant along the background.  `kJ2_exponential` / `kJ2_exponential_ratio`: for the
   exponential term it is `Q(Q - x_T) n'(xbar)` with `n'(xbar) = nbar/x_T`, density-dependent
   through nbar as claimed.

4. **The DT1 section 2 trade-off.**  Certified in the DISCRETE TWO-POINT form the lane permits
   (`tradeoff_two_point`): a continuous, interior-differentiable n with `n' >= k^2` there satisfies
   `k^2 (x_b - x_a) <= n(x_b) - n(x_a)`; `tradeoff_span` divides by `k^2 > 0` for the offset bound
   `x_b - x_a <= (n_b - n_a)/k^2`, and `tradeoff_cap_conflict` is the well-cap consequence.
   The stronger INTEGRAL statement (`int n' = n_b - n_a` by the FTC) is NOT formalized — the
   monotonicity / mean-value two-point estimate is what is certified here.

5. **Budget exhaustion.**  `budget_exhaustion_iff`: with X the non-negative branch of
   `X(1+X) = x^2`, `X(x) = R_b` iff `x = sqrt(R_b(1+R_b))` for `x >= 0` and `R_b > 0`.
   `budgetX_identity`, `budgetX_nonneg` and `budget_char` show X is that branch and is the UNIQUE
   non-negative solution, so the branch convention is immaterial.
-/

noncomputable section
namespace FINAL12

/-! ## 0. definitions -/

/-- the clock's kinetic variable Q = 1 + x -/
def Qof (x : ℝ) : ℝ := 1 + x

/-- the quadratic (mu) well: V = mu^2 x^2 / 2 -/
def Vquad (mu x : ℝ) : ℝ := (mu ^ 2 / 2) * x ^ 2
/-- its charge density n = V_Q = mu^2 x -/
def nQuad (mu : ℝ) : ℝ → ℝ := fun x => mu ^ 2 * x

/-- the exponential well's charge density n = n_* exp(x / x_T) -/
def nExp (nstar xT : ℝ) : ℝ → ℝ := fun x => nstar * Real.exp (x / xT)
/-- its kinetic function in DT1's normalisation V = x_T n -/
def Vexp (nstar xT x : ℝ) : ℝ := xT * nExp nstar xT x

/-- pressure times kappa:  kappa p = V -/
def pressK (V : ℝ) : ℝ := V
/-- density times kappa:  kappa rho = Q n - V -/
def densK (Q n V : ℝ) : ℝ := Q * n - V
/-- the equation of state w = p/rho = (kappa p)/(kappa rho) -/
def eosw (Q n V : ℝ) : ℝ := pressK V / densK Q n V

/-- the exact adiabatic speed c_ad^2 = dp/drho = n/(Q n') with Q = 1 + x -/
def cad2 (n : ℝ → ℝ) (x : ℝ) : ℝ := n x / (Qof x * deriv n x)
/-- DT1's leading (Q approximately 1) expression: the pure ratio n/n' -/
def cs2 (n : ℝ → ℝ) (x : ℝ) : ℝ := n x / deriv n x

/-- the isolated-fluid Jeans wavenumber squared: kappa rho / c_ad^2 = (Q n - V)/c_ad^2 -/
def kJ2 (Q n V c : ℝ) : ℝ := densK Q n V / c

/-- w0 = I0/(4 mu^2) -/
def w0of (I0 mu : ℝ) : ℝ := I0 / (4 * mu ^ 2)
/-- the FRW equation of state w(a) = w0/(w0 + a^3) -/
def wFRW (w0 a : ℝ) : ℝ := w0 / (w0 + a ^ 3)

/-- the budget-exhaustion point x_b(R_b) -/
def xBudget (Rb : ℝ) : ℝ := Real.sqrt (Rb * (1 + Rb))
/-- the budget function: the non-negative branch of X(1+X) = x^2 -/
def budgetX (x : ℝ) : ℝ := (Real.sqrt (1 + 4 * x ^ 2) - 1) / 2

/-! ## 1. the FRW equation of state of the quadratic dust -/

/-- the charge density of the quadratic well IS the Q-derivative of its kinetic function -/
theorem Vquad_deriv (mu x : ℝ) : deriv (Vquad mu) x = nQuad mu x := by
  change deriv (fun y : ℝ => (mu ^ 2 / 2) * y ^ 2) x = mu ^ 2 * x
  rw [deriv_const_mul_field, deriv_pow_field]
  ring

/-- the conserved charge a^3 n(xbar) = n0 solved for the quadratic law -/
theorem quad_background (n0 mu a : ℝ) (hmu : 0 < mu) (ha : 0 < a) :
    nQuad mu (n0 / (mu ^ 2 * a ^ 3)) = n0 / a ^ 3 := by
  dsimp [nQuad]
  have hmu2 : mu ^ 2 ≠ 0 := pow_ne_zero 2 (ne_of_gt hmu)
  have ha3 : a ^ 3 ≠ 0 := pow_ne_zero 3 (ne_of_gt ha)
  field_simp [hmu2, ha3]

/-- **(1)** the FRW equation of state: the exact quadratic w = x/(2+x), evaluated at the background
    xbar(a) = I0/(2 mu^2 a^3), is w0/(w0 + a^3) with w0 = I0/(4 mu^2) -/
theorem frw_eos_quadratic (I0 mu a : ℝ) (hI0 : 0 < I0) (hmu : 0 < mu) (ha : 0 < a) :
    (I0 / (2 * mu ^ 2 * a ^ 3)) / (2 + I0 / (2 * mu ^ 2 * a ^ 3)) =
      wFRW (w0of I0 mu) a := by
  dsimp [wFRW, w0of]
  have hmu2 : mu ^ 2 ≠ 0 := pow_ne_zero 2 (ne_of_gt hmu)
  have ha3 : a ^ 3 ≠ 0 := pow_ne_zero 3 (ne_of_gt ha)
  have hxbar_pos : 0 < 2 + I0 / (2 * mu ^ 2 * a ^ 3) := by positivity
  have hw0_pos : 0 < I0 / (4 * mu ^ 2) + a ^ 3 := by positivity
  field_simp [hmu2, ha3, hxbar_pos.ne', hw0_pos.ne'] <;> ring

/-- helper: a > 1 forces a^3 > a -/
theorem one_lt_cube {a : ℝ} (ha : 1 < a) : a < a ^ 3 := by
  have ha0 : 0 < a := by linarith
  have hsq : (1 : ℝ) < a ^ 2 := by
    nlinarith [sq_pos_of_pos (by linarith : (0 : ℝ) < a - 1)]
  have hmul : a * 1 < a * a ^ 2 := mul_lt_mul_of_pos_left hsq ha0
  nlinarith

/-- **(1a)** w < 1/2 exactly when a^3 > w0 -/
theorem wFRW_lt_half_iff (w0 a : ℝ) (hw0 : 0 < w0) (ha : 0 < a) :
    wFRW w0 a < (1 / 2 : ℝ) ↔ w0 < a ^ 3 := by
  dsimp [wFRW]
  have hden : 0 < w0 + a ^ 3 := by positivity
  constructor
  · intro h
    have hmul : w0 < (1 / 2 : ℝ) * (w0 + a ^ 3) := (div_lt_iff₀ hden).mp h
    nlinarith
  · intro h
    have hmul : w0 < (1 / 2 : ℝ) * (w0 + a ^ 3) := by nlinarith
    exact (div_lt_iff₀ hden).mpr hmul

/-- **(1b)** w is STRICTLY DECREASING in the scale factor -/
theorem wFRW_strictly_decreasing (w0 a b : ℝ) (hw0 : 0 < w0) (ha : 0 < a) (hab : a < b) :
    wFRW w0 b < wFRW w0 a := by
  dsimp [wFRW]
  have _ : 0 < b := lt_trans ha hab
  have hda : 0 < w0 + a ^ 3 := by positivity
  have hdb : 0 < w0 + b ^ 3 := by positivity
  have hab3 : a ^ 3 < b ^ 3 := pow_lt_pow_left₀ hab (le_of_lt ha) (by norm_num : (3 : ℕ) ≠ 0)
  have hsum : w0 + a ^ 3 < w0 + b ^ 3 := by linarith
  rw [div_lt_iff₀ hdb]
  rw [show (w0 / (w0 + a ^ 3)) * (w0 + b ^ 3) =
        (w0 * (w0 + b ^ 3)) / (w0 + a ^ 3) by ring]
  simpa [mul_comm, mul_left_comm, mul_assoc] using (lt_div_iff₀ hda).mpr (mul_lt_mul_of_pos_left hsum hw0)

/-- **(1c)** w -> 0 as a -> +infinity, stated without filter notation: for every eps > 0 there is
    A > 0 such that every a >= A has 0 <= w(a) < eps.  The witness A = w0/eps + 2 is the rate. -/
theorem wFRW_tendsto_zero (w0 : ℝ) (hw0 : 0 < w0) :
    ∀ eps : ℝ, 0 < eps → ∃ A : ℝ, 0 < A ∧
      ∀ a : ℝ, A ≤ a → 0 ≤ wFRW w0 a ∧ wFRW w0 a < eps := by
  intro eps heps
  refine ⟨w0 / eps + 2, by positivity, ?_⟩
  intro a ha
  have ha1 : (1 : ℝ) < a := by
    have hq : 0 < w0 / eps := by positivity
    linarith
  have _ : 0 < a := by linarith
  have hden : 0 < w0 + a ^ 3 := by positivity
  constructor
  · dsimp [wFRW]
    positivity
  · dsimp [wFRW]
    rw [div_lt_iff₀ hden]
    have hgt : w0 / eps < a := by linarith
    have hept : w0 < a * eps := (div_lt_iff₀ heps).mp hgt
    have hacube : a < a ^ 3 := one_lt_cube ha1
    have hepsc : a * eps < a ^ 3 * eps := mul_lt_mul_of_pos_right hacube heps
    nlinarith

/-! ## 2. coldness / sound speed -/

/-- the derivative of the quadratic law: n' = mu^2 -/
theorem nQuad_deriv (mu x : ℝ) : deriv (nQuad mu) x = mu ^ 2 := by
  change deriv (fun y : ℝ => mu ^ 2 * y) x = mu ^ 2
  rw [deriv_const_mul_field, deriv_id'', mul_one]

/-- the derivative of the exponential law: n'(x) = n(x)/x_T -/
theorem nExp_deriv (nstar xT x : ℝ) : deriv (nExp nstar xT) x = nExp nstar xT x / xT := by
  change deriv (fun y : ℝ => nstar * Real.exp (y / xT)) x = nstar * Real.exp (x / xT) / xT
  have h1 := (hasDerivAt_id x).div_const xT
  have h2 := (Real.hasDerivAt_exp (x / xT)).comp x h1
  have h3 := h2.const_mul nstar
  convert h3.deriv using 1
  · rfl
  · ring_nf

/-- **(2, quadratic)** DT1's ratio n/n' for n = mu^2 x is x — exact and epoch-independent -/
theorem cs2_quadratic (mu x : ℝ) (hmu : 0 < mu) :
    cs2 (nQuad mu) x = x := by
  dsimp [cs2]
  rw [nQuad_deriv]
  dsimp [nQuad]
  field_simp [ne_of_gt hmu]

/-- **(2, quadratic, EXACT)** the adiabatic speed dp/drho of the quadratic dust is x/(1+x) =
    (Qbar - 1)/Qbar.  DT1's value x is its leading order in x. -/
theorem cad2_quadratic (mu x : ℝ) (hmu : 0 < mu) (hQ : 1 + x ≠ 0) :
    cad2 (nQuad mu) x = x / (1 + x) := by
  dsimp [cad2]
  rw [nQuad_deriv]
  dsimp [nQuad, Qof]
  field_simp [ne_of_gt hmu, hQ]

/-- **(2, quadratic, exact w)** w = p/rho = (Qbar-1)/(Qbar+1): the equation of state is NEITHER
    c_s^2 NOR `Qbar - 1` -/
theorem eos_quadratic (mu x : ℝ) (hmu : 0 < mu) (hx : 0 < x) :
    eosw (Qof x) (nQuad mu x) (Vquad mu x) = x / (2 + x) := by
  dsimp [eosw, pressK, densK, Qof, nQuad, Vquad]
  rw [show (1 + x) * (mu ^ 2 * x) - (mu ^ 2 / 2) * x ^ 2 =
        mu ^ 2 * x * (2 + x) / 2 by ring]
  have h2 : (2 : ℝ) + x ≠ 0 := by positivity
  field_simp [ne_of_gt hmu, ne_of_gt hx, h2]

/-- **(2, correction)** the exact adiabatic speed is not w: c_ad^2 - w = x/((1+x)(2+x)), which is
    O(x): the DT1 identification w = c_s^2 holds only to leading order. -/
theorem quad_cs_minus_w (mu x : ℝ) (hmu : 0 < mu) (hx : 0 < x) :
    cad2 (nQuad mu) x - eosw (Qof x) (nQuad mu x) (Vquad mu x)
      = x / ((1 + x) * (2 + x)) := by
  have hQ : (1 : ℝ) + x ≠ 0 := by positivity
  have h2 : (2 : ℝ) + x ≠ 0 := by positivity
  rw [cad2_quadratic mu x hmu hQ, eos_quadratic mu x hmu hx]
  field_simp [hQ, h2] <;> ring_nf

/-- **(2, exponential)** DT1's ratio n/n' for n = n_* exp(x/x_T) is x_T exactly, at every epoch:
    as a RATIO it is epoch-independent, which is the sense in which the exponential term is
    isothermal. -/
theorem cs2_exponential (nstar xT x : ℝ) (hnstar : 0 < nstar) (hxT : xT ≠ 0) :
    cs2 (nExp nstar xT) x = xT := by
  dsimp [cs2]
  rw [nExp_deriv]
  dsimp [nExp]
  have hn : nstar * Real.exp (x / xT) ≠ 0 :=
    mul_ne_zero (ne_of_gt hnstar) (Real.exp_pos (x / xT)).ne'
  field_simp [hn, hxT, ne_of_gt hnstar] <;> ring_nf

/-- **(2, exponential, EXACT speed)** the adiabatic speed is x_T/Q — NOT the epoch-independent x_T -/
theorem cad2_exponential (nstar xT x : ℝ) (hnstar : 0 < nstar) (hxT : xT ≠ 0)
    (hQ : 1 + x ≠ 0) :
    cad2 (nExp nstar xT) x = xT / (1 + x) := by
  dsimp [cad2]
  rw [nExp_deriv]
  dsimp [nExp, Qof]
  have hn : nstar * Real.exp (x / xT) ≠ 0 :=
    mul_ne_zero (ne_of_gt hnstar) (Real.exp_pos (x / xT)).ne'
  field_simp [hxT, hQ, hn] <;> ring_nf

/-- **(2, exponential, exact w)** w = x_T/(Q - x_T): the exponential term is NOT exactly isothermal.
    (The premise is the positive-energy branch Q > x_T; at Q = x_T the density vanishes.) -/
theorem eos_exponential (nstar xT x : ℝ) (hnstar : 0 < nstar)
    (hden : xT < 1 + x) :
    eosw (Qof x) (nExp nstar xT x) (Vexp nstar xT x) = xT / ((1 + x) - xT) := by
  dsimp [eosw, pressK, densK, Qof, nExp, Vexp]
  rw [show (1 + x) * (nstar * Real.exp (x / xT)) - xT * (nstar * Real.exp (x / xT)) =
        ((1 + x) - xT) * (nstar * Real.exp (x / xT)) by ring]
  have hn : nstar * Real.exp (x / xT) ≠ 0 :=
    mul_ne_zero (ne_of_gt hnstar) (Real.exp_pos (x / xT)).ne'
  have hd : (1 : ℝ) + x - xT ≠ 0 := by linarith
  field_simp [hn, hd] <;> ring_nf

/-- **(2, exponential, correction)** w - c_ad^2 = x_T^2/(Q(Q - x_T)) -/
theorem exp_w_minus_cs2 (nstar xT x : ℝ) (hnstar : 0 < nstar)
    (hxT : xT ≠ 0) (hQ : 1 + x ≠ 0) (hden : xT < 1 + x) :
    eosw (Qof x) (nExp nstar xT x) (Vexp nstar xT x) -
        cad2 (nExp nstar xT) x = xT ^ 2 / ((1 + x) * ((1 + x) - xT)) := by
  rw [eos_exponential nstar xT x hnstar hden, cad2_exponential nstar xT x hnstar hxT hQ]
  have hd : (1 + x) - xT ≠ 0 := by linarith
  field_simp [hxT, hQ, hd] <;> ring_nf

/-! ## 3. the Jeans wavenumber -/

/-- **(3, quadratic)** the exact isolated-fluid Jeans wavenumber of the quadratic dust:
    k_J^2 = kappa rho / c_ad^2 = mu^2 (1 + xbar/2)(1 + xbar) -/
theorem kJ2_quadratic (mu x : ℝ) (hmu : 0 < mu) (hx : 0 < x) :
    kJ2 (Qof x) (nQuad mu x) (Vquad mu x) (cad2 (nQuad mu) x)
      = mu ^ 2 * (1 + x / 2) * (1 + x) := by
  dsimp [kJ2]
  have hQ : (1 : ℝ) + x ≠ 0 := by positivity
  rw [cad2_quadratic mu x hmu hQ]
  dsimp [densK, Qof, nQuad, Vquad]
  rw [show (1 + x) * (mu ^ 2 * x) - (mu ^ 2 / 2) * x ^ 2 =
        mu ^ 2 * x * (2 + x) / 2 by ring]
  field_simp [ne_of_gt hmu, ne_of_gt hx] <;> ring_nf

/-- **(3, quadratic, restated)** k_J^2 = mu^2 + mu^2 xbar (3+xbar)/2: DENSITY-DEPENDENT through
    xbar(a) = I0/(2 mu^2 a^3), equal to mu^2 only in the dust limit xbar -> 0. -/
theorem kJ2_quadratic_value (mu x : ℝ) (hmu : 0 < mu) (hx : 0 < x) :
    kJ2 (Qof x) (nQuad mu x) (Vquad mu x) (cad2 (nQuad mu) x)
      = mu ^ 2 + mu ^ 2 * x * (3 + x) / 2 := by
  rw [kJ2_quadratic mu x hmu hx]
  ring_nf

/-- **(3, quadratic)** along the cold branch (xbar > 0) k_J^2 is STRICTLY larger than mu^2: the
    quadratic's Jeans wavenumber is constant only to leading order. -/
theorem kJ2_quadratic_gt_mu2 (mu x : ℝ) (hmu : 0 < mu) (hx : 0 < x) :
    mu ^ 2 < kJ2 (Qof x) (nQuad mu x) (Vquad mu x) (cad2 (nQuad mu) x) := by
  rw [kJ2_quadratic_value mu x hmu hx]
  have hmu2 : 0 < mu ^ 2 := sq_pos_of_pos hmu
  have hxx : 0 < x * (3 + x) := by nlinarith
  nlinarith

/-- **(3, exponential)** the Jeans wavenumber of the exponential term is
    k_J^2 = Q(Q - x_T) n'(xbar), DENSITY-DEPENDENT through nbar -/
theorem kJ2_exponential (nstar xT x : ℝ) (hnstar : 0 < nstar) (hxT : xT ≠ 0)
    (hQ : 1 + x ≠ 0) :
    kJ2 (Qof x) (nExp nstar xT x) (Vexp nstar xT x) (cad2 (nExp nstar xT) x)
      = (1 + x) * ((1 + x) - xT) * (nExp nstar xT x / xT) := by
  dsimp [kJ2]
  rw [cad2_exponential nstar xT x hnstar hxT hQ]
  dsimp [densK, Qof, nExp, Vexp]
  field_simp [hxT, hQ] <;> ring_nf

/-- **(3, exponential)** the ratio of k_J^2 to n'(xbar) is exactly Q(Q - x_T); at Q approximately 1
    this is the advertised k_J^2 approximately n'(xbar) = nbar/x_T. -/
theorem kJ2_exponential_ratio (nstar xT x : ℝ) (hnstar : 0 < nstar)
    (hxT : xT ≠ 0) (hQ : 1 + x ≠ 0) :
    kJ2 (Qof x) (nExp nstar xT x) (Vexp nstar xT x) (cad2 (nExp nstar xT) x) /
        (nExp nstar xT x / xT) = (1 + x) * ((1 + x) - xT) := by
  rw [kJ2_exponential nstar xT x hnstar hxT hQ]
  have hn : nExp nstar xT x ≠ 0 := by
    dsimp [nExp]
    exact mul_ne_zero (ne_of_gt hnstar) (Real.exp_pos (x / xT)).ne'
  field_simp [hn, hxT] <;> ring_nf

/-! ## 4. the DT1 section 2 trade-off (discrete two-point form) -/

/-- **(4)** the two-point estimate.  If n is continuous on [x_a, x_b], differentiable on its interior,
    and n' >= k^2 there, then k^2 (x_b - x_a) <= n(x_b) - n(x_a).  Proof: g(x) := n x - k^2 x has
    g' = n' - k^2 >= 0 on the interior, hence g is monotone on the interval (mean value theorem);
    g x_a <= g x_b rearranges to the claim.

    This is the DISCRETE TWO-POINT version the lane permits.  DT1 section 2's continuum phrasing
    ("that stretch spans an offset of at most (n_b - n_a)/k^2") is the division by k^2 carried out in
    `tradeoff_span`; the integral identity `int n' = n_b - n_a` behind it is NOT formalized here. -/
theorem tradeoff_two_point {n : ℝ → ℝ} {xa xb k2 : ℝ} (hxa : xa ≤ xb)
    (hcont : ContinuousOn n (Set.Icc xa xb))
    (hdiff : DifferentiableOn ℝ n (Set.Ioo xa xb))
    (hder : ∀ y ∈ Set.Ioo xa xb, k2 ≤ deriv n y) :
    k2 * (xb - xa) ≤ n xb - n xa := by
  let g : ℝ → ℝ := fun y => n y - k2 * y
  have hgcont : ContinuousOn g (Set.Icc xa xb) := by
    dsimp [g]
    exact hcont.sub ((continuous_const.mul continuous_id).continuousOn)
  have hgdiff : DifferentiableOn ℝ g (interior (Set.Icc xa xb)) := by
    rw [interior_Icc]
    dsimp [g]
    exact hdiff.sub (by fun_prop : DifferentiableOn ℝ (fun y : ℝ => k2 * y) (Set.Ioo xa xb))
  have hgder : ∀ y ∈ interior (Set.Icc xa xb), 0 ≤ deriv g y := by
    intro y hy
    have hyn : y ∈ Set.Ioo xa xb := by simpa [interior_Icc] using hy
    have hgd : deriv g y = deriv n y - k2 := by
      change deriv ((fun z : ℝ => n z) - (fun z : ℝ => k2 * z)) y = deriv n y - k2
      rw [deriv_sub]
      · simp
      · exact (hdiff y hyn).differentiableAt (isOpen_Ioo.mem_nhds hyn)
      · fun_prop
    rw [hgd]
    linarith [hder y hyn]
  have hmono : MonotoneOn g (Set.Icc xa xb) :=
    monotoneOn_of_deriv_nonneg (convex_Icc xa xb) hgcont hgdiff hgder
  have hxain : xa ∈ Set.Icc xa xb := ⟨le_rfl, hxa⟩
  have hxbin : xb ∈ Set.Icc xa xb := ⟨hxa, le_rfl⟩
  have hg_le : g xa ≤ g xb := hmono hxain hxbin hxa
  dsimp [g] at hg_le
  linarith

/-- **(4)** the offset-span bound: the stretch carrying the background density from n_a to n_b spans
    at most (n_b - n_a)/k^2 of clock offset. -/
theorem tradeoff_span {n : ℝ → ℝ} {xa xb na nb k2 : ℝ} (hxa : xa ≤ xb) (hk : 0 < k2)
    (hcont : ContinuousOn n (Set.Icc xa xb))
    (hdiff : DifferentiableOn ℝ n (Set.Ioo xa xb))
    (hder : ∀ y ∈ Set.Ioo xa xb, k2 ≤ deriv n y)
    (hna : n xa = na) (hnb : n xb = nb) :
    xb - xa ≤ (nb - na) / k2 := by
  have h := tradeoff_two_point (n := n) (xa := xa) (xb := xb) (k2 := k2) hxa hcont hdiff hder
  rw [hna, hnb] at h
  have hmul : k2 * (xb - xa) / k2 ≤ (nb - na) / k2 :=
    div_le_div_of_nonneg_right h (le_of_lt hk)
  have hcancel : k2 * (xb - xa) / k2 = xb - xa := by
    field_simp [ne_of_gt hk]
  rwa [hcancel] at hmul

/-- **(4)** the well-cap consequence (DT1 section 2's sufficient implication).  With monotonicity
    continuing from the reference point x0 out to the well point x0 + phi, a well deeper than
    (x_a - x0) + (n_b - n_a)/k^2 holds at least n_b, so a cap n(x0 + phi) < n_b is contradictory.
    Monotonicity beyond x_b is DT2's stated extra hypothesis and is a PREMISE here, not a
    conclusion. -/
theorem tradeoff_cap_conflict {n : ℝ → ℝ} {x0 xa xb na nb k2 phi : ℝ}
    (hx0 : x0 ≤ xa) (hxx : xa ≤ xb) (hk : 0 < k2)
    (hcont : ContinuousOn n (Set.Icc xa xb))
    (hdiff : DifferentiableOn ℝ n (Set.Ioo xa xb))
    (hder : ∀ y ∈ Set.Ioo xa xb, k2 ≤ deriv n y)
    (hmono : MonotoneOn n (Set.Icc x0 (x0 + phi)))
    (hphi : (xa - x0) + (nb - na) / k2 < phi)
    (hna : n xa = na) (hnb : n xb = nb) (hcap : n (x0 + phi) < nb) : False := by
  have hspan := tradeoff_span (n := n) (xa := xa) (xb := xb) (na := na) (nb := nb) (k2 := k2)
    hxx hk hcont hdiff hder hna hnb
  have hxb_le : xb ≤ x0 + phi := by linarith
  have hx0_le_xb : x0 ≤ xb := le_trans hx0 hxx
  have hxbin' : xb ∈ Set.Icc x0 (x0 + phi) := ⟨hx0_le_xb, hxb_le⟩
  have hwellin : x0 + phi ∈ Set.Icc x0 (x0 + phi) := ⟨by linarith, le_rfl⟩
  have hle : n xb ≤ n (x0 + phi) := hmono hxbin' hwellin hxb_le
  rw [hnb] at hle
  linarith

/-! ## 5. budget exhaustion -/

/-- the budget function solves its defining quadratic X(1+X) = x^2, unconditionally -/
theorem budgetX_identity (x : ℝ) : budgetX x * (1 + budgetX x) = x ^ 2 := by
  dsimp [budgetX]
  set S := Real.sqrt (1 + 4 * x ^ 2) with hS
  have hSsq : S ^ 2 = 1 + 4 * x ^ 2 := by
    rw [hS]
    exact Real.sq_sqrt (by positivity : (0 : ℝ) ≤ 1 + 4 * x ^ 2)
  rw [show ((S - 1) / 2) * (1 + (S - 1) / 2) = (S ^ 2 - 1) / 4 by ring]
  rw [hSsq]
  ring

/-- the budget function is the NON-NEGATIVE branch -/
theorem budgetX_nonneg (x : ℝ) : 0 ≤ budgetX x := by
  dsimp [budgetX]
  have h1 : (1 : ℝ) ≤ Real.sqrt (1 + 4 * x ^ 2) := by
    have hsq : (1 : ℝ) ^ 2 ≤ 1 + 4 * x ^ 2 := by nlinarith [sq_nonneg x]
    have h := Real.sqrt_le_sqrt hsq
    simpa [Real.sqrt_one] using h
  linarith

/-- uniqueness: any non-negative solution of u(1+u) = x^2 IS the budget function, so the branch
    convention (which root of the quadratic one calls X) is immaterial -/
theorem budget_char (x u : ℝ) (hu : 0 ≤ u) (huid : u * (1 + u) = x ^ 2) :
    u = budgetX x := by
  let X := budgetX x
  have hX0 : 0 ≤ X := by
    dsimp [X]
    exact budgetX_nonneg x
  have hXid : X * (1 + X) = x ^ 2 := by
    dsimp [X]
    exact budgetX_identity x
  have hprod : (u - X) * (u + X + 1) = 0 := by
    nlinarith [huid, hXid]
  have hpos : 0 < u + X + 1 := by nlinarith
  have hs : u - X = 0 := by
    rcases mul_eq_zero.mp hprod with h | h
    · exact h
    · exfalso
      nlinarith
  dsimp [X] at hs
  linarith

/-- **(5)** budget exhaustion: X(x) = R_b iff x = x_b = sqrt(R_b(1+R_b)), for x >= 0 and R_b > 0 -/
theorem budget_exhaustion_iff (x Rb : ℝ) (hx : 0 ≤ x) (hR : 0 < Rb) :
    budgetX x = Rb ↔ x = xBudget Rb := by
  constructor
  · intro h
    have hident : Rb * (1 + Rb) = x ^ 2 := by
      simpa [h] using budgetX_identity x
    calc x = Real.sqrt (x ^ 2) := by
          rw [Real.sqrt_sq_eq_abs, abs_of_nonneg hx]
        _ = Real.sqrt (Rb * (1 + Rb)) := by rw [hident]
        _ = xBudget Rb := by rfl
  · intro hx_eq
    have hx2 : x ^ 2 = Rb * (1 + Rb) := by
      rw [hx_eq]
      dsimp [xBudget]
      exact Real.sq_sqrt (by positivity : (0 : ℝ) ≤ Rb * (1 + Rb))
    have huid : Rb * (1 + Rb) = x ^ 2 := hx2.symm
    exact (budget_char x Rb (le_of_lt hR) huid).symm

/-- **(5)** the budget point really does exhaust the budget -/
theorem budget_exhaustion_at_xb (Rb : ℝ) (hR : 0 < Rb) :
    budgetX (xBudget Rb) = Rb := by
  exact (budget_exhaustion_iff (xBudget Rb) Rb
    (Real.sqrt_nonneg (Rb * (1 + Rb))) hR).2 rfl

end FINAL12
end

#print axioms FINAL12.Vquad_deriv
#print axioms FINAL12.quad_background
#print axioms FINAL12.frw_eos_quadratic
#print axioms FINAL12.wFRW_lt_half_iff
#print axioms FINAL12.wFRW_strictly_decreasing
#print axioms FINAL12.one_lt_cube
#print axioms FINAL12.wFRW_tendsto_zero
#print axioms FINAL12.nQuad_deriv
#print axioms FINAL12.nExp_deriv
#print axioms FINAL12.cs2_quadratic
#print axioms FINAL12.cad2_quadratic
#print axioms FINAL12.eos_quadratic
#print axioms FINAL12.quad_cs_minus_w
#print axioms FINAL12.cs2_exponential
#print axioms FINAL12.cad2_exponential
#print axioms FINAL12.eos_exponential
#print axioms FINAL12.exp_w_minus_cs2
#print axioms FINAL12.kJ2_quadratic
#print axioms FINAL12.kJ2_quadratic_value
#print axioms FINAL12.kJ2_quadratic_gt_mu2
#print axioms FINAL12.kJ2_exponential
#print axioms FINAL12.kJ2_exponential_ratio
#print axioms FINAL12.tradeoff_two_point
#print axioms FINAL12.tradeoff_span
#print axioms FINAL12.tradeoff_cap_conflict
#print axioms FINAL12.budgetX_identity
#print axioms FINAL12.budgetX_nonneg
#print axioms FINAL12.budget_char
#print axioms FINAL12.budget_exhaustion_iff
#print axioms FINAL12.budget_exhaustion_at_xb
