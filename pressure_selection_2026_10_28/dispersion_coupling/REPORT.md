# PN28-DISP: a conserving dispersion coupling with a conditional logarithmic limit

Owner `/root/mechanism_closure`, 2026-10-28. Requested base checkpoint:
`66c45c5082f651dd54e171f98c11acd9cb3d9086`. Actual input SHA256 values are in
`INPUT_PROVENANCE.json`; the working tree and HEAD changed concurrently.
Only `pressure_selection_2026_10_28/dispersion_coupling/` is written here.

**Result: a constructive escape from the common-force obstruction, not theory
closure.** An explicit positive-kinetic, Galilean-invariant interaction with
relative stream motion transfers random kinetic energy to a scalar. One
specified convex scalar potential gives a pressure that is polytropic at low
density and asymptotically logarithmic at high density, with positive reduced
compressibility. Its amplitude obeys `B=m_phi^2/(9g^2)` in canonical field units,
but `B` remains independent of the vacuum energy. The potential and selected
phase-space state are modeling assumptions, not microscopic results.

The pressure entering this result is the **total matter-plus-scalar pressure**.
It is not MC27's bare kinetic pressure. Full kinetic formation, phase selection,
finite-gradient halo dynamics and vacuum normalization remain open.

The frozen algebra used by the parallel halo route is `EOS.md`, SHA256
`05f919345cb73c8b96e3f07d5fdb421ae8ee1d24a01e177abc9551aab4092274`.

## Route contract and changed hypothesis

OSC28 proved that an ordinary kinetic metric with a coupling only to total
density/current produces a common force `E+v_b cross B`; its central random
energy trace vanishes. MS27 already introduced a quadratic kinetic-metric
mediator and checked its static quartic elimination. That example did not give
the desired logarithmic response. MC27 then proved a general concavity
restriction on positive affine kinetic elimination, while identifying a
pressure-invisible density-linear energy as a genuine exception.

This route changes the relative kinetic metric itself and performs the actual
energy-exchange calculation. The new potential exploits the density-linear
high-density exception without choosing its coefficient from the acceleration
target. The ratio of exponents is an explicit design choice motivated by the
three-dimensional canonical scaling weights; no symmetry is claimed to force
it. A permitted deformation below tests how dependent the result is on that
choice.

Success for this scoped route means a positive non-gravitational Hamiltonian,
reciprocal random-energy transfer, a constitutive response derived from the
chosen action and state, and an honest fixed-vacuum normalization test. It does
not mean the original physical selection target has been solved.

## 1. Full local action and Galilean invariance

Let positive cold streams have mass densities `rho_b`, separately conserved
continuity equations and velocities `v_b`. Define

    rho=sum rho_b,    u=sum rho_b v_b/rho,
    w_b=v_b-u,        K_v=(1/2)sum rho_b |w_b|^2.

This local action is defined where total rho>0. Its mean velocity and canonical
Hamiltonian need an exterior prescription at rho=0; a finite EOS edge alone
does not supply a well-posed vacuum-crossing dynamical extension.

Let `s` be a real dimensionless scalar, `F^2>0`, and `c_s>0` its propagation
speed relative to the mean medium. Here `c_s` names the scalar propagation
speed, not the reduced matter sound speed. Take the action density

    L=rho |u|^2/2+Z(s) K_v-rho Phi
      +(F^2/2)[(D s)^2-c_s^2 |grad s|^2]-U(s),
    D=partial_t+u.grad,      Z(s)=exp(2s),
    U(s)=V+B[exp(3s)-3s-1],             B>0.                    (1)

The Newtonian gravitational field action may be appended to vary Phi; it is
omitted from the local non-gravitational positivity checks. The stream
continuity constraints are imposed in the ordinary fluid displacement
variation. The potential is coercive, has a unique minimum at `s=0`, and has
`U(0)=V`, `U'(0)=0`, `U''(0)=9B`. We use `V` as the candidate physical vacuum
energy in this nonrelativistic model; a covariant gravitational completion is
not supplied by giving it this name.

Under a constant Galilean boost, all velocities and u shift by the same
constant; `w_b`, `D s`, and `grad s` are invariant. The center-of-mass kinetic
term changes by the usual total mass/current boundary term. Thus (1) is
Galilean invariant up to that term. Using `partial_t s` alone in an arbitrary
laboratory frame would not establish this property; the material derivative
is part of this construction. No Lorentz-covariant or quantum completion is
asserted.

The choice `Z=exp(2s)` is positive at every real s. The scalar potential was
not found in the original cold-field action. Its exponential-minus-tangent
form is a new completion hypothesis that must itself earn a physical origin.

## 2. Positive Hamiltonian and the exact reciprocal source

