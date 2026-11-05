# What the curvature term does to local matter dynamics

The field equations determine a static susceptibility. A dynamical statement
also requires a matter model. Here that model is explicitly the ordinary
nonrelativistic continuity equation and barotropic Euler equation, with a
local density rho0>0 and squared sound speed c_s²>=0. This does not assume
a relativistic completion, collisionless stellar closure or microscopic
cutoff. The result below is exact for the frozen-coefficient linear system
and is a local short-wavelength diagnostic of a slowly varying background.

## 1. Full Fourier symbol, including the mixed terms

Let E(g,H)=a0² x R(z), x=g.g/a0², s=ell² H:H/a0², z=x+s**p.
The specified full field equations can be written

    Delta psi=4piG rho,
    Delta Phi=(1/2) partial_i E_gi-(1/2) partial_i partial_j E_Hij.

Freeze the second derivatives of E at a smooth local background jet (g,H).
For delta psi proportional to exp(i k n.r), |n|=1, set

    K(n)=(1/2) E_gg[n,n],
    N(n)=(1/2) E_HH[nn,nn].

The two mixed terms in Delta delta Phi are

    -(i/2) k³ E_gH[n,nn] delta psi
    +(i/2) k³ E_Hg[nn,n] delta psi.

They cancel by symmetry of the second variation of E. Hence the complete
constant-coefficient transfer is

    delta Phi_hat=[K(n)+N(n) k²] delta psi_hat.

The sign is positive in front of N k². This follows by dividing the
linearized field equation by -k², and is separately checked by a sinusoidal
second-energy variation. Derivatives of the actual nonconstant background
give lower-order terms; this formula is not an assertion that g and H can
both be independent constants over an entire galaxy.

For x>0 and s>0 define f=x/z, t=s**p/z=1-f, d=zR'(z)<0 and
alpha=-zR''(z)/R'(z). Then

    D=p ell² s**(p-1) f d,
    K(n)=R+f d+2[(n.g)²/(a0² z)] d [2-alpha f],
    N(n)=D {1+2[(p-1)-p alpha t] (n.H.n)²/(H:H)}.

N has length-squared units. At H=0, p>1, N=0 and K reduces to the ordinary
QUMOND linear response around a nonzero uniform field. No derivative through
the joint g=H=0 singularity is invoked here.

For a symmetric H with eigenvalues lambda_i, put

    qmax=max_i lambda_i²/(H:H),
    qmin=0 if [min lambda_i,max lambda_i] contains zero,
         min_i lambda_i²/(H:H) otherwise.

N is affine in q=(n.H.n)²/(H:H), whose attainable interval is exactly
[qmin,qmax]. Its directional minimum and maximum are therefore obtained by
evaluating the displayed expression at these two endpoints, in either order.
This gives an exact angular optimization, not a sampled-direction estimate.

## 2. A useful exact bound for the simple-nu primitive

Since Q(0)=0,

    R(z)=integral_0^1 Q'(u z) du,
    -R'(z)=integral_0^1 u [-Q''(u z)] du>0.

For the specified simple nu,

    -Q''(z)=1/[2 z**(5/4) sqrt(sqrt(z)+4)].

Its negative logarithmic slope is

    beta(z)=5/4+(1/4) sqrt(z)/(sqrt(z)+4),
    5/4<beta(z)<3/2, for every finite z>0.

Differentiating the integral above shows alpha is the positive-weighted
average of beta(u z), with weight u[-Q''(u z)]. The endpoint singularity is
integrable (weight proportional to u**(-1/4)); differentiation on compact
positive-z intervals is justified by the same integrable bound. Therefore

    5/4<alpha(z)<3/2,  z>0.

The limits are 5/4 as z tends to zero and 3/2 as z tends to infinity.
For stable evaluation, with v=z**(1/4), use

    alpha=2-(zQ'')/d,  zQ''=-1/[2v sqrt(v²+4)].

## 3. Negative static response is not automatically unstable

In a locally comoving, accelerating frame, the principal linearized fluid
equations are

    partial_t delta rho=-rho0 div delta v,
    partial_t delta v=-grad delta Phi-(c_s²/rho0) grad delta rho.

Eliminating velocity and using delta psi_hat=-4piG delta rho_hat/k² gives

    partial_t² delta rho_hat=
      {4piG rho0 K(n)+[4piG rho0 N(n)-c_s²] k²} delta rho_hat.

Equivalently, for exp(-i omega t),

    omega²=[c_s²-4piG rho0 N(n)] k²-4piG rho0 K(n).

Here omega is the comoving frequency. In a laboratory frame with a locally
constant background velocity v0, the left side is instead

    (omega-k_vector.v0)².

Constant translation supplies this leading Doppler shift; it is not a
lower-order term. It changes the real frequency but not the exponential
growth rate. Background velocity gradients and other varying coefficients
require the separate lower-order WKB analysis.

Thus N<0 contributes positive effective compressibility/sound-speed squared;
it stabilizes the sufficiently short-wave branch of this fluid model. N>0
instead subtracts from pressure support. A high-k growing branch exists if

    c_s²<4piG rho0 N(n).

Its growth rate is asymptotic to
k sqrt(4piG rho0 N(n)-c_s²). The equality case is marginal only at leading
order and requires the lower-order terms. No assertion that finite pressure
always cures a full inhomogeneous problem follows from this necessary local
condition.

