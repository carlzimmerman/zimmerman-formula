# Gravitational constraints, physical sources and normalization

2026-10-20. Base f1565bc90; contract: FROZEN_CRITERIA.md.
**The original healthy microscopic xi=1/4 goal remains open.**
The exact algebra below does not supply quantum health or amplitude selection.
Standing kappa=1/2 remains fitted; the separate CFG493 rho_DE and rho_crit
results are not action inputs. No measured acceleration or PPN value is used.
We use c=hbar=1, signature -+++, and distinguish source mass m from clock M.
Set A=(phi+i chi)/sqrt(2), g,tau,F0>0 and s0=F0^2; f_B0=f_B(0) is a BM curvature.
Primary versions and the distinction between source results and new
calculations are recorded in SOURCES.md.

## 1. Specified covariant rational model and a consistent background

Add to ../clock_flux/RESULT.md the explicit bosonic action

    S=int sqrt(-g)[M_Pl^2 R/2-M nabla_mu u_nu nabla^mu u^nu/2
                   +lambda(u^2+1)+L_rational]+S_m, M>0,
    L_rational=-gX+g|F|^2+2w ReF+Lambda(Y-2X|F|^2+|F|^4),
    X=partial A.dot.partial A*, Y=(partial A)^2(partial A*)^2,
    J=(g^{mu nu}+u^mu u^nu)partial_mu A partial_nu A*,
    Lambda=-tau s0/(s0-X+5J), s0=g/(6tau), w=-2g F0/3.

This c1-only covariant representative is an added model choice, not a derived
nonlinear supergravity completion. The unit constraint is solved regularly.
The denominator is s0+|u.dot.partial A|^2+4J>0 on its timelike clock patch.
Use Bianchi I, rather than an off-shell flat space with nonzero stress:

    ds^2=-dt^2+a_perp^2(dx^2+dy^2)+a_parallel^2 dz^2,
    phi=pz, chi=0, u=partial_t, h=p/a_parallel, F=f(h).

The scalar current is homogeneous spatial with zero temporal component, so
its divergence vanishes. Spatial aether equations vanish by reflection and
homogeneity; its temporal equation fixes the multiplier. The scalar stress is

    rho=E(h), p_perp=-E(h), p_parallel=-E(h)+h^2 E_X.

With H_i=adot_i/a_i, lapse variation of the homogeneous action gives exactly

    M_Pl^2(H_perp^2+2H_perp H_parallel)
      +(M/2)(2H_perp^2+H_parallel^2)=E(h).

Writing a_perp=exp(alpha+beta), a_parallel=exp(alpha-2beta), the kinetic
terms are -3(M_Pl^2+M/2)alphadot^2+3(M_Pl^2-M)betadot^2.
For M<M_Pl^2 this homogeneous reduction is nondegenerate. Initial zero
shear gives H_bg^2=E/[3(M_Pl^2+M/2)]; anisotropic stress subsequently drives
shear and Hdot_i at order E/M_Pl^2. Smooth local background evolution is
the relevant domain, not a global cosmological or sourced-halo theorem.
At a fixed regular finite-gradient point, curvature is O(E/M_Pl^2), and
hdot/h and fractional coefficient drift are O(sqrt(E)/M_Pl).

## 2. Exact nonzero-wave-number local instability and continuation scope

Use a local orthonormal frame, phi=Hz, and a wave parallel to H. Set

    a=E_X>0, j=L_J>0, K=a+j, b=E_X+2X E_XX>0.
    L2=K varphidot^2/2-b(varphi_z)^2/2-jHv varphidot
       +M vdot^2/2-M(v_z)^2/2+jH^2v^2/2.

F is already eliminated on its regular finite-h branch. Its response enters
b; chi decouples from this real mode. The declared clock is a real vector.
For w_mode=omega^2 the frozen fixed-metric polynomial is

    (K w_mode-b k^2)[M(w_mode-k^2)+jH^2]-j^2 H^2 w_mode=0.

