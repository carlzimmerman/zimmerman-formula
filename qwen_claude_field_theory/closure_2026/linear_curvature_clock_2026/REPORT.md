# Linear curvature-clock construction and physical-radiation test

2026-09-10. Base `36f8d4a91ff27010c28a928bd129c01fc837f9d4`.
Previous turn: verified progress, not completion. Original full-gravity goal
remains OPEN. This package constructs a different auxiliary constraint which
**repairs the frozen vacuum domain-of-dependence problem**, then tests actual
positive-energy minimally coupled radiation. It does not claim a new law of
nature, a complete theory, or literature-wide novelty.

Credit: Carl Zimmerman's fixed exponential law, fitted acceleration-scale
relation, and requirement to pursue a complete physical-metric theory motivate
the construction. The curvature multiplier and beam calculation are research
deductions, not coefficients derived by Carl or from observations.

## One action, one change

Use c=1, m>0, (-+++), F=exp(2chi), a_i=D_i log N and the same weighted average
Kbar_F as in `../elliptic_curvature_clock_2026/REPORT.md`. Consider

\[
S=m\int N\sqrt h\,dt\,d^3x\left[
\frac F2(R^{(3)}+K_{ij}K^{ij}-K^2)-\Lambda+f(a)
+4D_i\chi a^i+2\chi a^2+\frac{2F}{3}(K-\bar K_F)^2+\nu(t)\chi
\right]+S_m[g,\psi],
\]
\[
f(a)=2a_0^2[1-(1+y)e^{-y}],\quad y=|a|/a_0,\qquad
\bar K_F=\frac{\int N\sqrt h F K}{\int N\sqrt h F}.
\]

Only the auxiliary self-gradient term 2(Dchi)² has been removed from the
previous action. This is a structural change: at principal order chi becomes
a multiplier imposing lapse/spatial-metric matching instead of solving an
elliptic self-equation. It is not an assertion that chi is nonpropagating
nonlinearly. nu is global and imposes only the weighted spatial mean of chi.

Its chi Euler equation is

\[
F[R^{(3)}+K_{ij}K^{ij}-K^2+\tfrac43(K-\bar K_F)^2]
-4D_i a^i-2a^2+\nu=0.
\]

Integration by parts with N sqrt(h) is essential. The script independently
varies the flat one-dimensional spatial terms, obtaining −4u''−2u'² for
u=log N. The complete nonlinear metric and clock equations remain to be derived.

## Static branch and constraints

Independent static variation of

\[
 L_{stat}=m[(\nabla\Psi)^2-2\nabla\Phi\cdot\nabla\Psi+f
 +4\nabla\chi\cdot(\nabla\Phi-\nabla\Psi)]-\rho\Phi
\]

gives chi=0 and Psi=Phi with decaying boundary conditions (up to zero modes),
and div[(1−exp(−|grad Phi|/a0))grad Phi]=rho/(2m).
Thus G_measured=1/(8pi m); the static slip ratio is one. This is not a full
PPN calculation of beta or preferred-frame parameters.
The code verifies the directional fluxes; the field-level step uses uniqueness
of decaying harmonic differences. It is not a proof for arbitrary boundaries.

For each nonzero Fourier mode q=|k|², retain the spatial gauge variable E:

\[
K_{ij}=\operatorname{diag}(\dot z+q(B-\dot E),\dot z,\dot z),\quad
L=\tfrac m2(K_{ij}K^{ij}-K^2)+\tfrac{2m}3K^2
+mq[z^2+2nz+\alpha n^2+4\chi(z+n)].
\]

Physical Phi=n, Psi=−z. Here alpha=exp(−y)(1−y cos²theta), not a constant
coupling substituted into an isotropic dispersion formula. The Legendre
transform and full finite-mode preservation algorithm give primaries
pn,pB,pchi and equivalent secondaries alpha n+z+2chi, pE, n+z.
All brackets, generated constraints and multiplier solutions are printed.
The computed Poisson rank is four, with two first-class and four second-class
constraints on ten phase coordinates: one scalar pair, explicitly counted as
the clock/gravitational scalar. chi does not add another pair in this test.
alpha=1 and alpha=0 are recomputed separately; both close with the same counts.
The lapse/chi Hessian determinant is computed as −16m²q², not supplied.

The removed term vanishes with its first variation on homogeneous backgrounds.
Therefore the unchanged exact FLRW action is re-varied using the existing
homogeneous function: H²=Lambda/3+pT/(3m A³), with ordinary dust and expanding
solutions. Its six constraints have computed bracket rank four. This is the
k=0 isotropic calculation, not a substitution into a q≠0 inverse.
The same F multiplies tensor space and time terms; the computed tensor kinetic
matrix is mF/2 times the identity and the tensor roots are omega²=k².

## A genuine vacuum repair at the tested order

Elimination of the action-derived constraints gives

\[
 n=-z,\qquad\chi=-\frac{\mu_\theta z}{2},\qquad
 B=-\frac{3\dot z}{2q},\qquad
 L_{red}=\frac{3m}{2}\dot z^2-mq\mu_\theta z^2.
\]

Set q=−Delta, D=−mu_t Delta_perp−mu_l partial_z², where
mu_t=1−exp(−y), mu_l=1+(y−1)exp(−y), and mu_theta=D/q in Fourier space.
The equations imply the LOCAL first-order evolution identities

