# Exact-exponential MOND Kepler spectrometer, finite-e null, and curvature closure

Date: 2026-09-04

Verdict: **CLOSED as a bounded spherical weak-static prediction; not a
relativistic completion.**  The inverse two-clock law below is new to this
repository and was not located in the bounded literature search recorded in
`LITERATURE_SCOPE.md`.  That is not a claim of global novelty.  The parent
HPI-Delta action remains **DEAD** as a complete theory because its exact
force-free regular-center branch has divergent curvature.  This calculation
extracts a falsifiable positive-field exterior prediction from the same
varied weak-static branch; it does not erase that obstruction.

The strongest observational form is the exact, branch-aware and
branch-conditional
finite-eccentricity cross-radius null in section 4: it removes the central
mass, \(a_0\), source distance, and absolute clock calibration, leaving a
dimensionless apsidal/turning-radius consistency condition.  The exact forward
apsidal map was already present elsewhere in this repository; the advance here
is the explicit inverse observable, endpoint diagnosis, and cross-orbit null.

## 1. Headline: one radius, two orbital clocks, two inferred constants

For an isolated spherical exterior governed by

\[
\mu(y)=1-e^{-y},\qquad y={g\over a_0},
\]

let

\[
\Omega^2={g\over r},\qquad q={\kappa^2\over\Omega^2},
\]

where \(\Omega\) is the circular angular frequency and \(\kappa\) is the
frequency of an infinitesimal radial epicycle.  Define

\[
L={q-1\over3-q},\qquad
Y(q)=-L-W_{-1}(-Le^{-L}).
\]

Then the exact exponential law gives the inverse Kepler spectrometer

\[
\boxed{
a_0={r\Omega^2\over Y(q)},\qquad
GM=r^3\Omega^2\left[1-e^{-Y(q)}\right].
}
\]

Thus \(r,\Omega,\kappa\) determine estimators for both \(a_0\) and the central
mass in this model.  The \(a_0\) estimator does not take a baryonic mass as an
input.  A single radius by itself estimates rather than predicts: it becomes a
sharp test only through cross-radius consistency or comparison with an
external \(a_0\) or baryonic-mass measurement.  It is not a universal
identity; it is specific to the stated interpolation function on a spherical,
point-mass exterior branch.

The physical domain is

\[
y>0\quad\Longleftrightarrow\quad1<q<2.
\]

The principal branch is a trap:

\[
W_0(-Le^{-L})=-L
\]

returns \(Y=0\) for every \(L\in(0,1)\).  Only \(W_{-1}\) returns the unique
positive acceleration.  A measured \(q\notin(1,2)\), inconsistent values of
\(a_0\) at different exterior radii, or disagreement between the inferred
mass and an independently measured baryonic mass falsifies this branch under
the stated source and boundary assumptions.

## 2. Parent action and explicit weak-static branch reduction

The parent ADM action audited in `../hpi_delta_covariant_lift_2026/` is

\[
S={M_{\rm Pl}^2\over2}\int dt\,d^3x\,N\sqrt h
\left[\bar K_{ij}\bar K^{ij}-\bar K^2+{}^{(3)}R-2\Lambda
-{2\over\ell_0^2}F_{\exp}(y)\right]+S_m[g,\psi],
\]

\[
\bar K_{ij}=K_{ij}-{D^2\lambda\over2N}h_{ij},\qquad
y=\ell_0\sqrt{h^{ij}D_i\ln N D_j\ln N},\qquad
\ell_0={c^2\over a_0},
\]

\[
F_{\exp}(y)=2[(1+y)e^{-y}-1].
\]

`adm_weak_static_reduction_audit.py` now derives the frozen branch directly
from this displayed action.  Put \(\epsilon=c^{-2}\) and choose

\[
N=e^{\epsilon\Phi},\qquad
h_{ij}=e^{-2\epsilon\Psi}\delta_{ij},\qquad
N^i=0,\qquad K_{ij}=0.
\]

