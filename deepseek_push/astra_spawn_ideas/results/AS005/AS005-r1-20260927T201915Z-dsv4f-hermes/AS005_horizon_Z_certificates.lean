import Mathlib

/-!
# AS005 — Horizon normalization and Z: algebraic certificates

SCOPE. `deepseek_push/astra_spawn_ideas/AS005_horizon_normalization_and_z.md` (task AS005,
CORE scale identities, kappa = 1/2 ADOPTED as framework input). Lean certifies the algebra
behind the horizon statements:

    a0        = κ · c · sqrt(G_N · ρ)           (κ = 1/2 adopted; G_N the scale/measured coupling)
    Λ_eff     = 8π · G_E · ρ / c²               (Einstein coupling G_E, vacuum mass density ρ)
    H_L       = c · sqrt(Λ_eff / 3)             (Lambda-only Hubble rate, framework ρ — NOT H0,
                                                 NOT the critical-density rate)
    R_dS      = c / H_L                         (de Sitter radius)
    Z_H       = c · H_L / a0                    (dimensionless horizon normalization)

Main theorem: Z_H = sqrt(8π G_E / (3 G_N)) / κ, so at κ = 1/2 with G_E = G_N:
Z_H = sqrt(32π/3) = 5.78881...  (= √(32π/3); the "Z~21" error is excluded: it would force
κ = 0.1378, contradicting the adopted κ = 1/2).

Negative control certified here: κ · Z_H = sqrt(8π G_E / (3 G_N)) — a one-dimensional
constraint: treating Z_H and κ as independent fitted constants is redundant (Z_H is κ
restated, exactly as STANDING.md rev. 11 records: "Z = √(32π/3) = 5.7888 is κ restated").
The identity explicitly tracks G_E ≠ G_N; it is NOT certified at H0 or at the
critical-density rate, and fails there (R_dS = c/H_L only with the framework H_L).

Constants and numerics live in `as005_horizon_z.py` (50-digit mpmath + sympy); this file
certifies the exact algebraic content only.
-/

noncomputable section

open scoped Real

namespace AS005

/-- framework vacuum scale: a0 = κ c sqrt(G_N ρ) -/
def a0 (κ c G_N ρ : ℝ) : ℝ := κ * c * Real.sqrt (G_N * ρ)

/-- vacuum curvature with the Einstein coupling: Λ_eff = 8π G_E ρ / c² -/
def Λeff (G_E ρ c : ℝ) : ℝ := 8 * Real.pi * G_E * ρ / c ^ 2

/-- Lambda-only Hubble rate: H_L = c sqrt(Λ_eff / 3) -/
def HL (Λ c : ℝ) : ℝ := c * Real.sqrt (Λ / 3)

/-- the dimensionless horizon normalization Z_H = c H_L / a0 -/
def Z (c G_E G_N ρ κ : ℝ) : ℝ := c * HL (Λeff G_E ρ c) c / a0 κ c G_N ρ

/-- positivity of the scale: 0 < a0 -/
theorem a0_pos (κ c G_N ρ : ℝ) (hκ : 0 < κ) (hc : 0 < c) (hG : 0 < G_N) (hρ : 0 < ρ) :
    0 < a0 κ c G_N ρ := by
  unfold a0
  positivity

/-- positivity of the horizon normalization: 0 < Z_H -/
theorem z_pos (c G_E G_N ρ κ : ℝ) (hκ : 0 < κ) (hc : 0 < c) (hGE : 0 < G_E) (hG : 0 < G_N)
    (hρ : 0 < ρ) : 0 < Z c G_E G_N ρ κ := by
  unfold Z HL Λeff a0
  positivity

