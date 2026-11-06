# Fed-layer nonactivation with a merely bounded positive clock speed

This extends PF11's continuous-clock-speed step, not its other hypotheses.
Let s be proper interface time, a positive C1 area with local upper/lower bounds,
and phi_Sigma a strictly increasing bi-Lipschitz clock. Its derivative v exists
almost everywhere and satisfies 0<vmin<=v<=vmax. Retain the regular matched
outer tangential identities almost everywhere, convergent integrable side
fluxes, and the Israel/outer-Codazzi surface energy law. These are independent
conditions; they do not follow merely from a bi-Lipschitz clock.

Let q denote the PF11 slice charge composed with phi_Sigma(s), y=a sigma, and
f=[T(N,T)]. The native measure and balance identities give

    q=2y/v a.e.,    q>=0,
    q'=a f/v,    y'=a f-(a'/(2a))y.

The clock change is bi-Lipschitz, so its composition preserves absolute
continuity of the limiting charge. The energy equation makes y absolutely
continuous as well. Choose their continuous representatives. Since v has a
positive lower bound, y>=0 everywhere.

On an open connected component I of {q>0}, define v_rep=2y/q. Locally on I,
it is absolutely continuous, agrees with v almost everywhere and inherits its
positive upper/lower bounds. The smooth PF11 calculation is valid almost
everywhere using v_rep, yielding

    q/(v_rep sqrt(a))=constant C_I >=0.

If I has a left endpoint s1 with q(s1)=0, a positive constant would give
q>=C_I vmin sqrt(amin)>0 almost everywhere approaching s1, contradicting
continuity of q. Therefore no such positive component exists. If q(s0)=0,
all hypothetical positive components have a left zero endpoint (possibly s0).
Thus q=y=sigma=0 throughout the connected interval.

Discontinuity or lack of a derivative bound for the positive clock speed alone
cannot activate a fed sheet. This statement does not establish the required
outer flux convergence or jump identities for a general BV weak solution.
It also does not cover clocks whose speed tends to zero or infinity, singular
source measures at birth, nonmatching polarization traces, or singular geometry.
