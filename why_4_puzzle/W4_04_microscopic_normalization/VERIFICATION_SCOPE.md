# Exact verification scope, before checker implementation

2026-10-20. Supplements the criteria-only commit 1eb877c0d with the explicit
analytical outputs returned by the independent routes. No checker exists yet.
No new candidate or numerical trial is introduced.

Verify PROOF.md A-E: operational amplitude dictionary and field rescaling;
common hbar/species cancellation; canonical BI expansion and fixed-V
gravitino mutation; actual weak-field BI exponent; thermal coefficient
ratios 16/15 and 16/5 with negative cubic; equal common-gamma cancellation;
relative-slope deformation; the five finite-spectrum cancellation sums,
positive induced constants via rational log intervals; and exact stationary
and curvature identities of the displayed KKLT potential.

Positive p'(2),q'(1) certification uses ln(x)=2 sum_(k>=0) z^(2k+1)/(2k+1),
z=(x-1)/(x+1), with 40 terms and an absolute geometric remainder bound
2|z|^81/[81(1-z^2)]. All mass ratios are rational and the resulting interval
arithmetic is exact; decimal values are reporting only, not selection.

The thermal coefficient ratio cancels a COMMON gamma. This is expected,
not a failure of the mutation. Doubling gamma doubles C2 and multiplies
|C3| by 2^(3/2), leaving the formal amplitude ratio invariant. A two-group
relative deformation gamma(1+t),gamma(1-t) keeps the leading thermal vacuum
and quadratic coefficient fixed but changes the cubic unless symmetry
forbids it. Use the single declared example t=3/5 and its analytic convexity
proof, not a parameter scan; then A(t)=9sqrt(10)/25, A(t)^2=162/125.

For the MUTATE run, double the BI probe alpha (squared threshold ratio
quadruples), turn on m32 with 3Mp^2m32^2=V (T: V/2 -> V), and change n=3
to n=4 (amplitude prefactor multiplies by pi/2). Compare to original baseline
identities: each must fail exactly where physics was changed, with nonzero
exit. The common-mediator q rescaling remains invariant by design. The
relative thermal slope example changes its formal coefficient ratio by
125/162 and must also fail its equal-slope baseline. All bookkeeping and
normalization invariance checks should continue to pass.

The spectrum is constructed, its masses and zeta are not selected. Its
zeta=1/4 is a curvature coupling, never the target xi. No conclusion about
positive MOND C3 follows from a determinant exponent or a squared negative
thermal coefficient. Static local identities, free determinant limits and
the leading KKLT EFT are the verification range; full quantum gravity,
loop nonrenormalization, cosmological perturbations and exact flux vacua
remain outside it.
