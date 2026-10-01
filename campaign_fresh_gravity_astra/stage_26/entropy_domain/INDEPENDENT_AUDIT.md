# Independent root-only audit: FGF039 entropy domain

Primary verdict: **correct only after a stated restriction/clarification**: the sentence after (5) must refer to zero excess energy, not to all saturators of inequality (5). The exact inequality is correct for the stated fixed-background Q comparison class, sufficient shortness gates, and conditional trajectory hypotheses. CORRECTION.md supplies the necessary clarification; its counterexample and replacement statement have been checked. The energetic minimum has no density cap; the static comparison still imposes the scale cap. The scale no-exit statement requires an already existing conservative trajectory with the stated regularity.

## Claim, independence and source pins

On one fixed sufficiently short inherited crossing, let n>=0 have mass M and finite relative entropy to the positive background rho. Let psi,eta belong to H1_0(I), with |eta|<=1/4. The exact energy difference obeys

DeltaE >= cs² D(n||m_psi) + k/(4C) integral A psi'^2
          + J/(2C) integral eta'^2 + S0/(4C) integral eta²,

where m_psi=rho exp(-psi/cs²)/Z, Z is the normalized rho-weighted integral of exp(-psi/cs²), and k=exp(-1/4)/64. The two coefficient gates stated in the proof suffice. Zero excess energy forces the background state. The accompanying L1 estimate, arbitrarily low-energy density-cap and vacuum counterfamilies, and conditional scale barrier are also correct.

This is a root-only independent analytic reconstruction under the proof-audit workflow. I did not read the new author proof or the other reviewer's proof. I reconstructed the density minimizer, variance/log-moment estimate, retained full energy terms, L1 conversion, counterfamily and scale barrier. No numerical sweep or new mathematical computation was performed. File hashing and serialization only record provenance. The inherited FGF038 field bound was independently audited by this same reviewer in the preceding stage; that is a disclosed dependency, not a newly independent second derivation of that ancestor in this pass.

Reviewed source hashes:

- CORRECTION.md: 074561af900385e111dc8e7fe5cd8cf0e1124057b8cb5e17217e6a5e79ed1371

- ROOT_DERIVATION.md: d227f50e3a8027db221f2a34c69481fedb55008d2edc6158c6fb0240cffced11
- PROOF_RECORD.json: 3eca9d728844f3846162adaa8c4df2ffd15360446c86cc806b3f6c900b50ffe4
- Task FGF-039.md: 85ef997d2707f248bfd7838b2f2d14460e07fdc7d9c08fcabfb6d04b574fc6bc
- FGF038 root proof: 404901535858dee0c368dd879c16cd329627ef372d1fa5e001e08af544056817
- Prior root-only audit result: 3f0a467b1690423facd4ea3c5ccddfba1732bece07f78e098a56514c0b20dbc6

Every input and artifact hash listed in PROOF_RECORD.json was checked against its actual file and matched. The record's statement about root's freeze timing is recorded as its provenance declaration, not independently reconstructed from all root messages. Root source bytes were not changed.

## Dependencies and obligations

| Obligation | Status | Basis |
|---|---|---|
| Fixed inherited diagnostic Q equilibrium | Conditional input | The stated background, coefficients, crossing regularity and walls |
| Exact mass-constrained minimizer including vacuum | Passed | Algebraic entropy decomposition and pointwise strict convexity |
| Global log-moment constant 1/8 | Passed | Bounded-variable tilted variance and two integrations |
| Full matter/source/scale cancellation | Passed | Mass multiplier, signed MOND flux and scale equation |
| Field bound and first shortness gate | Passed, inherited | Personally audited FGF038 bound, independent of a density cap |
| Oscillation estimate and second gate | Passed | Reciprocal-A Cauchy-Schwarz and exact coefficient allocation |
| L1 estimate and change of reference | Passed | Direct scalar entropy bound and normalized exponential ratio |
| Arbitrarily small energy with cap violation or vacuum | Passed | Fixed-mass localized depletion and disjoint compensation |
| Scale barrier and conditional no exit | Passed | Two-sided endpoint inequality, H1 continuity and total energy |
| Unqualified uniqueness of inequality saturators | Failed in original; corrected | Nonbackground densities with unchanged fields saturate (5) |
| Zero-excess-energy uniqueness | Passed | All lower-bound terms must vanish when DeltaE=0 |
| Nonlinear solution construction, no vacuum, physical closure | Out of scope | Explicitly not concluded |

