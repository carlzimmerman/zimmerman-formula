# Scale-covariant algebraic cutoff: a viable NR boundary construction, not a selector

## Similarity and its regular-stiffness obstruction
Use the frozen parent Newton normalization ΔΦN=Ω Gnρ in spatial n≥3, κ=a0²/(2Ω Gn), y=|∇ΦN|/a0 and its Claude cutoff q(y,T)=2∫_0^y t b(t)/(1+(t/T)²)dt, b=√(1+1/t)−1. The self-similar source transformation is x→Lx, ΦN→LΦN, Φ→LΦ, ρ→L^(−1)ρ, M→L^(n−1)M. Acceleration and y are invariant. Exact injectivity of ν in T at y>0 requires invariant T for the same physical constitutive kernel.

The gravitational/source action densities and a local potential V(T) have weight zero; the action receives a common factor L^n. A fixed finite quadratic stiffness |∇T|² has weight −2. Thus the action is not covariant under this transformation with a nonzero fixed stiffness. More generally an analytic local derivative expansion with finite coefficients at a zero-field vacuum contains distinct negative derivative weights; a regular nonzero leading stiffness cannot have weight zero. This is a statement for invariant dimensionless T and fixed a0,Gn, not a classification of all possible new fields or nonlocal actions.

One can formally assign stiffness a local weight +2, e.g. Z(ρ)∝ρ^(−2), since density has weight −1, or Z∝|∇y|^(−2). Both choices are singular at the zero-density/zero-derivative vacuum; the latter also fails at a source's y-turnover. They are not regular repairs. In the actual latter action −D|∇T|²/(2|∇y|²), letting R=|∇y|², variation of ΦN contributes

δSextra=D∫(|∇T|²/R²) ∂i y ∂i[ (∂jΦN)/(a0²y) ∂jδΦN ] dx.

It changes the varied physical potential equation and is not permission to retain the parent's spherical ν force law. An external prescribed-density stiffness also requires a matter/source variation dictionary to become a dynamical completion. Neither is accepted here. A dimensionful mass/potential does not cancel the gradient's radius weight; the accepted parent two-body proof applies.

## Constructive boundary route: remove spatial stiffness
Take an auxiliary dimensionless T≥0, with no derivative term and no nonzero vacuum cutoff, and the actual NR action density

L=−∇Φ·∇ΦN/(Ω Gn)+κ[Q(y²,T)−λT²/2]−ρΦ,
Q=y²+q, λ>0 dimensionless.

An additive vacuum offset is set to zero as a convention, not dynamically determined. The whole density has weight zero under the stated similarity. This is motivated only as a test of exact similarity; the quadratic potential is a simple diagnostic, not a microscopic symmetry requirement. No relativistic propagating modulus is claimed.

Varying all fields gives

ΔΦN=Ω Gnρ,
ΔΦ=div[ν(y,T)∇ΦN], ν=1+b/(1+(y/T)²),
λT=q_T(y,T).

For each y>0 the positive root is unique: q_T/T=4∫_0^y t³b(t)/(T²+t²)²dt is strictly decreasing in T, tends to infinity at T↓0 and to zero at T↑∞. The first limit follows from scaling t=Tu on any fixed u-interval and b(Tu)~(Tu)^(−1/2). The energy e=λT²/2−q has derivative T[λ−q_T/T], negative below the root and positive above it. Consequently this is its unique positive global minimum, with e_TT=λ−q_TT>0 at the root. T=0 is also a stationary boundary point for y>0 but is not a minimum. For y=0, q=0 and the unique vacuum minimum is T=0.

Implicit differentiation gives T_y=2yν_T/(λ−q_TT)>0. The root defines exactly the same T(y) and physical ν(y) for every prescribed source. The spherical force follows from the full differential flux equation and a regular center: g=y a0ν(y). The auxiliary envelope action is Qeff=Q−λT(y)²/2; Qeff_y=Q_y because its T derivative vanishes. Its second derivative does contain T_y, so force invertibility must not be inferred from fixed-T differentiation.

## Vacuum and cutoff asymptotics
The global parent bound q_T≤π/2 gives T≤π/(2λ). As y↓0, T↓0; otherwise the equation contradicts q_T→0. Furthermore y/T→0: if T/y stayed bounded along a sequence, the scaled positive-integral bound q_T/T would diverge like y^(−1/2), contradicting fixed λ. In this regime

T(y)=(8/(7λ))^(1/4)y^(7/8)[1+o(1)],
ν(y)~y^(−1/2), g~a0√y.

