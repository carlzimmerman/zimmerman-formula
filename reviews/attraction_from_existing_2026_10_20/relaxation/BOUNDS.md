# Exact finite supported pass and a stiffness-limited gravitational ceiling

20 October 2026. Same pinned base and equations as `RESULT.md`.
`SUPPORTED_CONTINUATION.md` derives the fixed-rank circular-action inner
energy and its variational minimum. `BARRIER_PROOF.md` removes the support
restriction for all sufficiently small masses. This note proves an
**exact finite energy inequality** for those actual radial minima; no
asymptotic sign is substituted for the finite-state test.

## 1. A finite upper bound after minimizing the inner shape

Choose a smooth normalized tracer density `h0` supported in
`a/2<r<a`, with cumulative `H0` and
`I4=integral h0^2 d^3x<1/(pi a^3)`. Its conserved rank actions are
`j(s)^2=GM0 r0(s)`. Let `A0` be its tracer energy and
`S0=(gamma/2)I4`. The exact inner minimum at mass `z` is

    E_inner(z)=min_H [z A[H]+z^2 S[H]+V_z[H]].           (1)

Since `A>=A0` and the two field terms are nonnegative,
`E_inner(m)>=mA0`. Using `H0` as a trial state at `2m` gives
`E_inner(2m)<=2mA0+4m^2S0+V_(2m)[H0]`. With `E_inner(0)=0`,

    Delta^2 E_inner <=4m^2S0+V_(2m)[H0].                (2)

This direction is important: separately bounding both nonzero energies
above would not control their second difference.

Put `epsilon=Gm/(a0a^2)` and `x=8epsilon<1`. Because `H0=0` below
`a/2`, throughout its field profile
`G(2m)H0/(a0r^2)<=x`. The exact remainder series implies

    W_rem(v)<=v^3/[3K a0(1-x)]   for 0<=v/a0<=x.

Moreover `integral H0^3/r^4 dr<=8/(3a^3)`. Hence

    V_(2m)[H0] <=64G^2m^3/[9a0a^3(1-8epsilon)],
    4m^2S0 <4Gm^2L*^2/a^3.                            (3)

These bounds include the full rational remainder and canonical stiffness.

Use the main note's exact relaxed host and outer-stock energies with

    M_h=2M0,  j_h^2=4GM0a,
    j_f^2=100GDa,   D=M0+M_h+m.

They contribute respectively
`-Gm^2/(2a)` and `(Gm^2/(100a))[1+m/(4D)]` to the finite pair curvature.
Consequently the exact supported finite inequality is

    U_pair/(Gm^2/a)
       < -1/2 +4(L*/a)^2
          +64epsilon/[9(1-8epsilon)]
          +(1/100)[1+m/(4D)].                          (4)

For example impose the simultaneous state conditions

    a>=10L*,   epsilon<=1/1000,   m/M0<=1/100,
    0<theta<=Gm^2/(10a),

and the explicit barrier smallness condition (2) of `BARRIER_PROOF.md`
at `z=2m`, with `l=a/4`, `u=7a/4`, `e=a/8`. Its left side increases
with `z` on the chosen branch, so the condition holds for every
`0<z<=2m`. These restrictions have a nonempty region: keep the inner
geometry, rank actions, host action and masses `M0,M_h` fixed, choose `m`
sufficiently small, and set `j_f` by the displayed finite configuration
with its actual `D=M0+M_h+m`. All three occupation sectors then use
that same `j_f` and the indicated positive temperature. This differs
from the continuation's asymptotic example, which fixes `j_f` at its
`m=0` value; the distinction affects only the stated finite coefficient,
not the sign or the common-action requirement across occupation sectors.

The positive terms of (4) are at most `0.04`, less than `0.0072`, and
less than `0.01001`. Thus

    U_pair < -0.44279Gm^2/a
           < -0.442Gm^2/a
           < -3theta ln2.                             (5)

The last inequality already follows from `ln2<1`. These are strict
finite inequalities, not a series truncation or sampled parameter test.

