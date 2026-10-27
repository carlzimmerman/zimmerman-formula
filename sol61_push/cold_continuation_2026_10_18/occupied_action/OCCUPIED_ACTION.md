# A local density-constrained action with an exact finite-stock edge

Lane: CE-CONT-OCC-2026-10-18. Task base: CE-FM-080,
`ea2da902eeddc0a9612e5ef0d393ed6f3c794e37`. Observed read-base HEAD:
`123fefe43e02bcd44fe919fd11613ec83553bc54`. Exact source hashes are in
`INPUT_SHA256.txt`. Owner: occupied_action subagent; write scope: this directory.

The result is **conditional on a new Newtonian constrained-fluid action**.
It gives an exact regular spherical equilibrium with finite conserved stock,
nonnegative settled and baryonic densities, positive compressibility, and an
interface derived from variations. It escapes CE-FM-079's exterior theorem by
changing the admissible polarization variations through a local density
constraint. It does not derive that constraint from the original microscopic
carrier, select a cosmic supply, produce a halo, or establish a relativistic
or causal completion. No observational score is claimed.

## 1. Target and relation to earlier results

Retain the physical dictionary

\[
 K=4\pi G,\qquad u=KP_r,\qquad
 \rho_t=\nabla\cdot P\geq0,\qquad
 m(r)=4\pi r^2P_r={r^2u\over G}.
\]

CE019/020 already proved that a fixed-supply constrained radial energy can
have a finite edge. Repeating its annulus optimizer would add no information.
The present target is different: provide a local first-order action including
the conserved current, identify the multiplier in both reciprocal field and
fluid equations, derive the interface conditions, and give a regular-center
exact witness with positive baryonic source. No numerical optimizer is used.

Three discriminators are executed below: a simple occupation gate changes the
mass dictionary or fails in vacuum; a density constraint supplies the missing
vacuum multiplier; and a positive-compressibility exact solution checks all
bulk, interface, and vacuum inequalities. The last construction is a new
effective model, not evidence that the original independent-P action already
contains these degrees of freedom.

## 2. Local action and reciprocal equations

Let \(\rho\geq0\) be the settled rest-mass density, \(\theta\) a velocity
potential, \(v=\nabla\theta\), and \(\lambda\) a multiplier. On a Newtonian
fixed spatial geometry take

\[
\begin{split}
S=\int dt\,d^3x\{&-\rho[\partial_t\theta+|\nabla\theta|^2/2]-e(\rho)
 -{|\nabla\Phi|^2\over2K}+P\cdot\nabla\Phi-W(|P|)\\
&-{\gamma\over2}\partial_iP_j\partial_iP_j
 -(\rho_b+\rho_f)\Phi+\lambda(\rho-\nabla\cdot P)\}.
\end{split}                                                    \tag{1}
\]

Here \(\rho_b,\rho_f\) are prescribed nonnegative sources in this restricted
construction. The exact witness has \(\rho_f=0\). The full rational W is
retained:

\[
W={-a_0u-a_0^2\log(1-u/a_0)\over K},\quad
0\leq u=K|P|<a_0,\quad
W_P={a_0u\over a_0-u}\widehat P.                              \tag{2}
\]

Varying every displayed dynamical field gives

\[
\begin{array}{rl}
\delta\theta:&\partial_t\rho+\nabla\cdot(\rho v)=0,\\
\delta\lambda:&\rho=\nabla\cdot P,\\
\delta\Phi:&\Delta\Phi=K(\rho_b+\rho_f+\nabla\cdot P),\\
\delta P:&W_P-\gamma\Delta P=\nabla\Phi+\nabla\lambda,\\
\delta\rho\ (\rho>0):&
 \partial_t\theta+|v|^2/2+e'(\rho)-\lambda=0.
\end{array}                                                     \tag{3}
\]

Thus

\[
 {Dv\over Dt}=\nabla\lambda-\nabla e'(\rho)
 =W_P-\gamma\Delta P-\nabla\Phi-\nabla e'(\rho).                \tag{4}
\]

The multiplier force has not been added only to the response equation; its
opposite occurrence in the material chemical potential is fixed by the same
action. The total settled stock \(S=\int\rho\,d^3x\) is conserved for zero
material flux at infinity. It equals the polarization flux through infinity.
The coupling \(P\cdot\nabla\Phi\), after integration by parts, is exactly
\(-\rho\Phi\) under the constraint and vanishing infinity boundary term.
Consequently the settled density is counted once in Poisson's equation;
adding a second \(-\rho\Phi\) term would double count it.

For a static state write \(\theta=-\mu t\). The density equation and its
one-sided extension to vacuum are

