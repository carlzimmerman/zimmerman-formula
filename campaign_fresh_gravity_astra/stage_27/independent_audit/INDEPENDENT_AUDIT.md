# Independent audit of FGF040

**Primary verdict: proved as written**, within the stated energy-class and smooth-equation scope. The force-product counterexample is valid, the combined smooth momentum signs are correct, and the conditional integrability and boundary qualifications are sufficient. A meaningful candidate weak formulation is not promoted to an existence, equivalence or conservation theorem for rough solutions.

## Normalized claim and independence

Finite fixed mass, isothermal entropy and Q field action do not force n phi_x to be locally integrable. Nevertheless, for smooth solutions the actual matter and both field momenta combine into an exact local conservation law. Its momentum density and stress are integrable at an energy-finite time slice and in spacetime under the additional component/time bounds stated in the proof. Defining a rough weak system with these combined fluxes is an explicit formulation choice; equivalence to separate forced matter momentum, weak-limit closure, initial/wall traces and solution existence remain separate questions.

The auditor froze FROZEN_DERIVATION.md at 2026-09-30T21:36:36.370654+00:00, SHA256 04372794ede2e8bcf04761549957dfe0a590b641222cb9abb68f659b4445bf2e, before any new author/root proof or formula preview. It independently derived a counterexample with density exponent 3/4 and gradient exponent 1/3, the full signed momentum identity and explicit spacetime/trace conditions. The author's readiness message arrived afterward. Its different counterexample, with exponents 2/3 and 2/5, was then checked. The extra raw-energy-to-component estimate was first inspected and audited after reading the author; it is not claimed as part of the pre-read freeze. The new stage27 root proof was never read. No correction was requested or source/report replaced.

This audit applied the mathbox proof-audit workflow. It executed no mathematical computation, numerical trajectory, symbolic program or parameter scan. Python was used only for file hashing, JSON checks and writing this review. All 11 worker input hashes, 3 worker artifact hashes, 4 independently frozen source pins, frozen-proof identity and required result fields matched. Additional ancestor hash matching is provenance verification, not a fresh mathematical audit of every older artifact. No numerical manifest or enforced computation limits are claimed.

## Dependency graph and obligation matrix

The chain is: pinned diagnostic action and energy class -> explicit fixed-mass force counterexample; separately, smooth full equations -> cancellation of matter and scale exchanges -> full momentum/stress -> component and spacetime integrability -> candidate interior weak identities. Boundary and weak-equivalence conclusions are explicitly excluded without further premises. All new mathematical leaves are elementary algebra and inequalities; no imported external theorem is needed.

| Obligation | Status | Decisive evidence |
|---|---|---|
| Exact mass and entropy | Passed | Normalized q integrates to one; x^(-2/3) log(x) is integrable |
| Potential walls and finite action | Passed | Gradient has zero integral and exact squared norm 70 a_p² L/9 |
| Separate force failure | Passed | Positive lower bound proportional to x^(-16/15) |
| Matter/potential/scale signs | Passed | Both kinetic stresses retained; signed source and T chi_x exchanges cancel |
| Independent sign control | Passed | Static background stress derivative vanishes by the actual equations |
| Instantaneous combined fluxes | Passed | Mass/kinetic and field L2 Cauchy estimates |
| Spacetime bounds | Passed with stated assumptions | Compatible weak derivatives plus locally time-integrated component bounds |
| Raw total-energy component estimate | Passed conditionally | Negative interaction absorbed using fixed mass, left wall value and scale bound |
| Candidate weak identities | Well-defined under stated bounds | No undefined force multiplication appears |
| Global conservation from fixed walls | Not earned | Wall traction and normal/time traces are additional obligations |
| Rough equivalence, closure or existence | Not addressed | Finite fluxes alone do not prove these implications |

## Counterexample: actual mass, potential and all energy components

The worker chooses 0<L<d/4 and q=(x/L)^(-2/3)/(3L) on (0,L), zero elsewhere. Its integral is (1/3)int_0^1 y^(-2/3)dy=1. Hence n=(rho+M q)/2 has exactly mass M and is positive almost everywhere. Finite jumps do not affect entropy integrability; near zero it has the integrable power-log bound x^(-2/3)(1+abs(log x)). Since the background rho is bounded positive, entropy relative to rho is finite as well.

