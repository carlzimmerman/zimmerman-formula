# IC-4 auxiliary principal symbol and a constructive square-form condition

Base: `6708f1e3e`, 2026-09-08. **Necessary local compatibility calculation;
full nonlinear theory remains open.** Only the three files named in this
package are new. No pinned action, calculation, or manifest was changed.

## Result and scope

IC-4's auxiliary-gradient null direction is exact on its expanding witness,
but is not an identity in the independent background fields and trace
momentum. A negative outer-square Hamiltonian can reproduce this witness's
quadratic jet and leave the flat homogeneous action unchanged. Preserving the
original static branch requires matching back to its original gradient
Hamiltonian; a smooth static/expanding patch is one constructive way to do so.

This is a fixed-barred-metric auxiliary principal-symbol calculation, not a
full coupled metric symbol, a nonlinear Dirac count, or an on-constraint
existence theorem for the off-witness parameters. In particular, a null
direction of a gradient block is **not** a null direction of the full
auxiliary constraint matrix.

## Differentiate the actual Hamiltonian

Write $V=\sqrt{\bar h}$, $\xi=\ln N$, $w=(u-1)\xi$, and

\[
C_k=\frac m2V e^{(3u-4)\xi},\qquad
D_+=\frac m2V e^{u\xi},\qquad E=\frac{e^{-2w}}{a_0^2},
\]
\[
\bar J=A_J|\bar D\xi|^2+B_J\bar D\xi\cdot\bar Du+C_J|\bar Du|^2,
\quad Z=E(\bar J+F\bar R),\quad t=-\frac23+Z.
\]

The differentiated density is

\[
\mathcal H=\frac{\pi_{\rm TF}^2+\pi^2/(9t)}{C_k}
-D_+\left(4u\xi\bar D\xi\cdot\bar Du+2\xi^2|\bar Du|^2\right).
\]

Terms independent of auxiliary gradients do not contribute to this block.
At $\bar D\xi=\bar Du=0$ and $\bar R=0$, direct differentiation of the
**rational** trace term gives

\[
\rho=\frac{\pi^2 E}{4C_kD_+}
=\frac{\pi^2e^{-6w}}{m^2V^2a_0^2},\qquad
\boxed{\mathcal H_{gg}=-D_+
\begin{pmatrix}
2\rho A_J&\rho B_J+4u\xi\\
\rho B_J+4u\xi&2\rho C_J+4\xi^2
\end{pmatrix}.}
\]

Here $g=(\partial_i\xi,\partial_i u)$ in a local orthonormal barred frame;
rotational invariance supplies $\bar h^{ij}$ for a general covector. The
trace-free momentum and $F\bar R$ contribute nothing to this fixed-metric,
flat-background block. This does not discard their metric cross-variations.

For secondary constraints $\chi_a=-\delta H/\delta\phi_a$,
$\phi=(\xi,u)$, the constant-coefficient principal part is
$\chi_a=\mathcal H_{gg,ab}\bar\Delta\delta\phi_b$. Thus
$\{\chi_a,p_b\}_{\rm principal}=-|k|_{\bar h}^2\mathcal H_{gg,ab}$.
This functional sign and covector factor are analytic identities; the
program evaluates the finite two-field coefficient matrix. It does not
execute an infinite-dimensional Poisson-rank calculation.

## Bridge to the independently computed quadratic Hamiltonian

On the frozen witness,

\[
\xi_0=\frac14,\quad u_0=\frac23,\quad
\pi_0=-3mVe^{-1/2}h,\quad
a_0^2=\frac{27h^2e^{-1/2}}{8\ell^2},\quad
\rho_0=\frac{8\ell^2}{3}.
\]

The coefficients are imported from the frozen action calculation. With
its $\alpha,\beta,\gamma$, this gives $\mathcal H_{gg,0}=-2D_{+,0}G_0$,
where

\[
G_0=\begin{pmatrix}2\alpha&\beta+1/3\\
\beta+1/3&2\gamma+1/8\end{pmatrix}
=2\alpha\begin{pmatrix}1&b\\b&b^2\end{pmatrix},\qquad
b=-\frac{\mathcal T}{9}-\frac38.
\]

The zero determinant and null vector $(-b,1)$ are calculated, not supplied
as expected ranks. In the pinned twice-spatial-average convention,
$H_2=|k|_{\bar h}^2\phi^T\mathcal H_{gg}\phi/2$.
Since $x=e^{2/3}|k|_{\bar h}^2/h^2$ and
$F_{\rm mode}=mVe^{-1/2}$, the normalized gradient Hessian is $-xG_0$.
The independently Legendre-transformed result in `quadratic_dirac.py` is
checked against this matrix:

\[
\frac{H_{(n,v)(n,v)}}{F_{\rm mode}h^2}=-M,\qquad
M=\begin{pmatrix}24&-27\\-27&2\mathcal T+135/8\end{pmatrix}+xG_0,
\]
\[
\det M=\frac{3(4\mathcal T-27)(8\mathcal T+x)}{2\mathcal T}>0
\quad(\mathcal T>27/4,\ x\ge0).
\]

Thus $M$ is positive definite on this domain although $G_0$ is rank one.
The displayed $x=0$ statement concerns this algebraic matrix limit, not an
identification of the genuine uniform-mode phase space with $k>0$.

## What changes off the witness

Let $j=\pi/\pi_0$ while $V$ and action parameters remain fixed. Then

