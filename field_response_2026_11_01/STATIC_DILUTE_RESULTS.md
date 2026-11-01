# Dilute controls: resolved static contraction in three full families

The frozen dilute controls use `psi_c=.2,.4,.6` at the same `epsilon=.01`,
with the same parent coefficients and waterbag level. Each forcing path
preserves its own initial dark mass. The Plummer forcing fractions and
scales are unchanged from the dense tests; no response was fitted.

`static_dilute_run_001` contains all 246 records: 173 passing states
(6 zero, 167 nonzero), 3 nonconverged attempts and 70 explicitly skipped
states after failure. Its evidence manifest validates with status **failed**
because not every requested forcing state converged. All three baselines,
the Plummer controls and all reported material-core mass checks pass.

Three families reach their full prespecified forcing:

| Initial psi_c | Forcing | C_q/C_q0 | n_c/n_c0 | R/R0 | M_dark(<rq0)/Mc0 | r(Mc0)/rq0 |
|---:|---|---:|---:|---:|---:|---:|
| .2 | diffuse | 1.08158830 | 1.12670655 | .96550759 | 1.05696637 | .96443905 |
| .2 | compact | 3.03708403 | 7.04564853 | .72655225 | 1.43026827 | .68562066 |
| .4 | diffuse | 1.10892302 | 1.17471034 | .96001525 | 1.07159018 | .95646727 |

Here `rq0` is the initial quarter-density radius and `Mc0` is the original
dark mass inside it. Thus `r(Mc0)` tracks the same dark mass after forcing,
separately from a moving quarter-density threshold. The full compact `.2`
case contracts this material-core radius by about 31.4%, while its
density-defined quarter radius contracts more strongly, to `.43105812`
times its initial value. The two measures must not be conflated.

All 167 passing nonzero dilute states increase the measured column and
decrease the radius containing the original core mass in this finite sample.
This differs from the three completed diffuse dense-branch families.
Concentration and the state being continued therefore matter; the earlier
dense failures cannot justify a statement that the entire chosen parent
fails to produce static baryonic contraction.

The remaining paths have these frozen last-passing/first-failing fractions:

| Initial psi_c | Family | Last passing | First failing |
|---:|---|---:|---:|
| .4 | compact | .325 | .350 |
| .6 | diffuse | .825 | .850 |
| .6 | compact | .025 | .050 |

Their failures exhaust the BVP mesh budget and remain numerical
inconclusiveness, not located physical endpoints, nonexistence or instability.
No additional step, tolerance, domain or initial-guess scan was performed.

Across passing nonzero cases, maximum errors are `8.09e-8` (dark mass),
`5.74e-8` (Poisson enclosed mass), `1.36e-9` (scalar integral), `1.39e-7`
(independent anisotropic stress derivative), `8.66e-11` (virial) and
`4.40e-8` (self-gravity energy identity). The additional original-core
mass checks agree with slope-minus-Plummer enclosed mass within `1.67e-9`;
the solved material mass target agrees within `4.22e-15`.

The run took 5.18 seconds, reported 249,004,032 bytes macOS peak RSS, and
produced about 1.11 MB of artifacts. Input hashes stayed unchanged and the
manifest validates. The author has self-reviewed the derivation and checks;
independent review and the root's energy screens remain separate.

`endpoint_reconstruction.py` provides a bounded-run helper for those screens:
`reconstruct_endpoint(pc,family)` rebuilds the exact `.025` path to a saved
passing endpoint and returns the full SciPy BVP, baseline BVP, records and
numerical agreement. It performs no scientific work on import and no energy
calculation. It was syntax-checked here but not executed by this subtask.

These are conditional static equilibria. None of the present results alone
establishes fluid or collisionless kinetic stability, dynamic accessibility,
formation, an observed galaxy response, or the microscopic normalization B/V.
