# EFN1 amendment A1 (2026-11-10): the razor-thin sheet's two plane rows are held static; committed alone, before any outcome number

Post hoc with respect to the criteria (98364c8d20). Committed before any route-D run, route-W eigenvalue or outcome.

## What was seen first (setup numbers only; canonical expo log M_b 9.4, g_e = 0.1 a0)

- My operators reproduce SCS2's phantom() N0 to 1.7e-11 (relative) and SCS2's cell gradients to 1e-10; my route-L maximum at
  R0 gives an e-folding time of 0.97751 Gyr, SCS3's R0 value (0.97751). The exact Jacobian of the discrete P flux agrees with
  finite differences (error falling as the step squared).
- **The stiffness.** In the dynamic region r >= 0.4 r_e, the largest local rate omega_max (|4 pi G D.P u (2+u)|^1/2) sits in the
  two plane rows of the razor-thin sheet, where D.P is positive and large: the disc's exponential tail still carries a surface
  density at 6-12 R_d, and a plane cell's D.P scales as 1/(cell thickness). Local rate^2 over Gamma_ref^2 in the plane rows at
  R3: -15700 at 0.4 r_e, -490 at 0.6 r_e, -10 at 0.8 r_e (negative = a stable oscillation); in the neighbouring off-plane
  cells: -70, -14, -2.7. The plane maximum of |rate^2| grows with resolution: 815 (R0), 1909 (R1), 4551 (R2), 9699 (R3)
  times Gamma_ref^2; off-plane it is 50-55 at every grid.
- So the frozen dt rule (0.25/omega_max) gives omega_max/Gamma_ref of about 127 at R3 and more at R4: about 7,000-9,000
  RK4 steps per run (R3 about 9 min, R4 about 30 min per run, from measured stage times of 0.020 s at R3 and 0.050 s at R4).
  The graded set (12 backgrounds at R3 and R4, plus dt halving) would take about 11 hours, above the brief's 3-hour line.
- The frozen seed's amplitude a(0) at eps = 1e-4 was 9.3e-4 at R3 and 1.9e-3 at R4: its maximum sits in a plane cell (the
  seed's n = -div(N0 xi) picks up the sheet's large N0).
- SCS3 (criteria 2c) already excluded the sheet's plane cells from route L because their D.P is not a convergent quantity.

## The change (reading A1)

- The razor-thin sheet's two plane rows (the cells SCS3's sheet_mask marks; expo and Kuzmin backgrounds alike) are held
  static like the region r < r_in: pi = n = 0 there, and the faces between them and the off-plane cells carry no clock flux.
  phi and s are still solved on the whole grid. The dynamic region, a(t)'s normalisation |min N0| and the seed all refer to
  the off-plane cells with r >= 0.4 r_e.
- Everything else (equations, dt rule, seed, stop lines, labels, known answers, mutations, routes) is unchanged. The same
  exclusion applies to the isolated twins of KA-c.
- What this assumes: the plane acts as a wall for the clock flow at r >= 0.4 r_e. SCS3's maximum is at theta 137-142 degrees,
  about 50 degrees from the plane, at 0.85-0.91 r_e; the far-field band near the plane grows at about 0.3 Gamma_ref^2 or less
  at r >= 1.5 r_e on the off-plane cells.

## Frozen reading (reported beside, partly)

The frozen reading (plane rows dynamic) is run on R3 and R4 for two backgrounds (canonical expo 9.4 and alt expo 9.4) with
the frozen dt rule if the A1 runs leave time within the brief's 3-hour line; its labels are reported beside A1's for those
two. For the other ten the frozen reading is NOT COMPUTED (cost), so their frozen-reading label is NO VERDICT. A1's reading is
reported after the frozen one, as the record's rule asks.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
