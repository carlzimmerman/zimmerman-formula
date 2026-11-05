# AC1: canonical potential portal, attraction and algebraic mass response

Base checkpoint: 672291043450354f2620f24259058baada3c04be.
Owner authorized continuation toward a healthy action on 2026-11-05.
Scope is action_search_2026_11_05/AC1_canonical_portal only; do not edit AZ43/FN6.
No downloads, new observational claims, or replacement of adopted action.
Kappa=1/2 FITTED. Not theory closed.

Target: discriminate whether AZ40's exact constant-w density tie requires
permanent fine tuning of homogeneous initial conditions, and whether its
potential-only insertion necessarily produces negative scalar curvature.
These are necessary subproblems, not the full constrained action spectrum.

Route A: canonical scalar plus dust on the homogeneous P=0,Q=1 branch.
Mpl=1, beta in (0,1), B=2 sqrt(3(1-beta))/(3 beta), n=2(1-beta)/beta,
V=Vstar sinh(y)^(-n), phi=B*y. Use N=log(scale factor), v=phi_N,
Omega=rho_b/(3H²), z=coth(y), lambda=n*z/B.
ODE: z'=-(z²-1)*v/B;
v'=-(3-v²/2-3Omega/2)*v+lambda*(3-v²/2-3Omega);
Omega'=Omega*(-3+v²+3Omega).
Physical domain z>1, Omega>=0, v²/6+Omega<1.
Exact branch: v=B*3 beta/(2z), Omega=(1-z^(-2))/(1+beta*z^(-2)).
Verify this expression from AZ40's densities before using it: an incorrect
algebraic expression is a failed known-answer check, never adjusted silently.
Prefer derive Omega directly from rho_b/(rho_b+rho_phi)=csch(y)^2/(1+csch(y)^2).
The latter identity simplifies to 1-z^(-2); use the derived expression,
and retain the above competing expression as a deliberate negative control.
Check exact branch tangency and late fixed point z=1,v=sqrt(3(1-beta)),Omega=0.
Derive full 3x3 Jacobian eigenvalues at the fixed point symbolically.
Success: strictly negative real parts for all 0<beta<1, conditional on this
homogeneous subsystem. This is local attraction, not global or spatial health.

Finite check beta=1/3,2/3,9/10, y_initial=.3,1; six starts per beta:
exact, v increased/decreased 1%, Omega increased/decreased 1%, both increased
1%. Total 36 histories, all initialized in physical domain. N=0..12.
DOP853 rtol=1e-9/1e-11, atol=1e-11/1e-13; compare at 241 shared N points.
Known-answer exact trajectories: scalar equation of state remains -beta;
tie ratio a²/(kappa² G rho_phi)=(2/(1+beta))*V/rho_phi remains 1.
Normalized trajectory discrepancy <1e-6; exact tie drift <1e-7.
Perturbed cases report initial/final tie residual and maximum excursion without
inventing a success tolerance after seeing results. Numerical histories only
corroborate finite attraction, not prove a basin or health of charged branch.

Route B: at fixed p with 0<p<a, W=a²[-p/a-log(1-p/a)]/K,
a(phi)=sqrt(xi G V(phi)), xi=2 kappa²/(1+beta).
Differentiate W twice in phi at fixed p. Seek an analytic sign reduction,
including W_aa*(a')²+W_a*a''. Include canonical V''.
Check independent differentiation at beta=1/3,2/3,9/10, y=.1,1,3,
u=p/a=.01,.5,.99 with 40/80-digit agreement <1e-25.
Negative control reverses V curvature or removes chain term and must break
its named identity. Positive fixed-p curvature does not prove positivity after
eliminating polarization/lapse, so derive and inspect the p/phi Schur complement
as a separate conditional diagnostic. Do not identify fixed-p mass with a
physical screened-background spectrum.

Route C (deferred pending A/B): AZC1's independent cuscuton foliation. Different
failure mechanism (constraint degeneracy), not a relabeling of A. Start only if
A/B expose an obstruction or leave no executable continuation toward full
spectrum. Current priority: canonical route.

Persist scripts, raw failures, output hashes and manifest. Criteria committed
alone before script or graded numbers. Every new diagnostic has a negative
control, stated domain and no transferred observational PASS.
