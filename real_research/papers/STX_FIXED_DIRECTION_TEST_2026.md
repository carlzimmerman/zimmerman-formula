# A Fixed-Direction Ephemeris Test of s̄^TX at the CMB Apex: Pre-Registered Prediction, Analysis Recipe, and a Provisional Bound from Public Data

**Carl P. Zimmerman** · Briar Creek Tech · 2026-07-02

## Abstract

Planetary-ephemeris constraints on the boost sector of the gravitational Standard-Model Extension (SME) are limited not by data quality but by degeneracy: the standard analysis fits the components of s̄^{T J} jointly with free orientation, and the published marginal uncertainty on s̄^{TX} is ~8×10⁻⁹ with correlation coefficients near unity (Hees et al. 2015). A specific physical hypothesis removes the degeneracy. If the MOND acceleration scale reflects a preferred frame — the frame in which the cosmic microwave background is isotropic — then the induced boost vector is **fixed in direction at the CMB dipole apex**, (l,b) = (264.02°, 48.25°), i.e. (RA, Dec) = (167.94°, −6.94°) in the Sun-centered frame, with component ratios s̄^{TY}/s̄^{TX} = −0.214 and s̄^{TZ}/s̄^{TX} = +0.125 locked. The ephemeris test then collapses to a **one-parameter fit** for the amplitude A, with the de Sitter–Unruh modified-inertia framework predicting **|A| ≈ 8.7×10⁻¹⁰ with negative s̄^{TX}** — the same sign as the published central value. We supply (i) the pre-registered prediction and its kill condition; (ii) the concrete analysis recipe for an ephemeris group (one added acceleration term, one fitted parameter, no change to light-time modeling); (iii) a *provisional* fixed-direction bound from public secular perihelion/node-advance tables: **A = (−2.5 ± 5.9)×10⁻¹⁰** (INPOP10a set; (−0.9 ± 6.4)×10⁻¹⁰ with INPOP15a updates), i.e. the prediction sits at ~1.4σ with matching sign — neither detected nor excluded — while the fixed direction alone already sharpens the effective bound to |A| < 1.2×10⁻⁹ (95%), about twice better than the published marginal; and (iv) an honest scoping discovery: under a *per-body* reading of the underlying relation (s̄ ∝ a₀/2g per planet) the signal falls 30–1000× below current secular sensitivity, so planetary ephemerides test only the *universal* reading. A dedicated one-parameter fit on archival Mars and MESSENGER ranging reaches an idealized floor σ_A ≈ 4×10⁻¹¹, with realistic degradation σ_A ~ 1–4×10⁻¹⁰: **decidable either way with data already in hand.** The prediction and its kill condition were committed to a public repository before any dedicated fit exists; we accept the kill as written.

## 1. The degeneracy, and the hypothesis that removes it

The gravitational SME parametrizes leading Lorentz violation in the gravitational sector by a symmetric tensor s̄^{μν}; its boost components s̄^{TJ} enter planetary equations of motion through a velocity-coupled acceleration (Bailey & Kostelecký 2006). The most complete ephemeris analysis (Hees et al. 2015, INPOP10a secular advances) fits the SME components jointly and reports s̄^{TX} = (−2.9 ± 8.3)×10⁻⁹ — consistent with zero, with the large uncertainty driven by near-unit correlations among simultaneously-fitted components, not by ranging noise.

