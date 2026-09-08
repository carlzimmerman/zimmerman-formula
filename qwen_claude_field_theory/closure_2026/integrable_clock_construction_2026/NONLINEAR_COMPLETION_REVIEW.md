# Local nonlinear auxiliary-gradient completion: constructive review

2026-09-08. Base: `6708f1e3e`. Read-only mathematical assessment of the
[IC-4 action](IC4_ACTION.md), [IC-1 homogeneous/static conventions](ACTION.md),
and `local_clock_wave.py`. Only this report is added. No full-theory verdict,
new empirical claim, global novelty claim, or nonlinear degree-of-freedom
count follows from it.

## Result and the necessary sign distinction

A new Hamiltonian can satisfy all three requested compatibility conditions
locally: exact stationary first-variation agreement, an unchanged flat
homogeneous Hamiltonian, and the unchanged IC-4 scalar quadratic action.
An activation with a constant plateau can make its auxiliary-gradient sector
an **exact single square on an open expanding domain**. One auxiliary variable
then has an elliptic equation and the other an algebraic equation.

The relevant square is negative in the Hamiltonian. It is **minus** the
auxiliary Hamiltonian Hessian that is positive/coercive. This is not a claim
that auxiliary Hamiltonian energy itself is positive, nor a substitute for
the separate physical reduced-energy calculation.

The replacement must generally change cubic perturbation terms. It can match
the old gradient matrix's value at the witness, but cannot also match all of
its first field derivatives while remaining rank one. The exact obstruction
to that stronger, unnecessary matching requirement is calculated below.

## 1. Definitions and an explicit Hamiltonian

Use barred canonical metric variables, with

\[
\xi=\ln N,\quad w=(u-1)\xi,\quad V=\sqrt{\bar h},\quad
\pi=\bar h_{ij}\bar\pi^{ij},\quad
\pi_{\rm TF}^{2}=\bar\pi^{ij}\bar\pi_{ij}-\pi^2/3.
\]

Here \(\pi\) is a density and \(\pi/V\) is a spatial scalar. Gradient
contractions in the canonical formulas use the intrinsic barred metric;
the explicitly covariant formulas in Section 6 use the physical leaf metric.
Keep the IC-4 constants \(\ell,\mathcal T,e,\alpha,d,\beta,\gamma,F\), where

\[
e=\tfrac18,\quad d=-9e/\mathcal T,\quad
\alpha=81e/\mathcal T^2,\qquad
b=d/\alpha-\tfrac38=-\mathcal T/9-\tfrac38.
\]

The following densities do not include the shift multiplier or the unchanged
ordinary-matter Hamiltonian, which must be retained when assembling the full
system:

\[
\begin{aligned}
\mathcal H_b={}&\frac{2e^{(4-3u)\xi}}{mV}
 (\pi_{\rm TF}^2-\pi^2/6)-\frac m2Ve^{u\xi}\bar R\\
&+mVe^{(3u-2)\xi}[\Lambda+a_0^2U(u^2)]
-\frac\kappa2Ve^{(3u-4)\xi},\\
\mathcal D={}&-\frac{e^{(6-5u)\xi}\pi^2}{2mVa_0^2},\\
\bar J={}&\frac{3}{4\ell^2}
 [\alpha|D\xi|^2+\beta D\xi\cdot Du+\gamma|Du|^2],\\
\mathcal G={}&-mVe^{u\xi}
 [2u\xi D\xi\cdot Du+\xi^2|Du|^2]+\mathcal D\bar J,\\
\mathcal S={}&-mVe^{u\xi}\alpha|D(\xi+bu)|^2.
\end{aligned}
\]

Put \(h_0=\sqrt{\kappa/(6m)}\) and

\[
r=-\frac{\pi e^{(4-3u)\xi}}{3mVh_0}.
\]

One explicit smooth, momentum-reversal-even activation is

\[
\eta(r)=\frac{E(1/4-(r^2-1)^2)}
 {E(1/4-(r^2-1)^2)+E((r^2-1)^2-1/16)},\qquad
E(t)=\begin{cases}e^{-1/t}&t>0,\\0&t\le0.\end{cases}
\]

