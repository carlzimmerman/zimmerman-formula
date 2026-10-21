# Existing gravitational relaxation: a real mixed coupling, and its remaining dictionary gap

20 October 2026. Initial assessment HEAD:
`b10ed68d6bbc90744c5aa77ae7c702c2898507c1`. Analytic route only; no scientific
run, fitted occupation coupling, old-packet edit, campaign change or Git
mutation. Exact read-source hashes are in `source_hashes.json`.

**Result.** The canonical field has no gravitational occupation coupling
for a co-located conversion at fixed total density. Allowing a *specified
spatial transfer* creates a different source and a real coupling to ordinary
orbital baryons. Eliminating a radially stable baryonic shell then produces
an exact negative occupation pair curvature, with coefficient determined by
its mass and conserved angular momentum. That coefficient can exceed the
full remainder, canonical stiffness and outer free-stock costs. It requires
no added `J` or mediator. The supported continuation, barrier proof and
finite bounds in this directory construct actual radially stable inner
profiles and prove an exact finite energy pass. This is a constructed
spatial-binding family, not a derived memory: the inherited equations do
not fix its geometry/actions, identify its microscopic site count or
supply the conversion operator, receiver and complete thermal trace.
General nonspherical/action-changing stability is also unproved.

## 1. Exact target and source conventions

The prior finite-state audit proves that, for its declared two-particle,
two-site count `(Omega_0,Omega_1,Omega_2)=(1,4,2)`, there is a bias at which
both endpoints are strict occupancy modes exactly when

    U_pair = E_2-2 E_1+E_0 < -3 theta ln 2,   theta>0.       (1)

An arbitrary term linear in occupation cancels from `U_pair`. A mechanical
energy satisfying (1) does not derive these multiplicities, a Gibbs bath,
finite transition rates or a switching time. All claims about (1) below
retain that conditional interpretation. Here `n=0,1,2` denotes the number
of mass-`m` parcels moved from an outer free orbital stock into an inner
tethered collective density mode. It is not a change of scalar source
charge `b` into daughter charge `psi`; those are distinct objects in MASTER.

Use spherical symmetry, outward positive acceleration, `K=4 pi G`,
`gamma=K L*^2/2`, `u=GT/r^2`, and the canonical branch `0<=u<a0`.
`B,T,F,N=T+F` are enclosed baryonic, tethered, free and total cold masses.
Additive rest masses and fixed baryon self-energies cancel from (1).
Whenever baryons or free stock move, their kinetic and gravitational
energies are included rather than absorbed into a binding bias.

The reciprocal source note is already an explicit two-population extension
of S2, not a derivation of S4. Restoring the canonical stiffness to that
same spherical energy gives the mechanical functional used here:

    H = K_b+K_t+K_f
        -G/2 integral (B+N)^2/r^2 dr
        +G/2 integral T^2/r^2 dr
        +integral 4 pi r^2 W_rem(GT/r^2) dr
        +(gamma/2) integral |grad P_t|^2 d^3x,             (2)
    div P_t=rho_t,   P_t=T/(4 pi r^2) rhat,
    K W_rem'(u)=R(u)=u^2/(a0-u).

The positive critical term cancels tethered Newtonian self-gravity once.
It does not cancel tether-free or tether-baryon attraction. Regular finite
profiles, suitable decay and no independent copy of the same polarization
field are assumed. In the extended source dictionary the response charge
is tethered mass, not total gravitating mass.

The separately conserved inventories of (2), before adding a conversion
operator, are baryon mass, tethered mass and free mass. A prescribed change
of `n` conserves total cold mass `2m` but is **not** a trajectory generated
by (2). It would require a reaction law. If response charge is realized as
an independent conserved gauge charge, its transfer also requires a
charge-carrying receiver; no such receiver is derived here.

## 2. The exact zero and the general Hessian test

Write `C[T]` for the last three terms of (2). In independent Eulerian
density coordinates `(B,N,T)`, the static Hessian is

    H_static'' = -G L^* L on (delta B+delta N)
                 direct_sum C'' on delta T,              (3)

