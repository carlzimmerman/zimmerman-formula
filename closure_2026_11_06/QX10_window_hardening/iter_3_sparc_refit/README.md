# QX10 iter_3: flagship SPARC grade with the sector's galaxy profiles. PASS for all four cells

Kappa = 1/2 FITTED; not theory closed. Criteria c1f0cadb7a. Script qx10_i3.py (parts, then grade). QX8's pipeline and
exact-field corrections T are imported read-only.

- K1 (zero sector) reproduces QX8's exact-field numbers: canonical 0.05605 @ 0.58, alt 0.05583 @ 0.52. PASS.
- Line rms <= 0.110 and median U 0.50-0.80:

| Cell | canonical rms @ U | alt rms @ U | Label |
|---|---|---|---|
| C1 | 0.0572 @ 0.58 | 0.0579 @ 0.51 | PASS |
| C2 | 0.0601 @ 0.58 | 0.0624 @ 0.51 | PASS |
| C3 | 0.0562 @ 0.58 | 0.0561 @ 0.52 | PASS |
| C4 | 0.0578 @ 0.58 | 0.0589 @ 0.51 | PASS |

- All 175 galaxies keep some sector mass. Little of it lies inside the rotation-curve radii, so the rotation curves
  move by at most 0.006 dex in rms.
- MUTATE (lambda_0 1 kpc, sector compact in every galaxy): rms 0.544 / 0.556 @ U 0.30 -> FAIL. BITES.
- Approximation: T (the disc's exact-minus-law correction) is carried unchanged; the sector is spherical.

The rotation curves cannot see the sector halo; galaxy lensing (iter_2 G6) can.