Its constant term bM k^2(k^2-m_b^2) is negative throughout
0<k^2<m_b^2, where m_b^2=jH^2/M. Thus it has one negative real root.
At x=X/s0=11/112, y=F/F0=3/4, exact branch arithmetic gives

    E/V0=283/252, a/g=22/27, j/g=5/54, K/g=49/54,
    m_b^2=(55/1698)E/M, m_t^2=(a/K)m_b^2=(1210/41601)E/M.

For s=w_mode/m_b^2, kappa=k^2/m_b^2, theta=a/K and beta=b/K>0,
the polynomial is s^2+[theta-(1+beta)kappa]s+beta kappa(kappa-1).
At kappa=1/4 and s=-theta/4 its value is
[theta(1-3theta)+beta(theta-3)]/16<0, since theta=44/49.
Therefore k=m_b/2 has a simple negative root below -m_t^2/4.
Its growth gamma exceeds m_t/2; this is not a k=0 inference.

A conditional weak-gravity continuation takes M_Pl to infinity with
M,g,tau,h fixed at this finite branch point. Let epsilon_g=M/M_Pl^2.
Then k and gamma stay finite, while background drift/m_b is O(sqrt(epsilon_g)).
In generalized harmonic gauge, the metric block at omega=i gamma and real
nonzero k has leading inverse O[1/(k^2+gamma^2)]. Canonical variables
h_c=M_Pl delta_g and v_c=sqrt(M)v give off-diagonal metric mixing of order
sqrt(epsilon_g), in units m_b^2; E/(M_Pl^2 m_b^2)=(1698/55)epsilon_g.
Under a regular finite-k constraint/gauge reduction, the metric Schur
correction is O(epsilon_g), and the separated negative root persists.
The Ward identity supplies harmonic-constraint propagation; using it here
requires the full covariant linear equations and constraint-compatible data.
Every metric mixing coefficient and a numerical finite-coupling threshold
have NOT been computed. This is conditional continuity, not a finished ADM
reduction or an unconditional full-gravity instability theorem.

A wavepacket over Delta_t=epsilon_g^(-1/4)/m_b has O(epsilon_g^(1/4))
background drift but parametrically many growth times. It is relevant only if

    L_bg^(-1) << k,gamma << Lambda_valid.

M_Pl>>sqrt(M)>>E^(1/4) allows such a window below the nominal clock scale,
conditional on validity of the rational scalar action on this background.
The actual microscopic cutoff/strong-coupling scale is unproved. Finite
coupling, unspecified curvature operators, nonlinear SUGRA and varying halo
solutions remain distinct obligations. Auxiliary-Hessian signs alone prove
none of these physical conclusions.

## 3. Actual universal matter coupling and the n-dimensional scalar law

Specify S_m[tilde_g,psi], tilde_g=exp(2q phi)g, phi_background=0, so A0=1.
Point particles have action -sum m int exp(q phi)ds_g. Hence
delta S_m/delta phi=sqrt(-g)qT and nabla_mu T^{mu nu}=qT nabla^nu phi;
weak dust has T=-rho. Source and test-body couplings follow from one action.
No disformal or direct matter-aether coupling is included.
Choose q>0 by scalar orientation and m>0; q=0 has no scalar MOND force.

For a static scalar in n>=2 space dimensions, with Omega_(n-1) the unit
sphere area, the selected branch and spherical source obey

    div[(E_h/h)grad phi]=q rho,
    Omega_(n-1) r^(n-1) E_h=q m.
    E~C2 h^2 (UV), E-V0~C3 h^3 (IR),
    Gs_n=q^2/(2 Omega_(n-1) C2), a_s=2q C2/(3C3),
    g_s,UV=Gs_n m/r^(n-1),
    g_s,IR=sqrt(Gs_n m a_s)/r^((n-1)/2).

Only n=3 gives the 1/r exterior MOND acceleration. The four-dimensional
chiral construction is not a derivation by dimension counting. Here
C2=25g/48, C3=10sqrt(5g tau)/9, V0=g^2/(12tau), from the actual static
UV/IR limits, not a surviving quadratic infrared Taylor coefficient.

