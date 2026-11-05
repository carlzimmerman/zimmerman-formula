# HC011 — mathematical answer and explicit force-law tests

2026-11-05. Continues HC010. This is a substantive partial resolution, not a derivation of a new theory. Self-reviewed derivations; no independent referee. Original target remains open. This report consolidates prior exact obstructions and adds new force-law fits and a source/response consistency test.

## Answer in one paragraph

Ordinary BH gravity, a constant amplification of its central force, and the specified BH-only deep nonlinear scalar do not supply the measured radial discrepancy under the tested assumptions. An extended extra field can fit it; on the nominal NGC7331 stellar model, an approximately constant inward acceleration over 19–36 kpc fits well. The stellar mass uncertainty changes its amplitude and inferred slope substantially, so this is not a universal acceleration law. The same radial field can be represented by an ordinary extended mass density. The area target AΛ=32π² is not a Schwarzschild–de Sitter horizon area, and local scalar dynamics alone leave the vacuum normalization free. Thus these calculations do not determine a horizon cause or the coefficient 32π; they do determine specific mathematical obstacles and a fitted radial behavior.

## 1. Fix the actual puzzle

The repository target is

    Λ = 32π a0²/c⁴,
    A* = πc⁴/a0²,
    A*Λ = 32π².

The 32π belongs to the acceleration relation; the area product has 32π². HC007 and HC008–010 contain a prose typo AΛ=32π. This record corrects it without altering their hashed historical text. The numerical area tests used 32π² correctly.

For arbitrary positive dimensionless η, define

    a0 = η c² sqrt(Λ).

Then A*Λ=π/η². The target requires η=1/sqrt(32π). Neither dimensional consistency nor defining A* determines η. This is an exact one-parameter family of equally dimensionally valid alternatives.

## 2. Exact horizon calculation: the proposed area is not an ordinary SdS horizon

Assume static spherical Schwarzschild–de Sitter (SdS), Λ>0, M>=0, with

    f(r)=1-2GM/(c²r)-Λr²/3.

Set x=r sqrt(Λ), μ=GM sqrt(Λ)/c². At a horizon,

    μ = (x/2)(1-x²/3).

Since μ>=0 and x>0, x²<=3. Therefore every positive-radius horizon in this specified family satisfies

    AΛ = 4πx² <= 12π = 37.6991.

The black-hole branch has x<=1, so A_BH Λ<=4π=12.5664. The proposed area product is 32π²=315.8273, outside both bounds. Inserting its x=sqrt(8π) requires μ=-18.49285. This rules out identifying the constructed area with an ordinary nonnegative-mass SdS horizon; it is not a theorem about every spacetime or every horizon notion.

The Schwarzschild surface-gravity formula cannot be used unchanged for a hole at this cosmological scale. With the conventional static SdS Killing-time normalization, the BH acceleration surface gravity is

    κ = c² sqrt(Λ) (1-x²)/(2x).

Setting κ=aLambda=c² sqrt(Λ/(32π)) gives

    x = sqrt(1+1/(32π)) - 1/sqrt(32π) = 0.9052257,
    AΛ = 10.2973062,

not 315.8273. This explains precisely where the literal horizon substitution fails. Surface-gravity normalization in non-asymptotically flat space requires a convention; the area/root bound does not depend on that convention.

The four-dimensional Euler normalization also does not fix the radius. For a round four-sphere of radius L, E4=24/L⁴ and volume=8π²L⁴/3, giving integral E4=64π²=32π²χ with χ=2 at every L. The topological integral is scale independent. On the Einstein four-sphere Λ=3/L²; a corresponding radius-L spherical cross-section has AΛ=12π, not 32π². This restates the prior project obstruction with an explicit example; it is not a new topology result.

## 3. Direct radial answer from NGC7331

Use the 17 outer SPARC radii, 19.24–36.31 kpc, at the published 14.7 Mpc distance. The signed gas acceleration contribution is retained:

    Vbar² = Vgas |Vgas| + Ud Vdisk² + Ub Vbul².

Fit the explicit family

    Vmodel² = Vbar² + B (r/r0)^s,  r0=25 kpc, B>=0.

