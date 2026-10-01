# Independent root-only audit: FGF042 energy compactness

Primary verdict: **proved as written**, under the stated strengthened shortness gates and comparison-state hypotheses. No mathematical error was found. The time-dependent conclusion additionally requires already-existing trajectories, all-time energy inequality and retained regularity. The result concerns vanishing full excess about one fixed static background; it does not prove general finite-energy compactness or nonlinear evolution.

## Exact claim and provenance

On a fixed sufficiently short restriction of the inherited Q crossing, vanishing full relative total energy controls the full kinetic energy, an exact Q Bregman remainder, weighted potential energy, scale H1 energy and relative entropy to the tilted matter minimizer. Retaining that Bregman term and splitting increments at a dimensional threshold proves unweighted strong L2 convergence of the potential gradient. The other estimates imply strong convergence of matter density, internal energy, kinetic quantities and scale fields, hence strong L1 convergence of combined momentum, stress and full energy density. Only the field contribution to energy flux is controlled; the general matter energy flux remains outside the conclusion.

I reconstructed the new retained-remainder budget, scalar increment bound, entropy return, kinetic/vacuum arguments and product-identification implications from the root proof. I read task FGF042 and checked every source pin in the proof record. Prior root proofs and action definitions are known from earlier audit work; old author/reconciliation artifacts listed in the record were hash-checked, not used as substitutes for checking the current argument. No new FGF042 author or other reviewer proof/preview was read. No numerical scan, symbolic calculation or other mathematical executable was run. Hashing and report serialization are provenance operations. Root's freeze-timing statement is recorded as a provenance declaration, not independently reconstructed from all messages.

Principal source hashes:

- ROOT_DERIVATION.md: 30c4906982fffc0a31475b4363ed01c8e0153be407c214d995729bf86a31d938
- PROOF_RECORD.json: 1994dfcc3c021c2cbe52b30c0245f2530cee39a9750442326b261c3aa0c054bb
- Task FGF-042.md: 178321d66829f9479c064ede82bb580e5796f41a50d81f7b0a71c28516d0e6fb

All other input hashes are retained verbatim in audit_result.json and were verified against the actual files. Root proof bytes were preserved.

## Dependency graph and obligations

| Obligation | Status | Decisive check |
|---|---|---|
| Inherited static Q crossing and action | Conditional input | Fixed positive coefficients, induced walls/mass and stated regularity |
| Full exact relative energy and signs | Passed | Mass, MOND flux and scale first-variation cancellations |
| Retained Bregman budget and all constants | Passed | Half-remainder split and the two distinct Young/entropy costs |
| Strengthened gates nonempty | Passed | Same-crossing small-gradient asymptotics, no retuning |
| Increment-sensitive scalar inequality | Passed | Both signed cases, including zero background gradient |
| Dimensional threshold and unweighted L2 | Passed | Fixed threshold first, then threshold tending to zero |
| Entropy reference and internal energy | Passed | Exact equal-mass identity and nonnegative pointwise remainder |
| Kinetic and vacuum conventions | Passed | Finite quotient, sqrt-density estimate, zero limiting kinetic contribution |
| Strong momentum and energy-density identification | Passed | All constitutive and quadratic factors checked separately |
| Limited field energy flux | Passed as scoped | Strong L2 products; no fluid cubic/enthalpy claim |
| Conditional time/barrier argument | Passed as scoped | H1 time continuity plus energy inequality at hitting time |
| Nonlinear construction or physical closure | Out of scope | Neither follows from the static comparison estimates |

Dependency chain: inherited equilibrium -> exact finite-increment energy decomposition; global signed Q convexity and bounded scale -> retained field remainder; constrained entropy minimization and two strengthened gates -> inequality (1); increment-sensitive convexity -> threshold estimate (3) -> unweighted strong convergence. Entropy and kinetic estimates complete the strong product identifications. The time result adds separate trajectory and energy-inequality assumptions; these are not conclusions of the preceding chain.

## Reconstructed constants and edge cases

