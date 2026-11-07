# Conditional temporal regularity of an actual native weak solution

This lemma uses the native on-branch equations, not a prescribed-source model.
It is an a priori statement for an existing solution; it constructs none.

## Hypotheses

Work on a fixed conformal cylinder (0,T) times a periodic spatial circle.
Assume the PF13 bounded weak class: phi,A,Pi are jointly Lipschitz,
p=d phi is spacetime BV, g is C1 with the stated curvature regularity,
and all states stay in a compact on-branch subluminal hyperbolic neighborhood.
In particular the Legendre inversion in PF13 is uniformly regular.
Constants below depend on these bounds, including the auxiliary Lipschitz
norms. They are not estimates deriving those norms from initial data.

Set U=(m,b), b=phi_x and m=exp(2 beta) h phi_t/r. The exact equations are

    partial_t U + partial_x f(U,A,alpha,beta) = (S,0),
    f=(K^x,-phi_t),
    S=A_t Pi_x-A_x Pi_t-E(V_phi+W_phi).

The right side is bounded under the hypotheses. The local inverse for phi_t
makes f continuously differentiable with bounded derivatives on the compact
state neighborhood. A,alpha,beta have bounded spatial derivatives. For almost
every time, the BV composition estimate on that slice therefore gives

    TV_x f(t) <= C TV_x U(t)+C.

Spacetime BV implies that TV_x U(t) is integrable in time.

## Conclusion and proof

There is an L1-continuous representative of U with, for all interior s<t,

    ||U(t)-U(s)||_L1 <= C integral_s^t [1+TV_x U(tau)] d tau.       (1)

To see this without assuming a differentiable characteristic flow, pair the
balance equation with a smooth spatial test vector psi of supremum norm at
most one. Its time pairing is absolutely continuous: its derivative is the
pairing of -D_x f+(S,0) dx with psi, bounded by TV_x f+||S||_L1. Integrate
between Lebesgue times s,t and take the supremum over such psi to obtain (1).
The right side has a common integrable majorant independent of psi. It makes
U(t) Cauchy in L1 as Lebesgue times approach any time; completeness of L1
defines the continuous representative and extends the inequality to all s,t.
This is metric absolute continuity in L1, not a claim of an L1-valued strong
time derivative. If ess sup_t TV_x U(t) is finite, the representative is
Lipschitz in L1. The same argument gives one-sided endpoint traces whenever
the bounds are integrable up to the endpoints.

More locally the equation implies

    |D_t U|(I times circle) <= C integral_I [1+TV_x U(t)] dt.

Thus the time projection of |D_t U| is absolutely continuous with respect
to dt. In particular there is no derivative mass on a null set of times
crossed with the whole circle. A time-only Cantor reparametrization that
produces such mass cannot solve these equations in this class.

## What this does not settle

A spacetime Cantor derivative can have absolutely continuous time projection.
For example translating a spatial Cantor staircase at constant speed has
exactly this property. That example illustrates the measure geometry only;
it is not an AC2q solution. Equation (1) therefore does not exclude native
Cantor variation along acoustic directions, nor continuous unbounded gradients.

For two solutions, the corresponding difference estimate involves
TV_x(f(U_1,A_1,g_1)-f(U_2,A_2,g_2)) and the difference of the native Jacobian
sources. Neither is bounded here by C||U_1-U_2||_L1. Applying (1) separately
to each solution does not yield a uniqueness estimate.

No uniform outgoing TV bound, auxiliary Lipschitz bound, curvature bound,
compactness of an approximation, or preservation of all constraints is
constructed by this lemma. It strengthens the necessary regularity of any
solution already in the bounded weak class; it is not the requested dynamical
existence theorem and does not establish that an extension is necessary.
