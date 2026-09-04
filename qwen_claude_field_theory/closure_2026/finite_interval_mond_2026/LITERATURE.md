# Finite-interval MOND tests: literature and novelty boundary

Audit date: 2026-09-04. This note records a bounded prior-work search, not a
certificate of global novelty. The study's frozen choices are in
`CONTRACT.md`; no empirical result is asserted here.

## What the two equations add

Write positive baryonic radial acceleration as b and the algebraically
predicted dynamical acceleration as g. For the specific isolated response

\[
b=g\mu_{\exp}(g/a_0),\qquad \mu_{\exp}(y)=1-e^{-y},\qquad a_0>0,
\]

define

\[
L(y)=\frac{d\ln\mu_{\exp}}{d\ln y}=\frac{y}{e^y-1}.
\]

For finite y>0, 0<L<1 and L'<0. Consequently,

\[
s=\frac{d\ln g}{d\ln b}=\frac1{1+L},\qquad
\frac{ds}{d\ln b}=-\frac{yL'}{(1+L)^3}>0.
\]

Integrating 1/2<s<1 over b_lo<b_hi gives the finite-response bounds

\[
\sqrt{\frac{b_{\rm hi}}{b_{\rm lo}}}
 <\frac{g_{\rm hi}}{g_{\rm lo}}
 <\frac{b_{\rm hi}}{b_{\rm lo}}.
\]

Convexity of ln g as a function of ln b gives, for b0<b1<b2,

\[
t=\frac{\ln(b_1/b_0)}{\ln(b_2/b_0)},\qquad
J=\log_{10}g_1-(1-t)\log_{10}g_0-t\log_{10}g_2<0.
\]

Each logarithm of an acceleration uses the same fixed reference unit, which
cancels from J. Changing the logarithm base changes J's magnitude, not its
sign. The closed versions use <= and include the pure Newtonian and pure
deep-MOND limiting power laws; these have J=0. The ordering is by b, not by
galactocentric radius. These inequalities concern model values, not an
assertion that every noisy observed triple must obey them.

These are elementary finite-interval consequences of a response's slope and
convexity, not independent physical postulates. The MOND endpoint powers
alone do not imply global bounds or convexity. The empirical RAR response
g=b/[1-exp(-sqrt(b/g_dagger))] is distinct from the implicit mu_exp response;
it and the simple-mu response nevertheless share these two qualitative
properties. Derivative-based comparisons of interpolation functions are
established: Desmond, Bartlett and Ferreira explicitly define the
logarithmic slope in Section 3.3, Eq. (4), compare response shapes, and test
recovery with mock data. They caution that finite dynamic range and data
uncertainty limit inference about the generating function and its
asymptotes. [Desmond, Bartlett & Ferreira, *On the functional form of the
radial acceleration relation*, MNRAS (2023),
DOI:10.1093/mnras/stad597; checked arXiv:2301.04368v2, 1 March
2023](https://arxiv.org/abs/2301.04368v2).

The sign/bound tests contain no measurable a0 normalization: passing them
cannot identify mu_exp uniquely or confirm a proposed a0-Lambda relation.
The accompanying exact predicted ratios and exact J values can depend on
a0 and distinguish specified kernels. They still test a rotation-law
phenomenology, not its derivation from a covariant action.

## Closest external prior work

- **Within-galaxy normalization and nuisance cancellation are known.**
  Frandsen and Petersen normalize each galaxy's baryonic and total
  accelerations to values at a reference radius in Eq. (11), and introduce a
  local-reference average in Eq. (14). Appendix A derives cancellation of
  common distance and inclination factors in normalized observed
  accelerations, subject to a radius-independent inclination. This is
  direct prior art for normalized two-radius shape observables; changing
  notation or taking logarithms does not create a new physical test.
  [Frandsen & Petersen, *Investigating Dark Matter and MOND Models with
  Galactic Rotation Curve Data*, arXiv:1805.10706v1, 27 May
  2018](https://arxiv.org/abs/1805.10706v1).

- **Equal-baryonic-acceleration branches and g-squared-space loops are
  known.** Petersen and Frandsen discuss the coincidence of the inner and
  outer branches for a single-valued algebraic relation, and the associated
  zero-area closed curve. Section 4, Eqs. (9)-(14), constructs an empirical
  inner/outer comparison with corrections for unequal sampling in baryonic
  acceleration. Their g_N and g_tot correspond to this study's b and g.
  Thus an equal-b null, an inner-minus-outer residual, or a signed-loop
  diagnostic is not a newly discovered MOND discriminator.
  [Petersen & Frandsen, *A method for discriminating between dark matter
  models and MOND modified inertia via galactic rotation curves*, MNRAS
  **496**, 1077 (2020), published primary
  text](https://academic.oup.com/mnras/article/496/2/1077/5850781).

- **Other normalized radial-profile tests already exist.** Rodrigues,
  Hernandez-Arboleda and Wojnar define the additional squared velocity
  Delta V^2=V_obs^2-V_bar^2 in Eq. (1), then normalize its radial profile by
  the value at the outermost radius in Eq. (7). They compare such profiles
  with MOND and dark-matter models using SPARC. A new statistic must be
  distinguished from this existing normalized-shape program.
  [Rodrigues, Hernandez-Arboleda & Wojnar, *Normalized additional velocity
  distribution: testing the radial profile of dark matter halos and MOND*,
  Physics of the Dark Universe **41**, 101230 (2023),
  DOI:10.1016/j.dark.2023.101230; checked
  arXiv:2204.03762v2](https://arxiv.org/abs/2204.03762v2).

- **Individual RAR tracks, bends and hooks are already discriminants.**
  Mercado and collaborators study non-monotonic tracks in simulations and
  in SPARC, with observational caveats. Their work is relevant to any
  curvature/branch test; a finite chord is not the first proposal to use
  shape information beyond a pooled RAR fit.
  [Mercado et al., *Hooks & Bends in the radial acceleration relation:
  discriminatory tests for dark matter and MOND*, MNRAS **530**, 1349-1362
  (2024), DOI:10.1093/mnras/stae819](https://doi.org/10.1093/mnras/stae819).

No exact match to this study's combination of a baryonically selected broad
triple, paired finite-response and chord statistics, and shared-measurement
covariance handling was located in the bounded search. That is not proof
of methodological priority. The supportable contribution is a new
repository implementation and empirical comparison of explicit finite
corollaries. Stronger claims of a new physical law or a globally new
observable are not established.

## Repository prior work

The local search found relevant predecessors:

- `prep_2026/mi_fingerprint/PRIOR_ART.md` already surveys modified-inertia
  versus modified-gravity rotation-curve discriminants.
- `prep_2026/equation_book/MINE_M1.md` and
  `prep_2026/equation_book/eqbook_S8_estimators.py` already construct
  distance/inclination-cancelling two-radius estimators and three-radius
  consistency tests. Those explicit inversion formulas use the older
  quadratic response g^2=b^2+a0*b, not the present mu_exp law, and must not
  be imported unchanged.
- `hunt_2026/k_unexplained-regularities_closure.py` explores whether
  candidate regularities restate a one-radius relation and includes
  synthetic controls. Its synthetic outputs are not independent empirical
  evidence for this study.

Earlier local novelty language is not treated as authentication of
priority. These files were inspected, not rerun as part of this literature
audit.

## Domain and statistical qualifications

An algebraic mapping of the Newtonian radial force in a disk is not an
exact generic non-spherical AQUAL or QUMOND solution. Field geometry and
the external field can alter that mapping. Nor does testing an exact
circular-orbit algebraic rule exhaust modified inertia: Milgrom's
Section VI.3.2 contrasts the circular-orbit relation with modified gravity,
and Section VI.3.3, Eqs. (45)-(47), exhibits non-circular/vertical-motion
dependence in modified-inertia models. The present comparison must not be
described as a rejection or confirmation of every MOND theory.
[Milgrom, *MOND as manifestation of modified inertia*, checked
arXiv:2310.14334v2, 16 November 2023](https://arxiv.org/html/2310.14334v2).

Common multiplicative rescalings of g cancel from log ratios and J because
their coefficients sum to zero. This does not remove radius-dependent
inclinations, uncertain stellar mass-to-light ratios, non-circular motions,
or inter-ring covariance. Uncertainty in b can change both t and the
selected ordering. One triple per galaxy avoids counting many overlapping
triples as independent, but does not supply missing covariance. Bootstrap
intervals conditional on the available inputs are not a complete theory
likelihood. Selection, sensitivities and limitations are fixed in
`CONTRACT.md`; SPARC has already been extensively analyzed in this
repository, so this is not an unseen-data preregistration.

## SPARC provenance

The primary distribution is the [official SPARC
website](https://astroweb.cwru.edu/SPARC/), which provides the galaxy
catalogue (Table 1) and Newtonian mass models (Table 2 and individual
rotation-model archive). The master publication is [Lelli, McGaugh &
Schombert, *SPARC: Mass Models for 175 Disk Galaxies with Spitzer Photometry
and Accurate Rotation Curves*, AJ **152**, 157 (2016),
DOI:10.3847/0004-6256/152/6/157](https://arxiv.org/abs/1606.09251v1).
Original HI/Halpha references are listed in Table 1 and should be credited
when appropriate.

The local `real_research/data/SPARC_Lelli2016c.mrt` has the expected
Table-1 title and fixed-width schema, including distance, inclination,
disk scale length and quality flags. In contrast,
`real_research/data/SPARC_table.txt` is an HTML **404 error page**, not a
usable data table. It must not silently enter analysis. This audit verified
these local headers and the primary distribution page, not byte identity
of every local rotation-model file with a newly downloaded archive. The
analysis manifest must identify and hash the actual local inputs and
record the parsing/sign conventions. No papers were cached for this audit.

## Search scope and remaining novelty work

The 2026-09-04 search covered relevant repository Markdown/Python/text/TeX
files and primary arXiv, journal and official SPARC sources. Query families
included Frandsen/Petersen g-squared space; equal-baryonic-acceleration
inner/outer branches; normalized two-radius acceleration and additional
velocity profiles; RAR loops/hooks; logarithmic slopes, convexity and
finite intervals. Full source text was checked for the equation/section
claims above, rather than treating search snippets as proof.

This was not an exhaustive ADS search, complete backward/forward citation
traversal, or survey of every non-English source. Remaining work before a
priority claim includes searching explicitly for secant-slope bounds and
Jensen/chord tests of interpolation functions, checking cited predecessors
and successors, and comparing the complete proposed estimator and error
model. Independent data, more complete nuisance covariance and appropriate
disk-field predictions are separate requirements for a stronger physical
conclusion. A failed search alone satisfies none of them.
