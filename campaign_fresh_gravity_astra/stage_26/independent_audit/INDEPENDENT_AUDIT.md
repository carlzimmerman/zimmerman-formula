# Independent audit of FGF039

**Primary verdict: proved as written in the corrected revision.** The expanded-density lower-energy theorem, exact entropy minimization, L1 controls and density counterexample are supported. The scale barrier is supported only with its explicit pre-existing-trajectory assumptions. One false equality characterization was identified and corrected before this verdict; the original evidence is preserved.

## Normalized claim and revision

Fix a sufficiently short Q crossing interval with fixed mass M, physical coefficients and field walls. For every nonnegative fixed-mass finite-relative-entropy density n and ordinary H1_0 potential/scale perturbations with scale supremum at most one quarter, the complete static relative energy controls cs²D(n|rho_psi), weighted potential energy and scale H1 energy under the displayed alpha/beta gates. Here rho_psi is the mass-normalized exponential minimizer, not automatically the original rho. L1 distance to rho is controlled by a separate conversion. Small energy does not enforce a pointwise density half-cap or exclude vacuum. Reaching the scale cap has a positive energy threshold only applicable to an already existing trajectory in the declared continuous conservative class.

The initial DERIVATION.md, SHA256 71ef5d150ff3912c378bec4df457a6ef8e0ab727628c5aa3177991b8f2e1d6a3, stated: “Equality in (8) forces psi=eta=0 and n=rho.” That literal statement is false: choose psi=eta=0 and any admissible n different from rho. Both sides of (8) then equal the positive cs²D(n|rho). The auditor identified this counterexample and requested replacement by “Zero excess energy Delta E=0 forces psi=eta=0 and n=rho.” The latter follows from the nonnegative lower terms and is the strict-minimum claim actually needed.

The corrected proof is SHA256 c0f098c821ab9ec3346c3365fd9e45d8d536fe437ad47850fe38ecc523ebead8 and corrected result is 7a3ffddec2231f7d8606a94d243027b3c21b2d1ef1b456747ca9d9e2f41bb8b5. Byte comparison confirms this sentence is the only proof change. Both worker and auditor preserve identical original proof bytes; the worker also preserves its original result. CORRECTION.md and the reviewer's CORRECTION_REQUEST.json record the counterexample and attribution. The original result is a historical snapshot, not a current-file hash-validation record. No lower-bound coefficient, entropy formula or barrier changed.

## Independence and execution

The auditor independently froze FROZEN_ENERGY_DERIVATION.md at 2026-09-30T20:35:54.569349+00:00, SHA256 016c2af282b0f484887efe87a0f1582ab8afbd1188ecae409dcf1d13bcd51f53, before any new author/root proof or formula preview. The author's readiness message arrived after that freeze. Its initial proof was then read and the equality error identified. The new stage26 root proof was never read. The corrected author proof was compared against the preserved initial candidate. This is independent pre-derivation followed by an author audit and one openly recorded repair, not an assertion that the repaired sentence was originally correct.

The audit used the mathbox proof-audit workflow. No mathematical computation, numerical scan, trajectory or spectrum was run. Python was used for hashing, byte/text comparison, JSON validation and report writes only. All 10 current worker input hashes, 6 current worker artifact hashes, 5 independently pinned sources, frozen-proof identity and required result fields match. Historical result bytes are pinned without treating their references to the old candidate paths as current validation. No numerical manifest or execution-bound enforcement is claimed.

## Dependency graph and obligations

The dependency chain is: inherited action/crossing and FGF038 scale bound -> exact mass-constrained entropy identity -> elementary global exponential-integral bound -> full lower bound -> density distances and counterexample -> separate conditional scale first-hit argument. All new leaves are elementary proofs; the old action/scale estimates are pinned prior evidence. No external statistical or functional-analytic inequality is being imported by name without proof.

