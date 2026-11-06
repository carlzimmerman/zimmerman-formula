# Independent review of the expanded adapted RHS

**Outcome: the continuum cancellation is correct.** No native evolution
term was dropped from the jet derivation. It retains the full p_lambda
time equation and uses the momentum constraint, its spatial derivative,
and the uniform-lambda gauge. The expanded form is not identically the
old collocation RHS on unresolved or off-constraint grid states. Its
use requires resolved comparisons and continued raw constraint monitoring.
This is a numerical review; the principal-formation transfer remains open.

Reviewed read-only: derive_expanded.py, expanded_rate.py, the seven-check
expanded_algebra.json, expanded_constraints.py, fft_constraints.py,
gradient_constraints.py, and the associated validation code/results.
No solver or generator files were edited. I ran only two small symbolic
residual-coefficient calculations in memory, described below.

## 1. Jet definitions and retained equations

The generator uses

    U=exp(lambda), E=exp(2beta), V3=U E, M=Mpl^2,
    c=2 M^2 E^2/p, S=2 beta_xx+3 beta_x^2,
    p_beta=r+cS, p=p_lambda.

Its spatial jet correctly sets E_x=2E beta_x and U_x=0. The starting
beta, p_lambda and p_beta time equations match the previously audited
canonical equations. In particular the full p_lambda equation is

    p_t=N Hk+N V3(F-F_D D)-Lsp+(w p)_x.

All terms in that equation enter the chain-rule expression

    r_t=p_beta,t-c(4 beta_t-p_t/p)S
        -c(2 beta_t,xx+6 beta_x beta_t,x).

No homogeneous truncation of p_t, scalar equation replacement, or discarded
matter pressure term appears. F, F_D, their needed spatial derivative,
P, P_x, and D are retained as independent symbols where appropriate.

The substitutions are exactly

    w_x=Lrate-N(p-p_beta)/(2M V3),
    w_xx=-partial_x[N(p-p_beta)/(2M V3)],
    p_x=beta_x p_beta,
    p_xx=beta_xx p_beta+beta_x p_beta,x.

Lrate denotes the spatially constant lambda_t; it is not a metric scale
factor. The derivative of p_beta in the last line includes the p_x term
inside c_x, and the sequential substitution correctly replaces that term.
After these operations the absence of N_xx and beta_xxx is a genuine
algebraic cancellation. The seven checks also verify absence of the
eliminated jets and coefficient w for r_x. Those checks alone would not
validate an incorrectly chosen starting equation, but the independent
equation comparison above supplies that missing check.

## 2. Concrete constraint-remainder identities

I independently kept a symbolic momentum residual

    Cmom=p_x-beta_x p_beta,
    Cmom_x=p_xx-beta_xx p_beta-beta_x p_beta,x

in the generator's unsimplified chain rule, imposing the gauge exactly.
The exact continuum difference is

    r_t(chain)-r_t(expanded)
      =2 M E/(U p) [N Cmom_x+2 N_x Cmom].

There are no quadratic Cmom terms. This identity is a particularly useful
comparison diagnostic: a small residual Cmom alone need not make the
expanded and unexpanded rates close when Cmom_x is large at high frequency.
Report the displayed weighted residual, or at least Cmom_x, in addition
to the existing raw momentum norm.

Separately, with momentum exact, define

    G=w_x-Lrate+N(p-p_beta)/(2M V3),
    G_x=w_xx+partial_x[N(p-p_beta)/(2M V3)].

The gauge contribution to the same difference is

    r G-4 M^2 E^2 beta_x G_x/p.

These two statements were derived by retaining each residual family in
the original symbolic expression and differentiating with respect to its
independent residual jets; no source file was regenerated. They quantify
the use of the constraints rather than assuming it is innocuous.

For sampled spectral products, add the independent discrete Leibniz-rule
errors: differentiating beta_x p_beta is not exactly the same as multiplying
separately differentiated truncated factors. Therefore these continuum
remainder formulas do not purport to account for every collocation error.

## 3. Generated code and caller

