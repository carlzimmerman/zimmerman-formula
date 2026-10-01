# Independent audit of FGF036

**Primary verdict: proved as written**, within the stated sufficiently short induced-wall Q diagnostic scope. The elementary Hilbert-space steps invoked briefly in the worker proof are spelled out below; no unverified external theorem is promoted. No numerical evidence is claimed.

The normalized claim is: for the same positive-density local crossing constructed in FGF035, with fixed positive C, cs², J, tau and sigma and inherited signed coefficients A,q_s,m, every sufficiently short symmetric restriction satisfying the displayed alpha/beta conditions has a closed positive full coupled form on H1_0 x V_A x H1_0. It defines a positive self-adjoint kinetic-space operator with compact inverse, the derived global transmission domain and conserved-energy linear evolution. The mass and endpoint values are fixed for perturbations on each chosen interval; total background mass varies as the interval is changed.

## Independence, ancestry and evidence type

The auditor independently froze FROZEN_WEIGHTED_DERIVATION.md at 2026-09-30T17:34:51.426792+00:00, SHA256 5c231865662ada4a210384166d62dcb276f97b1949ae94013a195e53bc42a2f6. At freeze, only the task and old action/crossing sources were used. No new author/root proof or formula preview was read. The author candidate was inspected only afterward; the new stage23 root proof was never read. The author readiness message arrived after the independent freeze. No worker proof edits were requested.

This review applied the mathbox proof-audit procedure. It ran no mathematical experiment, ODE solver, symbolic program or spectral calculation. Python file hashing, JSON checks and report writes are administrative only. There is no numerical manifest or claimed execution-bound enforcement. All 10 worker input hashes, 3 worker artifact hashes, 4 independently pinned sources and the frozen proof identity matched. Additional worker ancestor hashes were verified for provenance without treating each as a fresh proof audit. All required result-contract fields were present.

## Dependency graph and obligation matrix

The internal chain is: pinned Q action and FGF035 crossing -> reciprocal-A integrability and signed coefficient bounds -> weighted completion/density/compact embedding -> full mixed-term shortness estimate -> closed coercive form -> kinetic variational inverse -> global distributional operator/transmission -> compact positive inverse and eigenbasis -> linear energy evolution. The initial existence/action facts are pinned prior evidence; all new special-case analytical implications are supplied in the candidate and this review. There are no computation-dependent or external-source leaves.

| Obligation | Verdict | Decisive check |
|---|---|---|
| Actual weighted completion and center value | Passed | Reciprocal-A coordinate identifies the space with one H1_0 interval, including its center |
| Smooth physical-coordinate density | Passed | Flatten smooth transformed functions near the center before pulling back |
| Compact embedding | Passed | Weighted modulus and a finite-grid subsequence argument |
| Full signed form and all cross terms | Passed | Fluid 2d psi and signed -2q_s eta psi' both estimated |
| Positive shortness region | Passed | alpha tends to zero as h^(3/2), beta as at least h² on the same solution |
| Physical kinetic gap units | Passed | Every entry of T_h² has time-squared units |
| Closedness and exact operator domain | Passed | Equivalent complete form norm and whole-interval weak equations |
| Center transmission | Passed | Global H1 enthalpy/flux and H2 eta; no zero-flux condition |
| Nonzero central-flux control | Passed | Explicit full operator-domain triple satisfies fixed mass and outer traces |
| Compact inverse, self-adjointness, linear evolution | Passed | Constructive Hilbert arguments completed below, with summable modal energy tails |
| Ordinary product-H1 coercivity | Refuted by inherited control | The old localized phi sequence is unchanged |
| Nonlinear evolution, nonlinear response, observations | Out of scope | No applicable nonlinear map or empirical model is supplied |

## Weighted space and density audit

For I=(-h,h), ell=2h, let I_A=int_I 1/A. A is positive off zero, bounded, and comparable to sqrt(|x|) near zero, so I_A is finite. The coordinate s=int_-h^x 1/A is strictly increasing and AC; its inverse has derivative A(X(s)), bounded and vanishing only at the center. The change of variables gives int A psi'² dx=int |v_s|² ds for v=psi composed with X. Conversely v in H1_0 yields globally AC psi because int |psi'| dx=int |v_s| ds is finite. These changes of variables can be made off the single central point and passed to the limit by monotone exhaustion. Thus no separate half-interval domain or center trace condition has been introduced.