where `L` is the enclosed-mass map with radial weight `r^-2`. Thus the
`N,T` and `B,T` cross blocks vanish exactly. For regular radial variations,

    delta^2 C = G integral [1+R'(u)] (delta T)^2/r^2 dr
                +gamma integral |grad delta P_t|^2 d^3x >0

for a nonzero admissible tethered variation. `1+R'(u)=(1-u/a0)^-2`.
Eliminating a stable baryonic or total-density mode while keeping `N`
independent of `T` cannot change this zero. Giving that mode a term
`-g q n` by hand would change the source dictionary.

For actual constrained source profiles `rho_i(n,q)`, the chain rule has
both the pullback of (3) and terms containing the first functional
derivative times the second profile derivative. The latter terms may be
discarded only at a true constrained stationary point. This matters for
moving material surfaces; the Eulerian zero is not a theorem that every
material-coordinate mixed derivative vanishes.

At a stationary responder `q*(n)`, write the quadratic form as

    (delta n,delta q) [ A  B^T ; B  D ] (delta n,delta q)^T.

If `D` is strictly positive on the actual conserved and
boundary-constrained response space and the branch is differentiable,

    E_eff'' = A-B^T D^-1 B.                              (4)

This subtraction is negative semidefinite but is zero when `B=0`.
For an invertible indefinite `D` the algebraic Schur identity also
holds, but it does not describe elimination of a stable responder and
its subtraction need not be negative semidefinite.
If the full Hessian is positive semidefinite, its Schur complement is
also positive semidefinite. A negative complement therefore identifies a
direction unstable when occupation is allowed to vary, not a second
stable branch by itself. For finite occupation, calculate the three
minimized energies; a local Hessian is not sufficient for (1).

Pure kinetic coefficients contribute no static mixed term at zero momenta
when their minimum kinetic energy is zero. Conserved orbital angular
momentum is different: `j^2/(2q^2)` remains in the effective radial
potential. Neither a phenomenological pressure nor the MASTER band
medium's positive oscillator representation supplies an occupation
coupling without its actual source map.

## 3. A stable existing orbital responder produces an exact attraction

The following is an explicit *spatial control* of (2), not co-located label
conversion. Take central baryon mass `M0>0`; a spherical baryonic orbital
shell of mass `M_h>0`, radius `q` and common conserved specific angular
momentum `j_h>0`; an inner tethered density of total mass `mn`, supported
inside radius `a`; and an outer free orbital shell of mass `m(2-n)` and
radius `R`. Require

    a < q < R,   n=0,1,2.                               (5)

Uniformly distributed orbit orientations make each shell spherical.
`j_h` and `j_f` below are initial orbital data, not fitted interaction
coefficients. This proves radial stability of the retained shell modes;
it does not prove stability against every nonspherical collisionless
perturbation. Central baryon self-energy is a common subtraction; a
small regular central baryon profile gives the same exterior formulas.

Newton's shell theorem and (2) give the **actual** host-shell energy

    E_h(n,q) = M_h j_h^2/(2q^2)
               -G M_h A_n/q,
    A_n=M0+mn+M_h/2.                                    (6)

The `M_h/2` counts its own Newtonian shell self-energy once. The outer
free shell contributes a constant potential inside and hence no `q`
force. Tether critical/remainder/stiffness terms do not depend on `q`
while the inner source remains interior. Consequently (6) is an exact
subsector of the counted energy, not a chosen linear mediator coupling.

Its stationary radius, Hessian and relaxed energy are

    q_n = j_h^2/(G A_n),
    D_h=partial_q^2 E_h|q_n=G M_h A_n/q_n^3>0,
    partial_n partial_q E_h=G M_h m/q_n^2,
    E_h^*(n)=-G^2 M_h A_n^2/(2j_h^2).                   (7)

The radial kinetic mass is `M_h>0`, so the retained radial mode has
positive squared frequency `G A_n/q_n^3`. At fixed `q`, (6) is linear
in `n`; eliminating `q` gives exactly

    (E_h^*)'' = -G^2 M_h m^2/j_h^2
               =-(partial_n partial_q E_h)^2/D_h,
    Delta^2 E_h^*=-G^2 M_h m^2/j_h^2.                  (8)

Thus no negative-energy responder or inverted oscillator was used.
At `q_n`, its magnitude is `Gm^2 M_h/(A_n q_n)<2Gm^2/q_n`.
There is no unlimited susceptibility obtained by arbitrarily enlarging
`M_h`. The coupling exists because the *ordinary enclosed cold mass at
the host shell changes by `m`* when one parcel moves from outside to
inside. If free and tethered parcels were co-located on the same side
of the shell, that derivative and (8) would vanish.

The bound also supplies a necessary scale test, before any numerical
choices. Since `q_0` is the largest of the three host radii,

    |Delta^2 E_h^*| < 2Gm^2/q_0 < 2Gm^2/a.              (8a)

Consequently (16) requires, in particular,
`a^3>(3/4)L*^2 q_0` and hence `a>(sqrt(3)/2)L*`.
Positive remainder, outer-stock and thermal costs make that necessary
bound stricter. A source concentrated far below the canonical stiffness
length cannot obtain this latch from the retained orbital host response.

Even dropping every positive mechanical cost, the finite-count test
requires `3theta ln2<2Gm^2/q_n`. Under the additional declared thermal
interpretation `theta=m sigma^2`, this becomes

    m > (3 ln2/2) sigma^2 q_n/G.                        (8b)

The right side is of the order of a virial mass at that radius and
dispersion. This identifies a potential macroscopic-parcel requirement,
not a microscopic particle mechanism. A collisionless velocity dispersion
does not automatically define a Gibbs temperature or the finite-state
count. The microscopic scalar-carrier benchmark mass of `1 MeV` in
MASTER is not identified with the extended occupation mass `m` here;
one cannot import it while retaining an arbitrary ordinary galactic
dispersion and claim this gravitational latch.

For the uniform-ball control used below, stiffness also gives a global
energetic ceiling independent of the freely chosen host mass and orbit:

    U_pair > Gm^2[-2/a+(3/2)L*^2/a^3]
           >= -8Gm^2/(9L*).                            (8c)

The second expression attains its minimum at `a=3L*/2`. Hence a necessary
condition for (1) in this uniform-ball control is
`theta<8Gm^2/(27 ln2 L*)`. The positive outer-stock and full-remainder
terms tighten it. This is a bound for that specified source shape, not
a shape-independent theorem by this particular argument. `BOUNDS.md`,
Section 2, separately extends the same ceiling to the shape-relaxed
fixed-action family with a common support ball by joint convexity.

## 4. Count the outer free stock rather than pinning it

The outer stock also needs support. Retain its existing orbital kinetic
energy, with fixed specific angular momentum `j_f>0` for every free
parcel. Its full energy, including all interactions with central baryons,
host, tethered cloud and itself, is

    E_f(n,R) = m(2-n) [j_f^2/(2R^2)-G C_n/R],
    C_n=M0+M_h+mn+m(2-n)/2
       =D+mn/2,   D=M0+M_h+m.                          (9)

No additional tether-free cross term is to be added: it is already
inside (9). The inner tether's ordinary self-energy is canceled by the
critical term, whatever its regular density shape. At `n<2`,

    R_n=j_f^2/(G C_n),
    partial_R^2 E_f|R_n=G m(2-n)C_n/R_n^3>0,
    E_f^*(n)=-G^2 m(2-n)(D+mn/2)^2/(2j_f^2).

At `n=2` that stock is empty; no fictitious zero-mass responder is
inverted. Direct evaluation of the three energies gives

    Delta^2 E_f^* = G^2 m^2 (D+m/4)/j_f^2 >0.           (10)

As `j_f` makes the outer orbit large this cost becomes small. If the
outer shell were instead held at a common fixed `R`, its direct
occupation curvature would be `+Gm^2/R`, not the negative self-energy
of a second separately added free halo. Equation (10) includes its
relaxation and avoids that double count.

For each fixed occupation the retained `(q,R)` Hessian is diagonal with
the positive entries above while (5) holds. The inter-shell potential
is constant inside the outer shell, so there is no omitted `q,R`
mixed radial term. At `n=2` retain only the `q` block.

## 5. Full canonical remainder and stiffness of a regular source

To expose the size of the costs without a singular thin tether shell,
use the declared extended occupation density

    rho_t(n,x)=mn h_a(x),
    h_a=3/(4 pi a^3) for |x|<a, and 0 outside,
    H_a(r)=min[(r/a)^3,1].                             (11)

`P_t` is continuous and weakly differentiable; the density jump does
not create a delta function in `grad P_t`. A thin *mass shell* would
make `P_t` jump and would have divergent canonical stiffness. For (11),
integration by parts gives

    integral |grad P_t|^2 d^3x
      =integral rho_t^2 d^3x,
    E_stiff(n)=gamma m^2 n^2/2 integral h_a^2 d^3x,
    Delta^2 E_stiff=(3/2)Gm^2 L*^2/a^3.                (12)

Both boundaries vanish in the integration by parts. A smoothly tapered
density gives a finite nearby coefficient and the same scaling; no
zero-stiffness limit has been used in the criterion below.

Choose `W_rem(0)=0`. The exact positive remainder primitive is

    W_rem(u)=a0^2/K [-ln(1-x)-x-x^2/2],   x=u/a0.

Put `epsilon=Gm/(a0 a^2)` and require `2epsilon<1`. For (11), its finite
extended-source energy has the convergent analytic series

    E_rem(n)=a0^2 a^3/G sum_(k>=3) (epsilon n)^k/k
                         [1/(k+3)+1/(2k-3)].            (13)

This is an exact integral evaluation, not a fitted local quartic.
Every term in `Delta^2 E_rem` is positive, and its leading value is

    Delta^2 E_rem=G^2 m^3/(a0 a^3)+O(epsilon^2 Gm^2/a).

An explicit bound, avoiding a truncation assumption, is

    0 < Delta^2 E_rem
        <= (6Gm^2/(5a)) [(1-2epsilon)^-2-1].             (14)

Indeed the second occupation derivative is
`Gm^2 integral R'(Gmn H_a/r^2) H_a^2/r^2 dr`,
`integral H_a^2/r^2 dr=6/(5a)`, and
`R'(u)=(1-u/a0)^-2-1`. The finite second difference is its integral
over a unit-area positive weight on `0<=n<=2`.

All the cold critical self-energy has already canceled the ordinary
inner tether self-energy. Adding the positive co-located critical
pair cost `Gm^2/a` to (12)-(14) would count it a second time in this
spatial-transfer geometry. The outer free-stock cost in (10) remains.

The complete pair curvature of this restricted mechanical control is
therefore

    U_pair = Delta^2 E_rem + (3/2)Gm^2 L*^2/a^3
             +G^2m^2(D+m/4)/j_f^2
             -G^2M_hm^2/j_h^2.                         (15)

The central baryon/inner tether interaction is linear in `n` for (11),
so it cancels from (15). A term for an inner orbital distribution would
also cancel only if its kinetic energy were linear in `n` at the same
specified mode. It has not silently been included as a stationary
support mechanism here.

For this control the exact necessary and sufficient energetic condition
for the inherited finite-state test is

    G^2M_hm^2/j_h^2 > Delta^2 E_rem
          +(3/2)Gm^2L*^2/a^3
          +G^2m^2(D+m/4)/j_f^2 +3theta ln 2.             (16)

This explicitly displays every pre-existing coupling and the thermal
cost, instead of replacing them by a free `J`.

Equivalently, define
`eta=M_h/A_0<2`, `lambda=q_0/a`, `rho=R_0/a`,
`s=L*/a`, `tau=theta a/(Gm^2)`, and
`d(epsilon)=a Delta^2 E_rem/(Gm^2)`. Then the exact energetic condition is

    eta/lambda > d(epsilon)+(3/2)s^2
                  +(1/rho)[1+m/(4D)]+3tau ln 2.         (16a)

In this expression `q_2>a` additionally requires
`lambda>1+2m/A_0`. A sufficient finite-domain inequality follows by
replacing `d(epsilon)` with
`(6/5)x(2-x)/(1-x)^2`, where `x=2epsilon<1`; this is exactly (14),
not an asymptotic estimate. This dimensionless form leaves the required
geometry, orbital actions, source mass and temperature explicit.

For a nonempty analytic parameter region, set

    M_h=2M0,  0<m/M0<=1/100,
    q_0=2a,  j_h^2=4GM0 a,
    R_0=100a,  j_f^2=100GDa,
    a>=10L*,  epsilon<=1/1000,
    0<theta<=Gm^2/(10a).                               (17)

Then `q_2=2a/(1+m/M0)>a`, all `q_n<=2a`, and all nonempty outer
stock radii exceed `99a`. The negative term of (15) is
`-Gm^2/(2a)`. Its positive terms are respectively less than
`0.005Gm^2/a`, at most `0.015Gm^2/a`, and less than
`0.01001Gm^2/a`. Hence

    U_pair < -0.46999Gm^2/a < -3theta ln 2,              (18)

using `ln 2<1`. These strict margins survive small smooth regularizations.
The choices in (17) are a constructed configuration and initial orbital
data, not a universal or observationally selected set of parameters.
None of the inspected inherited equations or memory packet supplies
the values of `a,R,j_h,j_f,M_h,theta` for a proposed actual memory site.
No owner computation or campaign rerun was used to fill them in.

For clarity, the complete retained interior Hessian at a stationary
orbital pair, with `0<n<2`, has responder block
`diag(D_h,D_f)>0`, occupation diagonal
`E_rem''+E_stiff''+Gm^2/R_n`, and the two mixed entries

    B_h=G M_h m/q_n^2,
    B_f=Gm^2(2-n)/(2R_n^2).

Its exact Schur complement is

    E_rem''+E_stiff''
      +(Gm^2/R_n)[1-m(2-n)/(4C_n)]
      -G^2 M_hm^2/j_h^2.                               (19a)

In (17) this is negative throughout `0<n<2`: (14)'s same supremum
bounds `E_rem''`, the stiffness bound is constant, and the free
curvature is less than `G^2m^2(D+m)/j_f^2<0.01004Gm^2/a`.
Thus the full retained interior Hessian has one negative direction;
the responders alone do not turn that interior state into a stable
equilibrium. For a continuous bounded occupation `0<=n<=2`, a linear
bias between the two endpoint derivatives of this strictly concave
relaxed energy makes both endpoints one-sided energy minima. At each
endpoint the allowed orbital modes are still locally stable; at the
empty-free-stock endpoint the `R` variable is absent. This statement
concerns the retained coordinates only. Finite discrete occupation
uses the exact Gibbs test (1). The supported continuation below replaces
the imposed inner shape; general phase-space stability remains unproved.

## 6. Why this is not yet an actual memory mechanism

The shell responder is physically ordinary and radially stable, and
its nonzero source derivative follows from conserved spatial transfer.
The outstanding problem is the *occupation sector*, not a missing
sign in its gravitational Schur term:

1. Density (11) is an imposed extended control. With a central baryon
   and no inner kinetic stress it is generally not a canonical cold
   rest profile. Its mechanical gradient need not vanish. Consequently
   (18) is not a construction of three fully relaxed states of (2).
   A finite stationary tether profile and its actual conserved actions,
   or another already specified support, must replace (11). Its minimized
   three energies must be evaluated again; the uniform-source result
   cannot be transferred by assertion.
   This narrower mechanical obligation is completed in
   `SUPPORTED_CONTINUATION.md`, `BARRIER_PROOF.md` and `BOUNDS.md`:
   fixed circular actions give a genuine inner minimum, shifted cumulative
   barriers prove exact support without a wall, and finite variational
   bounds prove the three-energy criterion for those actual minima.
2. A radially stable host shell does not prove stability of every
   nonspherical collisionless mode or of the joint source/host system.
   If the desired model requires full stability, those additional
   response directions must enter `D` and be checked before elimination.
   No Jeans-unstable direction has been inverted in (7)-(10), but no
   whole-halo stability certificate follows from those two positive
   radial entries.
3. Tether/free conversion is absent from the conservative kinetic
   equations used here. Neither a spatial transition operator, positive
   rates, heat receiver nor response-charge transfer law is derived.
   The `(1,4,2)` count is not produced by spherical density mechanics.
4. Integrating orbital coordinates at positive temperature gives a
   constrained free energy, not just their minimum energies. Its
   occupation-dependent orbital density of states must be counted.
   In the low-temperature limit, finite regular responder fluctuations
   give corrections of order `theta ln theta` and `theta` after a stated
   measure; that measure and its behavior at empty stock have not been
   specified here. Equation (18) is an energy test conditional on the
   prior finite-state reference, not a completed thermal trace.
5. Any real free stock still changes the reciprocal canonical cold-rest
   source from `B` to `B+F`, as SOURCE_RESPONSE derives. This gravitational
   attraction does not recover the baryon-only rest law, the canonical
   abundance or empirical S4/O4 predictions.

Thus the primary physical verdict is **incomplete, with a concrete
existing-force interaction and a remaining source-to-occupation,
transition/receiver and thermal-trace gap**. The exact narrower
mathematical statement proved is that ordinary orbital response can
yield the required negative finite energy curvature in a constructed,
radially stable conserved spatial-binding family of the reciprocal
canonical energy, including nonzero stiffness. The supported files
establish fixed-action radial stationarity and support; they do not
derive S4. A universal claim that existing gravity can never yield the
needed sign would be too strong. A claim that this calculation derives
an actual latch would also be too strong.

## 7. Pressure response is a second route only after a closure is specified

For comparison, a single mass-conserving spatial mode with occupation
amplitude `t`, total-density amplitude `z`, and a declared local kinetic
free energy `f_t(t)+f_f(z-t)` has quadratic coefficients

    A=c+p_t+p_f,   B=-p_f,   D=p_f-g,
    c=C_field''>0,  p_i=f_i''>0,  g>0,                  (19)

where `-g z^2/2` is that mode's existing Newtonian gravity. These are
projections with compatible units, not an asserted universal local
gravity kernel. If `D>0`,

    A_eff=c+p_t - p_f g/(p_f-g).                        (20)

It is negative exactly when
`g>p_f(c+p_t)/(p_f+c+p_t)`, together with `g<p_f` for the responder.
The full determinant is then negative. This is a coupled occupation/
compression instability, not proof of a stable two-state memory.
Approaching `g=p_f` and retaining a large inverse response while dropping
its support is a Jeans singularity, not a justified passive elimination.

For an actual classical ideal gas the curvatures would be fixed by its
kinetic trace and densities. Canonical S3 is collisionless and supplies
no general local barotropic free energy or isothermal bath. MASTER's
carrier pressure bound is an inequality in a different sector, not the
closure `p_i` in (19). Therefore (19)-(20) are a diagnostic conditional
identity; selecting `p_i` to force (1) would introduce the missing physics
under another name. The explicit orbital route in Sections 3-5 does not
use this unspecified pressure closure.

## 8. Provenance, comparison and verification

Closest checked prior: `memory/RESULT.md` and its
`INDEPENDENT_AUDIT.md` establish fixed-position convexity and (1), while
`reciprocity/SOURCE_RESPONSE.md` supplies the full rational-remainder
two-population energy but omits stiffness. This note changes the actual
source variation, restores the recorded canonical stiffness, and retains
the kinetic energy that stabilizes the responding baryonic/free orbital
shells. It does not repeat a co-located fixed-`N` no-go as a universal
result.

MASTER's scalar carrier has conserved
`Q=integral(psi^dagger psi+2b^dagger b)` and a positive regulated excess
Hamiltonian. Its force-sector bands have their own positive homogeneous
response. MASTER explicitly leaves `S_bridge` unspecified. Neither object
identifies the spatial tether/free occupation above, and their energies
were not added to (2) as if that bridge already existed. In particular
no extra scalar/fermion-mediated attraction is claimed here.

Verification is analytic: differentiate (6) twice; substitute (7) into
(6); evaluate (9) at its stationary radius and take its three-state second
difference; integrate the radial stiffness by parts; integrate each
positive term of the convergent remainder series; use the positive
second-derivative integral for (14). No external theorem, numerical
sampling, symbolic package, fit or simulation is load bearing. Only
read-only source inspection and byte hashing were executed.

Proofreading/self-review scope is this new note only. Mathematical signs,
dimensions, the empty-free-stock boundary, mass conservation and
critical/cross-energy double counting were rechecked. This is author
self-review within a separately delegated lane, not an independent blind
audit or formal stability certificate.