/-- master identity: Z_H² = 8π G_E / (3 G_N κ²) (exact, G_E and G_N carried separately) -/
theorem z_sq (c G_E G_N ρ κ : ℝ) (hκ : 0 < κ) (hc : 0 < c) (hGE : 0 < G_E) (hG : 0 < G_N)
    (hρ : 0 < ρ) : (Z c G_E G_N ρ κ) ^ 2 = 8 * Real.pi * G_E / (3 * G_N * κ ^ 2) := by
  unfold Z HL Λeff a0
  have hpi : 0 < Real.pi := Real.pi_pos
  have hΛ3 : 0 ≤ (8 * Real.pi * G_E * ρ / c ^ 2) / 3 := by positivity
  have hGρ : 0 ≤ G_N * ρ := by positivity
  have hsq1 : (Real.sqrt ((8 * Real.pi * G_E * ρ / c ^ 2) / 3)) ^ 2 =
      (8 * Real.pi * G_E * ρ / c ^ 2) / 3 := Real.sq_sqrt hΛ3
  have hsq2 : (Real.sqrt (G_N * ρ)) ^ 2 = G_N * ρ := Real.sq_sqrt hGρ
  rw [div_pow, mul_pow, mul_pow, mul_pow, mul_pow, hsq1, hsq2]
  field_simp [hκ.ne', hc.ne', hG.ne', hρ.ne']

/-- redundant constraint: κ · Z_H = sqrt(8π G_E / (3 G_N)); Z_H and κ are NOT independent
    fitted constants (one-dimensional constraint) -/
