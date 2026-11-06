# Coupled abundance and temperature feedback

## Exact outcome

A phenomenological global feedback law can stabilize both a halo density
amplitude and its temperature while preserving v_flat^4 proportional to Mb.
A Lyapunov calculation proves a unique attracting state for the positive
variables in that reduced model. This is stronger than finding a steady state.
However the abundance law is postulated, not derived from the earlier scalar
interaction. The normalization still depends on independent microphysical
coefficients, and a finite total pool mass still needs a boundary. No 1/2 is
derived, and no full galaxy attractor or microscopic theory is established.

Base: b101d584e9. Contracts frozen in 15d32f223e and 8167706e3c. Only the
present investigation is changed. The model is not an adopted action.

## 1. Why simple local reactions do not solve the previous marginal mode

Retain linear cooling and local flux F=L/(4 pi r^2), with positive constants:

    T_dot=a F-b n T,
    n_dot=K F^s T^u n^v-D T^w n^z.

Define d=z-v>0 and h=u-w. At positive equilibrium,

    n T=(a/b)F,
    n^d=(K/D) F^s T^h.

Eliminating n gives

    T^(d+h)=(a/b)^d (D/K) F^(d-s).

For a constant-temperature outer halo, with n proportional to 1/r^2 and F
proportional to 1/r^2 over a radial interval, one needs s=d within this
power-law rate family. If d+h is nonzero, the equations then select a fixed
T independent of luminosity. Combined with hydrostatic v_flat^2=2 kB T/m,
this does not yield a continuous baryonic mass-speed family with fixed
microscopic parameters. If d+h=0, the chemical condition is either incompatible
with thermal balance or duplicates it. In the compatible case it does not
select an additional equilibrium variable.

This can be seen directly in the coupled linear modes. Let x=delta n/n*,
y=delta T/T*, A>0 be the thermal rate, and B>0 the source rate per particle.
Allow an extra term -eta(T/n)n_dot in T_dot to parameterize energy changes
from number exchange. The Jacobian is

    J = [ -d B,           h B          ]
        [ -A+eta d B,    -A-eta h B    ],
    det J=A B(d+h).

In the scaling-compatible case h=-d, a zero mode remains for any eta. This
obstruction is restricted to the stated local power-law chemistry, fixed
coefficients, linear cooling and constant-temperature tail. It does not cover
nonlocal gravitational feedback, transport, density-dependent opacity or all
possible reaction networks. Even the eta parameterization is not a complete
reaction-energy budget: energy carried by injected and removed particles must
be derived in a physical implementation.

### Two explicit examples

A source plus decay, n_dot=1-n and T_dot=1-nT, stabilizes both variables at
(1,1). In dimensional form n_dot=kF-gamma n gives n*=kF/gamma and
T*=a gamma/(b k), the same temperature for all luminosities. It solves local
relaxation but not the requested hydrostatic galaxy scaling.

A scaling-compatible example is

    n_dot=n(1-nT),  T_dot=1-nT.

It conserves ln(n)-T exactly. Its equilibria satisfy nT=1 but retain the
initial invariant. Four numerical initial states converge to different final
states, including approximately (0.61564,1.62434) and (1.05119,0.95131).
States (2,0.5) and (0.5,2) are already distinct equilibria. This explicitly
exhibits abundance/temperature memory despite exact heating-cooling balance.
These examples are dimensionless rate equations, not derived particle reactions.

## 2. A constructive global feedback law

The local obstruction motivates a different construction: let feedback respond
to the gravitational state of the whole halo. Introduce

    X=v_h^2,                   Theta=2 kB T/m,
    B_heat=2 G kB sigma_abs/Lambda_1,
    S=B_heat L.

Here v_h is the speed associated with the density amplitude of an outer
isothermal-shaped material halo,

    rho_p(r)=X/(4 pi G r^2).

During this reduced calculation the profile is assumed homologous: one
amplitude X describes it, while transport maintaining that shape is not solved.
The previous heating/cooling derivation motivates the thermal product condition
X Theta=S. Hydrostatic equilibrium requires Theta=X.

Postulate the coupled global dynamics

    X_dot=gamma(Theta-X),
    Theta_dot=epsilon(S-X Theta),       gamma,epsilon>0.

The first equation increases halo amplitude when thermal support exceeds the
current gravitational amplitude, and decreases it in the opposite case. It
is an explicitly engineered phenomenological source/exchange feedback, not
a consequence of gravity or escape alone. In particular hotter unbound matter
can escape rather than increase pool mass. Realizing this sign requires an
actual production, capture or reservoir mechanism. The previous two-scalar
model has not supplied one.

The second equation keeps the linear cooling/heating product relation. A single
epsilon assumes an effective global thermal timescale; the local heating rate
varies with radius, so homogenization/transport is an additional assumption.
Neither equation is claimed as a complete mass- and energy-conserving halo
initial-value problem. Nonetheless their attractor can be tested exactly.

### Unique equilibrium and proof of history erasure

For fixed L>0,

    X*=Theta*=sqrt(S).

Let x=X/sqrt(S), y=Theta/sqrt(S), a=gamma and b=epsilon sqrt(S). Then

    x_dot=a(y-x),   y_dot=b(1-xy).

