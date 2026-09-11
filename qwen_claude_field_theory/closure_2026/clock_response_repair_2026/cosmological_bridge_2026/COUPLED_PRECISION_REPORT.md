# Joint high-precision evolution — bounded numerical advance, theory OPEN

Starting commit `9906b1b87635e1768ac0d6c52fdd7d17cbd2b8f8`; 2026-09-11.

## Result

The original eight Euler-equation residuals now decrease across six step
refinements of a joint high-precision evolution. The action, coefficient
functions, physical initial conditions and six initial perturbation modes
are unchanged. This supplies a working numerical alternative for the short
low-k test, not a proof of global convergence or CMB viability.

| Integration step | Maximum scaled Euler residual |
|---|---:|
| 0.002 | 4.1614e-6 |
| 0.001 | 7.1198e-7 |
| 0.0005 | 5.4022e-8 |
| 0.00025 | 4.3513e-8 |
| 0.000125 | 1.6822e-8 |
| 0.0000625 | 3.0516e-9 |

At the finest step, independently differentiated metric reconstruction gives
scaled momentum residual `5.264e-14` and scaled Phi-minus-Psi `1.268e-14`.
Sampled absolute background-constraint residual is `2.013e-16`.
The first three refinements agree at 40 and 50 digits in the reported
binary64 diagnostics. The three finest steps were run at 40 digits.
The ratios are not a uniform convergence order; no such order is claimed.

## What changed, and what did not

[coupled_precision.py](coupled_precision.py) integrates a 45-component state:
three barred coefficient variables, six physical background variables, and
36 transfer-matrix entries. If the original coefficient history satisfies

\[
 d\bar c/d\tau=F(\bar c),
 \qquad d\tau/dt=s_0,
\]

the joint system uses `d(bar_c)/dt = s0 F(bar_c)`. This is the chain rule,
not a newly reconstructed coefficient history. The original action-derived
3x3 background solve and 4x4 perturbation solve are reused unchanged.
No particle CDM, local a0, extra coefficient, or fitted target is introduced.

The new integrator is mpmath RK4 with cubic Hermite interpolation. All three
histories are evolved together, eliminating nested float64 interpolation.
Several parameters and the initial constraint root remain seeded from their
original binary64 values; this is not exact-rational initial data.

At `t=0.00413,0.01037,0.01591`, each interpolation segment is locked before
mpmath differentiation. No sample is a knot; the closest distance in the
finest runs is `5e-6`. First and second derivatives of all reconstructed
fields are inserted into the unmodified action-derived Euler matrix.
Phi and Psi are constructed separately. No equation assigns their derivatives
to force a vanishing residual. The integration and algebraic reconstruction
still use a reduction of these same field equations: this is a consistency
and refinement check, not an independent derivation of the theory.

This changes precision, integrator and joint-history organization together.
It does not isolate the separate contribution of each change, retroactively
validate the previous DOP853 residual, or repair the radial 129-to-257 failure.

## Verification, limits and next step

**26 Python tests passed, exit 0**, including two new tests written before
implementation. The new test checks cubic interpolation/derivatives and a
predeclared decreasing-Euler-residual criterion; no threshold was relaxed.
All three archived computations and provenance validations returned exit 0.
The source-pinned manifests contain commands, inputs, limits and result hashes.
An independent code review found no indexing or clock-time-chain defect.

**Full theory remains OPEN.** These are three sample times, one dimensionless
wavenumber `k=0.3`, and the short interval `[0,0.02]`. There is no interval
error bound, all-k stability result, CMB spectrum, exact MOND construction,
or new Lean proof. Existing conditional Lean algebra is not a certificate
of these numerical results.

Next: transport this joint system onto the demonstrated backward
radiation-majority branch and check finite-k growth and kinetic/gradient
health before any acoustic-peak or galaxy claim. The action coefficients
must remain unchanged. Carl Zimmerman's primordial-clock/global-scale target
remains the motivation; this is a numerical improvement, not new physics.

The computation-audit workflow required source-pinned runs and distinguishing
sampled improvement from a universal proof. Exact commands and changed-file
inventory are in [COUPLED_PRECISION_COMMANDS.md](COUPLED_PRECISION_COMMANDS.md).
