# Gravity and empirical audit, 2026-11-03

Primary verdict: **correct only after stated restrictions** for the empirical scorecards; the claim that KT14's source-only filtered map is a universally coupled reduced static energy gradient is **refuted** on a positive-density periodic case. No reviewed lane derives kappa=1/2 or supplies a common verified theory.

Revision: base `4cba03defe795a2f8e40bc181d8bd7c1a5362752`, audited checkpoint `c8b2586bb1921cff3bcb75feae827233ce62db8b`. The repository was dirty and HEAD advanced during the audit; all 53 selected READMEs and all 15 recorded load-bearing input files match the checkpoint. See `coverage.json` and `source_hashes.json` for absolute paths and full SHA-256 values. No project files, jobs, or git state were changed by this subagent. All executed numerical work is under this directory.

## Coverage and evidence depth

README-level review covered 53 changed lanes: KT1–23 and KT25–27 (no changed KT24 README), KU1–2, LAM1–3, RQ2–3, CRG1, NP1–2, RF1–4, BF1–3, BK1–2, SL1–2, SY1, LW1, LM1, HM1, SP3 and GT1. This is not a claim to have audited all roughly 220 changed rebuild READMEs. Adjacent gas, spin, native-collapse and material lanes were read only where named dependencies required it.

Code-level audits: KT2/3 auxiliary action; KT14 fixed filter; KT26 local-width MW screen; KT27 variable-width Cassini/dwarf/SPARC operations; KT23 ladder-distance estimator; KU2 model choice and label; NP2 derivative constraints/checker; RQ3 marginal and joint statistics. Raw stored results inspected include KT23, KT25, KT27, KU2 and RQ3 law. Large empirical pipelines were not rerun. CRG1's clean-room reproduction and RF1–4 astrophysical inputs remain read-only evidence, not independently remeasured inputs.

## Findings

1. **KT14/17/25 source-only filtering lacks the variational reciprocity needed for ordinary universal matter coupling.** `rebuild_2026_10_22/KT14_filtered_phantom_mw/kt14.py:63–68` implements

   `F[rho] = N rho + (Q-N)[S rho]`.

   With fixed self-adjoint Gaussian S and symmetric QUMOND phantom Hessian B, `DF=N+B S` whereas `(DF)*=N+S B`. There is no generic commutation. An energy `U_N[rho]+U_ph[S rho]` instead gives `N rho+S*(Q-N)[S rho]`. This is an obstruction to the stated map and coupling, not all nonlocal or dynamical models.

   Independent finite evidence: actual simple nu, planar 2pi-periodic domain, `4piG=a0=1`, external Newtonian gradient 3, `h=sin x+0.2sin2x`, positive density `rho=2+h'`, Gaussian sigma .7. Source-only net internal force is `0.00034398520126445`; ordinary QUMOND and adjoint-completed controls are below `5e-17`. N=256,1024,4096,16384 agree to about `5e-18`. This is a periodic external-field example, not an isolated 3D galaxy calculation. `run/manifest.json`: completed and validated.

   The older action is different: `qwen_claude_field_theory/closure_2026/FRIED_CHICKEN_SPEC.md:25–26` explicitly has outer `S*` and inner `S`, with nu_mono rather than simple nu. L340 inherits that parent. CFG653 uses a two-sided **high-pass** operator. Neither transfers its action or observational results to the KT implementation. AS471 is a proposed older adjoint audit, not completed evidence for KT14.

