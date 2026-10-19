# Complete Born kernel and the charged-proton infrared endpoint

FSP-008 proton route, 2026-10-19. All new numerical results below are for a precisely specified point-Dirac benchmark, not a pointlike model substituted for the physical proton. No empirical alpha, proton form-factor parametrization or cosmological target is an input.

## 1. The actual full-current integral

Let u=e²=4 pi alpha. The canonical QCD current is j_mu=sum_f Q_f qbar_f gamma_mu q_f, with no e. Work to first order in u around massive, infinite-volume QCD, holding its MSbar strong coupling and renormalized quark masses fixed at a declared reference scale. A complete result additionally specifies the electromagnetic charge convention; scheme changes of charge begin beyond this first u derivative. Spin-average relativistically normalized external proton states. Define the Euclidean H_mu,nu(x)=<p|T j_mu(x)j_nu(0)|p>_vacuum-subtracted/(2m). Vacuum-subtracted means connected to the external proton state through the gauge ensemble, not restriction to quark-line-connected contractions. Then

    M_u(reg) = (1/2) integral d4x H_mu,nu(x) D_mu,nu(reg)(x) + M_u(counterterms).

This is the coupling-stripped version of Feng–Jin 1812.09817v1 equations (1)-(2). It needs the temporal and spatial components, the entire relative separation, same-loop and separate-loop determinant responses, current/action contacts, and the renormalization insertions. The continuum Dirac benchmark has no elementary A² seagull. A lattice implementation's conserved-current or action seagulls cannot simply be omitted. Quark-mass and strong-coupling counterterms and their finite parts specify the fixed-MSbar path; see the preceding FSP-007 sea/OPE route. A finite photon integral is not by itself a renormalized QCD mass derivative.

For the scalar amplitudes T_1,T_2 of Walker-Loud–Carlson–Miller (WLCM), 1203.0254v2 equations (2)-(7), write Q=|Q_E|, x=Q_4/Q, z=Q/(2m). A multiplicative radial photon regulator P(Q²), defined by D_E(Q)=P(Q²)/Q² in Feynman gauge, gives

    M_u(reg)/m = 1/(32 pi³ m²) integral_0^infinity dQ² P(Q²)
        integral_-1^1 dx sqrt(1-x²)
        [-3 T_1(iQx,Q²)+(1-x²) T_2(iQx,Q²)].                 (1)

The spin average is already included. Equation (1) follows directly from WLCM's alpha/(8 pi² m) prefactor and u=4 pi alpha. Its subtraction-only contribution is -3/(64 pi² m²) integral dQ² P(Q²) S_1(Q²), agreeing with FSP-006; it is only one term of (1). One imaginary-energy line, one spatial temporal moment, or a p-n difference does not provide (1) for the individual proton.

## 2. A convention-complete Born sector

Separate the standard on-shell spin-1/2 Born graphs, including their non-pole Dirac term, from the remaining transverse tensor. Define

    tau=z², G_E=F_1-tau F_2, G_M=F_1+F_2,
    A=F_1²+tau F_2²=(G_E²+tau G_M²)/(1+tau).

The corresponding amplitudes at imaginary energy are

    T_1^B = 2 [ z² G_M²/(z²+x²) - F_1² ],
    T_2^B = 2 A/(z²+x²).                                    (2)

The polynomial -2 F_1² is part of this Born convention. Omitting it or treating all of the pole tensor as unsubtracted gives the elastic inconsistency diagnosed by WLCM. In particular S_1^B=2(G_M²-F_1²), as in its equation (18a). A redistribution of regular transverse terms between Born and non-Born pieces changes neither the complete tensor nor (1), but must be stated before naming a partial integral.

Using

    I_0(z) = integral_-1^1 sqrt(1-x²)/(z²+x²) dx
           = pi [sqrt(1+z²)/z - 1],
    I_2(z) = pi/2-z² I_0(z),

the complete Born angular kernel is

    M_u^B(reg)/m = 1/(2 pi²) integral_0^infinity dz P(4m²z²) B(z),
    B(z) = z(3F_1²-A)/2
           + [(1+z²)A-3z² G_M²] [sqrt(1+z²)-z].             (3)

An orthogonal comparison is WLCM equation (11), the dispersive elastic integral, PLUS equation (18a), its elastic subtraction. In units alpha/pi times dQ their sum is

    E(z) - (3z/2)(G_M²-F_1²),
    E(z) = 3z G_M²/[2(1+z²)]
       + (G_E²-2z²G_M²)/(1+z²)
           [(1+z²)^(3/2)-z³-3z/2].                          (4)

This equals B(z) exactly. Applying equation (11) alone would retain a spurious term proportional to z(G_M²-G_E²) in the soft expansion. Equations (2)-(4) give a practical all-component Born benchmark for a full position-space or momentum-space proton calculation. They still require the QCD F_1,F_2 for the physical elastic contribution; none is fitted or imported here.

## 3. A real physical-proton coefficient without form-factor fitting

