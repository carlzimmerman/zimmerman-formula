# Fine-structure puzzle: handoff to Claude

Prepared 2026-10-19 at the user's request. Scientific cutoff: **FSP-010**.
Repository HEAD observed before this handoff: `e54c33252909e38a529a69f7adac265e37b54cb4`.

## Assignment and current answer

Continue the programme in [fine_structure_puzzle](fine_structure_puzzle/README.md).
The user wants a rigorous physical derivation of the fine-structure constant,
especially through QCD/QED vacuum response and proton matching, with parallel
subagents and no numerical fitting to the measured answer. They regard earlier
loop coincidences as numerology and want an actual mechanism or useful overlooked
piece. Be ambitious about calculations and candid about their limits.

**Alpha has not been derived. The full physical proton electromagnetic response,
smooth curved-space QCD coefficient, ratio, and finite-alpha dependence have not
been calculated.** FSP-010 is partial progress, not a breakthrough claim.

The immediately preceding request was to push further on the full proton response
and physical smooth curved-space QCD, including missing mass and electromagnetic
responses. The user then redirected this session to preparing this handoff and
pushing the files. No FSP-011 scientific calculations or new research packages
were started. A read-only subagent checked the facts needed for this handoff.

## Read these first

1. [Target contract](fine_structure_puzzle/TARGET.md): precise success criteria.
2. [Live status](fine_structure_puzzle/STATUS.md) and
   [FSP-010 checkpoint](fine_structure_puzzle/checkpoints/FSP-010.md).
3. [FSP-010 synthesis](fine_structure_puzzle/qcd_hard_vacuum/REPORT.md).
4. [Review reconciliation](fine_structure_puzzle/qcd_hard_vacuum/reviews/RECONCILIATION.md):
   restrictions that govern broader wording in frozen author files.
5. [Current continuation](fine_structure_puzzle/HANDOFF.md),
   [route index](fine_structure_puzzle/qcd_hard_vacuum/ROUTES.md), and
   [reproduction instructions](fine_structure_puzzle/qcd_hard_vacuum/REPRODUCE.md).
6. [Pinned checkpoint](fine_structure_puzzle/CHECKPOINT.json).

Load older material through these links when a specific dependency needs it.
[HISTORY.md](fine_structure_puzzle/HISTORY.md) indexes earlier phases; it is not
necessary to read the entire archive before doing useful work.

## Definitions and differentiation path

Use the conventions in the actual derivations, particularly the signs of current
insertions and Euclidean stress. The common notation is

```text
u = e^2 = 4 pi alpha,
W = -log Z,
V = Omega H^(-4),  Omega = 8 pi^2 / 3,
t = log(radius),   rho = W_t / (4 V),
rho(H,u) - rho(0,u) = A(u) H + o(H),
R(u) = A(u) / M_p(u)^3,
dR/dalpha = 4 pi [A_u/M_p^3 - 3 A M_p,u/M_p^4].
```

The radius, charge, mass, regulator, continuum and differentiated-remainder limits
must be justified. Both observables must use the same fixed renormalized physics
path; retuning the proton mass or changing the matching scale while differentiating
can change the question. The expansion above defines a target coefficient; its
existence and nonzero value in physical QCD have not been established here.

Calculating R(alpha), even if successful, does not by itself select alpha. The
original goal additionally requires an independently justified selection equation,
fixed UV inputs and physical charge normalization, uniqueness, running/matching
to the Thomson limit, uncertainty and independent observational checks. A measured
alpha input, fitted missing matrix element, or chosen boundary condition is not
a prediction.

## What FSP-010 actually established

### Local proton matching

The [hard-proton package](fine_structure_puzzle/qcd_hard_vacuum/hard_proton/REPORT.md)
derives the leading sharp-O(4)-photon-cutoff to MSbar quark conversion:

```text
M_u,ct^q = sum_f Q_f^2 sigma_f^p
           [3 log(mu^2/Lambda^2) + 5/2] / (16 pi^2),
sigma_f^p = m_f partial M_p / partial m_f.
```

The source-calibrated `0.8243609709 MeV per e^2` at `mu=Lambda` is a local
conversion using imported scalar, scale and mass information. It is not a full
proton electromagnetic mass or a fit-free ab initio prediction. New 2026 lattice
form-factor stencils are finite-spacing light-current functionals on a limited
momentum interval. Their source fits/calibrations remain inputs. They omit the
full non-Born and all-flavor electromagnetic response, missing momenta and a
controlled continuum extrapolation. Do not sum them with local terms as a full
answer.

