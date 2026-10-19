# Fresh review packet

Owner/base: hard_bridge, FSP-009 -> prospective FSP-010. Write review
outside the frozen hard_bridge scientific inputs. Start from the exact
primary source and definitions, reconstruct the implication independently,
and only then inspect author outputs.

1. Read SOURCE_ADMISSION.json and the corrected primary source
   arxiv:1506.06747v3, sections 6.1/6.3 equations (56)-(57),(64), plus
   summary items 3-4. Confirm operator matching obligations and the actual
   status of Reggeon dominance. Cache lookup before retrieval is available
   by PDF hash c44709743db788651e71c20874e22bad2212a8e54a07fac158140540e12cca41.
2. Starting from canonical `D_s(Q)=1/(Q^2+s)` and
   `h_n=(-1)^n s^(n-1)f^(n)/(n-1)!`, derive its finite-L integral,
   endpoint signs and UV-log-subtracted formula. Check sufficient lower
   endpoint and remainder hypotheses. Determine the required finite UV
   matching datum before reading the author's numerical values.
3. Independently combine the massive photon and free Dirac denominator in
   d=4-2epsilon and fixed MSbar mass. Keep evanescent numerator terms;
   derive the heavy-photon endpoint and compare to DERIVATION.md(7)-(8).
   Check that any canonical-theory finite matching is not mistaken for a
   new independent coupling or a pointwise decoupling limit.
4. Then inspect DERIVATION.md, CONTACT_AND_BAND_COMPANION.md,
   check_reconstruction.py, COMPUTATION_CONTRACT.json and run_001 output.
   Check radial/parameter normalization, quadrature scope and frozen
   provenance. Review equation (12) only as the leading quark sector,
   with no gluonic or all-orders closure claimed.
5. Check the scalar Ward rank test and conditioned Feynman-Hellmann
   statement. Identify whether they justify any physical QCD no-go
   stronger than the explicit missing-input assertion.

Report an exact scoped verdict, remaining inputs and any correction.
Agreement with author output is not itself a proof certificate.
