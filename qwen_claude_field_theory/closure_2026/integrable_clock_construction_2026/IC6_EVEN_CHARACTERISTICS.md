# IC6 even-sector reduction and constructive quartic conditions

Base `0b75e72bf5797e451beb258847ade528cd9c4551`, 2026-09-08.
**IC6 has a scalar principal obstruction arbitrarily close to its isotropic
witness. This IC6 calculation does not implement a replacement action.**
The separate [IC7 continuation](IC7_CURVATURE_SQUARE.md) implements a local
isotropic repair while retaining the sheared-background obstruction.

The full even-sector variation agrees between the IC6 phase Hamiltonian and
its compact plateau Lagrangian on the tested constrained homogeneous states.
Including the actual background evolution recovers the isotropic witness
speeds \(1/3\) and \(1\). An exact local calculation then gives a negative
scalar quartic spatial coefficient on nearby isotropic solutions. A separate
sheared state also has a nonzero mixed time/spatial principal term. These
findings give two concrete conditions for further action construction; they
do not amount to a nonlinear ill-posedness theorem or an empirical claim.

## Actual canonical and auxiliary reduction

Use the unchanged IC6 action on \(\eta=1\), \(J_T>0\), \(K_6\ne0\),
with units \(m=h_0=1\), \(\kappa=6\), and the frozen action constants.
All numerical states below have \(0<u<1\) and lie in the activation plateau.
There is no matter contribution in this gravity-clock calculation.

For a diagonal barred metric write

\[
\bar h=\operatorname{diag}
(B_1^2e^{2\zeta+\gamma},B_2^2e^{2\zeta-\gamma},B_3^2e^{2\rho}),
\qquad \lambda_i=\bar h_{ii}\bar\pi^{ii}.
\]

The exact symplectic density is
\(2(\lambda_1+\lambda_2)\dot\zeta+
(\lambda_1-\lambda_2)\dot\gamma+2\lambda_3\dot\rho\),
in addition to the affine background terms. Varying the longitudinal shift
before reduction gives, for \(k_z\ne0\),

\[
\delta\lambda_3=(\lambda_{10}+\lambda_{20})\zeta
+\tfrac12(\lambda_{10}-\lambda_{20})\gamma+\lambda_{30}\rho.
\]

Only then use \(\rho=0\), with
\(\delta\lambda_1=p_\zeta/4+p_\gamma/2\) and
\(\delta\lambda_2=p_\zeta/4-p_\gamma/2\).
This is a spatial gauge at nonzero wave number, not a treatment of the
homogeneous physical perturbation. The surviving variables are the two
canonical pairs \((q,p)=((\zeta,\gamma),(p_\zeta,p_\gamma))\).

The exact diagonal curvature identity is

\[
\bar R=-\frac{2e^{-2\rho}}{B_3^2}
[2\zeta_{zz}+3\zeta_z^2+\gamma_z^2/4-2\rho_z\zeta_z].
\]

If \(v=\ln V\), \(\pi=\sum_i\lambda_i\),
\(\tau=\sum_i\lambda_i^2-\pi^2/3\), the nongradient Hamiltonian is

\[
H_0=2e^{(4-3u)\xi-v}\left(\frac{\tau}{J_T}-\frac{\pi^2}{6}\right)
+e^{v+(3u-2)\xi}[\Lambda+a_0^2U(u^2)]
-3e^{v+(3u-4)\xi},
\]
\[
J_T=1+\frac{e^{-6(u-1)\xi-2v}\pi^2F}{a_0^2}.
\]

Both \(\xi,u\) are varied. Their quadratic block includes the actual
Hessian of this expression, plus the auxiliary spatial square. The curvature
coefficient is \(c=e^{v+u\xi}J_T/B_3^2\); its variations in all momenta,
\(\xi,u,V\) are retained before spatial integration by parts. In particular,
no \(k^4\) term or \(\delta F\) coupling is discarded before constraints
are eliminated.

The resulting Hessian for \((q,p,n,\delta u)\), where \(n=\delta\xi\),
has the form \(H_0^{(2)}+k_z^2H_1^{(2)}\). Eliminating its actual two
auxiliary equations gives

