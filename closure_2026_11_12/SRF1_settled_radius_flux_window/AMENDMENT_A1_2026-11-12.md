# SRF1 AMENDMENT A1 (2026-11-12): rare-group scope, forced counts, and a reduced grid, fixed before any flux number

Committed alone, after the halo-model tables were built and before any flux field of this lane was computed. FROZEN_CRITERIA.md
(fa73352ceb) stays the reference; everything not named here is unchanged.

## What I saw (halo model only, no flux, no realised field)

- Known answer (c0) already reads PASS at z 2.2 on both footings: my record-convention R_cold equals SRH1's stored R_cold to
  1.7e-6 / 2.0e-6 / 5.7e-6 (f 1, 2, inf; canonical) and 1.6e-6 / 2.6e-6 / 5.3e-6 (alt) on k 0.3 to 10 h/Mpc (tolerance 1e-4).
- At z 2.2 the settled layout's turnaround-scope one-halo difference at k 3 h/Mpc is carried 99.9 to 100 % by rare bins
  (expected count in the 20 Mpc/h box below 30; the first rare bin is log M 11.1). By 0.5 dex group (canonical, f 1.00 /
  1.30 / 2.00): 12.0: 13 / 13 / 13 %; 12.5: 32 / 25 / 23 %; 13.0: 38 / 38 / 36 %; 13.5: 16 / 22 / 24 %; 14.0: 1.3 / 1.6 /
  2.3 %; 11.5: -0.3 / -0.1 / +1.1 %; 11.0 and above 14.5: under 0.3 %. Alt is similar (14.0 up to 2.8 %).
  Expected counts in the box: 12.0: 7.6; 12.5: 1.36; 13.0: 0.15; 13.5: 0.0077; 14.0: 8.8e-5.
- So the stratified estimator is the whole measurement at z 2.2, not a correction. The box's mass is about 6.8e14 Msun/h:
  twelve forced haloes of 1e13 to 1e14 would hold 18 % to over 100 % of it, which is not a box of IGM any more.
- One flux field costs about 5 s; nine groups x 15 f values x 30 parts does not fit the budget.

## Changes

1. **Groups kept:** a 0.5 dex rare group is forced if the absolute value of its share of the turnaround-scope one-halo
   difference at k 3 h/Mpc is at least 3 % at any of f = 1.00, 1.30, 2.00, at that z and footing. The share dropped is
   computed and reported per z, footing and f (expected at z 2.2: about 1.5 % at f 1, about 4 % at f 2, mostly 14.0 and 11.5).
2. **Forced count:** n_g = min(12, max(1, floor(0.05 rho_m V / M_g))), M_g the expected-count-weighted mean turnaround mass
   of the group (each group's forced mass at most about 5 % of the box, except a single halo heavier than that).
3. **Flux grid (all 12 bins):** f = 0.70, 0.90, 1.00, 1.10, 1.20, 1.30, 1.40, 1.50, 2.00, 3.00, inf. f = 0.30, 0.50, 0.80 are
   dropped from the flux run (halo-model numbers kept at every f). f = 0 (known answer a) and MU2 at the anchors, seed 0.
4. **Poisson-only reading:** f = 1.00 and inf only (inf is known answer b).
5. **Seeds unchanged:** anchors 0 and 1 (base and forced boxes), other bins 0.
6. **Mutations:** M1 (saturation removed) at z 2.2 and 3.0, seed 0, f 1.00, 1.30, 2.00; bites as frozen (x 1.25 at f 1.30 on
   those bins). M2 (MU2) at the anchors, seed 0, as frozen.
7. **Brackets:** z 2.2 and 3.0, seed 0, f 1.00, 1.30, 2.00 (lambda_P x 0.5, x 2, 100 proper kpc; gamma 1.2, 1.6; tau x 0.9,
   x 1.1); clustered placement and N 256 at z 2.2, seed 0. The 12-bin estimate = primary 12-bin x (bracket / primary on the
   z 2.2 + 3.0 bins at seed 0). B-conv as frozen.
8. Not bracketed, stated as left out: the threshold 30, the share cut 3 %, n_g, uniform placement of forced haloes.

The labels, gate, statistic and known answers are unchanged. The as-frozen reading cannot be run inside the budget; the
results are reported under this amendment, and RESULT says so first.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
