import Mathlib

/-! # AS035 — High-field recovery of the operative MONO branch (Lean certificate)

The operative MONO continuation (FRAMEWORK_CONTRACT.md branch table; FRIED_CHICKEN_SPEC.md
requirement 1, 2026-09-26 amendment) is

  h_mono(y) = h_RAR(y*) + δ·h_p·ln((y + y_p)/(y* + y_p))   for y ≥ y*,
  ν_mono(y) = 1 + h_mono(y)/y .

`hMonoLog` below implements the continuation. It is stated as
h_RAR(y*) + δ·h_p·(ln(y + y_p) − ln(y* + y_p)); by `Real.log_div` this is pointwise equal
to the ratio form ln((y+y_p)/(y*+y_p)) on the operative domain y > −y_p (theorem
`hMonoLog_eq_ratio`), but the difference form makes the derivative chain and the
asymptotic decomposition direct (no log-domain side conditions).

Certificates here:
  1. `splice_value`      — the continuation returns h_RAR(y*) at y = y* (value-match).
  2. `deriv_continuation`— d/dy of the log continuation equals δ·h_p·(y + y_p)⁻¹
                           (= δ·h_p/(y + y_p)); the algebraic core defining the branch
                           for y > y*.
  3. `deriv_pos`         — strictly monotone phantom on the continuation (δ, h_p > 0).
  4. `ratio_tendsto_zero`— h_mono(y)/y → 0, i.e. ν_mono(y) − 1 → 0 (Newtonian high-field
                           recovery of the exact log formula), by decay of log(y+y_p)/y.
  5. `absolute_tail_tendsto_atTop` — the NEGATIVE CONTROL: the absolute phantom h_mono(y)
                           itself diverges to +∞ while its ratio to y tends to 0; the
                           inference "ν_mono → 1 ⇒ h_mono → 0" is therefore false.
-/

noncomputable section
open Filter
open scoped Topology

namespace AS035

/-- The operative MONO log continuation: h_RAR(y*) + δ·h_p·(ln(y+y_p) − ln(y*+y_p)),
pointwise equal to the ratio form on y > −y_p (see `hMonoLog_eq_ratio`). -/
def hMonoLog (hR δ hp yp ys : ℝ) (y : ℝ) : ℝ :=
  hR + δ * hp * (Real.log (y + yp) - Real.log (ys + yp))

/-! ## 1. Splice value-match: the integration constant is fixed by construction. -/

theorem splice_value : hMonoLog hR δ hp yp ys ys = hR := by
  unfold hMonoLog
  ring

/-- The Lean definition equals the spec's ratio form ln((y+y_p)/(y*+y_p)) on y > −y_p. -/
theorem hMonoLog_eq_ratio {y : ℝ} (h₁ : 0 < y + yp) (h₂ : 0 < ys + yp) :
    hMonoLog hR δ hp yp ys y = hR + δ * hp * Real.log ((y + yp) / (ys + yp)) := by
  unfold hMonoLog
  rw [Real.log_div (ne_of_gt h₁) (ne_of_gt h₂)]

/-! ## 2. Algebraic core: derivative of the log continuation. -/

