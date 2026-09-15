/-
  G002+G003 — the OneFunction construction and the phantom-bracket algebra,
  certified in Lean 4 (mathlib). Only fully-proven theorems; verified clean
  compile, exit 0, zero sorry.

  Certified here:
    onefunction_value_at_origin : f(0) = -1 -- the value at the non-analytic
      point IS the dark energy (L236 V6 condition 5; G002 V2)
    mu2_slope_form : mu_2(Y)/Y = (2+Y)/(1+Y)^2 -- the deep-MOND slope is the
      mode count 2, so kappa = 1/2 is its reciprocal (G002 V3/V8)
    deep_mond_cleared : the deep-MOND static law with s-denominators cleared is
      exactly g^2(2s+g) = gN(s+g)^2 -- the deep limit is g^2 = (s/2) gN, so the
      acceleration scale a_0 = s/2 is the output (G002 V7)
    phantom_bracket : r^2(g - g_N) = sqrt(GMa0) r - GM for the deep-MOND
      point-mass field -- the bracket whose derivative gives the phantom
      density (G003 V1, phantom side)

  mu_2 is carried in its rational form (2Y+Y^2)/(1+Y)^2, identical to
  1-(1+Y)^(-2) for Y ≠ -1 (sympy residual exactly zero, G002 V1).

  Verified symbolically+numerically in the committed Python lanes, not restated
  here (needs the HasDerivAt chain / a squaring argument): f'(X) = mu_2(sqrt X)
  for X > 0 (G002 V1/V3); phantom = isothermal coefficient 1 (G003 V1/V2).

  Scope: Lean certifies mathematics, not physics. Physical verdicts are the
  committed Python lanes' (G001/G002/G003 .out and _results.json).
-/
import Mathlib

noncomputable section

/-- The one function: f(X) = X - 2 ln(1+sqrt X) - 2/(1+sqrt X) + 1. -/
def f (X : ℝ) : ℝ := X - 2 * Real.log (1 + Real.sqrt X) - 2 / (1 + Real.sqrt X) + 1

/-- The measured interpolating function (SPARC-selected member, L232), in its
rational form -- identical to 1-(1+Y)^(-2) wherever Y ≠ -1. -/
def mu2 (Y : ℝ) : ℝ := (2 * Y + Y ^ 2) / (1 + Y) ^ 2

/-- **G002 V2.** The function's value at the non-analytic point is exactly
minus one: with amplitude rho_Lambda, the value there IS the measured dark
energy (L236 V6, condition 5). -/
theorem onefunction_value_at_origin : f 0 = -1 := by
  norm_num [f]

/-- **G002 V3 (slope form).** mu_2(Y)/Y = (2 + Y)/(1 + Y)^2 for Y ≠ 0, -1:
the deep-MOND slope is the mode count 2, and the coefficient kappa = 1/2 is
the reciprocal of the mode count the galaxies measured. -/
theorem mu2_slope_form {Y : ℝ} (hY : Y ≠ 0) (hY1 : Y ≠ -1) :
    mu2 Y / Y = (2 + Y) / (1 + Y) ^ 2 := by
  have hne : (1 + Y) ^ 2 ≠ 0 := by
    have h2 : (2 : ℕ) ≠ 0 := by norm_num
    intro h0
    have h1 : 1 + Y = 0 := by
      exact (pow_eq_zero_iff h2).mp h0
    exact hY1 (by linarith)
  unfold mu2
  field_simp


/-- **G002 V7 (cleared form).** The deep-MOND static law mu_2(g/s) g = g_N --
i.e. (2(g/s)+(g/s)^2) g = gN (1+g/s)^2 by the rational form -- with the
s-denominators cleared EXACTLY (s ≠ 0), is g^2(2s+g) = gN(s+g)^2. The deep
limit is g^2 = (s/2) gN: the acceleration scale a_0 = s/2 is the OUTPUT and
the 2 is the mode count. -/
theorem deep_mond_cleared (g s gN : ℝ) (hs : s ≠ 0)
    (h : (2 * (g / s) + (g / s) ^ 2) * g = gN * (1 + g / s) ^ 2) :
    g ^ 2 * (2 * s + g) = gN * (s + g) ^ 2 := by
  -- clear denominators by multiplying the hypothesis through by s^2, then
  -- recognise both sides as the same polynomial identity (s ≠ 0)
  have h2 : ((2 * (g / s) + (g / s) ^ 2) * g) * s ^ 2
      = (gN * (1 + g / s) ^ 2) * s ^ 2 := by rw [h]
  have hL : ((2 * (g / s) + (g / s) ^ 2) * g) * s ^ 2 = (2 * s + g) * g ^ 2 := by
    field_simp
  have hR : (gN * (1 + g / s) ^ 2) * s ^ 2 = gN * (s + g) ^ 2 := by
    field_simp
  rw [hL, hR] at h2
  linear_combination h2

/-- **G003 V1 (phantom side).** For a point mass with the deep-MOND law
g^2 = a0 g_N, the field is g = sqrt(G M a0)/r and the phantom bracket
r^2 (g - g_N) = sqrt(G M a0) r - G M -- the quantity whose r-derivative gives
the phantom density sqrt(G M a0)/(4 pi G r^2), verified against the isothermal
density at the virial temperature in G003 V1/V2 (coefficient exactly one). -/
theorem phantom_bracket (G M a0 r : ℝ) (hr : 0 < r) :
    r ^ 2 * (Real.sqrt (G * M * a0) / r - (G * M) / r ^ 2)
      = Real.sqrt (G * M * a0) * r - G * M := by
  field_simp

#print axioms onefunction_value_at_origin
#print axioms mu2_slope_form
#print axioms deep_mond_cleared
#print axioms phantom_bracket
