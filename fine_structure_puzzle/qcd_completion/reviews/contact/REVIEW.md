# Independent contact-sector audit

Normalized claim: on a closed round S4, for the specified compact abelian
three-form measure with fixed chi_g>0 and its compact singlet constant-mode
extension B>=0, the displayed flux/branch normalizations, rho=-d_V log Z,
B=0 screening, Laplace coefficients, and absence of a linear-H term at
theta=0 are correct. The determinant replacement in section 4 defines a
Gaussian-plus-exact-constant-mode approximation, not the interacting QCD
partition function.

**Primary verdict: proved as written**, within that explicitly stated model.
No blocking mathematical error was found. This verdict does not establish
full-QCD matching, its metric-dependent normalization, a general QCD no-go,
or a fine-structure prediction. Those are already left open by the target.

Review provenance: fresh subagent `contact_independent_review`. The full
derivation in `INDEPENDENT_RAW.md` was saved before the target files were
read; it starts with the compact gauge theory and canonical scalar
coefficient, not the target implementation. The target code and report were
subsequently audited, and a new independent implementation was executed in
this review directory without importing the target code. No target input or
existing result was edited or overwritten.

## Exact revision and source checks

Repository HEAD: 9516ee01c79f35c04b7556050669ba77b0c98b99, dirty worktree.
Authoritative project contract: `qcd_completion/CONTRACT.md`, SHA256
9ebafcae2324cfd421a5d4793e2f9e6cf4312ea7858494972c72a48dcef401c1.
Paths below are relative to `fine_structure_puzzle/qcd_completion/` unless
otherwise stated. Target files have the following unchanged hashes:

| Artifact | SHA256 |
|---|---|
| anomaly_contact/DERIVATION.md | ff7049109b26b20be2722f272c9705adfe9de7b444d49a941efaaa2096e89204 |
| anomaly_contact/check_contact.py | 9380a229cb0e51c3be012acf6ddc49d1137dd8a438d5f4758f9646531757568b |
| anomaly_contact/contract.json | 26ca6d9a0611079698a66268517751b54f33fa38900ec184a44a3ba3c21a0165 |
| anomaly_contact/run-001/results.json | d13d66af8051a2f21dcd6b37f43f5f00841562b302a6d9c468dcd17012a1a399 |
| anomaly_contact/run-001/manifest.json | 192efd4ee4ef2d4a46a7733aceaba6791cf1ddc01bbaf8333674a04adcee1c73 |

Primary sources checked:

