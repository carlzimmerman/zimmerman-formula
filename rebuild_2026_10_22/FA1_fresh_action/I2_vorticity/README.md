# I2_vorticity: KILLED on both readings, both footings. As Phase 1 wrote it, the dust can't weigh in a cluster (the ICM's measured shear is 27-130x the threshold). The scale-free V/sigma reading fails the ellipticals: 13 SLUGGS galaxies it switches on sit at +0.094 dex against the +0.199 it predicts (Z -2.15)

Not blind. kappa = 1/2 FITTED. Footings never pooled. Not theory closed. Nothing here says the data favour the framework.
Adopts nothing. The cold sector stays retired. This lane grades where a selector would let a dust part weigh, using
baryon and kinematic data only, so it did not reopen the cold sector under the owner's 11-04 lift.

Order on record: `FROZEN_CRITERIA.md` (4603460516), committed alone before any script or number; then `i2_vorticity.py` →
`i2.out`, `i2_results.json`; MUTATE twin `i2_MUTATE.out`, `i2_results_MUTATE.json`.

Dust when the selector is on: FA1's minimum cluster-level amount, D = 1.5 x the law's mass. That is +0.398 dex in g and
+0.199 dex in a dispersion. The selector fixes where the dust weighs. The amount is the retired cold sector's.

## Reading P: Phase 1's action, F = exp(-omega^2/omega_*^2): KILLED AT THE CLUSTER GATE
The floor on the ICM's vorticity is half the Hitomi Perseus shear, about 150 km/s across 60 kpc (Hitomi 2016; recalled,
PROVISIONAL): omega_lo = 4.05e-17 s^-1.

| omega_* | canonical: omega_lo/omega_*, ln F | alt | SPARC min omega/omega_* (canonical) |
|---|---|---|---|
| a0/c | 130, -1.7e4 | 107, -1.2e4 | 219 |
| 2 a0/c = sqrt(G rho_DE) | 65, -4.2e3 | 54, -2.9e3 | 110 |
| 4 a0/c = sqrt(G rho_DE)/kappa | 32, -1.1e3 | 27, -720 | 55 |

- **G-P-CL: FAIL on both footings.** The dust can't weigh in a cluster with Perseus-like gas motions. It would weigh
  only if the ICM's vorticity were more than 27x below half the measured shear.
- G-P-SEP: SEPARATES, with f = 0.000. SPARC discs are off by a wide margin.
- Reported: a dSph with 1 km/s of mean rotation across 1 kpc sits at 21-104 omega_*. The MW disc at the Sun sits at
  580-2800. Both are off.

So the threshold Phase 1 named, omega_* ~ a0/c, turns the dust off almost everywhere matter has moved after shell
crossing, clusters included. Only FRW and the linear regime stay on.

## Reading R: scale-free F(V/sigma), on at x <= t_c = 0.5: KILLED BY THE ELLIPTICALS

| gate | canonical | alt |
|---|---|---|
| G-R-SEP, f_SP at Y 0.5 / 0.3 / 0.7 (sigma_HI 10 km/s) | 0.0035 / 0.0032 / 0.0038, **SEPARATES** | 0.0034 / 0.0031 / 0.0036, **SEPARATES** |
| G-R-ETG, on set (V/sigma_e <= 0.5, N 13) | +0.094 +- 0.049 vs +0.199, Z -2.15, **EXCLUDED** | +0.084 +- 0.049, Z -2.35, **EXCLUDED** |
| G-R-ETG, off set (N 3) | +0.085 +- 0.073 vs 0, Z +1.16 | +0.077, Z +1.05 |
| G-R-DSPH, KT15's 19 MW and M31 satellites, external field: law / dust-on passes | 12 / 12, **ALLOWED** | 12 / 12, **ALLOWED** |
| the same, isolated | 16 / 15 | 16 / 15 |
| **lane, reading R** | **I2-R KILLED** | **I2-R KILLED** |

- **Ellipticals.** The selector switches on 13 of CFG323's 16 SLUGGS galaxies, all those with ATLAS3D V/sigma_e <= 0.5,
  fast rotators included. Their outer-GC offsets average +0.09, well short of the +0.20 the dust would add. The four
  slow rotators alone sit at +0.182 (Z -0.26 against "on", alt +0.171, Z -0.43), as close to the prediction as the
  criteria said they would be. The 12 fast rotators would need to be off (+0.062; Z +1.31 off, Z -2.88 on). At the
  variant t_c = 0.25 (8 on, 8 off) the class reads ALLOWED, at Z -1.41 / -1.57. The frozen t_c is 0.5, so the label stands.
- **dSphs: the predicted extra is allowed.** 17 of 19 satellites have room for D >= 1.5 at 2 e_sigma (median D_max
  +7.1 canonical, +6.5 alt). Dust gains Sculptor and Leo II, and loses And II (D_max 0.12 / 0.02) and And VII
  (1.12 / 0.94). Draco, Ursa Minor, Sextans, Carina and CVn I fail either way under KT15's 1D external field: the law
  gives 1-2.5 km/s against 7-9.5. Counting all 34 MW and M31 satellites that have e_sigma: 17 -> 18 with the external
  field, 25 -> 26 isolated.
- G-R-BUL: WEIGHT ALLOWED AT GALAXIES. The selector can't tell gas from galaxies. G-Q2: INHERITS (the Sun's frame
  rotates, so the dust is off). Keys: NOT COMPUTED.

## Inverse checks (reported, no label)
- Slow minus fast against the predicted +0.199: VS1 +0.120 +- 0.047 (Z -1.68); VS4 +0.057 +- 0.037 (Z -3.84; VS4 is NO
  VERDICT). The record's slow-rotator excess points the right way, but it is smaller than this selector needs, and VS1/VS2
  couldn't separate it from being central.
- SPARC's Ursa Major members are rotating galaxies in a group, so the selector is off there. Their g_b < a0 law residual:
  canonical mean -0.007, rms 0.119 (n 286), against +0.004 / 0.207 for the rest. Alt: -0.041 / 0.127 against -0.030 /
  0.211. This is consistent with "off", but it is not a lever: a group this poor needs little dust at disc radii anyway.

## Checks
- K0: D = 0 gives the law to 0. The ETG offsets equal CFG323's primary to 0. The dSph pass lists equal KT15's A0 rows,
  dwarf by dwarf, in all four footing x field cases.
- K1: KT15's deep-MOND estimator check, rel 0.0016.
- MUTATE (selector inverted): G-R-SEP reads DOES NOT SEPARATE on both footings, and G-P-SEP does too. The gate bites.
- Rerun: `i2_results.json` is byte-identical across two runs.
- Compute: 47 MB RSS, under 1 s, one thread.

## What is not done
- Reading R isn't a field-level action. V/sigma is a property of a system, and the one local version (reading P) fails.
- t_c and the ICM shear are literature values recalled, not fetched (PROVISIONAL). The ETG on/off split uses inner
  (R_e) kinematics, while the offsets are measured at R > R_e.
- SLACS (CFG713 wants an extra ~0.36 of the mass inside theta_E, about 0.56x the law's) has no rotation class per lens,
  so it isn't graded. ATLAS3D JAM masses inside R_e aren't on disk.
- The 15 shear keys and a Bullet weight model are not computed.
- X22's capture wall and X57's mu-pincer and Theorem G still stand for any successor.

kappa = 1/2 FITTED; not theory closed.
