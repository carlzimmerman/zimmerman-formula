# Two-electron channels and finite-rate/photon interface

**Partial result: absolute finite collision rates are still unresolved. No new
physical disk/dwarf/cluster separation test has been completed.**

The previous photon model is unchanged. This stage computes correlated
(two-electron) channel energies and implements a conservative interface for
future scattering coefficients. It does not turn bound-state energies into
reaction rates.

## Findings

1. The Coulomb Hamiltonian fixes the dimensional collision scale:
   k_phys=hbar²/(m_C² c alpha) times a dimensionless scattering integral.
   No independent collision normalization is needed in a first-principles
   completion. The missing quantity is the actual quantum reaction probability.
2. The same microscopic interaction supports neutral X2C2 and negative XC2
   bound channels. At R=1.4, singlet neutral electronic energy is −1.164608
   (aug-cc-pVDZ) and −1.172633 (aug-cc-pVTZ). Negative-ion electronic energy
   is −.524029 and −.526562, below the clamped atomic threshold−.5.
3. With nuclear mass100, the DZ neutral BO curve gives a J=0 ground binding
   about .12574 atomic energy units relative to its two-atom asymptote.
   Three J=0 negative eigenvalues appear in this finite box; that is NOT a
   complete rovibrational spectrum. Nuclear step refinement changes ground
   binding by7.4e−7 from h=.01 to.005, but electronic basis/interpolation/BO
   errors dominate. This is evidence for the channel, not precision spectroscopy.
4. At the previously tested shared point alpha=.2 and m_C=10^7eV, representative
   entrance Coulomb parameters eta are2275,228,16.1,3.94 for the two dwarf,
   disk and cluster profiles. None satisfies eta<<1. A plane-wave Born
   calculation cannot be accepted as a controlled low-temperature rate estimate.
5. The finite DR source and its detailed-balance inverse conserve both counts,
   charge and energy when coupled to recycled photons. A manufactured-rate
   integration has energy error6.94e−17 per pair and charge error1.11e−16;
   its Jacobian directional error is1.60e−9. Four software tests pass.
   Manufactured rates are not physical evidence for population separation.

## What is still required

A Coulomb-matched continuum S matrix with electronic exchange, spin, neutral
resonances, nuclear couplings and product branches is missing. Both the bound
Gaussian FCI calculation and an S-matrix probability ceiling lack that
information. No physical finite-rate halo run was made (count=0), and no
hand-set galaxy types or fitted rate multipliers were introduced.

The additional species also need dynamic populations, countercharge accounting,
energy transport and their own formation/dissociation channels. Finite-mass
thermochemical corrections must be made consistently with a refined photon
spectrum before claiming precision. Live gravity, rotating disks and the
acceleration relation remain outside this homogeneous chemistry calculation.

## Files and reproduction

- `surfaces.py`: correlated neutral singlet/triplet BO energies and negative ion;
  `run_surfaces/results.json`:46 R points, two basis checks and nuclear steps.
- `coupling.py`: probability-to-Maxwell-rate integral, omitted-energy-tail
  unitarity bound, conservative DR source, and photon RHS/Jacobian adapter.
- `test_coupling.py`, `audit.py`, `run_audit/results.json`: independent
  normalization, equilibrium, invariants, integration and applicability tests.
- `DERIVATION.md`: conventions, rate scaling, energy/charge proof and caveats.
- `SOURCES.md`, `AUDIT.md`, `VALIDATION.json`: provenance and interpretation.

Use Python3.9.6, NumPy1.26.2, SciPy1.11.4, h5py3.14.0, PySCF2.11.0.
PySCF was installed in `/private/tmp/two-electron-pyscf` with `--no-deps`;
no global environment was changed. That temporary installation is not a durable
repository dependency. Install the pinned PySCF version in your own environment
for reproduction; all scientific scripts use its public interfaces.

The exact runner invocations and inputs are in each run's manifest. For a quick
unrecorded software test from the repository root:

```
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 python3 -m unittest discover -s two_state_mechanism_2026_10_25/scattering -p 'test_*.py'
```

Both recorded runs completed. The surface result is conditional on finite bases
and the stated BO/box approximations; the coupling result verifies implementation
with manufactured rates. Neither outcome establishes the requested mechanism.
