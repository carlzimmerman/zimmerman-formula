# Neutral microscopic current: exact two-condensate test

2026-10-20. Analytic continuation within the frozen gauge/current scope.
This tests a regular compensating charge sector before amplitude
elimination. It adds no target input, fit, scan or new normalization
candidate. The original physical and Lean goals remain open.

## Opposite charges and a physical clock

In the same 2+1 dimensional pressure sector, take two canonical complex
scalars with charges +e and -e, positive
sextic potentials lambda_i Q_i^3/3, Q_i=|Psi_i|^2, and a neutral scalar
gradient h. In a common positive clock ensemble write

    mu_+=mu+delta, mu_-=mu-delta, delta=eY,
    L_static=sum_i[Q_i mu_i^2-lambda_i Q_i^3/3]-F(Q_+,Q_-)h^2/2.

The displayed local action omits amplitude derivatives only for these
homogeneous equations; the microscopic scalars retain canonical kinetic
terms. Its full charge equation BEFORE eliminating Q is

    j0=2e[(mu+delta)Q_+-(mu-delta)Q_-].

At mu=0 this is 2e delta(Q_++Q_-). Opposite charge signs do not cancel
this susceptibility. With no electric flux, nonzero delta requires both
amplitudes zero. The signs of the electrochemical potentials matter as
well as the charge signs.

For mu>0 and h=0 there is an actual neutral clock medium. Put
a=lambda_+^(1/4), b=lambda_-^(1/4), both positive. On the positive-mu_i
branches, Q_i=mu_i/sqrt(lambda_i), and neutrality gives

    delta0=mu(a-b)/(a+b),
    mu_+=2mu a/(a+b), mu_-=2mu b/(a+b),
    Q_+=2mu/[a(a+b)], Q_-=2mu/[b(a+b)].

Each retained scalar has positive canonical kinetic energy, positive
radial curvature about its clock solution and positive susceptibility.
These sector checks and a neutral homogeneous solution do not by
themselves establish a full MOND/clock/gravity quantum theory.

The balanced clock pressure and its neutral phase charge are

    P0=16mu^3/[3(a+b)^2], N=partial_mu P0=16mu^2/(a+b)^2,
    epsilon=mu N-P0=2P0, epsilon+P0=mu N>0.

Thus this compensator is a finite-density medium, not a Lorentz vacuum.

If the amplitude/Gauss Jacobian is nondegenerate and F is regular, the
implicit function theorem gives Q_i(h^2)=Q_i(0)+O(h^2) and
delta(h^2)=delta0+O(h^2). If F(Q(0))>0, the response starts quadratically.
Neutralizing a regular finite-density state therefore does not produce
the desired pure cubic infrared response. A vanishing stiffness or
degenerate Jacobian requires a separate analysis, not this expansion.

## Exact dilute check and failure of gradient truncation

For the explicit affine stiffness F=2 sum_i c_i^2 Q_i, c_i^2>0,
amplitude elimination gives

    X_i=mu_i^2-c_i^2 h^2,
    Q_i=sqrt((X_i)_+/lambda_i),
    P_i=2 (X_i)_+^(3/2)/(3sqrt(lambda_i)).

At mu=0 the exact Gauss current is

    j0=2e^2Y sum_i sqrt((e^2Y^2-c_i^2h^2)_+/lambda_i).

Every active term has the sign of Y. Neutrality removes all active
condensates. The expansion P_i approximately const |Y|^3 minus
const |Y|h^2 falsely suggests a cubic MOND stationary branch: that
putative balance has h^2/Y^2 of order one, so all omitted terms are
equally important. The exact pressure removes the apparent branch.

For the same explicit F and a fixed positive neutral charge density N,
Gauss imposes p_theta+=p_theta-=N/2. The amplitude Hamiltonian is

    H_amp(s)=sum_i[N^2/(16Q_i)+lambda_i Q_i^3/3+c_i^2 s Q_i],
    partial_Qi^2 H_amp=N^2/(8Q_i^3)+2lambda_i Q_i>0.

It has a unique positive amplitude minimum; its gradient response is
analytic near s=0. This supplies a regular classical compensator but
does not supply the positive cubic or the vacuum normalization.

## Restricted variational obstruction, including critical tuning

Let s=h^2. Suppose the ACTUAL static Hamiltonian in the chosen fixed-charge
ensemble has

    E(s)=inf_{x in X}[V(x)+s F(x)],

finite on the interval, with an admissible set X independent of s.
The infimum of these affine functions is concave: each trial energy at
lambda s+(1-lambda)t is at least lambda E(s)+(1-lambda)E(t), and taking
the infimum preserves this lower bound. Subtracting any linear term
C2 s preserves concavity. Consequently

    E(s)=E(0)+C2 s+C3 s^(3/2)+o(s^(3/2)), C3>0,

is impossible. For 0<lambda<1, concavity would require
lambda^(3/2)>=lambda after subtracting the linear term and taking the
small-s limit. A zero-stiffness vacuum trial V=F=0 gives the stronger
bound E(s)<=0; if V,F>=0 it stays a zero-energy minimizer.

On a differentiable stable local minimum with a positive-definite
amplitude Hessian the same restriction reads

    E''(s)=-F_x^T(V_xx+s F_xx)^(-1)F_x<=0.

Charge-neutrality constraints and Coulomb energy may enter X,V only if
their definitions are s-independent. At fixed clock chemical potentials
the corresponding concavity statement applies to the minimized grand
potential H-sum_i omega_i N_i, not automatically to physical H.

An equivalent pressure check is useful. If a regular equilibrium pressure
is the Legendre supremum

    P(Y,s)=sup_x[omega.N+Y Q-H0-sF],

it is jointly convex in (Y,s). An EXACT pressure
gamma Y^3/6-f(Y)s/2 has P_ss=0 and P_Ys=-f'/2. For f' nonzero its joint
Hessian has negative determinant. It cannot be that exact Legendre
pressure under these hypotheses. The missing higher-gradient terms in
the scalar pressure are therefore load-bearing, not optional corrections
on the proposed MOND balance.

These statements exclude the tested amplitude-only neutral-pair route,
including a critical subtraction, under their explicit ensemble and
affine-gradient hypotheses. They do not exclude arbitrary derivative
currents, temporal Gauss extrema, fermion vacuum traces, higher-gradient
microscopic actions or gradient-dependent constraint domains. The next
constructive route must specify which of these hypotheses changes and
derive the current before relaxing the microscopic fields. Even a
successful current would still need the independent positive-vacuum
relation epsilon0=16pi gamma b^3 to force the requested ratio.

## Review provenance

Two analytic agents independently derived the full current, the regular
neutral branch/dilute obstruction and the variational discriminator.
The coordinator recomputed the neutral solution and concavity argument.
No scripts, scans, downloads or Lean compilation were used for this
additional analytic test; it is not one of the four verified modules.
