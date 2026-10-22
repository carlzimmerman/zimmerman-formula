/-
Copyright (c) 2026 Carl Zimmerman. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: A83 lane
-/

import Mathlib

/-!
# A83 Block B — the saturating law g_N = g²/(g+a₀), the rectification obstruction (odd ⟹ f''(0) = 0

Part of the A83 algebraic-spine formalization; see `A83_Spine.lean` for the sources and
the statement of what is and is not formalized.  No `axiom` declarations, no proof
holes, no kernel-bypassing evaluation.
-/

open Filter Matrix
open scoped Topology

noncomputable section

namespace A83

/-! ## Block B — the saturating law, the rectification obstruction, and the
mass cancellation (A63, A54, A75) -/

/-- A54/A63: `g_N(g) = g²/(g+a₀)`. -/
def gN (g a0 : ℝ) : ℝ := g ^ 2 / (g + a0)

/-- The saturating law undershoots the drive: `g_N < g` for `g > 0`, `a₀ > 0`. -/
theorem gN_lt_g (g a0 : ℝ) (hg : 0 < g) (ha0 : 0 < a0) : gN g a0 < g := by
  unfold gN
  have h : 0 < g + a0 := by linarith
  rw [div_lt_iff₀ h]
  nlinarith

/-- `dg_N/dg = (g² + 2a₀g)/(g+a₀)²`. -/
theorem deriv_gN (g a0 : ℝ) (h : g + a0 ≠ 0) :
    deriv (fun x : ℝ => gN x a0) g = (g ^ 2 + 2 * a0 * g) / (g + a0) ^ 2 := by
  have h1 : HasDerivAt (fun x : ℝ => x ^ 2) (2 * g) g := by
    simpa using hasDerivAt_pow 2 g
  have h2 : HasDerivAt (fun x : ℝ => x + a0) 1 g := by
    simpa using (hasDerivAt_id g).add_const a0
  have h3 : HasDerivAt (fun x : ℝ => x ^ 2 / (x + a0))
      ((2 * g * (g + a0) - g ^ 2 * 1) / (g + a0) ^ 2) g := h1.div h2 h
  unfold gN
  rw [h3.deriv]
  field_simp
  ring

/-- The forward slope is positive: `dg_N/dg > 0`. -/
theorem deriv_gN_pos (g a0 : ℝ) (hg : 0 < g) (ha0 : 0 < a0) :
    0 < deriv (fun x : ℝ => gN x a0) g := by
  have h : g + a0 ≠ 0 := by positivity
  rw [deriv_gN g a0 h]
  have hnum : 0 < g ^ 2 + 2 * a0 * g := by nlinarith
  exact div_pos hnum (pow_pos (by linarith : 0 < g + a0) 2)

/-- The explicit inverse branch: for `g_N > 0` the positive solution of
`g_N = g²/(g+a₀)` is `g = (g_N + √(g_N² + 4a₀g_N))/2`. -/
def gOfgN (x a0 : ℝ) : ℝ := (x + Real.sqrt (x ^ 2 + 4 * a0 * x)) / 2

/-- The branch really inverts the law: `g_N = g(g_N)²/(g(g_N)+a₀)`. -/
theorem gOfgN_eq (x a0 : ℝ) (hx : 0 < x) (ha0 : 0 < a0) : x = gN (gOfgN x a0) a0 := by
  unfold gN gOfgN
  have hS : 0 ≤ x ^ 2 + 4 * a0 * x := by nlinarith
  have hkey : ((x + Real.sqrt (x ^ 2 + 4 * a0 * x)) / 2) ^ 2
      = x * ((x + Real.sqrt (x ^ 2 + 4 * a0 * x)) / 2) + x * a0 := by
    rw [show ((x + Real.sqrt (x ^ 2 + 4 * a0 * x)) / 2) ^ 2
        = ((x + Real.sqrt (x ^ 2 + 4 * a0 * x)) ^ 2) / 4 by ring]
    rw [show (x + Real.sqrt (x ^ 2 + 4 * a0 * x)) ^ 2
        = x ^ 2 + 2 * x * Real.sqrt (x ^ 2 + 4 * a0 * x)
          + (Real.sqrt (x ^ 2 + 4 * a0 * x)) ^ 2 by ring]
    rw [Real.sq_sqrt hS]
    ring
  have hden : (x + Real.sqrt (x ^ 2 + 4 * a0 * x)) / 2 + a0 ≠ 0 := by positivity
  rw [eq_div_iff hden]
  have hsqS : (Real.sqrt (x ^ 2 + 4 * a0 * x)) ^ 2 = x ^ 2 + 4 * a0 * x := Real.sq_sqrt hS
  nlinarith [hkey, hsqS]

