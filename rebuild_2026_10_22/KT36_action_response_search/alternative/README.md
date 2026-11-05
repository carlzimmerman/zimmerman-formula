# Positive mixtures do not rescue the tested Gaussian supports

The new action-consistent alternative was tested, with the original baryons,
simple nu, acceleration footings, and observational cuts unchanged. No normalized
positive mixture of the fifteen tested Gaussian widths reaches the necessary
Milky Way local speed while satisfying the inherited Cassini quadrupole cut,
when evaluated using the stored component arrays. This is an exact reduction
over mixture weights applied to numerical component data, not an exclusion of
arbitrary real widths or a rigorous continuum error bound.

| Footing | Best two widths | Weight on first width | Maximum local speed | Refined selected speed | Required minimum |
|---|---|---:|---:|---:|---:|
| canonical | .50, .55 | .6492865551 | 216.934586 | 216.949794 | 219.9 km/s |
| alt | .55, .60 | .1248284482 | 218.195228 | 218.209629 | 219.9 km/s |

The weights shown put the fresh numerical Cassini ratio at equality. Both
maxima occur at original baryon index 1350. The selected finer-grid checks
remain below the local-speed threshold by 2.950206 and 1.690371 km/s.
Consequently these selected mixtures also fail the complete set of four cuts.
Passing a local-speed test would by itself have been insufficient.

## Action and parameter accounting

For fixed Gaussian operators S_j, define

    E_mix[rho] = E_N[rho] + sum_j w_j E_ph[S_j rho],
    w_j >= 0, sum_j w_j = 1.

Variation gives

    Phi_mix = N rho + sum_j w_j S_j* Phi_ph[S_j rho].

Each continuum isotropic Gaussian is self-adjoint; the numerical implementation
retains its exact weighted adjoint. No term has independently selected source
and outer widths. This is a sum of separate nonlinear energy terms: applying a
single mixed filter inside one nonlinear energy is a different model.

The two-scale model has three shape parameters, two widths and one independent
weight; k components have 2k-1 before any additional restrictions. Normalization
preserves the isolated asymptotic deep-MOND coefficient because each finite
Gaussian component has the same total mass. It also makes the full potential a
convex combination of the component full potentials. As in KT33, each width is
fixed during source variation; this construction does not derive a global,
state-dependent width prescription. It establishes variational reciprocity,
not a relativistic completion or a dynamical stability proof.

## Complete finite weight coverage

The support is exactly

    0, .1, .15, .2, .25, .3, .35, .4, .45, .5, .55, .6, .75, 1, 2.

For each fixed baryon cell let v_j denote its component local circular speed.
The local radial acceleration is linear in the potential, so

    v_mix^2 = sum_j w_j v_j^2.

All fifteen freshly computed signed Cassini signals are negative on each
footing. Writing c_j=abs(Q2_j)/ceiling therefore gives the single linear
constraint `sum_j w_j c_j <= 1`. Positive weights cannot use sign cancellation.

A linear objective over `w>=0`, `sum w=1`, `sum c_j w_j<=1` attains a maximum
at a vertex. An inactive Cassini constraint gives a passing singleton. An active
constraint has at most two positive components: with three, a nonzero direction
preserving both equalities exists, contradicting extremality. With one failing
component i and one passing component j, its unique crossing weight is

    w_i = (1-c_j)/(c_i-c_j),   w_j=1-w_i.

Enumerating every such vertex covers mixtures with arbitrarily many components
supported on this finite set. There are 55 canonical and 48 alternate vertices,
evaluated over all 1,375 original cells on each footing: 141,625 cell-vertex
evaluations. The maximum remains the same under the relaxation that permits
each component to use a different baryon cell.

An independent algebraic bound checks the numerical convex envelope. For every
stored cell and tested component, the squared speed obeys `v_j^2<=A+B c_j`
within recorded floating precision, with positive B and these supporting lines:

| Footing | A [(km/s)^2] | B [(km/s)^2] | sqrt(A+B) [km/s] |
|---|---:|---:|---:|
| canonical | 44118.00304160536 | 2942.6115474839853 | 216.934586 |
| alt | 44707.59977036736 | 2901.5578121515796 | 218.195228 |

Multiplying by positive weights and summing yields `v_mix^2<=A+B` whenever
Cassini passes. The checked per-width slack is saved in the refinement result.
This dual check does not turn approximate component data into exact physics.
If every stored component speed is increased by 1 km/s before optimization,
the finite maxima are still only 217.934578 and 219.195224 km/s. That allowance
is a sensitivity check, not a certified error estimate.

## Numerical verification and remaining limits

Fresh Cassini component calculations use the unchanged corrected KT33 flux
implementation, 20,000 radial by 400 angular points, and radius `[1e-8,1e6]`.
Signed values, flux/density discrepancies, and the finite surface term are
retained. This experiment inherits the quadrupole-only observational convention
and does not perform an ephemeris fit.

The exhaustive weight optimization imports KT34 component arrays. The low-width
arrays use a coarser grid and some fail the angular approximation's negative
mass gate; the high-width arrays use refinement 2. Therefore the entire stored
population optimization is an exploratory numerical statement. It is not a
validated exclusion of all physical mixtures even on this finite support.
The optimum happens to use only the broad, accepted high-width components.

Both selected maxima were replayed as literal mixtures of full potentials at
`(refine,lmax,filter_radius)=(2,96,120),(3,128,120),(3,128,600)`.
The largest component negative-mass fraction is below 2.27e-9, all source-mass
relative errors are below 1e-10, and each mixture fails L1. The local squared
speed affine identity agrees within 8.95e-10 (km/s)^2; the outer-curve squared
speed identity agrees within 1.21e-9 (km/s)^2. Signed-force linearity is checked
through the stored vertical observables on this selected input. Increasing the
filter radius from 120 to 600 kpc shifts local speeds by under 3.3e-9 km/s.
These are observed refinement differences, not rigorous error bars. They do
not prove that another cell becomes no larger on a finer grid.

The useful discriminator is the convex-envelope test: another positive-mixture
proposal must supply component response points that lift this envelope above
the unchanged MW threshold while maintaining the signed Cassini budget. Merely
adding more weights on the tested components cannot help. Changing nu, allowing
negative coefficients, changing the object-width rule, or supplying new widths
would be distinct hypotheses requiring new tests. Negative coefficients are
outside this positive-action-mixture experiment.

## Evidence and reproduction

All original files are read-only. The new runs have no random sampling and use
Python 3.9.6, NumPy 1.26.2, SciPy 1.11.4. CPU/wall/log/thread caps are recorded;
no memory or CPU-affinity cap is claimed. Both v2 manifests validate against
current before/after input hashes and output hashes.

| Contract | Result | Status | Program runtime |
|---|---|---|---:|
| contract_scan.json | scan_001/results.json | completed, manifest validated | 3.76 s |
| contract_refine.json | refine_001/results.json | completed, manifest validated | 15.38 s |

The programs are `mixture_scan.py` and `mixture_refine.py`. Exact argv arrays are
in their manifests. For a reproduction choose a fresh run directory, pass the
matching contract and every listed execution artifact to the installed mathbox
`run_experiment.py`, and execute the corresponding program with
`--output <fresh_run>/results.json`. Scan caps are 180 seconds wall /160 CPU;
refinement caps are 240 seconds wall /210 CPU. Both use a 1 MiB combined-log cap
and one numerical-library thread. Validate with:

    python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py MANIFEST --root "$PWD"

The outcome is **finite assertion verified conditional on numerical resolution**;
the full mixed-resolution population optimization remains exploratory, and only
its two maximizers received the selected accepted numerical replay.
