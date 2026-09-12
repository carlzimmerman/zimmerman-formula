# Physical clock-gradient variance from the frozen action

Claim and verdict: on a regular homogeneous FLRW background of the frozen
action, the first nonzero coefficient of its physical clock-frame gradient
is

\[
Y^{[2]}=a^{-2}\left|\nabla\left(\sigma-\frac q{\bar s}\pi\right)\right|^2,
\qquad \pi=\delta\tau.
\]

This formula is proved by the projector expansion below and independently
checked with exact symbolic arithmetic. The proposed universal scalar law
\(\dot{\mathcal Y}=f(t,\mathcal Y)\) is refuted for the full regular
six-state *linear* solution family, under the nondegeneracy assumptions in
the explicit witness below. This is a statement about the exact evolution
of the leading variance coefficient. Asymptotic attraction, finite-amplitude
closure, the MOND kernel and its cosmological normalization remain open.

The calculation uses `mathbox:computation-audit` to distinguish the finite
symbolic checks from the argument they support and `mathbox:proof-audit`
to check the physical definition, admissible witness and quantifier scope.
No action coefficient is reconstructed and no particle species is added.

## Frozen definitions and expansion convention

The source action is

\[
S=\int d^4x\sqrt{-g}\left[\frac{M^2}{2}(R-2\Lambda)
 +P(X,\tau)-V(\tau)+sW(Y,\tau)+\gamma X\Box\chi\right]+S_m,
\]
\[
s^2=-g^{\mu\nu}\tau_\mu\tau_\nu>0,\quad
n_\mu=-\tau_\mu/s,\quad Q=n^\mu\chi_\mu,\quad
X=-g^{\mu\nu}\chi_\mu\chi_\nu=Q^2-Y.
\]

The frozen matter sector contains minimally coupled irrotational dust and
radiation with kinetic density \(C_rX_r^2\). Its homogeneous radiation field
rate is \(q_r\), and its background dust density is \(\rho_b>0\).

Use signature \(-+++\), background proper time \(t\), \(a>0\),
\(\bar s=\dot{\bar\tau}>0\), \(q=\dot{\bar\chi}\), and
\(\chi=\bar\chi+\epsilon\sigma+O(\epsilon^2)\),
\(\tau=\bar\tau+\epsilon\pi+O(\epsilon^2)\).
The notation \(Y^{[2]}\) denotes the coefficient of \(\epsilon^2\),
not a second derivative without its factorial.

The authoritative source paths are
`../../cosmological_bridge_2026/derive.py`,
`../../cosmological_bridge_2026/transfer_evolve.py`, and
`../../nonlinear_evolution_2026/constitutive.py`, relative to this file.
The parent task supplied baseline revision `48ab93de3` (PAPER20).
The canonical bounded runner subsequently recorded actual revision
`08281ae2582ef39f853ad85405f3c56cb25dcc37` with a dirty worktree. Its
read-only revision/status capture is the only Git access in this subtask;
no Git mutation occurred. The frozen source bytes remained unchanged across
the run and their hashes agree with the initial symbolic read.

## The projector, including a perturbed clock

Introduce the projected covector

\[
r_\mu=(\delta_\mu{}^\nu+n_\mu n^\nu)\chi_\nu
       =\chi_\mu-\frac Qs\tau_\mu,
\qquad Y=g^{\mu\nu}r_\mu r_\nu.
\]

On the homogeneous background \(r_\mu^{[0]}=0\). For arbitrary first-order
lapse, shift and spatial metric perturbations,

\[
\delta Q=\dot\sigma-q\alpha,\qquad
\delta s=\dot\pi-\bar s\alpha,
\qquad
\delta(Q/s)=\frac{\dot\sigma}{\bar s}
             -\frac{q\dot\pi}{\bar s^2}.
\]

The first-order projected covector is therefore

