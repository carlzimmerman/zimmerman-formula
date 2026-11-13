# CP02: static gate and external-field matching

This lane derives and executes the coupled static equations. It does **not** justify replacing only the quadratic dust source by that source times a gate. The force equation changes at the same time.

The main new obstruction is conditional but sharp: an unchanged AQUAL external-field solution cannot remain an approximately unchanged solution through the flat gate's return to its cosmological value at astrophysical radius. Moving the transition outward worsens the force-equation residual. This rules out the proposed *unchanged-law, quiet exterior switch* construction. It does not rule out a substantially deformed outer state, compensated reservoir, time-dependent solution, or another action.

The mass/force tests and finite-box solves below are canonical-footing calculations, not a fit to measured galaxies. They do not replace the independent GR constraint and transport lanes.

## 1. Inputs and scope

The authoritative starting action is QX17, with only

\[
H(Q,\Pi)=\frac{\mu_K^2}{2K}(Q-1)^2 S(\Pi/\Pi_c),\quad
S(u)=e^{-u^3},\quad K=4\pi G,
\]

replacing the quadratic clock term. The polarization potential and stiffness remain

\[
W=\frac{a^2}{K}[-p-\log(1-p)],\quad
p=K|P|/a<1,\quad
\gamma=K L_*^2/2,\quad \Gamma=\gamma\Pi_+^2/2.
\]

Here `a=a0/c²`, and the dimensionless gravitational potential is `phi=Phi_phys/c²`. Source hashes are in `source_hashes.json` and in each v2 execution manifest. Historical files were not edited.

The parent phase was assigned at HEAD `2207a1df48348f01ca1084d4add5d214c55d0e7e`; actual executions observed HEAD `cace4617bb6a518bf910b56a4c0ee8bddce7fa07`, dirty. The pinned source hashes are unchanged across the executed checks. No inference depends on silently assuming a clean checkout.

The literal flat gate is suppressing only on `Pi>=0`: it grows exponentially on negative Pi. External-field configurations have signed polarization-divergence lobes. Replacing it by `exp[-(max(u,0))³]` avoids that growth and is C² at zero, but defines a different gate. All positive-Pi transition results below apply to either choice; spherical numerical acceptance requires positive Pi.

## 2. The actual static equations

In a static unitary chart, `Q sqrt(-g)=sqrt(gamma_spatial)`, so Pi is independent of the lapse. The clock contribution to the normal energy density is therefore `Q H_Q-H`; the Pi derivative cannot be discarded from the polarization equation. At leading Newtonian order, and with the background clock offset negligible compared with the galaxy potential,

\[
\nabla^2\phi=K\rho_b+K\Pi-\mu_K^2\phi S,
\qquad
\nabla\phi+\gamma\nabla\Pi_+-\nabla H_\Pi=W_P.
\]

The full leaf equation, before this Newtonian truncation, is

\[
(1+\gamma\Pi_+-H_\Pi)A+\gamma D\Pi_+-D H_\Pi=W_P.
\]

Thus `K P=(1-mu) grad(phi)` is no longer available as an unchanged constitutive identity. Substituting it into Poisson while keeping a nonconstant gate is generally inconsistent.

Define

\[
r_M=\sqrt{GM_b/a_0},\quad \epsilon=a r_M,\quad
x=r/r_M,\quad \phi=\epsilon f,\quad y=f',
\]
\[
p=K P/a,\quad Z=p'+2p/x=K\Pi r_M/a,\quad
d=K\Pi_c r_M/a,\quad m=\mu_K r_M,\quad \ell=L_*/r_M.
\]

Primes below denote x derivatives, except `S'` and `S''`, which denote derivatives with respect to u. Let `b(x)=4 pi r_M³ rho_b/M_b`. On the positive-Pi branch the radial action, up to an overall constant, is

\[
\mathcal I=\int x^2\left[-\frac{y^2}{2}+py-w(p)
+\frac{m^2f^2}{2}S(Z/d)-\frac{\ell^2 Z^2}{4}-bf\right]dx,
\quad w=-p-\log(1-p).
\]

Direct variation gives

\[
f'=y,\quad
 y'=b+Z-m^2 fS-2y/x,\quad
 p'=Z-2p/x,
\]
\[
B=\frac{\ell^2 Z}{2}-\frac{m^2f^2}{2d}S'(Z/d),\qquad
y+B'=\frac{p}{1-p}.
\]

Equivalently,

