# Independent bounded review of the conditional DF2 PDE solver

Date: 2026-09-12. Verdict: **implementation and finite assertions verified in
the stated range**. The accompanying import-safe `audit_solver.py` performs
five PDE controls and independent discrete-energy differentiation. It writes
JSON to stdout for archival by the parent experiment manifest. No root solver,
test, stellar-profile, or frozen bridge-report file was edited by this reviewer.

The numerical result is not an observational PASS. Neither five controls nor
the parent's larger set of external-field solves supplies the missing
relativistic action bridge, an equilibrium distribution function, or an
aperture/selection likelihood for DF2.

## Action, Hessian, and corrected cancellation

With internal gradient \(u\) and constant external potential gradient
\(b=(0,-e)\), the corrected implementation assembles exactly
\(J(b+u)-J(b)\), where \(J(p)=(1-e^{-|p|})p\). It evaluates the difference
using

\[
 |b+u|-e=\frac{|u|^2-2eu_z}{|b+u|+e},\qquad
 \mu(|b+u|)-\mu(e)=-e^{-e}\operatorname{expm1}[-(|b+u|-e)].
\]

For fixed Dirichlet boundary data, subtracting the constant flux leaves the
weak equation unchanged. The independent discrete energy used in the audit is

\[
 E_h=\sum_q w_q\left[\frac{y_q^2}{2}+(1+y_q)e^{-y_q}-1
                   -J(b)\cdot u_q+4\pi\eta\rho_q\phi_q\right].
\]

Here quadrature weights include cylindrical radius, and the exponential
primitive is evaluated independently of the solver's primitive helper. The
Hessian block is precisely
\(\mu(y)I+e^{-y}pp^T/y\), with its continuous zero matrix at \(p=0\).
Thus it is the action Hessian, not a frozen-\(\mu\) surrogate. It is positive
definite where \(y>0\), degenerates at zero total field, and uses no \(\mu\)
floor. The audit tests one nonzero-gradient direction, not all configurations.

On a 7 by 13 mesh of extent 8, internal potential
\(-0.06/\sqrt{1+R^2+z^2}\), external field 0.15, and direction
\(\sin(0.7R+0.2z)\) set to zero on fixed boundary nodes, step \(10^{-4}\)
gives energy-gradient and energy-Hessian relative errors
\(1.51\times10^{-7}\) and \(8.95\times10^{-9}\). Direct centered
differentiation of the external-form residual gives Jacobian relative error
\(1.03\times10^{-11}\), with Hessian asymmetry below \(9\times10^{-16}\).

The first implementation stored the large total potential. The requested
weak-source case then stalled at relative residual \(6.47\times10^{-7}\):
even a constant-field zero-source calculation generated a residual equivalent
to \(3.77\times10^{-7}\) of the tiny source norm. The root corrected this
floating-point cancellation by storing the internal potential and analytically
subtracting the background flux. Independent reruns below pass the original
\(3\times10^{-10}\) convergence tolerance. The earlier failure is corrected;
it is not a remaining convergence limitation of these tested cases.

## Independent reference checks

For Plummer mass and tracer profiles with \(\eta=10^{-5}\), external field
0.5, use the analytic spherical EFD tensor factors derived in `REPORT.md`.
The full nonlinear solver should approach that linear EFD reference for this
weak source. The analytic perpendicular and parallel moments are respectively
\(2.20066538734\times10^{-6}\) and \(1.74163056388\times10^{-6}\), in
the solver's units \(a_0b\).

| Mesh; extent | Relative PDE residual | Perpendicular moment error | Parallel moment error |
|---|---:|---:|---:|
| 49 by 97; 32 | 6.66e-13 | -0.1458% | -0.1628% |
| 97 by 193; 32 | 2.84e-12 | -0.04225% | -0.04613% |
| 57 by 113; 64 | 1.45e-12 | -0.1392% | -0.1565% |

