# FGF038: exact coupled lower-energy control, with explicit caps

Accepted conditional analytic result: every sufficiently short restriction of
one inherited Q crossing has a strict exact static energetic minimum on the
specified capped finite-action class. This is stronger than a linear Hessian
statement, but does not construct nonlinear evolution or prove stability.

The class fixes mass and both field walls, takes Eulerian density increment r
with integral r=0 and |r|<=rho/2, psi,eta in H1_0, and |eta|<=1/4. Potential
gradients can be arbitrarily large. All coefficients and central data remain
fixed when shortening the same crossing; induced mass and walls change with
restriction. Neither density cap nor scale cap is derived as dynamically invariant.

A directly proved global Q scalar inequality is
W(|g+h|,a)-W(|g|,a)-B(g,a)h >= A(g,a) h²/64.
It follows from exact integration of the signed second derivative and two
subinterval cases, and includes reversed sign and large gradients. At g=0
the weighted right side is zero; this single point does not destroy the
integrated Dirichlet norm. No deep-MOND expansion is extrapolated to large h.
Scale changes obey A(g,a exp eta)>=exp(-1/4)A(g,a). Put k=exp(-1/4)/64.

The exact energy retains r psi and the entire finite scale response. All
linear terms cancel by hydrostatic mass multiplier, signed MOND B'=4piG rho,
and the actual scale equilibrium. The matter term is not dropped or replaced
with a Newtonian discrepancy. Taylor integration is used only in the capped
scalar scale variable and in the positive-density entropy, never as a
weighted potential-space Taylor theorem.

The root proof provides an explicit sufficient version. Let C=4piG,
P=length(I)*integral_I 1/A, qcap=sup_|theta|<=1/4 |B_chi(g,a exp theta)|,
K=sup_(x,theta)|W_chichi(|g|,a exp theta)| and L=sup_x qcap²/A,
with the zero value at the center. Require K+L/k<=S0/2 and
3 C rho_max P/cs²<=k/2. Then

DeltaE >= integral cs²r²/(6rho) + k integral A psi'^2/(4C)
         + J integral eta'^2/(2C) + S0 integral eta²/(4C).

The crossing gives P->0, K->0, L->0 on restriction, so the gates are nonempty
without changing coefficients. The independent frozen reviewer derives a
compatible alternative using a scale-gradient endpoint estimate to absorb
the scale remainder. Its sufficient constants need not equal the root's.
The root's a-prime notation inside F means a shifted parameter, explicitly
clarified in its proof; no differentiation ambiguity enters the result.

The decisive distinction from FGF037 is the inequality direction and domain.
Large positive energy for weighted-small concentrations is fully compatible
with this lower bound. Weighted nonlinear continuity, a quadratic upper bound,
and an everywhere finite nonlinear energy on the completed linear domain
remain refuted. The singular infinite-energy states are excluded here.

Remaining gap: the pointwise density cap is an assumption and is not controlled
by the displayed L2 distance alone. FGF039 specifies a distinct exact
mass-constrained entropy elimination test to seek a lower bound without that
cap, retaining finite action and the scale cap. It must also test which caps
energy can control. That task is ready, not launched or proved. Even success
would not replace a nonlinear Cauchy and energy-conservation theorem.

All evidence is proof-only; no mathematical run, numerical radius, measured
parameter or empirical likelihood was produced. Both a0 choices and separate
vacuum/frozen-H/evolving-H hypotheses remain. Q is diagnostic, with locally
responsive scale an added premise. No RAR/M/filtered-MONO, metric/photon/DOF,
physical scale reservoir or calibrated cluster gate is promoted. FGF031
calibration stop and primary AS228 repair ownership are unchanged.

## Evidence pins

- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-038/fgf038_run_001/result.json` SHA256 `c88bd2ebd307653d98dbabdd3588f98900f312e1db13093265c76c8dcea51bc6`.
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-038/fgf038_run_001/DERIVATION.md` SHA256 `3891484b03b38d8697155d9a28a3eaa6344a0337f7c8504c4adf510ef23f86d1`.
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-038/fgf038_run_001/REPORT.md` SHA256 `e0e1c47de5859972232d3739bb485742e7b2e8e940faed3b1eabd758a5287fec`.
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-038/fgf038_run_001/input_sha256.json` SHA256 `9d1e8beff626d246306195ae601387eca59079044ac9908661b5b9e83836dd76`.
- `campaign_fresh_gravity_astra/stage_25/relative_energy/INDEPENDENT_AUDIT.md` SHA256 `4fbacf208db6310af8396f3f99ac0e75c60d4176b63b7e38998706dd233c5f62`.
- `campaign_fresh_gravity_astra/stage_25/relative_energy/PROOF_COMPARISON.json` SHA256 `2a07ce6393de0df42df12675faa919d7ccfe35667f6b02aa062ad8887afb09ec`.
- `campaign_fresh_gravity_astra/stage_25/relative_energy/PROOF_RECORD.json` SHA256 `d333bee0ab4897cf88355c0d66294f337c7c2a1922e527dd303eb44861a953fb`.
- `campaign_fresh_gravity_astra/stage_25/relative_energy/ROOT_DERIVATION.md` SHA256 `404901535858dee0c368dd879c16cd329627ef372d1fa5e001e08af544056817`.
- `campaign_fresh_gravity_astra/stage_25/relative_energy/audit_result.json` SHA256 `3f0a467b1690423facd4ea3c5ccddfba1732bece07f78e098a56514c0b20dbc6`.
- `campaign_fresh_gravity_astra/stage_25/independent_audit/DERIVATION_FROZEN.json` SHA256 `f78b0616cb9b973e5901b62b492d0be0be618fec6898ecedff6524ce2f4b6631`.
- `campaign_fresh_gravity_astra/stage_25/independent_audit/FROZEN_ENERGY_DERIVATION.md` SHA256 `3030def73e0c3aaac2624899143b87f432f1397a993a30560279bec6fe98695a`.
- `campaign_fresh_gravity_astra/stage_25/independent_audit/INDEPENDENT_AUDIT.md` SHA256 `8e45e4970f10bc5dd42123afbf9206f49e50c7d313dfc2280b16bf6102615097`.
- `campaign_fresh_gravity_astra/stage_25/independent_audit/audit_result.json` SHA256 `f0e8fb0f00efa8c7de799f39beb10fbad7bc9e3a51d48fbe66df46d8418d08ff`.

Reconciled 2026-09-30T19:41:24.371422+00:00.
