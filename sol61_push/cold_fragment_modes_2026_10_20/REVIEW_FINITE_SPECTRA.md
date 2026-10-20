# Independent review of finite fragment spectra and natural mode sources

20 October 2026. Focused peer review of the same-action discrete backgrounds, full five-real-field operators, constrained radial test, closed-box mode identification, and natural quadratic forcing. Reviewed source bytes are pinned in `sources_review_spectra.json`. The reviewer derived the analytic operator and quadratic forces earlier, so this is an independent reconstruction check but not a blind review. No stationary, spectral, outgoing, or evolution experiment was rerun here.

**Assessment:** accept the reviewed results as finite numerical evidence for the specified modified matter action, with the scope limits below. The numerical values and normalization are consistent. A negative unconstrained radial direction is not evidence of a dynamical instability; the reported positive fixed-charge energy test and localized quadrupole candidates are meaningful finite results. Neither these spectra nor a nonzero quadratic source establish a continuum stability theorem, a radiation rate, merger capture, orbital cooling, or four-dwarf selectivity.

## Same-grid stationarity and the phase identity

`radial_tools.py:22` constructs the background as a stationary point of the same radial finite-difference action later differentiated. Its three field residuals, frequency derivatives, normalized charge residual and Newton Jacobian (`:28` through `:45`) have the correct coefficients. The apparently unequal neutral cross entries in this noncanonical background Jacobian are consistent with the neutral kinetic factor one half. After transforming to canonical perturbations, the fluctuation Hessian cross entries are symmetric and contain the required sqrt(2) factors (`:74` through `:87`). The reduced gradient energy, rotation energy, potential and charge (`:63` through `:68`) use the same discrete derivative and quadrature.

Thus the phase zero restoration is obtained by relaxing each background on its own grid. It is not achieved by modifying the potential to force a preferred eigenvalue. The continuum true-origin profiles are seeds, not falsely asserted to solve the distinct discrete stationarity equations exactly. The prior high-accuracy finite-r_min failures remain separate preserved records.

The phase vector p and linear charge vector a=-Gp (`radial_tools.py:88`) have the correct canonical weights. The radial fixed-charge correction used at `grid_spectrum.py:36` is precisely `a_amp a_amp^T/||p||^2`. A common uniform dr factor cancels in this rank-one matrix; angular Y00 and background 4pi factors cancel consistently as well. It is applied only in ell=0, where the global linear charge constraint acts. This is the correct velocity-minimized quadratic-energy test, not a pointwise replacement of a potential coefficient.

## Lowest Hessian eigenvalues and dynamical scope

The shift-invert point is below a justified pointwise matrix-potential bound. Adding the radial positive derivative operator and centrifugal term cannot lower that bound, and the fixed-charge update is positive semidefinite. Therefore the symmetric shift-invert procedure targets the actual lowest eigenvalues of each finite matrix. Its Sherman-Morrison update is consistent with the symmetric matrix inverse.

At L=60, dr=.05 the primary records give:

| Q | Unconstrained radial amplitude minimum | Fixed-charge radial minimum | ell=1 amplitude minimum | ell=2 amplitude minimum |
|---|---:|---:|---:|---:|
| 80000 | -0.05242205316310811 | 0.1538366263860509 | 2.954677649213977e-6 | 0.09654159167642162 |
| 160000 | -0.032316612782888665 | 0.1764949642788176 | 1.8642088734921458e-6 | 0.06270420685696587 |

The phase ell=0 minimum is at numerical roundoff, and the reported phase-vector residual is correspondingly small. Tiny signed roundoff around a symmetry zero is not a resolved physical instability. The positive ell=1 amplitude offsets shrink by approximately four when dr is halved at fixed L, consistent with translation symmetry breaking by the radial discretization. They should not be identified with an exact physical restoring frequency. The fixed-charge positive minima include box-discretized continuum levels, so their listed values are finite-box quantities, not asserted infinite-volume gap values.

The actual dynamical pencil is `W-lambda_frequency^2+i lambda_frequency G`, or the equivalent first-order block matrix in the code. The spatial Hessian spectrum alone is not a list of growth rates. Arnoldi probes near three shifts locate selected eigenvalues; they do not exhaust the full pencil. The raw small complex splittings remain useful evidence to retain, rather than erase by a stability filter. Finite energy-test results do not substitute for a continuum/domain proof or nonlinear stability argument.

## Closed-box quadrupole identification

The finest-grid selected positive-frequency modes have:

| Q | Omega | Lowest positive Psi threshold | Fraction of canonical norm at r<15 | Fraction at r>45 |
|---|---:|---:|---:|---:|
| 80000 | 0.07546765515846882 | 0.0782124701771344 | 0.9607965438528006 | about 5.45e-5 |
| 160000 | 0.055984806795658586 | 0.09048360082973983 | 0.9913622832476263 | about 6.39e-10 |

