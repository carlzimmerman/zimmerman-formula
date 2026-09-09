# IC30: vary the galaxy–cosmology bridge before trying to join it

Base `002fba201d1e8830a4e39818ea59c3f926bb51c9`, 2026-09-09.
Full theory **OPEN**. This extends the IC29 constant-tensor action, not a
substitute theory assembled from unrelated successful limits.
Credit: Carl Zimmerman's exponential law, vacuum-scale relation and primordial
clock direction motivate this construction. No empirical fit, global novelty
claim or derivation of his coefficient 1/2 is made.

The preceding conversational answer clarified vacuum density but did not
advance closure. This checkpoint derives executable equations for the missing
inhomogeneous bridge and constructs momentum-compatible transition data.

## 1. Action and exact spherical reduction

Use the entire IC20 phase action with IC29's v=v0, A=.1, E4=.01,
h0=.5 and its fixed, implicitly constructed D(S). Do not change the function
when varying a field or adding sources. Its global extension remains open;
the equations below are functional identities for S-only A,D,E4 wherever
these functions exist smoothly. The implementation keeps those functions
symbolic, so their derivatives are not discarded.

In clock coordinates T=t set, with c=1,

    hbar_ij = exp(2Q) diag(1,r²,r² sin²theta),
    h_ij = exp(2w) hbar_ij, N=exp(S+w), xi=S+w,
    u=(S+2w)/(S+w), v0=m exp(S+2w)/2, t=exp(2S)/v0,
    pi^i_j/V = q delta^i_j/3 + s diag(2/3,-1/3,-1/3).

Here s is the trace-free momentum amplitude, not the coordinate S; beta is
the radial shift, ell the existing pin multiplier, and J=r² exp(3Q).
The coordinate chart requires xi!=0, and the constitutive regular branch
has 0<u<1. These restrictions are not silently extended to degenerate strata.

