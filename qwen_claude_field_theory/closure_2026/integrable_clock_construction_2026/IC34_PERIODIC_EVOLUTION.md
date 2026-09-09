# IC34: many-step inhomogeneous evolution, with the periodic zero mode retained

Base 9e7bf25b9ae48e287537fa708d7ae252be272951, 2026-09-09.
Original full-theory target **OPEN**. This is a new dynamical test of the SAME
IC29/30 action, not a new constitutive law or a completed MOND galaxy.
Credit: Carl Zimmerman's exponential law, vacuum-scale proposal and primordial
clock direction motivate this construction. No empirical calibration or novelty
priority is asserted.

## 1. Why periodic geometry is used

IC33 supplied the previously omitted tracefree metric equation. Its exterior
still has diagnostic radial boundary conditions rather than a derived match
to a galaxy. A first many-step test should not depend on arbitrary incoming
boundary data. Here all fields are periodic in x of period 2pi, independent of
the two transverse coordinates. This is a plane-symmetric cosmological test
case of the same local action, not the spherical exterior claimed as solved.

Keep independent spatial metrics before varying:

    hbar = diag(exp(2a), exp(2b), exp(2b)), J=exp(a+2b),
    Rbar=exp(-2a)[-4b''-6b'^2+4a'b'].

The script independently reconstructs this scalar from the three-dimensional
Christoffel symbols. The gravitational radial-coordinate-free density is

    Lg/J =
      2(q+2sh) adot/3 + 4(q-sh) bdot/3
      -2t sh^2/3 + t q^2/6 + A q z + exp(S)P0 + D z^2 + E4 z^4
      +eta exp(S)ell(w-wc)
      -2(q+2sh)(beta'+beta a')/3 -4(q-sh)beta b'/3
      +v Rbar+2v exp(-2a)[2u xi xi' u'+xi^2 u'^2].

Every coefficient and the off-pin fields P0, eta, u, xi, v, t have the
definitions in IC30. For each ordinary fluid add

    Lm=Pi sigma_dot - beta Pi sigma' - J H(Pi/J,exp(-2a)sigma'^2).

Curvature integration by parts is checked including the boundary derivative.
Both a and b are varied, with their full canonical time Euler terms,
before imposing the coordinate chart and active pin below.

## 2. The homogeneous anisotropy cannot be discarded

Choose

    a=Q+2Xi(T)/3, b=Q-Xi(T)/3, w=wc, eta=1.

Xi is a homogeneous metric anisotropy, not the auxiliary xi=S+w.
This chart keeps a-b spatially constant without pretending its time derivative
vanishes. The symplectic density is J[2q Qdot+(4/3)sh Xidot].
The homogeneous metric degree of freedom must be retained in any future global
canonical count; this computation does not assign a DOF number to it.

Let HQ=h_q/2 and

    h=-t q^2/6-Aqz-exp(S)P0-Dz^2-E4z^4,
    B=2v(1-u^2), v=m exp(S+2wc)/2, t=exp(2S)/v.

The q and shear variations give

    Qdot=HQ+beta Q'+beta'/3,
    Xidot=beta'+t sh.

Periodicity forces the actual zero-mode compatibility condition

    Xidot = average_x(t sh),
    beta' = average_x(t sh)-t sh.

The spatially constant shift is fixed to zero as a coordinate convention.
Setting Xidot=0 independently would require the extra condition average(t sh)=0.
The initial sinusoidal test does not satisfy that nonlinear weighted condition,
even though its unweighted shear average vanishes. The code keeps the mean
mode and solves only the nonzero Fourier modes for beta. A suppressed-Xidot
negative control measures the gauge equation violation.

## 3. General evolved metric and auxiliary equations

Writing a=Q+2Xi/3, independent metric variation yields

    qdot = beta q' -3h/2+t sh^2
      +exp(-2a)[-2v Q'^2-4v S'Q'+(B-4v)S'^2-4v(Q''+S'')]/2
      +sum_i[3(j_i H_j_i-H_i)/2+k_i H_k_i],

    shdot = beta sh' -3HQ sh
      +exp(-2a)[v(Q''+S''-Q'^2-2Q'S')+(v-B)S'^2]
      +sum_i k_i H_k_i.

Here k_i=exp(-2a)(sigma_i')^2 is a squared spatial gradient, not a Fourier
wavenumber. The displayed matter derivatives are derivatives of each fluid's
own H_i. The initial-slice condition of vanishing fluid gradients is NOT
reimposed after the first step.

The varied lapse constraint is

    C = h_S+(2/3)t sh^2+sum_i H_i
      +exp(-2a)[4vQ''+2vQ'^2+2BQ'S'+2BS''+B_S S'^2] = 0.

The algebraic z constraint is Aq+2Dz+4E4 z^3=0. Its monotone branch for D>0,
E4>0 is evaluated without assigning z by a desired background fit.
The independent w variation gives W_vac+exp(S)ell-sum_i p_w_i=0;
the multiplier is evaluated from this equation, not fixed by hand.

The momentum constraint, independently varied from beta, is

    M = (2/3)q'+(4/3)sh'+4Q'sh-sum_i j_i sigma_i' = 0.

**M is never solved or projected during evolution.** Its drift is an independent
diagnostic of the coupled flow. Lapse and z are nondynamical auxiliaries, so
solving their Euler equations at Runge-Kutta stages is part of the constrained
evolution algorithm, not evidence that momentum preservation has been proved.

## 4. Matter evolves from its canonical action

For each fluid, variation gives

    sigma_dot = beta sigma' + H_j,
    Pi_dot = [beta Pi+2J exp(-2a) H_k sigma']'.

For the unchanged constant-equation-of-state fluid action of IC32,

    H_j=exp(S)v_f, H_k=exp(S)j/(2v_f),

where v_f is obtained from its full timelike Legendre relation. Therefore

    Pi_dot = [Pi(beta+exp(S-2a)sigma'/v_f)]',
    (sigma')dot = [beta sigma'+exp(S)v_f]'.

The integrator stores log(j), with j=Pi/exp(3Q), so its rate includes
Pi_dot/Pi-3Qdot. Both fluids' gradients are stored and evolved.
On the periodic domain integral(Pi dx) must be conserved. The computation
measures its actual drift; it does not renormalize the charges.
These scalar charges supplement, not replace, the original covariant matter
Ward identity and do not certify all baryonic physics before recombination.

## 5. Numerical contract

Use the exact same fixed repaired 81-node coefficient approximation as IC32/33.
No source, state, resolution, or elapsed time refits the coefficient function.
Extrapolation outside its defined S interval is rejected. Stages leaving the
active-pin plateau are rejected.

Initial data are Q=Q_background, q=q_background+0.02 cos(2x),
sh=-(q-q_background)/2, Xi=0, constant fluid canonical densities, and zero
fluid gradients. This satisfies the initial momentum constraint. The lapse is
solved from its periodic nonlinear equation, not from the reference history.

Periodic differentiation uses Fourier collocation. The real first derivative
sets the even-grid Nyquist mode to zero; the second derivative retains its
usual squared frequency. The shift's undetermined mean is zero. The discarded
Nyquist contribution is not hidden: the actual shear-gauge residual is measured.
There is no universal aliasing or high-frequency stability certificate.

At each RK4 stage use a damped Newton solve of C=0, eliminating z. The Jacobian is

    diag((C_vac)_S-(C_vac)_z h_Sz/h_zz+rho)
       +diag((C_vac)_S') Dx +diag((C_vac)_S'') Dxx.

Here C_vac is C without the ordinary-fluid energy. The partial derivatives
are taken in independent field jets before
eliminating z; rho=sum H_i is its S derivative at fixed canonical state.
The solver permits 20 Newton iterations and 16 line-search halvings.
Residual target is 5e-11; no iteration changes the matter or propagating metric
state to enforce a constraint. The multiplier ell is reconstructed afterward.

The main runs reach T=.2 with (N,dt)=(32,.02),(32,.01),(32,.005),(64,.005).
This is 10,20,40,40 time steps respectively, not repeated kicks off one slice.
The regression test also evolves 20 steps to T=.04. All units are model units.
Time and spatial differences, unprojected momentum drift, solved-auxiliary
residuals, charge drift, generated gradients, expansion, and pin margin are
reported. Finite differences between time resolutions are not universal error
bounds. An apparent fourth-order convergence ratio is a finite observation,
not a regularity theorem for the piecewise C2 coefficient approximation.

The normal volume expansion diagnostic (K/3) is evaluated locally as
exp(-S-wc)[Qdot-beta Q'-beta'/3]; its minimum over accepted states is reported.
This measures positive volume expansion in the test, not a fitted Hubble history.

## 6. Interpretation and remaining closure

Passing means a finite, reproducible many-step plane-symmetric solution
approximation with independently monitored constraints and tested refinement.
It does NOT establish an all-background PDE existence theorem or stability.
The full theory remains OPEN even if every scoped check passes.

The next constructive step is nonlinear source/transition evolution connecting
the pinned clock cosmology to the unpinned exponential-MOND branch with physical
matching data. A periodic evolving cosmology cannot substitute for that galaxy.
The full functional Dirac algebra, healthy separately counted clock, all-mode
causality/strong coupling, k=0 and y=0 strata, full PPN and measured Newton
constant, exact weak-field limits/lensing on the connected solution, and
empirical galaxy/binary/cluster/CMB tests remain original obligations.

The vacuum-scale relation and its factor 1/2 remain input. No observational
data were fitted. Lean/lake are not available on the checked PATH; no formal
certificate is claimed. All adverse numerical controls are retained.