2. **KT27 evaluates different variable-width operators in its different observational tests.** `kt27.py:20–26` computes the Cassini radial field as `GM F(r/xi(r))/r^2`, where F is the enclosed fraction of a fixed-width Gaussian. `kt27.py:45–62` and `:103–113` instead compute a row-wise smoothed density and then its enclosed integral for dwarfs/SPARC.

   For a point source, the latter density is `rho_s(r)=M(2pi)^(-3/2)xi(r)^(-3)exp[-r^2/(2xi(r)^2)]`. Its enclosed mass is the integral of this density. Differentiating the Cassini proxy gives

   `d[M F(r/xi(r))]/dr = 4pi r^2 rho_s(r) [1-r xi'(r)/xi(r)]`.

   Thus they agree only for constant xi (or exceptional points), precisely the case the reproduction control checks. This is more than the already disclosed nonconservation: KT27's README:21–23 reports SPARC mass ratios 0.36–1.13, median .81, an uniterated field, and a separate one-width MW screen. KT26/kt26.py:68 additionally sets that MW width from observed V=229.1 km/s and observed slope -1.7 km/s/kpc, rather than the predicted field of each cell. The combined label cannot be a falsification or pass of one solved local field equation. Its individual screens remain useful diagnostics.

3. **RQ3's claimed correlation-safe joint p-values use an uncalibrated marginal tail.** `RQ3_acceptance_v2/acceptance.py:179–180` turns A30 chi-square into `Z=(chi2-56)/sqrt(112)`; `:314–319` then applies a Gaussian two-sided tail. A chi-square is not normally distributed in this extreme tail. Independent exact even-dof gamma-series arithmetic on its pinned law JSON gives:

   | Footing | chi2/56 | Gaussian p used | Exact chi-square survival |
   |---|---:|---:|---:|
   | canonical | 154.1485777 | 1.79009e-20 | 4.16424e-11 |
   | alt | 124.9956936 | 7.05514e-11 | 3.51663e-7 |

   The canonical exaggeration is a factor 2.326e9. Bonferroni at `:320–334` does not repair invalid marginal p-values. This arithmetic does not authenticate the covariance, fitted degrees of freedom or absent inventory systematics. Overall candidate rejection may survive; the quoted no-solar lens significance does not. `p_run/manifest.json`: completed and validated.

