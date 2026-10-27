# FSP-009 common-response clean independent review

## Primary verdict and normalized target

**Primary verdict: conditional on a named input.** The named input is a
controlled SU(2) HBChPT remainder, with fixed chiral-limit LECs, sufficient that
its log-M_pi derivative vanishes in the stated sequential soft-then-chiral
limit. Under this standard EFT hypothesis, the bounded exact comparison and
leading-log claim pass. No discrepancy was found in the critical coefficient,
Wick sign, complete soft contraction, kappa_s exception or order of limits.
The exact flavor-covariance comparison itself does not require a chiral
expansion and passes under the explicitly stated covariant-regulator/matching
hypotheses.

Target: for m_u=m_d>0, Q'=SQS^{-1}, compare the full unconditioned vacuum
functional W[g,u;Q] with the same-proton Born-subtracted two-current tensor,
and verify the primary-source O(q^4) polarizability log and its complete SO(4)
soft-ball contraction. Here u=e^2, a=alpha_E/u, b=beta_M/u and
kappa_s=kappa_p+kappa_n. The audited raw target is
common_response/RAW_DERIVATION.md, SHA256
368ef3171872e5f00f02aa64703582829e2d92ed88f6776eb17e5bdb31205fab.
The title of this review does not turn the source EFT expansion into an exact
nonperturbative computation.

## Independence and chronology

This fresh subagent first derived the mathematical objects and their covariance
from the supplied definitions, then pinned PRETARGET.md before opening any
primary PDF or author raw/coefficient/source-summary/code/result/report file.
PRETARGET.md SHA256:
c56fdcc3163b9cd94c9e13029d1a6c2093b9f1cb2fbad90d5db37116a6a2df2f.
No candidate coefficient was provided. In particular alpha-minus-beta and its
Wick sign were derived before seeing author material.

The two primary PDFs were then extracted afresh directly, with relevant full
pages visually inspected, and SOURCECRITICAL.md was pinned before author
inspection. SOURCECRITICAL.md SHA256:
8be485383085939855fb087de703c2d1397e66ccd969fe23c7fb4d0a0988db0c.
It contains the independent source subtraction, the full field-strength tensor
contraction, a photon-mass-regulator cross-check, exceptions and limits. Source
page renderings and full-text extractions were transient and removed after
inspection; their observed extraction hashes remain in pre_author_pins.json.
The author's existing text extractions were not used for the blind source check.

After those two notes were pinned, I inspected the author target and code.
The new computational implementation was written afterward. It imports no
author code or coefficient data, and instead builds all six Euclidean F_ab
components and checks sparse polynomial matrices, but **code blindness is not
claimed**. The independent provenance is the pre-author raw/source derivation;
this exact run is a structurally different implementation of that pinned math.
All 21 common_response files were hashed before/after author inspection and
remain unchanged. No old/root/author files were edited. No Git calls, cache
writes, installs, external jobs, network retrieval or author messages occurred.

## Dependency graph

1. Degenerate light masses + nonanomalous vector flavor change of variables
   -> invariance of the full unconditioned functional under Q<->Q'.
2. The same change of variables applied to external nucleon conditioning
   -> proton at Q' maps to neutron at Q.
3. Covariant complete Born subtraction -> the same map for the NB tensor.
4. BKSM primary formulas + direct exact subtraction -> p-minus-n electric
   and magnetic O(q^4) chiral coefficients.
5. Gauge-invariant local polarizability action at fixed M_pi>0 + Wick rotation
   + complete SO(4) photon contraction -> C_soft=3(a-b)/(32*pi).
6. Steps 4+5 + fixed LECs + controlled differentiated chiral remainder
   -> sequential leading-log coefficient -3*kappa_s*g_A^2/(512*pi^4*F^2*m).
7. No step in this graph supplies the full all-momentum M_u, A_rho, R or alpha.

## Obligation matrix

