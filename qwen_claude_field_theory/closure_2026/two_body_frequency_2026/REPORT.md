# A comparable-mass force and an orbital three-frequency relation

## Result, without an empirical victory claim

For the existing double-filter action T-B, two source positions can be varied
consistently. In an isolated, Gaussian-filtered, compact deep-field pair the
leading relative equation is

\[
 \ddot{\mathbf r}=-\frac{GM}{r^3}\mathbf r-h(M)\mathbf r+\cdots,
 \qquad h(M)\sim\frac{2}{9}\frac{\sqrt{GMa_0}}{\xi^2},
 \quad M=m_1+m_2.
\]

The mutual anomalous force is minus the reduced mass times h r. This is
derived from the two-position action, not an assumed total-mass substitution
in the previously derived test-particle field. Its harmonic coefficient is
independent of mass ratio at leading order, but higher terms need not be.

A different, external-field-dominated regime yields the main orbital result:

\[
 \boxed{\frac{\omega_r^2-\omega_\phi^2}
 {\omega_\phi^2-\omega_z^2}
 =\frac{3[5\lambda(y)-y]}{2y}},\qquad
 \lambda(y)=1+(y-1)e^{-y}.
\]

Here omega_phi is circular orbital frequency; omega_r and omega_z are the
frequencies of infinitesimal radial and vertical perturbations about an orbit
perpendicular to the fixed external-field axis. The equation holds in the
harmonic-core limit and linear constitutive response. The nonsingular form is

\[
 2y(\omega_r^2-\omega_\phi^2)
 -3[5\lambda(y)-y](\omega_\phi^2-\omega_z^2)=0.
\]

At y=1 the predicted ratio of squared-frequency differences is 6. At fixed
background, total mass, mass ratio and the isotropic filtering amplitude
cancel in this limit. This is an orbital translation of the earlier central
tidal identity, not an independently new action or an empirical discovery.

**Status:** conditional static derivation with bounded numerical verification.
Empirical significance, global novelty and relativistic completion are OPEN.
The isolation and external-field limits above must not be combined.

## Same action; both sources varied

Use the action and q of `../smoothed_onset_action_2026/REPORT.md`:

\[
 I=\int dt\,d^3x\left\{L_{m,kin}-\rho\Phi
 -\frac{2\nabla\Phi\cdot\nabla u-|\nabla u|^2
 -a_0^2q(|\nabla Su|^2/a_0^2)}{8\pi G}\right\}.
\]

The filter S is Gaussian with width xi, and q'(s^2)=nu(s)-1, where
s=y(1-exp(-y)), nu=y/s. Eliminating stationary potentials gives

\[
 U_{\rm ph}[\rho]=-\frac{a_0^2}{8\pi G}\int q(|p|^2/a_0^2)\,d^3x,
 \quad p=\nabla Su,\qquad
 \delta U_{\rm ph}=\int\Phi_{\rm ph}\,\delta\rho\,d^3x.
\]

The last identity includes the outer adjoint filter. For a unit source define
v_xi(x)=-erf(|x|/(sqrt(2)xi))/|x| and its Hessian H_xi. Then
p=G sum_a m_a grad v_xi(x-x_a), so independent source-position variation gives

\[
 \mathbf a_{a,\rm ph}=-\frac1{4\pi}
 \int H_\xi(x-x_a)\,[f(p_e+p)-f(p_e)]\,d^3x,
 \quad f(p)=[\nu(|p|/a_0)-1]p.
\]

This is the force quadrature implemented directly. The external constant
flux is subtracted before calculating internal forces; the specified physical
uniform external acceleration is separate boundary data. Its subtraction
corresponds to subtracting constant and linear background terms in the
reduced functional. In isolation use a fixed-total-mass reference:
U_ph(pair)-U_ph(M delta_0). Subtracting two isolated self energies instead
does not remove the logarithmic far-field divergence. Newtonian point-source
self energies are position-independent and excluded; their mutual force
remains exactly -G m1 m2 r/r^3. Nonlinear phantom halos are not additive.

