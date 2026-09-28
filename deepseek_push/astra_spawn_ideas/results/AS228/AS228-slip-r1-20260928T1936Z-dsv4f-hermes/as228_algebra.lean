import Mathlib

/-!
# AS228 algebraic certificate

Certifies the pure-algebra identities that the numerics rely on:

1. the frozen convex gate ramp  G(r) = Δ(7r⁵ − 14r⁶ + 10r⁷ − (5/2)r⁸),
   its derivative  f(r) = G′(r) = Δ(35r⁴ − 84r⁵ + 70r⁶ − 20r⁷),
   and the boundary closures G(0) = 0, G(1) = Δ/2, f(0) = 0, f(1) = Δ;
2. the RAR / MONO-kernel algebra: for ν(y) = 1/(1 − e^{−s}), s = √y:
   ν(y) − 1 = 1/(e^s − 1)  and  h(y) = y·(ν(y) − 1) = y/(e^{√y} − 1);
3. the slip-source bracket expansion (g1 + g2 − g4) with
   g1 = c_N f [4(ν−1)|p|² + 2ℓΔW],  g2 = 2 c_N ℓ (DΦ·DW),
   g4 = c_N [G(Y_h) − ℓΔW];
4. the vanishing-gate / vanishing-coupling limits of the slip source.

No sorry.  Axiom bar: {propext, Classical.choice, Quot.sound}.
-/

noncomputable section
open scoped Real
open Filter

/-- Gate ramp G(r) = Δ·(7r⁵ − 14r⁶ + 10r⁷ − (5/2)r⁸) (FINAL_ACTION gate). -/
def ramp (d r : ℝ) : ℝ := d * (7 * r ^ 5 - 14 * r ^ 6 + 10 * r ^ 7 - (5 / 2 : ℝ) * r ^ 8)

/-- Ramp derivative f(r) = G′(r) = Δ·(35r⁴ − 84r⁵ + 70r⁶ − 20r⁷). -/
def rampDeriv (d r : ℝ) : ℝ := d * (35 * r ^ 4 - 84 * r ^ 5 + 70 * r ^ 6 - 20 * r ^ 7)

-- ---------------------------------------------------------------- gate ramp --

lemma ramp_hasDerivAt (d r : ℝ) :
    HasDerivAt (fun x : ℝ => ramp d x) (rampDeriv d r) r := by
  have h1 : HasDerivAt (fun x : ℝ => (7 : ℝ) * x ^ 5) (7 * (5 * r ^ 4)) r := by
    exact HasDerivAt.const_mul 7 (hasDerivAt_pow 5 r)
  have h2 : HasDerivAt (fun x : ℝ => (14 : ℝ) * x ^ 6) (14 * (6 * r ^ 5)) r := by
    exact HasDerivAt.const_mul 14 (hasDerivAt_pow 6 r)
  have h3 : HasDerivAt (fun x : ℝ => (10 : ℝ) * x ^ 7) (10 * (7 * r ^ 6)) r := by
    exact HasDerivAt.const_mul 10 (hasDerivAt_pow 7 r)
  have h4 : HasDerivAt (fun x : ℝ => (5 / 2 : ℝ) * x ^ 8) ((5 / 2 : ℝ) * (8 * r ^ 7)) r := by
    exact HasDerivAt.const_mul (5 / 2 : ℝ) (hasDerivAt_pow 8 r)
  have hh := ((h1.sub h2).add h3).sub h4
  have hd : HasDerivAt
      (fun x : ℝ => d * (7 * x ^ 5 - 14 * x ^ 6 + 10 * x ^ 7 - (5 / 2 : ℝ) * x ^ 8))
      (d * (7 * (5 * r ^ 4) - 14 * (6 * r ^ 5) + 10 * (7 * r ^ 6) - (5 / 2 : ℝ) * (8 * r ^ 7))) r := by
    simpa using hh.const_mul d
  have hEq : d * (7 * (5 * r ^ 4) - 14 * (6 * r ^ 5) + 10 * (7 * r ^ 6) - (5 / 2 : ℝ) * (8 * r ^ 7))
      = d * (35 * r ^ 4 - 84 * r ^ 5 + 70 * r ^ 6 - 20 * r ^ 7) := by
    ring
  have hd2 : HasDerivAt (fun x : ℝ => ramp d x)
      (d * (35 * r ^ 4 - 84 * r ^ 5 + 70 * r ^ 6 - 20 * r ^ 7)) r := by
    simpa [ramp, hEq] using hd
  simpa [rampDeriv] using hd2

lemma ramp_deriv_eq (d r : ℝ) : deriv (fun x : ℝ => ramp d x) r = rampDeriv d r := by
  have hf : ∀ x : ℝ, HasDerivAt (fun y : ℝ => ramp d y) (rampDeriv d x) x := by
    intro x
    exact ramp_hasDerivAt d x
  simpa using congrFun (deriv_eq hf) r

lemma ramp_zero (d : ℝ) : ramp d 0 = 0 := by
  simp [ramp]

lemma ramp_one (d : ℝ) : ramp d 1 = (1 / 2 : ℝ) * d := by
  norm_num [ramp]
  ring

lemma rampDeriv_zero (d : ℝ) : rampDeriv d 0 = 0 := by
  simp [rampDeriv]

lemma rampDeriv_one (d : ℝ) : rampDeriv d 1 = d := by
  norm_num [rampDeriv]

-- ------------------------------------------------- kernel / RAR algebra --

