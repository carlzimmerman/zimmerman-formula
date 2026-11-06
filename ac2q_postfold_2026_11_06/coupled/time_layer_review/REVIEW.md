# Independent review: time-dependent regular planar corners

**Primary verdict: proved as written**, with the candidate's regular corner
class normalized explicitly below and the PF02 defect-free stress condition
retained. The proposed affine tangential correction is correct, with
sign -J v T. Stationary field profiles are unnecessary for this restricted
obstruction. This does not prove the existence, nonexistence, or uniqueness
of singular time-dependent layers.

## Claim card and provenance

At each event of a regular timelike planar interface, use a conformal chart
in which the interface is x=0. Fields alpha,beta,phi,P are continuous and
piecewise C1 up to the interface, with a common differentiable tangential
trace. Their normal one-sided derivatives are finite. The metric is
nondegenerate, Mpl^2>0, gamma>0, and s=phi_t at the trace is finite and
strictly positive. Both sides have X>0, strictly positive q=D+2X,
same-sign nonzero v=-phi_x/s, and 0<gamma exp(-2alpha)s^2<1/3.
Potential sources are bounded. The tested continuation has no surface
action, concentrated current/stress, or unresolved oscillatory defect and
satisfies both normal conjugate-flux and normal-stress balance.

Conclusion: the necessary corner conditions admit no distinct pair of
normal v and polarization-gradient states. The normal metric derivatives
are continuous. Arbitrary finite common tangential derivatives do not alter
the PF02 obstruction.

This is an independent delegated proof review from base e50f32a0a7. Exact
input SHA-256 values are recorded in `check_result.json`. The source action
is AC7_charge_switch/README.md; internal PF02 input is DERIVATION.md section
4. No external theorem is used. The current candidate, rather than the
previous stationary-only proof, is the object audited.

Continuity alone without sufficient trace regularity is not a substitute
for the common-tangential-derivative hypothesis. Likewise normal-stress
balance is part of the defect-free physical corner class; it must not be
claimed to follow from weak scalar/polarization Euler equations alone.

## Direct differentiation of the action

Write

    E=exp(2alpha+2beta), c0=exp(alpha+2beta), C=(1-v^2)^(-1/2),
    ell=P_x+2P beta_x, T=P_t+2P beta_t,
    B=exp(-2alpha)s^2(1-v^2), D=exp(-alpha)C(ell+vT).

At the interface s,T and all undifferentiated coefficients are common.
The on-branch matter density is

    Lm=E F,
    F=-D+B/2-W-V-gamma D^2/2-gamma D B.

Use Q=1+gamma(D+B) and Z=1/2-gamma D, so F_D=-Q and F_B=Z.
Holding s,ell,T fixed gives

    D_v=exp(-alpha) C^3(v ell+T).

The normal and temporal polarization currents are

    pi_P^x=-c0 C Q,
    pi_P^t=v pi_P^x.

The scalar currents, taking phi_t and phi_x as independent variables, are

    pi_phi^x=E Q D_v/s+2 exp(2beta)s v Z,
    pi_phi^t=E Q v D_v/s+2 exp(2beta)s Z.

In particular pi_phi^x=-Lm,v/s; pi_phi^t=Lm,s-v Lm,v/s when the partial
derivatives on the right use variables (s,v,ell,T). The temporal scalar
current cannot be obtained by incorrectly holding v fixed while varying
phi_t. Off branch the same formulas hold with Q=1 and Z=1/2+gamma B.

The gravitational first-order density is

    LG=Mpl^2 exp(2beta)[-2alpha_t beta_t-beta_t^2
                       +2alpha_x beta_x+beta_x^2].

Metric currents therefore are

    pi_alpha^x= 2Mpl^2 exp(2beta) beta_x,
    pi_alpha^t=-2Mpl^2 exp(2beta) beta_t,
    pi_beta^x= 2Mpl^2 exp(2beta)(alpha_x+beta_x)+2P pi_P^x,
    pi_beta^t=-2Mpl^2 exp(2beta)(alpha_t+beta_t)+2P pi_P^t.

These identities retain the tangential polarization coupling. Continuity
of normal conjugate currents and P forces first [beta_x]=0, then
[alpha_x]=0. The common tangential metric derivatives are already part of
the regular trace assumptions.

## Partial Legendre transform and convexity

Normal polarization-flux continuity fixes a common

    A=-pi_P^x/c0=C[1+gamma(D+B)], J=c0 A=-pi_P^x.

Holding the interface coefficients and A fixed, define f=Lm+J ell.
For z=D, the inverse affine change of variables is

    ell=exp(alpha)z/C-vT.

Hence, before even solving for z,

    f=E[F(z,B)+A z/C]-J v T.

Stationarity in z gives z=(A/C-1)/gamma-B, exactly the stationary PF02
elimination. Thus, including the common continuous potentials,

    f(v)=E f0(v;A,s_local)-J v T,
    s_local=exp(-alpha)s.

Here f0 is the PF02 partial transform. The affine term shifts the scalar
normal current by +J T/s equally on both sides. It changes neither f'''
nor v f'-f. The PF02 third derivative, multiplied by the positive E, is

    f'''=E (3v/gamma) {4epsilon^2
       +A/(1-v^2)^(5/2)[1-epsilon(3-2v^2)(1-v^2)]},
    epsilon=gamma s_local^2.

It is strictly positive on 0<v<1 for 0<epsilon<1/3. Consequently f' is
strictly convex. If two distinct positive velocities share f'=j, then
the integral of j-f' between them is positive, contradicting equality of
v j-f. Reflection covers two negative velocities. Equal velocities force
equal D and ell through fixed A, so there is no residual finite jump.