For a stable charged proton in QCD with positive pion mass, F_1(0)=1, F_2(0)=kappa is finite and the QCD form factors are analytic at Q²=0. Write F_1=1+a z²+O(z4), F_2=kappa+b z²+O(z4). Equivalently G_E=1-(2/3)m² r_E² z²+O(z4). Equation (3) gives

    B(z)=1+c z²+d z³+O(z4),
    c=-3/2-4 kappa-2 kappa²-(4/3)m² r_E²,
    d=2+6 kappa+(3/2)kappa².                               (5)

In particular, the coefficient linear in z is exactly zero after the Born subtraction is included. The non-Born low-energy tensor starts at quadratic photon momenta for a gapped QCD spectrum. Thus for a sharp SO(4)-invariant soft photon window 0<Q<epsilon m, its contribution to (1) starts at order epsilon4, while

    (1/m) M_u(soft window)
      = epsilon/(4 pi²) + c epsilon³/(48 pi²)+O(epsilon4),
    lim_epsilon->0 [ M_u(soft window)/(epsilon m) ]=1/(4 pi²). (6)

This is an actual universal endpoint of the physical-proton kernel under the stated QCD gap/analyticity assumptions. In alpha units the limit is 1/pi. It uses unit charge, not the measured value of alpha or kappa. It is not the total proton electromagnetic self-energy, and it cannot be extrapolated to epsilon of order one. It is defined before local parameter-matching counterterms are added to the full integral. The kernel partition itself is not a separately measured mass.

## 4. Exact full point-Dirac benchmark

Now choose a different, completely specified theory: one free massive, unit-charge Dirac field at u=0, with F_1=1,F_2=0 and no inelastic states. This is a kernel verification theory, not QCD. All of its first-order current tensor is Born. Then

    B_D(z)=2z³+(1-2z²)sqrt(1+z²)
          =[sqrt(1+z²)+2z]/[sqrt(1+z²)+z]² > 0.             (7)

The second expression is numerically stable at large z. An independent Euclidean self-energy trace gives the angular integrand 2(1+2x²)/(z²+x²), reproducing (7). An exact primitive is

    F_D(z)=[2z4+z(1-2z²)sqrt(1+z²)+3 asinh z]/4,
    integral_a^b B_D(z) dz=F_D(b)-F_D(a).                   (8)

Consequently a finite photon shell has the exact no-fit result

    M_u^D(Q_a,Q_b)/m=[F_D(Q_b/2m)-F_D(Q_a/2m)]/(2 pi²).

For the benchmark 0<Q<m this reduces to

    M_u^D(0,m)/m = (1+sqrt(5))/(64 pi²)
                   +3 log[(1+sqrt(5))/2]/(8 pi²).          (9)

Its ultraviolet log derivative is 3/(16 pi²) per log Q², the Dirac mass anomalous-dimension check. This differs from the QCD gluonic sea band of FSP-007: these are different theories and operators.

## 5. A 2026 regulator permitting a complete all-momentum convolution

Erb–Meyer–Ottnad 2603.13086v1 equations (2.3)-(2.4) uses a doubly Pauli–Villars photon. Its momentum-space multiplier is

    P_Lambda(Q²)=1-2Q²/(Q²+Lambda²/2)+Q²/(Q²+Lambda²)
        =Lambda4/[2(Q²+Lambda²/2)(Q²+Lambda²)] > 0.          (10)

Unlike a hard photon band this permits the complete point-Dirac integral over 0<Q<infinity. Let lambda=Lambda/m. We compute

    D(lambda)=M_u^D(PV)/m
      =1/(2 pi²) integral_0^infinity dz
          B_D(z) lambda4/[2(4z²+lambda²/2)(4z²+lambda²)].   (11)

The comparison paper's actual QCD observable is HVP, not a proton matrix element; its N451 pion mass is 286 MeV, and it explicitly does not compute the counterterm. It supplies a useful regulator and factorization method, not the missing proton data.

The exact primitive (8) has F_D(z)=(3/4)log(2z)+3/16+O(z^-2). Also the difference between the smooth cutoff and a sharp Q<Lambda cutoff, integrated against dQ/Q, is -log 2. Therefore

    D(lambda) = [3 log(lambda²)+3/2-6 log 2]/(16 pi²)+o(1). (12)

Equation (12)'s constant is for this photon regulator. It is not an MSbar or on-shell finite counterterm by itself. We retain a symbolic finite matching constant rather than declare a renormalized proton response. At fixed g_MSbar,m_f_MSbar a complete QCD calculation must compute the corresponding quark and gluon insertions and the convention-dependent finite matching. No adjustment to reproduce alpha or the cosmological ratio is made.

## 6. What this does and does not close

The new step is the full Born T_1/T_2 convolution, an exact all-component point-Dirac reference, the physical charged-proton infrared coefficient, and a positive regulator usable with the 2026 factorization method. These supply real executable checks on a future full tensor implementation. They do not determine physical QCD F_1,F_2 over all Q, the non-Born tensor, the full sea covariance, finite QCD matching, or the global S4 vacuum functional. Therefore neither R(alpha) nor its full derivative is evaluated here. In particular a photon-band infrared mass coefficient is not an H-linear gravitational vacuum coefficient.

All identities in this derivation were written before the authoritative bounded calculation. The finite assertion and reproduction command are fixed in COMPUTATION_CONTRACT.json and REPRODUCE.md. Any later amendment requires a new input hash/run.
