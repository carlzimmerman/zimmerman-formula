# Higher-spatial-derivative MOND: explicit radiative protection test

No microscopic symmetry jointly selecting the vacuum and force amplitude has been established. This continuation tests a concrete proposed repair, rather than repeating the Galileon result already in symmetry_protection/GOLDSTONE.md. The new result is a finite-shell one-loop background calculation: a positive time kinetic and k^4 stabilizer do not by themselves protect a bare zero quadratic spatial coefficient in this MOND scalar EFT.

Kappa=1/2 remains FITTED; CFG493 kappa_Lambda=0.417 +/- 0.095 and kappa_crit=0.345 +/- 0.078 are separate and unused. No observed acceleration, vacuum density, tuning scan or numerical target enters the script.

## Candidate and its classical health

In a preferred frame, consider

    L=K dot(phi)^2/2-D(laplacian phi)^2/2-gamma |grad phi|^3/3-V,
    K,D,gamma>0.

This is a nonrelativistic EFT, not a completed AeST action or a microscopic quantum-gravity theory. Its coefficients are not identified numerically with the preceding AeST normalization. Baryonic sourcing may be supplied externally, but is switched off in this self-fluctuation calculation; no baryon-loop or full gravity claim is made.

For a nonzero constant background gradient grad phi=s n, |n|=1, s>0, the cubic spatial energy has Hessian

    H_ij=gamma s(delta_ij+n_i n_j).

Both eigenvalues gamma s (transverse) and 2gamma s (longitudinal) are positive. The exact quadratic frequency is

    omega(k,mu)^2=[D k^4+gamma s k^2(1+mu^2)]/K,
    mu=n dot k_hat.

It is positive. Thus the calculation starts with a classically healthy fluctuation sector at nonzero s, not the negative-time-kinetic P(X) branch previously excluded. This does not certify the quantum vacuum, nonlinear global solutions or a generally covariant completion.

## Finite-shell quantum calculation

Take a fixed spatial shell 0<kL<|k|<kU in this preferred frame and the canonical scalar measure. Its zero-point energy is

    Delta E(s)=(hbar/2) integral_shell d^n k/(2pi)^n omega(k,mu).

In general n, angular averages are <mu^2>=1/n and <mu^4>=3/[n(n+2)]. The constant, linear and quadratic terms in s have radial integrals proportional to k^(n+1), k^(n-1), and k^(n-3), respectively. Specializing to n=3 gives

    Delta E(s)=E0+A1 s+A2 s^2+O(s^3),
    E0=hbar sqrt(D/K)(kU^5-kL^5)/(20 pi^2),
    A1=hbar gamma(kU^3-kL^3)/(18 pi^2 sqrt(K D)),
    A2=-7 hbar gamma^2(kU-kL)/(120 pi^2 sqrt(K) D^(3/2)).

This is an exact Taylor coefficient calculation for the finite-shell one-loop determinant. The expansion requires gamma s/(D kL^2)<<1, including a harmless angular factor bounded by two. If the energy includes b s^2/2, the shell correction is

    Delta b=2A2=-7 hbar gamma^2(kU-kL)/(60 pi^2 sqrt(K) D^(3/2)),

which is nonzero. The new A1 |grad phi| operator is even lower order. Constant shifts and spatial rotations allow both operators. The proposed restricted bare operator set is therefore not closed under this formal one-loop shell operation. Setting b=0 at one scale is not sufficient protection in this model.

These coefficients are Wilsonian, cutoff dependent, and not universal observables. Counterterms and a full microscopic matching can change them. In particular, the negative isolated Delta b is not by itself a diagnosis of the fully renormalized vacuum, and E0 must not be identified with measured dark energy. The full effective response includes A1 as well; dropping it and asserting an exact lowest-gradient force would be unjustified.

There is another essential limitation: the bare |grad phi|^3 interaction is nonanalytic at zero gradient. Higher-loop expansions about s=0 need not be uniform. Semiclassical use of the background expansion additionally requires fluctuation gradients small compared with s. We have not established an all-orders s->0 limit or a complete RG flow. The result is a finite-shell one-loop diagnostic and demonstrates the absence of automatic protection by the stated symmetries, not impossibility of a new symmetry or ultraviolet completion.

## Why the known protective symmetry does not transfer

[Multicritical symmetry breaking, arXiv:1308.5967v2](https://arxiv.org/html/1308.5967v2) constructs higher-order dispersion with enhanced polynomial-shift protection in a free-field limit and analyzes interacting models. This supports the existence of a real protection mechanism, not its applicability to the MOND operator. The broader 1412.1046 source was found, but its HTML exceeded the tool's size limit; no detailed theorem from that inaccessible text is imported.

The incompatibility for the present operator follows directly. Restrict to a one-dimensional profile with phi'>0. Its cubic-gradient Euler expression, up to an overall sign, is

    E=partial_x[gamma(phi')^2]=2gamma phi' phi''.

Under the linear spatial shift phi->phi+epsilon x,

    Delta E=2gamma epsilon phi'',

which is generally nonzero. Therefore this interaction is not invariant even up to a boundary term under that subgroup of polynomial shifts. A proposed completion with additional transforming fields could change this conclusion, but its invariant action and Ward identity would need to be supplied. The calculation does not exclude all such completions.

Ordinary constant shift survives but allows b, gamma and V independently. A constant vacuum shift changes neither the fluctuation Hessian nor the force vertex. Nonrenormalization of some chosen coupling, where it holds in another theory, also does not by itself choose that coupling's boundary value or fix vacuum energy.

## Evidence and disposition

Frozen before the executable: 5b11740a2a. Twelve symbolic identities verify the Hessian, angular factors and shell integrals. A separate mutation removes the longitudinal anisotropic term; five baseline checks fail and the run exits nonzero. This tests the factors that determine the new coefficients, not a fitted target. No independent review, simulation, baryonic halo stability proof, microscopic symmetry construction or parameter-free a0 result is claimed.

The requested mechanism must cancel or forbid these lower-gradient contributions in its complete field content while keeping the MOND cubic and physical baryon source, and then constrain the independent vacuum term. This explicit higher-derivative model does not do that. A shell vacuum contribution and a force coefficient coming from the same integral is not enough: the shell scales and matching terms remain independent physical input until a microscopic theory selects them.
