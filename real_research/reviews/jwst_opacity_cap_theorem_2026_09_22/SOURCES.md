# Primary-source check and limits of novelty assessment

Checked2026-09-22. The mathematical proof is written out in THEOREM.md;
external references below identify standard machinery and adjacent results,
not an external proof of the displayed opacity-cap bound.

1. Zhaoyang Liu, Yong Jiao and Guoxin Liu, *Measure-Valued Generators of
   General Piecewise Deterministic Markov Processes*, arXiv:1704.00938v3,
   26April2017. [Primary PDF](https://arxiv.org/pdf/1704.00938v3).
   Definition5.7 and Theorem5.8, equations5.7–5.10, pp35–36, inspected again.
   The generator is deterministic-flow differentiation plus jump rate times
   the kernel difference, under flow regularity and jump-integrability
   conditions. Our flow is straight travel, kernel is the stated Thomson
   law, and bounded rate/increments satisfy the finite-horizon conditions.
   Time can be an extra deterministic coordinate. We stop on reaching the
   boundary; no reset-at-boundary rule is assumed. The local-martingale
   assertion does not alone justify unbounded stopping: the separate tail
   and dominated-convergence arguments in Sections2–4 supply that step.
   Classification: known methodological input, not novelty.

2. A. Zoia, E. Dumonteil and A. Mazzolo, *Collision statistics for random
   flights with anisotropic scattering and absorption*, arXiv:1110.0789v1,
   4October2011. [Primary PDF](https://arxiv.org/pdf/1110.0789v1).
   Header, introduction, SectionIII equations26–37 and SectionIV inspected.
   The paper derives collision-number moments via equilibrium kernels and
   discusses a diffusion-limit relationship to residence-time moments.
   This verifies that random-flight moment methods and anisotropic scattering
   statistics are established. The inspected material is not the exact
   finite-speed central Thomson D=T-Z opacity-cap inequality. Classification:
   adjacent result only; no conclusion about the rest of the literature.

Prior authenticated repository notes also cover Hua's inhomogeneous transport
and density-dependent timing papers. See ../jwst_radial_variance_audit_2026_09_22/SOURCES.md
and its analytic/SOURCES.md. Neither density-sensitive photon timing nor the
generator/martingale method is claimed as a discovery here.

This visit used the web index with queries:

- "radiative transfer" "variance" "lower bound" escape time
- "photon" "escape time" "opacity" "variance" bound
- "Thomson" "delay" "variance" bound sphere
- "random flight" "variance" "first passage" bound
- photon residence time moments bounded scattering rate sphere variance lower bound

Coverage: English transport, first-passage, residence-time and astrophysical
terminology; sources indexed by the current date. Many hits were unrelated
estimator-variance bounds and were not treated as evidence. Primary arXiv PDFs
were opened directly for the strongest methodological/adjacent candidates.
No exhaustive backward/forward citation graph or independent second database
search was completed. A failed exact-match search does not establish priority.

**Novelty remains unverified.** The result can be called a proved model theorem
in this repository, with the self-review provenance stated. It cannot yet be
called an independently established new physical law or a JWST discovery.
