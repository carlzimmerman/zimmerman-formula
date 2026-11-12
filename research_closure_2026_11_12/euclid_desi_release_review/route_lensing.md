# Lensing/dynamics ratio route — conditional analytic result, 12 November 2026

Requested baseline: 09b8dd7c... . This note reads the live files, pinned by hashes below; it does not assert that the live checkout equals that baseline. No data agreement fit or existing research-file edit was performed.

## Outcome

A useful mass-amplitude-free relation exists in homogeneous acceleration limits. In the isolated, spherical, entirely deep-MOND, self-gravitating constant-M/L limit, global luminosity-weighted line-of-sight dispersion and asymptotic no-slip deflection obey

    c^2 alpha_infinity / sigma_LOS,infinity^2 = 9 pi.

At finite projected radius, measured light shape gives an explicit correction rather than a universal constant. The ratio cancels both stellar amplitude and a0 in this limit: it tests the joint force/lensing prescription, not Zimmerman's normalization or its cosmological origin. This is a combination of known deep-MOND virial content and the standard no-slip deflection integral, not a new theory or established novel theorem. Its practical limitation is severe: typical strong-lens ellipticals and fibre dispersions do not satisfy the deep/global/asymptotic hypotheses.

## Exact hypotheses and observable

Assume a stationary isolated spherical system, vanishing virial boundary term, smooth stellar self-gravity, constant stellar M/L, negligible gas/compact central mass, and a specified acceleration law valid on all relevant radii. Assume light deflection uses Phi=Psi and the same radial acceleration g=Phi' as stellar dynamics, in the weak-field Born approximation. Radial anisotropy may vary, but the full-aperture projected second moment must be observed; include streaming in the second moment if present. Ellipsoids, external fields, extra cold mass and M/L gradients require explicit replacements.

For an axisymmetric spherical lens without external convergence, the Einstein condition supplies the physical deflection alpha(RE)=theta_E D_s/D_ls. Thus the directly constructed ratio is c^2 theta_E D_s/(D_ls sigma_global^2), using angles in radians. External convergence, line-of-sight structure and noncircular configuration modify this condition and must be fitted/propagated. A catalogue SIE velocity scale is not an independent sigma measurement.

## Derivation

Let x=r/Re and m(x)=M_star(<r)/Mstar, with m(0)=0, m(infinity)=1, and luminosity tracer measure dL/L=dm. Exact Abel deprojection of a measured Sersic profile defines m_n(x); no fitted n from lens residuals is allowed.

For spherical systems, angular averaging of the observed LOS second moment gives one third of the total second moment, even with radial anisotropy. The scalar virial theorem therefore gives

    sigma_global^2 = (1/3) integral_0^infinity r g(r) dm.

The same no-slip potential yields

    alpha(R) = (4R/c^2) integral_R^infinity g(r) dr/sqrt(r^2-R^2)
             = (4R/c^2) integral_0^infinity g(R cosh t) dt.

The normalizations are checked by g=GM/r^2, giving alpha=4GM/(c^2 R), and by g=V^2/r, giving alpha=2 pi V^2/c^2.

In the deep spherical self-gravitating limit, g=V_infinity^2 sqrt(m(x))/(Re x), V_infinity^4=G Mstar a0. Therefore

    sigma_global^2 = (V_infinity^2/3) integral_0^1 sqrt(m) dm
                   = (2/9) V_infinity^2,
    H_n(x) = integral_0^infinity sqrt(m_n(x cosh t)) sech(t) dt,
    c^2 alpha(x Re)/sigma_global^2 = 18 H_n(x).

Since 0<=m<=1, 0<=H_n(x)<=pi/2. For increasing m, H_n increases with x and tends to pi/2. Hence the finite-radius ratio approaches 9 pi from below. At finite x it depends on the measured light profile; the asymptotic constant does not depend on n. Sersic profiles are not compact, so asymptotic means a controlled tail limit, not merely R>Re.

