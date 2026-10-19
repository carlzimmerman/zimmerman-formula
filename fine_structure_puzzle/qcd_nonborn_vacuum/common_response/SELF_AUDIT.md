# Focused self-audit, FSP-009 C1

Primary verdict: **correct only after the stated restriction**. The exact
vacuum-null comparison requires isospin-symmetric QCD and exchange-covariant
matching. The controlled chiral coefficient requires the source's HBChPT
domain and sequential soft/chiral limits. The full physical R target is
incomplete. This is author self-review, not independent approval.

Audited frozen RAW_DERIVATION SHA256:
`368ef3171872e5f00f02aa64703582829e2d92ed88f6776eb17e5bdb31205fab`.

Dependency graph:

1. Nonanomalous vector isospin change of variables -> W[Q]=W[Q^S].
2. Differentiated regulated action -> complete I_t-covariance metric map.
3. Same flavor change on external interpolators -> proton maps to neutron.
4. Covariant full Born subtraction -> same relation for non-Born tensor.
5. Primary HBChPT source -> p-n electric and magnetic logarithms.
6. Euclidean polarizability action OR low-Q T1/T2 -> SO(4) soft coefficient.
7. Sequential K->0 then M_pi->0 with controlled remainder -> shape limits.

Obligation matrix:

| Obligation | Self-audit result |
| --- | --- |
| Actual QCD comparison, rather than fake spectra | Passed: only conserved charge-current spurions are exchanged on one QCD measure |
| Vacuum disconnected vs proton connected subtraction | Passed: derived separately in RAW (1)--(4); no vacuum factor treated as a proton matrix element |
| Metric, source and matching contacts | Passed conditionally on declared common flavor-covariant regulator; they transform under the same variable change |
| Physical isospin breaking | Out of scope; exact null claim is not asserted there |
| Pole/non-pole Born convention | Passed by source paragraph following companion (8), with inherited full Born definition |
| Source coefficients | Passed: exact versions retained, (7a),(8a) subtracted and cross-checked against source (10) and companion (15),(16) |
| Electric-only vs full angular contraction | Passed: worldline E/B covariance and parent T1/T2 independently yield a-b |
| Euclidean sign | Passed in self-review: magnetic static energy is -2pi b_M B^2; Wick rotation reverses electric relative sign |
| Chiral logarithm vs analytic contacts | Passed at displayed q^4; full asymptotic limit conditional on standard power counting/remainder control |
| kappa_s=0 exception | Passed: explicit, and no nonzero soft mass logarithm claimed on that branch |
| All-momentum scalar cancellation | Not addressed: no claim that full M_u is nonzero follows from the soft window |
| A_rho existence, value or derivative | Not addressed; only a conditional charge-odd null relation if the limit exists |
| Calibration path | Passed as bookkeeping: fixed-theory symmetry is kept distinct from inherited proton-mass projector |
| V2 execution provenance | Passed: completed manifest validates with all current input hashes |

Strongest safe statement: the full proton non-Born tensor cannot be
reconstructed by the stated flavor-covariant vacuum trace/current Ward
identities alone, since a genuine QCD low-energy isovector electric
logarithm lies in the exact kernel of the unconditioned-vacuum comparison.
The full soft mass functional has the additional cancellation and explicit
kappa_s-dependent logarithm shown in RAW (10),(11).

Smallest remaining implication for the original cancellation proposal:
evaluate whether all non-Born momenta, subtraction functions and finite
matching combine to cancel the scalar p-n response, then address the
independent isospin-even vacuum response. The present computation does not
settle either. The cheapest fresh review is to derive RAW (7)--(11) without
reading check_common.py, then check the isospin/contact map from the actual
regulated generating functional.