theorem deriv_gOfgN (x a0 : ℝ) (hx : 0 < x) (ha0 : 0 < a0) :
    deriv (fun y : ℝ => gOfgN y a0) x
      = 1 + a0 ^ 2 / (gOfgN x a0 ^ 2 + 2 * a0 * gOfgN x a0) := by
  set g : ℝ := gOfgN x a0 with hgdef
  have hS : 0 < x ^ 2 + 4 * a0 * x := by nlinarith
  have hgpos : 0 < g := by
    rw [hgdef]
    unfold gOfgN
    have h0 : 0 ≤ Real.sqrt (x ^ 2 + 4 * a0 * x) := Real.sqrt_nonneg _
    linarith
  have hga : 0 < g + a0 := by linarith
  -- the forward derivative at `g`
  have hnum : HasDerivAt (fun y : ℝ => y ^ 2) (2 * g) g := by
    simpa using hasDerivAt_pow 2 g
  have hden' : HasDerivAt (fun y : ℝ => y + a0) 1 g := by
    simpa using (hasDerivAt_id g).add_const a0
  have hf : HasDerivAt (fun y : ℝ => gN y a0)
      ((g ^ 2 + 2 * a0 * g) / (g + a0) ^ 2) g := by
    have h := hnum.div hden' hga.ne'
    have hval : (2 * g * (g + a0) - g ^ 2 * 1) / (g + a0) ^ 2
        = (g ^ 2 + 2 * a0 * g) / (g + a0) ^ 2 := by
      congr 1
      ring
    rw [hval] at h
    have h' : (fun y : ℝ => y ^ 2) / (fun y : ℝ => y + a0) = fun y => gN y a0 := by
      funext y
      simp [gN]
    rw [h'] at h
    exact h
  have hf' : (g ^ 2 + 2 * a0 * g) / (g + a0) ^ 2 ≠ 0 := by
    have h1 : 0 < g ^ 2 + 2 * a0 * g := by nlinarith
    exact div_ne_zero h1.ne' (pow_ne_zero 2 hga.ne')
  have hcont : ContinuousAt (fun y : ℝ => gOfgN y a0) x := by
    unfold gOfgN
    apply ContinuousAt.div_const
    apply ContinuousAt.add continuousAt_id
    exact ContinuousAt.sqrt (by fun_prop)
  have hfg : ∀ᶠ y : ℝ in 𝓝 x, gN (gOfgN y a0) a0 = y := by
    have hpos : {y : ℝ | 0 < y} ∈ 𝓝 x := isOpen_lt continuous_const continuous_id |>.mem_nhds hx
    filter_upwards [hpos] with y hy
    exact (gOfgN_eq y a0 hy ha0).symm
  have hderiv := HasDerivAt.of_local_left_inverse hcont hf hf' hfg
  rw [hderiv.deriv]
  field_simp
  ring