For all x,y>0 define

    V=b(x-1)^2/(2a)+(y-1)^2/2.

Direct differentiation gives the exact identity

    V_dot=-b[(x-1)^2+x(y-1)^2] <= 0.

The positive quadrant is forward invariant; on x=0 the vector field points
inward for y>0, and on y=0 it points inward. V bounds both variables, so
solutions remain bounded and cannot blow up. Its derivative vanishes only
at (1,1) in the nonnegative quadrant. The standard invariant-set argument
therefore gives convergence to (1,1) for every positive initial state in this
model. This is a global result for these two ODEs, not just linear stability.
The linear trace is -(a+b)<0 and determinant 2ab>0 as a separate check.

Four widely separated initial states also converge numerically to (1,1).
The numerical checks confirm the implementation; the analytic identity is
what establishes the unrestricted positive-state result for this model.

## 3. The rotation scaling survives, but the normalization is still free

At the attracting state,

    v_h^4=X*^2=S=B_heat L.

If L=ell Mb, then

    v_h^4=G Mb [2 kB sigma_abs ell/Lambda_1],
    kappa=2 kB sigma_abs ell/[Lambda_1 c sqrt(G rho_DE)].

Thus adding this global feedback does not spoil the previously conditional
baryonic fourth-power scaling. No MOND coefficient was inserted in the ODEs.
But gamma and epsilon only affect relaxation; they do not fix B_heat or ell.
Stability therefore cannot determine the 1/2. Positive rescaling of B_heat
changes the final normalization while retaining the same Lyapunov proof.
The conditional L proportional to Mb relation and linear cooling law remain
unproved physical assumptions, especially across different stellar populations.

The displayed outer density shape gives a flat halo speed by construction of
the homologous reduction, motivated by the earlier equilibrium derivation.
No inner rotation curve, disk geometry, radial stability or observed dataset
was solved here. A two-variable global attractor is not a galaxy-wide attractor.

## 4. Total mass and pressure still need a boundary and a supply

At fixed outer radius R, Mp approximately X R/G for the ideal halo tail, so
convergence of X gives convergence of total mass under that fixed-boundary
assumption. Core corrections and central baryonic gravity have been omitted.
If instead an independently specified positive phase pressure Pext sets the
boundary, pressure matching gives

    R*=X*/sqrt(8 pi G Pext),
    Mp*=S/[G sqrt(8 pi G Pext)].

Consequently a specified pressure plus the proposed amplitude attractor selects
a conditional mass proportional to L (and to Mb if L=ell Mb). But the pressure
was supplied, not predicted. A phenomenological wall relaxation

    R_dot=zeta[X^2/(8 pi G R^2)-Pext], zeta>0,

has a restoring radius derivative at equilibrium. Because the X,Theta system
above is independent of R, adding this radius equation is locally triangular
and stable at fixed Pext. This is an analytic extension, not part of the
numerical experiment. It omits wall inertia, phase kinetics and feedback of
radius on thermal rates, so it is not a derived physical boundary law.

Inventory accounting makes the missing mechanism concrete. With homologous
radial flow u=(R_dot/R)r and n=X/(4 pi G m r^2), continuity requires

    partial_t n+div(n u)=J,
    J=n[X_dot/X+R_dot/R].

The postulated feedback therefore needs a particle source or sink with this
specific dependence on the global halo state. Its rest-mass energy, reaction
products, reservoir supply and transport must be accounted for. Heating or
collisional cooling by itself is not that source. Nor does positive external
vacuum pressure follow from adding a restoring wall equation: the phase-energy
difference remains independent of absolute cosmological vacuum energy, as
shown in earlier results.

The earlier halo-dominance consistency constraint also remains: assigning
Pext=rho_DE c^2 and forcing kappa=1/2 would give Mp/Mb about0.10 in this
ideal tail formula, invalidating its halo-dominated approximation at the edge.
This diagnostic is not used as an input or a claimed successful solution.

## Evidence and interpretation

coupled_feedback.py passes42 checks covering exact Jacobian/invariant/Lyapunov
identities and twelve ODE trajectories. The negative control omits h from
the determinant and fails its two intended symbolic checks. Both manifests
are retained and validated. The proof is self-reviewed, not independently
reviewed. Mathematical attractor validity is distinguished from physical
realizability throughout.

Related literature search returned dissipative halo studies such as
[Foot, The steady state solution](https://arxiv.org/abs/1707.02528), which
consider heating/cooling and hydrostatic equilibrium. The abstract was checked
for context only; it does not establish our postulated abundance feedback or
its coefficient. No novelty claim is made for general dissipative feedback.

Disposition: a stable global reduced feedback preserving the scaling has been
constructed and proved conditionally. The restricted local power-law failure
has also been derived. The physical task is still open: derive the global
source sign and normalization from an energy-conserving microscopic reaction,
with sufficient rates and supply, rather than imposing the desired equilibrium
relation as a relaxation law. The sigma/chi action currently lacks that source.
Even a successful source derivation must also link B_heat and the phase pressure
to rho_DE. More trajectory integrations cannot establish either identity.
This is neither a completed pool theory nor a no-go theorem for all such theories.
