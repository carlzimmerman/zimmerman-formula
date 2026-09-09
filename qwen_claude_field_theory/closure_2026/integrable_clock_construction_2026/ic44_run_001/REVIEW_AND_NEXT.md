# IC44: action-derived moving-boundary transmission

Base: ef2a66f447a0a84047ff214381f007f90bc67d15.
Full gravity objective: **OPEN**. Previous turn: verified progress (IC43).
This turn constructs necessary local joining data, not a completed theory.

## Candidate variational completion and its scope

Let L0 be the actual IC30 radial action density with its pin term removed.
Its explicit expression is emitted as phase_action_density by
ic44_moving_interface.py, directly from radial_action(), not reconstructed
from desired field equations. Locally take

    I_split = integral_{r<R(t)} L0 dt dr
            + integral_{r>R(t)} L0|_{w=wc, w_r=0} dt dr.

The active side is r>R and the inactive side r<R. At their common trace impose
w=wc and x=0, where the IC39 activation is a function of

    x = exp(-6w) q^2/(9 m^2 h0^2) - 1/2.

Use its negative-q boundary q_b=-3 m h0 exp(3wc)/sqrt(2). The inequalities
x>0 and x<0 must hold on the corresponding sides, not just at their boundary.
S,Q and the shift beta have common traces. The monotone algebraic z branch
has D>0, E4>=0, Fz=2D+12E4 z^2>0. For noncharacteristic joins the normal
fluxes below enforce continuous q and shear; the z equation then enforces
continuous z.

This is a split-domain candidate specification, not a globally invertible
multiplier change in IC39. Its inactive Euler equation includes E_w=0; the
active action fixes w and does not impose that equation. Define its reaction by

    E_w^+ = -J lambda,  J=r^2 exp(3Q).

In the original activated bulk lambda=eta exp(S) ell. Here lambda labels the
reaction computed from the active solution; it is NOT an arbitrary new force.
The implementation derives the inactive E_w both by radial Euler variation and
an independent jet-chain derivative, obtaining identical expressions.

A complete global variational/function-space and Hamiltonian formulation is
still missing. The results below are necessary conditions on smooth one-sided
solutions of this candidate. They are not a proof such solutions exist.

## First variation at a moving interface

Write [f]=f^- - f^+ (inactive minus active). Integrating by parts on both sides
and varying the boundary gives normal momentum and shape coefficients

    pi_f = partial L0/partial f_r - Rdot partial L0/partial f_t,
    [pi_f] delta f_boundary
      + [L0 - sum_f pi_f f_r] delta R.

Fixed boundary traces w=wc and q=q_b are varied consistently with boundary
motion. The relevant freely varied S,Q,beta traces give the normal flux
conditions. The radial action's only explicit metric time momentum is 2Jq
conjugate to Q; omitting it gives the wrong transmission law.

IC43 identified the spatial null direction

    ([S_r],[w_r],[Q_r])=(-a,a,-a),

which preserves both physical metric gradients. With continuous metric fields
and shift, the actual normal metric and shift fluxes give

    [pi_Q]/J    = -2 (Rdot+beta) [q],
    [pi_beta]/J = -(2/3)([q]+2[shear]).

Thus for V=Rdot+beta !=0, q and shear must be continuous. Equal q forces equal
z on the monotone branch because the finite difference of the z equation is

    (z_- - z_+)[2D + 4E4(z_-^2+z_- z_++z_+^2)].

Let b=[beta_r]. Hadamard compatibility gives [Q_t]=Rdot*a.
The separately varied q and shear equations then require

    2 V a - 2b/3 = 0,    -4b/3 = 0.

Consequently a=b=0 when V!=0: the spatial null direction does not permit an
arbitrary first-gradient jump through a noncharacteristic moving boundary.
The actual shape coefficient vanishes for the stated derivative-jump family.
This necessary shape check alone does not settle all global variations.

For the recorded IC41 profile, recalculation gives beta=0 and

    V = 0.0162129942135968218025879453488,

so the noncharacteristic restriction applies. This is a calculation from its
recorded jets, not an exact certificate that that profile evolves.

## Constructive second-derivative transmission

The restriction above does not require all second derivatives to agree.
Assume S,w,Q,beta are C1 at the interface, while continuous q and shear may
have first-derivative jumps. Define

    K = 2m exp(S+2w-2Q),       u=(S+2w)/(S+w),
    tau = 2 exp(S-2w)/m,      gamma=A(S)^2/(2Fz),
    (s,b,c,d,h,e)=([S_rr],[w_rr],[Q_rr],[q_r],[shear_r],[beta_rr]).

Here b denotes the SECOND derivative of w, not the preceding temporary
first-jump variable. The time-jump identities are [q_t]=-Rdot*d and
[Q_tr]=-Rdot*c. Differentiating the algebraic z equation gives
[z_r]=-A*d/Fz. The program forms the actual Euler equations, including the
time derivative of 2Jq, before taking their differences.

The six resulting conditions are

    -K[(1-u^2)s+(2-u^2)b+c]                       = 0,
    -K[(2-u^2)s+(4-u^2)b+2c]                      = lambda,
    -K[s+2b+c] + 2Vd                             = 0,
    (2/3)d+(4/3)h                                = 0,
    -2Vc+(tau/3-A^2/Fz)d-(2/3)e                   = 0,
    -(4/3)(tau h+e)                              = 0.

