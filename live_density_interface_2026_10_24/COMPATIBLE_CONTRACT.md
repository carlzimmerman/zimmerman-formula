# LD-15: repair a load-bearing discretization mismatch before interpretation

The final plot revealed grid-scale empty/full density oscillations. Earlier
gravity used point-shell self energy while W used midpoint enclosed mass and
cell volume. These are separately convergent quadratures but need not have
compatible high-frequency curvature. Do not interpret the density comb as
physical fragmentation. Earlier finite stationary curves remain records,
not a continuum matter-equilibrium proof.

Use the common field quadrature for both energies:
E_grav=-sum vol(.5 g_dark²+g_b g_dark)-M²/(2R)-M/sqrt(R²+b²),
where g_dark=A m and the last two terms are exact exterior self/cross tails.
W uses the same A and vol. In pure cold T, the interior material Hessian is
A^T diag(vol[W''(u)-1]) A, positive for 0<u<1. The exterior W-minus-gravity
tail is also convex. This removes the spurious bulk density curvature without
adding a new physical force, stiffness, pressure or fitted law prior.

Check joint energy derivative and positive cold-bulk Hessian, optimize all-T
controls at n64/128, then redo the charge-free beta20 K3 core from the old
front and law-independent seed at n96. Retain intermediate checkpoints.
Broad law and actual density, not merely core acceleration, are mandatory.
Any earlier interpretation of depletion remains provisional until this test.