The [finite-gluon package](fine_structure_puzzle/qcd_hard_vacuum/gluon_matching/REPORT.md)
translates primary two-loop decoupling formulae, independently reconstructed by
a source-first reviewer. For `k=1/(16 pi^2)`, `L=log(s/mu^2)` and
`S_Q=sum_f Q_f^2`, the displayed operator matching is

```text
(g_s,EFT - g_s,full)/u = k^2 g_s^3 S_Q [L - 3/4],
(m_f,EFT - m_f)/(u m_f)
  = k Q_f^2 [-3L + 5/2]
    + k^2 g_s^2 C_F Q_f^2 [-3L + 17/4] + higher orders.
```

Sequential matching must subtract both the top-QED threshold and its induced
mass threshold, with the correct intermediate flavor count. These are results
known after source translation, not a new fundamental-physics discovery. The
source/vector/contact and separate sharp-cutoff filter-moment hypotheses matter.
The canonical gluon matrix element scales as `1/g_s^2`; the next unknown gluon
Wilson coefficient contributes at the hadronic order of the known mixed-quark
term. Consequently this is **not complete NLO hadronic accuracy**. The massless
three-flavor local subtraction `-1/(288 pi^2)+O(alpha_s)` is not physical massive
QCD or the full proton mass.

### All-scale reconstruction

The [hard bridge](fine_structure_puzzle/qcd_hard_vacuum/hard_bridge/REPORT.md)
reconstructs the mass from derivatives across **all** positive photon masses plus
the calculated UV endpoint. Complete Dirac benchmarks verify the finite endpoint
identity; a soft response alone does not recover the hard mass. Explicit derivative
endpoint conditions are required: a function `O(sqrt(s))` bound does not imply
them. Physical QCD still needs running/mixing, contacts, the intermediate-scale
response and a controlled tail.

### Actual unconditioned vacuum calculations, with finite scope

The [pure-gauge calculation](fine_structure_puzzle/qcd_hard_vacuum/global_qcd/REPORT.md)
uses normalized SU(3) Haar measure on the closed cubical family
`K_n = boundary[0,n]^5`, with `Z(0)=1` and no topology conditioning. Its K1 series
through beta^9 includes a collective cube term with coefficient `5/236196` at
beta^6. Its tiny-beta error bound concerns that finite model, not physical bare
coupling or the continuum limit. Support completeness has the restricted meaning
in the review, not every ordinary connected plaquette set or every n.

The [charged-sea calculation](fine_structure_puzzle/qcd_hard_vacuum/coordinator/sea_hodge/REPORT.md)
uses an explicitly defined integer-flavor staggered determinant and noncompact
photon. Its actual leading coefficient is

```text
W_u at order beta*kappa^4
  = beta*kappa^4 (sum_f q_f^2) (30n^4 + 20n^2 - 1) / 6.
```

This includes the photon covariance, current and contact pieces. The calculated
sectors lack an n^3 term. They do **not** prove physical A=0 or A_u=0. Ambient
staggered phases, heavy hopping and a finite-spacing polyhedral radius family
have not been matched to physical continuum spin/taste transport on a smooth
round sphere.

### A useful constraint on combining the pieces

The [common UV ratio note](fine_structure_puzzle/qcd_hard_vacuum/coordinator/COMMON_UV_RATIO.md)
and [restriction](fine_structure_puzzle/qcd_hard_vacuum/coordinator/COMMON_UV_RATIO_RESTRICTION.md)
show conditionally that a universal QCD scale shift cancels in A/M_p^3. At
physical nonzero quark masses, quark-mass derivatives of A remain necessary;
proton sigma terms alone do not provide them. Division by beta_s requires a
nonzero value or a separately controlled limit.

An earlier [charge-exchange comparison](fine_structure_puzzle/qcd_nonborn_vacuum/common_response/REPORT.md)
also matters: at equal up/down masses, swapping their charges leaves the full
unconditioned vacuum invariant while exchanging proton and neutron responses.
It prevents a proposed flavor-covariant Ward identity from reconstructing the
entire proton non-Born tensor from only that vacuum functional. It is not a
general impossibility result for a dynamical relation at physical parameters.

## Next work that would change the answer

Use disjoint subagent scopes and have a separate reviewer derive each critical
step before seeing its author's verdict. A useful continuation must change the
recorded stuck step, not just repeat a soft or heavy-matter benchmark.

1. **Full proton response:** identify or calculate all-current, non-Born
   two-current data across the required scales, including disconnected insertions,
   matching contacts and finite mass dependence. Complete higher gluon matching
   with consistent operator evolution and flavor thresholds. Establish the
   conversion onto the common fixed-physics path and control the remaining tail.
   Existing Born stencils and local Wilson coefficients do not fill this gap.
