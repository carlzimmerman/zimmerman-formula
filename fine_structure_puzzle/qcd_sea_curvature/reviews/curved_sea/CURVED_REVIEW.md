# Independent review: curved trace contribution

Normalized claim: at positive pion masses, the LO SU(2) chiral two-pion trace cut defines a finite, three-times-subtracted scalar metric response about flat Euclidean space. Its electromagnetic mass-path derivative is only one selected contribution. It supplies no full QCD+QED response and no homogeneous sphere coefficient.

Primary verdict: **proved as written**, for that explicitly delimited LO/chiral/dispersive claim. No blocking error found in DERIVATION.md or REPORT.md at the hashes below. This verdict does not assess a full-QCD numerical coefficient; none is asserted by the audited target.

## Independence and revisions

The isolated reviewer saved PRETARGET_DERIVATION.md before opening target DERIVATION.md, REPORT.md, checks or prior verdicts. Only the permitted source-path manifest had been read. The critical cut, source-Hessian sign, curvature factor and cutoff moment were freshly derived there. The target was subsequently audited, not edited. No author messages, external jobs, installs, Git mutations, navigation edits or prior-artifact edits were made.

Audited bytes:

| Artifact | SHA-256 |
|---|---|
| curved_response/DERIVATION.md | 7c1e7be130fe68db362408cc7acf53505a35270c1ac4b9390f3ce5c30192fc79 |
| curved_response/REPORT.md | 3e55070d492eec4a1470e846479b7ac1c11af7a80e590439e75f2fe2f24d7931 |
| curved_response/checks/check_trace_cut.py | 53268f27bdcaa7bc5a4dbb3dca4a78c7142a6739d8393d218ab4b627fc5a1303 |
| curved_response/SOURCES.json | b6ee48014acf8e6e44a0e941617b2ecf4b098dc5c3279603f7a00525424bd2a2 |
| curved_response/INPUTS.json | 1282badb4caf6d2190bba59459c82fde78641f63a065f87886e4f7abd09a49df |

No Git revision/dirty-state observation is asserted. CHECKS.json verifies all four pinned input snapshots against their declared hashes and compares them to current source bytes.

## Dependency graph and obligations

`LO covariant pion action -> crossed trace vertex -> two-body cut -> subtracted Stieltjes kernel -> W=-logZ Hessian -> R F R normalization` is the internal mathematical chain. The independent EM matching chain is `Urech mass operator + fixed matching path -> charged mass dependence`, and `Kubis–Meissner k15 operator/running + charged trace vertex -> separate curvature insertion`. Neither chain includes an implication to the sphere one-point stress.

| Claim | Primary verdict | Decisive check |
|---|---|---|
| LO trace amplitude and spectral multiplicity, eqs(4),(5) | proved as written | amplitude s+2M²; phase space beta/(8pi), 1/2! and discontinuity 1/2 give one-real-species rho=beta(s)(s+2M²)²/(32pi²). Three real pions and two charged real species are counted once. |
| Three subtractions and sign, eqs(1),(7),(12) | proved as written | Pi_hat=−P³ integral rho/[s³(s+P)]; W''=contact−cov reverses the separated sign. R_linear=6P sigma with no 1/2 in R F R gives F_hat=P integral rho/[s³(s+P)]/72. |
| Cutoff moment and leading singularity, eqs(9)–(13),(24) | proved as written | v=sqrt(1−4M²/Lambda²) yields [3v³−6v⁵/5+v⁷/7]/(256pi²M²). At fixed positive cutoff the leading term is 17/(2240pi²M²) per real pion, and F'_hat=17/(161280pi²M²). The NLO-order caveat and unknown physical-mass tail are retained. |
| Finite-charge mass component and derivative, eqs(15)–(17) | proved as written | Both threshold and s+2Mplus² vertex change. Two charged species give derivative −17C/(560pi²F²M⁴) with respect to lambda=e². Inputs M,F,C and the fixed-strong-input path remain declared. |
| k15 normalization and running, eqs(18)–(21) | externally proved in the exact required form | Primary v2 eq(5.12) fixes the explicit e² convention. beta15=1/2+2Z/3 and k15^r=beta15[kbar15+log(M0²/mu²)]/(32pi²) give 12e²k15^r s=e²(3+4Z)s[kbar15+log(M0²/mu²)]/(16pi²). Charged-species expansion gives c=1+12e²k15^r and the stated moment insertion 3k15^r/(10pi²M²). |
| Completeness restrictions on EM response and contacts | proved as written | The isolated mass and k15 terms omit independent photon/chiral/inclusive contributions. Differentiating W'' produces the five terms in eq(22), including all metric/current seagulls. The source paper requires radiative completion, so an exclusive charged-pion square is not promoted to a physical inclusive cut. |
| Local R Box R ambiguity and homogeneous S4 boundary | proved as written | A local R Delta R coefficient can shift an analytic Taylor coefficient while leaving its discontinuity unchanged. On round S4, Delta R=0. The positive-mass k15 tadpole has only local integer curvature powers; this does not calculate or exclude a global/nonanalytic H-linear term. |
| Bounded check execution and assertion | computationally verified only in a stated range | Byte-identical owned copy reproduces all 20 (z,c) kernel comparisons and five cutoff cases. Independent original-s cutoff quadrature and analytic-bubble evaluation agree on the stated additional cases. |

