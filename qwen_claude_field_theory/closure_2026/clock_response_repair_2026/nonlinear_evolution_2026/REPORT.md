# Finite-time susceptibility, the static dust obstruction, and the unresolved evolution gate

Base: `41d63553c90b6c60adf6f4ffffb59f9f8428391d`. The preceding initial-data
checkpoint is `440dad1ed324594ad4768d9ff5d3ec4b841b3d30`.
Original goal: one action satisfying all relativistic MOND requirements.
**Verdict: incomplete. The full theory remains OPEN.**

The present calculation derives new necessary conditions and a matter-model
limitation. It does not claim a new established law of nature or global novelty.
The underlying gravitational action and its reconstructed coefficient functions
are unchanged. A pressure-fluid matter extension is explicitly separate from
every existing dust result.

## Same action and exact equations

With signature (-+++), X=-grad(chi)^2, s=sqrt(-grad(tau)^2)>0,
n=-grad(tau)/s, Q=n.grad(chi), Y=Q^2-X, the action is

\[
 S=\int\sqrt{-g}\,[M^2(\mathcal R-2\Lambda)/2+P(X,\tau)
       +sW(Y,\tau)-V(\tau)+\gamma X\Box\chi]+S_b.
\]

P,W,V are the fixed logarithm/square-root functions in
`../cubic_background_completion/README.md`. Their time-dependent coefficients
are prescribed from the original reconstructed clock history, not replaced by
the local metric or source. `constitutive.py` evaluates their full off-branch
jets and checks the constitutive domain before every evaluation. No MOND law
or acceleration scale is inserted into the evolution equations.

`equations.py` imports the unrestricted spherical Euler equations and only then
chooses zero shift. The independent time equations are the radial and angular
metric equations, the conserved chi current, and preservation of

\[
 T=V_\tau-P_\tau+W(k+2h)-2W_Yk\chi_r^2/A^2
 -\frac{2Q}{AR^2}\partial_r(R^2W_Y\chi_r/A)=0.
\]

The state retains A,R,k,h,Q,chi_r, baryon velocity and conserved baryon mass.
The symbolic calculation verifies the radial and time Noether identities,
cancellation of N_t, and the original initial-slice restriction. It computes
the linear system for k_t,h_t,Q_t,N_rr rather than assuming a rank or determinant.
Its matrix is not a Dirac Poisson-bracket matrix.

Adding eta*N*C_H and 2eta*N*C_H to the spatial equations changes no solution
on C_H=0. Eta=1 is the spatial Ricci formulation. `center.py` takes the exact
regular-origin limit with consistent Taylor jets including Q=Qc+Q2*r^2/2.
Its solved N2 is N''(0); the center lapse row is
2(N1-N0)/dr^2=N2, with no extra factor three.

## A finite-time necessary condition, checked in Lean

Let a0,n,epsilon,C>0, L>0, and suppose a nonnegative force obeys a source
response estimate on a common solution family,

\[
 0\le g(t,\varepsilon)\le C e^{Lt}\varepsilon.
\]

The same constants must apply across source amplitudes. This estimate is an
explicit hypothesis: no energy estimate, PDE existence theorem, differentiable
solution map or observable bound for this action is proved by this package.

Since 1-exp(-x)<=x, exact exponential MOND at a time t requires

\[
 \varepsilon n=(1-e^{-g/a_0})g\le g^2/a_0
 \le C^2e^{2Lt}\varepsilon^2/a_0,
 \qquad \boxed{a_0n\le C^2e^{2Lt}\varepsilon.}
\]

Consequently the analytic logarithmic corollary is

\[
 \boxed{t\ge\frac{1}{2L}\log\frac{a_0n}{C^2\varepsilon}.}
\]

`FiniteTimeMOND.lean` proves the exact gain inequality, its exponential form,
and a threshold formulation: if C^2 exp(2L t0) epsilon<a0 n and L>=0, any
time attaining the exact law must satisfy t>t0. It also proves exclusion below
a specified finite-gain threshold. It does not formalize the logarithm
corollary or a limit theorem; those are stated separately above. All five
declarations compile without sorry or new axioms, with the four main results'
axioms printed explicitly.

