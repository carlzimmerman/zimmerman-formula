# Baryons coupled to the same clock action

Base `776cc413d13ced7996fc06d544b68cacbebc5615`. Full gravity target: **OPEN**.
This package advances the missing source calculation. It does not select an
action from first principles, derive a0, or turn reconstructed P/W functions
into a fundamental theory. No exponential force law is imposed on the solver.

## What is now varied, and what is actually solved

`action/REPORT.md` gives the fully nonlinear spherical action, all four metric
variations and the chi equation before any radial gauge is fixed. It keeps
clock density, lapse and shift, and the time-dependent scalar current. The
companion matter package supplies a dynamical dust source for the nonlinear
equations. Those equations have not yet been evolved into nonlinear galaxies.

`source.py` and `response.py` construct a different, explicitly bounded level
of evidence: the linear baryon-sourced initial-value problem on the **same**
homogeneous repaired background. This is the benchmark a nonlinear solver must
recover, not a substitute for the requested nonlinear matched-source experiment.

## Full nonlinear current: the omitted term is identified

In clock gauge, write
\(ds^2=-N^2dt^2+A_r^2(dr+vdt)^2+R^2d\Omega^2\),
\(Q=(\dot\chi-v\chi')/N\), and \(Y=(\chi'/A_r)^2\).
The exact radial action current satisfies

\[
\partial_t p_\chi+\partial_r j_\chi=0,\qquad
p_\chi=A_rR^2\{2QP_X+
\gamma[-2Q^2K+2K_rY+4QD^2\chi]\}.
\]

For a regular center with vanishing center flux,

\[
\boxed{j_\chi(t,r)=-\partial_t\int_0^r p_\chi(t,s)\,ds.}
\]

Thus regularity does not justify setting radial current to zero. The earlier
two-radius obstruction imposed zero time-current divergence and omitted part
of the clock density. The new formula identifies what has to be computed to
test that omitted physics; it does not show that it cancels the obstruction.

The covariant and ADM local currents differ by a boundary improvement, explicitly
verified in the action package. Total charge and boundary conditions must use
one consistent convention. This is not evidence that a clock exchanges ordinary
baryon number or exerts a nonmetric force on matter.

## Conserved linear baryon source and physical initial data

For a real Fourier mode, minimally coupled nonrelativistic test dust contributes
\(L_b=-C n/2\), where \(C=a^3\delta\rho_k\) is constant. The factor 1/2
is the real-mode spatial average, not a fitted gravity coefficient. This stress
is conserved on the background at O(epsilon); gravitationally induced dust
momentum contributes at O(epsilon²). No arbitrary time-switching function is
allowed. This does not make a finite-mass frozen comoving halo an exact solution.

Use \(M=M^2_{\rm action}\), \(\Theta=H+\gamma q^3/M\), and
\(\beta=-a^2b/k\) for the shift potential (not a PPN parameter). Direct
variation, with background scalar current \(j=A\), gives

\[
n=\frac{M\dot\zeta+\gamma q^2\dot\sigma+A\sigma/2}{M\Theta},
\]
\[
\beta=-\frac{M\zeta+\gamma q^2\sigma}{M\Theta}
 +\frac{a^2}{2k^2M\Theta}
 [q\widehat B(\dot\sigma-qn)+3\Theta A\sigma+\delta\rho_k].
\]

The density changes the shift constraint; it does not add an explicit density
term to the lapse solution obtained from the zero-momentum constraint.
The complete lapse is nevertheless sourced through the evolved clock/metric.

For \(u=\sigma-(q/H)\zeta\), integrating the source's \(\dot\zeta\)
term by parts produces the nonzero constraint source

\[
f_z=\frac{C[U-2\gamma q^2\dot q]}{4H(MH+\gamma q^3)}.
\]

The independently varied quadratic action has
\(D\zeta+J\dot u+Eu+f_z=0\). Eliminating it generates **both** a
velocity source and a position source in the physical scalar action. Omitting
the velocity source changes the initial data and force calculation.
`SourceSchur.lean` proves this substitution exactly for D != 0; it does not
formalize covariant gravity. `source.py` supplies the action-to-coefficient
bridge in exact symbolic arithmetic outside Lean.

Numerics use common physical data u=udot=0 at ln(a)=-1. The corresponding
canonical momentum equals the affine velocity-source coefficient, rather than
zero. That source-dependent coordinate shift is not a fitted scalar charge.

## Two separately reconstructed metric potentials

Under \(t\mapsto t+T\), the scalar metric variables transform as
\(n\mapsto n-\dot T\), \(\beta\mapsto\beta+T\),
\(\zeta\mapsto\zeta-HT\). Consequently,

\[
\boxed{\Phi=n+\dot\beta,\qquad \Psi=-\zeta-H\beta.}
\]

Neither potential is assigned to the other. For numerical conditioning, the
code cancels equal derivative terms algebraically before evaluation. It computes
the remaining time derivative by complex-step differentiation along the actual
background and sourced Hamilton equations, with a finite-difference check.
Phi-Psi is an independent diagnostic, not an input. Even equality in this linear
cosmological experiment would not constitute a full PPN gamma calculation.

## Discriminating the mechanisms without overstating the result

Two Gaussian sources of mass M_b and 4M_b, with widths R_b and 2R_b, have the
same enclosed baryonic inverse-square acceleration at r and 2r. Comparing their
derived forces tests dependence on size in addition to baryonic acceleration.
Both Newtonian gravity and a universal MOND law can pass that comparison.

A separate fixed-radius source-amplitude comparison distinguishes the regular
linear scaling from deep-MOND square-root scaling: four times the source gives
four times the linear response, whereas the deep-MOND target approaches twice
the force. This fact does **not** rule out a singular/nonperturbative branch of
the full action. Such a theorem requires a controlled source-to-solution inverse,
fixed data/domain/time, and separately justified exchanges of limits.

Here k=0 is excluded, and the solved time interval is finite. The action's log
and square-root neighborhoods shrink with the background m toward zero. No
uniform m→0, k→0, infinite-radius or late-time conclusion follows. The force
normalization against bare Einstein gravity is explicitly **not** a measurement
of the full theory's Solar-System Newton constant.

## Method attribution and remaining calculation

This work follows the source-realization and residual-control lesson discussed
in the [OpenAI Navier–Stokes construction, §§2–3](https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf)
and the statement-locking workflow already cited in the project blueprint.
No fluid theorem is imported as a gravity theorem, and no claim of physical
novelty follows. Carl supplied the paddle/swirl intuition motivating the question
about persistent internal momentum transport; the variational calculations are
the tests of that intuition, not its confirmation.

Next: solve the full spherical constrained evolution with dynamical matter,
common cosmological clock data and regular center/exterior matching. Demonstrate
whether its nonlinear source response produces the exact exponential law and
independent no-slip metric. PPN, nonlinear DOF/constraint closure, CMB safety,
strong coupling and first-principles coefficient selection all remain required.