theorem deriv_continuation {y : ℝ} (hy : -yp < y) :
    HasDerivAt (fun y : ℝ => hMonoLog hR δ hp yp ys y) (δ * hp * (y + yp)⁻¹) y := by
  have hyy : 0 < y + yp := by linarith
  have hnum : HasDerivAt (fun y : ℝ => y + yp) (1 : ℝ) y := by
    simpa [id_eq] using ((hasDerivAt_id y).add_const yp)
  have hlog1 : HasDerivAt (fun y : ℝ => Real.log (y + yp)) ((y + yp)⁻¹) y := by
    have hc1 := HasDerivAt.comp (x := y) (hh₂ := Real.hasDerivAt_log hyy.ne') (hh := hnum)
    convert hc1 using 1
    all_goals first | rfl | rw [mul_one]
  have hsub : HasDerivAt (fun y : ℝ => Real.log (y + yp) - Real.log (ys + yp))
      ((y + yp)⁻¹) y := by
    have hs := hlog1.sub (hasDerivAt_const y (Real.log (ys + yp)))
    have hfuneq : (fun y : ℝ => Real.log (y + yp) - Real.log (ys + yp)) =ᶠ[𝓝 y]
        ((fun y : ℝ => Real.log (y + yp)) - fun _ : ℝ => Real.log (ys + yp)) :=
      (Filter.Eventually.of_forall (by intro y; rfl))
    simpa using (hs.congr_of_eventuallyEq hfuneq)
  have hmain : HasDerivAt (fun y : ℝ => δ * hp * (Real.log (y + yp) - Real.log (ys + yp)))
      (δ * hp * (y + yp)⁻¹) y :=
    hsub.const_mul (δ * hp)
  have hfin : HasDerivAt (fun y : ℝ => hR + δ * hp * (Real.log (y + yp) - Real.log (ys + yp)))
      (δ * hp * (y + yp)⁻¹) y :=
    hmain.const_add hR
  convert hfin using 1
  · funext y
    unfold hMonoLog
    rfl

/-! ## 3. Monotone phantom: the derivative is positive on the continuation. -/

theorem deriv_pos (hδ : 0 < δ) (hhp : 0 < hp) {y : ℝ} (hy : -yp < y) :
    0 < δ * hp * (y + yp)⁻¹ := by
  have hyy : 0 < y + yp := by linarith
  positivity

/-! ## 4. Newtonian high-field recovery: h_mono(y)/y → 0 (exact log formula). -/

/-- log z / z → 0 by the squeeze 0 ≤ log z / z ≤ 2/√z (z ≥ 1). -/
private lemma log_div_self_tendsto_zero : Tendsto (fun z : ℝ => Real.log z / z) atTop (𝓝 0) := by
  have hlo : ∀ᶠ z in atTop, 0 ≤ Real.log z / z := by
    filter_upwards [eventually_ge_atTop (1 : ℝ)] with z hz
    have hz0 : 0 < z := lt_of_lt_of_le zero_lt_one hz
    exact div_nonneg (Real.log_nonneg hz) (le_of_lt hz0)
  have hup : ∀ᶠ z in atTop, Real.log z / z ≤ (2 : ℝ) / Real.sqrt z := by
    filter_upwards [eventually_ge_atTop (1 : ℝ)] with z hz
    have hz0 : 0 < z := lt_of_lt_of_le zero_lt_one hz
    have hlogb : Real.log z ≤ 2 * Real.sqrt z := by
      have h2 : Real.log z = 2 * Real.log (Real.sqrt z) := by
        rw [Real.log_sqrt (le_of_lt hz0)]
        ring
      have h1 : Real.log (Real.sqrt z) ≤ Real.sqrt z - 1 :=
        Real.log_le_sub_one_of_pos (Real.sqrt_pos.2 hz0)
      nlinarith
    rw [div_le_iff₀ hz0]
    have hred : (2 / Real.sqrt z) * z = 2 * Real.sqrt z := by
      have hsq : Real.sqrt z * Real.sqrt z = z := by
        simpa [pow_two] using Real.sq_sqrt (le_of_lt hz0)
      field_simp [ne_of_gt (Real.sqrt_pos.2 hz0)]
      nlinarith
    rw [hred]
    exact hlogb
  have hg : Tendsto (fun z : ℝ => (2 : ℝ) / Real.sqrt z) atTop (𝓝 0) := by
    have hz : Tendsto (fun z : ℝ => (Real.sqrt z)⁻¹) atTop (𝓝 0) :=
      tendsto_inv_atTop_zero.comp Real.tendsto_sqrt_atTop
    simpa [div_eq_mul_inv] using
      (tendsto_const_nhds : Tendsto (fun _ : ℝ => (2 : ℝ)) atTop (𝓝 2)).mul hz
  exact squeeze_zero' hlo hup hg

/-- log(y + yp)/y → 0 for any fixed yp. -/
private lemma log_shifted_div_tendsto_zero (yp : ℝ) :
    Tendsto (fun y : ℝ => Real.log (y + yp) / y) atTop (𝓝 0) := by
  have hshift : Tendsto (fun y : ℝ => y + yp) atTop atTop := by
    simpa [add_comm] using
      (Filter.Tendsto.add_atTop
        (tendsto_const_nhds : Tendsto (fun _ : ℝ => yp) atTop (𝓝 yp)) (tendsto_id : Tendsto id atTop atTop))
  have h1 : Tendsto (fun y : ℝ => Real.log (y + yp) / (y + yp)) atTop (𝓝 0) :=
    log_div_self_tendsto_zero.comp hshift
  have hzero : Tendsto (fun y : ℝ => yp / y) atTop (𝓝 0) := by
    simpa [div_eq_mul_inv] using
      (tendsto_const_nhds : Tendsto (fun _ : ℝ => yp) atTop (𝓝 yp)).mul tendsto_inv_atTop_zero
  have hone : Tendsto (fun y : ℝ => (y + yp) / y) atTop (𝓝 1) := by
    have hplus : Tendsto (fun y : ℝ => (1 : ℝ) + yp / y) atTop (𝓝 1) := by
      simpa using
        ((tendsto_const_nhds : Tendsto (fun _ : ℝ => (1 : ℝ)) atTop (𝓝 1)).add hzero)
    refine hplus.congr' ?_
    filter_upwards [eventually_ge_atTop (1 : ℝ)] with y hy
    have hyn : y ≠ 0 := ne_of_gt (lt_of_lt_of_le zero_lt_one hy)
    field_simp [hyn]
  have hprod : Tendsto (fun y : ℝ => Real.log (y + yp) / (y + yp) * ((y + yp) / y)) atTop (𝓝 0) := by
    simpa [div_eq_mul_inv] using h1.mul hone
  refine hprod.congr' ?_
  filter_upwards [eventually_ge_atTop (|yp| + 1)] with y hy
  have hy0 : 0 < y := by nlinarith [abs_nonneg yp]
  have hyy : y + yp ≠ 0 := by
    have habs : yp ≤ |yp| := le_abs_self yp
    have habs' : -|yp| ≤ yp := neg_abs_le yp
    have hpos : 0 < y + yp := by nlinarith
    exact ne_of_gt hpos
  field_simp [ne_of_gt hy0, hyy]

/-- h_mono(y)/y → 0. Equivalently ν_mono(y) − 1 → 0 (Newtonian high-field recovery). -/
theorem ratio_tendsto_zero :
    Tendsto (fun y : ℝ => hMonoLog hR δ hp yp ys y / y) atTop (𝓝 0) := by
  have hRterm : Tendsto (fun y : ℝ => hR / y) atTop (𝓝 0) := by
    simpa [div_eq_mul_inv] using
      (tendsto_const_nhds : Tendsto (fun _ : ℝ => hR) atTop (𝓝 hR)).mul tendsto_inv_atTop_zero
  have hlogterm : Tendsto (fun y : ℝ => δ * hp * Real.log (y + yp) / y) atTop (𝓝 0) := by
    have h1 : Tendsto (fun y : ℝ => (δ * hp) * (Real.log (y + yp) / y)) atTop (𝓝 0) := by
      simpa [div_eq_mul_inv] using
        ((tendsto_const_nhds : Tendsto (fun _ : ℝ => δ * hp) atTop (𝓝 (δ * hp))).mul
          (log_shifted_div_tendsto_zero yp))
    refine h1.congr' ?_
    filter_upwards [eventually_ge_atTop (1 : ℝ)] with y hy
    have hyn : y ≠ 0 := ne_of_gt (lt_of_lt_of_le zero_lt_one hy)
    field_simp [hyn]
  have hCterm : Tendsto (fun y : ℝ => δ * hp * Real.log (ys + yp) / y) atTop (𝓝 0) := by
    simpa [div_eq_mul_inv] using
      ((tendsto_const_nhds : Tendsto (fun _ : ℝ => δ * hp * Real.log (ys + yp)) atTop
        (𝓝 (δ * hp * Real.log (ys + yp)))).mul tendsto_inv_atTop_zero)
  have hlin : Tendsto
      (fun y : ℝ => hR / y + δ * hp * Real.log (y + yp) / y - δ * hp * Real.log (ys + yp) / y)
      atTop (𝓝 0) := by
    simpa using (hRterm.add hlogterm).sub hCterm
  refine hlin.congr' ?_
  filter_upwards [eventually_ge_atTop (1 : ℝ)] with y hy
  have hy0 : y ≠ 0 := ne_of_gt (lt_of_lt_of_le zero_lt_one hy)
  unfold hMonoLog
  field_simp [hy0]
  ring

/-! ## 5. Negative control: absolute phantom diverges while the ratio decays. -/

theorem absolute_tail_tendsto_atTop (hA : 0 < δ * hp) :
    Tendsto (fun y : ℝ => hMonoLog hR δ hp yp ys y) atTop atTop := by
  have hshift : Tendsto (fun y : ℝ => y + yp) atTop atTop := by
    simpa [add_comm] using
      (Filter.Tendsto.add_atTop
        (tendsto_const_nhds : Tendsto (fun _ : ℝ => yp) atTop (𝓝 yp)) (tendsto_id : Tendsto id atTop atTop))
  have hlog : Tendsto (fun y : ℝ => Real.log (y + yp)) atTop atTop :=
    Real.tendsto_log_atTop.comp hshift
  have hmul : Tendsto (fun y : ℝ => δ * hp * Real.log (y + yp)) atTop atTop :=
    hlog.const_mul_atTop hA
  have hlin : Tendsto
      (fun y : ℝ => hR - δ * hp * Real.log (ys + yp) + δ * hp * Real.log (y + yp))
      atTop atTop :=
    Filter.Tendsto.add_atTop
      (tendsto_const_nhds : Tendsto (fun _ : ℝ => hR - δ * hp * Real.log (ys + yp)) atTop
        (𝓝 (hR - δ * hp * Real.log (ys + yp))))
      hmul
  refine hlin.congr' ?_
  exact (Filter.Eventually.of_forall (by intro y; unfold hMonoLog; ring))

end AS035

end