For L=0 the ordinary finite-gain exclusion applies directly; division by L
is not allowed. When t is fixed and the uniform gain bound holds for arbitrarily
small sources, exact MOND fails for sufficiently small epsilon. A formation
time diverging as epsilon decreases, nonuniform susceptibility, changing
boundary/initial data, or a distinct nonlinear branch can escape this result.
Thus regular short-time evolution alone cannot establish universal deep MOND.
This is a conditional obstruction, not a proof that all MOND theories fail.

## The current dust model cannot be a stationary spherical galaxy

The baryon action used in the evolution is

\[
 S_d=-\frac12\int\sqrt{-g}\,\rho_b[(\nabla\theta)^2+1].
\]

`static_dust_gate.py` imports its actual variation. In a zero-shift spherical
metric, with w=theta_r, its conserved radial mass flux is

\[
 j_d=-NR^2\rho_b w/A.
\]

Stationarity of the conserved mass density makes this flux spatially constant.
A regular center without a source or sink sets the constant to zero. On any
positive-density interval with N,A,R>0, this implies w=0. The independently
varied momentum equation then gives

\[
 \partial_t w=N_r.
\]

A stationary state requires N_r=0 there. In a static metric this excludes a
nonzero Newtonian potential gradient inside a stationary pressureless dust cloud.
The integration of continuity is an analytic step; the script verifies the
action-derived flux, its unique root and the residual momentum equation.

This is a standard consequence of geodesic pressureless matter, not a claimed
new fundamental no-go theorem. It does not exclude a rotating disk, a
collisionless population with velocity dispersion, nonzero boundary flux, a
central sink, or evolving dust. A collapse calculation can still diagnose
transients and caustics. It cannot by itself deliver a stationary galaxy.

## A pressure-supported matter action passes its local gate

`pressure_supported_baryons.py` derives a separately labelled baryon-fluid proxy:

\[
 S_b=\int\sqrt{-g}\,P_b(Z),\quad Z=-(\nabla\theta)^2,
 \quad P_b(Z)=\lambda(\sqrt Z-m_b)^{5/2},
 \quad \lambda,m_b>0,\quad h=\sqrt Z-m_b>0.
\]

Direct differentiation gives

\[
 p_b=\lambda h^{5/2},\qquad
 \rho_b=\frac{\lambda}{2}h^{3/2}(3h+5m_b),
\]
\[
 P_{b,Z}=\frac{5\lambda h^{3/2}}{4(h+m_b)}>0,\qquad
 P_{b,Z}+2ZP_{b,ZZ}=\frac{15\lambda\sqrt h}{8}>0,
\]
\[
 0<c_b^2=\frac{2h}{3(h+m_b)}<\frac23<1.
\]

For static theta=omega*t, Z=omega^2/N^2, its matter Ward identity is

\[
 \boxed{p_b'=-(\rho_b+p_b)N'/N.}
\]

This supplies support against a nonzero lapse gradient directly from an action.
It introduces no dark-particle population. It is an irrotational fluid proxy,
not a derived stellar distribution or a fit to observed baryons. The exponent
5/2 is chosen to supply a nonrelativistic 5/3 polytrope; it is not a first-principles
coefficient derivation. At h=0 the kinetic coefficients vanish, so a vacuum
boundary needs a separate treatment. This script has not solved its coupled
clock-gravity equations, certified their mixed modes, or derived MOND.

## Numerical gate and interpretation

`evolve.py` uses fourth-order parity-respecting radial derivatives, a second-order
lapse solve, RK4 time stepping, and conservative spherical baryon mass flux.
`project.py` solves the actual radial Hamiltonian, momentum and clock constraints
for A_r,h_r,k at each stage. An independent directional-derivative diagnostic
in `diagnose.py` tests whether this projection preserves metric time equations;
solving constraints alone does not guarantee a spacetime solution.

