# Root review of the independent Solar and dwarf reductions

This is a separate analytic reading of the two subagents' formulas and code,
not a fresh numerical implementation or an interval error certificate.

The filtered Plummer density representation is correct:
integrating t^(3/2) exp[-t(1+r^2/b^2)]/(pi^(3/2)b^3) gives
3/(4 pi b^3)(1+r^2/b^2)^(-5/2), since Gamma(5/2)=3sqrt(pi)/4.
Its Gaussian variance is b^2/(2t), and convolution adds a^2. Differentiating
the resulting potential, rather than its spherical tensor entries, preserves
Cartesian isotropy. Mass-preserving compression at fixed a gives
dot v=−b^2/t; differentiating the enclosed Gaussian mass gives the recorded
dot H_tt and dot H_rr=(1-r^2/v)dot H_tt integrands. This verifies the
otherwise easy-to-miss a partial_a Hbar term in the homology identity.

The virial factor is also correct. E_ph=−int E_ex/(8 pi G), so
W_ph=−dE_ph/dlog(lambda)=int(A.delta g+B.delta Hbar)/(4 pi G).
Integration over azimuth and division by 3M gives 1/(6GM) in the recorded
radial/mu expression. Newtonian Plummer W/(3M)=pi GM/(32b). The external
linear subtraction vanishes after angular integration for a centered radial
compression but is properly retained in the integrand. The energy difference
control changes b while holding physical a fixed, which checks the relevant
variation. Positive trace-averaged variance is not an anisotropic equilibrium
or a line-of-sight fit; negative total virial is a stronger obstruction under
the explicitly stated lack of a confining surface stress.

For the Solar B term, let F=(3mu^2−1)/r^3. The STF zz Hessian of the inverse
Laplacian is −F/(4 pi), so source −partial_i partial_j(T B)_ij contributes
+int B_ij partial_i partial_j(TF)/(4 pi). If hr,ht are radial/tangential
eigenvalues of Hess(T(−1/r)), set t=ht−hr. Then
TF=t(3mu^2−1)/3, because trace subtraction removes the softened point-source
contact part. Contracting its Hessian with B=D diag(hr,ht,ht) yields
D[hr t''+ht(2t'/r−6t/r^2)](3mu^2−1)/3. Azimuthal integration gives the
recorded 1/6 prefactor. At a=0, hr=−2/r^3,ht=1/r^3,t=3/r^3; the bracket is
−108/r^8, recovering the older −18 integral(d/r^5)dlogr exactly.

For A, integrating by parts once gives int A.grad F/(4 pi).
Inserting the unfiltered point gradient and constant external field gives
(3/2)int[c{eta(3mu−5mu^3)+g(1−3mu^2)}]/r dmu dlogr,
matching the implemented formula. Angular-independent coefficient subtraction
has exactly zero contribution and improves cancellation. This confirms signs,
normalization and placement of the adjoint independently of the code's
zero-filter reproduction. It does not alone bound quadrature errors.

For a>0 the point-source high-gradient origin has z~x~r^-4 and the ordinary
large-x response asymptotic. One must use the exterior regular l=2 coefficient
and show the local nonharmonic l=2 part has vanishing tidal limit. The literal
Hessian inside a shrinking resolved source is a distinct limit. Solar's own
origin/adjoint audit records that remaining check and should be read with this
review before using its final quadrupole values.

Both diagnostics keep a uniform external auxiliary gradient and zero external
Hessian, matching the inherited comparison. They do not yet embed a source in
the full spatially varying Galactic potential. This scope matters particularly
for a curvature-dependent constitutive law and cannot be suppressed in a
physical interpretation of the finite tests.
