# First same-action finite-wavelength transfer run

2026-09-11; base 2aec794b2ad8da6c60e4a959e70480ba441c76bb.
Status: **bounded numerical checks passed; full theory OPEN**.

The previously algebra-only [handoff](FIRST_ORDER_HANDOFF.md) is now
implemented in [transfer_evolve.py](transfer_evolve.py). It evolves all six
independent initial scalar/matter basis modes, rather than selecting a
particular growing mode. These normalized columns are linear transfer
coefficients, not claims that order-one nonlinear perturbations are physical.

The same frozen action, coefficient histories, sourced background and
minimal ordinary matter coupling are used. Neither the original action
code nor the coefficient functions were edited. Carl Zimmerman's
primordial-clock/global-scale direction motivates this test; it does not
derive his acceleration relation or introduce a local acceleration scale.

## Computation

- Physical proper time \(0\le t\le0.02\), dimensionless \(k=0.3,3,30\).
- One sourced history: initial \(a=1,\tau=0,\rho_b=0.001,\rho_r=0.01\);
  the original two background constraints determine physical \(H,q\).
- The background clock rate is solved, not held at one.
- Integrate a \(6\times6\) fundamental transfer matrix for each \(k\), with
  DOP853 relative/absolute tolerances \(2\,10^{-10},2\,10^{-12}\).
- Solve the actual time-dependent \(4\times4\) perturbation matrix; record
  determinants and conditioning. No expected rank/determinant is supplied.
- Reject \(k=0\) before entering the divided equations; its homogeneous
  analysis remains separate.
- Reconstruct \(z,b,\alpha\), and obtain field derivatives with five-point
  time stencils at seven interior times and two stencil widths.
- Apply the ORIGINAL eight Euler equations exported by unmodified derive.py
  to those field jets. The reduced evolution equations are not substituted
  to make the derivative residuals vanish.

The lapse/Hamiltonian equation is used to reconstruct \(z\), so its small
residual alone is not independent evidence of dynamical preservation.
The differenced momentum, shear and evolution equations are stronger tests.
Both metric potentials are evaluated separately:
\[
 S=-a^2b/k,\qquad
 \Phi=\alpha-\frac{a^2}{k}(\dot b+2Hb),\qquad
 \Psi=-z-HS.
\]
Their equality is a diagnostic, not an assignment.

The additional \(P_{XXX},P_{XX\tau},P_{X\tau\tau}\) are differentiated
symbolically from the same existing P in [transfer_jets.py](transfer_jets.py).
The time derivatives include
\[
 \dot P_{X\tau}=s_0P_{X\tau\tau}+2q\dot qP_{XX\tau}.
\]
Independent five-point differences of the original evaluator verify these
jets, including off-history X, two clock rates and two field velocities.

## Results and numerical limitation

| k | Euler residual, h=0.001 | Euler residual, h=0.0005 | slip residual, h=0.0005 |
|---:|---:|---:|---:|
| 0.3 | 4.820e-8 | 1.830e-7 | 1.551e-10 |
| 3 | 1.399e-9 | 1.409e-9 | 3.305e-11 |
| 30 | 1.400e-8 | 1.750e-9 | 6.410e-12 |

Euler residuals use \(|r_i|/(1+\sum_j|A_{ij}x_j|)\), over all six columns
and the seven stored diagnostic times. Slip uses
\(|\Phi-\Psi|/(1+|\Phi|+|\Psi|)\).
Maximum background constraint residual is \(1.027\,10^{-15}\).
The perturbation matrix determinants remain nonzero at the sampled times;
their maximum recorded condition numbers are about 35.94, 15.51 and 123.00
for the three wavenumbers. This is NOT a kinetic-sign or stability test.

**At k=0.3 the Euler residual increases when the differentiation step is
halved.** These data do not establish convergence order or an interval-wide
error bound. Roundoff/differentiation sensitivity is a possibility, not a
demonstrated explanation. At k=30 the corresponding residual decreases.
All remain below the preset check thresholds: \(3\,10^{-6}\) for scaled
Euler equations and \(10^{-6}\) for momentum/slip. No tolerance was relaxed
after seeing the results. A separate tighter-integrator comparison at k=3
passes the predeclared transfer-matrix agreement tolerance; it does not
resolve the low-k finite-difference issue.

Thus this run establishes bounded numerical agreement, not full numerical
convergence. In particular it does not fix or supersede the existing
radial fine-grid tangency failure.

## What this does and does not establish

The missing finite-k integration now exists and has run. It provides
explicit time-dependent metric/clock/baryon/radiation transfer data for
this short late-epoch history. The independently reviewed matrix signs,
coefficient rates and field reconstruction agree with the handoff.

There is still NO CMB spectrum or empirical fit. Perfect-fluid radiation
does not include photon scattering, polarization, neutrino free streaming
or recombination. The normalized basis is not a derived primordial
initial-condition distribution. No early radiation-era history, no-ghost
result, exact MOND law, galaxy depletion, PPN result or full-theory closure
follows from these short runs.

Next: distinguish the low-k differentiation/precision limitation before
claiming numerical convergence; establish an admissible radiation-era
solution of the unchanged functions; then couple the verified stress
response to the full Boltzmann hierarchy. Do not refit coefficient
functions to manufacture a desired background.

## Reproduction and tests

From repository root, the exact archived child command was:

```bash
python3 -B qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/transfer_evolve.py --result-file qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/transfer_001/result.json
```

The archived run used the bounded Mathbox runner; [manifest](transfer_001/manifest.json) pins inputs, versions, output hashes and resource limits. Use a fresh result filename when repeating it. It exited 0, and manifest validation exited 0.

```bash
python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026 -p 'test_*.py' -v
```

All 17 tests passed, exit 0. The seven new tests first failed with their respective implementation modules absent. They cover off-history coefficient derivatives, the full time chain rule, logarithm-domain rejection, all-mode action residuals, k=0 rejection, and integrator-tolerance agreement.

Created: transfer_evolve.py, transfer_jets.py, test_transfer.py, test_transfer_jets.py, transfer_contract.json, this report, and transfer_001/{manifest.json,result.json,stdout.txt,stderr.txt}. Modified: REPORT.md only to link this subsequent checkpoint. Old coefficient/action sources and prior evidence remain unchanged.

Mathbox computation-audit supplied the bounded, hashed run record; independent review and mathematical self-review kept the conservation, finite-sampling and CMB limitations explicit.
