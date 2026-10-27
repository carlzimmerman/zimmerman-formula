# A nodal quantum band supplies the required cold response—but not yet a galaxy mechanism

**New partial result:** an explicit three-dimensional nodal-ring effective
Hamiltonian produces the exact zero-temperature critical polarization curve that
we previously supplied as a gap-distribution ansatz. A driven nonthermal
preparation test can approach that curve while accounting for all source work.
The existence, formation and astrophysical population of such a material remain
unproved. This is not an exact interacting many-body theory or a completed answer.

## What is now derived

[The Hamiltonian](DERIVATION.md) has two kinetic matrices and three mutually
anticommuting dipole matrices. Its energies are

E_plus/minus=+/-sqrt(xi(p_perp)²+v_z²*p_z²+d²*|E_field|²),
xi=(p_perp²-p0²)/(2*m_star).

At zero field, the bands touch on a ring in three-dimensional momentum space.
The available states obey g(u)=C*u below a specified cutoff. Both this linear
density of states and the nonzero dipole transition matrix elements follow from
the displayed Hamiltonian. Counting modes alone would not have established it.
At half filling and zero temperature, integration gives

P/(chi*E)=sqrt(1+e²)-|e|, e=dE/Lambda, chi=C*d²*Lambda.

This is the predecessor's cold response exactly. The band realizes its exponent
and response together, rather than supplying an independent prescribed spectrum.
However m_star, v_z, p0, Lambda, d, multiplicity and filling are still effective
band inputs. Neither their microscopic interactions nor a0 are derived. Spectral
isotropy of the Clifford model is not proof of a physically realizable isotropic,
inversion-symmetric, gauge-complete dark material.

## State tests: two difficulties and one surviving route

**Temperature:** at half filling the occupation difference is tanh(r/(2kBT)).
For every fixed positive T, sufficiently weak fields again have an analytic
response. Holding the charge matching fixed restores a leading linear source
law. The same cold-law vulnerability therefore survives the microscopic spectrum
improvement. Thermal tolerance at x=g/a0=.01 is kBT/Lambda<=.006352 for a .05dex
shift relative to this candidate's own cold curve.

**Filling:** even at T=0 a nonzero chemical potential blocks the soft interband
transitions. At the same x=.01 the .05dex response tolerance is
|mu|/Lambda<=.01220. These are separate one-variable screens, not simultaneous
joint bounds. Half filling and charge compensation need a physical state,
not a parameter chosen separately for each object. Finite-mu calculations are
fixed-chemical-potential diagnostics, not self-consistent fixed-mass halos.

**Nonthermal unitary preparation:** an isolated filled band can avoid thermal
occupation. We tested a smooth field ramp from an already prepared negative-band
ground state, with fermion number conserved and source work explicitly counted.
The sensitive comparison is the small remainder chi*E-P that sources the force,
not just the much larger polarization.

| Final field e | Ramp duration (hbar/Lambda) | Dephased source-remainder error |
|---:|---:|---:|
| .01 | 1 | 56.77% |
| .01 | 100 | 29.58% |
| .01 | 1000 | 2.23% (refined) |
| .1 | 100 | 2.33% |
| .1 | 1000 | .119% |

For e=.01,T_ramp=1000,64->128 mode refinement changes the error from2.2207%
to2.2297%; halving dt=.1 to.05 changes the refined relative error by2.92e-10.
The discrete matter-energy plus source-work error stays below5e-15 in these
units. The field is prescribed, so this is not an isolated assembly calculation.
“Dephased” means projection onto the final fixed Hamiltonian's eigenbasis, not
thermalization, irreversible cooling or an actual measured galaxy response.
Finite mode quadrature and finite tests do not prove the continuum adiabatic limit.

This route remains open precisely because the previous finite-temperature
obstruction does not cover a prepared nonthermal state. The test does not derive
its initial filling, protect it against collisions, create the nodal band, or
show that gravity/rotation generates the required ramp. Formation remains the
central missing step; do not rename the prescribed protocol galaxy assembly.