Weighted Cauchy-Schwarz gives |psi(x)-psi(y)|² <= int_between A psi'² * int_between 1/A and ||psi||_2² <= ell I_A int A psi'². Completeness follows equally by convergence of transformed L2 derivatives and their endpoint integrals. Smooth density is not automatic from renaming the norm, but the author's construction supplies it: smooth v is flattened to its center value on a shrinking s-neighborhood, with bounded derivative error supported on a set of vanishing length. Its pullback is constant near x=0 and smooth elsewhere. It is smooth in x and retains compact support away from the outer endpoints. Standard unweighted H1 approximation used first can be constructed by approximating derivatives, correcting their integral and integrating, with endpoint cutoffs/local smoothing. No weighted density theorem is needed.

Uniform bounded energy gives a uniform sup bound and common modulus from the absolute continuity of int 1/A. A diagonal subsequence on finer finite grids is uniformly Cauchy by that modulus. This proves compact embedding in continuous functions and hence kinetic L2; ordinary fluid/scale H1 components obey the same argument with A=1. Finite energy therefore permits one continuous central value and excludes jumps. It permits singular derivatives; it does not restore ordinary H1 control.

## Full-form constants and signs

The fluid variable is d=-(rho xi)', with integral d=0 from the outer traces. The signed cross coefficient is q_s=sgn(g)(|g|A-|B|), not the positive-side q on both halves. With E_d=int cs²d²/rho, E_p=int A psi'²/C and E_eta=int J eta'²/C, the pointwise Young estimates give exactly

    2|int d psi| <= E_d/2 + alpha E_p,
    (2/C)|int q_s eta psi'| <= E_p/2 + (2Qh ell²/J)E_eta,
    alpha=2C rho_max ell I_A/cs²,
    beta=ell²(2Qh+Mh)/J,
    Qh=sup(q_s²/A), Mh=sup max(-m,0).

The quotient q_s²/A extends to zero and is O(|x|^(3/2)). Therefore Q >= E_d/2+(1/2-alpha)E_p+(1-beta)E_eta. Under alpha<=1/4 and beta<=1/2 this yields the claimed lower bound, while the corresponding upper estimates show equivalence to the complete form norm. Shortening preserves the same solution and physical coefficients: rho extrema stay finite and positive, I_A=O(sqrt(h)), Qh=O(h^(3/2)) and Mh stays bounded. Both gates hold for all sufficiently small h. No unjustified equality or discarded matter/scale mode is used.

The independent frozen proof derived the same sufficient gates with D=Mh+2Qh and P=ell I_A. For kinetic control, xi=-rho^(-1)int d implies N_fluid <= rho_max² ell² E_d/(cs² rho_min²). The other components give N_phi<=tau ell I_A E_p and N_eta<=sigma ell² E_eta/J. Consequently the candidate's

    T_h²=max{2rho_max² ell²/(cs² rho_min²),
             4tau ell I_A, 2sigma ell²/J}

satisfies N<=T_h² Q. All three terms have time-squared units. Q/N is a symbolic inverse-time-squared lower bound in the declared kinetic norm; no physical numerical frequency or interval width was computed. Product norm comparisons use fixed positive dimension-balancing weights.

## Operator domain and center control

