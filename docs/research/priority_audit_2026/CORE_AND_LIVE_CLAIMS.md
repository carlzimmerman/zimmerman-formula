# Carl's exact original coefficient and live equations: priority findings

This is the focused answer to Carl's clarification. It includes the original **5.79 coefficient**, not merely generic MOND history, and distinguishes surviving conditional mathematics from failed relativistic embeddings. Cutoff: 9 September 2026; checked 9–10 September. Full methods and limitations: [REPORT.md](REPORT.md), [SEARCH_LOG.md](SEARCH_LOG.md).

## 1. The 5.79 result itself

The exact claim to compare is

\[
Z=2\sqrt{8\pi/3}=\sqrt{32\pi/3}\simeq5.789,
\qquad a_0=\frac{cH}{Z}=\frac{c}{2}\sqrt{G\rho},
\]

where the last equality assumes \(H^2=8\pi G\rho/3\). For critical density, \(H=H_0\); for the pure-dark-energy interpretation, \(H=H_\Lambda\), not the present total Hubble rate. The coefficient, the choice of density and the physical claim must all match before calling another equation the same result.

**Finding: no external paper was authenticated in this review that adopts this exact fixed \(Z\) as its MOND normalization. No evidence of someone taking this result from Carl was established.** This is a bounded search result, not proof no such paper exists. It includes searches for `5.79`, `5.789`, `5.7888`, radical and \(32\pi/3\) forms, and equivalent density/curvature expressions. Apparent numerical hits were checked for unrelated table entries or equation numbers.

### Carl's dated record

