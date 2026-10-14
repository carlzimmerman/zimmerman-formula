# Frozen March forecast versus MUSE-DARK III: matched-redshift check

Checked October 13, 2026. This is a comparison of published summaries, not a new fit to the data cubes.

The exact helper functions and constants were extracted from `test_highz_predictions.py` at commit `e1603604aa02e06e5dd397234295e87bb4654b64`. The original H0 = 71.1 km/s/Mpc, Omega_m = 0.315, Omega_Lambda = 0.685, c and Mpc conversion were retained. Nothing was fitted to MUSE. The original helper gives a0(0) = 1.1931775786 in units 1e-10 m/s^2; the manuscript table rounded this differently.

The primary-source MOND-based relation is a0(z) = 1.03 + 1.20 z in those units (PDF Appendix E, Eq. E.5; arXiv HTML Eq. 14). Comparing at the same redshifts:

| z | Frozen forecast | Published MOND central curve | Relative difference |
|---|---:|---:|---:|
| 0.33 | 1.4249 | 1.4260 | -0.08% |
| 0.50 | 1.5776 | 1.6300 | -3.22% |
| 0.80 | 1.8949 | 1.9900 | -4.78% |
| 1.00 | 2.1361 | 2.2300 | -4.21% |
| 1.30 | 2.5361 | 2.5900 | -2.08% |
| 1.44 | 2.7368 | 2.7580 | -0.77% |

A 10,001-point grid gives a largest absolute central-curve difference of 4.78177%. An independent stationary-point check gives the same maximum at z = 0.786979875. For the ratio of the forecast to the fitted line, the derivative vanishes when 0.378(1+z)^3 - 0.16065(1+z)^2 - 1.644 = 0. This polynomial is strictly increasing throughout the observed range, so its one root there is the only interior extremum. Endpoints are closer. The two numerical implementations agree to floating-point accuracy.

The four Figure 3 points are halo-based, not MOND-based. Approximate manual digitization from PDF page 3 gives centers at z approximately 0.506, 0.833, 1.056, 1.283 and levels 1.99, 2.20, 2.58, 2.71. These are illustrative coordinates, with approximate readout uncertainty of 0.01 in z and 0.02 in a0 units; they are not author-supplied values. The frozen forecast is about 7-20% lower. No significance is assigned because graphical error conventions, covariance and the raw likelihood are not reconstructed.

The public catalogue site and already assembled catalogue summaries do not supply the 79 individual MOND acceleration estimates and their joint posteriors. The MOND result also shares baryonic-profile assumptions and common-parameter priors. Therefore a statistical pass against independent MOND measurements cannot be certified from this material.

**Verdict:** the unchanged March forecast closely anticipates the subsequently published MOND-based central redshift trend, within 4.8% across the sampled range. This supports calling it a close advance forecast. It does not establish a verified Kepler-grade statistical success, uniqueness, independent public preregistration, or a model-independent measurement. The earlier 2.3% headline comparison was not a matched-redshift test.

Source: Ciocan et al., arXiv:2604.22613v1, https://arxiv.org/pdf/2604.22613v1. The retained PDF hash is recorded in manifest.json. Outputs: reproducible script, JSON results, CSV comparison and plot. No external source PDF was added to the publication payload.
