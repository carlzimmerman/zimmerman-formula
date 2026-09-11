# Coupled pressure-supported initial data: solved, but not MOND

Base `51d973208`. The original complete-theory goal remains **OPEN**.
This package advances the matter extension proposed in the preceding checkpoint
by actually coupling its stress to the gravitational constraints. The result is
a pressure-balanced **initial configuration**, not a stationary spacetime or an
observational galaxy fit. The distinction is checked, not merely disclaimed.

The gravitational action is unchanged:

\[
 S_g=\int\sqrt{-g}[M^2(\mathcal R-2\Lambda)/2+P(X,\tau)
       +\sqrt{-\nabla\tau\cdot\nabla\tau}\,W(Y,\tau)-V(\tau)
       +\gamma X\Box\chi].
\]

The separately declared matter extension is

\[
 S_b=\int\sqrt{-g}\lambda(\sqrt Z-m_b)^{5/2},\quad
 Z=-\nabla\theta\cdot\nabla\theta,
 \quad h=\sqrt Z-m_b>0.
\]

No dark-particle population is added. The matter EOS is an irrotational fluid
proxy; its exponent and positive constants are chosen, not derived microscopic
constants. The previous dust results are not transferred to this matter action.

## Derivation from both action sectors

`derive.py` imports the unrestricted spherical gravitational variation and
independently differentiates the matter density N A R² P_b(theta_t²/N²) on the
normal-rest initial slice. It obtains lapse source -AR² rho, radial source NR² p,
and angular source 2NAR p. Thus pressure affects the spatial equations even
though it is not an additional Hamiltonian density source.

Only after varying, set R=r, chi_r=0, Q=q_bg, Kr=Ko=H_bg and zero shift, and
impose the original background Friedmann relation. Scalar gradients immediately
develop through chi_rt=q N_r; their contribution to clock preservation is retained.
Eliminating the metric and scalar time derivatives gives

