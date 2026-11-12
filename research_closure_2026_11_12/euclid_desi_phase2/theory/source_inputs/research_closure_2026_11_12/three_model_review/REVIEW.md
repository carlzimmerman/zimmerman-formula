# Fable HY4 and DeepSeek closure review

> Follow-up: the requested repairs and combined-route investigation are recorded in [the new result](../combined_route/RESULT.md). This review remains the original dated assessment; its source inventory describes the pre-correction revisions.

12 November 2026. The theory is not closed. The useful next step is a single, consistently defined dynamical model, tested with corrected mass accounting and external fields. Several recent claims of either success or impossibility do not follow from their supporting calculations.

The most promising synthesis is conditional: retain a conserved cold field, distinguish its initial cosmic abundance from its mass relative to the baryons remaining in a galaxy, and investigate an environment-dependent transition radius. Neither retention nor that transition has yet been derived. This is a research target, not a new completed theory or an adoption of a previously retired model.

## Coverage and evidence

Reviewed the current Fable 5.2 and HY4 inventories, their closure/framework documents, the latest formation, amount, coefficient, perturbation and observation lanes, and DeepSeek G238–G242 plus the DSF-21 structural errata. Followed central claims into code and earlier dependencies. Three separate reviewers covered Fable, HY4 and DeepSeek; the coordinator reconstructed decisive algebra and numerical witnesses. This is a substantive review of the latest relevant work, not an execution of every historical lane, simulation, data likelihood or Lean certificate.

The checkout was already dirty and contains many untracked research artifacts. Initial HEAD was `e8d96b729f231ab028f5391402f89dc897f7a20c`; during review another session committed G242 at `d215a3d278267accee5a39ca5b689e34a2c171bf`. Current G242 was read after that commit. At inventory time HEAD was `aa235e9fb2b71a10e1e632e4c9d4940bf7838f27`, adding criteria for FINAL-7F, with no new result in that commit. `source_inventory.json` pins the reviewed artifacts individually. Existing research files were not edited, and nothing was committed or published by this review.

The new bounded arithmetic/analytic witnesses are in `check_witnesses.py`, with a validated computation record in `run_001/manifest.json` and outputs in `run_001/witnesses.json`. These checks establish the stated counterexamples; they do not establish viability of any replacement theory.

## What the three efforts contribute

| Work | Useful surviving contribution | What it has not established |
|---|---|---|
| Fable 5.2 | Explicit equations and static identities; detailed separation of cosmological and galaxy states; useful formation bookkeeping and data tensions | A healthy evolution from cosmological initial conditions through shell crossing to the required galaxy and cluster states |
| HY4 | Concentrates attention on amount, reach, stress and normalization; many useful conditional algebraic checks | A universal observed-baryon mass cap, a physical gauge fixing kappa, or a temperature-independent decisive gas test |
| DeepSeek | External-field truncation is a concrete physical candidate; the newest G242 supplies a conditional environmental scaling | A matched AQUAL/QUMOND comparison, a unique completion selected by field ontology, or simultaneous forest/lensing closure |

The exact galaxy identities are conditional on the chosen interpolation law and static state. Lean can certify those implications. It does not supply their physical premises, a post-caustic evolution, a correct data model or a coefficient derivation.

## Findings that change the closure decision

### 1. The cosmic ratio is not a universal cap per observed galaxy baryon

**Verdict: correct only after a stated restriction.**

CRUX step 4 uses `M_c <= 5.41 M_b` as an entire budget. The derivation in FINAL3 assumes that the initial catchment and the present collapsed patch coincide, with the relevant baryons retained. Conservation alone is weaker.

Let an initial patch contain baryonic mass `M_b,i` and cold mass `R M_b,i`, where `R=5.41`. Define retained fractions `F_b=M_b,obs/M_b,i` and `F_c=M_c,obs/(R M_b,i)` for that same patch. Then

    X_obs = M_c,obs / M_b,obs = R F_c/F_b.

