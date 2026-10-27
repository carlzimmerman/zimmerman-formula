# Raw round-2 derivation: de Sitter endpoint and oblique principal modes

Input: the exact Hodge/clock candidate in round 1, published base
`8aa3f7046a7ae14a99f3515fd42df5bf061fb1db`. Units c=1, signature (-+++),
K=4piG>0; beta,eta,gamma>0; physical spatial **covector** P; u=K|P|<a0.
The round-1 independent review confirms only its stated flat/static/principal
calculations. None of its Minkowski evidence substitutes for this derivation.

## A. The unchanged candidate

In unitary clock gauge T=t, orthogonality gives P0=N^i Pi. Let

    Kij=(dot hij-Di Nj-Dj Ni)/(2N), theta=trace K,
    Ei=(dot Pi-Lie_shift Pi)/N, Fij=partial_i Pj-partial_j Pi,
    d=Di P^i, u=K sqrt(h^ij Pi Pj).

The gravitational/polarization ADM Lagrangian divided by N sqrt(h) is

    [R3+Kij K^ij-(1+beta)theta²-2Lambda]/(4K)
    +P^i Di log N-W_full(u)+eta E²/2-gamma d²/2-gamma F²/4,

where `W_full=a0²[-u/a0-log(1-u/a0)]/K`. There is no matter in the
de Sitter vacuum calculation. The covariant clock is varied, not prescribed;
the unitary gauge is legitimate only on the branch with timelike dT.

## B. Background equations, including the expansion stress

Set Pi=0, Ni=0, hij=a² deltaij and retain N(t). Write A=2+3beta and
H_N=adot/(aN). The background action is exactly

    Lbg=-3A a adot²/(4K N)-Lambda N a³/(2K).

Lapse variation gives `3A H_N²=2Lambda`. Scale-factor variation at N=1 gives
`A(2 Hdot+3H²)=2Lambda`. Their common expanding solution is

    H=constant>0,  H²=2Lambda/[3(2+3beta)].

The clock term's stress, defined by varying that term separately while retaining
the Einstein-Hilbert term on the left, is

    rho_beta=-9beta H²/(4K),
    p_beta=3beta(2Hdot+3H²)/(4K).

It is covariantly conserved on this homogeneous ansatz. On de Sitter it has
`p_beta=-rho_beta`; omitting it would incorrectly give H²=Lambda/3. This effective
negative background energy is not a statement about the physical perturbation
kinetic signs, which must be reduced separately below.

For pure bare-Lambda dark energy, rho_DE=Lambda/(8piG)=Lambda/(2K).
S1 gives `a0²=kappa² Lambda/(8pi)` in c=1; at kappa=1/2,

    a0²=Lambda/(32pi),  H²=64pi a0²/[3(2+3beta)].

Thus Lambda, H and a0 are all nonzero here. If observational rho_DE includes
other clock/matter stress rather than the bare-Lambda density, that is a
different normalization question; it is not silently substituted here.
The homogeneous T equation is satisfied: changing a homogeneous monotone T
does not change n_mu, and its local spatial equation vanishes by homogeneity.
Pi=0 solves its own equation because the lapse has no spatial gradient.

## C. Nonzero-k scalar quadratic action before constraints

Take `hij=a² exp(2zeta) deltaij`, `N=1+n`, `Pi=partial_i sigma`, use spatial
diffeomorphisms to remove the second scalar metric perturbation, and retain
the scalar shift through `Y=partial_i N^i`. For a Fourier mode k>0 write
`p=k/a`, the physical wavenumber. Overall real-mode normalization is common to
every term. After using only the background equations and integrations by parts,

    Lg/a³=[-3A(zetadot-Hn)²+2A(zetadot-Hn)Y-beta Y²
            +2p² zeta²+4p² n zeta]/(4K),

    LP/a³=p² n sigma+eta p² sigmadot²/2
            -K p² sigma²/2-gamma p⁴ sigma²/2.

An independent direct expansion can use a single real mode
`zeta=eps z cos(kx)`, `n=eps n0 cos(kx)`,
`N^x=eps Y0 sin(kx)/k`. If
`q0=H+zetadot-N^x partial_x zeta` and `X=partial_x N^x`, the exact diagonal
extrinsic-curvature numerator is `(q0-X,q0,q0)`. Consequently its kinetic
combination is `-3A q0²+2A q0 X-beta X²`. Expand `exp(3zeta)/N` and average
the mode before dropping the z*zdot boundary term with its a³ weight. This
reproduces the displayed bracket and retains the otherwise easily missed
lapse-squared and shift-lapse terms.