\[
\left[\frac{\ell^2}{2}-\frac{m^2f^2}{2d^2}S''\right]Z'
=\frac{p}{1-p}-y+\frac{m^2fy}{d}S'. \tag{1}
\]

The full constitutive correction to this display is `(1+epsilon B)y+B'=p/(1-p)`. Its absence from the Newtonian action is an ordering assumption, not an exact identity. Comparisons in a regime with large coefficients are consistency tests of the desired reference field; they do not certify that the truncated equations describe a new large-correction state.

The exact symbolic Euler–Lagrange residuals in `run03/results.json` are both zero. Deleting the gate gradient fails the symbolic check. Independent finite differences verify the explicit gate-gradient expression to a maximum relative discrepancy `6.63e-9` in the nine stated test cases.

### Critical surfaces and the static correlation

For the flat gate,

\[
S'=-3u^2e^{-u^3},\qquad
S''=(9u^4-6u)e^{-u^3}.
\]

If gamma is zero, the coefficient of `Z'` changes sign at `u=(2/3)^(1/3)`. Nonzero gamma moves the critical surfaces. A smooth crossing of a zero coefficient in (1) requires its right side to vanish there.

On the unchanged AQUAL relation `y=p/(1-p)`, with a negative well `f<0`, positive outward force `y>0`, and `S'<0`, that right side is strictly positive. Hence an unchanged AQUAL field cannot cross the critical surface smoothly. A deformed field can change the first two terms; this argument does not establish nonexistence of all static solutions.

The Q–Pi correlation is therefore included, rather than replaced by an unrestricted Hessian argument. The explicit transition substitution below also shows that the ordinary reference correlation does not keep the gate's curvature small.

## 3. The small-value test misses the derivative

For a point baryon mass, the exact simple-mu dust-free reference has

\[
s=\sqrt{1+4x^2},\quad y=\frac{1+s}{2x^2},\quad
p=\frac{2}{1+s},\quad Z=\frac{2}{xs},
\]
\[
f=\operatorname{asinh}(2x)-\frac{1+s}{2x}-\operatorname{asinh}(120).
\]

It is matched at `R=60` to `f(R)=-R y(R)`. This is an imposed finite-box potential, not a dynamically derived cap. The identities `y=p/(1-p)` and `div(y-p)=0` are checked symbolically.

For this reference,

\[
G\equiv H_\Pi=\epsilon\frac{m^2 f^2}{2d}S',
\qquad
\frac{G_x}{\epsilon}=\frac{m^2}{d}
\left[fyS'+\frac{f^2}{2d}S''Z'\right].
\]

Set the outer gate value to `S_R=(1/mu_K)^2`, with mu_K measured in Mpc^-1, the historical local effective-mass ceiling of 1/Mpc. This is only a sufficient pointwise ceiling on the reference dust source. Over the tested `1<=x<=60`:

| baryon mass | mu_K / Mpc^-1 | max abs(G) | max abs(grad G)/g |
|---|---:|---:|---:|
| 1e9 Msun | 25120 | 6.50e-9 | 18.99 |
| 1e10 Msun | 25120 | 2.06e-7 | 189.94 |
| 1e11 Msun | 25120 | 6.50e-6 | 1899.36 |
| 1e12 Msun | 25120 | 2.06e-4 | 18993.64 |
| 1e11 Msun | 198.25 | 3.39e-6 | 493.13 |

Every listed `abs(G)` passes 1e-3, while every listed derivative fails. These numbers expose the earlier consistency error in a dimensionally explicit way.

There remains an inner-box suppression choice: for `Mb=1e11,mu_K=25120`, lowering the historical `xi=Pi_c/rho_d0` from the mass-only ceiling `13.2919` to about `10.9862` gives the sampled derivative boundary 1e-3, at `u_R=3.29842`. Thus the derivative correction alone is **not** a galaxy-only parameter-space no-go. Very small Pi_c can suppress both corrections inside a selected finite observed box. It moves the unavoidable return to `S(0)=1` farther out.

## 4. The transition cannot preserve the external-field law

This section is a consistency test of the unchanged external-field reference, with hypotheses stated explicitly. It is not a solution of a deformed transition layer.

Let the external field point along z and define

\[
x_e=g_e/a_0,\quad \mu_e=\frac{x_e}{1+x_e},\quad
L_e=\frac{1}{1+x_e}.
\]

Where the internal field is small compared with the approximately uniform external field, the ordinary linearized AQUAL potential of a compact baryon source is

\[
\phi_h=-\frac{A}{\sqrt{(1+L_e)(X^2+Y^2)+z^2}},
\qquad A=\frac{GM_b}{\mu_e c^2}.
\]

