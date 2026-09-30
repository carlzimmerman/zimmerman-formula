# Spatial response changes the Newton calibration

Base 3e647adcf515e487628f89a7c4a0122575676522. Verdict: in the explicitly truncated weak-static diagnostic below, canonical scalar gradients can invalidate the pointwise-relaxation calibration even at large local acceleration. A finite small-Z solution recovers it. This is a self-reviewed scalar/flux boundary probe, not a full metric and foliation solution, an observational exclusion, or a derivation of 32π.

## Specify the approximation before matching

Use the variable-clock family U=A/q²+Bq², lambda(q)=1+ell q. Hold the cosmological extrinsic-curvature scalar K_trace² at 9H² in the scalar equation, neglect its weak metric/shift corrections, and neglect the curvature-squared stabilizer and nonlocal fermion kernel. The cubic coefficient K_c is still an assumed local coupling. Then

    Z Laplacian q=U'(q)+C+K_c P³,
    C=(9/2)M²H²ell,
    g=P+b,  b=12πG K_c q P².

The cosmological boundary value is q*, where U'(q*)+C=0. It is not the old flat-static minimum q0=(A/B)^(1/4). In spherical symmetry assume the leading bare flux law b=G M(r)/r². Scalar stress in the metric equations and the clock's spatial response have not been solved; importing that flux law is part of this diagnostic's contract.

For a smooth Plummer source with scale R and bare compactness epsilon=GM/R,

    M(r)=M r³/(r²+R²)^(3/2),
    b(r)=epsilon R r/(r²+R²)^(3/2),
    P=sqrt[b/(12πG K_c q)].

