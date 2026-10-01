# Independent proof audit: zero-background energy expansion

Reviewer: /root/pressure_extrema. **Accepted in its stated scalar Q/RAR
scope.** No mathematical error was found. I read only ROOT_DERIVATION.md
for this new proof and independently checked the expansions, directional
factors and limits. I did not read new worker/auditor formulas, source code
or results. No numerical computation or finite-point verification was run.

The root file records that it was fixed before reading new author/auditor
formulas. This audit does not enlarge that provenance claim or turn its
asymptotic statements into checked finite-sample values.

## Constitutive inversion and local series

Integrating the Q inverse gives exactly the displayed w. Expansion of
sqrt(1+4x²) gives bbar=x²-x⁴+O(x⁶), and integration gives
w=x³/3-x⁵/5+O(x⁷). The rationalized form of bbar is equivalent and avoids
the cancellation in subtracting one from the square root at small x.

For RAR, expansion of t²/(1-exp(-t)) gives
f(t)=t+t²/2+t³/12+O(t⁵). Substitution of
t=x-x²/2+5x³/12+O(x⁴) cancels the x² and x³ residuals. Squaring t then
gives x²-x³+13x⁴/12+O(x⁵), whose integral is the stated w_R.
The regular inverse at zero follows from f'(0)=1. For positive t,

    f'(t)=t[2-(2+t)exp(-t)]/[1-exp(-t)]²>0,

since 2exp(t)>2+t. Thus the chosen nonnegative inverse branch is unique.
No Q interpolation was substituted for RAR in this check.

## Linear subtraction, vector Hessian and deep ratios

For radial energy W(|G|), the gradient is b(g) Ghat. Its Hessian has
longitudinal eigenvalue b'(g) and transverse eigenvalue b(g)/g. Multiplying
the Hessian quadratic form by one half gives H2 as written. The subtraction
in D is exactly the linear Taylor term, including the sign for an opposite
parallel perturbation. Convexity implies D>=0.

The common leading scalar energy is g³/(3a). At G=0 its vector Hessian is
zero: both nonzero-background Hessian eigenvalues tend to zero. Strict
convexity nevertheless persists and is not a uniform positive quadratic
lower bound at that point. More explicitly, the next Q correction has order
|h|⁵/a³, while the first RAR correction has order |h|⁴/a², with a fixed.

For a fixed positive relative amplitude epsilon, dividing the leading D
by a²x³ produces exactly the displayed angle expression. The corresponding
H2 coefficient is epsilon²(1+cos²(theta))/2. For signed parallel directions
with epsilon<=1, expansion of (1+epsilon)³ or (1-epsilon)³ therefore gives
1+epsilon/3 or 1-epsilon/3. The opposite case at epsilon=1 is included:
the perturbed gradient reaches zero and the ratio tends to2/3.

For transverse perturbations the ratio is
2[(1+epsilon²)^(3/2)-1]/(3epsilon²), with expansion
1+epsilon²/4+O(epsilon⁴). The epsilon=1 examples follow directly.
At each fixed epsilon>0 the next Q contribution is relatively O(x²),
and the next RAR contribution O(x), because their next energy terms have
orders x⁵ and x⁴ respectively versus a nonzero order-x³ denominator.
These error statements are not asserted uniformly as epsilon tends to zero,
nor do they certify numerical errors at the task's finite sample points.

## Fixed-background relative remainders

For signed parallel perturbation d=s epsilon g, the cubic Taylor term is
b''(g)d³/6. Division by b'(g)d²/2 gives
s epsilon g b''(g)/(3b'(g)), with the stated O(epsilon²) remainder.

For a transverse perturbation,
|G+h|-g=g(epsilon²/2-epsilon⁴/8+O(epsilon⁶)). Expanding W gives the
quartic correction (g²b'-gb)epsilon⁴/8; division by gb epsilon²/2 yields
(gb'-b)epsilon²/(4b)+O(epsilon⁴). Odd transverse powers vanish by symmetry.
The deep coefficient limits are respectively1/3 and1/4. Small |h|/a alone
does not justify the quadratic expansion uniformly near zero background;
the relevant gradient ratio is |h|/g. The Fourier-gradient qualification
correctly prevents confusing field-potential amplitude with its derivative.

## Iterated limits

For independent absolute amplitudes g,d>0 in the same direction, taking
d to zero first at fixed g gives D/H2->1. Taking g to zero first at fixed
d instead gives D->W(d)>0 while H2~g d²/a->0, hence the extended-real
ratio tends to positive infinity. The later d limit remains infinity.
The ratio is undefined at exactly g=0, so no finite observable is assigned
there by this argument.

Both orders of the raw D limits give zero, and both orders of raw H2 give
zero. Thus the noncommutation claim is correctly restricted to the normalized
relative approximation. Fixed epsilon paths are another family of limits;
they are not mislabeled as these absolute-amplitude iterated limits.

## Kinetics, units and acceptance boundary

With positive fixed K=2, the time kinetic coefficient stays positive. The
linearized uniform-background spatial eigenvalues give
c_parallel²/c²=b'(g)/2 and c_perp²/c²=b(g)/(2g). Their leading limits are
g/a and g/(2a), so the stated speed square roots follow. Vanishing spatial
quadratic stiffness is not a negative time kinetic coefficient, and this
calculation does not establish a ghost, a nonlinear PDE well-posedness result,
a matter instability or continuation through the zero-gradient set excluded
by FGF034.

Homogeneity b=a bbar and W=a²w verifies the physical restoration. For fixed
x and epsilon, physical g and |h| scale with a, and energy density increments
scale as a²/(4piG). Both empirical a normalizations can share dimensionless
formulas without sharing the same physical-gradient background. Frozen H
references change these physical factors; an evolving reference requires its
separate work balance and is not modeled by this static expansion.

The accepted claim is an analytic diagnostic of the unfiltered scalar Q/RAR
energy and its nonuniform quadratic approximation. It supplies no finite-point
numerical certification, registered-M or filtered-MONO transfer, coupled-matter
stability, density/discrepancy inference, observational calibration, physical
metric/photon sector, historical novelty or full-theory closure.
