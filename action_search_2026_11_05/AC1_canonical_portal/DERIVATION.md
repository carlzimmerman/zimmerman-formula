# AC1: homogeneous attraction is supported; full action health remains open

Base AZ40, criteria 688264b14f. Kappa=1/2 FITTED. No adopted action changes.

## Exact homogeneous subsystem

On P=0,Q=1, the polarization potential and its first variations vanish.
Conditioned on remaining on this homogeneous branch, the system is canonical
scalar plus pressureless dust. Set reduced Mpl=1, phi=B*y, N=log(scale factor),
v=dphi/dN, Omega=rho_b/(3H²), z=coth(y),
B=2 sqrt(3(1-beta))/(3 beta), 0<beta<1. Let
V=Vstar sinh(y)^[-2(1-beta)/beta] and lambda=-V_phi/V=sqrt(3(1-beta))*z.
Friedmann gives V/(3H²)=1-Omega-v²/6, and Raychaudhuri gives
H_N/H=-v²/2-3Omega/2. Klein-Gordon and dust conservation then give

    z_N=-(z²-1)v/B,
    v_N=-(3-v²/2-3Omega/2)v+lambda*(3-v²/2-3Omega),
    Omega_N=Omega*(-3+v²+3Omega).

This uses no externally fitted expansion history. The physical interior is
z>1, Omega>0, v²/6+Omega<1. The exact AZ40 branch has
v=B*3 beta/(2z), Omega=1-z^-2. In particular Omega is NOT
(1-z^-2)/(1+beta*z^-2); the latter fails the dust tangency check and is
retained as the negative control specified in the criteria.

The late equilibrium is (z,v,Omega)=(1,sqrt(3(1-beta)),0). Its characteristic
polynomial factors as (x+3beta)^2*(x+3(1+beta)/2). All three rates are strictly
negative on 0<beta<1; endpoints beta=0,1 are excluded. The vector field is
smooth on a neighborhood of this point for fixed beta. The repeated eigenvalue
can introduce polynomial prefactors, not change the negative exponential sign.
Thus the linearization is exponentially stable; nonlinear local attraction
follows by bounding the quadratic remainder with a positive-definite quadratic
form solving the stable linear system's Lyapunov equation. This conclusion is
about the homogeneous autonomous subsystem, not the full field equations.
The boundary z=1 represents y=infinity; attraction means approach in z,v,Omega,
not a finite stationary value of phi. Dust normalization and phase can differ.

The ratio of interest is

    a0²/(kappa² G rho_phi)
      = 2/(1+beta) * (1-Omega-v²/6)/(1-Omega).

It tends to 1 at that equilibrium. Exact finite-time constant w and an exact
finite-time tie remain special-trajectory properties; asymptotic attraction
does not turn them into identities for arbitrary histories.

## Finite corroboration

36 histories cover beta=1/3,2/3,.9, y0=.3,1, exact starts and five specified
1% perturbations. N runs 0..12. Independent DOP853 tolerance levels are compared
on 241 points. Maximum normalized trajectory discrepancy is 5.181e-9; exact
branch tie drift is 3.273e-11. The largest final absolute tie residual among
perturbed histories is 5.785e-8. These are 12 e-fold experiments, not a forecast
for the present universe. No basin size outside these starts was established.

## Fixed-p interaction curvature

