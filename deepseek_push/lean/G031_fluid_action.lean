/-
  G031 -- THE GR FLUID ACTION AND THE ZIMMERMAN HYDROSTATIC CHAIN --
  the Lean certificate.

  The theory's central rung, now machine-checked: the Zimmerman temperature
  -> the isothermal identification -> the flat curve (BTFR) -> THE DEEP RAR
  g^2 = a0*g_N with coefficient exactly 1.  Companion computational lane:
  G031_gr_fluid_action.py (sympy-exact, V1-V9); this file puts the same
  arrows in Lean with zero sorry.

  The chain, with S := sqrt(G*Mb*a0) treated as the atom:

    rho_L_from_a0          the scaling closes: (c/2)*sqrt(G rho_L) = a0
                           <-> rho_L = 4a0^2/(Gc^2)   [V1, V2 via lambda_geom_fixed]
    zimmerman_temperature  sigma^2 = G*Mb/(2 r_M) = S/2 EXACTLY
                           (sqrt composition: sqrt(GMb/a0)*sqrt(GMb a0) = GMb)
                           [V3]
    phantom_is_isothermal  sigma^2/(2 pi G r^2) = S/(4 pi G r^2)  [V4]
    enclosed_mass_*        M(r) := S*r/G = 2 sigma^2 r / G satisfies
                           M' = 4 pi r^2 rho with M(0) = 0, and the integral
                           form int_0^r 4 pi t^2 rho(t) dt = S r/G   [V5]
    btfr                   G*M(r)/r = 2 sigma^2 = S  (BTFR, v^4 = G Mb a0)
                           [V5 second half]
    deep_rar               (S/r)^2 = a0*(G*Mb/r^2)  -- THE DEEP RAR, coeff 1
                           [V6; sqrt-free once S^2 = G Mb a0 is discharged]
    w_window_cold          |(-3)(1+w) - (-3)| = 3|w| < 2e-6 on 0 <= w <= 5.7e-7
                           [G028 V1: the dust's density exponent is a^-3 to
                           within 2e-6 across the whole cold window]
    the_spine              the whole implication chain as one conjunction,
                           mirroring the_equilibrium_spine.

  Strategy (as in EQUILIBRIUM_THEORY.lean): only rho_L_from_a0 and
  zimmerman_temperature touch Real.sqrt; everything downstream is pure
  field_simp/ring in terms of the atom S.  No nonlinear sqrt arithmetic
  anywhere.
-/
import Mathlib

noncomputable section

/-! ## The key lemma — sqrt composition -/

/-- **The key lemma.** For positive G, M, a0:
sqrt(GM/a0) * sqrt(GM a0) = GM — pure sqrt composition:
sqrt x * sqrt y = sqrt(xy) with (GM/a0)(GM a0) = (GM)^2. -/
theorem key_sqrt_composition (G M a0 : ℝ) (hG : 0 < G) (hM : 0 < M) (ha0 : 0 < a0) :
    Real.sqrt (G * M / a0) * Real.sqrt (G * M * a0) = G * M := by
  have hx : 0 ≤ G * M / a0 := by positivity
  have hprod : (G * M / a0) * (G * M * a0) = (G * M) * (G * M) := by
    field_simp
  calc Real.sqrt (G * M / a0) * Real.sqrt (G * M * a0)
      = Real.sqrt ((G * M / a0) * (G * M * a0)) := (Real.sqrt_mul hx _).symm
    _ = Real.sqrt ((G * M) * (G * M)) := by rw [hprod]
    _ = G * M := by
      have hGM : 0 ≤ G * M := by positivity
      exact Real.sqrt_mul_self hGM

/-! ## V1/V2 — the one-constant scaling -/

