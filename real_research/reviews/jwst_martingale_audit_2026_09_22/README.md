# Escape-delay angular audit, 2026-09-22

Independent Codex audit of Qwen b5a51a5e743042349b1cf6aa630f9efc.
Its declared success compared inserted coefficients with themselves and set the
negative result to False. The actual Thomson integral refutes both coefficients.
No new physical law, novelty, or observed JWST result is asserted here.

For mu=u dot u', the normalized density is 3(1+mu^2)/8 on [-1,1].
Its first moment vanishes and its second moment is 2/5. Consequently

    E[u' u'^T | u] = (3/10) Id + (1/10) u u^T
    E[(x dot (u'-u))^2 | x,u] = (3/10) r^2 + (11/10) z^2,

where z=x dot u. Direct parallel and perpendicular integrations agree.
The isotropic comparison is r^2/3+z^2, not r^2/3+4z^2/3.
The first audit run caught that latter mistake in the audit's own expectation;
`certified/` preserves the failed run. Its input hash is historical and no
longer matches the corrected script. `certified_v2/` is the successful current
run with twelve checks; its manifest validates against the current source.
For the rejected Qwen polynomial 3(r^2+z^2)/8, the exact residuals at unit
perpendicular and parallel orientations are -3/40 and 13/20, respectively.
The kernel perturbation uses the same residual, with both kernels normalized.

## Stochastic reduction, separate from the executable angular checks

In the contract's conservative, central-source unit sphere, put
I(r)=integral_0^r s kappa(s) ds and f=2I(r)+2z. Streaming contributes
2 kappa(r) z+2 and scattering contributes -2 kappa(r) z, hence Lf=2.
M_t=f(X_(t wedge T),U_(t wedge T))-2(t wedge T) starts at zero.
Its jump is 2x dot (u'-u), so its predictable bracket is the time integral
of 4 kappa(r)[3r^2/10+11z^2/10], not merely that polynomial times kappa.
At exit, M_T=2I(1)-2D. Thus the factor four cancels when passing from the
martingale's second moment to Var(D).

For K=sup kappa<infinity, from any surviving state the no-collision exit
probability within time 2 is at least p=exp(-2K)>0. The Markov property gives
P(T>2n)<=(1-p)^n, hence all positive moments of T are finite. Bounded f and
finite E[T^2] allow M_(t wedge T) -> M_T in L2; the bracket is bounded by a
constant times T and converges in L1. Applying bounded-time martingale
isometry and taking limits yields

    Var(D) = E integral_0^T kappa(r_t)[3r_t^2/10+11z_t^2/10] dt.

This is a manually derived occupation identity under the specified model,
not a numerically independently validated transport result. The script proves
only its angular leaf. The identity leaves unknown path occupation averages;
it is not yet a profile-only prediction or a claimed novel equation.

## Next Qwen task

Keep this same route and stop guessing angular constants. Derive a usable
profile relation or a controlled bound for the remaining occupation averages.
One explicit route is the backward second-moment problem: remaining delay is
future travel time minus exit z; m(x,u)=I(1)-I(r)-z satisfies Lm=-1 and outgoing
boundary m=-z. Its raw second moment w obeys Lw=-2m with outgoing boundary
w=z^2. At the central source Var(D)=w(0,u)-I(1)^2.
Check this reduction, retain the boundary angular dependence, then solve or
bound it. A radial ansatz must be derived, not assumed. A failed polynomial
ansatz excludes only that ansatz. Preserve any open angular hierarchy.

Independent continuous-flight/path-integral verification and a primary-source
novelty search are still outstanding before any promotion. No literature claim
was made in this audit. Existing mean-delay identities are benchmarks.
