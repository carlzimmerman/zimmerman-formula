# Upcoming non-CONDOR discrimination candidates — 2026-11-04

**Follow-up status:** This is the initial search and conditional shortlist, not the final target-specific assessment. The subsequent [VC875 analysis](../vc875_2026_11_04/REPORT.md) finds no demonstrated clean discrimination from its November release and supersedes the initial optimism about that target. The [AzTEC/C159 analysis](../aztec159_2026_11_04/REPORT.md) supports a conditional test of particular halos, but not a promised decisive FDESI-versus-MOND test. See [next steps](NEXT_STEPS.md). The original search calculations and metadata below are preserved.

Outcome: identified genuinely forthcoming observations with larger conditional F-DESI/MOND separations, but did not establish a scheduled dataset with demonstrated three-way discrimination power. The leading immediate candidate is VC875; the better mass-plus-outer-curve opportunity is AzTEC/C159 in 2027. Existing PAPER66 predictions and seals are unchanged.

## Verified archive candidates

All dates below describe specific units in a public metadata snapshot, not first-ever observations or guaranteed delivery. No proprietary science pixels were accessed.

| Candidate | Project / unit | Listed release (US Eastern) | Why relevant |
|---|---|---|---|
| VC875 = vuds_cosmos_5110377875, z=4.5505 | 2022.1.01118.S / A001/X2d1f/X33a | 2026-11-13 19:00 EST | Deep high-resolution [CII], listed beam0.04457 arcsec; proposed resolved mass distribution, gas clouds and possible halo/outflows |
| AzTEC/C159, z=4.567 | 2023.1.00835.S / A001/X3621/X205e | 2027-07-20 12:28 EDT | Ultradeep [CII] designed to trace extended rotation; beam0.17938 arcsec |
| AzTEC/C159 gas excitation | 2025.1.00827.S / A001/X3833/X2514 | 2027-09-24 14:08 EDT | Multi-transition CO to improve gas conversion/mass constraints |
| BRI1335 gas excitation | 2025.1.00827.S / A001/X3833/X2510 | 2027-03-04 12:34 EST | Same programme combining existing resolved [CII], JWST and VLA observations |
| AzTEC-1 gas excitation | 2025.1.00827.S / A001/X3833/X2530 | 2027-02-19 13:50 EST | Gas information useful, but merger/equilibrium suitability must be established |

The 2025.1.00827.S proposal describes a 16-galaxy programme explicitly aimed at breaking the gas/dark-halo degeneracy. CO excitation constrains but does not uniquely determine alphaCO; do not promise few-percent baryon masses. Its abstract is an observing goal, not evidence of achieved precision.

Lower-redshift alternatives include ROCOKCO data on November19–20,2026 and August2027, and three z~1.5 discs in 2025.1.00182.S on August6,2027. At z1.5 the fixed F-DESI/MOND speed ceiling is only1.77%, so these are less favorable for the distinctive redshift dependence.

## Quantified difference and required accuracy

The screen retains PAPER66's canonical a00=9.3603e-11 m/s², w0=-.838, wa=-.62 and n=1 law g=(gN+sqrt(gN²+4gN a0))/2. The MOND comparator has the identical interpolation and local normalization, held constant with redshift. At z4.5505, F-DESI predicts a0/a00=.660345; constant-scale MOND predicts1. At z4.567 the ratio is .659327. F-flat remains identical to matched MOND.

Conditional VC875-redshift examples at a physical radius5kpc:

| Assumed baryonic acceleration gN/a00 | F-DESI km/s | MOND km/s | Difference | Velocity-only 1sigma budget for nominal 3sigma separation |
|---:|---:|---:|---:|---:|
| .1 | 67.10 | 73.11 | 6.01 | 2.00 km/s |
| .3 | 94.60 | 101.82 | 7.22 | 2.41 km/s |
| 1 | 144.91 | 152.86 | 7.95 | 2.65 km/s |
| 3 | 226.64 | 233.99 | 7.35 | 2.45 km/s |
| 10 | 391.65 | 397.05 | 5.39 | 1.80 km/s |

These are acceleration-conditioned predictions, NOT a measured mass model or a claim that the data reach5kpc. The spectral window covers the redshifted [CII] line. High angular resolution by itself does not establish sufficient outer surface-brightness sensitivity. Spatially varying excitation, inclination, beam smearing, noncircular motions, pressure support and environment require treatment.

In the gN=a00 row, MOND exactly reproduces the F-DESI speed if its inferred gN is0.86160 of the original value: only a0.0647dex shift. With an ideal independent1% velocity uncertainty, the linearized three-sigma budget requires baryonic acceleration uncertainty below3.87%, before other systematics. At gN=.1a00, the corresponding limit is9.0%. These budgets are requirement calculations, not calibrated detection significances or achieved errors. Correlated errors across radii cannot simply be averaged down.

Deep-regime velocity ceilings are9.85% at z4.5505 and14.25% at z7; dense inner regions give smaller differences. In a genuinely asymptotic isolated disk the fixed z4.5505 prediction is Vflat^4/(G Mb)=.6603 a00, compared with a00 for MOND. Testing that ratio requires an actual outer asymptotic curve and independent total baryonic mass. Existing compact high-z measurements cannot be relabelled asymptotic.

