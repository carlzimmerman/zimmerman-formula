# FSP-003 fresh chiral/metric audit

**Normalized claim.** The displayed charged-pion determinant, individual proton local operator and common nucleon nonanalytic term are valid fixed-mass chiral contributions; meson and isoscalar baryon LECs do not cancel by symmetry; a round-S4 current-current insertion gives a free-energy response which requires metric variation to obtain stress.

**Primary verdict: correct only after a stated restriction.** The chiral formulas require positive fixed renormalized quark masses in a specified matching scheme, the stated finite chiral subtraction, and the displayed finite chiral/electromagnetic orders. The metric relation requires an invariant round-S4 state with the stated stress/continuation conventions. Those restrictions are already present in the current electromagnetic report and coordinator note, so no correction to their core formulas is required. This verdict does not establish a physical four-dimensional A_H or its alpha dependence.

The stronger physical objective remains incomplete: neither this audit nor the existing symbolic run calculates the small-H QCD stress observable or the matched individual-proton response needed for R(alpha). Agreement on the chiral formulas does not fill that gap.

## Independent derivation and decisive checks

The pre-comparison derivation is [RAW_DERIVATION.md](RAW_DERIVATION.md), saved before reading the target report, implementation, self-review or coordinator note. Its SHA-256 is `a8fcfdcb0ea6f74dbf09b3562b276b68d4cff1a870a076b3c5f6a44d9e4ae9a9`. No subsequent change was made to that artifact. The parent supplied candidate formulas, and SOURCES.json was read for source locations; this is a fresh reconstruction with that disclosed limitation, not a blind external referee review.

1. Two charged real pion modes give one complex determinant. The aligned pion mass has x''(0)=-rM^2 and chi_0=rF^2M^2. With Delta_EM=2e^2F^2Z, differentiating the GL-subtracted determinant yields

       delta chi_loop/chi_0
         = -e^2 Z/(8pi^2) [1+log(M^2/mu_chi^2)].

   The coefficient of the logarithm and its sign agree with GV (36). The finite 1 is subtraction dependent; an MS-bar scalar determinant changes it by an analytic term absorbed into the meson LECs. The current report explicitly retains K_chi^r and the subtraction convention, so its isolated loop is not misrepresented as a physical numerical slope.

2. Evaluating MM (2.28)-(2.29) at u=1 gives O1=O3=e^2/2 and O2=e^2 tau_3/2. The pole sign therefore gives

       delta m_p,local=-e^2 F^2(f1+f3+f2)/2,
       delta m_n,local=-e^2 F^2(f1+f3-f2)/2.

   The individual mass needs the isoscalar f1+f3, while p-n sees only -e^2F^2 f2. This distinction is correct in the report and implementation.

3. The pion species weights reconstruct the common nucleon term

       delta m_N,loop=-g_A^2[(M^2+Delta_EM)^(3/2)-M^3]/(16pi F^2)
                     =-3e^2g_A^2 ZM/(16pi)+higher terms.

   Its sign is negative for positive Z and it cancels in p-n. A dimensionally explicit estimate of the Taylor remainder is O(g_A^2 Delta_EM^2/(F^2 M)), equivalently O(e^4 g_A^2 F^2 Z^2/M), at fixed positive M. RAW_DERIVATION.md used shorter O(Delta_EM^2/M) and O(e^4/M) notation with the fixed prefactors suppressed; this sentence makes those factors explicit without altering the frozen derivation. The report correctly warns that the linear e^2 limit is nonuniform as M tends to zero.

4. The actual PDF pixels of MM printed p.14 display the inconsistent equation (3.8): no F_pi^2 in its two electromagnetic terms, plus an isoscalar sign opposite the invariant Lagrangian. The factor omission violates the paper's own dimensions [f_i]=mass^-1. This is a source inconsistency, not an extraction artifact. The project correctly uses the invariant operators. The retained mm-page7.png and mm-page14.png show the definitions and inconsistent equation; gv-page11.png shows the susceptibility formula. No erratum search was performed.

5. A symmetry-allowed variation of f1+f3 changes the individual proton response while leaving the meson susceptibility and the p-n splitting unchanged. Thus chiral/gauge/isospin symmetry does not supply a cancellation with k5+k6 or k7. This does not forbid dynamical correlations after matching actual QCD, nor prove a nonzero physical A_H response. The current report maintains both qualifications.

