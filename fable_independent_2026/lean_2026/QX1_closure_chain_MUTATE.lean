import Mathlib.Analysis.SpecialFunctions.Log.Deriv
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Deriv
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Analysis.Real.Pi.Bounds
import Mathlib.Tactic

/-!
# QX1 MUTATE twin (must fail exactly on M1-M4): the equation chain of v3s and AC2q, algebraic steps (2026-11-06)

Criteria: closure_2026_11_06/QX1_equation_chain/FROZEN_CRITERIA.md (0bc8da973b). Kappa = 1/2 FITTED; not theory closed.
Each theorem is one algebraic step of closure_2026_11_06/EQUATIONS_IN_ORDER.md. Physical premises are hypotheses.
Steps already certified elsewhere are cited there, not re-proved: a0 = c²√(Λ/32π) (TOE_BEST_ATTEMPT_2026_10_12),
κ = ½ not derivable (KAPPA_LOGIC_2026_10_20), the switched-stiffness WKB facts and the α ≡ 1 law (V3_PICTURE_2026_10_23),
leaf convexity (XC2, XC5).

1. J(Y) = Λ − 2a²[u − ln(1+u)], u = √Y/a: dJ/du, J_Y = −1/(1+u), 1 + J_Y = μ(u) = u/(1+u).
2. The simple-μ law S: g² = g_N(g + a₀); positive root, uniqueness, g_N < g < g_N + a₀, exact Tully–Fisher
   v⁴ = GM(a₀ + v²/r).
3. The a₀ tie at κ = ½ and the clock bound s² ≤ 2ρ_DE: s² ≤ 8a₀²/(Gc²).
4. AC2q's stiffness −(γ/2)[max(d + 2X, 0)² − (2X)²]: v3s at X = 0, on/off pieces, continuity at the switch, zero on
   an FRW background (d = 0), and the planar charge form at N = 1 (AC10 S1).
5. AC10 A2: the clock-only stream J = 1 − A sin(Ωτ) solves J'' = Ω²(1 − J); it folds iff A ≥ 1 iff Ωτ_f ≤ 1.
6. AC9: the massive tensor dispersion gives 1 − v_g²/c² = m²c²/ω², the new masses vanish at s = 0, and the record's
   largest masses give dv/c < 2e-46 at 100 Hz, inside the GW170817 band.
-/

open Real

namespace QX1M

/-! ## 1. The postulated J(Y) and the AQUAL kernel -/

/-- J as a function of u = √Y/a (POSTULATED input). -/
noncomputable def Jfun (Λ a u : ℝ) : ℝ := Λ - 2 * a ^ 2 * (u - Real.log (1 + u))

/-- the simple μ -/
noncomputable def mu (x : ℝ) : ℝ := x / (1 + x)

theorem J_hasDerivAt (Λ a u : ℝ) (hu : 0 ≤ u) :
    HasDerivAt (Jfun Λ a) (-2 * a ^ 2 * (u / (1 + u))) u := by
  have h1 : (1 + u) ≠ 0 := by linarith
  have hlog : HasDerivAt (fun v => Real.log (1 + v)) (1 / (1 + u)) u := by
    have := ((hasDerivAt_id u).const_add 1).log h1
    simpa using this
  have hin : HasDerivAt (fun v => v - Real.log (1 + v)) (1 - 1 / (1 + u)) u :=
    (hasDerivAt_id u).sub hlog
  have hJ := (hin.const_mul (2 * a ^ 2)).const_sub Λ
  have key : 1 - 1 / (1 + u) = u / (1 + u) := by
    rw [eq_div_iff h1, sub_mul, div_mul_cancel₀ (1 : ℝ) h1]; ring
  have hJ' : HasDerivAt (fun x => Λ - 2 * a ^ 2 * (x - Real.log (1 + x))) (-2 * a ^ 2 * (u / (1 + u))) u :=
    hJ.congr_deriv (by rw [key]; ring)
  exact hJ'

