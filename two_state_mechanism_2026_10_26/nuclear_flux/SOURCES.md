# Sources and implementation provenance

Base research checkpoint:0343483bcb63d46da0b1fd4fde2f1509d0bdbb3c.

- [Hörnquist, Orel and Larson, PRA109,052806 (2024)](https://journals.aps.org/pra/pdf/10.1103/PhysRevA.109.052806): source checked for the physical role of
  state-resolved nuclear propagation and nonlocal autoionization. Its equations6–11
  distinguish a nuclear nonlocal kernel from a local width and construct DR
  amplitudes from capture coupling and outgoing nuclear solutions. The study
  concerns HD+ and uses approximations; neither its rates nor its fitted/quasidiabatic
  curves have been imported for mass ratio100. It supports the need for the missing
  calculation, not a claim that our program reproduces it.
- [Čurík, Hvizdoš and Greene, arXiv1910.02628](https://arxiv.org/abs/1910.02628):
  energy-dependent frame transformation and exterior-complex-scaled nuclear
  functions for HeH+. This is an alternative method, not a ready-made product
  branching table for the present Coulomb parent.
- [UKRmol-in3.3.0](https://zenodo.org/records/18340340) and
  [UKRmol-out3.3.0.1](https://zenodo.org/records/18538198): same authenticated
  source/binaries as ../continuum/SOFTWARE.json. No external physics code was patched.
  CI file conventions checked in tests/scripts/dump-scatci.py; boundary normalization
  and binary layout checked in source/libouter/outerio.f, READRH/READRM. Own Python
  readers implement those formats and test independent eigenvalues/optical identities.
  Prior templates and bundled license remain in ../continuum.

The finite-difference projection, lattice matching and conservative event ledger
are derived in DERIVATION.md. Atomic2p energy and dipole coefficient have analytic
Coulomb checks. Literature searches did not supply an authenticated complete
mass-ratio100 electron+nuclear capture kernel or branching dataset.
