# W4-04 scoped proof review

Date: 2026-10-20. Primary verdict on PROOF.md A-E: **proved as written,
within the explicit restrictions**. This is a verdict about the displayed
normalization calculations and failures of the specific operational bridges.
It is not a derivation of xi, a complete dynamical model, or a global no-go.

| Obligation | Outcome |
|---|---|
| A: flux, force-calibrated G, deep-MOND a0, invariant xi | Passed |
| A: positive field rescaling and common-factor cancellation | Passed |
| B: canonical SUSY BI action, restricted electric quarter | Passed |
| B: actual electric tail and fixed-V response deformation | Passed |
| C: thermal coefficients, ratios, signs, slope deformation | Passed |
| D: finite spectral sums, positive log signs, curvature deformation | Passed |
| D: induced scalar slope and low-curvature consistency failure | Passed |
| E: restricted D3 electric-component dictionary | Passed |
| E: fixed-parameter KKLT differentiation and radial curvature | Passed |
| Full BPS endpoint force, complete gravity stability, all-orders protection, exact flux realization | Out of scope |

The reviewer reconstructed A from spherical flux and independently derived
the actual BI electric field and canonical electric coefficient. The
thermal ratios were rederived from the primary free-energy expansion.
For D it independently established the log signs via equal-moment cubic
root families and divided differences; it also checked the exact rational
interval implementation. The induced H bound follows from the same
coefficient intervals and limits, rather than validates, its cosmological
interpretation.

A separate isolated E reviewer rederived the D3 dictionary and KKLT
stationary/curvature identities, holding W0 and D fixed during field
differentiation. Review caused three explicit restrictions: s>0 in A,
positive gamma and N in C's ratios, and fixed-embedding electric-component
meaning in E. E also names the GKP no-scale background and restricts its
stability statement to the displayed real-modulus EFT with a,sigma,A>0.
All are incorporated into the final proof before its final bounded runs.

Checker review was read-only and not executed by the reviewers. It found
the implemented exact identities consistent. K02-K03 explicitly instantiate
n=3; general-n flux is proved analytically. K25 uses epsilon=3|F| as an
input to its ratio, with the equation of state supplied independently by
thermal thermodynamics. K32's nonzero conclusion also uses the analytic
inequality 27/16>1. A test count is not a replacement for these arguments.

Coordinator execution: final normal **39/39**, exit 0; final mutant
**34/39**, exit 1 as expected, with K07,K08,K11,K14,K23 failing. Both final
v2 manifests validate against current input hashes. The reviewer did not
claim to execute these runs.

Exact reviewed SHA-256:

    PROOF.md
    abc7d1d4751a37edbc72d5f05061934225cea341f03c01831986c41a787fe9eb
    FROZEN_CRITERIA.md
    f416883960890becf54dde2a2c37f5ee68b9aab9cc7249406cbeca1a602a8b0d
    VERIFICATION_SCOPE.md
    31a1a17fae8fd23d50492c1601cd2f225a3b1f9d37aae8555160d6700cf87889
    checks.py
    67fffde1bb73caff53963d8414340d295dfc3637f61bc78a27c1be70379409ef

Review-time HEAD was `132b11e3837787c138d7427aa9c83e86af42abaa`, with
the new proof/checker then uncommitted and unrelated concurrent work.
The hashes above pin the actual artifact rather than relying on HEAD alone.

Independence limitation: the main reviewer initially received only raw
artifacts and sources and independently reconstructed the main algebra.
An agent-inventory call later exposed earlier route summaries, so this
review was not fully blinded throughout. The separately spawned E reviewer
received only raw artifacts and source identifiers and remained blinded.
Neither reviewer edited files or downloaded sources. Source locators are
in SOURCES.md. Agreement is not a formal proof certificate.
