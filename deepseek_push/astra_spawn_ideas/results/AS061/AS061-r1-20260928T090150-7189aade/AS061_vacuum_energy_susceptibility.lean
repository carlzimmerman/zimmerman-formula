import Mathlib
import Mathlib.Tactic

/-
  AS061 -- Vacuum energy does not fix linear susceptibility (Lean 4 certificate).

  Static scalar-kinetic functional (PD08 particle-free class):
      S = (1/8 pi G) INT s^2 K(|grad Phi|^2/s^2) d^3x - INT rho_b Phi d^3x
      K(X) = C0 + eps*X + alpha*X*sqrt(X),   s = c sqrt(G rho_L),  alpha > 0.

  Formalized content (all on the CORE coefficient lane, group A03):
    A  flux on the positive drive axis: flux(C0,eps,alpha,Y) = eps + (3/2) alpha Y
       for Y >= 0, where flux := eps + (3/2) alpha sqrt(Y^2) is the response
       mu(Y) = K'(Y^2).
    B  zero-gradient response: flux(...,0) = eps  (the linear susceptibility).
    C  C0-independence: the flux does not depend on the vacuum-energy constant C0
       at any Y (the field equations cannot see the vacuum energy; k01 K1 mirror).
    D  NEGATIVE CONTROL (task-mandated): C0 = 0, eps = 1  ->  K(0) = 0  AND
       mu(0) = 1  AND  (1 : R) != 0: the vacuum primitive vanishes but the linear
       Newtonian response remains nonzero.  (A reverse control: eps = 0, C0 = 1
       gives K(0) = 1 != 0 with mu(0) = 0.)
    E  the calculus step: K is differentiable at every X > 0 with
       K'(X) = eps + (3/2) alpha sqrt(X)  (no C0), and at X = 0 with K'(0) = eps.
    F  deep-line matching algebra: for a = 2s/(3 alpha), the constitutive law
       g * ((3/2) alpha (g/s)) = g_N  is equivalent to  a * g_N = g^2
       (the X^(3/2) coefficient alone sets the a0-line: g^2 = a_deep g_N).
    G  the adopted footing: a_deep = s/2  <->  alpha = 4/3  (kappa = 1/2 fixed;
       this pins the DEEP COEFFICIENT, not eps and not C0).
-/

noncomputable section
open scoped Topology
open Filter
open Real

/-- The kinetic function K(X) = C0 + eps*X + alpha*X*sqrt(X) on the gradient
    invariant X = |grad Phi|^2/s^2. -/
def Kfun (C0 eps alpha : ℝ) (X : ℝ) : ℝ :=
  C0 + eps * X + alpha * (X * Real.sqrt X)

/-- The response (flux coefficient) mu(Y) = K'(Y^2) = eps + (3/2) alpha sqrt(Y^2). -/
def flux (C0 eps alpha : ℝ) (Y : ℝ) : ℝ :=
  eps + (3 / 2 : ℝ) * alpha * Real.sqrt (Y ^ 2)

/- A: flux on the positive drive axis. -/
lemma flux_eq_of_nonneg {_C0 eps alpha Y : ℝ} (hY : 0 ≤ Y) :
    flux _C0 eps alpha Y = eps + (3 / 2 : ℝ) * alpha * Y := by
  unfold flux
  rw [Real.sqrt_sq hY]

/- B: zero-gradient response is the linear susceptibility eps. -/
lemma flux_zero (C0 eps alpha : ℝ) : flux C0 eps alpha 0 = eps := by
  unfold flux
  simp [Real.sqrt_zero]

/- B': the seed's other half: K(0) = C0. -/
lemma K_at_zero (C0 eps alpha : ℝ) : Kfun C0 eps alpha 0 = C0 := by
  unfold Kfun
  simp [Real.sqrt_zero]