/-- J_Y = (dJ/du)/(dY/du) with Y = a²u²: equals −1/(1+u). -/
theorem JY_value (a u : ℝ) (ha : a ≠ 0) (hu : 0 < u) :
    (-2 * a ^ 2 * (u / (1 + u))) / (2 * a ^ 2 * u) = -1 / (1 + u) := by
  have h1 : (1 + u) ≠ 0 := by linarith
  have hu0 : u ≠ 0 := hu.ne'
  have ha2 : a ^ 2 ≠ 0 := pow_ne_zero 2 ha
  rw [div_eq_iff (mul_ne_zero (mul_ne_zero two_ne_zero ha2) hu0)]
  ring

/-- 1 + J_Y = μ(u): the khronon term turns GR's ∇·∇Ξ into AQUAL's ∇·(μ∇Ξ). -/
theorem one_add_JY_is_mu (u : ℝ) (hu : 0 ≤ u) : 1 + (-1 / (1 + u)) = 1 / (1 + u) := by  -- MUTATION M2
  have h1 : (1 + u) ≠ 0 := by linarith
  unfold mu; field_simp; ring

/-- deep regime: x − x² ≤ μ(x) ≤ x -/
theorem mu_deep (x : ℝ) (hx : 0 ≤ x) : x - x ^ 2 ≤ mu x ∧ mu x ≤ x := by
  have h1 : 0 < 1 + x := by linarith
  unfold mu
  constructor
  · rw [le_div_iff₀ h1]; nlinarith [sq_nonneg x, mul_nonneg hx (sq_nonneg x)]
  · rw [div_le_iff₀ h1]; nlinarith

/-- Newtonian regime: 1 − 1/x ≤ μ(x) < 1 -/
theorem mu_newton (x : ℝ) (hx : 0 < x) : 1 - 1 / x ≤ mu x ∧ mu x < 1 := by
  have h1 : 0 < 1 + x := by linarith
  unfold mu
  constructor
  · rw [le_div_iff₀ h1, sub_mul, div_mul_eq_mul_div, one_mul]
    rw [show (1 + x) / x = 1 / x + 1 by field_simp]
    nlinarith [div_pos one_pos hx]
  · rw [div_lt_one h1]; linarith

/-! ## 2. The simple-μ law S -/

