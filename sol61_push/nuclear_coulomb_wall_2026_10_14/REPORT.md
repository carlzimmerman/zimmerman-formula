# A conditional repulsive material wall from nuclear Coulomb energy

2026-10-14. Parent checkpoint: 9028d4bca65e78f7831c1c86de0b5d485cf76ccc.

The eV branch's photon portal can generate a repulsive carrier potential in
ordinary matter through nuclear electromagnetic binding energy. In a
Coulomb-only estimate, the stronger assigned source coupling gives a barrier
about 5.1e-7 eV, above the 1e-8 eV carrier-energy cut. An ideal centimetre cavity
then supports a confined mode. This is a concrete confinement candidate, not
a verified container: full scalar-to-material matching and production into its
finite-volume levels remain unresolved.

## Derive the sign and response rather than assigning a wall

Use the same hypothetical scalar interactions and canonical photon convention:

    L = -(1+g R) F^2/4 - M_R^2 R^2/2 - mu R |phi|^2 + ...

For slowly varying R, canonical normalization gives
alpha(R)=alpha(0)/(1+g R). At first order d ln(alpha)/dR=-g. A nucleus with
positive pair Coulomb energy E_C proportional to alpha therefore contributes

    d M_nucleus/dR = -g E_C.

In bulk material with number density n_N, the Coulomb-only source and induced
carrier mass shift are

    R_bulk = g E_C n_N/M_R^2,
    U_wall = mu R_bulk/(2m)
           = mu g E_C n_N/(2m M_R^2).

Positive mu*g produces a REPULSIVE material potential for both signs of phi.
That same sign produces an attractive potential from a macroscopic magnetic
field; electric nuclear binding and magnetic field energy enter differently.
An electrically neutral atom need not have zero scalar electromagnetic mass
sensitivity. Its electron binding and nucleon electromagnetic self-energies
must, however, be included in a complete calculation.

This term is a contribution to the material response, not proof that g alone
fixes the full response. Other scalar couplings, matching counterterms, quark
mass effects, nuclear correlations, charge form factors and running can alter
it. In particular, optical on-shell g is not sufficient to determine a
coefficient sampled by nuclear virtual photons. We explicitly assume the local
RF^2 coefficient remains applicable through momenta of order 28 MeV and that
uncomputed terms do not cancel the estimated Coulomb contribution. These are
additional matching obligations, not established by optical production.

## Material inputs and nuclear approximation

For a uniform distribution of Z independent proton centers in radius R_N,
the pair Coulomb expectation is

    E_C = 3 Z(Z-1) alpha (hbar c)/(5 R_N).

The Z(Z-1) factor excludes individual proton self-energies. Using the
approximate relation R_N=sqrt(5/3) r_charge,rms for a uniform sphere gives
R_N=7.1085 fm for the radius input below. This uniform sphere is a modeling
choice; it is not the Fermi distribution used to extract the experimental
radius.

Inputs checked on 2026-10-14:

