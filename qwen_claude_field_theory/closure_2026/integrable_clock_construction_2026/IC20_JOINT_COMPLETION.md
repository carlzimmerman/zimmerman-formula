# IC20: a joint kinetic/curvature action, not full closure

Base: `8a1b4c020c399678fba987c8433059d8ff7b9f12`, 2026-09-08.
**Full theory OPEN.** This is a constructive solution of two previously
incompatible local design conditions, with a varied expanding witness. It is
not a complete cosmology or a certified relativistic MOND theory.

Credit: Carl Zimmerman supplied the exponential acceleration law, vacuum-scale
relation and primordial-clock direction motivating this work. The action
engineering and computations here test that direction; they do not derive
the coefficient 1/2 in his scale relation. No global novelty or empirical
claim, independent referee certification, or Lean proof is made.

## 1. Solve both compatibility equations before choosing functions

Write q for canonical trace momentum density, R for barred spatial curvature,
S for the clock lapse coordinate, and t for the trace-free kinetic coefficient.
The IC19 necessary local scalar and tensor conditions were

    (H_qq+t/3) H_RR-H_qR²=0,     t*(-H_R)=exp(2S).

Set v=-H_R>0. Where H_RR is nonzero, the partial Legendre transform
K(S,q,v)=H+vR satisfies K_v=R and

    K_qq=H_qq-H_qR²/H_RR=-exp(2S)/(3v).
    K=-exp(2S)q²/(6v)+a(S,v)q+b(S,v).

This integrates the two local conditions together. It is not yet a field
theory health theorem. An analytic auxiliary chart avoids a singular v
coordinate at the static endpoint:

    v=v0+z²,   v0=m exp(S+2w)/2,
    a q=-A(S)qz,
    b=-exp(S)P0(S,w)-D(S)z²-E4(S)z⁴.

z is an independent varied auxiliary, not a prescribed curvature function.
Use z as the field on both sides of zero; never differentiate sqrt(v-v0)
there to count modes.

## 2. One explicit global phase action

Use the physical metric, varied timelike clock T, six independent tangent
components P, and integrable canonical map in IC5_ACTION.md. In particular

    X=-g^{mu nu} T_mu T_nu/2>0, N=(2X)^(-1/2), xi=ln N,
    w=(u-1)xi, S=xi-w, xi=S+w, 0<u<1,
    Q_ij=K_ij-h_ij n^mu partial_mu w,
    hbar=exp(-2w)h, V=sqrt(hbar), q=pi/V=exp(3w)p,
    R=exp(2w) Rhat, N sqrt(h)=V exp(S+4w).

The clock coordinate chart additionally excludes xi=0. Introduce scalar z
and multiplier L. With all gradients below barred, define the scalar F20 by

    F20 = exp(2S)/v [exp(6w) P_TF²-q²/6]
          -A(S)qz-exp(S)P0(S,w)-D(S)z²-E4(S)z⁴-v R
          -m exp(S+2w)[2u xi Dxi.Du+xi²|Du|²]
          -eta exp(S)L(w-wc),
    H20physical=exp(-S-4w) F20,
    I20=integral sqrt(-g)[2P:Q-H20physical]+Sm[g,psi].

Here eta is the IC18 one-sided smooth activation, now with the IC19 argument
r=-p/(3mh0); eta=0 for r²<=1/2 and eta=1 for r²>=3/4. All appearances use
this same argument. The off-pin functions are

    Xtilde=exp(-2S)/2,
    P0=-m exp(4w)[Lambda+a0² U(u²)]+kappa exp(2w)Xtilde,
    U(c)=(1-c)[ln²(1-c)-2ln(1-c)+2]-2.

Take wc=-1/40, m=h0=1, kappa=6 in the numerical units and Lambda from
ic19_normalized_spatial.constants(); a0²=Lambda/(32pi) is imposed. This
revision has NO pole-clock pressure and inherits NO IC18/IC19 early history.
No old curvature square, switched pressure, or extra gradient term is implicit.

The positive coefficient functions are fully specified by

    tau=S-0.1,
    A=A_* exp(a1 tau),
    D=D_* exp(d1 tau+d2 tau²/2),
    E4=E_* exp(e1 tau).

`design()` defines their constants uniquely from its displayed linear systems,
positive D_*, negative square-root choice for Z, and input targets at
S=.1,q=-3,z=1,R=0: A_*=E_*=.1, H_SS=-3 after eliminating z,
H_Sq=0, actual UV scalar speed squared .2. Targets are action-design inputs,
not claimed predictions. Derived constants and actual residuals are in the
run output. The symbol `a0` in that coefficient dictionary means A_*, NOT
the MOND scale (which is `a02` in the inherited constants).

## 3. Vary the action; do not assign auxiliary equations

