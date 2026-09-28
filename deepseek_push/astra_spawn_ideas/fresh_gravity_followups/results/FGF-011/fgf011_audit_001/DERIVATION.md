# FGF-011: independent audit of coupled matter modes and slab boundaries

Worker: actual Astra agent `/root/dynamics_precision`, run `fgf011_audit_001`.
This is not a DeepSeek execution. The worker previously authored DP1 but did
not author MS1. All seven MS1 intake hashes matched before the audit. No
author-reported verdict is used as proof. The equations are reconstructed
below, with a separate finite implementation and no import of candidate code.
No literature was searched, and no historical novelty is asserted.

## Normalized claim card and dependency scope

Let C=4 pi G>0, tau=K/c²>0, rho0>0 and cs²>0. The constant-coefficient model
has an affine potential of nonzero magnitude g0, isotropic barotropic matter,
source subtraction rho-rho0 and a fixed externally supporting acceleration.
For Q/R, A is the positive constitutive Hessian and
L=khat dot A khat>0. Quantification is over all nonzero wavevectors in that
**supported, subtracted model**, not unsupplemented homogeneous matter.

The separate slab claim uses an exact finite isothermal hydrostatic background
rho(x)>0, g(x)>0, A(x)=b'(g(x))>0 on [0,d]. Perturbations obey xi=0 and psi=0
at both endpoints. Smoothness sufficient for the integrations by parts below
is assumed; the quadratic identity extends by density to the associated H¹
Dirichlet spaces when the coefficients are smooth and bounded away from zero.

Primary verdict: **proved as written** for MS1's dispersion, threshold, peak
growth, kinetic-sign classification, slab-length identity and proposed
quadratic form under these restrictions. No observational or cosmological
interpretation is promoted. In addition, the actual proposed finite slab has
the positive factorization in section 5, which determines its longitudinal
linear stability without invoking a locally homogeneous growing band.

Dependencies: Q/R inversion -> positive A (DP1 input, formula rechecked here);
supported fluid/scalar equations -> first-order operator -> dispersion/energy;
exact hydrostatic balance -> slab identity and quadratic factorization.
No imported physical mechanism or unverified external theorem is a leaf.

## 1. Reconstruct the operator before eliminating variables

Use delta rho=D cos(k dot x), longitudinal velocity V sin(k dot x),
delta phi=P cos(k dot x), delta phi_t=Pi cos(k dot x). Linearized continuity,
Euler and the scalar equation give directly

    Ddot=-rho0 k V,
    Vdot=k(cs² D/rho0+P),
    Pdot=Pi,
    Pidot=-(L k² P+C D)/tau.                              (A1)

The signs follow from acceleration=-grad phi and derivative of cosine=-k sine.
In particular, the positive P contribution to Vdot is compatible with
attractive gravity because a positive density sources a negative potential.

For a mode exp(-i omega t), continuity plus Euler give
(omega²-cs² k²)D=rho0 k² P. The scalar equation independently gives
(tau omega²-L k²)P=C D. Their determinant is therefore

    (x-cs² k²)(x-vphi² k²)-C rho0 k²/tau=0,
    x=omega², vphi²=L/tau.                               (A2)

The sum is positive, the discriminant is
(cs²-vphi²)² k⁴+4C rho0 k²/tau>0, and the product is
(k²/tau)(cs² L k²-C rho0). Exactly one root is negative precisely when

    0<k<kJ, kJ²=C rho0/(cs² L).                          (A3)

At the threshold the zero mode allows secular displacement; it is not strict
positive-energy stability. K is absent from the threshold, but present in the
two roots. The omitted transverse velocities are neutral, not growing modes.

An independent canonical change of variables is
q1=-D/(sqrt(rho0)k), q2=sqrt(tau/C)P,
p1=sqrt(rho0)V, p2=sqrt(tau/C)Pi. It transforms (A1) into
qdot=p, pdot=-Hq, where

    H=[[cs² k², -sqrt(C rho0/tau) k],
       [-sqrt(C rho0/tau) k, vphi² k²]].                  (A4)

Both canonical kinetic coefficients are positive. A negative root of H is a
potential-energy direction, not a kinetic ghost. The conserved physical
amplitude energy is

    E=[rho0 V²+cs² D²/rho0+tau Pi²/C+Lk²P²/C+2DP]/4.     (A5)

