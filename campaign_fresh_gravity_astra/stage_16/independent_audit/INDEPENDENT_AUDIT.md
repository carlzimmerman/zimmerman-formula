# Independent FGF030 fixed-physical-unit audit

**Verdict: proved as written, within the stated conditional Q diagnostic fixed-wall model.** The worker's uniform four-reference gap and first-turn theorem are sound. The separate root certificate gives a valid stronger common gap. Neither is a calibrated physical selection or a completed gravity theory.

## Independence and evidence type

The auditor derived and froze ANCHOR_DERIVATION.md at the recorded 2026-09-30T10:31:54.556928+00:00 receipt before reading either new FGF030 proof. It uses only the task and pinned FGF027 parent. That independent route already obtains the common-unit ODE and quadratic/kinetic forms, a coarse uniform turn enclosure, and gap 224850/11. Afterwards the worker and root derivations, code, contracts, manifests and results were proof/code reviewed. No new mathematical program, ODE integration or spectral mesh was executed by this auditor. Current-file hash verification is metadata validation, not an independent numerical experiment or runner manifest.

## Physical scaling checked independently

Set C=4piG, Lc=cs²/ac, tc=cs/ac, rho_c=ac²/(C cs²), phi_c=cs² and Ec=ac cs²/C. With xi_phys=Lc xi, psi_phys=cs² psi, unchanged eta, every potential-energy term has scale Ec and every physical kinetic-mass term has scale Ec tc². In particular the fluid coefficient is rho_c Lc³=Ec tc²; the psi coefficient is (K/c²)cs^4 Lc/C=Ec tc²; the eta coefficient is (J/vchi²)Lc/C=Ec tc². This uses the prescribed fixed J=cs^4, S0=ac², K=c²/cs², vchi=cs.

Thus alpha=a_ref/ac occurs in a=alpha exp(chi), not in U=(cosh(2chi)-1)/4, the interval D=.01, the initial slope, or either field inertia. The physical frequency conversion is omega²=(ac/cs)² Omega² for all four cells. Inserting alpha² there or into U would change the specified physical problem. The canonical and alternative normalizations and their separate frozen H(z=1) references all lie in the proved interval [1,11/5]. The initial constitutive force satisfies f0²=1+alpha; it cannot be held at 2 in the other cells. The inherited MOND source law remains b'=r, with physical force ac sqrt(b²+ab).

## Worker proof checked

The constitutive identities A=2f/(2b+a), q=fA-b=(a/2)(1-a/sqrt(a²+4f²)), T_f=q and m=cosh(2chi)-2T+fq have consistent signs and dimensions. The last identity uses differentiation at fixed f and fixed reference alpha, giving T_chi=2T-fq. On the bootstrap box, a is between .99 and 9/4 and f between 1.3 and 2. The actual-point A lower bound 52/89>1/2 and q<9/8 are valid.

The nontrivial integral lower bound is valid separately for its integration variable: on v in [13/20,13/10], 1+4v²/a²>2701/2025>(23/20)², hence q(v,a)>297/4600 and T>3861/92000>1/25. This does not misuse the actual-point q bound inside the integral. Combined with T<9/4 and |sinh(2chi)/2|<.011, it gives -23/10<w'<-1/40. All first-exit margins are strict: b<=1.011, r>=.978, |chi|<=1/4000 and -.0229<=w<=.0001 remain inside the box with |w|<=.025. Smoothness on this compact regular set supplies ODE continuation through D, not merely sampled containment. The first turn is uniquely bracketed by (1/23000,1/250); D exceeds it by more than 3/500 in common anchor length units.

The Hessian retains material displacement, potential and scale perturbations on H1_0(0,D)^3. The fluid bound uses (a-b)²>=a²/2-b². The matter cross term integrates to 2 integral r xi psi' with endpoint -2[r xi psi]=0. Each coupling spends only A/4 of the psi' stiffness. The respective negative penalties are 352/25 and 109/8, so Q2>=.25||u'||²-15||u||². All components use fixed dimensionless anchor units; no dimensional fields are added without scaling. Poincare with pi²>9 gives derivative coercivity 1499/6000, L2 lower bound 22485 and N<=1.1||u||², hence inf Q2/N>=224850/11>20400. The positive kinetic norm and coercive regular closed form on this finite fixed interval support the stated linear spectral lower bound. No static field elimination, discarded rank-one term, w division or endpoint singularity is used.

Fixed zero field traces imply zero linear field-energy flux, and zero material displacement fixes mass within each equilibrium. Background right field values, wall pressure and total mass can differ across references. This proves existence for IVP-induced boundary data, not arbitrary externally prescribed equal right data or a same-total-mass comparison.

## Separate root proof checked