## D. Eliminate shift and lapse, then the remaining auxiliary combination

For beta>0,

    Y=A(zetadot-Hn)/beta.

Set `C=A/(K beta)` and `Z=zeta/K+sigma`. Then

    L/a³=C(zetadot-Hn)²/2+p² zeta²/(2K)+p² n Z
          +eta p² sigmadot²/2-K p² sigma²/2-gamma p⁴ sigma²/2.

The lapse equation at H>0 gives

    n=zetadot/H-p² Z/(C H²).

After substitution,

    L/a³=eta p² sigmadot²/2+p² Z zetadot/H
          +p² zeta²/(2K)-K p² sigma²/2-gamma p⁴ sigma²/2
          -p⁴ Z²/(2C H²).

Use `zeta=K(Z-sigma)` and `d_t(a³p²)=H a³p²`. Integrating only the
`a³ K p² Z Zdot/H` term removes `+Kp² Z²/2`. The result is

    L/a³=eta p² sigmadot²/2-K p² Z(sigmadot+H sigma)/H
          -gamma p⁴ sigma²/2-p⁴ Z²/(2C H²).

Now Z is auxiliary, with

    Z=-C K H(sigmadot+H sigma)/p².

Define `B=C K²=K(2+3beta)/beta`. The reduced action is exactly

    S_scalar²=1/2 integral a³ [eta p² sigmadot²
                       +B(sigmadot+H sigma)²-gamma p⁴ sigma²] dt,

or, after integrating the cross term with the a³ measure,

    S_scalar²=1/2 integral a³ [Q(p) sigmadot²-V(p) sigma²] dt,
    Q=B+eta p²,  V=gamma p⁴+2B H².

No claim about exact k=0 follows from these eliminations. No lapse, shift or
auxiliary variable has been assigned a propagating-mode sign before elimination.

## E. Actual de Sitter evolution, not a frozen-frequency slogan

The equation is

    Q sigmaddot+H(3B+eta p²) sigmadot+V sigma=0.

Since p_dot=-Hp,

    E_scalar=(Q sigmadot²+V sigma²)/2,
    E_scalar_dot=-H(3B+2eta p²) sigmadot²-2H gamma p⁴ sigma² <=0.

For positive coefficients and H>0, this positive definite energy controls sigma
and sigmadot at every time and every fixed k>0. This proves linear boundedness
of the reduced vacuum scalar, not merely a positive instantaneous omega².
It does not prove nonlinear stability, strong hyperbolicity, or a uniform
constraint estimate over arbitrary backgrounds.

The late-time equation in p is

    (B+eta p²)p² sigma_pp-2B p sigma_p+(2B+gamma p⁴/H²)sigma=0.

Its indicial exponents are 1 and 2. The two regular asymptotic branches are

    sigma_1=p[1-gamma p⁴/(12B H²)+O(p⁶)],
    sigma_2=p²[1-eta p²/(3B)+O(p⁴)].

Reconstruction gives `zeta=-B H(sigmadot+Hsigma)/p²-Ksigma`. It decays on the
first branch and tends to a constant on the second; the reconstructed lapse and
physical shift decay. Thus the apparent 1/p² in the constraint is not by itself
an exponentially growing metric mode. Uniform control of arbitrary initial
data as k approaches zero remains a separate constraint/domain question.

For transverse covector polarizations, metric vector shifts decouple at P=0:

    S_PT²=1/2 integral a [eta |dot Pi_T|²-(K+gamma p²)|Pi_T|²] dt,
    Pi_T_ddot+H Pi_T_dot+(K+gamma p²)Pi_T/eta=0.

Their positive oscillator energy decreases as
`-eta H |Pi_T_dot|²-H gamma p² |Pi_T|²`. For physical components `qT=Pi_T/a`,
the equation is `qT_ddot+3H qT_dot+[2H²+(K+gamma p²)/eta]qT=0`.
Tensor perturbations have `a³[hdot²-p² h²]/(16K)` and the usual friction 3H;
their speed is c and their kinetic coefficient is positive.

## F. Exactly homogeneous modes and noncommuting limits

At exactly k=0, the representation `Pi=partial_i sigma` carries no uniform
covector perturbation. Start again with the fields, not the k>0 reduced formula.
The homogeneous metric scalar has

    L_metric,k0/a³=-3A(zetadot-Hn)²/(4K).

Its lapse constraint is `zetadot-Hn=0`, and its on-constraint action vanishes.
It is the homogeneous coordinate/background-normalization freedom, not an
extra scalar oscillator. The homogeneous shift is a translation/gauge variable.

