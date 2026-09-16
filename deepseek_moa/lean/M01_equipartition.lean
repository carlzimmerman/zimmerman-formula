/-
  M01 -- THE EQUIPARTITION + GAUSS FLUX (fork lane M01, Lean-first).

  Physical statement (registered: G03G 2e-16, G090, G031):
    r_M      = sqrt(G M_b / a0)      the MOND radius (the one boundary)
    M_ph(<r) = sqrt(G M_b a0) * r/G  the Gauss-map phantom enclosed mass
    equipartition:  M_ph(<r_M) = M_b   (the dark sector carries exactly the
                                       baryon mass inside r_M)
    gauss_flux:     r^2 * g / G = M_ph(<r) with g = sqrt(G M_b a0)/r
                    (the deep-limit field; the flux picture: dark mass is the
                     baryonic flux, Gauss-charge ontology -- COUNCIL #40/#2)
    surface_density: M_b/(pi r_M^2) = a0/(pi G)  (the universal 213.74
                    Msun/pc^2 -- G083/H037)

  Proof strategy: copy the G031 patterns ONLY (key_sqrt_composition,
  Real.sq_sqrt, field_simp, ring). No nested-sqrt nlinarith. Three-strike
  rule: a theorem not closed in 3 attempts is dropped with the blocker named.

  Axiom discipline: zero sorry; axioms subseteq {propext, Classical.choice,
  Quot.sound}.
-/
import Mathlib

noncomputable section

/-! ## The key sqrt composition (G031 pattern, verified in this Mathlib). -/

/-- **key_sqrt_composition.** For positive G, M, a0:
sqrt(GM/a0) * sqrt(GM a0) = GM. -/
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

/-! ## rM_sq -- the MOND radius is the geometric mean of GM_b and 1/a0. -/

/-- **rM_sq.** r_M^2 = G M_b / a0. -/
theorem rM_sq (G Mb a0 : ℝ) (hG : 0 < G) (hMb : 0 < Mb) (ha0 : 0 < a0) :
    Real.sqrt (G * Mb / a0) ^ 2 = G * Mb / a0 := by
  exact Real.sq_sqrt (by positivity : 0 ≤ G * Mb / a0)

/-! ## The enclosed phantom mass: M_ph(<r) = sqrt(GMb a0) * r / G. -/

/-- **phantom_mass_linear.** The Gauss-map phantom enclosed mass is exactly
linear in r with slope sqrt(G M_b a0)/G -- the isothermal sphere's linear
mass profile M(r) = 2 sigma^2 r / G (G031 V5). -/
theorem phantom_mass_linear (G Mb a0 r : ℝ) :
    Real.sqrt (G * Mb * a0) * r / G = (Real.sqrt (G * Mb * a0) / G) * r := by
  ring

/-! ## equipartition -- THE identity: M_ph(<r_M) = M_b. -/

/-- **equipartition.** The phantom's enclosed mass at the MOND radius equals
the baryon mass EXACTLY: sqrt(G M_b a0) * r_M / G = M_b with
r_M = sqrt(G M_b / a0). No free parameter. (Registered: G03G, 2e-16.) -/
theorem equipartition (G Mb a0 : ℝ) (hG : 0 < G) (hMb : 0 < Mb) (ha0 : 0 < a0) :
    Real.sqrt (G * Mb * a0) * Real.sqrt (G * Mb / a0) / G = Mb := by
  have hk := key_sqrt_composition G Mb a0 hG hMb ha0
  -- key_sqrt_composition: sqrt(GMb/a0) * sqrt(GMb a0) = GMb; commute the product
  have hc : Real.sqrt (G * Mb * a0) * Real.sqrt (G * Mb / a0) = G * Mb := by
    calc Real.sqrt (G * Mb * a0) * Real.sqrt (G * Mb / a0)
        = Real.sqrt (G * Mb / a0) * Real.sqrt (G * Mb * a0) := by ring
      _ = G * Mb := hk
  calc Real.sqrt (G * Mb * a0) * Real.sqrt (G * Mb / a0) / G
      = (G * Mb) / G := by rw [hc]
    _ = Mb := by field_simp [hG.ne]

/-! ## gauss_flux -- the flux picture (COUNCIL #2/#40). -/

/-- **gauss_flux.** In the deep limit the phantom's field is
g(r) = sqrt(G M_b a0)/r; the Gauss-map mass from the flux 4 pi r^2 g is
r^2 g / G = M_ph(<r). Dark mass = baryonic flux. -/
theorem gauss_flux (G Mb a0 r : ℝ) (hG : 0 < G) (hMb : 0 < Mb)
    (ha0 : 0 < a0) (hr : r ≠ 0) :
    r ^ 2 * (Real.sqrt (G * Mb * a0) / r) / G
      = Real.sqrt (G * Mb * a0) * r / G := by
  field_simp [hr]

/-! ## surface_density -- the universal Sigma = a0/(pi G). -/

/-- **surface_density.** The mean surface density inside r_M:
M_b / (pi r_M^2) = a0 / (pi G) -- the universal 213.74 Msun/pc^2
(G083/H037), from the definition of r_M alone. -/
theorem surface_density (G Mb a0 : ℝ) (hG : 0 < G) (hMb : 0 < Mb)
    (ha0 : 0 < a0) :
    Mb / (Real.pi * (G * Mb / a0)) = a0 / (Real.pi * G) := by
  field_simp [Real.pi_ne_zero, hG.ne, hMb.ne, ha0.ne]

/-! ## the_spine -- the fork M01 chain as one conjunction. -/

/-- **the_spine.** The M01 chain: r_M^2 = GMb/a0 and equipartition and the
flux identity and the surface density -- one statement of the Gauss-charge
ontology: at the one boundary, the phantom IS the baryons' flux. -/
theorem the_spine (G Mb a0 r : ℝ) (hG : 0 < G) (hMb : 0 < Mb)
    (ha0 : 0 < a0) (hr : r ≠ 0) :
    Real.sqrt (G * Mb / a0) ^ 2 = G * Mb / a0 ∧
    Real.sqrt (G * Mb * a0) * Real.sqrt (G * Mb / a0) / G = Mb ∧
    r ^ 2 * (Real.sqrt (G * Mb * a0) / r) / G
      = Real.sqrt (G * Mb * a0) * r / G ∧
    Mb / (Real.pi * (G * Mb / a0)) = a0 / (Real.pi * G) := by
  constructor
  · exact rM_sq G Mb a0 hG hMb ha0
  · constructor
    · exact equipartition G Mb a0 hG hMb ha0
    · constructor
      · exact gauss_flux G Mb a0 r hG hMb ha0 hr
      · exact surface_density G Mb a0 hG hMb ha0

end