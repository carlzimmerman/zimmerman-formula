# Independent topology/contact review

Normalized claim: the specified finite-regulator QCD generating functional
gives exact topology/metric/current derivative identities and, under a
controlled differentiated fixed-Q saddle on round S4, a sector-conditioned
test for the theta-dependent part of an H-linear stress coefficient.

**Primary verdict: conditional on a named input.** The exact finite-regulator
identities and information obstruction are proved as written. The physical
small-H diagnostic is conditional on the stated common-regulator/renormalized
limit and uniform differentiated sphere saddle, together with differentiated
small-H susceptibility asymptotics. No value of the full physical A_rho is
established. One source-locator correction is required, documented separately;
the underlying source implication remains valid.

## Provenance and revision

This delegated reviewer first derived and saved
[INDEPENDENT_DERIVATION.md](INDEPENDENT_DERIVATION.md), SHA256
`64b193da19c95b031ccdd56dbcb722cf21a6bf16a1d79cca84494a9c612ec031`,
before opening any target file. The task input supplied only Z, t, V, Q,
CP and the candidate saddle formula. The audit uses the proof-audit workflow
and the exact-source implication discipline of literature-check. All writes
are confined to this topology review directory; no author target, navigation,
previous evidence or Git state was modified.

The exact reviewed targets are:

| Artifact | SHA256 |
|---|---|
| vacuum_response/DERIVATION.md | `592a7fb94b58f7fac6541447e3d1bc83dff598c535155f698acb4e97ff45132a` |
| vacuum_response/REPORT.md | `c5066b8a86a4c0b6e0cae3c60c32a719e426479b8221e8c72537bdb2b7c04f49` |
| vacuum_response/checks.py | `7014b0aac7e993ecd7f36681f7d4f111cf9576cfffb02e8c14777d399e25352c` |
| vacuum_response/SOURCES.json | `626d5c9fb8639f3217c51e6cc48fcebc3c871dd5d7789075c64760d16e7cffec` |

The machine-readable source/file hashes and reexecution receipt are in
[RECEIPT.json](RECEIPT.json). Existing source-acquisition authentication was
reused; hashes, version banners and relevant source passages were inspected
independently, without claiming an independent refetch or an all-page review.

## Claim card and dependencies

Objects are regulated normalized expectations with
`Z=integral exp[-S(t,u)+i theta Q]`, `W=-log Z`,
`t=log a`, `V=Omega a^4`, `T=S_t`, `I=S_u`,
`rho=W_t/(4V)`, `chi=W_theta_theta/V`. The integer integrated Q is
t/u independent; the measure is fixed or absorbed in S; the variations
preserve CP at theta=0; mixed derivatives exist and commute. The continuum
interpretation additionally requires the specified renormalized parameter
path, counterterms and stress matching. No independently adjustable
theta-source-only normalization is silently added.

The dependency chain is:

1. Regulated source conventions and normalized differentiation imply exact
   topology/stress identities, including the mixed action contact.
2. `P_Q=Z_Q/Z(0)` implies the exact constrained-sector stress difference.
3. An analytic isolated theta saddle with positive chi, fixed integer Q,
   controlled higher cumulants, and suitable global saddle dominance gives
   the displayed fixed-Q expansion. Applying it on S4 is an additional
   conditional bridge, not a source measurement on S4.
4. Uniform differentiation of that expansion and the small-H susceptibility
   gives X_top and the theta-curvature of A_rho.
5. Theta-independent common factors cancel in normalized topology data,
   proving that this test cannot determine the full A_rho(theta=0).

No dependency closes through an evaluated QCD mixed matrix element: that
physical leaf remains open rather than circularly supplied by a toy check.

## Obligation matrix