This calculation repairs the previously missing time-dependent implication
without dropping T. It does not extend the theorem to sign-changing flow,
null limits, irregular traces, or a surface defect.

## Normal Hamiltonian and tangential flux

The total canonical normal stress for the first-order reduced action is

    Hx=sum_i q_i,x pi_i^x-(LG+Lm)
      =HGx+v Lm,v+ell Lm,ell-Lm
      =HGx+v f_v-f.

The combination of P_x and beta_x matter terms is exactly ell pi_P^x.
The gravitational term HGx is continuous because both normal and tangential
metric derivatives are common. The -JvT contribution cancels from v f_v-f.
There is no unaccounted temporal term in this normal Legendre transform:
time derivatives are held fixed, not included among the transformed normal
variables.

For the canonical tangential momentum/energy flux,

    tau^x_t=sum_i pi_i^x q_i,t,

normal-current continuity and common tangential derivatives already imply
[tau^x_t]=0. Temporal currents themselves may jump: for example
pi_P^t=v pi_P^x changes when v changes. A finite jump of a temporal current
at a fixed x=0 interface creates no delta under partial_t. Such a jump is
not a surface current and does not invalidate the normal-flux conditions.
For a moving interface one must first use adapted coordinates or retain
the interface-velocity terms in distributional differentiation.

## Thin-layer surface balances: what survives without regularity

Write the reduced field equations as

    partial_a pi_i^a=L_,q_i, a=t,x.

Suppose a thin family has distributional limits consisting of bulk currents
plus finite surface measures j_i^a(t) delta(x), and the source has bulk plus
r_i(t) delta(x), with no dipole source. For a fixed interface,

    j_i^x=0,
    [pi_i^x]+partial_t j_i^t=r_i.

The first equation is the delta-prime coefficient; the second is the delta
coefficient. Thus a nonzero surface temporal current can change the ordinary
normal-flux matching. If dipoles are allowed, the first equation changes;
this regular measure ansatz must not be imposed on a more singular limit.

For the total reduced canonical translation stress

    tau^a_b=sum_i pi_i^a q_i,b-delta^a_b L,

on-shell translation invariance gives partial_a tau^a_b=0 (no external
coordinate-dependent source). A limit with surface coefficient sigma^a_b
therefore satisfies

    sigma^x_b=0,
    [tau^x_b]+partial_t sigma^t_b=0.

These are reduced canonical balance equations, not an identification of
canonical gravitational energy with a covariant local matter stress tensor.
For physical surface stress one must use the Hilbert stress and Einstein
matching conditions. Where metric derivatives have a common bounded trace,
the densitized mixed Hilbert balance has the analogous form

    partial_mu(sqrt(-g) T^mu_nu)
      -1/2 sqrt(-g) T^{alpha beta} partial_nu g_alpha beta=0.

If its surface coefficient is S_dens^{mu nu}, absence of dipoles requires
S_dens^x_nu=0 and the delta balance is

    [sqrt(-g) T^x_nu]+partial_t S_dens^t_nu
      -1/2 S_dens^{alpha beta} partial_nu g_alpha beta|Sigma=0

in the planar chart. With discontinuous metric derivatives this product
requires a justified junction prescription or a specified thin-limit
construction; the displayed regular-coefficient formula alone is inadequate.
Any proposed physical surface stress must also satisfy the full Einstein
constraints and junction equations, not only reduced conservation.

## What is required for a nonzero defect or unique stress

Uniformly bounded current/stress densities on a layer of width tending to
zero have vanishing integrated surface content. A nonzero surface measure
requires concentration (typically order inverse width in an integrated
component), or another explicitly characterized noncompact nonlinear limit.
Large temporal derivatives alone do not prove a defect: distributional
differentiation is continuous, so if the integrated temporal current tends
to zero distributionally its time derivative also tends to zero. Fast
oscillations without concentration can instead require a Young-measure or
bulk-defect analysis, which is not supplied by the surface-measure ansatz.

The balances constrain a defect if one exists. They do not construct it,
prove it is generated from smooth data, or determine its initial surface
content. Even known normal stress jumps determine only time derivatives
of some surface components; integration constants, remaining components,
constitutive information, and Einstein consistency remain. Unique stress
requires an independently established native evolution/limit with specified
initial data and uniqueness, or an additional admissible surface model.
No choice of entropy rule or flux balance alone supplies this proof.

## Obligation matrix and verification

| Obligation | Status |
| --- | --- |
| Normal and tangential currents from the action | passed |
| Metric normal-derivative continuity in the regular class | passed |
| Affine -JvT correction and its sign | passed |
| Normal-stress cancellation and PF02 convexity implication | passed |
| Extension to irregular traces or opposite-sign velocities | out of scope |
| Measure surface-balance identities under the stated ansatz | passed |
| Existence, uniqueness, or native selection of a nonzero defect | not addressed |
| Full coupled weak-solution construction | not addressed |

`check.py` verifies eight exact symbolic identities, all passing in
`check_result.json`. Command:

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python ac2q_postfold_2026_11_06/coupled/time_layer_review/check.py > ac2q_postfold_2026_11_06/coupled/time_layer_review/check_result.json

Those checks support algebra only. The trace assumptions and measure-limit
conditions above are separate analytic hypotheses. The cheapest next step
for the defect route is to formulate and prove a specific compactness and
surface-initial-data result, rather than infer a unique surface stress from
the corner mismatch.
