# Independent FGF033 global-driver and stability audit

**Verdict: proved as written within the declared conditional Q diagnostic extension.** The driver supplies exact global energy exchange, but a constant driver potential cannot support a nonzero-field static equilibrium. At an actual equilibrium with a matching coercive fixed-lambda form, the full Schur margin is the additional necessary and sufficient coercive-stability condition. Neither conservation nor positive inertia supplies that margin.

## Independence and evidence

FROZEN_DRIVER_DERIVATION.md was frozen at 2026-09-30T12:32:41.336970+00:00, before any new worker or root proof was read. Its inputs were FGF033 and pinned FGF023/032 derivations. It independently contains the equilibrium condition, full Hessian, weak Schur representation, transformed kinetic Hamiltonian, linked theta boundary domain and transformed global-momentum endpoint term. The new root and worker proofs were subsequently read and audited. No other stage18 audit was read. No numerical, symbolic or sampled computation was executed; administrative file hashes are not mathematical experiments.

The root's BOUNDARY_ADDENDUM explicitly credits the auditor's boundary observation and then checks it from the original equations. The worker reports independently deriving its section 7 endpoint identity before informing the coordinator. These are separate ancestry statements; the root addendum is not counted as an independent discovery of that detail.

## Driver force, energy and equilibrium

With C=4piG and fixed physical coefficients, partial_lambda L_field=T/C gives

 I lambda_ddot+V'(lambda)=integral T/C.

The original field-plus-matter energy loses lambda_dot integral T/C; the driver energy I lambda_dot²/2+V gains exactly that amount. Total energy changes only by the original physical boundary flux, which vanishes under fixed phi/chi traces and impermeable matter. The interaction rho phi, enthalpy flux and signed field-source equations are retained. In evolution the MOND flux is P_x=C rho+tau phi_tt; static B_x=C rho is not substituted into the time-dependent system.

At equilibrium the indispensable additional equation is V'(lambda0)=integral T0/C. Q has T>0 on a nonzero-field regular patch, so constant V cannot satisfy it. This is failure of static equilibrium, not an eigenvalue computation about that nonexistent equilibrium, and not a proof of indefinite runaway or exclusion of every possible V. One fixed, independently specified V must satisfy the balance at any claimed background. No old fixed-lambda slab automatically becomes an equilibrium of the enlarged model, and no V is tuned in this proof.

I has energy*time²/area units, V energy/area and lambda is dimensionless. A global mechanical coordinate does not define a local driver stress or covariant energy density. Total energy conservation of this chosen model establishes neither a lower bound on nonlinear gravitational energy nor physical adequacy.

## Full Hessian and equation signs