\[
H_{\rm red}^{(2)}=\tfrac12q^TCq+q^TBp+\tfrac12p^TAp.
\]

The code checks the auxiliary Euler residuals after this Schur complement.
An independent calculation starts from the **compact IC6 Lagrangian**,
differentiates its Hessian in \((Q_i,\widehat R,\xi,u,\ln V)\), retains
the quadratic shift-advection terms, and eliminates
\((\delta\xi,\delta u,\partial_z\beta)\) together. Its reduced Hessian
agrees with

\[
L_{\rm red}^{(2)}=
\tfrac12(\dot q-B^Tq)^TA^{-1}(\dot q-B^Tq)-\tfrac12q^TCq.
\]

This comparison uses all lapse/auxiliary/shift variations, rather than a
frozen-coefficient auxiliary substitution. At \(k=1,10,1000\), the worst
relative bridge residual in the initial 80-digit runs was below
\(3\times10^{-75}\); the code also reports the independently varied
auxiliary/shift Euler residuals. These comparisons are numerical checks of
two independently constructed Hessians, not interval certificates.

## Why the background time derivatives matter

Put \(M=A^{-1}\), \(N=MB^T\), \(S=C-BMB^T\). With time derivatives at
fixed comoving \(k_z\), exact momentum elimination gives

\[
M\ddot q+(\dot M-N+N^T)\dot q+(S-\dot N)q=0.
\]

The implementation evaluates these time derivatives along the **actual**
homogeneous solution tangent:

\[
\dot v=\tfrac12\sum_i(H_0)_{\lambda_i},\quad
\dot\lambda_i=-\tfrac12(H_0)_v,\quad
\frac{d\ln B_3}{dt}=\tfrac12(H_0)_{\lambda_3},
\]
\[
\binom{\dot\xi}{\dot u}
=-(H_0)_{qq}^{-1}(H_0)_{q,\mathrm{can}}
\dot x_{\mathrm{can}}.
\]

The last equation is the differentiated auxiliary constraint, not a chosen
clock rate. Complex-step differentiation at 80 digits is checked against a
second step. Affine background translations in logarithmic metric and mixed
momentum variables add only linear terms canceled by the background equations;
there is no omitted quadratic generating term in the surviving canonical
pairs.

At the exact isotropic witness the complete reduced equation is

\[
\ddot q+3\dot q+
e^{2/3}k_z^2\operatorname{diag}(1/3,1)q=0.
\]

Since the physical squared coordinate light speed is \(e^{2/3}\), this
recovers the independently derived scalar/tensor speeds. As a negative
control, freezing the original canonical Hamiltonian matrix instead yields
a spurious scalar squared-speed limit approximately \(-0.55977091\).
The difference comes from \(\dot N=O(k_z^2)\). The tests require the
corrected isotropic equation, so this mistake cannot silently pass.

## Exact quartic obstruction on nearby isotropic solutions

Scale the isotropic initial momenta by
\(\lambda_i=-e^{-1/2}j\) at \(\bar h=I\), keeping action parameters
fixed, and solve the actual auxiliary constraints. Their nonsingular witness
Hessian gives a smooth local branch, with

\[
\left.\frac{d(\xi,u)}{dj}\right|_1=
\left(-\frac{8\mathcal T+27}{4(4\mathcal T-27)},
-\frac{18}{4\mathcal T-27}\right).
\]

Transverse rotational symmetry decouples the even tensor from the scalar.
The auxiliary spatial square has null direction
\(D_t=\partial_u-b\partial_\xi\); the subscript here is a label, not a
time derivative. Write \(\chi\) for this direction. Let the nongradient
Hessian in \((p_\zeta,\chi)\) be

\[
\mathsf H=\begin{pmatrix}h_{pp}&h_{p\chi}\\h_{p\chi}&h_{\chi\chi}\end{pmatrix},
\]

and the curvature source be \(k_z^2\zeta(g_p p_\zeta+g_\chi\chi)\).
Exact auxiliary and momentum elimination gives the scalar quartic stiffness

