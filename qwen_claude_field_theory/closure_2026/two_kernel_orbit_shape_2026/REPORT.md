# Two MOND kernels: orbital discriminator and action audit

Date: 2026-09-04. Relativistic completion: **OPEN**. The naive two-scalar
Lorentzian promotion tested below is **DEAD**, on its own stated assumptions.

This work follows the live tree at `17ebae63b`, including the concurrent
`f50741f0a` update. It preserves the user's explicit target
`mu_exp(y)=1-exp(-y), y=g/a0`. The older field-theory document instead uses
`mu(t)=1-exp(-t), y=t^2/mu(t)`, which is the empirical RAR kernel. These are
distinct targets; neither their empirical status nor their relativistic
certificates may be silently interchanged.

## Research contract and method

Derive a parameter-free orbital test of the two spherical force laws, check it
against independent force differentiation and integrated orbits, and establish
the correct action primitive before attempting a relativistic promotion.
Audit the statistical claim in f21 using a separately specified descriptive
score with complete galaxies resampled together and a0 fitted for both laws.
This is a bounded calculation plus the analytic arguments below. It is not a
search over all actions or a calibrated statistical rejection of MOND.

Arithmetic: SymPy exact expressions over real positive parameters; mpmath
45–100 decimal digits for inversions and quadratures; float64 force inversion,
orbit integration, and catalog comparison. Tests specify the numerical ranges
and tolerances. The final manifest records commands, hashes and exit statuses.
The tests were run before implementation and failed; subsequent tests caught
a symbolic substitution mismatch, an exponential/hyperbolic simplification
issue, and identical initial guesses in an independent root solver. These
implementation failures were corrected without relaxing the mathematical
assertions.

## 1. A new repository-level orbital test

Assume an isolated, static, spherical source; a test particle outside all its
baryonic mass; ordinary nonrelativistic particle inertia; negligible external
field; and the infinitesimal radial oscillation limit. Define

\[
q=\frac{\kappa^2}{\Omega^2},\qquad
D=\frac{dq}{d\ln r},\qquad 1<q<2.
\]

Here Omega is the circular angular frequency and kappa is the radial epicyclic
angular frequency. Varying the particle action, and differentiating its radial
effective potential at fixed angular momentum, gives

\[
\Omega^2=\frac{g}{r},\qquad \kappa^2=g'+\frac{3g}{r},\qquad
q=3+\frac{d\ln g}{d\ln r}.
\]

For `mu_exp`, let y=g/a0 and L=y/(exp(y)-1). Differentiating the spherical
flux law r² g mu(y)=GM gives

\[
\frac{dy}{d\ln r}=-\frac{2y}{1+L},\qquad
q=\frac{1+3L}{1+L},\qquad
D=\frac{4L(y+L-1)}{(1+L)^3}.
\]

For `nu_rar`, write s=g_N/a0 and t=sqrt(s). Then
g/a0=t²/(1-exp(-t)), dt/d ln r=-t, and, with L=t/(exp(t)-1),

\[
q=1+L,\qquad D=L(t+L-1).
\]

The same real inverse function eliminates either acceleration coordinate:

\[
X(L)=-L-W_{-1}(-Le^{-L}),\quad 0<L<1.
\]

The principal Lambert branch gives the extraneous zero solution. The actual
parameter-free field-shape equations are therefore

\[
\boxed{D_{\exp}(q)=
\frac{4L_\exp[X(L_\exp)+L_\exp-1]}{(1+L_\exp)^3},
\quad L_\exp=\frac{q-1}{3-q}}
\]

\[
\boxed{D_{\rm RAR}(q)=
L_{\rm RAR}[X(L_{\rm RAR})+L_{\rm RAR}-1],
\quad L_{\rm RAR}=q-1.}
\]

At q=3/2, D_exp=0.6958952031227157 and D_RAR=0.3782156043130848.
Changing mass or a0 cannot change these numbers at fixed q. A common distance
or time-unit calibration also cancels. This compares different radii/models
at the same q; it does not assume that the two laws have the same q at a fixed
mass and physical radius.

### Exact inequivalence, independent of normalization

Set epsilon=2-q. Series expansion and elimination of the acceleration give

\[
D_\exp=\epsilon+\frac43\epsilon^2+O(\epsilon^3),\qquad
D_{\rm RAR}=\epsilon-\frac13\epsilon^2+O(\epsilon^3).
\]

