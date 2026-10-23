# Bath formation: missing quantum absorption channel and the unresolved transition

The existing action contains an omitted bath-assisted reaction,

\[
X+\Phi+\bar\Phi\leftrightarrow\Phi+\Phi,
\]

and its charge conjugate. We calculated its complete **vacuum tree** amplitude, thermal Maxwell–Boltzmann average, and equilibrium Bose correction. It is quantitatively important in the old conditional thermal trajectory. **We have not derived a thermalization epoch or a seed-free surviving cosmological abundance.** No new matching time or cold seed was selected in this calculation.

## Existing action and conventions

\[
V=m^2|\Phi|^2+M^2|X|^2+g(X^*\Phi^2+X\Phi^{*2})+\lambda|\Phi|^4.
\]

The unchanged benchmark is m=0.001 GeV, M=2m sqrt(1+0.02²), g=2.168e-6 GeV, lambda=0.00881292. Phi and X have charges 1 and 2. Densities n and nX below include both charge signs, balanced within each species. Define W=n+2nX.

An absorption event consumes one X, leaves total Phi number unchanged, and reduces W by two. Its energy becomes kinetic energy of the two outgoing Phi particles. This is a **heating and chemical-relaxation channel**, not an automatic source of cold particles. It needs Phi particles to scatter on; it does not supply the initially generated Phi population by assumption.

## Full five-point amplitude and absence of a vacuum real-intermediate-state pole

Use all-incoming external momenta p0,...,p4, with charges (2,1,-1,-1,-1). Physical incoming particles are indices 0,1,2; indices 3,4 are minus the outgoing momenta. Set

\[
d_j=(p_0+p_j)^2-m^2,\qquad
D_j=(\sum_{k\in\{2,3,4\}\setminus\{j\}}p_k)^2-M^2.
\]

Up to an irrelevant common sign, the complete amplitude is

\[
\mathcal M=\sum_{j=2}^4\left[\frac{8g\lambda}{d_j}
 +\frac{8g^3}{d_jD_j}\right].
\]

There are three cubic–quartic trees and three all-cubic trees. An independent unordered-partition recursion, rooted at each of the five external legs, agrees with this explicit expression to 2.38e-15 relative over the sampled checks.

For d2, X and the incoming antiPhi have future-directed momenta, so d2 >= (M+m)²-m² > 0. For d3 or d4, put k=pX-pout. If an on-shell k were future-directed, the other final Phi would be a sum of k and the two initial Phi momenta: an impossible massive 3-to-1 process. If k were past-directed, pout=pX+(-k) would itself be an impossible massive 2-to-1 process. Thus neither denominator can vanish in physical vacuum phase space. D2 is the final pair invariant minus M², bounded below by (M+2m)²-M². D3,D4 involve differences of equal-mass future Phi momenta and are <= -M². This establishes absence of real poles for **this physical channel**, independently of the finite sample checks.

The crossed channel X+antiPhi+antiPhi -> Phi+antiPhi is different: two initial antiPhi can form a real antiX followed by pair conversion. It needs real-intermediate-state subtraction to avoid double counting. Its complete subtracted kernel remains uncomputed. No bare pole integral was added.

Bath-assisted absorption has no analogue of the single-particle decay threshold M>2mPhi: with positive quasiparticle masses, initial rest energy MX+2mPhi always exceeds final threshold 2mPhi. The vacuum amplitude calculated here must not be extrapolated through the dense, strongly dressed source stage without computing its in-medium propagators.

## Rate, inverse reaction, and Bose factors

At zero incoming velocity,

\[
D_0=\frac{\sqrt{1-4m^2/(M+2m)^2}}{256\pi M m^2}
|\mathcal M_0|^2=1767.57819270\;{\rm GeV}^{-5},
\]

with M0=-0.0573020425738 GeV^-1. The forward contribution is

\[
\dot W+3HW=-D\,n_X n^2.
\]

The coefficient includes two conjugate channels, the identical-final-particle factor 2!, and removal of two W units per event. At finite temperature the MB average is

\[
D(T)=\left\langle
\frac{\beta_f|\mathcal M|^2}{256\pi E_X E_\Phi E_{\bar\Phi}}
\right\rangle_{\text{three normalized MB incoming momenta, outgoing solid angle}}.
\]

For a general incoherent quasiparticle distribution, the quantum gain–loss factor is

\[
f_0f_1f_2(1+f_3)(1+f_4)
 -(1+f_0)(1+f_1)(1+f_2)f_3f_4.
\]

This includes spontaneous terms, stimulated terms and the inverse 2-to-3 reaction. It assumes kinetic factorization; it is not an equation for a coherent quantum field with arbitrary connected correlations.

In a common-temperature BE state the affinity is mu0+mu1+mu2-mu3-mu4 = muX-muPhi+muAntiPhi, and the reverse/forward ratio is exp[-(muX-muPhi+muAntiPhi)/T]. In the balanced case muPhi=muAntiPhi this reduces to muX. With fast decay equilibrium muX=2muPhi, the net factor is 1-exp(-2muPhi/T). The forward magnitude still requires the actual Bose integral, not just this detailed-balance factor.

At mu=0, the equilibrium forward reaction-density enhancement relative to MB is about 1.16 at T/m=0.532, 1.67 at 1.031, and 3.01 at 2. These are **forward reaction-density ratios**, not ratios of coefficients normalized by BE number densities and not nonequilibrium bounds.

Seventeen temperatures T/m=0.01..2 were evaluated with independently scrambled Sobol samples of 16384 and 65536 points. Maximum coarse/fine difference is 1.99%; this is a sampling diagnostic, not a certified error bound. Four-momentum conservation, threshold behavior, equilibrium detailed balance and independent amplitude recursion checks pass.

