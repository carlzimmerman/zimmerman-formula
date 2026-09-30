# A three-halves collective resonance with its continuum retained

Base 71ec122825c9539d6c1dac2843fa397651f00ec0. This executes the retarded-loop dependency of CANONICAL_CLOCK_RESULTS.md. It is a free planar, neutral, zero-temperature calculation coupled to the assumed local clock reduction. It is not a new derivation of 32pi or a proof of the whole theory's causality.

## Frequency kernel from the mass vertex

For the prior four-band planar Dirac operator, the three polarization components enter as anticommuting mass vertices. They are not electric density vertices; importing a graphene charge-density response would give a different numerator. With positive-band degeneracy nu, coupling y, tangential speed v, and rescaled Euclidean external momentum Q=sqrt(Omega^2+v^2 k_parallel^2), the analytic-constant-subtracted mass bubble is

Pi_E(Q)=nu y^2 Q/(8v^2).

The trace reduction gives nu y^2 Q^2/v^2 times the massless scalar integral I(Q). Feynman parametrization evaluates

I(Q)=integral d^3l/[(2pi)^3 l^2(l+Q)^2]

    =integral_0^1 dx/[8pi Q sqrt(x(1-x))]=1/(8Q).

The planar spatial rescaling supplies 1/v^2. At nu=2 and Omega=0 this reproduces y^2|k_parallel|/(4v), independently matching SLOW_WALL_RESULTS.md. The constant subtraction and critical quadratic matching are assumptions inherited from that route.

Analytic continuation gives the retarded bubble

Pi_R(omega,k_parallel)=nu y^2/(8v^2) sqrt(v^2 k_parallel^2-(omega+i0)^2),

with the branch analytic in Im omega>0 and positive on the positive imaginary-frequency axis. For positive real omega above the pair threshold the square root has negative imaginary part. Its particle continuum is part of the response; it cannot be discarded when assessing causality or damping. SciSpace discovery returned charge-response candidates, whose abstracts do not authenticate this mass-vertex formula. The derivation above and its prior static limit are the load-bearing inputs.

## Isotropic orientations eliminate a strict threshold

For independent equal-weight planes whose normals are isotropic in three dimensions, write mu=|khat dot normal|, uniform on [0,1]. The averaged square root is

B_R(omega,k)=integral_0^1 sqrt(v^2 k^2(1-mu^2)-(omega+i0)^2)dmu

             =vk J(r), r=omega/(vk).

For 0<r<1,

J(r)=pi(1-r^2)/4 - (i/2)[r-(1-r^2)atanh(r)].

For r>1,

J(r)=-(i/2)[r+(r^2-1)atanh(1/r)],

and J(1)=-i/2. The real/imaginary integrals are obtained by splitting at mu=sqrt(1-r^2). The resulting small-frequency expansion is

J(r)=pi/4-pi r^2/4-i r^3/3-i r^5/15+O(r^7).

Planes nearly normal to k have arbitrarily small tangential momentum. As a result the averaged continuum starts at zero frequency. A pole that would lie below the threshold of one selected plane becomes a damped resonance in the isotropic ensemble. Calling it exactly undamped would be an incorrect transfer from aligned support.

## Dressed clock reduction and its acceleration link

Let q0 be the assumed area density and define

zeta_loop=pi G nu q0 y^2/(2v^2), Gamma_R=zeta_loop B_R.

At quadratic order the polarization constraint is p=a/(1+Gamma_R). Because Re Gamma_R>0 in the upper half-plane, this elimination introduces no upper-half-plane zero in its denominator. In the retarded linear-response equations, the effective lapse coefficient is eta_R=2/(1+Gamma_R). Eliminating lapse and shift as in the previous clock probe changes the scalar inverse response to

A_kin omega^2-2 zeta_loop k^2 B_R,

A_kin=2(3lambda-1)/(lambda-1)>0.

Set the separate R3^2 stabilizer to zero for this test and define gamma=2 zeta_loop/A_kin. The normalized inverse is

F_R(omega,k)=omega^2-gamma k^2 B_R(omega,k).