4. **KT3's positive-delta attractor has a sign problem under the conventional kinetic completion.** KT2/kt2.py:24–38 has `U'=2(1-chi)^2/chi`. KT3/kt3.py:44–51 only checks the assumed reduced equation `3H delta_dot=-A delta^2`, with `delta=1-chi`; it does not derive it from a kinetic action. With positive kinetic coefficient K and the KT2 potential sign, at g=0 the conventional equation is `K(delta_ddot+3H delta_dot)=+V_chi`, positive on chi<1. The displayed positive `delta=3H/(At)` then is not the claimed attractor. At fixed nonzero g the stationary branch also has

   `d2/dchi2 [(1-chi^2)g^2+(s/b)^2 U] = -4(s/b)^2(1-chi)/chi^2 < 0`.

   This is a fixed-g, conventional positive-kinetic completion audit. Constrained gravitational backreaction or other kinetic couplings can matter; it is **not** a universal tachyon theorem. KT2's algebraic stationary elimination and the unfixed b/zero-mode conclusion survive.

5. **KU2's UNIVERSAL label is stronger than its test.** `KU2_kappa_universality_model_choice/ku2.py:58–61` issues UNIVERSAL whenever the total error is below .06 and `|D|<=2sigma`. That establishes no detected difference under the chosen estimator, not universal kappa or an equivalence bound. At canonical D=.02333, sigma=.02263, the approximate 95% interval is [-.021,.068] in residual log acceleration; its implied dln a0=.0745 with sigma about .072 admits differences of order 20% at the upper end. Code `:22–26,:55–57` chooses lowest reduced chi-square and treats best-vs-second difference as model uncertainty; README:25–26 itself acknowledges weak model preference and uncalibrated absolute offsets. Stored medians are +1.40 and +1.18 in ln, not small agreement with the law. Safe wording: **no slow/fast residual difference detected after matching and this model-selection rule**. Common mass calibration does not necessarily cancel exactly because nu is nonlinear and the classes need not share acceleration distributions.

## Strongest surviving results

- **Kappa remains an adopted/fitted amplitude.** KT2's stationary equation gives kappa=1/(nb); KT3's constant shift leaves a free vacuum normalization. KT23's 19 ladder-distance galaxies return a0=1.12459e-10 with sigma_ln=.23144 under simple nu, hence kappa=.6007±.1390 canonical or .4971±.1150 alt. This is compatible with one-half, too broad to select it, and changes with the interpolation kernel. Code-level audit, stored-result check; no new full fit.
- **The filter produces a real static geometric effect in the implemented map:** it can reduce vertical force relative to radial force. But KT25's canonical nine MW cells sit at prior corners, none at thick share .12, all fail the stricter Kz scale length, and its SPARC check is a spherical surrogate whose monotone-envelope criterion failed. These are conditional screens, not a common-theory success. Raw KT25 JSON retains `fail=2`.
- **NP1/NP2 show that discs plus relaxed-cluster holdouts do not establish a leaf-space impossibility.** Flexible L3 rules fit the designated first five gates, including unseen X-COP clusters. NP2's analytic derivative directions and kernel derivative formulas are coherent in the inspected code, but the checker is finite Sobol/observed-point coverage (`np2_core.py:86–95,:186–203`), not global admissibility. L3 failures at a chosen fit/smoothness do not exclude every admissible rule; L5 already fails its independent finite checker.
- **The empirical infrastructure exposes sensitivity instead of one coherent win.** CRG1 documents reproduction of definitions, not their validity. RF1's MW feasible cells need simultaneous extreme baryon choices; RF2's inclination conclusion is model/prior conditional and is not exclusion; RF3's HSE-free X-COP validation is unavailable and its key threshold is gas-scale sensitive; RF4's native two-halo template fails common-amplitude consistency. BF/BK large formula counts with scrambled controls supply no new physical derivation.

## Nonduplicative routes and first decisive tests

1. **Repair the precise operator before more fitting.** Use the already-known variational adjoint principle on the *KT simple-nu low-pass operator*, not another renamed older action. First solve the same constant-width, outer-adjoint-completed equation for one canonical KT25 near-pass MW cell and its Solar System counterpart; require identical matter coupling, normalization, and boundary conventions. Reciprocity and momentum tests precede this. If those near-pass observables fail, stop this completion at that premise before searching widths.
2. **Define adaptive filtering by a variational state, then test composition.** A field-dependent `S[rho]rho` requires the full Jacobian adjoint, including derivative-of-width terms. First decisive test: split one smooth source into arbitrarily labelled pieces and embed a compact satellite in a smooth host; the field must be independent of labels and converge under splitting, with one equation across both scales. KT25's system-mass prescription has no such definition; KT27 does not implement one. This route is open only after a specific action and boundary problem is declared.
3. **A serious empirical falsification of any surviving completed filter:** freeze its canonical matter coupling and scale rule, then jointly predict MW radial force, vertical profile including h=2.72±.15 kpc, and a vector host+Fornax calculation with independent baryons. No separate per-object width or footing swap. Fornax and Kz radial scale are already failures or liabilities of the screens, so these tests can kill the proposal. Independently repair RQ3 tail calibration and nuisance covariance before ranking candidates; that is infrastructure, not new physics.

## Reproducibility and independent proof review

Exact commands are arrays in both v2 manifests. Executed commands were the computation-audit bounded runner on `fixed_filter_force.py` and `chisq_tail_check.py`, then its validator with this directory as root. Both status values are completed. Only the latter reads an empirical-result file, `law_snapshot.json`; hashes before/after are recorded. The former is a newly designed analytic-input experiment, not an undocumented reproduction command. No full project reproduction was attempted.

I independently checked the parent's `reviews/repo_audit_2026_11_03/FILTER_RECIPROCITY.md`: two-mode exact sign and normalization pass. The pairing proof, density positivity, zero-mass variation and fixed-total-mass-width extension are sound. One notation correction was requested: include the fixed external field in the definition of u. External papers cited there were not independently authenticated by this subagent.