Retaining scalar gradients gives the nonlinear radial equation

    Z(q''+2q'/r)=−2A/q³+2Bq+C
                 +K_c[b/(12πG K_c q)]^(3/2).

The pointwise prescription instead sets its right side to zero at each radius. Multiplying that algebraic equation by q³ yields a strictly increasing function of positive q, so its local positive root is unique. This does not establish uniqueness or stability of the differential boundary problem.

## Finite boundary experiment

Choose A=B=M²=1, G=1/(8π), K_c=16, ell=10 and epsilon=0.001. The vacuum has q*=0.7795472964, H approximately 0.24325 and D=12πG(2A K_c²)^(1/3)=12. For Z=1, solve at R={10^−3,10^−4,10^−5,10^−6}; outer radius is 0.01. Compare Z=10^−14 at R=10^−6, and repeat with a tenfold smaller inner cutoff and a doubled outer boundary. There are eight finite BVP runs in total.

Use log radius, impose dq/dln r=0 at the declared finite inner cutoff and q=q* at the outer boundary, scipy solve_bvp tolerance 10^−6 and maximum 20000 nodes. The default inner cutoff is 10^−6 R; its refinement is 10^−7 R. Small-Z guesses resolve the outer Dirichlet boundary layer. These are finite-domain boundary conditions, not an exact match to a complete cosmological solution at infinity.

At the maximum flux radius r=R/sqrt(2):

| R | Z | q from differential equation | q from local root | g/b from differential equation | g/b from local root |
|---|---|---|---|---|---|
| 10^−3 | 1 | 0.77954721 | 0.77696233 | 1.37264827 | 1.37326764 |
| 10^−4 | 1 | 0.77954726 | 0.70058425 | 1.11784173 | 1.12430544 |
| 10^−5 | 1 | 0.77954728 | 0.15530529 | 1.03726483 | 1.08348860 |
| 10^−6 | 1 | 0.77954729 | 0.01558840 | 1.01178417 | 1.08333348 |
| 10^−6 | 10^−14 | 0.01558840 | 0.01558840 | 1.08333348 | 1.08333348 |

At the last radius b approximately 384.90 is large compared with the cubic acceleration scale. Nevertheless the Z=1 scalar departs from q* by only about 5.76×10^−9 relatively, while the local root would be smaller by about 98%. Large acceleration by itself does not enforce pointwise relaxation. The small-Z case tracks that root at the flux peak; changing either tested boundary leaves that peak value unchanged to the declared 10^−5 relative tolerance.

The sampled sourced-potential integrals are below 0.0015. A static-curvature correction proxy (Hr)²/(P/a0_bare) stays below 0.0035, where a0_bare=1/(12πG K_c q*). These help choose a weak local diagnostic; they are not residuals of the omitted ADM equations, error bounds on every omitted term, or a certificate that the phenomenological action has a controlled physical cutoff. Toy lengths and couplings have not been calibrated to astronomical data.

## An analytic near-vacuum comparison bound

Let h=q*−q and restrict to a positive branch q*/2<=q<=q*. Then the restoring force can be written U'(q)−U'(q*)=−M(q)h, with M(q)>0. The radial equation implies

    −Z(r²h')' <= r² f_upper(r),
    f_upper=2^(3/2)K_c[b/(12πG K_c q*)]^(3/2).

With zero inner derivative and h=0 at the outer boundary, integrate this inequality twice. For every radius in the annulus,

    h(r) <= (1/Z) integral_0^infinity t f_upper(t) dt
          = 2^(3/2) K_c epsilon^(3/2) sqrt(R)
            × I/[Z(12πG K_c q*)^(3/2)],
    I=integral_0^infinity s^(5/2)/(1+s²)^(9/4) ds
     =(1/2)Beta(7/4,1/2)=0.7188841408.

The finite-annulus integral is smaller than the displayed infinite-domain source bound. This argument is conditional on the near-vacuum branch; it neither asserts that every solution lies there nor proves a global basin or uniqueness theorem. It shows that within such a branch, shrinking a source at fixed epsilon and fixed positive Z makes its maximum displacement vanish as sqrt(R), even though peak b grows as 1/R. All five Z=1 sampled profiles lie in the branch and below that bound. The small-Z solution is outside it and is not constrained by this estimate.

The associated formal weak-compact limit on the near-vacuum branch has q approaching q*, P proportional to sqrt(b), and g/b approaching 1. The pointwise-relaxed high-field limit instead has g/b approaching 1+1/D. Thus these are distinct orders of spatial-response and field limits inside this truncation; choosing the latter as a universal laboratory Newton dictionary needs an additional physical argument.

## Corrected conditional coefficient bridge

At small P, the local-curvature algebraic branch has q=q*−K_c P³/U''(q*)+higher orders. Its bare deep scale is therefore a0_bare=1/(12πG K_c q*), while the cosmological curvature is Lambda=16πG U(q*)/S*. Define x=q*/q0. The linear-coupling vacuum equation gives

    1/3 < x⁴ < 1,
    S*=2(1+x⁴)/(3x⁴−1).

Consequently the bare scale ratio is

    Lambda/a0_bare² = D³(3x⁴−1)/3.

If an independently justified Newton measurement gives G_N/G=R_N, matching the deep spherical force sets a0_N=a0_bare/R_N, so the ratio becomes the preceding expression times R_N². In particular, only if local high-field relaxation supplies R_N=(1+D)/D does it become

    Lambda/a0_N² = D(1+D)²(3x⁴−1)/3.

If the near-vacuum high-field dictionary R_N=1 applies, it stays the bare expression. For the illustrative D=12, ell=10 parameters these two conditional coefficients are approximately 72.92414 and 62.13655 respectively; neither equals 32π approximately 100.53096. A finite measured g/b in the table is not itself an asymptotic Newton constant.

Stationarity relates x to the free coupling ell; it does not quantize it. D is also still independent. Imposing either coefficient to be 32π merely fits a condition on these parameters. An additive vacuum constant remains an independent allowed modification. These formulas organize the missing mechanism; they do not supply it.

## Provenance, failures and dependency impact

The final radial BVP record passes 50 finite checks, the conditional coefficient bridge passes four symbolic checks, and the gradient comparison record passes 11 checks including independent quadrature of the beta integral. Input/output hashes and contracts are retained in their runs directories. Two earlier singular-radius attempts failed the mesh-node bound in the small-Z case: the first near the outer layer, the second near the origin after resolving that layer. Their scripts, failed manifests and diagnostic logs are retained. They have no completed scientific-result JSON and are not evidence of a physical exclusion. The final log-radius coordinate and boundary/cutoff comparisons address those numerical obstructions without loosening the collocation threshold.

Earlier BBN exclusions were explicitly conditional on the adiabatic local Newton dictionary. This work makes that dictionary a load-bearing matching requirement; it does not alter the published abundance interval or retroactively refute the conditional algebra. The new diagnostic does not decide which dictionary applies to real laboratory sources or galaxies.

Next: solve the coupled weak-source ADM and scalar boundary problem in a common cosmological foliation, then determine whether a physical parameter regime makes the Newton calibration source-independent while preserving the cubic galaxy response. The coefficient-selection, microscopic, quantum and causal obligations remain open.
