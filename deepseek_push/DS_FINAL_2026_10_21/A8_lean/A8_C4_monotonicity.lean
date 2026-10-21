/-
A8 / C4 — dg/dgN > 0 for both laws ("stable at every acceleration").

Physics claim being certified (BRIEF section 1, "stable at every acceleration"):
both interpolation laws are increasing functions of the baryonic acceleration
`gN` at fixed `a0`, with strictly positive derivative at every `gN > 0`.  The
physical content is that neither law has a branch fold, a negative-response
window, or a multivalued region: a small increase in baryonic mass always
produces a small increase in total acceleration, at every acceleration.

Certified here, for all `gN > 0`, `a0 > 0`:

* `deriv_gQuad`:   d/dgN sqrt(gN^2 + a0 gN) = (2 gN + a0)/(2 sqrt(gN^2 + a0 gN))
* `deriv_gCanon`:  d/dgN g_c = 1/2 + (gN/2 + a0)/(2 sqrt(gN^2/4 + a0 gN))
* `deriv_gQuad_pos`, `deriv_gCanon_pos`: both derivatives are > 0.
* `gQuad_strictMonoOn`, `gCanon_strictMonoOn`: both closed forms are strictly
  increasing on gN > 0 (the integrated form; independent of the derivative API).
* `gQuad_slope_pos`, `gCanon_slope_pos`: every difference quotient is > 0, i.e.
  the discrete form of dg/dgN > 0 on every interval, not merely pointwise.
* `gQuad_strictMonoOn_a0`, `gCanon_strictMonoOn_a0`: both are strictly
  increasing in a0 as well (a larger a0 gives a larger boost at fixed gN).

NOT certified: that either law is physically realised; that "stable" holds in
the dynamical (perturbation) sense — this is the monotonicity of the algebraic
map gN -> g, not a linear-stability statement about any field equation.
-/
import Mathlib

namespace A8

open Filter Topology

/-- Canonical law, solved for `g`. -/
noncomputable def gCanon (gN a0 : ℝ) : ℝ :=
  gN / 2 * (1 + Real.sqrt (1 + 4 * a0 / gN))

/-- `n = 2` law, solved for `g`. -/
noncomputable def gQuad (gN a0 : ℝ) : ℝ := Real.sqrt (gN ^ 2 + a0 * gN)

/-- Manifestly positive form of the canonical root. -/
theorem gCanon_form {gN a0 : ℝ} (hgN : 0 < gN) :
    gCanon gN a0 = gN / 2 + Real.sqrt (gN ^ 2 / 4 + a0 * gN) := by
  unfold gCanon
  have harg : gN ^ 2 / 4 + a0 * gN = (gN / 2) ^ 2 * (1 + 4 * a0 / gN) := by
    field_simp
    ring
  rw [harg, Real.sqrt_mul (by positivity : (0 : ℝ) ≤ (gN / 2) ^ 2),
    Real.sqrt_sq (by positivity : (0 : ℝ) ≤ gN / 2)]
  ring

/-! ## Derivatives of the two closed forms -/

/-- Derivative of the inner polynomial of the `n = 2` law. -/
theorem deriv_inner_quad (a0 gN : ℝ) :
    deriv (fun x : ℝ => x ^ 2 + a0 * x) gN = 2 * gN + a0 := by
  have hfun : (fun x : ℝ => x ^ 2 + a0 * x)
      =ᶠ[nhds gN] ((fun x : ℝ => x ^ 2) + fun x => a0 * x) := by
    filter_upwards with x
    rfl
  rw [hfun.deriv_eq]
  rw [deriv_add (by fun_prop) (by fun_prop)]
  rw [deriv_fun_pow (by fun_prop)]
  rw [deriv_const_mul a0 (by fun_prop)]
  simp

/-- Derivative of the inner polynomial of the canonical law. -/
theorem deriv_inner_canon (a0 gN : ℝ) :
    deriv (fun x : ℝ => x ^ 2 / 4 + a0 * x) gN = gN / 2 + a0 := by
  have hfun : (fun x : ℝ => x ^ 2 / 4 + a0 * x)
      =ᶠ[nhds gN] ((fun x : ℝ => (1 / 4) * x ^ 2) + fun x => a0 * x) := by
    filter_upwards with x
    simp only [Pi.add_apply]
    ring
  rw [hfun.deriv_eq]
  rw [deriv_add (by fun_prop) (by fun_prop)]
  rw [deriv_const_mul (1 / 4) (by fun_prop)]
  rw [deriv_fun_pow (by fun_prop)]
  rw [deriv_const_mul a0 (by fun_prop)]
  simp
  ring