\[
 \lambda=e'(\rho)-\mu\quad(\rho>0),\qquad
 \lambda\leq e'(0)-\mu\quad(\rho=0).                           \tag{5}
\]

The inequality is the KKT condition for minimizing the fixed-stock energy,
equivalently maximizing the concave density part of the static action.
It is essential: there is no freely varied vacuum fluid density of both signs.

In spherical symmetry with no central flux and
\(b+f=G(M_b+M_f)/r^2\), (3) gives

\[
g=b+f+u,\qquad
R(u)-h\Delta_vu=b+f+\lambda',\qquad
R(u)={u^2\over a_0-u},\quad h={\gamma\over K}.                  \tag{6}
\]

Inside the carrier, \(\lambda'=d e'(\rho)/dr\). For
\(e(\rho)=\kappa\rho^2/2\), \(\kappa>0\),

\[
\rho={u'+2u/r\over4\pi G},\qquad
{d e'(\rho)\over dr}={\kappa\over4\pi G}\Delta_vu,
\qquad -H\Delta_vu+R(u)=b+f,
\quad H=h+{\kappa\over4\pi G}>0.                               \tag{7}
\]

Positive compressibility renormalizes the radial longitudinal stiffness.
It does not by itself make the independent full-W exterior finite. The
constraint and vacuum inequality, rather than this coefficient change, do so.

## 3. Edge matching and a useful necessary inequality

At a material-vacuum surface without surface action or surface mass, finite
\(\gamma>0\) requires continuous \(P\). Integration of the P variation gives

\[
 [\gamma\partial_nP+\lambda n]=0.                              \tag{8}
\]

The sign convention in the jump is exterior minus interior; either jump
orientation gives the same zero condition. The gravitational potential and
normal gravitational field are continuous when there is no surface density.
The material boundary moves with \(v\cdot n\) by continuity. A static sharp
positive-density jump is incompatible with the variational matching for a
convex \(e\) in this model. Indeed (8), (5), and the spherical constraint give

\[
 0=4\pi Gh\rho_-+e'(\rho_-)-\mu-\lambda_+
 \geq4\pi Gh\rho_-+e'(\rho_-)-e'(0)\geq0.                    \tag{9}
\]

which forces \(\rho_-=0\) when \(h>0\) and \(e\) is convex. For a smooth
edge at \(r=E\), therefore

\[
m(E)=S,\quad m'(E)=0,\quad
u(E)={GS\over E^2},\quad u'(E)=-{2GS\over E^3},\quad
\lambda(E)=e'(0)-\mu.                                        \tag{10}
\]

For \(\rho\to0\), the barotropic pressure
\(p=\rho e'-e\) tends to zero if \(e(0)=0\) and \(e'\) is finite. In the
smooth witness below, \(P,\partial P,\Phi,\partial\Phi,\lambda\) and all
varied carrier/constraint/field Lagrangian terms match, while \(p=0\) at the
edge. Their local translation stress therefore has no jump or delta surface
force. This checks the carrier shape variation as well as the P flux
variation. The prescribed baryon source is held fixed in that variation;
its own mechanical support is not supplied. No carrier wall, tension, or
compensating negative shell is inserted.

For the quadratic EOS, positivity immediately inside a smooth edge requires
\(m''(E^-)\leq0\). Equation (7) then gives the necessary condition

\[
 R(GS/E^2)\leq b(E)+f(E).                                     \tag{11}
\]

If the external mass \(Q=M_b+M_f\) is already constant there, this is
\(E^2\geq (G/a_0)(S+S^2/Q)\). Equality is the zero-stiffness cap edge;
strict inequality is compatible with a taper. This is an edge discriminator,
not a general formula determining E from a supplied stellar source.

Outside all material sources, set \(u=GS/r^2\), \(\rho=0\).
Then \(\Delta_vu=0\), but the response equation is now

\[
 \lambda'(r)=R(GS/r^2)-{GQ\over r^2}.                          \tag{12}
\]

If (11) holds at the edge, \(r^2R(GS/r^2)\) decreases beyond it. Hence
\(\lambda'\leq0\) and integrating outward from (10) obeys the vacuum
inequality (5). The precise failed hypothesis of CE-FM-079 is the everywhere
freely varied equation \(-h\Delta_vu+R=b+f\), not nonnegative density, finite
mass, or the mass-flux dictionary.

## 4. Exact regular finite-stock witness

Use dimensionless \(G=a_0=E=1\), with

\[
S={1\over10},\quad h={1\over200},\quad
\kappa={\pi\over50},\quad H={1\over100},\quad \mu=0.
\]

Define for \(0\leq r\leq1\)

\[
\begin{split}
m(r)&={1\over10}\left({5r^3\over2}-{3r^5\over2}\right),\\
u(r)&={r\over4}-{3r^3\over20},\\
\rho(r)&={3\over16\pi}(1-r^2),\qquad
\lambda(r)={3\over800}(1-r^2),\\
Q(r)&={r^2u(r)^2\over1-u(r)}+{3r^3\over200}.
\end{split}                                                   \tag{13}
\]

For \(r\geq1\), set \(m=S\), \(u=S/r^2\), \(\rho=0\),
\(Q=Q(1)=47/1800\), and

\[
\lambda(r)=\int_1^r\left[{(1/10)^2\over s^2(s^2-1/10)}
                         -{47\over1800s^2}\right]ds.          \tag{14}
\]

The baryonic enclosed mass is \(M_b=Q\); \(M_f=0\). The gravitational
field is \(g=(Q+m)/r^2\), and the isolated potential is
\(\Phi(r)=-\int_r^\infty g(s)ds\). All sources and fields are regular
at the center, and the potential is finite there. Here \(\Delta_vu=-3r/2\)
inside, so (7), the P equation with h, and the pressure/multiplier equation
are exact identities. The potential value is not needed to certify the
derivative equations, but its isolated normalization exists and is fixed.

The density and stock checks are exact:

\[
 \rho\geq0,\quad 4\pi\int_0^1r^2\rho\,dr={1\over10},\quad
 m'={3\over4}r^2(1-r^2)\geq0,\quad
 u_{\max}={\sqrt5\over18}<{1\over8}<1.                       \tag{15}
\]

For completeness the baryonic source also has nonnegative local density.
Write \(R=u^2/(1-u)\). Then

\[
 {Q'\over r^2}={2R\over r}+R'(u)u'+{9\over200}.
\]

For \(0<r\leq\sqrt5/3\), \(u'\geq0\), so this is positive.
For \(\sqrt5/3\leq r\leq1\), use
\(1/10\leq u\leq1/8\), \(u'\geq-1/5\), and
\(0\leq R'(u)\leq15/49\). Therefore

\[
 {Q'\over r^2}\geq{1\over50}-{3\over49}+{9\over200}
 ={37\over9800}>0.                                           \tag{16}
\]

At the center \(Q/r^3\to3/200\), so the baryonic density is bounded.
It can jump from a finite positive value to zero at r=1; Q and g are
continuous and there is no baryonic surface mass. No smooth C-infinity
baryon-density matching is claimed.

At r=1, \(u=1/10\), \(u'=-1/5\), \(\rho=\lambda=p=0\).
Both u and u' match the exterior exactly. Since

\[
 r^2R(S/r^2)={S^2\over r^2-S}\leq{1\over90}
 <{47\over1800}=Q,
\]

\(\lambda'<0\) throughout the exterior and \(\lambda<0\) there.
Thus the vacuum KKT inequality is satisfied. The density is continuous at
the edge, and its derivative need not be: the action supplies no delta term
from that finite jump. The exterior P field has a finite positive W and
stiffness energy integral, since W=O(r^-4) and |grad P|^2=O(r^-6).

This is a full analytic witness for the changed Newtonian action, rather
than a freely truncated profile whose exterior equation was discarded.

## 5. Energy certificate and scope of stability

After eliminating the isolated Newtonian field, write the Helmholtz
decomposition \(P=P_L+P_T\). The settled self-gravity is
\(-K\int|P_L|^2/2\), while its external gravitational energy is
\(\int\rho\Phi_{b+f}\). Hence, up to fixed source self-energy,

\[
 E=\int\left[{V(K|P|)\over K}+{K\over2}|P_T|^2
       +{\gamma\over2}|\nabla P|^2+e(\rho)
       +\rho\Phi_{b+f}\right]d^3x,
\quad \rho=\nabla\cdot P,                                    \tag{17}
\]

where
\(V(u)=-u^2/2-a_0u-a_0^2\log(1-u/a_0)\), \(V'=R\geq0\),
and \(V''\geq0\). The radial function \(V(K|P|)\) is convex as a
function of the vector P (nondecreasing convex radial profile). All nonlinear
terms in (17) are convex for convex e; the source term is linear. Thus the
energy is convex on the linear constraint and convex nonnegative-density,
fixed-stock, sub-saturation domain. Positive gamma makes the gradient part
strict except for constants, which the isolated decay removes.

More directly, at a static solution (3), the first variation after using
\(\delta\rho=\nabla\cdot\delta P\) is

\[
 DE[\delta P,\delta\rho]
 =\int[e'(\rho)-\lambda]\delta\rho\,d^3x.
\]

Here variations have fixed stock and zero net flux change at infinity.
The integration by parts otherwise includes the boundary term
\(\lambda_\infty\delta S\); the witness has finite nonzero
\(\lambda_\infty\), so that term must not be silently dropped for
stock-changing variations. Decay also excludes independent nonzero angular
boundary terms.

It equals \(\mu\delta\rho\) on the occupied region, and is at least
\(\mu\delta\rho\) in vacuum because admissible vacuum additions have
\(\delta\rho\geq0\). Fixed total stock removes the constant-mu term.
The KKT inequality therefore certifies that the witness minimizes (17)
within this admissible class. This variational certificate includes
nonspherical static variations with the same prescribed spherical source,
provided the stated finite-energy/decay domain permits the integrations.

This is not a global well-posedness, strong-hyperbolicity, relativistic
positive-energy, or nonlinear dynamical stability theorem. The auxiliary
elliptic P sector and the irrotational fluid are new effective choices.

## 6. Why simple occupation multipliers do not achieve the same result

If an occupation variable chi multiplies \(P\cdot\nabla\Phi\), Poisson
gravity sees \(\nabla\cdot(\chi P)\). The actual settled flux becomes
\(4\pi r^2\chi P_r\), changing the retained \(m=r^2u/G\) dictionary.
If only W and the stiffness are multiplied and both vanish in vacuum while
the coupling is retained, freely varying P in an open vacuum region instead
requires \(\nabla\Phi=0\), inconsistent with positive enclosed mass.

A regular universal vacuum W0 with nonzero quadratic stiffness is also
strongly constrained if P remains freely varied. For an exterior flux S,
\(P=S\widehat r/(4\pi r^2)\), \(\Delta_vP=0\), and
\(g=G(Q+S)/r^2\). Requiring the P equation at every exterior radius means

\[
 W_{0,P}={Q+S\over S}u\widehat r
\]

through an interval accumulating at u=0. Thus W0 must be exactly quadratic
on that interval and its constant susceptibility fixes Q/S. One universal
vacuum W0 cannot admit arbitrary external-to-stock ratios in this simple
class. A fixed-ratio supply could evade that last objection; a more general
density-dependent stress could also change the premise. This is a bounded
failure result, not an obstruction to every occupation-dependent action.

## 7. Dictionary changes, unresolved work, and handoff

Preserved: full rational W; Newtonian gravitational coupling and its signs;
settled mass \(m=r^2u/G\); nonnegative local rest-mass density; fixed finite
conserved stock; and positive gamma. Changed: P is a constrained auxiliary
field tied to a new irrotational material density/current; vacuum P is not an
independently freely varied response. A new EOS coefficient kappa is used.
P's constitutive energy is not counted as a second independent rest-mass
population; relativistic gravitation of that energy is outside the Newtonian
model. The baryon source in the exact witness was manufactured to certify
existence, not fitted or inferred from a dwarf.

No conversion between settled and free populations is supplied: the witness
has no free component and all cold stock is settled. Adding a free reservoir
requires varying its own current and chemical potential, feeding its gravity
into Q, and specifying any reciprocal conversion term. Merely adding a
desired free density after solving (7) is not a solution of the coupled model.
Formation, collisionless phase-space admissibility, carrier microphysics,
causal propagation, metric/lensing, abundance and empirical fitting remain
open. The known at-rest preparation issue is not removed by equilibrium.

The next discriminator is a fixed independently specified regular stellar
source, fixed stock, and whole-center unknown-edge BVP with the matching
(10), followed by the exterior KKT test. For a total supplied compact source
this uses H in (7), not h alone. The root lane is examining that problem in
`../free_boundary/`; no duplicate annulus search is proposed here.

## 8. Evidence and review record

The proof above is analytic. `check_exact.py` supplies supplementary exact
symbolic controls of the action reductions, witness, normalization, edge
matching, and a negative control that omits the multiplier. Contract and
completed run details are in `contract.json` and `run_001/manifest.json`.
Finite rational samples are labelled samples; they do not prove positivity
on a continuum. Equation (16) is the continuum positivity proof.

Review provenance: derivation and self-review by the lane author, followed
by separate-agent focused review in
`../finite_stock_stress/OCCUPIED_ACTION_REVIEW.txt`. That review confirms the
action signs, vacuum KKT, interface, exact witness and fixed-stock convexity
under the stated changed-action domain. No claim of literature novelty or
external theorem transfer is made.

Proofread self-review scope: this note only. Routine edits: none pending.
Mathematical-token changes after derivation: none pending. Unresolved prose
issues: none found. Correctness auditing is distinct from proofreading.
