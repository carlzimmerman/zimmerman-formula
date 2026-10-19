# Actual charged sea coefficient in a declared closed lattice model

**This computes a microscopic vacuum coefficient, not the physical curved-QCD A or its ratio.** The full unconditioned finite measure contains SU(3) links, integer-flavor one-component staggered determinants and every physical noncompact photon mode. The graph and phases are defined explicitly; equivalence to continuum QCD spin/taste transport on a smooth round sphere is unverified.

For the cubical S4 complex K_n=boundary[0,n]^5, arbitrary positive common photon/color plaquette weights, and rational flavor charges S_Q=sum q_f^2, the exact multivariate coefficient is

    W_u |_(beta kappa^4) = beta kappa^4 S_Q (30n^4+20n^2-1)/6,
    u=e^2=4pi alpha, W=-logZ.

The calculation uses the actual leading plaquette term of the specified fermion determinant. A direct hopping-matrix second derivative independently verifies both current and contact terms. The complete photon covariance has weighted plaquette trace rank(d1); this global linear-algebra identity removes the need to fit a photon response or choose an unknown coefficient. The staggered factor is2 kappa^4, and a flat Wilson-spinor factor16 is not substituted.

For charges(2/3,-1/3,-1/3), the coefficient of beta kappa^4 in W_u is49/9,559/9,2609/9 at n=1,2,3. These are exact model coefficients, with no measured alpha, physical mass or cosmological input. The formula is independent of positive plaquette weights only because the color and photon actions use the same declared weights and this hopping coefficient is uniform.

There is no n^3 term at this order. At V=10a^4n^4, the formal polynomial radius derivative gives rho_u=beta kappa^4 S_Q/a^4[1/2+1/(6n^2)]. Its n^-1 coefficient vanishes. This is a result at finite spacing/heavy hopping on an unprojected polyhedral regulator. It neither excludes a physical nonperturbative H-linear term nor proves its differentiated continuum limit. Higher orders, light-quark dynamics, physical state normalization, taste/spin matching and the smooth fixed-physics trajectory remain unresolved.

The completed current-v2 run performs55,469 bounded checks: actual cells/ranks/boundary-of-boundary and all square phases at n1,2,3, two independent tree-gauge Gaussian controls at n1, and four direct hopping-matrix derivative controls. For uniform weights all80 plaquette variances equal49/80; for nonuniform weights their individual values change while their weighted sum remains49. Forty-digit arithmetic uses1e-30 comparisons for these independent Gaussian/matrix checks; exact counts use integers/F2. These are finite implementation checks, not a physical precision claim or a universal proof from case counts. The analytic H1/rank and hopping argument is in DERIVATION.md. Runtime0.995112 seconds, wall cap120 seconds, CPU100 seconds, one numerical thread, no RLIMIT_AS on macOS.

Independent review is separate from the completed run. This package alone leaves physical A,A_u,full proton M_u,R(alpha) and alpha open.
