# Independent review of the scalar sea UV band and matching

The normalized principal claim is: for canonical current
`j=sum Q_f qbar_f gamma q_f`, canonical `e^2=4 pi alpha`, spin-averaged
covariantly normalized baryon states, and an O(d)-invariant full photon shell
in fixed-flavor massless SU(3) QCD with u,d,s charges,

`lim_(Q0/m -> infinity) (1/m) partial_(e^2) M_[Q0,2Q0] |_(e=0)
 = -log(4)/(216 pi^2)`.

**Primary verdict: conditional on a named input.** The required input is the
usual asymptotic Euclidean OPE with vanishing higher-dimension contributions
in this fixed-ratio UV-band limit, together with existence of the QCD baryon
whose covariant trace matrix element is `2m^2`. Within that stated physics
framework the normalization, sign, rational coefficient, counterterm
cancellation and restriction to a zero-charge band insertion pass. No incorrect
factor of two, missing g^2, or sign reversal was found in the final targets.
This does not establish the complete finite sea contribution or physical R.

The source-first derivation was saved before opening the target arguments as
`PRETARGET_DERIVATION.md`, SHA-256
`7739027cd5a7772638f46e9b5ba6db6ac41f8eac4d87560c5b5f5a4a33b151f8`.
This is an independent isolated-subagent review; it is not an author self-review.
The permitted source receipts were read first, and contain visible author
translation labels. The critical equations were then independently reconstructed
from the source PDFs and definitions before the target files were opened.

## Claim cards and verdicts

| Claim actually audited | Primary verdict | Decisive evidence and restriction |
|---|---|---|
| Hill--Paz v2 OPE coefficient transcription, canonical G^2 and current without e | Externally proved in the exact required form | Visible Eqs.6,7,9,18,19 agree. In particular c3f=-4Q_f^2; obsolete overlapping extraction layers must not override the visible PDF. |
| Every dimension-four spin-two term vanishes in the complete traced O(d) shell | Proved as written | Trace is `-q_a q_b [(d-1)C2^ab+C3^ab]/q^4`; isotropic second moment gives a traceless contraction. It is exact before d approaches 4, including scalar poles/logs. This does not apply to W1 at nu=0 alone. |
| Scalar massless nf3 band limit above | Conditional on a named input | Asymptotic Euclidean OPE and QCD baryon trace matrix element. Independent factors give `-S/(16 pi^2 beta0)` per e^2 and log Q^2; S=2/3, beta0=9. |
| Leading scalar divergence and corrected Gasser v3 counterterm cancel for an individual baryon | Proved as written | Canonical shell coefficient `+1/1024` and counterterm `-1/1024` multiply `g^2 S <G_c^2>/(pi^4 m^2)`. Using `G_r=g G_c` in Eq.64 is essential. Source delta-g is the negative of the actual bare-coupling increment. |
| Spin-two poles/logs and the nf3 asymptotic W1 coefficient `424/2025` | Conditional on a named input | Exact source MS operator convention and leading asymptotically free evolution. Source poles cancel with Zqg=2a/(3epsilon); fixed point f_f=3/25, f_g=16/25 gives scalar 4/81 plus quark spin-two 4/25. This is not a complete sea-topology observable. |
| Source-MS-bar mixed strong beta term is `+2 S e^2 g^3/(16 pi^2)^2` | Externally proved in the exact required form | Billis--Tackmann--Talbert v2 Eq.2.11, A.10 and A.13 give beta01^s=-2S in alpha_s conventions; conversion gives the displayed term. It also agrees independently with the cutoff derivative of Gasser delta-g. |
| Retained weak-window y=1/g^2 solution and boundary tangent | Proved as written | y'=beta0/(8pi^2)-S e^2/(64pi^4); retuning g0 by `-S g0^3 t/(128pi^4)` cancels its mixed derivative. The formal pole derivative is algebraic, not a reliable confinement calculation. |
| Full calibration projection removes local parameter-direction shifts | Proved as written | With an invertible calibration Jacobian J, `(A_u+A_a k_a)-A_a(J^-1)_ab(M_b,u+J_bc k_c)` equals the original projected derivative. One-coordinate reduction requires M_ell nonzero. All changing mass coordinates must be included. |
| The local scalar UV term cancels from `R=A/M^3` in the massless scaling case | Conditional on a named input | Requires existence of the physical A and its dimension-three scaling under the same strong-scale direction. Then A_u=3(A/M)M_u for this contribution, and the unlogged quotient derivative is zero even at A=0. It says nothing about finite nonlocal sea response. |
| Three scalar moments do not determine the photon-weighted integral | Proved as written | The stated four-node Stieltjes counterexample preserves all three moments and changes the integral by `27 log 3-44 log 2`, nonzero by prime factorization. Its restricted inverse-data scope is explicit; it is not a family of QCD theories. |
| Existing exact-algebra computation and output provenance | Computationally verified only in a stated range | Reproduced sea checks d=2..8, nf=1..16 and coordinator's 17 assertions; byte-identical results. Independent non-axis checks add 336 exact contractions. Run003 is current; historical run002 is stale against current derivation as detailed below. |