/-- Derivative of `x/2`. -/
theorem deriv_half (gN : ℝ) : deriv (fun x : ℝ => x / 2) gN = 1 / 2 := by
  have hfun : (fun x : ℝ => x / 2) =ᶠ[nhds gN] (fun x => (1 / 2) * x) := by
    filter_upwards with x
    ring
  rw [hfun.deriv_eq]
  rw [deriv_const_mul (1 / 2) (by fun_prop)]
  simp

/-- **C4, `n = 2` derivative.** -/
theorem deriv_gQuad (a0 : ℝ) {gN : ℝ} (hgN : 0 < gN) (ha0 : 0 < a0) :
    deriv (fun x => gQuad x a0) gN = (2 * gN + a0) / (2 * Real.sqrt (gN ^ 2 + a0 * gN)) := by
  have hu : gN ^ 2 + a0 * gN ≠ 0 := ne_of_gt (by positivity)
  show deriv (fun x : ℝ => Real.sqrt (x ^ 2 + a0 * x)) gN
      = (2 * gN + a0) / (2 * Real.sqrt (gN ^ 2 + a0 * gN))
  rw [deriv_sqrt (f := fun x : ℝ => x ^ 2 + a0 * x) (x := gN) (by fun_prop) hu]
  rw [deriv_inner_quad]

/-- **C4, canonical derivative.** -/
theorem deriv_gCanon (a0 : ℝ) {gN : ℝ} (hgN : 0 < gN) (ha0 : 0 < a0) :
    deriv (fun x => gCanon x a0) gN
      = 1 / 2 + (gN / 2 + a0) / (2 * Real.sqrt (gN ^ 2 / 4 + a0 * gN)) := by
  have hu : gN ^ 2 / 4 + a0 * gN ≠ 0 := ne_of_gt (by positivity)
  have heq : (fun x => gCanon x a0)
      =ᶠ[nhds gN] (fun x => x / 2 + Real.sqrt (x ^ 2 / 4 + a0 * x)) := by
    filter_upwards [Ioi_mem_nhds hgN] with x hx
    exact gCanon_form hx
  rw [heq.deriv_eq]
  rw [deriv_fun_add (by fun_prop) (by fun_prop)]
  rw [deriv_sqrt (f := fun x : ℝ => x ^ 2 / 4 + a0 * x) (x := gN) (by fun_prop) hu]
  rw [deriv_inner_canon, deriv_half]

/-! ## Positivity of both derivatives -/

/-- **C4, `dg_q/dgN > 0` at every `gN > 0`.** -/
theorem deriv_gQuad_pos (a0 : ℝ) {gN : ℝ} (hgN : 0 < gN) (ha0 : 0 < a0) :
    0 < deriv (fun x => gQuad x a0) gN := by
  rw [deriv_gQuad a0 hgN ha0]
  apply div_pos (by linarith)
  positivity

/-- **C4, `dg_c/dgN > 0` at every `gN > 0`.** -/
theorem deriv_gCanon_pos (a0 : ℝ) {gN : ℝ} (hgN : 0 < gN) (ha0 : 0 < a0) :
    0 < deriv (fun x => gCanon x a0) gN := by
  rw [deriv_gCanon a0 hgN ha0]
  have h1 : 0 < (gN / 2 + a0) / (2 * Real.sqrt (gN ^ 2 / 4 + a0 * gN)) := by
    apply div_pos (by linarith)
    positivity
  linarith

/-! ## The integrated form: strict monotonicity -/

/-- **C4, `n = 2` law is strictly increasing in `gN`.** -/
theorem gQuad_strictMonoOn (a0 : ℝ) (ha0 : 0 < a0) :
    StrictMonoOn (fun gN => gQuad gN a0) (Set.Ioi 0) := by
  intro x hx y hy hxy
  have hx0 : 0 < x := hx
  have hy0 : 0 < y := hy
  have hsq : x ^ 2 < y ^ 2 := by
    nlinarith [mul_pos (by linarith : (0 : ℝ) < y - x) (by linarith : (0 : ℝ) < y + x)]
  have h : x ^ 2 + a0 * x < y ^ 2 + a0 * y := by nlinarith
  exact Real.sqrt_lt_sqrt (by positivity) h

