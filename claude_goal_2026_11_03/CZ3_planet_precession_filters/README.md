# CZ3_planet_precession_filters: TID and LOC PASS astra's planetary precession gate by about seven orders of magnitude on both footings, so both SURVIVE FIVE ON ALT; HALF (r_M/2) FAILS at Mars and Saturn

Criteria `FROZEN_CRITERIA.md` (16e2226f95), committed alone before the script. Run `OMP_NUM_THREADS=1 python3 -I cz3.py`, output `cz3.out` / `cz3.json` / `cz3.time` (2 s, 0.09 GB); MUTATE twin `cz3_MUTATE.*`. The gate is astra's AZ12 (`astra_goal_2026_11_03/P2/AZ12_orbit_precession`), re-implemented here; astra's files were read, not edited. No download. κ = ½ FITTED, held fixed. Footings never pooled. Not theory closed. Nothing here says the data favour the framework.

What the gate tests: the radial monopole of the filtered anomalous source, from Gauss' law, orbit-averaged exactly into a secular perihelion rate for six planets. A planet passes if |rate| / max(EPM, INPOP) ≤ 2. The Sun's field is filtered row-wise with CZ2's ξ at the Newtonian Galactic field.

| footing | form | ξ at Saturn | worst planet Z | Mars Z | **Label** | with CZ2 |
|---|---|---|---|---|---|---|
| canonical | TID | 261 r_M | Saturn 1.6e-7 | 1.8e-10 | **PASSES PLANETS** | fails MW, SPARC |
| canonical | LOC | 208 r_M | Saturn 3.1e-7 | 3.5e-10 | **PASSES PLANETS** | fails MW, SPARC |
| canonical | HALF | 0.5 r_M | Saturn 11.2 | 3.06 | **FAILS: Mars, Saturn** | fails Cassini |
| alt | TID | 238 r_M | Saturn 3.4e-7 | 3.8e-10 | **PASSES PLANETS** | **TID SURVIVES FIVE ON ALT** |
| alt | LOC | 189 r_M | Saturn 6.7e-7 | 7.5e-10 | **PASSES PLANETS** | **LOC SURVIVES FIVE ON ALT** |
| alt | HALF | 0.5 r_M | Saturn 18.1 | 4.97 | **FAILS: Mars, Saturn** | fails Cassini |

The labels match the expectation written in the criteria, in both direction and size. HALF's Z is 1.60x AZ12's (11.17 / 6.98), which is the Gaussian core √(2/π)/3 against the resolvent's 1/6 at the same ξ.

## Reading
- **This gate doesn't separate the two local rules; it only removes fixed-width filters.** In the Newtonian regime both local rules give ξ ∝ r g / g*, so near the Sun ξ is hundreds of r_M and the phantom inside the planets' orbits is smoothed to almost nothing (A ∝ r/ξ³). Any filter with ξ fixed near r_M/2 fails here, KT25's and astra's resolvent alike.
- **astra's and CZ2's Newtonian conversions agree exactly** (K4, to 1e-8): g_e²/(g_e + a0) is the inverse of the simple ν.

## As hard as a fail
- **ξ at the Sun is 7–9 pc** (238 r_M on alt). That's larger than the distance to the nearest stars, yet ξ is built from the Sun's field alone, as an isolated point mass. Within that radius the Galactic disc's local density and nearby stars dominate the mass a real filter would smooth. The spherical isolated-Sun model behind both Cassini and this gate is not self-consistent at that scale. It's stated, not fixed, and it's the same model KT16/KT27/KT28's Cassini rows used.
- Monopole only, with no ephemeris refit and no covariance (AZ12's scope). The quadrupole is CZ2's Cassini row.
- CZ2's caveats carry over: post hoc rules, corner-cell MW, SPARC median near its line, the 1D external-field form.

## Checks
K1: AZ12's kernel reproduces astra's Saturn 6.983944 / 11.329246 and Mars 1.918578 / 3.112914. K2: AZ12's oracles at all six eccentricities. K3: changing the orders changes Z by ≤ 3e-12, except HALF at 4.5e-10. K4: e agrees to 1e-8. K5: doubling the ξ grid changes Saturn by ≤ 9e-6. 0 failed checks.

## MUTATE (filter removed, h = GM☉/r²), `cz3_MUTATE.out`
It bites and exits 1. Every planet fails in every arm: worst Mars Z 1.68e4 canonical, 2.03e4 alt, and Saturn 9.7e3 / 1.2e4, matching AZ11's "above 16000/19000" for no filter. The checks are forced under MUTATE; K3 there is 1.1e-4, since the unfiltered case converges more slowly. The twin isn't graded.