Thus `X_obs=59.5` requires `F_b/F_c=0.0909244`. It does not by itself require new cold charge. This is already acknowledged in [the share audit, lines 218–223](/Users/carlzimmerman/new_physics/zimmerman-formula/closure_2026_11_11/FINAL3_share_derivation/CLOSE3_A_SHARE_DERIVATION.md:218); the same audit ends with a lane-level NO VERDICT and an uncomputed basin branch.

This correction does not make 9.1% retention plausible or derived, and it does not move missing baryons wherever convenient. A successful model must predict the catchment, transport, retained fractions and surrounding baryon inventory using inputs independent of the mass discrepancy. The observed lensing can also include correlated neighboring structure, which must be modeled before assigning it to one halo.

**Cheapest next check:** reconstruct one host-free lens bin using a common initial patch, explicit cold and baryonic fluxes, and independently constrained baryon retention. Test the required ratio rather than imposing `X=59.5` or `X=5.41` as the answer.

### 2. DeepSeek's large external-field rescue compares different environments

**Verdict: refuted as written.**

G240 supplies the same number `0.01273` to a QUMOND Newtonian external field and an AQUAL physical external-field boundary. These are not the same boundary condition. For the simple interpolation pair,

    mu(x)=x/(1+x),  y_e=x_e mu(x_e),
    x_e=(y_e+sqrt(y_e^2+4 y_e))/2.

At `y_e=0.01273`, the matched physical field is `x_e=0.1193716955`. The approximate transition scales are then `8.3772 r_M` and `8.8631 r_M`, not a factor-six separation. The same interpolation pair must also be used; G239's exponential kernel and G240's simple kernel are another distinction.

G240's analytic asymptote has a separate sign/normalization/angular-average error. Linearizing its own AQUAL equation gives

    mu_e (Laplacian + L_e partial_z^2) deltaPhi = 4 pi G rho,
    M_eff/M_b = atan(sqrt(L_e))/(mu_e sqrt(L_e)).

At physical `x_e=0.01273`, this is `62.6253`, agreeing closely with the recorded numerical `62.49–62.54`; the report instead declares `21.42` correct and the numerical result unconverged. At matched external fields, the same-simple-kernel far-field monopoles are AQUAL `7.51247` and QUMOND `7.90236`, about 5% apart. This does not replace a finite-radius solve, but it invalidates the stated interpretation of that solve.

