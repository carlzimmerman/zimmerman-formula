import Mathlib

/-! # Cert: the assembly clock (T11) — ln-ratio identity

Certifies the ALGEBRA of the historical face of the settling law:

  law:      f = 1 - e^{-Gamma t}          (T10 S1 heat-mode settling)
  inputs:   f_c = 0.43 (clusters, X-COP), f_g = 0.60 (groups)
  density-locking:  R500 is density-defined (rho_bar(<R500) = 500 rho_crit)
                    => Gamma COMMON, cancels in the ratio
  result:   t_c / t_g = ln(1 - f_c) / ln(1 - f_g) = 0.6135

Numeric evaluation (ln 0.57 / ln 0.40 = 0.6135) and the inequality
0.6135 < f_c/f_g = 0.7167 live in the lane script (house pattern:
inequality/analysis statements ride with the lane when the build's
analysis lemmas resist; C1 and C2 verify them numerically). This file
certifies the exact identity: given the law at both epochs with the SAME
rate Gamma, the ratio of formation times IS the ratio of the
log-completenesses, with Gamma dividing out.

Zero sorry; axioms = {propext, Classical.choice, Quot.sound}.
-/

noncomputable section

open Real

variable {Gamma t_c t_g f_c f_g : ℝ}

/-- The settling law at both epochs with a common rate Gamma gives the
assembly-time ratio as the log-completeness ratio, Gamma cancelling. -/
theorem assembly_ratio_from_law (hΓ : Gamma ≠ 0) (htg : t_g ≠ 0)
    (hc : 1 - f_c = Real.exp (-Gamma * t_c))
    (hg : 1 - f_g = Real.exp (-Gamma * t_g)) :
    t_c / t_g = Real.log (1 - f_c) / Real.log (1 - f_g) := by
  have hlogc : Real.log (1 - f_c) = -Gamma * t_c := by
    rw [hc, Real.log_exp]
  have hlogg : Real.log (1 - f_g) = -Gamma * t_g := by
    rw [hg, Real.log_exp]
  have hlg_ne : Real.log (1 - f_g) ≠ 0 := by
    rw [hlogg]
    exact mul_ne_zero (neg_ne_zero.mpr hΓ) htg
  field_simp [hlg_ne]
  rw [hlogc, hlogg]
  ring

end