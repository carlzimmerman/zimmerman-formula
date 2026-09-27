# Positive vacuum tension as a barrier in the perspective carrier

This is a constructive **different carrier action**, denoted CA4-GNC-P,
coupled to the same compensated gravity host. It addresses two actual
failures of the earlier trials: exponential auxiliary elimination can give
negative reduced kinetic curvature, while a reciprocal coupling without a
positive energy floor can reach its zero-lapse boundary. The arguments below
were independently checked by the evolution and transport agents.

It is not a global-in-time theorem for self-gravitating solutions. Its exact
new results are joint canonical convexity and a globally defined, smooth,
positive auxiliary solution for fixed smooth canonical data on a compact leaf.

## Explicit change to the action

Keep the GNC gravity/heat/clock action in ../action/FINAL_ACTION.md. Replace
only its carrier term, and choose the bare cosmological term to be zero:

    t=1+P_h Z>0, P_h Z=Z-<Z>_h,
    Ld=t Kd-Wd/t,
    Wd=sum|D phi_A|^2/2+V0+Vconversion(phi), V0>0,
    Vconversion=Mcarrier^2|Psi|^2
       +mcarrier^2|Chi+gamma s Psi|^2+mu^2 s^2/2.

The five real fields are sqrt(2)Re/Im Psi, sqrt(2)Re/Im Chi and s.
The physical metric for ordinary matter is unchanged. The carrier's
composite lapse is N/t, its speed relative to the normal frame is 1/t,
and it introduces no second independent metric or particle population.
The projection makes <t>_h=1 and leaves the Z shift gauge intact.

At fixed t, its lapse energy density and its Z source are different:

    rho_d=t Kd+Wd/t,
    sigma_d=Kd+Wd/t^2=rho_d/t.

The exact auxiliary equation is therefore

    2 M_P^2 cN div_N(DZ-a+DU)
       +sigma_d-<N sigma_d>_h/N=0.

All projector stress and clock terms must use sigma_d in place of the
exponential coupling's Z source; the lapse still sees rho_d. Their difference
is explicit. The cold-source subtraction can be recovered in a joint weak-field,
short-wavelength approximation where the background susceptibility is negligible;
it is not an exact identity on a nonzero vacuum background. With only V0,
rho_d=V0-V0(t-1)+... while sigma_d=V0-2V0(t-1)+... . Subtracting homogeneous
vacuum energy does not remove this linear response. The projected source also
has lapse/mean terms, and a consistent FRW calculation must retain the
background metric equations. Full PPN and source mixing need a new calculation.
This is not a silent redefinition of the exponential action.

## Joint momentum/auxiliary positivity

Write r_A=Pi_A/sqrt(h), m_g=M_P^2 cN>0, b=a-DU, and

    epsilon0=sum r_A^2/2+Wd >= V0.

The Z-dependent canonical Hamiltonian at fixed geometry, U and carrier
coordinates is

    H[t,r]=integral N dvol_h [m_g|Dt-b|^2+epsilon0/t], <t>_h=1.

For variations v=delta t and delta r, the exact Hessian is

    delta^2 H = integral N {
      2m_g|Dv|^2 + sum|delta r_A-r_A v/t|^2/t +2Wd v^2/t^3 }.

Every term is nonnegative. With V0>0 the expression vanishes only for
v=0 and delta r=0. Eliminating t by minimization consequently preserves
convexity in the canonical momenta; for smooth bounded data and the positive
bounds proved below, the corresponding Schur block is positive. A uniform
numerical coercivity constant over an evolving family still requires
uniform bounds on its coefficients and momenta.

The evolution lane retains a negative control: for the exponential two-cell
model H=kappa z^2+exp(-z)p^2/2, its unique auxiliary minimum has
H_red,pp=exp(-z)(1-z)/(1+z), negative at z>1. Replacing it by the perspective
coupling removes that sign change, but with no floor the empty second cell
can reach t2=1-z=0 at p^2=16kappa. The V0/t term is an explicit repair of
this latter boundary problem, not an assumption that empty cells stay safe.

## A positive, smooth constraint solution for every fixed smooth datum

Assume a smooth compact connected leaf without boundary, smooth positive
lapse N, smooth b, and smooth epsilon0>=epsilon_min>0. These are fixed
canonical data. Minimize

    H[t]=integral N [m_g|Dt-b|^2+epsilon0/t],
    <t>_h=1, t>0.

The proof also supplies a lower bound, rather than presupposing t stays away
from zero. For 0<d<1 define the convex C2 regularization

    f_d(t)=1/t                         for t>=d,
           (t^2/d^2-3t/d+3)/d         for t<=d.