Let `p_b` be the stream canonical momentum per mass, and `pi_s` the scalar
canonical momentum density. At fixed densities and field gradients,

    pi_s=F^2 D s,
    p_b=u+Z w_b+(pi_s/rho) grad s,
    pbar=sum rho_b p_b/rho=u+(pi_s/rho) grad s,
    p_b-pbar=Z w_b.

Define `K=(1/2)sum rho_b |p_b-pbar|^2=Z^2 K_v`. The exact Legendre transform is

    H_non-grav=
      (rho/2)|pbar-(pi_s/rho)grad s|^2 + K/Z
      +pi_s^2/(2F^2)+(F^2 c_s^2/2)|grad s|^2+U(s).               (2)

After subtracting the constant vacuum baseline V, every displayed term is
nonnegative. The kinetic Hessian at fixed densities and gradients is positive
definite: it is a sum of positive center-of-mass, relative-motion and material
scalar-velocity squares. This is a local non-gravitational statement, not a
positive-energy theorem for self-gravity or all possible relativistic modes.

Scalar variation gives

    partial_t pi_s+div(u pi_s)-F^2 c_s^2 laplacian s+U'(s)
      =Z'(s) K_v=2 Z K_v.                                      (3)

The stream variations include the reciprocal metric and common material-
derivative terms in (2). There is no independent damping term in (1).
Translation/time-translation invariance supplies the corresponding total
momentum/energy conservation on a periodic domain or with its boundary fluxes.

For a spatially homogeneous cell at rest, densities are constant, gradients
vanish, and every canonical relative momentum is constant. Thus K is constant,
while physical relative velocities and energies obey

    w_b=(p_b-pbar) exp(-2s),
    K_v=K exp(-4s),       E_rel=Z K_v=K exp(-2s),
    dot E_rel=-2 E_rel dot s,
    F^2 ddot s+U'(s)=2 E_rel.                                  (4)

Consequently

    d/dt[(F^2/2)dot s^2+U(s)]=+2 E_rel dot s,
    d/dt[E_rel+(F^2/2)dot s^2+U(s)]=0.                          (5)

This is genuine transfer of random-motion Hamiltonian energy. It evades the
OSC28 theorem because the relative canonical/physical velocity relation now
depends on the scalar. The corresponding homogeneous force contains
`dot w_b=-2 dot s w_b`, which is stream-relative rather than common.

The bare kinematic energy K_v and its pressure are also changed. They must not
be substituted into the old ordinary-metric stress ledger: the conjugate
kinetic stress in an isotropic state is `P_kin=2 E_rel/3=2 Z K_v/3`.
Anisotropy is not erased by homogeneous rescaling; a separate isotropization
mechanism would still be needed for general initial data.

`STATIC_WATERBAG.md` separately derives the stationary canonical Hamiltonian
and the coupled finite-gradient kinetic/scalar/Poisson equations. At zero
mean current and zero scalar momentum, `h=p^2/(2Z)+Phi`; a global one-level
`f=f_* 1_(h<mu)` is stationary. Its extension into empty space is explicitly
limited to a declared zero-mean static continuation, not a general completion
of the action's vacuum dynamics.

## 3. A positive outgoing realization actually exports random energy

Equations (4)-(5) by themselves exchange energy reversibly. To test a genuine
outlet, attach the homogeneous scalar coordinate to a positive massless field
on a half-line with action

    L_out=(T/2) integral_0^infinity
          [psi_t^2/c_out^2-psi_x^2] dx,
    psi(0,t)=lambda_out s(t),        T,c_out>0.

The half-line coordinate is an internal rest-frame outlet coordinate. This is
an explicit reduced boundary coupling, not a derivation of a spherical
three-dimensional radiation geometry from (1). The constraint supplies equal
and opposite boundary reaction. With no incoming waves,

    F^2 ddot s+Gamma dot s+partial_s W(K,s)=0,
    W(K,s)=K exp(-2s)+U(s),       Gamma=T lambda_out^2/c_out>0,
    dot E_cell=-Gamma dot s^2,    dot E_out=Gamma dot s^2.       (6)

The test starts with `s=dot s=0` and a zero initial outlet field, so its data
are compatible and contain no hidden incoming energy. Since

    W_ss=4K exp(-2s)+9B exp(3s)>0

and W is coercive for every K>=0, there is a unique minimum. For K>0 it lies
at s>0. The damped one-coordinate system converges to it for every finite
initial energy: energy decreases on a compact sublevel set, its velocity
tends to zero, and the unique possible accumulation point has W_s=0.
This is a theorem for the declared reduction, not a halo attractor theorem.

Four bounded trajectories use `B=F^2=1`, `Gamma=0.6`, K equal to
`0.03,0.3,3,30`. Their complete energy ledger includes relative kinetic energy,
scalar kinetic/potential energy, and exported energy. This calculation starts
from random kinetic energy and explicitly transfers a positive part to the
outlet; it is not merely damping an imposed bulk oscillator.

