# Scope of the cited material-frame action principle

Checked 2026-10-15. **Verified framework support; conditional application.**
This check concerns the current-rest-frame action in
`sol61_push/reciprocal_tether_medium_2026_10_14/REPORT.md`, not its mode calculation.

## Authenticated source

François Gay-Balmaz, *General relativistic Lagrangian continuum theories —
Part II: electromagnetic fluids and solids with junction conditions*,
[arXiv:2511.18383v1](https://arxiv.org/abs/2511.18383v1), submitted
2025-11-23 10:22:29 UTC. Read the
[official exact-version HTML](https://arxiv.org/html/2511.18383v1) and checked
the downloaded [exact-version PDF](https://arxiv.org/pdf/2511.18383v1).
The PDF has 58 pages and its first page identifies v1 and 23 Nov 2025.

The project-root cache returned zero exact-identifier or author hits. The earlier
RTM `LITERATURE.json` explicitly recorded no retained full text. An ignored
lane-local cache now retains the PDF and `pdftotext -layout` extraction; this
keeps every new file within the assigned literature lane. Cache verification
returned `valid: true`, one record checked, no issues.

- PDF SHA-256: `d0a4537e4e62e729d8cb7d396af90afa0ac31c7bdae30cf1480c00528d537d1f`.
- Extracted text SHA-256: `bc22f737a4f2ecc2fa7fa1ca74b7060a1652f9dd1ea0c32a63616020a8525286`.
- Extraction: available, Poppler `pdftotext` 26.04.0. Local availability is not
  assumed on another clone; full text is ignored, not a tracked artifact.

## Source extraction: paraphrase and locators

The following is the bounded source summary.

- §4.1, (4.1)–(4.4), pp. 31–32: electric, magnetic, displacement and intensity
  fields are decomposed relative to a normalized timelike observer velocity.
- §4.2.1, (4.11)–(4.30), pp. 33–37: that velocity belongs to one material
  world-tube. The action depends on density, entropy and rest-frame fields.
  Proposition 4.1 varies material motion and the gauge potential; its Eulerian
  variations are induced Lie-transport variations. Mass and entropy are
  advected. The resulting equations couple continuum stress balance and Maxwell
  dynamics.
- §4.2.2, Example 3, (4.50), p. 44: nonlinear isotropic response may depend on
  the three electric/magnetic scalar invariants. Constitutive stress details
  are left to the reader.
- Remark 4.8, p. 42: the action's density called epsilon requires an electric
  Legendre transform to give physical rest energy.

Source status: variational propositions with derivations, plus an illustrative
nonlinear constitutive example. [Source, §§4.1–4.2](https://arxiv.org/html/2511.18383v1#S4).

## Translation to the project's one-current notation

For the displayed project signs, set c=1 and use the dictionary below. These
equalities specify a proposed local identification; they do not establish global
equivalence of different fluid variable systems.

| Project | Source convention / required identification |
|---|---|
| spacetime dimension 4, signature -+++ | specialize the source's dimension to 3+1 |
| n, J=nU | rho=mn, rho u=mJ, with fixed m>0 |
| U=J/sqrt(-J.J) | u at c=1 |
| electric and magnetic one-forms | E and B, with the same orientation for the Hodge star |
| particle charge q | source specific charge q_src=-q/m for its displayed minus coupling and the project's plus coupling; an overall charge/potential convention can reverse this sign |
| epsilon_fluid(n), L_e(E), beta(E,n) | total source action-density function epsilon_src=epsilon_fluid-L_e+beta B²/2, after the entropy specialization |

The last row concerns the complete field-plus-fluid density: adding a second
Maxwell term would double count it. The project's `epsilon_fluid` alone is not
the source's complete `epsilon_src`.

**Implication checked:** the citation supports a covariant constitutive action
whose frame is the varied material motion. It does not by itself prove that
arbitrary independent component variations of J, with no conservation or
vorticity structure, are a fluid theory. The project's Clebsch description must
recover the appropriate local conserved-current Euler equations and vorticity
sector. Timelike nonzero density, smoothness, an entropy/EOS choice and compatible
endpoint or boundary conditions are part of that application. No source theorem
about global Clebsch coordinates is imported here.

## Additional two-species commitments: project inferences

These are application requirements inferred here, not results attributed to the
paper.

1. Use two independent material variations (or a demonstrated equivalent
   constrained-current representation). A single common displacement only
   describes locked motion. Keep each species' current future timelike on the
   proposed fluid domain; charge cancellation does not remove either material
   degree of freedom.
2. Specify the constitutive frame and all constitutive arguments. One possible
   definition is the normalized total number current N=J_++J_-, on N.N<0;
   another is a species frame. A charge current q_+J_++q_-J_- can vanish for a
   neutral pair medium and cannot generically define its rest frame. A common
   background rest frame does not require equal species perturbations. Vary
   every chosen frame through every current on which it depends.
3. State whether relative-flow invariants or entrainment are included or set to
   zero by assumption. Covariance permits dependence on J_+.J_- as well as the
   separate densities and field invariants. The one-species citation does not
   choose these functions or justify neglecting cross-response terms.
4. Use one shared gauge potential and count its pure-field action once. Define
   the signed gauge source j_q=q_+J_++q_-J_- explicitly. Derive the separate
   material equations, the gauge equation and the total reciprocal stress from
   the same proposed action.
5. Choose the continuity contract. Separate untouched Clebsch shift symmetries
   impose div J_+=div J_-=0, which excludes species production. If reactions are
   intended, supply source equations div J_a=Gamma_a with
   q_+Gamma_++q_-Gamma_-=0 and a consistent energy/momentum exchange mechanism.
   The source does not supply that mechanism.
6. Establish the admissible density domain, frame regularity and boundary
   conditions. A normalization involving N does not automatically extend through
   N=0. Fresh coupled mode and constraint calculations are required after adding
   the second material displacement; one-fluid characteristics cannot be
   inherited by citation.

## Remaining implication and search boundary

The unresolved arrow is: **a specified two-current action and its admissible
variations imply the intended species equations, constraints and reciprocal
stress, with the required physical properties**. It must be derived in the
project. This source check supplies no engineered constitutive law, causal-cone
proof, conversion operator, microscopic identification or physical viability.

Classification: framework known after notation translation; two-current
application conditional. Search scope was the exact cited preprint/version,
project-local cache and the dependent RTM report/record. No novelty survey,
citation-graph search or claim about the wider multifluid literature was made.