This is exactly the activation implemented in `nonlinear_square_completion.py`,
not merely another cutoff with similar support. Its denominator is positive;
it equals one for \(|r^2-1|\le1/4\), and zero for
\(|r^2-1|\ge1/2\).
The proposed new Hamiltonian density is

\[
\boxed{\mathcal H_5=\mathcal H_b+\mathcal D F\bar R
 +(1-\eta)\mathcal G+\eta\mathcal S.}
\]

This is a specified **new Hamiltonian**, not a canonical rewriting of exact
IC-4. In particular, \(\mathcal H_b+\mathcal D(F\bar R+\bar J)\) uses the
term linear in the IC-4 kinetic modification. The exact IC-4 trace Hamiltonian
contains its reciprocal denominator. With

\[
Z=\frac{e^{-2w}}{a_0^2}(\bar J+F\bar R),
\]

the omitted reciprocal-denominator contribution begins at \(O(Z^2)\). On the
chosen flat witness, \(\bar J=O(\epsilon^2)\) and
\(F\bar R=O(\epsilon^2)\), so this difference starts at fourth perturbative
order. It must not be described as an exact IC-4 Hamiltonian identity.

## 2. The three compatibility checks

**Stationary limit.** At \(\pi^{ij}=0\), both \(\mathcal D\) and its first
momentum derivatives vanish. The activation is identically zero in a
neighborhood of \(r=0\). Thus \(\mathcal H_5\) has exactly the IC-1 static
Hamiltonian and first variations there. In unitary time this Hamiltonian is
minus the zero-velocity static Lagrangian; agreement means the corresponding
stationary equations, not equality of Hamiltonian and Lagrangian signs.
This does not manufacture the missing globally matched galactic solution.

**Flat homogeneous limit.** All displayed spatial gradients and \(\bar R\)
vanish identically, so \(\mathcal H_5=\mathcal H_b\) for every flat
homogeneous configuration, not merely at the witness. The homogeneous action
and its independent uniform-mode calculation therefore remain unchanged.
No corresponding claim is made for spatially curved FLRW backgrounds.

**Witness quadratic action.** At

\[
\xi_0=\tfrac14,\quad u_0=\tfrac23,\quad
\pi_0=-3mVh_0e^{-1/2},\quad r_0=1,
\]

one obtains

\[
\mathcal D_0\frac3{4\ell^2}=-mVe^{1/6},\qquad
\mathcal G^{(2)}=-mVe^{1/6}\alpha|D(\delta\xi+b\delta u)|^2
=\mathcal S^{(2)}.
\]

The activation is constant on an open neighborhood of the witness. Hence
\(\mathcal H_5-\mathcal H_4=O(\epsilon^3)\); its value, first variation and
quadratic Hamiltonian agree there. The same linear physical scalar-wave result
transfers after the regular local Legendre transformation. This statement does
not assert agreement of cubic interactions or nonlinear characteristics.

## 3. Why first-derivative matching is too strong

Write \(\mathcal G=-mVe^{u\xi}G_{AB}Dq^A\cdot Dq^B\), \(q=(\xi,u)\).
At fixed \(\theta=\pi/(mV)\),

\[
G=\begin{pmatrix}0&u\xi\\u\xi&\xi^2\end{pmatrix}
+\rho\begin{pmatrix}\alpha&\beta/2\\\beta/2&\gamma\end{pmatrix},\qquad
\rho=\frac{3\theta^2e^{6(1-u)\xi}}{8a_0^2\ell^2},\quad \rho_0=1.
\]

The null vector of \(G_0=\alpha(1,b)^T(1,b)\) is \(v=(-b,1)^T\).
Actual differentiation gives

\[
v^TG_{,\xi}v\big|_0=\frac{2\mathcal T}{27}+\frac58>0,\qquad
v^TG_{,u}v\big|_0=\frac{\mathcal T}{9}+\frac{15}{32}>0.
\]

