# Restricted Hamiltonian obstruction — full action still NO VERDICT

Kappa=1/2 FITTED; not theory closed. This is new exact algebra for the
previously omitted scalar–polarization mixing in AZ40's parallel,
constant-coefficient PN block at mu_K=0. It is not a full constrained-action
calculation or a solved galaxy, Solar or cosmological background.

## The missing distinction

Positive kinetic coefficients and real nonzero frequencies do not by
themselves imply a bounded Hamiltonian when a zero-frequency clock mode
is retained. The potential-only portal escapes the old scalar kinetic
obstruction but has a separate restricted energy obstruction if clock
momentum is allowed to vary. Imposing zero clock momentum changes the
answer; that restriction needs a derivation from the full theory.

## Constraint elimination

Use the existing normalized K=4*pi*G=1 convention, q=delta phi,
d=D-1>0, D=(1+s)^2+gamma*k^2, and k>0. Hold local coefficients constant.
Let A=W_Pphi and Omega2=k^2+V_phiphi+W_phiphi. The extended quadratic block is

    L = -k^2 Phi^2/2 + k P Phi - k P sigma_dot - (d+1) P^2/2
        + q_dot^2/2 - v Phi q_dot - A P q - Omega2 q^2/2.

Eliminating Phi and P exactly gives

    L_red = (1+v^2/k^2) q_dot^2/2
            + (v q_dot/k + k sigma_dot + A q)^2/(2d)
            - Omega2 q^2/2.

The kinetic matrix is the earlier positive AZ40 result:

    K11=1+v^2(d+1)/(k^2 d), K12=v/d, K22=k^2/d,
    det K=(k^2+v^2)/d > 0.

After removing the constant-coefficient total derivative
A*v*q*q_dot/(k*d), define G=k*A/d and M=Omega2-A^2/d. Then

    L_red = dot(Q)^T K dot(Q)/2 + G q sigma_dot - M q^2/2.

The frequency determinant is

    det E(omega) = omega^2/d * [(k^2+v^2) omega^2-k^2 Omega2].

Thus there is a zero-frequency mode and, if Omega2>0, an oscillatory mode
omega^2=k^2 Omega2/(k^2+v^2). The A dependence cancels only because the
q*sigma_dot term is present. Omitting it changes the characteristic equation.
This real frequency is not a positive-energy proof.

## Hamiltonian and the fixed-charge exception

With p=(p_q,p_sigma), the exact Legendre transform is

    H = [p-(0,Gq)]^T K^(-1) [p-(0,Gq)]/2 + M q^2/2.

Consequently its nontrivial (q,p_q,p_sigma) quadratic form is positive
definite iff M>0; sigma itself is a flat cyclic coordinate. For M=0
it is semidefinite; for M<0 it is indefinite. At p=(0,Gq), H=M q^2/2.
The Hessian determinant is (d Omega2-A^2)/(k^2+v^2).

Example: k=d=v=Omega2=1, A=2. K has determinant2 and is positive definite;
the nonzero frequency has omega^2=1/2, yet H=-3/2 at q=1,p_q=0,p_sigma=2.
The example demonstrates the distinction, not a measured background.

Since sigma is cyclic in this restricted block, j=p_sigma is conserved.
Its fixed-j Routhian, up to total derivatives, is

    R_j = (1+v^2/k^2) q_dot^2/2 - Omega2 q^2/2
          + (A j/k) q - d j^2/(2k^2).

At j=0 and Omega2>0 this scalar block has positive kinetic coefficient
and positive restoring force. The unrestricted negative-energy direction
changes j. A prescribed j=0 sector must therefore not be confused with
a proof of health for unrestricted clock perturbations. Nor does an
indefinite Hamiltonian alone establish exponential growth in this frozen
block: the characteristic calculation explicitly shows the distinction.
Time-dependent coefficients, gradients, nonzero mu_K and full constraints
remain outside this calculation.

## What the potential portal does

For the actual polarization potential in the same normalization,

    W=a[-P-a log(1-P/a)], P=a s/(1+s), s>0,
    h(s)=s+s/(1+s)-2 log(1+s),

its derivatives at fixed P give

    W_a=-a h,
    W_aa=-h+s^3/(1+s),
    W_Pa=-s^2.

Therefore A=-a_phi s^2 and the algebraic portal contribution to M is

    W_phiphi - A^2/d
      = a_phi^2[-h+s^3/(1+s)-s^4/((1+s)^2+gamma*k^2-1)]
        - a*a_phiphi*h.

At fixed finite k and gamma,

    lim_(s->infinity) M/s = -a*a_phiphi,

because k^2 and V_phiphi are finite local coefficients. For the proposed
constant-w branch, a is proportional to sinh(y)^(-n), with
n=(1-beta)/beta>0, y=(phi-phi_star)/B, and

    a_phiphi = a/B^2 [n^2 coth(y)^2+n csch(y)^2] > 0.

The restricted unrestricted-charge Hamiltonian therefore becomes indefinite
at sufficiently large s. This result applies to either positive-a0 footing.
It does not locate that regime on a screened physical background, establish
that it is dynamically reached, or prove that omitted full-theory terms
cannot change the conclusion. In particular s is a polarization-conjugate
parameter, not automatically the measured g/a0.

## Answer and next mathematical requirement

The potential-only portal is not established as a healthy action by its
positive kinetic block. It must either derive and preserve a physical
zero-charge restriction, show from complete constraints/backgrounds that
the negative-energy regime is excluded or altered, or change the action.
Those are distinct missing mathematical requirements, not completed fixes.
The normalization remains independently free:

    kappa^2 = xi*(1+beta)/2.

Nothing in this energy calculation fixes xi or derives kappa=1/2.

Frozen scope1110094c7f. mixed_block.py verifies19/19 exact symbolic checks.
The separate mutation drops only q*sigma_dot: it preserves the kinetic
matrix but fails the characteristic cancellation, v=0 frequency known
answer and positive-frequency example. No numerical tolerance or fitted
scan enters the proof. Reproduce from this lane directory:

    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python mixed_block.py
    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python mixed_block.py --mutate

Main exits0; mutation exits1. All original adopted-action records remain
unchanged.