| Obligation | Status | Decisive reason |
|---|---|---|
| Finite-regulator signs and volume derivative | Passed | Independent differentiation gives `rho_theta_theta=chi+chi_t/4=(1-D/4)chi`. |
| Mixed current/metric contact | Passed | `rho_theta_theta_u=[kappa(Q^2,I,T)-Cov(Q^2,I_t)]/(4V)`. The contact is present with the correct minus sign. |
| Three-variable versus four-insertion cumulant | Passed | With CP-even I,T, `kappa(Q^2,I,T)=kappa(Q,Q,I,T)`; one-Q mixed moments vanish. |
| Actual EM stress versus theta-differentiated stress | Passed | Target equation (5) correctly has `[<I_t>-Cov(I,T)]/(4V)` without Q probes. |
| Exact sector identity | Passed | `W_Q=W-log P_Q` gives target equation (6) at fixed Q and Omega. |
| AFHO fixed-Q saddle and c4 sign | Passed | Exact v2 equation (16), with its analytic-theta assumptions, translates to target equation (7). |
| Differentiating the saddle uniformly along S4 | Conditional | No such QCD uniformity proof or measurement is supplied; the target explicitly requires it. |
| H4 constraint correction, H5 signal and amplification sign | Passed under named conditional input | Independent derivation below reproduces equations (8)–(11). |
| Recovering a full A_rho from topology | Not addressed, explicitly excluded | A theta-independent common metric factor cancels in all these normalized data. |
| Treating that factor as an arbitrary physical counterterm | Passed scope restriction | Target expressly does not grant this freedom in fixed microscopic QCD. |
| Source locator accuracy | Failed locally | Makino–Suzuki master formula is `(4.70)`, not `(4.73)`; see correction note. |
| Exact bounded algebra run | Passed within stated range | All 37 checks reproduced, exactly matching the recorded result. |
| Physical-QCD coefficient or all-gap no-go theorem | Out of scope | Neither follows from this audit or the finite fixture. |

## Decisive algebra and exact remaining asymptotic obligation

Normalized differentiation gives

`W_ttheta_theta=-Cov(Q^2,T)` and
`W_ttheta_thetau=kappa(Q^2,I,T)-Cov(Q^2,S_tu)`.

Equality `S_tu=I_t` proves the contact completion in the target. Omitting it
would fail even at finite regulator. A constant theta-dependent vacuum
potential has `chi_t=0` and correctly gives `rho_theta_theta=chi`.

For the supplied fixed-Q saddle write `x=chi V`, `B=c4/chi^2`,
`d=4+chi_t/chi=4-D log chi`, and let its logarithmic remainder be R.
Direct differentiation gives the more explicit formula

`rho_Q-rho = d(1-Q^2/x)/(8V) + (B_t-4B)/(32V^2) - R_t/(4V)`.

This reproduces the H4 and H8 coefficients in target equation (9), including
the negative c4 term, when chi and c4 are t independent. In the Q=0 case,

`X_top = -D log chi/H + (B_t-4B)/(4VH) - 2 R_t/H`.

Thus the stated O(H3) contamination requires `B_t-4B=O(1)` and a sufficient
bound on R_t (the natural differentiated saddle bound
`R_t=O(V^-2)` is more than enough). This spells out what the target calls
uniform remainder/derivative control. Merely bounded c4, or a pointwise
`R=O(V^-2)`, does not suffice. The phrase should always be read to include
the first scale derivative of retained coefficients, not only of the tail.
Likewise `chi=chi0+a H+O(H^2 log H)` must be differentiated under a stated
error bound; an undifferentiated expansion alone does not imply the limit.

With those bounds, chi0>0 and `D chi=a H+o(H)`,
`lim X_top=-a/chi0`, and `(A_rho)_theta_theta=3a/4` follows from the exact
metric identity. Fixed-Q formulas are not uniform statements about all
`Q=O(sqrt(V))`; the target does not sum their asymptotic series termwise.
The exact statement that summing sectors returns the theta ensemble is valid.
The chi0=0 massless limit cannot use this saddle and is appropriately
discussed separately as an axial structural check.

## Exact primary-source coverage

All six PDF byte counts and PDF/text SHA256 pairs in SOURCES.json matched
the existing exact files. Relevant exact text supports the following arrows:

| Exact primary source | Checked implication and verdict |
|---|---|
| AFHO `0707.0396v2`, Section II.A `(1),(5),(6),(16)` | **Verified:** sets Z(0)=1, assumes analytic theta energy near its dominant minimum, derives the normalized fixed-Q saddle. **Conditional:** derivative-uniform S4 application. Its Fourier sign convention is opposite, harmless for the CP-even Q dependence used here. |
| Gorghetto–Villadoro `1812.01008v2`, Appendix A.1 `(27),(28),(31),(34),(36)` and main `(10)` | **Verified:** flat susceptibility EM coefficient and fixed-quark-mass to pion-variable translation. Independent LECs and calibration remain; no metric derivative is evaluated. The inspected version banner is 2025-12-07, as recorded. |
| Kotov–Lombardo–Trunin `2502.15407v2`, Sections 2.1–2.2, Table 1, Section 6.4 `(6.4)` | **Verified adjacent scope:** physical pion tuning, f_pi scale setting, thermal ensembles, and normalized `Z(theta)/Z(0)` reconstruction. **Inapplicable:** as a full S4 vacuum metric evaluation. No new exhaustive literature or continuum-error audit is claimed. |
| Makino–Suzuki `1403.4772v5`, Section 1, `(2.10),(2.11),(4.68),(4.70)`, Section 5 `(5.6)` | **Verified after local locator correction:** vacuum subtraction, separated-insertion restriction and EOM contact caveat. **Conditional:** as an implementation tool for integrated curved observables. |
| Zhitnitsky `1902.07737v2`, Section II `(1),(4)` and footnote 1 | **Verified adjacent scope/date:** version is 2019-05-08, proposes the linear inverse-size/holonomy response and leaves its strong-QCD coefficient to lattice computation. Does not evaluate the target S4 observable. |
| Yamamoto `1405.6665v2`, formulation and numerical application around Sections III–V | **Verified adjacent restriction:** inspected version banner, quenched simulation and curved FLRW formulation are consistent with the reused source audit. No unquenched full S4 vacuum-stress result is supplied. |

The mandatory citation correction is in
[SOURCE_LOCATOR_CORRECTION.md](SOURCE_LOCATOR_CORRECTION.md). This is the only
concrete error found in the reviewed targets. No exact source here supplies
the missing uniform differentiated QCD sphere theorem or an evaluated mixed
metric/current response. No exhaustive absence or novelty claim is certified.

## Computation check and scope

The reviewed script implements the stated seven-charge CP-even rational
fixture with a mixed action term, a direct normalized bivariate Taylor
coefficient check, constant trace-shift cancellations, four stated H values
and Q=0,1,2 Gaussian-sector algebra, and formal source-coefficient subtraction.
The fixed output path was replaced only in memory with this review's
CHECKS_RESULTS.json, and the compiled computation was executed once using
Python 3.9.6. All 37 checks passed and the complete result object exactly
matched the frozen author result. The source computation itself was unchanged;
its original hash is pinned in RECEIPT.json.

These are finite exact algebra assertions. The Gaussian derivative fixtures
do not test the non-Gaussian c4 term, saddle dominance, uniformity, continuum
QCD contacts or an actual H limit. The raw independent derivation checks the
explicit c4 coefficient algebra; neither that derivation nor the fixture
establishes the physical asymptotic input. The target's nonclaims are accurate.

## Physical scope, strongest safe statement and next check

The quantity X_top is an actual proposed measurement of a stress difference,
not an evaluation already performed. Under the named controls it is sensitive
to `(A_rho)_theta_theta`, and therefore can discriminate a mechanism with a
specified nonzero theta curvature. It does not test an arbitrary
theta-independent A_rho. A common factor `exp[-C(g,u)]` demonstrates precisely
that information limitation. For `C=V c(u)H` its stress shift is correctly
`3cH/4`, but locality/covariance and the fixed QCD definition still decide
whether any such term exists or is permissible. On a smooth closed sphere,
ordinary analytic local bulk curvature counterterms do not automatically
provide an H term. No physical counterterm freedom or all-QCD-gap no-go is
therefore inferred.

The smallest physical gap is a controlled sphere sequence evaluating the
action-defined joint trace/topology observable, with the retained-cumulant
scale derivative and remainder bounds spelled out. The cheapest check is
the target's proposed one-regulator comparison between joint Q/trace
measurements and independent radius differences of chi, before extrapolating
X_top. At order e^2 it also needs the matched I_t contact. The theta-independent
coefficient continues to require an unconditioned stress or an absolute
matched free-energy comparison. The full A_rho, R and a predictive alpha
remain unevaluated.