The barriers give inner support `r<=a+e=9a/8`, while
`q_2=2a/(1+m/M0)>1.98a` and every nonempty free radius exceeds `99a`.
The supports are therefore actually separated. At fixed occupation,
the inner shape is the unique global rank-action radial energy minimum.
The host/free radial Hessians are positive. Their mixed shape blocks
vanish because their potential is constant over the inner support.
This supplies stable retained radial mechanical states at both occupied
endpoints. It supplies no stability theorem for nonspherical modes,
shell crossing or redistribution of the conserved actions.

## 2. An exact lower bound allowing the inner shape to relax

The uniform-ball stiffness bound can be extended to the actual supported
fixed-action family. Suppose all the inner minima for `0<=z<=2m` are
supported in a common ball of radius `a_s`; the barriers supply
`a_s=a+e`. Set `T=zH` and `rho=T'/(4 pi r^2)`. The inner functional is

    integral [z J(T/z)/r^3-GM0 T/r^2] dr
      +(gamma/2) integral rho^2 d^3x +V[T].              (6)

The perspective `z J(T/z)` is jointly convex in `(z,T)` because `J`
is convex. It extends at `(z,T)=(0,0)` by zero. The saturation domain
and the constraints `T>=0`, `T'>=0`, and `T=z` outside `a_s` are jointly
convex. Write `V_ball=4 pi a_s^3/3`. Since `integral rho=z`,

    (gamma/2) integral rho^2 d^3x -gamma z^2/(2V_ball)
       =(gamma/2) integral_(ball) (rho-z/V_ball)^2 d^3x. (7)

The right side is jointly convex in `rho,z`; so are the remaining terms
of (6). Minimization over the jointly convex density constraints shows

    E_inner(z)-gamma z^2/(2V_ball) is convex.

No derivative of the minimized branch is needed. Its exact finite
curvature therefore obeys

    Delta^2 E_inner >=gamma m^2/V_ball
                     =(3/2)Gm^2 L*^2/a_s^3.            (8)

This bound retains orbital kinetic energy, central binding, the rational
remainder and shape relaxation. A subtraction of a linear occupation
energy does not affect it.

The host curvature has magnitude
`Gm^2 M_h/(A_n q_n)<2Gm^2/q_n`, and the outer-stock curvature is
positive. If `q_n>a_s`, (8) consequently gives

    U_pair >Gm^2[-2/a_s+(3/2)L*^2/a_s^3]
            >=-8Gm^2/(9L*).                            (9)

The scalar expression reaches its minimum at `a_s=3L*/2`. A necessary
thermal condition for the inherited `(1,4,2)` finite-state criterion is
therefore

    theta <8Gm^2/(27 ln2 L*).                           (10)

Under the additional declared interpretation `theta=m sigma^2`, this
also requires `m>(27 ln2/8) sigma^2 L*/G`. Independently, the local
host bound gives `m>(3ln2/2) sigma^2 q_n/G`. A collisionless dispersion
does not automatically define this temperature or a Gibbs measure.
These bounds forbid arbitrarily increasing the gravitational pair
attraction by tuning host mass while retaining microscopic occupation
mass and a finite ordinary dispersion. The collective parcel mass here
is not identified with MASTER's scalar daughter benchmark mass.

## 3. Exact result and remaining physical gap

Existing orbital kinetic energy, ordinary gravity, the canonical critical
cancellation, full remainder and nonzero canonical stiffness admit a
constructed, radially supported spatial-binding family satisfying the
finite *energy* threshold (5), with no added attractive coupling.
The geometric sizes, action functions, parcel mass and temperature are
state inputs, not values derived from the inherited candidate.

The conversion between the inner and outer action families is absent
from the conservative equations. The `(1,4,2)` multiplicity, microscopic
site inventory, thermal trace of fluctuating orbital coordinates,
response-charge/angular-momentum receiver and positive transition
operator remain unconstructed. No S4 memory, permanent untethering,
switching lifetime, baryon-only rest law or observational closure is
proved. General nonspherical/action-changing stability remains open.

All bounds are analytic; no scientific program or owner computation was
run. This is a checked delegated derivation, not blind external review.