For any differentiable exact rank-one curve \(G_*=caa^T\) through \(G_0\),
\(v^T\delta G_*v=0\). Therefore the old first jets cannot all be retained.
An invertible point field transformation also preserves the gradient matrix's
rank by congruence; it cannot alone remove this issue. Altering cubic terms,
as \(\mathcal H_5\) does, is consistent with the requested quadratic matching.

## 4. Local mixed algebraic–elliptic coercivity route

On the activation plateau, set

\[
s=\xi+bu,\qquad \rho_a=u,\qquad \xi=s-b\rho_a.
\]

This is an invertible point transformation, with canonical momenta
\(p_s=p_\xi\), \(p_{\rho_a}=p_u-bp_\xi\). The two primary zero momenta are
not replaced by an additional auxiliary velocity pair. The gradient density
of \(-\mathcal H_5\) is exactly

\[
A(s,\rho_a)|Ds|^2,\qquad
A=mV\alpha e^{\rho_a(s-b\rho_a)}>0,
\]

and there is no \(D\rho_a\) term. For fixed barred canonical metric/momentum,
the \(\rho_a\) equation is algebraic, while the \(s\) equation is elliptic.

The directly differentiated witness auxiliary mass matrix is

\[
\frac{H_{qq}}{mVh_0^2e^{-1/2}}=
M_0=\begin{pmatrix}-24&27\\27&-2\mathcal T-135/8\end{pmatrix}.
\]

Thus \((-M_0)_{11}=24\) and
\(\det(-M_0)=12(4\mathcal T-27)>0\). The logarithm bound already used in
IC-4 gives \(\mathcal T>27/4\). This mass sign persists under the invertible
\((s,\rho_a)\) transformation and sufficiently small coefficient variations.

For a concrete operator theorem, fix a compact spatial manifold, periodic cell,
or decay/Dirichlet domain with controlled geometry. Work at a fixed time, or
on a bounded time interval with uniform bounds. Require the fields and
canonical metric/momentum to remain inside the activation plateau; bound the
curvature entering \(F\bar R\); and take \(|Ds|\) sufficiently small.
Suppose the algebraic Hessian of \(-\mathcal H_5\) is bounded below by
\(c_0I\), and \(A\ge a_0^{\rm ell}>0\), with bounded first and second
field derivatives of \(A\). These conditions hold at the witness and are
open in the corresponding coefficient norms.

For a variation \((\delta s,\delta\rho_a)\), the extra cross terms have the
form \(4\delta A\,Ds\cdot D\delta s+\delta^2A|Ds|^2\). Young's inequality
therefore yields, for sufficiently small background \(|Ds|\),

\[
\delta^2(-H_5)\ge c\bigl(
\|\delta s\|_{L^2}^2+\|\delta\rho_a\|_{L^2}^2+
\|D\delta s\|_{L^2}^2\bigr),\qquad c>0.
\]

The natural space is \(H^1_s\oplus L^2_{\rho_a}\), **not** a claim of
two-gradient coercivity on \(H^1\oplus H^1\). The algebraic implicit-function
step eliminates \(\rho_a\) locally; the remaining Schur operator is elliptic.
This supplies a precise local coercivity/invertibility route. Specifying the
function spaces, boundaries and regularity of the complete constraint drift
is still required before promoting it to a full preservation/evolution theorem.

## 5. Legendre map and symmetry obligations

On the plateau, the metric-momentum dependence remains quadratic. Its trace
factor relative to the GR Hamiltonian is

\[
1+\frac32Y_R,\qquad Y_R=e^{-2w}F\bar R/a_0^2.
\]

The metric Legendre block is nondegenerate near the witness because this
factor is one there. Equivalently its reconstructed trace Lagrangian factor
is \((2/3)/(1+3Y_R/2)\). No such assertion is made on its zero surface or in
the activation-transition region, where derivatives of \(\eta(r)\) change
the momentum Hessian. The explicit covariant reconstruction in Section 6
supersedes the earlier open algebraic-reconstruction obligation; it is
derived from this new Hamiltonian, not borrowed from IC-4.

