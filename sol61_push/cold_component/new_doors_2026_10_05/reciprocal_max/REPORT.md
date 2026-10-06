# A reciprocal maximum action, and the price of extending it

**A variational spherical maximum is constructible once the cold force is
allowed to change.** The displayed flux-constrained action gives exactly
g_b=b+max(d,p(b)), with positive material cold sources and reciprocal source
reaction. Its changed cold force is derived, not imposed independently.
A convex six-vector completion also exists, but it changes nonspherical
Newtonian behavior. Conversely, a globally convex completion that preserves
the complete Newton vector law in its OFF region is impossible on the
unrestricted flux domain. A second price is absent baryonic capture of dilute
cold tracers in the MOND-active branch. Some cold circular orbits are unstable,
but a cosmic-ratio finite positive profile has stable ordered radial support.

This is a **new static nonrelativistic construction**, not closure of the cold
identity, abundance, cosmology, lensing, or covariant action. The original
FL1 coupling is changed; its earlier cosmological/merger gates do not transfer.

Requested base: `11b994fee`; observed entry HEAD was
`614eab208a205314e7076c4edfe018c9b78e47f7`. Shared HEAD advanced during the
work; final run observed `2b166352b1c7603592194e1af34feedf55832aa2`.
Actual before/after source hashes and dirty checkout state are pinned in the
version-2 run manifests. Writes are confined to this directory; no commits or
other-lane edits. This is a derivation and author self-review.

## 1. Exact scalar primitive and reciprocal forces

Let b,d>=0 be outward aligned Newtonian baryon/cold source flux magnitudes,
a=a0>0, and specifically adopt the **P2** phantom

    p(b)=sqrt(b²+ab)-b.

It increases from 0 to a/2. Define

    I(b,d)=integral_0^b [p(s)-d]_+ ds,
    H_k(b,d)=b²/2+bd+k d²/2+I(b,d).                              (1)

k=1 implements the proposed boundary H(0,d)=d²/2. k>1 is a separate
continuation changing that boundary to k d²/2 and adding a declared cold
self-gravity parameter. Neither k nor a is derived by this package.

For 0<d<a/2, p(b_t)=d has unique solution

    b_t(d)=d²/(a-2d), b_t'=2d(a-d)/(a-2d)².

The active region is b>b_t, equivalently p(b)>d. For d>=a/2 it is empty.
Writing P'=p, P(0)=0, a convenient primitive is

    P(b)=(b+a/2)sqrt(b²+ab)/2-b²/2
         -(a²/8)log[(2b+a+2sqrt(b²+ab))/a].

Active:

    H_k=b²/2+k d²/2+P(b)-P(b_t)+d b_t,
    H_b=b+p(b), H_d=k d+b_t.                                  (2)

Inactive:

    H_k=b²/2+bd+k d²/2,
    H_b=b+d, H_d=b+k d.                                       (3)

The moving lower-boundary terms in H_d cancel because P'(b_t)=d.
Thus the baryon force is exactly the desired maximum, and

    g_d=k d+min(b,b_t(d)),                                    (4)

with min=b for d>=a/2 and b_t(0)=0. H and its first derivatives are continuous
at the interface. Its second derivatives have one-sided limits; it is not
a globally C2 constitutive law.

The **reciprocity price theorem** follows immediately. In the open active
region g_b=b+p(b) is independent of d, so integrability requires
partial_b g_d=partial_d g_b=0. An unchanged g_d=b+d violates that equality.
For a general finite pure-cold boundary F(d)=H(0,d), the active dark force is
F'(d)+b_t(d); the b-independent behavior is not specific to k=1.

## 2. Actual constrained action and source reaction

Introduce independent spatial flux vectors B,D, density sources rho_b,rho_c,
and multiplier potentials phi_b,phi_c. The static gravitational part is

    L_g=H(B,D)/(4piG)
        +phi_b[div B/(4piG)-rho_b]
        +phi_c[div D/(4piG)-rho_c].                            (5)

Add baryonic kinetic terms and, if the existing wave realization is retained,
its standard nonrelativistic complex-field kinetic/gradient terms, with
rho_c=m|psi|². Variation of phi imposes

    div B=4piG rho_b, div D=4piG rho_c.

Variation of the independent fluxes, integrating by parts, gives

    grad phi_b=partial_B H, grad phi_c=partial_D H.