Sources: [G240 code](/Users/carlzimmerman/new_physics/zimmerman-formula/deepseek_push/G240_aqual_plateau/g240.py:124), [solver boundary](/Users/carlzimmerman/new_physics/zimmerman-formula/qwen_claude_field_theory/theory_2026/aqual_solver_2026.py:90), [recorded plateau](/Users/carlzimmerman/new_physics/zimmerman-formula/deepseek_push/G240_aqual_plateau/g240.out:40). The reconstructed Green function agrees with [Banik and Zhao, equations 11 and 18](https://arxiv.org/html/1509.08457v3).

**Cheapest next check:** rerun the existing solver with the matched physical boundary, one fixed interpolation pair, two resolutions and the corrected asymptote. Compare the measured radial range with its covariance; derive `r_200c` self-consistently rather than identifying `M(<200 kpc)` with `M_200c`.

### 3. G242 supplies a candidate scaling, not a derived settling mechanism

**Verdict: conditional on named physical inputs.**

The newest committed lane assumes

    g_ext = sqrt(G rho_m a0 R_struct),
    R_set = r_M/(g_ext/a0) = sqrt(M_b/(rho_m R_struct)).

The cancellation is correct under those assumptions. However, an external-field transition radius is a static response scale; identifying it with the radius where a conserved medium settles is an additional dynamical hypothesis. `R_struct`, its evolution, the relevant environment and halo assembly remain physical inputs.

G242's fixed-mass ratio is `0.608705`, while the proxy bounds require at most `0.56`. Its latest README correctly notes this failure and shows that a growth factor above `1.64935` would open the two-endpoint ratio window. The growth factor is a condition, not computed assembly; a normalization freedom remains. The forest and lensing populations also need a justified mapping before they can be treated as progenitors and descendants. Neither the forest likelihood nor the host-free lensing stack was rerun. Opening that proxy window is not proof that the original likelihoods pass, and the preceding G240 empirical calibration needs correction.

Source: [G242 README](/Users/carlzimmerman/new_physics/zimmerman-formula/deepseek_push/G242_settled_radius_efe/README.md:14), [explicit missing inputs](/Users/carlzimmerman/new_physics/zimmerman-formula/deepseek_push/G242_settled_radius_efe/g242.py:195).

**Cheapest next check:** obtain environments and progenitor growth from an independent catalog or fixed simulation, predict the whole radius history without fitting the two gate values, and then run that history through both existing observable pipelines. If it survives, derive or falsify `R_set=R_EFE` from the evolution equations.

### 4. Fable's two-variable gate is not invisible in linear perturbation theory

**Verdict: the stated linear-invisibility theorem is refuted; full viability remains unresolved.**

PIK1 argues that its first-order action contribution is a boundary term, then concludes that the linear field equations are unchanged. Linear equations depend on the second-order action. For

    L_K = A (Q-1)^2 S(Pi/Pi_c),  A=mu_K^2/(2K),

the quadratic terms include

    A [2 (Qbar-1) S'(0) deltaQ deltaPi/Pi_c
       + (Qbar-1)^2 S''(0) (deltaPi)^2/(2 Pi_c^2)].

They are generically not boundary terms. Choose the lane's admissible `S(u)=exp(-u)`, constant `Qbar>1` on a spatial slice and periodic `P=-epsilon cos(s)`, so `deltaPi=epsilon sin(s)`. The first-order spatial integral vanishes but the quadratic contribution is positive, proportional to `pi epsilon^2/2`. Its variation changes the linear polarization equation.

The separate monotone-ordering argument compares values near different systems' outer radii; it does not establish an ordering of their different weighted integrals without additional profile/weight hypotheses. The promised full static solve was not completed. This does not show that the proposed gate works. It means the broad exclusion is not established by this lane.

Source: [PIK1 purported theorem](/Users/carlzimmerman/new_physics/zimmerman-formula/fable52_push/PIK1_pi_gated_dust/RESULT.md:108), [its own modified constitutive equation](/Users/carlzimmerman/new_physics/zimmerman-formula/fable52_push/PIK1_pi_gated_dust/RESULT.md:49).

**Cheapest next check:** fix one explicit gate, derive the full constrained quadratic action and compare it with direct linearization. Stop if it is unhealthy. Only if that passes should the galaxy/cluster solutions be recomputed; the old Jeans bound cannot simply be inherited unchanged.

### 5. The promised flat gas plateau and universal 100-sigma decision are not established

**Verdict: spherical projection claim refuted; forecast conditional.**

FINAL5 identifies the spherical enclosed-mass quantity `M(<r)/(pi r^2)=Sigma0` with the projected column. For its own model,

    M(<r)=pi Sigma0 r^2  =>  rho(r)=Sigma0/(2r),
    Sigma_proj(b)=Sigma0 acosh(R_out/b),  0<b<R_out.

For `R_out=2.6 Mpc`, the column factors at `b=0.3,1,2 Mpc` are `2.8493,1.6094,0.75643`, and the column tends to zero at the edge. It is not flat. The code contains the spherical option, but its headline result uses the flat-sheet default. That default is not a lower bound throughout the radius interval. Its emission-measure code correctly uses an arccos/arctan expression; the prose incorrectly calls it arccosh.

Moreover, `y=(sigma_T/(m_e c^2)) integral n_e k_B T_e dl` measures electron pressure. A conversion to gas column requires temperature information. The noise forecast also imports map-noise scaling rather than measuring the proposed stack covariance. A tSZ stack is useful, but it cannot yet be presented as a guaranteed, temperature-independent closure measurement. The density/temperature issue and the relevance of correlated halos are explicit in [Tanimura et al., MNRAS 491, 2318](https://academic.oup.com/mnras/article/491/2/2318/5614507).

Sources: [FINAL5 result](/Users/carlzimmerman/new_physics/zimmerman-formula/hy4_preview_push/FINAL5_measurement/RESULT.md:18), [projection implementation](/Users/carlzimmerman/new_physics/zimmerman-formula/hy4_preview_push/FINAL5_measurement/final5_signal.py:73).

**Cheapest next check:** specify one 3D gas profile and temperature model, project it consistently through the instrument beam and map filtering, include correlated structure, and estimate the covariance on the actual lens sample. Use independent temperature or electron-column information when interpreting a non-detection as a mass bound.

### 6. Kappa remains a measurable physical coefficient

**Verdict: neither 1/2 nor the rate-lock value is dynamically derived.**

The dimensionless ratio `kappa=a0/(c sqrt(G rho_Lambda))` cannot be set by a change of ordinary units. Holding measured baryonic masses and radii fixed, changing `a0` changes the predicted accelerations. Covariance of a ratio under simultaneous rescaling is not a gauge symmetry of the action and observables.

HY4's proposed clock relabeling also fails for the stated rate-dependent action: under `tau -> 2 tau`, `Q -> 2Q` with the leaf geometry fixed. `V_Sigma/Q` halves, and at initial `Q=1`, the term `mu_K^2(Q-1)^2/(2K)` changes from zero to `mu_K^2/(2K)`. A physical clock-rate condition must be added and justified; it cannot be hidden as gauge fixing.

OUT-2 imposes `a0/c=H_Lambda/(2pi)`. Conditional algebra gives `kappa=sqrt(2/(3pi))=0.460658866`, about 7.87% below 1/2. The rate lock is the missing physical premise. Dimensional analysis restricts possible forms after the allowed inputs are chosen; it neither evaluates the coefficient nor proves that future dynamics cannot do so. Even the statement that a time-independent normalization uniquely selects dark energy requires extra assumptions about which densities and reference epochs are allowed.

Sources: [FRAMEWORK](/Users/carlzimmerman/new_physics/zimmerman-formula/hy4_preview_push/FRAMEWORK.md:38), [clock relabeling premise](/Users/carlzimmerman/new_physics/zimmerman-formula/hy4_preview_push/OUT-3_kappa_equality_fixed/FROZEN_CRITERIA.md:21), [rate-lock disclosures](/Users/carlzimmerman/new_physics/zimmerman-formula/hy4_preview_push/OUT-2_kappa_ratelock/RESULT.md:198).

**Next step:** retain kappa as a globally fitted coefficient while testing dynamical consistency. Keep exact 1/2 and the thermal value as distinguishable hypotheses. A consistent effective theory with a fitted coefficient would be a meaningful achievement; it would not finish the stronger first-principles normalization claim.

## Additional issues that must not be inherited

- **Different galaxy laws are called the same law.** FRAMEWORK uses both `g^2-g_b^2=a0 g_b` and `g_b=g^2/(g+a0)`. At `g_b=a0` they give `sqrt(2) a0` and `1.61803 a0`, differing by 14.4%. They share a deep limit but are not equivalent. Choose the action's exact kernel before transferring predictions.
- **DT2 has landed despite the stale door inventory.** Its specific band is below the density visited by the early collapsing material; this is a useful scoped obstruction. However, `dt2_form.py:61` and `dt2_reach.py:28` integrate `1/(aH)` against `d ln a`; the correct cosmic-time factor is `1/H`. `dt2_linear.py:53` uses `3+d ln H/d ln a` for a derivative with respect to `ln a`; the stated pressureless growth equation requires `2+d ln H/d ln a`. In an Einstein–de Sitter limit, its declared growing-mode initial condition `delta=a` fails the implemented reference equation. Repair before using times or its growth pass. Its own RESULT lines 156–164 do not exclude all band placements or post-caustic completions.
- **The formation class scores are retrospective.** Fable's FRM1 disclosure says the class data were known before the bands were frozen. The cluster ceiling additionally assumes a restricted retention/geometry history; it is not a theorem excluding every transfer history. It supplies a target ledger, not a predictive formation model.
- **G238's slope is generally a mean-density slope.** If `p=d ln M/d ln r`, the local slope is `p-3+d ln p/d ln r`. The omitted derivative vanishes for a power law. For `M=C(r+b)`, local density is exactly proportional to `r^-2`, whereas the proxy is `-2-b/(r+b)`. Rebuild the claimed local-density falsifier.
- **G241 tests some conclusions by construction.** `M_QUM` returns `M_MI`, and the decisive field-to-AQUAL test is hard-coded `True`. Milgrom's [1994 circular-orbit result](https://arxiv.org/html/astro-ph/9303012v1) does not prove a general algebraic modified-inertia EFE. [QUMOND's field equation](https://arxiv.org/html/0911.5464v2) also differs from pointwise algebraic acceleration. Field ontology alone does not select AQUAL.
- **DSF-21's own erratum supersedes its first-class-algebra closure claim.** Its README at line 144 says that classification was false and that the Lean algebraic certificates did not certify it. This is scoped to that action, not a refutation of the separate v3 action.
- **FINAL4 is not a first-principles growth derivation.** Its own displayed reference includes baryon pressure and drag, so equal baryon/cold perturbations are not exact without further limits. Its settled-fraction evolution and the imported halo redistribution/forest test are separate modeling steps. The large quoted discrepancies are evidence against those specified models, not universal exclusions of every formation history.
- **A failed member is not a failed class.** CLOSE2 explicitly distinguishes its amended “member sense” closure from a theorem covering both multivalued-carrier branches. M5's exact-equilibrium argument assumes a particular local stress class and the law for every baryon distribution. Neither supplies an unrestricted theorem that all field-based history-dependent completions are impossible.

## A concrete path to closure

The objective should be stated as two separate obligations: (A) one healthy predictive dynamical model, and (B) a first-principles derivation of its acceleration normalization. Solving A with fitted kappa does not solve B, but failure to solve B does not excuse leaving A undefined.

1. **Freeze one mathematical model and observable dictionary.** Specify the action or complete evolution system, interpolation function, physical versus Newtonian external field, metric potentials for lensing, conserved charge, initial composition, aperture and initial patch. Every downstream lane must use those definitions. Resolve the 14.4% kernel discrepancy first.
2. **Repair the three calculations with immediate discriminating power.** Run the matched external-field comparison; derive the PIK1 quadratic action; correct DT2's time and growth reference. This is much cheaper than another broad search and determines which existing constructions deserve further computation.
3. **Make formation predict amount and radius together.** The next theory target is a source-free evolution that predicts `F_c/F_b` and a transition radius from independently specified initial conditions and environments. G242 supplies a possible radius scaling; the corrected mass ledger supplies the amount requirement. The model must also continue through crossing/folding, account for energy transfer, and reach a stable state. Choosing retention, damping, a front or the observed law independently for each galaxy is not a solution.
4. **Use one development case and two held-out stress tests.** Start with a resolved isolated disc, then a hosted dwarf and a cluster using the same coefficients and measured inputs. Derive the synthetic rotation, lensing and baryon profiles. In parallel, send the same formation prescription through the forest and growth calculation. A failure must identify the assumption it rejects; a pass on one case is not cross-scale closure.
5. **Only then return to exact kappa.** A viable action may expose an independently calculable ratio of coefficients. Without that, selecting a horizon, epoch, equality or rate that algebraically reproduces the desired number is only another normalization condition.

The first new physical implication worth testing is therefore: **the same field evolution and environment predict both the amount of cold mass relative to retained baryons and the radius/history of its galactic response.** This is more precise than “find a mechanism,” and it is not supplied by any of the three latest programs. It might fail. The present review establishes neither its existence nor uniqueness.

No existing retired route is reinstated here. Any new candidate must explicitly differ at the failed assumption and face its predecessor's data and stability checks. The broader goal remains open; the review provides corrected decision points and a bounded next research program.