## Why total mass appears in the compact-pair coefficient

Fix the COM and write m_red=m1 m2/M. The density expansion is

\[
 \rho=M\delta_0+\frac{m_{\rm red}}2r_ir_j\partial_i\partial_j\delta_0
 +O(r^3).
\]

Expand the reduced phantom energy about the combined monopole. In isolation
its central potential is even and isotropic. Consequently

\[
 U_{\rm ph}(r)-U_{\rm ph}(0)
 =\frac{m_{\rm red}}2h(M)r^2+O(r^4).
\]

The source quadrupole is already the variation producing this energy term;
it does not add another leading coefficient. Differentiating and dividing
by the reduced mass yields the displayed relative equation.

Let epsilon=GM/(a0 xi^2). The parent's Gaussian integral gives
h=(2/9)sqrt(GMa0)/xi^2 in the epsilon->0 limit. Relative corrections are
O(sqrt(epsilon))+O((r/xi)^2) in the ordered compact/deep expansion. Fixed
positive mass fractions and pointlike baryonic sources relative to the
separation are assumed. This regular filtered-source expansion is not a
proof of regularity for all unsmoothed MOND critical points.

For a circular isolated pair this gives

\[
 \omega_\phi^2=\frac{GM}{r^3}+h(M)+\cdots.
\]

It extends, rather than replaces, the previous sixth-power onset result.
No comparable-mass law at arbitrary separation or arbitrary environment
has been solved by this asymptote.

## Three frequencies from independent potential derivatives

In the linear external-field regime the pair-response kernel is symmetric
and translation invariant. Self terms are position independent; varying
the cross term gives a relative potential with source mass M. Its Fourier
phantom contribution is

\[
 \widehat V_{\rm ph}(k)=-\frac{4\pi GM}{k^2}|\sigma(k)|^2
 [A+B(\hat k\cdot\hat e)^2],\quad
 A=\nu(s_e)-1,\quad B=s_e\nu'(s_e).
\]

For a convergent isotropic spectral integral the central Hessian is the
one independently established in `../filtered_tidal_relation_2026/`:

\[
 H_\perp=C(5A+B),\quad H_\parallel=C(5A+3B),\qquad
 C_{\rm Gaussian}=\frac{GM}{30\sqrt\pi\,\xi^3}.
\]

Write cylindrical coordinates (R,z), with z along the constitutive external
field. The relative potential per reduced mass in the core is

\[
 V=-\frac{GM}{\sqrt{R^2+z^2}}
 +\frac12(H_\perp R^2+H_\parallel z^2).
\]

At z=0 differentiate before substituting:

\[
 \omega_\phi^2=\frac{V_R}{R}=n^2+H_\perp,\quad
 \omega_r^2=V_{RR}+\frac{3V_R}{R}=n^2+4H_\perp,\quad
 \omega_z^2=V_{zz}=n^2+H_\parallel,\quad n^2=GM/R^3.
\]

Thus the squared-frequency-gap ratio is -3(5A+B)/(2B). For the exact
exponential inverse, B/A=-y/lambda, giving the boxed expression. The
coefficient C cancels for any isotropic filter with a finite central Hessian,
not just the two smooth filters tested here. The Gaussian/mixture finite-R
errors are O((R/xi)^2); this error power requires additional spectral moments
and must not be assumed for every rough filter.

Circular existence and linear orbital stability require all three displayed
frequency squares to be positive. For weak anomalies, the apsidal rate is
omega_phi-omega_r ~ -3H_perp/(2n), and the nodal rate is
omega_phi-omega_z ~ (H_perp-H_parallel)/(2n). These are physical orbital
stability statements within this static model, not ghost or GW checks.

## Numerical evidence capable of failing

The force run covers 36 combinations: epsilon={1e-8,1e-6,1e-4}, mass fraction
{0.1,0.3,0.5,0.9}, and r/xi={0.02,0.06,0.2}. It integrates the actual
nonlinear flux against each source Hessian; it does not set h to 2/9.
The action derivative is checked with a separate energy finite difference.