Dependency chain: the fixed isothermal matter law and mass constraint give an exact entropy decomposition; bounded psi gives the log-moment bound; background equilibrium cancels first variations; the inherited field bound plus the new shortness gate absorbs the negative density-minimized functional. Separate elementary estimates yield the L1 consequence and the density counterfamily. The scale barrier additionally uses endpoint geometry, while its dynamical consequence additionally assumes existence, topology retention and total-energy conservation. No external theorem citation or computation is needed to complete these implications.

## Decisive reconstructed checks

**Entropy and vacuum.** Since integral n=integral rho=M, the matter Bregman remainder is cs² integral n log(n/rho). The identity log(n/m_psi)=log(n/rho)+psi/cs²+log Z therefore gives exactly equation (1), including its minus signs in -M cs² log Z and -integral rho psi. For n=0, every expression is interpreted with 0 log 0=0; m_psi remains strictly positive and bounded. Finite entropy relative to rho is equivalent to finite entropy relative to m_psi because their logarithmic ratio is bounded. Pointwise f(z)=z log z-z+1 is nonnegative and vanishes only at z=1, including f(0)=1; this proves the asserted attained, unique constrained minimum without compactness. Finite entropy also suffices for integrability of e(n): the negative part of n log n is bounded on a finite interval, and log rho is bounded.

**Log moment.** After subtracting the rho-weighted mean of psi, X has mean zero. For F(t)=log<exp(-tX)>, direct differentiation yields F''(t)=Var_t(X), while F(0)=F'(0)=0. The tilted probability remains normalized and positive. For a variable in [L,U], its variance is at most its mean square distance from the midpoint, hence at most (U-L)²/4. Integrating with weight 1-t gives (U-L)²/8. Jensen's lower sign is obtained directly from exp(y)>=1+y. Thus the minimized matter contribution is bounded below by -M(osc psi)²/(8cs²), globally in the amplitude of bounded psi. No small-amplitude approximation occurs.

**Exact full energy and gates.** The density linear term cancels via e'(rho)+phi=mu and fixed mass. The rho psi term cancels integral B psi'/C because the background satisfies B'=C rho. Only the background source law is used: comparison states need not solve static field equations. The scale first variation vanishes using -J chi''+U'-T=0 with inherited T=-W_chi. The term (n-rho)psi remains in the exact entropy functional G; it is not lost in minimization. The inherited finite-scale field estimate spends no density assumption and yields k E_A/(2C), J integral eta'^2/(2C), and S0 integral eta²/(4C) under gate (3). Weighted Cauchy-Schwarz gives (osc psi)²<=R E_A. Gate (4), CMR/(8cs²)<=k/4, spends at most k E_A/(4C), leaving precisely the coefficient in equation (5). M=O(ell) and R=O(sqrt(ell)) on the same shrinking crossing, so this gate and the inherited scale gate hold without retuning coefficients. A>0 almost everywhere and zero outer traces ensure that zero energy excess forces psi=eta=0 and D(n||rho)=0.

**Density distance.** Taylor integration for f uses f''(z)=1/z along the segment between 1 and z, giving f(z)>=(z-1)²/[2 max(1,z)]. The limit at z=0 is valid. Multiplication by m and weakening max(n,m) to n+m gives the first inequality in (6). Cauchy-Schwarz with integral(n+m)=2M gives the constant 1/(4M), including at vacuum since m>0. Thus the controlled entropy is first a distance to m_psi. Since the exponential normalization lies between its extreme values, m_psi/rho lies between exp(-osc psi/cs²) and exp(osc psi/cs²). Integrating the pointwise ratio bound and combining with E_A<=4CE/k and D<=E/cs² gives exactly (7). No L-infinity control is inferred.

