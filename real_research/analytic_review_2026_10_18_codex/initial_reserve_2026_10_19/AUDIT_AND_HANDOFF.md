# Propagation results and the strict radial continuation

19 October 2026. Checkpoint ZAR-2026-10-19-07; parent ZAR-2026-10-19-06. The Git HEAD observed at the start was f4424595259bd1ae40addb890e338f85c4f48eb1. Input hashes and parent checkpoint identity, rather than arrival time or a moving repository HEAD, pin the mathematical base. All prior files remain unchanged.

## Target contract and current result

The requested target is a verifiable nonstationary initial-data condition that propagates the outward binding reserve, keeps the entire halo within one finite radius for all time, and retains nonlinear stability, the law and radial dispersion. A future work or launch condition merely restated as a hypothesis is not completion. A stationary distribution, a label change or a massless tracer is not accepted as nonstationary data.

P1 meets that target in the full central kinetic equations on the spherical-density subspace: the nonstationary orientation-odd perturbation changes real velocity correlations, retains the exact radial law and dispersion, and has a propagated pointwise envelope and restricted nonlinear stability. It is outside the earlier SO(3)-invariant radial phase-distribution class. This symmetry enlargement is explicit; the strict radial target remains open.

P2 sharpens the obstruction inside the strict radial class. Smooth initially even data, zero radial current and a negative initial energy cap can coexist with actual self-consistent expansion of a tiny exterior population. Its core law and dispersion are exact and the whole solution stays O(delta) close in X. The construction requires a broad angular interval, added mass and an exterior initial tail; its energy gap is delta-dependent. It does not decide the canonical unchanged-support problem with a separately prescribed initial gap.

| Claim | Strongest statement | Proof and dependencies |
|---|---|---|
| ZAR-P1 | Exact confined nonstationary angular-current sector, preserved density/all radial moments, propagated initial binding and restricted full-phase nonlinear stability | ORIENTATION_ODD_INVARIANT.md; old exact smooth equilibrium and direct central transport |
| ZAR-P2 | Smooth self-consistent initially bound radial shell with positive collective energy and uniformly small mass/kinetic deviation has unbounded outer support | INITIALLY_BOUND_EXPANDING_SHELL.md; old core plus radial one-population global flow, barrier and virial |
| ZAR-P3 | Initial density/current/pressure matching does not propagate a fixed field | RADIAL_PROPAGATION_OBSTRUCTIONS.md, equations 25-26 |
| ZAR-P4 | Exact linear work correction, actual nonzero diagonal resonance and finite-energy mode compatibility; no nonlinear bound is inferred | RADIAL_PROPAGATION_OBSTRUCTIONS.md, equations 27-33 |
| ZAR-P5 | Nearby two-species independent homologous breathing is excluded on the overlapping law annuli | RADIAL_PROPAGATION_OBSTRUCTIONS.md, equations 34-36 |

## Routes executed and scoped outcomes

The invariant-class route found P1. Its uncertain implication was whether odd angular-momentum orientation stayed invisible to density after transport. Conservation of L_z and radial dependence of the remaining factor close that implication exactly. Positivity and support are propagated by a checkable initial relative bound. Averaging restores precisely F, proving that the mechanism has no nonzero strictly radial version. This closes this route's symmetry question, while preserving a useful larger kinetic sector.

The initial-order and counterexample route found P2. The key distinction is the factor one half in collective self energy versus the full self potential in individual energy. A separate centrifugal comparison proves spatial separation without assuming it. The isolated exterior population then embeds exactly into the full model, and positive conserved Hamiltonian gives the unbounded-support conclusion. The even-velocity version also closes the zero-initial-current shortcut in this range. No claim of fixed-mass canonical escape or one permanently escaping packet is made.

The normal-form route derives the pointwise linear correction psi-h/F_E. The old integral estimates do not bound it near the flat edge. A proposed uniform nonresonance condition fails on the actual kernel: the diagonal denominator vanishes where the free-species coupling is strictly nonzero. This closes only division by uniformly bounded-away-from-zero denominators. Principal-value cancellation and self-consistent phase mixing remain open. Arbitrary prescribed resonant forcing is not silently promoted to a valid normal mode: finite quadratic energy imposes a vanishing numerator on a regular resonant surface.

The moment and homology checks close two additional shortcuts. The initial shell angular moment can change despite matching all radial velocity moments, and its effect appears in the second density derivative. The fixed point baryon term, together with the exact-law coefficients and warm velocity interior, excludes the nearby independent-homology ansatz. Neither result excludes other radial breathing solutions.

## Review provenance and validation

Read-only route agents worked from the same pinned parent with disjoint conceptual tasks and no write scope. The primary agent derived and checked the orientation-odd mechanism, reconstructed the tail barrier/energy/virial argument, and reconciled the linear response normalization before writing the new artifacts.

Fresh-context reviewers were separately given the actual raw proof files, conventions and named prior inputs, without the authors' desired verdicts. Their exact final hashes, conditions and verdicts are recorded in CHECKPOINT.json. Agent agreement is not a mathematical certificate; the displayed transport identities, inequalities and counterexample carry the claims. A self-review of the five new Markdown files checks notation, local links, delimiters and the strict-radial versus spherical-density qualifications.

No external theorem is a hidden new leaf. The one-population global flow used for the tail is the earlier characteristic theorem with a positive central point mass, zero tether population and a fixed positive angular interval. No simulation, orbit integration, statistics, scientific script or process operation supports these conclusions.

## Exact continuation

The strict radial target remains: identify an explicit nonstationary initial-data class near F with a prescribed uniform negative gap, original support or canonical mass/Casimir constraints, and propagate an invariant controlling the outward reserve. The orientation-odd theorem proves something stronger about radial observables in a different symmetry sector, but cannot be used to assert this missing implication.

The next executable normal-form step is to analyze the actual resonant integral operator with its principal-value cancellation, first on compact eccentric action bands, and determine whether a signed-work estimate can survive passage to the flat outer cutoff. A quantitative estimate for psi-h/F_E or a support barrier would close the needed implication; a formal division by the resonant denominator would not. Nonlinear phase mixing has not been proved or assumed.

A second open continuation is a genuinely radial invariant support family outside the excluded homology ansatz, with a proof of nonstationarity and a barrier verified from initial data. The initial evenness and moment-matching route needs an additional propagated angular-moment hierarchy; the first two moments do not supply it. These continuations are deferred at these specific mathematical leaves, not declared impossible or exhausted.

The broader initial-bound-gap conjecture is refuted only in P2's stated range. The fixed-gap, narrow-angular, canonical or unchanged-support versions retain their separate status. No nonspherical stability theorem, full interpolation/covariant completion, formation mechanism, parameter selection or new observational validation is claimed. The authorized resource boundary remains analytic work only and new checkpoint files only.
