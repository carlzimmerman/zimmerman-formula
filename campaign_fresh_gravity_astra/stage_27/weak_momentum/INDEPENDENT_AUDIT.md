# Independent root-only audit: FGF040 weak momentum

Primary verdict: **proved as written**, within the stated fixed-reference Q diagnostic action and explicit state/spacetime hypotheses. No mathematical error was found. The finite-energy force counterexample is an admissible comparison state, not a solution. The combined weak system has meaningful coefficients; existence and weak equivalence are not established.

## Normalized claim and provenance

There exist positive fixed-mass finite-entropy densities and zero-trace H1 potential perturbations with finite exact energy for which n phi_x is not locally integrable. Such states can have arbitrarily small nonnegative exact excess energy on the previously selected short crossing. For smooth solutions of the stipulated equations, the exact combined momentum is

P=j-(tau u g+sigma w k)/C,
F=j²/n+cs²n+[B g-W+tau u²/2+sigma w²/2+J k²/2-U]/C,
P_t+F_x=0.

Under the stated spacetime integrability and bounded-scale hypotheses these coefficients, along with the mass and field equations, define a distributionally meaningful candidate system. No undefined force product is needed for that candidate definition. Its equivalence to a separate forced Euler equation is proved only for smooth solutions.

This is an independent root-only analytic reconstruction under the proof-audit workflow. I read the root derivation and record, task FGF040, and the pinned old FGF023 action; the old FGF039 root and correction are known from my preceding audit. I did not read any new author or other reviewer proof. No mathematical numerical or symbolic run was performed. All source pins in PROOF_RECORD.json were checked against the actual files and matched. Hashing and report serialization are provenance operations. The root record's freeze-timing declaration is recorded, not independently reconstructed from all root messages.

- ROOT_DERIVATION.md: 9eb8d61177602f4cf4cc093bf43162ec997ced56693dc9e0ee709e601c5d534a
- PROOF_RECORD.json: 202f5617944d5368b133432546e5046ea3921076f05f9cb815ab29f44c5ec29e
- Task FGF-040.md: 87f048567e2ffdefcfa995b58c5dc757d92de07dc8a2deb2bad7c33e2e0603d0
- FGF023 DERIVATION.md: 0b9babab32edd602cf5aea8db63126a52f09c379b858e5c5967d46835bbf1f4a
- FGF039 ROOT_DERIVATION.md: d227f50e3a8027db221f2a34c69481fedb55008d2edc6158c6fb0240cffced11
- FGF039 CORRECTION.md: 074561af900385e111dc8e7fe5cd8cf0e1124057b8cb5e17217e6a5e79ed1371

## Dependency graph and obligation matrix

| Obligation | Status | Decisive evidence |
|---|---|---|
| Fixed Q diagnostic action and crossing | Conditional inherited input | Pinned action, fixed reference, short-patch background |
| Density mass, positivity and entropy | Passed | Convex mixture with normalized integrable singular density |
| Potential H1 traces and full finite energy | Passed | q=1/3, zero-integral derivative, bounded potential |
| Nonintegrable separate force | Passed | Positive leading exponent p+q=13/12 |
| Arbitrarily small excess strengthening | Passed | Exact remainders bounded by O(epsilon)+O(epsilon H)+O(H²) |
| Full smooth momentum identity | Passed | Independently differentiated both field contributions and matter equation |
| Spacetime coefficient integrability | Passed | Explicit L1/L2 assumptions, bounded scale, elementary constitutive bounds |
| Distributional signs and tests | Passed | Direct integration by parts for compactly supported tests |
| Smooth versus weak equivalence | Passed as scoped | Reverse algebra only when products and chain rules exist |
| Walls and traces | Passed as scoped | Local testing uses no traces; global balance requires more |
| Nonlinear existence/closure/physical interpretation | Out of scope | No such conclusion asserted |

The logical chain is: inherited energy/action -> admissible exact singular state and smooth equations; integrable singular powers -> finite energy but divergent force; exact background cancellation and the prior lower bound -> arbitrarily small nonnegative excess. Separately, smooth product differentiation -> combined momentum identity; additional spacetime bounds -> an L1 candidate weak system. Passing from that candidate definition to an actual evolution is deliberately not a proved arrow.

## Reconstructed critical implications

**Exact state and singular product.** The normalized F_p has mass one and integrable F_p log F_p because p=3/4<1; the logarithmic factor near the singularity does not change that threshold. Where the smooth cutoff vanishes, its f log f term is bounded, so it adds no entropy divergence. The mixture n=(1-epsilon)rho+epsilon M F_p is strictly positive almost everywhere, has mass M and finite entropy. The potential derivative has zero integral by the compensating bump, belongs to L2 since 2q=2/3<1, and its primitive is H1_0 and bounded. The disjoint support and choice away from the background cusp isolate a bounded, smooth background. W<=g²/2, finite entropy, bounded potential and L1 density verify every exact energy term; the scale field is unchanged and kinetic energy is zero. Setting instantaneous velocities to zero does not assert that the field accelerations or dynamical source vanish.

