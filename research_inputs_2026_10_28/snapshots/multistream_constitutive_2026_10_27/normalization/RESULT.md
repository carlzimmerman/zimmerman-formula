# MC27 normalization: exact elimination constraints and the missing reservoir identity

2026-10-27. Requested base: 4aea352e6b. Observed HEAD while reading: 86220bf0b31740b723174cdefb0663eadbcc30c5. Writes are confined to this directory. This is a self-reviewed analytic investigation with one bounded check, not an independent referee review or a halo simulation.

**User target remains incomplete.** A general positive-affine-kinetic elimination theorem rules out obtaining the pure logotropic internal energy by this route, including its finite-temperature and finite-dimensional quantum versions. The pressure-invisible density-linear term creates a genuine restricted-branch exception; an explicit witness below prevents overstating the obstruction. Neither that exception nor a loop logarithm fixes the coefficient relative to the physical vacuum. The exact missing normalization is a state-selection or transfer identity, with a physical vacuum definition and a fixed phase-space measure.

## 1. General elimination theorem

Let K be canonical random kinetic energy density and s an internal state in a K-independent admissible set. Assume b(s)=1/Akin(s)>0 and

    W(K) = inf_s { b(s) K + U(s) }

is finite on an interval. No particular polynomial potential is assumed.

**Claim, proved under these hypotheses:** W is nondecreasing and concave in K. For K2>K1 every affine branch increases, hence its infimum cannot decrease. For 0<t<1,

    W(t K1+(1-t) K2)
      = inf_s [t (b_s K1+U_s)+(1-t)(b_s K2+U_s)]
      >= t W(K1)+(1-t) W(K2).

Where W is differentiable and the minimum is attained smoothly, W'=b(s*)>0; where twice differentiable, W''<=0. The inequalities remain meaningful at branch transitions. Strict monotonicity is not asserted for an unattained infimum with b approaching zero.

Thus the pressure-normalized pure logotropic energy,

    u_log(rho) = -A [ln(rho/rho_ref)+1],    A>0,

cannot equal W along K=k rho^(5/3): it has W'=-3A/(5K)<0 and W''=3A/(5K^2)>0. Adding a constant vacuum offset does not change either violation. This is stronger than the earlier quartic example.

The density relation is a specified canonical affine family, x->b x and p-pbar->(p-pbar)/b, with k fixed. It is not a universal kinetic closure. Different multistream states at the same density need not have the same K.

### Thermal and quantum internal modes do not automatically evade the theorem

For a convergent classical partition integral in a fixed cell volume V, with fixed state measure and temperature T,

    F_T(K)=-(T/V) ln integral ds exp[-V(b(s)K+U(s))/T],
    F_T'= <b> >=0,    F_T''= -(V/T) Var(b) <=0.

Temperature is in energy units. This is a free energy at fixed T, not the adiabatic internal energy. Allowing T or the state measure to depend on density changes the problem and introduces additional state-selection data.

For a finite-dimensional quantum internal Hamiltonian H(K)=H0+K B with B positive semidefinite, the ground energy density is the infimum of affine expectation values divided by V over a K-independent set of normalized states. It obeys the same inequalities. For the quantum thermal free energy density F=-(T/V) ln Tr exp(-H/T), F'=Tr(varrho B)/V>=0 and

    F''= -1/(V T) integral_0^1 dt
          Tr[varrho^t deltaB varrho^(1-t) deltaB] <=0,
    deltaB=B-Tr(varrho B).

The sign follows directly in an eigenbasis of the positive density matrix: the integrand is a sum of positive weights times |deltaB_ij|^2. Commutation of H0 and B is unnecessary.

A stable Gaussian determinant with positive affine stiffness is a special case: its log is increasing and concave. The occurrence of a logarithm does not supply the negative, convex logotropic internal energy. A continuum quantum field, density-dependent regulator/state counting, non-affine coupling, or a renormalized subtraction outside these assumptions requires its own derivation; this result does not exclude those theories.

## 2. Essential exception: pressure does not fix density-linear energy

It would be incorrect to promote section 1 into a no-go for every logotropic pressure. Put r=3/5 and Kref=k rho_ref^(5/3). Solving the pressure equation

    P=(5/3) K W' - W = A ln(rho/rho_ref)

gives the full family

    W(K)=B K^r - r A ln(K/Kref) - A,
    B K^r = c rho.