Consequently the dimensionless invariant

\[
\boxed{\lim_{q\to2^-}
\frac{dq/d\ln r-(2-q)}{(2-q)^2}
=\begin{cases}4/3&\mu_\exp,\\-1/3&\nu_{\rm RAR}\end{cases}}
\]

proves that no constant change of M, a0, radial scale or clock calibration can
make the complete exterior orbit profiles identical. Both shape functions
are analytic on 1<q<2; equality on any open q interval would force equality
throughout that connected interval and of the deep-limit expansion, a
contradiction. This does not prohibit their intersecting at isolated data
points or being indistinguishable within observational errors.

There is also an exact one-sided prediction for the RAR curve:

\[
(2-q)-D_{\rm RAR}
=1-\left[\frac{t}{2\sinh(t/2)}\right]^2>0\quad(t>0),
\]

because sinh(z)>z for z>0. The exponential law violates this inequality in an
open neighborhood of the deep regime (its epsilon² coefficient is positive),
and at q=3/2. The 99-point numerical separation scan is only a bounded check;
we do not use it to claim a uniform ordering of the two curves everywhere.

These are predictions conditional on the two laws, derived from established
central-force mechanics. They do not establish a new law of nature. A measured
rotation curve can supply q=2+d ln(v_c²)/d ln r; then D involves another
derivative and is not an independent data set. Measuring orbital frequencies
independently would be a different test. Baryonic mass gradients, a disk,
external fields and finite eccentricities require additional modeling.
The pre-existing finite-eccentricity inverse for mu_exp does not automatically
apply to nu_RAR.

## 2. Correct nonrelativistic actions for the RAR curve

For AQUAL use F(y), with y=|grad Phi|/a0, in

\[
S_{\rm AQUAL}=-\int dt\,d^3x
\left[\frac{a_0^2 F(y)}{8\pi G_N}+\rho\Phi\right]+S_{\rm kin}.
\]

The varied equation is div[F_y/(2y) grad Phi]=4 pi G_N rho. For mu_exp the
specified primitive is y²+2(1+y)exp(-y)-2. For RAR an exact parametric primitive is

\[
y(t)=\frac{t^2}{1-e^{-t}},\qquad
F(y(t))=\int_0^t2u^2 y'(u)du.
\]

The two constitutive eigenvalues are mu=1-exp(-t) and
d(y mu)/dy=2t/y'(t)>0. Indeed y'(t)>0 follows from
2(exp(t)-1)-t>0. They vanish as y tends to zero. Convexity of this static
constitutive operator proves neither dynamical ghost freedom nor controlled
relativistic strong coupling at zero field. F(y)~(2/3)y³ is finite there.

The corresponding QUMOND action is the established two-potential action

\[
S_Q=-\int dt\,d^3x\left\{
\frac{2\nabla\Phi\cdot\nabla\chi-a_0^2 Q(Z)}{8\pi G_N}
+\rho\Phi\right\}+S_{\rm kin},\quad
Z=\frac{|\nabla\chi|^2}{a_0^2}.
\]

Independent variations give

\[
\boxed{\Delta\chi=4\pi G_N\rho,\qquad
\Delta\Phi=\nabla\cdot[Q_Z(Z)\nabla\chi].}
\]

To obtain the empirical RAR requires Q_Z(Z)=nu_RAR(sqrt(Z)). With
t=Z^(1/4), the correct primitive is

\[
\boxed{Q(Z)=Z+4 I_3(Z^{1/4}),\qquad
I_3(t)=\int_0^t\frac{u^3}{e^u-1}du.}
\]

Equivalently Q(t⁴)=integral_0^t 4u³/(1-exp(-u))du. Thus
Q~(4/3)Z^(3/4) deep, Q~Z Newtonian, and
F(y(t))+Q(t⁴)=2t²y(t). This last Legendre identity checks the two independent
quadratures. It agrees with the AQUAL primitive in concurrent f23; the
primitive itself is not claimed as new.

### An actionable error in the concurrent f23 update

At commit f50741f0a, f23 instead called

\[
J(s)=s+2\sqrt{s}\ln(1-e^{-\sqrt{s}})
-2\operatorname{Li}_2(e^{-\sqrt{s}})+\pi^2/3
\]

