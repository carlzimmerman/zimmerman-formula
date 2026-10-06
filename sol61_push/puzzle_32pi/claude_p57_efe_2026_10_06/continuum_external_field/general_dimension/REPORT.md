# General-dimensional continuum quadrupole bridge

For every integer spatial dimension n>=3, the formal n-dimensional QUMOND point-source operator has a finite, positive all-external-field quadrupole coefficient:

    integral_0^infinity e^(-p) Q_n(e)de = (a0/r_M) D_n C,
    p=1/(n-1), C=integral_0^infinity y[nu(y)-1]dy,
    D_n=c_n K_n > 0.

Here Q_n is the Hessian difference of the negative anomalous potential, as defined below. The desired Mellin index is s=1-p=(n-2)/(n-1). The three-dimensional coefficient is D3=9pi/35; D4=18/35. Thus this continuation has no dimensional divergence or blind vacuum moment for n>=3. It is a universal classical operator bridge, not a principle selecting n, C, or 32pi. No physical continuum of external fields is observed or constructed here.

## Force and Green normalization

Define the normalized central force by g_N=mu_n/r^(n-1), r_M=(mu_n/a0)^(1/(n-1)), and t=g_N/a0=(r_M/r)^(n-1). If Delta Phi_N=kappa_n rho, Gauss' law gives mu_n=kappa_n M/Omega_(n-1), where Omega_j=2pi^((j+1)/2)/Gamma((j+1)/2). This is a force normalization, not an identification with the Einstein-Hilbert coupling in arbitrary dimension.

Use G=-a0 t rhat+a0 e zhat, f(y)=nu(y)-1, D=f(|G|/a0)G-f(e)a0 e zhat, and Delta psi=div D. Explicitly psi=-Phi_p: the physical anomalous acceleration is grad psi. The physical potential Phi_p has the opposite Hessian sign. Write the degree-two zonal harmonic as Y2(mu)=mu^2-1/n. Define psi_2=A r^2Y2 in a source-free inner neighborhood, and Q_n=psi_zz-psi_xx=2A. In n=3, Phi_Q=-(Q2/2)r^2(mu^2-1/3), so Q_n=+Q2. This agrees with the actual Claude solver, Q2=3 times its coefficient of r^2P2 in psi.

The angular norm is N2=integral Y2^2 dOmega=Omega_(n-1) 2(n-1)/[n^2(n+2)]. The radial equation is

    psi_2''+(n-1)psi_2'/r-2n psi_2/r^2=s2(r),
    s2=integral (div D)Y2 dOmega/N2.

Its homogeneous solutions are r^2 and r^(-n), and their Wronskian is -(n+2)r^(1-n). With the regular/decaying Green choice,

    A=-1/(n+2) integral_0^infinity s2(r)/r dr.

Compact annular kernel perturbations make the boundary manipulations unambiguous. The response extends to the stated absolute-moment class by the integrability argument below. Radial and angular integration by parts give

    A=-1/[(n+2)N2] integral r^(-2)
                   [n D_r Y2-D_tangent dot grad_S Y2] dr dOmega.

The n in this bracket is loadbearing: it comes from differentiating r^(-n) in the radial divergence term.

## Exact angular weight

Set xi=-mu, y=sqrt(e^2+t^2+2et xi), h=(n-3)/2, and

    H_n(t,xi)=n t(xi^2-1/n)+e xi[(n+2)xi^2-3].

The bracket above becomes -a0 f H_n. The radial measure is r^(-2)|dr|=t^(p-1)dt/[(n-1)r_M], while dOmega=Omega_(n-2)(1-xi^2)^h dxi. Therefore

    Q_n(e)=(a0/r_M)c_n integral f(y)W_n,e(y)dy,
    c_n=n^2 Omega_(n-2)/[(n-1)^2 Omega_(n-1)],
    W_n,e(y)=integral_|y-e|^(y+e) (y/e)t^(p-2)
                     H_n(t,xi(y,t))(1-xi(y,t)^2)^h dt.

This is the full angular weight, on either side of y=e. Rescaling t=y tau gives W_n,e(y)=y^p F_n(e/y). In n=3, H3 is minus the parent's raw quadrupole bracket, W3=-2 w_parent, and c3=9/8. Thus the physical Q3 prefactor is -9a0/(4r_M), reproducing both the raw operator and the earlier sum-rule sign.

## Convergence without dimensional guesswork

For q near zero, change tau=1+qz, -1<=z<=1. The angular factor has a uniformly analytic binomial expansion after factoring (1-z^2)^h. The constant quadrupole vanishes by isotropy and the linear term by parity, so F_n(q)=O(q^2).

For large q, tau=q+z and

    xi=-1+(1-z^2)/[2q(q+z)],
    1-xi^2=q^(-2)(1-z^2)(1+z/q)^(-1)
                        [1-(1-z^2)/(4q^2(1+z/q))].

Expansion gives H_n=(n-1)z+(n+3)(1-z^2)/(2q)+O(q^(-2)). The leading odd contribution integrates to zero. Consequently

    F_n(q)=b_n q^(p-n-1)+O(q^(p-n-2)),
    b_n=(n-1)(1+p) B(1/2,(n-1)/2)/n >0.

This recovers F3=-2F_parent approximately 2q^(-7/2). Near q=1 the t=|1-q|z boundary layer instead gives

    F_n(q)=sgn(q-1) a_n |q-1|^(p-1)+less singular terms,
    a_n=(n-1)(1+p) B(1-p/2,(n-1)/2)/[2(n+1-p)] >0.