| Obligation | Finding |
| --- | --- |
| Correct object and exact flavor action | Passed: external proton rotates to neutron; it is not held fixed by the change of variables. |
| Complete photon integration | Passed: equality of the background-field integrands survives identical full photon integration. |
| Matching and metric contacts | Passed: covariant schemes transform seagulls, Green functions, weights, counterterms and coincident contacts together; arbitrary noncovariant finite choices are outside the hypothesis. |
| Complete normalized external-state/Born map | Passed under the declared complete covariant Born subtraction, including regular elastic terms and matched form factors. |
| BKSM Eq. (6)-(10) source coefficients | Passed: direct PDF extraction and page inspection; source Eq. (10) separately checks the subtraction. |
| Primary source pole convention | Passed for real-Compton polarizabilities; it does not alone authenticate an arbitrary doubly-virtual convention at all momenta. |
| Wick rotation and complete soft combination | Passed: alpha-minus-beta, with both subtraction and dispersive contributions retained. |
| Soft-ball radial normalization | Passed: 3/(32*pi), independently from the action and four-ball measure. |
| kappa_s=0 and nonzero-g_A conditions | Passed: author states the exceptional scalar branch; electric tensor log survives for g_A!=0. |
| Limit order | Passed: K->0 at fixed M_pi>0, then chiral expansion; exchanging limits is not justified. |
| Literal M_pi->0 differentiated remainder | Conditional on the named controlled EFT remainder; finite algebra does not prove it. |
| Full A_rho, M_u, R, alpha and downstream calibration | Out of scope; not established by this bounded result. |

## Decisive mathematics

