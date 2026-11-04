# Curvature-only Gaussian action and fixed-filter virial

This is a new application of the known generalized QUMOND architecture, not a new architecture. The kernel and action distinction is documented in KT41/nonlocal. Keep p=9/8, ell=3 kpc, Q(0)=0 and Q'(z)=nu_simple(sqrt(z)), R=Q/z.

Let g=grad psi remain unfiltered, Hbar=T_a Hess psi=Hess T_a psi in Euclidean space, where T_a=exp(a² Delta/2) is the fixed isotropic Gaussian convolution. Put x=g.g/a0², s=ell² Hbar:Hbar/a0², E=g.g R(x+s^p). The static action is

    I=int[-rho Phi-(2 grad Phi.grad psi-E)/(8piG)]d³x.

Its full variation gives Delta psi=4piG rho and

    A=(R-1+xR')g,
    Bbar=p ell²s^(p-1)xR' Hbar,
    Delta Phi=Delta psi+div A-partial_i partial_j(T_a*Bbar)_ij.

The tensor filter acts on Cartesian components. Smoothing radial/tangential orthonormal components independently would not give T_a H. A finite implementation using H_h T_h psi must use the adjoint of that entire composite. This continuum calculation instead obtains Hbar by differentiating the correctly filtered potential.

For a fixed uniform external Newtonian gradient e, background and linear tangent subtraction are as in KT40. The attractive-positive scalar virial is

    W_ph=(1/(4piG))int[(A-A_ext).delta g+Bbar:T_a delta H]d³x,

where delta denotes centered mass-preserving compression rho_lambda(r)=lambda³rho(lambda r), holding e and filter length a fixed. For the source scale b_lambda=b/lambda,

    delta g=2g+r g',
    T_a delta H=3Hbar+r partial_r Hbar+a partial_a Hbar.

The last term cannot be discarded. Equivalently compute -b partial_b Hbar at fixed a, as done below. No output filter is omitted: the adjoint is transferred onto delta H by self-adjointness inside the virial pairing.

## Exact filtered Plummer representation

For a Plummer source of scale b and mass M,

    rho_b(r)=3M/(4pi b³)(1+r²/b²)^(-5/2)
            =M int_0^infinity e^(-t) G_sigma0(t)(r) dt,
    sigma0(t)²=b²/(2t),
    G_sigma(r)=(2pi sigma²)^(-3/2) exp[-r²/(2sigma²)].

This equality follows by the Gamma(5/2) integral. Gaussian convolution replaces sigma0² by v(t)=a²+b²/(2t), so it preserves positivity and mass. Differentiation commutes with convolution for the smooth Plummer source. With P(t,r)=gammainc(3/2,r²/(2v)), the normalized enclosed Gaussian mass,

    Hbar_tt = GM int e^-t P/r³ dt,
    Hbar_rr = GM int e^-t [sqrt(2/pi) v^-3/2 exp(-r²/(2v))-2P/r³] dt.

Both tangential eigenvalues coincide. These are eigenvalues of the **filtered Cartesian Hessian**, not independently smoothed eigenvalues.

Under source compression, dot v=-b²/t=-2chi with chi=b²/(2t). Direct differentiation gives

    dot Hbar_tt=GM int e^-t sqrt(2/pi) chi v^-5/2 exp(-r²/(2v)) dt,
    dot Hbar_rr=GM int e^-t sqrt(2/pi) chi v^-5/2 exp(-r²/(2v)) (1-r²/v) dt.

This incorporates the fixed-filter scale variation exactly. At a=0 both the filtered Hessian and these variations reduce to analytic Plummer expressions. Numerically t=exp(u), with u in [-32,8], and Simpson integration includes the Jacobian t.

## Axisymmetric scalar integral

The unfiltered self gradient is g=GM r/(r²+b²)^(3/2). Let mu be the cosine relative to e, and x=(g²+e²+2ge mu)/a0². With C=R-1+xR', D=p ell²s^(p-1)xR', A_ext=[nu(e/a0)-1]e,

    V_A=(1/(6GM))int r²dr int dmu [C(g+e mu)-A_ext mu]delta g,
    V_B=(1/(6GM))int r²dr int dmu D[Hbar_rr dot Hbar_rr+2Hbar_tt dot Hbar_tt],
    V=pi GM/(32b)+V_A+V_B = W/(3M).

Negative V is retained and means the imposed profile cannot satisfy stationary scalar virial balance with nonnegative kinetic energy. Positive V alone does not establish equilibrium or an observed line-of-sight fit.

Controls compare the Gaussian-mixture formulas to analytic unfiltered Plummer fields, reproduce stored KT40 signed virials at a=0, refine radial/angular/mixture quadratures and outer radius, and difference the actual energy at b exp(+-h) with a fixed. The energy derivative is independently formed from values of E, rather than the A/B derivative formula. A mutation that pairs Bbar with the unfiltered delta H must disagree for a=.3 kpc; this catches omission of the composite adjoint.
