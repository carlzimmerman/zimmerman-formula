# Empirical screen: the unit-charge 10 MeV messenger produces too large an electron-moment correction

2026-10-13. The 10 MeV messenger benchmark should no longer be treated as an empirically credible apparatus point in the minimal sector. Its calculable electromagnetic vacuum-polarization contribution is much larger than the comparison scale of the 2023 electron magnetic-moment experiment. This is a dated, explicit consistency screen, not a global statistical exclusion or an assumption-free statement about all possible extensions.

## Observable and calculation

Define a_e=(g_e-2)/2. A hypothetical elementary complex scalar S with electric charge magnitude e and mass M contributes at two loops even without a direct electron–carrier interaction. For the positive Euclidean, charge-subtracted scalar polarization,

    Pi_E(Q^2) = alpha/(4pi) integral_0^1 dz (1-2z)^2
                 log[1+Q^2 z(1-z)/M^2],
    Delta a_e = alpha/pi integral_0^1 dx (1-x)
                  Pi_E(m_e^2 x^2/(1-x)).

An independent dispersive representation uses the point-scalar spectral ratio

    R_S(s) = (1/4)(1-4M^2/s)^(3/2),
    K_e(s) = integral_0^1 dx x^2(1-x)/[x^2+(1-x)s/m_e^2],
    Delta a_e = alpha^2/(3pi^2) integral_(4M^2)^infinity ds R_S(s) K_e(s)/s.

Both representations are positive. In the heavy-mass limit,

    integral_0^1 dz (1-2z)^2 z(1-z) = 1/30,
    Delta a_e = (alpha/pi)^2 (m_e/M)^2 / 360 + higher mass corrections.

The full leading two-loop integrals, rather than just this expansion, are evaluated. log(1+t)<=t also makes the displayed leading heavy expression an upper bound on this particular integral at finite mass. The calculation uses m_e=0.51099895 MeV and alpha=1/137.035999; rounding alpha at this level is negligible for the screen and does not fit alpha to absorb the new contribution.

| Messenger mass | Full leading Delta a_e | Full / leading heavy approximation |
|---:|---:|---:|
| 10 MeV | 3.89989e-11 | 0.996515 |
| 100 MeV | 3.91329e-13 | 0.999939 |
| 1000 MeV | 3.91352e-15 | 0.999999 |

This contribution exists in the vacuum theory. Binding real S particles into neutral atoms does not remove their virtual charged-scalar vacuum loop. Reducing the bath density also does not change this observable.

## Experimental comparison and its limits

[Fan, Myers, Sukra and Gabrielse, Measurement of the Electron Magnetic Moment](https://arxiv.org/pdf/2209.13084), published in PRL 130, 071801 (2023), reports g/2=1.00115965218059(13). Its measurement uncertainty is 1.3e-13. The paper discusses discrepant independent alpha measurements and gives approximately 0.7e-12 as the theory–measurement comparison scale on page 4. That scale is not a standard deviation or a confidence interval.

The 10 MeV scalar contribution is about 55.7 times that comparison scale. It is also about 300 times the measurement-only uncertainty, but **this is not a 300-sigma exclusion**: the independent alpha determinations, theory uncertainties, other model contributions and their correlations must enter a proper fit. Nevertheless, the discrepancy is large enough that the minimal unit-charge benchmark cannot responsibly be presented as experimentally supported or ready for apparatus development. No compensating new contribution has been derived in the repository's specified sector.

Solving the full integral for Delta a_e=7e-13 gives M approximately 74.77 MeV; choosing 1e-12 gives 62.55 MeV. These are diagnostic mass scales only, not allowed-mass boundaries. The 100 MeV and 1 GeV rows have not passed collider, fixed-target, cosmological, stable-charge, atomic-spectroscopy or other precision constraints. We do not claim that moving to either mass solves viability. This comparison uses the named 2023 reference, not a claim to reproduce the latest combined electron-moment fit.

## Consequence for the manufacturing route

Earlier wall, bath, source and stability calculations at M_S=10 MeV remain conditional mathematical calculations. Their physically viable interpretation is superseded by this screen. Further optimization of that benchmark should stop until a compatible microscopic sector is specified and tested against measurements.

Increasing M_S changes the preparation model rather than simply improving this bound. At fixed h, the carrier potential scales as n/M_S and the matched photon coefficient as h/M_S^2. Keeping the previous source photon coupling fixed requires A proportional to M_S^2, and the square-completed lambda_RS minimum also scales as M_S^2. For example, raising 10 MeV to 100 MeV requires ten times the density to preserve the same wall potential and one hundred times A to preserve the same leading source photon coefficient. The new medium, scattering, stability, and constraints must then be recalculated. These are algebraic scaling consequences, not a recommendation that the heavier point is viable.

The next useful route is a constraint-led choice of messenger sector or a different explicitly coupled production mechanism. The global goal of theoretically making the proposed cold carrier is unresolved; this result rules out treating a convenient assumed ingredient as empirical evidence.

## Source and numerical audit

The original experiment above is the empirical source. For normalization, the author-written QFT treatment [Jegerlehner and Nyffeler, arXiv:0902.3360](https://arxiv.org/pdf/0902.3360) gives the scalar spectral factor in Eq. (108), including the point-particle form-factor limit, and the vacuum-polarization dispersion framework in Sec. 4.1. Here the scalar is stipulated elementary, with unit form factor; no measured pion form factor or hadronic data is applied to it. The small-mass-ratio coefficient is independently integrated symbolically.

The initial tensor-product Gauss integration failed its refinement check at 100 MeV: the endpoint layer 1-x of order (m_e/M)^2 was unresolved. The corrected implementation uses adaptive integration in x, with an explicit split at 1-(m_e/M)^2, and 256/512 point quadrature for the second variable. Both independent representations now agree within the stated 2e-6 relative check, as do their refinements. The tolerance was not relaxed.

Sixteen checks pass in canonical run_v2: two exact coefficient checks; three representation comparisons; six refinements; three positivity/upper-bound checks; and two diagnostic roots. Its manifest validates. The failed run and check_initial.py are retained for transparency; the original failed manifest refers to the earlier check.py bytes now preserved in check_initial.py and is not the canonical validation target. No new Lean certificate is claimed for QED or the experimental comparison.

Reproduce:

    python3 sol61_push/messenger_electron_moment_2026_10_13/check.py /tmp/messenger_electron_moment_results.json

Related model assumptions are in ../charged_messenger_2026_10_13/REPORT.md, ../threshold_resonance_2026_10_13/REPORT.md and ../stable_source_completion_2026_10_13/REPORT.md.
