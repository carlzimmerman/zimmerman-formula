import Mathlib

/-!
Axiom audit for the AS035 Lean certificate.
Prints the axiom sets of every certified theorem. The hard bar for this campaign is
axioms ⊆ {propext, Classical.choice, Quot.sound}.
-/

noncomputable section
open Filter
open scoped Topology

namespace AS035

def hMonoLog (hR δ hp yp ys : ℝ) (y : ℝ) : ℝ :=
  hR + δ * hp * (Real.log (y + yp) - Real.log (ys + yp))

theorem splice_value : hMonoLog hR δ hp yp ys ys = hR := by
  unfold hMonoLog
  ring

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

end AS035

end

#eval Lean.Elab.Command.liftTermElabM none
-- axiom prints (run in the file's environment):
#print axioms AS035.splice_value
#print axioms AS035.ratio_tendsto_zero
