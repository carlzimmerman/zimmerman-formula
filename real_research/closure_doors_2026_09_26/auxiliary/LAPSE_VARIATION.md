# Complete fixed-metric lapse variation of the weighted filter

**Continuum verdict: proved under the fixed-background hypotheses below.**
The proposed sign and weighted adjoint are correct. The lapse variation contains
a nonzero heat-operator term in addition to the measure and acceleration terms.
A separate 12-node weighted-graph calculation verifies its exact discrete
counterpart by central differences, a matrix-exponential Frechet derivative,
and Duhamel quadrature. This closes a particular first-variation calculation;
it does not supply the full metric/clock equations, constraint algebra, or
physical-time response.

## Claim, hypotheses, and conventions

Let the spatial leaf be smooth, closed, and connected, with fixed smooth
Riemannian metric h. Fix smooth positive N, a smooth real U, constants
alpha=a0/c^2>0 and b>=0, and a smooth real lapse direction n. Set

\[
N_\epsilon=N e^{\epsilon n},\quad
a=D\ln N,\quad L=\Delta_N=N^{-1}D_i(ND^i),\quad S=e^{bL},
\]
\[
E[N,U]=\int N\,dV_h\, e,\qquad
e=2|DU-a|^2+J(DSU).
\]

The derivative below holds U, h, alpha, b, and the leaf fixed. In particular,
there is no implicit lapse dependence of b or alpha in this calculation.
The divergence is div_N X=N^{-1}D_i(NX^i), and the inner product is
\(\langle f,g\rangle_N=\int N f g\,dV_h\).
L is self-adjoint in this weighted inner product and has nonpositive spectrum.

For the exact exponential kernel, define x>=0 by
\(|p|/\alpha=x(1-e^{-x})\). Then

\[
J(p)=2\alpha^2\big[2-2(1+x)e^{-x}-x^2e^{-2x}\big],
\qquad
j(p)=\nabla_pJ=4\alpha x e^{-x}\frac{p}{|p|}\quad(p\ne0),
\qquad j(0)=0.
\]

The inverse is unique because x(1-exp(-x)) is strictly increasing for x>0,
starts at zero, and tends to infinity. Near p=0,
\(J(p)=(8/3)\sqrt\alpha\,|p|^{3/2}+O(|p|^2)\), so J is C1 and j is continuous,
with \(|j|\le4\alpha/e\). No C2 Hessian at p=0 is assumed or needed.

## Derivation of the nonlocal lapse term

At epsilon=0, with delta=d/d epsilon,

\[
\delta N=Nn,\qquad \delta a=Dn,\qquad
\delta L f=-nLf+N^{-1}D_i(NnD^if)=Dn\cdot Df.
\]

Define \(w_s=e^{sL}U\). Differentiating its heat equation gives

\[
\partial_s(\delta w_s)=L\delta w_s+(\delta L)w_s,
\qquad \delta w_0=0,
\]

and hence the Duhamel expression

\[
\delta(SU)=\int_0^b e^{(b-s)L}(\delta L)w_s\,ds.
\]

This is a variation at the baseline N. Self-adjointness is used in the
baseline weighted inner product; its measure variation has already been
included separately in the term n e below.
Writing j=j(DSU), weighted integration by parts gives

\[
\begin{aligned}
\delta E
&=\int N\,dV_h\,[n e-4(DU-a)\cdot Dn+j\cdot D\delta(SU)]\\
&=\int N\,dV_h\,[n e-4(DU-a)\cdot Dn]
 +\int_0^b\langle -\operatorname{div}_N j,
 e^{(b-s)L}(\delta L)w_s\rangle_N\,ds.
\end{aligned}
\]

Set

\[
r_s=e^{(b-s)L}(-\operatorname{div}_N j),\qquad
Q=\int_0^b r_s Dw_s\,ds.
\]

Moving the baseline heat operator to the adjoint factor and using
\(\delta L w_s=Dn\cdot Dw_s\) yields the complete first variation

\[
\boxed{\displaystyle
\delta E=\int N\,dV_h\left[n e+
\left(-4(DU-a)+Q\right)\cdot Dn\right].}
\]

Thus, in the weak sense,

\[
\boxed{\displaystyle
F=e+4\operatorname{div}_N(DU-a)-\operatorname{div}_N Q,
\qquad \delta E=\int N n F\,dV_h=\int\delta N F\,dV_h.}
\]

Functional-derivative normalization matters: when the reference measure is
dV_h, \(\delta E/\delta N=F\), while
\(N^{-1}\delta E/\delta(\ln N)=F\). Calling F simply an "N derivative divided
by N" would be ambiguous without defining that derivative.

