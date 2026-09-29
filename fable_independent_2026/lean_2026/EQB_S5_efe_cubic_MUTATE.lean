import Mathlib

/-!
# EQB_S5 -- the external-field cubic and the attenuated a0-line (Lean 4 certificate)

Source (committed): `prep_2026/equation_book/eqbook_S5_efe.py`, checks E-S5.1 (cubic, lines 57-78), E-S5.2 (attenuated a0-line,
lines 80-84), E-S5.3 (half-quench locus, lines 86-91), E-S5.4 (susceptibility, lines 93-104); write-up `MINE_M1.md` item 3.

PREMISES (declared, NOT certified as physics): the worldline inertia dressing
    mu(t) = (sqrt(1 + 4 t^2) - 1) / (2 t)          (the exact inverse of nu(y) = sqrt(1 + 1/y)),
and the internal force balance  mu(A) * g_int = g_bar  with  A = g_int + e a0  (dimensionless: x = g_int/a0, b = g_bar/a0, A = x + e).
The script takes e = sqrt 2 * g_ext / a0 (the "DC weight sqrt 2" of the dS Wightman kernel, BASELINE_ACTION.md:49); here e >= 0 is
an ARBITRARY parameter, so the certificate does not depend on the value sqrt 2, nor on that postulate.

CERTIFIED (premises => conclusions):
  * `efe_balance_iff_line` : for x > 0, e >= 0, b >= 0:  x * mu(x + e) = b  <->  (x^2 - b^2)(x + e) = b x
                             (the attenuated a0-line; the squaring step is reversible because both sides are positive)
  * `efe_cubic_eq`         : (x^2 - b^2)(x + e) - b x = x^3 + e x^2 - b(b+1) x - b^2 e   (the EFE cubic)
  * `efe_isolated`         : e = 0 recovers x^2 = b^2 + b
  * `efe_attenuation`      : from the line, x^2 - b^2 = b * (x/(x+e)) : the isolated excess times an exact attenuation factor
  * `efe_half_quench`      : (b > 0) the excess equals half the isolated excess iff e = x
  * `efe_root_unique`      : for any real b and e >= 0 the cubic has at most one positive root (F(x)/x is strictly increasing)
  * `efe_susceptibility`   : if a differentiable family x(e) solves the cubic near e = 0 with x(0) = sqrt(b^2 + b), then
                             x'(0) = -1/(2(b+1)); bounds -1/2 < -1/(2(b+1)) < 0 for b > 0 (deep-MOND -1/2, Newtonian -> 0)
