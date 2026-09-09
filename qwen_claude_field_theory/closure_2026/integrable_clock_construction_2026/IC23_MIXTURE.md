# IC23: simultaneous radiation/matter and the evolving coefficient gate

Base `12fd52243236cacda49b58224e6876e6ca5531ec`, 2026-09-09.
**Full theory OPEN.** The unchanged IC20 gravitational action is now varied
with BOTH matter sectors simultaneously. Separate IC21/IC22 eigenvalues are
not pooled. This yields explicit combined inequalities, a tested local
three-scalar branch, and the next coefficient-function construction equation.
Carl Zimmerman's exponential kernel, vacuum-scale relation and primordial
clock motivate the gravitational model. No new empirical fit, global novelty
claim, derived normalization coefficient, or completed theory is announced.

## 1. One summed action

The action is I20_grav+Sr+Sm, where I20_grav is fully defined in
IC20_JOINT_COMPLETION.md, with its selected coefficient functions unchanged.
Use two distinct, varied ordinary matter scalars with

    Sr=integral sqrt(-g) X_r²,
    Sm=integral sqrt(-g) exp(-4wc) P_w(exp(2wc) X_m),
    P_w(X)=w[sqrt(2X)/(1+w)]^((1+w)/w), w=10^-8,
    X_i=-g^{mu nu} partial_mu sigma_i partial_nu sigma_i/2>0.

Both couple to the same physical metric, with constant normalizations only.
These are noninteracting, irrotational perfect-fluid idealizations. They are
NOT a photon-baryon collision model or a measured baryonic equation of state.
Their individual matter Euler equations imply their individual covariant
Ward identities; no nonmetric force or artificial charge transfer is imposed.

On the pin their canonical Hamiltonian densities are

    h_i=exp(S)c_i j_i^(1+w_i),
    (w_r,c_r)=(1/3,3/4), (w_m,c_m)=(10^-8,1),
    j_i=P_i/V=(M_i/c_i)^(1/(1+w_i))exp(-3Q),
    u_i=partial h_i/partial j_i=(1+w_i)h_i/j_i,
    beta_i=partial²h_i/partial j_i²/2=w_i u_i/(2j_i)>0.

Here Q=ln(barred scale factor), V=exp(3Q); M_i are separately conserved
positive matter amplitudes. The radiation coefficient follows from its actual
Legendre transform, not from assigning its sound speed to a mixed mode.

## 2. Vary their common background and constraints

Let h be the raw IC20 gravity Hamiltonian before z elimination. Define
rhoH=sum h_i and pH=sum w_i h_i. Then

    h_S+rhoH=0, h_z=0,
    Qdot=h_q/2, qdot=-3(h-pH)/2,
    Aaux(0)=[[h_SS+rhoH,h_Sz],[h_Sz,h_zz]],
    source=(3Qdot(h_S+rhoH)+h_Sq qdot-3Qdot(rhoH+pH),
            3Qdot h_z+h_qz qdot)^T,
    Aaux(0)(Sdot,zdot)^T=-source.

The conserved total Hamiltonian is exp(3Q)(h+rhoH). The two amplitudes are
held fixed because each matter action has its own shift symmetry; the
relative radiation/matter densities nevertheless evolve differently.

At k!=0 replace h_SS+rhoH by h_SS+rhoH-2B k². At unit volume the actual
secondary-secondary bracket follows from

    fQ=(3h_S-3q h_Sq+4k²h_SR-3pH,
        3h_z-3q h_qz+4k²h_zR), fpi=(h_Sq,h_qz),
    D_ij=(fQ_i fpi_j-fpi_i fQ_j)/2,
    PB=[[0,-Aaux],[Aaux,D]].

The script computes this 4x4 matrix and its ranks at k²=0,1,10000 on each
sampled mixed background. It does not insert the vacuum or radiation-only
matrix. The unchanged pin pair remains regular here. The positive-pressure
matter Legendre maps introduce two genuine matter modes, not auxiliaries.
The local count therefore has two tensors, one explicit clock scalar and
two matter scalars. General nonlinear functional closure is still unproved.