/- C: the response does not depend on the vacuum-energy constant C0 at any Y. -/
lemma flux_indep_C0 (C0 C0' eps alpha Y : ℝ) : flux C0 eps alpha Y = flux C0' eps alpha Y := by
  unfold flux
  ring

/- D: NEGATIVE CONTROL (task-mandated): zero vacuum energy, nonzero linear response. -/
theorem control_zero_vac_nonzero_lin :
    Kfun 0 1 (1 : ℝ) 0 = 0 ∧ flux 0 1 (1 : ℝ) 0 = 1 ∧ (1 : ℝ) ≠ 0 := by
  constructor
  · exact K_at_zero 0 1 1
  · constructor
    · exact flux_zero 0 1 1
    · norm_num

/- D': reverse control: degenerate susceptibility is not zero vacuum energy. -/
theorem control_reverse_nondegenerate_vac :
    Kfun 1 0 (1 : ℝ) 0 = 1 ∧ flux 1 0 (1 : ℝ) 0 = 0 := by
  constructor
  · exact K_at_zero 1 0 1
  · exact flux_zero 1 0 1

/- E1: the calculus step at X > 0: K'(X) = eps + (3/2) alpha sqrt(X), no C0. -/
lemma K_hasDerivAt_pos {C0 eps alpha x : ℝ} (hx : 0 < x) :
    HasDerivAt (fun X : ℝ => Kfun C0 eps alpha X) (eps + (3 / 2 : ℝ) * alpha * Real.sqrt x) x := by
  have h_id : HasDerivAt (fun X : ℝ => eps * X) eps x := by
    simpa using (hasDerivAt_id x).const_mul eps
  have hlin : HasDerivAt (fun X : ℝ => C0 + eps * X) eps x := by
    simpa using h_id.const_add C0
  have hsqrt : HasDerivAt (fun X : ℝ => X * Real.sqrt X) ((3 / 2 : ℝ) * Real.sqrt x) x := by
    have hsq : Real.sqrt x * Real.sqrt x = x := Real.mul_self_sqrt (le_of_lt hx)
    have hsq2 : Real.sqrt x ^ 2 = x := by simpa [pow_two] using hsq
    have hden : (2 * Real.sqrt x) ≠ 0 := by positivity
    have hderiv : 1 * Real.sqrt x + id x * (1 / (2 * Real.sqrt x)) = (3 / 2 : ℝ) * Real.sqrt x := by
      simp [one_mul, id]
      field_simp [hden]
      rw [hsq2]
      ring_nf
    have hd_raw := (hasDerivAt_id x).mul (hasDerivAt_sqrt hx.ne')
    rw [hderiv] at hd_raw
    convert hd_raw using 3
    all_goals first
      | simp [Pi.mul_apply, id]
      | rfl
      | ring_nf
  have hquad : HasDerivAt (fun X : ℝ => alpha * (X * Real.sqrt X))
      (alpha * ((3 / 2 : ℝ) * Real.sqrt x)) x := hsqrt.const_mul alpha
  have hderiv2 : eps + alpha * ((3 / 2 : ℝ) * Real.sqrt x) =
      eps + (3 / 2 : ℝ) * alpha * Real.sqrt x := by
    ring_nf
  have hadd := hlin.add hquad
  rw [hderiv2] at hadd
  convert hadd using 3
  all_goals first
    | simp [Kfun, Pi.add_apply]
    | rfl
    | ring_nf

/- E2: the calculus step at X = 0: K'(0) = eps (the "but K_X(0) = eps" clause). -/
lemma x_mul_sqrt_hasDerivAt_zero : HasDerivAt (fun X : ℝ => X * Real.sqrt X) 0 0 := by
  rw [hasDerivAt_iff_tendsto]
  have hEq : (fun y : ℝ =>
        ‖y - 0‖⁻¹ * ‖y * Real.sqrt y - 0 * Real.sqrt 0 - (y - 0) • (0 : ℝ)‖) =ᶠ[𝓝 (0 : ℝ)]
      (fun y : ℝ => ‖Real.sqrt y‖) := by
    apply Filter.Eventually.of_forall
    intro y
    by_cases hy : y = 0
    · simp [hy]
    · simp [hy]
  have hsqrt_tendsto : Tendsto (fun y : ℝ => ‖Real.sqrt y‖) (𝓝 (0 : ℝ)) (𝓝 0) := by
    have hc : ContinuousAt (fun y : ℝ => ‖Real.sqrt y‖) (0 : ℝ) :=
      Real.continuous_sqrt.continuousAt.norm
    simpa [Real.sqrt_zero] using hc.tendsto
  exact Tendsto.congr' hEq.symm hsqrt_tendsto

lemma K_hasDerivAt_zero {C0 eps alpha : ℝ} :
    HasDerivAt (fun X : ℝ => Kfun C0 eps alpha X) eps 0 := by
  have h_id : HasDerivAt (fun X : ℝ => eps * X) eps 0 := by
    simpa using (hasDerivAt_id 0).const_mul eps
  have hlin : HasDerivAt (fun X : ℝ => C0 + eps * X) eps 0 := by
    simpa using h_id.const_add C0
  have hquad : HasDerivAt (fun X : ℝ => alpha * (X * Real.sqrt X)) 0 0 := by
    simpa using x_mul_sqrt_hasDerivAt_zero.const_mul alpha
  have hadd := hlin.add hquad
  convert hadd using 3
  all_goals first
    | simp [Kfun, Pi.add_apply]
    | rfl
    | ring_nf

/- E3: at X = Y^2 the flux equals K'(Y^2) with the explicit value: the bridge
   between E1/E2 and A (stated as the derivative of K at the squared drive). -/
lemma Kderiv_at_sq_drive {C0 eps alpha Y : ℝ} (hY : 0 < Y) :
    HasDerivAt (fun X : ℝ => Kfun C0 eps alpha X) (eps + (3 / 2 : ℝ) * alpha * Y) (Y ^ 2) := by
  have hpos : 0 < Y ^ 2 := pow_pos hY 2
  convert K_hasDerivAt_pos (C0 := C0) (eps := eps) (alpha := alpha) (x := Y ^ 2) hpos using 3
  all_goals first
    | rw [Real.sqrt_sq (le_of_lt hY)]
    | rfl
    | ring_nf

/- F: deep-line matching algebra: mu = (3/2) alpha Y  <->  a0-line g^2 = a*g_N
   with a = 2s/(3 alpha). -/
theorem deep_line_equiv {g gN s alpha a : ℝ} (hs : s ≠ 0) (halpha : alpha ≠ 0)
    (ha : a = 2 * s / (3 * alpha)) :
    g * ((3 / 2 : ℝ) * alpha * (g / s)) = gN ↔ a * gN = g ^ 2 := by
  rw [ha]
  constructor <;> intro h
  · field_simp [hs, halpha] at h ⊢
    nlinarith
  · field_simp [hs, halpha] at h ⊢
    nlinarith

/- G: the adopted footing kappa = 1/2 (a_deep = s/2) pins the deep coefficient
   alpha = 4/3; eps and C0 play no role in this pinning. -/
theorem kappa_half_pins_alpha {s alpha : ℝ} (hs : s ≠ 0) (halpha : alpha ≠ 0) :
    (2 * s / (3 * alpha) = s / 2) ↔ alpha = 4 / 3 := by
  constructor
  · intro h
    field_simp [hs, halpha] at h
    nlinarith
  · intro halpha43
    rw [halpha43]
    field_simp [hs, halpha]
    norm_num

end