The same sign follows from the density energy. Because delta U/delta rho=Phi,
the leading high-k gravitational quadratic energy is
-2piG N |delta rho|². The barotropic matter term is
c_s² |delta rho|²/(2rho0). Their sum has the sign of
c_s²-4piG rho0 N. The new curvature response therefore behaves locally like
an anisotropic contribution to compressibility, with either sign; it is not
simply a positive smoothing pressure.

## 4. An exact positive-density tidal example at p=9/8

For a pure Kepler tide H proportional to diag(-2,1,1), qrad=2/3 and
qtan=1/6. For p=9/8,

    Nrad=D [4p-1-4p alpha t]/3.

Since D<0, t>28/45 guarantees Nrad>0 for every z>0 by alpha>5/4.
The tangential N remains negative, since p+2-p alpha t>0. A vacuum tide
alone has rho0=0 and cannot by itself demonstrate a matter-fluid instability.

To remove that loophole, choose the following local jet in a0=ell=1 units:

    g=(1,0,0), H=diag(-199/100,101/100,101/100), p=9/8.

This is a Kepler tide plus (1/100)I. It is realizable by a point source at
distance ell and a locally uniform positive-density component. Its trace is
3/100, so rho0=3a0/(400piG ell)>0 in physical units. It is an admissible
local initial background, not a claimed static global galaxy solution.

Here s=60003/10000>6 and t=s**p/(1+s**p)>6/7. Consequently

    J=(p-1)-p alpha t < -121/112,
    qrad=39601/60003,
    1+2J qrad < 1-4791721/3360168 < 0.

Therefore Nrad>0, strictly. Conversely J> -25/16 and
qtan=10201/60003 imply

    1+2J qtan > 1-255025/480024 > 0,

so Ntan<0. These are rational sign bounds, not numerical sampling.

Numerically, in ell² units,

    Nrad=+0.0153524100137, Ntan=-0.0161826587081,
    Krad=1.34354314758, Ktan=1.41464745151.

With ell=3 kpc, the original canonical a0 gives local density
0.00053427 Msun/pc³ and radial critical sound speed 1.99770 km/s; the
alternate footing gives 0.00064567 Msun/pc³ and 2.19611 km/s. These numbers
describe the explicit example, not a measured or fitted MW location. In the
formal dust/high-k limit, a one-parsec wavelength has e-folding times about
77,900 and 70,862 years respectively. No claim that the continuum law applies
to arbitrarily short physical scales is being supplied by this illustration.

For c_s=0 the frozen linear system has growth proportional to unbounded k
and hence is not well posed in ordinary Sobolev norms without a cutoff or
additional pressure/kinetic physics. For the full varying-background system,
this is a local WKB obstruction, not a complete PDE well-posedness theorem.
It is more specific than a sign warning, but it is not a collisionless,
microscopic or relativistic no-go theorem.

## 5. Several gas components and a fixed-profile hydrostatic completion

Let each responding component i have density rho_i>0 and a local barotropic
sound speed c_i, while other matter supplies only a fixed background. At
leading order in k the symmetric growth matrix for
y_i=delta rho_i/sqrt(rho_i) is

    M_ij=4piG N(n) sqrt(rho_i rho_j)-c_i² delta_ij.

For N>0 and all c_i²>0, congruence by diag(1/c_i) gives

    -I+4piG N w w^T,  w_i=sqrt(rho_i)/c_i.

Congruence preserves the signs of the eigenvalues. There is exactly one
positive direction iff

    4piG N(n) sum_i rho_i/c_i²>1.

Equality is marginal at leading order. If any responding component is
strictly pressureless and has positive density, N>0 already gives a positive
Rayleigh quotient in that component's direction. This is a multi-fluid
statement, not a replacement for a collisionless kinetic calculation.

For a fixed vertical profile rho_i proportional to sech²(z/(2h_i)),

    rho_i'/rho_i=-tanh[z/(2h_i)]/h_i.

Vertical hydrostatic balance P_i'=-rho_i g_z, together with the *additional
barotropic closure*, fixes the local derivative

    c_i²=dP_i/d rho_i=h_i g_z/tanh[z/(2h_i)].

For z>0 and g_z>0 this is positive. Hydrostatic equilibrium alone does not
determine the perturbation sound speed: entropy, anisotropy, turbulence,
magnetic forces or a nonbarotropic closure can change the perturbation law.
Applying this formula therefore tests a named completion of the fixed gas
profiles, rather than imposing an observed gas dispersion or rejecting all
possible matter completions.

## Evidence and scope

`run_003` checks 432 deterministic jets against independent tensor finite
differences, both mixed partials and four sinusoidal second-energy tests.
It also evaluates the exact positive-density example above. Historical KT39
code is imported read-only. The primary sign result and alpha bound are
proved analytically here; the finite checks are supporting evidence.

Two earlier runs are preserved as failed numerical controls. The first used
a component-relative mixed-derivative comparison on very small contractions;
the second used the correct full-tensor normalization but ordinary centered
differences still lost precision in the small H-dependence of a much larger A.
The accepted run keeps the tensor-normalized 2e-6 accuracy gate and uses
Richardson-extrapolated differences over larger steps. The law, physical
parameters and observational cuts were not changed. Source hashes and all
three run statuses are recorded in VERIFICATION.json.
