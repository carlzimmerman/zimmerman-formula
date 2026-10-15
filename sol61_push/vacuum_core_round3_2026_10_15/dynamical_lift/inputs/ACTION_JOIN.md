# S2–current-action join: an exact static reduction, with dynamical obligations remaining

2026-10-15. Source revision `f111b2d8d6f28387881bf2582d4e29e35f14e4b7`.
The raw frozen action, AG4 implementation/results and current-action definitions
are pinned in `inputs/`; hashes and revision comparison are in
`inputs/source_manifest.json`. This is a fresh local derivation from those
artifacts, by the same model family; it is not external peer review.

**Normalized claim and primary verdict: correct only after a stated restriction.**
The gamma-zero S2 functional has the canonical spherical, positive, aligned
static branch claimed by AG4. It is exactly a static Legendre reduction of the
specified critical-charge dust model when its charge density equals its rest
mass density times zeta, the background density is zero or treated separately,
and boundary variations conserve total mass. This identity does not transfer a
carrier kinetic term, magnetic response, covariant frame, finite-density
positivity constraint or the nonzero S2 stiffness to the other action.
Consequently AG4 supplies a useful static bridge, but does not by itself supply
our dynamical central body or our material-to-vacuum matching.

## 1. Static variation, without assuming the desired interpolation

Write kappa_G=4 pi G, zeta=sqrt(kappa_G), u=kappa_G |P| and
A=grad Phi-kappa_G P. The source action is

    L_S2 = -|A|^2/(2 kappa_G) - rho_b Phi - W(u)
           - gamma |grad P|^2/2,
    kappa_G W'(u)=u^2/(a0-u),  0 <= u < a0.

Here P is a spatial polarization field; it is not pressure or a number current.
Integration by parts in the independent Phi and P variations gives

    div A = kappa_G rho_b,
    A - [u^2/(a0-u)] P_hat + gamma laplacian P = 0.

For a radial vector P(r) r_hat, its vector Laplacian is
`P''+2P'/r-2P/r^2`; the last term cannot be replaced by a scalar Laplacian.
At gamma=0, on the exterior positive branch of a point baryon source,
A=gb r_hat, gb=G Mb/r^2, and P is parallel to A. Hence

    gb = u^2/(a0-u),
    g = gb+u,
    gb = g^2/(g+a0).

The positive root is unique because u^2/(a0-u) increases strictly from zero to
infinity on (0,a0). This does not prove uniqueness of a general nonspherical
solution, or identify the finite-gamma rest state with the gamma-zero profile.
The density inferred on this radial branch is positive, but that property
comes from this solution; the S2 field domain does not enforce it in general.

## 2. Exact constitutive dictionary and the static reduction

For the reciprocal current model use

    D0=a0/zeta,
    Le(E)=D0 E-D0^2 log(1+E/D0),
    D=Le'(E)=E/(1+E/D0),
    H(D)=D E-Le(E)=D0^2[-x-log(1-x)],  x=D/D0.

The exact identification on the positive, purely electric branch is

    u=zeta D,     P_vector=D_vector/zeta,
    W(u)=H(u/zeta)-u^2/(2 kappa_G),
    kappa_G W'(u)=zeta(E-D)=u^2/(a0-u).

Constants in W are chosen so W(0)=0. Expanding S2 at gamma=0 therefore gives

    L_S2 = -|grad Phi|^2/(2 kappa_G) - rho_b Phi
           + grad Phi . D_vector/zeta - H(|D_vector|).

If Gauss counts actual particles of critical charge/mass ratio,
`div D_vector=zeta rho_c`, the mixed term integrates to
`-Phi rho_c` plus a boundary term. The resulting functional is the Newtonian
static gravitational action sourced by rho_b+rho_c and the negative electric
Hamiltonian. This is the precise common static sector. Rest-mass energy is a
constant only for fixed total rest mass; its variation cannot simply be
silenced if the admissible variations change the inventory. A nonzero reference
rho_bar in `div P=rho_c-rho_bar` requires an explicit background/source
convention and adds its corresponding gravitational term.

