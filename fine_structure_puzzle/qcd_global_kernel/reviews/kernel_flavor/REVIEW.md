# Independent flavor and proton-kernel audit

**Primary verdict: correct only after a stated restriction.** The restriction
concerns sea_flavor/DERIVATION.md equation (8) when one-current sea means are
allowed to be nonzero: photon integration adds `G_ab C_a <L_b>`. In the intended
charge-conjugation invariant QCD vacuum those means vanish, so the advertised
physical application remains covered. The fixed-source Hessian (2) is exact
without this restriction. The full Born angular kernel, arbitrary-Pauli soft
cancellation, point-Dirac integral and separate elementary MSbar finite matching
pass the analytic and bounded computational checks below. A complete physical
QCD mass or curved-vacuum response is not evaluated.

## Claim cards and exact revision

1. At a finite nonsingular regulator, with common flavor-independent source
vertices and additive scalar masses, differentiate a normalized proton
contraction at eta=0. Resolve same-loop, mixed and separate-loop sea classes,
their exact 2+1 flavor factors, local SU(3)-splitting orders, covariance bounds,
noise bias and metric contacts. The covariance bound additionally needs a
positive normalized gauge measure and finite displayed moments.
2. With relativistically normalized, spin-averaged proton states, canonical
e-stripped current and u=e2, integrate the **complete** on-shell spin-1/2 Born
tensor over the Euclidean photon angles. Establish the local charged-proton
soft coefficient under a stable, massive-QCD spectrum and analytic form factors;
then separately evaluate the complete point-Dirac verification theory with
sharp photon windows, double-PV regularization and its one-loop MSbar conversion.

The 15 exact frozen author-file pins are in INPUT_HASHES_BEFORE.json and
INPUT_HASHES_AFTER.json. All are unchanged. They include both derivations,
the flavor bound, all three scripts, the requested inputs/source receipts,
the three author manifests and the separate MSbar contract. The current
scientific result/output pins are also checked by their manifests; the exact
manifest hashes, argv and validation responses are in FINAL_PROVENANCE.json
(the earlier seven-run checkpoint is VALIDATION_AND_HASHES.json).
No author file, result or manifest was rewritten.

## Independence and dependency graph

This isolated reviewer saved PRETARGET_DERIVATION.md before reading the author
reports, derivations, inputs, scripts, results or manifests. Only the delegated
claim, filenames and permitted sea source metadata had been seen. Its direct
quotient, resolvent, gamma trace, angular integral, Pauli cancellation, point
primitive and PV asymptotic were then compared with the author package. The
pretarget tensor amplitudes use half the WLCM amplitudes and twice their
prefactor; the resulting radial kernels agree exactly after this translation.

The dependencies are:

    determinant/source derivatives -> normalized-source quotient Hessian
      -> exact flavor reduction -> orders / moment bounds / noise conditions
      -> photon-integrated normalization -> vacuum insertion -> metric response

    Born tensor + nonpole term -> full T1/T2 angular integral
      -> local soft endpoint (QCD gap/analyticity input)
      -> separate point-Dirac full-Q integral -> PV UV asymptotic
      -> elementary d-dimensional finite MSbar matching

The source identities and finite algebra are checked internally. External
normalization/regulator leaves are checked against exact primary versions in
SOURCE_CHECKS.json. The massive-QCD gap/analyticity and absence of extra
massless states are named physical inputs. Full physical current-tensor and
curved-vacuum data are unprovided inputs, rather than negative theorems.

## Obligation matrix