| Obligation | Status | Decisive check |
|---|---|---|
| Nonnegative density and vacuum admissibility | Passed | Entropy extends with 0 log0=0; interaction terms remain integrable |
| Mass-normalized minimizer | Passed | Positive finite Z, exact mass M, unique zero entropy remainder |
| Minimized functional signs | Passed | Both -M cs² log Z and -int rho psi retained |
| Global amplitude bound | Passed | Tilted variance derived directly and bounded by squared range/4 |
| Full coupled lower bound | Passed | Changed density alpha plus unchanged exact finite-scale beta |
| Entropy and L1 reference conversion | Passed | rho_psi reference explicit; author constants checked separately |
| Density cap/vacuum counterexample | Passed | Exact fixed-mass vacuum-hole energy tends to zero |
| Scale barrier | Passed, conditionally | Two-wall estimate and first hit on an existing continuous conservative trajectory |
| Equality in lower bound characterizes background | Failed and corrected | Positive pure density entropy also saturates the bound |
| Zero excess energy characterizes background | Passed in corrected revision | All nonnegative lower distances must vanish |
| Nonlinear solution existence or no-vacuum theorem | Out of scope | Neither follows from this energy-class argument |

## Entropy minimization and normalization

Write u=cs² and D(n|q)=int[n log(n/q)-n+q]. The exact density part of relative energy is uD(n|rho)+int(n-rho)psi. Since psi is bounded, Z=M^(-1)int rho exp(-psi/u) is finite and positive. The candidate q=rho_psi=rho exp(-psi/u)/Z is positive, has mass M and finite relative entropy. Direct substitution gives

    uD(n|rho)+int(n-rho)psi
       =uD(n|rho_psi)-u M log Z-int rho psi.

The entropy identity is valid for every nonnegative admissible n, including n=0 on sets: log(rho_psi/rho) is bounded, so changing the reference preserves finiteness. The scalar function t log t-t+1 is nonnegative on [0,infinity), with its unique zero at one. This proves attainment and uniqueness of the minimizer without assuming a positive lower bound on n or using a statistical inequality from memory.

The normalization and mean-potential term are essential. A constant shift of psi multiplies Z by the inverse exponential factor and cancels against int rho psi; both the minimizing density and minimized energy are unchanged. Freezing the mass multiplier or dropping the mean term would fail this control.

All complete-energy first variations still cancel for r=n-rho in L1: the hydrostatic multiplier is bounded and constant, psi is bounded, and the background flux/scale integrations involve H1 zero traces. No old density pointwise cap or L2 density assumption is needed. The density may be unbounded with finite entropy. Its interaction with the bounded potential is nevertheless integrable.

## Global minimized-potential bound

Using probability rho dx/M, define L(t)=log int exp(-t psi/u)dmu. Bounded psi permits direct differentiation and gives L''(t)=Var_t(psi)/u². The variance bound is elementary: for a value Y in [a,b], the nonnegative product (Y-a)(b-Y) implies Var(Y)<=(mean-a)(b-mean)<=(b-a)²/4. Thus

    0<=L(1)-L'(0)<=osc(psi)²/(8u²),
    -M osc(psi)²/(8u)<=F_min(psi)<=0.

This is global in psi; it is not a truncated exponential approximation. Weighted Cauchy-Schwarz between its extrema gives osc(psi)²<=I_A int A psi'². Consequently the density term is bounded below by uD(n|rho_psi)-alpha E_p with alpha=C M I_A/(8u). The background reciprocal-A integral is finite even across the cusp, and ordinary H1_0 is within the weighted space where this estimate holds.

Combining the exact inherited finite-scale inequality with the retained scale-gradient and convex-potential terms yields

    Delta E>=uD(n|rho_psi)+(k/2-alpha)E_p
                     +(1/2-beta)E_eta+S0 int eta²/(2C).

Under alpha<=k/4 and beta<=1/4 this is the advertised bound. M=O(d), I_A=O(sqrt(d)) and Rmax=O(d^(3/2)) along the same central solution give alpha=O(d^(3/2)) and beta=O(d^(7/2)); physical coefficients remain fixed. The change of interval changes induced mass and walls, not the comparison mass within a fixed interval. These are symbolic sufficient gates with no calibrated numerical size.

## Density distances and the correct reference

The exact controlled entropy is D(n|rho_psi). The author's elementary inequality

    t log t-t+1 >= (t-1)²/[2 max(1,t)]
                         >= (t-1)²/[2(t+1)]

follows by integrating the second derivative 1/t along the segment from one to t, and extends to zero. Multiplication by a positive reference q and Cauchy-Schwarz, using int(n+q)=2M, give D(n|q)>=||n-q||_1²/(4M). This proof requires no lower bound on n. The intermediate fraction is integrable even for unbounded n because (n-q)²/(n+q)<=n+q.

