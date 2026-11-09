# HL3 AMENDMENT A1 (dated 2026-11-08; committed before any graded number exists, after the downloads and the loader read)

The frozen rule (FROZEN_CRITERIA.md, ef4595f390) is not changed. Four readings of its inputs are fixed here, after
reading the on-disk files and the downloaded sources and before hl3.py or hl3_grade.py exist.

1. **Footing values.** The criteria's header names the footings "canonical a0 1.2e-10, alt 1.1e-10". The record's
   footings, as every loader the criteria name carries them (QX5/QX7/NA2 `A0`, NA2's own frozen criteria), are
   canonical a0 = 9.3603e-11 m/s^2 (1/2 c sqrt(G rho_DE) at the record's rho_DE) and alt a0 = 1.1312e-10 m/s^2.
   KA3 can only reproduce NA2's 4.206 / 3.811 and -0.068 / +0.089 / +0.070 on those values, so HL3 grades on them.
   Both footings separately, never pooled, as frozen.
2. **X-COP sample.** Measured stellar-mass profiles (`_mstar.fits`) exist on disk for 7 of the 12 X-COP clusters
   (A85, A644, A1795, A2029, A2142, A2319, ZW1215); A1644, A2255, A3158, A3266, RXC1825 have gas and hydrostatic
   profiles only. NA2's bins (the KA3 numbers) are those 7. The hydrostatic leg's PRIMARY sample is therefore the 7
   with measured stars; "all 12" is reported as a bracket with the 5 star-less clusters given the 7-sample median
   M_star/M_gas(r/R500), flagged as imputed. A2319 with and without, as frozen. The "shared bin" rule (>= 6 clusters
   per leg) is unchanged and is met by 7.
3. **KA4 replay.** `hl2_results.json` carries HL2's frozen main read (n 53, g +0.031 +- 0.035); the "+0.031 +- 0.020,
   81 clusters" quoted in the criteria is HL2's post-result all-three-sources line (`hl2_post.out`, README). Both are
   replayed and printed; the consistency check uses the 81-cluster interval the criteria quote.
4. **Downloads.** VizieR holds neither J/ApJ/821/116 nor J/ApJ/794/136 ("Table or Catalog not found" at CfA; CDS
   timed out twice). The arXiv-source fallback the criteria name was used (FETCH_LOG.md). Umetsu+2016's source has
   per-cluster M500c (table3) and NFW parameters (table2) but the surface-mass-density profiles only as figures, so
   the D1 extension of the lensing leg beyond 600 kpc is NOT RUN as the criteria say, and the lane grades the on-disk
   14.3-600 kpc leg. CLASH R500 primary = from Umetsu's M500c with rho_c(z) in the convention Umetsu states (h 0.7,
   Omega_m 0.27, Omega_Lambda 0.73), the same background convention the X-COP R500 (Ettori 2019) uses; bracket =
   Donahue+2014's tabulated Chandra r500 (h70). Donahue's source has no per-radius gas profile table and no BCG table,
   so g_bar beyond 600 kpc is not needed and not built. Okabe & Smith 2016 has shear profiles only as figures: D3 NOT RUN.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