The root uses a different conservative box and actual-point bounds. A²=1-[a/(2b+a)]²>=56/81>(4/5)² and q=ab/(2b+a)<=99/178<3/5 follow from monotonicity on the box. Its distinct integral argument gives T>1287/40000>.03; w' lies in (-227/100,-19/1000), giving turn bracket (1/22700,1/190) and post-turn length >9/1900. The sharper Young penalties 209/20<11 and 53/10<6 give Q2>=.4||u'||²-11||u||², derivative coefficient 35989/90000 and common gap 359890/11>32700. This uses the same anchor physical frequency factor. These different enclosures are compatible; shared lower bounds do not imply equal spectra, profiles or turn locations. The worker's tighter turn enclosure and root's stronger gap can both hold for the same task-prescribed family by IVP uniqueness.

## Arithmetic, provenance and controls

Worker certificate code contains 77 exact Fraction checks, with recorded Python 3.9.6 run time .047572 seconds. Root certificate records Python 3.13.9 run time .024476 seconds. Both runs completed within 120-second wall, 110-second CPU and 1 MiB log limits, with a cooperative one-thread environment cap. The auditor inspected their arithmetic source and result records, and verified every manifest input/output hash against the current files, including before/after input agreement. The worker's separate final result input/artifact pins also match. These finite arithmetic checks support constants in an analytic proof; they do not by themselves establish continuum existence or spectral claims.

The controls correctly reject reference retuning, hidden alpha=1, an insufficient T upper bound, excess Young allocations and a no-turn endpoint assertion. The nonadmissible boundary fixture checks an algebraic integration-by-parts term, not a stability result for those nonadmissible data. The root's D=1 failure means this estimate is uncertified there, not unstable. Some controls are deliberately elementary identities; they do not independently verify the action or physical assumptions.

## Remaining implication

No mathematical gap was found in these bounded conditional claims. The illustrative couplings and induced walls still need physical justification; the task does not discriminate normalizations observationally. Frozen H references are stationary alternatives, not a time-dependent H solution or one shared vacuum density. The locally varying actual a remains incompatible with a literal pointwise constant-vacuum actual-a identity unless a different physical relation is established. The proof supplies no RAR/M action or stability transfer, filtered-MONO or metric/photon coupling, nonlinear/3D/free-wall result, observational likelihood or theory closure. Repeating a short-domain mesh spectrum would not resolve those gaps.

## Exact source and result pins

- `campaign_fresh_gravity_astra/stage_16/independent_audit/ANCHOR_DERIVATION.md`: `c8e69740131dea0ee19fd1fa99c36bbf7de5a0ac5d4e4049b6f94e47d2681fc7`
- `campaign_fresh_gravity_astra/stage_16/independent_audit/DERIVATION_FROZEN.json`: `0e97c0eee62edd5eba98237c2de99ebe63170184cde462392e6b1801e1bad899`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/tasks/FGF-030.md`: `94f89d4755f4b14945c1c3ddacfc8f08ee0661a36b5f0e6331dfdad50d619fc4`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-027/fgf027_run_001/DERIVATION.md`: `5ec8588646fb1ca70f9b908b18ce8af5abc466cd478455de379a8a37070b13f6`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-030/fgf030_run_001/DERIVATION.md`: `abf52e6e1b1d385dbbb549ae65045866acdc425c20d089158e42a9bfb9bd6db1`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-030/fgf030_run_001/check_certificate.py`: `de91ba0b1be0078cda299928e060127f012b5c0406c59ba2ce5a4bc2a9fa5922`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-030/fgf030_run_001/contract.json`: `47a1431a5d71a05410ec00f6045cf0c86827647858b9c95cb540256579634874`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-030/fgf030_run_001/result.json`: `0ffa2b8da658ef11ca04a841c5b6799f9d23f560735e194520ff17379d32a6de`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-030/fgf030_run_001/numeric_001/results.json`: `09f572c550e00b5c9c85bc926cf02f9eff69375500fdca0b6ee72952ff60277f`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-030/fgf030_run_001/numeric_001/manifest.json`: `117a21084c776591a328bc7787401a0e87b708f10c4d0012ef7248c2637a4367`
- `campaign_fresh_gravity_astra/stage_16/fixed_units/ROOT_DERIVATION.md`: `bf0b7efb7d3b8df1a26ae3761f398e25e04e5614ee6dbddf1d1b3d56882c4164`
- `campaign_fresh_gravity_astra/stage_16/fixed_units/check.py`: `0eca275af4bc261ad9063eee57bc674eb43aa866934e356a0d4273379f00fed9`
- `campaign_fresh_gravity_astra/stage_16/fixed_units/contract.json`: `cbf764f921653953f8e08fad780d11533cba13081698074e983f42464e42ef5e`
- `campaign_fresh_gravity_astra/stage_16/fixed_units/run_001/results.json`: `b708b84a66f0ea6f4b5a6be039de3ad25e8e93ab9b8133d4386d2cf96e4431d9`
- `campaign_fresh_gravity_astra/stage_16/fixed_units/run_001/manifest.json`: `0e70ea73debaf61d4efe7e0df47e8d51cb94afa130a2cb60dbc201f18b598f81`