/-- **rho_L_from_a0 (V1).** The Zimmerman scaling closes in both directions:
(c/2)*sqrt(G rho_L) = a0  <->  rho_L = 4a0^2/(Gc^2). The cosmological
density is not an independent input: it is fixed by the same a0 that sets
the galaxy regime. -/
theorem rho_L_from_a0 (G c a0 rhoL : ℝ) (hG : 0 < G) (hc : 0 < c) (ha0 : 0 < a0) :
    Real.sqrt (G * rhoL) * c / 2 = a0 ↔ rhoL = 4 * a0 ^ 2 / (G * c ^ 2) := by
  constructor
  · intro h
    -- sqrt(G rhoL) = 2a0/c (positive), so squaring gives G rhoL = 4a0^2/c^2
    have hsqrt : Real.sqrt (G * rhoL) = 2 * a0 / c := by
      field_simp at h ⊢
      linarith
    have hGρ : 0 ≤ G * rhoL := by
      have hpos : 0 < Real.sqrt (G * rhoL) := by rw [hsqrt]; positivity
      have hx := (Real.sqrt_pos.mp hpos)
      linarith
    have hsq : Real.sqrt (G * rhoL) ^ 2 = G * rhoL := Real.sq_sqrt hGρ
    have h4 : Real.sqrt (G * rhoL) ^ 2 * c ^ 2 / 4 = a0 ^ 2 := by
      have hs2 : (Real.sqrt (G * rhoL) * c / 2) ^ 2 = a0 ^ 2 := by rw [h]
      have hexp : (Real.sqrt (G * rhoL) * c / 2) ^ 2
          = Real.sqrt (G * rhoL) ^ 2 * c ^ 2 / 4 := by ring
      rw [hexp] at hs2
      exact hs2
    rw [hsq] at h4
    field_simp at h4 ⊢
    linarith
  · intro h
    rw [h]
    -- G * (4a0^2/(Gc^2)) = (2a0/c)^2, and sqrt of a square is the square
    have hexp : G * (4 * a0 ^ 2 / (G * c ^ 2)) = (2 * a0 / c) ^ 2 := by
      field_simp [hc.ne]
      ring
    rw [hexp, Real.sqrt_sq (by positivity : (0:ℝ) ≤ 2 * a0 / c)]
    field_simp [hc.ne]

/-- **lambda_geom_fixed (V2).** The geometric cosmological term:
Lambda = 8 pi G rho_Lambda / c^2 = 32 pi a0^2 / c^4 — fully fixed by a0,
no independent parameter. -/
theorem lambda_geom_fixed (G c a0 : ℝ) (hG : 0 < G) (hc : 0 < c) :
    8 * Real.pi * G * (4 * a0 ^ 2 / (G * c ^ 2)) / c ^ 2 = 32 * Real.pi * a0 ^ 2 / c ^ 4 := by
  field_simp [hG.ne, hc.ne]
  ring

/-! ## V3 — the Zimmerman temperature -/

/-- **zimmerman_temperature (V3).** sigma^2 = G Mb/(2 r_M) with
r_M = sqrt(G Mb/a0) gives sigma^2 = sqrt(G Mb a0)/2 EXACTLY — the
equilibrium temperature is half the geometric mean of the well's depth
and a0. No fitting anywhere. -/
theorem zimmerman_temperature (G Mb a0 : ℝ) (hG : 0 < G) (hMb : 0 < Mb) (ha0 : 0 < a0) :
    G * Mb / (2 * Real.sqrt (G * Mb / a0)) = Real.sqrt (G * Mb * a0) / 2 := by
  have huv := key_sqrt_composition G Mb a0 hG hMb ha0
  have hne : Real.sqrt (G * Mb / a0) ≠ 0 :=
    ne_of_gt (Real.sqrt_pos.mpr (by positivity))
  calc G * Mb / (2 * Real.sqrt (G * Mb / a0))
      = Real.sqrt (G * Mb / a0) * Real.sqrt (G * Mb * a0)
          / (2 * Real.sqrt (G * Mb / a0)) := by rw [huv]
    _ = Real.sqrt (G * Mb * a0) / 2 := by field_simp [hne]

/-! ## V4 — the isothermal identification -/

/-- **phantom_is_isothermal (V4).** The isothermal sphere at temperature
sigma^2 = S/2 has density sigma^2/(2 pi G r^2) = S/(4 pi G r^2) — the G003
phantom, coefficient exactly 1. The halo is the dust at equilibrium. -/
theorem phantom_is_isothermal (S G r σsq : ℝ) (hG : 0 < G) (hr : 0 < r)
    (hσ : σsq = S / 2) :
    σsq / (2 * Real.pi * G * r ^ 2) = S / (4 * Real.pi * G * r ^ 2) := by
  rw [hσ]
  field_simp [Real.pi_ne_zero]
  ring

/-! ## V5 — the enclosed mass and the flat curve -/