It is nonnegative, has a globally Lipschitz derivative for fixed d, and

    f_d(t)+t f_d'(t)=0                 for t>=d,
                       3(t-d)^2/d^3   for t<=d.

The regularized H_d has a unique mean-one H1 minimizer by Poincare
coercivity, weak lower semicontinuity and strict convexity. Its semilinear
elliptic equation is

    -2m_g div_h[N(Dt-b)]+N epsilon0 f_d'(t)+lambda=0.

Since f_d' has at most linear growth, elliptic regularity gives enough
classical regularity to evaluate the minimum. Full smoothness is not assumed
for the merely C2 regularization. Integration gives
lambda=-<N epsilon0 f_d'(t)>_h. Testing with t-1 gives

    lambda Vol_h
      =-integral N epsilon0 t f_d'(t)
        -2m_g||Dt||_N^2+2m_g<b,Dt>_N
      <=integral N epsilon0 f_d(t)+(m_g/2)||b||_N^2
      <=integral N epsilon0+(3m_g/2)||b||_N^2.

The last step compares with t=1. Define

    lambda_max=[integral N epsilon0+(3m_g/2)||b||_N^2]/Vol_h,
    C=lambda_max+2m_g||div_h(Nb)||_infinity.

At a minimum, div_h(NDt)>=0. If t_min<=d, then -f_d'(t_min)>=1/d^2,
and the equation would require

    N_min epsilon_min/d^2 <= C.

Choose d<min(1,sqrt(N_min epsilon_min/C)). This is a contradiction, so the
regularized solution lies everywhere above d. It solves the original 1/t
problem, and the same minimum argument now yields the actual bound

    t_min >= sqrt(N_min epsilon_min/C)>0.

For 0<t<d, 1/t-f_d(t)=(1-t/d)^3/t>=0, with equality above d.
Consequently every positive competitor has H>=H_d, while the regularized
minimizer has H=H_d. It is therefore a global minimizer of the original
functional, not merely a solution of its Euler equation.

Strict convexity gives uniqueness. The now smooth equation and this lower
bound give a finite elliptic upper bound on t (for the fixed smooth data
and geometry), with mean one fixing the constant. Elliptic bootstrapping
then gives a smooth solution. Thus all fixed smooth canonical data satisfying
the stated positive-floor hypothesis admit a positive finite carrier lapse.
No initial smallness of the carrier momentum was used.

The proof is an analytic continuum argument. The regularization, Hessian
and finite controls are checked separately; Lean algebra certificates do
not formalize its compactness or elliptic-regularity inputs.

## What this says about dark energy

On a homogeneous inactive FLRW leaf, t=1. With all carrier excitations zero,
V0 contributes exactly

    epsilon_vac=V0, p_vac=-V0.

Within this candidate, positive vacuum tension therefore has two explicit
roles: negative homogeneous pressure and a barrier against a degenerate
carrier lapse in the fixed-data constraint. This is a functional connection
derived from the action. It does not calculate the magnitude of V0 or prove
that nature uses this mechanism. Calling it “vacuum tension” is justified
for this specified constant contribution; other carrier excitations have
their own stress and charge.

The centered clock term vanishes on FLRW, so G_cosm=G_bare=cN G_N. If one
imposes a0^2=kappa^2 G_N V0 (energy-density convention, c=1), then

    H_vac^2=(8pi/3)cN G_N V0,
    (H_vac/a0)^2=8pi cN/(3kappa^2).

The acceleration relation remains an explicitly permitted constitutive input.
In SI, V0 is energy density, H_vac^2=8pi G_bare V0/(3c^2), and the last
ratio uses c H_vac/a0. Adding an independent bare Lambda would add another
vacuum contribution, so this variant has explicitly set it to zero.

At t=1, V0 does not change any carrier field equation, conversion threshold,
Floquet calculation or charge-current identity: its field derivatives vanish.
For fixed spatially varying t the transport theorem applies with
A=t/N and B=N/t. On R3 use energy relative to the constant vacuum background;
on the compact leaf the constant energy is finite. None of these facts
establishes evacuation efficiency or global evolution of the coupled metric.

## Remaining common-theory obligations

The fixed-data t result is only one elliptic constraint, with U,N,h held
fixed. Their simultaneous constraints and time evolution, full reduced
gravity kinetic matrix, field count, foliation continuation and the switching
metric/clock terms remain to be proved. The GNC host also still modifies
the exact globally filtered static target through its gate and interfaces.
Its bound on the inactive Newton response and its positive frozen scalar
block do not erase that modification. No historical observational pass is
transferred to CA4-GNC-P.