the QUMOND action primitive because J'(s)=nu_RAR(s). That identity is correct;
its interpretation as the standard action primitive is incorrect. The action
requires a derivative in **Z=s²**. Inserting Q(Z)=J(sqrt(Z)) yields
g/a0=nu_RAR(s)/2 in spherical symmetry and g/g_N->0 at high acceleration.
Inserting Q(Z)=J(Z) instead yields g/a0=s/(1-exp(-s)), which tends to 1, not 0,
at zero source acceleration. The script computes both failed limits.
The f23 QUMOND primitive and its derivative/limit check are corrected in this
change. Its QUMOND quadrupole calculation consumes nu directly and is not
changed by this primitive correction.

This action is Newtonian QUMOND, not a relativistic completion. AQUAL and
QUMOND share the algebraic relation in spherical symmetry; their general
non-spherical equations and external-field quadrupoles are different.

## 3. Constraints and the next obstruction

For one real nonzero Fourier mode of the frozen static potential sector,
let f=delta Phi, c=delta chi, A=1/(8 pi G_N), and b be the directional
constitutive derivative. The Hamiltonian is

\[
H=A k^2(2fc-bc^2)+\rho_k f.
\]

Both momenta vanish as derivatives of the velocity-free Lagrangian. Their
preservation produces C_f=-2Ak²c-rho_k and C_c=-2Ak²f+2Abk²c. The script
constructs every Poisson bracket from canonical differentiation, calculates
the constraint Jacobian and matrix ranks, and preserves these secondaries
with H_T=H+u_f p_f+u_c p_c. It finds u_f=u_c=0 for a static source, no tertiary
constraint, four independent second-class constraints, no first-class ones,
and zero propagating potential configurations in this finite-k NR block.
The matrix determinant is computed as 16 A⁴ k⁸.

At k=0 the matrix rank is zero, but the secondary source condition is
rho_0=0. On a periodic spatial volume a positive mean density is incompatible
with the unmodified Poisson equation. If rho_0=0, the two remaining momenta
are first class in this external-source potential-only system. This is not an
FLRW result or a matter-inclusive constraint count. It identifies a necessary
boundary/background treatment for any cosmological use.

Promoting the two potentials to **independent Lorentzian scalar fields** on
a fixed metric gives the temporal quadratic action on a static-gradient
background

\[
L_t=A(2\dot f\dot c-b\dot c^2),\qquad
W=\begin{pmatrix}0&2A\\2A&-2Ab\end{pmatrix},\qquad
\det W=-4A^2<0.
\]

The determinant follows by differentiating that Lagrangian twice. The block
is nondegenerate and has one positive and one negative kinetic eigenvalue.
Hence this simple independent-scalar relativistic promotion has a ghost.
It cannot inherit the zero-mode count of the elliptic action. This is a
scoped failure, not a no-go for every metric/connection or constrained action.
No lapse, shift or metric constraints have been silently assumed here.

Full Phi/Psi, PPN, matter Ward identity, tensor speed, homogeneous dynamics and
the zero-field dynamical limit remain unproved for a single relativistic
completion. A0's relation to Lambda remains an input. G_N is the high-field
Poisson coefficient of these NR actions; a measured relativistic Newton
constant has not been established.

## 4. Statistical correction to the latest repo claims

The original f21 output reproduces its 18-bin diagonal statistics:
38.8 for nu_RAR, 201.6 for mu_exp, difference 162.8. Its largest transition
bin standardized residual is 7.5. These are fixed-a0, fixed-M/L diagnostics.
Separate bin bootstraps omit cross-bin covariance; the prediction is evaluated
at bin centers combined with median gbar; per-point velocity errors are
computed but unused; distance and inclination nuisance parameters are fixed.
Those numbers alone do not establish a 7.5-sigma model rejection.

The new comparison uses all 3140 positive points in 147 galaxies from the
same loader, individual log residuals, and equal galaxy weights. Each model
profiles a0 on a 501-point grid from 10^-10.6 to 10^-9.4 m/s². Each of 999
paired multinomial draws resamples whole galaxies and refits both kernels.
This is a descriptive MSE analysis, without observational-error weighting or
nuisance marginalization; its percentile interval is not a likelihood test.

| Kernel | Best grid a0 (m/s²) | Equal-galaxy RMS (dex) |
|---|---:|---:|
| mu_exp | 1.06856e-10 | 0.204079 |
| nu_RAR | 8.70964e-11 | 0.201492 |

