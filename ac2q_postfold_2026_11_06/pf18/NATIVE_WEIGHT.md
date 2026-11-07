# Opposite-family compression can be removed, self-compression remains

Use PF17's continuous BV subclass, compact native coefficient bounds, and
bounded auxiliary rates on the interval in question. Write

    W_sigma=e(theta)+sigma e(r)/(r c)+bounded density,
    A_q=(1-c^2+r c c_r)/2,
    B_q=(1+c^2-r c c_r)/2.

The bounded density includes omega(e) and sigma I_A e(A). The native equations
then give, as diffuse measure identities,

    div_2 D_sigma=A_q W_sigma+B_q W_-sigma+bounded density,
    D_sigma r=-r c^2 W_-sigma+bounded density,
    D_sigma A=r u+sigma c W_P/r.

Choose the positive bounded local weight

    rho(r,A)=exp(integral_(r_star)^r B_q(s,A)/(s c(s,A)^2) ds).

Its derivatives are bounded on the compact hyperbolic coefficient domain.
The product rule with the continuous coefficients is legitimate in the
continuous BV class. The opposite-family coefficient cancels exactly:

    div_2(rho D_sigma)=rho A_q W_sigma+bounded density.   (1)

Terms involving rho_A D_sigma A and the lower-order part of D_sigma r
are bounded under the stated rate bounds. The weight is the reciprocal of
the Riccati mixed-term weight recorded in PF08.

This does not make the acoustic field divergence-bounded. On the genuinely
nonlinear packet domain A_q>0, the remaining divergence contains the same
signed gradient being transported. In particular its Cantor component can
remain rho A_q W_sigma^c. Taking an absolute value or using a renormalization
theorem for bounded divergence at this point would assume away the obstacle.

Equation (1) isolates native self-compression; it does not bound its sign,
prove a unique flow, or define a square of a singular measure. It also does
not rule out a nonlocal construction or a more refined interaction estimate.