This provides a falsifiable shape-normalized conditional null:

    T(x,n) = [c^2 alpha(x Re)/sigma_global^2] / [18 H_n(x)] = 1.

With a constant gravitational slip gamma=Psi/Phi under the same force law, lensing multiplies by (1+gamma)/2, so T=(1+gamma)/2. Inferring slip this way is conditional on the complete dynamical model; extra mass or tracer mismatch can imitate it.

## Newtonian and transition limits: what cancels

For Newtonian self-gravity define V_n=integral [m_n(x)/x] dm_n(x), and m_2,n(x)=M_projected(<x Re)/Mstar. Then

    sigma_global^2 = GMstar V_n/(3 Re),
    c^2 alpha/sigma_global^2 = 12 m_2,n(x)/(x V_n).

The mass amplitude cancels here too. Comparing this shape function with 18H_n is a gravity-response test after n and x are known. It cannot by itself fix Mstar or a0.

For a general interpolation define eta=GMstar/(a0 Re^2), h_n(x)=m_n(x)/x^2 and g=a0 f(eta h_n). Then exactly under these spherical assumptions,

    Q(x,n,eta) = c^2 alpha/sigma_global^2
      = 12 x [integral_0^infinity f(eta h_n(x cosh t)) dt]
             /[integral_0^infinity u f(eta h_n(u)) dm_n(u)].

If f(s)=s^q, the factor eta^q cancels. Newtonian q=1 and deep q=1/2 are special cases. In transition, the two integrals weight different accelerations and Q generally depends on eta. Therefore there is no general boost-independent transition invariant. The derivative d ln Q/d ln eta equals the difference between the lensing-weighted and virial-weighted averages of d ln f/d ln s. A small difference means poor mass/scale leverage despite precise data. Since eta depends on Mstar/a0 at fixed physical size, a ratio-only constraint cannot separately determine a stellar boost and a0. Absolute dispersion or lensing amplitude must supply additional information.

Redshift adds distances and physical size through eta, not a new invariant. A redshift trend is interpretable only after controlling stellar populations, aperture/PSF, selection and environment. Measured n changes both response kernels and can supply leverage across diverse x, but must not be chosen to zero a residual.

## Adversarial counterexamples and scope failures

1. A point-mass-dominated tracer in a deep logarithmic potential has g=V^2/r and sigma_global^2=V^2/3, hence c^2 alpha_infinity/sigma_global^2=6 pi, not 9 pi. Same acceleration scaling, different source/tracer relation. This explicitly disproves a universal 9 pi relation without self-gravity and constant tracer-to-mass assumptions.
2. Changing a constant slip changes alpha while leaving stellar dynamics unchanged. Thus no ratio is a theory-independent identity.
3. A finite aperture does not eliminate anisotropy: projected velocity weights and aperture boundary terms retain beta dependence. Substituting fibre sigma for sigma_global invalidates the derivation. Extrapolating fibre data to a global value with the tested Jeans model would make the alleged anisotropy-free observation circular.
4. Any spherical force g=A f(r) has amplitude cancellation in the two linear functionals, but different radial functions generally have different ratios. A common mean ratio cannot certify the entire force profile: one can perturb g in two narrow radial regions so their virial-weighted contributions cancel while their lensing-weighted contributions do not. Conversely a single ratio leaves infinitely many profile perturbations unconstrained. Physical admissibility must be checked inside the chosen field theory, but the functional non-identifiability is already enough to reject a model-independent curvature theorem.

## Repo overlap and the slope obstacle

A85 already performs the finite-aperture version of lensing-normalized dynamics using simple-mu, exact light deprojection and aperture/PSF integration. VERDICT lines 8-22 record 2.3% mean agreement but 13.29% scatter and chi2/N=3.89. Lines 38-61 show nearly parallel boost/kappa constraints and an apparent preference driven by a poor fit. Its code already has a full-aperture virial check (a85_checks.py lines 266 onward). Consequently the broad idea of a normalization-cancelled lensing/dynamics check is not new to this repo. The useful clarification here is the explicit global anisotropy-free limit, finite-radius shape function and reason normalization sensitivity disappears in homogeneous regimes.

