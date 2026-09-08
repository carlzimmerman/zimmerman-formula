# IC-2: a uniform finite bound through the negative-frequency band

2026-09-08. Base checkpoint: `179aae2392de1aa65fad08115d446d7d542e3c73`.

The same IC-2 action has a positive constructive result beyond late-time
indicial roots: **every solution of the reduced scalar equation that starts
in the negative-frequency band has a uniform finite future amplification
bound**. In the norm defined below, the exact upper factor is approximately
4.2354211. Deterministic numerical transfer matrices give a largest sampled
factor of about 2.3624018. The latter is not claimed to be the sharp uniform
bound.

This does not remove the negative instantaneous frequency, establish
observational acceptability, or prove physical causality or nonlinear closure.
It applies to the exact expanding witness and its genuine-clock scalar mode;
additional ordinary-matter perturbations are not included.

## Inputs and normalization

The computation imports the frozen [scalar action calculation](scalar_completion.py),
SHA256 `801e50f8a3485842eec9bafd58d4f652c42200050917da6d9f0360aea5ff7745`,
and checks that hash. It does not replace the action-derived coefficients
with a guessed oscillator. [SCALAR_REPORT.md](SCALAR_REPORT.md) fixes the
action and normalization.

Write

\[
d=8\mathcal T=-\frac{27}{2}+\frac{432}{5\ln(9/5)},\qquad
\tau=h(t-t_0),\qquad p=\frac{dz}{d\tau}=\frac{\dot z}{h},
\qquad x(\tau)=x_0e^{-2\tau}.
\]

Here $h=\dot B/B>0$, and $x=(k_{\rm physical}/H_{\rm physical})^2$.
For each fixed comoving $k>0$, the imported action gives

\[
z'=p,\qquad p'=-\beta(x)p+c(x)z,
\]
\[
a(x)=3\frac{d+x-54}{d+x},\qquad
\beta=3-2x\frac{a_x}{a}
      =3-\frac{108x}{(d+x)(d+x-54)},
\]
\[
c=\frac ga
=\frac{2x[d(d-27)-(d+81)x-2x^2]}
       {9(d+x)(d+x-54)}.
\]

Primes on $z,p$ denote $d/d\tau$; the subscript $x$ denotes an $x$
derivative. The factor in the damping numerator is **108**, not 324: the
common factor 3 cancels in $a_x/a$. A preliminary hand calculation used
324; the retained computation derives and independently tests 108 from $a$.
No executed numerical conclusion uses the preliminary expression.

The numerator polynomial $q(x)=d(d-27)-(d+81)x-2x^2$ decreases strictly
for $x\ge0$, starts positive, and has the single positive zero

\[
x_*=-\frac{d+81}{4}+\frac34\sqrt{d^2-6d+729}
\simeq46.2937226611.
\]

Thus $c\ge0$ on the whole future trajectory whenever $0<x_0\le x_*$.
Also $q(d)=-2d^2-108d<0$, so $x_*<d$.

## Uniform theorem and proof

For arbitrary real or complex initial amplitudes define the genuine norm

\[
W(\tau)=|z(\tau)|+\frac12|p(\tau)|,\qquad W_0=W(0).
\]

There is no division by $z$, $p$, or a component that may cross zero.
The zero initial vector gives the zero solution. Define

\[
\Gamma(x)=-\frac d{18}\ln\!\left(1+\frac xd\right)
 +\frac{4d-189}{18}\ln\!\left(1+\frac{x}{d-54}\right)-\frac x9,
\qquad C_*=e^{\Gamma(x_*)}.
\]

Then for all $0<x_0\le x_*$ and all $\tau\ge0$,

\[
\boxed{W(\tau)\le
 e^{\Gamma(x_0)-\Gamma(x(\tau))}W_0\le C_*W_0.}
\]

The value $C_*\simeq4.2354210613$ is a numerical evaluation of the exact
expression, not an interval-certified decimal.

To prove the bound, first $\ln(9/5)<4/5$: the function

\[
F(y)=y-\ln(1+y),\qquad F(0)=0,\qquad F'(y)=\frac y{1+y}>0
\]

gives this inequality at $y=4/5$. Therefore $d>189/2>243/4$. The exact
identity

\[
(d+x)(d+x-54)(\beta-2)
=(x+d-81)^2+108\left(d-\frac{243}{4}\right)>0
\]

shows that $\beta>2$ on $x\ge0$. Absolute continuity, or upper Dini
derivatives at zeros of the components, now gives

\[
D^+W\le |p|+\frac12[-\beta|p|+c|z|]
\le\frac c2 W.
\]

Direct integration of the rational expression gives

\[
\Gamma_x=\frac{c(x)}{4x},\qquad\Gamma(0)=0.
\]

Multiplying the differential inequality by its integrating factor and using

\[
\int_0^\tau\frac{c(x(s))}{2}\,ds
=\Gamma(x_0)-\Gamma(x(\tau))
\]

proves the first bound. Since $\Gamma_x\ge0$ on the band, the second bound
follows. This is an all-future-time inequality, not a finite grid extrapolation.

## Convergence and physical scalar observables

The exact rational force obeys

