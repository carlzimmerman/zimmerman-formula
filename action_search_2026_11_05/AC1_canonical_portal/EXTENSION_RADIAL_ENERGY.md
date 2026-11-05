# AC1 radial energy second variation, frozen before execution

Same finite-box quasistatic model as EXTENSION_RADIAL_BACKGROUND, no new
background or observational claims. Test its static energy, not physical
oscillation frequencies. Clock/shift/expanding-background dynamics remain open.

Normalized radial energy after the spherical Newtonian potential is eliminated:
 integral x² dx [A² f(u/A)-u²/2-b*u + l²/4*(u'+2u/x)²
       +psi'^2/(2epsilon)+(4pi/xi)*(A²-(A²)_psi,bar*(psi-psi_bar))].
The source subtraction is linear, so has no second variation. Check its two
Euler equations reproduce the frozen radial BVP. Rescale scalar perturbation
as delta psi=sqrt(epsilon)*chi, including the epsilon->0 limiting Hessian.
Let z=u/A, g=2f-z*f', gp=-z²/(1-z)².
Hessian potential coefficients:
 Dpp=(1-z)^(-2)-1;
 h=W_upsi=-z²*A_psi/(1-z)²;
 M=(4pi/xi)*(A²)_psipsi+(g-z*gp)*A_psi²+A*g*A_psipsi.
Quadratic form is integral x² [Dpp*du²+l²/2*(du'+2du/x)²
                  +chi'^2+epsilon*M*chi²+2sqrt(epsilon)*h*du*chi] dx.

Discretize this form directly by piecewise-linear finite elements, midpoint
integration; 200 and 400 intervals on [0,20]. du(0)=du(20)=0, chi(20)=0;
regular scalar center has natural zero flux. Extend the already solved
background from x=1e-4 to zero by u~x, d constant. This changes the numerical
inner model explicitly; convergence does not prove full on-shell matching.
The norm matrix is the same midpoint discrete integral of x²(du²+chi²);
if midpoint underintegration makes it singular, use exact element integration
for that norm, and report this implementation choice before numbers.
Use exact element integration of x² times basis products for the norm from
the start. Lowest generalized eigenvalue measures sign of discrete static
energy, NOT a dynamical frequency because du is a constraint variable.

24 frozen backgrounds, 2 energy meshes; compare minimum eigenvalues to relative
1e-3 using max(abs(lambda_fine),1e-10) in denominator. Known answer pure
massless scalar in ball with outer Dirichlet: pi²/20², relative error<1e-3 at
400 intervals. Reverse scalar gradient sign as negative control at epsilon=0,
which must give negative lowest eigenvalue. Record any negative main eigenvalue
without changing tolerance. Analytic local Schur lower potential
M-h²/Dpp is a diagnostic, not a continuum certificate from sampled values.
Use one thread; no heavy queue needed for matrices of dimension <=800.
