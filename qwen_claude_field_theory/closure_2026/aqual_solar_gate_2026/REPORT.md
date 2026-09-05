# Gate 1: exact exponential AQUAL remains strongly adverse, not fully certified

Date: 2026-09-04 (America/New_York).

**Verdict:** the completed numerical checks support a Solar-System conflict for
the specified exponential AQUAL static branch. The formal audit remains **OPEN**:
the stricter 1e-11 iteration check exhausts its cap, and no certified continuum
error bound or independent PDE discretization has been supplied. No full
relativistic theory, universal no-go, or new law of nature is claimed.

## Results

The equation is exactly

\[
 \nabla\cdot[(1-e^{-|\nabla\Phi|/a_0})\nabla\Phi]
 =4\pi G M_\odot\delta^{(3)}(\mathbf x),
 \qquad \nabla\Phi\longrightarrow-g_{\rm ext}\hat{\mathbf z}.
\]

The dimensionless solver uses GM=a0=1. With
Phi_2=c2*r^2*P2(cos theta), the physical quadrupole is
Q2=-3*c2*a0^(3/2)/sqrt(GM_sun), including its sign. This follows from
Park et al.'s equation (6), not calibration to an expected numerical result.

| Calculation | Q2 [s^-2] |
| --- | ---: |
| 256 x 64 grid | 2.12977e-26 |
| 512 x 128 grid | 2.10272e-26 |
| 768 x 192 grid | 2.09783e-26 |
| Canonical a0, lower adopted external-field endpoint | 2.15416e-26 |
| Canonical a0, upper adopted external-field endpoint | 1.99586e-26 |
| Alternative a0=1.1279e-10 m/s^2 | 2.85051e-26 |
| Independent 2011 exponential-kernel benchmark configuration | 2.98080e-26 |

Medium-to-fine change is 0.233%. Moving inner/outer boundaries, or changing
their prescriptions, changes the baseline by at most 0.017% in the tested
cases. Angular-order/radial-fit variations on the baseline stay within 0.089%.
These are measured sensitivities, **not rigorous discretization-error bounds**.

The independent Blanchet-Novak benchmark is about 3.0e-26 s^-2, reproduced
within 0.64%. It uses this exact exponential function, not the inverse RAR.
The published Cassini estimate is Q2=(1.6 +/- 1.8)e-27 s^-2; its mean+2sigma
upper endpoint is 5.2e-27. The canonical fine-grid prediction is 4.03 times
that endpoint. Across the tested canonical external-field endpoints the
ratios remain 3.84--4.14. These comparisons are conditional on the stated
physical inputs and model; they are not a new joint posterior or a new
analysis of raw Cassini tracking data. Primary sources and translations are
recorded in CONTRACT.md.

## Numerical failure retained

Thirteen of fourteen cases complete at their requested tolerance. The
1e-11 pointwise iteration criterion does not complete within 160 iterations.
The aggregate therefore exits **1**, not 0. The instrumented rerun retains
the last eight updates and quadrupole coefficients in results.json. Even if
the quadrupole is stable there, that does not satisfy the failed criterion.
The cause of the stopping floor is not established merely by observing it.

The completed cases have small discrete cell flux imbalances, recorded per
case. Small residuals do not bound continuum error near the degenerate
zero-field saddle. The next numerical step is a differently discretized or
higher-precision solve that resolves the stricter stopping issue and supplies
an independent error assessment. Do not spend a new covariant construction
as though the static branch had passed.

## What was corrected, and what was not

The inherited extraction uses continuous Legendre orthogonality on discrete
midpoint weights. Their weighted P2 moment is nonzero, leaking spherical
radial errors into the quadrupole. A synthetic spherical potential is a
decisive counterexample: its true quadrupole is zero, while the legacy
extractor reports a nonzero coefficient. New tests require the corrected
extraction to remove this leakage and recover independent mixed harmonics.