Matter therefore feels attractive forces -grad phi_b and -grad phi_c. With
a single H=|B|²/2, eliminating B gives the familiar negative
|grad phi|²/(8piG)-rho phi action. The signs in (5) do not interpret positive
convex H as a positive **physical gravity Hamiltonian**: this is the dual
static/elliptic formulation, not a Lorentzian energy-health theorem.

In isolated spherical symmetry, regular central matching and source Gauss
constraints fix B=G M_b(<r) rhat/r² and D=G M_c(<r) rhat/r², aligned outward
for nonnegative sources. Equations (2)-(4) then give the exact target without
subtracting a phantom profile from positive material mass. The earlier
negative-residual-density obstruction is escaped by changing the coupling.

Reaction is built into the same variation. For smooth solutions, put

    T_ij=[B_j (partial_B H)_i+D_j (partial_D H)_i
          -delta_ij(B dot partial_B H+D dot partial_D H-H)]/(4piG).

Because both constitutive gradients are potential gradients, their curls
vanish. The Legendre trace cancels B_j partial_i(partial_B H)_j and its
D counterpart. Differentiating T therefore yields

    partial_j T_ij=rho_b partial_i phi_b+rho_c partial_i phi_c.

Hence matter force plus field-stress divergence vanishes. Isolated surface
conditions give zero net internal force. The weak/subgradient version needs
its corresponding regularity/boundary treatment; it is not silently inferred
from this smooth formula. An autonomous coupled matter action also has the
usual time-translation conservation identity, but global dynamical bounds
and a covariant stress tensor have not been proved.

Wave variation gives Schrodinger evolution in phi_c, with the usual conserved
U(1) mass current. It does **not** retain FL1's Newtonian u-force. Source
conservation and reciprocal forces are achieved together; the cold field's
mass, state and abundance remain independently specified.

## 3. Convex full-vector completion, including its axes and null directions

Choose the explicit isotropic extension

    H_norm(B,D)=H_k(|B|,|D|).                                  (6)

The scalar Hessian is active diag(1+p',k+b_t') and inactive
[[1,1],[1,k]]. For k=1 it is positive semidefinite, with a radial flux-split
null direction in the inactive region. H is jointly convex and coordinatewise
nondecreasing on the quadrant, so composition with both norms is convex.

At nonzero fluxes write n=B/b,t=D/d. Its entire six-variable Hessian is

    H_BB=H_bb n n^T+(H_b/b)(I-n n^T),
    H_DD=H_dd t t^T+(H_d/d)(I-t t^T),
    H_BD=H_bd n t^T, H_DB=H_BD^T.                              (7)

This checks transverse as well as radial variations for arbitrary relative
directions. The two transverse blocks are positive, not hidden by assuming
alignment. For k>1 the global strong-convexity modulus is

    mu_k=[1+k-sqrt((k-1)²+4)]/2>0.

The inactive radial eigenvalue is mu_k; the active radial values exceed 1,k;
H_b/b>=1 and H_d/d>=k. More globally, subtract
mu_k(b²+d²)/2 from scalar H: its Hessian remains positive semidefinite and
its coordinate derivatives remain nonnegative. Norm composition then proves
H_norm-mu_k(|B|²+|D|²)/2 convex, including the axes. k=2 gives
mu=(3-sqrt5)/2. This is an actual strongly convex monotone dual candidate.

There is an axis price: at B=0,D!=0 the norm extension has a baryon cusp
with a subgradient ball, since H_b(0,d)=d. Flux convexity and a weak variational
form remain meaningful, but a unique baryon **test potential** in such a zero-B
region is not provided just by unique fluxes. At D=0,b>0, H_d tends to zero
and there is no analogous cold cusp. Smooth regularization of the B-axis
changes the exact small-b maximum and must be treated as a new premise.

On a bounded compatible domain, assume the prescribed divergence/normal-flux
constraints define a nonempty closed affine L2 flux set. H_norm is coercive
and has at most quadratic growth plus a linear term. For k>1 a minimizing
sequence is bounded, has a weakly convergent subsequence, the constraint set
is weakly closed, and convex integral energy is weakly lower semicontinuous.
It has a unique constrained flux minimizer. This standard direct argument
does not prove smooth multiplier existence, global PDE/matter evolution,
or a cosmological solution. k=1 permits nonunique splitting; it still supplies
the explicit static stationarity system.