The last mesh approximately preserves the coarse mesh's central spacing while
doubling the extent. In this case the remaining virial error is mainly mesh
error. These comparisons are bounded floating-point checks, not certified
continuum error bounds.

On the 49 by 97, extent-32 mesh, the Newtonian Plummer control at
\(\eta=0.06,e=0.1\) agrees with \(\pi\eta/32\) to -0.1450% and -0.1687%
in the two directions. The isolated exponential-AQUAL control at
\(\eta=0.06\) agrees with a separate spherical radial integral to -0.2480%
and -0.2550%. Its acceleration inversion and radial quadrature use existing
solver helpers; the isolated comparator is therefore a distinct reduction,
not an independently implemented inverse law. Both PDE cases converge.

## Normalization, axis, boundary, and observable caveats

Source normalization is correct: the residual has \(4\pi\eta\rho\), its
action quadrature includes \(R\,dR\,dz\), and the virial restores the
azimuthal factor \(2\pi\). For the radius-32, half-height-32 cylinder, the
analytic enclosed Plummer mass is

\[
 M_{\rm cyl}=\frac{L}{\sqrt{1+L^2}}
       -\frac{L}{(1+L^2)\sqrt{1+2L^2}}
       =0.9988223841740158.
\]

The coarse quadrature returns 0.9988223840317998: the missing mass is the
physical profile tail outside the computational domain, not a density
normalization failure. The code appropriately leaves the virial numerator
normalized to the prescribed full mass rather than silently dividing by the
smaller in-domain mass. The source and tracer are the same supplied profile;
this implements constant mass-to-light ratio and does not model a distinct GC
selection. The stellar Sersic implementation was source-inspected: it uses
the normalized projected profile and its spherical Abel deprojection.

Axis nodes are free, implementing natural weak regularity with radial weight
\(R\). Q1 elements do not enforce a pointwise zero radial derivative at the
axis on each finite mesh; convergence remains the relevant check. The outer
external-field Dirichlet potential is a softened anisotropic point-source
asymptotic form, not an exact finite-source solution. Its unit softening is
not specific to an arbitrary supplied stellar profile. Domain checks remain
necessary, especially if the outer boundary is not externally dominated.

The reported boundary reaction sum equals total source load by partition of
unity once the free-node residual is small. This is a useful conservation
identity; it does not prove that the selected exterior boundary approximates
the physical host/environment correctly.

The virial expressions correctly calculate
\(\int\rho R\phi_R/2\,d^3x\) and
\(\int\rho z\phi_z\,d^3x\) for the internal field. They are global total
second moments conditional on equilibrium, including ordered streaming.
They cannot be identified directly with a finite-aperture, rotation-subtracted,
or sparsely sampled dispersion. Solving the static field with a spherical
stellar source also does not prove that a nonnegative stationary collisionless
distribution realizes that density in the resulting nonspherical potential.

## Reproduction and provenance

From the repository root, the final commands and observed exits were:

```bash
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 qwen_claude_field_theory/closure_2026/df2_fixed_a0_2026/bridge/audit_solver.py
# Exit 0: PASS_BOUNDED_CONDITIONAL_PDE_AUDIT; all ten checks true.

PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 -m unittest discover -s qwen_claude_field_theory/closure_2026/df2_fixed_a0_2026 -p test_solver.py -v
# Exit 0: all six tests pass.
```

The first audit-script invocation encountered a NumPy boolean JSON-serialization
error after computation; the script's output conversion was corrected and the
complete command rerun successfully. This was an audit output bug, not a PDE
or mathematical failure. The successful independent suite took about one second
on Python 3.9.6, NumPy 1.26.2, SciPy 1.11.4, with the thread settings above.
The script records the actual solver SHA-256; at this audit it was
`46fb269720b0e89e1b8ad4916906cfa9c15053c4b4fb151fccbf87f5e55f1b70`.
The parent manifest should archive the script, this report, inputs and stdout.
