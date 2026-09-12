# The equation a gradient-criticality mechanism must actually solve

L192 (`5fdec3d9a`) identifies roots of a proposed sound-speed expression.
Its sign test is not an evolution equation for the background gradient.
Here is the exact missing kinematic relation, without altering the action's
coefficient functions. This is standard differential geometry applied to
this candidate, not a claim of a newly discovered law.

Use signature (-+++), n.n=-1, h=g+n n, v_mu=D_mu chi, Q=n.grad chi,
Y=v.v, a_mu=n.grad n_mu and
K_mu_nu=h_mu^alpha h_nu^beta grad_alpha n_beta. A dot denotes n.grad.
Since grad_mu chi=v_mu-Q n_mu and covariant derivatives commute on a scalar,

\[
\boxed{\dot Y=2D^\mu\chi\,(D_\mu Q+Q a_\mu)
             -2K_{\mu\nu}D^\mu\chi D^\nu\chi.}
\]

To derive it, differentiate v_mu=grad_mu chi+Q n_mu and contract with
2v^mu. The derivative of Q n_mu contributes 2Q v.a; the derivative of
grad_mu chi contributes 2v.grad Q-2v^mu(grad_mu n^nu)v_nu. Projecting the
last term yields the displayed K contraction. No sound speed appears.

On an FLRW clock foliation (zero acceleration, K_mu_nu=H h_mu_nu), a
spatially uniform Q gives dot Y=-2HY. This is a kinematic statement, **not**
an assertion that a nonzero single-gradient configuration solves isotropic
Einstein equations; its stress and metric response must still be solved.

For a moving proposed critical point Y*(tau), define E=Y-Y*. Its exact
tracking condition at E=0 is

\[
 2D\chi\cdot(DQ+Qa)
 =\dot Y_*+2K_{\mu\nu}D^\mu\chi D^\nu\chi.
\]

In the isotropic expansion specialization the right side is dot Y*+2HY*.
A constant positive Y* requires a source 2HY*, not simply a vanishing
sound speed. The action must determine this source and its response to E;
attraction further needs the perturbation of the full coupled evolution to
restore E, not just a change of sign of a spatial coefficient.

`gradient_transport.py` independently differentiates Y in a zero-shift
metric with spatially varying lapse and FLRW spatial metric. It verifies
the acceleration sign, dilution term, and tracking balance using exact
SymPy local jets. Its tests do not formalize general tensor calculus or
establish nonlinear existence, stability, or cosmological viability.

The next action-derived calculation is therefore the coupled finite-gradient
principal operator **and** the evolution of this source on the same
solution. Fitting a function Y*(a) or optimizing unrelated coefficient
histories would not compute that response.