The original second-order implementation failed refinement at t=.02:
momentum residual 7.41e-6 at 129 points versus 1.77e-5 at 257 points. At t=.005
it decreased 7.13e-6,1.89e-6,4.94e-7 at 65,129,257 points, showing why a single
short successful run was insufficient. Tightening the radial ODE tolerance
to 2e-13/2e-15 made a diagnostic run take over four minutes; it was interrupted
(exit 130), and the original 2e-10/2e-12 tolerance was restored.

The fourth-order revision passes its manufactured derivative tests but still
fails the unchanged t=.02 refinement gate: Hamiltonian/momentum errors are
(2.62e-6,4.89e-6) at 129 points and (9.11e-6,8.88e-6) at 257 points in the
development run. Background, positive-density rejection and short sourced
mass-conservation tests pass. These failures are numerical validation failures,
not action-derived physical instability or a universal MOND exclusion.
No evolved force, empirical prediction or late-time relaxation is certified.

`run_001/` records fresh commands, logs, input hashes and exits, including the
failed gate; the aggregate runner returns nonzero if any gate fails.
The strict test has not been weakened to manufacture a pass.

Fresh final execution: **18 of 19 jobs exited 0; `evolution_tests` exited 1**,
with exactly the refinement failure above. The three other evolution tests
passed. The full-gradient identities, coefficient checks, center control,
manufactured derivatives, two matter calculations, five Lean declarations and
existing action/matter/tensor/initial-potential regressions passed their stated
checks. The Mathbox evidence validator exited 0; it validates provenance even
when a recorded scientific gate fails. Every created Python script was executed,
including `../run_evolution_checks.py`; no new dependency was installed.

The projection time-consistency check remains unresolved too: its A mismatch
depends appreciably on the directional finite-difference step. With the updated
scheme at t=.005 and 129 points, the maximum A mismatch is 4.97e-4 at step 1e-5
and 7.07e-4 at step 5e-6. No continuum temporal-consistency claim follows.

Lean development initially encountered an unavailable broad tactic import and
a conflicting cached log dependency. The final source uses the existing narrow
exponential/tactic imports and certifies the exact exponential threshold rather
than the logarithm corollary. A multiplication-cancellation proof command also
needed correction. The final fresh build exits 0 and prints only propext,
Classical.choice and Quot.sound; failed development builds are not counted.

Reproduce the complete suite from the repository root (choose a new output path
for each execution):

```sh
python3 -B qwen_claude_field_theory/closure_2026/clock_response_repair_2026/run_evolution_checks.py qwen_claude_field_theory/closure_2026/clock_response_repair_2026/nonlinear_evolution_2026/recheck_001
```

The exact outer provenance command is stored as argv in `run_001/manifest.json`;
the per-job commands and exit statuses are in `run_001/checks/checks.json`.
The expected current aggregate exit is 1, not a certification pass.

## What remains unavoidable

1. Derive and solve a baryon-supported galactic branch from this gravitational
   action with an adequate matter action, including boundary matching and the
   full nonzero-gradient clock constraint. A pressure proxy is one bounded test;
   realistic stellar systems need a distribution function or equivalent stress.
2. Establish an accurate metric evolution or solve the branch directly. Current
   center/projection errors still prevent trusting nonlinear force measurements.
3. Derive both metric potentials and the MOND source law. If a regular-response
   bound holds uniformly, the new Lean obstruction identifies the required
   departure from that branch; it does not manufacture that departure.
4. Complete nonlinear Dirac closure, all-sector health, full PPN, cosmological
   perturbations/CMB, observed galaxies and clusters, and first-principles
   selection of the coefficient functions. None is bypassed by these results.

Carl Zimmerman's primordial-clock direction motivates this work. Credit continues
to Carl for suggesting the dynamical interpretation after sharing Brian Keating's
video https://www.youtube.com/watch?v=HRnselv8Y6E. The video is motivation, not a
verified transcript, a derivation source, or an endorsement.

Mathbox research-program and computation-audit guided the route changes and
recorded failures; proof-audit self-review checked the theorem hypotheses and
the matter-domain exclusions. Proofread-math self-review covered this report.
