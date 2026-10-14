# Conditional optical access and retention through a silica shell

2026-10-14. Parent checkpoint: 051d10c00848d7684a216c9d71191f914f8a39b1.

A transparent-wall candidate removes the need to postulate an open pump hole.
The same Coulomb-only photon-portal model gives a silica barrier of 2.86e-8 eV.
For a 2 cm-radius vacuum cavity, a 5 mm ideal silica shell has a calculated
single-particle tunneling lifetime of 3.18 seconds. Recomputing the optical
virtual-pair source for silica gives a leading 1% creation timescale of 11.5 ms.
Including tunneling in a weak-drive model changes that estimate to 0.996%.

This is a shared material-and-mode calculation under explicit assumptions, not
a demonstrated apparatus. The complete scalar material response, optical mode
through the curved shell, thermal/absorption performance and other losses remain
unverified. The quoted lifetime is a tunneling lifetime only.

## Optical and material evidence

[Corning's HPFS industrial-grade datasheet](https://www.corning.com/media/worldwide/csm/documents/1e624b3034474193b5b00ea6f558dd3d2.pdf)
lists density 2.201 g/cm^3. The [manufacturer's material overview](https://www.corning.com/worldwide/en/products/advanced-optics/product-materials/semiconductor-laser-optic-components/high-purity-fused-silica.html)
describes broad optical transmission and different grades. These are material
properties, not a certificate for the previously assumed circulating intensity.

Malitson, [Interspecimen Comparison of the Refractive Index of Fused Silica,
JOSA 55, 1205 (1965)](https://opg.optica.org/josa/abstract.cfm?uri=josa-55-10-1205),
reports dispersion over 0.21–3.71 micrometres. Its Sellmeier formula gives
n=1.44760 at the approximately 1 eV photon wavelength, 1.23984 micrometres.
A single uncoated, normal-incidence vacuum interface then reflects 3.344% in
the real-index model. Absorption is not inferred from a real refractive index;
we have not assigned a measured attenuation coefficient at the required power.
These sources were checked on 2026-10-14. A separate manufacturer's PDF failed
to open and was not used as evidence.

No shell hole is required in principle for electromagnetic transmission. That
observation does not solve refraction, coatings, resonator feedback, pump phase,
absorption or heat removal. The preparation calculation continues to ASSIGN
intracavity intensity 1e12 W/m^2 in each wave; it does not calculate the external
power or an achievable buildup factor.

## Apply the same hypothetical portal to SiO2

Retain m=1 eV, M_R approximately 2 eV, mu=0.002 eV and g=1e-20/eV.
Use density 2201 kg/m^3 and molar mass 0.0600843 kg/mol. For a simple nuclear
composition model take Si-28 and O-16 and the semi-empirical Coulomb coefficient
ac=0.717 MeV used in the previously checked Damour–Donoghue source. Set

    E_C(Z,A)=ac Z(Z-1)/A^(1/3),
    R_N=r0 A^(1/3), r0=3 alpha (hbar c)/(5ac)=1.205 fm.

These radii are model radii, not isotope-specific measured charge radii.
Apply the preceding muon-loop spacelike correction separately to each nucleus.
It gives ratios 0.91304 for silicon and 0.88465 for oxygen, for a total matched
Coulomb response of 67.43 MeV per SiO2 formula unit. The number density is
2.2060e28 formula units/m^3. Thus

    U=mu g n_formula (E_Si+2E_O)/(2m M_R^2)
      =2.85732e-8 eV.

Only the modeled nuclear pair-Coulomb contribution is included. Atomic binding,
nucleon electromagnetic masses, other scalar operators and microscopic defects
are not silently set by the optical refractive index. The wall potential remains
a conditional new-particle prediction, not a measured property of silica.

## Finite shell: use an outgoing resonance rather than a bound-state label

Take a vacuum sphere of radius a=2 cm, material barrier U over a<r<a+d, and
vacuum again outside. For an s-wave, the radial function is proportional to
sin(kr) inside, a combination of exponentials in the shell, and exp(ikr)
outside. At a complex resonance energy E,

    k=sqrt(2mE), q=sqrt(2m(U-E)),
    L_inner=(i k-q tanh(qd))/(1-i k tanh(qd)/q),
    k cot(ka)=L_inner.

Lengths in this equation are natural-unit lengths. The outgoing boundary makes
Im(E)<0. Define Gamma=-2 Im(E) and the single-particle decay time hbar/Gamma.
Roots are computed at 80 decimal precision. An independent transfer-matrix
propagation checks the exterior logarithmic derivative. Initial unbracketed
reference-root search failed; a bracket within the first s-wave interval fixes
the starting branch before the complex outgoing root is located.

| Shell thickness | Re(E), eV | Single-particle tunneling lifetime |
|---|---:|---:|
| 1 mm | 4.3640e-10 | 0.183 ms |
| 5 mm | 4.4296e-10 | 3.176 s |
| 10 mm | 4.4296e-10 | 5.275e5 s |

These are ideal elastic tunneling results, not total storage predictions.
At 10 mm, halving the assumed barrier changes this lifetime to about 221 s;
doubling it changes it to 2.40e10 s. This sensitivity underscores why the
largest ideal lifetimes must not be advertised as physical performance. The
factor-two cases are sensitivity tests, not confidence intervals.

## Recompute preparation for this material

prepare.py repeats the prior single-ground-pair/free-mediator-resolvent
calculation with silica's U. It retains the same conditional prescribed optical
field and source cutoff at the inner cavity. The corresponding infinitely thick
reference wall is used for normalized orbitals. Its ground energy agrees with
the 5 mm finite-shell real pole within 1e-6 relatively; the 1 mm case is too
leaky to inherit an equally accurate bound-mode approximation.

The recomputed values are

    E0=4.42960e-10 eV,
    dressed pair excess=8.85816e-10 eV,
    delta-Epair=1.11418e-9 eV > 0,
    |Omega|/hbar=8.70627 per second,
    t_1%=0.011486 s.

The confined pair remains below the free mediator threshold. The photon energy
must be retuned to this pair state, including finite-shell and interaction
shifts; the previous lead-wall frequency must not be reused unchanged. The
spatial field through a transparent shell, including possible drive within the
material, has not yet been solved; prescribed intensity inside is retained.

As a weak-drive loss diagnostic, let the independent single-particle tunneling
lifetime be tau. The pair's population loss rate is 2/tau, so its initially zero
amplitude obeys

    d c_pair/dt = -c_pair/tau-i Omega/hbar,
    P_pair(t)=[(|Omega|/hbar) tau (1-exp(-t/tau))]^2.

This assumes an undepleted vacuum amplitude and a resonantly tuned pair level.
It omits many-pair stimulation and other losses. The 5 mm baseline gives
P_pair(t_1%)=0.00996391; 10 mm gives approximately 0.01. Numerical ODE solutions
check this expression. The 1 mm and scaled-barrier rows retain the SAME drive
matrix element only as loss sensitivity diagnostics; they are not recalculated
loading predictions for each changed orbital. Jumps leaving a single carrier
and subsequent repumping are outside the leading weak-drive treatment.

## What this advances

The material can be optically accessible in a conventional linear-optics model
while serving as a conditional carrier barrier, and the same silica mode has
both a calculated preparation amplitude and finite-shell leakage. No open
carrier escape hole has been assumed away. This improves the preparation chain
beyond separate source and trap estimates.

It still does not establish the physical dark sector, the complete material
potential, high-power operation, a solved curved-shell resonator or total
retention. Photon-induced losses, wall excitations, imperfections, higher modes
and a finite pulse must be treated before calling this a preparation protocol.
The connection to the repo's cosmological cold component remains separate.

## Evidence and reproducibility

The material/finite-shell runner passes 18 bounded checks; the recomputed
preparation passes 12. Scientific outputs material.json, preparation.json and
results.json are all hash-recorded. prepare.py is a pinned adaptation of the
prior ground-pair script, with only its material input and output interface
changed. No new Lean proof is claimed; the previously proved conditional
free-mediator energy inequality applies when its hypotheses hold, but does not
certify these material or mode calculations.

Reproduce into a dedicated output directory:

    mkdir -p /tmp/silica-shell-check
    python3 sol61_push/silica_shell_retention_2026_10_14/check.py /tmp/silica-shell-check/results.json

The overall goal remains open. The next step is a finite-pulse, multi-pair
calculation with a consistent electromagnetic mode and loss budget, retaining
the material-response and empirical-admission obligations.
