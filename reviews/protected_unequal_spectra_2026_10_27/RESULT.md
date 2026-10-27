# Protected unequal spectra: an actual mechanism, but no joint MOND vacuum

> **Audit clarification (2026-10-27):** This is a restricted source-transfer and infrared audit, not a constructed microscopic model. Symbolic pass counts do not validate the missing physical bridges. See [adversarial audit](AUDIT_REWORK.md).

The requested interacting model has not been found. A genuine microscopic
mechanism exists for protected cancellations without level-by-level pairing:
modular invariance and tachyon absence in non-supersymmetric strings. This
avoids hand-tuned spectral weights. However, its established identities do not
fix the required gradient-response moment, and the explicit heterotic example
has a leading dilaton runaway rather than a stationary positive vacuum.

The new useful result is a conditional infrared separation lemma: gapped
partners cannot cancel K796's s^(5/2) term if their subtracted determinant has
uniformly convergent third derivatives. A symmetry protecting ultraviolet
supertraces therefore does not, by itself, settle the infrared response.

Kappa=1/2 remains FITTED. CFG493 kappa_Lambda=0.417 +/- 0.095 and kappa_crit=
0.345 +/- 0.078 are separate, unused. No fitted weights, target density or a0
enter this work. Positive regulated energy is not identified with rho_DE c^2.

## Duplicate-route check and scope

Read K796-K798, the previous SUSY Lifshitz result, and W4-04/W4-08 microscopic
normalization, symmetry and protected-auxiliary records. Targeted text searches
of reviews, why_4_puzzle and CFG894 for misaligned supersymmetry, Scherk-Schwarz,
SO(16), modular invariance and dilaton runaway found no matching earlier audit.
This is a scoped local-record check, not an exhaustive global novelty claim.
Exact pairing, independent uplifts, single-field detailed balance and the two
spectator potentials are already covered and are not new routes here.

## 1. What real protection supplies

The primary source hep-th/9503055v2, equations (1),(2),(11)-(13), derives
regulated mass supertraces from modular invariance and absence of physical
tachyons for its stated string classes. In four spacetime dimensions its
normalization gives Str 1=0 and Str M^2=-3 Lambda_string/(4pi^2).
The infinite sum must be regulated before taking the limit; a finite truncation
or exchanging expansion and sum does not inherit the identity. In ten dimensions
the lower moments through M^6 vanish for the cited SO(16)xSO(16) example.

These are genuine consistency-enforced cancellations across unequal levels,
not our four-node fixture. They are relations involving tree-level masses and
a one-loop vacuum amplitude, not an all-orders MOND nonrenormalization theorem.
They do not identify the source derivatives of those masses with our t_i, or
supply sum sigma_i d_i v_i t_i^(5/2)=0. A deformed background's partition
function and physical source dictionary would have to establish that arrow.
See [SOURCES.md](SOURCES.md) for pinned versions and locators.

Even at elementary algebra level, moments are not interchangeable: the signed
weights (15,-6,1) at t=(1,4,9) give M1=M2=0 but M(5/2)=66. This is only a
counterexample to inferring fractional moments from those two polynomial
moments, not a string spectrum or a new tunable candidate.

Ordinary unbroken supersymmetry would enforce equal energies for positive-energy
partners under its Hamiltonian algebra. A symmetry preserving a homogeneous
background and commuting with translations pairs dispersions at the same
momentum. This returns to the earlier paired route. Broken backgrounds,
spacetime-dependent symmetries, dualities and infinite-tower constraints lie
outside that simple argument. It is not a no-go on every possible symmetry.

## 2. New discriminator: the fractional term belongs to gapless response

Fix a finite spatial momentum cutoff L and any spatial dimension n. For a mode

    omega(s,k,mu)=sqrt(A+B s),
    A=m^2+D k^4 >= m^2>0,   B=gamma (1+mu^2) k^2 >=0,

its third source derivative for s>=0 is

    partial_s^3 omega = 3 B^3/[8(A+B s)^(5/2)] <= 3 B^3/(8m^5).

Subtract the Taylor polynomial through degree two. Taylor's integral remainder
is bounded in magnitude by B^3 s^3/(16m^5). Finite momentum integration therefore
leaves an O(s^3) remainder. Such a remainder cannot cancel a nonzero s^(5/2)
term, whose third derivative diverges as s^(-1/2).

The statement extends to an infinite gapped tower if the degeneracy-weighted
absolute third-derivative bounds are summable, for example

    sum_i d_i gamma_i^3/m_i^5 < infinity,

with uniformly controlled kinetic normalizations and angular factors. The
subtracted integrals then have a uniformly convergent third derivative near
zero. Divergent degree-zero, one or two terms must be handled as matching data;
no finite absolute vacuum is inferred from this subtraction.

