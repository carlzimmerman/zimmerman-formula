# A geodesic stationary clock cannot carry a nonlinear mass exterior on this branch

Base: `07fa64b44891fc87697f53f86812287946481586`. This is a necessary-equation obstruction for logarithmic KGB plus the fixed positive-A P2 acceleration response. It does not obstruct the accelerated flowing-clock candidate.

Take n spatial dimensions, n>=2, unitary clock phi=qt, and stationary areal metric
`ds²=-N²dt²+B²(dr+Vdt)²+r²dΩ_(n-1)²`.
Let `K_E>0`, `c>0`, `H>0`, `b=2c/(nH)`, and `Veff=n(n-1)K_E H²/2`. Assume a connected vacuum interval, nonzero radial clock flow V, geodesic clock N'=0, and the flat cosmological normalization N=B=1. The exact momentum equation first makes B constant wherever V is nonzero. The response and its first variation vanish at zero clock acceleration.

Varying the stationary radial action with respect to B and N *before* fixing N=B=1 gives necessary equations

`(r^(n-2)V²)'=nH² r^(n-1)`,

`V'+(n-1)V/r=-nH`.

The first integrates to `V²=H²r²+mu/r^(n-2)`; the second integrates to `V=-Hr+C/r^(n-1)`. Substitution gives

`r^(n-2)V²=H²r^n-2HC+C²r^(-n)`.

Its derivative differs from the required first equation by `-n C² r^(-n-1)`. Hence C=0 and mu=0 on the interval. For n=3 the Schwarzschild-like mass term mu/r is excluded on this fully geodesic branch. The n=2 identity is mathematical; no ordinary four-dimensional Newtonian interpretation is assigned to its constant mu.

This explains why an order-M expanding-dust metric can have a Newtonian potential with an unaccelerated clock: the forbidden residual starts at order C². A linear exterior calculation alone cannot establish a finite-mass exact stationary geodesic solution. The theorem makes no claim about N' nonzero, matter interiors with momentum, nonstationary sources, other response actions, or all possible clock theories.

For reproducibility, the radial action used for the necessary variations, with angular volume omitted and D=V'+B'V/B, is

```
K_E (n-1)/2 * [
 (n-2) N r^(n-3) (B+1/B) + 2 N' r^(n-2)/B
 - B/N * (2 r^(n-2) V D + (n-2) r^(n-3) V²)]
+ N B r^(n-1) (2c ln N - Veff)
- b B r^(n-1) V N'/N.
```

The omitted fixed-A response is zero to first variation on the geodesic configuration. Radial N/B variations are necessary even though the angular equation must also be retained for existence proofs. The accompanying script checks the two equations symbolically in dimensions n=2..7 and includes a control rejecting the false claim that the C/r^(n-1) linear perturbation is an exact finite-mass solution. The universal conclusion comes from the displayed algebra, not the finite dimension checks.
