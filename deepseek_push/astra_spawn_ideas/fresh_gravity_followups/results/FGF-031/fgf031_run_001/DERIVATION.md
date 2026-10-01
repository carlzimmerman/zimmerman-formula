# FGF031: one uniform robustness neighborhood

This argument was fixed before reading any new stage19 proof or audit. Hold
the saved FGF029 response [U,c] of size15x16, target [L,0], sixteen pressure
nodes, fifteen annuli, fixed offset and support6. Interpret its binary64
coefficients exactly as rationals. New uncertain coefficients themselves
may be arbitrary real numbers satisfying the bounds below.

Define ||M||_infinity,ind=max_i sum_j |M_ij|, vector infinity norm=max_i |v_i|,
and row-target norm l=||L||_1. Induced matrix norm is not maximum entry norm.
Let h=U^-1 c, kappa=||U^-1||_infinity,ind, H=||h||_infinity and mu=-L h>0.
For an absolute radius delta assume

    ||E||_infinity,ind <= delta,   ||e||_infinity <= delta.

U entries and c entries are Compton-y response per normalized pressure
coefficient; these are unscaled absolute response bounds. The combined
entrywise sufficient alternative is max(|E_ij|,|e_i|)<=delta/15. It implies
the induced E bound and a stronger-than-required e bound. No measured error
budget is asserted for either version.

If kappa delta<1, the geometric series for (I+U^-1 E)^-1 converges in the
induced norm. Thus U+E is invertible and

    ||(U+E)^-1||_infinity,ind <= kappa/(1-kappa delta),
    h_E=(U+E)^-1(c+e),
    h_E-h=(U+E)^-1(e-Eh),
    ||h_E-h||_infinity <= r(delta)
       :=kappa delta(1+H)/(1-kappa delta),
    |mu_E-mu| <= l r(delta),       mu_E=-L h_E.

Choose just one explicit rational radius

    delta_safe=min(1/(4kappa), mu/[4kappa l(1+H)]).

Then kappa delta_safe<=1/4 and r(delta_safe)<=mu/(3l), so
mu_E>=2mu/3>0 for every allowed real E,e. The uncertain extended response
has the null vector n_E=(-h_E,1), and its target response is mu_E. Its row
rank is15 and target-augmented rank16 throughout this mathematical neighborhood.
This establishes uniform non-identification, not a statistical sensitivity
estimate or a statement that instrumental errors lie inside the neighborhood.

Use the saved strictly decreasing positive baseline p0 from FGF029, with
fixed zero endpoint p0_16=0. Let m0=min_i(p0_i-p0_(i+1))>0 and
V=max(1,H+r(delta_safe)). Then ||n_E||_infinity<=V and every consecutive
null gap, including the last gap to the fixed endpoint, is bounded by2V.
The common positive step

    eta=m0/(4V)

therefore makes p0+/-eta n_E strictly decreasing and positive, with every
gap at least m0/2. Their common synthetic data are [U+E,c+e]p0, separately
for each allowed operator, and their target separation is
2eta mu_E>=4eta mu/3>0. The uniform step is common; the null direction and
synthetic data vary with the operator. No single pair or observed-data vector
is asserted to work unchanged for every uncertain response.

Zero-error control: exact inversion recovers the pinned FGF029 mu and null
direction, and the common-step witnesses satisfy its exact data equations.
As a threshold control, define

    delta_threshold=mu/[kappa(l(1+H)+mu)].

At this radius the bound l r(delta_threshold)=mu reaches zero margin, while
kappa delta_threshold<1. The sufficient nonzero-target certificate is then
inconclusive; it does not establish restored identification. Indeed E=e=0
is still a member of that larger uncertainty set and remains ambiguous.
No parameter scan or uncertainty sampling is used.

Exact rational inversion and inequalities verify one finite source matrix
and these constants. Uniform validity for all real perturbations follows
from the displayed norm argument, not from enumerating perturbations. No
additional pressure support or annular rows are constructed. This finite
robustness route stops after the certificate; actual calibration/response
error bounds and a scalar outer-pressure datum sensitive to the null mode
remain independent empirical obligations.

No mass/force calculation is made. Later source inference preserves both
a0=9.3619e-11 and1.1279e-10 m/s², separate constant-vacuum/H histories,
Q/RAR/registered M, density and total/electron-pressure conversion. This
does not authenticate a physical metric or close the gravity theory.

One bounded deterministic run:120s wall,110s CPU, cooperative one-library
thread,1MiB logs, no memory cap. Exact checks use tolerance zero. Failures
are retained; no computation of actual instrumental errors is attempted.
