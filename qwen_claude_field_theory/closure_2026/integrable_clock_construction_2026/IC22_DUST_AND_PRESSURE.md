# IC22: constrained dust and a positive-pressure matter completion

Base `47fe051f7ffcdda06774a3b0aaf76b98b1ea14f0`, 2026-09-09.
**Full theory OPEN.** The IC20 gravitational coefficient functions are
unchanged. This calculation derives pressureless matter independently and
then constructs an explicit positive-pressure matter branch. It does not
borrow radiation's eigenvalues or call an ideal dust defect a no-go for
gravity. Carl Zimmerman's primordial-clock direction and vacuum-normalized
exponential framework motivate the gravitational action. The scale relation
remains imposed, not derived; there is no new empirical or novelty claim.

## 1. Vary pressureless matter including its multiplier

Use the single physical metric g and

    Sdust=-1/2 integral sqrt(-g) rho [g^{mu nu} tau_mu tau_nu+1].

Varying rho gives the unit-timelike constraint. Varying tau gives
nabla_mu(rho nabla^mu tau)=0. The normalized velocity is geodesic, and the
ordinary dust stress obeys its own covariant conservation equation. No
nonmetric baryonic force is inserted. On the pin use constant redefinitions
tau_bar=exp(-wc)tau, rho_bar=exp(4wc)rho, so the barred action has the same
form. Below tau,rho denote these barred variables and N=exp(S).

For barred volume V the exact matter Lagrangian and Hamiltonian are

    Ld=V rho taudot²/(2N)-NV rho(1+|Dtau|²)/2,
    P_tau=V rho taudot/N, p_rho=0,
    Hd=N[P_tau²/(2V rho)+V rho(1+|Dtau|²)/2].

Preservation of p_rho gives

    C_rho=-P_tau²/(2V rho²)+V(1+|Dtau|²)/2=0,
    {p_rho,C_rho}=-P_tau²/(V rho³).

On positive density/current this is nonzero and fixes the next multiplier;
rho is not a hidden propagating field. Solve it on the positive-current
branch to obtain Hd=N P_tau sqrt(1+|Dtau|²). At homogeneity,

    j=P_tau/V>0, Hd/V=N j, jdot=-3Qdot j.

The canonical density momentum is linear, unlike radiation. This is why
substituting zero sound speed in IC21's nondegenerate reduction is invalid.

## 2. Same-action background and complete local auxiliary block

Solve h_S+Nj=0 and h_z=0 using IC20's h, with its original coefficient
functions. The homogeneous equations are Qdot=h_q/2 and qdot=-3h/2.
Preservation includes the dust source -3Qdot Nj in the S secondary.

Before eliminating rho, the primary set (p_S,p_z,p_rho) has three
secondaries. On homogeneous, on-shell rho=j, their primary-secondary block
at unit barred volume is given below. For this matrix the density secondary
is the unrescaled delta H/delta rho=N C_rho; section1 divided it by N.

    Aaux=[[h_SS+Nj-2B k²,h_Sz,0],
          [h_Sz,h_zz,0], [0,0,N/j]].

The canonical Q derivatives of those secondaries, at fixed pi,P_tau,rho, are

    fQ=(3h_S-3q h_Sq+4k²h_SR,
        3h_z-3q h_qz+4k²h_zR, 3N),
    fpi=(h_Sq,h_qz,0).

Thus D_ij=(fQ_i fpi_j-fpi_i fQ_j)/2, and the full PB is [[0,-Aaux],[Aaux,D]].
The script constructs this 6x6 matrix, computes its determinant and SVD rank
at k²=0,1,10000 for each sampled dust background. There is no assigned rank.
Together with the regular IC20 pin sector, invertibility fixes auxiliary
multipliers locally. General nonlinear spatial functional closure is not
proved by these mode matrices. The matter scalar tau contributes ONE
physical matter mode; rho does not. The gravitational clock remains explicitly
counted separately from the two tensors.

## 3. Cold quadratic equations retain frequency-dependent mixing

Fields x=(zeta,delta tau), momenta p=(delta q,s), s=delta P_tau/V,
have symplectic term V p^T D xdot with D=diag(2,1). Define

    a=t/6+H_qq/2, d=H_qR, C=H_Sq, e=H_SR,
    u=N, Z=4e k²-3Nj, M=H_SS+Nj-2B k²,
    f=(C,u)^T, g=(Z,0)^T.

Using the sourced spatial momentum constraint, the varied quadratic
Hamiltonian H2/V=p^T Kp+2p^T Lx+x^T Wx has

    K=diag(a,0)-ff^T/(2M),
    L=[[2d k²,-t j/4],[0,0]]-fg^T/(2M),
    W=diag(-2v k²+8H_RR k^4,3t j²/8+u j k²/2)-gg^T/(2M).

Its inverse is derived explicitly:

    K^(-1)=[[1/a,-C/(au)],[-C/(au),-2M/u²+C²/(au²)]],
    det K=-a u²/(2M)>0 when a>0,M<0.

The fluid normalization equation follows directly:
delta taudot=u n, n=-(C delta q+Z zeta+u s)/M. The other matter Hamilton
equation gives the density-current identity

    sdot+3Qdot s=j[t delta q/2-(3t j/4+u k²)delta tau].

In particular at j=0 the perturbative dust charge V s is conserved; this
is a useful limiting algebraic check, not a positive-density vacuum chart.
Both identities are checked symbolically.

