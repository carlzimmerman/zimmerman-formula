# Independent review of the two-tracer virial mass floor

**Normalized claim.** Two spherical stationary Plummer tracers with scales `0<a1<a2`, global LOS second moments using the same weights as their densities, vanishing radial-pressure boundary terms, and a common Newtonian force from a finite nonnegative radial mass measure obey the stated kernel, ratio domain, sharp measure mass floor and total-support bound. Anisotropy may differ between tracers.

**Primary verdict: proved as written** for the corrected exact mathematical statement reviewed below. Its application to Sextans remains conditional on the explicitly stated tracer, weighting, geometry, equilibrium and force assumptions. No algebraic error was found. “Sharp” refers to the positive-mass measure relaxation, not to existence of physical tracer distribution functions.

## Exact revision and correction history

- Review date: 2026-10-19. Observed Git HEAD: `42b43a572c921d2894ad475a0969a0078c89b286`.
- Corrected [VIRIAL_DERIVATION.md](/Users/carlzimmerman/new_physics/zimmerman-formula/sol61_push/cfg853_independent_transport_2026_10_19/VIRIAL_DERIVATION.md), SHA256 `d21e561cbf81a94a5334fb465d4bc05a1e43192565deb3a008788d96894031dd`.
- [source_extraction.json](/Users/carlzimmerman/new_physics/zimmerman-formula/sol61_push/cfg853_independent_transport_2026_10_19/source_extraction.json), SHA256 `9a6114429005c7436d2e2cd1cf766bdeb7e11f8c2c4f6692d8f4a9d7e1115839`.
- Initially reviewed derivation SHA256 `918d6273daf9fed6530f0a975e35d3836d175e75cce2f904b4c086d1e8623ba8` mixed a number-density premise with a luminosity-weighted moment. I reported the missing weight-consistency condition immediately. The author corrected the statement to a common tracer-weight density/moment, explicitly distinguishing number and luminosity weighting. The primary verdict applies to the corrected hash, not silently to the initial wording. The source-extraction application-limit sentence was also updated to consistent tracer weighting (initial extraction hash `93564852843a4b974a668d4b5c4cde2a406bd0ed69e450a26ad5d827d87ac171`); its extracted numbers did not change. This reviewer changed neither root file.

## Dependency graph and independent reconstruction

The only physical starting leaf is the assumed spherical Jeans equation for each tracer. No cited numerical experiment or external theorem is required for the inequality.

1. **Jeans plus boundary condition → integrated kinetic identity.** Put `q=nu <v_r^2>` and `beta=1-<v_t^2>/(2<v_r^2>)`. Multiplying `q'+2 beta q/r=-nu GM(<r)/r^2` by `r^3` and integrating gives

   `integral (3-2 beta) q r^2 dr = G integral nu M(<r) r dr`,

   provided `[r^3 q]_0^infinity=0`. The whole-sky average of one fixed Cartesian component is one third of the velocity trace. Hence the weighted global LOS second moment is

   `S=4 pi G/(3L) integral nu M(<r) r dr`.

   The cancellation uses global spherical averaging; it does not hold for a finite observed aperture with arbitrary selection.

2. **Plummer density plus positive mass → shell kernel.** For `nu=3L/(4 pi a^3)(1+r^2/a^2)^(-5/2)`, interchange the nonnegative integrals in `M(<r)=integral_[0,r) dM(s)`. Direct antiderivative evaluation gives

   `integral_s^infinity r(1+r^2/a^2)^(-5/2) dr = a^2/3 (1+s^2/a^2)^(-3/2)`.

   Therefore `y=3aS/G=integral w_a(s)dM(s)`, with `w_a=(1+s^2/a^2)^(-3/2)`. The normalization, factor `1/3`, dimensions and central mass atom are correct. Whether a shell is included in `M(<r)` at its own radius has no effect on the ordinary `dr` integral.

3. **Kernel → allowed ratio.** With `dP=w_1 dM/y1`, the ratio is `R=E_P[w_2/w_1]`. The weight ratio increases strictly from `1` at zero to the unattained limit `h^3` at infinity. Thus `1<=R<h^3`; `R=1` forces all mass to the origin, while `R<1` and `R>=h^3` are impossible. An unbounded support does not change strictness because no finite radius attains `h^3`.

4. **Kernel plus concavity → sharp mass floor.** Write `u=w_1`, `A=h^2-1>0`, and `g(u)=h^3 u/(1+A u^(2/3))^(3/2)`. Independent differentiation reproduces both derivatives in the derivation, including the negative sign and `u^(-1/3)` factor in `g''`. For `x=y1/M>0`, the concave tangent inequality `g(u)<=g(x)+g'(x)(u-x)` integrated against `dM/M` gives

   `R <= g(x)/x = h^3/(1+A x^(2/3))^(3/2)`.

   Raising to `2/3`, dividing positive quantities and solving yields

   `x <= [(h^2/R^(2/3)-1)/(h^2-1)]^(3/2)`,

   exactly the displayed lower bound on `M`. The direction is correct: spreading a fixed total mass across radii cannot exceed the concave shell curve in moment space.