The normalized path rho_t has derivative -rho_t(psi-mean_t psi)/u. Integrating the author's bound ||partial_t rho_t||_1<=M osc(psi)/u gives its stated conversion. Squaring the triangle bound yields

    ||n-rho||_1²<=8M D(n|rho_psi)
                          +2M² C I_A E_p/u²
                   <=K_rho Delta E,
    K_rho=max{8M/u,8M² C I_A/(k u²)}.

Every factor checks. The independently frozen proof used the variance estimate to improve the path bound by a factor two, giving a smaller sufficient second coefficient; that improvement is not silently substituted for the author's actual certificate. Both are valid. Neither estimate is pointwise control or a quadratic density norm bound. D has mass-per-area units, uD energy-per-area units, and K_rho has the units needed for squared L1 density distance divided by energy.

## Density counterexample and potential dynamics

Let J_epsilon have shrinking positive background mass m_epsilon. The density zero on that set and equal to M rho/(M-m_epsilon) outside is nonnegative, fixed-mass and finite-entropy. With psi=eta=0, exact hydrostatic first-variation cancellation leaves

    Delta E=uM log[M/(M-m_epsilon)] ->0.

It violates the old lower half-cap on a positive-measure set and creates vacuum there. There is no density-gradient energy in this inherited action that would reject these measurable comparison profiles. As an additional elementary check, the midpoint density (rho+n_epsilon)/2 lies exactly on the old lower half-cap in the hole and has energy at most half this value by entropy convexity. Thus even reaching that density-cap boundary has no positive energy threshold in the comparison class.

These states are not claimed to be equilibria or actual solution trajectories; the example does not demonstrate dynamical vacuum formation. The source/potential coupling is accounted for, not dropped. In the inherited dynamic potential action, let P=sgn(phi_x)b(abs(phi_x),a) be the current signed constitutive flux. Its equation is P_x=C n+tau phi_tt. Therefore an arbitrary energy comparison state need not obey static P_x=C n with phi fixed. Entropy minimization also does not impose n=rho_psi instantaneously along a trajectory. Constructing an evolution or giving meaning to all weak force products remains a different obligation.

## Conditional scale barrier and its exact limits

For eta in H1_0, the two endpoint integrals imply int eta'²>=4||eta||infinity²/ell: at an interior absolute extremum, apply Cauchy separately to its distances from the two walls and add. The lower energy term E_eta/4 therefore gives Delta E>=J||eta||infinity²/(C ell). At the quarter-cap this is J/(16C ell).

The total perturbation energy includes nonnegative matter and field kinetic energies in addition to Delta E. At vacuum, finite kinetic energy must be interpreted consistently; no positive-density velocity norm or no-vacuum assertion is inferred. The barrier argument assumes an already existing trajectory that retains nonnegative fixed-mass finite-entropy density, finite-action fields, static prescribed field walls and impermeable fluid walls, is continuous in eta's H1 topology, and conserves the full fixed-reference energy. If its scale starts strictly below the cap and its relative total energy is strictly below the threshold, H1 continuity supplies a first hit whenever the cap would be reached. At that hit the closed scale cap still holds, so the static lower bound and nonnegative kinetic energy contradict the conserved value.

This closes a conditional scale-cap bootstrap only during the trajectory's existing lifetime. It does not supply existence, uniqueness, continuation through singularities, weak energy equality, preservation of the finite-entropy/action class, pointwise density control or a no-vacuum theorem. Time-dependent walls, unaccounted boundary/source work or a prescribed evolving reference would remove the conservation premise. The positive barrier is not a proof of physical-theory stability.

## Remaining scope

The corrected static theorem is checked; no load-bearing gap remains within its stated conditions. Its equality-in-bound claim was withdrawn, with the valid zero-excess-energy statement substituted transparently. FGF037 discontinuity, infinite-action weighted directions and failure of uniform upper/Taylor control remain unaffected.

Both positive a0 reference normalizations are distinct cases. Constant-vacuum, frozen-H and truly evolving-H branches remain separate; locally responsive scale is an added diagnostic premise, and an evolving reference still requires its own energy exchange accounting. Signed MOND Q sources are retained. RAR/M transfer, physical metric/photon/DOF, filtered-MONO, calibrated observations and theory closure are not established.

The worker proposes a next question about the integrability of n phi_x or a combined weak momentum formulation. That is a specific unresolved evolution-admissibility target, not evidence accepted by this audit and not a solution construction. This reviewer dispatched no new task or numerical run.

