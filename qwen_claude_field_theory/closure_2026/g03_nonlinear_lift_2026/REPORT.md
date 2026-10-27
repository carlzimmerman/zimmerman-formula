# C-H: unique nonlinear auxiliaries, singular response, and a nonuniform limit

2026-09-05. **Full theory OPEN. Regular quadratic auxiliary lift obstructed.**

This continues the same Gaussian C-H action, not Fable's different
dynamical-scalar construction. It identifies why the previous dust-like
quadratic mode is insufficient as a nonlinear health certificate:

1. The exact spatial auxiliary equation has a unique small-lapse solution.
2. That solution cannot have a bounded H1 coefficient U/epsilon2 as epsilon
   tends to zero along a nonzero cosine lapse direction.
3. The reduced energy has an explicit nonanalytic cubic correction anyway.
4. A direct trial sequence disproves extending the preceding fixed-direction
   quadratic limit uniformly in the H1 norm to arbitrarily short wavelengths.

These are mathematical statements about this action and specified function
spaces. They are not a proof of a ghost, absence of exact nonlinear spacetime
solutions, or the nonexistence of relativistic MOND. No priority claim is made.

## 1. Exact action, variation and conventions

Use the fields and constants of `../g03_covariant_action_2026/ACTION.md`.
On a flat compact leaf, after eliminating the exact heat extension, the
auxiliary functional per spatial volume is

\[
F_N[U]=\left\langle N\left[2|DU-a|^2+
2\alpha^2q(|D S U|^2/\alpha^2)\right]\right\rangle,
\quad a=D\ln N,\quad S=e^{\xi^2\Delta/2}.
\tag{1}
\]

Here alpha=a0/c2>0, xi>0, and U is fixed modulo its spatial constant.
Numerics use alpha=1, period 2pi and spatial averages; x and xi are expressed
in the same chosen length unit. The overall positive gravitational-action
prefactor is suppressed. The original exponential kernel is unchanged:

\[
s=y(1-e^{-y}),\quad q(s^2)=2-2(1+y)e^{-y}-y^2e^{-2y},
\quad f(p)=\bigl(\nu(|p|/\alpha)-1\bigr)p.
\]

The code differentiates this primitive and computes
\(q(s^2)\sim(4/3)s^{3/2}\) and
\(f(\varepsilon^2p)/\varepsilon\to
f_0(p)=\sqrt\alpha\,\operatorname{sgn}(p)\sqrt{|p|}\)
for epsilon down to zero. In the vector case replace sign(p) by p/|p|.
The value at p=0 is zero. No finite constitutive tangent is assigned there.

For periodic variations eta the full first variation is

\[
\delta F=4\langle N(DU-a)\cdot D\eta+
N f(D S U)\cdot D S\eta\rangle.
\tag{2}
\]

In one dimension D and S commute, and stationarity therefore gives

\[
\boxed{N(U'-a)+S[N f(SU')]=C,}
\tag{3}
\]

where C is a spatial constant. The lapse weight is inside the outer heat
operator: replacing S[Nf] by N S[f] changes the varied action. The exact
nonlinear numerical gradient and an independent FFT flux residual retain it.

## 2. Exact small-lapse solutions do exist uniquely

The mean-fixed squared-gradient term is coercive in H1. The nonnegative q
term is continuous under weak H1 convergence on bounded sets because
positive-time heat smoothing is compact into continuous gradients. The
direct method thus gives a minimizer for every smooth positive N on the
fixed compact leaf.

Uniqueness at small lapse contrast is also controlled. Put
\(\lambda(y)=ds/dy=1+(y-1)e^{-y}\). Its derivative is
\((2-y)e^{-y}\), so its maximum on y>=0 is \(1+e^{-2}\) at y=2.
The radial eigenvalue of the exact flux derivative is

\[
\frac{df}{dp}=\frac1{\lambda(y)}-1
\ge-\frac1{1+e^2}=-\kappa_*.
\]

The transverse eigenvalues are nonnegative. The bound holds in the
semiconvex sense across zero, where the positive tangent diverges. Heat
contraction in L2 therefore bounds the second variation from below by

\[
4\bigl(N_{\min}-\kappa_*N_{\max}\bigr)\|D\eta\|_2^2.
\tag{4}
\]

For \(N=e^{\varepsilon\cos x}\), this is strictly positive whenever
\(|\varepsilon|<\tfrac12\log(1+e^2)\). The functional is then strongly
convex modulo constants, and the minimizer is the unique stationary
auxiliary. This establishes an exact spatial solution, not time evolution
of the full metric/clock system.

## 3. No bounded quadratic auxiliary lift

