# Conserved circular actions support the inner profile: exact radial variational continuation

20 October 2026. Same pinned base and source inventory as `RESULT.md`.
This continues its imposed-source calculation using the existing kinetic
energy, rather than adding a pressure law, a pinning potential or `J`.
The radial variational statement and small-mass energy expansion below
are proved. `BARRIER_PROOF.md` removes the annulus support restriction
and establishes an isolated global radial minimum for sufficiently small
mass. `BOUNDS.md` gives an exact finite energy pass and a stiffness ceiling.
No singular implicit function theorem is assumed.

## 1. Conserved orbital data and an exact convex functional

Let `z>0` be total inner tethered mass. Label noncrossing circular shells
by normalized enclosed-mass rank `s in [0,1]`. Give each shell a fixed
specific angular momentum `j(s)>0`, with `j(s)^2` strictly increasing.
The total conserved angular momentum data are the function `j(s)` and an
isotropic distribution of orbit orientations. They are state data, not
a new interaction coefficient or an inherited S4 transition rule.

Write `H(r)=T(r)/z`, nondecreasing from zero to one, and
`J(s)=integral_0^s j(v)^2 dv`. Rank-preserving rearrangements preserve
each circular shell's angular momentum. Their orbital kinetic energy is

    K_t=z integral_0^1 j(s)^2/[2r(s)^2] ds
       =z integral_0^infinity J(H(r))/r^3 dr.             (1)

The integration by parts includes the outer tail where `H=1`; dropping
that tail changes the energy. The central baryonic potential energy is
`-GM0 z integral H/r^2 dr`. Tethered Newtonian self-energy cancels its
critical self-energy exactly as in the main note. Hence the remaining
inner functional is exactly

    E_z[H]=z A[H]+z^2 S[H]+V_z[H],
    A[H]=integral [J(H)/r^3-GM0 H/r^2] dr,
    S[H]=gamma/(8 pi) integral H'(r)^2/r^2 dr,
    V_z[H]=integral 4 pi r^2 W_rem(Gz H/r^2) dr.          (2)

This is ordinary positive angular kinetic energy plus the existing
canonical field terms. In particular `S=(gamma/2)integral h_H^2 d^3x`,
where `h_H=H'/(4 pi r^2)`.

