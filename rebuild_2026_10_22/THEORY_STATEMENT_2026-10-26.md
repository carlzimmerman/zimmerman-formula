# The theory as it stands (2026-10-26)

Original summary from committed lanes; the 2026-10-27 corrections link current workspace audit artifacts. κ = ½ FITTED. Footings canonical a₀ = 9.3603e-11 / alt 1.1312e-10 m s⁻², never pooled.
Not "theory closed". Nothing here says the data favour the framework. The adoption decision (route E, below) is the owner's.

**Audit correction, 2026-10-27.** The selector exclusions below apply to the
specified tested rules and halo prescriptions. They do not exhaust all possible
object-property or history-dependent mechanisms. X53 establishes a relative
lensing preference, not an absolute pass. The executed
[X57 R4b and X64 C6R corrections](../closure_program_2026_10_27/gate_fixes/README.md)
leave M6 **NOT DECIDABLE on both footings**. X64's primary labels still do not
separate among the eight tested keys, but its reported strict-need labels now
separate under corrected C6R; this profile-dependent split is not a mechanism.
P1D1 has returned **NOT DIAGNOSTIC**; it supplies no calibrated physical M6
population limit. The [population calculation](../closure_program_2026_10_27/population/RESULTS.md)
gives conditional capacities, not a measured required isolated fraction or a
physical forest limit. A later [M6-specific audit](../closure_program_2026_10_27/m6_decision/RESULTS.md)
finds a full-cold assignment in all 175 SPARC galaxies satisfying the
simultaneous numerical RMS and median mass-to-light constraints; the earlier
common-f cap depends on profiling U before applying the median cut. New
individual candidates and survey environment masks do not yet measure a
cosmic population requiring M6. The current closure record is
[`closure_program_2026_10_27/RESULTS.md`](../closure_program_2026_10_27/RESULTS.md).

## 0. UPDATE 2026-10-27: route E as stated below no longer passes; read this first

| lane | result |
|---|---|
| X53 outer lensing (KiDS isolated lenses) | **the law beats route-E halos**: Δχ² +430 / +456. Halos are too light by 0.35–0.5 dex and end at R200. |
| X55 one halo mass for SPARC + lensing | **Specified relation fails**: SPARC and lensing prefer different masses under its fixed profiles and deterministic no-scatter relation. The contour-contact score is 4.55 / 4.26; it is not a universal halo-exclusion significance. |
| X48 A2, nine seeds at ng 48 | c_f = 11.6 / 8.2 / 7.3, **ABOVE WINDOW**. The X43 rule with it **fails the SPARC line** (Υ 0.31). Caveat: r₋₂ is resolution-limited in 8/27 runs. |
| X48 A3, ng 64 at 10¹² (10-29) | c_f 11.6 → **7.7** (−33 %, **RESOLUTION-DEPENDENT**), still above the window. The pinned ng 48 seeds were inflated. With it, SPARC passes again (Υ 0.59 / 0.51); clusters (still at ng 48) fail 3 keys. |
| X54 cold DE ↔ DE exchange | **excluded** beyond ξ ∈ [−0.0035, +0.0011]: no conversion. |
| X56 g = max(law, route E) | **FAILS**: the law's tail over-predicts cluster outskirts. |
| X58 one-crossover mass switch (law below the crossover, halos above) | **FAILS** for the adopted class requirements: retain/exclude/retain is non-monotone in mass. More general mass-dependent functions are not covered. |
| X52 dwarf tides at current distance | no effect |

**Where this leaves the theory.**
- **The law** (a₀ = c²√(Λ/32π), κ = ½ fitted) has SPARC rms 0.054 and is preferred over the tested route-E halos in galaxy
  lensing to about 3 Mpc. X53 reports that no tested lensing model fits well in absolute terms. It fails clusters, which need extra mass, and the ultra-faint dwarfs, which are under-predicted by
  about 0.6 dex.
- **The tested cold dark energy halo prescriptions** fit some cluster and dwarf tests but fail others. X55 finds a
  dynamics/lensing mass-relation tension conditional on its profile, scatter and selection assumptions.
- **No combination tried so far** (max, mass switch) fits everything.
- **The open problems:** establish a common admissible mass profile and population relation, determine which systems
  require exclusion, and derive the dynamics that supplies those properties. X57 is complete; its M6 population
  requirement and forest-response mapping remain open. A selector alone cannot repair an inconsistent halo prescription.

The text below is the 10-26 statement, kept for the record.

## 1. Statement

1. **Λ sets the acceleration scale.** a₀ = κ c √(G ρ_Λ) = c² √(Λ/32π) (κ = ½, fitted).
2. **Two dark components.**
   - Dark energy (w = −1).
   - **Cold dark energy** (w ≈ 0). It is a collisionless, gravitating field component, not matter and not a particle, and
     it clumps.
3. **Gravity is ordinary** on baryons + cold dark energy (route E). The galaxy law is not a separate force; it is what the
   halos below look like.
