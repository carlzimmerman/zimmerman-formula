# First endpoint turn: independent root derivation

2026-09-30. Candidate conditional theorem for the reviewed Q/R diagnostic
wall slab. Let d*>0 be finite, background smooth through [0,d*], B,rho,g>0,
all coefficients regular and kinetic coefficients positive. Write w=chi',
R=rho q/lambda>0, Jw''=Mw-C R as in FGF025. Assume w>0 on [0,d*) and
w(d*)=0. The original quadratic form has smooth bounded coefficients even
though the weighted representation divides by w. All fields have fixed
Dirichlet perturbations: u=(xi,psi,eta) in H1_0(0,d*)^3.

## 1. The first zero is simple

Left positivity implies w'(d*)<=0. If w'(d*)=0, the background identity
implies w''(d*)=-C R(d*)/J<0. Taylor expansion would give w(d*-h)<0 for
small positive h, contradicting first-zero status. Thus w'(d*)<0 and,
with h=d*-x and a=-w'(d*)>0,

    w=a h+O(h²),   w'/w=-1/h+O(1).

In particular w is comparable to h near the right endpoint. This conclusion
uses strictly positive rho and q; a vanishing source endpoint is outside it.

## 2. Domain and traces, with no extra flux condition

For eta in H1_0, Cauchy-Schwarz from the right trace gives

    |eta(d*-h)|²/h <= integral_(d*-h)^d* |eta'|² ->0.

Also integral eta²/h² <=4 integral eta'². For smooth trace-zero functions
this follows by integrating (eta²/h)' and applying Cauchy-Schwarz; the
nonpositive far-end boundary term may be discarded. Approximation extends
the inequality to H1_0. Consequently (w'/w)eta is in L2 and
w(eta/w)'=eta'-(w'/w)eta is in L2. The singular-looking square is integrable.
The other new term (R/w)(eta+w xi)² is integrable by these estimates and
boundedness of R,w. Finally (w'/w)eta² ->0 at the right endpoint.
There is no new requirement that eta/w itself vanish or remain bounded.

Integrate the FGF025 product-rule identity up to d*-h and let h decrease
to zero. The original energy coefficients are regular; the new squares
are integrable and their extra endpoint term tends to zero. Thus the four-
nonnegative-square expression remains an equality on the full H1_0 domain.
For nonsmooth functions this follows either by the above weak product rule
on truncated intervals or by H1 approximation plus the controlled weights.

## 3. Positivity AND a gap of the original form

Denote the original quadratic form by Q=2V. It is nonnegative. If Q=0,
its fluid derivative square gives xi=0. Then R/w>0 in the interior forces
eta=0, and the potential square forces psi=0. Thus Q is strictly positive
for every nonzero H1_0 triple, but this alone is not taken as coercivity.

The original regular form has uniformly positive diagonal second-derivative
coefficients cs²rho, lambda/C and J/C. Its first-order couplings and zeroth
order terms are bounded. Young inequalities therefore give constants A_G>0,
B_G>=0 with

    Q[u]>=A_G ||u'||²-B_G ||u||².                         (G)

Suppose the
infimum of Q over ||u||_L2=1 were zero. A minimizing sequence is bounded in
H1 by (G), admits a weak H1 and strong L2 convergent subsequence on the finite
interval, and keeps L2 norm1. The principal gradient energy is weakly lower
semicontinuous; bounded lower-order terms converge using strong L2 and weak
derivatives. The limit then has Q<=0, contradicting strict positivity.
Thus Q>=lambda0 ||u||² with lambda0>0 on this fixed interval. Combining
this inequality with (G) yields Q>=c* ||u||_H1² for some c*>0.
No explicit value, uniform-in-parameter bound or numerical spectrum is claimed.
The positive bounded kinetic weights make this a positive longitudinal
squared-frequency gap in the corresponding weighted norm.

## 4. Same full interval slightly beyond the first turn

Assume/continue the same smooth equilibrium IVP to x>d* while B,rho remain
positive. Regular local ODE continuation supplies some such neighborhood.
On intervals [0,d] near d*, rescale x=d y to [0,1]. Use the ORIGINAL form,
not division by w. Its coefficients and the length factors depend uniformly
continuously on d, so the rescaled forms satisfy

    |Q_d[U]-Q_d*[U]| <= epsilon(d) ||U||_H1(0,1)²,
    epsilon(d)->0 as d->d*.

The fixed-domain coercivity at d* therefore survives for sufficiently small
positive d-d*. The same full continued slab is stable in this open length
neighborhood, including w<0 just beyond its first zero. Initial data at the
left wall are held fixed; right-wall field values and pressure are induced
at each length. This is a family of wall problems, not moving-wall evolution
with fixed endpoint data. It does not allow arbitrary continuation beyond
that neighborhood, free boundaries or global isolated-body conclusions.

## 5. Nonempty first-turn family, without a numerical claim

Take fixed B_i,rho_i>0, chi_i=0 and small w_i>0 at the LEFT endpoint.
For the inherited cosh potential, w'(0)=-T(F(B_i,a_ref),a_ref)/J=-k<0,
independent of w_i. Smooth dependence/locally bounded ODE coefficients on
a compact neighborhood of the w_i=0 data gives a uniform short existence
interval on which w'<=-k/2 for sufficiently small positive w_i. Choosing
w_i so that 2w_i/k lies in that interval forces a first zero before that
time; B,rho stay positive. This realizes the endpoint assumptions in the
same left-data class used by FGF023. No length value or larger-domain
example violating the former shortness bound was computed.

## Controls and physical scope

Dropping the extra endpoint term before proving its trace limit is invalid;
requiring eta/w=0 at the first zero would change the domain. Zero rho or q
would invalidate the simplicity argument. Extending the singular weighted
identity naively through an interior negative w is invalid: the continuation
argument uses regular form perturbation and its attained fixed-domain gap.
These are analytic controls, not numerical executions.

All premises are those of the added local Q/R diagnostic action. Source flux
is MOND B'=C rho with g=F(B,a_ref exp chi), not Newtonian missing mass. Both
registered a_ref=9.3619e-11 and 1.1279e-10 m/s² and separate constant-vacuum
versus frozen H reference families remain. Actual a varies and does not
satisfy a literal pointwise constant-vacuum interpretation. No M action,
filtered-MONO metric, photon coupling, 3D/nonlinear or observational result
is supplied. This is a conditional wall-stability theorem, not theory closure.
