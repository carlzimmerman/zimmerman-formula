# Finite-frequency radial variational diagnostic

Continue from the four frozen shell solutions, not a new parameter scan.
Freeze before calculation. Perturb B,p with Dirichlet values at both shell
ends. These boundary conditions define a diagnostic radial box and differ
from the original natural p boundary; no claim about the physical exterior.
The lapse is an algebraic cell variable with no imposed endpoint value.
The shift boundary term vanishes because delta Bdot=0 at the ends.

Integrate the N' terms in STATIC_RESULT.md by parts instead, giving

 Lr=M^2 N[B-1/B+2r B'/B^2]+NB r^2[X-V-W]
          -N(r^2 p)'/K-gamma N r^2(p'+2p/r)^2/(2K^2 B).

Derive its Hessian in (B,N,p,B',p') symbolically from the actual W.
Linear finite elements for delta B,delta p, cellwise-constant lapse;
midpoint action quadrature. Eliminate the coupled (N,p) constraint matrix
together; do not invert the local N diagonal across zeros of T. Use the
consistent linear-element mass matrix with midpoint Mt from RADIAL_RESULT.
Generalized frequencies solve -H_static_reduced v=omega^2 Mtime v.

Use40,80,160 logarithmic cells per original case. Evaluate the fixed201-point
saved background interpolant with cubic splines; obtain derivative jets
from its field equations. This is a fixed-interpolant diagnostic; the
original BVP mesh study is separate. For each rung record low5 eigenvalues,
constraint solve backward residual, matrix symmetry and scaled constraint
condition estimate. Record discrete background action-gradient residuals
rather than assuming the interpolated profile exactly extremizes every mesh.

Criterion for a finite diagnostic PASS: positive low5 on all rungs and last
two rungs agree to2% relative on the low3; solve/eigen backward residuals
<=1e-8 and estimated scaled constraint condition<1e14. A robust negative
mode is a restricted instability result; failed convergence is NO VERDICT.
Do not loosen criteria. A positive finite low5 spectrum is not positivity
of all continuum modes. High-k positivity has its separate derivation.

Known-answer control: consistent FE Dirichlet -d^2/dr^2 on [0,1] must
approach pi^2 on40,80,160 uniform cells to1e-3 relative by160. Its sign
reversal must produce a negative eigenvalue. No underlying physical sign
may be flipped to obtain a pass.

Single-core bounded run120seconds; less than1GB. Retain failure records.
No physical data, no coefficient derivation, no angular modes or cosmic match.