4. **Cold dark energy halo cores** (Burkert form):

       Σ_core(M) = max( a₀ / (2πG),  η(c_f) · Σ_coll(M) ),   η = (4 / (3 B(1))) c_f^{5/4},  B(1) = 3 ln 2 − π/2

   - **The floor, a₀/(2πG):** cold dark energy is never cored more thinly than the Λ-set surface density (107 / 129
     M☉ pc⁻²). Halos below about 10¹² M☉ sit on it, so the RAR and the a₀ line emerge.
   - **Σ_coll(M):** the collapse surface density of the half-mass object at its Lacey–Cole formation epoch, on the record's
     own P(k) (X41). It scales as M^0.23.
   - **c_f:** the formation concentration, measured natively in collisionless zooms on the record's own background (X48).
     It is not taken from simulations.

## 2. Scorecard (both footings; frozen lanes)

| test | result | lane |
|---|---|---|
| SPARC (rms, median Υ) | PASS, 0.065 / 0.66 (native c_f) | X38, X43, X48 |
| galaxy groups (63) | PASS, Z +1.53 | X48 regrade |
| cluster cores, 0.3–1 Mpc (KT terciles + slope) | PASS | X48 regrade |
| cluster outskirts, 1.4–3 Mpc (KT and MGAS terciles) | PASS, incl. MGAS T3 (+1.80), which every earlier rule failed | X48 regrade |
| cluster inner band, all 326 | **FAIL**, 4.8 vs 2.3 ± 1.05, Z −2.4 / −2.1 | X48 regrade |
| CMB, growth, Lyman-α forest | pass by construction (dust-like cold dark energy) | route E, EM1 |
| Bullet Cluster | a collisionless dust-like tracer survives | X32 |
| tidal dwarfs, DF2/DF4 (below the law) | consistent (no halo) | route E |
| Solar System, GWs, binary pulsars | Newtonian/GR | route E |
| low-z shear power | the late-heating cap no longer applies (no heating in this model) | X29 |
| LG dwarfs, 5 classes (a₀-floor halos, no new constant) | **4 of 5 PASS** (LG field, MW classical, bright M31, M31 others); **MW ultra-faints FAIL** (Z +3.8 / +3.7, under) | X49 |

## 3. Constants

- **κ = ½:** fitted (sets a₀ from Λ).
- **c_f:** native, from the record's own collisionless dynamics. At ng 48 it is 7.2 / 7.0 / 5.6 at 10¹² / 10¹³ / 10¹⁴ M☉,
  not converged (×2). 18 more seeds are running (X48 A2).
- **Ω_c / Ω_b = 5.364:** the cold-dark-energy abundance, an initial condition.
- **Nothing else is tuned.** δ_c, Δ = 18π² and ω̃ = 0.974 are collapse statistics; the 9/4 infall slope is first principles.

## 4. What is open, in order

1. **The floor's mechanism.** Nothing in an action produces "never thinner than a₀/(2πG)". X47 found that a local
   threshold fails on growth and the data. An object-keyed threshold is consistent but nonlocal, and no action is written.
   This is the theory's one missing piece of physics.
2. **c_f convergence:** X48 A2 is running, about 14 h wall time.
3. **The cluster inner band** (Z −2.4) is the one remaining data miss. It is likely tied to c_f's inner value.
4. **The MW ultra-faints** (X49) were under-predicted by +0.48 dex; **X51**: a first-principles cooling-threshold halo mass (atomic, 1.1e8 Msun) brings them to −0.22 (canonical, all five dwarf classes PASS) / −0.32 (alt, UFD overshoot) and removes the dwarf mass trend; the truth lies between the H2 and atomic limits. (Original X49 note:) Their halo masses come from extrapolating EM1's SPARC
   relation far below its range (M200 ≈ 5×10⁵ M☉). The data want more massive halos there. The other four dwarf classes
   fit with no new constant, which retires v3s's separate ~4 km/s floor.

## 5. Sharp tests

- **Σ_floor(z) ∝ a₀(z):** the floor tracks dark energy (X47's prediction), testable with core surface densities at high z.
- **The crossover near 10¹² M☉:** halos above it are collapse-cored and below it a₀-cored. A break in the halo
  surface-density relation should appear there.
- **Gaia DR4 (12-02):** the route-E Milky Way numbers are committed (GD1, wide binaries Newtonian).
- **ALMA (11-06, 11-28):** sealed predictions from the earlier record. Their reading under route E needs a note.

## 6. The decision this asks of the owner

**Adopting route E** keeps a₀ = c²√(Λ/32π) as cold dark energy's defining density and closes the cold sector on the
theory's own numbers. The price: the galaxy law becomes emergent, not fundamental, and v3s's modified-gravity field is no
longer needed for galaxies.

Sources: COLD_SECTOR_SPEC_2026-10-24.md (§6–8), X38, X41, X43, X47, X48 (A1, A2), and verdict §8 in
covariant_push_2026_10_22/V3S_FINAL_VERDICT_2026-10-24.md.