These are respectively the lapse, inactive clock, spatial metric, momentum,
radial derivative of q, and radial derivative of shear equations. This is a
transmission matrix, NOT a Poisson-bracket matrix. Exact elimination computes

    det M = -(64/9) K^2 V^2 u^2,

and generic rank six. No rank or determinant is assigned as an expected result.
For K V u !=0 and Fz!=0, the unique solution is

    [S_rr]     = -(2-u^2) lambda/(K u^2) + gamma lambda/(2V^2),
    [w_rr]     =  (1-u^2) lambda/(K u^2) - gamma lambda/(2V^2),
    [Q_rr]     = gamma lambda/(2V^2),
    [q_r]      = -lambda/(2V),
    [shear_r]  =  lambda/(4V),
    [beta_rr]  = -tau lambda/(4V).

All six substituted residuals vanish exactly. An independent compact-form
audit reproduces every formula from the raw action-derived solution.

In physical logarithmic metric variables F=S+w and Psi_log=-(Q+w),

    [F_rr]       = -lambda/(K u^2),
    [Psi_log,rr] = -(1-u^2)lambda/(K u^2).

Thus a finite reaction can be transmitted by finite second-derivative changes
while the physical metric and its first derivatives remain continuous. This
does NOT establish Phi=Psi, absence of all curvature singularities, or a global
solution. It gives a local candidate mechanism that a multiplier-only test
could miss. The radial, isotropic reduction is not a substitute for the
independent angular equations or the full three-dimensional theory.

## Phase membership and exceptional limits

Because w_r=0 at this interface and x=0 there,

    x_r^- = (q_r^+ - lambda/(2V))/q_b.

For the chosen orientation q_b<0, both sides require positive one-sided x_r
locally. A unit test explicitly rejects a reaction that reverses this sign.
For the fixed IC41 jets (V>0), strict off-side transversality requires

    lambda > 2 V q_r^+ = -2.80981611226683236266431114112.

This is only a local model-unit condition. Equality needs a higher-order
phase-membership test; the program does not call it a pass.

At u=0 a verified left-null combination of the six equations is row 2 minus
twice row 1. At V=0 it is row 2 minus rows 1 and 3. Each annihilates the actual
matrix but leaves source lambda. Hence lambda=0 is NECESSARY at either
exceptional surface in this transmission class. It is not sufficient for
unique evolution there.

The explicit formulas also expose nonuniform limits. With finite nonzero K,
bounded physical jumps near u=0 require lambda/u^2 bounded. When gamma remains
finite and nonzero, bounded Q_rr near V=0 requires lambda/V^2 bounded.
A sufficient joint scaling for all displayed jumps is

    lambda = u^2 V^2 L,

with bounded L, finite gamma,tau, and K bounded away from zero. This scaling is
checked symbolically but NOT derived from dynamics. The exceptional ranks and
possible strong coupling cannot be dismissed by choosing this scaling as input.
Neither u=0 nor V=0 is being relabeled as the homogeneous k=0 sector; that
separate gravitational constraint analysis remains outstanding.

## Evidence, audit and next calculation

All six new Python files executed. The 28-test IC40-44 suite passes (exit 0,
44.918 s); the six IC30 radial regression tests pass (exit 0, 5.018 s).
The initial 25-test suite also passed. Three scientific --strict runs exit 2
because full-theory closure is OPEN; their runners return 1, not a Python
exception. All six final evidence manifests are validated with input hashes.
Exact commands and file inventory are in run_index.json.

The first raw six-matrix determinant calculation was interrupted deliberately
(exit 130) after the stack trace located expensive multivariate GCD expansion
inside SymPy's default Bareiss algorithm. Factoring after each exact Gaussian
row operation reduced the developmental three-test run to 5.209 seconds.
Pivots are chosen from actual entries; determinant, rank and solutions are
computed. This was a computational bottleneck, not a failed construction.
The old IC42 bounded-multiplier failure remains preserved and is not retracted.

Self-audit verdict: the local transmission claim is correct under the stated
radial, regular-branch restrictions; the global completion remains incomplete.
Dependencies are the actual IC30 action, IC39 activation, common-trace
assumptions, and elementary first-variation/jump identities. External theorem
and observational claims are not used. Mathbox auditing separated exact local
algebra from the missing existence and constraint-preservation implications.
Self-proofreading covered this note; no proofreading-driven mathematical-token
changes. Lean/lake are not available on PATH; no Lean certificate is claimed.

The next discriminating calculation is now explicit: evolve BOTH phase
equations with the moving boundary x=0 and the above transmission conditions,
computing lambda from E_w^+, rather than setting w=wc on both sides or supplying
lambda by hand. Determine whether boundary preservation enforces a regular
reaction and the required limiting behavior. Only then can this completion
advance to its full gravitational Dirac, k=0, characteristic, PPN, cosmological
and empirical gates. The local solution does not discharge any of those gates.

Credit Carl Zimmerman for the framework and primordial-clock direction.
L44's activation proposal remains credited in IC39. No priority claim is made.
All previous failed constructions and concurrent Fable work are retained.

Concurrent commits detected before integration: 540d88109 (L56 potential-depth
trigger) and d6cabd648 (L53 saturated carrier). Their changed-file inventories
and opening report sections were inspected, not their complete proofs or
executables. L53's variational-domain distinction is relevant motivation for
checking what a singular coefficient actually means, but it concerns a
different carrier action. No L53/L56 numerical result or closure claim is used
as evidence for IC44, and neither commit was edited.
