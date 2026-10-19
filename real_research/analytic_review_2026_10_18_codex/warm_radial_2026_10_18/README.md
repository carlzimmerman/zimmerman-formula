# Radial dispersion with an exact finite halo profile

18 October 2026. Checkpoint ZAR-2026-10-18-03, continuing [the finite halo checkpoint](../finite_halo_2026_10_18/README.md) at Git baseline `3c01aa2861bf576f4c2d942251eb9d2f89cae108`.

**The finite circular halo can be replaced by an ordinary positive distribution with genuine radial motion while retaining exactly its density, law annulus and outer boundary.** A new accessible radial energy identity supplies a stability certificate for that same distribution. The qualification is regularity: the constructed distribution is integrable and smooth away from the circular-orbit curve, but can become unbounded near that curve. Linear stability is established in a specified accessible energy completion, rather than as a classical differentiable L1 Vlasov theorem at the possible singularity.

No scientific scripts, numerical integrations, simulations, statistics or process operations were performed. Claude's calculations and previous research artifacts were left untouched.

## What is preserved and what changes

The starting halo has a smooth cumulative cold mass M(r), hollow support r0 < r < R, M <= A r, and M = A r on a closed interior annulus. Its two populations have M_t = f M and M_f = (1-f) M, with 0 < f < 1 and A = sqrt(a0 M_b/G). Choose the already identified sufficient condition r0 > 2 f^2 r_M/(1-f), with r_M = M_b/A, and remain in the deep cubic regime as specified in the previous checkpoint.

| Property | Warm construction |
|---|---|
| Total and individual density profiles | Exactly unchanged |
| Cold mass, fraction f, law amplitude A | Exactly unchanged; still selected inputs |
| Hollow core and smooth finite outer taper | Exactly unchanged; no wall or surface pressure |
| Exterior potential and forces | Exactly unchanged by self-consistency |
| Radial velocity dispersion | Strictly positive on the entire law annulus; bounded and arbitrarily small if desired |
| Phase-space distribution | An ordinary nonnegative finite-mass L1 function, with no delta component |
| Regularity | Smooth at every accessible eccentric phase point; a possibly unbounded circular ridge remains |
| Radial stability | Coercive accessible quadratic and a well-defined linear energy-form flow |
| Classical, nonlinear or nonspherical stability | Not established |

The exact density is obtained by a positive, countable decomposition into narrow families of eccentric bound orbits. The decomposition is an analytic existence proof; no numerical orbit library or infinite computation was executed. A compact interval of the law region receives a positive lower bound on radial dispersion, not merely a formal nonzero parameter. Its value is not prescribed or measured.

Here preserving the law means preserving density, acceleration and the circular-speed curve. The dark population's tangential velocity moment also contains a radial-pressure-gradient term. On the r^-2 law annulus, its exact Jeans relation is <v_perp^2>_i = v_ci^2 + r d(sigma_ri^2)/dr; a constant dispersion would remove that correction, but is not prescribed by this construction.

## Why the new stability argument applies

The earlier susceptibility estimate need not survive this construction: the energy derivative of the distribution can be too large near circular orbits. The new proof uses weighted velocity moments that remain finite. It derives the actual warm radial quadratic, including orbital transport and the reciprocal field response, rather than assuming continuity of the circular-shell stability result.

For an odd radial canonical generator, the quadratic splits into nonnegative orbital terms and the same positive relative-population square found previously. Uniformly positive background epicyclic coefficients make the complete form coercive. No small-temperature spectral-continuity argument is required.

The resulting energy controls linear dynamically accessible radial disturbances in the explicitly constructed energy space. The aggregate perturbation can be a distribution at the circular ridge. This distinction matters: the equilibrium itself is an ordinary L1 function, but its tangent under a smooth canonical motion need not be an ordinary L1 function.

## Proofs and remaining obligation

[EXACT_WARM_DF.md](EXACT_WARM_DF.md) constructs the distribution, proves positivity and exact self-consistency, and checks radial pressure and finite boundaries. [ACCESSIBLE_STABILITY.md](ACCESSIBLE_STABILITY.md) gives the warm quadratic, the energy-space flow and its uniform bound. [AUDIT_AND_HANDOFF.md](AUDIT_AND_HANDOFF.md) records the reviewed claims and their limits.

The request is achieved at the level of a finite positive warm equilibrium and a precise radial linear energy theorem. The stronger physical target remains open: control the circular ridge sufficiently to obtain a bounded smooth distribution and a classical stability theorem, then derive formation and test the same model against observations. The amplitude, population fraction, covariant action, finite stiffness and nonradial dynamics have not been derived here. No global novelty or empirical-success claim is made.