A flavor change of variables gives exactly

  W[g,u;Q']=W[g,u;Q],
  T_p^NB[Q']=T_n^NB[Q],
  T_n^NB[Q']=T_p^NB[Q].

Every metric derivative of the same complete vacuum functional inherits the
first equality. The p-minus-n NB tensor is odd, while the vacuum response is
even. Flavor-covariant Ward relations preserve this distinction and leave
transverse NB reduced matrix elements undetermined. They do not imply
T_p^NB[Q']=T_p^NB[Q].

This supports the author's intended obstruction to a map whose charge
dependence is exhausted by the unconditioned singlet vacuum response. A broader
logical assertion about every possible reconstruction formula must keep its
scope explicit: a formula that admits additional explicit charge/state flavor
structures or independent baryon reduced matrix elements is not excluded merely
because W(Q)=W(Q'). Those are additional data; covariance alone does not fix
them. No exact numerical relation at one chosen physical Q is refuted here.

Writing P=g_A^2/(96*pi^3*F^2*m) and L=log(M_pi/mu_chi), the source gives

  Delta a=P*(6L+4)+d_a+higher,
  Delta b=P*(6(1+kappa_s)L+3(1+kappa_s))+d_b+higher,
  Delta(a-b)=P*(-6*kappa_s L+1-3*kappa_s)+(d_a-d_b)+higher.

The common leading 1/M_pi term and common c_2,c^+ terms cancel. At fixed LECs,
the displayed analytic polarizability contacts cannot remove the log across
a chiral family. This is not a claim of a nonzero total at every positive mass.

Directly constructing E_ab and G_ab=k^2 delta_ab-k_a k_b from F_ab gives

  K_ab=4*pi*u*((a+b)*E_ab-b*G_ab),
  1/2 Tr(K D)=2*pi*u*((a+b)*(k^2+2k4^2)-3b*k^2)*D.

The SO(4) average is 3*pi*u*(a-b)*k^2*D. The relative minus sign follows from
L_E=2*pi*u*(a E_E^2-b B_E^2). The complete subtraction/dispersive coefficients
are -3b and (3/2)(a+b), respectively; both are essential. Integrating the
massless photon over |k|<K then yields

  M_u^NB(soft)=3*(a-b)*K^4/(32*pi)+o(K^4),
  partial_logMpi Delta C_soft
    -> -3*kappa_s*g_A^2/(512*pi^4*F^2*m).

At kappa_s=0 this particular scalar logarithm vanishes. It cannot be advertised
as universally nonzero. The tensor-level electric logarithm stays nonzero for
g_A!=0. A common quark-mass scalar insertion has the extra factor 1/2 from
M_pi^2=2B m_l at this order.

The clean notes also derive an orthogonal photon-mass check: for a soft SO(4)
ball cutoff Lambda and photon mass lambda,

 I_lambda-I_0=[-lambda^2 Lambda^2+
               lambda^4 log((Lambda^2+lambda^2)/lambda^2)]/(16*pi^2).

Multiplying by 3*pi*(alpha-beta) fixes the lambda^4 log(lambda^2) coefficient
as -3*(alpha-beta)/(16*pi). This regulator check agrees with the same
alpha-minus-beta combination; it is not an extra full-mass result.

## Primary source check

- arXiv:hep-ph/9309211v1, Bernard/Kaiser/Schmidt/Meissner, visible date
  1 Sep 1993, printed pp. 4-5, Eqs. (6)-(10). PDF SHA256:
  09af9bc7bfc8fc07b22e344a60aa922da0efe4d2fda0c5e23ffda2819e3c94f4.
- arXiv:hep-ph/9311354v1, Bernard/Kaiser/Meissner/Schmidt, visible date
  24 Nov 1993, printed pp. 5-6, Eqs. (5)-(9) and pole-exclusion paragraph
  at the beginning of printed p. 6. PDF SHA256:
  d86056f9b18b305ac7b36b69497fc77df3ca9745ac7624cc967a23f1f2f5dcbe.

Authentication is by the supplied PDFs' primary-source banners, formula
locators and fixed hashes, not by a fresh external-server checksum. The source
pole statement verifies the real-Compton convention. The off-shell soft bridge
uses the declared complete covariant Born subtraction and the local
spin-averaged O(k^2) F^2/vFvF effective action. This does not establish the full
virtual tensor or its hard subtraction function. The older WLCM/other source
lane was not opened for this narrow review.

## Bounded execution and reproducibility

Independent implementation: check_clean.py. Pre-execution contract:
COMPUTATION_CONTRACT.json. Provenance wrapper: execute_clean.py. The command
`python3 fine_structure_puzzle/qcd_nonborn_vacuum/reviews/common_clean/execute_clean.py`
ran once, with run_clean_001/manifest.json status `completed`, exit 0, in
0.046440708 seconds. Python 3.9.6; exact fractions and sparse polynomials only.
Hard wall bound 20 seconds, per-process CPU bound 10 seconds, thread convention
1; no RLIMIT_AS, affinity request or external dependencies. The program emits a
fixed bounded summary; no hard output-byte monitor was added.

Checks cover the full declared four-dimensional degree-two kernel as exact
polynomials, twelve transversality equations, sixteen Maxwell-kernel component
identities, the degree-one kappa_s source coefficients, exact SO(4) quadratic
moments, radial polynomial division and 49 finite rational-charge diagnostics.
The finite charge enumeration is not the proof of the analytic flavor theorem.
All seven declared inputs have observed unchanged before/after hashes.

The manifest passed the installed computation-audit validate_manifest.py with
`--root /Users/carlzimmerman/new_physics/zimmerman-formula`; its saved output is
run_clean_001/validation.txt. This is a valid completed v2 evidence record, with
an explicit provenance limit: no Git query was permitted. The repository commit
is marked unavailable and dirty=true is a conservative schema marker, explicitly
not an observed Git-cleanliness measurement. Scientific inputs and targets are
identified by content hashes instead. A valid manifest does not prove its
mathematical interpretation.

## Remaining gap and strongest safe statement

The source coefficient, full soft normalization and exact flavor map need no
further finite checks. Promotion to the displayed literal chiral-limit formula
needs a differentiated remainder tending to zero; this is the named conditional
input. Establishing a nonzero full p-minus-n mass response requires a complete
matched all-momentum calculation and is not supplied. Establishing A_rho or a
ratio/root requires additional independent physics as the author already says.
No expansion at fixed K while M_pi->0 is licensed.

The strongest safe conclusion is that the singlet unconditioned vacuum Ward
relations do not by themselves force same-proton NB equality: the allowed
isovector electric EFT coefficient is nonzero for nonzero g_A. The full SO(4)
soft projection has the additional kappa_s cancellation exactly as stated.
This review does not re-audit history, full amplitudes, the all-momentum NB
band, Eq. (12)'s inherited calibration inputs or the full physical target.
