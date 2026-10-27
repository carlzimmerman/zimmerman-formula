# Exact causal outlet reduction to audit before implementation

This is a derivation/proposed continuation, NOT an executed solver or a result
of the Gaussian-profile mode-wave run. The formula below is for a UNIFORM
spherical source; do not silently use it with the Gaussian profile already run.

With radial dV=r²dr and profile w=3/R³ inside R, source -Qdot(t)w has mean field

 chi_avg(t)=-(1/c²)integral_0^(2R) K(s) Qdot(t-s/c) ds,
 K(s)=3s/R³-9s²/(4R^4)+3s^4/(16R^6).

This is the pair-separation average of the3D outgoing Green function. Its
static integral is6/(5R). Integrating twice by parts, using K endpoints0,
K'(0)=3/R³ andK'(2R)=0, gives the numerically cancellation-free reaction

 chi_t,avg(t)=-integral_0^(2R) K''(s)[Q(t-s/c)-Q(t)] ds,
 K''(s)=-9/(2R^4)+9s²/(4R^6).

A constant prehistory Q=Q0 represents zero incident physical field. At frequency
omega, Dret=integral K exp(i omega s/c)ds obeys

 ImDret=(omega/c)|F(omega R/c)|²,
 F(x)=3(sin x-x cos x)/x³.

Thus the same kernel determines conservative reaction and positive radiative
loss. They must not be fitted independently. The constant-source and harmonic
identities need an independent numerical audit before relying on a new solver.

One implementation route is implicit two-stage Gauss collocation on material
modes with a dense current-step polynomial. Retarded arguments inside that
step use the collocation polynomial; older arguments use completed source
polynomials. This avoids a globally fine outgoing spatial wave grid. It still
requires convergence and a causal/passive error audit; a negative internal-time
composition is not a direct causal delay solver.

Outside the source, write
 qeff(t)=integral_-R^R 3(R²-z²)/(4R³)Q(t+z/c) dz.
Then r chi=-qeff_dot(t-r/c)/c². The radiation component is
P=qeff_ddot²/c³, and finite-radius total flux adds the derivative of boundary
storage qeff_dot²/(2c²r). Use the actual observer delay when comparing to body
work W=-integral chi_t,avg Qdot dt. Interior stored field energy W-Fout must
remain nonnegative within numerical error. These identities distinguish a
physical outlet from a loss inserted inside the near field.

For a global variable source the kernel is a matrix of spatial overlap
functions, not this single monopole formula. Separate an exact variational
quasistatic near field from controlled retarded corrections; preserve the
reciprocal transpose force. No global density manifold or assigned power is
introduced by this construction.
