# Sharp kinetic edge regularity — frozen before calculation

Audit the formation implication of CFG620's hard-edge stationary target,
without duplicating its ongoing repaired-kernel rerun CFG626. Assume spherical
Newtonian real-mass potential with nonnegative enclosed mass, finite outer
radius R, and g(R)>0 finite. Orbits are entirely confined to r<=R. A bounded
phase-space density f<=fmax must have density tending to zero at R, even with
arbitrary anisotropy. Prove using the allowed velocity volume. This does not
exclude singular distributions, initially cold sheets, coarse-grained states,
collisions, or other boundary conditions, and is not a full candidate-B failure.

Set A=1-r^2/R^2 and D=Phi(R)-Phi(r)>0. Verify the necessary velocity ellipsoid
vr^2+A vt^2<=2D and its volume (4pi/3)(2D)^(3/2)/A. At the edge this scales
as sqrt(R-r); report the exact leading coefficient. For nonnegative mass,
show the accessible region is bounded using L^2<=G M(R)R.

Construct an explicit stationary singular counterexample
f=C/sqrt(E_R(L)-E), E_R=Phi(R)+L^2/(2R^2), on confined orbits (and zero
otherwise). Compute density exactly from its velocity integral and verify its
finite nonzero edge limit. The amplitude C is only a normalization of this
mathematical counterexample, not a proposed free constant or kinetic model.
Use it to prevent overclaiming that every hard edge is impossible.

Controls: constant f velocity integral; singular f integral; density edge
limits for a Kepler potential G M=R=1 at gaps 1e-2,1e-4,1e-6; independent
quadrature using w=sqrt(2D) sin(theta). Analytic-vs-quadrature relative 1e-10;
limiting ratios at smallest gap within 1e-4. MUTATE omit the transverse
Jacobian 1/A (must miss singular density by >1% at r=.9); MUTATE replace
vanishing radial phase volume by constant (must disagree with limit).
Check the finite-entropy integral near the velocity boundary, not an assertion
that this particular f is CFG620's entropy maximizer.

No astrophysical fits, PM jobs or inferred formation times. Kernel-independent
conditional result: relevant when either footing's target has a positive
one-sided density at its imposed edge. Finite-grid success cannot settle the
continuum regularity question. Bounded smooth phase-flow conservation excludes
formation from bounded initial f in finite time; primordial singular f remains
an explicit loophole. One thread, CPU10s/wall20s, memory <150MB. Preserve failures.
Commit criteria alone before running. Kappa fitted; no global closure claim.