This is an explicit symmetry-reduced static branch expansion, not an
unrestricted variation of the full ADM theory.  In the fixed-\(a_0\)
nonrelativistic scaling associated with \(a_0\propto c^2\sqrt\Lambda\), the
program sets \(\Lambda=\epsilon^2\Lambda_2\).  After division by the common
weak scale, the leading cosmological contribution is the field-independent
constant \(-\Lambda_2\), while its generated \(\Phi,\Psi\)-dependent residual
is zero.  The mutation \(\Lambda=\epsilon\Lambda_1\) instead leaves
\(\Lambda_1(-\Phi+3\Psi)\) and fails.  Holding \(\Lambda\) fixed as
\(c\to\infty\) would require an (A)dS-background expansion and is outside this
local result.  The program constructs
the three-dimensional Christoffels and Ricci tensor from \(h_{ij}\) and
verifies with zero symbolic residual that

\[
{}^{(3)}R=e^{2\epsilon\Psi}
\left(4\epsilon\nabla^2\Psi
-2\epsilon^2|\nabla\Psi|^2\right).
\]

Consequently the \(\epsilon^2\) coefficient of
\(\tfrac12N\sqrt h\,{}^{(3)}R\) is, before and after integration by parts,

\[
2(\Phi-\Psi)\nabla^2\Psi-|\nabla\Psi|^2
\quad\longrightarrow\quad
-2\nabla\Phi\!\cdot\!\nabla\Psi+|\nabla\Psi|^2.
\]

The nonrelativistic scaling is singular but controlled:

\[
\ell_0={1\over\epsilon a_0},\qquad
y=e^{\epsilon\Psi}{|\nabla\Phi|\over a_0}
\longrightarrow {|\nabla\Phi|\over a_0}.
\]

Thus the constitutive function is retained exactly rather than Taylor-expanded
at \(y=0\), and the ADM MOND term reduces to
\(-a_0^2F_{\exp}(|\nabla\Phi|/a_0)\).  Finally a static minimally coupled point
particle gives

\[
-mc^2N+mc^2\longrightarrow-m\Phi.
\]

With the restored relation
\(M_{\rm Pl}^2=c^4/(8\pi G)\), the common weak gravitational scale is
\(M_{\rm Pl}^2\epsilon^2=1/(8\pi G)\).  Replacing the point mass by a dust
rest-mass density and dividing \(-\rho\Phi\) by that computed common scale
therefore derives \(-8\pi G\rho\Phi\).  The high-acceleration no-slip Euler
equation is generated independently as

