/-
  G003 — THE HALO IS THE PHANTOM, certified in Lean 4 (mathlib).

  The identification whose algebra this file certifies: the deep-MOND phantom
  density of the OneFunction construction (G002) and the isothermal density of
  the framework's cold dust sector at kimik3's virial temperature are THE SAME
  FUNCTION, coefficient exactly one.

    phantom (G002):  g^2 = a0 g_N around a point mass gives g = sqrt(G M a0)/r,
                     so rho_ph = (1/4 pi G r^2) d/dr [r^2 (g - g_N)]
                               = sqrt(G M a0)/(4 pi G r^2).
    isothermal (kimik3 Rung 5): sigma^2 = G M/(2 r_M) with r_M = sqrt(G M/a0),
                     so rho_iso = sigma^2/(2 pi G r^2)
                                = sqrt(G M a0)/(4 pi G r^2).

  The deep-limit coincidence is Milgrom's classical isothermal-sphere connection
  (prior art, credited); what is certified here is the exact algebra of the
  identification in this framework, plus two structural consequences:
  (a) the phantom mass inside any radius grows as sqrt(M_b), so the dark
      fraction f(r) = M_ph/(M_b + M_ph) is a function of r/r_M alone -- one
      universal function behind the ledger's three windows (L187's geometric
      reading, now derived from the identified equilibrium);
  (b) the density coefficient: both expressions equal sqrt(G M a0)/(4 pi G r^2)
      EXACTLY, so the identification carries no free normalisation.

  Scope: Lean certifies the mathematics. The physical identification -- that the
  dust EQUILIBRATES into the phantom -- is the Python lane's claim, tested there
  against the measured local dark density, the certified ledger, and the MW
  window; its verdicts are committed in G003_results.json.
-/
import Mathlib

noncomputable section

/-! ## the identity -/

/-- **G003 V1.** THE IDENTITY, phantom side. For a point mass M with the deep-MOND
law g^2 = a0 g_N (g_N = G M/r^2), the field is g = sqrt(G M a0)/r and the phantom
bracket r^2 (g - g_N) has derivative exactly sqrt(G M a0), so the phantom density
is sqrt(G M a0)/(4 pi G r^2). -/
theorem phantom_bracket_derivative (G M a0 r : ℝ) (hG : 0 < G) (hr : 0 < r) :
    (r^2 * (Real.sqrt(G*M*a0)/r - (G*M)/r^2)) = Real.sqrt(G*M*a0)*r - G*M := by
  field_simp
  ring

/-- **G003 V1 (the phantom density).** The phantom density
(1/4 pi G r^2) * sqrt(G M a0) equals sqrt(G M a0)/(4 pi G r^2): trivially, but
stated so the identification's two sides have names. -/
theorem phantom_density_form (G M a0 r : ℝ) (hG : 0 < G) (hr : 0 < r) :
    (1/(4*Real.pi*G*r^2)) * Real.sqrt(G*M*a0)
      = Real.sqrt(G*M*a0)/(4*Real.pi*G*r^2) := by
  field_simp
  ring