## Exact pins

- `campaign_fresh_gravity_astra/stage_25/independent_audit/INDEPENDENT_AUDIT.md`: `8e45e4970f10bc5dd42123afbf9206f49e50c7d313dfc2280b16bf6102615097`
- `campaign_fresh_gravity_astra/stage_25/relative_energy/ROOT_DERIVATION.md`: `404901535858dee0c368dd879c16cd329627ef372d1fa5e001e08af544056817`
- `campaign_fresh_gravity_astra/stage_25/relative_energy/audit_result.json`: `3f0a467b1690423facd4ea3c5ccddfba1732bece07f78e098a56514c0b20dbc6`
- `campaign_fresh_gravity_astra/stage_26/independent_audit/CORRECTION_REQUEST.json`: `c748857882f9414c82d4a22a3234886deaed3796504cb113996667bf956cf724`
- `campaign_fresh_gravity_astra/stage_26/independent_audit/DERIVATION_FROZEN.json`: `3cd0da5dd0c119ac9a32bb0f793545ba6f3f39d86eac87d160b617d705737e7d`
- `campaign_fresh_gravity_astra/stage_26/independent_audit/FROZEN_ENERGY_DERIVATION.md`: `016c2af282b0f484887efe87a0f1582ab8afbd1188ecae409dcf1d13bcd51f53`
- `campaign_fresh_gravity_astra/stage_26/independent_audit/REVIEWED_CANDIDATE_BEFORE_CORRECTION.md`: `71ef5d150ff3912c378bec4df457a6ef8e0ab727628c5aa3177991b8f2e1d6a3`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/FRAMEWORK_AND_EXECUTION.md`: `ff0d2873065578b0bd8aa50907e0a39495ff8da775bf2b4890768d83775fd750`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/RESULT_CONTRACT.json`: `ba388d0ca8e447a38649a478483e3ff4c2d3293e842eedc8f035499c77a20c29`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-023/fgf023_run_001/DERIVATION.md`: `0b9babab32edd602cf5aea8db63126a52f09c379b858e5c5967d46835bbf1f4a`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-036/fgf036_run_001/DERIVATION.md`: `71727e56c1c7d88bd2d24988af4683339b5fdc4db6f9ca54d9c800752a747f1a`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-038/fgf038_run_001/DERIVATION.md`: `3891484b03b38d8697155d9a28a3eaa6344a0337f7c8504c4adf510ef23f86d1`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-038/fgf038_run_001/result.json`: `c88bd2ebd307653d98dbabdd3588f98900f312e1db13093265c76c8dcea51bc6`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-039/fgf039_run_001/CORRECTION.md`: `bdf8001c004384856e8fcb07209b3ce61dddd4fff1d2591ead1ab47f769a50fe`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-039/fgf039_run_001/DERIVATION.md`: `c0f098c821ab9ec3346c3365fd9e45d8d536fe437ad47850fe38ecc523ebead8`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-039/fgf039_run_001/DERIVATION_PRE_CORRECTION.md`: `71ef5d150ff3912c378bec4df457a6ef8e0ab727628c5aa3177991b8f2e1d6a3`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-039/fgf039_run_001/REPORT.md`: `d85b87242d0c04f1f6c2623454b7a114b3367509498cf3d50b380de4bc7727a8`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-039/fgf039_run_001/input_sha256.json`: `d580648fc5e7ab7364c32652d290b1e40b1b72e3092b794d48b16d88fe9e243a`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-039/fgf039_run_001/result.json`: `7a3ffddec2231f7d8606a94d243027b3c21b2d1ef1b456747ca9d9e2f41bb8b5`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-039/fgf039_run_001/result_pre_correction.json`: `c6a0f4289ea47959a825ad102f39d52e93aca78391269031c778a2b5a343b363`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/reviews/FGF-037_RECONCILIATION.md`: `b361281d7e09edb5bfe7cc67ec3ba3cb9ecb319629ef38a64203248680397994`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/reviews/FGF-038_RECONCILIATION.md`: `7997c0c381ac315560e542f76346d5601db89e63a1ff4e40384cf734105d383a`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/tasks/FGF-039.md`: `85ef997d2707f248bfd7838b2f2d14460e07fdc7d9c08fcabfb6d04b574fc6bc`
