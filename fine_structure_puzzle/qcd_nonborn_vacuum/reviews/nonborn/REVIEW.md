# Independent non-Born and charge-exchange audit

Normalized claim: at fixed positive pion mass and in the stated on-shell
Born convention, the leading SO(4) soft-photon functional is determined by
the full polarizability difference; AHLP supplies one covariant pi-N-loop
static sector, NP supplies the complete strict leading HB pi-N functions
for the declared finite bands, and flavor exchange distinguishes the
unconditioned vacuum from the one-baryon response.

**Primary verdict: conditional on a named input.** The analytic soft
reduction requires the gapped pure-QCD low-energy tensor, and the source
sector results require the stated SU(2) chiral effective description with
a nonzero Delta–nucleon gap. Under those hypotheses the reviewed algebra
and source translations pass. The separate numerical outcome is
**implementation and finite assertion verified in the stated range**.
There is no full physical-proton mass or curved-QCD result.

## Decisive result and normalization

Let a=alpha_E/u, b=beta_M/u, u=e², and let K=M_u/M. Both independent Born
amplitudes give t_i=2M T_i(AHLP)/u=S_i(NP), including the non-pole Dirac
term. Starting from the rest-frame polarizability action and then using
the complete two-amplitude contraction gives

    M_u^NB(0<Q<Lambda)=3 Lambda4(a-b)/(32 pi)+O(Lambda6),
    K_NB(0<Q<Lambda)=3 Lambda4(a-b)/(32 pi M)+O(Lambda6).

Thus the two possible soft-coefficient conventions differ by M. The
author's reported C_NB is the second one, with dimension GeV^-4. The
subtraction term alone is -3 b Lambda4/(16 pi M); it cannot replace the
full result. The electric and magnetic Euclidean photon contractions
have equal SO(4) means 3/2 and opposite signs in the mass insertion.

The leading pi-N chiral difference is

    a-b=3g_A²/(256 pi² F_pi² m_pi)+less singular terms.

The soft limit precedes the chiral limit. A fixed nonzero photon band
cannot be kept within a threshold expansion as m_pi tends to zero.

## Dependency graph and obligations

- Effective polarizability action + on-shell Born convention + state
  normalization -> transverse T1/T2 low-energy tensor -> full angular
  contraction -> soft coefficient. These algebraic steps pass.
- Authenticated AHLP archive -> two exact ancillary assignments -> inert
  source extraction -> principal-branch real formulas -> static sector.
  These source/parser/branch checks pass; full-QCD interpretation is
  restricted to the declared pi-N sector.
- Authenticated NP archive -> complete leading HB S1/S2 including the
  seagull -> independent nonsingular trace -> full finite-band convolution.
  The source translation and finite computation pass within the stated
  numerical tolerances.
- Flavor-covariant path and regulator + m_u=m_d -> exact vacuum exchange
  null, while proton maps to neutron. This change-of-variables argument
  passes under those explicit hypotheses.
- Authenticated BKSM coefficients -> p-n logarithms -> complete SO(4)
  contraction -> the kappa_s-dependent scalar log. The exact coefficient
  subtraction passes; the asymptotic interpretation remains conditional
  on the standard chiral remainder.

| Obligation | Status | Evidence or limit |
|---|---|---|
| Both Born tensors and charge/state factors | passed | AHLP Eq.(6), NP (2.11), inherited WLCM basis |
| Full soft electric/magnetic contraction | passed | PRETARGET action/basis derivations and exact symbolic check |
| Ancillary assignment identity | passed | Independently downloaded archive member equals worker notebook bytes |
| No notebook constants or saved outputs evaluated | passed | Both parser implementations select only two unique RHSs |
| Static covariant loop real branches | passed in checked range, analytic branch reduction verified | Nine mu values from 0.0001 through 1.99, including both sides of sqrt(2); source principal ArcTanh reduction |
| Static chiral series through mu² | passed | Separate exact symbolic run |
| NP source seagull retained | passed | Source (4.26)–(4.27), S1 constant 3/2 and vanishing zero-momentum amplitude |
| Apparent angular endpoint singularities | passed for derived trace | Algebraic rationalization plus endpoint continuity checks at r=.1,.25,.5 |
| Full HB pi-N finite bands | computationally verified in stated range | Independent parameter-integral/Chebyshev implementation, all four bands |
| Vacuum exchange null versus baryon p↔n | passed under explicit assumptions | Exact flavor relabeling with matching/contact covariance |
| Scalar nonsinglet log | passed at stated chiral order | kappa_s-independent log cancels; exceptional kappa_s=0 branch retained |
| Phenomenological polarizability contacts/Delta fits | excluded | No delta-beta fit, Baldin fit, resonance estimates or numerical kappa_s used |
| Physical matched u=0 strong inputs | not supplied | Numerical values are source-parameter benchmarks |
| Full QCD non-Born tensor/mass, A_rho, R or alpha | out of scope/open | Missing all-momentum data, sea coverage, matching and global curved functional |

## Independent finite computation

The new implementation is not an invocation of either author script. It
reads the separately downloaded AHLP archive, parses inert box calls using
Python AST, and parses only a whitelisted arithmetic RHS. The worker uses
a different recursive box parser and SymPy's Mathematica parser. Principal
branches were checked beyond the author's seven-point interval, through
mu=1.99; the real source formulas and the displayed log cancellation agree.
An exact second run establishes

    F_S-2F_B=3pi/256-5mu/64+147pi mu²/2048+O(mu³ log mu).

