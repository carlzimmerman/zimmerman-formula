# Independent review of the nonconstant-photon epsilon contribution

Primary verdict: **conditional on named inputs**. The coupled quadratic photon/pion cancellation, transverse S4 spectrum, defined zeta tadpole, photon-only curvature residue, and compact metric/charge derivatives are correct at the declared epsilon² order. A physical absolute sphere response remains conditional on finite curvature/source matching, consistent Maxwell normalization, and the unresolved pion-Z counterterm bridge. No full-NLO, full-QCD, or alpha claim is certified.

## Independence and audited revision

I saved `PRETARGET_DERIVATION.md` and ran the independent checks before reading any new author `epsilon_photon/` target. `GLOBAL_QUOTIENT_NOTE.md` separately derives the residual U(1) quotient and distinguishes its normalization from source-only curvature contacts. The exact target code/math/source/input revisions are in `TARGET_HASHES_BEFORE.json` and the final check in `TARGET_HASHES_AFTER.json`. The five science/code/input/source/contract files were frozen when read. The completed author run is `run_002`; the failed `run_001` is not accepted result evidence.

Both completed review directories, `global_sphere/` and `compact_chiral/`, were read-only throughout; their full before/after file hashes are checked against `PRIOR_REVIEW_HASHES.json`. No author script was imported, executed, or edited. No inherited compact-integral grid was repeated.

The normalized claim is the source-dependent ratio around a constant SU(2) orientation with canonical photon, `u=e²~epsilon⁴`, `H~epsilon`, zero-average nonconstant pion fields and effectively massless nonconstant pion kinetic operator at this order. The photon correction is first order in the transverse mass squared `uF²s`; the compact LO y=uCV dependence remains resummed. This is not a Taylor approximation of the entire compact partition at fixed physical volume and mass to all orders in u.

## Gauge cancellation is the load-bearing result

The original LO kinetic action gives one canonical tangent pion along the gauge Killing vector and a mass parameter `mA²=uF²s`. For every scalar nonconstant eigenvalue lambda>0, the longitudinal photon and that pion have block

`[[lambda/xi+mA²,−mA sqrt(lambda)], [−mA sqrt(lambda),lambda]]`.

Its determinant is `lambda²/xi`, exactly independent of mA. The order-u longitudinal seagull and the two derivative-mixing insertions therefore cancel. In Landau gauge `integral A_T dot grad pi=0` on closed S4, giving the same transverse-only result. This supports the surviving seagull only **after** checking the combined determinant.

The author's equation (2) is accepted with its explicitly declared transverse reading of the Maxwell Hodge term. On the complete vector space the gauge-fixed Maxwell operator is `delta d+(1/xi)d delta`; adding a full Hodge longitudinal kinetic term would spoil (5), and is not the operator used by the target's block calculation.

Abelian prime ghosts and the Hodge/gauge-fixing measure are source independent for this ratio. The constant scalar gauge parameter generates no longitudinal vector and is omitted once. The collective pion constant mode stays in U0. S4 has no harmonic one-form; no photon vector zero mode is introduced. The residual global U(1) rotates the charged angle; a direct Haar-coordinate quotient, or its a2=0 Faddeev–Popov patch, gives the same uniform s pushforward measure. The s=0 stabilizer is handled by continuity, not by deleting orientations or inserting a new s-dependent determinant.

## Obligation matrix

| Obligation | Result | Evidence |
|---|---|---|
| Pauli seagull and derivative mixing factors | passed | `Tr[Q,U][Q,U]dag=2s`, gauge Killing norm²=s; canonical `mA²=uF²s` |
| General covariant-gauge cancellation | passed | Exact nonconstant 2×2 determinant; seagull/mixing coefficients cancel modewise |
| Landau reduction | passed | Closed-sphere integration by parts kills transverse derivative mixing |
| Global quotient, scalar prime, no H1 mode | passed in declared ratio convention | Explicit Haar quotient and primary global-gauge determinant normalization |
| Transverse Hodge spectrum and multiplicity | passed | lambda/H²=(l+1)(l+2), d=l(l+3)(2l+3)/2, l>=1; lowest level 6 with degeneracy 10 |
| Transverse trace multiplicity | passed | Already included in d_l; no extra polarization factor allowed |
| Curvature pole and finite zeta prescription | passed | Heat coefficients 1/2,−1,19/30; residue−1 and FP=2/3−2gamma independently derived |
| Photon beta15 comparison | passed under explicit common bare convention | Pole requires delta k15=−1/(64pi²epsilon), hence photon beta=1/2 |
| Finite k15 running and fixed-mu metric derivative | passed in the declared photon scheme | Explicit mu log cancels photon-only running; radius derivative keeps the log term |
| Compact covariance/cumulant response | passed | Independent chain rule and one fresh numerical metric/u check |
| Full k15 pion-Z bridge | unresolved, correctly excluded | Photon agreement supplies no missing pion/off-shell/form-factor translation |
| Source-only R·EM contact and absolute Maxwell factor | separate matching obligations | Neither is fixed by the orientation ratio or by normalized Haar measure |
| Full NLO/QCD/alpha or fixed-mass H→0 | out of scope | Target explicitly excludes these extrapolations |

## Spectral and renormalization checks

