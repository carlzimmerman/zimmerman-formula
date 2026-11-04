# FN3 amendment A1, post-result: K1 failed as frozen

Written after K1 ran (`fn3_k1.out`, `fn3_k1.json`). It changes no frozen label, line or tolerance. kappa = 1/2 FITTED. Not theory closed.

## What happened
K1 failed on every listed convention (18 of 18). The best variant puts 1.4 % of primary galaxies within 3 % rms, against the frozen 90 %. Median rms is 0.45-0.54. By the frozen rule, **the Stage 0 forecast reads NOT EVALUABLE.** It is not run.

## What the failure shows, read after the fact
- **The engine itself passes its own known answers.** The razor-thin MGE limit matches Freeman's exponential disc to 0.03 %. The spherical limit is exact. The DC14 halo rebuilt from the released V_vir, concentration and X matches the released alpha, beta, gamma, r_s, R_vir and log M_vir (rho_s within 0.3 % for ID0003 and ID0011).
- **The released curve is not the quantity K1 compared.** For well-behaved galaxies it sits 5-10 % below the intrinsic v_perp inside about 2 R_e and matches outside (ID0003: 113.5 against 123.8 km/s at 7 kpc; 154.1 against 154.3 at 19 kpc). That is the pattern of a flux-weighted slit extraction through a thick model disc. The file's own `flux_slit` column points the same way.
- **Where pressure exceeds gravity, the survey's code keeps a speed.** The worst galaxies' released curves fall and then rise again (ID1086: 16.6, 12.4, 7.3, then 62.1 km/s). That fits sqrt(|v_c^2 - v_AD^2|), which wasn't on the frozen list.
- **Marginal medians don't make the median curve.** V_vir, concentration and X are strongly degenerate (ID0003: V_vir 160.6, 95 % range 138-195). The released v22 is tight (149.4 +- 1.6), so the curve built from each parameter's own median needn't match it.

## What changes and what doesn't
- **No change to Stage 1's grading.** It rests on K2 (planted recovery) and K3 (the DC14 model refit on real cutouts recovers the survey's v22 within 5 % and inclination within 3 deg). Both stay as frozen. K3 compares two fits to the same data, so the slit-extraction question doesn't arise there.
- **Added diagnostic, no gate:** K1b builds the survey's DC14 model as a 3D cube without PSF and extracts a major-axis slit (flux-weighted first moment, deprojected by sin i), using sqrt(|v_c^2 - v_AD^2|). It is reported only. It cannot change the Stage 0 label.
- **For the law refit (Stage 1), pressure support keeps the frozen readings R0-R2.** Where v_AD^2 > v_c^2 the law model sets v_perp = 0, as the frozen engine does. The survey's sqrt(|.|) handling is reported as a row, not adopted.
