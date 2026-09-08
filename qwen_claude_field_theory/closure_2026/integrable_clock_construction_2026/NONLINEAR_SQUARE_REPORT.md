# Nonlinear construction checkpoint: one exact auxiliary square

Base `6708f1e3e`, 2026-09-08. **Full theory OPEN.**
The new [IC-5 action](IC5_ACTION.md) promotes the special-background
auxiliary-gradient cancellation to an exact identity on an open expanding
phase-space region. The result is a local functional invertibility lemma
under explicit bounds, not a global gravitational stability or causality proof.

## 1. What was constructed

The exact IC-4 Legendre transform is derived in
[NONLINEAR_HAMILTONIAN.md](NONLINEAR_HAMILTONIAN.md). Its auxiliary-gradient
matrix has a null direction at the witness but not at arbitrary nearby
independent phase points; [AUXILIARY_SYMBOL.md](AUXILIARY_SYMBOL.md) calculates
the precise coefficient condition. IC-5 implements that condition directly
in a complete smooth Hamiltonian, and supplies its covariant phase action.
This is a construction, not an inference from a finite list of failed models.

The new program computes the canonical/covariant density conversion,
stationary momentum elimination, static first-jet agreement, homogeneous
agreement, witness quadratic agreement, auxiliary mass matrix and the full
second-variation identity. Independent reviewers check the nonlinear
Hamiltonian and square compatibility from the original coefficients.
The construction changes cubic interactions; old nonlinear results would
not transfer merely because the quadratic action agrees.

## 2. Actual nonlinear auxiliary equations

Work on the activation plateau $|r^2-1|<1/4$. Use coordinates
$s=\xi+bu$, $t=u$; their Jacobian determinant is one. Fix the barred
canonical metric/momentum at a time. With the barred volume measure, write

\[
-H_5=\int dV_{\bar h}\,[\mathcal P(s,t)+A(s,t)|\bar Ds|^2],
\quad A=m\alpha e^{t(s-bt)}>0.
\]

$\mathcal P=-(\mathcal H_b+\mathcal D F\bar R)/V$ is explicitly defined
by the action, not a free potential. Its metric, curvature and momentum
arguments are held fixed in auxiliary variations. The vacuum/clock calculation
here does not silently include a nonexistent ordinary-matter model; any chosen
matter Hamiltonian contributes its actual auxiliary variations to $\mathcal P$.

The two secondary equations obtained by varying the Hamiltonian are

\[
\boxed{C_s=\mathcal P_s+A_s|\bar Ds|^2
-2\bar D_i(A\bar D^i s)=0,\qquad
C_t=\mathcal P_t+A_t|\bar Ds|^2=0.}
\]

Thus the second equation contains no derivative of $t$. The first is a
second-order equation for $s$ with coefficient $A>0$. Algebraic elimination
of $t$ still changes the reduced principal operator; it must not be ignored.

For variations $(v,w)=(\delta s,\delta t)$, the full Frechet operator is

\[
\begin{aligned}
L_{ss}v={}&[\mathcal P_{ss}+A_{ss}|Ds|^2-2D_i(A_sD^is)]v
-2D_i(AD^iv),\\
L_{st}w={}&[\mathcal P_{st}+A_{st}|Ds|^2]w-2D_i(A_tD^is\,w),\\
L_{ts}v={}&[\mathcal P_{ts}+A_{ts}|Ds|^2]v+2A_tD^isD_iv,\\
L_{tt}w={}&[\mathcal P_{tt}+A_{tt}|Ds|^2]w.
\end{aligned}
\]

All $D$ in this section are barred derivatives. In particular the two mixed
blocks are adjoints under the stated boundary conditions; they are not zero.
The accompanying two-jet computation differentiates the full density twice
and retains every mixed term.

## 3. A precise nonlinear coercivity lemma

**Domain.** A fixed smooth three-torus with a smooth positive-definite barred
metric; no boundary terms. Fields and metric/momentum coefficients are smooth
and remain strictly inside the plateau, $0<u<1$ and the regular metric
Legendre branch. On a bounded time interval require uniform bounds. No
claim here covers all of $\mathbb R^3$, an unbounded cosmological interval,
the transition region, or a vanishing Legendre denominator.

