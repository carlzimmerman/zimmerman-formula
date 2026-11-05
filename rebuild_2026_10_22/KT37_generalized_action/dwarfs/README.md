# KT37 isolated Plummer dwarf checkpoint

The full Hessian variation at the Milky Way witness length ell=3 kpc passes 12/24 of the original dwarf screen on each a0 footing. Plain isolated simple QUMOND passes 19/24. This comparison uses the original baryonic profiles, gas convention, 41 sampled Upsilon values from 1 to 3, and two-sigma cuts. It is an isolated spherical diagnostic, not an external-field satellite calculation.

| Common physical ell (kpc) | Canonical a0 passes | Alternate a0 passes |
| --- | --- | --- |
| 0.03 | 19/24 | 19/24 |
| 0.1 | 19/24 | 19/24 |
| 0.3 | 16/24 | 18/24 |
| 1.0 | 13/24 | 13/24 |
| 3.0 | 12/24 | 12/24 |
| 10.0 | 5/24 | 7/24 |

The original planned four lengths were .03, .1, .3 and 1 kpc. Before the first dwarf run, the coordinator explicitly widened the test to 3 and 10 kpc after finding the provisional Milky Way witness at 3 kpc. All six are reported; this extension was responsive to the Milky Way result.

At ell=3 kpc, the seven lost plain passes on both footings are Sculptor, Sextans (I), Carina, Leo II, Andromeda I, Andromeda XIV, and Leo T. Fornax and Leo I retain narrow sampled passes; their Gaussian-model failures must not be transferred to this distinct action.

| Object | Lower two-sigma cut (km/s) | Canonical sigma at Upsilon=3 | Alternate sigma at Upsilon=3 |
| --- | --- | --- | --- |
| Sculptor | 6.4000 | 4.926369 | 5.094477 |
| Fornax | 9.9000 | 9.943660 | 10.321148 |
| Leo I | 6.4000 | 6.519875 | 6.684156 |

Canonical Fornax passes only the sampled Upsilon=3; canonical Leo I passes Upsilon=2.90, 2.95 and 3.00. Alternate Fornax passes the sampled 2.65 through 3.00, and alternate Leo I 2.70 through 3.00. Sculptor fails all 41 values on both footings. No continuous-Upsilon exclusion or monotonicity is inferred from this grid.

The exact radial reduction retains A_r−B_r′−2(B_r−B_t)/r. Independent integration by parts and a fixed-radius variation of the energy under Plummer homology check the same virial integral. Selected finite differences of the actual energy provide a further check. No negative variance was replaced by a physical zero or a passing value.

The bounded run completed with all checks passing. Across the entire six-length, two-footing sample, the maximum dispersion shift under n=1000/2000 and a doubled radial domain was 0.000402668916 km/s; the maximum direct/weak/energy virial relative discrepancy was 1.31880588e-08; selected energy finite differences agreed to 1.42474462e-08; the maximum Newtonian Plummer integral error was 4.47610788e-07. The original 24-object sample matches KT36 exactly, and the plain isolated control reproduces 19/24 on each footing.

The 24 objects, 41 Upsilon values, six lengths and two footings comprise 11,808 distinct physical configurations, each evaluated on three radial grids. These are numerical coverage statements. The results do not establish that isolation is an upper bound, that external fields can only suppress support, or that every generalized-action model fails.

Evidence: `contract.json`, `isolated.py`, `test_isolated.py`, `run_001/results.json`, and `run_001/manifest.json`. The manifest validator reports a valid completed evidence record. The analytic controls have their own completed and validated `../analytic/tests_001/manifest.json`. No historical result or original observational input was edited.

A read-only post-run consistency check also confirms identical passing object sets on all three radial grids at every length and footing, and zero invalid variances in the stored evaluations. See `POST_RUN_CHECKS.json`.
