# QX32 frozen criteria (door C, narrowed): can cluster asphericity in the law's own field fake the hot/cold step?

Frozen before any QX32 number. Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Rules: SWARM_BRIEF.md.

## Scope (what is new against the record)

QX30 audited the cluster data products and labelled them ROBUST: clumping, ICL, deprojection, IMF, beta, mass-model columns,
native D_A. QX2 graded the law with the spherical algebraic form. Neither tested this: in the law's NONLINEAR field, the boost
of an aspherical cluster is not the spherical law applied to its enclosed mass, while a spherical hydrostatic analysis measures
the shell-averaged radial field. QX32 computes that bias.

## Method (frozen)

- Field: the QUMOND form of the a0 law, g = curl-free part of g_law-interpolated nu(|g_N|/a0) g_N, solved by FFT on a 3D grid.
  QUMOND stands in for the action's AQUAL-form static equation (v3s/AC2q). This is stated; a QUMOND/AQUAL difference in this
  bias is second order and NOT evaluated.
- Clusters: all 7 X-COP. The spherical baryon density rho_b(r) comes from the measured M_b(<r) (gas + stars, iter_5's
  profile; constant beyond the last joint radius, i.e. truncated there).
- Shapes: volume-preserving homoeoids rho(m) with m^2 = q^(2/3)(x^2 + y^2) + q^(-4/3) z^2 (oblate) and the prolate swap,
  for q in {0.5, 0.7}, plus the spherical q = 1 reference.
- Observable: the spherical-HSE mass the cluster appears to have, M_app(r) = r^2 <g_r>_shell / G at r = 0.1, 0.2, 0.3, 0.5,
  0.7 R500 (the X-COP grading radii). Bias: Delta(r) = log10[M_app,q(r) / M_app,1(r)], the aspherical minus spherical solve on
  the same grid, so grid and box errors cancel to first order.
- Grid: 256^3, box side 6 Mpc (cell 23 kpc), periodic FFT Poisson with the mean removed. Both footings.

## Label (needed to explain the step: +0.30 to +0.47 dex)

- **EXPLAINS:** the class-mean Delta >= +0.30 at some realistic q (at least one shape orientation).
- **PARTIAL:** |mean Delta| >= 0.10.
- **NEGLIGIBLE:** |mean Delta| < 0.10 for every shape.
- The sign is reported. A positive Delta means the spherical analysis over-reads the mass relative to the spherical law.

## Controls

- K1: q = 1 against the algebraic law, M_app,1 vs M_law(M_b(<r)): agreement within 0.03 dex at 0.2-0.7 R500 sets the grid error
  scale (0.1 R500 reported; it is near 5 cells).
- K2 (Gauss): with nu = 1 (Newtonian), Delta = 0 to within the K1 error scale for every q.
- MUTATE (bite): replacing the field by nu^2 g_N (an over-boosted phantom) must move M_app,1 by more than 0.1 dex at 0.5 R500.
- Memory/compute: float32/complex64, under 1 GB RSS, 1 thread, nice 15.

## Amendment A1 (2026-11-07, before any QX32 number)

A systematics re-grade of the X-COP residue (DIRECTION 11-07 item 4). The new input against QX30 is the cluster's 3D shape in
the law's nonlinear field. QX30's bounds are all spherical.

## Amendment A2 (2026-11-07, before any QX32 number): the bias is taken against each shape's own sphere-enclosed baryons

A volume-preserving homoeoid's baryon mass inside a sphere of radius r differs from the spherical model's M_b(<r). So the
ratio M_app,q / M_app,1 would show a "bias" even in Newtonian gravity, and K2 could never pass. The observable is therefore
the one the X-COP grade uses: the spherical law applied to the sphere-enclosed baryons of the SAME shape.
  Delta_q(r) = log10[ M_app,q(r) / M_law(M_b,q(<r sphere)) ] - log10[ M_app,1(r) / M_law(M_b,1(<r sphere)) ].
M_b,q(<r) is summed over the same grid cells. K2 (nu = 1) then gives Delta = 0 by Gauss, and the labels are unchanged.