5. **Strict concavity → equality and support.** Equality for `1<R<h^3` requires constant `u` almost everywhere in mass, hence a single finite shell. Its radius is

   `s_star = a1 sqrt[h^2 (R^(2/3)-1)/(h^2-R^(2/3))]`.

   The shell with mass `M_min` reproduces both moments and saturates the measure bound. If all gravitating mass lies in `[0,b]`, monotonicity of `w_2/w_1` gives the stated `R<=w_2(b)/w_1(b)` and hence `b>=s_star`. This bounds the entire support; it is not a compact-core scale bound in the presence of an extended envelope.

The source-application arrow is separate: authenticated fitted number-density scales and selected Gaussian velocity widths → correctly weighted whole-tracer moments in a spherical stationary Newtonian model. That arrow is conditional, not proved by the paper or algebra.

## Obligation matrix and boundary checks

| Obligation | Result | Reason |
|---|---|---|
| Density and moment weights agree | passed after correction | Corrected statement now expressly matches them. |
| Radial and angular virial normalization | passed | Reconstructed above; anisotropy is eliminated only after full angular integration. |
| Nonnegative integral interchange | passed | Tonelli applies; finite mass and the bounded kernel give finite moments. |
| Concavity and Jensen direction | passed | Explicit derivatives and integrated tangent bound reproduce the formula. |
| Strict ratio domain | passed | Positive finite-radius weights exclude both `R<1` and `R>=h^3`. |
| `R=1` | passed | Only a central mass atom; `M=y1=y2`. Formula has the correct limiting value. |
| `R` tending to `h^3` from below | passed | Shell radius and required mass diverge for fixed positive `y1`. No finite limiting solution is asserted. |
| `h=1`, zero mass or `y1=0` | passed as exclusions | The stated theorem excludes coincident scales and zero moment; with finite nonnegative nonzero mass the positive kernel implies `y1>0`. |
| Equality shell | passed in measure class | Unique radius and mass reproduce both constraints. |
| Physical DF existence | conditional, explicitly not claimed | Jeans moments and shell measures do not prove nonnegative stationary DFs. Fixed stellar density and regularity only restrict the feasible class and cannot lower the bound. |
| Source numerical extraction | passed | Primary v1 HTML/metadata checked as detailed below. |
| Observational application | conditional | Weighting, selection, geometry, equilibrium, binary contamination and Newtonian-force premises remain to be established. |
| Parent numerical checker / LP | not addressed | No checker or LP was run or used as proof by this reviewer. |

Two exact small cases provide separate normalization checks. A central point mass gives `S_i=GM/(3a_i)` and `R=1`. A shell with `a1=1`, `a2=2`, `s=sqrt(2)` has `u=3^(-3/2)`, `R=2^(3/2)`, and `M_min=3^(3/2)y1=M`, exactly saturating the formula. As a further hand check, a self-consistent Plummer gravitating mass at the tracer scale gives `S=pi GM/(32a)` from `integral_0^infinity x^4/(1+x^2)^4 dx=pi/32`.

## External source authentication and application

I independently checked [Tolstoy et al., arXiv:2504.02787v1](https://arxiv.org/html/2504.02787v1), dated 3 April 2025, and its [journal metadata](https://arxiv.org/abs/2504.02787v1). Section 1 gives distance 84.7 kpc. Section 4.2 reports FLAMES dispersion `8.3 +/- .3 km/s` and no significant rotation gradient. Table 2 gives MR `Rh=.339 +/- .021 deg`, `sigma=7.0 +/- .4 km/s`, fraction `.63 +/- .05`; MP `Rh=.62 +/- .05 deg`, `sigma=10.5 (+.8/-.7) km/s`, fraction `.37 +/- .05`. Its radii are projected elliptical half-light radii of Plummer **number-density** fits. Section 4.3 uses Gaussian LOS distributions in a selected 303-star sample. Appendix B confirms a 1.7 km/s survey zero-point difference from 442 matching measurements; that is not an offset measured among Walker instruments. The extraction is accurate for these locators. No remote source-byte SHA256 is claimed and no full article was retained.

For a spherical Plummer tracer, direct projection gives `Sigma(R)=L/(pi a^2)(1+R^2/a^2)^(-2)` and projected cumulative weight `L R^2/(R^2+a^2)`, so the projected half-weight radius equals `a`. Thus `a=D tan(Rh)` is the correct declared spherical translation. It is not an exact deprojection of an elliptical population. A common radius factor rescales all masses but cannot represent arbitrary differing population geometries. Also, `S=sigma^2` presumes the fitted width estimates the required whole-population moment in the correct rest frame; bulk offsets would contribute additional squared means.

The conditional stock formula counts stars once and all cold once: `(1+5.364/f_ret)Mstar`. It is consistent with its declared inventory and is more permissive than subtracting a retained draw before applying a total-mass floor. It remains a model assumption; any extra gravitating supply must be counted. An additional non-Newtonian/tether acceleration invalidates the theorem's specified force premise and needs a new virial calculation.

## Remaining obligation and strongest safe use

There is no remaining algebraic gap in the corrected statement. The cheapest discriminating observational check is to recover the population selection/geometry model and consistently weighted global moments, or to forward-model the actual selected velocities in a common potential. A mass-floor violation under the central spherical reinterpretation is a conditional exclusion of that finite-stock Newtonian model; it is not yet a measured exclusion of every cold-core proposal or the original action.

This was an independent subagent reconstruction from the claim, density/mass definitions and primary source, not a reproduction of the author's checker. The finite numerical/LP validation, model fitting and source-data reduction remain outside this review.