For the gradient p=a_p[(x/L)^(-2/5)1_(0,L)-(5/3)1_(2L,3L)], the positive integral is 5a_p L/3 and the negative integral is its opposite. Thus psi=int_left^x p has zero outer traces and compact support inside the interval. Its derivative is L2, with

    int p²=a_p² L[5+25/9]=70 a_p² L/9,
    ||psi||infinity<=5a_p L/3.

It is globally AC and H1_0 despite its unbounded derivative. Its units are correct: a_p=a_ref is acceleration and integration in x produces potential. eta=0 and all instantaneous velocities zero preserve the scale cap and field walls and make every kinetic term zero.

On (0,L), the actual central crossing has g0>0. Therefore n phi_x has the exact positive lower bound M a_p (x/L)^(-16/15)/(6L). The exponent exceeds one, so the product is not locally integrable at the interior point zero. The divergent contribution has one sign; cancellation from the other side cannot turn it into an ordinary integrable force, and integration against a nonnegative smooth test equal to one there is divergent. A finite-part or other renormalized extension would be an additional definition, not supplied by this energy class.

All static energy components are nonetheless finite: density entropy is finite; n phi is integrable because phi is bounded and n has finite mass; W(abs(phi_x),a)<=phi_x²/2; the scale-gradient/potential terms remain their finite background values. There is no density-gradient penalty in the inherited action. These data are comparison states, not claimed equilibria or constructed nonlinear solutions. B_x=C n is not a static constraint that can be imposed on arbitrary initial configurations of this dynamic potential action.

The independent frozen counterexample uses a separate normalized shape 1+(L0/abs(x))^(3/4) on a central subinterval, with exact normalization ell+8L0, and an odd cutoff potential proportional to sgn(x)abs(x)^(2/3). Its derivative is positive on both sides and in L2, while the force is comparable to positive abs(x)^(-13/12). It reaches the same obstruction through different fixed exponents and a different endpoint construction. Neither derivation is a numerical scan or a statement of ill-posedness on all stronger classes.

## Full smooth momentum identity and signs

Let g=phi_x, w=chi_x, B=sgn(g)b(abs(g),a), T=-W_chi and j=nv. The smooth equations retain

    j_t+(j²/n+cs²n)_x=-n g,
    tau phi_tt-B_x=-C n,
    sigma chi_tt-J chi_xx+U'=T.

The constitutive chain rule is W_x=B g_x-T w. Consequently

    (-tau phi_t g/C)_t
      +[(tau phi_t²/2+gB-W)/C]_x=n g+T w/C,
    (-sigma chi_t w/C)_t
      +[(sigma chi_t²/2+Jw²/2-U)/C]_x=-T w/C.

These calculations fix every disputed sign: g B_x=(gB-W)_x-T w, the scale equation supplies the opposite T w exchange, and the positive source B_x-tau phi_tt=Cn cancels the matter force when the momenta are added. Thus

    P=j-(tau phi_t phi_x+sigma chi_t chi_x)/C,
    Pi=j²/n+cs²n
        +[tau phi_t²/2+sigma chi_t²/2+B phi_x-W
                                      +J chi_x²/2-U]/C

satisfy P_t+Pi_x=0 for smooth solutions. There is no missing n phi stress term: its force has been accounted for through the actual field source equation. Both field kinetic stresses and the scale gradient stress have positive signs; U enters with a negative sign.

An independent static sign check differentiates cs²rho+(gB-W+Jw²/2-U)/C. Hydrostatic balance cancels the rho g terms, leaving (T+Jw'-U')w/C=0. This confirms the pressure, field and scale signs together. The identity is a 1D preferred-time momentum balance, not a covariant stress tensor.

## Spatial and spacetime product domains