The term c rho has zero pressure. Whether it is a specified rest-energy term, a generated energy term, or inadmissible in the chosen reduced Hamiltonian must be decided from that Hamiltonian; it cannot simply be discarded when claiming an obstruction.

The envelope conditions become

    W'  = r [B K^r-A]/K,
    W'' = r [A-(1-r)B K^r]/K^2.

For B>0 they both hold on a high-density branch when

    B K^(3/5) >= (5/2) A.

They cannot hold for this exact logotropic form all the way to K=0. That leaves a mathematically viable active-phase route, conditional on its energy term, phase boundary, and state selection.

### Exact restricted witness, deliberately inverse-designed

In dimensionless units define for s>=1

    f(s)=(8/3)s^(3/5)-(3/5)ln s-1,
    b(s)=f'(s)=(3/5)[(8/3)s^(3/5)-1]/s >0,
    U(s)=f(s)-s f'(s),
    W(K)=inf_{s>=1}[b(s)K+U(s)].

Here f''<0 on s>=1. Differentiation of the minimized expression gives f''(s)(K-s), so the unique minimizer is s=max(1,K). Therefore

    W(K)=K+2/3                        for 0<=K<=1,
    W(K)=(8/3)K^(3/5)-(3/5)ln K-1    for K>=1.

Along K=rho^(5/3), the active pressure is exactly P=ln rho. The inactive pressure is 2K/3-2/3. Akin=1/b is positive, the energy is continuously differentiable at activation, and U is bounded below on the stated domain.

This is a counterexample to an unrestricted pressure no-go, not an explanation of the log law. The logarithm and its normalization were placed into b and U by inverse design. It gives no cold-field derivation, phase selection, vacuum coefficient, or global dynamical stability theorem.

## 3. What a vacuum-normalization identity must actually constrain

Let Vphys be the gravitating vacuum energy density and A the pressure coefficient, measured for the selected material state. The target is R=A/Vphys=1/(4 pi xi_quarter^2), with the adopted quarter-density core convention.

If an independent additive vacuum term C is allowed, the local fixed-background constitutive elimination obeys

    W_C=W+C,    P_C=P-C,
    dP_C/d ln rho = dP/d ln rho,
    A_C=A,    Vphys,C=Vphys+C,
    d/dC [A/(Vphys+C)] = -A/(Vphys+C)^2.

This is an exact response identity, not merely a parameter-counting complaint. It says which missing relation a shared-origin mechanism must overcome. It compares the local material response at fixed state; a full cosmological solution may change when the vacuum changes and must be recomputed if that state is claimed to select A.

A genuine parameter-independent ratio R=R* requires, for every allowed physical deformation delta at the selected state,

    delta A - R* delta Vphys = 0,

and one reference value fixing the integration constant. A scale identity alone is weaker. If A=M^4 a(g) and Vphys=M^4 v(g), scale covariance removes M but leaves a(g)/v(g). More generally an exactly homogeneous energy with density dimension d obeys

    M partial_M e = 4 e - d rho partial_rho e

when all other scales are held in their specified homogeneous ratios. This identity does not constrain independent dimensionless couplings g.

### The new two-measure work passes a shared-origin identity but fails this stronger test

The checked local record, reviews/action_first_measure_test_2026_10_27/RESULT.md, lines 34-44 and 58-101, supplies the regular Einstein-frame action and an original-action kinetic deformation. Its coefficients obey

    U=A0^2/(4D), Z=1-A0 Delta/(2D), B2=-Delta^2/(4D),
    4 U B2+(1-Z)^2=0.

After canonical normalization, however,

    J=U B2/Z^2=-A0^2 Delta^2/[4(2D-A0 Delta)^2],
    dJ/dDelta=-A0^2 D Delta/(2D-A0 Delta)^3.

The displayed symmetry-preserving change of bphi changes Delta at fixed U and Einstein coupling on a regular positive-kinetic branch. Our bounded check independently recomputes this derivative. For A0=D=1, Delta=0.25,0.5,0.75, U remains 0.25 while J becomes -0.00510204, -0.0277778, -0.09.

J is a scalar response invariant, not yet the logotropic A. Consequently this is an adjacent normalization obstruction, not a proof that an unconstructed multistream A must vary identically. It establishes that the cited common denominator/identity alone cannot select physical response normalization. The source still lacks the action-to-multistream-pressure map. We do not repeat its separate MOND cubic analysis or extend its claim to all two-measure theories.

