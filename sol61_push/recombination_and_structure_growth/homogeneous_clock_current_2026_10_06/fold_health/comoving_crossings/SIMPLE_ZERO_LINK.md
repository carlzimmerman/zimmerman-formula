# The two comoving crossings are genuine simple zeros covered by the local theorem

The illustrative eta=.5,kappa=.99 fixed-comoving mode satisfies the hypotheses of ../canonical_crossing/REPORT.md at both reported zeros. This link is stronger than detecting a negative coefficient: exact rational brackets certify true roots and nonzero derivatives, with finite positive q,rho and nonzero Theta. It does not integrate modes through the zeros or prove global uniqueness of crossings.

Let H=hH*, S be the comoving envelope in this folder's REPORT, and denote the coefficient by Kclock. At a zero kbar²=S(z),

    dKclock/dz=-kappa M z^(2/3)Sprime(z)/(h-eta)²,
    z_dot=-3Hz,
    alpha=Kclock_dot=3kappa M H z^(5/3)Sprime(z)/(h-eta)².

Thus nonzero Sprime is exactly a simple zero in physical time; no WKB dispersion interpretation is required. The signs are negative on entry from the earlier universe and positive on exit.

The reported kbar² decimal is fixed as an exact rational in the certified check. This specifies an actual nearby mode without treating the prior rounded stationary maximum as an exact number. The proof locates true coefficient zeros for that explicitly declared mode.

crossing_hypotheses.py encloses the authentic z(t)>1 branch on the rational t rectangles[1.728,1.729] and[160.69,160.70]. It authenticates z enclosures using exact Fraction arithmetic for ln x: after argument reduction to1<=x<2, ln x is bounded by80 terms of the atanh series and the explicit positive geometric tail. The numerical LambertW value only proposes an enclosure; both endpoints are then certified against the original monotone z-ln z equation.

Within each rectangle the sign of S-kbar² is tested without fractional-power rounding by cubing positive quantities:

    sign(S-kbar²)=sign((3eta²)^3(t-1)^3-kappa³(kbar²)^3z²).

Exact endpoint sign changes give a genuine root by continuity. To certify a nonzero derivative throughout each root rectangle, bound

    E=3t(z-1)-2(t-1)²(1+eta t)

from below by3t_lo(z_lo-1)-2(t_hi-1)²(1+eta t_hi), and from above by3t_hi(z_hi-1)-2(t_lo-1)²(1+eta t_lo). The first rectangle has a strictly positive lower bound; the second has a strictly negative upper bound. The positive prefactor in the exact Sprime formula therefore certifies nonzero derivative at every possible root in each rectangle. These strict derivative signs also give uniqueness within those two rectangles; no global root-count claim follows.

Descriptive70-digit evaluations at the earlier computed root approximations give:

| z | Sprime | alpha/(M H*) | q/q* | Theta/(M H*) |
|---:|---:|---:|---:|---:|
| 6539.89627563 | -8.471722447e-6 | -.716189979 | .0191361074 | 80.8467074 |
| 2.01351936563 | .1899495374 | 1.814588526 | .668417114 | 1.36406616 |

The root-existence and nonzero-slope conclusions use the exact rational bounds, not those descriptive decimals. On these rectangles t>1,z>1; the implicit background derivative denominator(t-1)(1+eta t) is nonzero. Hence t(z) is analytic. The equations H=H*(1+eta t),rho=2c z,q/q*=t exp(-eta/2)/z and z_dot=-3Hz make the background analytic in physical time, with positive finite q,rho,H and Theta. The chosen kbar is nonzero, so physical p is nonzero. This verifies all local background/simple-zero hypotheses needed by the canonical theorem.

That theorem's separate exact full-action result now applies: generic local mode amplitudes have logarithmic zeta and a1/(T-T0) pole in the invariant deltaX_clock=-q²nu. Its regular local subspace is codimension one at each crossing. This link does not prove the two local regularity conditions are globally independent, select those amplitudes dynamically, quantify nonlinear continuation or establish quantum vacuum decay. It identifies actual finite comoving modes to which the conditional linear obstruction applies, beyond an instantaneous IR sign argument.

Authoritative new run link_a9/9; link_redshift_control_a rejects the exact proper-time derivative identity when physical-p redshift is deleted. Both standard manifests validate. Original16-check script/manifests and parent inputs are untouched. The new runner bounds are wall30s,CPU20s,1MiB logs,one cooperative thread. No ODE mode integration or astronomical dataset was run.
