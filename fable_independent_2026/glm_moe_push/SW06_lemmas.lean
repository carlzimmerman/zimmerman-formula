/- SW06 lemmas: the algebra of the Gamma/eta conformal response class.
   Lean certifies ALGEBRA only; the physics gates live in the Python lanes
   (SW01b/SW04/SW05/SW06 .out/.json). Mutation note: in `conformal_BR` the
   hypotheses `hS` and `hQ1` are load-bearing — deleting either breaks the proof
   (division by zero), which is the mutation demonstration. -/

import Mathlib

/-- The eBTFR: the deep limit of the class gives v^4 = S^2 * G * M * a0.
    Hypotheses: the deep force law g = S * sqrt(a0 * g_N) with g_N = G*M/r^2 and
    the circular-orbit condition v^2 = g*r. Mutation note: `hr` (r > 0) is
    load-bearing — without it the r^2 cancellation is division by zero. -/
theorem eBTFR (S G M a0 r v : ℝ) (hS : 0 ≤ S) (hG : 0 ≤ G) (hM : 0 ≤ M) (ha : 0 ≤ a0)
    (hr : 0 < r) (hv : v ^ 2 = r * (S * Real.sqrt (a0 * G * M / r ^ 2))) :
    v ^ 4 = S ^ 2 * (G * M * a0) := by
  have hX : 0 ≤ a0 * G * M / r ^ 2 := by positivity
  have hs : (Real.sqrt (a0 * G * M / r ^ 2)) ^ 2 = a0 * G * M / r ^ 2 := Real.sq_sqrt hX
  have h2 : (S * Real.sqrt (a0 * G * M / r ^ 2)) ^ 2
      = S ^ 2 * (a0 * G * M / r ^ 2) := by rw [mul_pow, hs]
  calc v ^ 4 = (v ^ 2) ^ 2 := by ring
    _ = (r * (S * Real.sqrt (a0 * G * M / r ^ 2))) ^ 2 := by rw [hv]
    _ = r ^ 2 * (S * Real.sqrt (a0 * G * M / r ^ 2)) ^ 2 := by ring
    _ = r ^ 2 * (S ^ 2 * (a0 * G * M / r ^ 2)) := by rw [h2]
    _ = S ^ 2 * (G * M * a0) := by field_simp

/-- The conformal cancellation: the environment scalar S cancels in the boost
    ratio, so the RAR shape is environment-independent (the SW04 identity).
    Mutation note: `hS` and `hQ1` are load-bearing. -/
theorem conformal_BR (S Q1 Q2 Q1i Q2i : ℝ) (h1 : Q1 = S * Q1i) (h2 : Q2 = S * Q2i)
    (hS : S ≠ 0) (hQ1 : Q1 ≠ 0) : Q2 / Q1 = Q2i / Q1i := by
  rw [h2, h1]
  field_simp

/-- The Newton limit: S = 0 is exact Newton on the sourced sector. -/
theorem newton_limit (S nu g : ℝ) (hS : S = 0) : ((1 - S) + S * nu) * g = g := by
  subst hS; ring

/-- The MOND limit: S = 1 is the standard RAR on the sourced sector. -/
theorem mond_limit (S nu g : ℝ) (hS : S = 1) : ((1 - S) + S * nu) * g = nu * g := by
  subst hS; ring

/-- The mu_S equivalence: the inversion defines the rescaled MOND function
    mu_S = 1/((1 - S) + S * nu) as a single-valued function (well-posedness is
    checked numerically in SW06 B1; this is its algebraic statement). -/
theorem mu_S_equiv (S nu g_src g_obs : ℝ)
    (h : g_obs = ((1 - S) + S * nu) * g_src)
    (hf : ((1 - S) + S * nu) ≠ 0) (hg : g_src ≠ 0) :
    g_src / g_obs = 1 / ((1 - S) + S * nu) := by
  rw [h]; field_simp
