# Direct derivation chains, AFG-001 → AFG-003

These are deductions made here from the specified framework branches. No
external theoretical result is imported. This is not a claim of historical
novelty or a completed gravity theory. All averages use the SAME normalized,
nonnegative weights. B is the positive baryonic radial acceleration, g the
positive total radial acceleration, and a the common acceleration scale.

## 1. The algebraic law has an exact moment closure

Assume Q pointwise: g² = B² + aB. Linear averaging gives

    <g²> - <B²> = a <B>.                                  (1)

Consequently the scale inferred by applying Q to mean accelerations is

    a_mean = (<g>² - <B>²)/<B>
           = a - [Var(g) - Var(B)]/<B>.                    (2)

This is exact for finite positive-weight mixtures or distributions with finite
second moments and <B> > 0. No expansion in scatter is used.

For F(B) = sqrt(B²+aB),

    F' = (2B+a)/(2 sqrt(B²+aB)) > 1,
    F'' = -a²/[4(B²+aB)^(3/2)] < 0.                       (3)

For two independent copies B and B', the mean value theorem gives
|F(B)-F(B')| >= |B-B'|. Since Var(X) = <(X-X')²>/2,
Var(g) >= Var(B). Thus a_mean <= a, strictly for nonconstant B and a>0.
Equivalently concavity gives <F(B)> <= F(<B>).

**Physical scope:** this is averaging already computed radial accelerations.
It is not a solution of a nonlinear three-dimensional gravitational field
equation for a clumpy density. Applying the theorem to that different operation
would be unjustified. Nor does an X-ray hydrostatic inversion measure <g> with
these weights. The sign theorem therefore cannot dismiss every cluster
measurement systematic.

The exact invariant (1) belongs to Q only. For R, numerical differentiation
and a symbolic second derivative locate a curvature zero near B/a=6.63412:
the function is concave below and convex above that crossing in the sampled
range. A universal R concavity claim is false. No universal root count is
inferred from that numerical check. M also remains a distinct branch.

## 2. Translate Q into a conditional spectroscopic test

Consider independent circular tracer elements with a common known radius r and
line-of-sight projection p != 0. Their intrinsic line velocities, relative to
the systemic rest frame, obey u² = p² r g. These assumptions can describe an
idealized matched stack; a real beam requires demonstrating the common-geometry
approximation or explicitly modelling its variation. Arbitrary clumpy patches
do not automatically admit circular equilibrium.

Let observed velocity v = u + epsilon. Assume epsilon is independent,
zero-mean Gaussian with known common variance s², combining a calibrated
instrument width and an independently constrained intrinsic Gaussian width.
Define OBSERVED RAW moments m2=<v²>, m4=<v⁴>, not central kurtosis. Expansion gives

    U2 = <u²> = m2 - s²,
    U4 = <u⁴> = m4 - 6s² m2 + 3s⁴.                       (4)

The exact Q estimator is

    a_moment = [U4/(p⁴ r²) - <B²>]/<B>.                  (5)

The baryonic moments must use the SAME emissivity/selection weights as the
spectrum. A baryonic mass-weighted average cannot silently replace them.
With controlled projection, Q additionally demands

    U4/(p⁴r²) - <B²> - a(z)<B> = 0.                      (6)

This is a falsifiable measurement equation. The scale a(z) can be fixed by the
vacuum branch or the H(z) branch BEFORE examining the spectrum. Rebinning with
known weights preserves (1), although r and p variations prevent directly using
(5) on an arbitrary spatially averaged spectrum.

The synthetic four-component spectrum recovers a/a_true=1 to floating accuracy
for three widths. Applying Q to mean g instead gives 0.814492. Underestimating
s by 20% gives inferred scales 1.00904, 1.23051 and 2.84708 times the true value
as the broadening grows. Therefore line moments are not automatically immune
to instrumental or thermal uncertainty. Non-Gaussian or component-dependent
broadening requires its own higher-moment response; a PSF alone does not specify
it. No actual high-redshift spectrum was analysed here.

## 3. Invert the mass discrepancy after including MOND

Let g_H be a spherical hydrostatic-equivalent acceleration at measured r.
From catalogued baryons, B = G M_b(<r)/r². For any monotone F, calculate

    B_required = F^{-1}(g_H; a),
    M_source,required = r² B_required/G,
    Delta M_source = M_source,required - M_b.             (7)

This is an equivalent additional source INSIDE the MOND kernel. It is not the
mass of an extra component that couples differently. In particular,

    Q: B_required = 2g_H²/[sqrt(a²+4g_H²)+a].             (8)

R and M are inverted numerically with a monotone bracket and then passed through
the forward law as a check. An independent diagnostic is

    q_force = F(B;a)/g_H.                                (9)

If hydrostatic acceleration is attributed to a multiplicative measurement bias,
the inferred value must be reduced to q_force of its current value while
holding the baryonic profile and radius fixed. Real changes in distance,
temperature and density affect multiple quantities together; (9) is the target
for such a joint forward model, not proof that such a bias exists.

If one instead adds an independently Newtonian source outside the kernel, its
required equivalent mass is r²[g_H-F(B)]/G. This is a DIFFERENT coupling rule;
it cannot be substituted for (7) without specifying dynamics.

For the seven X-COP clusters with their own stellar profiles, all 21 evaluated
radial points need positive extra source on every Q/R/M normalization branch.
At 300 kpc the canonical R source factor is 5.998 median, with force coverage
0.3098. Alternative normalization gives 5.556 and 0.3340. M agrees closely in
this low-acceleration range. These are cached central-profile diagnostics,
without joint errors or a likelihood, conditional on hydrostatic equilibrium,
distance, deprojection, stellar masses and the published reconstruction.

At matched B within 0.1 dex, and counting each matched SPARC galaxy once, the
seven cluster points at 300 kpc lie a median 0.481 dex above the galaxy
acceleration-discrepancy medians. This is a direct cross-regime diagnostic;
it is not a statistically established violation, because the instruments,
tracer equations and nuisance distributions differ.

## 4. Can unresolved structure hide cosmological scaling?

In the strict deep limit, g=sqrt(aB). Suppose ln B is normal with variance S
and mean chosen so <B>=b. Completing the Gaussian square gives, for any p,

    <B^p> = b^p exp[(p²-p)S/2].                          (10)

Thus <g>=sqrt(ab) exp(-S/8), and the mean-acceleration deep estimator is

    a_mean = <g>²/b = a exp(-S/4).                        (11)

If a_true(z)=a_today E(z), matching the constant-scale mean requires

    S=4 ln E,    CV(B)=sqrt(exp(S)-1)=sqrt(E⁴-1).         (12)

With the contract's illustrative cosmology, E(3)=4.56563 and CV=20.821.
This large scatter is a conditional price, not evidence that it occurs.
For the common-geometry line model, define the intrinsic RAW moment ratio

    K = U4/U2² = <g²>/<g>².                              (13)

In the strict deep limit, the hiding construction implies K=E. It cannot hide
the evolution in the mean without changing the line shape in this model.
K is not the usual central excess kurtosis. Brightness weighting, geometry,
systemic-velocity errors and Gaussian deconvolution must be specified to use it.

A lognormal has an unbounded tail, so (11)-(12) are deep-limit asymptotics, not
exact for Q or R. AFG-002 solves the full functions with the first moment of B
held fixed, rather than using the asymptotic result outside its regime.
At z=3 and b/a_today=0.01, the exact Q/R solutions need CV=21.89/21.05 and
predict K=9.275/9.003. At b/a_today=0.1 the predicted K rises to 77.95/42.21.
The high-acceleration tail strongly affects the fourth line moment even when
the mean response is close to its deep approximation. These large values
require actual spectra and a realistic geometry before becoming an exclusion.

## 5. Stronger result: a distribution-independent spectral price

The previous route need not assume a lognormal. For ANY positive distribution
with finite second moments, keep b=<B> and assume the evolving Q law with
a_true=E a_today, E>1. If its mean is made to equal the constant-scale prediction,
<g>=sqrt(b²+a_today b), equation (1) yields

    K = [b² + Var(B) + E a_today b]/[b²+a_today b]
      >= (q+E)/(q+1),      q=b/a_today.                  (14)

For E>1 the equality configuration Var(B)=0 cannot also meet the specified
mean, so equality is not attained. The conservative non-strict lower bound is
still valid and needs no distribution fit. A measured deconvolved K below it
rules out hiding H(z) by this averaging mechanism under the stated geometry.

For R one still has a general inequality. For t>0, 1-exp(-t)<=t, so
F_R(B;a)>=sqrt(aB). If <g>=F_R(b;a_today), then

    K >= E q / f_R(q)²
       = E [1-exp(-sqrt(q))]²/q,                        (15)

in addition to K>=1. This applies to all source distributions with finite
moments, including those with a non-deep tail. For M the pointwise relation
F_M>=F_R follows from its definition h'_M=max(h'_R,positive floor) and the
common low-end initial value, WITHIN its defined grid; its corresponding
bound uses its own target denominator f_M(q)², not f_R(q)².

At z=3, q=0.01, (14) requires K>=4.530 and (15) requires K>=4.135.
The exact lognormal example exceeds both, as required. The bound is the stronger
research result: hiding evolution has a testable spectral cost even without
selecting a distribution. It is conditional on the local static law and
measurement map, not a new relativistic field equation.

## What these chains do not derive

They do not derive kappa, select a unique interpolation law, produce a conserved
covariant action, prove stability, calculate CMB/BAO, establish lensing closure,
or fit all observations. A0 scaling alone underdetermines those obligations.
The new campaign has a mathematical test of a measurement explanation and a
quantified cross-regime source requirement. Both can guide a new physical
construction; neither is that construction already completed.
