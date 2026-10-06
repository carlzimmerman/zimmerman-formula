# One P(X), two branches: normalization does not select 32pi, and the clock matters

Checkpoint 2026-10-06. Supplied and observed entry HEAD
`276ae422f0fb0b6990b9824a10fa4979c148aff0`. Writes are confined to this folder.
The substantive result is a scoped obstruction to the simplest same-scalar
proposal: a sourced attractive MOND profile on a fixed timelike clock cannot
extend into a healthy first-derivative condensate. The metric lapse can evade
that flat-clock argument, but the explicit baryon-lapse control has the wrong
mass scaling. Neither stationarity nor branch health selects the vacuum ratio.
There is no complete action deriving 32pi here.

## 1. Declare the source, force, metric and units

Use c=1 and signature (-+++). Let

    S = integral sqrt(-g)[R/(16piG_T)+P(X)] + S_m[A(phi)^2 g, matter],
    X=-g^{mu nu}partial_mu phi partial_nu phi/2,
    A(phi)=exp(alpha phi), alpha>0.

The scalar self-action is shift symmetric and minimally coupled to curvature.
The conformal matter force coupling explicitly breaks the shift symmetry of
**the full action**. This distinction cannot be hidden. G_T is the measured
tensor-sector Einstein normalization, not a Cavendish constant including an
unknown fifth force. No screened high-acceleration continuation is supplied
by the pure cubic model; identifying G_T from a Cavendish experiment would
require an explicit extra kinetic branch or screening and its source audit.
At the local comparison epoch choose A=1; the physical
Jordan tensor normalization is then G_T. A weak, slowly changing conformal
background and a negligible scalar stress contribution to the local Einstein
potential are declared assumptions of the static source/force calculation.

Direct variation gives

    div(P_X grad phi)=-alpha T_m ≈ alpha rho_b,
    T^phi_{mu nu}=P_X partial_mu phi partial_nu phi+P g_{mu nu}.

Here rho_b and its mass are in the local A=1 Einstein frame; higher weak-field
and conformal corrections are neglected. The matter stress reaction obeys
nabla_mu T_m^{mu nu}=alpha T_m nabla^nu phi; the scalar stress supplies the
opposite exchange using its sourced equation. Thus the force is part of the
same varied action, rather than an externally prescribed MOND acceleration.
For an attractive spherical solution u=partial_r phi>0,

    r^2 P_X u=alpha M_b/(4pi),
    g_test=G_T M_b/r^2+alpha u.

The scalar-dominated deep limit defines the measured galaxy acceleration scale.
The choice of alpha is a physical coupling, not fixed by scalar stationarity.

If exact shift symmetry is required of matter as well, this particular source
is inadmissible. A representative derivative coupling J_m^mu partial_mu phi
instead sources the divergence of J_m. A compact conserved static current
has no such monopole source. More generally a stationary spherically symmetric
shift-preserving action conserves the *total* radial shift flux; regularity at
the center sets its net flux to zero absent imposed scalar charge or flux
boundary conditions. It does not supply the alpha M_b charge above by itself.
This is a scoped source objection to the displayed derivative-current repair,
not a classification of every derivative/disformal matter theory.

## 2. The actual normalized a0 and vacuum curvature

For a pure spacelike branch, take

    P(X)=P_0-C(-X)^(3/2), C>0, X=-u^2/2,
    P_X=gamma u, gamma=3C/(2sqrt2).

The positive-flux solution and scalar acceleration are

    u=sqrt(alpha M_b/(4pi gamma))/r,
    (alpha u)^2=G_T M_b a0/r^2,
    a0=alpha^3/(4pi gamma G_T).

The usual Newtonian term remains additive; this cubic branch is a deep-limit
model, not the full adopted P2 law or a high-acceleration completion. Its
normalization cannot be inferred by identifying C with a0 without both the
source alpha and the test force alpha.

