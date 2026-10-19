# Independent global sphere review

Primary verdict: **correct only after a stated restriction**. Acceptance is limited to the declared positive-mass scalar determinant and the massless weak-coupling sphere coefficients, with the printed-source correction in `SOURCE_INCONSISTENCY.md`. The frozen targets do not compute full physical QCD, the proton-current functional, an infrared interpolation, or alpha selection. Their mathematical formulas within those restricted scopes are accepted.

## Claim card and independence

For one real scalar with `M>0`, `z=M^2/H^2>0` and `z+12xi>0`, the reviewed claim is an exact finite global S4 determinant after the declared subtraction through `a2`, its direct fixed-parameter metric derivative, and its first charge derivative for two real charged modes. The low-curvature statement holds uniformly on a positive-mass compact parameter neighborhood. It is not a statement about a minimal massless Gaussian scalar.

The ultraviolet claim is for fixed-nf=3 massless SU(3) plus one photon, with `u=e^2=4pi alpha`, all renormalized couplings and mu fixed during metric differentiation. The source has nine vector and nine Dirac color/flavor components. It is a finite-order weak-coupling result; perturbative logarithms must remain controlled. No assertion uniform in arbitrarily large `log(H/mu)` at fixed couplings has been established.

I saved `PRETARGET_DERIVATION.md` before reading target math, code, inputs, source records, or manifests; neither author REPORT nor a coordinator verdict was read. This is an isolated reviewer derivation, not proof by agent agreement. That preserved preliminary note contains my own free-anomaly sign error; `REVIEWER_CORRECTION.md` explicitly corrects it without rewriting the pretarget record. The target's free-anomaly sign is correct.

The exact target revisions are in `TARGET_HASHES_BEFORE.json` and `TARGET_HASHES_AFTER.json`. All nine requested target files had unchanged before/after SHA256 values, including both manifests. I changed only this review directory. The two author source/input records and their declared parent-input hashes were also checked; the three inherited parent pins match current bytes. The chiral action's mapping to `C,F,k15` is an input supplied for this review, not a fresh audit of the older source packet.

## Dependency graph

1. Given S4 eigenvalues/multiplicities -> heat trace -> local heat coefficients (internal exact derivation; Kluth--Litim independently confirms spectrum/coefficient normalization).
2. Declared heat subtractions -> convergent proper-time W -> fixed-M/xi metric derivative -> convergent resolvent / digamma identity (internal derivation, checked against original heat sum).
3. Positive-mass compactness + small-time heat asymptotics -> uniform differentiated large-z remainder (analytic argument; numerical samples are corroboration only).
4. Given charged mass/xi insertions + two real species -> charge chain rule -> conditional leading H6 response (internal algebra).
5. Primary gauge-sphere total logarithm + gauge normalization and beta functions -> fixed-coupling H derivative (external result plus internal algebra).
6. Separate primary QED exact Gamma expression -> photon exchange logarithm -> actual current trace `S=Nc sum Qf^2` -> electromagnetic slope (external result, independently extracted and expanded).
7. Free anomaly and local counterterm scaling -> total free/interaction sphere stress (external anomaly coefficients plus internal radius scaling).

There is no dependency arrow here from either controlled sector to the full infrared QCD coefficient or to a selected alpha.

## Obligation matrix

| Obligation | Result | Decisive point |
|---|---|---|
| Spectrum, volume, scalar factor 1/2 | passed | Original l-spectrum, including l=0; one complex charged pion is exactly two real modes |
| Heat coefficients and xi shifts | passed | `a3=37/189-58xi/15+24xi^2-48xi^3` independently derived |
| Complete finite-radius W and stress | passed | Target (3)-(8) agree with independently derived integral and resolvent; `rho=3H^4 z I/(32pi^2)` |
| Digamma continuation and exceptional points | passed | Conjugate pair above `q=9/4`, positive real arguments below; regular at coalescence and at `q=2`; actual zero-mode pole at q=0 |
| Subtraction finite parts | passed | `log z`, constant `2/9-2xi`, and `-a2/z` required by the declared common prescription |
| Charged mass and xi derivatives | passed | Full chain rule, including derivative of the stress prefactor, and correct two-real-mode factor |
| Positive-mass differentiated remainder | passed in declared regime | Common heat remainder and exponential tail bounds on compact parameters; no massless uniformity follows |
| Zero mode and chiral regime | passed | Gaussian massless determinant is singular; physical chiral zero mode requires another treatment |
| EFT-local ambiguity | passed | Independent R3 matching can change H6; finite dimension-four local terms cannot create linear H |
| Gauge log, H derivative, signs and traces | passed with source correction | Total (4.39) is RG-consistent and photon term is separately supported by primary QED (B.5) |
| Every cited v1 intermediate fermion equation consistent | failed | (4.30)/(4.34) factor two and (4.37)/(4.39) opposite signs; ordinary sum (4.2) does not resolve this |
| Free anomaly, gauge normalization, counterterms | passed | `H d_H W_free=-4a`; gauge `-log e` retained for RG; local Euler/R2 terms H-independent |
| Finite coupling normalization | passed after explicit clarification | H-independent `f(u,g)` shifts raw W/charge derivative, leaves fixed-coupling rho unchanged |
| Numerical finite assertions | conditional on stated numerical libraries/tolerances | Fresh direct sums/quadratures and positive-tail brackets; no interval certification |
| Declared v2 author manifests | passed as provenance | Both validate with `--root`, each `run.status=completed`; execution is not physics proof |
| Full QCD, cosmological continuation, alpha determination | out of scope | No missing bridge is silently supplied |

