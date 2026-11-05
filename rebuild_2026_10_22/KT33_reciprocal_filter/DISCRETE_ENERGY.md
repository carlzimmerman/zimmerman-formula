# Fixed-width reciprocal map and numerical realization

The authorized continuum construction is

    U[rho] = U_N[rho] + U_ph[S rho],
    Phi = N rho + S* Phi_ph[S rho].

S is a normalized Gaussian of the declared fixed width in each controlled
problem. The gradient points outward; matter acceleration is minus that
gradient. Nu is the unchanged simple function. This document specifies why
the finite Milky Way implementation needs more than another smoothing call.

## Volume-weighted energy

Let W be the diagonal cell-volume matrix, L the inherited Newton Laplacian,
N=4 pi L^-1 in G=a0=1 units, and G_r,G_theta the cell-gradient matrices.
The inherited Newton matrix is self-adjoint under W. Define

    u = G N S rho,
    A(u) = (nu(|u|)-1) u,
    H'(g) = g (nu(g)-1), H(0)=0,
    U_ph,h = -(1/(4 pi)) sum_i W_i H(|u_i|).

Direct variation, with the grid and S held fixed, gives

    Phi_ph,h = -L^-1 W^-1 (G_r^T W A_r + G_theta^T W A_theta),
    Phi_h = N rho + S* Phi_ph,h,
    S* = W^-1 S^T W.

Consequently this finite map has a symmetric volume-weighted response
Jacobian (away from non-differentiable zero-field configurations). The
Newtonian limit is exact because A=0 when nu=1. This construction also makes
the tangential response enter with its transpose; the older face-normal
QUMOND implementation does not do this exactly on a finite grid.

The Milky Way worker approximates the Gaussian by a finite even-Legendre
expansion on the axisymmetric reflected grid. If the symmetric weighted kernel
action is H_g and d=H_g 1, use

    S = H_g D^-1,  S* = D^-1 H_g,  D=diag(d).

This corrects quadrature mass loss column-wise, rather than assuming the
forward and reverse maps coincide after normalization. It gives exact
volume-weighted mass preservation and S*1=1 (additive potential gauge
preservation). Kernel shape, angular truncation and domain cutoff still need
convergence checks. These are numerical settings, not fitted physical widths.

## Boundary qualification

The centered gradients annihilate constants. Their negative adjoints include
the boundary terms of the finite-volume energy, so the integrated nonlinear
source is zero on the finite domain: the physical interior source is
accompanied by a compensating surface contribution. A spherical distant
surface shifts only the interior potential constant; nonspherical terms must
be tested by moving the boundary. Exact finite reciprocity is not by itself
proof of accuracy for the isolated continuum problem.

For the Gaussian, the numerical interior block is joined to identity outside
a large fixed radius. Its columns and adjoints include that prescription;
moving the cutoff tests its effect. The reported scores must identify the
finite implementation, spatial/angular/domain refinement, and differences
from the original source-only solver. A historical score cannot be transferred
to a new discretization without those checks.

## Independent periodic check

`validation/periodic_filter.py` implements the same continuum map using
Fourier Poisson solves and gradients on a periodic cube, independently of the
Milky Way implementation. It reproduces the prior audit's two-mode analytic
response coefficients, recovers the Newtonian and zero-width controls, and
tests net force on a nonspherical multi-mode source in a fixed external field
on four grids. The density is inversion-even; the external field breaks that
symmetry of the combined problem. This verifies those
finite periodic cases; it does not validate isolated observational boundaries.

## Width qualification

The width assigned by KT25 is retained for each baryon configuration and is
held fixed during source-variation checks. This is the requested controlled
diagnostic. It does not define one filter on an arbitrary unsplit universe,
nor does it provide the extra variations of a genuinely spatially
state-dependent width field.
