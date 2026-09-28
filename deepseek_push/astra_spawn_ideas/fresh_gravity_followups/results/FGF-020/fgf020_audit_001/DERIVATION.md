# FGF-020 independent proof audit: two integrated density moments

Actual worker: Astra agent `/root/dynamics_precision`, run `fgf020_audit_001`.
This is not a DeepSeek run. This worker did not author DM1. Candidate source
hashes were checked against the FGF-020 snapshot; all five entries matched,
and the verdict applies to those exact bytes. No candidate verdict is used as proof.

Primary verdict: **proved as written**, within DM1's stated idealized
observation model and positive-density assumptions. The argument below also
sharpens the finite-volume feasibility and equality conditions. That extension
is not a correction of DM1, which explicitly labeled its variance bound
necessary and its equal-volume construction sufficient. No new scientific
computation was run: this is the allowed proof-only audit, with source-code
inspection and provenance validation. No literature search or novelty claim.

## 1. State the inverse problem on its actual support

Let (Omega,dP) be a nonatomic probability space representing normalized
three-dimensional volume in a spherical aperture. Density x is measurable,
strictly positive almost everywhere and square-integrable. Fix

    E[x]=mu>0, E[x²]=nu, V=nu-mu², 0<V<mu².

A prescribed shell S has P(S)=epsilon with 0<epsilon<1 and x=L>0 on S.
No smoothness, hydrostatic equilibrium, lower feature width or detector map
is assumed. A density value on a zero-measure boundary alone is unobservable
from these moments; the construction below instead changes a positive-volume
shell. Thus its nonidentifiability is stronger than that trivial exception.

Conditional expectation on the complement determines exactly

    m=E[x | S^c]=(mu-epsilon L)/(1-epsilon),
    v=Var(x | S^c)
      =[V-epsilon(V+(L-mu)²)]/(1-epsilon)².              (F1)

These equations follow from mass and second-moment decomposition, without
assuming how many complementary density levels exist. Rearranging gives the
law of total variance

    V=(1-epsilon)v+epsilon(L-mu)²/(1-epsilon).           (F2)

## 2. Independent constructive proof of unbounded shell density

For any finite L>0, choose a strictly positive epsilon no larger than

    min{1/2, V/[2(V+(L-mu)²)], (mu-sqrt(V))/(2L)}.        (F3)

Every entry is positive under 0<V<mu². Equation (F3) ensures that the numerator
of v is at least V/2>0, while
mu-epsilon L >= (mu+sqrt(V))/2 > sqrt(V).
Consequently m>0 and m²>v. Assign the two equal-volume parts of S^c the
positive densities m-sqrt(v) and m+sqrt(v). Their moments are m and m²+v;
(F1) therefore returns the prescribed mu and nu exactly after adding S.

This proves, constructively and without taking epsilon=0, that every finite
L>0 occurs in a strictly positive piecewise-constant profile with the same
moments. The family has no finite uniform upper bound on its essential
supremum; no claim is made that a single profile has infinite density.
Each target L has its own small but positive epsilon.

For a spherical aperture of radius R, take the shell between
R(1-epsilon)^(1/3) and R. Split its complement at
R[(1-epsilon)/2]^(1/3). These radii realize precisely the three required
volume fractions. This verifies the geometry without interchanging a radial
length fraction and a volume fraction. At large L, the variance ceiling
scales as epsilon=O(L^(-2)); shell thickness is approximately R epsilon/3
when epsilon is small. No independently justified minimum thickness is present.

DM1's continuity argument is valid; (F3) merely supplies an explicit version
of its sufficiently small epsilon choice.

## 3. Sharp variance condition, positivity and exact sufficiency

Since v>=0, (F1) implies

    epsilon <= V/[V+(L-mu)²].                            (F4)

For L=mu this says only epsilon<=1, while the original domain still requires
epsilon<1. It cannot turn the entire aperture into a constant-density region
when V>0. No extra case is hidden in division by L-mu.

Strict positivity of the complementary density independently requires

    epsilon L < mu.                                     (F5)

Together, (F4), (F5), 0<epsilon<1 and L>0 are **necessary and sufficient**
for a positive measurable profile with these moments on a nonatomic aperture.
To prove sufficiency, (F1) gives m>0 and v>=0. If v=0, use constant density m
on S^c. If v>0, use the two positive complementary levels

    ell=m/2, h=m+2v/m,
    P(ell | S^c)=4v/(m²+4v),
    P(h | S^c)=m²/(m²+4v).                              (F6)