Spatial diffeomorphisms are preserved by the displayed density weights and
scalar activation. The even activation above also avoids unnecessarily
breaking momentum-reversal symmetry; a one-sided cutoff around \(r=1\)
would require explaining that additional choice. Section 6 supplies the varied
clock and the same physical matter coupling in a diffeomorphism-covariant
phase-space action. Deriving the full metric/clock Euler–Lagrange equations,
checking constraint-drift regularity and completing the functional constraint
algebra remain explicit tasks. No degree-of-freedom theorem is inferred merely
from the labels “clock,” “auxiliary,” or “activation.”

The strongest surviving result is the explicit compatible local Hamiltonian
completion and its mixed coercivity estimate under stated open-neighborhood
hypotheses. The activation profile is a design input. Global transition-region
health, nonlinear physical causality, stationary/cosmological matching and PPN
are not settled by this construction.

## 6. Explicit covariant phase-space reconstruction

Work on \(X=-\nabla_\mu T\nabla^\mu T/2>0\), with
\(N=(2X)^{-1/2}\), \(\xi=\ln N\), and the future-directed unit normal
\(n_\mu=-\nabla_\mu T/\sqrt{2X}\). Let
\(h_{\mu\nu}=g_{\mu\nu}+n_\mu n_\nu\), \(a_\mu=D_\mu\xi\),
\(W=n^\mu\nabla_\mu w\), and
\(Q_{\mu\nu}=K_{\mu\nu}-h_{\mu\nu}W\). In this section all dot products,
traces and \(D\)-contractions are physical leaf-metric contractions. Set

\[
\widehat R=e^{-2w}\bar R,\qquad J=e^{-2w}\bar J,\qquad
C=\Lambda+a_0^2U(u^2).
\]

Take \(P^{\mu\nu}\) to be a symmetric tangential tensor: six independent
leaf components, not an unconstrained ten-component field. Put
\(p=h_{\mu\nu}P^{\mu\nu}\) and
\(P_{\rm TF}^{\mu\nu}=P^{\mu\nu}-p h^{\mu\nu}/3\). Define

\[
\begin{aligned}
\mathscr H_5={}&\frac2m(P_{\rm TF}^2-p^2/6)+mC-\kappa X
-\frac m2\widehat R-\frac{p^2F\widehat R}{2ma_0^2}\\
&-(1-\eta)\left[m(2u\xi\,a\cdot Du+\xi^2|Du|^2)
 +\frac{p^2J}{2ma_0^2}\right]
-\eta m\alpha|D(\xi+bu)|^2,
\qquad r=-\frac{Np}{3mh_0},\\
S_5={}&\int d^4x\sqrt{-g}\,[2P^{\mu\nu}Q_{\mu\nu}-\mathscr H_5]
+S_m[g,\psi].
\end{aligned}
\]

This is a specified covariant phase-space action for the same \(H_5\), not a
bare appeal to restoring a clock. The normal/tangential restrictions belong
to the field definition; a redundant parametrization would require its own
constraints. The six components of \(P\) represent the existing metric
momentum, not an additional matter sector.

In unitary coordinates its exact canonical dictionary is

\[
\bar\pi^{ij}=V e^{5w}P^{ij},\qquad
p=e^{-3w}\pi/V,\qquad
P_{\rm TF}^2=e^{-6w}\pi_{\rm TF}^2/V^2.
\]

Indeed,

\[
Q_{ij}=\frac{e^{2w}}{2N}
 (\dot{\bar h}_{ij}-\mathcal L_{\vec N}\bar h_{ij}),\qquad
2N\sqrt h\,P^{ij}Q_{ij}
=\bar\pi^{ij}(\dot{\bar h}_{ij}-\mathcal L_{\vec N}\bar h_{ij}).
\]

