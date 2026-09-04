# HPI-Delta finite-eccentricity Kepler law (2026)

## Result

**PASS (bounded analytic and numerical consequence), not relativistic closure
and not a global novelty claim.** The spherical exterior weak-static branch

\[
\mu(g/a_0)g={GM_b\over r^2},\qquad \mu(y)=1-e^{-y}
\]

has an exact finite-eccentricity turning-point law. Its deep-MOND limit gives
an eccentric analogue of Kepler's period law:

\[
\boxed{\quad T_r^4={F(e)^4R^4\over GM_ba_0}\quad}.
\]

Here \(T_r\) is the pericenter-to-pericenter radial period and

\[
R={r_a+r_p\over2},\qquad
e={r_a-r_p\over r_a+r_p},\qquad 0<e<1.
\]

Unlike the Newtonian Kepler law, the coefficient is not constant: \(F(e)^4\) is a
universal function of turning-point eccentricity. This is stronger than the
previous near-circular epicycle prediction because no small-eccentricity
expansion is used.

The same branch predicts a test-particle virial invariant,

\[
\boxed{\quad \bigl(\langle v^2\rangle_t\bigr)^2=GM_ba_0\quad},
\]

for a bound slow-motion test particle on any exterior orbit wholly in the
deep-MOND logarithmic regime. This is a one-particle analogue of circular
baryonic Tully--Fisher scaling. It is not by itself a theorem about a
self-gravitating galaxy or an ensemble of interacting tracers.

## Provenance and conditional scope

This computation starts from the spherical exterior flux equation derived in
the preceding HPI-Delta weak-static work. The parent action/constraint probe
is in ../cde_hpi_delta_2026/cde_hpi_delta_action_gate_2026.py; the weak-field
equations and circular prediction are in
../hpi_delta_predictions_2026/hpi_delta_predictions_2026.py. The present
calculation does not promote that still-open candidate into a closed
relativistic theory. It asks what that one branch predicts for a leading
weak-field, slow-motion geodesic test particle if the branch survives the
remaining action-level gates.

## Exact exponential-force construction

Introduce the source scales

\[
r_M=\sqrt{GM_b/a_0},\qquad
v_\infty=(GM_ba_0)^{1/4},\qquad
t_M={r_M\over v_\infty}
=\left({GM_b\over a_0^3}\right)^{1/4},
\]

and define

\[
x={r\over r_M},\qquad y={g\over a_0},\qquad
W={\Phi\over v_\infty^2},\qquad \tau={t\over t_M},
\]

\[
\lambda={\ell\over r_Mv_\infty},\qquad
\mathcal E={\varepsilon\over v_\infty^2},
\]

where \(\ell\) and \(\varepsilon\) are the test particle's specific angular
momentum and energy. The full exponential constitutive equation becomes

\[
\boxed{x^2y(1-e^{-y})=1}.
\]

It has one positive solution for every \(x>0\), because

\[
{d\over dy}\left[y(1-e^{-y})\right]
=1+(y-1)e^{-y}>0\qquad(y>0).
\]