Polarizing the full form yields H_f=cs²d/rho+psi and F=A psi'-q_s eta. The weak differential expressions are

    (Lu)_xi=H_f',
    (Lu)_psi=(C d-F')/tau,
    (Lu)_eta=(-J eta''+m eta-q_s psi')/sigma.

The fluid sign follows from int H_f[-(rho v_xi)']=int rho H_f' v_xi. The scalar cross entries are adjoint, with the signed q_s, and no spurious q_s' term belongs in the scale expression.

For every u in the form domain, q_s psi' is L2 since q_s²/A is bounded. F is L2 since A is bounded, and H_f is L2. Hence an H right-hand side forces H_f,F in global H1 and eta in H2 by the distributional expressions; conversely those conditions put all three expressions in H and integration by parts on dense tests recovers the weak form. This proves the exact domain, not only a formal candidate. For weighted tests the scalar pairing is continuous because F/sqrt(A)=sqrt(A)psi'-q_s eta/sqrt(A) is L2; extension from smooth tests is legitimate.

All fields have one continuous center trace. The additional continuous transmissions are H_f, F and J eta'. A jump would yield a delta incompatible with the L2 kinetic right-hand side. There is no additional prescribed center value or flux.

The author's control is stronger than a merely kinematic weighted profile. Choose smooth compactly supported v(s) with nonzero constant derivative near the center. Its pullback psi has F=A psi'=v_s(s(x)) constant near zero and H1 globally. Taking eta=0, c=(int rho psi)/(int rho), d=rho(c-psi)/cs² and xi=-rho^(-1)int_-h^x d makes integral d=0, xi zero at both walls and H_f=c. Thus the full triple lies in D(L), has nonzero F(0), and has an H right-hand side. Imposing a reflecting center would exclude an admissible operator state. The kinetic and form domains, rather than a pointwise substitution A(0)psi'(0)=0, determine the transmission.

## Elementary Hilbert leaves and evolution

The worker states weak subsequence extraction and norm lower semicontinuity briefly. Here are the needed special-case proofs, rather than an external theorem condition.

First, variational inversion does not require weak compactness. For J_f(v)=a(v,v)/2-(f,v)_H, coercivity makes the infimum finite and minimizing sequences bounded. The parallelogram identity gives

    a(v-w,v-w) <= 4[J_f(v)+J_f(w)-2 inf J_f]

for two members of a minimizing sequence. It is Cauchy in the complete a norm; its limit minimizes J_f, and differentiation along every test direction gives a(Tf,v)=(f,v)_H. Strict positivity gives uniqueness and the coercive estimate gives boundedness. Thus T:H->V->H is compact, symmetric, strictly positive and injective. Its range is dense since a vector orthogonal to its range lies in ker T by symmetry.

For the spectral step, H is a separable finite product of positively weighted L2 intervals. Take a countable orthonormal basis obtained from a dense set. From a bounded sequence, diagonal extraction makes each coordinate converge. The limiting coordinates have square sum at most the liminf squared norms, since this holds for every finite partial sum. They define a vector; approximation by finite basis combinations plus the uniform norm bound proves weak convergence to it. This proves both the weak extraction and the needed lower semicontinuity directly. Compactness makes a subsequence of T images converge strongly to the weak limit's T image, as follows by pairing against any test vector and symmetry.

For a maximizing sequence of the positive T Rayleigh quotient on the unit sphere, that strong/weak convergence preserves its positive limiting quotient. The limit has norm at most one; if its norm were smaller than one, rescaling would exceed the supremum. Thus a unit maximizer exists, and tangent variation produces a positive eigenvector. Repetition on invariant orthogonal complements yields the ordered eigenvectors. Nonzero eigenvalues have finite multiplicity and tend to zero, or compactness would fail on their orthonormal vectors. A nonzero remaining complement would have a positive Rayleigh quotient, contradicting both maximality at every step and the eigenvalues tending to zero. Hence the basis is complete. The form basis is also complete because a(v,e_n)=lambda_n(v,e_n)_H, so form orthogonality implies kinetic orthogonality.

Self-adjointness may also be checked without the spectral construction: write L=T inverse. If (v,Lu)_H=(g,u)_H for every u=Tf, then (v,f)_H=(Tg,f)_H, so v=Tg lies in D(L) and Lv=g. This gives equality with the adjoint domain. The resulting eigenvalue domains and positive gap are therefore attached to the actual domain above.

The oscillator series has conserved energy in every finite partial sum. Initial data in V x H have summable energy tails, and modewise conservation bounds those tails uniformly in time. Taking the limit yields C(R;V) displacement, C(R;H) velocity, the weak equation in V dual and conserved total quadratic energy. Coefficientwise uniqueness follows from the scalar oscillator equations. The stronger initial domain claimed by the worker gives the stronger evolution by the corresponding lambda-weighted sums. This is a justified linear energy evolution statement. It proves no nonlinear Cauchy theorem.

## Limits, failed route and next implication

The old phi-only localized sequence still disproves positive coercivity in ordinary product H1. Weighted positivity changes the topology, not that fact. The induced-wall/mass restriction, positivity of kinetic weights and frozen background remain hypotheses; no global astrophysical patch or arbitrary preassigned boundary problem has been proved. A nonlinear map on the weighted space, nonlinear well-posedness, nonlinear stability and the former H2 parameter-response theorem are not supplied.

Both a_ref=9.3619e-11 and 1.1279e-10 m/s² are separate positive-reference choices. Frozen H comparisons, actual time-evolving H, and constant-vacuum hypotheses are not identified. The responsive local scale remains an additional diagnostic assumption, with the previously recorded physical energy reservoir and literal vacuum-identity gap unresolved. This is signed Q source balance throughout. RAR/M transfer, filtered-MONO, physical metric/photon/DOF, instrument-calibrated cluster constraints and theory closure remain unproved.

The strongest safe result is the closed positive weighted linear wall problem on sufficiently short restrictions of this diagnostic crossing, including its continuous transmission and compact inverse. A specific next check is whether the nonlinear Q energy or static source map is differentiable on this weighted form space under localized gradient concentration; state its target space and exact remainder norm before claiming a nonlinear inverse. No follow-up task was dispatched here.

## Exact input and artifact pins

- `campaign_fresh_gravity_astra/stage_22/independent_audit/INDEPENDENT_AUDIT.md`: `32dc34bf2a829e44d790bd60920c753b204f96511af89405dd42bbc9d7881192`
- `campaign_fresh_gravity_astra/stage_22/zero_crossing/ROOT_DERIVATION.md`: `3631b24829052f30e1d2935615ec5f9316b4773f54b9e8b9330e59fd3cc286a6`
- `campaign_fresh_gravity_astra/stage_22/zero_crossing/audit_result.json`: `d32d36846e911641fcd6fc24ba8c2f98a90931281826fea93988810f5c7f399a`
- `campaign_fresh_gravity_astra/stage_23/independent_audit/DERIVATION_FROZEN.json`: `acbb8497b34c63e8e70fc19b85011c6655c619b68a217e7ec68381cfefa6a331`
- `campaign_fresh_gravity_astra/stage_23/independent_audit/FROZEN_WEIGHTED_DERIVATION.md`: `5c231865662ada4a210384166d62dcb276f97b1949ae94013a195e53bc42a2f6`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/FRAMEWORK_AND_EXECUTION.md`: `ff0d2873065578b0bd8aa50907e0a39495ff8da775bf2b4890768d83775fd750`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/RESULT_CONTRACT.json`: `ba388d0ca8e447a38649a478483e3ff4c2d3293e842eedc8f035499c77a20c29`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-023/fgf023_run_001/DERIVATION.md`: `0b9babab32edd602cf5aea8db63126a52f09c379b858e5c5967d46835bbf1f4a`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-035/fgf035_run_001/DERIVATION.md`: `5aa9e64b81a9dcaac14926f43c680a82d44d57be838423ccc4b0ebeee1cb1d3b`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-035/fgf035_run_001/result.json`: `a92f785e1642c43d1b9df4030add980ca621b484e20b5d6980a33bb620c4a747`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-036/fgf036_run_001/DERIVATION.md`: `71727e56c1c7d88bd2d24988af4683339b5fdc4db6f9ca54d9c800752a747f1a`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-036/fgf036_run_001/REPORT.md`: `885138f7a87fcc8e90d0a204189504b0b1167157c7b76a10dfaa79bea17a495c`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-036/fgf036_run_001/input_sha256.json`: `ae9326e94db0d82472dc12a6b03c5e11f84573ffe21464af247ceb7231e55fac`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-036/fgf036_run_001/result.json`: `d238f3db45e4aacbce15487c89c1c66f7131915cba7a1c6e5043179b0e30c515`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/reviews/FGF-034_RECONCILIATION.md`: `9df1b83ca18f15b0fcb13c6595378a124fd6b2d67fe3be3687d5b59e38e00ff9`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/reviews/FGF-035_RECONCILIATION.md`: `d732e678ee2a4b27022aab2bd4953816cec9e3d6cfab9ca4411d4925b62d8e06`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/tasks/FGF-036.md`: `94158f29d08e8d277a283a42e6dc114625670642ebe1767b142a9511f6b00a9d`