In a static critical-charge dust interpretation, the charged particle force is

    a_r = -gb-u+zeta E = -gb+u^2/(a0-u).

It balances at the same radial algebraic branch. Neutral baryons respond to the
metric acceleration gb+u, not to the dark electric field. In the multicurrent
model, in contrast,

    div D = sum q_a n_a,
    g_c = G sum M_a/r^2,
    u_Q = G sum [(q_a/m_a)/zeta] M_a/r^2.

Only a common critical ratio and no additional massive neutral stock make
`g_c=u_Q` an identity. A neutral supporting atmosphere changes the gravitational
source, so it cannot be inserted into the canonical reduction without solving
the altered equilibrium. Field energy and pressure also gravitate beyond this
leading Newtonian rest-mass comparison.

| Object | Frozen S2 / AG4 | Reciprocal current model | Required restriction |
|---|---|---|---|
| Static field | P and Phi | D(E) and metric potential | P=D/zeta, gamma=0 |
| Constitutive energy | W(u) | H(D), Le(E) | W=H-D^2/2 |
| Positive matter | S3 asserts div P=rho-rho_bar | Timelike counted currents with n_a>0 | Additional domain/constraint; not supplied by W |
| Source | div(grad Phi-kappa_G P)=kappa_G rho_b | Metric stress plus charge Gauss law | Equal critical charge/mass and declared background |
| Carrier motion | S3 declares P_dot=-j | Varied J_a, Clebsch variables and epsilon_a(n_a) | Kinetic/flow dynamics must be retained or added |
| Stiffness | gamma | No spatial gradient of D in Le-beta B^2/2 | Extra derivative term and fresh mode/interface analysis |
| Frame/vacuum | Spatial static functional | U built from nonzero material current | No vacuum U or joining law follows from the static identity |

## 3. The actual missing dynamics and density constraint

The frozen S2 expression contains no time derivative of P or Phi. Its Hessian
with respect to P_dot is identically zero. Declaring the continuity identities
in S3 is not a variational derivation of the carrier's acceleration. For a
nonrelativistic dust current with rho_c>0 and j=-P_dot, the missing ordinary
kinetic term alone would be

    L_kin = |j|^2/(2 rho_c)
          = |P_dot|^2/[2(rho_bar+div P)].

Its velocity Hessian is I/rho_c, unlike zero for S2. A magnetic response and the
current-frame boost terms of the reciprocal action are further differences.
Adding either sign of a quadratic time-derivative term leaves the static
functional unchanged while changing kinetic positivity and the wave problem;
static agreement cannot decide those issues. This observation does not assert
that all possible dynamical lifts are unhealthy; it identifies the missing
choice.

Nor does the smooth condition `kappa_G |P|<a0` ensure positive rest density.
For example, on a small ball take `P(x)=-alpha x`, with alpha>0 and the radius
chosen so kappa_G alpha |x|<a0. Then div P=-3 alpha<0, although W is defined.
One may smoothly cut off this field outside the ball without changing the
interior witness. This is a counterexample to automatic positivity on the
variational field domain, not a counterexample to the positive radial on-shell
branch. A physical timelike current with n>0 excludes it by construction.

For nonzero stiffness the exact dictionary adds

    -gamma |grad P|^2/2 = -(L*^2/4) |grad D|^2.

That term is absent from the derivative-free reciprocal constitutive action.
If D is eliminated in favour of derivatives of the gauge potential, it changes
the derivative structure; if D is kept independent, constraints and its kinetic
completion must be supplied. Neither the previous local characteristic proof
nor the present static reduction certifies that completion.

## 4. A corrected, exact stiffness residual bound