## 4. Tensor/scalar forces, two physical potentials and density footing

Let B_T=M_Pl^2-M/2, B_cos=M_Pl^2+M/2. In the aligned local UV rest frame,
N=1+n and gamma_ij=exp(2psi)delta_ij give the leading static action

    M_Pl^2[(grad psi)^2-2n Delta psi]+M(grad n)^2/2
       -C2(grad phi)^2-rho(n+q phi).

Variation yields psi=-n, (2M_Pl^2-M)Delta n=rho, 2C2 Delta phi=q rho.
Scalar field energy is higher weak-potential order here; vacuum curvature
is negligible over this local patch. Therefore

    Gt=1/(8pi B_T), Gcos=1/(8pi B_cos), Gs=q^2/(8pi C2),
    Guv=Gt+Gs, f=Gs/Guv=q^2 B_T/(C2+q^2 B_T).

Positive Gt alone needs M<2M_Pl^2. The c1-only tensor kinetic/speed further
has c1=M/M_Pl^2 and c_tensor^2=1/(1-c1); real nondegenerate tensor speed
requires c1<1. Set r=M/(2M_Pl^2), so the used domain is 0<r<1/2.
For U_T=Gt m/radius and U_s=Gs m/radius=-q delta_phi,

    g00=-1+2U_T, gij=(1+2U_T)delta_ij,
    tilde_g00=-1+2(U_T+U_s),
    tilde_gij=[1+2(U_T-U_s)]delta_ij,
    gamma_UV=(Gt-Gs)/(Gt+Gs)=1-2f.

This is the unscreened weak-field UV two-potential coefficient. It is not a
global PPN expansion around the MOND infrared vacuum. Moving-source preferred
frame parameters, compact-body sensitivities, screening and disformal matter
require new calculations. The scalar's known clock instability is not cured
by writing this conditional static observable.

In n=3, matching the IR acceleration to sqrt(Guv m a_IR)/radius gives

    a_IR=f a_s,
    xi_V0=a_IR^2/(Guv V0)=f^3(125pi/128)
          =125pi(1-gamma_UV)^3/1024.

The cube is essential: the old scalar-only dictionary is not the observed
tensor-plus-scalar normalization. q remains independent. Counterfactually
xi_V0=1/4 would imply gamma_UV=1-[256/(125pi)]^(1/3), a second observable
without any measured gamma input. This condition does not select q.

For the constant-phi vacuum, the declared bosonic covariant action gives
3 B_cos H0^2=V0. The inferred density defined using Guv instead satisfies

    epsilon_inf=3H0^2/(8pi Guv)=(Gcos/Guv)V0,
    xi_inf=xi_V0(Guv/Gcos)
          =(125pi/128) f^3 (1+r)/[(1-r)(1-f)].

