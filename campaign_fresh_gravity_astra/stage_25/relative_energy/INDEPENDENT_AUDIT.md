# Independent root-only audit: FGF038 relative energy

Primary verdict: **proved as written**, within the explicitly capped finite-action class and the two sufficient shortness gates. This is a conditional diagnostic Q energy theorem, not a nonlinear evolution or physical-gravity closure result. No error was found.

## Exact claim and evidence boundary

For one fixed inherited crossing on I=(-l,l), with fixed positive C, cs², J, S0 and reference scale, take Eulerian perturbations with integral r=0, |r|<=rho/2 almost everywhere, psi,eta in H1_0(I), and |eta|<=1/4. If gates (4) and (5) of the reviewed proof hold, its exact energy difference satisfies

DeltaE >= integral cs² r²/(6rho) + k/(4C) integral A psi'^2
          + J/(2C) integral eta'^2 + S0/(4C) integral eta²,

where k=exp(-1/4)/64 and A is the background Q tangent coefficient. The right side is strictly positive for any nonzero perturbation (modulo equality almost everywhere). The gates hold on sufficiently short restrictions of the same inherited crossing. No numerical value of that size is established.

This is an independent root-only analytic inspection. I reconstructed the scalar inequality, first variations, scale derivatives, and all coefficient allocations without reading the new worker proof or the other reviewer's proof. No numerical sweep, symbolic package, or new mathematical computation was run. Hashing and report serialization are provenance operations. The proof record says that root froze its proof before reading new author/reviewer formulas; that provenance statement is recorded, not independently reconstructed from message history.

Reviewed immutable inputs:

- ROOT_DERIVATION.md: 404901535858dee0c368dd879c16cd329627ef372d1fa5e001e08af544056817
- PROOF_RECORD.json: d333bee0ab4897cf88355c0d66294f337c7c2a1922e527dd303eb44861a953fb

The record pins the old task and stage 23/24 ancestry. This review takes the stated inherited equilibrium and crossing regularity as the hypotheses of the local theorem; it does not claim to re-prove their construction or to revalidate every ancestor in this pass.

## Dependency graph and obligation matrix

| Obligation | Status | Decisive check |
|---|---|---|
| Signed Q scalar energy and curvature | Passed | F'=B and F''=A continuously at zero; no Newtonian substitution |
| Global scalar lower bound | Passed | The two interval arguments cover all real h, including sign reversal and unbounded amplitude |
| Finite scale change | Passed | A(g,a exp eta)>=exp(-1/4)A(g,a); scale remainder expanded only at fixed background g |
| Full first-variation cancellation | Passed | Chemical-potential, MOND flux, and scale equilibrium cancel all and only the linear terms |
| Density and scale remainder constants | Passed | Density 1/3 factor, potential curvature S0, and K_l,L_l bounds checked directly |
| Shortness and full mixed energy | Passed | Two Young inequalities and weighted endpoint estimate give exactly the four final coefficients |
| Admissible finite energy and strictness | Passed | Positive capped density, bounded positive scale, H1 gradients, mass and outer traces suffice |
| Existence of the inherited crossing | Conditional input | Fixed inherited diagnostic crossing as stated; no new construction in this audit |
| Nonlinear dynamics, cap invariance, physical interpretation | Out of scope | Explicitly excluded by the reviewed theorem |

The dependency chain is: inherited equilibrium and crossing -> exact first-variation cancellation and integrable reciprocal A; scalar convexity plus capped scale -> global field remainder; positive-density cap -> matter remainder; shrinking the same crossing -> two gates; gates plus the retained mixed term -> the stated strict lower bound. There is no numerical or external-source leaf in this argument.

## Reconstructed decisive checks

1. **All-amplitude scalar inequality.** The integral Taylor identity is valid because the even scalar F is C2, including at g=0. For |h|<=2|g|, t<=1/4 ensures |g+th|>=|g|/2. The integral of 1-t on this interval is 7/32. Monotonicity and concavity of A on nonnegative arguments give A(|g|/2)>=A(|g|)/2, hence 7Ah²/64. For |h|>2|g|, t>=3/4 gives |g+th|>=t|h|-|g|>|g|/2 and the weight integral is 1/32, hence Ah²/64. This second argument remains valid when h opposes g and crosses zero, and for arbitrarily large h. At g=0 the asserted bound is zero and convexity suffices; no division by g occurs. The scale comparison follows from sqrt(a² exp(2eta)+4g²)<=exp(d)sqrt(a²+4g²).