6. With W=V_4f and V_4 proportional to H^-4, a uniform metric rescaling gives dW/dlog a=V_4(4f-Hf_H). In an invariant state this is 4V_4 rho, yielding rho=f-Hf_H/4. A linear term in f therefore has 3/4 of its coefficient in rho. Gaussian photon integration with Euclidean coupling ieA.J gives S_eff=S_QCD+e^2I, so <I>/V is partial f/partial e^2. The stress derivative is [1-(H/4)partial_H](<I>/V). Both target artifacts now make this distinction correctly.

7. The coordinator's coefficient extractor is a valid formal reduction under its declared asymptotic conditions. For D=H partial_H and P(D)=D(D-2)(D-4), P(D)H^n=n(n-2)(n-4)H^n. It annihilates b0+b2H^2+b4H^4, while P(D)(A_f H)=3A_f H. The stress operator 1-D/4 commutes with P(D), and multiplies the n=1 mode by 3/4. Consequently the two coefficient-extractor limits agree with A_rho=3A_f/4. H^4 log H and higher regular powers/logarithms vanish after applying P and dividing by H. This argument requires a controlled asymptotic expansion under the needed derivatives: a bare remainder o(H) alone is insufficient, since repeated derivatives of an oscillatory remainder need not remain o(H). For the combined insertion extractor the necessary H derivatives extend through order four. An H log H term prevents a finite constant coefficient; interchange with e^2 or theta derivatives requires its own control. The note explicitly treats these as assumptions and does not claim to have measured the limits.

8. After saving the raw derivation, `coordinator/SUSCEPTIBILITY_TO_VACUUM.md` was also read. Its information distinction is correct: if the geometry difference is H A_f(theta,alpha)+o(H) with controlled theta derivatives, its susceptibility coefficient is A_f''(0,alpha), not A_f(0,alpha). For an explicit CP-even periodic family, take A_f(theta,alpha)=C(alpha)[1-cos theta]+B(alpha). The entire theta susceptibility is independent of B, while the round-S4 stress coefficient at theta=0 is 3B(alpha)/4. Flat subtraction does not remove H B(alpha), and P(D) retains it. This demonstrates missing information in the susceptibility inference; it does not grant arbitrary freedom to a fixed microscopic theory or classify H B as an ordinary analytic local gravitational counterterm. The note's compact-Maxwell example was not independently audited in this lane.

## Obligation matrix and dependency coverage

| Obligation | Status | Evidence / limit |
| --- | --- | --- |
| Fixed-mass susceptibility loop and charged multiplicity | passed | Hand determinant derivation and exact GV v2 Appendix A.1 |
| Full leading meson analytic combination | passed | Exact GV (36), pixels inspected; no numerical LEC matching |
| Proton local operator, sign and dimension | passed | Direct invariant evaluation; actual MM pages 7 and 14 inspected |
| Common nonanalytic e^2 M term | passed | Species-weight reconstruction and MM (3.4) |
| Symmetry forces independent meson/baryon cancellation | failed | Allowed independent isoscalar variation; current report rejects this implication |
| Fixed-MSbar versus fixed-invariant mass path | passed as a conditional chain-rule distinction | Report gives conversion and regular-branch conditions; actual matching functions are not calculated |
| Round-S4 f-to-rho conversion | passed | Independent uniform scale variation |
| Current insertion sign and observable | passed with stated Euclidean convention | Independent Gaussian integration; no evaluation of the QCD expectation value |
| Coordinator local-counterterm projection | passed as a formal conditional reduction | Hand check P(n)=n(n-2)(n-4), P(1)=3; controlled differentiable small-H expansion and limit interchange remain assumptions |
| Susceptibility determines A_f(0) | failed | A_f'' is unchanged by a CP-even periodic theta-independent B(alpha); current coordinator note rejects this implication |
| Existing symbolic implementation | audited, not executed | Read complete v3 code, contract, inputs, result and manifest; current hashes equal manifest hashes |
| Full four-dimensional geometric stress coefficient | not addressed | No small-H matched QCD measurement/calculation supplied |
| Numerical physical alpha root | not addressed | No full R(alpha), matched constants or root computation supplied |