\[
S_4=-\frac{h_{pp}g_\chi^2-2h_{p\chi}g_pg_\chi+h_{\chi\chi}g_p^2}
{h_{pp}h_{\chi\chi}-h_{p\chi}^2}.
\]

The actual IC6 kinetic Hessian, including derivatives of \(J_T\), obeys
on isotropic data

\[
h_{pp}=\frac{e^{(4-3u)\xi}}{6V}(J_T^{-1}-1).
\]

At the witness, \(h_{pp}=g_p=S_4=0\). Direct action coefficients give

\[
h_{p\chi}=\frac{2\mathcal T}{9},\qquad
g_\chi=-\frac{e^{1/6}(8\mathcal T-27)}9,
\quad J_T'=-\frac{4(5\mathcal T-27)}{3(4\mathcal T-27)},
\]
\[
h_{pp}'=-\frac{e^{1/2}}6J_T',\qquad
g_p'=\frac{2e^{2/3}}3J_T'.
\]

Primes here mean \(d/dj\) at \(j=1\). Substitution produces the exact
identity

\[
\boxed{
S_4'(1)=-\frac{e^{5/6}(5\mathcal T-27)(8\mathcal T-27)(8\mathcal T+27)}
{18\mathcal T^2(4\mathcal T-27)}<0.}
\]

All factors in the final denominator and numerator are positive for the
frozen domain \(\mathcal T>27/4\). Seven symbolic residual groups check
the generic kinetic Hessian, Schur identity, constraint tangent and coefficient
reductions. A central derivative of the actual nonlinear auxiliary solve at
\(j=1\pm10^{-15}\) separately agrees to better than \(10^{-25}\).

Therefore every sufficiently small positive \(j-1\) has \(S_4<0\), while
the scalar kinetic mass remains positive by continuity from the witness.
The antisymmetric \(N_2\) coefficient is exactly zero on isotropic data.
Consequently the leading scalar equation has
\(M_0\ddot\zeta+S_4 k_z^4\zeta\), with real temporal roots
\(\lambda\sim\pm\sqrt{-S_4/M_0}\,k_z^2\).
Background time derivatives contribute at order \(k_z^2\) and cannot
cancel this quartic coefficient. This is an analytic principal obstruction
on actual nearby homogeneous solutions; it is not inferred solely from a
floating-point fixture or from freezing a nonstationary momentum.

For orientation, the actual \(j=1.007\) solution gives
\(\xi\simeq0.24297809\), \(u\simeq0.66347046\),
\(S_4\simeq-0.07526051653\) and
\(\lambda^2/k_z^4\to0.03456985650\).
This does not prove nonlinear PDE ill-posedness; it does prevent this IC6
branch from satisfying the requested positive, finite-cone scalar principal
behavior on all nearby backgrounds.

## Shear and the two constructive cancellation conditions

The supplied sheared initial momenta are treated as exact decimal data:

\[
\lambda=(-0.6424435072183933,-0.622272178918671,-0.5676134368548011).
\]

The script re-solves the auxiliary constraints to 80-digit precision. It gets
\(\xi=0.242752746344542675\),
\(u=0.663589818477735377\), \(J_T=0.986102159712075428\).
The initial auxiliary residuals are below \(10^{-78}\).

An exact rank-one inverse formula for the auxiliary block gives leading
coefficients

\[
A\sim A_0,\quad B\sim k_z^2B_2,\quad C\sim k_z^4C_4,
\qquad M_0=A_0^{-1},\quad N_2=M_0B_2^T,
\quad S_4=C_4-B_2M_0B_2^T.
\]

Two necessary construction conditions for eliminating these higher spatial
orders in this reduced class are

\[
\boxed{N_2=N_2^T,\qquad S_4=0.}
\]

They are conditions on the actual action Hessians after constraints are
varied. They are not sufficient for positive or luminal remaining cones;
the order-\(k_z^2\) matrix, including \(\dot N_2\), must then be tested.
The script obtains on the sheared data

\[
N_2\simeq\begin{pmatrix}-3.63094656487434&0\\
0.000563025148110635&0\end{pmatrix},\qquad
S_4\simeq\begin{pmatrix}-0.0642323935174161&0\\0&0\end{pmatrix}.
\]