With the vacuum convention j=0 at n=0 and j²/n=0 there, finite matter kinetic energy gives int abs(j)<=sqrt(M int j²/n). The field momenta are L2-by-L2 products. Every stress term is L1: j²/n and n, the two time-derivative squares, spatial gradient squares, and U. For Q, abs(B)<=abs(g) and 0<=W<=g²/2 suffice to bound the field stress; in fact 0<=gB-W<=g²/2 follows directly by integrating s A(s,a)<=s. The worker's weaker individual-term bounds are already adequate.

The other weak equations have meaningful sources: B is L2, and q=T_s=a b/(2b+a)<=a/2 gives 0<=T<=a abs(g)/2. A uniform scale cap bounds a, making T locally spacetime L2 when g is, and bounds U'. These estimates do not license multiplication of a distributional field equation by rough g or chi_x.

Time-slice finiteness alone is insufficient. The author correctly requires compatible weak field derivatives and locally time-integrated nonnegative component bounds for j²/n, both field time derivatives, both spatial gradients and U, together with fixed finite mass, measurability and a uniform scale/source bound. Cauchy-Schwarz in spacetime then makes P and Pi L1 on each compact time slab. The density source is spacetime L1 by mass and measurability. The velocity variables must actually be the distributional time derivatives of the fields; assigning unrelated finite kinetic variables would not suffice.

The additional raw-energy estimate was independently checked after reading the author. Under uniform a<=a_max and fixed left wall potential phi_L, the one-dimensional endpoint bound gives int n phi>=-M abs(phi_L)-M sqrt(ell)||g||_2. Q supplies W>=g²/4-a_max²/4. The exact Young estimate

    M sqrt(ell)||g||_2
       <=||g||_2²/(8C)+2C M² ell

gives

    E>=K+||g||_2²/(8C)+J||chi_x||_2²/(2C)
                         +int U/C+int e(n)-C0,
    C0=M abs(phi_L)+a_max²ell/(4C)+2C M²ell.

Every factor and physical unit checks. Since e(n)>=-cs²rho_ref pointwise, an assumed uniform upper bound on E controls all nonnegative components and also int e(n)_+. This legitimately supplies the time-integrated component conditions under the additional mass/wall/scale hypotheses. It is not a proof that a weak trajectory has that energy bound, conserves energy, or keeps the cap. The author explicitly retains those as separate assumptions.

## Weak formulation versus existence and equivalence

