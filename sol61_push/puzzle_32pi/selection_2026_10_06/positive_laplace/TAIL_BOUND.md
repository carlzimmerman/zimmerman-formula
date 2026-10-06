# Ellipticity forces a minimum unmeasured tail

Same base and target as REPORT.md. This is a second executed route: extract a necessary measurable constraint after the analytic selector fails. It uses the existing symmetric NR dictionary and sector-only vacuum convention C=integral_0^infinity y e(y)dy, not a universal cosmological theorem.

Let e(y)>0 be C1 for y>0, f(y)=y e(y), and require the full NR action's radial ellipticity D(y)=1+2f'(y)>0. If C is finite, then for every Y>0,

    C > integral_0^Y y e(y)dy + [Y e(Y)]^2.                 (1)

The nonstrict version remains valid with D>=0, e>=0. To prove it, put h=f(Y)>0. For 0<t<2h, integrating f'>-1/2 gives f(Y+t)>h-t/2. Integrate this triangle: its area is h^2. The remaining tail is nonnegative. Strict inequality follows from strict D on a nonempty interval. No higher-derivative bounds, monotonic e, analytic continuation, or fitted cutoff shape enter this proof.

If only e(Y) is known and e is nonincreasing, e(y)>=e(Y) on 0<y<Y. Consequently the weaker one-point condition is

    C > Y^2 e(Y)[1/2+e(Y)].                                (2)

At fixed positive target C, this yields the strict upper endpoint bound

    e(Y) < [sqrt(1+16C/Y^2)-1]/4.                           (3)

It constrains a single inferred isolated-spherical response value under this action dictionary. It is not an observational extraction from disc or planetary data. For noisy e and a measured window, lower confidence envelopes can be integrated in (1) only with a joint error model, including source mass, a0, isolation and geometry. Pointwise nominal errors are insufficient for a certified confidence bound.

## Exact P2 persistence is limited

Suppose the exact response e(y)=a(y)=sqrt(1+1/y)-1 holds on the entire interval (0,Y]. Its accumulated integral is

    P(Y)=(Y+1/2)sqrt(Y^2+Y)/2-Y^2/2
         -log[2Y+1+2sqrt(Y^2+Y)]/8.

Both P(Y) and f(Y)=1/[sqrt(1+1/Y)+1] increase strictly. Therefore P(Y)+f(Y)^2 has one crossing of 32pi. It occurs at

    Y*=202.112560248705598869062256563406160434.

If C=32pi and D>0 globally, exact P2 persistence must end before Y*. Even equality at Y* cannot be attained by strictly elliptic positive kernels, since (1) is strict. The rule does not predict that a cutoff starts exactly there, or select a particular interpolation. A kernel can depart from P2 at smaller y and then contribute additional positive area elsewhere; the analytic counterfamily shows why that remaining freedom is substantial.

With only a P2 response value at Y and monotonicity, the weaker (2) crossing is separately computed by the script. It should not be confused with the full-prefix crossing.

## Relation to the earlier orbital sum rule

The measured isolated-spherical orbital partial integral is O(Y)=1/4 integral_0^Y y nu(R-1)dy. Under its endpoint convention, integration by parts gives O(Y)=integral_0^Y y e dy-Y^2 e(Y)/2. Thus the strengthened bound is C>O(Y)+Y^2 e(Y)/2+[Y e(Y)]^2. All quantities must refer to the same isolated spherical action, source mass and a0. This is a stronger necessary condition when nu at the upper endpoint is also inferred; it does not remove unmeasured high-y freedom or an independent additive vacuum term.

## Sharpness and next test

The limiting linear tail f(Y+t)=[h-t/2]_+ saturates the area h^2 but has D=0 on its support and compact endpoints. It is excluded by strict ellipticity. Smooth, nearly saturating tails can approach the bound, so demanding strict positivity alone supplies no fixed quantitative extra margin. A specified uniform D>=d0>0 would change the tail-area bound to h^2/(1-d0) for 0<=d0<1. If d0>=1, positive f cannot decay sufficiently and the integral diverges. The physical next test is therefore either a measured weighted partial integral or a microscopically justified quantitative ellipticity/tail margin; another arbitrary cutoff fit cannot close the puzzle.