The terms proportional to \(\dot w-N^iD_iw\) cancel exactly, including
both the lapse-velocity and auxiliary-velocity contributions. Multiplying
each of the eight displayed Hamiltonian terms by
\(N\sqrt h=NVe^{3w}\) gives respectively the canonical kinetic density,
potential, clock term, intrinsic-curvature term, \(\mathcal D F\bar R\),
static-gradient term, \(\mathcal D\bar J\), and the square \(\mathcal S\).
The activation argument also maps exactly to Section 1. The usual shift
constraint follows from the displayed symplectic density by spatial
integration by parts, with the unchanged matter contribution retained.

On the constant activation plateau define

\[
\mathcal K=1+\frac{3F\widehat R}{2a_0^2}.
\]

Variation with respect to the actual six momentum components gives

\[
P_{\rm TF}^{\mu\nu}=\frac m2 Q_{\rm TF}^{\mu\nu},\qquad
p=-\frac{mQ}{\mathcal K},
\]

and, for \(\mathcal K\ne0\), the same-action local Lagrangian on that branch is

\[
\mathscr L_5=\frac m2\left[
Q_{\rm TF}^2-\frac{2Q^2}{3\mathcal K}
+\widehat R-2C+2\alpha|D(\xi+bu)|^2\right]+\kappa X.
\]

This formula is valid only where the resulting
\(r=NQ/(3h_0\mathcal K)\) remains on the plateau. It is not a formula
for the transition region. At the witness \(\mathcal K=1\) and \(r=1\),
so the regular branch contains an open neighborhood.

The static comparison instead uses the full phase-space action on its
\(P=0,\eta=0\) branch, **not** the plateau-only eliminated formula.
The conformal identity
\(\widehat R=R(h)+4D^2w-2|Dw|^2\), with
\(Dw=(u-1)a+\xi Du\), yields

\[
\mathscr L_{5,\mathrm{stat}}-\mathscr L_{1,\mathrm{stat}}
=\frac{2m}{N}D_i(ND^iw).
\]

After multiplication by \(N\sqrt h\), this is a spatial boundary term.
Thus stationary first variations agree for compactly supported or periodic
variations, sufficient decay, or boundary conditions/counterterms that annul
this displayed boundary variation. Dirichlet values alone should not be
silently assumed to fix all normal derivatives. The unintegrated densities
need not be pointwise equal. No unproved time integration by parts is used here.

The action is explicitly diffeomorphism-covariant for a varied clock on its
timelike-gradient domain. This fact and its exact canonical dictionary do not
alone establish regularity of the complete nonlinear equations, global
Legendre invertibility, a physical characteristic cone, or a full constraint
classification. Those remain separate obligations.

## 7. Executed exact checks

Read-only SymPy execution used
`OPENBLAS_NUM_THREADS=1 /opt/homebrew/Caskroom/miniconda/base/bin/python -B`
with standard input; exit **0**. It differentiated the homogeneous Hamiltonian
before substituting the witness, and independently formed the gradient matrix
above. Returned checks were:

```text
auxiliary mass matrix residual Matrix([[0, 0], [0, 0]])
minus mass leading minor 24
mass determinant identity 0
rho witness 1
rank one identity Matrix([[0, 0], [0, 0]])
rank 1
null derivative xi (5*ell + 8)/(10*ell) residual 0
null derivative u 3*(15*ell + 64)/(160*ell) residual 0
transformed minus mass determinant residual 0
H stationarity 0 0
```

The two null-derivative expressions equal the displayed formulas after
\(\mathcal T=-27/16+54/(5\ell)\). These exact finite algebra checks verify
the identities used in the local estimate; they do not execute a nonlinear
functional constraint solver.

A second independent, read-only SymPy command with the same Python invocation
checked every term in the physical-to-barred density dictionary, the full
\(\dot w\)-term cancellation, actual differentiation with respect to trace
and traceless momentum components, and the stationary divergence identity.
It exited **0**, returning

```text
eight density residuals [0, 0, 0, 0, 0, 0, 0, 0]
activation residual 0
full symplectic wdot cancellation 0
actual momentum solutions {Pt: Qt*m/2, pp: -Q*m/K}
Legendre residual 0
static divergence residual 0
```