| Obligation | Status | Decisive check and scope |
|---|---|---|
| Determinant signs and contacts | Passed | L_a=sum q Tr(SV); L_ab=sum q2 Tr(SW-SV_aSV_b); H and H+UU are distinguished. |
| Normalized fixed-source Hessian | Passed | Exact quotient differentiation yields valence, two mixed covariances, same-loop covariance and the full third cumulant, including nonzero means. |
| Charge and flavor factors | Passed | U_a=delta Tr(S_l S_s V_a)/3; H_ab=(5h_l+h_s)/9; sum q=0 does not cancel sum q2=2/3. |
| Resolvent and local splitting orders | Passed | Exact common-operator identity; mixed O(delta), separate-loop O(delta2), same-loop O(1), with regularity and path qualifications retained. |
| Residual bounds | Passed | Complex bilinear covariances bounded by Hermitian variances; centered-product variance controls the third cumulant. Sample moments are explicitly not certified population error bars. |
| Auxiliary-noise products | Passed | Independent pools or off-diagonal pairs eliminate conditional noise covariance; gauge covariance remains physical. |
| Integrated baryon equation (8) | Correct only after restriction | Requires G_ab C_a <L_b>=0, or addition of that term. See NORMALIZATION_CORRECTION.md. |
| Vacuum equation (9) | Passed | Photon integration requires uncentered <L_a L_b>; the frozen author expression retains this correctly. |
| Metric contacts and UV/path terms | Passed as formal identities | Equation (10) differentiates photon kernel, vertices, regulator weights, measure and counterterms. It supplies no numerical S4 limit or matching Jacobian. |
| Full Born normalization | Passed | WLCM factor-two amplitudes and Cottingham prefactor give the independently derived radial kernel. Feng-Jin's 1/(2m) external normalization is consistent. |
| Born subtraction/nonpole term | Passed | WLCM elastic contribution plus Born subtraction equals the complete kernel; -2F1 squared is essential. |
| Arbitrary-Pauli soft endpoint | Passed conditional on named inputs | For F1(0)=Z and arbitrary finite F2(0), -Z2 z and +Z2 z cancel. For Z=1 the e2-normalized coefficient is 1/(4pi2). |
| First soft corrections | Passed in local massive-QCD scope | Form-factor slopes enter O(Q2); a non-Born tensor uniformly O(Q2) contributes O(epsilon4) after radial integration. No full-radius/chiral/global-curvature inference follows. |
| Point-Dirac radial normalization | Passed | Explicit 4x4 gamma trace independently reproduces the full angular numerator, primitive, cutoff-band value and UV coefficient. |
| Double-PV integral and constant | Passed | Full positive-line convolution; asymptotic constant (3/2-6log2)/(16pi2), distinct from a finite counterterm. |
| Separate point MSbar appendix | Passed | Evanescent numerator contributes -1; finite log integral contributes 5, giving 4. PV-to-MSbar finite term is (5/2+6log2)/(16pi2). Elementary theory only. |
| Full QCD or alpha determination | Not addressed, explicitly excluded | No complete physical tensor, all-Q form factors, inelastic response, sea ensemble moments, QCD finite matching or global curved vacuum was supplied. |

## Decisive formulas

Writing z=Q/(2m), A=F1 squared+z2 F2 squared and
C=(1+z2)A-3z2(F1+F2) squared, the complete e2-normalized Born radial kernel is

    K_B(Q) = [C(sqrt(1+z2)-z)+z(3F1 squared-A)/2]/(4pi2).

Its linear coefficient is `-F1(0) squared+F1(0) squared=0`, independent of the
Pauli moment. With F1=1+a z2 and F2=kappa+b z2,

    4pi2 K_B = 1+[-3/2-6kappa-2kappa2+2a]z2
                    +[2+6kappa+3kappa2/2]z3+O(z4).

Since a=kappa-(2/3)m2 r_E squared, this is exactly the author's radius form.
It only controls Q much smaller than m and the hadronic threshold scale. The
point specialization is `[(1-2z2)sqrt(1+z2)+2z3]/(4pi2)`, with the UV
coefficient `3m/(8pi2 Q)`. No heavy-pion form factor or temporal-moment
interpolation is used as a complete QCD tensor.

The only companion correction is derived explicitly in
NORMALIZATION_CORRECTION.md. It also corrects the reviewer's pretarget generic
vacuum line: the Hessian of -log Z(eta) contains Cov(U_a,U_b), whereas the
photon-integrated W_u contains <U_a U_b>. The pretarget file is preserved.

## Bounded computation and current validation

All commands were constructed after reading the relevant scripts and documented
reproduction procedures. No command stored in a manifest was executed. The
installed computation-audit runner wrote only fresh directories below this
review's owned directory, with 30-50 second wall and 20-40 second per-process
CPU caps and one conventional numerical-library thread.