A80 report lines 23-42 and 79-97 show why measured n and an independently defined mass anchor are necessary. A fitted n can erase shape trends or run to unphysical values; this does not validate n.

CFG712 README lines 15-25 records imaging-slope offsets 0.19-0.24 too steep and no per-lens ranking despite Einstein-radius normalization. CFG713 lines 9-23 shows an IMF-only repair fails in that fixed-n, nu_mono, global-power-law mapping. These are not literally the same kernel as A85, so the exact prediction must be recomputed consistently. They establish the mandatory stress test: a new mean-ratio pass is insufficient unless independent radial lens-image shape and per-lens variation also pass. SIE catalogue slopes fixed to two cannot supply that test.

## Surviving implication, first uncertainty, next step

Survives analytically: under the exact hypotheses, Q=18H_n in the deep regime and Q=12m2/(x V_n) in Newtonian gravity; mass normalization cancels. In transition its residual dependence is precisely a mismatch of weighted logarithmic force responses. No data test was performed.

First uncertain empirical implication: whether any released/crossmatched Euclid lenses have genuinely independent, sufficiently extended kinematic second moments and measured stellar profiles in a regime where these response functions differ more than the nuisance budget. Current small catalogues contain neither independent dynamics nor full lens/light images. Typical early-type Einstein radii inside Re and fibre spectra favor a transition/aperture calculation, not the 9 pi shortcut.

Next discriminating step: a model-only sensitivity map over measured n, RE/Re and observed-aperture/Re, with realistic beta/M-L-gradient/environment variations, computing both absolute lensing/dynamics and radial shape. Require held-out image-slope sensitivity at least as explicit as CFG712's stars-only mutation. Select a target on expected information and data quality before opening gravity residuals. If nuisance envelopes cover the kernel differences, record NO VERDICT rather than fitting an n or IMF relation. If they do not, obtain targeted light/arc images and independent resolved spectroscopy. This could yield a new empirical constraint; it is not a derivation of kappa, a cosmological completion or a present breakthrough.

## Primary-source overlap

Milgrom, General virial theorem for modified-gravity MOND (2014), https://journals.aps.org/prd/abstract/10.1103/PhysRevD.89.024016, gives the established deep-MOND mass-dispersion virial relation (its sigma is 3D; divide by three for global spherical LOS). Milgrom's original light-constituent mass estimator is https://arxiv.org/abs/astro-ph/9311031 . The present 2/9 coefficient is independently derived above for the stated smooth spherical model. Neither source alone certifies the relativistic no-slip lensing assumption. No broad novelty claim is made.

## Exact live-source SHA256

- `deepseek_push/DS_FINAL_2026_10_21/A80_slacs_sersic/report.md`: `48bbe0ba5809cfefcd3258d5b3dbe2efa6394b81c42e2637fcf1c603ce68ca8e`
- `deepseek_push/DS_FINAL_2026_10_21/A85_slacs_jeans_joint/VERDICT.md`: `e582ccc5b4ece15de433c95ff7ee603c9c66538de48691c78753505411182c81`
- `deepseek_push/DS_FINAL_2026_10_21/A85_slacs_jeans_joint/a85_checks.py`: `cc89ba3b0263a3456a0f214482c0a9af23b71c9014c002b5195b06abab33d18f`
- `campaign_fresh_gravity/CFG712_slacs_imaging_slopes/README.md`: `b77fa9a1afcdada40d4da8c6c4ee41e9691d9896e35e2df89a4ee70e5ef9d301`
- `campaign_fresh_gravity/CFG713_slacs_required_extra/README.md`: `cf083ffaeeb6e634a488319bfd1775d89c05debd2eb322e0b69a2a73acf8d23b`