Fix xi>0, let epsilon decrease to zero, and take
\(\ln N_\varepsilon=\varepsilon\cos x\). Suppose a stationary sequence
satisfied \(\|U_\varepsilon\|_{H^1}=O(\varepsilon^2)\).
After fixing means, weak compactness and compact heat smoothing give a
subsequence \(U_\varepsilon/\varepsilon^2\rightharpoonup V\) in H1 and
\(S(U_\varepsilon'/\varepsilon^2)\to SV'\) uniformly. Dividing (3) by
epsilon gives the necessary limit

\[
S f_0(SV')=-\sin x+c.
\]

Heat injectivity, with A=exp(xi2/2), then requires

\[
SV'=\frac{(c-A\sin x)|c-A\sin x|}{\alpha}.
\]

The left side has zero mean. The integral of the right side is strictly
increasing in c and vanishes at c=0, so c=0 without imposing reflection
symmetry on U. Hence

\[
\boxed{SV'=-\frac{e^{\xi^2}}{\alpha}\sin x|\sin x|.}
\tag{5}
\]

The right side is C1 but not C2 at the zeros of sin x; the second derivative
of sin x|sin x| jumps by four at x=0. The left side is smooth (indeed
analytic) for every H1 V. This contradiction rules out the entire bounded
sequence, not merely a guessed convergent series. Thus the unique small-lapse
solutions satisfy \(\|U_\varepsilon\|_{H^1}/\varepsilon^2\to\infty\).
The previous result \(DU_\varepsilon=o(\varepsilon)\) remains valid.

This also obstructs a C2 family in all fields, including U in mean-fixed H1:
its first-order U coefficient must vanish, since division of the auxiliary
equation by sqrt(epsilon) and testing that coefficient gives
\(\langle|D S U_1|^{3/2}\rangle=0\). Its quadratic coefficient would then
have to satisfy (5). This does not exclude smooth metric/clock dependence
accompanied by a less regular auxiliary dependence. Even at xi=0, signed
amplitudes generally involve epsilon|epsilon|; the identity-filter control
is a one-sided H1 range check, not a two-sided C2 certificate.

The leading argument survives a fixed smooth uniformly elliptic family
\(h_\varepsilon=h_0+O(\varepsilon)\) with flat h0 and
\(\ln N_\varepsilon=\varepsilon\cos x+O(\varepsilon^2)\).
Positive-time heat maps vary continuously in smoothing norms, so these
corrections vanish in the scaled weak equation.

Nor is auxiliary plane symmetry a necessary assumption on flat T3. For
arbitrary U(x,y,z), write W=SV and
\(b=D S^{-1}\cos x=-A\sin x\,e_x\). The limit equation is the weak
divergence equation for \(f_0(DW)-b\). Trigonometric polynomials lie in
the heat range, providing dense test functions. The explicit W* with
gradient given by (5) solves it. Strict monotonicity of f0, tested against
W-W*, forces DW=DW*. The same lack of smoothness contradicts heat smoothing.

## 4. Spectral obstruction and the filter-order threshold

An independent exact calculation yields

\[
\sin x|\sin x|=\sum_{n\ge1}b_n\sin(nx),\qquad
b_n=\begin{cases}8/[\pi n(4-n^2)]&n\text{ odd},\\0&n\text{ even}.
\end{cases}
\]

For the putative Gaussian lift,

\[
\langle|V'|^2\rangle=
\frac{e^{2\xi^2}}{2\alpha^2}\sum_{n\ {
\rm odd}}e^{\xi^2n^2}b_n^2=\infty\quad(\xi>0).
\tag{6}
\]

The formula proves divergence; the finite computation only checks its
implementation. Log-domain sums avoid overflow and do not invert quadrature
noise. With xi=0 the sum instead equals 3/(8 alpha2), a negative control.

For comparison only, let a positive even filter have gains
\(m_n\asymp |n|^{-r}\), m0=1. Equation (5) uses \(e^{\xi^2}=m_1^{-2}\),
so \(V'_n\asymp n^{r-3}\) along odd n. Therefore the leading auxiliary
equation has a mean-fixed H1 solution exactly when

\[
\boxed{r<\frac52.}
\tag{7}
\]

The endpoint diverges logarithmically. A single Helmholtz filter (r=2)
passes this necessary range test; Gaussian smoothing fails it. This does
not validate a replacement action, its nonlinear branch or its physics.
The underlying issue is the combination of the deep-MOND cusp with the
filter's smoothing strength, not the exponential interpolation's full shape.

## 5. A cubic reduced energy without a regular auxiliary expansion

For the plane-periodic minimum define F0=F_N[0] using averages. Despite (6),

\[
\boxed{\inf_UF_N[U]=F_0-
\frac{16}{9\pi\alpha}e^{3\xi^2/2}|\varepsilon|^3
+o(|\varepsilon|^3),\qquad F_0=\varepsilon^2+O(\varepsilon^4).}
\tag{8}
\]

Proof of the coefficient, not just a numerical fit: from s<=y2,

\[
q(s^2)=2\int_0^s[y(t)-t]dt\ge\frac43s^{3/2}-s^2.
\]

For the true minima the prior quadratic theorem gives v=U'=o(epsilon)
in L2 and \(\langle|Sv|^{3/2}\rangle=o(\varepsilon^2)\). Expanding only
the square in (1), \(F_{\min}\le F_0\), q>=0 and v=o(epsilon) also give
\(\langle q(|Sv|^2/\alpha^2)\rangle=o(\varepsilon^2)\).
Expanding only
the lapse weights, their contribution to F-F0 is o(epsilon3): the cross
error is \(O(\varepsilon^2\|v\|_2)\), the squared-gradient error is
\(O(\varepsilon\|v\|_2^2)\), and the q error is O(epsilon) times its o(epsilon2)
integral. Transfer only the single sinusoid through the inverse heat
operator; **do not apply inverse heat to the full exponential lapse**.
With p=Sv, heat contraction gives

\[
F-F_0\ge 2(\|v\|_2^2-\|p\|_2^2)
-4\varepsilon\langle(-A\sin x)p\rangle
+\frac83\sqrt\alpha\langle|p|^{3/2}\rangle+o(\varepsilon^3).
\]

The first term is nonnegative. Pointwise minimization of the other terms
gives \(p=-\varepsilon^2 A^2\sin x|\sin x|/\alpha\) and the lower
coefficient in (8), since \(\langle|\sin x|^3\rangle=4/(3\pi)\).
For the upper bound, use fixed trials U=epsilon2 V. Their cubic functional
is
\(J[V]=-4\langle V'(-\sin x)\rangle+
(8/3)\sqrt\alpha\langle|SV'|^{3/2}\rangle\).
Approximate the relaxed minimizing p by zero-mean trigonometric polynomials,
each in the heat image; their J values approach the lower coefficient.
Take the amplitude limit first for each trial, then the polynomial limit.
Translation x -> x+pi proves the signed |epsilon|3 form.

The infimum of this leading J is not attained in the H1 heat-image class.
It is essential to distinguish fixed-mode minima J_M from their continuum
limit. This is a reduced-action equation, not a new empirical law.

## 6. Explicit failure of a uniform quadratic limit

Let k be a positive integer tending to infinity on the same torus, and
keep alpha and xi fixed. Choose

\[
\nu_k=\ln N_k=\varepsilon_k\cos(kx),\qquad
\varepsilon_k=\frac\alpha k e^{-\xi^2k^2},\qquad U_{\rm trial}=\nu_k.
\]

The square in (1) vanishes exactly. Put t=xi k. Then

\[
F_{\rm trial}=2\alpha^2\langle e^{\nu_k}
q(e^{-3t^2}\sin^2kx)\rangle,\quad
F_0=2\alpha^2e^{-2t^2}\langle e^{\nu_k}\sin^2kx\rangle.
\]

The exact small-field q asymptotic, uniform in the phase, proves

\[
0\le\frac{\inf_UF_{N_k}[U]}{F_0}
\le\frac{F_{\rm trial}}{F_0}
\sim\frac83\langle|\sin x|^{3/2}\rangle e^{-t^2/4}\to0.
\tag{9}
\]

No stationary property of the trial is assumed. In contrast, holding k
fixed and taking epsilon to zero gives inf F/F0 -> 1 by the prior theorem.
The two limits cannot be interchanged uniformly.

More precisely, the fixed-direction candidate quadratic term in the lapse
logarithm is \(Q(\nu)=2\|D\nu\|_2^2\). In one dimension the functional is defined on
H1 lapses (which are continuous). Along the smooth sequence above,

\[
\frac{\inf_UF_{N_k}[U]-Q(\nu_k)}{\|\nu_k\|_{H^1}^2}\to-2.
\]

This rules out that second-order Frechet expansion in H1. In three
dimensions the same smooth plane-periodic sequence refutes the proposed
uniform H1 estimate; no unsupported open-domain H1(T3) differentiability
claim is needed. The sequence tends to zero in every fixed Cm seminorm,
but the normalization here is H1, not every stronger topology.
Consequently the preceding fixed-direction scalar action is still correct
in its stated scope, but is not a uniform continuum perturbation theory.

## 7. Computation, checks and limits

`nonlinear_lift.py` uses the existing cancellation-resistant exact q kernel.
It varies the nonlinear weighted functional in preconditioned Fourier
coordinates; an independent FFT computes the weighted flux residual.
The derivative/finite-difference relative error is 2.48e-11.
The bounded 32-mode, 2048-node results include:

| xi | epsilon | (F-F0)/epsilon3 | RMS(U'/epsilon2) |
|---|---:|---:|---:|
| 0.2 | 1e-2 | -0.59837330 | 0.651990 |
| 0.2 | 1e-8 | -0.60087575 | 2.294880 |
| 0.5 | 1e-2 | -0.81176927 | 0.971813 |
| 0.5 | 1e-6 | -0.82325617 | 3.793566 |
| 0.5 | 1e-8 | -0.82329486 | 15.203686 |

The largest projected normalized flux residual in these runs is 2.36e-9.
Mode/quadrature refinements are stored, not inferred from a residual.
At xi=.5, the independently minimized leading cubic values for
M=4,8,16,32 are -0.82199604, -0.82329052, -0.82335306, -0.82335650;
the exact relaxed limit is -0.82335671. Fixed-M amplitude convergence
is checked against J_M, not falsely against its continuum limit.
Optimizer flags and messages are retained separately from numerical
residual acceptance. No finite stationary solve is promoted to a continuum
global-minimizer certificate; that existence result has its own proof above.

The exact trials in (9) use xi=.5, k=4,8,12,16,20 and 4096 phase nodes.
They test an energy upper bound, not a solved evolution. All numerical
choices, coefficients and raw rows are in results.json; the manifest hashes
code, theory inputs and this report. No ranks, degrees of freedom, PPN
parameters or expected determinants are assigned by this study.

## 8. Reproduction and interpretation

Created only this directory's CONTRACT.md, nonlinear_lift.py,
test_nonlinear_lift.py, REPORT.md, results.json and computation_manifest.json.
No existing action or other contributor's files were changed. No commit or
push was made. HEAD was 129311b8e when this study started, with a dirty tree.

Commands from the repository root:

```sh
git status --short
git log -3 --oneline
OPENBLAS_NUM_THREADS=1 python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/g03_nonlinear_lift_2026 -v
OPENBLAS_NUM_THREADS=1 python3 -B qwen_claude_field_theory/closure_2026/g03_nonlinear_lift_2026/nonlinear_lift.py
```

The unit suite passes 11/11 (exit0); the producer passes 13 diagnostic
groups (exit0). `--require-closed`, exercised in a private output directory
by the tests, exits2 because full theory closure is not established.
Tests were written first and failed before implementation. Additional
finite-mode, convexity and joint-limit assertions likewise failed before
their implementations. No mathematical test failure was hidden or converted
into a physics PASS.

Existing regressions were rerun afterward. The FLRW suite uses temporary
CLI outputs. The three older suites were copied with their two required
`hunt_2026` source dependencies into a private fixture because their CLI
tests otherwise overwrite live evidence. GIT_DIR and GIT_WORK_TREE pointed
to the original repository for read-only provenance queries. Exact test
commands, with the same `OPENBLAS_NUM_THREADS=1` prefix, were:

```sh
python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/g03_flrw_scalar_2026 -v
# 10/10, exit0
python3 -B -m unittest discover -s /private/tmp/ch-lift-regression-FwOdUO/qwen_claude_field_theory/closure_2026/smoothed_onset_action_2026 -v
# 10/10, exit0
python3 -B -m unittest discover -s /private/tmp/ch-lift-regression-FwOdUO/qwen_claude_field_theory/closure_2026/two_body_frequency_2026 -v
# 9/9, exit0
python3 -B -m unittest discover -s /private/tmp/ch-lift-regression-FwOdUO/qwen_claude_field_theory/closure_2026/filtered_tidal_relation_2026 -v
# 6/6, exit0
```

Including the new suite, 46 unit tests pass. Independent read-only checks
rederived the cusp coefficients, integration-constant argument, cubic
coefficient and joint-limit countersequence. A separate code review
independently ran the 11 tests and producer, and refined selected quadrature
to 8192 nodes. Its label/provenance suggestions were applied: the reported
norm is explicitly that of log N, and the manifest lists supporting
finite-mode and gradient-check settings as well as the main sweep.
A final independent proof review found no critical or important gap in the
existence, range-obstruction, cubic-coefficient or H1-countersequence claims.
Mathematical self-proofreading covered this report; squared L2 norms were
made explicit, with no change of conclusions. The remaining physical gaps
are the ones stated below.

**Research state:** the Gaussian action is obstructed as a regular
second-order auxiliary response and as a uniform H1 quadratic approximation.
It is not proven DEAD as a nonlinear classical theory, and is not CLOSED.
The original general-source exact AQUAL requirement also remains unmet by
this screened construction. The clock interpretation does not change that.
Neither a primordial origin nor its cosmological abundance has been derived;
no dark-matter particle is postulated in this auxiliary calculation.

**Next unavoidable calculation:** establish or refute well-posed full
metric/clock evolution after eliminating the unique but nonsmoothly
responding auxiliary, in an explicitly stated function space. An answer
must control the high-frequency countersequence in (9). Returning to the
same fixed-direction quadratic mode count cannot settle that question.