## 4. Why globally convex Newton-OFF vector completion is impossible

The simple alternative retaining |B+D|²/2 rather than (b+d)²/2 has the same
aligned scalar result, but its active transverse cold Hessian is

    1+(b_t-b)/d.

At a=1,b=1,d=0.1 it equals -8.875. The coupled transverse block has minimum
eigenvalue -8.972215. Thus the naive Newton-vector extension is not convex.

There is a stronger obstruction to **any** globally convex repair confined
to the active region. Assume a globally convex finite H on unrestricted
(B,D) in R6, exact aligned baryon radial maximum, a finite boundary
F(d)=H(0,d), and full Newton vector gradients

    partial_B H=partial_D H=B+D whenever |D|>=a/2.

That OFF region is connected. Integrating its prescribed gradient fixes
H=|B+D|²/2+C there, with one constant C. Fix an aligned active point
X=(B,D), d<a/2 and sum S=B+D. For a sufficiently large vector V, both

    X_plus=(B+V,D-V), X_minus=(B-V,D+V)

are OFF and have the same sum S. Their midpoint is X. Convexity therefore
requires H(X)<=|S|²/2+C.

On aligned fields, integrating the required baryon force gives instead

    H(b,d)-(b+d)²/2=F(d)-d²/2+I(b,d).

For fixed d<a/2, I(b,d) grows asymptotically as (a/2-d)b plus slower terms.
No finite F(d) can keep this difference below C as b becomes unbounded.
**Contradiction.** This version allows arbitrary finite boundary offsets,
not only F=d²/2. With the requested boundary already fixed, the explicit
point b=1,d=.1 suffices: required H=.845709719, while Newton-OFF endpoint
mean=.605, a convexity gap .240709719.

This is a scoped price theorem, not a no-go for the spherical maximum itself.
It assumes unrestricted opposing flux directions and unbounded magnitudes,
the full OFF vector-gradient condition, and global convexity. Restricted
flux domains/finite windows, changed OFF vectors, or nonconvex actions escape
its hypotheses and need their own health analysis. Extra angular terms that
vanish everywhere OFF cannot restore global convexity under these assumptions.

The construct (6) pays the changed OFF-vector price: partial_B H=(b+d)n and
partial_D H=(b+k d)t there, rather than B+D. For k=1 these agree with Newton
in the aligned spherical reading; for k>1 even that dark self-force becomes
kG. No linear cosmological or lensing pass is inherited.

## 5. Cold capture, orbit instability and a surviving radial-support window

For fixed b>0, as d approaches zero the active cold force satisfies

    g_d=k d+d²/a+O(d³/a²) ->0,

although baryons feel b+p(b)>0. Dilute cold tracers are not captured by the
baryonic MOND field in this completion. This is the reciprocal price of a
baryonic force independent of d, rather than an omitted source reaction.
For example a=b=r=1,d=.1,k=1 gives g_b=sqrt2 and g_d=.1125, so the two
circular speeds differ by sqrt(.1125/sqrt2). This predicts changed halo
assembly and cold velocity support; no measured cold speed is claimed.

For compact spherical sources exterior to both bodies, b,d are proportional
to r^-2. On the active branch the dark epicyclic stiffness is

    omega_r²=g_d'+3g_d/r
            =[k d-d²(a+2d)/(a-2d)²]/r.                         (8)

Static convexity is not dynamical orbital stability. a=b=r=1,d=.3 is active
and has omega_r²=-.6 at k=1, -.3 at k=2. An independent nonlinear radial
integration at k=1, starting only 1e-5 away from the circular radius, grows
to displacement .00011099 by t=4 while remaining active; its conserved
background-orbit energy drifts by only 1.1e-16. The d=.1 stable control
oscillates within its initial 1e-5 displacement over t=40.

No finite k protects all compact-source ratios: the second term in (8)
diverges as d approaches a/2 from below, and b can be chosen larger than b_t.
More generally with nonnegative finite pure-cold force K(d)=F'(d), active
g_d=K+b_t. Stability for every allowed d would require
g_d/d^(3/2) nonincreasing in d. But g_d>=b_t diverges at the finite endpoint
d=a/2, contradicting that requirement after any finite interior starting
value. This excludes universal stable active point-source orbits under these
premises, not every physically restricted cold profile.

