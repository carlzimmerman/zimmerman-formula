# Late-vacuum scalar perturbations of the variable clock

Base 1ae6550b4e6ba3de8a7bf23fb2e3b9c590ae324a; own preceding checkpoint 70e930c0d. Verdict: within the specified local phenomenological action, the linear-coupling family has positive scalar kinetic coefficients for every nonzero Fourier mode and future-bounded linear perturbations of its expanding de Sitter vacuum. The canonical scalar decays and the metric scalar freezes. This is a self-reviewed action-level result, not a microscopic theory, a nonlinear stability theorem, or a solution of 32π.

## Scope and background

Use the action of CANONICAL_CLOCK_RESULTS.md with lambda=lambda(q), critical eta=2 from auxiliary polarization, canonical kinetic Z>0, and curvature term −kappa R3²/Mstar², kappa>=0. There are no matter perturbations. On the constant-q vacuum,

    H²=2U/(3M²S),  S=3lambda−1,
    U'=−(9/2)M²H²lambda',
    M²=1/(8πG),  H>0.

Primes on U and lambda denote q derivatives at the vacuum. The particular family is U=A/q²+Bq² with A,B>0 and lambda=1+ell q, ell>0. Its unique vacuum lies between 3^(−1/4)(A/B)^(1/4) and (A/B)^(1/4). These background and convexity results extend the unit-normalized trial in VARIABLE_CLOCK_RESULTS.md by direct rescaling.

Take h_ij=a² exp(2zeta)delta_ij, lapse N=1+n, scalar shift with linear divergence chi, and Q=sqrt(Z)deltaq/M. Let physical X=k_com²/a², so Xdot=−2HX. Exclude k_com=0 in the shift reduction; the homogeneous scalar was separately audited. Define constants

    B_lambda=lambda−1>0,  tau=M lambda'/sqrt(Z),
    alpha=2S/B_lambda,
    b=6H tau/B_lambda,  d=9H²tau²/B_lambda,
    m_F²=U''/Z+(9/2)M²H²lambda''/Z,
    Delta=alpha H²+2X,  T=alpha H².

All fields below are infinitesimal; unit amplitudes in finite checks specify a basis that can be scaled arbitrarily small.

## Derive and eliminate constraints

Normalized by M²/2, the quadratic Lagrangian density divided by a³, up to boundaries, is

    −3S u²+2S u chi−B_lambda chi²
    −18H tau Q u+6H tau Q chi
    +Qdot²−(X+m_F²)Q²
    +X(2zeta²+4n zeta+2n²)−16kappa X²zeta²/Mstar²,

where u=zetadot−Hn. The Q u and Q chi terms are essential: dropping them treats the varying coupling as an external parameter and gives the wrong mass and mode mixing.

The script independently expands the periodic one-dimensional ADM scalar mode before using this expression. In that expansion K has eigenvalues (f−chi,f,f)/N, where f=H+zetadot−N^i partial_i zeta. The second-order shift-advection term cancels the volume-shift cross term after spatial averaging. Potential cross terms cancel using both background equations. The remaining metric-only temporal boundary is a^−3 d[−9a³SH zeta²]/dt. Spatial isotropy and Fourier orthogonality extend the one-mode scalar coefficient calculation to each wavevector at quadratic order.

Eliminating chi gives chi=(S u+3H tau Q)/B_lambda. Eliminating the lapse then gives

    n=(alpha H zetadot+bH Q−2X zeta)/Delta,

and the reduced expression

    alpha zetadot²+2bQ zetadot
    −(alpha H zetadot+bH Q−2X zeta)²/Delta
    +Qdot²−(X+m_F²−d)Q²+2X zeta²
    −16kappa X²zeta²/Mstar².

Do not freeze X while integrating temporal boundaries: it redshifts. In particular, the zeta zetadot term supplies curvature-dependent terms that the earlier Minkowski principal-part calculation omitted.

After those integrations, write

    L2/a³ = K zetadot²+Qdot²
             +g(Q zetadot−zeta Qdot)
             −V_z zeta²−N_Q Q²+J Q zeta,

with

    K=2alpha X/Delta>0,
    g=2bX/Delta,
    V_z=8alpha H²X²/Delta²+16kappa X²/Mstar²,
    N_Q=X+m_F²−d+b²H²/Delta,
    J=2bH X(T−2X)/Delta².

The two time-kinetic coefficients are positive. The antisymmetric mixing is not a kinetic ghost. At X approaching zero the metric coefficient degenerates; this limit cannot be used to claim strong-coupling control.

## Positive-potential check for the linear coupling

Let m=m_F²−d. For lambda=1+ell q, the vacuum relation gives d=−2U'/(Zq), and therefore

    m=(2A/q⁴+6B)/Z>0,
    d=4(A/q⁴−B)/Z>0,
    b²/(8alpha)=d/(4S)<d/8<m.

