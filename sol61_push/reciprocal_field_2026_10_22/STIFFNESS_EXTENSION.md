# Positive polarization stiffness: extension of the radius bound

This follow-up was selected after the base-field checks. Add the repository's positive spherical polarization-gradient energy gamma |grad P|^2/2 (equivalently the div/curl form under the appropriate boundary terms), gamma>=0. Do not assume its static state obeys the algebraic law exactly.

Let u=K P_r be signed, g=Phi'>=0, Lp^2=gamma/K, and F(u)=partial W(K|P|)/partial P_r, an odd increasing function with F(u)<0 at u<0. Static variation gives

    -Lp^2 [u''+2u'/r-2u/r^2]+F(u)=g.

With a regular centre u(0)=0 and a nonnegative outer boundary value, u cannot have a negative interior minimum. At that minimum u'=0, u''>=0 and -2u/r^2>0; the left side is strictly negative, contrary to g>=0. The gamma=0 limit gives the same sign directly. This is a conditional sign proof, not existence/uniqueness of a global halo.

Poisson and cold chemical equilibrium imply, without using F's detailed shape,

    Q=r^2(g-u),  Q'=r^2[K rho_b+K chi h],
    Q(0)=0,  0<=Q<=r^2 g=-r^2 h',

while h>0, chi>=chi0 and rho_b>=0. The comparison proof in RESULT.md section 4 therefore goes through unchanged: R_positive_e<=pi ell0. It is enough that the passive polarization boundary makes u nonnegative. Different orientation/boundary states remain outside the claim.

The quasistatic Fourier check also retains the bound on ell0 as an optimistic growth limit. With z=A0 k^2/K>=0 and t=gamma k^2/K>=0, elimination of P gives

    S_gamma=1-z(1+t)/(1+t+z),
    S_gamma-S_0=-t z^2/[(1+z)(1+t+z)]<=0.

Positive polarization stiffness cannot increase the cold self-gravity fraction relative to the previous gamma=0 calculation. It may make S negative at short wavelength (pressure restoration), so those modes require their own dynamical analysis. No existing numerical growth amplitude is claimed as a finite-gamma result.

Pre-execution finite checks: exact Schur derivative including gamma; exact difference and gamma=0 limit; a declared positive-coefficient grid for the sign; reverse the gradient-energy sign as a control. The central-minimum and radial-comparison arguments are mathematical proofs with self-review, not consequences of the finite grid.