The exact IC5 symplectic map gives canonical pi^{ij} dot hbar_ij. L variation
sets w=wc wherever eta>0. The w equation determines L, including all gradient
and matter terms. At the pin the reduced Hamiltonian is

    H/V = t |pi_TF/V|²+h(S,q,z,R)-B(S)|DS|²+Hm/V,
    t=exp(2S)/v, B=m exp(S+2wc)(1-u²)>0,
    h=-exp(2S)q²/(6v)-Aqz-exp(S)P0-Dz²-E4z⁴.

There is no factor (1-eta) multiplying B. The canonical Euler equations are
dot hbar=delta Htot/delta pi, dot pi=-delta Htot/delta hbar, the spatial
momentum constraint, and the varied auxiliary equations

    C_z/V=t_z |pi_TF/V|²+h_z=0,
    C_S/V=t_S |pi_TF/V|²+h_S+(Hm/V)_S
            -B_S|DS|²+2 D_i(B D^i S)=0,
    h_z=exp(2S)q²z/(3v²)-Aq-2(D+R)z-4E4z³.

Eliminating z locally gives H_ab=h_ab-h_az h_bz/h_zz, for a,b=S,q,R.
The executable differentiates h itself; the Hessian entries are not assigned.
On h_z=0,

    h_zz=Aq/z-4 exp(2S)q²z²/(3v³)-8E4z²,
    aUV=t/6+H_qq/2=-h_qz²/(2h_zz),
    H_qR=2z h_qz/h_zz, H_RR=-4z²/h_zz.

For q<0,z>0,A,E4>0 the auxiliary derivative is negative and aUV positive.
At q=z=0, h_zz=-2(D+R); the original static Hamiltonian value and first
q,z,R jets are recovered for the regular branch R>-D. This is a static
restriction/first-variation statement, NOT a matched galactic solution.

## 4. Actual constraints and preservation in the tested sector

After pin elimination the primary constraints are p_S=p_z=0 plus the three
shift momenta; secondaries are C_S,C_z and spatial momentum constraints.
Before elimination also retain p_w,p_L, C_L proportional to w-wc and C_w
which solves L. These four form the regular holonomic pin sector on eta>0.
The first-order metric momentum P has already been put in canonical form;
it must not be counted as six extra configuration fields with new dynamics.

For homogeneous isotropic data, the (S,z) auxiliary block at spatial k is

    A(k) = [[h_SS-2B k², h_Sz], [h_Sz,h_zz]],
    PB = [[0,-A], [A,Dsecondary]],
    Dsecondary_ij = (3/2)(f_i f_jq-f_iq f_j)
                 +(2k²-R)(f_iR f_jq-f_iq f_jR),  f=(h_S,h_z).

Unit barred volume is used in this mode matrix. The 2k² term follows from
delta R=(4k²-2R)zeta and the scalar symplectic pair {zeta,delta pi}=1/2.
It was missing from an initial draft and is now tested against direct
canonical derivatives. A minisuperspace bracket alone is not the k!=0 matrix.
The code forms PB and computes its determinant, singular values and rank.
At the witness h_zz<0 and the reduced H_SS=-3<0, B>0; therefore A(k) is
negative definite for every k²>=0, so PB is invertible independently of D.

For vacuum homogeneous data preservation gives, without assigning multipliers,

    Qdot=h_q/2, qdot=-3h/2+R h_R, Rdot=-h_q R,
    A(0) (Sdot,zdot)^t = -(3Qdot f+f_q qdot+f_R Rdot).

Thus preservation fixes both multipliers, with no new homogeneous constraint
on this regular branch. This is genuine closure of this auxiliary subsystem,
not an evaluation of all nonlinear inhomogeneous functional brackets.

The local regular count with shifts included is 13 configuration variables,
six spatial first-class constraints and eight second-class auxiliary
constraints: (26-12-8)/2=3 physical modes. These are two tensors plus ONE
explicit clock scalar. The rank calculation, not this arithmetic, is the
load-bearing local input. Global rank, boundary invertibility and interactions
remain unproved. The k=0 homogeneous isotropic truncation has one Q canonical
pair after removing auxiliaries; spatial gauge constraints vanish in that
truncation, so do not apply a nonzero-mode count to it unchanged.

## 5. Tensor and time-dependent scalar equations

Pure tensor variation on isotropic data gives positive kinetic coefficient
t and cT²=-t h_R/exp(2S)=1. Vector gravitational perturbations are constrained
by spatial diffeomorphisms in this local regular count; general anisotropic
mixed perturbations have not been diagonalized.

For flat vacuum FLRW, write hbar_ij=exp(2Q+2zeta)delta_ij. Solving the scalar
momentum constraint gives |delta pi_TF/V|²=(delta pi/V-3q zeta)²/6. Define
delta q=delta pi/V-3q zeta. The quadratic symplectic term is 2V delta q zetadot.
The background volume mass (9/2)V(h-qh_q)zeta² cancels 3 pidot zeta² from
the integration by parts of 6pi zeta zetadot, using the varied background.

