# Gate 1: the action-to-force dictionary is not closed

2026-09-08. Reviewed baseline `e1e6868c6b4fced8bea716d7428070e3ebf379c3`.
Original files and published claims are preserved. This is a new audit and
an explicitly different static constrained construction, not a silent repair.

**Verdict:** the same-kernel identification used to connect the displayed
action, PPN pipeline and carrier phenomenology fails in the stated static
limit. A constrained plateau can be defined variationally, but changes the
requested exponential law. The full theory remains **OPEN**.

## 1. Exact scope and source discrepancy

Use c=1, physical lapse Phi and spatial curvature Psi. g03t/f33b name these
`Psi` and `Phi`, respectively. Take a regular static clock tau=t, xi=0 and
the condensate vacuum limit Qbar=Q0->0. Merely setting Qbar=0 at fixed
nonzero Q0 is not this limit. Discard boundary variations by fixed potential
data, and remove harmonic slip by regularity and matching boundary data.
The static clock perturbation's decoupled biharmonic equation admits this
branch; no statement about its time-dependent health follows.

We adopt the executable pipeline's COMMON gravitational prefactor 1/(16 pi G).
The Markdown action puts this factor on EH alone; taken literally its clock
coefficients must instead be rescaled by 16 pi G before comparing formulas.
That normalization ambiguity itself needs an explicit amendment.

Let A=2-K_B, alpha=c14, Y=|grad chi|^2, Jtot(Y)=bY+F(Y). Source inspection:

| Source | b | Meaning of its named J derivative |
|---|---:|---|
| THE_ACTION, line 8; g03t, line 96 | 0 | total coefficient Jtot_Y |
| f33b, lines 120–121 and 175 | 1 | additional F_Y, on top of bare Y |
| g03j, lines 3–9 | assumed carrier equation | baryon-source coefficient, not derived from metric variation |

Paths: `../THE_ACTION_2026-09-05.md`, `../g03t_flrw_linear_from_action.py`,
`../../../hunt_2026/f33b_ppn_k4_clock_host_healthy.py`,
`../g03j_scalar_carrier_kernel.py`. The run hashes pin the literal sources.

## 2. Vary both metric potentials

At leading weak-field order, retaining the nonlinear constitutive function,

\[
16\pi G L=2|\nabla\Psi|^2-4\nabla\Phi\cdot\nabla\Psi
+\alpha|\nabla\Phi|^2+2A\nabla\Phi\cdot\nabla\chi
-AJ_{\rm tot}(Y)-16\pi G\rho\Phi.
\]

The script calculates the spatial Christoffel symbols and Ricci scalar for
a conformally flat three-metric, expands N sqrt(h) R, and verifies the
discarded total derivative. SymPy then varies this density independently:

\[
\Delta(\Phi-\Psi)=0,\quad
2\Delta\Psi-\alpha\Delta\Phi-A\Delta\chi=8\pi G\rho,\quad
\nabla\cdot(J_{{\rm tot},Y}\nabla\chi)=\Delta\Phi.
\]

Thus Psi=Phi on this branch. This is not a moving-source PPN calculation.
In spherical symmetry, with signed radial gradients and no extra central
scalar charge, define

\[
B={A\over2-\alpha},\quad G_{\rm scr}={2G\over2-\alpha},\quad
g_N={G_{\rm scr}M(r)\over r^2}.
\]

Here Gscr is DERIVED in the scalar-decoupled/screened limit, not assumed to
be the measured coupling in every regime. The equations integrate to

\[
g-Bg_\chi=g_N,\qquad J_{{\rm tot},Y}g_\chi=g,
\qquad (J_{{\rm tot},Y}-B)g_\chi=g_N.
\]

**The scalar is sourced by the physical lapse, not directly by the baryonic
Newtonian potential with the same kernel.** If one defines physical extra
force gphi=B gchi, its coefficient is Jtot_Y/B-1, evaluated at
Y=gphi^2/B^2. The rescaling affects the argument too.

At K_B=1/5 and alpha=1/100000, B=180000/199999. For b=1 and F_Y->0,

\[
{g\over g_N}\longrightarrow{199999\over19999}=10.0004500225\ldots,
\]