Near the chosen point, the product of the two leading singular pieces is positive and proportional to epsilon H |y|^(-13/12). Its integral diverges. The background times the density singularity has exponent 3/4, and the background density times the gradient singularity exponent 1/3; both are integrable and cannot cancel the leading term. The correcting bump is absent locally. Thus the positive part of n g has infinite local integral. The example is not a solution and need not satisfy the static source equation. A distributional extension of this product would require an additional prescription.

**Small exact energy.** Convexity gives D((1-epsilon)rho+epsilon M F_p||rho)<=epsilon D(M F_p||rho), with the right side finite. At fixed scale the exact field Bregman remainder is nonnegative and at most h²/2 because 0<=A<=1 globally, including sign crossings. The retained interaction is bounded by ||n-rho||_1 ||psi||_infinity<=2epsilon M H times a fixed profile constant. Exact background first variations cancel by the inherited equilibrium, equal mass and zero traces, so these are all remaining terms. Therefore an upper bound tends to zero with epsilon,H>0 tending to zero. Nonnegativity follows from FGF039's valid lower bound on the selected sufficiently short patch; its corrected equality wording is irrelevant to this inference. The singular product persists for each positive pair. This is a proved small-energy obstruction to defining the force on the entire energy class, not a dynamical instability claim.

**Momentum signs and scale terms.** At fixed reference, W_x=B g_x-T k. Therefore (B g-W)_x=B_x g+T k. The source B_x=Cn+tau u_t and g_t=u_x give

Cng=(B g-W+tau u²/2)_x-(tau u g)_t-T k.

The scale equation gives T=sigma w_t-J k_x+U'. With k_t=w_x,

-Tk=-(sigma w k)_t+(sigma w²/2+J k²/2-U)_x.

Substitution into j_t+(j²/n+cs²n)_x=-ng yields precisely the stated P and F. Both field momentum terms enter with minus signs, both kinetic stresses with plus signs, the scale gradient stress is positive, and U enters with a minus sign. No n phi term is silently omitted: the matter force has been replaced using the dynamic source and both field identities. The positive matter pressure follows from the pinned isothermal action. Smooth reversal with the field equations recovers the separate momentum equation; mass conservation remains separate.

**Spacetime integrability.** Finite fixed mass gives integral n=M T over the bounded slab. Finite integral j²/n forces j=0 on vacuum under the stated convention, and Cauchy-Schwarz gives ||j||_1<infinity. The stipulated u,g,w,k in L2 make ug and wk integrable and every quadratic stress integrable. For Q, b(s)<=s and monotonicity imply 0<=B g-W<=g². B is L2 since |B|<=|g|. Bounded chi makes a,U,U' bounded. Direct differentiation gives

T_s=-a b_a=s b_s-b=a b/sqrt(a²+4s²),

which lies between zero and a/2. With T(0)=0 this gives 0<=T<=a|g|/2, hence T in L2. These are genuine spacetime hypotheses; finite values at every time alone are not an integrable-in-time bound. The proof does not infer all these unweighted norms from the weaker relative-energy metric alone.

**Distributional and boundary scope.** For compact tests, integrating tau u_t-B_x+Cn gives -tau u zeta_t+B zeta_x+Cn zeta, as stated. The scale test has -sigma w zeta_t+J k zeta_x+(U'-T)zeta. All factors are integrable. The combined test is integral(P zeta_t+F zeta_x)=0. No distributional acceleration is multiplied by a gradient, and no n g term is needed. This defines a candidate system, not a weak-limit passage or proof of equivalence of rough formulations. L1 coefficients need not have pointwise wall/initial traces. For smooth walls the integrated balance has F(left)-F(right); fixed field values and impermeability set velocities/current to zero there but do not cancel the remaining pressure or field tractions. Global momentum conservation therefore does not follow from those boundary conditions.

**Units and framework.** F_p and b0 have inverse-length units, Z_p and c_q have length units, and H has acceleration units, making h an acceleration and psi a potential. P has momentum per volume units and F has stress units under the action's tau and sigma dimensions; dividing field terms by C is essential. This is signed Q MOND source bookkeeping with both positive a0 values separately admissible. It proves nothing for RAR/M/filtered MONO or a physical metric. Fixed-reference use does not erase the separate evolving-reference work/reservoir obligation.

## Exact remaining gap

The strongest safe conclusion is that the separate L1 force formulation fails on the full admitted energy domain even arbitrarily near the background in exact excess energy, while the combined momentum coefficients permit a local distributional candidate under the stated time-integrable bounds. There is no error requiring source correction in this pass.

To obtain a nonlinear solution from approximation one still must identify the constitutive and quadratic flux limits, justify field compatibility and boundary/initial traces, and prove the appropriate energy statement. Uniform bounds alone do not identify products of weakly convergent sequences. The cheapest useful next target is a specified approximation/compactness claim for one of those fluxes, including possible defect terms. No nonlinear solution construction, uniqueness, weak equivalence, global momentum conservation, covariant conservation, calibrated evidence, historical novelty or theory closure follows here.