At fixed `z`, in a regular region with `0<H<1`, the radial Euler equation is

    j(H)^2-GM0 r+r^3 R(GzH/r^2)
       -gamma z/(4 pi) [rH''-2H']=0.                    (3)

This is the circular-force condition
`j^2/r^3-GM0/r^2+R- gamma partial_r rho_t=0`.
It displays the actual centrifugal support and the field/stiffness
reaction. There is no imposed uniform density in (3).

For radial variations preserving the rank actions and endpoint masses,

    delta^2 E_z
       =z integral j^2'(H) (delta H)^2/r^3 dr
        +gamma z^2/(4 pi) integral (delta H')^2/r^2 dr
        +Gz^2 integral R'(GzH/r^2)(delta H)^2/r^2 dr.      (4)

Every displayed term is nonnegative; the first is strictly positive on
a nonzero interior variation when `j^2` is strictly increasing. At the
obstacles `H=0,1`, use the corresponding one-sided convex energy
inequality instead of inverting a nonexistent unconstrained mode.
This is positive radial shape energy, not a Jeans-unstable responder.
It is not a proof of nonspherical Vlasov stability or of stability when
the actions themselves can be redistributed.

## 2. Choose a genuine tracer equilibrium, not a desired occupation energy

Choose any smooth normalized radial density `h0` compactly supported in
`a/2<r<a`, positive in the interior. Let `H0` be its cumulative and `r0(s)`
its quantile. Set the conserved action distribution to

    j(s)^2=GM0 r0(s).                                  (5)

For vanishing cold self-interaction this is the actual circular-orbit
relation. Pointwise minimization of `A` gives exactly

    j(H0(r))^2=GM0 r

on its occupied annulus, with `H0=0` below and `H0=1` above. Thus `H0`
is the unique minimizer of `A` over normalized monotone cumulatives.
Its orbital energy is
`A0=-GM0 integral h0(x)/(2|x|) d^3x`.

For example, smooth tapering of the uniform annulus density can be
chosen so that

    integral h0^2 d^3x < 1/(pi a^3).                   (6)

The uniform annulus itself has squared norm `6/(7 pi a^3)`;
approximating it in `L2` by normalized smooth positive densities proves
the strict room in (6). This choice fixes state geometry and circular
actions. It is not an independently selected prediction of a memory site.

## 3. A rigorous variational sandwich on a compact radial component

Fix an enlarged annulus `I=[l,u]` with `l<a/2<a<u`, for example
`l=a/4,u=7a/4`. Let the admissible set be `H in H1(I)` with
`0<=H<=1`, `H'>=0`, `H(l)=0,H(u)=1`, extended by zero/one outside `I`.
The baseline `H0` is constant on neighborhoods of both endpoints.
For `Gz/l^2<a0`, the saturation branch is uniformly admissible and
`0<=V_z[H]<=C z^3` on this set, with the outer tail counted.

The set is weakly closed. `z^2 S` controls its `H1` seminorm, the fixed
endpoints control its norm, `A` and `V_z` are convex continuous integral
functionals, and lower semicontinuity gives an attained minimum `H_z`.
Strict convexity of `J` gives uniqueness. Thus for each fixed `z>0`
there is a genuine radially supported energy minimum **within this
component**, with the positive shape form (4) wherever the active
constraints permit two-sided variations.

Write `S0=S[H0]`. The trial state and nonnegative field terms give

    z A0+z^2 S[H_z]
       <= E_z[H_z]
       <= z A0+z^2 S0+O(z^3).                          (7)

Consequently `A[H_z]-A0=O(z)` and `S[H_z]<=S0+O(z)`.
On `I`, strict monotonicity of `j^2` can be bounded below by a positive
constant because `H0'` is bounded above. More explicitly
`j^2'(s)=GM0/H0'(r0(s))>=GM0/max H0'>0` on the interior,
with the natural limiting inequality at its endpoints. The pointwise
convexity gap for `A` then controls a positive multiple of
`norm(H_z-H0)_L2(I)^2`. Hence `H_z -> H0` in `L2`.

The bound on `S` gives weak `H1` compactness. Its only possible limit is
`H0`, and lower semicontinuity yields
`liminf S[H_z]>=S0`. Together with (7), this proves `S[H_z]->S0`.
Substituting that convergence back into (7) gives the sharper result

    A[H_z]-A0=o(z),
    E_inner(z)=z A0+z^2 S0+o(z^2).                     (8)

No differentiability in `z` or termwise perturbation of the minimizer
was required. In particular this avoids an unjustified ordinary IFT:
the stiffness introduces a higher radial derivative with coefficient
`z`, so applying an IFT at `z=0` in the same function space would require
an additional argument.

For fixed `n=0,1,2` and mass unit `m ->0`, use the *same* action function
`j(s)` for each occupied stock and define `E_inner(0)=0`. Equation (8)
implies the finite, bias-independent curvature

    Delta^2 E_inner
       =2m^2 S0+o(m^2)
       =gamma m^2 integral h0^2 d^3x+o(m^2).            (9)

The full rational remainder is included in the `o(m^2)`, not discarded
from the energy. Its trial contribution is `O(m^3)`; the shape
relaxation is controlled by (7)-(8).

## 4. Combine with the already counted orbital responder

If these inner stationary profiles remain interior to the baryonic
shell throughout the occupation branch, the shell potential is constant
throughout the inner stock. It adds exactly `-GM_h z/q` to the inner
energy and changes none of (3)-(4) or the minimizer. The main note's
host/free-shell energies therefore give

    U_pair=m^2 [ gamma integral h0^2 d^3x
                +G^2(M0+M_h)/j_f^2
                -G^2 M_h/j_h^2 ]+o(m^2).              (10)

The expansion of the free shell is from its exact finite difference
`G^2m^2(D+m/4)/j_f^2`, `D=M0+M_h+m`. Thus define the coefficient fixed
by the source state and orbital actions,

    kappa_orb=G^2 M_h/j_h^2
               -G^2(M0+M_h)/j_f^2
               -gamma integral h0^2 d^3x.              (11)

This `kappa_orb` is not the canonical cosmological normalization `kappa`.
If `kappa_orb>0`, then for sufficiently small positive `m`,
`U_pair<0`. If also `theta=tau m^2` with
`3tau ln2<kappa_orb`, the inherited finite-state inequality holds for
sufficiently small `m`. Temperature scaling here specifies an allowed
family of states; no inherited physical receiver fixes it.
In particular this limit makes the conditional thermal dispersion
`sigma^2=theta/m=tau m` tend to zero. It supplies no microscopic
finite-dispersion escape from the host bound in `RESULT.md`, (8b).

There is an explicit nonempty geometric range: choose
`M_h=2M0`, `q0=2a`, `R0=100a`, set the orbital actions to those circular
radii at `m=0`, and use (6). Then

    G^2 M_h/j_h^2=G/(2a),
    G^2(M0+M_h)/j_f^2=G/(100a),
    gamma integral h0^2 < 2G L*^2/a^3.

For `a>=10L*`, (11) is greater than `0.47G/a`.
This is a supported-profile asymptotic coefficient with actual angular
kinetic energy. The barriers prove the required support separation for
sufficiently small masses; the finite bound in `BOUNDS.md` then replaces
an asymptotic sign with an exact three-energy inequality. The common
action family is state data, not a universal interaction or a derived
conversion channel.

## 5. Exact boundary result and remaining physical obligations

Mere `L2` convergence to a compactly supported tracer profile would not
prove exact support separation. `BARRIER_PROOF.md` supplies the additional
argument: the shifted cumulatives `H0(r-e)` and `H0(r+e)` are subsolution
and supersolution under an explicit small-mass inequality. Weak
positive-part comparison places the actual minimizer between them.
It is therefore exactly zero below `a/2-e` and one above `a+e`.
The constant extension has no endpoint stiffness reaction, satisfies
the exterior obstacle signs, and is the unique global radial minimum.

The complete status is:

- Positive radial shape energy and an isolated stable minimum with
  conserved rank actions: proved by (2)-(8) and `BARRIER_PROOF.md`.
- Small-mass finite occupation curvature with all canonical terms:
  proved by (9)-(11) and exact support separation; `BOUNDS.md` supplies
  the finite sufficient inequality and exact necessary ceiling.
- Removal of the component's support restriction without a reaction:
  proved by shifted cumulative barriers and global convexity.
- Stability under general nonspherical, shell-crossing or action-changing
  perturbations: not established.
- One finite microscopic site with the `(1,4,2)` trace, energy-conserving
  S4 conversion and finite positive rates/receiver: not established.

The spatially distinct angular-action families are ordinary orbital
binding states of a conservative model. A path that converts between
them may have to transfer angular momentum and response charge. Giving
each occupation the same normalized `j(s)` distribution does not derive
that path or its conservation ledger. No lifetime, universal retained
fraction, observational pass or S4/O4 closure follows from (10).

All derivations are analytic; no scientific program was run. This is
self-review, with proofreading restricted to this new continuation.