/-- **enclosed_mass_derivative (V5, dynamical form).** The enclosed-mass
function M(r) := 2 sigma^2 r/G = S r/G satisfies M'(r) = 4 pi r^2 rho(r)
with rho the isothermal density — i.e. M is THE antiderivative of the
shell integrand. -/
theorem enclosed_mass_derivative (S G r : ℝ) (hG : 0 < G) (hr : 0 < r) :
    HasDerivAt (fun x : ℝ => S * x / G)
      (4 * Real.pi * r ^ 2 * (S / (4 * Real.pi * G * r ^ 2))) r := by
  have hval : 4 * Real.pi * r ^ 2 * (S / (4 * Real.pi * G * r ^ 2)) = S / G := by
    field_simp [Real.pi_ne_zero, hG.ne, hr.ne]
  have hd : HasDerivAt (fun x : ℝ => x * (S / G)) (S / G) r := by
    simpa using (hasDerivAt_id r).mul_const (S / G)
  have hfun : (fun x : ℝ => S * x / G) = fun x : ℝ => x * (S / G) := by
    funext x
    field_simp [hG.ne]
  rw [hval, hfun]
  exact hd

/-- **enclosed_mass_at_zero (V5, boundary condition).** M(0) = 0. -/
theorem enclosed_mass_at_zero (S G : ℝ) (_hG : 0 < G) :
    (fun x : ℝ => S * x / G) 0 = 0 := by
  simp

/-- **integrand_const (V5, the shell integrand).** The shell integrand of
the isothermal sphere is CONSTANT: 4 pi t^2 rho(t) = S/G for every t ≠ 0 —
this is why M(r) is exactly linear in r. -/
theorem integrand_const (S G t : ℝ) (hG : 0 < G) (ht : t ≠ 0) :
    4 * Real.pi * t ^ 2 * (S / (4 * Real.pi * G * t ^ 2)) = S / G := by
  field_simp [ht, Real.pi_ne_zero, hG.ne]

/-- **enclosed_mass_integral (V5, integral form).** M(r) = int_0^r 4 pi t^2
rho(t) dt = S r / G = 2 sigma^2 r/G — the isothermal sphere's linear mass
profile, from the constant shell integrand. -/
theorem enclosed_mass_integral (S G r : ℝ) (hG : 0 < G) (hr : 0 < r) :
    ∫ (t : ℝ) in (0)..r, 4 * Real.pi * t ^ 2 * (S / (4 * Real.pi * G * t ^ 2))
      = S * r / G := by
  have h0 : ∫ (t : ℝ) in (0)..r, 4 * Real.pi * t ^ 2 * (S / (4 * Real.pi * G * t ^ 2))
      = ∫ (t : ℝ) in (0)..r, (S / G) :=
    intervalIntegral.integral_congr_ae (μ := MeasureTheory.volume)
      (by rw [Set.uIoc_of_le hr.le]; filter_upwards with t ht;
          exact integrand_const S G t hG (ne_of_gt ht.1))
  rw [h0, intervalIntegral.integral_const, sub_zero, smul_eq_mul]
  field_simp [hG.ne]

/-- **btfr (V5, the flat curve).** v_c^2 = G M(r)/r = 2 sigma^2 = S =
sqrt(G Mb a0) — the baryonic Tully-Fisher law as the isothermal sphere's
equilibrium property (v^4 = G Mb a0). -/
theorem btfr (G r σsq S : ℝ) (hG : 0 < G) (hr : 0 < r) (hσ : σsq = S / 2) :
    G * (2 * σsq * r / G) / r = 2 * σsq ∧ 2 * σsq = S := by
  constructor
  · rw [hσ]
    field_simp [hG.ne, hr.ne]
  · rw [hσ]
    field_simp

/-! ## V6 — THE DEEP RAR -/

/-- **deep_rar (V6 — THE THEOREM).** With g_obs = S/r (the flat-curve
field) and g_N = G Mb/r^2 (the baryonic field):
g_obs^2 = a0 * g_N with coefficient EXACTLY 1. Sqrt-free: (S/r)^2 = S^2/r^2
and S^2 = G Mb a0, so g_obs^2 = G Mb a0/r^2 = a0*(G Mb/r^2) — pure field
algebra after the one application of Real.sq_sqrt. -/
theorem deep_rar (G Mb a0 r S : ℝ) (hG : 0 < G) (hMb : 0 < Mb) (ha0 : 0 < a0)
    (_hr : 0 < r) (hS : S = Real.sqrt (G * Mb * a0)) :
    (S / r) ^ 2 = a0 * (G * Mb / r ^ 2) := by
  have hS2 : S ^ 2 = G * Mb * a0 := by
    rw [hS]
    exact Real.sq_sqrt (by positivity)
  calc (S / r) ^ 2 = S ^ 2 / r ^ 2 := by ring
    _ = G * Mb * a0 / r ^ 2 := by rw [hS2]
    _ = a0 * (G * Mb / r ^ 2) := by ring

