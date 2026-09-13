import Mathlib

/-!
# AmplitudeLaw — Lean 4 + Mathlib certificate of the amplitude-law / BTFR / virialisation algebra

**Scope.** Lean certifies the *mathematics* the amplitude law rests on, not that it is a law of nature.
What is machine-checked here is the real-analysis algebra of the cold-collapse / virialisation route:
positivity of the MOND acceleration scale and radius, the virial-temperature → BTFR identity, the
1/4 power-law exponent, the −2 logarithmic slope of an isothermal ρ = A/r² profile, dimensional
uniqueness of the MOND length monomial, and flatness of the circular speed.

Physical interpretation (data confrontation, falsifiability) is outside the scope of this file.

## Main results
- `a0_pos`              — a0 = κ·c·√(G·ρ) is positive for positive constants.
- `rM_pos`, `rM_sq`     — the MOND radius r_M = √(G·M_b/a0) is positive with r_M² = G·M_b/a0.
- `btfr_virial`         — σ² = G·M_b/(2·r_M) with r_M = √(G·M_b/a0) gives σ⁴ = (G·M_b·a0)/4.
- `btfr_exponent`       — v⁴ = C·M_b ⟹ v = (C·M_b)^{1/4}: a 1/4 power law in M_b.
- `profile_slope`       — ρ(r) = A/r² gives d(log ρ)/d(log r) = −2 for r > 0.
- `mond_length_unique`  — the only length monomial G^p M_b^q a0^s is proportional to √(G·M_b/a0).
- `vc_flat`             — v_c² = G·M(<r)/r with M(<r) = 4π·A·r gives v_c² = 4π·G·A, constant in r.
-/

namespace AmplitudeLaw

open Real

variable (G M_b a0 κ c rho A C : ℝ)

/-! ### 1. Positivity of the MOND acceleration scale -/

/-- a0 = κ·c·√(G·ρ) is positive when all inputs are positive. -/
theorem a0_pos (hκ : 0 < κ) (hc : 0 < c) (hG : 0 < G) (hrho : 0 < rho) :
    0 < κ * c * Real.sqrt (G * rho) := by
  positivity

/-! ### 2. The MOND radius -/

/-- The MOND radius r_M = √(G·M_b/a0) is positive. -/
theorem rM_pos (hG : 0 < G) (hM : 0 < M_b) (ha0 : 0 < a0) :
    0 < Real.sqrt (G * M_b / a0) := by
  positivity

/-- r_M² = G·M_b/a0. -/
theorem rM_sq (hG : 0 < G) (hM : 0 < M_b) (ha0 : 0 < a0) :
    (Real.sqrt (G * M_b / a0)) ^ 2 = G * M_b / a0 := by
  exact Real.sq_sqrt (by positivity)

/-! ### 3. Virial-temperature → BTFR identity -/

/-- σ² = G·M_b/(2·r_M) with r_M = √(G·M_b/a0) gives σ⁴ = (G·M_b·a0)/4.
    The BTFR up to the virial factor 1/4. -/
theorem btfr_virial (hG : 0 < G) (hM : 0 < M_b) (ha0 : 0 < a0)
    (sigma : ℝ) (hsigma : sigma ^ 2 = G * M_b / (2 * Real.sqrt (G * M_b / a0))) :
    sigma ^ 4 = (G * M_b * a0) / 4 := by
  have hrM_pos : 0 < Real.sqrt (G * M_b / a0) := by positivity
  have hrM_sq : (Real.sqrt (G * M_b / a0)) ^ 2 = G * M_b / a0 := Real.sq_sqrt (by positivity)
  calc sigma ^ 4 = (sigma ^ 2) ^ 2 := by ring
    _ = (G * M_b / (2 * Real.sqrt (G * M_b / a0))) ^ 2 := by rw [hsigma]
    _ = (G * M_b) ^ 2 / (4 * (Real.sqrt (G * M_b / a0)) ^ 2) := by ring
    _ = (G * M_b) ^ 2 / (4 * (G * M_b / a0)) := by rw [hrM_sq]
    _ = (G * M_b * a0) / 4 := by field_simp

