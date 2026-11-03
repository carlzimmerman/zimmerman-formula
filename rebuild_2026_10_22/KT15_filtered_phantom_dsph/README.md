# KT15_filtered_phantom_dsph: universal xi = 2 kpc HURT by dwarfs (9 of 24 vs plain QUMOND's 15, with the external field); size-scaled xi = 0.215 r_M SURVIVES (15 of 24, same as plain), because its xi is under 0.05 kpc for every dwarf

Criteria: `FROZEN_CRITERIA.md` (e12926066c), alone first, confirmed landed before any script, **not blind**. `kt15.py`, `kt15.out`, `kt15.json`, `kt15_MUTATE.out`, `kt15_MUTATE.json`. No download (McConnachie 2012 on disk). κ = 1/2 FITTED and held fixed. Footings never pooled. Not theory closed. Register K826. About 4 minutes, one thread.

Sample: 24 Local Group dwarfs (V_mag <= -8, listed e_sigma; M32, NGC 147/185/205 and Sagittarius excluded as frozen). Plummer, a = R2, M = Upsilon_V L_V + 1.33 M_HI; pass = some Upsilon_V in [1, 3] within 2 e_sigma of the measured dispersion.

| arm | footing | with MW external field (primary) | isolated |
|---|---|---|---|
| A0, plain QUMOND | canonical | 15 / 24 | 19 / 24 |
| A0, plain QUMOND | alt | 15 / 24 | 19 / 24 |
| A1, xi = 2.0 kpc | alt | 9 / 24: **HURT** | 10 / 24: **HURT** |
| A2, xi = 0.2154 r_M | alt | 15 / 24: **SURVIVES DSPH** | 19 / 24: **SURVIVES DSPH** |
| MUTATE, Newton | both | 3 / 24 | 3 / 24 |

## Reading
- **A universal 2 kpc filter loses the Milky Way's own classical dwarfs.** At Upsilon 2: Fornax 5.5 km/s against 11.7, Sculptor 2.8 against 9.2, Leo I 4.3 against 9.2. What still passes are dwarfs with large errors (And XV, And IX), large radii (And II, And VII) or a lot of gas (WLM, Leo A). It falls just short of the frozen "killed" line (10 vs 9.5 isolated, 9 vs 7.5 with the external field), so the label is HURT. In substance a universal 2 kpc filter doesn't work for dwarfs. My hand estimate said killed. The line is the one frozen.
- **The size-scaled filter costs nothing here, by construction of the numbers.** eps = 2.0 kpc / r_M,MW (9.29 kpc) = 0.2154 gives xi 0.005-0.047 kpc for these dwarfs, all well inside r_half. So A2 is just plain QUMOND on dwarfs. The test was whether that holds, and it does, but it carries no extra information about the filter.
- **Plain QUMOND's own dwarf misses are unchanged:** Draco, Ursa Minor, Sextans, Carina, Canes Venatici I and others fail in A0 too, mostly under the 1D external-field approximation. That's the record's satellite liability, not this lane's.

## What it leaves, and the next test
The scaled filter xi = eps sqrt(G M / a0) survives the Milky Way (KT14, alt, at box corners) and the dwarfs. **Its next owed test is Cassini, and I expect it to fail there.** For the Sun, xi = 0.2154 r_M is about 1500 AU. Inside that radius the Sun's smoothed field drops below the Galaxy's, nu - 1 is order one, and the smoothed field is nearly linear. By hand, the resulting quadrupole scales as (r_M / xi)^3, about 100 times plain QUMOND's, which already fails at the record's ceiling. Passing would need xi of at least about 1.7 r_M at the Sun but 0.2 r_M in the Milky Way, so a scaled filter would need xi/r_M to fall with mass. That's a second fitted exponent. Next lane: compute it properly.

## Checks
C1: deep-MOND estimator on a diffuse Plummer, relative 0.0016. C2: smoothing conserves mass to 1.5e-5. C3: Gaussian width test to 7.2e-6. MUTATE (Newton): 3 of 24 pass, exit 1. The external field enters only through nu's argument, a 1D approximation, labelled; M31 and field dwarfs are treated as isolated.
