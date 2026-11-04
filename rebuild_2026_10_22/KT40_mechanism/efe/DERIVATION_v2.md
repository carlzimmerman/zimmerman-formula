# Scalar virial in a fixed uniform external field

Fix p=9/8, ell=3 kpc and the KT39 action, and write the auxiliary Newtonian
potential as psi_self+e.z. The Plummer source is spherical and centered;
e is a prescribed constant auxiliary Newtonian gradient, not necessarily the
physical external acceleration. Because H_ext=0, its physical uniform field
is nu_simple(e/a0)e. No orbit or Galactic environment is fitted here.

Let f(g,H)=E(g,H)-g.g, with

    E=a0² x R(x+s^p), x=g.g/a0², s=ell² H:H/a0²,
    A=.5 f_g=[R-1+xR']g,
    B=.5 f_H=p ell² s^(p-1)xR'H.

For e>0 use the background-subtracted functional

    U_ph[rho;e]=-(1/(8piG)) integral [f(e+g_self,H_self)
                     -f(e,0)-2 A(e,0).g_self] d³r.

The linear tangent is necessary for absolute convergence before angular
integration: g_self=O(r^-2), while the quadratic remainder is O(r^-4).
For the centered spherical source its angular integral is zero exactly.
For e=0 the usual isolated deep-MOND energy has a logarithmic far-field
term independent of the Plummer scale at fixed mass. Work with its difference
or homology derivative, not a finite absolute isolated energy.

For a centered compact or sufficiently decaying density variation, with the
external boundary gradient held fixed, integration by parts twice gives

    delta U_ph=-(1/(4piG)) integral [(A-A_ext).grad(delta psi)
                                      +B:Hess(delta psi)] d³r
              =(1/(4piG)) integral delta psi [div A-double_div B] d³r
              =integral Phi_ph delta rho d³r.

This uses Delta(delta psi)=4piG delta rho and Delta Phi_ph=div A-double_div B.
It retains the Hessian term; no approximation to an algebraic MOND force is
introduced. For the Plummer homology below, delta psi=O(r^-3), so the Green
surface terms vanish even with isolated logarithmic Phi_ph. At the origin
all source fields and the homology variation are regular. Uniform physical
external acceleration contributes zero scalar virial because integral rho r
vanishes. This identity prescribes a static virial; it does not prove existence
of a stationary distribution function.

## Fixed-mass homology

Take rho_lambda(r)=lambda³ rho(lambda r), equivalently a_lambda=a/lambda.
The external gradient e is held fixed. The self field transforms as

    psi_lambda(r)=lambda psi(lambda r),
    g_lambda(r)=lambda² g(lambda r),
    H_lambda(r)=lambda³ H(lambda r).

Consequently, at lambda=1,

    delta g_self=2g_self+(r.grad)g_self,
    delta H_self=3H_self+(r.grad)H_self,
    delta rho=div(rho r).

Using the attractive-positive sign convention for the scalar binding virial,
write W=integral rho r.grad Phi. Its sign is not assumed positive.
We have dU/d(log lambda)=-W. Therefore the anomalous contribution is

    W_ph=(1/(4piG)) integral [(A-A_ext).delta g_self
                                      +B:delta H_self] d³r.

In stationary scalar virial balance, 2K=W; define the trace-averaged one-axis
variance sigma_bar²=W/(3M). It is the mean of the three global velocity
variances, not a direction-specific line-of-sight prediction when e!=0.
The baryonic and tracer Plummer shapes coincide in this fixed diagnostic.

## Axisymmetric reduction without a second Poisson solve

Let g(r)=GM r/(r²+a²)^(3/2), gp=g', gt=g/r, mu=cos(theta) relative to e.
The self Hessian has eigenvalues (gp,gt,gt), even though the total gradient
is g n+e ez. Put

    x=(g²+e²+2ge mu)/a0²,
    s=ell²(gp²+2gt²)/a0², z=x+s^p,
    C=R-1+xR', D=p ell² s^(p-1)xR',
    A_r=C(g+e mu), B_rr=D gp, B_tt=B_pp=D gt,
    delta_g=2g+r gp,
    delta_Hrr=3gp+r gpp,
    delta_Htt=delta_Hpp=2gt+gp.

The exact reduced scalar integral is

    sigma_ph²=(1/(6GM)) integral_0^infinity r² dr integral_-1^1 dmu
      [(A_r-A_ext mu)(2g+r gp)
       +D gp(3gp+r gpp)+2D gt(2gt+gp)].

The Newtonian piece is sigma_N²=pi GM/(32a). The code stores the separate
A and B contributions and adds this exact Newtonian value. Negative total
variance, if encountered, is reported rather than converted to a pass.
For e=0 the angular integral is exactly twice its radial value, reproducing
the independent KT39 radial full-force/weak/energy virial. This is a strong
normalization and sign control on the reduction.

## Numerical checks and scope

The production quadrature uses logarithmic radius and Gauss-Legendre mu.
All 41 original Upsilon values are retained for Draco, Sculptor, Leo II and
Fornax, both original a0 footings, eta=[0,.1,.3,1,3]. Three radial/angular/domain
settings are declared before execution. Every eta0 result is compared to the
accepted full radial KT39 result; all settings must agree within .02 km/s.

A separate compact-domain control directly differences the actual energy
at a*exp(±h), h=1e-4, using a 40-digit implementation of the closed primitive

    y=sqrt(z),
    Q(z)=y²/2+(y+2)sqrt[y(y+4)]/2-4 asinh(sqrt(y)/2).

The domain [0.01a,10a] and quadrature nodes stay fixed during the variation.
This avoids invoking a divergent isolated absolute energy, while testing the
full homology derivative rather than restating the A/B integrand. It also
avoids double-precision subtraction of an almost constant external energy.
The relative comparison gate is 1e-5. Newtonian mutation and independent
Newtonian Plummer virial integration supply additional controls.

A trace virial does not identify the tensor velocity dispersions, arbitrary
line-of-sight projection, actual external field, Galactic tides, or equilibrium
existence. The old two-sigma object comparison applied to sigma_bar is labeled
an orientation-averaged screen. It is useful to falsify a universal claim that
an external field only lowers this model's isolated scalar dispersion, but
not to declare a satellite explained without its anisotropic dynamics.