A homogeneous clock phi=q t has X_t=q^2/2. In vacuum, a condensate with
P_X(X_t)=0 solves the scalar equation, and its exact Einstein-frame stress is
P(X_t)g_{mu nu}. With no additional bare cosmological constant,

    rho_v=-P(X_t)>0,
    Lambda_E=8piG_T rho_v, H_E^2=8piG_T rho_v/3,
    C_v=Lambda_E/a0^2
       =128pi^3 gamma^2 G_T^3 rho_v/alpha^6.

Restoring c, C_v is Lambda_E c^4/a0^2. The desired C_v=32pi requires
rho_v=4a0^2/G_T in c=1 units; equivalently a0=(c/2)sqrt(G_T rho_v) when rho_v
is a mass density. This equation is an added relation among coefficients,
not a consequence of P_X=0. Under phi_new=s phi, alpha_new=alpha/s and
gamma_new=gamma/s^3, so alpha^3/gamma is invariant: field normalization is
not the missing physical selector.

Adding a constant to P changes rho_v and the Einstein curvature while keeping
the source equation, branch derivatives and scalar principal coefficients
unchanged. This is an exact action-level freedom. It does not keep the metric
or all large-distance galaxy predictions unchanged. A fixed curvature boundary
condition would fix that freedom observationally, not predict its value.

Even imposing a convention P(0)=0 does not suffice for derivative/asymptotic
conditions. Let t=X/X_t and B(t)=10t^3-15t^4+6t^5. A deformation
P_epsilon=P-epsilon B changes P(X_t) by -epsilon but leaves P(0), the first
two derivative jets at 0 wherever those base derivatives exist, and P_X,P_XX
at X_t unchanged. The deformation itself has zero first/second derivative
at 0; it does not repair the exact cubic branch's divergent second derivative. Near X=0- it is O(X^3),
subleading to the cubic-gradient P~(-X)^(3/2), so the asymptotic galaxy a0 is
unchanged. Finite-range galaxy forces and intermediate branch health can
change; this is not a claim of identical full phenomenology. A smooth plateau
supported outside a specified spacelike measurement window can instead leave
that whole window identical, while retaining the condensate derivative jets.
Neither deformation by itself proves a globally healthy interpolation.

## 3. Health and analytic continuation give constraints, not a coefficient

Quadratic scalar fluctuations have principal tensor

    K^{mu nu}=P_X g^{mu nu}-P_XX partial^mu phi partial^nu phi.

On a homogeneous timelike background, positive time kinetic coefficient is
P_X+2X P_XX>0, and positive spatial coefficient is P_X>0. At a nonzero
condensate P_X=0 with P_XX=kappa>0, the time coefficient is 2X_t kappa>0,
but the ordinary k^2 gradient term is zero. A pure P(X) condensate is therefore
a degenerate first-derivative endpoint, not a strictly healthy propagating
wave theory. Higher-derivative terms used to restore dispersion are extra
action operators and need a fresh constraint/stability audit.

On the spacelike cubic branch, the time coefficient is P_X>0 and the
longitudinal spatial coefficient is P_X+2X P_XX=2P_X. The longitudinal speed
squared is 2 in the Einstein metric, and also relative to the conformal
physical light cone; the transverse speed squared is 1. Hyperbolicity alone
does not exclude this, but a stipulated subluminal scalar condition does.
These local health tests involve derivatives, not P(X_t)'s value.

Exact P=-C(-X)^(3/2) on an interval ending at zero is not real analytic through
zero; its second derivative diverges there. Thus analytic continuation cannot
turn that exact branch into a unique healthy analytic timelike condensate.
Complex continuation is not a real scalar action. A smoothing at small |X|
or a finite-window approximation is a changed premise introducing branch
shape/scale choices. Real analyticity on a connected domain plus the exact
complete function on an open subinterval would mathematically remove function
freedom, but the stipulated fractional branch does not have such an extension.
Analyticity alone on an unspecified approximate branch fixes no vacuum ratio.

