# Independent FGF034 constrained-branch and susceptibility audit

**Verdict: proved as written under the stated smooth-base and full-coercivity hypotheses.** The argument establishes an actual local fixed-mass, fixed-field-wall branch and its full fluid/field susceptibility. It does not merely differentiate a proposed equilibrium family. No global autonomous equilibrium or physical driver potential is supplied.

## Independence and scope

The auditor independently froze FROZEN_CONSTRAINED_BRANCH.md at 2026-09-30T14:33:55.077947+00:00 using task034 and pinned023/033 before receiving any new formula preview or reading the new worker/root proofs. The worker DERIVATION and final result were then read and audited. No new stage20 root proof or other audit was read. The independent route uses the same explicit H2 Dirichlet-to-L2 nonlinear mapping, exact fluid minimization and strong inverse bootstrap. No mathematical program, numerical integration, symbolic computation or spectrum was executed. File-hash checks are administrative provenance, not experimental evidence.

The hypotheses are one actual smooth positive-gradient, positive-density Q equilibrium on a fixed finite physical interval, fixed total mass, fixed phi/chi endpoint values and physical coefficients, and the exact full Q0 bounded and coercive on H1_0 triples after fixed unit scalings. The derivative theorem does not apply automatically at a zero or negative full fixed-reference mode. No endpoint flux or fixed endpoint pressure is added to the declared wall conditions.

## Density normalization and the full constraint domain

Hydrostatic equilibrium with the isothermal closure integrates exactly to rho=M exp(-phi/cs²)/Z. Differentiating the denominator gives

 delta rho=-(rho/cs²)(psi-mean_rho psi),
 mean_rho psi=(integral rho psi)/M.

Its ordinary integral is zero. This weighted-mean term is required, not an optional gauge convention. For smooth positive base rho, the map xi -> -(rho xi)' is a bounded bijection from H1_0 to zero-integral L2. The displayed inverse xi=-rho^-1 integral_0^x delta rho is in H1, and its right trace vanishes exactly when the density variation integrates to zero. Both directions of the bounded map use the positive lower bound on rho and bounded rho'. This establishes the material representation of the branch derivative and prevents an untracked mass mode.

## Nonlinear mapping and inverse, not a formal Hessian inference

Use affine field corrections in X=(H2 intersect H1_0)^2 and residuals in Y=L2^2. The original positive-gradient base gives an X-open neighborhood with phi'>gmin/2 because one-dimensional H2 controls C1. Exponential normalization stays positive, and the Q inverse b(phi',a_c exp(chi+lambda)) has smooth derivatives on the resulting compact positive region. The H1 algebra and composition bounds make the differentiated flux and nonlocal density C1 into L2. Thus the claimed nonlinear map is genuinely Frechet differentiable in the spaces needed for the inverse argument. It is not asserted on bare H1.