**Exact energy.** W_chi=-T, so subtracting the background scale first variation produces +T eta in Frel. The hydrostatic multiplier multiplies the zero mass difference. The background source B'=C rho cancels integral rho psi against the linear B h/C term. The scale gradient and potential linear terms cancel by the scale equation and zero traces. The remaining matter interaction is exactly integral(n-rho)psi in G; no finite coupling term is lost. Comparison states need not satisfy a static source law. K contains all three nonnegative kinetic contributions, with the stipulated vacuum convention.

**Retained convexity.** Split D into two equal parts and use only one half to provide k A h²/2. The elementary square

qcap |h eta| <= k A h²/4 + qcap² eta²/(k A)

spends half of that weighted contribution. The background scale Taylor remainder costs Kcap eta²/2. Adding Urel>=S0 eta²/2 and gate G1 leaves S0 eta²/4 while retaining D/2, k A h²/4 and the full J eta'^2/2. At the center qcap=0; qcap²/A has continuous zero extension, so no forbidden division survives. Exact matter minimization costs at most M R integral A h²/(8cs²), which is alpha/C times the weighted integral. Gate G2, alpha<=k/8, therefore leaves k/(8C). The resulting coefficients in (1), including 1/(2C) in front of the retained D, are correct. No part of K or the entropy remainder is spent.

**Nonempty gates.** Uniformly on the bounded positive scale interval, b(s,a)=s²/a+O(s^4), so B_chi=O(s²) and W_chichi=O(s³). The latter also follows by differentiating the exact integral: its scale second-derivative integrand is O(s²) near zero. Since A is comparable to |g| and |g| is comparable to sqrt(|x|), both Lcap and Kcap are O(d^(3/2)). The fixed background density gives M=O(d), while reciprocal A is integrable with R=O(sqrt(d)). Thus alpha has the same vanishing order. G1 and G2 hold on sufficiently short restrictions of one unchanged central solution. These are stronger sufficient gates than before and are not silently inherited from weaker constants. Each final comparison takes place on a fixed selected interval with fixed mass and wall data.