NOT certified: existence of a positive root (the script's Cardano branch is numeric); the value or origin of the weight sqrt 2; the
aligned-scalar composition A = g_int + e a0 (a framework usage, flagged in the script); the external-dominated series (E-S5.6);
any data.  kappa = 1/2 (FITTED) does not enter.
-/

open Real

noncomputable section

/-- the framework inertia dressing, exact inverse of nu(y) = sqrt(1 + 1/y). -/
def mu (t : ℝ) : ℝ := (Real.sqrt (1 + 4 * t ^ 2) - 1) / (2 * t)

/-- the EFE cubic polynomial. -/
def efeF (b e x : ℝ) : ℝ := x ^ 3 + e * x ^ 2 - b * (b + 1) * x - b ^ 2 * e

theorem efe_cubic_eq (b e x : ℝ) : (x ^ 2 - b ^ 2) * (x + e) - b * x = efeF b e x := by
  unfold efeF; ring

theorem efe_balance_iff_line {x e b : ℝ} (hx : 0 < x) (he : 0 ≤ e) (hb : 0 ≤ b) :
    x * mu (x + e) = b ↔ (x ^ 2 - b ^ 2) * (x + e) = b * x := by
  have hA : 0 < x + e := by linarith
  set A := x + e with hAdef
  set s := Real.sqrt (1 + 4 * A ^ 2) with hs
  have hs2 : s ^ 2 = 1 + 4 * A ^ 2 := Real.sq_sqrt (by positivity)
  have hs0 : 0 ≤ s := Real.sqrt_nonneg _
  have key : x * mu A = b ↔ x * s = 2 * A * b + x := by
    unfold mu
    rw [← hs]
    constructor
    · intro h
      field_simp at h
      linarith
    · intro h
      field_simp
      linarith
  rw [key]
  constructor
  · intro h
    have h2 : (x * s) ^ 2 = (2 * A * b + x) ^ 2 := by rw [h]
    have : (x * s) ^ 2 = x ^ 2 * (1 + 4 * A ^ 2) := by rw [mul_pow, hs2]
    rw [this] at h2
    have h3 : 4 * A * ((x ^ 2 - b ^ 2) * A - b * x) = 0 := by nlinarith
    have hA4 : 4 * A ≠ 0 := by positivity
    have := (mul_eq_zero.mp h3).resolve_left hA4
    linarith
  · intro h
    have h2 : (x * s) ^ 2 = (2 * A * b + x) ^ 2 := by
      have : (x * s) ^ 2 = x ^ 2 * (1 + 4 * A ^ 2) := by rw [mul_pow, hs2]
      rw [this]; nlinarith
    have hl : 0 ≤ x * s := by positivity
    have hr : 0 ≤ 2 * A * b + x := by positivity
    exact (sq_eq_sq₀ hl hr).mp h2

theorem efe_isolated {x b : ℝ} (hx : 0 < x) (hb : 0 ≤ b) :
    x * mu x = b ↔ x ^ 2 = b ^ 2 + 2 * b := by
  have := efe_balance_iff_line (e := 0) hx le_rfl hb
  simp only [add_zero] at this
  rw [this]
  constructor
  · intro h
    have : x * (x ^ 2 - b ^ 2 - b) = 0 := by nlinarith
    have := (mul_eq_zero.mp this).resolve_left hx.ne'
    linarith
  · intro h; rw [h]; ring

theorem efe_attenuation {x e b : ℝ} (hx : 0 < x) (he : 0 ≤ e)
    (h : (x ^ 2 - b ^ 2) * (x + e) = b * x) : x ^ 2 - b ^ 2 = b * (x / (x + e)) := by
  have hA : x + e ≠ 0 := by linarith
  field_simp
  linarith

theorem efe_half_quench {x e b : ℝ} (hx : 0 < x) (he : 0 ≤ e) (hb : 0 < b)
    (h : (x ^ 2 - b ^ 2) * (x + e) = b * x) : x ^ 2 - b ^ 2 = b / 2 ↔ e = x := by
  have hA : 0 < x + e := by linarith
  constructor
  · intro h1
    rw [h1] at h
    have : b * (x + e) = 2 * (b * x) := by linarith
    have : b * (e - x) = 0 := by nlinarith
    have := (mul_eq_zero.mp this).resolve_left hb.ne'
    linarith
  · intro h1
    rw [h1] at h
    have h2 : x * (2 * (x ^ 2 - b ^ 2) - b) = 0 := by nlinarith
    have := (mul_eq_zero.mp h2).resolve_left hx.ne'
    linarith

/-- at most one positive root of the EFE cubic (Descartes: G(x) = F(x)/x is strictly increasing). -/
theorem efe_root_unique {b e x₁ x₂ : ℝ} (he : 0 ≤ e) (h1 : 0 < x₁) (h2 : 0 < x₂)
    (r1 : efeF b e x₁ = 0) (r2 : efeF b e x₂ = 0) : x₁ = x₂ := by
  have G : ∀ x : ℝ, 0 < x → efeF b e x / x = x ^ 2 + e * x - b * (b + 1) - b ^ 2 * e / x := by
    intro x hx; unfold efeF; field_simp
  have mono : ∀ u v : ℝ, 0 < u → u < v →
      u ^ 2 + e * u - b * (b + 1) - b ^ 2 * e / u < v ^ 2 + e * v - b * (b + 1) - b ^ 2 * e / v := by
    intro u v hu huv
    have hv : 0 < v := lt_trans hu huv
    have h3 : b ^ 2 * e / v ≤ b ^ 2 * e / u := by
      apply div_le_div_of_nonneg_left (by positivity) hu huv.le
    have h4 : u ^ 2 < v ^ 2 := by nlinarith
    nlinarith
  have e1 := G x₁ h1
  have e2 := G x₂ h2
  rw [r1, zero_div] at e1
  rw [r2, zero_div] at e2
  by_contra hne
  rcases lt_or_gt_of_ne hne with hlt | hgt
  · have := mono x₁ x₂ h1 hlt
    linarith
  · have := mono x₂ x₁ h2 hgt
    linarith

theorem efe_susceptibility {b : ℝ} (hb : 0 < b) (xf : ℝ → ℝ) (d : ℝ)
    (hd : HasDerivAt xf d 0) (h0 : xf 0 = Real.sqrt (b ^ 2 + b))
    (hsol : ∀ᶠ e in nhds (0 : ℝ), efeF b e (xf e) = 0) :
    d = -1 / (2 * (b + 1)) := by
  have hsq : Real.sqrt (b ^ 2 + b) ^ 2 = b ^ 2 + b := Real.sq_sqrt (by positivity)
  -- derivative of e ↦ F(b, e, x(e))
  have hx3 : HasDerivAt (fun e => xf e ^ 3) (3 * xf 0 ^ 2 * d) 0 := by
    have h := hd.pow 3
    exact h.congr_deriv (by simp)
  have hx2 : HasDerivAt (fun e => xf e ^ 2) (2 * xf 0 * d) 0 := by
    have h := hd.pow 2
    exact h.congr_deriv (by simp)
  have hex2 : HasDerivAt (fun e : ℝ => e * xf e ^ 2) (1 * xf 0 ^ 2 + 0 * (2 * xf 0 * d)) 0 :=
    (hasDerivAt_id (0 : ℝ)).mul hx2 |>.congr_deriv (by simp)
  have hphi : HasDerivAt (fun e => efeF b e (xf e))
      (3 * xf 0 ^ 2 * d + (1 * xf 0 ^ 2 + 0 * (2 * xf 0 * d)) - b * (b + 1) * d - b ^ 2) 0 := by
    have hlin : HasDerivAt (fun e => b * (b + 1) * xf e) (b * (b + 1) * d) 0 := hd.const_mul _
    have hlin2 : HasDerivAt (fun e : ℝ => b ^ 2 * e) (b ^ 2 * 1) 0 :=
      (hasDerivAt_id (0 : ℝ)).const_mul _
    have := ((hx3.add hex2).sub hlin).sub hlin2
    unfold efeF
    exact this.congr_deriv (by ring)
  have hzero : HasDerivAt (fun e : ℝ => efeF b e (xf e)) 0 0 := by
    have hc : HasDerivAt (fun _ : ℝ => (0 : ℝ)) 0 0 := hasDerivAt_const _ _
    exact hc.congr_of_eventuallyEq (hsol.mono fun e he => he)
  have huniq := hphi.unique hzero
  rw [h0] at huniq
  have hxsq : Real.sqrt (b ^ 2 + b) ^ 2 = b ^ 2 + b := hsq
  have hb1 : b + 1 ≠ 0 := by positivity
  have : 2 * b * (b + 1) * d + b = 0 := by nlinarith
  field_simp
  have hb0 : b ≠ 0 := hb.ne'
  have : b * (2 * (b + 1) * d + 1) = 0 := by linarith
  have := (mul_eq_zero.mp this).resolve_left hb0
  linarith

theorem efe_susceptibility_bounds {b : ℝ} (hb : 0 < b) :
    -(1 / 2) < -1 / (2 * (b + 1)) ∧ -1 / (2 * (b + 1)) < 0 := by
  have hp : 0 < 2 * (b + 1) := by positivity
  constructor
  · rw [neg_div, neg_lt_neg_iff, div_lt_div_iff₀ hp (by norm_num)]
    nlinarith
  · exact div_neg_of_neg_of_pos (by norm_num) hp

end

#print axioms efe_cubic_eq
#print axioms efe_balance_iff_line
#print axioms efe_isolated
#print axioms efe_attenuation
#print axioms efe_half_quench
#print axioms efe_root_unique
#print axioms efe_susceptibility
#print axioms efe_susceptibility_bounds
