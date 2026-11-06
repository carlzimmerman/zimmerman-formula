# Independent audit: incoming traces at the first packet breakdown

**Verdict: the compact prebreak estimates give unique terminal traces in
the classes described below. They do not propagate the PF11 thin-shell
hypotheses through breakdown or construct a postbreak solution.** Fix one
of the sufficiently narrow packets covered by the PF09 result and its
first strong-evolution endpoint tau_*. All statements are incoming limits.

Inputs read: PF09 `COMPACT_BOOTSTRAP.md`, SHA256
`fde8900442d8517469f55e13ac6e1bb3757f497495a6d7cd40e233cfe1705f5a`,
and PF08 `principal_review/RIEMANN_SOURCES.md`, SHA256
`a91513dae48b6f1e498e9d1f8afc4e4c42fe4a66a74864ccdfe183fe8c7f9e63`.
Use their verified prebreak compact bootstrap and native equations, not
an assumed postshock theorem. Independent delegated audit, 2026-11-06.

## Incoming compact fields and polarization regularity

The bootstrap bounds r,A,P,theta in a compact strict domain, keeps cap,
clock, hyperbolicity and metric margins positive, and bounds conformal
metric first derivatives. Its variation functional Z stays bounded on
the whole interval up to tau_*. The auxiliary inverse gives bounded
u=nA/r and v_aux=nP/r. These bounds are independent of the diverging
pointwise compression variables a_clock=e log r and K=div_2 n.

The exact spatial equations are

    eA=W_P/r,    eP=D-2P e beta.

Every quantity on their right is bounded in this incoming compact state
set. Together with nA=r u and nP=r v_aux, this bounds both frame
derivatives of A,P. The bounded boost and regular conformal metric convert
them to bounded coordinate derivatives. Hence A,P extend jointly
Lipschitz to the incoming terminal boundary; their values have unique
uniform limits and the cap margin persists. The same conclusion follows
directly in the uniform-arclength clock gauge below.

The clock gradient has bounded coordinate components
phi_t=r exp(alpha) cosh(theta), phi_x=-r exp(alpha) sinh(theta).
In particular phi_t is bounded above and away from zero. Thus phi is
jointly Lipschitz with a unique uniform terminal extension. This does
not assert continuity of its gradient at the terminal boundary.

## Unique BV traces for r and theta

In the fixed periodic uniform-arclength gauge,

    n=r(partial_tau-w partial_x),    e=ell^-1 partial_x,
    ell'/ell=mean(K/r),
    w_x=mean(K/r)-K/r,    mean(w)=0.

Z bounds the proper-slice total variation of r and theta. Since
K=e theta+omega(e) and the connection is bounded, it also bounds
||K||L1; likewise ||a_clock||L1 is bounded by TV(r)/r_min.
The slice length stays bounded above and away from zero. Consequently
ell' and ||w||infinity remain bounded, although w_x need not.

The exact evolution equations give

    n r=-r c^2 K+S,
    n theta=-a_clock-omega(n),

with S uniformly bounded by the auxiliary and geometric estimates.
Thus

    ||r_tau||L1+||theta_tau||L1 <= C,

because partial_tau=n/r+w partial_x and both spatial variations are
bounded. In particular

    ||r(tau2)-r(tau1)||L1+
    ||theta(tau2)-theta(tau1)||L1 <= C |tau2-tau1|.

There are unique L1 terminal traces r_*,theta_*, which belong to BV by
lower semicontinuity of total variation. The compact value/margin bounds
persist almost everywhere. The conclusion is stronger than subsequential
BV compactness, but weaker than uniform convergence or continuous clock
gradient traces. Jumps in these terminal BV traces are not proved to
exist, and the estimates do not forbid them.

Also A_tau=u+w A_x and P_tau=v_aux+w P_x are bounded; their joint
Lipschitz extensions hold in this gauge as well. The bounded clock/conformal
frame and slice-length factors give controlled bi-Lipschitz coordinate
maps up to the terminal boundary. Thus this trace assertion is not based
on an unbounded arbitrary reparametrization of the spatial circle.