The coefficient of s^((n+2)/2) in the massless Lifshitz mode follows from
k~sqrt(gamma s/D). For n=3 this is K796's s^(5/2). Thus, within this class,
its cancellation must occur among gapless response modes or through changing
the infrared dynamics. Massive spectral partners elsewhere in a tower cannot
do it merely by cancelling ultraviolet divergences.

### Twisted-tower diagnostic and control

For periodic bosonic masses |j|/R and antiperiodic fermionic masses
|j+1/2|/R, there is a bosonic zero mode and no fermionic zero mode. The remaining
masses are at least 1/(2R). With bounded response couplings and fixed
multiplicities their third-derivative sum is bounded by a constant times
sum j^(-5), so the gapped remainder cannot cancel the zero-mode fractional term.
Restoring zero twist supplies a massless fermion; with the same response
parameters its fractional term cancels. This is the mutation test.

This is a conditional KK response diagnostic, NOT a complete supersymmetric
MOND action. The required Lifshitz/gradient coupling is assumed for the test,
not derived from compactification. String spectra have exponentially growing
degeneracies: the polynomial KK summability estimate cannot be applied to
them wholesale. Their source-dependent modular amplitude requires its own
analysis. Accumulating gaps, interacting critical modes, nonlocal response,
or failure of uniform convergence are explicit exceptions, not excluded models.

## 3. Actual interacting candidate: nonsupersymmetric heterotic string

The SO(16)xSO(16) heterotic construction has a modularly completed torus
amplitude and an interacting string parent. The inspected published source
shows this amplitude in Eq.(2.14), its nonvanishing one-loop dilaton potential
in Eq.(2.15), and its leading Einstein-frame action in Eqs.(2.16)-(2.18).
Keeping only the relevant ten-dimensional terms, in its convention,

    S_E = 1/(2 kappa_10^2) integral sqrt(-g)
          [R - (partial varphi)^2/2 - T exp(5varphi/2)
             - exp(-varphi) H_3^2/(2*3!) + ...].

Here varphi is the string dilaton, NOT the MOND scalar phi. T is the positive
vacuum-potential coefficient in the considered branch, and kappa_10 denotes
the gravitational coupling, not the fitted acceleration-law coefficient.
No four-dimensional compactification or sourced MOND operator has been derived.

The exponent can be checked without choosing dimension first. A genus-one
string-frame constant has no tree-level exp(-2varphi) factor. Under

    g_string=exp[4varphi/(d-2)] g_E,

its volume element gives V_E=T exp[2d varphi/(d-2)]. For d=10 this is
T exp(5varphi/2), whose derivative is (5/2)V_E>0 at every finite varphi.
With fluxes and other stabilization terms absent, the constant-dilaton field
equation would require V_E'=0 and has no solution. Weak coupling varphi->-infinity
reduces the potential toward zero. A finite amplitude is not a stabilized
positive vacuum. This is a leading-truncation statement, not a theorem excluding
flux compactifications, further corrections, rolling cosmologies or all strings.

Likewise, in a fixed lower-dimensional metric frame a one-scale massless
Casimir potential V(R)=C/R^d has derivative -d C/R^(d+1). If C is nonzero,
it has no finite stationary radius. Weyl rescaling and additional physical
scales require a new potential calculation; this dimensional diagnostic is
not a full Einstein-frame radion analysis. Adding a stabilizer must be derived
and matched, rather than declaring its minimum to give the desired ratio.

The real microscopic example therefore improves on arbitrary weights but
fails the joint target: the known protected relation is not the infrared
response identity, the vacuum is not stationary in the tested sector, and the
MOND cubic, Newtonian coefficient and baryon portal are not jointly calculated.

## Verification, review and remaining route

Freeze: 435025a363. check.out passes 15/15 exact symbolic checks. The zero-twist
mutation gives 13/15 and exit 1, with the expected disappearance of the unmatched
massless contribution. These checks verify derivatives, powers and the stated
counterfactual, NOT a string spectrum computation or an interacting vacuum.
The infrared convergence proof and source-to-target distinction were separately
self-reviewed; no independent agent review or formal theorem certificate.

No empirical inputs in the executable, no target normalization substitutions,
no Friedmann argument, and no pooling of density footings. hbar and the
phase-space pi factors remain those of K796; neither is asserted to disappear
in a classical kappa prediction. No sources were downloaded to the repository.

The unequal-spectrum route remains OPEN, with a more precise missing object:
a source-dependent protected identity in the GAPLESS interacting sector,
compatible with a stable four-dimensional vacuum and physical baryon matching.
A modular vacuum partition function alone is insufficient. The explicit
flux-free heterotic truncation and gapped-KK repair fail their stated tests;
we have not closed all string or duality constructions. No concrete protected
MOND deformation of such a parent is identified in the inspected sources, so
inventing another spectral fixture or importing a mass sum rule would not
advance the target. The next needed input is that deformation and its symmetry
identity, not a choice of particle weights. Kappa remains unselected.