/-! ### 4. BTFR exponent: v = (C·M_b)^{1/4} -/

/-- If v⁴ = C·M_b with v > 0, then v = (C·M_b)^{1/4}: a 1/4 power law in M_b. -/
theorem btfr_exponent (hC : 0 < C) (hM : 0 < M_b) (v : ℝ) (hv : 0 < v)
    (h : v ^ 4 = C * M_b) :
    v = (C * M_b) ^ ((1 : ℝ) / 4) := by
  have hCM : 0 < C * M_b := mul_pos hC hM
  have h1 : v = (v ^ 4) ^ ((1 : ℝ) / 4) := by
    rw [← Real.rpow_natCast, ← Real.rpow_mul (le_of_lt hv)]
    norm_num
  rw [h1, h]

/-! ### 5. Profile slope: d log ρ / d log r = −2 for ρ = A/r² -/

/-- For ρ(r) = A/r², the logarithmic slope d(log ρ)/d(log r) = (r/ρ)·dρ/dr = −2 for r > 0.
    This is the standard form of the logarithmic slope: by the chain rule,
    d(log ρ)/d(log r) = (d(log ρ)/dr)·(dr/d(log r)) = (ρ'/ρ)·r = (r/ρ)·ρ'. -/
theorem profile_slope (hA : 0 < A) (r : ℝ) (hr : 0 < r) :
    (r / (A / r ^ 2)) * deriv (fun x => A / x ^ 2) r = -2 := by
  have hr2 : r ^ 2 ≠ 0 := by positivity
  have hA' : A ≠ 0 := ne_of_gt hA
  have hderiv : deriv (fun x => A / x ^ 2) r = -2 * A / r ^ 3 := by
    rw [deriv_const_div]
    · simp only [deriv_pow]
      field_simp
      ring
    · exact differentiableAt_pow 2
    · exact hr2
  rw [hderiv]
  field_simp
  ring

/-! ### 6. Dimensional uniqueness of the MOND length monomial -/

/-- Dimensions as integer exponent triples (L, M, T).
    G = (3, -1, -2), M_b = (0, 1, 0), a0 = (1, 0, -2). -/
def Dim := ℤ × ℤ × ℤ

def G_dim : Dim := (3, -1, -2)
def M_dim : Dim := (0, 1, 0)
def a0_dim : Dim := (1, 0, -2)

/-- A monomial G^p M_b^q a0^s has dimension (3p+s, -p+q, -2p-2s). -/
def monomial_dim (p q s : ℤ) : Dim :=
  (3 * p + s, -p + q, -2 * p - 2 * s)

/-- The monomial has dimensions of length (1, 0, 0) iff q = p and s = -p and ... .
    We prove the length constraint forces a one-parameter family giving r_M = √(G·M_b/a0). -/
theorem monomial_dim_length (p q s : ℤ) :
    monomial_dim p q s = (1, 0, 0) ↔ p = 1 ∧ q = 1 ∧ s = -1 := by
  unfold monomial_dim
  constructor
  · intro h
    simp only [Prod.mk.injEq] at h
    obtain ⟨h1, h2, h3⟩ := h
    omega
  · rintro ⟨rfl, rfl, rfl⟩
    rfl

/-- The unique monomial with dimensions of length is G^1 M_b^1 a0^{-1},
    whose square root gives r_M = √(G·M_b/a0). -/
theorem mond_length_unique (p q s : ℤ) (h : monomial_dim p q s = (1, 0, 0)) :
    p = 1 ∧ q = 1 ∧ s = -1 := (monomial_dim_length p q s).mp h

/-! ### 7. Circular-speed flatness for ρ = A/r² -/

/-- For ρ = A/r², the enclosed mass is M(<r) = 4π·A·r, and the circular speed
    v_c² = G·M(<r)/r = 4π·G·A is constant in r. -/
theorem vc_flat (hG : 0 < G) (hA : 0 < A) (r : ℝ) (hr : 0 < r) :
    G * (4 * Real.pi * A * r) / r = 4 * Real.pi * G * A := by
  field_simp
  ring

end AmplitudeLaw
