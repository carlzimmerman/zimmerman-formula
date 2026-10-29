# MV28 author self-review

Primary claim: the collective model yields the stated stiffness/sector-energy
formula in its declared leading-log reduction. **Verdict: conditional on the
common-threshold RG reduction and matching hypotheses.** Its algebra and
finite checks pass; its full physical applicability is not established.
This is an adversarial pass by the same author, with no independent-agent
or formal certification. Reviewed hashes are pinned in VERIFICATION.json.

| Obligation | Review result |
|---|---|
| Four-field boson/fermion multiplicity | Passed: six real scalars versus three Weyl fermions, with Weyl weight two. |
| Transverse bound and determinants | Passed symbolically; actual minimum spectra checked numerically. |
| Microscopic Hessian | Passed against a 65-digit potential stencil, avoiding the spectral-Hessian implementation. |
| Source benchmark and small-y controls | Passed in the frozen ranges; they do not certify every parameter. |
| Full scalar pressure | Passed by envelope differentiation; bare kinetic pressure would omit U. |
| First model supplies viable dense halo | Not established; eight cases have a compressional obstruction, ninth reaches finite transverse bound. |
| Collective SU(5) component normalization | Passed: Tr(Ta Tb)=delta_ab for adjoints and conventional gauge trace delta_ab/2 were used consistently. Explicit generators reconstruct symmetric contractions and C_adj=5. |
| Effective F running | Passed by differentiating f lambda/sqrt(lambda^2+30h^2), including both weights' running. |
| Critical-surface curvature | Passed by a separate derivative: on g^2=29lambda^2/200, gamma_eff,t=(16pi^2)^(-2) h^2 lambda^2[174h^2+(1131/8)lambda^2]/(lambda^2+30h^2), giving the stated positive ratio. |
| Finite RG integration | Passed for all nine frozen initial coupling choices. This checks the reduced differential equations, not the complete threshold theory. |
| Common-threshold identification with physical radial field | Conditional; light modes and multiple thresholds require full matching. |
| All transverse quantum modes and lifetime | Not addressed for the collective model. Radial positivity is not full vacuum stability. |
| Full cosmological vacuum energy | Incomplete; canonical K, absent W0, weak-gravity hierarchy and omitted sectors are substantive assumptions. |
| Unique B/V | Refuted within the displayed leading-log family: uniform coupling scaling preserves the stationary relation and tree height but changes the ratio as t^4. |

The two-sector RG continuation was checked separately. Its SU(2) holomorphic
power is a building block; canonical Kahler metric and controlled heavy
thresholds are additional conditions. The decreasing F sector was not
constructed, and same-F interference cannot be dropped. This package is not
silently counted as part of the successful collective model.

The numerical contracts cover every listed grid point and retain the one
case without a pressure-zero. No unwanted case was filtered from the model
inventory. All runs passed on their first attempt; no post-result tolerance
or input was changed. Floating-point tolerances, library behavior and
leading approximations remain explicit limitations. There is no novelty
claim for the known supersymmetric models or source formulas.
