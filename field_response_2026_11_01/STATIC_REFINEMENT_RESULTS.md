# A2: smaller steps extend paths, with no additional final endpoint

The separately frozen `.025` grid retains the same twelve families,
parameters, endpoint forcings, physical equations and numerical thresholds.
`static_refinement_run_001` has a valid evidence manifest with status
**failed**: not all requested states/refinements converged. All 492 records
are present: 163 passing states (12 zero, 151 nonzero), 9 failed attempts,
and 320 explicitly unattempted fractions following failures.

The three full diffuse endpoints remain those in `STATIC_RESULTS.md`.
All 24 available shared coarse-fraction comparisons agree; the largest
relative difference in density, column or total radius is `3.05e-8`, below
the frozen `5e-5` threshold. The one available endpoint domain/tolerance
check also passes, with maximum relative change `2.89e-7`.

| Baseline psi_c | epsilon | Family | Last passing fraction | C_q/C_q0 there | First failed fraction |
|---:|---:|---|---:|---:|---:|
| .80 | .0001 | diffuse | .225 | .86297706 | .250 |
| .80 | .01 | diffuse | .200 | .88069386 | .225 |
| .80 | .0001 | compact | 0 | 1 | .025 |
| .80 | .01 | compact | 0 | 1 | .025 |
| .95 | .0001 | diffuse | 1 | .82433036 | none |
| .95 | .01 | diffuse | 1 | .84043811 | none |
| .95 | .0001 | compact | .100 | .69972401 | .125 |
| .95 | .01 | compact | .100 | .72214471 | .125 |
| .99 | .0001 | diffuse | .025 | 1.02374861 | .050 |
| .99 | .01 | diffuse | 1 | .80379111 | none |
| .99 | .0001 | compact | 0 | 1 | .025 |
| .99 | .01 | compact | .125 | .63279618 | .150 |

All nine remaining failed attempts hit the mesh-node budget. A failure at
the next recorded fraction is not a mathematically located branch endpoint
or a proof of nonexistence. No second reduced-step scan, predictor change,
alternative initial guess or branch substitution was performed.

One new response has the opposite sign from the three completed diffuse
families: at baseline `.99,.0001`, diffuse fraction `.025` means
`mb/M=.00125`. Its solved central `psi=.9952215243`, central density ratio
is `1.73580645`, quarter-radius ratio `.58978270` and column ratio
`1.02374861`. The next step failed. Consequently the data do **not** support
a universal claim that baryons lower this parent's static core column.
Seeding a solve from the preceding state supports a continuation attempt,
but is not an analytic uniqueness or branch-continuity certificate.

Across all 151 successful nonzero states, maximum errors are `4.41e-8`
(fixed dark mass), `3.61e-8` (Poisson enclosed mass), `9.55e-11` (scalar
integral), `1.01e-7` (independently differentiated anisotropic stress),
`1.07e-11` (virial), and `2.21e-8` (self-gravity energy identity). Plummer
controls and wrong-source-sign rejection pass. These establish the stated
finite numerical checks, not stability or kinetic accessibility.

Run time was 6.88 seconds; macOS peak RSS 209,649,664 bytes; all artifacts
total about 1.14 MB. Input hashes were unchanged and the manifest validates.
The earlier coarse code, contracts and runs were preserved unchanged.
This record makes no interpretation of the root's separate fluid or
canonical-kinetic stability screens.
