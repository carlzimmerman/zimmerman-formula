# The ideal quadrupole continuum identifies the entire finite-moment kernel

This extends the parent exact continuum moment sum rule. In the class `integral_0^infinity y |f(y)|dy<infinity`, ideal exact knowledge of Q2(e) for every positive external Newtonian field e identifies f=nu-1 up to equality almost everywhere. It does not choose the value of C, provide observed all-e data, or establish stable reconstruction from a finite/noisy window.

Use the parent's full weight `w_e(y)=sqrt(y) F(e/y)`, including both sides of its integrable cancellation shell. Its Mellin transform is

`K(s)=integral_0^infinity q^(s-1) F(q)dq`, `-2<Re(s)<7/2`.

The endpoint limits are `F(q)~q²/10` at zero and `F(q)~-q^(-7/2)` at infinity. Direct algebra gives the following meromorphic expression, with all apparent singularities inside the convergence strip interpreted by their removable limits:

`K(s)=-(2/35)[1+cos(pi s)-sin(pi s)]`

`       *Gamma(s-3)Gamma(7/2-s)/sqrt(pi)`

`       *20s(s-2)/[(2s-5)(2s-1)]`.

## Derivation and endpoint cancellation

Write the parent endpoint polynomials as `Pplus=sum_(n=0)^3 a_n q^n`, `Pminus=sum_(n=0)^3 (-1)^n a_n q^n`, with a=(12,6,1,2). Then F is -2/(35q³) times the difference between Pplus/sqrt(1+q) and sgn(1-q)Pminus/sqrt(|1-q|).

For r=s-3+n, the continued elementary beta integrals are

`Iplus(r)=Gamma(r)Gamma(1/2-r)/sqrt(pi)`,

`Iminus(r)=B(r,1/2)-B(1/2-r,1/2)`

`          =Iplus(r)[cos(pi r)-sin(pi r)]`.

The second identity follows from the two gamma reflection identities. Therefore `Iplus-(-1)^n Iminus=Iplus[1+cos(pi s)-sin(pi s)]`. Applying the beta recurrence to the four coefficients yields

`sum a_n Iplus(s-3+n)/Iplus(s-3)=20s(s-2)/[(2s-5)(2s-1)]`.

The four terms do **not** have a common strip of ordinary individual convergence. The termwise formulas must be understood as finite parts before combination. This can be justified without assigning the divergent integrals arbitrary values: put common cutoffs epsilon,R on every term; subtract each endpoint power series through its divergent orders; evaluate the convergent remainders and elementary integrated subtractions. Their constant parts are the continued beta functions. Because the full endpoint combination is O(q²) and O(q^(-7/2)), all divergent endpoint powers cancel in the finite sum for generic s in the stated strip. The remaining constant is precisely the ordinary convergent integral of the combined F. Analyticity of that integral extends the identity across the removable exceptional points. Integrability at q=1 is separate and unchanged by these endpoint subtractions.

In particular the removable s=1/2 limit gives `K(1/2)=-4pi/35`, independently matching the parent geometric calculation. One must not read the zero trigonometric factor at that point without its cancelling rational pole.

## Injectivity in the correct weighted space

Define x=ln e, z=ln y and `g(z)=exp(2z)f(exp z)`. The finite absolute moment makes g an L1 function. Write the unnormalized response `R(e)=integral f(y)w_e(y)dy`, and set

`h(x)=exp(x/2)R(exp x)`, `k(u)=exp(u/2)F(exp u)`.

The exact response is the ordinary convolution `h=g*k`. The endpoint bounds and shell integrability make k an L1 function. Its Fourier transform is `khat(omega)=K(1/2-i omega)`.

This multiplier is nonzero for every real omega. For omega!=0, neither gamma factor has a pole or zero, both rational denominator factors are nonzero, and the numerator's s and s-2 factors do not vanish. The trigonometric factor factors as `2cos(pi s/2)[cos(pi s/2)-sin(pi s/2)]`; its zeros are real integers of the form 1+2n or real half-integers of the form 1/2+2n. None lies on the indicated line away from omega=0. At omega=0 the removable value is -4pi/35, also nonzero.

Consequently h=0 implies ghat=0. Fourier uniqueness for L1 functions gives g=0 almost everywhere, and hence f=0 almost everywhere. For clarity this last uniqueness step can be obtained using a Gaussian approximate identity: g convolved with every Gaussian has zero transform and an integrable Gaussian-damped Fourier inversion, so it vanishes; those convolutions converge to g in L1. Applying this to a difference of two kernels proves the claimed injectivity. No pointwise smoothness assumption is needed; continuous representatives, when present, then agree everywhere.

The result requires the **entire**, exact continuum. The finite-observable null-family theorem is not contradicted. No finite-domain error estimate, lower bound on the inverse multiplier, observational continuum, or action principle selecting C=32pi is supplied.

## External leaves and checks

Gamma's absence of zeros and reflection formulas were checked against primary NIST DLMF sections [5.2](https://dlmf.nist.gov/5.2) [5.5](https://dlmf.nist.gov/5.5), and beta integral [5.12](https://dlmf.nist.gov/5.12) on 2026-10-06. The beta reduction, endpoint cancellation, convolution and zero-location arguments are derived here. Bounded numerical transform checks are corroboration of the formula, not a proof of every complex s. Parent conventions, the full shell and the absolute-moment hypothesis must remain in any use of this result.
