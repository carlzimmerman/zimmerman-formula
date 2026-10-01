# MS1: responsive matter changes the stability question

Date: 2026-09-27. Parent: stage-three DP1 scalar family, frozen Git base
`eccd1c0e59459b5ec1acf2e916fb7a05a7f67971`. Q and R are kept separate.
No literature search, imported mechanism, global background solution, or
historical novelty claim is used. This is a new conditional derivation, not
an empirical gravity model or a cosmological perturbation calculation.

## 1. Background and additional matter assumptions

Retain DP1's preferred inertial time, constant a>0, K>0, c>0, G>0,
tau=K/c² and C=4 pi G. The physical acceleration is −grad phi. The scalar
equation is

    tau phi_tt − div[mu(|grad phi|) grad phi] = −C rho,

where b=F^(-1), mu=b/g, and the spatial Hessian at g0>0 has positive
eigenvalues lambda_perp=b(g0)/g0 and lambda_parallel=b'(g0).

**New matter assumptions:** one inviscid barotropic nonrelativistic fluid,
rho0>0, positive squared sound speed cs²=(dp/drho)_0>0, universal force
−grad phi, and no viscosity, entropy mode or extra matter stress. Continuity
and Euler are rho_t+div(rho v)=0 and
v_t+(v dot grad)v=−grad p/rho−grad phi plus any declared background support.

A homogeneous fluid at rest in a constant nonzero gradient is **not** an
equilibrium of these unsupplemented equations. Constant grad phi has zero
constitutive divergence and cannot source rho0>0. A homogeneous barotropic
pressure also cannot balance the force −grad phi0. The following exact
constant-coefficient calculation therefore has an explicitly artificial,
but unambiguous, background prescription:

* Replace the scalar source by rho−rho0, removing the uniform mode.
* Add a fixed external acceleration +g0 n to the matter equation.
* Impose an affine background phi0=g0 n dot x and periodic, zero-mean
  perturbations psi. The support and subtraction have no perturbations.

Then (rho,v,phi)=(rho0,0,phi0) is an exact equilibrium of this **modified
supported/subtracted model**. This prescription is a definition of a local
perturbation problem, not a negative-mass component or a global solution of
the original isolated-source theory. The imposed background/sources are
external; conserved quadratic perturbation energy below does not establish
global conservation including their unmodelled reservoirs. No accelerating
coordinate transformation is invoked: the preferred-time theory has not been
shown invariant under such a transformation.

One may instead read the same coefficients as a locally frozen approximation
inside a smooth, genuinely balanced inhomogeneous background. That reading
requires k L_background >>1 and relevant times short compared with background
variation, with gradients, advection, tides and boundary effects controlled.
It does not validate the k→0 limit or a global collapse rate. In particular a
putative unstable band is physically useful in a local patch only if it
overlaps the patch's validity range. Existence of that overlap is not proved
here. The exact homogeneous-model theorem and a physical local application
must not be conflated.

## 2. Linear equations and exact dispersion relation

Let delta rho, v and psi be first-order perturbations. For the prescribed
background the equations are

    delta rho_t + rho0 div v = 0,
    v_t = −(cs²/rho0) grad(delta rho) − grad psi,
    tau psi_tt − A_ij partial_i partial_j psi = −C delta rho,

where A=lambda_perp Identity+(lambda_parallel−lambda_perp) n n^T.
For a nonzero wavevector k, put

    L=lambda_perp sin²(theta)+lambda_parallel cos²(theta)>0,
    vphi²=L/tau=c² L/K, s=cs² |k|², J=C rho0 |k|²/tau.

The transverse velocity components are neutral vortical modes (constant in
time at this order). The two longitudinal/scalar branches follow from
the convention exp[i(k dot x−omega t)]. Eliminating the longitudinal velocity
gives

    (omega²−cs² k²) delta rho = rho0 k² psi,
    (tau omega²−L k²) psi = C delta rho.

Thus, with x=omega²,

    (x−cs² k²)(x−vphi² k²) − J = 0,                    (M1)

    x_± = [(cs²+vphi²)k²
           ± sqrt((cs²−vphi²)² k⁴+4 C rho0 k²/tau)]/2. (M2)

The discriminant is strictly positive for k>0, so x_± are real and distinct;
x_+>0 always. The determinant is

    x_+ x_- = (k²/tau)(cs² L k²−C rho0).               (M3)