Let $q=(s,t)$, and suppose pointwise

\[
\mathcal P_{qq}\succeq c_0 I,\quad A\ge A_{\min}>0,\quad
\left(\|A_{qq}\|+\frac{4|A_q|^2}{A}\right)|Ds|^2\le c_0/2,
\qquad c_0>0,
\]

with all these coefficients bounded above as well. These are bounds on the
explicit candidate, not requirements inserted in place of varying it.
They hold at its witness and in a sufficiently small smooth coefficient
neighborhood. Indeed direct differentiation at **fixed canonical momentum**
gives, in the original $(\xi,u)$ coordinates,

\[
\frac{(-\mathcal H_5)_{qq}}{mVh_0^2e^{-1/2}}
=M_0=\begin{pmatrix}24&-27\\-27&2\mathcal T+135/8\end{pmatrix},\qquad
\det M_0=12(4\mathcal T-27)>0.
\]

Here $\mathcal T>27/4$ follows, for example, from $0<\ln(9/5)<4/5$.
Congruence by the coordinate Jacobian preserves this strict mass positivity;
at the witness $Ds=0$ and $A>0$. Crucially, the gradient part remains one
exact square off the witness. Positivity of the mass matrix alone would
not repair a sign-changing high-frequency principal eigenvalue.

**Proof.** For $W=(v,w)$ the exact second variation is

\[
B(W,W)=\int dV\,\{W^T[\mathcal P_{qq}+A_{qq}|Ds|^2]W
+4(A_q\cdot W)Ds\cdot Dv+2A|Dv|^2\}.
\]

Young's inequality bounds the magnitude of its cross term by
$A|Dv|^2+4|A_q|^2|Ds|^2|W|^2/A$. Therefore

\[
\boxed{B(W,W)\ge\frac{c_0}{2}\|W\|_{L^2}^2
+A_{\min}\|Dv\|_{L^2}^2.}
\]

This is coercivity on $\mathcal X=H^1_s\oplus L^2_t$, not on two copies
of $H^1$. Polarization and the coefficient bounds give a bounded symmetric
bilinear form on $\mathcal X$. Via its Hilbert Riesz map the represented
operator has closed range (the lower bound), and the orthogonal complement
of its range is its zero kernel (symmetry). Hence its range is all of
$\mathcal X$: the corresponding weak auxiliary operator is a bounded
isomorphism $L:\mathcal X\to\mathcal X^*$.

This last standard functional-analysis step is also expressed by Mathlib's
`IsCoercive.continuousLinearEquivOfBilin`: a bounded coercive real bilinear
form on a complete Hilbert space induces a continuous equivalence. The
required project-specific Hilbert space and coercivity estimate are supplied
above, not by that library theorem. [Mathlib documentation](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Analysis/InnerProductSpace/LaxMilgram.html).

At the exactly homogeneous witness the $k=0$ auxiliary block is the strictly
positive mass matrix. For $k\ne0$ it receives a nonnegative rank-one gradient
addition. Away from a constant background Fourier modes mix, and the energy
estimate—not a collection of sampled Fourier ranks—controls the operator.
This does not identify the full genuine homogeneous phase space with the
nonzero-mode phase space.

## 4. What this establishes for preservation, and what is missing

The unitary phase action has primary momenta $p_s=p_t=P_{\beta^i}=0$.
Their preservation yields $C_s,C_t$ and the spatial diffeomorphism
generators. For the unnormalized constraints $\delta(-H_5)/\delta q$, the
auxiliary Poisson matrix has the following **formal operator blocks**. The
inverse formula is valid only on a common domain supporting the displayed
compositions, not solely from the weak isomorphism in section 3:

\[
\mathbb D=\begin{pmatrix}0&-L\\L&\Omega\end{pmatrix},\qquad
\mathbb D^{-1}=\begin{pmatrix}L^{-1}\Omega L^{-1}&L^{-1}\\-L^{-1}&0\end{pmatrix}.
\]

