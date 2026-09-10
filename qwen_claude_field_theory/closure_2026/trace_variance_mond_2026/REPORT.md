# Trace-variance MOND: a real action bridge and a radial stability obstruction

Checkpoint 2026-09-10; base `5943d5325c377836ca1a303f0676283328259871`.
**Full theory OPEN. No empirical confirmation or first-principles derivation
of kappa=1/2 is claimed.** The regular scalar version of the family below
fails a necessary principal-health condition. Its trace-degenerate endpoint
is an action reformulation of an already studied constrained Hamiltonian,
not a new escape from that Hamiltonian's unresolved causal gate.

## Target, scope, and the mathematical connection

Retain one physical metric, exact mu(y)=1-exp(-y), the fitted optional
a0-squared=Lambda/(32 pi) relation, two healthy tensor modes, and an expanding
homogeneous sector. Test whether changing only trace kinetics can remove or
make healthy the unwanted scalar. Ranks, momenta and frequencies are computed,
not supplied as certification inputs. Natural units, signature (-+++),
m=M-squared>0, and K_ij=(dot h_ij-Lie_shift h_ij)/(2N) are used throughout.

The key connection, on the spherical static branch, is

\[
g_N=\mu(g/a_0)g,\quad g_{\rm ph}=g-g_N,
\qquad
\boxed{\alpha_\parallel=\frac{d g_{\rm ph}}{dg}
=1-\mu-y\mu'.}
\]

For the specified exponential mu,
g_ph=a0 y exp(-y), with maximum a0/e at y=1. Above that point
alpha_parallel=(1-y)exp(-y)<0. The extra force's turnover is precisely the
negative radial lapse Hessian in this acceleration-only potential. The static
AQUAL eigenvalue is instead 1-alpha_parallel=mu+y mu'>0: **a healthy static
equation does not certify the dynamical scalar.**

Credit: Carl Zimmerman's research target, scale relation, and insistence on
connecting bounded force boosts to the relativistic architecture motivate
this investigation. The action-to-Hessian/kinetic analysis here is the
assistant's calculation. Carl's previously quoted RAR nu(s) is a DIFFERENT
interpolation prescription: its maximum 0.6476 a0 is not the a0/e maximum
derived here. The two kernels are not silently identified. No literature-wide
novelty claim is made for this connection or the resulting obstruction.

## 1. One explicit family, not a collection of phenomenological equations

On finite-volume preferred leaves with positive lapse, define
W=int N sqrt(h), Kbar=int N sqrt(h) K/W. Consider

\[
S_d=\int dt\,d^3x\,N\sqrt h\left[
\frac m2(R^{(3)}+K_{ij}K^{ij}-K^2-2\Lambda)
+m f(a)+\frac{md}{3}(K-\bar K)^2\right]+S_m[g,\psi],
\]
\[
a_i=D_i\log N,\quad y=|a|/a_0,
\qquad f(a)=2a_0^2[1-(1+y)e^{-y}].
\]

d is a real constant, not fitted here. The d=0 action is the minimal repaired
CAM action audited at the base commit. The average includes N; replacing
it by an unweighted average changes the theory. Boundaryless compact leaves
or the stated finite slab with Dirichlet completion and vanishing shift flux
are allowed. No infinite-volume average is invented. A clock-covariant
definition and its full functional constraint algebra remain to be audited;
this report uses the explicit preferred-foliation action as written.

Three distinct checks: d=0 retains the original scalar pair; regular d gives
a possible dynamical clock; d=1 makes local trace kinetics degenerate while
retaining the global trace. They are parameter branches of this action.

### Exact trace Legendre bridge at d=1

Split K_ij=K^TF_ij+h_ij K/3. Then, without expanding the fields,

\[
L_{K,d=1}=\frac m2\int N\sqrt h K_{TF}^{ij}K^{TF}_{ij}
-\frac{m}{3W}\left(\int N\sqrt h K\right)^2,
\qquad \pi/\sqrt h=-m\bar K.
\]

Thus the trace constraint is pi-sqrt(h) int(pi)/int(sqrt(h))=0.
For fixed trace density P=pi/sqrt(h), the trace Hamiltonian is
-W P^2/(3m), just the Einstein trace Hamiltonian restricted to this constraint.
The traceless Legendre map is the unchanged Einstein map. Hence this is the
same bulk constrained Hamiltonian as
`../g03_global_kernel_bridge_2026/METRIC_CONSTRAINT.md`, after that file's
overall momentum normalization is translated. Mean variation, boundary terms
and primary multipliers must be retained in using this equivalence.

The script checks the trace identity and all lapse derivatives on three
arbitrary positive-volume/lapse cells. It obtains the rank-one velocity
Hessian by differentiation. The continuum identity above follows directly by
expanding the variance integral; it is not inferred from a three-cell rank.
The logarithmic-volume cell momentum is 2/3 of the metric trace momentum,
accounting for the 3/4 versus 1/3 Hamiltonian coefficients in the raw output.

## 2. Static potentials and expanding FLRW

For a static zero-shift branch K=0, the added variance and its first variation
vanish. The leading weak-field density is

\[
L_{stat}=m[(\nabla\Psi)^2-2\nabla\Phi\cdot\nabla\Psi+f(|\nabla\Phi|)]
-\rho\Phi.
\]

Independent variations give Delta(Psi-Phi)=0 and
div(grad Psi-exp(-y)grad Phi)=rho/(2m). Boundary data eliminating harmonic
slip therefore yield the requested MOND equation with G_N=1/(8 pi m).
Newtonian and deep-MOND limits follow from this mu. This is leading static
slip=0, **not** a calculation of moving-frame PPN beta or alpha_i.

On homogeneous FLRW, K=Kbar exactly. The variance and its first variation
again vanish, without setting K or H to zero. With minimally coupled dust
of conserved comoving mass M, actual lapse variation gives

\[
L_0=-3m A\dot A^2/N-m\Lambda NA^3-NM,
\qquad H^2=\Lambda/3+M/(3m A^3).
\]

The k=0 Hamiltonian is separately transformed before imposing constraints:
H0=N[-p_A^2/(12mA)+m Lambda A^3+p_T]. Primary p_N and its secondary have
computed zero mutual Poisson matrix; preservation closes. Two first-class
constraints in the six-dimensional phase space leave one homogeneous pair
INCLUDING the ordinary matter clock. This is not a hidden local gravitational
DOF count and not a perturbative cosmology viability proof.

For ordinary minimally coupled matter, its separate diffeomorphism identity
gives nabla_mu T_m^{mu nu}=0 on the matter equations. For canonical scalar
matter explicitly, nabla_mu T^{mu nu}=(Box phi-V_phi) nabla^nu phi.
This matter statement neither proves covariance of the preferred-leaf
gravity completion nor removes the gravitational scalar.

## 3. Actual scalar variation, frequency pole, and Dirac generations

Freeze a static smooth background jet with y>0 and a unit Fourier direction
making angle theta with a. The complete order-two lapse coefficient is

\[
\alpha(\theta)=e^{-y}(1-y\cos^2\theta).
\]

This follows by differentiating m f with respect to the three components
of a; metric-lapse cross terms from f have at most one derivative and cannot
change this order-two principal symbol. Since background K=0, variance
weight/average perturbations do not add order-two local terms. Its averaging
part is spatially finite-rank and does not alter the local principal symbol.

Keep the spatial scalar gauge coordinate E until after Legendre transformation.
For one real k!=0 mode write
K_ij=diag(zdot+k^2(B-Edot),zdot,zdot), h_ij=exp(2z)delta_ij before E.
The code builds the kinetic terms from this matrix. With N=1+n, it obtains

\[
L_2=\frac m2(K_{ij}K^{ij}-K^2)+\frac{md}{3}K^2
+mk^2(z^2+2nz+\alpha n^2).
\]

For d!=0,1 and alpha!=0, solve the varied B,n equations, then choose E=0:

\[
L_{red}=m\frac{3(d-1)}d\dot z^2+mk^2(1-1/\alpha)z^2,
\quad
\boxed{c_s^2=\frac{d}{3(d-1)}\frac{1-\alpha}{\alpha}.}
\]

An independent determinant of the three frequency-domain Euler equations
vanishes at the derived omega^2=c_s^2 k^2. This is a physical scalar pole,
not a rank or sound speed supplied as an input.

The full linear Dirac algorithm starts with primary constraints ONLY and
continues preservation. Raw Poisson matrices, their computed ranks, all
generations and final primary multipliers are in the reproducible output.
In phase order (z,E,n,B,pz,pE,pn,pB):

| Branch | Primaries | Independent secondaries, normalized | PB rank | FC / SC | Scalar pairs |
|---|---|---|---:|---:|---:|
| d!=1, alpha!=0 | pn,pB | alpha*n+z,pE | 2 | 2 / 2 | 1 |
| d=1, alpha!=1 | pn,pB,pz | alpha*n+z,pE,n | 4 | 2 / 4 | 0 |
| d=1, alpha=1 | pn,pB,pz | n+z,pE | 2 | 3 / 2 | 0 |

Here the first row includes d=0, but the sound formula does not: at d=0
the scalar quadratic Hamiltonian has no pz-squared term. That degeneracy is
not a new primary constraint; the base CAM audit supplies its nonlinear
interaction warning. At alpha=0 the chain is recomputed separately, not
obtained from an inverse divided by alpha. The extra quadratic first-class
constraint at d=1,y=0 is not certified as a nonlinear gauge symmetry.

The transverse vector calculation independently gives zero physical pairs
per polarization from its primary shift constraint and momentum secondary.
The TT block has positive kinetic matrix (m/2)I and derived omega^2=k^2.
These local principal results do not constitute nonlinear total-DOF closure.

## 4. Scoped sign theorem, with a genuine background

Positive scalar kinetic energy requires d<0 or d>1. For EVERY such d and
EVERY y>1, radial alpha=(1-y)exp(-y)<0, so c_s^2<0. More generally the
unstable cone is y cos^2(theta)>1. For 0<d<1 the kinetic sign itself is
negative. Thus no regular trace-kinetic coefficient is healthy across all
accelerations for this unchanged acceleration potential.

Lean proves the universal sign implication for every positive normalized
kinetic coefficient and every y>1, and the angular-cone sign. The bridge from
the explicit action to those quantities is the SymPy/analytic derivation,
not formalized differential geometry. Lean uses no added physics axioms or
`sorry`; printed axioms are the standard propext, Classical.choice, Quot.sound.

This is not merely an arbitrary off-shell background assignment. Following
the repository's plane-vacuum construction, the code independently varies

\[
L=\frac{NA'^2+2AA'N'}B-\Lambda NBA^2+NBA^2f(N'/(NB))
\]

with respect to N,A,B BEFORE B=1, in dimensionless m=a0=1 units. Put
u=N'/N>0, b=A'/A, chi=(1-u)exp(-u). Its radial constraint is
C=b^2+2bu+Lambda-f+2u^2 exp(-u)=0. The two evolution equations have matrix
[[2,2chi],[1,1]] on (b',u'), and the exact identity
C'+(u+2b)C=u E_N+2b E_A proves constraint propagation in the normalized
equations. A constrained seed with the optional framework relation is

\[
u_0=20,\quad \Lambda=32\pi,\quad N_0=A_0=1,
\quad b_0=-20+\sqrt{400-32\pi+f(20)-800e^{-20}}.
\]

The discriminant is positive (indeed >270 using pi<4 and exp(20)>800),
the ODE determinant is 2(1+19exp(-20))>0, and alpha_radial=-19exp(-20)<0.
The ODE is analytic near the seed; local existence gives a smooth static
vacuum patch for this same action, for every d (K=0). Dirichlet slab boundary
data may be taken from that solution; this is NOT a boundaryless compact
static universe. A negative squared characteristic speed on this regular
patch obstructs a strongly hyperbolic, ghost-free two-derivative scalar
completion. We have not proved a global nonlinear instability theorem or
computed a cutoff for a different higher-derivative EFT.

### Generalization: the turnover, not the exponential alone

For a C1 kernel whose static extra acceleration B(y)=y[1-mu(y)] is positive
somewhere and tends to zero at high acceleration, B' is negative somewhere:
choose a later point with lower B and apply the mean-value theorem. Since
alpha_parallel=B', EVERY such kernel has this radial obstruction in the
regular trace-kinetic family. A kernel with nonzero limiting extra acceleration
is outside this argument. This is a restricted architectural no-go, not a
universal exclusion of MOND, modified inertia, extra fields or time nonlocality.

## 5. Why an older PASS does not answer this calculation

`../theory_discovery/khronometric_mond_gauntlet_2026.py` derives a correct
constant-coupling scalar formula, then substitutes eta=2exp(-y) into it.
That omits the longitudinal derivative of the running coupling. The correct
replacement along a is eta_parallel=2(1-y)exp(-y), not 2exp(-y).
At lambda=2 (our d=-3/2), y=2, the older substitution gives
(exp(2)-1)/5>0; actual radial variation gives -(exp(2)+1)/5<0.
The old program can still exit zero because it tests the wrong specialization.
Its all-y health claim therefore cannot be used as evidence for this family.
Old files and historical evidence are preserved, not silently rewritten.

## 6. Next unavoidable change and verification

Changing d or the averaging prescription alone cannot repair the regular
scalar sign. The d=1 constrained endpoint returns to the previously studied
causal-response problem. A genuinely new candidate must change the coupled
principal operator (for example an independent dynamical field or temporal
response), then rederive the SAME physical static MOND equation and metric
response. Positing healthy extra fields without their action and full response
does not clear this gate. PPN, nonlinear clock restoration, full y=0 control,
cluster/cosmological data, and kappa derivation remain unproved.

Run `python3 -B run_suite.py` from this directory. Its output contains exact
commands, working directories and individual exit statuses, including the
expected refusal of `--require-closure` (exit 2), the unchanged old gauntlet,
Lean, and the base CAM regression suite. `run_001/manifest.json` pins all
declared inputs; `run_001/stdout.txt` preserves the calculations and statuses.
Initial new regressions failed before their corresponding action/background
implementation; the completed six-test run passes. Passing this AUDIT is
evidence for the obstruction, not a completed gravitational theory.

Self-review: equation/notation proofreading covers this report and the Lean
file; no unrelated manuscript edited. Mathematical review is by the same
agent, with independent frequency-determinant and action-variation checks,
not an external referee or a claim of empirical discovery.
