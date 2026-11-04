# Corrected Gaussian epsilon scan

Date: 2026-11-04. Explicit user authorization: scan epsilon with the corrected
filter, keep everything else fixed, and determine whether Milky Way and
Cassini have a common allowed interval.

## Fixed model and question

    Phi = N rho + S* Phi_ph[S rho],
    xi = epsilon sqrt(G M_b/a0).

Reuse the reviewed KT33 operator, simple nu, both acceleration footings,
external field, Solar mass, all 1,375 original allowed baryon models per
footing, and the original observational cuts. Keep the original Milky Way
log-width quantization of 0.005. Width remains fixed within each controlled
source problem and source variation. No other parameter is adjusted.

This is an explicitly authorized parameter scan, not a blind test or a new
derivation of epsilon. It tests this Gaussian prescription and baryon family;
it cannot by itself exclude all nonlocal or Gaussian-filter theories.

## Tasks

- [x] Cassini: broad signed-quadrupole scan, including plain epsilon=0,
  small positive widths and large widths; locate every observed ceiling and
  sign crossing; refine roots with independent density/flux integrals.
- [x] Milky Way: verify epsilon=0.5 against KT33, scan all original cells,
  resolve numerical filtering at small widths, and refine candidate windows.
- [x] Coverage: use exact width breakpoints near any possible overlap,
  preserve failed numerical gates, and distinguish sampled intervals from
  exhaustive quantized intervals or analytic conclusions.
- [x] Independent review: audit the model, constants, numerical resolution,
  coverage and scope of any exclusion claim.
- [x] Integration: validate run manifests and source hashes; save joint
  interval comparison, code, results, and a final report.

## Numerical contract

Initial Cassini range: zero plus logarithmic positive widths 1e-3 through 10,
with adaptive root/shape refinement and justified tail checks. Initial Milky
Way range: zero and representative widths 0.1 through 2, extending/refining
where the Cassini result or a possible Milky Way pass requires it. These are
starting probes, not promises of continuum coverage. Exact executed lists
and selected subsets belong in each run's contract and result.

Use numerical refinements rather than change any physical input. The harmonic
order required for a narrow Gaussian may exceed KT33's epsilon=0.5 settings;
an unresolved filter cannot produce a trusted observational label. Preserve
volume adjoints, mass and potential-gauge invariants, quantify negative
truncation tails, and check all candidates near decisions at finer spatial
resolution. No monotonicity is assumed from smoothing alone.

Each worker establishes code, an explicit bounded command and a computation
contract before execution, pins code/data before and after, and retains its
outputs and manifest. All original KT33 and earlier files remain unchanged.
Numerical-library threads are one. No address-space cap is requested because
the host rejected that limit in KT33; CPU/wall/log bounds remain explicit.

## Quantization and interpretation

For one cell let R_M=sqrt(G M_b/a0). Its width equals exp(0.005 k) when

    exp(0.005(k-1/2))/R_M < epsilon
        < exp(0.005(k+1/2))/R_M,

with Python round-to-even at exact ties. Evaluating one representative of
every intersecting bin gives finite exhaustive coverage for that cell on a
bounded epsilon interval, subject to numerical accuracy. Different cells
have different R_M; a single shared epsilon list does not automatically
cover all their bins. Boundary membership must be reported explicitly.

If no overlap is found, report the actual searched range and unresolved
coverage limitations. A practical rejection of the specified route is
different from a theorem over every positive epsilon and every possible
Gaussian gravity model.