The new extraction simultaneously fits angular modes and includes a decaying
r^-3 quadrupole in the radial fit. The nonlinear solve retains the original
finite-volume operator, but measures updates pointwise so the large inner
monopole cannot hide changes near the MOND transition. The inherited solver
file is unchanged. Fixing this extraction defect does **not** erase the
observational conflict in the completed runs.

## Why the next action cannot simply hide this result

**Scoped static-equivalence lemma (standard monotonicity argument).** On a
bounded domain, take two sufficiently regular weak solutions with the same
source and Dirichlet boundary data, permitting their difference as a test
function. Let A(p)=(1-exp(-|p|/a0))*p. Subtracting the field equations gives

\[
 \int_\Omega(\nabla\Phi_1-\nabla\Phi_2)\cdot
 [A(\nabla\Phi_1)-A(\nabla\Phi_2)]\,d^3x=0.
\]

A is strictly monotone: its radial/tangential derivative eigenvalues are
positive away from p=0, and integrating along a nontrivial segment retains
strict positivity even if the segment crosses p=0. Hence the gradients agree;
equal boundary data fixes the additive constant. Uniform ellipticity at p=0
is not needed for this uniqueness implication.

Apply this to finite annuli with matching inner/outer data; extension to a
point-source/infinite-domain limit requires existence, admissibility and
boundary control, not supplied by this lemma. Consequently, two relativistic
actions with exactly the same applicable static equation, physical potential
and boundary data cannot produce different static quadrupoles on this branch.
The claim is a formal consequence of standard monotonicity, not an originality
claim or a no-go for actions with genuinely different static limits.

## Latest concurrent commits

The run started at 90eaf42dd. During it, 6b1a57be2 added a coherence-length
proposal and c8adf0d7b updated the standing summary. Their files were not
modified. f29 uses a smoothed-source **QUMOND/RAR** construction, not the
exact unsmoothed exponential AQUAL equation tested here. It is a distinct
candidate extension, not an automatic escape for this frozen requirement.
Its full action and health claims have not been audited in this study.

## Files and commands

Only this new folder is changed:

- audit.py: solver wrapper, extraction, bounded case runner and provenance.
- test_audit.py: eight independent behavior tests.
- CONTRACT.md: frozen range, criteria, assumptions and primary-source ledger.
- REPORT.md: interpretation and remaining gap.
- results.json: all completed cases, extraction variants and failure records.
- computation_manifest.json: actual command, software, input/output hashes,
  starting/ending commit, dirty state and execution status.

Commands from the repository root (PYTHONDONTWRITEBYTECODE=1 for each):

| Command after the environment prefix | Exit / result |
| --- | --- |
| `python3 -m unittest discover -s qwen_claude_field_theory/closure_2026/aqual_solar_gate_2026 -v` | 0; 8 tests pass after initial test-first failure |
| `python3 qwen_claude_field_theory/closure_2026/aqual_solar_gate_2026/test_audit.py -q` | 0; direct execution passes |
| `python3 qwen_claude_field_theory/closure_2026/aqual_solar_gate_2026/audit.py` | 1; 13 cases complete, 1 strict-tolerance case fails |
| `python3 -m unittest discover -s qwen_claude_field_theory/closure_2026/finite_interval_mond_2026 -q` | 0; 26 existing tests pass |
| `python3 -m unittest discover -s hunt_2026/exact_mu_cassini_2026 -q` | 0; 6 existing QUMOND tests pass, not AQUAL certification |

Manifest validation command:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/2.2.0/skills/computation-audit/scripts/validate_manifest.py qwen_claude_field_theory/closure_2026/aqual_solar_gate_2026/computation_manifest.json
```

Validation exit 0 checks structure only; hashes are separately recomputed.
Development: eight initial tests failed before implementation; later one
regression failed until nonconvergence diagnostics were retained. Neither
development failure is hidden or counted as physical evidence. The final
instrumented numerical run remains intentionally nonzero on the failed gate.

**Status:** full relativistic goal OPEN; this static branch is strongly
disfavoured under the tested assumptions; the numerical gate is not fully
closed. No action or requirement was changed to manufacture a pass.
