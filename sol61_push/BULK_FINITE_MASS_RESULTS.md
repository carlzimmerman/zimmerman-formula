# Finite-mass bulk response and formal far field — 2026-09-30

**Original goal OPEN:** derive a0=c² sqrt(Lambda/(32pi)) from one physical mechanism/action, not a fitted normalization. In c=1 units this is Lambda/a0²=32pi. A complete gravity theory additionally needs consistent dynamics, cosmology and successful observations. The following advances the spatial-response obligation; it does not fix the vacuum coefficient.

Base `ea962ad3a`. [Contract](BULK_FINITE_MASS_CONTRACT.md). Existing core files remain read-only; all new work is under sol61_push.

## 1. The finite-mass kernel is now calculated

Retain the declared isotropic three-dimensional eight-band Hamiltonian with three momentum Clifford matrices and three internal mass matrices. At uniform polarization P n, mass m=yP>0, its dispersion is

    E(k,m) = sqrt(k³/mu + m²),   mu>0.

The trace dimension is d=8 and there are nu=4 occupied negative-energy bands per flavor. The homogeneous finite fermion energy is nu mu |m|³/(9pi²), after the explicit analytic subtractions from the previous run. This is still a nonlocal spatial spectral model without a causal ultraviolet completion.

Take static perturbations of the mass triplet. “Longitudinal” here means parallel to the **internal background polarization**, not necessarily parallel to spatial wavevector q; “transverse” means perpendicular in that internal space. Integrating frequency exactly, define d_k=k sqrt(k/mu), E=sqrt(|d_k|²+m²), F=sqrt(|d_(k+q)|²+m²). After symmetric subtraction of q=0 curvature,

    DeltaPi_T = (d y²/2) integral d³k/(2pi)³ S_T,
    S_T = |d_k-d_(k+q)|² / [2EF(E+F)],
    S_L = S_T + 2m²[1/(EF(E+F))-(1/E³+1/F³)/4].

DeltaPi_L uses S_L with the same prefactor. The transverse integrand is nonnegative. For numerical stability the longitudinal difference is evaluated as

    1/(EF(E+F))-(1/E³+1/F³)/4
      = -(E-F)²(E²+3EF+F²)/[4E³F³(E+F)].

This avoids subtraction of large nearly equal terms. The longitudinal integrand need not be nonnegative pointwise; its integrated correction is positive at all tested q. No universal all-momentum sign theorem is claimed from those six values.

## 2. Exact small-momentum coefficients

For q much smaller than k0=(mu m²)^(1/3), the two static kernels have leading terms

    DeltaPi_T = C_T mu^(1/3)m^(-1/3)y² q² + higher orders,
    DeltaPi_L = C_L mu^(1/3)m^(-1/3)y² q² + higher orders,

where the fermion-loop coefficients are

    C_T = 17d B(4/3,1/6)/(576pi²),
    C_L = 43d B(4/3,1/6)/(1728pi²),
    C_L/C_T = 43/51.

At d=8, C_T approximately 0.134177931116 and C_L approximately 0.113130412510, both positive. B is the Euler beta function. This exact ratio is a property of the specified loop; it is **not** Lambda/a0² or a physical universal constant. Independent bare derivative operators, interactions or a different spectrum can change the complete response.

The derivation retains the radial integrals. For z=3/2,

    integral_0^infinity k³ dk/(1+k³)^(3/2) = B(4/3,1/6)/3,
    integral_0^infinity k⁶ dk/(1+k³)^(7/2) = B(7/3,7/6)/3.

Expanding the transverse integrand gives the first integral with angular factor (z²+2)/3=17/12. The longitudinal correction follows from the convolution of f(k,omega)=1/(omega²+E²): its q² difference is minus the integral of (partial_kz f)². The exact frequency integral is 5/(32E⁷), giving a subtraction 5d B(7/3,7/6)/(64pi²). The recurrence B(7/3,7/6)/B(4/3,1/6)=8/135 then produces 43/51. Two independent one-dimensional quadratures check the radial beta integrals.

Full momentum/angular quadratures test q=0.03,0.1,0.3,1,3,10 at m=mu=y=1, using orders 256,512,1024. Each last refinement passes the predeclared relative tolerance 2e-4, and both integrated corrections are positive at every tested q. At q=0.03 they agree with the analytic small-q expressions within the predeclared 1e-3 tolerance. Independent m=0.25 and m=4 calculations also reproduce the full-kernel scaling mu m times a function of q/(mu m²)^(1/3). These are bounded numerical checks, not a nonuniform determinant or covariant health proof.

