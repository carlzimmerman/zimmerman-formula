# v3s self-consistent khronon fluid: does the MW–M31 soft lobe shell-cross? — RESULT

Owner's request (2026-10-24). Criteria `FROZEN_CRITERIA.md` (`1343f40b91`) + AMENDMENT A1 (`5129845dc5`, after the solver
tests, before production). κ = ½ FITTED; both footings, never pooled. No dark-matter particle. Not theory closed.

## Verdict (frozen rule): SELF-CONSISTENT SHELL CROSSING — on the constant-velocity orbit O2; none on the timing orbit O1

| case (h = 20 → h = 10) | soft min J by t_end | first soft crossing | distance to a galaxy |
|---|---|---|---|
| canonical O2 t_i 3 | −19.6 → −390 | 14.20 → 14.00 Gyr (t₀ + 0.2–0.4) | 69 → 43 kpc |
| canonical O2 t_i 6 | −0.65 → −4.4 | 15.60 → 15.50 | 49 → 61 |
| canonical O2 t_i 9 | −1.02 → −0.30 | 16.80 → 16.80 | 50 → 57 |
| alt O2 t_i 3 / 6 / 9 | −16.2 / −2.4 / −0.67 → −64 / −7.3 / −1.5 | 14.2/15.4/16.8 → 13.9/15.6/16.6 | 39–61 |
| canonical / alt **O1** t_i 3, 6, 9 (h = 20) | **+0.78 / +0.76 / +0.53** (alt +0.78 / +0.75 / +0.54) | none | — |

- **The self-consistent khronon does not prevent the crossings that the frozen-field model found on O2.**
  - The halos follow their galaxies: centroid offsets ≲ 25 kpc. But they lose 50–60 % (MW) and 10–20 % (M31) of their
    positive khronon mass within 100 kpc.
  - Soft-lobe elements swept by the approaching MW still fold 40–70 kpc from it, between t₀ + 0.1 and t₀ + 3.0 Gyr.
  - Crossing times agree between h = 20 and h = 10 to ≤ 0.3 Gyr; the frozen-F mode gives 14.0 / 15.2 / 17.0 Gyr (V6).
  - A soft element never gets γ_L pressure, so in v3s these folds are singular: the khronon foliation folds.
- **On the timing-argument orbit O1 the lobe is compressed but does not cross by r = 300 kpc** (min J 0.53–0.78, both
  footings). O1 was not in the rung: the frozen selection takes the smallest min J per footing, which were all O2 cases.
- O2 has the galaxies 1.3–2 Mpc apart at t_i, approaching at a constant 110 km/s, so it sweeps the MW through the old lobe.
  O1 (apocentre 1.05 Mpc at 8.5 Gyr) is the more realistic history.
- **Reading:** v3s's soft khronon can shell-cross within a few Gyr when a galaxy sweeps through a former saddle lobe. Such
  a configuration is generic in hierarchical assembly (galaxies moving through the medium's old saddles), but this run does
  not show it for the Local Group's own timing orbit. **v3s needs a caustic completion (soft-side pressure or a
  multi-stream khronon) unless galaxies never cross old lobes, which is unlikely in general.** This qualifies X3's
  "well-posed" verdict at the nonlinear level.

## Checks

| check | result |
|---|---|
| V1 Gauss law vs analytic | **FAIL as frozen** (ratio 1.88 < 2.5; worst error at r ≈ 2.1h by the axis; potential converges at 2nd order) — A1 |
| V2 Poisson vs Plummer | **FAIL as frozen** (11 % at h = 20 by a one-cell core; 3.0 % h = 10, 0.76 % h = 5) — A1 |
| V3 equilibrium | **FAIL as frozen**: 1.4–1.6e-6 > 1e-6, entirely the γ_L pressure (the AQUAL initial state omits it, γ_L∇ρ ≈ 0.002 kpc/Gyr² at a core); without γ_L the residual is 0.8–2.1e-12 |
| V4 resume | PASS (exit 75, resume, idempotent, bit-identical) |
| V5 MUTATE static masses | **FAIL as frozen**: max displacement 6.6e-3 h and \|J−1\| 2.4e-3 > 1e-3. Same cause as V3: γ_L pressure moves core khronon by ~0.13 kpc over 15 Gyr, with no lobe motion |
| V6 frozen-F mode | PASS (t_sc 14.0 / 15.2 / 17.0 vs 14.44 / 15.43 / 16.44) |
| C | reading SELF-CONSISTENT SHELL CROSSING, 6/6 rung cases confirmed, no h20/h10 disagreement |

The four FAILs are solver-accuracy or γ_L-inertness checks. None of them concerns the soft lobe's crossing, which
reproduces at both resolutions and in frozen mode. Stiff (positive) khronon multi-streams at grid scale around the moving
galaxies in every run (stiff min J ≪ 0). Physically, those are γ_L-regularised sheets far below the grid. Cost: h = 20 runs
40–60 s, h = 10 runs 4–8 min, ≤ 0.67 GB, one thread, nice 15. The engine is preemptible (V4), and no queue was needed.

## Not done

h = 5, O1 at h = 10, non-axisymmetric motions, a time-dependent outer boundary, the Hubble flow and other Local Group
members, BS dust, the DBI K, and resolving γ_L's sub-grid regularisation of the stiff sheets.