- [NIST lead composition](https://physics.nist.gov/cgi-bin/Star/compos.pl?matno=082&refer=ap)
  lists density 11.35 g/cm^3 and Z=82.
- [NIST isotope/atomic-weight listing](https://pml.nist.gov/cgi-bin/Compositions/stand_alone.pl?ascii=ascii&ele=Pb)
  supplies 207.2 as the tabulated standard atomic weight used for this estimate.
- Sun et al., [arXiv:2504.19977v2](https://arxiv.org/pdf/2504.19977v2), September
  2025, give a Pb-208 rms charge radius 5.5062 fm from a spectroscopy and QED
  reanalysis, with 0.0017 fm suggested reduced-model-dependence uncertainty.
  This radius is theory-dependent extracted evidence, not assumption-free data.

Combining natural-lead density/atomic weight with a Pb-208 radius is an
explicit isotope-averaging approximation. It gives n_N=3.2988e28/m^3 and
E_C approximately 807 MeV per nucleus. Nuclear-model uncertainty dominates
retaining additional numerical digits in this estimate.

The physical basis is established scalar-response physics, not a newly observed
interaction: Damour and Donoghue,
[Equivalence Principle Violations and Couplings of a Light Dilaton](https://arxiv.org/pdf/1007.2792),
section 4.3, discuss the Coulomb term proportional to alpha Z(Z-1)/R_N and
independent scalar sensitivities of atomic masses. Their framework motivates
keeping other scalar charges separate. We do not transfer their long-range
force constraints to this approximately 100 nm-range mediator.

## Surface smoothing and barrier scale

The static equation is

    (-laplacian+M_R^2) R = g E_C n_N(x).

For a planar half-space of material at x>0, the exact continuum solution is

    R/R_bulk = exp(M_R x)/2                    for x<0,
             = 1-exp(-M_R x)/2                for x>=0.

Coordinates here are natural-unit lengths. The field and its first derivative
match at the interface. For M_R=2 eV, the smoothing length is 98.7 nm, much
smaller than the millimetre-scale carrier wavelength and cavity dimensions.
The homogeneous source averages over many atoms on this range; it does not
resolve individual nuclei at the wall boundary.

Retain m=1 eV, g=1e-20/eV and mu^2=lambda_rep M_R^2:

| lambda_rep | mu (eV) | Coulomb-only repulsive barrier (eV) | Attractive 10 T magnetic depth (eV) |
|---|---:|---:|---:|
| 1e-6 | 0.002 | 5.115e-7 | 4.770e-18 |
| 1e-15 | 6.325e-8 | 1.618e-11 | 1.509e-22 |

The magnetic depth is recomputed with the same eV-branch inputs using
U_B=-mu*g B_nat^2/(4m M_R^2). It remains inadequate at the assigned energy
cut. Nuclear Coulomb energy is not represented by a laboratory 10 T field.

The scalar mean in the material is R_bulk=5.115e-4 eV; g R_bulk is tiny, so
the displayed first-order electromagnetic normalization is internally small.
This check does not establish the omitted nuclear matching or all higher
operators. Requiring the Coulomb-only barrier to reach 1e-8 eV corresponds to
mu>=3.910e-5 eV, or lambda_rep>=3.822e-10 in this assigned family. It does not
remove the previously calculated scattering and decay-distance tradeoff.

## Quantum confinement and finite-wall leakage

As a geometry diagnostic, put a vacuum sphere of radius a=1 cm inside an
infinitely thick material with potential U. A below-material-threshold s-wave
exists only if

    U > pi^2 (hbar c)^2/(8 m a^2) = 4.804e-10 eV.

The stronger case passes; the weaker case fails this particular spherical
criterion. The ground level of the stronger case, relative to the vacuum
carrier rest energy, is 1.849e-9 eV. It solves

    x cot(x) = -sqrt(z0^2-x^2),
    z0=a sqrt(2mU)/(hbar c), E=(hbar c)^2 x^2/(2ma^2).

This reference problem is not the earlier 1 m optical resonator. No combined
cavity geometry, modal overlap or source rate into these levels is asserted.
For a finite material shell with vacuum beyond it, the levels become resonances
with tunneling loss rather than globally bound negative-energy states.

An independent planar rectangular-barrier diagnostic uses

    T = [1+U^2 sinh^2(kappa d)/(4E(U-E))]^-1,
    kappa=sqrt(2m(U-E))/(hbar c), 0<E<U.

At E=1e-8 eV in the stronger case, T is approximately 1.20e-5 for thickness
1 mm and 2.52e-45 for 1 cm. These are transmission probabilities per ideal
normal-incidence encounter, not storage lifetimes. Roughness, interfaces,
scattering, absorption, scalar conversion, defects and a three-dimensional
escape calculation remain absent. Four-boundary wave matching independently
checks the 1 mm values and reflected-plus-transmitted flux.

## Loading is a separate calculation

A static repulsive wall cannot capture an incoming particle from infinity by
itself. The relevant proposal is to CREATE carriers inside its low-potential
cavity. Unlike loading an attractive well from a fixed above-threshold source,
this does not require making their global energies negative: they can occupy
levels below the surrounding material barrier, with finite-shell metastability.
Energy conservation and wavefunction overlaps still decide whether creation
actually populates those levels.

For the illustrative sphere, two ground levels cost approximately 3.70e-9 eV
above the free pair rest energy. The previous moving optical mediator has
available excess approximately delta+epsilon=6.87e-9 eV. That exceeds the
minimum energy but does not prove a transition: discrete levels, source recoil,
angular momentum, linewidth and the finite geometry must all be matched. The
old continuum decay width cannot simply be reused as a trapped-pair loading
rate. The mediator itself still tends to leave the production region before
its vacuum decay.

This is a conditional route to supplying the missing wall from ordinary
matter, without reinstating the previously excluded charged messenger. It is
not an independently added arbitrary trap coefficient: the displayed Coulomb
piece is derived from the same photon portal under the stated extrapolation.
Its total magnitude/sign and compatibility with constraints remain open.

## Verification and next step

Thirteen bounded checks cover the uniform-sphere Coulomb coefficient, five
Yukawa surface integrals, two potential-normalization comparisons, spherical
level matching, two independent transmission matches and two flux checks.
Manifest validation records the reproducible execution. These computations
are self-reviewed; no new Lean certification of nuclear response or trapping
is claimed.

Reproduce:

    python3 sol61_push/nuclear_coulomb_wall_2026_10_14/check.py /tmp/coulomb_wall_results.json

The next decisive task is to replace the Coulomb-only extrapolation with a
specified microscopic scalar-photon/material matching calculation, then compute
creation into the same finite cavity's modes. The goal remains open until those
steps and a consistent loss/constraint analysis establish a preparation route.
