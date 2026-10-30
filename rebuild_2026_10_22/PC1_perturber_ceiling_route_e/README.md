# PC1_perturber_ceiling_route_e: floor halos have a hard mass ceiling; J0946's dark solution breaks it, and the ultra-faints sit under it

Criteria: `FROZEN_CRITERIA.md` (ad466e9c38, committed alone). κ = ½ FITTED. Footings never pooled. Route E, Newtonian. Cold dark
energy, not matter; no particle species. Not "theory closed". Nothing here says the data favour the framework. Every number is from
`pc1_ceiling.out` / `pc1_results.json`, or from `pc1_posthoc.out` where marked POST-HOC.

## The ceiling

A Burkert halo with ρ₀r₀ = a₀/(2πG) obeys M₃D(<r) ≤ 1.599 Σ r², whatever its M200 or r₀. This is the same statement as
g ≤ 0.2545 a₀, which is X47's g_T: **the identity is not new**. What is new is using it as an upper bound on measured objects.

## Frozen results

| object | canonical R | alt R | class (both footings) | dark reading R, reported |
|---|---|---|---|---|
| J0946 dark, <0.3 kpc | 31.2 | 25.8 | **EXCEEDS** | 33.8 / 28.0 |
| J0946 dark, <0.6 kpc | 15.6 | 12.9 | **EXCEEDS** | 16.3 / 13.5 |
| B1938 A, <0.6 kpc | −5.4 | −4.5 | ALLOWED (baryon room) | 1.64 / 1.36 |
| B1938 V, 80 pc, 2D | 0.31 | 0.26 | ALLOWED | same |

J0946 luminous: CONSISTENT on both footings.

**Label:** route E joins the law in needing J0946's luminous solution. CFG671's deciding observation (the satellite's light) now
decides both pictures. B1938 V's ALLOWED is only "possible at some r₀", not a pass.

| class | N | E_C can (Z_C) | E_C alt (Z_C) | above ceiling by >2 s |
|---|---|---|---|---|
| MW ultra-faint | 31 | −0.275 (−2.49) | −0.357 (−3.24) | 0 / 0 |
| bright M31 | 25 | −0.390 (−2.58) | −0.471 (−3.11) | 0 / 0 |
| M31 others | 5 | +0.001 (0.00) | −0.081 (−0.25) | 0 / 0 |
| MW classical | 8 | −0.036 (−0.42) | −0.109 (−1.26) | 1 / 1 (Draco) |
| LG field | 13 | −0.149 (−2.12) | −0.230 (−3.21) | 0 / 0 |

**Ultra-faint label: BELOW CEILING, both footings.** X49's "more massive halos" reading stays open for pure floor halos. Median M200
needed is 2.5e6 / 2.3e6 M☉, about 4× X49's extrapolated relation. That median covers only the reachable systems. Six canonical and
five alt systems have central values above the ceiling (Canes Venatici II on canonical only; Carina III, Eridanus IV, Horologium I,
Segue 1, Willman 1 on both), none by more than 2 s, so the median leans low.

Checks K1–K4 pass. MUTATE (Σ/10) lowers the ceiling by exactly 10 and raises Z_C; it bites. K3 fails under MUTATE because 1e12 saturates
the solver, as X49's K1 does.

## POST-HOC (no verdict depends on this)

- **B1938 V's frozen 2D ceiling is inflated.** It peaks at r₀ ≈ 1.6 kpc, a nearly uniform sheet with M200 ≈ 1e10, which would not read
  as a compact perturber. In 3D at 80 pc, R = 0.96 / 0.79. At r₀ = 40 pc (M200 ≈ 1e7), 2D R = 0.81 / 0.67. V fits only just.
- **Draco is above the ceiling:** E_C = +0.148 ± 0.027 canonical, +0.068 ± 0.027 alt, g_obs 0.368 / 0.304 a₀. The excess is ×1.41 / ×1.17
  in acceleration, within the width the criteria allow for profile shape, and s has data-side errors only. It is the one kinematic
  system that presses on the floor rule directly and is not a rule failure on this evidence.
- **A single low-mass halo floor fits all five classes:** M200 = max(EM1 relation, M_f) reproduces every class at lg M_f = 6.25–7.00 on
  both footings. **This is a scan, it adds a fitted constant, and it is not a result.** It only sets a target for a derivation. It
  may also restate X24's velocity floor of about 4 km/s: the peak speed of a floor halo at 4e6 M☉ is near 5 km/s, not a separate
  measurement. CFG344's M_need 3.83e7 (lg 7.58) lies outside the window.

## Limits and deviations

- Burkert shape is the record's choice, and X81 found native 1e12 halos are cusps. Low-mass native profiles are unmeasured (X80 queued).
  If low-mass lumps are cusps, the ceiling does not apply and the floor rule itself is wrong there.
- Deviation from §2: the M_b + C over M_b ratio was reported at 1 kpc only, using the generous 2D ceiling (1.6–7.4), not at 0.3 kpc. CFG667's
  sealed Q limits are law-based and were not edited, so they should not be read as route E's prediction.
- K2 and an unused line were corrected in the script before the committed run, after the first run. No graded number changed.
- Lens masses depend on assumed profiles, and perturbers may be line-of-sight objects. Hosted dwarfs are treated as in equilibrium.

## Correction (MF1, 2026-10-30)

The post-hoc M_f window above came from a grid ending at lg 8. MF1's finer grid shows canonical passes all five classes again at lg 8.25, so 6.25–7.00 has no sharp upper edge on canonical. See `../MF1_h2_cooling_floor_mass/README.md`.
