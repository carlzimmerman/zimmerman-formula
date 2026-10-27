# The front cannot be assigned the infall energy

This note proves statements about the specified reduction, not galaxy formation.
Conventions: dV=r²dr, radii in rM, time in the original dynamical unit. The original
energy is evaluated on a restricted density interpolation and a translated
locked phase profile. The canonical J=30 spin inertia is an alignment closure;
it is not an exact elimination of the moving independent-field theory.

## Conversion, curvature and reciprocal work

Write rho=rho0+lambda Delta_rho and Q'=r² Delta_rho, with Q(0)=Q(infinity)=0.
Continuity fixes v=-Q lambdadot/(r²rho). For q(r,R)=sin²(theta(r-R)),

    Gamma=rho (partial_t+v partial_r)q
         =c_lambda lambdadot+c_R Rdot,
    c_lambda=-Q q_r/r², c_R=-rho q_r.

Integration by parts gives integral c_a dV=partial_a M_T. This is a continuum
identity. Quadrature errors in the numerical implementation are recorded
separately; midpoint static mass and continuously interpolated phase mass
are not identical discretizations.

Let C_a=g integral chi c_a dV. At each spatial point,

    partial_R c_lambda-partial_lambda c_R=(Q q_r)'/r².

Consequently the curvature force is

    F_lambda^curv=-g Rdot integral chi_r Q q_r dr,
    F_R^curv=+g lambdadot integral chi_r Q q_r dr.

Its total mechanical work vanishes identically. It vanishes for spatially
constant chi, but not generally for the actual radiation field. Thus it cannot
be omitted on the grounds that the integrated source is dM_T/dt.

For L=G_ab qdot^a qdot^b/2-V-C_a qdot^a+L_chi, the other forces are

    G_ab qddot^b+Christoffel_abc qdot^b qdot^c+V_a
      =F_a^curv+g integral c_a chidot dV,
    chiddot-c² Delta chi=-g c_a qdot^a.

Multiplying by velocities cancels the remaining exchange exactly. Total
mechanical plus field energy changes only by boundary flux. The shift charge
is integral chidot dV+g M_T, including its outgoing flux.

## The field adds inertia, not a static pin

At low frequency let A=-Delta with decay at infinity. Its radial Green kernel
in these conventions is 1/max(r,s). Eliminating the instantaneous particular
solution chi=-(g/c²) A^-1 Gamma adds

    Delta G_ab=(g²/c²) integral integral
       c_a(r)c_b(s) r²s²/max(r,s) dr ds.

For any vector u, put M_u(r)=integral_0^r u^a c_a(s)s²ds. Integration by parts
gives u^a DeltaG_ab u^b=(g²/c²) integral_0^infinity M_u(r)²/r² dr >=0.
Hence this term cannot lower a transport inertia or supply a static restoring
potential. The quasistatic approximation requires small source frequency
times source radius/c; it is used for the slow branch, not as an exact fast
mode self-energy.

The far outgoing monopole is chi=-g Gamma_total(t-r/c)/(c²r) at leading long
wavelength order. Thus P_out=g² (dGamma_total/dt)²/c³ in the radial convention.
A constant conversion rate is not a continuous radiative power source.

There is also an exact locality statement, independent of the slow expansion:
on any region where partial_mu j_T^mu=0, the interaction g partial_mu chi j_T^mu
is a boundary term. That region supplies no direct scalar source. With zero
initial scalar data and zero incident scalar data, an everywhere conserved
current yields the zero scalar solution, hence zero export through this
operator. This does not prove that such a subspace is invariant for the whole
finite-J galaxy: conversion and stresses at its interface can still exchange
energy with the interior. It identifies the transfer that must be computed.

## How much does infall force the front?

Let R_*(lambda) solve V_R=0. Set R=R_*(lambda)+z and use the positive dressed
metric. Along z=0 put

    A=G_ll+2G_lR R_*'+G_RR R_*'²,
    B=G_Rl+G_RR R_*', C=G_RR, K=V_RR,
    A_z=partial_R[G_ll+2G_lR R_*'+G_RR R_*'²].

Retain terms linear in z and zdot while prescribing slow lambda(t). Put
B_z=partial_z B at z=0. The complete tangent equation is

    d(C zdot)/dt+K_eff z=F,
    K_eff=K+B_z lambdaddot+(B_z' -A_zz/2) lambdadot²,
    F=-B lambdaddot-(B' -A_z/2) lambdadot².

FD-03 initially uses K instead of K_eff. FD-04 explicitly audits this omission;
FD-05 repeats with its computed correction. No finite difference audit is an
interval bound. The slow motion itself uses its actual branch potential U=V(lambda,R_*) and
conservative rest data at lambda0=1/16:

    lambdadot²=2[U(lambda0)-U(lambda)]/A,
    lambdaddot=(-U' -A' lambdadot²/2)/A.

This is a conditional test after an initial nucleus, not the initial-value
formation problem. It omits back reaction from z on lambda. Neither the energy
drop nor a chosen fraction of it is inserted into F.

## A bound that does not choose a damping coefficient

Proposition. Consider the scalar linear oscillator with C,K>0, force F,
canonical p=C zdot, and an initially unenergized passive outlet connected
only to this coordinate. Let its nonnegative stored energy be S and its
cumulative exported energy be D. At fixed coefficients the outlet obeys

    d/dt [p²/(2C)+K(z-F/K)²/2+S]=-Ddot <=0.

For a piecewise constant coefficient sequence define h_i=F_i/K_i,

    a_i=max(1,sqrt(C_(i-1)/C_i),sqrt(K_i/K_(i-1))),
    b_i=sqrt(K_i/2) abs(h_i-h_(i-1)),
    B_0=sqrt(K_0/2) abs(h_0), B_i=a_i B_(i-1)+b_i.

Assume z=p=S=D=0 initially and that changing coefficients does not directly
energize the outlet. Then, at every step,

    D+S+p²/(2C)+K(z-h)²/2 <= B_i².

Proof. At a parameter jump p,z,S,D are fixed. Scaling of the kinetic and
spring coordinates has norm at most a_i, and translating the spring origin
has norm b_i. The Euclidean triangle inequality, including sqrt(S) and
sqrt(D) as extra coordinates, yields sqrt(E_new+D)<=a_i sqrt(E_old+D)+b_i.
Between jumps passivity preserves or decreases E+D. Induction proves the
claim. No resonance assumption or damping coefficient appears. For positive
bounded C,K and h of bounded variation, subdivision gives the corresponding
continuous-parameter bound whenever these products/sums converge. QED.

The numerical bound is exact algebraically for its sampled coefficient
sequence. Time subdivision converges in the tests, but the bound does not
converge across the three source-branch grids: it grows as finer grids resolve
more coefficient variation. No uniform bound for the continuum branch is
claimed. The theorem does not cover an additional active infall port,
time-varying coupling that supplies energy directly to the outlet, nonlinear
mode conversion, initially supplied field energy, or loss of C,K positivity.
In particular it is not a universal no-go for the full scalar/material action.

## Implication

The successful frozen-profile radiation prototypes did not establish their
own energy pump. FD-02 tests slow tracking; FD-03 tests its forced linear
front. Their missing implication is explicit energy transfer out of material
infall through the full two-port system or through additional resolved local
degrees of freedom. A larger passive loss coefficient on the already weakly
forced front is insufficient within the proposition's hypotheses.