/-- The inverse slope exceeds one: `1 < dg/dg_N` (A54 gate (iv)). -/
theorem deriv_gOfgN_gt_one (x a0 : ℝ) (hx : 0 < x) (ha0 : 0 < a0) :
    1 < deriv (fun y : ℝ => gOfgN y a0) x := by
  rw [deriv_gOfgN x a0 hx ha0]
  have h1 : 0 < gOfgN x a0 := by
    unfold gOfgN
    have h0 : 0 ≤ Real.sqrt (x ^ 2 + 4 * a0 * x) := Real.sqrt_nonneg _
    linarith
  have h2 : 0 < gOfgN x a0 ^ 2 + 2 * a0 * gOfgN x a0 := by nlinarith
  have h3 : 0 < a0 ^ 2 / (gOfgN x a0 ^ 2 + 2 * a0 * gOfgN x a0) :=
    div_pos (pow_pos ha0 2) h2
  linarith

/-- The Langmuir isotherm `θ(x) = x/(1+x)` (A63 §1, `c₂ = −1`). -/
def theta (x : ℝ) : ℝ := x / (1 + x)

/-- `θ(0) = 0`. -/
theorem theta_zero : theta 0 = 0 := by simp [theta]

/-- `θ'(x) = 1/(1+x)²`. -/
theorem theta_deriv (x : ℝ) (hx : 1 + x ≠ 0) : deriv theta x = 1 / (1 + x) ^ 2 := by
  have h : HasDerivAt theta ((1 * (1 + x) - x * 1) / (1 + x) ^ 2) x := by
    unfold theta
    exact (hasDerivAt_id x).div
      ((hasDerivAt_id x).const_add 1) hx
  rw [h.deriv]
  ring_nf

/-- `θ'(0) = 1`: unit linear response. -/
theorem theta_deriv_zero : deriv theta 0 = 1 := by
  rw [theta_deriv 0 (by norm_num)]
  norm_num

/-- `θ''(0) = −2`: the Langmuir gate is non-centrosymmetric with `c₂ = −1`
(A63 §1).  This is the second-order coefficient that the deep limit `g²/a₀` requires. -/
theorem theta_second_deriv_zero : deriv (deriv theta) 0 = -2 := by
  have hev : (deriv theta) =ᶠ[𝓝 (0 : ℝ)] (fun x : ℝ => 1 / (1 + x) ^ 2) := by
    have hmem : {x : ℝ | 1 + x ≠ 0} ∈ 𝓝 (0 : ℝ) := by
      have hopen : IsOpen {x : ℝ | 1 + x ≠ 0} := by
        have hset : {x : ℝ | 1 + x ≠ 0} = (fun x : ℝ => 1 + x) ⁻¹' {y : ℝ | y ≠ 0} := rfl
        rw [hset]
        exact isOpen_ne.preimage (by continuity)
      exact hopen.mem_nhds (by norm_num)
    filter_upwards [hmem] with x hx using theta_deriv x hx
  have hd2 : deriv (fun x : ℝ => 1 / (1 + x) ^ 2) 0 = -2 := by
    have hfun : (fun x : ℝ => 1 / (1 + x) ^ 2)
        = ((fun _ : ℝ => (1 : ℝ)) / (fun x : ℝ => (1 + x) ^ 2)) := by
      funext x; simp
    rw [hfun, deriv_div]
    · norm_num
      rw [deriv_fun_pow (by fun_prop : DifferentiableAt ℝ (fun x : ℝ => 1 + x) 0) 2]
      norm_num
    · fun_prop
    · fun_prop
    · norm_num
  have hdiff : DifferentiableAt ℝ (fun x : ℝ => 1 / (1 + x) ^ 2) 0 :=
    DifferentiableAt.div (by fun_prop) (by fun_prop) (by norm_num)
  have h1 : HasDerivAt (fun x : ℝ => 1 / (1 + x) ^ 2)
      (deriv (fun x : ℝ => 1 / (1 + x) ^ 2) 0) 0 := hdiff.hasDerivAt
  rw [hd2] at h1
  have h2 := h1.congr_of_eventuallyEq hev
  simpa using h2.deriv