The derivative has first component delta rho-(A psi'-q eta)'/C and second component (-J eta''+m eta-q psi')/C. Its symmetric weak quadratic form contains the exact negative variance term

 -integral rho(psi-mean_rho psi)^2/cs².

Minimizing the original full fluid expression cs² r²/rho+2r psi over all zero-integral r produces exactly this term and the normalized density derivative. The minimizer is realized by the admissible displacement above. Hence Qred=Q0(xi_psi,psi,eta) inherits an H1 coercivity bound for the field pair. The full fluid response has been retained; setting r=0 would produce a different derivative and susceptibility.

For each L2 forcing, the coercive symmetric form gives a unique H1_0 weak solution. The worker correctly supplies the missing regularity step: the second equation yields eta'' in L2; the first yields (A psi'-q eta)' in L2. Since the flux itself is L2 and A,q are W1,infinity with A bounded below, division by A then gives psi' in H1. Both fields are H2, with a bounded H2 estimate controlled by the L2 forcing and the base coefficient/coercivity constants. Thus the derivative is a bounded isomorphism X to Y, not merely injective or formally elliptic. Dirichlet values impose no extra forcing-integral condition because fluxes are free to adjust.

The subsequent contraction argument is valid: the derivative of y-Lred^-1 F at the base is zero; C1 continuity makes it a strict contraction on a sufficiently small ball, and small parameter variation keeps the center inside the self-map margin. Invertibility persists locally, and difference quotients give a continuous lambda derivative. This proves a unique nearby C1 branch in X with identical endpoints and mass. Positive density follows from the normalization with a locally uniform lower bound; positive gradient follows from the C1 control. The neighborhood is existential, not numerically sized. It does not connect the two registered reference normalizations or give global continuation.

## Full response and susceptibility signs

Let s=T_chi=2T-gq and ell[v]=-integral(q psi_v'+s eta_v)/C. Explicit parameter differentiation of the actual nonlinear map gives F_lambda=(q'/C,-s/C). Pairing this with zero-trace field tests is exactly ell; the q integration by parts has no endpoint term. The fluid equation of the full weak inverse enforces the same normalized minimizing density, so the reduced branch derivative lifts to the full H1_0 triple. Uniqueness then yields

 a0(u_lambda,v)=-ell[v], u_lambda=-z,
 a0(z,v)=ell[v].

This includes the material component of z. Substituting a field-only inverse with frozen density would miss it.

For R(lambda)=integral T/C on this constrained branch,

 R'=integral s/C+integral(q phi_lambda'+s chi_lambda)/C
    =integral s/C-ell[u_lambda]
    =integral s/C+beta, beta=ell[z]=Q0[z]>=0.

All signs and C factors match direct differentiation. Positive beta does not imply R'>0 because s can have either sign. Physical units remain fixed: lambda is dimensionless, and R and R' have energy-per-area units.

At an actual intersection of one independently supplied V with V'=R, the prior full Schur margin is exactly Delta=V''-R'. This is not an existence assertion for an intersection and does not select V or its derivatives. A zero margin gives the prior linear neutral direction under its hypotheses; it is insufficient to establish a fold, hysteresis or nonlinear stability. Local persistence of Q0 coercivity is justified because the H2 branch makes rho, rho', and constitutive form coefficients continuous in the bounded norms controlling the H1 form.

## Old-IVP negative control and boundary terms

The old fixed-left-IVP family generally changes mass and right field values. Its density derivative gains rho M'/M, and the reconstructed displacement has right trace -M'/rho(D). Its phi and chi derivatives also need not have zero right traces. It therefore generally lies outside the domain of the present weak inverse; the old computation itself is not thereby erroneous.

The energy check keeps the omitted terms explicitly. On a varying-boundary/mass local equilibrium family at fixed D,

 Epot'=h M'+[B phi_lambda+J chi' chi_lambda]_0^D/C-R,
 h=e'(rho)+phi.

Hydrostatic h is constant in x, and field integration by parts gives exactly the displayed boundary signs. Only on the new constrained branch do all mass/boundary terms vanish. Discarding their derivatives on the old family would yield the wrong curvature/susceptibility comparison. Likewise the constrained MOND source difference obeys delta B(D)-delta B(0)=0, whereas the old mass-varying family gives C M'. Neither statement fixes each endpoint flux separately. The dynamic source, if needed, remains P_x=C rho+tau phi_tt.

## Provenance and remaining physical implication

All11 final worker input pins and3 artifact pins match current files. The final proof-only result accurately declares no computation or numerical manifest. Exact reviewed and independently frozen source hashes are listed below. No mathematical gap was found within the stated regularity/coercivity domain.

This is a local Q diagnostic theorem. It supplies no independently justified V, actual enlarged-model equilibrium, calibrated parameter, local covariant sector, scale-vacuum identification, metric/photon coupling or required gravitational degree count. Both a0 choices are separate base hypotheses; frozen H references and evolving H histories remain distinct. No RAR or registered M action, operative filtered-MONO transfer, force/mass estimate, observational evidence, global branch or theory closure follows.

The local constrained-response gate is closed under its assumptions. A further global-equilibrium or stability calculation requires an independently specified physical potential and an actual intersection, not fitted desired derivatives or substitution of the old IVP response.

## Exact pins

- `campaign_fresh_gravity_astra/stage_20/independent_audit/FROZEN_CONSTRAINED_BRANCH.md`: `b930bda2e261a396e53d0a14d70eac74bcc69c9421ac22aae1c68844b3ca62c0`
- `campaign_fresh_gravity_astra/stage_20/independent_audit/DERIVATION_FROZEN.json`: `95dd3f7fe9848d2e43f41b0f58f8d8ba57c8392d54aa7e1d8873ca24a6e968e6`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/tasks/FGF-034.md`: `71ab5c8568aecaa39ad3aebfac8ba60f0055f7b00dcea50662aa1ee246e6ff8f`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-023/fgf023_run_001/DERIVATION.md`: `0b9babab32edd602cf5aea8db63126a52f09c379b858e5c5967d46835bbf1f4a`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-033/fgf033_run_001/DERIVATION.md`: `d1de4d4836093225a80edac5134cfb6bc3e30feaa6c513efbc43379da2b830fd`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-034/fgf034_run_001/DERIVATION.md`: `1ec0a8604e6c66804804fe02779edb6ce9dd8d61fd09e5719b5cbcb9b9863b0a`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-034/fgf034_run_001/REPORT.md`: `480747a350ac2e7dcb2cbc4ff6521978260af8bc886365051317925b298ce3a1`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-034/fgf034_run_001/result.json`: `89ce834a6a073d4cf6da91345151d645da39104333d17d6f2528f602ba9f50f3`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-034/fgf034_run_001/input_sha256.json`: `e80dbd49a390e7625536ab32ec0b2517642960150afa9f587eb9f945e2ef795a`
