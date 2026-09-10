# Radiation added to the fixed cubic clock action

Base ebb49936640781e220c7b28ac4369acf36b46711. **Nearby regular expanding
homogeneous radiation branches exist under the stated local nondegeneracy
conditions.** The one-epoch numerical solves below support that construction
at the recorded parameters. This is not radiation-era evolution, perturbation
health, recombination, CMB or full-theory closure.

The action functions remain exactly those in `../cubic_background_completion/`:

    P=P0+3 gamma qbar(tau)Hbar(tau)[X-qbar(tau)^2],
    W=W0-2 gamma qbar(tau)^2 qbar_dot(tau), V=U(tau).

Bars distinguish the fixed reconstructed coefficient history from the new
physical H,Q. In particular, Hbar is never recomputed using radiation.
Signature is -+++, gamma is constant, and M2 denotes M squared. The clock
gauge is tau=t, with arbitrary lapse N; H=alpha_dot/N, Q=chi_dot/N and
alpha=log(a). Dots below denote coordinate tau derivatives unless specified.

## 1. Explicit minimally coupled radiation and its charge

Add S_r=int sqrt(-g) C_r X_r^2, X_r=-grad(r)^2, C_r>0, choosing the
positive homogeneous radiation-velocity branch. In a unit comoving cell,

    L_r=C_r a^3 r_dot^4/N^3,
    p_r=4 C_r a^3(r_dot/N)^3,
    rho_r=3 C_r(r_dot/N)^4, p_rad=rho_r/3.

The scalar r is shift symmetric. Its conserved canonical momentum gives

    H_r=N R/a, R=3 C_r[p_r/(4 C_r)]^(4/3), rho_r=R/a^4,
    rho_r_dot=-4 N H rho_r.

This is an action-derived fluid with separate minimal matter conservation.
The radiation coefficient C_r and integration constant p_r enter only the
combination R in the homogeneous gravitational constraints.

## 2. Actual constraints and lapse source

Write the unchanged gravity/clock density as

    f=-3M2 H^2+P(Q^2,tau)-V-M2 Lambda-2 gamma Q^3 H,
    f_H=-6M2 H-2 gamma Q^3,
    j=f_Q=2Q P_X-6 gamma H Q^2,
    K=hessian_(H,Q)(f)
      =[[-6M2,-6 gamma Q^2],[-6 gamma Q^2,B-12 gamma H Q]],
    B=2P_X+4Q^2P_XX.

The complete Hamiltonian is N a^3 c-a^3 W(0,tau), where

    c=c0+rho_r,
    c0=-3M2 H^2+2Q^2P_X-P+V-6 gamma H Q^3+M2 Lambda.

Preserving the lapse primary imposes c=0. The next constraint density is

    t0=V_tau-P_tau+3H W,

with derivatives of P at fixed X. Radiation adds nothing directly to t0:
R/a has no explicit tau dependence at fixed canonical coordinates and
commutes with the coordinate-only H0=-a^3 W.

Let b=(3W,-2Q P_tauX)^T. The scaled-momentum Hamiltonian flow gives

    Rc_r=(3f-3H f_H+rho_r,-3H j)^T,
    K (H_dot,Q_dot)^T=N Rc_r+b.

The +rho_r in its first entry is 3p_rad, obtained from
-partial_alpha(R/a)/a^3. It must not be replaced by +3rho_r.
The actual extensive tertiary bracket and lapse source, divided by a^3, are

    Delta_r=3H t0+b^T K^-1 Rc_r,
    F0=V_tautau-P_tautau+3H W_tau+b^T K^-1 b.

F0 has no direct radiation term but must be evaluated at the new physical
H,Q. The homogeneous preservation equations are

    c_dot=t0-3NH c,
    t0_dot=N Delta_r+F0-3NH t0.

On c=t0=0, the lapse is therefore N=-F0/Delta_r when Delta_r!=0.
The script checks these identities symbolically, as well as
j_dot+3NHj=0. It numerically checks the independent Raychaudhuri equation
with p_clock=P-V+W/N+2 gamma Q^2 Q_dot/N. The factor W/N is essential
after allowing lapse response; setting it to W would reuse the old N=1 branch.

## 3. Analytic small-radiation response and local existence

Fix tau and physical a at a regular old radiation-free solution (H0,q),
where j=A!=0, N=1 and c0=t0=0. Define

    J=partial(c0,t0)/partial(H,Q),
    c_H=-6M2 H-6 gamma Q^3,
    c_Q=QB-18 gamma H Q^2,
    t_H=b_H=3W, t_Q=b_Q=-2Q P_tauX.

The response per small radiation density follows from actual constraints:

    (delta H,delta Q)^T=-J^-1(1,0)^T rho_r,
    delta H=-b_Q rho_r/det(J), delta Q=b_H rho_r/det(J).

