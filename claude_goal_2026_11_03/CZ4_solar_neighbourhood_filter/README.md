# CZ4_solar_neighbourhood_filter: with the Galactic disc and the nearby stars inside the filter, TID and LOC still PASS the planets (worst Saturn Z 3–4e-4) and Cassini (≤ 0.44x) on both footings, so both SURVIVE FIVE ON ALT WITH NEIGHBOURS; the neighbourhood term is now ~1000x the Sun's own term at the planets

Criteria `FROZEN_CRITERIA.md` (285353a57b), committed alone before the script. Run `OMP_NUM_THREADS=1 python3 -I cz4.py`, output `cz4.out` / `cz4.json` / `cz4.time` (57 s, 0.20 GB); MUTATE twin `cz4_MUTATE.*`. The baryon densities are read from the committed S3 Milky Way models (`rebuild_2026_10_22/S3_v3_mw_seals/s3_mw.py`, imported, not edited). No download. κ = ½ FITTED, held fixed. Footings never pooled. No cold component, no particle. Not theory closed. Nothing here says the data favour the framework.

What changes from CZ3: with ξ of 7–250 pc at the planets, the filter takes in the neighbourhood, and the Sun's own field no longer screens ν there. So the Galaxy's local phantom density (ν_e − 1 times the baryon tide, plus the ν' term) acts inside the planetary orbits. g̃ = h̃☉ r̂ + e x̂ + T·r: the disc tide T is built from the largest S3 midplane density (B2b, 0.160 M☉/pc³; McMillan 0.107), unsmoothed, at the worst in-plane slope β. The nearby stars enter through a 3σ Campbell bound plus α Cen, added in absolute value.

| footing | rule | ξ Mercury / Saturn | worst planet Z_cons | of which Sun / disc / stars | Cassini total (Sun + env) | **Label** | with CZ2 |
|---|---|---|---|---|---|---|---|
| canonical | TID | 249 / 10.1 pc | Saturn 3.3e-4 | 1.6e-7 / 3.0e-4 / 2.4e-5 | 0.210x (0.208 + 0.0018) | **PASSES WITH NEIGHBOURS** | fails MW, SPARC |
| canonical | LOC | 198 / 8.0 pc | Saturn 3.4e-4 | 3.1e-7 / 3.0e-4 / 3.4e-5 | 0.0058x (0.0039 + 0.0018) | **PASSES WITH NEIGHBOURS** | fails MW, SPARC |
| canonical | HALF | 0.019 pc | Saturn 11.2 | Sun-dominated | 1.18x | **FAILS: Mars, Saturn, Cassini** | fails Cassini |
| alt | TID | 206 / 8.3 pc | Saturn 4.0e-4 | 3.4e-7 / 3.6e-4 / 3.8e-5 | 0.444x (0.442 + 0.0019) | **PASSES WITH NEIGHBOURS** | **TID SURVIVES FIVE ON ALT WITH NEIGHBOURS** |
| alt | LOC | 164 / 6.6 pc | Saturn 4.2e-4 | 6.7e-7 / 3.6e-4 / 5.4e-5 | 0.023x (0.0215 + 0.0019) | **PASSES WITH NEIGHBOURS** | **LOC SURVIVES FIVE ON ALT WITH NEIGHBOURS** |
| alt | HALF | 0.018 pc | Saturn 18.1 | Sun-dominated | 2.97x | **FAILS: Mars, Saturn, Cassini** | fails Cassini |

The labels and sizes match the expectation written in the criteria (Saturn Z_env ≈ 1e-4, Cassini env ≳ 500x below the ceiling). The disc's ΔA matches the linear formula (r/3)[(ν_e − 1) tr T + ν'_e (e/a0) T_xx] to ≤ 5e-6 everywhere.