## 3. Full three-field quadratic action

Let x=(zeta,delta sigma_r,delta sigma_m), p=(delta q,s_r,s_m),
where s_i=delta P_i/V. The canonical normalization is D=diag(2,1,1), so the
symplectic term is V p^T D xdot. The spatial momentum constraint gives

    |delta pi_TF/V|²=(delta q-(3/2)sum j_i delta sigma_i)²/6.

Use the z-eliminated gravity derivatives H_ab=h_ab-h_az h_bz/h_zz, and set
a=t/6+H_qq/2, d=H_qR, C=H_Sq, e=H_SR, E=exp(2S). For
H2/V=p^T Kp+2p^T Lx+x^T Wx, before eliminating the lapse,

    K0=diag(a,beta_r,beta_m),
    L0_00=2d k², L0_0i=-t j_i/4, L0_i0=-3w_i u_i/2,
    W0_00=-2v k²+8H_RR k^4+(9/2)sum w_i(1+w_i)h_i,
    W0_ij=3t j_i j_j/8+delta_ij E j_i k²/(2u_i), i,j>0.

All other entries vanish. The lapse source vectors and coefficient are

    f=(C,u_r,u_m)^T, g=(4e k²-3sum(1+w_i)h_i,0,0)^T,
    M=H_SS+rhoH-2B k²,
    K=K0-ff^T/(2M), L=L0-fg^T/(2M), W=W0-gg^T/(2M).

The matrix is coupled; no fluid or clock eigenvalue is predetermined.
Eliminate canonical momenta and define

    A=D K^(-1)D/2, Bm=-D K^(-1)L, Cm=2(W-L^T K^(-1)L).

The actual time-dependent equations are

    A xddot+[Adot+3Qdot A+Bm-Bm^T]xdot
       +[Bmdot+3Qdot Bm+Cm]x=0.

The three componentwise Euler identities are checked symbolically. Numerical
derivatives use the combined sourced flow, k²dot=-2Qdot k² and jdot_i=-3Qdot j_i.
The full six-root frequency problem is computed independently of the following
principal formula. Finite instantaneous slow roots are not cosmological growth
histories or signal velocities.

## 4. Combined positivity and light-cone conditions

The exact leading Schur terms are checked entry by entry. With rho_mix=d/a,
the resulting aligned principal matrix has star form

    Vprincipal=[[c_g²,f_r,f_m],[g_r,w_r,0],[g_m,0,w_m]],
    c_g²=[-2av+4a(e-Cd/(2a))²/B]/E
            -2a[dot rho_mix+Qdot rho_mix]/E,
    f_i=d t j_i/(2E), g_i=2 beta_i d t j_i/(aE),
    J_i=f_i g_i=beta_i d² t² j_i²/(a E²)>=0.

Its characteristic polynomial is derived as

    (lambda-c_g²)(lambda-w_r)(lambda-w_m)
       -J_r(lambda-w_m)-J_m(lambda-w_r).

The leading kinetic matrix diag(2/a,1/(2beta_r),1/(2beta_m)) symmetrizes
Vprincipal. For 0<w_i<1 and positive kinetic coefficients, completing squares
gives the necessary and sufficient strict bounds for all principal speeds
to lie between zero and the physical light cone:

    c_g² - sum J_i/w_i > 0,
    1-c_g² - sum J_i/(1-w_i) > 0.

For the symmetric normalization, write r_i²=J_i. Its gradient quadratic form
equals sum w_i(x_i+r_i x0/w_i)²+[c_g²-sum J_i/w_i]x0². The light-cone
complement has the analogous square completion with 1-w_i. Both are checked
exactly for this two-fluid system; the displayed finite-sum argument extends
to any finite set of regular positive-pressure aligned fluids of this form.
Exactly cold dust is excluded because this normalization is degenerate.

The mixture matters: each fluid uses part of both inequalities, so separate
two-field successes do not establish the summed result.

## 5. Computed local mixture and its actual evolution limit

