# HR01-T adversarial self-review

Normalized claim: a single covariant action with the existing fitted kappa=1/2 and no unaccounted fit produces a well-posed turnaround-triggered galaxy law, the required region/frame prescription, conserved dark mass and joint local/cosmological observables. Primary verdict: **incomplete, with the smallest missing implication**. The newly supplied fixed-region action and constitutive repairs do not establish a moving-region conserved covariant dynamics.

Dependency graph: baryon/clock/metric action -> full constraints and kinetic symbol -> region evolution and source/flux rule -> frame/tidal response -> spherical/halo/web observables -> joint gates. A separate branch, carrier evolution -> available dark mass and exchange current -> physical source edge, is required for the retained-source continuation. Reusing a numerical halo reservoir without that branch does not derive the edge.

| Obligation | Status | Decisive reason |
|---|---|---|
| C2 saturated local gate has some negative curvature | passed | Mean-value argument at fixed positive B; finite step checks support implementation |
| Entire coupled action is well posed | not addressed | Frozen fluid symbol omits full metric/clock/region constraints |
| Gaussian threshold includes equality | failed | Equality leaves a kinetic zero; strict coercivity requires R>Rmin |
| Uniform-field auxiliary frame cancels a constant field | passed | Exact shift covariance for fixed region and prescribed W |
| Auxiliary stationary mean equals material COM acceleration | failed | Different weights; explicit three-cell counterexample |
| The density-tide monopole is always second order | failed | First-order response proportional to tr(T); exact paired profile supplies stronger finite example |
| New region/frame action exists for merging theta-components | conditional | Shape derivatives and merger/zero-mode conditions have not been supplied |
| D2 gate can cause its own first turnaround before Newtonian turnaround | failed in stated shell class | W=0 before the event; identical initial-value problem until the event |
| KiDS/Local Group sharp/ramp gates pass jointly | failed in tested family | Large KiDS excess, small sharp R0, and disjoint sampled ramp requirements |
| Cluster crossed-shell proxy is true splashback | not addressed | Radial tracer shells lack the required self-consistent phase-space dynamics |
| Static source gate keeps exterior mass | passed | Integrated radial density mask and named mutation |
| Source mask is automatically the original scalar Euler-Lagrange rule | failed | Nonselfadjoint WL unless [W,L]=0 |
| Additive retained source is harmless for the cosmic mean | failed in HOD surrogate | Selected-population extra mean 0.26–0.37 of matter density |
| Capped replacement conserves static halo budget | computationally verified in stated range | Exact total-mass cap; compact control preserves mass to 1e-12 |
| Source density has a conserved evolving exchange current | not addressed | Required (partial_t W)rho + j.grad(W) transfer not yet derived |
| Compact replacement has O(k²) infrared difference | passed under finite-moment assumptions | Taylor expansion of spherical form factor; computed coefficient control |
| Infrared mass compensation implies unchanged sigma8/CMB lensing | not addressed | Dynamics and finite-k correlations are missing |
| Local shear repair preserves tensor propagation | failed | It adds C to TT kinetic coefficient |
| Scalar-projected shear repair avoids that TT term | passed at frozen nonzero flat Fourier modes | Double divergence annihilates TT/transverse pieces |
| Scalar projection is a local causal covariant theory | not addressed | Instantaneous spatial inverse and full constraints require construction |
| CMASS data likelihood passed | not addressed | No measured CMASS covariance on disk; conditional forecast only |
| Kappa is derived | out of scope | It remains fitted by contract |

These checks were performed in one worker and are labeled self-review. Numerical baseline reproduction is not independent physical validation. Cached external observational summaries are not newly authenticated here. All new analytic claims are derived in the linked reports under explicit hypotheses; no finite run is presented as a universal theorem.