\[
r_0^{[1]}=0,\qquad
r_i^{[1]}=\partial_i\sigma-\frac q{\bar s}\partial_i\pi.
\]

Since its background vanishes, the quadratic coefficient of its norm uses
only the background inverse metric. Neither first- nor second-order metric
perturbations, nor second-order field perturbations, enter \(Y^{[2]}\).
This proves the displayed formula. Under the linear time gauge change
\(\sigma\mapsto\sigma-qT\), \(\pi\mapsto\pi-\bar sT\), the combination
\(\sigma-q\pi/\bar s\) is invariant. The coefficients \(q/\bar s\)
are homogeneous, so their spatial derivatives vanish.

An independent check begins directly with

\[
Y=g^{\mu\nu}\chi_\mu\chi_\nu
 +\frac{(g^{\mu\nu}\tau_\mu\chi_\nu)^2}
             {-g^{\mu\nu}\tau_\mu\tau_\nu}.
\]

`derive_geometry.py` expands this rational expression through order two,
retaining all ten arbitrary symmetric metric coefficients at each order
and all four field-gradient coefficients at each order. Its numerator's
zeroth and first coefficients vanish, and its quadratic coefficient is the
same expression. This independently checks the cancellation of metric
and second-order field terms.

In unitary clock gauge \(\pi=0\), the exact ADM inverse metric gives
\(Y=h^{ij}\partial_i\chi\partial_j\chi\), independently of lapse and
shift, since the clock normal is the hypersurface normal. Expanding this
exact identity again gives \(Y^{[2]}=a^{-2}|\nabla\sigma|^2\).

For the original `derive.py` representative \(\sigma(t)\cos(kx)\),

\[
Y^{[2]}(t,x)=p_k\sigma(t)^2\sin^2(kx),\qquad
\langle Y^{[2]}\rangle_x=\tfrac12p_k\sigma(t)^2,
\quad p_k=k^2/a^2.
\]

Thus the expression \(p_k\sigma^2\) refers to a mode with unit mean-square
normalization, or to a power-spectrum normalization with its weights
included. The local cosine expression and its period average must not be
identified. The script compares the independent result to the original
action's `projected_gradient` export.

## The action-to-state map and exact leading variance transport

The frozen action's scalar clock constraint is

\[
2qP_{X\tau}v-W\delta K-2qW_Yp_k\sigma=0,
\qquad v=\delta Q=\dot\sigma-q\alpha.
\]

For \(W\ne0\), it gives \(\delta K=Fv+G\sigma\), with
\(F=2qP_{X\tau}/W\) and \(G=-2qW_Yp_k/W\). The six reduced coordinates are

\[
u=(\sigma,v,r,v_r,\theta,\delta_b)^T,
\quad v_r=\dot r-q_r\alpha,\quad \delta_b=\delta\rho_b.
\]

The action-derived lapse reconstruction is \(\alpha=\ell(t,k)u\), hence

\[
\dot u=\mathsf A(t,k)u,\qquad
\mathsf A_{0j}=\delta_{1j}+q\ell_j.
\]

This identifies the physical observable's row of the actual transfer
system. The checks also compare the clock constraint and density
reconstruction directly with the unrestricted action in `derive.py`.
They do not substitute a separately chosen oscillator for this map.

For unit mean-square spatial modes, or Fourier modes with the appropriate
fixed nonnegative weights \(w_k\), let
\(C_{ij}(t,k)=\mathbb E[u_i(t,k)u_j(t,k)^*]\). The expectation can instead
be a deterministic quadratic product, and may be an uncentered second
moment; no zero-mean assumption is needed for the formula. Then

\[
\mathcal Y(t)=\sum_k w_kp_k C_{00}(t,k),\qquad
\dot C=\mathsf AC+C\mathsf A^\dagger,
\]
\[
\boxed{\dot{\mathcal Y}=-2H\mathcal Y
 +2\sum_k w_kp_k\operatorname{Re}
 \left[C_{10}+q\sum_{j=0}^5\ell_j C_{j0}\right].}
\]

