# Independent review of W4-02

2026-10-20. Primary verdict: **proved as written**, at the explicitly
specified effective-sector scope. This verdict concerns the nonselection
propositions, not a derivation of the coefficient or a completed theory.

An isolated fresh reviewer read PROOF.md and the frozen criteria before
checks.py, without the author's route narrative or other agent reports.
It reconstructed the field variations and characteristic speeds independently.
No scripts were executed by the reviewer. The coordinator subsequently ran
and validated the symbolic evidence. Agreement is not a formal certificate.

| Obligation | Result |
|---|---|
| Dimensions, Gauss normalization, all n>=2 | Passed |
| Potential and polarization variations, including attractive source sign | Passed |
| Convexity, origin regularity, zero source variation | Passed in stated sector |
| Algebraic simple-mu law | Passed with stiffness contribution omitted |
| Preferred-frame energy and local cones | Passed at constant finite g>0 |
| Supplemental quadratic integral, law and cones | Passed analytically |
| Continuous physical coefficient freedom | Passed |
| Restricted rational-function pi lemma | Passed |
| Covariant completion, coupled cosmological stability, global nonlinear evolution | Out of scope |

The reconstructed vector equation is

    Q=grad Phi-K_n P,
    div Q=K_n rho_b,
    Q-K_n W'(K_n|P|) P_hat+gamma Delta P=0.

At gamma=0, positive spherical flux has outward grad Phi and attractive
physical acceleration `-grad Phi`. The source signs need no repair.
The radial W extension is C^2 at the origin with zero Hessian. The source
variations and stiffness vanish at the identically zero P background;
no unspecified covariant stress tensor was inferred.

For the scalar, direct variation gives

    Phi_tt/(K_n c^2)-div(E'_a(g) grad Phi/g)=-rho_b.

The Hessian factors in PROOF.md give exactly its stated speeds. The
quadratic-member integral differentiates to h_a. Degeneracy at g=0 is
properly excluded. The pi lemma also passes: algebraicity is transitive,
so pi is transcendental over the algebraic-number field, and the rational
function identity has the impossible order `1+2 ord_0 R=0` at zero.

Initial implementation review found two coverage limitations: quadratic
formulas were not yet in the checker, and dimension was checked in two
examples rather than an explicit mutation. These were disclosed before
revision in SUPPLEMENT.md. A follow-up delta review passed C28-C34:
the mutant selects n=4 and its n=3-baseline check fails; the additional
quadratic derivatives and factorizations match the analytic proof. Earlier
C01-C27 checks were unchanged. Claim C remains analytically audited.

Exact reviewed SHA-256 artifacts:

    PROOF.md
    bcc94c7648fdd181ba8c520f1ce8e66f3ec9bdecba74ad604ea98ed991185dfa
    FROZEN_CRITERIA.md
    8c0a7314e76e6a34171e2eaf10a5e0d7c7ebfa2496f2414e70cbcfb471b7333e
    SUPPLEMENT.md
    0fe255f3caeff3db5e5cc4dd4a4928149de892c53136a809c5d76171abb2cf3e
    checks.py (final delta)
    55fe8d4aa676e0ce430e7490eaeca62958c970b5c8df04e13182f4c490e36e25

Base checkpoint: `177591c05a384bc07c819e3fe0d5517aa8798cb4`.
Criteria: `72a3b470d7eaf1b05d386f61694d275b9889b793`.
Supplement: `05b047a17`.

No further restriction was needed beyond the written hypotheses. The
remaining research implication is an independently selected normalization
that distinguishes a quarter from the continuous family. Unknown
microscopic completions were not refuted or exhausted.
