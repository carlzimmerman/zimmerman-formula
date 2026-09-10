# Executed checkpoint: same-action background and principal gates

Original theory goal: **OPEN, not certified**. No derived MOND constitutive
law, kappa=1/2, full Dirac count, PPN or observational likelihood results here.

## Strongest mathematical result

The cubic clock interaction changes both the homogeneous lapse bracket and
the scalar acoustic response. Exact background-preserving changes to P and W
can be computed, but they do not preserve the original dust perturbations.
The complete formulas and hypotheses are in `README.md` and
`../cubic_principal_audit/REPORT.md`. Independent symbolic derivations agree
on the lapse source, scalar kinetic coefficient, and metric-gradient correction.

There is also an exact non-uniqueness witness: lambda(tau)(X-q²)²/2 leaves
the chosen background unchanged while changing its kinetic coefficient.
Matching that background therefore cannot derive a unique action or all its
coefficients. This is a constructive limitation on the reconstruction method,
not a theorem against all relativistic MOND theories.

## Actual finite scan, not a parameter-volume claim

For the prescribed dimensionless history and the 361 sampled epochs:

- Gamma=0 is the original zero-restoring dust control.
- Gamma=1e-6 has positive homogeneous kinetic Schur, positive homogeneous
  lapse gap, positive tau spatial coefficient and positive scalar restoring
  coefficient at every sampled epoch. Its principal c² lies between
  3.3692e-19 and 0.001269909. At a=1, c²=3.2612213e-6.
- Each of the other 11 specified nonzero gamma choices fails at least one
  listed diagnostic. Example: gamma=.001 encounters kinetic-map zeros near
  a=8.59494 and 18.01933. Gamma=3 additionally encounters lapse-block zeros
  while its kinetic map is still invertible.

These 13 selected points do **not** measure how much of all theory space is
excluded. The surviving point is not a stability theorem: no finite-k,
caustic, nonlinear well-posedness, strong-coupling or empirical certificate
follows. There is no radiation in this sample history, so early-a results
do not certify the CMB or recombination. No observational sound-speed band
was fitted. The clock interaction strength remains a free input.

## Verification record

The bounded runner completed with exit 0. All three provenance manifests
(this directory, cubic_current_audit, cubic_principal_audit) validated with
exit 0. Validation checks evidence consistency, not the physics verdict.

| Executed test | Exit | What is actually checked |
| --- | ---: | --- |
| background_variation | 0 | Action derivatives, repair, lapse source and actual Hamiltonian flow |
| homogeneous_scan | 0 | 13 couplings x 361 epochs, plus action-derived scalar principal coefficients |
| HomogeneousGap.lean | 0 | Three conditional real-algebra theorems |
| independent_current_stress | 0 | 13 exact current, stress and Ward checks |
| independent_scalar_principal | 0 | 26 exact quadratic/principal/metric-feedback checks |
| prior_ellipticity | 0 | Original uncoupled clock regression only |
| prior_lapse | 0 | Original uncoupled clock lapse regression only |

Exact test argv, working directories, stdout, stderr and exit statuses are
in `run_001/checks.json`; runner argv, limits, runtime, environment versions,
dirty-tree provenance and all input SHA-256 hashes are in
`run_001/manifest.json`. `run_001/numerical.json` contains every scan summary,
root bracket, independent-integrator residual and caveat. The two integrators
disagreed by at most 2.1268e-11 in the sampled log coordinates.

All three Lean theorems report only propext, Classical.choice and Quot.sound;
there is no sorry or added theory axiom. They formalize the normalized gap
algebra, not the entire physics. Previous clock results are not silently
transferred to the modified action.

Development note: an intermediate source-identity run exited 1 because a
SymPy substitution introduced Hdot after the Hdot replacement had already
run. The diagnostic residual was -3U(Aq+2M²Hdot+U)/(2M²). Applying the
background Hdot replacement after the source substitutions fixed the order;
the final run also checks the independent Hamiltonian flow. This was an
implementation issue, not a failed physical matching condition.

## Exact created-file scope

No previously tracked source was edited. New files are confined to:

1. `cubic_background_completion/`: `derive.py`, `numerical.py`,
   `run_checks.py`, `HomogeneousGap.lean`, `contract.json`, `README.md`,
   `RESULTS.md`; `run_001/{manifest.json,stdout.txt,stderr.txt,checks.json,
   derivation.json,numerical.json,prior_ellipticity.json,prior_lapse.json}`.
2. `cubic_current_audit/`: `derive.py`, `REPORT.md`, `contract.json`,
   `run_001/{manifest.json,stdout.txt,stderr.txt}`.
3. `cubic_principal_audit/`: `derive.py`, `REPORT.md`, `contract.json`,
   `run_001/{manifest.json,stdout.txt,stderr.txt}`.

All paths are under `qwen_claude_field_theory/closure_2026/clock_response_repair_2026/`.
Unrelated preexisting and concurrent working-tree files were preserved.

## Next unavoidable calculation

Obtain the full finite-wavelength constrained quadratic action, not just its
high-frequency principal part, on a radiation-containing background from the
same covariant theory. Independently obtain its sourced galactic equations
and nonlinear spatial constraint closure. A mechanism selecting the action,
the exponential law, and the numerical acceleration-scale relation is still
missing; further inverse fitting does not supply it.