- Donnelly--Michel--Wall, [arXiv:1611.05920v1](https://arxiv.org/pdf/1611.05920v1),
  equations (2.1), (2.7), (2.9), (2.14), (2.19), printed pages 5--8.
  The cached exact-version text was read before the target; its source
  metadata and exact-version official PDF were subsequently checked online.
  The cached PDF and text hashes agree with `anomaly_contact/SOURCES.json`.
  The p=3,D=4 application of the partition formula is verified. No use of
  a negative-degree dual theory is needed.
- Dvali, [hep-th/0507215v1](https://arxiv.org/abs/hep-th/0507215v1), section 4,
  equations (36)--(44), printed pages 11--13. Cached exact-version text and
  official version metadata checked. This motivates a composite QCD
  three-form and screening; the exact function K(F) is unknown there.
  It does not establish the chosen Gaussian global measure or curved
  matching. The target correctly states that limitation.

No novelty search was performed; no novelty verdict is given.

## Dependency graph and obligations

The source measure plus integral flux quantization implies the canonical
three-form prefactor and Gaussian flux weights. Hodge spectral pairing
eliminates the nonzero oscillator product. Poisson summation yields the
constant-normalized branch sum, whose volume derivative fixes the stress.
The scalar L2 coefficient supplies its sqrt(V) measure. Unfolding and Fourier
analysis then establish B=0 screening and the exact compact identities;
Laplace expansion yields the large-volume stress. The optional nonconstant
Gaussian determinant uses the prior scalar heat-kernel subtraction and has
its Gaussian zero mode replaced exactly once. No leaf in this graph supplies
the missing microscopic QCD metric functional.

| Obligation | Status | Decisive check |
|---|---|---|
| Type, signs, dimensions and fixed-coupling variation | Passed | chi_g and B have dimension four; q has dimension two; the exponent and zero-mode measures are dimensionless. |
| Ghosts-for-ghosts and hidden determinant anomaly | Passed | Coexact exponents are (1/2,-1/2,1/2,-1/2); equal positive spectra C3=C0 and C2=C1 pair exactly in a shared regulator. |
| Harmonic gauge-volume normalization | Passed | Equation (2.14) gives (2 pi mu^8 V/q^2)^(-1/2); Gamma_0=V. |
| Global flux/branch normalization | Passed | Canonical Z is (2 pi chi_g/mu^4) sum_k exp[-chi_g V(theta+2pi k)^2/2]. The divided factor is V independent. |
| Sign of rho | Passed | In flux variables rho=1/(2V)-<Q^2>/(2 chi_g V^2); in branch variables rho=<chi_g(theta+2pi k)^2/2>. |
| Scalar compact measure and Fourier phase | Passed | a0=f_s sqrt(V)phi. The sign in exp(-i n theta) is equivalent to exp(+i n theta) after n->-n. |
| B=0 screening | Passed | Unfolding gives sqrt(2pi/(chi_g V)), cancelling the canonical sqrt(V); Z0=mu f_s/sqrt(chi_g). |
| Laplace coefficients and leading H^8 stress | Passed | Independent Gaussian moments reproduce both displayed coefficients; rho0=B/[8(chi_g+B)^2 V^2]+B(3B-chi_g)/[24(chi_g+B)^4 V^3]+O(V^-4). |
| Finite-volume susceptibility and infinite-volume screening | Passed | Fourier charge moments and the unfolded variance give the same curvature; minimization gives chi_g B/(chi_g+B). |
| No duplicated Gaussian zero mode | Passed | The determinant zero mode is mu/M_s; multiplying by Z0/(mu/M_s) replaces it. It does not multiply it twice. |
| Ordinary scalar H^6 term | Passed for referenced subtraction | Prior FSP-003 proper-time prescription subtracts H^0,H^2,H^4; the heat coefficient 74/63 gives the stated positive stress. Higher local matching terms remain separate. |
| Exact interacting nonconstant singlet theory | Out of scope | The target expressly calls section 4 an approximation and omits its interactions and walls. |
| Full QCD and metric-dependent absolute normalization | Not addressed | An additional theta-independent metric functional changes stress while leaving normalized theta correlators unchanged. The target explicitly retains this gap. |

For the imported scalar result I inspected
`fine_structure_puzzle/qcd_prediction/coordinator/curved_pion/DERIVATION.md`
(SHA256 b0b3028571ec737b813ee11a9fe52f518d56e1462a16af54368eea393e3ae96b)
and its `REPORT.md`
(SHA256 59a5ccba8790f2c4f7af51a929119305106323f76e92ebc50b3d42609118e1eb).
The exact spectrum and heat/subtraction argument support this reuse. I did
not rerun its older numerical suite. The H^6 coefficient is a statement
about that residual determinant; it is not a universal matched gravitational
Wilson coefficient.

## Findings by severity

No P0, P1, or P2 correctness defect was found in the assigned target.

**P3, evidence-label precision:** `check_contact.py`'s final
`assertion_tested` includes “canonical spectral and zero-mode cancellation”.
The code symbolically checks the oscillator exponents and numerically checks
the already normalized Poisson and scalar identities. It does not derive
the gauge zero-mode factor from Gamma_0=V or verify the source formula's
normalization; that factor is inserted into the displayed mathematical
definitions. The canonical gauge-volume claim is supported by the source
translation and hand derivation audited here. It should not be represented
as independently certified by the 94 numerical/symbolic checks. This does
not change any result or invalidate the manifest.

One boundary observation, not a defect in the target's theta-zero claim:
there is no uniform B->0,V->infinity limit for all normalized observables.
For fixed theta not congruent to zero modulo 2pi,

    lim_(B->0+) lim_(V->infinity) Z0(theta)/Z0(0) = 0,
    lim_(V->infinity) lim_(B->0+) Z0(theta)/Z0(0) = 1.

For each B>0, the minimized potential is strictly positive at such theta;
at B=0 the partition is exactly theta independent. At theta=0, the two
iterated limits of Z0 and rho0 agree. The limiting energy density and
susceptibility also tend to zero with B. This distinction prevents an
unwarranted extension of the target's fixed-positive-parameter asymptotics.

## Computation audit and new independent check

The target `run-001` contains 94 checks: four symbolic checks and, at each
of 55 and 80 decimal digits, 12 pure flux comparisons, 18 compact Fourier
comparisons, 9 susceptibility comparisons, and 6 asymptotic stress checks.
The loops match the declared finite bounds. The tolerance is floating
precision, not interval certification. The Gaussian tail and charge-series
cutoffs are negligible in the tested representation comparisons. The
large-volume stress residual is tested only at its declared six points
per precision; the all-V asymptotic statement comes from the Laplace
argument, not those finite checks. I inspected the code and output and
validated its manifest; I did not rerun or overwrite the target suite.

The independently written `independent_check.py` does not import the target.
Its pre-execution contract is `independent_contract.json`; it tests 47 finite
assertions at 60-digit precision, including direct derivatives of the
canonical flux partition, branch stress, direct derivatives of the compact
integral, the explicit scalar-measure term -1/(2V), B=0 controls, and two
joint-limit paths. `run-001/manifest.json` in this review directory records
status `completed`, unchanged inputs and hashed results. It passes manifest
validation with `--root`.

The two joint-limit paths at V=10000, theta=0.8, chi_g=1.7 give

| B(V) | Z0(theta)/Z0(0) |
|---|---:|
| V^-2 | 0.999969672023014420768967998869 |
| V^-1/2 | 7.8340158004019921635361965208e-14 |

These finite values support the separately proved nonuniform limit; they
are not offered as a numerical proof of the limit.

Commands used for validation:

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py fine_structure_puzzle/qcd_completion/anomaly_contact/run-001/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py fine_structure_puzzle/qcd_completion/reviews/contact/run-001/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

Regeneration of the independent check must use a fresh output directory,
not overwrite `run-001`. The exact launch argv, environment, enforced
60-second wall cap, CPU cap, software versions and observed runtime are in
the independent run manifest.

## Strongest safe statement and next physical obligation

The canonical compact Gaussian contact sector has exponentially small
theta-zero finite-volume stress. Its compact singlet constant-mode
completion has leading H^8 stress for B>0 and exactly zero stress at B=0.
The explicitly defined Gaussian extension adds the ordinary massive scalar
residual beginning at H^6. None supplies a linear-H coefficient at fixed
positive matched parameters in these stated approximations.

To establish a statement about actual QCD, the missing arrow is a microscopic
matching of the full metric functional and composite-field/global-state
measure, including theta-independent normalization and curvature-dependent
terms. Matching only chi_g or singlet screening does not fix that arrow.
The cheapest necessary next check is to specify such a matching observable
or controlled microscopic geometry before assigning a physical A_rho.