The k15 row verifies the source/operator translation; the moment insertion itself is also independently checked algebraically by `I'(1)=2/5` and `2 charged *12 k15*I'(1)/(32pi²M²)=3 k15/(10pi²M²)`. Its scale dependence is not canceled by treating k15 alone as an observable. The target correctly retains this restriction.

## Exact source check

B. Kubis and U.-G. Meissner, *Virtual photons in the pion form factors and the energy–momentum tensor*, [arXiv:hep-ph/9908261v2](https://arxiv.org/abs/hep-ph/9908261v2), 15 May 2001. The retained primary PDF's title/authors/v2 banner were authenticated. Printed pp11 and14 were rendered and visually checked; eq(2.5) and explicit-e mass formula (2.7) were checked in extracted text. PDF SHA-256 is `6c4267db298d51fdf8df0205edeaa5dede792b4b014eb88cd2397e58025bdb72`; text hash is `a45aa7e4dbdbb336bee02ee056f65723af22d4eccd1bd8ee198347980ab5949c`.

The source's raw operator display (4.7) suppresses e² while its nearby Q is written dimensionlessly. Reading that display alone would be ambiguous. The explicit-e charged trace formula (5.12), together with (2.5),(4.8), resolves the convention and agrees with target eq(20); no extra e² is inserted into an already explicit-e formula. The k15 term is independent of the mass splitting. The finite part is not fixed by its beta function. The source also has strong curvature constants, photon functions and an infrared logarithm in (5.12), and real-photon completion in section6.2. These are the exact restrictions used by the target.

Source authentication, formula extraction and target application were all performed. The browser could not newly fetch the old arXiv version URL, so authentication relies on the retained primary PDF, not a web snippet. No claim about the currently latest version or a global absence of curved-QCD data follows from that failure. Other target source metadata were not exhaustively re-audited; the load-bearing cut, contact identity and geometry boundary were independently derived. UV tensor/RG work is outside this review.

## Computation, availability and constraints

Command: `python3 fine_structure_puzzle/qcd_sea_curvature/reviews/curved_sea/run_review_checks.py`.

The script copies the documented target check byte for byte into this review's checks directory, executes it there, and records target hashes before/after. The target files remain unchanged. CPython3.9.6 on macOS26.5.2 arm64 completed; the 20 target kernel comparisons reproduce maximum absolute discrepancy 4.5467102305352114e−15. The independent cutoff check integrates in the original dimensionless s/M² variable (threshold regularized by log(s/4)=w²), rather than the target beta variable. Four further minimal-coupling cases compare a closed analytic scalar bubble against the target cut quadrature. CHECKS.json records exact cases and discrepancies.

Exact rational coefficients are algebraic checks. Double-precision quadrature is bounded evidence at the stated tolerances, not a proof on an unbounded numerical domain. No measured alpha, pion/proton mass, cosmological scale or fitted LEC was inserted. The source/check artifacts are local public inputs, not a new lattice dataset. All required unknown physical matching constants and the high-energy spectral tail remain unknown.

## Exact remaining gap and strongest safe statement

The package supplies an evaluated LO low-energy trace cut, its finite-cutoff moment and a chosen dispersive flat scalar metric response, with two isolated charge-dependent components. The complete physical-mass inclusive QCD+QED response requires matched finite LECs, loops/radiative states and nonpionic spectral data. The sphere coefficient separately requires the specified unconditioned curved-ensemble one-point stress and control of its global radius limit. No q=H substitution or flat-to-S4 bridge supplies that input.

A low-cost next test is a common-regulator trace correlator and its metric contact at several positive light-quark masses, with subtractions specified, testing the leading 51/(2240pi²) two-flavor chiral moment. This tests the calculated component; it does not test the global H-linear coefficient. On S4, metric variation can make some individual local powers vanish (for example the four-dimensional R² contribution); this does not alter the no-linear-H conclusion.