Define the directional threshold

    kJ²(theta)=C rho0/[cs² L(theta)].                  (M4)

For 0<k<kJ, exactly one branch has x_-<0 and grows at gamma=sqrt(−x_-).
For k>kJ both branches oscillate. At k=kJ the zero-frequency mode is marginal:
the second-order system also allows linear-in-time displacement along its
zero-restoring-force direction. It is not strict positive-energy stability.
K cancels from (M4), but not from frequencies or growth rates.

This already answers the first stage-four question: **positive field-only
energy does not suffice when matter responds.** The attractive coupling can
produce a growing density mode even though K, lambda_perp and lambda_parallel
are all positive. The assertion is about the declared coupled model, not a
proof that every physical galaxy or cluster background is unstable.

## 3. The negative direction is potential energy, not a ghost

Introduce a fluid displacement xi with delta rho=−rho0 div xi and v=xi_t.
Up to first-order background terms, the quadratic action density is

    L2 = rho0 |xi_t|²/2 − rho0 cs² (div xi)²/2
         + rho0 (div xi) psi
         + [tau psi_t² − grad psi dot A grad psi]/(2C).

Both kinetic coefficients, rho0 and tau/C, are positive. There is no
negative-kinetic-energy ghost in this linearized scalar-plus-fluid sector.
For real longitudinal Fourier amplitudes xi=X n_k sin(k dot x) and
psi=Y cos(k dot x), define canonical amplitudes
q1=sqrt(rho0)X and q2=sqrt(tau/C)Y. Spatially averaged quadratic energy is

    E2 = [qdot1²+qdot2² + q^T H q]/4,

    H = [ cs² k²                    −sqrt(C rho0/tau) k
          −sqrt(C rho0/tau) k       vphi² k²           ]. (M5)

Its eigenvalues are exactly x_±. The negative determinant below kJ identifies
an attractive potential-energy instability, while the kinetic matrix stays
positive. Above kJ the whole quadratic form is positive (for these nonzero
longitudinal modes). A field-only calculation drops the interaction term and
therefore cannot detect this negative direction.

Equivalently use real density D cos(k dot x), velocity V sin(k dot x),
potential Psi cos(k dot x) and scalar velocity Pi cos(k dot x). Then

    Ddot=−rho0 k V,
    Vdot=k(cs² D/rho0+Psi),
    Psidot=Pi,
    Pidot=−(L k² Psi+C D)/tau,                          (M6)

and the conserved spatial-average energy is

    E2 = rho0 V²/4 + cs² D²/(4rho0)
         + tau Pi²/(4C)+L k² Psi²/(4C)+D Psi/2.        (M7)

Differentiating (M7) with (M6) cancels every term. This provides an independent
sign and numerical-integrator invariant without assuming the dispersion.

## 4. Long-wave growth, high-frequency well-posedness and limits

For cs²>0 and finite tau>0 the high-k principal characteristic speeds are
cs and vphi; both are real. If cs²=vphi², (M2) becomes
x_±=cs²k² ± sqrt(Crho0/tau)k, again positive for sufficiently high k.
The degeneracy therefore introduces no ultraviolet growth in this constant
coefficient problem. The positive kinetic and principal spatial forms give a
well-posed linear evolution; the lower-order attractive coupling permits only
a bounded unstable band. This is not a global nonlinear existence theorem.

There is a useful analytic bound. For a growing mode (M1) is equivalent to

    (gamma²+cs²k²)(tau gamma²+L k²)=C rho0 k².

Because all factors are positive,

    0<gamma²<C rho0/L−cs²k²       (0<k<kJ, tau>0).     (M8)

Thus retardation reduces growth relative to the instantaneous scalar limit.
At fixed k in the unstable band, implicit differentiation also shows gamma²
strictly decreases as tau (and hence K) increases. The cutoff remains fixed.

The limits do not commute. At fixed nonzero k as tau→0,

    x_- → cs²k²−C rho0/L,

the ordinary static attractive-response result for this anisotropic kernel.
At fixed tau and k→0 instead,

    gamma² = sqrt(Crho0/tau)|k| − (cs²+vphi²)k²/2
             + O(|k|³),

so gamma→0. The zero mode was removed by the background prescription, and
this long-wave asymptotic is not an isolated-system or cosmological result.