## Reading
- **The self-consistency caveat from CZ3 is closed for these two gates.** The physics term it pointed to is real and dominates: at every planet the un-screened Galactic phantom is ~1000x (Saturn) to ~1e6x (inner planets) the Sun's filtered term. It is still ~2500x under the pass line at Saturn. In density terms it is a uniform phantom of ~0.05–0.08 M☉/pc³ inside the solar system.
- **This is a prediction of the local rules, not a fit:** a secular perihelion drift A = k r, with k = (1/3)[(ν_e − 1) tr T + ν'_e (e/a0) T_xx] ≈ −1.6e-30 s⁻² (alt), the same at every planet and largest in absolute rate at Saturn (≈ 4e-4 of Saturn's ephemeris σ). It is far below reach.
- **Cassini barely moves.** Putting the neighbourhood tide into ξ changes ξ only beyond the Sun's tidal radius (~1 pc), and Q2☉ is unchanged to four digits. The environment's own quadrupole is ≤ 0.0019x of the ceiling, even bounded by the whole local Oort-limit tide (S3's 0.166 / 0.174 M☉/pc³).
- **Nothing here separates TID from LOC or the footings.** The verdict still rests on CZ2: alt only, MW corner cells, SPARC near its median line.

## As hard as a fail
- **K1 fails as frozen, at Mars only, for TID and LOC** (4 failed checks). The Sun-only Mars Z is 1.8e-10 (canonical TID) to 7.5e-10, and CZ4 differs from CZ3 by 0.65 %, 0.01 %, 0.04 % and 0.06 %. That term sits at a round-off floor: re-running CZ3's own code with only the η root computed differently moves its Mars value by 0.3 %, and changing the angular order moves it ±0.3 %. With the zero-order term subtracted, it converges to 1.7563e-10 (canonical TID), 0.08 % from CZ4's value. Saturn and every HALF row reproduce CZ3 to ≤ 6e-6. The frozen 1e-4 tolerance was too tight for a number at round-off; it's left failed, not re-set. It doesn't touch the grade: Mars' Z_cons (8e-5 to 1e-4) is disc-dominated by 5e5x.
- The slab tide is at the midplane. The Sun's 20 pc height, spiral arms and the Local Bubble are ignored, and the Bubble lowers ρ, so this errs high. Vertical smoothing at ξ would lower ρ̃ to 0.44–0.97 of the midplane value (printed, not graded), so the graded numbers are upper bounds.
- The stars are a linear 3σ bound with M_w = 2 M☉, not a realisation of the real neighbourhood (positions of the actual nearest stars aren't used; α Cen is placed in the worst orientation). At ξ = 8 pc the bound is |tr T*| 4.2e-31 s⁻², against the disc's 9.1e-30.
- CZ2/CZ3's caveats carry over: post hoc rules, row-wise spherical filter, |g| not iterated, Newtonian Galactic field from the simple ν, monopole plus one quadrupole number, no ephemeris refit.

## Checks
- K2: the linear formula holds to ≤ 5e-6.
- K3: doubling the angular orders changes Z_cons by ≤ 3e-7.
- K4: ξ at the planets is unchanged by the neighbourhood (≤ 1e-13).
- K5: the blob-Hessian oracle holds to 3.4e-6.
- K6: with ξ unchanged, Q2☉ reproduces CZ2 (0.2079 / 0.4419 TID, 0.003948 / 0.02147 LOC).
- K1: as above, failed at Mars for TID and LOC.

## MUTATE (ρ_b × 1e5, a dense cluster-core neighbourhood), `cz4_MUTATE.out`
It bites and exits 1. Saturn's Z_cons is 27.3 canonical and 33.0 alt for both rules, and every arm fails Mars, Saturn and Cassini (Q2 total 181–194x). The scaling checks by hand: the density term scales by exactly 1e5 but the in-plane β term doesn't, giving 0.906 × 1e5 × 3.6e-4 ≈ 33. Under MUTATE the neighbourhood in ξ does move Q2☉ (LOC 0.0039 → 1.55x), so that route is live, just negligible at the real density.