## Metric derivatives: what the equations add to boundedness

A uniform bound on first metric derivatives alone would give Lipschitz
metric values and weak derivative compactness, not continuous convergence
of the derivatives. Here the exact conformal wave equations give more.
Their sources contain only compact matter invariants and bounded metric
first derivatives, so the sources F_alpha,F_beta are uniformly bounded.

For either metric scalar z=alpha,beta,

    (partial_t-partial_x)(z_t+z_x)=F_z,
    (partial_t+partial_x)(z_t-z_x)=F_z.

Each null derivative is therefore uniformly Lipschitz along its fixed
null-characteristic label. Before breakdown these derivatives are
continuous. Integration to the terminal boundary makes their values
uniformly Cauchy along each family, with tail bounded by C times the
remaining characteristic time. The terminal clock boundary is a uniformly
spacelike Lipschitz graph: |dt/dx|=|tanh(theta)| stays strictly below one,
and phi_t stays positive. Its intersections with the two null families
vary continuously with the labels. Evaluating a small fixed characteristic
time before those intersections and then taking its uniform limit gives
continuous terminal traces of z_t+z_x and z_t-z_x.

Consequently the conformal metric first derivatives have incoming
continuous terminal traces in this regular chart, not just weak limits.
This uses the semilinear null equations and prebreak continuity in
addition to the bound. It supplies no bound or convergence theorem for
second metric derivatives, and does not make the terminal clock graph
or an unknown future timelike interface a regular Israel hypersurface.

## Currents, initial charge and limitations

The incoming Hilbert stress is uniformly bounded: r,A,P and the unit-clock
boost remain compact, and the prebreak evolution is on branch. The
specified scalar current is uniformly bounded too, because its base part
is algebraic in those fields and its other part uses bounded coordinate
derivatives of Pi=exp(2 beta)P. Thus no incoming stress/current measure
concentration is forced at the first endpoint.

This is not convergence of the current in a regular trace norm.
nP=r v_aux and nA=r u are only bounded by the present estimates; their
temporal limits or continuous tangential traces are not established.
Lipschitz A,P can have derivatives with merely weak limits. In particular
the convergent regular outer side fluxes assumed in PF11 do not follow
from these bounds alone.

At a shrinking clock-slice crossing the incoming compact bound gives

    |Q_epsilon| <= C epsilon.

It therefore supplies zero incoming slice charge wherever a proposed
common approximating layer interval is connected to this controlled
incoming evolution. It does not justify replacing an uncontrolled
postbreak birth corner by such an interval or importing a postbreak
scalar balance without its side-trace convergence.

## Which PF11 assumptions are and are not supplied

The incoming side supplies compact r and boost, cap/source margins,
positive bounded A, regular nondegenerate metric values, controlled
incoming metric first-derivative traces, continuous Lipschitz phi,A,P,
bounded incoming stress/current, and zero shrinking-slice incoming charge.
It also supplies unique incoming L1/BV r,theta traces.

It does not supply a future timelike interface, a smooth approximating
family through breakdown, matching outgoing Pi/A traces, regular common
tangential derivatives along that interface, convergent outgoing side
currents, a positive continuous interface clock speed, postbreak finite
stress measures, Israel/outer Codazzi geometry, or preservation of the
domain margins after breakdown. No outgoing state or entropy/admissibility
condition has been constructed. These are the exact reasons PF11 is a
restricted exclusion theorem rather than an existence or uniqueness
theorem for the terminal BV data.

Follow-up qualification: the separately audited measurable-clock
nonactivation lemma weakens PF11's continuous interface-speed assumption
to a bi-Lipschitz interface clock with positive bounded measurable speed.
Therefore failure of continuity alone does not evade that balance lemma.
It still does not provide the future interface, outgoing trace identities,
side-flux convergence or Israel law missing from the incoming estimates.