These are exact equalities within the linear six-state system for its
quadratic observable. For smooth perturbative solutions of the full
theory, \(\langle Y\rangle=\epsilon^2\mathcal Y+O(\epsilon^3)\),
subject to the existence of that perturbative solution expansion.
At this order a normalized physical-volume average on a fixed comoving
periodic cell equals the background spatial average: perturbed volume
weights multiply an already quadratic scalar. The physical clock-normal
derivative also reduces to the background proper-time derivative at this
order. A changing smoothing window would add derivatives of its weights;
that is outside this fixed-window statement.

The frozen constitutive \(W\) is smooth near \(Y=0\). Since \(Y\) starts
at order two, the action term \(W_{YY}Y^2/2\) starts at order four.
Consequently linear transport by itself does not probe the full response
of \(W\) at finite gradient variance.

## Admissible correlation witnesses against a scalar law

To avoid confusing the scalar kinetic coefficient with \(\mathsf A\),
call it \(A_c\). In `transfer_evolve.py` the four constrained unknowns
\((\dot v,\dot v_r,\dot\delta_b,\alpha)\) obey a matrix equation with

\[
\mathsf M=\begin{pmatrix}
A_c&0&0&D\\0&R&0&-\dot j_r\\0&0&1&-\dot\rho_b\\E&0&0&L
\end{pmatrix},\quad
\Delta=A_cL-ED,\quad \det\mathsf M=R\Delta,
\]
\[
\begin{split}
A_c&=B-12\gamma Hq-2\gamma q^2F,&B&=2P_X+4q^2P_{XX},\\
D&=qC_c-\dot j,&C_c&=-2\gamma q^2G-2\gamma qp_k,\\
E&=F+3\gamma q^2/M^2,&
L&=qG-3\dot H+p_k-3V_p/(2M^2),\\
V_p&=\bar sW+2\gamma q^2\dot q.&
\end{split}
\]

Here \(j=2qP_X-6\gamma Hq^2\), \(j_r=4C_rq_r^3\), and
\(R=12C_rq_r^2\); all constitutive jets are evaluated on the frozen
homogeneous background \(X=q^2,Y=0\).

The source column multiplying \(\delta_b\) is
\((0,0,3H,1/(2M^2))^T\), and the solve is \(\mathsf Mz=-Su\).
Inverting only its coupled first and fourth rows yields

\[
\ell_5=-\frac{A_c}{2M^2\Delta},\qquad
\mathsf A_{05}=-\frac{qA_c}{2M^2\Delta}.
\]

Assume \(M^2>0\), \(a,\bar s>0\), \(k>0\), \(W\ne0\),
\(R\ne0\), \(\Delta\ne0\), and \(qA_c\ne0\). At one common time
choose any nonzero real \(x,r_b\) and the two reduced initial states

\[
u_+=xe_0+r_be_5,\qquad u_-=xe_0-r_be_5.
\]

Both have the same \(\mathcal Y=p_kx^2\). Nevertheless,

\[
\dot{\mathcal Y}_+-\dot{\mathcal Y}_-
 =4p_kxr_b\mathsf A_{05}
 =-\frac{2p_kxr_bqA_c}{M^2\Delta}\ne0.
\]

Their diagonal powers are identical; only the \(\sigma\)-density
correlation changes sign. Equivalently take the positive semidefinite
rank-one covariances \(C_\pm=u_\pm u_\pm^T\). A random overall sign with
equal probabilities realizes each as a zero-mean ensemble. The two states
can instead be realized as same-wave-number cosine perturbations with
relative density phase zero or \(\pi\); the unnormalized cosine convention
multiplies both variance derivatives by \(1/2\).

The coordinates are admissible within the regular reduced system: lapse,
curvature and shift are reconstructed from the action constraints, rather
than independently assigned. Explicitly, in spatial gauge \(e=0\),