In particular, boundedness/domain compatibility of $\Omega$ and
$L^{-1}\Omega L^{-1}$ is an additional obligation. Density/Riesz
identifications must be included when using the normalized
equations above. $\Omega$ is the actual metric-momentum bracket of the
secondary functionals, not an assumed zero. The general smeared variation
formula and an explicit nonzero off-shell homogeneous control are in
[NONLINEAR_HAMILTONIAN.md](NONLINEAR_HAMILTONIAN.md). The homogeneous control
transfers because that Hamiltonian restriction is identical; it does not
assert a nonzero bracket on the constraint surface.

The newly proved inverse removes the auxiliary kernel obstruction **on the
stated weak domain**. At a smooth constrained state, preservation would fix
the two auxiliary multipliers by $L\lambda=-\{C,H_5\}$ modulo spatial
transport, provided the drift belongs to the dual domain. Smooth finite jets
give such a weak source instantaneously on the torus. However, a complete
nonlinear result still needs the expanded IC-5 drift, its regularity under
the coupled metric evolution, and continued membership in the regular
plateau. No full nonlinear gravitational/matter DOF count is certified by
this partial functional result. Invertibility of an auxiliary equation is
not absence of an instantaneous **physical** channel.

## 5. A nonuniform numerical constraint witness

The finite-grid solve uses $m=h_0=V=1$, $\kappa=6$, the exact action's
$a_0,\Lambda$, $\bar h_{ij}=\delta_{ij}$, $\pi=-3e^{-1/2}$ and

\[
\bar\pi_{\rm TF}^{ij}
=\operatorname{diag}(\epsilon\cos z,-\epsilon\cos z,0),\qquad
\epsilon=0.035,\quad z\in[0,2\pi).
\]

Its spatial momentum constraint vanishes by direct differentiation. The
code varies a periodic edge-discretized energy, assembles its actual
gradient and Hessian, and solves for both auxiliary fields. It does not
feed the continuum equations an asserted solution.

At 16, 32 and 64 nodes, three Newton steps give residuals below
$1.2\times10^{-14}$; the smallest computed Hessian eigenvalue is greater
than $4.42$. The lapse-log field varies by approximately $0.00225$,
so these are not just repetitions of a homogeneous root. Changes on common
nodes decrease from $2.07\times10^{-8}$ to $5.37\times10^{-9}$ under
successive refinements. All computed $|r-1|<0.00375$, well inside the plateau.
These are finite numerical corroborations, not continuum existence,
time-evolution, stability or empirical proofs.

## 6. Verification and next physical gate

`nonlinear_square_completion.py` and its sixteen tests are executable;
`--require-full-closure` deliberately returns exit 2 after the partial checks.
The reproduction record supplies the actual commands, inputs, logs and exits.

Next: calculate and, if necessary, jointly balance the tensor kinetic and
curvature response away from the exact $F=0$ witness, without changing the
static, homogeneous or quadratic bridges. Then derive the full coupled
physical characteristics and multiplier drift. PPN and galactic matching
remain mandatory, not optional downstream polish.

**Same-turn follow-up:** [TENSOR_BALANCE.md](TENSOR_BALANCE.md) executes that
tensor calculation and constructs IC-6. Its explicit correction changes
only the nongradient auxiliary potential at fixed canonical metric/momentum.
The square is unchanged and its auxiliary mass matrix at the shear-free
witness is unchanged; smoothness holds where its new $J_T$ denominator stays
positive. The same local coercivity argument therefore applies in a
sufficiently small smooth neighborhood, with the bounds checked for the
new potential. IC-6's nonuniform numerical equations are solved separately.
The next missing calculation is the **coupled inhomogeneous physical
characteristic system and full multiplier drift**, not another repetition
of the homogeneous tensor check.

**Source record / Lean boundary.** The primary Mathlib generated documentation
above was read 2026-09-08: real complete Hilbert space, bounded coercive
bilinear form, continuous-equivalence conclusion. Its source link identifies
revision `9a1338a6a1a8eb784150b180bee61950c418eca9`; both source-file fetch
attempts failed, so only the displayed documentation was authenticated here.
No source cache was created, no Lean file was built, and no project-specific
Lean proof is claimed. The analytic argument above is independent of a
successful external source download.