- At epsilon=0.02, mass fraction=0.3 and r/xi=0.15, energy and force
  derivatives agree to 1.01e-8 relative; normalized net force is 8.73e-13.
- In the declared asymptotic subset epsilon<=1e-6, r/xi<=0.06, the largest
  difference from the leading coefficient is 0.0756%. This includes physical
  finite-epsilon/separation corrections, not just quadrature error.
- Force quadrature orders 42 and 58 differ by 2.76e-9 on the selected check.
- Additional tests compare both independently varied forces with the linear
  external tensor for parallel/perpendicular separation at y=1, epsilon=1e-4,
  mass fraction=0.3 and r/xi=0.03; both satisfy the 0.1% tolerance and the
  momentum residual threshold 2e-6.

The spectral run covers 50 cases: y={0.3,1,2.5,4,6}, R/xi={0.01,0.03,0.1,0.3,1},
and Gaussian versus a normalized Gaussian-mixture filter. It differentiates
the full finite-R Fourier potential, not a preset harmonic Hessian. Its
frequency differences are formed before adding the common Newtonian term to
avoid subtraction of large nearly equal floating-point numbers.

At y=1 for the Gaussian filter:

| R/xi | Computed squared-frequency-gap ratio | Core limit |
|---|---:|---:|
| 0.01 | 5.999903572 | 6 |
| 0.03 | 5.999132192 | 6 |
| 0.10 | 5.990363179 | 6 |
| 0.30 | 5.913702045 | 6 |
| 1.00 | 5.094352179 | 6 |

The last row is an explicit failure of extending the core formula to R=xi;
it is retained, not calibrated away. Across all R/xi=0.01 rows, the maximum
normalized division-free residual is 1.835e-5. The normalization is the sum
of the absolute values of the two terms being compared. Spectral orders
42/58 change the selected ratio by 1.21e-12. These are bounded float64
results, not interval-certified errors or data uncertainties.

## Limits that matter before observational claims

The three-frequency relation requires a nonzero constant background, linear
constitutive response, a small core orbit, small radial/vertical oscillations
and the stated boundary subtraction. It is not universal for arbitrary
orbits, varying Galactic fields, added ordinary external tides or nonlinear
internal fields. Nonlinear external response can break inversion symmetry:
an unequal-mass source octupole can couple to a third derivative of the
monopole potential, allowing cubic separation energy and a displaced orbital
plane. That coefficient is not computed here.

The parameter y is defined by s_e=y(1-exp(-y)), where s_e is the filtered
Newtonian background divided by a0. It is not automatically the measured
physical external acceleration divided by a0. Kernel comparisons must use
the same independently modeled environment. Deep-background behavior alone
is not an exponential fingerprint: the ratio tends to 27/2 for the usual
differentiable deep-MOND inverse asymptotic.

No data establish that all three frequencies can be measured at useful
precision in a suitable binary. A long-period wide binary does not supply
three accurately measured frequencies merely because a static model
predicts them. Quasistatic applicability, external-field time variation,
source sizes, baryonic masses, distances and other tidal sources require
an observational forward model. No interpolation kernel or xi was fitted
against observations here; neither xi nor a0 is derived cosmologically.
The construction is not the strict exponential AQUAL equation, and supplies
no independent metric, PPN, DOF, causal or cosmological closure.

## Prior art and honest contribution