If the pressureless boundary cs²=0 is admitted, all k>0 have one growing
branch, but gamma²→C rho0/L as k→infinity: growth does not become arbitrarily
fast. This is distinct from the negative-compressibility control cs²<0,
which yields gamma proportional to k at high k and is a gradient instability
of the assumed matter equation. Pressureless-fluid caustics and zero-gradient
scalar degeneracy require separate nonlinear analysis. We do not extend the
strict cs²>0 theorem to those cases.

## 5. Q/R anisotropy and the normalizations

For u=B0/a>0, Q gives

    lambda_perp=sqrt[u/(u+1)],
    lambda_parallel=2sqrt(u²+u)/(2u+1).

For R set t=sqrt(u), d=1−exp(−t):

    lambda_perp=d,
    lambda_parallel=d²/[d−t exp(−t)/2].

These follow from b/g and 1/F_B directly. Both branches have
lambda_parallel>lambda_perp>0, hence kJ is smaller for propagation along the
background gradient than across it. In the deep regime the ratio
lambda_parallel/lambda_perp→2, so the corresponding threshold-wavenumber
ratio kJ_perp/kJ_parallel→sqrt(2). All of this retains the chosen scalar
extension; it is not a universal statement about every gravity theory sharing
the same radial curve.

At fixed u the eigenvalues do not depend on which registered a normalization
is used. At a fixed physical B0 they differ, and the finite calculation carries
a=9.3619e-11 and 1.1279e-10 m/s² separately. It also records a frozen-epoch
comparison a=a_today E(3), E(3)=sqrt(.315*64+.685). That comparison supplies no
time-dependent a equation or expansion terms; it is valid dynamically only
if the parameters can be frozen over the timescale of interest. The separate
stage-four scale lane owns the missing scale dynamics.

## 6. What data could constrain K

Static equilibrium, this instability cutoff and a static density response
contain no K. A measurement of those quantities alone cannot select it.
With calibrated B0/a, angle, sound speed and wavenumber, two dynamically
resolved branches give

    K = c² L / [(x_++x_-)/k²−cs²].                     (M9)

Here x_- may mean −gamma² if growth is independently measured. Density
calibration is not needed in this trace formula, but both modes and the other
listed inputs must be identified in the same valid background model.

A single nonzero mode, with independently known rho0 as well, gives

    K = c² k² [L(x−cs²k²)+C rho0]
        / [x(x−cs²k²)],                               (M10)

provided the denominators are nonzero and the mode belongs to this model.
The same statement can be expressed through a measured growth rate using
(M8)'s exact preceding equation. Dynamic source-response phase/time delays
or a propagating scalar mode could provide such information. None has been
measured in this campaign.

This identifiability can be badly conditioned: when cs and gamma/k are much
smaller than vphi, the lower branch is nearly quasistatic and its fractional
K sensitivity is suppressed. A synthetic dimensional example deliberately
quantifies that suppression. It is not a forecast or a real source fit.
Nuisance density, sound speed, B/a, boundaries, driving and background support
must be constrained jointly; assigning a growth rate to K without them is
not a measurement.

## 7. Exact scope, dependency graph and first remaining implication

Q/R static law -> inverse constitutive Hessian (accepted DP1 input).
Additional fluid equation + supported/subtracted background -> (M6).
(M6) -> determinant (M1), energy (M7), threshold and kinetic-sign diagnosis.
Positive eigenvalues + cs²>0 -> high-k characteristic control.
Dynamic frequencies and calibrated inputs -> conditional K inversion.

The main theorem is the exact longitudinal dispersion and energy-sign
classification of this specified constant-coefficient model. Numerical runs
test the implementation and independent time evolution; they do not supply
a global physical background or prove the universal statements.

**First remaining implication:** construct and independently balance a finite
inhomogeneous scalar-plus-fluid background with physical boundaries, then
solve its coupled perturbation problem. This must establish whether the local
unstable wavelength/time range actually exists inside that background before
interpreting the homogeneous-model growth as an astrophysical instability.
The next executable step is a one-dimensional finite slab or spherical
barotropic equilibrium, with specified density/pressure or boundary data,
followed by the coupled eigenproblem with the same constitutive law and K.
Field-only positive energy cannot substitute for that calculation. Selecting
and observing K, closing scale dynamics, photon coupling and cosmology remain
separate obligations.
