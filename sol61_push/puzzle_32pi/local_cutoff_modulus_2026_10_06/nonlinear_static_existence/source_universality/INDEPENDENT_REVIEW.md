# Independent source-universality and force-series audit

**Primary verdict: proved as written within the declared fixed-parameter radial source class.** Two distinct self-similar compact spherical masses with finite positive Z,m and the same vacuum cutoff cannot have one exact exterior physical interpolation function at every common Newtonian acceleration y. The primary proof is an equation subtraction, not a formal series. The three-dimensional source-dependent force coefficient and its fixed-body remainder also agree after independent reconstruction.

## Frozen inputs and scope

Inspected final REPORT.md SHA256 `ad0e7794413f5d46f94f6d2a1555fef558aa86090ee5bf0ae22bc5dee45180db` and checks.py `f0f7c088fda50e8669d426d7d010826651f4337a697b7a1bf7d47722c014e4e3`. The parent nonlinear report is pinned at `7adb5d15a30e6843ead2b3180b0e7eeb4e3e2ed63824dc72c288c23cd20d13e1`; this peer previously reconstructed its positive source bounds, Green map, existence and finite-stiffness tail. Actual peer-inspection HEAD was `854004892cf7f9f80398b231b7ed8c1c7e7b9067`. Author scientific inputs are unmodified.

The hypotheses are n>=3, common positive a0,G_n,Z,m,kappa,T0, prescribed compact smooth spherical nonnegative source profiles related by the stated scaling, regular central physical flux, and positive bounded radial modulus solutions approaching T0. The parent's strict contraction regime supplies actual unique radial solutions for this entire family, independently of mass. Outside that sufficient regime the obstruction is conditional on the assumed positive radial solutions existing. Neither branch asserts matter equilibrium or full gravitational/causal health.

Exact universality means equality of g/gN throughout a shared exterior interval extending to infinity, equivalently all its common exterior y values. The claim is not about finitely many data points, a finite tolerance, or a restricted astrophysical mass sample.

## Independent exact rescaling proof

Normalize the radial density shape f by `Omega integral s^(n-1)f(s)ds=1`, and choose

`rho_i(r)=M_i rM_i^-n f(r/rM_i)`,

`rM_i=(G_n M_i/a0)^(1/(n-1))`.

At r=rM_i s its Newtonian field ratio is `y(s)=F_enclosed(s)/s^(n-1)`, independent of M_i. In the common exterior, `y=s^(-(n-1))>0`. No assumption of strict positivity of the density at the center is needed.

The actually varied physical potential equation gives

`r^(n-1)(Phi'-nu(y,T)Phi_N')=C_flux`.

Central regular flux without an added singular mass sets C_flux=0. Thus g/gN=nu(y,T) is the physical response, retaining the gradient-T contribution under the differential divergence. The cutoff dependence is strictly injective at every finite y>0 and T>0 because

`nu_T=2T y² b(y)/(T²+y²)²>0`.

A common response at the same exterior s must therefore give a common scaled modulus T(s). This inference does not require nu*(y) to be analytic, y(s) to be invertible inside the source, or injectivity at y=0.

The two scaled field equations are

`-Z rM_i^-2 Delta_s T+Zm²(T-T0)=kappa q_T(y(s),T)`.

For rM_1!=rM_2 their difference forces Delta_s T=0 in the common exterior. A radial harmonic function in n>=3 has `T=A+D s^(2-n)`; its decay boundary condition gives A=T0. The unsimplified modulus row then requires

`Zm²D s^(2-n)=kappa q_T(s^(-(n-1)),T0+D s^(2-n))`.

If D<0 the signs already contradict q_T>0. For D>=0, use the parent bound `q_T<=8y^(7/2)/(7T0³)`. More generally a positive bounded solution tending to T0 has T>=T0/2 far enough out, and the same estimate with that lower cutoff applies. Multiplication by s^(n-2) then gives a bounded left constant Zm²D and a right side tending to zero, since

`7(n-1)/2-(n-2)=(5n-3)/2>0`.

Thus D=0. The remaining equation is zero equal to kappa q_T(y,T0)>0, a contradiction. This exact exterior-only argument covers hollow smooth profiles and avoids any questionable central harmonic extension. It also makes clear why finite positive m matters: a massless harmonic displacement has a different operator balance and is outside this theorem.

For a profile with nonzero enclosed mass at every positive radius, the whole-space harmonic argument is also valid, but is not needed. The sufficient contraction condition is independent of rM, and uniqueness plus rotations gives the radial solutions. The obstruction is therefore instantiated among existing admitted static solutions, rather than merely a failure to find solutions numerically.

## Independent quantitative expansion: scalar field

In n=3 write y=(rM/r)², lambda=(m rM)^-2. From the exact kernel derivative, expansion at fixed T0 gives

`nu_T=T0^-3[2y^(3/2)-2y²+y^(5/2)+O(y^(7/2))]`.

Integrating `q_T,y=2y nu_T` yields

`q_T(y,T0)=T0^-3[(8/7)y^(7/2)-y^4+(4/9)y^(9/2)+O(y^(11/2))]`.

