# TP02-MC: what the specified action actually couples to

This derives conditional occupied-state energies from the rigid canonical-K SU(5) action in `microscopic_vacuum_2026_10_28/INVERTED_HIERARCHY.md` and TP01's actual representation blocks. It does not add a new species, particle abundance, interaction, gauge-singlet construction or gravity completion. The original kinetic-only waterbag is a comparator.

## Actual massive modes: rest energy cannot be removed from the source

At constant T, diagonalizing the canonical quadratic action gives each physical massive mode the relativistic dispersion E_a(p,s)=sqrt(p^2+m_a(s)^2), s=ln(|T|/|T_v|). In a local slowly varying eigenbasis this is the leading adiabatic/WKB Hamiltonian, not an exact result on arbitrary gradients. Changing eigenvectors produces connection/off-diagonal derivative terms and possible transitions. Neglecting them requires adiabatic gaps, an occupation prescription and collision terms controlled on the time scale in question.

For phase-space occupations f_a, with the measure including spin/representation degeneracies,

    epsilon_m = sum_a integral f_a E_a,
    P_kin = sum_a integral f_a p^2/(3E_a),
    C := partial_s epsilon_m = sum_a integral f_a m_a m_a,s/E_a.

The same coupling enters the scalar equation U_s+C=0 in the local static elimination, and the quasiparticle force dp/dt=-(m m_s/E) grad s. In a homogeneous evolving background, epsilon_m_dot+3H(epsilon_m+P_kin)=C s_dot. Covariantly in signature (-,+,+,+), div T_m^{mu nu}=-C partial^nu s; the scalar stress has the opposite divergence. Thus the energy drawn from one sector is deposited in the other by the same action. This is reciprocal work, not an independently adjustable heating reservoir.

The nonrelativistic expansion is epsilon_m=n m(s)+K_2(n)/m(s)+..., where an isotropic filled phase-space sphere has K_2 proportional to n^(5/3). If beta=dln m/ds then C=beta[n m-K_2/m]+... . The rest term dominates in a cold state. It cancels out of P=n partial_n epsilon-epsilon at fixed s but remains in the stationary scalar equation and in the relaxed compressibility. Subtracting n m(s) would change the interaction; subtracting only a constant reference mass n m(s0) does not remove its scalar derivative.

For the unbroken SU(3) adjoint Weyl block, M=3hX, q=2 lambda a, a^2=2fh/(30h^2+lambda^2), the canonical complex symmetric matrix is unitarily congruent to [[M,q],[q,0]]. Its positive singular masses are

    m_H=(sqrt(M^2+4q^2)+M)/2,
    m_L=q^2/m_H,
    dln m_H/ds=+M/sqrt(M^2+4q^2),
    dln m_L/ds=-M/sqrt(M^2+4q^2).

Their product is q^2. Heavy/light rest and kinetic energies have opposite scalar slopes. At large X their masses scale as X and X^(-1), respectively; neither supplies a field-independent rest energy plus inertial mass proportional to X^2. The SU(2) adjoint has the analogous result with |(1+r)hX| and |r lambda a|. Vector masses also vary: m_V=5g sqrt(a^2+b^2), with logarithmic slope b^2/(a^2+b^2). Constant-mass singlets and the massless modes do not supply a local scalar rest source at this order; basis/gradient interactions are a separate question.

These adjoint modes carry unbroken gauge charges. Their independent particle numbers are not symmetries of the interacting action. In particular the SU(3) scalar H_minus is its fermion squared-mass matrix minus diag(3c,0), c=fh lambda^2/(30h^2+lambda^2)>0. Its light eigenvalue is strictly smaller while remaining positive. Decay of the Weyl mode to a lighter adjoint scalar plus the massless Goldstino is kinematically open, with gauge representation and fermion parity compatible; no lifetime has been calculated. An instantaneous gas is therefore only a conditional quasiparticle-state probe, not a derived stable cold component. Interactions, annihilation, confinement and massless radiation cannot be dismissed by assigning an abundance.

## General occupied-state pressure and moment closure

For any explicit state parametrized by a genuinely conserved/frozen number n, let epsilon(n,s)=U(s)+epsilon_m(n,s), and eliminate s on epsilon_s=0 with D=epsilon_ss>0. Then

    P=n epsilon_n-epsilon,
    dP/dln n=n^2[epsilon_nn-epsilon_ns^2/D].