lemma exp_neg_ne_one {s : ℝ} (hs : s ≠ 0) : Real.exp (-s) ≠ 1 := by
  intro h
  have harg : -s = 0 := Real.exp_strictMono.injective (by simpa using h)
  have hs' : s = 0 := by linarith
  exact hs hs'

lemma exp_ne_one {s : ℝ} (hs : s ≠ 0) : Real.exp s ≠ 1 := by
  intro h
  have harg : s = 0 := Real.exp_strictMono.injective (by simpa using h)
  exact hs harg

lemma exp_neg_mul_exp (s : ℝ) : Real.exp (-s) * Real.exp s = 1 := by
  rw [← Real.exp_add, neg_add_cancel, Real.exp_zero]

/-- ν(y) − 1 = 1/(e^s − 1),  s = √y: the RAR kernel core. -/
lemma rar_nu_minus_one {s : ℝ} (hs : s ≠ 0) :
    (1 - Real.exp (-s))⁻¹ - 1 = 1 / (Real.exp s - 1) := by
  have hcore : 1 - Real.exp (-s) ≠ 0 := sub_ne_zero.mpr (exp_neg_ne_one hs).symm
  have hne : Real.exp s - 1 ≠ 0 := sub_ne_zero.mpr (exp_ne_one hs)
  calc
    (1 - Real.exp (-s))⁻¹ - 1 = Real.exp (-s) / (1 - Real.exp (-s)) := by
      field_simp [hcore]
      ring
    _ = 1 / (Real.exp s - 1) := by
      field_simp [hcore, hne]
      ring_nf
      rw [exp_neg_mul_exp]
      ring

lemma rar_nu_minus_one' {s : ℝ} (hs : s ≠ 0) :
    (1 - Real.exp (-s))⁻¹ - 1 = (Real.exp s - 1)⁻¹ := by
  simpa [div_eq_mul_inv] using (rar_nu_minus_one hs)

/-- h(y) = y·(ν(y) − 1): the quadrature identity with h = y/(e^{√y} − 1). -/
lemma rar_h_eq_y_mul_nu_minus_one {y : ℝ} (hy : 0 < y) :
    y * ((1 - Real.exp (-Real.sqrt y))⁻¹ - 1) = y / (Real.exp (Real.sqrt y) - 1) := by
  have hs : Real.sqrt y ≠ 0 := ne_of_gt (Real.sqrt_pos.2 hy)
  rw [rar_nu_minus_one hs]
  simp [div_eq_mul_inv]

/-- exp(−s)/(1 − exp(−s)) = 1/(exp(s) − 1): equivalent ν-form used by the
    MONO branch at large y. -/
lemma rar_exp_form {s : ℝ} (hs : s ≠ 0) :
    Real.exp (-s) / (1 - Real.exp (-s)) = 1 / (Real.exp s - 1) := by
  have hcore : 1 - Real.exp (-s) ≠ 0 := sub_ne_zero.mpr (exp_neg_ne_one hs).symm
  have h : (1 - Real.exp (-s))⁻¹ - 1 = Real.exp (-s) / (1 - Real.exp (-s)) := by
    field_simp [hcore]
    ring
  rw [← h]
  exact rar_nu_minus_one hs

-- ------------------------------------------------ slip-source bracket (g1+g2−g4) --

/-- The slip-source bracket as evaluated in the numerics:
    rho_slip ∝ c_N·f·(4(ν−1)n2 + 2ℓΔW) + 2c_N·ℓ·(DΦ·DW) − c_N·(G − ℓΔW).
    Certifies the regrouping into the reported coefficient table. -/
lemma slip_source_bracket (c f nu n2 ell dw dpdw g : ℝ) :
    c * f * (4 * (nu - 1) * n2 + 2 * ell * dw) + 2 * c * ell * dpdw - c * (g - ell * dw)
      = c * (4 * f * (nu - 1) * n2 + 2 * f * ell * dw + 2 * ell * dpdw - g + ell * dw) := by
  ring

/-- Vanishing-gate limit: at f = 0 the slip source collapses to the
    ℓ-coupling remainder. -/
lemma slip_source_gate_zero (c nu n2 ℓ dw dpdw g : ℝ) :
    c * 0 * (4 * (nu - 1) * n2 + 2 * ℓ * dw) + 2 * c * ℓ * dpdw - c * (g - ℓ * dw)
      = 2 * c * ℓ * dpdw - c * (g - ℓ * dw) := by
  ring

/-- Vanishing-coupling limit: at ℓ = 0 the slip source is the gate trace
    stress alone. -/
lemma slip_source_coupling_zero (c f nu n2 dw dpdw g : ℝ) :
    c * f * (4 * (nu - 1) * n2 + 2 * 0 * dw) + 2 * c * 0 * dpdw - c * (g - 0 * dw)
      = c * f * (4 * (nu - 1) * n2) - c * g := by
  ring

-- ------------------------------------------------------------- sanity block --

/-- Gate ramp closure at the threshold and its endpoints, grid units. -/
example (ELL : ℝ) : ramp ELL 1 = (1 / 2 : ℝ) * ELL ∧ ramp ELL 0 = 0 ∧
    rampDeriv ELL 1 = ELL ∧ rampDeriv ELL 0 = 0 := by
  constructor
  · exact ramp_one ELL
  constructor
  · exact ramp_zero ELL
  constructor
  · exact rampDeriv_one ELL
  · exact rampDeriv_zero ELL

/-- RAR: at s = 1: ν − 1 = 1/(e − 1); algebra-only statement. -/
example : (1 - Real.exp (-1))⁻¹ - 1 = 1 / (Real.exp 1 - 1) := by
  exact rar_nu_minus_one (by norm_num : (1 : ℝ) ≠ 0)

end