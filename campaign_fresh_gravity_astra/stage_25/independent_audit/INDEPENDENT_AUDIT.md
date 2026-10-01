# Independent audit of FGF038

**Primary verdict: proved as written**, for the explicit capped finite-action class on sufficiently short induced-wall Q crossing intervals. The proof earns a strict restricted static energetic minimum and an exact lower distance bound. It does not earn nonlinear evolution, cap preservation or dynamical stability, and does not repair the failed FGF037 upper/Taylor implication.

## Normalized claim and independence

Fix the same inherited central Q solution and positive physical coefficients. For every sufficiently short symmetric restriction satisfying alpha<=k/4 and beta<=1/4, with k=exp(-1/4)/64, all Eulerian comparison states satisfying integral r=0, abs(r)<=rho/2, psi,eta in H1_0 and ||eta||infinity<=1/4 obey

    Delta E >= E_r/6 + (k/4)E_p + E_eta/4
                         + S0 int eta²/(2C),

where E_r=int cs²r²/rho, E_p=int A psi'²/C and E_eta=int J eta'²/C. There is no imposed supremum bound on the potential gradient. The walls and mass are fixed for each comparison, but change across the family of background interval restrictions.

The auditor froze FROZEN_ENERGY_DERIVATION.md at 2026-09-30T19:35:47.876638+00:00, SHA256 3030def73e0c3aaac2624899143b87f432f1397a993a30560279bec6fe98695a. No new author/root proof or formula preview had been read. The task suggested a global scalar inequality as a possible route; the auditor independently derived its constant and the full coupled bound before viewing the author's derivation. Author readiness and source inspection occurred afterward. The new stage25 root proof was not read. No author edit was requested.

The independent freeze obtains the same scalar constant 1/64, density coefficient and final energy coefficients. It uses an explicit background scale-remainder bound in place of the author's qhat/Dhat suprema; these are distinct valid sufficient estimates and need not give identical allowable interval sizes. Post-freeze comparison checks the author's actual suprema and gates below.

This mathbox proof audit ran no numerical or symbolic experiment, spectrum or scan. Python was used for file hashing, JSON validation and writing this record only. All 11 worker input hashes, all 3 worker artifact hashes, 5 independent source pins, frozen-proof identity and required result-contract fields matched. Additional ancestor hashes were checked as provenance, not represented as fresh audits of every old proof. No numerical manifest or enforced computation bounds are claimed.

## Dependencies and obligation matrix

The chain is: pinned action/crossing and weighted endpoint control -> exact complete energy identity -> global signed scalar inequality -> finite-scale decomposition -> entropy and mixed-term estimates -> two same-solution shortness gates -> strict restricted minimum. The old action/crossing facts are pinned ancestors; every new implication uses internal exact algebra or elementary integral inequalities. There is no external theorem or computation-dependent leaf.

| Obligation | Status | Decisive evidence |
|---|---|---|
| Finite-action comparison class | Passed | Density and scale caps, H1 potential/scale, fixed mass and walls |
| Complete first-variation cancellation | Passed | Hydrostatic multiplier, signed B'=C rho and scale equation |
| Global scalar constant | Passed | Two segment cases give 7/64 or 1/64, with zero and sign controls |
| Finite scale change | Passed | Exact decomposition at the new scale; only background coefficients enter adverse terms |
| Density curvature cap | Passed | Exact integral entropy formula gives E_r/3 |
| Retained couplings | Passed | Both r psi and finite scale flux change explicitly estimated |
| Shortness and units | Passed | alpha=O(d^(3/2)), beta=O(d^(7/2)); both dimensionless |
| Uniformity over comparison states | Passed | Coefficients depend on background and fixed caps, not potential-gradient size |
| Strictness | Passed | All lower distances vanish only for the background |
| Nonlinear evolution and cap invariance | Out of scope | No conservative nonlinear solution class or invariant-region proof |
| FGF037 upper/Taylor control | Remains refuted | Positive large exact energy is compatible with a lower bound |

## Exact energy and admissibility

A measurable r with the prescribed cap is bounded and leaves rho+r between rho/2 and 3rho/2 on the compact interval. H1_0 perturbations have bounded continuous representatives in one dimension. Thus a exp eta is bounded positive, new density/internal energy is integrable, interaction terms are finite, and g+psi' lies in L2. The exact Q field energy has at most quadratic growth, so all comparison energies are finite. These are admissible states, not claimed to solve the field or hydrostatic equations. The Eulerian r is not identified with an exact finite material-displacement map.

