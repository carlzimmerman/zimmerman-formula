# CP02: gated clock current and closed leading Newtonian transport

Checkpoint HEAD: `2207a1df48348f01ca1084d4add5d214c55d0e7e`.
This derives the actual current and a closed, explicitly ordered reduction of
the gated QX17 action. It supplies a transport law; it does not adopt the gate
as a healthy completed theory or identify its solutions with an observed halo.

## 1. Action, conventions, and exact variation

Use c=1, signature(-,+,+,+), K=4piG, future timelike clock gradient Q>0,
`n_mu=-partial_mu tau/Q`, `Q=sqrt(-partial tau.partial tau)`, l=lnQ and tangent
polarization n.P=0. The same constrained off-shell extension as QX17 is

    L = H(Q,Pi) - P^mu partial_mu l - W(K|P|) - Gamma(Pi) + lambda n.P,
    Pi = nabla_mu P^mu + P^mu partial_mu l,
    H(Q,Pi) = F(Q) S(Pi/Pic),
    Gamma(Pi) = gamma_L [max(Pi,0)]^2/2.

The Einstein and minimally coupled baryon actions are included separately.
On n.P=0 this is the QX17 Legendre action because P.A=-P.dlnQ and
Pi=D.P. Off the constraint, replacing P.A by -P.dlnQ entails a multiplier
redefinition; all lambda formulas below refer to the displayed convention.
Gamma' is continuous; derivatives at the switch are interpreted one-sided or
weakly, not by inventing an analytic Taylor expansion at Pi=0.

Define

    B = 1 + Gamma'(Pi) - H_Pi(Q,Pi),     b = B/Q.

At fixed metric and P, deltaPi=P.d(deltaQ/Q). Apart from the multiplier term,
integration by parts therefore gives

    delta L = [H_Q + nabla_mu(B P^mu)/Q] deltaQ,
    deltaQ = n^mu partial_mu(delta tau).

On the tangent constraint, delta(lambda n.P) contributes
`-lambda P^mu partial_mu(delta tau)/Q`. Thus the exact clock equation is

    nabla_mu J^mu = 0,
    J^mu = rho_Q n^mu - lambda P^mu/Q,
    rho_Q = H_Q + nabla_mu(B P^mu)/Q.                 (1)

Varying P gives

    -B partial^mu l + partial^mu B - W_P^mu + lambda n^mu = 0,
    W_P^mu = K W'(K|P|) Phat^mu.                    (2)

Projecting (2) tangentially and normally gives, respectively,

    Q D_mu b = W_P,mu,
    lambda = n.partial B - B n.partial lnQ = Q n.partial b.

Consequently the on-P-equation form of the current is

    J^mu = rho_Q n^mu - P^mu (n.partial b).          (3)

**Exact criterion:** transport is along the clock flow precisely when
`P^mu(n.partial b)=0`. This holds if P=0, or if B/Q is advected unchanged,
but not for a general changing polarization/gate configuration. Lambda is
fixed by the normal P equation and is not an independently tunable flux.

For H=mu_K^2(Q-1)^2/(2K), H_Pi=0, (1) reduces exactly to QX17 E3. The gated
current requires both F'(Q)S and the -H_Pi contribution inside B. Keeping only
the first is incorrect. The direct 1+1 jet check in exact_current.py varies
this L before imposing tangency on test fields. Clock and P derivatives match;
deleting any of gate-Pi, leaf flux, or gated H_Q fails on all three witnesses.

In unitary gauge tau=t, lapse N, shift N^i, spatial metric gamma_ij,

    partial_t(sqrt(gamma) rho_Q)
      + partial_i {sqrt(gamma)[-N^i rho_Q - lambda N^2 P^i]} = 0.      (4)

This is an explicit conserved density and coordinate flux, without guessing
that rho_d is a material shell mass.

## 2. Controlled leading Newtonian reduction

Write tau=t+sigma and use the weak metric with Newtonian potential Phi. Set

    v = -grad sigma,
    x = Q-1 = partial_t sigma - Phi - |grad sigma|^2/2 + O(epsilon^2).

The ordering is v^2,x,Phi=O(epsilon), time derivatives O(v/L), P=O(rho L),
Pi=O(rho), H and Gamma and W=O(rho epsilon), H_Q=O(rho), and importantly

    H_Pi = O(epsilon),   Gamma' = O(epsilon),
    derivatives of these quantities vary on the stated spatial/time scales.

Large or singular gate derivatives can violate this ordering. In particular,
small Pic relative to the charge density must be checked rather than treated
as harmless. Large C alone does not invalidate the expansion if x and the
resulting H_Pi remain in range. With F=Cx^2, H_Pi=Cx^2 S'/Pic and its scale is
explicit. This is a regular Newtonian sector of the action, not a uniform
approximation for arbitrary coefficients and states.

