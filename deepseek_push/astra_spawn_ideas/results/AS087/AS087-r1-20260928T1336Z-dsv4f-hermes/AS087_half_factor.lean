import Mathlib

/-!
# AS087 Lean certificate — "Boundary pressure and the claimed half factor"

Seed sha256: b09eb2e2fe8bed9c3b29c4bedd7f508f7e35e420085ae6f641104d750c60ebbe
Run:          AS087-r1-20260928T1336Z-dsv4f-hermes

Certified algebra (real numbers; symbols are opaque, so the certificate is
about the algebraic identities, not the physics):

* T1 — the half-factor ratio.  The truncated singular isothermal phantom has
  2T = 3·M·σ².  Virial with the fluid-closure surface term: 2T + W = σ²·M
  (B = σ²·M).  Virial with ZERO surface pressure on the same profile and same
  equilibrium: 2T + W = 0.  Then σ₁²/σ₂² = 3/2 EXACTLY, for every W, M ≠ 0:
  the coefficient 1/2 vs 1/3 is entirely the surface-pressure term — the
  claimed half factor is conditional on the boundary condition.

* T2 — the seed's math line: for a full singular isothermal sphere with
  P_s = σ²·A/R², V = 4πR³/3, M = 4π·A·R:  3·P_s·V = σ²·M  exactly.

* T3a — substitution check of the closed form: the shell-virial solution
  σ² = (C/2)·[1 + (r_M − r_in)·ln(R/r_in)/(R − r_in)]  satisfies
  2·σ²·(R − r_in) = C·(R − r_in) − C·r_in·L + C·r_M·L,  L = ln(R/r_in),
  i.e. the closed form reproduces the virial equation by direct substitution.

* T3b — uniqueness: any solution of that virial equation with R ≠ r_in is
  the closed form (division safe: R − r_in ≠ 0).
-/

namespace AS087

/- T1: exact 3/2 ratio between fluid-closure and zero-surface-pressure readings.
   s1 = σ₁² (closure), s2 = σ₂² (bare), W = W_self + W_bar, M = M_T. -/
theorem virial_half_factor_ratio (s1 s2 W M : ℝ) (hM : M ≠ 0)
    (h1 : 3 * M * s1 + W = M * s1)
    (h2 : 3 * M * s2 + W = 0) :
    s1 = (3 / 2 : ℝ) * s2 := by
  have h1' : 2 * M * s1 = -W := by nlinarith
  have h2' : 3 * M * s2 = -W := by nlinarith
  have hboth : M * (2 * s1) = M * (3 * s2) := by nlinarith
  have hcancel : 2 * s1 = 3 * s2 := by
    exact mul_left_cancel₀ hM hboth
  linarith

/- T2: full singular isothermal sphere — 3 P_s V = σ² M. -/
theorem full_sis_surface_pressure_identity (σ2 A R : ℝ) (hR : R ≠ 0) :
    3 * (σ2 * A / R ^ 2) * (4 * Real.pi * R ^ 3 / 3) = σ2 * (4 * Real.pi * A * R) := by
  field_simp [hR]

/- T3a: the closed form satisfies the shell-virial equation (substitution),
   2·σ²·(R − r_in) = C·(R − r_in) − C·r_in·L + C·r_M·L. -/
theorem shell_virial_substitution (s C rM rin R L : ℝ) (hR : R - rin ≠ 0)
    (hs : s = (C / 2) * (1 + (rM - rin) * L / (R - rin))) :
    2 * s * (R - rin) = C * (R - rin) - C * rin * L + C * rM * L := by
  rw [hs]
  field_simp [hR]
  ring

/- T3b: uniqueness — any solution of the shell-virial equation with a proper
   shell (R ≠ r_in) is the closed form. -/
theorem shell_virial_closed_form (s C rM rin R L : ℝ) (hR : R - rin ≠ 0)
    (h : 2 * s * (R - rin) = C * (R - rin) - C * rin * L + C * rM * L) :
    s = (C / 2) * (1 + (rM - rin) * L / (R - rin)) := by
  have hsR : s * (R - rin) = (C / 2) * ((R - rin) + (rM - rin) * L) := by
    nlinarith [h]
  have hB : (C / 2) * (1 + (rM - rin) * L / (R - rin)) * (R - rin)
      = (C / 2) * ((R - rin) + (rM - rin) * L) := by
    field_simp [hR]
  have hB2 : (R - rin) * ((C / 2) * (1 + (rM - rin) * L / (R - rin)))
      = (C / 2) * ((R - rin) + (rM - rin) * L) := by
    field_simp [hR]
  have hm : (R - rin) * s = (R - rin) * ((C / 2) * (1 + (rM - rin) * L / (R - rin))) := by
    rw [mul_comm, hsR, ← hB2]
  exact mul_left_cancel₀ hR hm

end AS087

#print axioms AS087.virial_half_factor_ratio
#print axioms AS087.full_sis_surface_pressure_identity
#print axioms AS087.shell_virial_substitution
#print axioms AS087.shell_virial_closed_form