The absence of a y^5 term follows from the explicit square-root/denominator expansion; it is not an arbitrary truncation. The known nonlinear solution obeys u=T-T0=O(y^(7/2)). The mean-value derivative bound at small y gives

`q_T(y,T0+u)-q_T(y,T0)=O(y^(7/2)u)=O(y^7)`.

Thus nonlinear feedback is beyond the displayed first three source powers at finite fixed Z.

For the radial three-dimensional operator, `Delta r^-j=j(j-1)r^(-j-2)`. The leading y^(7/2) field term produces a derivative correction at y^(9/2), with multiplier42 lambda; `42*(8/7)=48`. Consequently

`u=kappa/(Zm²T0³)[(8/7)y^(7/2)-y^4+(4/9+48lambda)y^(9/2)+O(y^5)]`.

The sign of the derivative correction is positive: inversion of m²-Delta adds Delta(source)/m^4 at this order.

The remainder is justified rather than only guessed. Smoothly cut off this trial field inside an exterior radius. Its linear massive-operator residual matches the actual fixed-T0 source through r^-9. The next uncancelled derivative term from r^-8 is O(r^-10), while the direct source remainder is O(r^-11) and nonlinear feedback O(r^-14). Therefore the difference from the trial solves the linear massive equation with a bounded O(r^-10) forcing plus compact terms. The positive Green kernel bounds its absolute convolution: displacements <=r/2 retain the O(r^-10) bound, while displacements >r/2 are exponentially small using the global forcing bound and the parent's exponential Green moment. A decaying homogeneous difference is zero. This proves the stated O(y^5) remainder for each fixed body and fixed positive parameters. No expansion in 1/Z or derivative assumption about the unknown remainder is needed.

## Actual force coefficient and source dependence

The physical cutoff correction relative to the same constant-T0 kernel is

`delta g=a0 y[nu(y,T0+u)-nu(y,T0)]`.

At first order in the small far-field displacement use a0 y nu_T u. The quadratic Taylor contribution is O(y^(19/2)), since nu_TT=O(y^(3/2)) and u²=O(y^7). Multiplying the independently reconstructed series gives

`delta g=kappa a0/(Zm²T0^6)[(16/7)y^6-(30/7)y^(13/2)+(254/63+96lambda)y^7+O(y^(15/2))]`.

The universal part of the y^7 coefficient is `8/9+2+8/7=254/63`; the source-size part is `2*48lambda=96lambda`. The field remainder O(y^5) makes a force error O(y^(15/2)), dominating the smaller quadratic-displacement remainder. The coefficient has acceleration dimensions; lambda is dimensionless. The correction is to inward magnitude, with opposite sign in the outward signed radial acceleration.

For two fixed distinct masses the shared constant-T0 force cancels, and the earlier y^6 and y^(13/2) correction coefficients cancel as well. Therefore

`g1-g2=96kappa a0/(Zm²T0^6)(lambda1-lambda2)y^7+O(y^(15/2))`.

In n=3, `lambda=a0/(m²G_n M)`, so the smaller mass has the larger far-field correction at this order. The source-dependent term lies at y^7 in force, or y^6 in g/gN after dividing by a0 y. The statement is a fixed-two-body, y approaching zero asymptotic. Its constants are not uniform as M approaches zero, m approaches zero, or the source/body scale is taken to infinity; r must be beyond the body and the Compton length, with u<<T0. Compact-profile influence does not change these power coefficients, but can change subleading exponential terms and nonasymptotic response.

## Evidence and interpretation audit

The 18 exact checks reconstruct algebraic source normalization, exterior scaling, radial powers, derivative/source series and the force product. The explicit polynomial compact profile in the code is used only for a mass-normalization algebra check; it is not a claimed C-infinity source/PDE solution. The universal smooth-source theorem uses the independently specified admissible family. The symbolic n check corroborates an identity; positivity of its exponent uses the stated n>=3 hypothesis analytically.

The controls reject false candidate statements: dropping the radius-gradient difference, calling a nonzero harmonic displacement a massive sourced solution, and asserting that the computed force coefficient has zero lambda derivative. These are direct equation/derivative contradictions, not numerical PDE or observational tests. All four runner manifests validate final input and output hashes. No author input or parent evidence was modified by this peer.

The exact obstruction needs no series and makes no statement about approximate observational universality. Taking a local heavy-modulus approximation removes the radius-dependent Laplacian and can give an approximately common response; externally fixing T or changing Z,m by source changes the hypotheses. Within the finite common-parameter theory, the extra material length scale prevents an exact source-universal kernel. This also blocks automatically assigning one varying-source response a single vacuum moment C: the constant-T0 moment is a separate defined mathematical object, and a covariant vacuum dictionary remains unproved. No measured violation, cold abundance or 32pi selector is established.

Passed: action-to-force flux, equal-y injectivity, general-n exterior contradiction, actual-solution coverage, small-y coefficients, finite-parameter remainder argument, source-dependent force coefficient and computation scope. No blocking gap remains in the stated claim.