For \(\lambda=k_z^2z\), the complete leading pencil is

\[
\det[z^2M_0+z(-N_2+N_2^T)+S_4]=0.
\]

It has a nonzero branch with
\(z^2\simeq0.03017563410255345>0\).
The full time-dependent reduced coefficient calculation over
\(k_z=10,100,1000,10000\) approaches this value. The remaining wave pair
approaches a physical squared phase ratio near \(1.000013733\) on this
particular state. No universal interpretation or exact inequality is inferred
from that small numerical displacement.

## A curvature-square correction is concrete but insufficient under shear

Adding a Hamiltonian density term \(c_{RR}\bar R^2\) at \(V=B_3=1\)
shifts the scalar quartic Hessian by \(32c_{RR}\), since
\(\bar R_1=4k_z^2\zeta\). Choosing

\[
c_{RR}=-S_{4,\zeta\zeta}/32
\]

would cancel the displayed quartic stiffness. On the sheared state this is
\(c_{RR}\simeq0.00200726229741925\). The gyroscopic coefficient is
unchanged, however. The corrected leading pencil would still have
\(z^2\simeq-4.91923345112562\times10^{-7}\): an order-\(k_z^2\)
oscillatory-frequency branch remains. Thus a curvature-square correction
alone does not restore finite-cone second-order propagation under shear.

On isotropic data an equivalent exact design formula uses the nongradient
Hamiltonian **per barred volume** \(h(\rho,\tau,\xi,u)\), where
\(\rho\) here denotes normalized trace momentum (not the earlier metric
gauge perturbation), and \(c=e^{u\xi}J_T\). At \(\tau=0\), set

\[
\mathsf M=\begin{pmatrix}
h_{\rho\rho}/4+h_\tau/12&D_t h_\rho/2\\
D_t h_\rho/2&D_t^2h
\end{pmatrix},\qquad
v=\binom{c_\rho/2}{D_tc}.
\]

Then \(g=-2v\), \(S_4=-4v^T\mathsf M^{-1}v\), so a term
\(V\eta c_7\bar R^2\) with
\(c_7=v^T\mathsf M^{-1}v/8\) has the correct isotropic cancellation
normalization. The corresponding covariant density factor is
\(\eta e^{w-\xi}c_7\widehat R^2\), because
\(\bar R=e^{2w}\widehat R\) and \(N\sqrt h=Ne^{3w}V\).
This independently checks the parent continuation's proposed coefficient.
It does not implement that action, certify its branch, or solve the shear
integrability condition.

## Reproduction and scope

Files: [ic6_even_characteristics.py](ic6_even_characteristics.py) and
[test_ic6_even_characteristics.py](test_ic6_even_characteristics.py).
The script pins the three frozen action-document hashes and emits its own
hash, software versions, numerical residuals, exact sign formula and explicit
unproved flags. Existing files are not imported or modified.

From the repository root, with the cooperative environment prefix
`OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1`:

```text
python3 qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026/test_ic6_even_characteristics.py
python3 qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026/ic6_even_characteristics.py
python3 qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026/ic6_even_characteristics.py --require-all-background-causality
```

The final test suite has 13 tests. The first asymptotic test run failed an
overly strict finite-\(k\) leading-coefficient tolerance; retaining the
known next two terms of the exact asymptotic expansion resolved that test
without changing the calculation. The negative global-causality command
returns exit 2 by design. Runs take approximately one second, below the
180-second experiment limit. Python 3.9.6, SymPy 1.14.0 and mpmath 1.3.0
were used, with 80-digit numerical precision and exact symbolic sign
identities. Thread caps are cooperative, not operating-system affinity.
The parent continuation records bounded-run manifests centrally.

The Hessian and constraint normalizations were independently reviewed by a
separate agent, and the compact-Lagrangian bridge is a distinct construction.
This is not a fully independent proof of the entire theory. The new exact
claim is the local isotropic sign implication above; the quantitative sheared
values remain controlled numerical evidence in the stated fixture.
