# SCS3 AMENDMENT A2 (post hoc, AFTER the frozen and A1 PL map runs at R0-R1; committed alone, before any A2 number)

TEST lane. Adopts nothing. kappa = 1/2 FITTED; not theory closed.

**The frozen and A1 readings stay as they are and are reported first.** A2 adds a third reading for the in-plane (PL)
family and its thick twin only. The axial family is untouched.

**What changes in the A2 reading (PL and THICK_PL only; everything else as A1).**
1. **The polar-axis row is excluded.** In the 3D grids the cells of the first theta row (the cells touching the grid's
   polar axis, which is the disc's axis) are excluded from route L, route L-tilde and the region, as the sheet cells are.
   Route 2's Rayleigh certificate and pencil are unchanged.
2. **A third resolution, by an iterative solver if needed.** The frozen probe stands: one PL R2 solve (base 108, 36, 36)
   by the frozen direct solver, killed at 4 GB RSS. If it stays below 4 GB, PL R2 is run as frozen. If not, PL R2 is solved
   by the same equations, grid, Picard scheme and residual line (1e-8), with each linear step solved by conjugate gradients
   preconditioned by an incomplete LU (scipy spilu) to a relative tolerance of 1e-11. The solver swap is graded first: the
   iterative solver re-solves PL R1 for two backgrounds (expo 9.4 at 0.1 a0 and Kuzmin 10.9 at 0.01 a0, canonical), and its
   Gamma_L^2 (A2 reading) must equal the direct solve's to 1e-3 relative and its min D.P to 1e-3; otherwise R2 is not used.
   With R0-R2 the three-grid rule of section 3 applies to PL; otherwise the two-grid rule as frozen.
3. Labels, lines, known answers and MUTATE arms as frozen; KA4 is read as before.

**Why, and what was seen first (post hoc).**
- In the frozen and A1 PL maps (R0, R1), route L's maximum sits on all 16 PL backgrounds in the first theta row and the
  first phi cell (theta 5.4 / 3.7 deg, phi 5.6 / 3.7 deg at R0 / R1), at 1.3-1.6 r_e, with e-folding times 0.36-30.8 Gyr at
  R0 and 0.28-23.7 Gyr at R1: Gamma_L^2 rises by about 70 % per refinement there. The axial family has its maximum at the
  null's flank instead (0.82-1.05 r_e).
- Those cells sit where the spherical grid's polar axis meets the y = 0 mirror plane: wedge cells whose phi faces have
  vanishing width, the finite-volume scheme's coordinate singularity. The far-field closed form (Lean: farfield_plane_rate)
  gives the band's rate at 1.4-1.6 r_e three to four times slower than those cells show, so they are not the band.
- A diagnostic on two backgrounds (canonical expo 9.4 at 0.1 a0; canonical Kuzmin 10.9 at 0.1 a0) excluding the first theta
  row put the maximum at the null's flank, 0.88-1.03 r_e, theta 51-57 deg, phi 141-169 deg (the null is on the x axis,
  theta about 89 deg, phi about 175 deg, at 0.82-0.94 r_e), with e-folding 0.98 -> 0.93 Gyr and 2.24 -> 2.16 Gyr from R0 to
  R1, close to the axial family's same masses and field (0.85-0.98 and 2.0-2.26 Gyr). Excluding two rows gave the same cells.
- A1's PL map run used 0.17 GB (cached solves); the frozen PL R1 solves peaked at 2.6 GB. No PL R2 solve has been run.
- A two-grid estimate with the AX family's order on those two diagnostics would give errors of roughly 25-35 %, above the
  frozen 25 % line: that is the reason for item 2.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
