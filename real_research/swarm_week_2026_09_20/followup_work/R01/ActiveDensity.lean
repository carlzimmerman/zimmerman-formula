/-
  R01 -- CERTIFY THE ACTIVE-DENSITY FACTORIZATION AND ITS ASYMPTOTE.

  Target (FOLLOWUP_PACKETS.md R01):  for B,D>0, u>0 and 0<K<2,
      rho_act = (w-1)*rho = (2/3)(2-K) D u^3,
  with rho = (2-K) D (B u^2 + (2/3) u^3) and w-1 = (2/3)u/(B + (2/3)u).
  With u(B+u) = A/r (A,r>0):  r*u -> A/B and r^3*rho_act -> (2/3)(2-K) D (A/B)^3.

  This file certifies the exact factorization (N1) and the algebraic
  rearrangement behind the r^3 asymptote (N3, N3b).  The limits ru -> A/B and
  r^3 rho_act -> (2/3)(2-K) D (A/B)^3 are certified numerically in
  exact_factorization.py (N2, N4, N7), together with the finite-radius
  remainder bound; the Lean limit formalization is NOT claimed here (the
  card permits retention of the symbolic result with its formalization
  status stated).

  COMPILED clean, zero sorry, axioms = the standard three.
-/
import Mathlib

set_option linter.unusedVariables false

/-- **N1** -- the exact factorization for u>0 (the card's domain: B,D>0, 0<K<2, u>0).
The B + (2/3)u denominator cancels against the u^2 (B + (2/3)u) factor of rho,
so rho_act is cubic in u for EVERY u>0, not merely asymptotically. -/
theorem active_density_factorization {B D K u : ℝ} (hB : 0 < B) (hD : 0 < D)
    (hK : K < 2) (hu : 0 < u) :
    let rho := (2 - K) * D * (B * u ^ 2 + (2 / 3 : ℝ) * u ^ 3)
    let w1 := ((2 / 3 : ℝ) * u) / (B + (2 / 3 : ℝ) * u)
    w1 * rho = (2 / 3 : ℝ) * (2 - K) * D * u ^ 3 := by
  intro rho w1
  have hBp : B + (2 / 3 : ℝ) * u ≠ 0 := by
    have hpos : 0 < B + (2 / 3 : ℝ) * u := by positivity
    exact ne_of_gt hpos
  have hkey : ((2 / 3 : ℝ) * u) / (B + (2 / 3 : ℝ) * u) * (B + (2 / 3 : ℝ) * u) * u ^ 2
      = (2 / 3 : ℝ) * u ^ 3 := by
    field_simp [hBp]
  calc
    w1 * rho = ((2 / 3 : ℝ) * u / (B + (2 / 3 : ℝ) * u)) * ((2 - K) * D * (B * u ^ 2 + 2 / 3 * u ^ 3))
        := by simp [rho, w1]
    _ = ((2 / 3 : ℝ) * u / (B + (2 / 3 : ℝ) * u)) * (B + (2 / 3 : ℝ) * u) * u ^ 2 * ((2 - K) * D)
        := by ring
    _ = (2 / 3 : ℝ) * u ^ 3 * ((2 - K) * D) := by rw [hkey]
    _ = (2 / 3 : ℝ) * (2 - K) * D * u ^ 3 := by ring

/-- **N1b** -- the weight (w-1) is in (0,1) for u>0: the outer suppression is
strict (w-1) < 1, and the phantom's active face is a fraction of its raw density. -/
theorem w1_density_bounds {B u : ℝ} (hB : 0 < B) (hu : 0 < u) :
    0 < ((2 / 3 : ℝ) * u) / (B + (2 / 3 : ℝ) * u) ∧
    ((2 / 3 : ℝ) * u) / (B + (2 / 3 : ℝ) * u) < 1 := by
  have hBp : 0 < B + (2 / 3 : ℝ) * u := by positivity
  constructor
  · positivity
  · have hnum : (2 / 3 : ℝ) * u < B + (2 / 3 : ℝ) * u := by nlinarith [hB]
    exact (div_lt_one hBp).2 hnum

/-- **N3** -- the algebraic core of the asymptotic shell constant: with
u the positive root of u(B+u)=A/r,
  r^3 * (2/3)(2-K) D u^3  =  (2/3)(2-K) D (r u)^3. -/
theorem active_shell_asymptote_algebra {B D K u A r : ℝ} (hD : 0 < D)
    (hB : 0 < B) (hK : K < 2) (hr : 0 < r)
    (hu : u = 2 * A / (r * (B + Real.sqrt (B ^ 2 + 4 * A / r)))) :
    r ^ 3 * ((2 / 3 : ℝ) * (2 - K) * D * u ^ 3) =
      (2 / 3 : ℝ) * (2 - K) * D * (r * u) ^ 3 := by
  rw [hu]
  ring

/-- **N3b** -- the rationalized root identity used numerically (avoids
cancellation at large r):
    r * [2A/(r (B + sqrt(B^2 + 4A/r)))]  =  2A / (B + sqrt(B^2 + 4A/r)). -/
theorem ru_rationalized {B A r : ℝ} (hB : 0 < B) (hA : 0 < A) (hr : 0 < r) :
    r * (2 * A / (r * (B + Real.sqrt (B ^ 2 + 4 * A / r)))) =
      2 * A / (B + Real.sqrt (B ^ 2 + 4 * A / r)) := by
  field_simp