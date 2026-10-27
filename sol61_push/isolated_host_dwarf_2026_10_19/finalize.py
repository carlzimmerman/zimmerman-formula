"""Record final scientific analysis under a fresh computation manifest."""
import json
import platform
import subprocess
from pathlib import Path
import numpy as np
import scipy
import matplotlib
import launch
from audit_outputs import EXPECTED

HERE=launch.HERE; ROOT=launch.ROOT; REL=launch.REL
inputs=[str(REL/name) for name in ['analyse.py','audit_outputs.py','finalize.py','run_dwarf.py',
        'run_dwarf_remnant.py','dynamics.py','direct_gravity.c','direct_gravity.dylib','remnant.py']]
for name in EXPECTED:
    for f in ('initial.npz','final.npz','results.json','manifest.json'):
        inputs.append(str(REL/('run_'+name)/f))
output=REL/'analysis_run_001'
contract=dict(claim_id='ISO_HOST_FINAL_FINITE_ANALYSIS',
    mathematics=dict(assertion_tested='Finite records for13declared experiments: conservation, identical paired initial dwarf, bitwise diagnostic replay, remnant apertures, numerical controls, fixed-material energy and vector-J transfers',
        coefficient_domain='IEEE754 double with declared tolerances',conventions='Saved pc,Msun,Myr particle states; potential-minimum remnant centre; instantaneous self-unbinding; endpoint comparisons',
        inputs=EXPECTED,bounds=dict(cases=len(EXPECTED),time_Myr=10000,maximum_particles=4608),
        non_claims=['No continuum100pc core confirmation','No canonical full-theory completion','No primordial/source-derived initial conditions','Fixed host has no live response']),
    execution_artifacts=inputs,
    software=[dict(name='analysis Python',version=platform.python_version()),dict(name='numpy',version=np.__version__),dict(name='scipy',version=scipy.__version__),dict(name='matplotlib',version=matplotlib.__version__)],
    randomness=dict(used=False,generator='',seed=None))
path=HERE/'contracts'/'final_analysis.json';path.write_text(json.dumps(contract,indent=2)+'\n')
command=[launch.RUNNER_PYTHON,str(launch.SKILL/'scripts/run_experiment.py'),'--root',str(ROOT),
         '--contract',str(path),'--output',str(output),'--timeout','180','--max-threads','1','--max-output-bytes','1048576']
for item in inputs:command+=['--input',item]
for item in ('analysis.json','comparison.csv','isolated_host_comparison.png','same_material_transfer.json','same_material_transfer.csv','audit.json'):
    command+=['--result',str(output/item)]
command+=['--','nice','-n','19',launch.SIM_PYTHON,str(REL/'audit_outputs.py'),'--output',str(output)]
if __name__=='__main__':
    raise SystemExit(subprocess.call(command))