Along either symmetry pole, at radial distance r,

\[
\phi_h=-A/r,\quad g_h=A/r^2,\quad K\Pi=\eta A/r^3,
\qquad \eta=2L_e>0.
\]

This last identity follows by taking the ordinary three-dimensional Laplacian of the displayed anisotropic potential. It uses the positive-Pi poles, so clamping the gate in negative-Pi lobes does not remove the result.

First ignore the linear external contribution to the clock potential and use `Q-1=A/r`. At the gate transition `u=1`, with radius r_t,

\[
\boxed{\frac{|\partial_r H_\Pi|}{g_h}
=\frac{3}{2e\eta}(\mu_K r_t)^2}, \tag{2}
\]
\[
\frac{H_Q}{\Pi}=\frac{(\mu_K r_t)^2}{e\eta},\qquad
\frac{H_{\Pi\Pi}}{\gamma}
=\frac{3}{e\eta^2}(\mu_K r_t)^2(r_t/L_*)^2. \tag{3}
\]

Equation (2) is checked exactly by symbolic differentiation. With the recorded `x_e=0.0131841657`, the coefficient is `0.279547...`. Requiring its value to remain below 1e-3 puts a formal transition radius below `301.69 pc` for mu_K=198.25 or `2.381 pc` for mu_K=25120. For most galaxies those radii are themselves outside the deep-EFE assumptions: the point is that there is no perturbatively unchanged deep-EFE transition at an astrophysical outer radius, not that the formula is valid down to parsec scales.

At 1 Mpc, the reference values for mu_K=25120 are

- `abs(grad G)/g_h=1.76398e8`;
- `H_Q/Pi=1.17599e8`;
- `H_PiPi/gamma=3.69264e17` for Lstar=22 pc.

Whether 1 Mpc is actually deep EFE depends on baryon mass; the numerical output reports that ratio rather than assuming it.

### Including the external clock gradient and an arbitrary clock offset

A globally static uniform external potential is not an asymptotically flat spacetime. The calculation can only be a local external-field patch. Even there, using only the internal potential in H needs justification. The following stronger two-pole test includes the leading external gradient and any constant clock offset.

At the two poles, write

\[
Q-1=X_0\pm a_e r+A/r,\qquad a_e=g_e/c^2.
\]

At r_t define

\[
a=X_0r_t/A,\quad b=a_e r_t^2/A=g_e/g_h,\quad
T=\frac{3(\mu_Kr_t)^2}{2e\eta}.
\]

The signed radial gate-gradient ratios are

\[
\frac{\partial_r H_{\Pi,\pm}}{g_h}
=-T(a\pm b+1)(3a\pm5b+1).
\]

Their mean divided by `-T` is

\[
3(a+2/3)^2+5b^2-1/3.
\]

Consequently, whenever `b>=1/sqrt(15)`,

\[
\boxed{\max_\pm\frac{|\partial_r H_{\Pi,\pm}|}{g_h}
\ge T(5b^2-1/3).} \tag{4}
\]

The polynomial identity is checked exactly. No single choice of the additive clock offset can cancel the correction on both poles in the deep external-field regime. Relative to the external acceleration, divide the bound by b.

For `Mb=1e11 Msun,r_t=3 Mpc`, `b=10.3666`, so this example is in the stated small-internal-field regime. The lower bound relative to the **total-field scale** g_e is `5.12224e6` for mu_K=198.25 and `8.22381e10` for mu_K=25120. Both are far above the frozen 1e-3 constitutive tolerance. Finite Lstar=22 pc gives a stiffness-gradient correction only of order `(Lstar/r_t)^2`; it cannot cancel this residual while the reference field is maintained. The covariant multiplicative term G A is suppressed relative to the natural radial gate-gradient scale by the weak potential `a_e r_t`; it does not rescue this perturbative construction.

A strongly deformed transition may avoid the reference assumptions. Establishing its existence, mass inventory, observations and health requires a different calculation. Equations (2)-(4) forbid declaring an unmodified EFE truncation a solution merely by suppressing a dust source.

## 5. The ungated exterior has a short static response scale

If Pi tends to zero, the flat gate tends back to one with zero first and second derivatives. Around a locally frozen clock background q, the clock density perturbation contains

\[
\delta\rho_H=-q^2\mu_K^2\delta\phi/K+\text{higher-order terms}.
\]

