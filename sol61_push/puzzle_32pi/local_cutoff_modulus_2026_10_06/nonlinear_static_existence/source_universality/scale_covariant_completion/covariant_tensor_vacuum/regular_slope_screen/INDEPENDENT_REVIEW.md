# Independent raw review: regular vacuum slope screen

Accepted within the report's stated action and continuation assumptions. I find no blocking mathematical correction. The exact evolving de Sitter TT result is stronger than a frozen dispersion test, but it does not establish the auxiliary candidate's missing two-sided regular continuation, classify all BIMOND actions, or select an interaction normalization.

## Pinned evidence

Reviewed at HEAD `e7babcfcc12f9458c318727f9f008c30ac0bd2e3` on 2026-10-06:

- REPORT.md SHA256 `53754095d1a2161da2361dd36f64876e1e44ecb267ad2e29c2105cb7887b5a37`.
- checks.py SHA256 `b90ec639741f73d5a9dcae4d48148fde4d4ec50d16c3144a5864e9a061939ba8`.

This audit reconstructs the mathematics rather than adopting the author's test verdict. I read the exact report and script, independently recomputed the action Euler equation, evolving energy derivative, and source/growth identities using SymPy, and independently validated the three current b manifests with the standard computation-audit validator. No author inputs were changed.

## Raw action and evolving equation

For one real relative-TT polarization the inherited action is, with an irrelevant positive polarization normalization suppressed,

`L=a^n {q [dot d^2−k^2 d^2/a^2]+KmnH^2 d^2/2}`, `q=K(1−2m)/8`.

The healthy mean tensor has positive coefficient K/2. This relative action includes the expanding-connection term: the parent invariant has `H tr(d dot d)`, whose integration by parts supplies the positive de Sitter `KmnH^2 tr d^2/2` term. It cannot be discarded by importing a flat-space principal symbol. For constant H and m, raw Euler variation divided by `2q a^n` gives

`ddot d+nH dot d+[k^2/a^2−4mnH^2/(1−2m)]d=0`.

The division is admissible only for m≠1/2. Direct symbolic variation gave zero residual against this equation. The background is empty coincident de Sitter, not a finite-density sourced galaxy or a general FRW history. Its TT block closes by isotropy; auxiliary/lapse/shift scalar constraints do not remove a nonzero-k TT polarization at quadratic order. This closure does not certify other helicities.

A two-sided expansion `M(z)=−A+mz+o(z)` makes this quadratic calculation meaningful since the TT connection invariant begins at second order. The positive-z NR source slope alone is insufficient: purely time-dependent TT variations visit negative z. The actual eliminated auxiliary source branch has not supplied that continuation, and the vacuum-first auxiliary order need not yield the same slope. The report keeps this hypothesis explicit.

## Fixed-comoving-k future proof

Let `x=k/(aH)`, `alpha=4mn/(1−2m)`, and `nu^2=n^2/4+alpha`. Differentiating `d=a^(−n/2)Y(x)` with dot x=−Hx gives exactly

`x^2Y''+xY'+(x^2−nu^2)Y=0`.

For real nu>0, the series `Y=x^nu sum c_j x^(2j)` has recurrence `c_j=−c_(j−1)/[4j(j+nu)]`. Its ratio tends to zero at every finite x, so it converges and solves the differential equation, rather than merely being a formal asymptotic expansion. Since c_0=1, the corresponding solution is nonzero sufficiently far in the future and behaves as `d_minus~a^(−n/2−nu)`.

Reduction of order is legitimate on that nonzero tail:

`d_plus=d_minus integral a^(−n)/d_minus^2 dt`.

The integrand is a positive nonzero constant times `a^(2nu)(1+o(1))`; integration gives the nonzero leading behavior `d_plus~a^(nu−n/2)`. Subleading resonant logarithms do not invalidate this leading term. The Wronskian is a nonzero constant times a^(−n). Thus for 0<m<1/2, nu>n/2 and every finite comoving k has a growing solution; its absence is one linear condition on the two initial data of each polarization. This is an exact late-time evolving-mode statement, not a fixed-physical-momentum approximation.

