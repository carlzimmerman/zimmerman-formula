# A physical electric mass, and the charge transport it entails

This is a distinct continuation after the real-bond route, not a claim that all
electric couplings only move nodes. A neutral cell can contain mobile charged
particles in opposite-parity orbitals and fixed opposite ionic countercharge.

Choose real orbitals s (even) and p_z (odd). In this basis P_inversion=tau_z,
T=complex conjugation, and the position matrix element is
< s | z | p_z >= ell_sp != 0. Therefore H_dip=-Q ell_sp E_z tau_x.
The coefficient is an orbital integral, not an assigned quasiparticle charge.
For illustrative hydrogenic 1s and 2p_z wavefunctions direct integration gives
ell_sp=256 a_B/(243 sqrt(2)); a_B=4pi epsilon0 hbar^2/(mu Q^2) for Coulomb ±Q.
Those isolated levels are not degenerate: this calculation establishes a
physical dipole, NOT a nodal band in hydrogen. A material still needs the
onsite energy difference, overlaps, lattice and filling to produce band inversion.

A symmetry-compatible charged tight-binding band is
H0(k)=[m-B(cos kx+cos ky)-Bz cos kz] tau_z+v sin kz tau_y.
At m=2,B=Bz=v=1 it has a nodal ring at kz=0, cos kx+cos ky=1,
and no ring at kz=pi. T and inversion hold at E=0. The physical electric term
-d E_z tau_x anticommutes with both terms and produces a linear mass.
E breaks inversion, so the real-symmetry obstruction in the other route does
not apply. This is a constructed orbital band, not a first-principles material.
Its filled-band local patch has the desired positive |d E_z|^3 free energy.

It is anisotropic. Three fixed orthogonal copies give sum_a |E_a|^3, not |E|^3.
An isotropic distribution of domain normals would give <|n.E|^3>=|E|^3/4
and <(n.E)^2>=E^2/3, but that distribution and its assembly cannot be assumed
as a solution; fields and rotation may orient domains. No such averaging is
used in the finite transport test.

## The electric coupling is not just an onsite mass

The SAME charged particle has position R_i+z_internal. A uniform static field
also gives -QE R_i identity. Omitting this term removes real charge transport.
In a vector-potential gauge its counterpart is Peierls phases and acceleration;
it cannot be gauged away while keeping all dynamics unchanged.

For a slowly varying scalar potential in a slab of length L, the locally opened
bandgap is 2|dE| but the potential drop is |QE| L. A necessary local-band-edge
condition for a global chemical potential in every local gap is

|QE| L < 2|dE|, i.e. L < 2 |ell_sp|.

This is a semiclassical bulk-gap criterion, not a universal finite-system
spectral theorem or an estimate of a screening time. Level spacing, contacts,
interactions, localization, finite lifetime, and self-consistent fields matter.
For macroscopic samples it exposes a missing equilibrium assumption in the
mass-only free energy. It does not prove instantaneous screening or rule out
metastable operation. Neutral emergent fermions would evade monopole acceleration
only after deriving their physical orbital-like dipole operator microscopically.

## Finite slab test with explicit ionic countercharge

At a nodal-ring transverse momentum use the one-dimensional Wilson slice
H0(kz)=(1-cos kz) tau_z+sin kz tau_y. Open-chain onsite tau_z and hopping
(-tau_z-i tau_y)/2 implement it. Add -d E tau_x at every site, and, in the full
case, -Q E z_i I. Units: spacing=1, Q=1, d=.2, hence ell_sp=.2. This value is
an explicit orbital-overlap choice, not a fitted galaxy constant. Counterions
carry -Q at each site; fill exactly N single-particle states among 2N orbitals.
The resulting density integrates to +NQ, exactly cancelling countercharge.

Compare N=32,64,128, E=.01,.03,.1 for the full position operator and for the
mass-only truncation. Record transferred charge on the positive half, maximum
local charge imbalance, internal and site dipoles, excitation level spacing,
and total energy. With H(E)=H0-E P_total, finite differences of the occupied
energy must give -P_total, including both dipole terms. This verifies source-work
accounting for the prescribed-field diagnostic. It is not a self-consistent
Maxwell/Poisson screening calculation. Fixed ionic positions also mean no ionic
transport, cooling, live gravity or assembly is being simulated here.

Primary context checked 2026-10-25: Syzranov and Skinner, 'Electron transport in
nodal-line semimetals', PRB96,161105 (2017), MIT repository abstract
https://dspace.mit.edu/entities/publication/f07b623c-18d1-4644-9e90-b99f8e075902
reports nontrivial screening and conductivity in charged nodal-line materials.
We do not import its impurity formulas, or infer a screening rate from its
abstract. The finite-slab calculation and gap/drop criterion above are our
explicit scoped tests. No novelty claim.