Write u=p/a, f(u)=-u-log(1-u), g(u)=2f-u*f', K=4pi G.
At fixed p,

    W_a=a*g/K, W_aa=(g-u*g')/K,
    W_pp=1/[K(1-u)²], W_pa=-u²/[K(1-u)²],
    W_phiphi=W_aa*(a_phi)²+W_a*a_phiphi.

The last term cannot be omitted. A direct high-precision second derivative and
this chain rule agree on 27 frozen fixtures. V_phiphi+W_phiphi and the
polarization-only Schur complement are positive at those fixtures. This is
finite corroboration, not positivity for all u or a metric-constrained spectrum.
In particular the lapse/shift, clock, gradients, switching surface, background
equations and cosmological-to-local matching have not been eliminated here.

## Self-review and exact missing implication

Using proof-audit: primary verdict **correct only after a stated restriction**
for the interpretation as an action-stability claim; the restriction is the
P=0,Q=1 homogeneous scalar/dust subsystem and local late attraction.
Definitions to ODE: passed by Friedmann/Raychaudhuri/KG reconstruction.
Exact branch tangency and characteristic polynomial: passed symbolically.
Finite domain and numerical agreement: passed in frozen range.
Attraction of physical screened backgrounds: not addressed.
Full constrained action spectrum: not addressed.
No independent-agent review claimed. Existing v3s causal/caustic gaps remain.

Reproduce with run.py --out PATH. The evidence/homogeneous/manifest.json records hashes,
versions and bounded execution. initial/ retains the pre-manifest first run.

## Allowing the polarization to respond at fixed external acceleration

This is a conditional source ensemble, NOT the full metric constraint problem.
At fixed A>0, minimize W(p,a)-p*A/K in 0<=p<a. It gives
p=a*A/(a+A), and the effective scalar potential is

    U(a;A)=a²/(xi G)+a²/K*[log(1+A/a)-A/a].

With s=A/a and C=2K/(xi G)>0,

    U_a=(a/K) F(s), F(s)=C+2log(1+s)-s-s/(1+s),
    F'(s)=-s²/(1+s)²<0.

F(0)=C and F tends to minus infinity. There is exactly one positive root s*.
At this root U_aa=s*³/[K(1+s*)²]>0. Since a_phi is nonzero, U_phiphi is
positive at the stationary solution. For kappa=1/2 and beta=1/3,2/3,.9,
s*=74.68707026,91.84851287,103.81841594 (40/80 digit checks agree).
The preferred a=A/s* scales with the external acceleration. This is not a
mechanism fixing a to its cosmic value; spatial gradients and cosmological
boundary/time evolution must be included before making a physical claim.

Off the stationary solution, fixed external A and a tending toward saturation
s>>1 give U_phiphi ~ -A*a_phiphi/K plus subleading logarithmic terms. Here
a_phiphi>0 for the sinh potential, so curvature can be negative. All nine
s=1e4 fixtures have negative curvature; this is NOT a demonstrated on-shell
instability. It explicitly prevents extrapolating the earlier fixed-p finite
positive fixtures into a global stability statement. Removing the positive
source coupling eliminates the positive interior polarization stationary point.

The independent identity tested is
U_phiphi=V_phiphi+W_phiphi-W_piphi²/W_pp. It is a polarization-only Schur
complement, distinct from eliminating the lapse and the clock below.

## All-angle conditional PN constraint model

The Lagrangian and exclusions are explicitly frozen in
EXTENSION_PN_CONSTRAINTS.md. Let D=H+gamma*kvec*kvec^T, n=kvec/k,
Q=n^T D^-1 n, delta=k²(1-Q)-mu². H has eigenvalues greater than 1, so
0<Q<1. The constraint matrix is negative definite exactly when delta>0.
Eliminating its four coordinates gives

    K11=1+v²/delta,
    K12=v*(mu²+k²Q)/delta,
    K22=k²*(mu²+k²Q)/delta,
    det K=(k²+v²)*(mu²+k²Q)/delta.

For mu²>=0 and k>0, K is positive definite iff delta>0. At delta<0 the
determinant is negative; delta=0 is singular and cannot be eliminated.
At mu=0 the condition holds at every angle for the stated H and gamma.
This removes the parallel-only limitation of AZ40's restricted velocity
Hessian, not the remaining full-action restrictions. The finite-mu low-k
boundary lies outside any automatic static/PN interpretation of cosmology.

Let e=(-t,-h*ez) be the coordinate coupling to the constraints. The scalar
entry of the effective potential matrix is

    U11=k²+m²-h²*(ez^T D^-1 ez)
        -(t+h*k*n^T D^-1 ez)²/delta,
    U22=rho_tau*k², U12=0.

The eliminated velocity/coordinate cross matrix is R=-B^T C^-1 E. Its
antisymmetric part G=R-R^T is retained. For G12=g and x=omega²,

 det(U-x*K-i*omega*G)
   = det(K)*x²-[K11*U22+K22*U11+g²]*x+U11*U22.

If K>0 and U>0, the conserved quadratic energy is positive; multiplying the
normal-mode equations by the conjugate velocity proves no exponentially growing
mode in this constant-coefficient conservative system. Alternatively the
polynomial has real positive roots (its discriminant is nonnegative by
K11*K22>K12² and U11,U22>0). If rho_tau>0 and U11<0, the product of x roots
is negative, so one frequency is imaginary irrespective of gyroscopic mixing.
For rho_tau=0 the zero-frequency sector requires separate treatment.

144 frozen fixtures agree between 4x4 matrix inversion and these formulas at
40/80 digits. All have positive K and U; their roots satisfy the direct
frequency determinant. The deliberately excessive mu² control fails kinetic
positivity. A separate exact U=diag(-1,1),K=I,G12=1 control yields
x²-x-1=0, with one negative root. Decoupling t=h=v=mu=0 gives independent
omega_phi²=k²+m² and omega_sigma²=rho_tau*(1-Q)/Q.

This model keeps mass/mixing terms that AZ40 omitted, but t,m,h are NOT yet
fixed by a complete on-shell charged background. In particular it is incorrect
to promote the favorable fixture count to a healthy covariant action.