theorem kappa_mul_z (c G_E G_N ρ κ : ℝ) (hκ : 0 < κ) (hc : 0 < c) (hGE : 0 < G_E)
    (hG : 0 < G_N) (hρ : 0 < ρ) :
    κ * Z c G_E G_N ρ κ = Real.sqrt (8 * Real.pi * G_E / (3 * G_N)) := by
  have hsq : (κ * Z c G_E G_N ρ κ) ^ 2 = 8 * Real.pi * G_E / (3 * G_N) := by
    rw [mul_pow, z_sq c G_E G_N ρ κ hκ hc hGE hG hρ]
    field_simp [hκ.ne']
  have hpos : 0 ≤ κ * Z c G_E G_N ρ κ := le_of_lt (mul_pos hκ (z_pos c G_E G_N ρ κ hκ hc hGE hG hρ))
  rw [← Real.sqrt_sq hpos]
  rw [hsq]

/-- explicit form: Z_H = sqrt(8π G_E / (3 G_N)) / κ -/
theorem z_explicit (c G_E G_N ρ κ : ℝ) (hκ : 0 < κ) (hc : 0 < c) (hGE : 0 < G_E)
    (hG : 0 < G_N) (hρ : 0 < ρ) :
    Z c G_E G_N ρ κ = Real.sqrt (8 * Real.pi * G_E / (3 * G_N)) / κ := by
  have hm := kappa_mul_z c G_E G_N ρ κ hκ hc hGE hG hρ
  calc
    Z c G_E G_N ρ κ = (κ * Z c G_E G_N ρ κ) / κ := by field_simp [ne_of_gt hκ]
    _ = Real.sqrt (8 * Real.pi * G_E / (3 * G_N)) / κ := by rw [hm]

/-- κ = 1/2 specialization: Z_H² = 32π G_E / (3 G_N) -/
theorem z_sq_half (c G_E G_N ρ : ℝ) (hc : 0 < c) (hGE : 0 < G_E) (hG : 0 < G_N) (hρ : 0 < ρ) :
    (Z c G_E G_N ρ (1 / 2)) ^ 2 = 32 * Real.pi * G_E / (3 * G_N) := by
  have h := z_sq c G_E G_N ρ (1 / 2) (by norm_num) hc hGE hG hρ
  calc
    (Z c G_E G_N ρ (1 / 2)) ^ 2 = 8 * Real.pi * G_E / (3 * G_N * (1 / 2) ^ 2) := h
    _ = 32 * Real.pi * G_E / (3 * G_N) := by ring

/-- κ = 1/2, G_E = G_N: Z_H² = 32π/3 (the task's reduction) -/
theorem z_sq_half_GE_GN (c G ρ : ℝ) (hc : 0 < c) (hG : 0 < G) (hρ : 0 < ρ) :
    (Z c G G ρ (1 / 2)) ^ 2 = 32 * Real.pi / 3 := by
  have h := z_sq_half c G G ρ hc hG hG hρ
  calc
    (Z c G G ρ (1 / 2)) ^ 2 = 32 * Real.pi * G / (3 * G) := h
    _ = 32 * Real.pi / 3 := by field_simp [hG.ne']

/-- κ = 1/2, G_E = G_N: Z_H = sqrt(32π/3) ≈ 5.78881 (Z_H is positive) -/
theorem z_half_value (c G ρ : ℝ) (hc : 0 < c) (hG : 0 < G) (hρ : 0 < ρ) :
    Z c G G ρ (1 / 2) = Real.sqrt (32 * Real.pi / 3) := by
  have hpos : 0 ≤ Z c G G ρ (1 / 2) :=
    le_of_lt (z_pos c G G ρ (1 / 2) (by norm_num) hc hG hG hρ)
  rw [← Real.sqrt_sq hpos]
  rw [z_sq_half_GE_GN c G ρ hc hG hρ]

/-- κ = 1/2, arbitrary G_E/G_N: Z_H = sqrt(32π G_E / (3 G_N)) -/
theorem z_half_value_ratio (c G_E G_N ρ : ℝ) (hc : 0 < c) (hGE : 0 < G_E) (hG : 0 < G_N)
    (hρ : 0 < ρ) : Z c G_E G_N ρ (1 / 2) = Real.sqrt (32 * Real.pi * G_E / (3 * G_N)) := by
  have hpos : 0 ≤ Z c G_E G_N ρ (1 / 2) :=
    le_of_lt (z_pos c G_E G_N ρ (1 / 2) (by norm_num) hc hGE hG hρ)
  rw [← Real.sqrt_sq hpos]
  rw [z_sq_half c G_E G_N ρ hc hGE hG hρ]

/-- R_dS = c / H_L = sqrt(3 / Λ_eff): the de Sitter radius uses the framework Lambda rate only -/
theorem rds_sqrt3 (c Λ : ℝ) (hc : 0 < c) (hΛ : 0 < Λ) :
    c / (c * Real.sqrt (Λ / 3)) = Real.sqrt (3 / Λ) := by
  have h1 : (c / (c * Real.sqrt (Λ / 3))) ^ 2 = 3 / Λ := by
    rw [div_pow, mul_pow]
    have hsq : (Real.sqrt (Λ / 3)) ^ 2 = Λ / 3 := by
      exact Real.sq_sqrt (by positivity : 0 ≤ Λ / 3)
    rw [hsq]
    field_simp [hc.ne', hΛ.ne']
  have hpos : 0 ≤ c / (c * Real.sqrt (Λ / 3)) := by positivity
  rw [← Real.sqrt_sq hpos]
  rw [h1]

/-- Λ_eff expressed through a0: Λ_eff = 8π G_E a0² / (κ² G_N c⁴);
    at κ = 1/2: Λ_eff = 32π G_E a0² / (G_N c⁴) — the framework contract's Lambda -/
theorem lambda_eff_from_a0 (κ c G_E G_N ρ : ℝ) (hκ : 0 < κ) (hc : 0 < c) (hGE : 0 < G_E)
    (hG : 0 < G_N) (hρ : 0 < ρ) :
    Λeff G_E ρ c = 8 * Real.pi * G_E * (a0 κ c G_N ρ) ^ 2 / (κ ^ 2 * c ^ 4 * G_N) := by
  unfold Λeff a0
  have hpi : 0 < Real.pi := Real.pi_pos
  have hGρ : 0 ≤ G_N * ρ := by positivity
  have hsq : (Real.sqrt (G_N * ρ)) ^ 2 = G_N * ρ := Real.sq_sqrt hGρ
  rw [mul_pow, mul_pow, hsq]
  field_simp [hκ.ne', hc.ne', hG.ne', hρ.ne']

/-- ρ from a0 at κ = 1/2: a0² = G ρ c² / 4, i.e. ρ = 4 a0² / (G c²), the framework's
    rho_Lambda mass density -/
theorem rho_from_a0_half (c G ρ : ℝ) (_hc : 0 < c) (hG : 0 < G) (hρ : 0 < ρ) :
    (a0 (1 / 2) c G ρ) ^ 2 = (G * ρ) * c ^ 2 / 4 := by
  unfold a0
  have hGρ : 0 ≤ G * ρ := by positivity
  have hsq : (Real.sqrt (G * ρ)) ^ 2 = G * ρ := Real.sq_sqrt hGρ
  rw [mul_pow, mul_pow, hsq]
  ring

#print axioms z_sq
#print axioms kappa_mul_z
#print axioms z_explicit
#print axioms z_sq_half
#print axioms z_sq_half_GE_GN
#print axioms z_half_value
#print axioms z_half_value_ratio
#print axioms rds_sqrt3
#print axioms lambda_eff_from_a0
#print axioms rho_from_a0_half

end AS005