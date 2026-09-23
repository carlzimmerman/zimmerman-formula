# Sources and bounded overlap check

Checked 2026-09-21. Primary sources were read through the web tool. Stable versions
and locators below are sufficient to repeat the extraction; no source PDF is
redistributed in this package. Source authentication is separate from the
applicability of a stellar-atmosphere approximation to an LRD.

## Sun et al., arXiv:2609.09274v1

[Overmassive No More](https://arxiv.org/html/2609.09274v1), sections 2.2, 2.4 and
3.1, Table 2. The fits constrain net gravity; the authors assume negligible
dynamical correction for their fiducial stack masses. Radiation is already
included in the hydrostatic models. The dense CLOUDY layer's quoted size is
thickness, not central radius. Numerical inputs used here: median log g=-2.2
(cgs), R=941 au; luminous (-2.5,1989); intermediate (-1.9,900); faint (-2.5,747).
These are separate stack summaries, not epochs of one object. Their shared
sample and posterior covariances prevent treating them as independent tests.

Translation: their fitted g becomes g_s here; true Newtonian gravity is g_N.
Their g_net=g-g_dyn becomes g_s=g_N+a_gas only under the explicit momentum and
atmosphere-matching assumptions in PROOF section 1. Outflow velocity alone does
not specify acceleration. Wave U's cancellation is algebraically valid but its
identification of the measured parameter with g_N needs this extra hypothesis.

## Zhang et al., arXiv:2512.05180v1

[Little red dot variability over a century reveals black hole envelope via a giant Einstein cross](https://arxiv.org/html/2512.05180v1),
main pulsation discussion, Figure 3 and Methods “Pulsation scenario.” R2211-RX1
has a fiducial photometric redshift near 4.3 and multiple lensed images sampling
different emission times. The 32-year period is fixed using an assumed mode
factor and Eddington-based mass, then used in a multiband sinusoidal fit. It is
not an independent period measurement. The paper calls for future spectroscopy;
it does not supply the phase-resolved atmosphere gravities needed here.

Application: this motivates a target and warns against a circular period/mass
test. Its photometric record alone does not validate the phase-gravity law.
The current package does not turn photometric magnitudes into a measured radius
amplitude or combine this individual source with the other paper's stack as data.

## Barcza, arXiv:astro-ph/0304188v1, A&A 403, 683–691 (2003)

[Distance and mass of pulsating stars from multicolour photometry and atmospheric models](https://arxiv.org/pdf/astro-ph/0304188v1),
section 2.3, equations (11)–(15); DOI
[10.1051/0004-6361:20030410](https://doi.org/10.1051/0004-6361:20030410).
This is direct prior art for recovering mass and distance from atmospheric
gravity, changing photometric radius and momentum balance. It explicitly retains
dynamical corrections and distinguishes a material radius from an opacity-driven
apparent radius. It is not a theorem that these corrections vanish for BH*s.

Translation: its ge is the outward support inferred from a static atmosphere;
the present g_s includes radiation consistently in that support. The leading
equation g_s=GM/R²+R'' is known after translating notation and neglecting the
specified residual terms. Our finite-window integral equations and harmonic
form follow by elementary integration by parts/Fourier transformation. They are
formal corollaries, not a claim of globally novel mathematical physics.

## Chen et al., arXiv:2606.04711v1

[ABCD: The Nuclear Structure of the Little Red Dots Revealted through Absorption, Break, Continuum, and Decrement](https://arxiv.org/html/2606.04711v1).
The absorber covering fractions belong to a decomposition of emitting and
absorbing components. Their existence does not establish the photospheric disk
covering fraction required by a simple occultation bound. This is why a discovery
query suggesting large covering factors did not become a claimed observation
excluding the local-density coincidence.

## Search boundary and status

Repository comparison: read BHSTAR_CAMPAIGN_INDEX, the review through Wave U,
Waves K/P/R/S/T/U, the CFJC draft and the existing I13 pulsation file. Searches in
real_research, fable_independent_2026, deepseek_push and qwen_claude_field_theory
used “Baade”, “Wesselink”, “photometric-hydrodynamic”, “phase gravity”, cycle/gravity
and harmonic/gravity variants. The proposed inversion was not located in that
scope. The existing algebraic Eddington readout and radius-density relation are
acknowledged dependencies, not relabelled discoveries.

Web discovery used general search and arXiv/publisher primary follow-up. Queries
included “little red dots effective gravity acceleration pulsation mass”,
“black hole stars gravity radius acceleration mass pulsation”, “photometric
hydrodynamic method atmospheric acceleration surface gravity distance mass”,
and LRD/BH* combinations with “Baade-Wesselink”, “photometric-hydrodynamic” and
“harmonic”. Backward comparison to stellar methods found Barcza immediately.
The same researcher performed discovery and verification; no independent novelty
review or exhaustive ADS citation traversal was performed.

Standing: known stellar dynamics, a missed application in the inspected BH*
campaign, with a concrete integral estimator and falsifiers. No world-first
claim, measured detection, or proof that the material-photosphere premise holds.
