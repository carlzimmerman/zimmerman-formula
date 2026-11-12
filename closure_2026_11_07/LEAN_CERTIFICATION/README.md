# Lean certification of Claude's latest closure work, 2026-11-07

**Premise update, 2026-11-07:** web-side CMB-lensing numerical bounds await GL3's reread following GL2's kernel audit. The conditional Lean statements remain valid; consult the [latest certification](../LEAN_LATEST_CERTIFICATION/README.md) before using their numerical premises.

**Verdict: conditional on the named physical and numerical inputs.** Lean checks
the algebra below. This is not certification of the complete gravity theory,
of its covariant variational derivation, or of agreement with observations.
Kappa = 1/2 FITTED; not theory closed. No adoption or deposit is performed here.

The reviewed remote revision is `df13ade969149d6dc1ccf864222bcc0f338b1bca`
(PAPER70 v0.4 and the November 7 closure register). The current checkout at the
start of the review was `a9063fbd089f8c3b1978bab31a6d859909b24a48`; the
publication worktree starts at the remote revision to preserve concurrent work.
`verification.json` records exact hashes of every compiled source and log.
The final worktree incorporates Claude's PAPER70 v1.0 publication at
`861efa1171`; none of the reviewed Lean sources changed from the initial
snapshot. PAPER70's updated v1.0 audit was rerun after that integration.
Provenance: Codex self-review, not an independent mathematical referee report.

## Claim cards and dependency graph

| Claim, domain and hypotheses | Certified conclusion | Input still owed |
|---|---|---|
| EW2: real scale m, web requires m >= 10, hosts require m <= 0.063 (or 0.1 with free Delta) | No m satisfies both; the nominal ratio is exactly 10000/63, about 158.73 | The bounds must hold for every admissible action member; a sampled scan alone does not prove that universal premise |
| WL1: real retained population q >= 0.384, coherent response r = (1+q)^2 | r > 1.072; this covers each of the reported canonical/alt q values separately | Population integration, redshift evolution, bias and coherent response model; no halo-model spectrum is proved |
| FA3: any finite index set, real weights w_i >= 0, real source values, common weights, pointwise web_i >= c host_i | Sum w_i web_i >= c Sum w_i host_i | Pointwise history comparison, common normalization and identification with the physical response |
| FA3 gate: c >= 0, web >= c host, host >= hostMin, web <= webMax, webMax < c hostMin | The gates are incompatible | Physical validity of those inequalities; the finite-sum result is not a continuous-kernel theorem |

Dependencies: source results and model conventions -> explicit inequalities ->
real arithmetic / finite-sum order -> gate exclusion. The first arrow remains
conditional; the second is checked by Lean. Nothing points from a gate exclusion
back to a proof of its input bounds.

## Existing algebra rechecked

The verification script compiles these nine sources from
`fable_independent_2026/lean_2026/`, checks every printed theorem's axiom list,
and separately compiles their MUTATE twins:

| Source | Theorems | Scope |
|---|---:|---|
| QX1_closure_chain | 28 | Constitutive law, roots, clock/charge and dispersion algebra |
| QX17B_field_equations | 12 | Legendre and field-equation algebraic kernels |
| FRW_correction | 11 | Corrected mixing algebra and speed bounds |
| SE1_shock_entropy | 5 | Entropy-sector algebra |
| SV1_shell_bound | 5 | Finite shell sums under nonnegative radial-component hypotheses |
| SV2_causality | 5 | Time-ordering algebra, given the stated causal assumptions |
| SV2_repair | 11 | Dispersion/anisotropy algebra within the specified class |
| SV5_growth_nogo | 15 | Weighted bounds, projection, switching and history algebra |
| EW2_aest_window | 4 | Capped map, leakage, finite dust sum and abstract empty window |
| ClosureLatest (this directory) | 11 | Exact threshold consequences, finite memory order and counterexamples |