Both probabilities are positive, sum to one, and give conditional mean m and
variance v. The nonatomic volume permits regions with those fractions. The
weights need not be equal; this extends DM1's equal-volume example rather
than declaring it defective. It also handles fixed epsilon cases where v>=m²
and the equal-weight lower level would fail positivity.

The variance ceiling alone is the strongest necessary condition available
from nonnegative complementary variance. It is not the complete positive
feasibility condition unless (F5) is also imposed. DM1 already warns that its
variance bound need not suffice once positivity is required.

At variance equality with L!=mu, the complement is constant and

    m=(mu L-nu)/(L-mu).                                 (F7)

If L<mu, this m is positive. If L>mu, positivity requires L>nu/mu. At
L=nu/mu the complement would have density zero and strict positivity fails.
For mu<L<nu/mu, the positive-mass ceiling epsilon<mu/L is stricter than (F4).
These endpoint distinctions matter if a finite-width claim saturates a bound.

If the shell is independently known to occupy at least epsilon_min>0, (F4)
gives the correct necessary interval

    |L-mu| <= sqrt[V(1-epsilon_min)/epsilon_min].         (F8)

In addition, strict positivity gives L<mu/epsilon_min. The first bound remains
valid as stated in DM1; a complete feasibility claim must retain the second.
An instrumental PSF width measures the response to a source, not a physical
lower width for the source itself. Applying epsilon_min from a PSF without a
source-regularity or thickness premise would be an unsupported extra step.

## 4. Equality and degenerate controls

If V=0, the nonnegative integrand (x-mu)² has zero mean, so x=mu almost
everywhere. Any L!=mu on a positive-volume shell is impossible. If L=mu,
the whole complement must also equal mu almost everywhere; any 0<epsilon<1
is then permitted. Integral data alone still do not constrain exceptional
zero-measure points without continuity or other regularity.

Negative V would violate the variance identity and describes no real profile.
The stated domain excludes mu=0, which is also incompatible with strictly
positive density on a unit-volume aperture. DM1's assumption V<mu² is a
sufficient margin for equal-weight positive bulk levels; the more general
positive realization (F6) does not need that upper inequality once m>0 and
v>=0 are supplied. No larger-domain conclusion is needed for the task.

## 5. Audit of the actual rational experiment

The candidate fixes mu=3/2 and nu=5/2, so V=1/4. Its code chooses

    epsilon=min{1/1000, V/[10(V+(L-mu)²)], mu/(10L)}.

For this fixed pair and any finite L>0, epsilon>0 and epsilon<1. The variance
numerator is at least 9V/10>0. Also mu-epsilon L>=9mu/10, whose square is
81mu²/100>V. Therefore its exact `mean > 0` and `mean*mean > var` tests are
justified for the seven displayed rational targets and all eight positive
force-derived rationalized targets. This is a proof about its actual input
pair, not a claim that the chosen epsilon recipe works for all possible
mu,V arbitrarily close to V=mu².

The mass and emission expressions checked in the code simplify symbolically
to mu and nu through (F1). `Fraction` represents epsilon,m,v and the moment
identities exactly. The actual complementary densities m +/-sqrt(v) need
not be rational; they are exact real algebraic values specified by m and v.
Their floating square roots are display-only, and positivity is checked
without those roots through m>0 and m²>v. Calling the parameter calculation
rational must not be inflated into a claim that all three density levels are
rational numbers.

The controls have the intended sign: exceeding (F4) makes v<0; V=0 with a
different positive-volume shell also gives v<0; leaving the bulk at mean mu
while replacing a shell by L changes mass by epsilon(L-mu). The displayed
L=10, epsilon=1/1000 frozen-bulk difference is exactly 17/2000. Those are
mathematical negative controls, not physical exclusions of measured clusters.

The eight force-derived targets are first computed in binary64, then
`Fraction.from_float(L)` preserves exactly that represented float. It does
not make the square root/exponential force calculation exact. The reported
force-restoration check is algebraic recovery of the declared synthetic inputs,
not an observed residual or a confidence interval. The source code uses the
correct Q/R formulas separately, both a0 values, and a distinct frozen E(3)
comparison. No candidate code was rerun during this proof-only audit.

