# Frozen first group interval, after189-cell reconciliation

Domain canonicalL in[3.5,3.5001], upper conservatively covering both exact
specified decimal and binary64 literal. Use published63groups, original FP0/
P4/EM1 unit constants and A2 shape. Reconstruct189cell Mb,parentM,R,a, X43 EPS
collapse column and floor with50-digit directed arithmetic. CLASS-produced
EPS growth/variance grids and source quadrature/kernel/Hernquist arrays are
fixed numerical primitives. Do not use X53's coarse collapse interpolation.
Check all189lower-end branch signs; uncertain branches stop this bounded test
as inconclusive. No silently assumed branch monotonicity across a switch.

For both endpoints independently bracket every compact root using normalized
F(x)=B(x)/x^2 and directed signs on[1,1e7]. Verify compact side h(1)<2 and no
saturation. Bisection120steps or stop at an uncertain comparison while retaining
the enclosing bracket. Keep M,R fixed inL and invoke the existing analytic
compact-mass-order argument for intermediate L; law cells would be fixed if
certifiably below floor at the upper endpoint. This first run may declare
inconclusive instead of implementing any encountered mixed/uncertain branch.

For each endpoint propagate outward baryonic+halo mass intervals through the
actual positive kernel at all3000nodes. Fixed XG/M_H and kernel are interpreted
exactly. Record189velocity intervals acrossL from lower/upper endpoint order.
Build d_i=ls_i-v_i and slope_i=(v_i(+.01)-v_i(-.01))/.02. Enclose mean, sample
variance via sum_{i<j}(d_i-d_j)^2/[63*62], se=sqrt(var/63), systematic=.10*mean
slope, total=sqrt(se^2+systematic^2), and Z=mean/total. No fixed denominator or
monotonic-Z assumption. Original cuts tot<=.045 and absZ<2 remain unchanged.

Output common-scope necessary failure only if directed Z lower>=2, upper<=-2,
or total lower>.045. Otherwise INCONCLUSIVE, not a passing full-model witness.
Compare source baseline cells diagnostically within1e-10dex without padding
analytic boxes to contain rounded source values; record misses/deviations.
Require finite/outward arrays, all378root signs, positive kernels, original
input hashes and a wrong-velocity/statistic mutation. Independent70digit
root/velocity selected-case and separate interval statistic recomposition.
One thread, wall600/CPU480. Keep analytic fixed-primitive scope separate from
original floating libm/solver and CLASS continuum certification. No globalL
claim or added physical parameter. Preserve negative/inconclusive outcomes.
