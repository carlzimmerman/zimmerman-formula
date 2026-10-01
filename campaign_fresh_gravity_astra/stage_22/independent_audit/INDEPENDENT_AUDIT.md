# Independent audit of FGF035

Verdict: the stated local conditional crossing theorem and the standard-H1 coercivity obstruction are supported by the proof. No load-bearing mathematical gap was found within that scope. This is a proof audit of the inherited Q diagnostic action; neither observational evidence nor physical theory closure is established.

## Independence and execution record

The independent derivation was frozen at 2026-09-30T16:35:53.671618+00:00 as FROZEN_CROSSING_DERIVATION.md, SHA256 2b604f5cb3e1672fbd3407b1559e025b2869da7042338886387a3a8c347eccc5. The task and old stage04, FGF023 and FGF007 sources were available then. No new author or root proof and no formula preview had been read before this freeze. Subsequently the worker DERIVATION.md, REPORT.md and result/input records were inspected. The new stage22 root proof was not read. A worker readiness message described the subject of the forthcoming proof, not a derivation; the frozen record's no-formula-preview statement is accurate.

This audit used the mathbox proof-audit procedure. No numerical, symbolic, ODE or spectral computation was run. Python was used only for file hashing, JSON verification and writing these review records; no numerical manifest or execution bounds are claimed. All 11 worker input hashes and all 3 worker artifact hashes match current files, as do the 4 independently pinned sources and the frozen independent proof. Hash verification of additional worker ancestors is provenance verification, not a claim to have freshly re-audited every ancestor in this pass.

## Checked derivation

For B=sgn(g)b(|g|,a), a=a_ref exp(chi), the flux equation is B'=C rho. Positive density makes B a valid local coordinate. The transformed hydrostatic equation is rho_B=-g/(C cs²), with rho cancelling exactly; omitting that cancellation would change the model. The inverse is g=sgn(B)sqrt(B²+a|B|). Its chi derivative is sgn(B)a|B|/[2sqrt(B²+a|B|)], tending uniformly to zero as B tends to zero on compact positive-a sets. This establishes the needed dependent-state Lipschitz bound despite the independent-coordinate square-root cusp. Inverse-density factors remain smooth in a small rectangle with rho bounded away from zero. T is O(|B|^(3/2)) there and has bounded dependent-state derivatives. The two-sided integral-map contraction and positive x_B therefore justify local existence and uniqueness in the specified regular positive-density flux class. They do not prove uniqueness of arbitrary measure-valued weak solutions or global fixed-wall existence.

The exact off-zero derivative is

    g'=[(2|B|+a) C rho + a' B]/[2 sqrt(B²+a|B|)].

The term a'B changes sign with B; the leading density term does not. Consequently, with k=sqrt(a_* C rho_*), g'~k/(2sqrt(|x|)) on both sides. This independently verifies phi not in H2, with no illicit differentiation of a little-o remainder. Hydrostatic rho=rho_* exp[-(phi-phi_*)/cs²] gives the local potential minimum, density maximum and the same non-H2 obstruction for density. The sharp leading cusp and bounded coefficients give C^(1,1/2) and W^(2,p), 1<=p<2, for both fields. Since B'=C rho, the signed constitutive flux is C^(2,1/2).

For Q, T(s,a)=s³/(3a)+O(s^5/a³). Substitution into the signed reconstruction makes T=|B|^(3/2) times a function smooth in |B| and positive a. It is C^(1,1/2) along the local solution. Bootstrapping J chi''=U'-T therefore gives chi at least C^(3,1/2) and w at least C^(2,1/2). No unproved H4 claim is needed. The independent frozen derivation also obtains the compatible stronger error estimates B=C rho_* x+O(|x|^(5/2)), g=k sgn(x)sqrt(|x|)+O(|x|^(3/2)); the worker's weaker leading asymptotics suffice for its claims.

The constitutive flux is C1, so distributionally B'=C rho has no delta term. The singular phi'' is locally integrable and is not the MOND source. Continuity of the scale derivative likewise precludes a singular scale-flux term. W~k³|x|^(3/2)/(3a_*) is integrable; fluid internal energy, interaction rho phi and scale terms are bounded on a sufficiently small compact interval. This is finite static energy, not a theorem of positive total energy or time-dependent conservation.

## Hessian and exact failed gate

