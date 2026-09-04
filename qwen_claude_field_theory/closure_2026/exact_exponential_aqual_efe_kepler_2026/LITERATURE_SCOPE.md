# Literature and novelty scope

Search date: 2026-09-03.

## Primary foundations checked

- Bekenstein & Milgrom, *Does the missing mass problem signal the breakdown of
  Newtonian gravity?*, ApJ 286 (1984), DOI
  <https://doi.org/10.1086/162570>, scan
  <https://adsabs.harvard.edu/pdf/1984ApJ...286....7B>.
- Milgrom, *Solutions for the modified Newtonian dynamics field equation*,
  ApJ 302 (1986), DOI <https://doi.org/10.1086/164021>, scan
  <https://adsabs.harvard.edu/pdf/1986ApJ...302..617M>.
- Blanchet & Novak, *External field effect of modified Newtonian dynamics in
  the Solar system*, <https://arxiv.org/abs/1010.1349>.
- Banik & Zhao, *The External Field Dominated Solution In QUMOND & AQUAL:
  Application To Tidal Streams*,
  <https://arxiv.org/abs/1509.08457>.
- Banik & Zhao, *Testing gravity with wide binary stars like alpha Centauri*,
  <https://arxiv.org/abs/1805.12273>.
- Zhao & Famaey, *Refining MOND interpolating function and TeVeS
  Lagrangian*, <https://arxiv.org/abs/astro-ph/0512425>, DOI
  <https://doi.org/10.1086/500805>.  This is an early explicit discussion of
  the empirical MOND interpolation function
  \(\widetilde\mu(x)=1-e^{-x}\); it is not cited as the source of the AQUAL
  \({\cal G}\) used here or asserted to establish absolute priority.
- Sánchez-Salcedo & Hernandez, *Masses, Tidal Radii, and Escape Speeds in
  Dwarf Spheroidal Galaxies under MOND and Dark Halos Compared*,
  <https://arxiv.org/abs/astro-ph/0702443>, DOI
  <https://doi.org/10.1086/521213>.  Its appendices already map a deep-EFD
  homogeneous physical sphere to an oblate ellipsoid with
  \(z'=z/\sqrt2\).
- Li & Liu, *Periodic orbits of the spatial anisotropic Kepler problem with
  anisotropic perturbations*, EJDE 2021, Paper 63,
  <https://ejde.math.txstate.edu/Volumes/2021/63/li.pdf>.  Its spatial
  Delaunay expansion and averaged Hamiltonian contain the same
  eccentricity/periapsis structure as the node law here after notation and
  anisotropy-sign translation.

Bekenstein--Milgrom establishes the action and EFD behavior; Milgrom,
Blanchet--Novak, Banik--Zhao, and Zhao--Famaey give closely related EFD
operators or point-source potentials.  The wide-binary paper supplies orbital
context rather than the original AQUAL action.  Therefore the circular
nodal-frequency split in this bundle is explicitly classified as a prior-art
corollary, not a discovery.

## Targeted searches

Repository-wide searches covered `nodal precession`, `node precession`,
`longitude of ascending node`, `vertical frequency`, `omega_z`, `nu_z`,
`external-field dominated`, `anisotropic Green`, ellipsoid depolarization
factors, and the closed constants involving `pi-2` and `4-pi`.

Web/arXiv and SciSpace semantic searches included:

- AQUAL external-field-dominated point-mass binary orbit inclination;
- MOND nodal precession with eccentricity and argument of periapsis;
- longitude of ascending node in the MOND external-field effect;
- homogeneous/uniform sphere in AQUAL under a constant external field;
- ellipsoidal depolarization factors after anisotropic Poisson rescaling;
- the literal factor `e/(1+sqrt(1-e^2))` in nodal formulas.

No checked source stated verbatim

\[
P\dot\Omega_{\rm node}=\pi\epsilon_e{\cos i\over\sqrt{1-e^2}}
[1-\alpha^2\cos(2\omega)]
\]

or the general-\(q\) boundary-matched uniform-sphere clock ratio in this
notation.  That absence is not a structural novelty claim: Li--Liu contains
the averaged spatial anisotropic-Kepler Hamiltonian from which the first
formula follows, while Sánchez-Salcedo--Hernandez already performs the deep
\(q=2\) MOND homogeneous-sphere coordinate stretch underlying the second.

## Novelty classification and blind spot

The defensible wording is:

> Both results are repository-new observable extractions from known
> structures.  The finite-e node law is a MOND specialization of the known
> first-order averaged spatial anisotropic-Kepler Hamiltonian; the general-q
> core clock ratio extends a homogeneous-sphere EFD coordinate-stretch
> construction already used in MOND.  Neither is claimed globally novel.

Li--Liu is a close structural antecedent, not merely a possible blind spot.
The earlier planar paper *Periodic orbits for anisotropic perturbations of the
Kepler problem*, <https://doi.org/10.1016/j.na.2006.11.019>, and the newer
spatial work <https://arxiv.org/abs/2607.03244> further show an active generic
mechanics literature.  The search was not exhaustive over paywalled full
text, citation graphs, theses, or non-English literature.

The ellipsoid depolarization machinery is classical.  The contribution here
is the general-\(q\) exponential specialization, extraction and independent
check of the individual Hessian frequencies, and correction of a
repository-local shortcut.  The deep coordinate-stretch application itself
is already present in Sánchez-Salcedo--Hernandez (2007), and homogeneous-
ellipsoid gravity is classical.
