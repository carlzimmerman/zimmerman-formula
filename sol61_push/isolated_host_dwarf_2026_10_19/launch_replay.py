"""Recorded observational replays; only diagnostics differ from the v1 runs."""
import json
import subprocess
import sys
from pathlib import Path
import launch

HERE=launch.HERE; ROOT=launch.ROOT; REL=launch.REL


def replay(label):
    if label not in ('iso','host'):
        raise ValueError('replay label must be iso or host')
    original='base_'+label; name='replay_'+label; output=REL/('run_'+name)
    contract=json.loads((HERE/'contracts'/(original+'.json')).read_text())
    inputs=launch.INPUT_NAMES+['run_dwarf_remnant.py','remnant.py','test_remnant.py','launch_replay.py','DIAGNOSTIC_REFINEMENT.md']
    inputs=[str(REL/f) for f in inputs]
    for f in ['results.json','initial.npz','final.npz','manifest.json']:
        inputs.append(str(REL/('run_'+original)/f))
    contract['execution_artifacts']=inputs
    contract['claim_id']='ISO_HOST_DIAGNOSTIC_REPLAY_'+label
    contract['mathematics']['assertion_tested']='Identical physical evolution to base_'+label+' with repaired remnant centring, full100Myr snapshots, per-particle host receipts; verify initial/final x,v bitwise identity after execution'
    contract['mathematics']['bounds']['case']=name
    path=HERE/'contracts'/(name+'.json'); path.write_text(json.dumps(contract,indent=2)+'\n')
    command=[launch.RUNNER_PYTHON,str(launch.SKILL/'scripts/run_experiment.py'),
             '--root',str(ROOT),'--contract',str(path),'--output',str(output),
             '--timeout','1800','--max-cpu-seconds','1750','--max-threads','1','--max-output-bytes','1048576']
    for item in inputs:
        command+=['--input',item]
    for item in ['results.json','initial.npz','final.npz','trajectory.npz']:
        command+=['--result',str(output/item)]
    command+=['--','nice','-n','19',launch.SIM_PYTHON,str(REL/'run_dwarf_remnant.py'),'--output',str(output)]
    if label=='host':
        command+=['--host','--dt','.5']
    print(json.dumps(dict(case=name,command=command)),flush=True)
    return subprocess.call(command)


if __name__=='__main__':
    for label in sys.argv[1:]:
        code=replay(label)
        if code:
            raise SystemExit(code)
