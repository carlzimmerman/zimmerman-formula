# X57 R4b and X64 C6R corrections

Authorized implementation of the closure audit, 2026-10-27. Scientific outcome:
**X57's general R4b exclusion is withdrawn on both footings; X64 still has no
primary-label separation in the eight tested scalar candidates, but its
pre-existing reported strict-need labelling G now separates under corrected C6R.**
Neither result demonstrates a physical completion. Kappa remains fitted.

The historical scripts, frozen criteria, assumption ledgers and result files
were not changed. New pure correction modules and explicit post-result
amendments are in the corresponding lanes. Their README headers now distinguish
the corrected status from the historical reports.

## Numerical changes

The R4b downward absolute changes needed to enter the two-sigma band are:

| Footing | h=0.672 | h=0.686 |
|---|---:|---:|
| canonical | 0.0007783392 | 0.0195077365 |
| alt | 0.0849533560 | 0.1021842860 |

Because the inherited D=0.3231607504 is described as a fractional response
bound, the comparison uses the corresponding fractional drops:
0.0007794670/0.0195351345 and 0.0850649914/0.1023141176. Every cell yields
“BOUND DOES NOT EXCLUDE.” D is still a conditional generous proxy, not an
independently certified projected-response bound. General positive radial
profiles have an unresolved R4b line; a positive shell demonstrates why density
positivity alone does not fix the shear sign. This changes **M6 alt from
EXCLUDED BY R4b to NOT DECIDABLE**. M1–M4 retain their other failing gates.

C6R evaluates the adopted baryonic potential and enclosed-mass force at the
same reference radius. Its point-mass value is sqrt(2/nu(1))=1.11178594.
Groups, SPARC large and the MW use the same point-mass approximation, so their
primary-label intervals tie exactly and cannot be strictly separated. The
historical C6 overlap of about 0.685 dex is replaced by a zero primary gap.
The eight-candidate null relabelling frequency is now **2/120**, not 3/120.

The pre-existing reported G labelling leaves Groups and Clusters T1
unconstrained because the isolated law already fit them. C6R separates its
remaining retained and excluded classes with gaps **0.2494045764 dex canonical**
and **0.2546064986 dex alt**. The wide labelling, strict intervals and fixed lens
radius primary-label variants still fail. The host-inclusive variant is not
regraded: it needs a specified host geometry. No growth, early-capture,
conservation or dynamical admissibility test has been performed for the G
separation. Its dependence on the adopted Plummer, point-mass and beta-profile
conventions must remain visible.

## Verification and evidence

- [red_v1/manifest.json](red_v1/manifest.json): expected **failed** run. Three
  actual historical implementation regressions fail: upper-band entry,
  zero required correction inside the band, and point-mass C6 invariance.
  Six new-domain checks were deliberately skipped in this historical run.
- [green_v1/manifest.json](green_v1/manifest.json): **completed**, all nine
  targeted tests pass, including the positive-shell counterexample, fractional
  units, below-band direction, Plummer, uniform gas and beta-profile checks.
- [corrected_v1/manifest.json](corrected_v1/manifest.json): **completed**, 1.66 s
  for the child, peak RSS 0.151 GB. Exact commands, top-level input hashes,
  output hashes, interpreter and workspace revision are in the manifest.
- [corrected_v1/provenance.json](corrected_v1/provenance.json): all **201**
  observed scientific/code inputs have equal before/after hashes, including
  external catalogue files. The Python audit hook rejected any attempt to
  mutate outside this new run directory. No attempt occurred.
- Rebuilt historical C6 class intervals match the saved original to
  **1.12e-16 dex**, with identical member counts, before C6R is applied. X19
  class-table and radius checks also pass.

Corrected scientific outputs:
[X57 R4b](corrected_v1/x57_r4b_corrected.json),
[X64 C6R](corrected_v1/x64_c6r_corrected.json).
Seven unchanged X64 candidate intervals are inherited from the saved result;
this is not a full CLASS/EPS rerun or independent revalidation of those inputs.

## Reproduction

Use the existing runtime (no installation was made):

```bash
PYTHONDONTWRITEBYTECODE=1 /Users/carlzimmerman/new_physics/_external_data/tools/pysco_venv/bin/python closure_program_2026_10_27/gate_fixes/test_gate_corrections.py --historical
# expected exit 1: three assertion failures
PYTHONDONTWRITEBYTECODE=1 /Users/carlzimmerman/new_physics/_external_data/tools/pysco_venv/bin/python closure_program_2026_10_27/gate_fixes/test_gate_corrections.py
# expected exit 0: nine tests pass
```

For an isolated new correction run, from the repository root, choose a fresh
output name and execute this Python launcher using that runtime. It expands
the frozen execution-artifact list into the bounded runner's declared inputs;
the result directory must not already exist.

```python
import json, os, pathlib, subprocess, sys
root = pathlib.Path.cwd()
base = pathlib.Path('closure_program_2026_10_27/gate_fixes')
contract = base / 'corrected_contract.json'
output = base / 'corrected_reproduction_001'  # fresh name required
skill = pathlib.Path('/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit')
argv = [sys.executable, str(skill/'scripts/run_experiment.py'), '--root', str(root),
        '--contract', str(contract), '--output', str(output), '--timeout', '180',
        '--max-output-bytes', '1000000', '--max-threads', '1']
for p in json.loads(contract.read_text())['execution_artifacts']:
    argv += ['--input', p]
for name in ['x57_r4b_corrected.json', 'x64_c6r_corrected.json', 'provenance.json']:
    argv += ['--result', str(output/name)]
argv += ['--', sys.executable, str(base/'run_gate_corrections.py'), '--output-dir', str(output)]
subprocess.run(argv, check=True, env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'))
subprocess.run([sys.executable, str(skill/'scripts/validate_manifest.py'),
                str(output/'manifest.json'), '--root', str(root)], check=True)
```

## Remaining obligations

Independent review of the new implication and profile calculations remains
separate from the author's tests. A cluster profile needs exact projected
response, conserved mass and dynamical admissibility before R4b can be decided.
The G-label C6R separation needs robustness to the adopted source profiles and
an actual field/retention mechanism before any physical success claim.
The specified M6 population-versus-forest calculation remains a separate work
package; no physical population limit is inferred from these corrections.
