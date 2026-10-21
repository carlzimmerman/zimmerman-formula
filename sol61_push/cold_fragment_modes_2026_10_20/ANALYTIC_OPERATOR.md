# Full five-real-field fragment operator and constrained stability test

20 October 2026. Independent analytic continuation of the explicitly changed common matter action. Task base: `e63b8b234`. Exact reviewed source bytes are pinned in `sources_operator.json`. No profile, sparse spectrum, scattering solve or PDE was run by this reviewer.

**Conclusion.** The full linearized problem is a self-adjoint spatial Hessian coupled to a skew gyroscopic matrix. A negative unconstrained radial amplitude eigenvalue is expected and does not establish an instability. A direct fixed-charge quadratic-energy test supplies a sufficient stability criterion without identifying a bulk compressibility test with fragment stability. Phase positivity and, under extra monotonicity hypotheses, nonradial amplitude positivity have exact ground-state-transform proofs.

## 1. Normalization and background

Use the matter potential

    V=m^2|Psi|^2+MX^2|X|^2+g(X*Psi^2+X Psi*^2)
          +lambda|Psi|^4+a chi|Psi|^2+U(chi),
    U(chi)=M^2 chi^2/2-M chi^3/8+chi^4/4.

The performed branch has m=1, MX^2=4.0016, g=.002168>0, lambda=1.99+g^2/MX^2, a=200>0 and M=100. Nothing below transfers to the original positive-square carrier without this additional neutral interaction.

Let an exact isolated radial stationary background satisfy

    Psi_0=e^(i omega t) f(r), X_0=e^(2i omega t)b(r), chi_0=h(r),
    f''+2f'/r=(m^2-omega^2+2lambda f^2+a h+2g b)f,
    b''+2b'/r=(MX^2-4omega^2)b+g f^2,
    h''+2h'/r=U'(h)+a f^2.

All profiles are real and decay at infinity. The mathematical statements below are conditional on such an exact smooth finite-energy background. A numerical profile approximates these hypotheses; a finite list of positive sampled values does not itself prove them throughout the continuum.

Choose **canonical** real perturbations:

    Psi=e^(i omega t)[f+(u+i v)/sqrt(2)],
    X=e^(2i omega t)[b+(s+i t_X)/sqrt(2)],
    chi=h+z.

Each real perturbation then has kinetic energy one half its squared time derivative. These sqrt(2) factors must also be used in the neutral cross coupling, charge constraint and translation zero vector.

## 2. Complete spatial operators and gyroscopic dynamics

For a scalar harmonic of angular momentum ell, put

    L_ell=-d^2/dr^2-(2/r)d/dr+ell(ell+1)/r^2,
    D=MX^2-4omega^2,
    Vu=m^2-omega^2+6lambda f^2+a h+2g b,
    Vv=m^2-omega^2+2lambda f^2+a h-2g b,
    Vh=U''(h)=M^2-3M h/4+3h^2.

Order the amplitude and phase vectors as A=(u,s,z), P=(v,t_X). Their real spatial Hessians are

    Hplus_ell = [ L_ell+Vu    2g f          sqrt(2)a f ]
                [ 2g f        L_ell+D       0         ]
                [ sqrt(2)a f  0            L_ell+Vh  ],

    Hminus_ell = [ L_ell+Vv    2g f       ]
                 [ 2g f        L_ell+D  ].

The equations, including all five real fields, are

    A_tt-C P_t+Hplus_ell A=0,
    P_tt+C^T A_t+Hminus_ell P=0,
    C=[2omega 0; 0 4omega; 0 0].

Equivalently Z=(A,P) obeys Z_tt+G Z_t+H Z=0, with

    G=[0 -C; C^T 0], G^T=-G,
    H=diag(Hplus_ell,Hminus_ell).

All off-diagonal factors follow directly from the Hessian of V-omega^2(|Psi|^2+4|X|^2), not from the homogeneous two-by-two Hessian alone. A growth mode exp(s_g t) satisfies the **quadratic pencil**

    [s_g^2 I+s_g G+H] Z=0.

Eigenvalues of H alone are not dynamical growth rates. With real self-adjoint closed-boundary operators, the pencil has conjugation and Hamiltonian sign symmetries, with the usual qualifications at zero/continuous spectrum. Outgoing radiation boundary conditions instead define a different open/scattering or resonance problem; they must not be silently treated as a self-adjoint Hessian eigenproblem.

Use the radial inner product 4pi integral r^2 x^T y dr, with a consistent harmonic normalization. The transform w=r Z gives ordinary radial L2 operators -d^2/dr^2+ell(ell+1)/r^2+matrix potentials. Regular perturbations have w=O(r^(ell+1)) at the origin. Isolated bound modes decay at infinity. Dirichlet truncation at L is an approximation whose L and mesh convergence must be checked.

