# FGF047: actual local coupled diagnostic evolution

Accepted after a full independent construction audit and a separate, narrower
compatibility/energy audit. For each fixed finite admissible N, the exact
C1,1 compact velocity and inherited smooth positive-gradient hydrostatic data
admit a positive-time classical solution of the actual one-dimensional,
fixed-reference diagnostic Q/scale/isothermal-fluid equations. Matter and first
field derivatives are C1, with spatially Lipschitz first derivatives; field
potentials are C2. This closes the fixed-field source mismatch locally: the
source is B_x=Cn+tau phi_tt, with phi and chi actually evolving.

The proof is a construction, not only a real-speed principal-symbol check.
It includes seven characteristic coordinates, all h_chi source terms, a compact
state box separated from g=0, a coefficient cutoff, characteristic iteration,
uniform first-derivative and derivative-Lipschitz bounds, C0 contraction, and
an explicit interpolation upgrade to a spacetime C1 limit. The actual unchanged
polynomial joins are retained. Norms are dimensionally normalized first; the
positive physical time is restored afterward. The time depends on actual norms
and coefficient bounds and has NOT been proved to scale as N^-4.

Adding and subtracting the field characteristic equations gives g_t=p_x and
p_t=b^2 g_x+A+b h_chi(chi_x-k). The scale pair and chi_t=w propagate chi_x=k;
the phi time integral propagates phi_x=g. Thus compatibility is proved after
the diagonal limit, not assumed for each iterate. Coincident characteristic
speeds cause no loss of this coordinate basis. A same-point displacement bound
propagates positive density, scale and g margins and keeps the cutoff inactive.
Finite-speed cones and local uniqueness make the physical germ independent of
auxiliary exterior extensions on common backward domains. No wall or cusp is
crossed; different extensions can give different guaranteed lower times.

Full local matter+interaction+Q+scale energy holds for the constructed solution.
Matter exchange +n phi_t cancels Q exchange -n phi_t, while -T chi_t/C cancels
+T chi_t/C. Both field fluxes -(phi_t B+J chi_t chi_x)/C are essential.
Moving-boundary energy terms remain; no conserved shrinking-cone integral is
claimed. The exact hydrostatic zero-velocity control checks all four equations,
including the spatial h_chi terms when chi_x is nonzero.

The full reviewer froze an independent construction before author exposure.
Its original off-constraint subtraction contained an algebraic error; the
reviewer detected and explicitly corrected it BEFORE author exposure. Both
original and correction are preserved. The corrected identity agrees with the
author and independently frozen narrow audit. The author's final proof needed
no correction. Old-source text was read before some pin checks, then all nine
ancestry pins matched before derivation; that chronology is disclosed. The
coordinator critical reconstruction followed exposure and is not presented as
a third blinded theorem. The narrow audit does not claim to verify PDE existence.

A precise next gap remains: the cutoff construction proves a time for each N,
but supplies no uniform lower time comparable to ell/V. Initial field time
jets cannot replace a feedback estimate on an actual uniform interval. FGF048
therefore tests uniform coupled existence and force response before a fixed
small compression time. It must not inherit the fixed-force upper-lifespan or
first-gradient-divergence theorem from FGF046 without new bounds. It is a ready
specification only, with no launched run or claim at this checkpoint.

Both a0=9.3619e-11 and 1.1279e-10 remain separate fixed-reference cases, as do
constant-vacuum and frozen H comparisons. Evolving H has protocol work and is
outside this conservation theorem. Q is not replaced by RAR, registered M or
filtered MONO. The added diagnostic scale degree of freedom does not establish
a physical vacuum reservoir, pointwise vacuum relation, two gravitational DOF,
metric/photon coupling, criterion B, calibrated cluster evidence, cosmology,
stability or theory closure. No historical novelty is asserted.

This is an analytic local theorem for the specified diagnostic equations.
Zero mathematical executable computations, numerical samples or observational
runs support this pass; administrative hash/JSON checks are not experiments.

## Evidence pins