\[
\lambda=\rho/\rho_0
=j^2 e^{-6[(u-1)\xi+1/12]},\qquad
G=\frac{-\mathcal H_{gg}}{2D_+}
=\begin{pmatrix}2\alpha\lambda&\beta\lambda+2u\xi\\
\beta\lambda+2u\xi&2\gamma\lambda+2\xi^2\end{pmatrix}.
\]

The full first derivatives of $\det G$, including the field dependence of
$\lambda$, evaluated at $(j,\xi,u)=(1,1/4,2/3)$ are

\[
\partial_j\det G=-\frac{3(16\mathcal T+81)}{16\mathcal T^2},\quad
\partial_\xi\det G=\frac{3(16\mathcal T+135)}{16\mathcal T^2},\quad
\partial_u\det G=\frac{9(32\mathcal T+135)}{64\mathcal T^2}.
\]

All are nonzero on the action's $\mathcal T>27/4$ domain. These are
independent phase-space directions, not a claim that arbitrary such
deviations solve all constraints. At $\pi=0$, $\det G=-4u^2\xi^2$;
it is generically negative, with special zero loci $u\xi=0$ explicitly
excluded from that strict sign claim.

## Precise construction condition

For $\rho A_J\ne0$, a rank-one gradient coefficient requires

\[
(\rho B_J+4u\xi)^2=4\rho A_J(\rho C_J+2\xi^2),
\]
\[
\boxed{C_J=\frac{(B_J+4u\xi/\rho)^2}{4A_J}-\frac{2\xi^2}{\rho}.}
\]

More specifically, the desired density
$-D_+L|\bar D\xi+b\bar Du|^2$ requires

\[
A_J=\frac L\rho,\qquad
B_J=\frac{2Lb-4u\xi}{\rho},\qquad
C_J=\frac{Lb^2-2\xi^2}{\rho}.
\]

These equations concern the gradient jet. They cannot be satisfied for all
trace momenta by fixed field-only coefficients on a generic $u\xi\ne0$
domain: $\det(-\mathcal H_{gg}/D_+)$, as a polynomial in $\rho$, has
constant term $-16u^2\xi^2$.
They also do not produce a regular extension through $\rho=0$ by themselves.

For **finite gradients**, the exact trace difference is

\[
H_{\rm kin}(Z)-H_{\rm kin}(0)
=-\frac{\pi^2}{4C_k}\frac{Z}{1-3Z/2}.
\]

Put $Q_g=4u\xi\bar D\xi\cdot\bar Du+2\xi^2|\bar Du|^2$,
$R_g=L|\bar D\xi+b\bar Du|^2-Q_g$, and
$a=\pi^2/(4C_kD_+)$. Solving the exact rational equation, rather than
truncating it, gives

\[
Z=\frac{R_g}{a+3R_g/2},\qquad
\bar J=\frac{R_g}{\rho+3ER_g/2}\quad(\bar R=0).
\]

These identities require nonzero displayed denominators and the regular
Legendre branch $t\ne0$. Their leading quadratic jet is $\bar J=R_g/\rho$.
They are compatibility formulas, not a proposed globally regular action.

An exact Hamiltonian square with $L=2\alpha$ and the displayed constant $b$,

\[
H_{\rm square}=-mVe^{u\xi}\alpha
|\bar D\xi+b\bar Du|^2,
\]

has precisely the IC-4 witness gradient jet. Both its difference from the
IC-4 gradient jet and all first variations vanish when the gradients vanish,
so this part of a correction leaves the flat homogeneous action unchanged.
The square is negative semidefinite; it must not be labeled a positive
Hamiltonian energy merely because its coefficient matrix has rank one.

A smooth interpolation that equals the original Hamiltonian near
$\pi=0$ and equals this square near the expanding witness can preserve both
branches' stated restrictions. One cannot additionally demand that the
same fixed-metric auxiliary symbol remain rank one everywhere while also
matching the generic original static symbol. A separate construction must
specify the interpolation, other Hamiltonian terms, and transition region,
and then derive preservation and the full coupled principal system anew.

## Reproducibility

Executed from the repository root with Python 3.9.6 and SymPy 1.14.0:

```text
python3 qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026/test_nonlinear_auxiliary_symbol.py
  TDD red: exit 1; nine intended assertion failures for the missing derivation.
  Implemented/final verification: exit 0; nine tests passed.
python3 qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026/nonlinear_auxiliary_symbol.py
  Exit 0; 21 computed exact residual groups vanish; input hashes match.
python3 qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026/nonlinear_auxiliary_symbol.py --require-full-nonlinear-closure
  Exit 2; same exact checks pass, requested full closure remains unresolved.
```

The tests and each CLI execution take approximately ten seconds on the
available machine. They are exact symbolic checks, not numerical parameter
sampling. The tests include independently hand-computed deviation controls
at $\mathcal T=9$ in the larger formal coefficient family, and the full
action-domain sign statements above are analytic inequalities.

The complete local executable import closure is `local_clock_wave.py`,
`quadratic_dirac.py`, and their shared `scalar_completion.py`. Those files
and `IC4_ACTION.md` are hash-pinned in the new program; its JSON prints the
actual hashes. `derive()` returns symbolic intermediate results; `run()`
returns JSON-safe results, computed residual checks, and explicit scope.
No bounded output is promoted to a full stability, matter-coupling,
causality, or nonlinear-constraint theorem.