## Accepted scalar formulas

Let `I=integral exp(-zx)[Kxi-a0/x^2-a1/x-a2] dx` and `Psi=zI`. The exact source-independent result is

`I=(q-2)[psi(3/2+nu)+psi(3/2-nu)-log z]/6+2/9-2xi-a2/z`,

where `q=z+12xi`, `nu=sqrt(9/4-q)`. Consequently

`rho_one=3H^4 Psi/(32pi^2)` and `rho_one=37H^6/(2016pi^2 M^2)+O(H^8/M^4)` at xi=0.

The target's charged coefficient is correct:

`d_u(rho_pi/H^6) -> 3/(16pi^2)[116 k15/(15M^2)-74 C/(189 F^2 M^4)]`.

The target makes appropriate qualifications about higher-order pion/photon operators, the Gaussian p-regime, and the independent dimension-six gravitational action. Its uniform result implies only `d_u rho_pi/H=O(H^5)` in this selected positive-mass sector.

## Accepted ultraviolet formula and required source correction

Using the consistent total source logarithm and the separately checked QED result gives

`rho_UV/H^4=219/(320pi^2)+(u-27g^2)/(64pi^4)+O(g^4,u^2,ug^2)`,

`d_alpha rho_UV/H^4=1/(16pi^3)+higher orders`.

The frozen source narrative must be read with `SOURCE_INCONSISTENCY.md`: the individual printed fermion pole/finite term do not independently corroborate the total. The accepted coefficient has two real checks: total-log/RG consistency, and the older primary QED exact Gamma formula with its own W convention. No reconstructed two-loop finite constant is load-bearing for the stress.

The notation `alpha(mu)` would be a useful nonblocking clarification. In this review alpha is the declared renormalized source parameter at fixed mu. It has not been matched to a Thomson-limit charge. The target already excludes physical thresholds and does not assert such a matching.

## Fresh independent finite computation

`independent_checks.py` never imports an author module and writes only a caller-specified fresh result file. Its authoritative record is `run_002/manifest.json`, `run.status=completed`; the record validates with the computation-audit v2 validator and `--root`.

* Five original heat-sum / subtracted-integral cases: `(z,xi)=(1,0),(2,0),(2.25,0),(0.4,-0.02),(7.3,1/6)`. Largest absolute discrepancy from the independent digamma formula: `4.865e-21` at 55 decimals.
* Three positive spectral sums, 4000 terms each, with an explicit integral tail bound. All enclose the digamma value, including negative xi with a positive full spectrum and the `q=9/4` branch point.
* At `(z,xi)=(3.7,-0.02)`, a direct proper-time action difference at fixed M gives `-d_logH W=zI` within `9.789e-12` using step `1e-5`.
* A simultaneous two-real-mode charged mass/xi difference (`b=0.3`, `k15=0.007`, `du=1e-6`) agrees with the analytic charge chain rule within `1.829e-19`.
* Exact rational heat coefficients through x3, free anomaly `a=73/40`, strong `beta0=9`, and current trace `S=2` agree. Massive asymptotic samples approach `a3`; the small-z sample approaches `61/90` but is not given a physical Gaussian massless interpretation.

The low-time quadrature segment uses ten asymptotic heat terms below x=0.04; it is not interval-certified. Spectral bracketing supplies a separate check at the listed cases. No finite test proves the uniform remainder; its acceptance rests on the analytic heat/tail argument.

`run_001` was a failed reviewer run caused by an exact comparison of rounded mpmath values. It is preserved, its original script bytes are pinned under `historical_inputs/`, and the precise transition is in `RUN_TRANSITION.md`. It supplies no successful result evidence.

## Sources, commands, and remaining gaps

Source versions, hashes and exact locators are listed in `SOURCE_RECORDS.json`. The accepted scalar source is arXiv:1910.00543v2, Table 4 and (88), with the stipulated volume/spectrum definitions. The gauge sources are arXiv:2212.11848v1, (4.1),(4.34),(4.39)-(4.46), and arXiv:1508.06354v3, (4.15),(4.16),(B.5); differing epsilon and G2 sign conventions are translated explicitly in the correction note.

The two author commands were audited statically. I did not run either author program or overwrite their outputs. The fresh command and exact limits are in the review contract/run manifest. The validator was run on each author manifest and the fresh review manifest:

`python3 <computation-audit>/scripts/validate_manifest.py MANIFEST --root /Users/carlzimmerman/new_physics/zimmerman-formula`.

Residual gaps are physical matching and omitted sectors, not defects in the scoped scalar calculation: independent chiral and gravitational low-energy constants, pion/photon and mixed higher loops, thresholds, nonperturbative strong dynamics, and a shared all-radius QCD/proton construction. Neither a calculation in the ultraviolet theory nor a free pion determinant settles the full linear-H coefficient. No alpha or full target ratio is certified.

Self-proofreading of the review-only additions found no remaining local notation/typography issue. No mathematical token in a frozen author file was changed.
