# Scattering-resonance follow-up

12 October 2026. Continuation of EVIDENCE.md; same starting candidate and workspace ancestry. This is theoretical screening against an observationally inferred limit, not new observational evidence.

## What changed

Reducing the threshold cross section alone preserves dilute production, but does not reliably remove the cluster problem. The source has a physical two-daughter resonance near relative speed 2 c u. At u=0.01 this lies near 5996 km/s. A Maxwell distribution with mean relative speed 1900 km/s has a small but potentially consequential tail there. Escape truncation and the actual distribution matter greatly.

The first scan held m=1 MeV, u=0.01, alpha=2, and source density fixed, varying threshold S from 0.01 to 4 cm²/g. All points retain occupation bound below 0.001 and width/gap below 0.0001. Scaling is lambda_min proportional to sqrt(S), g proportional to S^(1/4), Gamma proportional to sqrt(S), and Omega/Gamma proportional to S^(-1/4). Lower scattering modestly increases occupation; it does not destroy this conditional production calculation.

## Explicit conditional resonance model

To test the neglected tail, use the vacuum running-width ansatz

    x = (s - 4m²)/(4m²u²)
    eta(x) = lambda_min u sqrt(x)/(8 pi sqrt(1+u²x))
    lambda_eff/lambda_min = 3 + 1/(x - 1 + i eta(x))
    sigma(x)/m = S |lambda_eff/(2 lambda_min)|²/(1+u²x).

This is a resummed vacuum two-body ansatz with alpha=2; a renormalized real self-energy and finite-density corrections are not computed. No separate real-source conversion rate is added to this scattering integral, which would double-count the resonance. The speed variable v=2p/m is a nonrelativistic proxy with corrections of order u². The effective cross section is <sigma v>/<v> for a Maxwell relative-speed distribution. Integrals run to 25,000 km/s.

The pole is resolved with x=1+eta(1) tan(theta), and geometric subdivisions outside the central window. Two central widths (100 and 1000 pole widths) agree within the declared tolerance in all 16 comparisons. An earlier unsplit quadrature failed this test and raised a warning; it is preserved in resonance_run/. Only resonance_run_v2/ is accepted.

## Finite results

| Threshold S (cm²/g) | u | Effective cross section at mean relative speed 1900 km/s (cm²/g) |
|---:|---:|---:|
| 0.1 | 0.010 | 58.347 |
| 0.1 | 0.015 | 0.0924 |
| 0.1 | 0.020 | 0.0959 |
| 0.1 | 0.030 | 0.0982 |
| 0.3 | 0.010 | 101.162 |
| 0.3 | 0.015 | 0.2772 |
| 0.3 | 0.020 | 0.2876 |
| 0.3 | 0.030 | 0.2946 |

The large u=0.01 values are conditional on the high-speed Maxwell tail, not robust exclusion bounds for escape-truncated halos. Moving the resonance out of that tail makes the lower-normalization branch worth further study. This parameter choice was made after seeing the constraint; it is not a successful prior prediction.

For S=0.3 cm²/g and u=0.02, the calculation gives:

- g=2168.0000 eV and lambda_total=0.00881292 at m=1 MeV.
- Source lifetime 3.52096e-13 seconds, conditional on a prepared source.
- Prescribed-pump occupation bound 6.52799e-6.
- Free daughter pressure/energy 1.33280e-4 and initial speed about 0.02c.
- Effective group scattering 0.29559 cm²/g at mean speed 1150 km/s.
- Effective cluster scattering 0.28761 cm²/g at mean speed 1900 km/s.

The last value is below the 0.35 cm²/g 95% upper limit from [Sagunski et al., arXiv:2006.12515v1, equation 19](https://arxiv.org/pdf/2006.12515). That comparison inherits the paper's halo modelling and our distribution/width assumptions. It is not a global observational allowance or a fit to the group's and cluster's individual likelihoods.

## What this buys for galaxies—and what it does not

At an explicitly assumed density 0.1 solar mass/pc³ and relative speed 30 km/s, S=0.3 gives a single-collision time of about 5.20 Gyr. S=0.1 gives 15.61 Gyr. These are density-dependent rate estimates, not a core-formation prediction. The lower scattering may permit some galactic evolution but supplies no target-profile selector. It is not legitimate to inherit the earlier 4 cm²/g halo calculation as the new branch's result.

Likewise, low pressure at creation does not establish cosmological coldness. Production epoch, redshifting, free streaming, relic abundance, and perturbations remain uncomputed for the revised branch. No source-origin mechanism has been supplied.

## Evidence and next discriminators

The scripts and contracts are lower_scattering.py / lower_contract.json and resonance_scan_v2.py / resonance_contract_v2.json. Both completed manifests validate. Checks establish finite numerical behavior only.

The next necessary discriminators are (1) truncated and non-Maxwellian cluster distributions plus uncertainty in the resonance amplitude; (2) production-epoch/free-streaming constraints; and (3) forward halo formation and lensing with the revised parameters. These remain open. No evidence for a unique vacuum acceleration scale, microscopic carrier detection, or the missing halo selector has been added.