This is a retarded response reduction, not a complex single-copy action used as a substitute for a closed-time-path quantum calculation. Noise/fluctuation correlators and loop backreaction on the vacuum are not calculated.

Using the bare static scale a0_bare=v^2/(2G nu y^3 q0),

zeta_loop=pi/(4y a0_bare),

gamma=pi(lambda-1)/[4y a0_bare(3lambda-1)].

The density, degeneracy and gravitational coupling cancel in this conditional dynamical/static relation. Unlike an arbitrarily assigned fractional kinetic term, the collective stiffness is now tied to the same static scale through the specified loop. Free y,v,lambda and the critical matching still remain.

For t=gamma k/v<<1, the continued resonance satisfies

omega_real^2=(pi gamma v/4)k^3[1+O(t)],

Gamma_width=pi gamma^2 k^3/(24v)[1+O(t)],

Gamma_width/omega_real=(sqrt(pi)/12)t^(3/2)[1+O(t)].

Thus the low-momentum resonance has exponent 3/2 and becomes narrow, although its spectral continuum is never absent. In the original parameters its leading real squared frequency is pi^2 v(lambda-1)k^3/[16y a0_bare(3lambda-1)]. The resonance is a lower-sheet continuation of the retarded boundary. Evaluating the principal angular square root directly in the lower half-plane instead would choose another boundary and is not this resonance calculation.

## Exact frequency stability statement

For k>0,gamma>0, F_R has no zeros in the open upper half-plane. Write omega=x+i s with s>0. If x is nonzero, omega^2 has imaginary part of sign x. Every square root in B_R has imaginary part of the opposite sign, because its argument has imaginary part -2xs and its chosen real part is positive. Therefore Im F_R has the sign of x and cannot vanish. If x=0, omega^2=-s^2 while every square root and B_R are positive real, so F_R<0. This covers the entire upper half-plane, not just numerical samples. A nonnegative k^4 term on the right hand side leaves the same argument intact.

On the positive real axis Im B_R<0, so Im F_R>0 and the conventionally normalized spectral density -2 Im[1/(A_kin F_R)] is positive. The numerator's sign and the pole exclusion support a passive, temporally stable free response in this reduction. They do not establish a bounded spatial signal cone. Constraints, omitted bulk modes, spacetime support and interactions require separate checks.

In particular the earlier free-field obstruction in CAUSALITY_GAP_RESULTS.md concerned an exact isolated fractional pole with its canonical fixed-time kernel. That is not the full propagator calculated here: retaining the continuum changes the object. This prevents applying that isolated-pole argument unchanged, but does not prove that the full kernel has the cancellations needed for finite-cone propagation. No such proof is claimed.

## Evidence and physical limits

Twenty-nine checks pass. They include the Feynman parameter integral and static normalization, exact small-r coefficients, independent angular quadrature on both sides of the single-plane threshold, upper-half-plane continuation/sign checks, and four damped resonance roots. The maximum real-axis angular discrepancy is about 2.24e-16. At t=0.001 the width/frequency ratio is about 4.67e-6; at t=0.3 it is about 0.0184. The proof above supplies the universal frequency-pole conclusion; the grid supplies implementation evidence only.

Self-review status: the specified free planar kernel, orientation average and retarded principal-clock reduction are internally consistent. The assumed independent-plane geometry, zero filling and temperature, constant quadratic subtraction, matching to the scalar q, and omission of other fields remain physical dependencies. The calculation applies locally where curvature and the de Sitter state can be neglected relative to the actual mode frequency, not merely relative to k. The microscopic continuum's vacuum stress has not been folded into the canonical background calculation, so the preceding geometric coefficient bridge is not upgraded to a quantum self-consistent solution.

This gives a constructive mechanism for the previously problematic exponent without declaring a fundamental fractional operator. Next, audit finite-cone propagation and the actual de Sitter/thermal mode response or determine the physical window in which this local result applies. The conditional cosmological-coupling prediction in CANONICAL_CLOCK_RESULTS.md still needs a current observational check. D,lambda and the additive vacuum normalization are unselected; no exact 32pi follows from these retarded identities.
