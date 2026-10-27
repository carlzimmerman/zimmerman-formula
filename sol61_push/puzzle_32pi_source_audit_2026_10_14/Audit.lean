import Mathlib
noncomputable section
namespace SourceAudit

theorem quadratic_energy_bound (stiff radial transverse lap scale : ℝ)
    (hs : 0 ≤ stiff) (_hscale : 0 < scale) :
    lap^2/scale^2 ≤ stiff*(2*radial^2+transverse^2)+lap^2/scale^2 := by
  have h : 0 ≤ stiff*(2*radial^2+transverse^2) := by positivity
  linarith

theorem shell_linear_coefficient_positive (kap scale hi lo norm : ℝ)
    (hk : 0 < kap) (hs : 0 < scale) (hl : 0 < lo) (hh : lo < hi)
    (hn : 0 < norm) : 0 < kap*scale*(hi^3-lo^3)/norm := by
  have hhi : 0 < hi := lt_trans hl hh
  have hdiff : 0 < hi-lo := sub_pos.mpr hh
  have hprod : 0 < (hi-lo)*(hi^2+hi*lo+lo^2) := by positivity
  have hp : lo^3 < hi^3 := by nlinarith
  apply div_pos (mul_pos (mul_pos hk hs) (sub_pos.mpr hp)) hn

theorem shell_quadratic_coefficient_negative (kap scale hi lo norm : ℝ)
    (hk : 0 < kap) (hs : 0 < scale) (hh : lo < hi) (hn : 0 < norm) :
    -(7*kap^2*scale^3*(hi-lo)/norm) < 0 := by
  have h : 0 < 7*kap^2*scale^3*(hi-lo)/norm := by positivity
  linarith

#print axioms quadratic_energy_bound
#print axioms shell_linear_coefficient_positive
#print axioms shell_quadratic_coefficient_negative
end SourceAudit
