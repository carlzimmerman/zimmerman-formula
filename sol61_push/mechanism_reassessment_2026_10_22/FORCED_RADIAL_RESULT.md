# Driven radiation through a polarized spherical background

A global radial driven-response calculation now carries positive outward energy through the finite-stiffness spherical background. The work supplied by the prescribed source matches the outgoing flux to about one part in a million. Relative to the same source in vacuum, radiation is strongly suppressed at one tested frequency and enhanced at the other. There is no single frequency-independent escape efficiency. This is progress toward testing radiation as a settling channel, not an established autonomous settling mechanism.

## What was solved

The background is the fixed Plummer baryon model of SPHERICAL_RESULT.md, with A=1 and epsilon=0.1. It is recomputed for each outer radius. The perturbation is radial, u=r sigma, in the formal weak-field reduced model:

    gamma u''''+(eta omega²-h)u''-h'u'+(h'/r-omega²)u=f(r),
    h=(1-q)^(-2)-1,
    f=-r(r²-3) exp(-r²/2)/(2pi)^(3/2).

The density perturbation integrates to zero total mass. Its quoted amplitude is a linear-response normalization; multiply it by an arbitrarily small amplitude to remain perturbative, and all powers scale with its square. It is prescribed externally and is not derived as a motion of live baryons or cold matter.

Length is in units R and time in units R sqrt(b)/c, with b=(2+3 beta)/beta and beta=0.02798. B=1, gamma=0.01 and eta=0.01/b in these units. This is the inherited illustrative beta choice, not a derived parameter.

The centre is treated at rmin=1e-5 using u-rmin u'=0 and u''-rmin u'''=0, which extrapolate the regular odd expansion to the origin. At outer radii 100,200,400 the admissible subspace contains both the outgoing oscillatory branch and the decaying branch. For h~H/r, H=2, these have leading forms

    outgoing: exp(i k r) r^(i alpha),
    alpha=-H k/[2(2 gamma k²-eta omega²)],
    decaying: exp(-kappa r) r^a,
    a=-H kappa/[2(2 gamma kappa²+eta omega²)].

Their first three derivatives define the two-dimensional boundary subspace. The incoming and growing coefficients are set to zero there. These are finite-order asymptotic conditions; domain convergence tests their effect on the measured powers, not exactness at a finite radius.

## Energy budget and results

For complex amplitudes with exp(-i omega t), the angular-normalized outward power is

    P(r)=omega/2 Im[(h-eta omega²) u* u'
                    +gamma(u'^* u''-u* u''')].

The corresponding source work is integral dr omega Im[f* u]/2. All displayed powers omit the common solid-angle factor 4pi. The exterior flux is constant outside the negligible Gaussian source tail. Physical units and a live-mode amplitude have not been assigned.

| Dimensionless frequency | Power at outer radius 400 | Same-source analytic vacuum power | Ratio |
|---|---:|---:|---:|
| 0.3 | 2.1484903e-6 | 0.0122855953 | 0.000174879 |
| 1 | 0.0004464970 | 0.0002261454 | 1.97438 |

The ratio below one at omega=0.3 is about a factor 5718 suppression. The ratio above one at omega=1 is allowed: a fixed-amplitude external drive supplies different work in different media. It is not an energy transmission fraction and is not bounded by one. The source shape has a frequency-dependent vacuum form factor; these two points do not establish a resonance, a universal filter law, or which mechanism dominates the change.

Between outer radii 200 and400 the powers change by 0.0357% and0.00364%, respectively. The worst source-work mismatch is 1.33e-6 relative; the worst exterior flux variation is 1.36e-6 relative. The analytic vacuum controls agree to better than4e-9 relative. Every accepted BVP reports convergence at tolerance2e-7; the largest mesh has72872 nodes. No independent discretization or wave-tolerance refinement was performed in this checkpoint, and the centre cutoff has not been systematically scanned.

## Numerical diagnostics retained

The first complex-valued collocation probe exhausted the mesh and failed a vacuum control. A real/imaginary split improved convergence and removed the large work discrepancy. The remaining small vacuum error disappeared after Taylor-extrapolating the centre conditions rather than imposing exact-origin values at a nonzero radius. Mesh limits were then increased without relaxing the residual tolerance. Failed probe scripts and outputs are retained; FORCED_RADIAL_CONTRACT.md records these diagnostic amendments. They are not counted as successful evidence.

The current bounded run forced_radial_run/manifest.json validates and all six acceptance checks pass. Replacing the outgoing branch with the incoming branch produces negative power and fails the outward-power check. The mutation still balances energy, as it should for an incoming solution: energy balance alone cannot certify the radiation boundary. Mathematical review remains self-review.

## Implication for the research goal

Unlike the earlier planar interface calculation, this includes a varying polarized spherical background and a compact mass-conserving source, so it supplies a genuine reduced-model source-to-exterior energy calculation. It supports continuing the radiation route, but rules out assuming a universal cooling efficiency from the existence of a gapless mode. A freely evolving perturbation or a live matter degree of freedom must determine its own frequency, energy and backreaction before a damping time can be inferred. Dividing arbitrary driven energy by power would not supply that proof.

This does not remove the independent observational obligations. The concurrently updated D7c_q2_rar_gate/README.md reports a scoped failure of the tested unscreened law families to satisfy its Cassini and SPARC gates together on both footings. D7d is investigating the stiffness-screened case separately. Our radiation result neither resolves nor bypasses those tests. The exact finite-background metric/clock reduction, cold-density selector and derivation of kappa=1/2 remain open.
