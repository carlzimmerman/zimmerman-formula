# KT38 isolated Plummer checkpoint

The predeclared five-length scan is complete. The fixed square in z=x+s² changes the weak-field limit and improves several dwarf counts relative to KT37; it does not automatically restore the original dwarf performance at galaxy-scale lengths. The table reports the unchanged global virial-dispersion screen, not complete equilibrium viability.

| Common ell (kpc) | Canonical passes | Alternate passes | Plain isolated control |
| --- | --- | --- | --- |
| 0.3 | 19/24 | 19/24 | 19/24 on each |
| 1.0 | 17/24 | 18/24 | 19/24 on each |
| 3.0 | 14/24 | 16/24 | 19/24 on each |
| 5.0 | 13/24 | 14/24 | 19/24 on each |
| 10.0 | 10/24 | 12/24 | 19/24 on each |

All five lengths (.3,1,3,5,10 kpc), both original a0 footings, original 24 objects, unchanged baryon and gas conventions, original 41 Upsilon samples from 1 to 3, and original two-sigma cuts were declared before this run. There are 9,840 distinct physical configurations, each evaluated on three radial grids. The power two is an explicit structural model choice, not an additional fitted continuous parameter.

| Object at ell=3 kpc | Lower cut (km/s) | Canonical sigma(U=3) | Alternate sigma(U=3) |
| --- | --- | --- | --- |
| Sculptor | 6.4000 | 5.482904 | 5.860002 |
| Fornax | 9.9000 | 11.893942 | 12.709914 |
| Leo I | 6.4000 | 6.322190 | 6.576050 |

At ell=3, the canonical lost plain passes are Sculptor, Carina, Leo II, Leo I and Leo T; alternate losses are Sculptor, Leo II and Leo T. Fornax passes on both footings. Sculptor fails all sampled Upsilon values on both. Leo I fails the canonical grid and passes part of the alternate grid. No continuous-Upsilon conclusion or monotonicity is assumed.

A separate physical caution is visible in the stored force diagnostics: some sampled Plummer models have a negative local total radial gradient at ell=5 and10 kpc. At ell=5, Draco, Ursa Minor and Andromeda XV show this on both footings; Andromeda XV nevertheless passes the global virial screen. At ell=10, further cases show it. No such negative gradient occurs at .3,1 or3 kpc on the evaluated grids. All integrated variances are positive. These observations were retained without imposing a new retrospective cut. A global dispersion-screen pass alone is not evidence for a positive distribution function or a complete equilibrium.

The complete A and B variation is used. Three virial forms (direct analytic force, integration by parts, and fixed-radius energy homology) are checked, along with selected finite differences of the actual new energy g²[R(x+s²)−1].

All predeclared numerical checks passed. Maximum dispersion change under radial refinement/domain enlargement: 0.000382868839 km/s. Maximum relative disagreement among the three virial forms: 1.59842615e-14. Maximum selected actual-energy finite-difference discrepancy: 1.1027022e-08. Maximum Newtonian Plummer quadrature error: 4.17128726e-07. All passing object sets agree across the three grids, the sample equals the original 24 exactly, and plain isolated QUMOND reproduces19/24 on each footing.

Scope: isolated spherical numerical coverage only. This is not an actual satellite external-field prediction, an isolation upper bound, a continuous-Upsilon exclusion, an equilibrium existence theorem, or a rejection of every generalized action. KT38 is a phenomenological functional choice within the cited general action framework, not literally Milgrom equation16 or a claimed fundamental derivation.

Evidence is in `contract.json`, `run_001/results.json` and its completed validated manifest. The analytic six-test bounded run also completed and validates. The unchanged KT37 scalar primitive is explicitly pinned as an input. See `CHECKPOINT.json` for result/source hashes, pass-set comparisons and negative-gradient rows. No KT37 files were changed.