\[
z=\frac{\delta\rho_{\rm tot}-2M^2H\delta K}{2M^2p_k},\qquad
b=-\frac{\delta K+3J/(2M^2)}k,
\]
\[
J=j\sigma+2\gamma q^2v+j_rr+\rho_b\theta,
\quad\delta\rho_{\rm tot}=R_vv+R_\sigma\sigma+12C_rq_r^3v_r+\delta_b.
\]

The density coefficients are
\(R_v=qB-18\gamma Hq^2-2\gamma q^3F\) and
\(R_\sigma=-2\gamma q^3G-2\gamma q^2p_k\).

The action-derived background and constraint reduction ensure the remaining
linear equations are propagated on this branch. Their numerical residuals
are checked by the companion evolution calculation, which is a separate
evidence artifact. All perturbations can be multiplied by a common
sufficiently small amplitude. For a positive background dust density this
keeps the total dust density positive and stays in the local open
constitutive and timelike-clock domains. Existence of arbitrary nonlinear
continuations is not supplied by the linear argument.

If a single-valued \(f(t,\mathcal Y)\) held for every member of this
linear solution family, the same time and variance would give the same
derivative, contradicting this witness. More generally, for one real mode
with all six coordinates freely admissible, exact scalar closure requires
\(\mathsf A_{0j}=0\) for every \(j>0\). If those five coefficients vanish,
the one-mode law is
\(\dot{\mathcal Y}=2(\mathsf A_{00}-H)\mathcal Y\). For multiple
independently populated wave numbers this rate must also be the same at
each wave number if only their summed variance is retained.

This proof does not cover exceptional singular reductions, \(k=0\), or
restricted initial-condition manifolds. An approximate attracting relation
among the missing correlations remains possible. Establishing one needs
a dynamical convergence argument in a stated basin and time regime.

## Evidence obligations and reproducibility

| Obligation | Status | Evidence or limit |
|---|---|---|
| Observable is the action's physical projection | Passed | Covariant contraction, projected covector and exact ADM calculations agree |
| Perturbed-clock gauge invariance | Passed | \(\sigma-q\pi/\bar s\) invariant under the displayed time change |
| Fourier normalization | Passed | Local cosine and half-weight period average checked separately |
| Physical observable reaches the frozen state system | Passed | Frozen action gradient, clock equation, density and velocity maps checked |
| Variance identity | Passed | Exact covariance transport and direct rank-one state derivative agree |
| Witness is in the stated linear domain | Passed under regularity assumptions | Six unconstrained coordinates; auxiliary metric fields reconstructed |
| Frozen background meets nonzero witness coefficients | Separate numerical evidence | Companion evolution task |
| All nonlinear states or late-time attractors excluded | Out of scope | No such conclusion follows |

Run from the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s qwen_claude_field_theory/closure_2026/clock_response_repair_2026/variance_closure_2026/geometry -p 'test_*.py' -v
PYTHONDONTWRITEBYTECODE=1 python3 qwen_claude_field_theory/closure_2026/clock_response_repair_2026/variance_closure_2026/geometry/derive_geometry.py --result-file qwen_claude_field_theory/closure_2026/clock_response_repair_2026/variance_closure_2026/geometry/result.json
```

All symbolic identities use exact rational expressions, with no random
sampling or numerical integration. The test's single rational matrix fixture
checks signs and normalization only; it is explicitly not a claimed
physical background sample. Source hashes, actual Python/SymPy versions,
elapsed time and command arguments are in `run_001/result.json`, the canonical
result. `run_001/manifest.json` records before/after hashes, the command,
resource limits and successful exit, and passed validation against the
repository root. The earlier `result.json` is an exploratory result predating
the combined-test CLI. Exact recorded commands and the deliberate negative
controls are in `COMMANDS.md`.