The corresponding extra inward acceleration is

    delta_g = (B/r0)(r/r0)^(s-1).

Here B must be converted from fitted km²/s² to m²/s² for SI. Central point gravity has s=-1; inverse-radius extra force has s=0; constant acceleration has s=1. Free s is bounded [-3,3]. Fits minimize original velocity residuals divided by errV, rather than linearized squared-speed errors.

For nominal Ud=.5, Ub=.7:

| Extra force | Parameters | χ² on 17 points | Alternating-radius held-out RMSE |
|---|---:|---:|---:|
| Arbitrarily amplified central 1/r² | 1 | 563.58 | 25.20 km/s |
| Extended 1/r | 1 | 136.27 | 11.99 km/s |
| Constant inward acceleration | 1 | 4.69 | 2.54 km/s |
| Free radial power | 2 | 4.02 | 2.06 km/s |

The constant-acceleration model was added after the first free-power fit suggested s close to 1. It is explicitly post-hoc exploratory, not a prespecified discovery test. Alternating-radius holdouts test interpolation only; neighboring radii share distance, inclination and other errors. No population p-value is assigned.

The nominal free-power fit is

    delta_g(r) ≈ 3.677e-11 (r/25 kpc)^(-0.0670) m/s².

The simpler constant fit gives about 3.661e-11 m/s². These hold only over the fitted interval with the stated baryonic decomposition. They must not be extrapolated to the centre, infinity or other galaxies.

Across the nine fixed stellar choices Ud=.3,.5,.7 and Ub=.5,.7,.9, the fitted constant acceleration is 0.272–0.513 aLambda. The free-power force exponent α in delta_g∝r^(-α) spans -0.786 to +0.536. Thus a numerical value near aLambda/2 for some choices does not select a half coefficient: the stellar assumptions move it substantially. This is a direct degeneracy, not a reason to choose the favorable stellar model.

An exploratory nuisance fit allowed Ud∈[.1,1.2], Ub∈[.1,1.4]. Even then the amplified central model has held-out error 24.81 km/s and hits the low stellar bounds. Extended models fit much better, but several also hit the poorly constrained bulge bound. The inverse-radius model improves to 3.95 km/s at both lower stellar bounds. Therefore the data distinguish central from extended support far more strongly than they distinguish specific extended radial laws.

## 4. An extended field is not a uniquely horizon signal

For any s>-1 in the fitted spherical extra-force family,

    M_extra(<r) = B r0^(-s) r^(s+1)/G,
    rho_extra(r) = (s+1) B r0^(-s) r^(s-2)/(4πG) > 0.

Consequently the same rotational acceleration can be produced by a positive extended Newtonian density in this interval. In particular, constant extra acceleration a gives

    M_extra(<r)=a r²/G,
    rho_extra(r)=a/(2πG r).

This is an exact equivalence of radial accelerations, not proof that dark matter exists or that a horizon model is false. It establishes non-identifiability from this rotation curve alone. A global model needs inner/outer transitions: a constant force continued to infinity would have infinite enclosed mass.

A positive ordinary Yukawa addition from a central source cannot repair the shape by increasing its effective enclosed charge. For delta_g=C(1+r/L)e^(-r/L)/r², C,L>0,

    d[r² delta_g]/dr = -C (r/L²) e^(-r/L) < 0.

Its equivalent enclosed mass decreases outward. The nominal required equivalent mass rises. This rules out that particular positive screened central-force form as the required growing component, subject to the baryonic-model limits already stated. General signed or multi-field modifications are not covered.

## 5. A conservative scalar exposes the missing source physics

An explicit nonrelativistic field-plus-particle action is

    S = integral dt { -a0²/(8πG) integral d³x F(|grad φ|²/a0²)
                     + sum_i [mi vi²/2 - qi φ(xi)] }.

