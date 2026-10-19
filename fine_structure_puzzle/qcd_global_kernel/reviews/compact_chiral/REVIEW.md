# Independent review of the matched compact-chiral continuation

Primary verdict: **conditional on named inputs**. The new exact/Gaussian replacement formulas, first nonconstant-pion source contraction, aligned Gaussian subtraction, covariance/cumulant derivatives, and explicitly defined zeta finite part are correct in their stated mathematical/common-regulator scope. A physical NLO sphere response remains conditional on a common subtraction/matching prescription, independent curvature LECs, and omitted photon contributions. The literal mapping to the printed k15 beta function is unresolved here.

## Independence, scope, and ancestry

`PRETARGET_DERIVATION.md` was saved before reading any `chiral_zero_mode/` file. After the coordinator identified the FSP003 ancestor, I read the named old route and saved `DELTA_PRETARGET_DERIVATION.md` before opening the frozen new targets. I did not read an author REPORT or take another agent's verdict as evidence. The completed `reviews/global_sphere/` files were never edited; `PRIOR_REVIEW_HASHES.json` records their bytes for the final preservation check.

The base Haar/Dashen integral, its axes, first charge response, canonical measure cancellation, and replacement proposal are **known after notation translation within this project**. They already occur in FSP003 `qcd_prediction/controlled_model/qcd_zero_modes/REPORT.md`, sections 4,6,7,9, and `qcd_prediction/coordinator/ZERO_MODE_QED_RAW.md`. Here x is the ancestor's 2mu and y is its t at theta=0. The new target correctly acknowledges this overlap. No inherited base-integral grid was repeated as new review evidence.

The audited revisions are the five files in `TARGET_HASHES_BEFORE.json`: `DERIVATION.md`, `compute_matched.py`, `INPUTS.json`, `SOURCES.json`, and `contract.json`, plus the subsequently completed `run_001/manifest.json` and `RESULTS.json`. The audit concerns theta=0, topology-summed SU(2), fixed renormalized a=F²M²,b=uC,F,C,mu, and only the selected pion contraction. The source flavor integral does not authenticate an absolute S4 QCD normalization.

## Dependency and obligation checks

| Obligation | Verdict | Reason |
|---|---|---|
| Ancestry/novelty calibration | passed | Target explicitly credits the existing Haar integral, axes and Gaussian proposal |
| Q trace, local volume term and Haar normalization | passed as inherited setup | `Tr QUQUdag=5/9-s`; removed W shift is `-5y/9`; no physical vacuum matching inferred |
| Exact-over-Gaussian replacement | passed | Same-normalization `ZG=sqrt(2/pi)e^x/[sqrt(x)(x+2y)]`; canonical Jacobian gives the already-counted three scalar constant modes |
| Fixed-parameter replacement stress and charge response | passed | Target (7),(8) follow from `D=x∂x+y∂y`; both covariance terms are retained |
| First replacement saddle coefficient | passed | Haar Jacobian and quartic mass potential yield target (10), including negative finite-charge differential response for b>3a/2 |
| First nonconstant-pion contraction | passed in selected order | Direct quaternion expansion gives `(1-3g/2)a0` and `(1-4g)s+2g` |
| Source-dependent constant factor | passed | `exp(-2yg)` is retained and cannot be dropped as a source-independent normalization |
| Matching to an existing massive determinant | passed as common-regulator identity | Target subtracts `g(3x/2+2y)` already present in the nonconstant Gaussian determinant |
| Kinetic/collective Jacobian normalization | passed for these ratios/order | U0/source independent at the retained massless nonconstant order; source-dependent corrections and absolute normalization remain outside this cancellation |
| B, DB, By, DBy including third cumulants | passed | Independent chain-rule reconstruction agrees with target (18)-(20) |
| S4 tadpole residue and chosen finite part | passed in the declared zeta scheme | Prime heat trace fixes residue 1/3; independent heat-Mellin check confirms the stated finite part |
| Fixed-mu g derivative | passed | `Dg=-g/2+H²/(16pi²F²)` for the explicit zeta prescription; g is not held constant |
| Complete k15 RG/basis identification | conditional/unresolved | Literal collective-background pole and printed form-factor beta differ by two under the naive same-operator identification; no unproved bridge accepted |
| Full NLO pion+photon partition and common finite matching | not addressed, correctly excluded | Photon seagull/mixing and independent same-order curvature source terms are load-bearing |
| Epsilon regime and order of limits | passed | Fixed physical mass/charge H→0 is distinguished from x,y fixed epsilon scaling |
| Full QCD, alpha selection and H-linear coefficient | out of scope | None is certified |

## Decisive algebra

With `m=<a0>`, `q=<s>`, the extra source correction beyond the already massive Gaussian baseline is

`delta W_extra=g B`, `B=(3x/2)(m-1)-4yq`.

This follows from `delta W_massless=g[2y+(3x/2)m-4yq]` after subtracting the aligned term `g(3x/2+2y)`. Its same-radius charge difference is `g[(3x/2)(m(x,y)-m(x,0))-4yq]`. The target performs this subtraction and explicitly defers translating it to the mass-dependent decoupling determinant's finite scheme. That qualification is necessary.