Three backgrounds use (Mr,Mm)=(10^-8,10^-6),(10^-6,10^-6),(10^-5,10^-5).
All solve their combined constraints at q=-3,Q=0. For the middle case the
computed squared characteristic speeds are approximately

    (.33333454452, .20001101371, 9.9999818348e-9).

Both combined inequalities and the finite-k kinetic signs are positive at
these points. The full frequency system at k²=10^14 checks all three principal
values; no mode may be dropped from the comparison.

The same middle branch was then followed toward requested Q=.01 with actual
constraint and charge solves. Damped Newton steps use an analytic Jacobian,
reject chart exits, reduce step size on nonconvergence, and retain failed
attempts. This prevents a Newton overshoot from masquerading as a physical
branch endpoint. The continuation DOES NOT reach .01 while healthy.

The first detected light-cone crossing is numerically bracketed by

    .00372332590967417 < Q_cross < .00372332591116428.

At that crossing the lapse Schur value is about -.02125, still negative.
The scalar characteristic exceeds the light cone before the auxiliary matrix
loses rank. This falsifies a healthy extended-history claim for this specified
trajectory and coefficient choice, not every MOND or clock action. The last
coarser accepted endpoint is already beyond the bound and is deliberately
retained in the output; it is not called a healthy state. The bracket is a
high-precision numerical result, not a rigorous interval enclosure.

## 6. Next construction: integrate a coefficient function, not a new snapshot

The analytic auxiliary structure gives

    rho_mix=-4z/h_qz,
    e-Cd/(2a)=-v0+2z h_Sq/h_qz.

In particular the second expression cancels the explicit h_Sz dependence.
Define rho derivatives with respect to independent S,q,z, and use
zdot=-(h_Sz Sdot+h_qz qdot)/h_zz on the auxiliary shell. A chosen c_g² target
then solves the following actual equation for Sdot:

    Sdot=[E(c_frozen-c_target)/(2a)
            -(rho_q-rho_z h_qz/h_zz)qdot-Qdot rho]
           /(rho_S-rho_z h_Sz/h_zz),
    c_frozen=(-2av+4a(e-Cd/(2a))²/B)/E.

Both identities are checked symbolically, and the original multiplier and
D'' coefficient are reconstructed from the initial action data. These are
local coefficient-design equations, NOT a license to prescribe the lapse.
Targeting the original c_g² at the later endpoint would make its lapse Schur
positive, introducing a spatial auxiliary pole. That diagnostic is retained.

A safer next design parameter is a strictly negative desired lapse Schur
M_*. Write h_SS^(0) for the raw partial derivative with D'' set to zero.
Since the action contains -D(S)z²,

    D''=[h_SS^(0)+rhoH-h_Sz²/h_zz-M_*]/z².

`lapse_potential_control` inserts this D'' jet, varies the resulting local
Hamiltonian, solves preservation, and recomputes the clock diagonal. It does
not assign the multiplier. This is checked at the evolved endpoint as a
construction diagnostic. It is NOT a globally defined replacement D(S).

The next implementation must integrate this prescription into ONE single-
valued D(S), maintaining D_Q=D' S_Q and D'_Q=D'' S_Q while evolving the
same mixed matter background. Monitor monotonicity of S, coefficient
regularity, the combined cone inequalities, finite-wavelength stability and
interaction scales. When varying that new action, hold D as a function of S
only; recomputing it from q,z or matter during variation would change the
theory and fake the desired constraints. A smoothly defined extension to
the static domain is also required. No integrated replacement is claimed here.

## 7. Remaining full-theory obligations

Relative flow, plasma interactions, general nonlinear constraints, long
cosmology, static/zero-field matching, Phi/Psi, measured G, all PPN coefficients,
instantaneous physical channels, interaction scales and empirical galaxy,
cluster and CMB fits remain unverified. The combined local result does not
erase these requirements. Strict execution exits2 after its scoped checks;
the full objective remains OPEN. See `ic23_run_001/run_index.json` for exact
commands, test statuses and files. Mathbox computation audit and mathematical
self-review were used, not independent peer review or Lean certification.
