# What the outer heat filter actually repairs at a zero

This route follows the externally amended target at commit `9092fc0fd`:
filtered QUMOND with `nu_mono`, with well-posedness still required under causal
criterion B. The result is constructive but deliberately narrower than a
coupled gravity evolution theorem.

On a fixed flat periodic leaf, let

\[
F=\frac{h_{\rm mono}(|S\nabla u|/a_0)}{|S\nabla u|/a_0}\,S\nabla u,
\qquad a_{\rm ph}=-S P_LF,
\quad S=e^{(\xi^2/2)\Delta},\quad\xi>0.
\]

Here P_L is the longitudinal Fourier projector (zero mode set to zero), and
the continuous extension at a vanishing inner gradient is F=0. Take normalized
L2 on a torus of side 2pi and Fourier lattice k in Z^3. The projector has norm
at most one. Cauchy–Schwarz, applied to the matrix Fourier series, gives

\[
\|D a_{\rm ph}\|_{L^\infty}
\leq \left(\sum_{k\ne0}|k|^2e^{-\xi^2|k|^2}\right)^{1/2}\|F\|_{L^2}.
\]

The sum is finite for every positive xi, independently of whether the inner
acceleration vanishes. All higher spatial derivatives have similar Gaussian
moment bounds. Thus **the physical filtered force is spatially Lipschitz at
MOND zeros** when F is square-integrable. The argument does not differentiate
the constitutive square root at its zero. For a fixed source this supplies
unique test-particle trajectories; a time-dependent source additionally needs
measurability in time and locally time-integrable force and Lipschitz bounds.
Add the ordinary Newtonian force with its own spatial regularity assumptions.

Periodic Poisson inversion uses the mean-zero source perturbation: the
sinusoidal input below corresponds to a cosine density perturbation about a
uniform background. Its zero Fourier mode is excluded consistently. A
sufficiently positive background makes the total matter density positive;
the example is not an isolated positive-mass solution of a periodic Poisson
equation with an unremoved nonzero mean.

With the standard Fourier normalization on R3, the corresponding bound is

\[
\|D a_{\rm ph}\|_\infty
\leq\frac{\sqrt3}{4\pi^{3/4}\xi^{5/2}}\|F\|_2.
\]

That R3 statement assumes F in L2. An isolated MOND 1/r tail is not globally
L2 in three dimensions, so the torus result cannot simply be relabeled as an
isolated-source result. Weighted/local estimates would be a separate task.

## What it does not repair

For a small source amplitude epsilon, the inner phantom satisfies
F_epsilon/sqrt(epsilon) -> F_0 of nonzero norm in the displayed example.
For the actual input grad(u_epsilon)=epsilon sin(x1)e1 and a0=1,
F_0=exp(-xi^2/4)sgn(sin x1)sqrt(|sin x1|)e1. This field is zero-mean and
longitudinal, so P_L F_0=F_0 and S F_0 is nonzero. Heat smoothing is linear,
so this output also scales as sqrt(epsilon).
Consequently source-to-force Lipschitz continuity still fails at the zero
source. Smooth dependence on **position** and smooth dependence on **source
data** are different assertions. Coupled lapse/metric variations, constraint
preservation, the clock's principal block and the mixed Cauchy problem remain
open. There is no estimate uniform as xi -> 0.

## Checks and formalization

`check.py` tests an exact below-peak RAR/nu_mono phantom on an embedded
one-dimensional periodic source at 512, 1024, 2048, 4096 and 8192 points for
three positive filter widths. It computes norms of +S P_L F; changing to the
physical minus sign leaves every reported norm and bound unchanged. The
finite Fourier bound applies exactly to that trigonometric interpolant;
refinement is numerical evidence for its continuum approximation, not a
rigorous interpolation-error certificate. The unfiltered spectral derivative
grows with refinement while the filtered derivative converges. A separate
four-amplitude control retains the square-root source dependence.

The accepted `run1` records 15 refinement cases, four source cases and the
exact three-dimensional Gaussian integral. `PushFilter20260926.lean` compiles
three scoped theorems: finite-mode Cauchy–Schwarz, its heat-weight specialization
and the square-root-versus-linear inequality. The continuum Fourier/ODE
arguments above are analytic proofs, not Lean-certified PDE theorems.
