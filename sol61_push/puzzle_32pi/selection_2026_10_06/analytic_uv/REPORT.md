# Positive spectral assumptions: an incompatibility and an analytic counterfamily

**No32pi selector was obtained.** The sharper result is that ordinary positive Stieltjes/simple-pole excess responses are incompatible with the finite vacuum integral under the current additive convention. Generalized positive spectral kernels of order greater than two admit finite integrals, but positivity, fixed deep-MOND amplitude, real analyticity, complete monotonicity and full NR spatial convexity still leave that integral free. A concrete positive spectral family realizes this freedom with a uniform finite-window bound.

Requested base276ae422f0fb0b6990b9824a10fa4979c148aff0; actual starting HEADd23562980c4e99430702f7fa8ef2ee12e58c6d99. Pinned read inputs and current run HEAD are in source registry/standard manifests. Writes are confined here. This result is distinct from the sibling Laplace-positive perturbation route: it proves an order threshold for positive Stieltjes spectral measures and reconstructs the genuine linear-pole source dictionary.

## 1. Exact claim and vacuum convention

Use y=g_N/a0>0, nu=1+e, e>0, the exchange-symmetric alpha=beta=1 static energy

    W(p,ph)=|p|²+|ph|²−a0² M(|p−ph|²/a0²).

