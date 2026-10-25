# X32_bullet_cold_sector: AMENDMENT A1 (before any graded number)

Committed with the script, before the first graded run. **Seen before amending:** a smoke test of the passage machinery only.
That covered the well calibration, the isolated-control fractions inside 300 kpc, the cold-profile normalisation, and run
times. No reading, offset, κ̄ or aperture mass of this lane had been computed.

## A1.1 Wells: the frozen fallback applies (no change to the rule)

The M200 pair (1.5e15 / 1.5e14) has no Hernquist calibration. A 40 × 40 scan of (a_main, a_sub) gives a best worst-residual of
25 % of 2.3e14: the sub's total mass cannot supply its own aperture. So frozen §3.2's fallback is used: M_sub = 2.3e14. The
solution is a_main ≈ 450 kpc, a_sub ≈ 26 kpc.

## A1.2 Integrator: dt 0.5 → 0.1 Myr, N 20 000 → 5 000 per halo (implementation)

With a_sub ≈ 26 kpc and c_s ≈ 600 km/s, the cold tracer e-folds within ~0.25 kpc of the sub's centre. At dt = 0.5 Myr the
isolated control loses 6 % of its particles from the aperture (K2 would fail: 0.938). That loss is integration error. At
dt = 0.1 and 0.05 Myr the control holds (1.000). N is cut to keep the runs at minutes. K6 now compares dt = 0.1 with 0.05 Myr.
K2, K6 and their tolerances are unchanged.

## A1.3 A third fluid placement, F-c (conservative: it can only make an F exclusion harder)

The smoke test shows the cold sector at the sheet c_s sitting as a dense nucleus in each well. A frozen-§3.6 retained core
that dense would not be held back by ram pressure the way the extended X-ray gas is. Momentum, not pressure, decides where it
goes. So F gains a placement built on momentum accounting:

- **F-c (inelastic columns, b = 0).** Each projected annulus R of the two coaxial fluids merges perfectly inelastically: column
  Σ_main(R) + Σ_sub(R). In the main's frame the merged column moves at v Σ_sub/(Σ_sub + Σ_main). By the end it sits at
  BCG1 + 849 kpc × Σ_sub(R)/(Σ_sub(R) + Σ_main(R)) along the axis.
  - Each annulus (60 log bins up to the main's r_200) is carried as a Plummer sphere of its mass, with scale radius max(R, 1 kpc),
    at that position.
  - Gravity's pull-back after the collision is ignored, as in F-b.

F is now graded at the most favourable of F-a, F-b and F-c. Everything else in the frozen criteria is unchanged (observables,
σ's, classes, MUTATE). The frozen Gunn–Gott quantities (r_strip, f_core) are still computed and reported, and still define
F-a and F-b.
