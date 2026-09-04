# Two finite-interval tests of algebraic MOND responses

Date: 2026-09-04. These equations are formal consequences of specified response
laws. Their empirical status is determined separately by the catalog analysis.
They are not new fundamental laws or a relativistic completion.

## Scope and the two distinct exponential kernels

Write b=g_bar>0 for the Newtonian radial acceleration inferred from the baryons,
g=g_obs>0 for the circular acceleration, and a0>0 for a constant acceleration scale.
The explicitly requested kernel is

\[
 b=g(1-e^{-g/a_0}). \tag{1}
\]

The empirical RAR exponential is a different relation,

\[
 g=\frac{b}{1-e^{-\sqrt{b/a_0}}}. \tag{2}
\]

Both will be compared. Relation (1) follows exactly from spherical AQUAL outside
or inside a spherical baryonic source when b=GM_b(r)/r^2 and the usual regular
flux boundary condition applies. Applying (1) or (2) pointwise to a disk is an
algebraic-response hypothesis. A non-spherical AQUAL or QUMOND disk generally
needs a field solve; geometrical and external-field corrections are not derived
by this note. We assume circular equilibrium and consistent baryonic profiles.

The framework's proposed normalization
a0=(c/2)sqrt(G_N rho_Lambda) may be inserted as a fixed input. It is not derived
here. The inequalities below do not determine a0; the predicted finite responses
at specified dimensional b values do depend on it.

## Global slope and curvature proof

Use natural logarithms for derivatives and define

\[
 L(x)=\frac{x}{e^x-1},\qquad x>0.
\]

Since e^x>1+x, we have 0<L<1. Moreover,

\[
 L'(x)=\frac{e^x(1-x)-1}{(e^x-1)^2}<0.
\]

The numerator is zero at x=0 and has derivative -x e^x<0 thereafter.
This establishes its sign globally, without numerical sampling.

For (1), x=g/a0 and b/a0=x(1-e^-x). Chain-rule differentiation gives

\[
 S_{\exp}=\frac{d\ln g}{d\ln b}=\frac1{1+L},\qquad
 K_{\exp}=\frac{d^2\ln g}{d(\ln b)^2}
       =-\frac{xL'}{(1+L)^3}>0. \tag{3}
\]

For (2), x=sqrt(b/a0), so

\[
 S_{\rm RAR}=1-\frac L2,\qquad
 K_{\rm RAR}=-\frac{xL'}4>0. \tag{4}
\]

Both slopes lie strictly between 1/2 and 1, approach 1/2 in the deep limit,
and approach 1 in the Newtonian limit. Thus ln g is a strictly convex function
of ln b. Changing both logarithms to base 10 leaves the slope unchanged and
multiplies the curvature by ln(10), preserving its sign.

These statements are not universal consequences of MOND asymptotes alone.
For example, mu(x)=1-exp[-(x+10x^3)] is smooth and increasing, with mu~x at zero
and mu->1 at infinity, but d ln mu/d ln x exceeds 1 near x=1/4. Its corresponding
response slope is below 1/2 there. The following bounds are shared predictions
of the kernels actually proved above, not a no-go against every possible kernel.

## Test 1: an exact endpoint transfer, without a local derivative

For 0<b_lo<b_hi, integrate 1/2<S<1 over the interval in ln b:

\[
 \boxed{\sqrt{b_{\rm hi}/b_{\rm lo}}
       < g_{\rm hi}/g_{\rm lo} < b_{\rm hi}/b_{\rm lo}.} \tag{5}
\]

Equality belongs to the pure deep-MOND or Newtonian comparison laws, respectively.
The exact kernel prediction is

\[
 T_k=\log_{10}g_k(b_{\rm hi};a_0)
       -\log_{10}g_k(b_{\rm lo};a_0). \tag{6}
\]

For mu_exp this uses the unique positive inverse of x(1-e^-x); for the RAR law
it uses (2). This is a finite secant, not a midpoint derivative approximation.
Both the amount of transfer and any departure from the interval bounds can be
measured directly from endpoint velocities and radii.

## Test 2: a three-radius chord defect

Take three distinct baryonic accelerations ordered as b0<b1<b2, irrespective
of their physical radial order. Define

\[
 t=\frac{\log_{10}b_1-\log_{10}b_0}{\log_{10}b_2-\log_{10}b_0},\qquad
 J=\log_{10}g_1-(1-t)\log_{10}g_0-t\log_{10}g_2.
\]

Strict convexity implies

\[
 \boxed{J<0} \tag{7}
\]

for either exponential law at any finite positive noncollapsed interval.
The pure power laws g=C b^(1/2) and g=C b instead give J=0. The exact values
J_exp(b0,b1,b2;a0) and J_RAR(b0,b1,b2;a0) need not agree, so the sign test and
the comparison of kernel predictions are distinct statistical questions.
Computing J takes no numerical derivative and involves no division by a small
velocity difference. Broad intervals and an interior b1 avoid near-collapsed
geometry, but do not remove ordinary measurement noise.

## Nuisance cancellation and measurement conditions

Multiplying all three g values by a common positive number leaves J and T
unchanged. Multiplying all b values by a common positive number leaves t and
the endpoint bounds unchanged. Thus, under the usual SPARC catalog rescalings,
the observed statistics cancel a galaxy-wide distance or inclination correction
to g. A coherent stellar mass-to-light amplitude also cancels the baryonic ratios
for a purely stellar profile. Its shift of the dimensional b values still changes
the a0-dependent prediction. A mixture of gas, disk and bulge need not share one
amplitude; radial mass-to-light gradients and baryonic shape errors do not cancel.
Inclination-dependent reconstruction of the baryonic geometry is likewise outside
the simple common-amplitude statement.

An empirical test should select one broad triple per galaxy deterministically
from baryonic profiles and independent quality rules, before inspecting the
observed velocity response. Keeping one triple avoids treating overlapping
triples as independent galaxies. Do not sort or discard observed g values to
force monotonicity: that would erase genuine violations. Galaxy resampling and
synthetic catalog injections should retain the shared endpoint errors and
propagate the uncertainties in b as well as g. A noise-biased logarithm, a
non-circular velocity, or an incorrect baryonic shape is not evidence for a new
force law by itself.

## Verification and novelty boundary

`response_math.py` symbolically differentiates the two laws and prints the exact
residuals and positive-coordinate domains. It reuses the vectorized force
inversion in `../two_kernel_orbit_shape_2026/orbit_shape.py`; no competing inverse
solver was introduced. Tests recover independently specified forward forces over
b/a0 from approximately 1e-16 to 1e12, compare the analytic curvature to finite
differences, check invalid-input rejection, and verify the nuisance cancellations.
The tests were written and run before the implementation and initially failed
because the response API was missing. The empirical runner records final checks.

The project already contains a local RAR slope test in
`hunt_2026/k02_rar_slope_law.py`, a withdrawn radius-residual claim in
`hunt_2026/f20_rar_radius_slope_verification.py`, and a spherical orbital-curvature
test in `two_kernel_orbit_shape_2026`. The local slope is already recognized there
as prior literature. Equations (5) and (7) are elementary finite-interval
corollaries of the specified kernels and convexity; the contribution here is a
directly measurable statistic with explicit sampling and nuisance handling.
No exhaustive novelty search, global originality, independent law of nature,
or empirical confirmation is claimed in this mathematical note.