A stationary nonzero Kepler perturbation `delta_phi=-A/r` cannot then be an asymptotic solution with finite nonzero Gauss excess mass: the displayed source is order 1/r, while Laplacians and regular polarization responses are order 1/r³ or smaller. Gate corrections vanish still faster. This is a static asymptotic statement. A compensated cosmological halo can have zero net excess mass at infinity, so absence of a nonzero Kepler asymptote is not by itself absence of a halo.

With zero stiffness and frozen external coefficients, the exterior equation is

\[
\mu_e[\partial_X^2+\partial_Y^2+(1+L_e)\partial_z^2]\delta\phi
+\mu_K^2\delta\phi=0.
\]

After the anisotropic coordinate change, the spherical mean multiplied by radius obeys the Helmholtz oscillator equation. A nonzero mean cannot maintain a single-sign 1/r tail indefinitely. The inverse wavenumber is `sqrt(mu_e)/mu_K` in transverse coordinates; this is a local coefficient calculation, not a global-uniform-external-field cosmology.

The physical stiffness cannot be neglected at the shortest quoted scales. For one frozen positive-Pi branch, let `H_W` be the polarization Hessian and define

\[
v=K\widehat k^T H_W^{-1}\widehat k,\quad
\beta=\gamma v/K=L_*^2v/2.
\]

Eliminating P gives the directional static characteristic polynomial

\[
\boxed{\beta k^4+(1-v-\beta\mu_K^2)k^2-\mu_K^2=0.} \tag{5}
\]

Its roots in k² have opposite signs. There is an oscillatory branch and a screened Yukawa branch. A specially selected Yukawa solution need not oscillate; it also does not carry a nonzero Kepler excess to infinity. On the negative-Pi branch the one-sided stiffness is absent. Angular matching across the Pi=0 switch is a separate weak-solution issue.

For Lstar=22 pc, the directional numbers are:

| mu_K / Mpc^-1 | direction | oscillatory inverse k | Yukawa decay length |
|---:|---|---:|---:|
| 198.25 | transverse | 590.16 pc | 132.09 pc |
| 198.25 | parallel | 816.47 pc | 94.86 pc |
| 25120 | transverse | 22.71 pc | 27.09 pc |
| 25120 | parallel | 22.84 pc | 26.76 pc |

These lengths show that a restored-gate region cannot simply be treated as a long Kepler exterior. They are spatial-response scales, **not** a full-GR ghost proof or a global no-go against compensated matching.

## 6. Executed coupled boundary-value checks

The scripts solve all four equations in section 2 and check the original, unclipped gate on the accepted solution. Trial Newton iterates use a bounded gate extension; accepted large-positive-u clipping only replaces values already below double-precision underflow. Negative-Pi or p>=1 iterates are never accepted as physical solutions.

`run03` contains a smooth Plummer finite-box benchmark on `x in[.001,60]`, `ell=.2,d=.01`. It converges at `m=0,1e-5,1e-4,3e-4`; the tighter-tolerance repeat of m=3e-4 has:

- minimum leading coefficient in (1): `0.0119145`;
- maximum original constitutive residual: `1.30e-6`;
- maximum original Poisson residual: `4.26e-5`;
- relative integrated Poisson-flux discrepancy: `7.26e-7`;
- exact imposed boundary residual at stored precision;
- maximum state change on tolerance refinement: `6.94e-7`.

The m=.001 continuation exceeds its 12000-node cap and enters negative-Pi/p>1 trial states. It is rejected. This is a solver failure near loss of the regular branch, not a mathematical nonexistence proof. The benchmark ell is deliberately larger than the physical galaxy value, so these small-m checks establish solver/equation behavior only.

A physical-parameter annulus is also solved in `run04_annulus`. Set `Mb=1e11 Msun`, `Lstar=22 pc`, `rM=12.2043 kpc`, `ell=.00180265`, `x in[1,60]`, and choose `d=6.94420e-5` so the reference outer `u_R=4`. The inner Gauss flux is one baryon mass; inner Z and outer f,p are fixed to reference values. These are explicit boundary data, not a dynamically obtained mass cap or cosmological match.

Both `mu_K=198.25` (`m=2.41950`) and `mu_K=25120` (`m=306.571`) converge. For the latter, the tighter `5e-7` tolerance gives:

- actual `u_min=4.00092`, positive Pi throughout and `0<p<1`;
- minimum coefficient in (1): `1.62477e-6>0`;
- maximum original constitutive residual: `2.37e-12`;
- maximum original Poisson residual: `1.03e-8`;
- maximum fractional force deviation from the reference: `3.55e-7`;
- original boundary residual zero at stored precision;
- maximum state change on refinement: `1.55e-8`;
- integrated Gauss-flux discrepancy: `4.31e-10` baryon masses.