- `campaign_fresh_gravity_astra/stage_34/compatibility_audit/AUTHOR_COMPARISON_AUDIT.md` SHA256 `096542a6cde2f17fdd9fb8f75ed436ffd66b23c329470532b94ff3f4b5218ce6`.
- `campaign_fresh_gravity_astra/stage_34/compatibility_audit/INDEPENDENT_DERIVATION.md` SHA256 `d7f9f0855671329ea79b511a8ece35b776675f8681a9b8decd908633d66e3ffe`.
- `campaign_fresh_gravity_astra/stage_34/compatibility_audit/audit_result.json` SHA256 `417d42acb915546711ad3d34abdd7ec8d665b178043b00e4109f33843a6f3fd9`.
- `campaign_fresh_gravity_astra/stage_34/compatibility_audit/independent_freeze.json` SHA256 `fd2efc060fa8e30c55f21474db45b1b547902803f0c37b46e0d91fa03b5d0efe`.
- `campaign_fresh_gravity_astra/stage_34/compatibility_audit/input_sha256.json` SHA256 `bb9b531a4d6be227ce37c9ef42987c2aee37a31b14ae14cc7812b906c2b27dc0`.
- `campaign_fresh_gravity_astra/stage_34/coordinator/CHECK_RECORD.json` SHA256 `1645d1b6e20b49abdc6b573f87e602cd308c03d55ebc9deec81104aff15dae6c`.
- `campaign_fresh_gravity_astra/stage_34/coordinator/CRITICAL_CHECKS.md` SHA256 `6a68e1463a622071b58826f74c61c4147e245a91c9ad81801a5048f6736bad41`.
- `campaign_fresh_gravity_astra/stage_34/independent_audit/AUTHOR_EXPOSURE.json` SHA256 `50f79d4e3b2d2ff4dee2cce3ebd074a94f0271bd4fe03885c2ec6d6c14452853`.
- `campaign_fresh_gravity_astra/stage_34/independent_audit/DERIVATION_FROZEN.json` SHA256 `2f6aab6f60433ed8608731e47c38fc5c5a2172e9c963de4a9ddcd07fec4e0cb0`.
- `campaign_fresh_gravity_astra/stage_34/independent_audit/FROZEN_DERIVATION.md` SHA256 `28643f530341805d86a316025e5388f3b40b5c05db01b937dd3e47324b608cd6`.
- `campaign_fresh_gravity_astra/stage_34/independent_audit/INDEPENDENT_AUDIT.md` SHA256 `8cc492fff6647c3a2813751cedb7ca029e5af339fab6014ab16c403774f151c4`.
- `campaign_fresh_gravity_astra/stage_34/independent_audit/PRE_EXPOSURE_CORRECTION.json` SHA256 `c3cebae2148cb2c222cb84e84cec198763d599dcb81dd9dfe66687e1acc2b51d`.
- `campaign_fresh_gravity_astra/stage_34/independent_audit/PRE_EXPOSURE_CORRECTION.md` SHA256 `8c2f6846fb42b84b8a6030a8da1fd41d5acb64bbfdce33c6c2d622fec67fc083`.
- `campaign_fresh_gravity_astra/stage_34/independent_audit/audit_result.json` SHA256 `aa242fce8902f386a4e1fb2603092fe68dc12e0b7debe3a654afe64f3c5a7eac`.
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-047/fgf047_run_001/DERIVATION.md` SHA256 `1f11fd635d50a36b6cc747187595b26ebd1f4d2c4e19b9ee58c024cc5b47cf7a`.
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-047/fgf047_run_001/FREEZE.json` SHA256 `145a28e4774a2437feacd517c550a7fe9d91f49b02ee1d2cf3a2f09001a0da74`.
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-047/fgf047_run_001/REPORT.md` SHA256 `fffec686276257d249aaf82d267527e0ccfa9759515d199a8028ceacf5b5171e`.
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-047/fgf047_run_001/input_sha256.json` SHA256 `06f8cda276ffd3bce353a67e1e306c694f6a54719d0675608d42242e8d64ff73`.
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-047/fgf047_run_001/result.json` SHA256 `bbc88bd9ea34282728fd620b7973a1a329b80ffceccd8d611242a1a5adbb43ad`.

Reconciled 2026-10-06T03:49:40.930242+00:00.
