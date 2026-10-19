# A photon-regulator diagnostic, not a curvature identification

FSP-009 coordinator candidate, independently derived before the new worker packet. This resumes an observation in the clean common review: a mass for the photon produces an infrared nonanalyticity fixed by the complete soft non-Born polarizability action. It does not provide the full unknown mass response at zero regulator. The coefficient and its audit are preserved separately rather than modifying any earlier science.

Put s=lambda_gamma^2 and work at first order in u, infinite volume, fixed positive QCD pion mass and fixed mass-independent ultraviolet parameters. A conserved-current contraction uses D_s(Q)=1/(Q^2+s). Let f(s)=M_u^NB(s)/M and C=3(a-b)/(32pi M), with a=alpha_E/u,b=beta_M/u. The massless radial density has g(t)=2Ct+O(t^2), t=Q^2, so its local contribution through a fixed small cutoff L is

    f_local(s)=2C integral_0^(L^2) t^2/(t+s) dt
              =C L^4-2CsL^2+2Cs^2 log[(L^2+s)/s].

Consequently its s^2 log(s) coefficient is -2C. Unknown analytic constant, s and s^2 terms are removed by

    P3(D)=D(D-1)(D-2)=s^3 d_s^3, D=s d_s,
    C=-lim_(s->0) s f'''(s)/4.

The differentiated propagator supplies a UV-convergent infrared filter rather than a numerical fit. On the leading radial density its normalized weight is 3s t^2/(t+s)^4, whose integral over t>=0 is one. Higher soft terms and the hard tail still need a controlled differentiated remainder. A finite cutoff changes the convergence rate, not the limiting coefficient when those bounds hold.

## Starting from the full proton mass

The parent's complete Born kernel is B(z)=1+c z^2+d z^3+..., z=Q/(2M), d=2+6kappa+3kappa^2/2. Its linear z term cancels only after the non-pole Born subtraction is included. With P_s=Q^2/(Q^2+s), the Born regulator dependence has half-integer powers s^1/2 and s^3/2 and

    c_log,B=-d/(64pi^2 M^4)

as the coefficient of s^2 log(s). The missing z term means there is no s log(s) at this order. The coefficient d is independent of the radius slopes; c is not. For the complete fractional mass response F(s)=M_u(s)/M, define

    P5(D)=D(D-1/2)(D-1)(D-3/2)(D-2).

It kills the lower Born half powers and analytic constant/s/s^2 terms, while P5[s^2 log(s)]=(3/2)s^2. If the complete expansion and differentiated remainder hold, then

    C=-d/(128pi^2 M^4)-(1/3)lim_(s->0) P5(D)F(s)/s^2.

This candidate requires an independent source/normalization/remainder audit. It may make a soft non-Born quantity accessible from the full mass-regulator response with kappa as a separate input, rather than requiring form factors at all virtual momenta. It leaves F(0), the full zero-regulator mass derivative, unknown. Choosing a photon-mass-dependent retuning prescription changes the problem; the stated ultraviolet path is essential.

## Coordinate representation and physical limits

For x-distance r, D_s(r)=sqrt(s) K1(sqrt(s)r)/(4pi^2 r). Differentiating its Schwinger representation gives

    partial_s^3 D_s(r)=-r^2 K2(sqrt(s)r)/(32pi^2 s).

Thus the third derivative can be implemented as a current-correlator kernel, retaining its vacuum subtraction, contact terms and tensor contraction. It does not require reconstructing a spectral function by an inverse transform. Its exact external-state normalization remains the programme's full-current convention.

The volume/zero-mode and charged-state limits are part of this proposed observable. At finite volume a retained photon zero mode can produce inverse-s artifacts, which these projectors do not remove. Infinite volume must be controlled before the zero-mass limit, or the zero-mode prescription and corrections must be explicit. lambda_gamma is a regulator; setting it equal to H would not compute the unconditioned curved-space QCD vacuum. The known Born term linear in lambda_gamma is a mass-regulator effect, not evidence for the target A_rho H vacuum term.
