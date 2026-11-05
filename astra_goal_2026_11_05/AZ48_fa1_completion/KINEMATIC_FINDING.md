# FAIL — a projected velocity gradient does not establish a vorticity floor

This audits one load-bearing inference in FA1/I2-P, not the actual cluster
flow or the whole selector. The original record is untouched. Retired
sector, adopts nothing; kappa = 1/2 FITTED; not theory closed.

Let z be the line of sight and x a sky coordinate. For any constant alpha,
consider the smooth local velocity field

\[
\mathbf v_\alpha(x,y,z)=(\alpha\gamma z,0,\gamma x).
\]

At z=0 all these fields have the identical velocity map (0,0,gamma x),
including the same nonzero line-of-sight gradient. Their curls are

\[
\nabla\times\mathbf v_\alpha=(0,(\alpha-1)\gamma,0).
\]

Thus alpha=1 has zero vorticity despite the observed gradient. Alpha=-1
has rigid rotation and the same projected observations. No strictly
positive lower bound on the curl follows from that projected gradient
alone. Taking half the gradient does not repair the implication. Changing
whether "vorticity" denotes curl or half-curl cannot repair a zero witness.

The statement also has an exact relativistic local witness. In Minkowski
coordinates (x0=ct,x,y,z), set a=gamma/c and

\[
T=x^0-a xz,\qquad
N=[1-a^2(x^2+z^2)]^{-1/2},\qquad u_\mu=-N\partial_\mu T.
\]

In the finite region a^2(x^2+z^2)<1, this is a unit timelike four-velocity
with ordinary velocity (gamma z,0,gamma x). Its projected vorticity vanishes
exactly. To see this without a numerical solver, differentiate u: its
antisymmetric derivative contains only products of a derivative of N and
a derivative of T, because the mixed second derivatives of T commute.
The projector P_mu^alpha=delta_mu^alpha+u_mu u^alpha annihilates dT, which
is proportional to u. Projecting both indices therefore gives zero.
covariant_witness.py verifies normalization, velocity and all16 projected
components symbolically; a rigid-rotation control gives a nonzero tensor.
All4 checks pass. This is a kinematic witness, not a claimed solution of
the full gravity and gas equations. Additional dynamical assumptions would
need to be stated and tested to use them as observational constraints.

The frozen kinematic computation passes23/23 checks, including independent
curl components, oriented circulation and central differences at1kpc and
0.5kpc. Scientific output repeats exactly. The separate mutation replaces
the antisymmetric gradient with the full gradient norm: it fails the
zero-strain-vorticity check, counterexample recognition and the conditional
irrotational activation checks on both footings (19/23; expected exit1).

Using I2's recalled150km/s over60kpc only as an illustrative normalization,
the old assumed half-gradient suppresses its exponential selector. The
equally projected irrotational witness instead has log F=0 for all three
omega-star variants on both footings. This does not show that the actual
cluster is irrotational or that I2 passes its observational gates. It shows
that the quoted gradient alone cannot support the old G-P-CL exclusion.
The separate I2-R elliptical result and other action/galaxy constraints
are not re-audited or overturned here. The Hitomi value itself was not
authenticated by this computation and remains a recalled input.

For the requested fifteen I2 selector keys, do not substitute this same
single cluster's gradient for the per-system velocity field. Those inputs
and the native shear/gas reconstruction remain pending. No rescue, adoption
or new action follows from identifying this missing inference.