Use u=(xi,psi,eta) in H1_0(0,D)^3 and l=delta lambda in R. Write r=-(rho xi)', s=T_chi=2T-gq and m=U''-s. The complete second variation is

 Q=Q0[u]+2l L[u]+k l²,
 L[u]=-integral(q psi'+s eta)/C,
 k=V''(lambda0)-integral s/C,
 Q0=integral[cs² r²/rho+2r psi+(A psi'²-2q eta psi'+J eta'²+m eta²)/C].

The signs follow directly from W_gchi=-q and W_chichi=-s and the total variation delta(chi+lambda)=eta+l. The original U depends on chi only, so inserting U'' l² or a U'' eta*l term in these coordinates would be wrong. There is no direct matter-lambda term because the interaction is rho phi, but matter responds inside the full Q0 inverse. Hydrostatic e'(rho)+phi=constant and the actual mass constraint justify the density Hessian exactly as in the pinned parent.

A separate linearized-equation check gives

 tau psi_tt-[A psi'-q eta-q l]'=-C r,
 sigma eta_tt-J eta''+m eta-q psi'-s l=0,
 I l_tt+k l+L[u]=0.

Together with the inherited material equation these agree with the claimed Hessian and positive kinetic form N=N0+I l_dot². The derivative in the phi equation acts on the variable background q; no constant-coefficient simplification or additional zero-flux boundary condition is imposed.

The proof retains the full form. If psi were statically minimized, setting h=C rho xi-q(eta+l), compatibility integral psi'=0 would leave (integral h/A)²/[C integral 1/A]. It cannot generally be set to zero. Retaining Q0 and its original Dirichlet weak inverse automatically preserves this contribution.

## Schur criterion and precise stability interpretation

The functional gate is essential: Q0 must be a continuous coercive symmetric form on the actual H1_0 product domain, in fixed reference units. Strict pointwise positivity alone is not silently upgraded to bounded invertibility. Smooth bounded coefficients make L continuous. There is a unique z with B0(z,v)=L[v], and S=L[z]=Q0[z]>=0. Exact completion gives

 Q[u,l]=Q0[u+l z]+Delta l², Delta=k-S.

The bounded invertible map (u,l)->(u+l z,l) proves full coercivity exactly for Delta>0. Equality gives precisely one null direction (-z,1), including (0,1) if L=0. Delta<0 gives negative index exactly one, not merely a heuristic negative stiffness. With smooth finite-domain coefficients and strictly positive kinetic weights, adding a sufficiently large mass-space multiple closes and bounds the full form below; the compact H1-to-L2 embedding plus the finite coordinate yields compact resolvent. Its spectrum therefore has a positive gap, a zero mode, or one negative squared-frequency eigenvalue in the respective cases. The latter produces exponential linear growth. The equality case permits zero-mode linear drift and proves no nonlinear stability.

Increasing finite I changes modal rates, not Delta's sign. The scalar fixture in the worker is correctly identified as an algebraic Schur control, not an actual hydrostatic solution. No numerical frequency, simultaneous equilibrium, empirical inertia or physical V has been supplied. In particular the old four-reference fixed-lambda bounds cannot alone establish four stable equilibria for one common V.

## Autonomous theta transformation and linked traces

When lambda is dynamical, theta=chi+lambda is a time-independent change on the enlarged configuration space. The exact kinetic term is integral sigma(theta_t-lambda_dot)²/(2C)+I lambda_dot²/2 and the potential is U(theta-lambda). The momenta obey

 pi_theta=sigma(theta_t-lambda_dot)/C,
 P_lambda=I lambda_dot-integral pi_theta,
 H_kin,scale+driver=integral C pi_theta²/(2sigma)+(P_lambda+integral pi_theta)²/(2I).

The integral subtraction and positive sign inside the final square are correct. The field-only prescribed-coordinate energy correction is canceled when the global Legendre transform is included, so the full Hamiltonian is exactly the physical total energy. The kinetic form stays nondegenerate; exactly one new global canonical pair remains. No gauge reduction or local gravitational degree count follows.

The transformed perturbation zeta=eta+l must satisfy zeta(0)=zeta(D)=l, equivalently zeta-l in H1_0. The transformed Hessian with U''(zeta-l)² maps exactly to the original form. Independent zero theta traces would remove allowed variations and change the model.

The boundary check is consequential: integrating the original scale equation and using P_lambda gives

 P_lambda_dot=integral U'(theta-lambda)/C-V'-J[theta_x]_0^D/C.

The same term arises from -J[theta_x delta theta]/C because delta theta equals delta lambda at both endpoints. Combining this identity with the integrated field momentum recovers the original driver equation exactly. Dropping it yields a spurious J[theta_x]/C force, unless an exceptional equal-gradient background happens to mask the mistake. No equal-gradient condition is assumed. The term is coordinate/domain bookkeeping for the same original fixed walls, not an added support force.

## Provenance, limitations and remaining implication

All 11 worker input pins and 3 artifact pins match current files; the reported proof-only execution has no numerical manifest or measured computational runtime. The final result, reviewed proofs, frozen independent derivation and root addendum are pinned below. No mathematical gap was found in the scoped claims.

This is an explicitly added global diagnostic coordinate with new I, V and initial-data pair. Neither a physically justified V, an actual enlarged-model equilibrium, a local driver stress nor the scale-vacuum relation has been derived. Both a0 normalizations and their separate frozen H references remain candidates requiring the same declared V's balance. No H history is selected, and no reference relabeling repairs the literal constant-vacuum actual-scale incompatibility. No RAR/M action, operative filtered-MONO transfer, metric/photon completion, nonlinear/3D/free-wall result, observation or theory closure follows.

The next admissible physical step requires an independently specified V and interpretation, followed by simultaneous equilibrium and full Schur evaluation on its original boundary domain. Fitting V' and V'' to make a desired state pass would not establish that missing derivation.

## Exact pins

- `campaign_fresh_gravity_astra/stage_18/independent_audit/FROZEN_DRIVER_DERIVATION.md`: `94e8369d8be21cd379d377e299b877e02f9ab3eac7c68713bd013dc56ae511b4`
- `campaign_fresh_gravity_astra/stage_18/independent_audit/DERIVATION_FROZEN.json`: `d663e7a03bf82c8b70afd37708ec57ce4e8dd1db2be41daf4c3eb502f8f2c45a`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/tasks/FGF-033.md`: `96623cac2e3793d75d72ef26d38c0fe233538db2274b53805a07a6a030f874e4`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-023/fgf023_run_001/DERIVATION.md`: `0b9babab32edd602cf5aea8db63126a52f09c379b858e5c5967d46835bbf1f4a`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-032/fgf032_run_001/DERIVATION.md`: `593451d00dfece43f71def5426001b7b863020389f94ca088fcb308c90367590`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-033/fgf033_run_001/DERIVATION.md`: `d1de4d4836093225a80edac5134cfb6bc3e30feaa6c513efbc43379da2b830fd`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-033/fgf033_run_001/result.json`: `96555a0360c4ac99d80f4d1186b0a1140ef6206e4a92b5fbd972d432ff8dac50`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-033/fgf033_run_001/REPORT.md`: `1ca95743534a7f8bb2898f836aecc02f1c35c038ea5063f15420b6514fff666e`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-033/fgf033_run_001/input_sha256.json`: `27266fd562b8690d7ec932104e95019840eeed56708f18c098a1d1733e9aecc1`
- `campaign_fresh_gravity_astra/stage_18/global_reference/ROOT_DERIVATION.md`: `642369f3d43df94d45c66ec5d2f437a173e6185cd834ff93a1dcaed4239d6637`
- `campaign_fresh_gravity_astra/stage_18/global_reference/BOUNDARY_ADDENDUM.md`: `43bda7649072ab389cd25369f7cc70c8a04f53a010a09ac78f90415e89dab6e5`