The read-only review also covered `derive()`, the finite-grid implementation,
result serialization and CLI in `nonlinear_square_completion.py`. The mass
matrix comes from actual differentiation at fixed canonical data; the square
rank and mass determinant are computed, not supplied as expected answers.
No blocker was found within those bounded claims. The grid solve is not an
independent proof of continuum coercivity or nonlinear physical evolution.

The independently rerun commands were the same Python invocation followed by
`qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026/nonlinear_square_completion.py`
and respectively:

- `--symbolic-only`: exit **0**, every exact residual zero.
- `--symbolic-only --require-full-closure`: exit **2**, correctly retaining
  `full_theory_closed: false` despite those algebraic passes.

The audited module SHA-256 was
`4f440d250b88ef955c5656589a5337f6a47dfcbc012502a14c10dc1d1b5a23bd`;
its IC-4 action input was
`cb37292e21e0b1fbeef59a20f7800cb3d32c0cd20a46d36fd286cc3dd0f467a8`.
The run reported Python 3.13.9, SymPy 1.13.1 and NumPy 1.26.4.
The pinned `scalar_completion.py` remained at SHA-256
`801e50f8a3485842eec9bafd58d4f652c42200050917da6d9f0360aea5ff7745`.

No other source or code file was modified by this review.

## 8. Frozen-source and functional-statement re-review

The subsequently frozen `nonlinear_square_completion.py` has SHA-256
`4c9a79caa9a6d54a6a5f006440886f54b9092d68978249fb79f95a0f73229ece`;
its test module has SHA-256
`5623fd5e0d1ea231d8644e236bf358dc776feac7d656fb3607f163b10c8846a2`.
The refactor delegates `numerical()` to
`solve_auxiliary_density(d, Hnongrad)`. That function actually differentiates
the supplied density; the added regression perturbs it and recomputes the
solution rather than reusing the previous fixture. The specified gradient
density and fixed numerical domain remain unchanged. This is a reusable
density calculation within that domain, not an arbitrary-action solver.

Using the same thread-capped Python invocation and directory prefix recorded
above, independent reruns gave:

- `test_nonlinear_square_completion.py`: **16 tests, exit 0**.
- `nonlinear_square_completion.py`: **exit 0**, all exact residuals zero;
  the 16/32/64-node solves reproduced maximum residual
  \(1.196\times10^{-14}\) and minimum discrete Hessian eigenvalue
  \(4.4237\).
- `nonlinear_square_completion.py --symbolic-only --require-full-closure`:
  **exit 2**, preserving the unpassed full-theory gate.

The review also checked the exact phase-space action in `IC5_ACTION.md` and
Sections 2–4 of `NONLINEAR_SQUARE_REPORT.md`. Their signs, volume factors,
same-action switch and plateau momentum inversion agree with Section 6 above.
The stated Young bound is sufficient for a bounded symmetric coercive
linearized form on \(H^1_s\oplus L^2_t\). The closed-range/zero-orthogonal-
complement argument then correctly proves the represented weak linearized
operator is an isomorphism to its dual. This does not assert that the full
nonlinear constraint map is defined on an unrestricted open set of that
low-regularity space, or supply a nonlinear evolution theorem.

The preservation block has the correct signs for
\(C=\delta(-H_5)/\delta q\):
\(\{p,C\}=-L\), and preservation gives
\(L\lambda=-\{C,H_5\}\) modulo transport. Its displayed block inverse
must be read formally, or on a common domain where the actual secondary
bracket \(\Omega\) and the compositions with \(L^{-1}\) are defined.
The weak isomorphism of \(L\) alone does not prove that domain statement for
the full Dirac matrix. The report's continued requirements of expanded drift,
regularity and staying on the plateau are therefore substantive, not optional.

The author was asked to make that operator-domain qualifier explicit beside
the block inverse, specify the static boundary prescription, and update the
outdated fifteen-test count. No root-authored document or source was edited
by this re-review. No IC-6 construction was included in this audit.