The generated CSE expression uses the correct powers of M,U,E,p and
contains no new evolution coefficient. The remaining denominators require
p to stay away from zero, as already enforced by the coordinate guard.

The caller passes physical w=ws/k, not ws, into the generated rate.
It supplies U=exp(lambda), E=exp(2beta), Lrate=lambda_t,
F_D=-1-gamma q, and (F_D)_x=-gamma q_x correctly. P_x is taken from the
authoritative gradient coordinate gvar-mean(gvar). The separately expanded
p_lambda rate uses

    (w p)_x=(Lrate-gauge_rate)p+w beta_x p_beta,

again exactly on the same gauge/momentum constraints. Thus the expanded
p_lambda rate too differs from the raw divergence form off constraint;
it should not be interpreted as an independent unconstrained extension.

No filtering or viscosity is introduced by these algebraic changes.
They choose a numerically better constrained representation of the same
continuum equations. Because constraint reconstruction and spectral
products are approximate, equivalence is demonstrated by resolved
refinement, not by equality at arbitrary finite resolution.

## 4. FFT and gradient-coordinate constraints

On the enforced odd grids, the Fourier derivative is invertible on
zero-mean modes. The mapping

    gvar=P_x+mean(P)

has Fourier multiplier ik on nonzero modes and identity on the zero mode.
The recovery code uses exactly its inverse. It retains every represented
mode and the mean; this is a coordinate change, not a spectral filter.
The gradient-coordinate Jacobian is the original P Jacobian composed
with recovery, and the preconditioner uses the corresponding inverse
composition. The inspected formulas agree with that chain rule.

Using gvar directly for P_x can avoid losing tiny derivative-relevant
corrections when recovering nodal P and differentiating it again. At
finite precision, re-differentiated recovered P need not reproduce the
authoritative gvar residual at the same tolerance. This is the purpose
of the representation, not evidence of a changed constraint. A useful
consistency diagnostic is the round-trip discrepancy itself. Restart
must preserve gvar; the inspected evolve_gradient.py correctly saves
and restores final_gvar as well as final_P.

Matrix-free GMRES is checked against its actual linear residual, and the
nonlinear residual target remains 2e-9. The transformation does not
relax that target. Dense/FFT agreement and Jacobian checks are numerical
evidence for the implementation, not a proof at every resolution.

## 5. Inspected validation evidence and small caveat

The recorded expanded validation reports all checks passing:

* smooth-state RHS maximum difference versus dense: 4.39e-9;
* initial RHS difference: 1.79e-9;
* t=.5 charge/lapse differences: 3.11e-11 and 3.60e-12;
* reconstructed p_beta difference: 1.65e-7;
* padded homogeneous error: 2.09e-11;
* n1023 initial gradient-coordinate residual: 4.21e-11.

I inspected those outputs rather than independently rerunning the whole
validation. They support use on resolved states and at the declared
tolerances. They do not make unresolved high-frequency comparison
meaningful or certify later nonlinear evolution automatically.

One small validation-isolation detail: assigning `f.P *= 0` after a prior
gradient solve does not reset the cached `f.gvar`. The next solve uses
gvar as its warm start. This does not invalidate a converged residual,
but a test intended to compare identical cold starts should reset both.

Continue monitoring physical-field refinement, multifield tails, raw
constraints and their differentiated remainder, branch/cap/clock margins,
and projection corrections. A reduced roundoff floor is a numerical
improvement; it cannot be relabeled as a proof of physical breakdown,
avoidance, or unique singular continuation.

## Provenance

Independent delegated numerical/code review, 2026-11-06. Reviewed SHA-256:

    derive_expanded.py 3f4518186dcba10f5e44227e027b6779af37bf5f9f0a0c81d6411103c035bc4b
    expanded_rate.py bd32fbcc24f3ff491424c68b266e74fc85b79b94b20079feb135ca13b9ac558a
    expanded_constraints.py 7a7b1f288b5bc45c60cb26ab2ad356fb6ff50f9d4a91222e6a255b5ff9f87712
    gradient_constraints.py 73f7b87bdf6aee6690df2ef119bbc5af8c52fbd83440d8e9620443c05a289d6f