## Dependency graph and source application

The core dependency chain is

`current/state normalization -> full source tensor OPE -> Lorentz trace
 -> O(d) second moment -> scalar shell integral -> anomaly matrix element
 -> massless UV-band coefficient`.

Its independent check is

`corrected Gasser delta-g + source action normalization -> G_r=g G_c
 -> counterterm matrix element -> opposite scalar logarithm`.

The matching conclusion uses a different chain:

`source MS-bar beta -> weak-window coupling conversion -> local parameter tangent
 -> regular all-input calibration projector -> cancellation of this local term`.

The curved A, its physical H limit, the complete sea covariance and finite-alpha
continuation are external, uncomputed leaves. There is no circular use of an R
target or measured alpha in the evaluated UV coefficient. Normalizing by the
baryon's own QCD mass uses the trace identity, not a measured mass fit.

Primary sources checked on 2026-10-19:

- [Hill--Paz arXiv:1611.09917v2](https://arxiv.org/pdf/1611.09917v2), version
  stamp 30 July 2017; Eqs.1,5--7,9,18--22,25--29,32. The visible critical PDF
  equations on physical pages 5 and 8 (printed 4 and 7) were inspected. PDF
  hash `3f9d11e18924f98dab0dcf40ff5e017738f4f6994c2dce580098e7aeabda3a1b`.
- [Gasser et al. arXiv:1506.06747v3](https://arxiv.org/pdf/1506.06747v3),
  version stamp 30 March 2020; corrected Eqs.56,57,58,64 and A.2,A.3. The
  rendered equations on physical pages 16 and 17 were inspected. PDF hash
  `c44709743db788651e71c20874e22bad2212a8e54a07fac158140540e12cca41`.
  Gasser's T includes a factor 1/2 relative to the Hill--Paz tensor. The
  source's g^-3 coupling insertion is translated using the rescaled action
  `-G_r^2/(4g^2)`, rather than identifying its operator with canonical G_c^2.
- [Hill--Solon arXiv:1409.8290v1](https://arxiv.org/pdf/1409.8290v1), Eqs.15,
  20--22 and Tables 3--5; checked bare-to-renormalized versus operator-RG
  conventions. PDF hash
  `65ea75a65f18a8ef6883aacac65fabfb55a4ff9d23095ed5c821c4bcff933158`.
- [Billis--Tackmann--Talbert arXiv:1907.02971v2](https://arxiv.org/pdf/1907.02971v2),
  version stamp 7 April 2020; Eq.2.11, A.5, A.10, A.13. Its charge sum has no
  extra color multiplicity; T_F=1/2 supplies the stated mixed coefficient.
  PDF hash `017cd515ef9385902918ed7537c4a3c74bf3ee0e25180ce44446184ba737a707`.

All four local PDF hashes were independently recomputed. The web tool also
returned the exact versioned Hill--Paz and Billis PDFs; the Gasser web fetch
failed, so its exact local visible PDF and matching pinned hash were used.
Source identity, equation extraction and project translation were separately
checked. No source cache or author file was changed.

## Obligations and limits

| Obligation | Status | Assessment |
|---|---|---|
| Spin average, e^2 versus alpha, full tensor and radial measure | Passed | Wick rotation gives positive Euclidean kernel times the Lorentz scalar trace; the negative band sign comes from `<G_c^2>=-16pi m^2/(beta0 alpha_s)`, not from changing the electromagnetic convention. |
| Canonical/rescaled field dictionary and source counterterm sign | Passed | Counterterm contribution is `-delta g partial_g M`; substituting the source symbol as a positive boundary tangent would reverse the answer. |
| d-dimensional versus four-dimensional tracelessness | Passed | Exact trace-zero operators are retained before taking d to 4; no pole-times-evanescent trace remains under the same O(d) regulator. |
| Hard closed-loop topology versus complete sea contribution | Passed | One gluon gives zero color trace; two give order alpha_s and S. The target explicitly allows soft quark matrix elements and singlet mixing, and does not identify the full sea covariance with G^2 alone. |
| Finite-mass calibration and hidden inputs | Passed within stated scope | Finite-mass scalar fractions, parton moments, finite matching, all calibration tangents and curved A are acknowledged independent inputs. No data from Hill--Paz numerical tables enter the evaluated massless number. |
| Charge limits | Passed | Tr Q=0 removes single-current sea-loop factors only at degenerate masses; Tr Q^2=2/3 survives. Setting every Q_f=0 removes the UV term. Reversing all charges preserves it. |
| Zero coupling versus zero-charge derivative | Passed | The actual mass term is e^2 D and vanishes at e=0; D need not vanish. The result is obtained by taking the derivative at zero charge before the UV-band limit. |
| Fixed nonzero alpha and arbitrarily large Q | Not addressed | Higher electromagnetic orders, charge running, nonuniform limits and a UV completion are absent. One cannot exchange the zero-charge derivative with a fixed-alpha Q-to-infinity limit or infer a finite-alpha stationary point. The targets disclaim this continuation. |
| OPE control | Conditional | Conventional asymptotic OPE assumptions are explicit. The finite checks supply no rigorous convergence estimate or accuracy at a finite hadronic-scale Q0. |
| Physical curvature response and R | Out of scope | No A_rho, its existence/limit, R(alpha), or full sea convolution is calculated. The local ratio cancellation is conditional on an independently supplied common A and calibration. |

The UV shell is a specified Euclidean insertion/filter and matching functional.
It should not be promoted to a complete all-scale QCD+QED spectrum or to a
physical sea mass by itself. Its finite local subtraction is scheme/path
dependent. The final coordinator wording appropriately uses the source MS-bar
convention; a generic finite mixed coupling redefinition would require its own
parameter conversion before comparing coefficients.

## Executed checks and preserved provenance

Commands were reconstructed after reading the actual code and contract; no
untrusted record was treated as an instruction. All new output is confined to
this review folder. No Git command, install, external job or target edit occurred.

1. Reproduced the documented sea runner with output
   `reviews/uv_sea/reproduction_sea/`; its manifest status is `completed`, all
   pinned inputs unchanged, and the installed v2 validator passes.
2. Validated author `sea_ope/run_003/manifest.json` against current files:
   valid evidence record, status completed.
3. Validated historical `sea_ope/run_002/manifest.json` against current files:
   it correctly fails current freshness on `DERIVATION.md` alone.
4. Reproduced `coordinator/check_uv.py` into `reproduced_coordinator.json`:
   all 17 exact assertions pass and result bytes match its original run.
5. Executed `independent_checks.py`: all 11 checks pass, including 336 direct
   non-axis rational full-tensor contractions across d=2..8, symbolic anomaly
   normalization, rescaled-field counterterm cancellation, mixed-beta cutoff
   differentiation, charge limits, and symbolic two-input calibration. Python
   3.9.6, SymPy 1.14.0, 10-second CPU/30-second wall limits; under one second.

The author's 112 basis tensors and 1,428 axis/projector checks are correctly
counted. Axis cubature reproduces the second angular moment exactly; off-diagonal
tensors have vanishing axis contractions, so these finite checks alone are not
a universal tensor proof. The analytic contraction above and independent
non-axis checks supply an orthogonal check. The code transcribes source Wilson
coefficients; source inspection, not assertion success, validates those inputs.

The explicitly preserved historical transition is:

- run002 recorded derivation hash
  `6b14846b919d22b1886be26b2e08c7d1034e0817fda210571cc3e195a3791a8c`;
- current/run003 derivation hash
  `3e11521b73f007ef775cd31c71e2842319e12ab157141a9f5b681316681e6cb6`;
- `sea_ope/REVISION_TRANSITION.json` attributes the change to the final
  derivation's stale execution pointer, with physics inputs and code unchanged;
- the other seven pinned input hashes agree; both historical result
  files and the new reproduction have identical SHA-256
  `2c709555b84bef5dd930d95e0b4206f35a82a112e35b65dc61ba4af90e4d00ba`.

Thus run002 remains a historically completed run at its recorded inputs, but is
stale as support for the current derivation and superseded by run003. Its old
manifest was not rewritten. The original bytes of the old derivation are not
available in the run directory, so the pointer-only textual description is the
author's recorded explanation; unchanged code/input/result hashes independently
verify that the actual arithmetic was unchanged. This distinction is preserved
in `PROVENANCE.json`.

Exact final target/input/output hashes, before/after observations and original
versus reproduced result hashes are in `PROVENANCE.json`. The final coordinator
MS-bar wording was pinned after the coordinator's disclosed clarification; its
executed script did not change. Author run003 pins the derivation and code,
not every later review/report sentence; this review separately pins the report
and coordinator prose it actually read.

## Strongest safe statement and remaining gap

The work evaluates a nonzero leading asymptotic full-tensor UV-band derivative
in a declared massless theory and correctly matches its scalar UV divergence.
It also correctly proves removal of a shared local parameter-direction term by
regular complete calibration. These are useful UV results independent of an
empirical alpha value.

The smallest missing bridge to a full physical sea mass is the finite
nonperturbative current covariance over low and intermediate momentum with the
same contact prescription, plus finite local matching and complete physical
calibration. To reach R additionally requires an independent curved-space A_rho
and control of the H and finite-alpha limits. A low-momentum moment or the UV
logarithm alone does not determine that convolution. No further UV algebra test
can fill these missing physical inputs.