## 4. The near-matching relaxation coefficient still needs two physical maps

The parallel relaxation route reports a conditional broad-level result

    A = 2 K / [3 ln(eta_max/eta_min)].

Taking that conditional formula as input, setting K=Vphys and eta_max/eta_min=rho_Planck/rho_Lambda would give 2/[3 ln(rho_Planck/rho_Lambda)]. Numerical proximity to the target does not derive either equality.

First, kinetic and vacuum energy have different stresses. Isotropic nonrelativistic random energy has Pkin=2K/3; an exact vacuum has Pvac=-Vphys. K=Vphys can compare distinct coupled reservoirs but cannot identify their stress tensors. For a collisionless distribution with isotropic stress, the random-energy moment is

    D K/Dt + (5/3) K div u + div q = Q_K,

where q is the third central-moment energy flux and Q_K contains actual noncollisionless exchange/heating. Mean-flow compression is already represented on the left. In a static core this imposes Q_K=div q, not K=Vphys. A cooling/outgoing-wave rate, an accretion source, or a common thermal reservoir must be derived before equality of their steady energies follows. A box-averaged K also needs a bridge to a local core coefficient.

Second, eta is a phase-space density, not mass density. Both ratios above are dimensionless, so their identification is not a units error, but it is an unproved physical map. For similar-shaped velocity populations,

    eta_high/eta_low ~ (rho_high/rho_low) (sigma_low/sigma_high)^3.

The velocity-volume factors and the distribution shapes matter. The Vlasov phase-level data are set by the initial distribution/Casimirs and can change with primordial dispersion at fixed physical vacuum. A density ratio alone does not specify that information. The actual definitions and applicability of the relaxation formula remain with its own route.

The coordinator's separate conditional diffusion-tail formula A=F/(30 D0) exposes a different precise normalization obligation:

    F/(D0 Vphys) = 30 R*.

A nonzero stationary velocity-space flux F requires a source and sink/boundary flux. For regular finite f at v=0 with D=D0 v^4, the flux -4 pi v^2 D f_v vanishes at the origin; a nonzero constant-flux branch therefore cannot by itself be a source-free, closed stationary distribution over all velocities. A cutoff and forcing model must select F/D0. The bare vacuum-shift identity does not provide that selection.

## 5. Primary-source checks and their limits

The source checks are recorded separately in SOURCES.md. No external theorem is needed for the elementary envelope proof or the explicit witness.

- Weinberg's primary one-loop calculation exhibits field-dependent prefactors and renormalization conditions multiplying logarithms. It supplies no vacuum-to-logotropic-pressure normalization.
- Chavanis's complex-scalar model starts with a logarithmic potential. Its identification of a density reference with Planck density is an additional premise in its cosmological normalization, and its density is a pseudo rest density in the relativistic field formulation. It is not a derivation from multistream mixing.
- The two-measure original reduction is inherited from the pinned local source record; its primary PDF could not be refetched in this session. The normalization algebra was checked directly, but the full original reduction was not independently rederived.

## 6. Bounded discriminant and disposition

check_normalization.py and contract.json were frozen before execution. The run completed in about 1.5 seconds under a 10-second wall limit, 8-second CPU limit, and one-thread limit. run/manifest.json passed the mathbox validator.

It verifies exact reconstruction identities, the explicit positive-kinetic witness at seven K values, three classical thermal derivative checks, ground/thermal concavity on a 51-point noncommuting two-state quantum example, the additive-vacuum derivative, and the two-measure invariant derivative. The largest witness energy discrepancy is 6.05e-10 on the stated scaled measure. The pure-log midpoint gap is -0.0863046, with concavity requiring a nonnegative value.

The general conclusion rests on the written proof; these finite examples are discriminants and implementation checks, not an exhaustive classification. There is no long simulation, parameter fit, or new shared-file edit.

**Cheapest next physical discriminator:** select one explicit energy-exchange/initial-state parent and test whether its allowed fixed-vacuum deformation changes either the selected K or the occupied phase-level span. If it does, the near-matching broad-level coefficient remains a state-dependent result. To succeed, that parent must derive both maps and preserve the exact amplitude under its allowed deformations. No such parent was found here.