Set A=D K^(-1)D/2, Bm=-D K^(-1)L, Cm=2(W-L^T K^(-1)L). The full equation is

    A xddot+[Adot+3Qdot A+Bm-Bm^T]xdot
       +[Bmdot+3Qdot Bm+Cm]x=0.

All derivatives follow the dust-sourced background and k²dot=-2Qdot k².
The script computes four instantaneous growth exponents from this full
quadratic frequency problem, including the term linear in frequency. It
does not diagonalize a static restoring matrix and declare its values speeds.
Slow instantaneous roots depend on the time-dependent field representation;
they are NOT integrated cosmological growth rates.

## 4. What the exact cold principal polynomial really establishes

Use delta tau=y_d/k to balance its O(k²) kinetic coefficient. Define

    rho_mix=d/a, E=N², Zbar=e-Cd/(2a),
    A1=2/a, A2=2B/u², F=4Zbar/u,
    G=-4[v+dot rho_mix+Qdot rho_mix].

For omega/k in coordinate time, the principal symbol is

    [[G-A1 omega²,-i omega F],[i omega F,-A2 omega²]],
    determinant=omega²[A1 A2 omega²-A2 G-F²].

The nonzero physical squared characteristic speed is therefore
(A2 G+F²)/(A1 A2 E). It is approximately .20000606572 at Md=10^-6.
Discarding the gyroscopic term F instead gives approximately -.45782968824.
The coupling is essential; its stabilizing contribution must be derived.

However the zero root is defective in the balanced first-order principal
reduction. Its generator is

    J0=[[0,0,1,0],[0,0,0,1],[-G/A1,0,0,-F/A1],[0,0,F/A2,0]].

For nonzero G, e=(0,1,0,0)^T and g=(-F/G,0,0,1)^T satisfy J0 e=0,
J0 g=e. This exact Jordan chain is checked symbolically. The numerical
eigenspace dimension and algebraic multiplicity are computed separately.
The sampled zero root has multiplicity2 but eigenspace dimension1.
Thus real fast characteristics do not establish strong hyperbolicity in
this reduction. Nonlinear pressureless caustics and possible derivative-loss
formulations remain unresolved; this is not a framework-wide gravity no-go.

## 5. Construct an explicit positive-pressure completion

For 0<w<=1, define a distinct ordinary matter action, keeping gravity fixed:

    P_w(X)=w [sqrt(2X)/(1+w)]^((1+w)/w),
    Sm_w=integral sqrt(-g) exp(-4wc) P_w(exp(2wc) X_sigma).

The constant normalization ensures that on the pin the barred matter
Hamiltonian is Hm/V=N j^(1+w). It is a choice of matter units, not another
metric coupling. In the tested units the overall Hamiltonian coefficient is
one. The Legendre relations are v_sigma=(1+w)j^w and L/V=N w j^(1+w).
Consequently p/rho=w and the standalone sound speed squared is w. This
is a specified barotropic idealization, NOT an empirical baryonic equation
of state or proof of a healthy ultraviolet completion at arbitrarily small w.

The general quadratic calculation replaces

    h_m=N j^(1+w), u=N(1+w)j^w, beta=w u/(2j)>0,
    K0=diag(a,beta), L0_s,zeta=-3w u/2,
    Z=4e k²-3(1+w)h_m,
    W0_zeta,zeta=-2v k²+8H_RR k^4+(9/2)w(1+w)h_m,
    W0_sigma,sigma=3t j²/8+E j k²/(2u).

Use the same lapse Schur subtraction and full time-dependent Euler equation.
The background is varied anew: qdot=-3h/2+3w h_m/2, with the source
-3(1+w)Qdot h_m in preservation. It is not evolved as a radiation/dust
mixture. The nondegenerate principal matrix has the IC21 derived form with
matter diagonal 2 beta j/u=w; its two eigenvalues are computed, not assigned.

At amplitude10^-6, pressure parameters w=.001,10^-6,10^-8 give positive
kinetic coefficients and two real subluminal characteristics. For w=10^-8
the squared speeds are approximately (.200006065724,9.9999818343e-9).
The full frequency calculation at k²=10^14 independently checks the principal
values. This supplies a constructive regular matter candidate rather than
declaring cold dust healthy. The dust zero-mode result and finite-pressure
health are results of DIFFERENT explicit matter actions and are not pooled.

## 6. Scope and next calculation

Five exact-dust backgrounds (Md=10^-12,10^-8,10^-6,10^-5,10^-4) and three
positive-pressure backgrounds are tested. Finite-k cold roots include growth;
neither finite instantaneous growth nor a real UV root is by itself a verdict
on the actual evolving density contrast. No full cold-sector stability pass
is claimed. The ideal dust's defective principal sector is retained as an
explicit unresolved limit, not hidden behind the positive-pressure result.

Next vary radiation AND positive-pressure baryons simultaneously, producing
the coupled three-scalar clock/matter principal system. Separate two-field
passes do not certify their mixture. Then test relative flows and extend a
healthy cosmological trajectory before sourcing a galactic metric. PPN,
measured G, lensing, zero-field/static matching, instantaneous channels,
interaction scales, empirical clusters and CMB remain unverified.

Mathbox computation audit and mathematical self-review were used; there is
no independent peer review or Lean certificate. The strict script exits2 to
refuse full closure. Exact commands, statuses and changed files are recorded
in `ic22_run_001/run_index.json`.