2. **Physical smooth curved-space vacuum:** construct and match one smooth
   round-sphere gauge/fermion regulator with an absolute measure and specified
   current/gravity normalization. Evaluate actual normalized mass/coupling
   integration and the metric/current/contact cumulants at physical quark masses.
   Control the continuum, large-radius and charge-derivative limits. A flat
   condensate, baryon form factor, thermal Rindler probe or higher finite cubical
   Taylor coefficient is insufficient by itself.
3. **Joint ratio and selection:** calculate A, A_u, its needed quark-mass
   derivatives and M_p,u on the same path before assigning R or dR/dalpha.
   Higher charge responses or finite-u dynamics are needed for finite-alpha
   dependence. Then separately test a predictive alpha-selection mechanism.

No physical smooth-sphere QCD ensemble or full all-current proton dataset was
produced here. New large external jobs, installations or paid resources were not
started. If those inputs cannot be obtained, record the exact remaining
observable and its acquisition requirements rather than fitting a coefficient.

## Evidence and working rules

- Preserve executed science, source checks, reviewer cutoffs and old snapshots.
  Before changing navigation, take a new checkpoint as the existing programme
  does. Do not refresh old hashes to hide a changed input.
- [Final manifest assessment](fine_structure_puzzle/qcd_hard_vacuum/reviews/FINAL_MANIFEST_VALIDATION.json)
  distinguishes five current authoritative science executions, one completed
  predecessor, four completed review executions, three retained failed diagnostics
  and one original completed record with a stale administrative input. A valid
  record can document a failed run; it is not a physics proof.
- Updating live HANDOFF.md made the original hard-proton run's administrative
  input stale. The [current replay](fine_structure_puzzle/qcd_hard_vacuum/coordinator/hard_proton_replay/REPRODUCE.md)
  uses the byte-identical archived input and gives byte-identical numerical
  output. The original record and separate replay review are retained.
- The previous final audit checked 1,737 programme inventory entries, 189 current
  phase inventory entries, 62 checkpoint pins, 186 review comparisons, all 14
  current-phase manifests with their proper classifications, and 1,535 unchanged
  parent science files. This is mechanical evidence, not validation of missing
  physical limits. See the actual records for scope and exclusions.
- Historical commands contain author-machine absolute paths. Read each contract
  and REPRODUCE.md before rerunning into a new output directory. The mathbox
  validator/runner is a local Codex skill, not a bundled repository dependency.
  Observed numerical tools included Python 3.9.6, SymPy 1.14.0 and mpmath 1.3.0;
  individual manifests are authoritative about each run.
- This is a shared working tree with extensive unrelated changes. Commit only
  explicitly owned paths. No Git history rewriting, broad staging, publication,
  author messages or automated follow-ups are part of this handoff.

## What is transported in Git

The handoff commit includes the programme's original reports, code, run records,
results, source receipts and immutable hash inventories. Downloaded papers,
paper source archives/full-text extractions and paper-page screenshots remain
local. Their omitted paths, hashes and sizes are recorded in
[FINE_STRUCTURE_HANDOFF_TO_CLAUDE_SOURCES.json](FINE_STRUCTURE_HANDOFF_TO_CLAUDE_SOURCES.json).
The newer ignored `.research-cache/` is also local and is not transported.

The original inventories are intentionally unchanged and therefore include some
untransported source paths. On a fresh clone, a full inventory check will report
those missing sources until the exact versions are restored. Source receipts and
primary identifiers tell you what to obtain; PDF layout extraction may vary, so
do not claim byte identity merely from a matching arXiv identifier. Cache/source
availability and scientific applicability are separate checks.

To verify all transported programme artifacts without treating declared source
omissions as corruption, run from the repository root:

```bash
python3 - <<'PY'
from pathlib import Path
import hashlib, json
root = Path.cwd()
packet = json.loads((root / 'FINE_STRUCTURE_HANDOFF_TO_CLAUDE_SOURCES.json').read_text())
omitted = {item['path'] for item in packet['omitted_source_files']}
base = root / 'fine_structure_puzzle'
checked = missing_sources = 0
for line in (base / 'ARTIFACTS.sha256').read_text().splitlines():
    expected, relative = line.split('  ', 1)
    path = base / relative
    if not path.exists() and str(path.relative_to(root)) in omitted:
        missing_sources += 1
        continue
    assert path.is_file(), str(path)
    assert hashlib.sha256(path.read_bytes()).hexdigest() == expected, str(path)
    checked += 1
print({'verified_files': checked, 'declared_missing_source_files': missing_sources})
PY
```

Resume from FSP-010. The scientific target remains open.
