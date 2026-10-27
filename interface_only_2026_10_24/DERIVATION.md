# Interface-only couplings and their reciprocal variations

Scope: candidate spherical Newtonian effective energies, fixed baryon moments
and total cold density in the numerical phase tests. These are new postulates
built on the previous response-weighted stiffness, not microscopic derivations.
Base a442dd0e256cacb80316c0a717ab4b1232752546; source snapshots and manifests
pin exact ancestry. Review is self-review.

## Variables and unchanged terms

q=h(x)=sin²(pi x/2), s(x)=sin²(pi x)/pi². The actual T field is
u(r)=integral_0^r n(t) q(t)dt/r², where n=dMc/dr. All F and T mass gravitates.
In units rM=sqrt(G Mb/a0), Eunit=Mb a0 rM, retain w(u)=-log(1-u)-u,
F(u)=u²/(1-u), and beta C s(x)F(u) with beta20. The phase length is30kpc.
There is NO -epsilon q B bulk binding term in this work.

C=A/(A+B), A=|curl v_b|², B=sigma_b² I, I=Lrho^-2=
|grad log rho_b|²+||Hess log rho_b||_F. Kinematic moments use the inherited
Jeans construction with prescribed tapered rotation. They are not observed
profiles or a self-consistent evolving distribution function.

The W energy extends to infinity. The material coupling below exists inside
the supplied cold reservoir. The exterior retains the previous minimized
response-weighted gradient tail to x=0 at2Rreservoir. Its dependence on total
T mass, gamma'(M) and gamma''(M), is included. The support and boundary remain
model assumptions; no free gravitating mass is deleted.

## Route1: positive compliance

Let K0=ell² F(u) and v=Lrho grad C. Introduce a fast scalar z with energy

    e_grad=(K0/2)[|grad x-z v|²+z²/lambda].

For lambda>0 and K0>0 the minimum is at z=(v.grad x)/(v²+lambda^-1), giving

    e_grad=(K0/2) grad x . [I-v v^T/(lambda^-1+v²)] grad x.

