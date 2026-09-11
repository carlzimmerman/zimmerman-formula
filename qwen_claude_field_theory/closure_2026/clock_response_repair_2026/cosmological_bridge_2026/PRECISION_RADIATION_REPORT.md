# Precision isolation and backward radiation continuation — OPEN

2026-09-11; starting commit `95e61fa4e68dba1bbfc0931fdc352600748a6d89`.

## Outcome

Two bounded advances, and one explicitly negative diagnostic:

1. Re-evaluating the **same stored solution** at higher precision removes
   the small-stencil residual blow-up. The remaining error floor is not zero.
2. The unchanged action and coefficient initial-value problem reach a
   homogeneous radiation-majority branch, without a new reconstruction.
3. Finer float64 integration does **not** produce a monotonic decrease of
   the differentiated Euler residual. Full numerical convergence stays open.

These results neither establish CMB viability nor complete relativistic MOND.
No observation is rejected by this calculation. There is no new Lean theorem
or claim of a new law of nature in this checkpoint.

## 1. Isolating the small-stencil failure

[transfer_precision.py](transfer_precision.py) replays the existing DOP853
nested dense polynomials, including their original binary64 coefficients,
initial conditions, segment boundaries and source literals. It switches only
subsequent arithmetic to mpmath. The three trajectory integrations themselves
remain float64. Original arithmetic functions are cloned with a different
numeric backend; their modules and equations are not modified.

All six initial modes at dimensionless `k=0.3`, on `t in [0,0.02]`, are
checked at seven interior times. The reconstructed eight fields are
differenced with five-point stencils and substituted into the original
action-derived Euler operator. Metric derivatives are not assigned from
the momentum or shear equations. The underlying transfer system is itself
a field-equation reduction, so the entire computation is not independent
of those equations; independence here concerns the derivative check.

Maximum scaled Euler residual, across eight equations and six columns:

| Differencing step | Float64 evaluation | 50-digit evaluation |
|---|---:|---:|
| 0.002 | 1.641e-8 | 5.780e-9 |
| 0.001 | 4.820e-8 | 5.844e-9 |
| 0.0005 | 1.830e-7 | 5.948e-9 |
| 0.00025 | 1.028e-6 | 5.928e-9 |
| 0.000125 | 4.977e-6 | 5.923e-9 |

The smallest-step residual decreases by about 840 times when evaluation
precision changes. The 30- and 50-digit runs agree in their reported
binary64 diagnostics; the archive does not establish 30-digit accuracy.
At the smallest step the higher-precision scaled momentum/slip residuals
are respectively `2.620e-11` and `2.334e-11`. Phi and Psi are separately
constructed as in the preceding transfer calculation.

This isolates a major evaluation/differencing roundoff contribution.
It does **not** prove the remaining floor is exclusively integration error,
nor fix the separate radial `129 -> 257` convergence failure.

Evidence: [precision_001/result.json](precision_001/result.json), with
source hashes and bounded execution in the adjacent manifest.

## 2. The remaining numerical floor did not close

[integration_precision_probe.py](integration_precision_probe.py) reintegrates
the same coefficient history, sourced background and transfer matrix with
three maximum-step caps. It holds tolerances and physical inputs unchanged
and uses 40-digit evaluation with stencil step `0.000125`.

| Maximum integration step | Scaled Euler residual |
|---|---:|
| 0.01 | 1.372e-8 |
| 0.005 | 5.188e-9 |
| 0.0025 | 3.841e-8 |

Adjacent endpoint transfer matrices differ by at most `1.561e-13` in
absolute entries, and sampled background constraints stay below `7.1e-16`.
That endpoint agreement does not certify differentiated dense output.
The residual sequence is non-monotonic; this negative result is preserved
in [integration_precision_001/result.json](integration_precision_001/result.json).
The test suite checks that the experiment is recorded correctly, not that
it has achieved convergence.

## 3. A backward homogeneous branch with radiation majority