\[
 \boxed{S\Delta_hN-\lambda_0(N-1)-\lambda_b(\rho_b+3p_b)N=0,}
\]
\[
 f=A^{-2},\quad I_b'=\rho_b r^2,\quad
 f=1-I_b/(M^2r),\quad
 \Delta_hN=fN''+(2f/r+f'/2)N'.
\]

S=W-2q²W_Y and the same lambda0,lambdab expressions in
`../nonlinear_infall_2026/initial.py` are used. The pressure coefficient is
computed and checked to be three times the density coefficient. The angular
metric equation is independently checked as well. Ten new symbolic identities
pass, with the 36 original gravitational identities imported as regressions.

The normal-rest phase theta_t=omega, spatially constant at this instant, gives

\[
 N(m_b+h)=\omega,\qquad
 p_b=\lambda h^{5/2},\qquad
 \rho_b=\frac\lambda2h^{3/2}(3h+5m_b),
 \qquad p_b'=-(\rho_b+p_b)N'/N.
\]

This is pressure balance relative to the clock-normal congruence. On the chosen
expanding initial slice the same matter action also implies

\[
 \partial_t\rho_b=-3NH_{bg}(\rho_b+p_b)\ne0.
\]

Therefore these data do not describe a static galaxy, despite the pressure
balance. The distinction is material when interpreting the acceleration.

## A necessary minimum-enthalpy condition

Assume a smooth regular configuration on a finite ball with f,N,S,lambda0,
lambdab>0, N=1 at the outer boundary, positive matter somewhere, vacuum at the
outer boundary, and the pressure-balanced phase relation above. At an interior
minimum N* the spatial Laplacian is nonnegative, so the varied lapse equation
implies

\[
 \lambda_0\le N_*[\lambda_0+\lambda_b(\rho_*+3p_*)].
\]

The vacuum exterior requires omega<=m_b. Since N*(m_b+h*)=omega,

\[
 N_*(m_b+h_*)\le m_b.
\]

Eliminating N* gives the necessary condition

\[
 \boxed{\lambda_0h_*\le m_b\lambda_b(\rho_*+3p_*).}
\]

The fluid enthalpy is largest where N is smallest. For centrally peaked data,
h*=h_c. With the chosen EOS this becomes

\[
 \boxed{2\lambda_0\le m_b\lambda_b\lambda\sqrt{h_c}(9h_c+5m_b).}
\]

For fixed positive coefficients, the right-hand side vanishes as h_c tends to
zero. Thus this initial family does not admit arbitrarily dilute compact
pressure-balanced configurations with vacuum exterior. The bound is necessary,
not sufficient; it does not exclude other clock profiles, other boundary
conditions, moving matter or other equations of state.

`BindingThreshold.lean` proves three exact algebraic statements: elimination
of N*, the EOS polynomial threshold with r=sqrt(h_c)>0, and contradiction below
threshold. The maximum-principle/PDE and phase-relation steps are analytic
outside Lean and appear as explicit theorem hypotheses. No gravity closure,
PDE existence, or first-principles EOS selection is claimed by compilation.

At gamma=1e-6, in the original dimensionless background units,

\[
 S=0.0008265149328,\quad\lambda_0=0.005194848096,
 \quad\lambda_b=0.004545509971.
\]

For m_b=1, lambda=50 the necessary minimum enthalpy is approximately
8.35660e-5, with rho=9.54941e-5 at that threshold. These are code-unit values,
not measured galactic densities. `cases.py` calculates the threshold from the
actual coefficients; no numerical threshold is hard-coded into a check.

## Actual coupled boundary solves

`solve.py` solves for I_b(r), N(r), N'(r) and omega together. It prescribes
central enthalpy and enforces regular-center series at r=1e-5 plus N(L)=1.
The regular-center series has omitted higher powers of this small cutoff;
this is a numerical approximation, not an interval-certified origin theorem.
The zero-pressure surface is found as a root rather than assigned a radius.
The EOS is continued by zero for h<=0 solely for this initial boundary problem.
The kinetic degeneracy at its vacuum surface remains a time-evolution question.

The initial chemical potential and density are not inserted as an external
Gaussian. Tests refine the mesh/tolerance and double the outer radius. Probe
residuals are evaluated between collocation nodes, not only at the nodes.
An unphysical numerical solution with omega>m_b is rejected even if its equation
residual is tiny. Rejected exterior solutions do not receive extrapolated force
diagnostics.

Nine cases include four distinct successful parameter choices and two numerical
refinements of one of them, two analytic exclusions, and one solution rejected
for lacking a vacuum exterior. The latter has h_c=1e-4,lambda=50 and
omega=1.00001534; the necessary threshold alone does not establish existence.

## Independent geodesic-force gate

The angular metric equation supplies the initial background-subtracted inward
acceleration of a test particle momentarily normal-rest:

\[
 g_{init}=\frac{I_b}{2M^2r^2}+\frac{rp_b}{2M^2}
 +\frac{r}{2M^2N}\left[U(1-N)+2\gamma q^2(Q_t-\dot q_{bg})\right].
\]

It is not the acceleration of the pressure-supported fluid element; that
element has an additional pressure force. Nor can N'/N alone be called the
physical galactic force on this expanding slice. The coordinate source radius
is specified, and the areal radius equals r on this initial slice only.

At h_c=.01,lambda=50,L=3, the computed values are

\[
 \omega=0.99743683765,\quad r_s=0.49750246631,
 \quad N_{min}=0.98756122541,\quad f_{min}=0.99820574159.
\]

At r=1.5 r_s the refined values give

\[
 \boxed{g_{init}/g_{N,bare}=1.00461882970,}
\]
\[
 \boxed{\frac{(1-e^{-g_{init}/a_0})g_{init}}{g_{N,bare}}
       =0.00810657815,\qquad a_0=\sqrt{\Lambda/(32\pi)}.}
\]

The MOND target for this diagnostic would be 1. Doubling L from 3 to 6 changes
the latter result to 0.00810657795. Mesh/tolerance refinement also agrees.
Across the four distinct solved parameter choices, the force ratio is
1.00268–1.00462 and the MOND balance is 0.000447–0.011413. Pressure support
has not produced a MOND realization on this tested initial family.

The normalization uses G_bare=1/(8pi M²). A measured high-acceleration Newton
constant has not been calibrated for the full candidate. Thus these are
action-derived initial diagnostics, not an observational exclusion of the
whole theory. No empirical data are fitted, and no local a0 is introduced.

## Verification and next implication

The bounded runner executes every new Python script, the three Lean statements,
and the existing dust-variation, initial-data and matter-extension regressions.
Actual commands, input hashes and output are in `run_002/manifest.json` and
`run_002/stdout.txt`. Passing checks establish these calculations and their
limited claims; the logged initial MOND mismatch remains a mismatch.

Final execution: all eight jobs returned exit status 0 (`derive`, `solve`,
`test_branch`, `cases`, `old_initial`, `old_matter`, `matter_extension`, `lean`).
The five new regression tests passed; all three Lean statements compiled with
only propext, Classical.choice and Quot.sound reported as axioms. The evidence
manifest validator also returned 0. `run_001` is retained as historical output
before the threshold-root reporting extension to `cases.py`; use `run_002` for
the current input hashes and results.

The next physical branch must relax the homogeneous initial clock restrictions
and solve nonzero spatial clock gradients together with supported baryons and
cosmological matching. A stationary or controlled slowly evolving solution is
required before rotation curves and lensing can be inferred. The earlier failed
time-evolution solver is not used as evidence here and remains unresolved.
Full nonlinear Dirac closure, PPN, CMB, global stability and the origin of
kappa=1/2 remain open. The present result neither proves uniqueness nor claims
a globally novel gravity law.

Credit Carl Zimmerman for the primordial-clock direction and the dynamical
interpretation motivated by Brian Keating's video
https://www.youtube.com/watch?v=HRnselv8Y6E. This is motivation attribution,
not a verified transcript or endorsement. Mathbox computation/proof audit
guided scope, failed-case retention, and independent source checks; mathematical
proofreading covered the report and the distinction between h and H_bg.
