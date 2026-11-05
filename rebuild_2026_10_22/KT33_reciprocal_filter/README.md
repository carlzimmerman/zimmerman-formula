# KT33: reciprocal filter at the existing KT25 parameters

**The fixed epsilon=1/2 window does not survive.** The corrected map fails
both the Milky Way and Cassini tests on both footings. No physical parameter,
baryon prior, observational cut, or external field was fitted or changed.

The implemented map is

    Phi[rho] = Phi_N[rho] + S* Phi_ph[S rho],

with the existing simple nu and fixed Gaussian width for each controlled
source problem. The Milky Way implementation uses the volume-weighted adjoint
and a force derived from a discrete energy. Cassini uses the Hessian of the
Gaussian-convolved Poisson Green function. The Newtonian contribution remains
unsmoothed. Original lanes and outputs are unchanged.

## Results

The original Milky Way parameter grid contains 1,375 in-prior configurations
per footing. Both the initial scan and the complete doubled-resolution scan
give **0/1,375 passing on each**; no configuration passes the outer
rotation-curve cut L3. The final scan uses 96 angular cells, twice the radial
resolution, and even Legendre modes through 48. The values below are from
that completed scan, with selected triple-resolution comparisons below.

| Test | Canonical | Alternate |
|---|---:|---:|
| Original KT25 Milky Way passing count | 9 / 1,375 | 78 / 1,375 |
| Corrected Milky Way passing count, final complete scan | **0 / 1,375** | **0 / 1,375** |
| Corrected best Milky Way rotation-curve chi-squared, doubled grid | **183.0769** | **76.8482** |
| Unchanged rotation-curve chi-squared ceiling | 59.8925 | 59.8925 |
| Corrected Cassini abs(Q2) / ceiling | **1.09159063** | **1.61965966** |
| Corrected Cassini abs(Q2), s^-2 | 5.67627125e-27 | 8.42223022e-27 |
| Unchanged Cassini ceiling, s^-2 | 5.2e-27 | 5.2e-27 |

The source smoothing alone, evaluated with the new energy-consistent numerical
method, retains 9 canonical and 83 alternate passes on the initial grid,
and 8 and 82 on the final doubled grid. These small shifts from the historical
9 and 78 illustrate how close the old margins were to numerical errors;
they are not an improvement of the corrected model.
Applying the required outer adjoint removes every pass. All nine saved
canonical and thirty stored alternate passing configurations were also
recomputed using the literal old solver for an explicit control.

For the best saved canonical model, source-only local rotation speed is about
227.0 km/s, versus 215.7 km/s with the outer adjoint on the initial grid.
The change from the numerical energy construction alone is about 0.1 km/s.
The additional smoothing therefore removes radial support that the Milky Way
fit needed; the observed change is much larger than the discretization shift.

## A second Cassini error in the old result

The archived canonical **0.480594 times the ceiling** is reproduced as an
arithmetic control, but it is not the physical quadrupole of that smoothed
source. The integration by parts in KT16/KT25 omits a nonzero origin surface
term after the point Sun is smoothed. The physical source-only Hessian is
instead **3.69093 times the ceiling** on canonical and **5.90827** on alternate.

The reciprocal outer Gaussian removes that origin boundary contribution, and
its flux and independent density calculations agree. It reduces the physical
source-only quadrupole, but only to **1.09159 / 1.61966 times the ceiling**.
Thus it would be misleading to describe the change from 0.481 to 1.092 as
the physical effect of outer smoothing alone. The old apparent Cassini
margin was also affected by an integration error.

The full derivation, signs, both controls and numerical values are in
[cassini/README.md](cassini/README.md).

## Accuracy and checks

- Cassini was evaluated with two independent integral forms at four radial,
  angular and domain settings. The corrected values change by less than
  7.4e-14 relatively across those settings; seven unit tests and 22 structured
  checks pass. This is empirical numerical stability, not interval certification.
- Milky Way reciprocal response, volume-weighted adjoint, mass, constant
  potential, Newtonian and zero-width controls were checked. The anisotropic
  Gaussian convolution has an independent closed-form benchmark and converges
  under refinement.
