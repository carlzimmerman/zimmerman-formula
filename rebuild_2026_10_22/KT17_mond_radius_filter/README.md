# KT17_mond_radius_filter: eps = 0.55 PASSES ALL THREE on both footings (Milky Way on star-count cells, 24 dwarfs, Cassini). eps = 1 fails the Milky Way. A lead with a window, not a derivation; owed SPARC, wide binaries, lensing, clusters

Criteria: `FROZEN_CRITERIA.md` (3d4dba837a), alone first, confirmed landed before any script, **not blind**. `kt17.py`, `kt17.out`, `kt17.json`, `run.log`, `kt17_MUTATE.out`, `kt17_MUTATE.json`, `run_mutate.log`. No download. κ = 1/2 FITTED and held fixed. Footings never pooled. Not theory closed. Register K828. 16 minutes, peak RSS 0.79 GB, one thread, nice 15.

Field equation: filtered QUMOND, simple nu (the board law), phantom sourced by the mass smoothed over **xi = eps sqrt(G M_b / a0)**, the system's MOND radius times eps.

| | canonical, eps 1 | canonical, eps 0.55 | alt, eps 1 | alt, eps 0.55 |
|---|---|---|---|---|
| Cassini (x ceiling) | 0.0038: PASS | 0.247: PASS | 0.0083: PASS | 0.544: PASS |
| Dwarfs, with MW field (plain: 15) | 15/24: SURVIVES | 15/24: SURVIVES | 15/24: SURVIVES | 15/24: SURVIVES |
| Milky Way xi | 9.1-10.9 kpc | 5.0-6.0 kpc | 8.3-10.0 kpc | 4.6-5.5 kpc |
| MW in-prior cells passing all four | 0 (v_c max 217.4) | **5** | 0 (v_c max 221.1) | **62** |
| MW lowest K with v_c in line | none | 65.5 | 67.7 | 63.9 |
| **Label** | FAILS: Milky Way | **PASSES ALL THREE** | FAILS: Milky Way | **PASSES ALL THREE** |

## Reading
- **This is the first rule in today's sequence that passes the Milky Way on star-count baryons, the Local Group dwarfs (as well as plain QUMOND does) and Cassini, together, on both footings.** Plain QUMOND with the same kernel fails the Milky Way (KT13) and Cassini (7.9x and 9.1x, KT16).
- **Why it works.** Smoothing the phantom's source over the MOND radius does two jobs. In the Milky Way it spreads the extra pull vertically, so K_z falls to the measured value while v_c holds (KT13's disc problem). Around the Sun it spreads the phantom over thousands of AU, so the anomalous quadrupole falls under Cassini's ceiling. In dwarfs xi stays well inside r_half (Fornax: 9.3 to 9.6 km/s against plain's 9.7 at Upsilon 2), so nothing changes there.
- **eps isn't derived; there's a window.** Cassini needs eps >= 0.45 (canonical) / 0.50 (alt) (KT16). The Milky Way passes at 0.55, and at eps = 1 v_c falls short (217-221 against a floor of 219.9) because the phantom inside R0 gets smeared out. So the allowed range is about 0.5 to somewhere below 1. 0.55 was picked as the smallest round value above both Cassini thresholds, before the MW run, not tuned to the Milky Way. The natural eps = 1 is out.

## What weakens it, stated as hard as the pass
- **The Milky Way cells are at the edge of the priors.** On canonical, all 5 sit at Sigma_b 53.9 (+2 sigma), M_bb 2.12e10 (+2 sigma), thick share 0.35, in BV2 (thick R_d 2.0). On alt, of the 30 best stored, 23 have thick share 0.35 and 7 have 0.26. Star counts give 12 +- 4 percent (RF1 A4), so 0.26 is about +3.5 sigma. I didn't check whether any cell at 0.12 passes (the JSON keeps the best 30 of 62); that's a quick next check. BV2's thick R_d of 2.0 kpc is the star-count value, so that one is fine.
- **The K_z scale length fails everywhere:** h 3.18-3.32 against 2.72 +- 0.15, strict count 0. It isn't in the frozen gate, but it's measured and it misses by about 3 sigma.
- **"The system's mass" isn't defined locally.** The Sun's xi uses one solar mass though it orbits inside the Galaxy; the Milky Way's uses its total. A field equation would have to choose. Until it does, this is a rule, not a theory.
- **Owed before any claim:**
  - **SPARC.** A galaxy of 1e10 Msun gets xi of about 1.9 kpc, so inner points of small discs lose part of their boost. That could break the a0 law's main success.
  - **Wide binaries.** xi is about 3,900-4,400 AU for a solar-mass pair, so the anomaly should be suppressed below that separation. That's a sharp, testable prediction.
  - Lensing and clusters.

## Checks
C1: xi = 0 reproduces UX5's form Q on all 1375 cells per footing, max relative 0. C2: smoothed mass within 1.2e-3 of the original at every tested xi (tolerance 2e-3). Q5: doubled grid on the best passing cell, dK +0.05 / +0.06, dv +0.08: converged. Cassini and dwarf code as KT16 and KT15.

**C3 FAILED as frozen, and the failure is in the check.** The solver grid covers the upper half-space only (`theta_edges(..., full=False)`), so its gas sum is half the full integral: 5.955e9 x 2 = 1.191e10, matching the integral to 1e-4. M_gas = 1.191e10 is right; the check didn't account for the half grid. Disclosed, exit 1. C2's ratio is unaffected, since both sides use the same grid.