Three homogeneous covector components Pi(t) are allowed independently; they
have `a[eta dotPi²-K Pi²]/2`, hence

    Pi_ddot+H Pi_dot+(K/eta)Pi=0.

They have positive kinetic and restoring terms. Homogeneous traceless metric
perturbations satisfy `hddot+3H hdot=0`. This separately resolves the quadratic
homogeneous vacuum sector, but it does not make the finite-k longitudinal
constraint map continuous at k=0. Also H=0 and beta=0 were excluded when
eliminating n and Y. Along S1 the limit H->0 also sends a0->0 and shrinks the
potential domain; it is not the fixed-finite-a0 auxiliary Minkowski family.

## G. Full oblique static principal block

Freeze a regular **static clock-aligned** background at a point with nonzero
P, Ebar=0 and theta=0, and take k along z. Background derivatives and potential
curvatures are finite and subleading in the high-k limit. Write
`P=(P_L,P_T1,P_T2)`, `q=delta P_L`, `r=delta P_T`, and `y_i=ik delta N_i`.
The leading lapse relation is `zeta=iK q/k+O(k^-2)`.

The complete shift block at this order is

    L_principal=eta[(qdot-P.y)²+|rdot|²]/2
                +y^T S0 y/2-gamma k²(q²+|r|²)/2,
    S0=diag[-beta/(2K),1/(4K),1/(4K)].

The electric coupling mixes the longitudinal polarization with all three shifts;
dropping the transverse shifts would miss its angular dependence. Define

    Delta=1+eta P^T S0^-1 P
         =1-2K eta P_L²/beta+4K eta |P_T|².

For Delta != 0,

    y=eta S0^-1 P qdot/Delta,
    L_reduced=eta qdot²/(2Delta)+eta |rdot|²/2
               -gamma k²(q²+|r|²)/2,
    omega_q²/k²=(gamma/eta)Delta,
    omega_r²/k²=gamma/eta.

The shift determinant is `det S0 * Delta`. At Delta=0 its null vector is
`S0^-1 P`, and the shift equation is compatible only if qdot=0. This is a rank
change; extending the reduced formula across it is invalid.

Write `u=K|P|`, `r0=2eta u²/(K beta)` and angle theta between k and P. Then

    Delta=1-r0+(1+2beta)r0 sin²(theta).

Consequently the round-1 strict inequality `beta>2eta a0²/K` is both necessary
and sufficient for a strictly positive **uniform angular principal margin**
over `0<=u<=a0` (the action itself only admits u<a0). Equality is pointwise
positive for finite u<a0 but loses its limiting aligned margin. If beta<2eta a0²/K
strictly, an aligned open interval inside the cap has a negative kinetic coefficient
and a negative omega². The conclusion concerns accessible high-frequency modes
of this continuum action; an independently justified EFT cutoff can change its
physical reach. It does not settle low-frequency halo modes or evolving Pbar.

The two TT polarizations retain the round-1 principal block; their transversality
removes the derivative metric-polarization mixing. The five reduced physical
principal polarizations on this regular static branch therefore consist of two
luminal tensors, two transverse P modes and the angular longitudinal P mode.
This is not a nonlinear or arbitrary-time-dependent degree-count theorem.

## H. A limited cubic check, not a strong-coupling certificate

At finite a0,

    W_full=K |P|²/2+K² |P|³/(3a0)+O(|P|⁴).

For the scalar branch the direct potential cubic term scales as
`-a³ K² p³ |sigma|³/(3a0)`. Let u_amp be the spatial L-infinity amplitude.
Using `integral |P|³ <= |P|amp integral |P|²`, its integrated ratio to the
positive reduced quadratic restoring term obeys

    R_W <= R_envelope(p)=2K p² u_amp/[3a0(gamma p⁴+2B H²)],
    sup_p R_envelope=K u_amp/[3a0 H sqrt(2B gamma)],
    p_peak⁴=2B H²/gamma,  u_amp=Kp|sigma|.

For a real single sinusoidal mode the actual integrated ratio is
`8/(3pi)` times the envelope, from its cubic/quadratic spatial averages.
This is an upper bound for that **one direct cubic contribution** evaluated on
the linear scalar parametrization. It identifies a classical nonlinearity scale.
Constraint substitution and gravitational/clock vertices supply other cubic
terms, and |P|³ is not analytic to third order in Cartesian components at P=0.
Thus neither this bound nor quadratic positivity determines a quantum cutoff,
all cubic interaction strengths, or nonlinear well-posedness. Those claims are
explicitly left open rather than inferred from the linear vacuum calculation.
