/-
Copyright (c) 2026 Carl Zimmerman. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: A83 lane
-/

import Mathlib

/-!
# A83 Block C — the A72 coefficient: κ_DE = Z/(4π) = √(2/3π), 8π/κ² = 12π², and the unreduced-wavel

Part of the A83 algebraic-spine formalization; see `A83_Spine.lean` for the sources and
the statement of what is and is not formalized.  No `axiom` declarations, no proof
holes, no kernel-bypassing evaluation.
-/

open Filter Matrix
open scoped Topology

noncomputable section

namespace A83

/-! ## Block C — the coefficient `κ_DE` and the 2π branch (A72) -/

/-- A72 §0: `Z = 2√(8π/3)`. -/
def Zcanon : ℝ := 2 * Real.sqrt (8 * Real.pi / 3)

/-- `Z² = 32π/3` for the canonical `Z` (A72 §0). -/
theorem Zcanon_sq : Zcanon ^ 2 = 32 * Real.pi / 3 := by
  unfold Zcanon
  rw [mul_pow, Real.sq_sqrt (by positivity)]
  ring

/-- `κ_DE = Z/(4π)` (A72 §0). -/
def kappaDE (Z : ℝ) : ℝ := Z / (4 * Real.pi)

/-- `κ_DE = √(2/(3π))` from `Z² = 32π/3`, `Z > 0`. -/
theorem kappaDE_eq_sqrt (Z : ℝ) (hZ : Z ^ 2 = 32 * Real.pi / 3) (hZ0 : 0 < Z) :
    kappaDE Z = Real.sqrt (2 / (3 * Real.pi)) := by
  unfold kappaDE
  have hsq : (Z / (4 * Real.pi)) ^ 2 = 2 / (3 * Real.pi) := by
    rw [div_pow, hZ]
    field_simp
    ring
  have hx : 0 ≤ 2 / (3 * Real.pi) := by positivity
  have hy : 0 ≤ Z / (4 * Real.pi) := le_of_lt (div_pos hZ0 (by positivity))
  rw [eq_comm, Real.sqrt_eq_iff_eq_sq hx hy]
  exact hsq.symm

/-- **The Friedmann normalisation behind A72 eq. (0.1):** with `8πGρ_Λ = 3H_Λ²` and
`Z² = 32π/3`, `Z > 0`, `H > 0`, one has `√(Gρ_Λ) = 2H_Λ/Z`.  (Positivity of `G` and
`ρ` is not needed for the identity and is therefore not assumed.) -/
theorem sqrt_Grho_eq (G ρ H Z : ℝ) (hH : 0 < H)
    (hFried : 8 * Real.pi * G * ρ = 3 * H ^ 2)
    (hZ : Z ^ 2 = 32 * Real.pi / 3) (hZ0 : 0 < Z) :
    Real.sqrt (G * ρ) = 2 * H / Z := by
  have hGrho : G * ρ = 3 * H ^ 2 / (8 * Real.pi) := by
    field_simp at hFried ⊢
    linarith
  have h2Z : Real.sqrt (3 / (8 * Real.pi)) = 2 / Z := by
    have hsq : (2 / Z) ^ 2 = 3 / (8 * Real.pi) := by
      rw [div_pow, hZ]
      field_simp
      ring
    rw [Real.sqrt_eq_iff_eq_sq (by positivity) (by positivity)]
    exact hsq.symm
  rw [hGrho, show 3 * H ^ 2 / (8 * Real.pi) = H ^ 2 * (3 / (8 * Real.pi)) by ring]
  rw [Real.sqrt_mul (by positivity), Real.sqrt_sq hH.le, h2Z]
  ring

/-- **A72 eq. (0.1), with its premises:** with the Friedmann normalisation
`8πGρ_Λ = 3H_Λ²`, `Z² = 32π/3`, and `a₀ = κc√(Gρ_Λ)`, the coefficient is
`a₀/(cH_Λ) = 2κ/Z` — equivalently `κ = Za₀/(2cH_Λ)`, which is the definition
`kappaOfA0` below. -/
theorem kappa_of_a0_from_friedmann (κ c G ρ H Z a0 : ℝ)
    (hH : 0 < H) (hc : c ≠ 0) (hFried : 8 * Real.pi * G * ρ = 3 * H ^ 2)
    (hZ : Z ^ 2 = 32 * Real.pi / 3) (hZ0 : 0 < Z)
    (ha0 : a0 = κ * c * Real.sqrt (G * ρ)) :
    a0 / (c * H) = 2 * κ / Z := by
  rw [ha0, sqrt_Grho_eq G ρ H Z hH hFried hZ hZ0]
  field_simp

