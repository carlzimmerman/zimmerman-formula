# QX7 iter_7 frozen criteria (door B): Jeans-switch retention (iter_4) + a phase-mixed remnant that traces the host

Frozen before any iter_7 number. Kappa = 1/2 FITTED; not theory closed. Adopts nothing. TEST lane under SWARM_BRIEF.md
(cold dark energy, never cold dark matter; no particle). This is a hypothesis lane: it states an idealisation in advance.

## Why

The record has two halves that were never combined:
- **QX7 iter_4:** the leaf-uniform Jeans switch lambda_J = lambda_* Omega_DE^p empties ordinary galaxies (no dust if
  R_c = lambda_0/2 >= r_ta). It passes the galaxy gates for lambda_0 >= 1.47 Mpc and builds the CMB-lensing shape. Its
  clusters fail on profile SHAPE (an isolated n = 1 core).
- **QX29 B1:** captured dust that TRACES the baryons at the cosmic share passes X-COP (-0.003/0.082, -0.027/0.087), but every
  galaxy keeps it, so KiDS fails (-0.37).

iter_7 asks: if the switch decides WHO keeps dust (iter_4's rule) and the kept dust is a phase-mixed remnant that traces its
host (QX29 B1's shape), is there a window?

## Mechanism (frozen)

- Retention: iter_4's rule, unchanged. A system keeps M_d,tot = f_cap R M_b,tot (f_cap 0.76, R 5.562) iff
  lambda_0/2 < r_ta(M_b,tot (1+R), z = 0); otherwise it keeps none.
- Profile in a retaining system (the remnant hypothesis): after capture the dust is collisionless and phase-mixed at the host's
  temperature. An isothermal component at the same sigma as the hot gas, in the same potential, has the same density shape as
  the gas. So:
  - **PRIMARY:** M_d(<r) = M_d,tot * M_gas(<r) / M_gas,tot.
    - X-COP: the measured MGAS profile, with M_gas,tot = the gas mass at Mb_last's radius, held constant beyond it.
    - Groups: the gas power law through (R25, R5), constant beyond R5.
    - Ellipticals: no gas profile on disk, so they trace Mbar (stated).
    - KiDS lenses and the G5 SPARC systems: point masses (all dust inside r).
  - **REPORTED (not graded):** M_d(<r) = M_d,tot * M_b(<r) / M_b,tot (traces all baryons, QX29 B1's shape).
- Field: the plain law g_law(G (M_b + M_d)/r^2), per footing, as iter_4.
- Stated inconsistency, which the lane does not resolve: a remnant that traces the host on 100 kpc scales cannot also carry the
  Jeans pressure that lambda_J >= 1.47 Mpc implies for a fluid (iter_5). iter_7 assumes the captured remnant is pressureless
  after phase mixing and that the switch acts only on the linear web and at capture. Any pass here is CONDITIONAL on that.
- Growth/forest: carried from iter_4 (the switch is unchanged; R1 recomputes one cell).

## Gates and label

G5, G6, G7, X-COP and groups lines exactly as iter_4/iter_5. PASS / FAIL (clusters) / FAIL (no window), by iter_4's rule.
Both footings, never pooled. A PASS is labelled "PASS (CONDITIONAL on the pressureless-remnant assumption)".

## Controls

- K1: with the profile replaced by iter_4's isolated n = 1 core, iter_4's X-COP mean/rms at lambda_0 2.154 is reproduced to 2e-3.
- K2: with the retention rule replaced by "every system keeps dust" and the profile by baryon tracing, QX29 B1's X-COP mean is
  reproduced (-0.003 / -0.027) to 0.01 (a cross-lane reproduction; differences in the loader are disclosed if it misses).
- MUTATE A: f_cap 0 gives QX2 iter_1's X-COP (+0.4675 / +0.4345) to 1e-3.
- MUTATE B: lambda_0 1e-3 (everyone keeps dust) must fail G5 or G6.
- MUTATE C: f_cap x 0.3 must move the X-COP mean by more than 0.1 dex at a window lambda_0 (the profile has power).