This Schur complement is the actual relaxed compressibility. There is no universal Uss>3Us criterion for arbitrary mode-derived energies.

For a filled isotropic fermion sphere with degeneracy g_occ,

    n=g_occ p_F^3/(6 pi^2), E_F=sqrt(p_F^2+m^2),
    epsilon_nn=p_F^2/(3n E_F), epsilon_ns=m m_s/E_F,
    D=Uss+g_occ/(2 pi^2)[(m_s^2+m m_ss)J0-m^2 m_s^2 J1],
    J0=[p_F E_F-m^2 asinh(p_F/m)]/2,
    J1=asinh(p_F/m)-p_F/E_F,
    dP/dln n=n p_F^2/(3E_F)-n^2 m^2 m_s^2/(E_F^2 D).

The exact source is C=g_occ m m_s J0/(2 pi^2). For the light eigenbranch m_s<0 this permits Us>0; for the heavy branch m_s>0 it requires Us<0. Specifying the occupied branch changes the force balance, rather than deriving the old relative-motion-only portal.

## Model-native phase current: a constructive different material state

The actual complex valley coordinate has canonical kinetic term |partial T|^2. Put T=R exp(i theta), R=|T_v|exp(s). In a homogeneous state its cyclic-phase momentum is n=q_theta=2R^2 theta_dot. Legendre transformation at fixed n gives

    epsilon(n,s)=n^2/(4R^2)+U(s),
    U_s=n^2/(2R^2), D=Uss+2Us,
    P=n^2/(4R^2)-U=Us/2-U,
    dln n/ds=D/(2Us),
    dP/dln n=Us(Uss-2Us)/D.

This produces an exp(-2s) term from the specified action, but its coefficient scales as n^2, not n^(5/3). It is a coherent rotating field state; it is not the old cold-stream waterbag and does not have independently conserved massive species numbers.

Keeping phase gradients, j_theta^mu=-2R^2 partial^mu theta in signature (-,+,+,+). On a timelike-gradient, zero-vorticity local fluid branch, mu=sqrt(-partial theta dot partial theta), n=2R^2 mu, epsilon+P=n mu. Neglecting radial gradients at long wavelengths, the phase-fluid sound speed is

    c_IR^2=(Uss-2Us)/(Uss+2Us).

Positive source Us>0 and radial stability D>0 are necessary; positive compressibility additionally requires Uss>2Us, which gives 0<c_IR^2<1. This thermodynamic result is not by itself a finite-wavelength dispersion or a bound on halo gradients. Vacuum-subtracted epsilon_ex=Us/2+U-Umin and P_ex=Us/2-(U-Umin) define w_ex on this branch. At a nondegenerate broken-symmetry radial minimum, n tends to zero and w_ex,c_IR^2 tend to 1. Model-native does not mean cold. For a strictly logarithmic U linear in s, c_IR^2=-1, so this simple charge state does not supply a stable dense logarithmic fluid.

The superfield R assignments are R(X)=R(B)=2, R(A)=0, hence R(T)=2 and q_R=2q_theta. The Weyl charges are +1 for X and B, -1 for A, +1 for the gaugino. With T(adj)=5, the SU(5)^2 U(1)_R anomaly coefficient is 5+5(-1)+5(+1)=5. Thus the continuous charge is a classical Noether current of this rigid action, not an exact quantum conserved abundance protected by the model. A lifetime or selected net charge has not been supplied.

## General angular metric required by matching

If the matched angular term is -F(s)(partial theta)^2, the fixed-charge energy is n^2/(4F)+U. Define a=(ln F)' and assume Us/a>0 and a nonzero. Then

    n^2=4F Us/a,
    D=Uss+(a-a'/a)Us,
    P=Us/a-U,
    dP/dln n=2Us[Uss-(a+a'/a)Us]/(aD),
    c_IR^2=[Uss-(a+a'/a)Us]/D.

Canonical F=R^2 has a=2,a'=0 and reduces to the preceding formulas. A running reference-field metric must be used consistently with the matched U; the pressure boundary is not automatically Uss=2Us. The radial canonical mass also needs the matched radial kinetic coefficient. Finite threshold derivative-action corrections, gauge/IR dynamics and state selection remain independent physical obligations.
