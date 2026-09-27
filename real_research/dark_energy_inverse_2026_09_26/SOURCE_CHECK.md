# Source check — inverse dark-energy interpretation, 2026-09-26

Scope: primary-source checks for background identifiability and the currency
of cosmological interpretation. This is not a comprehensive literature or
novelty review, and no external likelihood was fitted in CD26-3. The specific
versions below were read through web retrieval; no complete authenticated
PDF cache or source-file hash is claimed.

## Background inverse degeneracy

Martin Kunz, *The dark degeneracy: On the number and nature of dark
components*, [astro-ph/0702615v2](https://arxiv.org/abs/astro-ph/0702615v2),
27 February 2007. Inspected the abstract and PDF pp. 1–2, especially Eqs. (3)
and (4). The flat-background inverse for `w(z)` depends on the chosen matter
normalization; shifting the conserved dust split can leave the same expansion.
This supports the limited background nonuniqueness used here. It does not
justify declaring all constitutive models observationally equivalent, or
discarding perturbation and non-gravitational information.

Translation: Kunz uses the usual energy-density equation of state. Our
`epsilon` is energy per volume, `Pi=-p`, and constant-pressure continuity
gives `epsilon=Pi+D a^-3`. Our derivation is supplied in full in
`reconstruction/RESULT.md`; the existence of this broad degeneracy is not
claimed as new. Its pressure-scale null-test application is a proposed
repository calculation, with no global novelty claim.

## Observational currency and interpretation

DESI Collaboration, *DESI DR2 Results II: Measurements of Baryon Acoustic
Oscillations and Cosmological Constraints*,
[2503.14738v3](https://arxiv.org/abs/2503.14738v3), 9 October 2025;
Physical Review D 112, 083515. Abstract inspected. BAO alone are well described
by flat LambdaCDM; the reported preference for evolving dark energy depends
on the combined data and model. It is not a direct measurement of a clock
pressure or proof of the repository's pressure-promotion postulate.

DESI Collaboration, *DESI DR2 Results IV: Alcock-Paczyński Measurements
from the Ly-alpha Forest and Cosmological Constraints*,
[2607.27410v3](https://arxiv.org/abs/2607.27410v3), 4 August 2026. Abstract
inspected, reached through the [official DR2 paper index](https://data.desi.lbl.gov/doc/papers/dr2/).
It adds the Ly-alpha Alcock-Paczyński measurement at `z=2.33` and reports
model/data-dependent evolving-dark-energy preferences. Therefore the
repository's 2025 CPL example points cannot be presented as a complete
September 2026 likelihood. No new posterior or significance is inferred here.

A direct test of the proposed pressure relation needs the expansion
likelihood and its derivative covariance, the sound-horizon calibration
where relevant, and independent galaxy-scale likelihoods. Published
cosmological parameter posteriors conditional on a different action cannot
be imported as proof against or for this action without reanalysis.

## Detector-temperature scope

S. Deser and O. Levin, *Accelerated Detectors and Temperature in (Anti) de
Sitter Spaces*, [gr-qc/9706018v1](https://arxiv.org/abs/gr-qc/9706018v1),
6 June 1997. Abstract and PDF pp. 1–3, especially Eq. (8), inspected.
For the specified constant-acceleration de Sitter detector, the temperature
contains the quadrature of acceleration and inverse curvature radius.
Restoring SI units gives `T=hbar sqrt(a_detector²+(cH_vac)²)/(2 pi c k_B)`.
The discussion uses an appropriate quantum-field state and detector response;
it supplies no MOND constitutive law. Equating separate Unruh and de Sitter
temperatures cancels their common `2 pi`, as the scale audit checks.

G. W. Gibbons and S. W. Hawking, *Cosmological event horizons, thermodynamics,
and particle creation*, [Phys. Rev. D 15, 2738 (1977)](https://journals.aps.org/prd/abstract/10.1103/PhysRevD.15.2738).
Publisher abstract inspected for the historical cosmological-detector
interpretation only. No complete derivation was audited. Neither source
establishes that the present gravity action's clock obeys this thermometry.

## Local provenance that limits interpretation

- `nbody_2026/stage17_a0z_from_the_action_2026.py`: pressure promotion and the
  selected DBI parameter relation are construction inputs; their consequences
  must be distinguished from a derivation of the coefficient.
- `fable_independent_2026/L273_desi_a0z_band.py`: prior forward distinction
  between pressure and density promotions; acknowledged, not rediscovered.
- `kappa_closure/README.md`: existing free-coupling and vacuum-counterterm
  obstructions. An algebraic inverse does not remove them.
- `real_research/FRAMEWORK.md`: contains an older total-Hubble scaling branch.
  It must not be silently identified with the current vacuum/pressure branch.

Only these source-dependent implications were checked. Full paper proofs,
complete current observational coverage, and novelty remain outside this pass.