\[
0\le c(x)\le\rho x,\qquad
\rho=\frac{2(d-27)}{9(d-54)},\qquad 0\le x\le x_*.
\]

For example, its positive numerator decreases and its positive denominator
increases relative to their $x=0$ values; the computation also checks the
coefficientwise positive expression for $\rho-c/x$. Variation of constants,

\[
|p(\tau)|\le e^{-2\tau}
 \left[|p_0|+\rho x_0 C_*W_0\tau\right],
\]

then proves convergence of $z$ and the explicit tail bound

\[
|z_\infty-z(\tau)|\le e^{-2\tau}
\left[\frac{|p_0|}{2}
 +\rho x_0 C_*W_0\left(\frac\tau2+\frac14\right)\right].
\]

The lapse and auxiliary fields are reconstructed from the same eliminated
equations, not treated as independent oscillator amplitudes:

\[
v=\frac{36p-4xz}{d+x},\qquad
n=\frac{d+x+27}{2(d+x)}p-\frac{3x}{2(d+x)}z,
\]
\[
\zeta_{\rm physical}=z-\frac n3+\frac v4
=\frac{2d+x}{2(d+x)}z-\frac{d+x-27}{6(d+x)}p.
\]

Both $n$ and $v$ decay by the preceding bounds. Moreover,

\[
|n|\le\left(1+\frac{27}{d}\right)W,\quad
|v|\le\max\!\left\{\frac{4x_*}{d+x_*},\frac{72}{d}\right\}W,
\quad |\zeta_{\rm physical}|\le W.
\]

These are dual-norm bounds on the displayed linear functionals. The first
uses $x_*<d$; no ratios through nodes are involved.

The physical intrinsic scalar curvature of the genuine-clock slices is
recomputed using the pinned Christoffel-derived Ricci tensor and the physical
scale $A=B e^{-1/12}$, rather than the barred scale. Its Fourier amplitude is

\[
\frac{\delta R^{(3)}_T}{H_{\rm physical}^2}=4x\zeta_{\rm physical},\qquad
\left|\frac{\delta R^{(3)}_T}{H_{\rm physical}^2}\right|
\le4x_0e^{-2\tau}C_*W_0.
\]

This is a physical scalar: the clock-defined intrinsic curvature has zero
background value. Similarly $n=\delta\ln N(X)$ and $v=\delta u$ perturb
background-constant scalars. The claim is not a computation of the
four-dimensional Ricci scalar, Weyl tensor, or their retarded support.

## Deterministic numerical corroboration

The script solves the $2\times2$ fundamental matrix with identity initial
data. Its reported amplification is the induced weighted 1-norm

\[
\|S\mathcal F(\tau)S^{-1}\|_1,\qquad S=\operatorname{diag}(1,1/2).
\]

It does not select one favorable initial vector. Eight deterministic cases
use $x_0/x_*\in\{10^{-8},10^{-4},0.01,0.1,0.25,0.5,0.75,1\}$,
with $0\le\tau\le20$ and 801 sample times. DOP853 is rerun with
relative/absolute tolerances $10^{-9}/10^{-11}$ and $10^{-12}/10^{-14}$,
and maximum steps 0.25 and 0.125, respectively.

The retained run found:

- Maximum sampled weighted transfer norm: 2.3624017887.
- Maximum matrix difference under refinement: $1.10\times10^{-9}$.
- Maximum excess above the analytic time-dependent envelope: 0 at the
  sampled points; the initial equality is included.
- Maximum early Wronskian error: $8.06\times10^{-13}$.

The independent Wronskian control is

\[
\det\mathcal F(\tau)=e^{-3\tau}\frac{a(x_0)}{a(x(\tau))}.
\]

It is checked only up to $\tau=4$, avoiding misleading relative errors
when the two late-time columns become nearly proportional. The $x_0=0$
test is a closed-form control of the *limiting nonzero-mode ODE*, not an
identification with IC-1's genuinely homogeneous constraint system.

Unit initial vectors normalize a linear transfer matrix. Their numerical
amplitudes are not claimed to be small physical perturbations: the homogeneous
linear solutions can be rescaled to any sufficiently small initial norm.
No nonlinear remainder estimate follows from that rescaling.

## Reproduction and remaining gap

From the repository root:

```sh
python3 qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026/test_ir_growth.py
python3 qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026/ir_growth.py
python3 qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026/ir_growth.py --require-full-closure
```

Executed statuses: 9 tests passed (exit 0, about 3.1 seconds); default main
exit 0; full-closure requirement exit 2. The source hash matches the frozen
input. Exact symbolic checks, numerical tolerance checks, software versions,
and individual transfer matrices are regenerated in the JSON output.
BLAS/OpenMP thread limits are set to one cooperatively; OS CPU affinity is
not claimed. Tests were written first and observed failing before their
implementation; the stable numerical logarithm formula has its own exact
derivative and origin controls.

The result closes a specific gap left by an indicial-root argument: the
linear reduced scalar cannot accumulate unbounded amplification while it
redshifts through this band. It does **not** assert absence of negative
instantaneous frequency, full scalar health on other backgrounds, causal
support, nonlinear stability, realistic ordinary-matter cosmology, or a fit
to observations. Those remain separate obligations of the same action.