At a zero of DSU, j remains continuous, but div_N j need not be a classical
function. The equations above then use its distributional divergence. For
b>0, r_s is smoothed for s<b; pairing the Duhamel formula with j is an
unambiguous weak definition including the endpoint s=b. More concretely,
j is in L2, so div_N j is in H^-1; heat smoothing gives an integrable
O((b-s)^(-1/2)) L2 bound near that endpoint. Smooth U has bounded Dw_s,
so Q is well-defined as an L2 flux. At b=0, Q=0 directly. Therefore the
C1 join creates no additional delta-function term in this first variation.
No boundary terms occur because the leaf is closed.

## Exact graph counterpart and independent check

The finite test is a periodic oriented cycle with 12 nodes. Let dx=2pi/12,
\((Du)_i=(u_{i+1}-u_i)/dx\), and \((Pu)_i=(u_i+u_{i+1})/2\).
For ell=ln N, use diagonal node and edge weights

\[
M=dx\,\operatorname{diag}(e^{\ell}),\qquad
W=dx\,\operatorname{diag}(e^{P\ell}),\qquad
L=-M^{-1}D^TWD,\qquad S=e^{bL}.
\]

The graph energy uses edge quadrature:
\(E_g=\sum_e W_e[2(DU-D\ell)_e^2+J((DSU)_e)]\).
Varying ell by n differentiates **both** M and W:

\[
\delta L=-\operatorname{diag}(n)L
-M^{-1}D^TW\operatorname{diag}(Pn)D.
\]

This exact graph formula is used, rather than imposing a continuum Leibniz
identity on a finite incidence matrix. Its heat term is

\[
\delta E_{g,\mathrm{heat}}=
\int_0^b r_s^TM(\delta L)w_s\,ds,
\qquad r_s=e^{(b-s)L}M^{-1}D^TWj,
\]
\[
=\int_0^b\left[-\sum_iM_i n_i r_{s,i}(Lw_s)_i
-\sum_eW_e(Pn)_e(Dr_s)_e(Dw_s)_e\right]ds.
\]

The direct terms are
\(\sum_eW_e[(Pn)_e e_e-4(DU-D\ell)_e(Dn)_e]\).
This is a discretization-specific identity. No continuum convergence theorem
is inferred from one graph.

The declared inputs are b=.11, alpha=.8 and, at the node positions x,

\[
\ell=.8\cos x+.25\sin2x,\quad
U=1.7\sin(x+.2)+.5\cos(3x-.1),\quad
n=.4\sin(x-.7)+.55\cos(2x+.1)+.15.
\]

The constitutive inverse uses 64 bisections. A degree-12 small-x series avoids
cancellation only for x<.001. Duhamel uses 32-point Gauss-Legendre quadrature;
the independent matrix derivative uses scipy.linalg.expm_frechet; the energy
central differences rebuild all weights, L, S, and the constitutive inverse.

All **16 checks passed** in the bounded run:

| Quantity | Value |
|---|---:|
| Direct lapse derivative | -4.763189212200195 |
| Heat-operator derivative | -0.17815580930612956 |
| Complete analytic graph derivative | -4.941345021506325 |
| Central difference, step 1e-5 | -4.941345021691745 |
| Absolute derivative error | 1.8542e-10 |
| Duhamel/Frechet full-matrix difference | 4.1633e-17 |
| Duhamel/Frechet energy difference | 5.5511e-17 |
| Error after freezing the filter | 0.1781558093 |
| Error after omitting its node-mass vertex | 0.3766050634 |

Central-difference errors decrease by a factor 100.00075 when the step changes
from .01 to .001, as expected for a second-order difference. Controls also
check weighted self-adjointness, L1=delta L1=0, constant lapse rescaling,
b=0, U=0 at the C1 join, and the one-sided small-gradient asymptotic.

## Reproduction and scope

The run pins repository HEAD
`763086b2345085e93f35628b4d59abe69a5a7da3` with a dirty worktree. Concurrent
external work had advanced the parent task's initial base; this task did not
commit or merge anything. The source and contract are new files and their
hashes are recorded in `lapse_run1/manifest.json`.
Python 3.9.6, NumPy 1.26.2, SciPy 1.11.4; runtime 0.439891 s; 60 s wall cap,
45 s CPU cap, one cooperative numerical-library thread. The manifest validator
reported a valid evidence record with current source and output hashes.

The exact recorded command and regeneration command are in the manifest. To
reproduce with a **new** result directory, run the computation-audit bounded
runner using `lapse_contract.json`, input `lapse_variation.py`, and this child
command:

```text
python3 real_research/closure_doors_2026_09_26/auxiliary/lapse_variation.py --output NEW_RUN_DIRECTORY/results.json
```

The continuum first-variation identity follows from the displayed heat
equation, weighted integration by parts, and C1 kernel. The graph results
independently test signs and omitted terms in a specified finite binary64
surrogate. They establish neither the full lapse equation of an unspecified
gravity action nor a constraint/DOF count, physical causality, or empirical
equivalence after replacing the original geometric filter. If U is eliminated
at its stationary value, its implicit variation contributes no first-order
term; the modified gravitational and clock sectors still must be varied.
