# Lean certificates for the gravity architecture

Scope: the conditional mathematical deductions in the October 12 gravity-architecture synthesis. This is a new, targeted formalization, not a certification of every research file in the repository. The source is [Architecture.lean](Architecture.lean); the reproducibility driver is [verify.py](verify.py).

The physical architecture is metric gravity with baryons, radiation, cold gravitating matter, dark energy and a possible interaction sector. The proposed galaxy law and its vacuum normalization remain hypotheses. The selector that would dynamically arrange cold matter into the galaxy-law profile is not supplied by these proofs.

**Verified result:** all 18 theorems compiled without warnings or errors; all three damaged proof files were rejected. The complete axiom reports contain only `propext`, `Classical.choice`, and `Quot.sound`. See [results](run/results.json), [compiler output](run/main.log), and the [provenance manifest](run/manifest.json). The manifest was validated against the execution inputs and recorded outputs. This is a self-reviewed formalization using the installed compiler, not external scientific review.

## Claim-to-theorem map

All mathematical variables below are real. Inequalities, nonzero denominators and source assumptions are explicit arguments in Lean. No project-specific axioms are declared.

| Architecture claim | Lean theorem(s) | What is assumed |
|---|---|---|
| Squaring the proposed scale gives a0² = κ² c² G ρ | `scale_squared` | Definition a0 = κ c sqrt(Gρ), Gρ ≥ 0; ρ is mass-equivalent density |
| The vacuum relation gives a0² = κ² Λ c⁴/(8π) | `vacuum_coefficient` | Λ = 8πGρ/c², c ≠ 0 |
| κ = 1/2 gives the denominator 32π | `half_kappa_32pi` | κ is specified; not selected by this proof |
| The same definition admits other coefficients | `coefficient_family` | Arbitrary κ; not a no-go against a future additional selection principle |
| Circular motion in the ideal deep law yields V⁴ = G M a0 | `baryonic_quartic` | V²/r = sqrt(a0 GM/r²), G > 0, M ≥ 0, a0 ≥ 0, r > 0 |
| Real mass reproducing a chosen spherical boost has Mc = (ν−1)Mb | `target_mass_unique`, `target_mass_sufficient` | Newtonian spherical enclosed-mass relation; ν is its value at that radius |
| The enclosed target is nonnegative exactly when ν ≥ 1 | `target_mass_nonnegative_iff` | Mb > 0; nonnegative enclosed mass does not guarantee nonnegative local density |
| A linear enclosed-mass tail has constant derivative A | `tail_mass_derivative` | Exact ideal profile Mc(r) = A r − Mb; actual `HasDerivAt` proof |
| The spherical density of that tail is A/(4πr²) | `tail_density` | The spherical reconstruction equation 4πr²ρ = dMc/dr, r ≠ 0 |
| A finite supply bounds the tail radius by (S+Mb)/A | `supply_radius_bound` | A > 0 and Mc(r) ≤ S |
| That tail cannot hold at all positive radii with finite supply | `no_finite_supply_for_infinite_tail` | A > 0, fixed real supply S; constructs a violating radius |
| An additive force absent from lensing produces a dynamics/lensing residual | `nonlensing_residual`, `matched_lensing_forces_zero_extra` | The specified additive equations; exact equality is idealized, not an empirical likelihood |
| Equal and opposite component exchanges conserve their sum | `exchange_conserves_total` | Abstract componentwise divergence values; no tensor calculus formalized |
| A receiver with zero divergence cannot receive nonzero exchange | `passive_vacuum_no_exchange` | Zero divergence and the exchange equation are hypotheses; deriving vacuum divergence from metric compatibility is outside this file |
| The stated response-energy expression is nonnegative | `response_energy_nonnegative` | Nonnegative coefficients, squared mismatch and amplitude; not stability of the full gravitating theory |
| Positive linear and quadratic mass laws cannot agree at two distinct positive masses with universal coefficients | `distinct_mass_scalings` | Exact asymptotic models and shared coefficients; not exclusion of an uncomputed crossover |

There are 18 theorem declarations. The interpretation of an infinite tail is deliberately limited: a real halo may truncate, change profile or exchange material. The theorem excludes only keeping the ideal linear mass law at every positive radius under a fixed finite bound.

## Verification

The existing repository environment supplies Lean 4.34.0-rc2 and Mathlib pinned by `fable_independent_2026/lean_2026/lake-manifest.json`. This package does not alter that environment or another researcher's source files.

From the repository root, the narrow compilation command is:

```bash
cd fable_independent_2026/lean_2026
lake env lean -j 1 ../../sol61_push/gravity_architecture_lean_2026_10_12/Architecture.lean
```

For compilation, axiom inspection and negative controls together, create a fresh directory under this package and run `python3.11 sol61_push/gravity_architecture_lean_2026_10_12/verify.py PATH_TO_FRESH_DIRECTORY`. The driver uses the existing Lake environment, compiles sequentially with one Lean worker, and imposes a 180-second timeout on each invocation.

Every theorem has a `#print axioms` report. The driver requires all reports and permits only the standard dependencies `propext`, `Classical.choice`, and `Quot.sound`. It rejects additional axioms, admitted proofs, missing reports, compiler errors, and main-build warnings. This is kernel checking through the installed Lean toolchain; no independent compiler or external referee is claimed.

Three negative controls alter the source in the output directory only:

1. Replace the final 32π denominator by 16π.
2. Replace the derivative A by 2A.
3. Remove the mass-supply hypothesis from the radius-bound theorem.

Each damaged file must be rejected by Lean. These controls check sensitivity of the proof workflow; they do not replace the proofs or validate the astrophysical premises.

`contract.json` specifies the reproducibility contract. A completed evidence run records actual commands, input hashes, dependency configuration, logs, and results in `run/`. A manifest validator checks those records against the current files. See the run results rather than inferring execution success from the presence of this README.

## Not certified

- The Einstein equations, geodesic equations, weak-field metric reduction or spherical reconstruction from differential geometry.
- The physical existence, abundance, production history or interactions of the proposed cold carrier.
- A covariant action yielding the galaxy selector, metric coupling and energy receiver.
- The microscopic fermion calculation, crossover, cosmological perturbations or global stability.
- The empirical adequacy of the galaxy law, fitted κ, dataset processing or model comparisons.
- A complete account of gravity, quantum gravity or black-hole interiors.

The certificate therefore reads **“these mathematical implications follow from these stated premises”**, not “the universe implements those premises.”

## Mechanism continuation

The subsequent [edge-transport calculation](../edge_transport_2026_10_12/REPORT.md) tests a fluctuating escape level, a nonzero diffusion floor, and replenishment at an absorbing boundary. Its 13 additional Lean theorems certify conditional spectral/current algebra; its numerical checks and stochastic-calculus interpretation are recorded separately. It narrows a kinetic completion's boundary requirements without supplying the missing microscopic selector.