For kappa=0 the determinant of the symmetric potential matrix is H²X²/Delta⁴ times

    8alpha X Delta²+(8alpha m−b²)Delta²
    +8b²T(T+3X),

which is strictly positive for X>0. Adding kappa>=0 adds 16kappa X²N_Q/Mstar² to the determinant. Thus the potential matrix is positive in this exact reduced-action representation. With coefficients frozen, its gyroscopic frequency polynomial is

    K omega⁴−(V_z+K N_Q+g²)omega²
       +(V_z N_Q−J²/4)=0.

It has positive real omega² roots. This frozen-coefficient diagnostic alone is not a stability proof on a time-dependent spacetime, nor is freezing justified for frequencies of order H. The next argument instead uses the actual redshifting equations.

Explicitly, the discriminant is (V_z−K N_Q)²+2g²(V_z+K N_Q)+g⁴+K J², positive for this family. The root sum and product are positive by the preceding potential and kinetic inequalities.

## Exact mode transformation and future-boundedness proof

Define

    I=(zetadot+H zeta+(b/alpha)Q)/Delta,
    m_hom²=m_F²−d+b²/alpha=(S U)''/(Z S)>0.

The exact Euler–Lagrange equations reduce to

    zetadot=−H zeta+Delta I−(b/alpha)Q,
    Idot=−8kappa X zeta/(alpha Mstar²),
    Qddot+3H Qdot+(X+m_hom²)Q=2bX I.

For kappa=0, I is conserved and the canonical scalar is a positively massive damped oscillator with a source proportional to exp(−2Ht). The homogeneous mass agrees with the previously derived background constraint reduction.

For any fixed finite initial wavevector and finite kappa>=0, the same equations give a direct future-boundedness argument. In variables y=(zeta,I,Q,Qdot), write ydot=(A_infinity+E(t))y. All entries of E(t) are constant multiples of X=X_initial exp(−2Ht), so their norm is integrable to the future. The constant limiting system has one simple zero eigenvalue, eigenvalue −H, and the roots of r²+3Hr+m_hom²=0. The latter have negative real parts. Its matrix exponential is bounded even at coincident negative eigenvalues, since any Jordan factors multiply decaying exponentials.

Variation of constants then bounds ||y(t)|| by M||y(0)||+M integral_0^t ||E(s)|| ||y(s)|| ds for a finite M bounding that exponential. Iterating this inequality gives ||y(t)||<=M||y(0)|| exp(M integral_0^infinity ||E(s)||ds), a finite bound. This supplies the all-initial-amplitude, fixed-wavevector linear statement; the numerical samples are not its proof.

Bounded zeta makes Idot integrable, so I tends to I_infinity. The scalar equation is a constant damped massive oscillator driven by X(2bI−Q), which decays; hence Q and Qdot tend to zero. The first equation then implies zeta tends to alpha H I_infinity. Its derivative tends to zero, the lapse perturbation tends to zero, and the intrinsic curvature perturbation proportional to X zeta decays.

This proves future boundedness and the stated limits, not monotonic decay, a uniform bound as k_initial tends to infinity, or absence of finite transient amplification. The bound can worsen with initial momentum. It does not cover the evolving radiation background, arbitrary foliation backgrounds, quantum fluctuations, nonlinear interactions, causal propagation or an EFT used above its cutoff.

## Finite evidence and remaining obligations

variable_clock_modes.py passes 50 checks. They include direct periodic ADM expansion, shift/lapse elimination, both redshifting boundary terms, the triangular transformation, determinant decomposition and mass-floor identities. Twelve trajectories use ell={1,10}, initial k/H={0.1,1,10}, kappa={0,0.01}, A=B=M²=Z=Mstar=1 over 16 e-folds. Six kappa=0 trajectories are also integrated using the untransformed second-order equations; their largest absolute field difference is approximately 1.06×10^−10. All twelve show the predicted late scalar decay and finite metric amplitude under the declared tolerances. The bounded run and input/output hashes are in runs/variable_clock_modes/manifest.json.

Passed within the assumed action: exact quadratic reduction, positive scalar kinetic coefficients, positive reduced potential for the linear family, and fixed-wavevector future linear boundedness on its vacuum. Open: perturbations during the radiation-to-vacuum transition, nonlinear/strong-coupling control, the nonlocal fermion response and causal completion, cosmological-to-galaxy matching, observations, protection of critical eta, and selection of 32π. No external paper is used to assert the new reduction or a novelty claim.

This removes the late-vacuum linear scalar instability as an immediate reason to abandon this particular local action. It does not close the research goal. The next substantive task is matching the vacuum scalar and clock to a galaxy: using q0 from flat static space without checking its boundary against q* would still give an unverified acceleration coefficient.