a finite inverse-square enhancement, not the deep-MOND square-root law.
For b=0 and Jtot_Y->0+, the local signed response tends to zero through a
repulsive branch; no regular attractive deep-MOND branch is obtained.
For b=1 the old same-F dictionary requires B=1, i.e. c14=K_B, which the
stated PPN corner does not satisfy. Finite xi/condensate terms require their
own calculation; these results do not establish that all such regimes fail.

## 3. Reconstruct the actual exponential carrier

For B>0 and y=g/a0, the required branch is

\[
{g_N\over a_0}=y(1-e^{-y}),\quad
{g_\chi\over a_0}={ye^{-y}\over B},\quad
J_{{\rm tot},Y}=Be^y.
\]

Integrating along this branch gives

\[
Y(y)={a_0^2y^2e^{-2y}\over B^2},\qquad
J_{\rm tot}(y)={2a_0^2\over B}
[(y^2+y+1)e^{-y}-1].
\]

In particular Jtot_Y(0)=B, not zero. For Jtot=bY+F this means F_Y(0)=B-b.
Changing this coefficient is an action change; old PPN/stability labels do
not transfer automatically.

**Scoped obstruction, analytic rather than a finite scan:** Y increases on
(0,1), decreases on (1,infinity), and tends to zero at both ends. Each
0<Y<a0^2/(eB)^2 therefore has two distinct positive y values, demanding
different values Be^y of one derivative Jtot_Y(Y). No differentiable,
single-valued Jtot on that whole interval realizes both branches. Moreover,
the effective carrier stiffness after eliminating the static metric is

\[
{d(g_N/a_0)\over d(g_\chi/a_0)}
=B{e^y+y-1\over1-y}<0\qquad(y>1).
\]

Its numerator is positive for y>0. This excludes a globally convex carrier
of this form, not every relativistic MOND construction. A static negative
stiffness alone is not a full dynamical ghost diagnosis. g03j already found
the turning-point problem under its assumed dictionary; this audit corrects
the action-dependent coefficients and does not claim the turning point is new.

## 4. A valid constrained plateau, explicitly NOT the target theory

For dimensionless vectors v=grad Phi/a0, p=grad chi/a0 and flux j, set s=|j|,

\[
W(s)=\begin{cases}[1-(1+s)e^{-s}]/B,&0\le s\le1,\\
(1-2/e)/B+(s-1)/(eB),&s\ge1.\end{cases}
\]

Replace the static scalar density by 2A a0^2[(v-j).p+W(|j|)]. Varying j
gives p=grad_j W; varying chi gives div(a0 j)=Delta Phi. In spherical symmetry
the regular flux is s=y. The convex conjugate is parametrically

\[
F(p)=[(y^2+y+1)e^{-y}-1]/B,\quad p=ye^{-y}/B,\quad0\le y\le1,
\]

and F=+infinity for |p|>C=1/(eB). At p=C n its subdifferential contains
every s n with s>=1. Thus a boundary multiplier, not a derivative at one
fixed Y, supplies the growing flux. Fenchel equality and matching conditions
are checked symbolically. Jtot=2a0^2 F with dimensionless argument p.

The actual resulting law is

\[
\mu_{\rm sat}(y)=\begin{cases}1-e^{-y},&y\le1,\\
1-1/(ey),&y\ge1.\end{cases}
\]

For y=2 this is 0.8160603, versus the requested 0.8646647. Saturation is one
chosen continuation, not forced by boundedness alone, and is not an exact
exponential solution at high acceleration.

### Static constraints: what was actually counted