/-- An even function has zero derivative at the origin.  (Proof: `deriv (g ∘ neg) 0
= −deriv g 0`, but `g ∘ neg = g`.)  This is the analytic core of the rectification
obstruction. -/
theorem deriv_eq_zero_of_even {g : ℝ → ℝ} (heven : ∀ x, g (-x) = g x) : deriv g 0 = 0 := by
  have h1 : deriv (fun x : ℝ => g (-x)) 0 = -deriv g (-0) := deriv_comp_neg g 0
  have h2 : (fun x : ℝ => g (-x)) = g := funext heven
  rw [h2] at h1
  have h3 : deriv g 0 = -deriv g 0 := by simpa using h1
  linarith

/-- The derivative of an odd function is even. -/
theorem deriv_odd_is_even {f : ℝ → ℝ} (hodd : ∀ x, f (-x) = -f x)
    (hdf : ∀ x, DifferentiableAt ℝ f x) (x : ℝ) : deriv f (-x) = deriv f x := by
  have h1 : deriv (fun y : ℝ => f (-y)) x = -deriv f (-x) := deriv_comp_neg f x
  have h2 : (fun y : ℝ => f (-y)) = (fun y : ℝ => -f y) := funext hodd
  rw [h2] at h1
  have h3 : deriv (fun y : ℝ => -f y) x = -deriv f x := by
    have h4 : HasDerivAt f (deriv f x) x := (hdf x).hasDerivAt
    have h5 : HasDerivAt (fun y : ℝ => -f y) (-deriv f x) x := h4.neg
    exact h5.deriv
  linarith

/-- **Rectification obstruction (A63):** an odd function has `f''(0) = 0`.  Hence no
centrosymmetric saturating isotherm can produce the `g²` term that `g_N = g²/(g+a₀)`
requires; the Langmuir gate is `θ` above, with `θ''(0) = −2`. -/
theorem odd_second_deriv_zero {f : ℝ → ℝ} (hodd : ∀ x, f (-x) = -f x)
    (hdf : ∀ x, DifferentiableAt ℝ f x) :
    deriv (deriv f) 0 = 0 :=
  deriv_eq_zero_of_even (fun x => deriv_odd_is_even hodd hdf x)

/-- A75 §2.5, the real content: with `λ_C = ħ/(mc)`, the saturation acceleration
`a_sat = k_BT/(mλ_C)` equals `k_BTc/ħ` **identically** — the mass cancels.  This is why
A72's coefficient carries no carrier mass (A75 K11). -/
theorem mass_cancellation (kB T m c hbar : ℝ) (hm : m ≠ 0) (hc : c ≠ 0) (hb : hbar ≠ 0) :
    kB * T / (m * (hbar / (m * c))) = kB * T * c / hbar := by
  field_simp

/-- The gate as a function of drive and affinity — **no temperature argument**
(A75 §1.2). -/
def thetaOf (g a0 : ℝ) : ℝ := g / (g + a0)

/-- `θ` written with an explicit (ignored) temperature slot.  This is a
**definitional** device, not a physics theorem: it records that `thetaOf` has no `T`
argument, so its temperature-independence at fixed drive is a fact about the
definition.  The physics (why the drive is an activity, and the free-energy
derivation) is A75 §1 and is *not* formalized here. -/
def thetaAtTemperature (_T g a0 : ℝ) : ℝ := thetaOf g a0

/-- Definitional temperature-blindness, stated as such (see `thetaAtTemperature`). -/
theorem theta_temperature_blind (T g a0 : ℝ) :
    thetaAtTemperature T g a0 = thetaOf g a0 := rfl

/-- The gate is a function of the activity `z = g/a₀` — an algebraic identity
(A75 eq. 1.2). -/
theorem thetaOf_eq_activity (g a0 : ℝ) (ha0 : a0 ≠ 0) :
    thetaOf g a0 = (g / a0) / (1 + g / a0) := by
  unfold thetaOf
  field_simp
  ring

end A83
