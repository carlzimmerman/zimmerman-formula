/- QX5 MUTATE twin: three false claims; each must fail to compile. kappa = 1/2 FITTED; not theory closed. -/
import Mathlib
namespace QX5M
-- M1 false: the cap applied in the wrong direction (k above the calibrated key)
theorem mono_cap_wrong {F : ℝ → ℝ} (hF : Monotone F) {k khi ε : ℝ}
    (hk : khi ≤ k) (hcal : F khi ≤ 1 + ε) : F k ≤ 1 + ε := by
  exact le_trans (hF hk) hcal
-- M2 false: antitone with the monotone ordering
theorem anti_wrong {F : ℝ → ℝ} (hF : Antitone F) {kc kg ε δ : ℝ}
    (hk : kc ≤ kg) (hcal : F kg ≤ 1 + ε) (hneed : 1 + δ ≤ F kc) (hlt : ε < δ) : False := by
  have := hF hk
  linarith
-- M3 false: model mass monotone in F without a nonnegative phantom
theorem model_wrong {Mb Ml F₁ F₂ : ℝ} (hF : F₁ ≤ F₂) :
    Mb + F₁ * (Ml - Mb) ≤ Mb + F₂ * (Ml - Mb) := by
  nlinarith
end QX5M