The proposed compact-interior test identities for continuity, the two field equations and combined momentum all have the correct signs. In particular the source identities use -tau phi_t zeta_t+B zeta_x+C n zeta and -sigma chi_t zeta_t+J chi_x zeta_x+(U'-T)zeta. The combined identity uses P zeta_t+Pi zeta_x. All these integrals are defined under the specified spacetime bounds.

The smooth cancellation occurs before any passage to low regularity. For smooth solutions, subtracting the field momentum identity recovers the separate matter momentum law. At the rough energy regularity this subtraction has not been justified, and n phi_x may not even define a distribution by ordinary integration. Therefore adopting the combined system is a candidate weak-solution definition, not a proved equivalent repair of the original rough Euler force equation. Quadratic fluxes need compactness or other closure information to pass to weak limits; no defect-free limit is earned here.

The counterexample's finite combined fluxes do not make that time-slice state a solution. No solution existence, uniqueness, stability, energy inequality/equality, convergence theorem or global ill-posedness conclusion is established.

## Boundary and initial data

For smooth states the global balance is d/dt int P=Pi(left)-Pi(right). Fixed field values set wall field velocities to zero, and impermeability sets the matter velocity to zero when these traces exist. They leave pressure and static field/scale traction. Thus zero boundary energy work cannot be substituted for zero momentum flux; momentum can be transferred to the walls.

For rough states, H1 field values give Dirichlet traces but L2 gradients and field velocities generally do not give the stress traces needed in that global formula. L1 momentum/pressure also has no automatic wall trace. A weak impermeability condition, normal stress trace and enough time control must be supplied separately for wall tests or global momentum. Initial terms likewise require declared temporal weak traces. Compactly supported interior tests avoid those endpoint obligations but do not solve them. No artificial center wall is inserted.

## Exact scope and remaining implication

No load-bearing error was found and no correction was requested. The proof establishes a force-product counterexample, a full smooth conservative identity and a conditional domain in which candidate weak equations can be written. It does not establish weak equivalence or a nonlinear evolution. The next mathematical obligation must specify a product/compactness or approximation criterion and its trace requirements rather than assume that finite fluxes imply solutions.

Both registered a_ref values, 9.3619e-11 and 1.1279e-10 m/s², remain distinct positive hypotheses. Constant-vacuum/frozen-H cases are not identified with actual evolving-H histories. The author's additional qualification is correct: a spatially uniform time-varying reference need not add an explicit spatial force to the smooth translation identity, but it changes energy exchange and cannot inherit the assumed energy bounds without accounting for that work. Local responsive scale remains diagnostic. Signed MOND Q sources are retained; RAR/M, physical metric/photon/DOF, filtered-MONO, calibration and theory closure remain open.

## Exact pins

- `campaign_fresh_gravity_astra/stage_26/entropy_domain/CORRECTION.md`: `074561af900385e111dc8e7fe5cd8cf0e1124057b8cb5e17217e6a5e79ed1371`
- `campaign_fresh_gravity_astra/stage_26/entropy_domain/ROOT_DERIVATION.md`: `d227f50e3a8027db221f2a34c69481fedb55008d2edc6158c6fb0240cffced11`
- `campaign_fresh_gravity_astra/stage_26/entropy_domain/audit_result.json`: `2accec5b0bd30502a6f504b3a7b428bed6239539886209cf0414efa85735784a`
- `campaign_fresh_gravity_astra/stage_26/independent_audit/INDEPENDENT_AUDIT.md`: `1c67e6252471f2921682d63e5d153b7d6bbfbe255f27d57c92013a48940fe29a`
- `campaign_fresh_gravity_astra/stage_27/independent_audit/DERIVATION_FROZEN.json`: `60d9b5e6ef9e534965edd744ddfc6583fddc97139f984016f377a7f5416edd0e`
- `campaign_fresh_gravity_astra/stage_27/independent_audit/FROZEN_DERIVATION.md`: `04372794ede2e8bcf04761549957dfe0a590b641222cb9abb68f659b4445bf2e`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/FRAMEWORK_AND_EXECUTION.md`: `ff0d2873065578b0bd8aa50907e0a39495ff8da775bf2b4890768d83775fd750`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/RESULT_CONTRACT.json`: `ba388d0ca8e447a38649a478483e3ff4c2d3293e842eedc8f035499c77a20c29`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-023/fgf023_run_001/DERIVATION.md`: `0b9babab32edd602cf5aea8db63126a52f09c379b858e5c5967d46835bbf1f4a`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-039/fgf039_run_001/DERIVATION.md`: `c0f098c821ab9ec3346c3365fd9e45d8d536fe437ad47850fe38ecc523ebead8`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-039/fgf039_run_001/result.json`: `7a3ffddec2231f7d8606a94d243027b3c21b2d1ef1b456747ca9d9e2f41bb8b5`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-040/fgf040_run_001/DERIVATION.md`: `c9bf96698f5dc0675af01103e929bda4001e8f1b44f45e5960ae68a33ab0ca06`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-040/fgf040_run_001/REPORT.md`: `8e7a3face30f7eb15a8d55c05d0b75d65398c85c6c3c64fc87ddb432a4d5df04`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-040/fgf040_run_001/input_sha256.json`: `d2d30cfe488246be5d14a1d75d27547e7ff67f3eb4f2dbccf89766d0a27ee843`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-040/fgf040_run_001/result.json`: `4ba102598510b35d6a1f61e445c7d4bd954166e999d4eda89dc23635765badc4`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/reviews/FGF-032_RECONCILIATION.md`: `a7612d873f13635df650bb1ca09c824ceb91a191169a5b4861e243804e2464b0`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/reviews/FGF-039_RECONCILIATION.md`: `ff73e6c39d4cccde7bb2af14ae945cda129a75db87cbb4e01551e19b9e4fe4cd`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/tasks/FGF-040.md`: `87f048567e2ffdefcfa995b58c5dc757d92de07dc8a2deb2bad7c33e2e0603d0`