## 4. A clock changes the galaxy branch: an exact local obstruction

It is invalid to place a homogeneous timelike scalar and an independent purely
spacelike scalar profile into the same X. For one stationary scalar in a local
flat patch,

    phi=q t+psi(r), X=(q^2-u^2)/2.

Stationarity also requires q to be spatially constant: attempting q(r) gives
partial_r phi=q'(r)t+psi'(r), so the profile is time dependent. A local shutdown
of the cosmic clock must be dynamically solved, not declared static.

If the sourced attractive scalar acceleration is exactly MOND, u=A_M/r,
then the Gauss equation enforces, along this branch,

    P_X=gamma u=gamma sqrt(q^2-2X),
    P(X)=P(X_t)-gamma(q^2-2X)^(3/2)/3,
    P_XX=-gamma/u.

This is a shifted cubic, not the pure spacelike function in section 2. In the
(t,r) subspace its full principal tensor, including the clock/spatial mixing,
is

    K_tt=-P_X-q^2P_XX, K_tr=q u P_XX,
    K_rr=P_X-u^2P_XX,
    det K_tr=-P_X(P_X+2X P_XX)
             =-gamma^2(2u^2-q^2).

Transverse coefficients remain gamma u>0. Hyperbolicity requires u>q/sqrt2.
At smaller u the two-coordinate block becomes positive definite, so the
scalar equation no longer has a time-like characteristic direction. At the
threshold it degenerates. The original matter t-slicing has a positive scalar
time kinetic coefficient only for u>q; between q/sqrt2 and q the effective
cone remains Lorentzian but that original slicing is unsuitable. Thus exact
MOND extending to arbitrarily small u on a fixed clock cannot join a healthy
first-derivative condensate. Its formal breakdown radius is

    r_break=sqrt2 A_M/q=sqrt(2G_T M_b a0)/(alpha q).

This is a mass-dependent diagnostic with a free clock scale, not a universal
radius selecting Lambda/a0^2. q=gamma=1, u=.25 gives both principal-block
eigenvalues positive; u=2 gives opposite signs. The finite control supports
the exact determinant proof and retains a mutation dropping P_XX.

A separate argument does not rely on exact MOND. A smooth time-healthy
condensate has P_X(X_t)=0, P_XX(X_t)=kappa>0. On the same flat fixed clock,
small u gives X-X_t=-u^2/2 and P_X=-kappa u^2/2+O(u^4)<0. Hence the radial
flux is negative for an attractive u>0, contradicting the positive baryon
charge. This excludes a stationary attractive weak-gradient approach from
below X_t under those specific local assumptions. The opposite u sign would
make the scalar force repulsive. It excludes neither time-dependent profiles
nor metric-lapse effects nor extra derivative operators.

## 5. The metric-lapse escape and its explicit price

For a static spherical Einstein metric with lapse N and radial metric factor
A_r, the exact kinematics are

    X=q^2/(2N^2)-u^2/2, u=psi'/A_r,
    radial flux=N r^2 P_X u.

The source mass integral also has the corresponding metric weights. Thus
near a healthy condensate in a weak potential N=1+Phi_E,

    delta X=-q^2 Phi_E-u^2/2+O(Phi_E^2),
    P_X≈kappa delta X.

An attractive Einstein potential Phi_E<0 can make P_X positive. It invalidates
any claim that the flat-clock flux obstruction applies to every fully
backreacted Einstein-P(X) solution. Even a small lapse matters when P_X tends
to zero. Near the flat-clock degeneracy, neglected corrections need not be
small relative to the principal margin.

Test the controlled alternative in which the Einstein lapse is baryon dominated,
Phi_E=-G_T M_b/r, with scalar stress initially negligible. The leading flux is

    r^2 kappa(q^2G_T M_b/r-u^2/2)u=alpha M_b/(4pi).