Total: 107 theorems. Allowed axioms are only `propext`, `Classical.choice` and
`Quot.sound`; no `sorryAx`, new axioms or admitted proofs are accepted. The
MUTATE files are expected compiler failures. Rejection of an attempted proof
is **not** proof that the theorem is false, and a file-level failure does not
certify that every mutation was detected. The new file additionally proves
concrete counterexamples for EW2's cap-identity and reversed-leakage mutations.

## Obligation matrix and remaining gaps

| Obligation | Reading |
|---|---|
| Exact Lean statements under their explicit hypotheses | Passed when `verification.json` says all_passed |
| Axiom inspection for every compiled positive theorem | Passed when the recorded lists contain only the allowed standard axioms |
| Existing rejection controls | Compiler rejection only; consult individual logs |
| Exact rational threshold arithmetic | Passed by ClosureLatest; zero and empty finite sums are allowed in the memory-order theorem |
| Physical interpretation and source identification | Conditional on the cited lane results |
| Numerical scans, convergence and extrapolation to all real scales | Not addressed by Lean |
| Full covariant first variation / ADM / Fourier reduction | Not addressed by these Lean kernels; existing SymPy evidence remains separate |
| Universal signed radial shell field | Not addressed: SV1 assumes each radial component is nonnegative; extension beyond that hypothesis is not certified |
| All positive continuous causal kernels | Not addressed; would require a measure/integrability formulation and pointwise source comparison |
| EW2 H-inf integral bound | Not addressed (EW2 README section 5 explicitly says not Lean-certified) |
| Moving-Sun MS3 and the legacy-factor PN chain | Open in the reviewed record; no label changed |
| Literature, observational likelihoods and raw numerical outputs | Not rerun or independently verified here |

Two numerical presentation cautions are encoded without rewriting lane results:

* EW2's x160 is a rounded ratio; the free-Delta envelope instead leaves x100.
* WL1's q = 0.0354 gives r = 1.07205316, slightly above 1.072. The rounded
  ceiling is not an exact equivalent of the response gate. The reported
  populations exceed either threshold by a large margin.

FA3's reported host range 0.033--0.185 alone does not imply a uniform 0.17
coefficient. A separate source comparison is needed for that coefficient.
The new numerical implication also works with c = 0.033 and host >= 0.816,
**if** web >= c host is established. It does not supply that physical premise.
Cheapest next check: extract the paired, normalized web/host source histories
and verify their pointwise ordering before claiming a kernel-independent
physical exclusion. No lane label is upgraded here.

## Reproduce

With this repository's Mathlib build available:

```sh
python3 closure_2026_11_07/LEAN_CERTIFICATION/verify.py
```

To reuse an existing build of the identical dependency revision:

```sh
python3 closure_2026_11_07/LEAN_CERTIFICATION/verify.py \
  --library-project /absolute/path/to/built/lean_2026
```

The second mode checks matching `lean-toolchain` and `lake-manifest.json`
hashes, then invokes Lean with that project's prebuilt package libraries.
All source files compiled are from this review worktree, not the library copy.
The actual Lean version, source hashes, axiom lists, exit codes and logs are
saved in `verification.json`. It is a build record, not a proof of the verifier.

The PAPER70 literal/source audit and its digit-mutation control are also
rerun; logs are saved alongside the Lean logs. These check textual provenance,
not the truth of numerical source results.

Self-proofreading scope: this README and ClosureLatest only. No existing
mathematical statements or coefficients were edited.


## Follow-up: memory and analytic gaps

The [memory-kernel continuation](../MEMORY_KERNEL_CERTIFICATION/README.md)
proves the continuous comparison with explicit source-ordering hypotheses and
an age-fraction bound for decreasing kernels. It refutes the arbitrary-positive
cross-epoch comparison with a normalized strictly positive kernel. It also
proves the normalized H-inf integral/variation chain and simple-mu error band,
and records an obstruction to the signed-shell algebraic extension. Consult
that report for the remaining physical identifications; the original build
record and its 107 theorem sources are preserved.