Both one-sided singularities are integrable because p>0. The point value at q=1 is immaterial. Thus integral q^(s-1)|F_n(q)|dq is finite on the strip -2<Re(s)<n+1-p, which contains s=1-p.

There is also an independent absolute-convergence proof for the computation of K_n, avoiding dependence on asymptotic cancellations. Put t=e rho before integrating the fixed-y shell. The double integral for K_n below has absolute convergence at rho=0 and infinity because 0<p<1. Around rho=1, xi=-1 its denominator is comparable to (rho-1)^2+(1+xi). Even bounded numerator times angular weight (1+xi)^h is integrable: integrating rho gives an upper bound proportional to (1+xi)^(h-1/2), and h>=0. Every order change used next is therefore legitimate.

## Exact all-field coefficient

Let K_n=integral_0^infinity q^(-p)F_n(q)dq. Equivalently insert delta(1-sqrt(e^2+t^2+2et xi)) into the original t,xi expression and integrate e. The change t=e rho has Jacobian e; it yields exactly

    K_n=integral_0^infinity rho^(p-1)drho integral_-1^1
       (1-xi^2)^h [n rho(xi^2-1/n)+xi((n+2)xi^2-3)]
                           /(1+rho^2+2rho xi) dxi.

For theta=acos xi and 0<a<2,

    integral_0^infinity rho^(a-1)/(1+2rho cos(theta)+rho^2)drho
       =pi sin[(1-a)theta]/[sin(pi a)sin(theta)].

It follows first for 0<a<1 by partial fractions and the Euler beta integral, with conjugate roots off the positive axis; analyticity and absolute convergence extend it across a=1 to 0<a<2, with the removable value taken there. Our exponents are a=p and a=1+p, both strictly inside this range.

After these two rho integrals,

    K_n=pi/sin(pi p) integral_0^pi sin^(n-3)(theta)
       [(n cos^2(theta)-1)sin(p theta)
       +cos(theta)((n+2)cos^2(theta)-3)sin((1-p)theta)]dtheta.

Define G=sin^(n-1)(theta)[(n+2)cos^2(theta)-1]. Its derivative is (n+1)sin^(n-2)(theta)cos(theta)[(n+2)cos^2(theta)-3]. Splitting sin((1-p)theta) and integrating G' by parts, with zero endpoint G, reduces the expression to

    K_n=pi(1-p^2) J_(n-1)(p)/[(n+1-p)sin(pi p)],
    J_m(p)=integral_0^pi sin^m(theta)sin(p theta)dtheta.

For integer m, an entirely elementary evaluation is supplied by

    J0=(1-cos(pi p))/p,
    J1=sin(pi p)/(1-p^2),
    J_m=m(m-1)J_(m-2)/(m^2-p^2), m>=2.

The recurrence follows by two integrations by parts; the relevant sine-power boundary terms vanish for m>=2. Combining this with gamma reflection/duplication gives the convenient closed form

    K_n=pi^2(1-p^2)Gamma(n)/
       [2^n(n+1-p)cos(pi p/2)
                   Gamma((n+1+p)/2)Gamma((n+1-p)/2)].

Every factor is positive and finite for every integer n>=3. This is an analytic universal statement, not inferred from the tested finite dimension range. Direct gamma simplification gives K3=8pi/35, D3=9pi/35, and D4=18/35. Representative D5=0.3803552165, D6=0.3030058177; the calculation is not searching dimensions for 32pi.

## Fubini and scope of the physical arrow

Assume the same measurable f applies to every e>0 and integral y|f(y)|dy<infinity. At the required Mellin index,

    integral de e^(-p) integral dy |f(y)|y^p|F_n(e/y)|
          =[integral y|f(y)|dy][integral q^(-p)|F_n(q)|dq]<infinity.

Tonelli/Fubini gives the initial sum rule with D_n=c_nK_n. Therefore equality of the ideal continuum Q_n functions implies equality of C in this class for every n>=3. Neither full-kernel injectivity nor an inversion theorem is asserted.

The construction only continues the classical QUMOND field operator to formal spatial dimension n. It does not prove that any covariant completion has vacuum coefficient C=integral yf in that dimension, and it does not identify the force-normalized mu_n with an arbitrary gravitational action parameter. Even in n=3, the physical vacuum normalization remains a separate action-dependent arrow. Observed external acceleration is e nu(e); its integration measure requires a kernel-dependent Jacobian. There is no independently controlled physical continuum of all external fields, and finite measurements retain the earlier compact-support moment freedom. No numerical value of C is selected, and the dimensional extension alone supplies no preference for d=4.

## Validation and sources

The bounded computation tests exact sphere normalization, n3 raw weight and prefactor, angular integration-by-parts algebra, J recurrence and independent angle quadrature for n3 through12, rho-integral factors, both full-weight branches in n3, and shell limits at n3,4,6. Forty assertions pass; three intended controls fail wrong Hessian normalization, vacuum blindness, and reuse of the three-dimensional Mellin index in n4. Numerical quadrature is not interval certified and does not replace the universal analytic proof.

The field law is inherited from the pinned parent QUMOND sources and exact operator; the n-dimensional Green solution is derived here. Gamma recursion, reflection and duplication are checked against [DLMF5.5](https://dlmf.nist.gov/5.5), especially equations5.5.1,5.5.3,5.5.5; all arguments used are positive and away from poles. Exact source/input records are in sources.json/provenance.json. No novelty claim, orbit integration, observational exclusion or peer-file modification is made.
