import Mathlib

/-!
# AS001 — Mass-density versus energy-density normalization (certificate)

Framework base (adopted inputs, NOT derived here):
    a0(mass)   := kappa * c * sqrt(G * rho)        (rho : mass density, kg/m^3)
    a0(energy) := kappa * sqrt(G * (rho * c^2))    (eps = rho * c^2 : energy density)
    kappa = 1/2 adopted;  G, c measured/fixed inputs.

What is certified (real arithmetic identities, nonnegativity domain):

1. `a0_energy_density_form` — the mass-density and energy-density
   normalizations are the SAME function of rho:
       kappa * c * sqrt(G * rho) = kappa * sqrt(G * (rho * c^2))
   for kappa >= 0, c >= 0, G >= 0, rho >= 0 (in particular for all rho > 0).
   Consequence: switching variable representation (rho |-> eps = rho c^2)
   introduces NO new coefficient and changes NO prediction. The factor c
   disappears from the explicit prefactor exactly because it is absorbed by
   the density's change of units.

2. `a0_footing_ratio_is_sqrt_density_ratio` — for two footings sharing
   (kappa, c, G):
       a0(rho2) / a0(rho1) = sqrt(rho2 / rho1)
   a purely dimensionless footing statement: at fixed kappa the acceleration
   scale ratio is the square root of the density ratio, and a single fixed
   (kappa, rho) pair cannot produce two distinct a0 values.

3. `r_M_representation_invariant` and `vflat4_representation_invariant` —
   the derived MOND radius r_M = sqrt(G*M/a0) and the deep flat-speed relation
   v_flat^4 = G*M*a0 give identical values through either representation of a0.

These certify the algebra of the normalization equivalence only. They do not
derive kappa = 1/2, do not fix the physical value of rho_Lambda, and do not
establish that the galactic scale is set by the actual cosmic vacuum density
(that identification remains an input/postulate of the framework).
-/

open Real

noncomputable def a0 (kappa c G rho : ℝ) : ℝ :=
  kappa * c * Real.sqrt (G * rho)

/-- Mass-density and energy-density normalizations coincide:
    kappa*c*sqrt(G*rho) = kappa*sqrt(G*(rho*c^2)) on the nonnegativity domain. -/
theorem a0_energy_density_form {kappa c G rho : ℝ}
    (_hk : 0 ≤ kappa) (hc : 0 ≤ c) (hG : 0 ≤ G) (hrho : 0 ≤ rho) :
    a0 kappa c G rho = kappa * Real.sqrt (G * (rho * c ^ 2)) := by
  unfold a0
  have hGrho : 0 ≤ G * rho := mul_nonneg hG hrho
  have hsq : (c * Real.sqrt (G * rho)) ^ 2 = G * (rho * c ^ 2) := by
    rw [mul_pow, Real.sq_sqrt hGrho]
    ring
  have hnonneg : 0 ≤ c * Real.sqrt (G * rho) := by
    exact mul_nonneg hc (Real.sqrt_nonneg (G * rho))
  have hsqrt : Real.sqrt (G * (rho * c ^ 2)) = c * Real.sqrt (G * rho) := by
    rw [← hsq, Real.sqrt_sq_eq_abs]
    exact abs_of_nonneg hnonneg
  rw [hsqrt]
  ring

/-- At fixed (kappa, c, G) with positive densities the a0 footing ratio is the
    square root of the density ratio. -/
theorem a0_footing_ratio_is_sqrt_density_ratio {kappa c G rho1 rho2 : ℝ}
    (hk : 0 < kappa) (hc : 0 < c) (hG : 0 < G) (hr1 : 0 < rho1) (hr2 : 0 < rho2) :
    a0 kappa c G rho2 / a0 kappa c G rho1 = Real.sqrt (rho2 / rho1) := by
  unfold a0
  have hkc : kappa * c ≠ 0 := ne_of_gt (mul_pos hk hc)
  have hG1p : 0 < G * rho1 := mul_pos hG hr1
  have hG2 : 0 ≤ G * rho2 := le_of_lt (mul_pos hG hr2)
  have hs1 : Real.sqrt (G * rho1) ≠ 0 := by
    exact ne_of_gt (Real.sqrt_pos.2 hG1p)
  have hratio : (G * rho2) / (G * rho1) = rho2 / rho1 := by
    field_simp [ne_of_gt hG, ne_of_gt hr1]
  have hmain : Real.sqrt (G * rho2) / Real.sqrt (G * rho1) = Real.sqrt (rho2 / rho1) := by
    rw [← Real.sqrt_div hG2 (G * rho1)]
    rw [hratio]
  calc
    kappa * c * Real.sqrt (G * rho2) / (kappa * c * Real.sqrt (G * rho1))
        = Real.sqrt (G * rho2) / Real.sqrt (G * rho1) := by
          field_simp [hkc, hs1]
    _ = Real.sqrt (rho2 / rho1) := hmain

/-- The MOND radius r_M = sqrt(G*M/a0) is representation-invariant. -/
theorem r_M_representation_invariant {kappa c G M rho : ℝ}
    (hk : 0 ≤ kappa) (hc : 0 ≤ c) (hG : 0 < G) (_hM : 0 ≤ M) (hrho : 0 ≤ rho) :
    Real.sqrt (G * M / a0 kappa c G rho) =
      Real.sqrt (G * M / (kappa * Real.sqrt (G * (rho * c ^ 2)))) := by
  rw [a0_energy_density_form hk hc (le_of_lt hG) hrho]

/-- The deep flat-speed relation v_flat^4 = G*M*a0 is representation-invariant
    (fourth root via two nested real square roots, nonneg domain). -/
theorem vflat4_representation_invariant {kappa c G M rho : ℝ}
    (hk : 0 ≤ kappa) (hc : 0 ≤ c) (hG : 0 < G) (_hM : 0 ≤ M) (hrho : 0 ≤ rho) :
    Real.sqrt (Real.sqrt (G * M * a0 kappa c G rho)) =
      Real.sqrt (Real.sqrt (G * M * (kappa * Real.sqrt (G * (rho * c ^ 2))))) := by
  rw [a0_energy_density_form hk hc (le_of_lt hG) hrho]

#print axioms a0_energy_density_form
#print axioms a0_footing_ratio_is_sqrt_density_ratio
#print axioms r_M_representation_invariant
#print axioms vflat4_representation_invariant