## 3. Construct and vary the leading derivative energy

For the loop contribution, internal rotational invariance organizes the leading two-derivative energy into magnitude and direction terms:

    E_grad = [mu^(1/3)y^(5/3)/2] P^(-1/3)
             [C_L |grad P|² + C_T P² |grad n|²],   n dot n=1.

Use the same static gravitational normalization W=4pi G E for this contribution. Define K=4pi G mu^(1/3)y^(5/3). For a radial hedgehog n=rhat, partial_i n_j=(delta_ij-n_i n_j)/r. Squaring and tracing the rank-two tangent projector gives |grad n|²=2/r². The radial variational induction is

    f_grad = K [ C_L P'^2/(6P^(4/3))
                 -2C_L P'/(rP^(1/3)) - C_L P''/P^(1/3)
                 +5C_T P^(2/3)/(3r²) ].

An independent Euler variation of the radial energy gives that expression exactly. Substituting the leading P=A/r gives

    f_grad = D A^(2/3)/r^(8/3),
    D = K(C_L/6 + 5C_T/3) > 0.

Both magnitude and directional stiffness matter. Dropping the angular term would give the wrong coefficient. With the loop ratio, D=K C_T (553/306).

The declared constitutive equation is g=P+P²/a0+f_grad, and spherical Gauss law fixes g-P=GM/r². Its **formal leading-gradient asymptotic branch** is

    P(r) = A/r - D a0/[2A^(1/3) r^(5/3)] + higher orders,
    A = sqrt(GM a0),
    g(r) = GM/r² + P(r).

Direct substitution cancels the residual at order r^(-8/3); the next residual is bounded at order r^(-10/3). Thus the leading MOND amplitude can survive these finite-mass gradient corrections, with a calculable subleading term. This differs from the prior massless |grad| point-source toy, whose spatial term stayed at the same radial order as the cubic response and changed the leading mass relation.

The gap hierarchy is consistent with examining a derivative expansion in the far field:

    q/k0 ~ [mu y² A²]^(-1/3) r^(-1/3) -> 0.

This is not a proof that the full nonuniform determinant has this solution. It is a formal asymptotic result for the constructed leading derivative energy on the positive-P branch at sufficiently large r. The total system still needs finite boundaries, formation dynamics, an error-controlled derivative expansion and perturbation analysis. The prescribed internal hedgehog is not a demonstrated outcome of the original passing stream. Finite regular bare gradient terms would also need to be included; no full-action universality claim follows from the loop ratio.

## 4. The critical and vacuum gaps remain separate

The local MOND branch still assumes that the quadratic polarization susceptibility cancels the ordinary linear induction. A nonzero positive detuning restores a linear low-field response, as the previous calculation showed. The cubic fermion determinant requires an analytic quadratic counterterm. The spectral model does not set its finite part.

A narrow exact obstruction to symmetry protection is now recorded: any linear internal transformation preserving |p|³ also preserves |p|², because equality of nonnegative cubic norms implies equality of the norms. Ordinary rotations or internal norm-preserving symmetries therefore allow the quadratic term as well. This excludes only that protection argument. Scale symmetries, nonlinear symmetries, constrained variables or dynamical selection of a critical state require separate examination.

The same calculation still allows an independent absolute vacuum constant. Neither the ratio 43/51, the cubic energy coefficient nor the formal far-field amplitude selects it. The original 32pi goal remains unresolved.

## 5. Reproducibility and retained correction

Principal bounded runs:

- `runs/bulk_finite_mass_response`: 23/23 checks.
- `runs/bulk_far_field_real_domain`: 15/15 checks.

Both scripts, contracts, results and raw output are retained. An initial far-field run, `runs/bulk_far_field`, passed 13/14 checks. Its failed test used a generic symbolic solver that returned two complex roots despite the intended nonnegative norm domain. The corrected script explicitly tests the positive real domain and the zero-norm case separately; it preserves the original mathematical claim and does not loosen a tolerance. The initial script and failed run are retained unchanged.

These **38 principal checks** support the scoped derivations. They do not establish full theory health, a completed galaxy solution, global novelty or the coefficient 32pi.

Next discriminators: an explicit mechanism protecting or selecting the critical quadratic cancellation, and an error-controlled nonuniform calculation. Absolute covariant vacuum stress must eventually be obtained from that same completed action/state; choosing it to satisfy the target does not count.