Differentiating with (A1) cancels all terms. This supplies a sign check
independent of solving the characteristic polynomial.

## 2. Independently optimize growth and inspect limits

Put y=k² and z=gamma²>0. The growing mode satisfies

    (z+cs² y)(tau z+L y)=C rho0 y.                       (A6)

At fixed nonzero k, F_z>0 and F_tau=z(z+cs²y)>0, hence dz/dtau<0.
Dividing (A6) by y gives z<C rho0/L-cs²y. This strict bound requires finite
tau>0 and an interior unstable mode, exactly as stated in MS1.

At a stationary z(y), differentiation of (A6) yields
cs²(tau z+L y)+L(z+cs² y)=C rho0. Subtract y times that expression from (A6):

    tau z²=cs² L y², so z=cs vphi y.

Substitution back gives the unique positive stationary point

    k_peak/kJ=sqrt(cs vphi)/(cs+vphi),
    gamma_max=sqrt(C rho0/L)/(1+cs/vphi).                 (A7)

The arithmetic-geometric mean inequality bounds k_peak/kJ by 1/2.
Growth vanishes at both endpoints for finite tau, so this stationary point
is the unique maximum. These formulas are correct as written; they do not
specify the growth rate of an unconstructed physical background.

At high k and cs²>0, x/k² tends to cs² or vphi², with both positive.
Equal principal speeds give x=cs² k² +/-sqrt(Crho0/tau) k, still positive
for sufficiently high k. At fixed tau and small k,
gamma²=sqrt(Crho0/tau)|k|-(cs²+vphi²)k²/2+O(|k|³), whereas the fixed-k
tau->0 limit gives x_-=cs²k²-Crho0/L. The limits indeed do not commute.
Pressureless cs²=0 gives bounded high-k growth gamma²->Crho0/L; that fact
alone does not assert a nonlinear or derivative-loss-free dust evolution.
Negative cs² is outside the main assumptions and supplies a genuine
short-wave gradient-instability control.

The two dynamic K inversions in MS1 follow directly from the trace and (A2).
For one mode the denominators x(x-cs²k²) must be nonzero. Density, sound speed,
L, boundaries and support must still be calibrated; no static K measurement
or observation is supplied by these algebraic identities.

## 3. Background audit and exact slab length obstruction

An unmodified uniform positive density cannot source an affine potential:
div(mu grad phi0)=0, whereas the scalar equation requires C rho0>0.
Uniform barotropic pressure also cannot balance the nonzero acceleration.
MS1 correctly makes both the uniform-source subtraction and fixed external
support explicit. Removing force by an accelerating coordinate transformation
would require a symmetry not established for this preferred-frame action.

Consequently the exact homogeneous dispersion is a theorem for the declared
supported/subtracted model. An actual local use would require k times every
relevant variation length much greater than one, plus a frozen-background
time window. It cannot inherit that validity from the determinant calculation.

For a genuine positive-gradient hydrostatic slab, the actual equations are

    cs² rho'=-rho g,   A g'=C rho.

Thus Lrho=cs²/g, Lg=g A/(C rho), while the longitudinal local threshold is
kJ²=C rho/(cs² A). Multiplication gives the exact identity

    kJ² Lrho Lg=1.                                      (A8)

Since min(Lrho,Lg)<=sqrt(Lrho Lg), every k<kJ has
k min(Lrho,Lg)<1. There is no growing band that is simultaneously a slowly
varying local patch of **this** equilibrium class. This does not itself prove
the slab's global linear stability; section 5 supplies a separate argument.

Dimensionless chi=x a/cs², u=B/a and r=C cs² rho/a² reduce the exact static
equations to u'=r, r'=-r f(u). The first integral is
r+integral_(u0)^u f(v)dv=r0. The independent computation reconstructs r from
this first integral and integrates a scalar ODE for u, rather than copying
the author's two-state integration. It checks the four pinned backgrounds.

## 4. Is the proposed inhomogeneous quadratic form correct?

For a material displacement xi about the static slab, linear continuity gives
delta rho=-(rho xi)'. The isothermal Euler force varies as

    delta[-cs² (log rho)'-phi']
       =-[cs² delta rho/rho+psi]'.

