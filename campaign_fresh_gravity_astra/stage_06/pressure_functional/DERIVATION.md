# PF1: finite pressure measurements and point derivatives

Candidate exact lemma, 2026-09-27. Parent: stage-five density-shape gap,
FGF-020 reviewed moment non-identification, and released FGF-019. This is a
new spatial-response premise, not a rerun of the two-moment calculation.
No literature mechanism or historical novelty assertion is used.

## Declared observation model

Use dimensionless radius x=r/L_* in a finite interval and dimensionless pressure
p=P_e/P_*. The finite measurements are linear functionals

    y_i[p] = integral K_i(x) p(x) dx,  i=1,...,m.

The kernels incorporate the declared spherical projection, beam, annular bins
and fixed mask, where these really act linearly on pressure. This lemma assumes
bounded kernels on the perturbation supports; raw line-of-sight tangent kernels
need a separate check. No actual instrument kernel is authenticated here.
Unknown nonlinear temperature/relativistic response is outside the premise.

Let x0 be an interior point, and let p0 be a smooth nonnegative profile which
has a positive lower bound on a neighborhood of x0 and on a compact set J
separated from x0. Assume the restrictions K_i|J are linearly independent as
functionals on smooth compactly supported functions in J. A dependent complete
measurement list can be reduced first; independence just near x0 is insufficient.

Then one can choose m smooth functions h_j supported in J for which
A_ij=integral K_i h_j is invertible. To see this, if the measurement vectors
of all test functions failed to span R^m, a nonzero annihilating row vector
would give a vanishing combination of the functionals on J, contradicting
the assumption. The h_j need not be positive individually.

## Exact null perturbation

Choose a smooth compactly supported function phi on (-1,1) with phi'(0)=1,
0<alpha<1, and a fixed finite coefficient b != 0. For delta small enough that
the local support misses J, set

    u_delta(x) = b delta^alpha phi((x-x0)/delta),
    v_i(delta) = integral K_i u_delta,
    c(delta) = A^(-1) v(delta),
    p_delta = p0 + u_delta - sum_j c_j(delta) h_j.

Exactly, y[p_delta]=y[p0]. Bounded kernels give
|v_i| <= |b| ||K_i||_infinity ||phi||_1 delta^(alpha+1).
The fixed inverse A and fixed h_j therefore make the compensation uniformly
O(delta^(alpha+1)); the local perturbation is O(delta^alpha). Hence p_delta
remains nonnegative for all sufficiently small delta and is strictly positive
where it was changed. Every p_delta is smooth. Because h_j vanish near x0,

    p_delta'(x0) - p0'(x0) = b delta^(alpha-1).

This tends to either sign of infinity with b's sign while the full pressure
profile converges uniformly to p0 and every finite measurement stays exactly
fixed. Thus these measurements cannot uniformly bound the point derivative
over this positive smooth profile class. This is an exact conditional proof,
not a floating-point rank assertion or a fit to the actual cluster map.

Even without the compensation-rank hypothesis, the uncorrected u_delta has
measurement changes O(delta^(alpha+1)). Any positive fixed measurement-error
box around y[p0] eventually contains the perturbed observations while the
point derivative diverges. This second statement concerns finite tolerances,
not exact equality, and does not require a covariance model.

## Physical and framework scope

Restore pressure gradients by P_* / L_*. Electron-to-total pressure conversion,
composition, density and instrumental response must be supplied separately.
For a specified positive density, radial hydrostatic balance would require
P_tot'=-rho F(B;a), B=G(M_gas+M_star)/r^2. Here F is separately Q, RAR or the
registered M law, never a replacement Newtonian missing-mass calculation.
Carry a=9.3619e-11 or 1.1279e-10 m/s^2 on the constant-vacuum branch; the
distinct history branch uses a=a0 E(z). This dimensionless observation lemma
does not select a, F, G or a gravitational action and applies to either footing
only through this explicit force/pressure bridge.

Neither the constructed pair nor its unbounded point derivative is asserted
to obey global hydrostatic balance, monotone pressure, a bounded second
derivative, thermal equilibrium, the filtered-MONO field equation, a boundary
flux prescription or the same X-ray counts. These are additional restrictions
that can remove this family. The theorem cannot exclude the user's framework.

## Discriminating next test

FGF-019 must report both its finite-basis target rank and what changes when
outer/basis modes are admitted. A full-rank finite model alone cannot refute
this conditional continuum construction. Audit the actual response kernels
and compensation rank before applying exact non-identification to that map.
If a justified regularity bound is supplied, replace the unbounded point
derivative problem with a finite-resolution gradient or a certified derivative
bound. The source of that regularity bound must be physical or observational,
not merely the chosen number of bins.
