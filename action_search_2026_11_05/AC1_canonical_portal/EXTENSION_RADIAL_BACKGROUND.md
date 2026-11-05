# AC1 extension: coupled radial quasistatic boundary-value model

Frozen before computation. This tests whether scalar gradient response can keep
a near its cosmological boundary value despite the local stationary tendency
found above. It is not a globally on-shell relativistic solution. Homogeneous
time derivatives are frozen at their background values; lapse, expansion and
clock backreaction on those derivatives are omitted. Fixed spherical positive
source; no galaxy data or FN6 engine used.

Use x=r/R, normalized p=a_bar*u, a=a_bar*A(psi), psi=phi/Mpl,
B=2sqrt(3(1-beta))/(3beta), psi_bar=B, q=(1-beta)/beta,
A=[sinh(psi/B)/sinh(1)]^(-q), V/Vbar=A²,
xi=2*kappa²/(1+beta), kappa=1/2, epsilon=2*(a_bar*R/c²)².
Set psi=psi_bar+epsilon*d. Positive fixed baryonic acceleration
b(x)=mass*x/(1+x²)^(3/2). Poisson gives g/a_bar=b+u.
With the radial switched stiffness active, l=Lstar/R:

 u''+2u'/x-2u/x²=(2/l²)*(u²/(A-u)-b),
 d''+2d'/x=(4pi/xi)*[(A²)_psi-(A²)_psi at psi_bar]
              + A*A_psi*[2f(u/A)-(u/A)*f'(u/A)],
 f(z)=-z-log(1-z).

The subtraction is the explicitly frozen homogeneous KG source, not a claim
that a static configuration with evolving DE solves every field equation.
The switch assumed on requires u'+2u/x>=0 on the resulting profiles.
All solutions must have 0<u<A for x>0; do not clip the physical solution.
At epsilon=0 the d equation is the scalar linear response coefficient; u is
fixed-a, and actual delta psi is zero. At finite epsilon this is coupled.

Finite domain x in [1e-4,20], BC u'=u/x at inner boundary, d'=0 inner;
u equals the algebraic no-stiffness value at x=20, d(20)=0. These are explicit
finite-box BC, not proof of asymptotic matching. Use solve_bvp with initial
mesh 400, max_nodes 20000, tol 1e-5 and independent tol 1e-7 on mesh800.
Compare profiles on 301 points: normalized discrepancy <1e-4; residual and
BC norm below stated solver tolerances. Failure to converge is NO VERDICT.
No changing tolerances after observing results. Source smooth, finite total
mass; outer scalar condition is imposed, not inferred.

Fixtures beta=2/3,.9; mass=1,100; l=.1,.3; a_bar R/c²=0,1e-4,1e-3,
24 models each at two tolerances. Report actual counts and rejected solutions.
Measure fractional changes in a and in g, sign of switch, and scaling of
finite-epsilon correction against the zero-epsilon response. No magnitude
threshold constitutes observational acceptance. If nonlinear branch fails,
report location/condition and preserve attempted result.

Known answers: epsilon=0 decouples the polarization from d, and the radial
Laplacian of d=(x²-20²)/6 is 1, with regular center. Negative control reverse
the scalar source; its correction must reverse at epsilon=0. Also check
numerical d against independent radial Green integration on the fixed-a
profile (inner Neumann flux zero, outer Dirichlet zero) to normalized 1e-4.
This is a candidate background construction, not full G0 or complete action.
