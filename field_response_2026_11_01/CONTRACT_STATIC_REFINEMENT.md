# Frozen A2: smaller-step continuation and branch consistency

Written before the new script or numerical execution. Root authorizes this
numerical-resolution study because nine coarse families failed on their
first nonzero continuation step. It changes only the intermediate forcing
increments, not the parent, endpoint forcing or success thresholds.

Reconstruct the same six baseline solutions with the unchanged frozen
`inputs/check_gradient.py`. Run all twelve baseline/forcing families,
including three already completed diffuse families as independent branch
consistency comparators. Use the exact fractions `j/40`, `j=0,...,40`:
`.0,.025,.05,...,1`. Thus there are exactly 492 records, counting explicit
not-attempted records following an earlier failed step. Start each family
at its own baseline; seed each next attempted step only from the previous
passing solution of that same family. Do not retry a failed step, reduce
the increment again, choose another guess or switch branches.

All mass constraints, B,k,C_s, original main domains, Plummer mass/scale,
`1e-6` solve tolerance, 20,000-node cap, independent mass/scalar/stress/
virial/source-sign tests and their thresholds remain unchanged in
`static_response.py`. The external potential is a fixed diagnostic, not a
fit. No script from a previous run is edited.

At all shared fractions `{0,.25,.5,.75,1}` with a passing coarse result,
compare central density, matter radius and quarter-density column. Report
their relative differences; `5e-5` is the prespecified numerical consistency
line, not an acceptance test on the physical sign of the response. Any
larger difference is a branch/conditioning warning and remains recorded.
Keep the full path of intermediate attempted fractions and every failure.

If newly available, repeat the original four endpoint domain/tolerance
checks (both families at baseline psi_c=.99 and both epsilon values), using
the already declared longer domain and `2e-7` refinement tolerance. No new
refinement choices are selected from results.

Store all result rows and 400-point profiles at the shared coarse fractions,
plus the last successful state before a family stops and available refined
endpoints. The coarse reference is the immutable `static_run_002/result.json`.
Use bounded runner 300 seconds wall, 240 seconds CPU, one configured
numerical thread; target RSS below 1 GB. No unsupported macOS memory/affinity
limit is claimed. The fresh command will be

    python3 field_response_2026_11_01/static_refinement.py NEW_RUN/result.json

Outcomes: converged states with independent checks are conditional static
equilibria; shared-point agreement supports numerical branch consistency.
Remaining convergence failures are inconclusive. Neither a successful
static solve nor a changed core column makes a claim of dynamical stability,
formation, kinetic accessibility, real-galaxy calibration or B/V selection.
The root's separate radial energy tests and kinetic closure audit are not
replaced or altered by this numerical study.
