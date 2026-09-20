import Mathlib
/-!
L305 -- the phantom-boosted RAR (real_research/clock_2026/L305_phantom_rar_boost.py, 3/3).
The deep-MOND isothermal with the phantom's ACTIVE mass: v_c = (a0 G (M_b + M_act(<r)))^{1/4}:
the boost ratio v_c/√-flat = (1 + M_act/M_b)^{1/4}.  Certified here: the structural ratio identity.
-/
namespace L305

/-- the boost ratio: sqrt(aG (M+A)) / sqrt(aG M) = sqrt((M+A)/M), the structural content of the
    phantom-boosted RAR. -/
theorem boost_ratio (aG M A : ℝ) (hM : 0 < M) (ha : 0 ≤ aG) (hA : 0 ≤ A) (hm : aG * M ≠ 0) :
  Real.sqrt (aG * (M + A)) / Real.sqrt (aG * M) = Real.sqrt ((M + A) / M) := by
  have hx : 0 ≤ aG * (M + A) := by positivity
  have hden : 0 ≤ aG * M := by positivity
  have hdiv : Real.sqrt ((aG * (M + A)) / (aG * M)) = Real.sqrt (aG * (M + A)) / Real.sqrt (aG * M) :=
    Real.sqrt_div hx (aG * M)
  rw [← hdiv]
  congr 1
  have haG : aG ≠ 0 := by
    intro hz
    apply hm
    rw [hz]
    ring
  field_simp [hm, haG]

end L305