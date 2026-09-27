# CA4-GNC-PQ: retain the positive barrier while repairing the vacuum scalar

The perspective floor passes the fixed-data constraint theorem, but that
theorem does not imply healthy scalar evolution on an expanding background.
The subsequent actual de Sitter calculation found a long-wavelength negative
stiffness in CA4-GNC-P. This prompted a specific additional action term,
independently varied by the action lane and tested by the evolution lane:

    Delta L = -A z^2, z=P_h Z=t-1,
    A=V0 zeta>0, zeta=4/ell-1, 0<ell<=1.

It is outside the reciprocal carrier term, not an addition to Wd/t. Keep
V0>0 and bare Lambda=0. This defines a distinct candidate, **CA4-GNC-PQ**.
The common action and its source/stress variations are in
../action/VACUUM_STIFFNESS_VARIANT.md. The new term adds no field. It vanishes
with its first variation on homogeneous z=0 and preserves the background
vacuum stress. Its second variation is essential for the perturbations.

## The positive-data theorem survives the new term

Use the exact hypotheses of PERSPECTIVE_REPAIR.md. The auxiliary Hamiltonian
now adds q(t)=A(t-1)^2:

    H_Q[t]=integral N [m_g|Dt-b|^2+epsilon0/t+A(t-1)^2], <t>_h=1.

The same convex regularization works. Its multiplier bound changes because

    q(t)+t q'(t)=3A(t-2/3)^2-A/3 >= -A/3.

Testing the regularized equation with t-1 and comparing with t=1 gives

    lambda <= lambda_max,Q
      =[integral N epsilon0+(3m_g/2)||b||_N^2+(A/3)integral N]/Vol_h.

The multiplier itself is now
lambda=-<N[epsilon0 f_d'(t)+2A(t-1)]>_h; the added term cannot be omitted.

At a minimum t_min<=1 by mean-one normalization, so q'(t_min)<=0.
The minimum equation therefore still implies

    N_min epsilon_min[-f_d'(t_min)]
       <=lambda_max,Q+2m_g||div_h(Nb)||_infinity = C_Q.

Choosing d<min(1,sqrt(N_min epsilon_min/C_Q)) rules out t_min<=d,
and gives the positive lower bound

    t_min>=sqrt(N_min epsilon_min/C_Q)>0.

The regularization domination and elliptic bootstrapping from the original
proof are unchanged. Thus existence, uniqueness, positivity and smoothness
hold for the new fixed-data functional. Its joint canonical Hessian gains
the nonnegative term 2A integral N (delta t)^2. The independent review of
this extension is preserved separately in the transport lane.

These statements still hold U,N,h fixed. The coefficients of the bound
depend on their data and are not an invariant bound for the evolving theory.

## Why the additional coefficient is connected to vacuum stability

On the homogeneous inactive vacuum solution,

    H^2=V0/(3M_P^2), t=1, q=k/a,
    S_q=exp(-xi^2 q^2/2), r0=ell/4, r=r0 S_q.

For nonzero scalar modes the independent U equation gives Z=r Phi.
The properly varied projection removes a spurious psi-Z volume cross term.
The original reciprocal floor contributes V0(Phi Z-Z^2); the new term
adds -V0 zeta Z^2. In the gravity normalization their lapse contribution is

    6H^2 r[1-(1+zeta)r].

Thus zeta=1/r0-1 cancels its constant infrared limit without removing the
positive floor itself, leaving 6H^2 r0 S_q(1-S_q). The all-wavelength scalar
test and the limitations of the infrared argument are displayed in the
evolution lane's [de Sitter report](../evolution/FRW_RESULT.md); they are derived on a constraint-satisfying
expanding background, not a positive-density Minkowski placeholder.

Define x=q^2, u=xi^2 x/2, eta=3H^2 xi^2 r0 and

    alpha_eff=2-2cN(1-r)^2,
    d(x)=alpha_eff+eta exp(-u)[1-exp(-u)]/u,
    D=x d, K=2(2+3c2)/c2, F=K H^2+D.

The quotient is extended continuously at u=0. The independently derived
reduced kinetic coefficient is K D/F. After the required integration of
the mixed psi psi_dot term, the spatial coefficient in the Lagrangian is

    -2x^2 {K H^2[d+2+2x d'(x)]+x d(2-d)}/F^2.

The minus sign matters: a positive expression in braces is restoring
stiffness. With

    0<alpha<=1, 0<ell<=1, c2>0, eta<=1/10,

the checked analytic bounds d>0, d<=123/80<2 and
d+2+2x d'>=3/5>0 make both kinetic and restoring coefficients positive for
every finite nonzero q. The bounds are sufficient, not a fit or an optimal
parameter region. As q approaches zero the reduced kinetic coefficient
also tends to zero; this is not a uniform coercivity theorem including k=0.
The homogeneous projection/constraints must be treated separately.

The positive-square carrier potential has nonnegative quadratic masses on
this zero-excitation background, and the homogeneous tensor branch is the
Einstein branch. This controlled linear background result is stronger than
the earlier carrier-free, flat frozen-block test. It still does not prove
general-background tensor/clock health, full constraint rank, or nonlinear
global evolution with an occupied transporting carrier.

For each fixed nonzero comoving mode on the vacuum branch, the same report
also proves future boundedness and convergence: the reduced friction is at
least H and the remaining q(t)^2 coefficient is time-integrable. This is a
modewise linear result, without a uniform nonlinear or Sobolev conclusion.

## Scientific status

The new coefficient relates vacuum stiffness to the gate compensator through
an explicit stability calculation. It does not determine V0, ell, xi or a0
from observations or fundamental constants. The exact globally filtered
static target, preferred-frame/PPN tests, moving-source coupling and useful
transport rate remain obligations for this same PQ action. The new positive
term changes the auxiliary source and must accompany every future calculation;
it cannot be appended only to a perturbation equation.