A useful **surviving window** follows by fixing the enclosed ratio eta=d/b.
Active fields then satisfy d<a/(eta+2). Since
t(1+2t)/(1-2t)² increases on 0<t<1/2, the whole active compact-source interval
is stable when

    eta >= [1+sqrt(1+16k)]/(2k).                               (9)

The threshold is 2.561553 for k=1 and 1.686141 for k=2. Cosmic eta=5.36 is
comfortably above both; the global instability does not exclude that window.

For an extended **fixed** cold density profile, the test-particle epicycle
adds 4piG rho_c(k+b_t') to (8), since d'=4piG rho_c-2d/r.
An ordered **Lagrangian moving shell** instead holds enclosed source mass
fixed: d'=-2d/r, so it has (8), without that density derivative. This distinction
prevents using fixed-profile test stability as a collective-shell theorem.

As a concrete finite positive support construction, choose matching Plummer
enclosed profiles

    M_b(r)=r³/(1+r²)^(3/2), M_c(r)=5.36 M_b(r), G=a=1.

Both have finite positive total mass and density, and eta=5.36 everywhere.
Choose cold circular-shell angular momenta j_c²=r³g_d. Active shell stiffness
is positive by (9). Inactive cold shell stiffness is
b'+3b/r+k d/r=4piG rho_b+b/r+k d/r>0. Fixed-profile tracer epicycles are also
positive. The script checks 801 radii from .001 to 100 for k=1,2, corroborating
these analytic signs. A baryonic circular support can likewise be assigned:
active fixed-label stiffness is (b²+2ab)/(r sqrt(b²+ab))>0.

This is **chosen circular support**, not a conserved formation mechanism,
an exact stationary finite-hbar Schrödinger state, or nonradial/merger health.
The profile scale, mass ratio, wave state and angular-momentum distribution
are not selected by (5). The absent dilute-tracer capture remains unresolved.

## Evidence, executed routes and next gap

Internal overlap search covered prior Sol61 cold/action records, CFG44/45 and
the common-action assembly. Those already identify additive bookkeeping and
adiabatic assembly failures. No inspected record contained this positive
flux-action maximum primitive, the global opposing-flux convexity obstruction,
or the cold stability-ratio theorem. Novelty is project-relative; all displayed
proofs are direct derivations and no global literature novelty claim is made.

Executed: scalar reciprocal primitive; full six-vector norm completion;
Newton-vector transverse falsification; global convexity midpoint theorem;
strong-convexity continuation k>1; cold capture limit; point-orbit instability;
and a finite positive stable-ratio radial-support profile. The first symbolic
primitive check initially failed because a manually named Sympy symbol did
not match its generated derivative placeholder; substituting the actual
derivative node fixed the implementation, without changing the equations.

Final main run `runs/main_c/`: 23/23 checks, exit 0. Keeping Newtonian dark
baryon response fails the reciprocity check: control is 22/23, expected exit 1.
Both version-2 manifests validate with actual input/output hashes and retained
stdout/stderr. Earlier `main_a`/control records remain historical and pin the
older script before the added global midpoint test; `main_b` and its control
pin the pre-stress-correction script. They are not the final
evidence. Numerical checks include independent energy-gradient finite
differences, full six-vector derivative reconstruction and nonlinear energy
controls. Runtime is below a second; caps are 30 s wall, 20 s CPU/process,
1 MiB logs and cooperative one-thread numerical libraries.

An independent review found that the initial displayed stress subtracted H
rather than the Legendre trace B dot H_B+D dot H_D-H. This was a real
nonlinear momentum-balance error, corrected above. The final script adds an
exact three-dimensional quartic-energy identity: the corrected divergence
leaves only constitutive curls, while the previous trace fails. The action,
force, convexity and orbit derivations did not depend on that mistaken trace.

Self-review verdict: the displayed static reciprocal construction and scoped
price theorems are proved under their exact assumptions. Bounded calculations
corroborate them. No global healthy theory is asserted. The missing implication
is a physically justified choice paying one of these prices while retaining
cosmological cold growth, galaxy/cluster sources and wave-compatible formation.
The next executable test is a finite-wave or ordered-shell assembly under the
changed phi_c force, initialized independently of the desired profile. A
separate covariant completion and source/lensing dictionary remain open.
