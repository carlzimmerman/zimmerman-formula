# Independent hard proton and bridge review

**Primary verdict: correct only after a stated restriction.** The finite quark
matching, literal lattice-node transformation and all-scale reconstruction
identity pass this review in their declared sectors. The bridge theorem uses
its explicit derivative endpoint assumptions; a bound on the function alone
does not imply those assumptions. The physical full-QCD endpoint and response
remain conditional on missing matching and matrix-element inputs.

The exact author revisions reviewed are all 34 file hashes in
AUTHOR_PINS.json. No author or ancestor scientific file was edited. PRETARGET.md
was written and hashed before either new author derivation, report, code or
result was read. The required three ancestor derivations were read first.
This is an independent fresh subagent derivation relative to the new packets,
with inherited ancestor exposure explicitly disclosed, not blind independence
from the established Dirac benchmark. Posttarget source/code exposure is
necessary for, and does not invalidate, the subsequent comparison.

## Claim and dependencies

The reviewed arrows are:

1. Sharp O(4) one-loop quark matching -> a local mass-parameter conversion
   -> the proton Feynman--Hellmann scalar insertion, at strong order zero.
2. Literal finite-a light-current form-factor nodes -> a defined, clipped
   nodal Born functional and its linearized marginal-error ceiling.
3. All positive-photon-mass derivatives + a matched large-mass endpoint ->
   the massless-photon response. An elementary Dirac field supplies a complete
   control theory, not the physical proton endpoint.

Leaves are respectively the inherited full-current normalization, independently
rederived Dirac loop and evanescent contact; authenticated primary source
numbers with disclosed calibration; and explicit lower/upper endpoint and
integrability hypotheses. The missing QCD gluon matching, common scalar data,
all-current tensor and curved-vacuum expectation are unchecked physical leaves,
not consequences of the control calculation.

## Decisive checks

| Obligation | Verdict | Evidence and limit |
|---|---|---|
| Sharp cutoff finite constant and sign | Passed | Sharp loop finite 3/2, MSbar finite 4, added conversion +5/2. The evanescent numerator integrates to -1; dropping it gives 5 rather than 4. |
| Proton insertion | Passed at leading strong order | `sum Q_f² sigma_f [3log(mu²/Lambda²)+5/2]/(16pi²)` per e². Sigma is `m_f partial M/partial m_f`; no additional quark-mass or 4pi factor. |
| Finite gluon endpoint | Conditional, not calculated | The e² g_s² coefficient multiplies a canonical gluon matrix element of order 1/alpha_s. It cannot be discarded or assigned the quark 5/2 constant. The authors explicitly retain this gap. |
| Source extraction | Passed | Independent fresh versioned PDF/source acquisition agrees with author hashes. All 280 selected form-factor cells in 35 rows match the exact TeX. Tables XVI-XVIII have 21 printed rows each; the literal nodes and the contradictory 50-bin prose are distinguished. |
| Current and continuum scope | Passed | Equations (5)-(6) insert the u,d electromagnetic current. Strange/charm sea dynamics does not insert their electromagnetic currents. Three finite-a tables are not source-fitted continuum functions in Table XX. |
| Nodal quadrature/normalization | Passed in finite assertion | Independent integration of the full T1/T2 angular tensor, rather than importing the author's closed Born kernel, reproduces all three reported K values and disconnected differences. Exact rational clipped weights integrate constant and linear fixtures. |
| Marginal-error ceilings | Passed as linearized bounds | For covariance C with given diagonal, `sqrt(v^T C v)<=sum |v_i| sigma_i`. Independent angular coefficients reproduce the reported L1 ceilings. This says nothing about nonlinear bias, interpolation, calibration, continuum or omitted-current errors. |
| Sigma calibration | Conditional source application | 2412.01535v1 Tables VI/VIII and its MSbar(2 GeV) conversion support the quoted sigma/gS inputs. Combining them with 2104.13408v3 m_l requires the declared common pure-QCD path identification. |
| Finite-L theorem and log/harmonic constants | Passed with explicit endpoint limits | n integrations by parts yield the finite boundary polynomial. For `f=-a log(s/S0)+B+o(1)`, the constant is `B+a H_(n-1)`; neither B nor the harmonic term can be dropped. |
| Dirac all-momentum benchmark | Passed within numerical tolerance | Independent n=2,4 checks at fresh s,L values compare radial and parameter derivatives and reconstruct f(0). The heavy-photon endpoint has a=3/(16pi²), B=5/(32pi²) at M=mu=S0=1. |
| Full QCD single-log application | Conditional | QCD running and mixing require an RG-improved endpoint/reference. Neither package transplants the elementary single-log result as the full proton endpoint. |
| Full QCD ratio/alpha selection | Not addressed | No full proton response, unconditioned curved coefficient A, R=A/M³ or selection equation is evaluated. |