Differentiating the distribution gives `m_x=Var(a0)`, `m_y=-Cov(a0,s)`, `q_x=Cov(a0,s)`, `q_y=-Var(s)`. These identities reconstruct every sign and coefficient in target (18),(19); the coefficients 11/2 arise from combining both mass and electromagnetic covariance terms. Since `∂y DB=By+DBy`, the target's charge derivative `(gdot+g)By+gDBy` is correct when the leading massless tadpole is charge independent.

For the saddle, Gaussian variances are `1/x` in the neutral tangent direction and `1/(x+2y)` in each charged direction. The density term `<r²>/2` and mass term `-x<r⁴>/8` give

`Qrep-1=1/[8x]+1/[2(x+2y)]-x/(x+2y)²+...`.

This reproduces the target's k(a,b), its charge difference and derivative. The sign change in the derivative is a property of this mathematical replacement; it supplies no charge-selected vacuum.

## Tadpole finite part and renormalization restriction

I independently reconstructed the target's Hurwitz finite-part calculation. Only k=0 and k=1 have poles at p=1. Their sum has residue 1/3. The regular tail reduces to `[2psi(5/2)-psi(4)-psi(1)]/3`; its psi(5/2) dependence cancels the pole terms, leaving

`FP zeta_D(1)=2gamma/3-8/9`.

An orthogonal Mellin formula is

`FP zeta_D(1)=∫_0^1 [Kprime(t)-1/(6t²)-1/(3t)]dt +∫_1^infinity Kprime(t)dt -1/6+gamma/3`.

Here `Kprime=K0-1`; the `gamma/3` comes from `1/Gamma(1+epsilon)`. This independently checks the finite part's subtraction convention. It is a conventionally defined number, not a universal physical curvature LEC.

The diagonal heat coefficient R/6 yields `Gbar_div=R/(96pi²epsilon)` for d=4−2epsilon. Strong R·mass matching cross-checks the normalization against the primary beta13=1/8. The naive literal k15 comparison remains unresolved, as documented in `ANCESTRY_AND_RG_OBLIGATION.md`; I do not promote that difference into a proved source error or a completed RG result. The target cites Kubis–Meissner for operator content only, not a demonstrated numerical beta cancellation, which is the correct restriction.

## Computation audit and fresh checks

The author code was read statically and never imported or executed by this reviewer. It implements the stated finite domain, covariance positivity checks, bounded Gauss–Legendre construction, direct finite differences, two precisions, an independent tanh-sinh point, and a finite Hurwitz-series tail bound. The bound is valid on its small positive Laurent offsets: `(p)_k/k!<=k+1` for 1<p<=2, and a Hurwitz integral bound supplies the displayed geometric tail. The 4-point Laurent extrapolation is numerical corroboration of the separately derived closed form, not an interval proof.

The observed author run is completed, exit zero, and its v2 manifest validates with `--root`. It reports 143 finite controls at 40/60 decimals, maximum repeated-precision discrepancy `1.818e-36`, and a declared six-point matched grid plus three saddle tests. These finite controls are not a proof of full NLO physics.

Two fresh reviewer runs write only under this review directory:

* `run_001`: exact polynomial contraction; one shifted-source derivative at x=1.7,y=0.4 agrees within `1.635e-15`; one matched fixed-mu radius derivative agrees within `1.527e-15`. It also records the unresolved beta translation explicitly.
* `run_002`: an original spectral heat trace and heat-Mellin subtraction check the new zeta finite part, independently of the target's Hurwitz Laurent implementation. The finite result and discrepancy are in its results file. The short early-time heat segment is asymptotic, so the check is conditional on numerical tolerances rather than interval certified.

Both fresh v2 manifests validate against current input bytes. Exact argv, software versions, limits, output hashes and run statuses are retained in their manifests. The failed-run history of the earlier global-sphere task remains untouched.

## Sources and exact remaining gap

`SOURCE_RECORDS.json` pins authenticated Urech, Lenaghan–Wilke and Kubis–Meissner primary versions, plus the nearest ancestor hashes. I additionally inspected the author's primary Damgaard–Fukaya arXiv:0812.2797v2, banner 2009-09-18, SHA256 `dbe44bb8ec58fb7e07850c37078604bcf0a964ffe45d8d4cfcec81135d12d96c`: (2.1)-(2.5) explicitly separates exact zero modes, zero-average fluctuations and a massive Gaussian baseline. Its flat-volume construction supports the decomposition, not an absolute curved-QCD stress. The Mehen–Tiburzi v2 PDF hash matches the receipt; it is an adjacent Haar/epsilon benchmark, not a load-bearing EM or S4 theorem.

The smallest missing physical implication is a common renormalized assembly of this pion correction with the chosen scalar determinant, full photon/mixing terms and the same-order curved source counterterms. Their finite LECs and the complete QCD normalization remain unknown. None is supplied by setting a zeta finite part or by cancelling a common source-independent measure factor. The strongest safe statement is therefore a verified new **partial nonconstant-pion source contribution and matched mathematical replacement**, with the stated physical matching conditional. No full-QCD or alpha result follows.

Self-proofreading covered only these new review additions. No frozen author file or prior review file was corrected.