## 6. The idealized emission moment is not detector-count conservation

With fixed composition, an actual optically thin emission map would still
have an energy-, temperature-, abundance- and position-dependent weight.
Schematically the count in channel/bin j depends on

    C_j = integral dV dE R_j(E,position)
                      rho² Lambda_E(T,Z,composition,...),           (F9)

including geometry, projection and detector response in the stated weights.
This is a description of the missing map, not a calibrated plasma model.
Two unweighted volume moments do not fix all such weighted functionals.
Even with composition fixed, holding thermal pressure P while changing rho
changes ideal-gas temperature as T proportional to P/rho. Thus the emissivity
coefficient generally changes with the proposed density redistribution.

An elementary logical counterexample makes the missing assumption precise.
For a purely illustrative positive coefficient Lambda(T) proportional to 1/T
at uniform pressure, the integrated functional in (F9) becomes proportional
to E[x³], which the first two moments do not fix. This is not asserted to be
an actual cluster emissivity law. For the symmetric baseline levels 1 and 2
with equal weights, mu=3/2, V=1/4 and the third central moment is zero. For
DM1's L=10 witness, put delta=L-mu=17/2. Its third central moment is

    epsilon delta [(1+epsilon)delta²-3(1-epsilon)V]
       /(1-epsilon)² > 0.                              (F10)

The bracket is positive because delta²=289/4>3V=3/4. Both profiles preserve
the first two moments but change that response functional. Hence detector
counts cannot be universally inferred to be preserved without supplying and
checking their actual thermal/emissivity/response dependence. A resolved image
or spectrum adds constraints not contained in mu and nu. Conversely the audit
does not claim all possible emissivity functions distinguish the profiles.

## 7. Gravity scope and the registered scale

At a fixed spherical aperture, mu fixes the enclosed gas mass only when the
physical volume and rho_ref are also fixed. With fixed enclosed stellar mass,
B=G(Mgas+Mstar)/R² is then unchanged at that aperture. This does not preserve
the enclosed mass or force at every interior radius. For an inward force
magnitude F(B;a)>0 and a specified outward pressure gradient P'<0, the local
thermal balance requires

    rho_required=(-P')/F(B;a), L=rho_required/rho_ref>0.

Each finite positive L has the moment countermodel above. This remains a
local force compatibility construction, not a radial hydrostatic solution,
pressure profile, temperature fit, smooth interface, lensing fit or cluster
solution. It correctly uses the chosen MOND force rather than a Newtonian
missing-mass surrogate.

The code retains Q=sqrt(B²+aB) and R=B/[1-exp(-sqrt(B/a))] separately at
B=1e-12 m/s², rho_ref=1e-25 kg/m³ and declared |P'|=1e-35 in SI pressure
per length. The scale references 9.3619e-11 and 1.1279e-10 m/s² both appear.
Constant vacuum a=kappa c sqrt(G rho_Lambda) is distinct from the comparison
a=a0 sqrt(.315*4³+.685) at frozen z=3. No dynamical H history or determination
of kappa is obtained. No M branch is numerically tested here; the abstract
moment construction only needs a specified finite positive force and does
not provide nonlocal filtered-field dynamics.

## Verdict, coverage and stopping point

The mathematical nonidentifiability survives attempted falsification. The
strongest gain is the exact positive feasibility region (F4)-(F6), including
its equality restrictions. DM1's narrower sufficient construction is correct.
A scalar emission integral does not remove the density-shape ambiguity and
cannot be promoted to unchanged detector data when the thermal response changes.

Coverage: source-pinned raw derivation, exact arithmetic code logic, all seven
rational and eight rationalized-target construction rules by algebra, equality
cases, spherical volume realization, positivity, finite-width interpretation,
Q/R normalization/history branch handling, and gravity/emissivity scope.
The source manifest was provenance-validated. No new numerical experiment,
full binary64 reproduction, actual detector/plasma evaluation or data fit was
performed; none is fabricated as audit evidence.

Next discriminating implication: supply an independently authenticated spatial
response or physical feature-width constraint, and the actual emissivity map
including the induced temperature change, then ask whether any positive profile
satisfies those additional observations together with the moment and local
force conditions. Until such input exists, the route stops at a mathematically
valid observation-map counterexample rather than a manufactured cluster repair.
