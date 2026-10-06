# Positive analytic tails do not select the vacuum integral

Checkpoint SOL61-SELECTION-20261006; base 276ae422f0fb0b6990b9824a10fa4979c148aff0. Root-owned continuation of the [NR action dictionary](../../breakthrough_2026_10_05/REPORT.md). Target C=Lambda c^4/a0^2=32pi remains OPEN.

## A stronger surviving counterfamily

The previous compact-support deformation is not real analytic. Could analyticity, positivity of a Laplace representation, and fixed leading asymptotics remove its freedom? **No, under the specified NR action/vacuum convention.** An explicit family is real analytic for every y>0, completely monotone, positive, decreasing, has the same deep-MOND amplitude and leading high-acceleration tail, and admits the same convex six-variable NR action lift. Yet its vacuum integral can change by any prescribed positive amount while all finitely many response derivatives change arbitrarily little.

This is a mathematical Laplace-positive acceleration response. It is not a Kallen-Lehmann propagator, a proof of causal passivity in physical time, a microscopic spectral derivation, or a covariant ghost-freedom theorem. The sibling ordinary-Stieltjes route explains why those distinctions matter.

## 1. A P2-based analytic positive baseline

Put a(y)=sqrt(1+1/y)-1, y>0, and

e_T(y)=a(y)/(1+y/T)^2, nu=1+e_T, T>2.

Each factor has a positive Laplace representation. In particular

a(y)=1/2 integral_0^1 ds /[sqrt(y) sqrt(y+s)],

and each inverse square root is a Gamma-integral Laplace transform of a positive function. The cutoff (1+y/T)^(-2) has positive density T^2 t exp(-Tt). Products correspond to convolution of the nonnegative densities. Differentiating their convergent transforms proves (-1)^n e_T^(n)(y)>0 for every finite n and y>0. These are explicit integral constructions, not an appeal to an unverified spectral analogy.

Deep MOND has sqrt(y)e_T ->1. The high-y leading coefficient is y^3 e_T -> T^2/2. Both make the previously derived endpoint terms vanish. The action source map is x*=y(1+2e), m=e/(1+2e), z=x*^2. Its radial invertibility coefficient D=1+2e+2y e' obeys, with x=y/T and s=sqrt(1+1/y),

D=1+(s-2+1/s)/(1+x)^2-4x a(y)/(1+x)^3 >=1-2/T>0.

The positive term uses s-2+1/s=(s-1)^2/s. The negative term is bounded using a(y)<=1/(2y). Therefore the same-action NR spatial Hessian is positive away from its normal zero-difference MOND degeneracy, with eigenvalues 2 (common), 2/(1+2e) (difference transverse) and 2/D (difference radial). This proves full spatial convexity within that dictionary, rather than just a one-variable response check.

## 2. Conditional vacuum dictionary and a fitted control

Use the exchange-symmetric two-potential normalization and M(infinity)=0 from the previous derivation. Then C=integral_0^infinity y e(y)dy. The primary [Milgrom 0912.0790v2](https://arxiv.org/html/0912.0790v2), equations (1)-(2), supplies the NR action/source dictionary; its identical-metric vacuum equations supply the conditional vacuum interpretation. The source does not select the full M or its additive constant. It was re-opened in this cycle. The integral identity and Hessian lift are previously derived project results, not claims that the source proves the new counterfamily.

For this baseline the stable quadrature is

C(T)=integral_0^infinity dy /[(sqrt(1+1/y)+1)(1+y/T)^2].

The positive integrand increases strictly with T. Continuity on compact T ranges follows by domination; as T tends to zero C tends to zero by the integrable T=1 dominator, while an interval [T,2T] gives unbounded growth for large T. Thus every positive C has a unique fitted T over T>0. The proved sufficient ellipticity range T>2 covers only C>C(2); no claim that every positive C satisfies that sufficient condition is made. For 32pi it is T=202.3676812881133819303795420260172701599. This is a benchmark selected by the desired coefficient, not a prediction or galaxy-data fit.

## 3. Fixed-asymptotic analytic deformation with arbitrary integral shift

For A,Y>0 add

delta e(y)=A/(1+y/Y)^4.

Its positive Laplace density is A Y^4 t^3 exp(-Yt)/6. Hence positivity, complete monotonicity, real analyticity for y>0, and decreasing response persist. The deep amplitude stays exactly one. Since delta e=O(y^-4), the high-y leading coefficient T^2/2 also stays EXACTLY unchanged.

Direct integration gives delta C=A Y^2/6. The source-map correction is

delta D=2A(1-3y/Y)/(1+y/Y)^5, |delta D|<=2A.

If 2A<1-2/T, the entire NR source map remains invertible and the full spatial Hessian remains positive. The bound follows from (1+3x)/(1+x)^5<=1 for x>=0.

For every finite n,

sup_(y>0) |delta e^(n)(y)| <= (4)_n A/Y^n,

where (4)_n=4*5*...*(n+3), (4)_0=1. Fix any finite derivative count N, tolerance epsilon>0, and desired positive coefficient shift Delta. Choose Y>=1 arbitrarily large and A=6Delta/Y^2. Every derivative through N then becomes smaller than epsilon, and ellipticity is retained, while delta C=Delta exactly. This is a uniform whole-axis derivative bound, stronger than a finite measurement-window statement. The exact analytic functions do differ on every open interval; analyticity's uniqueness principle concerns exact agreement, not finite measurement errors.

Consequently C is not continuous in these unweighted finite-derivative response norms, even after fixing both leading asymptotics and imposing this positive-transform property. No finite-precision force-law reconstruction within these restrictions fixes its vacuum value without a quantitative weighted-tail bound or a microscopic selector. This does not show invisibility to arbitrarily accurate measurements or that both actions are healthy covariant theories.

## Evidence and research decision

`checks.py` verifies the source-map identity, exact deformation integral, endpoint limits and finite-derivative formula with SymPy; high-precision quadrature uses two coordinate representations of C(T). Bounded examples shift C by 0.01, 1 and 100 while keeping global response changes below declared tolerances; all source-map/Hessian samples are corroborative, with the proof provided above. A deliberate incorrect A Y^2/2 normalization is rejected.

The obstacle that changed is analyticity: the old compact bump no longer supplies exact agreement on a measured open interval, but positive analytic tails preserve practical non-identifiability and even preserve the UV leading coefficient. This closes the claim that these functional restrictions alone select 32pi. The live continuation is a bound on the weighted UV response or an actual microscopic action producing it. Positivity in an acceleration Laplace variable cannot be substituted for that missing physical derivation.