The relative normal-frame traceless extrinsic curvature is dot d/2. Setting the mean tensor to zero gives matter-metric tensor d/2 and its shear dot d/4. The growing mode therefore changes geometric shear. Tiny initial data can remain perturbative over any prescribed finite interval, but no nonlinear endpoint or observational amplitude is proved.

## Complete slope classification in this block

For m<0, define positive mu^2=−alpha H^2. Direct differentiation using the exact evolving equation gives

`dot E=−nH dot d^2−H(k/a)^2d^2`, `E=[dot d^2+((k/a)^2+mu^2)d^2]/2`.

This bounds every future solution. The quoted characteristic exponents have negative real part, with the repeated-root logarithmic qualification correct. At m=0, the exact massless equation has a constant future branch and a decaying branch; boundedness also follows from the nu=n/2 series and reduction-of-order construction. The nonnegative energy at m=0 alone would not directly bound d after momentum redshifts to zero, so the separate solution argument matters.

For m>1/2, the divided equation has positive mass, but its canonical kinetic coefficient q is negative relative to the healthy mean tensor. The report properly distinguishes classical damping from a healthy Hamiltonian. The high-frequency interpretation requires a momentum/rate window within the specified effective theory; no cutoff has been supplied that automatically admits every slope arbitrarily near criticality.

At m=1/2, raw variation instead gives `KnH^2 d/2=0`, up to the overall Euler sign convention. Unsourced relative d is algebraically zero when H≠0. At H=0 that entire quadratic equation vanishes. Neither a propagating ghost nor a consistent nonlinear elimination follows from this degenerate block. The report does not misuse the divided formula at this endpoint.

## Source relation and its limits

The inherited flat NR radial/aligned equations give `y=(1−2m)x` and `g/a0=(1−m)x` on the admitted m<1/2 branch. Hence

`B=(1−m)/(1−2m)`, `m=(B−1)/(2B−1)`, `alpha=4n(B−1)`, and `q=K/[8(2B−1)]`.

Combining the growing characteristic equation with these identities yields exactly `Gamma(Gamma+nH)=4n(B−1)H^2`. These identities were independently checked without numerical fitting. For m≤0 the range is 1/2<B≤1, with the lower endpoint attained only as m→−infinity. For 0<m<1/2, B>1 and the conditional de Sitter growth rate is positive.

The static map and the expanding-vacuum evolution are distinct limits of the same assumed regular interaction. This is not a derivation of a finite-wavelength de Sitter fifth force, an arbitrary nonspherical QUMOND response, or a directly observed force/lensing relation. Matching their hypotheses requires that the same two-sided regular slope controls the weak radial source branch. Deep MOND is the degenerate slope endpoint, not a regular stable finite boost. No lambda value or vacuum moment is fixed by this screen.

## Executable evidence and first missing arrow

All three current b manifests validate against their recorded inputs and outputs. Main_b is 38/38. Control_mass_b is 37/38, failing the exact nonautonomous operator identity; control_comoving_b is 34/38, failing precisely the four evolving transfer comparisons. The numerical rows use a particular Bessel Y branch at initial p/H=.01 over four e-folds for four n=3 slopes. They corroborate its leading asymptote; they are not a numerical full-constraint cosmology or a universal parameter survey. The general conclusion is supported by the convergent-series/reduction-order proof. Historical a runs are explicitly superseded because of their incorrect SciPy version metadata, not silently overwritten.

The first outstanding implication is an actual regular Lorentzian auxiliary completion (or a correctly analyzed nonlinear critical constraint) admitting this TT block. With that additional premise, the stated slope classification and conditional boost/growth relation follow. Without it, this is a precise conditional repair screen rather than an established instability of the original nonsmooth auxiliary theory.