[radiation_probe.py](radiation_probe.py) continues the **original** coefficient
ODE backward from its original initial data. The independent variable is
the logarithm of the *coefficient* scale factor; inversion to tau is allowed
only inside its explicitly integrated interval. That scale factor is not
identified with the physical scale factor. An independent finite-difference
test checks that the reparameterized solution obeys the original tau flow.

The physical system uses `x=log(a)` and the already derived equations:

\[
 \frac{dH}{dx}=\frac{\dot H}{H},\qquad
 \frac{dq}{dx}=\frac{\dot q}{H},\qquad
 \frac{d\tau}{dx}=\frac{s_0}{H},\qquad
 \rho_b=10^{-3}e^{-3x},\quad \rho_r=10^{-2}e^{-4x}.
\]

Matter charge conservation is imposed here via exact first integrals, not
claimed as an independent numerical check. Both action constraints and the
clock scalar charge are monitored independently. The physical initial
`H,q` solve the sourced constraints. No background target is fitted.

The two runs use checkpoint steps `0.025,0.0125` and relative tolerances
`2e-11,2e-12`. Both reach the radiation-fraction target at `x=-2.30`:

\[
 a=0.1002588437,\quad H=8.107064817,\quad s_0=0.7234438362>0,
 \qquad \Omega_r=\frac{\rho_r}{3M^2H^2}=0.5019502655.
\]

At that endpoint, `rho_r=98.97129`, `rho_clock=96.50993`,
`rho_b=0.992275`, and `M^2 Lambda=0.7` in the unchanged dimensionless units.
Thus this is just beyond radiation/matter equality, **not** a demonstration
of a deep radiation era or a recombination-calibrated history. No particle
CDM is inserted, but the clock's substantial gravitating density remains.

The endpoint clock coordinate `tau=-2.298173512` lies inside the integrated
coefficient interval approximately `[-2.344261575,0]`. The relative logarithm
domain margin is `6.9813e-4`, and the actual background matrix condition
number is approximately `1.382e5`; these warrant attention on further extension.
The refined run's maximum scaled Friedmann and clock residuals are
`2.381e-13` and `9.860e-13`; relative scalar-charge drift is `1.449e-12`.
The two endpoint H values differ by `1.21e-12`. No convergence order is claimed.

Evidence: [radiation_001/result.json](radiation_001/result.json) and
[radiation_002/result.json](radiation_002/result.json).

## Status, verification and next unavoidable calculation

**Full theory: OPEN.** The action is exactly the one in [REPORT.md](REPORT.md).
Its coefficient histories were reconstructed in earlier work; freezing them
now is not a first-principles derivation. This sector still has no derived
exponential MOND operator or derivation of Carl's fitted kappa=1/2. No new
DOF, PPN, stability, galaxy-dust depletion or empirical CMB gate is certified.

The immediate numerical task is a derivative-consistent, precision-controlled
integration/diagnostic for the transfer system that resolves the remaining
non-monotonic residual floor. After that, evolve finite-k perturbations on
the demonstrated backward branch, test their kinetic/gradient health, and
add observational calibration and the photon/baryon/neutrino hierarchy.
A homogeneous radiation-majority branch alone cannot predict acoustic peaks.

Fresh verification: **24 Python tests, exit 0**; four computation runs and
their provenance validations, each exit 0; unchanged
`ConstraintPropagation.lean`, exit 0. Its four existing theorems certify
conditional real-jet algebra, not these numerical integrations or nature.
The growing integration residual is a scientific non-pass despite process
exit 0. Exact important commands and file inventory are in
[PRECISION_RADIATION_COMMANDS.md](PRECISION_RADIATION_COMMANDS.md).

Carl Zimmerman is credited for the primordial-clock direction and the
same-action/global-scale target. The computation-audit workflow motivated
separate precision and integration experiments, archived negative results,
and source-pinned evidence. No novelty or priority claim is made.