An especially useful test combines independent cosmological rhoDE(z) with a0(z) measured from the galaxies: the framework requires a0(z)^2/a00^2=rhoDE(z)/rhoDE0. A match to DESI alone tests the cosmological input, not the galaxy linkage. The frozen PAPER66 CPL numbers are a conditional benchmark; marginalizing their uncertainty weakens separation.

## What this can distinguish

- A sufficiently accurate low-acceleration curve and baryon map near z4.55 can distinguish the fixed evolving branch from matched constant-scale MOND. Values near.66 versus1 for inferred a0/a00 are measurably distinct in principle; current public metadata does not establish the requisite total error.
- Dark matter does not predict a unique speed without halo and galaxy-formation constraints. It can imitate an individual positive mass discrepancy. Cross-radius, cross-galaxy comparisons with independently constrained halo priors and a preregistered population likelihood are needed to establish a preference. No target-specific dark-halo exclusion is calculated here.
- Gaia DR4, scheduled December2,2026, offers a real ~20% MOND-versus-Newton wide-binary signal in common external-field implementations. Smooth Galactic dark matter is negligible for the internal pair force. However PAPER66's scalar galaxy law alone does not fix a two-body external-field prescription; assigning it a distinct wide-binary forecast would require an explicitly selected extension. A local result cannot isolate the redshift dependence, and previous wide-binary analyses disagree.
- Euclid DR1 Foundation is listed for November12,2026; higher-level weak-lensing/clustering products are listed for mid2027. It is not an immediate turnkey test of the galaxy law. The near-local F-DESI signal is small, and a lensing comparison requires a specified relativistic mapping and baryon/environment control.
- DESI five-year dark-energy results are expected in2027. Evolving dark energy alone does not exclude dark matter; w0waCDM contains dark matter. DESI does not directly measure galactic a0.

## Sources, query and reproducibility

Public metadata from [ALMA TAP](https://almascience.eso.org/tap), fetched2026-11-04, saved in archive_dynamics.csv and archive_named_candidates.csv. Main query:

```sql
SELECT target_name,proposal_id,obs_id,s_ra,s_dec,s_resolution,data_rights,
obs_release_date,frequency_support,proposal_abstract
FROM ivoa.obscore
WHERE data_rights='Proprietary' AND
(proposal_abstract LIKE '%rotation curve%' OR
 proposal_abstract LIKE '%dark matter%' OR
 proposal_abstract LIKE '%dynamical mass%')
```

The query returned1627 spectral-window rows including calibrators, not1627 targets. A companion named-target query covered REBELS, CRISTAL, DLA0817 and SPT0418; upcoming REBELS entries were chiefly continuum, not verified outer rotation curves. Year3000 release placeholders mean unknown dates. This is a bounded keyword search, not an exhaustive inventory of all upcoming observatories. Generated inventory.json is a non-J-name shortlist only; J-prefixed science names also occur in raw metadata (for example J1000+0234), so that file must not be read as a complete science-target catalogue.

Primary reading:

- [ALPINE catalogue, Bethermin et al.](https://cris.unibo.it/retrieve/handle/11585/806107/e1dcb337-26e2-7715-e053-1705fe0a6cc9/aa37649-20.pdf): VC875 redshift4.5505 and coordinates matching archive. No SFR/table entry was misused as rotation velocity or baryonic mass.
- [AzTEC/C159 molecular gas](https://arxiv.org/abs/1710.10181): z4.567, large gas reservoir and uncertain conversion factor. Its dynamically constrained alphaCO must not be reused as an independent gravity-test prior.
- [AzTEC/C159 and J1000+0234 dynamics](https://arxiv.org/abs/2011.05340): rapidly rotating, inner baryon-dominated disks; motivates measuring farther out.
- [ALMA execution record for ultradeep programme](https://asa.alma.cl/reporting/executions?end=1723485600000&reportFormat=PDF&start=1722880740000): programme2023.1.00835.S, PI Lelli.
- [Wide-binary simulations](https://arxiv.org/abs/1805.12273) and [2026 quality study](https://arxiv.org/abs/2602.24035): common MOND external-field predictions and contamination risks, not proof of a consensus outcome.
- [Gaia DR4 meeting at Cambridge](https://www.kicc.cam.ac.uk/events/kavli-science-themed-meetings/panta-rhei-moving-varying-sky-gaia-dr4): December2,2026,66 months. Direct ESA release-page fetch was blocked451; [ESA mission page](https://www.esa.int/Science_Exploration/Space_Science/Gaia/%28archive%29/50) lists December2026.
- [Euclid DR1 content and dates](https://euclid.caltech.edu/page/euclid-dr1).
- [Berkeley Lab DESI five-year schedule](https://newscenter.lbl.gov/2026/04/15/desi-completes-planned-3d-map-of-the-universe-and-continues-exploring/).

Computation: screen.py, contract.json, run01/grid.csv, results.json, inventory.json and manifest.json.100 cases:4 redshifts x5 radii x5 accelerations. Checks verify local normalization, an independent algebraic inverse for exact MOND mass mimicry, analytic separation ceiling, and full grid count. Bounded runner completed; manifest validated against inputs. No random sampling. Outcome: finite conditional calculations verified; target-specific achieved precision and unique preference over dark matter remain unestablished.
