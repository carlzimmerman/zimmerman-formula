# AG4h FROZEN CRITERIA (2026-10-20): can distance or inclination errors explain AG4g's 13 large pulls?

Committed alone, before any AG4h fit or number. Owner's go (2026-10-20, in chat, "ok do it right") on checking the pulled
galaxies against independent distances and inclinations. It runs as a small job under the owner's 10-20 rule.

## Pre-flight, disclosed: coverage counts only, no fits
- Cosmicflows-4 rotation-free distances (TRGB > Cepheid > SBF > SN Ia > SN II, 60″ match, as in p50) and LITTLE THINGS
  (Oh+2015) kinematic inclinations are on disk (owner-approved fetch, 2026-10-05).
- **Of the 13 pulled galaxies:**
  - 6 already have TRGB distances in SPARC: CamB, IC2574, NGC0024, NGC1705, UGC08286, UGC08837. CF4 has TRGB for 4 of them
    (all except IC2574 and NGC0024).
  - 6 are on Hubble-flow distances (NGC5985, UGC00128, UGC00731, UGC03580, UGC06787, UGC12506) and 1 on Ursa Major (NGC4217).
    None has a CF4 rotation-free distance.
  - None is in LITTLE THINGS, which overlaps SPARC in only DDO154, DDO168 and NGC2366.
- **So no pulled galaxy can be re-measured with an independent distance or inclination from on-disk data.** This lane therefore
  inverts the error budget, and checks the TRGB distances against CF4.

## Fits per galaxy (AG4g's data, law n=1, canonical a₀, prior and s₀; the coherent offset c in log g)
- **A_ML:** Υ and c both free, no priors → χ²_A (data part only).
- **B:** Υ fixed at the stellar-population value (Υ_disk 0.5, bulge 0.7), c free with no prior → c_req and χ²_B (data part).
- Δχ² = χ²_B − χ²_A (one fewer free parameter in B).
- K1: AG4g's MAP pull is reproduced for each of the 13 (same code path).

## Readings per galaxy
- **COHERENT-ABSORBABLE:** Δχ² ≤ 4. A pure coherent shift in log g, which is what a distance or inclination error produces,
  fits as well as the Υ change.
  - Distance needed: f = D_true/D_SPARC = 10^(−c_req), since g_obs ∝ 1/D and g_bar does not change with D.
    n_D = |c_req|/(eD/D/ln10), using SPARC's eD/D. For TRGB galaxies, CF4's TRGB distance is also reported.
  - Inclination needed: i_new from sin i_new = sin i·10^(c_req/2), since g_obs ∝ 1/sin²i. n_i = |i_new − i|/eInc.
    It is impossible if |sin i_new| > 1.
  - **DISTANCE-PLAUSIBLE** if n_D ≤ 2; **INCLINATION-PLAUSIBLE** if n_i ≤ 2; otherwise **NEEDS > 2σ ERRORS**.
- **SHAPE-DRIVEN:** Δχ² > 4. No coherent shift can replace the Υ change, so the pull comes from the rotation curve's shape:
  non-circular motions, the bulge/disc decomposition, or a real difference in the mass distribution.

## Summary readings (13 galaxies)
- Report the counts in each class.
- **DISTANCE/INCLINATION EXPLAIN THE EXCESS** if at least 10 of 13 are DISTANCE- or INCLINATION-PLAUSIBLE.
- **SHAPE DOMINATES** if at least 7 of 13 are SHAPE-DRIVEN.
- **MIXED** otherwise.
- **Reported, not graded:** the Q flag of each SHAPE-DRIVEN galaxy, and the sign of its pull. AG4g already showed a Q pattern,
  so this is not a new test.

## Independent cross-check (the only one on disk)
- **TD:** for the 4 pulled TRGB galaxies with a CF4 TRGB distance, D_CF4/D_SPARC must lie within 10% for each. If one does not,
  that galaxy's distance is flagged as disputed and its n_D is recomputed with the CF4 distance, reported only.

## Controls
- **K2 (bites):** a law-true mock of each of the 13 (Υ at the SPS value, no offset, per-point noise from its errors) with
  g_obs ÷ 1.3 (a 30% distance overestimate) must come out COHERENT-ABSORBABLE with f within 5% of 1.3, for at least 11 of 13.
- **MUTATE:** `AG4H_MUTATE=1` replaces each pulled galaxy's data by a law-true mock with Υ_disk × 3 in the inner half only
  (a shape change). At least 7 of 13 must come out SHAPE-DRIVEN; the script then exits 1 (the control bites).

## What would close it fully (not fetched here; needs the owner's OK)
- Rotation-free distances for the 6 Hubble-flow galaxies.
- Independent tilted-ring inclinations and non-circular-motion analyses (for example THINGS for IC2574) for the pulled galaxies.

## Settings
κ = ½ fitted; not theory closed. Outputs: `ag4h.py` → `ag4h.out`, `ag4h_results.json`; MUTATE → `_MUTATE`.