This factor is Guv/Gcos, not its inverse. If f<=1/4 and r<1/2, then
f^3/(1-f)<=1/48 and (1+r)/(1-r)<3. Using only pi<4 gives
xi_inf<125pi/2048<125/512<1/4. Thus a downstream target xi_inf=1/4
requires f>1/4 and gamma_UV<1/2. It leaves an r-dependent curve, not the
same unique gamma as the actual-V0 footing. No observed gamma enters this
bound. It is a counterfactual discriminator of a presently unhealthy model.
As a downstream comparison only, Bertotti, Iess and Tortora's Cassini
measurement reports gamma=1+(2.1+/-2.3)10^(-5) ([original abstract](https://pubmed.ncbi.nlm.nih.gov/14508481/)).
The conditional gamma_UV<1/2 prediction disagrees with that reported result
if this local unscreened UV coupling applies in the Solar System. No
significance conversion or measured value selected any coefficient above.
With c restored, V is energy density, rho_mass=V/c^2 and
xi=a_IR^2/(Guv V)=a_IR^2/(Guv rho_mass c^2);
epsilon_inf=3c^2 H0^2/(8pi Guv). A rolling conformal factor needs a new
cosmological conversion; the displayed relation assumes phidot=0 and A0=1.

## 5. Pure Blanchet-Marsat de Sitter: actual lapse and shift reduction

This is a separate metric/khronon theory, not the independent vector tilt.
Use M_B^2=1/(8pi G) and

    S_B=(M_B^2/2)int N sqrt(gamma)[R3+KijKij-K^2-2f_B(a)],
    a_i=D_i lnN, f_B(a)=f_B0-a^2+2a^3/(3a0)+O(a^4).

Its true homogeneous vacuum has H^2=f_B0/3>0. Write
N=1+n, gamma_ij=a_dS^2 exp(2zeta)delta_ij, N_i=partial_i chi,
W=a_dS^3, X_k=k^2/a_dS^2, B=a_dS^(-2)Delta chi, U=zetadot-Hn.
For finite nonzero k, the raw quadratic bracket is

    -6U^2+4UB+X_k(2zeta^2+4n zeta+eta n^2)+2mu^2 n^2,
    eta=2 for BM; mu=0 for pure BM.

Shift variation gives U=0, hence n=zetadot/H. The lapse equation is
12HU-4HB+4X_k zeta+2(eta X_k+2mu^2)n=0; it fixes
B=X_k zeta/H+(eta X_k+2mu^2)zetadot/(2H^2), not another zeta constraint.
The required temporal boundary is exact because Wdot=3HW, X_kdot=-2HX_k:

    d[2 W X_k zeta^2/H]/dt=2W X_k zeta^2+4W X_k zeta zetadot/H.

After this boundary subtraction,
S2_red=(M_B^2/2)int W(eta X_k+2mu^2)zetadot^2/H^2.
For pure BM, finite nonzero k and H>0, kinetic energy is positive but there is no
restoring term: zeta=C1+C2 exp(-Ht). This retained scalar is not removed
as gauge. k=0, H->0, interactions and strong coupling are separate limits.
An optional KT K(Q)=mu^2(Q-1)^2, Q=1/N, adds the displayed 2mu^2 n^2
at its exact Q=1 condensate; it contributes no vacuum energy there.
That statement does not cover other cosmological clock states.
The older flat lambda>1 ADM calculation is prior work, not a new result;
division by lambda-1 is inapplicable to this pure-BM corner.

## 6. BM static normalization and a deformation invisible to this test

The stationary physical metric potential has source -rho Phi and
C2_B=1/(8pi G), C3_B=1/(12pi G a0), epsilon_B=f_B0/(8pi G).
Thus R_B=4f_B0/(9a0^2); recovering GR in the UV does not select it.
The allowed specified deformation

    f_delta(a)=f_B(a)+[2delta/(3a0)]a^3 exp(-a/L), L>0,

preserves f_B0, f_B''(0), the high-acceleration constant, homogeneous vacuum
and its quadratic constraints. It changes C3_B to (1+delta)C3_B,
a0_oper to a0/(1+delta), and R_B to (1+delta)^2 R_B near delta=0.
This is a nonselection test, not full health for every deformation.
Flanagan's stationary stability result assumes a stable conventional MOND
background and its stated low-acceleration, symmetry and sign/density
hypotheses. It does not give all-background stability or normalization.

## 7. Formal and remaining physical scope

GravitySelection.lean records fourteen conditional ordered-field statements:
lapse/shift and redshift identities, kinetic signs, static ratios, the
tensor/scalar cube, the inferred-target fraction/PPN bounds and three band
polynomial identities/signs. ADM/component variations, integration by parts,
actual pi, source calibration, stress and constraint continuation remain
analytic inputs. The final_gravity03 manifest records PASS in 4.447s with
fourteen standard-axiom prints; true controls pass and three false mutants
fail at False. This separate run evidence does not certify the physical bridge.
No scalar/clock quantum completion, independent selecting equation, universal
normalization or complete physical-to-Lean chain has been obtained.
