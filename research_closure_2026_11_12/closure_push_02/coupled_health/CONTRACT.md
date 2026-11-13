# CP02 coupled scalar-health contract

Base checkpoint: `2207a1df48348f01ca1084d4add5d214c55d0e7e`. Owner: HY4 review agent. Exclusive write scope: this directory. No changes to historical results or other owners' work.

Target: derive the physical scalar quadratic/principal dynamics of QX17 with `H(Q,Pi)=F(Q)S(Pi/Pic)`, including Einstein lapse, shift and spatial-metric constraints. Carry nonzero gate derivatives at FRW, active positive-Pi stiffness at finite density, and test a finite-density state satisfying the background constraints. A bad polarization subblock alone does not satisfy this target.

Conventions: signature (-,+,+,+), c=1, K=4*pi*G>0, M2=1/(2K), F=C(Q-1)^2, C>0; W(|P|)=a0²/K[-K|P|/a0-ln(1-K|P|/a0)], K|P|<a0. Stiffness is gamma*Pi_+²/2, gamma>=0. The positive branch is smooth only at Pi>0. At FRW Pi=0, either gamma=0 or an explicitly smooth/blended stiffness is required for a single quadratic Hessian.

Routes and discriminators:

1. Exact flat-FRW ADM reduction. Derive the quadratic action and solve shift/lapse/P constraints; check against unreduced equations. Determine what survives the earlier fixed-metric argument. Do not call positive curvature-variable gradient coefficient absence of cosmological Jeans growth.
2. Finite-density constrained data. Solve the spherical Hamiltonian, momentum and P constraints with a spatially constant lapse. At a regular center derive the large-k physical scalar dispersion and test active-stiffness examples on both sides of its health inequality. A local constrained initial-data construction is stronger than arbitrary jets but is not a global galaxy or a nonlinear existence/stability theorem.
3. Compare the Legendre/Hamiltonian reduction. Distinguish positivity of the fixed-charge P block from positivity of the fully reduced scalar Hamiltonian. Characterize surviving principal conditions even after constructing an unhealthy state.

Success criteria: explicit constraint-eliminated scalar coefficients; direct-action/constraint cross-checks; a genuine constrained finite-density witness with an unbounded physical growth rate or a healthy-principal region; mutations that change load-bearing terms and fail the checks; commands, environment and input/output hashes. Partial scope must remain explicit. No fitted Pi_c, selected cutoff, all-background theorem or observational fit may be inferred from illustrative numerical values.

Source anchors: QX17 operative Legendre action; corrected PIK1 quadratic variation; TPA1 health; SCS1/SCS3 approximations. SCS1 drops shift/momentum constraints and cannot certify the present full ADM calculation.
