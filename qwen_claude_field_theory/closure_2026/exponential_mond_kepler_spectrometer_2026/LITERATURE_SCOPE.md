# Literature and novelty scope

Search date: 2026-09-04

Purpose: determine whether the exact-exponential spherical MOND map

\[
q={\kappa^2\over\Omega^2}
\longmapsto
L={q-1\over3-q}
\longmapsto
y=-L-W_{-1}(-Le^{-L})
\]

and the resulting one-radius inference of \((a_0,M)\) had already appeared in
the repository or in the bounded external search.  The follow-up search also
covered the transition-wide \(O(e^2)\) fundamental-frequency correction,
guiding-radius correction, distance-free cross-radius null, and the
branch-selected exact all-orders inverse/null.  This is a search record, not
proof of worldwide novelty.

## Primary sources checked

1. J. Bekenstein and M. Milgrom, “Does the missing mass problem signal the
   breakdown of Newtonian gravity?”, *Astrophysical Journal* **286** (1984)
   7–14, DOI 10.1086/162570.
   [NASA ADS scan](https://adsabs.harvard.edu/pdf/1984ApJ...286....7B)

   Relevance: derives AQUAL from a Lagrangian and obtains
   \(\nabla\cdot[\mu(|\nabla\phi|/a_0)\nabla\phi]=4\pi G\rho\).  It establishes
   the action-derived starting point but does not state the exact exponential
   kernel, the epicycle inversion, or a Lambert-branch spectrometer.

2. M. A. Abramowicz and W. Kluźniak, “Epicyclic orbital oscillations in
   Newton's and Einstein's dynamics,” arXiv:gr-qc/0206063.
   [arXiv](https://arxiv.org/abs/gr-qc/0206063)

   Relevance: primary discussion of orbital and radial epicyclic frequencies.
   It supports the established orbital machinery, not the MOND-specific
   inverse map.

3. R. M. Corless, G. H. Gonnet, D. E. G. Hare, D. J. Jeffrey, and
   D. E. Knuth, “On the Lambert W function,” *Advances in Computational
   Mathematics* **5** (1996) 329–359, DOI 10.1007/BF02124750.
   [DOI](https://doi.org/10.1007/BF02124750)

   Relevance: authoritative branch structure for the multivalued inverse of
   \(w\mapsto we^w\).  The present calculation needs the real \(W_{-1}\)
   branch; \(W_0\) produces the extraneous zero-field solution.

4. X. Hernandez, R. A. Sussman, and L. Nasser, “Approaching the Dark Sector
   through a bounding curvature criterion,” arXiv:1705.06356; *MNRAS* **483**
   (2019) 147–151.
   [arXiv](https://arxiv.org/abs/1705.06356)

   Relevance: derives the deep-isothermal/MOND curvature combination with
   coefficient 28.  Therefore this bundle explicitly treats its own
   deep-MOND \(c^4K/\Omega^4=28\) as adjacent prior art, not a novelty claim.
   The paper does not give the full exponential transition, the two-frequency
   inverse, or simultaneous \((a_0,M)\) reconstruction.

5. D. Benisty, J. Wagner, and D. Staicova, “Dark Energy as a Critical Period
   in Binary Motion: Bounds from Multi-scale Binaries,” arXiv:2310.11488;
   *Astronomy & Astrophysics* **683** (2024) A83.
   [arXiv](https://arxiv.org/abs/2310.11488)

   Relevance: relates Kepler periods to Kretschmann curvature in a
   Schwarzschild–de Sitter setting.  This is adjacent to a period/curvature
   bridge but is neither MOND nor the two-clock exponential inverse derived
   here.

6. H. Zhao and L. Tian, “Roche Lobe Shapes for testing MOND-like Modified
   Gravity,” arXiv:astro-ph/0511754; *Astronomy & Astrophysics* **450** (2006),
   DOI 10.1051/0004-6361:20054379.
   [arXiv](https://arxiv.org/abs/astro-ph/0511754)

   Relevance: gives analytic inner-Lagrange-point and Roche-lobe laws for
   arbitrary MOND \(\mu\) and non-Keplerian host fields.  This source, together
   with the repository's existing `hunt_2026/h39_open_cluster_tails.py`, is why
   a superficially attractive exponential-MOND Hill/Jacobi specialization was
   rejected as the headline: it would be immediate prior-art specialization,
   not a comparably new formula.

7. S. R. Valluri, P. A. Wiegert, J. Drozd, and M. DaSilva, “A Study of the
   Orbits of the Logarithmic Potential for Galaxies,” arXiv:1209.1342;
   *MNRAS* **427** (2012), DOI 10.1111/j.1365-2966.2012.22071.x.
   [arXiv](https://arxiv.org/abs/1209.1342)

   Relevance: uses Lambert W for turning points and apsidal angles in a
   logarithmic galactic potential.  It confirms that Lambert W in orbital
   dynamics is prior art, but it does not invert an exponential-MOND epicycle
   ratio into \((a_0,M)\).

8. B. Monreal, X. Moskala, and S. Splawska, “An eccentric transit timing test
   of modified gravity,” arXiv:2410.01513 (2024).
   [arXiv](https://arxiv.org/abs/2410.01513)

   Relevance: proposes apsidal timing as a MOND test and derives an
   eccentricity-dependent precession for a two-body QUMOND force written as a
   Newtonian term plus a logarithmic perturbation.  This makes MOND apsidal
   tests and finite-eccentricity dependence clear prior art.  It does not give
   the exact-exponential AQUAL transition coefficient, the two-fundamental-
   frequency inverse, the guiding-radius correction, or the distance-, mass-,
   and clock-free cross-radius null derived here.

9. R. Castelli, “The monotonicity of the apsidal angle in power-law potential
   systems,” arXiv:1509.08662; *Journal of Mathematical Analysis and
   Applications* **428** (2015) 653–676.
   [arXiv](https://arxiv.org/abs/1509.08662)

   Relevance: proves eccentricity dependence of apsidal angles for a broad
   power-law class.  Thus neither finite-amplitude central-force mechanics nor
   eccentric apsidal shifts are claimed new.  The source does not state the
   exact-exponential MOND coefficient or the corrected multi-radius null.

## External queries run

The web/arXiv/ADS search used the following literal or close queries:

- `site:arxiv.org MOND epicyclic frequency acceleration scale Lambert W interpolation function exponential`
- `site:ui.adsabs.harvard.edu MOND epicyclic frequency infer a0 orbital frequencies`
- `site:arxiv.org MOND "epicyclic frequency" "a_0"`
- `MOND AQUAL epicyclic frequency rotation curve radial oscillations paper`
- `MOND epicyclic frequency formula kappa Omega logarithmic slope paper`
- `MOND acceleration scale measurement epicycle radial period galaxy orbit`
- `MOND exact exponential interpolation function 1-exp(-x) epicyclic`
- `"Lambert W" MOND "epicyclic"`
- `"LambertW" MOND orbit`
- `"kappa^2/Omega^2" MOND`
- `"radial epicyclic" MOND "acceleration scale"`
- `"Kretschmann" "epicyclic frequency" static spherical weak field`
- `"Ricci scalar" "epicyclic frequency" orbital frequency weak field`
- `"Kretschmann scalar" "orbital frequency" MOND`
- `"two-clock" gravity epicyclic orbital frequency curvature`
- `MOND finite eccentricity epicyclic frequency apsidal angle correction`
- `exponential interpolation MOND eccentric orbit apsidal precession`
- `MOND eccentricity radial azimuthal frequency ratio`
- `central potential Poincare Lindstedt apsidal frequency finite amplitude MOND`
- `MOND apsidal angle turning radii distance independent null`

No returned primary source stated the branch-correct formula

\[
y=-L-W_{-1}(-Le^{-L}),\qquad L={q-1\over3-q},
\]

as an inversion of exact-exponential MOND epicycle data, or the paired
one-radius estimators for \(a_0\) and \(M\).  Search engines can miss papers,
notation varies, and absence of a result is not a theorem.

## Repository search

The internal search covered `qwen_claude_field_theory/closure_2026`, the wider
`qwen_claude_field_theory`, `hunt_2026`, `real_research`, and `theory_2026`
for combinations of:

- `Lambert`, `W_-1`, and `LambertW`;
- `epicyclic`, `kappa`, `Omega`, and `two-clock`;
- inference or estimation of `a0` from orbital clocks;
- `Kretschmann`, `Ricci scalar`, `Jacobi`, `Hill radius`, and `Roche`.

The repository already contained the forward exact-exponential epicyclic law,
apsidal shifts, generalized circular Kepler law, finite-eccentricity period
integrals, EFD clock ratios, flyby scattering, and center-curvature
obstructions.  It did not contain the \(W_{-1}\) inverse spectrometer or the
two-clock curvature identities in the form derived here.  The closest
finite-e overlap is `../hpi_delta_eccentric_kepler_2026/`, which gives exact
turning-point quadratures and a deep-logarithmic law.  The forward all-orders
quadrature is therefore prior repository work and is not claimed as new here.
That bundle does not contain the transition-wide \({\cal C}_e(y)\), the
load-bearing azimuthal-clock term, the guiding-radius correction, the
branch-diagnosed inverse, or the exact detected-set cross-radius null.

## Novelty grade and claim boundary

Supported statement:

> The branch-resolved inverse spectrometer and paired \((a_0,M)\) estimators
> together with the exact-exponential small-e correction, branch-diagnosed
> all-orders inverse, and corrected branch-aware cross-radius null are new to
> this repository and were not found in a bounded primary-source search
> performed on 2026-09-04.  The exact all-orders forward quadrature is prior
> repository work.

Unsupported statements, which this bundle does not make:

- first discovery worldwide;
- new epicyclic mechanics;
- new finite-amplitude central-force or apsidal mechanics;
- new AQUAL action;
- new Lambert W mathematics;
- new deep-MOND coefficient 28;
- viable relativistic MOND theory;
- observational validation.
