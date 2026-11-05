# KT39 bounded power-curvature dwarf synthesis

Exactly one of the initial18choices preserves the requested auxiliary comparison of at least17/24 dwarf dispersion-screen passes on both a0 footings: p=1.75,ell=1.5kpc gives17/17. Neither of the two separately authorized adaptive choices reaches that comparison. This threshold is auxiliary; the original object-level observational cuts were never replaced.

| p | Common ell (kpc) | Canonical passes | Alternate passes |
| --- | --- | --- | --- |
| 1.25 | 1.5 | 13/24 | 15/24 |
| 1.25 | 2 | 13/24 | 13/24 |
| 1.25 | 2.5 | 13/24 | 13/24 |
| 1.25 | 3 | 13/24 | 13/24 |
| 1.25 | 3.5 | 12/24 | 13/24 |
| 1.25 | 4 | 11/24 | 12/24 |
| 1.5 | 1.5 | 15/24 | 17/24 |
| 1.5 | 2 | 14/24 | 15/24 |
| 1.5 | 2.5 | 13/24 | 15/24 |
| 1.5 | 3 | 12/24 | 15/24 |
| 1.5 | 3.5 | 12/24 | 14/24 |
| 1.5 | 4 | 12/24 | 12/24 |
| 1.75 | 1.5 | 17/24 | 17/24 |
| 1.75 | 2 | 16/24 | 17/24 |
| 1.75 | 2.5 | 15/24 | 16/24 |
| 1.75 | 3 | 14/24 | 15/24 |
| 1.75 | 3.5 | 13/24 | 15/24 |
| 1.75 | 4 | 12/24 | 14/24 |

After those results and the initial Milky Way bracket, exactly two further pairs were declared in CONTINUATION_PLAN.md and their own contract before running:

| Adaptive p | Common ell (kpc) | Canonical passes | Alternate passes |
| --- | --- | --- | --- |
| 1.125 | 3 | 12/24 | 13/24 |
| 1.25 | 2.75 | 13/24 | 13/24 |

The original plain isolated simple-QUMOND control remains19/24 on each footing. For the sole auxiliary17/17 choice, the lost plain passes on both footings are:
canonical: Leo II, Leo T.
alt: Leo II, Leo T.

There are35,424 distinct physical configurations in the initial18choices and3,936 in the adaptive2choices, totaling39,360. Each is evaluated on three radial grids. All original24objects,41Upsilon samples, gas and baryonic profiles, a0 footings and two-sigma cuts are unchanged. Both p and ell are shared searched parameters; no object-specific power or length was fitted.

All predeclared numerical gates passed in both physical runs. Passing object sets agree across every coarse/fine/expanded grid. Every stored integrated variance is positive, and no negative total radial gradient occurs on these evaluated grids. These are finite sampled statements, not global force-positivity or equilibrium-existence proofs.

| Numerical diagnostic | Initial18 | Adaptive2 |
| --- | --- | --- |
| Max dispersion refinement/domain shift (km/s) | 0.000316965263 | 0.000277220557 |
| Max direct/weak/energy virial relative difference | 3.78190936e-12 | 2.11970788e-10 |
| Max actual-energy finite-difference discrepancy | 8.29580425e-09 | 2.71963743e-09 |
| Max Newtonian virial relative error | 3.12425052e-07 | 2.40013622e-07 |

The full Hessian adjoint and analytic derivative of D=p ell²s^(p−1)xR′ are retained. Six bounded analytic controls pass across the original three powers, including reproduction of the read-only p1/p2 actions. Additional bounded controls for the adaptive power1.125 explicitly verify its slower weak-field/H-zero rates and full finite-H energy derivative, rather than imposing the faster-power tolerance at an unsuitable finite amplitude.

Limits of interpretation remain material. This is isolated spherical41-point-Upsilon coverage, without actual satellite external fields or a proof that isolation is an upper bound. No continuous parameter exclusion or monotonicity assumption is made. At fixed nonzero gradient, the energy is C² at H=0 for p>1, but B is not generally C² for p<=1.5, so the double divergence may require a weak interpretation. The uniform-field linear improvement also does not remove negative short-wave principal response on every tidal background. None of these static statements is a dynamical no-go, and dispersion-screen passes are not full equilibrium or general-health claims.

Evidence: PLAN.md and contract.json for initial18; CONTINUATION_PLAN.md and contract_continuation.json for the adaptive pairs; completed run_001 and continuation_001 results/manifests; ../analytic/tests_001 and ../analytic/continuation_001 controls; CHECKPOINT.json and ../analytic/VERIFICATION.json. No prior scientific source was changed, and no further scan was run.