The dependency graph is: primary chiral potential/determinant and baryon invariants -> finite infrared benchmark formulas; independent metric variation and Gaussian integration -> operational stress insertion; a separately evaluated, common-scheme four-dimensional generating functional -> A_H(alpha); matched proton response plus mass/scale Jacobian -> R(alpha). The last physical branch is missing. The flat susceptibility branch cannot replace it.

## Existing-code and evidence assessment

Reviewed `chiral_response_v3.py` in full, `SOURCE_INPUTS.json`, `contract_v3.json`, `run_003/manifest.json`, and `run_003/result.json`. This review did not rerun the suite, install dependencies, or execute any new symbolic or numerical mathematical experiment. The recorded completed run has 29 exact symbolic checks, Python 3.9.6 and SymPy 1.14.0, no numerical alpha, and the source/input hashes remain current. The script's matrix conventions, charged multiplicity, determinant subtraction, fixed-positive-mass expansion and local pole sign agree with the independent derivation.

The evidence is narrower than the number 29 might suggest. The nucleon loop formula is supplied as an input and then expanded, not rederived by a loop-integral implementation. The check called “shared pion cloud cancels” subtracts the same expression from itself; it does not independently compute proton and neutron clouds. The full analytic meson LEC formula is a recorded external input, not derived from all meson operators in this script. These are limitations of computational independence, not counterexamples: the missing physical checks are supplied here by the source/species and invariant-operator arguments. No suite success is evidence of a four-dimensional de Sitter mechanism.

The code uses a diagonal phase matrix of determinant exp(i theta) as a convenient mass-phase representative. The report explains that the common theta phase is absorbed into that representative; it is not silently asserted to be a generic SU(2) Goldstone field. The checked vacuum curvature is local near theta=0 with positive masses. No all-theta phase/stability claim is audited.

The report's constrained derivative follows from dlog m_p=0: dlog Lambda=-(p_alpha/a_Lambda)dlog alpha. Substitution into dlog A_H yields a_alpha-(b_Lambda/a_Lambda)p_alpha. Expressing the same statement through invariant masses requires a common QCD+QED mass conversion; the report states that conversion is required and does not silently equate the paths. No explicit conversion or physical sigma-term dataset was evaluated in this audit.

## Exact remaining gap and strongest safe statement

The first missing physical implication is an evaluated common-scheme QCD+QED round-S4 (or other fully specified state/geometry) stress coefficient and its electromagnetic derivative. The current-current formula specifies an observable, subject to regulator, state and limiting assumptions; it does not calculate its expectation value. Independent meson and individual-proton matching must also be supplied on the chosen mass-retuning path. The cheapest decisive physical next step is an actual controlled geometry-subtracted stress/insertion calculation with continuum and small-H limits, not more algebraic checks of the same infrared formulas.

The safe positive result is that the electromagnetic report has correct, source-normalized leading chiral benchmarks and correctly identifies the additional independent matching information and stress conversion. It does not yet predict the requested physical R(alpha).

## Provenance and proofreading

Current repository HEAD during review: `3c01aa2861bf576f4c2d942251eb9d2f89cae108`; files are uncommitted and identified by their hashes in INPUT_HASHES.json. Reviewed target report SHA-256: `5d85c84de99f02f42f9356218012209d59e4c3deee67afd78e30e1adcf1245e7`; coordinator note: `b8c4e16d2b09e83f1af66a2780e8685e85ae876f2b6a15ce7c677a47a46fad25`.

The additional susceptibility-to-vacuum note has SHA-256 `bcf56f4c7de989ace21e4c8f1c8b9e923c47500bc132ec4e358e96d419a66684`. It was opened only after the pre-comparison raw derivation had been saved.

Skills applied: proof-audit, literature-check, read-only PDF inspection, computation-audit of existing evidence, and proofread-math self-review of this review and the frozen raw derivation. Routine proofreading edits: none to existing project artifacts. Mathematical-token changes to existing artifacts: none. The dimensionally explicit remainder clarification is recorded above; no leading coefficient was changed. Validation performed: primary version authentication, exact PDF/text hashes, selected PDF pixels, complete implementation/contract read, and hash comparison. Coverage excludes a novelty search, third-source RM123 text authentication in this fresh lane, full source errata history, complete higher-order EFT, and all four-dimensional QCD evaluation.