- The best corrected Milky Way chi-squared changes from 183.0769 to 183.4150
  on canonical, and from 76.8482 to 77.0125 on alternate, going from double to
  triple spatial resolution. Both remain well above the 59.8925 ceiling.
- Extending the outer domain on the identical inner lattice changes those
  chi-squared values by about 5e-10. This tests the finite energy's distant
  surface contribution separately from changes in grid spacing.
- The first angular approximation failed its small-negative-density-tail
  check. Increasing the angular expansion reduces the checked negative mass
  fraction below 3.2e-6 across all 2,750 production sources without clipping,
  and below 3e-8 for the tripled-grid
  best candidates. Predictions are stable under this increase. The initial
  failed validation is retained, not relabelled as a pass.
- Adding a large constant potential changes forces in the observed radial
  region by less than 1e-9 in solver units. A scale-aware roundoff tolerance
  replaces an inappropriate radius-independent absolute test at the tiny
  innermost cells. This tolerance is a numerical check, not a formal bound.
- An independent periodic spectral implementation reproduces the prior
  analytic reciprocity counterexample, repairs the unequal responses, and
  cancels net force for the tested nonspherical multi-mode source in a fixed
  external field. It is a separate operator check, not a substitute for
  isolated-boundary convergence. The density itself is inversion-even; the
  fixed external field breaks the system's inversion symmetry.

The old gas-mass check's factor of two is reproduced and diagnosed as
half-space accounting: twice the represented half-grid mass agrees with the
full analytic gas mass. Neither the baryon normalization nor the width's
mass input was altered to achieve this agreement.

## Implementation and evidence

- [DISCRETE_ENERGY.md](DISCRETE_ENERGY.md): continuum and finite energy,
  weighted transpose, boundary qualification and fixed-width scope.
- [mw/mw_reciprocal.py](mw/mw_reciprocal.py): import-safe Gaussian and Milky Way
  solver. Use the documented final settings, not the quick pilot defaults.
- [mw/README.md](mw/README.md): full method, unchanged parameters and cuts,
  force components, numerical checks and reproduction instructions.
- [mw/grid_refined_run/results.json](mw/grid_refined_run/results.json): final
  complete doubled-resolution scan of all 2,750 configurations, using
  `--mode grid --refine 2 --lmax 48 --cut 120`.
- [mw/grid_run/results.json](mw/grid_run/results.json): complete initial scan,
  per-cell force profiles and all original cuts.
- [mw/final_checks_run/results.json](mw/final_checks_run/results.json): accepted
  numerical checks, refined candidates and boundary comparisons.
- [mw/audit_run/results.json](mw/audit_run/results.json): every production
  source, width, population membership and recalculated score checked.
- [cassini/cassini_v2.py](cassini/cassini_v2.py): supported Cassini implementation.
- [cassini/run_002/results.json](cassini/run_002/results.json): signed
  quadrupoles, corrected and archival controls, all quadrature refinements.
- [validation/run/results.json](validation/run/results.json): independent
  periodic operator checks.

The primary runs have bounded-execution manifests recording input hashes before and
after, Git/dirty state, commands, software, timing, limits and output hashes.
Initial unsuccessful runs are preserved: unsupported memory-limit launch,
the coarse angular/gauge validation, and a Cassini exact-zero assertion
against negligible roundoff. Their status is explicitly unsuccessful even
when the evidence records themselves validate. The final computations use
the accepted numerical settings and separate completed manifests.
The small independent-review probes instead have the narrower provenance
record in `validation/independent_review/provenance.json`; they are archived
byte copies of the actual review computations, not newly rerun experiments.

[REVIEW.md](REVIEW.md) records the independent code and mathematical review.

## Scope of the conclusion

This rules out the tested fixed-parameter completion of the KT25 window under
the inherited observational assumptions. It is not a universal no-go theorem
for nonlocal gravity or all Gaussian widths. Epsilon remains 1/2 and the
canonical/alternate accelerations remain separate. The width is held fixed
inside each controlled source problem; a common unsplit-source prescription
is still absent. Kappa=1/2 remains fitted; this does not derive kappa or
epsilon. No corrected dwarf, SPARC, cluster or cosmology scores are
claimed. No owner decision, seal, or retired research branch was changed.