Thus deep MOND amplitude survives, but T has no positive vacuum cutoff and is only Hölder at y=0. The auxiliary potential has V''(0)=κλ>0; this is not a regular propagating completion. The auxiliary action is C1 at the joint origin, since q_y≤2y b(y)→0 and q_T≤constant√T→0 for T↓0 (the latter follows by b(t)≤t^(−1/2) and integration to infinity). It is not jointly C2 there. The exact partial derivative at fixed y is q_TT=4∫_0^y t³ b(t)(t²−3T²)/(T²+t²)^3 dt. Evaluate this partial derivative on the joint-origin path y=T=ε, after differentiating at fixed y. Rescaling t=εu gives ε^(1/2)q_TT→4∫_0^1 u^(5/2)(u²−3)/(1+u²)^3 du<0 by dominated convergence, using √ε b(εu)≤u^(−1/2). Thus q_TT→−∞ along an actual path to (0,0). This is not the second total derivative along that path. At fixed y>0 the different T↓0 limit instead diverges positively; neither limit is a propagating mass claim. No regular C2 field completion is inferred.

Monotonic T and its bound give a finite limit T∞>0. It obeys λT∞=q_T(∞,T∞), whose positive root is unique by the same decreasing-ratio argument. Then

ν(y)−1~T∞²/(2y³), y→∞.

The response moment Cresp=∫_0^∞ y[ν(y)−1]dy is finite: its integrand behaves as √y near zero and as T∞²/(2y²) at infinity. This is a constitutive response moment, not a derivation of Λc⁴/a0² for this action.

## Actual static source invertibility
Let z=y/T and b'=db/dy. The longitudinal source derivative is

D=d[yν(y)]/dy=1+(b+yb')/(1+z²)−2b z²/(1+z²)²+yν_T T_y.

The last term is positive. The transverse constitutive eigenvalue is ν>0. A rigorous sufficient interval is 0<λ<5/96:

* For y≥1/8, b≤2, so the negative term N=2b z²/(1+z²)²≤b/2≤1; the other term b+yb'=(√(1+1/y)−1)²/[2√(1+1/y)] is strictly positive.
* For y≤1/8 and z≤1/3, (b+yb')/b≥1/3, whereas 2z²/(1+z²)≤1/5, so even the fixed-T contribution is positive.
* Otherwise z≥1/3. Stationarity and b(t)≥b(y) on t≤y imply λ≥(15/16)b(y)z⁴/(1+z²)² by restricting the integral to t∈[y/2,y]. Hence N≤(32/15)λ/z²≤(96/5)λ<1.

Thus both static constitutive eigenvalues are positive everywhere in this admitted interval. This is reduced source ellipticity, not positivity of the two-potential variational Hessian (which is saddle-like), not a propagating-health theorem.

The condition is sufficient, not an exact threshold. Large λ can fail. Taking T=10^(−8), y=3T and defining λ=q_T/T gives λ≈22332.7701 and D≈−98.8957 after retaining T_y. The positive auxiliary minimum therefore does not imply static gravity invertibility. checks.py evaluates this witness by independent high-precision quadrature twice; it also samples an admitted λ=1/100 branch using root bracketing. The samples are bounded corroboration, whereas the inequality proves the admitted range.

## What the symmetry did and did not repair
The algebraic construction gives exact source universality for general n because it contains no spatial length scale. The n-dependent normalization resides only in κ and the Newton force radius; λ remains dimensionless and arbitrary. Increasing λ strictly lowers T(y), because T_λ=−T/(λ−q_TT)<0, hence strictly lowers ν(y) at every y>0. Among any two admitted λ, their finite Cresp values differ strictly. On any compact positive λ interval the bound T≤π/(2λ_min) gives a common integrable tail, and b(y) bounds the small-y integrand; dominated convergence proves continuity of Cresp(λ). As λ↓0 at any fixed y>0, the decreasing ratio q_T/T forces T→∞, so ν−1↑b(y). Monotone convergence gives Cresp→∞, since ∫y b(y)dy diverges. Thus the sufficient healthy interval supports a continuous, strictly decreasing, unbounded family of finite response moments. Similarity cannot select a coefficient.

This is a genuine NR construction at a nonsmooth/auxiliary boundary of the previous finite-stiffness theory. It does not evade that theorem at finite Z, prove observational agreement, repair a covariant kinetic operator, or define a vacuum cosmological constant. The first missing full-theory arrow is a covariant, regular matter/source and vacuum dictionary preserving this auxiliary elimination and its admitted force ellipticity. No physical 32π selector is established.

## Evidence
provenance.json pins the actual checkout and frozen action/source-universality inputs. The computation checks exact algebra plus explicitly bounded mpmath quadrature/root evaluations, with three negative controls: omitting T_y, asserting the large-λ witness is elliptic, and claiming scale invariance for fixed stiffness. Current manifests are summarized separately in RUNS.md. No external classification theorem is used; all source-dependent premises are the authenticated parent action and its q bounds. No novelty claim is made.
