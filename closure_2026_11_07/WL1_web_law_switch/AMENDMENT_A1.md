# WL1 amendment A1 (technical): stage 2's web statistic. Filed after stage 1's numbers, BEFORE any stage-2 number

Kappa = 1/2 FITTED; not theory closed. Adopts nothing.

## Disclosure
Stage 1 has been run (wl1.out): K-G6 PASSES at the ceiling and at the lower reading on both footings, GB1 rows equal L0.
Its R_ms values are 0.9-3.7 Mpc for the KiDS lens masses. No stage-2 number of any kind exists. This amendment is
motivated by those R_ms values. Before writing it, an order-of-magnitude estimate (not a graded number, not saved) was
made: the retained phantom per L* galaxy is of order 1e13 Msun. So a large q_pop is expected. That expectation is
stated here so the reader can weigh the amendment.

## Why stage 2 as frozen cannot see the key
Frozen stage 2 marks multi-streamed cells on SV5 iter_1's own field with the Zel'dovich criterion. Those cells are
15.6 Mpc across, at 128^3 in 2000 Mpc. Every host's R_ms (0.9-3.7 Mpc physical today, smaller earlier) is below one
cell. The grid would therefore read F = 0 by resolution alone. SV5 itself flags its web as a floor ("finer cells raise
the web's charge peaks"). Under K_ms, though, the law stays ON inside each host's R_ms. Stage 1 needs this, because the
KiDS signal to 3 Mpc is that retained phantom. That phantom is a lensing source. In the action, lensing equals dynamics
(V3W W3). It is present wherever galaxies are, so the CMB-lensing kernel (z 0.5-5) sees it.

## Stage 2, as amended (graded; replaces the grid reading, which is not computed)
- **Population phantom ratio** q_pop(z) = rho_ph,pop / rho_d. Both are comoving densities.
  - rho_d = omega_d rho_crit,100 (omega_d 0.11958060, the target's dust).
  - rho_ph,pop = Int phi(M*) M_ph(< R_ms(M_b, z)) dlog M*, over 9 <= log M* <= 12.
- **GSMF:** Driver+2022 double Schechter, from the record's closure_program_2026_10_27/population/inputs.json (raw
  survey data). The h70 conversion is exactly compute_population.py's, at the corner's h = 0.65.
- **Conservative choices** (each makes q_pop smaller):
  - M_b = M* (no gas);
  - R_ms = R_ms^L, the lower graded reading (law-on, no dust), computed at the epoch z (turnaround at a(z));
  - phantom bias 1 relative to the dust (galaxies are biased >= 1);
  - z = 0 GSMF used at z_eval. The comoving stellar mass density is not larger at z > 0, so M* is not larger either.
- **Gain:** r_pop = (1 + q_pop)^2. Line r_pop <= 1.072 (SV5 iter_1's line), so q_pop <= 0.0354.
- **Graded epoch:** z_eval = 1, near the PR4 lensing kernel peak. z = 0.5 and 2 are reported.
- **Reported:** the factor by which phi M_ph would have to fall to meet the line. Also the self-consistent R_ms reading
  (NC, Newton outside R_ms, dust counted).
- **MUTATE-A1:** R_ms -> 0 must give q_pop = 0. M_ph is then 0, which bites by construction; it is printed.
- **KA-A1:** the GSMF integral of M* over 9-12 at h = 0.65 is reported next to compute_population's analytic total.
  This checks the h conversion.
- **Labels:**
  - FAIL (stage 2, population phantom) if q_pop(z = 1) > 0.0354 on either footing.
  - Otherwise stage 2 passes, and stages 3-4 follow as frozen.
