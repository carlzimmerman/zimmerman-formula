# Recent data and a sharper theoretical route

October 8, 2026.

The next target should be a **covariant cosmology-to-galaxy response relation**: derive which cosmological quantity controls the local acceleration scale, then test its evolution. Another static reconstruction of the same galaxy law would not answer that question. None of the inspected OpenAI results supplies the missing \(32\pi^2\) normalization or a theory of everything.

This review supplies a reproducible conditional prediction and two theoretical exclusions with explicit assumptions. It does not fit new data. The newest combined supernova likelihood is not yet publicly released according to its current preprint.

## New observations and availability

| Primary source and date | What changed | Consequence |
|---|---|---|
| [DESI Lyman alpha AP, July 29, revised August 4](https://arxiv.org/abs/2607.27410v3) | AP precision is 1% at \(z=2.33\). Joint AP and BAO give \(D_H/r_d=8.600\pm0.066\), \(D_M/r_d=39.32\pm0.33\). Updated combinations prefer evolving dark energy at 2.7 or 3.2 sigma, depending on included data. | Include this high-redshift anchor. The central shift moves toward the cosmological-constant model; do not select only observations favoring evolution. These measurements overlap earlier DESI products. |
| [Supernovae Unite, September 4, revised September 9](https://arxiv.org/abs/2609.05053v2) | Combines 2,884 likely SNe Ia. Its combined flat-CPL analysis reports central values \(w_0=-0.861,\ w_a=-0.60,\ \Omega_m=0.305\). The current version reports weak Bayesian preference for evolving dark energy and 3.3/3.1 sigma using MAP/maximum likelihood. | A useful new benchmark. The Hubble diagram and likelihood are promised upon acceptance: no independent Unite fit is performed here. Do not recombine it with constituent SN samples. |
| [Unite host masses, September 9 revision](https://arxiv.org/abs/2609.05321v2) | Reassesses host-galaxy masses and cosmology systematics. Host photometry is also awaiting acceptance. | Calibration matters; an equation-of-state central value is not proof of a new field. |
| [DES Y6 papers](https://www.darkenergysurvey.org/des-y6-cosmology-results-papers/), January and May | Lensing/clustering and later multiprobe dark-energy analysis. The [May combined analysis](https://arxiv.org/abs/2605.27221v2) gives central \(w_0=-0.82,\ w_a=-0.63\). | Essential for a relativistic theory's growth and lensing predictions. May DES and September Unite are overlapping analyses, not independent confirmations. |
| [DES Dovekie products](https://github.com/des-science/DES-SN5YR) | Updated calibration, simulations and cosmology products publicly supplied. | A usable SN starting point while Unite remains unavailable; preserve the covariance and calibration choices. |
| [Euclid official timeline](https://euclid.caltech.edu/page/data-release-timeline) | Q2 released June 24. DR1 Foundation scheduled November 12, 2026; Complete mid-2027. | Corrects the assumed October release. Q2 availability does not establish that it supplies a ready cosmology likelihood for this test. |
| [DESI release documentation](https://data.desi.lbl.gov/doc/releases/) | DR1 is the latest listed full public spectroscopic release; paper-associated DR2 cosmology products are separate. | A DR2 analysis is not a public release of every DR2 spectrum. |

The bounded search covered official OpenAI research and linked papers, DESI releases, DES Y6, Euclid's timeline, recent supernova papers, and searches for October cosmology/RAR releases. It did not establish a new October galaxy-acceleration dataset. Retrieved Gaia results were stale and do not establish a released DR4. A recent reanalysis of old galaxies is not new observational data.

## A coefficient-independent prediction

The original statement
\[
a_0=k\,c\sqrt{G\rho_\Lambda},\qquad k=\frac12
\]
uses a cosmological constant and gives constant \(a_0\). Replacing \(\rho_\Lambda\) with evolving dark energy is a **new hypothesis**, ultimately requiring an action.

Under that extension, assume positive separately conserved dark-energy mass density, constant \(G,c,k\), and an adiabatic local galaxy response:
\[
a_0(a)=k\,c\sqrt{G\rho_{\rm DE}(a)},\qquad
\frac{d\ln\rho_{\rm DE}}{d\ln a}=-3(1+w).
\]
Then
\[
\boxed{\frac{d\ln a_0}{d\ln a}=-\frac32(1+w(a)).}
\]
For \(w(a)=w_0+w_a(1-a)\),
\[
\boxed{\frac{a_0(z)}{a_0(0)}
=(1+z)^{\frac32(1+w_0+w_a)}
\exp\!\left[-\frac{3w_a z}{2(1+z)}\right].}
\]
For \(w_a\ne0\), an interior stationary point lies at
\[
a_*=1+\frac{1+w_0}{w_a},\qquad z_*=a_*^{-1}-1,
\]
when \(0<a_*<1\). It occurs where \(w=-1\), and is a maximum for the two central examples tested.

The September Unite central values give \(z_*=0.301518\), maximum ratio \(1.026616\). This is an illustration conditional on that reported background, not a measurement or posterior prediction.

| Redshift | Constant vacuum scale | Density-tracking scale | Hubble-tracking scale |
|---:|---:|---:|---:|
| 0.3 | 1 | 1.02662 | 1.18430 |
| 0.5 | 1 | 1.01981 | 1.32370 |
| 1 | 1 | 0.97111 | 1.75938 |
| 2 | 1 | 0.85241 | 2.95635 |

All ratios are normalized to today. The Hubble column uses the same flat CPL background, \(\Omega_m=0.305\), neglecting radiation:
\[
H^2/H_0^2=\Omega_m(1+z)^3+
(1-\Omega_m)[a_0(z)/a_0(0)]_{\rm density}^2.
\]
This isolates which quantity the acceleration tracks instead of changing the background between columns. These are competing physical bridges, not equivalent formulas.

At fixed baryonic mass, \(v_f^4=GM_ba_0\) translates the density-tracking example into only a \(+0.66\%\) speed change near its peak and \(-3.91\%\) at \(z=2\). Inclination, pressure support, mass calibration, environment and evolution must be controlled. Neither clean asymptotic velocities nor fixed masses are automatically available for high-redshift galaxies. The Hubble-tracking alternative is much more widely separated.

If \(\dot\rho+3H(1+w)\rho=Q\), the slope identity gains \(Q/(2H\rho)\). Varying \(k,G,c\) adds their logarithmic derivatives; response delay changes the local-to-background map. These are ingredients to derive, not parameters to introduce after disagreement.

## Two filters on proposed mechanisms

### A conformal vector vacuum cannot simply supply the response

For a \(d\)-dimensional CFT, let a constant relevant source \(J\) couple linearly to a physical primary operator of dimension \(\Delta\). If this deformation supplies the only scale and ordinary hyperscaling applies to the singular free-energy density,
\[
f_{\rm sing}(J)\propto |J|^p,\qquad p=\frac d{d-\Delta}.
\]
This assumes a well-defined homogeneous response, with no other scale or dangerously irrelevant coupling. It is not a statement about every nonlinear effective action.

A spin-one primary in a unitary CFT obeys \(\Delta\ge d-1\), from positivity of descendant norms: [Simmons-Duffin, section 7.3, equations 129–134](https://arxiv.org/pdf/1602.07982). Thus a relevant vector source has \(p\ge d\).

| Required power | Required dimension in \(d=4\) | Vector bound \(\Delta\ge3\) |
|---:|---:|---|
| \(3\) | \(8/3\) | Fails |
| \(3/2\) | \(4/3\) | Fails |

This excludes directly identifying our source with a spin-one primary of a four-dimensional Lorentz-invariant conformal vacuum, with no extra scale, and claiming it produces the required cubic or three-halves response. It does not exclude a finite-density state, scalar source, curvature scale, nonrelativistic fixed point or different operator map.

In \(d=3\), cubic response saturates the conserved-current bound; it does not prove a nonzero spatial-source response. A constant source for an ordinary conserved current can be locally pure gauge in flat simply connected space. Boundaries, holonomies and chemical potentials require separate analysis.

The existing preferred-frame spinor model has not satisfied these CFT hypotheses; its dimensionful \(a_0\) also prevents casual application of the one-scale assumption. OpenAI's scale-to-conformal paper motivates the check but is not a load-bearing theorem here: conformality is an explicit assumption and the bound is independently sourced.

### A healthy minimal scalar cannot implement the illustrated crossing

For a minimally coupled scalar \(P(\phi,X)\), signature \((-+++)\), \(X=-\partial_\mu\phi\partial^\mu\phi/2>0\) on a homogeneous rolling background,
\[
\epsilon=2XP_X-P,\quad p=P,\quad \epsilon+p=2XP_X.
\]
The high-frequency time and gradient coefficients are
\[
K_t=P_X+2XP_{XX},\qquad K_s=P_X.
\]
Strict absence of ghosts and gradient instability requires both positive. For positive \(\epsilon\), this implies \(w>-1\). This healthy minimal class cannot reproduce the illustrated crossing. Vanishing coefficients require separate analysis and do not satisfy strict stability.

This is a known obstruction, not a claimed new theorem; compare [Vikman](https://arxiv.org/abs/astro-ph/0407107v4). [Kinetic gravity braiding](https://arxiv.org/abs/1008.0048v2) supplies established ways scalar-metric mixing can evade it. Those examples do not automatically supply MOND, acceptable lensing or the normalization. An effective \(w\) inferred assuming GR also need not be a fundamental fluid equation of state in modified gravity.

## The selected next theoretical route

Investigate a covariant medium whose cosmological state determines its local gravitational susceptibility. A concrete first class to screen is a scalar-tensor action with constant Planck mass,
\[
S=\int d^4x\sqrt{-g}\left[\frac{M_{\rm Pl}^2}{2}R+
K(\phi,X)-G_3(\phi,X)\Box\phi\right]+S_m[g,\psi].
\]
This is an existing theory class, not a completed Zimmerman theory. Two arbitrary functions would make reconstruction too easy to count as a derivation. Specify a small fixed family and its symmetries before matching either regime.

The decisive deliverable is **one action with two derived limits**:

1. Derive homogeneous evolution and the perturbation kinetic matrix, retaining scalar-metric mixing.
2. Derive the same action's galaxy equation and the force measured by baryons. Determine whether it gives the deep response and full P2 law instead of imposing an unrelated constitutive relation.
3. Derive whether \(a_0\) is constant, density-tracking or Hubble-tracking, including screening and relaxation.
4. Derive both metric potentials and growth/lensing observables. A force law alone cannot be compared to DES as a complete relativistic model.
5. Determine whether a symmetry or quantization condition fixes \(k\). If it remains continuously adjustable while the other properties hold, the coefficient puzzle is unsolved.

If the finite candidate family fails, record the failure rather than adding an unrestricted function per observable. Ordinary braiding need not generate the required galaxy response at all; that is the first substantive existence test, not an assumed result.

With the comparison-area definitions used in this project,
\[
A=\frac{\pi c^4}{a_0^2},\qquad
\Lambda=\frac{8\pi G\rho_\Lambda}{c^2}
\quad\Longrightarrow\quad
A\Lambda=\frac{8\pi^2}{k^2}.
\]
The desired number follows if \(k=1/2\); it does not select \(k\). The redshift test cancels this coefficient and can reject a proposed bridge while normalization remains open. For evolving dark energy, \(8\pi G\rho_{\rm DE}/c^2\) is not a constant cosmological constant.

## Review of OpenAI releases

The review covers the publicly located releases below and the October catalogue pinned to commit fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb. All 372 families are indexed in catalogue_screen.json. The release reports 719 manuscripts. The 25 mathematical-physics and 16 PDE family summaries were inspected; seven primary manuscript statements received closer reading. Other entries are indexed or title-screened as explicitly recorded. This is not independent verification of hundreds of proofs. No Lean builds were run.

| Release | Relevant scope | What transfers |
|---|---|---|
| [Formal mathematics, 2022](https://openai.com/index/formal-math/) | Theorem-proving methods and benchmarks. | Machine-check precise lemmas after fixing definitions. Formal correctness does not establish empirical interpretation. |
| [Early science experiments, 2025](https://cdn.openai.com/pdf/4a25f921-e4e0-479a-9b38-5367b47e8fd0/early-science-acceleration-experiments-with-gpt-5.pdf) and [Scientific collaborator, January 2026](https://cdn.openai.com/pdf/f4b4a5da-b2de-418d-9fcd-6b293e9dc157/oai_ai-as-a-scientific-collaborator_jan-2026.pdf) | Research case studies across disciplines. | Methods for proposing and checking conjectures; capability demonstrations do not define a physical model. |
| [Single-minus gluons, February 13](https://arxiv.org/abs/2602.12176) | Tree amplitudes in special half-collinear kinematics. | Recursion, factorization and limit checks once a relativistic action exists. Not a galaxy-response calculation. |
| [First Proof, February 20](https://openai.com/index/first-proof-submissions/) | Ten attempts with varying correctness; attempt 2 subsequently recognized as incorrect. | Independent review and corrected dependencies matter. |
| [Single-minus gravitons, March 4](https://cdn.openai.com/pdf/graviton.pdf) | Distributional half-collinear amplitudes, notably in split signature; matrix-tree methods and recursion. | Future scattering-consistency benchmark. Does not fix cosmological background, particle spectrum or \(a_0\). |
| [Unit distances, May 20](https://cdn.openai.com/pdf/74c24085-19b0-4534-9c90-465b8e29ad73/unit-distance-proof.pdf) | Number-theoretic counterconstruction to a geometric conjecture. | Seek countermodels to uniqueness claims. No established map from these point sets to vacuum energy. |
| [Ten advances, August 1](https://openai.com/index/ten-advances-in-mathematics/) | Geometry/codes, groups/operator algebras, complexity, quantum games, lattice hardness and combinatorics; formalizations supplied. | Bounds and certificates are methods, not a derivation of spacetime or the Standard Model. |
| [Navier–Stokes and Euler, September 8](https://openai.com/index/navier-stokes-solution/) | Claimed forced NS blowup from rest with finite energy; separate unforced Euler result; NS formalization supplied. | Finite energy alone cannot establish global regularity of our equations. The forcing and PDE hypotheses must not be dropped. |
| [Mathematics catalogue, October 6](https://openai.com/index/sharing-ai-progress-in-mathematics/) | Large collection with varied verification status. | Check theorem hypotheses, version and the map to our equations before use. |

The [October 7 history](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/history.md) records three withdrawals after a sign error affected a construction and dependent papers, plus repairs and citation updates. It reports 300/719 top-line results formalized. That is repository-reported status, not a certificate check by this review.

### Closest October candidates

The seven selected primary PDF URLs and hashes are recorded in selected_source_records.json. Source copies are retained in the ignored local research cache.

| Family | Statement scope inspected | Missing connection |
|---|---|---|
| 270, BFSS | Unique normalizable zero-energy state claimed for each finite relative SU(N), \(N\ge2\); continuum starts at zero. | Closest to quantum-gravity foundations, but not a mass gap, positive 4D vacuum density, realistic compactification or derivation of \(k\). |
| 282, scale/conformal | Unitary positive-energy 4D theory with specified spectrum, local-net realization and scale-current hypotheses; local Ward-identity conclusion. | Prompts the conditional dimension filter. Does not apply automatically to the preferred-frame medium; global net action remains separate. |
| 267, BEC | Positive-temperature dilute 3D hard-sphere canonical gas, with specified density and thermodynamic limits. | Condensation alone selects neither gravitational coupling nor vacuum normalization. |
| 260, Penrose | Selected PDF: charged asymptotically flat initial data, enclosing-area bound and conditional rigidity. | ADM mass is not de Sitter vacuum energy; the area bound cannot be substituted for the desired coefficient. |
| 362, Vlasov–Maxwell | Smooth one-species relativistic electromagnetic kinetic system with specified support and field conditions. | Attractive gravity and our response equations are different systems; no halo-formation theorem follows. |
| 365, inverse boundary | Smooth metric and rank-two unitary connection from a partial-boundary response operator, modulo specified equivalences. | One galaxy profile is not the full boundary operator. |
| 371, defocusing NLS | Stable high-power supercritical blowup on the twelve-dimensional torus. | Positive energy need not control regularity; no direct blowup conclusion for our 3D model. |

Kerr censorship, Einstein four-manifolds, critical statistical models, entropy inequalities and operator algebras are adjacent topics. Return to them when an explicit physical dictionary exists. A topological invariant does not by itself set an absolute curvature or measured response scale.

## Verification and remaining gap

bridge_checks.py passed 34 checks: symbolic continuity/normalization identities, independent continuity quadrature for three backgrounds at seven redshifts, extrema, and algebra supporting the filters. Deliberately reversing the CPL exponential sign failed 14 checks. Substituting \(k=1/3\) for \(1/2\) failed the normalization check. Both expected failed controls are preserved.

The displayed derivations establish conditional identities; finite checks support their implementation. No posterior covariance was used, and central parameter values are not assumed jointly most probable. No confidence interval is assigned to the turnover. External OpenAI proofs have not been independently verified.

The concrete result is a discriminator between three cosmological bridges and two restrictions on possible mechanisms. The outstanding deliverable is a covariant action with both limits derived. Normalization, relativistic phenomenology, quantum completion and Standard Model content remain open. The present evidence does not establish a TOE or justify calling its completion the final mile.
