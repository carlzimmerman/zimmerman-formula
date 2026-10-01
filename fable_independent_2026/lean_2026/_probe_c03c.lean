import Mathlib

noncomputable section

open Filter

#check nhds
#check 𝓝
#check atTop
#check Filter.Tendsto.comp

example (b : ℝ) (hb : 0 < b) :
    Filter.Tendsto (fun t : ℝ => t / b) atTop atTop := by
  exact (Filter.Tendsto.atTop_div_const (r := b) hb (Filter.tendsto_id : Filter.Tendsto id atTop atTop))

example (b : ℝ) (hb : 0 < b) :
    Filter.Tendsto (fun t : ℝ => Real.arctan (t / b)) atTop (nhds (Real.pi / 2)) := by
  have hdiv : Filter.Tendsto (fun t : ℝ => t / b) atTop atTop := by
    exact (Filter.Tendsto.atTop_div_const (r := b) hb (Filter.tendsto_id : Filter.Tendsto id atTop atTop))
  have hc : Filter.Tendsto (fun t : ℝ => Real.arctan (t / b)) atTop
      (nhdsWithin (Real.pi / 2) (Set.Iio (Real.pi / 2))) := by
    simpa [Function.comp_def] using (Real.tendsto_arctan_atTop.comp hdiv)
  exact hc.mono_right nhdsWithin_le_nhds