* `independent_run_001`: completed; 30 exact checks, 15 angular cases and five
  complete double-PV integrals at 65-decimal precision. It uses direct
  exponential quotient differentiation, distinct noncommuting 3x3 matrices,
  a complex-valued Cauchy-Schwarz example, explicit gamma matrices and theta
  quadrature. Maximum angular comparison discrepancy is 1.77e-62.
* `sea_reproduction_001`: completed; 174 exact checks over the author's three
  explicit 2x2 configurations, two source coordinates and four mass splittings.
  Result byte-identical to the frozen author result.
* `proton_reproduction_001`: completed; 14 exact identities, 24 angular cases,
  five sharp windows and ten full double-PV integrals. Result byte-identical.
* `msbar_reproduction_001`: completed; six exact/translation assertions and
  ten saved-PV translations. Result byte-identical.
* `pauli_run_002`: completed; 21 additional exact symbolic checks of the full
  arbitrary-F1/F2 Born tensor from two explicit gamma-matrix graphs: all 16
  components, four Ward identities and the Lorentz trace. The rational identity
  holds for symbolic energy and spatial momentum, off the poles, with common
  analytic continuation. This is a posttarget orthogonal verification. The
  original `pauli_run_001` failed because the reviewer's literal zero comparison
  rejected SymPy's unevaluated `0*I`; its input and failed manifest are preserved.
  The v2 input adds zero canonicalization only. See PAULI_DEBUG_NOTE.md.

The independent theta-transformed PV values at Lambda/m=0.1,1,16,1024 differ
from the author's saved 48-digit results by at most 2.01e-49. This is numerical
agreement, not interval certification. At Lambda/m=1024 the matched point value
is approximately 0.02533118527953, still 8.89369e-7 above its exact asymptotic
limit 1/(4pi2)=0.02533029591058. Finite cutoffs are not called the limit.

All **nine** current manifests (three author, six review) validate against
current files: eight have run.status=completed; the preserved initial Pauli
implementation failure has run.status=failed. It is not mathematical negative
evidence. FINAL_PROVENANCE.json records this final validation. The author result SHA-256 values,
reproduced exactly, are:

    sea:    341d43ec7fbf4d193b1281c82016477ea8c4d5d41b5cf239e8a75ec84139cd03
    proton: 49f568fe65985b2566e2aecda47f103e8ce5c7de7ea70d4205e4d6c824dbaf83
    MSbar:  1cf139d78cb9ec55ae57ee9ef5894a61154bbf720e7ecbecb298ecfbcb438144

## Sources and remaining gap

Fresh primary arXiv metadata/version histories authenticate 2301.03995v2
(2026-05-01, including its equation (8) correction), 2506.19770v1 (2025-06-24),
1812.09817v1 (2018-12-24), 1203.0254v2 (2012-06-03), and 2603.13086v1
(2026-03-13). Local PDF/text bytes match the receipts and their version headers.
The exact used equations, retained hashes, failed initial versioned fetches and
authentication limits are recorded in SOURCE_CHECKS.json. A new remote PDF-byte
comparison was not performed. The checks cover only the listed equations and
scope statements, not every theorem or numerical result in those papers.

Harris et al. supports the flavor-difference/split-even strategy; the 2025
comparison is an unphysical-mass, fixed-ensemble HVP test; the 2026 work supplies
the regulator and factorization method and explicitly excludes its counterterm.
None supplies a complete physical proton or curved-vacuum dataset. The author's
bounded acquisition result is not promoted to a theorem that no such data exists.

The strongest safe result is therefore an exact finite-regulator flavor
decomposition and residual-moment bound, a conditional physical-proton local
soft endpoint, and an analytically and numerically checked complete elementary
Dirac benchmark including its own finite MSbar conversion. The cheapest next
physical check requires actual ensemble estimates of the omitted sea covariance
classes or a declared full-tensor dataset; rerunning the finite fixtures cannot
produce those inputs. No alpha fit, QCD certification, external large job,
installation, author message or Git mutation was performed.

Final proofreading covered only this review, PRETARGET_DERIVATION.md and
NORMALIZATION_CORRECTION.md. No author edits or mathematical-token changes were
made. The pretarget vacuum-normalization issue is corrected transparently in
the companion, rather than silently changed in the original derivation.
