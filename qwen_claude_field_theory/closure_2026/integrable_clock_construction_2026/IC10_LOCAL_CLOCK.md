# IC10: a local Einstein–clock plateau from the exponential primitive

2026-09-08. **Constructive local result; full relativistic MOND theory OPEN.**
This continues [the optical alignment calculation](OPTICAL_ALIGNMENT.md).
It does not retain IC9's old expanding solution or borrow its numerical
passes. The new background, constraint pair and evolution are recomputed.

## One complete candidate action, and its precise tested restriction

Retain all fields, constants, eta and boundary conventions of
[IC5_ACTION.md](IC5_ACTION.md). In particular 0<u<1, X>0, xi=ln N,
w=(u-1)xi, S=(2-u)xi, J9=exp(-2w-1/6), C=Lambda+a0² U(u²), and

    U(c)=(1-c)[ln²(1-c)-2 ln(1-c)+2]-2.

The proposed GLOBAL phase action is

    S10 = integral sqrt(-g) [2 P:Q-H10] + Sm[g,psi],

    H10 = H5 + eta {
      (2 P_TF²-p²/3)(1/J9-1)/m
      - m(J9-1) Rhat/2 + p² F Rhat/(2m a0²)
      + m alpha |D(xi+b u)|² }.

H5, F, alpha, b and the smooth eta are explicitly specified in the linked
IC5/IC4 definitions. There is no new empirical coefficient. The factor
exp(-1/6) is a design normalization at the earlier witness, not a derivation
of the observed Newton constant or of the fitted 1/2 in a0.

On eta=1 this becomes

    H10 = (2 P_TF²-p²/3)/(m J9) + m C-kappa X-m J9 Rhat/2.

Varying BOTH momentum components yields

    P_TF=m J9 Q_TF/2,  p=-m J9 Q,
    L10=m J9 [Q_TF²-2 Q²/3+Rhat]/2-m C+kappa X.

This follows by a stationary Legendre elimination, not a phenomenological
stress assignment. Outside eta=1 the momentum equation has eta derivatives;
the last compact Lagrangian is not valid there.

## Exact nonlinear local form on the expanding plateau

Let tilde g=exp(-2w)g, tilde X=-tilde g^{mu nu}T_mu T_nu/2,
S=-ln(2 tilde X)/2 and mstar=m exp(-1/6). Then

    xi=S+w,  u=(S+2w)/(S+w),
    Q=exp(-w) tilde K,  Rhat=exp(-2w) bar R.

The metric kinetic and spatial curvature density is exactly the ADM
Einstein density with coefficient mstar. Up to its usual boundary term,

    S10|eta=1 = integral sqrt(-tilde g) [mstar tilde R/2+P(tilde X,w)]
               + Sm[exp(2w)tilde g,psi],

    P = -m exp(4w){Lambda+a0² U([(S+2w)/(S+w)]²)}
        + kappa exp(2w) tilde X.

The w equation is algebraic in vacuum: P_w=0. Where P_ww is nonzero it
defines w=w(tilde X) locally and gives a local effective clock pressure
P_eff(tilde X). There is no inverse Laplacian or hidden w initial datum in
this restriction. This coordinate chart excludes S+w=0; the computation
does not use it to claim that xi=0 or y=0 is controlled.

The two metrics here are related by an invertible conformal field
re-expression on the stated chart; all ordinary matter still uses the
single original physical metric g. Conformal equality of null cones does
not imply equality of the physical weak-field potentials.

## Euler equations, characteristics and constraint preservation

In vacuum on this plateau, the independently varied equations are

    mstar tilde G_mu nu = P_eff,X T_mu T_nu + P_eff tilde g_mu nu,
    tilde nabla_mu(P_eff,X tilde nabla^mu T)=0,
    P_w=0 before algebraic elimination.

The clock principal matrix is
P_eff,X tilde g^{mu nu}-P_eff,XX tilde nabla^mu T tilde nabla^nu T.
On a timelike homogeneous background it has positive kinetic coefficient
Qclock=P_eff,X+2 tilde X P_eff,XX and speed squared P_eff,X/Qclock.
The tensor principal operator is the Einstein one with positive mstar.
Thus its physical null cone is the same as g's. This is an exact action
identity on eta=1, not an inferred tensor speed from a single isotropic fit.

For the auxiliary constraint it is essential to hold the CANONICAL clock
momentum fixed, not its velocity. At unit barred spatial volume let
subscripts S,w mean derivatives of the displayed P. Define

    PSS_eff=P_SS-P_Sw²/P_ww,
    PX=-P_S/(2 tilde X),
    Qclock=(PSS_eff+P_S)/(2 tilde X),
    Qbare=(P_SS+P_S)/(2 tilde X).

The primary is p_w=0, its secondary is C_w=H_w=-P_w, and their actual
Poisson-bracket block on a homogeneous background is

    [[0,A],[-A,0]],
    A=P_ww-P_Sw²/(P_SS+P_S)=P_ww Qclock/Qbare.

