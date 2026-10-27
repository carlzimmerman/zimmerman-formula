# Author audit of the source, transport and restoration claims

Primary verdict: **computationally verified only in the stated range**.
The original nonlinear formation implication is incomplete. Review provenance:
author self-review, not an independent agent or peer review. Authoritative
locators are RADIATION_TRANSPORT_DERIVATION.md, TRANSPORT_COUPLING.md and the
hash-pinned scripts/results listed in MANIFEST_AUDIT.json.

## Claim card and restrictions

The finite claim is: the unchanged full radial CC system, on the specified
grids and inherited coefficients, continues from zero-wave internally quiet
mixed infall to 12.8825 Myr with real outgoing radiation, very small inward
50-kpc mass repair, a populated but nonmonotonic transition, effectively F
exterior, and a positive local moving-boundary response for the tested family.
The early finite perturbations return/overshoot over 0.5 Myr under time-ceiling
refinement. No other initial conditions, angular modes, long-time stability or
<1% law result is included.

The structural finite-dimensional lemma assumes real positive coherent initial
species amplitudes, chi=0 and positive transport weights B on the retained
edges. Its conclusion is the exact B-orthogonal decomposition into the source
functional's bright direction and kernel. The numerical projection toward an
energy-derived reference is diagnostic, not a prescribed density history.

## Dependency graph and obligations

| Implication / leaf | Type | Audit status |
|---|---|---|
| Hamiltonian -> continuous full field, including all density/carrier/current derivatives | Internal differentiation plus independent energy differences | Passed at two structured finite directions/states; not exhaustive symbolic certification |
| Material field -> total-mass current and source-charge identity | Internal telescoping algebra plus numerical checks | Passed; conversion cancels from total mass |
| Actual source history -> outgoing field | Internal radial retarded Green derivation plus independent packet prediction | Passed to 0.3085% final waveform L2 error |
| Characteristics -> radiating versus reactive energy | Inherited discrete identity and analytic calibration | Passed within recorded finite precision |
| Common-phase velocity -> kinetic metric B and source L | Direct expansion of original positive edge square | Passed; source derivative agrees to 5.03e-13 |
| B and L -> orthogonal bright/kernel split | Finite linear algebra | Passed; L(v_dark)=0 and orthogonality checked |
| Continuum harmonic retardation -> sinc form factor | Internal integration of radial Green function | Passed; code uses point-cell quadrature, not exact finite-grid resolvent |
| Small projection -> permanent dynamically dark subspace | Unchecked physical implication | Not established and explicitly not claimed |
| Perturbed full field -> moving-boundary Rddot | Chain rule plus three derivative scales | Passed for tested charge-safe perturbation family |
| Local Rddot and half-Myr return -> global/asymptotic restoration | Unchecked implication | Not established and explicitly not claimed |
| Emission plus restoration -> enough inward mass and galaxy law | Original target implication | Fails in the tested interval; law error remains 17.361245% |

There are no external theorem leaves or novelty claims in these derivations.
The inherited phenomenological constitutive choices and coefficient g2 remain
model assumptions, not derived fundamental physics.

## Adversarial checks

* Recomputed the retarded Green sign and 1/(2c) factor using an odd extension
  of u=r chi. The outgoing characteristic power is c u_tau^2. Ordinary physical
  finite-radius flux has an additional reactive derivative; it is not used as
  the radiation definition.
* Rechecked time units: d/dtau=t_dyn d/dt_Myr. The initial charge-history unit
  error is frozen in the first run and corrected in the checked evidence.
* Reconstructed kinetic normalization from sigma^2=kappa and the exact edge
  cosine expansion. The source functional follows by telescoping the actual
  bulk contributions, not by assuming a fitted luminosity.
* Reversed the boundary perturbation sign, halved its displacement, and changed
  derivative scale. Global charge and every initial total cell mass remain
  fixed; the scalar fields and material phases receive no packet.
* Distinguished the bright kinetic fraction, its share of a mass current, and
  actual outgoing/field-work efficiency. They are different quantities.
* Checked nine diagnostic cutoff/floor combinations. These support robustness
  of the stated projection but do not establish continuum or nonlinear results.
* Checked the scalar grid's wave-frequency ceiling. Lack of fast exterior
  radiation cannot be promoted to a physical no-go above that ceiling.
* Checked actual run endpoints and adaptive behavior. A process-completed
  bounded run can contain a wall-limited physical partial trajectory. One-step
  qualification did not become a production numerical improvement.

## Exact remaining implication

A source kernel can rotate under nonlinear evolution. A sufficient joint
formation argument would need quantitative mixing/observability of the broad
redistribution modes, enough outward energy flux to approach the relevant
mass/charge-constrained restoring branch, and control of density troughs and
exterior conversion on that timescale. None follows from the instantaneous
projection. This is the smallest unresolved mechanism identified here; it is
preserved as open rather than asserted impossible or solved.

## Mathematical proofreading scope

Self-reviewed only the new derivation/result/handoff files. Routine changes:
units, scope and terminology clarified. Mathematical restriction added: the
harmonic continuum form factor is evaluated numerically by point-cell
quadrature, not an exact finite-grid propagator. The time-derivative unit factor
was corrected in a new checked script/run; no frozen evidence was overwritten.
No unrelated manuscript or historical file was edited.