With C=H_Sq, M=H_SS-2B k², d=H_qR, e=H_SR, a=aUV, the remaining Hamiltonian is

    H2/V=K delta q²+2L delta q zeta+W zeta²,
    K=a-C²/(2M), L=2d k²-2C e k²/M,
    W=-2v k²+8H_RR k⁴-8e² k⁴/M.

The actual time-dependent Euler equation is

    zetaddot+(3Qdot-Kdot/K)zetadot
      +[K W-L²-Ldot+(Kdot/K-3Qdot)L]zeta=0.

Here k²dot=-2Qdot k². Freezing L before differentiating loses leading k²
physics. The exact Euler identity and numerical along-flow derivatives are
both checked. At C=0 define rho_mix=d/a and

    cUV²=(-2av+4a e²/B)/exp(2S)
          -2a[dot rho_mix+Qdot rho_mix]/exp(2S),
    cbase=cUV²-4a e²/[B exp(2S)],
    cIR_ratio=cbase+2 Cdot e/[exp(2S) H_SS].

The complete all-wavelength coefficient at the design point is exactly

    omega²/[exp(2S)k²]
       =[H_SS cIR_ratio-2B k² cUV²]/[H_SS-2B k²].

For this action choice cIR_ratio is approximately .35003935, cUV²=.2 and
K=a approximately .12638695. Both weights are positive for all k²>=0 after
multiplying numerator and denominator by -1. This establishes positivity of
this oscillator coefficient for every k!=0 at this point, conditional on the
numerically evaluated coefficient signs; the algebraic interpolation is exact.
The k=0 equation has zero gradient restoring term, not an omitted scalar pole.
Finite-k omega²/k² is NOT a signal velocity. Only the characteristic limit
gives the stated subluminal scalar cone. Time-dependent growth, interactions,
and physical instantaneous response are not settled by this result.

## 6. Evolving backgrounds and ordinary matter

The vacuum continuation solves h_S=h_z=0 at changing q, with multiplier
predictors. The independent conserved charge Vh checks the integrated scale
factor. The main run follows 10 steps of dq=.0001, about .00055275 e-folds:
a genuinely evolving but very short interval, NOT cosmological viability.

For minimally coupled homogeneous dust and radiation their canonical
Hamiltonian can be parameterized, absorbing the fixed conformal factors into
nonnegative conserved amplitudes, as

    Hm/V=exp(S)[Md exp(-3Q)+Mr exp(-4Q)]=hD+hR.

Vary it together with h. The lapse equation is h_S+hD+hR=0; the z equation
is unchanged. The canonical equations give

    Qdot=h_q/2, qdot=-3h/2+hR/2,
    A_matter=A(0)+diag(hD+hR,0),
    source_S=3Qdot C_S/V+h_Sq qdot-Qdot(3hD+4hR),
    source_z=3Qdot h_z+h_qz qdot.

Solve A_matter(Sdot,zdot)^t=-source. The total autonomous Hamiltonian
exp(3Q)(h+hD+hR) is conserved. The run solves both auxiliary constraints and
this charge at prescribed Q, then independently checks integrated qdot/Qdot.
Md=Mr=10^-6 over .0001 e-folds probes the local matter branch only. It is
not radiation domination, recombination, or a coupled perturbation test.

Sm depends only on g and its own matter fields. Its own diffeomorphism
variation gives integral sqrt(-g) T^{mu nu} nabla_mu xi_nu plus matter Euler
terms; integrating by parts gives nabla_mu T^{mu nu}=0 on matter shell.
This ordinary-matter identity is not conservation of a pooled effective stress.

## 7. Adverse control and exact outstanding obligations

Changing the action-design H_SS input to -1000 extends the sampled vacuum
background to .35977 e-folds and admits larger homogeneous matter amplitudes,
but its finite-k omega² is negative (the report recomputes k²=.0001), while
its UV coefficient stays positive. That DIFFERENT parameter choice must not
donate its longevity to the main action's healthy-point claim. The recorded
control is a diagnostic against falsely equating UV health with full stability.

The main action still requires a useful long evolving branch with full
matter/clock scalar and vector perturbations, general nonlinear constraint
closure, boundary/instantaneous-channel analysis, interaction scales, static
matching through eta=0, controlled zero field, independent Phi/Psi, measured
Newton constant, all PPN coefficients, and empirical galaxy/cluster/CMB fits.
The static primitive alone supplies none of those certifications. Strict
execution therefore exits 2 after successful local checks. No complete-theory
PASS is emitted. The next calculation should vary the coupled matter/clock
quadratic action on the current regular branch, while constructing coefficients
whose all-wavelength positivity persists along a useful cosmological interval.
