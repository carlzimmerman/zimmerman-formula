/-
  C07 -- THE GAUSS-CHARGE EXPONENT CONSISTENCY -- the Lean certificate.

  The chain (each arrow an exponent bookkeeping, all links bidirectional at the
  level the house patterns allow):

      rho = A/r^2   <->   M_ph(<r) = 4 pi A r   <->   g = G M_ph/r^2 = 4 pi G A / r
      <->   the flux 4 pi g r^2 integrated over the sphere recovers the charge

  The exponents: the r^-2 in the phantom density EXACTLY cancels the r^2 shell
  measure of the volume element, leaving the CONSTANT shell flux density
  4 pi A (exponent 2 - 2 = 0); the constant integrates to the LINEAR enclosed
  mass 4 pi A r (exponent 1); Newton's shell statement g = G M_enc/r^2 turns
  the linear mass into the inverse-square acceleration 4 pi G A / r (exponent
  1 - 2 = -1); and the Gauss flux 4 pi r^2 g = 4 pi G * M_enc (exponent
  -1 + 2 = 1) recovers the charge EXACTLY (M01's gauss_flux, restated at the
  exponent-consistency level).  The literal constants of the chain are the
  shell flux density 4 pi A and the product g * r = 4 pi G A ("g ~ r^-1 <-> g r
  = const"); the flux itself is LINEAR in r because the enclosed mass is linear
  in r (a constant flux is the POINT-MASS statement flux = 4 pi G M with M
  constant -- NOT the phantom's, and the task formula "4 pi g r^2 = constant"
  is read in that exponent sense and stated exactly below: the per-unit-radius
  flux density is constant, the flux's exponent is zero after the r^2 shell
  measure is applied to rho, and the flux law is 4 pi r^2 g = 4 pi G M_enc).

  Closed on the registered numbers (G03E/G03G/G090/G154/G227):
      A  := sqrt(G M_b a0) / (4 pi G)     the phantom amplitude (coefficient 1)
      rM := sqrt(G M_b / a0)              the MOND radius (the one boundary)
      M_ph(<r_M) = 4 pi A rM = M_b        the equipartition, from the A/r^2 form
      the registered deep flux: g = S/r, S := sqrt(G M_b a0):
          4 pi r^2 g = 4 pi S r           (G227 isothermal_flux, re-derived)

  Techniques (house patterns ONLY): G031's intervalIntegral for the enclosed
  mass integral, G03G's sqrt_pair for the sqrt endpoint, field_simp/ring for
  everything else.  Zero sorry.  Axioms: {propext, Classical.choice,
  Quot.sound} only (each of the #print axioms blocks below).
-/
import Mathlib

noncomputable section

/-! ## 1. THE CONSTANT SHELL FLUX DENSITY: rho = A/r^2 instantly cancels the
        r^2 shell measure: 4 pi t^2 rho(t) = 4 pi A (exponent 2 - 2 = 0). -/

/-- **shell_flux_density_const.** The phantom shell integrand is the CONSTANT
4 pi A for every t != 0: the r^-2 exponent exactly cancels the r^2 shell
measure.  This one cancellation is the whole exponent consistency: it makes
the enclosed mass linear (theorem enclosed_mass_linear). -/
theorem shell_flux_density_const (A t : ℝ) (ht : t ≠ 0) :
    4 * Real.pi * t ^ 2 * (A / t ^ 2) = 4 * Real.pi * A := by
  field_simp [ht]

/-- **density_profile_iff_linear.** The bidirectional link at the integrand
level: the shell flux density is the constant 4 pi A IF AND ONLY IF the
density profile is A/t^2 -- "rho = A/r^2 <-> 4 pi g r^2 = constant (in the
per-unit-radius sense)" is an iff, not a one-way. -/
theorem density_profile_iff_linear (A rho t : ℝ) (ht : t ≠ 0) :
    (4 * Real.pi * t ^ 2 * rho = 4 * Real.pi * A ↔ rho = A / t ^ 2) := by
  field_simp [ht]

/-! ## 2. THE LINEAR-IN-r IDENTITY: M(<r) = 4 pi A r (integral form). -/

/-- **enclosed_mass_linear (THE core identity).** For the phantom density
rho(t) = A/t^2 the enclosed mass inside r is exactly 4 pi A r:

    M(<r) = int_0^r 4 pi t^2 (A/t^2) dt = 4 pi A r,

the linear-in-r identity of the task: rho = A/r^2  =>  M_ph(<r) ~ r.
(G031's intervalIntegral pattern; the constant shell integrand integrates to
the constant times r, no sign hypotheses needed.) -/
theorem enclosed_mass_linear (A r : ℝ) (hr : 0 < r) :
    ∫ (t : ℝ) in (0)..r, 4 * Real.pi * t ^ 2 * (A / t ^ 2)
      = 4 * Real.pi * A * r := by
  have h0 : ∫ (t : ℝ) in (0)..r, 4 * Real.pi * t ^ 2 * (A / t ^ 2)
      = ∫ (t : ℝ) in (0)..r, (4 * Real.pi * A) :=
    intervalIntegral.integral_congr_ae (μ := MeasureTheory.volume)
      (by rw [Set.uIoc_of_le hr.le]; filter_upwards with t ht;
          exact shell_flux_density_const A t (ne_of_gt ht.1))
  rw [h0, intervalIntegral.integral_const, sub_zero, smul_eq_mul]
  ring

/-! ## 3. FROM THE LINEAR MASS TO THE INVERSE-SQUARE ACCELERATION:
        g := G M_enc / r^2  =  4 pi G A / r   (exponent 1 - 2 = -1). -/

/-- **accel_inversesq.** With the enclosed mass M_enc = 4 pi A r and Newton's
shell statement g = G M_enc / r^2, the acceleration is EXACTLY 4 pi G A / r:
the linear enclosed mass forces the inverse-square (r^-1) acceleration. -/
theorem accel_inversesq (G A r : ℝ) (hr : r ≠ 0) :
    let Menc := 4 * Real.pi * A * r
    let g := G * Menc / r ^ 2
    g = 4 * Real.pi * G * A / r := by
  intro Menc g
  dsimp [g, Menc]
  field_simp [hr]

/-- **accel_times_r_const.** The literal constant of the inverse-square law:
g * r = 4 pi G A, independent of r -- "g ~ r^-1 <-> g r = const" exactly. -/
theorem accel_times_r_const (G A r : ℝ) (hr : r ≠ 0) :
    let Menc := 4 * Real.pi * A * r
    let g := G * Menc / r ^ 2
    g * r = 4 * Real.pi * G * A := by
  intro Menc g
  dsimp [g, Menc]
  field_simp [hr]

/-! ## 4. THE GAUSS STATEMENT CONNECTING THE FLUX TO THE ACCELERATION
        (M01's gauss_flux, restated at the exponent-consistency level). -/

/-- **charge_recovered_from_flux.** The Gauss-map charge: the flux through the
sphere (sphere area 4 pi r^2 times g, divided by 4 pi G) recovers the enclosed
mass EXACTLY: r^2 g / G = M(<r) = 4 pi A r, with g = 4 pi G A / r the
inverse-square acceleration of theorem accel_inversesq.  This is the minimal
Gauss statement: the flux of the field IS the charge, exponent-wise
(r^2 * r^-1 = r^1 = the mass's exponent). -/
theorem charge_recovered_from_flux (G A r : ℝ) (hG : 0 < G) (hr : r ≠ 0) :
    let g := 4 * Real.pi * G * A / r
    r ^ 2 * g / G = 4 * Real.pi * A * r := by
  intro g
  dsimp [g]
  field_simp [hG.ne, hr]

/-- **gauss_flux_law.** Gauss's law in the exact flux form: the surface
integral 4 pi r^2 g equals 4 pi G times the enclosed mass -- flux = 4 pi G *
M_enc with M_enc = 4 pi A r.  The flux is LINEAR in r (NOT constant): a
constant flux is the point-mass statement (M_enc constant); the phantom's
constant is the shell flux density 4 pi A and the product g r = 4 pi G A. -/
theorem gauss_flux_law (G A r : ℝ) (hr : r ≠ 0) :
    let g := 4 * Real.pi * G * A / r
    4 * Real.pi * r ^ 2 * g = 4 * Real.pi * G * (4 * Real.pi * A * r) := by
  intro g
  dsimp [g]
  field_simp [hr]

/-! ## 5. CLOSED ON THE REGISTERED NUMBERS: A := sqrt(G M_b a0)/(4 pi G),
        r_M := sqrt(G M_b/a0).  The chain endpoint: 4 pi A r_M = M_b. -/

/-- **sqrt_pair.** The product identity sqrt(G M_b a0) * sqrt(G M_b/a0) = G M_b
(G03G #0, re-derived in-file -- every certificate standalone). -/
theorem sqrt_pair (G Mb a0 : ℝ) (hG : 0 < G) (hMb : 0 < Mb) (ha0 : 0 < a0) :
    Real.sqrt (G * Mb * a0) * Real.sqrt (G * Mb / a0) = G * Mb := by
  have hG0 : G ≠ 0 := by positivity
  have hx : 0 ≤ G * Mb * a0 := by positivity
  have hy : 0 ≤ G * Mb / a0 := by positivity
  have hs : (Real.sqrt (G * Mb * a0) * Real.sqrt (G * Mb / a0)) ^ 2 = (G * Mb) ^ 2 := by
    rw [mul_pow]
    rw [Real.sq_sqrt hx]
    rw [Real.sq_sqrt hy]
    field_simp [hG0]
  have hnonneg : 0 ≤ Real.sqrt (G * Mb * a0) * Real.sqrt (G * Mb / a0) := by positivity
  have hGpos : 0 ≤ G * Mb := by positivity
  have hor : Real.sqrt (G * Mb * a0) * Real.sqrt (G * Mb / a0) = G * Mb
      ∨ Real.sqrt (G * Mb * a0) * Real.sqrt (G * Mb / a0) = -(G * Mb) :=
    eq_or_eq_neg_of_sq_eq_sq _ _ hs
  rcases hor with h | h
  · exact h
  · nlinarith

/-- **equipartition_from_amplitude.** The chain closed on the registered
constants: with A := sqrt(G M_b a0)/(4 pi G) (the phantom amplitude, G03G's
A) the linear-in-r identity at r = r_M := sqrt(G M_b/a0) gives
M_ph(<r_M) = 4 pi A r_M = M_b EXACTLY -- the equipartition (G03G/G090) as the
endpoint of the exponent chain. -/
theorem equipartition_from_amplitude (G Mb a0 : ℝ) (hG : 0 < G) (hMb : 0 < Mb)
    (ha0 : 0 < a0) :
    let rM := Real.sqrt (G * Mb / a0)
    let A := Real.sqrt (G * Mb * a0) / (4 * Real.pi * G)
    4 * Real.pi * A * rM = Mb := by
  intro rM A
  dsimp [A, rM]
  have hG0 : G ≠ 0 := by positivity
  have hMb0 : Mb ≠ 0 := by positivity
  field_simp [hG0, hMb0]
  nlinarith [sqrt_pair G Mb a0 hG hMb ha0]

/-- **registered_flux_linear.** The registered deep field g = S/r with
S := sqrt(G M_b a0) gives the flux 4 pi r^2 g = 4 pi S r -- G227's
isothermal_flux re-derived as the chain's endpoint: the flux is exactly linear
in r, consistent with the linear enclosed mass through Gauss's law. -/
theorem registered_flux_linear (G Mb a0 r : ℝ) (hG : 0 < G) (hMb : 0 < Mb)
    (ha0 : 0 < a0) (hr : r ≠ 0) :
    let S := Real.sqrt (G * Mb * a0)
    let g := S / r
    4 * Real.pi * r ^ 2 * g = 4 * Real.pi * Real.sqrt (G * Mb * a0) * r := by
  intro S g
  dsimp [g, S]
  field_simp [hr]

/-! ## 6. THE SPINE: the whole exponent chain as one conjunction. -/

/-- **the_spine.** The C07 chain as one statement: the constant shell flux
density (rho = A0/t^2 cancels the r^2 shell measure) AND the enclosed mass
identity M(<r) = 4 pi A0 r AND the inverse-square acceleration
g = 4 pi G A0 / r AND the charge recovery r^2 g / G = M(<r) AND Gauss's law
4 pi r^2 g = 4 pi G M_enc AND the equipartition 4 pi A0 r_M = M_b -- with the
registered amplitude A0 := sqrt(G M_b a0)/(4 pi G). -/
theorem the_spine (G Mb a0 r t : ℝ) (hG : 0 < G) (hMb : 0 < Mb)
    (ha0 : 0 < a0) (hr : 0 < r) (ht : t ≠ 0) :
    let A0 := Real.sqrt (G * Mb * a0) / (4 * Real.pi * G)
    -- 1. the constant shell flux density (exponent 2 - 2 = 0)
    4 * Real.pi * t ^ 2 * (A0 / t ^ 2) = 4 * Real.pi * A0
    -- 2. the linear-in-r identity M(<r) = 4 pi A0 r
    ∧ (∫ (s : ℝ) in (0)..r, 4 * Real.pi * s ^ 2 * (A0 / s ^ 2)
        = 4 * Real.pi * A0 * r)
    -- 3. the inverse-square acceleration (exponent 1 - 2 = -1)
    ∧ G * (4 * Real.pi * A0 * r) / r ^ 2 = 4 * Real.pi * G * A0 / r
    -- 4. the Gauss statement: the flux recovers the charge (r^2 * r^-1 = r)
    ∧ r ^ 2 * (4 * Real.pi * G * A0 / r) / G = 4 * Real.pi * A0 * r
    -- 5. Gauss's law: flux = 4 pi G * M_enc
    ∧ 4 * Real.pi * r ^ 2 * (4 * Real.pi * G * A0 / r)
        = 4 * Real.pi * G * (4 * Real.pi * A0 * r)
    -- 6. the equipartition endpoint: M_ph(<r_M) = M_b, r_M := sqrt(G M_b/a0)
    ∧ 4 * Real.pi * (Real.sqrt (G * Mb * a0) / (4 * Real.pi * G))
        * Real.sqrt (G * Mb / a0) = Mb := by
  intro A0
  dsimp [A0]
  constructor
  · exact shell_flux_density_const (Real.sqrt (G * Mb * a0) / (4 * Real.pi * G)) t ht
  · constructor
    · exact enclosed_mass_linear (Real.sqrt (G * Mb * a0) / (4 * Real.pi * G)) r hr
    · constructor
      · exact accel_inversesq G (Real.sqrt (G * Mb * a0) / (4 * Real.pi * G)) r
          (ne_of_gt hr)
      · constructor
        · exact charge_recovered_from_flux G
            (Real.sqrt (G * Mb * a0) / (4 * Real.pi * G)) r hG (ne_of_gt hr)
        · constructor
          · exact gauss_flux_law G
              (Real.sqrt (G * Mb * a0) / (4 * Real.pi * G)) r (ne_of_gt hr)
          · exact equipartition_from_amplitude G Mb a0 hG hMb ha0

#print axioms shell_flux_density_const
#print axioms density_profile_iff_linear
#print axioms enclosed_mass_linear
#print axioms accel_inversesq
#print axioms accel_times_r_const
#print axioms charge_recovered_from_flux
#print axioms gauss_flux_law
#print axioms sqrt_pair
#print axioms equipartition_from_amplitude
#print axioms registered_flux_linear
#print axioms the_spine