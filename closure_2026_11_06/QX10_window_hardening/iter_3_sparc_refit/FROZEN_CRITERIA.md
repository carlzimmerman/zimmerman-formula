# QX10 iter_3 frozen criteria: the flagship SPARC grade with the sector's galaxy profiles

Frozen before any iter_3 number. Kappa = 1/2 FITTED; not theory closed.

Pipeline: QX8 (closure_2026_11_06/QX8_sparc_exact_field/qx8.py, imported read-only: loader, mask, weights, per-galaxy
U refit on 0.30-1.20, pooled rms, line) and its committed exact-field corrections T(R, U) (parts/, read-only).
For each galaxy, footing and cell: the sector's hydrostatic profile M_d(<r) from iter_2 method A in the galaxy's own
sphericalised baryon potential M_b(<r) = running max of V_bar^2 r / G at the data radii, flat beyond R_last at
max(that, U L36 + 1.33 MHI). Computed at QX8's U nodes {0.30, 0.42, 0.60, 0.85, 1.20}, interpolated linearly in log U.
Then log10 g_pred = log10[nu((GB + g_d)/a0) (GB + g_d)] + T(R, U), with g_d = G M_d(<R)/R^2. Stated approximation: T
(the disc's exact-minus-law correction) is carried unchanged; for a spherical source the exact AQUAL field equals the
algebraic law.

Line (PAPER67's own, as QX8): rms <= 0.110 and 0.50 <= median U <= 0.80, per footing.
PASS if the line holds on both footings. FAIL otherwise. Reported: rms, median U, the change from QX8's exact-field
numbers, and the number of galaxies that keep sector mass.
Known answer K1: sector mass 0 reproduces QX8's exact-field rms and median U to 1e-4.
MUTATE: the sector forced into every galaxy (lambda_0 = 1e-3 Mpc) must FAIL the line on both footings.
