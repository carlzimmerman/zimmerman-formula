# QX24 iter_1 frozen criteria: is the law's hot/cold step keyed on ENVIRONMENT?

Frozen before any graded number of this lane. Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Both footings, never
pooled. Rules: closure_2026_11_06/SWARM_BRIEF.md.

## Why
QX20-QX23: the plain-law offset step is not keyed on M_b, g_N, depth, r/r_M, f_gas, kinematic support, cold gas (inside SPARC's
range), or uncounted baryons. Post-data lead (QX23, 4 systems): gas-poor LG FIELD dwarfs +0.05, gas-poor SATELLITES +0.20 to
+0.22. Hypothesis E (tested, not adopted): the boost turns on in a host's environment.

Two cautions, stated up front:
- **Sign.** The standard EFE LOWERS the MOND boost in a host's field, so a key that RAISES the offset near a host is not EFE.
  The offsets used here are plain-law offsets with no EFE. With EFE included, satellite offsets would be larger still.
- **Tides.** Tides and non-equilibrium inflate satellites' dispersion masses. T3 separates that from environment.

## Environment variable (measured, not fitted)
x_e = Newtonian external field / a0 (footing a0).
- Dwarfs: X1's x_e_mid (rebuild_2026_10_22/X1_hosted_recount/x1_per_system.csv), the host's field at d_host.
- SPARC: gext_vectors_2026/data/gext_vectors.csv, log_eN_noclu (units 1.2e-10 m/s^2), x_e = eN * 1.2e-10 / a0.
  log_eN_maxclu is reported as a bracket.
- Ellipticals: the record's estimator (gext_estimator, ks115, as QX14) at each galaxy's position and Humphrey D, noclu and
  maxclu.
  - Positions: the median SLUGGS GC position (real_research/data/sluggs_forbes2017_gcvel.tsv) where the galaxy is in SLUGGS.
  - Otherwise standard literature coordinates written in the script, disclosed as not from a file.

## Key E, calibrated on dwarfs only (frozen rule)
E(x_e) = Delta_s * H(x_e - x_c), with:
- Delta_s = median plain offset of the graded satellite classes (MW classical + bright M31, LW1 per_system 'plain') minus the
  SPARC anchor (QX20 sparc_mean), per footing;
- x_c = sqrt(max x_e over LG field dwarfs * median x_e over the graded satellites).

Everything else is predicted from E.

## Tests
- **T1 KiDS isolated lenses** (Brouwer+21 Fig-8 isolated colour split; isolated = no neighbour with > 0.1 M* within 3 Mpc).
  - E predicts an early/late split D = 0, since isolated lenses sit below x_c by construction.
  - Observed D is QX21's +0.158 +- 0.064 (total), CARRIED and KNOWN BEFORE THIS FREEZE (disclosed).
  - T1 KILLS E for lenses if D/sigma >= 3, reads COMPATIBLE if < 2, and is NO VERDICT otherwise.
  - Reported, not graded: the isolated Sersic split (Fig-8 Sersicbin 1/2), with the same D statistic and covmatrix.
- **T2 ellipticals** (QX18's per-galaxy plain-law offsets, Kroupa, median over 2/4/8 Re).
  - E predicts 0 for every elliptical with x_e < x_c on the noclu reading.
  - T2 KILLS E if the median offset of those ellipticals exceeds 0.15 dex (QX18's G7 line).
  - It reads COMPATIBLE if they sit <= 0.15 and those with x_e >= x_c sit >= Delta_s - 0.15.
  - NO VERDICT if fewer than 2 ellipticals fall below x_c.
  - Reported: the Spearman of offset vs log x_e (N 7, no line).
- **T3 satellites: environment vs tides.**
  - Tidal susceptibility tau = R_e / r_J, with r_J = d_host * (M_W / (3 M_host))^(1/3).
    - M_W = 4 sigma^2 R_e / G (Wolf), from X1's sigma and rh_pc.
    - M_host = V_c^2 d_host / G, with V_c = 200 km/s for the MW and 230 km/s for M31.
  - T3a (graded): tidally safe satellites (tau < 0.05, all satellite classes in X1 except ultra-faints) compared with LG field
    dwarfs.
    - STEP SURVIVES TIDES if their median plain offset minus the field median is >= 0.15 dex and the 95% bootstrap CI lower
      bound is > 0.
    - TIDES ACCOUNT if the CI contains 0.
    - Otherwise NO VERDICT, and NO VERDICT if N_safe < 5.
  - T3b (reported): over all satellites (ultra-faints included), the partial Spearman of offset with log x_e at fixed log tau,
    and with log tau at fixed log x_e.
- **T4 SPARC** (per-galaxy mean plain-law residual at disc Upsilon 0.5, bulge 0.7, QX23's sparc_points).
  - Galaxies with x_e >= x_c (noclu) form the 'dense' set.
  - T4 KILLS E if N_dense >= 5 and mean(dense) - mean(rest) <= Delta_s - 3 sigma (bootstrap over galaxies).
  - COMPATIBLE if within 2 sigma of Delta_s.
  - NO POWER (NO VERDICT) if N_dense < 5.
  - Reported: Spearman of residual vs log x_e over all SPARC.

## Overall label
- **KILLED** if any graded test (T1, T2, T4) kills E with power, on either footing.
- **SUPPORTED** if T3a reads STEP SURVIVES TIDES, no test kills, and at least one of T1, T2, T4 reads COMPATIBLE.
- **NO VERDICT** otherwise.

If E is killed, the README states plainly which measured variables have now been tried and failed. That list is the crisp
target.

## Known answers and controls (separate outputs, qx24_MUTATE.*)
- KA1: the graded satellite medians reproduce QX21 T2 (MW classical 0.2445 canonical) to 1e-4.
- KA2: the SPARC anchor reproduces QX20 sparc_mean to 1e-6.
- KA3: SPARC x_e is taken from gext_vectors.csv, and the estimator reproduces it on 3 SPARC galaxies to 1e-3 dex.
- M1 (shuffle): permute x_e among the dwarfs (1000 draws). T3b's |partial rho| for log x_e must fall below its 95th
  percentile in >= 95% of draws. Any observed environment trend must exceed the shuffle's 95th percentile to be reported as a
  trend.
- M2 (Newton): replace plain offsets with X1's Delta[Newton]. Delta_s must move by > 0.3 dex (bites).

Light compute, one thread.

Kappa = 1/2 FITTED; not theory closed.