AG4 evaluates the finite-gamma residual on the gamma-zero point-source profile;
it does not solve the finite-gamma field equations. Put y=r/rM>0,
ell=L*/rM, s=sqrt(1+4y^2), and f=u/a0=2/(1+s). Direct differentiation of the
radial vector profile gives the exact ratio

    R(y)=|gamma laplacian P|/[u^2/(a0-u)]
        =ell^2 [2/s-1/s^3].

Its limits and global maximum are

    R(0+)=ell^2,
    R(y) ~ ell^2/y as y -> infinity,
    max R=(4 sqrt(6)/9) ell^2,
    y_at_max=1/(2 sqrt(2)).

The derivative with respect to s is ell^2(3-2s^2)/s^4, proving the maximum and
the decreasing outer branch. Thus the ratio is finite as y tends to zero on
this singular point-source gamma-zero profile; it does not diverge there.
The ratio alone neither validates that profile at its origin nor proves that a
small residual yields a proportionally close finite-gamma solution.

This exposes an internal reporting error in the landed AG4 handoff/stdout:

- The raw JSON records 0.09636363652017307 (9.636%) at the ell=1 corner,
  whereas the prose says at most 1.09% in every corner.
- Exactly at y=10 and ell=1, R=2/sqrt(401)-1/(401 sqrt(401)), about 9.975%.
  Monotonicity shows the supremum for all y>=10 is this endpoint value.
- For ell=1 the outer 1% crossing lies between 99.99 rM and 100 rM. The
  original grid ends at 10^1.7 rM, about 50.12 rM. Its NaN is absence of an
  observed crossing, and cannot imply no intrusion into the inner annulus.
- For ell=0.1 the exact global maximum is about 1.08866%, so its 1% gate
  remains failed. For the floor L*=5.75pc, rM=1kpc the maximum is about
  0.0035994%; that separate small-stiffness statement is supported.

The original G4=false, gate_pass=false, source stdout and raw JSON are preserved
unchanged. No new passing threshold, canonical law change or data rescore is
introduced. The exact formula repairs the interpretation of the existing
residual check; it does not repair the failed gate.

## 5. Dependency graph, audit obligations and finish-line consequence

The local dependency chain is
`Le -> D -> H -> W identity -> gamma-zero static functional -> aligned radial
branch`. The hypotheses `critical charge/mass`, `physical nonnegative density`,
`fixed inventory/boundary term`, `negligible field stress at Newtonian order`,
and `gamma=0` enter explicitly. Current dynamics, neutral inventory and vacuum
frame behaviour are separate leaves; no algebraic identity supplies them.

| Obligation | Status | Evidence |
|---|---|---|
| Static first variations and radial vector Laplacian | Passed | Derivation above; exact symbolic reconstruction |
| Positive aligned radial root and canonical identity | Passed with restriction | Domain 0<u<a0, gamma=0, point-source exterior |
| Le/H/W identification and static source term | Passed with restriction | Legendre identities; declared Gauss and boundary hypotheses |
| Positive current encoded by W | Failed as an implication | Explicit negative-divergence admissible-field witness |
| Carrier acceleration or kinetic positivity derived by AG4 | Not addressed by static action | Zero P_dot Hessian versus I/rho_c required for dust |
| Nonzero stiffness transferred to reciprocal modes | Not addressed | Missing -(L*^2/4)|grad D|^2 term |
| G4 frozen gate | Failed, retained | Original JSON; exact ratio and corrected corner interpretation |
| Dynamical core and material/vacuum matching | Open | Static identity supplies neither missing equation set |

The strongest safe advance is an exact reduction showing that the two proposals
share their specified static critical-charge dust sector. This removes a
possible constitutive mismatch without merging their dynamical claims. The next
cheap check is to write a counted, positive-density dynamical carrier action
with the chosen stiffness and boundary conditions, then vary that exact action.
Its finite-frequency stability and vacuum conditions must be derived before
using AG4 to replace a fixed central source in the neutral-supported model.
No observational gate, S4 conversion postulate, microscopic identification,
parameter derivation or relativistic lensing prediction is closed here.
