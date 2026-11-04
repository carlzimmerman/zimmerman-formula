# Reproduction

Run from `/Users/carlzimmerman/new_physics/zimmerman-formula` with the
already installed Python, NumPy and SciPy. The names below are fresh example
destinations; an existing output directory must not be reused.

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py \
 --root /Users/carlzimmerman/new_physics/zimmerman-formula \
 --contract reviews/coupled_trapping_2026_11_04/photino/contract_source.json \
 --input reviews/coupled_trapping_2026_11_04/photino/source.py \
 --input reviews/radial_ir_cold_2026_11_01/gapless_charge/gaugino_threshold.py \
 --input reviews/finite_matching_2026_11_01/two_loop/model.py \
 --input reviews/three_priorities_2026_11_01/spectrum_pressure/spectrum.py \
 --input reviews/gravity_completion_2026_11_03/thermal_kinetic/run_stationary_002/result.json \
 --input reviews/coupled_trapping_2026_11_04/CONTRACT.md \
 --output reviews/coupled_trapping_2026_11_04/photino/run_source005 \
 --result reviews/coupled_trapping_2026_11_04/photino/run_source005/result.json \
 --timeout 240 --max-cpu-seconds 235 --max-threads 1 --max-output-bytes 1048576 \
 -- python3 reviews/coupled_trapping_2026_11_04/photino/source.py \
 reviews/coupled_trapping_2026_11_04/photino/run_source005/result.json

python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py \
 --root /Users/carlzimmerman/new_physics/zimmerman-formula \
 --contract reviews/coupled_trapping_2026_11_04/photino/contract_phase_space.json \
 --input reviews/coupled_trapping_2026_11_04/photino/phase_space.py \
 --input reviews/coupled_trapping_2026_11_04/photino/run_source004/result.json \
 --input reviews/coupled_trapping_2026_11_04/photino/run_source004/manifest.json \
 --output reviews/coupled_trapping_2026_11_04/photino/run_phase002 \
 --result reviews/coupled_trapping_2026_11_04/photino/run_phase002/result.json \
 --timeout 240 --max-cpu-seconds 235 --max-threads 1 --max-output-bytes 1048576 \
 -- python3 reviews/coupled_trapping_2026_11_04/photino/phase_space.py \
 reviews/coupled_trapping_2026_11_04/photino/run_phase002/result.json

python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py \
 --root /Users/carlzimmerman/new_physics/zimmerman-formula \
 --contract reviews/coupled_trapping_2026_11_04/photino/contract_audit.json \
 --input reviews/coupled_trapping_2026_11_04/photino/audit.py \
 --input reviews/coupled_trapping_2026_11_04/photino/run_source004/result.json \
 --input reviews/coupled_trapping_2026_11_04/photino/run_phase001/result.json \
 --output reviews/coupled_trapping_2026_11_04/photino/run_audit002 \
 --result reviews/coupled_trapping_2026_11_04/photino/run_audit002/result.json \
 --timeout 240 --max-cpu-seconds 235 --max-threads 1 --max-output-bytes 1048576 \
 -- python3 reviews/coupled_trapping_2026_11_04/photino/audit.py \
 reviews/coupled_trapping_2026_11_04/photino/run_audit002/result.json
```

The phase and audit scripts deliberately consume the pinned completed
preferred records; a source rerun does not silently redirect those inputs.
To validate existing evidence, use `validate_manifest.py MANIFEST --root
/Users/carlzimmerman/new_physics/zimmerman-formula`. Completed source004,
phase001 and audit001 must validate against current inputs. Failed histories
have since-changed source paths; their original source hashes are checked
against `inputs_historical/archive_map.json`, rather than calling those old
failed manifests fresh evidence.

The orbit, parameter-map and inclusive-current controls can be reproduced
with this bounded runner command. It takes the exact declared execution
inputs from these local contracts and launches the named local scripts;
no command is read from a result or manifest.

```bash
python3 - <<'PY'
import json, subprocess, sys
from pathlib import Path
root=Path('/Users/carlzimmerman/new_physics/zimmerman-formula')
base=Path('reviews/coupled_trapping_2026_11_04/photino')
runner='/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py'
for contract,program,dest in [
 ('contract_orbit.json','orbit_control.py','run_orbit004'),
 ('contract_parameter_map.json','parameter_map.py','run_parameter002'),
 ('contract_current.json','inclusive_current.py','run_current002')]:
    spec=json.loads((root/base/contract).read_text())
    output=base/dest
    result=output/'result.json'
    args=[sys.executable,runner,'--root',str(root),'--contract',str(base/contract)]
    for source in spec['execution_artifacts']:
        args+=['--input',source]
    args+=['--output',str(output),'--result',str(result),'--timeout','240',
           '--max-cpu-seconds','235','--max-threads','1','--max-output-bytes','1048576',
           '--',sys.executable,str(base/program),str(result)]
    subprocess.run(args,cwd=root,check=True)
PY
```