This matches the proposed xi_tt equation, including background density
gradients. Varying the proposed potential energy

    V=integral [cs²(delta rho)²/(2rho)
                 +A(psi')²/(2C)+delta rho psi] dx                    (A9)

with delta xi=delta psi=0 at the walls gives
rho xi_tt=-rho[cs²delta rho/rho+psi]' and
tau psi_tt-(A psi')'=-C delta rho. The kinetic form is positive:
integral [rho xi_t²+tau psi_t²/C]dx/2.

For the scalar part the endpoint term is A psi' delta psi/C; for the matter
variation it is -rho[cs²delta rho/rho+psi]delta xi. Both vanish with the stated
Dirichlet/impermeability conditions. A fixed wall does no pressure work, and
psi=0 for all times implies psi_t=0 at the wall and zero perturbative scalar
energy flux there. Unequal background wall pressures and fixed background
potential values are nevertheless external support, not an isolated object.

One must not additionally impose zero perturbed scalar flux A psi'=0 at both
walls: that would generally overdetermine the Dirichlet problem. The initial
background fluxes can be reported as properties of the constructed background;
they need not remain fixed when external scalar potentials are held fixed.
This boundary distinction should be retained by any numerical continuation.

## 5. New audit result: positive factorization on the whole finite slab

The proposed global quadratic form has more structure than the homogeneous
calculation suggests. Set zeta=rho xi. Integrating its coupling term by parts,
then completing the square, gives

    2V = integral [(A/C)(psi'+C zeta/A)²
                    +cs²(zeta')²/rho-C zeta²/A] dx
           -2[zeta psi]_0^d.

Use rho'/rho=-g/cs² and g'=C rho/A to calculate

    cs²(rho')²/rho-cs²rho''-C rho²/A=0.

Expanding zeta'=rho xi'+rho'xi and integrating its cross term therefore yields

    2V = integral [cs² rho (xi')²
                  +(A/C)(psi'+C rho xi/A)²] dx
           +[cs² rho' xi²-2rho xi psi]_0^d.             (A10)

For xi=psi=0 at both walls the boundary term vanishes exactly. Each integrand
is nonnegative. If V=0, the first term makes xi constant and impermeable walls
make xi=0; the second then makes psi constant and Dirichlet walls make psi=0.
Thus V is strictly positive on every nonzero admissible longitudinal
perturbation. On a finite interval with positive smooth bounded coefficients,
Poincare estimates strengthen this to coercivity on the two H¹_0 fields.

Together with the positive kinetic form, this proves positive squared
frequencies and bounded linear energy evolution for the specified full finite
one-dimensional slab boundary problem, for all K>0. It is not a theorem about
three-dimensional modes, a free boundary, an isolated halo, a different equation
of state, g=0 degeneration, nonlinear matter collapse, lensing, or cosmology.
No finite eigenvalue grid is required to prove (A10). A conforming variational
discretization should preserve this sign. A converged negative eigenvalue for
these exact assumptions would refute the implementation or the factorization,
and should first be treated as an audit failure, not a discovered physical
instability. This sharpens the proposed FGF-015 continuation; FGF-012 is a
separate cluster audit. No shared task specification is modified by this worker.

## 6. Computational contract, controls and coverage

Before coding, the contract is: independently assemble (A1), its canonical
transform, (A4), and the energy Hessian on MS1's declared 672-case parameter
box; audit both roots and their signs rather than only a large-root-scaled
error; independently maximize growth in its 96 backgrounds; restore both
registered a normalizations and the separate frozen E(3) comparison; reconstruct
four slabs via their first integrals; check (A8) and the integrated (A10) on
nontrivial admissible trial functions. Use binary64, deterministic inputs and
the bounded computation-audit runner. No candidate module is imported.

Negative controls are the nonzero residual of the unsupplemented homogeneous
background and a signed boundary term when xi does not vanish at a wall.
The latter distinguishes an actual boundary-dependent identity from a
pointwise positivity slogan. Analytic statements above, rather than finite
sampling, carry the universal claims. The results report implementation
coverage, tolerances, source hashes, failures if any and exclusions.

The exact Q/R formulas are retained. At fixed B/a the normalization cancels;
at fixed physical B it does not. The H comparison freezes a at one epoch
and does not supply an evolving scale or a cosmological background. The
variable-scale field from SD1 is not included in this audit.

Remaining implication: verify a conforming finite-slab eigen-discretization
against (A10), then decide which boundary/background class is physically
relevant before converting a frequency into a constraint on K. The current
supported homogeneous growth rates cannot be attached to the exact slab via
a locally homogeneous unstable approximation.