Here A=-grad x+O(epsilon^2/L), Pi=divP+relative O(epsilon), and B=1+O(epsilon).
Consequently rho_Q=H_Q+Pi+O(rho epsilon), while the noncomoving term in (3)
is O(epsilon rho v). It can consistently be dropped **at this order**. The
ignored corrections to Pi in the action multiply H_Pi or Gamma' and are also
one order higher. Keeping the full dependence of S on Pi is compatible with
this scaling; S itself need not be close to1.

After integrating -P.grad x by parts, the leading action is

    L_NR = -|gradPhi|^2/(2K) - rho_b Phi
           + H(1+x,Pi) + x Pi - W(K|P|) - Gamma(Pi),
    Pi=divP.                                                   (5)

Direct independent derivatives of (5) give the closed system

    n = H_Q(1+x,Pi) + Pi,
    partial_t n + div(n v) = 0,                                (6)
    partial_t v + (v.grad)v = -grad(Phi+x),                     (7)
    Delta Phi = K(rho_b+n),                                    (8)
    grad[x+H_Pi(1+x,Pi)-Gamma'(Pi)] + W_P = 0,
    Pi = divP.                                                 (9)

Initial v is irrotational, and the gradient force preserves that property
while the solution remains smooth. Equations (6)–(9), initial n and v, the
baryon source, and gravitational/polarization boundary conditions constitute
the leading evolution problem. No missing arbitrary current is needed at
this order. It is the combined source n, not bare H_Q or Pi separately, that
is advected. Positive initial n stays nonnegative on smooth characteristics:
`n(X(t),t)=n(X(0),0) exp[-integral divv dt]`. Pi itself may have signed lobes.

For F=Cx^2, C>0 and S>0, invert the first equation locally:

    x = (n-Pi)/(2C S(Pi/Pic)).                                 (10)

Equations (9) and (10) supply a nonlinear elliptic polarization constraint on
each time slice whenever its linearization is elliptic. Equation (8) supplies
Phi, then (6) and (7) evolve the state. This statement does not presume
ellipticity for an arbitrary gate or across a singular auxiliary branch.

## 3. Hamiltonian closure, uniqueness conditions, and actual linear response

The internal energy after eliminating x is

    e(n,Pi,P) = (n-Pi)^2/[4C S(Pi/Pic)] + W(K|P|) + Gamma(Pi).   (11)

Its derivatives obey

    e_n=x,   e_Pi=-(x+H_Pi-Gamma'),
    delta integral e / delta P = grad(x+H_Pi-Gamma')+W_P.

Thus one can obtain P by stationarity of (11) for fixed n. Positivity of the
P Hessian and appropriate boundary conditions give the required local
elliptic solve; a positive Hessian does not alone prove global uniqueness
outside its domain. For the numerical exponential gate, writing h=n-Pi,

    e_PiPi = exp(Pi/Pic)/(2C) [1-2h/Pic+h^2/(2Pic^2)],
    W_PP = K/[1-K|P|/a0]^2                         (one dimension).

The benchmark stays on the positive branch with h/Pic around.1 and well below
the polarization cap K|P|=a0. The constraint solver uses these actual
derivatives, not a pressureless shell substitute.

At a homogeneous P=0 background define A=H_QQ, b=H_QPi,
D=H_PiPi-Gamma'', c=1+b, and longitudinal w=W_PP. For a Fourier mode k,

    delta n = A delta x + c delta Pi,
    (w-D k^2) delta Pi = c k^2 delta x.

Where the coupled denominator is nonzero,

    delta x / delta n = (w-Dk^2)/[Aw+(c^2-AD)k^2],
    omega^2 = n0 { k^2(w-Dk^2)/[Aw+(c^2-AD)k^2] - K }.         (12)

This follows both from the linear constraint and by eliminating Pi from the
Hamiltonian Hessian. One must not divide by w-Dk^2 at its zero; the coupled
formula must be checked there directly. Gamma'' at the one-sided switch
requires a specified branch; the benchmark sets gamma=0.

For the ungated P=0 QX17 potential, w=K, b=D=0, and

    omega^2 = -n0 A K^2/(AK+k^2).                              (13)

The high-k pressure response and self-gravity partially cancel. This is not
the growth equation obtained by separately advecting rho_d with an unrelated
sound speed. Formula(12) has been exercised against the actual nonlinear
transport integrator in its small-amplitude limit, not only simplified
symbolically. It is a Newtonian mode result, not the full relativistic
metric-clock-polarization health calculation.

## 4. Moving EFE boundary: the required flux is now explicit

For a region with moving boundary velocity u_boundary, (6) gives

    d/dt integral_V n dV = integral_boundary n(u_boundary-v).dS. (14)

In spherical symmetry at radius R(t),

    M_dot(R,t) = 4pi R^2 n(R,t) [R_dot-v_r(R,t)].               (15)

This formula is valid before caustics for the leading system. At exact level
use the density and flux in (4): their Reynolds flux is F^i-q u_boundary^i,
including the lambda polarization term. A moving boundary is not a material
surface unless its speed equals the transported flow (including exact drift).

If one chooses the external-field aperture R_E=sqrt(G M_b/a0)/x_e, then

    R_E_dot/R_E = .5 M_b_dot/M_b - .5 a0_dot/a0 - x_e_dot/x_e.

If one additionally asks the actual charge inside that aperture to equal
`M_b [F_A(x_e)-1]`, conservation requires

    4pi R_E^2 n(R_E)(R_E_dot-v_r)
      = M_b_dot(F_A-1)+M_b F_A'(x_e) x_e_dot.                  (16)

Equation(16) is the concrete matching condition. A static EFE potential or
an external-field history alone does not enforce it: n and v must come from
the evolution. Increasing the aperture can add charge without creating any;
shrinking it can still gain charge if inward material transport is faster.
The periodic benchmark explicitly tests this mechanism and rejects omission
of the moving-boundary term.

## 5. Is the amount selected?

There is a definite answer for the global charge in this action. On homogeneous
FRW with P=Pi=0, (1) becomes

    a^3 H_Q(Q,0) = I,                                        (17)
    Q(a)=1+I/[2C S(0) a^3]               for F=C(Q-1)^2.

For fixed action coefficients and S(0)>0, I is an integration constant fixed
by initial charge. Different admissible I give distinct homogeneous solutions
(with correspondingly different self-consistent gravitational histories).
There is no source or relaxation term selecting I. This exact family refutes
unique global charge normalization from these action coefficients alone.

It does not refute a possible local environmental capacity or a conditional
halo relation after an initial cosmological inventory and assembly history
are supplied. Such local predictions would have to be obtained by solving
(6)–(9), or the exact system when ordering fails, with those data. A fitted
static mass enhancement does not set I, and conservation cannot turn it into
a universally selected retention fraction. The numerical mean-charge1 and1.3
examples preserve distinct inventories; their periodic compatibility
backgrounds differ, so they are illustrations, not the proof of(17).

The concrete advance over the preceding checkpoint is therefore a derived
flux, a closed leading evolution system, an executable nonlinear constraint
solver, a verified growth law, and an exact nonselection result for the global
normalization. The missing transport law is no longer merely named as future
work. This does not repair a gate's independent health or observational failures.

## 6. The simplest stationary flowing-clock escape is closed

There are two precise results, with different hypotheses.

**Leading NR, any dimension:** let a smooth stationary solution have n>0,
single-valued velocity potential sigma_0, v=-grad sigma_0, and zero pointwise
normal charge flux at the boundary. A periodic domain is allowed if sigma_0
is also single-valued and periodic. Equations(6) imply

    div(n grad sigma_0)=0,
    0 = integral sigma_0 div(n grad sigma_0)
      = boundary integral sigma_0 n partial_normal sigma_0
        - integral n |grad sigma_0|^2.

The boundary term vanishes, hence v=0 wherever n>0. On an infinite domain one
must require the weighted boundary term to vanish, not merely announce finite
mass or zero integrated net flux. The result does not assume any particular S.
Exceptions to this proof include nonzero boundary throughput, sinks or singular
boundaries, time dependence, a multivalued circulation potential, or loss of
the positive-density/smooth single-fluid assumptions. If n changes sign the
integral argument is unavailable; that fact alone constructs no solution.

**Exact static spherical current:** take a static spherical metric and a
stationary clock tau=t+psi(r), with all scalars Q,B,b depending only on r.
Using (3),

    J^r=n^r[rho_Q-P^r b']
       =n^r[H_Q+(B/Q)Pi].                                   (18)

The identity follows because

    div(BP)/Q - P^r(B/Q)' = (B/Q)[divP+P^r(lnQ)']=(B/Q)Pi.

Conservation fixes `r^2 sqrt(-g_tt g_rr) J^r` to a constant. A regular origin
with finite fields sets that constant to zero. Wherever
`H_Q+(B/Q)Pi != 0`, equation(18) forces n^r=0. In particular a positive
coefficient closes the proposed stationary radial clock-flow loophole.
**A negative nonzero coefficient does not evade this exact radial result.**
A smooth nonzero clock flow with zero radial current instead requires the
coefficient to vanish identically on an open flowing region; alternatively
there must be nonzero boundary/central charge flux, a singular origin, or
time dependence. These are different dynamical/boundary branches, not the
regular closed stationary halo assumed in the proof.

Positive rho_Q alone is not enough to assert the coefficient's positivity:
rho_Q differs from it by P^r b'. The exact tests retain an algebraic witness
for this distinction. They do not claim that the witness solves all metric
and polarization equations. In the regular NR ordering the coefficient is
n+O(epsilon rho), so a strictly positive n separated from zero does provide
the needed implication to leading order.

These results close the simplest static-flow workaround under explicit
hypotheses. They do not rule out open accretion, post-caustic/multistream
behavior, or a time-dependent halo; nor do they prove that those alternatives
produce the required EFE profile or select its charge.