**Density counterfamily.** The compensating bump has unit integral and disjoint support, so the proposed n_epsilon has exactly mass M. At alpha=3/4 its depletion plateau is rho/4; at alpha=1 it is exactly zero. Background positivity on both chosen compact regions guarantees all stated estimates. The hydrostatic first variation vanishes by mass equality even though phi varies in space. With fields unchanged, the exact remainder is cs² integral rho f(n_epsilon/rho). On the shrinking depletion region its integrand is bounded and its measure is O(epsilon); on the compensation region the ratio is 1+O(epsilon), giving O(epsilon²) entropy. Hence both families have finite entropy and energy tending to zero. This disproves a positive energy threshold that alone rules out the old density cap violation or vacuum in this comparison class. It does not show that a positive classical solution reaches vacuum.

**Scale barrier.** For an interior x, zero boundary traces and two separate Cauchy-Schwarz estimates yield integral eta'^2>=eta(x)²(1/a_x+1/b_x)>=4eta(x)²/ell. H1 functions in one dimension have continuous representatives, so taking the supremum is legitimate. At norm d this makes the J gradient term at least 2Jd²/(C ell)=J/(8C ell). The other terms in (5) are nonnegative. For an already existing trajectory continuous in H1, its supremum norm is time-continuous, so exit from the cap requires a first equality time. At that time the static bound remains valid. Nonnegative kinetic energy gives total excess >= static excess >= E_bar, contradicting conserved total excess below E_bar. Static energy itself need not be conserved. The argument requires that all other admissibility and conservation assumptions persist to this time.

**Units and branch scope.** M is mass per transverse area; R has length; hence CMR/cs² is dimensionless. D has the units of M, so cs²D has energy per area units. The argument of the exponential in (7) is dimensionless: sqrt(C R E) has units cs². J/(C ell) has energy per area units, as required for the scale barrier. Both a0 values and all three reference-history uses remain separate backgrounds. The fixed-reference result supplies no evolving-reference reservoir, RAR/M transfer, metric/photon construction or observational calibration.

## Equality error, correction and cue chronology

My initial audit interpreted the proof's word “Equality” as equality with the background minimum, and explicitly used that narrower meaning in the report. That was too charitable to an adversarial audit of the literal inequality-saturation sentence. After the first audit files were written, root relayed an external author-audit cue and requested checking the unqualified sentence. I did not read the author or other reviewer proof; I independently checked the counterexample root supplied and then read root's separately attributed CORRECTION.md. This is a cue-assisted correction of the initial audit, not a discovery from a fully isolated second audit.

Choose a measurable subset E with integral_E rho=M/2 (available because rho is positive on an interval). Set n=(1+epsilon)rho on E and n=(1-epsilon)rho elsewhere, where 0<epsilon<1, and take psi=eta=0. This is positive, fixed-mass, finite entropy and nonbackground. The exact energy remainder and the entire right side of (5) are both cs²D(n||rho)>0. Hence inequality (5) is saturated by a nonbackground density. The sentence “Equality forces ... n=m_0=rho” is false if equality means saturation of (5).

The corrected claim is exactly: **DeltaE=0 forces the background state.** Equation (5) then makes each nonnegative lower term vanish, giving eta=0, psi=0 and D(n||rho)=0. Conversely the background has zero excess. CORRECTION.md preserves the original proof bytes, withdraws uniqueness of all inequality saturators, and states this narrower valid equality conclusion. No constant, gate, L1 bound, counterfamily or scale barrier requires changing. The initial audit's acceptance has accordingly been revised; the original wording is not accepted without this clarification.

## Remaining gap and strongest safe statement

The result extends the exact static minimum to all fixed-mass nonnegative finite-entropy densities, with no pointwise density cap. It also supplies a conditional energetic obstruction to leaving the scale cap. The equality sentence needs the explicit zero-excess clarification above; the remaining claims require no further restriction beyond their stated hypotheses.

The missing dynamical implication is an actual nonlinear evolution that exists in, and retains, the required entropy/finite-action/H1 class and conserves the full energy with the stipulated boundaries. The density counterfamily prevents using small energy alone to obtain pointwise density positivity or the old density cap. A targeted next investigation must address those evolution/regularity properties directly; repeating the static estimate cannot establish them. The failed weighted upper bound and continuity from FGF037 remain failed. No full nonlinear stability or theory closure follows from this audit.