A preferred-frame hypothesis removes the orientation freedom. In a de Sitter–Unruh modified-inertia reading of MOND (Milgrom 1999; the present framework's realization with a₀ = c²√(Λ/32π) = 9.36×10⁻¹¹ m/s²), local dynamics carries an imprint of the frame in which the vacuum is isotropic — observationally, the CMB rest frame. The solar system moves through that frame at v = 369.82 km/s toward the dipole apex; the induced boost background is then

> s̄^{TJ} = A · n̂_J,  n̂ fixed at (RA, Dec) = (167.94°, −6.94°),  β = v/c = 1.234×10⁻³,

leaving a single amplitude A. The framework's estimate (committed as `reviews/stx_target.py`; reproduced independently to 1%) is **|A| ≈ 8.7×10⁻¹⁰, sign negative in s̄^{TX}**. We emphasize scope honestly: the *magnitude* carries the framework's O(1) modelling freedom; the *direction* and *CPT-even-only* structure are its sharp content, and the CPT-even prediction implies **exactly zero gravitational-wave birefringence** as an independent kill-switch.

## 2. A load-bearing fork: universal vs per-body reading

Carrying the derivation through the ephemeris observables exposed a fork that any test of this class must state. If the induced s̄ is **universal** (one background constant, reading U), planetary secular drifts scale as computed below and the test is sharp. If instead the relation is read **per-body** (s̄ ∝ a₀/2g evaluated at each planet's orbital gravity, reading P), the low-gravity outer planets dominate the naive formula but the *observable* drifts fall 30–1000× below current secular uncertainties (best case S/N ≈ 0.3–0.4 for Mars); no existing or near-term ranging tests reading P. **All ephemeris statements in this note therefore constrain reading U only**, and the framework's "in-hand test" claim is hereby scoped to that reading. We found no published statement of this fork; analyses to date implicitly assume U.

## 3. The recipe (what an ephemeris group runs)

1. Add to each planet's equation of motion the SME pure-gravity boost term (Bailey & Kostelecký 2006; Hees et al. 2015, Eq. 3): δa⃗ = (2GM_⊙/c r³)[(s⃗·v⃗) r⃗ − (r⃗·v⃗) s⃗], with s⃗ = A·n̂ and n̂ **fixed** as above (component ratios locked; s̄^{TT} unobservable here; s̄^{jk} = 0).
2. No modification to light-time/Shapiro modeling (boost components are negligible in propagation at this sensitivity).
3. Fit the single parameter A jointly with the standard ephemeris set (initial conditions, GM_⊙, asteroid ring). The fixed direction is the entire leverage: it converts an 8-parameter, 0.99-correlated problem into a one-parameter fit ~100× tighter.
4. Report both variants: (U) universal A; (P) per-body A·(g_Saturn/g_planet) — the latter as the framework's own-reading control, expected unconstrained.
5. Detection signature: A < 0 (n_X < 0), amplitude ~8.7×10⁻¹⁰, direction consistent with the apex. Kill: |A| < 2σ with σ_A ≤ 4.3×10⁻¹⁰ excludes the prediction at ≥2σ; the idealized (white-noise) combined floor from archival MESSENGER + Mars ranging is σ_A ≈ 4.3×10⁻¹¹, at which a null excludes it at ~20σ.

Sensitivity is Mars-dominated (MGS/MEX/MRO ranging; idealized per-dataset S/N at the prediction: Mars 21–40, Mercury/MESSENGER 1.3–4.4, Venus ~1.3, Saturn/Cassini 0.6–1.0, Jupiter/Juno ≲0.1). These are white-noise upper estimates; realistic systematics (asteroid modeling above all) degrade them by a few ×.

## 4. A provisional bound from public data

No machine-readable normal-point archive is publicly downloadable at present (the INPOP APDB service and the published Cassini normal points were not retrievable at run time), but the published **secular perihelion and node advances** (Hees et al. 2015, Table I; INPOP15a updates from Fienga et al. 2016) permit the fixed-direction fit directly. Fitting the single amplitude A to the ten secular observables (Earth–Moon barycenter excluded on ω-definition grounds; Venus carries a 1/e enhancement making it competitive despite weaker ranging):

> **A = (−2.5 ± 5.9)×10⁻¹⁰** (INPOP10a set) · **A = (−0.9 ± 6.4)×10⁻¹⁰** (INPOP15a-updated set)
> 95% bound |A| < 1.2×10⁻⁹ · prediction −8.7×10⁻¹⁰ sits at **1.4σ (1.2σ)** with **matching sign**.

Direction-fixing alone thus already improves on the published marginal s̄^{TX} bound by roughly an order of magnitude (and on the combined-analysis bound ~2×) using nothing but public tables. We state plainly what this is not: it is not a detection (1.4σ), the sign agreement with the published central value is at present a coincidence-level observation, and the secular-table fit inherits whatever systematics the underlying ephemeris solutions carry. It is a floor-demonstration: the dedicated fit of §3 on archival ranging decides the question.

## 5. Scope, credit, and the pre-registration clause

The SME formalism and the ephemeris methodology are Bailey & Kostelecký (2006) and Hees et al. (2015); the Planck dipole fixes the apex; the framework supplies only the *hypothesis* that fixes the direction and the target amplitude, and it is a one-parameter reframing of the MOND scale whose earlier over-claims were publicly retracted (2026-06-23) and are not reasserted. The prediction, recipe, fork-scoping, and kill condition above were committed to the public repository (github.com/carlzimmerman/zimmerman-formula, `PREREGISTERED_EMPIRICAL_FLEET_2026-07.md`) before any dedicated ephemeris fit has been performed. If the dedicated fit returns a null at the stated sensitivity, this realization's sharpest prediction is dead, and we will say so in those words.

## References
- Q. G. Bailey & V. A. Kostelecký, *Signals for Lorentz violation in post-Newtonian gravity*, Phys. Rev. D 74 (2006) 045001 (gr-qc/0603030).
- A. Hees et al., *Testing Lorentz symmetry with planetary orbital dynamics*, Phys. Rev. D 92 (2015) 064049 (arXiv:1508.03478).
- A. Fienga et al., *Constraints on SME coefficients from INPOP planetary ephemerides* (2016) (arXiv:1601.00947).
- A. Hees et al., *Tests of Lorentz symmetry in the gravitational sector*, Universe 2 (2016) 30 (arXiv:1610.04682).
- M. Milgrom, *The Modified Dynamics as a Vacuum Effect*, Phys. Lett. A 253 (1999) 273 (astro-ph/9805346).
- Planck Collaboration, dipole v = 369.82 km/s toward (l,b) = (264.02°, 48.25°).

*Reproducible: `reviews/stx_target.py`, `reviews/stx_inpop_recipe.py` (both committed, exit 0). Companion pre-registration: `PREREGISTERED_EMPIRICAL_FLEET_2026-07.md`. Prediction DOI lineage: 10.5281/zenodo.20978308.*