The action/source/vacuum dictionary comes from [Milgrom0912.0790v2](https://arxiv.org/html/0912.0790v2), with the restrictions established in the prior NR audit: no twin source, physical potential minimally coupled to matter, proportional identical vacuum metrics, f(1)=1,f'(1)=0, M(infinity)=0, and no independent vacuum contribution. Then

    x*=y(1+2e), m=M'(x*²)=e/(1+2e),
    D=dx*/dy=1+2e+2ye',
    C=−M(0)/2=integral_0^infinity y e(y)dy.

The last equality requires endpoint y²e²→0. An independent additive shift M→M+b changes C by−b/2 without changing the NR source law. The report never claims positive spectral conditions fix this offset or the total gravitating vacuum. Full covariant health remains unproved.

## 2. Ordinary positive Stieltjes response cannot have finite C

Assume, as a **mathematical constitutive ansatz** in acceleration y,

    e(y)=b+integral_[0,infinity) rho(dt)/(y+t),
    b>=0, rho>=0,

with e finite for every y>0 and e not identically zero. If b>0 the integral C is plainly divergent. Otherwise any nonzero measure has a bounded interval[0,L] of positive finite mass w. Local finiteness follows from convergence of the Stieltjes integral. Thus

    e(y)>=w/(y+L),
    integral_0^R y e(y)dy >= w[R−L ln(1+R/L)] -> infinity.

For L=0 the expression means wR. Consequently the positive ordinary Stieltjes ansatz cannot satisfy the present finite M(infinity)=0 primitive convention. This is an incompatibility, **not** a selection of a large finite coefficient and not a no-go for all quantum field theories. A subtracted/renormalized vacuum construction would require an additional counterterm prescription, outside this theorem; its finite part is not selected by the positive measure.

For generalized order alpha>0,

    e(y)=integral rho(dt)/(y+t)^alpha,

the same bounded-subinterval argument gives divergent C for every nonzero positive measure when alpha<=2 (logarithmic atalpha2). For alpha>2, Tonelli and y=t u give the exact moment

    C = 1/[(alpha−1)(alpha−2)] integral t^(2−alpha) rho(dt).

Finiteness of that moment is necessary and sufficient for finite C within this positive representation. In particular a mass at t=0 gives infinite C for alpha>2. A positive constant term also gives infinite C. Positivity specifies the sign of the moment, not its numerical value.

[Generalized Stieltjes transforms: basic aspects, Karp–Prilepkina1111.4271v2](https://arxiv.org/pdf/1111.4271v2), definition(1)-(2), supplies the positive-measure class and convergence conditions. The order threshold and vacuum moment above are elementary derivations here, not claims extracted from that paper. Our alpha3 construction need not have minimal/exact Stieltjes order3; its representation of order3 is all that is used.

## 3. A constructive analytic positive spectral family

Fix deep-MOND amplitude A>0 and let B=8A/(3pi). For a dimensionless acceleration-spectrum cutoff s>0 define the positive measure

    rho_s(dt)=B t^(3/2) 1_[0,s](t)dt,
    e_s(y)=B integral_0^s t^(3/2)/(y+t)^3 dt
          = B y^(-1/2) F(s/y),
    F(v)=integral_0^v u^(3/2)/(1+u)^3 du.

The **response has no compact support**. The compact endpoint is in its spectral measure; e_s is positive, real analytic for every y>0 and holomorphic off the negative-axis singularity set. Differentiation under the finite measure gives

    (-1)^n e_s^(n)(y)=(3)_n B integral_0^s t^(3/2)/(y+t)^(3+n)dt>0.

It is therefore completely monotone to every order, not merely monotone. Since F(infinity)=Beta(5/2,1/2)=3pi/8,

    e_s(y)~A y^(-1/2) as y->0,
    e_s(y)~(2B/5)s^(5/2)y^-3 as y->infinity,
    C_s=(B/3)s^(3/2)=8A s^(3/2)/(9pi).

A useful closed form is F(v)=3theta/4−sin(2theta)/2+sin(4theta)/16, theta=atan(sqrt(v)). Numerical evaluation near v=0 instead uses the incomplete beta function, avoiding catastrophic cancellation in this trigonometric expression.

Differentiating explicitly, with v=s/y,

    D_s=1+B y^-1/2 [F(v)−2v^(5/2)/(1+v)^3]
       >=1−(2B/sqrt(s)) v³/(1+v)³
       >=1−2B/sqrt(s).

Hence s>(2B)² guarantees the global invertible source map and full NR Hessian positivity away from zero difference field. The six spatial Hessian eigenvalues are common block2,2,2; difference-transverse2/(1+2e), twice; radial2/D. Endpoint x*(0)=0, x*(infinity)=infinity follows from the fixed deep and UV powers. The primitive M(z)=−integral_z^infinity m(w)dw exists, and

    m dz−2ye dy=d(2y²e²)

has vanishing endpoints. Thus C_s is the same-action vacuum coefficient under the stated convention, not an integral assigned to an unrelated response. Uniform ellipticity at zero difference field remains false, as in ordinary deep MOND.

Positive convex mixtures e=sum_j w_j e_sj, sum_j w_j=1, preserve the fixed A, positive order3 spectral representation, analyticity, complete monotonicity, UVy^-3 decay and the D bound whenever s_j>=s0>(2B)². The source construction therefore survives all these mathematical restrictions. Changing s or the mixture changes the spectral moment and C. No parameter in this family was chosen to reproduce32pi.

## 4. Exact finite-window ambiguity

Fix a reference e_s0, any finite Y>0 and choose S>=s0. For

    e_mix=(1−epsilon)e_s0+epsilon e_S, 0<epsilon<1,

monotonicity of F gives, uniformly for0<y<=Y,

    0 <= e_mix/e_s0−1
       <= epsilon [F(infinity)/F(s0/Y)−1].

This is a strict analytic bound on excess response, not an empirical fit to actual galaxy data. Agreement in nu is at least as good because nu=1+e. The deep amplitude is **exactly** identical, while

    C_mix−C_s0=epsilon (B/3)[S^(3/2)−s0^(3/2)].

For any desired positive shift DeltaC, first choose epsilon small enough for any specified positive tolerance, then choose

    S=[s0^(3/2)+3DeltaC/(B epsilon)]^(2/3).

All admissibility properties above survive. Thus finite precision on any finite acceleration window leaves arbitrary positive UV moment freedom, even in this positive generalized Stieltjes class. Real analyticity forbids two distinct responses from being **exactly** equal on an open interval; this result uses a controlled tolerance, not exact equality.

The bounded example uses A1,s016,epsilon1e-6,Y10,DeltaC1. It gives S23202.7880515, C_base18.1082957473, C_mix19.1082957473, and relative window error<=6.28108721e-6. The global D lower bound is1−4/(3pi)>0. This example changes the leading UV amplitude; the separate sibling Laplace perturbation route addresses preservation of the leading UV amplitude and finitely many measured derivatives. Neither construction has been lifted to a healthy covariant theory.

## 5. Why microscopic positive poles are not this constitutive ansatz

The earliest uncertain arrow is the acceleration-to-momentum dictionary. It does **not** follow from a Källén–Lehmann-style positivity statement, and no such theorem is applied here.

For an explicit healthy-sign linear scalar sector, take a canonical scalar with positive static quadratic operator −Laplace+mu² and universal linear matter source g rho. Solving its field equation gives Green function1/(k²+mu²). Integrating out several such scalars yields a positive-weight sum of simple momentum-space poles. For a point mass and an attractive test-source coupling the additional potential is

    delta Phi(r)=−G M alpha e^(-mu r)/r, alpha=g²/(4piG)>=0,
    delta g/g_N=alpha(1+mu r)e^(-mu r).

Positive superposition gives F(r)=integral alpha(dmu)(1+mu r)e^(-mu r). This genuine linear-source dictionary differs from e(y)=integral rho(dt)/(y+t): the Fourier **potential** Green function is in momentum squared; its ratio to Newton's Fourier potential includes k²; the real-space acceleration differentiates the Yukawa kernel. A heuristic k~1/r also gives k²~a0 y/(GM), explicitly depending on source mass. The variables are not interchangeable.

More decisively, F(r) is independent of M. If a universal e(y), y=GM/(a0r²), agrees with this linear-source response for all M,r>0, then fixing r and varying M sweeps every y>0 while F(r) stays fixed. Therefore e must be constant; varying r then requires F constant. This cannot reproduce both deep MOND e~y^-1/2 and Newtonian e->0. Even for one fixed mass, every positive massive Yukawa term decreases with r and hence increases with y, the opposite of the MOND excess. A massless pole only contributes a constant. If high-acceleration Newton G is normalized including all positive short-range contributions, the long-range excess is nonpositive instead of MOND-positive.

The theorem concerns fixed linear operators, universal linear source coupling and attractive positive weights. Nonlinear screening, background-dependent masses/couplings, nonlocal source laws or additional tensor constraints invalidate its hypotheses and need their own derivation. It excludes this straightforward positive-pole mechanism as a universal MOND response; it does not exclude every passive nonlinear theory.

For a nonlinear action, linearize around a fixed acceleration background y0. Static Hessian coefficients such as2/D(y0) constrain its perturbation kinetic blocks; momentum k labels fluctuations **around** that background, while y0 is a separate constitutive parameter. Positive propagator spectral weights at each y0 do not specify how those weights or vacuum offsets vary with y0. A microscopic selector must supply this map, its full covariant constraints and a vacuum normalization principle. Repeated generalized poles (y+t)^−3 are mathematical positive spectral kernels, **not** positive simple-pole propagators of three healthy particles.

## Evidence and remaining implication

The analytic divergence/order/moment statements and global D/window inequalities are proofs under stated hypotheses. Computation independently checks direct spectral versus incomplete-beta evaluation, moment factors, same-action differential normalization, 181 positive-field Hessian samples, alternating derivatives through order6, deep asymptotic amplitude, UV moment shift and a two-mass Yukawa source counterexample. Grids corroborate but do not prove global positivity. Mutation runs reject doubled moment normalization, a fictitious finite ordinary-pole integral and false acceleration/source-mass universality.

Initial trigonometric-form integration failed because cancellation contaminated the extreme UV quadrature (computed19.10625 instead of19.10830). Stable incomplete-beta evaluation repaired it; its failed raw result is retained under`direct/`, not counted as positive evidence. The final standard runs pin the repaired script. Actual output is bounded numerical evidence, never a covariant health proof.

The remaining arrow is a nonlinear microscopic action whose legitimate spectral/passivity constraints apply to the acceleration constitutive law and also determine its full vacuum moment and additive normalization. No checked source supplies that arrow. Exact32pi stays fitted/unproved. p50's limited rotation-free sample and p51's horizon-equipartition mismatch do not change this spectral mathematical conclusion; they were read to avoid presenting those older routes as new selection principles.

Novelty is project-relative: the Stieltjes order threshold, explicit generalized spectral moment family and linear-pole universal-source obstruction were not present in the reviewed prior NR report/p46-p51. Limited web discovery used generalized Stieltjes/complete monotonicity and positive-pole spectral representation terms; the primary class definition and BIMOND dictionary were verified. No exhaustive global novelty claim or external QFT positivity theorem is made.