Trying a 1/r force u=v/r yields, at large r within this expansion,

    kappa[v q^2G_T M_b-v^3/(2r)]=alpha M_b/(4pi),
    v -> alpha/(4pi kappa q^2 G_T).

The coefficient is independent of M_b, whereas MOND needs v proportional to
sqrt(M_b). This is a concrete failure of the simplest lapse rescue, not a
proof for every coupled solution. Moreover its scalar density perturbation
starts as q^2 kappa delta X~kappa q^4 G_T M_b/r, so that tail eventually
backreacts; one cannot extend the assumed baryon-dominated lapse to infinity.
A self-consistent backreacted or time-dependent repair remains open and would
bring in kappa, q, source coupling and boundary data. None are fixed by the
stationary condensate value alone.

## 6. Physical cosmology and comparison with prior work

The conformal force choice has another same-action cost. In Einstein de Sitter
with phi=q t and A=exp(alpha q t), the matter metric has proper time d tau=A dt
and scale factor a_J=A a_E. Therefore

    H_J=(H_E+alpha q)/A,
    G_T,J=A^2 G_T.

For alpha q nonzero, H_J is not constant: Einstein de Sitter vacuum stress is
not an observed constant-curvature de Sitter universe for this matter sector.
The quoted C_v is consequently an Einstein/tensor-frame diagnostic, not an
already-observed physical ratio. Extra couplings or a different physical-frame
completion need a new normalization and cosmology calculation. A strictly
shift-preserving derivative coupling does not automatically retain the same
MOND source/force dictionary.

The project overlap search covered p20's acoustic-horizon setup and p20c,
N2's static existence/FRW threshold study, the Sol61 puzzle README and its
previous derivative-kernel normalization. Those records already expose free
functions, condensate stationarity and horizon-scale insertion. This result
adds the normalized conformal source/force formula, the exact clock-required
MOND branch and hyperbolicity threshold, the independent smooth-condensate
flux-sign argument, and the explicit lapse mass-cancellation escape control.
Novelty is relative to the inspected project records, not to all literature.

Primary literature checked directly: Arkani-Hamed et al.,
[Ghost Condensation](https://arxiv.org/pdf/hep-th/0312099), retrieved v1,
sections 2.1-2.3, especially equations 2.16-2.18. It explains the vanishing
ordinary gradient term at the condensate and introduces higher derivatives
to supply k^4 dispersion. Its signature and X normalization differ; the
coefficients above were derived independently in the declared convention.
Bekenstein, [Relativistic gravitation theory for the MOND paradigm](https://arxiv.org/pdf/astro-ph/0403694),
section II's RAQUAL discussion, distinguishes the conformal physical metric
and its scalar force/lensing liabilities. Our conformal source choice is not
TeVeS and inherits none of its vector-sector propagation results. Initial
arXiv HTML fetches failed; the primary PDFs were subsequently opened and
checked. No unverified source theorem is load bearing.

## Evidence and next implication

`checks.py` verifies 16 exact/local assertions. `runs/main_a/` is the
bounded authoritative run; `runs/drop_PXX_a/` is the expected failing control.
Both version-2 manifests validate with unchanged inputs, retained logs and
actual hashes. CPU20s/process, wall30s, 1MiB logs, cooperative one-thread
numerical libraries; no memory or affinity cap. The four rational signature
cells are finite checks, while the displayed determinant and flux arguments
are the uniform proofs. No failed mathematical route was silently discarded:
exact analytic crossing, naive spacelike/timelike superposition, fixed-clock
MOND continuation, and the baryon-lapse rescue each have their stated failure.

The live constructive alternative is a fully backreacted, time-dependent
clock/galaxy boundary with explicitly specified source coupling, physical
metric, and higher-derivative completion where needed. It must first preserve
the sqrt(M_b) force normalization and scalar principal health; only then
could a dynamical selector for P(X_t), gamma and alpha be tested. Fixing their
ratio to 32pi before that calculation would insert the target.