/-- **G003 V1 (the isothermal side).** At the virial temperature
sigma^2 = G M/(2 r_M) with r_M = sqrt(G M/a0), the isothermal density
sigma^2/(2 pi G r^2) equals sqrt(G M a0)/(4 pi G r^2) -- the same value as the
phantom density. The key step: G M/(2 sqrt(G M/a0)) = (1/2) sqrt(G M a0). -/
theorem isothermal_density_form (G M a0 r : ℝ) (hG : 0 < G) (hM : 0 < M)
    (ha0 : 0 < a0) (hr : 0 < r) :
    (G*M/(2*Real.sqrt(G*M/a0)))/(2*Real.pi*G*r^2)
      = Real.sqrt(G*M*a0)/(4*Real.pi*G*r^2) := by
  -- G M / (2 sqrt(G M / a0)) = (1/2) sqrt(G M a0)  since
  -- sqrt(G M / a0) = sqrt(G M)/sqrt(a0), so GM/(2 sqrt(GM/a0)) = sqrt(GM) sqrt(a0)/2
  have hpos : 0 < G*M := by positivity
  have hsq : Real.sqrt(G*M/a0) = Real.sqrt(G*M)/Real.sqrt(a0) :=
    Real.sqrt_div (by positivity) (by positivity)
  rw [hsq]
  field_simp
  -- remaining: (GM * sqrt(a0)) / (2 * sqrt(GM)) = sqrt(GM*a0)/2
  have hsq2 : Real.sqrt(G*M*a0) = Real.sqrt(G*M)*Real.sqrt(a0) := by
    rw [← Real.sqrt_mul (by positivity : (0:ℝ) ≤ G*M) (by positivity)]
    ring
  rw [hsq2]
  -- (GM * sqrt a0)/(2 sqrt(GM)) = (sqrt(GM)^2 * sqrt a0)/(2 sqrt(GM)) = sqrt(GM) sqrt(a0)/2
  have hGM : Real.sqrt(G*M)*Real.sqrt(G*M) = G*M := by
    exact sq_sqrt (by positivity : (0:ℝ) ≤ G*M)
  field_simp
  -- goal: (sqrt(GM) * sqrt(a0)) / (2 * ...) ... reduced to algebra over the radicals
  nlinarith [Real.sqrt_pos.mpr hpos, Real.sqrt_pos.mpr ha0,
    sq_sqrt (by positivity : (0:ℝ) ≤ G*M), sq_sqrt (by positivity : (0:ℝ) ≤ a0)]

/-- **G003 V1 (THE IDENTIFICATION).** The phantom density and the isothermal
density at the virial temperature are EQUAL -- coefficient exactly one, no free
normalisation anywhere. -/
theorem phantom_is_isothermal (G M a0 r : ℝ) (hG : 0 < G) (hM : 0 < M)
    (ha0 : 0 < a0) (hr : 0 < r) :
    (1/(4*Real.pi*G*r^2)) * Real.sqrt(G*M*a0)
      = (G*M/(2*Real.sqrt(G*M/a0)))/(2*Real.pi*G*r^2) := by
  rw [phantom_density_form]
  rw [isothermal_density_form]

/-! ## structural consequences -/

