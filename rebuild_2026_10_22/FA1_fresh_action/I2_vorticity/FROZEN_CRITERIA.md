# FA1 / I2 FROZEN CRITERIA: the vorticity selector

Committed alone, before any script or number for this lane. Owner, in chat, 11-04: "Yes, run both".

**Not blind.** Before writing this I read: FA1's four files and fa1_zeta.py; DR5's README (rotation-support gate,
REDUCES TO EXISTING ROWS); K1's README; KT15's README, criteria and script (24 LG dwarfs, plain QUMOND 15/24 with the
external field, 19/24 isolated); CFG323's README and its stats block (SLUGGS outer-GC offsets: 4 centrals +0.182,
err_tot 0.038; 12 non-centrals +0.062, err_tot 0.051; the four centrals are the four slow rotators); VS1-VS4's
READMEs (slow minus fast +0.12 dex, NOT SEPARATED; VS4's Pulsoni reduction +0.057, NO VERDICT); CFG713's README
(SLACS lenses want an extra ~0.36 of the projected mass inside theta_E). So I know, before any run, that the slow
rotators' mean offset sits near the +0.199 dex this file predicts for "dust on". kappa = 1/2 FITTED. Footings
(canonical a0 9.3603e-11, alt 1.1312e-10 m s^-2) never pooled. Adopts nothing. The cold sector stays retired; this
lane grades where a selector would let a dust part weigh, on baryon and kinematic data only.

## The idea (PHASE1_IDEAS.md, I2)
The dust part weighs where the matter frame's mean flow is irrotational, and is inert where the flow has ordered
vorticity. Phase 1's action: L = ... - (1/2) M^2 exp(-omega^2/omega_*^2) (A.dchi - Q0)^2, with omega^2 from the
aether aligned with the matter frame and omega_* ~ a0/c.

## The dust amount when the selector is on (same convention as FA1)
FA1's line: cluster-level dust is at least 1.5 x the law's mass. When the selector is on, a system gets that much,
D = 1.5, as extra mass proportional to the law's own mass at every radius. So g -> (1 + D) g_law, which is
+0.398 dex in g and +0.199 dex in a dispersion. This is the minimum cluster-level amount, not a fitted value. The
selector fixes where; the amount is the retired cold sector's and is not derived here.

## Reading P (primary: the action as Phase 1 wrote it)
F = exp(-omega^2 / omega_*^2), omega_* in {a0/c, 2 a0/c = sqrt(G rho_DE), 4 a0/c = sqrt(G rho_DE)/kappa} per footing.
- **G-P-CL, cluster amount.** The dust weighs in a cluster only if F >= 0.5 there. The ICM's vorticity floor comes
  from the Hitomi Perseus measurement: a line-of-sight velocity gradient of about 150 km/s across about 60 kpc
  (Hitomi Collaboration 2016, Nature 535, 117; recalled, not fetched: PROVISIONAL). A gradient is shear, which can
  be strain rather than rotation, so the floor is taken as half of it: omega_lo = 0.5 x 150 km/s / 60 kpc.
  PASS if F(omega_lo) >= 0.5 at any omega_* variant on a footing; FAIL otherwise.
- **G-P-SEP, SPARC null.** omega = V_obs / R at each SPARC point with g_b < a0 (flat or rising curve gives omega >=
  V/R; V/R is used as the floor). f = fraction of those points with F >= 0.5. Line f <= 0.046 (FA1's).
- Reported: omega and F for a dSph with 1 km/s of mean rotation at 1 kpc, and for the MW disc at the Sun.
- Label: **I2-P KILLED AT THE CLUSTER GATE** if G-P-CL fails on both footings and all checks pass.
  **I2-P ALIVE** if G-P-CL and G-P-SEP pass on both footings. Otherwise FOOTING-SPLIT or UNDECIDED.

## Reading R (reported second: a scale-free rotation-support reading)
The task's wording: inert in rotating discs, active in pressure-supported systems. F = F(x) non-increasing in
x = V_rot / sigma, with no form assumed. Clusters need F at their x, so ANY such F gives every system with x <= x_cl
at least the clusters' weight. x_cl: the ICM's rotation support, about 150 km/s against a 1D sound speed near
900 km/s in Perseus, ~0.2; cluster galaxy ensembles up to ~0.5 (PROVISIONAL, from memory of Hitomi 2016 and of
rotating-cluster studies, not fetched). Primary t_c = 0.5 (the upper value; the harder one for the SPARC null);
variant t_c = 0.25. Reading R is not a local field invariant: V/sigma is a system property. It is graded as a
necessary condition only.
- **G-R-SEP, SPARC null.** x = V_obs / sigma_HI at each SPARC point with g_b < a0 (Y 0.5 primary, 0.3 and 0.7),
  sigma_HI = 10 km/s (DR5's provisional value; 8 and 12 reported). f_SP = fraction with x <= t_c.
  SEPARATES if f_SP <= 0.046 at all three Y; DOES NOT SEPARATE if > 0.046 at all three; else UNDECIDED.
- **G-R-ETG, ellipticals.** CFG323's 16 SLUGGS galaxies, primary outer-GC offsets log10(sigma_obs/sigma_pred)
  per footing, read from `cfg323_measured_tracers_results.json`. x = V/sigma_e from ATLAS3D (Emsellem+11 table B1,
  `_external_data/atlas3d_emsellem11/tableb1.tsv`, column V/sige). On set: x <= t_c. Predicted offset: +0.199 on,
  0 off. Per set, mean offset m, err^2 = sd^2/N + s_gamma^2 + s_beta^2 + s_meas^2 x (16/N), with s_gamma, s_beta,
  s_meas from CFG323's ALL row on that footing. Z = (m - prediction)/err.
  On set: EXCLUDED if Z < -2 (the data sit below the predicted extra), ABOVE if Z > +2, ALLOWED otherwise.
  Off set: CONSISTENT if |Z| <= 2, else MISSES. Class label: ALLOWED if the on set is ALLOWED or ABOVE and the off
  set is CONSISTENT; EXCLUDED if the on set is EXCLUDED; else MIXED. An empty set is reported as such.
  The on/off split is by inner (R_e) kinematics while the offsets are at R > R_e; disclosed, not corrected.
- **G-R-DSPH, dwarf spheroidals.** KT15's sample (McConnachie 2012, V_mag <= -8, listed e_sigma, M32, NGC 147,
  185, 205 and Sagittarius excluded), restricted to MW and M31 satellites (SubG MW or M31). All are taken as
  pressure-supported, x <= t_c (most dSphs have v_rot/sigma below 0.5; a few M31 dSphs show rotation;
  PROVISIONAL). KT15's model unchanged: Plummer, a = R2, M = Y_V L_V + 1.33 M_HI, simple nu, the 1D external field
  (200 km/s)^2/D for MW satellites, global virial sigma. Dust on: sigma_pred x sqrt(1 + D). Per dwarf PASS if
  some Y_V in [1, 3] gives |sigma_pred - sigma_obs| <= 2 e_sigma (KT15's rule, from the measured errors).
  n0 = law-alone passes, n1 = dust-on passes, external-field case primary, isolated beside.
  EXCLUDED if n1 <= n0/2; ALLOWED if n1 >= n0 - 2; HURT otherwise. Per footing.
  Reported: per dwarf the largest D allowed at 2 e_sigma (any Y_V in [1, 3]); the same count with MW and M31
  satellites of any V_mag that have e_sigma (ultra-faints included).
- **G-R-BUL.** Reported: in reading R the Bullet's galaxies (pressure-supported) are on, so WEIGHT ALLOWED AT
  GALAXIES; the selector does not tell gas from galaxies (NO SIGN information beyond that).
- **G-Q2.** The matter frame at the Sun rotates with the MW disc (x ~ 220/20): dust off; Q2 INHERITS v3s's L*.
- **Keys: NOT COMPUTED** (same reason as FA1: the 15 keys' gas lives inside X30's drivers).
- Label for reading R: **I2-R KILLED** if G-R-SEP DOES NOT SEPARATE, or G-R-ETG or G-R-DSPH is EXCLUDED, on both
  footings. **I2-R PASSES THESE GATES** if G-R-SEP SEPARATES and G-R-ETG is ALLOWED and G-R-DSPH is ALLOWED on both
  footings. Otherwise MIXED (named by gate) or FOOTING-SPLIT.

## Inverse checks (reported, no label)
- VS1's slow-minus-fast +0.120 +- 0.047 (canonical) and VS4's +0.057 +- 0.037 (NO VERDICT) against the predicted
  contrast +0.199 when slow are on and fast are off.
- Rotating galaxies inside a group: SPARC's Ursa Major members (f_D = 4) are rotating, so off; their law rms
  against the other SPARC galaxies at g_b < a0, reported.

## Checks (a failed check means no clean label)
- **K0:** D = 0 reproduces the law exactly: the dSph pass list equals KT15's A0 rows for the same dwarfs and
  footings (same pass/fail per dwarf); the ETG offsets equal CFG323's primary values to 0.
- **K1:** the dSph sigma machinery passes KT15's C1 deep-MOND estimator check (3 %).
- **MUTATE (must bite):** the selector inverted (on where x > t_c) must turn G-R-SEP into DOES NOT SEPARATE on both
  footings. Separate `_MUTATE` outputs.
- **Rerun:** the result JSON from two runs must be byte-identical.

Compute: one thread, nice 19, < 1 GB, seconds to minutes. No downloads.
kappa = 1/2 FITTED; not theory closed.
