# Do the negative cold-source shells survive correlated errors?

**Partially, and conditionally.** The negative shells survive some generous marginal-error bounds, but they are not a model-independent exclusion of a cold component. The strongest sign depends on the hydrostatic reconstruction and on which field equation the cold material sources. The actual correlated posterior is not present in the inspected products, so a posterior probability or significance has not been computed. A parameter-free mechanism predicting both cluster profiles and the galaxy law remains unresolved.

This report distinguishes the previous additional-source AQUAL calculation from the newer selectively coupled continuous-wave candidate found in commit 351d365892. The latter's cold source adds Newtonian gravity to the baryon-only law; importing the former's inversion into it would be incorrect.

## 1. What uncertainty information exists

The local X-COP files contain forward hydrostatic masses and EM_FORW, gas masses and asymmetric error magnitudes, and smoothed stellar masses with absolute lower/upper bounds. They contain no joint radial mass–gas–star covariance or posterior draws. FITS schemas and every error conversion were checked. In particular, MSTAR_SMOOTHED_LO/HI are bounds whereas MGAS_LO/HI are error magnitudes; confusing them would greatly inflate stellar errors.

The [X-COP mass paper](https://arxiv.org/html/1805.00035) describes a correlated pressure likelihood and MCMC inference, with quoted errors generally representing marginal statistical intervals. The inspected [per-cluster release page](https://dominiqueeckert.wixsite.com/xcop/a1795) lists profiles, not a joint posterior. The release also links a full archive, whose contents were not inspected here. These observations do not prove the necessary chains are unavailable from the authors or elsewhere.

Central masses are interpolated logarithmically to the same six fixed physical radii as before. Positive error widths are interpolated linearly in log radius; stellar absolute bounds are log-interpolated before differencing. Those interpolated widths are treated as marginal sigma-like scales, not authenticated joint standard deviations. Radius, distance, fit-parameter covariance, radial hydrostatic bias and shared systematics are not propagated. No missing covariance was replaced by a chosen correlation length.

## 2. Two source equations, kept separate

Let H be the hydrostatic dynamical enclosed mass, B=Mgas+Mstar and A=a0 r²/G, all in consistent mass units.

**Additional AQUAL source, as in the preceding inversion:**

    Mc = H²/(H+A) - B.

**Selective Newtonian cold source, as in the new CCT bridge:**

    L(B) = [B + sqrt(B²+4AB)]/2,
    Mc = H - L(B).

The second equation implements gstars=glaw(baryons)+GMc/r². It is not literal v3s and is not the same as inserting Mc into the AQUAL source. Both retain the two previously assumed a0 footings, 9.3603e-11 and 1.1312e-10 m/s², separately. Neither equation selects a0 or the cold abundance.

The selective coupling is specified in `sol61_push/continuous_cold_envelope_2026_10_24/COUPLING_BRIDGE.md`. Its ontology, non-universal scalar charge and microscopic completion remain postulates. This audit does not promote it to an established theory.

## 3. Bounding unknown correlations without inventing a covariance

For one shell, linearize its mass difference in six endpoint quantities: two hydrostatic, two gas and two stellar masses. If ai=Ji si combines a derivative and a marginal width, then for every positive-semidefinite unit-diagonal correlation matrix R,

    sigma_shell² = a^T R a,
    max sigma_shell = sum_i |ai|,
    min sigma_shell = max(0, 2 max_i |ai| - sum_i |ai|).

Proof: represent R as the Gram matrix of unit vectors. The variance is the squared length of a sum of vectors with lengths |ai|. Alignment gives the maximum, and the polygon inequality gives the minimum. The maximizing rank-one matrix is explicit and PSD. Individual shell maxima need not be attained simultaneously by one full-cluster covariance.

The implementation also reports independent errors and fully coherent radial errors within each component, with components independent. Those are diagnostic covariance choices, not measured alternatives. Positive common-mode errors often cancel in shell differences and make shape discrepancies sharper; correlations do not automatically erase a negative shell. No quoted ratio to a width is called a detection significance.

For an exact nonlinear check, every input is allowed to vary independently within t times its marginal lower/upper width, with nonnegative component masses. Monotonicity of each source map gives exact endpoint extrema. These rectangular sets contain any correlated realization staying inside the same marginal bounds, but are **not** joint confidence regions and have no assigned probability.

## 4. Results: source coupling materially changes robustness

Counts of central negative shells and of those remaining negative everywhere in the stated marginal box:

| Coupling / footing | Central negative /35 | Remain negative, t=1 | t=2 | t=3 |
|---|---:|---:|---:|---:|
| Additional AQUAL, canonical | 6 | 6 | 2 | 1 |
| Additional AQUAL, alternative | 9 | 6 | 2 | 1 |
| Selective cold, canonical | 6 | 1 | 1 | 1 |
| Selective cold, alternative | 6 | 2 | 1 | 1 |

In every row the t=3 survivor is A644, 0.7–1 R500. In the canonical AQUAL calculation its central deficit is 1.10e14 solar masses and the largest linear width over arbitrary correlations is 2.63e13 solar masses. Their ratio, 4.19, is **not** a Gaussian significance. Even the exact t=3 box leaves its shell at most −3.06e13 solar masses. The selective-coupling ratio to maximum linear width is 3.19.

Thus most selective-cold shell signs are marginal-error fragile, whereas the original AQUAL source signs are harder to remove. The result is conditional on the released forward reconstruction, adopted error semantics and fixed radii.

## 5. Can all shells be repaired simultaneously?

Pairwise repair is insufficient: changes to one radius affect both adjacent shells. We solve the exact six-radius interval-feasibility problem for a nonnegative, nondecreasing enclosed Mc. For intervals [li,ui], the greedy witness max(0,l1,...,li) is feasible iff it never exceeds ui. Bisection finds the smallest common width multiplier t.

Two versions are reported:

- Full marginal-box relaxation: hydrostatic, gas and stellar masses can all move within their boxes. This does not impose joint posterior support or monotonicity of each individually varied baryon component, so its minimum t is an optimistic feasibility bound.
- Constructive hydrostatic-only witness: baryons stay fixed, H alone changes. The reconstructed H is positive and nondecreasing, lies inside the stated bounds and reproduces the nonnegative cold shells exactly. This is a data-feasibility witness, not a cold dynamical solution or maximum-likelihood profile.

Canonical hydrostatic-only minimum width multipliers:

| Cluster | AQUAL source | Selective cold |
|---|---:|---:|
| A1795 | 2.214 | 1.079 |
| A2029 | 1.646 | 0.615 |
| A2142 | 0 | 0 |
| A2319 | 1.232 | 0.761 |
| A644 | 5.893 | 4.029 |
| A85 | 1.516 | 0.133 |
| ZW1215 | 0 | 0 |

For A644 the full-box minima are 5.53 (AQUAL) and 3.66 (selective), compared with hydro-only 5.89 and 4.03. These are maximum coordinate displacements in units of marginal widths, not Mahalanobis distances, chi-squared values or probabilities. The selected greedy witness is not the unique profile at the minimum t; its unneeded inner changes should not be interpreted as individually required changes.

## 6. Reconstruction systematics prevent a universal negative-shell verdict

Repeat the central calculation using each released mass reconstruction without refitting or selecting a preferred model:

| Mass reconstruction | AQUAL negative shells, canonical / alternative | Selective negative shells, canonical / alternative |
|---|---:|---:|
| Forward | 6 / 9 | 6 / 6 |
| NFW | 4 / 5 | 1 / 1 |
| Einasto | 6 / 9 | 2 / 4 |
| Isothermal | 13 / 13 | 7 / 8 |
| Burkert | 11 / 13 | 6 / 6 |

These models use the same observations and are not independent datasets. Their counts are neither model probabilities nor a prescription to adopt whichever passes.

A644 is the decisive illustration. The forward H barely rises from 4.890e14 to 4.932e14 solar masses between 0.7 and 1 R500. The released NFW reconstruction instead rises from 4.332e14 to 5.938e14. Under selective coupling, A644 has **zero negative shells in the NFW reconstruction on either footing**. Canonical Einasto also has none. Under additional-source AQUAL, A644 retains at least one negative shell in every tested central reconstruction, but their joint uncertainty has not been tested model by model.

Therefore even the strongest forward-profile sign is not a coupling- and reconstruction-independent proof that positive cold material is impossible. The full correlated statistical question remains open pending the joint profile likelihood or draws. The exact bounds above are useful partial answers, not a replacement for that missing likelihood.

## 7. A dynamical constraint stronger than fitting a temperature

An added positive source inside AQUAL must satisfy the field equation before choosing its pressure, velocity dispersion or wave state. Write f(g)=g²/(a0+g) and alpha=-d ln g/d ln r. Then

    dMc/d ln r = (r²/G) f(g) [2-alpha (g+2a0)/(g+a0)] - dMb/d ln r >= 0.

Even if baryon shell mass were ignored, positivity requires

    alpha <= 2(g+a0)/(g+2a0).

The limit is alpha<=1 in deep MOND and <=2 at high acceleration; positive baryon shell mass makes it stricter. This is an algebraic source-realizability condition, not a restriction on one halo profile. No cold pressure or orbital distribution can repair its violation while the same instantaneous spherical AQUAL mapping and positive source remain in force. Time dependence can instead invalidate the hydrostatic inference of g; it cannot be invoked while silently keeping that inference exact.

Selective cold has a different condition, d[H-L(B)]/dr>=0. Its greater flexibility is visible in the uncertainty results. It still cannot hide an extra positive force in a galaxy that already obeys the baryon-only law: exact preservation requires Mc(<r)=0; a tolerated fractional acceleration increase epsilon gives GMc/r²<=epsilon glaw. A generated exclusion/retention history remains necessary.

## 8. Does the existing wave dynamics supply the missing cluster scale?

The new CCT action uses

    i eta partial_t psi = -(eta²/2) lap psi + (Phi_b,N+Phi_c) psi,
    lap Phi_c = 4 pi G |psi|².

Its eta=1500 pc km/s is an existing imposed input, not a constant derived here. The candidate's conserved density is rho=|psi|². Stars additionally feel the baryon-only law, while cold modes feel baryonic Newtonian gravity; these couplings were kept separate in the estimate.

For a smooth density varying on scale r, the gradient-stress to gravity scale ratio is

    epsilon_Q ~ [eta/(r v_c)]²,
    v_c² = G[Mb(<r)+Mc(<r)]/r.

Using the central selective-cold source requirements, epsilon_Q spans **6.8e-13–2.6e-10 canonical** and **7.5e-13–2.7e-10 alternative** across the 42 radii. Thus the existing eta does not provide smooth quantum-pressure support for a 100-kpc-to-Mpc cluster envelope. This estimate assumes density gradients on r; short-wavelength phases, nodes and excited-mode stress are not bounded by it.

The coherent self-gravity length eta²/(G Mc(R500)) is about **1.3e-6–4.5e-6 pc** across both footings. It is an order-of-scale balance, not a fitted core radius or an exact soliton solution. A broad cluster component must instead obtain support through excited modes, orbital motion, multistreaming or other physics. In that regime wave phase mixing may generate collisionless-like stress, but eta alone does not select its radial distribution.

Two exact conservation arguments show the remaining freedom:

1. For the stated real potential, partial_t rho+div j=0. Total cold mass changes only through boundary flux. The vacuum coefficient does not select the initial norm or the incoming flux in these equations. Local retention can be dynamically generated only from a specified supply/history; it is not fixed just by writing a continuity equation.
2. In the isolated self-gravitating limit, fixed eta and G admit the rescaling psi_lambda(r,t)=lambda² psi(lambda r,lambda² t), Phi_lambda=lambda² Phi(lambda r,lambda² t), giving M_lambda=lambda M and R_lambda=R/lambda. The action therefore does not pick one mass and radius from eta. Baryons break that exact scaling but do not remove the need to select norm, energy and incoming state.

A barotropic alternative has the same closure issue in another form. For positive dp/drho, define enthalpy h(rho)=integral dp/rho. Static balance integrates to h(rho)+Phi=C. Even a fixed equation of state leaves C or total mass/boundary data to select. Isothermal gas gives an exponential density with a free normalization; a polytrope can have finite support but still needs a boundary/central state. Constant vacuum pressure has no pressure gradient and cannot supply static support. These are scoped closure statements, not a theorem excluding microscopic state selection.

The existing CCT transport work reports that eta, supply and incoming history remain postulates, and its matched Fornax/Leo I pilots do not reach a validated late outcome. We have not rerun those heavy experiments or relabeled their initial states as predictions. A new cluster simulation with assigned occupations or a fitted dispersion would not meet the user's no-new-parameter objective.

## 9. What is established and what remains open

Established here, conditional on the inputs and interpolation:

- exact marginal-box sign bounds and minimum six-radius positivity repairs;
- linear covariance extrema that do not require selecting a correlation matrix;
- strong dependence of shell-sign conclusions on source coupling and released reconstruction;
- the source-positivity acceleration-slope condition;
- the existing wave scale's inability to support a smooth cluster envelope by gradient stress alone.

Not established:

- the probability that any shell is negative under the actual joint observational posterior;
- a unique data-supported cold profile;
- parameter-free cold production, capture, stress or galaxy exclusion;
- a microscopic origin of eta, the source charges, abundance or a0.

The next identifiable data object is a joint draw of H(r), Mgas(r), Mstar(r), radius/distance and their common inference parameters, or the underlying likelihood needed to generate it. Score shell positivity draw by draw under both source equations and reconstruction models. The next theory object is an action plus independently selected incoming state that predicts the normalization and mode/stress distribution while passing the galaxy guard. Neither can be substituted by a fitted equilibrium.

## Reproduction and review

`launch.py --runner <computation-audit scripts/run_experiment.py>` creates the AQUAL, selective and deliberate-mutation runs in fresh directories. Both normal runs pass their controls; the mutation misreads the stellar absolute bound as an error width and fails the required schema identity. Manifests hash source, equation dependencies and raw data. CSVs retain every shell, model and repair size; JSONs retain explicit witnesses and wave scales. The figure is a sensitivity plot, explicitly not a confidence interval. Results are self-reviewed, not independent peer review.
