# DF2 observational input check

Checked 2026-09-12. Scope: source authentication and observational normalization for a fixed-a0 static calculation; no likelihood, empirical significance, or relativistic closure is established. Exact means transcribed as published, not error-free. No matching local source copy was found by identifier/filename search. Source files were not retained; hashes therefore unavailable. Only this report and inputs.json are written.

## Distances and geometry

[Tang, Anand, Romanowsky, van Dokkum & Bundy, arXiv:2606.05144v2](https://arxiv.org/html/2606.05144v2), 22 June 2026, *New Measurements of Distances to Galaxies in the NGC 1052 Field with the Hubble and James Webb Space Telescopes*. Full main text, Table 1, and appendices A/B inspected. Table 1 provides coordinates and distances encoded in inputs.json. Section III gives DF2 modulus 31.23 ± 0.07 mag, including calibration uncertainty. Section II's SBF errors include calibration systematics but exclude differences between empirical calibrations. Host and dwarf SBF calibrations differ. No joint distance covariance is tabulated. Section IV acknowledges a closer host PNLF result; Section V leaves the HST/JWST discrepancy unresolved. The PNLF source is [Jacoby et al., arXiv:2309.11603](https://arxiv.org/abs/2309.11603), ApJS 271, 40 (2024); full source retrieval failed, so its number remains verified only as quoted by Tang.

Our geometry calculation uses r²=(Dhost−Ddf2)²+2Dhost Ddf2(1−cos theta). Coordinates give theta=13.650869 arcmin. At 17.6 Mpc the transverse projection is 69.887 kpc. The central SBF-host geometry yields r=3700.799 kpc; the alternative PNLF-host central geometry gives 308.168 kpc. These are conditional central values, not inferred separation distributions. Covariance and method offsets prevent assigning a supported close-passage probability here. An 80 kpc physical separation requires additional geometric assumptions.

## Stellar profile and normalization

[van Dokkum et al., arXiv:1803.10237v1](https://arxiv.org/pdf/1803.10237v1), 27 March 2018, *A galaxy lacking dark matter*: main text page 1 and Methods structural-parameter section inspected. Published Sérsic n=0.6, projected q=0.85, major-axis Re=22.6 arcsec, LV=1.1e8 solar luminosities at D=20 Mpc, M606=−15.4, and approximate Mstar=2e8 solar masses. Stellar M/LV=2 is an adopted population normalization, not a dynamical fit. Keeping the photometry fixed implies Re proportional to D and luminosity/mass proportional to D². The rounded quoted Mstar and LV times 2 differ by 10%; calculations must choose and disclose a convention. The angular radius is preferable to the rounded 2.2 kpc conversion. This check did not authenticate newer morphological fits or a modern population posterior.

## Kinematic apertures and version trap

[Danieli et al., arXiv:1901.03711](https://arxiv.org/abs/1901.03711), *Still Missing Dark Matter: KCWI High-Resolution Stellar Kinematics of NGC1052-DF2*: latest record identifies v2, 11 March 2019, with sigma=8.4 ± 2.1 km/s. However, the unversioned PDF returned an older body containing 8.5(+2.3,−3.1) and a 95% upper limit of 11.8. Exact-v2 PDF, HTML, and publisher retrieval failed. The latest central summary is authenticated only at abstract level; its likelihood is unavailable. The older full body's Fig. 1/Section 2 specifies the 16.5×20.4 arcsec KCWI rectangle reaching about 0.7 Re, with optimal exposure weighting and source masking. Its Section 4 gives circularized Re=2.0 kpc at 20 Mpc. These aperture details need exact-v2/data confirmation for a rigorous comparison; a full circular Re aperture is not equivalent.

[Emsellem et al., A&A 625 A76 (2019)](https://www.aanda.org/articles/aa/pdf/2019/05/aa34909-18.pdf), *The ultra-diffuse galaxy NGC 1052-DF2 with MUSE. I. Kinematics of the stellar body*. Published extraction section and arXiv body Sections 2.3, 3.3, 4.2 inspected; [arXiv record](https://arxiv.org/abs/1812.07345) identifies v3 dated 1 April 2019. Elliptical apertures use major-axis Re, q=0.85, PA=−48 degrees from north through east. The nominal Re dispersion is 10.8(+3.2,−4.0) km/s, incorporating ordered and random motion. Full-systematics 95% upper limit is 21 km/s. Nested aperture measurements are correlated and cannot be multiplied as independent data. The full mask, spatial weights, PSF, and joint posterior were not acquired.

## Existing MOND estimate

[Famaey, McGaugh & Milgrom, arXiv:1804.04167](https://arxiv.org/pdf/1804.04167), *MOND and the dynamics of NGC1052-DF2*, Sections 2–3 inspected, unversioned copy. Its host V=210 km/s and projected-separation external field are assumptions of an approximate estimator. M/LV=1–4 is a sensitivity range around 2, not an observed probability distribution. Its 13.4 km/s estimate must not be imported as an action-derived PDE result or reused at the new central host geometry.

## Remaining measurement requirements

A rigorous empirical test still requires the exact revised KCWI extraction/likelihood, observed spatial weights and mask, a population M/L posterior, deprojection/inclination and anisotropy treatment, and host/environment baryonic distributions with joint distance calibration information. This bounded search supplies conditional inputs and explicitly missing quantities; it does not support fitting these omissions to the dispersion.
