# SV4: inputs not on disk (nothing was downloaded)

1. **Malin 1 HI velocity-dispersion profile** sigma_HI(R) (or the paper's stated asymmetric-drift term), Lelli,
   Fraternali & Sancisi 2010 (arXiv:1003.1312) text/tables. Needed for iter_1 (pressure support) on Malin 1, now
   NOT EVALUABLE. Scale of the need (iter_1 output): the outer rings would need AD2 of 1.3-2.4e4 (km/s)^2, i.e.
   sigma ~ 65-90 km/s at a slope factor of 3, against HI dispersions of order 10 km/s in discs; and AD would raise V_c
   at 37.5 kpc too, where the canonical law already sits below the data. Unlikely to change the label.
2. **Harmonic decomposition / residual velocity fields** (bisymmetric and radial non-circular amplitudes) for AGC
   114905 (Mancera Pina+2022/2024 cubes or tables) and Malin 1 (Lelli+2010). Needed for iter_2 (c), now NOT
   EVALUABLE. AGC 114905 would need coherent LOS non-circular amplitudes of 3-20 km/s rising outward, 1.6-3.9x
   sigma_HI in the outer three rings.
3. **Malin 1 redshift and the optical analysis distance** from the paper (z = 0.0826 used from memory for the
   (1+z)^2 bracket in iter_4). A bar length for Malin 1 (iter_4 used a generous 10 kpc bound).
4. **An all-sky, mass-complete catalogue** (e.g. 2MRS/2MPZ all-sky with K-band masses) would replace iter_3's
   ALFALFA-footprint fill and the F_c = 10 allowance, and tighten the MOND-reading bound (currently NOT EVALUABLE).