## 4. A derived conditional pressure, including scalar stress

The exact local minimum and EOS equations are pinned in `EOS.md`. Put
`y=exp(3s)>1`. Stationarity gives

    K=(3B/2)y^(2/3)(y-1),
    E_rel=(3B/2)(y-1),
    W_min-V=B[(5/2)(y-1)-ln y].                                 (7)

To obtain a density response, specify an isotropic one-level canonical
waterbag `f=f_* 1_(|p|<p_F)` with fixed f_*>0. Its elementary momentum integrals
give `K=k rho^(5/3)`, with

    k=(3/10)[3/(4pi f_*)]^(2/3),
    rho_*=[3B/(2k)]^(3/5).

The same relation holds under isotropic canonical affine compression at fixed
phase content. It is not a consequence of arbitrary multistream evolution.
At a static local minimum and with vanishing scalar gradients, variation of
the **complete** energy with physical volume gives

    rho/rho_*=y^(2/5)(y-1)^(3/5),
    P_total=(5/3)K partial_K W_min-W_min
           =(2/3)E_rel-U(s),
    P_total+V=B ln y,
    dP_total/dln rho=5B(y-1)/(5y-2)>0.                          (8)

The kinetic and total material stresses differ by a large amount at high
density:

    P_kin=B(y-1),       P_total+V=B ln y,
    (P_total+V)/P_kin=ln y/(y-1) -> 0.                          (9)

Thus no step equates this result to MC27's bare kinetic logarithmic pressure.
Here a cancellation between kinetic pressure and scalar potential pressure
produces the logarithm. The leading energy is asymptotically density-linear,
precisely the exception permitted by MC27's positive-elimination theorem.

For low density, `P_total+V=(2/3)k rho^(5/3)+o(rho^(5/3))`.
At high density, `y/(rho/rho_*)->1`, so

    P_total+V=B ln(rho/rho_*)+o(1),
    dP_total/dln rho -> B.                                     (10)

The corresponding energy expansion is also explicit:

    W_min-V=(5B/(2rho_*))rho-B ln(rho/rho_*)-B+o(1).

Its first term is pressure-invisible and linear in density. After retaining
that term, the remaining asymptotic energy is precisely the logotropic fluid
energy form. Dropping it before applying the positive-elimination theorem
would incorrectly exclude this construction.

No exact finite logarithmic interval is asserted. The parallel halo route must
use (8), not substitute the old exact-log core formula at finite central
density. In a Newtonian regime, the non-rest-energy contributions should also
remain small relative to `rho c^2`; the high-density ratios require
`B/rho_* << c^2`, which is a state/parameter restriction, not an automatic
property of the chosen action.

## 5. Finite scalar response: a useful restricted mode calculation

There is a closed hydrodynamic approximation in which the local isotropic
waterbag relation is imposed at every time and its internal energy is

    epsilon(rho,s)=k rho^(5/3) exp(-2s)+U(s).

This defines a separate reduced fluid-plus-scalar model. It does not prove
that the full kinetic hierarchy remains isotropic. Linearize this model around
a homogeneous equilibrium with y>1, omit gravity, and keep the scalar's finite
response time. The required curvatures are

    epsilon_rhorho=5B(y-1)/(3rho^2),
    epsilon_rhos=-5B(y-1)/rho,
    epsilon_ss=3B(5y-2),
    epsilon_rhorho-epsilon_rhos^2/epsilon_ss
       =5B(y-1)/[rho^2(5y-2)]>0.                              (11)

Put `c_inf^2=rho epsilon_rhorho`, `m_eff^2=epsilon_ss/F^2`.
For wave number k_w, the two longitudinal mode frequencies satisfy

    [omega^2-c_inf^2 k_w^2]
    [omega^2-c_s^2 k_w^2-m_eff^2]
      -(rho epsilon_rhos^2/F^2) k_w^2=0.                      (12)

Its trace is positive, its discriminant is nonnegative, and its product is

    c_inf^2 c_s^2 k_w^4
      +(rho/F^2)(epsilon_rhorho epsilon_ss-epsilon_rhos^2) k_w^2,

which is positive for k_w>0. Hence both squared frequencies are positive in
this restricted no-gravity model; at zero wave number there is one zero mode
and the massive scalar mode. Thirty finite points check (12). A positive
auxiliary scalar curvature alone would not establish this result: the Schur
complement is essential. Conversely this calculation does not establish the
full Vlasov spectrum, arbitrary-background PDE health, gravitational Jeans
stability, relativistic causality, or stability of a finite halo.

## 6. Finite gradients limit the usable logarithmic halo regime

The actual static scalar equation contains

    -F^2 c_s^2 laplacian s+U'(s)-2K exp(-2s)=0.