Known MOND two-body laws must not be renamed as this result. Milgrom,
*Quasi-linear formulation of MOND*, [arXiv:0911.5464v2](https://arxiv.org/pdf/0911.5464v2)
(2 March 2010), section 4.1, gives the deep-MOND virial and its nontrivial
mass-ratio dependence. The present added-scale compact regime is different.

Zhao, Li and Bienayme, *Modified Kepler's Law, Escape Speed and Two-body
Problem in MOND-like Theories*,
[arXiv:1007.1278v2](https://durham-repository.worktribe.com/OutputFile/1530851)
(18 August 2010), equations (13), (23), (34), already derive modified orbital
laws and discuss Hernquist smoothing. Their force/kernel is not the varied
Gaussian double-filter action used here. This establishes substantial
adjacent prior art, not an exact match of the present coefficients.

Milgrom, *A novel MOND effect in isolated high-acceleration systems*,
[arXiv:1205.1317v3](https://arxiv.org/pdf/1205.1317v3) (16 August 2012),
derives an isolated quadrupolar two-body anomaly proportional to separation
cubed and explicitly discusses quasistatic restrictions. It is not our
isotropic leading harmonic term proportional to separation, but rules out
claiming that an inner-orbit MOND anomaly is itself unprecedented.

The action architecture already falls within Milgrom's nonlocal functional
generalization, arXiv:2305.01589v2 (reviewed in the parent report). The new
repository contribution is the two-position derivation/check of the compact
coefficient and an orbital-frequency translation of the existing central
tidal identity. The frequency formula is a formal corollary of that identity
and the standard epicyclic derivative equations. No global priority claim
is made.

Bounded English-language web searches used `MOND filtered QUMOND binary
epicyclic vertical frequency precession relation` and `MOND Gaussian
smoothing two body harmonic force mass ratio`, checked 4 September 2026
local time. Sources were read through the web reader, not retained in a local
cache (the exact-version cache lookup found none). The precise formula was
not identified in inspected passages; this is not an exhaustive literature
or citation-chain search. Mathbox literature and proof checks limited the
claim to its actual scope rather than certifying novelty.

## Reproduction and files

Six new files in this directory: CONTRACT.md, REPORT.md, binary_frequency.py,
test_binary_frequency.py, results.json and computation_manifest.json.
Existing physics code is unchanged. Running the parent and tidal regressions
regenerated their normal CLI outputs, including the tracked parent computation
manifest (commit/timing metadata only). At the original study handoff no commit
or push had been performed; the user subsequently authorized both on
5 September 2026. Independent Astra G03 files are separate work and not
counted as evidence for the orbital relation.

| Exact command from repository root | Exit / result |
|---|---|
| `python3 qwen_claude_field_theory/closure_2026/two_body_frequency_2026/binary_frequency.py` | 0; eight finite check groups |
| `python3 -m unittest discover -s qwen_claude_field_theory/closure_2026/two_body_frequency_2026 -v` | 0; nine tests |
| `python3 -m unittest discover -s qwen_claude_field_theory/closure_2026/smoothed_onset_action_2026 -q` | 0; ten parent tests |
| `python3 -m unittest discover -s qwen_claude_field_theory/closure_2026/filtered_tidal_relation_2026 -q` | 0; six tidal tests |
| `python3 -m unittest discover -s hunt_2026/exact_mu_cassini_2026 -q` | 0; six inverse-kernel tests |
| `python3 qwen_claude_field_theory/closure_2026/elliptic_phantom_action_gate_2026/test_elliptic_phantom_action_gate_2026.py` | 0; two tests |
| `python3 <home>/.codex/plugins/cache/openai-curated-remote/mathbox/2.2.0/skills/computation-audit/scripts/validate_manifest.py qwen_claude_field_theory/closure_2026/two_body_frequency_2026/computation_manifest.json` | 0; valid manifest |

Total: 33 distinct tests, not 33 independent predictions. The manifest pins
actual commit/dirty state, Python/NumPy/SciPy/SymPy versions, bounds and hashes.
Development failures: six initial expected missing-implementation failures
(exit 1); a later exact-center test exposed a numerical division warning in
an unused expression branch (exit 1). A finite unused denominator plus the
existing analytic central series fixed it without changing any physics or
tolerance. The exact-center test now runs with numerical warnings as errors.

An independent reviewer checked the action-force normalization, reduced-mass
factor, spectral derivative signs, tests and scope, finding no important
issue. The final report received a mathematical-notation self-review.

**Next decisive calculation:** a joint observability/precision forecast for
the radial and nodal signals in a realistic system, alongside nonlinear
external-field/finite-source corrections. Until both the domain and the
measurement are established, this is a candidate orbital consistency law,
not an observed Kepler-grade breakthrough.