For the FORMAL time extension of the fixed-source static saddle density
j.grad chi-W(j)+q chi, all four momenta vanish (primary). Preservation yields
div j=q and grad chi=grad_j W (secondary). On a uniform flux background the
Hessian is H=W'' nn^T+(W'/s)(I-nn^T); plateau H has a radial null vector.
Preservation gives div u_j=0 and grad u_chi-H u_j=0 for the stationary-source
linear perturbations used here. The script differentiates the real-mode
Hamiltonian, removes dependent constraints, calculates EVERY bracket, and
preserves the secondaries. No remaining multiplier-independent tertiary
term occurs in this autonomous quadratic static problem.

| Tested sector | Primary | Independent secondary | Actual bracket rank | Linear static first class |
|---|---:|---:|---:|---:|
| regular nonzero k, parallel | 8 | 8 | 16 | 0 |
| plateau nonzero k, parallel | 8 | 8 | 16 | 0 |
| plateau nonzero k, transverse | 8 | 6 | 12 | 2 |
| regular k=0 | 4 | 3 | 6 | 1 |
| plateau k=0 | 4 | 2 | 4 | 2 |

Nonzero modes use a real cosine/sine pair; k=0 has one real amplitude.
Matrices and multiplier equations are in the result JSON. Counts are outputs,
not script inputs. They leave zero propagating DOF in this STATIC toy problem,
which says nothing about gravitational DOF after adding metric/clock dynamics.
Linear null directions need not survive nonlinearly. On a compact slice a
nonzero mean source violates integrated divergence compatibility; it cannot
be removed by simply dropping k=0.

## 5. Concrete next route and the calculation that can kill it

Keep the exponential law in the TOTAL metric potential, where its primitive
G(y)=y^2+2(1+y)e^-y-2 has positive transverse and longitudinal eigenvalues
for y>0. Both eigenvalues vanish at y=0: that limit remains a real gate.
The script checks the identities and asymptotic limits, not full relativistic
health. An algebraic screen of a NEW VCDM+f(a^2) candidate is included:

\[
S=M^2\int N\sqrt h\,[\tfrac12(R+K_{ij}K^{ij}-K^2)-V(\varphi)
-\tfrac34\lambda^2-\lambda(K+\varphi)
-\lambda_{\rm gf}^iD_i\varphi/N+f(a^2)]+S_m,
\]

with a_i=D_i ln N and f=2a0^2[1-(1+y)e^-y], y=|a|/a0. The starting action
without f is published, not claimed novel: [De Felice, Doll and Mukohyama,
Eq. 36](https://arxiv.org/html/2004.12549v2).
Direct algebraic elimination of lambda gives trace kinetic Hessian zero and
pi=M^2 sqrt(h) varphi. The added f has no velocities. Its leading static
variation gives mu=1-f_s=1-e^-y; f(0)=0 leaves the background action unchanged.
None of these facts supplies the FULL modified constraint count.

The decisive tasks are (1) the modified lapse/trace constraint operator and
FLRW scalar reduction at f_s(0)=1, retaining H, V'', and matter; (2) the full
conserved-source curvature response at nonzero acceleration. Existing
kinetic-conformal regularity results require beta(2 beta-alpha)!=0, which
this zero-field normalization does not satisfy; their two-mode certificate
cannot be imported. [Bellorin and Restuccia, Eq. 2.50](https://arxiv.org/html/1606.02606v2).

The existing G03 `METRIC_CAUSAL_SYMBOL.md` calculation was rerun successfully:
its exact exponential principal system fails finite-speed curvature response
under its stated regular-background/source assumptions. A derivative-free
V(varphi) does not change the highest-derivative nonzero-mode block when
D_i varphi=0. Transfer to the proposed VCDM variant therefore looks obstructed,
but has not been certified here. VCDM's canonical trace constraint must not
be confused with imposing K=0; its K can vary spatially.
[VCDM and Cuscuton, Eqs. 14–19](https://arxiv.org/html/2204.08294v2).

**Do not spend the next cycle on another capture simulation or a scan of V.**
Test the same-action FLRW constraint operator and the causal transfer first.
If the latter survives all admissibility checks, a successful route must alter
the leading kinetic/constraint structure, not just the homogeneous potential.
This is a falsifiable research direction, not a promise of a completed theory.

## Audit status

Two independent derivations agreed on the static signs and coefficient
dictionary. A separate final review found no actionable issue in this static
audit, reran all eight tests and matched the saved result exactly. That review
did not certify the external literature transfer or full relativistic system.
Computational audit supplied exact residuals, real-mode brackets,
controls and provenance. Mathematical self-proofreading covered this new note
only; no original theory text was edited. No novelty or full PPN claims are
made. See REPRODUCE.md for commands, exits and the distinction between a
successful obstruction check and a physically viable theory.