At the old constraint solution, Rc_0=3A(q,-H0)^T and grad(c0)=K(H0,q)^T.
An exact two-by-two identity then gives

    det(J)=-det(K) Delta_0/(3A).

Consequently a regular velocity map and nonzero old lapse block imply
det(J)!=0. For smooth coefficients and an interior logarithm-domain point,
the implicit-function theorem supplies a unique nearby H,Q branch at fixed
tau,a for sufficiently small radiation. Continuity preserves H>0 and N>0
near the old H0>0,N=1 point. Local evolution follows from the smooth
Hamiltonian vector field and a_dot=NaH; no global time interval is asserted.

For the lapse, define G(H,Q)=F0(H,Q)+Delta_0(H,Q), using the **off-shell**
expressions. G vanishes at the old point. With h1=delta H/rho_r,
q1=delta Q/rho_r,

    delta N/rho_r=
      -[G_H h1+G_Q q1+b^T K^-1(1,0)^T]/Delta_0.

The explicit last term is radiation's contribution to the bracket. Omitting
it or differentiating a formula already restricted to the old background
would give an incorrect response. The script checks all slopes against a
separate nonlinear solve at rho_r/oldclock=1e-8.

## 4. Conserved charge is a separate initial-data choice

At fixed tau,a, the constraint-selected H,Q generally change

    delta j=(-6 gamma q^2)delta H+(B-12 gamma H0 q)delta Q.

Each new branch conserves its own a^3j; this is not charge production.
Requiring the old charge and the same a at the same tau adds a third
condition, not generally compatible with the two constraint responses.

For comparison, the old integration charge can be retained without retuning
the action by allowing physical a to shift at that tau. At first order,

    delta a/a=-delta j/(3A).

The script also solves this branch nonlinearly: impose a^3j=I and
rho_r=R/a^4 together with c=t0=0. This comparison is reported separately
from the requested fixed-a response and does not change the fixed Hbar
or any reconstruction coefficient.

## 5. Actual bounded one-epoch diagnostics

Use a=1, m=.1, v=.5, M2=Qc=1, I=.1, Lambda=.7. The original background
has H0=.5163977795, q=.9090909091, clock density .1. The original stationary
m,v equations determine the **local coefficient jets through order two**.
No radiation-containing H is passed into them. Those jets suffice for all
action and lapse-source variations at this one epoch; they do not replace
the original functions by a new global quadratic-time model.

The gamma=0 control and gamma=1e-6 each solve seven fixed-a samples:
rho_r/oldclock=0,1e-4,1e-3,.01,.1,.3,1. All computed samples have H>0,
N>0, positive logarithm denominator, positive homogeneous kinetic Schur,
and nonzero lapse block. For gamma=1e-6, the linear coefficients per unit
rho_r are

    delta H/rho_r = .2457288478317,
    delta Q/rho_r = -.1136364218953,
    delta N/rho_r = -2.999994122052,
    delta j/rho_r = -.2625010329868.

At radiation density equal to the old clock density, the fixed-a solve gives

    H=.5416406011735, Q=.8969675329096, N=.7828900525058,
    j=.07800104334018,
    -Delta_r=.00759250856571, Bhat=1.425476750886,
    U-2dQ^2=.001045401539969.

Constraint, current-conservation, Raychaudhuri, and preservation residuals
are below 2e-69 in the 70-digit runs. The small-radiation slope comparison
has normalized differences below 5e-9, consistent with its finite step;
these are numerical residuals, not interval-certified enclosures. The separate
fixed-old-charge branches also solve all seven samples for each gamma.

This answers the local admission question positively at these regular points.
It does not prove radiation-era existence, a complete history from early
times, finite-wavelength stability, scalar/tensor causal propagation or CMB
agreement. A positive homogeneous Schur is not a full perturbation certificate.

## Reproduction and audit scope

Run `python3 -B derive.py`. Exact symbolic identities and all numerical
points are printed as JSON. The bounded manifest records the script and
prior reconstruction source hashes, actual argv, environment, logs, dirty
state, time and resource bounds. No external data or random samples are used.
Mathbox proof-audit and computation-audit separate the local analytic theorem,
floating-point diagnostics and unproved global implications. Mathematical
proofreading is confined to this new report and its notation.

Recorded `run_001/` completed with exit 0 (Python 3.9.6, SymPy 1.14.0,
mpmath 1.3.0). All nine exact symbolic identities passed; all 14 fixed-scale
and 14 fixed-old-charge numerical samples satisfy the reported regularity
checks. The bounded manifest validates against the current input hashes.
Proofread-math self-review required no mathematical-token corrections.