For the finite convolution, the review first derived and saved
INDEPENDENT_FINITE_DERIVATION.md. It combines the source amplitudes into a
single nonsingular trace, rationalizes the Feynman-parameter integral,
integrates directly in t=Q²/m_pi², and uses Gauss–Chebyshev weights for the
angular measure. The worker uses separate potentially singular S1/S2,
arctangents and an angular theta transformation. Exact algebra in the
second review run proves the rationalization modulo H²=1+t*x², and
recovers both scalar soft limits and the 9pi L4/64 integrated limit.

At 50 digits, Legendre orders 16,32,48 and angular orders 32,64,96 give:

| Photon band in Q/m_pi | Independent dimensionless J_band |
|---|---:|
| 0 to .1 | 0.0000441500706722953429137836075068098169041 |
| 0 to .25 | 0.001718825018972117650563407171768137884656 |
| 0 to .5 | 0.02718536976811713689759560742269443027737 |
| .25 to .5 | 0.02546654474914501924703220025092629239271 |

All four agree with the frozen worker values to absolute error below
5e-47. This is numerical convergence evidence, not a rigorous interval
bound or a physical EFT uncertainty. With the source's printed strong
parameters, K_HBpiN(0,.5)=1.1984656389312044e-6 and
K_HBpiN(.25,.5)=1.1226913256831551e-6. They are charge derivatives divided
by M, not physical electromagnetic mass shifts at a supplied alpha.

The independently parsed static covariant pi-N formula gives
C_NB=0.0395567179429793893730774704095 GeV^-4 for the same printed
parameters. This is a distinct covariant static calculation; multiplying
its coefficient by the HB finite-band shape would not produce a computed
covariant finite-momentum result.

## Charge exchange and the cancellation that matters

BKSM hep-ph/9309211v1 (7)–(10), independently cross-checked against
hep-ph/9311354v1 (15)–(16), gives, in units g_A²/(96pi³F²M),

    Delta a=6L+4+contacts,
    Delta b=6(1+kappa_s)L+3(1+kappa_s)+contacts.

The SO(4) difference is therefore 1-3kappa_s-6kappa_s L, with log derivative
-3kappa_s g_A²/(512pi4 F²M) after multiplication by 3/(32pi).
In particular the electric-only logarithm cannot be quoted as a full soft
mass logarithm: its kappa_s-independent part cancels against the magnetic
term. At kappa_s=0 the contracted log vanishes even though the electric
tensor log remains nonzero. The common-response derivation states this
exception and does not infer nonzero full all-momentum M_u from the soft
functional alone.

The exact vacuum null involves the unconditioned flavor-singlet measure;
flavor exchange maps a proton matrix element to a neutron matrix element.
Metric and scalar insertions preserve this representation distinction.
This excludes reconstruction of the full proton non-Born tensor solely
from flavor-covariant vacuum Ward identities. It does not exclude an
additional dynamical relation at one physical charge choice, or an
accidental cancellation in a complete scalar mass integral.

## Provenance, limitations and remaining leaf

PRETARGET.md was saved before nonborn_proton/DERIVATION.md, its implementation,
inputs or results were opened. A broad search had exposed the common-response
factor; that limitation and the finite-band numerical-answer exposure are
recorded explicitly. Consequently this is an independent source-first
static non-Born review and an independent implementation of the finite-band
integral, but not a blinded common-response factor review.

The independently fetched arXiv source archives and BKSM PDFs exactly match
the worker's stored bytes; SOURCE_AUTHENTICATION.json contains URLs/hashes.
The original author static, finite and common-response manifests all validate
as completed with current input/output hashes. No author files were changed.
REVIEWED_PINS_BEFORE.json and REVIEWED_PINS_AFTER.json pin the audited files.
The review's two v2 manifests are run_001/manifest.json and
symbolic_run_001/manifest.json. Both completed and validated. No RLIMIT_AS was
requested on macOS. Exploratory failed methods and the pretarget equation-
numbering correction are preserved in FAILURES_AND_CORRECTIONS.md.

The printed AHLP m_pi=.13957 GeV is a physical charged-pion calibration,
not an independently matched pure-QCD pion mass at u=0 on the declared MSbar
path. M,F_pi,g_A are likewise imported calibrations. Their use defines
deterministic source-formula evaluations; it does not determine a physical
u=0 proton derivative with the displayed digits. The symbolic mass dependence
and specified EFT functional remain valid. No numerical alpha is entered.

The smallest missing physical implication is still the full renormalized
Born-subtracted proton tensor on one common matched path, with all sea
classes and finite UV matching, together with an unconditioned curved-QCD
functional controlling A_rho and its charge response. The reviewed pi-N
sector neither provides nor eliminates those inputs. No R or alpha follows.

The cheapest next physical check is a complete low-momentum determination
of (alpha_E-beta_M)/u in a declared pure-QCD calibration, including its
contacts and quark contraction coverage; the finite HB functions provide
a long-distance benchmark for that check. They are not a replacement for
the all-momentum and curved-vacuum obligations.