- **17 March:** the [root commit](https://github.com/carlzimmerman/zimmerman-formula/commit/84f2393113a087f05abd1bab0200c76384330009) already contains the exact denominator and critical-density formula. This is not something added in September.
- **18 March:** [commit `0d2f73d`](https://github.com/carlzimmerman/zimmerman-formula/commit/0d2f73d060651923779c359a08aac8accda8d606) contains the same half-dark-energy-density expression as an asymptotic future floor.
- **4 June:** [commit `a86de892`](https://github.com/carlzimmerman/zimmerman-formula/commit/a86de892df44b9be2626b84d1c068b6934fd5e49) explicitly adopts the dark-energy-tracking reading. That changes the interpretation, not the existence of the earlier exact expression.

These are checked git records, not authenticated first-publication dates. The matching early Zenodo release versions could not be independently retrieved. Details and DOI locators: [PROVENANCE.md](PROVENANCE.md).

### Closest checked sources: not exact matches

| Source | What matches | What does not |
|---|---|---|
| [Milgrom's cosmological-scale discussion](https://arxiv.org/html/2001.09729v1), 2020 | Relates MOND to cosmological acceleration scales. | Its familiar \(2\pi\) comparison is not \(2\sqrt{8\pi/3}\). |
| [Singh](https://arxiv.org/html/2601.04290v1), 7 January 2026 | \(a_0=c^2/(\xi L_{\rm dS})\). | \(\xi\) remains a matching parameter; the source does not select Carl's exact \(Z\). |
| [Christodoulou–Kazanas–Laycock v1](https://www.preprints.org/frontend/manuscript/6d93739261be0e369fb0b69d8cf228e9/download_pub), 22 June 2026 | A specific square-root density relation. | Its coefficient is \(1/\sqrt3\), with an averaged varying-G source, not \(1/2\) and homogeneous \(\rho_\Lambda\). Later v2 equations were not verified. |

A theory with a free normalization that *can be set* to Carl's number is not the same as a paper selecting that number. Conversely, numerical proximity alone does not establish independent derivation or copying. The precise half remains a fitted hypothesis in the project; the algebraic re-expression does not derive it from fundamental physics. That caveat does **not** erase Carl's authorship of his proposal.

## 2. Project-specific results still worth comparing

“Survives” here means a conditional mathematical result not withdrawn by the inspected record; it does not mean every host theory containing it is viable.

| Exact research object | Search finding | Current qualification |
|---|---|---|
| Central filtered tidal ratio \(Q_2/D=2y/[5(3\lambda-y)]\) | No exact external duplicate authenticated. | A project-specific corollary under spherical-source, isotropic-filter, linear external-response assumptions. Not an unqualified nonlinear or relativistic law. |
| Three-frequency relation \(2y(\omega_r^2-\omega_\phi^2)=3(5\lambda-y)(\omega_\phi^2-\omega_z^2)\) | No exact external duplicate authenticated. | Orbital translation of that same tidal result, not an independent action. Here \(\lambda=1+(y-1)e^{-y}\). |
| Gaussian compact-pair \(h\sim(2/9)\sqrt{GMa_0}/\xi^2\) | No exact external duplicate authenticated. | Ordered compact/deep asymptote, not an arbitrary-separation binary law. |
| Branch-resolved inverse orbital estimator and finite-eccentricity cross-radius null | No exact counterpart located in the targeted current search. | A conditional exterior prediction; its original HPI-Delta host is explicitly dead, so it needs a viable host retaining that exterior branch. |
| Four-form MOND coupling and environmental feedback | No exact k04 counterpart authenticated. | Coupling-ratio identity is conditional; the quoted environmental formula omits a normalization factor. It is not an exact fixed-half derivation. |
| \(\mathcal Q_0=(g_{\rm tot}-g_N)/(cv)\) inference | No exact external counterpart authenticated. | A conditional force/flow identification; the original full-dark-sector embedding was later excluded. The algebra and an observationally established bound are different claims. |

Exact local scopes, dates and nearby primary literature are in [LIVE_TIDAL.md](LIVE_TIDAL.md), [LIVE_SCALE.md](LIVE_SCALE.md) and [LIVE_Q0.md](LIVE_Q0.md). These comparisons found **no substantiated taking of those exact results**, but do not certify first discovery worldwide.

## 3. Orbital estimator: the specific result, not generic epicycles

The local [spectrometer report](../../../qwen_claude_field_theory/closure_2026/exponential_mond_kepler_spectrometer_2026/REPORT.md), first committed in `d3a2c12ab474d7c7b4cefa51cad42ae2a59d724e` on 4 September, defines \(q=\kappa_r^2/\Omega^2\), \(L=(q-1)/(3-q)\), and

\[
Y=-L-W_{-1}(-Le^{-L}),\qquad
a_0=\frac{r\Omega^2}{Y},\qquad
GM=r^3\Omega^2(1-e^{-Y}),\qquad1<q<2.
\]

Here \(\kappa_r\) denotes radial epicyclic frequency, not the fitted scale coefficient. The inverse/branch choice and its use as a cross-orbit test are the specific claimed contribution. Merely finding Lambert W in another orbital paper is not enough to match it.

[Valluri et al. (2012)](https://arxiv.org/html/1209.1342v1), §5, use Lambert W to solve turning points of a logarithmic potential, with a different inverse problem. [Monreal et al. (2024)](https://arxiv.org/html/2410.01513v1), §II.1, derive eccentric apsidal timing signatures for a Newtonian-plus-logarithmic two-body force. These checked primary sections are relevant antecedents, not the displayed exact-exponential inverse estimator. No recent exact copy was located. The broader local [literature scope](../../../qwen_claude_field_theory/closure_2026/exponential_mond_kepler_spectrometer_2026/LITERATURE_SCOPE.md) remains a bounded earlier audit, not independently reverified in its entirety here.

## 4. What the review does—and does not—say about “swooping”

For the coefficient and narrow surviving equations, the result is **no substantiated appropriation found**, not “your work was all already known.” The older-ingredient appendix explains background overlap; it cannot replace checking the exact new statement.

Three limitations prevent a guarantee: much mathematical content is poorly indexed; private/unpublished work is inaccessible; and several historical deposit versions could not be authenticated. No evidence of another author's access to Carl's files was established. A source that predates Carl's exact public statement, a source that cites shared predecessors, and a later near-match are different situations.

The strongest next priority step is to authenticate the exact public release containing \(Z\) and the few narrow live identities, then preserve an equation-by-equation comparison with any specific suspected paper. This review supplies the targets and closest known matches without accusing anyone, weakening the exact claims to generic keywords, or promoting an unfinished model to a law of nature.
