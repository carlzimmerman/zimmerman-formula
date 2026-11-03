# KT16_filtered_phantom_cassini: SCALED FILTER (eps 0.2154) FAILS CASSINI, 69x and 103x; UNIVERSAL 2 kpc PASSES. Threshold: xi at least 0.45 (canonical) and 0.50 (alt) times r_M passes, only about 2.3x above the Milky Way's eps

Criteria: `FROZEN_CRITERIA.md` (72a296bf17), alone first, confirmed landed before any script, **not blind**. `kt16.py`, `kt16.out`, `kt16.json`, `kt16_MUTATE.out`, `kt16_MUTATE.json`. No download. κ = 1/2 FITTED and held fixed. Footings never pooled. Not theory closed. Register K827. Seconds.

Sun's phantom sourced by its mass smoothed over xi, simple nu, external field 2.32e-10 m/s^2, ceiling 5.2e-27 s^-2, KT7's integral generalised to a smoothed field.

| xi | canonical (eta 2.48, r_M 7961 AU) | alt (eta 2.05, r_M 7241 AU) |
|---|---|---|
| 0, plain QUMOND | q 0.348, 7.88x: FAIL | q 0.301, 9.05x: FAIL |
| 0.2154 r_M (KT15's A2), 1715 / 1560 AU | q 3.04, **68.9x: FAIL** | q 3.42, **103x: FAIL** |
| 2 kpc universal | below 1e-9x: **PASS** | below 1e-9x: **PASS** |
| smallest passing xi / r_M | **0.450** (3583 AU) | **0.504** (3649 AU) |

## Reading
- **The expectation held for the arms.** A filter smaller than r_M makes Cassini worse than plain QUMOND: inside xi the Sun's smoothed field falls below the Galaxy's, nu - 1 is order one, and the anisotropy is large. q peaks near the smallest xi scanned (0.05 r_M, 4800-7300x).
- **The threshold is the useful number.** Above about 0.5 r_M the smoothing spreads the Sun's phantom far enough that the quadrupole falls under the ceiling. My hand estimate put the needed eps near 1.7; the integral says 0.45-0.50. So a scaled filter needs eps of at least 0.50 at the Sun, against 0.2154 fitted to the Milky Way in KT14. **That's a factor 2.3, not the factor 8 I guessed.**
- **That opens one clean test.** eps = 1, xi equal to the system's own MOND radius sqrt(G M / a0), has no fitted number and passes Cassini on both footings by this table. For the Milky Way it gives xi about 9.3 kpc (alt). KT14 tested only up to 2 kpc. For dwarfs it gives 0.02-0.2 kpc, still inside most half-light radii. Next lane: eps = 1 on the Milky Way's in-prior cells and the dwarfs, frozen before running.
- **Open in the definition:** "the system's mass M" isn't a local field. The Sun sits inside the Milky Way, and here its xi uses 1 solar mass. A field equation would need to say which mass sets xi. Not solved here.

## Checks
C1: xi = 0 reproduces KT7's dblquad `q()` at both footings, relative 1e-8. C2: smoothed field limits to 9.5e-10. C3: doubled resolution moves the plain and scaled q by at most 4.5e-4. **C3 FAILED on the universal 2 kpc arm:** q is about 1e-11 there, the integral's cancellation floor, and doubling resolution moves it by order one. The analytic scaling (r_M / xi)^3 gives about 1e-14, so the true value is far below the ceiling either way; the PASS doesn't depend on those digits. Disclosed; exit 1 from that check. MUTATE (nu = 1): q = 0 everywhere, exit 1.