Varying φ and xi gives, respectively,

    div[F'(X) grad φ] = 4πG rho_q,
    rho_q = sum_i qi delta³(x-xi),
    ai = -(qi/mi) grad φ.

The same qi appears in the source and response. In this action, ordinary stars with qi=0 neither source nor feel φ. Stars with universal response qi/mi=1 also source it. Therefore a prescription “only BHs source the new field, but all matter universally feels it” does not follow from this simple action. Assigning source and response separately is not a conservative derivation. Horizon boundary conditions or more complicated nonminimal couplings might alter this conclusion, but must be specified and varied rather than assumed.

For F(X)=(2/3)X^(3/2), spherical vacuum flux outside total charge Q gives

    r² gφ²/a0 = GQ,
    gφ = sqrt(GQ a0)/r,
    Vφ⁴ = GQ a0.

The field-action form is the familiar nonlinear-Poisson construction; see [Bekenstein & Milgrom 1984](https://adsabs.harvard.edu/pdf/1984ApJ...286....7B). The displayed variation is derived here. This is a nonrelativistic demonstrator, not a complete relativistic model or a new MOND derivation.

If Q is only NGC7331's published 33-degree BH upper limit, rescaled to 14.7 Mpc, Q=1.923e8 solar masses. With fixed a0=aLambda=9.35847e-11 m/s², the scalar contributes

    Vφ² = 1545.50 (km/s)²,  Vφ≈39.31 km/s.

The nominal fitted inverse-radius addition instead needs B=29341.79 (km/s)², corresponding to Q about 360 times that upper-limit charge. The direct fixed-Q model, also including its Newtonian BH contribution, gives χ²≈6649.6 on the 17 points. The 33-degree upper limit is orientation dependent, and this does not bound arbitrary enhanced scalar charges. It does reject the particular identification Q=published BH mass scale with the stated fixed acceleration scale.

If universal coupling instead makes Q the baryonic mass, the spherical deep limit becomes V⁴=G Mbar a0. That explains how a baryonic acceleration scaling can arise mathematically, but it does not derive a BH origin, its normalization from Λ, disc geometry, cluster lensing, or a viable high-acceleration completion.

## 6. Why the coefficient still cannot be extracted from the local field equation

The scalar equation depends on F'(X). Replacing F(X) by F(X)+C leaves it unchanged for constant C. In a covariant completion, a constant term proportional to integral sqrt(-g) d⁴x is a vacuum contribution and changes the effective cosmological constant.

Equivalently, a gravitational action can contain an independent term

    S_vac = -(c³/8πG) Λ_bare integral sqrt(-g) d⁴x.

Its coefficient is not fixed by the local scalar source/response equation. Models can share the same F', local acceleration parameter and source coupling while differing in their vacuum constant. Changing that constant does change the background geometry; this is NOT a claim that all exact cosmological solutions or all observables stay fixed. It proves that local scalar dynamics alone do not supply a unique equation Λ=32πa0²/c⁴.

A cosmological constraint, symmetry or boundary principle might tie the coefficients together. None has been supplied or established by these fits. Setting the free vacuum constant to obtain 32π would be a fit or a postulate, not a derivation. This repeats the established project coefficient-shift obstruction in the explicit action used above.

## 7. Review and reproducibility

- force001 tests the three frozen force families; force002 adds the disclosed post-hoc constant-force family. Both complete with empty stderr. Final manifests validated against the project root.
- force002 has 248 numerical/symbolic assertions, primarily optimizer convergence and finiteness, not 248 independent physical tests. Independent scalar minimization reproduces the nominal one-parameter central and inverse-radius coefficients within 1e-6 relative tolerance.
- Exact checks include the SdS mass/root relation, surface-gravity solution, Yukawa derivative and nonlinear flux identity. Area bounds follow the displayed inequalities, not a numerical scan.
- Self-review checked source-response reciprocity, signs of inward acceleration versus grad potential, SI conversions, s=-1/0/1 cases, positive equivalent-density range, finite-aperture scope, and vacuum-shift caveat. Lensing, relativistic stability, cosmological evolution and high-acceleration completion remain unproved.
- No old manuscript or external project script was modified. Historical shorthand area-target typos are corrected here and in the live status.

The strongest answer is therefore specific: the tested central-BH mechanisms fail, an extended radial force fits, and neither a horizon origin nor 32π is determined by these data and equations. The unknown is not another correlation coefficient; it is a consistent additional physical law with independently fixed source, response, vacuum normalization and metric predictions.
