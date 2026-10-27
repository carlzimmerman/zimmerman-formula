# NGC5023: independent J-PLUS integrated stellar mass

Checked 2026-10-20; append-only supplement. Existing input JSON and downloaded files were not modified.

The 2026 study supplies an independent, rotation-curve-free stellar mass estimate, but **does not establish an uncertainty-bounded asymptotic total mass for this inversion**.

**Primary source pin.** J. Thainá-Batista et al., arXiv:2603.15869v1, submitted 2026-03-16, A&A708,A274, DOI[10.1051/0004-6361/202557271](https://doi.org/10.1051/0004-6361/202557271). [Exact inspected version](https://arxiv.org/html/2603.15869v1): Table1/footnote and §§2.2–3. The NGC5023 row reports log10(Mstar/Msun)=8.75 and Mr=-17.55AB, using8.59Mpc for every group member. The footnote integrates all datacube spaxels; §2.3 defines a galaxy contour and masks. AlStar uses J-PLUS DR3 twelve-band optical data, updatedBC03/Plat2019 populations, Chabrier IMF, and two-component Calzetti attenuation with tauBC=1.27tauISM. Masses average100 flux-perturbed fits. A maximum r-band S/N50 accommodates calibration/model limitations. Table1 gives no NGC5023 global mass error; AppendixA Fig15 displays local MonteCarlo dispersion maps. No global covariance, missing-light correction, or complete IMF/SPS systematic error budget was recovered. (The detailed living-star/remnant versus initially formed mass convention is not restated in these passages.)

**Aperture source pin.** The 2026 §2.3 explicitly delegates preprocessing details to Thainá-Batista et al., [arXiv:2505.13167v1](https://arxiv.org/html/2505.13167v1), submitted2025-05-19; A&A699,A45; DOI[10.1051/0004-6361/202554704](https://doi.org/10.1051/0004-6361/202554704). That paper's §2.3 sets galaxy boundaries from r-band mu_r=24mag/arcsec² isophotes, allowing manual adjustments. Thus “all spaxels” must not be read as all radii to infinity. The exact NGC5023 contour, manual changes, and unmeasured exterior mass were not recovered. Applying the shared method to this object is a documented-method inference, not a recovered aperture polygon. The 2025 local mass-density scatter concerns other galaxies and is not a NGC5023 global mass error.

## Distance translation and admissible comparison

Holding the observed fluxes, angular aperture, fitted populations and attenuation fixed, the analyst's distance translation is

\[
M_{\star,\mathrm{J+}}(6.50)
=10^{8.75}\left(\frac{6.50}{8.59}\right)^2M_\odot
=3.2198852\times10^8M_\odot,
\]

or log10(M/Msun)=8.5078404. This changes the assumed distance; it is not a new measured mass or a confidence bound. No numerical uncertainty is assigned here.

A nonnegative-annulus optimization may calculate the minimum full-support stellar mass required by the declared force law, gas contribution, geometry and rotation-error intervals. Its ratio to this nominal J-PLUS estimate is a useful **conditional mass-budget discrepancy**. Setting the rescaled J-PLUS number as an equality or ceiling is an additional assumption about aperture correspondence, missing exterior mass and SED systematics. It must not become an unconditional rejection of every stellar gradient.

If Mrequired,min exceeds the translated nominal mass, the difference can be reported as the additional stellar mass or upward SED revision needed under those assumptions. It is not necessarily exterior mass: an increased mass inside the observed footprint could also supply the discrepancy. Formal significance cannot be inferred from the two-decimal table precision, fit residuals, an invented mass error, or independent-spaxel averaging. Recovering the actual footprint and summed-mass MonteCarlo/systematic uncertainty is required to sharpen this comparison.

Checks performed: exact primary versions and table row authenticated; aperture definition followed to the directly cited method; model/IMF/dust/error prescriptions extracted; arithmetic distance translation checked. Verdict: verified nominal integrated SED estimate; whole-galaxy mass-bound application remains conditional.
