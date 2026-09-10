# Executed finite-wavelength checkpoint

Original complete-theory objective: **OPEN**. The same reconstructed action
has passed new, explicitly bounded dynamical gates. It has not yet produced
the required exponential MOND source law, derived kappa=1/2, full nonlinear
Dirac closure, all PPN parameters, or a CMB/galaxy data comparison.

## Strongest result

After varying the full quadratic ADM action, eliminating lapse and shift,
and treating the remaining scalar constraint, one dynamical scalar remains
on the regular linear branch. The actual finite-wavelength kinetic coefficient is

    Aeff=A0-J²/(D0+D2 k²).

At the specified epoch a=1, gamma=1e-6, the action-derived coefficients reduce
to the explicit real functions in `PointSigns.lean`. Lean proves D0<0,
D2<0 and A0>0 from H>0 and H²=4/15, then positive Aeff and a nonzero
constraint coefficient for every k²>=0. The physical reduction requires
k!=0. An exact rational-interval and polynomial-remainder script verifies
the definitions against the actual action output. This is an exact
selected-epoch quadratic kinetic/constraint result, not just a finite grid.
It is not a Lean formalization of the action's variation or a nonlinear proof.

The independently varied tensor sector has two positive kinetic eigenvalues
and two luminal speeds on homogeneous clock backgrounds. Both the tensor
rank and speed are calculated from the action, with mutation controls.

The unchanged action also admits nearby regular expanding homogeneous
solutions after adding a minimal radiation-fluid proxy. That local result
is derived from the constraint Jacobian, not by replacing the original H
inside the action's coefficient functions. A full radiation history and
realistic photon/neutrino perturbations have not been solved.

## Actual runs and exit statuses

The main bounded run completed in 112.208198 seconds, exit 0, with a
cooperative one-thread cap. Both new evidence manifests validate, exit 0.
No zero exit status is interpreted as completion of the theory.

| Important test | Exit | Scope |
| --- | ---: | --- |
| finite_wavelength_action | 0 | Exact quadratic action, independent raw-action comparison, constraints and high-k regression |
| finite_wavelength_evolution | 0 | 74 profile slices; six canonical transfer maps with two solvers |
| ConstraintSchur.lean | 0 | Three conditional constraint/Schur positivity theorems |
| PointSigns.lean | 0 | Two exact selected-epoch/all-k algebra theorems |
| selected_epoch_exact_bridge | 0 | Actual Lean definitions checked against actual symbolic action coefficients |
| tensor_variation | 0 | 26 exact tensor metric/curvature/action and sensitivity checks |
| fixed_action_radiation | 0 | Nine exact identities; 28 one-epoch samples across two distinct initial-data families |
| prior_background_regression | 0 | Previous cubic homogeneous action/source/flow checks |
| prior_principal_regression | 0 | Previous 26 exact scalar-principal checks |

All five Lean theorems print only propext, Classical.choice and Quot.sound;
none uses sorry or a new physics axiom. Their scope remains the displayed
real-algebra propositions.

For gamma=0 and gamma=1e-6, all 74 sampled profile slices satisfy the
sufficient signs; separate evaluation covered 17 wavelength/Hubble ratios
per slice. The conditional algebra then covers all nonzero wavenumbers
whenever those signs hold, but numerical profile signs are not a rigorous
continuum-time enclosure. The exact selected-epoch proof is separate.

Canonical transfers at k=1,10,100 from ln(a)=-2 to 0 were integrated with
DOP853 and Radau. Maximum relative solver disagreement was
3.37131572e-11; maximum canonical transfer determinant error was
4.45956605e-11. These are arbitrary-state maps, not observed or primordial
cosmological transfer functions. There is no empirical fit or new measured
prediction in this checkpoint.

## Exact commands and files

Every important test's exact argv, working directory, stdout, stderr and exit
status is in `run_001/checks.json`. The wrapper command, limits, software
versions, source hashes and dirty-state provenance are in
`run_001/manifest.json`. These records describe the commands actually run,
not an inferred reproduction recipe. The separate radiation execution record
is `../cubic_radiation_background/run_001/manifest.json`.

All newly created files are confined to these two directories under
`qwen_claude_field_theory/closure_2026/clock_response_repair_2026/`:

- `cubic_finite_wavelength/`: `derive.py`, `numerical.py`, `tensor_gate.py`,
  `point_certificate.py`, `run_checks.py`, `ConstraintSchur.lean`,
  `PointSigns.lean`, `contract.json`, `README.md`, `TENSOR.md`, `RESULTS.md`;
  `run_001/{manifest.json,stdout.txt,stderr.txt,checks.json,derivation.json,numerical.json}`.
- `cubic_radiation_background/`: `derive.py`, `REPORT.md`, `contract.json`;
  `run_001/{manifest.json,stdout.txt,stderr.txt}`.

No previously tracked source was edited. Unrelated and concurrent work was
preserved. Development runs included an exit-1 unsimplified matrix-equality
assertion (its exact simplified residual was zero) and an interrupted,
unnecessary multivariate factorization of the potential coefficient (exit
130). The potential is now retained in exact Schur form; no physics was
removed to make a test pass. The final bounded run above uses the final sources.

## Next unavoidable connection to the original goal

Derive and solve the **nonlinear baryon-sourced galactic equations from this
same action**, retaining clock density, explicit clock dependence and time
current, and derive Phi and Psi independently. Determine whether this
candidate actually generates the target MOND law rather than merely a healthy
clock sector. Full nonlinear spatial constraint closure and radiation-era
evolution remain required too. None of these missing results is replaced by
the finite-wavelength or Lean certificates recorded here.