Local minimization discards its first term. At a homogeneous equilibrium,

    ell_s^2=F^2 c_s^2/[B(15y-6)].

Compare it with the high-density core scaling length
`L_c^2=B/(4pi G rho_c^2)`. The exact ratio at a central state y_c is

    ell_s^2/L_c^2
      =4pi G F^2 c_s^2 rho_c^2/[3 B^2(5y_c-2)]
      =eta y_c^(4/5)(y_c-1)^(6/5)/(5y_c-2),
    eta=4pi G F^2 c_s^2 rho_*^2/(3B^2).                       (13)

It is strictly increasing for y_c>1: the numerator of its logarithmic
derivative, after multiplying by the positive denominator, is
`25y_c^2-15y_c+8>0`. At large y_c it grows as `eta y_c/5`, approximately
linearly with central density. Thus the formal infinite-concentration
logotropic limit of the local EOS is **not** a controlled finite-gradient
limit at fixed F,c_s,B,rho_*.

There can instead be a finite window. A fractional local slope error below
delta requires `y>(2+3/delta)/5`, because the exact relative error is
`3/(5y-2)`. To demand this through the quarter-density core, impose that bound
at its outer y_q, then set

    y_c^(2/5)(y_c-1)^(3/5)
      >=4 y_q^(2/5)(y_q-1)^(3/5).

At that minimum central y, the gradient condition is (13) much less than one.
This supplies an explicit bound on eta for a chosen accuracy, rather than
assuming all arbitrarily concentrated halos remain inside the effective
description. It is a scale discriminator, not a rigorous error estimate for
the nonlinear spatial boundary-value problem.

The temporal separation must also be checked:

    (4pi G rho_c)/m_eff^2
      =4pi G F^2 rho_c/[B(15y_c-6)]
      ->4pi G F^2 rho_*/(15B).

The density-independent high-density limit of this temporal ratio does not
remove the spatial-gradient growth. A full coupled scalar/kinetic halo is the
next calculation when either approximation fails.

## 7. What determines the amplitude, and what does not

Canonical normalization `phi=F s`, `g=1/F` gives

    Z=exp(2g phi),
    m_phi^2=U_phiphi(0)=9g^2 B,
    B=m_phi^2/(9g^2).                                         (14)

This is an invariant combination of a vacuum scalar stiffness and its
dispersion-metric coupling within the specified parent. It is a useful
replacement for an unexplained fluid coefficient. It is not a prediction of
either parameter or of their ratio to V. V and B are independent coefficients:
changing B at fixed V keeps the same vacuum position and energy and changes
the asymptotic pressure coefficient. The local non-gravitational action
therefore does not select the desired B/V.

Nor is the logarithmic shape protected by the given assumptions. For every
epsilon_d>0, the additional positive potential

    delta U=epsilon_d B[exp(6s)-6s-1]

preserves the vacuum energy, vacuum location, positivity and convexity. At high
density it dominates. Balancing `K exp(-2s)` against its exponential yields
`W_min proportional to K^(3/4)` and therefore, on the same waterbag branch,
`P_total+V proportional to rho^(5/4)`. Nine bounded checks test this changed
asymptote. An independent microscopic symmetry or dynamics must exclude such
allowed deformations before the logarithm can be called universal.

Conditional on the independently established high-density halo limit and the
framework's adopted column identification, one would obtain

    a0^2=pi xi_quarter^2 G B
        =pi xi_quarter^2 G m_phi^2/(9g^2).

No acceleration target, kappa value, or vacuum-normalized B was inserted into
the action or numerical checks. This equation remains a conditional bridge.

## Evidence, review status and continuation

`check_dispersion.py` is preserved as the first attempted run. It reached JSON
serialization and failed because a NumPy Boolean was not a native Python
Boolean; its failure and unchanged source remain in `run/`. The separate
`check_dispersion_checked.py` changes only Boolean serialization, with a fresh
contract and run. No failed physical assertion was retuned. Current execution
and numerical results are summarized in `VERIFICATION.json`.

The analysis rests on the written action and algebra, not on finite sampling.
The coordinator independently reconstructed the EOS and is investigating its
finite-halo hydrostatic realization in a disjoint directory. Full independent
action/mode review remains a separate obligation until explicitly recorded.

The route is open. Its first unproved physical implication is that the
dimensionless scalar dilation, the particular exponential-minus-tangent
potential, and a fixed-level isotropic canonical state arise from the owner's
cold-field parent. For the specified model itself, the next useful calculation
is the full finite-gradient static halo, followed by conserving non-isotropic
kinetic evolution, with boundary fluxes and scalar response retained. That
would test whether the local pressure mechanism survives beyond its declared
reductions. Selecting B/V and the phase-level content remains an independent
requirement even if those dynamical tests succeed.

No existing scientific file, manuscript, shared status record or active job was
modified; no commit, push, expensive simulation or external message was made.
