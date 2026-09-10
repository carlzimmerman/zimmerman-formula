# Lapse preservation residual audit

Base: `81ef7508749fe36fcad8882ea494fe567d868e67`, 2026-09-10.
The original `dirac_operator/` code and evidence are unchanged.

**Verdict: implementation and finite assertion verified in the stated range.**
The reported roundoff residual is the residual of the finite-difference matrix
equation. Applying the differential lapse operator to the computed lapse gives
a larger residual that converges at approximately second order. This is
consistent with the original report, which explicitly calls its number a
linear-system residual. It is not a refutation of the clock-sector calculation.

The check uses amplitude 0.05 at the original single clock epoch, periodic plane
data, and float64 arithmetic. It observes the returning frame of the unchanged
`lapse_source.case` function to retrieve its coefficients and solution. It then
independently assembles the sampled differential residual using FFT derivatives:

\[
R=-\partial_x(a_2\partial_xN)+\sqrt h\,\mathrm{mass}\,N-\sqrt h F_0.
\]

This reuses the original source, mass coefficient, and constraint solver. It is
an orthogonal consistency check of the matrix solution against the differential
operator, not an independent reimplementation of the entire action.

| Modes / mesh | Matrix residual max | Sampled differential residual max | Relative to RHS max | Observed order |
|---|---:|---:|---:|---:|
| 8 / 64 | 9.8012e-17 | 1.5488e-7 | 2.7785e-5 | — |
| 16 / 128 | 3.3567e-16 | 3.8654e-8 | 6.9343e-6 | 2.00246 |
| 32 / 256 | 1.6757e-15 | 9.6594e-9 | 1.7328e-6 | 2.00062 |

The lapse stays positive in all three discrete solves. The 32-mode sampled
range is approximately 0.9955438158 to 1.0064379842. The analytic sine/cosine
derivative control has maximum error below 1.5e-13. Raw constraint residuals,
source and mass minima, and all numeric values are in `run_001/results.json`.

The differential residual is sampled on the existing mesh for trigonometric
interpolants. It is not an interval-certified continuum norm or a rigorous
solution error bound. Refinement changes both the constraint Fourier truncation
and the lapse finite-difference mesh. The calculation does not establish a
global inverse, positive lapse during evolution, unrestricted 3D closure, a
MOND coupling, or observational validity.

An independent action-level audit also reproduced the signs of the zero-lapse
source and its fixed-canonical-momentum clock correction, and the principal
tensor's positive eigenvalues under the stated regular-domain assumptions.
The existing `derive.py`, `ellipticity.py`, `lapse_source.py`, and
`Ellipticity.lean` were rerun successfully. Pointwise principal positivity still
does not establish the full inverse or constrain the source sign on all data.

The cheapest next numeric improvement is to retain this differential residual
as the preservation diagnostic. For a proposed MOND completion, the necessary
next physics calculation is the constraint chain and lapse source of the
**combined action**; these clock-sector checks do not transfer automatically.

## Reproduction and provenance

`check_residual.py` rejects changed versions of its two original code inputs.
`contract.json` fixes the finite assertion, bounds, software versions, and
non-claims. `run_001/manifest.json` records the actual command, base commit,
dirty state, input hashes before and after, output hashes, actual exit 0,
1.873905-second runtime, 90-second wall cap, 60-second CPU cap, 65536-byte log
cap, and cooperative one-thread numerical-library setting. No memory or CPU
affinity cap was requested. No random sampling or package installation occurred.

Actual child command, from the repository root (exit 0):

```bash
python3 -B qwen_claude_field_theory/closure_2026/clock_response_repair_2026/lapse_residual_audit/check_residual.py --result-file qwen_claude_field_theory/closure_2026/clock_response_repair_2026/lapse_residual_audit/run_001/results.json
```

Use a fresh result path when rerunning; preserve `run_001/`. For a new complete
manifest, use the installed computation-audit `run_experiment.py` with this
contract and its three `execution_artifacts`, a fresh output directory, and the
recorded limits. The recorded result was validated with the exact command in
`verification.json`, exit 0: “valid evidence record; mathematical interpretation
requires review.”

SHA-256 identifiers:

| Artifact | SHA-256 |
|---|---|
| `check_residual.py` | `d1e6c5eff244e89c2dea8e9e2c25751e31413238b4ec10fa60e039d51db8bf20` |
| `run_001/results.json` | `11f540c0f9f8d8f872b7baa0c968b1674107646ea2c67a7396f72055ed4917f2` |
| `run_001/manifest.json` | `f223b2f8bd5fbc90e28afab37b39517d3bfc5abda08a8cd01ea26db83a067cde` |
| Original `derive.py` | `c31e6c72740b404a7db92abde6ad4c022874b7758b08889b3dba78fe28bc3553` |
| Original `constraint_data.py` | `0d31f01de91f92909612bf19b5095d3fd789e53816ede6b26d6733c284fd9397` |
| Original `lapse_source.py` | `2f8f72b343b346a2e5922c098ddb6bcd14824ce4a610558f41f34e85d945a3a8` |
| Original `Ellipticity.lean` | `6ea19db1d92e12cbe21807c803b1b1f1746283d3315b36e148f94df49dbf57db` |
| Original `README.md` | `0988416512fca801649648177ce5e5d7dee9eea4308d4023474da66601b2efcd` |

Mathbox proof-audit guided the independent sign/domain review;
computation-audit guided the bounded run, manifest, and limited interpretation.
