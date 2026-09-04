# Literature and novelty scope

Search date: 2026-09-04.

## Primary foundations and close antecedents checked

- Bekenstein & Milgrom, *Does the missing mass problem signal the breakdown of
  Newtonian gravity?*, ApJ 286 (1984), DOI
  <https://doi.org/10.1086/162570>, scan
  <https://adsabs.harvard.edu/pdf/1984ApJ...286....7B>.  This is the AQUAL
  action foundation; neither that action nor its external-field effect is new
  here.
- Milgrom, *Solutions for the modified Newtonian dynamics field equation*,
  ApJ 302 (1986), DOI <https://doi.org/10.1086/164021>, scan
  <https://adsabs.harvard.edu/pdf/1986ApJ...302..617M>.  This establishes
  analytic solutions and asymptotics of the nonlinear AQUAL equation,
  including external-field structure.
- Banik & Zhao, *The External Field Dominated Solution In QUMOND & AQUAL:
  Application To Tidal Streams*, MNRAS 459 (2016),
  <https://arxiv.org/abs/1509.08457>, DOI
  <https://doi.org/10.1093/mnras/stw787>.  It states the EFD AQUAL point-mass
  potential and its nonradial force, including an under-20-degree directional
  bound.  That potential is the direct starting point of this bundle.
- Zhao & Famaey, *Refining MOND interpolating function and TeVeS Lagrangian*,
  ApJ 638 (2006), <https://arxiv.org/abs/astro-ph/0512425>, DOI
  <https://doi.org/10.1086/500805>.  It discusses the empirical interpolation
  function \(\widetilde\mu(x)=1-e^{-x}\); it is not asserted to be the source
  of the particular primitive used in this repository.
- Maciejewski, Przybylska & Szumiński, *Anisotropic Kepler and anisotropic two
  fixed centres problems*, Celestial Mechanics and Dynamical Astronomy 127
  (2017), DOI <https://doi.org/10.1007/s10569-016-9722-z>.  This is a close
  mathematical antecedent for the spatial axisymmetric anisotropic-Kepler
  Hamiltonian and its invariant subsystems.
- Li & Liu, *Periodic orbits of the spatial anisotropic Kepler problem with
  anisotropic perturbations*, EJDE 2021, Paper 63,
  <https://ejde.math.txstate.edu/Volumes/2021/63/li.pdf>.  This further limits
  any broad novelty claim about the orbit mechanics.

The exactly invariant plane is ordinary attractive Kepler motion after the
coefficient replacement \(GM\mapsto k_e=GM/(\mu_e\sqrt q)\).  Its conics,
period, hyperbolic deflection, and Rutherford cross-section are classical
once that reduction is recognized.  They are recorded here to prevent the
generic Born result from being overextended, not as new Kepler mathematics.

## Repository scope checked

Targeted text searches covered `flyby`, `impulse`, `scattering`, `Rutherford`,
`external-field dominated`, `anisotropic Green`, `sqrt(q)`, the EFD point
potential, and the principal force axes.  Commit-history searches also looked
for the flyby formula and its Schur-complement structure.

Important overlaps found:

- `qwen_claude_field_theory/closure_2026/exact_exponential_aqual_efe_kepler_2026/`
  already derives the same exponential-AQUAL EFD operator and Green potential,
  the equatorial circular Kepler coefficient, a finite-eccentricity nodal law,
  and uniform-core clocks.  The circular anchor is not new in this bundle.
- `real_research/reviews/mi_route_a_mi_vs_mg_separation_2026.py` already
  contains the static point-field AQUAL principal-axis `sqrt(q)` force ratio.
  A static force-axis ratio is not the integrated flyby impulse tensor.
- Other EFE files contain angular force, mass, morphology, or phenomenological
  prescriptions, but the search found no prior repository implementation of
  the coordinate-free impulse

  \[
  -{2C\over v_\infty\sqrt a\,D}
  \left(A-{(A\mathbf n)(A\mathbf n)^T\over a}\right)\mathbf b,
  \]

  its generic impact-azimuth factor, or its scattering-map Jacobian.

A failed repository search is evidence only about the indexed live tree and
history; it is not proof of global priority.

## Defensible novelty wording

The wording supported by the present search is:

> The full three-dimensional first-Born impulse tensor, its transversality,
> generic-azimuth bounds, misalignment bound, and anisotropic small-angle
> cross-section are repository-new formal observable corollaries of the known
> EFD AQUAL Green function.  The EFD potential, static force anisotropy,
> principal-axis `sqrt(q)` ratio, and equatorial Kepler reduction are prior
> structures.  No global novelty claim is made.

The search was not exhaustive over paywalled full text, citation graphs,
conference proceedings, theses, non-English literature, or every mechanics
paper using a line-integrated anisotropic Coulomb field.  A global novelty
claim would require a dedicated systematic review beyond this bundle.