/-! ## G028 V1 — the cold window -/

/-- **w_window_cold (G028 V1).** Across the whole cold window
0 <= w <= 5.7e-7, the dust's density exponent -3(1+w) differs from -3 by
3|w| <= 1.71e-6 < 2e-6: the charge dust's density is indistinguishable
from a^-3 across the window. -/
theorem w_window_cold (w : ℝ) (hw : 0 ≤ w) (hwb : w ≤ 57 / 100000000) :
    abs ((-3:ℝ) * (1 + w) - (-3)) < 2 / 1000000 := by
  have hform : (-3:ℝ) * (1 + w) - (-3) = -(3 * w) := by ring
  rw [hform, abs_neg, abs_mul]
  have h3 : abs (3:ℝ) = 3 := abs_of_pos (by norm_num)
  have hw' : abs w = w := abs_of_nonneg hw
  rw [h3, hw']
  calc (3:ℝ) * w ≤ 3 * (57 / 100000000) := by
        exact mul_le_mul_of_nonneg_left hwb (by norm_num)
    _ < 2 / 1000000 := by norm_num

/-! ## THE SPINE — the capstone -/

/-- **the_spine.** The G031 hydrostatic chain as one machine-checked
implication chain: the Zimmerman temperature (V3) => the isothermal
identification (V4) => the mass profile M' = 4 pi r^2 rho (V5) => the flat
curve / BTFR (V5) => THE DEEP RAR g^2 = a0 g_N (V6). Every arrow exact;
zero free parameters. -/
theorem the_spine (G Mb a0 r : ℝ) (hG : 0 < G) (hMb : 0 < Mb) (ha0 : 0 < a0)
    (hr : 0 < r) :
    -- V3: the Zimmerman temperature
    G * Mb / (2 * Real.sqrt (G * Mb / a0)) = Real.sqrt (G * Mb * a0) / 2
    -- V4: the isothermal identification (the G003 phantom, coefficient 1)
    ∧ (G * Mb / (2 * Real.sqrt (G * Mb / a0))) / (2 * Real.pi * G * r ^ 2)
        = Real.sqrt (G * Mb * a0) / (4 * Real.pi * G * r ^ 2)
    -- V5: the mass profile M' = 4 pi r^2 rho
    ∧ HasDerivAt (fun x : ℝ => Real.sqrt (G * Mb * a0) * x / G)
        (4 * Real.pi * r ^ 2
          * (Real.sqrt (G * Mb * a0) / (4 * Real.pi * G * r ^ 2))) r
    -- V5: the flat curve / BTFR
    ∧ G * (Real.sqrt (G * Mb * a0) * r / G) / r = Real.sqrt (G * Mb * a0)
    -- V6: THE DEEP RAR
    ∧ (Real.sqrt (G * Mb * a0) / r) ^ 2 = a0 * (G * Mb / r ^ 2) := by
  refine ⟨zimmerman_temperature G Mb a0 hG hMb ha0, ?_, ?_, ?_, ?_⟩
  · exact phantom_is_isothermal (Real.sqrt (G * Mb * a0)) G r
      (G * Mb / (2 * Real.sqrt (G * Mb / a0))) hG hr
      (zimmerman_temperature G Mb a0 hG hMb ha0)
  · exact enclosed_mass_derivative (Real.sqrt (G * Mb * a0)) G r hG hr
  · field_simp [hG.ne, hr.ne]
  · exact deep_rar G Mb a0 r (Real.sqrt (G * Mb * a0)) hG hMb ha0 hr rfl

#print axioms key_sqrt_composition
#print axioms rho_L_from_a0
#print axioms lambda_geom_fixed
#print axioms zimmerman_temperature
#print axioms phantom_is_isothermal
#print axioms enclosed_mass_derivative
#print axioms enclosed_mass_at_zero
#print axioms integrand_const
#print axioms enclosed_mass_integral
#print axioms btfr
#print axioms deep_rar
#print axioms w_window_cold
#print axioms the_spine