Writing H_r=e(rho+r)-e(rho)-e'(rho)r, U_rel=U(chi+eta)-U(chi)-U'(chi)eta and

    F_rel=W(abs(g+psi'),a exp eta)-W(abs(g),a)-B psi'+T eta,

direct expansion yields Delta E=int(H_r+r psi)+int(F_rel+J eta'²/2+U_rel)/C. The r-linear term is the hydrostatic constant e'(rho)+phi times r and integrates to zero by fixed mass. The potential-linear terms cancel because int B psi'=-C int rho psi, using the actual signed MOND source. Scale-linear terms cancel because int[J chi' eta'+(U'-T)eta]=0. The background regularity and zero outer traces justify these identities on the whole interval; no center boundary term is inserted. The surviving r psi is essential. The plus sign on T eta in F_rel is correct, since the local chi derivative of W is -T.

## Global scalar bound and sign controls

For fixed a let V_a(y)=W(abs(y),a). It is C2 in signed y, with second derivative A(abs(y),a)=2abs(y)/sqrt(a²+4y²). Its exact remainder is z² int_0^1(1-t)A(abs(g+t z),a)dt. Monotonicity of A and A(s/2)>=A(s)/2 give the stated constants:

- For abs(z)<=2abs(g), the segment t in [0,1/4] stays at magnitude at least abs(g)/2. Its weight integral is 7/32, giving 7A(g)z²/64.
- For abs(z)>2abs(g), t in [3/4,1] has magnitude greater than abs(g)/2 by the reverse triangle inequality. Its weight integral is 1/32, giving A(g)z²/64.

At g=0 the lower right side vanishes and convexity supplies the result; z=0 is exact equality. These statements cover negative g, opposite signs, internal segment zeroes and unbounded z. As a separate algebraic reversal check, z=-2g has exact remainder 2abs(g)b(abs(g),a). Its ratio to A(g)z² is sqrt(a²+4g²)/[2(sqrt(a²+4g²)+a)]>=1/4, comfortably above 1/64. No same-sign premise is hidden.

This integral identity is exact; it does not assume a uniform Taylor approximation in the weighted norm. The constant is conservative rather than optimized or fitted.

## Finite scale response and a direct global remainder check

The author's k=exp(-1/4)/64 follows from A(s,a exp eta)>=exp(-1/4)A(s,a) for either sign of eta within the cap. Decomposing at a exp eta keeps the first scalar remainder global in the new gradient, but places the flux difference and pure scale remainder at the fixed background gradient. Their derivatives are -sgn(g)q and -D respectively, with

    q=s A-b=a b/sqrt(a²+4s²),
    D=T_chi=2T-sq.

Thus F_rel>=k A z²-qhat abs(eta z)-Dhat eta²/2. Young's inequality correctly gives F_rel>=(k/2)A z²-R eta², with R=qhat²/(2kA)+Dhat/2. The signed derivative and the pure-scale remainder sign both check. At the central zero qhat=Dhat=0, and direct convexity treats the zero point; no undefined division is needed.

The author's uniform background expansions are correct. There is also an exact global check avoiding reliance on their remainder notation. For all s>=0, 0<=q<=b<=s²/a. Since T_s=q and T(0)=0, 0<=T<=s³/(3a), and therefore abs(D)<=2T+s q<=5s³/(3a). Uniformly over theta within the cap,

    qhat <= exp(1/4)s²/a,
    Dhat <= (5/3)exp(1/4)s³/a,
    R <= exp(1/2)s³ sqrt(a²+4s²)/(4k a²)
                                    +(5/6)exp(1/4)s³/a.

This last expression extends continuously to zero and is O(s³) for the actual bounded positive background scale. Since s=abs(g)=O(sqrt(abs(x))), it verifies Rmax=O(d^(3/2)) directly. The suprema themselves are continuous in x: the underlying functions are jointly continuous on compact background/cap sets, so the supremum changes by at most their uniform change. Crucially, these are background coefficient estimates; no bound or asymptotic expansion of the new gradient g+z has been introduced.

The convex cosh potential obeys U''>=S0 globally, so U_rel>=S0 eta²/2 exactly. The frozen independent derivation used the signed upper bound D<=2T rather than abs(D), giving another sufficient scale remainder coefficient. It is not substituted silently for the author's R or gate in this audit.

## Entropy, coupled gates and strictness

The exact entropy remainder is cs²r² int_0^1(1-t)/(rho+t r)dt. The density cap gives rho+t r<=3rho/2, hence H_r>=cs²r²/(3rho), including negative r. The lower cap also preserves positivity and finite entropy; it is not being derived from the energy inequality.

Young's inequality yields abs(int r psi)<=E_r/6+(3rho_max/(2cs²))||psi||_2². Weighted endpoint Cauchy gives ||psi||_2²<=ell I_A int A psi'², hence precisely alpha=3C rho_max ell I_A/(2cs²). The finite-scale penalty obeys int R eta²/C<=beta E_eta with beta=ell² Rmax/J. Collecting every term gives

    Delta E >= E_r/6+(k/2-alpha)E_p
                 +(1/2-beta)E_eta+S0 int eta²/(2C).

The author's gates alpha<=k/4 and beta<=1/4 therefore yield the advertised lower coefficients without a missing factor of two. On restrictions of the same central solution, rho extrema remain positive and bounded, I_A=O(sqrt(d)) and Rmax=O(d^(3/2)); alpha and beta tend to zero as claimed. All coefficient caps and physical parameters are held fixed while the interval is shortened. The resulting statement is existential in physical interval size, with explicit sufficient gates and no numerical radius.

The quantities alpha and beta are dimensionless: C rho_max ell I_A/cs² and ell² Rmax/J have that form. q has acceleration units, D and R acceleration-squared units, and every term in the final lower bound has energy-per-transverse-area units. Fixed physical reference units are retained.

If Delta E=0, the positive lower terms force r=eta=0 and A psi'²=0 almost everywhere. A is positive except at one point, so psi'=0 almost everywhere; H1_0 then forces psi=0. Strictness is valid in the stated capped finite-action class, including arbitrarily large finite L2 potential gradients. It is not an assertion that comparison states obey an evolution or preserve their caps.

## Scope and remaining implication

The FGF037 singular completed directions are outside this finite-action class and still have infinite exact energy at nonzero amplitude. Its smooth concentrating sequences have large positive exact energy and small weighted distance, which is consistent with the present lower bound. No upper control, weighted continuity or uniform quadratic Taylor estimate is recovered. The earlier weighted linear theorem remains separate.

The strongest safe conclusion is a restricted exact static energetic minimum on sufficiently short induced intervals for each allowed reference hypothesis. To infer any dynamical statement requires a separately justified nonlinear solution class, appropriate conservation and preservation of the density/scale comparison conditions. None is supplied here. There is no load-bearing gap in the stated static result, but no cap invariance, nonlinear Cauchy existence, nonlinear response or dynamical stability theorem.

Both a_ref=9.3619e-11 and 1.1279e-10 m/s² remain separate positive choices. Constant-vacuum, frozen-H and actual evolving-H interpretations are not equated, and responsive local scale remains an added diagnostic premise with its physical reservoir/vacuum-identity gap. Signed MOND Q sources are used throughout. RAR/M, fitted V, metric/photon/DOF, filtered-MONO, instrument calibration and theory closure are outside the result.

The cheapest next action is to record this static lower-bound gate as checked. Further work should start only from a specific nonlinear or physical evolution target; another parameter sweep or repetition of the failed upper/Taylor route would not establish the missing implication. This reviewer created no follow-up task or numerical run.

## Exact pins

- `campaign_fresh_gravity_astra/stage_24/independent_audit/INDEPENDENT_AUDIT.md`: `09fb154960b3ae7f3e8723da2d0f4547668f15868f354374db6ca9b9d3ea519f`
- `campaign_fresh_gravity_astra/stage_24/nonlinear_domain/ROOT_DERIVATION.md`: `6f5cb19ddbe88399909b711f12538c667658b516de994918e6e34543b5d4847d`
- `campaign_fresh_gravity_astra/stage_24/nonlinear_domain/audit_result.json`: `e761ee5b74abfb540552e5af1035d86ff60b5703856999c6996cef49cbc19780`
- `campaign_fresh_gravity_astra/stage_25/independent_audit/DERIVATION_FROZEN.json`: `f78b0616cb9b973e5901b62b492d0be0be618fec6898ecedff6524ce2f4b6631`
- `campaign_fresh_gravity_astra/stage_25/independent_audit/FROZEN_ENERGY_DERIVATION.md`: `3030def73e0c3aaac2624899143b87f432f1397a993a30560279bec6fe98695a`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/FRAMEWORK_AND_EXECUTION.md`: `ff0d2873065578b0bd8aa50907e0a39495ff8da775bf2b4890768d83775fd750`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/RESULT_CONTRACT.json`: `ba388d0ca8e447a38649a478483e3ff4c2d3293e842eedc8f035499c77a20c29`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-023/fgf023_run_001/DERIVATION.md`: `0b9babab32edd602cf5aea8db63126a52f09c379b858e5c5967d46835bbf1f4a`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-036/fgf036_run_001/DERIVATION.md`: `71727e56c1c7d88bd2d24988af4683339b5fdc4db6f9ca54d9c800752a747f1a`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-037/fgf037_run_001/DERIVATION.md`: `07a7a0d4e22c18c8963d4264dc61b69de035c99acd09624f8a54966d8822ce38`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-037/fgf037_run_001/result.json`: `12b386bc172121cb21379a67fa57f6ccad18d97b051f7c049c3d40e9ec34863e`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-038/fgf038_run_001/DERIVATION.md`: `3891484b03b38d8697155d9a28a3eaa6344a0337f7c8504c4adf510ef23f86d1`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-038/fgf038_run_001/REPORT.md`: `e0e1c47de5859972232d3739bb485742e7b2e8e940faed3b1eabd758a5287fec`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-038/fgf038_run_001/input_sha256.json`: `9d1e8beff626d246306195ae601387eca59079044ac9908661b5b9e83836dd76`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-038/fgf038_run_001/result.json`: `c88bd2ebd307653d98dbabdd3588f98900f312e1db13093265c76c8dcea51bc6`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/reviews/FGF-036_RECONCILIATION.md`: `2ce6b03d38f4d5f7bb63da3a718c87b04e8bd46143c4e3c5da49045e06b259c5`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/reviews/FGF-037_RECONCILIATION.md`: `b361281d7e09edb5bfe7cc67ec3ba3cb9ecb319629ef38a64203248680397994`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/tasks/FGF-038.md`: `5bdba921e97366e7d9698190397a40b5b59c8ad4dd9cd27c2db54e36a7e0765e`