**Increment inequality.** If |g|>=|h|/2 and t<=1/4, the reverse triangle inequality gives |g+t h|>=|h|/4. If |g|<|h|/2 and t>=3/4, it gives the same bound. The weighted t integrals are respectively 7/32 and 1/32. Since A is increasing in absolute gradient, the integral Taylor formula gives D>=h² A(|h|/4,a')/32 for all signed g,h. This includes large opposite-sign increments and g=0; h=0 is trivial. A decreases as a increases, so amax is a valid common comparison scale. Splitting |h|<=r and |h|>r gives the first term ell r² and the tail term 32 integral D/A(r/4,amax). Inequality (1) bounds integral D by 2C mathcalE, giving exactly 64C mathcalE/A(r/4,amax). For every fixed r>0 the denominator is positive. Taking the sequence limsup before sending r to zero proves the unweighted L2 result. No exchange of these limits or uniform Hessian lower bound is needed. Indeed W(h,a)~|h|³/(3a) at g=0 verifies the stated failure of a positive pointwise quadratic constant.

**Field and entropy norms.** The kinetic and scale coefficients in (1) give the quoted factors 2C/tau, 2C/sigma, 2C/J and 4C/S0. The sharp two-endpoint elementary estimate ||eta||_infinity²<=ell||eta'||²/4 is valid for H1_0 representatives and yields uniform scale convergence. Weighted control and zero traces give ||psi||_infinity<=osc psi<=sqrt(8CR mathcalE/k). Ordinary H1 convergence follows from the unweighted derivative convergence and fixed traces.

The tilted minimizer has mass M and remains strictly positive. Its logarithmic ratio to rho is bounded in absolute value by osc psi/cs². The entropy-to-L1 estimate remains valid at vacuum. Returning the reference uses the exact equal-mass identity D(n||rho)=D(n||mpsi)+integral n log(mpsi/rho); the possible negative sign of the last term is harmless for the stated upper bound. This gives vanishing relative entropy to rho, which is genuinely stronger information than density L1 convergence alone. Pointwise convexity gives e(n)-e(rho)=H_e+e'(rho)(n-rho) with H_e>=0 and integral H_e=cs²D(n||rho). Taking absolute values proves the displayed L1 internal-energy bound, including n=0. The positive bounded background makes e'(rho) bounded.

**Kinetics and vacuum.** At vacuum finite energy enforces j=0 and z=j/sqrt(n)=0 by convention. Pointwise (sqrt(n)-sqrt(rho))²<=|n-rho| gives strong square-root-density convergence. The kinetic budget gives ||z||²<=2 mathcalE, so z tends strongly to zero regardless of vacuum holes in approximating densities. Therefore j tends to zero in L1 by Cauchy-Schwarz with fixed M, and j²/n tends to zero in L1. No hidden limiting kinetic quotient remains. No lower pointwise bound on n is asserted; localized vacuum holes remain compatible with these convergences.

**Product identification and flux scope.** Strong L2 field derivatives/velocities identify all their quadratic products. The exact bounds |B_g|<=1 and |B_a|<=1/2 identify B in L2 under uniform scale convergence, and hence B(g+h,a')(g+h) in L1. This is the explicitly clarified meaning of the shorthand B(g+h) in the displayed Pi. Integrating |B|<=|g| and using |W_a|=T/a<=|g|/2 identifies W in L1. U converges uniformly. Finally,

||n(phi0+psi)-rho phi0||_1
<= M||psi||_infinity + ||phi0||_infinity ||n-rho||_1,

so the interaction also converges in L1. Together with the internal and kinetic estimates, every term of combined momentum, stress and full energy density is identified strongly in L1. Field energy flux is a product of strongly convergent L2 factors and therefore converges in L1. General fluid energy flux involves cubic velocity and current-times-enthalpy factors that these norms do not control. The proof correctly makes no full energy-flux or local energy-equation passage claim, nor any conclusion that the separate force n(g+h) is always integrable.

**Conditional time statement.** While the scale cap holds, the retained J term and the endpoint inequality imply mathcalE>=2J||eta||_infinity²/(C ell). At equality of the cap, the exit energy is J/(8C ell). Strong H1 continuity in time makes the supremum norm time-continuous, giving a first hitting time if exit occurs. At that time the stated all-time energy inequality and initial energy below the barrier contradict the lower bound. The proof explicitly assumes the inequality at that represented time rather than upgrading an a.e.-time estimate without traces. For a sequence of initial excesses tending to zero, all sufficiently late members are below the barrier. The same fixed-threshold limsup argument, with sup over time, gives uniform-in-time strong L2 convergence on the already-existing common interval. This argument neither constructs those trajectories nor proves their energy inequality, entropy retention or continuation.

**Controls and dimensions.** With density and scale fixed, G=0 and Frel=D, so the exact energy reduces to K+integral D/C as claimed. The finite-energy FGF041 packet does not satisfy vanishing excess; its vanishing-amplitude control does. This one-way energy-to-norm statement does not contradict the failed weighted norm-to-energy upper/Taylor bound. Kcap, Lcap and S0 have acceleration-squared units, alpha and k are dimensionless, and both terms in (3) have acceleration-squared times length units. The threshold r carries acceleration units. The barrier has energy-per-area units. Both registered a0 values and distinct reference histories remain separate conditional backgrounds; the fixed-reference inequality supplies no evolving-reference reservoir.

## Remaining gap and strongest safe conclusion

Vanishing full excess energy about the selected static Q crossing rules out the momentum, stress and energy-density concentration mechanism of FGF041 in this changed class. The static implication, its kinetic/vacuum extension and its explicitly conditional time consequence are supported without correction.

What remains missing is an approximation or nonlinear evolution mechanism that supplies the assumed energy inequality, regularity/entropy persistence, initial and wall traces, and any additional fluid energy-flux control needed for a local energy law. The result does not address compactness at bounded nonzero excess, comparisons between arbitrary solutions, physical metric/photon coupling, observational calibration, historical novelty or theory closure.