/-- The thermal coefficient `a₀ = cH/(2π)` (A72 route (a)). -/
def a0Thermal (c H : ℝ) : ℝ := c * H / (2 * Real.pi)

/-- `2cH/a₀ = 4π` for the thermal coefficient. -/
theorem two_cH_over_a0 (c H : ℝ) (hc : c ≠ 0) (hH : H ≠ 0) :
    2 * (c * H) / a0Thermal c H = 4 * Real.pi := by
  unfold a0Thermal
  field_simp
  ring

/-- `κ` read off `a₀`: `a₀/(cH) = 2κ/Z` gives `κ = Za₀/(2cH)` (A72 eq. 0.1). -/
def kappaOfA0 (Z c H a0 : ℝ) : ℝ := Z * a0 / (2 * (c * H))

/-- **The A72 equivalence:** `a₀ = cH/(2π)` iff `κ_DE = Z/(4π)` — one algebraic
identity, not two independent conditions. -/
theorem a0_eq_iff_kappa_eq (Z c H a0 : ℝ) (hZ : Z ≠ 0) (hc : c ≠ 0) (hH : H ≠ 0) :
    a0 = a0Thermal c H ↔ kappaOfA0 Z c H a0 = kappaDE Z := by
  constructor
  · intro h
    subst h
    unfold kappaOfA0 kappaDE a0Thermal
    field_simp
    ring
  · intro h
    unfold kappaOfA0 kappaDE at h
    have h2cH : 2 * (c * H) ≠ 0 := by
      have : c * H ≠ 0 := mul_ne_zero hc hH
      positivity
    have h4pi : 4 * Real.pi ≠ 0 := by positivity
    rw [div_eq_div_iff h2cH h4pi] at h
    have h' : a0 * (4 * Real.pi) = 2 * (c * H) := by
      have h1 : Z * (a0 * (4 * Real.pi)) = Z * (2 * (c * H)) := by
        calc Z * (a0 * (4 * Real.pi)) = Z * a0 * (4 * Real.pi) := by ring
          _ = Z * (2 * (c * H)) := h
      exact mul_left_cancel₀ hZ h1
    unfold a0Thermal
    field_simp
    linarith

/-- `8π/κ_DE² = 12π²` (A72; the reduced branch). -/
theorem eight_pi_over_kappa_sq (Z : ℝ) (hZ : Z ^ 2 = 32 * Real.pi / 3) :
    8 * Real.pi / (kappaDE Z) ^ 2 = 12 * Real.pi ^ 2 := by
  unfold kappaDE
  have hsq : (Z / (4 * Real.pi)) ^ 2 = 2 / (3 * Real.pi) := by
    rw [div_pow, hZ]
    field_simp
    ring
  rw [hsq]
  field_simp
  ring

/-- `a₀` read off a wavelength: `a₀ = c²/(2πλ)` (A72's thermal construction). -/
def a0OfWavelength (c lam : ℝ) : ℝ := c ^ 2 / (2 * Real.pi * lam)

/-- The reduced wavelength `λ = c/H` gives `a₀ = cH/(2π)`. -/
theorem a0_reduced (c H : ℝ) (hc : c ≠ 0) (hH : H ≠ 0) :
    a0OfWavelength c (c / H) = a0Thermal c H := by
  unfold a0OfWavelength a0Thermal
  field_simp

/-- The unreduced wavelength `λ_full = 2π(c/H)` divides `a₀` by `2π`. -/
theorem a0_full (c H : ℝ) (hc : c ≠ 0) (hH : H ≠ 0) :
    a0OfWavelength c (2 * Real.pi * (c / H)) = a0Thermal c H / (2 * Real.pi) := by
  unfold a0OfWavelength a0Thermal
  field_simp

/-- The unreduced branch divides `κ_DE` by `2π`: `κ_full = Z/(8π²)`. -/
theorem kappa_full (Z : ℝ) :
    kappaDE Z / (2 * Real.pi) = Z / (8 * Real.pi ^ 2) := by
  unfold kappaDE
  field_simp
  ring

/-- **The 2π branch (the slip that refuted the external package):** with the
unreduced wavelength, `8π/κ_full² = 48π⁴`, not `12π²`. -/
theorem eight_pi_over_kappa_full_sq (Z : ℝ) (hZ : Z ^ 2 = 32 * Real.pi / 3) :
    8 * Real.pi / (kappaDE Z / (2 * Real.pi)) ^ 2 = 48 * Real.pi ^ 4 := by
  unfold kappaDE
  have hsq : (Z / (4 * Real.pi) / (2 * Real.pi)) ^ 2 = 1 / (6 * Real.pi ^ 3) := by
    rw [div_pow, div_pow, hZ]
    field_simp
    ring
  rw [hsq]
  field_simp
  ring

end A83