At infinity, the charged Hessian entries approach m^2-omega^2 and MX^2-4omega^2, but the gyro terms remain. Vacuum dispersions factor as

    k^2+m^2-(omega +/- Omega)^2=0,
    k^2+MX^2-(2omega +/- Omega)^2=0,
    k^2+M^2-Omega^2=0.

Therefore static Hessian thresholds are not the rotating-frame scattering thresholds. Coupled channels and their energy/charge signs must be retained.

## 3. Exact U(1) and translation zero modes

Define F=sqrt(2)f and B=sqrt(2)b. The global U(1) zero vector lies in the phase block:

    p_P=(F,2B), Hminus_0 p_P=0,
    p=(0,p_P) in amplitude/phase ordering.

The source phase is twice the daughter phase. Using (f,b) instead of (f,2b) would miss the symmetry. In full space translations give

    A_j=(partial_j F,partial_j B,partial_j h), P=0,
    Hplus A_j=0.

Their radial representative is (F',B',h') in ell=1, with three spatial harmonics. A finite Dirichlet box preserves U(1), but generally breaks exact translations: profile derivatives need not vanish at its outer boundary. A near-zero ell=1 eigenvalue must converge with L/mesh, not be forced to zero numerically.

There are symmetry-related generalized zero modes. Differentiating a smooth stationary family with respect to omega yields

    Hplus_0 d_omega(F,B,h)=a_Q,
    a_Q=(2omega F,8omega B,0)=C p_P.

Thus A=d_omega(F,B,h), P=t p_P is a secular family/phase solution of the linearized equations. It carries delta Q=dQ/domega, and is not automatically an allowed fixed-Q perturbation. Translation/boost Jordan partners similarly express centre motion rather than a growing internal instability. Zero eigenvalues and symmetry drifts must be separated from exponentially growing physical modes.

## 4. Direct fixed-charge quadratic energy

In the rotating frame, the exact positive-charge convention is

    Q=integral [2 Im(Psi*Psi_t)+4 Im(X*X_t)] d^3x.

Its linear variation and the conserved second variation of E-omega Q are

    delta Q=<p_P,P_t>+<a_Q,A>,
    E2=(||A_t||^2+||P_t||^2)/2
          +<A,Hplus A>/2+<P,Hminus P>/2.

The gyro matrix does no work: dE2/dt=0 because Z_t^T G Z_t=0. Likewise delta Q is conserved because Hp=0 and a_Q=-G p in full ordering. The neutral field has no entry in p or a_Q, but does couple dynamically through Hplus.

For fixed A,P subject to delta Q=0, the least kinetic energy is obtained by

    A_t=0,
    P_t=-p_P<a_Q,A>/||p_P||^2,

up to arbitrary additional velocity perpendicular to the constraint. Hence the radial constrained amplitude Hessian is

    HfixedQ_0=Hplus_0+(a_Q outer a_Q)/||p_P||^2.

This is a global rank-one correction, not a pointwise addition. Here ||p_P||^2=2 integral(f^2+4b^2)d^3x. For w=r Z on a uniform radial grid, consistent constant angular/quadrature weights cancel: the matrix addition is outer(a_w,a_w)/sum(p_w^2). Nonuniform meshes require their mass/quadrature matrix.

**Sufficient radial stability test:** Hminus_0 is nonnegative with only the U(1) kernel, and HfixedQ_0 is strictly positive/coercive on the nonsymmetry amplitude sector, with appropriate isolated boundary conditions. Then the conserved quadratic energy on delta Q=0 excludes exponentially growing finite-energy radial modes. This is a linear constrained-energy result. Nonlinear orbital stability requires further well-posedness/coercivity and higher-order control; a finite discrete eigenvalue calculation is not that proof.

Conversely, a negative eigenvalue of HfixedQ is a failed energy-positivity test, not automatically a proved growing mode of the gyroscopic pencil. An actual dynamical claim must examine the pencil or establish the requisite index theorem/hypotheses. At zero constrained eigenvalues the test is inconclusive and generalized modes require attention.

Only ell=0 enters the global linear charge constraint: higher harmonics have zero angular average. Applying this rank-one correction independently to every ell would be incorrect.

### Why an unconstrained negative radial direction is expected

For any nontrivial exact localized stationary configuration in three spatial dimensions, write F_omega=T_grad+U_omega. Scaling every spatial profile as a(r/lambda) gives

    F_omega(lambda)=lambda T_grad+lambda^3 U_omega,
    T_grad+3U_omega=0,
    F_omega''(1)=6U_omega=-2T_grad<0.

Thus the unconstrained radial amplitude Hessian has a negative quadratic direction. Scaling also changes charge; it is not a fixed-charge perturbation with zero velocity. Finding this negative direction is therefore neither a surprise nor an instability certificate.

As an optional family check, when Hplus_0 is invertible on the relevant radial amplitude space,

    dQ/domega=||p_P||^2+<a_Q,Hplus_0^(-1)a_Q>.

The rank-one determinant factor is (dQ/domega)/||p_P||^2. Turning this slope into a stability conclusion additionally needs the Morse-index/nondegeneracy hypotheses, such as exactly one unconstrained negative radial direction and no extra kernel. The slope sign alone cannot substitute for them. The direct fixed-charge Hessian test avoids assuming that whole theorem without checking its inputs.

## 5. Exact phase-block positivity under a nodeless-profile hypothesis

Assume g>0, f(r)>0 and b(r)<0 in the interior. For a decaying subthreshold background, b<0 follows from

    (-laplacian+D)b=-g f^2, D>0,

and the positive inverse with decaying/Dirichlet boundary conditions. Set S_P=diag(1,-1). The conjugated phase operator has negative off-diagonal -k with k=2g f>0, and positive zero vector

    y=(F,-2B)>0,
    (S_P Hminus_0 S_P)y=0.

For a smooth compactly supported real test vector z_i=y_i v_i, integration by parts gives the exact ground-state identity

    <z,(S_P Hminus S_P)z>
       = integral [y_1^2|grad v_1|^2+y_2^2|grad v_2|^2
                       +k y_1 y_2(v_1-v_2)^2]d^3x >=0.

Extension by quadratic-form closure handles the origin/tail where y approaches zero. No division by zero at the boundary is used as a pointwise test. This proves phase positivity in **all angular sectors**, conditional on the exact positive background. For ell>0 the radial expression has the additional nonnegative centrifugal term. The ell=0 kernel is the common phase vector, subject to connectedness and the stated domain.

Nodelessness of a numerical profile is finite evidence for the hypothesis, not a rigorous existence/positivity certificate for the exact profile. Small finite-grid negative phase eigenvalues or phase-zero residuals must be convergence-audited rather than relabeled as continuum instability or exact positivity by decree.

## 6. Nonradial amplitude positivity needs stronger hypotheses

Suppose in addition that the exact radial profiles satisfy f'<0, b'>0 and h'>0 for r>0. Conjugate Hplus_1 by S_A=diag(-1,+1,+1). Its two nonzero off-diagonals become -2g f and -sqrt(2)a f, and its translation zero vector becomes

    y=(-F',B',h')>0.

The same componentwise ground-state identity, now with the connected star graph of couplings, gives

    <z,(S_A Hplus_1 S_A)z>
      = integral_radial [sum_i y_i^2 |d_r(z_i/y_i)|^2
                  +sum_(i<j) k_ij y_i y_j(z_i/y_i-z_j/y_j)^2] >=0.

Here the ell=1 centrifugal term is already included in Hplus_1, and k_12=2g f, k_13=sqrt(2)a f, k_23=0. The kernel is the translation radial vector under the connectedness/domain assumptions. For ell>=2,

    Hplus_ell=Hplus_1+[ell(ell+1)-2]/r^2,

so the additional angular term is positive. Together with phase positivity this supplies a sufficient nonradial energy test, modulo translations and their centre-motion partners.

**Do not infer f'<0 merely from f>0.** Strict monotonicity is an extra hypothesis unless separately proved for the branch. Given f'<0, the other two signs follow under the isolated hypotheses from

    (L_1+D)b'=-2g f f'>0,
    (L_1+U''(h))h'=-2a f f'>0,
    U''(h)=3(h-M/8)^2+61M^2/64>0.

Positive inverses then imply b',h'>0. A discrete monotonicity scan can support, but cannot prove, these continuum inequalities. If any hypothesis fails, this analytic positivity route is unavailable; the full operator remains valid and the actual nonradial dynamics still needs testing.

## 7. Scope and discriminating numerical checks

The homogeneous phase's positive compressibility and reduced amplitude Hessian do not establish any of the fragment hypotheses above. Spatial gradients, surface modes, all five real fields and the global charge constraint are essential.

For the finite calculation, preserve at least: canonical normalization; ell=0 fixed-Q rank one; U(1) residual; isolated translation residual and finite-box symmetry breaking; lowest-eigenvalue convergence in mesh and box; residuals; sampled profile/derivative signs; and the distinction between the spatial Hessian and the full gyroscopic spectrum. A shift below a justified pointwise matrix-potential lower bound can help target the actual lowest eigenvalues. Successful finite controls remain finite evidence.

No passed energy test predicts a merger, outgoing branching fraction, cooling time, low-density population, angular bias, the dwarf mass inventory or the empirical force law. Those remain separate same-action/observable obligations. This operator supplies a mathematically normalized next test, not a completed theory or a stability conclusion extracted from one coarse eigenvalue.

Review provenance: independent analytic derivation of the full canonical Hessian, gyroscopic signs, conserved linear charge, fixed-Q rank-one correction and ground-state transforms. A symbolic Hessian reconstruction checks all entries; no authors' stationary/spectral/PDE script is executed. This was not blind to the previous action/audit, and every continuum positivity statement retains its exact-profile/domain hypotheses.
