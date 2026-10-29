# Exact necessary conditions for two proposed shortcuts

Checkpoint OSC28; base `44fd23a71c9888d9ea204c0ee832805829f9c090`, with FD1 result `36b861cb74` added during the review. This is new route work. It does not amend the frozen lanes. The original theory is not completed.

## 1. A Burkert surface-density floor does not imply the exact galaxy law

Claim under review: Newtonian baryons plus a spherical Burkert halo at the adopted surface-density floor can reproduce the exact simple-mu galaxy law just by choosing the halo radius.

Assume a fixed baryonic acceleration magnitude `g_N>0`, aligned with the spherical halo force, and

\[
\rho_h(r)=\frac{\rho_0}{(1+x)(1+x^2)},\quad x=r/r_0,
\qquad \Sigma=\rho_0r_0=\frac{a_0}{2\pi G}.
\]

Direct mass integration, with exactly X43's convention, gives

\[
B(x)=2\ln(1+x)+\ln(1+x^2)-2\arctan x,
\quad M_h(r)=\pi\Sigma r_0^2B(x),
\quad \frac{g_h}{a_0}=q(x)=\frac{B(x)}{2x^2}.
\]

The amplitude of the halo acceleration is independent of `r0`. Its maximum is finite. A simple analytic bound suffices: writing `I(x)=B(x)/4`,

\[
\frac{d}{dx}\left(\frac{x^2}{6}-I(x)\right)
=\frac{x[(1-x)^2+x^3]}{3(1+x)(1+x^2)}>0.
\]

The bracket vanishes at zero, so `q(x)<1/3` for every positive `x`.

For the sharp bound put `H(x)=xB'(x)-2B(x)`. Then

\[
B'(x)=\frac{4x^2}{(1+x)(1+x^2)},\qquad
H'(x)=\frac{4x^2(1-x^2-2x^3)}{[(1+x)(1+x^2)]^2}.
\]

The numerator's final factor decreases strictly from 1 to minus infinity. Thus `H` first increases from zero and then decreases to minus infinity, crossing zero exactly once. This proves uniqueness of the maximum without extrapolating a finite grid. Its numerical location and value are

\[
x_{max}=0.9633982829983,\qquad q_{max}=0.2544835655694.
\]

The implemented simple-mu law instead demands

\[
\frac{g-g_N}{a_0}=h(y)=\frac{\sqrt{y^2+4y}-y}{2},\quad y=g_N/a_0.
\]

`h` increases from 0 to 1. Solving `h(y)=qmax` gives the necessary condition

\[
y\leq \frac{q_{max}^2}{1-q_{max}}=0.0868684876067.
\]

Therefore **no radius choice can make a halo exactly on this floor reproduce the simple-mu law at a point with `g_N/a0>0.08687`**, keeping the baryonic field fixed. The fully analytic conservative version already excludes `g_N/a0>=1/6`. At `g_N=a0`, the law gives `g/a0=1.618034`, while any such halo gives at most `1.254484`.

This is a scoped obstruction to identifying the core floor with the exact law. It does not contradict a fitted finite-radius SPARC RMS, where stellar masses are profiled. It does not apply to X43 halos above the floor, a different halo shape, extra force components, or a nonaligned geometry. The newer CL2/BS1 prescription explicitly puts some objects on a law branch, so this is not a refutation of that switch prescription either. It proves that its two branches cannot be identified by the floor alone.

The connection between Burkert surface density and bounded halo acceleration is established prior work: [Gentile et al. 2009, supplementary equations 3–5](https://arxiv.org/pdf/0909.5203v1). Their approximate core-radius maximum is not used in the exact differentiation above. No novelty claim is made.

## 2. IC 1613 now has a concrete conditional mass target

[Taibi et al., arXiv:2402.01631v2](https://arxiv.org/html/2402.01631v2), Table 1 and section 6.2, report `Re=1.50±0.02 kpc` and an inferred `vcirc(rhalf)=15±2 km/s`, using `rhalf=(4/3)Re` and inclination `32±11 degrees`. Their inference includes an asymmetric-drift prescription; the paper emphasizes the need for joint tracer modelling and limitations of a spherical dispersion-only estimator. These are published model-dependent estimates, not new measurements by this review.

Under the **spherical, isolated simple-mu law**, inversion is exact:

\[
g_N=\frac{g^2}{g+a_0},\qquad
M_{b,required}(<r)=\frac{v_c^4}{G(a_0+v_c^2/r)}.
\]

At `r=2 kpc`, `vc=15 km/s`, the required enclosed baryonic mass is **3.9224 million solar masses canonical / 3.2668 million alternative**. The rectangle formed by the quoted marginal `v=13–17 km/s` and `r=2±0.02667 kpc` spans **2.23–6.41 / 1.86–5.34 million solar masses**. This rectangle is not a joint confidence interval.

FD1's K-band mass, with its own half-stellar-mass convention, is **35.247 million solar masses inside the half-mass radius**, before adding gas. If that mass is retained at the new radius, the same law requires at least **26.47 / 27.68 km/s**; gas increases these minima. This conditional comparison is a useful target for the next resolved mass/kinematics analysis. It does **not** establish a significance or settle the theory: the luminosity-to-mass profile, tracer geometry, inclination, non-equilibrium motion and external-field treatment must be consistent in one model. The new radius is not silently substituted into FD1's frozen grading.

The decisive next check is therefore quantitative: determine whether a common tracer and baryon model can reconcile the enclosed mass and acceleration, with the candidate gravity model's field equation. Simply adding an outer HI rotation amplitude to a stellar-dispersion estimate is insufficient.

## Verification and disposition

`check_conditions.py` integrates the density independently, extracts only X43's pure `B` definition for a normalization comparison, locates the unique analytic critical point, checks the law inversion, and evaluates the stated source-input rectangle. **Eight checks pass**; the largest quadrature relative discrepancy is `1.62e-12` on five declared radii. A 500-point grid is a regression, not the proof of the universal cap. No historical pipeline was rerun.

The [run manifest](run/manifest.json) validates under computation-audit v2 with status `completed`; it records exact commands, versions and before/after input hashes. [SOURCES.json](SOURCES.json) pins the literature version and extracted numbers; no remote full-text hash is claimed. [run/result.json](run/result.json) contains the numerical outputs. Proof review is recorded separately in `REVIEW.md` when available.

Route disposition: exact floor-to-law shortcut refuted under the displayed hypotheses; realistic common-profile and dynamical-selection routes remain open. IC 1613 resolved inference is deferred to an actual joint tracer analysis; the present arithmetic is a necessary-condition diagnostic, not a catalogue repair or a new fitted model.