## Thermal collective alternatives tested

[Two elementary thermal routes](THERMAL_SIGN.md) do generate cubic free energies,
but with the wrong sign. A three-dimensional Gaussian mode with M proportional
to |E| gives, after its analytic quadratic term is subtracted,

F_nonanalytic=-kBT*M³/(12*pi).

A stable tricritical phi^6 saddle with negative E²*phi² coupling also gives
F_min proportional to -|E|³. Both enhance the polarization. The tether curve
requires a positive cubic matter-free-energy correction that saturates it.
A directly conjugate quartic critical order parameter instead has singular
P proportional to E^(1/3), not the desired finite susceptibility plus correction.
These results reject only the displayed mechanisms. They do not rule out all
interacting thermal critical phases, nonlocal couplings or nonequilibrium media.

## The light-carrier loophole has a further conditional limit

For a local unit consisting of exactly two opposite charges with subluminal
velocity operators, the dipole-current identity implies
Delta*|p_0n|<=2*hbar*q*c. If d=q*ell and the interband gap is2Lambda,
Lambda<=hbar*c/ell. Combined with the earlier critical-curve mass inventory,
this prevents arbitrarily raising the bandwidth by making a countercarrier
lighter while keeping the local-pair realization and density fixed.

For the generous large-disk inventory, epsilon=.1 gives ell_min=8.71pc and
an optimistic temperature ceiling5.41e-23K at x=.01 from this speed bound alone.
Reducing epsilon to1e-8 changes it only to5.95e-23K. The canonical nonrelativistic
oscillator-strength bound may be stronger. These are not universal temperature
limits: a collective band with different current operators, carrier inventory,
nonlocality or pair creation is outside the local-two-carrier assumption. Nor
can a Bloch-band state count automatically be identified with independent
positive-mass pairs without a microscopic construction.

## Verification

- Clifford anticommutation: exact in the implemented matrices.
- Band eigenvalue error:4.45e-16; dipole trace identity error:4.80e-16.
- Closed response versus independent occupation quadrature:2.83e-10.
- Direct transverse-state grids128²/256²/512² reproduce the response; largest
  tested512² polarization error1.62e-5. Hard-circle cumulative state counts have
  boundary quadrature error up to.14%; no claim of monotonic CDF convergence.
- Eight closed fixed-D mode evolutions conserve their field-plus-band energy;
  finest-tolerance maximum relative error6.11e-11. Norm errors below6.84e-12.
  These are homogeneous independent-mode checks, not full Maxwell transport.
- Thermal cubic coefficient converges to -1/(12*pi), with relative cutoff
  correction4.78e-5 at M/Lambda=1e-4; the tricritical minimum is-1/3 in test units.
- Eleven driven ramp calculations include timestep and mode-count refinement.

All three provenance manifests completed and validate against current inputs:
[band](run_band/manifest.json), [thermal sign](run_thermal/manifest.json),
[nonthermal ramp](run_ramp/manifest.json). Raw results accompany each. No failed
runs are hidden. Scripts/contracts retain exact bounds and reproduction commands.

## Remaining research obligations

1. Derive a stable nodal phase from a specified microscopic interaction, including
   its mass, charge compensation and physical spatial symmetries.
2. Derive formation/filling and entropy removal or nonthermal preparation,
   including collisions and the work source, without a prescribed galaxy label.
3. Couple its irreducible response consistently to live fields and gravitating
   matter; demonstrate positively charged tethering and retained free populations.
4. Test acceleration, lensing and disk/dwarf/cluster predictions with common
   microscopic parameters and resolved dynamics.

These are not completed. This checkpoint improves the spectral origin and tests
an explicit preparation loophole, while preserving the original scientific goal.
Primary context for nodal-line bands:
https://arxiv.org/abs/1110.1089 . The result here is our effective-Hamiltonian
calculation, not a claim that that paper proposes or validates this dark medium.