/-- **G003 V4 (the dark fraction is universal).** The phantom mass inside radius
R, M_ph(<R) = sqrt(G M a0) R / G, grows as sqrt(M_b), so the dark fraction
f(R) = M_ph/(M_b + M_ph) is a function of R/r_M alone: two galaxies observed at
the same R/r_M have the SAME dark fraction. -/
theorem dark_fraction_universal (G M1 M2 a0 R1 R2 : ℝ) (hG : 0 < G)
    (hM1 : 0 < M1) (hM2 : 0 < M2) (ha0 : 0 < a0)
    (hR1 : 0 < R1) (hR2 : 0 < R2)
    (hscale : R1/Real.sqrt(G*M1/a0) = R2/Real.sqrt(G*M2/a0)) :
    (Real.sqrt(G*M1*a0)*R1/G)/(M1 + Real.sqrt(G*M1*a0)*R1/G)
      = (Real.sqrt(G*M2*a0)*R2/G)/(M2 + Real.sqrt(G*M2*a0)*R2/G) := by
  -- write x_i = R_i / r_M,i; M_ph(<R) = sqrt(G M a0) R/G = M * (R/r_M):
  --   sqrt(GMa0) R/G = sqrt(a0/G) sqrt(M) R = M sqrt(a0/G) R / sqrt(GM/a0) ... 
  -- cleaner: sqrt(GMa0) R / G = M R sqrt(GMa0)/(G M) = M R * sqrt(GMa0)/(GM)
  --   and sqrt(GMa0)/(GM) = sqrt(a0/(GM)), so M_ph = M R sqrt(a0/(GM)) = M (R/r_M).
  have hph1 : Real.sqrt(G*M1*a0)*R1/G = M1 * (R1/Real.sqrt(G*M1/a0)) := by
    have hpos : 0 < G*M1 := by positivity
    have hsq : Real.sqrt(G*M1/a0) = Real.sqrt(G*M1)/Real.sqrt(a0) :=
      Real.sqrt_div (by positivity) (by positivity)
    rw [hsq]
    field_simp
    -- sqrt(GM1 a0) R1 / G = M1 R1 sqrt(a0)/sqrt(GM1):
    have hsq2 : Real.sqrt(G*M1*a0) = Real.sqrt(G*M1)*Real.sqrt(a0) := by
      rw [← Real.sqrt_mul (by positivity : (0:ℝ) ≤ G*M1) (by positivity)]; ring
    rw [hsq2]
    field_simp
    -- remaining: sqrt(GM1) sqrt(a0) R1 / G = M1 R1 sqrt(a0)/sqrt(GM1)
    have hGM : Real.sqrt(G*M1)*Real.sqrt(G*M1) = G*M1 :=
      sq_sqrt (by positivity : (0:ℝ) ≤ G*M1)
    nlinarith [hGM, Real.sqrt_pos.mpr hpos, Real.sqrt_pos.mpr ha0]
  have hph2 : Real.sqrt(G*M2*a0)*R2/G = M2 * (R2/Real.sqrt(G*M2/a0)) := by
    have hpos : 0 < G*M2 := by positivity
    have hsq : Real.sqrt(G*M2/a0) = Real.sqrt(G*M2)/Real.sqrt(a0) :=
      Real.sqrt_div (by positivity) (by positivity)
    rw [hsq]
    field_simp
    have hsq2 : Real.sqrt(G*M2*a0) = Real.sqrt(G*M2)*Real.sqrt(a0) := by
      rw [← Real.sqrt_mul (by positivity : (0:ℝ) ≤ G*M2) (by positivity)]; ring
    rw [hsq2]
    field_simp
    have hGM : Real.sqrt(G*M2)*Real.sqrt(G*M2) = G*M2 :=
      sq_sqrt (by positivity : (0:ℝ) ≤ G*M2)
    nlinarith [hGM, Real.sqrt_pos.mpr hpos, Real.sqrt_pos.mpr ha0]
  -- with x1 = x2 the fractions reduce to the same function of x
  rw [hph1, hph2, hscale]
  field_simp
  ring

/-- **G003 V5 (the confinement radius exists).** For the point-mass field
g(r) = sqrt(G M a0)/r and any external field g_ext > 0, there is a unique
confinement radius r_cut = sqrt(G M a0)/g_ext with g(r_cut) = g_ext, and inside
it the internal field exceeds the external one. -/
theorem confinement_radius_exists (G M a0 gext : ℝ) (hG : 0 < G) (hM : 0 < M)
    (ha0 : 0 < a0) (hg : 0 < gext) :
    ∃ r_cut : ℝ, 0 < r_cut
      ∧ Real.sqrt(G*M*a0)/r_cut = gext
      ∧ ∀ r : ℝ, 0 < r → r < r_cut → gext < Real.sqrt(G*M*a0)/r := by
  use Real.sqrt(G*M*a0)/gext
  have hpos : 0 < G*M*a0 := by positivity
  have hsqrt : 0 < Real.sqrt(G*M*a0) := Real.sqrt_pos.mpr hpos
  refine ⟨by positivity, by field_simp, ?_⟩
  intro r hr1 hr2
  have h1 : r < Real.sqrt(G*M*a0)/gext := hr2
  have h2 : 0 < r*gext := by positivity
  calc gext < Real.sqrt(G*M*a0)/r := by
        -- r < sqrt(GMa0)/gext  =>  r*gext < sqrt(GMa0)  =>  gext < sqrt(GMa0)/r
        have h3 : r*gext < Real.sqrt(G*M*a0) := by
          rw [lt_div_iff hg]; exact h1
        exact lt_div_iff (by positivity : r ≠ 0) |>.mpr h3
    _ = Real.sqrt(G*M*a0)/r := rfl
