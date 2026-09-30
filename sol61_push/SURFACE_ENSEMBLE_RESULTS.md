# What a radius distribution can and cannot restore

Base checkpoint: f9290e8d48ab3f9a6e3702c4c4442121d8ea644d. This extends the closed-support response proved in CLOSED_SURFACE_RESULTS.md, with its checked untwisted-sphere spectrum and assumed quadratic subtraction. It does not change the requested common-theory goal.

## Scoped theorem: fixed finite capacity is insufficient

Consider independent neutral free round-sphere modes with fixed radius R, speed v>0 and finite coupling y>0, and a distribution of these parameters independent of polarization magnitude P. Define the positive polarization gap g=v/(yR). Let dA be area per physical volume and let the capacity measure be the push-forward

dC(g) = [nu y^3/(6pi v^2)] dA.

Assume C_total is finite. This is stronger and more precise than finite area alone when speeds or couplings vary. With x=P/g, define q(x)=3F(x)/x^3 using the preceding convergent spectral sum. The energy density is

E(P)=P^3 integral q(P/g) dC(g).

For a formal infinite-radius planar sector with v,y positive, define q(P/0)=1. This is an explicit extension by the planar thermodynamic limit, not a claim that every zero mode has a planar response. Magnetic zero modes or zero-speed singularities are different models.

To bound q, write F(x)=x^2 sum h(n/x), where h(t)=1/[2(sqrt(1+t^2)+t)^2]. The function is positive and decreasing, and integral_0^infinity h(t)dt=1/3. Right-endpoint Riemann sums imply 0<q(x)<1. The small-x expansion gives q(x)=pi^2 x/16+O(x^3), and the large-x Riemann limit gives q(x)->1.

Every finite-radius member has g>0 and hence q(P/g)->0 as P->0. Dominated convergence with bound one and finite measure C proves

lim_{P->0} E(P)/P^3 = C({0}).

This conclusion also controls the constitutive force rather than just the energy. Direct differentiation gives

F'(x)=x sum [1-n/sqrt(n^2+x^2)],

r(x)=F'(x)/x^2=(1/x) sum phi(n/x),

where phi(t)=1-t/sqrt(1+t^2). It is positive decreasing with integral one, so 0<r(x)<1. At small x, r(x)=pi^2 x/12+O(x^3); at large x it tends to one. Uniform convergence on compact positive-x intervals justifies differentiating the spectral series, and the capacity bound justifies differentiating its ensemble integral. Therefore

lim_{P->0} E'(P)/(3P^2)=C({0}).

Under the earlier assumed critical matching W=P^2/2+4pi G E(P), b=g_field-P=4pi G E'(P). The asymptotic MOND coefficient is consequently

lim b/P^2 = 12pi G C({0}).

For a fixed finite-capacity ensemble entirely made of finite round spheres, this coefficient is zero. Unbounded radii with no planar atom do not change the conclusion. A planar fraction with capacity fraction w>0 retains the coefficient w times the all-planar value. The symbol g in the gap distribution must not be confused with the gravitational field g_field.

This theorem concerns the stated additive free-sphere model. Field-dependent sizes or weights, interactions, different topology, divergent capacity, boundary modes and nonuniform polarization are outside its hypotheses. It neither rules out MOND nor excludes a finite observational window approximating a cubic.

## Heavy tails: exact exponent and coefficient

For fixed v,y and a normalized area-weighted Pareto radius distribution beta R0^beta/R^(1+beta), R>=R0, the gap density is beta g^(beta-1)/g0^beta on 0<g<=g0, g0=v/(yR0). For 0<beta<1 and delta=P/g0,

Q(delta)=E(P)/(C_total P^3)

         = beta delta^beta integral_delta^infinity q(x)x^(-1-beta)dx.

The full Mellin integral converges because q(x) is proportional to x near zero and tends to one at infinity. Its coefficient is

J_beta = integral_0^infinity q(x)x^(-1-beta)dx

       = (3/2) zeta(1+beta) L_beta,

L_beta = 2^(-beta-2) [B((1-beta)/2,1+beta)+B((3-beta)/2,1+beta)].

Proof: substitute the positive stable summand into q, interchange sum and integral by positivity, then set x=nt. The individual integral scales as n^(-1-beta). The remaining integral is integral t^(-beta)/(sqrt(1+t^2)+1)^2 dt. Setting t=2sqrt(z)/(1-z) gives the two beta integrals above. All endpoints are integrable precisely for this beta range.

The first correction is obtained from the already established small-x expansion:

Q(delta) = beta J_beta delta^beta - beta pi^2 delta/[16(1-beta)] + O(delta^3).

The magnitude of the displayed remainder is bounded by beta pi^4 delta^3/[480(3-beta)] for 0<delta<1. Thus the deep energy scales as P^(3+beta), and its constitutive response as P^(2+beta), rather than the exact cubic/quadratic pair. At beta=1 the leading energy is proportional to P^4 log(g0/P); at beta>1 it is quartic with normalized coefficient Q~[pi^2 beta/(16(beta-1))]delta. These last two statements follow by isolating q(x)~pi^2 x/16 at the lower endpoint. Beta=0 is not a normalized Pareto distribution. Taking it to zero while changing the ensemble is different from the small-P limit of one fixed theory.

## Evidence and self-review

The original 18-check run retained at runs/surface_ensemble fails one check: a guessed 2% leading-asymptotic convergence threshold at beta=0.75, delta=1e-6. The exact leading correction there is about 2.302%, so this is a false finite-range expectation, not a discrepancy in the Mellin formula. Inputs and failed evidence remain intact. The corrected run checks the derived first correction and analytic remainder instead; all 24 checks pass. Independent quadrature verifies the beta-function integral for three beta values and the scaling of three individual spectral terms. Six-term alternating integration of the small-x series supplies the remaining finite evaluations and explicit next-term bounds; these do not replace the universal proof.

Self-review verdict for the theorem: proved as written within the fixed additive free-sphere model. The source spectrum and subtraction convention are inherited explicit dependencies; kernel bounds, capacity integrability, limiting exchanges and force differentiation are given above. Physical identification of the ensemble, its fixed weights, microscopic neutrality and a common gravitational action are not established. In particular this is not an independently refereed physical theory.

## Consequence for the actual 32pi program

A radius distribution around a cosmological length does not by itself supply the exact deep cubic. Within this route, a viable asymptotic response needs a planar gapless contribution of nonzero capacity, or a different mechanism that invalidates the fixed independent-sphere hypotheses. Merely adding larger closed surfaces cannot do it. The required capacity still contains unselected speed, coupling and area density. It has no derived relation to covariant vacuum stress or Lambda.

The next common-action test should focus on a genuinely extended gapless medium (or explicitly dynamical geometry), and calculate its state-selection and vacuum stress together. Finite closed support remains a possible finite-window approximation; it is closed as the sole exact asymptotic mechanism under the theorem's hypotheses. The original goal and the distinction between the geometric horizon and density length remain open.
