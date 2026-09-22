# Spectral spine closure: target and checkpoint

Delegated base: `e3af62a453ca6625db8428f6d32957b27a7f1331`.
Targets: commits `ca2f8fd0d`, `827ef5f17`, `34e5eafd8`, `790ee1d37`.
Authorization: user requested an attempt to close the gaps identified in the
review ("see if you can swing it home"). Mathematical derivations, scoped code
changes, local experiments, and source checks are authorized. No continuum
Yang–Mills solution, physical parameter selection, or fabricated stellar data
is part of the definition of success.

## Original obligations

1. I13: relate the stated pressure-work expression to the actual radial
   pulsation operator, determine the direction of each variational inequality,
   derive the structural GR coefficient, and evaluate the physical instability
   on authenticated profiles if available.
2. I14: determine the complete finite-box spectrum and sharp uniform stability
   boundary including confinement; derive the alleged physical fluctuation
   form from the cited action or exhibit the precise obstruction.
3. I15: prove an actual Hamiltonian gap inequality, with the gauge constraint,
   ground energy, full Hilbert space, lattice volume, coupling normalization,
   and N dependence explicit. Distinguish a single plaquette from a lattice.

## Executed routes and ownership

- I13 operator/variational route: `i13_radial_bridge`, write scope `i13/` and
  comments in I13 Lean. Decisive checks: exact work identity, known n=3 PN
  coefficient, trial/eigenvalue discrepancy, exact GR comparison.
- I14 diagonalization/counterexample/source route: `i14_exact_spectrum`, write
  scope `i14/` and I14 Lean. Decisive checks: sine basis, sharp slab family,
  constant confinement counterexample, direct scalar Hessian.
- I15 min–max and weak-interaction transfer routes: coordinator, write scope
  `i15/`, I15 Lean and shared report. Decisive checks: Casimir minimum,
  magnetic multiplication norm, interacting ground-state subtraction, exact
  source hypotheses and dependence of constants.
- I15 source-transfer review: `i15_transfer_audit`, read-only. This is a fresh
  reconstruction of the critical application from its statement and primary
  source; agreement is not itself mathematical proof.

The original physical goals remain distinct from weaker completed statements.
Source/version limits and numerical tolerances are recorded with each result.
Unrelated concurrent commits and working-tree files are not modified by this
work. A final report reconciles actual inputs against this base.
