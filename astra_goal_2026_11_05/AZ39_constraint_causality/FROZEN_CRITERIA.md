# AZ39 — constraint causality, lane 5(e)

Frozen before computation. Base016cbd9e89. Kappa = 1/2 FITTED;
not theory closed. C5's frozen principal matrix and C8's causality
argument are inputs to audit, not established physical response functions.

## Full target and labels

PASS requires a constrained initial-value formulation and physical retarded
response on the adopted backgrounds, including nonzero khronon charge and
the switch interface. FAIL requires a conserved-source perturbation of an
on-shell background with observable curvature outside its causal domain,
or another explicit physical causality counterexample. A spatial inverse,
a non-real root in a different slicing, or an arbitrary time-dependent
Newtonian density by itself is neither. A conditional GR branch is
insufficient for either full label: report NO VERDICT.

## Bounded calculation

Verify the exact conditional P=0,Q=1 geodesic branch: extra-action value
and first variation vanish, including both one-sided derivatives of the
switched term at zero. Locally a unit geodesic clock can be chosen before
its congruence develops caustics. This does not select the physical branch.

On its Minkowski linearization, use eta=(-,+,+,+), Box=-dt²+Laplacian,
G_linear=8*pi*G*T. Two independently conserved signed external probes:

1. T_mn=(d_m d_n-eta_mn Box)f, with compact smooth f. Verify conservation,
the linearized Einstein tensor of h_mn=-16*pi*G*d_m d_n u
-8*pi*G*eta_mn*f where Box u=f, and cancellation of every pure-Hessian
contribution to Riemann. Curvature from f is local. This special source
is nonradiating outside its support; do not claim generic cancellation
of all radiation. Known answer: pure gauge has all256 Riemann entries zero.

2. A planar TT stress T12=T21=b(t)c(z), other entries zero, with
b=256*t^4*(1-t)^4 on[0,1], c=(1-z²)^4 on[-1,1], zero elsewhere.
It is conserved, signed, infinitely extended in x,y, and is a linear
probe rather than a positive-energy isolated material body. Normalize
8*pi*G=1 and use zero incoming data. Then
h12=int_0^t ds int_[z-t+s,z+t-s] dq b(s)c(q),
R0102=-h12,tt/2. At z=3 evaluate times1/4,1/2,3/2,9/4,5/2,3,7/2,9/2,11/2.
The first three lie outside the source's causal future; the middle times
include a nonzero tidal signal. Verify the exact polynomial integrals,
and independent split Gauss-Legendre16/32 quadratures. Split at source
support edges; max absolute discrepancy <=1e-10 in these dimensionless
units, chosen above double-precision polynomial quadrature roundoff.
Outside-cone curvature must be <=1e-12; at least one inside-cone value
must exceed1e-6 to exclude an identically zero test.

## Mutation and scope

MUTATE replaces the TT wave equation by h12,zz=-2*T12 at each time,
using its symmetric one-dimensional Green function
h12=-int |z-q| b(t)c(q)dq. Grade the same outside-cone tidal test; it
must fail. This is a deliberately altered response operator, not a
demonstration that v3s has that operator. Compare exact and16/32 numerical
integrals also for the mutant. Scalar identities remain unchanged.

Report canonical a0=9.3603e-11 and alt1.1312e-10 separately. The GR
branch is exactly independent of a0 and Lstar; there are no fitted
response parameters or observational exclusions here. No PDE refinement
claim is made: numerical outputs are quadratures with convergence pairs.
Keep full charged-background causality NO VERDICT unless the full target
is actually resolved. C8's unconditional instantaneous-force conclusion
does not follow from its stated elliptic argument alone.