The transverse heat trace is the full Hodge-one-form trace minus the prime scalar trace. Its local curvature coefficient is `−R/2`, yielding

`K_T(t)=1/(2t²)−1/t+19/30−5t/63−11t²/630+...`.

Consequently `Res zeta_T(1)=−1`. In the fixed-S4 finite-part prescription, the independent half-integer/Hurwitz calculation gives `FP zeta_T(1)=2/3−2gamma`. An independent heat-Mellin calculation includes the inverse-Gamma finite contribution and confirms this value. It is a defined subtraction-scheme result; the negative finite tadpole is not a negative bare covariance.

The source correction is `delta W_gamma=t q`, with `q=<s>`. Before finite local matching,

`t=uF²[2/3−2gamma−log(mu²/H²)]/(2H²)`.

Its pole is `−uF²RVs/(64pi²epsilon)`. Comparing the literal Euclidean orientation operator `−uF² k15 R s` gives `delta k15=−1/(64pi²epsilon)`. With d=4−2epsilon and `L_pole=1/[16pi²(d−4)]`, this independently matches the photon-only source coefficient beta15=1/2. The target's finite combination `−64pi² k15,zeta^r` and photon-only running are algebraically consistent in this common convention. The usual finite MSbar value cannot be substituted without a conversion.

The k15 operator also contains its constant 5/9 part. A pure-source electromagnetic curvature contact is required to track that component; its finite value is not determined here. The free Maxwell determinant/global gauge factor is likewise a separate absolute normalization. Its nonanalytic raw free-coupling logarithm cannot be differentiated as though it were this analytic O(u) insertion at u=0. The target explicitly factors the same-u orientation ratio, which avoids that error.

## Response check

Writing `h=t/u`, `D=V partial_V`, the independent calculation gives

`delta rho=[(Dt)q+t(x Cov(a0,s)−y Var(s))]/V`.

At fixed renormalized parameters and mu, `Dt=t/2−uF²/(4H²)`. Taking a charge derivative adds the second and third cumulant terms in target (18). Rewriting my independent expression with `y=uCV` reproduces it exactly. Omitting the derivative of the Haar distribution or holding a numerical tadpole constant fixed while varying H would fail this check.

## Computation and provenance

The author code was statically audited. It checks exact Pauli/gauge algebra, the finite-part continuation and its positive geometric tail bound, direct heat sums, a short early-time asymptotic quadrature segment, and symbolic source/metric/RG identities. The finite-series tail formula follows from a Hurwitz integral bound and ratio c/A²=1/25. The three finite Laurent offsets are numerical checks; no interval proof is claimed.

Observed authoritative author record: `epsilon_photon/run_002/manifest.json`, status completed, exit zero; it validates against current files with `--root`. The heat finite-part discrepancy is `9.765e-24`, below the unchanged `1e-20` criterion. The author result manifest pins all executed science inputs; execution success alone is not the gauge/physics proof.

The earlier author `run_001` failed the heat finite-part assertion and produced no declared results file. The historical snapshot's SHA256 matches its original code pin `55d547b99e6b5838bcec4a317a1577143ba48ba0b0ba94763500215aa36b11b7`. I checked the exact diff: the live code changes the early-time heat default from order8 to order10, leaving the assertion tolerance unchanged. The old manifest remains a failed historical record and its live input path is stale; its original executed bytes remain available in the snapshot. It is not conflated with completed run002.

Fresh reviewer record: `reviews/epsilon_photon/run_001/manifest.json`, completed and validating. It independently checks the exact coupled determinant, rational transverse heat coefficients, heat-Mellin finite part, and one genuinely new response point `(x,y,u)=(1.3,0.2,0.04)` with fixed-mu derivatives. Results:

* Heat-Mellin finite-part discrepancy: `2.807e-21` at 45 decimals, with a separate x<0.04 heat segment and harmonic cap200.
* Fixed-parameter metric finite-difference discrepancy: `1.462e-27`.
* Charge-response finite-difference discrepancy: `4.280e-26`.

The fresh quadrature is conditional on the stated arbitrary-precision libraries and asymptotic early-time treatment. It is not interval certified. No old compact grid was rerun or counted as new.

## Sources, remaining gap, and safe conclusion

`SOURCE_RECORDS.json` pins the primary gauge/QED spectra and global quotient conventions, and the literal Kubis–Meissner operator/beta source. De Cesare–Di Pietro–Serone v1 (2.13)-(2.32) and Giombi–Klebanov–Tarnopolsky v3 (2.4)-(2.11) support the rough-vector/Hodge shift and prime/global factor. Their previously noted interacting-fermion discrepancy is irrelevant to this new calculation and was not used. Kubis–Meissner v2 (4.7),(4.8) supplies only the comparison convention; its photon term was not imposed as an answer.

No forced correction to the frozen photon science was found. The strongest safe conclusion is a gauge-complete quadratic nonconstant-photon source contribution at epsilon² order, with a checked photon-only curvature residue and conditional finite scheme. The remaining physical task is to assemble pion, photon, source-only and curvature terms with the absolute state/gauge normalization in one matched scheme. The old pion-Z bridge remains unresolved. This result does not compute the full QCD sphere response, an H-linear coefficient, a proton ratio, or a value of alpha.

Self-proofreading covered only this new review directory. Both completed earlier review directories and all frozen author inputs remain unchanged.
