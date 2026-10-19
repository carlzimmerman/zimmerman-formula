# Self-audit of the physical electromagnetic lane

Primary verdict: **conditional on a named input**. The named inputs are the
four hypotheses in DERIVATION.md section 5 and, for differentiating A_ρ itself,
a further uniform charge/small-curvature interchange. The raw mathematical
spectral identities and finite EFT trace are hand-derived claims; the full
QCD application is explicitly conditional.

| Obligation | Status | Evidence / limitation |
|---|---|---|
| Canonical order-e² sign and UV contacts | Passed at fixed regulator | Direct Gaussian integral; exact RM123-v1 insertion framework |
| Stress differs from action density | Passed | ρ=(1-D/4)f, including the H⁶ factor -1/2 |
| Metric derivative includes more than flat JJ | Passed | δD term, connected TJJ and local contact variations explicitly retained |
| Positive flat-current spectral analytic domain | Conditional on ordinary unitary spectral axioms and given positive gap | Subtracted dispersion and bound derived; not promoted to all mixed metric correlators |
| Maxwell rough/Hodge conversion | Passed | Add Ric=3H²; l=1 eigenvalue 6H², multiplicity10 |
| Photon scalar gauge zero mode | Passed | Canonical V^-1/2 quotient, not an omitted normalization |
| Anomaly sign in stipulated Euclidean convention | Passed | W=-logZ, -ζ_T+ζ_scalar+2=31/45 |
| Negative-integer zeta limits | Passed by hand; finite arithmetic checked | Hurwitz pole residues -17/64 and 13/384 retained |
| Entire physical H⁶ coefficient determined | Failed if asserted | c_R and pure-gravity matching not supplied; report never asserts it |
| H coefficient absent under section5 assumptions | Passed as conditional argument | Wilsonian/local expansion, actual low photon spectrum, differentiated remainder bound |
| Section5 assumptions proved for full QCD | Not addressed | Explicit missing dynamical/global-state arrow |
| Flat gap alone excludes global soft enhancement | Refuted as an inference | Kinematic positive transverse finite-mode countermodel, not a local QCD construction |
| Soft insertion gives fixed-alpha A_ρ | Failed if asserted | Exact finite-charge Gaussian log determinant demonstrates nonuniform expansion |
| Full-QCD no-go / alpha selector | Out of scope and not established | No fitted coefficient or physical selector calculation |

Independent checks: exact zeta and Bernoulli arithmetic was compared with a
heat-sum representation using the original spectrum. The finite Dirac moment
uses a separate spectral integral. Both run manifests validate, and only
run_002 has status completed. The run_001 failure is environmental and not a
negative mathematical result. The monotone tail formula is analytic, while
its decimal evaluation uses non-certified mpmath quadrature.

Proofread scope: all newly written DERIVATION.md and REPORT.md prose/equations.
Routine notation checks completed. Mathematical-token typo changes: none.
The substantive strengthening of the global remainder hypothesis to an explicit
exponential bound was part of the research derivation before this proofread,
not represented as a proofreading correction. No source/scientific bytes
outside this lane were edited. No neutral_interactions content was read.

Provenance: same-author self-review, no independent reviewer in this lane;
repository base commit 9516ee01c79f35c04b7556050669ba77b0c98b99 with dirty
workspace, as recorded by the bounded runner. Final lane hashes are in
ARTIFACT_SHA256.txt. No novelty claim.