On smooth fixed-trace test triples let r=-(rho xi)'. The full form retains

    cs² r²/rho + 2 r psi
    + [A psi'² - 2 sgn(g) q eta psi' + J eta'² + (U''-T_chi)eta²]/C.

The signed mixed coefficient is essential on the negative side and tends to zero at the crossing. All coefficients are bounded and continuous. The mass constraint is integral r=0. Thus the directional second variation has a bounded extension to H1_0 triples. This statement does not require or imply twice Frechet differentiability of the full nonlinear energy on an unrestricted H1 neighborhood.

The admissible restriction xi=eta=0 leaves integral A psi'²/C, with A~(2k/a_*)sqrt(|x|). For psi_epsilon=sqrt(epsilon)f(x/epsilon), where nonzero f is smooth and compactly supported in (-1,1), the squared derivative norm is fixed, the squared L2 norm is epsilon² times integral f², and the quadratic energy is O(sqrt(epsilon)). The product-H1 coercivity constant must therefore be zero, even after fixed positive dimension-balancing norm weights are introduced. Matter and scale have not been removed from the general form: this is a legitimate test subspace of the full form.

Each bump has strictly positive energy since A>0 almost everywhere. In fact its leading energy is proportional to sqrt(epsilon), so its energy divided by a fixed positive phi kinetic L2 norm squared scales as epsilon^(-3/2), not zero. The sequence proves neither a negative-energy mode nor a zero-frequency sequence. Ghosts, spectral instability, nonlinear instability and PDE ill-posedness do not follow from this norm obstruction. The sign and operator domain of the full coupled form remain unresolved.

## Scope and next implication

Both positive a0 reference normalizations remain separate choices; the theorem uses only positive frozen a_ref. Frozen H(z) choices are distinct static reference hypotheses. An actually evolving reference requires the previously identified energy exchange or dynamical reservoir; this proof supplies neither. A responsive local a=a_ref exp(chi) is an additional diagnostic premise and does not establish the literal pointwise constant-vacuum identity. The Q constitutive law is used in the source and energy throughout. RAR transfer, any M action, filtered-MONO transfer, physical metric/photon coupling, calibrated cluster constraints and global theory closure are not proved.

The walls and mass are induced by this local IVP. For the Hessian test they are held fixed on a selected compact interval, not held fixed across every background in an IVP family. Failure of phi to lie in H2 and failure of uniform H1 coercivity independently block application of the previous FGF034 proof unchanged. They do not rule out an appropriate weighted inverse or response theory.

A specific next mathematical target is to define the completion with norm containing integral sqrt(|x|)|psi'|² plus fluid and scale H1 contributions and L2 terms, then prove or disprove closedness and boundedness of the full mixed form on that domain. Only after such a domain is justified should fixed-wall response or stability be considered. No task was dispatched or queued by this reviewer.

## Exact pins

The following hashes pin audit inputs, worker ancestry and the independent freeze. The JSON audit record repeats this mapping and identifies worker hash-verification counts.

- `campaign_fresh_gravity_astra/stage_04/scale_dynamics/DERIVATION.md`: `2d00fa29165b274d7288505ffc7756c2189a6915dbec6d500fd1a775f6ffb724`
- `campaign_fresh_gravity_astra/stage_20/constrained_response/ROOT_DERIVATION.md`: `6e5bea47841c4dab7ce8cdbcb0e5fa790701f415b76ba85043abe61ec5538dcc`
- `campaign_fresh_gravity_astra/stage_21/zero_field/ROOT_DERIVATION.md`: `2ab4ef7723b8bd13636ec693ee9fad738e9af55c3f79830220068213b73748e1`
- `campaign_fresh_gravity_astra/stage_21/zero_field/audit_result.json`: `b073dc450af84ce8f8e72ee898d9cf26a486a89f7c72a788c0cfc7a65ca96e78`
- `campaign_fresh_gravity_astra/stage_22/independent_audit/DERIVATION_FROZEN.json`: `bc7fa7932e12ebb7e1789140a9be1bf9b5d49e58c7e4b9982a92416927cdaf27`
- `campaign_fresh_gravity_astra/stage_22/independent_audit/FROZEN_CROSSING_DERIVATION.md`: `2b604f5cb3e1672fbd3407b1559e025b2869da7042338886387a3a8c347eccc5`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/FRAMEWORK_AND_EXECUTION.md`: `ff0d2873065578b0bd8aa50907e0a39495ff8da775bf2b4890768d83775fd750`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/RESULT_CONTRACT.json`: `ba388d0ca8e447a38649a478483e3ff4c2d3293e842eedc8f035499c77a20c29`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-007/fgf007_run_001/DERIVATION.md`: `c103dc2f252ef1be27458dff2ddf60895e33c3f0a680c1028fd5e19a4eab4104`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-007/fgf007_run_001/result.json`: `165bc799422be7a8610a4fad3b45d55d1b4ec70c70e68c3f590ea7ba41f3d80d`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-023/fgf023_run_001/DERIVATION.md`: `0b9babab32edd602cf5aea8db63126a52f09c379b858e5c5967d46835bbf1f4a`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-035/fgf035_run_001/DERIVATION.md`: `5aa9e64b81a9dcaac14926f43c680a82d44d57be838423ccc4b0ebeee1cb1d3b`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-035/fgf035_run_001/REPORT.md`: `cf15d52faf8204c4c7a2c8d8c4327b89687d84751f0186d0906935fc0f992950`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-035/fgf035_run_001/input_sha256.json`: `b36b28ef156d9500ba7b5e8c8b90a7c82034e9cef1d1d9cf7c2c7abda16e9d7b`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-035/fgf035_run_001/result.json`: `a92f785e1642c43d1b9df4030add980ca621b484e20b5d6980a33bb620c4a747`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/reviews/FGF-007_RECONCILIATION.md`: `aa8ae3cc4cb3c022bf4efaaa1686fbc52ec2303e4512fec061162215bd14f6e1`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/reviews/FGF-034_RECONCILIATION.md`: `9df1b83ca18f15b0fcb13c6595378a124fd6b2d67fe3be3687d5b59e38e00ff9`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/tasks/FGF-035.md`: `0823d0f6298db21b4cf6992497227ea10a1e2532da6c1d136fa6521ea84455b0`
