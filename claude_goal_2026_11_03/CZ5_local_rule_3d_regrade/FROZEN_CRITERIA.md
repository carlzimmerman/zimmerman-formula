# CZ5_local_rule_3d_regrade: FROZEN CRITERIA

Written 2026-11-04, committed alone before any CZ5 script or number. κ = ½ FITTED, held fixed. Footings never pooled. No cold component, no particle. Not theory closed. Nothing here says the data favour the framework.

## Why
- CZ2–CZ4 found the local rule LOC surviving on alt: Milky Way, Cassini, 24 dwarfs, SPARC and the planets.
- Those grades took |g| from the spherical quadrature √(g_int² + g_e²).
- CW1 (e7672a30e1) evaluated the same rule on the real 3D field. There, the zero of |g| at the Sun–Galaxy saddle sends ξ_loc → 0. Cassini reads 13.3× the ceiling on canonical and 18.1× on alt.
- CW1 reported this as a reading. **CZ5 is the frozen re-grade of LOC on every gate, on the 3D field.**

**Not blind:** CW1's Cassini numbers are known, so the T1 row is expected to FAIL on both footings. The open grade is the dwarfs in 3D.

## Rule (frozen)
- ξ_loc = |g|² / (|∇|g|| g*), with g* = a0/κ = 2 a0.
- |g| = ν(|g_N|/a0) |g_N|. g_N is the **vector** Newtonian field: the system's own field plus the host's uniform Newtonian field.
- |∇|g|| is the full 3D gradient magnitude, taken analytically.
- **Smoothing is field-gather.** The filtered field at x is the system's mass Gaussian-smoothed with width ξ(x), evaluated at x. For a spherical source this is G M_s(< r; ξ(x)) / r². It is CZ2's and CW1's Cassini construction.
- ξ is clipped as in CZ2: 1e4 r_M for the Sun, 200 kpc for dwarfs.
- ν(y) = ½ + √(¼ + 1/y). a0: canonical 9.3603e-11, alt 1.1312e-10.

## Gates (frozen; CZ2's T0–T3 plus CZ3's planets)
- **T0, Milky Way: carried from KT26** (canonical 0 cells, alt 30). In the midplane, symmetry gives g_z = 0 and ∂g_R/∂z = 0, so the 3D |∇|g|| equals KT26's radial form exactly at R0. Two things are inherited as approximations and stated as limits: KT26's single smoothing width, and the (R, z) variation of ξ, which isn't graded here. KT31–KT32 graded that variation for the tidal rule.
- **T1, Cassini, 3D.** CW1's multipole solver with the Sun as a point mass and η from inverting 2.32e-10 (CZ2's field). Q2 ≤ KT16's ceiling, 5.2e-27 s⁻².
- **T2, dwarfs, 3D.**
  - CZ2's sample: 24 McConnachie dwarfs, Plummer profiles, M = Υ L + 1.33 M_HI, Υ on a 1–3 grid of 41 values.
  - A dwarf passes if some Υ gives |σ − σ_obs| ≤ 2 e. **Line: ≥ 15/24.**
  - The graded field is E1, the MW Newtonian field G M_MW,b / D² for MW satellites (M_MW,b 7e10) and 0 for the others. E2 (the MW + M31 vector sum, CZ1) is printed beside.
  - σ² = (1/3M) ∫ ρ r g_r 4π r² dr, with g_r the internal Newtonian field plus the l = 0 phantom field, a_0 = ½ ∫ F_r dμ. Here F = (ν(|g_f|/a0) − 1) g_f − (ν_e − 1) g_Ne, with g_f the filtered internal field plus g_Ne. For a spherical tracer the virial integral needs only l = 0, so no Poisson solve is needed.
  - The gather table is the enclosed-mass fraction of a Gaussian-smoothed Plummer sphere, T(r/a, ξ/a). It is computed once, with kernel quadrature where ξ > 0.05 r and the second-order expansion M + (ξ²/2) 4π r² ρ′ below that.
  - **STRICT:** at least the count of plain QUMOND in 3D under the same field, printed beside.
- **T3, SPARC: carried from KT27** (canonical d rms +0.0129, fail; alt +0.0031, pass). KT27's ξ uses the midplane rotation-curve field, which equals 3D at z = 0. SPARC carries no external field on record.
- **T4, planets, 3D.** CZ3's exact secular rate and AZ12's bounds, using the l = 0 phantom field from the 3D solver. Every one of the six planets must have Z ≤ 2.

## Rows beside the graded one (dwarfs)
- **R0:** CZ2's `sig_los` verbatim (1D quadrature, density-row smoothing), for the K1 check.
- **R1:** 1D quadrature with field-gather. This isolates the construction change.
- **R3:** 3D ν argument with R1's 1D ξ. This isolates the ν argument.
- **R2:** the graded 3D row.

## Checks (frozen; a failed check is reported and left failed)
- **K1.** R0 reproduces CZ2's E1 counts (LOC 17, plain 18, HALF 18 on both footings) and Fornax LOC 11.94 / 12.52.
- **K2.** The table T reproduces the Plummer M(< r) to 1e-6 as ξ → 0, tends to 1 at large r, and gives the point-mass fraction erf − Gaussian for ξ ≫ a, within 1e-4.
- **K3.** T1 in 3D reproduces CW1's LOC3 Cassini, 13.3 / 18.1, within 1 %.
- **K4.** T4 in 3D reproduces CW1's worst planet Z at g* = 2 a0 within 1 %.
- **K5.** With a constant width, field-gather equals density-gather. So R1 at ξ = 0.5 r_M reproduces CZ2's HALF E1 dwarf count (18 / 18).
- **MUTATE twin (ν ≡ 1, separate outputs).** Every σ is Newtonian, Q2 = 0 and the planet rates are 0. Exit 1 by design.

## Labels (per footing, CZ2's form)
- **LOC SURVIVES** if T0–T4 all pass.
- Otherwise **LOC FAILS:** followed by the failing gates.
- STRICT is printed beside.
- If K1–K5 fail in a way that touches a graded number, the label is **NOT EVALUABLE**.

## Outputs
`cz5.py`, `cz5.out` / `cz5.json`, `cz5.time`, `cz5_MUTATE.*`, `README.md`. No download. No file outside this folder is edited.