## Material effect on the previous conditional result

No matching epoch was changed and no corrected relic abundance was manufactured. We inserted the new kernel as a diagnostic along the already saved old thermal trajectory:

- At its start T=m/2, the new forward W-loss prefactor is 0.41935 times the previous pair-plus-contact prefactor.
- At fixed total energy, its additional linear chemical-relaxation rate is 150.57 H, compared with 359.05 H from the old channels.
- Integrated on the **unchanged** old trajectory, its omitted net loss is deltaY=1.53771e-8, or 20.75% of that trajectory's final Y=7.40907e-8.

Do not subtract deltaY from the old Y as a prediction: heating, inverse rates and densities would respond. The old approximately 17%-of-target result was already conditional on thermal matching and is not a seed-free prediction; the new calculation shows that its partial reaction network also misses a material term.

## What can determine a bath-formation time

There is no exact, universal instant at which an interacting state becomes thermal. A controlled calculation must specify a tolerance, evolve the state, and measure when a common-temperature description becomes accurate and remains so under expansion. Choosing a tolerance is different from choosing a cosmological matching time.

Within a valid quasiparticle kinetic regime, fit a common beta and charge chemical potential to

\[
\log[(1+f_i(p,t))/f_i(p,t)]=\beta(t)[E_i(p,t)-q_i\mu_Q(t)].
\]

Check momentum-dependent residuals, small unresolved coherent/anomalous and connected correlations, and validity of narrow quasiparticles. A fit to energy density alone is insufficient. Elastic rates can establish momentum equilibrium without chemical equilibrium.

The stoichiometric matrix of the two decays and the two new absorption channels, in species order (Phi+,Phi-,X+,X-), is

\[
S=\begin{pmatrix}2&0&-1&0\\0&2&0&-1\\1&-1&-1&0\\-1&1&0&-1\end{pmatrix}.
\]

It has rank three and null vector (1,-1,2,-2). Consequently full chemical equilibrium leaves only the charge chemical potential. For the balanced neutral equilibrium branch it vanishes. W is not a protected number. A common nonzero particle-number chemical potential can persist only while the W-changing reactions are ineffective.

Near a controlled equilibrium solution, nonconserved perturbations relax through the eigenmodes of the linearized collision operator. Their integrated damping, not one chosen equality Gamma=H, sets loss of memory. Schematically a mode with rate gamma obeys exp[-integral gamma dt], with an expansion-driven forcing term. This linear statement is not a bound for the preceding far-from-equilibrium coherent stage.

The present source computation has not evolved that stage quantum mechanically. It retained a finite band of stochastic/Hankel modes, omitted intermediate infrared and ultraviolet modes, and then propagated classical fields. Its high-resolution result ends at H/M approximately 2.67e7. The much later four-cycle experiment used a separately prepared Phi bath. Neither supplies the continuous renormalized quantum evolution connecting them.

## Why a moments-only reconstruction cannot close the gap

The exact interaction contribution to the free X energy equation is

\[
\dot\rho_X+3H(\rho_X+P_X)
=-2g\,\mathrm{Re}\langle\dot X^*\Phi^2\rangle.
\]

It depends on phase-sensitive correlations. Reversing physical velocities while holding field coordinates fixed preserves kinetic and potential energies and reverses this transfer. The saved early and late 96-cubed states explicitly pass that check; it is an instantaneous algebraic diagnostic, not another cosmological history. The early realization carries a small nonzero sampled charge, which also reverses; it is not an exact same-charge counterexample.

For an exactly neutral quantum counterexample, compare the X-sign two-mode number state |N,N> with the mixture

\[
\rho_K=(1-N/K)|0,0\rangle\langle0,0|+(N/K)|K,K\rangle\langle K,K|,
\qquad K\ge N.
\]

Both have zero charge, mean occupation N in each sign, identical one-body two-point data, and identical free energy. With an identical Phi vacuum, their mean cubic interaction energies also agree. But the pair-annihilation transition weight <n+ n-> is N² versus NK. For N=10, K=1000 it differs by a factor 100. This is a leading transition-probability/kinetic-weight statement, not an assertion that the exact initial first time derivative of a number eigenstate is nonzero. Neither state is asserted to be the actual evolved inflationary state. The example disproves inference of its pair-conversion rate from the retained matching moments alone.

A fully specified initial quantum state and expansion history, evolved with the action, can in principle determine the needed correlations. They are missing from the **performed evolution**, not forbidden by the theory. A self-consistent nonequilibrium correlator calculation is the relevant next calculation; the general framework is described in [Berges, Introduction to Nonequilibrium Quantum Field Theory](https://arxiv.org/abs/hep-ph/0409233). That reference does not supply a solution for this action or establish novelty of this reaction.

## Reproducible evidence and remaining obligations

- `bath_assisted_conversion.py`, contract and `bath_assisted_conversion_run/manifest.json`: completed; new vacuum collision kernel and quantum state counterexample.
- `bath_transition_audit.py`, contract and `bath_transition_audit_run/manifest.json`: completed; old-path diagnostic, charge/number algebra, saved-state phase audit.
- Both manifests record exact commands, input hashes and bounded execution. Existing evidence was not overwritten.

Remaining: evolve source statistical and spectral correlations through X oscillation/conversion; obtain controlled in-medium collision kernels including the crossed RIS-subtracted channels; test actual thermalization without energy matching; evolve cooling and losses; only then extract the surviving cold abundance and its phase-space distribution. No scalar-to-collapse-medium bridge was added.

**Outcome:** a verified missing reaction and a quantitative correction to the reaction-network assessment, not a completed formation mechanism or a determined relic abundance.