The tensor has positive transverse eigenvalues1 and longitudinal eigenvalue
1/(1+lambda v²). In spherical symmetry e_grad=.5 K0 kappa x'²,
kappa=1/(1+lambda C'²/I). At K0=0 the energy vanishes; the auxiliary minimizer
need not be unique. Lambda0 means the unmodified gradient energy.

This is an explicit stable auxiliary representation of the proposed
compliance, not evidence for a physical carrier. It vanishes in uniform
pure phases, including its first C and cold-mass variations. The discrete
phase derivatives are the inherited response-weighted derivatives with
link weights multiplied by kappa. Kappa depends on baryon moments, not cold
mass, so the F'(u) mass derivatives remain compulsory.

## Route2: positive gradient alignment

Define a=grad x-eta h'(x) grad C and postulate

    e_grad=.5 ell² F(u) |a|².

This preserves positive stiffness rather than weakening it. The extra
coupling is isotropic, contains no assigned interface radius, and is zero
for uniform x=0 or1 because h' vanishes. It may act in a uniform mixed
region when C varies; 'interface-only' here means it vanishes in both pure
phases, not that it has compact support for every non-pure configuration.
Eta is an undetermined dimensionless coefficient, not inferred from data.

For radial fields d=x'-eta h'(x)C', the exact phase Euler derivative is

    deltaE/deltax = n h' mu_u + beta r² C s' F
                   -eta r² ell² F d h'' C'
                   -d_r(r² ell² F d),

where mu_u is the full nonlocal mass response defined below. The phase
gradient therefore includes the local h'' term as well as the divergence.

Face discretization uses d=D x-eta h'(Aavg x) D C. Its Jacobian is
Jd=D-eta diag[(DC)h''(Aavg x)]Aavg. Its Hessian involves h'''=-pi²h'.
The implemented energy Hessian includes Jd^T diag(links F) Jd, the second
derivative of d, F'' terms, all mixed d/u terms and the tail. Directional
checks and independent T-mass variations test these terms together.

## Separate cold-matter forces

For alignment, the potential response through the actual enclosed T field is

    mu_u(r)=integral_r^infinity [w'(u)+beta C s F'(u)
                                +.5 ell² F'(u)|a|²]dt,

with the actual exterior matching variation. For compliance replace |a|²
by kappa |grad x|². The discrete mu_u uses the same face residual as its
energy; using old (Dx)² in an aligned model would give the wrong force.

At fixed Eulerian phase, mu_c=q mu_u. Write mu_q=(1/n)deltaE/deltaq;
then independent T and F variations give

    mu_T=mu_c+(1-q)mu_q,
    mu_F=mu_c-q mu_q,
    a_T=-g_total-grad(mu_T),  a_F=-g_total-grad(mu_F).

In the discrete model mu_q=E_x/(m h'). The ratio for mu_T is evaluated as
cos(pi x/2)/[pi sin(pi x/2)] near pure T. A T potential is not interpreted
as an acceleration of material where T is absent. Large raw numerical force
values in failed nearly-F cells are not evidence for a physical force anomaly.
The test is meaningful only after the retained-T condition is satisfied.

In a pure T interior, all local barrier and added interface terms vanish.
An exterior interface changes mu_u there by a spatial constant, so its radial
force vanishes in spherical symmetry. The remaining derivative gives the
parent T force, -(gb+gF)+u²/(1-u). Thus this class can avoid the previous
bulk-binding force by construction. It still needs actual phase stability
and negligible enclosed F mass; those are independent tests.

## Baryon momentum and stress variations

These cannot be omitted from a live completion. Use per-volume derivatives,
with the usual radial measure understood. For alignment, holding u and x
fixed, the coefficient of delta C after integration by parts is

    S=beta s F + div[eta ell² F h'(x) a].

For compliance it is

    S=beta s F + div[ell² F lambda kappa² |grad x|² grad C/I],

and there is a direct coefficient of delta I,

    P_direct=.5 ell² F lambda kappa² |grad x|² |grad C|²/I².

Alignment has P_direct=0. The kinematic chain rule gives

    deltaC=[B deltaA-A deltaB]/(A+B)²,
    deltaA=2 omega.curl(delta v_b),
    deltaB=I delta(sigma_b²)+sigma_b² deltaI.

Therefore the required functional derivatives are

    deltaE/delta v_b = curl[2 S B omega/(A+B)²],
    deltaE/delta(sigma_b²) = -S A I/(A+B)².

Put P=P_direct-S A sigma_b²/(A+B)², g=grad log rho_b, and
H=Hess log rho_b. Where rho_b>0 and ||H||>0, the density derivative is

    deltaE/delta rho_b = [-div(2P g)
                         +partial_i partial_j(P H_ij/||H||)]/rho_b.

These follow from delta log rho_b=delta rho_b/rho_b. Boundary terms supply
the corresponding boundary tractions and must be retained in a live problem.
The density Hessian norm needs a regularization/subgradient prescription at
H=0; the prescribed Plummer profiles do not encounter that ambiguity here.
The vacuum and material edge also need a physical matching prescription.

These are all reciprocal variations of the stated interaction, not a solved
baryon evolution law. Because the energy depends on velocity moments, a
live action must account for its correction to canonical momentum and close
the dispersion stress equation. A bare Newtonian extra acceleration is not
obtained by simply dropping those terms. The numerical tests explicitly keep
baryons fixed; no full live baryon or 3D stability claim is made.

## Boundary stability and dissipation

For any collective interface coordinate R with phase x(R),
F_R=-grad E.dx/dR and at a stationary point k_R=(dx/dR)^T H(dx/dR).
A positive value for one translation mode is insufficient: the lowest full
phase Hessian eigenvalue must also be nonnegative. This is why the apparent
IO-3 force-safe fronts were not accepted from their phase fractions alone.

Evolution uses a fixed positive metric M with M xdot=-grad E and
Qdot=grad E^T M^-1 grad E. The independently integrated heat satisfies
d(E+Q)/dt=0. Internal time is not Gyr. x is an angle and h(x) stays within
[0,1] for every real x, so unconstrained evolution does not create negative
mass even if it leaves the optimizer's principal phase box.

Both interactions remain nonnegative, with all-F a global minimum of the
extra energy. A metastable local front, if found, would not explain how
formation supplied its energy or overcame its barrier. That work remains
separate from the present preservation question.

## Route3: curvature pressure confined to a material interface

A distinct new postulate is

    E4=(a0²/G) ell4^5 integral r² |q'| H^4 dr.

For a spherical level surface H=2/r. A sharp unit jump at R gives
E4=16(a0²/G)ell4^5/R², outward generalized force
32(a0²/G)ell4^5/R³, and positive curvature of the energy
96(a0²/G)ell4^5/R⁴. Unlike ordinary surface tension, this opposes shrinking.
This is conditional on a maintained unit jump: it is NOT a proof that a
freely converting diffuse phase retains that jump. It can instead lower its
amplitude, or move to the material boundary and convert the exterior.

The implemented spherical functional is gamma integral r^-2 f(q') dr,
gamma=16(ell4/rM)^5 and f(p)=sqrt(p²+delta²)-delta. Delta is held fixed
per dimensionless radius, not per cell. On a face this is
gamma/r_face² [sqrt((Dq)²+(delta dr)²)-delta dr]. It vanishes at q'=0.
There is no direct u, baryon C or mass dependence at fixed Eulerian q.
Its exact radial variation is

    V4=deltaE4/deltaq=-gamma d_r[r^-2 q'/sqrt(q'²+delta²)],
    (E4)_x=h'(x)V4,
    (mu_T)_4=(1-q)V4/n,  (mu_F)_4=-q V4/n.

The extra radial accelerations are minus the gradients of these potentials.
They vanish for occupied pure T or pure F away from the interface. Discrete
Hessian terms include both the positive f'' part and the h'' V4 part;
discarding the latter would falsely stabilize the phase. No direct baryon
moment coupling is added by E4; indirect gravity remains.

This radial calculation does not establish a regular, well-posed 3D
level-set curvature theory, angular stability, or a microscopic coefficient.
At zero phase gradient the geometric normal is undefined in such a 3D
extension; only the explicit regularized spherical functional is tested.
Its material support excludes a T/vacuum boundary from the new curvature
term, so escape to an all-T reservoir is allowed and fails the requested gate.