With \(W'(x)=y(x)\), a useful exact parametric representation is

\[
x(y)=[y(1-e^{-y})]^{-1/2},
\]

\[
W(y)-W(y_*)=yx(y)-y_*x(y_*)
-\int_{y_*}^{y}{du\over\sqrt{u(1-e^{-u})}}.
\]

For supplied dimensionless turning radii \(x_p<x_a\), define

\[
\lambda^2={2[W(x_a)-W(x_p)]\over x_p^{-2}-x_a^{-2}},\qquad
\mathcal E=W(x_p)+{\lambda^2\over2x_p^2},
\]

\[
P(x)=2[\mathcal E-W(x)]-{\lambda^2\over x^2}
=\left({dx\over d\tau}\right)^2.
\]

This construction produces a valid single-well radial motion for every
\(0<x_p<x_a\). To see this, let \(H(x)=x^3y(x)\). Differentiating the
flux relation gives

\[
{H'(x)\over x^2y}
={1-e^{-y}+3ye^{-y}\over1-e^{-y}+ye^{-y}}>0.
\]

The mean-value theorem applied in the variable \(x^{-2}\) then gives
\(H(x_p)<\lambda^2<H(x_a)\). Hence the effective potential derivative is
negative at \(x_p\), positive at \(x_a\), and crosses zero only once.
Therefore \(P(x)>0\) between its two simple endpoint roots.

Then the full exponential law is the exact two-parameter surface

\[
\boxed{
T_r=2t_M\int_{x_p}^{x_a}{dx\over\sqrt{P(x)}},\qquad
\Theta=2\lambda\int_{x_p}^{x_a}{dx\over x^2\sqrt{P(x)}}
}.
\]

Here \(\Theta\) is the azimuth from one pericenter to the next and
\(\Delta\varpi=\Theta-2\pi\). The full interpolation cannot collapse to a
function of eccentricity alone: it also depends on \(R/r_M\).

## Deep-MOND closed law

For \(y\ll1\), the force and potential become

\[
g={v_\infty^2\over r},\qquad
\Phi=v_\infty^2\ln(r/r_*).
\]

Set \(z=r/R\), \(z_p=1-e\), \(z_a=1+e\), and define

\[
J={\ell\over Rv_\infty},\qquad
E={\varepsilon\over v_\infty^2}-\ln(R/r_*).
\]

Solving the two turning-point energy equations, rather than assigning an
elliptical orbit, gives

\[
J^2(e)={(1-e^2)^2\over2e}\ln{1+e\over1-e},
\]

\[
E(e)=\ln(1+e)+{J^2(e)\over2(1+e)^2},
\]

\[
Q_e(z)=2[E(e)-\ln z]-{J^2(e)\over z^2}.
\]

The observable functions are therefore

\[
\boxed{F(e)=2\int_{1-e}^{1+e}{dz\over\sqrt{Q_e(z)}}},
\]

\[
\boxed{\Theta(e)=2J(e)\int_{1-e}^{1+e}
{dz\over z^2\sqrt{Q_e(z)}}},\qquad
\Delta\varpi(e)=\Theta(e)-2\pi.
\]

The turning points are genuine simple roots. With
\(q=(1+e)/(1-e)>1\),

\[
{J^2\over z_p^2}={q^2\ln(q^2)\over q^2-1}>1,\qquad
{J^2\over z_a^2}={\ln(q^2)\over q^2-1}<1,
\]

by \(\ln t<t-1<t\ln t\) for \(t>1\). Thus the effective potential has one
minimum between \(z_p\) and \(z_a\), \(Q_e>0\) in the open interval, and
\(Q_e'(z_p)>0>Q_e'(z_a)\). The endpoint square-root singularities are
integrable.

The analytic limits of the scale-free logarithmic model are

\[
e\to0^+:\quad F,\Theta\to\sqrt2\,\pi,
\]

\[
e\to1^-:\quad F\to2\sqrt{2\pi},\qquad\Theta\to\pi.
\]

The second line is a limit through noncollision logarithmic-potential orbits;
it is not a rule for continuing an orbit through the singular center. It is
also nonuniform for the full exponential branch. If \(\xi=R/r_M\), deep MOND
over the entire orbit requires

\[
x_p=\xi(1-e)\gg1.
\]

Consequently the physical version of the second line is the joint limit
\(\xi\to\infty,\ e\to1^-\) with \(\xi(1-e)\to\infty\), while keeping
\(r_p\) outside the source. At fixed finite \(\xi\), taking \(e\to1\)
instead enters the Newtonian/interior region and the pure-log endpoint is
inapplicable.

| \(e\) | \(F(e)\) | \(\Theta(e)\) | \(\Delta\varpi\) |
|---:|---:|---:|---:|
| 0.1 | 4.446595614 | 4.439164764 | -105.654594474 deg |
| 0.3 | 4.477064259 | 4.408223081 | -107.427422334 deg |
| 0.6 | 4.591731415 | 4.283890053 | -114.551180074 deg |
| 0.9 | 4.847967732 | 3.928482111 | -134.914555152 deg |

The retrograde angle changes substantially with finite eccentricity, so the
near-circular epicycle value cannot be reused away from \(e=0\).

## Test-particle virial derivation

The scalar virial theorem for the logarithmic potential gives

\[
2\langle K\rangle_t
=\langle\mathbf r\cdot\nabla\Phi\rangle_t=v_\infty^2.
\]

Since \(2K=v^2\), it follows without a circular-orbit assumption that

\[
\langle v^2\rangle_t=v_\infty^2,\qquad
\bigl(\langle v^2\rangle_t\bigr)^2=GM_ba_0.
\]

This statement concerns one test-particle orbit, not the velocity dispersion
of a self-gravitating many-body galaxy. The four numerical eccentricities
above reproduce \(\langle v^2\rangle_t/v_\infty^2=1\) with maximum absolute
error \(1.20\times10^{-13}\).

## A tempting shortcut is dead

Replacing the circular radius and azimuthal period in

\[
T_\phi^4={16\pi^4r^4\over GM_ba_0}
\]

by the mean turning radius \(R\) and radial period \(T_r\) would predict a
constant coefficient. The exact eccentric law shows that the ratio of that
shortcut to the correct coefficient is

\[
{16\pi^4\over F(e)^4}.
\]

It tends to \(4\), not \(1\), as \(e\to0^+\), and to \(\pi^2/4\), not
\(1\), in the formal logarithmic \(e\to1^-\) limit. The latter is
physically approached on the full branch only in the joint limit stated above.
Thus the new law is not the old circular equation with names changed.

## Independent checks

The implementation performs all of the following live:

- SymPy nondimensionalizes the exponential flux and checks the parametric
  potential, turning-point solution, limiting force laws, virial identity,
  endpoint constants, and failed-shortcut factors.
- A seven-point, nine-decade radius grid checks that the numerical root solver
  satisfies \(y(1-e^{-y})=x^{-2}\) and remains monotone; its maximum relative flux
  residual must remain below \(5\times10^{-10}\).
- Endpoint-regularized quadratures evaluate \(F(e)\) and \(\Theta(e)\).
  A scaled arbitrary-precision branch controls cancellation through
  \(e=10^{-8}\), while an end-to-end multiprecision branch controls the sharp
  near-radial layer through \(e=0.99999\). Nonphysical interior radicands and
  integration warnings are fatal rather than silently clamped.
- Three full exponential orbits spanning turning-point eccentricities from
  0.1 to 0.9 are integrated again as nonlinear RK45 initial-value problems,
  independently of the DOP853 potential interpolation used by the quadrature.
  Pericenter and apocenter events agree with the separate quadratures with a
  maximum relative discrepancy of \(4.24\times10^{-11}\).
- Three pure-logarithmic orbits are independently integrated with RK45. Their
  pericenter events verify the displayed finite-eccentricity table at relative
  error below \(2\times10^{-9}\).
- Same-input cross-backend tests agree across the arbitrary-precision and
  dense-potential implementations at the numerical cutover for three source
  scales.
- The high-acceleration orbit \((0.01,0.03)\) recovers the Newtonian Kepler
  period and closed apsidal angle at relative error below \(2\times10^{-8}\).
- The low-acceleration orbit \((1000,3000)\) approaches the universal deep law;
  period and angle discrepancies are \(3.31\times10^{-5}\) and
  \(3.92\times10^{-5}\), respectively.
- A fixed-eccentricity Newtonian/deep comparison rejects collapsing the full
  transition surface to a function of eccentricity alone.
- Twenty-three unit tests and twelve live certificate gates pass.

No target rank, period, angle, or invariant is copied into the nonlinear ODE
measurement.

## Prior art and non-claims

Central-force apsidal methods and logarithmic-potential orbits are established
subjects. Relevant checks include Schmidt (2008),
<https://arxiv.org/abs/0803.0920>; Castelli (2013),
<https://arxiv.org/abs/1309.1594>; Valluri et al. (2012),
<https://arxiv.org/abs/1209.1342>; and Touma & Tremaine (1997),
<https://arxiv.org/abs/astro-ph/9706046>. An exponential MOND interpolation
appears in Zhao & Famaey (2006),
<https://arxiv.org/abs/astro-ph/0512425>. This limited literature check does
not certify that the boxed presentation is globally new.

This artifact does **not** prove the HPI-Delta relativistic action closes, does
not supply PPN parameters, does not test FLRW or stability, does not include
nonspherical sources or an external-field effect, and does not control the
exact \(y=0\) endpoint. Nor does its one-particle virial identity establish a
galaxy-scale BTFR theorem. The full fried-chicken theory therefore remains
**OPEN** even though this additional orbital prediction is closed conditional
on the stated branch.

## Reproduction

    python3 hpi_delta_eccentric_kepler_2026.py
    python3 -m unittest -v test_hpi_delta_eccentric_kepler_2026.py
    python3 -m py_compile hpi_delta_eccentric_kepler_2026.py test_hpi_delta_eccentric_kepler_2026.py

The run is deterministic and uses no random numbers. See
computation_manifest.json for the finite computation contract and
hpi_delta_eccentric_kepler_2026.out for a recorded run.
