# Independent audit: uniform compact interval for localized packets

**Verdict: proved for the stated small-amplitude periodic planar packet
family, using the audited local strong theory and residual propagation.**
The conformal-coordinate continuation and clock comparison must be read
as part of the improving bootstrap, as detailed below. Together with the
previous exact gradient comparison, this supplies a restricted native
finite-gradient-breakdown result. It supplies no singular continuation.

## Einstein wave signs

For ds_base^2=exp(2alpha)(-dt^2+dx^2), the base trace and transverse
equations give

    beta_tt-beta_xx=exp(2alpha)(rho-p)/(2M)-2beta_t^2+2beta_x^2,
    alpha_tt-alpha_xx=beta_t^2-beta_x^2
                         +exp(2alpha)(p-rho-2p_perp)/(2M).

I independently recover both signs from
tr_base G=2 box(beta)+4(grad beta)^2 and
G_perp=box(beta)+(grad beta)^2-R_base/2. A flat FRW specialization also
has the correct alpha_tt=beta_tt=-exp(2alpha)(rho+3p)/(6M).

The sources contain the rest-frame invariants rho,p,p_perp and first
metric derivatives, not derivatives of matter fields or clock rapidity.
On the compact on-branch r,A,P domain these invariants are bounded. Null
integration therefore gives a first-metric-derivative bound of the form

    M(t)<=M0+C integral_0^t [1+M(s)^2] ds,

with constants independent of packet width. Zeroth metric fields are
controlled by time integration. No separate externally prescribed matter
evolution is assumed; the estimate holds on the portion of the coupled
solution already existing in the bootstrap region.

## Coordinate and clock-time point that must not be omitted

Use conformal initial coordinates on the flat proper initial slice with
alpha=beta constant, alpha_x=beta_x=0 and bounded alpha_t,beta_t determined
by the prescribed bounded K,B. The initially steep r_x is then in the
scalar time derivative, not in an initially unbounded conformal metric
derivative. The regular two-dimensional metric admits these local null
coordinates; periodic normalization fixes their spatial period.

Continue the two null-coordinate families on the existing regular solution.
Same-family characteristics do not cross while the regular coordinate flow
exists. The bootstrap's improving metric and clock-frame bounds prevent
its Jacobian from degenerating before the asserted short interval. The
needed clock identities are explicit:

    phi_t=r exp(alpha)cosh(theta),
    phi_x=-r exp(alpha)sinh(theta),
    phi_t+/-phi_x=r exp(alpha)exp(-/+theta).

Thus all three future derivatives are bounded above and bounded away from
zero on the positive side in the claimed compact neighborhood. Clock and conformal times and
the null coordinate continuation are uniformly comparable there. Past
metric-null segments from a point remain in the earlier clock-time
bootstrap region, so null integration does not assume a larger unknown
solution domain. This supplies the coordinate comparison without any
pointwise bound on r_x.

The argument is a continuation bootstrap of the chart on the already
existing solution, not an assertion that an arbitrary singular Lorentz
metric has regular conformal coordinates. An initial Lipschitz strong
solution is interpreted through its regular constrained frame equations;
the estimates and characteristic maps hold at that finite regularity.

## Coupled variation and amplitude bounds

The proper-clock-slice conservative W_sigma equation in RIEMANN_SOURCES.md
gives

    Z'<=C(1+Z)^2,
    ||u,v||infinity<=C(1+Z).

It also controls slice length through its derivative integral K/r. The
constants depend on compact lower fields and bounded conformal connection,
not on peak a,K. Initial Z is uniformly bounded for a localized packet:
the steep part contributes its O(delta) total variation, not its
O(delta/epsilon) peak derivative.

Along normal clock worldlines A and P change at rates u and v in clock
time. Along acoustic characteristics the exact z_sigma sources, divided
by positive r, are bounded by the same variation and metric estimates.
The map (z_plus,z_minus,A)->(theta,r,A) has a uniformly controlled local
inverse because I_r=1/(r c)>0. Therefore r,A,P,theta remain in the fixed
compact neighborhood for a common sufficiently short time.

These field bounds keep the stress invariants compact, improving the
metric-null estimate. The bounds for alpha,beta and theta in turn control
B,E_beta and the spin connection used in the variation inequality. A
standard first-exit argument closes this finite set of inequalities on
a time T0>0 independent of packet width. This is not an estimate that
assumes the pointwise compressive gradient stays bounded.

## Formation conclusion within the specified subfamily

The audited initial auxiliary solve and ADM data give compatible,
finite-regularity packets of fixed sufficiently small amplitude delta
and arbitrarily small width epsilon. Their lower fields, initial metric
first derivatives and Z0 are uniformly controlled. Their negative
weighted compression is of order delta/epsilon, with bounded positive-
to-negative peak ratio.

The exact weighted gradient equations and maximum comparison yield
breakdown by clock time 2/(a0 q0), where a0>0 is the uniform Riccati
coefficient lower bound. Choose epsilon so this is smaller than T0.
If the native strong evolution terminates sooner, the proved constrained
continuation criterion identifies loss of a,K boundedness: the other
compactness/domain/length controls persist. If it survives, the Riccati
comparison itself forces that loss by the stated upper time.

This proves existence of finite-gradient breakdown for this periodic
planar, constant-V/a0, on-branch, finite-regularity native subfamily. The
blowing variables are a=e(log r) and/or the clock congruence expansion K.
It is not a theorem that every datum breaks, that curvature invariants
must diverge, or that the numerical fixture has a particular blowup time.
Nor does it construct endpoint states of a postbreak corner or select an
entropy/measure continuation. The singular-selection question remains
independent and open.

Independent delegated audit, 2026-11-06, of COMPACT_BOOTSTRAP.md together
with the now-audited local, residual, and exact characteristic estimates.
No numerical trend was used as proof of formation.