After angular integration (dividing by 4pi) and radial boundary integration,

    Lrad = J [2q Qdot -2t s²/3+t q²/6+Aqz
              +exp(S)P0+Dz²+E4z⁴+eta exp(S)ell(w-wc)
              -(2/3)q(beta'+3beta Q'+2beta/r)
              -(4/3)s(beta'-beta/r)]
           +r² exp(Q)[2v0 Q'²+4v0(S'+2w')Q'
                       +2v0(2u xi xi' u'+xi² u'²)],

    P0=-m exp(4w)[Lambda+a0² U(u²)]+kappa exp(2w-2S)/2,
    U(c)=(1-c)[ln²(1-c)-2ln(1-c)+2]-2.

eta is precisely the IC18 smooth activation evaluated at
`-exp(-3w)q/(3mh0)`, with eta=0 for its square <=1/2 and eta=1 for
its square >=3/4. Writing eta(q,w) in the symbolic variation retains BOTH
partial derivatives. wc=-1/40; other constants are those of IC29.

`radial_equations()` differentiates this Lagrangian in all eight fields:
S,w,Q,q,z,s,beta,ell. The Q equation additionally subtracts
`2J qdot+6J q Qdot`, the time derivative of its canonical momentum.
Run with `--equations` for the actual expanded expressions. In particular,

    E_q/J = 2Qdot+tq/3+Az
            -(2/3)(beta'+3beta Q'+2beta/r)
            +eta_q exp(S)ell(w-wc),
    E_s/J = -(4/3)(ts+beta'-beta/r),
    E_beta/J = (2/3)q'+(4/3)s'+4(Q'+1/r)s,
    E_z/J = Aq+2Dz+4E4z³,
    E_ell/J = eta exp(S)(w-wc).

The unreduced S,w,Q expressions, including all gradients, are executable,
not replaced by the homogeneous equations. This radial conformal spatial
coordinate choice retains the radial shift equation. A separate independent
radial/angular metric variation below checks the static reduction before
imposing that coordinate choice.

This is a vacuum-exterior reduction. Matter contributions must be varied from
the unchanged minimally coupled action; an arbitrary prescribed radial source
is not inserted into the canonical equations and called conserved matter.

## 2. Static branch follows conditionally from the auxiliary equations

On the open eta=0 plateau, beta=0 and Qdot=0 imply s=0 and

    tq/3+Az=0,
    z[2D-3A²/t+4E4z²]=0.

If t>0, E4>=0 and 2D>3A²/t, the only real solution is q=z=0.
Thus that static restriction can be derived rather than merely imposed.
The inequality must still be checked on a global coefficient extension;
it is not a universal theorem about every action in the family.

All additional trace/auxiliary terms and their first variations vanish there.
For the static physical metric define exact logarithmic potentials

    N=exp(Phi), h_ij=exp(-2Psi)delta_ij,
    w=(u-1)Phi, S=(2-u)Phi, Q=-Psi-w.

Substitution into the varied action gives the exact static density, after the
same boundary integration,

    Lstatic/r² = m exp(Phi-Psi)[Psi'²-2Phi'Psi'+(1-u²)Phi'²]
                 -m exp(Phi-3Psi)[Lambda+a0²U(u²)]
                 +(kappa/2)exp(-Phi-3Psi).

For u!=0, varying u gives

    |a|²=a0² ln²(1-u²), |a|=exp(Psi)|Phi'|,
    u²=1-exp(-|a|/a0).

u=0 is a separate stationary branch. Its rank and limiting health are not
settled by dividing the equation by u. The exact Legendre identity is

    (1-u²)y²-U(u²)=y²-G(y),
    G(y)=y²+2(1+y)exp(-y)-2, y=|a|/a0.

## 3. Independently varied radial and angular metric equations

The code first builds Christoffels and Ricci from

    h_ij=diag(exp(2a),exp(2b)r²,exp(2b)r²sin²theta), N=exp(Phi),

then independently varies a,b,Phi,u, retaining second spatial derivatives
in the curvature density. Only afterward does it set a=b=-Psi. Thus the
angular equation is not inferred from a conformal trace or assigned slip.

With f=1-u², C=Lambda+a0²U(u²), X=1/(2N²), the equations are

    m R3/2-mC-mf a²-2m D_i(f a^i)=rho_m+kappa X,

    m[G3_ij+(h_ij Delta N-D_iD_jN)/N
        +2f a_i a_j-f h_ij a²+C h_ij]
      =T^m_ij+kappa X h_ij.

The code checks these against the action derivatives and also checks the
off-shell radial coordinate Noether identity, including the u equation.
For isotropic ordinary matter, their radial component gives

    2(Phi'-Psi')/r+Psi'²-2Psi'Phi'+(1-u²)Phi'²
       =exp(-2Psi)[(P_r+kappa X)/m-C].

Their radial-minus-angular component gives

    (Psi-Phi)''-(Psi-Phi)'/r
      +Psi'²-2Psi'Phi'+(1-2u²)Phi'²=0.

Consequently, setting d=Phi'-Psi', the radial equation independently fixes

    d²+2d/r=u²Phi'²+exp(-2Psi)[(P_r+kappa X)/m-C].

On the root connected to a weak field, d=-1/r+sqrt(1/r²+right_hand_side).
This is not an empirical prediction until the sources and boundary data are
fixed and the remaining lapse/auxiliary equations solved.

In the local leading weak-field/quasistatic ordering, neglecting the explicitly
retained vacuum/clock sources only when their contribution is demonstrably
small, the independently varied equations reduce to

    Delta(Phi-Psi)=0,
    (Psi-Phi)''-(Psi-Phi)'/r=0,
    div[(1-exp(-|grad Phi|/a0))grad Phi]=rho_b/(2m).

Suitable boundary normalization then removes the constant leading slip.
The high-acceleration coefficient identifies G_N=1/(8pi m), rather than
assigning it to an unrelated bare coupling. This is a leading static result,
not a full nonlinear identity Phi=Psi, a full PPN calculation, or a global
matched galaxy. Exact logarithmic potentials need not coincide beyond leading
order even in GR; that is not a failure of the user's leading no-slip condition.

## 4. Why direct static-to-pinned gluing is not the bridge

Restricted proposition: take an aligned-clock, static, spherical exterior in
the leading MOND regime, with y>0, outward increasing xi, a decreasing spherical
MOND acceleration, and try a C1 finite-radius join to w=wc<0 on an open
cosmological pin region. Write

    mu=1-exp(-y), u=sqrt(mu),
    lambda_parallel=mu+y exp(-y)>0.

Differentiating the spherical mass law r² y mu=constant gives

    r y'=-2y mu/lambda_parallel,
    r u'=-y u exp(-y)/lambda_parallel.

Continuity of w=(u-1)xi=wc forces xi=wc/(u-1)>0. Hence

    r w'=-xi y u exp(-y)/lambda_parallel+(u-1) r xi' < 0.

Both terms are strictly negative. The pinned side instead has w'=0, so this
direct join is not C1. This is a sign proof under the stated leading-regime
hypotheses, not a universal obstruction to the full action. Higher-order
corrections, nonstatic motion or a different clock configuration require the
full equations, not this reduced proposition. For the numerical check,
`r xi'=epsilon*y` with epsilon>0; the conclusion does not require that precise
normalization, only its sign. No would-be matching acceleration is promoted
to a new observational law.

The w equation has, on w=wc,

    E_w(without pin)+J eta exp(S)ell=0.

A bounded ell as eta approaches zero requires the unpinned numerator to be
O(eta). Because eta is flat at its boundary, generic smooth data need not meet
this compatibility condition. A vanishing pin determinant alone is not a
global DOF theorem: preservation must be rederived on the eta=0 stratum.

## 5. Constructive result: a momentum-compatible transition with a shear tail

The exact radial momentum equation derived above integrates to

    (r³ exp(3Q)s)'=-(1/2)r³ exp(3Q)q'.

If q varies monotonically from zero to a negative cosmological value through
a vacuum collar, it cannot have s=0 at both finite endpoints: the weighted
integral has a definite sign. This does not demand an extra propagating
auxiliary scalar. It tells us to allow the existing trace-free momentum.

An explicit initial-slice construction uses Q spatially constant and
dimensionless radii 1<=r<=2. Define x=r-1 and

    q=-(35x⁴-84x⁵+70x⁶-20x⁷),
    s(r)=-(1/(2r³)) integral_1^r R³ q'(R)dR.

For r<=1 set q=s=0. For r>=2 set q=-1 and

    s=C_tail/r³,
    C_tail=-(1/2) integral_1^2 R³ q'(R)dR > 0.

The exact result is C_tail=7/4 in this chosen normalization. The executable
integrates it and checks the momentum equation,
values and derivatives through third order across both endpoints. Thus the
constructed data are C3, not claimed C-infinity. For locally constant t, the
outer shear equation is also solved by

    beta=H_shift r+t C_tail/(3r²).

H_shift is an integration constant, not yet a measured cosmological Hubble
rate. The initial quintic trial was only C2: q'''=-60 at the inner endpoint
forced s'''=30. Rather than hide this failed smoothness check, the implemented
septic profile makes the required third derivatives agree.

This is a constructive exact solution of the radial momentum constraint and
an outer shift equation. It is NOT a solution of the lapse, w or Q
equations, nor is Q=constant here a requirement H=0. It supplies admissible
momentum data for the next coupled boundary-value/initial-value solve. The
q=-1 normalization is freely illustrative; to reach the actual IC29 exterior
it must be replaced by that exterior's momentum while solving the other
constraints. No parameters are fitted to galaxies or recombination data.

The next algebraic constraint can also be solved without changing the action.
For D>0,E4>0, E_z/J=0 is a strictly increasing cubic in z and has the unique
real solution

    z=2 sqrt(D/(6E4)) sinh[asinh(-3Aq sqrt(6E4/D)/(4D))/3].

For E4=0 it is z=-Aq/(2D). Its implicit derivative is
`z_q=-A/(2D+12E4z²)` at fixed S, and the denominator is strictly positive.
Thus the auxiliary solution extends smoothly through q=z=0 in this domain;
one need not divide by z or discard this endpoint. The numerical check holds
S=.1, A=.1, D=.13, E4=.01 (IC29's values at that S) fixed and solves z at
seven radii across the collar. Residuals and derivatives are checked at
50-digit precision. This satisfies the z constraint but still does not solve
the lapse/pin constraints for that prescribed S. A local invertible cubic
alone is not the full nonlinear Dirac or stability analysis.

## 6. Next calculation, certification scope and reproducibility

Solve E_S=E_w=E_z=E_ell=0 with the momentum equation across the collar using
ONE fixed globally extended D(S), then evolve Q,q with the remaining varied
equations and shift condition. Check the eta->0 multiplier compatibility,
the complete nonlinear constraint preservation and physical characteristics.
The static branch and homogeneous cosmology cannot be counted as one solved
galaxy before this step succeeds. The momentum construction changes this from
an unconstrained interpolating ansatz to a specified partially constrained
initial-data problem, without asserting the other constraints are satisfied.

Other open original requirements remain: nonlinear/zero-mode Dirac closure,
all PPN coefficients and high-acceleration calibration beyond the leading
static equation, healthy clock/auxiliary sectors across the transition,
strong-coupling and causal support, global coefficient regularity, real
galaxy/cluster evidence and photon–baryon/CMB evolution. Seven designed e-folds
are not a recombination calculation. The a0–Lambda relation remains input.

Run the six new unit tests and the script with `--strict --equations`.
Strict exit 2 means the scoped checks passed but the full theory is OPEN;
exit 1 means an actual scoped check failed. The bounded-run records retain
that distinction. Existing closure regressions must also be rerun.
No Lean/lake executable was found on PATH; no formal certificate is claimed.
This file receives mathematical proofreading and self-review, not independent
peer review. Arithmetic is exact SymPy plus mpmath50 diagnostics at
y=.001,.1,1,10 and epsilon=1e-6, not interval certification of a PDE solution.
