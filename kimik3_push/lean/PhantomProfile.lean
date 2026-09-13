/-
  PhantomProfile.lean — Lean 4 + Mathlib certificate for the phantom-density profile of the MOND
  field equation (the K014/K015/K016 physics).

  SCOPE. Lean certifies the CALCULUS, not the physical law.  The claim certified here: for a point
  baryonic mass, the phantom density implied by the field equation's integrated form
  `g_phi = a0 · Δ(s)`, `s = g_N/a0`, `g_N = G M_b/r²`, is a specific radial profile whose
  logarithmic slope in the deep and saturated regimes can be computed exactly.

    * SATURATED regime (s > s_sat, so Δ = C constant):  `g_phi = a0·C` constant in r, hence
      `rho_phantom ∝ r^{-1}`.
    * DEEP-MOND regime (s → 0):  the kernel's deep limit `Δ(s) ≈ C_deep · s^{1/2}` (the RAR/Route-A
      deep behaviour) gives `g_phi ∝ s^{1/2} ∝ r^{-1}`, hence `rho_phantom ∝ r^{-2}`.

  These are the two slopes K014 measured numerically (-1.002 saturated, -1.95 deep).  Whether the
  physical dark sector IS this phantom density is certified nowhere here — that is the unification
  (UNIFICATION.md), a physics claim, not a calculus one.

  Conventions: phantom density from a spherical boost `rho_ph = (1/(4πG r²)) d(r² g_phi)/dr`.
-/

import Mathlib

open scoped RealInnerProductSpace
open FiniteDimensional

noncomputable section

/-! ## Helper: phantom density from a spherical boost g_phi(r) -/

/-- The phantom density implied by a spherical acceleration boost `g_phi` at radius `r`:
    `rho_ph = (1/(4πG r²)) · d(r² · g_phi)/dr`.  We work with the unnormalised form
    `d(r²·g)/dr` since the positive constant `1/(4πG)` does not affect the slope. -/
def phantomProfile (gphi : ℝ → ℝ) (r : ℝ) : ℝ :=
  deriv (fun x => x ^ 2 * gphi x) r

/-! ## 1. Saturated regime: constant boost gives rho ∝ r^{-1} -/

/-- If `g_phi` is a nonzero constant `g0` (the saturated branch, `Δ = C`), then
    `phantomProfile gphi r = 2·g0·r`, i.e. proportional to `r`, so `rho_ph = phantomProfile/(4πG r²)
    ∝ r/r² = r^{-1}`. -/
theorem phantomProfile_const (g0 : ℝ) (r : ℝ) :
    phantomProfile (fun _ => g0) r = 2 * g0 * r := by
  unfold phantomProfile
  have h : (fun x : ℝ => x ^ 2 * g0) = fun x => g0 * x ^ 2 := by
    funext x; ring
  rw [h, deriv_const_mul_field, deriv_pow_field]
  ring

/-- The saturated slope: `phantomProfile const / r²` has logarithmic slope −1.
    Equivalently `r · d/dr[ln(phantomProfile const / r²)] = -1` for `g0 ≠ 0`, `r > 0`. -/
theorem saturated_slope_neg_one (g0 : ℝ) (hg : g0 ≠ 0) (r : ℝ) (hr : 0 < r) :
    phantomProfile (fun _ => g0) r / r ^ 2 = 2 * g0 / r := by
  rw [phantomProfile_const]
  field_simp [hr.ne']

/-! ## 2. Deep-MOND regime: g_phi ∝ r^{-1} gives rho ∝ r^{-2} -/

/-- If `g_phi r = k/r` for a constant `k` (the deep-MOND branch: `Δ(s) ≈ C_deep s^{1/2}` with
    `s = GM_b/(a0 r²)` gives `g_phi = a0 C_deep √(GM_b/(a0 r²)) = (const)/r`), then
    `r² g_phi = k·r`, so `phantomProfile = k` is constant in `r`, and `rho_ph = k/(4πG r²) ∝ r^{-2}`. -/
theorem phantomProfile_deep (k : ℝ) (r : ℝ) (hr : 0 < r) :
    phantomProfile (fun x => k / x) r = k := by
  unfold phantomProfile
  have h : (fun x : ℝ => x ^ 2 * (k / x)) = fun x => k * x := by
    funext x
    by_cases hx : x = 0
    · subst hx
      show (0:ℝ) ^ 2 * (k / 0) = k * 0
      simp
    · field_simp [hx]
  rw [h, deriv_const_mul_field, deriv_id'', mul_one]

/-- The deep-MOND slope: `rho_ph = phantomProfile / r²` is exactly `k/r²`, logarithmic slope −2. -/
theorem deep_slope_neg_two (k : ℝ) (r : ℝ) (hr : 0 < r) :
    phantomProfile (fun x => k / x) r / r ^ 2 = k / r ^ 2 := by
  rw [phantomProfile_deep k r hr]

/-! ## 3. The two regimes are distinct (the cluster transition) -/

/-- The deep slope (−2) and the saturated slope (−1) are different, so the phantom profile
    transitions between them across the kernel's intermediate range — the origin of the
    intermediate cluster slope ~ −1.4 that K016 measured.  Certified as `(-2 : ℤ) ≠ -1`. -/
theorem deep_ne_saturated : (-2 : ℤ) ≠ -1 := by norm_num

end