2. **Exact coupled cancellation.** Expanding the matter interaction gives phi r + rho psi + r psi. The first two terms combine with the density first variation and with B(g,a)psi' using e'(rho)+phi=mu, integral r=0, and B'=C rho. Thus integral rho psi=-integral B psi'/C. The scale first variation is (J chi' eta'+U'eta+W_chi eta)/C and vanishes by the scale equilibrium and zero boundary traces. Splitting the finite field change first at a'=a exp eta leaves exactly D_a'(g,h), (B(g,a')-B(g,a))h, and the fixed-g scale remainder. No density-scale term exists in the stipulated energy to be dropped; r psi is retained. B is continuous with the stated C1 regularity, so there is no spurious center boundary term or delta source.

3. **Remainder bounds.** Along the density segment, rho+t r<=3rho/2 and rho+t r>=rho/2, giving e''>=2cs²/(3rho). Taylor integration contributes 1/2, hence H_e>=cs²r²/(3rho). U''=S0 cosh(2chi)>=S0 gives R_U>=S0 eta²/2. Direct differentiation of b with respect to log scale gives the displayed absolute first derivative and second-derivative integrand. The elementary bound 1-(1+u)^(-1/2)<=u/2 gives |partial_theta B|<=g²/a_theta. Consequently qcap²/A=O(|g|³) extends continuously by zero at the crossing. The displayed second derivative of b vanishes at v=0 and is uniformly continuous for the compact positive scale range; integration to |g| proves K_l->0. All these uniform bounds concern one fixed background restricted to smaller intervals.

4. **Constants and gates.** The scale Young bound spends kA h²/2 from the available kA h² and costs L_l eta²/(2k). Gate (4) leaves S0 eta²/4. The matter Young bound spends cs²r²/(6rho) from cs²r²/(3rho), retaining cs²r²/(6rho), and costs 3rho psi²/(2cs²). The endpoint estimate follows directly from |psi(x)|²<=R_l integral A psi'^2 and integration over length 2l. Gate (5) makes the matter cost at most k/(4C) integral A psi'^2, leaving that same coefficient from the initial k/(2C). The J/(2C) gradient term is never spent. These are the exact final coefficients; no missing factor of C or 2 was found.

5. **Shrinking and units.** From A comparable to sqrt(|x|), R_l=O(sqrt(l)) and P_l=O(l^(3/2)); rho_max stays bounded. Both gates therefore hold for sufficiently short restrictions with all dimensional coefficients fixed. A and k are dimensionless, P_l has length squared, qcap has acceleration units, and K_l and L_l have acceleration-squared units, matching S0. C rho_max P_l/cs² is dimensionless. Each final term has the stipulated energy-per-transverse-area units.

6. **Domain and strictness.** The caps keep density positive and scale bounded above and away from zero. On the compact interval H1 fields are bounded, while Q's at-most-quadratic growth makes the full field energy finite for psi' in L2. The crossing has A>0 almost everywhere. A vanishing right side therefore forces r=0, eta=0, and psi'=0 almost everywhere; zero outer traces then force psi=0. No perturbed equilibrium equation or finite material-displacement map is required. This proves an exact restricted energetic minimum, not an assertion about an open ball of the larger weighted completion.

## Remaining gap and strongest safe use

The lower bound does not supply the failed upper bound, weighted continuity, or a uniform Taylor expansion. Concentrating perturbations with small weighted size and large positive exact energy remain compatible with it. Singular infinite-energy directions remain outside the admissible class.

No invariant-region result for either cap is given, and no nonlinear solution, uniqueness, weak energy conservation, or preservation of H1 finite action has been constructed. A dynamical use requires those additional properties (and the appropriate full conserved energy including nonnegative kinetic terms), rather than assuming the static energy alone is conserved. The cheapest next meaningful proof target is preservation of the stated admissible class for a specified local nonlinear evolution; the present audit neither asserts nor solves that target.

Both registered a0 values and the separate reference histories remain distinct conditional backgrounds. The result is Q-only, not a RAR/M or physical metric/photon result, an instrument constraint, or a theory closure. No historical novelty claim is reviewed or inferred.