The quantities in the last columns are canonical L2-norm fractions, not energy fractions. These modes are plausible localized subthreshold candidates rather than generic box continuum levels. In particular Q80000 is only about .002745 below the first threshold, so retaining the box/localization controls is essential.

Matching the same candidate across the primary natural-source rows gives relative mode-frequency differences of `5.30e-5` for the Q80000 L40 to L60 box comparison and `6.87e-5` on dr halving; the Q160000 values are `2.82e-8` and `6.79e-5`. These comparisons support the candidate identification. They do not rigorously prove an infinite-domain isolated pole. Levels above a vacuum threshold remain reflecting-box states until an outgoing calculation gives them their proper interpretation.

## Natural-source and K/J normalization

`natural_mode_source.py:24` uses the correct no-half real-field normalization `z=A[Z Y exp(+i Omega t)+c.c.]`, with unit-normalized harmonics and reduced fields w=r z. The resulting invariant is K_mode=A^2. `:29` through `:36` evaluates the independently derived quadratic force as a polynomial in the complex modal fields, without replacing squares by moduli; the source ordering and `-r sqrt(5/(14pi))` projection are correct. The background F in that polynomial is sqrt(2)f, as required.

The explicit angular convention `partial_phi Y=-imY` in the contract/result reverses the standard harmonic index and makes the reported physical intrinsic `J=+2K/Omega` sign consistent. The circular-sideband J expression includes both charged branches and the neutral contribution correctly. The finest-grid unit-K values are J=26.501419658532473 and 35.723977887426585. There is no extra 4pi mode factor. The raw source norm-squared is nonzero and settles under grid refinement, but it is not itself a radiated power or an escape fraction: the actual overlap with outgoing open channels may be suppressed or cancel.

The selected fundamentals are below scalar vacuum thresholds, while their second harmonics open Psi+ and keep X+ and chi closed. This is a kinematic and source-level finding. An outgoing response must use the true ell=4 boundary, conserve E/Q/J with the correct signed sidebands, and distinguish link flux from continuum-amplitude flux. Positive outgoing K-power gives negative retained dK_mode/dt. Static second-order deformation and charge/frequency backreaction remain necessary for a full perturbative trajectory.

This internal mode carries spin about the fragment centre. Its loss is not yet angular momentum transfer from fragment orbits in Sextans/Draco, a mechanism creating their excitation, a population/abundance prediction, or a proof that Fornax and Leo I avoid excess mass. Every physical rate additionally needs the action-to-physical-unit bridge and a justified weak-amplitude history.

## Provenance and interpretation controls

The original `grid_run_001` and `natural_run_001` v2 manifests validate against current pinned inputs, with completed status and 79/49 reported checks. Their scripts omit an explicit ARPACK initial vector although their contracts label randomness unused. The recorded numerical evidence is still interpretable, but the solver initialization is not pinned and bitwise reproducibility is not established. Preserve those records; any deterministic initialization and additional convergence checks belong in new source/contract/run records. A high check count should not be described as a continuum proof or as exhaustive dynamical coverage.

### Deterministic v2 follow-up reviewed

New `grid_spectrum_v2.py` and `natural_mode_source_v2.py` set every ARPACK start vector explicitly to `cos(.731 arange(n))+.3 sin(1.17 arange(n))`. Their new contracts and outputs preserve the older records and accurately resolve the initialization-provenance limitation for the new runs. This controls algorithm initialization; different BLAS/platform rounding can still prevent bitwise identity. The underlying action, stationary relaxation and source formulas are unchanged.

`grid_run_002` completed with 95/95 checks; `natural_run_002` completed with 49/49. Both v2 manifests independently validated against the pinned current source/data bytes. The additional grid controls explicitly match localized subthreshold quadrupoles across boxes/meshes, bound the frequency differences by one percent, check translation-zero refinement and compare discrete energy convergence to the true-origin continuum profile. The energy-error ratios on dr halving are .2499589/.2499581, and translation-offset ratios .2499099/.2499136, consistent with the declared second-order scheme. These are finite convergence checks, not interval error enclosures or a proof of the asymptotic order for all meshes.

The deterministic mode frequencies agree with the prior values to their displayed precision: finest natural-cache Omega=.07546765515846882/.055984806795658586. The new intrinsic unit-K angular momenta are 26.501419658533962/35.723977887423096. The difference from the older values is numerical rounding. No material source, normalization, or spectral-interpretation error remains in the reviewed deterministic v2 calculation under its stated finite scope.

No action coefficient, charge target, old failed result, frozen criterion or publication was changed by this review.