The direct gate-source quadrature is about `8.36e-21` baryon masses in the annulus. That tiny value is below the flux-error resolution and should be interpreted as negligible source, not as a resolved prediction at 1e-21 accuracy.

**Thus a strongly suppressed static inner annulus exists at the large cosmological mu_K in the tested Newtonian equations.** This prevents an overbroad conclusion that no static galaxy interval can exist. The gate stays off through that box; its later transition, total reservoir, origin, global boundary conditions and dynamical health remain unprovided. The conditional transition obstruction in section 4 is exactly the next matching problem, not contradicted by this finite-box success.

## 7. Further matching and repair results

The continuation in [`matching/RESULT.md`](matching/RESULT.md) supplies an analytic outer-matching obstruction under the explicit condition `gamma_active-H_PiPi>=0`, allowing deformation and compensation rather than assuming an unchanged exterior. The literal flat gate cannot have negative Pi on a regular static solution of that branch; outward polarization flux therefore cannot decrease from the positive inner annulus to a compensated decaying exterior. This condition is not asserted necessary for every full-GR healthy branch, and the clamped gate escapes the negative-Pi argument.

The same continuation quantifies the proposed bounded-piece, Q-independent stabilizing repair. Suppression on the physical annulus forces an off-gate slope `Gamma'_infinity>=1.45e13` at mu_K=25120. Its full covariant constitutive and density terms destroy the fixed-W AQUAL response. The next Q-dependent repair is distinct; pressure columns are provisional scale conversions, with the `sup(B/Q)` correction documented in the matching report; the health lane's separate stress proof controls any pressure-floor claim.

The final perspective/Q-Gamma repair was then independently audited in [`matching/perspective_audit/REVIEW.md`](matching/perspective_audit/REVIEW.md). Its on-shell pressure bound produces an integrated lapse-flux inconsistency of factor 3330.16 at mu_K=25120 even on the actual finite Q band. The corresponding low-mu finite-band test does not exclude that case. Exact domains, Lambda/background qualifications, and the validated run are given in that review.

The follow-up [`polarized_pressure/RESULT.md`](polarized_pressure/RESULT.md) retains pressure in the full static Einstein trace and then subtracts polarization. It rejects the explicit quiet low-mu repair while carefully leaving deformed low-mu polarization outside that diagnostic. A separate scalar bound, independent of quiet P, gives a necessary coefficient ceiling of 435.327/Mpc for Lambda=0 or 445.318–446.305/Mpc for the stated nonzero-Lambda benchmarks, on the same finite-Q-band target. This ceiling can be compared with a separately verified unchanged-FRW lower bound; it does not rely on the historical CMB proxy.

## 8. Reproducibility and interpretation

Accepted core evidence: `run03/manifest.json` and `run04_annulus/manifest.json`, both status **completed**, validated with the installed v2 validator against current pinned files. `run01` failed because its rejected Newton branch produced nonfinite diagnostics that JSON refused to serialize. `run02` completed, but its post-solve boundary diagnostic accidentally closed over reassigned arrays; it is superseded for that diagnostic by run03. The solver's own boundary equations were unchanged. All original scripts and run records are retained.

The run03 stderr retains NumPy scalar-conversion deprecation warnings and a warning from the rejected Newton branch. Neither is counted as successful evidence; accepted runs use finite original-equation checks. Execution and validation commands, versions, CPU/thread policy, elapsed times, input hashes, and output hashes are in the manifests. Source-only algebra does not depend on external literature.

To reproduce run03, use the argv and execution-artifact list in its manifest with a fresh output directory and result path. Do not overwrite the recorded directory. The bounded command has a 40-second wall cap, 1 MiB log cap and one-thread setting.

**Evidence classification:** exact symbolic identities verified for the stated Newtonian radial action and EFE reference; floating-point finite-profile corrections and finite-box solves checked in the stated domain; conditional obstruction to retaining the unchanged AQUAL field through the flat-gate transition. This is substantive negative evidence against that proposed closure mechanism, while leaving a substantially deformed, dynamically supplied, or modified-action construction as an explicit separate problem.

Self-review: this file was checked for local notation and equation/prose consistency using the proofread-math self-review workflow. No unrelated historical text was rewritten. Correctness scope remains the derivations and finite assertions explicitly stated here.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