/-- **C4, canonical law is strictly increasing in `gN`.** -/
theorem gCanon_strictMonoOn (a0 : ℝ) (ha0 : 0 < a0) :
    StrictMonoOn (fun gN => gCanon gN a0) (Set.Ioi 0) := by
  intro x hx y hy hxy
  have hx0 : 0 < x := hx
  have hy0 : 0 < y := hy
  show gCanon x a0 < gCanon y a0
  rw [gCanon_form hx0, gCanon_form hy0]
  have hsq : x ^ 2 < y ^ 2 := by
    nlinarith [mul_pos (by linarith : (0 : ℝ) < y - x) (by linarith : (0 : ℝ) < y + x)]
  have h : x ^ 2 / 4 + a0 * x < y ^ 2 / 4 + a0 * y := by nlinarith
  have := Real.sqrt_lt_sqrt (by positivity) h
  linarith

/-- **C4, discrete form of `dg/dgN > 0` (`n = 2` law):** every difference
quotient on the positive axis is strictly positive. -/
theorem gQuad_slope_pos (a0 : ℝ) (ha0 : 0 < a0) {x y : ℝ} (hx : 0 < x) (hxy : x < y) :
    0 < (gQuad y a0 - gQuad x a0) / (y - x) := by
  have hmono := gQuad_strictMonoOn a0 ha0
  have hlt : gQuad x a0 < gQuad y a0 :=
    hmono (show x ∈ Set.Ioi 0 from hx) (show y ∈ Set.Ioi 0 from lt_trans hx hxy) hxy
  exact div_pos (by linarith) (by linarith)

/-- **C4, discrete form of `dg/dgN > 0` (canonical law).** -/
theorem gCanon_slope_pos (a0 : ℝ) (ha0 : 0 < a0) {x y : ℝ} (hx : 0 < x) (hxy : x < y) :
    0 < (gCanon y a0 - gCanon x a0) / (y - x) := by
  have hmono := gCanon_strictMonoOn a0 ha0
  have hlt : gCanon x a0 < gCanon y a0 :=
    hmono (show x ∈ Set.Ioi 0 from hx) (show y ∈ Set.Ioi 0 from lt_trans hx hxy) hxy
  exact div_pos (by linarith) (by linarith)

/-- **C4, both laws increase with `a0`** (`n = 2` side). -/
theorem gQuad_strictMonoOn_a0 {gN : ℝ} (hgN : 0 < gN) :
    StrictMonoOn (fun a0 => gQuad gN a0) (Set.Ioi 0) := by
  intro x hx y hy hxy
  have hx0 : 0 < x := hx
  have h : gN ^ 2 + x * gN < gN ^ 2 + y * gN := by nlinarith
  exact Real.sqrt_lt_sqrt (by nlinarith) h

/-- **C4, both laws increase with `a0`** (canonical side). -/
theorem gCanon_strictMonoOn_a0 {gN : ℝ} (hgN : 0 < gN) :
    StrictMonoOn (fun a0 => gCanon gN a0) (Set.Ioi 0) := by
  intro x hx y hy hxy
  show gCanon gN x < gCanon gN y
  rw [gCanon_form hgN, gCanon_form hgN]
  have hx0 : 0 < x := hx
  have h : gN ^ 2 / 4 + x * gN < gN ^ 2 / 4 + y * gN := by nlinarith
  have := Real.sqrt_lt_sqrt (by nlinarith) h
  linarith

end A8

#print axioms A8.gCanon_form
#print axioms A8.deriv_gQuad
#print axioms A8.deriv_gCanon
#print axioms A8.deriv_gQuad_pos
#print axioms A8.deriv_gCanon_pos
#print axioms A8.gQuad_strictMonoOn
#print axioms A8.gCanon_strictMonoOn
#print axioms A8.gQuad_slope_pos
#print axioms A8.gCanon_slope_pos
#print axioms A8.gQuad_strictMonoOn_a0
#print axioms A8.gCanon_strictMonoOn_a0