/-- the balance μ(g/a₀) g = g_N is law S: g² = g_N (g + a₀) -/
theorem balance_iff_lawS (g gN a0 : ℝ) (hg : 0 ≤ g) (ha : 0 < a0) :
    mu (g / a0) * g = gN ↔ g ^ 2 = gN * (g + a0) := by
  have h1 : 0 < 1 + g / a0 := by positivity
  have h2 : 0 < g + a0 := by linarith
  have key : mu (g / a0) * g = g ^ 2 / (g + a0) := by
    unfold mu; field_simp; ring
  rw [key, div_eq_iff h2.ne']

/-- the positive root of law S -/
noncomputable def lawSroot (gN a0 : ℝ) : ℝ := (gN + Real.sqrt (gN ^ 2 + 4 * gN * a0)) / 2

theorem lawS_root_solves (gN a0 : ℝ) (hN : 0 ≤ gN) (ha : 0 ≤ a0) :
    (lawSroot gN a0) ^ 2 = gN * (lawSroot gN a0 + a0) := by
  have hD : 0 ≤ gN ^ 2 + 4 * gN * a0 := by positivity
  have hs := Real.sq_sqrt hD
  unfold lawSroot
  nlinarith [hs]

theorem lawS_root_pos (gN a0 : ℝ) (hN : 0 < gN) (ha : 0 ≤ a0) : 0 < lawSroot gN a0 := by
  unfold lawSroot
  have := Real.sqrt_nonneg (gN ^ 2 + 4 * gN * a0)
  linarith

/-- the positive solution of law S is unique -/
theorem lawS_unique (g₁ g₂ gN a0 : ℝ) (hN : 0 ≤ gN) (ha : 0 ≤ a0) (h1 : 0 < g₁) (h2 : 0 < g₂)
    (e1 : g₁ ^ 2 = gN * (g₁ + a0)) (e2 : g₂ ^ 2 = gN * (g₂ + a0)) : g₁ = g₂ := by
  have : (g₁ - g₂) * (g₁ + g₂ - gN) = 0 := by nlinarith
  rcases mul_eq_zero.mp this with h | h
  · linarith
  · -- g₁ + g₂ = gN gives g₁ < gN, so g₁² − gN g₁ < 0 ≤ gN a0: contradiction
    have hg1 : g₁ < gN := by linarith
    nlinarith [mul_nonneg hN ha, mul_pos h1 (sub_pos.2 hg1)]

/-- law S bounds: g_N < g < g_N + a₀ -/
theorem lawS_bounds (g gN a0 : ℝ) (hN : 0 < gN) (ha : 0 < a0) (hg : 0 < g)
    (e : g ^ 2 = gN * (g + a0)) : g < gN ∧ g < gN + a0 := by  -- MUTATION M4
  constructor
  · by_contra h
    push Not at h
    have : g ^ 2 ≤ gN * g := by nlinarith
    nlinarith [mul_pos hN ha]
  · by_contra h
    push Not at h
    have : g * (gN + a0) ≤ g * g := mul_le_mul_of_nonneg_left h hg.le
    have : gN * (g + a0) < g * (gN + a0) := by nlinarith [mul_pos hg ha, mul_pos hN ha]
    nlinarith

/-- exact Tully–Fisher of law S: with g = v²/r, g_N = GM/r², v⁴ = GM(a₀ + v²/r); flat rotation → v⁴ = GMa₀ -/
theorem lawS_tully_fisher (v r G M a0 : ℝ) (hr : 0 < r)
    (e : (v ^ 2 / r) ^ 2 = (G * M / r ^ 2) * (v ^ 2 / r + a0)) :
    v ^ 4 = G * M * (a0 + v ^ 2 / r) := by
  have hr2 : r ^ 2 ≠ 0 := by positivity
  field_simp at e
  field_simp
  nlinarith [e]

/-! ## 3. The a₀ tie and the clock bound -/

/-- a₀² = κ²Gρc² at κ = ½ gives ρ = 4a₀²/(Gc²); the clock bound s² ≤ 2ρ is s² ≤ 8a₀²/(Gc²) (κ FITTED) -/
theorem clock_bound (a0 G ρ c s2 : ℝ) (hG : 0 < G) (hc : 0 < c)
    (tie : a0 ^ 2 = (1 / 2) ^ 2 * G * ρ * c ^ 2) (hs : s2 ≤ 2 * ρ) :
    ρ = 4 * a0 ^ 2 / (G * c ^ 2) ∧ s2 ≤ 8 * a0 ^ 2 / (G * c ^ 2) := by
  have hGc : 0 < G * c ^ 2 := by positivity
  have hρ : ρ = 4 * a0 ^ 2 / (G * c ^ 2) := by
    rw [eq_div_iff hGc.ne']; nlinarith [tie]
  refine ⟨hρ, ?_⟩
  rw [hρ] at hs
  calc s2 ≤ 2 * (4 * a0 ^ 2 / (G * c ^ 2)) := hs
    _ = 8 * a0 ^ 2 / (G * c ^ 2) := by ring

/-! ## 4. AC2q's stiffness -/

/-- AC2q stiffness density −(γ/2)[max(d + 2X, 0)² − (2X)²], d = D·P -/
noncomputable def stiffQ (γ d X : ℝ) : ℝ := -(γ / 2) * ((max (d + 2 * X) 0) ^ 2 - (2 * X) ^ 2)

/-- v3s's switched stiffness −(γ/2)max(d, 0)² -/
noncomputable def stiffV3s (γ d : ℝ) : ℝ := -(γ / 2) * (max d 0) ^ 2

theorem ac2q_reduces_to_v3s (γ d : ℝ) : stiffQ γ d 0 = stiffV3s γ d := by
  unfold stiffQ stiffV3s; simp

theorem ac2q_on (γ d X : ℝ) (h : 0 ≤ d + 2 * X) :
    stiffQ γ d X = -(γ / 2) * d ^ 2 + (-2 * γ * X * d) := by
  unfold stiffQ; rw [max_eq_left h]; ring

theorem ac2q_off (γ d X : ℝ) (h : d + 2 * X ≤ 0) : stiffQ γ d X = -2 * γ * X ^ 2 := by  -- MUTATION M1
  unfold stiffQ; rw [max_eq_right h]; ring

theorem ac2q_continuous_at_switch (γ X : ℝ) :
    -(γ / 2) * (-2 * X) ^ 2 + (-2 * γ * X * (-2 * X)) = 2 * γ * X ^ 2 := by ring

/-- on FRW (d = D·P = 0, X ≥ 0) the stiffness vanishes: the background is the canonical scalar's -/
theorem ac2q_frw_background (γ X : ℝ) (hX : 0 ≤ X) : stiffQ γ 0 X = 0 := by
  unfold stiffQ; rw [max_eq_left (by linarith)]; ring

/-- unitary gauge X = s²/(2N²) is non-negative -/
theorem X_nonneg (s N : ℝ) : 0 ≤ s ^ 2 / (2 * N ^ 2) := by positivity

/-- AC10 S1 at N = 1: X = s²/2, so the switch variable is the charge Π = d + s² and P sees Π − s² -/
theorem ac10_charge_form (γ d s : ℝ) :
    stiffQ γ d (s ^ 2 / (2 * 1 ^ 2)) = -(γ / 2) * ((max (d + s ^ 2) 0) ^ 2 - (s ^ 2) ^ 2) := by
  unfold stiffQ; ring_nf

/-! ## 5. AC10 A2: the clock-only fold threshold -/

/-- clock-only stream after the sheet kick -/
noncomputable def Jstream (A Ω τ : ℝ) : ℝ := 1 - A * Real.sin (Ω * τ)

theorem Jstream_hasDerivAt (A Ω t : ℝ) :
    HasDerivAt (Jstream A Ω) (-(A * Ω * Real.cos (Ω * t))) t := by
  have h := ((((hasDerivAt_id' t).const_mul Ω).sin).const_mul A).const_sub 1
  have h' : HasDerivAt (fun x => 1 - A * Real.sin (Ω * x)) (-(A * Ω * Real.cos (Ω * t))) t :=
    h.congr_deriv (by ring)
  exact h'

theorem Jstream_ode (A Ω τ : ℝ) :
    HasDerivAt (fun t => deriv (Jstream A Ω) t) (Ω ^ 2 * (1 - Jstream A Ω τ)) τ := by
  have hd : (fun t => deriv (Jstream A Ω) t) = fun t => -(A * Ω * Real.cos (Ω * t)) := by
    funext t; exact (Jstream_hasDerivAt A Ω t).deriv
  rw [hd]
  have h := ((((hasDerivAt_id' τ).const_mul Ω).cos).const_mul (A * Ω)).neg
  have h3 : HasDerivAt (fun y => -(A * Ω * Real.cos (Ω * y))) (-(A * Ω * (-Real.sin (Ω * τ) * (Ω * 1)))) τ := h
  refine h3.congr_deriv ?_
  show _ = Ω ^ 2 * (1 - (1 - A * Real.sin (Ω * τ)))
  ring

theorem Jstream_initial (A Ω : ℝ) : Jstream A Ω 0 = 1 := by unfold Jstream; simp

/-- the stream folds (J reaches ≤ 0 at some τ ≥ 0) iff A ≥ 1 -/
theorem fold_iff_amplitude (A Ω : ℝ) (hA : 0 < A) (hΩ : 0 < Ω) :
    (∃ τ, 0 ≤ τ ∧ Jstream A Ω τ ≤ 0) ↔ 1 ≤ A := by
  constructor
  · rintro ⟨τ, -, h⟩
    unfold Jstream at h
    have := Real.sin_le_one (Ω * τ)
    nlinarith
  · intro h
    refine ⟨π / 2 / Ω, by positivity, ?_⟩
    unfold Jstream
    rw [show Ω * (π / 2 / Ω) = π / 2 by field_simp, Real.sin_pi_div_two]
    linarith

/-- with A = KΣ/(wΩ) and the free-stream fold time τ_f = w/(KΣ), A = 1/(Ωτ_f): folds iff Ωτ_f ≤ 1 -/
theorem fold_iff_threshold (Ω τf : ℝ) (hΩ : 0 < Ω) (hτ : 0 < τf) :
    (∃ τ, 0 ≤ τ ∧ Jstream (1 / (Ω * τf)) Ω τ ≤ 0) ↔ Ω * τf ≤ 1 / Real.sqrt 2 := by  -- MUTATION M3
  have hp : 0 < Ω * τf := mul_pos hΩ hτ
  rw [fold_iff_amplitude _ _ (by positivity) hΩ, le_div_iff₀ hp, one_mul]

/-! ## 6. AC9: tensor masses -/

/-- massive dispersion ω² = c²k² + m²c², group velocity c²k/ω: 1 − v_g²/c² = m²c²/ω² -/
theorem tensor_group_velocity (c k m ω : ℝ) (hc : c ≠ 0) (hω : ω ≠ 0)
    (disp : ω ^ 2 = c ^ 2 * k ^ 2 + m ^ 2 * c ^ 2) :
    1 - (c ^ 2 * k / ω) ^ 2 / c ^ 2 = m ^ 2 * c ^ 2 / ω ^ 2 := by
  field_simp
  rw [disp]; ring

/-- AC9's new masses vanish at s = 0 (AC2q = v3s's tensor sector) -/
theorem ac9_masses_vanish (γ Gxx Gyy Az P0z : ℝ) :
    16 * π * γ * (0 : ℝ) ^ 2 * (Gxx + Gyy - Az * P0z) = 0 ∧ 8 * π * γ * (0 : ℝ) ^ 4 = 0 := by
  constructor <;> ring

/-- record numbers: m² ≤ 1.7e-57 m⁻² (alt) and 1.1e-57 (canonical), f = 100 Hz, c = 2.99792458e8:
    m²c²/(2ω²) < 2e-46 (alt) and < 1.3e-46 (canonical), inside the GW170817 band (7e-16) -/
theorem ac9_dv_bounds :
    (17 / 10 * (10 : ℝ) ^ (-57 : ℤ)) * (299792458 : ℝ) ^ 2 / (2 * (2 * (314 / 100) * 100) ^ 2) < 2 * (10 : ℝ) ^ (-46 : ℤ) ∧
    (11 / 10 * (10 : ℝ) ^ (-57 : ℤ)) * (299792458 : ℝ) ^ 2 / (2 * (2 * (314 / 100) * 100) ^ 2) < 13 / 10 * (10 : ℝ) ^ (-46 : ℤ) ∧
    2 * (10 : ℝ) ^ (-46 : ℤ) < 7 * (10 : ℝ) ^ (-16 : ℤ) := by
  refine ⟨?_, ?_, ?_⟩ <;> norm_num

/-- the bound above used π > 3.14 (ω = 2πf ≥ 2·3.14·f), so the true dv/c is smaller -/
theorem omega_lower (f : ℝ) (hf : 0 < f) : (2 * (314 / 100) * f) ^ 2 ≤ (2 * π * f) ^ 2 := by
  have : (314 / 100 : ℝ) < π := by have := Real.pi_gt_d2; norm_num at this ⊢; linarith
  have h : 2 * (314 / 100) * f ≤ 2 * π * f := by nlinarith
  exact pow_le_pow_left₀ (by positivity) h 2

end QX1M

#print axioms QX1M.J_hasDerivAt
#print axioms QX1M.JY_value
#print axioms QX1M.one_add_JY_is_mu
#print axioms QX1M.mu_deep
#print axioms QX1M.mu_newton
#print axioms QX1M.balance_iff_lawS
#print axioms QX1M.lawS_root_solves
#print axioms QX1M.lawS_root_pos
#print axioms QX1M.lawS_unique
#print axioms QX1M.lawS_bounds
#print axioms QX1M.lawS_tully_fisher
#print axioms QX1M.clock_bound
#print axioms QX1M.ac2q_reduces_to_v3s
#print axioms QX1M.ac2q_on
#print axioms QX1M.ac2q_off
#print axioms QX1M.ac2q_continuous_at_switch
#print axioms QX1M.ac2q_frw_background
#print axioms QX1M.X_nonneg
#print axioms QX1M.ac10_charge_form
#print axioms QX1M.Jstream_hasDerivAt
#print axioms QX1M.Jstream_ode
#print axioms QX1M.Jstream_initial
#print axioms QX1M.fold_iff_amplitude
#print axioms QX1M.fold_iff_threshold
#print axioms QX1M.tensor_group_velocity
#print axioms QX1M.ac9_masses_vanish
#print axioms QX1M.ac9_dv_bounds
#print axioms QX1M.omega_lower