The paired 2.5/50/97.5 percentiles of MSE_exp-MSE_RAR are
[-0.00009044, 0.00098750, 0.00212046] dex²: the interval contains zero.
No bootstrap optimum hits the acceleration-grid boundary. Doubling the grid
resolution changes the full-sample minimum MSE by at most 7.55e-8 dex².
Using equal point weights produces different fitted a0 and scatter; the
script reports both. At the alternative fixed a0 even the ordering of the
equal-galaxy MSE reverses. Thus the earlier diagnosis is not invariant to the
score and normalization treatment. This does not establish that mu_exp is an
adequate physical fit, nor that nu_RAR is disfavored.

The raw catalog has 779 points in 63 galaxies above 0.66a0 at the canonical
footing, and 585 points in 52 galaxies at the alternative footing. These are
inferred values with errors, not true-force counterexamples. They do directly
contradict f21's former claim that its bin-median test established a ceiling
for every catalog galaxy. A Newtonian limit alone also does not imply a
vanishing phantom acceleration: the familiar simple kernel has a constant
asymptotic phantom acceleration. F21's misleading captions were corrected;
some were incorporated by the concurrent f50741f0a commit.

## 5. Literature and novelty boundary

Mathbox computation-audit guided the explicit domains, independent checks,
and reproducibility manifest; literature-check and SciSpace were used for
overlap checks. Proofreading covers this report and the changed mathematical
captions, not unrelated repository claims.

Primary sources checked on 2026-09-04:

- McGaugh, Lelli & Schombert, arXiv:1609.05917v1, PRL 117 (2016) 201101,
  [equation 4, PDF page 4](https://arxiv.org/pdf/1609.05917v1). Their g_dagger
  is our a0; their gobs and gbar are g and g_N. This is the RAR fitting law,
  not mu_exp. The paper distinguishes a fitting relation from a field theory.
- Milgrom, arXiv:0911.5464v2 (2 March 2010), MNRAS 403 (2010) 886,
  [QUMOND, equations 3–6](https://arxiv.org/pdf/0911.5464v2). Its Q argument
  is the squared Newtonian field and nu(s)=Q'(s²). This supports the action
  convention used above and the primitive correction, not a relativistic
  conservation or tensor-mode claim.
- Abramowicz & Kluzniak, arXiv:gr-qc/0206063v1,
  [epicyclic orbital oscillations](https://arxiv.org/pdf/gr-qc/0206063v1).
  Adjacent established orbital machinery; the general central-force relation
  used here is independently derived from the particle action in our script.

PDF text was read through the research tool, not retained locally. The prior
Kepler bundle's LITERATURE_SCOPE.md was read. SciSpace was asked whether a
parameter-free relation between q and its radial derivative had been used to
distinguish MOND kernels. Web queries included "MOND epicyclic frequency
apsidal precession interpolation function radial acceleration relation" and
"McGaugh Lelli Schombert 2016 radial acceleration relation 1 exp sqrt".
SciSpace returned adjacent works, including Milgrom's global deep-MOND
discriminant; abstracts and inconsistent metadata were treated as discovery
aids. This bounded English-language search does not establish worldwide
novelty. Classification: formal corollaries of the specified MOND laws and
known orbital dynamics, newly made explicit/testable in this repository.
The action primitives and QUMOND framework are prior art.

## 6. Decision and next unavoidable calculation

The result is **OPEN** for the requested full theory. We have a falsifiable
orbital shape equation, a repaired action primitive, and a failed minimal
Lorentzian promotion. We have not achieved a relativistic MOND action with
all the user's gates.

For a relativistic construction the next unavoidable step is to identify
precisely how Phi and chi descend from metric/connection or constrained
variables, then vary that same covariant action and compute its full
metric–auxiliary constraint chain. Independent scalar promotion already
fails the kinetic gate; static convexity cannot answer it. Cosmological
zero modes require a background equation, not a discarded Poisson zero mode.

For selecting the empirical target, the next unavoidable data calculation is
a matched AQUAL or QUMOND disk/external-field forward solve, with a0,
distance, inclination and stellar M/L treated consistently. The shape test
should first be extended to or bounded against realistic mass gradients and
external fields. Additional algebraic repackagings of BTFR cannot resolve
these architectural or observational questions.