A multiplies the spatial delta distribution; this vacuum auxiliary has no
spatial derivative in its constraint block. A nonzero A fixes the p_w
multiplier upon preservation of C_w. No tertiary auxiliary constraint is
left, and the pair is second class. The code computes this block from P,
its singular values and rank, rather than entering rank=2 as a result.

After eliminating this pair, the remaining local theory is Einstein gravity
plus one first-derivative clock scalar. In ADM variables its lapse and three
shift momenta are primaries; preservation gives the Hamiltonian and three
spatial momentum constraints. The clock Legendre identity gives
H_p=v and H_{T_i}=V P_X h^{ij}T_j, so their product is p_T h^{ij}T_j:
the clock Hamiltonian bracket produces its spatial momentum contribution,
not an extra constraint. Combined with the Einstein bracket, the
diffeomorphism constraints close. Before eliminating w there are 12 pairs,
eight first-class constraints and the two second-class auxiliary constraints;
locally (24-16-2)/2=3 physical modes: **two tensors plus one genuine clock**.
This count is a plateau action argument, not a global IC10 Dirac certificate.
The numerical code checks the auxiliary block and Legendre identities,
not the entire nonlinear distribution-valued gravitational bracket.

For ordinary matter, varying its unchanged Sm[g,psi] under a compactly
supported infinitesimal diffeomorphism gives, on its own matter equations,
integral sqrt(-g) T_m^{mu nu} nabla_mu epsilon_nu=0. Integration by parts
gives nabla_mu T_m^{mu nu}=0. The interacting clock stress need not be
separately conserved in the physical frame. Matter-coupled clock kinetic
mixing must still be varied; the vacuum principal calculation is not that test.

## Genuine homogeneous evolution, separate from k!=0 perturbations

The code uses m=h0=1,kappa=6 and the unchanged IC5 a0²,Lambda values.
Solving P_w=0 afresh gives:

| S | u | PX | Qclock | cs² | physical H |
| --- | ---: | ---: | ---: | ---: | ---: |
| 0.10 | 0.492193 | 1.940700 | 5.259811 | 0.368968 | 0.719275 |
| 0.15 | 0.536585 | 1.755980 | 5.731699 | 0.306363 | 0.781459 |
| 0.20 | 0.570419 | 1.548515 | 5.841075 | 0.265108 | 0.807703 |

Here H is in h0 units; cs is relative to the shared physical null cone.
The auxiliary residuals are below 1e-50 and their computed ranks are two.
Finite differences independently check the eliminated pressure derivatives.
These are bounded numerical witnesses, not an interval-arithmetic theorem
or a proof of health for every allowed initial condition.

With tilde proper time tau, the exact vacuum FLRW equations are

    3 mstar Htilde² = rho_clock = -P_S-P,
    dS/dtau = 3 Htilde cs²,
    dln(bar A)/dS = 1/(3 cs²),
    bar A³ PX sqrt(2 tilde X) = constant,
    Hphysical=exp(-w) Htilde(1+3 cs² dw/dS).

Direct quadrature from S=0.1 to 0.2 yields 0.1085841845 barred e-folds,
0.08216385334 physical e-folds and 0.1107567421 tilde proper-time units.
The conserved charge agrees to the tested 45 decimal-place tolerance.
This is genuinely expanding and time-dependent; it does not impose K=0,
clock momentum=0 or H=0. It is emphatically not a realistic full cosmology.

The phase-space activation, re-evaluated on this NEW solution, is
r=exp(S)J9 Htilde/h0. It lies inside eta=1 at all three samples.
`plateau_boundary()` solves r²=5/4 on the continuation and records the next
boundary. Values at S=0.5 and 1 are also retained as continuation controls,
NOT full-candidate solutions: they lie outside eta=1. At S=1 the continued
plateau pressure has cs²<0. That failure cannot be hidden, nor can it be
assigned to the different full transition action without varying that action.

## What remains, in order

1. Continue the FULL phase equations through the newly located eta boundary,
   including eta momentum derivatives, then recompute the scalar principal
   operator and constraint rank there. Do not extrapolate P_eff beyond eta=1.
2. Derive the matter-coupled characteristic matrix and strong-coupling scale.
   A healthy vacuum linear cone is not a no-strong-coupling theorem.
3. Match the cosmological clock to a sourced galactic branch; independently
   derive Phi, Psi, baryon-only AQUAL, measured G and all PPN parameters.
4. Establish global k=0/y=0 control and a viable cosmological history.

At the static eta=0 plateau the action difference and all its first jets
vanish. The old exponential constitutive equation therefore survives under
the IC5 boundary prescription. This does NOT yet prove the required
baryon-only physical MOND equation or lensing. The a0–Lambda proportionality
and its 1/2 coefficient remain input, not a result. No empirical prediction,
global novelty claim, Lean proof or full-theory PASS is asserted.

Self-audit verdict: **computationally verified only in the stated range**,
with exact Legendre/conformal identities. The next missing implication is
healthy full-action evolution across eta's boundary, not another kernel fit.
