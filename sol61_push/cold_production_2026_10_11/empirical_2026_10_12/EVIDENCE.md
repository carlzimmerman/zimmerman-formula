# Empirical checkpoint: support for the law, tension for the carrier

Checked 12 October 2026. Base workspace revision: dbe89ed33bf2416b71a9c58424a74273e6665792. Candidate research snapshot published as e2440ea304ed96e1b48c39691a2ee441220aa093. This checkpoint does not alter the candidate parameters or claim discovery of its particles.

## 1. Direct check against released galaxy measurements

Downloaded the official [SPARC RAR table](https://astroweb.case.edu/SPARC/RAR.mrt), attributed to Lelli, McGaugh, Schombert and Pawlowski, *One Law to Rule Them All: The Radial Acceleration Relation of Galaxies*. The release contains 2,693 rows of log baryonic/observed acceleration and their errors. See the [SPARC source and citation instructions](https://astroweb.case.edu/SPARC/).

Using all rows, with no parameter optimization, the frozen repaired monotone kernel gives:

| Acceleration scale (m/s²) | RMS log10 acceleration residual | Median observed-minus-predicted residual | Fraction within 0.2 dex |
|---|---:|---:|---:|
| Canonical 9.3603e-11 | 0.13712 | +0.03163 | 86.11% |
| Alternate 1.1312e-10 | 0.13290 | +0.00369 | 88.64% |
| Literature reference 1.2e-10 | 0.13293 | -0.00421 | 88.56% |
| Baryons alone, Newtonian | 0.51398 | +0.43000 | 22.65% |

These are our computed descriptive statistics, not a quoted source result. The two repository scales were copied from CFG544; the monotone construction was reimplemented from CFG626. The original exponential kernel produces almost identical aggregate residuals (canonical 0.13714 dex). This dataset therefore supplies no meaningful preference for the repair based on this RMS comparison.

This is agreement with observations, but not independent validation: the phenomenological RAR family was developed using this dataset, and the normalization is not a new microscopic prediction. Baryons-only Newtonian gravity is a useful null comparison, not a competitive fitted dark-matter model. No model-selection significance follows. The released table lacks galaxy identifiers and full covariance; radial points are correlated. Reported RMS is not intrinsic scatter. No pointwise bootstrap, p-value, or fitted-parameter confidence interval is asserted.

Data SHA256: `24aa7059dab7fa44787f7c11191052489899819370f6508621674769f3b72833`.

## 2. Independent observational channel: weak lensing

[Mistele et al., arXiv:2310.15248v3, 8 April 2024](https://arxiv.org/html/2310.15248v3), especially sections 2, 3, 5 and 7, find a weak-lensing continuation of the kinematic RAR over about 2.5 additional decades in acceleration. This supports the target relation through a different observable. The analysis assumes spherical deprojection, uses strict isolation and consistent stellar/gas mass estimates, and treats the unmeasured outer profile as a systematic. It does not detect our fields or derive their action. It reuses KiDS data from earlier lensing work; these papers are not independent surveys. Our work here verifies the published inference, not a fresh shear-catalogue replication.

The useful next comparison is a forward prediction of excess surface density from the evolved carrier, with the published radial covariance. Agreement obtained by imposing the target density would test the phenomenology only. Existing repository lensing work and covariance files should be reused rather than duplicated; `real_research/reviews/lensing_rar/lr_data_acquisition.md` points to them.

## 3. Carrier constraint: the illustrative cross section is too large in this screen

[Sagunski et al., arXiv:2006.12515v1](https://arxiv.org/pdf/2006.12515), equations 6 and 19 and section IV, infer a cluster upper limit of 0.35 cm²/g at 95% confidence in their Jeans analysis. Their effective cross section is <sigma v>/<v>; representative mean relative speeds are about 1150 km/s for groups and 1900 km/s for clusters. The analysis depends on halo and baryonic modelling, so its limit is not a model-independent particle exclusion.

For our alpha=2, u=0.01, threshold 4 cm²/g benchmark, the below-resonance formula gives sigma/m=3.566 cm²/g at 1900 km/s. More carefully, assume the paper's Maxwell relative-speed distribution and integrate sigma(v) v only from 0 to 3000 km/s, dividing by the full mean speed. This gives a **partial effective rate of 2.8644 cm²/g** for mean speed 1900 km/s. The integration covers 82.54% of the velocity-weighted distribution and stays at x<=0.251, away from the pole. An unknown positive contribution from higher speeds cannot reduce it. It exceeds the quoted bound by a factor 8.18 under this translation. For groups the corresponding partial rate is 3.7483 cm²/g.

This is a conditional tension test for a dominant interacting component, not a full likelihood analysis. Different component fractions, phase-space distributions, or halo histories require new modelling. Merely removing the resonant tail cannot fix this result. At fixed shape, the partial bound alone would require a threshold normalization no larger than about 0.489 cm²/g; this is a necessary condition in this screen, not a sufficient allowed value. Reducing it also changes the production couplings and halo evolution, which must be recomputed rather than silently inherited.

## 4. Counterevidence to unrestricted universality

[Júlio et al., arXiv:2510.06905v1 / A&A 704 A330 (2025)](https://arxiv.org/html/2510.06905v1) study 12 low-mass dwarfs with stellar kinematics and Jeans modelling. They report systematic departures above the usual low-acceleration RAR, with substantial galaxy-to-galaxy scatter. This challenges an unrestricted density-only universal target. Their inferred accelerations are model-dependent, but omitting this regime would overstate support. A real cold component could in principle have history-dependent departures; the present action has not predicted these data.

## Reproducibility and next decision

`check_empirical_v2.py`, `contract_v2.json`, `RAR.mrt`, and `run_v2/` record the finite computation. All seven numerical checks pass. The first run failed only when serializing a NumPy boolean; the original script and failed manifest remain in place. The corrected version converts check flags to native booleans before saving. No data or physical formula changed.

The strongest surviving empirical statement is support for a tight acceleration relation in the measured disk-galaxy regime, with an independently measured lensing continuation under stated assumptions. There is **no direct empirical identification of the proposed carrier**. The immediate priority is a joint galaxy/cluster constraint calculation for a physically consistent lower-scattering branch, followed by forward lensing predictions and dwarf departures. These are open follow-ups; they have not been executed at this checkpoint. More simulations of the already failing 4 cm²/g benchmark would not by themselves supply the missing observational support.