\[
 \dot z=-\tfrac23qB,\qquad \dot B=-2\chi,\qquad\dot\chi=\tfrac13DB.
\]

With the constraint q chi=−Dz/2, each of z,n,B,chi obeys

\[
 \boxed{\ddot U+\tfrac23DU=0.}
\]

For compact constrained vacuum initial fields, their initial time derivatives
are local too; hence this constant-coefficient system has finite propagation
within its wave cone. This is stronger than checking phase speed alone.
Lean proves 0<2mu_theta/3<1 for y>0 and 0≤cos²theta≤1, using the exponential
tangent inequality. At y=0 the kinetic term remains positive but spatial
propagation degenerates; nonlinear well-posedness is not certified.
In particular compact profiles z0=qf, zdot0=qv give
R00(0)=q(q+D)f and R00''''(0)=4D²q(q+D)f/9, a spatial polynomial rather
than the previous inverse-elliptic expression.

## Next gate: actual positive-energy radiation

The same physical metric couples to massless particles via the einbein action

\[
 S_{rad}=\frac12\sum_A w_A\int d\lambda\,
 e_A^{-1}g_{\mu\nu}(x_A)\dot x_A^\mu\dot x_A^\nu,\qquad w_A,e_A>0.
\]

Variation of e imposes null motion; coordinate variation gives the null
geodesic equation; metric variation gives positive-weight p^mu p^nu stress.
The script varies the flat particle Lagrangian, obtains its constraint,
coordinate equations and metric variation, and checks all four null directions.
Ordinary covariant conservation follows on matter shell from diffeomorphism
invariance: delta S_rad under delta g=Lie_xi g and delta x=−xi(x), integrated
by parts, gives ∇_mu T^{mu nu}=0. The executable beam checks are the exact
flat/free-streaming limit of this identity, not its full curved formalization.

Take smooth compact f≥0. Configuration A consists of equal counterstreaming
beams along ±x; configuration B uses ±z. Each has initial rho=f, current=0,
stress trace S=f. They differ only in stress direction inside supp(f).
Each beam transports f at speed one. The script checks both conservation
equations exactly. At t=0,

\[
 \Delta\rho=\Delta\dot\rho=\Delta S=0,\qquad
 \Delta\ddot\rho=\Delta\ddot S=(\partial_x^2-\partial_z^2)f.
\]

The scalar constraints and initial gravitational canonical data can be the
same for the two sources. Global density/trace zero modes of the difference
vanish; the following calculation concerns nonzero modes on the frozen R³
patch, not global anisotropic cosmology.

Varying the conserved-source coupling −n rho+z S+B rhodot+E rhoddot and
including the shift in physical R00 yields, with W=partial_t²+2D/3,

\[
 W R_{00}=\frac{q(\rho+S)}{3m}
 +\frac{(D/q)\ddot\rho-\ddot S}{2m}.
\]

This equation is derived from the action solution, not assigned. For the
initially matched beam configurations the off-source symbol in Delta R00'' is

\[
 \frac{\delta}{2m}\frac{k_z^2(k_z^2-k_x^2)}{|k|^2}\widehat f,
 \qquad\delta=\mu_l-\mu_t=y e^{-y}>0.
\]

Using the Green function of −Delta, the exterior point-kernel on the y-axis is

\[
 \boxed{K(0,R,0)=\frac{3\delta}{4\pi m R^5}>0.}
\]

The fourth spatial derivative of 1/(4pi r) is computed, not fitted. A sufficiently
small nonnegative smooth bump around the origin preserves this off-source sign
by continuity. Thus two admissible positive-energy free-streaming radiation
sources, initially indistinguishable outside their compact support, produce
different second time derivatives of physical Ricci curvature there in the
frozen model. The isotropic control delta=0 removes this tail.

This closes the earlier **external-source admissibility gap at this order**:
no negative-energy stress or arbitrary nonconserved forcing is needed. It is
still not a full nonlinear curved-background causal theorem. Radiation travels
on the same physical metric; geodesic corrections and the nonlinear background
must be included in any such lift. In the leading perturbative test their
self-gravity corrections to the matter source are higher order.

## Status and handoff

Constructive result: same static MOND/no-slip law, computed principal auxiliary
count, positive tensor/clock kinetic terms, unchanged expanding FLRW, and a
local vacuum wave cone. Obstruction: physical-radiation causal response at
frozen weak-field order. Full theory remains OPEN and this member cannot be
certified. No empirical prediction is advertised as a new law.

The next repair must change the ANISOTROPIC STRESS response D/q in the R00
equation while keeping the static density law. Retuning a free-wave speed is
insufficient. A materially different route is a matched spatial-tensor
curvature/kinetic completion; its first test must retain the tensor and vector
constraints and rerun this same positive-radiation comparison. Such additional
terms may change cT or add modes; none is presumed viable or derived yet.

Full nonlinear functional Dirac closure, a regular finite-gradient background,
all-sector matter-coupled characteristics, PPN, zero-field well-posedness and
empirical confirmation remain missing. The coefficient kappa=1/2 stays fitted.
Lean checks the stated scalar-cone and sign inequalities, not nature's laws.
All new scripts are run by `run_suite.py`; raw commands, status codes and input
hashes are retained in the run manifest. Review is self-review of the displayed
action and source conventions, not independent external refereeing.