The common-mass nodal values independently reproduced are
`-0.0003343715367844876`, `-0.0004164176384594101`, and
`-0.0004332606994426978` for B,C,D. They are functionals of source-fitted,
finite-a light-current nodes. No new fit is performed; this is not a fit-free
QCD prediction. Negative complete-Born values are allowed. The three positive
disconnected elastic differences are much smaller than their respective
linearized marginal-error ceilings, so they do not establish a physical sign.

The sigma-weighted input is 52.0711466667 MeV and its finite leading quark
conversion is 0.8243609709 MeV per e². These are source calibrations with
substantial charm input, not a controlled full hard-QCD mass. The formal hard
tail requires Q0 above every retained active mass and the QCD scales; no
numerical Q0 or bound on the omitted strong/mass-power terms is established.
At mu=Q0 the quark logarithm vanishes while its finite term remains.

The 2026 variational source 2610.20362v1 is authenticated by its actual versioned
PDF title page and public HTML. Its B64 mass 944.0(4.4) MeV and scale 0.07948(11)
fm support the disclosed mass sensitivity. Its retuned finite-a sigma results
45.7(3.0)(3.3), 42.1(6.5)(2.3), and 107.4(30.4)(0.6) MeV are not continuum
replacements for the 2024 calibration. Changing the scalar source between
these numbers without accounting for extraction, tuning and continuum
differences would be invalid; the author package does not do so.

## Precise restriction in the bridge prose

DERIVATION.md section 1 states that `f(s)-f(0)=O(s^1/2)` ensures the lower
integration-by-parts endpoint vanishes. That implication needs derivative
control: `f(s)=sqrt(s) sin(1/s)`, extended by f(0)=0, obeys the displayed
function bound but `s f'(s)` contains `-cos(1/s)/sqrt(s)`. The immediately
following explicit conditions `s^k f^(k)(s)->0` supply the correct theorem
hypotheses. The Dirac control satisfies them. Read the theorem with those
conditions, or replace the earlier sentence by a derivative-controlled soft
expansion. This is a localized mathematical wording defect, not a failure of
the finite identity or of the executed benchmark.

## Computation and provenance

The independently written independent_check.py imports no author implementation.
Its contract, source-extracted numeric subset and code were frozen before its
actual installed mathbox v2 runner execution. run_001 completed in 4.229535 s
with 55 checks at 32 and 48 decimal digits. Full angular integrations reproduce
the double-precision author outputs within 3e-17; internal endpoint/derivative
checks use 1e-24 absolute tolerance. The largest recorded discrepancy, 5.58e-17,
is the independently evaluated quark conversion versus the author's serialized
double and is below its 3e-15 tolerance. This is numerical precision evidence,
not interval-certified analysis. No RLIMIT_AS was requested on macOS.

Both current author v2 manifests and the independent v2 manifest validate with
`--root`, completed status and unchanged declared inputs. VALIDATED_CHECKS.json
records pin comparisons and exact validation outputs. A successful manifest
alone does not verify the physical interpretation.

## Posttarget coordinator companion

COMMON_UV_RATIO.md was read only after PRETARGET and is reviewed separately.
For an RG-invariant O of dimension d with no extra scale, dimensional analysis
and `gamma_f=-dlog m_f/dlogmu` give
`beta_s partial_g O=-d O+sum(1+gamma_f)m_f partial_mf O`.
Applying the quotient rule to A/M³ gives `beta_s partial_g R=D_m R`.
Common hard matching then gives its equation (2) by the chain rule, at a
reference coupling where beta_s is nonzero, or after a separately justified
finite limiting ratio c_g/beta_s. Signs and dimensions agree.

The scale-only gluon contribution cancels in a strictly massless family only
under the stated existence, regularity, absence-of-extra-scales and uniform
decoupling assumptions. In particular finite mass derivatives of A remain
unknown; proton sigma terms do not supply them. This is an inherited scale
projection applied conditionally to matching, not a new QCD number or a
zero-endpoint result for physical nonzero quark masses.

## Strongest safe statement and next obligation

The sharp-photon quark finite conversion is specified at leading strong order,
and all-mass derivative reconstruction is a valid conditional route when its
matched endpoint and all intermediate masses are supplied. The lattice data
exercise produces exactly the declared finite node functional. The cheapest
new physical calculation on this route is the finite gluon/strong-parameter
matching in the same prescription with scalar mixing/evanescent terms retained;
it must be paired with the missing full current and unconditioned vacuum data.
Neither a benchmark nor a source-calibrated partial elastic band solves the
requested full-QCD ratio or alpha problem.