\[
2\left(\Phi''+{2\Phi'\over r}\right)-8\pi G\rho=0,
\]

so the stated Planck--\(G\) relation gives the required Poisson normalization.
This is a factor-consistency derivation, not an independent measurement or
derivation of \(G\).  Reversing the sign in the spatial metric, doubling the
overall gravitational prefactor, using the wrong Planck scaling, or changing
the \(\Lambda\) scaling produces nonzero residuals in the executable negative
controls.

The static auxiliary condition is also generated rather than merely assigned.
Writing \(b=D^2\lambda/N\), direct contraction gives

\[
\bar K_{ij}\bar K^{ij}-\bar K^2=-{3\over2}b^2.
\]

For a Fourier mode on the leading local branch, the action density is
\(-3k^4\lambda_k^2/4\) and its Euler equation is
\(-3k^4\lambda_k/2=0\).  Therefore \(D^2\lambda=\bar K_{ij}=0\) for
\(k\ne0\); for \(k=0\), \(D^2\lambda=0\) identically and the homogeneous
kernel remains separate.  Direct symbolic differentiation of the displayed
reduced density gives a zero Hessian with respect to \(\dot\lambda\).  This is
a branch result, not the parent action's
full nonlinear constraint count.

After removing the common positive normalization and angular factor, the
derived radial density is

\[
{\cal L}_r=r^2\left[-2\Phi'\Psi'+(\Psi')^2
-a_0^2F_{\exp}(\Phi'/a_0)-8\pi G\rho\Phi\right].
\]

`derive_action_and_flux()` differentiates this density with SymPy while
keeping \(\Phi\) and \(\Psi\) independent.  On the attractive branch it
obtains

\[
{d\over dr}\left[r^2(\Phi'-\Psi')\right]=0,
\]

and

\[
{d\over dr}\left[r^2(\Psi'-e^{-\Phi'/a_0}\Phi')\right]
=4\pi G\rho r^2.
\]

All integrations by parts are understood on a finite-radius domain with fixed
boundary data, equivalently with compactly supported variations, followed by
physical matching.  They do not assume that a deep-MOND logarithmic potential
vanishes at spatial infinity.  Regular finite-source interior data,
distributionally source-free slip, and matching to the exterior set the
integration constant to zero; asymptotic
decay alone would still permit a harmonic \(C/r\) term.  Thus
\(\Phi'=\Psi'\) is imposed only after both variations, and

\[
{1\over r^2}{d\over dr}\left[r^2
(1-e^{-\Phi'/a_0})\Phi'\right]=4\pi G\rho.
\]

The primitive is generated in the same run:

\[
{\cal G}(y)=y^2+2(1+y)e^{-y}-2,
\qquad {{\cal G}'(y)\over2y}=1-e^{-y}.
\]

For exterior mass \(M\), integration gives

\[
\boxed{(1-e^{-g/a_0})g={GM\over r^2}}.
\]

Changing the \((\nabla\Psi)^2\) coefficient from one to two is a live
negative control: the derived slip becomes \(\Psi'/\Phi'=1/2\), and the
modulus becomes \(1/2-e^{-y}\).  The desired result is therefore not inserted
after variation.

## 3. Derivation of the second clock and exact inverse

For the test-particle effective potential

\[
V_{\rm eff}=\Phi(r)+{\ell^2\over2r^2},
\]

the circular condition and second variation give

\[
\ell^2=r^3g,\qquad
\Omega^2={g\over r},\qquad
\kappa^2=g'+{3g\over r}.
\]

Differentiating the exterior field equation, rather than assigning a rotation
curve slope, gives

\[
L(y)={d\ln\mu\over d\ln g}={y\over e^y-1},
\qquad
{d\ln g\over d\ln r}=-{2\over1+L},
\]

and hence

\[
\boxed{
q(y)={\kappa^2\over\Omega^2}
={1+3L(y)\over1+L(y)}
={e^y-1+3y\over e^y-1+y}.
}
\]

Solving the rational part yields \(L=(q-1)/(3-q)\).  The remaining
transcendental equation is

\[
L(e^y-1)=y.
\]

Writing \(z=-(y+L)\) gives \(ze^z=-Le^{-L}\), proving the branch-resolved
inverse in section 1.  No numerical root finder is needed for the final law.

The inverse is ill-conditioned at both asymptotic endpoints.  A bounded
numerical minimization of

\[
{\cal C}(y)=\left|{d\ln y\over d\ln q}\right|
\]

over \(e^{-12}\le y\le e^{12}\) finds its best point at

\[
y=3.0601446758,\quad q=1.2616538376,\quad
{\kappa\over\Omega}=1.1232336523,\quad {\cal C}=2.5094826306.
\]

This is a numerical design optimum over the stated interval, not an analytic
global-minimum theorem.  Because \(q=(\kappa/\Omega)^2\), the corresponding
condition number with respect to the directly measured frequency ratio is
\(2{\cal C}=5.0189652612\).  Neither number includes covariance among
\(r,\Omega,\kappa\), finite-eccentricity bias, source modelling, or external-
field systematics.  Deep-MOND and Newtonian measurements become rapidly poor
estimators of \(a_0\), even though the forward prediction remains well-defined
as a one-sided limit.

The numerical functions select precision adaptively (up to a documented
2000-decimal-digit safety cap) because the two endpoints
are delicate: near \(q=2\), the Lambert argument approaches \(-1/e\)
quadratically.  The tests now include round trips at \(y=10^{-100}\) and
\(y=200\).  A finite floating-point \(q\) already rounded to exactly 1 or 2 has
irretrievably lost the information and is correctly rejected.  Thus the
analytic domain is all \(1<q<2\), while the executable inverse covers the
precision-resolvable interior supplied by its inputs; it cannot recreate
digits a measuring process or binary float did not retain.

## 4. Finite-eccentricity completion and distance-free null

The circular ratio is not assigned to a visibly eccentric orbit.  Let
\(r_0\) be the circular guiding radius at the orbit's fixed angular momentum,
\(\Omega_0^2=g(r_0)/r_0\), and let

\[
q_e=\left({\Omega_r\over\Omega_\phi}\right)^2
=\left({2\pi\over\Theta}\right)^2,
\]

where \(\Theta\) is the measured apsidal angle.  Define the turning-point
eccentricity and mean radius by

\[
e={r_a-r_p\over r_a+r_p},\qquad R={r_a+r_p\over2}.
\]

`finite_eccentricity_null_2026.py` generates a Poincare-Lindstedt expansion of
the fixed-angular-momentum effective potential.  With

\[
s=q_0-3,\qquad D={dq_0\over d\ln r},\qquad
E={d^2q_0\over d(\ln r)^2},
\]

the generated cubic and quartic coefficients are

\[
u_3=D+s^2-s-12,
\]

\[
u_4=E+3(s-1)D+(s-2)(s^2-s)+60.
\]

The \(-12,+60\) terms come from differentiating the centrifugal potential.
Secular cancellation and the independently generated mean-azimuth correction
then give

\[
\boxed{
q_e=q_0\left[1+{\cal C}_e(y)e^2+O(e^4)\right],
}
\]

\[
\boxed{
{\cal C}_e={u_4\over8q_0}-{5u_3^2\over24q_0^2}
-3-{u_3\over q_0}.
}
\]

The order symbol is now proved rather than assumed.  Introduce a signed
first-harmonic amplitude \(a\), allow both odd frequency terms
\(w_1a+w_3a^3\), and solve the secular equations without setting them to zero.
The program obtains

\[
w_1=w_3=0,\qquad
w_2={u_4\over8q_0}-{5u_3^2\over24q_0^2},
\]

while a live \(w_3=1\) mutation leaves residual \(-q_0\).  The odd terms in
the mean azimuthal clock also vanish.  Exchanging the signed turning-point
eccentricity \(e_s\mapsto-e_s\) merely swaps \(r_a,r_p\); analyticity about a
nondegenerate stable circle therefore makes the periods and mean radius even.
The generated turning equations explicitly give

\[
e_s=a+O(a^3),\qquad {R\over r_0}=1-{u_3\over6q_0}a^2+O(a^4).
\]

Consequently \(a^2=e_s^2+O(e_s^4)\).  This proves the displayed \(O(e^4)\)
remainder pointwise at each finite \(y>0\), and uniformly only on compact
\(y\)-intervals where the inverse stays away from its endpoints.  It does not
provide a universal numerical remainder coefficient.

The last two terms are load-bearing: omitting the azimuthal-clock correction
gives \(-11/6\), rather than the correct \(+1/6\), in deep MOND.  Exact
Kepler and isotropic-harmonic controls both give \({\cal C}_e=0\).

For the exponential exterior,

\[
D={4L(y+L-1)\over(1+L)^3},
\]

\[
E=-{8L\over(1+L)^5}
\left[L^3+3L^2y-5L^2+2Ly^2-6Ly+5L-y^2+3y-1\right].
\]

The fully explicit transition is

\[
\boxed{
{\cal C}_e(y)={L P_e(y,L)\over6(1+L)^4(1+3L)^2},
}
\]

\[
\begin{aligned}
P_e={}&9L^5+54L^4+(192-33y)L^3\\
&+(42+105y-36y^2)L^2\\
&+(-41+65y-14y^2)L+6y^2-9y.
\end{aligned}
\]

It obeys

\[
{\cal C}_e\to0\quad(y\to\infty),\qquad
{\cal C}_e\to{1\over6}\quad(y\to0).
\]

Thus a finite-e deep-MOND orbit predicts
\(q_e=2+e^2/3+O(e^4)\); a measured ratio slightly above two is not by itself
a falsification.  Representative values of \({\cal C}_e\) are 0.167129 at
\(y=0.1\), 0.161336 at \(y=1\), 0.220022 at \(y=3\), and 0.229078 at
\(y=7\).

The same expansion generates the guiding-radius correction

\[
\boxed{r_0=R\left[1+{u_3\over6q_0}e^2\right]+O(e^4).}
\]

For each orbit, solve

\[
q_e=q_0\left[1+{\cal C}_e(Y(q_0))e^2\right]
\]

for \(q_0\in(1,2)\), using the implicit solve when \(q_e\ge2\).  Define

\[
X(q)=Y(q)\left[1-e^{-Y(q)}\right].
\]

The exterior flux law implies \(r_0^2X(q_0)=GM/a_0\).  Therefore two orbit
families around the same isolated source must satisfy the new null

\[
\boxed{
{\cal N}_{ij}=\ln{r_{0,i}^2X(q_{0,i})\over
r_{0,j}^2X(q_{0,j})}=O(e_i^4+e_j^4).
}
\]

This version is operationally cleaner than the one-radius estimator:
\(q_e=(2\pi/\Theta)^2\) uses an apsidal angle, while \(e,R\) use turning
radii.  For angular radii in one system the common distance cancels, as do
\(M,a_0\), and the absolute time calibration.  It remains restricted to the
isolated point-mass exterior and small eccentricity.

The endpoint \(2(1+e^2/6)\) belongs to the truncated \(O(e^2)\) model; it is
not a physical ceiling.  The exact logarithmic-potential orbit at \(e=0.03\)
has

\[
q_e=2.0003001482>2.0003000000.
\]

Accordingly the executable point inverse labels a datum outside the truncated
image as **asymptotically unresolved**, not physically excluded.  The interval
API accepts a caller-supplied absolute bound on the omitted \(q_e\) remainder
and returns a one-sided \(y\)-interval when it touches \(y=0\) or \(y=\infty\).
No such bound is silently invented.  Its endpoint diagnostic records the
ratio of the model-image margin to \(e^4\); a small ratio warns that formally
higher-order terms are amplified by the inverse.

### 4.1 Exact all-orders eccentric null

The small-\(e\) expansion is useful for a closed analytic coefficient, but it
is not necessary for the observable.  Define

\[
r_M=\sqrt{GM/a_0},\qquad x={r\over r_M},\qquad
X(y)=y(1-e^{-y}).
\]

The exact exterior flux law is simply \(x^2X(y)=1\).  Let \(y_p>y_a\) be the
accelerations at pericenter and apocenter.  Turning-point geometry gives

\[
X_a=X_p\left({1-e\over1+e}\right)^2.
\]

With

\[
A(y;y_p)=\int_y^{y_p}{sX'(s)\over X(s)^{3/2}}\,ds,\qquad
\lambda^2={A(y_a;y_p)\over X_p-X_a},
\]

eliminating the orbit energy and angular momentum yields the exact full-cycle
apsidal angle

\[
\boxed{
\Theta(y_p,e)=\lambda\int_{y_a}^{y_p}
{X'(y)\,dy\over
\sqrt{X(y)}\sqrt{\lambda^2[X_p-X(y)]-A(y;y_p)}} .
}
\]

The factor is the full peri-to-peri or apo-to-apo cycle.  Dropping the
outbound-to-inbound factor produces \(\Theta=\pi\), \(q_e=4\), in the Kepler
limit instead of the correct \(\Theta=2\pi\), \(q_e=1\); that error is an
analytic negative control.  The production factor is independently exercised
by the Newtonian limit and the separate radius-space quadrature cross-check.

For an observed \(q_e=(2\pi/\Theta)^2\), a selected positive solution \(y_p\)
then gives

\[
\boxed{
I=R^2(1-e)^2X(y_p)={GM\over a_0}.
}
\]

Thus two orbit families around the same source obey the all-orders null

\[
\boxed{
{\cal N}^{\rm exact}_{ij}=
\ln {R_i^2(1-e_i)^2X(y_{p,i})\over
R_j^2(1-e_j)^2X(y_{p,j})}=0.
}
\]

There is no eccentricity-series remainder in this identity.  A common
distance multiplying angular turning radii cancels, as do \(M\), \(a_0\), and
absolute clock calibration.  The numerical program integrates a normalized
dimensionless potential, removes both square-root endpoints, reproduces the
exact logarithmic and Kepler limits, round-trips three finite-\(e\) cases, and
recovers \(r_M^2=25\) from two different synthetic orbit families with a log
null of \(3.7\times10^{-13}\).

The qualification is important: global injectivity of
\(y_p\mapsto\Theta(y_p,e)\) has not been proved for every \(0<e<1\).  The
executable inverse scans 32 cells uniformly in \(\log y_p\), refines every
detected sign-changing root, reports each local derivative/condition number,
and makes the set of candidate invariants executable.  The scalar API refuses
to return unless exactly one branch is detected.  This scan can still miss an
even-multiplicity or narrower-than-cell root, which is recorded in its output;
it is evidence, not a global injectivity theorem.  The scalar null is therefore
branch-conditional, while the set-valued API tests all detected branch pairs.
The Newtonian and deep-MOND plateaus are intrinsically ill-conditioned.
Nonzero endpoint residuals within the empirical \(10^{-8}\) numerical guard
of either finite inverse endpoint are returned as
`ENDPOINT_NUMERICALLY_UNRESOLVED`, not as invented root records; an exact
computed endpoint equality remains admissible, and accepted interior roots
carry a forward-
\(q_e\) residual certificate.  A detected interior root does not override an
unresolved endpoint: the scalar inverse refuses that mixed case, and the
detected-set null propagates both per-orbit endpoint warnings.
The guard is more than four times the worst absolute disagreement
\(2.294\times10^{-9}\) in a 64-point comparison with the independently coded
radius-space quadrature across both inverse endpoints.  That is a bounded
numerical safety audit, not a rigorous global error theorem.

The displayed quadrature is exact for \(y_p>0\) and \(0<e<1\), but the present
double-precision implementation claims only

\[
10^{-6}\le y_p\le25,\qquad0.01\le e\le0.7,
\]

with the inverse restricted further to \(10^{-5}\le y_p\le20\).  Inputs below
the forward floor now fail loudly: the old absolute-tolerance force root could
silently collapse the two turning accelerations as \(y_p\to0\).  The analytic
logarithmic limit controls that zero-field endpoint; the numerical program
does not pretend to resolve it arbitrarily closely.

## 5. Two clocks also determine local weak curvature

The metric tensor is not inferred from the orbit equation.  The code first
constructs the linearized Riemann tensor of

\[
ds^2=-(1+2\Phi/c^2)c^2dt^2
+(1-2\Psi/c^2)d\mathbf x^2
\]

with separate radial/tangential Hessian eigenvalues

\[
p_\Phi=\Phi'',\quad t_\Phi={\Phi'\over r},\qquad
p_\Psi=\Psi'',\quad t_\Psi={\Psi'\over r}.
\]

Before no slip, contraction gives

\[
c^2R=-2(p_\Phi+2t_\Phi)+4(p_\Psi+2t_\Psi),
\]

\[
c^4K=4\left[p_\Phi^2+2t_\Phi^2+p_\Psi^2+2t_\Psi^2
+(p_\Psi+2t_\Psi)^2\right].
\]

Only then is \(\Phi=\Psi\) imposed.  Eliminating \(\Phi'\) and \(\Phi''\)
with the independently derived orbital clocks gives

\[
\boxed{c^2R=2(\kappa^2-\Omega^2)},
\]

\[
\boxed{
c^4K=4\left(3\kappa^4-14\kappa^2\Omega^2+23\Omega^4\right)}.
\]

Equivalently,

\[
K=3R^2-{16R\Omega^2\over c^2}+{48\Omega^4\over c^4}.
\]

These are leading weak-field identities; omitted terms are higher order in
the metric potentials.  They are not specific to MOND until \(q(y)\) is
inserted.  For the exact exponential exterior,

\[
\boxed{{c^2R\over\Omega^2}={4y\over e^y-1+y}},
\]

\[
\boxed{
{c^4K\over\Omega^4}
={16(3+2L+2L^2)\over(1+L)^2},
\qquad L={y\over e^y-1}.
}
\]

Three exact fingerprints are

| regime | \(\kappa^2/\Omega^2\) | \(c^2R/\Omega^2\) | \(c^4K/\Omega^4\) |
|---|---:|---:|---:|
| Newton/Schwarzschild exterior | 1 | 0 | 48 |
| deep-MOND exterior | 2 | 2 | 28 |
| exact exponential smooth-density center | \(7/2\) | 5 | 43 |

The deep-MOND coefficient 28 is not claimed new: Hernandez, Sussman, and
Nasser obtained the equivalent deep-isothermal Kretschmann combination.  The
new repository result is the full exponential transition together with its
branch-correct inverse spectrometer.

## 6. Independent attempts to break it

The main test suite contains 20 tests.  It checks both action variations,
the primitive, the generated Riemann contractions, independent treatment of
\(\Phi\) and \(\Psi\), the exact exponential transition, both real Lambert
branches, invalid-domain rejection, parameter recovery, endpoint precision,
and three negative controls.

The separate ADM-reduction suite contains 12 tests.  In addition to the exact
branch expansion and dust normalization, it generates the spatial Ricci scalar
directly from the metric, records all symbolic residuals, and proves that both
coefficient mutations and a wrong \(\ell_0\)-scaling mutation fail.  It also
derives the static auxiliary Fourier equation, separates \(k=0\) from
\(k\ne0\), and checks the spherical \(4\pi r^2\) reduction on the attractive
\(\Phi'>0\) branch.  This closes the earlier provenance gap between
the displayed parent action and the reduced density, within the explicitly
stated symmetry-reduced branch.

The finite-e symbolic suite contains 15 tests.  It generates the second
harmonic and secular-cancellation equations, force-derivative recurrence,
azimuthal clock correction, signed-amplitude parity equations, exact
exponential polynomial, endpoint limits, closed-orbit controls, an implicit
\(q_e>2\) inversion, a truncation-aware endpoint interval, and synthetic
nulls.  Its
deep-MOND negative control shows that a radial-period-only calculation would
return \(-11/6\), not \(+1/6\).

The exact all-orders eccentric suite contains 16 tests.  It derives the
dimensionless scaling and turning-energy cancellation symbolically, evaluates
the endpoint-regularized apsidal map, verifies the Newton and logarithmic
limits, round-trips three selected roots, accepts exact bracket and interior-
node roots, rejects false roots one floating-point step or \(2.5\times10^{-11}\)
from an unresolved endpoint, enforces the audited inverse window, enumerates
a synthetic two-branch counterexample, refuses a synthetic interior root when
an endpoint remains unresolved, and checks an exact
two-orbit null and common-distance cancellation.  It also cross-checks three
orbits against the older, independently coded radius-space quadrature and
audits 64 endpoint cases to calibrate the numerical guard.  It proves that
caller mutation cannot poison the cached forward calculation.
These tests certify the displayed forward law and bounded detected branches;
they do not constitute a global injectivity theorem.

`independent_metric_audit.py` imports none of the production functions.  It
builds the exact metric in spherical coordinates, including the nonzero flat
background Christoffels, differentiates the exact curvature at zero weak-field
amplitude, and obtains

\[
R^{(1)}=2f''+{4f'\over r},
\]

\[
K^{(2)}=12(f'')^2+{16f'f''\over r}+{32(f')^2\over r^2}.
\]

Both residuals against the production tensor construction are exactly zero.

`independent_orbit_audit.py` imports none of the production functions.  It
sets \(GM=a_0=1\), solves

\[
y(1-e^{-y})={1\over r^2}
\]

afresh at every force evaluation, integrates five slightly eccentric orbits
from \(y=0.1\) to 7, and measures successive radial maxima.  Across those
runs:

- maximum relative clock-ratio error from direct orbits:
  \(2.67\times10^{-10}\);
- maximum relative error from a five-point force derivative:
  \(1.71\times10^{-12}\);
- maximum recovered-\(a_0\) error using the measured orbit clock:
  \(1.70\times10^{-8}\);
- maximum recovered-\(GM\) error:
  \(1.62\times10^{-8}\).

These are numerical checks over five inputs, not universal proofs.  The
symbolic derivation supplies the identity; the integrations test its
implementation and interpretation.

`independent_finite_e_orbit_audit.py` likewise imports none of the production
formula.  It root-solves the implicit force at every ODE evaluation and
measures apsidal angles and both turning radii for 12 nonlinear orbits:
\(y=0.1,1,3,7\) at three apoapsis offsets.  At offset 0.003 the largest
relative error in the recovered \({\cal C}_e\) is
\(2.61\times10^{-5}\).  The maximum corrected-null residuals are
\(1.11\times10^{-9}\), \(1.34\times10^{-7}\), and
\(1.02\times10^{-5}\) for offsets 0.003, 0.01, and 0.03, respectively,
consistent with an \(O(e^4)\) remainder.  At the largest offset the
uncorrected radius/clock null misses by as much as \(2.02\times10^{-2}\), so
the improvement is not a consequence of an already tiny baseline error.
The same independent file also integrates the exact deep-MOND logarithmic
potential at \(e=0.03\).  Its measured \(q_e=2.0003001482\) lies
\(1.48\times10^{-7}\) above the truncated endpoint, proving that the old hard
ceiling would have rejected a valid orbit.

## 7. Scope, failure modes, and scientific status

The inverse spectrometer assumes all of the following:

- a static isolated spherical exterior with constant enclosed baryonic mass;
- the positive-field branch \(y>0\);
- infinitesimal radial oscillations for the exact circular inverse, or
  a pointwise small-\(e\) asymptotic correction.  The implementation is
  numerically exercised only through \(e=0.03\), on the recorded interior
  grid, and this is not a uniform error theorem;
- the weak-field physical metric and leading no-slip relation;
- negligible external-field effect and nonspherical multipoles.

Here \(r\) is the isotropic/Euclidean radius of the leading weak-field chart,
and \(\Omega,\kappa\) are coordinate-time frequencies in its asymptotic time
normalization.  This bundle does not supply the 1PN map to circumferential
radius, local proper periods, or a finite cosmological/external-field time
normalization.  Those conversions and their covariance are required before
advertising a precision-observational estimator.

For an extended spherical source with

\[
m={d\ln M_b\over d\ln r},
\]

the clock law instead reads

\[
{\kappa^2\over\Omega^2}={1+3L+m\over1+L};
\]

the exterior inverse is invalid unless \(m=0\) is established.  A disk cannot
be substituted for the spherical source.  A radial frequency inferred only
by differentiating the same fitted rotation curve is not an independent
clock measurement, although it can still test the functional identity.

Most importantly, this result does **not** turn HPI-Delta into fried chicken.
The same exact law has a divergent no-slip curvature at an isolated smooth
force-free center, and the full action lacks a completed acceptable PPN and
inhomogeneous-cosmology closure.  The honest classification is therefore:

- **new circular Kepler inverse:** CLOSED within its stated weak-static
  exterior scope;
- **finite-e null:** CLOSED as a pointwise asymptotic identity, with endpoint
  inversions explicitly conditional on a supplied remainder bound;
- **exact all-orders eccentric null:** CLOSED as a forward and detected-set/
  branch-conditional identity on the stated numerical window; global inverse
  uniqueness remains OPEN;
- **HPI-Delta as a full relativistic theory:** DEAD;
- **the broader causal/nonlocal two-tensor route:** OPEN.

The weak-static density and dust normalization are now derived from the
displayed action on the stated branch.  This still cannot be cited as a full
relativistic closure: the reduction is symmetry-restricted, while the parent
action's unrestricted regular-center, Dirac, PPN, and cosmological gates retain
the adverse/open verdicts stated above.

## 8. Reproduction

From the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s qwen_claude_field_theory/closure_2026/exponential_mond_kepler_spectrometer_2026 -p 'test_*.py' -v
python3 qwen_claude_field_theory/closure_2026/exponential_mond_kepler_spectrometer_2026/exponential_mond_kepler_spectrometer_2026.py
python3 qwen_claude_field_theory/closure_2026/exponential_mond_kepler_spectrometer_2026/adm_weak_static_reduction_audit.py
python3 qwen_claude_field_theory/closure_2026/exponential_mond_kepler_spectrometer_2026/finite_eccentricity_null_2026.py
python3 qwen_claude_field_theory/closure_2026/exponential_mond_kepler_spectrometer_2026/exact_finite_e_kepler_null_2026.py
python3 qwen_claude_field_theory/closure_2026/exponential_mond_kepler_spectrometer_2026/independent_metric_audit.py
python3 qwen_claude_field_theory/closure_2026/exponential_mond_kepler_spectrometer_2026/independent_orbit_audit.py
python3 qwen_claude_field_theory/closure_2026/exponential_mond_kepler_spectrometer_2026/independent_finite_e_orbit_audit.py
python3 qwen_claude_field_theory/closure_2026/exponential_mond_kepler_spectrometer_2026/verify_computation_manifest.py qwen_claude_field_theory/closure_2026/exponential_mond_kepler_spectrometer_2026/computation_manifest.json --require-tracked
```

The final command performs strict JSON parsing, rejects unsafe/duplicate
paths and non-finite constants, requires every declared artifact to be
git-tracked, and recomputes every recorded SHA-256 byte-for-byte.  The git
commit pins the manifest itself, avoiding a self-referential commit hash
inside that manifest.
