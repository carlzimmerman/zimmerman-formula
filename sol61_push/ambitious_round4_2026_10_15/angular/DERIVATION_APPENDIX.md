# Elementary details behind VC4-ANGULAR-001

This appendix supplements the frozen `PROOF.md`; it is not an input to the
bounded experiment and does not change that experiment's immutable inputs.

## An explicit material mass-flux representative

For l>=1, put Y=Y_lm, q_a=rho_a xi_a and define scalar radial amplitudes

    u_a(r)=rho_a(1) h r^(l-1),
    v_a(r)=[(l+1)rho_a(1)h r^(l-1)+r eta_a(r)]/[l(l+1)],
    q_a=u_a(r)Y n+v_a(r) grad_S Y.

Here grad_S is the gradient on the unit sphere expressed in its unit tangent
vectors. The spherical divergence is

    div q_a=[u_a'+2u_a/r-l(l+1)v_a/r]Y=-eta_aY.

The radial trace is exactly rho_a(1)hY, independently for the two fluids.
The leading center term is a multiple of grad(r^lY); the eta_a part has the
usual smooth harmonic center behavior. Thus it gives an explicit smooth
representative and avoids invoking a Neumann existence theorem in section 1.
The construction permits independent eta_b and eta_c and arbitrary h.
Additional weighted divergence-free tangent fields give exactly the static
material relabeling freedom.

For exact configuration paths one can prescribe the smooth common radial
graph, set rho_a,epsilon=rho_a+epsilon eta_a+O(epsilon^2), and correct each
mass by a smooth compactly supported interior scalar of order epsilon^2.
Since rho_a is uniformly positive, these densities stay positive for small
epsilon of either sign. The acceleration correction cancels in the
constrained Hessian. The continuity equation supplies material velocities
with the corresponding normal trace; the displayed flux gives its tangent.
No separate instantaneous local incompressibility condition is imposed.

## The all-l Legendre divided-difference integral

Define

    J_l=integral_-1^1 [1-P_l(u)]/(2-2u)^(3/2) du.

The harmonic kernel expansion on two concentric spheres, followed by its
increasing-radius limit (the limiting singularity is integrable), gives

    integral_-1^1 P_k(u)/sqrt(2-2u) du=2/(2k+1).

This may also be verified by inserting the polynomial Rodrigues formula.
The elementary polynomial recurrences are

    P_n'=sum_{k=n-1,n-3,...>=0}(2k+1)P_k,
    (u-1)(P_l'+P_(l-1)')=l(P_l-P_(l-1)).

The first follows by telescoping P'_(k+1)-P'_(k-1)=(2k+1)P_k.
Consequently the weighted integral of P_n' is 2 ceil(n/2), and the weighted
integral of P_l'+P_(l-1)' is 2l. The second recurrence now gives

    J_l-J_(l-1)=1/(2l) integral_-1^1
                    [P_l'+P_(l-1)']/sqrt(2-2u) du=1.

As J_0=0, J_l=l for all nonnegative integers. The normalized polar integral
is 2pi J_l, giving the exact fractional-kernel eigenvalue used in the wall
self-gravity calculation. The bounded exact checks l=0..16 independently
integrate the polynomials after u=1-v^2/2; they are implementation checks,
while this recurrence covers the unbounded range.

## Direct meaning of the wall/fluid potential expansion

For a smooth common material map, the wall/fluid gravitational interaction
can be written in fixed reference variables as

    -Gs integral_Omega rho_0(y) integral_S2
                 J_surface(n)/|T_wall(n)-T_fluid(y)| dOmega dy.

The difference of two displacement vectors is O(|n-y|) near coincidence.
After two material derivatives, the integrand is therefore bounded by a
constant times 1/|n-y|, which is locally integrable in this surface/volume
pair integral. A cutoff around coincidence justifies differentiation and
then its removal. The fixed-interior-point wall potential expansion (9)
can consequently be integrated, after pairing its first derivative with the
fluid tangent. Its second-derivative monopole is -Gs Lh^2, and the cross
pairing is twice the interior value of (9) against the full distribution (2).
This gives equation (10) without mixing normal traces. In this argument the
shell is moved with its actual area element; no wall mass conservation is
introduced.

For wall self-gravity the difference of two surface displacements similarly
removes the apparent diagonal divergence. The displayed divided-difference
formula is a convenient explicit way to perform the integrable limit.
