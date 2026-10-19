# Self-audit of CDQ-001 and CDQ-002

Primary verdict: **proved as written** for the claim card below, with the stipulated EFT/regulator inputs. This is a same-agent self-review, not independent verification and not a verdict on the full gauge-theory or physical-QCD target.

Claim card: for each fixed positive u,kappa,L, consider the canonical compact SU2 dual scalar with smooth field configurations on round S3, no electric line insertions, one chosen stable theta branch, and a common zeta/proper-time local subtraction. At tree plus Gaussian order, its bulk-subtracted isotropic spatial metric response has lim_(R->infinity) R Delta tau_s=0. In the same regulated neutral gas, the constant 1/R part of the mean-zero Coulomb kernel cancels for every finite magnetically neutral configuration. Neither statement includes unknown geometry dependence of matched u,kappa or W_hard.

## Dependency graph and obligations

| Arrow | Evidence | Status |
|---|---|---|
| Small-circle gauge theory -> flat root/kinetic/event input | Exact v2 primary source plus direct signed-event expansion; source typos retained | Passed in stated normalization; curved matching conditional |
| Compact phi0 -> neutrality and integer topology | Fourier projection and charge table | Passed |
| Exact uniform integral -> integer-Q sum | Species Bessel expansion; finite independent quadrature/sum tests | Passed; only uniform sector |
| Canonical zero variable -> J0 and constant eigenvalue | a0=sqrt(kappa V)phi0, one real-mode measure | Passed; residual p metric independent |
| S3 harmonics -> n² spectrum | Harmonic-polynomial dimension and radial Laplacian | Passed |
| All-mode spectrum -> determinant | Finite-part resolvent, integration constant fixed by proper time/large a, independent winding and Hessian checks | Passed for prescribed scheme |
| Determinant -> spatial metric response | Fixed-m derivative; independent numerical differentiation | Passed |
| Asymptotic response -> zero 1/R coefficient | Explicit formula and bound below | Passed analytically |
| Mean-zero S3 Green function -> finite neutral cancellation | PDE, Gauss singularity, mean, antipode, exact (sum q)² identity | Passed for finite configurations at fixed distances |
| These EFT results -> full curved deformed-YM stress | Common-regulator hard/core/global matching not supplied | Conditional, first missing arrow |
| Deformed-YM product geometry -> physical Lorentzian QCD/QED/proton ratio | No derivation in scope | Out of scope, open |

For the decisive asymptotic step set x=mR, a=sqrt(x²-1), s=sqrt(1-x^-2). The bracket in D15 is

    1-s coth(pi a) = 1/[x²(1+s)] - 2s/(exp(2pi a)-1).

For x>=sqrt(2), the absolute value of R Delta tau_s is bounded by

    m²/(12pi L) [1/x + 2x/(exp(2pi sqrt(x²-1))-1)],

which tends to zero. This checks the limiting operation without invoking a generic mass-gap claim. Changes in local analytic curvature counterterms start at R^-2 and preserve this scoped limit. A hypothetical coefficient depending on R at order 1/R is excluded from the claim card and handled explicitly by D18-D19, not silently set to zero for the gauge theory.

Reviewed operations and boundaries: all-mode versus primed determinant; normalized gas versus absolute canonical scalar partition; V differentiation versus W/V; theta branch exchange and theta=pi exclusion; positive fixed m versus epsilon scaling; finite separation versus r~R; charge neutrality versus merely zero mean charge; inclusion of regular self terms; compact-cell multiplicity; source factor two and real-theta convention. No isolated uniform interaction term is appended as a complete higher-loop result.

The 60/85-digit tests are not interval-certified. Exact symbolic checks establish the stated algebraic kernel identities; numerical tail bounds apply to the declared truncations, not arbitrary many-body coverage. The serialized cross-precision statistic has only the 45-digit table precision and is not evidence for its raw tiny displayed value as an accuracy claim.

Proofread-math self-review: scope was this lane's newly authored derivation, supplement and report. Routine corrections: none after the executed inputs were frozen. Mathematical-token changes after execution: none. Unresolved mathematical issue: full curved core/hard/global matching as above. Validation: all three v2 manifests pass; full run commands in REPRODUCE.md.

Exact derivation revisions audited are content-pinned in the completed manifests and the final hash receipt. The parent coordinator may append an independent review without mutating these executed inputs.
