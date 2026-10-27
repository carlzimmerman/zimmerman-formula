# Opposite-sign portal: local quadrupole storage

2026-10-13. A different branch from the preceding attractive-well test. The
relative Yukawa/source sign is not fixed by the decay widths. Choosing mu*y>0
in the conventions of ../muon_field_source_shift_2026_10_13/REPORT.md gives

    U(B)=kappa B^2,
    kappa=1.93821197597e-28 eV/T^2 > 0.

This makes the hypothetical spin-zero carrier seek low field. It is a scalar
polarizability potential, not the linear Zeeman interaction of a magnetic atom.
No atomic magnetic moment or spin-flip rate is imported into the model.

## A local field that satisfies Maxwell's equations

Choose a current-free neighborhood with

    B(x,y,z)=b (x,y,-2z),
    div B=0, curl B=0.

Coordinates are in metres and b in T/m. Both identities are verified symbolically.
The field gives a genuine local minimum of B^2 and therefore of U. This avoids
the attractive high-field geometry issue without adding a new coupling.

The local carrier Hamiltonian, with its rest mass subtracted, is

    H=-(hbar*c)^2/(2m) Laplacian + kappa*b^2*(x^2+y^2+4z^2).

Here m denotes rest energy in eV. Define

    w=(hbar*c)*b*sqrt(2kappa/m),
    omega_x=omega_y=w/hbar, omega_z=2w/hbar,
    ell=sqrt((hbar*c)^2/(m*w)).

The infinite-quadrupole ground state has

    psi0 proportional to exp[-(x^2+y^2+2z^2)/(2ell^2)],
    E0=2w.

Direct substitution into H verifies the eigenvalue. The rms x width is
ell/sqrt(2); ell itself is the conventional oscillator length. The radial
probability inside the cylinder x^2+y^2<a^2 is 1-exp(-a^2/ell^2), independently
checked by quadrature. This cylinder probability is not the probability inside
a spherical trap.

## Finite-region localization test

For a hypothetical spherical boundary of radius a, the equatorial energy is
V_eq=kappa*b^2*a^2; the polar value is four times greater. Compare E0 with V_eq:

| b (T/m) | a | Equatorial B | ell | E0/V_eq |
|---:|---:|---:|---:|---:|
| 100 | 1 cm | 1 T | 10.01 m | 4.01e6 |
| 1000 | 1 cm | 10 T | 3.166 m | 4.01e5 |
| 0.001 | 10 km | 10 T | 3.166 km | 0.401 |

The 1 cm cases fail the local harmonic localization test by many orders of
magnitude. At a fixed 10 T equatorial boundary, E0=V_eq occurs at radius 4.009 km.
At fixed radius 1 cm the equality requires a gradient 4.009e8 T/m and equatorial
field 4.009e6 T, extrapolating the leading coefficient. Equality alone is not a
long-lived storage criterion.

An infinite quadrupole has infinite field energy and is not a device. These
calculations establish only a local field and its harmonic approximation. Finite
coils require an exterior field and escape paths. Where B tends to zero far away,
a positive B^2 potential does not provide negative-energy true bound states;
a useful finite bottle would need metastable states with sufficiently small
escape rates. The table does not compute those resonances or prove their absence
for every possible finite geometry. The 10 km example passes one local scale
comparison, not an engineering or lifetime test.

## Gravity is a separate obstacle in a supported terrestrial device

Assume equal ordinary gravitational and inertial mass and a locally uniform
downward acceleration g. Adding U_g=m*g*z/c^2 shifts the oscillator center to

    z0=-m*g/(8c^2*kappa*b^2)=-g/(4omega_x^2).

Both formulas agree numerically; square completion is checked symbolically.
For b=1000 T/m and g=9.80665 m/s^2, the formal displacement is 7.04e10 metres.
That is not a predicted trajectory or an extrapolation of terrestrial gravity
to that distance. It means the force-balance point lies entirely outside the
local model's 1 cm region: no static equilibrium exists within that region under
the stated uniform-gravity approximation.

Even placing that equilibrium at the 1 cm axial boundary would require
b=2.653e9 T/m (equatorial B=2.653e7 T). An equilibrium at the boundary would still
not retain a finite wavefunction. These enormous numbers are leading-coefficient
scale extrapolations, not strong-field predictions or proposed apparatus.

In a freely falling apparatus uniform gravity cancels in relative coordinates;
tidal gradients and finite-field limitations remain. Thus terrestrial sag is
not a universal impossibility result. Conversely, weakening ordinary gravity
for these particles would introduce another hypothesis requiring its own model
and evidence; the prior magnetic calculation supplies none.

## Source compatibility

The inherited vacuum source excess is delta=2e-9 eV. Creation near B=0 gives
K=delta/2=1e-9 eV per carrier. A 10 T equatorial barrier has energy only
1.93821e-26 eV, so the inherited on-resonance source produces particles with about
5.16e16 times that energy. Making the source originate inside the cavity does
not fix this mismatch.

For production directly into the ideal lowest pair mode the incoming energy
would instead need to match approximately 2m+2E0, with finite-field shifts,
recoil, overlap and linewidth treated consistently. The source central mass can
be assigned or the drive detuned, but neither choice by itself computes a loading
rate. Unlike an attractive well with free exterior, a repulsive finite bottle
can in principle retain positive-energy particles temporarily behind a barrier.
This is a different loading route from the negative-excess window; they must not
be conflated. The finite geometry and pair spectral function remain uncomputed.

## Verification and next decision

Ten checks pass: Maxwell divergence and curl, oscillator eigenfunction,
gravity square completion, three independent force-balance comparisons and three
Gaussian integrals. Inputs pin the preceding photon-coupling calculation. No new
Lean proof is claimed; exact algebra uses SymPy. The quantum oscillator and Maxwell
results are derived in the script rather than inferred from an atomic trapping
analogy. A web search for quadrupole magnetic traps was used only for context;
no empirical atom-trap coefficient or lifetime enters this result.

This branch supplies a locally consistent trapping geometry, but the inherited
coupling does not supply a small storage apparatus at the tested scales. A full
production proposal still needs compatible source energies, finite-volume states
and their losses. Both signs of the existing photon portal have now been tested;
adding another magnetic example at the same coupling would not resolve those
gaps. A useful next route is a separately constrained interaction with ordinary
matter, or a direct calculation of production into finite-volume modes with
explicitly changed dimensions and source parameters.

Reproduce:

    python3 sol61_push/repulsive_quadrupole_storage_2026_10_13/check.py /tmp/repulsive_quadrupole_results.json
